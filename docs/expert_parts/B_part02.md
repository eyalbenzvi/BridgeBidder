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

## Board 487 — NOTHING-WRONG (competitive)

RHO opens a weak 2H at trick zero at both tables; there is no uncontested
constructive seat on this board.  Checked: N's pass over 2H (`vw2_pass`, fit
1.000 against `vw2_X` at 0.800) and E's `w2x_raise4` at table B, which is a
sound Law raise on 11 HCP and four trumps opposite a disciplined weak two.
Both belong to the competitive reviewer.

**Constructive observation.** At table B our side opened a weak two with
`KJ985.T.T8.AKT52` — 5-5 in the blacks and 11 HCP — and once RHO doubles there
is no rung anywhere in the file for a two-suited opener to show the second suit.
That is the general density point, not a board-specific defect.

---

## Board 532 — NOTHING-WRONG (competitive)

Both first divergences are overcall decisions (`oc1S_pass` vs `oc1S_2H` at fit
0.757 with a 13-count 6-5).  Every one of our calls after call 2 is made under
an opposing bid.

**Constructive observation.** The 5-5 shape problem recurs: S opened 1S on
`KJ985.T.T8.AKT52` and, over the 2H overcall, the file's only shape-showing
call for a 5-5 opener is a natural 2S rebid it never reaches.  A "fit-showing /
second-suit at the three level" family is the missing vocabulary; it is worth a
subject of its own, not a rung on this board.

---

## Board 751 — PROPOSAL — responder's game-forcing jump in the unbid minor after the 1NT rebid

**Seat/call that went wrong.** Table B, call 6, **E** after `1C - P - 1S - P -
1NT - P`, holding `AQJ9.AK6.AJ8532.` (19 HCP, 4-3-6-0).  The engine bid **2D**
via `uc_new_D2` — "natural D at the cheapest level: 5+ cards, 10+ points" —
because `responder_rebid_after_1NT_rebid` has no rung for a hand whose second
suit is longer than its major.  Opener passed the auction out in 3D with 3NT
cold for twelve tricks.

**The missing agreement.** Opposite the 12-14 notrump rebid, a jump to three of
the unbid minor is a natural game force showing five or more cards there —
the way a 19-count with a six-card side suit says "this is not a 3NT hand".

```yaml
# ADDED to the existing context responder_rebid_after_1NT_rebid
# (expand: { m: [C, D], M: [H, S] }; $om is the other minor, so the jump is
#  always below three of responder's major)
      - id: rr_nt_jump_$om
        call: 3$om
        priority: 55
        requires:
          suits: { $om: [5, 13] }
          hcp: [13, 21]
          not: { suits: { $M: [5, 13] } }
        shows: "jump in the unbid minor: 5+ $om, game forcing - a second suit too good for 3NT"
        establishes: { forcing: game_forcing }
```

**THE ANSWERING SEAT** (ships with it — the jump is a game force and the seat
did not exist):

```yaml
  - id: opener_over_1NT_rebid_minor_jump
    description: "Opener answers responder's game-forcing 3om jump over the 1NT rebid"
    expand: { m: [C, D], M: [H, S] }
    pattern: "1$m - P - 1$M - P - 1NT - P - 3$om - P - ?"
    rules:
      - id: o1ntj_3NT_$om
        call: 3NT
        priority: 50
        requires: {}
        shows: "placing the game opposite the forcing jump"
        establishes: { forcing: sign_off }
      - id: o1ntj_raise_$om
        call: 4$om
        priority: 54
        requires:
          suits: { $om: [4, 13] }
          evals: { weakest_unshown_stopper: [0, 0.6] }
        shows: "four-card support and a suit wide open: no notrump"
        establishes: { forcing: game_forcing, agreed_suit: $om }
```

**What it endangers.**
* `uc_new_D2` / `uc_new_D2_hi` (2D, fit 1.000 today): not the same call, but the
  new rung takes the hand off them — three of a new suit opposite a limited
  rebid is a force, and 2D on a 19-count is an underbid partner can pass.
