# Algorithms review: five ideas, ranked, and one measurement error

An outside review of the *machinery* — the decision rule, the credit-assignment
metric, the search path, and above all the measurement harness.  The bridge
content is not the subject.  Every number below was recomputed in this repo;
where I reproduce a number from `DECISIONS.md` I say so.

Scripts used were throwaway and live under `/tmp`.  The repo is otherwise
untouched.

---

## 0. What I measured before forming an opinion

All on `reports/e10_final.jsonl` (1000 boards, 10,358 of our decisions) and
`reports/held_final.jsonl` unless stated.

**(a) Noise, per board and per changed board.**

| | held-out (828282) | review (e10) |
|---|---|---|
| per-board IMP margin, sd | 5.26 | 5.00 |
| SE of the 1000-board total | **± 166** | ± 158 |
| boards flat (margin 0) | 466 | 454 |
| boards with an identical auction at both tables | 138 | 124 |

Absolute totals from different seeds are therefore not comparable: -474 and
-677 differ by 203 against an SE-of-difference of 229.  Only the paired
comparison means anything, and the project already does that.  The paired
noise is what matters:

| paired run | boards changed | net delta | sd per changed board | t |
|---|---|---|---|---|
| `held_before -> held_final` (round 14) | 15 | **+51** | 6.80 | **1.94** |
| `e10_before -> e10_final` (round 14) | 20 | +52 | 5.80 | 2.00 |
| `held_final -> held_arb` (round 16 arbitration) | 18 | **-13** | 4.92 | **-0.62** |
| `e10_final -> e10_arb` | 18 | +26 | 3.99 | 1.54 |
| `held_final -> held_r15a` | 1 | -2 | — | — |

Pooled over all 74 changed boards: **sd = 5.54 IMPs per changed board.**

**(b) How the decision rule actually behaves.**  I re-ran `score_candidates` /
`fast_decision` over all 10,358 e10 decisions and recorded, per decision, how
many candidates cleared the 0.9 fast-path threshold.

| candidates at fit >= 0.9 | n | share |
|---|---|---|
| 0 (the "soft-miss lottery") | 109 | 1.1% |
| 1 (the choice is forced) | 7,790 | 75.2% |
| 2 | 1,952 | |
| 3 | 437 | |
| 4+ | 70 | |
| **>= 2 — the static `priority` alone decides** | **2,459** | **23.7%** |

Stage-matched (baseline = mean par gap of live decisions at the same depth in
the auction), live decisions only:

| population | n | our gap | stage | delta | total gap-points |
|---|---|---|---|---|---|
| exactly one candidate fits | 6,771 | +0.32 | -0.24 | **+0.56** | +3,772 |
| **two or more fit — priority decides** | **2,413** | -1.59 | -0.27 | **-1.32** | **-3,187** |
| nothing fits — soft-miss lottery | 108 | -5.72 | -0.30 | -5.42 | -585 |

And the contest gets worse the closer it is, which is what you would expect if
the hand-authored numbers were carrying real decision weight:

| priority margin between the best and second-best *fitting* candidate | n | stage-adj gap | total |
|---|---|---|---|
| 0 (exact tie — the only case `is_clear=False` reports) | 33 | -3.61 | -119 |
| 1-2 | 129 | -3.21 | -414 |
| 2-3 | 88 | -1.69 | -148 |
| 3+ | 2,163 | -1.13 | -2,506 |

**This reframes the project's own map.**  Round 16 concluded that "the soft-miss
lottery (58 decisions at -5.90) is the one hypothesis that survived rounds 15
and 16."  On the whole corpus the soft-miss population is 108 live decisions
worth -585 gap-points; the population where a *static float that sees neither
the hand nor the auction* is the sole discriminator is **2,413 decisions worth
-3,187**, and its near-tie core alone (margin < 3, n = 250) is worth -682 —
larger than the whole soft-miss lottery.  `is_clear` reports 33 of those 250,
because it fires only on an exact float equality.  The project has been sizing
this population with a `1e-9` comparison.

The usual caveat applies and I state it in the project's own language: this is
partly selection.  A decision with two fitting candidates is a decision in a
richer auction.  But the stage control removes the depth confound, and the
monotone gradient in the priority margin is a dose-response curve, which
selection does not generally produce.

