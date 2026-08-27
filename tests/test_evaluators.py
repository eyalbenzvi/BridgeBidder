"""Unit tests: every registered evaluator against known-value fixtures."""

import pytest

from bridgebidder.domain.cards import Hand
from bridgebidder.domain.types import Seat, Vulnerability
from bridgebidder.evaluation import EvalContext, evaluate, register_evaluator, REGISTRY

H = Hand.parse


def ev(spec, hand, **ctx):
    return evaluate(spec, H(hand) if isinstance(hand, str) else hand, EvalContext(**ctx))


def test_hcp():
    assert ev("hcp", "AKQJ.AKQ.AKQ.AKQ") == 37
    assert ev("hcp", "5432.5432.543.32") == 0
    assert ev("hcp", "AQ52.KJ4.T92.873") == 10


def test_adjusted_hcp_stiff_honors():
    assert ev("adjusted_hcp", "K.QJ32.5432.5432") < ev("hcp", "K.QJ32.5432.5432")


def test_dist_points():
    assert ev("dist_points", "AKQJT9.432.32.32") == 2  # 6-card suit
    assert ev("dist_points", "5432.432.432.432") == 0


def test_shortness_points_with_trump_context():
    # agreed hearts; singleton spade (3) + doubleton club (1)
    assert ev("shortness_points", "5.KQ432.65432.32", agreed_suit="H") == 4


def test_total_points_support_aware():
    hand = "A.KQ432.5432.KQ2"
    plain = ev("total_points", hand)             # hcp 14 + 1 length = 15
    support = ev("total_points", hand, agreed_suit="H")  # hcp 14 + stiff spade 3 = 17
    assert plain == 15
    assert support == 17


def test_rule_of_20():
    assert ev("rule_of_20", "AQ752.K9642.4.32") == 9 + 5 + 5  # 19
    assert ev("rule_of_20", "AQJ75.KT642.4.32") == 20


def test_rule_of_15():
    assert ev("rule_of_15", "AQ752.K964.42.32") == 9 + 5


def test_rule_of_26_uses_partner_range():
    v = ev("rule_of_26", "AQ52.KJ42.T92.87", partner_min_hcp=12, partner_max_hcp=21)
    assert v == pytest.approx(10 + (12 + 16) / 2)


def test_ltc():
    # classic minimum opener ~7 losers
    assert ev("ltc", "AKQ32.432.432.32") == 0 + 3 + 3 + 2
    assert ev("ltc", "AKQJT98765432..-.") == 0
    assert ev("ltc", "5432.5432.543.32") == 3 + 3 + 3 + 2


def test_controls():
    assert ev("controls", "AK52.A42.K92.873") == 2 + 1 + 2 + 1


def test_quick_tricks():
    assert ev("quick_tricks", "AK52.AQ2.K92.873") == 2 + 1.5 + 0.5


def test_lott_total_trumps():
    v = ev("lott_total_trumps", "QT52.K42.K92.873",
           agreed_suit="S", partner_min_length={"S": 5})
    assert v == 9


def test_suit_length_and_diff():
    assert ev("suit_length(S)", "AQ752.K4.Q92.J87") == 5
    assert ev("suit_diff(S,H)", "AQ752.K4.Q92.J87") == 3
    assert ev("suit_diff(H,S)", "AQ752.K4.Q92.J87") == -3


def test_suit_quality():
    assert ev("suit_quality(S)", "AKQJT.432.432.32") == 3 + 1.0
    assert ev("suit_quality(H)", "AKQJT.432.432.32") == 0


def test_top_honor_features():
    assert ev("two_of_top3(S)", "AK752.432.432.32") == 1
    assert ev("two_of_top3(S)", "AJ752.432.432.32") == 0
    assert ev("three_of_top5(S)", "QJT52.432.432.32") == 1
    assert ev("good_suit(S)", "KQ7532.432.43.32") == 1
    assert ev("good_suit(S)", "J86532.A32.43.A2") == 0


def test_stoppers():
    assert ev("stoppers(S)", "A32.5432.543.432") == 1.0
    assert ev("stoppers(S)", "K2.65432.543.432") == 1.0
    assert ev("stoppers(S)", "Q32.5432.543.432") == 1.0
    assert ev("stoppers(S)", "Q2.65432.543.432") == 0.5
    assert ev("stoppers(S)", "432.5432.543.432") == 0.0
    assert ev("stopper(S)", "Q2.65432.543.432") == 0.0


def test_shortness_features():
    assert ev("void(C)", "AKQJT98765432..-.") == 1
    h = "AQ752.KJ42.T92.8"
    assert ev("singleton(C)", h) == 1
    assert ev("singleton(any)", h) == 1
    assert ev("void(any)", h) == 0
    assert ev("singleton_or_void(any)", h) == 1


def test_balanced_classifiers():
    assert ev("balanced", "AQ52.KJ4.T92.873") == 1
    assert ev("balanced", "AQ752.KJ4.T92.87") == 1  # 5332
    assert ev("balanced", "AQ752.KJ42.T92.8") == 0
    assert ev("semi_balanced", "AQ7542.KJ4.T9.87") == 1  # 6322
    assert ev("semi_balanced", "AQ7542.KJ42.T9.8") == 0


def test_keycards_and_queen():
    hand = "AK752.A42.K92.87"
    # aces = 2 (SA, HA), trump king (S) = 1  => 3 keycards
    assert ev("keycards(S)", hand) == 3
    assert ev("keycards(H)", hand) == 2
    assert ev("trump_queen(S)", "AQ752.A42.K92.87", agreed_suit="S") == 1
    assert ev("keycards(agreed)", hand, agreed_suit="S") == 3


def test_aces_kings():
    assert ev("aces", "AK752.A42.K92.87") == 2
    assert ev("kings", "AK752.A42.K92.87") == 2


def test_suit_resolution_partner_their():
    assert ev("suit_length(partner)", "AQ752.K4.Q92.J87", partner_suits=["H"]) == 2
    assert ev("stoppers(their)", "AQ752.K4.Q92.J87", their_suits=["S"]) == 1.0


def test_registry_pluggable():
    @register_evaluator("test_only_spade_aces")
    def _f(hand, ctx):
        return 1.0 if 14 in hand.suit_ranks("S") else 0.0

    assert ev("test_only_spade_aces", "A432.432.432.432") == 1
    del REGISTRY["test_only_spade_aces"]


def test_unknown_evaluator_raises():
    with pytest.raises(KeyError):
        ev("no_such_eval", "A432.432.432.432")
