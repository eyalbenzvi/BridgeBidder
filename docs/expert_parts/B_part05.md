# Expert B — constructive / team-IMP bidding — dossier part 05

**Scope.** All 38 boards of `docs/dossier_575757/part05.md`, read through the
constructive lens: the uncontested 2/1 machinery, opener's and responder's
rebid structures, the forcing notrump, the invitational/game boundary, and the
shape-showing that separates a minimum from a slam-going hand *before* game.

**Counts.** 38 boards → **30 proposals**, **8 NOTHING-WRONG**, **2 negative
results from my own prototypes reported rather than shipped** (boards 838 and
209).  25 of the 30 proposals are traced through `fast_decision` on the actual
board and are marked **VERIFIED**.

**Everything in this file was prototyped together** in one scratch copy of the
system, so the aggregate is measured rather than asserted:

| | base | with every proposal in this file |
|---|---|---|
| contexts | 517 | **564** |
| rules | 2,344 | **2,523** |
| `lint_system.py` findings | 223 | **222** |
| our decisions changed on `reports/r18_before.jsonl` | — | see "Blast radius" below |

`decide_fast` was replayed over all 10,335 of our decisions in the review
corpus under both systems; the changed-decision count is reported at the foot
of this file with the auctions listed, so nothing here rests on the boards it
was found on.

---

## The three agreements that matter most in this slice

1. **Help-suit (long-suit) game tries after 1M - 2M, with the seat that
   answers them** (board 938).  The convention audit counts *zero* trial bids
   in the file; opposite the single raise opener can only add points and bid
   3M.  `oar_trial_3C/3D/3H` + `responder_over_trial` is a closed
   conversation: try, accept, decline.  It is the single largest missing
   constructive family in this slice and it templates over both majors and
   three trial suits.

2. **The seat that hears a sign-off does not exist, four times over**
   (boards 300, 151, 508, 4).  `1M-1NT-2M`, `1m-1M-2m-2M`, `1m-(act)-2m` and
   `1M-2M-3M` in competition are all unauthored, so the *generic* ladder
   answers them — `uc_nt2` bids a natural 2NT over a sign-off, `uc_raise_S3`
   raises a sign-off, `uc_raise_H4` accepts every invitation on 11 support
   points.  Four small contexts, each with a `requires: {}` floor, fix all
   four.  This is round 17's finding restated below game: *an invitation is
   worth nothing until the seat that answers it exists.*

3. **The ladders are banded by strength and forgotten by shape.**  A 5-5
   eighteen-count after 1M-1NT has to squeeze into a 12-17 rung (387); a 6-5
   hand repeats its six-card suit a third time instead of showing the second
   (870); a seven-card suit has no four-level rebid when partner has never
   spoken (49); a six-card suit is worth less than a five-card one over their
   1NT (243) and over their overcall (871); a limit raise is allowed on three
   ragged trumps (515, 885).  Every one of these is an *additive* rung.

---

## Method notes that apply to every entry below

* Every "deciding rule" claim was re-derived with `fast_decision`, not read out
  of the dossier's `rule` column.  **Board 261 is the guardrail's case in
  point:** the dossier names `uc_doubler_game3_H`, which fits **0.409**; the
  rule that actually chose 4H is `uc_raise_H4` at fit 1.000.  The proposal is
  written against the real chooser.
* Every new context that defines `P` was checked against the pass filter in
  `score_candidates`: a `requires: {}` pass is **not discriminating** and is
  dropped whenever pass is forbidden, so a floor pass written that way can
  silently delete an authored pass from a less specific context.  This bit one
  of my prototypes (board 585) and the corrected version is additive instead.
* New contexts that share a pattern with an existing one are placed **later in
  the file**, so `match_all_contexts`'s file-order tie-break makes them a pure
  superset: they can only supply calls the earlier context does not define.

---

## Board 784 — NOTHING-WRONG (constructive)

**Seat/call.** Table A call 0, N passes `97642.KQ6.A.Q986` in first seat;
BEN opens 1S.

**What I checked.**  `open_1S_rule20` scores 0.082 because its credential is
`suit_quality(S) >= 1.5` and 97642 holds no honour at all; `open_1S` misses on
HCP (11 v 12) at 0.800, and `open_pass` fits 1.00 at priority 20.  Opening
style and rule-of-20 thresholds are on the do-not-re-propose list
(`DECISIONS.md`), and the rest of both auctions is a weak jump overcall and a
Law-level competitive sequence — no constructive rung is consulted after call
0 at either table.

**Verdict.** NOTHING-WRONG in the constructive discipline.  The board belongs
to the competitive reviewer.

---

## Board 809 — responder's rebid after 1M - 1NT - 2M does not exist

**Seat/call.** Table A call 7, seat N: `P 1H P 1NT P 2H P`, hand
`T8.T3.AQ32.AT864`.  We pass; 4H is cold on the double-dummy sheet.

**The missing agreement.**  Opener's rebid of his own major over the
semi-forcing 1NT shows six cards, so responder's raise to three is
invitational on a **doubleton** — the eight-card fit is already known — and
that whole seat is unauthored: `context_at` returns only
`general_uncontested_continuation` and `general_slam_try`, and `uc_pass` wins
at fit 1.00.

**YAML.**

```yaml
  - id: responder_rebid_after_1M_rebid
    description: "Responder's second call after 1M - 1NT - 2M: opener has six"
    expand: { M: [H, S] }
    pattern: "1$M - P - 1NT - P - 2$M - P - ?"
    rules:
      - id: rr2m_game_$M
        call: 4$M
        priority: 58
        requires: { suits: { $M: [2, 13] }, evals: { total_points: [13, 40] } }
        shows: "game values and two or more of opener's six-card suit"
        establishes: { forcing: sign_off, agreed_suit: $M }
      - id: rr2m_raise_$M
        call: 3$M
        priority: 56
        requires: { suits: { $M: [2, 13] }, evals: { total_points: [10, 12] } }
        shows: "invitational raise: 10-12 with two or more of opener's six-card suit"
        establishes: { forcing: invitational, agreed_suit: $M }
      # carries uc_new_*3's own gate as the second half of the disjunction, so
      # defining 3C/3D here can only be a SUPERSET of what it shadows
      - id: rr2m_new_3C_$M
        call: 3C
        priority: 55
        requires:
          any_of:
            - { suits: { C: [6, 13] }, evals: { total_points: [10, 12] } }
            - { suits: { C: [5, 13] }, evals: { total_points: [14, 40] } }
        shows: "natural clubs: a six-card suit worth an invitation, or a five-card suit with game values"
        establishes: { forcing: invitational }
      - id: rr2m_new_3D_$M
        call: 3D
        priority: 55
        requires:
          any_of:
            - { suits: { D: [6, 13] }, evals: { total_points: [10, 12] } }
            - { suits: { D: [5, 13] }, evals: { total_points: [14, 40] } }
        shows: "natural diamonds: a six-card suit worth an invitation, or a five-card suit with game values"
        establishes: { forcing: invitational }
      - id: rr2m_pass_$M
        call: P
        priority: 20
        requires: {}
        shows: "no game interest opposite the minimum six-card rebid"
        establishes: { forcing: sign_off }
```

