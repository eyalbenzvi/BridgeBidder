"""Deal generator: repeatedly plays deals until BEN beats our engine, then
reports the losing deal over a WebSocket connection.

Blocking calls (BEN subprocess, double-dummy, play_table) are dispatched to a
thread-pool executor so the event loop is never blocked.
"""

from __future__ import annotations

import asyncio
import json
import random
import sys
import uuid
from collections import deque
from pathlib import Path
from typing import TYPE_CHECKING

# Make tools/ importable so compare_ben.Ben is available.
_TOOLS_DIR = Path(__file__).parents[4] / "tools"
if str(_TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(_TOOLS_DIR))

from compare_ben import Ben, BEN_PYTHON  # noqa: E402
from bridgebidder.domain.cards import FULL_DECK, Hand
from bridgebidder.domain.calls import Call
from bridgebidder.domain.types import Seat, Vulnerability
from bridgebidder.domain.auction import Auction
from bridgebidder.engine.dd import EndplayDD, get_dd
from bridgebidder.engine.decision import decide_fast, fast_decision
from bridgebidder.engine.explain import build_explanation
from bridgebidder.engine.scoring import imps, signed_score
from bridgebidder.inference.engine import prepare_decision, DecisionSetup
from bridgebidder.system.dsl import load_system

if TYPE_CHECKING:
    from bridgebidder.system.dsl import BiddingSystem

# ---------------------------------------------------------------------------
# module-level singletons (lazy)
# ---------------------------------------------------------------------------

_ben: Ben | None = None
_dd: EndplayDD | None = None
_system: "BiddingSystem | None" = None

VULS = [Vulnerability.NONE, Vulnerability.NS, Vulnerability.EW, Vulnerability.BOTH]
MAX_CALLS = 60

# Store last 10 deals so explanation can be retrieved.
_active_deals: "dict[str, dict]" = {}
_active_deal_order: "deque[str]" = deque(maxlen=10)


def ben_available() -> bool:
    """Whether the BEN worker can actually be spawned on this machine.

    `Ben()` constructs happily anywhere -- the model is loaded lazily by the
    subprocess -- so the only honest check is whether the interpreter it
    execs exists.  Without it every `ask()` dies with FileNotFoundError in the
    middle of a WebSocket stream, which is a far worse failure than declining
    the feature up front.
    """
    return Path(BEN_PYTHON).exists()


def dd_available() -> bool:
    """Whether the real double-dummy solver is installed.

    `get_dd()` falls back to a HCP/shape heuristic when `endplay` is missing.
    That is fine for a smoke test and useless for scoring: a verdict computed
    on estimated tricks is a made-up number wearing a t-statistic.  Callers
    that score boards must check this rather than trust whatever get_dd hands
    back.
    """
    try:
        EndplayDD()
        return True
    except Exception:
        return False


def _get_ben() -> Ben:
    global _ben
    if _ben is None:
        _ben = Ben()
    return _ben


def _get_dd() -> EndplayDD:
    global _dd
    if _dd is None:
        _dd = get_dd()
    return _dd


def _get_system() -> "BiddingSystem":
    global _system
    if _system is None:
        _system = load_system()
    return _system


# ---------------------------------------------------------------------------
# synchronous play_table variant that captures DecisionSetup per our call
# ---------------------------------------------------------------------------


def play_table_with_setups(
    system: "BiddingSystem",
    ben: Ben,
    deal: dict,
    dealer: Seat,
    vul: Vulnerability,
    our_side: str,
) -> "tuple[Auction, list[dict], dict[int, tuple[DecisionSetup, Call]]]":
    """Play one table and return (auction, our_calls, setups_by_n).

    setups_by_n maps call-index-in-auction -> (DecisionSetup, Call) for every
    call our engine makes.  This allows the explanation layer to reconstruct
    the full decision context later.
    """
    auction = Auction(dealer=dealer, vulnerability=vul)
    hands = {s.value: str(deal[s]) for s in Seat}
    our_calls: list[dict] = []
    setups_by_n: dict[int, tuple[DecisionSetup, Call]] = {}

    while not auction.is_complete:
        seat = auction.next_seat
        n = len(auction.calls)
        if seat.side == our_side:
            setup = prepare_decision(system, auction, perspective=seat)
            # Read the rule off the candidate that won, not the first declared
            # candidate making the same call -- see the note in
            # tools/match_ben.py:play_table.
            chosen, _by_call, _clear = fast_decision(setup, deal[seat])
            call = chosen.call
            rule_id = chosen.candidate.rule.id if chosen.candidate.rule else "fallback"
            setups_by_n[n] = (setup, call)
            our_calls.append({"seat": seat.value, "call": str(call), "rule": rule_id, "n": n})
        else:
            resp = ben.ask({
                "hands": hands,
                "dealer": dealer.value,
                "vuln_ns": int(vul.is_vulnerable(Seat.N)),
                "vuln_ew": int(vul.is_vulnerable(Seat.E)),
                "auction": [str(c) for c in auction.calls],
            })
            call = Call.parse(resp["bid"])
            if not auction.is_legal(call):
                call = Call.parse("P")
        auction.add(call)
        if len(auction.calls) > MAX_CALLS:
            break

    return auction, our_calls, setups_by_n


