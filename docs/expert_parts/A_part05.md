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

## Board 4 — -5; table B, call 7, W invites with 3H on an eight-card fit in a contested auction

`P 1C (1D) 1H P 2H P — ?`, W `QT93.AQ643.J94.6`, 9 HCP.  W invites, E accepts,
4H is down one; the other table played 3H making.  `uc_raise_H3` fits 1.00 at 31
and `uc_pass` is the only alternative, at 18.  At the seat:
`lott_total_trumps(H) = 8`, `total_points = 11`.

**Missing agreement.**  When the opponents have overcalled and partner has
merely supported me to the two level, eight combined trumps and a minimum mean
we are already at our level — the raise to three is not an invitation, it is a
lie about the fit.

**YAML** — context `general_uncontested_continuation`, insert before `uc_pass`
(the context is dispatched on RHO's last call, which is why a competitive
auction lands here; this is a rung ported under `is_competitive`, the pattern
`uc_raise_lott4_$M` already uses, NOT the wholesale re-routing round 12 killed):

```yaml
      - id: uc_pass_own_raise_H
        call: P
        priority: 31.5
        when: { my_suit: H, partner_suit: H, we_bid_last: true, is_competitive: true }
        requires:
          evals: { "lott_total_trumps(H)": [0, 8], total_points: [0, 14] }
        shows: "partner has supported my suit: with only eight trumps and a minimum we are already at our level"
        establishes: { forcing: non_forcing, agreed_suit: H }
      - id: uc_pass_own_raise_S
        call: P
        priority: 31.5
        when: { my_suit: S, partner_suit: S, we_bid_last: true, is_competitive: true }
        requires:
          evals: { "lott_total_trumps(S)": [0, 8], total_points: [0, 14] }
        shows: "partner has supported my suit: with only eight trumps and a minimum we are already at our level"
        establishes: { forcing: non_forcing, agreed_suit: S }
```

**Answering seat.**  None owed — it is a pass that agrees the suit and ends our
side's constructive sequence.

**Endangers.**
* `uc_raise_H3` / `S3` (31) — the rung immediately below; it keeps every hand
  with nine trumps, or with more than fourteen support points, so what it loses
  is exactly the eight-trump minimum invitation.
* `uc_rebid_H3` (29), `uc_new_*` (26-27.5), `uc_nt2` (28), `uc_nt3` (29) — all
  outranked for this hand; with a minimum and a fit found, none of them is the
  hand's best description.
* `uc_raise_H4` (32), `uc_raise_lott4_H` (32) — **above** it and untouched, so a
  hand that is really worth game still bids it, and so does a ten-trump Law
  hand.
* No fallback is deleted: P is already covered by `uc_pass` in this context.

**VERIFIED.**  base `3H [uc_raise_H3] fit=1.00 p=31` -> patched
`P [uc_pass_own_raise_H] fit=1.00 p=31.5`.  Downstream, E's 4H at call 9 never
arises.  This rung also fixes board 172 (below) and shows up twice in the
250-board blast measurement, both times converting 3H to P.

**Template.**  `expand: { M: [H, S] }`; untemplated context so written twice.
The minor twins are deliberately omitted — three of a minor is not a level
worth defending.

---

## Board 19 — -5; table B, call 10, E raises to game on an eight-card fit

`1C (1H) X P 1S (X) P (2H) P P — ?`, E `KJ85.Q43.K653.Q5`, 11 HCP, four spades
opposite partner's four.  4S is down one; 3S/2S makes.  At the seat
`lott_total_trumps(S) = 8`, `rule_of_26 = 25`, `their_fit = 8`.

**PRIMARY-READING NOTE.**  The dossier names `ballow_raise_lott4_S` for this
call.  That rule fits **0.000**.  The rule that actually chose 4S is
`ballow_raise_S4` at fit 1.00, priority 32 — the two tie on priority and the
blended score decides, so the higher-priority same-call rule got reported.
`repro.fires_summary` shows `ballow_raise_S4` "never fires" in the whole corpus
for the same reason.  Do not indict `ballow_raise_lott4_S` on this board.

**Missing agreement.**  The four-level raise is a game contract and the raise
ladder is separated by points alone: with only eight combined trumps and a game
estimate that rests on partner's unshown maximum, compete to the Law level and
stop.

**YAML** — context `general_balancing_low`, insert before `ballow_pass`:

```yaml
      - id: ballow_raise_brake_S2
        call: 2S
        priority: 32.5
        when: { partner_suit: S, cheapest_in_suit: true }
        requires:
          suits: { S: [3, 13] }
          evals: { "lott_total_trumps(S)": [7, 8], rule_of_26: [23, 27], total_points: [10, 40] }
        shows: "eight trumps and a game count that rests on partner's unshown maximum: compete, do not bid game"
        establishes: { forcing: non_forcing, agreed_suit: S }
      - id: ballow_raise_brake_H2
        call: 2H
        priority: 32.5
        when: { partner_suit: H, cheapest_in_suit: true }
        requires:
          suits: { H: [3, 13] }
          evals: { "lott_total_trumps(H)": [7, 8], rule_of_26: [23, 27], total_points: [10, 40] }
        shows: "eight trumps and a game count that rests on partner's unshown maximum: compete, do not bid game"
        establishes: { forcing: non_forcing, agreed_suit: H }
      - id: ballow_raise_brake_S3
        call: 3S
        priority: 32.5
        when: { partner_suit: S, cheapest_in_suit: true }
        requires:
          suits: { S: [3, 13] }
          evals: { "lott_total_trumps(S)": [7, 8], rule_of_26: [23, 27], total_points: [10, 40] }
        shows: "eight trumps and a game count that rests on partner's unshown maximum: invite at three, do not bid four"
        establishes: { forcing: non_forcing, agreed_suit: S }
      - id: ballow_raise_brake_H3
        call: 3H
        priority: 32.5
        when: { partner_suit: H, cheapest_in_suit: true }
        requires:
          suits: { H: [3, 13] }
          evals: { "lott_total_trumps(H)": [7, 8], rule_of_26: [23, 27], total_points: [10, 40] }
        shows: "eight trumps and a game count that rests on partner's unshown maximum: invite at three, do not bid four"
        establishes: { forcing: non_forcing, agreed_suit: H }
```

(Two levels because `cheapest_in_suit` decides which one is legal; on this board
the cheapest spade call over their 2H is **2S**, which is why a 3S-only version
never fired when I first traced it.)

**Answering seat.**  None owed — deliberately `non_forcing`, not
`invitational`.  An invitational three-level raise in the balancing seat would
owe an accepting rung that does not exist, which is round 17's -9.8 species.

**Endangers.**
* `ballow_raise_S4` / `H4` (32) — the rung it exists to stop; it keeps every
  nine-trump hand and every hand whose `rule_of_26` clears 27 honestly.
* `ballow_raise_S3` / `H3` (31) and `ballow_raise_S2` / `H2` (30) — same calls,
  same `when`; mine is the same bid with a reason attached, so nothing is
  covered that was not covered and no fallback dies.
* `ballow_raise_lott4_$M` (32) — untouched: with ten trumps and their fit shown,
  the Law bid is still four.
* `ballow_reopen_X` (41) / `ballow_X` (40) — above and untouched.

**VERIFIED.**  base `4S [ballow_raise_S4] fit=1.00 p=32` -> patched
`2S [ballow_raise_brake_S2] fit=1.00 p=32.5` — the Law level for eight trumps,
and the contract that makes.

**Template.**  `expand: { M: [H, S] }` crossed with the two levels; four rungs
as written.  The same four belong in `general_balancing_high` (`balhigh_`) and
`general_competitive_low/high` (`cl_`, `ch_`) — sixteen in all.  I shipped only
the `ballow_` four because that is the context this board lands in and the band
`rule_of_26: [23, 27]` should be measured on one context before it is swept.

**Second-order finding, not shipped.**  At call 6 E had no raise at all: over
their double of partner's one-level suit bid, `xd_raise_S2` caps at 9 total
points and `xd_jumpraise_S3` needs nine trumps, so a four-card raise worth 10-13
falls in the hole and passes.  That is a real starved rung
(`xd_raise_$X2_strong`, 10-13, priority 30.5) but I could not show it improves
this board, so I leave it as a note.

---

## Board 49 — -5; table A, call 5, opener passes out their 3S preempt with a seven-card suit

