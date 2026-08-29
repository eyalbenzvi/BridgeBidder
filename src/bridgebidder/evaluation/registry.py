"""Pluggable hand-evaluator registry.

Evaluators are pure functions (hand, ctx, *args) -> float.  DSL rules reference
them by name; parameterized specs look like "suit_quality(H)".  Registering a
new evaluator requires zero engine changes.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Callable

from ..domain.cards import Hand
from ..domain.types import Seat, Vulnerability


@dataclass
class EvalContext:
    """Auction-derived context available to evaluators.

    All fields are optional; evaluators must degrade gracefully when a field
    is missing.
    """

    seat: Seat | None = None
    vulnerability: Vulnerability = Vulnerability.NONE
    agreed_suit: str | None = None          # trump suit agreed by our side, if any
    partner_suits: list[str] = field(default_factory=list)   # suits partner has shown
    their_suits: list[str] = field(default_factory=list)     # suits opponents have shown
    opening_seat_number: int | None = None  # 1..4, only before any bid
    is_passed_hand: bool = False
    partner_min_hcp: float = 0.0
    partner_max_hcp: float = 40.0
    partner_min_points: float = 0.0   # partner's shown minimum TOTAL points
    partner_min_length: dict[str, int] = field(default_factory=dict)
    partner_max_length: dict[str, int] = field(default_factory=dict)
    standing_strain: str | None = None      # strain of the auction's standing bid

    # --- what the OPPONENTS have told us ------------------------------------
    # The inference engine has always maintained a full descriptor for each
    # opponent; none of it reached a rule, so the system could name "partner
    # has values" but never "they have values" - and a competitive auction is
    # exactly the one you cannot categorise without that.
    is_competitive: bool = False            # both sides have made a non-pass call
    their_shown_count: int = 0              # how many opponents have acted
    their_min_hcp: float = 0.0              # HCP the two of them have PROMISED
    their_min_length: dict[str, int] = field(default_factory=dict)
    their_max_fit: int = 0                  # longest combined fit they have shown

    @property
    def we_vulnerable(self) -> bool:
        return self.seat is not None and self.vulnerability.is_vulnerable(self.seat)

    @property
    def they_vulnerable(self) -> bool:
        return self.seat is not None and self.vulnerability.is_vulnerable(self.seat.lho)


REGISTRY: dict[str, Callable] = {}


def register_evaluator(name: str):
    def deco(fn: Callable):
        REGISTRY[name] = fn
        return fn

    return deco


def get_evaluator(name: str) -> Callable:
    if name not in REGISTRY:
        raise KeyError(f"Unknown evaluator {name!r}. Registered: {sorted(REGISTRY)}")
    return REGISTRY[name]


_SPEC_RE = re.compile(r"^(?P<name>[a-zA-Z_][\w]*)\s*(\((?P<args>[^)]*)\))?$")


def parse_spec(spec: str) -> tuple[str, tuple[str, ...]]:
    m = _SPEC_RE.match(spec.strip())
    if not m:
        raise ValueError(f"Bad evaluator spec {spec!r}")
    name = m.group("name")
    args_s = m.group("args")
    args = tuple(a.strip() for a in args_s.split(",")) if args_s else ()
    return name, args


def evaluate(spec: str, hand: Hand, ctx: EvalContext | None = None) -> float:
    """Evaluate a spec string like "hcp" or "suit_quality(H)" on a hand."""
    name, args = parse_spec(spec)
    fn = get_evaluator(name)
    return float(fn(hand, ctx or EvalContext(), *args))
