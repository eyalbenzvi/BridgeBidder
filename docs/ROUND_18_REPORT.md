# Round 18: one rule per lost board, from three experts

**The engine ships at 2,903 rules in 666 contexts, up from 2,344 in 517.**
The build is accepted on the 12,000-board screening pool at **+305 IMPs over
447 changed boards, t = +2.67, 95% bootstrap CI [+79, +532]** — the first
change in this project's history to clear the acceptance bar round 17 set.

---

## 1. The bootstrap, and the numbers this round rests on

Reproduced exactly on a fresh container before anything was touched: 766
tests passed, 223 lint findings over 517 contexts / 2,344 rules, fuzz
`--n 300 --strict` exit 0 with 3 starved decisions.

| corpus | recorded reference | reproduced |
|---|---|---|
| seed 242424 | -677 | **-677** |
| seed 828282 (held out) | -474 | **-474** |

Both to the IMP, so nothing here rests on a discrepancy.

Fresh corpus, seed 575757: **-489 IMPs**, 217 boards won, **302 lost**
(-1,824 IMPs), 481 flat.

---

## 2. What the mechanism produced

`tools/roundkit/dossier.py` emitted one self-contained record per lost board —
deal, par, the full 20-entry double-dummy table, both auctions seat by seat
with `sweep.deciding_rule()` for every call of ours, BEN's counterfactual call
and confidence at each of our seats, and the whole candidate list at the first
divergence — in 8 parts of 38 boards.

Two experts from **different disciplines** then reviewed **all 302 boards
each**, as sixteen parallel agents, never in contact:

* **Expert A** — competitive / matchpoint duplicate;
* **Expert B** — constructive / team IMP.

Counted mechanically by `tools/roundkit/proposals.py`, not estimated:

| | |
|---|---|
| boards reviewed, twice each | **302** |
| proposals | **410** (A 235, B 175) |
| NOTHING-WRONG verdicts | 183 (A 65, B 118) |
| both disciplines proposed | 124 boards |
| A only / B only / neither | 111 / 51 / **16** |
| distinct proposed rule ids | **975** |
| distinct new contexts | **127** |

**33,051 lines of review over 604 board-reviews.** Only 16 of 302 boards drew
silence from both reviewers.

---

## 3. Per-subject results — the table that matters

| batch | subject | rules | changed boards | delta | per 1000 | t | 95% bootstrap CI | verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | generic competitive ladder | 204 | **3,497** | **-1,107** | -92.2 | **-3.18** | [-1804, -433] | **DROPPED** |
| 1a | the same, minus the doubles | 191 | 2,810 | -122 | -10.2 | -0.42 | [-701, +448] | **DROPPED** |
| 2 | support doubles + their answering seats | 257 | 216 | **+200** | +16.7 | **+2.55** | [+44, +355] | **SHIPPED** |
| 3 | the starved answering seats | 302 | 231 | +105 | +8.8 | +1.26 | [-59, +270] | **KEPT (see below)** |
| — | **the whole build (2 + 3)** | **559** | **447** | **+305** | **+25.4** | **+2.67** | **[+79, +532]** | **SHIPPED** |

Every number is a paired delta on the same 12,000 cached boards, computed by
`roundkit/screen.py`, which reuses the recorded score wherever the auction is
unchanged and is therefore the exact full-corpus paired delta, not an estimate.

### Where I overrode the instrument, stated plainly

Batch 3's own interval covers zero, so `screen.py` says REVERT. **I kept it**,
under this round's own decision rule: *a batch that measures neutral and is
structurally sound should be KEPT, because the thesis is that density pays only
in aggregate.* Both structural tests pass — every force it introduces ships
with the seat that answers it, and **lint went down, 223 → 219**, because
authoring starved seats closes `floor` findings. The build ships on the
aggregate, whose interval excludes zero.

---

## 4. The round's central negative, and it is the important result

**Batch 1 was the best-supported subject in the round before it was measured.**
Three independent instruments picked it:

