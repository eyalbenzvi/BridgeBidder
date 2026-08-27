"""Per-player hand descriptors accumulated during auction analysis."""

from __future__ import annotations

from dataclasses import dataclass, field

from ..constraints.model import Box, HandConstraint
from ..domain.cards import Hand, SUITS
from ..evaluation.registry import EvalContext


@dataclass
class HandDescriptor:
    """What we know about one player's hand.

    `strong` constraints are hard knowledge (enforced when testing sample
    deals); `soft` constraints are tendencies (negative inferences flagged
    soft in the system) used for scoring/bias but not for hard rejection.
    """

    strong: list[HandConstraint] = field(default_factory=list)
    soft: list[HandConstraint] = field(default_factory=list)
    shown_suits: list[str] = field(default_factory=list)  # chronological
    notes: list[str] = field(default_factory=list)
    _box: Box | None = None

    def apply(self, constraint: HandConstraint, weight: str = "strong", note: str | None = None) -> None:
        if constraint.is_trivial:
            if note:
                self.notes.append(note)
            return
        if weight == "strong":
            self.strong.append(constraint)
            self._box = None
        else:
            self.soft.append(constraint)
        if note:
            self.notes.append(note)
        # record newly shown suits (3+ promised covers better-minor openings)
        b = constraint.box()
        for s in SUITS:
            lo = b.suit(s)[0]
            if lo >= 3 and s not in self.shown_suits:
                self.shown_suits.append(s)

    @property
    def min_total_points(self) -> float:
        """Strongest lower bound on total points across hard knowledge."""
        return max((c.min_total_points() for c in self.strong), default=0.0)

    @property
    def box(self) -> Box:
        if self._box is None:
            b = Box()
            for c in self.strong:
                b = b.intersect(c.box())
            self._box = b
        return self._box

    def satisfied(self, hand: Hand, ctx: EvalContext | None = None) -> bool:
        """Hard-knowledge satisfaction (soft constraints ignored)."""
        return all(c.satisfied(hand, ctx) for c in self.strong)

    def fit(self, hand: Hand, ctx: EvalContext | None = None) -> float:
        f = 1.0
        for c in self.strong:
            f *= c.fit(hand, ctx)
        for c in self.soft:
            f *= 0.5 + 0.5 * c.fit(hand, ctx)
        return f

    def summary(self) -> dict:
        """Coarse public model: HCP range and suit-length ranges."""
        b = self.box
        return {
            "hcp": [b.hcp[0], b.hcp[1]],
            "suit_lengths": {s: [b.suit(s)[0], b.suit(s)[1]] for s in SUITS},
            "shown_suits": list(self.shown_suits),
        }

    def clone(self) -> "HandDescriptor":
        d = HandDescriptor(
            strong=list(self.strong),
            soft=list(self.soft),
            shown_suits=list(self.shown_suits),
            notes=list(self.notes),
        )
        d._box = self._box
        return d


@dataclass
class SideState:
    """Partnership-level auction state for one side (NS or EW)."""

    game_forced: bool = False
    agreed_suit: str | None = None
    asking: str | None = None            # active ask convention id (e.g. "keycards")
    asking_by: str | None = None         # seat value ("N"...) that asked
    last_forcing: str = "non_forcing"    # forcing status established by side's last call

    def clone(self) -> "SideState":
        return SideState(
            game_forced=self.game_forced,
            agreed_suit=self.agreed_suit,
            asking=self.asking,
            asking_by=self.asking_by,
            last_forcing=self.last_forcing,
        )
