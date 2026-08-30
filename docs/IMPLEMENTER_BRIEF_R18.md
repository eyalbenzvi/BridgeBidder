# Implementing a round-18 batch

One agent per SUBJECT BATCH from `docs/EXPERT_REVIEW_575757_FINAL.md`.  Batches
are applied one at a time, never concurrently — they all edit the same file.

## The rules of the job

1. **Never rewrite the YAML with `yaml.safe_dump`** — it strips every comment.
   Use `tools/roundkit/addrules.py` (whole batch in one transaction: if any
   assert fires, nothing is written) or `tools/roundkit/yamledit.py` for
   surgical replacements.
2. **Every edit must assert that it applied**, and you confirm by **TRACING
   the motivating board** through `repro.rank()` — not by trusting the "ok"
   lines.  An edit that reports success and changes nothing has cost this
   project a whole round.
3. Write a `#== CONTEXT` / `#== RULES <context_id>` spec file, apply it, then:
   * `python3 -c "from bridgebidder.system.dsl import load_system; s=load_system(); print(len(s.contexts), sum(len(c.rules) for c in s.contexts))"`
   * trace at least one motivating board per agreement:
     `repro.rank(hand, dealer, vul, seat, calls)` and `sweep.deciding_rule()`
   * `python3 -m pytest -q` — **768 passed** is the bar
   * `python3 tools/lint_system.py` — compare the FINDING COUNT against the
     baseline of **223**, not against zero
   * `python3 tools/fuzz_decisions.py --n 300 --strict` — exit 0
4. **A broken locked scenario is a MEASUREMENT, not an obstacle.**  Read the
   scenario and its comment before touching it.  In round 17 two locks
   correctly priced a gate that had been set wrong, and one was a real board
   recorded as making exactly twelve tricks.  Only overwrite a lock with a
   number that beats it, and say so in your report.
5. **Adding a rung deletes the code fallback for that call** in every seat its
   `when` reaches, because `covered` is built without consulting fit.  So no
   rule is "safely additive" — that is why every batch is screened.
6. Template vars must END a rule id (`id: foo_$M`); `call: $L$X` does not
   expand.
7. If a rule in your batch cannot be made to work — it will not parse, its
   `when` can never fire, it breaks a lock you cannot honestly overwrite —
   **drop that rule, finish the rest of the batch, and report exactly what you
   dropped and why.**  Do not silently reshape the agreement.

## What to report back

* rules and contexts before -> after (from the loader, not from your spec);
* the trace for each agreement: board, seat, auction, the call before and
  after, and the deciding rule id;
* pytest / lint / fuzz results against the bars above;
* everything you dropped, with the reason;
* anything you noticed that the editor got wrong.