**(c) The "gates that do not gate" family is small.**  For every decision I
recomputed each atomic gate on the *winning* candidate and asked whether the
hand violated it yet still scored >= 0.9 — i.e. whether the leak actually let a
call through.

```
6,810 atomic gates evaluated on winning candidates
    32 violated-yet-still-chosen  (21 rule_of_26, 11 weakest_their_stopper)
     0 for suit_diff (758 uses), total_points (1044), lott_total_trumps (392),
       suit_quality (718), balanced/semi_balanced (331), quick_tricks* (178), ...
```

`tools/lint_system.py --only soft` reports 0 findings because it checks a
hand-maintained *name* whitelist (`DISCRETE_EVALS`) against membership in
`_EVAL_S2` — not whether the registered sigma makes the gate bite.  The
behavioural check above is 40 lines and gives the population size the standing
open items lack: **`weakest_their_stopper` is 11 decisions, not "27 generic
notrump rules"**, and `rule_of_26`'s softness is 21.  I therefore do *not*
propose the sharp-tolerance sweep as one of the five.  It is a real defect
worth at most 0.3% of decisions, and DECISIONS already records it measuring -9
held out.

**(d) Cost model — BEN is free, our own engine is the bottleneck.**

```
BEN (ONNX bidder, deterministic argmax):   0.63 ms/query   (1,600 q/s, measured)
our engine (prepare_decision + fast_decision): 6.6 ms/decision
full duplicate match:                      365 s / 1000 boards
```

Profiling the replay loop: `prepare_decision` is **96%** of it, and inside it
`match_all_contexts` / `_best_specificity` is **46%** — 4.0M `pattern_matches`
calls per 120 boards, because every context's pattern is re-matched against the
auction string on every decision.  Every experiment in this project is priced
in units of `prepare_decision`.

**(e) Two latent code defects found while reading.**

- `inference/engine.py:248` — the `partner_limited` condition reads a name
  `eval_ctx` that does not exist in that scope (the parameter is `ctx`).
  Verified: `_conditions_hold(Conditions.from_dict({"partner_limited": True}), ...)`
  raises `NameError`.  No YAML rule uses it, so it is a landmine, not a bug: the
  first rule that does will crash `make_setup`.
- `_SETUP_CACHE` is keyed on `id(system)` and holds no reference to the system
  object.  Any loop that builds and discards many `BiddingSystem`s —
  `tools/tune.py:211` does exactly this, `parse_system(copy.deepcopy(data))` per
  candidate — can in principle read a setup cached under a freed object's
  address.  I could not reproduce address reuse in a 6-iteration probe, so this
  is a soundness hazard rather than a demonstrated fault; but **any learning
  loop (ideas 4 and 5 below) must clear the cache between systems**, and the
  round where "a coordinate-descent search over every point threshold measured
  -0.025 +/- 0.062" ran through this code path.

---

## THE SINGLE MOST IMPORTANT MEASUREMENT ERROR

**The accept/reject test has roughly 17% power, no confidence interval is ever
computed, and the "held-out" corpus has been used as the decision rule sixteen
times — so it is a training set, and the round-to-round numbers are a running
maximum, not an estimate.**

The arithmetic, all from the table in §0(a).  A fix that changes *k* boards has

```
SE(paired delta) = 5.5 * sqrt(k) IMPs
```

because unchanged boards are bit-identical and contribute exactly zero (BEN is
a deterministic argmax over ONNX logits and `decide_fast` is deterministic, so
this is exact, not approximate).  Fixes in this project touch 2-20 boards.

| k (boards a fix changes) | SE | MDE at 80% power, alpha=.05 one-sided | that is, per changed board |
|---|---|---|---|
| 2 | 7.8 | 19 IMPs | 9.7 IMPs |
| 15 | 21.3 | **53 IMPs** | **3.5 IMPs** |
| 20 | 24.6 | 61 IMPs | 3.1 IMPs |

A genuinely good bidding fix is worth perhaps 0.5-1.5 IMPs per board it
touches.  At mu = 1 IMP per changed board and k = 15, **power is 17%.**

Three consequences, each visible in the record:

1. **Round 14's headline is t = 1.94.**  +51 on 15 changed boards.  That is a
   defensible finding *if it were the only test performed*.  It is the best of
   ~20 candidate fixes in the round, in the fourteenth round of selection on the
   same 1000 boards.  Unadjusted, it is not evidence.

