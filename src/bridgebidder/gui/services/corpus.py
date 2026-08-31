"""Corpus replay: measure a proposed patch against the 12,000-board pool.

The measurement, and why it is the one from `roundkit/screen.py`
----------------------------------------------------------------
Both bidders are deterministic, so a board whose auction does not move is
bit-identical between the baseline and the candidate and contributes exactly
zero to the paired delta.  That is what makes a 12k-board test affordable --
only the handful of boards a patch actually touches has to be replayed -- and
it is also what makes the statistics easy to get wrong.

Two traps, both of which this module used to fall into:

  * **Testing only the changed boards.**  The paired test runs over the WHOLE
    pool, with unchanged boards entering as zeros.  Averaging over the changed
    boards alone inflates t by sqrt(N/k) -- for a patch touching 15 boards out
    of 12,000, by a factor of 28 -- and turns noise into a confident SHIP.
  * **A lax threshold.**  `t > 1.5` is p ~ 0.13.  Keeping every change that
    clears it pays the selection premium, not the effect; sixteen rounds of
    this project were decided that way before the floor went in.

So the arithmetic here is delegated wholesale to `roundkit.screen.summarise`:
the same paired total, the same percentile bootstrap CI, the same eight-board
verdict floor, the same refusal to call a winner on a CI that covers zero.
One standard, in one place, so the GUI cannot quietly drift laxer than the
command-line tool the project already trusts.

Running without BEN
-------------------
Replaying a board whose auction diverges needs BEN's calls for the opponent
seats in positions the baseline never visited.  On a machine with no BEN
worker those positions can still be served from the shipped answer cache
(`data/ben_cache.sqlite.gz`) -- BEN is a pure function of the request, so a
cached answer is the answer -- but a genuinely new prefix is simply unknown.
Such boards are counted as UNRESOLVED and excluded from the pool the test runs
over, and the count is reported next to the verdict, because a verdict computed
over a corpus with a hole in it is only as good as the size of the hole.
"""

from __future__ import annotations

import asyncio
import gzip
import json
import shutil
import sys
from pathlib import Path
from typing import TYPE_CHECKING

# Make tools/ importable for Ben and the shared statistics.
_TOOLS_DIR = Path(__file__).parents[4] / "tools"
if str(_TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(_TOOLS_DIR))

from ben_cache import BenCache, request_key  # noqa: E402
from compare_ben import Ben  # noqa: E402
from roundkit.screen import summarise  # noqa: E402

from bridgebidder.domain.auction import Auction
from bridgebidder.domain.calls import Call
from bridgebidder.domain.cards import Hand
from bridgebidder.domain.types import Seat, Vulnerability
from bridgebidder.engine.decision import decide_fast
from bridgebidder.engine.scoring import imps, signed_score
from bridgebidder.inference.engine import prepare_decision

from . import deal_gen
from .rule_patch import get_system_for_patches, get_touched_rule_ids

if TYPE_CHECKING:
    from bridgebidder.system.dsl import BiddingSystem

ROOT = Path(__file__).parents[4]
POOL_DIR = ROOT / "data" / "pool"
CACHE_GZ = ROOT / "data" / "ben_cache.sqlite.gz"
CACHE_DB = ROOT / "reports" / "ben_cache.sqlite"
MAX_CALLS = 60


class BenMiss(Exception):
    """A position the shipped cache does not cover and no worker can answer."""


