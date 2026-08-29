"""Static lints for the bidding system.

Four defect species that three consecutive expert reviews rediscovered by
hand.  Every one of them is mechanically detectable, so no reviewer should
ever have to spend attention on them again:

  floor    a context defines a CALL but has no unconditional rule for it,
           so the context shadows the generic rule and can delete the call
           for any hand its gated rules miss
  collide  two rules in one context define the same call with materially
           different meanings - the engine merges same-call rules into a
           disjunction, so partner reads BOTH (a 6-10 raise that also read
           as game-forcing cost 23 IMPs)
  gap      a strength band inside a context that no rule covers, which the
           permissive pass floor then swallows ("range with no rule" is the
           single most recurring defect in the project's history)
  soft     a boolean/counting evaluator used as a [0,0]/[n,n] gate without a
           sharp tolerance registered, so "nearly satisfying" it scores ~0.8
           and the gate only leans

Usage:
    python3 tools/lint_system.py            # report
    python3 tools/lint_system.py --strict   # exit 1 on any finding
    python3 tools/lint_system.py --only gap
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from bridgebidder.constraints.model import _EVAL_S2, HandConstraint  # noqa: E402
from bridgebidder.system.dsl import BidRule, Context, load_system  # noqa: E402

# Evaluators whose values are counts or booleans: "nearly" satisfying them is
# meaningless, so a gate on one must be registered sharp in _EVAL_S2.
DISCRETE_EVALS = {
    "void", "singleton", "singleton_or_void", "balanced", "semi_balanced",
    "keycards", "trump_queen", "control_in", "controls", "aces", "kings",
    "worthless_doubleton", "two_of_top3", "three_of_top5", "good_suit",
    "suit_length", "longest_suit_length", "lott_total_trumps",
    "max_their_suit_length", "standing_suit_length", "is_partner_suit",
    "is_their_suit", "is_unbid_suit",
}


def eval_base(name: str) -> str:
    return name.split("(")[0].strip().strip('"')


def _walk(c: HandConstraint):
    yield c
    for sub in c.any_of + c.all_of:
        yield from _walk(sub)
    if c.not_ is not None:
        yield from _walk(c.not_)


def is_unconditional(r: BidRule) -> bool:
    """A floor rule: fires for any hand this context sees."""
    if not r.when.is_trivial:
        return False
    c = r.requires
    return not (c.hcp or c.suits or c.evals or c.features or c.shapes
                or c.any_of or c.all_of or c.not_)


def _band_of(c: HandConstraint) -> tuple[float, float] | None:
    if c.hcp:
        return (float(c.hcp[0]), float(c.hcp[1]))
    for k, v in c.evals.items():
        if eval_base(k) in ("total_points", "adjusted_hcp"):
            return (float(v[0]), float(v[1]))
    return None


def strength_band(r: BidRule) -> tuple[float, float] | None:
    """The rule's strength band - the HULL over any_of branches, since a
    rule stating "8-16 with shortness OR any 15+" covers 8-40, and reading
    only the top level invented gaps that do not exist."""
    c = r.requires
    top = _band_of(c)
    branches = [b for b in (_band_of(x) for x in c.any_of) if b]
    if branches:
        lo = min(b[0] for b in branches)
        hi = max(b[1] for b in branches)
        if top:
            lo, hi = min(lo, top[0]), max(hi, top[1])
        return (lo, hi)
    return top


def lint_floor(contexts: list[Context]) -> list[str]:
    """Contexts in which EVERY rule is gated, so the context can produce
    nothing at all for some hand it matches.

    Static shadow analysis per call is hopeless noise (the generic toolkit
    defines nearly every call, so every specific gated rule "shadows" one).
    What is checkable is this: a context with no unconditional rule anywhere
    is a context that can come up empty - and because it is the most
    specific interpreter for the calls it defines, coming up empty deletes
    those calls rather than falling through.  That is the shape behind both
    the splinter-context 4M deletion and the doubled-Stayman crash.

    Anchored patterns are reported first: an anchored context matches one
    exact auction family, so an empty result there is a real hole.
    """
    out = []
    for ctx in contexts:
        if not ctx.rules:
            continue
        if any(is_unconditional(r) for r in ctx.rules):
            continue
        anchored = not ctx.pattern.strip().startswith("...")
        # a context whose rules all carry a hand gate but which offers a
        # PASS is not stranded: passing is always legal and always available
        if any(r.call.is_pass for r in ctx.rules):
            continue
        out.append((0 if anchored else 1, ctx.pattern,
                    f"[floor]   {ctx.id} ({ctx.pattern!r}): every rule is gated "
                    f"and no pass is offered - the context can produce nothing "
                    f"({len(ctx.rules)} rules)"))
    return [msg for _, _, msg in sorted(out)]


def lint_collide(contexts: list[Context]) -> list[str]:
    out = []
    for ctx in contexts:
        by_call: dict[str, list[BidRule]] = defaultdict(list)
        for r in ctx.rules:
            by_call[str(r.call)].append(r)
        for call, rules in sorted(by_call.items()):
            if len(rules) < 2:
                continue
            # same-call rules merge into a disjunction, so a call meaning both
            # "weak" and "game forcing" is read as possibly-GF by partner
            forcings = {r.establishes.forcing for r in rules}
            gf = {"game_forcing"} & forcings
            weak = {"non_forcing", "sign_off"} & forcings
            if gf and weak:
                out.append(f"[collide] {ctx.id}: call {call} is defined both "
                           f"game-forcing and non-forcing "
                           f"({', '.join(r.id + ':' + r.establishes.forcing for r in rules)})")
                continue
            agreed = {r.establishes.agreed_suit for r in rules if r.establishes.agreed_suit}
            # rules whose `when` clauses are mutually exclusive can never
            # both match, so their readings never merge (the four per-suit
            # keycard asks are gated on partner_last_suit)
            gates = [r.when.partner_last_suit or r.when.partner_suit or
                     r.when.my_suit or r.when.standing_bid_strain for r in rules]
            exclusive = all(g is not None for g in gates) and len(set(map(str, gates))) == len(gates)
            if len(agreed) > 1 and not exclusive:
                out.append(f"[collide] {ctx.id}: call {call} agrees different "
                           f"suits {sorted(agreed)} ({', '.join(r.id for r in rules)})")
    return out


def lint_gap(contexts: list[Context], lo: int = 0, hi: int = 24) -> list[str]:
    """Strength bands no rule in the context claims.

    Only contexts whose rules are mostly band-stated are checked: a context
    of shape-driven rules (transfers, keycard replies) has no meaningful
    strength ladder and would produce pure noise.
    """
    out = []
    for ctx in contexts:
        banded = [r for r in ctx.rules if strength_band(r) is not None]
        if len(banded) < 3 or len(banded) < 0.6 * len(ctx.rules):
            continue
        if any(is_unconditional(r) for r in ctx.rules):
            continue  # a floor rule covers every band by construction
        covered = set()
        for r in banded:
            b0, b1 = strength_band(r)
            for pt in range(lo, hi + 1):
                if b0 <= pt <= b1:
                    covered.add(pt)
        missing = [pt for pt in range(lo, hi + 1) if pt not in covered]
        if not missing:
            continue
        # report only interior gaps: a context that starts at 6 is not
        # "missing" 0-5, it simply does not apply to those hands
        floor_pt = min(min(strength_band(r)) for r in banded)
        ceil_pt = max(max(strength_band(r)) for r in banded)
        interior = [pt for pt in missing if floor_pt < pt < ceil_pt]
        if interior:
            out.append(f"[gap]     {ctx.id}: no rule covers strength "
                       f"{interior} (context spans {floor_pt:.0f}-{ceil_pt:.0f})")
    return out


def lint_soft(contexts: list[Context]) -> list[str]:
    out = []
    seen: set[tuple[str, str]] = set()
    for ctx in contexts:
        for r in ctx.rules:
            for c in _walk(r.requires):
                for name, iv in c.evals.items():
                    base = eval_base(name)
                    if base not in DISCRETE_EVALS or base in _EVAL_S2:
                        continue
                    key = (r.id, base)
                    if key in seen:
                        continue
                    seen.add(key)
                    out.append(f"[soft]    {ctx.id}/{r.id}: gate on discrete "
                               f"evaluator '{base}' {list(iv)} has no sharp "
                               f"tolerance (nearly-satisfying it scores ~0.8)")
    return out



def _mentioned_suits(r: BidRule) -> set[str]:
    """Suits the rule's own constraint talks about (length or evaluator)."""
    out: set[str] = set()
    for c in _walk(r.requires):
        out |= set(c.suits)
        for name in list(c.evals) + list(c.features):
            for suit in "CDHS":
                if f"({suit})" in name or f"({suit}," in name or f", {suit})" in name:
                    out.add(suit)
    return out


