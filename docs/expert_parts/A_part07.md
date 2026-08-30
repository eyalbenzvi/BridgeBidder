# Expert A (competitive / matchpoint duplicate) — dossier part 07

38 boards, -80 IMPs, every one a 2- or 3-IMP loss.  Worked in dossier order.

| | |
|---|---|
| boards reviewed | **38** |
| proposals | **30**, all **VERIFIED** through `repro.rank()` on a patched copy of the system |
| NOTHING-WRONG | **8** (900, 168, 320, 392, 735, 739, 848, 920) |
| additive rungs | 24 |
| gates / re-ranks (subtractive — named as such) | 6 |

**How the verification was done.**  The engine's `choose_bid` accepts a
`system_path`, so every proposal below was written into a *copy* of
`two_over_one.yaml` in a scratch directory and traced.  The repository file was
not touched.  All 30 proposals were then loaded **together** into one patched
file, which parses, and all 30 boards were re-traced in that combined system:
**30 of 30 produce the intended call, 0 failures.**  So the set is internally
consistent as well as individually verified.

Every rule I gate or outrank was first re-scored across ALL its firings with
`repro.fires_summary` on both `reports/r18_before.jsonl` and
`reports/held_before.jsonl`.  Two of my six subtractive proposals accuse a rule
that is **profitable** on the whole corpus; both are flagged and neither should
ship in a bundle.

---

## The three agreements that matter most in this slice

**1. The takeout double of a preempt is priced in HIGH CARDS when it should be
priced in SHAPE.**  `v3_$X_X` demands **14-17** with three or fewer of their
suit, `vw2_X` demands **13-16**, `balhigh_X` demands **14+** — while its own
low-level twin `ballow_X` floors at **11** (and at 9 with a singleton) and its
`shows` sentence *quotes the ballow gates verbatim*.  So a textbook 12-13 count
with a singleton and support for the unbid suits passes a preempt out.  Boards
**195, 417, 282, 934**.  The pass rungs these replace are the largest losing
populations in my slice: `balhigh_pass` 767/768 tables at **-0.67 / -0.65**,
`ch_pass` 794/795 at **-0.72 / -0.69**, `cl_pass` 707/690 at **-0.81 / -0.49**,
`sw_pass` 247/240 at **-0.49 / -0.66**, `vw2_pass` 52/53 at **-0.60 / -0.79**.
Every one of these is a seat where we are not in the auction at all.

**2. The Law of Total Tricks exists in two contexts out of six, for two suits
out of four, at one level out of three.**  `cl_raise_lott4_$M` and
`ch_raise_lott4_$M` are majors-only; `ballow_*` has the four-level twin but no
three-level one; **`general_their_double` has no four-level raise of any kind**,
so when partner preempts and they double, the only 4M candidate is the code
fallback at priority 12 (`xd_pass` fires 88/91 times at **-1.72 / -0.43**).
Boards **947, 241, 933**.

**3. The suit-quality toll is a tax on light hands, and the file charges it to
strong ones.**  `oc1H_1S` refuses a 12-count with `J8754` (fit 0.757 — the
*only* failing gate is `suit_quality >= 1`); `cl_new_D3` refuses a 16-count with
`K9752`; `cl_new_S2` refuses a 10-count with `T9853`.  Honour requirements
belong on the 8-10 end of an overcall range, not on the 11-16 end, where the
hand is the trick source.  Boards **907, 2, 395**.  The same species produced
board **2**'s other finding: `general_balancing_low` has `ballow_reopen_X` (the
16+ second-round takeout double) and `general_competitive_low` **has no twin**.

---

## Board 900 — -3 IMPs — NOTHING-WRONG (competitive)

**Purely constructive.**  At table A E/W never make a call; at table B our E/W
pass throughout an uncontested `1D-1H-1NT-2H-3H`.  There is no competitive
decision on this board.

What I checked: W's pass over 1D holding `9873.7.A853.AQT2` is correct — the
takeout double of 1D needs shortness in *diamonds* and W has four of them; W's
pass at call 7 falls in `general_competitive_low` where `cl_takeout_X` is gated
`their_last_bid_suit: true` and the standing bid is 1NT, so no double exists —
correctly, since doubling a 1NT response with 10 HCP is not an agreement worth
having.  The loss is opener's `2C` rebid (`ob_1D1H_2C`, 58) beating `ob_1NT`
(57.5) on a 2=3=4=4 thirteen-count, and responder's `2D` false preference on
`J6` with five hearts.  **Both belong to the constructive reviewer.**

---

## Board 907 — -3 IMPs — table A, call 3, seat S: `P` over 1H

**Missing agreement.**  A one-level overcall made on opening values is bid on
length and playing strength; the suit-quality requirement is the price of the
LIGHT (8-10) overcall and must not be charged to an 11-16 hand.

`J8754.K.A965.A65` is 12 HCP with five spades and two aces.  `oc1H_1S` fits
**0.757** and the only failing gate is `suit_quality(S) >= 1`: `J8754` scores
0.5, deficit 0.5 against `_EVAL_S2["suit_quality"] = 0.9`, `exp(-0.25/0.9) =
0.757` — exactly the observed number.

```yaml
      # in context overcalls_of_1H, immediately before oc1H_2C
      - id: oc1H_1S_values
        call: 1S
        priority: 70.5
        requires: { suits: { S: [5, 13] }, hcp: [11, 16] }
        shows: "one-level overcall on opening values: 5+ spades, 11-16 (suit quality is the price of the LIGHT overcall, not of this one)"
        establishes: { forcing: non_forcing }
```

**Answering seat.**  Not a force — `establishes: non_forcing`.  The advance
already exists (`advance_overcall`, `1$o - 1$v - P - ?`), unchanged.

**Endangers.**  `oc1H_X` (72) — above me, so a genuine takeout double still
wins; `oc1H_1S` (71) — above me, so the quality reading stays primary and mine
only picks up the hands it drops; `oc1H_2D` / `oc1H_2C` (65) — a five-card
spade suit at the ONE level is cheaper and more useful than a two-level minor;
`oc1H_pass` (25) — a 12-count with a five-card major is not "nothing suitable".
No fallback is deleted: 1S was already covered by `oc1H_1S` in every seat this
`when`-less rung reaches.

**VERIFIED** — bids 1S, `oc1H_1S_values` fit 1.000, score 0.911.

**Template.**  `expand_pairs` over (their opening suit, my overcall suit) for
all twelve one-level combinations across `overcalls_of_1C/1D/1H/1S`; the four
contexts are written out longhand today, so this is four hand-written rungs or
one merged templated context.

---

## Board 937 — -3 IMPs — table A, call 3, seat N: `X` over `1C 1D 1H`

**Missing agreement.**  A negative double denies four-card support for the suit
partner has bid — with a fit you raise, you do not ask him to guess.

`JT63.74.Q873.KT9` is 6 HCP with four-card support for partner's 1D overcall.
`cl_negative_X1` (33) and `cl_raise_D2` (30) both fit 1.000 and priority hands
it to the double, which was redoubled.

```yaml
      # cl_negative_X1 and cl_negative_X2 in general_competitive_low: one added
      # clause each, on the evals line
      - id: cl_negative_X1
        # ...unchanged...
        requires:
          hcp: [6, 40]
          evals: { "suit_length(their)": [0, 3], longest_suit_length: [0, 4],
                   "suit_length(partner)": [0, 3] }
          any_of:
            - suits: { H: [4, 13] }
            - suits: { S: [4, 13] }
        shows: "negative double: 6+ HCP with a major they have not bid and no four-card fit for partner"
```

**Answering seat.**  Unchanged; the double keeps `forcing: one_round` and
`general_pull_or_sit` answers it.

**Endangers — THIS IS A GATE AND IT ACCUSES A WINNER.**  `repro.fires_summary`:
`cl_negative_X1` fires on **12 tables at +0.25** (r18) and **10 tables at
+1.90** (held out).  It is profitable on the whole corpus.  The gate removes
only the sub-population with a four-card fit for partner, which is small, but
the honest recommendation is: **measure this one alone, never in a bundle.**
Below it, `cl_raise_D2` (30) inherits the seat — the better description, since
four trumps and a weak hand is a raise.  Above it, `cl_takeout_X` (36) and
`cl_reopen_X` are untouched (different `when`).

**VERIFIED** — bids 2D, `cl_raise_D2` fit 1.000; `cl_negative_X1` drops to 0.349.

**Template.**  Apply to `cl_negative_X1`, `cl_negative_X2` and `ch_negative_X3`
identically (the sibling lint will otherwise flag the odd one out).

---

## Board 947 — -3 IMPs — table B, call 10, seat E: `P` in the passout seat over 2S

**Missing agreement.**  In the passout seat, with nine combined trumps, bid
three of partner's suit — the level of the fit is decided by trumps, not by a
combined point count.

`632.9532.AJ8.KT3`: 8 total points, three-card support for a partner who
opened 1D and rebid 2D (shown length 6), `lott_total_trumps(D) = 9`.
`ballow_raise_D3` misses on **two** gates at once (`total_points >= 10`,
`rule_of_26 >= 22` against an actual 21) and scores 0.328.

```yaml
      # in general_balancing_low, immediately before ballow_raise_D4
      - id: ballow_raise_lott3_D
        call: 3D
        priority: 30.5
        when: { partner_suit: D, cheapest_in_suit: true, is_competitive: true }
        requires:
          suits: { D: [3, 13] }
          evals: { "lott_total_trumps(D)": [9, 26], total_points: [8, 40] }
        shows: "the Law in the passout seat: nine combined trumps, so three of partner's suit is our level - do not sell out to their two-level contract"
        establishes: { forcing: non_forcing, agreed_suit: D }
```

**Answering seat.**  Non-forcing sign-off-flavoured raise; partner's seat is
`general_competitive_high` / `general_balancing_high`, both populated.

**Endangers.**  `ballow_raise_D3` (31) — above me, so the 10+ constructive
reading stays primary and I only take the 8-9 band it drops; `ballow_nt3` (29),
`ballow_nt2` (28), `ballow_new_*3` (27) — with three-card support for a known
six-card suit, the raise is the better description than a notrump without a
stopper or a new suit at the three level; `ballow_pass` (21).
**No fallback is deleted**: 3D is already `covered` by `ballow_raise_D3`, whose
`when` is identical.  `ballow_pass` fires on 270/271 tables at **-0.72 / -0.26**,
so the population I am taking from is a loser.

**VERIFIED** — bids 3D, `ballow_raise_lott3_D` fit 1.000, score 0.791.

**Template.**  `expand: { m: [C, D] }` for the minors and `{ M: [H, S] }` for
the majors in BOTH `general_balancing_low` and `general_competitive_low` (which
has `cl_raise_lott3_$M` for the majors only, and it is separately known to be
unreachable — I am **not** proposing to free that rule).