**THE ANSWERING SEAT** (3M is an invitation, so it ships in the same proposal):

```yaml
  - id: opener_over_1NT_rebid_invite
    description: "Opener answers the invitational raise after 1M - 1NT - 2M - 3M"
    expand: { M: [H, S] }
    pattern: "1$M - P - 1NT - P - 2$M - P - 3$M - P - ?"
    rules:
      - id: o2mi_accept_$M
        call: 4$M
        priority: 55
        requires: { evals: { total_points: [14, 40] } }
        shows: "accepting: better than the dead minimum the 2M rebid promised"
        establishes: { forcing: sign_off, agreed_suit: $M }
      - id: o2mi_decline_$M
        call: P
        priority: 50
        requires: {}
        shows: "declining: the minimum six-card rebid, nothing extra"
        establishes: { forcing: sign_off }
```

**What it endangers.**  The new context owns `P`, `3M`, `4M`, `3C`, `3D` in
this seat.  Below it: `uc_pass` (18) — replaced by an identical floor;
`uc_raise_H3`/`H4` (31/32) — those demand three trumps and an eight-card LOTT
count, which is wrong opposite a *shown* six-card suit, so mine is the better
description; `uc_new_C3`/`D3` (27) — their exact gate is carried verbatim as
the second `any_of` branch, so nothing is deleted.  Above it: nothing in this
seat is above 32 except `gst_rkc_H` at 46, which fits 0.000 here and is not
reachable on 6-11 anyway.

**VERIFIED.**  `1H P 1NT P 2H P` → **3H** (`rr2m_raise_H`), then
`3.AKQ964.JT8.K97` → **4H** (`o2mi_accept_H`).  Regression checks: a 7-count
with `T8.T3.Q432.T8642` still passes (`rr2m_pass_H`).

**Template.** `expand: { M: [H, S] }` on both contexts, as written.  A minor-
suit twin is not wanted (1m-1NT-2m is a different animal).

---

## Board 870 — six-five: show the second suit, do not name the first a third time

**Seat/call.** Table A call 8, seat S: `1H 2C 2D 3C 3H P P 4C`, hand
`AJ943.AQ8543.94.` — we bid 4H (`ch_rebid_H4`, fit 1.000, prio 29); 4S makes
ten tricks.

This is a competitive auction and the rung lands in the competitive-high
ladder, so it overlaps the other reviewer's lane; the *content* is
shape-showing, which is mine.

**The missing agreement.**  A hand that has already named a six-card suit
twice tells partner nothing by naming it a third time; with six-five the
five-card second suit is the new information, and the shape supplies the
tricks that the 12-HCP floor on `ch_new_S4` is asking for.

**YAML** (written out per suit because `general_competitive_high` is not
templated; the two majors are given, the minors are the same rung):

```yaml
      - id: ch_new_65_S4
        call: 4S
        priority: 29.5
        when: { unbid_suit: S, cheapest_in_suit: true, partner_has_acted: true }
        requires:
          suits: { S: [5, 13] }
          evals: { longest_suit_length: [6, 13], total_points: [13, 40], "suit_quality(S)": [1.0, 9] }
        shows: "six-five: showing the five-card second suit instead of repeating the six-card one"
        establishes: { forcing: non_forcing, agreed_suit: S }
      - id: ch_new_65_H4
        call: 4H
        priority: 29.5
        when: { unbid_suit: H, cheapest_in_suit: true, partner_has_acted: true }
        requires:
          suits: { H: [5, 13] }
          evals: { longest_suit_length: [6, 13], total_points: [13, 40], "suit_quality(H)": [1.0, 9] }
        shows: "six-five: showing the five-card second suit instead of repeating the six-card one"
        establishes: { forcing: non_forcing, agreed_suit: H }
```

**ANSWERING SEAT.**  None needed: the rung is `non_forcing` and sets
`agreed_suit`, so partner's existing raise/pass ladder reads it.  (That
`agreed_suit` is the same reason `ch_rebid_*4` carries one — see its comment.)

**What it endangers.**  `ch_rebid_H4` (29) — on a 6-5 hand the second suit is
strictly more informative than a third bid of the first; `ch_new_S4` (28) and
`ch_new_S4_hi` (28.5) — my rung is the same call with a *stricter* shape gate
and a lower point floor, so it only takes hands they were describing at fit
0.8 or worse.  Nothing below 27 is reachable at the four level here.

**VERIFIED.**  `1H 2C 2D 3C 3H P P 4C` → **4S** (`ch_new_65_S4`), replacing
4H.  4S by S is ten tricks on the sheet (+420 versus 4H down one).

**Template.** Four rules (C/D/H/S) in `general_competitive_high`, and the same
four in `general_balancing_high`, which has the identical `ch_`/`balhigh_`
ladder.

---

## Board 938 — THE ANCHOR: help-suit game tries, and the seat that answers them

**Seat/call.** Table A call 6, seat N: `P P 1S P 2S P`, hand
`AKT875.J74.Q.A96` — 16 total points, six spades.  `op_after_raise_pass`
(12-16) fits 1.000 and we pass out 2S; 4S makes ten tricks.
`op_after_raise_inv` (17-18) misses by one point at 0.800.

**The missing agreement.**  Opposite the single raise the file can only add
points and bid 3M; naming the suit in which partner's honours or shortness
turn losers into tricks asks a question 3M cannot, and because the answer is
informed the try opens two points lower.  **Trial bids: 0 rules in the file.**

**YAML — the try** (added to the existing context, which already owns P/3M/4M):

