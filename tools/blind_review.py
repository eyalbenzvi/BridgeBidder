#!/usr/bin/env python3
"""Blind expert review of lost boards: the deal and OUR auction, nothing else.

The finding that motivates this tool (DECISIONS.md, "Reading a lost board as
an expert would"): asked the way a bridge expert is asked - four hands, the
auction, "which call would a panel reject and why" - a strong model names the
flawed call AND the agreement that should have covered it.  Shown rule ids,
fit scores or BEN's distribution instead, no method found the same flaw,
because it was a MISSING rule and there is no signal in the absence of a row.

So the prompt is deliberately starved.  Per lost board, per table where our
engine sat, it contains: dealer, vulnerability, the four hands, the auction
as it was bid, which pair is under review.  It does NOT contain the result,
the double-dummy tricks, par, the other table's auction, or anything from
BEN.  Losing to BEN only selects the board; it never enters the prompt.

    python tools/blind_review.py pack    --rows reports/after9001.jsonl --n 50 --dir reports/review9001
    python tools/blind_review.py run     --dir reports/review9001 --model opus --jobs 4
    python tools/blind_review.py collect --dir reports/review9001

`run` drives `claude -p` one prompt at a time (skipping prompts that already
have a verdict, so it is restartable).  If `claude` is unavailable, the
prompts in <dir>/prompts/ can be answered by any means; drop each answer in
<dir>/verdicts/<same name>.txt and `collect` will read it.

`collect` prints one line per reviewed table for a human to mark, and writes
<dir>/verdicts.jsonl.  Marking those lines IS the calibration set: it did not
have to exist beforehand, it is produced by reading the machine's verdicts.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

SEATS = ["N", "E", "S", "W"]
SUIT_SYMBOLS = {"S": "♠", "H": "♥", "D": "♦", "C": "♣"}

PROMPT = """Answer from bridge knowledge alone. Do NOT use any tools, do not read files, do not search. Just think and answer.

A bridge deal and the auction that took place. Both pairs play 2/1 Game Forcing with standard modern agreements (negative doubles, support doubles and redoubles, Jacoby 2NT, RKC 1430, Michaels, unusual 2NT). {vul_text} {dealer_text}

{hands}

Auction ({order_text}):
{auction}

The pair under review is {pair_text}. Question: is there a call by {pair_text} that an expert panel would consider clearly unreasonable - a call that breaks a standard agreement, misdescribes the hand, or misjudges the auction in a way any experienced player would see? Judge each call on the information available when it was made, not on the layout of the other hands. If yes: which call, what it should have been, and why, in a few sentences. If every call by {pair_text} is defensible, say so. Be concise (under 200 words).