---

## Board 2 — -2 IMPs — table A, call 6, seat N: `P` over `1H 1NT P P 2H`

**Missing agreement.**  `general_balancing_low` has a second-round takeout
double when our side has already acted (`ballow_reopen_X`, 16+, short in their
suit); `general_competitive_low` has no twin, so a 16-count with a doubleton in
their suit passes their re-bid suit out.

`KQT.KQ.K9752.K62`, 16 HCP, `KQ` doubleton in hearts, longest suit five.  The
seat's only non-pass candidate today is the code fallback X at priority 9,
which can never beat `cl_pass` at 20.

```yaml
      # in general_competitive_low, immediately before cl_negative_X1
      - id: cl_reopen_X
        call: X
        priority: 35
        when: { their_last_bid_suit: true, side_has_acted: true, we_bid_last: false,
                my_last_call_was_double: false, we_hold_contract: false }
        requires:
          hcp: [16, 40]
          evals: { max_their_suit_length: [0, 2], longest_suit_length: [0, 5] }
        shows: "second-round takeout double: 16+, short in their suit, our side already in"
        establishes: { forcing: one_round }
```

**Answering seat.**  `forcing: one_round`, answered by `general_pull_or_sit`
(`... - X - P - ?`), which is fully populated (`adx_pull_$X2/3/4`,
`adx_neg_major_$M2/3`, `adx_nt`, `adx_sit`, `adx_pass_min`).  Traced: partner
answers.

**Endangers.**  `cl_takeout_X` (36) — above me, and its `when` is
`side_has_acted: false`, so we are disjoint; `cl_negative_X2_both` (33.5),
`cl_negative_X1/X2` (33) — below me, but their `when` requires
`i_have_acted: false` while mine requires our side to have acted *and* not to
have bid last, so again disjoint in practice; `cl_nt3` (29) and `cl_new_*3`
(27-27.5) — with 16 flat and a doubleton in their suit, takeout beats guessing
between 3NT and a three-level suit; `cl_pass` (20).
**Fallback deleted:** the undiscussed X (priority 9) is suppressed in every
seat this `when` reaches.  That fallback loses to `cl_pass` (fit 1.00, prio 20)
in every seat it can appear in, so it decides nothing and the deletion is free.

**VERIFIED** — bids X, `cl_reopen_X` fit 1.000, score 0.805.

**Template.**  One rung, no expansion needed (`max_their_suit_length` is
suit-free).  It should be added to `general_competitive_high` as
`ch_reopen_X` in the same edit — see board 262's note.

---

## Board 112 — -2 IMPs — table A, call 2, seat S: `P` over 1C

**Missing agreement.**  Not vulnerable, a one-level overcall may be made on
five-four in the majors and 8-11 — the shape is the trick source that the
honours are not.

`AT43.97653.J.KT4`: 8 HCP, five hearts (`97653`, quality 0.0 against a gate of
1.0 — fit 0.329), four spades, singleton diamond.  BEN overcalls 1H and the
board is worth 2 IMPs because partner then raises.

```yaml
      # in context overcalls_of_1C, immediately before oc1C_2D_jump
      - id: oc1C_1H_shape
        call: 1H
        priority: 70.5
        when: { we_vulnerable: false }
        requires:
          suits: { H: [5, 13], S: [4, 13] }
          hcp: [8, 11]
        shows: "shapely one-level overcall: five hearts and four spades, 8-11, not vulnerable - the shape is the trick source the honours are not"
        establishes: { forcing: non_forcing }
```

**Answering seat.**  Non-forcing; `advance_overcall` answers it unchanged.

**Endangers.**  `oc1C_X` (72) and `oc1C_X_minor` (71.5, board 206) — above me,
so a real takeout double still wins; `oc1C_1S` / `oc1C_1H` (71) — above me;
`oc1C_2H_jump` (60) — with only five hearts the weak jump is a misdescription;
`oc1C_pass` (25).  `oc1C_pass` fires 125/120 tables at **-0.32 / -0.33**, a
mild but consistent loser.  No fallback deleted (1H already covered).

**VERIFIED** — bids 1H, `oc1C_1H_shape` fit 1.000, score 0.911.

**Template.**  `expand_pairs` over (their minor, my major, the other major) —
1C and 1D openings, hearts-and-spades and spades-and-hearts.  Do **not** extend
it to overcalls of a major opening: there the second major is *their* suit.

---

## Board 152 — -2 IMPs — table A, call 6, seat S: `P` sitting partner's double of 1NT

**Missing agreement.**  With a bust and a five-card suit, run from partner's
double of their notrump — a yarborough is not a defence, and five cards is a
trump suit.

`J7543.63.AT63.T5`, 5 HCP, five spades.  `adx_pass_min` (52) fits 1.000 and
there is no weak pull rung at all: `adx_pull_my_S` needs `my_suit: S` (I have
never bid), the `uc_new_S2` rungs sit at 26 and demand 10+ points.

```yaml
      # in general_pull_or_sit, immediately before adx_neg_major_H2
      - id: adx_pull_weak_S2
        call: 2S
        priority: 53
        when: { unbid_suit: S, cheapest_in_suit: true, standing_bid_strain: [NT] }
        requires:
          suits: { S: [5, 13] }
          evals: { total_points: [0, 8] }
        shows: "running from partner's double of their notrump: a five-card suit is a better trump suit than a bust is a defence"
        establishes: { forcing: sign_off }
```

**Answering seat.**  `sign_off`; no answer required.  The `standing_bid_strain:
[NT]` gate is what makes that safe — a pull of a *suit* double is a different
conversation and is left to the existing `adx_pull_my_*` rungs.

**Endangers.**  `adx_sit` (61) and `adx_neg_major_$M2/3` (62) and
`adx_pull_my_*` (60) — all above me, so a trump stack, a promised major and my
own suit all still win; `adx_pass_min` (52) — directly below me, and a
five-card suit opposite a double *is* "a suit worth pulling to", which is what
that rule's own `shows` sentence denies.  `adx_pass_min` scores **+0.60 / +3.80**
on 5 tables, a small and favourable population, so the narrow `standing_bid_strain:
[NT]` and `total_points <= 8` gates are doing necessary work — with them, the
overlap is the sub-population where partner doubled 1NT and I am broke.
**Fallback:** 2S was already covered by `uc_new_S2` in this seat.

**VERIFIED** — bids 2S, `adx_pull_weak_S2` fit 1.000, score 0.859.

**Template.**  `expand: { X: [C, D, H, S] }` for all four run-out suits, with
the two majors at priority 53 and the minors at 52.5 (prefer the major).

---

## Board 168 — -2 IMPs — NOTHING-WRONG

Both flagged divergences are ours and one of them is right.  Table A call 8:
our `4C` (`balhigh_rebid_C4`) **makes ten tricks for +130, which is par**, and
BEN's pass would score less.  Table B call 5: our vulnerable `3D`
(`ch_rebid_D3`, six good diamonds, 14 total points) is **BEN's own call at
0.54** — no divergence is recorded.  The -200 is a double-dummy accident on a
board where the only winning action was to sell out to 3C.

**Reported negative.**  I prototyped a `we_vulnerable: true` clause on the
three-level free rebid (7 cards or 15+ points required).  It is defensible
bridge and I am declining to propose it: BEN agrees with the call the gate
would remove, and the rule family that owns it (`cl_rebid_D3`) **never fires**
in either corpus, so the change is unmeasurable and can only add risk.

---

## Board 195 — -2 IMPs — table A, call 1, seat N: `P` over 3C

**Missing agreement.**  The takeout double of a three-level preempt is priced
in SHAPE: 11-13 with at most a doubleton in their suit and three-plus cards in
every unbid suit is a double, not a pass.

`AK853.Q954.K62.6`: 12 HCP, singleton club, five spades and four hearts.
`v3_C_X` requires **14-17** (with C <= 3) or 18+, so it fits 0.409 and the hand
passes out a preempt with two four-card-or-longer majors.

```yaml
      # in defense_vs_preempt_C, immediately before v3_C_3NT
      - id: v3_C_X_shape
        call: X
        priority: 69
        requires:
          hcp: [11, 13]
          suits: { C: [0, 2], S: [3, 13], H: [3, 13], D: [3, 13] }
          evals: { longest_suit_length: [0, 5] }
        shows: "shapely takeout double of the three-level preempt: 11-13, at most a doubleton in their suit and three-plus cards in every unbid suit"
        establishes: { forcing: one_round }
```

**Answering seat.**  `forcing: one_round`.  `3C - X - P - ?` is owned by
`general_pull_or_sit`, and it is populated at the three and four level
(`adx_pull_$X3`, `adx_pull_$X4`, `adx_pass_min`, `adx_sit`).  **Traced:** a
5-3-2-3 nine-count answers 3D at fit 1.000 (`adx_pull_D3`).  This is not a
starved ask.

**Endangers.**  `v3_C_X` (70) — above me, so the 14-17 reading stays primary;
`v3_C_3NT` (66) — below, and 3NT with a singleton in their suit is a fantasy;
`v3_C_4S` (65), `v3_C_S/H/D` (64) — below, and with 5-4 in the majors the
double finds both suits where the overcall picks one; `v3_C_pass` (30) — the
population I am taking, which measures **-0.80 (5 tables) / +3.00 (3 tables)**:
tiny and non-replicating, so this rung is justified on bridge, not on the
denominator.  **No fallback is deleted:** X was already covered by `v3_C_X`,
which is `when`-less.

**VERIFIED** — bids X, `v3_C_X_shape` fit 1.000, score 0.907.

**Template.**  `expand: { X: [C, D, H, S] }` across all four
`defense_vs_preempt_$X` contexts — the four are written out longhand today, so
four rungs.  The identical agreement at the two level is board 282
(`vw2_X_three`) and in the passout seat is board 934 (`balhigh_X_shape`); the
three should ship as one family.

---

## Board 206 — -2 IMPs — table B, call 1, seat W: `P` over 1C

**Missing agreement.**  A 1C opening may be three cards long, so shortness in
clubs is not the test — the takeout double of a MINOR opening promises
three-plus cards in every other suit and opening values.

`K92.AK98.T93.Q86` is a 12-count, 3=4=3=3.  `oc1C_X` requires `C: [0, 2]` and
fits 0.349 on a one-card length miss.

```yaml
      # in context overcalls_of_1C, immediately before oc1C_1S
      - id: oc1C_X_minor
        call: X
        priority: 71.5
        requires:
          hcp: [12, 16]
          suits: { C: [0, 3], S: [3, 5], H: [3, 5], D: [3, 13] }
        shows: "takeout double of their MINOR: opening values and three-plus cards in every other suit - a 1C opening may be three cards, so shortness in it is not the test"
        establishes: { forcing: one_round }
```

