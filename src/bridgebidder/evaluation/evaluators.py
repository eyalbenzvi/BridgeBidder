"""Standard hand evaluators, registered by name.

Suit arguments are letters S/H/D/C.  Where noted, a suit argument may also be
"partner" (partner's first shown suit), "agreed" (the agreed trump suit) or
"their" (opponents' first shown suit); resolution uses the EvalContext.
"""

from __future__ import annotations

from ..domain.cards import Hand, SUITS
from .registry import EvalContext, register_evaluator


def _resolve_suit(arg: str, ctx: EvalContext) -> str | None:
    arg = arg.strip()
    if arg in SUITS:
        return arg
    if arg == "partner":
        return ctx.partner_suits[0] if ctx.partner_suits else None
    if arg == "agreed":
        return ctx.agreed_suit
    if arg == "their":
        return ctx.their_suits[0] if ctx.their_suits else None
    raise ValueError(f"Bad suit argument {arg!r}")


# --------------------------------------------------------------------------
# point counts
# --------------------------------------------------------------------------

@register_evaluator("hcp")
def hcp(hand: Hand, ctx: EvalContext) -> float:
    return hand.hcp


@register_evaluator("adjusted_hcp")
def adjusted_hcp(hand: Hand, ctx: EvalContext) -> float:
    """HCP with honor-location adjustments: deduct for stiff/unguarded honors,
    add a bit for concentrated honors with length."""
    val = float(hand.hcp)
    for s in SUITS:
        ranks = hand.suit_ranks(s)
        n = len(ranks)
        if n == 1 and ranks[0] in (13, 12, 11):  # stiff K/Q/J
            val -= 1.0
        elif n == 2:
            if 12 in ranks and 14 not in ranks and 13 not in ranks:  # Qx no A/K
                val -= 0.5
            if 11 in ranks and not any(r >= 12 for r in ranks):  # Jx bare-ish
                val -= 0.5
        if n >= 5 and sum(1 for r in ranks if r >= 12) >= 2:  # honors in long suit
            val += 0.5
    return val


@register_evaluator("dist_points")
def dist_points(hand: Hand, ctx: EvalContext) -> float:
    """Length points: one per card over four in each suit."""
    return float(sum(max(0, hand.suit_length(s) - 4) for s in SUITS))


@register_evaluator("shortness_points")
def shortness_points(hand: Hand, ctx: EvalContext) -> float:
    """Dummy points for shortness outside the agreed trump suit
    (void=5, singleton=3, doubleton=1)."""
    trump = ctx.agreed_suit
    pts = 0
    for s in SUITS:
        if s == trump:
            continue
        n = hand.suit_length(s)
        if n == 0:
            pts += 5
        elif n == 1:
            pts += 3
        elif n == 2:
            pts += 1
    return float(pts)


@register_evaluator("total_points")
def total_points(hand: Hand, ctx: EvalContext) -> float:
    """HCP + distribution.  Support-context aware: when a trump suit is agreed
    (or being agreed) and we hold 3+ of it, count shortness instead of length."""
    trump = ctx.agreed_suit
    if trump and hand.suit_length(trump) >= 3:
        return hand.hcp + shortness_points(hand, ctx)
    return hand.hcp + dist_points(hand, ctx)


@register_evaluator("rule_of_20")
def rule_of_20(hand: Hand, ctx: EvalContext) -> float:
    """HCP + lengths of the two longest suits (open when >= 20, seats 1-2)."""
    lens = sorted(hand.lengths.values(), reverse=True)
    return hand.hcp + lens[0] + lens[1]


@register_evaluator("rule_of_15")
def rule_of_15(hand: Hand, ctx: EvalContext) -> float:
    """HCP + number of spades (4th-seat opening test, >= 15)."""
    return hand.hcp + hand.suit_length("S")


@register_evaluator("rule_of_26")
def rule_of_26(hand: Hand, ctx: EvalContext) -> float:
    """Combined-values game test: my total points + midpoint of partner's
    shown HCP range (>= 26 suggests game)."""
    # partner's strength may have been shown in HCP or in support points;
    # take whichever bound is more informative
    floor = max(ctx.partner_min_hcp, ctx.partner_min_points)
    partner_mid = (floor + min(max(ctx.partner_max_hcp, floor), floor + 4)) / 2
    return total_points(hand, ctx) + partner_mid


# --------------------------------------------------------------------------
# trick-oriented
# --------------------------------------------------------------------------

@register_evaluator("ltc")
def ltc(hand: Hand, ctx: EvalContext) -> float:
    """Losing Trick Count (basic)."""
    losers = 0.0
    for s in SUITS:
        ranks = hand.suit_ranks(s)
        n = len(ranks)
        considered = min(3, n)
        winners = 0
        if n >= 1 and 14 in ranks:
            winners += 1
        if n >= 2 and 13 in ranks:
            winners += 1
        if n >= 3 and 12 in ranks:
            winners += 1
        losers += considered - min(winners, considered)
    return losers


