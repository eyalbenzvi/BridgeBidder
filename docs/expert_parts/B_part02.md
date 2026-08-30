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
added to existing contexts — and:

* all **30** seat checks (the trying seat AND the answering seat of each) still
  produce the intended call, so there is no cross-interference between them;
* the batch parses (`load_system` on the patched file, 0 duplicate ids);
* **`python3 -m pytest -q` against the patched system: 768 passed, 0 failed.**
  An earlier draft of the trial bid broke exactly one locked scenario
  (`rebids::opener_game_try_after_single_raise`) and that failure is reported in
  full under board 90 together with the narrowing that fixes it — round 14's
  lesson, taken literally: a locked scenario is a measurement.

Where a rung is placed above an existing one I list what it can outrank and why
mine is the better description of the hand.

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

## Board 12 — PROPOSAL — advancing partner's balancing 2NT over their weak two

**Seat/call that went wrong.** Table B, call 5, **E** after `2D - P - P - 2NT -
P`, holding `K86532.J9864.T.J` — 5 HCP, six spades and five hearts.  The engine
bid **3NT** via `uc_nt_raise3` (down three) because
`advance_2NT_over_weak_two` is patterned `2$X - 2NT - P - ?` — the DIRECT 2NT
only — and the balancing sequence `2$X - P - P - 2NT - P - ?` has no context at
all.  `context_at` returns `['general_uncontested_continuation']`.

**The missing agreement.** Opposite partner's balancing notrump over their weak
two, a five-card major is shown at the three level before notrump is considered,
and 3NT needs eight.

```yaml
  - id: advance_balancing_2NT_over_weak_two
    description: "Advancing partner's balancing 2NT over their weak two"
    expand: { X: [D, H, S] }
    pattern: "2$X - P - P - 2NT - P - ?"
    rules:
      - id: a2nb_pass_$X
        call: P
        priority: 20
        requires: {}
        shows: "not enough for game opposite the balancing 2NT"
        establishes: { forcing: sign_off }
        negative_inference_weight: soft
      - id: a2nb_3NT_$X
        call: 3NT
        priority: 55
        requires: { hcp: [8, 40], not: { any_of: [ { suits: { H: [5, 13] } }, { suits: { S: [5, 13] } } ] } }
        shows: "game opposite the balancing notrump, no five-card major"
        establishes: { forcing: sign_off }
      - id: a2nb_3H_$X
        call: 3H
        priority: 56
        when: { unbid_suit: H }
        requires: { suits: { H: [5, 13] }, evals: { "suit_diff(H,S)": [0, 13] } }
        shows: "five-plus hearts: showing the major before notrump"
        establishes: { forcing: one_round }
      - id: a2nb_3S_$X
        call: 3S
        priority: 56.5
        when: { unbid_suit: S }
        requires: { suits: { S: [5, 13] }, evals: { "suit_diff(S,H)": [1, 13] } }
        shows: "five-plus spades: showing the major before notrump"
        establishes: { forcing: one_round }
```

**THE ANSWERING SEAT.** 3H and 3S are `forcing: one_round`, and the seat that
answers them ALREADY EXISTS: `nt2_stayman_placement` does not reach here, but
`weak2_ask_continuation` does not either — what does is the generic notrump
opener's ladder plus, more precisely, the same reply structure the direct-2NT
advance uses.  I traced it: after `2D - P - P - 2NT - P - 3S - P - ?` the
balancer's candidates come from `general_uncontested_continuation` with
`uc_raise_S3`/`uc_raise_S4` fitting on three-card support, which is a real
answer but a thin one.  **If this ships, ship it with a matching
`balancer_over_major_advance` context** (`2$X - P - P - 2NT - P - 3(H|S) - P -
?`: raise to game with three-card support, 3NT with a doubleton) — I have not
authored that here because it belongs to the same subject and one board should
not carry two contexts it did not need.  The 3S bid on this board is passed by
nobody: partner is 19-21 and will act.  Mark that as the one loose end in this
proposal.

**What it endangers.**
* `uc_nt_raise3` (3NT, prio 26.5) — the round-14 rung that was re-ranked to
  26.5 precisely so it would stop outranking natural suit bids.  Here it is
  still raising a natural 2NT to game on **five HCP**; `a2nb_3NT_$X` replaces it
  with an 8-point floor.  Strictly a subtraction of bad 3NTs.
* `uc_pass` (P, prio 18) — replaced by an identical `requires: {}` pass at 20,
  soft negative inference, so nothing is starved.
* `uc_new_H3` / `uc_new_S3` (5+ cards, 14+ points) — my rungs are broader (any
  strength with a five-card major opposite a 19-21 balance), which is right:
  opposite a balancing 2NT the major is shown, not suppressed.

**VERIFIED.**  E → `a2nb_3S_D` 3S at fit 1.000 (the six-card spade suit
outranks the five-card heart suit through `suit_diff`, matching the system's own
"higher of unequal length" rule).  3S makes nine; 3NT went down three.

**TEMPLATE.**  `expand: { X: [D, H, S] }` as written (3 contexts, 12 rules).
The same twin is owed to every direct-seat advance context whose balancing
sibling is missing; `advance_2NT_over_weak_two` is the one this board proves.

---

## Board 90 — PROPOSAL — the file's first help-suit trial bid, with the seat that answers it

**Seat/call that went wrong.** Table A, call 6, **N** after `P - P - 1H - 1NT -
2H - P`, holding `KT53.AQJT9.AQ2.6` — 16 HCP, five hearts, four spades, a
singleton club.  The engine bid **4H** via `uc_raise_H4` and went down one with
partner holding `A84.765.3.JT9754`: five HCP and a wasted club length opposite
the singleton.

**The missing agreement — and it is the round-17 headline.**  Opposite a single
raise, three of a side suit is a **help-suit game try**, so a shapely
sixteen-to-nineteen asks instead of guessing.  `trial / help-suit game try` is at
**zero rules** in the file today; `responder_rebid_after_1M_raise` gives opener
exactly three choices (pass 12-16, a blunt 3M on 17-18, 4M on 19-24) and no way
to ask a question.

