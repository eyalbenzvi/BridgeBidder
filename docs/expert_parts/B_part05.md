# Expert B — constructive / team-IMP bidding — dossier part 05

**Scope.** All 38 boards of `docs/dossier_575757/part05.md`, read through the
constructive lens: the uncontested 2/1 machinery, opener's and responder's
rebid structures, the forcing notrump, the invitational/game boundary, and the
shape-showing that separates a minimum from a slam-going hand *before* game.

**Counts.** 38 boards → **27 proposals** (plus board 885, which is board 515's
agreement on a second hand), **8 NOTHING-WRONG**, and **2 negative results from
my own prototypes, reported rather than shipped** (mini-splinters, board 209;
"open the longer minor", board 838).

**Every one of the 27 proposals was traced through `fast_decision`** on the
actual hand and is marked **VERIFIED**; on **25** of them the board's own call
changes, and on the other two (19 and 172) the new rung fires on a hand of the
right type but the dossier board is not recovered — which is said so in the
entry rather than glossed.

**Everything in this file was prototyped together** in one scratch copy of the
system, so the aggregate is measured rather than asserted:

| | base | with every proposal in this file |
|---|---|---|
| contexts | 517 | **564** |
| rules | 2,344 | **2,523** |
| `lint_system.py` findings | 223 | **222** |
| our decisions changed on `reports/r18_before.jsonl` (10,335 replayed) | — | **87 (0.84 %)** |

`decide_fast` was replayed over all 10,335 of our decisions in the review
corpus under both systems, so the aggregate blast radius is measured and not
guessed; the per-batch breakdown and a sample of the changed auctions are at
the foot of this file.

**The 25 board-changing traces were re-run with every proposal applied at
once**, not one at a time: all 25 still produce the call the entry claims, so
the proposals do not cancel or shadow one another as a batch.

**The one thing in this file that is UNTESTED** is the companion
`opener_rebid_1D_2C_gf` ladder under board 942 — it loads and its ids and
template vars are legal, but the board is already recovered by the gate above
it and I did not trace a hand through the ladder itself.  It is labelled
UNTESTED in place.

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
## Board 387 — the 5-5 eighteen-count has no bid: opener's jump shift over the forcing notrump

**Seat/call.** Table B call 6, seat E: `P P 1S P 1NT P`, hand
`AKJ82.J7.KQ942.A` — five spades, five diamonds, 18 HCP.  Every second-suit
rebid in `opener_rebid_1M_1NT` is capped at 17, so `ob_1M1NT_2D` fits **0.800**
and wins the soft-miss lottery; the auction dies in 2S with 4S cold.

**The missing agreement.**  Opener's jump shift over the (semi-)forcing 1NT
shows 5-4 or better with 18-21 and is game forcing.  It is the standard way to
say "too good for a simple rebid", and the ladder simply has no rung above 17
that is not a rebid of the major.

**YAML — the jump** (`opener_rebid_1M_1NT`, `expand: { M: [H, S] }`):

```yaml
      - id: ob_1M1NT_jump3C_$M
        call: 3C
        priority: 58
        requires: { suits: { C: [4, 13], $M: [5, 13] }, hcp: [18, 21] }
        shows: "jump shift: 5-4 or better in $M and clubs with 18-21, game forcing"
        establishes: { forcing: game_forcing }
      - id: ob_1M1NT_jump3D_$M
        call: 3D
        priority: 58
        requires: { suits: { D: [4, 13], $M: [5, 13] }, hcp: [18, 21] }
        shows: "jump shift: 5-4 or better in $M and diamonds with 18-21, game forcing"
        establishes: { forcing: game_forcing }
```

and the other-major case, in `opener_rebid_1S_1NT_second_major` (which already
exists for exactly this reason — 1H-1NT-2S would be a reverse):

```yaml
      - id: ob_1S1NT_jump3H_S
        call: 3H
        priority: 58
        requires: { suits: { S: [5, 13], H: [4, 13] }, hcp: [18, 21] }
        shows: "jump shift: five spades and four or more hearts with 18-21, game forcing"
        establishes: { forcing: game_forcing }
      # inert floor (opener_rebid_1M_1NT[S] defines P earlier), added only so
      # this context stops tripping the [floor] lint once it has two rules
      - id: ob_1S1NT_floor_S
        call: P
        priority: 1
        requires: {}
        shows: "no second-suit rebid applies"
        establishes: { forcing: sign_off }
```

**THE ANSWERING SEAT — the jump is a game force, so both halves ship:**

```yaml
  - id: responder_over_1NT_jump_shift
    description: "Responder answers opener's 18-21 jump shift over the semi-forcing 1NT"
    expand_pairs:
      - { M: H, X: C }
      - { M: H, X: D }
      - { M: S, X: C }
      - { M: S, X: D }
      - { M: S, X: H }
    pattern: "1$M - P - 1NT - P - 3$X - P - ?"
    rules:
      - id: rjs1n_game_$X
        call: 4$M
        priority: 58
        requires: { suits: { $M: [3, 13] } }
        shows: "three-card support opposite the 5-4 or 5-5: the major game"
        establishes: { forcing: sign_off, agreed_suit: $M }
      - id: rjs1n_raise_$X
        call: 4$X
        priority: 57
        requires: { suits: { $X: [4, 13], $M: [0, 2] } }
        shows: "four-card support for opener's second suit, no fit for the major"
        establishes: { forcing: game_forcing, agreed_suit: $X }
      - id: rjs1n_pref_$X
        call: 3$M
        priority: 56
        requires: { suits: { $M: [2, 2], $X: [0, 3] } }
        shows: "doubleton preference to opener's major: no support for either suit, so the five-card one plays"
        establishes: { forcing: game_forcing, agreed_suit: $M }
      - id: rjs1n_3NT_$X
        call: 3NT
        priority: 54
        requires: {}
        shows: "placing the game opposite 18-21 when neither of opener's suits fits"
        establishes: { forcing: sign_off }

  - id: opener_over_1NT_jump_shift_preference
    description: "Opener over responder's doubleton preference to the jump-shift auction"
    expand_pairs:
      - { M: H, X: C }
      - { M: H, X: D }
      - { M: S, X: C }
      - { M: S, X: D }
      - { M: S, X: H }
    pattern: "1$M - P - 1NT - P - 3$X - P - 3$M - P - ?"
    rules:
      - id: ojsp_game_$X
        call: 4$M
        priority: 55
        requires: {}
        shows: "the 5-2 major game opposite the preference: 18+ opposite 6-11 is enough"
        establishes: { forcing: sign_off, agreed_suit: $M }
```

`rjs1n_3NT_$X` carries `requires: {}`, so the answering seat is never starved —
round 6's `rkc5H_signoff` lesson applied.