* `rr_nt_3NT` (3NT, 13-18, prio 54): my rung is one point higher and denies a
  five-card major.  A 6-4 hand with a void belongs in a suit auction, not in a
  blind 3NT — that is exactly the hand this board lost.
* `rr_nt_slam3_$M` (prio 56) and `rr_nt_4NT` (55, quantitative with
  `semi_balanced`) both keep their full bands; neither can fit a 6-4-3-0.
* In the answering context, `o1ntj_3NT_$om` carries `requires: {}` so opener can
  never be starved (round 6's `rkc5H_signoff` lesson).  I deliberately dropped
  a "3M with three-card support" rung after tracing it: opener's 1NT rebid has
  already denied four-card support, so the raise can only ever build a 4-3 fit,
  and on this board it took the auction away from a cold 3NT.

**VERIFIED.**  `1C-P-1S-P-1NT-P` → `rr_nt_jump_D` 3D at fit 1.000, prio 55;
opener's `KT8.T4.KQ6.KJ872` → `o1ntj_3NT_D` 3NT at fit 1.000.  3NT makes twelve
(+690 our way) instead of 3D+4 (+190).

**TEMPLATE.**  Already templated: the rung rides the context's existing
`expand: { m: [C, D], M: [H, S] }` (four rules), and the answering context uses
the same expansion (four contexts, eight rules).

---

## Board 837 — NOTHING-WRONG (competitive)

Both tables diverge over an opposing bid — N over `1D - 1NT - 3D` at table A,
W over `1D - 1NT` at table B.  Checked `ch_pass` (fit 1.000) against
`ch_free_3H` (0.800) on `J9763.KJT864..J2`: that is a competitive free-bid
judgment on a 6-HCP two-suiter and it is the other reviewer's call.

**Constructive observation.** Nothing in my discipline occurs on this board:
our side never gets two uncontested calls in a row.

---

## Board 856 — NOTHING-WRONG (competitive from call 3)

Our first two calls (`open_1C` on `AKQ9.QT.T6.A9832`, `r1C_1D` on
`J3..AQJ975.KQT75`) are both correct and both fit 1.000; W's 3H preempt then
owns the auction.  Everything after that — N's pass over 3H, S's 4D, the 4NT
and the 5D sign-off — happens under interference.

**Constructive observation, and it is the round-17 point in miniature.** The
hand that was lost is a 6-5 minor two-suiter with a void opposite a 15-count
with five clubs: 6C and 6D are both cold and we played 5D.  The reason is not
`rkc5C_signoff_D` — with two keycards missing the sign-off is *correct* — it is
that no call anywhere below game ever said "six diamonds, five clubs, no
hearts".  `resp_1m` has **no splinter and no jump shift** (compare
`resp_1H_splinters` / `resp_1S_splinters`, 18 rules between them), so a minor
opening cannot start a shape-showing auction at all.  That is a subject to
author, not a rung to add here.

---

## Board 866 — PROPOSAL — a shape-showing slam invitation opposite opener's jump shift

**Seat/call that went wrong.** Table A, call 6, **N** after `1D - P - 1H - P -
3C - P`, holding `KJ52.J8542..AK82` (12 HCP, 4-5-0-4) opposite a shown 18-21.
`rjs_3NT_H` — the context's own catch-all — signed off in 3NT with 6NT cold.

**The missing agreement.** Opposite the 18-21 jump shift, four-card support for
opener's second suit plus a side void is worth a slam invitation even though
the hand is not balanced — the shape rung that `responder_after_major_jump_shift`
already has (`rmjs_3S_$m`) and `responder_after_jump_shift` never got.

```yaml
# ADDED to the existing context responder_after_jump_shift
# (expand: { M: [H, S] }, pattern "1D - P - 1$M - P - 3C - P - ?"),
# inserted directly ABOVE rjs_3NT_$M so the catch-all keeps its full band
      - id: rjs_4NT_fit_$M
        call: 4NT
        priority: 57.5
        requires:
          hcp: [11, 14]
          suits: { C: [4, 13] }
          evals: { controls: [3, 12], singleton_or_void: [1, 2] }
        shows: "four-card club support and a side shortage: a slam invitation opposite 18-21 even though the hand is not balanced"
        establishes: { forcing: non_forcing }
        alertable: true
```