`P 1H (3S) P P — ?`, S `Q.AT98653.AK4.Q5`, 15 HCP, seven hearts,
`total_points = 18`, `suit_quality(H) = 1.5`.  We pass; BEN bids 4H.  The
candidate list at that seat has **four entries**: `balhigh_pass` (1.00),
`balhigh_reopen_X` (0.012), `uc_rebid_H4` (0.000), `balhigh_nt3` (0.000).

**The mechanism.**  `balhigh_rebid_H4` — the rung that exists for exactly this
hand — carries `when: { …, partner_has_acted: true }`, and partner has passed
the preempt.  So in the normal case, where the preempt silences partner, opener
cannot rebid his own suit at the four level at all.  `uc_rebid_H4` is the only
other 4H and needs `rule_of_26 >= 26`, which is unreachable opposite a silent
partner (`rule_of_26 = 20` here).  The seat is starved by construction.

**Missing agreement.**  Their preempt silenced partner, not me: with a good
six-plus-card major and opening values I bid it again at the four level in the
passout seat.

**YAML** — context `general_balancing_high`, insert before `balhigh_pass`:

```yaml
      - id: balhigh_rebid_solo_H4
        call: 4H
        priority: 29.5
        when: { my_suit: H, cheapest_in_suit: true, partner_has_acted: false, i_have_acted: true }
        requires:
          suits: { H: [6, 13] }
          evals: { total_points: [14, 40], "suit_quality(H)": [1.5, 9] }
        shows: "rebidding my own long hearts at the four level in the passout seat: partner never had room to speak"
        establishes: { forcing: non_forcing, agreed_suit: H }
      - id: balhigh_rebid_solo_S4
        call: 4S
        priority: 29.5
        when: { my_suit: S, cheapest_in_suit: true, partner_has_acted: false, i_have_acted: true }
        requires:
          suits: { S: [6, 13] }
          evals: { total_points: [14, 40], "suit_quality(S)": [1.5, 9] }
        shows: "rebidding my own long spades at the four level in the passout seat: partner never had room to speak"
        establishes: { forcing: non_forcing, agreed_suit: S }
```

**Answering seat.**  None owed — it is a sign-off-flavoured non-forcing game
bid and partner has already passed.

**Endangers.**
* `balhigh_rebid_H4` (29) — disjoint `when` (`partner_has_acted` true vs false),
  so it is untouched.
* `uc_rebid_H4` (29, in `general_uncontested_continuation`) — this IS a
  substitution: `general_balancing_high` is the more specific context, so once
  it defines 4H the `uc_` rung is suppressed in this seat.  My `requires` is a
  strict superset of `uc_rebid_H4`'s (same six cards, 14 points instead of 14
  points **plus** `rule_of_26 >= 26`), so every hand it caught, mine catches.
* `balhigh_nt3` (29) — 3NT with a stopper is still available to a balanced hand;
  mine demands six cards and a suit.
* `balhigh_pass` (21) — passing out a preempt with a seven-card suit and 18
  points is the loss.
* Above and untouched: `balhigh_X` (40) and `balhigh_reopen_X` (41).

**VERIFIED.**  base `P [balhigh_pass] fit=1.00 p=21` -> patched
`4H [balhigh_rebid_solo_H4] fit=1.00 p=29.5`.

**Template.**  `expand: { M: [H, S] }`; untemplated context so written twice.
Minors omitted on purpose: four of a minor over a three-level preempt is not a
contract, and the corresponding hand should be bidding 3NT or passing.

---

## Board 84 — -5; table A, call 8, N runs to 2S from their balancing double of our agreed 2H

`1D P 1H P 2H P P (X) — ?`, N `AQ76.AT85.K92.86`, 13 HCP, `total_points = 14`.
We hold an agreed eight-card heart fit at the two level; N introduces spades
(`xd_second_S2`, 1.00 at 25) and we end in 3H down one.  N/S make eight tricks
in hearts: **2H doubled making is +670 vulnerable**.

**Missing agreement.**  When they balance with a double of our agreed
partscore, a minimum passes — the new suit is a rescue we do not need and an
invitation to them to bid again.

**YAML** — context `general_their_double`, insert before `xd_pass`:

```yaml
      - id: xd_pass_agreed_H
        call: P
        priority: 26.5
        when: { my_suit: H, partner_suit: H, we_bid_last: true, we_hold_contract: true }
        requires:
          evals: { total_points: [0, 16] }
        shows: "they doubled our agreed partscore: a minimum passes rather than running to a new suit"
        establishes: { forcing: non_forcing, agreed_suit: H }
```

…and the identical rung for `S`, `C`, `D` (`xd_pass_agreed_S/C/D`, same body
with the suit substituted).

**Answering seat.**  None owed (a pass that ends the auction).

**Endangers.**
* `xd_second_S2` (25) and `xd_second_*1/2/3` (24-26) — the "my second suit"
  family; it keeps every hand above 16 total points, so what it loses is the
  minimum that has already told its story.  Whole-corpus record of
  `xd_second_S2`: 1 table, **-5**.
* `xd_run_*` (24-26) — mutually exclusive `when` (`we_hold_contract: false`).
* `xd_XX_extras` (23) — below; a 19-count still redoubles.
* `xd_rebid_*` (34) — above and untouched: a six-card suit is still rebid.
* No fallback is deleted; P is already covered by `xd_pass` (18).

**VERIFIED.**  base `2S [xd_second_S2] fit=1.00 p=25` -> patched
`P [xd_pass_agreed_H] fit=1.00 p=26.5`.

**Template.**  `expand: { X: [C, D, H, S] }` in spirit; four rungs written out,
because the `my_suit`/`partner_suit` pair has to name the same suit and the
context is untemplated.

---

## Board 151 — -5; table B, call 8, W reopens with a double holding five hearts

`P 1C P 1S P 2C P P — ?`, W `A85.QJT32.T752.Q`, 9 HCP, five hearts, singleton
club.  `ballow_X` fits (9 HCP + singleton in their suit) at priority 40 and
buries `ballow_new_H2` (26).  Partner then had to guess and we reached 3NT for
-100.  `ballow_X` whole-corpus: **11 tables, -32, mean -2.91** against a corpus
mean of -0.489 — the worst-performing balancing rung in the file.

**Missing agreement.**  In the passout seat a five-card major is a suit, not a
shape: bid it, because a double promises three cards in every unbid suit and
partner will otherwise place the contract in the one I do not hold.

**YAML** — context `general_balancing_low`, insert before `ballow_pass`:

```yaml
      - id: ballow_balance_major_H
        call: 2H
        priority: 41.5
        when: { unbid_suit: H, cheapest_in_suit: true, side_has_acted: false }
        requires:
          suits: { H: [5, 13] }
          evals: { total_points: [8, 13], "suit_quality(H)": [1, 9] }
        shows: "balancing in my five-card major rather than doubling: partner will pass a suit, and a double promises three cards in every unbid suit"
        establishes: { forcing: non_forcing }
      - id: ballow_balance_major_S
        call: 2S
        priority: 41.5
        when: { unbid_suit: S, cheapest_in_suit: true, side_has_acted: false }
        requires:
          suits: { S: [5, 13] }
          evals: { total_points: [8, 13], "suit_quality(S)": [1, 9] }
        shows: "balancing in my five-card major rather than doubling: partner will pass a suit, and a double promises three cards in every unbid suit"
        establishes: { forcing: non_forcing }
```

**Answering seat.**  None owed — non-forcing, and partner's raises are already
authored (`uc_raise_$M*`).

**Endangers.**
* `ballow_X` (40) — the only rung it outranks, and only on hands with a real
  five-card major and less than a full opening.  A 14+ balancing hand keeps the
  double because my ceiling is 13 total points.
* `ballow_reopen_X` / `_X2` (41) — those need `side_has_acted: true`; mine needs
  `false`, so they are disjoint.
* `ballow_new_H2` (26) etc. — same call, same `when` plus my `side_has_acted`
  restriction, so nothing new is covered and no fallback dies; mine is simply
  the same bid ranked where it belongs.
* `ballow_nt2_balance` (33) — a 15-21 balanced hand is above my ceiling.

