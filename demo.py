#!/usr/bin/env python3
"""Demo: self-play 5 random deals and print the auctions with per-call
explanations.

    python demo.py [seed]
"""

import random
import sys

from bridgebidder.domain.auction import Auction
from bridgebidder.domain.cards import FULL_DECK, Hand
from bridgebidder.domain.types import Seat, Vulnerability
from bridgebidder.engine.selfplay import self_play
from bridgebidder.inference.engine import analyze
from bridgebidder.system.dsl import load_system

VULS = [Vulnerability.NONE, Vulnerability.NS, Vulnerability.EW, Vulnerability.BOTH]


def main() -> None:
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 42
    rng = random.Random(seed)
    system = load_system()
    print(f"System: {system.name}   (seed {seed})\n")

    for board in range(1, 6):
        deck = list(FULL_DECK)
        rng.shuffle(deck)
        deal = {s: Hand(deck[i * 13:(i + 1) * 13]) for i, s in enumerate(Seat)}
        dealer = Seat.from_index((board - 1) % 4)
        vul = VULS[(board - 1) % 4]

        print("=" * 72)
        print(f"Board {board}   Dealer {dealer.value}   Vul {vul.value}")
        for s in Seat:
            print(f"  {s.value}: {deal[s]}   ({deal[s].hcp} HCP)")

        auction = self_play(system, deal, dealer, vul)
        analysis = analyze(system, auction)

        print("\n  Auction:")
        for ann in analysis.annotations:
            interp = ann.interpretation
            flags = []
            if interp.alertable:
                flags.append("ALERT")
            if interp.announce:
                flags.append(f'announce "{interp.announce}"')
            if interp.is_fallback:
                flags.append("undiscussed")
            flag_s = f"  [{', '.join(flags)}]" if flags else ""
            print(f"    {ann.seat.value}: {str(ann.call):4} — {interp.shows_text}{flag_s}")

        contract = auction.contract
        print(f"\n  Final contract: {contract if contract else 'passed out'}\n")


if __name__ == "__main__":
    main()
