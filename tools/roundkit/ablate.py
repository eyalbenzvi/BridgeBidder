"""Paired ablation of two commits over several fresh seeds.

The ledger records what each round measured on the corpus that accepted it.
It cannot say what a RANGE of rounds bought, because every one of those
numbers was also a selection: the fix was kept because the number was
positive, so the ledger's total is an upper bound on the truth.

The only unbiased estimate is to play both versions on seeds that were never
a decision rule for either, and pair them board by board.  That is what this
does.

    python3 tools/roundkit/ablate.py \
        --a reports/pool --a-label HEAD \
        --b reports/r10 --b-label round-10 \
        --seeds 313131,323232,343434,353535,363636

Reports the per-seed paired deltas, the pooled total with a t-statistic and a
95% CI, and - because five seeds is a small sample of seeds - a CI computed
BOTH ways: across boards (the paired test) and across seeds (which makes no
assumption that boards within a seed are exchangeable with boards across it).
When those two disagree, believe the seed-level one.
"""

from __future__ import annotations

import argparse
import json
import math
import random
import statistics
from pathlib import Path


def load(path: Path) -> dict[int, dict]:
    return {r["board"]: r for r in (json.loads(l) for l in open(path))}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--a", required=True, help="directory of the first arm")
    ap.add_argument("--b", required=True, help="directory of the second arm")
    ap.add_argument("--a-label", default="A")
    ap.add_argument("--b-label", default="B")
    ap.add_argument("--a-pattern", default="seed{seed}.jsonl")
    ap.add_argument("--b-pattern", default="r10_seed{seed}.jsonl")
    ap.add_argument("--seeds", required=True)
    args = ap.parse_args()

    seeds = [s.strip() for s in args.seeds.split(",") if s.strip()]
    per_seed, all_deltas, missing = [], [], []
    print(f"\n=== ablation: {args.a_label} vs {args.b_label} ===\n")
    print(f"{'seed':>10}  {args.a_label:>10}  {args.b_label:>10}  "
          f"{'delta':>8}  {'changed':>8}")
    for s in seeds:
        pa = Path(args.a) / args.a_pattern.format(seed=s)
        pb = Path(args.b) / args.b_pattern.format(seed=s)
        if not pa.exists() or not pb.exists():
            missing.append(s)
            continue
        a, b = load(pa), load(pb)
        common = sorted(set(a) & set(b))
        d = [a[i]["imp_margin"] - b[i]["imp_margin"] for i in common]
        changed = sum(1 for i in common
                      if a[i]["a_auction"] != b[i]["a_auction"]
                      or a[i]["b_auction"] != b[i]["b_auction"])
        ta = sum(a[i]["imp_margin"] for i in common)
        tb = sum(b[i]["imp_margin"] for i in common)
        per_seed.append(sum(d))
        all_deltas.extend(d)
        print(f"{s:>10}  {ta:>+10d}  {tb:>+10d}  {sum(d):>+8d}  {changed:>8d}")

    if missing:
        print(f"\n  (missing, not yet run: {', '.join(missing)})")
    if not per_seed:
        print("\n  nothing to compare yet")
        return

    n = len(all_deltas)
    total = sum(all_deltas)
    sd = statistics.stdev(all_deltas) if n > 1 else 0.0
    se_board = sd * math.sqrt(n)
    print(f"\n  pooled over {len(per_seed)} seeds / {n} boards")
    print(f"  {args.a_label} minus {args.b_label}: {total:+d} IMPs "
          f"({1000 * total / n:+.1f} per 1000 boards)")
    if se_board:
        print(f"  board-level:  t = {total / se_board:+.2f}, "
              f"95% CI [{total - 1.96 * se_board:+.0f}, {total + 1.96 * se_board:+.0f}]")

    if len(per_seed) > 1:
        m = statistics.mean(per_seed)
        sds = statistics.stdev(per_seed)
        se_seed = sds / math.sqrt(len(per_seed))
        lo, hi = m - 2.776 * se_seed, m + 2.776 * se_seed      # t(4), 95%
        print(f"  seed-level:   mean {m:+.0f} IMPs per 1000-board seed, "
              f"t = {m / se_seed:+.2f}, 95% CI [{lo:+.0f}, {hi:+.0f}]")
        print(f"  (the seed-level interval is the honest one for 'what did "
              f"rounds 11-16 buy per 1000 boards')")

        rng = random.Random(20250830)
        boots = sorted(statistics.mean(rng.choice(per_seed)
                                       for _ in per_seed) for _ in range(20000))
        print(f"  seed bootstrap 95% CI [{boots[500]:+.0f}, {boots[19500]:+.0f}]")

    print()
    if len(per_seed) > 1:
        m = statistics.mean(per_seed)
        se_seed = statistics.stdev(per_seed) / math.sqrt(len(per_seed))
        if m - 2.776 * se_seed > 0:
            print(f"  --> {args.a_label} is ahead, and the interval excludes zero")
        elif m + 2.776 * se_seed < 0:
            print(f"  --> {args.b_label} is ahead, and the interval excludes zero")
        else:
            print(f"  --> NOT DISTINGUISHABLE.  On seeds that were never a "
                  f"decision rule for either version, the difference between "
                  f"them is within noise.")


if __name__ == "__main__":
    main()