**VERIFIED.**  base `X [ballow_X] fit=1.00 p=40` -> patched
`2H [ballow_balance_major_H] fit=1.00 p=41.5`.  It fires four times in the
250-board blast sample (2x `X -> 2H`, 2x `P -> 2S`), which is the right order
of magnitude for an 11-table family.

**Template.**  `expand: { M: [H, S] }`; twin rungs for `general_balancing_high`
(`balhigh_balance_major_$M`, calls 3H/3S) are the natural completion and were
not needed by any board here.

---

## Board 172 — -5; table A, call 8, opener raises his own suit to three on eight trumps

`1H (X) 1S (1NT) P P 2H P — ?`, N `3.AKT52.T62.AT72`, 11 HCP,
`total_points = 14`, `lott_total_trumps(H) = 8`.  Partner's 2H is a balance
after he has already bid 1S and passed 1NT — a preference, not a raise.  3H is
down one (-100 vulnerable) where 2H makes (+110).

**Missing agreement.**  This is the SAME agreement as board 4 and the same rung
fixes it: eight trumps and a minimum, with our own bid standing, means we have
already bid to our level.

**YAML.**  `uc_pass_own_raise_H` / `_S` exactly as written under board 4
(`general_uncontested_continuation`, priority 31.5).

**This board's own contribution — the sibling coverage.**  The same seat occurs
after `... - bid - P - P - ?` and after `... - bid>=3C - ?`, where the rung does
not exist.  The completion is four more rungs, identical bodies with the
context prefix changed:

```yaml
      # in general_balancing_low  (before ballow_pass) and
      # in general_balancing_high (before balhigh_pass)
      - id: ballow_pass_own_raise_H       # / ballow_pass_own_raise_S
        call: P                            # / balhigh_pass_own_raise_H, _S
        priority: 31.5
        when: { my_suit: H, partner_suit: H, we_bid_last: true, is_competitive: true }
        requires:
          evals: { "lott_total_trumps(H)": [0, 8], total_points: [0, 14] }
        shows: "partner has supported my suit: with only eight trumps and a minimum we are already at our level"
        establishes: { forcing: non_forcing, agreed_suit: H }
```

**Answering seat.**  None owed.

**Endangers.**  In the balancing contexts: `ballow_raise_H3` / `balhigh_raise_H3`
(31) — the eight-trump minimum raise, which is the call that loses this board;
`ballow_raise_H4` (32) and `ballow_raise_lott4_H` (32) stay above it, so a real
game hand and a ten-trump Law hand are untouched.

**VERIFIED** for the shipped `uc_` pair: base `P [uc_pass] fit=1.00 p=18` ->
patched `P [uc_pass_own_raise_H] fit=1.00 p=31.5` (the call is unchanged here
because `uc_pass` already won; the value is that the rung now says WHY, and it
is the same rung that changes board 4).  **UNTESTED** for the four
`ballow_`/`balhigh_` twins — no board in this slice reaches them.

**Template.**  `expand: { M: [H, S] }` across three contexts = six rungs.

---

## Board 209 — -5; table A, call 3, N jumps to only 3D with a ten-card fit and a void

`1C (1D) X — ?`, N `JT54.AJ85.K9765.` — five diamonds opposite partner's
five-card overcall, void in their suit.  At the seat `lott_total_trumps(D) = 10`,
`singleton_or_void = 1`, `total_points = 10`.  We bid 3D; W then bid 4C and made
it (-130).

**Missing agreement.**  Bid to the level of the fit: ten known trumps and a
void opposite partner's overcall is a four-level preempt over their double, not
a three-level one.

**YAML** — context `general_their_double`, insert before `xd_pass`:

```yaml
      - id: xd_jumpraise_lott_D4
        call: 4D
        priority: 32.5
        when: { we_bid_last: true, we_hold_contract: false, partner_suit: D,
                standing_bid_level: [1] }
        requires:
          suits: { D: [5, 13] }
          evals: { "lott_total_trumps(D)": [10, 26], total_points: [5, 15], singleton_or_void: [1, 1] }
        shows: "bidding to the level of the fit over their double: ten known trumps and a side shortness"
        establishes: { forcing: non_forcing, agreed_suit: D }
      - id: xd_jumpraise_lott_C4
        call: 4C
        priority: 32.5
        when: { we_bid_last: true, we_hold_contract: false, partner_suit: C,
                standing_bid_level: [1] }
        requires:
          suits: { C: [5, 13] }
          evals: { "lott_total_trumps(C)": [10, 26], total_points: [5, 15], singleton_or_void: [1, 1] }
        shows: "bidding to the level of the fit over their double: ten known trumps and a side shortness"
        establishes: { forcing: non_forcing, agreed_suit: C }
```

**Note on the ceiling.**  `total_points` had to be widened from my first draft's
`[5, 12]` to `[5, 15]`: `candidate_ctx` sets `agreed_suit` from `establishes`,
so the rule is scored on SUPPORT points, and a void is worth five of them.  The
first version fitted 0.409 and never fired.  This trap will bite any rung that
sets `agreed_suit` and caps `total_points`.

**Answering seat.**  None owed (non-forcing, and it is a preempt).

**Endangers.**
* `xd_jumpraise_D3` (32) — the rung below, and mine only outranks it on the
  ten-trump, shortness-bearing hands the Law says belong at the four level.
  Whole-corpus record of `xd_jumpraise_D3`: 2 tables, **+1** — a small winner,
  which is why the gate is three separate conditions and not a band change.
* `xd_raise_D3` (31), `xd_raise_D2` (30), `xd_run_*`/`xd_second_*` (24-26),
  `xd_pass` (18).
* **This one DOES delete a code fallback**: `general_their_double` has no
  four-level rungs at all today, so adding 4D/4C makes those calls "covered" and
  suppresses whatever the fallback layer would have generated for them in that
  seat.  I have restricted the reach with `standing_bid_level: [1]` (only over a
  double of a one-level bid) and kept `requires` broad; this is the one
  proposal in the slice that carries genuine fallback-deletion risk and it
  should be measured on its own.

**VERIFIED.**  base `3D [xd_jumpraise_D3] fit=1.00 p=32` -> patched
`4D [xd_jumpraise_lott_D4] fit=1.00 p=32.5`.

**Template.**  `expand: { m: [C, D] }`; majors omitted because `xd_jumpraise_$M3`
already reaches three of a major and four of a major is game, which is a
different decision.

---

## Board 261 — -5; table A, call 5, the takeout doubler accepts an invitation with a flat 14

`(2D) X P 3H P — ?`, S `KQ75.QT95.T8.AK5`, 14 HCP, 4-4-2-3, no singleton.
Partner's 3H (`aw2D_3H`) is invitational, 9-11 with four hearts.  We bid 4H, one
down; 3H makes.  At the seat `total_points = 14`, `singleton_or_void = 0`,
`lott_total_trumps(H) = 8`, and 4H is chosen by `uc_raise_H4` at 32 — note the
dossier's `uc_doubler_game3_H` is the primary reading, not the chooser
(`uc_doubler_game3_H` wants 17+ total points and S has 14).

**Missing agreement.**  The takeout doubler accepts an invitational jump advance
only with a fifth trump or a shortness to ruff with: a flat hand facing a 9-11
advance is 23-25 combined and belongs in three.

**YAML** — context `general_uncontested_continuation`, insert before `uc_pass`:

```yaml
      - id: uc_doubler_decline_H
        call: P
        priority: 35.5
        when: { partner_suit: H, my_last_call_was_double: true, we_hold_contract: false,
                standing_bid_level: [3] }
        requires:
          suits: { H: [0, 4] }
          evals: { total_points: [0, 18], singleton_or_void: [0, 0] }
        shows: "declining the invitational jump advance: a flat doubler with no fifth trump and no shortness has nothing extra"
        establishes: { forcing: non_forcing, agreed_suit: H }
      - id: uc_doubler_decline_S
        call: P
        priority: 35.5
        when: { partner_suit: S, my_last_call_was_double: true, we_hold_contract: false,
                standing_bid_level: [3] }
        requires:
          suits: { S: [0, 4] }
          evals: { total_points: [0, 18], singleton_or_void: [0, 0] }
        shows: "declining the invitational jump advance: a flat doubler with no fifth trump and no shortness has nothing extra"
        establishes: { forcing: non_forcing, agreed_suit: S }
```

