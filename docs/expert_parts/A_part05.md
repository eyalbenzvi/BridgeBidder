# EXPERT A — competitive / matchpoint duplicate — dossier part 05

Repo read-only.  38 boards, `docs/dossier_575757/part05.md`, worst-first.

## Summary

| | |
|---|---|
| boards reviewed | 38 (all) |
| proposals | 33 |
| NOTHING-WRONG (purely constructive, or the auction was normal) | 5 (938, 942, 291, 387, 515) |
| new rungs written and traced | 49 rungs + 1 new context + 7 gate/band edits |
| VERIFIED (traced through `score_candidates`, base vs patched) | 33 of 33 |
| locked-scenario regression (all 516 in `tests/data/*.yaml`) | 1 changed, **0 failing** before and after |
| blast radius, measured | **32 changed decisions in 2,606 of our calls over 250 boards (1.23%)**, spread across 26 distinct agreements |

**How the verification was done.**  Every proposal below was written into a
copy of `two_over_one.yaml` in a scratch directory, the whole file re-loaded
(517 -> 521 contexts, parses clean), and the losing decision re-ranked with
`prepare_decision` + `score_candidates`.  "VERIFIED" below always quotes the
actual before/after top candidate.  I then replayed **all 516 locked
regression scenarios** through `decide_fast` under base and patched: exactly
one moved (`harvested::e1_doubler_raises_the_advance`, 4S -> 3S, still inside
its accepted set `["4S","2S","3S"]`), and nothing that passed began to fail.
Finally I re-decided every one of our calls on the first 250 boards of
`reports/r18_before.jsonl` under both trees to price the blast radius.

**Whole-corpus denominators used before accusing anything**
(`repro.fires_summary('reports/r18_before.jsonl', …)`; corpus mean board
margin **-0.489**):

```
sw_X          23 tables  -39  mean -1.70      cl_nt2         8 tables -21  mean -2.62
uc_nt2        21 tables  -33  mean -1.57      ballow_X      11 tables -32  mean -2.91
nx_1m1S_X     21 tables  -21  mean -1.00      sw_2C          8 tables -22  mean -2.75
nxj_X         18 tables  -22  mean -1.22      ballow_nt2_strong 7 tables -16 mean -2.29
bal_X         14 tables   -3  mean -0.21      ch_new_C5      2 tables -15  mean -7.50
cl_new_H2     16 tables  +12  mean +0.75      ch_rebid_H4    3 tables  +5  mean +1.67
aw2S_2NT       2 tables   +5  mean +2.50      cl_takeout_X   1 table  -10  mean -10.0
```

Two of those numbers changed a proposal.  `bal_X` is **above** the corpus mean
(-0.21), so board 705's fix WIDENS the balancing double instead of gating it.
`cl_new_H2` is a **net winner** (+12/16 tables), so board 64's misfit pass was
written as narrowly as I could make it (singleton in partner's overcalled
major, under opening values, two-level only) rather than as a band change.

### The three agreements that matter most in this slice

1. **The Law raise does not need three trumps when partner has promised six,
   and it is not a game raise on eight.**  `cl_raise_lott_short_$M` (board 809)
   and `ballow_raise_brake_$M` (board 19) are the two halves of one idea: the
   file's raise ladder is separated by POINTS and never by trumps, so a
   doubleton opposite a known six-card suit cannot raise at all while a 4-4 fit
   with a shaded 25 estimate leaps to game.  Nine boards in the eight parts of
   this dossier are partscore pushes of exactly this kind.

2. **Every generic "natural notrump in competition" rung is responder's rung
   being applied to a player who has already bid his hand.**  `uc_nt2`,
   `ballow_nt2_strong` and `cl_nt2` between them fire on 36 tables at -70 board
   margin, and boards 508, 243, 276 and 520 are four separate instances of the
   same thing: a seat that has already made a descriptive bid repeats it in
   notrump.  One `when: { i_have_acted: false }` closes most of it.

3. **A double is only worth writing if a seat answers it.**  Board 119's
   penalty double of their 1NT overcall is the strongest single call in this
   slice — and the first version of it LOST the board, because opener pulled it
   to 2C at `uc_rebid_C2` fit 1.00.  `general_pull_or_sit`'s `adx_sit` demands
   `their_last_bid_suit`, so it can never sit for a double of notrump.  The
   proposal ships `adx_sit_nt` with it.  Same species as round 17's -9.8 cue.

### Negative results from my own prototypes, reported rather than shipped

* **`ch_pass_no_save`** (board 838, first attempt): a PASS rung gated on
  `partner_shown_length: [0, 2]`.  It never fires — with no argument that
  evaluator resolves to partner's FIRST shown suit, not to the suit I am about
  to invent, so it was measuring partner's hearts while I was bidding clubs.
  Replaced by a seven-card requirement on `ch_new_$X5`.
* **`we_vulnerable: false` on `ch_new_$X5`** (board 838, second attempt): I had
  the vulnerability backwards — on that board the save was at FAVOURABLE
  vulnerability and cost only 120, so a vulnerability gate is not the
  agreement.  The agreement is the fit, not the colours.
* **`passed_hand: true`** on board 419's rung: `Auction.is_passed_hand` only
  looks at calls BEFORE the opening bid, so a responder who passes over
  partner's own opening is not a "passed hand" by that test.  The gate was
  silently unfireable; dropped, and the HCP ceiling does the work instead.
* **Board 243's own fix makes board 243 worse.**  `v1NT_2H_long` gets N to bid
  2H over their 1NT with a six-card suit — but on this deal 2H is down two
  (-100) against the -90 we actually scored.  The rung is right bridge and the
  board is a counter-example; the call that actually loses board 243 is at the
  other table, and that is `ballow_nt2_strong`.  Both are written up.

---