**THE ANSWERING SEAT — already authored, and that is why this rung is cheap.**
`jump_shift_quant_accept` (`1D - P - 1$M - P - 3C - P - 4NT - P - ?`) answers
it: `rjsq_accept_$M` bids 6NT on 20-21, `rjsq_decline_$M` passes on 18-19.  No
new context is needed anywhere in this proposal.

**What it endangers.**
* `rjs_4NT_$M` (the balanced quantitative, 12-13 + `semi_balanced`, prio 58)
  stays above mine, so the balanced reading remains primary wherever both fit.
* `rjs_6NT_$M` (prio 60, 14+ semi-balanced) is untouched — verified: a
  `KQ52.KJ52.Q4.AK8` still bids 6NT.
* `rjs_3NT_$M` (prio 55, `hcp: [6, 21]`, no shape gate) keeps its full band
  underneath, so a hand that misses my gates still has a bid — verified on a
  7-count with the same void, which still bids 3NT.
* `gf_new_3S` (prio 36) and `uc_raise_C4` are far below and unaffected.

**VERIFIED.**  N → `rjs_4NT_fit_H` 4NT at fit 1.000, prio 57.5; S
(`AT.AK.AKQ97.T763`, 20 HCP) → `rjsq_accept_H` 6NT at fit 1.000.  +990 instead
of +490.

**TEMPLATE.**  Rides the context's `expand: { M: [H, S] }`.  It should ALSO be
mirrored into `responder_after_major_jump_shift` (`1H - P - 1S - P - 3$m`) with
`$m` substituted for the club suit — that is the sibling this file keeps
half-writing, and the lint's `sibling` check should be pointed at the pair.

---

## Board 909 — PROPOSAL — the seat that answers opener's invitational 3m jump

**Seat/call that went wrong.** Table B, call 8, **E** after `P - P - 1D - P -
1NT - P - 3D - P`, holding `A96.K32.Q98.JT95` (10 HCP, every unshown suit
stopped).  `or1mn_jump_$m` had just made an **invitational** bid — "6+ $m,
16-19" — and the seat that answers it does not exist, so E passed at `uc_pass`
fit 1.000 with 3NT cold.  The candidate list contains nothing above fit 0.134.

**The missing agreement.** Opposite opener's invitational 3m jump rebid,
responder bids 3NT with eight or more and the unshown suits held, five of the
minor with support but a suit wide open, and otherwise passes.

```yaml
  - id: responder_over_1m_jump_rebid
    description: "Responder answers opener's invitational 3m jump after 1m - 1NT"
    expand: { m: [C, D] }
    pattern: "1$m - P - 1NT - P - 3$m - P - ?"
    rules:
      - id: r1mj_pass_$m
        call: P
        priority: 50
        requires: {}
        shows: "declining the invitation: a minimum 1NT response"
        establishes: { forcing: sign_off }
      - id: r1mj_3NT_$m
        call: 3NT
        priority: 56
        requires:
          hcp: [8, 11]
          evals: { weakest_unshown_stopper: [0.9, 1] }
        shows: "accepting: 8+ with every unshown suit stopped opposite the 16-19 six-card minor"
        establishes: { forcing: sign_off }
      - id: r1mj_5$m
        call: 5$m
        priority: 54
        requires:
          hcp: [8, 11]
          suits: { $m: [3, 13] }
          evals: { weakest_unshown_stopper: [0, 0.6] }
        shows: "accepting in the minor: 8+ with support but a suit wide open for notrump"
        establishes: { forcing: sign_off, agreed_suit: $m }
```

**THE ANSWERING SEAT.** This *is* the answering seat — it is the reply to
`or1mn_jump_$m`, which has been forcing nothing and getting nothing since it was
written.  The sign-off carries `requires: {}` so the seat can never be starved,
and none of the three rungs is forcing, so nothing further is owed.

