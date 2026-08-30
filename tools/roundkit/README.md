# roundkit — the four helpers an improvement round needs

Import them from anywhere in the repo with
`sys.path.insert(0, "tools/roundkit")`, and run from the repo root.

- **`repro.py`** — reproduce and dissect one decision.
  `board(path, n)` / `show(b)` / `seat_of(b, table, i)` / `at(b, table, i)` /
  `rank_at(b, table, i)` / `ask(hand, dealer, vul, seat, calls)` / `rank(...)` /
  `context_at(...)`, plus `rule_summary(path, rule_id)` and
  `fires_summary(path, rule_id)` for whole-corpus rescoring **including the
  winners** — never accuse a rule without that denominator.
  **Index carefully**: `at(b,'a',i)` asks the seat that makes call `i` (0-based)
  of that table's auction; `seat_of` tells you who that is. Table A = we are
  N/S, table B = we are E/W. Getting this wrong has produced false
  "nothing changed" readings in four separate rounds.

- **`yamledit.py`** — surgical, asserted edits to the system YAML.
  Never `yaml.safe_dump`: it strips every comment. `Edit().replace(old, new,
  count)`, `.after(anchor, block)`, `.rule(id)`, `.context(id)`, `.save()`
  (which reloads the system and fails loudly if it no longer parses). Every
  operation asserts that it applied — an edit that reports success and changes
  nothing is the bug this file exists to prevent.

- **`replay.py`** — `python3 tools/roundkit/replay.py <match.jsonl>` replays
  every decision we made in a recorded match under the CURRENT system and prints
  the ones that change. This is the blast radius of an edit, measured in
  seconds, before spending a match on it.

- **`paired.py`** — `python3 tools/roundkit/paired.py <before.jsonl>
  <after.jsonl> [--list]` compares two runs on the SAME deals: totals, the
  paired delta, and only the boards whose auction actually changed.