End with exactly one line in this format and nothing after it:
VERDICT: <seat> <call made> -> <call that should have been> | <the agreement or reason, at most twelve words>
or, if nothing is wrong:
VERDICT: none
"""


def fmt_hand(h: str) -> str:
    s, hh, d, c = h.split(".")
    return "  ".join(f"{SUIT_SYMBOLS[k]}{v or '-'}" for k, v in zip("SHDC", (s, hh, d, c)))


def fmt_hands(hands: dict) -> str:
    return "\n".join(f"{name:6} {fmt_hand(hands[s])}" for s, name in
                     zip("NESW", ("North:", "East:", "South:", "West:")))


def fmt_auction(dealer: str, calls: list[str]) -> str:
    """Four columns W N E S, dashes for seats ahead of the dealer."""
    pretty = {"P": "Pass", "X": "Dbl", "XX": "Rdbl"}
    cols = ["W", "N", "E", "S"]
    row = ["-"] * cols.index(dealer)
    lines = [f"{'West':<8}{'North':<8}{'East':<8}{'South':<8}"]
    for c in calls:
        c = pretty.get(c, c)
        c = re.sub(r"([1-7])([SHDC])", lambda m: m.group(1) + SUIT_SYMBOLS[m.group(2)], c)
        row.append(c)
        if len(row) == 4:
            lines.append("".join(f"{x:<8}" for x in row))
            row = []
    if row:
        lines.append("".join(f"{x:<8}" for x in row))
    return "\n".join(lines)


def build_prompt(r: dict, table: str) -> str:
    auction = r["a_auction"] if table == "A" else r["b_auction"]
    our_side = "NS" if table == "A" else "EW"
    vul = {"None": "Nobody is vulnerable.", "NS": "North/South are vulnerable.",
           "EW": "East/West are vulnerable.", "Both": "Both sides are vulnerable."}[r["vul"]]
    dealer_name = {"N": "North", "E": "East", "S": "South", "W": "West"}[r["dealer"]]
    return PROMPT.format(
        vul_text=vul,
        dealer_text=f"Dealer {dealer_name}.",
        hands=fmt_hands(r["hands"]),
        order_text=f"{dealer_name} dealt and called first; read each row left to right",
        auction=fmt_auction(r["dealer"], auction.split()),
        pair_text="North/South" if our_side == "NS" else "East/West",
    )


def pack(rows_path: Path, n: int, out: Path, min_loss: int, worst: bool) -> None:
    rows = [json.loads(l) for l in open(rows_path)]
    lost = [r for r in rows if r["imp_margin"] <= -min_loss]
    if worst:
        lost.sort(key=lambda r: r["imp_margin"])
    lost = lost[:n]
    (out / "prompts").mkdir(parents=True, exist_ok=True)
    (out / "verdicts").mkdir(exist_ok=True)
    index = []
    for r in lost:
        for table in ("A", "B"):
            name = f"b{r['board']:05d}_{table}"
            (out / "prompts" / f"{name}.md").write_text(build_prompt(r, table))
            index.append({"name": name, "board": r["board"], "table": table,
                          "our_side": "NS" if table == "A" else "EW",
                          "imp_margin": r["imp_margin"],
                          "auction": r["a_auction"] if table == "A" else r["b_auction"],
                          "contract": r["a_contract"] if table == "A" else r["b_contract"],
                          "our_calls": r["a_our_calls"] if table == "A" else r["b_our_calls"],
                          "hands": r["hands"], "dealer": r["dealer"], "vul": r["vul"]})
    with open(out / "index.jsonl", "w") as f:
        for it in index:
            f.write(json.dumps(it) + "\n")
    print(f"{len(lost)} lost boards -> {len(index)} review prompts in {out / 'prompts'}")


def _ask(prompt_path: Path, verdict_path: Path, model: str) -> str:
    text = prompt_path.read_text()
    res = subprocess.run(["claude", "-p", "--model", model, text],
                         capture_output=True, text=True, timeout=600)
    if res.returncode != 0 or not res.stdout.strip():
        return f"FAILED {prompt_path.name}: {res.stderr.strip()[:200]}"
    verdict_path.write_text(res.stdout)
    return f"ok {prompt_path.name}"


def run(d: Path, model: str, jobs: int) -> None:
    todo = [(p, d / "verdicts" / (p.stem + ".txt")) for p in sorted((d / "prompts").glob("*.md"))]
    todo = [(p, v) for p, v in todo if not v.exists()]
    print(f"{len(todo)} prompts to answer with {model}, {jobs} at a time")
    with ThreadPoolExecutor(max_workers=jobs) as ex:
        for msg in ex.map(lambda pv: _ask(pv[0], pv[1], model), todo):
            print("  " + msg, flush=True)


VERDICT_RE = re.compile(r"VERDICT:\s*(.*)", re.IGNORECASE)


def parse_verdict(text: str) -> dict:
    m = None
    for m in VERDICT_RE.finditer(text):
        pass
    if not m:
        return {"verdict": "unparsed", "raw": text[-200:]}
    v = m.group(1).strip()
    if v.lower().startswith("none"):
        return {"verdict": "none"}
    mm = re.match(r"(\w+)\s+(\S+)\s*->\s*(\S+)\s*\|\s*(.*)", v)
    if not mm:
        return {"verdict": "flaw", "raw": v}
    seat, made, should, why = mm.groups()
    return {"verdict": "flaw", "seat": seat, "made": made, "should": should, "why": why.strip()}


def collect(d: Path) -> None:
    index = {json.loads(l)["name"]: json.loads(l) for l in open(d / "index.jsonl")}
    out = []
    for name, it in index.items():
        vp = d / "verdicts" / f"{name}.txt"
        if not vp.exists():
            continue
        text = vp.read_text()
        v = parse_verdict(text)
        out.append({**it, **v, "review_text": text})
    with open(d / "verdicts.jsonl", "w") as f:
        for r in out:
            f.write(json.dumps(r) + "\n")
    flaws = [r for r in out if r["verdict"] == "flaw"]
    print(f"{len(out)} tables reviewed | {len(flaws)} flagged | "
          f"{sum(1 for r in out if r['verdict'] == 'none')} clean | "
          f"{sum(1 for r in out if r['verdict'] == 'unparsed')} unparsed\n")
    print("Mark each line: agree / disagree / unsure.  (board, table, our side, margin)\n")
    for r in out:
        tag = f"b{r['board']:04d}{r['table']} {r['our_side']} {r['imp_margin']:+3d}"
        h = r["hands"]
        deal = f"N {h['N']}  E {h['E']}  S {h['S']}  W {h['W']}   (dealer {r['dealer']}, vul {r['vul']})"
        if r["verdict"] == "flaw" and "seat" in r:
            print(f"[ ] {tag}  {r['seat']} {r['made']} -> {r['should']}  | {r['why']}")
        elif r["verdict"] == "flaw":
            print(f"[ ] {tag}  {r.get('raw', '')[:90]}")
        else:
            print(f"[ ] {tag}  none")
        print(f"        {r['auction']}")
        print(f"        {deal}")


CALL_WORDS = {"pass": "P", "p": "P", "dbl": "X", "double": "X", "x": "X",
              "rdbl": "XX", "redouble": "XX", "xx": "XX"}
SYM2LET = {"♠": "S", "♥": "H", "♦": "D", "♣": "C", "N": "NT", "NT": "NT"}


def norm_call(text: str) -> str | None:
    """'2♥' / '2H' / 'Pass' / 'Dbl' / '3NT' -> engine call string."""
    t = text.strip().strip(",.;")
    if t.lower() in CALL_WORDS:
        return CALL_WORDS[t.lower()]
    m = re.match(r"^([1-7])\s*(♠|♥|♦|♣|NT|N|S|H|D|C)$", t, re.IGNORECASE)
    if not m:
        return None
    lvl, st = m.groups()
    st = SYM2LET.get(st, SYM2LET.get(st.upper(), st.upper()))
    return f"{lvl}{st}"


def locate_decision(r: dict) -> int | None:
    """Index in the auction of the flagged call: the flagged seat's call that
    matches `made`, disambiguated by an '(over X)' note when present."""
    seat = r.get("seat", "")[:1].upper()
    made = norm_call(re.sub(r"\(.*?\)", "", r.get("made", "")).strip())
    over = re.search(r"\(over\s+(\S+)\)", r.get("made", ""))
    over_call = norm_call(over.group(1)) if over else None
    calls = r["auction"].split()
    order = SEATS[SEATS.index(r["dealer"]):] + SEATS[:SEATS.index(r["dealer"])]
    hits = [i for i, c in enumerate(calls)
            if order[i % 4] == seat and (made is None or c == made)]
    if over_call:
        hits = [i for i in hits if i > 0 and over_call in calls[max(0, i - 3):i]]
    return hits


def context(d: Path, limit: int) -> None:
    """For every flagged table: the engine's own view of the flagged decision -
    the candidates it scored, their fits, the rule that won - and whether the
    call the reviewer wanted even existed as a candidate.  This is the bridge
    from a verdict in bridge language to the row in the YAML."""
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
    from bridgebidder.domain.auction import Auction
    from bridgebidder.domain.calls import Call
    from bridgebidder.domain.cards import Hand
    from bridgebidder.domain.types import Seat, Vulnerability
    from bridgebidder.engine.decision import score_candidates
    from bridgebidder.inference.engine import prepare_decision
    from bridgebidder.system.dsl import load_system
    system = load_system()
    vmap = {v.value: v for v in Vulnerability}
    rows = [json.loads(l) for l in open(d / "verdicts.jsonl")]
    flaws = [r for r in rows if r["verdict"] == "flaw" and "seat" in r][:limit]
    for r in flaws:
        hits = locate_decision(r)
        tag = f"b{r['board']:04d}{r['table']}"
        print(f"\n=== {tag}  {r['seat']} {r['made']} -> {r['should']} | {r['why']}")
        if not hits:
            print(f"    could not locate the call in: {r['auction']}")
            continue
        calls = r["auction"].split()
        if len(hits) > 1:
            print(f"    ({len(hits)} matching calls by this seat; showing each)")
        for i in hits[:3]:
          _show_decision(system, vmap, r, calls, i, norm_call(re.sub(r"\(.*?\)", "", r["should"]).strip()))


def _show_decision(system, vmap, r, calls, i, want):
        from bridgebidder.domain.auction import Auction
        from bridgebidder.domain.calls import Call
        from bridgebidder.domain.cards import Hand
        from bridgebidder.domain.types import Seat
        from bridgebidder.engine.decision import score_candidates
        from bridgebidder.inference.engine import prepare_decision
        au = Auction(dealer=Seat(r["dealer"]), vulnerability=vmap[r["vul"]])
        for c in calls[:i]:
            au.add(Call.parse(c))
        seat = au.next_seat
        hand = Hand.parse(r["hands"][seat.value])
        setup = prepare_decision(system, au, perspective=seat)
        ranked = score_candidates(setup, hand)
        print(f"    {seat.value} holds {hand} ({hand.hcp} HCP)   after: {' '.join(calls[:i]) or '(open)'}")
        for sc in ranked[:6]:
            rule = sc.candidate.rule.id if sc.candidate.rule else "fallback"
            mark = "<- made" if str(sc.call) == calls[i] else ("<- wanted" if str(sc.call) == want else "")
            print(f"      {str(sc.call):4} fit={sc.fit:.2f} prio={sc.candidate.priority:<4} {rule:32} {mark}")
        if want and not any(str(sc.call) == want for sc in ranked):
            print(f"      {want:4} NOT A CANDIDATE - no rule offers this call here")
        ctxs = sorted({sc.candidate.rule.context_id for sc in ranked if sc.candidate.rule})
        print(f"    contexts: {', '.join(ctxs[:6])}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    x = sub.add_parser("context")
    x.add_argument("--dir", type=Path, required=True)
    x.add_argument("--limit", type=int, default=1000)
    p = sub.add_parser("pack")
    p.add_argument("--rows", type=Path, required=True)
    p.add_argument("--n", type=int, default=50)
    p.add_argument("--dir", type=Path, required=True)
    p.add_argument("--min-loss", type=int, default=1)
    p.add_argument("--worst", action="store_true", help="largest losses first (default: corpus order)")
    r = sub.add_parser("run")
    r.add_argument("--dir", type=Path, required=True)
    r.add_argument("--model", default="opus")
    r.add_argument("--jobs", type=int, default=4)
    c = sub.add_parser("collect")
    c.add_argument("--dir", type=Path, required=True)
    a = ap.parse_args()
    if a.cmd == "context":
        context(a.dir, a.limit)
    elif a.cmd == "pack":
        pack(a.rows, a.n, a.dir, a.min_loss, a.worst)
    elif a.cmd == "run":
        run(a.dir, a.model, a.jobs)
    else:
        collect(a.dir)
