"""What is actually available above our own game?

Before authoring a slam try, price one.  For every seat where we pass our own
side's game in an agreed major, this substitutes each plausible slam move,
finishes the auction with our engine in our seats and BEN in the opponents',
scores the contract double-dummy, and reports the change in the BOARD's IMP
margin - the number the match is actually decided on.

It answers three questions the corpus alone cannot:

  * is there money above our own game at all, or is passing right?
  * WHICH call collects it - and in particular whether a call whose answering
    seat is unauthored (a cue partner will simply pass) is a trap;
  * how big the population is, so the change can be priced before it is built.

The standing caveat is the same as cfr.py's: partner reads the substituted
call with the UNMODIFIED system, so this measures a unilateral deviation.  For
a call with an existing answering ladder (4NT) that is nearly the real thing;
for a call without one it measures the disaster of an unanswered force, which
is itself the finding.

    python3 tools/roundkit/slamprobe.py --rows reports/e10_final.jsonl --jobs 3
"""

from __future__ import annotations

import argparse
import json
import math
import statistics
import sys
import time
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

SEATS = "NESW"


def _slice(args):
    path, lo, hi, gate = args
    from cfr import _finish
    from compare_ben import Ben
    from bridgebidder.domain.auction import Auction
    from bridgebidder.domain.calls import Call
    from bridgebidder.domain.cards import Hand
    from bridgebidder.domain.types import Seat, Vulnerability
    from bridgebidder.engine.dd import EndplayDD
    from bridgebidder.engine.scoring import imps, signed_score
    from bridgebidder.evaluation.registry import evaluate
    from bridgebidder.inference.engine import prepare_decision
    from bridgebidder.system.dsl import load_system

    system, ben, dd = load_system(), Ben(), EndplayDD()
    rows, out = [json.loads(l) for l in open(path)][lo:hi], []

    for r in rows:
        deal = {s: Hand.parse(r["hands"][s.value]) for s in Seat}
        dealer, vul = Seat(r["dealer"]), Vulnerability.parse(r["vul"])
        for t, our_side in (("a", "NS"), ("b", "EW")):
            calls = r[f"{t}_auction"].split()
            other = r["b_score_ns"] if t == "a" else r["a_score_ns"]
            for oc in r[f"{t}_our_calls"]:
                i = oc["n"]
                if oc["call"] != "P" or i < 2 or i >= len(calls):
                    continue
                if calls[i - 1] != "P" or calls[i - 2] not in ("4H", "4S"):
                    continue
                M = calls[i - 2][1]
                me = SEATS[(SEATS.index(r["dealer"]) + i) % 4]
                if (SEATS.index(SEATS[(SEATS.index(r["dealer"]) + i - 2) % 4])
                        - SEATS.index(me)) % 4 != 2:
                    continue                      # the 4M is not partner's
                au0 = Auction(dealer=dealer, vulnerability=vul)
                for c in calls[:i]:
                    au0.add(Call.parse(c))
                setup = prepare_decision(system, au0, perspective=Seat(me))
                h = deal[Seat(me)]
                ev = setup.eval_ctx
                v = {k: evaluate(k, h, ev) for k in
                     ("controls", "ltc", f"lott_total_trumps({M})", f"keycards({M})")}
                if gate and not (v["controls"] >= 5 and v["ltc"] <= 6
                                 and v[f"lott_total_trumps({M})"] >= 8):
                    continue
                base_margin = r["imp_margin"]
                for cand in ("4NT", "5C", "5D", "5H", f"6{M}"):
                    call = Call.parse(cand)
                    if not au0.is_legal(call):
                        continue
                    au = Auction(dealer=dealer, vulnerability=vul)
                    for c in calls[:i]:
                        au.add(Call.parse(c))
                    au.add(call)
                    fin = _finish(system, ben, deal, dealer, vul, our_side, au)
                    c2 = fin.contract
                    if c2 is None:
                        s_ns = 0
                    else:
                        tricks = dd.tricks(deal, c2.declarer, c2.strain)
                        s_ns = signed_score(c2, tricks, vul, "NS")
                    new_margin = (imps(s_ns - other) if t == "a"
                                  else imps(other - s_ns))
                    out.append({
                        "board": r["board"], "table": t, "n": i, "seat": me,
                        "M": M, "hand": str(h), "sub": cand,
                        "auction_after": " ".join(str(c) for c in fin.calls),
                        "contract_after": str(c2) if c2 else "passed_out",
                        "base_margin": base_margin, "new_margin": new_margin,
                        "delta": new_margin - base_margin,
                        "controls": v["controls"], "ltc": v["ltc"],
                        "trumps": v[f"lott_total_trumps({M})"],
                        "keycards": v[f"keycards({M})"],
                    })
    ben.close()
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows", required=True)
    ap.add_argument("--out", default="")
    ap.add_argument("--jobs", type=int, default=3)
    ap.add_argument("--gate", action="store_true",
                    help="only the seats a controls/losers/trumps gate reaches")
    a = ap.parse_args()

    n = sum(1 for _ in open(a.rows))
    edges = [round(n * j / a.jobs) for j in range(a.jobs + 1)]
    slices = [(a.rows, edges[j], edges[j + 1], a.gate) for j in range(a.jobs)
              if edges[j] < edges[j + 1]]
    t0 = time.time()
    if len(slices) > 1:
        import multiprocessing as mp
        with mp.get_context("spawn").Pool(len(slices)) as pool:
            parts = pool.map(_slice, slices)
    else:
        parts = [_slice(s) for s in slices]
    rows = [x for p in parts for x in p]
    seats = len({(r["board"], r["table"], r["n"]) for r in rows})
    print(f"{seats} seats, {len(rows)} rollouts, {time.time() - t0:.0f}s")

    by = defaultdict(list)
    for r in rows:
        by[r["sub"]].append(r["delta"])
    print("\n  substitution   n    mean delta   SE     total")
    for k in sorted(by, key=lambda k: -sum(by[k])):
        v = by[k]
        se = statistics.stdev(v) / math.sqrt(len(v)) if len(v) > 1 else 0.0
        print(f"  {k:>6}      {len(v):4d}   {sum(v)/len(v):+7.2f}  "
              f"{se:5.2f}   {sum(v):+6d}")
    print("\n(delta is the change in the BOARD's IMP margin from making this")
    print(" call instead of passing our own game; positive = the move pays)")

    best = defaultdict(dict)
    for r in rows:
        best[(r["board"], r["table"], r["n"])][r["sub"]] = r
    if a.out:
        Path(a.out).parent.mkdir(parents=True, exist_ok=True)
        with open(a.out, "w") as f:
            for r in rows:
                f.write(json.dumps(r) + "\n")
        print(f"-> {a.out}")


if __name__ == "__main__":
    main()
