# Batch 2 — support doubles and the seat that answers them — SHIPPED

46 contexts, 257 rules. Applied first time with no repairs: 769 passed, lint
unchanged at 223, fuzz exit 0.

## The number

```
=== screen: batch2 support doubles + answering seats ===
  pool           12000 boards
  boards changed 216  (74 up, 44 down, 98 same margin)
  paired delta   +200 IMPs   (+16.7 per 1000 boards)
  t              +2.55   (SE of the total 78)
  95% CI         [+46, +354]  normal theory
  95% CI         [+44, +355]  percentile bootstrap
  --> SHIP - 95% bootstrap CI excludes zero and is positive
```

**This is the first change in the project's history to clear the acceptance bar
round 17 set** — a positive result whose bootstrap interval excludes zero. For
contrast, round 14's headline +51, which set the standing -474, measures
t = 1.73 with CI [-5, +111]; it was accepted under the old "keep if positive"
rule, which round 17 retired.

## What it is

The round's strongest A/B convergence. Both reviewers, from different
disciplines and without contact, found on the same boards that **support
doubles and redoubles exist only after a MINOR opening**, so after
`1H - P - 1S - (X)` opener has no support call at all.

Expert B found the larger half: **no seat in the file ANSWERS a support double
in any of its five auctions.** `1D-1S-2C-X-P-?` falls to `general_pull_or_sit`,
which pulls our own double at fit 1.000. The denominator it ran before
accusing anything: `sd_double` is +0.20 over 5 tables, while the six
`adx_pull_my_*` rules that answer it run **-3.00 over 15 tables**.

Three things about the construction are worth carrying forward:

* **The ask ships as a superset, structurally.** `support_double_wide` and
  `support_redouble_wide` use five-token patterns that TIE with the existing
  contexts on specificity and lose the tie by file order, so the four clean
  minor auctions keep every existing rung untouched while the major twin and
  the LHO-competed twin get the whole ladder.
* **Every landing has a `requires: {}` floor at the bottom of its ladder**, so
  no new seat can starve — and a floor was deliberately NOT put inside
  `support_double` itself, because a locked arbitration case harvested at
  exactly `1D-P-1S-(X)` catches that.
* **The ask alone would have been a rung.** The ask plus the seat that answers
  it is a closed conversation. That is round 17's lesson, and it is the first
  thing this project has measured as a significant gain.
