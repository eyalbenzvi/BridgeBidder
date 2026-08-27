"""Auction-consistent deal sampling.

Fix my hand, deal the other 39 cards with bias toward the coarse descriptor
summaries, then REPLAY the auction: partner's calls must be exactly
reproduced by the engine's deterministic policy (this enforces ALL negative
inference automatically); opponents' hands must satisfy their
explanation-derived constraints plus loose natural defaults.
"""

from __future__ import annotations

import random
import time
from dataclasses import dataclass

from ..domain.auction import Auction
from ..domain.cards import FULL_DECK, Card, Hand, SUITS
from ..domain.types import Seat
from ..evaluation.registry import EvalContext
from ..inference.engine import Analysis, DecisionSetup, analyze, build_eval_ctx, prepare_decision
from ..system.dsl import BiddingSystem
from .decision import decide_fast


@dataclass
class SampleResult:
    deals: list[dict[Seat, Hand]]
    attempts: int
    replay_rejects: int
    constraint_rejects: int
    elapsed: float
    degraded: bool = False  # True if we had to relax the replay filter

    @property
    def n(self) -> int:
        return len(self.deals)


def _partner_replay_setups(
    system: BiddingSystem,
    auction: Auction,
    partner: Seat,
    explanations: dict[int, dict] | None,
) -> list[tuple[int, DecisionSetup]]:
    """Decision setups at each of partner's turns (auction prefixes)."""
    out = []
    prefix = Auction(dealer=auction.dealer, vulnerability=auction.vulnerability)
    for i, call in enumerate(auction.calls):
        if prefix.next_seat == partner:
            expl = {k: v for k, v in (explanations or {}).items() if k < i}
            out.append((i, prepare_decision(system, prefix, expl, perspective=partner)))
        prefix.add(call)
    return out


def _biased_partner_cards(
    remaining: list[Card],
    partner_box,
    rng: random.Random,
) -> tuple[list[Card], list[Card]] | None:
    """Draw 13 cards for partner honoring the box's suit-length ranges when
    they are binding; returns (partner_cards, rest) or None to fall back."""
    by_suit = {s: [c for c in remaining if c.suit == s] for s in SUITS}
    los = {s: int(partner_box.suit(s)[0]) for s in SUITS}
    his = {s: min(int(partner_box.suit(s)[1]), len(by_suit[s])) for s in SUITS}
    if all(lo == 0 and hi >= 13 for (lo, hi) in ((los[s], his[s]) for s in SUITS)):
        return None  # nothing binding: plain shuffle is fine
    if sum(los.values()) > 13 or sum(his.values()) < 13:
        return None
    # sample suit lengths within bounds summing to 13
    for _ in range(30):
        lens = {s: rng.randint(los[s], his[s]) for s in SUITS}
        total = sum(lens.values())
        guard = 0
        while total != 13 and guard < 40:
            guard += 1
            s = rng.choice(SUITS)
            if total > 13 and lens[s] > los[s]:
                lens[s] -= 1
                total -= 1
            elif total < 13 and lens[s] < his[s]:
                lens[s] += 1
                total += 1
        if total == 13:
            partner_cards: list[Card] = []
            rest: list[Card] = []
            ok = True
            for s in SUITS:
                pool = list(by_suit[s])
                if lens[s] > len(pool):
                    ok = False
                    break
                rng.shuffle(pool)
                partner_cards.extend(pool[: lens[s]])
                rest.extend(pool[lens[s]:])
            if ok:
                return partner_cards, rest
    return None


def sample_consistent_deals(
    system: BiddingSystem,
    auction: Auction,
    my_seat: Seat,
    my_hand: Hand,
    n: int = 200,
    time_budget: float = 5.0,
    rng: random.Random | None = None,
    explanations: dict[int, dict] | None = None,
) -> SampleResult:
    rng = rng or random.Random(2718)
    t0 = time.monotonic()
    partner = my_seat.partner
    opponents = (my_seat.lho, my_seat.rho)

    analysis: Analysis = analyze(system, auction, explanations, perspective=my_seat)
    boxes = {s: analysis.descriptors[s].box for s in Seat if s != my_seat}
    opp_ctx = {s: build_eval_ctx(analysis, auction, s) for s in opponents}
    replay_setups = _partner_replay_setups(system, auction, partner, explanations)
    actual = [str(c) for c in auction.calls]

    remaining_master = [c for c in FULL_DECK if c not in set(my_hand.cards)]
    order = [partner, *opponents]

    deals: list[dict[Seat, Hand]] = []
    near_misses: list[dict[Seat, Hand]] = []  # pass constraints but fail replay
    attempts = replay_rejects = constraint_rejects = 0

    while len(deals) < n and time.monotonic() - t0 < time_budget:
        attempts += 1
        remaining = list(remaining_master)
        biased = _biased_partner_cards(remaining, boxes[partner], rng)
        if biased is not None:
            pcards, rest = biased
            rng.shuffle(rest)
            hands = [pcards, rest[0:13], rest[13:26]]
        else:
            rng.shuffle(remaining)
            hands = [remaining[0:13], remaining[13:26], remaining[26:39]]
        deal = {my_seat: my_hand}
        for s, cs in zip(order, hands):
            deal[s] = Hand(cs)
        # cheap box pre-filter
        if not all(boxes[s].accepts(deal[s]) for s in order):
            constraint_rejects += 1
            continue
        # opponents: hard descriptor constraints (explanations + natural reads)
        if not all(
            analysis.descriptors[s].satisfied(deal[s], opp_ctx[s]) for s in opponents
        ):
            constraint_rejects += 1
            continue
        # partner: exact replay of every call
        ok = True
        for i, setup in replay_setups:
            if str(decide_fast(setup, deal[partner])) != actual[i]:
                ok = False
                break
        if ok:
            deals.append(deal)
        else:
            replay_rejects += 1
            if len(near_misses) < n:
                near_misses.append(deal)

    degraded = False
    if not deals and near_misses:
        # graceful degradation: better a coarse model than none
        deals = near_misses
        degraded = True
    return SampleResult(
        deals=deals,
        attempts=attempts,
        replay_rejects=replay_rejects,
        constraint_rejects=constraint_rejects,
        elapsed=time.monotonic() - t0,
        degraded=degraded,
    )
