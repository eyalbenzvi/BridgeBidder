#!/usr/bin/env python3
"""Threshold calibration by coordinate descent, with a train/test split.

The system's point thresholds are just numbers in the YAML, chosen from
textbook knowledge and never tuned.  This tool searches them against a
training corpus and reports the change on a held-out corpus, so a value that
only helps the boards it was fitted on is discarded.

The double-dummy tables depend on the DEAL, not on the system, so they are
computed once and cached; each candidate setting then costs only self-play.

    python tools/tune.py cache --n 400 --seed 11 --out reports/train.pkl
    python tools/tune.py eval  --corpus reports/train.pkl
    python tools/tune.py search --train reports/train.pkl --test reports/test.pkl
"""

from __future__ import annotations

import argparse
import copy
import json
import pickle
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import yaml

from bridgebidder.domain.auction import Contract
from bridgebidder.domain.cards import FULL_DECK, Hand
from bridgebidder.domain.types import Seat, Vulnerability
from bridgebidder.engine.dd import get_dd
from bridgebidder.engine.scoring import contract_score, imps, signed_score
from bridgebidder.engine.selfplay import self_play
from bridgebidder.system.dsl import default_system_path, parse_system

VULS = [Vulnerability.NONE, Vulnerability.NS, Vulnerability.EW, Vulnerability.BOTH]
STRAINS = ("C", "D", "H", "S", "NT")


