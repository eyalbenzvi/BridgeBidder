"""Deal source that needs no BEN: replay boards BEN already won.

Why this exists
---------------
`deal_gen` finds a losing board by *playing* deals until one comes back
negative.  That needs the BEN worker (an ONNX model behind a subprocess at
`/tmp/benenv/bin/python`) and the native double-dummy solver, neither of which
exists on a plain machine -- a phone-launched cloud box, a fresh clone, a free
PaaS dyno.  Without them the Deal Explorer cannot show anything at all.

But the 12,000-board pool under `data/pool/` is exactly a record of that
search already having been run: every board carries both auctions, both
contracts, both double-dummy scores and the IMP margin, and 3,842 of them are
boards where BEN beat us.  Serving one of those is not a degraded imitation of
generating one -- it is the same object, already scored by the real solver,
and it arrives in milliseconds instead of minutes.

What still works, and what does not
-----------------------------------
Clicking a bid works fully.  The explanation needs a `DecisionSetup`, which is
a pure function of (system, auction prefix, seat); replaying the *stored* call
sequence reproduces our engine's decision points exactly, with no opponent
model involved, because the opponent's calls are read from the record rather
than predicted.  `_setups_for_table` asserts the replay lands on the same call
we recorded, so a system edit that would have changed the auction is reported
instead of silently explaining the wrong decision.

What is not available here is a board *outside* the pool.  The pool is fixed,
so this source cannot surface a loss on a deal nobody has played.  When BEN is
installed, `deal_gen` remains the better source and the app prefers it.
"""

from __future__ import annotations

import asyncio
import gzip
import json
import random
import uuid
from pathlib import Path
from typing import TYPE_CHECKING

from bridgebidder.domain.auction import Auction
from bridgebidder.domain.calls import Call
from bridgebidder.domain.cards import Hand
from bridgebidder.domain.types import Seat, Vulnerability
from bridgebidder.inference.engine import prepare_decision
from bridgebidder.system.dsl import load_system

if TYPE_CHECKING:
    from bridgebidder.system.dsl import BiddingSystem

POOL_DIR = Path(__file__).parents[4] / "data" / "pool"

# Boards where BEN beat us, loaded once and kept in memory.  Each record is
# roughly 700 bytes of JSON; a few thousand of them is a couple of megabytes.
_losing: list[dict] | None = None


def pool_files() -> list[Path]:
    return sorted(POOL_DIR.glob("*.jsonl.gz")) + sorted(POOL_DIR.glob("*.jsonl"))


def _load_losing() -> list[dict]:
    """All pool boards with a negative IMP margin (i.e. BEN won)."""
    global _losing
    if _losing is not None:
        return _losing
    out: list[dict] = []
    for path in pool_files():
        opener = gzip.open if path.suffix == ".gz" else open
        with opener(path, "rt") as f:
            for line in f:
                rec = json.loads(line)
                if rec.get("imp_margin", 0) < 0:
                    rec["_file"] = path.name
                    out.append(rec)
    _losing = out
    return out


def available() -> bool:
    return bool(pool_files())


def count() -> int:
    return len(_load_losing()) if available() else 0


# ---------------------------------------------------------------------------
# replay
# ---------------------------------------------------------------------------


def _setups_for_table(
    system: "BiddingSystem",
    dealer: Seat,
    vul: Vulnerability,
    our_side: str,
    calls: list[str],
) -> dict[int, tuple[object, Call, Seat]]:
    """Walk the recorded auction, capturing our engine's context at our seats.

    The opponent's calls are *read from the record*, not predicted, so no
    opponent model is consulted and the replay reproduces the recorded auction
    exactly.  Keyed by position in the auction, which is the same `n` the pool
    stores in `a_our_calls` -- so a click in the UI lands on the right setup.
    """
    auction = Auction(dealer=dealer, vulnerability=vul)
    setups: dict[int, tuple[object, Call, Seat]] = {}
    for n, text in enumerate(calls):
        seat = auction.next_seat
        call = Call.parse(text)
        if seat.side == our_side:
            setups[n] = (prepare_decision(system, auction, perspective=seat), call, seat)
        auction.add(call)
    return setups


def _check_drift(
    deal: dict[Seat, Hand],
    setups: dict[int, tuple[object, Call, Seat]],
) -> list[str]:
    """Positions where the engine would now bid something other than recorded.

    The pool was built at some earlier commit.  If the YAML has moved since,
    the board on screen is still a real board, but it is no longer a record of
    what the engine does today -- and quietly explaining a decision the engine
    would not now make is the one way this source can mislead.  So it is
    checked and surfaced rather than assumed away.
    """
    from bridgebidder.engine.decision import decide_fast

    drift: list[str] = []
    for n, (setup, recorded, seat) in sorted(setups.items()):
        try:
            choice = decide_fast(setup, deal[seat])
        except Exception:
            continue
        now = choice if isinstance(choice, Call) else choice.call
        if now != recorded:
            drift.append(f"call {n} ({seat.value}): pool {recorded}, engine now {now}")
    return drift


