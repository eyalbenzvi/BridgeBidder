#!/usr/bin/env python3
"""Where the engine has NO AGREEMENT: the two populations nobody has ruled on.

Round 15 ended at the same held-out number it started at.  The per-decision BEN
audit finds rule-level defects and the rule-level defects are gone; what is left
is not a bad rule but the ABSENCE of one.  This tool measures that directly, and
it needs no oracle: a hole is a hole whatever BEN thinks.

Two populations, both computed straight from the engine:

  FALLBACK  - no system rule covered the call at all, so `generate_fallbacks`
              invented a generic candidate.  Round 15 measured this at 4.4% of
              every call we make, at a par gap of -3.89 against a stage-matched
              +0.46: about -2,000 attributable gap-points, larger than every
              named rule family combined.  Grouped by (context, call) this is a
              map of every hole in the file, ranked by what the hole costs.

  UNCLEAR   - `fast_decision` returns is_clear=False when two candidates fit
              >= 0.9 at the SAME priority, i.e. the call was settled by a static
              number that sees neither the hand nor the auction.  `match_ben.py`
              calls `decide_fast`, which discards the flag, so every match number
              this project has ever produced is fast-path-only and this
              population has never been looked at.  `choose(use_arbitration=True)`
              already rolls candidates out and double-dummy-scores them; this
              tells us how often that would even be consulted, and what the
              coin flips cost.

Both are reported against a STAGE-MATCHED baseline - decisions at the same depth
in the auction - because the corpus mean par gap is a mixture that runs from
-0.34 early to well over +1 by the sixth call, so comparing a late-auction slice
to it flatters the slice.

    python3 tools/roundkit/holes.py --rows reports/e10_final.jsonl --scan --out reports/e10_holes.json
    python3 tools/roundkit/holes.py --cache reports/e10_holes.json --fallbacks
    python3 tools/roundkit/holes.py --cache reports/e10_holes.json --unclear
    python3 tools/roundkit/holes.py --cache reports/e10_holes.json --hole general_competitive_low 3H
"""
from __future__ import annotations

import argparse, json, sys, time
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))

from bridgebidder.domain.auction import Auction            # noqa: E402
from bridgebidder.domain.calls import Call                 # noqa: E402
from bridgebidder.domain.cards import Hand                 # noqa: E402
from bridgebidder.domain.types import Seat, Vulnerability  # noqa: E402
from bridgebidder.engine.decision import fast_decision     # noqa: E402
from bridgebidder.inference.engine import prepare_decision  # noqa: E402
from bridgebidder.system.dsl import load_system            # noqa: E402

SEATS = "NESW"


def _contexts(setup):
    """The live contexts, in the order their rules appear as candidates."""
    seen = []
    for cand in setup.candidates:
        cid = getattr(cand.rule, "context_id", None) if cand.rule is not None else None
        if cid and cid not in seen:
            seen.append(cid)
    return seen


def our_gap(row, table):
    """The par gap FOR US at this table, correctly signed (N/S-signed at both)."""
    return row["a_par_gap"] if table == "a" else -row["b_par_gap"]


def scan(rows_path, out_path):
    sysm = load_system()
    rows = [json.loads(l) for l in open(rows_path)]
    recs, t0 = [], time.time()
    for k, r in enumerate(rows):
        for t in ("a", "b"):
            calls = r[f"{t}_auction"].split()
            for oc in r[f"{t}_our_calls"]:
                i = oc["n"]
                if i >= len(calls):
                    continue
                seat = SEATS[(SEATS.index(r["dealer"]) + i) % 4]
                a = Auction(dealer=Seat(r["dealer"]),
                            vulnerability=Vulnerability.parse(r["vul"]))
                for c in calls[:i]:
                    a.add(Call.parse(c))
                try:
                    setup = prepare_decision(sysm, a, perspective=Seat(seat))
                    choice, ranked, clear = fast_decision(setup, Hand.parse(r["hands"][seat]))
                except Exception:
                    continue
                rule = choice.candidate.rule.id if choice.candidate.rule else None
                # the rivals that made it unclear: same priority, also fitting
                rivals = [str(sc.call) for sc in ranked
                          if sc.fit >= 0.9 and str(sc.call) != str(choice.call)
                          and abs(sc.candidate.priority - choice.candidate.priority) < 1e-9]
                recs.append(dict(
                    board=r["board"], table=t, index=i, seat=seat,
                    hand=r["hands"][seat], call=str(choice.call),
                    rule=rule, fallback=rule is None, clear=bool(clear),
                    fit=round(choice.fit, 3), prio=choice.candidate.priority,
                    contexts=_contexts(setup),
                    rivals=rivals, imp=r["imp_margin"], gap=our_gap(r, t),
                    auction=" ".join(calls[:i]),
                ))
        if k % 100 == 0:
            print(f"  ...{k}/{len(rows)} boards ({time.time()-t0:.0f}s)", file=sys.stderr)
    Path(out_path).write_text(json.dumps(recs))
    print(f"{len(recs)} decisions -> {out_path}")
    return recs