2. **Round 16 reverted arbitration on t = -0.62.**  -13 on 18 changed boards
   with SE 20.9.  That measurement cannot distinguish -13 from +30.  The round
   wrote "it is noise on a small population rather than a lever with a fixable
   flaw" — the first half is right about the *measurement*, and is not evidence
   about the *lever*.  Its follow-up split (level-changed -28 held out / +28
   review) has SE ~17 on each half: two draws from the same distribution, read
   as an inversion.

3. **Keeping-if-positive on a null effect pays +17 IMPs a round.**  For X ~
   N(0, SE) with SE ~ 21, `E[X | X > 0] = 0.798 * SE = +17`.  Held-out went
   -535 (round 10) to -474 (round 16): **+61 over seven rounds**, of which
   roughly five shipped anything.  Pure selection on a noiseless-looking but
   noisy statistic predicts about **+85**.  The observed progress since round 10
   is *smaller than what shipping nothing but noise would have produced.*
   Rounds 1-5 (+416, +76, +156, +126) are far outside this and are unambiguously
   real; rounds 6-16 total +226 across ~220 changed boards, t ~ 2.8 in aggregate
   against a selection expectation of ~+136.  **At most one of the last eleven
   rounds is individually distinguishable from noise, and the aggregate is only
   marginally so.**

There is a second, compounding error in the same place: the held-out corpus is
*fixed* and is the accept/reject criterion.  Sixteen rounds of "keep if the
held-out number improves" is sixteen bits of information leaked into the
statistic.  -474 is a running maximum of a random walk with a one-sided
ratchet, so it is a biased estimate of the engine's true strength; the bias
grows with the number of rounds.

**The check that settles it, and it costs ~2 hours.**  The git history has
clean per-round commits (`d775ad0` = round 10, `70201a7` = HEAD).  Check both
out in worktrees, run each against BEN on **five fresh seeds x 1000 boards**,
and compare paired, board by board.  That is the only unbiased estimate of what
rounds 11-16 bought.  My prior, from the arithmetic above, is that it comes in
between +0 and +60 with an SE of about 40 — i.e. that the true answer is
"somewhere between nothing and half of what the ledger claims."  Idea 1 below
is the fix that makes this stop happening.

---

## The five ideas, ranked by expected value per unit effort

### 1. Replay-screened evaluation on a 20,000-board cached corpus, with an actual test statistic

**The idea.**  Play one very large baseline corpus against BEN *once* and cache
it.  Thereafter evaluate a candidate change in two stages:

1. **Screen (engine only, no BEN).**  Replay every one of our recorded decisions
   in its recorded auction prefix under the candidate system —
   `tools/roundkit/replay.py` already does this.  A board on which no decision
   changes is **bit-identical**, by induction on the auction prefix: our policy
   is deterministic and BEN is a deterministic argmax, so if every one of our
   calls reproduces then every one of BEN's does too.  (Round 16 already relies
   on this: "whole-corpus replay: 0 of 10,358 decisions" alongside
   "byte-for-byte unchanged".)  The screen is exact, not heuristic.
2. **Play only the changed boards** against BEN, at both tables, and compute the
   paired delta over exactly those boards.

Then report, always: **n changed, net delta, bootstrap 95% CI over changed
boards, and the sign test.**  Never a bare integer.  Pre-register the fix list
before the held-out run, and rotate the held-out seed every round so no corpus
is ever the accept criterion twice.

**Why it beats the current loop, with numbers.**  The estimator is unchanged —
it is the same paired delta — but *k* goes up by the corpus ratio.  At 20,000
boards a fix that touches 15 boards per 1,000 touches ~300:

| | current (1,000 boards) | proposed (20,000 boards) |
|---|---|---|
| boards a typical fix changes | 15 | ~300 |
| SE of the paired delta | 21.3 | 95 |
| MDE per changed board (80% power) | **3.5 IMPs** | **0.79 IMPs** |
| power at a true 1 IMP/changed board | **17%** | **93%** |
| BEN/DD cost per evaluation | 365 s (all 1,000 boards) | ~110 s (300 boards) |

Note the last row: the proposed design is **cheaper per experiment** as well as
4.5x more powerful, because you stop replaying the 98.5% of boards that cannot
move.  The costs are a one-time 2-hour baseline run (365 s/1,000 boards,
measured) and a ~23-minute screen per candidate — which itself falls to a few
minutes if `match_all_contexts` is fixed (§0(d): 46% of engine time is
re-matching every context's pattern string against the auction on every
decision; index contexts by call-prefix and this is a lookup).

