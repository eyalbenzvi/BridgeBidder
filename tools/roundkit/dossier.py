#!/usr/bin/env python3
"""The round-18 dossier: one self-contained markdown record per LOST board.

Round 18 does not hunt for defects.  It manufactures an agreement for every
board we lose, so the input an expert gets has to be complete enough to judge
the board without re-running anything:

  * the deal, dealer, vulnerability and par
  * BOTH auctions, seat by seat, with the DECIDING rule id for every call of
    ours (`sweep.deciding_rule`, not `explanation.source_rule_id`, which is the
    primary reading and has produced two false findings)
  * the full 20-entry double-dummy table, so the expert can see what was there
  * for every call of ours, what BEN would have called from that seat with the
    same cards and the same auction, and how confident it was
  * for the FIRST call where we diverged from BEN, the whole candidate list out
    of `repro.rank()` - rule id, fit, blended score, priority - so a proposal
    can be priced against the rungs it would outrank

    python3 tools/roundkit/dossier.py --rows reports/r18_before.jsonl \
                                      --out docs/dossier_575757 --chunk 40
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "tools" / "roundkit"))

from compare_ben import Ben                      # noqa: E402  (cached BEN)
from repro import rank, seat_of                  # noqa: E402
from sweep import deciding_rule                  # noqa: E402

from bridgebidder.domain.cards import Hand       # noqa: E402
from bridgebidder.domain.types import Seat       # noqa: E402
from bridgebidder.engine.dd import EndplayDD     # noqa: E402

SEATS = "NESW"
STRAINS = ("C", "D", "H", "S", "NT")
VUL_NS = {"None": 0, "NS": 1, "EW": 0, "Both": 1}
VUL_EW = {"None": 0, "NS": 0, "EW": 1, "Both": 1}


def dd_table(dd, row):
    deal = {s: Hand.parse(row["hands"][s.value]) for s in Seat}
    return {(s.value, st): dd.tricks(deal, s, st) for s in Seat for st in STRAINS}


def fmt_dd(tab):
    out = ["| declarer | C | D | H | S | NT |", "|---|---|---|---|---|---|"]
    for s in SEATS:
        out.append("| " + s + " | " + " | ".join(str(tab[(s, st)]) for st in STRAINS) + " |")
    return "\n".join(out)


def our_side(table):
    return "NS" if table == "a" else "EW"


def board_record(row, dd, ben, want_rank=True):
    """One markdown record for one lost board."""
    b = row["board"]
    L = []
    L.append(f"## Board {b} — margin {row['imp_margin']:+d} IMPs")
    L.append("")
    L.append(f"dealer **{row['dealer']}**, vul **{row['vul']}**, "
             f"par(N/S) **{row['par_ns']:+d}**" if row["par_ns"] is not None
             else f"dealer **{row['dealer']}**, vul **{row['vul']}**, par unknown")
    L.append("")
    for s in SEATS:
        h = Hand.parse(row["hands"][s])
        L.append(f"    {s}  {row['hands'][s]}   ({h.hcp} HCP)")
    L.append("")
    tab = dd_table(dd, row)
    L.append("Double-dummy tricks:")
    L.append("")
    L.append(fmt_dd(tab))
    L.append("")
    L.append(f"Table A (**we are N/S**): {row['a_contract']}, N/S score {row['a_score_ns']:+d}  ")
    L.append(f"Table B (**we are E/W**): {row['b_contract']}, N/S score {row['b_score_ns']:+d}  ")
    L.append(f"IMP margin for us: **{row['imp_margin']:+d}**")
    L.append("")

    first_div = None
    for table in ("a", "b"):
        calls = row[f"{table}_auction"].split()
        ours = {c["n"]: c for c in row[f"{table}_our_calls"]}
        L.append(f"### Table {table.upper()} — we are {our_side(table)}, "
                 f"BEN is {'EW' if table == 'a' else 'NS'}")
        L.append("")
        L.append("| # | seat | call | whose | deciding rule | BEN would call |")
        L.append("|---|---|---|---|---|---|")
        seen_div = False
        for i, c in enumerate(calls):
            who = seat_of(row, table, i)
            mine = i in ours
            rule, benstr = "", ""
            if mine:
                rule = ours[i]["rule"] or "*(code fallback)*"
                try:
                    resp = ben.ask({"hands": row["hands"], "dealer": row["dealer"],
                                    "vuln_ns": VUL_NS[row["vul"]],
                                    "vuln_ew": VUL_EW[row["vul"]],
                                    "auction": calls[:i]})
                    bb = resp.get("bid")
                    conf = (resp.get("top") or [[None, 0.0]])[0][1]
                    benstr = f"{bb} ({conf:.2f})"
                    if bb != c:
                        benstr += " **≠**"
                        if not seen_div:
                            seen_div = True
                            benstr += " ← FIRST DIVERGENCE"
                            if first_div is None:
                                first_div = (table, i, who)
                except Exception as e:                       # BEN worker trouble
                    benstr = f"(ben error {e})"
            L.append(f"| {i} | {who} | {c} | {'US' if mine else 'BEN'} | "
                     f"{rule} | {benstr} |")
        L.append("")

    if want_rank and first_div is not None:
        table, i, who = first_div
        calls = row[f"{table}_auction"].split()
        L.append(f"### First divergence: table {table.upper()}, call {i}, seat {who}")
        L.append("")
        L.append(f"auction so far: `{' '.join(calls[:i]) or '(opening)'}`, "
                 f"hand `{row['hands'][who]}`")
        L.append("")
        try:
            cands = rank(row["hands"][who], row["dealer"], row["vul"], who,
                         calls[:i], top=14)
            dec = deciding_rule(cands) if cands else None
            L.append("| call | rule | fit | score | prio | shows |")
            L.append("|---|---|---|---|---|---|")
            for c in cands:
                mark = " **← DECIDED**" if dec is c else ""
                shows = (c["shows"] or "").replace("|", "/")[:70]
                L.append(f"| {c['call']} | {c['rule']}{mark} | {c['fit']:.3f} | "
                         f"{c['score']:.3f} | {c['prio']} | {shows} |")
        except Exception as e:
            L.append(f"(candidate list unavailable: {e})")
        L.append("")
    L.append("---")
    L.append("")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows", required=True)
    ap.add_argument("--out", required=True, help="output directory")
    ap.add_argument("--chunk", type=int, default=40)
    ap.add_argument("--max-margin", type=int, default=0,
                    help="include boards with imp_margin < this (default 0)")
    a = ap.parse_args()

    rows = [json.loads(l) for l in open(a.rows)]
    lost = [r for r in rows if r["imp_margin"] < a.max_margin]
    lost.sort(key=lambda r: r["imp_margin"])          # worst first
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)

    dd, ben = EndplayDD(), Ben()
    t0 = time.time()
    chunks: list[list[str]] = []
    for k, r in enumerate(lost):
        if k % a.chunk == 0:
            chunks.append([])
        chunks[-1].append(board_record(r, dd, ben))
        if (k + 1) % 20 == 0:
            print(f"  {k + 1}/{len(lost)} boards, {time.time() - t0:.0f}s", flush=True)
    ben.close()

    tot = sum(r["imp_margin"] for r in lost)
    index = [f"# Lost boards, {Path(a.rows).name} — {len(lost)} boards, {tot:+d} IMPs",
             "",
             f"Whole match: {len(rows)} boards, "
             f"{sum(r['imp_margin'] for r in rows):+d} IMPs.",
             "", "| chunk | boards | IMPs |", "|---|---|---|"]
    for ci, ch in enumerate(chunks, 1):
        lo = (ci - 1) * a.chunk
        part = lost[lo:lo + a.chunk]
        name = f"part{ci:02d}.md"
        head = (f"# Lost boards part {ci} of {len(chunks)} "
                f"({len(part)} boards, {sum(p['imp_margin'] for p in part):+d} IMPs)\n\n"
                "Sorted worst-first across the whole match.\n\n")
        (out / name).write_text(head + "\n".join(ch))
        index.append(f"| [{name}]({name}) | {len(part)} | "
                     f"{sum(p['imp_margin'] for p in part):+d} |")
    (out / "index.md").write_text("\n".join(index) + "\n")
    print(f"{len(lost)} lost boards ({tot:+d} IMPs) -> {out} "
          f"in {len(chunks)} parts, {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
