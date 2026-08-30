"""Paired comparison of two match runs on the SAME deals.

    python3 paired.py reports/before.jsonl reports/after.jsonl [--list]

Reports the total margins, the paired delta, and only the boards whose auction
actually changed (the rest are bit-identical and carry no sampling noise).
"""
import json
import sys


def load(p):
    return {r["board"]: r for r in (json.loads(l) for l in open(p))}


def main(bp, ap, show=False):
    b, a = load(bp), load(ap)
    common = sorted(set(b) & set(a))
    tb = sum(b[i]["imp_margin"] for i in common)
    ta = sum(a[i]["imp_margin"] for i in common)
    changed = [i for i in common
               if b[i]["a_auction"] != a[i]["a_auction"]
               or b[i]["b_auction"] != a[i]["b_auction"]]
    d = [(i, a[i]["imp_margin"] - b[i]["imp_margin"]) for i in changed]
    up = [x for x in d if x[1] > 0]
    dn = [x for x in d if x[1] < 0]
    print(f"boards: {len(common)}")
    print(f"before: {tb:+d}   after: {ta:+d}   paired delta: {ta - tb:+d}")
    print(f"auctions changed on {len(changed)} boards: {len(up)} up, {len(dn)} down, "
          f"{len(changed) - len(up) - len(dn)} same margin")
    print(f"net over changed boards: {sum(x[1] for x in d):+d}")
    if show:
        for i, delta in sorted(d, key=lambda x: x[1]):
            if delta == 0:
                continue
            print(f"\nboard {i}: {delta:+d}   ({b[i]['imp_margin']:+d} -> {a[i]['imp_margin']:+d})")
            for t in ("a", "b"):
                if b[i][f"{t}_auction"] != a[i][f"{t}_auction"]:
                    print(f"  table {t.upper()} before: {b[i][f'{t}_contract']:22s} {b[i][f'{t}_auction']}")
                    print(f"  table {t.upper()} after : {a[i][f'{t}_contract']:22s} {a[i][f'{t}_auction']}")


if __name__ == "__main__":
    args = [x for x in sys.argv[1:] if not x.startswith("--")]
    main(args[0], args[1], show="--list" in sys.argv)
