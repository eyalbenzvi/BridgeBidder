"""Property tests: 500+ random deals of full self-play must always terminate,
never crash, and never produce an illegal call."""

import random

from bridgebidder.domain.auction import Auction
from bridgebidder.domain.calls import Call
from bridgebidder.domain.cards import FULL_DECK, Hand
from bridgebidder.domain.types import Seat, Vulnerability
from bridgebidder.engine.selfplay import self_play
from bridgebidder.system.dsl import load_system

SYSTEM = load_system()
VULS = [Vulnerability.NONE, Vulnerability.NS, Vulnerability.EW, Vulnerability.BOTH]


def test_500_random_selfplay_auctions():
    rng = random.Random(31415)
    for i in range(500):
        deck = list(FULL_DECK)
        rng.shuffle(deck)
        deal = {s: Hand(deck[j * 13:(j + 1) * 13]) for j, s in enumerate(Seat)}
        dealer = Seat.from_index(i % 4)
        vul = VULS[(i // 4) % 4]
        auction = self_play(SYSTEM, deal, dealer, vul)

        assert auction.is_complete, f"deal {i}: auction did not terminate: {auction}"
        assert len(auction.calls) <= 40, f"deal {i}: runaway auction"
        # re-validate legality call by call
        check = Auction(dealer=dealer, vulnerability=vul)
        for c in auction.calls:
            assert check.is_legal(c), f"deal {i}: illegal call {c} in {auction}"
            check.add(c)
        # a completed non-passout auction must yield a contract with declarer
        if any(c.is_bid for c in auction.calls):
            assert auction.contract is not None, f"deal {i}: no contract for {auction}"
