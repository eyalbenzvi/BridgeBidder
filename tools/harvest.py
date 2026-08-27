#!/usr/bin/env python3
"""Bulk self-play harvester: deal boards, bid them, detect anomalies.

Usage:
    python tools/harvest.py --n 50 --seed 1 --out reports/round1.jsonl
    python tools/harvest.py --report reports/round1.jsonl      # triage summary

Detectors (per board):
  hard_failure       crash / illegal call / runaway / replay divergence /
                     game force passed out below game
  misbid             a call whose own interpretation the hand badly fails
  missed_game        uncontested: par says our game/slam, we stopped short
  overboard          uncontested: bid game down 2+ though par is a partscore
  absurd_contract    5+ level doubled down 3+, sub-7-card final fit with an
                     8+ fit available, 20+ HCP side passing a board out
  empty_descriptor   a call made some player's descriptor unsatisfiable
  fallback           undiscussed calls (content gaps; tracked for frequency)
  par_loss           IMPs lost vs double-dummy par (both sides; outliers)
"""

from __future__ import annotations

import argparse
import json
import random
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from bridgebidder.domain.auction import Auction
from bridgebidder.domain.cards import FULL_DECK, Hand
from bridgebidder.domain.types import Seat, Vulnerability
from bridgebidder.engine.decision import decide_fast
from bridgebidder.engine.dd import get_dd
from bridgebidder.engine.scoring import contract_score, imps, signed_score
from bridgebidder.engine.selfplay import self_play
from bridgebidder.inference.engine import analyze, prepare_decision
from bridgebidder.system.dsl import load_system

VULS = [Vulnerability.NONE, Vulnerability.NS, Vulnerability.EW, Vulnerability.BOTH]

MISBID_FIT_THRESHOLD = 0.5
PAR_LOSS_FLAG_IMPS = 5


def _par_score_ns(deal: dict, vul: Vulnerability, dealer: Seat) -> int | None:
    """Double-dummy par score from NS's point of view (endplay)."""
    try:
        from endplay.dds import calc_dd_table, par
        from endplay.types import Deal, Player, Vul

        pbn = "N:" + " ".join(str(deal[s]) for s in (Seat.N, Seat.E, Seat.S, Seat.W))
        vmap = {Vulnerability.NONE: Vul.none, Vulnerability.NS: Vul.ns,
                Vulnerability.EW: Vul.ew, Vulnerability.BOTH: Vul.both}
        pmap = {Seat.N: Player.north, Seat.E: Player.east,
                Seat.S: Player.south, Seat.W: Player.west}
        table = calc_dd_table(Deal(pbn))
        return int(par(table, vmap[vul], pmap[dealer]).score)
    except Exception:
        return None


STRAINS = ("C", "D", "H", "S", "NT")


def _best_score_for_side(deal: dict, side: str, vul: Vulnerability, dd,
                         strain: str | None = None) -> int:
    """Best score this side could reach on this deal, choosing declarer,
    strain and level freely (no interference).  With `strain` given, the best
    score available *in that strain*.

    This is the yardstick for CONSTRUCTIVE bidding: unlike par it contains no
    assumption about the opponents' sacrifices or our defence, so the whole
    gap is attributable to our own bidding.
    """
    from bridgebidder.domain.auction import Contract

    best = -10000
    strains = (strain,) if strain else STRAINS
    for declarer in [s for s in Seat if s.side == side]:
        for st in strains:
            tricks = dd.tricks(deal, declarer, st)
            for level in range(1, 8):
                c = Contract(level=level, strain=st, declarer=declarer, doubled=0)
                best = max(best, contract_score(c, tricks, vul))
    return best


def _game_reached(auction: Auction) -> bool:
    lb = auction.last_bid
    if lb is None:
        return False
    return (lb.strain == "NT" and lb.level >= 3) or \
           (lb.strain in ("H", "S") and lb.level >= 4) or \
           (lb.strain in ("C", "D") and lb.level >= 5)


