"""Screen a candidate system against a cached baseline corpus.

Why this exists
---------------
Both bidders are deterministic argmaxes, so a board whose auction does not
change is **bit-identical** between two runs and contributes exactly zero to
the paired delta.  All the signal - and all the sampling noise - lives on the
handful of boards a change actually touches:

    SE(paired delta) = sd_changed * sqrt(k)    for a change touching k boards

with sd_changed measured at about 5.5 IMPs.  A fix touching k=15 boards at a
real 1 IMP a board therefore sits at t = 15 / (5.5*sqrt(15)) = 0.70: the
1000-board accept/reject test that decided sixteen rounds of this project has
roughly **17% power**, and keeping-if-positive on a null effect pays about
+17 IMPs a round for nothing.

The fix is more boards, and more boards are affordable only because unchanged
ones are free.  With BEN's answers memoised (`tools/ben_cache.py`) and the
double-dummy solver consulted only where the contract moved, screening a
20,000-board pool costs a few minutes instead of two hours, and the same fix
reaches t = 15*20 / (5.5*sqrt(15*20)) = 3.1 - about 88% power.

What it does
------------
Re-plays every board of the pool under the CURRENT working tree, using the
same `play_table` the match itself uses, so the semantics cannot drift.  Where
the auction comes back identical the recorded score is reused untouched; where
it differs the contract is re-scored double-dummy.  The result is not an
approximation of the full-corpus paired delta - it IS the full-corpus paired
delta, computed without replaying what cannot have moved.

    # build the pool once, at the baseline commit
    python3 tools/roundkit/screen.py pool --seeds 401..420 --n 1000 --jobs 4

    # then, after any edit
    python3 tools/roundkit/screen.py run --pool reports/pool --jobs 4

Reporting
---------
Always a t-statistic and a 95% CI, never a bare delta, and **no verdict at all
below k=8 changed boards** - that is the floor under which the paired t-test
on IMP deltas is not trustworthy however the number looks.  A percentile
bootstrap CI is printed alongside the normal-theory one because per-board IMP
deltas are heavy-tailed; when the two disagree, believe the bootstrap.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import random
import statistics
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "src"))

VERDICT_FLOOR = 8          # refuse to call a winner below this many changed boards


# --------------------------------------------------------------------------
# replay
# --------------------------------------------------------------------------

def _replay_file(args):
    """Re-play one pool file under the current system.  Runs in a subprocess."""
    path, quiet = args
    import match_ben as M
    from compare_ben import Ben
    from bridgebidder.domain.cards import Hand
    from bridgebidder.domain.types import Seat, Vulnerability
    from bridgebidder.engine.dd import EndplayDD
    from bridgebidder.engine.scoring import imps, signed_score
    from bridgebidder.system.dsl import load_system

    system = load_system()
    ben = Ben()
    dd = EndplayDD()
    out = []
    t0 = time.time()
    rows = [json.loads(l) for l in open(path)]
    for r in rows:
        deal = {s: Hand.parse(r["hands"][s.value]) for s in Seat}
        dealer = Seat(r["dealer"])
        vul = Vulnerability.parse(r["vul"])
        rec = {"board": r["board"], "file": str(path),
               "before": r["imp_margin"], "changed": False}
        scores, changed_any = {}, False
        for t, side in (("a", "NS"), ("b", "EW")):
            auction, _calls = M.play_table(system, ben, deal, dealer, vul, side)
            text = " ".join(str(c) for c in auction.calls)
            if text == r[f"{t}_auction"]:
                scores[t] = r[f"{t}_score_ns"]          # bit-identical: reuse
                continue
            changed_any = True
            rec[f"{t}_before"] = r[f"{t}_auction"]
            rec[f"{t}_after"] = text
            c = auction.contract
            if c is None:
                scores[t] = 0
                rec[f"{t}_contract"] = "passed out"
            else:
                tricks = dd.tricks(deal, c.declarer, c.strain)
                scores[t] = signed_score(c, tricks, vul, "NS")
                rec[f"{t}_contract"] = f"{c} ({tricks} tricks)"
        if changed_any:
            rec["changed"] = True
            rec["after"] = imps(scores["a"] - scores["b"])
            rec["delta"] = rec["after"] - rec["before"]
        else:
            rec["after"] = rec["before"]
            rec["delta"] = 0
        out.append(rec)
    ben.close()
    if not quiet:
        k = sum(1 for r in out if r["changed"])
        print(f"  {Path(path).name}: {len(out)} boards, {k} changed, "
              f"{time.time() - t0:.0f}s  ({ben.cache.stats()})", flush=True)
    return out


# --------------------------------------------------------------------------
# statistics
# --------------------------------------------------------------------------

def summarise(recs: list[dict], label: str = "", boot: int = 20000) -> dict:
    """Paired t-test over the WHOLE pool; unchanged boards enter it as zeros."""
    n = len(recs)
    deltas = [r["delta"] for r in recs]
    changed = [r for r in recs if r["changed"]]
    k = len(changed)
    total = sum(deltas)
    sd = statistics.stdev(deltas) if n > 1 else 0.0
    se = sd * math.sqrt(n) if n > 1 else 0.0          # SE of the TOTAL
    t = total / se if se else 0.0
    lo, hi = total - 1.96 * se, total + 1.96 * se

    rng = random.Random(20250830)
    boots = []
    if k:
        for _ in range(boot):
            boots.append(sum(deltas[rng.randrange(n)] for _ in range(n)))
        boots.sort()
        blo, bhi = boots[int(0.025 * boot)], boots[int(0.975 * boot)]
    else:
        blo = bhi = 0.0

    cd = [r["delta"] for r in changed]
    # Power, stated every time rather than assumed.  Under the paired test the
    # SE of the total is sd_changed*sqrt(k), so an effect of e IMPs a changed
    # board is detectable at 5% two-sided with 90% power when
    #     e*k / (sd*sqrt(k)) >= 2.9   <=>   k >= (2.9*sd/e)^2
    # The project's working figure is sd = 5.5; the round-14 change measured
    # 7.04.  Both are reported because the difference moves the requirement by
    # 60%, and quoting only the friendlier one is how a test comes to be
    # believed beyond its resolution.
    sdc = statistics.stdev(cd) if k > 1 else 0.0
    res = {
        "label": label, "boards": n, "changed": k, "total": total,
        "per_1000": 1000.0 * total / n if n else 0.0,
        "sd_board": sd, "se_total": se, "t": t,
        "ci95": (lo, hi), "boot95": (blo, bhi),
        "sd_changed": sdc,
        "mde90": (2.9 * sdc / math.sqrt(k)) if k else float("inf"),
        "k_for_90_at_1imp": [round((2.9 * sd_) ** 2) for sd_ in (5.5, 7.04)],
        "up": sum(1 for d in cd if d > 0), "down": sum(1 for d in cd if d < 0),
        "flat": sum(1 for d in cd if d == 0),
    }
    res["verdict"] = verdict(res)
    return res


def verdict(s: dict) -> str:
    if s["changed"] < VERDICT_FLOOR:
        return (f"NO VERDICT - only {s['changed']} boards changed "
                f"(floor {VERDICT_FLOOR}).  Widen the pool or the change.")
    lo, hi = s["boot95"]
    if lo > 0:
        return "SHIP - 95% bootstrap CI excludes zero and is positive"
    if hi < 0:
        return "REVERT - 95% bootstrap CI excludes zero and is negative"
    return ("REVERT (not distinguishable from zero) - the 95% CI covers zero, "
            "so keeping this pays the selection premium, not the effect")


def render(s: dict) -> str:
    lo, hi = s["ci95"]
    blo, bhi = s["boot95"]
    L = [
        f"\n=== screen: {s['label'] or 'candidate'} ===",
        f"  pool           {s['boards']} boards",
        f"  boards changed {s['changed']}  ({s['up']} up, {s['down']} down, "
        f"{s['flat']} same margin)",
        f"  paired delta   {s['total']:+.0f} IMPs   "
        f"({s['per_1000']:+.1f} per 1000 boards)",
        f"  t              {s['t']:+.2f}   (SE of the total {s['se_total']:.0f})",
        f"  95% CI         [{lo:+.0f}, {hi:+.0f}]  normal theory",
        f"  95% CI         [{blo:+.0f}, {bhi:+.0f}]  percentile bootstrap",
        f"  sd per changed board {s['sd_changed']:.2f} IMPs",
        f"  resolution     this pool resolves {s['mde90']:.2f} IMPs/changed board "
        f"at 90% power; 1 IMP/board needs "
        f"{s['k_for_90_at_1imp'][0]}-{s['k_for_90_at_1imp'][1]} changed boards",
        f"  --> {s['verdict']}",
    ]
    return "\n".join(L)


# --------------------------------------------------------------------------
# commands
# --------------------------------------------------------------------------

def cmd_pool(a) -> None:
    """Build the cached baseline pool.  Run this ONCE, at the baseline commit."""
    seeds = parse_seeds(a.seeds)
    outdir = Path(a.pool)
    outdir.mkdir(parents=True, exist_ok=True)
    todo = [(s, outdir / f"seed{s}.jsonl") for s in seeds]
    todo = [(s, p) for s, p in todo if not p.exists()]
    print(f"building pool: {len(todo)} of {len(seeds)} seeds still to run "
          f"({a.n} boards each), {a.jobs} at a time")
    running: list = []
    logdir = ROOT / "logs"
    logdir.mkdir(exist_ok=True)
    while todo or running:
        while todo and len(running) < a.jobs:
            s, p = todo.pop(0)
            log = open(logdir / f"pool{s}.log", "w")
            env = dict(os.environ, OMP_NUM_THREADS="1")
            running.append((s, p, subprocess.Popen(
                [sys.executable, str(ROOT / "tools" / "match_ben.py"), "run",
                 "--n", str(a.n), "--seed", str(s), "--out", str(p)],
                stdout=log, stderr=subprocess.STDOUT, env=env), log))
            print(f"  started seed {s}", flush=True)
        time.sleep(5)
        for item in list(running):
            s, p, proc, log = item
            if proc.poll() is not None:
                running.remove(item)
                log.close()
                ok = p.exists()
                print(f"  seed {s} finished rc={proc.returncode} "
                      f"{'ok' if ok else 'MISSING OUTPUT'}", flush=True)
    print("pool complete:", sorted(x.name for x in outdir.glob("seed*.jsonl")))


def cmd_run(a) -> None:
    files = sorted(Path(a.pool).glob("seed*.jsonl")) if Path(a.pool).is_dir() \
        else [Path(x) for x in a.pool.split(",")]
    if a.seeds:
        keep = {f"seed{s}.jsonl" for s in parse_seeds(a.seeds)}
        files = [f for f in files if f.name in keep]
    if not files:
        sys.exit(f"no pool files under {a.pool}")
    print(f"screening {len(files)} pool file(s) with {a.jobs} job(s)")
    t0 = time.time()
    if a.jobs > 1:
        import multiprocessing as mp
        with mp.get_context("spawn").Pool(a.jobs) as pool:
            parts = pool.map(_replay_file, [(f, False) for f in files])
    else:
        parts = [_replay_file((f, False)) for f in files]
    recs = [r for part in parts for r in part]
    print(f"replayed {len(recs)} boards in {time.time() - t0:.0f}s")
    s = summarise(recs, a.label)
    print(render(s))
    if a.out:
        Path(a.out).parent.mkdir(parents=True, exist_ok=True)
        with open(a.out, "w") as f:
            f.write(json.dumps({"summary": s}) + "\n")
            for r in recs:
                if r["changed"]:
                    f.write(json.dumps(r) + "\n")
        print(f"  changed boards written to {a.out}")
    if a.list:
        for r in sorted((r for r in recs if r["changed"]),
                        key=lambda r: r["delta"]):
            print(f"\nboard {r['board']} [{Path(r['file']).name}]: "
                  f"{r['delta']:+d}  ({r['before']:+d} -> {r['after']:+d})")
            for t in ("a", "b"):
                if f"{t}_after" in r:
                    print(f"  {t.upper()} before: {r[f'{t}_before']}")
                    print(f"  {t.upper()} after : {r[f'{t}_after']}"
                          f"   -> {r.get(f'{t}_contract', '')}")


def parse_seeds(spec: str) -> list[int]:
    out: list[int] = []
    for part in spec.split(","):
        part = part.strip()
        if ".." in part:
            lo, hi = part.split("..")
            out.extend(range(int(lo), int(hi) + 1))
        elif part:
            out.append(int(part))
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("pool", help="build the cached baseline pool (once)")
    p.add_argument("--seeds", required=True, help="e.g. 401..420 or 1,2,3")
    p.add_argument("--n", type=int, default=1000)
    p.add_argument("--pool", default=str(ROOT / "reports" / "pool"))
    p.add_argument("--jobs", type=int, default=4)
    p.set_defaults(func=cmd_pool)

    r = sub.add_parser("run", help="screen the current tree against the pool")
    r.add_argument("--pool", default=str(ROOT / "reports" / "pool"))
    r.add_argument("--seeds", default="", help="restrict to these pool seeds")
    r.add_argument("--jobs", type=int, default=4)
    r.add_argument("--label", default="")
    r.add_argument("--out", default="")
    r.add_argument("--list", action="store_true")
    r.set_defaults(func=cmd_run)

    a = ap.parse_args()
    a.func(a)


if __name__ == "__main__":
    main()