@register_evaluator("controls")
def controls(hand: Hand, ctx: EvalContext) -> float:
    """A=2, K=1."""
    return float(sum(2 for c in hand.cards if c.rank == 14) + sum(1 for c in hand.cards if c.rank == 13))


@register_evaluator("quick_tricks")
def quick_tricks(hand: Hand, ctx: EvalContext) -> float:
    qt = 0.0
    for s in SUITS:
        ranks = set(hand.suit_ranks(s))
        n = hand.suit_length(s)
        if 14 in ranks and 13 in ranks:
            qt += 2.0
        elif 14 in ranks and 12 in ranks:
            qt += 1.5
        elif 14 in ranks:
            qt += 1.0
        elif 13 in ranks and 12 in ranks:
            qt += 1.0
        elif 13 in ranks and n >= 2:
            qt += 0.5
    return qt


@register_evaluator("quick_tricks_outside")
def quick_tricks_outside(hand: Hand, ctx: EvalContext, suit: str = "S") -> float:
    """Quick tricks excluding the named suit - the preempt-veto measure.
    AK inside your own seven-bagger is offence, not defence; what vetoes a
    preempt is fast DEFENSIVE tricks in the other three suits."""
    s = _resolve_suit(suit, ctx)
    qt = 0.0
    for other in SUITS:
        if other == s:
            continue
        ranks = set(hand.suit_ranks(other))
        n = hand.suit_length(other)
        if 14 in ranks and 13 in ranks:
            qt += 2.0
        elif 14 in ranks and 12 in ranks:
            qt += 1.5
        elif 14 in ranks:
            qt += 1.0
        elif 13 in ranks and 12 in ranks:
            qt += 1.0
        elif 13 in ranks and n >= 2:
            qt += 0.5
    return qt


@register_evaluator("max_their_suit_length")
def max_their_suit_length(hand: Hand, ctx: EvalContext) -> float:
    """My longest holding across ALL the suits the opponents have shown -
    the honest "short in their suit" test.  `suit_length(their)` reads only
    their FIRST suit, so with two or three suits on the other side the
    takeout-shape gate was nearly vacuous (a hand doubled holding four
    cards in their second suit).  0 when they have shown nothing."""
    if not ctx.their_suits:
        return 0.0
    return float(max(hand.suit_length(s) for s in set(ctx.their_suits)))


@register_evaluator("lott_total_trumps")
def lott_total_trumps(hand: Hand, ctx: EvalContext, suit: str = "") -> float:
    """Law of Total Tricks support: our side's known combined trumps
    (my length in the named suit + partner's minimum shown length there).

    With no argument it reads the agreed suit, or partner's FIRST shown suit -
    which is wrong for any rule about a different suit, and every raise rule
    is about a specific one.  Name the suit.
    """
    s = _resolve_suit(suit, ctx) if suit else (
        ctx.agreed_suit or (ctx.partner_suits[0] if ctx.partner_suits else None))
    if s is None:
        return 0.0
    return float(hand.suit_length(s) + ctx.partner_min_length.get(s, 0))


# --------------------------------------------------------------------------
# suit quality / features
# --------------------------------------------------------------------------

@register_evaluator("suit_length")
def suit_length(hand: Hand, ctx: EvalContext, suit: str = "S") -> float:
    s = _resolve_suit(suit, ctx)
    return float(hand.suit_length(s)) if s else 0.0


@register_evaluator("suit_diff")
def suit_diff(hand: Hand, ctx: EvalContext, a: str = "S", b: str = "H") -> float:
    """Length difference between two suits (relational shape constraints)."""
    sa, sb = _resolve_suit(a, ctx), _resolve_suit(b, ctx)
    if sa is None or sb is None:
        return 0.0
    return float(hand.suit_length(sa) - hand.suit_length(sb))


@register_evaluator("longest_suit_length")
def longest_suit_length(hand: Hand, ctx: EvalContext) -> float:
    return float(hand.shape[0])


@register_evaluator("suit_quality")
def suit_quality(hand: Hand, ctx: EvalContext, suit: str = "S") -> float:
    """Honor-weighted quality: A/K/Q count 1 each, J/T count 0.5 each."""
    s = _resolve_suit(suit, ctx)
    if s is None:
        return 0.0
    ranks = hand.suit_ranks(s)
    return sum(1.0 for r in ranks if r >= 12) + sum(0.5 for r in ranks if r in (10, 11))


@register_evaluator("two_of_top3")
def two_of_top3(hand: Hand, ctx: EvalContext, suit: str = "S") -> float:
    s = _resolve_suit(suit, ctx)
    if s is None:
        return 0.0
    return 1.0 if sum(1 for r in hand.suit_ranks(s) if r >= 12) >= 2 else 0.0


