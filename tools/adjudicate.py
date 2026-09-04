#!/usr/bin/env python3
"""Acceptance gate for a rule change: tests, then a paired match on a corpus
that already has a "before".

Only boards whose auction changed count.  The other boards are bit-identical
at both tables, so the paired difference carries no sampling noise - this is
the reading DECISIONS.md settled on after the 10,000-board round.

    python tools/adjudicate.py --before reports/before9001.jsonl --seed 9001
    python tools/adjudicate.py --before reports/before9001.jsonl --seed 9001 --skip-tests

The "after" file is named after the seed and the current commit, so each
accepted change leaves the file that is the next change's "before".  The
seed must be the one the before-file was generated with (match_ben.py deals
from the seed, so same seed + same n = same boards).  Requires BEN
(tools/setup_ben.sh) and the double-dummy solver.

Exit status is 0 when the net paired result is >= 0 and tests pass, 1
otherwise - so a cheap operator (a script, a small model) can run this and
report, while reading the changed boards stays with whoever wrote the rule.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def git_hash() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, text=True).strip()
    except Exception:
        return "wip"


def run_tests() -> bool:
    print("== pytest ==", flush=True)
    res = subprocess.run([sys.executable, "-m", "pytest", "tests", "-q", "-x"], cwd=ROOT)
    return res.returncode == 0


def run_match(seed: int, n: int, out: Path) -> None:
    print(f"== match: {n} boards, seed {seed} -> {out} ==", flush=True)
    subprocess.run([sys.executable, str(ROOT / "tools" / "match_ben.py"), "run",
                    "--n", str(n), "--seed", str(seed), "--out", str(out)], cwd=ROOT, check=True)


def paired(before: Path, after: Path, show: int) -> int:
    a = [json.loads(l) for l in open(before)]
    b = [json.loads(l) for l in open(after)]
    assert len(a) == len(b), "before/after have different board counts"
    for x, y in zip(a, b):
        assert x["hands"] == y["hands"], f"board {x['board']}: different deals - wrong seed?"
    changed = [(x, y) for x, y in zip(a, b)
               if x["a_auction"] != y["a_auction"] or x["b_auction"] != y["b_auction"]]
    delta = sum(y["imp_margin"] - x["imp_margin"] for x, y in changed)
    better = sum(1 for x, y in changed if y["imp_margin"] > x["imp_margin"])
    worse = sum(1 for x, y in changed if y["imp_margin"] < x["imp_margin"])
    print(f"\n== paired verdict on {len(a)} identical deals ==")
    print(f"  total margin before {sum(r['imp_margin'] for r in a):+d}, after {sum(r['imp_margin'] for r in b):+d}")
    print(f"  changed boards {len(changed)}: {better} improved, {worse} worse, {len(changed) - better - worse} flat")
    print(f"  NET {delta:+d} IMPs on the changed boards")
    rules = Counter()
    for x, y in changed:
        old = {(c["seat"], c["n"]): c["rule"] for t in ("a_our_calls", "b_our_calls") for c in x[t]}
        for t in ("a_our_calls", "b_our_calls"):
            for c in y[t]:
                if old.get((c["seat"], c["n"])) != c["rule"]:
                    rules[c["rule"]] += 1
    if rules:
        print("  rules that fired where a different rule fired before:", dict(rules.most_common(8)))
    print(f"\n== changed boards (worst first, {min(show, len(changed))} shown) - read these ==")
    for x, y in sorted(changed, key=lambda p: p[1]["imp_margin"] - p[0]["imp_margin"])[:show]:
        d = y["imp_margin"] - x["imp_margin"]
        print(f"\n  board {x['board']} {d:+d} IMPs   N {x['hands']['N']}  E {x['hands']['E']}  S {x['hands']['S']}  W {x['hands']['W']}")
        for t, lab in (("a", "A (we N/S)"), ("b", "B (we E/W)")):
            if x[f"{t}_auction"] != y[f"{t}_auction"]:
                print(f"    {lab} before: {x[f'{t}_auction']}  -> {x[f'{t}_contract']}")
                print(f"    {lab} after : {y[f'{t}_auction']}  -> {y[f'{t}_contract']}")
    return delta


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--before", type=Path, required=True)
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--after", type=Path, help="default: reports/after_<seed>_<commit>.jsonl")
    ap.add_argument("--skip-tests", action="store_true")
    ap.add_argument("--reuse-after", action="store_true", help="do not replay if the after-file exists")
    ap.add_argument("--show", type=int, default=20)
    a = ap.parse_args()
    ok = True
    if not a.skip_tests:
        ok = run_tests()
        if not ok:
            print("tests failed - not running the match")
            sys.exit(1)
    n = sum(1 for _ in open(a.before))
    after = a.after or (ROOT / "reports" / f"after_{a.seed}_{git_hash()}.jsonl")
    if not (a.reuse_after and after.exists()):
        run_match(a.seed, n, after)
    delta = paired(a.before, after, a.show)
    sys.exit(0 if delta >= 0 else 1)
