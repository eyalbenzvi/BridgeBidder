# EXPERT A — competitive / matchpoint duplicate — dossier part 06

38 boards (-122 IMPs), all of them -3 or -4.  **34 proposals, 4 NOTHING-WRONG**
(864, 582, 767, 861).  Every proposal was prototyped by loading a *copy* of
`two_over_one.yaml` with the rung inserted and re-running `score_candidates` /
`fast_decision` on the exact seat, hand, vulnerability and auction from the
dossier; the repo file was never touched.  **31 of 34 are VERIFIED that way,
with controls**; 3 are UNTESTED and say so.

Whole-corpus denominators (`repro.fires_summary('reports/r18_before.jsonl', …)`)
were pulled before demoting anything.  The ones that changed a verdict:

| rule | tables | mean | effect on this review |
|---|---|---|---|
| `v3_D_X` | 5 | **+1.60** | the takeout double of a preempt is a WINNER — board 98's rung was cut back to solid six-card suits only |
| `ballow_reopen_X` | 4 | **+3.75** | board 991's rung was checked to be mutually exclusive with it, not above it |
| `xd_run_S2` | 3 | **+0.67** | board 864 turned into NOTHING-WRONG |
| `open_pass_4th` | 4 | **0.00** | board 76's rung has no corpus support and is labelled speculative |
| `oc1D_1NT` | 7 | -4.57 | board 772 |
| `cl_rebid_jump_H` | 5 | -4.80 | board 850 |
| `cl_new_C3` | 12 | -3.92 | board 774 |
| `ob_1D1H_2C` | 7 | -3.57 | board 918 |
| `sw_2C / sw_2S / sw_2H` | 8 / 2 / 6 | -2.75 / -4.50 / -2.67 | boards 103, 199 |
| `uc_rebid_C3` | 10 | -2.10 | board 474 |
| `uc_nt2` | 21 | -1.57 | board 905 |
| `cl_negative_X2` | 15 | -2.07 | board 852 — CAUTION, my rung widens a losing family |
| `rrevh_2S`, `cl_new_long2_H_hi`, `ch_new_H3_hi` | 0 | — | starved rungs, boards 506 / 646 / 548 |

## The three agreements that matter most in this slice

**1. The takeout double of a PREPARED MINOR (boards 23, 512, 803; ~-11 IMPs).**
`oc1C_X` / `oc1D_X` demand at most a doubleton in their suit.  Nobody opens a
three-card major, but everybody opens a three-card minor, so the shortness test
is imported from the wrong opening.  Three seats in 38 boards passed a hand
every expert doubles: 4-3-3-3 thirteen- and fourteen-counts (23, 512) and a
4-4-4-1 ten-count with the singleton in their suit (803).  Two rungs
(`oc1x_X_flat`, `oc1x_X_shape`) across all four `overcalls_of_1x` contexts.
This one is a large behaviour change and deserves its own screened experiment.

**2. THE DISCIPLINE PASS: once I have described my hand, my second voluntary
bid in competition is the file's most expensive habit** (646, 103, 198, 230,
433, 474, 548, 820, 863 — nine boards, ~-30 IMPs).  There is no rung anywhere
in the four generic competitive contexts that says "I have already shown this
hand; pass".  Every ladder ends in a catch-all pass at priority 18-22, *below*
every natural bid, so the engine bids whenever anything fits at all.  The
repair is a family of narrow, high-priority PASS rungs — safe by construction,
because a pass is already covered in every one of those contexts so no code
fallback is deleted, and because a `requires` that only the described hand fits
cannot outrank anything on a hand it does not describe.

**3. THE LAW OF TOTAL TRICKS IS THE TEST IN A CONTESTED AUCTION, `rule_of_26`
IS NOT** (258, 597, 850, 198).  The file already knows this — the comment above
`cl_raise_lott4_$M` says it in as many words — and then never generalises it.
`ch_raise_$M3` still gates the three-level competitive raise on
`rule_of_26 >= 22`, so a nine-trump fit opposite a weak two cannot be raised;
there is no Law raise in a MINOR at any level; and nothing anywhere says that
eight trumps means eight tricks, so the engine competes to three on a 5-3 fit.

---
