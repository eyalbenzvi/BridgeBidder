"""Calls: contract bids, Pass, Double, Redouble."""

from __future__ import annotations

from dataclasses import dataclass
from functools import total_ordering

STRAINS = ("C", "D", "H", "S", "NT")  # ascending rank within a level


class Strain:
    ORDER = {s: i for i, s in enumerate(STRAINS)}

    @staticmethod
    def is_valid(s: str) -> bool:
        return s in STRAINS


@dataclass(frozen=True)
@total_ordering
class Call:
    """A call. kind is 'bid' | 'pass' | 'double' | 'redouble'."""

    kind: str
    level: int | None = None  # 1..7 for bids
    strain: str | None = None  # C D H S NT for bids

    PASS_TOKENS = {"P", "PASS", "-"}
    DOUBLE_TOKENS = {"X", "DBL", "D", "DOUBLE"}
    REDOUBLE_TOKENS = {"XX", "RDBL", "RD", "REDOUBLE"}

    def __post_init__(self) -> None:
        if self.kind == "bid":
            if self.level is None or not 1 <= self.level <= 7:
                raise ValueError(f"Bad bid level {self.level!r}")
            if self.strain not in STRAINS:
                raise ValueError(f"Bad strain {self.strain!r}")
        elif self.kind in ("pass", "double", "redouble"):
            if self.level is not None or self.strain is not None:
                raise ValueError(f"{self.kind} takes no level/strain")
        else:
            raise ValueError(f"Bad call kind {self.kind!r}")

    # ----- constructors -----
    @staticmethod
    def parse(s: str) -> "Call":
        tok = s.strip().upper().replace("N.T.", "NT")
        if tok in Call.PASS_TOKENS:
            return PASS
        if tok in Call.REDOUBLE_TOKENS:
            return REDOUBLE
        if tok in Call.DOUBLE_TOKENS:
            return DOUBLE
        if len(tok) >= 2 and tok[0].isdigit():
            level = int(tok[0])
            strain = tok[1:]
            if strain == "N":
                strain = "NT"
            return Call(kind="bid", level=level, strain=strain)
        raise ValueError(f"Cannot parse call {s!r}")

    @staticmethod
    def bid(level: int, strain: str) -> "Call":
        return Call(kind="bid", level=level, strain=strain)

    # ----- properties -----
    @property
    def is_bid(self) -> bool:
        return self.kind == "bid"

    @property
    def is_pass(self) -> bool:
        return self.kind == "pass"

    @property
    def bid_index(self) -> int:
        """Total order of contract bids: 1C=0 ... 7NT=34."""
        assert self.is_bid
        return (self.level - 1) * 5 + Strain.ORDER[self.strain]  # type: ignore[operator]

    def __str__(self) -> str:
        if self.is_bid:
            return f"{self.level}{self.strain}"
        return {"pass": "P", "double": "X", "redouble": "XX"}[self.kind]

    def __repr__(self) -> str:
        return f"Call({str(self)!r})"

    def __lt__(self, other: "Call") -> bool:
        """Order used for sorting candidate calls; only meaningful for bids."""
        key = lambda c: (0, c.bid_index) if c.is_bid else (1, {"pass": 0, "double": 1, "redouble": 2}[c.kind])
        return key(self) < key(other)


PASS = Call(kind="pass")
DOUBLE = Call(kind="double")
REDOUBLE = Call(kind="redouble")

ALL_BIDS: tuple[Call, ...] = tuple(
    Call.bid(level, strain) for level in range(1, 8) for strain in STRAINS
)
