# Per-decision regret, measured (round 18)

`tools/roundkit/cfr.py` was written in round 17 and never run.  Run here on the
whole 575757 corpus: **10,335 of our decisions, BEN disagreed on 2,046 (19.8%),
3,465 rollouts in 418 s.**

At each decision where BEN disagreed, an alternative call is substituted, the
auction is finished with **our engine in our seats and BEN in the opponents'**,
and the result is scored double-dummy.

    mean IMP change from substituting an alternative: -0.66 +/- 0.10

Negative is the expected sign: a system that mostly bids sensibly should lose
by deviating from itself.

## Rules an alternative systematically BEATS (n >= 8, mean > 2 SE)

| rule | mean | n | what it is |
|---|---|---|---|
| `r1m_2over1` | **+4.45 ± 2.05** | 11 | the 2/1 GF response in clubs, 12+ HCP |
| `oc1D_1NT` | **+4.12 ± 1.92** | 8 | the 15-18 balanced 1NT overcall of 1D |
| `oc1S_2C` | **+3.45 ± 1.30** | 11 | the two-level club overcall of 1S |
| `r1S_raise_passed` | **+2.62 ± 1.05** | 8 | the passed-hand 10-11 raise of 1S |
| **`ch_pass`** | **+1.90 ± 0.66** | **67** | **the catch-all pass of `general_competitive_high`, `requires: {}`, priority 22** |

`ch_pass` is the one with a population behind it: n = 67, **t = 2.9**, and it
is the rule that takes the seat whenever nothing in the file describes a hand
over the opponents' high-level contract.  It says the same thing coverage.py
says from an unrelated direction — `general_competitive_high` carries **592**
vacuous decisions, second only to `general_competitive_low`'s 783 — and it
adds the part coverage cannot see: **acting is worth about two IMPs a seat
more than the catch-all pass.**

On a 150-board pilot the indicted catch-all was `cl_pass` (+1.30 ± 0.58,
n = 27), `general_competitive_low`'s equivalent; at full corpus it no longer
clears the bar and `ch_pass` does.  Both readings point at the generic
competitive contexts; only the full-corpus one is quoted as a number.

## Rules that HOLD UP — the honest other half

The strongest are `rkc_5D` (-8.50 ± 2.70), `pref_2NT` (-7.67 ± 1.20),
`ballow_reopen_X` (-6.00 ± 1.95), `inv_accept_3NT` (-5.90 ± 2.04) and
`r1m_1S` (-5.50 ± 1.65): deviating from them costs five to eight IMPs a seat.
The keycard reply and the balancing reopening double are doing real work, and
neither should be touched.

## The two hazards, stated rather than buried

This is a **lead, not a verdict**, for two documented reasons:

1. A substituted call is read by partner with the **unmodified** system, so a
   rollout measures **unilateral deviation**, not a partnership agreement.
   Adding the rung that makes the alternative meaningful changes what partner
   hears, which is exactly what the rollout cannot model.
2. Double-dummy scoring **rewards a lie whose partner is misled favourably**.

Both are why the round's acceptance test is the screen on the pool, not this.
