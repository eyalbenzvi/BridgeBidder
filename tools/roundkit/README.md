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

- **`sweep.py`** — every board we lost, every decision BEN disagreed with,
  grouped into families, plus whole-corpus denominators. Two things it fixes
  that no other tool here gets right:
  **(a) the deciding rule.** `explanation.source_rule_id` — which `replay.py`,
  `repro.fires()` and the match rows' `rule` field all key on — is the PRIMARY
  READING, the highest-priority rule producing the same call. It is what the
  call *means*, not what chose it. `deciding_rule()` reconstructs
  `fast_decision` (keep everything fitting >= 0.9, take the highest priority
  among those; otherwise the top blended score) and was validated against the
  engine on 598 consecutive decisions with 0 mismatches.
  **(b) the right yardstick.** Par gap is jointly owned by the whole auction, so
  a context whose decisions land on big-swing boards shows a bad gap whatever
  its rules do. `--rank-rules` scores every rule against ITS OWN CONTEXT.
  Judging against the corpus mean indicts innocent rules: `opener_rebid_1m_1M`
  runs at -4.04 against a corpus -0.02, and its rungs at -4.16 are at their own
  baseline, not four points below the field.
  `--families` / `--boards` / `--board N` / `--family ID` / `--context ID` /
  `--denom RULE` / `--rank-rules`. Pass `--cache` and `--index-cache` — both
  scans replay every decision through the engine and are slow to rebuild.

- **`paired.py`** — `python3 tools/roundkit/paired.py <before.jsonl>
  <after.jsonl> [--list]` compares two runs on the SAME deals: totals, the
  paired delta, and only the boards whose auction actually changed.