def stage_baseline(recs):
    """Mean par gap by auction depth: the only fair yardstick for a slice."""
    by = defaultdict(list)
    for d in recs:
        by[d["index"]].append(d["gap"])
    return {k: sum(v) / len(v) for k, v in by.items()}


def _summary(recs, sel, label):
    base = stage_baseline(recs)
    n = len(sel)
    if not n:
        print(f"{label}: none")
        return
    gap = sum(d["gap"] for d in sel) / n
    exp = sum(base[d["index"]] for d in sel) / n
    imp = sum(d["imp"] for d in sel) / n
    allimp = sum(d["imp"] for d in recs) / len(recs)
    print(f"{label}: {n} of {len(recs)} decisions ({n/len(recs)*100:.1f}%)")
    print(f"  our par gap {gap:+.2f}   stage-matched baseline {exp:+.2f}   "
          f"DELTA {gap-exp:+.2f}")
    print(f"  board margin {imp:+.2f}/decision   (corpus {allimp:+.2f})")
    print(f"  total attributable gap {(gap-exp)*n:+.0f} points\n")


def _group(recs, sel, keyfn, limit, header):
    base = stage_baseline(recs)
    g = defaultdict(list)
    for d in sel:
        g[keyfn(d)].append(d)
    rows = []
    for key, ds in g.items():
        gap = sum(d["gap"] for d in ds) / len(ds)
        exp = sum(base[d["index"]] for d in ds) / len(ds)
        rows.append(((gap - exp) * len(ds), key, len(ds), gap, exp,
                     sum(d["imp"] for d in ds) / len(ds)))
    rows.sort()
    print(header)
    print(f"{'context / call':52s} {'n':>4s} {'gap':>7s} {'stage':>7s} {'DELTA':>7s} {'imp':>6s} {'TOTAL':>8s}")
    print("-" * 100)
    for tot, key, n, gap, exp, imp in rows[:limit]:
        print(f"{str(key)[:52]:52s} {n:4d} {gap:+7.2f} {exp:+7.2f} {gap-exp:+7.2f} {imp:+6.2f} {tot:+8.0f}")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--rows")
    p.add_argument("--scan", action="store_true")
    p.add_argument("--out")
    p.add_argument("--cache")
    p.add_argument("--fallbacks", action="store_true")
    p.add_argument("--unclear", action="store_true")
    p.add_argument("--hole", nargs=2, metavar=("CONTEXT", "CALL"))
    p.add_argument("--limit", type=int, default=30)
    a = p.parse_args()

    if a.scan:
        recs = scan(a.rows, a.out)
    else:
        recs = json.loads(Path(a.cache).read_text())

    if a.fallbacks:
        sel = [d for d in recs if d["fallback"]]
        _summary(recs, sel, "FALLBACK (no rule covered the call)")
        _group(recs, sel, lambda d: f"{d['contexts'][0] if d['contexts'] else '-'} -> {d['call']}",
               a.limit, "Holes, worst total cost first:")
    if a.unclear:
        sel = [d for d in recs if not d["clear"]]
        _summary(recs, sel, "UNCLEAR (settled by a static priority tie)")
        _group(recs, sel, lambda d: f"{d['contexts'][0] if d['contexts'] else '-'} -> "
                                    f"{d['call']} vs {'/'.join(d['rivals'][:2])}",
               a.limit, "Coin flips, worst total cost first:")
    if a.hole:
        ctx, call = a.hole
        sel = [d for d in recs
               if d["call"] == call and d["contexts"] and d["contexts"][0] == ctx]
        print(f"{ctx} -> {call}: {len(sel)} decisions\n")
        for d in sorted(sel, key=lambda d: d["gap"])[:a.limit]:
            print(f"  {d['board']}{d['table']} n={d['index']:<2d} {d['seat']} {d['hand']:18s} "
                  f"({d['imp']:+3d} gap{d['gap']:+5.1f}) {d['auction'] or '-':<30s} -> {d['call']}"
                  f"{'  [fallback]' if d['fallback'] else ''}{'' if d['clear'] else '  [unclear]'}")


if __name__ == "__main__":
    main()
