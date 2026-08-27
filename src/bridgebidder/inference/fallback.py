"""Generic fallback bidding semantics.

When the system YAML has no rule for a legal call in the current context, the
engine falls back to universal bridge logic so it NEVER lacks a candidate:
  - new suit by responder = forcing (uncontested, unpassed hand)
  - raises show support proportional to level
  - NT bids show balanced-ish hands with ranges by level
  - pass is illegal in a game force below game (filtered by the caller)
All fallback candidates are flagged is_undiscussed_fallback=True.
"""

from __future__ import annotations

from dataclasses import dataclass

from ..constraints.model import HandConstraint
from ..domain.auction import Auction
from ..domain.calls import Call, DOUBLE, PASS
from ..domain.cards import SUITS
from ..domain.types import Seat

# minimum total points to introduce a NEW suit at a given level (fallback logic)
_NEW_SUIT_MIN_PTS = {1: 6, 2: 10, 3: 12, 4: 14, 5: 16, 6: 18, 7: 20}
# support points to RAISE partner to a given level
_RAISE_MIN_PTS = {2: 6, 3: 10, 4: 12, 5: 15, 6: 18, 7: 21}
_NT_RANGES = {1: (6, 11), 2: (11, 14), 3: (14, 19), 4: (19, 22), 5: (22, 40), 6: (30, 40), 7: (34, 40)}


@dataclass(frozen=True)
class FallbackMeaning:
    call: Call
    constraint: HandConstraint
    shows: str
    forcing: str = "non_forcing"
    priority: float = 10.0
    agreed_suit: str | None = None


def _c(**kw) -> HandConstraint:
    return HandConstraint.from_dict(kw)


def generate_fallbacks(
    auction: Auction,
    seat: Seat,
    partner_suits: list[str],
    their_suits: list[str],
    agreed_suit: str | None,
    game_forced: bool,
    covered_calls: frozenset[str],
    we_have_acted: bool = False,
) -> list[FallbackMeaning]:
    """Generate generic candidates for calls NOT covered by system rules."""
    out: list[FallbackMeaning] = []
    lb = auction.last_bid
    floor = lb.bid_index if lb else -1

    def add(call: Call, constraint: HandConstraint, shows: str, forcing: str = "non_forcing",
            priority: float = 10.0, agreed: str | None = None) -> None:
        if str(call) in covered_calls or not auction.is_legal(call):
            return
        out.append(FallbackMeaning(call=call, constraint=constraint, shows=shows,
                                   forcing=forcing, priority=priority, agreed_suit=agreed))

    # ---- pass ----
    # Once our side has spoken, pass is the safe default in undiscussed spots
    # (any hand); before that it shows a weak-ish hand.
    if we_have_acted:
        add(PASS, HandConstraint(), "nothing more to say (undiscussed)", "sign_off", 8.0)
    else:
        add(PASS, _c(hcp=[0, 11]), "nothing suitable to say (undiscussed)", "sign_off", 8.0)

    # ---- raises of partner's suit(s) ----
    raise_suits = [s for s in ([agreed_suit] if agreed_suit else partner_suits) if s]
    for s in raise_suits:
        for level in range(1, 8):
            call = Call.bid(level, s)
            if call.bid_index <= floor:
                continue
            lo = _RAISE_MIN_PTS.get(level, 20)
            hi = lo + 4 if level < 4 else 40
            add(
                call,
                _c(suits={s: [3, 13]}, evals={"total_points": [lo, hi]}),
                f"raise: 3+ {s}, about {lo}-{hi if hi < 40 else '+'} support points",
                "non_forcing",
                12.0,
                agreed=s,
            )
            break  # cheapest raise only; higher raises come from real rules

    # ---- new suits / rebids of own suits (only through the 3-level: above
    # that, raises / NT / pass are the sane undiscussed actions) ----
    for s in SUITS:
        for level in range(1, 4):
            call = Call.bid(level, s)
            if call.bid_index <= floor:
                continue
            if str(call) in covered_calls or s in raise_suits:
                break
            if s in their_suits:
                break  # never invent cue-bids: those need explicit system rules
            lo = _NEW_SUIT_MIN_PTS.get(level, 20)
            forcing = "one_round" if (not game_forced and partner_suits and level <= 2) else (
                "game_forcing" if game_forced else "non_forcing")
            add(
                call,
                _c(suits={s: [4, 13]}, evals={"total_points": [lo, 40]}),
                f"natural, 4+ {s}, {lo}+ points (undiscussed)",
                forcing,
                11.0,
            )
            break  # cheapest level in this suit only

    # ---- notrump ----
    for level in range(1, 8):
        call = Call.bid(level, "NT")
        if call.bid_index <= floor:
            continue
        lo, hi = _NT_RANGES.get(level, (20, 40))
        feats = [f"stopper({s})" for s in their_suits[:2]]
        add(
            call,
            _c(hcp=[lo, hi], evals={"semi_balanced": [1, 1]}, features=feats),
            f"natural NT, {lo}-{hi} HCP, stoppers in their suit(s) (undiscussed)",
            "non_forcing",
            10.0,
        )
        break

    # ---- double ----
    if auction.is_legal(DOUBLE) and lb is not None:
        if lb.bid_index >= Call.parse("4S").bid_index or game_forced:
            add(DOUBLE, _c(hcp=[13, 40], evals={"stoppers(their)": [0.5, 99]}),
                "penalty-oriented double (undiscussed)", "non_forcing", 9.0)
        else:
            shorts = {s: [0, 2] for s in their_suits[:1]}
            add(DOUBLE, _c(hcp=[12, 40], suits=shorts),
                "takeout-flavored double (undiscussed)", "one_round", 9.0)

    # ---- ultimate backstop: cheapest legal bid, unconstrained ----
    if not any(m.call.is_bid for m in out):
        for b in auction.legal_calls():
            if b.is_bid:
                add(b, HandConstraint(), "forced continuation (undiscussed)", "non_forcing", 1.0)
                break

    return out
