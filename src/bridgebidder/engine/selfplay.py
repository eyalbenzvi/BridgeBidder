"""Engine self-play: bid a whole deal with the engine in all four seats."""

from __future__ import annotations

from ..domain.auction import Auction
from ..domain.cards import Hand
from ..domain.types import Seat, Vulnerability
from ..system.dsl import BiddingSystem
from ..inference.engine import prepare_decision
from .decision import decide_fast

MAX_CALLS = 40  # backstop; real auctions end long before this


def self_play(
    system: BiddingSystem,
    deal: dict[Seat, Hand],
    dealer: Seat,
    vulnerability: Vulnerability = Vulnerability.NONE,
    start: Auction | None = None,
) -> Auction:
    """Play out an auction with the deterministic fast-path policy in every
    seat.  Replaying the same deal reproduces the same auction exactly
    (the self-consistency invariant the sampler relies on)."""
    auction = start.copy() if start is not None else Auction(dealer=dealer, vulnerability=vulnerability)
    while not auction.is_complete:
        seat = auction.next_seat
        setup = prepare_decision(system, auction, perspective=seat)
        call = decide_fast(setup, deal[seat])
        auction.add(call)
        if len(auction.calls) > MAX_CALLS:  # pragma: no cover - safety net
            raise RuntimeError(f"Runaway auction: {auction}")
    return auction