```yaml
      - id: oar_trial_3C_$M
        call: 3C
        priority: 53.3
        requires:
          suits: { $M: [5, 13], C: [3, 5] }
          evals: { total_points: [15, 18], ltc: [0, 7], "suit_quality(C)": [0, 2.0] }
        shows: "help-suit game try: five or more $M, 15-18 total points, three to five losing clubs"
        establishes: { forcing: invitational, agreed_suit: $M }
        alertable: true
      - id: oar_trial_3D_$M
        call: 3D
        priority: 53.2
        requires:
          suits: { $M: [5, 13], D: [3, 5] }
          evals: { total_points: [15, 18], ltc: [0, 7], "suit_quality(D)": [0, 2.0] }
        shows: "help-suit game try: five or more $M, 15-18 total points, three to five losing diamonds"
        establishes: { forcing: invitational, agreed_suit: $M }
        alertable: true
      # the floor: this context now DEFINES 3C and 3D, so it must not delete
      # the natural three-level rebid the generic ladder used to supply
      - id: oar_natural_3C_$M
        call: 3C
        priority: 51
        requires: { suits: { C: [6, 13] }, evals: { total_points: [16, 40] } }
        shows: "natural clubs: a real six-card second suit with extras"
        establishes: { forcing: non_forcing }
      - id: oar_natural_3D_$M
        call: 3D
        priority: 51
        requires: { suits: { D: [6, 13] }, evals: { total_points: [16, 40] } }
        shows: "natural diamonds: a real six-card second suit with extras"
        establishes: { forcing: non_forcing }
```

(context: `responder_rebid_after_1M_raise`, `expand: { M: [H, S] }`, inserted
after `op_after_raise_inv`.)

The heart trial after 1S-2S cannot live in that context (`3$oM` would expand to
3S for M=H, which is not a trial), so it gets a same-pattern context placed
**later in the file** — the file-order tie-break makes it a pure superset that
can only add the 3H call:

```yaml
  - id: opener_trial_heart_after_1S_raise
    description: "1S - 2S: 3H is the heart help-suit game try"
    pattern: "1S - P - 2S - P - ?"
    rules:
      - id: oar_trial_3H_S
        call: 3H
        priority: 53.1
        requires:
          suits: { S: [5, 13], H: [3, 5] }
          evals: { total_points: [15, 18], ltc: [0, 7], "suit_quality(H)": [0, 2.0] }
        shows: "help-suit game try: five or more spades, 15-18 total points, three to five losing hearts"
        establishes: { forcing: invitational, agreed_suit: S }
        alertable: true
      - id: oar_natural_3H_S
        call: 3H
        priority: 51
        requires: { suits: { H: [6, 13] }, evals: { total_points: [16, 40] } }
        shows: "natural hearts: a real six-card second suit with extras"
        establishes: { forcing: non_forcing }
      # inert (the earlier context defines P first) - it exists only so the
      # [floor] lint can see this context is never the reason a seat is stuck
      - id: oar_trial_floor_S
        call: P
        priority: 1
        requires: {}
        shows: "no heart game try applies"
        establishes: { forcing: sign_off }
```

**THE ANSWERING SEAT — this is the half that makes the try worth anything:**

```yaml
  - id: responder_over_trial
    description: "Responder answers opener's help-suit game try 1M - 2M - 3T"
    expand_pairs:
      - { M: H, T: C }
      - { M: H, T: D }
      - { M: S, T: C }
      - { M: S, T: D }
      - { M: S, T: H }
    pattern: "1$M - P - 2$M - P - 3$T - P - ?"
    rules:
      - id: rtr_accept_$T
        call: 4$M
        priority: 56
        requires:
          any_of:
            - { suits: { $T: [0, 2] } }
            - { evals: { "top_honour($T)": [1, 1] } }
            - { evals: { total_points: [9, 40] } }
        shows: "accepting the game try: shortness or a top honour in $T, or a maximum raise"
        establishes: { forcing: sign_off, agreed_suit: $M }
      - id: rtr_decline_$T
        call: 3$M
        priority: 50
        requires: {}
        shows: "declining the game try: a minimum raise with three or more losers in $T"
        establishes: { forcing: sign_off, agreed_suit: $M }
```

Note the decline is **3M, never pass** — leaving partner in three of a side
suit is the one outcome a trial bid must not produce, and `rtr_decline` at
priority 50 beats `uc_pass` at 18 with `requires: {}` fitting 1.00, so the
seat can never be starved.

**Priority design.** 53.3 / 53.2 / 53.1 orders the trial suits **cheapest
first**, so two eligible help suits resolve deterministically and the cheaper
one leaves 3M available as the decline.  All three sit above
`op_after_raise_inv` (52) and below `op_after_raise_game` (54): with 19+ we
still bid game, and with 15-18 the try replaces the bare invitation.

**What it endangers.**
* `op_after_raise_pass` (P, 50) — 15-16-point hands that used to pass now
  make a try.  That is the *intended* subtraction and it is where the board's
  IMPs are; the `ltc <= 7` and five-trump gates keep flat minima out.
* `op_after_raise_inv` (3M, 52) — 17-18 hands with a help suit now name it.
  Strictly more information for the same level.
* `uc_new_C3`/`uc_new_C3_hi`/`uc_new_D3` (27/27.5) — **defining 3C and 3D in
  this context blocks them in every `1M-2M` seat, fit or no fit.**  That is
  why `oar_natural_3C/3D` are in the proposal: they carry a natural reading
  for the exact hand type (a real six-card second suit with extras) that the
  generic rungs were describing.
* `gst_rkc_$M` (46) — fits 0.000 in this seat; untouched.

**VERIFIED.**  `P P 1S P 2S P` → **3C** (`oar_trial_3C_S`, fit 1.000); then
`J64.K63.AJ76.Q83` → **4S** (`rtr_accept_C`, fit 1.000).  The board becomes
`P P 1S P 2S P 3C P 4S`, ten tricks, +420 instead of +170.  Regression battery:
an 18-count still bids 4S; a 19-count still bids 4S; `responder_over_game_try`
still answers a plain 3S try with 4S (`rgt_accept`).

**Template.** `expand: { M: [H, S] }` for the two minor trials; the third trial
suit needs the extra context above (H after 1S).  `expand_pairs` over five
(M, T) combinations for the answering context.  The natural extension, not
proposed here because it needs its own context, is **2S as the cheap trial
after 1H - 2H**.

---

## Board 942 — a flat twelve is not a game force

**Seat/call.** Table B call 3, seat E: `P 1D P`, hand `Q5.763.K72.AKT95` —
`r1m_2over1` (12+ HCP, 4+ clubs) fits 1.000 at priority 70 and forces to game;
opener's 24 flat HCP then reach 3NT, down one.  BEN bids 2NT.