**What it endangers.**  `uc_new_C3`/`uc_new_D3` (27) are the only other rules
offering 3C/3D in this seat, and they are already unreachable: `ob_1M1NT_2C`
(52) and `ob_1M1NT_2D` (53) fit every hand they describe at a lower level and
outrank them.  `ob_1M1NT_3$M` (56) and `ob_1M1NT_4$M` (57) demand six of the
major and are untouched.  `ob_1M1NT_2NT` (51, 18-19 balanced) — my rung
requires 5-4 shape, so a balanced 18 still bids 2NT.

**VERIFIED, whole conversation.**  `P P 1S P 1NT P` → **3D**
(`ob_1M1NT_jump3D_S`); `Q5.A82.T6.KT9542` → **3S** (`rjs1n_pref_D`);
`AKJ82.J7.KQ942.A` → **4S** (`ojsp_game_D`).  4S by E is eleven tricks: +450
instead of +200.

**Template.** As written: two rules under the existing `expand: { M: [H, S] }`,
one in the 1S-only context, and five-way `expand_pairs` on both answering
contexts.

---

## Board 507 — NOTHING-WRONG (constructive)

**Seat/call.** Table A call 7, seat S: `P P 1C P 1S P 2S`, hand
`T.J93.QJT4.AKQ73` — we pass; BEN doubles.  Table B's first divergence is a
fourth-seat opening decision (`open_pass` on `A654.AK2.75.T982`, rule of 15).

**What I checked.**  `cl_takeout_X` scores **0.000** not because of the
singleton spade but because the hand holds five cards in their *other* suit
(clubs), which is correct — a takeout double with five clubs opposite an
opening 1C bidder is not a takeout double.  `cl_new_D3` (5+ cards, 14+ points)
fits 0.349 on a 13-count with four diamonds.  Fourth-seat rule-of-15 opening
thresholds are scope-excluded.

**Verdict.** NOTHING-WRONG in my discipline; the live question is a balancing
double, which is the competitive reviewer's.

---

## Board 508 — opener's rebid after a competitive raise of his minor is unauthored

**Seat/call.** Table A call 6, seat S: `P P 1C 1D 2C P`, hand
`T764.KQJT.AQ.963` — partner's 2C is `cl_raise_C2`, a *competitive* raise
(3+ trumps, 6-9 support points).  We bid **2NT** (`uc_nt2`, 11-12 balanced),
down three, -300.

**The missing agreement.**  A competitive raise of my minor is not an
invitation; a minimum opening passes and lets the opponents have the next word.

**YAML.**

```yaml
  - id: opener_over_competitive_minor_raise
    description: "Opener after partner's competitive raise of my minor in a contested auction"
    expand: { m: [C, D] }
    pattern: "1$m - act - 2$m - P - ?"
    rules:
      - id: ocmr_3NT_$m
        call: 3NT
        priority: 54
        requires: { hcp: [18, 21], evals: { weakest_unshown_stopper: [0.9, 9] } }
        shows: "18-21 with the unshown suits stopped: game opposite the raise"
        establishes: { forcing: sign_off }
      - id: ocmr_3$m
        call: 3$m
        priority: 52
        requires: { suits: { $m: [6, 13] }, evals: { total_points: [15, 40] } }
        shows: "competing to three of my own six-card minor"
        establishes: { forcing: non_forcing, agreed_suit: $m }
      - id: ocmr_pass_$m
        call: P
        priority: 50
        requires: {}
        shows: "partner's raise was competitive, not constructive: a minimum opening passes"
        establishes: { forcing: sign_off }
```

Note the deliberate omission: the context does **not** define 2NT, so `uc_nt2`
is still offered — it simply loses to a fit-1.00 pass at priority 50 instead of
winning by default.  That is the smallest possible subtraction.

**ANSWERING SEAT.**  `ocmr_3$m` is `non_forcing`; `ocmr_3NT_$m` is a contract.
Nothing new is asked, so no new answering seat is owed.

**What it endangers.**  `uc_pass` (18) — replaced by an identical floor;
`uc_nt2` (28) and `uc_nt3` (29) — outranked, which is the fix;
`uc_raise_C3`/`uc_rebid_C3` (27) — the 3m rung carries the better description
(six cards *and* extras) for the hands that should compete.

**VERIFIED.**  `P P 1C 1D 2C P` → **P** (`ocmr_pass_C`), replacing 2NT.  The
IMP gain is not guaranteed by this board's double-dummy sheet alone — 2C by S
is also five tricks — but passing hands the auction back to E/W, who hold the
13-count that balanced into 3D for -110 at the other table, and -110 rather
than -300 is where the five IMPs are.

**Template.** `expand: { m: [C, D] }`.  The major twin
(`1$M - act - 2$M - P - ?`) is a *different* agreement — a major fit is worth
competing — and should not be copied blind.

---

## Board 515 (and 885) — a limit raise on three ragged trumps

**Seat/call.** Board 515, table B call 2, seat E: `1S P`, hand
`743.A95.65.KQT43` — `r1S_limit_raise` (3+ spades, 10-13 support points, 8-11
HCP) fits **1.000** and we bid 3S; opener accepts and 4S is one off.  Board 885
is the same rung on `T987.QT.J98.AQJ7`.

**The missing agreement.**  A raise to three promises **either eleven high-card
points or an honour in the trump suit**.  Ten support points made of side-suit
honours opposite three or four ragged trumps is a *maximum single raise*: the
tenth point is a doubleton that will never ruff anything, and the trump suit
contributes nothing.

**YAML** (`resp_1S`; the `resp_1H` twin is identical with H for S):

```yaml
      # A raise to three promises a trump honour or eleven high-card points.
      # Additive: the limit raise keeps its whole band except the ragged 8-10
      # corner this rung describes better.
      - id: r1S_raise_ragged_S
        call: 2S
        priority: 61
        requires:
          suits: { S: [3, 13] }
          hcp: [8, 10]
          evals: { total_points: [10, 11], "suit_quality(S)": [0, 0.5] }
        shows: "maximum single raise: 10-11 support points but no honour in the trump suit"
        establishes: { forcing: non_forcing, agreed_suit: S }
      - id: r1S_limit_raise
        call: 3S
        priority: 62
        requires:
          suits: { S: [3, 13] }
          evals: { total_points: [10, 13] }
          hcp: [8, 11]
          not: { hcp: [0, 10], evals: { "suit_quality(S)": [0, 0.5] } }
        shows: "limit raise: 3+ spades, 10-13 support points, and either eleven HCP or a trump honour"
        establishes: { forcing: invitational, agreed_suit: S }
```

**ANSWERING SEAT.**  Both calls are already answered: `opener_after_limit_raise`
hears 3S, and `responder_rebid_after_1M_raise` (plus this file's new trial
bids) hears 2S.  The point of the change is precisely that a hand routed to 2S
now gets a *trial bid* rather than a blind accept — boards 515 and 938 are two
halves of the same agreement.

