#!/usr/bin/env python3
"""Index the reviewers' markdown into a machine-readable proposal list.

Sixteen reviewer files, 33,000 lines, 604 board-reviews.  The consolidation
step has to know what is IN there before anyone can edit it, and counting by
hand is how a round loses its own numbers.  This extracts, per board and per
reviewer: the verdict, every YAML block, every rule id proposed, every context
id touched, and the VERIFIED/UNTESTED label.

    python3 tools/roundkit/proposals.py --dir docs/expert_parts --json reports/proposals.json
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

BOARD_RE = re.compile(r"^## Board (\d+)", re.M)
FENCE_RE = re.compile(r"```(?:yaml)?\n(.*?)```", re.S)
RULE_ID_RE = re.compile(r"^\s*- id: ([A-Za-z0-9_$\[\],]+)\s*$", re.M)
CTX_ID_RE = re.compile(r"^  - id: ([A-Za-z0-9_$\[\],]+)\s*$", re.M)


def split_boards(text: str) -> dict[int, str]:
    out: dict[int, str] = {}
    marks = list(BOARD_RE.finditer(text))
    for i, m in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
        out[int(m.group(1))] = text[m.start():end]
    return out


def classify(body: str) -> str:
    head = body[:2500].upper()
    if "NOTHING-WRONG" in head or "NOTHING WRONG" in head:
        return "NOTHING-WRONG"
    if FENCE_RE.search(body):
        return "PROPOSAL"
    return "OTHER"


def analyse(body: str) -> dict:
    blocks = FENCE_RE.findall(body)
    yaml_text = "\n".join(blocks)
    rules = RULE_ID_RE.findall(yaml_text)
    ctxs = CTX_ID_RE.findall(yaml_text)
    up = body.upper()
    return {
        "verdict": classify(body),
        "n_blocks": len(blocks),
        "rules": rules,
        "new_contexts": ctxs,
        "verified": "VERIFIED" in up,
        "untested": "UNTESTED" in up,
        "negative": "NEGATIVE" in up or "WITHDRAWN" in up,
        "chars": len(body),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default="docs/expert_parts")
    ap.add_argument("--json", default="")
    a = ap.parse_args()

    data: dict[str, dict] = {}
    for p in sorted(Path(a.dir).glob("[AB]_part*.md")):
        who = p.name[0]
        for board, body in split_boards(p.read_text()).items():
            rec = analyse(body)
            rec["file"] = p.name
            data.setdefault(str(board), {})[who] = rec

    n_boards = len(data)
    per = Counter()
    both = a_only = b_only = neither = 0
    all_rules: Counter = Counter()
    all_ctx: Counter = Counter()
    verified = 0
    for board, sides in data.items():
        pa = sides.get("A", {}).get("verdict") == "PROPOSAL"
        pb = sides.get("B", {}).get("verdict") == "PROPOSAL"
        both += pa and pb
        a_only += pa and not pb
        b_only += pb and not pa
        neither += not pa and not pb
        for who, rec in sides.items():
            per[who + ":" + rec["verdict"]] += 1
            verified += bool(rec["verified"])
            for r in rec["rules"]:
                all_rules[r] += 1
            for c in rec["new_contexts"]:
                all_ctx[c] += 1

    print(f"boards reviewed        {n_boards}")
    print(f"both proposed          {both}")
    print(f"A only                 {a_only}")
    print(f"B only                 {b_only}")
    print(f"neither (both quiet)   {neither}")
    print()
    for k in sorted(per):
        print(f"  {k:26s} {per[k]}")
    print()
    print(f"distinct proposed rule ids     {len(all_rules)}")
    print(f"total rule-id mentions         {sum(all_rules.values())}")
    print(f"distinct new context ids       {len(all_ctx)}")
    print()
    print("most-proposed contexts (a cluster is an agreement several boards want):")
    for c, n in all_ctx.most_common(25):
        print(f"  {n:3d}  {c}")

    if a.json:
        Path(a.json).parent.mkdir(parents=True, exist_ok=True)
        Path(a.json).write_text(json.dumps(data, indent=1))
        print(f"\n-> {a.json}")


if __name__ == "__main__":
    main()
