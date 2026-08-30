"""Replay every decision we made in a recorded match under the CURRENT system
and report the ones that change.  The blast radius of an edit, before any match."""
import json, sys, time
sys.path.insert(0, str(__import__('pathlib').Path(__file__).resolve().parent))
from repro import at, seat_of

rows = [json.loads(l) for l in open(sys.argv[1])]
n = 0; changed = []; t0 = time.time()
for r in rows:
    for t in ("a", "b"):
        calls = r[f"{t}_auction"].split()
        for oc in r[f"{t}_our_calls"]:
            i = oc["n"]
            if i >= len(calls):
                continue
            n += 1
            try:
                d = at(r, t, i)
            except Exception:
                continue
            if d["chosen_call"] != oc["call"]:
                changed.append((r["board"], t, i, seat_of(r, t, i), r["hands"][seat_of(r, t, i)],
                                oc["call"], oc["rule"], d["chosen_call"],
                                d["explanation"]["source_rule_id"], r["imp_margin"]))
print(f"{n} decisions replayed in {time.time()-t0:.0f}s: {len(changed)} change")
for b, t, i, s, h, a, ar, c, cr, m in changed[:40]:
    print(f"  {b}{t} n={i:2d} {s} {h:18s} ({m:+3d})  {a}({ar}) -> {c}({cr})")
