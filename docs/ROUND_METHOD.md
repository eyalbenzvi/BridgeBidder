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

**The number that matters is the HELD-OUT one.**  The review corpus is the one
place a fix is guaranteed to look good, because it is where the fix was found.

---

## The loop

1. **Fresh match.**  `python3 tools/match_ben.py run --n 1000 --seed <NEW> --out reports/<tag>_before.jsonl`
   Pick a seed never used before (used: 7, 828282, 919191, 303030, 515151,
   626262, 747474).  ~5 minutes.  Report with
   `python3 tools/match_ben.py report --rows reports/<tag>_before.jsonl`.
2. **Triage.**  `python3 tools/triage_match.py reports/<tag>_before.jsonl <SEED> <dossier>.md`
   Clusters the losing boards by the rule that made our last bid at the table
   where we did worse against par, plus the worst singles.
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
   The current bar is **-621** (`reports/x3_weak2_heldout.jsonl`).
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
- `qr3_4NT_quant`: 7 tables, -67 IMPs, zero wins across a corpus - a
  DELETE-THE-RULE candidate nobody has yet measured.
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
