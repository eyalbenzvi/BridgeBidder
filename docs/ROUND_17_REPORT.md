# Round 17: the measurement, and what it says about the slam project

*(in progress — numbers land as they are measured; the final section is written last)*

Baselines regenerated at `e97dd06` before anything else: review corpus (seed
242424) **-677**, held out (seed 828282) **-474**.  Both reproduce the recorded
numbers exactly, so nothing in this report rests on a discrepancy.

---

## Item 1 — a measurement that can see the effects we care about — **SHIPPED**

### What was built

* **`tools/ben_cache.py`** — BEN is a pure function of its request (hands,
  dealer, both vulnerabilities, auction prefix), so every answer is memoised
  forever in a content-addressed sqlite store, WAL-mode so several match
  processes share one cache.  A fully cached replay never loads the model at
  all.
* **`tools/compare_ben.py`** — `Ben` consults the cache and spawns its worker
  lazily.  Drop-in: `match_ben`, `ben_audit` and everything downstream benefit.
* **`tools/roundkit/screen.py`** — re-plays a cached pool under the current
  tree using the match's own `play_table`, reuses the recorded score wherever
  the auction comes back identical, and re-scores double-dummy only where it
  moved.  Reports **t**, a normal-theory 95% CI and a percentile bootstrap CI,
  prints its own resolution, and **refuses a verdict below k=8 changed boards**.

### Acceptance test

The plan asks that the screened result reproduce the full-corpus paired delta
exactly, tested on the round-14 fixes.  Round 14's YAML change reverts cleanly
onto HEAD, so that is the change measured, on the held-out corpus:

| | paired delta | boards changed | cost |
|---|---|---|---|
| full 1000-board match (`-474` → `-525`) | **-51** | 15 (4 up, 10 down, 1 flat) | 440 s |
| `roundkit/screen.py` | **-51** | 15 (4 up, 10 down, 1 flat) | 89 s |

Identical, not approximately identical — unchanged boards are bit-identical, so
the screened number **is** the full-corpus paired delta.  The full match also
lands on **-525**, the exact held-out number the ledger records for round 13,
which independently validates the whole reproduction.

### What the instrument immediately says about the ledger

Round 14's **+51** — the largest single gain since round 10, and the number
that set the standing bar of -474 — measures **t = 1.73, 95% CI [-5, +111]**.
It is not distinguishable from zero on the very corpus that accepted it.

### Honest correction to the plan's acceptance criterion

The plan asks for ">= 90% power at 1 IMP per changed board".  Power is
`k` -driven: the SE of the total is `sd_changed * sqrt(k)`, so 90% power at
1 IMP/board needs `k >= (2.9*sd)^2` changed boards — **254** at the project's
working `sd = 5.5`, and **417** at the **7.04** actually observed on the
round-14 change.  A 20k pool supplies about 300 changed boards for a
round-14-sized fix, so the honest claim is **70-88% power at 1 IMP/board**, not
93%.  `screen.py` now prints this line on every run rather than leaving it to
be assumed.

### Deviation: the pool is 12,000 boards, not 20,000

Measured throughput on this container is ~7 minutes per 1000-board match with
three matches sharing four cores.  A 20-seed pool plus the five round-10
ablation runs is about 4.5 hours of the session's critical path.  The pool was
cut to **12 seeds (12,000 boards)** — the five ablation seeds plus 401-407 — to
leave time to execute the rest of the plan.  Consequence, stated rather than
buried: for a fix touching 9 boards per 1000 the pool supplies ~108 changed
boards and resolves ~2.0 IMPs per changed board at 90% power.  The pool is
incremental (`screen.py` globs whatever exists), so it can be extended to 20k
later without redoing anything.

### The ratchet is retired

Discovery happens on corpora that may be looked at freely (242424, 828282).
Acceptance happens on the pool, whose seeds have never been a decision rule.
The rule is no longer "keep if positive": it is **keep only if the 95%
bootstrap CI excludes zero**, and no verdict at all below k=8.

---

*(items 2-5, the ablation, and the closing sections follow as they are measured)*
