#!/usr/bin/env python3
"""One losing board, every decision we made, laid out for a verdict.

The per-decision audit (`ben_audit.py`) ranks leads across a whole corpus.  This
tool does the opposite: it takes ONE board and prints everything needed to sit in
each of our seats in turn and say what is wrong, if anything.  For every call we
made, at both tables, it shows the hand, the auction to that point, what we bid
and which rule said so, the whole candidate set with fits and priorities, which
contexts were live, and what BEN would have called from the same seat.

Each decision gets exactly one verdict:

    OK               - the call is right, or a defensible judgment call
    CATEGORY         - the situation was filed as the wrong KIND of auction, so
                       the wrong family of rules was competing at all
    EXCEPTION        - the rule is right in general and wrong here; it needs a
                       stated exception
    RULE-WRONG       - the rule is wrong as written wherever it fires

    python3 tools/board_critique.py --rows reports/r13_batch1.jsonl \
                                    --audit reports/r13_audit1.jsonl --board 7
    python3 tools/board_critique.py --rows ... --audit ... --losses   # list them
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from bridgebidder.domain.auction import Auction            # noqa: E402
from bridgebidder.domain.calls import Call                 # noqa: E402
from bridgebidder.domain.cards import Hand                 # noqa: E402
from bridgebidder.domain.types import Seat, Vulnerability  # noqa: E402
from bridgebidder.engine.decision import score_candidates  # noqa: E402
from bridgebidder.inference.engine import prepare_decision  # noqa: E402
from bridgebidder.system.dsl import load_system            # noqa: E402

SEATS = "NESW"
_SYS = None


def system():
    global _SYS
    if _SYS is None:
        _SYS = load_system()
    return _SYS


def seat_of(row, table, index):
    return SEATS[(SEATS.index(row["dealer"]) + index) % 4]


def candidates(hand, dealer, vul, seat, calls, top):
    a = Auction(dealer=Seat(dealer), vulnerability=Vulnerability.parse(vul))
    for c in calls:
        a.add(Call.parse(c))
    setup = prepare_decision(system(), a, perspective=Seat(seat))
    ctxs, seen = [], set()
    for cand in setup.candidates:
        cid = getattr(cand.rule, "context_id", None) if cand.rule else None
        if cid and cid not in seen:
            seen.add(cid)
            ctxs.append(cid)
    out = []
    for sc in score_candidates(setup, Hand.parse(hand))[:top]:
        c = sc.candidate
        out.append((str(sc.call),
                    c.rule.id if c.rule else "FALLBACK",
                    round(sc.fit, 2), round(sc.score, 2), c.priority,
                    (c.shows or "")[:88]))
    return ctxs, out, setup.eval_ctx


def critique(row, audit, top):
    ben = {(a["table"], a["index"]): a for a in audit
           if a["board"] == row["board"]}
    print(f"{'='*78}\nBOARD {row['board']}   {row['imp_margin']:+d} IMPs   "
          f"dealer {row['dealer']}   vul {row['vul']}   par(NS) {row['par_ns']}")
    for s in SEATS:
        print(f"   {s}: {row['hands'][s]}")
    for table, side in (("a", "N/S"), ("b", "E/W")):
        calls = row[f"{table}_auction"].split()
        print(f"\n--- TABLE {table.upper()} (we are {side})  ->  "
              f"{row[f'{table}_contract']}")
        print("    " + " ".join(
            f"{SEATS[(SEATS.index(row['dealer'])+i) % 4]}:{c}"
            for i, c in enumerate(calls)))
        for oc in row[f"{table}_our_calls"]:
            i = oc["n"]
            if i >= len(calls):
                continue
            seat = seat_of(row, table, i)
            ctxs, cands, ec = candidates(
                row["hands"][seat], row["dealer"], row["vul"], seat, calls[:i], top)
            b = ben.get((table, i))
            print(f"\n  [{table}{i}] {seat} {row['hands'][seat]}   after: "
                  f"{' '.join(calls[:i]) or '(opening)'}")
            print(f"      WE {oc['call']:<4} ({oc['rule'] or 'fallback'})", end="")
            if b:
                print(f"   BEN {b['ben']:<4} conf {b['ben_conf']:.2f}"
                      f"   {'<-- FIRST DIVERGENCE' if b['first_divergence'] else ''}")
            else:
                print("   BEN agrees")
            print(f"      contexts: {ctxs}")
            print(f"      they: competitive={ec.is_competitive} bidders={ec.their_shown_count} "
                  f"min_hcp={ec.their_min_hcp:g} max_fit={ec.their_max_fit}  |  "
                  f"partner: {ec.partner_min_hcp:g}-{ec.partner_max_hcp:g} "
                  f"suits={ec.partner_suits}")
            for call, rid, fit, score, prio, shows in cands:
                mark = "*" if call == oc["call"] else (">" if b and call == b["ben"] else " ")
                print(f"      {mark} {call:<4} {fit:<5} s={score:<5} p={prio:<6} {rid:<26} {shows}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows", type=Path, required=True)
    ap.add_argument("--audit", type=Path, required=True)
    ap.add_argument("--board", type=int, action="append", default=[])
    ap.add_argument("--losses", action="store_true")
    ap.add_argument("--top", type=int, default=7)
    a = ap.parse_args()
    rows = [json.loads(l) for l in open(a.rows)]
    audit = [json.loads(l) for l in open(a.audit)] if a.audit.exists() else []
    if a.losses:
        lost = [r for r in rows if r["imp_margin"] < 0]
        print(f"{len(lost)} losing boards of {len(rows)}: " +
              " ".join(f"{r['board']}({r['imp_margin']:+d})"
                       for r in sorted(lost, key=lambda r: r["imp_margin"])))
    for n in a.board:
        critique(next(r for r in rows if r["board"] == n), audit, a.top)
