# The improvement round: method, guardrails, and the lessons that cost a cycle

This is the repeatable loop used to improve the engine against BEN.  It is
written so a session with no memory of previous rounds can run one correctly.
Read this file and `DECISIONS.md` before starting.

Rounds so far, measured on a fixed held-out corpus (seed 828282, 1000 boards):

| round | corpus seed | held-out after |
|---|---|---|
| pre-round baseline | - | -1474 |
| 1-3 (tips, first expert rounds) | 919191 / 303030 | -1058 -> -982 |
| 4 (triaged 1000) | 515151 | -826 |
| 5 | 515151 | -700 |
| 6 | 626262 | -639 |
| 7 | 747474 | -621 |
| 8 | 858585 | -612 |
| 9 | 969696 | -576 |
| 9b (agreed-suit follow-up) | - | -558 |
| 10 (per-decision BEN audit) | 171717 | -535 |
| 11 | 242424 | -535 (two fixes reverted) |
| 12 | 242424 (re-review) | -532 (categorization; one large fix reverted) |
| 13 | 131313 | -525 (board-by-board critique; 11 of 20 fixes killed by review) |
| 14 | 151515 | **-474** (8 of 20 killed by review; the biggest single gain was a broken locked test) |
| 15 | 161616 (1000 deals) | **-474** (no movement: 4 of 6 killed, 1 reverted; the rule-level defect supply is exhausted) |

**The number that matters is the HELD-OUT one.**  The review corpus is the one
place a fix is guaranteed to look good, because it is where the fix was found.

---

## The loop

1. **Fresh match.**  `python3 tools/match_ben.py run --n 1000 --seed <NEW> --out reports/<tag>_before.jsonl`
   Pick a seed never used before (used: 7, 828282, 919191, 303030, 515151,
   626262, 747474, 858585, 969696).  ~5 minutes.  Report with
   `python3 tools/match_ben.py report --rows reports/<tag>_before.jsonl`.
2. **Triage - use the PER-DECISION audit, not the cluster dossier.**
   `python3 tools/ben_audit.py run --rows reports/<tag>_before.jsonl --out reports/audit.jsonl`
   then `report --conf 0.80`.  For every call we made on every board we LOST it
   asks BEN what it would call from the same seat, the same cards, the same
   auction, and ranks by IMPs and by FIRST divergence.  Round 10 records why
   this replaced `triage_match.py`: last-rule clustering is correlational, it
   nominated the same innocent generic rules five rounds running, and its fixes
   returned 5x-20x less held out than in sample.  The per-decision audit's
   in-sample and held-out gains were the same size.  `triage_match.py` is still
   useful for a whole-family denominator; it is no longer the way in.
3. **Two independent expert reviews**, in parallel, as subagents.  Split the
   clusters between them and give the second a second-opinion pass on the
   largest two or three.  Disagreement between them is signal, not noise.  The
   prompt that has worked is reproduced at the bottom of this file.
4. **Merge and dedupe** the two fix lists.  Where they touch the same rule,
   resolve the interaction explicitly and test it (round 7: one reviewer wanted
   a new branch on `rkc5D_slam`, the other wanted a gate wrapping it - they were
   compatible, but only checking the actual board proved it).
5. **Implement in asserted, trace-verified sub-batches** (see below).
6. **Check**: `python3 -m pytest -q`, `python3 tools/lint_system.py`,
   `python3 tools/fuzz_decisions.py --n 300 --strict`.
7. **Measure twice**: the SAME 1000 boards paired against `<tag>_before`, and
   the held-out corpus (seed 828282) against the previous round's held-out run.
   The current bar is **-474** (round 14).
   Keep or revert on the held-out number.
8. Preserve both verdicts to `docs/EXPERT_REVIEW_<seed>_{A,B}.md`, add
   regression scenarios to `tests/data/harvested.yaml`, append a `DECISIONS.md`
   entry with the measured numbers, commit, push.

---

## Non-negotiable mechanics

