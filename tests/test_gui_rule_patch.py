"""The rule editor's patches, and what accepting one does to the rulebook.

Every case here is a bug that shipped.  The editor's three buttons all failed
at the preview call because nobody translated the shape the form produces into
the shape the YAML reads; accepting a proposal would have rewritten the whole
rulebook and deleted all 2,230 of its comment lines.  Neither showed up in any
existing test, because neither layer is wrong on its own -- only the seam
between them was.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tools"))

from bridgebidder.gui.services import rule_patch as rp  # noqa: E402
from bridgebidder.system.dsl import parse_system  # noqa: E402

CTX = "openings"
RULE = "open_1NT"


def _rule(data: dict, ctx_id: str = CTX, rule_id: str = RULE) -> dict:
    for ctx in data["contexts"]:
        if ctx["id"] == ctx_id:
            for rule in ctx["rules"]:
                if rule["id"] == rule_id:
                    return rule
    raise AssertionError(f"{ctx_id}/{rule_id} not in the rulebook")


# ---------------------------------------------------------------------------
# the editor's shapes
# ---------------------------------------------------------------------------


def test_modify_rule_accepts_the_editor_diff():
    """The form reports {field: {before, after}}, not a dotted path."""
    patch = {
        "type": "modify_rule", "context_id": CTX, "rule_id": RULE,
        "changes": {
            "hcp": {"before": [15, 17], "after": [15, 18]},
            "priority": {"before": 92, "after": 95},
            "shows": {"before": "x", "after": "15-18 balanced"},
            "forcing_status": {"before": "non_forcing", "after": "one_round"},
            "length_h": {"before": [0, 13], "after": [2, 5]},
        },
    }
    out = rp.apply_patches_to_yaml(rp.load_system_yaml(), [patch])
    rule = _rule(out)
    assert rule["requires"]["hcp"] == [15, 18]
    assert rule["requires"]["suits"]["H"] == [2, 5]
    assert rule["priority"] == 95
    assert rule["shows"] == "15-18 balanced"
    assert rule["establishes"]["forcing"] == "one_round"
    parse_system(out)


def test_explicit_field_shape_still_works():
    patch = {"type": "modify_rule", "context_id": CTX, "rule_id": RULE,
             "field": "requires.hcp", "after": [16, 18]}
    out = rp.apply_patches_to_yaml(rp.load_system_yaml(), [patch])
    assert _rule(out)["requires"]["hcp"] == [16, 18]


def test_suit_reset_to_full_range_removes_the_constraint():
    """`S: [0, 13]` constrains nothing and must not be written back."""
    add = {"type": "modify_rule", "context_id": CTX, "rule_id": RULE,
           "changes": {"length_s": {"after": [4, 5]}}}
    data = rp.apply_patches_to_yaml(rp.load_system_yaml(), [add])
    assert _rule(data)["requires"]["suits"]["S"] == [4, 5]

    reset = {"type": "modify_rule", "context_id": CTX, "rule_id": RULE,
             "changes": {"length_s": {"after": [0, 13]}}}
    data = rp.apply_patches_to_yaml(data, [reset])
    assert "S" not in _rule(data)["requires"].get("suits", {})


def test_forcing_status_outside_the_dsl_is_rejected():
    """The form used to offer 'forcing' and 'passable', which do not exist."""
    for bogus in ("forcing", "passable"):
        patch = {"type": "modify_rule", "context_id": CTX, "rule_id": RULE,
                 "changes": {"forcing_status": {"after": bogus}}}
        assert rp.preview_patch(patch)["ok"] is False


def test_exception_lands_under_the_dsl_not_key():
    patch = {"type": "add_exception", "context_id": CTX, "rule_id": RULE,
             "constraint": {"hcp": [15, 15], "lengths": {"s": [5, 13]}}}
    out = rp.apply_patches_to_yaml(rp.load_system_yaml(), [patch])
    assert _rule(out)["requires"]["not"] == {"hcp": [15, 15], "suits": {"S": [5, 13]}}
    parse_system(out)


def test_two_exceptions_accumulate_as_not_any_of():
    """not A and not B is not (A or B) -- one `not`, not a list of them."""
    patches = [
        {"type": "add_exception", "context_id": CTX, "rule_id": RULE,
         "constraint": {"lengths": {"s": [5, 13]}}},
        {"type": "add_exception", "context_id": CTX, "rule_id": RULE,
         "constraint": {"lengths": {"d": [7, 13]}}},
    ]
    out = rp.apply_patches_to_yaml(rp.load_system_yaml(), patches)
    assert _rule(out)["requires"]["not"] == {"any_of": [
        {"suits": {"S": [5, 13]}}, {"suits": {"D": [7, 13]}}]}
    parse_system(out)


def test_exception_that_constrains_nothing_is_refused():
    """The form always submits all four suits, usually untouched.

    Carried through literally, the exception matches every hand and denies the
    rule to everyone -- a rule silently switched off by a form nobody edited.
    """
    patch = {"type": "add_exception", "context_id": CTX, "rule_id": RULE,
             "constraint": {"hcp": [0, 37],
                            "lengths": {s: [0, 13] for s in "shdc"}}}
    result = rp.preview_patch(patch)
    assert result["ok"] is False
    assert "constrains nothing" in result["error"]


def test_add_rule_from_the_editor_shape():
    patch = {
        "type": "add_rule", "context_id": CTX, "after_rule_id": RULE,
        "rule": {"call": "1NT", "priority": 93, "shows": "18-19 balanced",
                 "forcing_status": "non_forcing",
                 "constraint": {"hcp": [18, 19],
                                "lengths": {s: [0, 13] for s in "shdc"}}},
    }
    out = rp.apply_patches_to_yaml(rp.load_system_yaml(), [patch])
    ctx = next(c for c in out["contexts"] if c["id"] == CTX)
    ids = [r["id"] for r in ctx["rules"]]
    new_id = ids[ids.index(RULE) + 1]           # inserted next to its sibling
    new = _rule(out, rule_id=new_id)
    assert new["requires"] == {"hcp": [18, 19]}  # no-op suit bounds dropped
    assert new["establishes"] == {"forcing": "non_forcing"}
    parse_system(out)


def test_add_rule_replays_the_whole_context_in_the_corpus_precheck():
    """A new rule's id is on no recorded board, so its context must be."""
    patch = {"type": "add_rule", "context_id": CTX,
             "rule": {"call": "1NT", "priority": 93, "shows": "x",
                      "constraint": {"hcp": [18, 19]}}}
    touched = rp.get_touched_rule_ids([patch])
    assert RULE in touched and "open_1C" in touched


