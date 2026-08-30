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