- The bidding system is **DATA**: `src/bridgebidder/systems/two_over_one.yaml`
  (~11k lines, ~490 contexts, ~2100 rules).  Never rewrite it with
  `yaml.safe_dump` - it strips every comment.  Edit surgically.
- The loader rejects duplicate mapping keys, so a botched edit fails loudly.
  Check with `python3 -c "from bridgebidder.system.dsl import load_system; print(len(load_system().contexts))"`.
- **Every scripted edit must assert that it applied.**  An edit that reports
  success and changes nothing is invisible for a whole round - that has
  happened.  And when a multi-edit script aborts on an assert, it discards its
  own earlier good edits, so **re-verify by tracing the board**, not by trusting
  the "ok" lines.
- **Template vars must END a rule id**: `id: foo_$M`, never `id: foo_$M_bar`.
- `call: $L$X` does not expand.  Write the level out.
- Never trade explainability for score.  Every gate must be explicable in one
  sentence of bridge.

## The scoring model, in one paragraph

Candidates are scored by soft Gaussian fit against each rule's `requires`.
Anything fitting >= 0.9 wins by `priority`; below that, blended score decides -
so a rule that misses by one point can still win if nothing else fits, which
produces "soft-miss lottery" bids.  Some evaluators are registered with sharp
tolerance in `constraints/model.py` `_EVAL_S2`, where a one-point miss really
fails.  Every generic context ends in a catch-all pass with `requires: {}` that
fits 1.00, so **any hole in an authored ladder becomes a PASS by construction**:
`all-pass` and `fallback` in a dossier name STARVED SEATS, not bad rules.

## The lesson that cost a whole cycle

Fixes that ADD a rung can only fill a hole.  Fixes that **add a gate** to an
existing rule, or **add a more specific context**, SUBTRACT behaviour everywhere
they reach - and the corpus that motivated them is the one place they are
guaranteed to look good.

**AMENDED IN ROUND 15, and the amendment matters more than the rule.**  "Adding
a rung is safe" is FALSE as stated.  `prepare_decision` builds `covered` from
every rule whose `when` holds and whose call is legal - **fit is never
consulted** - and `generate_fallbacks` only generates candidates for calls NOT
covered.  So a new rung **deletes the code fallback for its call** in every seat
its `when` reaches, whether or not the hand fits it.  Traced on board 691a: a
fit-**1.00** fallback replaced by a rung fitting **0.00**, the seat taken by a
fit-**0.066** keycard ask.  A new rung is safe only where no fallback covered its
call, or where the rung fits every hand the fallback caught - and that must be
MEASURED, because `when` is auction-only and fit is hand-dependent, so no `when`
can restrict the suppression to the hands the rung wants.  The code fallback
decides **4.4% of all our calls**; every "additive" fix has been quietly editing
the largest population in the engine.

In round 6 three such fixes gained 223 IMPs on the review corpus and lost 66 on
the held-out corpus: a `semi_balanced` gate killed five cold 6NTs, a narrower
slam-try context deleted the keycard asks it shadowed, and a checkback ladder
was authored without the seat that answers it.  So:

- Proposing a gate?  State what it SUBTRACTS and why that is acceptable.
- A new context that shadows an existing one MUST carry the shadowed rule's
  gates verbatim as a rung, so it can only ever be a superset.  (Round 7's
  weak-two overcalls hit this exact trap again and were caught by a test: the
  new context took over interpreting `2S`, and its narrower gate dropped a
  17-count's 2S from fit 0.76 to 0.33, so the engine began reporting a genuine
  judgment call as "clear".)
- A new asking bid or ladder must ship WITH the context that answers it.
- A gate justified on two or three boards needs the held-out corpus before it
  is kept.  Consider measuring it as its own experiment.
