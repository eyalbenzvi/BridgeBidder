"""Free-text notes about the rulebook, captured against a specific board.

Why notes instead of patches
----------------------------
The GUI used to let you edit a rule directly: an HCP range, four suit lengths,
a priority, a forcing status.  That form could express only what its fields
happened to cover, which is a small corner of what the rulebook can say -- no
`evals`, no `shapes`, no `when` conditions, no "this rule should not exist at
all", no "the real problem is two rules competing".  Worse, it demanded the
answer up front: to change anything you first had to know exactly which rule,
which field, and which number.

Describing the problem is a different act from encoding the fix, and only the
second one needs the DSL.  So the GUI now captures the first: what you saw,
what you think is wrong, in your own words, with the board attached.  The
second happens in a Claude session that reads these notes and edits the YAML.

What gets attached
------------------
Everything needed to act on the note without the GUI running: the durable
board reference (`seed510.jsonl.gz#89`, which survives restarts, unlike the
session's deal id), all four hands, both auctions with our calls and the rules
behind them, the scores, and -- when the note was written from a specific bid
-- that bid's seat, call and rule. A note that says "this double is wrong" and
cannot say which board is not actionable a day later.

On disk
-------
`data/notes/notes.jsonl` is the record, one JSON object per line, append-only.
`data/notes/NOTES.md` is regenerated beside it on every write: same content,
laid out to be read straight through. Both are in the repository, so a note
taken on a phone reaches the session by way of a commit.
"""

from __future__ import annotations

import datetime
import json
from pathlib import Path
from typing import Any

NOTES_DIR = Path(__file__).parents[4] / "data" / "notes"
NOTES_JSONL = NOTES_DIR / "notes.jsonl"
NOTES_MD = NOTES_DIR / "NOTES.md"

MAX_TEXT = 8000
STATUSES = ("open", "done")


def _now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat(
        timespec="seconds").replace("+00:00", "Z")


def board_ref(deal: dict) -> str:
    """A board identifier that still means something tomorrow.

    The deal id in the payload is a uuid minted per session and forgotten on
    restart; the pool file and board number address the same board forever.
    """
    src = deal.get("source_file")
    board = deal.get("board")
    if src and board is not None:
        return f"{src}#{board}"
    return str(deal.get("id") or "unknown")


def _table(t: dict | None) -> dict:
    t = t or {}
    return {
        "our_side": t.get("our_side"),
        "auction": list(t.get("auction") or []),
        "our_calls": [
            {"seat": c.get("seat"), "call": c.get("call"),
             "rule": c.get("rule"), "n": c.get("n")}
            for c in (t.get("our_calls") or [])
        ],
        "contract": t.get("contract"),
        "tricks": t.get("tricks"),
        "score_ns": t.get("score_ns"),
    }


def _deal_snapshot(deal: dict) -> dict:
    """Keep the board, drop everything else the client happened to send."""
    return {
        "ref": board_ref(deal),
        "session_id": deal.get("id"),
        "source": deal.get("source"),
        "source_file": deal.get("source_file"),
        "board": deal.get("board"),
        "dealer": deal.get("dealer"),
        "vul": deal.get("vul"),
        "hands": dict(deal.get("hands") or {}),
        "imp_margin": deal.get("imp_margin"),
        "table_a": _table(deal.get("table_a")),
        "table_b": _table(deal.get("table_b")),
    }


def _bid_snapshot(bid: dict | None) -> dict | None:
    if not bid:
        return None
    return {
        "table": bid.get("table"),
        "n": bid.get("n"),
        "seat": bid.get("seat"),
        "call": bid.get("call"),
        "rule_id": bid.get("rule_id"),
        "context_id": bid.get("context_id"),
        "shows": bid.get("shows"),
    }


# ---------------------------------------------------------------------------
# read / write
# ---------------------------------------------------------------------------


def load_notes() -> list[dict]:
    if not NOTES_JSONL.exists():
        return []
    out: list[dict] = []
    for line in NOTES_JSONL.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                continue          # a truncated line must not hide the rest
    return out


def _write_all(notes: list[dict]) -> None:
    NOTES_DIR.mkdir(parents=True, exist_ok=True)
    tmp = NOTES_JSONL.with_suffix(".jsonl.new")
    tmp.write_text(
        "".join(json.dumps(n, ensure_ascii=False) + "\n" for n in notes),
        encoding="utf-8")
    tmp.replace(NOTES_JSONL)
    render_markdown(notes)


def _next_id(notes: list[dict]) -> str:
    """One past the highest number ever used, not one past the count.

    Counting hands out a duplicate the moment a note is deleted, and then
    "mark note-0002 done" has two candidates -- in a list whose whole purpose
    is that someone can refer to an entry unambiguously later.
    """
    used = [int(n["id"].rsplit("-", 1)[-1]) for n in notes
            if n.get("id", "").rsplit("-", 1)[-1].isdigit()]
    return f"note-{(max(used) + 1) if used else 1:04d}"