**Concrete first step and cost.**  (i) `roundkit/bench.py`: `bench build --n
20000 --seed <fresh> --out reports/base20k/` (2 h wall clock, ~150 lines,
resumable, checkpoint every 1,000).  (ii) `bench eval --base reports/base20k
--system <path>`: screen, replay the changed boards, print `n / delta / CI /
sign test` (~120 lines).  (iii) One validation run: apply round 14's shipped
diff to the round-13 system and re-measure it at 20k.  That single number tells
you whether the project's best-documented win survives power.

**Risks.**  (a) Deal-generation seeds must never overlap the review corpora — a
seed registry file, 5 lines.  (b) The screen is exact only while both policies
are deterministic; if arbitration or any sampling is ever enabled by default it
becomes approximate and must fall back to a full replay (assert this in code).
(c) 20k boards is 20x the storage; the current `.jsonl` is 1 MB/1,000 boards, so
20 MB — a non-issue.  (d) The real risk is social: a properly powered harness
will retire findings the project believes in, including some already in
`DECISIONS.md`.  That is the point.

**Shape:** one round to build, permanent payoff.  **Everything else in this
list is worth less until this exists**, because none of it can be evaluated.

---

### 2. Per-decision counterfactual regret with BEN in the opponents' seats

**The idea.**  Replace par gap as the attribution metric with a direct
counterfactual, computed on the *actual* deal, with the *actual* opponent.  For
each of our decisions in a played board:

1. Ask BEN what it would call from that seat (0.63 ms).  If it agrees, skip.
2. Otherwise build two continuations from the same prefix — ours, and BEN's —
   finishing each with **our engine in our two seats and BEN in the opponents'
   two seats**, double-dummy-score the final contract, and record the signed IMP
   difference, tagged with the deciding rule, the context, and the auction stage.

Aggregate by rule / context / population with a standard error.  This is a
policy-improvement gradient, not a correlation: it answers "would a different
call at *this* seat have scored better on *this* deal against *this* opponent",
which is precisely what par gap cannot answer because a par gap is jointly owned
by the whole auction.

**Why it beats the current loop, with numbers.**  I prototyped it.  150 boards,
1,608 BEN queries, 320 counterfactual rollouts, **29 seconds** — 91 ms per
rollout, so a *whole 1,000-board corpus costs ~3.5 minutes* and 20,000 boards
costs ~70 minutes.  Output:

```
mean IMP change from taking BEN's call instead of ours: -1.16  (sd 6.35, n=320)
BEN/us per-decision disagreement rate: 320/1608 = 19.9%

rule                    n    mean     se
uc_pass                11   +3.55   1.75      <- we pass, bidding was worth +3.5
open_pass              12   +3.00   1.65
fallback                5   +4.80   2.09
cl_raise_S2             4   +4.50   3.17
...
uc_raise_H4             4   -4.50   2.49      <- our call was right, BEN's wrong
adx_sit                 3   -5.00   5.73
v1NT_pass               3   -4.33   3.54
```

Compare what the project has today: par gap, of which round 16 wrote "A CLOSING
CALL INHERITS THE AUCTION'S PAR GAP AND EXPLAINS NOTHING" after 461 of 470
fallback decisions turned out to be closing passes.  A closing pass has a
counterfactual regret of *exactly zero* by construction here — the auction is
over, there is nothing to substitute — so the entire class of false finding that
cost round 16 cannot occur.  Likewise the "uniformly bad context" blind spot of
round 15: a context is now scored by the sum of the regrets of the decisions
inside it, not by the outcomes of the boards it happened to land on.

This also **repairs the arbitration path's stated flaw for free**.  Round 16
recorded: "`rollout` finishes the auction with `decide_fast` for ALL FOUR SEATS,
so the simulation models the opponents with our own engine while the match is
played against BEN."  With a 19.9% per-decision disagreement rate and 2-4
further opponent calls per rollout, the simulated opponent line is wrong on
**36-59%** of rollouts.  BEN costs 0.63 ms; there is no reason for a rollout in
this repo ever to use `decide_fast` in an opponent's seat again.

