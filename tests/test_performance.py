"""Performance budget: fast-path < 50ms per decision, arbitration < 10s."""

import time

from bridgebidder.api import choose_bid
from bridgebidder.system.dsl import load_system
from bridgebidder.inference.engine import _SETUP_CACHE


def _req(hand, calls, seat, arbitration=False, budget=8.0):
    return {
        "hand": hand,
        "auction_state": {"dealer": "N", "seat": seat, "calls": calls},
        "use_arbitration": arbitration,
        "arbitration_budget": budget,
    }


def test_fast_path_under_50ms():
    load_system()  # warm the system cache (one-time YAML parse is excluded)
    cases = [
        ("AKJ72.K84.Q92.87", [], "N"),
        ("A5.KQJ64.842.K32", ["1S", "P"], "S"),
        ("KQ4.A72.AQJ84.94", ["1D", "P", "1S", "2C"], "N"),
        ("KQ52.A864.842.32", ["1NT", "P"], "S"),
        ("A52.KQJ64.4.A932", ["1H", "P", "2NT", "P"], "N"),
    ]
    for hand, calls, seat in cases:
        choose_bid(_req(hand, calls, seat))  # warm per-auction caches

    _SETUP_CACHE.clear()  # measure cold per-decision cost, warm system
    total = 0.0
    for hand, calls, seat in cases:
        t0 = time.perf_counter()
        choose_bid(_req(hand, calls, seat))
        total += time.perf_counter() - t0
    avg = total / len(cases)
    assert avg < 0.050, f"fast-path average {avg * 1000:.1f}ms exceeds 50ms"


def test_arbitration_under_10s():
    t0 = time.perf_counter()
    r = choose_bid(_req("AJ752.K4.Q92.J87", [], "N", arbitration=True, budget=8.0))
    elapsed = time.perf_counter() - t0
    assert elapsed < 10.0, f"arbitration took {elapsed:.1f}s"
    assert r["chosen_call"] in ("1S", "P", "1NT")
