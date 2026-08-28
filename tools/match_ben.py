"""Head-to-head duplicate match: our engine against BEN.

Each board is played twice, as a teams match is: at table A our engine holds
N/S and BEN holds E/W, at table B the same deal is dealt again with the sides
swapped.  Both tables use the same dealer and vulnerability, so the deal's own
luck cancels and what is left is the difference between the two bidders.

Three numbers come out of it:

  IMP margin   imps(score_ns_A - score_ns_B), signed for us.  This is the
               match result and the one that answers "are we beating BEN".
  par gap      imps(score_ns - par) at each table, from the N/S seat.  Par is
               what perfect bidding by BOTH sides reaches, so a table's gap is
               jointly owned; it says how far the auction landed from the best
               available spot, not who is to blame.
  contracts    what each table actually reached, for reading the losses.

Scoring is double-dummy throughout: the final contract is scored on the tricks
a perfect declarer takes against a perfect defence, so play never enters into
it and the whole difference is bidding.
"""

from __future__ import annotations

import argparse
import json
import random
import sys
import time
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from compare_ben import Ben  # noqa: E402

from bridgebidder.domain.auction import Auction  # noqa: E402
from bridgebidder.domain.calls import Call  # noqa: E402
from bridgebidder.domain.cards import FULL_DECK, Hand  # noqa: E402
from bridgebidder.domain.types import Seat, Vulnerability  # noqa: E402
from bridgebidder.engine.dd import EndplayDD  # noqa: E402
from bridgebidder.engine.decision import decide_fast  # noqa: E402
from bridgebidder.engine.scoring import imps, signed_score  # noqa: E402
from bridgebidder.inference.engine import prepare_decision  # noqa: E402
from bridgebidder.system.dsl import load_system  # noqa: E402

VULS = [Vulnerability.NONE, Vulnerability.NS, Vulnerability.EW, Vulnerability.BOTH]
MAX_CALLS = 60


def par_ns(deal: dict, vul: Vulnerability, dealer: Seat) -> int | None:
    from endplay.dds import calc_dd_table, par
    from endplay.types import Deal, Player, Vul

    pbn = "N:" + " ".join(str(deal[s]) for s in (Seat.N, Seat.E, Seat.S, Seat.W))
    vmap = {Vulnerability.NONE: Vul.none, Vulnerability.NS: Vul.ns,
            Vulnerability.EW: Vul.ew, Vulnerability.BOTH: Vul.both}
    pmap = {Seat.N: Player.north, Seat.E: Player.east,
            Seat.S: Player.south, Seat.W: Player.west}
    try:
        return int(par(calc_dd_table(Deal(pbn)), vmap[vul], pmap[dealer]).score)
    except Exception:
        return None


def play_table(system, ben: Ben, deal, dealer, vul, our_side: str) -> tuple[Auction, list]:
    """One auction with our engine in `our_side`'s seats and BEN in the others."""
    auction = Auction(dealer=dealer, vulnerability=vul)
    hands = {s.value: str(deal[s]) for s in Seat}
    ours: list = []
    while not auction.is_complete:
        seat = auction.next_seat
        if seat.side == our_side:
            setup = prepare_decision(system, auction, perspective=seat)
            choice = decide_fast(setup, deal[seat])
            call = choice if isinstance(choice, Call) else choice.call
            rule = None
            for c in setup.candidates:
                if c.call == call:
                    rule = c.rule.id if c.rule else "fallback"
                    break
            ours.append({"seat": seat.value, "call": str(call), "rule": rule,
                         "n": len(auction.calls)})
        else:
            resp = ben.ask({"hands": hands, "dealer": dealer.value,
                            "vuln_ns": int(vul.is_vulnerable(Seat.N)),
                            "vuln_ew": int(vul.is_vulnerable(Seat.E)),
                            "auction": [str(c) for c in auction.calls]})
            call = Call.parse(resp["bid"])
            if not auction.is_legal(call):          # BEN is statistical: it can
                call = Call.parse("P")              # offer an illegal call
        auction.add(call)
        if len(auction.calls) > MAX_CALLS:
            break
    return auction, ours


