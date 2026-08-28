"""Triage a 1000-board match: cluster the losing boards so experts read
clusters (with examples) instead of 380 individual deals."""
import json, sys
from collections import defaultdict

rows = [json.loads(l) for l in open(sys.argv[1])]
lost = [r for r in rows if r["imp_margin"] < 0]
total = sum(r["imp_margin"] for r in rows)
gross = -sum(r["imp_margin"] for r in lost)

def our_table_gap(r, t):
    """our side's par gap at table t (positive = we beat par)."""
    g = r[f"{t}_par_gap"]
    if g is None: return 0
    return g if t == "a" else -g

def worse_table(r):
    """the table where WE did worse against par."""
    return "a" if our_table_gap(r, "a") <= our_table_gap(r, "b") else "b"

def last_rule(r, t):
    last = None
    for c in r[f"{t}_our_calls"]:
        if c["call"] != "P":
            last = c
    return (last["rule"] or "fallback") if last else "all-pass"

def auction_family(r, t):
    a = r[f"{t}_auction"].split()
    while a and a[0] == "P": a = a[1:]
    return " ".join(a[:3])

clusters = defaultdict(list)
for r in lost:
    t = worse_table(r)
    key = last_rule(r, t)
    clusters[key].append((r, t))

ranked = sorted(clusters.items(), key=lambda kv: sum(x[0]["imp_margin"] for x in kv[1]))

def fmt_board(r, t, full=True):
    out = [f"### Board {r['board']} | we lost {-r['imp_margin']} IMPs | vul {r['vul']} dealer {r['dealer']} | par(NS) {r['par_ns']} | damage table {t.upper()} (we={'NS' if t=='a' else 'EW'})"]
    for s in "NESW": out.append(f"    {s}: {r['hands'][s]}")
    for tt, side in (("a", "NS"), ("b", "EW")):
        out.append(f"  Table {tt.upper()} (we={side}): {r[f'{tt}_contract']:24s} {r[f'{tt}_auction']}")
        out.append(f"    our rules: {[(c['call'], c['rule']) for c in r[f'{tt}_our_calls']]}")
    return "\n".join(out)

lines = [f"# Triaged dossier: seed {sys.argv[2]}, {len(rows)} boards, margin {total:+d} IMPs",
         f"# {len(lost)} losing boards, {gross} IMPs gross.  Clustered by the rule that made",
         "# our last bid at the table where we did worse against par (correlational - the",
         "# rule may be a symptom of a missing agreement upstream; judge the auctions).",
         ""]
covered = set()
lines.append("## CLUSTERS (by total IMPs lost)\n")
kept = 0
for rule, members in ranked:
    tot = -sum(r["imp_margin"] for r, _ in members)
    if len(members) < 3 and tot < 15:
        continue
    kept += 1
    if kept > 20: break
    members.sort(key=lambda x: x[0]["imp_margin"])
    fams = defaultdict(int)
    for r, t in members: fams[auction_family(r, t)] += 1
    lines.append(f"--- CLUSTER {kept}: last rule `{rule}` | {len(members)} boards | {tot} IMPs lost")
    lines.append(f"    auction families: {dict(sorted(fams.items(), key=lambda kv: -kv[1]))}")
    lines.append(f"    all boards: {[(r['board'], r['imp_margin']) for r, _ in members]}")
    for r, t in members[:4]:
        covered.add(r["board"])
        lines.append(fmt_board(r, t))
    lines.append("")

lines.append("## WORST SINGLE BOARDS not shown above\n")
singles = sorted((r for r in lost if r["board"] not in covered), key=lambda r: r["imp_margin"])
n = 0
for r in singles:
    if n >= 30: break
    if -r["imp_margin"] < 9: break
    n += 1
    lines.append(fmt_board(r, worse_table(r)))
    lines.append("")

out = "\n".join(lines)
open(sys.argv[3], "w").write(out)
print(f"clusters kept: {kept}, boards shown: {len(covered)} + {n} singles, dossier lines: {len(lines)}")
