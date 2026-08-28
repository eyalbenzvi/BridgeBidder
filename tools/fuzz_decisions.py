"""Random-auction fuzzer: the runtime half of the lint suite.

Static lints cannot see what the engine actually does at a position, and
two of this project's worst defects were runtime-only:

  * a seat with ZERO candidates (the doubled-Stayman abort, which killed a
    twelve-minute match mid-flight)
  * a seat whose only offer is an invented fallback while an authored
    context matched the auction - the "range with no rule" species, which
    every expert review has found by hand

Deals random hands, walks self-play auctions, and reports both.  Cheap
enough to run before every match round.

Usage:
    python3 tools/fuzz_decisions.py --n 400 --seed 1
    python3 tools/fuzz_decisions.py --n 2000 --strict   # exit 1 on a crash
"""

from __future__ import annotations

import argparse
import random
import sys
import traceback
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from bridgebidder.domain.auction import Auction  # noqa: E402
from bridgebidder.domain.cards import FULL_DECK, Hand  # noqa: E402
from bridgebidder.domain.types import Seat, Vulnerability  # noqa: E402
from bridgebidder.engine.decision import decide_fast  # noqa: E402
from bridgebidder.inference.engine import prepare_decision  # noqa: E402
from bridgebidder.system.dsl import load_system  # noqa: E402

VULS = [Vulnerability.NONE, Vulnerability.NS, Vulnerability.EW, Vulnerability.BOTH]
MAX_CALLS = 60


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=400, help="deals")
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--strict", action="store_true", help="exit 1 on any crash")
    ap.add_argument("--show", type=int, default=8, help="examples per category")
    args = ap.parse_args()

    system = load_system()
    rng = random.Random(args.seed)
    crashes: list[str] = []
    starved: Counter = Counter()
    starved_ex: dict[str, str] = {}
    decisions = 0

    for bi in range(args.n):
        deck = list(FULL_DECK)
        rng.shuffle(deck)
        deal = {s: Hand(deck[j * 13:(j + 1) * 13]) for j, s in enumerate(Seat)}
        dealer, vul = Seat.from_index(bi % 4), VULS[(bi // 4) % 4]
        auction = Auction(dealer=dealer, vulnerability=vul)
        while not auction.is_complete and len(auction.calls) < MAX_CALLS:
            seat = auction.next_seat
            try:
                setup = prepare_decision(system, auction, perspective=seat)
                decisions += 1
                if not setup.candidates:
                    crashes.append(f"ZERO CANDIDATES at [{dealer.value}] "
                                   f"{' - '.join(str(c) for c in auction.calls)} (seat {seat.value})")
                    break
                choice = decide_fast(setup, deal[seat])
                call = choice if hasattr(choice, "strain") else choice.call
                # an authored context matched, yet the engine's pick is an
                # invented fallback: the context has a hole this hand fell in
                chosen = next((c for c in setup.candidates if c.call == call), None)
                if chosen is not None and chosen.is_fallback and setup.context_rules:
                    ctx = setup.context_rules[0][0]
                    if not ctx.pattern.strip().startswith("..."):
                        starved[ctx.id] += 1
                        starved_ex.setdefault(
                            ctx.id,
                            f"[{dealer.value}] {' - '.join(str(c) for c in auction.calls)} "
                            f"| {seat.value} {deal[seat]} -> {call} (fallback)")
            except Exception:
                crashes.append(f"EXCEPTION at [{dealer.value}] "
                               f"{' - '.join(str(c) for c in auction.calls)} (seat {seat.value})\n"
                               + traceback.format_exc(limit=3))
                break
            auction.add(call)

    print(f"fuzzed {args.n} deals, {decisions} decisions")
    print(f"\n=== crashes / empty seats: {len(crashes)} ===")
    for c in crashes[:args.show]:
        print(" ", c)
    print(f"\n=== starved anchored contexts: {len(starved)} "
          f"({sum(starved.values())} decisions) ===")
    for cid, n in starved.most_common(args.show):
        print(f"  {n:4d}  {cid}")
        print(f"        e.g. {starved_ex[cid]}")
    return 1 if (args.strict and crashes) else 0


if __name__ == "__main__":
    raise SystemExit(main())
