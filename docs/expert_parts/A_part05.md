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

## Board 784 — -6; table A, call 4, N passes their 2NT overcall holding five spades

`P P 1D (2NT) — ?`, N `97642.KQ6.A.Q986`, 11 HCP.  4S by N is cold (11 tricks,
par +450); we defended 3C for +200 and lost 6.  Every 3S rung misses: 5-card
`cl_new_S3` wants 14+ total points (N has 12) **and** `suit_quality(S) >= 1.5`
(97642 scores **0.0**), `cl_new_long3_S` wants six.  Hole -> `cl_pass` at fit 1.00.

**Missing agreement.**  When they overcall two notrump they have located eleven
of their cards in two suits, so an unbid major at the three level is where our
fit is and it needs neither extra values nor a good suit.

**YAML** — context `general_competitive_low`, insert before `cl_nt1`:

```yaml
      - id: cl_free_major3_over_nt_S
        call: 3S
        priority: 28.5
        when: { unbid_suit: S, cheapest_in_suit: true, side_has_acted: true,
                i_have_acted: false, standing_bid_strain: [NT], standing_bid_level: [2] }
        requires:
          suits: { S: [5, 13] }
          evals: { total_points: [8, 40] }
        shows: "natural spades over their two-suited notrump overcall: 5+ cards, 8+ points, no suit-quality test"
        establishes: { forcing: non_forcing }
      - id: cl_free_major3_over_nt_H
        call: 3H
        priority: 28.5
        when: { unbid_suit: H, cheapest_in_suit: true, side_has_acted: true,
                i_have_acted: false, standing_bid_strain: [NT], standing_bid_level: [2] }
        requires:
          suits: { H: [5, 13] }
          evals: { total_points: [8, 40] }
        shows: "natural hearts over their two-suited notrump overcall: 5+ cards, 8+ points, no suit-quality test"
        establishes: { forcing: non_forcing }
```

**Answering seat.**  None owed — `forcing: non_forcing`, and partner's next
turn is already served by the `uc_raise_$M*` / `cl_raise_$M*` ladders.

**Endangers.**  Priority 28.5 sits between `cl_nt3` (29) and the natural-suit
ladder.
* `cl_new_S3` / `_hi` / `cl_new_long3_S` / `_hi` (27, 27.5) — same call; my
  `when` is a strict SUBSET of theirs, so 3S was already covered and no code
  fallback is deleted, and mine is the better description because over a
  two-suited overcall the suit's LENGTH is the asset, not its texture.
* `cl_new_C3` / `D3` (27, 27.5) — a five-card major outranks a minor here
  because they have shown the minors.
* `cl_nt1` (27, call 1NT) — not legal over 2NT.
* `cl_pass` (20) — passing with five of an unbid major over a two-suiter is
  how +450 becomes +200.
* Above it and untouched: `cl_nt3` (29) keeps 3NT with a real double stopper,
  `cl_rebid_*3` (29), `cl_raise_*3` (31), `cl_negative_X` (33), `cl_takeout_X`
  (36).

**VERIFIED.**  base `P [cl_pass] fit=1.00 p=20` -> patched
`3S [cl_free_major3_over_nt_S] fit=1.00 p=28.5`.

**Template.**  The agreement is `expand: { M: [H, S] }`, but
`general_competitive_low` carries no `expand:`, so it must be written out twice
as above.  If the consolidator prefers templating, the two rungs move into a
new templated context — but only one whose pattern is LESS specific than
`... - bid<3C - ?`, because `covered` is per-context and a later same-specificity
context would be shadowed for 3S.

---

## Board 809 — -6; table A, call 11, N passes their 2S holding a doubleton in partner's six-card suit

`P 1H P 1NT P 2H P P (X) P (2S) — ?`, N `T8.T3.AQ32.AT864`.  N/S make **ten**
tricks in hearts; we defended 2S for -140.  `cl_raise_H3` fits 0.349 for one
reason only: it demands `suits: { H: [3, 13] }` and N has two.  Measured at the
seat: `lott_total_trumps(H) = 8`, `partner_shown_length(H) = 6`,
`total_points = 11`.

**Missing agreement.**  Once partner has PROMISED six cards a doubleton is
three-card support by the Law, so the competitive raise to three needs eight
combined trumps, not three of my own.

**YAML** — context `general_competitive_low`, before `cl_nt1`:

```yaml
      - id: cl_raise_lott_short_H
        call: 3H
        priority: 31.5
        when: { partner_suit: H, cheapest_in_suit: true }
        requires:
          suits: { H: [2, 13] }
          evals: { "partner_shown_length(H)": [6, 13], "lott_total_trumps(H)": [8, 26],
                   total_points: [8, 40] }
        shows: "Law raise to three with a doubleton: partner has promised six hearts, so two is support"
        establishes: { forcing: non_forcing, agreed_suit: H }
      - id: cl_raise_lott_short_S
        call: 3S
        priority: 31.5
        when: { partner_suit: S, cheapest_in_suit: true }
        requires:
          suits: { S: [2, 13] }
          evals: { "partner_shown_length(S)": [6, 13], "lott_total_trumps(S)": [8, 26],
                   total_points: [8, 40] }
        shows: "Law raise to three with a doubleton: partner has promised six spades, so two is support"
        establishes: { forcing: non_forcing, agreed_suit: S }
```

**Answering seat.**  None owed — non-forcing, and it agrees the suit, so
partner's continuations run through the existing agreed-suit machinery.

**Endangers.**
* `cl_raise_H3` / `S3` (31) — same call, and my `when` is identical, so nothing
  new is covered and no fallback dies; mine is the better description because it
  says WHY two trumps are enough (partner promised six) instead of pretending to
  three.