```yaml
  - id: help_suit_game_try
    description: "Opener's help-suit trial bid after 1M - 2M"
    expand_pairs:
      - { M: H, x: C }
      - { M: H, x: D }
      - { M: S, x: C }
      - { M: S, x: D }
      - { M: S, x: H }
    pattern: "1$M - P - 2$M - P - ?"
    also_patterns: [ "1$M - act - 2$M - P - ?" ]
    rules:
      - id: hst_try_$M$x
        call: 3$x
        priority: 55
        requires:
          suits: { $M: [5, 5], $x: [3, 4] }
          evals: { total_points: [16, 19], singleton_or_void: [1, 2] }
        shows: "help-suit game try: 16-19 with exactly five $M, a side shortage and three or four $x - asking for help in $x (with six of the major the blunt 3$M try is enough)"
        establishes: { forcing: invitational, agreed_suit: $M }
        alertable: true
```

**THE ANSWERING SEAT** — the try is an invitation and is worthless without it:

```yaml
  - id: responder_over_help_suit_try
    description: "Responder answers opener's help-suit trial bid"
    expand_pairs:
      - { M: H, x: C }
      - { M: H, x: D }
      - { M: S, x: C }
      - { M: S, x: D }
      - { M: S, x: H }
    pattern: "1$M - P - 2$M - P - 3$x - P - ?"
    also_patterns: [ "1$M - act - 2$M - P - 3$x - P - ?" ]
    rules:
      - id: hsta_decline_$M$x
        call: 3$M
        priority: 50
        requires: {}
        shows: "declining the trial bid: no help in $x"
        establishes: { forcing: sign_off, agreed_suit: $M }
      - id: hsta_accept_$M$x
        call: 4$M
        priority: 55
        requires:
          any_of:
            - all_of:
                - suits: { $x: [3, 13] }
                - evals: { total_points: [7, 40] }
            - all_of:
                - suits: { $x: [2, 13] }
                - evals: { total_points: [9, 40] }
        shows: "accepting: three or more $x (real help), or a maximum raise without it"
        establishes: { forcing: sign_off, agreed_suit: $M }
```

`expand_pairs` deliberately lists only try suits BELOW the trump suit, so the
decline (3M) is always available — a 3S try over 1H would make the sign-off 4H,
i.e. the game the try was avoiding.

**What it endangers.**  This is the one proposal in the slice that outranks a
sign-off, so it is priced in full.
* `op_after_raise_game` (4M, prio 54, 19-24 total points) — at 19 both fit and
  mine wins.  **The bridge:** with 5-4-3-1 and nineteen *support* points opposite
  a 6-9 raise the extra values are distributional, game is not cold, and the
  standard action is a trial bid — a minimum raise then stops in three.  With no
  shortage, `singleton_or_void: [1, 2]` (sharp, σ²=0.05) vetoes hard and the
  game bid is untouched: verified on a balanced 19, which still bids 4H.
* `op_after_raise_inv` (3M, prio 52, 17-18) — mine outranks it, and a named
  suit is strictly more informative than a blunt raise.
* **`uc_new_$x3` (three of a new suit, "5+ cards, 14+ points") is NOT
  endangered**: my rung requires exactly three or four cards in the try suit, so
  the two rules cannot both fit the same hand.  That is deliberate — it removes
  the shadowing hazard entirely.
* `uc_raise_H3` / `uc_raise_H4` / `uc_pass` in the competitive twin: outranked
  at 55, and a 16-19 shapely hand opposite a raise is better described by a
  question than by a jump to game.
* **A locked scenario found the boundary and I moved to preserve it.**  With
  `suits: { $M: [5, 13] }` the rung took
  `rebids::opener_game_try_after_single_raise` (`AQJ752.A64.K42.9`, expecting
  3S) and bid 3D instead.  Gating the trump suit to exactly five restores it:
  with a six-card major you hold your own source of tricks and 3M is a
  sufficient try.  **767 passed / 1 failed before the narrowing; the narrowing
  is in the YAML above.**

**VERIFIED.**  N → `hst_try_HD` 3D at fit 1.000 (both the competitive seat on
this board and the uncontested twin).  Answering seat: a singleton diamond
declines (3H, fit 1.000 vs 0.279), `Q83` accepts (4H, fit 1.000), a void with
nine points declines.  On the board the auction becomes 1H (1NT) 2H - 3D - 3H:
+140 instead of -50.

**TEMPLATE.**  `expand_pairs` over the five (major, lower side suit) pairs —
exactly the set `opener_over_second_suit_raise` already uses — times the two
patterns, i.e. **5 contexts × 1 rule + 5 contexts × 2 rules across two auction
shapes**.  The natural extension, which I did NOT author here, is the
short-suit try (3 of a singleton) as a second family; it wants its own subject
and its own screen.

---

## Board 94 — PROPOSAL — responder's rebid after opener answers the negative double with 1NT

**Seat/call that went wrong.** Table B, call 7, **E** after `P - 1C - 1S - X -
P - 1NT - P`, holding `9.AKT6.6432.AK75` (14 HCP).  Opener has just shown 12-14
balanced with the spades stopped; 26+ combined is a game.  The engine bid **2C**
via `uc_doubler_raise_C`.  `context_at` returns
`['general_uncontested_continuation']` — the seat has no context.

**The missing agreement.** Opposite opener's 12-14 notrump reply to a negative
double, responder invites with 11-12 and bids game with 13+ — the plain
invitational ladder that every other 1NT rebid in the file already has.

