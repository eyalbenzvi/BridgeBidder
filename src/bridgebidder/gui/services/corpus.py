"""Corpus replay service: validate proposed rule patches against the 12k-board pool.

Each file in data/pool/seed501..512.jsonl.gz contains 1000 boards; each board
records the original auction, our calls, and the IMP margin.  For boards that
touch a patched rule we replay both tables with the new system + BEN and
compute the score delta.  A paired t-test over changed boards determines the
verdict.
"""

from __future__ import annotations

import asyncio
import gzip
import json
import math
import sys
from pathlib import Path
from typing import TYPE_CHECKING

# Make tools/ importable for Ben.
_TOOLS_DIR = Path(__file__).parents[4] / "tools"
if str(_TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(_TOOLS_DIR))

from compare_ben import Ben  # noqa: E402
from bridgebidder.domain.cards import Hand
from bridgebidder.domain.calls import Call
from bridgebidder.domain.types import Seat, Vulnerability
from bridgebidder.domain.auction import Auction
from bridgebidder.engine.dd import get_dd, EndplayDD
from bridgebidder.engine.scoring import imps, signed_score

from .rule_patch import get_system_for_patches, get_touched_rule_ids
from .deal_gen import play_table_with_setups

if TYPE_CHECKING:
    from bridgebidder.system.dsl import BiddingSystem

POOL_DIR = Path(__file__).parents[4] / "data" / "pool"
VULS_MAP = {v.value: v for v in Vulnerability}

# Module-level singletons for the replay (expensive to initialise).
_replay_ben: Ben | None = None
_replay_dd: EndplayDD | None = None


def _get_replay_ben() -> Ben:
    global _replay_ben
    if _replay_ben is None:
        _replay_ben = Ben()
    return _replay_ben


def _get_replay_dd() -> EndplayDD:
    global _replay_dd
    if _replay_dd is None:
        _replay_dd = get_dd()
    return _replay_dd


# ---------------------------------------------------------------------------
# Synchronous replay of a single board
# ---------------------------------------------------------------------------


def _replay_board(
    system: "BiddingSystem",
    ben: Ben,
    dd: EndplayDD,
    row: dict,
) -> int:
    """Return the new IMP margin for a board, replaying both tables."""
    dealer = Seat(row["dealer"])
    vul = VULS_MAP[row["vul"]]
    deal: dict[Seat, Hand] = {Seat(s): Hand.parse(h) for s, h in row["hands"].items()}

    a_auction, _a_calls, _ = play_table_with_setups(system, ben, deal, dealer, vul, "NS")
    b_auction, _b_calls, _ = play_table_with_setups(system, ben, deal, dealer, vul, "EW")

    def score_ns(auction: Auction) -> int:
        c = auction.contract
        if c is None:
            return 0
        tricks = dd.tricks(deal, c.declarer, c.strain)
        return signed_score(c, tricks, vul, "NS")

    return imps(score_ns(a_auction) - score_ns(b_auction))


# ---------------------------------------------------------------------------
# Synchronous batch replay (runs inside executor)
# ---------------------------------------------------------------------------