**The missing agreement.**  A 2/1 game force in a minor commits 24 flat points
to nine tricks; with a 5-3-3-2 twelve-count and no major the hand is worth an
invitation, not a force.

**YAML** (`resp_1m`, `expand: { m: [C, D] }`):

```yaml
      - id: r1m_2over1
        call: 2C
        priority: 70
        requires:
          hcp: [12, 40]
          suits: { C: [4, 13] }
          not: { hcp: [0, 12], balanced: true }
        shows: "2/1 game forcing: 4+ clubs, 12+ HCP (a flat twelve invites with 2NT instead)"
        establishes: { forcing: game_forcing }
        when: { passed_hand: false }
```

**ANSWERING SEAT.**  Already authored: the hand lands on `r1m_2NT`
(invitational 11-12) and `opener_over_invite_2NT_minor` answers it.  No new
seat is needed — that is the point of routing the hand *down* a rung.

**Companion proposal (the documented open item this board sits on).**
`ROUND_METHOD.md` records that `1D - P - 2C - P - ?` is unauthored: opener's
only candidates come from `gf_landing_nt` and `gf_landing_new_suit`, which is
why `gf_3NT` chose the contract.  The 2/1-in-a-minor rebid ladder:

```yaml
  - id: opener_rebid_1D_2C_gf
    description: "Opener's rebid after 1D - 2C, the 2/1 game force in a minor"
    pattern: "1D - P - 2C - P - ?"
    rules:
      - id: ob1d2c_2H
        call: 2H
        priority: 60
        requires: { suits: { H: [4, 13] } }
        shows: "four or more hearts, shown up the line in the game force"
        establishes: { forcing: game_forcing }
      - id: ob1d2c_2S
        call: 2S
        priority: 59
        requires: { suits: { S: [4, 13], H: [0, 3] } }
        shows: "four or more spades, no four-card heart suit"
        establishes: { forcing: game_forcing }
      - id: ob1d2c_2D
        call: 2D
        priority: 56
        requires: { suits: { D: [6, 13] } }
        shows: "six or more diamonds"
        establishes: { forcing: game_forcing }
      - id: ob1d2c_3C
        call: 3C
        priority: 55
        requires: { suits: { C: [4, 13] } }
        shows: "raising the 2/1 suit: four-card club support (GF)"
        establishes: { forcing: game_forcing, agreed_suit: C }
      - id: ob1d2c_3NT
        call: 3NT
        priority: 51
        requires: { hcp: [18, 19], balanced: true }
        shows: "18-19 balanced"
        establishes: { forcing: non_forcing }
      - id: ob1d2c_2NT
        call: 2NT
        priority: 40
        requires: {}
        shows: "no major, no sixth diamond, no club fit: 2NT keeps the game force alive at the cheapest level"
        establishes: { forcing: game_forcing }
```

The last rung is the landing floor: `requires: {}` so the seat can never be
starved, at a priority below every descriptive rung.

**What it endangers.**  The gate on `r1m_2over1` subtracts exactly one class:
balanced twelve-counts with four-plus clubs and no four-card major, which now
bid 2NT.  Every 13+ hand and every unbalanced twelve is untouched.  The new
context takes 2H/2S/2D/3C/3NT/2NT away from `gf_landing_*` in this one auction;
`gf_3NT` (37) and `gf_new_2$X` (36) are the rungs displaced, and a described
rebid beats a landing default in a game force by construction.

**VERIFIED** (the gate): `P 1D P` → **2NT** (`r1m_2NT`).  Regressions: a flat
*thirteen* still bids 2C; a shapely twelve with four hearts still bids 1H.
The rebid ladder is **UNTESTED** — it loads, but the board is already recovered
by the gate and I did not trace a hand through it.

**Template.** The gate is inside `expand: { m: [C, D] }` already.  The rebid
ladder should get `expand: { m: [C, D] }` with `pattern: "1$m - P - 2C - P - ?"`
so `1C - P - 2C` (the strong club raise) gets the same ladder.

---

## Board 4 — nobody answers an invitational raise

**Seat/call.** Table B call 9, seat E: `P 1C 1D 1H P 2H P 3H P`, hand
`A87.KT92.Q65.A72` — E raised to 2H (limited), W invited with 3H, and E
accepted with **`uc_raise_H4`** (11+ support points, a real trump fit), which
is the *generic* raise rung, not an answer to an invitation.  4H is one off.

**The missing agreement.**  A seat that has already limited itself with a raise
to two answers partner's invitation with a *maximum for the range it showed* —
it does not re-value the hand from scratch on the generic raise ladder.

**YAML.**

```yaml
  - id: answer_raise_invitation
    description: "Somebody raised to 2M and partner invited with 3M: the seat that must answer"
    expand: { M: [H, S] }
    pattern: "... - 1$M - P - 2$M - P - 3$M - P - ?"
    rules:
      - id: ari_accept_$M
        call: 4$M
        priority: 55
        when: { partner_last_suit: $M }
        requires:
          suits: { $M: [3, 13] }
          evals: { total_points: [15, 40] }
        shows: "accepting the invitation: a maximum for the raise already made"
        establishes: { forcing: sign_off, agreed_suit: $M }
      - id: ari_decline_$M
        call: P
        priority: 50
        when: { partner_last_suit: $M }
        requires: {}
        shows: "declining: the raise to two already described this hand"
        establishes: { forcing: sign_off }
```

**THE ANSWERING SEAT.**  This *is* the answering seat; the invitation
(`uc_raise_$M3`, or any 2M-then-3M sequence) already existed with nobody to
hear it.

**What it endangers, and the two prototypes I had to throw away to get here.**
My first draft used `pattern: "... - 2$M - P - 3$M - P - ?"` with no `when`.
That is five tokens of specificity, so it took over `4M` and `P` in **every**
auction ending `2M P 3M P` — including auctions where the 2M and 3M were bid by
the *opponents*.  The corpus replay caught it: board 385 went `4S → 3NT`
(my rung blocked `uc_raise_S4` and then did not fit) and board 389 went
`P → 4NT` in a 2C auction.  The shipped version fixes both by (a) anchoring the
pattern on `1$M` so the major must have been opened at the one level, and
(b) `when: { partner_last_suit: $M }` so the invitation must be partner's.
Within its own seat it outranks `uc_raise_$M4` (32) and `uc_pass` (18); the
`requires: {}` decline means the seat is never starved, and
`responder_over_game_try` (specificity 1007) still owns the uncontested
`1M-2M-3M` try.