**Concrete first step and cost.**  `tools/roundkit/cfr.py` — ~200 lines;
`tools/regret.py` already has the aggregation and the "never take the max over
alternatives" discipline, and needs its rollout swapped from self-play to
BEN-in-the-opponent-seats.  Run it on both existing corpora (~7 min total) and
produce the rule-ranked and context-ranked tables.  My prototype is 90 lines and
already produces them.

**Risks and how it fails.**  (a) **Stale partner.**  In the counterfactual,
partner interprets the injected call with the *unmodified* system, so the
estimate is "the value of deviating unilaterally", not "the value of changing
the rule".  In a cooperative partnership game these differ, and the sign can
flip.  This is the reason the whole-corpus mean came out at -1.16 rather than
near 0.  **The machinery to bracket it already exists**: `analyze()` accepts an
`explanations` dict whose `constraints` key overrides the positive inference for
one call (`inference/engine.py:_apply_call`).  Compute both the stale-partner
and the informed-partner counterfactual and report the interval; a finding that
is the same sign under both is safe to act on, and one that is not is a
partnership-agreement problem, not a rule problem.  (b) Double-dummy scoring
rewards a lie whose partner happens to be misled favourably — `regret.py`'s own
docstring already names this; keep its fit floor on the alternatives, and
average, never max.  (c) BEN's call is a *proposal*, not a label; the regret is
computed against the DD outcome, so BEN only chooses where to look.  (d) Per
occurrence sd is 6.35 IMPs, so a rule needs n ~ 40 firings to resolve a 2-IMP
effect — which is another argument for idea 1's 20k corpus (only 39 rules decide
>= 20 calls per 1,000 boards).

**Shape:** one round to build and produce its first ranked table; a multi-round
instrument thereafter.  It replaces the per-decision BEN audit as the way into a
round.

---

### 3. Make the code fallback unconditional, and widen the interpretation to match

**The idea.**  `make_setup` builds `covered` from every rule whose `when` holds
and whose call is legal — **fit is never consulted** — and `generate_fallbacks`
then skips every covered call.  So adding a rung deletes the generic fallback
for that call *for every hand*, including hands the rung fits at 0.00.  This is
the mechanism §4 of `EXPERT_CRITIQUE_161616.md` identified, and it is the reason
the project's central guardrail ("adding a rung is safe") had to be retracted.

The fix is two-sided:

- **Generation.**  Always emit the fallback candidate; drop the `covered`
  filter.  This is sound under the existing decision rule *without any other
  change*, because fallback priority is 10.0 and every authored rule is in
  [15, 96]: a fallback can therefore never outrank a rule that fits >= 0.9, and
  it wins only when nothing fits — which is exactly what a backstop is for.
- **Interpretation.**  `interpret_call` resolves a call to its rule whenever one
  exists, so a call *made* by an unconditional fallback would be *read* by
  partner as the rule the hand does not fit.  That is a systemic lie and it must
  be closed: when the fallback was live for a call, the call's positive
  constraint becomes `any_of(rule_meanings + fallback_meaning)`.  Partner's
  model widens for those calls — a real, measurable cost, and the second half of
  the experiment.

**Why it beats the current loop, with numbers.**  I prototyped the generation
half by monkey-patching `covered` to the empty set and replaying all 10,358 e10
decisions:

```
decisions replayed                                   10,358
decisions whose call changes                             61   (60 live)
live soft-miss decisions (nothing fits >= 0.9):  108  ->  21   (-81%)
decisions decided by a fallback:                 470  -> 559
mean par gap of the changed live decisions:          -5.93
```

Every one of the 60 changed decisions is a soft-miss decision — a call the
engine currently makes at fit 0.35-0.84 because nothing fits — being replaced by
a fit-1.00 call.  Examples from the trace:

```
board 68b n=7   3H  fit 0.349  ->  4C  fit 1.00     (gap -10)
board 203b n=4  X   fit 0.349  ->  2H  fit 1.00     (gap -10)
board 408b n=7  3S  fit 0.349  ->  3D  fit 1.00     (gap -17)
board 444b n=5  2NT fit 0.835  ->  3C  fit 1.00     (gap -13)
```

This is a direct, mechanical attack on the one population that survived rounds
15 and 16 — and it is a **code** fix, so unlike every YAML fix it cannot be
undone by the next rung anyone authors.  It also retires the guardrail: once the
fallback is unconditional, "a fix that adds a rung fills a hole" becomes true
again, which unblocks the residue items rounds 14 and 15 both named and both
failed to ship (`uc_doubler_own_$X4` etc.).