* `coverage.py` — `general_competitive_low` (783 vacuous decisions) and
  `_high` (592) hold **1,375 of the 1,745** backlog decisions, five times
  anything else;
* `cfr.py` — `ch_pass`, the catch-all of `general_competitive_high`, is beaten
  by acting at **+1.90 ± 0.66 over n = 67, t = 2.9**;
* the two reviewers named those four contexts **472 times**.

Adding 204 reviewed rungs to it measured **-1,107 IMPs, t = -3.18, CI
excluding zero**, on 3,497 changed boards — five times the power of anything
this project had previously measured.

The post-hoc attribution said the **doubles** were the loss (`P → X` on 556
boards, -261 IMPs) and the **major-suit raises** a gain (`P → 3H` +1.09/board
over 91, `P → 3D` +0.86 over 96). That reading was the best of several slices,
so it was **screened rather than believed** — and it did not survive: the same
batch with all 19 double rungs removed took the build from **+305 to -122**.
The attribution was a selection artifact, and screening it cost twenty minutes
and prevented a false conclusion.

**Three readings survive, and they are not the same claim:**

1. **Volume is not the active ingredient.** 204 rules in the emptiest subject
   lost; 257 rules in one well-defined convention won. The difference is not
   count — batch 1 was the *bigger* batch.
2. **A generic context is the wrong place to add rules.** These four contexts
   are dispatched on the *shape of the auction*, not on a partnership
   agreement, so a rung added there fires in auctions its author never saw.
   The catch-all pass really is bad on average; the specific replacements are
   worse.
3. **"An alternative beats this call" does not license a RULE.** `cfr.py`
   substitutes one call while partner reads it with the *unmodified* system, so
   it measures unilateral deviation. Authoring the rung changes what partner
   hears. The hazard was documented before the batch was built; this is what
   it costs, and it is worth -1,107 IMPs.

---

## 5. Where the two experts disagreed, and how it was resolved

This is the most interesting output of the two-discipline design and it should
not be buried.

| disagreement | resolution |
|---|---|
| **Does anything answer a support double?** A said the generic seats already do; B traced `adx_pull_my_S` PULLING our own double at fit 1.000. | **B**, on the trace. `sd_double` runs +0.20/5 tables while the six `adx_pull_my_*` that answer it run **-3.00/15**. This became the round's only significant gain. |
| **The cue-raise ladder: aces or shape first?** | **Shape before aces**, honouring A's own reported negative, where RKC bid 6H off two cashing tricks. No 4NT rung was authored anywhere; the batch leans on the file's single audited `rkc_4NT`. |
| **The four-level minor Law raise gate**, which both experts wrote as `their_fit ≥ 8`. | **Neither.** The editor measured that `their_fit` returns **7** on the very boards they wrote it for — a 1m opening shows 3 and its raise 4 — so `[8, 26]` is unreachable, the documented `cl_raise_lott3_$M` species. Arrived at independently by A part 8 from the other side. |
| A's `expand_pairs` edit to extend `support_double` | Unimplementable (`addrules.py` appends rules, it cannot edit a context header). Shipped as tying contexts that lose the file-order tie-break instead — the superset property obtained structurally. |
| A's `advance_support_double`, B's minor advances | Subsumed / cut on A's own measured 5C-5D blast. |

**A NOTHING-WRONG from one and a proposal from the other was never treated as a
disagreement** — 111 boards were A-only and 51 B-only, which is the two lenses
working, not conflict.

---

## 6. Everything killed, with the number that killed it