**VERIFIED.**  `P 1C 1D 1H P 2H P 3H P` → **P** (`ari_decline_H`), replacing
4H.  3H by W makes nine tricks on the sheet, so both tables score 3H making and
the board is flat instead of -5.  `rgt_accept` (1S-2S-3S) is unaffected.

**Template.** `expand: { M: [H, S] }`.  The minor twin (`... - 1$m - P - 2$m -
P - 3$m - P - ?`) is the same idea and should be added with a 5m accept.

---

## Board 19 — competitive; the ceiling it exposes is real

**Seat/call.** Table B call 4, seat W: `1C 1H X P`, hand `AT73.J86.A2.A942` —
`onx_major1_CH` (bid the major the double implied, 4 cards, **12-16**) fits
1.000 and is right for a 13-count.  The board is then lost to a Law-level
competitive sequence (`ballow_raise_lott4_S` bidding 4S).

**Verdict on the board: competitive.**  W's 1S is the correct constructive
call and I would make it.

**The agreement the board exposes.**  Both rungs that show the major the
negative double promised (`onx_major_$m$M` at 60, `onx_major1_$m$M` at 61) are
capped at 16, so a 17-19 opener with four of them makes exactly the same bid as
a twelve-count.  The ceiling species from rounds 6 and 7, still paying.

```yaml
      - id: onx_jumpmajor_$m$M
        call: "2$oM"
        priority: 59.5
        when: { cheapest_in_suit: false }
        requires: { suits: { $oM: [4, 13] }, hcp: [17, 19] }
        shows: "jump in the major the double implied: 4 cards, 17-19, invitational"
        establishes: { forcing: invitational, agreed_suit: $oM }
```

**THE ANSWERING SEAT.**  The jump is invitational and sets `agreed_suit`, so
the advancer's existing raise/pass ladder in `general_uncontested_continuation`
reads it; `board 4`'s `answer_raise_invitation` does **not** cover it (the
pattern is anchored on `1$M`).  If the batch is shipped, add the twin
`"... - X - P - 2$M - P - ?"` answering context modelled on
`doubler_answers_jump_advance` below.

**What it endangers.**  Nothing: `2$oM` at the jump level is undefined in this
context (`onx_major_$m$M` carries `cheapest_in_suit: true`), and the 12-16
rungs keep their whole band.  Additive.

**VERIFIED that it fires** on `AQ73.J86.AQ.AQ42` (17 HCP) → **2S**
(`onx_jumpmajor_CH`).  **It does not change board 19**, whose hand is 13 — I
am reporting it because it is a real hole, not because it recovers these IMPs.

**Template.** Already inside the context's four-way `expand_pairs`.

---

## Board 49 — a seven-card suit has no four-level rebid when partner never spoke

**Seat/call.** Table A call 5, seat S: `P 1H 3S P P`, hand
`Q.AT98653.AK4.Q5` — seven hearts, 15 HCP.  We pass out 3S.  `uc_rebid_H4`
scores **0.000** and `balhigh_reopen_X` 0.012; only `balhigh_pass` fits.

**Why the seat is starved (and it is not a points problem).**
`balhigh_rebid_H4` carries `when: { my_suit: H, cheapest_in_suit: true,
partner_has_acted: true }`.  Partner has *never had a cheap chance to speak* —
my one-level opening was jumped over — so the one condition that would let me
rebid rules the rung out structurally.  A `when` gate is a hard exclusion, so
no amount of playing strength reaches it.

**The missing agreement.**  Seven cards and fourteen points is a trump proposal
in its own right; it does not need partner to have spoken first.

```yaml
      - id: balhigh_rebid_solo_C4
        call: 4C
        priority: 29.5
        when: { my_suit: C, cheapest_in_suit: true }
        requires:
          suits: { C: [7, 13] }
          evals: { total_points: [14, 40], "suit_quality(C)": [1.5, 9] }
        shows: "a seven-card suit named again at the four level: a trump proposal, not a competitive noise bid"
        establishes: { forcing: non_forcing, agreed_suit: C }
```

…and the identical rung for D, H and S.

**ANSWERING SEAT.**  None required — `non_forcing` with `agreed_suit` set,
which is exactly the shape `ch_rebid_*4`/`balhigh_rebid_*4` already use so that
the `gf_landing` family is not left dark.

**What it endangers.**  `balhigh_rebid_$X4` (29) — same call, and my gate is a
strict subset of its hand type (seven cards instead of six, plus a quality
floor), so on the hands both describe mine is the more specific.
`balhigh_pass` (21) and `balhigh_reopen_X` (41): the double stays available and
outranks me whenever it fits, which is correct — with 16+ and shortness in
their suit the double is the better call.

**VERIFIED.**  `P 1H 3S P P` → **4H** (`balhigh_rebid_solo_H4`).  4H by S is
nine tricks: -50 instead of -140.

**Template.** Four rules in `general_balancing_high`; the same four belong in
`general_competitive_high` (`ch_rebid_solo_*4`), where the identical
`partner_has_acted` condition sits on `ch_rebid_*4`.

---

## Board 84 — our own agreed partscore is doubled and nobody owns the seat