**Concrete first step and cost.**  (i) Delete the `covered_calls` test in
`fallback.py:add` and the two other `covered_calls` sites (3 lines), pass
`frozenset()` from `make_setup`.  (ii) Screen with `replay.py`; you should see
~61 changed decisions on 1,000 boards.  (iii) Measure with idea 1's harness.
(iv) Only then do the interpretation half (~30 lines in `interpret_call` plus a
flag on `Candidate`), and re-measure — the two halves must be measured
separately because they push in opposite directions.

**Risks.**  (a) The lie described above, if the interpretation half is skipped:
the engine bids 2H "naturally" while the system reads 2H as a cue.  On 60
decisions this is small but it is exactly the "never trade explainability for
score" line the project has held.  Ship both halves or neither.  (b) Widening
`interpret_call` weakens partner's negative inference on every call that has a
live fallback, everywhere, not just on these 60 — this is the "adds a gate
subtracts behaviour" hazard wearing yet another hat, and it must be screened.
(c) 60 changed decisions is roughly 40-50 changed boards, which at SE = 5.5*sqrt(45)
= 37 is still under-powered on 1,000 boards; measure it at 20k.

**Shape:** one round, with a clearly defined second half.

---

### 4. Learn the priorities as a pairwise ranking problem

**The idea.**  The 2,344 `priority` floats are hand-authored, take 85 distinct
values in [15, 96], and are the *sole* discriminator on 23.7% of decisions
(§0(b)).  They are also the single most tractable parameter set in the system:
they do not change what any call *means*, so re-ranking is semantically safe in
a way that editing a `requires` block never is.

The well-posed problem, sized on this corpus:

```
contested live decisions (>= 2 candidates at fit >= 0.9)       2,413
distinct ordered (winner, loser) rule pairs                    1,054
pairs occurring >= 5 times                                       144
distinct rules appearing in any contested candidate set          748
rules that decide >= 4 calls in 10,358 decisions                 301
rules that never decide anything                       1,157 of 2,344
```

So: **~150 identifiable parameters, ~2,400 labelled comparisons per 1,000
boards.**  Fit `p_r` by pairwise logistic ranking (or a structured perceptron on
the argmax) with an L2 pull toward the authored value, so a rule with no
evidence keeps the number a human wrote.  Constrain the search to permutations
*within a context* — that is the unit a bridge player can explain, and it
preserves the cross-context specificity ordering the matcher relies on.

**The training signal, in order of preference.**

1. **Counterfactual regret from idea 2**, aggregated per (decision, candidate).
   This is the correct signal: it is measured in the objective's own units.
2. **BEN's argmax / top-5 distribution** as a dense, near-free proxy: 10,358
   labels per corpus at 0.63 ms each (~7 s for a whole corpus).  Note the
   objective's geometry — perfect imitation of BEN scores *exactly zero* IMPs in
   duplicate, i.e. +474 from here, so BEN agreement is a legitimate and very
   strong surrogate for this specific objective even though it is a bad proxy
   for "good bridge".  Use it to *pre-train*, and the regret signal to fine-tune.
3. **Not** double-dummy par: it is jointly owned, which is what got the project
   here.

**Why it beats the current loop.**  A round currently ships fixes that change
1-20 calls per 2,000 tables (round 15: "one call on 2,000 independent tables").
A ranking fit over 144 well-populated pairs touches, by construction, hundreds
of decisions, and it optimises the exact quantity the fast path uses.  It also
converts the project's bottleneck from *human review throughput* — two expert
subagent reviews per round, of which 8-11 of 20 findings get killed — into
*compute*.

**Concrete first step and cost.**  (i) Dump the contested set:
`(decision_id, [(rule_id, call, fit)], chosen, ben_call, ben_probs)` — my probe
does this in 68 s over the corpus, ~80 lines.  (ii) Fit the pairwise logistic
model on BEN argmax alone, hold out 20% of decisions, report ranking accuracy
before and after.  ~150 lines, minutes of CPU.  (iii) Write the fitted numbers
back into the YAML with `tools/roundkit/yamledit.py`, screen, and measure at
20k.  Total maybe 2-3 days of work.

