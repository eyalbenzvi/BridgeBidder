# Expert B — constructive / team-IMP bidding, dossier part 2 (38 boards, -389 IMPs)

**Scope of this review.** I read every board through the uncontested constructive
lens: the 2/1 machinery itself, opener's and responder's rebid ladders, the
forcing notrump, the invitational/game boundary, and the shape- and
control-showing that separates a minimum from a slam-going hand **before game
is reached**.  Round 17's finding is my mandate: nothing above 4M pays, because
by 4M the information exchange has already failed.

## Tally

| | count | boards |
|---|---|---|
| **Proposals (all VERIFIED)** | **20** | 12, 90, 94, 174, 175, 400, 545, 598, 606, 636, 708, 728, 751, 789, 790, 800, 866, 879, 909, 953 |
| Proposals reported as NEGATIVE prototypes (the agreement is real, it does not fire on this board) | 2 | 482, 622 |
| NOTHING-WRONG in my discipline (competitive from the first or second call, or opening style) | 16 | 133, 253, 255, 269, 396, 408, 487, 532, 695, 773, 791, 823, 837, 856, 858, 957 |

**Verification.** The repo was not modified.  Every proposal was written into a
scratch copy of `two_over_one.yaml`, loaded with `load_system(path=…)`, and
traced through `repro.rank()` / `sweep.deciding_rule()`.  **All twenty were then
loaded SIMULTANEOUSLY** — one file, 20 new agreements, 18 new contexts, 6 rungs
added to existing contexts — and all 30 seat checks (the trying seat and the
answering seat of each) still produce the intended call.  The batch parses, and
there is no cross-interference between the proposals.  Where a rung is placed
above an existing one I list what it can outrank and why mine is the better
description.

## The three agreements that matter most in this slice

1. **The help-suit trial bid (board 90) — the file's first, and the vocabulary
   count says trial bids are at exactly ZERO rules.**  `responder_rebid_after_1M_raise`
   offers opener three calls opposite a single raise — pass, a blunt 3M, or 4M —
   so a 5-4-3-1 sixteen-count either blasts a game that needs help or gives up.
   The proposal is a closed conversation: `help_suit_game_try` (five suit pairs,
   uncontested and competitive) plus `responder_over_help_suit_try`, which
   declines with `requires: {}` so the seat can never be starved.
2. **`resp_1M_over_2x` is missing its sixth combination, `1H - (2S)` (boards 953
   and 800).**  The template only covers overcalls in a *lower* suit, so after
   `1H - (2S)` responder has **no single raise, no cue-bid raise and no Law
   raise** and falls through to `general_competitive_low`, where the only rungs
   are the generic `cl_raise_H3`/`cl_raise_H4`.  Board 953 is the whole cost in
   one picture: a 10-count limit raise jumps to 4H, opener reads "11+ support
   points and the values", asks for keycards and plays 6H off two.  This is the
   safest species of change in the project — a sibling completion — and it is a
   below-game slam-machinery fix exactly as round 17 described.
3. **There is still no context for opener's rebid after a 2/1 in a MINOR
   (board 545).**  `opener_rebid_after_2over1_minor` is `1M - 2m` only, so
   `1D - P - 2C - P - ?` is unauthored and every candidate is a soft-miss: the
   engine's best fit is **0.134**, and `uc_nt2` — "natural 2NT: 11-12 balanced" —
   annexes a game-forcing seat holding fifteen and six good diamonds.  Partner
   then reads 11-12, and the auction ends in a quantitative 4NT that goes down.
   This is the ledger's own open item, verified on a real board.

## Two cross-cutting observations

* **Every proposal here is a landing or an answer, not a new question.**  Nine
  of the twenty are the seat that ANSWERS an existing force or invitation that
  the file already makes and never authored a reply to
  (`or1mn_jump_$m`, `rw2_new_*`, `r2c_3C_nat`, the reverse, the 1NT rebid, the
  balancing 2NT, `oc2nresp`, the preference, the transfer-completion).  Round
  17 priced an unanswered force at **-9.8 IMPs a seat**; this slice contains at
  least nine of them.
* **`... - P - ?` is doing constructive bidding it was never written for.**  In
  this slice `uc_pass`, `uc_nt2`, `uc_nt3`, `uc_new_*3`, `uc_raise_*` and
  `uc_rebid_*` decided **fourteen** game-forcing or invitational constructive
  seats.  The traces are in the individual boards; every one of them is a hole
  in an authored ladder, not a bad generic rule.

---