def run(n: int, seed: int, out: Path) -> None:
    system = load_system()
    ben = Ben()
    dd = EndplayDD()
    rng = random.Random(seed)
    rows = []
    t0 = time.time()

    for bi in range(n):
        deck = list(FULL_DECK)
        rng.shuffle(deck)
        deal = {s: Hand(deck[j * 13:(j + 1) * 13]) for j, s in enumerate(Seat)}
        dealer, vul = Seat.from_index(bi % 4), VULS[(bi // 4) % 4]

        a_auction, a_calls = play_table(system, ben, deal, dealer, vul, "NS")
        b_auction, b_calls = play_table(system, ben, deal, dealer, vul, "EW")

        def score_ns(auction: Auction) -> tuple[int, str]:
            c = auction.contract
            if c is None:
                return 0, "passed out"
            tricks = dd.tricks(deal, c.declarer, c.strain)
            return signed_score(c, tricks, vul, "NS"), f"{c} ({tricks} tricks)"

        sa, ca = score_ns(a_auction)
        sb, cb = score_ns(b_auction)
        p = par_ns(deal, vul, dealer)
        rows.append({
            "board": bi, "dealer": dealer.value, "vul": vul.value,
            "hands": {s.value: str(deal[s]) for s in Seat},
            "par_ns": p,
            "a_score_ns": sa, "a_contract": ca,
            "a_auction": " ".join(str(c) for c in a_auction.calls),
            "a_our_calls": a_calls,
            "b_score_ns": sb, "b_contract": cb,
            "b_auction": " ".join(str(c) for c in b_auction.calls),
            "b_our_calls": b_calls,
            "imp_margin": imps(sa - sb),                       # + = we win
            "a_par_gap": imps(sa - p) if p is not None else None,
            "b_par_gap": imps(sb - p) if p is not None else None,
        })
        if (bi + 1) % 100 == 0:
            m = sum(r["imp_margin"] for r in rows)
            print(f"  {bi + 1} boards, running margin {m:+d} IMPs "
                  f"({m / len(rows):+.2f}/board), {time.time() - t0:.0f}s", flush=True)

    ben.close()
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    report(out)


def report(path: Path, top: int = 0) -> None:
    rows = [json.loads(l) for l in open(path)]
    n = len(rows)
    margins = [r["imp_margin"] for r in rows]
    total = sum(margins)
    wins = sum(1 for m in margins if m > 0)
    losses = sum(1 for m in margins if m < 0)
    print(f"\n=== {n} boards, duplicate (each deal played both ways) ===")
    print(f"  match result: {total:+d} IMPs  ({total / n:+.3f} per board)")
    print(f"  boards won {wins}, lost {losses}, flat {n - wins - losses}")
    big = [m for m in margins if abs(m) >= 10]
    print(f"  swings >= 10 IMPs: {sum(1 for m in big if m > 0)} ours / "
          f"{sum(1 for m in big if m < 0)} theirs")

    ga = [r["a_par_gap"] for r in rows if r["a_par_gap"] is not None]
    gb = [r["b_par_gap"] for r in rows if r["b_par_gap"] is not None]
    print(f"\n  par gap, table A (we sit N/S): {sum(ga) / len(ga):+.2f} IMPs/board")
    print(f"  par gap, table B (BEN sits N/S): {sum(gb) / len(gb):+.2f} IMPs/board")
    print("  (positive means the N/S pair beat par, so a table's gap is the")
    print("   N/S pair's gain and the E/W pair's loss - it is jointly owned)")

    if top:
        worst = sorted(rows, key=lambda r: r["imp_margin"])[:top]
        print(f"\n=== our {top} worst boards ===")
        for r in worst:
            print(f"\n  board {r['board']}  {r['imp_margin']:+d} IMPs   par {r['par_ns']:+d} (N/S)")
            print(f"    N {r['hands']['N']}   E {r['hands']['E']}")
            print(f"    S {r['hands']['S']}   W {r['hands']['W']}")
            print(f"    we N/S : {r['a_auction']}")
            print(f"             -> {r['a_contract']}, {r['a_score_ns']:+d} N/S")
            print(f"    BEN N/S: {r['b_auction']}")
            print(f"             -> {r['b_contract']}, {r['b_score_ns']:+d} N/S")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run")
    r.add_argument("--n", type=int, default=100)
    r.add_argument("--seed", type=int, default=7)
    r.add_argument("--out", type=Path, required=True)
    p = sub.add_parser("report")
    p.add_argument("--rows", type=Path, required=True)
    p.add_argument("--top", type=int, default=0)
    a = ap.parse_args()
    if a.cmd == "run":
        run(a.n, a.seed, a.out)
    else:
        report(a.rows, a.top)