**Risks.**  (a) **Feedback loop.**  Re-ranking changes which auctions occur,
which changes the contested set, which changes the labels.  This is DAgger:
iterate — fit, replay, re-collect, re-fit — and stop when the changed-decision
count converges.  Do not fit once and ship.  (b) **Explainability.**  A learned
float is not a sentence of bridge.  Mitigate by (i) restricting to within-context
permutations, (ii) reporting only the *order* changes and having a human sign
off on each, (iii) an L2 prior that leaves un-evidenced rules alone.  The
project's line "never trade explainability for score" survives if the output is
a small list of "rule A should outrank rule B, here is the population and the
regret".  (c) `_SETUP_CACHE`'s `id(system)` key (§0(e)) — clear it between
systems or this whole idea silently measures the wrong engine.  (d) 1,157 rules
have zero gradient; do not let the optimiser pretend otherwise.

**Shape:** multi-round project.  But step (i)+(ii) is a one-round experiment
whose output — "here are the 20 priority inversions the data disagrees with,
ranked by population" — is useful even if nothing is shipped.

---

### 5. Replace "fit >= 0.9, then max static priority" with one calibrated objective

**The idea.**  The current rule is a lexicographic hack with a hard cliff.
Three specific pathologies, all measured above:

- **The cliff.**  A candidate at fit 0.899 is unreachable however good it is; a
  candidate at 0.901 wins on priority however marginal.  Below the cliff the
  rule changes character entirely (blended `fit * (0.7 + 0.3*p/100)`), which is
  why 25-28 decisions have `score_candidates` order and `fast_decision` order
  disagreeing — a trap the project has documented twice.
- **Above the cliff, fit is discarded.**  A candidate fitting 1.00 loses to one
  fitting 0.90 on a 0.5 difference in a hand-written float, on 2,413 live
  decisions worth -3,187 stage-adjusted gap-points.
- **Below the cliff there is no model at all.**  108 live decisions where the
  best fit is 0.35-0.84 and the least-bad misfit is taken.

Replace both with a single Bayesian score:

```
score(c) = log P(hand | c means what the system says it means)   [the fit, as a log-likelihood]
         + log P(c | auction)                                    [the priority, as a log-prior]
```

Concretely: `argmax_c [ log fit(c) + priority(c)/T ]`, one global temperature
`T`, no threshold anywhere.  This (i) removes the cliff, (ii) makes the two
terms commensurable so a 0.10 fit deficit and a 0.5 priority gap can be traded
off, (iii) degrades gracefully into the soft-miss region instead of switching
formulas, and (iv) gives the priorities a *meaning* — log-odds — which is what
makes idea 4 well-posed rather than a fit to an arbitrary scale.

**Why it beats the current loop, with numbers.**  There is exactly one free
parameter, `T`, and it can be calibrated so that the new rule reproduces the old
one on the 7,790 decisions where only one candidate fits (it does so trivially)
and differs only on the 2,413 contested plus 108 soft-miss decisions — a
**2,521-decision** blast radius that the harness in idea 1 can actually resolve.
Compare the population the current arbitration path addresses: 92 decisions,
0.9%, which round 16 measured at t = -0.62 and could never have resolved.

The immediately-shippable sub-experiment is smaller and even better posed:
**widen `is_clear` from an exact float tie to a priority band.**  Today
`is_clear=False` fires on `abs(dp) < 1e-9` and catches 33 decisions.  A band of
3.0 catches **250 decisions at a stage-adjusted -2.73 (total -682)** — a larger
and better-characterised population than the entire soft-miss lottery.  That
alone re-sizes the arbitration experiment by 7.5x, which is the difference
between t = -0.62 and a real test.

**Concrete first step and cost.**  (i) `FAST_FIT_THRESHOLD` and the blend live
in ~20 lines of `decision.py`; add an env-switchable `POLICY=map` branch (~40
lines).  (ii) Sweep `T` over the corpus offline, counting changed decisions per
`T` — no BEN needed, seconds per value.  (iii) Pick the `T` at the knee, screen,
and measure at 20k.  (iv) Separately, and independently measurable: widen
`CLEAR_MARGIN`'s sibling — the tie test in `fast_decision` — to a band, and
re-run the arbitration experiment on the resulting 250+108 population **with BEN
in the opponents' seats** (idea 2) and with a multiplicity-corrected stopping
rule.  Today `arbitrate` takes the argmax over up to 4 candidates and then
applies an unadjusted `t >= 1.5` test to the winner, which is selective
inference: the effective alpha is roughly 3x what it says.  (At 60 deals with a
per-deal IMP sd of ~6, SE = 0.77, so `t >= 1.5` requires a 1.16-IMP mean and the
`MIN_OVERTURN_IMP = 0.4` floor never binds.)