**Seat/call.** Table A call 8, seat N: `1D P 1H P 2H P P X`, hand
`AQ76.AT85.K92.86` — we bid **2S** (`xd_second_S2`, "my second suit over their
double, 4+ S, 14+ points", fit 1.000).  Having already raised to 2H and
limited the hand, introducing a fourth suit at the two level is a second
description of values already shown; the auction ran away to 3H, -100.

**The missing agreement.**  When our own agreed partscore is doubled in the
balancing seat, the seat that must speak is a *defence* seat: sit, redouble
with real extras, or compete with a sixth trump.  There is no context for it,
so the generic run-out ladder answers a balancing double as if it were a
takeout double of our opening.

**YAML.**

```yaml
  - id: our_agreed_partscore_doubled
    description: "Our agreed two-level partscore is doubled after two passes"
    expand: { M: [H, S] }
    pattern: "... - 2$M - P - P - X - ?"
    rules:
      - id: oapd_XX_$M
        when: { we_hold_contract: true }
        call: XX
        priority: 56
        requires: { evals: { total_points: [17, 40] } }
        shows: "redouble: real extras, we are not being pushed out of our own partscore"
        establishes: { forcing: non_forcing, agreed_suit: $M }
      - id: oapd_3$M
        when: { we_hold_contract: true }
        call: 3$M
        priority: 54
        requires: { suits: { $M: [6, 13] }, evals: { total_points: [14, 40] } }
        shows: "a sixth trump: competing to the three level in the agreed suit"
        establishes: { forcing: non_forcing, agreed_suit: $M }
      - id: oapd_pass_$M
        when: { we_hold_contract: true }
        call: P
        priority: 52
        requires: {}
        shows: "sitting for the balancing double of our agreed partscore: partner has the next word"
        establishes: { forcing: non_forcing }
```

`we_hold_contract: true` is load-bearing: without it the pattern also matched
auctions where **their** 2M was doubled, and the corpus replay showed the rung
firing there (board 350).

**ANSWERING SEAT.**  The pass is a sign-off in a live auction and partner's
existing `general_pull_or_sit` ladder answers it; the redouble is `non_forcing`
with `agreed_suit` set, which the same ladder reads.

**What it endangers.**  `xd_second_$X2` (25), `xd_pass` (18), `xd_XX_extras`
(23), `xd_rebid_*3` (34) — the whole run-out family, but only in the narrow
shape "our agreed 2M, doubled after two passes".  In that shape a run-out is
the wrong tool by definition: we have a fit and they are balancing.  The
`requires: {}` pass floor at 52 means the seat is never starved.

**VERIFIED.**  `1D P 1H P 2H P P X` → **P** (`oapd_pass_H`), replacing 2S.

**Template.** `expand: { M: [H, S] }`; the minor twin
(`... - 2$m - P - P - X - ?`) is the same agreement and should be added.

---

## Board 151 — a sign-off is raised, because the seat that hears it is empty

**Seat/call.** Table A call 9, seat N: `P 1C P 1S P 2C P 2S P`, hand
`KJ2.8.A98.AJ9874`.  Responder's 2S is `rmr_2M`, `establishes: { forcing:
sign_off }`.  We raise it: **`uc_raise_S3`** (3+ trumps, 10+ support points,
fit 1.000, prio 31), from the generic ladder.  3S is one off; 2S makes.

**The missing agreement.**  Responder's two-level rebid of his own major over
opener's minor rebid says "no fit for your suit, and no game" — opener passes
unless he has a genuine maximum with four-card support.

**YAML.**

```yaml
  - id: opener_over_minor_rebid_preference
    description: "Opener hears responder's to-play 2M after 1m - 1M - 2m"
    expand: { m: [C, D], M: [H, S] }
    pattern: "1$m - P - 1$M - P - 2$m - P - 2$M - P - ?"
    rules:
      - id: omrp_raise_$M
        call: 3$M
        priority: 52
        requires: { suits: { $M: [4, 13] }, evals: { total_points: [16, 40] } }
        shows: "four-card support and a maximum: raising responder's own suit"
        establishes: { forcing: invitational, agreed_suit: $M }
      - id: omrp_pass_$M
        call: P
        priority: 50
        requires: {}
        shows: "responder signed off in his own suit with no fit for the rebid minor; the 12-15 rebid has nothing to add"
        establishes: { forcing: sign_off }
```

**THE ANSWERING SEAT** for `omrp_raise_$M` (it is an invitation): board 4's
`answer_raise_invitation` does not match this pattern, so if the raise rung
ships it needs `"1$m - P - 1$M - P - 2$m - P - 2$M - P - 3$M - P - ?"` with a
4$M accept (`total_points: [10, 40]`) and a `requires: {}` pass.  I would ship
`omrp_pass_$M` alone if that context is not authored — the pass is the whole
gain on this board.

**What it endangers.**  `uc_raise_S3` (31), `uc_raise_S4` (32),
`uc_rebid_C3` (27) and `uc_pass` (18) in this one seat.  Every one of them is
the generic ladder ignoring the fact that partner has signed off; the raise
rung preserves the only case where bidding on is right.

**VERIFIED.**  `P 1C P 1S P 2C P 2S P` → **P** (`omrp_pass_S`).  2S by S is
eight tricks: +110 instead of -100.

**Also worth recording (not proposed as a separate fix).**  Responder's own
call on this board fits only **0.800**: `rmr_2M`'s five-card branch demands
6-10 HCP and the hand is a **5**-count, while `rmr_pass` demands two clubs and
the hand has a singleton.  There is a genuine band hole at 0-5 with shortness
in the rebid minor.  The one-line repair is to drop the five-card branch's HCP
floor to 0 — a weak preference is not a strength statement — but that is a
second agreement on the same board and the answering seat is the bigger one.

**Template.** `expand: { m: [C, D], M: [H, S] }` as written, four contexts.

---

## Board 172 — competitive; the agreement it exposes is the fit-showing jump

**Seat/call.** Table A call 2, seat S: `1H X`, hand `JT854.843.K94.Q3` — we bid
1S (`rx_H_1S`, 4+ S, 6-9, non-forcing, fit 1.000, prio 62) over
`jordan_raise` (60).  BEN raises to 2H.  With five spades and six points 1S is
a defensible constructive call and I am not indicting it.

**Verdict on the board: competitive.**

**The agreement it exposes: fit-showing jumps, which the convention audit counts
at ZERO rules.**  Over a takeout double the jump in a new suit is the cheapest
way to say "support AND a source of tricks" in one bid, which is exactly what
partner needs to judge the level — and it is the bid this hand *wants* to make
two points stronger.

```yaml
      - id: rxfit_3C_$M
        call: 3C
        priority: 63
        requires:
          suits: { C: [5, 13], $M: [3, 13] }
          evals: { total_points: [9, 12], "suit_quality(C)": [2, 9] }
        shows: "fit-showing jump: 9-12 with $M support and a good five-card club suit"
        establishes: { forcing: invitational, agreed_suit: $M }
        alertable: true
      - id: rxfit_3D_$M
        call: 3D
        priority: 63
        requires:
          suits: { D: [5, 13], $M: [3, 13] }
          evals: { total_points: [9, 12], "suit_quality(D)": [2, 9] }
        shows: "fit-showing jump: 9-12 with $M support and a good five-card diamond suit"
        establishes: { forcing: invitational, agreed_suit: $M }
        alertable: true