**What it endangers.**  The context is new and the seat previously held no rule
at all, so nothing is outranked.  It does delete the code fallback for P, 3NT
and 5m in this seat — priced: my pass is `requires: {}` at fit 1.000, i.e. an
exact superset of the fallback pass it replaces, and the other two calls had no
fallback candidate above fit 0.134.

**VERIFIED.**  E → `r1mj_3NT_D` 3NT at fit 1.000.  Controls: a 6-count still
passes (fit 1.000 on the pass, 0.009 on 3NT); a 9-count with hearts wide open
bids 5D.  3NT makes thirteen (-190 becomes +600 our way at this table).

**TEMPLATE.**  `expand: { m: [C, D] }` as written (2 contexts, 6 rules).  The
same seat is owed to `or1mn_2NT_$m` (18-19 balanced, invitational): the twin
context `1$m - P - 1NT - P - 2NT - P - ?` is missing too, while its major
counterpart `responder_over_2NT_rebid` exists.  Ship both.

---

## Board 953 — PROPOSAL — `resp_1M_over_2x` is missing its sixth combination, `1H - (2S)`

**Seat/call that went wrong.** Table A, call 3, **N** after `P - 1H - 2S`,
holding `QJ976.T642.AK6.6` — a 10-count with four trumps and two outside
controls, i.e. a textbook limit raise or better.  The engine bid **4H** via
`cl_raise_H4`, whose own `shows` is "11+ support points, a real trump fit, and
the values".  S read that as a game raise with values, asked for keycards
(`gr_rkc_H`) and played **6H off one**.

**The root cause, verified.** `resp_1M_over_2x` templates only over overcalls in
a *lower* suit — `{H,C} {H,D} {S,C} {S,D} {S,H}` — so `1H - (2S)` has **no
context at all**.  `context_at` returns `['general_competitive_low',
'general_slam_try']`: no single raise, no cue-bid raise, no negative double, no
Law raise.  The one auction in the family the template cannot express is also
one of the commonest in bridge.

**The missing agreement.** After `1H - (2S)`, 3H is the single raise, 3S is the
cue-bid raise showing a limit raise or better, and 4H is the Law raise on five
trumps — exactly what `resp_1M_over_2x` says in the other five combinations.

```yaml
  - id: resp_1H_over_2S
    description: "Responder after 1H - (2S): the sixth combination resp_1M_over_2x cannot template"
    pattern: "1H - 2S - ?"
    rules:
      - id: r1H2S_raise
        call: 3H
        priority: 70
        requires: { suits: { H: [3, 13] }, evals: { total_points: [6, 9] } }
        shows: "single raise in competition (the two level is gone)"
        establishes: { forcing: non_forcing, agreed_suit: H }
      - id: r1H2S_lott4
        call: 4H
        priority: 72
        requires:
          suits: { H: [5, 13] }
          evals: { "lott_total_trumps(H)": [10, 26], total_points: [6, 10] }
        shows: "the Law at the four level: five-plus trumps opposite the opening, ten trumps between us"
        establishes: { forcing: sign_off, agreed_suit: H }
      - id: r1H2S_cue
        call: 3S
        priority: 74
        requires: { suits: { H: [3, 13] }, evals: { total_points: [10, 40] } }
        shows: "cue-bid raise: limit raise or better in hearts"
        establishes: { forcing: one_round, agreed_suit: H }
        alertable: true
        convention: cue_raise
      - id: r1H2S_2NT
        call: 2NT
        priority: 55
        requires: { hcp: [10, 12], features: [ "stopper(S)" ], not: { suits: { H: [3, 13] } } }
        shows: "10-12 with a spade stopper"
        establishes: { forcing: invitational }
      - id: r1H2S_3NT
        call: 3NT
        priority: 56
        requires: { hcp: [13, 16], features: [ "stopper(S)" ], not: { suits: { H: [3, 13] } } }
        shows: "13-16 with a spade stopper"
        establishes: { forcing: sign_off }
      - id: r1H2S_pass
        call: P
        priority: 20
        requires: { hcp: [0, 8] }
        shows: "nothing to say"
        establishes: { forcing: non_forcing }
        negative_inference_weight: soft
```

