"""Explanation snapshot tests: the full structured BidExplanation JSON for ~20
representative calls is frozen in tests/data/explanation_snapshots.json.

Regenerate deliberately after a system change with:
    python tests/test_snapshots.py --regen
"""

import json
import sys
from pathlib import Path

import pytest

from bridgebidder.api import explain_bid

SNAPSHOT_FILE = Path(__file__).parent / "data" / "explanation_snapshots.json"

CASES = [
    ("open_1S", [], "1S"),
    ("open_1NT", [], "1NT"),
    ("open_2C", [], "2C"),
    ("open_weak_2H", [], "2H"),
    ("resp_2over1_2C", ["1S", "P"], "2C"),
    ("resp_jacoby_2NT", ["1S", "P"], "2NT"),
    ("resp_splinter_4C", ["1S", "P"], "4C"),
    ("resp_limit_raise", ["1H", "P"], "3H"),
    ("resp_semiforcing_1NT", ["1H", "P"], "1NT"),
    ("stayman", ["1NT", "P"], "2C"),
    ("jacoby_transfer", ["1NT", "P"], "2D"),
    ("quantitative_4NT", ["1NT", "P"], "4NT"),
    ("support_double", ["1D", "P", "1S", "2C"], "X"),
    ("support_double_denied_by_2D", ["1D", "P", "1S", "2C"], "2D"),
    ("support_redouble", ["1D", "P", "1H", "X"], "XX"),
    ("negative_double", ["1C", "1H"], "X"),
    ("cue_raise", ["1H", "1S"], "2S"),
    ("takeout_double", ["1H"], "X"),
    ("jordan_2NT", ["1S", "X"], "2NT"),
    ("rkc_response_5C", ["1S", "P", "2NT", "P", "3C", "P", "4NT", "P"], "5C"),
    ("general_agreement_2NT_deep", ["1C", "P", "1H", "P", "1S", "P", "2D", "P"], "2NT"),
    ("opener_1NT_rebid", ["1D", "P", "1S", "P"], "1NT"),
]


def _explain(calls, candidate):
    n = len(calls)
    return explain_bid({
        "auction_state": {"dealer": "N", "seat": "NESW"[n % 4], "calls": list(calls)},
        "candidate": candidate,
    })


def _load():
    return json.loads(SNAPSHOT_FILE.read_text())


@pytest.mark.parametrize("name,calls,candidate", CASES, ids=[c[0] for c in CASES])
def test_explanation_snapshot(name, calls, candidate):
    snapshots = _load()
    assert name in snapshots, f"snapshot {name} missing; regenerate with --regen"
    got = _explain(calls, candidate)
    assert got == snapshots[name], (
        f"snapshot drift for {name}:\n got: {json.dumps(got, indent=1)}\n"
        f" want: {json.dumps(snapshots[name], indent=1)}"
    )


def test_snapshot_schema_fields():
    """Every snapshot carries the full BidExplanation schema."""
    for name, snap in _load().items():
        for field in ("call", "shows", "denies", "forcing_status", "alertable",
                      "convention", "source_rule_id", "is_undiscussed_fallback"):
            assert field in snap, f"{name} missing {field}"
        for field in ("hcp", "suits", "features", "text"):
            assert field in snap["shows"], f"{name}.shows missing {field}"


if __name__ == "__main__" and "--regen" in sys.argv:
    out = {name: _explain(calls, candidate) for name, calls, candidate in CASES}
    SNAPSHOT_FILE.write_text(json.dumps(out, indent=1, sort_keys=True))
    print(f"wrote {len(out)} snapshots to {SNAPSHOT_FILE}")
