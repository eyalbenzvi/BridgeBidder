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

### The batch, measured — **REVERTED**

Two contexts and sixteen rules for the above-game conversation, plus a 5NT
king ask in all four major-suit RKC continuations with the seat that answers
it (the file's first seven-level rules; slam machinery 119 → 145).  All checks
clean: 766 passed, lint unchanged at 223 findings, fuzz identical to baseline.

**Screened on the fresh 9,000-board pool: -41 IMPs over 69 changed boards
(16 up, 23 down, 30 same margin), t = -0.57, 95% bootstrap CI [-179, +101].
REVERT.**

Post-hoc attribution of those 69 boards, recorded as a **lead and not a
verdict** — it is the best of three slices, which is exactly the selection
premium this round exists to stop:

| slice | n | total | mean |
|---|---|---|---|
| king ask / grand slam | 18 | **+52** | +2.89 ± 1.98 |
| above-game cue | 9 | -25 | -2.78 ± 1.60 |
| trick-currency RKC (4NT) | 35 | -68 | -1.94 ± 1.53 |

The round's largest single board is **+26** on `2NT 3C 3H 4H 4NT 5C 5NT 7H` —
the file's first grand slam, and it made.

The engine's behaviour at the end of the round is byte-identical to `e97dd06`.
The tree is preserved in the history so a later round can resurrect rather
than re-derive it.

### Why this does not refute the density thesis — and where it was aimed wrong

Going from 119 slam rules to 145 is still a stub, and a stub measuring zero is
what the thesis predicts.  But the more important correction came from the
project owner mid-round, twice, and both times I had it wrong:

1. **The unit of work in a thin subject is a closed conversation, not a rung.**
   Measured: a cue bid above game costs -9.8 IMPs a seat *because no seat
   answers it*.
2. **Slam machinery does not live above game at all.**  It lives at the two,
   three and four level, in the constructive sequences that separate a
   minimum from a slam-going hand *before* game is reached.  My whole build
   was in the wrong territory, which is exactly why every move there measured
   negative: by 4S the information exchange has already failed, and passing is
   right precisely because the auction never described the hands.

A grep of the convention vocabulary confirms it, and this is the most useful
single output of the round:

| convention | rules |
|---|---|
| splinter | 18 |
| Jacoby 2NT | 20 |
| cue bid | 60 |
| jump shift | 18 |
| **trial / help-suit game try** | **0** |
| **serious / frivolous 3NT** | **0** |
| **mini-splinter** | **0** |
| **fit-showing jump** | **0** |
| **control-showing raise** | **0** |

3. **And the claim generalises beyond slam:** the file needs two to three
   times as many rules overall.  `docs/PLAN_SCALE_THE_SYSTEM.md` is the
   proposal that follows from it.

---

## The ablation: what rounds 11-16 actually bought — **REAL, +53 per 1000 boards**

Round 10 (`d775ad0`) against HEAD, on five seeds that were never a decision
rule for either version.  This is the only unbiased estimate in the project.

| seed | HEAD | round 10 | delta | boards changed |
|---|---|---|---|---|
| 313131 | -882 | -919 | **+37** | 23 |
| 323232 | -705 | -772 | **+67** | 28 |
| 343434 | -643 | -718 | **+75** | 23 |
| 353535 | -847 | -889 | **+42** | 24 |
| 363636 | -657 | -699 | **+42** | 39 |

**Pooled: +263 IMPs over 5,000 boards.  Seed-level mean +53 per 1,000 boards,
t = 6.86, 95% CI [+31, +74]; seed bootstrap [+40, +67].  All five seeds
positive.**

**This contradicts the consolidated review's central suspicion, and it should
be said loudly.**  The review argued that the ledger's +61 across rounds 11-16
was mostly a selection premium against an expectation of ~+85.  It was not.
The unbiased interval **contains the ledger's own +61**, so the rounds were
roughly as good as claimed.  What round 17 established is narrower and still
true: *individual* rounds are not separately resolvable (round 14's +51 is
t = 1.73), and the loop has stopped paying *now* — not that its past record
was fictitious.  The prior session's two partial seeds are reproduced exactly
(313131 = +37).

---

## Items 3, 4 and 5 — not completed

Honest statement of what was left undone when the session was stopped.

* **Item 3 (per-decision regret).**  `roundkit/cfr.py` is written, committed
  and unrun — rollouts with BEN in the opponents' seats, the fit floor and the
  never-take-the-max discipline inherited from `regret.py`, and an
  `is_closing` flag so round 16's failure mode can be split out.  Its
  acceptance test (reproduce the sign of round 14's fixes) is probably not
  satisfiable at 1,000 boards: those fixes touch 15 boards, far below the
  n ≈ 40 firings the reviewer's own variance estimate requires.
* **Item 4 (unconditional code fallback).**  Applied and its blast radius
  measured — **216 changed decisions per 1,000 boards with both halves**,
  against the reviewer's prototype of 61 for the generation half alone, so the
  interpretation half cascades hard through partner's model.  Reverted, not
  measured in IMPs.  **This is the one change in the round with enough blast
  radius (~1,300 changed boards in a 12k pool) to resolve a 1 IMP/board effect
  at full power** — it should be measured first in any successor session.
* **Item 5.**  Both bugs were diagnosed and their patches written but not
  applied: `partner_limited` reads `eval_ctx` where the parameter is named
  `ctx`, so the first YAML rule to use it raises `NameError`; and
  `_SETUP_CACHE` keys on `id(system)` while holding no reference, so a
  rebuilt system can inherit a dead one's identity (`tools/tune.py:211` does
  exactly that).  The fix is a `WeakKeyDictionary` of stable tokens.

---

## Held out, before and after

**-474 before, -474 after.**  Nothing shipped that changes a call, so the
number is not merely unchanged — the engine is byte-identical to `e97dd06`.

Do I believe it?  Yes, with a caveat that matters more than the number: -474
is a **running maximum of a ratcheted walk**, because that corpus has been the
decision rule sixteen times.  The ablation above is the first estimate in the
project that is not.

---

## Everything killed, with the number that killed it

| | number |
|---|---|
| the review's five-level cue ladder above game | **-9.8 IMPs a seat** (5C), -10.0 (5D) — no seat answers a cue above game |
| six of the major, direct | -6.8 IMPs a seat |
| a trick-currency keycard ask over partner's game raise | **-42 IMPs / 39 boards, t = -0.70** |
| the whole above-game slam conversation, 28 rules | **-41 IMPs / 69 boards, t = -0.57** |
| the 4NT gate `controls>=5 & ltc<=6 & trumps>=8` | signs invert between corpora: e10 +2.20, held -3.35 |
| loosening the king ask to six losers | broke two locked scenarios, one a real board recorded as making exactly twelve tricks |

---

## What I would do next, and what I now think is wrong with the plan

**What is wrong with the plan.**  Its item 2 aims at the wrong territory.  It
prescribes a five-level cue ladder above game; measurement says every move
there loses, and the reason is that the slam has already been missed by then.
Its items 3 and 5 are instruments and refinements for a loop that the ablation
shows is now flat.  Item 1 was right and is done.  Item 4 is right, cheap, and
is the only remaining item with the statistical power to prove itself.

**What I would do next, in order.**

1. **Measure item 4 properly.**  One hour with the screen, ~1,300 changed
   boards, enough power to resolve 1 IMP/board.  It also removes the trap that
   makes bulk authoring dangerous.
2. **Run `roundkit/coverage.py`** (written, never run): bucket every decision
   into *knows* (a rule fits ≥ 0.9), *guesses* (soft-miss lottery), *nothing*
   (code fallback), and rank contexts by backlog.  That converts "the file
   needs 2-3× the rules" into a ranked authoring list.
3. **Then stop editing rungs.**  `docs/PLAN_SCALE_THE_SYSTEM.md` sets out the
   alternative: 400-800 *agreements* templated into 7,000-12,000 rules, from a
   convention-card audit, BEN distillation, expert-corpus mining and
   per-case simulation, validated at *subject* granularity with the screen.

**The honest summary of this session.**  One asset shipped — a measurement
that is exact, cheap and states its own resolution — plus one clean positive
result (the ablation) and five clean negatives.  No behaviour change.  The two
findings that matter came from the project owner, not from me: that a thin
subject needs a closed conversation rather than a rung, and that the system is
under-specified across the board rather than mis-specified in places.  I spent
most of the session building in the wrong territory before that landed.
