"""Per-decision counterfactual regret, with BEN in the opponents' seats.

Why this replaces par gap
-------------------------
A par gap is jointly owned by a whole auction: it says how far the final
contract landed from what perfect bidding by BOTH sides would reach, not who
is to blame.  Round 15 and round 16 both produced false findings from it, and
round 16's post-mortem states the failure mode outright - "A CLOSING CALL
INHERITS THE AUCTION'S PAR GAP AND EXPLAINS NOTHING", after 461 of 470
suspect decisions turned out to be the last pass of an auction already over.

This measures something a par gap cannot: **at this seat, on this deal,
against this opponent, would a different call have scored better?**

    baseline   the table's actual score - already recorded, so it is free
    alternative  re-play the auction from the same prefix with the substituted
                 call, our engine in OUR two seats and BEN in the OPPONENTS'
                 two seats, then score the contract double-dummy

Two things make that honest, and both are inherited from `tools/regret.py`:

* **Never take the max over alternatives.**  Max-of-noisy-estimates is
  optimistically biased and would "discover" that lying pays whenever partner
  happens to be misled favourably.  Each (rule, alternative) pair is averaged
  over every occurrence with a standard error.
* **Only systemically plausible alternatives.**  A double-dummy rollout
  rewards a lie, because partner then bids as though the lie were true.  An
  alternative must either fit the system at `MIN_ALT_FIT` or be BEN's own
  choice at that seat.

Why BEN in the opponents' seats matters
---------------------------------------
`engine/arbitration.py`'s `rollout` finishes the auction with `decide_fast`
for all four seats while the match is played against BEN.  At a 20%
per-decision disagreement rate and two to four further opponent calls per
rollout, the simulated opponent line is wrong on a third to a half of
rollouts.  BEN is cached here (`tools/ben_cache.py`), so there is no longer
any reason for a rollout in this repo to model the opponents with our own
engine.

The standing caveat, stated so nobody has to rediscover it
----------------------------------------------------------
Partner interprets the substituted call with the UNMODIFIED system, so this
estimates *the value of deviating unilaterally*, not *the value of changing
the rule*.  In a cooperative partnership game those differ and the sign can
flip.  Read a rule's regret as a lead, exactly as a BEN disagreement is a
lead, and confirm it with `roundkit/screen.py` before believing it.

    python3 tools/roundkit/cfr.py run --rows reports/e10_final.jsonl \
        --out reports/cfr_e10.jsonl --jobs 3
    python3 tools/roundkit/cfr.py report --rows reports/cfr_e10.jsonl
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import time
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "src"))

SEATS = "NESW"
MIN_ALT_FIT = 0.35        # below this an "alternative" is a lie, not a call
MAX_ALTS = 3
MAX_CALLS = 60


def _finish(system, ben, deal, dealer, vul, our_side, auction):
    """Finish an auction in progress: our engine in our seats, BEN in theirs.

    This is `match_ben.play_table`'s inner loop starting from a prefix, so a
    rollout is played exactly the way the match itself is played.
    """
    from bridgebidder.domain.calls import Call
    from bridgebidder.domain.types import Seat
    from bridgebidder.engine.decision import decide_fast
    from bridgebidder.inference.engine import prepare_decision

    hands = {s.value: str(deal[s]) for s in Seat}
    vn, ve = int(vul.is_vulnerable(Seat.N)), int(vul.is_vulnerable(Seat.E))
    while not auction.is_complete:
        seat = auction.next_seat
        if seat.side == our_side:
            setup = prepare_decision(system, auction, perspective=seat)
            choice = decide_fast(setup, deal[seat])
            call = choice if isinstance(choice, Call) else choice.call
        else:
            resp = ben.ask({"hands": hands, "dealer": dealer.value,
                            "vuln_ns": vn, "vuln_ew": ve,
                            "auction": [str(c) for c in auction.calls]})
            call = Call.parse(resp["bid"])
            if not auction.is_legal(call):      # BEN is statistical
                call = Call.parse("P")
        auction.add(call)
        if len(auction.calls) > MAX_CALLS:
            break
    return auction


def _board_rows(args):
    """All counterfactuals for one slice of a corpus.  Runs in a subprocess."""
    path, lo, hi = args
    from compare_ben import Ben
    from bridgebidder.domain.auction import Auction
    from bridgebidder.domain.calls import Call
    from bridgebidder.domain.cards import Hand
    from bridgebidder.domain.types import Seat, Vulnerability
    from bridgebidder.engine.dd import EndplayDD
    from bridgebidder.engine.decision import score_candidates
    from bridgebidder.engine.scoring import imps, signed_score
    from bridgebidder.inference.engine import interpret_call, prepare_decision
    from bridgebidder.system.dsl import load_system

    system, ben, dd = load_system(), Ben(), EndplayDD()
    rows, out = [json.loads(l) for l in open(path)][lo:hi], []
    n_dec = n_disagree = 0

    for r in rows:
        deal = {s: Hand.parse(r["hands"][s.value]) for s in Seat}
        dealer, vul = Seat(r["dealer"]), Vulnerability.parse(r["vul"])
        hands = {s.value: str(deal[s]) for s in Seat}
        for t, our_side in (("a", "NS"), ("b", "EW")):
            calls = r[f"{t}_auction"].split()
            base_score = r[f"{t}_score_ns"] if our_side == "NS" else -r[f"{t}_score_ns"]
            for oc in r[f"{t}_our_calls"]:
                i = oc["n"]
                if i >= len(calls):
                    continue
                n_dec += 1
                prefix = calls[:i]
                au = Auction(dealer=dealer, vulnerability=vul)
                for c in prefix:
                    au.add(Call.parse(c))
                seat = au.next_seat
                setup = prepare_decision(system, au, perspective=seat)
                ranked = score_candidates(setup, deal[seat])
                ours = oc["call"]

                bres = ben.ask({"hands": hands, "dealer": dealer.value,
                                "vuln_ns": int(vul.is_vulnerable(Seat.N)),
                                "vuln_ew": int(vul.is_vulnerable(Seat.E)),
                                "auction": prefix})
                bcall = bres.get("bid")
                if bcall == ours:
                    continue                     # BEN agrees: nothing to look at
                n_disagree += 1

                alts, seen = [], {ours}
                if bcall and bcall not in seen:
                    c = Call.parse(bcall)
                    if au.is_legal(c):
                        alts.append((c, "ben", next((s.fit for s in ranked
                                                     if str(s.call) == bcall), 0.0)))
                        seen.add(bcall)
                for s in ranked:
                    if len(alts) >= MAX_ALTS:
                        break
                    if str(s.call) in seen or s.fit < MIN_ALT_FIT:
                        continue
                    alts.append((s.call, "system", s.fit))
                    seen.add(str(s.call))
                if not alts:
                    continue

                interp = interpret_call(setup, Call.parse(ours))
                rule = interp.source_rule_id
                is_closing = all(c == "P" for c in calls[i + 1:]) and len(calls) - i <= 3
                for call, src, fit in alts:
                    au2 = Auction(dealer=dealer, vulnerability=vul)
                    for c in prefix:
                        au2.add(Call.parse(c))
                    au2.add(call)
                    fin = _finish(system, ben, deal, dealer, vul, our_side, au2)
                    c2 = fin.contract
                    if c2 is None:
                        alt_score = 0
                    else:
                        tricks = dd.tricks(deal, c2.declarer, c2.strain)
                        alt_score = signed_score(c2, tricks, vul, our_side)
                    out.append({
                        "board": r["board"], "table": t, "n": i,
                        "seat": seat.value, "auction": " ".join(prefix) or "(open)",
                        "rule": rule, "chosen": ours, "alt": str(call),
                        "alt_source": src, "alt_fit": round(fit, 3),
                        "is_closing": is_closing,
                        "delta_imps": imps(alt_score - base_score),
                        "alt_contract": str(c2) if c2 else "passed_out",
                    })
    ben.close()
    return out, n_dec, n_disagree


def cmd_run(a) -> None:
    total = sum(1 for _ in open(a.rows))
    n = min(a.limit, total) if a.limit else total
    jobs = max(1, a.jobs)
    edges = [round(n * j / jobs) for j in range(jobs + 1)]
    slices = [(a.rows, edges[j], edges[j + 1]) for j in range(jobs)
              if edges[j] < edges[j + 1]]
    t0 = time.time()
    if len(slices) > 1:
        import multiprocessing as mp
        with mp.get_context("spawn").Pool(len(slices)) as pool:
            parts = pool.map(_board_rows, slices)
    else:
        parts = [_board_rows(s) for s in slices]
    rows = [r for p, _, _ in parts for r in p]
    dec = sum(d for _, d, _ in parts)
    dis = sum(d for _, _, d in parts)
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    with open(a.out, "w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    print(f"{n} boards | {dec} of our decisions | BEN disagreed on {dis} "
          f"({100 * dis / dec:.1f}%) | {len(rows)} rollouts | "
          f"{time.time() - t0:.0f}s ({1000 * (time.time() - t0) / max(len(rows), 1):.0f} ms/rollout)")
    print(f"-> {a.out}")


def _stats(vals):
    n = len(vals)
    if not n:
        return 0.0, 0.0, 0
    m = sum(vals) / n
    sd = math.sqrt(sum((v - m) ** 2 for v in vals) / (n - 1)) if n > 1 else 0.0
    return m, sd / math.sqrt(n), n


def cmd_report(a) -> None:
    rows = [json.loads(l) for l in open(a.rows)]
    if a.exclude_closing:
        rows = [r for r in rows if not r["is_closing"]]
    allv = [r["delta_imps"] for r in rows]
    m, se, n = _stats(allv)
    print(f"\n=== {len(rows)} rollouts ===")
    print(f"mean IMP change from substituting an alternative: {m:+.2f} +/- {se:.2f}")
    print("(negative = our call was better than the average alternative, which")
    print(" is the expected sign for a system that mostly bids sensibly)")

    for key, title in (("rule", "RULES"), ("context", "CONTEXTS")):
        if key == "context":
            continue
        by = defaultdict(list)
        for r in rows:
            by[r[key]].append(r["delta_imps"])
        print(f"\n=== {title} an alternative systematically BEATS "
              f"(n >= {a.min_n}, mean > 2 SE) ===")
        found = [(x[0], x[1], x[2], k) for k, v in by.items()
                 for x in [_stats(v)] if x[2] >= a.min_n and x[0] > 2 * x[1]]
        for mm, ss, nn, k in sorted(found, reverse=True)[:a.top]:
            print(f"  {mm:+6.2f} +/- {ss:4.2f}  n={nn:3d}  {k}")
        if not found:
            print("  (none)")
        print(f"\n=== {title} that HOLD UP (alternatives do worse) ===")
        good = [(x[0], x[1], x[2], k) for k, v in by.items()
                for x in [_stats(v)] if x[2] >= a.min_n and x[0] < -2 * x[1]]
        for mm, ss, nn, k in sorted(good)[:a.top]:
            print(f"  {mm:+6.2f} +/- {ss:4.2f}  n={nn:3d}  {k}")
        if not good:
            print("  (none)")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run")
    r.add_argument("--rows", required=True)
    r.add_argument("--out", required=True)
    r.add_argument("--limit", type=int)
    r.add_argument("--jobs", type=int, default=3)
    r.set_defaults(func=cmd_run)
    p = sub.add_parser("report")
    p.add_argument("--rows", required=True)
    p.add_argument("--min-n", type=int, default=8)
    p.add_argument("--top", type=int, default=15)
    p.add_argument("--exclude-closing", action="store_true")
    p.set_defaults(func=cmd_report)
    a = ap.parse_args()
    a.func(a)


if __name__ == "__main__":
    main()