def harvest_board(system, deal, dealer, vul, dd) -> dict:
    """Self-play one board and run every detector. Returns a record dict."""
    rec: dict = {
        "dealer": dealer.value,
        "vul": vul.value,
        "hands": {s.value: str(deal[s]) for s in Seat},
        "issues": [],
        "calls": [],
    }

    def issue(kind: str, signature: str, detail: str, imp_cost: float = 0.0) -> None:
        rec["issues"].append({"kind": kind, "signature": signature,
                              "detail": detail, "imp_cost": round(imp_cost, 1)})

    # ---- self-play (hard failures) ----
    try:
        auction = self_play(system, deal, dealer, vul)
    except Exception as e:
        issue("hard_failure", f"selfplay:{type(e).__name__}", str(e)[:200])
        return rec
    rec["auction"] = [str(c) for c in auction.calls]

    analysis = analyze(system, auction)
    prefix = Auction(dealer=dealer, vulnerability=vul)
    fallback_calls = 0
    for ann in analysis.annotations:
        interp = ann.interpretation
        seat = ann.seat
        setup = prepare_decision(system, prefix, perspective=seat)
        # replay divergence (this is the sampler-critical invariant)
        replayed = decide_fast(setup, deal[seat])
        if str(replayed) != str(ann.call):
            issue("hard_failure", "replay_divergence",
                  f"{prefix} -> {ann.call} vs replay {replayed}")
        # misbid: the hand badly fails its own call's interpretation
        if not ann.call.is_pass:
            cand = next((c for c in setup.candidates if c.call == ann.call), None)
            ctx = setup.candidate_ctx(cand) if cand else setup.eval_ctx
            fit = interp.constraint.fit(deal[seat], ctx)
            if fit < MISBID_FIT_THRESHOLD:
                sig = f"misbid:{interp.source_rule_id}"
                issue("misbid", sig,
                      f"{seat.value} bid {ann.call} ({interp.shows_text!r}) with "
                      f"{deal[seat]} fit={fit:.2f} after {prefix}")
        if interp.is_fallback and not ann.call.is_pass:
            fallback_calls += 1
            tail = "-".join(str(c) for c in prefix.calls[-3:]) or "(open)"
            issue("fallback", f"fallback:{tail}->{ann.call}",
                  f"{seat.value}: {ann.call} after {prefix}", 0.0)
        rec["calls"].append({
            "seat": seat.value, "call": str(ann.call),
            "rule": interp.source_rule_id, "fallback": interp.is_fallback,
        })
        prefix.add(ann.call)

    # descriptor sanity: nobody's accumulated constraints may be unsatisfiable
    for s in Seat:
        if analysis.descriptors[s].box.is_empty:
            issue("empty_descriptor", "empty_descriptor",
                  f"{s.value}'s descriptor is empty after {auction}")

    # GF discipline
    contract = auction.contract
    for side in ("NS", "EW"):
        st = analysis.sides[side]
        if st.game_forced and contract is not None:
            if contract.declarer.side == side and not _game_reached(auction) \
               and contract.doubled == 0:
                issue("hard_failure", "gf_below_game",
                      f"{side} game-forced but played {contract}: {auction}")

    # ---- scoring vs par ----
    if contract is not None:
        tricks = dd.tricks(deal, contract.declarer, contract.strain)
    else:
        tricks = 0
    actual_ns = signed_score(contract, tricks, vul, "NS")
    par_ns = _par_score_ns(deal, vul, dealer)
    rec["contract"] = str(contract) if contract else "passed_out"
    rec["tricks"] = tricks
    rec["score_ns"] = actual_ns
    rec["par_ns"] = par_ns
    if par_ns is not None:
        loss_ns = max(0, imps(par_ns - actual_ns))
        loss_ew = max(0, imps(actual_ns - par_ns))
        rec["par_loss_imps"] = {"NS": loss_ns, "EW": loss_ew}
        competitive = auction.is_competitive

        # game accuracy checks: uncontested auctions only (par assumes
        # double-dummy sacrifices, so competitive boards use outlier flags)
        if not competitive and contract is not None:
            bidding_side = contract.declarer.side
            par_for_us = par_ns if bidding_side == "NS" else -par_ns
            us_loss = loss_ns if bidding_side == "NS" else loss_ew
            game_par = abs(par_ns) >= 300 and (par_for_us > 0)
            if game_par and not _game_reached(auction) and us_loss >= PAR_LOSS_FLAG_IMPS:
                issue("missed_game", f"missed_game:{contract.strain}",
                      f"par {par_ns:+d} but stopped in {contract} ({auction})", us_loss)
            need = 6 + contract.level
            if _game_reached(auction) and tricks <= need - 2 and abs(par_ns) < 300:
                issue("overboard", f"overboard:{contract.strain}",
                      f"bid {contract}, {need - tricks} down, par {par_ns:+d} ({auction})",
                      us_loss)
        # outliers, any auction type
        big = max(loss_ns, loss_ew)
        # only a last-resort flag: skip when a real detector already fired.
        # (fallback entries are informational and must NOT suppress it, or the
        # flag rate moves whenever the fallback rate does)
        already = [i for i in rec["issues"] if i["kind"] != "fallback"]
        if big >= PAR_LOSS_FLAG_IMPS and not already:
            side = "NS" if loss_ns >= loss_ew else "EW"
            issue("par_loss", f"par_loss:{side}",
                  f"{side} lost {big} IMPs vs par {par_ns:+d}: {contract} ({auction})", big)

    # ---- constructive gap: uncontested auctions only, so the whole gap is
    # our own bidding rather than their sacrifices or our defence ----
    if contract is not None and not auction.is_competitive:
        side = contract.declarer.side
        actual = contract_score(contract, tricks, vul)
        best_any = _best_score_for_side(deal, side, vul, dd)
        best_same_strain = _best_score_for_side(deal, side, vul, dd, contract.strain)
        rec["constructive"] = {
            "actual": actual,
            "best": best_any,
            "gap_imps": max(0, imps(best_any - actual)),
            "level_gap_imps": max(0, imps(best_same_strain - actual)),
            "strain_gap_imps": max(0, imps(best_any - best_same_strain)),
            "best_strain_beats_ours": best_any > best_same_strain,
        }

    # absurd contracts
    if contract is not None:
        need = 6 + contract.level
        decl_side = contract.declarer.side
        decl_loss = (rec.get("par_loss_imps") or {}).get(decl_side, 0)
        if contract.level >= 5 and contract.doubled and tricks <= need - 3 \
                and decl_loss >= PAR_LOSS_FLAG_IMPS:
            # ... but a doubled sacrifice that still beat par is good bridge
            issue("absurd_contract", "high_doubled_disaster",
                  f"{contract} down {need - tricks}, {decl_loss} IMPs worse than par ({auction})",
                  decl_loss)
        if contract.strain != "NT":
            decl_side = contract.declarer.side
            us = [s for s in Seat if s.side == decl_side]
            fit = sum(deal[s].suit_length(contract.strain) for s in us)
            best_fit = max(sum(deal[s].suit_length(x) for s in us) for x in "SHDC")
            if fit <= 6 and best_fit >= 8 and contract.level >= 3:
                issue("absurd_contract", "wrong_fit",
                      f"{contract} on a {fit}-card fit; {best_fit}-card fit existed ({auction})")
    else:
        for side in ("NS", "EW"):
            hcp = sum(deal[s].hcp for s in Seat if s.side == side)
            if hcp >= 21:
                issue("absurd_contract", "passed_out_with_values",
                      f"{side} held {hcp} HCP combined but board passed out")
    return rec


