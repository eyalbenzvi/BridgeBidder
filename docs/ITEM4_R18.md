# Item 4 — the unconditional code fallback — MEASURED AND KILLED

Round 17 nominated this as **"the one remaining change with enough blast radius
to resolve a 1 IMP/board effect at full power"**, applied it, measured its blast
radius at 216 changed decisions per 1,000 boards, and reverted it **unmeasured
in IMPs**.  Round 18 measured it.

## Why it mattered

`prepare_decision` builds `covered` from every rule whose `when` holds and whose
call is legal — **fit is never consulted** — and `generate_fallbacks` only
generates candidates for calls NOT covered.  So **adding a rung deletes the code
fallback for that call in every seat the rung's `when` reaches**, whether or not
the hand fits the rung.  That is the trap that makes a 200-rule batch dangerous,
which is exactly what this round is.

The reviewer's instruction was: **ship BOTH halves or NEITHER**, measured
separately because they push in opposite directions.

## The generation half — measured, the best-powered number in the project

`frozenset(covered)` → `frozenset()` at `inference/engine.py:526`.

```
=== screen: item4 generation half ===
  pool           12000 boards
  boards changed 670  (195 up, 225 down, 250 same margin)
  paired delta   -162 IMPs   (-13.5 per 1000 boards)
  t              -1.03   (SE of the total 158)
  95% CI         [-471, +147]  normal theory
  95% CI         [-476, +147]  percentile bootstrap
  sd per changed board 6.10 IMPs
  resolution     this pool resolves 0.68 IMPs/changed board at 90% power
  --> REVERT (not distinguishable from zero)
```

**670 changed boards.**  For scale: round 14's headline fix changed 15, and
round 17's largest batch changed 69.  This is the first measurement in the
project with enough power to resolve well under 1 IMP per changed board, and
what it resolves is **nothing** — a point estimate of -13.5 IMPs per 1,000
boards with a confidence interval covering zero.

## The interpretation half — never reached a number, and did not need to

Where a live fallback exists for a call, widen that call's constraint to
`any_of(rule meanings + the fallback meaning)`, so the engine cannot bid by
fallback while partner reads the call as a rule.

Applied on top of the generation half: **29 tests fail.**

| failing | what it is |
|---|---|
| 13 | locked regression scenarios |
| 13 | frozen explanation snapshots |
| 1 | **`test_support_double_negative_inference_in_samples`** |
| 1 | arbitration returns a sound call |
| 1 | (collateral: this round's own aliasing probe) |

The single most important one is the support-double invariant — the canonical
test this project's README leads with: *after `1D - P - 1S - (2C) - 2D`, no
sampled deal gives opener exactly 3 spades, because he would have made a
support double.*  Widening every call's constraint to admit the fallback's
hands **destroys the priority-ordered negative inference**, which is the
engine's central explainability asset and the thing the project rule "never
trade explainability for score" exists to protect.

That is not a locked scenario to be overwritten with a better number.  It is
the change telling you what it costs.

## Verdict

**NEITHER HALF SHIPS.**  The generation half is indistinguishable from zero at
670 changed boards; the interpretation half breaks the negative-inference
contract.  `engine.py` is restored to its pre-item-4 state and **769 tests
pass**.

## What this costs the rest of the round, stated plainly

The trap is still there.  Every rule this round adds still deletes the code
fallback for its call in every seat its `when` reaches, so **no rule in this
round is "safely additive" and every batch must be screened rather than
assumed.**  That was already the plan; it is now a measured necessity rather
than a precaution.

## The honest reading

Round 17 called this the highest-value remaining item and it was right to: it
was cheap, it had the power to settle itself, and settling it removes a
standing hypothesis.  The answer is that the code fallback's conditionality is
**not worth IMPs in either direction** — which also retires the round-16
finding that the fallback population was "the largest attributable population
in the engine".  It is large, and it is neutral.