# ---------------------------------------------------------------------------
# synchronous deal scoring
# ---------------------------------------------------------------------------


def _score_table(auction: Auction, deal: dict, vul: Vulnerability) -> tuple[int, int | None]:
    """Return (score_ns, tricks | None)."""
    dd = _get_dd()
    c = auction.contract
    if c is None:
        return 0, None
    tricks = dd.tricks(deal, c.declarer, c.strain)
    return signed_score(c, tricks, vul, "NS"), tricks


def _play_both_tables(
    system: "BiddingSystem",
    ben: Ben,
    deal: dict,
    dealer: Seat,
    vul: Vulnerability,
) -> dict:
    """Play both orientations and return a complete result bundle."""
    a_auction, a_calls, a_setups = play_table_with_setups(system, ben, deal, dealer, vul, "NS")
    b_auction, b_calls, b_setups = play_table_with_setups(system, ben, deal, dealer, vul, "EW")

    a_score, tricks_a = _score_table(a_auction, deal, vul)
    b_score, tricks_b = _score_table(b_auction, deal, vul)

    return {
        "a_auction": a_auction,
        "a_calls": a_calls,
        "a_setups": a_setups,
        "a_score": a_score,
        "tricks_a": tricks_a,
        "b_auction": b_auction,
        "b_calls": b_calls,
        "b_setups": b_setups,
        "b_score": b_score,
        "tricks_b": tricks_b,
    }


# ---------------------------------------------------------------------------
# public explanation accessor
# ---------------------------------------------------------------------------


def register_deal(deal_id: str, deal_dict: dict, setups: dict) -> None:
    """Put a deal and its captured decision setups in the explain cache.

    Shared by both deal sources -- the live BEN search and the pool replay in
    `corpus_deals` -- so `/api/deals/{id}/explain/...` serves either without
    knowing which produced the board.
    """
    if len(_active_deal_order) == _active_deal_order.maxlen:
        _active_deals.pop(_active_deal_order[0], None)
    _active_deals[deal_id] = {"deal": deal_dict, **setups}
    _active_deal_order.append(deal_id)


def _norm_lengths(requires: dict) -> dict:
    """Suit-length bounds keyed by lowercase letter.

    The DSL writes suits uppercase; the editor form reads and writes them
    lowercase and diffs the two to decide what the user actually changed.
    Left unnormalised, every suit compares unequal and a patch that touched
    nothing reports four length changes.
    """
    raw = requires.get("suits") or requires.get("lengths") or {}
    return {str(k).lower(): list(v) for k, v in raw.items()}


def _candidate_row(sc, chosen: bool = False) -> dict:
    rule = sc.candidate.rule
    return {
        "call": str(sc.call),
        "rule_id": rule.id if rule else "fallback",
        "shows": rule.shows if rule else "",
        "priority": rule.priority if rule else None,
        "fit": round(sc.fit, 4),
        "score": round(sc.score, 4),
        "chosen": chosen,
    }


def _winning_candidate(setup, hand, call):
    """The candidate the engine actually selected for `call`, if it selected it.

    Two rules can produce the same call, and then "which rule fired" has two
    plausible answers that disagree.  `score_candidates` sorts by score, but
    the engine does not take the top of that list: `fast_decision` picks by
    priority first among candidates that clear the fit threshold.  Reading the
    rule off score order therefore names the wrong rule whenever a lower-
    priority rule happens to score higher -- observed on about 5% of calls,
    quietly, since the call shown is identical either way and only the rule id
    differs.  So ask the decision function itself.

    When the recorded call is not what the engine would choose now (the system
    has moved since the board was recorded), `fast_decision` is answering a
    different question, and the best-scoring candidate for the recorded call is
    the closest honest answer.
    """
    from bridgebidder.engine.decision import fast_decision, score_candidates

    ranked = score_candidates(setup, hand)
    try:
        chosen, _by_call, _clear = fast_decision(setup, hand)
    except Exception:
        chosen = None
    if chosen is not None and chosen.call == call:
        return chosen, ranked
    return next((sc for sc in ranked if sc.call == call), None), ranked


