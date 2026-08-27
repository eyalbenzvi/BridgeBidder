"""Cards and hands.

Hand string format: "AQ52.KJ4.T92.873" = Spades.Hearts.Diamonds.Clubs.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from functools import cached_property

SUITS = "SHDC"  # display / parse order
RANK_CHARS = "23456789TJQKA"
RANKS = {ch: i + 2 for i, ch in enumerate(RANK_CHARS)}  # '2'->2 ... 'A'->14
RANK_NAMES = {v: k for k, v in RANKS.items()}

HCP_BY_RANK = {14: 4, 13: 3, 12: 2, 11: 1}


@dataclass(frozen=True, order=True)
class Card:
    suit: str  # one of "SHDC"
    rank: int  # 2..14

    def __post_init__(self) -> None:
        if self.suit not in SUITS:
            raise ValueError(f"Bad suit {self.suit!r}")
        if not 2 <= self.rank <= 14:
            raise ValueError(f"Bad rank {self.rank!r}")

    def __str__(self) -> str:
        return f"{self.suit}{RANK_NAMES[self.rank]}"

    @staticmethod
    def parse(s: str) -> "Card":
        s = s.strip().upper().replace("10", "T")
        if len(s) != 2:
            raise ValueError(f"Bad card {s!r}")
        return Card(suit=s[0], rank=RANKS[s[1]])


FULL_DECK: tuple[Card, ...] = tuple(
    Card(suit=s, rank=r) for s in SUITS for r in range(2, 15)
)


class Hand:
    """An immutable 13-card bridge hand."""

    __slots__ = ("cards", "_suit_ranks", "__dict__")

    def __init__(self, cards) -> None:
        cards = tuple(sorted(cards, key=lambda c: (SUITS.index(c.suit), -c.rank)))
        if len(cards) != 13:
            raise ValueError(f"A hand must have 13 cards, got {len(cards)}")
        if len(set(cards)) != 13:
            raise ValueError("Duplicate cards in hand")
        object.__setattr__(self, "cards", cards)
        suit_ranks: dict[str, tuple[int, ...]] = {}
        for s in SUITS:
            suit_ranks[s] = tuple(sorted((c.rank for c in cards if c.suit == s), reverse=True))
        object.__setattr__(self, "_suit_ranks", suit_ranks)

    @staticmethod
    def parse(s: str) -> "Hand":
        """Parse "AQ52.KJ4.T92.873" (S.H.D.C). '-' or '' allowed for a void."""
        parts = s.strip().upper().replace("10", "T").split(".")
        if len(parts) != 4:
            raise ValueError(f"Hand must have 4 dot-separated suits, got {s!r}")
        cards = []
        for suit, holding in zip(SUITS, parts):
            holding = holding.strip()
            if holding == "-":
                holding = ""
            for ch in holding:
                if ch not in RANKS:
                    raise ValueError(f"Bad rank char {ch!r} in {s!r}")
                cards.append(Card(suit=suit, rank=RANKS[ch]))
        return Hand(cards)

    def suit_ranks(self, suit: str) -> tuple[int, ...]:
        """Ranks held in `suit`, descending."""
        return self._suit_ranks[suit]

    def suit_length(self, suit: str) -> int:
        return len(self._suit_ranks[suit])

    @cached_property
    def lengths(self) -> dict[str, int]:
        return {s: len(self._suit_ranks[s]) for s in SUITS}

    @cached_property
    def shape(self) -> tuple[int, ...]:
        """Sorted suit lengths, descending. e.g. (5, 3, 3, 2)."""
        return tuple(sorted(self.lengths.values(), reverse=True))

    @cached_property
    def exact_shape(self) -> tuple[int, int, int, int]:
        """Lengths in S,H,D,C order."""
        return tuple(self.lengths[s] for s in SUITS)  # type: ignore[return-value]

    @cached_property
    def hcp(self) -> int:
        return sum(HCP_BY_RANK.get(c.rank, 0) for c in self.cards)

    def suit_hcp(self, suit: str) -> int:
        return sum(HCP_BY_RANK.get(r, 0) for r in self._suit_ranks[suit])

    def __str__(self) -> str:
        return ".".join(
            "".join(RANK_NAMES[r] for r in self._suit_ranks[s]) for s in SUITS
        )

    def __repr__(self) -> str:
        return f"Hand({str(self)!r})"

    def __eq__(self, other) -> bool:
        return isinstance(other, Hand) and self.cards == other.cards

    def __hash__(self) -> int:
        return hash(self.cards)


def deal_remaining(my_hand: Hand, rng: random.Random) -> list[list[Card]]:
    """Randomly split the 39 cards not in my_hand into three 13-card hands."""
    remaining = [c for c in FULL_DECK if c not in set(my_hand.cards)]
    rng.shuffle(remaining)
    return [remaining[0:13], remaining[13:26], remaining[26:39]]
