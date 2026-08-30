#!/usr/bin/env python3
"""Every board we lost, every decision BEN disagreed with, grouped into families.

`ben_audit.py` ranks individual leads.  With 1000 deals it produces well over a
thousand of them, which is more than any round can read one at a time.  This
tool is the digest: it joins the audit to the match rows, resolves the rule that
ACTUALLY DECIDED each call, and groups the disagreements so a whole family can be
ruled on once while still having looked at every board.

Two things it fixes structurally, both of which have cost the project findings:

  * **The primary-reading trap.**  The `rule` field in the match rows and the
    audit is the highest-priority rule that produces the same CALL, which is not
    necessarily the rule that matched.  Round 13 wrote three findings against the
    wrong rule.  Here every row is re-resolved through the live engine and the
    deciding rule is `explanation.source_rule_id`.
  * **The signed par gap.**  `par_gap` in the match rows is N/S-signed at BOTH
    tables, so ours is `+a_par_gap` at table A and `-b_par_gap` at table B.  Read
    at face value it inverts the verdict on whole families.  `gap` below is
    always ours, already signed.

Board margin and par gap disagree in both directions; the par gap is the
attributable one and the margin is the one that shows up in the match.  Both are
printed, always.

    python3 tools/roundkit/sweep.py --rows R --audit A --families
    python3 tools/roundkit/sweep.py --rows R --audit A --families --min-n 3
    python3 tools/roundkit/sweep.py --rows R --audit A --family uc_pass
    python3 tools/roundkit/sweep.py --rows R --audit A --context general_competitive_low
    python3 tools/roundkit/sweep.py --rows R --audit A --boards
    python3 tools/roundkit/sweep.py --rows R --audit A --board 17
    python3 tools/roundkit/sweep.py --rows R --audit A --cache reports/r15_sweep.json
"""
from __future__ import annotations

import argparse, json, sys, time
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from repro import at, context_at, rank_at, seat_of  # noqa: E402


def deciding_rule(cands):
    """The rule that ACTUALLY decided the call, reconstructing `fast_decision`.

    `explanation.source_rule_id` is the PRIMARY READING - the highest-priority
    rule producing the same call - which is what the call MEANS in the system,
    not what chose it.  `repro.rank_at` returns SCORE order, whose first row is
    not the choice either.  `fast_decision` keeps every candidate fitting >= 0.9
    and takes the highest priority among those; only if none fits does the
    blended score decide.  Round 15 wrote a finding against `rr_nt_slam3_S`
    (priority 56, floor 19 HCP) that has never fired: the hand was a 15-count and
    `rr_nt_gf3_S` (priority 53.5) matched it at 1.00, bidding the same 3S.

    Validated against the engine on 598 consecutive decisions: 0 mismatches.
    """
    sat = [c for c in cands if c["fit"] >= 0.9]
    return max(sat, key=lambda c: (c["prio"], c["fit"])) if sat else cands[0]


def our_gap(row, table):
    """The par gap FOR US at this table, correctly signed."""
    return row["a_par_gap"] if table == "a" else -row["b_par_gap"]


def resolve(rows_path, audit_path, cache=None):
    """Join audit -> match, re-resolve the deciding rule and live context."""
    if cache and Path(cache).exists():
        return json.loads(Path(cache).read_text())

    rows = {r["board"]: r for r in map(json.loads, open(rows_path))}
    audit = [json.loads(l) for l in open(audit_path)]
    out, t0 = [], time.time()
    for k, a in enumerate(audit):
        r = rows.get(a["board"])
        if r is None:
            continue
        try:
            d = at(r, a["table"], a["index"])
            cands = rank_at(r, a["table"], a["index"])
            ctx = context_at(r["hands"][a["seat"]], r["dealer"], r["vul"], a["seat"],
                             r[f"{a['table']}_auction"].split()[: a["index"]])
        except Exception as e:                        # a seat we can no longer reach
            d, cands, ctx = None, [], [f"<error: {type(e).__name__}>"]
        rec = dict(a)
        best = deciding_rule(cands) if cands else None
        rec["decided_by"] = best["rule"] if best else "?"
        rec["reading"] = (d or {}).get("explanation", {}).get("source_rule_id", "?")
        rec["fit"] = best["fit"] if best else 0.0
        rec["replayed"] = (d or {}).get("chosen_call", "?")
        rec["contexts"] = ctx
        rec["gap"] = our_gap(r, a["table"])
        out.append(rec)
        if k % 200 == 0:
            print(f"  ...{k}/{len(audit)} ({time.time()-t0:.0f}s)", file=sys.stderr)
    if cache:
        Path(cache).write_text(json.dumps(out))
    return out