@register_evaluator("three_of_top5")
def three_of_top5(hand: Hand, ctx: EvalContext, suit: str = "S") -> float:
    s = _resolve_suit(suit, ctx)
    if s is None:
        return 0.0
    return 1.0 if sum(1 for r in hand.suit_ranks(s) if r >= 10) >= 3 else 0.0


@register_evaluator("good_suit")
def good_suit(hand: Hand, ctx: EvalContext, suit: str = "S") -> float:
    """Preempt-quality suit: 2 of top 3 or 3 of top 5 honors."""
    return 1.0 if (two_of_top3(hand, ctx, suit) or three_of_top5(hand, ctx, suit)) else 0.0


@register_evaluator("stoppers")
def stoppers(hand: Hand, ctx: EvalContext, suit: str = "S") -> float:
    """1.0 = full stopper (A / Kx / QJx / Qxx / JTxx), 0.5 = partial (Qx / Jxx), 0 = none."""
    s = _resolve_suit(suit, ctx)
    if s is None:
        return 1.0  # vacuously stopped: nobody has shown a suit to stop
    ranks = hand.suit_ranks(s)
    n = len(ranks)
    if 14 in ranks:
        return 1.0
    if 13 in ranks and n >= 2:
        return 1.0
    if 12 in ranks and n >= 3:
        return 1.0
    if 11 in ranks and 10 in ranks and n >= 4:
        return 1.0
    if 12 in ranks and n == 2:
        return 0.5
    if 11 in ranks and n >= 3:
        return 0.5
    return 0.0


@register_evaluator("stopper")
def stopper(hand: Hand, ctx: EvalContext, suit: str = "S") -> float:
    """Boolean: full stopper in suit (vacuously true if the suit is unresolved)."""
    return 1.0 if stoppers(hand, ctx, suit) >= 1.0 else 0.0


@register_evaluator("weakest_unshown_stopper")
def weakest_unshown_stopper(hand: Hand, ctx: EvalContext) -> float:
    """The worst stopper among suits our side has NOT shown - the 3NT
    question.  "If 3NT is one of the logical options, bid it" is only sound
    when the unshown suits are actually stopped; a suit partner has bid, or
    the agreed suit, is partner's to stop.  1.0 = every unshown suit fully
    stopped, 0.5 = one of them only half-stopped (Qx / Jxx), 0 = one wide
    open."""
    shown = set(ctx.partner_suits)
    if ctx.agreed_suit:
        shown.add(ctx.agreed_suit)
    worst = 1.0
    for s in SUITS:
        if s in shown:
            continue
        worst = min(worst, stoppers(hand, ctx, s))
    return worst


@register_evaluator("weakest_their_stopper")
def weakest_their_stopper(hand: Hand, ctx: EvalContext) -> float:
    """The worst stopper among ALL the suits the opponents have shown - the
    competitive-3NT question.  `stoppers(their)` reads only their first
    suit (the same trap lott_total_trumps fell into), so a two-suited
    opposition left 3NT ungated in the second suit.  Vacuously 1.0 when
    they have shown nothing."""
    worst = 1.0
    for s in set(ctx.their_suits):
        worst = min(worst, stoppers(hand, ctx, s))
    return worst


@register_evaluator("wasted_in_partner_shortness")
def wasted_in_partner_shortness(hand: Hand, ctx: EvalContext) -> float:
    """Duplication detector: K/Q/J points held in a suit partner has shown
    shortness in (max length <= 1 - a splinter, or a Jacoby shortness
    reply).  Kings and queens opposite a singleton are wasted paper; ACES
    are not counted, because an ace works opposite anything.  Zero when
    partner has shown no shortness, so gates on this only ever fire once
    shortness is actually on the table."""
    pts = 0.0
    for s, mx in ctx.partner_max_length.items():
        if mx > 1:
            continue
        for r in hand.suit_ranks(s):
            if r == 13:
                pts += 3
            elif r == 12:
                pts += 2
            elif r == 11:
                pts += 1
    return pts


@register_evaluator("worthless_doubleton")
def worthless_doubleton(hand: Hand, ctx: EvalContext) -> float:
    """1.0 if the hand holds a doubleton headed by nothing better than the
    jack (xx / Jx) - the classic Blackwood veto: two fast losers that no
    keycard answer can diagnose.  Suits partner has bid naturally (shown
    4+ cards) and the agreed trump suit are exempt: xx under partner's
    known length is covered from the other side of the table, not a flaw."""
    for s in SUITS:
        if ctx.partner_min_length.get(s, 0) >= 4 or s == ctx.agreed_suit:
            continue
        ranks = hand.suit_ranks(s)
        if len(ranks) == 2 and max(ranks) < 12:
            return 1.0
    return 0.0