**Answering seat.**  This is the answering seat — it completes the conversation
`X … 3M (invitational) … pass/4M` that the file opens and never closes.
`aw2D_3H`/`aw2S_3H` are declared `forcing: invitational` and until now had no
declining rung at all; the only authored acceptances were
`uc_doubler_game3_$M` (17+) and `uc_doubler_game_$M`.

**Endangers.**
* `uc_doubler_game3_H` / `_S` (35) and `uc_doubler_game_H` / `_S` (35) — the
  rungs it exists to stop, and only for hands with at most four trumps, no
  shortness and 18 or fewer support points.  Whole-corpus: `uc_doubler_game3_H`
  3 tables **-5**, `uc_doubler_game3_S` 2 tables **0**.
* `uc_doubler_raise_$M` (34), `uc_doubler_raise3_$M` (33) — below; those are
  two- and three-level calls that are not legal over a three-level advance.
* `uc_raise_H4` (32) — the rule that actually chose 4S/4H here.
* No fallback deleted (P already covered by `uc_pass`).

**VERIFIED.**  base `4H [uc_raise_H4] fit=1.00 p=32` -> patched
`P [uc_doubler_decline_H] fit=1.00 p=35.5`.

**Template.**  `expand: { M: [H, S] }`; minors omitted (a three-level minor
advance of a double is not invitational in this file).

---

## Board 276 — -5; table B, call 7, the takeout doubler rebids 2NT with 17 balanced

`P P 1C X (2C) P P — ?`, W `AK54.Q52.A9.A642`, 17 HCP.  `ballow_nt2_strong`
(17-21 with a stopper) fits 1.00 at 30 and we play 2NT down one.  The rung's
`when` is `side_has_acted: true` — which **my own double satisfies**, so the
rung written for "partner has acted, I have not" is being applied to the player
who acted.

**Missing agreement.**  A player who has already made a descriptive bid has
already shown this hand; a 17-21 balancing 2NT is a call the doubler cannot
hold, because the double already promised the values and partner has denied
his.

**YAML** — context `general_balancing_low`, edit `ballow_nt2_strong`'s `when`:

```yaml
      - id: ballow_nt2_strong
        call: 2NT
        priority: 30
        when: { side_has_acted: true, i_have_acted: false, their_last_bid_suit: true, standing_bid_level: [2] }
        requires:
          hcp: [17, 21]
          evals: { weakest_their_stopper: [0.9, 9], semi_balanced: [1, 1] }
        shows: "natural 2NT: 17-21 balanced with their suit stopped"
        establishes: { forcing: non_forcing }
```

**What it SUBTRACTS.**  Every 17-21 balancing 2NT made by a seat that has
already bid.  Whole-corpus record of the rule as it stands: **7 tables, -16,
mean -2.29** against a corpus mean of -0.489, and it decides boards 243 and 276
in this slice alone.  With the gate in place the seat falls to `ballow_pass`,
which is what BEN does at both.

**Answering seat.**  None — this is a restriction, not a new call.  It does
re-expose the code fallback for 2NT in the seats it now refuses (fit ~1.00 at
priority 10, which loses to `ballow_pass` at 21).

**Endangers.**  Nothing outranks anything new; `ballow_nt2_balance` (33, the
true balancing 2NT with `side_has_acted: false`) and `ballow_nt2` (28) are
untouched, and the pair now partitions the seat correctly: 33 for "nobody on our
side has spoken", 30 for "partner spoke and I did not", 28 for the 11-12 rung.

**VERIFIED.**  base `2NT [ballow_nt2_strong] fit=1.00 p=30` -> patched
`P [ballow_pass] fit=1.00 p=21`.  Same result on board 243's table B.

**Template.**  Single edit.  The sibling repair is `uc_nt2` (board 508) and, on
explainability grounds, `balhigh_nt2` / `cl_nt2` should be reviewed for the same
condition by the lint.

---

## Board 291 — -5 — NOTHING-WRONG

Table A `1D P 1S P 1NT P P P`, all four of our calls passes and BEN agrees at
0.99/1.00/1.00/1.00.  Checked in my lane: N with `AT9.A53.J73.Q974` (11
balanced) over their 1D — the 1NT overcall needs 15-18 and the takeout double
needs shortness, so pass is the system's call and the right one; S in the
sandwich seat with `KQ842.8742.T84.8` (5 HCP) — `sw_pass`, correct at
matchpoints with five spades under the 1S bidder; N over their 1NT rebid with 11
balanced and no five-card suit — pass; S in the passout seat with 5 HCP — pass.
We took -90 against a par of -400.  The board is lost at table B in an entirely
uncontested `1D-1S-2D-2NT-3NT`.

---

## Board 300 — -5; table B, call 3, the sandwich 2C overcall with five cards in their suit

`1H P 1S — ?`, W `A4.Q8432.4.AJT97`, 11 HCP, five clubs **and five hearts —
hearts being the suit RHO opened**.  `sw_2C` fits 1.00 at 66.  The board's -300
is at table A in an uncontested auction (that is `uc_nt2`'s, and board 508's
proposal reaches it); the in-lane call is this one.

**Missing agreement.**  A sandwich overcall between two bidders is an action
bid, so it must not be made with a hand whose values are wasted: five cards in a
suit they have already named are five cards that will never take a trick for us.

**YAML** — context `sandwich_seat`, add one eval to each of `sw_2C`, `sw_2D`,
`sw_2H`, `sw_2S`:

```yaml
      - id: sw_2C
        call: 2C
        when: { unbid_suit: C }
        priority: 66
        requires: { suits: { C: [5, 13] }, hcp: [11, 17], evals: { suit_quality(C): [2, 9], max_their_suit_length: [0, 3] } }
        shows: "sandwich 2-level overcall: good 5+ clubs, 11-17"
        establishes: { forcing: non_forcing }
```

(and the same `max_their_suit_length: [0, 3]` added to `sw_2D`, `sw_2H`,
`sw_2S`.)

**What it SUBTRACTS.**  Sandwich two-level overcalls by hands holding four or
more cards in one of the two suits the opponents have bid.  Whole-corpus record
of `sw_2C`: **8 tables, -22, mean -2.75**; of the family's sibling `sw_X`,
23 tables, -39.  The sandwich seat as a whole is a losing seat in this corpus and
this is the narrowest honest gate on it.

**Answering seat.**  None — a restriction.  The hand falls to `sw_pass` (30),
which is authored.

**Endangers.**  Nothing gains rank.  `sw_2$X_jump` (69) and `sw_3$X` (69.5) are
above and untouched — a genuine preempt still goes in.  `sw_1H`/`sw_1S` (68)
untouched.

**VERIFIED.**  base `2C [sw_2C] fit=1.00 p=66` -> patched
`P [sw_pass] fit=1.00 p=30`.

**Template.**  Four edits inside a context already templated on `$o`; the eval
is suit-independent so it is a single line repeated four times.

---

## Board 387 — -5 — NOTHING-WRONG

Table A `P P 1S P 1NT P 3D P 3NT P P P`: our four calls are all passes and BEN
agrees at 1.00 on every one.  In my lane: N has 2 HCP and no seat; S has 11 HCP
with three spades over their 1S (pass — the overcall needs a suit and the double
needs shortness), passes again in the sandwich seat over their 1NT with a
balanced 11 and no five-card suit, and passes their 3D jump rebid holding
`A873` of diamonds — a penalty double of a jump rebid on four to the ace facing
a silent partner is not a call.  The -200 at table B is a constructive underbid
(`1S-1NT-2D-2S` on an 18-count).

---

## Board 507 — -5; table A, call 7, S passes their 1C-1S-2S auction with a singleton spade and 13

`P P 1C P 1S P 2S — ?`, S `T.J93.QJT4.AKQ73`, 13 HCP, singleton spade, five
clubs.  BEN doubles at 0.92; we pass.  `cl_takeout_X` fits **0.000**, and the
reason is the evaluator: it tests `max_their_suit_length: [0, 2]`, which is my
maximum length in ANY suit they have bid — and I hold five of their CLUBS.  At
the seat: `standing_suit_length = 1`, `max_their_suit_length = 5`,
`weakest_unbid_length = 3`.

**Missing agreement.**  When the opponents have bid two suits and settled in one
of them, the double is takeout of the suit they AGREED: shortness is measured in
that suit only, and length in the other one is normal, not disqualifying.

**YAML** — context `general_competitive_low`, insert before `cl_nt1`:

