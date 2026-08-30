"""Find the seat where the partnership stops investigating.

The consolidated review's central finding is that 67% of the held-out deficit
sits on the 14% of deals where a slam exists, and that the mechanism is a
missing seat rather than a bad rule: once our side holds a game contract,
`we_hold_contract` is true, every general context is gated
`we_hold_contract: false`, and the fallback layer goes `quiet` - so *reaching
game* is the terminal state of the whole system.

This scans a played corpus for that seat and scores it, so a candidate can be
priced against the population it is meant to serve rather than against three
anecdotes.

    python3 tools/roundkit/slamscan.py reports/e10_final.jsonl [--trace 12]

Reports, per corpus:
  * how many times we pass our own side's game contract;
  * the sub-population that WANTS to move (4+ controls and a singleton or
    void), with its board margin and par gap against the rest;
  * what the engine actually offers those seats - the candidate count and the
    best non-pass fit, which is the number that says "there is no rule here";
  * the slam-band accounting: deals with 12 or 13 tricks available, how many
    slams each side bid, and how many made.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from repro import rank, seat_of, system                      # noqa: E402
from bridgebidder.domain.cards import Hand                   # noqa: E402
from bridgebidder.domain.calls import Call                   # noqa: E402

SEATS = "NESW"


def game_reached(calls: list[str]) -> bool:
    for c in reversed(calls):
        if c in ("P", "X", "XX"):
            continue
        lvl, strain = int(c[0]), c[1:]
        return (strain == "NT" and lvl >= 3) or \
               (strain in "HS" and lvl >= 4) or (strain in "CD" and lvl >= 5)
    return False


def last_bid(calls: list[str]) -> tuple[int, str] | None:
    for i in range(len(calls) - 1, -1, -1):
        c = calls[i]
        if c not in ("P", "X", "XX"):
            return i, c
    return None


def our_game_passes(rows: list[dict]) -> list[dict]:
    """Every seat where we passed with our own side holding a game contract."""
    out = []
    for r in rows:
        for t in ("a", "b"):
            calls = r[f"{t}_auction"].split()
            for oc in r[f"{t}_our_calls"]:
                i = oc["n"]
                if oc["call"] != "P" or i >= len(calls):
                    continue
                prefix = calls[:i]
                lb = last_bid(prefix)
                if lb is None or not game_reached(prefix):
                    continue
                bidder = SEATS[(SEATS.index(r["dealer"]) + lb[0]) % 4]
                me = seat_of(r, t, i)
                if (SEATS.index(bidder) - SEATS.index(me)) % 2 != 0:
                    continue                       # the game is theirs
                out.append({"board": r["board"], "table": t, "n": i, "seat": me,
                            "hand": r["hands"][me], "prefix": prefix,
                            "contract": lb[1], "row": r,
                            "imps": r["imp_margin"],
                            "gap": r[f"{t}_par_gap"]})
    return out


def wants_to_move(rec: dict) -> bool:
    h = Hand.parse(rec["hand"])
    controls = sum(2 for c in h.cards if c.rank == 14) + \
        sum(1 for c in h.cards if c.rank == 13)
    short = any(h.suit_length(s) <= 1 for s in "CDHS")
    return controls >= 4 and short


def mean(xs):
    xs = [x for x in xs if x is not None]
    return sum(xs) / len(xs) if xs else 0.0


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("rows")
    ap.add_argument("--trace", type=int, default=0,
                    help="re-score this many of the wants-to-move seats")
    a = ap.parse_args()
    rows = [json.loads(l) for l in open(a.rows)]

    passes = our_game_passes(rows)
    movers = [p for p in passes if wants_to_move(p)]
    rest = [p for p in passes if not wants_to_move(p)]
    print(f"\n=== {a.rows}: {len(rows)} boards ===")
    print(f"we pass our own side's game contract: {len(passes)} seats")
    print(f"  of those, 4+ controls AND a singleton/void: {len(movers)}")
    print(f"    board margin {mean(m['imps'] for m in movers):+.2f}   "
          f"par gap {mean(m['gap'] for m in movers):+.2f}")
    print(f"  the rest ({len(rest)}):")
    print(f"    board margin {mean(m['imps'] for m in rest):+.2f}   "
          f"par gap {mean(m['gap'] for m in rest):+.2f}")

    if a.trace:
        print(f"\n--- what the engine offers {min(a.trace, len(movers))} of those seats ---")
        nonpass_counts, best_fits, offered = [], [], Counter()
        for m in movers[:a.trace]:
            cands = rank(m["hand"], m["row"]["dealer"], m["row"]["vul"],
                         m["seat"], m["prefix"], top=20)
            nb = [c for c in cands if c["call"] != "P"]
            nonpass_counts.append(len(nb))
            best_fits.append(max((c["fit"] for c in nb), default=0.0))
            for c in nb:
                offered[c["call"]] += 1
        print(f"  mean non-pass candidates offered: "
              f"{sum(nonpass_counts)/len(nonpass_counts):.2f}")
        print(f"  best non-pass fit < 0.10 in {sum(1 for f in best_fits if f < 0.10)}"
              f" of {len(best_fits)}; < 0.50 in {sum(1 for f in best_fits if f < 0.50)}"
              f"; >= 0.90 in {sum(1 for f in best_fits if f >= 0.90)}")
        print(f"  the calls ever offered: {offered.most_common()}")

    # --- the slam band -----------------------------------------------------
    # WHO bid it matters: at table A our engine holds N/S and BEN holds E/W,
    # at table B the sides are swapped.  Counting every slam at table A as
    # ours inflates our total by every slam BEN bid sitting E/W - which is
    # how a first pass at this made us look like the boldest pair at the club.
    slam_bid, made = Counter(), Counter()
    for r in rows:
        for t, our_seats in (("a", "NS"), ("b", "EW")):
            c = r[f"{t}_contract"]
            if c == "passed out" or " by " not in c:
                continue
            lvl = int(c[0])
            declarer = c.split(" by ")[1].split()[0]
            who = "us" if declarer in our_seats else "ben"
            if lvl >= 6:
                slam_bid[who] += 1
                tricks = int(c.split("(")[1].split()[0])
                if tricks >= 6 + lvl:
                    made[who] += 1
    print()
    for who in ("us", "ben"):
        n, m = slam_bid[who], made[who]
        print(f"slams bid by {who:3s}: {n:3d}, made {m:3d}"
              + (f" ({100*m/n:.0f}%)" if n else ""))
    print("(the IMP break-even for a small slam is about 50%: a hit rate far")
    print(" above it is under-bidding, not accuracy)")


if __name__ == "__main__":
    main()
