"""Surgical, asserted edits to the system YAML.  Never yaml.safe_dump.

Every operation asserts that it applied and that the file still loads; an edit
that reports success and changes nothing is the bug this file exists to prevent.

    from yamledit import Edit
    e = Edit()                      # defaults to the repo's system file
    e.replace(old, new, count=1)    # exact substring, asserted unique
    e.after(anchor, block)          # insert block right after the anchor line(s)
    e.save()                        # writes, then reloads the system
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
PATH = str(ROOT / "src" / "bridgebidder" / "systems" / "two_over_one.yaml")


class Edit:
    def __init__(self, path=PATH):
        self.path = path
        self.text = open(path).read()
        self.orig = self.text
        self.log = []

    def replace(self, old, new, count=1):
        n = self.text.count(old)
        assert n == count, (
            f"expected {count} occurrence(s), found {n}:\n---\n{old[:400]}\n---")
        assert old != new, "replacement is a no-op"
        self.text = self.text.replace(old, new)
        self.log.append(f"replace x{n}: {old.strip().splitlines()[0][:70]}")
        return self

    def after(self, anchor, block):
        n = self.text.count(anchor)
        assert n == 1, f"anchor not unique ({n}):\n---\n{anchor[:400]}\n---"
        self.text = self.text.replace(anchor, anchor + block)
        self.log.append(f"insert after: {anchor.strip().splitlines()[-1][:70]}")
        return self

    def rule(self, rule_id):
        """Return the exact text block of one rule (id line through the line
        before the next `      - id:` at the same indent, or the next context)."""
        m = re.search(rf"^      - id: {re.escape(rule_id)}\n", self.text, re.M)
        assert m, f"rule {rule_id} not found"
        start = m.start()
        nxt = re.search(r"^      - id: |^  - id: |^# ={10,}", self.text[m.end():], re.M)
        end = m.end() + (nxt.start() if nxt else len(self.text) - m.end())
        return self.text[start:end]

    def context(self, ctx_id):
        m = re.search(rf"^  - id: {re.escape(ctx_id)}\n", self.text, re.M)
        assert m, f"context {ctx_id} not found"
        start = m.start()
        nxt = re.search(r"^  - id: ", self.text[m.end():], re.M)
        end = m.end() + (nxt.start() if nxt else len(self.text) - m.end())
        return self.text[start:end]

    def save(self, verify=True):
        assert self.text != self.orig, "nothing changed - refusing to save"
        open(self.path, "w").write(self.text)
        for line in self.log:
            print("  ok:", line)
        if verify:
            r = subprocess.run(
                [sys.executable, "-c",
                 "from bridgebidder.system.dsl import load_system;"
                 "s=load_system();print('loaded', len(s.contexts), 'contexts',"
                 "sum(len(c.rules) for c in s.contexts), 'rules')"],
                capture_output=True, text=True, cwd=str(ROOT))
            print(r.stdout.strip() or r.stderr.strip()[-2000:])
            assert r.returncode == 0, "SYSTEM FAILED TO LOAD after edit"
        return self