```yaml
  - id: responder_over_1NT_after_negative_double
    description: "Responder's rebid after opener answers the negative double with 1NT"
    expand_pairs:
      - { m: C, M: H, oM: S }
      - { m: D, M: H, oM: S }
      - { m: C, M: S, oM: H }
      - { m: D, M: S, oM: H }
    pattern: "1$m - 1$M - X - P - 1NT - P - ?"
    rules:
      - id: rnx1nt_pass_$m$M
        call: P
        priority: 50
        requires: {}
        shows: "8-10: the 12-14 notrump is high enough"
        establishes: { forcing: sign_off }
      - id: rnx1nt_2NT_$m$M
        call: 2NT
        priority: 54
        requires: { hcp: [11, 12] }
        shows: "invitational: 11-12 opposite the 12-14 notrump"
        establishes: { forcing: invitational }
      - id: rnx1nt_3NT_$m$M
        call: 3NT
        priority: 55
        requires: { hcp: [13, 17] }
        shows: "game: 13+ opposite the 12-14 notrump"
        establishes: { forcing: sign_off }
      - id: rnx1nt_3$m
        call: 3$m
        priority: 53
        requires: { suits: { $m: [5, 13] }, hcp: [11, 40], evals: { weakest_their_stopper: [0, 0.6] } }
        shows: "five-card support for opener's minor with their suit unstopped: inviting in the minor"
        establishes: { forcing: invitational, agreed_suit: $m }
```

**THE ANSWERING SEAT.** The 2NT rung is an invitation and it is answered by an
already-existing family only in the uncontested shapes, so **ship it with**
`opener_over_negdouble_2NT` (`1$m - 1$M - X - P - 1NT - P - 2NT - P - ?`:
pass 12-13, 3NT 14 with their suit still stopped) — a two-rung mirror of
`opener_over_pref_2NT`, which is the file's own precedent.  On this board the
3NT rung is what fires and no reply is owed.

**What it endangers.**  New context, previously no rules.
* `uc_doubler_raise_C` (2C, prio 34) — not defined by my context, so it
  survives; it simply stops winning when a descriptive notrump call fits.
* `uc_pass` (P, prio 18) — replaced by a `requires: {}` pass; exact superset.
* `uc_nt2` / `uc_nt3` — replaced by bands tied to the *shown* 12-14, which is
  the whole point: the generic notrump rungs guess at the partnership total,
  and here it is known.
* Note `weakest_their_stopper` is used only on the minor-suit rung and only as a
  soft preference; `ROUND_METHOD.md` records that it has no sharp tolerance, so
  I have NOT leaned any of the notrump rungs on it.

**VERIFIED.**  E → `rnx1nt_3NT_CS` 3NT at fit 1.000, prio 55.  3NT makes nine
(+600 our way) instead of 2H making ten (+170).

**TEMPLATE.**  `expand_pairs` over the four (minor opening, major overcall)
combinations already used by `opener_over_negative_double` — 4 contexts, 16
rules, plus 4 more for the 2NT answer.

---

## Board 133 — NOTHING-WRONG (competitive)

