"""Unit tests: cards, hands, calls, auction legality."""

import pytest

from bridgebidder.domain.auction import Auction
from bridgebidder.domain.calls import Call, PASS, DOUBLE, REDOUBLE
from bridgebidder.domain.cards import Card, Hand
from bridgebidder.domain.types import Seat, Vulnerability


# ---------------------------------------------------------------- cards/hands

def test_hand_parse_roundtrip():
    h = Hand.parse("AQ52.KJ4.T92.873")
    assert str(h) == "AQ52.KJ4.T92.873"
    assert h.hcp == 4 + 2 + 3 + 1  # A Q K J
    assert h.suit_length("S") == 4
    assert h.exact_shape == (4, 3, 3, 3)
    assert h.shape == (4, 3, 3, 3)


def test_hand_parse_void_and_ten():
    h = Hand.parse("AKQJT98765432..-.")
    assert h.suit_length("S") == 13
    assert h.suit_length("H") == 0
    assert h.suit_length("D") == 0
    assert h.suit_length("C") == 0


def test_hand_wrong_count_rejected():
    with pytest.raises(ValueError):
        Hand.parse("AQ52.KJ4.T92.87")  # 12 cards
    with pytest.raises(ValueError):
        Hand.parse("AQ52.KJ4.T92.8732")  # 14 cards


def test_hand_duplicate_rejected():
    with pytest.raises(ValueError):
        Hand.parse("AA52.KJ4.T92.873")


def test_card_parse():
    assert Card.parse("SA") == Card(suit="S", rank=14)
    assert Card.parse("c2") == Card(suit="C", rank=2)
    with pytest.raises((ValueError, KeyError)):
        Card.parse("Z5")


def test_suit_hcp():
    h = Hand.parse("AQ52.KJ4.T92.873")
    assert h.suit_hcp("S") == 6
    assert h.suit_hcp("H") == 4
    assert h.suit_hcp("D") == 0


# ------------------------------------------------------------------- calls

def test_call_parse_variants():
    assert str(Call.parse("p")) == "P"
    assert str(Call.parse("PASS")) == "P"
    assert str(Call.parse("x")) == "X"
    assert str(Call.parse("XX")) == "XX"
    assert str(Call.parse("1n")) == "1NT"
    assert str(Call.parse("7NT")) == "7NT"
    assert Call.parse("2H").bid_index == 5 + 2


def test_call_bad():
    with pytest.raises(ValueError):
        Call.parse("8C")
    with pytest.raises(ValueError):
        Call.parse("1Z")


# ------------------------------------------------------------------- seats

def test_seat_relations():
    assert Seat.N.partner == Seat.S
    assert Seat.N.lho == Seat.E
    assert Seat.N.rho == Seat.W
    assert Seat.E.side == "EW"
    assert Seat.N.same_side(Seat.S)
    assert not Seat.N.same_side(Seat.E)


def test_vulnerability():
    assert Vulnerability.parse("ns").is_vulnerable(Seat.S)
    assert not Vulnerability.parse("ns").is_vulnerable(Seat.E)
    assert Vulnerability.parse("both").is_vulnerable(Seat.W)
    assert not Vulnerability.parse("none").is_vulnerable(Seat.N)


# ------------------------------------------------------------------ auction

def test_auction_turn_tracking():
    a = Auction.from_strings("E", ["P", "1H"])
    assert a.seat_of_call(0) == Seat.E
    assert a.next_seat == Seat.W


def test_auction_bid_must_be_higher():
    a = Auction.from_strings("N", ["1H"])
    assert not a.is_legal(Call.parse("1H"))
    assert not a.is_legal(Call.parse("1C"))
    assert a.is_legal(Call.parse("1S"))
    assert a.is_legal(Call.parse("2C"))


def test_auction_double_legality():
    a = Auction.from_strings("N", ["1H"])
    assert a.is_legal(DOUBLE)          # E can double N's bid
    assert not a.is_legal(REDOUBLE)
    a.add(DOUBLE)
    assert not a.is_legal(DOUBLE)      # S cannot re-double opponents' double
    assert a.is_legal(REDOUBLE)        # S can redouble
    a.add(PASS)
    assert not a.is_legal(REDOUBLE)    # W: partner's bid was doubled, but W is opponent? no:
    # W is the doubler's partner; the doubled bid belongs to NS, so W cannot redouble


def test_auction_double_own_side_illegal():
    a = Auction.from_strings("N", ["1H", "P"])
    assert not a.is_legal(DOUBLE)  # S cannot double partner


def test_auction_completion_passout():
    a = Auction.from_strings("N", ["P", "P", "P", "P"])
    assert a.is_complete
    assert a.contract is None
    assert a.legal_calls() == []


def test_auction_completion_after_bid():
    a = Auction.from_strings("N", ["1NT", "P", "P"])
    assert not a.is_complete
    a.add(PASS)
    assert a.is_complete
    c = a.contract
    assert c.level == 1 and c.strain == "NT" and c.declarer == Seat.N


def test_declarer_first_of_side_to_name_strain():
    # N opens 1NT, S raises: declarer is N (first to bid NT)
    a = Auction.from_strings("N", ["1NT", "P", "3NT", "P", "P", "P"])
    assert a.contract.declarer == Seat.N
    # transfer-ish: S names hearts first even though N bids them last
    a2 = Auction.from_strings("N", ["1H", "P", "4H", "P", "P", "P"])
    assert a2.contract.declarer == Seat.N


def test_doubled_contract():
    a = Auction.from_strings("N", ["4S", "X", "P", "P", "P"])
    assert a.contract.doubled == 1
    a = Auction.from_strings("N", ["4S", "X", "XX", "P", "P", "P"])
    assert a.contract.doubled == 2


def test_passed_hand_detection():
    a = Auction.from_strings("N", ["P", "P", "1H", "P"])
    assert a.is_passed_hand(Seat.N)
    assert a.is_passed_hand(Seat.E)
    assert not a.is_passed_hand(Seat.S)
    assert not a.is_passed_hand(Seat.W)


def test_competitive_detection():
    assert not Auction.from_strings("N", ["1H", "P", "2H"]).is_competitive
    assert Auction.from_strings("N", ["1H", "2C"]).is_competitive


def test_illegal_call_raises():
    a = Auction.from_strings("N", ["1H"])
    with pytest.raises(ValueError):
        a.add(Call.parse("1C"))