def lint_shape(contexts: list[Context]) -> list[str]:
    """Ladders that band by strength but never band by shape.

    Both reviewers of the seed-515151 match named this species
    independently: a context whose rules ladder purely on points has no
    rung for "responder holds his own long suit", so a six-bagger falls
    through to the catch-all pass.  Four contexts in that match had the
    defect and the `gap` lint could not see any of them - it reads
    strength only.

    Flagged: a context of three or more rules where every rule states a
    strength band and NO rule mentions a suit at all.  Such a ladder can
    only ever describe how strong the hand is, never what it looks like.
    """
    out = []
    for ctx in contexts:
        if len(ctx.rules) < 3:
            continue
        banded = [r for r in ctx.rules if strength_band(r) is not None]
        if len(banded) < 3 or len(banded) < 0.6 * len(ctx.rules):
            continue
        if any(_mentioned_suits(r) for r in ctx.rules):
            continue
        # a ladder whose bids are all in ONE strain is "how high in the suit
        # we have agreed", which needs no shape rung by construction
        strains = {r.call.strain for r in ctx.rules
                   if r.call.is_bid and not r.establishes.asking}
        if len(strains) < 2:
            continue
        out.append(f"[shape]   {ctx.id} ({ctx.pattern!r}): {len(ctx.rules)} rules "
                   f"ladder on strength alone - no rung mentions a suit, so a "
                   f"long-suit hand has nothing to bid")
    return out


