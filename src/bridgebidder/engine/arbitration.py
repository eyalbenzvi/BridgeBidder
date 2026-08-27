"""Simulation arbitration: roll out candidate calls over consistent deals,
double-dummy-score the final contracts and compare in IMPs."""

from __future__ import annotations

import math
import time

from ..domain.auction import Auction
from ..domain.calls import Call
from ..domain.cards import Hand
from ..domain.types import Seat
from ..inference.engine import DecisionSetup, prepare_decision
from ..system.dsl import BiddingSystem
from .dd import get_dd
from .decision import ScoredCandidate, decide_fast
from .sampler import sample_consistent_deals
from .scoring import imps, signed_score

MAX_ROLLOUT_CALLS = 24
MIN_DEALS_FOR_VERDICT = 8
SIGNIFICANCE_T = 1.5   # mean must exceed T * stderr to overturn the fast pick
MIN_OVERTURN_IMP = 0.4  # ... and be worth at least this many IMPs


def rollout(
    system: BiddingSystem,
    auction: Auction,
    deal: dict[Seat, Hand],
    first_call: Call,
) -> Auction:
    """Append first_call, then let the engine finish the auction in
    fast-path-only mode for all four seats."""
    a = auction.child(first_call)
    steps = 0
    while not a.is_complete and steps < MAX_ROLLOUT_CALLS:
        seat = a.next_seat
        setup = prepare_decision(system, a, perspective=seat)
        a.add(decide_fast(setup, deal[seat]))
        steps += 1
    while not a.is_complete:  # budget exceeded: everyone passes
        from ..domain.calls import PASS
        a.add(PASS)
    return a


def arbitrate(
    system: BiddingSystem,
    setup: DecisionSetup,
    hand: Hand,
    contenders: list[ScoredCandidate],
    explanations: dict[int, dict] | None = None,
    time_budget: float = 8.0,
    n_deals: int = 60,
) -> dict:
    """Compare candidate calls by expected IMPs over consistent deals.

    Returns a result dict: winner (call str or None), imp_deltas per call
    (expected IMPs vs the fast-path baseline), per-call mean scores, n_deals.
    """
    t0 = time.monotonic()
    seat = setup.seat
    side = seat.side
    sample_budget = min(time_budget * 0.45, 4.0)
    sample = sample_consistent_deals(
        system, setup.auction, seat, hand,
        n=n_deals, time_budget=sample_budget, explanations=explanations,
    )
    result: dict = {
        "n_deals": sample.n,
        "sample_attempts": sample.attempts,
        "sample_degraded": sample.degraded,
        "candidates": [str(sc.call) for sc in contenders],
        "imp_deltas": {},
        "mean_scores": {},
        "winner": None,
    }
    if sample.n < MIN_DEALS_FOR_VERDICT:
        return result  # not enough evidence; caller keeps fast-path top

    dd = get_dd()
    baseline = contenders[0]
    scores: dict[str, list[int]] = {str(sc.call): [] for sc in contenders}
    deadline = t0 + time_budget
    used_deals = 0
    prefetch = getattr(dd, "prefetch", None)
    for deal in sample.deals:
        if time.monotonic() > deadline:
            break
        if prefetch and used_deals % 8 == 0:
            remaining = max(0.0, deadline - time.monotonic())
            batch = sample.deals[used_deals:used_deals + max(1, int(remaining / 0.15))][:8]
            prefetch(batch)
        for sc in contenders:
            final = rollout(system, setup.auction, deal, sc.call)
            contract = final.contract
            tricks = dd.tricks(deal, contract.declarer, contract.strain) if contract else 0
            scores[str(sc.call)].append(
                signed_score(contract, tricks, setup.auction.vulnerability, side)
            )
        used_deals += 1
    result["n_deals"] = used_deals
    if used_deals < MIN_DEALS_FOR_VERDICT:
        return result

    base_scores = scores[str(baseline.call)]
    stats: dict[str, tuple[float, float]] = {}
    for name, ss in scores.items():
        diffs = [imps(s - b) for s, b in zip(ss, base_scores)]
        mean = sum(diffs) / len(diffs)
        var = sum((d - mean) ** 2 for d in diffs) / max(1, len(diffs) - 1)
        stderr = math.sqrt(var / len(diffs)) if diffs else 0.0
        stats[name] = (mean, stderr)
        result["imp_deltas"][name] = round(mean, 2)
        result["mean_scores"][name] = round(sum(ss) / len(ss), 1)

    # pick the best mean; overturn the baseline only when statistically clear
    best_name = max(stats, key=lambda k: stats[k][0])
    mean, stderr = stats[best_name]
    if best_name != str(baseline.call) and (
        mean <= SIGNIFICANCE_T * stderr or mean < MIN_OVERTURN_IMP
    ):
        best_name = str(baseline.call)  # not significant: prefer the more descriptive fast pick
    # final tie-breakers among near-equal candidates: prefer the more
    # descriptive bid (higher rule priority, then the tighter descriptor -
    # the call partner will read most accurately)
    best_mean = stats[best_name][0]
    near = [
        sc for sc in contenders
        if best_mean - stats[str(sc.call)][0] <= 0.15
    ]
    if len(near) > 1:
        def descriptor_entropy(sc: ScoredCandidate) -> float:
            box = sc.candidate.constraint.box()
            hcp_width = box.hcp[1] - box.hcp[0]
            suit_width = sum(box.suit(s)[1] - box.suit(s)[0] for s in "SHDC")
            return hcp_width + suit_width
        best_name = str(max(
            near,
            key=lambda sc: (sc.candidate.priority, -descriptor_entropy(sc), sc.fit),
        ).call)
    result["winner"] = best_name
    result["stats"] = {k: {"mean_imp": round(m, 2), "stderr": round(se, 2)} for k, (m, se) in stats.items()}
    return result