**Answering seat.**  `forcing: one_round`; `advance_takeout_double_suits_C`
(`1C - X - P - ?`) already exists and is unchanged.

**Endangers.**  `oc1C_1NT` (82) — above me, so 15-18 balanced with a club
stopper still bids 1NT; `oc1C_X` (72) — above me, so the classic short-club
double stays primary; `oc1C_1S` / `oc1C_1H` (71) and `oc1C_1H_shape` (70.5,
board 112) — below me, and the `S: [3, 5]` / `H: [3, 5]` ceilings mean I cannot
fire with a six-card major, while with a *five*-card major the 12-16 double
followed by bidding the suit is the stronger sequence; `oc1C_1D` (70);
`oc1C_pass` (25), the population I take.
No fallback deleted (X already covered by `oc1C_X`).

**VERIFIED** — bids X, `oc1C_X_minor` fit 1.000, score 0.914.

**Template.**  `expand: { m: [C, D] }` — the same rung belongs in
`overcalls_of_1D`.  Do **not** extend it to major openings: a 1H/1S opening
guarantees five, so shortness there is a real test.

---

## Board 227 — -2 IMPs — table A, call 3, seat S: `X` over `1D P 1S`

**Missing agreement.**  The sandwich seat has no natural notrump at all: a
15-18 balanced hand with a stopper must bid 1NT, not double with four cards in
their suit.

`QJT2.K3.K32.AQT2`: 15 HCP, four spades — RHO's suit — three diamonds, so
neither branch of `sw_X` is satisfied.  It fired anyway at **fit 0.409**, the
soft-miss lottery, because the only 1NT candidate in the context is the
undiscussed code fallback ("6-11 HCP") at priority 10 and fit 0.028.

```yaml
      # in context sandwich_seat, immediately before sw_1S
      - id: sw_1NT
        call: 1NT
        priority: 71
        requires:
          hcp: [15, 18]
          evals: { semi_balanced: [1, 1] }
          features: [ "stopper($o)" ]
          not: { any_of: [ { suits: { H: [5, 13] } }, { suits: { S: [5, 13] } } ] }
        shows: "natural notrump in the sandwich seat: 15-18 balanced, opener's suit stopped, no five-card major"
        establishes: { forcing: non_forcing }
```

**Answering seat.**  Non-forcing.  `advance_1NT_overcall` is patterned
`1$o - 1NT - P - ?` and does **not** match the sandwich shape `1$o - P - 1$v -
1NT - P - ?`; that seat falls to `general_uncontested_continuation`, which has
the full `uc_new_*` / `uc_raise_*` ladder.  Acceptable, but flagging it: a
`sandwich_1NT_advance` context is the natural follow-up and I have not written
one.

**Endangers.**  `sw_X` (70) — I am deliberately ABOVE it, because a 17-count
4-3-3-3 fits `sw_X`'s shapeless `hcp: [17, 40]` branch at 1.000 and 1NT is the
better description of that hand; the `semi_balanced` and stopper gates mean I
can only take balanced hands with a stopper.  `sw_1S` / `sw_1H` (68) — the
`not: five-card major` clause keeps them: with five spades you bid spades.
`sw_2C`/`sw_2D`/`sw_2H`/`sw_2S` (66), `sw_3$X` (69.5) — a preemptive jump or a
two-level overcall is not a 15-18 balanced hand.  `sw_pass` (30), which fires
**247/240 tables at -0.49 / -0.66**.
**Fallback deleted:** the undiscussed 6-11 1NT.  That is a gain — bidding a
weak notrump between two bidding opponents is the losing action, and `sw_X`
measures **-1.70 (23 tables) / +1.35 (17)**, i.e. this whole seat is noisy and
under-authored.

**VERIFIED** — bids 1NT, `sw_1NT` fit 1.000, score 0.913.

**Template.**  The context is already `expand: { o: [C, D, H, S] }`, so one
rung gives four.  A `sw_2NT` (19-21) rung above it is the obvious sibling and I
have not written it.

---

## Board 241 — -2 IMPs — table A, call 3, seat N: `P` over `2S 3D 3S`

**Missing agreement.**  The Law at the four level exists only for the majors:
with nine trumps ours, nine theirs and a void in their suit, eighteen total
trumps make four of partner's MINOR our level too.

`.T9.AT83.AJ97532`: spade void, four-card support for partner's 3D overcall
(`lott_total_trumps(D) = 9`), `their_fit = 9` after 2S-3S, 12 total points and
`rule_of_26 = 25`.  `ch_raise_D4` fails on exactly one gate,
`lott_total_trumps >= 10`, and `_EVAL_S2["lott_total_trumps"] = 0.4` makes that
a sharp miss: fit **0.082**.

```yaml
      # in general_competitive_high, immediately before ch_raise_D4
      - id: ch_raise_lott4_D
        call: 4D
        priority: 32
        when: { partner_suit: D, is_competitive: true }
        requires:
          suits: { D: [4, 13] }
          evals: { "lott_total_trumps(D)": [9, 26], their_fit: [9, 26], standing_suit_length: [0, 1],
                   total_points: [9, 40], "suit_diff(D, H)": [0, 13], "suit_diff(D, S)": [0, 13] }
        shows: "the Law at the four level in a minor: nine trumps ours, nine theirs, and a singleton or void in their suit - eighteen total trumps make the four level ours"
        establishes: { forcing: non_forcing, agreed_suit: D }
```

The `standing_suit_length: [0, 1]` clause is what separates this from a blanket
"nine trumps, bid four": it is a *shape* licence, not a values licence, and the
sharp `_S2 = 0.95` on `standing_suit_length` makes it a real gate.

**Answering seat.**  Non-forcing.  `general_competitive_high` /
`general_balancing_high` answer it; `agreed_suit: D` routes any continuation to
the diamond RKC ladder that already exists.

**Endangers.**  `ch_penalty_X` (38), `ch_negative_X3` (33) — above me, and a
penalty double with a void in their suit does not fit anyway; `ch_raise_lott4_H
/ _S` (32) — same priority, different `partner_suit`, disjoint;
`ch_new_C4_hi/C4` (28.5/28) — below me: with seven clubs and four diamonds this
is the one case where the choice is live, and raising partner's *known* suit
beats introducing my own at the four level opposite a passed-out preempt
auction; `ch_raise_D4` (27) — below me, and it is the values-based rule this
one deliberately does not duplicate; `ch_pass` (22), which measures
**-0.72 / -0.69 on 794/795 tables**.
**Fallback:** 4D was already covered by `ch_raise_D4` (`when: partner_suit: D`),
so nothing is deleted.  `ch_raise_D4` itself fires 0/1 times in the two corpora
— this is a genuinely empty region of the file, not a contested one.

**VERIFIED** — bids 4D, `ch_raise_lott4_D` fit 1.000, score 0.796.  (4D makes
eleven tricks double-dummy.)

**Template.**  `expand: { m: [C, D] }` in `general_competitive_high`,
`general_competitive_low`, `general_balancing_high` and
`general_balancing_low` — eight rungs, mirroring where `*_raise_lott4_$M`
already lives for the majors.

---

## Board 252 — -2 IMPs — table B, call 3, seat W: `3C` over `P 1C 2NT`

**Missing agreement.**  A six-card major outranks the raise of partner's minor
in competition — partner's clubs will still be there.

`K76432.9.A.KQ852`: six spades, five clubs, 12 HCP.  `cl_raise_C3` (31) and
`cl_new_long3_S` (27) BOTH fit 1.000; priority hands the auction to the minor
raise, and the auction then ran 3C - 4D - P - P - 5C for -620.

```yaml
      # in general_competitive_low, immediately before cl_raise_C4
      - id: cl_major6_S3
        call: 3S
        priority: 31.5
        when: { unbid_suit: S, cheapest_in_suit: true }
        requires:
          suits: { S: [6, 13] }
          evals: { total_points: [11, 40], "suit_quality(S)": [1, 9] }
        shows: "a SIX-card major outranks the raise of partner's minor: 6+ spades, 11+ points"
        establishes: { forcing: non_forcing }
```

**Answering seat.**  Non-forcing.

**Endangers — read this one carefully, it is the round-14 species.**
`cl_takeout_X` (36), `cl_reopen_X` (35), `cl_negative_X2_both` (33.5),
`cl_negative_X*` (33) — all above me, untouched.  Below me:
`cl_raise_C3` / `cl_raise_D3` (31) — the intended target, and the bridge is that
a six-card major is a better description of the hand than three-card support
for a minor; `cl_raise_H3` / `cl_raise_S3` (31) — cannot collide, because if
partner bid the major it is not an `unbid_suit`; `cl_raise_lott3_$M` (32) — ABOVE
me, so the preemptive major raise is untouched; `cl_new_long3_S` (27) and
`cl_new_S3_hi` (27.5) — my own strict subset, they simply never win where I do.
**Denominator:** `cl_raise_C3` measures **-0.78 (9 tables) / +3.50 (6 tables)** —
mixed, small, non-replicating.  This is a re-rank in effect and it is the single
proposal in my list I would most want measured on its own.
**Fallback:** 3S was already covered by `cl_new_S3` etc.

**VERIFIED** — bids 3S, `cl_major6_S3` fit 1.000, score 0.794 (vs `cl_raise_C3`
0.793 — a deliberately narrow margin).

**Template.**  `expand: { M: [H, S] }`, and a two-level twin `cl_major6_$M2` at
30.5 (above `cl_raise_$m2` at 30) plus the `ch_`, `ballow_` and `balhigh_`
mirrors — sixteen rungs from one idea.

---

## Board 262 — -2 IMPs — table A, call 8, seat S: `P` over `... 1S X 2C 2H`

The board's first divergence is the **opening decision** (`KQJ84.3.QJ54.Q84`,
rule of 20 = 20), which is scope-excluded, so I am ruling on the competitive
call further down the auction.

**Missing agreement.**  The overcaller's rebid ladder demands SIX cards at every
level, so a good five-card overcall suit has no rebid at all once they compete.

`cl_rebid_S2` needs `S: [6, 13]` and fits 0.349 on a one-card length miss;
`cl_pass` takes the seat at fit 1.000.

```yaml
      # in general_competitive_low, immediately before cl_rebid_S3
      - id: cl_rebid5_S2
        call: 2S
        priority: 28.5
        when: { my_suit: S, cheapest_in_suit: true }
        requires:
          suits: { S: [5, 13] }
          evals: { total_points: [11, 40], "suit_quality(S)": [2.5, 9] }
        shows: "rebid of my own five-card S at the two level: a suit good enough to play opposite a doubleton, and the values for the level"
        establishes: { forcing: non_forcing }
```

