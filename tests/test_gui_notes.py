"""Notes: what gets attached to one, and what survives a round trip.

The point of a note is that someone can act on it later, from the file alone,
without the GUI running and without the session that wrote it. So the tests
that matter are about the attachment: does the note say which board, and does
the board come back whole.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from bridgebidder.gui.services import notes as N  # noqa: E402

DEAL = {
    "id": "3f2a-session-uuid",
    "source": "corpus",
    "source_file": "seed507.jsonl.gz",
    "board": 477,
    "dealer": "E",
    "vul": "Both",
    "imp_margin": -12,
    "hands": {"N": "T5.763.Q9764.T52", "E": "K9763.AJ52.8.AKJ",
              "S": "AQJ82.QT98.J32.9", "W": "4.K4.AKT5.Q87643"},
    "table_a": {
        "our_side": "NS", "auction": ["1S", "P", "3C", "P"],
        "our_calls": [{"seat": "S", "call": "P", "rule": "oc1S_pass", "n": 1}],
        "contract": "3NT by W (10 tricks)", "tricks": 10, "score_ns": -630,
    },
    "table_b": {
        "our_side": "EW", "auction": ["1S", "P"],
        "our_calls": [{"seat": "E", "call": "1S", "rule": "open_1S", "n": 0}],
        "contract": "6C by W (11 tricks)", "tricks": 11, "score_ns": 100,
    },
}

BID = {"table": "a", "n": 1, "seat": "S", "call": "P",
       "rule_id": "oc1S_pass", "context_id": "overcalls_of_1S",
       "shows": "nothing suitable over 1S"}


@pytest.fixture(autouse=True)
def scratch(tmp_path, monkeypatch):
    """Never touch the repository's own notes while testing."""
    monkeypatch.setattr(N, "NOTES_DIR", tmp_path)
    monkeypatch.setattr(N, "NOTES_JSONL", tmp_path / "notes.jsonl")
    monkeypatch.setattr(N, "NOTES_MD", tmp_path / "NOTES.md")
    return tmp_path


def test_note_identifies_the_board_durably():
    """The session's deal id is a uuid forgotten on restart; the ref is not."""
    note = N.add_note("this pass is wrong", DEAL, BID)
    assert note["deal"]["ref"] == "seed507.jsonl.gz#477"
    assert note["deal"]["session_id"] == "3f2a-session-uuid"


def test_note_carries_enough_to_act_on_without_the_gui():
    note = N.add_note("this pass is wrong", DEAL, BID)
    deal = note["deal"]
    assert deal["hands"] == DEAL["hands"]
    assert deal["table_a"]["auction"] == ["1S", "P", "3C", "P"]
    assert deal["table_a"]["our_calls"][0]["rule"] == "oc1S_pass"
    assert deal["table_b"]["contract"] == "6C by W (11 tricks)"
    assert note["bid"]["rule_id"] == "oc1S_pass"


def test_a_note_needs_no_bid():
    """Some observations are about the auction, not one call."""
    note = N.add_note("the whole auction should have stopped at 2H", DEAL)
    assert note["bid"] is None
    assert note["deal"]["ref"] == "seed507.jsonl.gz#477"


def test_a_note_needs_no_deal_either():
    note = N.add_note("weak twos should deny a side four-card major", None)
    assert note["deal"] is None
    assert note["text"].startswith("weak twos")


def test_empty_text_is_refused():
    for text in ("", "   ", "\n"):
        with pytest.raises(ValueError):
            N.add_note(text, DEAL)


def test_ids_do_not_collide_after_a_delete():
    """Numbering off len(notes) would reuse an id once one is removed."""
    first = N.add_note("one", DEAL)
    second = N.add_note("two", DEAL)
    N.delete_note(first["id"])
    third = N.add_note("three", DEAL)
    assert third["id"] not in {second["id"]}
    ids = [n["id"] for n in N.load_notes()]
    assert len(ids) == len(set(ids)), ids


def test_status_round_trip():
    note = N.add_note("fix me", DEAL)
    assert N.set_status(note["id"], "done")["status"] == "done"
    assert N.set_status(note["id"], "open")["status"] == "open"
    with pytest.raises(ValueError):
        N.set_status(note["id"], "maybe")
    with pytest.raises(KeyError):
        N.set_status("note-9999", "done")


def test_jsonl_is_one_object_per_line(scratch):
    N.add_note("first\nwith a newline in it", DEAL)
    N.add_note("second", DEAL)
    lines = (scratch / "notes.jsonl").read_text(encoding="utf-8").splitlines()
    assert len(lines) == 2
    assert [json.loads(line)["id"] for line in lines] == ["note-0001", "note-0002"]


def test_markdown_shows_the_board_and_the_rules(scratch):
    N.add_note("this pass is wrong", DEAL, BID)
    md = (scratch / "NOTES.md").read_text(encoding="utf-8")
    assert "seed507.jsonl.gz#477" in md
    assert "this pass is wrong" in md
    assert "oc1S_pass" in md
    # the auction is rendered seat by seat, so it reads without the app
    assert "E:1S" in md and "S:P[oc1S_pass]" in md


def test_markdown_separates_open_from_done(scratch):
    a = N.add_note("still open", DEAL)
    b = N.add_note("already handled", DEAL)
    N.set_status(b["id"], "done")
    md = (scratch / "NOTES.md").read_text(encoding="utf-8")
    assert md.index("# Open") < md.index(a["id"])
    assert md.index("# Done") < md.index(b["id"])
    assert md.index(a["id"]) < md.index("# Done")


def test_unknown_client_fields_are_not_stored():
    """The page posts its whole deal payload; only the board is kept."""
    note = N.add_note("x", {**DEAL, "drift": ["..."], "tried": 41, "junk": "y"})
    assert set(note["deal"]) == {
        "ref", "session_id", "source", "source_file", "board", "dealer",
        "vul", "hands", "imp_margin", "table_a", "table_b"}
