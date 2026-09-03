#!/usr/bin/env python3
"""Screen the working tree against the 12,000-board pool shipped in `data/`.

The check after a rule change: did it help, and by enough to tell from noise.

Related but different from `roundkit/screen.py`, which replays an uncompressed
pool built with a live BEN worker.  This one runs against `data/pool/*.jsonl.gz`
using the answer cache in `data/ben_cache.sqlite.gz`, so it needs nothing
installed beyond `endplay` -- which makes it the one that actually runs on a
machine that has never had BEN on it.  Positions the cache does not cover are
reported as unresolved rather than quietly scored as unchanged.

The statistics are `roundkit.screen.summarise`, unchanged: paired total over
the whole pool with unchanged boards as zeros, a percentile bootstrap CI, an
eight-board verdict floor, and a CI covering zero read as REVERT.

WHAT THE NUMBER MEANS.  This measures the working tree against the scores the
pool RECORDED, and the pool was played at an older commit.  On a clean tree at
HEAD it already reports 38 changed boards per 1000 -- that is the rulebook
having moved since, not anything you just did.  So a single run does not
isolate your change.  Take a reading before your edit and one after, and
compare:

    python3 tools/screen_pool.py --json /tmp/before.json
    # ... edit the rulebook ...
    python3 tools/screen_pool.py --json /tmp/after.json --against /tmp/before.json

    python3 tools/screen_pool.py --boards 12000   # the whole pool
    python3 tools/screen_pool.py --list           # every changed board
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tools"))

from bridgebidder.gui.services import corpus  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--boards", type=int, default=2000,
                    help="how many pool boards to replay, rounded down to whole "
                         "1000-board files (default 2000)")
    ap.add_argument("--list", action="store_true",
                    help="print every changed board, worst first")
    ap.add_argument("--quiet", action="store_true", help="no progress line")
    ap.add_argument("--json", metavar="PATH",
                    help="write the full result here, for a later --against")
    ap.add_argument("--against", metavar="PATH",
                    help="a --json reading taken before the edit; the printed "
                         "delta is then your change alone, with the pool's own "
                         "drift subtracted out")
    args = ap.parse_args()

    ready = corpus.readiness()
    if not ready["ok"]:
        sys.exit("cannot screen: " + "; ".join(ready["reasons"]))

    t0 = time.time()

    def progress(done: int, changed: int, delta: int) -> None:
        if not args.quiet and done % 250 == 0:
            print(f"  {done:>6} boards · {changed} changed · {delta:+} IMP",
                  file=sys.stderr, flush=True)

    print(f"screening the working tree against {args.boards} boards "
          f"({ready['mode']} BEN)", file=sys.stderr)
    res = corpus.screen(boards=args.boards, progress=progress)

    lo, hi = res["boot95"]
    fmt = lambda v: "—" if v is None else f"{v:+.2f}"   # noqa: E731
    print(f"""
=== screen: working tree ===
  pool           {res['boards']} boards ({time.time() - t0:.0f}s)
  boards changed {res['boards_changed']}  ({res['up']} up, {res['down']} down, """
          f"""{res['flat']} same margin)
  unresolved     {res['unresolved']}  (positions the answer cache does not cover)
  paired delta   {res['total_delta']:+.0f} IMP   ({res['per_1000']:+.1f} per 1000)
  t              {fmt(res['t_stat'])}
  95% CI         [{lo:+.0f}, {hi:+.0f}]  percentile bootstrap
  sd per changed board {res['sd_changed']:.2f} IMP
  resolution     resolves {fmt(res['mde90'])} IMP/changed board at 90% power
  --> {res['verdict']}""")

    if args.json:
        Path(args.json).write_text(json.dumps(res, indent=1), encoding="utf-8")
        print(f"  reading saved to {args.json}", file=sys.stderr)

    if args.against:
        prior = json.loads(Path(args.against).read_text(encoding="utf-8"))
        print(f"""
=== against {args.against} ===
  that reading    {prior['total_delta']:+.0f} IMP over {prior['boards']} boards, """
              f"""{prior['boards_changed']} changed
  this reading    {res['total_delta']:+.0f} IMP over {res['boards']} boards, """
              f"""{res['boards_changed']} changed
  your change     {res['total_delta'] - prior['total_delta']:+.0f} IMP, """
              f"""{res['boards_changed'] - prior['boards_changed']:+d} boards

  Both readings carry the same drift between the pool and the tree, so the
  difference is your edit. It is not a significance test: for that, rebuild a
  pool at the current commit (tools/roundkit/screen.py pool).""")
    elif res["boards_changed"]:
        print("""
  NOTE: this compares the tree against scores the pool recorded at an older
  commit, so some of those changed boards predate anything you did. Take a
  --json reading before your edit and pass it as --against to separate them.""")

    if args.list:
        for board in res["changed_boards"]:
            print(f"\nboard {board['board']} [{board['file']}]: {board['delta']:+d}  "
                  f"({board['before']:+d} -> {board['after']:+d})")
            for t in ("a", "b"):
                if f"{t}_after" in board:
                    print(f"  {t.upper()} before: {board[f'{t}_before']}")
                    print(f"  {t.upper()} after : {board[f'{t}_after']}"
                          f"   -> {board.get(f'{t}_contract', '')}")


if __name__ == "__main__":
    main()