* `cl_new_H3` / `cl_rebid_H3` (27, 29) — mutually exclusive `when` (`unbid_suit`
  / `my_suit` versus `partner_suit`).
* `cl_pass` (20) — passing an eight-card fit out at the two level is the loss.
* Above it and untouched: `cl_raise_lott3_$M` (32), `cl_raise_$M4` (32),
  `cl_doubler_raise3` (33), `cl_negative_X` (33).  A hand good enough for the
  four level still finds it.

**VERIFIED.**  base `P [cl_pass] fit=1.00 p=20` -> patched
`3H [cl_raise_lott_short_H] fit=1.00 p=31.5`.

**Template.**  `expand: { M: [H, S] }` in spirit; written out twice because
the context is untemplated.  The same pair belongs in
`general_competitive_high`, `general_balancing_low` and `general_balancing_high`
(`ch_`/`ballow_`/`balhigh_` prefixes, same bodies) — eight rungs in all.  I did
not ship those three pairs because none of the 38 boards exercises them; they
are the obvious sibling completion.

---

## Board 870 — -6; table A, call 8, S rebids 4H on a 6-5 hand over their 4C

`1H (2C) 2D (3C) 3H (P) P (4C) — ?`, S `AJ943.AQ8543.94.`, 11 HCP, 6-5 in the
majors.  4H is down one (-100); **4S makes ten tricks** (+420 available).
`ch_rebid_H4` fits 1.00 at 29 and buries `ch_new_S4` (28) / `_hi` (28.5).

**Missing agreement.**  Six-five come alive: with six of one suit and five of
another, show the second suit rather than repeating the first, because partner
can choose and cannot otherwise know.

**YAML** — context `general_competitive_high`, insert before `ch_pass`:

```yaml
      - id: ch_second_suit_65_S
        call: 4S
        priority: 29.5
        when: { my_suit: H, unbid_suit: S, cheapest_in_suit: true }
        requires:
          suits: { S: [5, 13], H: [6, 13] }
          evals: { total_points: [12, 40] }
        shows: "six-five come alive: six hearts and five spades, showing the second suit instead of repeating the first"
        establishes: { forcing: non_forcing }
      - id: ch_second_suit_65_H
        call: 4H
        priority: 29.5
        when: { my_suit: S, unbid_suit: H, cheapest_in_suit: true }
        requires:
          suits: { H: [5, 13], S: [6, 13] }
          evals: { total_points: [12, 40] }
        shows: "six-five come alive: six spades and five hearts, showing the second suit instead of repeating the first"
        establishes: { forcing: non_forcing }
```

**Answering seat.**  None owed (non-forcing).  Partner chooses between the two
suits with the existing `ch_raise_*` / `ch_pass` rungs; on this board he holds
three spades and passes.

**Endangers.**
* `ch_rebid_H4` (29) — **whole-corpus record +5 IMPs over 3 tables, so this is a
  winner and my rung must stay narrow**; it only loses the seat when I hold a
  genuine second five-card suit, which is exactly when partner has a choice to
  make.
* `ch_new_S4` (28) / `ch_new_S4_hi` (28.5) — same call, and my `when` is their
  `when` plus `my_suit: H`, so nothing new is covered and no fallback dies;
  mine adds the information that I also hold six of my own.
* `ch_raise_D4` (27) — different `when` (`partner_suit`).
* `ch_pass` (22).
* Above and untouched: `ch_raise_lott_S4` (32), `ch_negative_X3` (33),
  `ch_penalty_X` (38) — a defensive hand still doubles.

**VERIFIED.**  base `4H [ch_rebid_H4] fit=1.00 p=29` -> patched
`4S [ch_second_suit_65_S] fit=1.00 p=29.5`.

**Template.**  `expand: { M: [H, S] }` with `$oM` would give exactly these two;
untemplated context, so written out.  The minor-suit twins (six of a major and
five of a minor) deliberately omitted: four of a minor is not a contract.

---

## Board 938 — -6 — NOTHING-WRONG (purely constructive board)

Both auctions are uncontested end to end (`P P 1S P 2S P P P`, and we pass
throughout at the other table).  The loss is opener's: N holds
`AKT875.J74.Q.A96`, 14 HCP and six spades, and passes the capped passed-hand
raise where BEN bids game.  That is the constructive reviewer's board.

**What I checked in my lane.**  (a) E and W have 6 and 9 HCP with no shape and
no seat to enter — `oc1S_pass` and `cl_pass` are right at both tables; (b) there
is no balancing seat in either auction; (c) `r1S_raise_passed` is itself a
competitive-discipline convention (a capped raise opposite a possibly light
third-seat opening), and its answering rung `op_after_raise_inv` (3S) fits
**0.800** here — a one-point ceiling miss, not a hole.  The competitive-lane
observation is therefore only this: **the capped passed-hand raise is a
convention whose second half is one point short of reachable**, and it is a
ceiling to hand to the constructive reviewer, not a competitive rung.

---

## Board 942 — -6 — NOTHING-WRONG

Table A `P 1D P 2NT P P P`: I re-ranked all four of our seats.  S as dealer with
`A32.AJ95.T8.Q752` (10 HCP) passes; N over their 1D with `J642.T5.AJT83.87`
(6 HCP, five diamonds sitting UNDER the opener) passes; S over their natural
invitational 2NT with 10 balanced passes; N in the passout seat over 2NT with
6 HCP passes.  BEN agrees with all four (P at 1.00, 1.00, 1.00, 1.00).  The
board is lost at table B in a wholly uncontested 1D-2C-3NT auction.

---