def build_deal(rec: dict, system: "BiddingSystem") -> dict:
    """Turn one pool record into the payload shape the front end expects."""
    dealer = Seat(rec["dealer"])
    vul = Vulnerability.parse(rec["vul"])
    deal = {s: Hand.parse(rec["hands"][s.value]) for s in Seat}

    a_calls = rec["a_auction"].split()
    b_calls = rec["b_auction"].split()
    a_setups = _setups_for_table(system, dealer, vul, "NS", a_calls)
    b_setups = _setups_for_table(system, dealer, vul, "EW", b_calls)

    drift = _check_drift(deal, a_setups) + _check_drift(deal, b_setups)

    deal_id = str(uuid.uuid4())
    payload = {
        "id": deal_id,
        "source": "corpus",
        "source_file": rec.get("_file", ""),
        "tried": 0,
        "board": rec["board"],
        "dealer": dealer.value,
        "vul": vul.value,
        "hands": {s.value: str(deal[s]) for s in Seat},
        "table_a": {
            "our_side": "NS",
            "auction": a_calls,
            "our_calls": rec["a_our_calls"],
            "contract": rec.get("a_contract") or "passed out",
            "tricks": _tricks_from(rec.get("a_contract")),
            "score_ns": rec["a_score_ns"],
        },
        "table_b": {
            "our_side": "EW",
            "auction": b_calls,
            "our_calls": rec["b_our_calls"],
            "contract": rec.get("b_contract") or "passed out",
            "tricks": _tricks_from(rec.get("b_contract")),
            "score_ns": rec["b_score_ns"],
        },
        "imp_margin": rec["imp_margin"],
        "drift": drift,
    }
    return payload, {"a_setups": a_setups, "b_setups": b_setups, "hand_deal": deal}


def _tricks_from(contract: str | None) -> int | None:
    """Pool contracts read like '3C by N (7 tricks)'."""
    if not contract or "(" not in contract:
        return None
    try:
        return int(contract.split("(")[1].split()[0])
    except (IndexError, ValueError):
        return None


# ---------------------------------------------------------------------------
# streaming source
# ---------------------------------------------------------------------------


def rehydrate(deal_id: str, source_file: str, board: int) -> bool:
    """Rebuild a pool board's decision setups under an existing deal id.

    The explain cache is in memory and holds a bounded number of boards, so a
    board goes missing for two ordinary reasons: enough newer boards pushed it
    out, or the process restarted — which on a free host happens every time
    the instance idles out, i.e. constantly. Either way the browser is still
    showing the board and its bids are still clickable, and the click 404s.

    Nothing about a pool board is stateful, so it can simply be rebuilt: find
    the record again and replay it. Re-registering under the id the client
    already holds means the page it is looking at keeps working, rather than
    being told to start over.
    """
    from . import deal_gen

    for rec in _load_losing():
        if rec.get("_file") == source_file and rec.get("board") == board:
            payload, setups = build_deal(rec, load_system())
            payload["id"] = deal_id
            deal_gen.register_deal(deal_id, payload, setups)
            return True
    return False


class CorpusDealSource:
    """Serves losing boards from the pool over the same protocol as DealGenerator."""

    def __init__(self, seed: int | None = None):
        self.rng = random.Random(seed)
        self.stop_event = asyncio.Event()
        self._served: set[int] = set()

    async def run(self, websocket) -> None:
        from . import deal_gen

        loop = asyncio.get_event_loop()
        system = await loop.run_in_executor(None, load_system)
        boards = await loop.run_in_executor(None, _load_losing)

        if not boards:
            await websocket.send_json({
                "type": "error",
                "message": "No pool data under data/pool/ — nothing to replay.",
            })
            return

        await websocket.send_json({
            "type": "source", "source": "corpus", "pool_size": len(boards),
        })

        while not self.stop_event.is_set():
            if len(self._served) >= len(boards):
                self._served.clear()
            while True:
                idx = self.rng.randrange(len(boards))
                if idx not in self._served:
                    break
            self._served.add(idx)

            payload, setups = await loop.run_in_executor(
                None, build_deal, boards[idx], system
            )
            payload["tried"] = len(self._served)
            deal_gen.register_deal(payload["id"], payload, setups)
            await websocket.send_json({"type": "found", "deal": payload})

            # One board per request: wait for the client to ask for another.
            try:
                msg = await websocket.receive_text()
            except Exception:
                return
            if msg and "stop" in msg:
                return
