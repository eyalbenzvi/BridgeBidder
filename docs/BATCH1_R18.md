# Batch 1 — the generic competitive ladder — MEASURED AND REVERTED

204 rungs across `general_competitive_low/high`, `general_balancing_low/high`,
`general_their_double` and `general_pull_or_sit`, from about sixty agreements.

**This was the round's best-supported subject before it was measured.** Three
independent instruments picked it:

* `coverage.py` — `general_competitive_low` (783) and `_high` (592) hold
  **1,375 of the 1,745** backlog decisions, five times anything else;
* `cfr.py` — `ch_pass`, the catch-all of `general_competitive_high`, is beaten
  by acting at **+1.90 ± 0.66 over n=67 (t = 2.9)**;
* the two reviewers named those four contexts **472 times** between them.

## The number

```
=== screen: batch1 competitive ladder ===
  pool           12000 boards
  boards changed 3497  (1236 up, 1263 down, 998 same margin)
  paired delta   -1107 IMPs   (-92.2 per 1000 boards)
  t              -3.18   (SE of the total 348)
  95% CI         [-1790, -424]  normal theory
  95% CI         [-1804, -433]  percentile bootstrap
  sd per changed board 5.89 IMPs
  resolution     this pool resolves 0.29 IMPs/changed board at 90% power
  --> REVERT - 95% bootstrap CI excludes zero and is negative
```

**3,497 changed boards.** Round 14's headline fix changed 15; round 17's
largest batch changed 69; item 4 changed 670. This is by a wide margin the
most powerful measurement in the project's history, and it is not a null
result — the interval **excludes zero**. Adding 204 well-reviewed rungs to the
emptiest subject in the file costs about **92 IMPs per 1,000 boards**.

## Where the damage is, recorded as a LEAD and not a verdict

First call that changes on each changed board, grouped (2,040 boards where the
screen kept both auctions):

| first change | n | total | mean |
|---|---|---|---|
| **`P → X`** | **556** | **-261** | **-0.47** |
| `P → 4D` | 46 | -65 | -1.41 |
| `P → 3C` | 76 | -59 | -0.78 |
| `2D → P` | 43 | -51 | -1.19 |
| `P → 2D` | 25 | -47 | -1.88 |
| … | | | |
| `P → 3H` | 91 | **+99** | **+1.09** |
| `P → 3D` | 96 | **+83** | **+0.86** |
| `P → 4S` | 42 | +32 | +0.76 |

**The new doubles are the loss and the new major-suit competitive raises are a
gain.** 556 boards where a pass became a double cost 261 IMPs on their own.
Meanwhile the Law raises the batch was built around — the thing the file had
nowhere in a minor — show up positive at the three level.

This is the best of several slices and therefore carries exactly the selection
premium this round's method exists to prevent, so it is written down as a
hypothesis to be **screened on its own**, not as a result.

## What it says about the round's premise

The premise was that the file is under-specified and that volume pays in
aggregate. On the subject where under-specification is most severe and best
measured, **volume measured clearly negative at t = -3.18**. Two readings
survive, and they are not the same:

1. **Density is not enough where the seats are generic.** These four contexts
   are dispatched on the shape of the auction, not on a partnership agreement,
   so a rung added there fires in auctions its author never saw. The catch-all
   pass is bad on average — `cfr.py` is right about that — but the specific
   replacements are worse than the average alternative it was measured against.
2. **A rollout's "an alternative beats this call" does not license a RULE.**
   `cfr.py` substitutes one call while partner reads it with the unmodified
   system; authoring the rung changes what partner hears. That hazard was
   documented before the batch was built, and this is what it costs.
