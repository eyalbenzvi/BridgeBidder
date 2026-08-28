"""Auction analysis: candidate generation, call interpretation, and the
per-player inference engine (positive + priority-ordered negative inference).

This module is the single source of truth used by choose_bid, explain_bid,
the sampler's replay and the arbitration rollouts, which is what makes the
self-consistency invariant hold.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Any

from ..constraints.model import HandConstraint
from ..domain.auction import Auction
from ..domain.calls import Call, PASS
from ..domain.cards import SUITS
from ..domain.types import Seat, Vulnerability
from ..evaluation.registry import EvalContext
from ..system.dsl import BiddingSystem, BidRule, Conditions, Context, Establishes
from ..system.matcher import match_all_contexts
from .descriptor import HandDescriptor, SideState
from .fallback import FallbackMeaning, generate_fallbacks

# ---------------------------------------------------------------------------
# data structures
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Candidate:
    call: Call
    rule: BidRule | None = None
    fallback: FallbackMeaning | None = None

    @property
    def constraint(self) -> HandConstraint:
        return self.rule.requires if self.rule else self.fallback.constraint  # type: ignore[union-attr]

    @property
    def priority(self) -> float:
        return self.rule.priority if self.rule else self.fallback.priority  # type: ignore[union-attr]

    @property
    def shows(self) -> str:
        return self.rule.shows if self.rule else self.fallback.shows  # type: ignore[union-attr]

    @property
    def is_fallback(self) -> bool:
        return self.rule is None

    @property
    def establishes(self) -> Establishes:
        if self.rule:
            return self.rule.establishes
        fb = self.fallback
        return Establishes(forcing=fb.forcing, game_force=fb.forcing == "game_forcing",
                           agreed_suit=fb.agreed_suit)  # type: ignore[union-attr]


@dataclass
class Interpretation:
    """The systemic meaning of one call at one auction position."""

    call: Call
    primary_rule: BidRule | None
    same_call_rules: list[BidRule]
    skipped_rules: list[BidRule]
    fallback: FallbackMeaning | None
    constraint: HandConstraint  # positive knowledge (anyOf of same-call rules)
    establishes: Establishes
    shows_text: str
    alertable: bool = False
    announce: str | None = None
    convention: str | None = None

    @property
    def is_fallback(self) -> bool:
        return self.primary_rule is None

    @property
    def source_rule_id(self) -> str:
        return self.primary_rule.id if self.primary_rule else "fallback"


@dataclass
class CallAnnotation:
    index: int
    seat: Seat
    call: Call
    interpretation: Interpretation
    explanation_given: dict | None = None


@dataclass
class Analysis:
    system: BiddingSystem
    auction: Auction
    descriptors: dict[Seat, HandDescriptor]
    sides: dict[str, SideState]
    annotations: list[CallAnnotation] = field(default_factory=list)

    def partner_model(self, seat: Seat) -> dict:
        return self.descriptors[seat.partner].summary()

    def opponent_models(self, seat: Seat) -> dict:
        return {
            seat.lho.value: self.descriptors[seat.lho].summary(),
            seat.rho.value: self.descriptors[seat.rho].summary(),
        }


@dataclass
class DecisionSetup:
    """Everything needed to decide/interpret a call at one position,
    independent of the actual hand held."""

    system: BiddingSystem
    auction: Auction
    seat: Seat
    analysis: Analysis                       # state BEFORE this call
    context_rules: list[tuple[Context, list[BidRule]]]  # matched, most specific first
    candidates: list[Candidate]
    eval_ctx: EvalContext
    pass_forbidden: bool = False
    pass_forbidden_hard: bool = False  # True when a game force is running

    def candidate_ctx(self, cand: Candidate) -> EvalContext:
        """Per-candidate eval context (support points need the trump suit
        the candidate is agreeing)."""
        agreed = cand.establishes.agreed_suit or self.eval_ctx.agreed_suit
        if agreed != self.eval_ctx.agreed_suit:
            return replace(self.eval_ctx, agreed_suit=agreed)
        return self.eval_ctx


# ---------------------------------------------------------------------------
# condition checks
# ---------------------------------------------------------------------------


def we_hold_contract(auction: Auction, seat: Seat) -> bool:
    """True when our own last contract bid stands: this seat made it, or
    partner made it and game is already reached.  Bidding on from here is
    bidding against ourselves."""
    lb_info = auction.last_bid_info
    if lb_info is None:
        return False
    bidder = auction.seat_of_call(lb_info[1])
    return bidder == seat or (bidder == seat.partner and _game_reached(auction))


def _conditions_hold(cond: Conditions, auction: Auction, seat: Seat, system: BiddingSystem,
                     ctx: EvalContext | None = None, call: Call | None = None) -> bool:
    if cond.is_trivial:
        return True
    if cond.cheapest_in_suit is not None and call is not None and call.is_bid:
        lb = auction.last_bid
        floor = lb.bid_index if lb else -1
        cheapest = None
        for level in range(1, 8):
            c = Call.bid(level, call.strain)
            if c.bid_index > floor:
                cheapest = level
                break
        if (call.level == cheapest) != cond.cheapest_in_suit:
            return False
    # suit-role gates: these depend only on the auction, so they are hard
    # conditions rather than soft hand features (a "raise partner's suit"
    # rule must not fire in a suit partner never bid)
    if cond.partner_suit is not None and ctx is not None:
        shown = set(ctx.partner_suits) | ({ctx.agreed_suit} if ctx.agreed_suit else set())
        if cond.partner_suit not in shown:
            return False
    if cond.unbid_suit is not None and ctx is not None:
        shown = set(ctx.partner_suits) | set(ctx.their_suits)
        if ctx.agreed_suit:
            shown.add(ctx.agreed_suit)
        # a suit I have bid myself is not "unbid" either: repeating it is a
        # rebid (a length statement), not the introduction of a new suit
        shown |= {c.strain for i, c in enumerate(auction.calls)
                  if c.is_bid and auction.seat_of_call(i) == seat}
        if cond.unbid_suit in shown:
            return False
    if cond.opening_seat is not None:
        if auction.opener_index() is not None:
            return False  # opening-seat conditions only apply before any bid
        if auction.opening_seat_number not in cond.opening_seat:
            return False
    if cond.passed_hand is not None and auction.is_passed_hand(seat) != cond.passed_hand:
        return False
    vul = auction.vulnerability
    if cond.we_vulnerable is not None and vul.is_vulnerable(seat) != cond.we_vulnerable:
        return False
    if cond.they_vulnerable is not None and vul.is_vulnerable(seat.lho) != cond.they_vulnerable:
        return False
    if cond.we_hold_contract is not None and we_hold_contract(auction, seat) != cond.we_hold_contract:
        return False
    if cond.their_last_bid_suit is not None:
        lb_info = auction.last_bid_info
        ok = (lb_info is not None
              and lb_info[0].strain != "NT"
              and not auction.seat_of_call(lb_info[1]).same_side(seat))
        if ok != cond.their_last_bid_suit:
            return False
    if cond.we_bid_last is not None:
        lb_info = auction.last_bid_info
        ok = lb_info is not None and auction.seat_of_call(lb_info[1]).same_side(seat)
        if ok != cond.we_bid_last:
            return False
    if cond.my_suit is not None:
        mine = {c.strain for i, c in enumerate(auction.calls)
                if c.is_bid and auction.seat_of_call(i) == seat}
        if cond.my_suit not in mine:
            return False
    if cond.their_bid_level is not None:
        lb = auction.last_bid
        if lb is None or lb.level not in cond.their_bid_level:
            return False
    if cond.i_have_acted is not None:
        acted = any(not c.is_pass for i, c in enumerate(auction.calls)
                    if auction.seat_of_call(i) == seat)
        if acted != cond.i_have_acted:
            return False
    if cond.side_has_acted is not None:
        acted = any(not c.is_pass for i, c in enumerate(auction.calls)
                    if auction.seat_of_call(i).side == seat.side)
        if acted != cond.side_has_acted:
            return False
    for flag, want in cond.config.items():
        if system.config.get(flag) != want:
            return False
    return True


def _context_when_holds(ctx: Context, side: SideState, auction: Auction, seat: Seat) -> bool:
    w = ctx.when
    if w.is_trivial:
        return True
    if w.we_hold_contract is not None and we_hold_contract(auction, seat) != w.we_hold_contract:
        return False
    if w.agreed_suit is not None:
        if w.agreed_suit is True and side.agreed_suit is None:
            return False
        if w.agreed_suit is False and side.agreed_suit is not None:
            return False
        if isinstance(w.agreed_suit, str) and side.agreed_suit != w.agreed_suit:
            return False
    if w.game_forced is not None and side.game_forced != w.game_forced:
        return False
    if w.asking is not None and side.asking != w.asking:
        return False
    return True


# ---------------------------------------------------------------------------
# setup construction
# ---------------------------------------------------------------------------


def _stripped_calls(auction: Auction) -> list[str]:
    calls = [str(c) for c in auction.calls]
    i = 0
    while i < len(calls) and calls[i] == "P":
        i += 1
    return calls[i:]


def _shown_suits_of(analysis: Analysis, seats: list[Seat]) -> list[str]:
    out: list[str] = []
    for s in seats:
        for suit in analysis.descriptors[s].shown_suits:
            if suit not in out:
                out.append(suit)
    return out


def build_eval_ctx(analysis: Analysis, auction: Auction, seat: Seat) -> EvalContext:
    side = analysis.sides[seat.side]
    partner_desc = analysis.descriptors[seat.partner]
    pbox = partner_desc.box
    return EvalContext(
        seat=seat,
        vulnerability=auction.vulnerability,
        agreed_suit=side.agreed_suit,
        partner_suits=list(partner_desc.shown_suits),
        their_suits=_shown_suits_of(analysis, [seat.lho, seat.rho]),
        opening_seat_number=auction.opening_seat_number if auction.opener_index() is None else None,
        is_passed_hand=auction.is_passed_hand(seat),
        partner_min_hcp=pbox.hcp[0],
        partner_max_hcp=pbox.hcp[1],
        partner_min_points=partner_desc.min_total_points,
        partner_min_length={s: int(pbox.suit(s)[0]) for s in SUITS},
    )


def _game_reached(auction: Auction) -> bool:
    lb = auction.last_bid
    if lb is None:
        return False
    if lb.strain == "NT":
        return lb.level >= 3
    if lb.strain in ("H", "S"):
        return lb.level >= 4
    return lb.level >= 5


def _pass_forbidden(auction: Auction, seat: Seat, analysis: Analysis) -> bool:
    """Never pass out a game force below game; never pass partner's forcing
    call when RHO passed."""
    side = analysis.sides[seat.side]
    n = len(auction.calls)
    rho_passed = n >= 1 and auction.calls[-1].is_pass
    # partner's last call and whether it is the auction's last non-pass call
    partner_ann = [a for a in analysis.annotations if a.seat == seat.partner and not a.call.is_pass]
    partner_forcing = bool(partner_ann) and partner_ann[-1].interpretation.establishes.forcing in (
        "one_round", "game_forcing")
    partner_last_is_live = bool(partner_ann) and all(
        a.call.is_pass for a in analysis.annotations[partner_ann[-1].index + 1:])
    if partner_forcing and partner_last_is_live and rho_passed:
        return True  # may be relaxed by the decision layer for one-round forces
    if side.game_forced and not _game_reached(auction):
        would_end = auction.child(PASS).is_complete if auction.is_legal(PASS) else False
        if would_end:
            return True
        # partner's below-game call with no interference: keep the force alive
        if rho_passed and partner_last_is_live:
            return True
    return False


def make_setup(system: BiddingSystem, auction: Auction, analysis: Analysis) -> DecisionSetup:
    """Build the decision setup for auction.next_seat given analysis of the
    calls so far."""
    seat = auction.next_seat
    side = analysis.sides[seat.side]
    eval_ctx = build_eval_ctx(analysis, auction, seat)
    stripped = _stripped_calls(auction)
    contexts = [
        c for c in match_all_contexts(system.contexts, stripped)
        if _context_when_holds(c, side, auction, seat)
    ]
    context_rules: list[tuple[Context, list[BidRule]]] = []
    for ctx in contexts:
        rules = [
            r for r in ctx.rules
            if auction.is_legal(r.call)
            and _conditions_hold(r.when, auction, seat, system, eval_ctx, r.call)
        ]
        if rules:
            context_rules.append((ctx, rules))

    candidates: list[Candidate] = []
    covered: set[str] = set()
    for ctx, rules in context_rules:
        ctx_calls = {str(r.call) for r in rules}
        for r in rules:
            if str(r.call) in covered:
                continue  # a more specific context already covers this call
            candidates.append(Candidate(call=r.call, rule=r))
        covered |= ctx_calls

    partner_suits = eval_ctx.partner_suits
    their_suits = eval_ctx.their_suits
    we_have_acted = any(
        not a.call.is_pass and a.seat.side == seat.side for a in analysis.annotations
    )
    # partner signed off with no intervention since: don't invent further action
    # (an explicit sign-off, or any non-forcing call once game is reached)
    partner_signed_off = False
    partner_forcing = False
    non_pass = [a for a in analysis.annotations if not a.call.is_pass]
    if non_pass and non_pass[-1].seat == seat.partner:
        forcing = non_pass[-1].interpretation.establishes.forcing
        partner_signed_off = forcing == "sign_off" or (
            forcing == "non_forcing" and _game_reached(auction)
        )
        partner_forcing = forcing in ("one_round", "game_forcing")
    # Never bid over your OWN last contract bid (that is what pulling your own
    # doubled contract looks like); partner's bid only silences us once game
    # is reached.  Keyed on the seat, so responder can still act after RHO
    # doubles partner's opening.
    pass_forbidden = _pass_forbidden(auction, seat, analysis)
    for fb in generate_fallbacks(
        auction, seat, partner_suits, their_suits,
        side.agreed_suit, side.game_forced, frozenset(covered), we_have_acted,
        partner_signed_off, we_hold_contract(auction, seat), partner_forcing,
        pass_forbidden,
    ):
        candidates.append(Candidate(call=fb.call, fallback=fb))

    return DecisionSetup(
        system=system,
        auction=auction,
        seat=seat,
        analysis=analysis,
        context_rules=context_rules,
        candidates=candidates,
        eval_ctx=eval_ctx,
        pass_forbidden=pass_forbidden,
        pass_forbidden_hard=side.game_forced,
    )


# ---------------------------------------------------------------------------
# interpretation
# ---------------------------------------------------------------------------


def interpret_call(setup: DecisionSetup, call: Call) -> Interpretation:
    """The systemic meaning of `call` at this position."""
    # find the first (most specific) matched context that defines this call
    for ctx, rules in setup.context_rules:
        same = sorted((r for r in rules if r.call == call), key=lambda r: -r.priority)
        if not same:
            continue
        primary = same[0]
        skipped = [
            r for r in rules
            if r.call != call and r.priority > primary.priority
        ]
        if len(same) == 1:
            constraint = primary.requires
        else:
            constraint = HandConstraint(any_of=tuple(r.requires for r in same))
        return Interpretation(
            call=call,
            primary_rule=primary,
            same_call_rules=same,
            skipped_rules=sorted(skipped, key=lambda r: -r.priority),
            fallback=None,
            constraint=constraint,
            establishes=primary.establishes,
            shows_text=primary.shows,
            alertable=primary.alertable,
            announce=primary.announce,
            convention=primary.convention,
        )
    # fallback
    fb = next((c.fallback for c in setup.candidates if c.is_fallback and c.call == call), None)
    if fb is None:
        fb = FallbackMeaning(call=call, constraint=HandConstraint(),
                             shows="undiscussed call", forcing="non_forcing", priority=1.0)
    return Interpretation(
        call=call,
        primary_rule=None,
        same_call_rules=[],
        skipped_rules=[],
        fallback=fb,
        constraint=fb.constraint,
        establishes=Establishes(forcing=fb.forcing, game_force=fb.forcing == "game_forcing",
                                agreed_suit=fb.agreed_suit),
        shows_text=fb.shows,
    )


# ---------------------------------------------------------------------------
# analysis (the inference engine proper)
# ---------------------------------------------------------------------------


def _empty_analysis(system: BiddingSystem, auction: Auction) -> Analysis:
    return Analysis(
        system=system,
        auction=auction,
        descriptors={s: HandDescriptor() for s in Seat},
        sides={"NS": SideState(), "EW": SideState()},
    )


def _apply_call(
    analysis: Analysis,
    setup: DecisionSetup,
    seat: Seat,
    call: Call,
    interp: Interpretation,
    explanation: dict | None,
    trusted_side: bool,
) -> None:
    """Update descriptors and side state for one call."""
    desc = analysis.descriptors[seat]
    side = analysis.sides[seat.side]

    # (c) an explanation attached to the call overrides the positive constraint
    override = None
    if explanation and explanation.get("constraints"):
        override = HandConstraint.from_dict(explanation["constraints"])
    positive = override if override is not None else interp.constraint
    note = explanation.get("text") if explanation else (interp.shows_text or None)
    if not call.is_pass or positive is not None:
        desc.apply(positive, weight="strong", note=f"{call}: {note}" if note else None)

    # (b) priority-ordered negative inference (only for a side playing OUR system)
    if trusted_side and override is None:
        for r in interp.skipped_rules:
            desc.apply(r.requires.negate(), weight=r.negative_inference_weight,
                       note=f"{call} denied: {r.shows}")
        if interp.primary_rule:
            for d in interp.primary_rule.denies:
                desc.apply(d.constraint.negate(), weight="strong", note=f"{call} denies: {d.text}")

    # side-state updates
    est = interp.establishes
    if not call.is_pass:
        if est.game_force:
            side.game_forced = True
        if est.agreed_suit:
            side.agreed_suit = est.agreed_suit
        side.last_forcing = est.forcing
        # ask lifecycle: answering a live ask clears it; establishing one sets it
        if side.asking and interp.primary_rule and any(
            ctx.when.asking == side.asking for ctx, _ in setup.context_rules
            if any(r is interp.primary_rule for r in ctx.rules)
        ):
            side.asking = None
            side.asking_by = None
        if est.asking:
            side.asking = est.asking
            side.asking_by = seat.value


def analyze(
    system: BiddingSystem,
    auction: Auction,
    explanations: dict[int, dict] | None = None,
    perspective: Seat | None = None,
) -> Analysis:
    """Walk the auction, interpreting every call and accumulating inference.

    perspective: the seat whose partnership is known to play this system.
    Negative inference is applied only to that side (None = trust all four
    seats, used in self-play/replay).
    """
    explanations = explanations or {}
    analysis = _empty_analysis(system, auction)
    prefix = Auction(dealer=auction.dealer, vulnerability=auction.vulnerability)
    for i, call in enumerate(auction.calls):
        seat = prefix.next_seat
        setup = make_setup(system, prefix, analysis)
        interp = interpret_call(setup, call)
        trusted = perspective is None or seat.side == perspective.side
        _apply_call(analysis, setup, seat, call, interp, explanations.get(i), trusted)
        analysis.annotations.append(
            CallAnnotation(index=i, seat=seat, call=call, interpretation=interp,
                           explanation_given=explanations.get(i))
        )
        prefix.add(call)
    analysis.auction = prefix
    return analysis


# cached full pipeline: analysis of all calls + setup for the next decision
_SETUP_CACHE: dict[tuple, DecisionSetup] = {}
_SETUP_CACHE_MAX = 20000


def _expl_key(explanations: dict[int, dict] | None) -> tuple:
    if not explanations:
        return ()
    return tuple(sorted((i, repr(sorted(e.items()))) for i, e in explanations.items()))


def prepare_decision(
    system: BiddingSystem,
    auction: Auction,
    explanations: dict[int, dict] | None = None,
    perspective: Seat | None = None,
) -> DecisionSetup:
    """Analysis + decision setup for the seat about to call. Cached."""
    key = (
        id(system), auction.dealer.value, auction.vulnerability.value,
        tuple(str(c) for c in auction.calls), _expl_key(explanations),
        perspective.value if perspective else None,
    )
    hit = _SETUP_CACHE.get(key)
    if hit is not None:
        return hit
    auction = auction.copy()  # callers may mutate their auction afterwards
    analysis = analyze(system, auction, explanations, perspective)
    setup = make_setup(system, auction, analysis)
    if len(_SETUP_CACHE) > _SETUP_CACHE_MAX:
        _SETUP_CACHE.clear()
    _SETUP_CACHE[key] = setup
    return setup