- **Price a new rung against the rungs BELOW it, not only the one above.**  A
  rung placed too high subtracts every more descriptive call it outranks, which
  is the "adds a gate" hazard wearing a different hat.  Round 14's
  `uc_nt_raise3` was placed at 28.5 "under `uc_nt3`, so the natural reading
  stays primary" - by me and by the reviewer, both reasoning only upward - and
  it thereby outranked every natural three-level suit bid (`uc_new_*3` at 27,
  `uc_new_*3_hi` at 27.5).  A 5-5 major hand raised partner's 2NT to game
  instead of bidding three spades.  `pytest` caught it on a locked round-9
  scenario; re-ranking to 26.5 was worth **+26 held out on five boards, five up
  and none down**, the round's largest single gain.  List every rule in the
  context whose call your new rung can legally outrank, and say in one sentence
  of bridge why yours is the better description.
- **Run the full suite before you believe a number.**  A broken locked scenario
  is a measurement, and in round 14 it was the most valuable one in the round.

## Two other recurring species

- **Ceilings.**  Ladders that cap their top rung (usually at 17 or 18) and have
  nothing above, so a 19-count finds no rule that fits and the soft model hands
  it to whichever sign-off misses by the fewest points.  Found in rounds 6 and 7.
- **A gate added to one rule and not to its siblings.**  The `sibling` lint
  catches most of these now; it compares gate presence AND bands.  Round 7 still
  found two by hand (`rr1H1SC_2S` / `rr1H1SD_2S`, and the RKC trump-queen clause
  that existed only on the 5H reply).

## Measured-neutral or scope-excluded - do not re-propose

`DECISIONS.md` is authoritative; the short list: tightening `uc_nt3`'s strength
gate (measured +1 IMP over 1000 boards, and it has been ruled a symptom three
rounds running); opening-style / rule-of-20 thresholds; 3NT-versus-5m
preferences; Michaels / unusual notrump as convention additions; the 5NT king
ask; and both points-estimator repairs (`rule_of_26` units fix measured -20;
the singleton-honour double-count measured +1 and was kept on explainability
alone).  Round 7 also killed, with whole-corpus data, "a takeout double must not
hide a six-card suit" for the remaining sibling rules: doubles WITH a 6+ suit
average -2.00/table, WITHOUT -2.54.

## Known open items (diagnosed, not fixed)

- After ANY double, the entire game-force landing family is unreachable: those
  contexts use pattern `... - P - ?` and only `gf_2NT_natural` uses `... - ?`.
  Repairing it needs a parallel `... - X - ?` context that would shadow
  `general_their_double`, so it needs the superset discipline above.
- No opener's reopening/second double (`1C - (1D) - P - (2D)` with 18 HCP has
  only a pass and the code-fallback double).  Adding a third meaning to `X` in a
  context that already defines two is a `collide` risk; wants its own round.
- `2C - 2NT` positive-response continuations have no landing ladder, so the
  engine walks `3C-3D-4C-4D-4H` inventing a suit each turn.
- `qr3_4NT_quant` was measured in round 8 and REPAIRED, not deleted: its floor
  is `rule_of_26_sharp >= 31`.  No longer an open item.
- **`suit_length(their)` does not mean "their first suit".**  `_their_suits`
  seeds itself LHO-before-RHO, so the evaluator resolves to my LHO's suit, which
  is their OTHER suit as often as not - this file's comments and DECISIONS both
  say otherwise.  Round 4 fixed it for one rule by adding `standing_suit_length`;
  sweeping the three negative doubles onto that measured **-40 held out** in
  round 9 and was reverted.  The misnaming is real; the naive sweep is not the
  repair.
- **The four-level pull, the 2NT-Stayman-over-interference twin and a
  non-forcing responsive double** are each structurally right, each measured
  individually in round 9 at -22, -12 and -8 held out, and each reverted.  The
  pull needs a "partner's double was PENALTY" condition before it can be safe.
- **The weak jump overcall is outranked by the simple overcall** and fires
  eight times in 2000 tables.  Round 11 re-ranked it and measured **-24 held
  out**: the jump was already reachable below 8 HCP (where the simple overcall
  does not fit), and on the 8-10 overlap the one-level call is better.  A rule
  that rarely fires may simply describe a rare hand - check the population
  before calling it dead code.