**What it endangers, and the two prototypes I threw away.**
* First attempt: widen `r1S_single_raise` to `total_points: [6, 10]`.  That
  moved a genuine limit raise (`T987.A95.A52.QT3`, 4 trumps) from 3S to 2S —
  reverted.
* Second attempt: an `any_of` with a `suits: { S: [3, 3] }` branch.  The
  length gate penalised four-trump hands and made it worse — reverted.
* Shipped version is a *new rung* plus a `not:` corner on the limit raise, so
  `r1S_single_raise` (60) is untouched, `r1S_1NT` (40) is untouched, and
  `r1S_jacoby_2NT` (90) / `r1S_splinter_*` (89) are far above and untouched.
  The subtraction is exactly the ragged 8-10 corner, by construction.

**VERIFIED.**  515: `1S P` → **2S** (`r1S_raise_ragged_S`).  885: `1S P` →
**2S**.  Regressions all held: `KJ8.A95.652.QT43` (trump honour, 10) → 3S;
`Q97.A95.652.KQT3` (11 HCP) → 3S; `T987.A95.652.QT3` (10, 4 ragged) → 2S;
`J43.A95.652.QT43` (weak) → 2S; and the heart twin `A95.743.65.KQT43` → 2H.

**Template.** One new rung and one `not:` clause in each of `resp_1S` and
`resp_1H`.  It should also be carried to `r1S_raise_passed`/`r1H_raise_passed`
(which are already capped at 2M) — no change needed there — and considered for
`jordan_raise`.

---

## Board 520 — NOTHING-WRONG (constructive)

**Seat/call.** Table B call 1, seat E: second-seat opening with
`T7.AT972.A76.QJ7` (11 HCP, rule of 20 = 11 + 5 + 3 = 19).  We pass; BEN opens
1H.

**What I checked.**  `open_1H` misses by one HCP (0.800) and `open_1H_rule20`
misses the rule-of-20 count (0.800); `open_pass` fits 1.00 at priority 20 and
wins on the fast path.  This is an opening threshold, scope-excluded.  The rest
of table B is a 1S overcall and a competitive 2NT.

**Verdict.** NOTHING-WRONG in my discipline.

---

## Board 585 — the penalty pass of a balancing double, and a NEGATIVE RESULT

**Seat/call.** Table A call 5, seat S: `1S P P X P`, hand `T982.AQ2.K84.AT8` —
13 HCP with **four spades sitting over the opener**.  We bid 2S
(`advbal_S_cue`, game forcing) and the pair then invented a suit a turn:
`3C 3D 3H 4H`, -50, where 1S doubled is two off for +300.

**The missing agreement.**  Four trumps behind a one-level opener, with
defensive values, is a penalty pass of partner's balancing double —
`advance_weak2_double_*` has one (`aw2S_pass_penalty`), the balancing family
never got one, and `adx_sit` demands a *quality* holding.

**Why the obvious version is wrong — reported as a negative result.**  My first
prototype put the penalty pass in `advance_balancing_double_S`.  It fires, but
that context **does not otherwise define `P`**, so defining it there shadowed
`general_pull_or_sit` entirely: on `T982.A92.K84.T84` the engine went from a
sound pass (`adx_pass_min`, fit 1.00) to **1NT**, because both of that
context's authored passes were blocked.  Adding a `requires: {}` floor pass did
not rescue it either — `score_candidates` drops a non-**discriminating** pass
whenever pass is forbidden, so the floor was never a candidate at all.  Both
halves reverted.

**Shipped version — additive, in the context that already defines `P`:**

```yaml
      # adx_sit demands a QUALITY holding (1.5) in their suit, so four small
      # trumps behind a one-level opener - the commonest penalty pass there
      # is - scored 0.33 and the hand invented an advance.  At the ONE level
      # four cards plus defensive values is the whole credential.
      - id: adx_sit_four
        call: P
        priority: 61.5
        when: { their_last_bid_suit: true, standing_bid_level: [1] }
        requires:
          evals: { standing_suit_length: [4, 13], total_points: [10, 40] }
        shows: "sitting the double at the one level: four trumps behind the opener and defensive values"
        establishes: { forcing: sign_off }
```

**ANSWERING SEAT.**  A pass ends the auction; nothing is owed.

**What it endangers.**  `adx_sit` (61) — same call, and my gate is the same
length requirement with the quality floor traded for a point floor and a level
restriction, so on the hands both describe the outcome is identical.
`advbal_$X_H`/`_D`/`_C` (54-57) and `advbal_$X_cue` (49) — all outranked, but
only when I hold four of their suit at the one level with 10+ points, which is
the one shape where advancing is wrong.  `standing_bid_level: [1]` keeps the
rung away from every higher-level double.

**VERIFIED.**  `1S P P X P` → **P** (`adx_sit_four`), replacing 2S.  1S
doubled is six tricks for declarer: +300 (they are vulnerable) instead of -50.
Regressions: `T982.A92.K84.T84` (8 HCP) still passes via `adx_pass_min`;
`32.A92.K843.T843` still advances 2D.

**Template.** Single rule in `general_pull_or_sit`, no expansion needed
(`standing_suit_length` is suit-agnostic).

---

## Board 661 — the doubler jumps to game opposite a FORCED advance

