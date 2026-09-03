#!/usr/bin/env python3
"""Read the rule notes captured in the GUI, and close them once fixed.

The Deal Explorer records what looked wrong, in the reporter's words, with the
board attached; the rulebook is then edited by hand.  This is the reading end
of that: what is open, everything a note knows about its board, and a way to
mark one done.

    python3 tools/notes.py list                 # open notes, one line each
    python3 tools/notes.py list --all           # including the done ones
    python3 tools/notes.py show note-0003       # everything, including hands
    python3 tools/notes.py show --open          # every open note in full
    python3 tools/notes.py done note-0003       # after the fix is in the YAML
    python3 tools/notes.py reopen note-0003

`data/notes/NOTES.md` holds the same content as one readable document and is
rewritten on every change, so reading that file is equivalent to `show --open`.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from bridgebidder.gui.services import notes as N  # noqa: E402

SEATS = ["W", "N", "E", "S"]


def _auction(deal: dict, key: str) -> str:
    """`W:1D N:1S[open_1S] …` — the auction with the rule behind each of ours."""
    table = deal.get(key) or {}
    calls = table.get("auction") or []
    if not calls:
        return ""
    rules = {c["n"]: c.get("rule") for c in (table.get("our_calls") or [])
             if c.get("n") is not None}
    start = SEATS.index(deal["dealer"]) if deal.get("dealer") in SEATS else 0
    return " ".join(
        f"{SEATS[(start + n) % 4]}:{call}" + (f"[{rules[n]}]" if rules.get(n) else "")
        for n, call in enumerate(calls))


def _summary(note: dict) -> str:
    deal = note.get("deal") or {}
    ref = deal.get("ref", "—")
    first = note["text"].strip().splitlines()[0]
    if len(first) > 70:
        first = first[:67] + "…"
    mark = "x" if note.get("status") == "done" else " "
    return f"[{mark}] {note['id']}  {ref:<24}  {first}"


def _detail(note: dict) -> str:
    lines = [f"=== {note['id']} · {note['created_at']} · {note.get('status', 'open')}"]
    deal = note.get("deal")
    if deal:
        lines.append(f"board   {deal['ref']}   dealer {deal.get('dealer')}   "
                     f"vul {deal.get('vul')}   "
                     f"BEN +{abs(deal.get('imp_margin') or 0)} IMP")
        for seat, hand in (deal.get("hands") or {}).items():
            lines.append(f"  {seat}  {hand}")
        for key, label in (("table_a", "A"), ("table_b", "B")):
            table = deal.get(key) or {}
            if table.get("auction"):
                lines.append(f"  {label} ({table.get('our_side')} us, "
                             f"{table.get('contract')}, NS {table.get('score_ns')})")
                lines.append(f"    {_auction(deal, key)}")
    bid = note.get("bid")
    if bid:
        lines.append(f"about   {bid.get('seat')}'s {bid.get('call')} "
                     f"(call {bid.get('n')}, table {bid.get('table')}) "
                     f"from {bid.get('rule_id')} in {bid.get('context_id')}")
        if bid.get("shows"):
            lines.append(f"        shows: {bid['shows']}")
    lines.append("")
    lines.append("  " + note["text"].replace("\n", "\n  "))
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("list", help="one line per note")
    p.add_argument("--all", action="store_true", help="include done notes")

    p = sub.add_parser("show", help="everything a note knows")
    p.add_argument("note_id", nargs="?")
    p.add_argument("--open", action="store_true", help="every open note")

    for name in ("done", "reopen"):
        p = sub.add_parser(name, help=f"mark a note {name}")
        p.add_argument("note_id")

    args = ap.parse_args()
    all_notes = N.load_notes()

    if args.cmd == "list":
        shown = all_notes if args.all else [
            n for n in all_notes if n.get("status") != "done"]
        if not shown:
            print("no notes" if not all_notes else "nothing open")
            return
        for note in shown:
            print(_summary(note))
        openn = sum(1 for n in all_notes if n.get("status") != "done")
        print(f"\n{openn} open of {len(all_notes)}")
        return

    if args.cmd == "show":
        if args.open or not args.note_id:
            for note in (n for n in all_notes if n.get("status") != "done"):
                print(_detail(note))
            return
        for note in all_notes:
            if note["id"] == args.note_id:
                print(_detail(note))
                return
        sys.exit(f"no note {args.note_id}")

    status = "done" if args.cmd == "done" else "open"
    try:
        note = N.set_status(args.note_id, status)
    except KeyError:
        sys.exit(f"no note {args.note_id}")
    print(f"{note['id']} -> {note['status']}")


if __name__ == "__main__":
    main()