def index_corpus(rows_path, cache):
    """Re-resolve EVERY decision we made in a corpus, not just the losing boards.

    This is the denominator no other tool produces correctly.  `repro.fires()`
    keys on the match row's `rule` field, which is the primary reading; a family
    accused on that basis may not contain the rule that actually decided any of
    it.  Here every decision is replayed and keyed on `source_rule_id`, and the
    par gap is signed for US at both tables.
    """
    if cache and Path(cache).exists():
        return json.loads(Path(cache).read_text())
    rows = [json.loads(l) for l in open(rows_path)]
    out, t0 = [], time.time()
    for k, r in enumerate(rows):
        for t in ("a", "b"):
            calls = r[f"{t}_auction"].split()
            for oc in r[f"{t}_our_calls"]:
                i = oc["n"]
                if i >= len(calls):
                    continue
                try:
                    cands = rank_at(r, t, i)
                    if not cands:
                        continue
                    best = deciding_rule(cands)
                except Exception:
                    continue
                out.append(dict(
                    board=r["board"], table=t, index=i, seat=seat_of(r, t, i),
                    hand=r["hands"][seat_of(r, t, i)], call=best["call"],
                    rule=best["rule"], fit=best["fit"],
                    imp=r["imp_margin"], gap=our_gap(r, t),
                    auction=" ".join(calls[:i]),
                ))
        if k % 100 == 0:
            print(f"  ...{k}/{len(rows)} boards ({time.time()-t0:.0f}s)", file=sys.stderr)
    if cache:
        Path(cache).write_text(json.dumps(out))
    return out


def denom(idx, rule_or_call, limit):
    """Whole-corpus population of a rule: tables, board margin, and OUR par gap.

    Board margin and par gap disagree in both directions and the disagreement is
    the point: the gap is what this decision is attributable for, the margin is
    what shows up in the match.  A family above baseline on either is not a
    defect just because BEN dislikes it.
    """
    sel = [d for d in idx if d["rule"] == rule_or_call]
    if not sel:
        print(f"{rule_or_call}: never decides anything in this corpus")
        return
    n = len(sel)
    imps = sum(d["imp"] for d in sel)
    gap = sum(d["gap"] for d in sel) / n
    won = sum(1 for d in sel if d["imp"] > 0)
    lost = sum(1 for d in sel if d["imp"] < 0)
    tot = len(idx)
    base_gap = sum(d["gap"] for d in idx) / tot
    base_imp = sum(d["imp"] for d in idx) / tot
    print(f"{rule_or_call}: decides {n} of {tot} decisions "
          f"({n/tot*100:.2f}%) on {len({(d['board'],d['table']) for d in sel})} tables")
    print(f"  board margin {imps:+d}, mean {imps/n:+.2f}   "
          f"(corpus mean {base_imp:+.2f})   {won} on boards we won / {lost} lost")
    print(f"  OUR par gap  mean {gap:+.2f}                  "
          f"(corpus mean {base_gap:+.2f})")
    print()
    for d in sel[:limit]:
        print(f"  {d['board']}{d['table']} n={d['index']:<2d} {d['seat']} {d['hand']:18s} "
              f"({d['imp']:+3d} gap{d['gap']:+5.1f})  {d['auction'] or '-':<28s} -> {d['call']}")
    if n > limit:
        print(f"  ... {n-limit} more")


def rule_context_map():
    """rule id -> context id, read from the live system (handles $-expansion)."""
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from repro import system
    m = {}
    for c in system().contexts:
        cid = getattr(c, "id", getattr(c, "name", "?"))
        for r in c.rules:
            m.setdefault(r.id, cid)
    return m


def rank_rules(idx, min_n, limit):
    """Rank rules by how far they sit BELOW THEIR OWN CONTEXT on the par gap.

    The corpus mean is the wrong yardstick.  Par gap is jointly owned by the
    whole auction, so a context whose decisions happen on big-swing boards shows
    a bad gap whatever its rules do: `opener_rebid_1m_1M` runs at -4.04 against a
    corpus mean of -0.02, and a rule sitting at -4.16 inside it is at its own
    baseline, not 4 points below the field.  Round 15 nearly wrote up two such
    rules.  What indicts a rule is being below the CONTEXT it competes in.
    """
    cmap = rule_context_map()
    by_rule, by_ctx = defaultdict(list), defaultdict(list)
    for d in idx:
        ctx = cmap.get(d["rule"], "?")
        by_rule[(ctx, d["rule"])].append(d)
        by_ctx[ctx].append(d)
    rows = []
    for (ctx, rule), ds in by_rule.items():
        if len(ds) < min_n:
            continue
        cds = by_ctx[ctx]
        g = sum(d["gap"] for d in ds) / len(ds)
        cg = sum(d["gap"] for d in cds) / len(cds)
        i = sum(d["imp"] for d in ds) / len(ds)
        ci = sum(d["imp"] for d in cds) / len(cds)
        rows.append((g - cg, ctx, rule, len(ds), len(cds), g, cg, i, ci,
                     sum(1 for d in ds if d["imp"] > 0), sum(1 for d in ds if d["imp"] < 0)))
    rows.sort()
    print(f"{'context':32s} {'rule':24s} {'n':>3s} {'/ctx':>5s} {'gap':>7s} "
          f"{'ctxgap':>7s} {'DELTA':>7s} {'imp':>6s} {'ctximp':>7s} {'W':>3s} {'L':>3s}")
    print("-" * 118)
    for d, ctx, rule, n, cn, g, cg, i, ci, w, l in rows[:limit]:
        print(f"{ctx[:32]:32s} {rule[:24]:24s} {n:3d} {cn:5d} {g:+7.2f} {cg:+7.2f} "
              f"{d:+7.2f} {i:+6.2f} {ci:+7.2f} {w:3d} {l:3d}")