RHO opens a weak 2S; both auctions are competitive from call 0.  Checked
`vw2_X` (fit 1.000) on `53.KT963.AKQJ2.Q` against the two natural 3-level bids
(both also fit 1.000, at priority 26 against the double's 70) — a takeout double
on a 5-5 red two-suiter with 15 is orthodox, and the loss came later when
`ch_pass` had to guess over 4S.

**Constructive observation.** None; our side never has an uncontested
constructive sequence on this board.

---

## Board 174 — PROPOSAL — opener's game try after responder's simple preference

**Seat/call that went wrong.** Table B, call 9, **W** after `P - 1D - P - 1H -
P - 2C - P - 2D - P`, holding `AQ8.Q.QJ632.AQ93` (17 HCP, 3-1-5-4).  The engine
**passed** at `uc_pass` fit 1.000; the next best candidate in the whole seat is
`uc_rebid_D3` at **0.349**.  `1$m - P - 1$M - P - 2$n - P - 2$m - P - ?` — opener's
third call after the preference — has no context, so a seventeen-count with a
two-suiter dies in 2D with 3NT cold.

**The missing agreement.** After responder's simple preference back to the first
suit (6-10), opener with 16-19 invites: 3m with a fifth card in the first suit,
2NT with the unshown suits held.

```yaml
  - id: opener_over_simple_preference
    description: "Opener's game try after responder's simple preference to the first suit"
    expand_pairs:
      - { m: C, n: D, M: H }
      - { m: C, n: D, M: S }
      - { m: C, n: H, M: S }
      - { m: D, n: C, M: H }
      - { m: D, n: C, M: S }
      - { m: D, n: H, M: S }
    pattern: "1$m - P - 1$M - P - 2$n - P - 2$m - P - ?"
    rules:
      - id: oosp_pass_$m$n
        call: P
        priority: 50
        requires: {}
        shows: "minimum two-suiter: the preference is the final contract"
        establishes: { forcing: sign_off }
      - id: oosp_3$m$n
        call: 3$m
        priority: 54
        requires:
          hcp: [16, 19]
          suits: { $m: [5, 13] }
        shows: "extras opposite the 6-10 preference: inviting game with the first suit"
        establishes: { forcing: invitational, agreed_suit: $m }
      - id: oosp_2NT_$m$n
        call: 2NT
        priority: 55
        requires:
          hcp: [16, 18]
          evals: { weakest_unshown_stopper: [0.9, 1], semi_balanced: [1, 1] }
        shows: "16-18 with the unshown suits held: inviting 3NT"
        establishes: { forcing: invitational }
```

**THE ANSWERING SEAT** (the 3m try is an invitation; it ships with its reply):

```yaml
  - id: responder_over_preference_game_try
    description: "Responder answers opener's 3m game try after the preference"
    expand_pairs:
      - { m: C, n: D, M: H }
      - { m: C, n: D, M: S }
      - { m: C, n: H, M: S }
      - { m: D, n: C, M: H }
      - { m: D, n: C, M: S }
      - { m: D, n: H, M: S }
    pattern: "1$m - P - 1$M - P - 2$n - P - 2$m - P - 3$m - P - ?"
    rules:
      - id: ropg_pass_$m$n
        call: P
        priority: 50
        requires: {}
        shows: "declining: a minimum preference"
        establishes: { forcing: sign_off }
      - id: ropg_3NT_$m$n
        call: 3NT
        priority: 56
        requires:
          hcp: [9, 12]
          evals: { weakest_unshown_stopper: [0.9, 1] }
        shows: "accepting with the unshown suits held: 3NT"
        establishes: { forcing: sign_off }
      - id: ropg_5$m$n
        call: 5$m
        priority: 54
        requires:
          hcp: [9, 12]
          suits: { $m: [4, 13] }
          evals: { weakest_unshown_stopper: [0, 0.6] }
        shows: "accepting in the minor: values but a suit wide open"
        establishes: { forcing: sign_off, agreed_suit: $m }
```

**What it endangers.**  Both contexts are new; the seats held no rule at all.
* `uc_pass` (P, prio 18) — replaced by a `requires: {}` pass at 50; exact
  superset, so nothing is starved.
* `uc_rebid_D3` / `uc_raise_D3` (3D, prio 27, best fit 0.349) — my rung is a
  named invitation instead of a soft-miss guess.
* `uc_nt2` / `uc_nt3` — outranked by `oosp_2NT`, which knows partner's range
  (6-10) rather than guessing at the total.
* The `2$n` slot in `expand_pairs` deliberately excludes the case where the
  preference suit ranks above the second suit, so 3m is always a live call.

**VERIFIED.**  W → `oosp_3DC` 3D at fit 1.000; E (`K72.KT62.KT7.JT4`, 10 HCP,
both unshown suits stopped) → `ropg_3NT_DC` 3NT at fit 1.000.  A 13-count in the
same seat still passes (3D at fit 0.134).  3NT makes nine (+600) instead of 2D
making ten (+130).

**TEMPLATE.**  `expand_pairs` over the six (first suit, second suit, response)
combinations that can produce a preference — 6 contexts × 3 rules for the try
and 6 × 3 for the answer, 36 rules from one idea.

---

## Board 175 — PROPOSAL — over a weak two in a MINOR, 3NT must outrank the suit game

**Seat/call that went wrong.** Table B, call 4 is the feature reply; the real
error is call **6, E**, after `2D - P - 2NT - P - 3S - P`, holding
`KJT9.KJ3.KQ5.A84` (17 HCP, both unshown suits stopped).  The engine bid **4D**
via `w2ac_game_D` (prio 56) while `w2ac_3NT_D` sat right underneath at prio 55 —
**both at fit 1.000**.  This is a pure priority defect and it only exists in the
minor: the file's own comment on `w2ac_game8_$W` already says "loosening
`w2ac_game_$W` in place also loosens the MINOR, where nine tricks beat eleven
and 3NT is right", and then the ladder was left with 4D on top anyway.

**The missing agreement.** Opposite a weak two in a minor, with 14+ and every
unshown suit stopped, nine tricks in notrump beat eleven in the suit.

```yaml
# NEW CONTEXT, and it MUST be filed IMMEDIATELY BEFORE weak2_ask_continuation.
# Same specificity (1000 + 7 tokens), so file order decides which context owns
# 3NT; placed first it owns 3NT for the DIAMOND branch only, and every other
# call in the seat still comes from weak2_ask_continuation.
  - id: weak2_ask_continuation_diamond
    description: "The 2NT asker places the contract opposite a weak two in DIAMONDS"
    pattern: "2D - P - 2NT - P - bid - P - ?"
    rules:
      - id: w2acd_3NT
        call: 3NT
        priority: 57
        requires: { hcp: [14, 40], evals: { weakest_unshown_stopper: [0.9, 9] } }
        shows: "nine tricks: opposite a weak two in a MINOR the unshown suits are stopped, so 3NT beats five diamonds"
        establishes: { forcing: sign_off }
```

**THE ANSWERING SEAT.** 3NT is a sign-off; nothing is owed.  Everything else in
the seat — `w2ac_game_D` (4D), `w2ac_game8_D` (4D) and `w2ac_sign_D` (3D, which
carries `requires: {}`) — stays in `weak2_ask_continuation` and still fires.

**What it endangers.**  Exactly one rule, and it is replaced by a superset:
* `w2ac_3NT_D` is shadowed out entirely (verified — it disappears from the
  candidate list).  My rung carries its `requires` **verbatim**
  (`hcp: [14, 40]`, `weakest_unshown_stopper: [0.9, 9]`) and only raises the
  priority, so the shadowing is a strict superset, which is the structural
  discipline `ROUND_METHOD.md` asks for.
* `w2ac_game_D` (4D, prio 56) is outranked at fit 1.000.  **The bridge:** five
  of a minor needs eleven tricks for the same game bonus that nine tricks buy in
  notrump; with the outside suits held there is no reason to take the risk.
* The MAJOR branches are untouched — `w2ac_game_S` still bids 4S at prio 56 over
  `w2ac_3NT_S` at 55.  Verified on a matching spade hand.
* Nothing without a stopper is affected: verified, a hand with `9832` in an
  unshown suit still bids 4D (3NT drops to fit 0.054).

**VERIFIED.**  E → `w2acd_3NT` 3NT at fit 1.000, prio 57.  3NT makes eleven
(+660) instead of 4D making twelve (+170); the board goes from -10 to a push.

**TEMPLATE.**  Deliberately NOT templated over `W`: the whole content of the
agreement is that the minor is different from the majors.  If the file ever
opens a weak 2C, add a second literal context `2C - P - 2NT - P - bid - P - ?`
with the same single rung.

---

## Board 253 — NOTHING-WRONG (competitive)

The seat is N advancing a takeout double of a weak 2H on `T8.83.K62.A76542`.
Every candidate in `advance_weak2_double_H` is a competitive advance; `aw2H_3C`
won at fit 0.800 with `aw2H_2NT` at 0.054, and BEN's 2NT would be a 7-count
lying about a stopper.  The other reviewer's board.

**Constructive observation.** None: partner's double is the first call and the
auction never leaves competition.

---

## Board 255 — NOTHING-WRONG (competitive)

Table A's divergence is S's 3D over `2H - P - 2NT` — a balancing-ish free bid
over their ask.  `cl_new_long3_D_hi` and `cl_pass` both fit 1.000 and the
priority ladder picks the suit; that is a competitive judgment.

**Constructive observation.** The FALLBACK double appears in this candidate list
at fit 0.409 ("takeout-flavoured cooperative double (undiscussed)") — a reminder
that the code fallback is still competing with authored rungs at three-level
decisions.  Not a constructive-discipline finding.

---

## Board 269 — NOTHING-WRONG (competitive)

Table A: N over `P - 1D - 2C` on `A9743.AQ6.AT74.5`.  A free bid of 2S over
their two-level overcall (`cl_new_S2_hi`, fit 0.757) against `cl_pass` at 1.000
is the competitive reviewer's call.  Table B is a competitive rebid.

**Constructive observation.** None available: our side's second call comes under
an overcall at both tables.

---

## Board 396 — NOTHING-WRONG (competitive)

`nx3_raise` (3S, "competitive raise", fit 1.000) over their preemptive 3H jump
overcall, then a passed-out 3S.  Wholly competitive.

**Constructive observation.** The `neg_double_3level_M` family it lives in has a
`nx3_cue` slam-try rung at priority 71 that no hand on this board can reach; the
contested three-level ladder is thin in the same way the constructive ones are,
but there is no uncontested seat here for me to fix.

---

## Board 400 — PROPOSAL — the quantitative rung above `oc2nresp_3NT`

**Seat/call that went wrong.** Table A, call 4, **N** after `1C - 2D - 2NT - P`,
holding `K973.AK98.K.AKJ5` — **21 HCP** opposite a natural, invitational 2NT
showing 11-12 with the diamonds stopped.  That is 32-33 combined.  The engine
bid **3NT** via `oc2nresp_3NT_$m`, whose band is `hcp: [13, 21]` — a textbook
CEILING, the species rounds 6 and 7 kept finding: the top rung of the ladder is
also the sign-off, so a 21-count and a 13-count make the same call.  6NT is cold
for thirteen tricks.

**The missing agreement.** Opposite the 11-12 competitive 2NT, nineteen to
twenty-one is 30-33 combined and 4NT is quantitative, not a sign-off.

```yaml
# ADDED to the existing context opener_over_competitive_2NT
# (expand: { m: [C, D] }, pattern "1$m - bid - 2NT - P - ?"),
# inserted between oc2nresp_3NT_$m (56) and oc2nresp_pass_$m (55)
      - id: oc2nresp_4NT_$m
        call: 4NT
        priority: 57
        requires: { hcp: [19, 21], evals: { controls: [6, 12] }, not: { evals: { void: [1, 4] } } }
        shows: "quantitative: 19-21 opposite the 11-12 invite is 30-33 combined, so slam is live"
        establishes: { forcing: non_forcing }
        alertable: true
```

**THE ANSWERING SEAT** (a quantitative 4NT with no answering seat is the exact
failure round 17 priced at -9.8 IMPs):

```yaml
  - id: responder_over_competitive_quant
    description: "Responder answers opener's quantitative 4NT over the competitive 2NT"
    expand: { m: [C, D] }
    pattern: "1$m - bid - 2NT - P - 4NT - P - ?"
    rules:
      - id: oc2nq_decline_$m
        call: P
        priority: 50
        requires: {}
        shows: "a minimum 11: declining the slam invitation"
        establishes: { forcing: sign_off }
      - id: oc2nq_accept_$m
        call: 6NT
        priority: 55
        requires:
          any_of:
            - hcp: [12, 12]
            - all_of:
                - hcp: [11, 12]
                - any_of:
                    - suits: { H: [5, 13] }
                    - suits: { S: [5, 13] }
                    - suits: { C: [5, 13] }
                    - suits: { D: [5, 13] }
        shows: "a maximum, or eleven with a five-card suit: accepting"
        establishes: { forcing: sign_off }
```

**What it endangers.**
* `oc2nresp_3NT_$m` (3NT, prio 56, 13-21) keeps its **full band** underneath, so
  a hand that misses my gates still bids game — verified on a 15-count and on a
  19-count with only four controls, both of which still bid 3NT.  This is the
  "add above the ceiling, never narrow the ceiling" pattern that `onx_jump_$m$M`
  already uses in this file.
* `oc2nresp_pass_$m` (P, 0-12) is untouched.
* **A note on the gate I removed during verification, because it is a live trap:**
  the first draft used `evals: { semi_balanced: [1, 1] }` and the rung scored
  **fit 0.000** on a 4-4-1-4 hand — `semi_balanced` has sharp tolerance
  (σ² = 0.08 in `_EVAL_S2`), so it is a veto, not a preference.  `controls` plus
  a void veto does the job without killing the shape.

**VERIFIED.**  N → `oc2nresp_4NT_C` 4NT at fit 1.000, prio 57; S
(`AT5.QJT32.AT2.84`, 11 HCP with a five-card suit) → `oc2nq_accept_C` 6NT at fit
1.000.  6NT makes thirteen (+990) instead of 3NT+4 (+520).

**TEMPLATE.**  Rides the context's `expand: { m: [C, D] }`; the answering
context uses the same.  The same ceiling exists on `dma_3NT_$m$y` (12-21) in
`doubler_over_minor_advance` four contexts below — the identical rung should be
templated there in the same edit.

---

## Board 408 — NOTHING-WRONG (competitive)

Table A's divergence is N's pass over their takeout double of our 1D
(`rdx_pass` fit 1.000 vs `rx_D_1S` 0.800 on a 5-HCP five-card spade suit) — a
competitive-structure question inside `resp_1x_over_X`.

**Constructive observation.** None: the double lands on call 3 at table A and on
call 3 at table B.

---

## Board 482 — NEGATIVE PROTOTYPE, reported rather than shipped

**Seat.** Table A, call 2, **N** after `1NT - P`, holding `K7.J72.AQ82.KQ94`
(15 HCP, 2-3-4-4).  `nt_3NT` fits 1.000 and the engine bid 3NT for +460; 6C is
cold for twelve tricks.

**What I checked, and why I am NOT proposing the obvious rung.** The natural
constructive agreement is a lower quantitative floor — `nt_4NT_quant` is
`hcp: [16, 17]`, so 15 misses it by one — and I prototyped
`nt_4NT_quant_shape` (15 HCP, both minors four-plus, four controls, answering
seat `nt_quant_opener_decides` already present).  **It does not fix the board
and would not have.**  Opener holds `AJ5.KT9.K65.A653` — fifteen, a minimum for
15-17 — so he declines, and 4NT making eleven scores **+460, exactly what 3NT
scored.**  The only route to 6C is a minor-suit slam ask over 1NT, and
`DECISIONS.md` scopes out minor-suit Stayman explicitly.

**Verdict: NOTHING-WRONG at this seat.**  3NT on a flat 15 with one ace opposite
15-17 is normal team bidding; 6C is a double-dummy artefact of a friendly club
break.  Recorded here as the negative result the brief asks for rather than as a
proposal.

**If the scope-out is ever revisited**, the in-scope half of the idea is worth
authoring on its own: `nt_quant_opener_decides` currently answers 4NT only in
notrump, so a 4-4 minor fit found at the 32-count level can never be played in
the minor.  That is a subject, not a rung, and it should be measured as one.

---

## Board 545 — PROPOSAL — opener's rebid after the 1D - 2C game force

**Seat/call that went wrong.** Table B, call 4, **E** after `1D - P - 2C - P`,
holding `64.A87.AKQ986.Q7` — 15 HCP and six good diamonds, opposite a
**game-forcing** 2/1.  The engine bid **2NT** via `uc_nt2`: *"natural 2NT: 11-12
balanced with their suit stopped"*.  The whole seat is a soft-miss lottery — the
best fit among all candidates is **0.134**.  Partner then read 11-12, and the
auction ran 2NT - 3NT - 4NT (quantitative, `qr3_4NT_quant`) - pass, down one.

This is `ROUND_METHOD.md`'s own open item — *"There is no context for opener's
rebid after a 2/1 in a MINOR; `1D - P - 2C - P - ?` is unauthored and the
generic 11-12 `uc_nt2` annexes a game-forcing seat"* — verified on a live board.
`1D - 2C` is the **only** minor-over-minor 2/1 the response ladder can produce
(`r1D_2C_gf` / `r1D_2C_gf3`), so one literal context closes it.

**The missing agreement.** Opposite the 1D - 2C game force, opener shows a
four-card major up the line, six diamonds with 3D on extras and 2D on a
minimum, four-card club support, and 2NT/3NT for the balanced ranges the 1NT
opening does not cover.

```yaml
  - id: opener_rebid_after_1D_2C
    description: "Opener's rebid after the 1D - 2C game force (the only 2/1 in a minor over a minor)"
    pattern: "1D - P - 2C - P - ?"
    rules:
      - id: ob1d2c_floor
        call: 2D
        priority: 45
        requires: {}
        shows: "nothing extra to describe: the cheapest rebid keeps the game force alive"
        establishes: { forcing: game_forcing }
      - id: ob1d2c_2H
        call: 2H
        priority: 57
        requires: { suits: { H: [4, 13] } }
        shows: "4+ hearts (GF continues)"
        establishes: { forcing: game_forcing }
      - id: ob1d2c_2S
        call: 2S
        priority: 56
        requires: { suits: { S: [4, 13] }, not: { suits: { H: [4, 13] } } }
        shows: "4+ spades (GF continues)"
        establishes: { forcing: game_forcing }
      - id: ob1d2c_2D
        call: 2D
        priority: 54
        requires:
          suits: { D: [6, 13] }
          hcp: [12, 16]
          not: { any_of: [ { suits: { H: [4, 13] } }, { suits: { S: [4, 13] } } ] }
        shows: "6+ diamonds, minimum (GF continues)"
        establishes: { forcing: game_forcing }
      - id: ob1d2c_3D
        call: 3D
        priority: 55
        requires:
          suits: { D: [6, 13] }
          hcp: [15, 21]
          features: [ "good_suit(D)" ]
          not: { any_of: [ { suits: { H: [4, 13] } }, { suits: { S: [4, 13] } } ] }
        shows: "6+ good diamonds with extras: setting trumps (GF)"
        establishes: { forcing: game_forcing, agreed_suit: D }
      - id: ob1d2c_3C
        call: 3C
        priority: 53
        requires:
          suits: { C: [4, 13] }
          not: { any_of: [ { suits: { H: [4, 13] } }, { suits: { S: [4, 13] } }, { suits: { D: [6, 13] } } ] }
        shows: "four-card club support: raising the 2/1 (GF)"
        establishes: { forcing: game_forcing, agreed_suit: C }
      - id: ob1d2c_2NT
        call: 2NT
        priority: 52
        requires: { hcp: [12, 14], evals: { semi_balanced: [1, 1] } }
        shows: "12-14 balanced (a 15-17 balanced hand opened 1NT)"
        establishes: { forcing: game_forcing }
      - id: ob1d2c_3NT
        call: 3NT
        priority: 51
        requires: { hcp: [18, 19], evals: { semi_balanced: [1, 1] } }
        shows: "18-19 balanced"
        establishes: { forcing: sign_off }
```

**THE ANSWERING SEAT — already authored, and I checked it rather than assuming.**
Every rung here is game-forcing, and after `1D - P - 2C - P - 3D - P` the
`gf_landing_*` family owns the seat: `gf_minor_3NT` fires at fit 1.000 on
`Q98.KT4.753.AK93`.  The `ob1d2c_floor` rung is the never-starve landing (round
6's lesson) and is priced below every descriptive rung, so it can only win when
nothing else fits — verified on a 4-3-4-2 thirteen-count.

**What it endangers.**  A brand-new anchored context (specificity 1004) that
takes 2D, 2H, 2S, 2NT, 3C, 3D and 3NT away from `general_uncontested_continuation`
and the `gf_landing_*` family at this one seat.
* `uc_nt2` (2NT, "11-12 balanced") — replaced by `ob1d2c_2NT`, which describes
  12-14 balanced opposite a **game force**, the only balanced range this seat can
  hold.  This is a pure subtraction of a lie.
* `uc_rebid_D2` (2D, prio 29, fit 0.100 here) and `uc_raise_C3` — replaced by
  rungs that keep the game force alive instead of sounding like a sign-off.
* `gf_new_2H` / `gf_new_2S` (prio 36) — my 2H/2S rungs are the same natural bid
  at a priority that beats the notrump lottery; they say four-plus rather than
  relying on `unbid_suit`.
* `gf_3NT` (prio 34) — my 3NT is banded 18-19, so a 15-count no longer reaches
  3NT by soft miss.

**VERIFIED.**  E → `ob1d2c_3D` 3D at fit 1.000, prio 55; W → `gf_minor_3NT` 3NT
at fit 1.000.  3NT makes nine (+400) instead of 4NT down (-50): the board swings
about 10 IMPs.

**TEMPLATE.**  None — `1D - 2C` is the only auction of its shape the response
ladder can produce, and templating over `m` would generate `1C - 2D`, which
`resp_1m` never bids.  That is exactly why this hole survived: it is the one
member of a family with no siblings to lint against.

---

## Board 598 — PROPOSAL — 1H - 1NT - 2S, the reverse `opener_rebid_1S_1NT_second_major` never got a twin for

**Seat/call that went wrong.** Table A, call 4, **S** after `1H - P - 1NT - P`,
holding `KQJ6.KQ742.5.AK6` (18 HCP, 4-5-1-3).  The engine bid **2C** via
`ob_1M1NT_2C` — *"3+ clubs, 12-17, no 6-card major"* — **at fit 0.800**, one
point over its own ceiling, because nothing in the seat fits: the best candidate
in the entire context is 0.800.  Partner passed 2C.

`opener_rebid_1S_1NT_second_major` exists and carries `ob_1S1NT_2H` with the
comment *"the 1M - 1NT context is expanded over both majors, so it can offer a
second suit in a minor but never the other major - and 1H - 1NT - 2S would be a
reverse, so only this half of it is a plain second suit."*  The reverse half was
then never written.  **That is the sibling gap**, and the file's own comment
names it.

**The missing agreement.** After 1H - 1NT, 2S is a reverse: five hearts, four or
more spades and 16+, forcing.

```yaml
  - id: opener_rebid_1H_1NT_second_major
    description: "1H - 1NT: 2S is the second suit and a reverse (five hearts, four spades, extras)"
    pattern: "1H - P - 1NT - P - ?"
    rules:
      - id: ob_1H1NT_2S
        call: 2S
        priority: 58
        requires:
          suits: { H: [5, 13], S: [4, 13] }
          hcp: [16, 21]
          not: { suits: { H: [6, 13] } }
        shows: "reverse into the second suit: five hearts, 4+ spades, 16+ - forcing"
        establishes: { forcing: one_round }
```

**THE ANSWERING SEAT** — 2S is `forcing: one_round` and the seat did not exist:

```yaml
  - id: responder_over_1H1NT_2S
    description: "Responder answers opener's 1H - 1NT - 2S reverse"
    pattern: "1H - P - 1NT - P - 2S - P - ?"
    rules:
      - id: r1h2s_2NT
        call: 2NT
        priority: 50
        requires: {}
        shows: "the cheapest call opposite the forcing reverse: 6-10, nothing better to say"
        establishes: { forcing: non_forcing }
      - id: r1h2s_3H
        call: 3H
        priority: 54
        requires: { suits: { H: [3, 13] } }
        shows: "three-card heart preference opposite the 5-4"
        establishes: { forcing: invitational, agreed_suit: H }
      - id: r1h2s_3S
        call: 3S
        priority: 55
        requires: { suits: { S: [4, 13] } }
        shows: "four-card spade support opposite the reverse"
        establishes: { forcing: game_forcing, agreed_suit: S }
      - id: r1h2s_3NT
        call: 3NT
        priority: 56
        requires:
          hcp: [9, 11]
          evals: { weakest_unshown_stopper: [0.9, 1] }
          not: { suits: { H: [3, 13] } }
        shows: "9-11 with both minors held and no heart fit: game opposite the 16+ reverse"
        establishes: { forcing: sign_off }
```

**What it endangers.**
* `ob_1M1NT_2C` (2C, prio 52, capped at 17): the new rung outranks it at 16-17
  where both can fit.  **The bridge:** with 5-4 in the majors and sixteen-plus,
  a reverse shows the shape *and* the extras in one call, while three small
  clubs shows neither; the 12-15 band underneath is untouched.  Verified: a
  13-count 4-5-1-3 still bids 2C at fit 1.000 (the reverse falls to 0.800).
* `ob_1M1NT_3H` (prio 56) and `ob_1M1NT_4H` (57) both require a six-card major;
  `not: { suits: { H: [6, 13] } }` keeps them clear of my rung entirely.
* `uc_new_S2` / `uc_new_S2_hi` (2S, prio 26/26.5, "5+ cards, 10+ points") — the
  new rung takes 2S off them and, unlike them, gets the four-card shape right.
* In the answering context, `r1h2s_2NT` is the `requires: {}` landing, so the
  forcing bid can never be passed out.

**VERIFIED.**  S → `ob_1H1NT_2S` 2S at fit 1.000; N (`987.8.AK986.Q974`, 9 HCP,
both minors held, one heart) → `r1h2s_3NT` 3NT at fit 1.000.  3NT makes nine
(+600) instead of 2C making ten (+130).

**TEMPLATE.**  No expansion — it is the literal twin of
`opener_rebid_1S_1NT_second_major`, and the pair should be filed adjacent so the
sibling lint can see them together.

---

## Board 606 — PROPOSAL — responder's jump showing five-five in the majors

**Seat/call that went wrong.** Table A, call 6, **N** after `1D - P - 1S - P -
2C - P`, holding `KQJT6.A9853.J7.9` — 5-5 in the majors with 11 HCP.  The
engine bid **2D** (`r1d2c_2D`, "preference back to the first suit: 6-10") at fit
0.800 and the auction died in 3D; 4H makes ten.  `responder_after_1D1S_2C` has
seven rungs and not one of them mentions a second suit, and 2H is owned by
`fourth_suit_forcing` (`fsf_2H`, fit 0.435 here), so the 5-5 hand has literally
nothing to bid.

**The missing agreement.** Responder's JUMP into the fourth suit is natural, not
fourth suit forcing: it shows five-five in the majors, invitational or better.

```yaml
# ADDED to the existing context responder_after_1D1S_2C
# (pattern "1D - P - 1S - P - 2C - P - ?"), filed directly above r1d2c_3S
      - id: r1d2c_3H
        call: 3H
        priority: 58
        requires:
          suits: { S: [5, 13], H: [5, 13] }
          hcp: [10, 40]
        shows: "jump in the second suit: five-five in the majors, invitational or better (a jump, so natural - not fourth suit forcing)"
        establishes: { forcing: invitational }
```

**THE ANSWERING SEAT** — an invitation with no reply is worth nothing:

```yaml
  - id: opener_over_55_major_jump
    description: "Opener answers responder's 3H jump showing five-five in the majors"
    pattern: "1D - P - 1S - P - 2C - P - 3H - P - ?"
    rules:
      - id: o55_3S
        call: 3S
        priority: 50
        requires: {}
        shows: "preference to the first major at the cheapest level: no extras"
        establishes: { forcing: non_forcing, agreed_suit: S }
      - id: o55_4H
        call: 4H
        priority: 56
        requires: { suits: { H: [2, 13] }, evals: { total_points: [13, 40] } }
        shows: "accepting the invitation with two-plus hearts"
        establishes: { forcing: sign_off, agreed_suit: H }
      - id: o55_4S
        call: 4S
        priority: 55
        requires: { suits: { S: [3, 13] }, evals: { total_points: [13, 40] } }
        shows: "accepting the invitation with three-plus spades"
        establishes: { forcing: sign_off, agreed_suit: S }
```

**What it endangers.**
* `fsf_2H` (2H, prio 65) is **untouched** — my rung is a jump to 3H, a different
  call, which is precisely why the jump is the right vehicle in a system that
  plays the fourth suit as artificial.
* `r1d2c_3S` (prio 59, "6+ spades, game values") outranks mine and still does;
  a genuine six-card suit is the better description.
* `r1d2c_2D` (prio 54), `r1d2c_2S` (55), `r1d2c_2NT` (56) all keep their bands;
  mine only wins on a hand that is 5-5 with ten-plus, which none of them fits.
* `o55_3S` carries `requires: {}` so the invitation can never be passed out.

**VERIFIED.**  N → `r1d2c_3H` 3H at fit 1.000, prio 58; S
(`.KQ.KQT9852.J843`, KQ doubleton in hearts, 11 HCP and seven diamonds) →
`o55_4H` 4H at fit 1.000.  4H makes ten (+620) instead of 3D+2 (+150).

**TEMPLATE.**  The rung is literal here, but the SAME agreement exists in the
other two-suit auctions the file already has contexts for —
`responder_rebid_1D_1H_2C` (`1D - 1H - 2C`, jump to 2S) and
`responder_after_1S_rebid` (`1m - 1H - 1S`).  Author it as
`expand_pairs` over those three shapes when this ships.

---

## Board 622 — NEGATIVE PROTOTYPE, and NOTHING-WRONG at the seat

**Seat.** Table A, call 6, **N** after `1NT - P - 2H - P - 2S - P`, holding
`KQ753..T83.J9742` — 6 HCP, five spades, five clubs, a heart void.
`tr_pass_weak` fits 1.000 and the engine passed 2S for +170; BEN's 2NT led to a
3NT that made ten.

**Verdict: NOTHING-WRONG.**  Passing 2S with six HCP opposite an accepted
transfer is right at IMPs; the 3NT that made was a bonus from a friendly layout
(N holds a heart void opposite a notrump opener).  `tr_2NT_inv` demands eight,
correctly.

**The agreement that IS missing here, reported as a prototype that does not fire
on this board.**  `ROUND_METHOD.md`'s open item — *"`nt_after_transfer` has no
natural second-suit rung, so a 5-6 hand after a transfer must choose between 3NT
and four of the five-card major"* — is real and this board is its habitat.  The
rung is:

```yaml
# ADDED to nt_after_transfer (expand_pairs [{M:H,T:D},{M:S,T:H}])
      - id: tr_second_$M
        call: 3C
        priority: 57.5
        when: { unbid_suit: C }
        requires:
          suits: { $M: [5, 13], C: [5, 13] }
          hcp: [8, 15]
        shows: "five-five: the second suit, game try - opener picks a game or passes the shape back"
        establishes: { forcing: invitational }
```
with an answering context `1NT - P - 2$T - P - 2$M - P - 3C - P - ?` (4M with
three-card support, 3NT with a club fit and stoppers, 4C with four).  **It does
not fire on board 622** — six HCP is below any invitational floor — so I am
recording it as the agreement the context needs rather than as this board's fix.
Ship it with a board that has the values, or as part of the transfer subject.

---
