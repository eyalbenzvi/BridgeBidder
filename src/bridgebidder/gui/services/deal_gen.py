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

from compare_ben import Ben  # noqa: E402
from bridgebidder.domain.cards import FULL_DECK, Hand
from bridgebidder.domain.calls import Call
from bridgebidder.domain.types import Seat, Vulnerability
from bridgebidder.domain.auction import Auction
from bridgebidder.engine.dd import EndplayDD, get_dd
from bridgebidder.engine.decision import decide_fast
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
            choice = decide_fast(setup, deal[seat])
            call = choice if isinstance(choice, Call) else choice.call
            rule_id = None
            for c in setup.candidates:
                if c.call == call:
                    rule_id = c.rule.id if c.rule else "fallback"
                    break
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


def get_explanation(deal_id: str, table: str, call_n: int) -> dict:
    """Return build_explanation output for the specified call.

    Raises KeyError if the deal or call is not in the cache.
    """
    entry = _active_deals[deal_id]  # KeyError if not found
    key = "a_setups" if table == "a" else "b_setups"
    setups_by_n = entry[key]
    if call_n not in setups_by_n:
        raise KeyError(f"call_n={call_n} not found in deal {deal_id} table {table}")
    setup, call = setups_by_n[call_n]
    return build_explanation(setup, call)


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

                # Store in cache (LRU-style via deque).
                if len(_active_deal_order) == _active_deal_order.maxlen:
                    oldest = _active_deal_order[0]
                    _active_deals.pop(oldest, None)
                _active_deals[deal_id] = {
                    "deal": deal_dict,
                    "a_setups": result["a_setups"],
                    "b_setups": result["b_setups"],
                    "hand_deal": deal,
                }
                _active_deal_order.append(deal_id)

                await websocket.send_json({"type": "found", "deal": deal_dict})
                # Reset counter for next search after frontend may continue.
                tried = 0
            else:
                # Progress heartbeat.
                if tried % 5 == 0:
                    await websocket.send_json({"type": "progress", "tried": tried})

            # Brief yield so other coroutines can run.
            await asyncio.sleep(0)
