"""Basic bridge table types: seats and vulnerability."""

from __future__ import annotations

from enum import Enum


class Seat(str, Enum):
    N = "N"
    E = "E"
    S = "S"
    W = "W"

    @property
    def index(self) -> int:
        return "NESW".index(self.value)

    @staticmethod
    def from_index(i: int) -> "Seat":
        return Seat("NESW"[i % 4])

    @property
    def partner(self) -> "Seat":
        return Seat.from_index(self.index + 2)

    @property
    def lho(self) -> "Seat":
        return Seat.from_index(self.index + 1)

    @property
    def rho(self) -> "Seat":
        return Seat.from_index(self.index + 3)

    @property
    def side(self) -> str:
        """'NS' or 'EW'."""
        return "NS" if self in (Seat.N, Seat.S) else "EW"

    def same_side(self, other: "Seat") -> bool:
        return self.side == other.side


class Vulnerability(str, Enum):
    NONE = "None"
    NS = "NS"
    EW = "EW"
    BOTH = "Both"

    @staticmethod
    def parse(s: str) -> "Vulnerability":
        key = s.strip().lower()
        aliases = {
            "none": Vulnerability.NONE,
            "-": Vulnerability.NONE,
            "love": Vulnerability.NONE,
            "ns": Vulnerability.NS,
            "n-s": Vulnerability.NS,
            "ew": Vulnerability.EW,
            "e-w": Vulnerability.EW,
            "both": Vulnerability.BOTH,
            "all": Vulnerability.BOTH,
        }
        if key not in aliases:
            raise ValueError(f"Unknown vulnerability: {s!r}")
        return aliases[key]

    def is_vulnerable(self, seat: Seat) -> bool:
        if self is Vulnerability.BOTH:
            return True
        if self is Vulnerability.NONE:
            return False
        return seat.side == self.value
