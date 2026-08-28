#!/usr/bin/env python3
"""Counterfactual decision regret: learn from mistakes at the DECISION level.

The par-based harvester judges the final contract against an omniscient
oracle, which conflates bad bidding with unknowable contracts and attributes
a whole board to nothing in particular.  This measures something different
and directly actionable:

    at each position the engine faced, would a different legal call have
    scored better on this actual deal?

For every decision we replay the auction forward once per candidate call
(engine in all four seats), score the resulting contract double-dummy, and
record the paired difference against the call actually chosen.  Rows are
tagged with the rule that made the decision, so regret aggregates into a
ranked list of which RULES cost IMPs.

Two design points matter for soundness:

* We never take the max over alternatives per decision.  Max-of-noisy-
  estimates is optimistically biased and would "discover" that lying pays
  whenever partner happens to be misled favourably.  Instead each
  (rule, alternative) pair is averaged across every occurrence, with a
  standard error, so single-deal luck cancels.
* Only systemically plausible alternatives are considered (fit floor), for
  the same reason: a double-dummy rollout rewards a lie because partner then
  bids as though the lie were true.

    python tools/regret.py run  --corpus reports/train.pkl --out reports/regret.jsonl
    python tools/regret.py report --rows reports/regret.jsonl
"""

from __future__ import annotations

import argparse
import json
import math
import pickle
import sys
import time
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from bridgebidder.domain.auction import Auction
from bridgebidder.domain.calls import Call
from bridgebidder.domain.cards import Hand
from bridgebidder.domain.types import Seat, Vulnerability
from bridgebidder.engine.decision import score_candidates
from bridgebidder.engine.scoring import imps, signed_score
from bridgebidder.engine.selfplay import self_play
from bridgebidder.inference.engine import interpret_call, prepare_decision
from bridgebidder.system.dsl import load_system

# an alternative must be systemically plausible to count: rolling out a call
# the hand cannot hold measures the value of deceiving partner, not of bidding
MIN_ALT_FIT = 0.35
MAX_ALTS = 4

VULS = {v.value: v for v in Vulnerability}


def _finish(system, deal, dealer, vul, prefix_calls, first_call):
    """Play the real deal out from this position after `first_call`."""
    au = Auction(dealer=dealer, vulnerability=vul)
    for c in prefix_calls:
        au.add(Call.parse(c))
    au.add(first_call)
    return self_play(system, deal, dealer, vul, start=au)


def run(corpus_path: Path, out: Path, limit: int | None = None) -> None:
    system = load_system()
    boards = pickle.load(open(corpus_path, "rb"))
    if limit:
        boards = boards[:limit]
    rows = []
    t0 = time.time()

    for bi, b in enumerate(boards):
        deal = {Seat(k): Hand.parse(v) for k, v in b["hands"].items()}
        dealer, vul = Seat(b["dealer"]), VULS[b["vul"]]
        actual = self_play(system, deal, dealer, vul)
        prefix: list[str] = []

        for call in actual.calls:
            au = Auction(dealer=dealer, vulnerability=vul)
            for c in prefix:
                au.add(Call.parse(c))
            seat = au.next_seat
            side = seat.side
            setup = prepare_decision(system, au, perspective=seat)
            ranked = score_candidates(setup, deal[seat])

            chosen = next((s for s in ranked if str(s.call) == str(call)), None)
            alts = [s for s in ranked
                    if str(s.call) != str(call) and s.fit >= MIN_ALT_FIT][:MAX_ALTS]
            if chosen is not None and alts:
                fin = _finish(system, deal, dealer, vul, prefix, call)
                c0 = fin.contract
                t0_ = b["tricks"][(c0.declarer.value, c0.strain)] if c0 else 0
                base = signed_score(c0, t0_, vul, side)
                interp = interpret_call(setup, call)
                for a in alts:
                    fa = _finish(system, deal, dealer, vul, prefix, a.call)
                    ca = fa.contract
                    ta = b["tricks"][(ca.declarer.value, ca.strain)] if ca else 0
                    alt_score = signed_score(ca, ta, vul, side)
                    rows.append({
                        "board": bi,
                        "seat": seat.value,
                        "auction": " ".join(prefix) or "(open)",
                        "rule": interp.source_rule_id,
                        "context": interp.primary_rule.context_id if interp.primary_rule else "fallback",
                        "chosen": str(call),
                        "alt": str(a.call),
                        "chosen_fit": round(chosen.fit, 3),
                        "alt_fit": round(a.fit, 3),
                        "delta_imps": imps(alt_score - base),
                        "chosen_contract": str(c0) if c0 else "passed_out",
                        "alt_contract": str(ca) if ca else "passed_out",
                    })
            prefix.append(str(call))

    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    print(f"{len(rows)} counterfactual comparisons over {len(boards)} boards "
          f"in {time.time() - t0:.0f}s -> {out}")


def _stats(vals):
    n = len(vals)
    m = sum(vals) / n
    sd = math.sqrt(sum((v - m) ** 2 for v in vals) / (n - 1)) if n > 1 else 0.0
    return m, sd / math.sqrt(n) if n else 0.0, n


def report(rows_path: Path, min_n: int = 8) -> None:
    rows = [json.loads(l) for l in open(rows_path)]
    by_rule_alt = defaultdict(list)
    by_rule = defaultdict(list)
    for r in rows:
        by_rule_alt[(r["rule"], r["chosen"], r["alt"])].append(r["delta_imps"])
        by_rule[r["rule"]].append(r["delta_imps"])

    print(f"comparisons: {len(rows)} | distinct rules: {len(by_rule)}\n")
    print("=== RULES that are systematically beaten by their alternatives ===")
    print("(mean IMPs an average alternative gains over the rule's own call;")
    print(" significant at 2 standard errors, n >= %d)\n" % min_n)
    findings = []
    for rule, vals in by_rule.items():
        m, se, n = _stats(vals)
        if n >= min_n and m > 2 * se:
            findings.append((m, se, n, rule))
    for m, se, n, rule in sorted(findings, reverse=True):
        # which alternative is doing the beating?
        best = sorted(
            ((_stats(v)[0], _stats(v)[2], c, a)
             for (r, c, a), v in by_rule_alt.items() if r == rule and len(v) >= 3),
            reverse=True)[:2]
        detail = "; ".join(f"{c} -> {a} +{bm:.1f} (n={bn})" for bm, bn, c, a in best)
        print(f"  +{m:5.2f} +/- {se:4.2f} IMPs  n={n:3}  {rule}")
        if detail:
            print(f"         {detail}")
    if not findings:
        print("  (none significant)")

    print("\n=== rules that hold up well (alternatives do WORSE) ===")
    good = [(m, se, n, r) for r, v in by_rule.items()
            for m, se, n in [_stats(v)] if n >= min_n and m < -2 * se]
    for m, se, n, rule in sorted(good)[:6]:
        print(f"  {m:+5.2f} +/- {se:4.2f} IMPs  n={n:3}  {rule}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run")
    r.add_argument("--corpus", type=Path, required=True)
    r.add_argument("--out", type=Path, required=True)
    r.add_argument("--limit", type=int)
    p = sub.add_parser("report")
    p.add_argument("--rows", type=Path, required=True)
    p.add_argument("--min-n", type=int, default=8)
    a = ap.parse_args()
    if a.cmd == "run":
        run(a.corpus, a.out, a.limit)
    else:
        report(a.rows, a.min_n)