```

(context `resp_1M_over_X_jordan`, `expand: { M: [H, S] }`.)

**THE ANSWERING SEAT** — shipped with it:

```yaml
  - id: opener_over_fit_jump
    description: "Opener answers responder's fit-showing jump over their takeout double"
    expand_pairs:
      - { M: H, T: C }
      - { M: H, T: D }
      - { M: S, T: C }
      - { M: S, T: D }
    pattern: "1$M - X - 3$T - P - ?"
    rules:
      - id: ofj_game_$T
        call: 4$M
        priority: 56
        requires: { evals: { total_points: [15, 40], wasted_in_partner_shortness: [0, 3] } }
        shows: "accepting the fit jump: the side suit supplies the tricks"
        establishes: { forcing: sign_off, agreed_suit: $M }
      - id: ofj_signoff_$T
        call: 3$M
        priority: 50
        requires: {}
        shows: "declining the fit jump: a minimum opening plays three of the major"
        establishes: { forcing: sign_off, agreed_suit: $M }
```

**What it endangers.**  `jordan_preempt` (3M, 62) is a different call.
`rdx_XX` (75) outranks the fit jump, so 10+ HCP hands still redouble — the fit
jump lives in the 9-12 *total point* band below it, which is where the shape
hands are.  `xd_run_C2`/`D2` (25) and the whole `uc_new_*3` family are
outranked; a fit jump is a strictly better description than "running to my own
suit".  The new answering context owns 4M and 3M in `1M - X - 3m - P - ?`,
which no context previously defined.

**VERIFIED that the conversation runs:** `1H X` with `K42.982.KQJ84.65` →
**3D** (`rxfit_3D_H`), then `A5.AKJ64.A73.982` → **4H** (`ofj_game_D`).
**It does not recover board 172** — that hand is 7 total points, two light for
the rung, and I did not widen the band to reach it because a fit jump on seven
points is not the agreement.

**Template.** Two rules × `expand: { M: [H, S] }` for the jump; four
`expand_pairs` for the answer.  The other-major fit jump (2S after 1H - X) needs
its own context, as with the trial bids.

---

## Board 209 — competitive; and a NEGATIVE RESULT on mini-splinters

**Seat/call.** Table A call 3, seat N: `1C 1D X`, hand `JT54.AJ85.K9765.` —
`xd_jumpraise_D3` (4+ trumps, 10+ support points) fits 1.000 on a hand whose
"10 support points" are 9 HCP plus a club void.  Competitive.

**Verdict on the board: competitive.**  The jump raise is Law-correct with
five-card support and a void; the board is lost on the four-level guess after
it.

**The agreement it exemplifies, and why I am NOT shipping it.**  The audit
counts **zero mini-splinters**.  I prototyped them in `resp_1H`/`resp_1S` — a
jump in a new suit one level below the splinter, showing the same shortness
with *limit-raise* values, which is precisely the distinction the raise ladder
cannot make:

```yaml
      - id: r1S_minispl_3C
        call: 3C
        priority: 64
        requires:
          any_of:
            - suits: { S: [4, 13], C: [0, 1] }
              hcp: [8, 11]
              evals: { total_points: [10, 13] }
            - suits: { C: [5, 13] }                 # uc_new_C3's own gate,
              evals: { total_points: [14, 40] }     # carried as a superset
        shows: "mini-splinter: 4+ spades, singleton or void in clubs, limit-raise values"
        establishes: { forcing: invitational, agreed_suit: S }
        alertable: true
```

**It is unreachable, and making it reachable costs more than it pays.**
`r1S_splinter_4C` is `hcp: [9, 13]` at priority **89**, so it swallows the
entire mini-splinter range: traced on `KQ85.K942.J8632.` the engine still bids
4C.  Re-cutting the splinter to 12-15 does make the mini-splinter fire — and it
opens an 11-point hole: `KQ85.KQ42.J863.2` (11 HCP, stiff club) went from a
sound **4C splinter to 1NT**, because it now misses the splinter's floor by one
and the mini-splinter's `total_points` ceiling by one.  Both halves reverted.

**Reported, not shipped.**  Mini-splinters need the splinter band re-cut *and*
the 11-13 seam re-authored in the same batch; that is a subject, not a rung, and
it belongs in its own round.

---

## Board 261 — the dossier names the wrong rule, and the real one accepts every invitation

**Seat/call.** Table A call 5, seat S: `2D X P 3H P`, hand `KQ75.QT95.T8.AK5`.

**The guardrail, exercised.**  The dossier's `rule` column says
`uc_doubler_game3_H`.  Re-ranked through `score_candidates`, that rule fits
**0.409** (15 total points against its 17 floor) and cannot be on the fast
path.  The rule that actually chose 4H is **`uc_raise_H4`** at fit **1.000**,
priority 32: *"raise of partner's H: 11+ support points, a real trump fit."*

**The missing agreement.**  Partner's jump advance of my takeout double is an
invitation showing 9-11; accepting it needs 17+ and a fit, not the generic
raise ladder's 11-point floor.  There is no context for the doubler's answer,
so the generic ladder answers it.

**YAML.**

```yaml
  - id: doubler_answers_jump_advance
    description: "The doubler answers advancer's invitational jump to three of a major"
    expand: { M: [H, S] }
    pattern: "... - X - P - 3$M - P - ?"
    rules:
      - id: daja_accept_$M
        call: 4$M
        priority: 40
        when: { partner_suit: $M, my_last_call_was_double: true, we_hold_contract: false }
        requires: { suits: { $M: [3, 13] }, evals: { total_points: [17, 40], "lott_total_trumps($M)": [8, 26] } }
        shows: "accepting the jump advance: 17+ and a real fit"
        establishes: { forcing: sign_off, agreed_suit: $M }
      - id: daja_decline_$M
        call: P
        priority: 38
        when: { partner_suit: $M, my_last_call_was_double: true, we_hold_contract: false }
        requires: {}
        shows: "declining the jump advance: a plain takeout double is not enough for game"
        establishes: { forcing: sign_off }
