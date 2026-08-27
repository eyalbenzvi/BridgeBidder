"""Sampling tests: consistent-deal generation enforces negative inference."""

import random
from collections import Counter

from bridgebidder.domain.auction import Auction
from bridgebidder.domain.cards import Hand
from bridgebidder.domain.types import Seat
from bridgebidder.engine.sampler import sample_consistent_deals
from bridgebidder.system.dsl import load_system

SYSTEM = load_system()


def test_support_double_negative_inference_in_samples():
    """After 1D - P - 1S - (2C) - 2D, opener denied exactly 3 spades (no
    support double).  Consistent deals must respect that."""
    auction = Auction.from_strings("N", ["1D", "P", "1S", "2C", "2D", "P"])
    my_hand = Hand.parse("KQT52.A4.932.865")  # responder (South)
    res = sample_consistent_deals(
        SYSTEM, auction, Seat.S, my_hand, n=120, time_budget=8.0,
        rng=random.Random(99),
    )
    assert res.n >= 30, f"too few consistent deals: {res.n} of {res.attempts} attempts"
    assert not res.degraded
    spade_counts = Counter(d[Seat.N].suit_length("S") for d in res.deals)
    assert spade_counts.get(3, 0) == 0, (
        f"support-double negative inference violated: {dict(spade_counts)}"
    )
    # positive knowledge holds too: opener rebid 2D shows 6+ diamonds
    assert all(d[Seat.N].suit_length("D") >= 6 for d in res.deals)
    # and every deal replays partner's exact calls by construction


def test_support_double_positive_case_samples():
    """After 1D - P - 1S - (2C) - X, opener holds exactly 3 spades."""
    auction = Auction.from_strings("N", ["1D", "P", "1S", "2C", "X", "P"])
    my_hand = Hand.parse("KQT52.A4.932.865")
    res = sample_consistent_deals(
        SYSTEM, auction, Seat.S, my_hand, n=60, time_budget=8.0,
        rng=random.Random(7),
    )
    assert res.n >= 20
    assert all(d[Seat.N].suit_length("S") == 3 for d in res.deals)


def test_opponent_explanation_constrains_samples():
    """An explanation attached to an opponent call restricts that opponent's
    hand in the sample."""
    auction = Auction.from_strings("N", ["1H", "2D", "P", "P", "P"][:2])
    # East overcalled 2D explained as weak with 6+ diamonds
    my_hand = Hand.parse("AQ752.KJ64.4.A32")  # I'm South, next to act... actually
    # auction: N=1H, E=2D; S to act.  Sample E's hand under the explanation.
    explanations = {1: {"text": "weak, 6+ diamonds", "constraints": {"suits": {"D": [6, 13]}, "hcp": [4, 10]}}}
    res = sample_consistent_deals(
        SYSTEM, auction, Seat.S, my_hand, n=60, time_budget=8.0,
        rng=random.Random(11), explanations=explanations,
    )
    assert res.n >= 20
    assert all(d[Seat.E].suit_length("D") >= 6 for d in res.deals)
    assert all(4 <= d[Seat.E].hcp <= 10 for d in res.deals)


def test_sampler_time_budget_graceful():
    """An extremely constrained position returns fewer samples, never hangs."""
    auction = Auction.from_strings("N", ["2C", "P", "2D", "P", "2NT", "P"])
    my_hand = Hand.parse("952.J64.T842.Q32")
    res = sample_consistent_deals(
        SYSTEM, auction, Seat.S, my_hand, n=500, time_budget=1.0,
        rng=random.Random(5),
    )
    assert res.elapsed < 3.0
    # opener showed 22-24 balanced: every surviving deal must comply
    for d in res.deals:
        assert d[Seat.N].hcp >= 22
