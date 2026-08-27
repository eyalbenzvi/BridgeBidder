"""Regression suite: auction scenarios as data files.

Each YAML file in tests/data/ holds a list of scenarios:
  name: short description
  hand: "AQ52.KJ4.T92.873"
  dealer: N          (default N)
  vulnerability: None (default)
  seat: N            (default: whoever is on turn)
  calls: ["1H", "P", ...]   entries may also be {call: "2D", explanation: {...}}
  expect:
    call: "1S"       or  calls: ["1S", "P"]  (accepted set)
    forcing: game_forcing     (optional)
    alertable: true           (optional)
    convention: stayman       (optional)
    fallback: true            (optional: is_undiscussed_fallback)
    rule: open_1S             (optional: source_rule_id prefix)
    denies_contains: "text"   (optional: some denial text contains this)

Scenarios run through the deterministic fast path (no simulation) so results
are stable; genuinely borderline hands use accepted sets.
"""

from pathlib import Path

import pytest
import yaml

from bridgebidder.api import choose_bid

DATA_DIR = Path(__file__).parent / "data"


def _load_scenarios():
    out = []
    for f in sorted(DATA_DIR.glob("*.yaml")):
        for sc in yaml.safe_load(f.read_text()) or []:
            sc["_file"] = f.stem
            out.append(sc)
    return out


SCENARIOS = _load_scenarios()


def _scenario_id(sc):
    return f"{sc['_file']}::{sc['name']}"


@pytest.mark.parametrize("sc", SCENARIOS, ids=_scenario_id)
def test_scenario(sc):
    calls = []
    for c in sc.get("calls", []):
        calls.append(c if isinstance(c, dict) else {"call": str(c)})
    dealer = sc.get("dealer", "N")
    n_calls = len(calls)
    seat_idx = ("NESW".index(dealer) + n_calls) % 4
    seat = sc.get("seat", "NESW"[seat_idx])

    result = choose_bid({
        "hand": sc["hand"],
        "auction_state": {
            "dealer": dealer,
            "vulnerability": sc.get("vulnerability", "None"),
            "seat": seat,
            "calls": calls,
        },
        "use_arbitration": False,
    })

    exp = sc["expect"]
    accepted = [str(x) for x in ([exp["call"]] if "call" in exp else exp["calls"])]
    assert result["chosen_call"] in accepted, (
        f"{sc['name']}: chose {result['chosen_call']}, expected {accepted}. "
        f"top alternatives: {[(a['call'], a['match_score']) for a in result['alternatives'][:3]]} "
        f"explanation: {result['explanation']['shows']['text']}"
    )
    e = result["explanation"]
    if "forcing" in exp:
        assert e["forcing_status"] == exp["forcing"], f"{sc['name']}: forcing {e['forcing_status']}"
    if "alertable" in exp:
        assert e["alertable"] == exp["alertable"], f"{sc['name']}: alertable {e['alertable']}"
    if "convention" in exp:
        assert e["convention"] == exp["convention"], f"{sc['name']}: convention {e['convention']}"
    if "fallback" in exp:
        assert e["is_undiscussed_fallback"] == exp["fallback"], f"{sc['name']}: fallback flag"
    if "rule" in exp:
        assert e["source_rule_id"].startswith(exp["rule"]), f"{sc['name']}: rule {e['source_rule_id']}"
    if "denies_contains" in exp:
        texts = " | ".join(d["text"] for d in e["denies"])
        assert exp["denies_contains"] in texts, f"{sc['name']}: denies {texts!r}"


def test_at_least_150_scenarios():
    assert len(SCENARIOS) >= 150, f"only {len(SCENARIOS)} regression scenarios"