- **`cl_raise_lott3_$M` carries `cheapest_in_suit: true`** and a preemptive
  raise to the level of the fit is a jump, so the rung is unreachable whenever
  the cheap raise is legal.  Round 11 freed it (+19 in sample, **-3 held out,
  twice**) and reverted: the gate is broken AND the rung does not pay.  Its
  content needs rethinking, not unblocking.
- **`weakest_their_stopper` has no sharp tolerance** (`constraints/model.py`,
  `_EVAL_S2`) while both its siblings carry 0.3, so the `[0.9, 9]` gate on 27
  generic notrump rules does not gate: no stopper at all scores 0.835.  Round 8
  measured the one-line repair at **-9 held-out** and reverted it - the wins are
  real but the seats behind the deleted notrumps are unauthored and pick worse
  suit contracts.  Author those seats first, then re-measure.
- **The keycard ask over a game raise is a measured loss** (16 asks, -35 IMPs;
  the sign-off branch 0 wins) but no gate on it survives: round 8 measured
  `keycards >= 3` at **-17 held-out**, where it deleted three cold slams.  The
  only honest separator is a `max_total_points` ceiling channel in the partner
  model, which does not exist.
- **After partner RAISES my own suit every generic raise rung is dead**: the
  sharp `lott_total_trumps >= 8` gate counts partner's SHOWN minimum, so a
  simple raise (3) plus my own bid suit (4) counts 7 and both the invitational
  and game rungs score ~0.08.  Named independently by both round-8 reviewers.
- **`general_uncontested_continuation` is dispatched on RHO's last call, not on
  whether the auction is contested.**  Its `pattern: "... - P - ?"` means "RHO
  passed"; a `uc_*` rule therefore decides a COMPETITIVE auction on 465 of 2000
  tables at mean **-1.14** (CI excludes the -0.804 corpus mean), against -0.67
  on the job it was written for.  The diagnosis is confirmed; the obvious repair
  is not.  Round 12 routed those positions to the competitive contexts
  (`also_patterns` + context-level `is_competitive`, both now in the DSL) and
  measured **-59 paired / -106 held out**, breaking five locked scenarios,
  because a context that DEFINES a call takes over interpreting it.  Port
  individual rungs under `when: { is_competitive: true }` instead - that is what
  `uc_raise_lott4_$M` does, at +12.
- **First-divergence ranking is blind to defects that only occur late in an
  auction.**  `uc_pass`, the catch-all of the population above, appears in the
  confident first-divergence list exactly once, at -1 IMP.  Use
  `ben_audit.py` to find the *entry* to a bad auction; use a whole-corpus scan,
  sliced on the new opponent vocabulary, to find defects that live downstream.
- **Re-rank every indictment through `score_candidates` before writing it
  down.** The dossier's and the critique tool's `rule` field is the PRIMARY
  READING - the highest-priority same-call rule - not the rule that matched.
  Round 13 wrote three findings against the wrong rule because of it, and three
  more against a `shows` sentence that did not match its own constraint. Open
  the `requires` block; quote the numbers, not the sentence.
- **`par_gap` in the match rows is N/S-signed at BOTH tables.** Our gap is
  `+a_par_gap` and `-b_par_gap`; the corpus baseline is **-0.378**. Read at face
  value it inverts the verdict on the sandwich seat, `general_pull_or_sit` and
  `cl_new_*2`.
- **`is_unbid_suit` has no sharp tolerance** in `_EVAL_S2` and no rule uses it.
  The first rule to do so will leak: a suit that IS bid still scores 0.8 against
  a `[1, 1]` gate. Same species as `two_of_top3` in round 5.
- **The forcing new suit opposite a weak two is passed out.** `rw2_new_*` is
  `forcing: one_round` and `2$W - P - <new suit> - P - ?` has no context, so a
  seven-card weak two passes it at `uc_pass` fit 1.00. Fourth instance of the
  starved-forcing-seat species, found in round 13 while killing a different fix.