```yaml
      - id: cl_takeout_X_agreed
        call: X
        priority: 36.5
        when: { their_last_bid_suit: true, side_has_acted: false, standing_bid_level: [2] }
        requires:
          hcp: [11, 40]
          evals: { standing_suit_length: [0, 2], weakest_unbid_length: [3, 13] }
        shows: "takeout double of the suit they have agreed: shortness in THAT suit and three cards in each unbid suit"
        establishes: { forcing: one_round }
```

**Answering seat — SHIPPED, and it already exists.**  The double is
`forcing: one_round`, so partner must answer.  The seat is
`general_pull_or_sit` (`... - X - P - ?`), and I traced partner's hand on this
board (`QJ7.T764.A632.54`, 7 HCP): he answers **3H** via `adx_pull_H3` (fit
1.00, priority 57), with `adx_pull_D3` (1.00) and `adx_pass_min` (1.00) behind
it.  The ladder is live and complete; nothing further is owed.

**Endangers.**
* `cl_takeout_X` (36) — same call, my `when` is a strict subset of the
  conditions under which X is already covered (`their_last_bid_suit` +
  `side_has_acted: false`), so **no code fallback is deleted**.  Mine is the
  better description because it names the trump suit as the one to be short in.
  Whole-corpus record of `cl_takeout_X`: **1 table, -10**.
* `cl_negative_X1` / `X2` (33) — disjoint (`side_has_acted: true`).
* `cl_new_*` (25-27.5), `cl_nt*` (27-29), `cl_raise_*` (30-32) — outranked, and
  with a singleton in their agreed suit and 13 points the double is the call
  that finds the fit rather than guessing one.
* `cl_nt2_direct` (37) — above and untouched: a 16-21 balanced hand still bids
  2NT.
* `cl_doubler_raise*` (33-35) — disjoint (`my_last_call_was_double`).

**VERIFIED.**  base `P [cl_pass] fit=1.00 p=20` -> patched
`X [cl_takeout_X_agreed] fit=1.00 p=36.5`.

**Template.**  Single rung (suit-independent — `standing_suit_length` and
`weakest_unbid_length` both read the auction).  The three-level twin belongs in
`general_competitive_high` with `standing_bid_level: [3]` and `hcp: [13, 40]`.

---

## Board 508 — -5; table A, call 6, opener bids a natural 11-12 2NT after opening 1C

`P P 1C (1D) 2C P — ?`, S `T764.KQJT.AQ.963`, 12 HCP.  S OPENED the bidding and
partner raised; `uc_nt2` ("natural 2NT: 11-12 balanced") fits 1.00 at 28 and we
play 2NT **down five, -300**.

**Missing agreement.**  An 11-12 natural notrump is responder's rung; a player
who has already opened or overcalled has shown his hand and cannot hold it.

**YAML** — context `general_uncontested_continuation`, edit `uc_nt2`'s `when`:

```yaml
      - id: uc_nt2
        call: 2NT
        priority: 28
        when: { side_has_acted: true, i_have_acted: false }
        requires:
          hcp: [11, 12]
          evals: { rule_of_26: [21, 99], semi_balanced: [1, 1], weakest_their_stopper: [0.9, 9] }
        shows: "natural 2NT: 11-12 balanced, their suits stopped"
        establishes: { forcing: non_forcing }
```