def _finite(obj):
    """Replace inf/nan with None throughout, recursively.

    `mde90` is +inf when nothing changed and `t` is +/-inf when the changed
    boards all move the same way.  Python's json writes those as bare
    `Infinity`/`NaN`, which is not JSON and makes the browser's `JSON.parse`
    throw -- losing the entire result to a field nobody was going to read.
    """
    import math as _m

    if isinstance(obj, float):
        return None if (_m.isinf(obj) or _m.isnan(obj)) else obj
    if isinstance(obj, dict):
        return {k: _finite(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_finite(x) for x in obj]
    return obj


# ---------------------------------------------------------------------------
# BEN, live or from the shipped cache
# ---------------------------------------------------------------------------


def ensure_cache_db() -> Path | None:
    """Decompress the shipped answer cache once, into `reports/`.

    The repository ships it gzipped (14 MB vs about 100 MB), and sqlite cannot
    read a gzip stream, so the first run pays the decompression and every run
    afterwards opens it directly.
    """
    if CACHE_DB.exists():
        return CACHE_DB
    if not CACHE_GZ.exists():
        return None
    CACHE_DB.parent.mkdir(parents=True, exist_ok=True)
    tmp = CACHE_DB.with_suffix(".sqlite.partial")
    with gzip.open(CACHE_GZ, "rb") as src, open(tmp, "wb") as dst:
        shutil.copyfileobj(src, dst)
    tmp.replace(CACHE_DB)          # atomic: a half-written cache is never seen
    return CACHE_DB


class CachedBen:
    """BEN's answers from disk only.  Raises `BenMiss` where it has none."""

    def __init__(self) -> None:
        path = ensure_cache_db()
        self.cache = BenCache(path) if path else None
        self.misses = 0

    def ask(self, req: dict) -> dict:
        if self.cache is None:
            raise BenMiss("no answer cache on this machine")
        hit = self.cache.get(request_key(req))
        if hit is None:
            self.misses += 1
            raise BenMiss("position not in the shipped cache")
        return hit

    def close(self) -> None:
        if self.cache is not None:
            self.cache.close()


_replay_ben: object | None = None
_replay_dd: object | None = None


def _get_replay_ben():
    global _replay_ben
    if _replay_ben is None:
        _replay_ben = Ben() if deal_gen.ben_available() else CachedBen()
    return _replay_ben


def _get_replay_dd():
    global _replay_dd
    if _replay_dd is None:
        from bridgebidder.engine.dd import EndplayDD
        _replay_dd = EndplayDD()      # never the heuristic: see readiness()
    return _replay_dd


def readiness() -> dict:
    """Whether a corpus test can produce a number worth believing."""
    live = deal_gen.ben_available()
    cache = CACHE_DB.exists() or CACHE_GZ.exists()
    dd = deal_gen.dd_available()
    pool = bool(sorted(POOL_DIR.glob("seed*.jsonl.gz")))
    ok = dd and pool and (live or cache)
    reasons = []
    if not dd:
        reasons.append("the double-dummy solver is missing (pip install endplay) — "
                       "without it a re-scored board is a guess, not a score")
    if not pool:
        reasons.append("no board pool under data/pool/")
    if not (live or cache):
        reasons.append("neither a BEN worker nor the shipped answer cache is present")
    return {
        "ok": ok, "live_ben": live, "cached_ben": cache, "dd": dd, "pool": pool,
        "mode": "live" if live else "cache-only" if cache else "unavailable",
        "reasons": reasons,
    }


# ---------------------------------------------------------------------------
# replay of one board
# ---------------------------------------------------------------------------


def _play_table(system: "BiddingSystem", ben, deal, dealer, vul, our_side) -> Auction:
    auction = Auction(dealer=dealer, vulnerability=vul)
    hands = {s.value: str(deal[s]) for s in Seat}
    while not auction.is_complete:
        seat = auction.next_seat
        if seat.side == our_side:
            setup = prepare_decision(system, auction, perspective=seat)
            choice = decide_fast(setup, deal[seat])
            call = choice if isinstance(choice, Call) else choice.call
        else:
            resp = ben.ask({
                "hands": hands,
                "dealer": dealer.value,
                "vuln_ns": int(vul.is_vulnerable(Seat.N)),
                "vuln_ew": int(vul.is_vulnerable(Seat.E)),
                "auction": [str(c) for c in auction.calls],
            })
            call = Call.parse(resp["bid"])
            if not auction.is_legal(call):
                call = Call.parse("P")
        auction.add(call)
        if len(auction.calls) > MAX_CALLS:
            break
    return auction


def _replay_board(system: "BiddingSystem", ben, dd, row: dict) -> dict:
    """Re-play one board; reuse the recorded score wherever the auction holds.

    Mirrors `roundkit/screen.py:_replay_file` exactly, including the
    reuse-on-identical-auction rule that makes the whole thing affordable.
    """
    dealer = Seat(row["dealer"])
    vul = Vulnerability.parse(row["vul"])
    deal = {s: Hand.parse(row["hands"][s.value]) for s in Seat}

    rec = {"board": row["board"], "file": row.get("_file", ""),
           "before": row["imp_margin"], "changed": False,
           "hands": row["hands"], "dealer": row["dealer"], "vul": row["vul"]}
    scores: dict[str, int] = {}
    changed_any = False

    for t, side in (("a", "NS"), ("b", "EW")):
        auction = _play_table(system, ben, deal, dealer, vul, side)
        text = " ".join(str(c) for c in auction.calls)
        if text == row[f"{t}_auction"]:
            scores[t] = row[f"{t}_score_ns"]        # bit-identical: reuse
            continue
        changed_any = True
        rec[f"{t}_before"] = row[f"{t}_auction"]
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
    return rec


# ---------------------------------------------------------------------------
# whole-pool replay
# ---------------------------------------------------------------------------


def _diverges(system: "BiddingSystem", row: dict) -> bool:
    """Would the patched engine still make every call this board recorded?

    Walk the *recorded* auction and re-decide only at our own seats.  If every
    one of our calls comes back identical, the board cannot have moved: the
    opponent is a pure function of the prefix, every prefix here is the
    recorded one, so the whole auction replays byte for byte.  That makes this
    a sound skip -- and it needs no opponent model and no solver, just our own
    engine, which is why it can afford to run on all twelve thousand boards.

    It replaces an earlier filter that skipped any board whose recorded calls
    named no patched rule.  That filter was sound only for patches that
    *narrow* a rule.  Widening one -- or adding one -- steals decisions from
    whatever rule wins them today, on boards where the patched rule appears
    nowhere in the record.  Tested on a 15-17 to 15-18 notrump widening, the
    rule filter reported 0 changed boards out of 12,000; the real number is
    about 670.  A confident, instant, wrong "no effect" is the worst answer
    this tool can give, so the cheap filter had to go.
    """
    dealer = Seat(row["dealer"])
    vul = Vulnerability.parse(row["vul"])
    deal = {s: Hand.parse(row["hands"][s.value]) for s in Seat}

    for t, side in (("a", "NS"), ("b", "EW")):
        auction = Auction(dealer=dealer, vulnerability=vul)
        for text in row[f"{t}_auction"].split():
            seat = auction.next_seat
            call = Call.parse(text)
            if seat.side == side:
                choice = decide_fast(
                    prepare_decision(system, auction, perspective=seat), deal[seat])
                now = choice if isinstance(choice, Call) else choice.call
                if now != call:
                    return True
            auction.add(call)
    return False


def _run_replay_sync(system: "BiddingSystem", files: list[Path], progress_cb):
    """Replay the selected pool files.  Returns (records, unresolved)."""
    ben = _get_replay_ben()
    dd = _get_replay_dd()

    recs: list[dict] = []
    unresolved: list[dict] = []
    seen = 0

    for gz in files:
        with gzip.open(gz, "rt", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                row = json.loads(line)
                row["_file"] = gz.name
                seen += 1

                if _diverges(system, row):
                    try:
                        recs.append(_replay_board(system, ben, dd, row))
                    except BenMiss as exc:
                        unresolved.append({"board": row["board"], "file": gz.name,
                                           "reason": str(exc)})
                else:
                    recs.append({"board": row["board"], "file": gz.name,
                                 "before": row["imp_margin"], "after": row["imp_margin"],
                                 "changed": False, "delta": 0})

                if seen % 25 == 0:
                    k = sum(1 for r in recs if r["changed"])
                    progress_cb(seen, k, sum(r["delta"] for r in recs))

    return recs, unresolved


# ---------------------------------------------------------------------------
# async entry point
# ---------------------------------------------------------------------------


def pool_files(boards: int | None = None) -> list[Path]:
    """Pool files to test against, each holding 1000 boards.

    The whole pool is the right test and costs about a minute per thousand
    boards on one core, so the caller may ask for less.  A smaller pool is not
    a cheaper version of the same answer -- it resolves a larger effect -- and
    `summarise` says so on every run, which is what makes offering the choice
    safe.
    """
    files = sorted(POOL_DIR.glob("seed*.jsonl.gz"))
    if boards:
        files = files[:max(1, boards // 1000)]
    return files


async def replay_corpus(websocket, patches: list[dict], boards: int | None = None) -> dict:
    """Replay the pool under `patches`, streaming progress, and report."""
    ready = readiness()
    if not ready["ok"]:
        result = {"type": "error", "message": "; ".join(ready["reasons"]),
                  "readiness": ready}
        await websocket.send_json(result)
        return result

    loop = asyncio.get_event_loop()
    touched = get_touched_rule_ids(patches)
    system = await loop.run_in_executor(None, get_system_for_patches, patches)

    files = pool_files(boards)
    total = len(files) * 1000
    queue: asyncio.Queue = asyncio.Queue()

    def _progress(done: int, changed: int, delta_sum: int) -> None:
        queue.put_nowait((done, changed, delta_sum))

    await websocket.send_json({
        "type": "started", "mode": ready["mode"],
        "touched_rules": sorted(touched), "total": total,
    })

    future = loop.run_in_executor(None, _run_replay_sync, system, files, _progress)

    async def drain() -> None:
        while not queue.empty():
            done, changed, delta_sum = queue.get_nowait()
            await websocket.send_json({
                "type": "progress", "board": done, "total": total,
                "changed": changed, "delta_imps": delta_sum,
            })

    while not future.done():
        await drain()
        await asyncio.sleep(0.1)
    await drain()

    recs, unresolved = await future

    # The paired test runs over every board that produced a score: unchanged
    # boards are the zeros that hold the estimate honest.  Boards the cache
    # could not resolve are absent rather than zero, and are reported as such.
    stats = await loop.run_in_executor(None, summarise, recs, "proposal")
    changed = [r for r in recs if r["changed"]]
    changed.sort(key=lambda r: r["delta"])

    result = _finite({
        "type": "result",
        "mode": ready["mode"],
        "verdict": stats["verdict"],
        "verdict_short": ("NO VERDICT" if stats["verdict"].startswith("NO VERDICT")
                          else stats["verdict"].split(" ")[0]),
        "boards": stats["boards"],
        "boards_changed": stats["changed"],
        "unresolved": len(unresolved),
        "unresolved_boards": unresolved[:50],
        "total_delta": stats["total"],
        "per_1000": stats["per_1000"],
        "mean_delta": (stats["total"] / stats["changed"]) if stats["changed"] else 0.0,
        "t_stat": stats["t"],
        "ci95": list(stats["ci95"]),
        "boot95": list(stats["boot95"]),
        "sd_changed": stats["sd_changed"],
        "mde90": stats["mde90"],
        "up": stats["up"], "down": stats["down"], "flat": stats["flat"],
        "changed_boards": changed[:200],
    })
    await websocket.send_json(result)
    return result
