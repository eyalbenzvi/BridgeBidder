#!/usr/bin/env python3
"""Batch-insert authored YAML into the system file, asserted at every step.

Round 18 adds rules by the hundred, so the edit itself has to be mechanical and
self-checking.  Two operations, both built on `yamledit.Edit` (never
`yaml.safe_dump`, which strips every comment):

  add_rules(context_id, block)   append rungs to an EXISTING context, after its
                                 last rule, at the file's rule indentation
  add_context(block)             append a WHOLE context at the end of the
                                 contexts list

Appending a context at the end is deliberate: `match_all_contexts` sorts by
pattern specificity and breaks ties by FILE ORDER, so a context added last can
never take a decision from an equally specific one that already exists.
Combined with `pattern: "... - ?"` - the least specific pattern in the file -
it gives the superset property structurally rather than by discipline.

Every batch is applied inside one transaction: if any assert fires nothing is
written, which is the failure mode `yamledit` alone does not cover (a
multi-edit script that aborts halfway discards its own earlier good edits).

    python3 tools/roundkit/addrules.py --spec batch01.yaml --report
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from yamledit import PATH, Edit                                   # noqa: E402


def _ctx_block(text: str, ctx_id: str) -> tuple[int, int]:
    m = re.search(rf"^  - id: {re.escape(ctx_id)}\n", text, re.M)
    assert m, f"context {ctx_id} not found"
    nxt = re.search(r"^  - id: ", text[m.end():], re.M)
    end = m.end() + (nxt.start() if nxt else len(text) - m.end())
    return m.start(), end


def add_rules(e: Edit, ctx_id: str, block: str) -> Edit:
    """Append `block` (already indented to six spaces) to a context's rules."""
    start, end = _ctx_block(e.text, ctx_id)
    body = e.text[start:end]
    assert "\n    rules:" in body, f"context {ctx_id} has no rules list"
    trimmed = body.rstrip("\n")
    if not block.endswith("\n"):
        block += "\n"
    e.text = e.text[:start] + trimmed + "\n" + block + e.text[end:].lstrip("\n")
    if not e.text.endswith("\n"):
        e.text += "\n"
    e.log.append(f"add_rules -> {ctx_id} (+{block.count('      - id:')} rules)")
    return e


def add_context(e: Edit, block: str) -> Edit:
    """Append a whole context (indented to two spaces) at the end of the file."""
    if not block.startswith("\n"):
        block = "\n" + block
    if not block.endswith("\n"):
        block += "\n"
    assert "\n  - id: " in block, "context block must contain a top-level id"
    e.text = e.text.rstrip("\n") + "\n" + block
    e.log.append(f"add_context (+{block.count(chr(10) + '  - id: ')} contexts, "
                 f"{block.count('      - id:')} rules)")
    return e


def counts() -> tuple[int, int]:
    out = subprocess.run(
        [sys.executable, "-c",
         "import sys; sys.path.insert(0, 'src');"
         "from bridgebidder.system.dsl import load_system;"
         "s = load_system();"
         "print(len(s.contexts), sum(len(c.rules) for c in s.contexts))"],
        capture_output=True, text=True, cwd=ROOT)
    assert out.returncode == 0, out.stderr
    a, b = out.stdout.split()
    return int(a), int(b)


def apply_spec(spec_path: str) -> None:
    """A spec file is plain text with markers:

        #== RULES <context_id>
        <six-space-indented rule block>
        #== CONTEXT
        <two-space-indented context block>
    """
    text = Path(spec_path).read_text()
    chunks = re.split(r"^#== ", text, flags=re.M)[1:]
    assert chunks, f"no #== sections in {spec_path}"
    before = counts()
    e = Edit()
    for ch in chunks:
        head, _, body = ch.partition("\n")
        head = head.strip()
        body = body.rstrip("\n")
        if not body.strip():
            continue
        if head.startswith("RULES "):
            add_rules(e, head[6:].strip(), body)
        elif head == "CONTEXT":
            add_context(e, body)
        else:
            raise SystemExit(f"unknown section {head!r}")
    e.save()
    after = counts()
    print(f"contexts {before[0]} -> {after[0]}, rules {before[1]} -> {after[1]}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True)
    a = ap.parse_args()
    apply_spec(a.spec)


if __name__ == "__main__":
    main()
