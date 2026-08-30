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