The `suit_quality >= 2.5` gate is the whole point — `KQJ84` scores 3.0, a
five-card suit worth repeating; `Q8432` scores 1.0 and is not.

**Answering seat.**  Non-forcing.

**Endangers.**  `cl_takeout_X` / `cl_reopen_X` (36/35), `cl_negative_*` (33+),
`cl_raise_*3` (31), `cl_rebid_jump_S` (31), `cl_nt3` (29), `cl_rebid_S2` (29) —
all above me, so the six-card reading and every stronger action stay primary;
`cl_nt2` (28), `cl_new_*` (25-27.5) — below me, and repeating a solid five-card
suit partner has already heard beats introducing a new one; `cl_pass` (20),
which fires **707/690 tables at -0.81 / -0.49**.
**Fallback:** 2S was already covered by `cl_rebid_S2` (identical `when`).

**VERIFIED** — bids 2S, `cl_rebid5_S2` fit 1.000, score 0.785.

**Template.**  `expand: { X: [C, D, H, S] }` at the two AND three level (the
three-level version is board 928's `cl_rebid5_D3`), in `general_competitive_low`,
`general_competitive_high`, `general_balancing_low` and
`general_balancing_high` — thirty-two rungs.  Also note for the consolidator:
`general_competitive_high` should get the `ch_reopen_X` twin of board 2's rung
in the same edit; `general_competitive_high` has **no takeout double at all**
(only `ch_penalty_X` and `ch_negative_X3`), which is a second, independent hole
this board's table B walks past.

---

## Board 266 — -2 IMPs — table A, call 6, seat N: `2H` over partner's support double

**Missing agreement.**  Partner's support double showed three-card support for
MY suit, so with six trumps the pull is to game, not to the two level.

`J983.KQ9853.7.QJ`: six hearts, singleton diamond, 9 HCP + shortness.  Partner
has shown exactly three hearts, so `lott_total_trumps(H) = 9`.
`adx_pull_my_H` (59, "pulling partner's double back to my own suit") fits 1.000
and outranks `uc_raise_H4` (32), which ALSO fits 1.000 — the right call was
sitting there two priorities down.

```yaml
      # in general_pull_or_sit, immediately before adx_neg_major_H2
      - id: adx_pull_game_H
        call: 4H
        priority: 63
        when: { my_suit: H, partner_suit: H }
        requires:
          suits: { H: [6, 13] }
          evals: { "lott_total_trumps(H)": [9, 26], total_points: [10, 40] }
        shows: "partner's double showed support for my own suit: six trumps opposite three is a nine-card fit, so the pull is to game"
        establishes: { forcing: sign_off, agreed_suit: H }
```

Note the `partner_suit: H` conjunct with `my_suit: H`: that pair is *only* true
after a support double or a raise, which is exactly the auction this describes.

**Answering seat.**  `sign_off` — no answer required, and `agreed_suit: H`
means any later slam move routes through the existing heart RKC ladder.

**Endangers.**  `adx_neg_major_$M2/3` (62) — above me, untouched; `adx_sit` (61)
— above me, and with a singleton in their suit it cannot fit; `adx_pull_my_H`
(59) — the intended target, and its own `shows` sentence ("pulling back to my
own suit") is the *right* description at the two level and the wrong one when
partner has already raised me to a nine-card fit; `adx_nt` (56),
`adx_pass_min` (52), `uc_raise_H4` (32) — all below.
**Denominator:** `adx_pull_my_H` measures **-2.20 (5 tables) / -2.00 (6 tables)**
— a small population, losing on BOTH corpora.  This is the cleanest indictment
in my slice.
**Fallback:** 4H was already covered by `uc_raise_H4`.

**VERIFIED** — bids 4H, `adx_pull_game_H` fit 1.000, score 0.889.  (4H makes
eleven.)

**Template.**  `expand: { M: [H, S] }` — two rungs.  A 3M invitational twin at
62.5 (five trumps, 8-9 points) is the obvious sibling and I have not written it.

---

## Board 273 — -2 IMPs — table B, call 2, seat W: `3S` over `3C 3D`

**Missing agreement.**  With a singleton in partner's preempt suit, no six-card
suit of my own and less than a game force, pass — a free bid at the three level
turns his plus into a minus.

`AKQT6.KJ43.953.2`: 13 HCP, five spades, singleton club opposite a 3C preempt.
`ch_free_3S` fits 1.000 at priority 30 and we went for -200 where passing 3D
scores the same as the other table.  BEN passes at only 0.47, so I would not
propose this on BEN's authority — I propose it on the Law: partner has at most
nine HCP and a seven-card suit, my hand has one card in it, and 3S is a
five-card suit opposite a singleton.

```yaml
      # in general_competitive_high, immediately before ch_free_3H
      - id: ch_pass_opposite_preempt
        call: P
        priority: 30.5
        when: { side_has_acted: true, i_have_acted: false }
        requires:
          hcp: [0, 15]
          evals: { partner_shown_max: [0, 10], longest_suit_length: [0, 5],
                   "suit_length(partner)": [0, 1] }
        shows: "misfit with partner's preempt: a singleton in his suit, no six-card suit of my own and no game force - a free bid at the three level turns his plus into a minus"
        establishes: { forcing: non_forcing }
```

`partner_shown_max <= 10` is what makes this "opposite a preempt" and not
"opposite an opening bid"; after a 3C preempt the evaluator returns **9.0**
(traced).

**Answering seat.**  Pass; none needed.

**Endangers.**  `ch_penalty_X` (38), `ch_negative_X3` (33) — above me, so a
double is unaffected; `ch_raise_*` (30-32) — with a singleton in partner's suit
none of them can fit, so no raise is lost; `ch_free_3H` / `ch_free_3S` (30) —
the intended target, measuring **-1.50 (4 tables) / +0.00 (4 tables)**;
`ch_new_*` (25-28.5) — below me, and the same argument applies to them.
**Fallback:** P is already covered by `ch_pass`, so nothing is deleted.
This is the same agreement as board 289's `rw2_pass_misfit`, in the seat where
they have competed rather than passed.

**VERIFIED** — bids P, `ch_pass_opposite_preempt` fit 1.000, score 0.791
(against `ch_free_3S` 0.790 — deliberately the narrowest margin in my list, so
that any hand with a sixth card or a doubleton in partner's suit still bids).

**Template.**  One rung; `suit_length(partner)` and `partner_shown_max` are
both suit-free.  It belongs in `general_competitive_low` and
`general_balancing_*` as well — four rungs.

---

## Board 282 — -2 IMPs — table B, call 3, seat E: `P` over their weak 2H

The board's first divergence is the third-seat opening style (scope-excluded:
BEN's `2H` is not even legal in our system, which requires exactly six).  I am
ruling on table B.

**Missing agreement.**  The takeout double of a weak two is available on 12-16
with three small in their suit when the hand holds two four-card suits
including a major — you cannot always be short.

`AQ42.984.73.AQ74`: 12 HCP, three hearts, four spades and four clubs.  `vw2_X`
misses on both its gates at once (13 HCP floor and `H: [0, 2]`) and fits 0.279.

```yaml
      # in defense_vs_weak2_overcalls3, immediately before vw2_2NT
      - id: vw2_X_three
        call: X
        priority: 69
        requires:
          hcp: [12, 16]
          suits: { $W: [0, 3] }
          evals: { longest_suit_length: [0, 5], weakest_unbid_length: [2, 13] }
          any_of:
            - suits: { H: [4, 13], C: [4, 13] }
            - suits: { H: [4, 13], D: [4, 13] }
            - suits: { S: [4, 13], C: [4, 13] }
            - suits: { S: [4, 13], D: [4, 13] }
        shows: "takeout double of the weak two on shape: 12-16 with at most three in their suit and two four-card suits including a major"
        establishes: { forcing: one_round }
```

**Answering seat.**  `forcing: one_round`; `advance_weak2_double_H` (`2H - X -
P - ?`) already exists for D/H/S, plus `advance_weak2_double_raised`.  Not a
starved ask.

**Endangers.**  `vw2_2NT` (72) — above me; `vw2_X` (70) — above me, the 13-16
short reading stays primary; `vw2H_over_2S` and the `vw2_*` overcalls (64-66) —
below me, and with 4-4 and no five-card suit the double describes the hand and
an overcall does not; `vw2_shadow*` (26) and `vw2_pass` (30), which fires
**52/53 tables at -0.60 / -0.79**, a replicating loser.
**Fallback:** X already covered by `vw2_X`.
Honest caveat: BEN's confidence for the double here is only 0.58, and E's
doubleton diamond is the flaw in the hand.  The `weakest_unbid_length: [2, 13]`
clause is a soft acknowledgement of that rather than a hard gate.

**VERIFIED** — bids X, `vw2_X_three` fit 1.000, score 0.907.

**Template.**  The context is already `expand: { W: [D, H, S] }` — one rung
gives three.  Same family as boards 195/417 (`v3_$X_X_shape`) and 934
(`balhigh_X_shape`); ship them together.

---

## Board 289 — -2 IMPs — table A, call 3, seat N: `2S` over partner's weak 2D

**Missing agreement.**  With a singleton or void in partner's preempt suit and
less than a game force, pass — a forcing new suit only drives us past his own
contract with no fit anywhere.

`KQ963.A9632.3.K4`: 12 HCP, 5-5 in the majors, **singleton diamond**.
`rw2_new_D_S` fits 1.000 at priority 63, partner rebid 3D and we played it one
down instead of 2D.

```yaml
      # in the weak-two response context, immediately before rw2_2NT_ask
      - id: rw2_pass_misfit
        call: P
        priority: 64
        requires:
          hcp: [0, 15]
          suits: { $W: [0, 1] }
        shows: "misfit with the preempt: a singleton or void in partner's suit and less than a game force - a new suit only drives us past his own contract"
        establishes: { forcing: non_forcing }
```

**Answering seat.**  Pass; none needed.

**Endangers.**  `rw2_2NT_ask` (70) — above me, so a genuine 15+ feature ask
still happens; `rw2_new_$W_$X` (63) — the intended target, and the bridge is
that the file's own comment records this species (**"The forcing new suit
opposite a weak two is passed out"** is a KNOWN OPEN ITEM: `2$W - P - <new
suit> - P - ?` has no context, so the force is answered by `uc_pass` at fit
1.00).  Rather than build that missing context, this rung stops us entering it
on the hands where the answer cannot help; `rw2_raise3` (60) — below me, and
with a singleton you are not raising; `rw2_pass` (40).
**Denominator:** `rw2_new_D_S` fires **2 tables at +4.50** (r18) and never in
the held-out corpus — so this is a rung firing twice, once well and once badly.
Small population; the `$W: [0, 1]` gate is very narrow and takes only the
misfits.
**Fallback:** P already covered by `rw2_pass`.

**VERIFIED** — bids P, `rw2_pass_misfit` fit 1.000, score 0.892.

**Template.**  The context is already expanded over the weak-two suit — one
rung gives three.  The same sentence in the competitive seat is board 273.

---

## Board 320 — -2 IMPs — NOTHING-WRONG

`AJ854.QT.QT94.J5` bidding 2S over `P 1H P 2H` is exactly what `cl_new_S2`
says — five spades, 11 total points — and 2S over their raise at equal
vulnerability is a normal matchpoint action; BEN's 0.98 pass is a style
difference, not a defect.  The IMPs came from partner's `4S` save
(`ch_raise_lott_S4`: five trumps, ten combined, non-vul), which went -500
against a -450 game: **a 50-point loss on a save the Law endorses** (10 + 9 = 19
total trumps; the hands produced 18 tricks).

**Reported negative.**  I prototyped splitting `ch_raise_lott_S4` on
`they_vulnerable`, keeping the current gate at favourable vulnerability and
demanding an eleventh trump or a void at equal.  I am not proposing it: it
subtracts from a rule that is doing what the Law says on a board where the Law
was one trick out, the corpus evidence is a single 50-point swing, and the
adjustment the hand actually wants (`QT` of their trumps is wasted on offence)
is not expressible with the evaluators in the file.

Also checked: N's `cl_takeout_X` (fit 0.409 — 10 HCP against a 12 floor) and
table B's `r1H_limit_raise` on a 7-count with a singleton (correct: 10 support
points).

---

## Board 347 — -2 IMPs — table B, call 4, seat W: `P` over their 2S

**Missing agreement.**  When they overcall our transfer, raise to the level of
the fit — the raise must be priced on trumps, because a transfer promises no
values for `rule_of_26` to count.

`A876.Q3.AT96.KQJ`: 16 HCP, four-card support for the spades partner
transferred to, `lott_total_trumps(S) = 9`.  `cl_raise_S3` fits **0.800** — a
one-point miss on `rule_of_26 >= 22`, because partner's shown minimum after a
transfer is nearly zero.  This is the same mechanism as the ledger's "after a
2C opening partner's shown minimum is ZERO by construction", in a different
tree.

```yaml
      # in general_competitive_low, immediately before cl_raise_S4
      - id: cl_raise_lott_S3
        call: 3S
        priority: 30.5
        when: { partner_suit: S, cheapest_in_suit: true, is_competitive: true }
        requires:
          suits: { S: [4, 13] }
          hcp: [14, 40]
          evals: { "lott_total_trumps(S)": [9, 26] }
        shows: "raise to the level of the fit: four-card support, nine combined trumps and a good hand - priced on trumps, not on a combined-point count partner has never promised"
        establishes: { forcing: non_forcing, agreed_suit: S }
```

The `hcp: [14, 40]` floor is what replaces `rule_of_26`: it puts the values
requirement on MY hand, where they can be counted, instead of on a sum with an
unknown.

**Answering seat.**  Non-forcing, `agreed_suit: S`; partner's next seat is
`general_competitive_high`, populated.

**Endangers.**  `cl_takeout_X` (36) and the negative doubles (33-33.5) — above
me, untouched; `cl_major6_S3` (31.5, board 252) — above me, but requires an
UNBID spade suit, so disjoint; `cl_raise_S3` (31) — above me, the values-based
reading stays primary and I take only the hands it drops; `cl_raise_lott3_$M`
(32) — above me, and its 3-10 point band cannot overlap my 14+ floor;
`cl_raise_S2` (30) — 2S is not legal here; `cl_nt3` (29), `cl_nt2` (28),
`cl_new_*` (25-27.5) — below me, and four-card support for a known five-card
suit is the better description; `cl_pass` (20).
**Fallback:** 3S already covered by `cl_raise_S3` (identical `when` less
`is_competitive`).

**VERIFIED** — bids 3S, `cl_raise_lott_S3` fit 1.000, score 0.791.

**Template.**  `expand: { M: [H, S] }` plus a minor version, in
`general_competitive_low/high` and `general_balancing_low/high`.  A more
specific context for `1NT - P - 2$T - bid - ?` (their overcall of our transfer)
is the structurally right home for a penalty double here, and I have
deliberately NOT written it: it would shadow `general_competitive_low` and
would have to carry all of its gates verbatim.

---

## Board 360 — -2 IMPs — table A, call 2, seat S: `2H` over `1NT 2C`

**Missing agreement.**  The negative double over their overcall of our notrump
shows BOTH majors — holding five of one does not deny four of the other.

`KJ84.QJ872.K32.5`: four spades AND five hearts opposite a 15-17 notrump.
`cl_negative_X2` carries `longest_suit_length: [0, 4]`, which is the right
denial at the ONE level (where you can bid the suit cheaply) and the wrong one
here: it fits 0.349, `cl_new_H2` takes the seat, and the 4-4 spade fit — worth
+450 at the other table — is never found.

```yaml
      # in general_competitive_low, immediately before cl_raise_lott3_H
      - id: cl_negative_X2_both
        call: X
        priority: 33.5
        when: { their_last_bid_suit: true, side_has_acted: true, i_have_acted: false, standing_bid_level: [2] }
        requires:
          hcp: [8, 40]
          suits: { H: [4, 13], S: [4, 13] }
          evals: { "suit_length(their)": [0, 3] }
        shows: "negative double at the two level showing BOTH majors: four-plus in each, 8+ HCP - holding five of one does not deny the other"
        establishes: { forcing: one_round }
        convention: negative_double
```

**Answering seat.**  `forcing: one_round`.  **Traced end to end:** partner
(`AQ73.A9.J74.AT76`) answers `2S` via `adx_neg_major_S2` at fit 1.000 — the
rung whose `shows` is literally "answering partner's negative double in the
major it promised".  The 4-4 fit is found, and 4S is par.

**Endangers.**  `cl_takeout_X` (36) / `cl_reopen_X` (35) — above me;
`cl_negative_X1` / `cl_negative_X2` (33) — directly below, and mine is a strict
special case (both majors) of what they describe, so nothing they catch is
lost; `cl_raise_lott3_$M` (32) — below, and with 4-4 majors I have no fit to
raise; `cl_new_H2_hi` / `cl_new_H2` (26.5 / 26) — the intended target, and the
double finds two fits where 2H finds one.
**Denominator:** `cl_negative_X2` measures **-2.07 (15 tables) / -0.80 (15
tables)** — losing on both corpora, so widening the double's population is a
bet against a rule that is already underwater; the mitigation is that my rung
requires four cards in BOTH majors, which is a much better-defined hand than the
parent rule's "a major they have not bid".
**Fallback:** X already covered by `cl_negative_X2`.

**VERIFIED** — bids X, `cl_negative_X2_both` fit 1.000, score 0.800; partner
answers 2S.

**Template.**  One rung at the two level; a `cl_negative_X1_both` twin at the
one level (priority 33.5) and a `ch_negative_X3_both` at the three level.  The
three-level version matters most: see board 933's table B.

---

## Board 372 — -2 IMPs — table A, call 4, seat N: `P` converting partner's negative double

**Missing agreement.**  Opener does not convert a NEGATIVE double for penalty
at the one level — it is takeout and it promised the other major, not defence;
opener answers it.

`AK95.A9.K654.943` after `1D (1S) X P`.  `adx_sit` ("sitting the double: real
trumps behind them", priority **61**, `general_pull_or_sit`, specificity 4)
beats every rule in `opener_over_negative_double` (specificity 1005) because
the two contexts produce DIFFERENT calls, so specificity never arbitrates and
priority does.  We defended 1SX for +100 where par is +600.

The fix is a re-rank inside `opener_over_negative_double`, +5 across the board,
so relative order inside the context is untouched and only the comparison
against the generic pass changes:

```yaml
      # context opener_over_negative_double — priorities only
      - id: onx_major1_$m$M   # 1$oM   61  ->  66
      - id: onx_major_$m$M    # 2$oM   60  ->  65
      - id: onx_jump_$m$M     # 3$m    59  ->  64
      - id: onx_jumpnt_$m$M   # 2NT    58.5 -> 63.5
      - id: onx_nt_$m$M       # $nt    58  ->  63
      - id: onx_rebid_$m$M    # 2$m    57  ->  62
```

**Answering seat.**  Nothing becomes forcing; this only re-orders opener's
existing non-forcing rebids.

**Endangers — THIS SUBTRACTS `adx_sit` FROM ONE FAMILY OF AUCTIONS.**  After the
bump, `adx_sit` (61) can no longer win in `1$m - 1$M - X - P - ?`.  That is the
intent: `adx_sit` requires only four cards in their suit and
`suit_quality >= 1.5` with **no HCP condition at all**, so it converts a
negative double on any hand from 8 to 20.  Everywhere else — partner's takeout
double of their opening, partner's penalty double of a high contract —
`adx_sit` is untouched, because those auctions are not `1m - 1M - X - P`.
**Denominator:** `adx_sit` fires **27/28 tables at +0.15 / +0.11** — essentially
neutral over the whole corpus, and the sub-population this removes is the four
`1$m - 1$M` patterns only.  `onx_rebid_DS` measures **-2.00 on 5 tables**.

**VERIFIED** — bids 1NT, `onx_nt_DS` fit 1.000, score 0.889 (against `adx_sit`
0.883).

**Template.**  Six priority edits inside one `expand_pairs` context = 24 rules.
The general lesson for the consolidator: any context more specific than
`general_pull_or_sit` that owns a seat must be priced ABOVE 61, or the generic
pass annexes it.

---

## Board 392 — -2 IMPs — NOTHING-WRONG

Entirely uncontested at both tables.  `Q983.QT8.K64.843` (7 HCP) passing a
15-17 notrump versus bidding Stayman on a 4-3-3-3 seven-count is a
constructive-lane judgement about the Stayman floor (`nt_stayman` requires
"invitational+ values" and fits 0.800 here).  Checked on the competitive side:
our E passed the 1NT at table B holding a balanced nine (`v1NT_pass`, correct —
the direct-seat defence to a strong notrump needs a suit), and no seat in either
auction had a competitive decision to make.

---

## Board 395 — -2 IMPs — table A, call 3, seat S: `P` over `1NT 2H`

**Missing agreement.**  A five-card suit at the two level is bid on length and
values; the honour requirement belongs to the rungs above, not to the whole
ladder.

`T9853.85.AJT5.A4`: 10 total points, five spades.  `suit_quality(T9853) = 0.5`
against a 1.5 gate, so `cl_new_S2` fits 0.329 and the hand sells out to their
overcall of our own 1NT opening — with a known 15-17 opposite.

```yaml
      # in general_competitive_low, immediately before cl_new_C3
      - id: cl_new_S2_values
        call: 2S
        priority: 24.5
        when: { unbid_suit: S, cheapest_in_suit: true }
        requires:
          suits: { S: [5, 13] }
          evals: { total_points: [10, 40] }
        shows: "natural S at the cheapest level on length and values: 5+ cards, 10+ points, no honour requirement"
        establishes: { forcing: non_forcing }
```

**Answering seat.**  Non-forcing.

**Endangers — deliberately placed BELOW everything.**  At 24.5 it is under
`cl_new_S1` and `cl_new_C1`/`cl_new_D1` (25), so a four-card suit at the ONE
level is still preferred; under `cl_new_S2`/`_hi` (26/26.5), so the
quality-bearing reading stays primary; under `cl_nt1` (27), so a balanced 8-11
with a stopper still bids notrump; under everything else in the context.  Its
only victim is `cl_pass` (20), which fires **707/690 tables at -0.81 / -0.49**.
**Fallback:** 2S already covered by `cl_new_S2` (identical `when`), so nothing
is deleted.  `cl_new_S2` itself measures **-1.93 (15) / +1.26 (19)** — mixed —
and my rung does not touch that population, it only fills the hole beneath it.

**VERIFIED** — bids 2S, `cl_new_S2_values` fit 1.000, score 0.773.

**Template.**  `expand: { X: [C, D, H, S] }` at the two and three level in
`general_competitive_low/high` and `general_balancing_low/high` — thirty-two
rungs, with the majors at 24.5 and the minors at 24.0 so a major is preferred.
Board 2 is the three-level case of the same tax (`cl_new_D3` fit 0.757 on a
16-count with `K9752`) and is separately fixed there by `cl_reopen_X`.

---

## Board 411 — -2 IMPs — table A, call 1, seat N: `2D` over 1H

**Missing agreement.**  A two-level overcall needs opening values or a
six-card suit: eleven soft high-card points in a 3-3-5-2 hand is a pass.

`QJ2.T84.AQT64.Q3` — `QJ2`, `T84`, `Q3` are three tricks that never take one on
offence.  `oc1H_2D` fits 1.000 on `hcp: [11, 17]`, we played 3D one down and
the other table was passed out.

```yaml
      # replaces the requires block of oc1H_2D (and its three siblings)
      - id: oc1H_2D
        call: 2D
        priority: 65
        requires:
          evals: { suit_quality(D): [1.5, 9] }
          any_of:
            - suits: { D: [5, 13] }
              hcp: [12, 17]
            - suits: { D: [6, 13] }
              hcp: [11, 17]
        shows: "2-level overcall: 5+ good diamonds and opening values, or a six-card suit on 11"
```

**Answering seat.**  Unchanged.

**Endangers — THIS IS A GATE.**  It subtracts exactly one population:
eleven-HCP two-level overcalls on a five-card suit.  Everything above it
(`oc1H_1NT` 82, `oc1H_X` 72, `oc1H_1S` 71, `oc1H_1S_values` 70.5) is untouched;
below it, `oc1H_3D_jump` (59) picks up the six-card weak hands and `oc1H_pass`
(25) picks up the flat elevens.
**Denominator:** `oc1H_2D` measures **-1.22 (9 tables) on r18 and +0.62 (8
tables) held out** — it does not replicate, so this is a one-point band change
justified on the system's own doctrine ("2-level 11-17 **with a good 5+ suit**",
DECISIONS) rather than on the corpus.  The engine's own DECISIONS entry says the
two-level overcall shows opening values; the requires block says 11.

**VERIFIED** — bids P; `oc1H_2D` drops to fit 0.800 and `oc1H_pass` wins at
1.000/0.775.

**Template.**  The same `any_of` restructure on all twelve `oc1$o_2$v` rungs
across the four overcall contexts, and on the four `sw_2$X` sandwich twins
(which already floor at 11).

---

## Board 417 — -2 IMPs — table A, call 1, seat S: `P` over 3H

Same agreement as board 195, in the other preempt context.

**Missing agreement.**  A 13-count with a doubleton in their suit and four
cards in two of the three unbid suits doubles a three-level preempt; the 14-HCP
floor is one point too high and turns a textbook double into a pass.

`A932.86.KQ4.KJT8`: 13 HCP, `86` in hearts, 4-3-4 in the unbid suits.
`v3_H_X` fits **0.800** — a single-point miss on the hcp gate.

```yaml
      # in defense_vs_preempt_H, immediately before v3_H_3NT
      - id: v3_H_X_shape
        call: X
        priority: 69
        requires:
          hcp: [11, 13]
          suits: { H: [0, 2], S: [3, 13], D: [3, 13], C: [3, 13] }
          evals: { longest_suit_length: [0, 5] }
        shows: "shapely takeout double of the three-level preempt: 11-13, at most a doubleton in their suit and three-plus cards in every unbid suit"
        establishes: { forcing: one_round }
```

**Answering seat.**  `forcing: one_round`; `general_pull_or_sit` answers, and I
traced a five-card-diamond bust answering `4D` at fit 1.000.

**Endangers.**  Identical to board 195: `v3_H_X` (70) above, `v3_H_3NT` (66),
`v3_H_4S` (65), `v3_H_S/C/D` (64) below — with a 4-3-4 hand and no six-card
suit none of them is a better description — and `v3_H_pass` (30), which
measures **+1.00 (3 tables) / -3.40 (5 tables)**: tiny and non-replicating in
both directions, so this is a bridge argument, not a corpus argument.
**No fallback deleted** (X already covered by `v3_H_X`).

**VERIFIED** — bids X, `v3_H_X_shape` fit 1.000, score 0.907.

**Template.**  As board 195: four rungs, one per `defense_vs_preempt_$X`.

---

## Board 475 — -2 IMPs — table A, call 7, seat S: `2D` over partner's negative double

**Missing agreement.**  `opener_over_negative_double` has no rung for opener's
SECOND suit: with five-four he must repeat the five-card suit or bid notrump
without a stopper.

`AT.Q7.AQ942.K843` after `1D (1S) X P`: five diamonds, four clubs, 15 HCP, and
`AT` is not a spade stopper.  The context's six rules are: support the other
major, bid the other major, notrump, rebid the minor, jump-rebid the minor,
jump notrump.  There is no 2C.  `onx_rebid_DS` measures **-2.00 on 5 tables**.

```yaml
      # in opener_over_negative_double, immediately before onx_jump_$m$M
      - id: onx_second_$m$M
        call: "2$om"
        priority: 62.5
        when: { cheapest_in_suit: true }
        requires: { suits: { $om: [4, 13], $m: [0, 5] }, hcp: [12, 17] }
        shows: "opener's second suit over the negative double: 4+ $om, 5-4 shape, 12-17"
        establishes: { forcing: non_forcing }
```

`$om` is the DSL's automatic "other minor".  The priority assumes board 372's
+5 bump is applied; without it, use 57.5.

**Answering seat.**  Non-forcing.  Responder's next seat after
`1$m - 1$M - X - P - 2$om - P - ?` is `general_uncontested_continuation`, which
has the full ladder.

**Endangers.**  `onx_major1_$m$M` (66) / `onx_major_$m$M` (65) — above me, so
supporting the major the double promised still wins; `onx_jump_$m$M` (64) —
above me, so a 16-19 jump rebid wins; `onx_jumpnt` (63.5) and `onx_nt` (63) —
above me, so a balanced 12-14 or 18-19 WITH a stopper still bids notrump;
`onx_rebid_$m$M` (62) — directly below, the intended target, and the `$m: [0, 5]`
ceiling means a six-card first suit still repeats itself.
**Fallback:** 2C was previously produced only by `uc_new_C2` at priority 26 and
fit 0.264 — a soft-miss candidate, not a real one.

**VERIFIED** — bids 2C, `onx_second_DS` fit 1.000, score 0.872 (against
`onx_rebid_DS` 0.871).

**Reported negative on the SAME board.**  Call 11 (S's `3NT` over their 2S with
`AT` in spades) is downstream of the excluded `weakest_their_stopper`
sharp-tolerance item: `cl_nt3` fits **1.000** because no stopper at all scores
0.835 against a `[0.9, 9]` gate.  I built the five-card-rebid rung
(`cl_rebid5_D3`, board 928) and traced it here: it fits **1.000** but loses to
`cl_nt3` at priority 29 vs 28.5.  I am **not** proposing to lift it above 3NT —
that would demote every legitimate competitive 3NT to repair one un-gated
evaluator.

**Template.**  One rung in an `expand_pairs` context of four = four rules.

---

## Board 516 — -2 IMPs — table A, call 2, seat S: `2D` over their takeout double

**Missing agreement.**  You do not run to a suit you have no honour in — the
runout over their takeout double promises a suit, not just five cards.

`5.J73.T8632.KJ96`, 5 HCP.  `xd_run_D2` says "running to my own D: **5+
cards**" and nothing else, so `T8632` qualifies at fit 1.000 and outranks
`rdx_pass` (20).  W then bid 2H and we were never in the auction.

```yaml
      # one added clause on xd_run_D2 in general_their_double
      - id: xd_run_D2
        call: 2D
        priority: 25
        when: { we_bid_last: true, we_hold_contract: false, unbid_suit: D, cheapest_in_suit: true }
        requires:
          suits: { D: [5, 13] }
          evals: { "suit_quality(D)": [1, 9] }
        shows: "running to my own D: 5+ cards with at least one high honour"
```

**Answering seat.**  Unchanged.

**Endangers — THIS IS A GATE, and the denominator supports it.**  `xd_run_D2`
measures **-1.40 (5 tables) on r18 and -0.25 (8 tables) held out** — losing on
both.  It subtracts runouts to honourless five-card suits; those hands now pass
(`rdx_pass`, 20) and partner reopens, which is the standard treatment.  Above
it: `rdx_XX` (75), `jordan_2NT` (80), `jordan_raise`/`jordan_preempt` (60/62),
`rx_$M_2H`/`rx_$M_1NT` (62/58) — all untouched.  Below it: `rdx_pass` (20)
inherits, which is the point.
Note `suit_quality >= 1` is a *low* bar (one of A/K/Q, or two of J/T); `T8632`
scores 0.5 and fails, `KJ963` scores 1.5 and passes.

**VERIFIED** — bids P; `xd_run_D2` drops to fit 0.757, score 0.587 against
`rdx_pass` 0.760.

**Template.**  `expand: { X: [C, D, H, S] }` — all four `xd_run_$X2` rungs and
their `xd_run_$X1` / `xd_run_$X3` siblings, which have the same defect.

---

## Board 625 — -2 IMPs — table B, call 6, seat W: `3S` over `1H 1S X P 2H`

The board's first divergence is an opening decision (scope-excluded).  I am
ruling on table B.

**Missing agreement.**  Do not invite a partner who has already passed: the
overcaller's invitational jump rebid requires that partner has made a call.

`AJT543.AJ.Q5.A63`, 16 HCP.  Partner PASSED over the takeout double — he has
denied values — and `cl_rebid_jump_S` (31, "16-19") still jumps.  `cl_rebid_S2`
(29) describes the same hand one level lower and fits 1.000.

```yaml
      # one added condition on each of the four cl_rebid_jump_$X rungs
      - id: cl_rebid_jump_S
        call: 3S
        priority: 31
        when: { my_suit: S, partner_has_acted: true }
        requires:
          suits: { S: [6, 13] }
          evals: { total_points: [16, 19], "suit_quality(S)": [1.5, 9] }
        shows: "invitational jump rebid in competition: 6+ good S, 16-19, opposite a partner who has spoken"
```

**Answering seat.**  Unchanged; the jump stays `invitational` where it fires.

**Endangers — THIS IS A GATE AND IT ACCUSES A WINNER.**  `cl_rebid_jump_S`
measures **+0.60 (5 tables) / +2.00 (3 tables)** — profitable on both corpora,
on a tiny population.  The gate is bridge-correct and the denominator says be
careful: **measure alone.**  What it subtracts is replaced, not deleted:
`cl_rebid_S2`/`_S3` (29) describe the identical hand (6+ cards, 11+ points) one
level lower, so there is no hole — this is a level reduction, not a removal.
Below 29, nothing changes.

**VERIFIED** — bids 2S, `cl_rebid_S2` fit 1.000, score 0.787.

**Template.**  All four `cl_rebid_jump_$X` and their `ch_`, `ballow_`,
`balhigh_` mirrors — sixteen rules, one condition each.

---

## Board 660 — -2 IMPs — table A, call 6, seat S: `P` in the passout seat over 2S

**Missing agreement.**  The doubler's SECOND double at the two level shows
15-18 with the shape unchanged, not 19+ — with 4-4-3 in the unbid suits and a
doubleton in theirs, a hand too good to pass must double again.

`43.AQT6.KQ62.AT5`: 15 HCP, two spades, four hearts, four diamonds, three
clubs, after `(1S) X (2S) P P`.  `ballow_reopen_X2` demands **19+** and fits
0.028; `ballow_pass` takes the seat and fires **270/271 tables at -0.72 / -0.26**
across the corpus.

```yaml
      # in general_balancing_low, immediately before ballow_reopen_X
      - id: ballow_reopen_X2_shape
        call: X
        priority: 40.5
        when: { their_last_bid_suit: true, side_has_acted: true, we_bid_last: false,
                my_last_call_was_double: true, we_hold_contract: false, standing_bid_level: [2] }
        requires:
          hcp: [15, 18]
          evals: { max_their_suit_length: [0, 2], longest_suit_length: [0, 4], weakest_unbid_length: [3, 13] }
        shows: "a SECOND takeout double at the two level: 15-18, still short in their suit and still three-plus in every unbid suit"
        establishes: { forcing: one_round }
```

`weakest_unbid_length >= 3` is the clause that makes a repeat double safe: it
says the hand is still takeout-shaped, and it carries a sharp `_S2` of 0.95.

**Answering seat.**  `forcing: one_round`; `general_pull_or_sit` answers, and
the advance ladder for a doubled two-level contract exists at the two and three
level.

**Endangers.**  `ballow_reopen_X2` (41) — above me, so the 19+ reading stays
primary; `ballow_reopen_X` (41) — above me, and its `my_last_call_was_double:
false` makes it disjoint from mine anyway; `ballow_X` (40) — above me, and its
`side_has_acted: false` makes it disjoint; `ballow_nt2_strong` (30) — below me,
and with two small spades a 17-21 notrump has no stopper; `ballow_raise_*`
(27-32) — below me, and partner has shown nothing to raise; `ballow_new_*3`
(27) — below me, and with 4-4 you double rather than guess which four-card suit
to bid at the three level; `ballow_pass` (21).
**Fallback:** X already covered by `ballow_reopen_X2`, so nothing is deleted.
The `standing_bid_level: [2]` gate confines this to the level where the second
double is cheap.

**VERIFIED** — bids X, `ballow_reopen_X2_shape` fit 1.000, score 0.821.

**Template.**  One rung, suit-free.  The `balhigh_` twin (three-level second
double) should floor at 17-18, not 15, and I have not written it.

---

## Board 735 — -2 IMPs — NOTHING-WRONG

Uncontested at both tables; neither side had a competitive decision.
`KT8.9872.QT74.86` (5 HCP) passing partner's 1C is a constructive-lane
judgement about the boundary between `r1m_pass` ("0-5") and `r1m_1H` ("6+") —
and it is one instance of the ledger's own open item, "the five responding
contexts are a uniform hole the rule-level yardstick cannot see."  Nothing on
this board is mine.

---

## Board 739 — -2 IMPs — NOTHING-WRONG

The same board as 735 with different spots: `K75.9765.853.QT2` (5 HCP) passing
1D, uncontested at both tables.  Checked on the competitive side: our E passed
1D at table B holding `AJT9.J3.A9.97543` (10 HCP, four spades, five clubs) —
`oc1D_pass` is correct, since a 1D overcall context requires five diamonds and
neither the takeout double (three-plus in every unbid suit) nor a one-level
suit overcall (five cards) is available on 4-2-2-5.  Constructive lane.

---

## Board 848 — -2 IMPs — NOTHING-WRONG

Both auctions are uncontested Stayman sequences.  The divergence is
`stmi_2D_3NT` accepting the invitation with a 16-count 3-3-4-3 — a
constructive-lane range question about whether a flat 16 with three
queens/jacks is a maximum.  No seat on this board faced a competitive decision;
our N/S passed correctly throughout at table A (`v1NT_pass` over their 1NT with
`K95.JT85.J4.KQ92` is right — the direct-seat defence needs a suit).

---

## Board 899 — -2 IMPs — table A, call 3, seat S: `1D` over partner's 1C

**Missing agreement.**  With five-card support for partner's minor and a
singleton, raise at once — the Walsh diamond response is a free invitation for
the opponents to enter, and on this board W held six hearts and took it.

`A64.6.Q842.QJ983`: five clubs, singleton heart, 9 HCP.  `r1C_1D` (74) fits
1.000; `r1m_raise3` fits **0.800** (a one-point miss on its 10-12 HCP floor).
After our 1D, W overcalled 2H and E raised to 3H; at the other table BEN's
immediate 3C shut them out completely and scored +110.

```yaml
      # in the 1m response context, immediately before r1m_2NT
      - id: r1m_raise3_shape
        call: 3$m
        priority: 78
        when: { cheapest_in_suit: false }
        requires:
          suits: { $m: [5, 13], H: [0, 3], S: [0, 3] }
          evals: { total_points: [9, 13], singleton_or_void: [1, 1] }
        shows: "shape raise: five-card support for partner's minor with a singleton, 9-13 - the obstructive raise beats a Walsh diamond that invites them in"
        establishes: { forcing: invitational, agreed_suit: $m }
```

`singleton_or_void` carries a sharp `_S2` of 0.05, so the shortness clause is a
real gate and not a soft preference; `H: [0, 3]` / `S: [0, 3]` keeps a
four-card major going up the line.

**Answering seat.**  `forcing: invitational`, `agreed_suit: $m` — opener's seat
after `1$m - P - 3$m - P - ?` is the existing minor-raise continuation, and the
rung is a strict widening of `r1m_raise3`, which that seat already answers.

**Endangers.**  `r1m_1S` (77) — above me, so a four-card spade suit still goes
first; `r1m_2over1` (70) — below me, but requires 12+ HCP, disjoint from my
9-13 with a singleton; `r1C_1D` (74) — the intended target, and it measures
**-1.43 (7 tables) / -1.42 (12 tables)**, losing on BOTH corpora; `r1m_1NT`
(45), `r1m_raise3` (52) — below me and a strict subset.
**Fallback:** 3$m was already covered by `r1m_raise3` (`when`-less), so nothing
is deleted.

**VERIFIED** — bids 3C, `r1m_raise3_shape` fit 1.000, score 0.934.

**Template.**  `expand: { m: [C, D] }` inside the existing `r1m_*` context (two
rules).  This is the competitive-lane argument for a constructive rung: the
raise is chosen because it denies the opponents a cheap entry, not because it
describes the hand better.

---

## Board 920 — -2 IMPs — NOTHING-WRONG

The board turns on a third-seat opening decision (`KQ.KJ965.8.98764`, 9 HCP,
5-5, `open_1H_rule20_third` fit 0.640) — scope-excluded.  The competitive call
that followed, `2H` over their `1NT - 2C`, is exactly what `cl_new_H2` says
(five hearts, 11 total points) and it is a normal non-vulnerable obstruction;
BEN's 0.81 pass is a style difference.

**Reported negative.**  I prototyped a discipline pass — "they have shown 22+
between them and I have neither a six-card suit nor the values, so entering the
auction only helps them" — using the `their_shown_hcp` evaluator, which no rule
in the file currently uses.  **It does not work as I expected:**
`their_shown_hcp` returned **8.0** in this seat (after a 15-17 notrump and a
Stayman 2C), i.e. it is not a combined count of what the opponents have shown.
The gate would never fire.  Reporting it so nobody else spends the cycle: if a
"they have the values" agreement is wanted, `their_shown_hcp` needs to be read
before it is leaned on.

---

## Board 928 — -2 IMPs — table A, call 10, seat S: `P` over their 2S

**Missing agreement.**  The three-level rebid ladder in competition demands six
cards, so a self-sufficient five-card suit has no bid and we sell out.

`954.Q3.AKQT9.Q54`: 13 HCP, `AKQT9` of diamonds (suit quality 3.5), no spade
stopper.  `cl_rebid_D3` needs `D: [6, 13]` and fits 0.349; `cl_pass` takes the
seat and we defended 2S making eight.  3D goes one down for -50 against -110.

```yaml
      # in general_competitive_low, immediately before cl_rebid_D3
      - id: cl_rebid5_D3
        call: 3D
        priority: 28.5
        when: { my_suit: D, cheapest_in_suit: true }
        requires:
          suits: { D: [5, 13] }
          evals: { total_points: [13, 40], "suit_quality(D)": [2, 9] }
        shows: "rebid of my own five-card D at the three level: a self-sufficient suit and the values for the level"
        establishes: { forcing: non_forcing }
```

**Answering seat.**  Non-forcing.

**Endangers.**  `cl_reopen_X` (35), `cl_negative_*` (33+), `cl_raise_*3` (31),
`cl_rebid_jump_D` (31) — above me; `cl_nt3` (29) and `cl_rebid_D3` (29) — above
me, so a genuine six-card rebid and a genuine 3NT stay primary (and on board 475
`cl_nt3` beats this rung, which is the correct ordering while the stopper gate
is broken); `cl_nt2` (28), `cl_new_*` (25-27.5) — below me, and repeating a
solid five-card suit beats a new one; `cl_pass` (20).
**Fallback:** 3D already covered by `cl_rebid_D3` (identical `when`).
`cl_rebid_D3` itself **never fires** in either corpus, so this is empty space.

**VERIFIED** — bids 3D, `cl_rebid5_D3` fit 1.000, score 0.785.

**Template.**  Same family as board 262: `expand: { X: [C, D, H, S] }` at the
two and three level across the four generic competitive/balancing contexts.
The quality floor should be 2.5 at the two level and 2.0 at the three level is
wrong-way-round on its face — I set 2.5 for 2S (board 262) and 2.0 for 3D here
because `AKQT9` at the three level is a better suit than `KQJ84` at the two;
the consolidator should pick one number per level and apply it, and my
recommendation is **2.5 at both**, which still fires on board 928 (3.5) and not
on 475 (2.0), which is the correct discrimination.

---

## Board 933 — -2 IMPs — table A, call 3, seat N: `P` after `1D 3H X`

**Missing agreement.**  `general_their_double` has no four-level raise of any
kind, so when partner preempts and they double, ten combined trumps have
nowhere to go.

`KJ42.KT5.T654.Q7`: three-card support for a 3H preempt,
`lott_total_trumps(H) = 10`.  The context's raise ladder is
`xd_raise_$X2` / `xd_raise_$X3` / `xd_jumpraise_$X3` (the last gated
`standing_bid_level: [1]`) and stops there; the only 4H candidate is the code
fallback at priority **12**, fit 0.409.  `xd_pass` fires **88/91 tables at
-1.72 / -0.43**.

```yaml
      # in general_their_double, immediately before xd_raise_S2
      - id: xd_raise_lott_H4
        call: 4H
        priority: 33
        when: { we_bid_last: true, we_hold_contract: false, partner_suit: H }
        requires:
          suits: { H: [3, 13] }
          any_of:
            - evals: { "lott_total_trumps(H)": [10, 26], total_points: [6, 40] }
            - evals: { "lott_total_trumps(H)": [8, 26], total_points: [12, 40] }
        shows: "the Law after they double: ten combined trumps make four of the major our level whether it makes or it is a save"
        establishes: { forcing: non_forcing, agreed_suit: H }
```

The second `any_of` branch is deliberate: it reproduces the code fallback's own
description ("raise: 3+ H, about 12+ support points") so the rung is a strict
**superset** of the fallback it deletes.  Without that branch, an eight-trump
hand with 12 support points would lose its 4H fallback — the round-15 trap.

**Answering seat.**  Non-forcing; partner is the preemptor and
`preemptor_discipline` plus `general_competitive_high` cover his seat.

**Endangers.**  `xd_rebid_$X2/3` (34) — above me, so partner rebidding his own
doubled suit still wins; `xd_jumpraise_$X3` (32) — below me, but gated to
`standing_bid_level: [1]`, disjoint; `xd_raise_$X3` (31), `xd_raise_$X2` (30) —
below me and produce different calls that are usually illegal at this level;
`xd_second_*` (24-26), `xd_run_*` (24-25), `xd_pass` (18).
**Fallback deleted:** the priority-12 4H raise, replaced by a superset.

**VERIFIED** — bids 4H, `xd_raise_lott_H4` fit 1.000, score 0.799.

**Template — and a separate one-line finding on this board.**
`expand: { M: [H, S] }` and a minor twin: four rungs.

**`neg_double_3level_m` is missing a pair.**  Table B, call 2: W holds
`AT75.A.K93.JT843` after `1D (3H)` — 12 HCP, singleton heart, four spades — and
passes, because the context that owns `1$m - $j` lists
`{C,2H} {C,2S} {D,2H} {D,2S} {C,3H} {C,3S} {D,3S}` and **omits `{D,3H}`**.  The
seat therefore falls through to `general_competitive_high`, where
`ch_negative_X3` is denied by a five-card minor (`longest_suit_length: [0, 4]`,
fit 0.349) and there is no takeout double at all.

```yaml
    expand_pairs:
      - { m: C, j: 2H }
      - { m: C, j: 2S }
      - { m: D, j: 2H }
      - { m: D, j: 2S }
      - { m: C, j: 3H }
      - { m: C, j: 3S }
      - { m: D, j: 3H }        # <- added
      - { m: D, j: 3S }
```

**VERIFIED** — with the pair added, W bids X (`nxj_X`, fit 1.000, score 0.910)
and partner answers 3S.
**Endangers:** the new context `neg_double_3level_m[D,3H]` has specificity 1003
and therefore takes over interpreting **X** and **P** for `1D - 3H - ?` from
`general_competitive_high`.  Its `nxj_pass` requires `hcp: [0, 7]` where
`ch_pass` was a `requires: {}` catch-all, so an 8-count with no double becomes a
soft-miss.  The seven existing pairs already carry that hazard, so this is
consistency rather than a new risk — but it is the reason I list this as a
templating fix rather than as the board's primary proposal.  DECISIONS also
records that `nxj_X` promises 8+ HCP and nothing else at priority 70, and that a
shape gate on it measured -5 held out; extending its reach inherits that.

---

## Board 934 — -2 IMPs — table B, call 3, seat E: `P` in the passout seat over 3D

**Missing agreement.**  `balhigh_X` requires 14+ where its own low-level twin
`ballow_X` requires 11 (and 9 with a singleton) — and `balhigh_X`'s `shows`
sentence quotes the *ballow* gates, so the rule promises less than it demands.

`JT82.AQ8.T3.AQ76`: 13 HCP, `T3` doubleton in their diamond suit, 4-3-4 in the
unbid suits, opposite a partner who has passed a preempt.  `balhigh_X` fits
**0.800** on a one-point miss and `balhigh_pass` takes the seat —
**767/768 tables at -0.67 / -0.65**, the largest losing population in this
dossier slice.

```yaml
      # in general_balancing_high, immediately before balhigh_raise_C2
      - id: balhigh_X_shape
        call: X
        priority: 39
        when: { their_last_bid_suit: true, side_has_acted: false }
        requires:
          evals: { longest_suit_length: [0, 5] }
          any_of:
            - hcp: [12, 40]
              evals: { standing_suit_length: [0, 2] }
            - hcp: [10, 40]
              evals: { standing_suit_length: [0, 1] }
        shows: "balancing double of their preempt: 12+ with at most a doubleton in their suit (10+ with a singleton), no long suit of my own to bid"
        establishes: { forcing: one_round }
```

Two points higher than `ballow_X` at every branch, because balancing over a
three-level preempt commits partner to the three level; `longest_suit_length <=
5` is the clause `ballow_X` lacks and `balhigh_reopen_X` has.

**Answering seat.**  `forcing: one_round`.  **Traced:** partner
(`KQ974.54.J8.KJT2`) answers `3S` via `adx_pull_S3` at fit 1.000 in
`general_pull_or_sit`.  Not a starved ask.

**Endangers.**  `balhigh_reopen_X2` / `balhigh_reopen_X` (41) — above me, and
both require `side_has_acted: true`, disjoint from mine; `balhigh_X` (40) —
directly above, so the 14+ reading stays primary and I take only 10-13;
`balhigh_raise_*` (27-32) — below me, and their `partner_suit` conditions
cannot hold when partner has passed throughout; `balhigh_nt3` (29),
`balhigh_new_*3` (27) — below me, and with 4-3-4 and no six-card suit the
double is the only call that finds all three suits; `balhigh_pass` (21).
**Fallback:** X already covered by `balhigh_X`.

**VERIFIED** — bids X, `balhigh_X_shape` fit 1.000, score 0.817.

**Template.**  One rung, suit-free.  Ship with boards 195/417 (`v3_$X_X_shape`)
and 282 (`vw2_X_three`) as one family: *the takeout double of a preempt is
priced in shape.*

---

## Appendix — the six subtractive proposals, ranked by how much they should be trusted

| # | board | change | whole-corpus score of the rule it takes from | verdict |
|---|---|---|---|---|
| 1 | 516 | `xd_run_D2` needs one honour | **-1.40 / -0.25** (5/8 tables) | ship; loses on both corpora |
| 2 | 372 | `onx_*` +5, so `adx_sit` cannot convert a negative double | `adx_sit` **+0.15 / +0.11** (27/28), `onx_rebid_DS` **-2.00** (5) | ship; the subtraction is confined to four patterns |
| 3 | 411 | two-level overcall floor 11 -> 12 on a five-card suit | `oc1H_2D` **-1.22 / +0.62** (9/8) | ship, but it does not replicate; system doctrine says 12 |
| 4 | 252 | six-card major outranks the minor raise | `cl_raise_C3` **-0.78 / +3.50** (9/6) | **measure alone** — this is a re-rank |
| 5 | 937 | negative double denies a four-card fit | `cl_negative_X1` **+0.25 / +1.90** (12/10) | **measure alone — accuses a winner** |
| 6 | 625 | no invitational jump opposite a passed partner | `cl_rebid_jump_S` **+0.60 / +2.00** (5/3) | **measure alone — accuses a winner**; but the hand keeps a bid one level lower |

## Appendix — what I did NOT propose, and why

* **Freeing `cl_raise_lott3_$M`** (do-not-re-propose).  Board 937 wanted it and
  I routed around it: the fix there is a denial on the negative double, so the
  existing `cl_raise_D2` inherits the seat.
* **The `weakest_their_stopper` sharp-tolerance repair** (do-not-re-propose).
  It is the reason board 475's `cl_nt3` fits 1.000 with `AT` in their suit, and
  the reason `cl_nt1`/`cl_nt2`/`cl_nt3`/`adx_nt`/`onx_nt` all promise stoppers
  they do not test.  I priced `cl_rebid5_D3` *below* `cl_nt3` rather than repair
  it by re-ranking.
* **Michaels / unusual notrump** (do-not-re-propose).  Board 252's table A wants
  2NT over 1C on 5-5 in the reds; I proposed the six-card-major re-rank on the
  other table instead.
* **A Stayman/transfer twin over their interference** (measured -12 in round 9).
  Board 360 wants one; I proposed the both-majors negative double instead, which
  finds the same 4-4 spade fit through a ladder that already exists.
* **Opening-style and rule-of-20 thresholds** (do-not-re-propose).  Boards 262,
  282, 625, 920 all have one as their first divergence; in each case I ruled on
  a competitive call further down the auction, or returned NOTHING-WRONG.
* **A more specific context for `1NT - P - 2$T - bid - ?`** (board 347).  It
  would shadow `general_competitive_low` and would have to carry every one of
  its gates verbatim.  I used a rung instead.
