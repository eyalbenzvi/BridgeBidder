"""The system lints run clean, and they catch the bugs that motivated them.

Three consecutive expert reviews rediscovered the same defect species by
hand.  These tests keep the machine finding them instead - and, just as
importantly, prove the detectors are not vacuous by running them against
a system that is known to contain the bug.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import lint_system as L  # noqa: E402

from bridgebidder.system.dsl import load_system  # noqa: E402


@pytest.fixture(scope="module")
def contexts():
    return list(load_system().contexts)


def test_no_call_collisions(contexts):
    """No context defines one call both game-forcing and non-forcing.

    Same-call rules merge into a disjunction, so a call that reads as both
    is a call partner cannot trust: over 1C the 2C response was defined as
    a 6-10 raise AND as the 2/1, and a nine-count drove to five of a minor.
    """
    assert L.lint_collide(contexts) == []


def test_no_strength_gaps(contexts):
    """No band-laddered context leaves an interior strength band uncovered.

    "Range with no rule" is the single most recurring defect in this
    project's history; the permissive pass floor swallows the hole silently.
    """
    assert L.lint_gap(contexts) == []


def test_discrete_gates_are_sharp(contexts):
    """Boolean/counting evaluators used as gates must be registered sharp.

    A hand failing a [1,1] boolean gate otherwise scores ~0.8 against it -
    the gate only leans, which is how twenty-four "two of the top three"
    penalty-pass gates were not gating at all.
    """
    assert L.lint_soft(contexts) == []


def test_no_strength_only_ladders(contexts):
    """No multi-strain ladder bands by strength while ignoring shape.

    Both reviewers of the seed-515151 match named this species: a context
    whose rules ladder purely on points has no rung for "responder holds
    his own long suit", so a six-bagger falls through to the catch-all
    pass.  The `gap` lint cannot see it - it reads strength only.
    """
    assert L.lint_shape(contexts) == []


def test_rule_families_are_gated_consistently(contexts):
    """No member of a rule family is missing a gate the rest require.

    The other species both reviewers named, and every real instance crossed
    calls or contexts: a combined-trump gate added to the keycard asks while
    the raw length gate stayed, a denial written over 1S but not over 1H,
    the their-suit stopper sweep that reached uc_nt2/uc_nt3 but not uc_nt1.
    """
    assert L.lint_siblings(contexts) == []


def test_collide_lint_catches_a_known_collision():
    """The detector is not vacuous: it finds the real historical bug."""
    fixture = ROOT / "tests" / "fixtures" / "lint_collision_fixture.yaml"
    system = load_system(str(fixture))
    findings = L.lint_collide(list(system.contexts))
    assert any("2C" in f and "game-forcing and non-forcing" in f for f in findings), findings