| | number |
|---|---|
| **Item 4, generation half** (unconditional code fallback) | **-162 IMPs / 670 changed boards, t = -1.03**, CI [-476, +147] |
| **Item 4, interpretation half** | **29 tests fail**, including `test_support_double_negative_inference_in_samples` — the invariant the README leads with |
| **Batch 1**, the generic competitive ladder, 204 rungs | **-1,107 / 3,497 boards, t = -3.18**, CI [-1804, -433] |
| **Batch 1a**, the same without the doubles, 191 rungs | takes the build from **+305 to -122**, t = -0.42 |
| `rrev_min_2$M` (a reverse's answer below 8) | broke `reverse_responder_rebids_major_forcing`: it took the primary reading of 2M and turned a one-round force non-forcing. **Cut, not re-priced** — it contradicts an existing agreement rather than filling a hole |
| four `xd_pass_agreed_*` rungs setting `agreed_suit` on a PASS | 1 new `collide` finding: P read as agreeing four different suits |
| `xd_nt_extras` without a high-card floor | broke a round-3 arbitration lock: soft-missed `[18,40]` at fit 0.800 on a 16-count and bid 3NT with a doubleton in partner's suit, reporting a judgment call as CLEAR |
| `rorr_game_$M` at priority 50 | outranked the keycard ask at 46, so an eight-card fit with slam values bid game instead of asking |
| `r1d1h2c_4H` gated only on `total_points` | a seven-card suit is three length points, so an **eleven-count** bid game over the invitational rung |

---

## 7. The two instruments round 17 left unrun, now run

### `coverage.py` — and it corrected its own instrument first

On its original three-bucket scale the file looks covered: KNOWS 94.5%,
GUESSES 1.0%, NOTHING 4.5%. **That is an artefact.** A rule with an empty
`requires` fits **1.00 against every hand**, so every catch-all pass and
unconditioned sign-off — precisely the starved seats this round exists to find
— counted as an agreement. Splitting them out as **VACUOUS**, on live
decisions only:

| bucket | all decisions | live only |
|---|---|---|
| KNOWS | 55.5% | 76.0% |
| **VACUOUS** | **39.0%** | **22.5%** |
| GUESSES | 1.0% | 1.4% |
| NOTHING | 4.5% | 0.1% |
| **backlog** | **44.5%** | **24.0%** |

**About a quarter of our live decisions are made by a rule that describes no
hand.** It also confirms round 16 from the other side: **463 of the 464**
code-fallback decisions are closing passes.

### `cfr.py` — 3,465 rollouts

Mean IMP change from substituting an alternative: **-0.66 ± 0.10** — the right
sign for a system that mostly bids sensibly. Five rules are systematically
beaten, only one with a population: **`ch_pass` at +1.90 ± 0.66 over n = 67**.
The other half is reported too: `rkc_5D` (-8.50), `pref_2NT` (-7.67),
`ballow_reopen_X` (-6.00) lose five to eight IMPs a seat when deviated from.

**Both instruments pointed at the same subject, and batch 1 shows that
agreeing with each other is not the same as being right about the repair.**

---

## 8. Round 17's two unfixed bugs, fixed

* **`partner_limited` read `eval_ctx` in a function whose parameter is `ctx`** —
  reproduced as a `NameError` against a copy of the pre-fix tree before fixing
  it. Two reviewers had parked proposals on this bug.
* **`_SETUP_CACHE` keyed on `id(system)` holding no reference**, so a collected
  system's address could be reused. A `BiddingSystem` is an unfrozen dataclass
  and therefore unhashable, so a `WeakKeyDictionary` is unavailable; the fix
  holds a weakref beside `id()` and checks it on every lookup. **A reviewer hit
  this bug live** while prototyping against a patched copy, which is how it got
  an end-to-end regression test.

Both verified behaviour-neutral: `replay.py` over the whole 575757 match
replays 10,335 decisions with **0 changes**.

---

## 9. The whole build, measured every way

| | before | after | delta |
|---|---|---|---|
| **pool, 12,000 boards** (acceptance) | — | — | **+305, t = +2.67, CI [+79, +532]** |
| seed 575757 (the corpus the rules were found on) | -489 | **-453** | +36 (43 changed) |
| seed 242424 | -677 | **-641** | +36 (43 changed) |
| seed 828282 (held out) | -474 | **-533** | **-59** (33 changed) |
| all three pooled | | | **+13 over 119 changed boards, t = +0.19, CI [-121, +145]** |

**The held-out corpus moved the wrong way and I am not hiding it.** Three
things about that number, in order of importance:

1. **It is one third the information of the pool.** 33 changed boards against
   447. Pooling all three 1,000-board corpora gives +13 with t = 0.19 and an
   interval from -121 to +145: **the three corpora together cannot resolve this
   change at all**, which is exactly the 17%-power problem round 17 built the
   screen to escape.
2. **It is consistent with the pool within noise.** The pool's estimate applied
   to those 119 changed boards predicts +81; observed +13, with an SE of 67 —
   about one standard error.
3. **828282 has been the decision rule sixteen times.** Round 17 established
   that -474 is a *running maximum of a ratcheted walk*, not an unbiased
   estimate. Accepting the build on it, or rejecting the build on it, is the
   selection premium this round's method exists to stop paying.

The acceptance instrument is the pool, whose seeds have never been a decision
rule, and it says **+305 with an interval excluding zero**.

---

## 10. Does "one rule per lost board" reach 7,000-12,000 rules?

**The mechanism produces rules at more than the required rate. That is not the
bottleneck.**

302 lost boards yielded 410 proposals and **975 distinct rule ids** in one
round — 1.36 proposals per board, and a *third* of the way to the target from a
single 1,000-board match. Three subject editors turned a slice of that into
765 concrete rules, of which **559 shipped**. Extrapolated, four or five rounds
of this shape would reach 7,000 rules.

**The bottleneck is not supply. It is that most of the supply is wrong**, and
the only thing that tells you which part is a 12,000-board screen:

* the round authored **765 rules**, screened them, and **shipped 559**;
* the batch with the most independent support was the one that lost, at
  t = -3.18;
* three of batch 3's rungs were caught by locked scenarios *after* an expert
  editor had reviewed them, all three the same error — a rung priced by
  reasoning only upward, which is now the most repeated mistake in this
  project's history.

At 7,000 rules that error rate is unmanageable by review. **The next constraint
is a tool, not an expert**: an automated check that no new rung outranks a
more descriptive call in its own context, and no new context reduces another's
coverage. Section 4 of `PLAN_SCALE_THE_SYSTEM.md` already names both; this
round is the evidence that they are prerequisites rather than refinements.

---

## 11. What I would do next, and what is wrong with this plan

**What is wrong with the plan, in one sentence:** its premise — that the file
is uniformly under-specified and that volume therefore pays in aggregate — is
**false as stated**, and this round measured the counter-example at t = -3.18.

The corrected version is narrower and better supported by the round's own
numbers: **specific, named conventions with their answering seats pay; rungs in
generic auction-shaped contexts do not.** Batch 2 is one convention and it
gained. Batch 1 is 204 rungs spread across four generic contexts and it lost
more than the whole round gained. Both were reviewed by the same experts to the
same standard.

**What I would do next, in order:**

1. **Author conventions, not rungs.** The reviewers named dozens with zero
   rules: trial bids, serious/frivolous 3NT, mini-splinters, fit-showing jumps,
   control-showing raises. Batch 3 shipped several answering seats; the asks
   themselves are still absent. Each is a closed conversation, each is
   independently screenable, and the one such batch this round shipped is the
   only significant gain in the project's history.
2. **Build the two structural tools before the next bulk round** — the
   priority-conflict check and the shadowing invariant. This round found three
   priority errors by breaking locked scenarios, i.e. by luck of coverage.
3. **Stop treating the four generic competitive contexts as an authoring
   target.** They are 1,375 vacuous decisions and they resisted 204 rules. The
   right question is whether they should be *dispatched* differently —
   `general_uncontested_continuation` is already known to be keyed on RHO's
   last call rather than on whether the auction is contested — not whether
   they need more rungs.
4. **Re-measure batch 3 alone** on a larger pool. It is +8.8 per 1,000 with an
   interval from -59 to +270; 20,000 boards would resolve it.

**What I got wrong in executing this round.** I edited `inference/engine.py`
while sixteen read-only reviewers were running, and one of them lost its
harness and had to pin a git snapshot to recover. The guardrail about not
editing the tree during a screen extends to any long read-only job; I applied
it to screens and not to agents.