**Risks.**  (a) The 0.9 threshold is load-bearing in places that are not obvious
— `score_candidates`' `pass_forbidden` relaxation tests `fit >= 0.9` on
discriminating pass rules; `holes.py`, `sweep.deciding_rule()` and every cached
report reconstruct it.  Changing the policy invalidates the caches; keep the old
path as the default and gate the new one.  (b) A single global `T` may be wrong
per context; resist per-context temperatures until the global one is measured,
or you have re-created idea 4 with worse identifiability.  (c) Removing the
cliff makes *every* decision continuous in fit, so small `_EVAL_S2` changes now
move the policy — the sharp-tolerance items become live again (though §0(c) says
they are worth ~32 decisions).  (d) This is the only idea here that changes the
engine's behaviour on three-quarters of the corpus if `T` is mis-set; it must
not be shipped on a 1,000-board measurement.

**Shape:** multi-round project.  The `is_clear` widening inside it is a
one-round experiment worth doing first, because it re-sizes the arbitration
question that round 16 answered with an under-powered test.

---

## Ranking, by expected value per unit effort

| # | idea | effort | why here |
|---|---|---|---|
| **1** | **Replay-screened 20k-board harness with a real test statistic** | ~1 round + 2 h compute | 17% -> 93% power *and* 3x cheaper per experiment. Nothing else on this list can be evaluated without it, and the last eleven rounds' ledger cannot be trusted until it exists. |
| **2** | **Per-decision counterfactual regret, BEN in the opponents' seats** | ~1 round, 3.5 min/corpus (prototyped) | Replaces the metric that has produced false findings in rounds 15 and 16 with one that is per-decision and not jointly owned. Fixes the arbitration path's opponent model for free. |
| **3** | **Unconditional fallback + widened interpretation** | ~1 round, ~35 lines | 60 live decisions, soft-miss population -81%, and it retires the guardrail that has constrained every round since round 6. A code fix, so it stays fixed. |
| **4** | **Learn the priorities as a pairwise ranking problem** | multi-round; first table in ~2 days | ~150 identifiable parameters, ~2,400 labels/corpus, targets the 23.7% of decisions a static float decides alone. Converts the bottleneck from review throughput to compute. |
| **5** | **One calibrated objective instead of the 0.9 cliff** | multi-round | Largest blast radius (2,521 decisions) and the highest ceiling, but also the highest variance and it needs 1, 2 and 4 to be evaluable. Its `is_clear`-widening sub-experiment (33 -> 250 decisions) should be done early and cheaply. |

The dependency structure matters more than the ranking: **1 unblocks everything,
2 tells 4 and 5 what to optimise, 3 is independent and cheap.**  If only one
thing is done, do 1.  If two, do 1 and 3 — 3 is the only item here that ships a
behaviour change inside a single round.

---

## Appendix: things I checked and am *not* proposing

- **A sharp-tolerance sweep over `_EVAL_S2`.**  Behaviourally, only 32 of 6,810
  atomic gates on winning candidates were violated-yet-still-chosen (§0(c)).
  The standing open items on `weakest_their_stopper` (11 decisions) and
  `rule_of_26` (21) are correctly diagnosed and correctly sized as small.
  `suit_diff` (237 rules, 758 evaluations, `s2 = 4.48`, so a 1-card error scores
  0.80) *looks* like the biggest un-audited leak in the file and produced **zero**
  violated-yet-chosen decisions.
- **Threshold tuning.**  Already measured at -0.025 +/- 0.062 held out, and the
  power analysis says that experiment could not have found anything smaller than
  ~3 IMPs/changed board anyway.  Re-run it only after idea 1, and only with the
  `_SETUP_CACHE` hazard in §0(e) closed.
- **Online arbitration as currently shaped.**  Sampling deals at decision time
  and rolling out is the expensive way to buy information that the offline
  corpus already contains: idea 2 gets a counterfactual on the *true* deal
  against the *true* opponent for 91 ms, where `arbitrate` spends up to 8 s on
  60 *sampled* deals against a *simulated* opponent that is wrong 36-59% of the
  time.  Keep the code; use it, if at all, only after the offline version has
  told you which populations are worth arbitrating.