def build_corpus(n: int, seed: int, out: Path) -> None:
    """Deal n boards and precompute every double-dummy number they need."""
    from endplay.dds import calc_dd_table, par
    from endplay.types import Deal, Player, Vul

    rng = random.Random(seed)
    dd = get_dd()
    vmap = {Vulnerability.NONE: Vul.none, Vulnerability.NS: Vul.ns,
            Vulnerability.EW: Vul.ew, Vulnerability.BOTH: Vul.both}
    pmap = {Seat.N: Player.north, Seat.E: Player.east,
            Seat.S: Player.south, Seat.W: Player.west}
    boards = []
    for i in range(n):
        deck = list(FULL_DECK)
        rng.shuffle(deck)
        deal = {s: Hand(deck[j * 13:(j + 1) * 13]) for j, s in enumerate(Seat)}
        dealer = Seat.from_index(i % 4)
        vul = VULS[(i // 4) % 4]
        tricks = {(s.value, st): dd.tricks(deal, s, st) for s in Seat for st in STRAINS}
        pbn = "N:" + " ".join(str(deal[s]) for s in (Seat.N, Seat.E, Seat.S, Seat.W))
        par_ns = int(par(calc_dd_table(Deal(pbn)), vmap[vul], pmap[dealer]).score)
        boards.append({"hands": {s.value: str(deal[s]) for s in Seat},
                       "dealer": dealer.value, "vul": vul.value,
                       "tricks": tricks, "par_ns": par_ns})
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "wb") as f:
        pickle.dump(boards, f)
    print(f"cached {len(boards)} boards -> {out}")


def _best_for_side(tricks: dict, side: str, vul: Vulnerability, strain: str | None = None) -> int:
    best = -10000
    for d in [s for s in Seat if s.side == side]:
        for st in ((strain,) if strain else STRAINS):
            t = tricks[(d.value, st)]
            for lvl in range(1, 8):
                best = max(best, contract_score(Contract(level=lvl, strain=st, declarer=d, doubled=0), t, vul))
    return best


def evaluate(system, boards) -> dict:
    """Self-play every board and score it against the cached tables."""
    vmap = {v.value: v for v in VULS}
    gap = lvl = strain = 0.0
    n_con = 0
    par_loss = 0.0
    errors = 0
    for b in boards:
        deal = {Seat(k): Hand.parse(v) for k, v in b["hands"].items()}
        vul = vmap[b["vul"]]
        try:
            auction = self_play(system, deal, Seat(b["dealer"]), vul)
        except Exception:
            errors += 1
            continue
        c = auction.contract
        tricks = b["tricks"][(c.declarer.value, c.strain)] if c else 0
        par_loss += max(0, imps(b["par_ns"] - signed_score(c, tricks, vul, "NS"))) + \
                    max(0, imps(signed_score(c, tricks, vul, "NS") - b["par_ns"]))
        if c is not None and not auction.is_competitive:
            side = c.declarer.side
            actual = contract_score(c, tricks, vul)
            best_any = _best_for_side(b["tricks"], side, vul)
            best_same = _best_for_side(b["tricks"], side, vul, c.strain)
            gap += max(0, imps(best_any - actual))
            lvl += max(0, imps(best_same - actual))
            strain += max(0, imps(best_any - best_same))
            n_con += 1
    n = max(1, len(boards))
    return {"gap": gap / max(1, n_con), "level": lvl / max(1, n_con),
            "strain": strain / max(1, n_con), "par": par_loss / n,
            "errors": errors, "n_con": n_con}


def load_raw() -> dict:
    with open(default_system_path()) as f:
        return yaml.safe_load(f)


def apply_knob(data: dict, pattern: str, path: list, value) -> int:
    """Set one threshold (or priority) on every rule whose id matches.

    `path` is either ["priority"] or a walk into `requires`, ending in the
    index of the interval bound to change, e.g.
    ["evals", "rule_of_26", 0].
    """
    import re
    rx = re.compile(pattern)
    n = 0
    for ctx in data.get("contexts", []):
        for rule in ctx.get("rules", []) or []:
            if not rx.fullmatch(str(rule.get("id", ""))):
                continue
            if path == ["priority"]:
                rule["priority"] = value
                n += 1
                continue
            node = rule.get("requires")
            for key in path[:-1]:
                if not isinstance(node, dict) or key not in node:
                    node = None
                    break
                node = node[key]
            if isinstance(node, list) and isinstance(path[-1], int) and path[-1] < len(node):
                node[path[-1]] = value
                n += 1
    return n


# The knobs: thresholds that decide invite-vs-game, chosen because the
# level-gap analysis showed these rules dominate both the underbid and the
# overbid boards.  Each is (name, id-pattern, path, candidate values).
KNOBS = [
    ("game raise threshold",   r"(uc|cl|ch|ballow|balhigh)_raise_[CDHS]4", ["evals", "rule_of_26", 0], [23, 24, 25, 26, 27]),
    ("invite raise threshold", r"(uc|cl|ch|ballow|balhigh)_raise_[CDHS]3", ["evals", "rule_of_26", 0], [20, 21, 22, 23, 24]),
    ("3NT threshold",          r"(uc|cl|ch|ballow|balhigh)_nt3",           ["hcp", 0],                 [11, 12, 13, 14, 15]),
    ("2NT threshold",          r"(uc|cl|ch|ballow|balhigh)_nt2",           ["hcp", 0],                 [10, 11, 12]),
    ("pass eagerness (uncontested)", r"uc_pass",                           ["priority"],               [14, 16, 18, 20, 22]),
    ("pass eagerness (competitive)", r"(cl|ch)_pass",                      ["priority"],               [18, 20, 22, 24]),
    ("new suit at the 2-level", r"(uc|cl|ch|ballow|balhigh)_new_[CDHS]2",  ["evals", "total_points", 0], [8, 9, 10, 11, 12]),
    ("new suit at the 3-level", r"(uc|cl|ch|ballow|balhigh)_new_[CDHS]3",  ["evals", "total_points", 0], [12, 13, 14, 15, 16]),
    ("simple raise threshold", r"(uc|cl|ch|ballow|balhigh)_raise_[CDHS]2", ["evals", "total_points", 0], [5, 6, 7, 8]),
    ("1m - 3NT threshold",     r"r1m_3NT",                                 ["hcp", 0],                 [12, 13, 14, 15]),
]


def search(train, test) -> None:
    """Coordinate descent on TRAIN; every accepted move re-checked on TEST."""
    data = load_raw()
    base_tr = evaluate(build(data), train)
    base_te = evaluate(build(data), test)
    print(f"baseline  train gap {base_tr['gap']:.3f} par {base_tr['par']:.3f} | "
          f"test gap {base_te['gap']:.3f} par {base_te['par']:.3f}\n")
    chosen = {}
    cur_tr = base_tr
    for name, pattern, path, values in KNOBS:
        best_val, best_stats = None, cur_tr
        for v in values:
            trial = copy.deepcopy(data)
            if not apply_knob(trial, pattern, path, v):
                print(f"  ! {name}: pattern matched nothing"); break
            st = evaluate(build(trial), train)
            # primary objective is the attributable gap; par is a guardrail
            better = (st["gap"] < best_stats["gap"] - 1e-9
                      and st["par"] <= cur_tr["par"] + 0.10
                      and st["errors"] == 0)
            mark = "*" if better else " "
            print(f"  {mark} {name:28} = {v:<3} gap {st['gap']:.3f} par {st['par']:.3f}")
            if better:
                best_val, best_stats = v, st
        if best_val is not None:
            apply_knob(data, pattern, path, best_val)
            chosen[name] = best_val
            cur_tr = best_stats
            print(f"  -> keep {name} = {best_val} (train gap {cur_tr['gap']:.3f})\n")
        else:
            print(f"  -> keep {name} unchanged\n")
    final_tr = evaluate(build(data), train)
    final_te = evaluate(build(data), test)
    print("=" * 70)
    print(f"train gap {base_tr['gap']:.3f} -> {final_tr['gap']:.3f} | par {base_tr['par']:.3f} -> {final_tr['par']:.3f}")
    print(f"TEST  gap {base_te['gap']:.3f} -> {final_te['gap']:.3f} | par {base_te['par']:.3f} -> {final_te['par']:.3f}")
    print(f"chosen: {json.dumps(chosen)}")
    Path("reports/tuned.json").write_text(json.dumps(
        {"chosen": chosen, "train": [base_tr, final_tr], "test": [base_te, final_te]}, indent=1))


def build(data: dict):
    return parse_system(copy.deepcopy(data))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("cache"); c.add_argument("--n", type=int, default=400)
    c.add_argument("--seed", type=int, default=11); c.add_argument("--out", type=Path, required=True)
    e = sub.add_parser("eval"); e.add_argument("--corpus", type=Path, required=True)
    sr = sub.add_parser("search")
    sr.add_argument("--train", type=Path, required=True); sr.add_argument("--test", type=Path, required=True)
    args = ap.parse_args()
    if args.cmd == "search":
        search(pickle.load(open(args.train, "rb")), pickle.load(open(args.test, "rb")))
        sys.exit(0)
    if args.cmd == "cache":
        build_corpus(args.n, args.seed, args.out)
    else:
        boards = pickle.load(open(args.corpus, "rb"))
        print(evaluate(build(load_raw()), boards))