**What it SUBTRACTS.**  Every 11-12 natural 2NT by a seat that has already made a
non-pass call.  `uc_nt2` is a standing open item in `ROUND_METHOD.md` ("ruled OK
on the wrong number in round 15 and is still open"); its record here is
**21 tables, -33, mean -1.57** against -0.489, and this gate does not touch the
population the rung was written for (responder's second call).  It re-exposes
the code fallback for 2NT in the refused seats, which loses to `uc_pass` (18) at
fit 1.00.

**Answering seat.**  None — a restriction.

**Endangers.**  Nothing gains rank.  `uc_nt3` (29) is untouched, as are all the
raise and rebid ladders.  The hole this opens — a strong balanced rebid after I
have already acted — is a KNOWN open item that round 14 measured at -1 on ten
boards and reverted, so leaving it a hole (and therefore a pass) is the measured
choice, not an oversight.

**VERIFIED.**  base `2NT [uc_nt2] fit=1.00 p=28` -> patched
`P [uc_pass] fit=1.00 p=18`.

**Template.**  Single edit; siblings `cl_nt2` / `ballow_nt2` / `balhigh_nt2`
carry the same 11-12 band and should get the same condition for sibling-lint
consistency (I only ship the two the boards prove).

---

## Board 515 — -5 — NOTHING-WRONG (uncontested board)

`1S P — ?`, E raises to 3S (limit) on `743.A95.65.KQT43` and we play 4S down
one; both auctions are uncontested and this is the constructive reviewer's
board.

**In-lane observation, offered rather than proposed.**  The rung that fires is
`r1S_limit_raise` at `total_points 10-13`, and E's ten points include length
points for a five-card CLUB suit opposite a spade opening — a suit that will be
dummy's and take no extra trick.  Every raise ladder in the competitive contexts
(`cl_raise_*`, `ch_raise_*`, `ballow_raise_*`, and the LOTT rungs) is driven by
the same `total_points`, so the same inflation is what puts us one level too
high in partscore battles.  A `total_points` variant that discounts length in a
suit partner has not shown would be a single evaluator change with very large
reach — too large for a per-board proposal, and outside this round's remit, but
it is the common cause behind boards 19, 261, 419 and 515.

---

## Board 520 — -5; table B, call 5, advancer bids 2NT holding a five-card major

`P P 1D (1S) 1NT — ?` from E's seat: partner overcalled 1S, RHO responded 1NT,
E holds `T7.AT972.A76.QJ7` — 11 HCP, five hearts, `suit_quality(H) = 1.5`,
`total_points = 12`.  `cl_nt2` fits 1.00 at 28 and buries `cl_new_H2_hi` (26.5).
2NT is down three.

**Missing agreement.**  A natural notrump in competition denies a five-card
major — exactly as its own one-level sibling `cl_nt1` already denies a six-card
one.

**YAML** — context `general_competitive_low`, edit `cl_nt2`:

```yaml
      - id: cl_nt2
        call: 2NT
        priority: 28
        when: { side_has_acted: true }
        requires:
          hcp: [11, 12]
          evals: { weakest_their_stopper: [0.9, 9], rule_of_26: [22, 99], semi_balanced: [1, 1] }
          not: { any_of: [ { suits: { H: [5, 13] } }, { suits: { S: [5, 13] } } ] }
        shows: "natural 2NT: 11-12 balanced with a stopper in their suit, denying a five-card major"
        establishes: { forcing: non_forcing }
```

**What it SUBTRACTS.**  11-12 competitive 2NTs on hands with a five-card major.
`cl_nt2`'s record: **8 tables, -21, mean -2.62**.  The call it hands the seat to,
`cl_new_H2`, is a **net winner** at +12 over 16 tables — the substitution is
from the file's worst notrump rung to one of its better suit rungs.  This is the
round-7 "gate given to one sibling and not the others" species: `cl_nt1` already
carries `not: { any_of: [ {suits:{H:[6,13]}}, {suits:{S:[6,13]}} ] }`.

**Answering seat.**  None — a restriction.

**Endangers.**  Nothing gains rank.  `cl_nt3` (29) untouched (a 13-19 hand with
a five-card major and a real stopper is a different animal and 3NT is often
right); `cl_nt2_direct` (37) untouched.

**VERIFIED.**  base `2NT [cl_nt2] fit=1.00 p=28` -> patched
`2H [cl_new_H2_hi] fit=1.00 p=26.5`.

**Template.**  Single edit; the same denial belongs on `ballow_nt2` and
`balhigh_nt2` for sibling consistency.

---

## Board 585 — -5; table A, call 5, S cue-bids game-forcing over partner's balancing double holding four trumps

`(1S) P P X P — ?`, S `T982.AQ2.K84.AT8`, 13 HCP, **four spades sitting over the
opener**.  `advbal_S_cue` ("13+, game forcing") fits 1.00 at 49 and we bid our
way to 4H down one.  E/W make six tricks in spades: **1S doubled is -300 to
them** and the par for N/S is +140.

**Missing agreement.**  Four of their trumps sitting over the opener, opposite a
balancing double, is a penalty pass — the balancing double is made on shape and
the trump stack is the reason to leave it in.

**YAML — a NEW CONTEXT, appended at the END of `contexts:`.**  The four existing
`advance_balancing_double_*` contexts define no pass at all, so a later context
with the same pattern can only ADD one; it carries the generic pass verbatim as
its floor so that suppressing `uc_pass` cannot starve the seat.

```yaml
  - id: advance_balancing_double_convert
    description: "Advancing partner's balancing double: converting it for penalty"
    pattern: "1$o - P - P - X - P - ?"
    expand: { o: [C, D, H, S] }
    rules:
      - id: advbal_convert_$o
        call: P
        priority: 56
        requires:
          suits: { $o: [4, 13] }
          hcp: [10, 40]
          not:
            any_of:
              - suits: { C: [5, 13] }
              - suits: { D: [5, 13] }
              - suits: { H: [5, 13] }
              - suits: { S: [5, 13] }
        shows: "converting the balancing double for penalty: four of their trumps sitting over the opener, 10+, and no suit of my own"
        establishes: { forcing: sign_off }
      - id: advbal_convert_min_$o
        call: P
        priority: 18
        requires: {}
        shows: "nothing to say opposite the balancing double"
        establishes: { forcing: non_forcing }
        negative_inference_weight: soft
```

**Why the second rung is not optional.**  Adding P to a context of specificity
1006 suppresses `uc_pass` (specificity 3) in this seat.  Without
`advbal_convert_min_$o` every hand that does not hold four of their trumps would
have no pass at all and would be forced to bid.  This is the round-15
"adding a rung deletes the fallback" mechanism, and the low rung is the superset
discipline applied.

**Answering seat.**  None — it ends the auction.

**Endangers.**
* `advbal_$o_cue` (49) — game-forcing on 13+; my rung takes only the hands with
  four trumps and no suit, where a game force opposite a balancing double is an
  overbid by a king.
* `advbal_$o_2NT` (50) and `advbal_$o_*_jump` (50-54) — a 10-12 hand with four
  of their trumps and a four-card side suit now passes; with a FIVE-card suit
  the `not:` clause lets the suit bid through.
* `advbal_$o_C/D/H/S` (54-58) — those require 0-9 HCP and my floor is 10, so
  they are untouched.
* No other context loses anything: the four existing contexts sort first and
  keep every call they define.

**VERIFIED.**  base `2S [advbal_S_cue] fit=1.00 p=49` -> patched
`P [advbal_convert_S] fit=1.00 p=56`.

**Template.**  `expand: { o: [C, D, H, S] }` — the whole point of writing it as
a new context is that it CAN be templated, where the four existing ones cannot.

---

## Board 661 — -5; table B, call 6, the doubler jumps to game opposite a 0-8 advance

`P 1D X P 1S P — ?`, W `QT98.AKQ3.8.AQJ3`, 18 HCP, four spades, singleton
diamond; partner's 1S advance is 0-8.  `uc_doubler_game_S` (20+ support points)
fits 1.00 at 35 and we play 4S down one.  The ladder has a hole in it: the 2S
raise shows 17-19, the game jump shows 20+, and there is **no jump raise at
all**, because `uc_doubler_raise3_S` carries `cheapest_in_suit: true` and 3S is
not the cheapest spade bid over a one-level advance.

**Missing agreement.**  Opposite a forced 0-8 advance, 19-22 is an invitation,
not a game: the jump raise to three is the missing rung and the game jump needs
22.

**YAML** — context `general_uncontested_continuation`, insert before `uc_pass`,
plus one band edit:

```yaml
      - id: uc_doubler_jumpraise_H
        call: 3H
        priority: 34.5
        when: { partner_suit: H, my_last_call_was_double: true, we_hold_contract: false,
                cheapest_in_suit: false, standing_bid_level: [1] }
        requires:
          suits: { H: [4, 13] }
          evals: { total_points: [19, 22] }
        shows: "jump raise of the cheapest advance: 19-22, invitational (the double promised 12+, the advance 0-8)"
        establishes: { forcing: invitational, agreed_suit: H }
      - id: uc_doubler_jumpraise_S
        call: 3S
        priority: 34.5
        when: { partner_suit: S, my_last_call_was_double: true, we_hold_contract: false,
                cheapest_in_suit: false, standing_bid_level: [1] }
        requires:
          suits: { S: [4, 13] }
          evals: { total_points: [19, 22] }
        shows: "jump raise of the cheapest advance: 19-22, invitational (the double promised 12+, the advance 0-8)"
        establishes: { forcing: invitational, agreed_suit: S }
```

and, in the same context and in `general_competitive_low` (the `cl_` twins), the
game jump's floor:

```yaml
        requires: { suits: { H: [4, 13] }, evals: { total_points: [22, 40] } }   # uc_doubler_game_H, cl_doubler_game_H
        requires: { suits: { S: [4, 13] }, evals: { total_points: [22, 40] } }   # uc_doubler_game_S, cl_doubler_game_S
```

**THE ANSWERING SEAT — this call is an invitation, so it ships with one.**  I
traced partner's next turn (`1D X P 1S P 3S P — ?`, advancer
`J643.J54.9543.T4`, 2 HCP): he answers **P** via `uc_pass_own_raise_S` (board 4's
rung, fit 1.00, priority 31.5), with `uc_raise_S4` at 32 available and fitting
0.000 on a 2-count.  So the two answers — decline with `uc_pass_own_raise_$M`,
accept with `uc_raise_$M4` — both exist and both fit correctly.  This is why the
board-4 rung has to ship in the same batch as this one.

**Endangers.**
* `uc_doubler_game_$M` (35) — the band edit is what stops 4S; the pair of rungs
  together turn one call into an invitation plus an acceptance.
* `uc_doubler_raise_$M` (34) — the cheapest raise, 17-19; disjoint by
  `cheapest_in_suit`.
* `uc_raise_$M4` (32), `uc_raise_lott4_$M` (32) — below and untouched.
* No fallback deleted for 3S: `uc_doubler_raise3_$M` already covers 3$M under
  the same `partner_suit`/`my_last_call_was_double` gates.
* **A locked scenario moves and this is deliberate.**
  `harvested::e1_doubler_raises_the_advance` (`AQ85.A4.KQ82.KJ5`, `1C X P 1S P`)
  went 4S -> 3S; its expectation is `["4S", "2S", "3S"]`, so it still passes.  It
  is the only one of the 516 locked scenarios that moves under my whole batch.

**VERIFIED.**  base `4S [uc_doubler_game_S] fit=1.00 p=35` -> patched
`3S [uc_doubler_jumpraise_S] fit=1.00 p=34.5`, and the answering seat verified
separately as above.

**Template.**  `expand: { M: [H, S] }` for the jump raises; the band edit is four
rules (`uc_`/`cl_` x `H`/`S`).  Minors omitted: three of a minor over a one-level
advance is not an invitation anyone can act on.

---

## Board 705 — -5; table A, call 3, N passes out their 1C with ten points in the balancing seat

`1C P P — ?`, N `KT87.94.AQJ4.972`, 10 HCP, three small clubs.  `bal_X` demands
`any_of: [{hcp 8-16, suits {C: [0,2]}}, {hcp 15+}]` — N has THREE clubs and ten
points, so it fits neither branch and `bal_pass` (0-10 HCP) wins.  1C is passed
out for -70 where +110 was there in spades.

**Missing agreement.**  A one-of-a-minor opening promises no length, so the
balancing double over it does not need shortness — three cards in their minor
and ten points is a reopening double.

**YAML** — context `balancing_seat` (already templated on `$o`), insert before
`bal_pass`:

```yaml
      - id: bal_X_minor_$o
        call: X
        priority: 63
        when: { standing_bid_strain: [C, D] }
        requires:
          hcp: [10, 16]
          suits: { $o: [0, 3] }
        shows: "balancing double of their minor: 10+ with at most three of their suit; a minor opening does not promise length, so shortness is not required"
        establishes: { forcing: one_round }
```

**Answering seat — verified live.**  The double is `one_round`; the answering
context `advance_balancing_double_C` exists and I traced partner's hand on this
board (`Q54.AJ63.K92.QT8`, 12 HCP): he answers **2H** via `advbal_C_H_jump`
(fit 1.00, priority 53), with `advbal_C_2NT` (1.00) and `advbal_C_cue` (0.80)
behind it.  Board 585's new `advance_balancing_double_convert` context adds the
penalty-pass rung to the same seat, so the two proposals compose.

**Endangers.**  Priority 63 is deliberately BELOW the existing ladder so it can
only fill the hole:
* `bal_2NT` (71), `bal_X` (70) — above and untouched, so a 19-21 balanced hand
  and a genuinely short 8-16 hand keep their calls.  `bal_X`'s record is
  **14 tables, -3, mean -0.21 — better than the corpus mean**, which is exactly
  why this proposal widens the seat rather than gating the rule.
* `bal_1NT` (66) — above: 11-14 balanced with a stopper still bids 1NT.
* `balancing_suits_$o` natural bids (64) — above: a five-card suit is still bid.
* `bal_pass` (30) — the rung it replaces, and only for 10-16 counts.
* No fallback deleted: X is already covered in this context by `bal_X`, which
  has no `when` at all.
* In the `o = H` and `o = S` expansions the rung is unreachable
  (`standing_bid_strain: [C, D]`), which is intended — doubling a major opening
  with three of their trumps is a different and worse proposition.

**VERIFIED.**  base `P [bal_pass] fit=1.00 p=30` -> patched
`X [bal_X_minor_C] fit=1.00 p=63`.

**Template.**  `expand: { o: [C, D, H, S] }` — already the context's own
expansion, so one rung as written.

---

## Board 723 — -5; table A, call 3, S bids 2NT over partner's double of their weak two with a six-card minor

`(2S) X P — ?`, S `A94.A6.QT9542.T9`, 10 HCP, six diamonds,
`total_points = 12`, `suit_quality(D) = 1.5`.  `aw2S_2NT` (8-11 with a stopper)
fits 1.00 at 55 and 2NT is down one; 4D makes eleven tricks at the other table.
The ladder is `aw2S_3D` at **0-8** and then nothing until the major game jump —
a 9-13 hand with a real minor has no bid.

**Missing agreement.**  Opposite a takeout double of a weak two, a real
five-card minor and 9-13 is a suit advance, not a notrump: partner's double has
already promised support for it.

**YAML** — context `advance_weak2_double_S`, insert before `aw2S_2NT`:

```yaml
      - id: aw2S_3D_inv
        call: 3D
        priority: 58
        requires:
          suits: { D: [5, 13] }
          evals: { total_points: [9, 13], "suit_quality(D)": [1, 9] }
          not: { any_of: [ { suits: { H: [4, 13] } } ] }
        shows: "competitive minor advance of the double: a real five-card diamond suit and 9-13, no four-card heart suit"
        establishes: { forcing: non_forcing }
      - id: aw2S_3C_inv
        call: 3C
        priority: 58.5
        requires:
          suits: { C: [5, 13] }
          evals: { total_points: [9, 13], "suit_quality(C)": [1, 9] }
          not: { any_of: [ { suits: { H: [4, 13] } } ] }
        shows: "competitive minor advance of the double: a real five-card club suit and 9-13, no four-card heart suit"
        establishes: { forcing: non_forcing }
```

**Answering seat — and why the rung is NOT invitational.**  My first draft
declared `forcing: invitational`.  I traced the doubler's reply
(`2S X P 3D P — ?`, N `53.K987.KJ3.AQ82`, 13 HCP) and the only fitting candidate
is `uc_pass` at 1.00: there is no rung anywhere that accepts a minor-suit
invitation from a takeout doubler.  Rather than ship an invitation into an empty
seat — round 17 priced that at up to -9.8 a seat — I demoted it to
`non_forcing` and worded `shows` to match.  The competitive value (getting to
diamonds instead of notrump) is unchanged.

**Endangers.**
* `aw2S_2NT` (55) — whole-corpus **2 tables, +5, mean +2.50**, so this is a
  small WINNER and the rung is priced accordingly: it only loses the seat with a
  genuine five-card minor and 9-13, i.e. the hands where notrump has no source
  of tricks.
* `aw2S_3D` (57) / `aw2S_3C` (58) — same calls, 0-8; mine is the stronger
  sibling and nothing new is covered.
* `aw2S_cue` (54), `aw2S_pass_penalty` (50) — below.
* `aw2S_3H` (62) and `aw2S_4H` (60) — above and untouched, and the `not:` clause
  makes sure a four-card heart suit never reaches my rungs anyway.

**VERIFIED.**  base `2NT [aw2S_2NT] fit=1.00 p=55` -> patched
`3D [aw2S_3D_inv] fit=1.00 p=58`.

**Template.**  `expand: { W: [D, H, S] }` is what the agreement wants; the three
`advance_weak2_double_*` contexts are separate and untemplated, so the pair has
to be written into each, with the `not:` clause naming whichever majors are
still unbid (over 2D the denial is both majors, over 2H it is spades, over 2S it
is hearts).

---

## Board 755 — -5; table A, call 7, the negative doubler corrects partner's 1NT to 2D on six points

`P 1D (1H) X P 1NT P — ?`, S `QJ43.T82.KT87.87`, 6 HCP.  S doubled (showing four
spades), partner rebid 1NT denying them, and S now "raises" to 2D on four small.
`uc_raise_D2` fits 1.00 at 30.  W then bid 2H and made nine tricks (-140); 1NT
was our contract.

**Missing agreement.**  My double already showed my values and my shape; with a
minimum I pass partner's rebid instead of correcting it.

**YAML** — context `general_uncontested_continuation`, insert before `uc_pass`:

```yaml
      - id: uc_pass_after_my_double
        call: P
        priority: 30.5
        when: { my_last_call_was_double: true, we_bid_last: true }
        requires:
          evals: { total_points: [0, 8] }
        shows: "my double already showed my values: a minimum does not correct partner's rebid"
        establishes: { forcing: non_forcing }
```

**Answering seat.**  None owed (a pass).

**Endangers.**
* `uc_raise_$X2` (30) — the rung it beats, and only for hands of eight support
  points or fewer that have already doubled.
* `uc_new_*` (26-27.5), `uc_nt2` (28), `uc_nt3` (29) — outranked; none of them
  describes a six-count that has already doubled.
* `uc_raise_$X3` (31) and above — untouched, so a doubler with real extras still
  competes.
* No fallback deleted (P covered by `uc_pass`).

**VERIFIED.**  base `2D [uc_raise_D2] fit=1.00 p=30` -> patched
`P [uc_pass_after_my_double] fit=1.00 p=30.5`.

**Template.**  Single suit-independent rung.  The twins belong in
`general_competitive_low/high` and `general_balancing_low/high` (`cl_`, `ch_`,
`ballow_`, `balhigh_` prefixes, identical bodies) — five rungs in all.

---

## Board 838 — -5; table B, call 5, W invents a five-level club sacrifice with no fit

`1D (1H) X (2H) 4S — ?`, W `8.AT653.K.KT9752`, 10 HCP, six clubs but
`lott_total_trumps(C) = 6` — partner has never mentioned clubs.  `ch_new_C5_hi`
fits 1.00 at 28.5; 5C doubled is -800 against their vulnerable game.
Whole-corpus record of the family: `ch_new_C5` **2 tables, -15, mean -7.50**.

**Missing agreement.**  A new suit at the five level over their game commits
eleven tricks opposite a hand that has never supported it — that needs a
seven-card suit, not a six-card one.

**YAML** — context `general_competitive_high`, edit all eight rungs
`ch_new_$X5` and `ch_new_$X5_hi` (`$X` in C, D, H, S):

```yaml
      - id: ch_new_C5
        call: 5C
        priority: 28
        when: { unbid_suit: C, cheapest_in_suit: true, partner_has_acted: true }
        requires:
          suits: { C: [7, 13] }
          evals: { total_points: [14, 40], "suit_quality(C)": [1.5, 9] }
        shows: "natural C at the five level: 6+ cards, 14+ points, partner has bid"
        establishes: { forcing: non_forcing }
```

(only the `suits:` line changes, `[6, 13]` -> `[7, 13]`, in each of the eight;
the `shows:` text should be updated to "7+ cards" when it is applied.)

**What it SUBTRACTS.**  Five-level new-suit bids on six-card suits.  Two firings
in this corpus, both losers, totalling -15.

**Answering seat.**  None — a restriction.  The seat falls to `ch_pass` (22),
which is authored.

**Endangers.**  Nothing gains rank.  `ch_rebid_$X5` (29) is untouched — a suit I
have already bid is a different case and partner has heard it.  `ch_penalty_X`
(38) and `ch_negative_X3` (33) are above and untouched.

**VERIFIED.**  base `5C [ch_new_C5_hi] fit=1.00 p=28.5` -> patched
`P [ch_pass] fit=1.00 p=22` (patched top candidate; `ch_new_C5_hi` drops to
0.349).

**Two negative results on this board, reported not shipped.**  (i) My first
draft was a PASS rung gated on `partner_shown_length: [0, 2]` — that evaluator
takes no suit argument by default and resolves to partner's FIRST shown suit, so
it was measuring partner's hearts while I was inventing clubs; it could never
fire.  (ii) My second draft gated the five-level bids on
`we_vulnerable: false` — but on this board the save was at FAVOURABLE
vulnerability and cost only 120, so the colours are not the agreement.  The fit
is.

**Template.**  Eight one-line edits inside an untemplated context; the same
change belongs on `ballow_new_$X4` / `balhigh_new_$X4`'s five-level equivalents
if any are ever written.

---

## Board 871 — -5; table A, call 3, S makes a negative double holding six hearts

`P 1D (1S) — ?`, S `95.AJ6542.K7.J87`, 9 HCP, **six hearts**,
`total_points = 11`, `suit_quality(H) = 1.5`.  `nx_1m1S_X` ("negative double:
4+ hearts, 6+ HCP") fits 1.00 at priority 80 and buries `nx_1m1S_2H` (78).  The
auction then wanders 2D-2H-3D-3H-4D for -100 where 3D makes.  Whole-corpus
record of `nx_1m1S_X`: **21 tables, -21, mean -1.00**.

**Missing agreement.**  A six-card major is a suit, not a shape: bid it, because
the negative double promises only four and partner will play me for four.

**YAML** — context `resp_1m_over_1S` (templated on `$m`), insert before
`nx_1m1S_2H`:

```yaml
      - id: nx_1m1S_2H_long
        call: 2H
        priority: 81
        requires:
          suits: { H: [6, 13] }
          evals: { total_points: [8, 40], "suit_quality(H)": [1, 9] }
        shows: "a six-card heart suit: bid it, because the negative double promises only four"
        establishes: { forcing: non_forcing }
```

**Answering seat.**  None owed — `non_forcing`, and opener's continuations over
a free 2H are already authored (`onx_*` / `uc_*`).  Note the deliberate
`non_forcing`: the existing `nx_1m1S_2H` is declared forcing at 10+, and this
rung is the weaker long-suit sibling that partner may pass.

**Endangers.**
* `nx_1m1S_X` (80) — the only rung it outranks, and only with SIX hearts.  This
  is not the round-14 `nxj_X` longest-suit cap that measured -5 and was
  reverted: nothing is gated, the double keeps every 4- and 5-card holding, and
  the landing seat (a natural 2H) already exists and is already authored.
* `nx_1m1S_2H` (78) — same call; mine is its long-suit, lower-strength sibling,
  so nothing new is covered and no fallback dies.
* `nx_1m1S_wj_H` (56, the weak jump to 3H) — below; with 11 points and a decent
  suit the two-level free bid is the better description, and the weak jump keeps
  everything under 8.
* `nx_1m1S_cue` (70), `nx_1m1S_3NT` (52) — untouched.

**VERIFIED.**  base `X [nx_1m1S_X] fit=1.00 p=80` -> patched
`2H [nx_1m1S_2H_long] fit=1.00 p=81`.

**Template.**  The context is already expanded on `$m`, so this single rung
serves `1C - 1S` and `1D - 1S`.  The twin over a 1H overcall is
`nx_1m1H_1S_long` (call 1S, six spades) in `resp_1m_over_1H`, at priority 79
above `nx_1m1H_X` (80)… note that over 1H the natural bid is at the ONE level
and already outranks nothing, so the twin needs priority 81 as well.

---

## Board 885 — -5; table A, call 3, sandwich double with a five-card major

`(1S) P (1NT) — ?`, N `A5.AKJ92.A654.65`, 16 HCP, five hearts.  `sw_X` fits 1.00
at 70 and buries `sw_2H` (66); partner then passed with a minimum and W bid 3S.
`sw_X`'s own `requires` already carries `not: { evals: { longest_suit_length:
[6, 13] } }` — the file has ALREADY decided that a long suit should be bid, and
stopped one card short.  Whole-corpus record: **23 tables, -39, mean -1.70**.

**Missing agreement.**  Between two bidding opponents a five-card major is a
bid, not a double: the double asks partner to choose among suits and I already
know which one I want.

**YAML** — context `sandwich_seat`, edit `sw_X`'s denial:

```yaml
      - id: sw_X
        call: X
        priority: 70
        requires:
          not:
            any_of:
              - evals: { longest_suit_length: [6, 13] }
              - suits: { H: [5, 13] }
              - suits: { S: [5, 13] }
          any_of:
            - hcp: [12, 16]
              suits: { $o: [0, 2] }
              evals: { longest_suit_length: [4, 13] }
            # (remaining branches unchanged)
