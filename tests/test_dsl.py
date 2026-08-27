"""Unit tests: pattern matcher + system DSL loading/validation."""

import pytest

from bridgebidder.system.dsl import load_system, parse_system
from bridgebidder.system.matcher import compile_pattern, pattern_matches


# ------------------------------------------------------------------ matcher

def m(pattern, calls):
    return pattern_matches(compile_pattern(pattern), calls)


def test_literal_patterns():
    assert m("?", [])
    assert not m("?", ["1H"])
    assert m("1H - P - ?", ["1H", "P"])
    assert not m("1H - P - ?", ["1H", "X"])
    assert not m("1H - P - ?", ["1H"])


def test_alternation():
    assert m("1(H|S) - P - ?", ["1H", "P"])
    assert m("1(H|S) - P - ?", ["1S", "P"])
    assert not m("1(H|S) - P - ?", ["1D", "P"])
    assert m("(1H|2C) - ?", ["2C"])


def test_wildcards():
    assert m("* - ?", ["3NT"])
    assert m("* - ?", ["P"])
    assert m("bid - ?", ["2C"])
    assert not m("bid - ?", ["X"])
    assert m("act - ?", ["X"])
    assert not m("act - ?", ["P"])


def test_bounded_bid_tokens():
    assert m("1H - bid<2H - ?", ["1H", "2C"])
    assert not m("1H - bid<2H - ?", ["1H", "2H"])
    assert m("1D - bid<=3S - ?", ["1D", "3S"])
    assert m("1D - bid>1NT - ?", ["1D", "2C"])
    assert not m("1D - bid>1NT - ?", ["1D", "1S"])


def test_open_prefix():
    assert m("... - 4NT - P - ?", ["1S", "P", "2NT", "P", "4NT", "P"])
    assert m("... - 4NT - P - ?", ["4NT", "P"])
    assert not m("... - 4NT - P - ?", ["4NT", "X"])


def test_pattern_must_end_with_decision_point():
    with pytest.raises(ValueError):
        compile_pattern("1H - P")
    with pytest.raises(ValueError):
        compile_pattern("1Z - ?")


def test_specificity_orders_anchored_over_open():
    anchored = compile_pattern("1H - P - ?")
    open_p = compile_pattern("... - ?")
    assert anchored.specificity > open_p.specificity


# ------------------------------------------------------------------ loader

def test_load_default_system():
    s = load_system()
    assert s.name.startswith("Two-over-One")
    assert len(s.contexts) > 100
    assert s.config["forcing_nt"] == "semi"
    # canonical contexts exist
    ids = set(s.context_ids())
    assert "openings" in ids
    assert any(i.startswith("support_double") for i in ids)
    assert any(i.startswith("rkc_response") for i in ids)


def test_config_overrides():
    s = load_system(config_overrides={"forcing_nt": "full"})
    assert s.config["forcing_nt"] == "full"


def test_template_expansion():
    data = {
        "system": {"name": "t"},
        "contexts": [{
            "id": "resp",
            "expand": {"M": ["H", "S"]},
            "pattern": "1$M - P - ?",
            "rules": [{"call": "2$M", "requires": {"suits": {"$M": [3, 13]}},
                       "shows": "raise of $M"}],
        }],
    }
    s = parse_system(data)
    assert len(s.contexts) == 2
    assert s.contexts[0].id == "resp[H]"
    assert str(s.contexts[0].rules[0].call) == "2H"
    assert s.contexts[1].rules[0].requires.suits == {"S": (3, 13)}


def test_expand_pairs():
    data = {
        "system": {"name": "t"},
        "contexts": [{
            "id": "tr",
            "expand_pairs": [{"M": "H", "T": "D"}, {"M": "S", "T": "H"}],
            "pattern": "1NT - P - 2$T - P - ?",
            "rules": [{"call": "2$M", "shows": "accept"}],
        }],
    }
    s = parse_system(data)
    assert [str(c.rules[0].call) for c in s.contexts] == ["2H", "2S"]


def test_other_major_template_var():
    data = {
        "system": {"name": "t"},
        "contexts": [{
            "id": "x",
            "expand": {"M": ["H", "S"]},
            "pattern": "1$M - P - ?",
            "rules": [{"call": "1NT", "requires": {"suits": {"$oM": [4, 13]}}, "shows": ""}],
        }],
    }
    s = parse_system(data)
    assert s.contexts[0].rules[0].requires.suits == {"S": (4, 13)}
    assert s.contexts[1].rules[0].requires.suits == {"H": (4, 13)}


def test_unknown_rule_key_rejected():
    data = {
        "system": {"name": "t"},
        "contexts": [{
            "id": "x", "pattern": "?",
            "rules": [{"call": "1H", "showz": "typo"}],
        }],
    }
    with pytest.raises(ValueError):
        parse_system(data)


def test_bad_forcing_status_rejected():
    data = {
        "system": {"name": "t"},
        "contexts": [{
            "id": "x", "pattern": "?",
            "rules": [{"call": "1H", "establishes": {"forcing": "sorta"}}],
        }],
    }
    with pytest.raises(ValueError):
        parse_system(data)


def test_duplicate_context_ids_rejected():
    data = {
        "system": {"name": "t"},
        "contexts": [
            {"id": "x", "pattern": "?", "rules": []},
            {"id": "x", "pattern": "1H - ?", "rules": []},
        ],
    }
    with pytest.raises(ValueError):
        parse_system(data)


def test_all_rule_evals_are_registered():
    """Every evaluator spec used in the shipped system must resolve."""
    from bridgebidder.evaluation.registry import parse_spec, get_evaluator

    s = load_system()
    for ctx in s.contexts:
        for r in ctx.rules:
            stack = [r.requires]
            while stack:
                c = stack.pop()
                for spec in list(c.evals) + list(c.features):
                    name, _ = parse_spec(spec)
                    get_evaluator(name)  # raises if missing
                stack.extend(c.any_of)
                stack.extend(c.all_of)
                if c.not_:
                    stack.append(c.not_)
