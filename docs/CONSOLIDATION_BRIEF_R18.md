# Consolidation brief — merging Expert A and Expert B, per dossier part

Two reviewers went over the SAME lost boards independently and never spoke:

* **Expert A** — competitive / matchpoint duplicate: contested auctions,
  overcalls, doubles, preempts, competitive judgement, balancing, the Law of
  Total Tricks, sacrifices, defending against interference.
* **Expert B** — constructive / team IMP: uncontested constructive sequences,
  the 2/1 GF machinery, invitational structures, game and slam investigation,
  trial bids, control-showing, shape-showing, notrump ladders.

They were given different lenses ON PURPOSE.  **Disagreement between the two
disciplines is signal, not noise**, and it is resolved downstream by a third
reviewer (a system editor), not by you.

## Your job, per board

1. **Where they AGREE** — same seat, same missing agreement, whatever the
   wording — keep ONE proposal.  Take the better-specified YAML (correct
   template-var placement, an answering seat present, a priority argued
   against the rungs below).  Note "A+B agree".
2. **Where they DISAGREE** — different seat, different call, or the same call
   with incompatible meaning — **keep BOTH**, mark `DISAGREEMENT`, and state
   in one line what the disagreement actually is, so the editor can rule on
   it.  Do not pick a winner.
3. **Where only one of them proposed anything** — keep it, marked `A only` or
   `B only`.  A NOTHING-WRONG from one and a proposal from the other is NOT a
   disagreement: keep the proposal, note that the other saw nothing.
4. **Where they both said NOTHING-WRONG** — record the board as NOTHING-WRONG
   with one line of why.
5. **Where they touch the SAME rule or context** — different rungs in one
   context, or one adding a gate to what the other extends — resolve the
   INTERACTION explicitly: say whether the two edits compose, and if they
   collide say so under `INTERACTION`.

## Deduplicate across boards

Several boards will motivate the SAME agreement (a missing help-suit game try
will show up five times).  Collapse those into ONE entry that lists all its
motivating boards.  At the end of your file, give:

* the count of distinct AGREEMENTS in your part;
* the count of concrete RULES they will produce after templating (`expand` /
  `expand_pairs`), summed;
* the list of agreements that appear in other parts too, if you can tell.

## Format

`## Board N` sections in dossier order, then a `# AGREEMENT INDEX` section at
the end.  Per board keep it TIGHT — the YAML, one sentence of bridge, the
answering seat, what it endangers, VERIFIED/UNTESTED, the templating — and
drop the reviewers' prose.  The editor has to read eight of these files.

Mark every entry with one of: `A+B`, `A only`, `B only`, `DISAGREEMENT`,
`NOTHING-WRONG`.

## Corrections that post-date the reviewers — apply these while merging

1. **`when: { partner_limited: … }` WORKS NOW.**  Two reviewers noted it as
   raising `NameError` (round 17's open item 5).  It was fixed during this
   round, with a test.  A proposal parked on that bug is live.
2. **Running two systems in one Python process is safe now.**  One reviewer hit
   corrupted results prototyping against a patched copy; that was the
   `_SETUP_CACHE` identity bug, also fixed this round with an end-to-end test.
   Any finding that reviewer marked doubtful for that reason can be trusted.
3. **Item 4 (the unconditional code fallback) was measured and KILLED**
   (-162 IMPs over 670 changed boards, t = -1.03; and its interpretation half
   breaks the support-double negative-inference invariant).  So the
   **"adding a rung deletes the code fallback for that call" trap is STILL
   LIVE.**  Every proposal that adds a rung is subtracting the fallback that
   used to catch the hands the rung does not fit.  Where a reviewer justified
   a rung as "structurally safe, purely additive", downgrade that claim and
   note it — it is not true, and it is why every batch gets screened.
4. **The primary-reading trap caught three reviewers** (boards 953, 12/255, 261
   and possibly others): the dossier's `rule` column is produced by
   `sweep.deciding_rule()`, but a reviewer quoting a rule id from elsewhere in
   the record may still have the wrong one.  Where a proposal's argument rests
   on a named rule, check the fit quoted beside it: a rule at fit 0.034 or
   0.409 is not what chose the call.

## Two measured signals to weigh proposals against

* **`coverage.py`**: 24.0% of our LIVE decisions are made by a rule whose
  `requires` is empty.  `general_competitive_low` (783) and
  `general_competitive_high` (592) hold 1,375 of the 1,745 backlog decisions —
  five times anything else.  See `docs/COVERAGE_R18.md`.
* **`cfr.py`**: `ch_pass`, the catch-all of `general_competitive_high`, is
  beaten by acting at **+1.90 ± 0.66 over n=67 (t = 2.9)**.  Four other rules
  are systematically beaten, all with n ≤ 11.  See `docs/CFR_R18.md`.

Proposals that put real rungs into those two contexts have independent
measured support.  Say so where you see one.