**Seat/call.** Table B call 6, seat W: `P 1D X P 1S P`, hand
`QT98.AKQ3.8.AQJ3` — 18 HCP, singleton diamond, four spades, 21 total points.
`uc_doubler_game_S` ("jump to game opposite the advance: **20+** with 4-card
support") fits 1.000 and we bid 4S, one off.  BEN bids 3S.

**The missing agreement.**  Advancer's cheapest suit at the one level is
**forced** and shows 0-8; twenty opposite it is an invitation, not a contract.
The ladder ran 2S (17-19) and then straight to game, so the jump raise — the
rung that actually describes 20-21 — was missing.

**YAML.**

```yaml
      - id: uc_doubler_game_$M          # band raised 20 -> 22
        call: 4$M
        priority: 35
        when: { partner_suit: $M, my_last_call_was_double: true, we_hold_contract: false }
        requires: { suits: { $M: [4, 13] }, evals: { total_points: [22, 40] } }
        shows: "jump to game opposite the FORCED cheapest advance: 22+ with 4-card support"
        establishes: { forcing: sign_off, agreed_suit: $M }
      - id: uc_doubler_jumpraise_$M
        call: 3$M
        priority: 34.5
        when: { partner_suit: $M, my_last_call_was_double: true, we_hold_contract: false,
                standing_bid_level: [1] }
        requires: { suits: { $M: [4, 13] }, evals: { total_points: [20, 21] } }
        shows: "jump raise of the forced advance: 20-21 with four-card support, invitational"
        establishes: { forcing: invitational, agreed_suit: $M }
```

**THE ANSWERING SEAT** — the jump raise is an invitation, so it ships with one:

```yaml
  - id: advancer_over_doubler_jump
    description: "Advancer answers the doubler's invitational jump raise of the forced advance"
    expand: { M: [H, S] }
    pattern: "... - X - P - 1$M - P - 3$M - P - ?"
    rules:
      - id: adj_accept_$M
        call: 4$M
        priority: 40
        requires: { suits: { $M: [4, 13] }, evals: { total_points: [7, 40] } }
        shows: "accepting: a maximum for the forced advance, with a fourth trump"
        establishes: { forcing: sign_off, agreed_suit: $M }
      - id: adj_decline_$M
        call: P
        priority: 38
        requires: {}
        shows: "declining: the advance was forced and this is the minimum it promised"
        establishes: { forcing: sign_off }
```

**What it endangers.**  Raising `uc_doubler_game_$M`'s floor from 20 to 22
subtracts exactly the 20-21 class, which the new rung catches one level lower.
`uc_doubler_raise_$M` (2$M, 34) keeps its 17-19 band underneath; the jump rung
sits at 34.5 between them and carries `standing_bid_level: [1]` so it can never
fire over a three-level advance (where `uc_doubler_game3_$M` already rules).
The answering context owns 4$M and P in that one shape; both rungs together are
total: one is `requires: {}`.

**VERIFIED.**  `P 1D X P 1S P` → **3S** (`uc_doubler_jumpraise_S`), and the
advancer's `J643.J54.9543.T4` → **P** (`adj_decline_S`).  3S by E makes nine
tricks: +140 to us instead of 4S one off.

**Template.** `expand: { M: [H, S] }` on all three pieces (the two rungs are
already written per suit in `general_uncontested_continuation`).

---

## Board 705 — NOTHING-WRONG (constructive)

**Seat/call.** Table A call 1, seat S: `1C`, hand `Q54.AJ63.K92.QT8` — a
4-3-3-3 twelve-count.  We pass; BEN doubles.

**What I checked.**  `oc1C_X` fits 0.349 (a takeout double wants shortness in
their suit and this hand has three clubs), `oc1C_1H` 0.349 (four hearts, not
five), `oc1C_1NT` 0.127 (15-18 needed).  Every rung correctly declines to
describe a flat twelve with three of their suit; whether to double anyway is a
style threshold, not a missing agreement, and takeout-double credentials are
recorded in `DECISIONS.md` as a settled system choice.

**Verdict.** NOTHING-WRONG in my discipline.

---

## Board 723 — the suit advances of a double all stop at eight points

**Seat/call.** Table A call 3, seat S: `2S X P`, hand `A94.A6.QT9542.T9` — ten
points and a **six-card** diamond suit.  Every suit advance in
`advance_weak2_double_S` is capped at 8 total points, and the only 9-11 rungs
are 2NT and a game jump in a major, so we bid **2NT** on a hand with two
doubletons and six diamonds.

**The missing agreement.**  A six-card suit with 9-13 opposite the double is
bid, not converted to notrump.

**YAML** (`advance_weak2_double_S`; the 2D and 2H twins are identical):

```yaml
      - id: aw2S_long3_D
        call: 3D
        priority: 59
        requires:
          suits: { D: [6, 13] }
          evals: { total_points: [9, 13] }
          not: { any_of: [ { suits: { H: [4, 13] } } ] }
        shows: "six-card diamond advance of the double, 9-13: the suit, not notrump"
        establishes: { forcing: non_forcing, agreed_suit: D }
      - id: aw2S_long3_C
        call: 3C
        priority: 59
        requires:
          suits: { C: [6, 13] }
          evals: { total_points: [9, 13] }
          not: { any_of: [ { suits: { H: [4, 13] } } ] }
        shows: "six-card club advance of the double, 9-13: the suit, not notrump"
        establishes: { forcing: non_forcing, agreed_suit: C }
```

**ANSWERING SEAT.**  `non_forcing` with `agreed_suit` set; the doubler's
existing raise ladder (`uc_doubler_raise_*`, and board 661's new jump raise)
reads it.  The `not:` clause preserves the system rule that a four-card major
is shown first, so the doubler's major-oriented rungs are not misled.

**What it endangers.**  `aw2S_3D`/`aw2S_3C` (57/58) keep their whole 0-8 band
underneath — additive.  `aw2S_2NT` (55) and `aw2S_cue` (54) are outranked only
by a genuine six-bagger with 9-13, which is exactly the hand type they describe
worst.  `aw2S_4H` (60) still outranks me, correctly: a four-card major and
game values comes first.

**VERIFIED.**  `2S X P` → **3D** (`aw2S_long3_D`), replacing 2NT.

**Template.** Two rules in each of `advance_weak2_double_D`, `_H` and `_S`
(six rules), with the `not:` clause naming whichever majors are still unbid.

---

## Board 755 — responder over opener's 1NT rebid after a negative double

**Seat/call.** Table A call 7, seat S: `P 1D 1H X P 1NT P`, hand
`QJ43.T82.KT87.87` (6 HCP) — we bid **2D** (`uc_raise_D2`, generic).  Partner's
1NT is a *contract*; pulling it to two of his minor with a balanced six-count
converts a plus into a minus, and the seat is unauthored.

**The missing agreement.**  After opener's 1NT rebid over the negative double,
notrump is our partscore: responder passes with a minimum, invites with 9-10
and bids game with 11+.  Nothing is corrected to a minor.

**YAML.**

```yaml
  - id: responder_over_1NT_rebid_after_negative_double
    description: "Responder over opener's 1NT rebid after the negative double"
    expand_pairs:
      - { m: C, M: H }
      - { m: D, M: H }
      - { m: C, M: S }
      - { m: D, M: S }
    pattern: "1$m - 1$M - X - P - 1NT - P - ?"
    rules:
      - id: rnd1n_3NT_$M
        call: 3NT
        priority: 56
        requires: { hcp: [11, 40] }
        shows: "game opposite the 12-14 notrump rebid"
        establishes: { forcing: sign_off }
      - id: rnd1n_2NT_$M
        call: 2NT
        priority: 54
        requires: { hcp: [9, 10] }
        shows: "invitational opposite the 12-14 notrump rebid"
        establishes: { forcing: invitational }
      - id: rnd1n_pass_$M
        call: P
        priority: 50
        requires: {}
        shows: "notrump is our best partscore: a minimum negative double has nothing to correct to"
        establishes: { forcing: sign_off }
```

**THE ANSWERING SEAT** for `rnd1n_2NT_$M`: `opener_over_invite_2NT_after_2suits`
does not match this pattern, so the invitation needs
`"1$m - 1$M - X - P - 1NT - P - 2NT - P - ?"` with a 3NT accept (`hcp:
[13, 14]`) and a `requires: {}` pass.  As on boards 151 and 300, the pass rung
alone is the board's gain and is safe shipped by itself.

**What it endangers.**  `uc_raise_D2` (30), `uc_nt2` (28), `uc_nt3` (29) and
`uc_pass` (18) in this one seat.  All four are the generic ladder treating
opener's 1NT as a suit bid.  The 2NT/3NT rungs are strictly more descriptive
than `uc_nt2`/`uc_nt3` here because the *combined* range is known.

**VERIFIED.**  `P 1D 1H X P 1NT P` → **P** (`rnd1n_pass_H`), replacing 2D.

**Template.** Four-way `expand_pairs` as written.

---

## Board 838 — a NEGATIVE RESULT: "open the longer minor" cannot be a gate alone

**Seat/call.** Table A call 0, seat S: opening with `AK953.J9.QJT964.` — five
spades, **six** diamonds, 11 HCP.  We open 1S (`open_1S_rule20`); BEN opens 1D.

**The agreement is right.**  With a five-card major and a longer minor, open
the minor and bid the major next: it is the textbook treatment and it is what
BEN does.  This is a *suit-selection* rule, not one of the opening-strength
thresholds `DECISIONS.md` rules out.

**What I tried and what it did.**  Adding the shape denial

```yaml
          not: { suits: { S: [5, 5] }, any_of: [ { suits: { D: [6, 13] } }, { suits: { C: [6, 13] } } ] }
```

to `open_1S`/`open_1S_rule20` makes the hand **pass**, not open 1D:
`open_1D` requires "no 5-card major" and `open_1m_rule20` fits 0.100, so
subtracting 1S subtracts the opening altogether.  Traced: `AK953.J9.QJT964.` →
**P**.  Reverted.

**What the shipped version would have to be** (I am not proposing it without
measurement, because it touches the busiest context in the file): the denial
above **plus** a matching pair of rungs in `openings` —

```yaml
      - id: open_1D_five_four_major
        call: 1D
        priority: 74.5
        requires:
          suits: { D: [6, 13], S: [5, 5] }
          evals: { rule_of_20: [20, 33] }
        shows: "six diamonds longer than the five-card major: open the longer suit and bid the major next"
        establishes: { forcing: one_round }
```

and its C/H permutations.  That is four rungs plus two gates in `openings`,
which is a subject of its own.

**Verdict:** negative result reported, not shipped.  Board 838's constructive
content is exhausted by it; the rest of both auctions is competitive.

---
## Board 871 — a negative double on a six-card suit

**Seat/call.** Table A call 3, seat S: `P 1D 1S`, hand `95.AJ6542.K7.J87` —
**six** hearts, 9 HCP.  `nx_1m1S_X` ("negative double: 4+ hearts, 6+ HCP")
fits 1.000 at priority **80**; the free bid `nx_1m1S_2H` needs 10 (fit 0.800)
and the weak jump `nx_1m1S_wj_H` sits at 56.  The double is a lie about the
hand and the auction wandered `2D 2H 3D 3H 4D`, -100.

**The missing agreement.**  A negative double promises *four* hearts and asks
partner to choose; with six it is the wrong bid at any strength.  The free bid
at the two level needs only eight points when the suit is six long.

**YAML** (`resp_1m_over_1S`, above the double):

```yaml
      - id: nx_1m1S_long2_H
        call: 2H
        priority: 81
        requires: { suits: { H: [6, 13] }, hcp: [8, 15] }
        shows: "six-card heart suit, 8-15: the suit, not the negative double"
        establishes: { forcing: one_round }
```

**THE ANSWERING SEAT.**  `forcing: one_round`, matching `nx_1m1S_2H`
immediately below it, so opener's existing answering ladder
(`opener_over_negative_double` is not reached; the free-bid answer is the
generic continuation) reads it exactly as it reads the 10+ version.  I am
deliberately keeping the two rungs' `establishes` identical so no new seat is
created.

**Why this is not the excluded "a double must not hide a six-card suit".**
That entry in `DECISIONS.md` is about **takeout** doubles and was killed with
whole-corpus data; and round 14 killed a **cap** on `nxj_X`.  This is the
additive half: it adds a rung that describes the hand, rather than gating the
double.  On every hand *without* six hearts `nx_1m1S_X` keeps its whole band.

**What it endangers.**  `nx_1m1S_X` (80) on six-card-heart hands with 8-15 —
intended.  `nx_1m1S_2H` (78) becomes redundant on the 10-15 six-card overlap;
identical call, identical forcing, so nothing changes there.
`nx_1m1S_wj_H` (56, weak jump, "less than a free bid") keeps every hand below
eight points.

**VERIFIED.**  `P 1D 1S` → **2H** (`nx_1m1S_long2_H`), which is BEN's call.

**Template.** The twin `nx_1m1H_long2_S` in `resp_1m_over_1H` — but note that
over 1H the spade bid is at the **one** level, so the rung is
`call: 1S, priority: 79` above `nx_1m1H_X` at 80... which means the twin needs
its priority set to 81 as well.  Both contexts, two rules.

---

## Board 885 — see board 515

The first divergence is table B call 2, seat W: `1S P` with
`T987.QT.J98.AQJ7`, and it is the *same* rung and the *same* agreement as board
515 — a limit raise on four ragged trumps and ten flat points.  With
`r1S_raise_ragged_S` in place the hand bids **2S** instead of 3S
(**VERIFIED**), which is where the opponents' 4H then wins the auction cheaply
instead of pushing us to 4S down one.

No separate proposal.

---

## Board 926 — the sandwich double outranks a good five-card major

**Seat/call.** Table B call 3, seat E: `1C P 1S`, hand `K92.AQT84.K985.K` —
15 HCP with **AQT84** of hearts.  `sw_X` (prio 70) beats `sw_2H` (66) and we
double; partner bids the wrong thing and the auction runs to 3H, +100 to them.

**The missing agreement.**  In the sandwich seat a good five-card major with
opening values is *bid*.  A double there says "both unbid suits" and puts
partner in charge of a hand that already knows its own trump suit.

**YAML** (`sandwich_seat`):

```yaml
      - id: sw_2H_strong
        call: 2H
        when: { unbid_suit: H }
        priority: 71
        requires: { suits: { H: [5, 13] }, hcp: [13, 17], evals: { "suit_quality(H)": [2.5, 9] } }
        shows: "sandwich overcall: a good five-card heart suit with 13-17 - bid it, do not double"
        establishes: { forcing: non_forcing }
      - id: sw_2S_strong
        call: 2S
        when: { unbid_suit: S }
        priority: 71
        requires: { suits: { S: [5, 13] }, hcp: [13, 17], evals: { "suit_quality(S)": [2.5, 9] } }
        shows: "sandwich overcall: a good five-card spade suit with 13-17 - bid it, do not double"
        establishes: { forcing: non_forcing }
```

**ANSWERING SEAT.**  `non_forcing` natural overcall; `advance_overcall` and the
`advsw_*` family already answer a sandwich two-level bid.  Nothing new is
asked.

**What it endangers.**  `sw_X` (70) only on hands holding a *good* five-card
unbid major with 13-17 — the quality floor of 2.5 means two of the top three
honours or better, so a ragged five-bagger still doubles.  `sw_2H` (66) keeps
its whole 11-17 band underneath: additive.  `sw_2H_jump` (69) requires six
cards and 5-10 and is untouched.

**VERIFIED.**  `1C P 1S` → **2H** (`sw_2H_strong`), which is BEN's call
(0.97).

**Template.** Two rules as written; the minors deliberately excluded — a
five-card minor in the sandwich seat is not worth pre-empting the double.

---

## Board 64 — NOTHING-WRONG (constructive)

**Seat/call.** Table A call 2, seat S: `P 1D`, hand `AK9865.T97.J.Q43` — we
overcall 1S (`oc1D_1S`, fit 1.000, prio 71); BEN jumps to 2S (`oc1D_2S_jump`
also fits 1.000, prio 60).

**What I checked.**  Both calls fit perfectly and the choice is settled by
priority.  **Re-ranking the weak jump overcall is on the do-not-re-propose
list**, with the number that killed it: round 11 measured -24 held out, and the
recorded reason is that on the 8-10 overlap the one-level call is better.  This
hand is a 10-count.  Nothing in the constructive machinery is consulted; table
B is a negative double of a jump overcall.

**Verdict.** NOTHING-WRONG.

---

## Board 119 — a "natural" notrump over their natural notrump

**Seat/call.** Table B call 4, seat W: `P P 1C 1NT`, hand `J82.AK5.QJ642.84`
— we bid **2NT** (`cl_nt2`, "natural 2NT: 11-12 balanced with a stopper in
their suit").  Over a *natural 15-18 notrump overcall* there is no such bid:
partner opened, they showed 15-18, and 11-12 balanced opposite that is a
partscore hand with nowhere to go.

**The missing agreement.**  The natural notrump rungs describe a notrump
*contract* opposite a suit contract; they are meaningless when the standing bid
is already notrump.

**YAML** (`general_competitive_low`):

```yaml
      - id: cl_nt2
        call: 2NT
        priority: 28
        when: { side_has_acted: true, standing_bid_strain: [C, D, H, S] }
        requires:
          hcp: [11, 12]
          evals: { weakest_their_stopper: [0.9, 9], rule_of_26: [22, 99], semi_balanced: [1, 1] }
        shows: "natural 2NT: 11-12 balanced with a stopper in their suit"
        establishes: { forcing: non_forcing }
```

**ANSWERING SEAT.**  None — this removes a call rather than adding one.

**What it endangers, stated plainly.**  This is a **gate** and it subtracts
`cl_nt2` in every seat where the standing bid is notrump.  That is exactly the
population it should not be describing, and the hands land on the natural suit
rungs (`cl_new_D2` and friends) or on `cl_pass`, all of which are still
offered.  I would *not* extend it to `cl_nt3` without measurement: 3NT over
their notrump overcall can be a genuine contract when partner has opened and I
hold a source of tricks.  `cl_nt2_direct` (37) already carries
`their_last_bid_suit: true` and is untouched.

**VERIFIED.**  `P P 1C 1NT` → **2D** (`cl_new_D2_hi`), replacing 2NT.  BEN
doubles; 2D is at worst a partscore and 2NT was the losing call.  The corpus
replay shows this gate is one of the wider-reaching items in the batch (it also
moves boards 216 and 94), so it is the one I would screen **on its own** rather
than inside a batch.

**Template.** One rule.  `cl_nt1` deserves the same treatment and `uc_nt2`
probably does too, but `uc_nt2` is an open item with its own history and I am
not touching it here.

---

## Board 182 — NOTHING-WRONG (constructive)

**Seat/call.** Table A call 8, seat S: `P P P 1D P 1H P 1NT`, hand
`AT9.J62.JT.KT983` — we bid 2C in the pass-out seat over their constructive
1NT rebid, -100.

**What I checked.**  `cl_new_C2_hi` and `cl_new_C2` both fit **1.000**: five
clubs and ten points is exactly what they describe.  The bid is wrong for a
reason the rule cannot see — my partner has passed three times, so ten points
opposite a passed hand facing a 12-14 opener is a defence, not a competition.
The condition "partner has passed throughout" is expressible
(`when: { partner_has_acted: false }`), but the only additive rung it supports
is a **pass at priority 27**, which would outrank every `cl_new_*2` rung in the
very large population of seats where our side has acted and partner has not —
including every legitimate second-round overcall.  I am not proposing a rung
whose blast radius I cannot bound, and the constructive rungs themselves are
correctly written.

**Verdict.** NOTHING-WRONG; the live question is a balancing/competitive
threshold.

---

## Board 235 — a 1NT response holding six of their suit

**Seat/call.** Table B call 2, seat E: `1D 1H`, hand `KT2.Q98543.84.J6` —
**six hearts**, 6 HCP.  `nx_1m1H_1NT` ("6-10 with a heart stopper") fits
1.000, because `stopper(H)` scores Q98543 as a full stopper.  We bid 1NT with
six of their suit and no other feature.

**The missing agreement.**  A natural 1NT over their overcall shows a
*balanced-ish* hand with a guard; six cards in their suit is a trump stack, not
a stopper, and with six points there is nothing to say.

**YAML** (`resp_1m_over_1H`; the 1S twin is identical):

```yaml
      - id: nx_1m1H_1NT
        call: 1NT
        priority: 50
        requires: { hcp: [6, 10], features: [ "stopper(H)" ], suits: { H: [0, 3] }, not: { suits: { S: [4, 13] } } }
        shows: "6-10 with a heart stopper and at most three of their suit"
        establishes: { forcing: non_forcing }
```

**ANSWERING SEAT.**  Unchanged — the hand lands on `nx_1m1H_pass`, which is
already authored.

**What it endangers.**  A length cap is a **gate** and it subtracts exactly one
class: 6-10 hands with four or more of their suit that used to bid 1NT.  Those
hands pass (`nx_1m1H_pass`, fit 1.000), which is right — and the length gate is
*sharp* (`_S2_SUIT = 0.95`), which matters because
`weakest_their_stopper`/`stopper` famously are not.  This is the honest way to
get a stopper gate to bite without touching the evaluator, which round 8
measured at -9 held out.

**VERIFIED.**  `1D 1H` → **P** (`nx_1m1H_pass`), which is BEN's call (0.99).

**Template.** Two rules (`nx_1m1H_1NT`, `nx_1m1S_1NT`); `nx_1m1H_2NT` and
`nx_1m1H_3NT` deserve the same cap and would be part of the same agreement.

---

## Board 243 — six cards is its own credential over their 1NT

**Seat/call.** Table A call 1, seat N: `1NT`, hand `Q32.AT8763.K86.7` — six
hearts, 9 HCP, a singleton club.  `v1NT_2H` requires
`features: [ "good_suit(H)" ]`, AT8763 is neither two of the top three nor
three of the top five, and a feature miss is a flat **0.2 multiplier** — so the
rule scores 0.200 and we pass out their 1NT.

**The missing agreement.**  Over their 1NT a six-card suit with a singleton is
worth a two-level bid on its length; the quality floor belongs on the *five*-
card version, which is the one that needs it.

**YAML** (`defense_vs_1NT`):

```yaml
      - id: v1NT_long2_H
        call: 2H
        priority: 60.5
        requires: { suits: { H: [6, 13] }, hcp: [7, 15] }
        shows: "natural: a six-card heart suit, 7-15"
        establishes: { forcing: non_forcing }
      - id: v1NT_long2_S
        call: 2S
        priority: 60.5
        requires: { suits: { S: [6, 13] }, hcp: [7, 15] }
        shows: "natural: a six-card spade suit, 7-15"
        establishes: { forcing: non_forcing }
```

**ANSWERING SEAT.**  `advance_1NT_overcall` is the wrong context (that answers
*our* 1NT overcall); a natural two-level bid over their 1NT is answered by the
generic competitive ladder, which already reads a `non_forcing` suit bid.
Nothing new is asked, so nothing new is owed.

**What it endangers.**  `v1NT_2H` (61) keeps its whole band and stays above the
new rung, so a good five-or-six-card suit is unaffected; the new rung only
catches the hands the feature multiplier was silencing.  `v1NT_pass` (30) is
outranked on six-card hands — intended.  `v1NT_X` (70, penalty, 15+) is far
above and untouched.

**VERIFIED.**  `1NT` → **2H** (`v1NT_long2_H`), replacing pass.

**Template.** Two rules as written; the minor twins (`v1NT_2C`/`2D`, both
`6+` already) should get the same 7-point floor rather than 8.

---

## Board 419 — NOTHING-WRONG (constructive)

**Seat/call.** Table A call 3, seat S: `1D P P`, hand `6532.K52.KJT8.A4` — we
bid the balancing 1NT (`bal_1NT`, 11-14 with a stopper, fit 1.000); BEN
doubles.

**What I checked.**  `bal_X` scores 0.028 because a balancing takeout double
wants shortness in their suit and this hand holds **four** diamonds — the gate
is doing exactly the right thing.  `bal_D_1S` fits 0.349 (four spades, not
five).  With four of their suit and a flat 11-count, 1NT is the system's
answer and it is a defensible one.  Table B's divergence is `uc_raise_H2` in a
competitive auction.

**Verdict.** NOTHING-WRONG in my discipline.

---

## Board 458 — a good five-card suit outranked by a bid that describes nothing

**Seat/call.** Table A call 4, seat S: `P P 1C 2H`, hand `KJ6.A9.QJT83.853` —
**`nxj_X`**, "negative double of the jump overcall: 8+ HCP, no shape shown",
priority **70**, fit 1.000.  BEN bids 3D.  Partner then bid the spades the
double implied and we ended in 2NT, -100.

**The missing agreement.**  A good five-card suit at the three level is a
description; a double that promises eight points and nothing else is not.  With
a real suit and no four-card unbid major, bid the suit.

**YAML** (`neg_double_3level_M`'s two-level sibling context, above `nxj_X`):

```yaml
      - id: nxj_new_D3
        call: 3D
        priority: 71
        when: { unbid_suit: D, cheapest_in_suit: true }
        requires:
          suits: { D: [5, 13] }
          hcp: [10, 15]
          evals: { "suit_quality(D)": [2, 9] }
          not: { any_of: [ { suits: { H: [4, 13] } }, { suits: { S: [4, 13] } } ] }
        shows: "natural: a good five-card diamond suit with 10-15 - the suit, not a shapeless double"
        establishes: { forcing: one_round }
      - id: nxj_new_C3
        call: 3C
        priority: 71
        when: { unbid_suit: C, cheapest_in_suit: true }
        requires:
          suits: { C: [5, 13] }
          hcp: [10, 15]
          evals: { "suit_quality(C)": [2, 9] }
          not: { any_of: [ { suits: { H: [4, 13] } }, { suits: { S: [4, 13] } } ] }
        shows: "natural: a good five-card club suit with 10-15 - the suit, not a shapeless double"
        establishes: { forcing: one_round }
```

**THE ANSWERING SEAT.**  `forcing: one_round`, which is what `nxj_X` and
`cl_new_D3` already establish, so opener's existing continuation reads it.  I
deliberately did not make it game-forcing precisely so that no new seat is
created — round 13's "the forcing new suit opposite a weak two is passed out"
is the failure mode I am avoiding.

**Why this is not the reverted round-14 fix.**  Round 14 measured a **cap** on
`nxj_X` (a longest-suit ceiling plus a four-card-unbid-major requirement) at
-5 held out, and the recorded reason is that *two of the nine replacement calls
score below the 0.9 fast path*, i.e. the landing seats were unauthored.  This
proposal is the opposite move: it authors one of those landing calls, at a
priority that only takes the hands it actually describes, and leaves `nxj_X`'s
band completely intact.

**What it endangers.**  `nxj_X` (70) on 10-15 hands with a good five-card
minor and no four-card unbid major — the `not:` clause is what preserves the
double's real job.  `cl_new_D3`/`cl_new_D3_hi` (27/27.5) and
`cl_new_long3_D` (27) are all below and are describing the same hand less well;
`cl_raise_C3` (31) requires club support and is untouched.

**VERIFIED.**  `P P 1C 2H` → **3D** (`nxj_new_D3`), which is BEN's call.

**Template.** Two rules per level; the same pair belongs in
`neg_double_3level_m` for a jump to the three level.

---

## Board 549 — a three-card raise of the overcall with 4-3-3-3 shape

**Seat/call.** Table A call 5, seat S: `P P 1C 1D X`, hand `KT7.K932.987.K72`
— `xd_raise_D2` ("raise of partner's doubled D: 3+ trumps, 6-9 support
points") fits 1.000 and we raise; BEN passes.  2D is one off where passing is
+100 or better.

**The missing agreement.**  A raise of partner's one-level overcall through
their negative double is a Law bid: it needs a ruffing value.  With three
trumps and 4-3-3-3 shape there is no ruff to take and no extra trick to win —
the raise buys nothing and hands them a target.

**YAML** (`general_their_double`; the same clause on all four suits):

```yaml
      - id: xd_raise_D2
        call: 2D
        priority: 30
        when: { we_bid_last: true, we_hold_contract: false, partner_suit: D, cheapest_in_suit: true }
        requires:
          suits: { D: [3, 13] }
          evals: { total_points: [6, 9], "lott_total_trumps(D)": [7, 26] }
          not: { suits: { D: [3, 3] }, evals: { balanced: [1, 1] } }
        shows: "raise of partner's doubled D: 3+ trumps with a ruffing value, or four trumps, 6-9 support points"
        establishes: { forcing: non_forcing, agreed_suit: D }
```

**ANSWERING SEAT.**  None owed — the change removes a call.  The hand lands on
`xd_pass`, which is authored and fits 1.000.

**What it endangers.**  A **gate**: exactly-three-card raises from 4-3-3-3 and
5-3-3-2-with-three-trumps hands (the `balanced` evaluator has sharp tolerance,
`_EVAL_S2["balanced"] = 0.08`, so the `not:` really bites and does not leak).
Those hands pass instead.  Four-card raises, three-card raises with a doubleton
or a singleton, and `xd_jumpraise_$X3` are all untouched.

**VERIFIED.**  `P P 1C 1D X` → **P** (`xd_pass`), which is BEN's call (0.90).

**Template.** Four rules (`xd_raise_C2`/`D2`/`H2`/`S2`), which is where I
applied it; the three-level twins `xd_raise_*3` should get it too.

---

# Blast radius, measured

`decide_fast` was replayed over **all 10,335 of our decisions** in
`reports/r18_before.jsonl` under the stock system and under a scratch copy
carrying **every** proposal in this file:

| | value |
|---|---|
| decisions replayed | 10,335 |
| decisions changed | **87 (0.84 %)** |
| contexts | 517 → 564 |
| rules | 2,344 → 2,523 |
| `lint_system.py` findings | 223 → **222** |

The intermediate measurements are worth recording because they show where the
mass is:

| batch | changed decisions |
|---|---|
| trial bids + 1M-1NT-2M + 1M-1NT-2S + jump shift + ragged raise + 2/1 gate | 27 (0.26 %) |
| \+ six-five, solo four-level rebid, `omrp_pass`, `onx_jumpmajor` | 39 (0.38 %) |
| \+ `answer_raise_invitation`, `our_agreed_partscore_doubled` | 45 (0.44 %) |
| \+ everything else in this file | **87 (0.84 %)** |

Two contexts in the batch account for a disproportionate share of the tail and
should be **screened on their own** rather than inside a subject batch:
`cl_nt2`'s `standing_bid_strain` gate (board 119) and
`our_agreed_partscore_doubled` (board 84), both of which reach auctions well
outside the boards that motivated them.

A sample of the changed decisions, as `(board, table, call index, seat, base
call, new call, auction)` — the first thirty of 87:

```
(  4,b, 9,E,'4H','P'  ,'P 1C 1D 1H P 2H P 3H P')      (261,a, 5,S,'4H','P'  ,'2D X P 3H P')
( 30,b, 3,E,'3S','2S' ,'P 1S P')                       (269,b,10,W,'P' ,'4C' ,'P 1D 2C 2S P 2NT 3C 3NT P P')
( 40,a, 4,N,'4H','3C' ,'1H P 1NT P')                   (271,b, 6,E,'2C','3C' ,'P P 1S P 1NT P')
( 49,a, 5,S,'P' ,'4H' ,'P 1H 3S P P')                  (290,a, 2,N,'P' ,'2S' ,'P 1NT')
( 54,b, 9,W,'P' ,'4S' ,'P 1S 2H P 2NT 3S 4H P P')      (291,b, 6,E,'2NT','P' ,'1D P 1S P 2D P')
( 62,a,10,N,'3S','P'  ,'P P 1D P 1S P 2D P 2S P')      (293,a, 9,S,'4H','P'  ,'P P 2D X 3D X P 3H P')
( 84,a, 8,N,'2S','P'  ,'1D P 1H P 2H P P X')           (300,a, 8,N,'2NT','P' ,'1H P 1S P 1NT P 2S P')
( 93,b, 2,W,'P' ,'2S' ,'P 1NT')                        (348,a, 2,S,'2C','2NT','1D P')
( 94,b, 5,W,'1NT','P' ,'P 1C 1S X P')                  (350,a,10,N,'P' ,'3H' ,'P 1D 1H P 1NT X 2H P P X')
( 97,b, 4,E,'2H','P'  ,'P 1C 1H X')                    (357,b,14,W,'P' ,'4H' ,'P 1C 1H X P 2C 2H 3C P P 3H 4C P P')
(119,b, 4,W,'2NT','2D','P P 1C 1NT')                   (216,a, 2,S,'1NT','2D','1C 1S')
(123,a, 1,N,'P' ,'2H' ,'1NT')                          (228,b,11,W,'P' ,'4D' ,'1C P 1NT 2D 3C P P 3D 4C P P')
(151,a, 9,N,'3S','P'  ,'P 1C P 1S P 2C P 2S P')        (235,b, 2,E,'1NT','P' ,'1D 1H')
(203,b, 6,E,'3S','3C' ,'P P 1S P 2S P')                (243,a, 1,N,'P' ,'2H' ,'1NT')
(258,b, 5,W,'P' ,'4S' ,'2D 2S 4D P P')
```

Two of these deserve a second look from whoever consolidates: **board 54**
(`P 1S 2H P 2NT 3S 4H P P` → 4S) and **board 258** (`2D 2S 4D P P` → 4S) are
both the six-five rung (board 870) firing at the four level in a competitive
auction, which is where its `total_points: [13, 40]` floor is doing all the
work.  If any single rung in this file wants its own screen, it is that one.

## Recommended shipping order, by confidence

1. **The four empty answering seats** — boards 300, 151, 508, 4.  Each is a
   two-rule context with a `requires: {}` floor, each replaces a generic rung
   bidding over a sign-off, and together they are 4 of the 27 decisions in the
   first batch.  Lowest risk in the file.
2. **The trial-bid conversation** (938) with `responder_over_trial`, and the
   `1M - 1NT - 2M` conversation (809) with its answering seat.  These are the
   two closed conversations and the two largest additions.
3. **The ceilings**: 387 (jump shift), 49 (solo four-level rebid), 723, 243,
   871, 19.  All additive, all one rung.
4. **The gates**, each on its own: 515/885 (ragged raise), 942 (flat twelve),
   235 (length cap), 549 (ruffing value), 119 (`cl_nt2` strain).
5. **Not shipped, reported as negatives**: mini-splinters (209) and
   "open the longer minor" (838).