def lint_siblings(contexts: list[Context]) -> list[str]:
    """A gate added to one member of a rule FAMILY but not to the others.

    The species both reviewers named.  Every real instance crossed calls
    or contexts rather than sitting side by side: the four per-suit keycard
    asks (a combined-trump gate added, the raw length gate left behind),
    the 2/1 denial written over 1S but not over 1H, a trump gate on the
    direct raise but not on the ask continuation.  So the grouping key is
    the rule id with suit letters and level digits normalised away, which
    is exactly what makes `gst_rkc_C/D/H/S` or `r1H_2C`/`r1S_2C` one
    family, and the check is whether one member's evaluator gate-set is
    missing something all the others require.

    Strength terms are excluded: rungs of a ladder differ by strength by
    design.
    """
    STRENGTH = {"total_points", "adjusted_hcp", "rule_of_26",
                "rule_of_26_sharp", "hcp"}

    def family_key(rid: str) -> str:
        k = re.sub(r"\$?[A-Z]{1,2}\b", "#", rid)      # $M, $oM, C, D, H, S
        k = re.sub(r"\d+", "#", k)                    # level digits
        return k

    fams: dict[str, list[tuple[str, set[str]]]] = defaultdict(list)
    for ctx in contexts:
        for r in ctx.rules:
            gates: set[str] = set()
            for c in _walk(r.requires):
                gates |= {eval_base(k) for k in c.evals}
                gates |= {eval_base(f) for f in c.features}
            gates -= STRENGTH
            bands: dict[str, tuple[float, float]] = {}
            for c in _walk(r.requires):
                for k, v in c.evals.items():
                    if eval_base(k) not in STRENGTH:
                        bands[k] = (float(v[0]), float(v[1]))
            # context ids carry the expansion in brackets; strip it so the
            # same rule across expansions lands in one family
            kind = ("nt" if (r.call.is_bid and r.call.strain == "NT")
                    else "bid" if r.call.is_bid
                    else "pass" if r.call.is_pass else "dbl")
            level = r.call.level if r.call.is_bid else 0
            fams[family_key(r.id) + "|" + kind].append(
                (f"{ctx.id.split('[')[0]}/{r.id}", gates, bands, level))

    # Divergences that are deliberate, with the reason.  A lint you cannot
    # tell "yes, on purpose" is a lint people learn to ignore wholesale.
    INTENTIONAL = {
        # round 3: six cards IS the credential for a reopening rebid - the
        # quality floor was pushing honourless six-baggers into a stopperless
        # 1NT, so the *2 rungs deliberately dropped what *3/*4 still require
        "ballow_rebid", "balhigh_rebid",
        # the 1430 ANSWERING scheme: 5C = 1-or-4, 5D = 0-or-3, 5H = 2 without
        # the queen, 5S = 2 with it.  Different bands per call are the whole
        # convention, not a divergence.
        "rkc",
    }

    out = []
    for fam, members in sorted(fams.items()):
        if any(name.split("/")[-1].rsplit("_", 1)[0] in INTENTIONAL
               for name, *_ in members):
            continue
        # one instance per expansion is normal; a family needs >= 3 members
        # before a lone odd one out means anything
        if len(members) < 3:
            continue
        # (a) a gate the rest of the family requires and this member lacks
        uniq = {frozenset(g) for _, g, _, _ in members}
        if len(uniq) >= 2:
            common = set.intersection(*(g for _, g, _, _ in members))
            union = set().union(*(g for _, g, _, _ in members))
            shared_by_most = {
                gate for gate in union - common
                if sum(1 for _, g, _, _ in members if gate in g) >= max(2, len(members) - 1)
            }
            for name, gates, _, _ in members:
                missing = shared_by_most - gates
                if missing:
                    out.append(f"[sibling] {name}: lacks {sorted(missing)}, required by "
                               f"the rest of its family ({len(members)} members)")
        # (b) the SAME gate carrying a different BAND on one member.  A
        # presence-only diff cannot see this, and it is how a correction
        # applied to the major-suit keycard continuations was left off the
        # minor-suit ones for two rounds: the gate was there in both, but
        # one still demanded three keycards where the rest asked for two.
        keys = set().union(*(set(b) for _, _, b, _ in members))
        for key in sorted(keys):
            vals = [(name, b[key], lv) for name, _, b, lv in members if key in b]
            if len(vals) < 3:
                continue
            # A band that rises with the call level is a LADDER, not a
            # divergence: a two-level raise legitimately needs seven
            # combined trumps where the three-level rung needs eight.
            by_level = sorted(vals, key=lambda t: t[2])
            los = [v[0] for _, v, _ in by_level]
            if len({lv for _, _, lv in vals}) > 1 and los == sorted(los):
                continue
            counts: dict[tuple[float, float], int] = defaultdict(int)
            for _, v, _ in vals:
                counts[v] += 1
            if len(counts) < 2:
                continue
            majority, n_major = max(counts.items(), key=lambda kv: kv[1])
            same_level = len({lv for _, _, lv in vals}) == 1
            # At ONE call level there is no ladder to justify a divergence,
            # so any split is a finding - including an even one.  (The
            # major-suit keycard continuations were corrected to two
            # keycards while the minor-suit ones stayed at three: a 2-2
            # split that a majority rule would have skipped forever.)
            if not same_level and n_major < len(vals) - 1:
                continue  # a genuine per-member ladder
            for name, v, _ in vals:
                if v != majority:
                    out.append(f"[sibling] {name}: gate '{key}' is {list(v)} but "
                               f"{n_major} of {len(vals)} family members at the "
                               f"same level use {list(majority)}")
    return out


LINTS = {"floor": lint_floor, "collide": lint_collide, "gap": lint_gap,
         "soft": lint_soft, "shape": lint_shape, "sibling": lint_siblings}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--strict", action="store_true", help="exit 1 on findings")
    ap.add_argument("--only", choices=sorted(LINTS), action="append")
    ap.add_argument("--quiet", action="store_true", help="counts only")
    args = ap.parse_args()

    system = load_system()
    contexts = list(system.contexts)
    names = args.only or sorted(LINTS)
    total = 0
    for name in names:
        findings = LINTS[name](contexts)
        total += len(findings)
        print(f"=== {name}: {len(findings)} finding(s) ===")
        if not args.quiet:
            for f in findings:
                print(" ", f)
    print(f"\n{total} finding(s) over {len(contexts)} contexts, "
          f"{sum(len(c.rules) for c in contexts)} rules")
    return 1 if (args.strict and total) else 0


if __name__ == "__main__":
    raise SystemExit(main())
