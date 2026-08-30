"""Split a corpus by how many tricks are actually available, and read the loss.

The consolidated review's headline is that 67% of the held-out deficit sits on
the 14% of deals where a slam exists.  That is a claim about a double-dummy
partition of the corpus, so it can be checked exactly - and, more usefully,
the same partition says WHERE in the auction the missed slams are lost, which
is the question that decides what a slam project should build.

    python3 tools/roundkit/slamband.py reports/held_final.jsonl
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "src"))

from bridgebidder.domain.cards import Hand                # noqa: E402
from bridgebidder.domain.types import Seat                # noqa: E402
from bridgebidder.engine.dd import EndplayDD              # noqa: E402

SEATS = "NESW"


def main(path: str) -> None:
    rows = [json.loads(l) for l in open(path)]
    dd = EndplayDD(cache_size=len(rows) + 10)
    deals = [{s: Hand.parse(r["hands"][s.value]) for s in Seat} for r in rows]
    for i in range(0, len(deals), 200):
        dd.prefetch(deals[i:i + 200])

    bands: dict[str, list] = {"12-13": [], "11": [], "<=10": []}
    for r, deal in zip(rows, deals):
        best = max(dd.tricks(deal, s, st) for s in Seat for st in ("C", "D", "H", "S", "NT"))
        key = "12-13" if best >= 12 else ("11" if best == 11 else "<=10")
        r["_best"] = best
        bands[key].append(r)

    print(f"\n=== {path}: {len(rows)} boards, partitioned double-dummy ===")
    tot = sum(r["imp_margin"] for r in rows)
    print(f"whole corpus: {tot:+d} IMPs")
    for k in ("12-13", "11", "<=10"):
        v = bands[k]
        s = sum(r["imp_margin"] for r in v)
        print(f"  best side can take {k:>5}: n={len(v):4d}  "
              f"{s:+5d} IMPs  ({s/len(v):+.2f} per board)  "
              f"= {100*s/tot:.0f}% of the deficit" if v else f"  {k}: none")

    # where do we stop on the deals where a slam is there and BEN bid one?
    print("\n--- deals with 12+ tricks available: what each pair did ---")
    stops: Counter = Counter()
    us_bid = ben_bid = both = neither = 0
    for r in bands["12-13"]:
        def level_of(t, our):
            c = r[f"{t}_contract"]
            if c == "passed out" or " by " not in c:
                return 0, "passed out"
            return int(c[0]), c
        la, ca = level_of("a", True)
        lb, cb = level_of("b", True)
        # our contract is table A when we declare N/S there, table B when E/W
        da = ca.split(" by ")[1].split()[0] if " by " in ca else ""
        db = cb.split(" by ")[1].split()[0] if " by " in cb else ""
        ours = la if da in "NS" else 0
        bens = lb if db in "NS" else 0
        # (table B: BEN sits N/S)
        if ours >= 6 and bens >= 6:
            both += 1
        elif ours >= 6:
            us_bid += 1
        elif bens >= 6:
            ben_bid += 1
            # where did OUR auction stop, and what was our last call?
            calls = r["a_auction"].split()
            lastbid = next((c for c in reversed(calls) if c not in ("P", "X", "XX")), "-")
            ourlast = [c["call"] for c in r["a_our_calls"] if c["call"] != "P"]
            stops[(lastbid, ourlast[-1] if ourlast else "-")] += 1
        else:
            neither += 1
    print(f"  both bid a slam {both} | only we did {us_bid} | "
          f"only BEN did {ben_bid} | neither {neither}")
    print("\n  where OUR auction stopped on the ones only BEN bid "
          "(final contract, our last bid):")
    for (final, mine), n in stops.most_common(15):
        print(f"    {n:3d}  final {final:4s}  our last bid {mine}")


if __name__ == "__main__":
    for p in sys.argv[1:]:
        main(p)
