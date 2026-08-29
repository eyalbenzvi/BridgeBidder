#!/usr/bin/env python3
"""Per-DECISION audit of a played match: where did BEN, in our exact seat,
with our exact cards, after our exact auction, make a different call?

Why this exists.  `triage_match.py` clusters losing boards by the rule that
made our LAST bid.  That attribution is correlational and it has spent five
rounds pointing at the same generic terminal rules (`uc_nt3`, `all-pass`,
`uc_raise_*`), every one of which was re-scored across the whole corpus and
ruled NOT a defect.  The rule that is the last bid on a bad board is usually
the rule that had to speak after the damage was already done.

This tool asks a sharper question.  For every call WE made on a board we LOST,
BEN is asked what it would call from the same seat, holding the same thirteen
cards, after the identical auction.  That is a controlled comparison: one
decision, two bidders, everything else held fixed.

Two things make the output more useful than a disagreement count:

  * **IMPs at stake.**  A disagreement on a board we lost by 13 matters more
    than one on a board we lost by 1, so decisions are weighted by the board's
    margin rather than merely counted.
  * **First divergence.**  Once our call differs from BEN's, every later
    decision in that auction is conditioned on our own earlier choice, and
    BEN's later opinions are answers to a different question.  The FIRST
    confident disagreement in an auction is the causally meaningful one; the
    rest are downstream.  They are marked, and ranked separately.

BEN is not a source of truth - it is statistical and sometimes wrong.  A
disagreement is a LEAD.  What earns investigation is a decision where BEN is
confident, the board was lost, and the divergence came first.

    python3 tools/ben_audit.py run  --rows reports/e9_before.jsonl \
                                    --out  reports/ben_audit.jsonl
    python3 tools/ben_audit.py report --rows reports/ben_audit.jsonl
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

BEN_PYTHON = "/tmp/benenv/bin/python"
BEN_WORKER = str(Path(__file__).resolve().parent / "ben_worker.py")

VUL_NS = {"None": 0, "NS": 1, "EW": 0, "Both": 1}
VUL_EW = {"None": 0, "NS": 0, "EW": 1, "Both": 1}


class Ben:
    """A persistent BEN worker (model load is slow; keep it warm)."""

    def __init__(self) -> None:
        self.p = subprocess.Popen(
            [BEN_PYTHON, BEN_WORKER], stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, text=True, bufsize=1)

    def ask(self, req: dict) -> dict:
        self.p.stdin.write(json.dumps(req) + "\n")
        self.p.stdin.flush()
        return json.loads(self.p.stdout.readline())

    def close(self) -> None:
        self.p.stdin.close()
        self.p.wait(timeout=10)


def run(rows_path: Path, out: Path, min_loss: int) -> None:
    rows = [json.loads(l) for l in open(rows_path)]
    lost = [r for r in rows if r["imp_margin"] <= -min_loss]
    ben = Ben()
    out_rows: list[dict] = []
    asked = 0
    t0 = time.time()

    for r in lost:
        for table in ("a", "b"):
            calls = r[f"{table}_auction"].split()
            seen_divergence = False
            for oc in r[f"{table}_our_calls"]:
                i = oc["n"]
                if i >= len(calls):
                    continue
                resp = ben.ask({
                    "hands": r["hands"],
                    "dealer": r["dealer"],
                    "vuln_ns": VUL_NS[r["vul"]],
                    "vuln_ew": VUL_EW[r["vul"]],
                    "auction": calls[:i],
                })
                asked += 1
                ours, theirs = oc["call"], resp.get("bid")
                if theirs == ours:
                    continue
                conf = (resp.get("top") or [[None, 0.0]])[0][1]
                out_rows.append({
                    "board": r["board"], "table": table, "index": i,
                    "seat": oc["seat"], "hand": r["hands"][oc["seat"]],
                    "dealer": r["dealer"], "vul": r["vul"],
                    "auction": " ".join(calls[:i]) or "(open)",
                    "full_auction": r[f"{table}_auction"],
                    "ours": ours, "rule": oc["rule"] or "fallback",
                    "ben": theirs, "ben_conf": conf,
                    "ben_top": resp.get("top"),
                    "imp_margin": r["imp_margin"],
                    "contract": r[f"{table}_contract"],
                    "par_ns": r["par_ns"],
                    "first_divergence": not seen_divergence,
                })
                seen_divergence = True

        if len(out_rows) and len(out_rows) % 200 < 3:
            print(f"  {asked} decisions asked, {len(out_rows)} disagreements, "
                  f"{time.time() - t0:.0f}s", flush=True)

    ben.close()
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w") as f:
        for row in out_rows:
            f.write(json.dumps(row) + "\n")
    print(f"\n{len(lost)} losing boards, {asked} of our decisions replayed, "
          f"{len(out_rows)} disagreements ({100 * len(out_rows) / max(asked, 1):.1f}%) "
          f"in {time.time() - t0:.0f}s -> {out}")


def report(rows_path: Path, conf: float, top: int) -> None:
    rows = [json.loads(l) for l in open(rows_path)]
    strong = [r for r in rows if r["ben_conf"] >= conf]
    first = [r for r in strong if r["first_divergence"]]

    print(f"# BEN per-decision audit: {len(rows)} disagreements on losing boards, "
          f"{len(strong)} with BEN >= {conf:.2f} confident, "
          f"{len(first)} of them the FIRST divergence in their auction.\n")
    print("# The first divergence is the causally meaningful one: after it, every\n"
          "# later decision answers a different question.  Ranked by the IMPs on\n"
          "# the boards where it happened.\n")

    by_rule: dict[str, list[dict]] = defaultdict(list)
    for r in first:
        by_rule[r["rule"]].append(r)

    ranked = sorted(by_rule.items(),
                    key=lambda kv: sum(x["imp_margin"] for x in kv[1]))
    print("## RULES, by IMPs on boards where they made the FIRST call BEN "
          "confidently disagreed with\n")
    for rule, rs in ranked[:top]:
        imps = sum(x["imp_margin"] for x in rs)
        calls = defaultdict(int)
        for x in rs:
            calls[f"{x['ours']}->{x['ben']}"] += 1
        common = sorted(calls.items(), key=lambda kv: -kv[1])[:4]
        print(f"--- {rule}: {len(rs)} decisions, {imps:+d} IMPs on those boards, "
              f"mean {imps / len(rs):+.1f}")
        print(f"    we bid -> BEN bids: {dict(common)}")
        for x in sorted(rs, key=lambda y: y["imp_margin"])[:3]:
            print(f"      board {x['board']}{x['table']} ({x['imp_margin']:+d}) "
                  f"{x['seat']} {x['hand']}")
            print(f"        after: {x['auction']}")
            print(f"        we {x['ours']} ({x['rule']}) | BEN {x['ben']} "
                  f"conf {x['ben_conf']:.2f} | final {x['contract']}")
        print()

    print("\n## THE WORST INDIVIDUAL DECISIONS "
          "(first divergence, BEN confident, biggest losses)\n")
    for x in sorted(first, key=lambda y: y["imp_margin"])[:top]:
        print(f"board {x['board']}{x['table']} ({x['imp_margin']:+d} IMPs)  "
              f"{x['seat']} {x['hand']}  vul {x['vul']}")
        print(f"   auction: {x['auction']}")
        print(f"   WE {x['ours']:<4} ({x['rule']})   BEN {x['ben']:<4} "
              f"conf {x['ben_conf']:.2f}   top {[(c, round(p, 2)) for c, p in (x['ben_top'] or [])[:3]]}")
        print(f"   full: {x['full_auction']}  ->  {x['contract']}")
        print()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run")
    r.add_argument("--rows", type=Path, required=True)
    r.add_argument("--out", type=Path, required=True)
    r.add_argument("--min-loss", type=int, default=1)
    p = sub.add_parser("report")
    p.add_argument("--rows", type=Path, required=True)
    p.add_argument("--conf", type=float, default=0.80)
    p.add_argument("--top", type=int, default=20)
    a = ap.parse_args()
    if a.cmd == "run":
        run(a.rows, a.out, a.min_loss)
    else:
        report(a.rows, a.conf, a.top)