@register_evaluator("void")
def void(hand: Hand, ctx: EvalContext, suit: str = "any") -> float:
    if suit == "any":
        return 1.0 if 0 in hand.lengths.values() else 0.0
    s = _resolve_suit(suit, ctx)
    return 1.0 if s and hand.suit_length(s) == 0 else 0.0


@register_evaluator("singleton")
def singleton(hand: Hand, ctx: EvalContext, suit: str = "any") -> float:
    if suit == "any":
        return 1.0 if 1 in hand.lengths.values() else 0.0
    s = _resolve_suit(suit, ctx)
    return 1.0 if s and hand.suit_length(s) == 1 else 0.0


@register_evaluator("singleton_or_void")
def singleton_or_void(hand: Hand, ctx: EvalContext, suit: str = "any") -> float:
    if suit == "any":
        return 1.0 if any(n <= 1 for n in hand.lengths.values()) else 0.0
    s = _resolve_suit(suit, ctx)
    return 1.0 if s and hand.suit_length(s) <= 1 else 0.0


# --------------------------------------------------------------------------
# shape classifiers
# --------------------------------------------------------------------------

@register_evaluator("balanced")
def balanced(hand: Hand, ctx: EvalContext) -> float:
    """4333 / 4432 / 5332."""
    return 1.0 if hand.shape in ((4, 3, 3, 3), (4, 4, 3, 2), (5, 3, 3, 2)) else 0.0


@register_evaluator("semi_balanced")
def semi_balanced(hand: Hand, ctx: EvalContext) -> float:
    """Balanced shapes plus 5422 / 6322."""
    return 1.0 if (balanced(hand, ctx) or hand.shape in ((5, 4, 2, 2), (6, 3, 2, 2))) else 0.0


@register_evaluator("keycards")
def keycards(hand: Hand, ctx: EvalContext, suit: str = "agreed") -> float:
    """RKC keycards: 4 aces + the king of trumps."""
    s = _resolve_suit(suit, ctx)
    aces = sum(1 for c in hand.cards if c.rank == 14)
    trump_k = 1 if (s and 13 in hand.suit_ranks(s)) else 0
    return float(aces + trump_k)


@register_evaluator("trump_queen")
def trump_queen(hand: Hand, ctx: EvalContext, suit: str = "agreed") -> float:
    s = _resolve_suit(suit, ctx)
    return 1.0 if (s and 12 in hand.suit_ranks(s)) else 0.0


@register_evaluator("control_in")
def control_in(hand: Hand, ctx: EvalContext, suit: str = "S") -> float:
    """Controls held in one suit: 2 = first round (ace or void),
    1 = second round (king or singleton), 0 = none.  The currency of
    cue-bidding: a slam needs first-round control of every side suit."""
    s = _resolve_suit(suit, ctx)
    if s is None:
        return 0.0
    ranks = hand.suit_ranks(s)
    n = len(ranks)
    if n == 0 or 14 in ranks:
        return 2.0
    if n == 1 or 13 in ranks:
        return 1.0
    return 0.0


@register_evaluator("aces")
def aces(hand: Hand, ctx: EvalContext) -> float:
    return float(sum(1 for c in hand.cards if c.rank == 14))


@register_evaluator("kings")
def kings(hand: Hand, ctx: EvalContext) -> float:
    return float(sum(1 for c in hand.cards if c.rank == 13))


# --------------------------------------------------------------------------
# auction-relative suit predicates
#
# These let the DSL express *general agreements* ("raise partner's suit",
# "bid a natural unbid suit") without naming a concrete suit, so the generic
# competitive and continuation toolkit lives in the system file as data
# instead of in engine code.
# --------------------------------------------------------------------------

@register_evaluator("is_partner_suit")
def is_partner_suit(hand: Hand, ctx: EvalContext, suit: str = "S") -> float:
    s = _resolve_suit(suit, ctx)
    if s is None:
        return 0.0
    return 1.0 if (s == ctx.agreed_suit or s in ctx.partner_suits) else 0.0


@register_evaluator("is_their_suit")
def is_their_suit(hand: Hand, ctx: EvalContext, suit: str = "S") -> float:
    s = _resolve_suit(suit, ctx)
    return 1.0 if (s is not None and s in ctx.their_suits) else 0.0


@register_evaluator("is_unbid_suit")
def is_unbid_suit(hand: Hand, ctx: EvalContext, suit: str = "S") -> float:
    """True when neither partner nor the opponents have shown this suit."""
    s = _resolve_suit(suit, ctx)
    if s is None:
        return 0.0
    shown = set(ctx.partner_suits) | set(ctx.their_suits)
    if ctx.agreed_suit:
        shown.add(ctx.agreed_suit)
    return 0.0 if s in shown else 1.0
