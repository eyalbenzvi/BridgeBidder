"""End-to-end tests for the simulation arbitration path.

Self-play runs fast-path-only, so these are the only tests that exercise
sampling -> rollout -> double-dummy scoring -> IMP comparison as a whole.
"""

import time

import pytest

from bridgebidder.api import choose_bid
from bridgebidder.domain.auction import Auction
from bridgebidder.domain.calls import Call
from bridgebidder.domain.cards import Hand
from bridgebidder.domain.types import Seat
from bridgebidder.engine.decision import choose, fast_decision
from bridgebidder.inference.engine import prepare_decision
from bridgebidder.system.dsl import load_system

SYSTEM = load_system()

# positions harvested from self-play where the fast path is genuinely unsure
UNCLEAR = [
    ("AJ752.K4.Q92.J87", "N", []),
    ("K9542.A72.K4.J83", "N", ["P", "1D", "1S", "X", "2S", "X"]),
]


@pytest.mark.parametrize("hand,dealer,calls", UNCLEAR, ids=["borderline_opening", "competitive"])
def test_arbitration_returns_a_sound_call(hand, dealer, calls):
    auction = Auction.from_strings(dealer, calls)
    seat = auction.next_seat
    t0 = time.monotonic()
    decision = choose(SYSTEM, auction, seat, Hand.parse(hand),
                      use_arbitration=True, arbitration_budget=6.0)
    elapsed = time.monotonic() - t0

    assert elapsed < 10.0, f"arbitration took {elapsed:.1f}s"
    assert auction.is_legal(decision.chosen.call)
    assert decision.confidence == "judgment"
    # it must consider at least two candidates and report what it found
    assert decision.arbitration is not None
    assert len(decision.arbitration["candidates"]) >= 2


def test_arbitration_only_considers_plausible_candidates():
    """A candidate the hand cannot hold must never reach the simulation:
    double-dummy rollouts reward systemic lies, because partner then bids as
    though the lie were true."""
    auction = Auction.from_strings("N", [])
    decision = choose(SYSTEM, auction, Seat.N, Hand.parse("AJ752.K4.Q92.J87"),
                      use_arbitration=True, arbitration_budget=6.0)
    if decision.arbitration:
        for call in decision.arbitration["candidates"]:
            sc = next(s for s in decision.ranked if str(s.call) == call)
            assert sc.fit >= 0.25, f"implausible candidate {call} reached arbitration"


def test_arbitration_agrees_with_fast_path_on_clear_decisions():
    """When one call plainly fits, arbitration must not be invoked at all."""
    auction = Auction.from_strings("N", [])
    decision = choose(SYSTEM, auction, Seat.N, Hand.parse("AQ52.KJ4.QT9.KJ7"),
                      use_arbitration=True, arbitration_budget=6.0)
    assert str(decision.chosen.call) == "1NT"
    assert decision.confidence == "clear"
    assert decision.arbitration is None


def test_api_reports_arbitration_details():
    result = choose_bid({
        "hand": "AJ752.K4.Q92.J87",
        "auction_state": {"dealer": "N", "seat": "N", "calls": []},
        "arbitration_budget": 6.0,
    })
    assert result["confidence"] in ("clear", "judgment")
    if result["confidence"] == "judgment" and result["arbitration"]:
        arb = result["arbitration"]
        assert arb["n_deals"] >= 0
        assert set(arb["imp_deltas"]) <= set(arb["candidates"])