def _famkey(rec):
    return (rec["contexts"][0] if rec["contexts"] else "-", rec["decided_by"],
            rec["ours"], rec["ben"])


def families(recs, min_n, min_conf, first_only, sort):
    fam = defaultdict(list)
    for rec in recs:
        if rec["ben_conf"] < min_conf:
            continue
        if first_only and not rec["first_divergence"]:
            continue
        fam[_famkey(rec)].append(rec)
    out = []
    for key, rs in fam.items():
        if len(rs) < min_n:
            continue
        out.append(dict(
            ctx=key[0], rule=key[1], ours=key[2], ben=key[3], n=len(rs),
            imps=sum(r["imp_margin"] for r in rs),
            gap=sum(r["gap"] for r in rs) / len(rs),
            conf=sum(r["ben_conf"] for r in rs) / len(rs),
            first=sum(1 for r in rs if r["first_divergence"]),
            boards=[f"{r['board']}{r['table']}" for r in rs][:8],
        ))
    out.sort(key=lambda f: (-f["n"] if sort == "n" else f["imps"]))
    return out


def print_families(fams):
    print(f"{'context':38s} {'decided by':26s} {'ours':>5s} {'BEN':>5s} "
          f"{'n':>4s} {'IMPs':>6s} {'gap':>7s} {'conf':>5s} {'1st':>4s}")
    print("-" * 118)
    for f in fams:
        print(f"{f['ctx'][:38]:38s} {f['rule'][:26]:26s} {f['ours']:>5s} {f['ben']:>5s} "
              f"{f['n']:4d} {f['imps']:6d} {f['gap']:+7.2f} {f['conf']:5.2f} {f['first']:4d}")
    print(f"\n{len(fams)} families, {sum(f['n'] for f in fams)} decisions")


def print_recs(recs, limit):
    for r in recs[:limit]:
        star = "*" if r["first_divergence"] else " "
        print(f"{star}{r['board']}{r['table']} n={r['index']:<2d} {r['seat']} "
              f"{r['hand']:18s} ({r['imp_margin']:+3d} gap{r['gap']:+5.1f})  "
              f"{r['auction'] or '-':<26s} | we {r['ours']:>4s} ({r['decided_by']}) "
              f"BEN {r['ben']:>4s} {r['ben_conf']:.2f}")
    if len(recs) > limit:
        print(f"  ... {len(recs)-limit} more")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--rows", required=True)
    p.add_argument("--audit")
    p.add_argument("--cache")
    p.add_argument("--families", action="store_true")
    p.add_argument("--boards", action="store_true")
    p.add_argument("--board", type=int)
    p.add_argument("--family")
    p.add_argument("--context")
    p.add_argument("--min-n", type=int, default=1)
    p.add_argument("--min-conf", type=float, default=0.0)
    p.add_argument("--first-only", action="store_true")
    p.add_argument("--sort", choices=["imps", "n"], default="imps")
    p.add_argument("--limit", type=int, default=200)
    p.add_argument("--denom", help="whole-corpus population of a DECIDING rule id")
    p.add_argument("--index-cache", default=None)
    p.add_argument("--rank-rules", action="store_true", dest="rank_rules")
    a = p.parse_args()

    if a.rank_rules:
        rank_rules(index_corpus(a.rows, a.index_cache), a.min_n, a.limit)
        return
    if a.denom:
        denom(index_corpus(a.rows, a.index_cache), a.denom, a.limit)
        return

    recs = resolve(a.rows, a.audit, a.cache)

    if a.families:
        print_families(families(recs, a.min_n, a.min_conf, a.first_only, a.sort))
    elif a.board is not None:
        print_recs([r for r in recs if r["board"] == a.board], a.limit)
    elif a.family:
        sel = [r for r in recs if r["decided_by"] == a.family]
        print(f"{a.family}: {len(sel)} disagreements, "
              f"{sum(r['imp_margin'] for r in sel)} IMPs, "
              f"mean gap {sum(r['gap'] for r in sel)/max(1,len(sel)):+.2f}\n")
        print_recs(sel, a.limit)
    elif a.context:
        sel = [r for r in recs if any(a.context in c for c in r["contexts"])]
        print(f"{a.context}: {len(sel)} disagreements\n")
        print_recs(sel, a.limit)
    elif a.boards:
        by = defaultdict(list)
        for r in recs:
            by[r["board"]].append(r)
        for b in sorted(by, key=lambda b: by[b][0]["imp_margin"]):
            rs = by[b]
            print(f"\n=== board {b}  ({rs[0]['imp_margin']:+d} IMPs)  {rs[0]['contract']}")
            print_recs(sorted(rs, key=lambda r: (r["table"], r["index"])), a.limit)
    else:
        p.error("pick one of --families / --boards / --board / --family / --context")


if __name__ == "__main__":
    main()
