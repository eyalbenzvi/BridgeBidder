#!/usr/bin/env python3
"""Compare our engine's bidding against BEN's, decision by decision.

BEN is a neural bidder trained on a large corpus of expert auctions.  It is
explicitly NOT a source of truth - it is statistical, it has no explanations,
and it is sometimes wrong.  What it provides is something no double-dummy
oracle can: an opinion about what an *expert human partnership* would bid,
which is exactly the judgement our rulebook is trying to encode.

Method.  For each deal we play the auction with OUR engine.  At every one of
our decisions we ask BEN what it would call from the same seat with the same
hand and the same auction so far.  A disagreement is recorded together with
the rule that produced our call and BEN's confidence.

Reading the output.  A disagreement is a LEAD, not a verdict.  The useful
signal is a cluster: the same rule disagreeing the same way many times, with
BEN confident each time, is worth investigating.  A one-off, or a
disagreement where BEN itself is unsure, is noise.

    python tools/compare_ben.py run --n 200 --seed 5 --out reports/ben.jsonl
    python tools/compare_ben.py report --rows reports/ben.jsonl
"""

from __future__ import annotations

import argparse
import json
import random
import subprocess
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from bridgebidder.domain.auction import Auction
from bridgebidder.domain.cards import FULL_DECK, Hand
from bridgebidder.domain.types import Seat, Vulnerability
from bridgebidder.engine.selfplay import self_play
from bridgebidder.inference.engine import analyze
from bridgebidder.system.dsl import load_system

BEN_PYTHON = "/tmp/benenv/bin/python"
BEN_WORKER = str(Path(__file__).resolve().parent / "ben_worker.py")
VULS = [Vulnerability.NONE, Vulnerability.NS, Vulnerability.EW, Vulnerability.BOTH]


class Ben:
    """A persistent BEN worker process (model load is slow; keep it warm)."""

    def __init__(self):
        self.p = subprocess.Popen(
            [BEN_PYTHON, BEN_WORKER], stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, text=True, bufsize=1)

    def ask(self, req: dict) -> dict:
        self.p.stdin.write(json.dumps(req) + "\n")
        self.p.stdin.flush()
        return json.loads(self.p.stdout.readline())

    def close(self):
        self.p.stdin.close()
        self.p.wait(timeout=10)


def run(n: int, seed: int, out: Path) -> None:
    system = load_system()
    ben = Ben()
    rng = random.Random(seed)
    rows, agree, total = [], 0, 0
    t0 = time.time()

    for bi in range(n):
        deck = list(FULL_DECK)
        rng.shuffle(deck)
        deal = {s: Hand(deck[j * 13:(j + 1) * 13]) for j, s in enumerate(Seat)}
        dealer, vul = Seat.from_index(bi % 4), VULS[(bi // 4) % 4]
        hands = {s.value: str(deal[s]) for s in Seat}

        auction = self_play(system, deal, dealer, vul)
        analysis = analyze(system, auction)
        prefix: list[str] = []
        for ann in analysis.annotations:
            resp = ben.ask({
                "hands": hands, "dealer": dealer.value,
                "vuln_ns": int(vul.is_vulnerable(Seat.N)),
                "vuln_ew": int(vul.is_vulnerable(Seat.E)),
                "auction": prefix,
            })
            total += 1
            ours = str(ann.call)
            theirs = resp.get("bid")
            if theirs == ours:
                agree += 1
            else:
                interp = ann.interpretation
                rows.append({
                    "board": bi, "seat": ann.seat.value,
                    "dealer": dealer.value, "vul": vul.value,
                    "hands": hands,
                    "auction": " ".join(prefix) or "(open)",
                    "ours": ours, "ben": theirs,
                    "ben_conf": (resp.get("top") or [[None, 0]])[0][1],
                    "ben_top": resp.get("top"),
                    "rule": interp.source_rule_id,
                    "fallback": interp.is_fallback,
                    "shows": interp.shows_text,
                    "hand": hands[ann.seat.value],
                    "hcp": deal[ann.seat].hcp,
                })
            prefix.append(ours)

    ben.close()
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    print(f"{total} decisions over {n} boards in {time.time() - t0:.0f}s | "
          f"agreed {agree} ({100 * agree / total:.1f}%) | "
          f"{len(rows)} disagreements -> {out}")


def report(rows_path: Path, min_conf: float = 0.7, min_n: int = 4) -> None:
    rows = [json.loads(l) for l in open(rows_path)]
    confident = [r for r in rows if (r["ben_conf"] or 0) >= min_conf]
    print(f"disagreements: {len(rows)} | BEN confident (>= {min_conf:.0%}): {len(confident)}\n")

    clusters = defaultdict(list)
    for r in confident:
        clusters[(r["rule"], r["ours"], r["ben"])].append(r)

    print(f"=== clusters: same rule, same disagreement, BEN confident (n >= {min_n}) ===\n")
    ranked = sorted(clusters.items(), key=lambda kv: -len(kv[1]))
    shown = 0
    for (rule, ours, theirs), items in ranked:
        if len(items) < min_n:
            continue
        conf = sum(i["ben_conf"] for i in items) / len(items)
        print(f"  {len(items):3}x  we bid {ours:4} / BEN bids {theirs:4}  (BEN avg conf {conf:.0%})   rule {rule}")
        ex = items[0]
        print(f"        e.g. {ex['auction'][:44]:44} {ex['seat']}: {ex['hand']} ({ex['hcp']} HCP)")
        print(f"        ours means: {ex['shows'][:70]}")
        shown += 1
        if shown >= 12:
            break
    if not shown:
        print("  (no cluster reached the threshold)")

    print("\n=== our rules by number of confident disagreements ===")
    byrule = Counter(r["rule"] for r in confident)
    for rule, c in byrule.most_common(10):
        print(f"  {c:4}  {rule}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run")
    r.add_argument("--n", type=int, default=100)
    r.add_argument("--seed", type=int, default=5)
    r.add_argument("--out", type=Path, required=True)
    p = sub.add_parser("report")
    p.add_argument("--rows", type=Path, required=True)
    p.add_argument("--min-conf", type=float, default=0.7)
    p.add_argument("--min-n", type=int, default=4)
    a = ap.parse_args()
    if a.cmd == "run":
        run(a.n, a.seed, a.out)
    else:
        report(a.rows, a.min_conf, a.min_n)