**THE ANSWERING SEAT** (the cue is `forcing: one_round`, so it ships with its
reply):

```yaml
  - id: opener_over_cue_raise_1H2S
    description: "Opener answers responder's cue-bid raise after 1H - (2S) - 3S"
    pattern: "1H - 2S - 3S - P - ?"
    rules:
      - id: ocr1h_game
        call: 4H
        priority: 55
        requires: {}
        shows: "the game opposite a limit raise or better"
        establishes: { forcing: sign_off, agreed_suit: H }
      - id: ocr1h_sign
        call: 3H
        priority: 56
        requires: { evals: { total_points: [12, 13] } }
        shows: "a dead minimum: stopping below game"
        establishes: { forcing: sign_off, agreed_suit: H }
      - id: ocr1h_rkc
        call: 4NT
        priority: 60
        requires: { evals: { controls: [7, 12], ltc: [0, 4] } }
        shows: "seven controls and four losers opposite a limit raise or better: keycard ask"
        establishes: { asking: keycards, agreed_suit: H }
```

**What it endangers.**  The pattern is anchored (`1H - 2S - ?`, specificity
1003) so it takes 3H, 4H, 3S, 2NT, 3NT and P away from `general_competitive_low`.
Priced rung by rung, and this is the whole reason to copy `resp_1M_over_2x`
verbatim rather than invent:
* `cl_raise_H3` / `cl_raise_lott3_H` (3H, prio 31/32) — replaced by
  `r1H2S_raise`, whose band 6-9 support points is the same competitive raise with
  a tighter `shows`.
* `cl_raise_H4` / `cl_raise_lott4_H` (4H, prio 32) — replaced by `r1H2S_lott4`,
  which says *Law*, not *values*.  This is the fix: opener must be able to tell
  a ten-trump preempt from a game raise, and today one rung does both jobs.
* `cl_pass` (P, prio 20) — `r1H2S_pass` is the identical 0-8 pass at the same
  priority, copied from `r1M2x_pass`.
* `cl_nt2` / `cl_nt3` — replaced by the `stopper(S)`-gated pair, which is
  strictly *narrower*; that is the one place this proposal subtracts, and it
  subtracts exactly the notrump bids made without a stopper in their suit.
* `cl_negative_X2` (X) is NOT defined by the new context, so it survives
  unchanged — deliberate, because over a spade overcall of 1H there is no other
  major to show and the double is penalty-flavoured.

**VERIFIED.**  N → `r1H2S_cue` 3S at fit 1.000, prio 74; S
(`.AKQJ9.T2.AT9843`, 5 controls) → `ocr1h_game` 4H at fit 1.000, the RKC rung
correctly at 0.057.  4H makes eleven (+450), matching the other table: the board
turns from -11 into a push.  A 7-count still raises to 3H.

**TEMPLATE.**  No expansion — this IS the one combination that cannot be
templated.  It should be filed immediately after `resp_1M_over_2x` so the two
read as one family, and the lint's sibling check should be taught that the pair
is now complete.

---

## Board 957 — NOTHING-WRONG (competitive)

The first divergence at table A is S's 3S over `P P 1H 1S P 2H X 2S P` — an
advance of our own overcall after their double.  Fully competitive.

**Constructive observation, offered for the other reviewer.** At table B our E
made a negative double of the 1S overcall on `QJ952.7.AT854.T6`: `r1H1S_X`
requires "both minors or a long minor, no heart fit" and fits, but the hand
contains **five spades — their suit** — and a penalty pass is the bid.  I did
not propose the gate: `DECISIONS.md` records that "a takeout double must not
hide a six-card suit" was measured with whole-corpus data in round 7 and killed
(doubles WITH a 6+ suit average -2.00/table, WITHOUT -2.54), and a
length-in-their-suit gate is the same species.

---
