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
