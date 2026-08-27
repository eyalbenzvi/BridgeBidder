"""The decision pipeline: soft scoring, fast path, and arbitration hand-off."""

from __future__ import annotations

import time
from dataclasses import dataclass, field

from ..domain.auction import Auction
from ..domain.calls import Call
from ..domain.cards import Hand
from ..domain.types import Seat
from ..inference.engine import Candidate, DecisionSetup, prepare_decision
from ..system.dsl import BiddingSystem

FAST_FIT_THRESHOLD = 0.9
CLEAR_MARGIN = 0.25
MAX_ARBITRATION_CANDIDATES = 4


@dataclass
class ScoredCandidate:
    candidate: Candidate
    fit: float
    score: float  # fit blended with priority
    expected_imp_delta: float | None = None

    @property
    def call(self) -> Call:
        return self.candidate.call


@dataclass
class Decision:
    setup: DecisionSetup
    chosen: ScoredCandidate
    ranked: list[ScoredCandidate]
    confidence: str  # "clear" | "judgment"
    arbitration: dict | None = None
    log: list[str] = field(default_factory=list)


def _sort_key(sc: ScoredCandidate) -> tuple:
    # deterministic: score desc, priority desc, then a stable call order
    c = sc.call
    call_rank = c.bid_index if c.is_bid else (100 + {"pass": 0, "double": 1, "redouble": 2}[c.kind])
    return (-sc.score, -sc.candidate.priority, call_rank)


def score_candidates(setup: DecisionSetup, hand: Hand) -> list[ScoredCandidate]:
    """Soft-score every candidate for this hand; sorted best-first."""
    out: list[ScoredCandidate] = []
    for cand in setup.candidates:
        if cand.call.is_pass and setup.pass_forbidden:
            continue
        if not setup.auction.is_legal(cand.call):
            continue
        ctx = setup.candidate_ctx(cand)
        fit = cand.constraint.fit(hand, ctx)
        pnorm = max(0.0, min(cand.priority, 100.0)) / 100.0
        score = fit * (0.7 + 0.3 * pnorm)
        out.append(ScoredCandidate(candidate=cand, fit=fit, score=score))
    out.sort(key=_sort_key)
    return out


def _dedupe_by_call(ranked: list[ScoredCandidate]) -> list[ScoredCandidate]:
    seen: set[str] = set()
    out = []
    for sc in ranked:
        k = str(sc.call)
        if k not in seen:
            seen.add(k)
            out.append(sc)
    return out


def fast_decision(setup: DecisionSetup, hand: Hand) -> tuple[ScoredCandidate, list[ScoredCandidate], bool]:
    """Deterministic fast path.

    Returns (choice, ranked_by_call, is_clear).  is_clear=False means a full
    engine would send the top candidates to simulation arbitration.
    """
    ranked = score_candidates(setup, hand)
    if not ranked:
        raise RuntimeError(f"No legal candidate at {setup.auction} (should be impossible)")
    by_call = _dedupe_by_call(ranked)

    satisfying = [sc for sc in by_call if sc.fit >= FAST_FIT_THRESHOLD]
    if satisfying:
        best = max(satisfying, key=lambda sc: (sc.candidate.priority, sc.fit,
                                               -_sort_key(sc)[2]))
        # clear unless another satisfying candidate has (nearly) the same priority
        rivals = [sc for sc in satisfying
                  if str(sc.call) != str(best.call)
                  and abs(sc.candidate.priority - best.candidate.priority) < 1e-9]
        return best, by_call, not rivals

    top = by_call[0]
    margin = top.score - (by_call[1].score if len(by_call) > 1 else 0.0)
    return top, by_call, margin >= CLEAR_MARGIN


def decide_fast(setup: DecisionSetup, hand: Hand) -> Call:
    """Fast-path-only policy used for replay and rollouts (deterministic)."""
    choice, _, _ = fast_decision(setup, hand)
    return choice.call


def choose(
    system: BiddingSystem,
    auction: Auction,
    seat: Seat,
    hand: Hand,
    explanations: dict[int, dict] | None = None,
    use_arbitration: bool = True,
    arbitration_budget: float = 8.0,
) -> Decision:
    """Full decision pipeline for the seat on lead to call."""
    if auction.next_seat != seat:
        raise ValueError(f"It is {auction.next_seat.value}'s turn, not {seat.value}")
    setup = prepare_decision(system, auction, explanations, perspective=seat)
    choice, ranked, clear = fast_decision(setup, hand)
    decision = Decision(setup=setup, chosen=choice, ranked=ranked,
                        confidence="clear" if clear else "judgment")
    decision.log.append(
        f"fast path: top={choice.call} fit={choice.fit:.2f} score={choice.score:.2f} clear={clear}"
    )
    if clear or not use_arbitration:
        decision.confidence = "clear" if clear else "judgment"
        return decision

    from .arbitration import arbitrate  # local import to avoid cycles

    # only plausible candidates go to simulation: a bad systemic lie can score
    # well double-dummy (partner bids as if the rule were true), so a hard fit
    # floor keeps deceptive candidates out
    fit_floor = max(0.25, ranked[0].fit - 0.35)
    contenders = [sc for sc in ranked if sc.fit >= fit_floor][:MAX_ARBITRATION_CANDIDATES]
    if len(contenders) < 2:
        decision.log.append("no plausible alternative; keeping fast-path top")
        return decision
    t0 = time.monotonic()
    result = arbitrate(system, setup, hand, contenders, explanations,
                       time_budget=arbitration_budget)
    decision.log.append(f"arbitration took {time.monotonic() - t0:.2f}s over "
                        f"{result.get('n_deals', 0)} deals")
    if result.get("winner") is not None:
        winner_call = result["winner"]
        for sc in contenders:
            sc.expected_imp_delta = result["imp_deltas"].get(str(sc.call))
        decision.chosen = next(sc for sc in contenders if str(sc.call) == winner_call)
        decision.arbitration = result
        decision.confidence = "judgment"
        decision.log.append(f"arbitration winner: {winner_call}")
    else:
        decision.log.append("arbitration inconclusive; keeping fast-path top")
        decision.arbitration = result
    return decision