def _run_replay_sync(
    system: "BiddingSystem",
    touched_rule_ids: set[str],
    progress_cb,
) -> tuple[list[dict], list[int]]:
    """Replay all 12k boards synchronously.

    Returns (changed_boards, all_deltas) where:
      - changed_boards: list of board dicts with added delta/new_margin fields
      - all_deltas: list of delta values for all *changed* boards
    """
    ben = _get_replay_ben()
    dd = _get_replay_dd()
    files = sorted(POOL_DIR.glob("seed*.jsonl.gz"))

    changed_boards: list[dict] = []
    all_deltas: list[int] = []
    board_count = 0

    for gz_file in files:
        with gzip.open(gz_file, "rt", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                row = json.loads(line)
                board_count += 1

                # Check whether any of our calls used a touched rule.
                a_rules = {c["rule"] for c in row.get("a_our_calls", []) if c.get("rule")}
                b_rules = {c["rule"] for c in row.get("b_our_calls", []) if c.get("rule")}
                touched = bool((a_rules | b_rules) & touched_rule_ids)

                if touched:
                    new_margin = _replay_board(system, ben, dd, row)
                    baseline = row.get("imp_margin", 0)
                    delta = new_margin - baseline
                    all_deltas.append(delta)
                    changed_boards.append({
                        "board": row.get("board", board_count),
                        "dealer": row.get("dealer"),
                        "vul": row.get("vul"),
                        "hands": row.get("hands"),
                        "baseline_margin": baseline,
                        "new_margin": new_margin,
                        "delta": delta,
                    })

                if board_count % 50 == 0:
                    progress_cb(board_count, len(changed_boards), sum(all_deltas) if all_deltas else 0)

    return changed_boards, all_deltas


# ---------------------------------------------------------------------------
# Statistical helpers
# ---------------------------------------------------------------------------


def _t_test(deltas: list[int]) -> tuple[float | None, float | None]:
    """Paired t-test on deltas.  Returns (t_stat, p_value) or (None, None)."""
    n = len(deltas)
    if n < 8:
        return None, None

    mean = sum(deltas) / n
    variance = sum((d - mean) ** 2 for d in deltas) / (n - 1)
    if variance == 0:
        return (float("inf") if mean > 0 else float("-inf")), (0.0 if mean != 0 else 1.0)

    std = math.sqrt(variance)
    t_stat = mean / (std / math.sqrt(n))

    # Approximate p-value using a Gaussian approximation (good for n >= 30).
    # For smaller n we use a rough approximation via error function.
    try:
        from scipy.stats import t as t_dist
        p_value = float(t_dist.sf(abs(t_stat), df=n - 1) * 2)
    except ImportError:
        # Gaussian approximation via math.erfc
        z = abs(t_stat) / math.sqrt(2)
        p_value = math.erfc(z)

    return t_stat, p_value


# ---------------------------------------------------------------------------
# Async entry point
# ---------------------------------------------------------------------------


async def replay_corpus(websocket, patches: list[dict]) -> dict:
    """Replay all 12k boards with the patched system.

    Streams progress via websocket and sends a final result message.
    """
    loop = asyncio.get_event_loop()

    touched_rule_ids = get_touched_rule_ids(patches)
    system = await loop.run_in_executor(None, get_system_for_patches, patches)

    total_boards = 12000
    progress_queue: asyncio.Queue = asyncio.Queue()

    def _progress_cb(done: int, changed: int, delta_sum: int) -> None:
        progress_queue.put_nowait((done, changed, delta_sum))

    # Run the heavy replay in a thread.
    replay_future = loop.run_in_executor(
        None,
        _run_replay_sync,
        system,
        touched_rule_ids,
        _progress_cb,
    )

    # Stream progress while waiting.
    while not replay_future.done():
        try:
            done, changed, delta_sum = progress_queue.get_nowait()
            await websocket.send_json({
                "type": "progress",
                "board": done,
                "total": total_boards,
                "changed": changed,
                "delta_imps": delta_sum,
            })
        except asyncio.QueueEmpty:
            pass
        await asyncio.sleep(0.1)

    # Drain any remaining progress items.
    while not progress_queue.empty():
        done, changed, delta_sum = progress_queue.get_nowait()
        await websocket.send_json({
            "type": "progress",
            "board": done,
            "total": total_boards,
            "changed": changed,
            "delta_imps": delta_sum,
        })

    changed_boards, all_deltas = await replay_future

    n = len(all_deltas)
    mean_delta = sum(all_deltas) / n if n else 0.0
    t_stat, p_value = _t_test(all_deltas)

    if t_stat is None:
        verdict = "INCONCLUSIVE"
    elif t_stat > 1.5 and mean_delta > 0:
        verdict = "SHIP"
    elif t_stat > 1.5 and mean_delta < 0:
        verdict = "REVERT"
    else:
        verdict = "INCONCLUSIVE"

    result = {
        "type": "result",
        "mean_delta": mean_delta,
        "t_stat": t_stat,
        "p_value": p_value,
        "boards_changed": n,
        "verdict": verdict,
        "changed_boards": changed_boards[:200],  # cap to avoid huge payloads
    }
    await websocket.send_json(result)
    return result