- **`responder_after_minor_rebid` has a ceiling, not a shape hole.** 18 tables,
  mean -2.78, our gap -5.00: 19- and 23-counts sign off in `rmr_4$M` / `rmr_3$m`
  because `rmr_4NT` demands `semi_balanced`. Larger than anything round 13
  shipped.
- **`nxj_X`, the negative double of a jump overcall, promises 8+ HCP and nothing
  else** at priority 70, above everything in its context, so a 3-2-5-3 nine-count
  doubles and partner can play a 4-3 fit.  The diagnosis is confirmed and the
  gate does not pay: round 14 measured a longest-suit cap plus a four-card-unbid-
  major requirement at **-5 held out** and reverted it, keeping the `shows`
  repair.  Same shape as `weakest_their_stopper`: two of the nine replacement
  calls score below the 0.9 fast path, so **author the landing seats first**.
- **There is no strong balanced notrump rung after I have already acted.**
  Round 14's reshaped FIX 18 (an 11-14 / 12-14 `i_have_acted` rung in
  `general_uncontested_continuation` and `general_competitive_low`) measured
  **-1 held out on ten changed boards, four up and four down** - a coin flip -
  and was reverted.  The bridge is sound; the rung leans on `weakest_their_stopper`,
  which does not gate, and that is the likeliest reason it does not pay.
- **After a 2C opening, partner's shown minimum is ZERO by construction.**
  `r2c_2D_waiting` is `requires: {}` and `gf_new_3$X` has no point floor, so every
  `rule_of_26_sharp >= 31` gate in the file is unreachable however strong the
  opener is.  `resp_2C` measures 15 tables, mean -0.60, our gap **-7.87**.  The
  repair belongs inside the 2C tree, not in `general_slam_try` (round 14 killed
  that patch: 0 of its 12 firings was a 2C auction).
- **`resp_1m_over_1H` has no weak jump shift at all.**  `1C - (1H) - 2S` on a
  six-card suit under a free bid has no rule; the `1S` overcall context has
  `nx_1m1S_wj_H`.  An additive sibling gap.
- **`nt_after_transfer` has no natural second-suit rung**, so a 5-6 hand after a
  transfer must choose between 3NT and four of the five-card major.
- **`opener_rebid_1H_1S` is the largest NON-SLAM negative family in the corpus**
  (30 tables, mean -2.37, our gap -6.07) and nothing in rounds 11-14 looks at it.
  The slam families are still the largest concentration overall: `general_slam_try`
  -12.10, `rkc_response_agreed_H` -9.67, `opener_rebid_after_2over1_minor` -9.10.
- **`fast_decision`, not `score_candidates`, is the engine's choice.**  Ranking by
  blended score mislabels 25 of 10,346 decisions - every one a rule at fit
  0.946/0.965 beating a fit-1.00 pass on priority.  `repro.rank_at()` returns
  SCORE order; its first row is not necessarily what the engine bid.  This is the
  primary-reading trap with a different mechanism.
- **A slice can be above baseline on board margin and far below it on par gap,
  and the two disagree in both directions.**  Quote both, always.  Corrected
  baselines: review **-0.729** per board, our par gap **-0.338**.
- **The soft-miss lottery is live at 0.946 in the notrump family.**  A measurable
  fraction of the engine's notrump decisions turn on half a point of `rule_of_26`
  clearing the 0.9 threshold rather than on an agreement.  Sharpening it measured
  3 tables / -2 IMPs in round 13 and was killed.
- **THE CODE FALLBACK IS THE LARGEST POPULATION IN THE ENGINE AND NOTHING HAS
  EVER RULED ON IT.**  456 of 10,358 decisions (4.4%) are made with no rule at
  all, at par gap **-3.89** against a stage-matched **+0.46** - about **-2,000
  attributable gap-points**, larger than every named family combined, replicating
  to within 0.3 across corpora.  Dump it grouped by `(context, call)`: that is a
  map of every hole in the file, produced by the engine itself, ranked by cost.
  Start a round there rather than with the per-decision audit.
