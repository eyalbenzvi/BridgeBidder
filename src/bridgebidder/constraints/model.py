"""HandConstraint: declarative constraints over a bridge hand.

Supports exact satisfaction, *soft* degree-of-fit scoring (sigmoid-ish
penalties around interval boundaries), intersection, negation-as-disjunction,
and a coarse interval summary (bounding box) for UI display and sampler
pre-filtering.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field, replace

from ..domain.cards import Hand, SUITS
from ..evaluation.registry import EvalContext, evaluate

Interval = tuple[float, float]

# Gaussian softness (sigma^2) per field kind: fit = exp(-(deficit^2)/s2).
# Calibrated so a 1-HCP deficit scores ~0.8 (mission requirement) and a
# 1-card suit-length deficit scores ~0.35 (length errors matter more).
_S2_HCP = 4.48
_S2_SUIT = 0.95
_S2_EVAL_DEFAULT = 4.48
# Sharper softness for specific evaluators (value units differ per evaluator)
_EVAL_S2 = {
    "ltc": 1.4,
    "controls": 1.4,
    "keycards": 0.05,
    "trump_queen": 0.05,
    "aces": 0.4,
    "kings": 0.4,
    "quick_tricks": 0.9,
    "suit_quality": 0.9,
    "stoppers": 0.3,
    "suit_length": _S2_SUIT,
    "longest_suit_length": _S2_SUIT,
    "balanced": 0.08,
    "semi_balanced": 0.08,
}

_FEATURE_MISS_FIT = 0.2

FULL_HCP: Interval = (0.0, 40.0)
FULL_SUIT: Interval = (0.0, 13.0)


def _interval_deficit(v: float, iv: Interval) -> float:
    lo, hi = iv
    if v < lo:
        return lo - v
    if v > hi:
        return v - hi
    return 0.0


def _gauss_fit(deficit: float, s2: float) -> float:
    if deficit <= 0:
        return 1.0
    return math.exp(-(deficit * deficit) / s2)


def _isect(a: Interval | None, b: Interval | None) -> Interval | None:
    if a is None:
        return b
    if b is None:
        return a
    return (max(a[0], b[0]), min(a[1], b[1]))


def _hull(a: Interval | None, b: Interval | None, full: Interval) -> Interval:
    a = a or full
    b = b or full
    return (min(a[0], b[0]), max(a[1], b[1]))


@dataclass(frozen=True)
class Box:
    """Coarse interval summary of a constraint (a bounding box)."""

    hcp: Interval = FULL_HCP
    suits: dict[str, Interval] = field(default_factory=dict)

    def suit(self, s: str) -> Interval:
        return self.suits.get(s, FULL_SUIT)

    def intersect(self, other: "Box") -> "Box":
        suits = {}
        for s in SUITS:
            iv = _isect(self.suits.get(s), other.suits.get(s))
            if iv is not None:
                suits[s] = (max(iv[0], 0.0), min(iv[1], 13.0))
        return Box(hcp=_isect(self.hcp, other.hcp) or FULL_HCP, suits=suits)

    def hull(self, other: "Box") -> "Box":
        suits = {}
        for s in SUITS:
            if s in self.suits or s in other.suits:
                suits[s] = _hull(self.suits.get(s), other.suits.get(s), FULL_SUIT)
        return Box(hcp=_hull(self.hcp, other.hcp, FULL_HCP), suits=suits)

    @property
    def is_empty(self) -> bool:
        if self.hcp[0] > self.hcp[1]:
            return True
        if any(iv[0] > iv[1] for iv in self.suits.values()):
            return True
        min_total = sum(iv[0] for s, iv in self.suits.items())
        max_total = sum(self.suits.get(s, FULL_SUIT)[1] for s in SUITS)
        return min_total > 13 or max_total < 13

    def accepts(self, hand: Hand) -> bool:
        if not self.hcp[0] <= hand.hcp <= self.hcp[1]:
            return False
        return all(iv[0] <= hand.suit_length(s) <= iv[1] for s, iv in self.suits.items())

    def to_dict(self) -> dict:
        return {
            "hcp": [self.hcp[0], self.hcp[1]],
            "suits": {s: [iv[0], iv[1]] for s, iv in sorted(self.suits.items(), key=lambda kv: SUITS.index(kv[0]))},
        }


def _parse_shape(pat: str) -> tuple[bool, tuple[int, ...]]:
    """Return (exact, lengths). "5=3=3=2" is exact S=H=D=C; "5332" is any order."""
    if "=" in pat:
        parts = tuple(int(p) for p in pat.split("="))
        if len(parts) != 4 or sum(parts) != 13:
            raise ValueError(f"Bad exact shape {pat!r}")
        return True, parts
    parts = tuple(sorted((int(ch) for ch in pat), reverse=True))
    if len(parts) != 4 or sum(parts) != 13:
        raise ValueError(f"Bad shape {pat!r}")
    return False, parts


@dataclass(frozen=True)
class HandConstraint:
    """A conjunction of simple field constraints plus logical combinators."""

    hcp: Interval | None = None
    suits: dict[str, Interval] = field(default_factory=dict)
    evals: dict[str, Interval] = field(default_factory=dict)
    features: tuple[str, ...] = ()
    shapes: tuple[str, ...] = ()
    any_of: tuple["HandConstraint", ...] = ()
    all_of: tuple["HandConstraint", ...] = ()
    not_: "HandConstraint | None" = None

    # ----------------------------------------------------------------- parse
    @staticmethod
    def from_dict(d: dict | None) -> "HandConstraint":
        if not d:
            return HandConstraint()
        d = dict(d)
        # sugar
        evals = {k: tuple(v) for k, v in (d.pop("evals", {}) or {}).items()}
        for sugar in ("balanced", "semi_balanced"):
            if sugar in d:
                want = d.pop(sugar)
                evals[sugar] = (1, 1) if want else (0, 0)
        kw = dict(
            hcp=tuple(d.pop("hcp")) if d.get("hcp") is not None else d.pop("hcp", None),
            suits={k: tuple(v) for k, v in (d.pop("suits", {}) or {}).items()},
            evals=evals,
            features=tuple(d.pop("features", []) or []),
            shapes=tuple(d.pop("shapes", []) or []),
            any_of=tuple(HandConstraint.from_dict(x) for x in d.pop("any_of", []) or []),
            all_of=tuple(HandConstraint.from_dict(x) for x in d.pop("all_of", []) or []),
            not_=HandConstraint.from_dict(d.pop("not")) if d.get("not") is not None else d.pop("not", None),
        )
        if d:
            raise ValueError(f"Unknown constraint keys: {sorted(d)}")
        c = HandConstraint(**kw)
        for s in c.suits:
            if s not in SUITS:
                raise ValueError(f"Bad suit key {s!r} in constraint")
        for pat in c.shapes:
            _parse_shape(pat)
        return c

    def to_dict(self) -> dict:
        out: dict = {}
        if self.hcp:
            out["hcp"] = list(self.hcp)
        if self.suits:
            out["suits"] = {k: list(v) for k, v in self.suits.items()}
        if self.evals:
            out["evals"] = {k: list(v) for k, v in self.evals.items()}
        if self.features:
            out["features"] = list(self.features)
        if self.shapes:
            out["shapes"] = list(self.shapes)
        if self.any_of:
            out["any_of"] = [c.to_dict() for c in self.any_of]
        if self.all_of:
            out["all_of"] = [c.to_dict() for c in self.all_of]
        if self.not_:
            out["not"] = self.not_.to_dict()
        return out

    @property
    def is_trivial(self) -> bool:
        return not (
            self.hcp or self.suits or self.evals or self.features or self.shapes
            or self.any_of or self.all_of or self.not_
        )

    # ------------------------------------------------------------ evaluation
    def _shape_ok(self, hand: Hand) -> bool:
        if not self.shapes:
            return True
        for pat in self.shapes:
            exact, lens = _parse_shape(pat)
            if exact and hand.exact_shape == lens:
                return True
            if not exact and hand.shape == lens:
                return True
        return False

    def satisfied(self, hand: Hand, ctx: EvalContext | None = None) -> bool:
        ctx = ctx or EvalContext()
        if self.hcp and not self.hcp[0] <= hand.hcp <= self.hcp[1]:
            return False
        for s, iv in self.suits.items():
            if not iv[0] <= hand.suit_length(s) <= iv[1]:
                return False
        for spec, iv in self.evals.items():
            v = evaluate(spec, hand, ctx)
            if not iv[0] <= v <= iv[1]:
                return False
        for spec in self.features:
            if evaluate(spec, hand, ctx) < 0.5:
                return False
        if not self._shape_ok(hand):
            return False
        if self.any_of and not any(c.satisfied(hand, ctx) for c in self.any_of):
            return False
        if any(not c.satisfied(hand, ctx) for c in self.all_of):
            return False
        if self.not_ is not None and self.not_.satisfied(hand, ctx):
            return False
        return True

    def fit(self, hand: Hand, ctx: EvalContext | None = None) -> float:
        """Soft degree of fit in [0, 1]; 1.0 = fully satisfied."""
        ctx = ctx or EvalContext()
        f = 1.0
        if self.hcp:
            f *= _gauss_fit(_interval_deficit(hand.hcp, self.hcp), _S2_HCP)
        for s, iv in self.suits.items():
            f *= _gauss_fit(_interval_deficit(hand.suit_length(s), iv), _S2_SUIT)
        for spec, iv in self.evals.items():
            v = evaluate(spec, hand, ctx)
            base = spec.split("(")[0].strip()
            f *= _gauss_fit(_interval_deficit(v, iv), _EVAL_S2.get(base, _S2_EVAL_DEFAULT))
        for spec in self.features:
            if evaluate(spec, hand, ctx) < 0.5:
                f *= _FEATURE_MISS_FIT
        if not self._shape_ok(hand):
            f *= 0.15
        for c in self.all_of:
            f *= c.fit(hand, ctx)
        if self.any_of:
            f *= max(c.fit(hand, ctx) for c in self.any_of)
        if self.not_ is not None:
            # negation is sharp: nearly-matching the denied condition is fine,
            # actually matching it is a hard miss
            f *= 0.1 if self.not_.satisfied(hand, ctx) else 1.0
        return max(0.0, min(1.0, f))

    # ------------------------------------------------------------- algebra
    def intersect(self, other: "HandConstraint") -> "HandConstraint":
        if other.is_trivial:
            return self
        if self.is_trivial:
            return other
        suits = dict(self.suits)
        for s, iv in other.suits.items():
            suits[s] = _isect(suits.get(s), iv)  # type: ignore[assignment]
        evals = dict(self.evals)
        for k, iv in other.evals.items():
            evals[k] = _isect(evals.get(k), iv)  # type: ignore[assignment]
        extra_all = list(self.all_of) + list(other.all_of)
        # any_of / not from both sides can't merge field-wise; push into all_of
        for c in (self, other):
            pass
        wrapped = []
        if self.any_of:
            wrapped.append(HandConstraint(any_of=self.any_of))
        if other.any_of:
            wrapped.append(HandConstraint(any_of=other.any_of))
        if self.not_ is not None:
            wrapped.append(HandConstraint(not_=self.not_))
        if other.not_ is not None:
            wrapped.append(HandConstraint(not_=other.not_))
        return HandConstraint(
            hcp=_isect(self.hcp, other.hcp),
            suits=suits,
            evals=evals,
            features=tuple(dict.fromkeys(self.features + other.features)),
            shapes=tuple(set(self.shapes) & set(other.shapes)) if (self.shapes and other.shapes) else (self.shapes or other.shapes),
            any_of=(),
            all_of=tuple(extra_all + wrapped),
            not_=None,
        )

    def negate(self) -> "HandConstraint":
        """Logical negation. Satisfaction treats the inner conjunction correctly
        as a disjunction of complements (De Morgan) via `not_` semantics."""
        if self.not_ is not None and self.is_trivial_except_not():
            return self.not_
        return HandConstraint(not_=self)

    def is_trivial_except_not(self) -> bool:
        return not (self.hcp or self.suits or self.evals or self.features or self.shapes or self.any_of or self.all_of)

    # ------------------------------------------------------------- summary
    def box(self) -> Box:
        """Coarse bounding box: sound over-approximation of satisfying hands."""
        suits = {s: (float(iv[0]), float(iv[1])) for s, iv in self.suits.items() if iv is not None}
        hcp = tuple(map(float, self.hcp)) if self.hcp else FULL_HCP
        # derive suit bounds from shapes
        if self.shapes:
            sh_box: Box | None = None
            for pat in self.shapes:
                exact, lens = _parse_shape(pat)
                if exact:
                    b = Box(suits={s: (float(l), float(l)) for s, l in zip(SUITS, lens)})
                else:
                    b = Box(suits={s: (float(lens[-1]), float(lens[0])) for s in SUITS})
                sh_box = b if sh_box is None else sh_box.hull(b)
            base = Box(hcp=hcp, suits=suits).intersect(sh_box)  # type: ignore[arg-type]
        else:
            base = Box(hcp=hcp, suits=suits)
        # well-known evaluator specs contribute to the box
        for spec, iv in self.evals.items():
            if spec == "hcp":
                base = base.intersect(Box(hcp=(float(iv[0]), float(iv[1]))))
            elif spec.startswith("suit_length(") and spec.endswith(")"):
                arg = spec[len("suit_length("):-1].strip()
                if arg in SUITS:
                    base = base.intersect(Box(suits={arg: (float(iv[0]), float(iv[1]))}))
            elif spec in ("balanced",) and iv[0] >= 1:
                base = base.intersect(Box(suits={s: (2.0, 5.0) for s in SUITS}))
            elif spec in ("semi_balanced",) and iv[0] >= 1:
                base = base.intersect(Box(suits={s: (2.0, 6.0) for s in SUITS}))
        for c in self.all_of:
            base = base.intersect(c.box())
        if self.any_of:
            union: Box | None = None
            for c in self.any_of:
                union = c.box() if union is None else union.hull(c.box())
            if union is not None:
                base = base.intersect(union)
        if self.not_ is not None:
            base = base.intersect(self.not_._complement_box())
        return base

    def _complement_box(self) -> Box:
        """Bounding box of the complement.  Only informative when the negated
        constraint binds a single simple interval field (then the complement
        is a disjunction of at most two intervals whose hull may still bind
        one side).  Otherwise the full box (sound over-approximation)."""
        bound_fields: list[tuple[str, str | None, Interval]] = []
        if self.hcp:
            bound_fields.append(("hcp", None, self.hcp))
        for s, iv in self.suits.items():
            bound_fields.append(("suit", s, iv))
        if self.evals or self.features or self.shapes or self.any_of or self.all_of or self.not_:
            return Box()
        if len(bound_fields) != 1:
            return Box()
        kind, suit, (lo, hi) = bound_fields[0]
        full = FULL_HCP if kind == "hcp" else FULL_SUIT
        below: Interval | None = (full[0], lo - 1) if lo > full[0] else None
        above: Interval | None = (hi + 1, full[1]) if hi < full[1] else None
        if below and above:
            return Box()  # hull of both sides = everything
        iv = below or above
        if iv is None:
            return Box(hcp=(1.0, 0.0)) if kind == "hcp" else Box(suits={suit: (1.0, 0.0)})  # empty
        if kind == "hcp":
            return Box(hcp=iv)
        return Box(suits={suit: iv})

    def describe(self) -> str:
        """Short human-readable rendering (for explanations)."""
        bits: list[str] = []
        if self.hcp:
            lo, hi = self.hcp
            bits.append(f"{int(lo)}-{int(hi)} HCP" if hi < 38 else f"{int(lo)}+ HCP")
        for s, iv in self.suits.items():
            lo, hi = iv
            if lo == hi:
                bits.append(f"exactly {int(lo)} {s}")
            elif hi >= 13:
                bits.append(f"{int(lo)}+ {s}")
            else:
                bits.append(f"{int(lo)}-{int(hi)} {s}")
        for spec, iv in self.evals.items():
            bits.append(f"{spec} in [{iv[0]}, {iv[1]}]")
        bits.extend(self.features)
        if self.shapes:
            bits.append("shape " + "/".join(self.shapes))
        if self.any_of:
            bits.append("(" + " or ".join(c.describe() for c in self.any_of) + ")")
        for c in self.all_of:
            bits.append(c.describe())
        if self.not_:
            bits.append("not(" + self.not_.describe() + ")")
        return ", ".join(b for b in bits if b) or "any hand"
