"""Unit tests: constraint satisfaction, soft fit, intersection, negation, boxes."""

import pytest

from bridgebidder.constraints.model import Box, HandConstraint
from bridgebidder.domain.cards import Hand

H = Hand.parse
C = HandConstraint.from_dict


def test_satisfaction_simple():
    c = C({"hcp": [12, 21], "suits": {"S": [5, 13]}})
    assert c.satisfied(H("AQ752.K42.QJ9.87"))          # 12 hcp 5 spades
    assert not c.satisfied(H("AQ752.842.Q92.87"))      # 9 hcp
    assert not c.satisfied(H("AQ72.K642.Q92.87"))      # 4 spades


def test_satisfaction_features_shapes():
    c = C({"features": ["stopper(H)"], "shapes": ["5332"]})
    assert c.satisfied(H("AQ752.K42.Q92.87"))
    assert not c.satisfied(H("AQ752.842.Q92.87"))      # no heart stopper
    c2 = C({"shapes": ["5=3=3=2"]})
    assert c2.satisfied(H("AQ752.K42.Q92.87"))
    assert not c2.satisfied(H("K42.AQ752.Q92.87"))     # 3=5=3=2 exact mismatch


def test_any_of_and_not():
    c = C({"any_of": [{"hcp": [15, 17]}, {"suits": {"S": [6, 13]}}]})
    assert c.satisfied(H("AQ7532.842.Q9.87"))          # 6 spades, 8 hcp
    assert c.satisfied(H("AQ75.KJ2.Q92.K87"))          # 15 hcp
    assert not c.satisfied(H("AQ752.842.Q92.87"))
    n = C({"not": {"hcp": [12, 40]}})
    assert n.satisfied(H("AQ752.842.Q92.87"))          # 9 hcp
    assert not n.satisfied(H("AQ75.K42.Q92.K87"))


def test_negation_is_disjunction():
    # not(hcp 12-21 AND 3 spades exactly): satisfied by breaking EITHER conjunct
    c = C({"hcp": [12, 21], "suits": {"S": [3, 3]}}).negate()
    assert c.satisfied(H("AQ7.K42.QJ2.8732")) is False  # 12 hcp AND 3 spades
    assert c.satisfied(H("Q75.842.Q92.8732"))           # weak (hcp broken)
    assert c.satisfied(H("AQ75.K42.QJ2.873"))           # 4 spades (length broken)


def test_double_negation():
    c = C({"hcp": [12, 21]})
    assert c.negate().negate().satisfied(H("AQ75.K42.Q92.K87"))


def test_fit_soft_boundaries():
    c = C({"hcp": [12, 21]})
    h11 = H("AQ75.K42.Q92.T87")  # 11 hcp
    assert c.fit(H("AQ75.K42.Q92.K87")) == 1.0
    assert 0.75 <= c.fit(h11) <= 0.85          # ~0.8 one point out (mission spec)
    assert c.fit(H("QT75.842.Q92.J87")) < 0.1  # 5 hcp: way out


def test_fit_suit_length_sharper_than_hcp():
    hand = H("AQ75.K42.Q92.K87")  # 15 hcp, 4 spades
    hcp_miss = C({"hcp": [16, 18]}).fit(hand)
    suit_miss = C({"suits": {"S": [5, 13]}}).fit(hand)
    assert suit_miss < hcp_miss


def test_fit_any_of_takes_best_branch():
    c = C({"any_of": [{"hcp": [12, 21]}, {"hcp": [10, 21], "evals": {"rule_of_20": [20, 33]}}]})
    # 10 hcp, 5-5: rule of 20 passes -> full fit through the second branch
    assert c.fit(H("AQ752.KJ642.4.32")) == 1.0
    # 11 hcp, 5-3: rule of 20 one short -> partial fit only
    f = c.fit(H("AQJ52.KJ6.842.32"))
    assert 0.5 < f < 1.0


def test_intersection():
    a = C({"hcp": [12, 21], "suits": {"S": [5, 13]}})
    b = C({"hcp": [15, 40], "suits": {"H": [3, 13]}})
    i = a.intersect(b)
    assert i.satisfied(H("AQ752.K42.A92.A7"))       # 17 hcp 5S 3H
    assert not i.satisfied(H("AQ752.K42.Q92.87"))   # 12 hcp < 15
    box = i.box()
    assert box.hcp == (15.0, 21.0)
    assert box.suit("S") == (5.0, 13.0)


def test_intersection_preserves_combinators():
    a = C({"any_of": [{"hcp": [15, 17]}, {"hcp": [20, 21]}]})
    b = C({"suits": {"S": [4, 13]}})
    i = a.intersect(b)
    assert i.satisfied(H("AQ75.KJ2.Q92.K87"))       # 15 hcp 4S
    assert not i.satisfied(H("AQ75.K42.QJ2.J87"))   # 13 hcp (gap)
    assert not i.satisfied(H("AQ7.K42.Q92.K873"))   # 3 spades


def test_box_summaries():
    c = C({"hcp": [12, 21], "suits": {"S": [5, 13]}})
    b = c.box()
    assert b.hcp == (12.0, 21.0)
    assert b.suit("S") == (5.0, 13.0)
    assert b.suit("H") == (0.0, 13.0)


def test_box_any_of_hull():
    c = C({"any_of": [{"hcp": [6, 9]}, {"hcp": [12, 14]}]})
    assert c.box().hcp == (6.0, 14.0)


def test_box_negation_one_sided():
    c = C({"not": {"hcp": [12, 40]}})
    assert c.box().hcp == (0.0, 11.0)
    c2 = C({"not": {"suits": {"S": [4, 13]}}})
    assert c2.box().suit("S") == (0.0, 3.0)
    # multi-field negation: complement box must stay the full box (sound)
    c3 = C({"not": {"hcp": [12, 21], "suits": {"S": [3, 3]}}})
    assert c3.box().hcp == (0.0, 40.0)
    assert c3.box().suit("S") == (0.0, 13.0)


def test_box_from_shapes_and_balanced():
    c = C({"shapes": ["5=3=3=2"]})
    assert c.box().suit("S") == (5.0, 5.0)
    b = C({"balanced": True}).box()
    assert b.suit("S") == (2.0, 5.0)


def test_box_empty_detection():
    assert Box(hcp=(5.0, 3.0)).is_empty
    assert Box(suits={"S": (7.0, 13.0), "H": (7.0, 13.0)}).is_empty  # >13 cards
    assert not Box().is_empty


def test_box_accepts():
    b = Box(hcp=(12.0, 21.0), suits={"S": (5.0, 13.0)})
    assert b.accepts(H("AQ752.K42.QJ9.87"))
    assert not b.accepts(H("AQ75.K42.Q92.873"))


def test_from_dict_rejects_unknown_keys():
    with pytest.raises(ValueError):
        C({"hpc": [12, 21]})
    with pytest.raises(ValueError):
        C({"suits": {"Z": [1, 2]}})


def test_to_dict_roundtrip():
    d = {"hcp": [12, 21], "suits": {"S": [5, 13]}, "features": ["stopper(H)"],
         "not": {"hcp": [20, 40]}}
    assert C(C(d).to_dict()).satisfied(H("AQ752.K42.QJ9.87"))


def test_describe():
    txt = C({"hcp": [12, 21], "suits": {"S": [5, 13]}}).describe()
    assert "12-21 HCP" in txt and "5+ S" in txt