# ---------------------------------------------------------------------------
# accepting a proposal
# ---------------------------------------------------------------------------


def test_accepting_a_proposal_keeps_every_comment(tmp_path, monkeypatch):
    """The rulebook is 2,230 comment lines of reasoning; a write must keep them.

    A PyYAML round-trip drops all of them and reflows the file from 16,683
    lines to 32,395 -- so one accepted three-line proposal would have landed
    as an unreviewable whole-file rewrite with the documentation gone.
    """
    pytest.importorskip("ruamel.yaml")

    original = rp.YAML_PATH.read_text(encoding="utf-8")
    scratch = tmp_path / "two_over_one.yaml"
    scratch.write_text(original, encoding="utf-8")
    monkeypatch.setattr(rp, "YAML_PATH", scratch)

    def comments(text: str) -> int:
        return sum(1 for line in text.splitlines() if line.strip().startswith("#"))

    result = rp.apply_and_write([
        {"type": "modify_rule", "context_id": CTX, "rule_id": RULE,
         "changes": {"hcp": {"after": [15, 18]}}},
    ])
    after = scratch.read_text(encoding="utf-8")

    assert comments(after) == comments(original)
    # The change reviews as the lines it touched, not as the whole file.
    assert result["changed_lines"] <= 10, result
    assert _rule(rp.load_system_yaml())["requires"]["hcp"] == [15, 18]


def test_a_patch_that_will_not_parse_never_reaches_the_file(tmp_path, monkeypatch):
    pytest.importorskip("ruamel.yaml")

    original = rp.YAML_PATH.read_text(encoding="utf-8")
    scratch = tmp_path / "two_over_one.yaml"
    scratch.write_text(original, encoding="utf-8")
    monkeypatch.setattr(rp, "YAML_PATH", scratch)

    with pytest.raises(Exception):
        rp.apply_and_write([
            {"type": "modify_rule", "context_id": CTX, "rule_id": RULE,
             "changes": {"forcing_status": {"after": "passable"}}},
        ])
    assert scratch.read_text(encoding="utf-8") == original
