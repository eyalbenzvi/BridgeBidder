"""The auction: legality, turn tracking, contract determination."""

from __future__ import annotations

from dataclasses import dataclass, field
from functools import cached_property

from .calls import ALL_BIDS, Call, DOUBLE, PASS, REDOUBLE
from .types import Seat, Vulnerability


@dataclass(frozen=True)
class Contract:
    level: int
    strain: str
    declarer: Seat
    doubled: int  # 0 = undoubled, 1 = doubled, 2 = redoubled

    def __str__(self) -> str:
        return f"{self.level}{self.strain}{'X' * self.doubled} by {self.declarer.value}"


@dataclass
class Auction:
    """An auction in progress (or complete)."""

    dealer: Seat
    vulnerability: Vulnerability = Vulnerability.NONE
    calls: list[Call] = field(default_factory=list)

    # ----- construction helpers -----
    @staticmethod
    def from_strings(dealer: str | Seat, calls: list[str], vulnerability: str | Vulnerability = "None") -> "Auction":
        d = dealer if isinstance(dealer, Seat) else Seat(dealer)
        v = vulnerability if isinstance(vulnerability, Vulnerability) else Vulnerability.parse(vulnerability)
        a = Auction(dealer=d, vulnerability=v)
        for c in calls:
            a.add(Call.parse(c))
        return a

    def copy(self) -> "Auction":
        return Auction(dealer=self.dealer, vulnerability=self.vulnerability, calls=list(self.calls))

    # ----- turn / seats -----
    def seat_of_call(self, i: int) -> Seat:
        return Seat.from_index(self.dealer.index + i)

    @property
    def next_seat(self) -> Seat:
        return self.seat_of_call(len(self.calls))

    def calls_by(self, seat: Seat) -> list[Call]:
        return [c for i, c in enumerate(self.calls) if self.seat_of_call(i) == seat]

    # ----- state -----
    @property
    def is_complete(self) -> bool:
        n = len(self.calls)
        if n >= 4 and all(c.is_pass for c in self.calls) and n == 4:
            return True
        if n >= 4 and any(not c.is_pass for c in self.calls):
            return all(c.is_pass for c in self.calls[-3:])
        return False

    @property
    def last_bid_info(self) -> tuple[Call, int] | None:
        """(last contract bid, its index) or None."""
        for i in range(len(self.calls) - 1, -1, -1):
            if self.calls[i].is_bid:
                return self.calls[i], i
        return None

    @property
    def last_bid(self) -> Call | None:
        info = self.last_bid_info
        return info[0] if info else None

    @property
    def doubled_state(self) -> int:
        """0/1/2 = current bid undoubled/doubled/redoubled. 0 if no bid."""
        state = 0
        for c in reversed(self.calls):
            if c.is_bid:
                break
            if c.kind == "double":
                state = max(state, 1)
            elif c.kind == "redouble":
                state = 2
        return state if self.last_bid is not None else 0

    def opener_index(self) -> int | None:
        """Index of the first non-pass call (the opening bid), or None."""
        for i, c in enumerate(self.calls):
            if c.is_bid:
                return i
        return None

    @property
    def opening_seat_number(self) -> int:
        """1-based seat position of the *next* caller if nobody has bid yet.

        Only meaningful before an opening: equals number of leading passes + 1.
        """
        return len(self.calls) + 1

    def is_passed_hand(self, seat: Seat) -> bool:
        """True if `seat` passed at its first turn(s) before its side's first bid."""
        opener = self.opener_index()
        limit = opener if opener is not None else len(self.calls)
        for i in range(limit):
            if self.seat_of_call(i) == seat and self.calls[i].is_pass:
                return True
        return False

    # ----- legality -----
    def is_legal(self, call: Call) -> bool:
        if self.is_complete:
            return False
        if call.is_pass:
            return True
        lb = self.last_bid_info
        if call.is_bid:
            return lb is None or call.bid_index > lb[0].bid_index
        # double / redouble
        if lb is None:
            return False
        bid_seat = self.seat_of_call(lb[1])
        me = self.next_seat
        state = self.doubled_state
        if call.kind == "double":
            return state == 0 and not me.same_side(bid_seat)
        if call.kind == "redouble":
            return state == 1 and me.same_side(bid_seat)
        return False

    def legal_calls(self) -> list[Call]:
        if self.is_complete:
            return []
        out = [c for c in (PASS, DOUBLE, REDOUBLE) if self.is_legal(c)]
        lb = self.last_bid
        floor = -1 if lb is None else lb.bid_index
        out.extend(b for b in ALL_BIDS if b.bid_index > floor)
        return out

    def add(self, call: Call) -> None:
        if not self.is_legal(call):
            raise ValueError(f"Illegal call {call} after {self}")
        self.calls.append(call)

    def child(self, call: Call) -> "Auction":
        a = self.copy()
        a.add(call)
        return a

    # ----- final contract -----
    @property
    def contract(self) -> Contract | None:
        if not self.is_complete:
            return None
        info = self.last_bid_info
        if info is None:
            return None  # passed out
        bid, idx = info
        declarer_side_seat = self.seat_of_call(idx)
        # declarer = first player of that side to have bid this strain
        for i, c in enumerate(self.calls):
            if c.is_bid and c.strain == bid.strain and self.seat_of_call(i).same_side(declarer_side_seat):
                return Contract(level=bid.level, strain=bid.strain, declarer=self.seat_of_call(i), doubled=self.doubled_state)
        return None

    # ----- misc -----
    def non_pass_calls(self) -> list[tuple[int, Call]]:
        return [(i, c) for i, c in enumerate(self.calls) if not c.is_pass]

    @property
    def is_competitive(self) -> bool:
        """True if both sides have made a non-pass call."""
        sides = {self.seat_of_call(i).side for i, c in enumerate(self.calls) if not c.is_pass}
        return len(sides) > 1

    def __str__(self) -> str:
        return f"[{self.dealer.value}] " + " - ".join(str(c) for c in self.calls)

    def key(self) -> tuple:
        return (self.dealer, tuple(str(c) for c in self.calls))
