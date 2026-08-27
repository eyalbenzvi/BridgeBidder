"""Double-dummy evaluation behind a swappable interface.

EndplayDD uses Bo Haglund's DDS (via the `endplay` package).  HeuristicDD is
a clearly-isolated fallback estimating tricks from HCP + fit + shape so the
whole pipeline works without the native solver.
"""

from __future__ import annotations

from typing import Protocol

from ..domain.cards import Hand, SUITS
from ..domain.types import Seat

DealMap = dict[Seat, Hand]


class DDEvaluator(Protocol):
    name: str

    def tricks(self, deal: DealMap, declarer: Seat, strain: str) -> int:
        """Double-dummy tricks for declarer in the given strain."""
        ...


def _deal_key(deal: DealMap) -> tuple:
    return tuple(str(deal[s]) for s in Seat)


class EndplayDD:
    """Real DDS.  Computes the full 20-entry DD table per deal and caches it."""

    name = "endplay-dds"

    def __init__(self, cache_size: int = 4096) -> None:
        from endplay.types import Deal, Denom, Player  # noqa: F401 (import check)

        self._cache: dict[tuple, dict] = {}
        self._cache_size = cache_size

    @staticmethod
    def _pbn(deal: DealMap) -> str:
        return "N:" + " ".join(str(deal[s]) for s in (Seat.N, Seat.E, Seat.S, Seat.W))

    def _store(self, key: tuple, table) -> dict:
        from endplay.types import Denom, Player

        denoms = {"C": Denom.clubs, "D": Denom.diamonds, "H": Denom.hearts,
                  "S": Denom.spades, "NT": Denom.nt}
        players = {Seat.N: Player.north, Seat.E: Player.east,
                   Seat.S: Player.south, Seat.W: Player.west}
        out = {
            (seat, strain): int(table[denom, player])
            for seat, player in players.items()
            for strain, denom in denoms.items()
        }
        if len(self._cache) >= self._cache_size:
            self._cache.clear()
        self._cache[key] = out
        return out

    def prefetch(self, deals: list[DealMap]) -> None:
        """Batch-compute DD tables (DDS multithreads across boards)."""
        from endplay.dds import calc_all_tables
        from endplay.types import Deal

        todo = [(d, _deal_key(d)) for d in deals]
        todo = [(d, k) for d, k in todo if k not in self._cache]
        if not todo:
            return
        tables = calc_all_tables([Deal(self._pbn(d)) for d, _ in todo])
        for (d, k), table in zip(todo, tables):
            self._store(k, table)

    def _table(self, deal: DealMap) -> dict:
        key = _deal_key(deal)
        hit = self._cache.get(key)
        if hit is not None:
            return hit
        from endplay.dds import calc_dd_table
        from endplay.types import Deal

        return self._store(key, calc_dd_table(Deal(self._pbn(deal))))

    def tricks(self, deal: DealMap, declarer: Seat, strain: str) -> int:
        return self._table(deal)[(declarer, strain)]


class HeuristicDD:
    """Trick estimator: combined HCP + fit + shortness, no card play.

    Deliberately simple; only used when the DDS library is unavailable, and
    for tests that must not depend on the native solver.
    """

    name = "heuristic"

    def tricks(self, deal: DealMap, declarer: Seat, strain: str) -> int:
        decl, dummy = deal[declarer], deal[declarer.partner]
        hcp = decl.hcp + dummy.hcp
        # baseline: 26 combined HCP ~ 9-10 tricks in a fit / 9 in NT
        tricks = 3.0 + hcp * 0.25
        if strain != "NT":
            fit = decl.suit_length(strain) + dummy.suit_length(strain)
            tricks += max(0, fit - 7) * 0.7
            if fit >= 8:
                for h in (decl, dummy):
                    for s in SUITS:
                        if s != strain:
                            n = h.suit_length(s)
                            if n == 0:
                                tricks += 1.0
                            elif n == 1:
                                tricks += 0.5
            else:
                tricks -= (7 - fit) * 0.6
        else:
            # NT: long-suit tricks help a little
            longest = max(decl.suit_length(s) + dummy.suit_length(s) for s in SUITS)
            tricks += max(0, longest - 7) * 0.4
        return max(0, min(13, round(tricks)))


_DD: DDEvaluator | None = None


def get_dd() -> DDEvaluator:
    """The best available evaluator (module-level singleton)."""
    global _DD
    if _DD is None:
        try:
            _DD = EndplayDD()
        except Exception:  # pragma: no cover - endplay is installed in CI
            _DD = HeuristicDD()
    return _DD


def set_dd(evaluator: DDEvaluator) -> None:
    """Swap the evaluator (tests / future engines)."""
    global _DD
    _DD = evaluator