```

**THE ANSWERING SEAT.**  This is it — the invitation (`aw2D_3H` and its
siblings) was authored without one.

**What it endangers.**  In this seat only: `uc_raise_$M4` (32),
`uc_doubler_game3_$M` (35), `uc_doubler_game_$M` (35) and `uc_pass` (18).  The
three raise rungs are all the generic ladder failing to notice that partner has
already limited himself; the `requires: {}` decline at 38 means the seat is
never starved and the decline is *discriminating*-free but sits in a context
where pass is legal, so it is reached.  The `when` triple is copied verbatim
from `uc_doubler_game3_$M` so the rung can only fire in the doubler's own seat.

**VERIFIED.**  `2D X P 3H P` → **P** (`daja_decline_H`).  3H by N is nine
tricks: +140 instead of -100.

**Template.** `expand: { M: [H, S] }`.  A minor twin
(`... - X - P - 3$m - P - ?` answering with 5m) is the same agreement.

---

## Board 276 — NOTHING-WRONG (constructive)

**Seat/call.** Table A call 2, seat S: third-seat opening decision with
`A32.AJ95.T8.Q752` (11 HCP, 4-4-2-3).  We pass; BEN opens 1C.

**What I checked.**  `open_1C` misses by one HCP (0.800); the third-seat light
rungs `open_1C_rule20_third` (0.211) and `open_1H_third_light` (0.115) both
fail on shape and suit quality; `open_pass` fits 1.00.  Third-seat light
opening thresholds and the rule of 20 are explicitly scope-excluded.  Nothing
constructive is consulted after call 2 at either table — table B is a takeout
double and a balancing 2NT.

**Verdict.** NOTHING-WRONG in my discipline.

---

## Board 291 — ten opposite a minimum minor rebid is not an invitation

**Seat/call.** Table B call 6, seat E: `1D P 1S P 2D P`, hand
`J653.K6.K6.K6532` (10 HCP) — we bid **2NT** (`rmr_2NT`, "invitational,
11-12"), opener raises to 3NT, down.

**Why it happens.**  It is a soft-miss lottery inside
`responder_after_minor_rebid`: `rmr_2NT` needs 11 and the hand has 10 (fit
0.8); `rmr_pass` needs 6-9 *and two diamonds* and the hand has 10 and two (fit
0.8).  Two rules at 0.8 and the blended score picks the invitation.  There is a
one-point band hole at exactly 10.

**The missing agreement.**  Ten flat opposite a 12-15 minor rebid is 22-25
combined: that is a partscore, not an invitation.

```yaml
      - id: rmr_pass
        call: P
        priority: 50
        requires: { hcp: [6, 10], suits: { $m: [2, 13] } }
        shows: "no game interest opposite a minimum rebid (ten flat opposite 12-15 is not an invitation)"
        establishes: { forcing: sign_off }
```

**ANSWERING SEAT.**  Not applicable — this removes an invitation rather than
creating one.  (`opener_over_invite_2NT_minor` already answers `rmr_2NT`.)

**What it endangers.**  Widening the pass band to 10 makes `rmr_pass` fit 1.00
on hands where `rmr_2NT`, `rmr_3m` (10-12) and `rmr_2M` also live.  `rmr_3m`
and `rmr_2M` are at priorities 54 and 52 against the pass's 50, so a hand with
a real fit or a real suit still bids; only the flat 10-count that had *no*
fitting rule changes, which is exactly the hole.

**VERIFIED.**  `1D P 1S P 2D P` → **P** (`rmr_pass`), replacing 2NT.

**Template.** Already inside `expand: { m: [C, D], M: [H, S] }`.

---

## Board 300 — 2NT bid over partner's sign-off, because that seat is unauthored

**Seat/call.** Table A call 8, seat N: `1H P 1S P 1NT P 2S P`, hand
`85.K9765.A96.KQ6` — responder's 2S is `rrh_nt_2S`, `forcing: sign_off`.  We
bid **2NT** (`uc_nt2`, "natural 2NT: 11-12 balanced"), -300.

**The missing agreement.**  Responder's two-level rebid of his own suit over
the 1NT rebid is to play; opener passes.  `context_at` returns only the two
generic contexts, so `uc_nt2` — the file's most-litigated generic rung — owns
the decision.

**YAML.**

```yaml
  - id: opener_over_1NT_rebid_to_play
    description: "Opener hears responder's to-play 2M after the 1NT rebid (1m - 1M - 1NT - 2M)"
    expand: { m: [C, D], M: [H, S] }
    pattern: "1$m - P - 1$M - P - 1NT - P - 2$M - P - ?"
    rules:
      - id: o2mp_raise_$M
        call: 3$M
        priority: 52
        requires: { suits: { $M: [3, 13] }, evals: { total_points: [14, 40] } }
        shows: "a maximum 1NT rebid with real support for the six-card suit"
        establishes: { forcing: invitational, agreed_suit: $M }
      - id: o2mp_pass_$M
        call: P
        priority: 50
        requires: {}
        shows: "responder signed off in his own suit; the 12-14 rebid has nothing to add"
        establishes: { forcing: sign_off }

  - id: opener_over_1NT_rebid_to_play_1H1S
    description: "Opener hears responder's to-play 2S after 1H - 1S - 1NT"
    pattern: "1H - P - 1S - P - 1NT - P - 2S - P - ?"
    rules:
      - id: o2mp_raise_1H1S_S
        call: 3S
        priority: 52
        requires: { suits: { S: [3, 13] }, evals: { total_points: [14, 40] } }
        shows: "a maximum 1NT rebid with real spade support"
        establishes: { forcing: invitational, agreed_suit: S }
      - id: o2mp_pass_1H1S_S
        call: P
        priority: 50
        requires: {}
        shows: "responder signed off in his own suit; the 12-14 rebid has nothing to add"
        establishes: { forcing: sign_off }
```

**THE ANSWERING SEAT** for `o2mp_raise_$M` — as on board 151, if the raise rung
ships it needs `"... - 1NT - P - 2$M - P - 3$M - P - ?"` with a 4$M accept
(`total_points: [9, 40]`) and a `requires: {}` pass.  The pass rung alone is the
board's gain and is safe on its own.

**What it endangers.**  `uc_nt2` (28), `uc_nt3` (29), `uc_raise_S3`/`S4`
(31/32), `uc_rebid_H3` (29) and `uc_pass` (18) in this seat.  Every one of them
is the generic ladder bidding over a sign-off; a 12-14 opener who has already
denied three-card support and shown his shape has, by construction, nothing to
add.

**VERIFIED.**  `1H P 1S P 1NT P 2S P` → **P** (`o2mp_pass_1H1S_S`), replacing
2NT.  2S is seven tricks: -100 instead of -300.  A maximum with support
(`K85.KQ975.A96.K6`) still bids 3S.

**Template.** `expand: { m: [C, D], M: [H, S] }` plus the explicit 1H-1S twin,
exactly as `responder_rebid_after_1NT_rebid` and
`responder_rebid_after_1H_1S_1NT` are already paired.

---
