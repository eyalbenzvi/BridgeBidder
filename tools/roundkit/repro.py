"""Reproduce and dissect one decision.  Read-only; import it or run it.

    cd /home/user/BridgeBidder
    python3 -c "
    import sys; sys.path.insert(0,'SCRATCH')
    from repro import *
    b = board('reports/e7_before.jsonl', 286)
    show(b)
    print(ask('AQ52.KJ4.QT9.KJ7','N','None','N',['P','P']))
    for r in rank('AQ52.KJ4.QT9.KJ7','N','None','N',['P','P']): print(r)
    "
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "src"))

from bridgebidder.api import choose_bid  # noqa: E402
from bridgebidder.domain.auction import Auction  # noqa: E402
from bridgebidder.domain.calls import Call  # noqa: E402
from bridgebidder.domain.cards import Hand  # noqa: E402
from bridgebidder.domain.types import Seat, Vulnerability  # noqa: E402
from bridgebidder.engine.decision import score_candidates  # noqa: E402
from bridgebidder.inference.engine import prepare_decision  # noqa: E402
from bridgebidder.system.dsl import load_system  # noqa: E402

SEATS = "NESW"
_SYS = None


def system():
    global _SYS
    if _SYS is None:
        _SYS = load_system()
    return _SYS


def rows(path):
    return [json.loads(l) for l in open(path)]


def board(path, n):
    for r in rows(path):
        if r["board"] == n:
            return r
    raise SystemExit(f"board {n} not in {path}")


def show(r):
    """Print a board the way the dossier does, plus per-call seats."""
    print(f"Board {r['board']}  margin {r['imp_margin']:+d}  vul {r['vul']}  "
          f"dealer {r['dealer']}  par(NS) {r['par_ns']}")
    for s in "NESW":
        print(f"   {s}: {r['hands'][s]}")
    for t, side in (("a", "NS"), ("b", "EW")):
        print(f"  Table {t.upper()} (we={side}): {r[f'{t}_contract']}")
        calls = r[f"{t}_auction"].split()
        seat = SEATS.index(r["dealer"])
        for i, c in enumerate(calls):
            who = SEATS[(seat + i) % 4]
            print(f"      {i:2d} {who} {c}")
        print(f"    our rules: {[(c['call'], c['rule']) for c in r[f'{t}_our_calls']]}")


def seat_of(r, table, index):
    """Which seat makes call number `index` (0-based) of the given table."""
    return SEATS[(SEATS.index(r["dealer"]) + index) % 4]


def ask(hand, dealer, vul, seat, calls, arb=False):
    """What does the engine bid?  calls = the auction so far, from the dealer."""
    return choose_bid({"hand": hand,
                       "auction_state": {"dealer": dealer, "vulnerability": vul,
                                         "seat": seat, "calls": list(calls)},
                       "use_arbitration": arb})


def at(r, table, index, arb=False):
    """Re-ask the decision at call `index` of `table` from the row itself."""
    calls = r[f"{table}_auction"].split()
    seat = seat_of(r, table, index)
    return ask(r["hands"][seat], r["dealer"], r["vul"], seat, calls[:index], arb=arb)


def rank(hand, dealer, vul, seat, calls, top=12):
    """Every candidate with rule id, fit, blended score and priority."""
    a = Auction(dealer=Seat(dealer), vulnerability=Vulnerability.parse(vul))
    for c in calls:
        a.add(Call.parse(c))
    setup = prepare_decision(system(), a, perspective=Seat(seat))
    out = []
    for sc in score_candidates(setup, Hand.parse(hand))[:top]:
        c = sc.candidate
        out.append({"call": str(sc.call),
                    "rule": (c.rule.id if c.rule else f"FALLBACK:{c.fallback.kind}"
                             if hasattr(c.fallback, "kind") else "FALLBACK"),
                    "fit": round(sc.fit, 3), "score": round(sc.score, 3),
                    "prio": c.priority, "shows": c.shows})
    return out


def rank_at(r, table, index, top=12):
    calls = r[f"{table}_auction"].split()
    seat = seat_of(r, table, index)
    return rank(r["hands"][seat], r["dealer"], r["vul"], seat, calls[:index], top=top)


def context_at(hand, dealer, vul, seat, calls):
    """Which context is interpreting this seat's call?"""
    a = Auction(dealer=Seat(dealer), vulnerability=Vulnerability.parse(vul))
    for c in calls:
        a.add(Call.parse(c))
    setup = prepare_decision(system(), a, perspective=Seat(seat))
    seen = []
    for cand in setup.candidates:
        cid = cand.rule.context_id if cand.rule is not None and hasattr(cand.rule, "context_id") else None
        if cid and cid not in seen:
            seen.append(cid)
    return seen


# --- whole-corpus rescoring: never accuse a rule without this -----------------

def rule_tables(path, rule_id):
    """Every table where `rule_id` made our LAST bid, with the IMP margin
    signed for us.  Winners included - this is the honest denominator."""
    out = []
    for r in rows(path):
        for t in ("a", "b"):
            last = None
            for c in r[f"{t}_our_calls"]:
                if c["call"] != "P":
                    last = c
            rid = (last["rule"] or "fallback") if last else "all-pass"
            if rid == rule_id:
                m = r["imp_margin"]
                out.append({"board": r["board"], "table": t, "imps": m,
                            "contract": r[f"{t}_contract"],
                            "auction": r[f"{t}_auction"]})
    return out


def rule_summary(path, rule_id):
    ts = rule_tables(path, rule_id)
    if not ts:
        return f"{rule_id}: no tables"
    tot = sum(t["imps"] for t in ts)
    w = sum(1 for t in ts if t["imps"] > 0)
    l = sum(1 for t in ts if t["imps"] < 0)
    return (f"{rule_id}: {len(ts)} tables, {tot:+d} IMPs, "
            f"{w} wins / {l} losses, mean {tot/len(ts):+.2f}")


def fires(path, rule_id):
    """Every table where the rule fired ANYWHERE in our auction (not just last)."""
    out = []
    for r in rows(path):
        for t in ("a", "b"):
            for c in r[f"{t}_our_calls"]:
                if c["rule"] == rule_id:
                    out.append({"board": r["board"], "table": t,
                                "imps": r["imp_margin"], "call": c["call"],
                                "auction": r[f"{t}_auction"]})
                    break
    return out


def fires_summary(path, rule_id):
    fs = fires(path, rule_id)
    if not fs:
        return f"{rule_id}: never fires"
    tot = sum(f["imps"] for f in fs)
    return (f"{rule_id}: fires on {len(fs)} tables, board margin {tot:+d}, "
            f"mean {tot/len(fs):+.2f}")
