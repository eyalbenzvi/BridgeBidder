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

## Item 2 — the slam project — **redirected by its own measurement**

### What the plan asked for, and why it was wrong in its details

The plan (from the bridge review) prescribes a **five-level cue ladder** above
our own game as sub-part (a).  Before authoring it, `tools/roundkit/slamprobe.py`
priced it: at **all 475 seats** in the two corpora where we pass our own game in
an agreed major, substitute each plausible move, finish the auction with our
engine in our seats and **BEN in the opponents'**, and score double-dummy.

| substitution | e10 (255 seats) | held (220 seats) |
|---|---|---|
| 4NT | **-3.77 ± 0.42** | **-4.98 ± 0.50** |
| six of the major | -6.23 / -6.35 | -7.36 / -7.38 |
| 5H | -6.86 ± 0.38 | -7.51 ± 0.44 |
| 5D | -9.72 ± 0.39 | -10.31 ± 0.39 |
| 5C | -9.78 ± 0.35 | -10.38 ± 0.42 |

Every move loses, and **the review's own prescription is the worst of them.**

The mechanism is not that cueing is bad bridge.  It is that **nothing in the
file answers a cue above game**: partner has no matching context, the fallback
layer is `quiet` because our side holds the contract, so his only candidate is
a pass at fit 1.00 and **we play five clubs**.  The -9.8 is the measurement of
an empty seat.  4NT beats it by five IMPs a seat for exactly one reason — its
answering ladder (`rkc_response*`, `rkc_continue_after_5*`, `rkc_5C_answerer`)
is already authored.

That cost twenty-one seconds of compute and saved a multi-round project from
being built the wrong way round.

### The rung, measured alone — REVERTED as a standalone

Sub-part (a) was then built the only way the data supported: a keycard ask in
the trick currency (item 2(b) applied locally rather than to the 104
`rule_of_26` sites), `gr_rkc_tricks_$M` — 4NT with six controls, at most five
losers and a known eight-card fit opposite partner's game bid.  Its gate was
chosen by out-of-sample sign replication (e10 +3.33, held +2.44) rather than by
prescription, and its known-fit clause exists because the first draft broke
round 3's locked `r3_no_rkc_without_partnership_values`.

**Screened on the fresh 6,000-board pool: -42 IMPs over 39 changed boards,
t = -0.70, 95% bootstrap CI [-160, +75].  REVERT.**

### Why that is the important result, and what replaced it

A well-motivated rung, whose gate replicated out of sample and whose answering
ladder already existed, still measured indistinguishable from zero.  The reason
is density, and it is the round's main finding:

| rules that bid at… | count |
|---|---|
| the three level | 686 |
| **the five level** | **55** |
| the six level | 70 |
| **the seven level** | **0** |
| all slam-named contexts | **119 of 2,346 (5.1%)** |

**A rule-based system needs a few hundred rules in a subject before that
subject works at all, and this file has 119 in the whole of slam.**  A slam
auction is a chain of questions; a question is worth nothing until the answer,
the answer's continuation and the sign-off all exist.  So the unit of work in a
thin subject is a **closed conversation**, not a fix — and a rung-at-a-time
method cannot build slam machinery at any speed.

Item 2 was therefore rebuilt as one: two contexts, sixteen rules, covering the
whole above-game conversation for both majors —

```
standing 4M, nobody has cued  ->  cue the cheapest first-round control
partner cued above game       ->  cue back, sign off in 5M, or bid 6M
partner signed off in 5M      ->  pass, or bid 6M with a real maximum
```

with every sign-off carrying `requires: {}` so no seat is ever starved (round
6's `rkc5H_signoff` lesson), and `pattern: "... - ?"` — the least specific in
the file — so the contexts sort last and cannot take a call from a context that
already defines it.  The superset discipline obtained structurally rather than
by copying gates.

Traced: e10 board 192a, the review's headline board, now runs
`1S 3C 3D 4C 4S P 4NT P 5S P 6S` — the cold slam we previously passed for -11.
And with a cue forced in, partner answers 5C with **5S at fit 1.00** instead of
passing it out.

*(the batch's screened number follows)*

---

*(items 3-5, the ablation, and the closing sections follow as they are measured)*