```

**What it SUBTRACTS.**  Sandwich doubles on hands with a five-card major.  The
seat they fall to is `sw_1H`/`sw_1S` (68) or `sw_2H`/`sw_2S` (66), both
authored, both natural.  I deliberately did NOT extend the denial to five-card
minors: a five-card minor between two bidders is rarely the right contract and
the double keeps more options.

**Answering seat.**  None — a restriction; the advance ladders
(`advance_sandwich_*`) are unchanged.

**Endangers.**  Nothing gains rank.  `sw_2$X_jump` (69), `sw_3$X` (69.5) are
above and untouched.

**VERIFIED.**  base `X [sw_X] fit=1.00 p=70` -> patched
`2H [sw_2H] fit=1.00 p=66`.

**Template.**  One edit inside a context already expanded on `$o`; the denial is
suit-independent.  Note this composes with board 300's `max_their_suit_length`
gate on `sw_2$X` — a hand with five hearts where hearts is THEIR suit now
neither doubles (it has a five-card major) nor bids (the values are wasted), and
passes, which is right.

---

## Board 926 — -5; table B, call 5, advancer bids a three-card major over a five-card diamond suit

`1C P 1S X P — ?`, W `T43.765.AQ642.T2`, 6 HCP, **five diamonds**, three small
hearts.  `advsw_C1S_H` ("cheapest major") fits 1.00 at 55 and we play hearts;
E raises and 3H is down one.  `advance_sandwich_C_1S` has three rules — a
cheapest-suit ladder — and no rung at all for a suit of my own.

**Missing agreement.**  Advancing partner's sandwich double, a five-card suit
of my own outranks the cheapest three-card major: partner promised support for
all the unbid suits, so I name the one I actually hold.

**YAML** — context `advance_sandwich_C_1S`, insert before `advsw_C1S_H`:

```yaml
      - id: advsw_C1S_own5_D
        call: 2D
        priority: 60
        requires:
          suits: { D: [5, 13] }
          evals: { "suit_diff(D, H)": [1, 13], "suit_diff(D, S)": [1, 13] }
        shows: "my own five-card diamond suit, longer than either major: advance the double in the suit I actually hold"
        establishes: { forcing: non_forcing }
```

**Answering seat.**  None owed (non-forcing; the doubler's continuations are the
generic `uc_*` / `cl_*` ladders).

**Endangers.**
* `advsw_C1S_H` (55) — the cheapest-major rung, and only when my minor is
  strictly longer than both majors, which is exactly when the major is a
  three-card fiction.
* The rest of the three-rule context (all at or below 55).
* No fallback deleted: 2D is already covered by the corresponding
  cheapest-suit rung in this context.
* The `suit_diff` pair is what keeps a 5-5 or 5-4 major hand out of it.

**VERIFIED.**  base `2H [advsw_C1S_H] fit=1.00 p=55` -> patched
`2D [advsw_C1S_own5_D] fit=1.00 p=60`.

**Template.**  The agreement is `expand_pairs` over the nine
`advance_sandwich_$o_$v` contexts x the two or three suits that are unbid in
each — about 20 rungs.  They are nine separate untemplated contexts today, and
this is the single largest templating win available in this slice: nine
three-rule contexts that should be one templated context with six rungs.

---
