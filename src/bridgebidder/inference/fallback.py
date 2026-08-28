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
    partner_signed_off: bool = False,
    we_hold_contract: bool = False,
    partner_forcing: bool = False,
    pass_forbidden: bool = False,
    our_artificial_doubled: bool = False,
) -> list[FallbackMeaning]:
    """Generate generic candidates for calls NOT covered by system rules."""
    out: list[FallbackMeaning] = []
    lb = auction.last_bid
    floor = lb.bid_index if lb else -1
    # When our own side holds the current contract in a COMPETITIVE auction
    # (or with game already reached) and nothing forces us, there is nothing
    # to compete over: never invent a higher bid (this stops the engine from
    # pulling its own doubled contracts).  Uncontested constructive auctions
    # keep their fallback continuations (invites must stay biddable).
    if lb is not None:
        game_reached = (lb.strain == "NT" and lb.level >= 3) or \
                       (lb.strain in ("H", "S") and lb.level >= 4) or \
                       (lb.strain in ("C", "D") and lb.level >= 5)
    else:
        game_reached = False
    quiet = partner_signed_off or (
        we_hold_contract and not partner_forcing and not game_forced
        and (auction.is_competitive or game_reached)
    )

    def add(call: Call, constraint: HandConstraint, shows: str, forcing: str = "non_forcing",
            priority: float = 10.0, agreed: str | None = None) -> None:
        if str(call) in covered_calls or not auction.is_legal(call):
            return
        out.append(FallbackMeaning(call=call, constraint=constraint, shows=shows,
                                   forcing=forcing, priority=priority, agreed_suit=agreed))

    # ---- pass ----
    # Once our side has spoken, pass is the safe default in undiscussed spots
    # (any hand); before that it shows a weak-ish hand.
    # INVARIANT (bought with -800 twice): the fallback layer never passes
    # when the standing doubled bid is our own side's artificial call - an
    # alertable cue or transfer has no trump suit, and letting the generic
    # pass sit it plays 2-of-a-nothing doubled.  Authored sit/retreat rules
    # still apply; only the undiscussed pass is withheld.
    if not our_artificial_doubled:
        if we_have_acted:
            add(PASS, HandConstraint(), "nothing more to say (undiscussed)", "sign_off", 8.0)
        else:
            add(PASS, _c(hcp=[0, 11]), "nothing suitable to say (undiscussed)", "sign_off", 8.0)

    # ---- raises of partner's suit(s): cheapest raise (banded) plus a
    # game-level raise so strong hands are not trapped in the cheap band ----
    raise_suits = [s for s in ([agreed_suit] if agreed_suit else partner_suits) if s]
    for s in raise_suits if not quiet else []:
        # with a minor fit the game is 3NT, never a fallback 5m: cap the
        # invented raise ladder at the 4-level for every suit
        game_level = 4
        cheapest = None
        for level in range(1, 8):
            call = Call.bid(level, s)
            if call.bid_index > floor:
                cheapest = level
                break
        # never invent a slam raise: above game the auction needs real system
        # machinery (control bids / keycards), not a generic point count
        if cheapest is None or cheapest > game_level:
            continue
        lo = _RAISE_MIN_PTS.get(cheapest, 20)
        # uncontested: banded so stronger hands route to the game raise;
        # in competition the cheap raise is the full competitive range
        hi = 40 if (auction.is_competitive or cheapest >= game_level) \
            else (_RAISE_MIN_PTS.get(cheapest + 1, 40) - 1)
        evals = {"total_points": [lo, hi]}
        if cheapest >= 5:
            # Law of Total Tricks: an 11-trick competitive raise needs the
            # combined trumps to be there
            evals["lott_total_trumps"] = [cheapest + 5, 26]
        add(
            Call.bid(cheapest, s),
            _c(suits={s: [3, 13]}, evals=evals),
            f"raise: 3+ {s}, about {lo}-{hi if hi < 40 else '+'} support points",
            "non_forcing",
            12.0,
            agreed=s,
        )
        # the game raise picks up exactly where the cheap band ends, so no
        # support range is left without a bid
        if cheapest < game_level and str(Call.bid(cheapest, s)) not in covered_calls \
                and not game_forced:
            glo = hi + 1 if hi < 40 else _RAISE_MIN_PTS.get(game_level, 20)
            add(
                Call.bid(game_level, s),
                _c(suits={s: [3, 13]}, evals={"total_points": [glo, 40]}),
                f"raise to game: 3+ {s}, {glo}+ support points",
                "non_forcing",
                12.0,
                agreed=s,
            )

    # ---- new suits / rebids of own suits (only through the 3-level: above
    # that, raises / NT / pass are the sane undiscussed actions) ----
    for s in (SUITS if not (quiet or agreed_suit) else []):
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

    # ---- notrump (never invent a NATURAL notrump above 3NT: at the 4-level
    # and beyond NT is conventional, so a fallback 4NT is always wrong) ----
    for level in (range(1, 4) if not quiet else []):
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
            add(DOUBLE, _c(hcp=[10, 40], evals={"quick_tricks": [2, 9]}),
                "penalty-oriented double (undiscussed)", "non_forcing", 9.0)
        else:
            # cooperative, NOT forcing: an invented forcing meaning could trap
            # partner into a hopeless forced bid
            shorts = {s: [0, 2] for s in their_suits[:1]}
            add(DOUBLE, _c(hcp=[12, 40], suits=shorts),
                "takeout-flavored cooperative double (undiscussed)", "non_forcing", 9.0)

    # ---- ultimate backstop: cheapest legal bid, unconstrained.  Only when
    # passing is actually illegal - otherwise its unconstrained fit (1.0)
    # outscores a poorly-fitting pass and the engine bids on forever. ----
    if pass_forbidden and not any(m.call.is_bid for m in out):
        for b in auction.legal_calls():
            if b.is_bid:
                add(b, HandConstraint(), "forced continuation (undiscussed)", "non_forcing", 1.0)
                break

    return out