def get_explanation(deal_id: str, table: str, call_n: int) -> dict:
    """Explain one of our calls, in the shape the inspector renders.

    `build_explanation` is the engine's own structured output and stays that
    way; this adds what the panel needs on top of it -- the rule's identity and
    its *own* `requires` (not the interpreted constraint, which is merged with
    inference and would write derived values back into the rulebook if the
    editor started from it), plus the full scored candidate list, which is the
    whole reason to open the panel: not what we bid, but what we nearly bid and
    by how little it lost.

    Raises KeyError if the deal or call is not in the cache.
    """
    entry = _active_deals[deal_id]  # KeyError if not found
    key = "a_setups" if table == "a" else "b_setups"
    setups_by_n = entry[key]
    if call_n not in setups_by_n:
        raise KeyError(f"call_n={call_n} not found in deal {deal_id} table {table}")
    # The live source stores (setup, call); the pool replay adds the seat.
    setup, call = setups_by_n[call_n][:2]

    out = build_explanation(setup, call)
    # `shows` is rewritten below to the rule's own one-line text, which is what
    # the panel prints and the editor edits; keep the engine's structured block
    # beside it rather than dropping it.
    out["shows_block"] = out.get("shows")
    out["rule_id"] = out.get("source_rule_id")

    hand = (entry.get("hand_deal") or {}).get(setup.seat)
    if hand is None:
        chosen, ranked = None, []
    else:
        chosen, ranked = _winning_candidate(setup, hand, call)
    out["candidates"] = [_candidate_row(sc, sc is chosen) for sc in ranked[:12]]

    rule = chosen.candidate.rule if (chosen and chosen.candidate.rule) else None
    out["fit_score"] = round(chosen.fit, 4) if chosen else 0.0
    out["seat"] = setup.seat.value

    if rule is not None:
        requires = rule.requires.to_dict()
        out.update({
            "rule_id": rule.id,
            "priority": rule.priority,
            "shows": rule.shows,
            "context_id": rule.context_id,
            # A context declared with `expand:` yields ids like `resp_1M[H]`.
            # A patch names the raw context, so editing one variant here edits
            # the template for every variant -- the UI warns on this badge.
            "is_template": "[" in rule.context_id,
            "constraint": {
                "hcp": list(requires.get("hcp", [0, 37])),
                "lengths": _norm_lengths(requires),
                "raw": requires,
            },
        })
    else:
        # No rule matched: the engine fell back.  Say so rather than showing an
        # empty editor that looks like a rule with no constraints.
        out.update({
            "rule_id": "fallback",
            "priority": None,
            "shows": out.get("shows", {}).get("text", "") if isinstance(
                out.get("shows"), dict) else out.get("shows", ""),
            "context_id": setup.context_rules[0][0].id if setup.context_rules else "",
            "is_template": False,
            "is_fallback": True,
            "constraint": {"hcp": [0, 37], "lengths": {}, "raw": {}},
        })
    return out


# ---------------------------------------------------------------------------
# DealGenerator
# ---------------------------------------------------------------------------


class DealGenerator:
    """Generate deals asynchronously until BEN wins; stream results over WS."""

    def __init__(self, seed: int | None = None):
        self.rng = random.Random(seed)
        self.stop_event = asyncio.Event()

    async def run(self, websocket) -> None:
        loop = asyncio.get_event_loop()
        system = await loop.run_in_executor(None, _get_system)
        ben = await loop.run_in_executor(None, _get_ben)

        tried = 0
        board_idx = 0

        while not self.stop_event.is_set():
            # Generate a random deal.
            deck = list(FULL_DECK)
            self.rng.shuffle(deck)
            deal: dict[Seat, Hand] = {
                s: Hand(deck[j * 13:(j + 1) * 13]) for j, s in enumerate(Seat)
            }
            dealer = Seat.from_index(board_idx % 4)
            vul = VULS[(board_idx // 4) % 4]

            # Play both tables in executor (blocking).
            result = await loop.run_in_executor(
                None,
                _play_both_tables,
                system, ben, deal, dealer, vul,
            )

            a_score = result["a_score"]
            b_score = result["b_score"]
            margin = imps(a_score - b_score)

            tried += 1
            board_idx += 1

            if margin < 0:
                # BEN wins — package the deal and report it.
                deal_id = str(uuid.uuid4())

                a_auction: Auction = result["a_auction"]
                b_auction: Auction = result["b_auction"]
                tricks_a: int | None = result["tricks_a"]
                tricks_b: int | None = result["tricks_b"]

                deal_dict = {
                    "id": deal_id,
                    "source": "live",
                    "tried": tried,
                    "board": board_idx - 1,
                    "dealer": dealer.value,
                    "vul": vul.value,
                    "hands": {s.value: str(deal[s]) for s in Seat},
                    "table_a": {
                        "our_side": "NS",
                        "auction": [str(c) for c in a_auction.calls],
                        "our_calls": result["a_calls"],
                        "contract": (
                            str(a_auction.contract) if a_auction.contract else "passed out"
                        ),
                        "tricks": tricks_a,
                        "score_ns": a_score,
                    },
                    "table_b": {
                        "our_side": "EW",
                        "auction": [str(c) for c in b_auction.calls],
                        "our_calls": result["b_calls"],
                        "contract": (
                            str(b_auction.contract) if b_auction.contract else "passed out"
                        ),
                        "tricks": tricks_b,
                        "score_ns": b_score,
                    },
                    "imp_margin": margin,
                }

                register_deal(deal_id, deal_dict, {
                    "a_setups": result["a_setups"],
                    "b_setups": result["b_setups"],
                    "hand_deal": deal,
                })

                await websocket.send_json({"type": "found", "deal": deal_dict})
                # Reset counter for next search after frontend may continue.
                tried = 0
            else:
                # Progress heartbeat.
                if tried % 5 == 0:
                    await websocket.send_json({"type": "progress", "tried": tried})

            # Brief yield so other coroutines can run.
            await asyncio.sleep(0)
