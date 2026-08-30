# Round 18 reviewer brief — one agreement per lost board

## The situation, in numbers

BridgeBidder is a 2/1 Game Forcing bidding engine whose **system is data**:
`src/bridgebidder/systems/two_over_one.yaml`, 517 contexts and 2,344 rules.
It is measured by duplicate matches against BEN, a neural-net bidder: the same
deals played at two tables, scored in IMPs.  Seventeen rounds took it from
-1474 to -474 IMPs per 1000 boards.

**Round 17 established that the old loop — find a defect, change one rung,
measure — is finished.**  Every single-rung intervention it made measured
indistinguishable from zero (the best-motivated one: -42 IMPs over 39 changed
boards, t = -0.70; a 28-rule batch: -41 over 69 boards, t = -0.57).  An
unbiased ablation says rounds 11-16 were nonetheless real (+53 IMPs per 1000,
t = 6.86), so the record is honest — the loop has simply stopped paying.

The diagnosis is that the file is **UNDER-SPECIFIED, not mis-specified**.  The
conventions that separate a slam-going hand from a minimum below game are at
exactly **zero** rules each: trial bids 0, serious/frivolous 3NT 0,
mini-splinters 0, fit-showing jumps 0, control-showing raises 0.  55 rules bid
at the five level; **0** at the seven.

## Your job

**You are not hunting for defects.  You are manufacturing agreements — one new
rule or sub-rule for EVERY board in your dossier.**  Expect to propose one per
board.  Do not prune your list to look disciplined; prune it only for
correctness, conflict and coherence.  Somebody else consolidates and edits.

A board can also be lost to a normal auction.  **NOTHING-WRONG is a legitimate
verdict and you must be willing to give it** — but say what you checked.

## What to produce, per board

1. **Board number** and the seat/call that went wrong (or NOTHING-WRONG).
2. **The missing agreement**, in ONE sentence of bridge.
3. **EXACT YAML** — context id (existing or new), rule id, call, priority,
   `when`, `requires`, `shows`, `establishes`.  It has to be implementable
   verbatim; see `docs/DSL_FOR_EXPERTS.md` for the vocabulary and the two id
   rules that break templating.
4. **THE ANSWERING SEAT.**  If your new call is a force, an ask or an
   invitation, the seat that ANSWERS it ships in the same proposal — context
   pattern and rungs.  This is not optional.  Round 17 measured the cost of
   ignoring it: a cue bid above game with no answering seat costs **-9.8 IMPs
   a seat**, because partner has no context, passes it out, and we play 5C.
   That number was measuring an empty seat, not a bad call.
5. **WHAT IT ENDANGERS.**  List every existing rule in that context whose call
   your new rung can legally outrank — the rungs BELOW it as well as above —
   and give one sentence of bridge saying why yours is the better description
   of the hand.  Round 17 broke two locked scenarios with one rung by
   reasoning only upward.
6. **VERIFIED or UNTESTED.**  VERIFIED means you actually traced it through
   `repro.rank()` (snippet in the DSL doc).  Do not label anything VERIFIED
   that you did not run.
7. **TEMPLATE?**  Should the same agreement be expanded across suits, seats,
   levels or vulnerabilities (`expand` / `expand_pairs`)?  Most should be, and
   that is how a few hundred ideas become a few thousand rules.  Say exactly
   which expansion.

## Two behaviours that have paid before, asked for explicitly

* **Re-score a suspect rule across ALL its firings, winners included, before
  accusing it.**  `repro.fires_summary(path, rule_id)` gives the honest
  denominator.  This is how "the biggest cluster is actually the most
  profitable family in the engine" got found.
* **Report NEGATIVE results from your own prototypes** rather than shipping
  them.  A proposal you tried and that made the board worse is a finding.

## The scoring model — the one paragraph that decides everything

> Candidates are scored by soft Gaussian fit against each rule's `requires`.
> **The fast path is fit >= 0.9 then max priority; below that the blended score
> decides; every generic context ends in a catch-all pass at fit 1.00, so any
> hole in a ladder is a PASS by construction.**

So `all-pass` or `fallback` in a dossier names a **starved seat**, not a bad
rule.  And a rule that misses its own gate by a point can still win when
nothing fits ("the soft-miss lottery").

## GUARDRAILS — every one of these has cost this project a cycle

* **`explanation.source_rule_id` and the dossier's `rule` field are the PRIMARY
  READING**, the highest-priority rule producing the same call — not
  necessarily the rule that chose it.  Use `sweep.deciding_rule()`.  This has
  produced false findings twice.
* **A force, an ask or an invitation ships with the seat that answers it.**
* **Price a new rung against the rungs BELOW it, not only the one above.**
* **Adding a rung DELETES the code fallback for that call** in every seat its
  `when` reaches, because `covered` is built without consulting fit.  So an
  "additive" rule is not automatically safe.
* **Adding a GATE or a MORE SPECIFIC CONTEXT subtracts behaviour everywhere it
  reaches.**  A new context that shadows an existing one must carry the
  shadowed rule's gates verbatim so it can only ever be a superset.
  `pattern: "... - ?"` is the least specific pattern in the file and sorts
  last, which gets you the superset property structurally.
* **Template vars must END a rule id** (`id: foo_$M`, never `id: foo_$M_bar`),
  and `call: $L$X` does not expand — write the level out.
* **Load the file and count the hand before writing a number down.**  Round 15
  lost three of five kills to miscounted hands and unfireable `when` gates.
* Never trade explainability for score: every gate must be one sentence of
  bridge.

## Measured-neutral or scope-excluded — do NOT re-propose

Tightening `uc_nt3`'s strength gate; opening-style / rule-of-20 thresholds;
3NT-versus-5m preferences; Michaels / unusual notrump as convention additions;
the 5NT king ask as a standalone; both points-estimator repairs; "a takeout
double must not hide a six-card suit"; sweeping the negative doubles onto
`standing_suit_length`; the four-level pull; the 2NT-Stayman-over-interference
twin; a non-forcing responsive double; re-ranking the weak jump overcall;
freeing `cl_raise_lott3_$M`; the `weakest_their_stopper` sharp-tolerance
repair; a `keycards >= 3` gate on the keycard ask over a game raise; routing
`uc_*` positions to the competitive contexts wholesale.  `DECISIONS.md` is
authoritative and you should read it.

## Files to read FIRST

1. `DECISIONS.md` (long; skim the round-by-round ledger, read the open items)
2. `docs/ROUND_METHOD.md` — especially "Known open items" and the lessons
3. `docs/ROUND_17_REPORT.md` and `docs/PLAN_SCALE_THE_SYSTEM.md`
4. `docs/DSL_FOR_EXPERTS.md` — the vocabulary your YAML must be written in
5. `src/bridgebidder/systems/two_over_one.yaml` — grep it constantly; never
   propose a rule without looking at the context it lands in