- **The five responding contexts are a uniform hole the rule-level yardstick
  cannot see.**  `resp_1m[C]`, `resp_1m[D]`, `resp_1H`, `resp_1S`, `resp_1NT`:
  475 decisions at **-3.0 to -4.6** on both corpora, about -1,700 gap-points, and
  **not one rule inside them is indictable**, because every rung in a uniformly
  bad context sits at its own baseline.  The intervention has to be at context
  granularity - author the whole ladder - not at rung granularity.
- **`uc_nt2` was ruled OK on the wrong number in round 15 and is still open.**
  18 e10 / 27 r15 decisions, board margin -3.11/-2.48, gap -4.56/-3.93 against a
  stage baseline of -0.20; a third of its firings are soft-miss picks below the
  0.9 fast path and those run at **-9.17**.  Unlike `ballow_nt1` and `cl_nt1` it
  denies no shape.  Larger than any population round 15 proposed to change.
- **The soft-miss lottery is where "no agreement" becomes a bid.**  When pass is
  forbidden and nothing fits >= 0.9, the engine takes the least-bad misfit: board
  970b's whole candidate set was four rules with a best fit of 0.409.  Within one
  rule the split is large - `uc_nt2`'s sub-threshold firings are 7 points of par
  gap worse than its clean ones.  This is a scoring-model question, not a rule
  question, and it has never been attacked directly.
- **`open_2C` replicates at -7.44 / -6.58 and has been deferred four rounds.**
  Its bad half is shapely 18-21 two-suiters, but balanced 22+ counts are equally
  bad, so the opening condition is not what separates them - it is that the 2C
  auction has no landing ladder.
- **There is no context for opener's rebid after a 2/1 in a MINOR.**
  `opener_rebid_after_2over1_minor` is `1M - 2m` only, so `1D - P - 2C - P - ?`
  is unauthored and the generic 11-12 `uc_nt2` annexes a game-forcing seat.
- **Load the file and count the hand before writing the number down.**  Round 15
  lost three of five kills to its own errors: two miscounted hands (both 15, not
  14 and 13, i.e. inside the rule's own band), a `when` that could never fire
  (`we_bid_last: false` where the standing bid is ours in 20/20 tables), and YAML
  that does not parse (`$M` in a context with no `expand:`).  Round 13 made
  re-ranking a step; this is the companion step.
- **A wait-loop must not match its own command line.**  `while ps aux | grep -q
  "[s]weep.py"` and `until ! pgrep -f "match_ben.py run"` both match the shell
  running them and spin forever.  This cost an hour of a round waiting on matches
  that had already finished.  Poll the output file, not the process table.
- The system cannot bid a grand slam.

---

## The expert-review subagent prompt that works

Give each reviewer: the repo path (read-only), `DECISIONS.md` to read FIRST,
the dossier path, its slice of clusters, the scoring-model paragraph above, the
five verdict labels (IMPLEMENTATION-BUG / NEEDS-EXCEPTION / MISSING-AGREEMENT /
DELETE-THE-RULE / NOTHING-WRONG), an instruction to be willing to say
NOTHING-WRONG, a worked `choose_bid` snippet so it can verify before asserting,
a requirement to mark each finding VERIFIED or UNTESTED, and the shadowing
lesson above as a hard constraint.  Ask for a deduplicated FIX LIST in priority
order giving rule ids, exact replacement YAML, boards and IMPs at stake,
VERIFIED/UNTESTED, and what each fix ENDANGERS.

The two best behaviours this prompt has produced, both worth asking for
explicitly: reviewers re-scoring a suspect rule across ALL tables (winners
included) before accusing it - which is how "the biggest cluster is actually the
most profitable family in the engine" got found - and reviewers reporting
NEGATIVE results from their own prototypes rather than shipping them.
