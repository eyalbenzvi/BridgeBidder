"""How often does the system actually KNOW what to bid?

Sixteen rounds have been spent editing a 2,344-rule system a rung at a time.
Round 17's measurements say that mode of work has stopped paying: every
single-rung intervention it made measured indistinguishable from zero, and the
unbiased ablation of rounds 11-16 is in `docs/ROUND_17_REPORT.md`.

The hypothesis this tool tests is different and much simpler: **the system is
too small.**  Not wrong in places - under-specified everywhere - so that a
large fraction of its decisions are not made by an agreement at all.

Every decision falls into exactly one of three buckets:

  KNOWS      an authored rule fits >= 0.9 and wins.  The partnership has an
             agreement covering this hand in this auction.
  GUESSES    a rule wins but fits < 0.9 - the soft-miss lottery.  Nothing in
             the file describes the hand, so the blended score picks the
             least-bad misfit.  Partner then reads it as the rule it isn't.
  NOTHING    the code fallback decides: no rule exists for this call here.

GUESSES and NOTHING together are the authoring backlog, and grouping them by
context ranks it: a context with many of them is a subject where the file has
run out of vocabulary, and the repair is more rules, not a better rule.

    python3 tools/roundkit/coverage.py reports/held_final.jsonl [--top 25]
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from repro import seat_of, system                                # noqa: E402
from bridgebidder.domain.auction import Auction                  # noqa: E402
from bridgebidder.domain.calls import Call                       # noqa: E402
from bridgebidder.domain.cards import Hand                       # noqa: E402
from bridgebidder.domain.types import Seat, Vulnerability        # noqa: E402
from bridgebidder.engine.decision import fast_decision           # noqa: E402
from bridgebidder.inference.engine import prepare_decision       # noqa: E402

FAST_PATH = 0.9


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("rows")
    ap.add_argument("--top", type=int, default=25)
    ap.add_argument("--live-only", action="store_true",
                    help="drop calls that merely end an auction already over")
    a = ap.parse_args()

    sysm = system()
    rows = [json.loads(l) for l in open(a.rows)]
    buckets = Counter()
    by_ctx: dict[str, Counter] = defaultdict(Counter)
    alts = Counter()

    for r in rows:
        dealer = Seat(r["dealer"])
        vul = Vulnerability.parse(r["vul"])
        for t in ("a", "b"):
            calls = r[f"{t}_auction"].split()
            for oc in r[f"{t}_our_calls"]:
                i = oc["n"]
                if i >= len(calls):
                    continue
                if a.live_only and all(c == "P" for c in calls[i:]):
                    continue          # a closing pass explains nothing
                s = seat_of(r, t, i)
                au = Auction(dealer=dealer, vulnerability=vul)
                for c in calls[:i]:
                    au.add(Call.parse(c))
                setup = prepare_decision(sysm, au, perspective=Seat(s))
                hand = Hand.parse(r["hands"][s])
                choice, _ranked, _clear = fast_decision(setup, hand)
                cand = choice.candidate
                ctx = (cand.rule.context_id if cand.rule is not None
                       else "(code fallback)")
                if cand.rule is None:
                    b = "NOTHING"
                elif choice.fit < FAST_PATH:
                    b = "GUESSES"
                elif cand.rule.requires.is_trivial:
                    # `requires: {}` fits 1.00 against every hand, so a
                    # catch-all pass or an unconditioned sign-off scores as a
                    # perfect fit while describing nothing.  Counting those as
                    # KNOWS is what makes an under-specified file look covered:
                    # they are the starved seats, not the agreements.
                    b = "VACUOUS"
                else:
                    b = "KNOWS"
                buckets[b] += 1
                by_ctx[ctx][b] += 1
                # how much choice did the seat actually have?
                n_fit = sum(1 for c in setup.candidates
                            if c.rule is not None)
                alts[min(n_fit, 9)] += 1

    n = sum(buckets.values())
    print(f"\n=== {a.rows}: {n} of our decisions "
          f"{'(live only)' if a.live_only else ''} ===\n")
    for b in ("KNOWS", "VACUOUS", "GUESSES", "NOTHING"):
        print(f"  {b:9s} {buckets[b]:6d}  {100 * buckets[b] / n:5.1f}%")
    backlog = buckets["GUESSES"] + buckets["NOTHING"] + buckets["VACUOUS"]
    print(f"\n  the authoring backlog (VACUOUS + GUESSES + NOTHING): {backlog} "
          f"({100 * backlog / n:.1f}% of decisions)")
    print(f"  of which VACUOUS - a rule fits 1.00 because it requires nothing: "
          f"{buckets['VACUOUS']}")

    print("\n  authored rules offered at the seat (any fit):")
    for k in sorted(alts):
        label = f"{k}" if k < 9 else "9+"
        print(f"    {label:>3} rules: {alts[k]:6d}  {100 * alts[k] / n:5.1f}%")

    print(f"\n=== the backlog, by context (top {a.top}) ===")
    print("  a context high on this list is a subject where the file has run")
    print("  out of vocabulary; the repair is MORE RULES, not a better rule.\n")
    ranked = sorted(by_ctx.items(),
                    key=lambda kv: -(kv[1]["GUESSES"] + kv[1]["NOTHING"]
                                     + kv[1]["VACUOUS"]))
    print(f"  {'context':46s} {'vacuous':>8} {'guess':>6} {'none':>6} {'knows':>6}")
    for ctx, c in ranked[:a.top]:
        if not (c["GUESSES"] + c["NOTHING"] + c["VACUOUS"]):
            break
        print(f"  {ctx:46s} {c['VACUOUS']:>8} {c['GUESSES']:>6} "
              f"{c['NOTHING']:>6} {c['KNOWS']:>6}")


if __name__ == "__main__":
    main()
