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


LINTS = {"floor": lint_floor, "collide": lint_collide, "gap": lint_gap, "soft": lint_soft}


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