def run(n: int, seed: int, out: Path) -> None:
    system = load_system()
    dd = get_dd()
    rng = random.Random(seed)
    out.parent.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    n_issues = 0
    with open(out, "w") as f:
        for i in range(n):
            deck = list(FULL_DECK)
            rng.shuffle(deck)
            deal = {s: Hand(deck[j * 13:(j + 1) * 13]) for j, s in enumerate(Seat)}
            rec = harvest_board(system, deal, Seat.from_index(i % 4), VULS[(i // 4) % 4], dd)
            rec["board"] = i
            rec["seed"] = seed
            n_issues += len([x for x in rec["issues"] if x["kind"] != "fallback"])
            f.write(json.dumps(rec) + "\n")
    print(f"harvested {n} boards in {time.time() - t0:.1f}s -> {out} "
          f"({n_issues} non-fallback issues)")


def report(path: Path) -> None:
    recs = [json.loads(line) for line in open(path)]
    n = len(recs)
    clusters: dict[str, list] = defaultdict(list)
    for r in recs:
        for iss in r["issues"]:
            clusters[iss["signature"]].append((r, iss))
    total_loss = Counter()
    for r in recs:
        for side, v in (r.get("par_loss_imps") or {}).items():
            total_loss[side] += v
    boards_with_issues = sum(1 for r in recs if any(i["kind"] != "fallback" for i in r["issues"]))
    fallback_rate = sum(1 for r in recs for c in r.get("calls", []) if c["fallback"] and c["call"] != "P")

    con = [r["constructive"] for r in recs if r.get("constructive")]
    if con:
        g = sum(c["gap_imps"] for c in con) / len(con)
        lg = sum(c["level_gap_imps"] for c in con) / len(con)
        sg = sum(c["strain_gap_imps"] for c in con) / len(con)
        print(f"constructive gap (uncontested, n={len(con)}): {g:.2f} IMPs/board "
              f"(level {lg:.2f}, strain {sg:.2f})")
    print(f"boards: {n} | boards with real issues: {boards_with_issues} "
          f"({100 * boards_with_issues / n:.0f}%)")
    print(f"total IMPs lost vs par: NS {total_loss['NS']}, EW {total_loss['EW']} "
          f"(avg {sum(total_loss.values()) / n:.2f}/board)")
    print(f"non-pass fallback calls: {fallback_rate}\n")
    ranked = sorted(clusters.items(),
                    key=lambda kv: (-sum(i['imp_cost'] for _, i in kv[1]), -len(kv[1])))
    for sig, items in ranked:
        cost = sum(i["imp_cost"] for _, i in items)
        print(f"[{len(items):3}x | {cost:5.0f} IMPs] {sig}")
        for r, iss in items[:2]:
            print(f"      b{r['board']}: {iss['detail'][:150]}")
    if not ranked:
        print("no issues found")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=50)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--out", type=Path, default=Path("reports/harvest.jsonl"))
    ap.add_argument("--report", type=Path)
    args = ap.parse_args()
    if args.report:
        report(args.report)
    else:
        run(args.n, args.seed, args.out)