def add_note(text: str, deal: dict | None, bid: dict | None = None) -> dict:
    text = (text or "").strip()
    if not text:
        raise ValueError("A note needs some text.")
    if len(text) > MAX_TEXT:
        raise ValueError(f"Note is too long ({len(text)} > {MAX_TEXT} characters).")

    notes = load_notes()
    note = {
        "id": _next_id(notes),
        "created_at": _now(),
        "status": "open",
        "text": text,
        "deal": _deal_snapshot(deal) if deal else None,
        "bid": _bid_snapshot(bid),
    }
    notes.append(note)
    _write_all(notes)
    return note


def set_status(note_id: str, status: str) -> dict:
    if status not in STATUSES:
        raise ValueError(f"status must be one of {', '.join(STATUSES)}")
    notes = load_notes()
    for note in notes:
        if note["id"] == note_id:
            note["status"] = status
            note["updated_at"] = _now()
            _write_all(notes)
            return note
    raise KeyError(note_id)


def delete_note(note_id: str) -> None:
    notes = load_notes()
    kept = [n for n in notes if n["id"] != note_id]
    if len(kept) == len(notes):
        raise KeyError(note_id)
    _write_all(kept)


# ---------------------------------------------------------------------------
# the readable copy
# ---------------------------------------------------------------------------


def _auction_lines(deal: dict) -> list[str]:
    """Both auctions, with the rule behind each of our calls."""
    lines: list[str] = []
    for key, label in (("table_a", "Table A"), ("table_b", "Table B")):
        t = deal.get(key) or {}
        calls = t.get("auction") or []
        if not calls:
            continue
        rules = {c["n"]: c.get("rule") for c in (t.get("our_calls") or [])
                 if c.get("n") is not None}
        seats = ["W", "N", "E", "S"]
        start = seats.index(deal["dealer"]) if deal.get("dealer") in seats else 0
        parts = []
        for n, call in enumerate(calls):
            seat = seats[(start + n) % 4]
            rule = rules.get(n)
            parts.append(f"{seat}:{call}" + (f"[{rule}]" if rule else ""))
        lines.append(f"- **{label}** ({t.get('our_side')} is us) — "
                     f"{t.get('contract') or 'passed out'}, "
                     f"NS {t.get('score_ns')}")
        lines.append(f"  `{' '.join(parts)}`")
    return lines


def render_markdown(notes: list[dict] | None = None) -> str:
    """Rewrite NOTES.md from the record.

    The JSONL is the source of truth; this is the same thing arranged to be
    read. Open notes come first because they are the ones with work in them.
    """
    notes = load_notes() if notes is None else notes
    openn = [n for n in notes if n.get("status") != "done"]
    done = [n for n in notes if n.get("status") == "done"]

    out: list[str] = [
        "# Rule notes",
        "",
        "Captured from the Deal Explorer: what looked wrong, in the reporter's",
        "words, with the board it happened on. The fixes are made by hand in",
        "`src/bridgebidder/systems/two_over_one.yaml` — nothing here edits it.",
        "",
        f"{len(openn)} open · {len(done)} done · "
        f"generated from `notes.jsonl`, do not edit this file by hand.",
        "",
    ]

    def block(note: dict) -> list[str]:
        lines = [f"## {note['id']} · {note['created_at']}"
                 + ("" if note.get("status") != "done" else " · done"), ""]
        deal = note.get("deal")
        if deal:
            lines.append(f"**Board `{deal['ref']}`** — dealer {deal.get('dealer')}, "
                         f"vul {deal.get('vul')}, "
                         f"BEN won by {abs(deal.get('imp_margin') or 0)} IMP")
            lines.append("")
            hands = deal.get("hands") or {}
            if hands:
                lines.append("| " + " | ".join(hands) + " |")
                lines.append("|" + "---|" * len(hands))
                lines.append("| " + " | ".join(hands.values()) + " |")
                lines.append("")
            lines += _auction_lines(deal)
            lines.append("")
        bid = note.get("bid")
        if bid:
            lines.append(
                f"**About:** {bid.get('seat')}'s {bid.get('call')} "
                f"(call {bid.get('n')}, table {bid.get('table')}) from rule "
                f"`{bid.get('rule_id')}` in `{bid.get('context_id')}`"
                + (f" — {bid.get('shows')}" if bid.get("shows") else ""))
            lines.append("")
        lines.append("> " + note["text"].replace("\n", "\n> "))
        lines.append("")
        return lines

    if openn:
        out += ["---", "", "# Open", ""]
        for note in openn:
            out += block(note)
    if done:
        out += ["---", "", "# Done", ""]
        for note in done:
            out += block(note)

    text = "\n".join(out)
    NOTES_DIR.mkdir(parents=True, exist_ok=True)
    NOTES_MD.write_text(text, encoding="utf-8")
    return text
