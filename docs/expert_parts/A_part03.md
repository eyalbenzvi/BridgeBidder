<!--SUMMARY-->

## Board 906 — E, call 7 (table B): `3H` should be `4H`

**Seat/call that went wrong.** Table B, E, `P P P 1H 1S P 2H — ?` with
`A5.AJT6543.AK.65` (16 HCP, seven hearts, **five losers**).  `cl_rebid_jump_H`
bid an invitational 3H; the auction died in 3S undoubled (+150) while the other
table collected 620 for 4H.

**The missing agreement.** When RHO cue-bids my suit (a limit raise or better,
so the auction is guaranteed to reach three of their major), a seven-card suit
with five losers is a game bid, not an invitation — there is no second chance.

**Why the rung does not exist.** `cl_rebid_H4` (line 11055) carries
`when: { my_suit: H, cheapest_in_suit: true }`.  Over their 2H the cheapest
heart call is 3H, so the four-level rebid of my own suit is structurally
unreachable in every competitive auction — the same defect the ledger records
for `cl_raise_lott3_$M`.  There is no 4H code fallback here either (the
fallback layer offered only `X`), so this rung suppresses nothing.

```yaml
  # context: general_competitive_low   (insert before `- id: cl_rebid_C2`)
      - id: cl_rebid_game_H
        call: 4H
        priority: 31.5
        when: { my_suit: H }
        requires:
          suits: { H: [7, 13] }
          evals: { total_points: [15, 40], ltc: [0, 5], "suit_quality(H)": [1.5, 9] }
        shows: "self-sufficient seven-card H and at most five losers: bid the game myself"
        establishes: { forcing: sign_off, agreed_suit: H }
```

**THE ANSWERING SEAT.** None required: `forcing: sign_off` closes the
conversation, which is the whole point of the rung — it replaces a question
(an invitation nobody could answer over their spade fit) with a contract.

**WHAT IT ENDANGERS** (every rule in `general_competitive_low` this can outrank):

* `cl_rebid_jump_H` 3H @31 — an invitation is the wrong tool when partner has
  already shown a bust by overcalling into my opening and RHO has shown a fit.
* `cl_rebid_H3` 3H @29 — same hand, one level too low.
* `cl_nt3` 3NT @29 / `cl_nt2` 2NT @28 — a 7-2-2-2 with a five-loser suit is not
  a notrump hand (both score 0.000 here anyway).
* `cl_new_*3(_hi)` @27–27.5, `cl_new_*2` @26–26.5, `cl_new_*1` @25 — introducing
  a four-card side suit at the three level with a seven-card major is inferior.
* `cl_pass` @20 — passing sells out to their fit with a five-loser hand.
* Rungs it must NOT outrank, and does not: `cl_raise_H4`/`cl_raise_lott4_H` @32
  (supporting partner's suit outranks repeating mine), `cl_negative_X` @33,
  `cl_takeout_X` @36, `cl_doubler_*` @33–35.

**VERIFIED.**  Patched copy of the system, `prepare_decision` + `score_candidates`:
`4H cl_rebid_game_H fit=1.000 prio=31.5` now beats `3H cl_rebid_jump_H fit=1.000
prio=31.0`; chosen call changes 3H → 4H.

**TEMPLATE.**  Not a templated context, so ship the sibling set by hand:
`cl_rebid_game_H` (4H) and `cl_rebid_game_S` (4S) in `general_competitive_low`,
and the identical pair `ch_rebid_game_H` / `ch_rebid_game_S` in
`general_competitive_high` (whose `ch_rebid_H4` @29 carries the same
`cheapest_in_suit: true`), plus `balhigh_`/`ballow_` twins.  **Majors only** —
five of a minor on a seven-card suit is a different (and much worse) bet, so do
not extend the idea to 5C/5D.

---

## Board 945 — NOTHING-WRONG (competitive); the board is lost in a constructive auction

**What I checked.**  Table B is uncontested from beginning to end
(`1D P 1S P 2C P 2H P 3S P 4NT P 5C P 5S`); the first divergence is W's
fourth-suit `fsf_2H` and the loss is the RKC sequence that ends in 5S one off
with 4S cold.  That is the constructive reviewer's board.

The only competitive decision on either table is N in the **sandwich seat** at
table A: `1D - P - 1S - ?` with `43.A97642.8.Q986` (6 HCP, six hearts).
`sw_pass` is correct here — A-9-7-6-4-2 fails every suit-quality floor in the
file and N/S have no fit and no save (DD: N makes four heart tricks; 2H would be
-200 against their 420, and they would not have let us play it).

**Secondary observation, offered but NOT proposed as this board's fix.**  The
sandwich ladder has a real sibling gap next door: `sw_2C_jump`/`sw_2D_jump`/
`sw_2H_jump`/`sw_2S_jump` (priority 69, 6+ cards, 5-10) all carry
`cheapest_in_suit: false`, so after `1D - P - 1S` there is no weak two-level
action in hearts at all — 2H is the cheap call and the only rung that reaches it
demands 11-17 (`sw_2H`).  The direct seat has `cl_new_long2_H` ("a SIX-card
suit, 8+ points") and the sandwich seat has no equivalent.  That is the
additive sibling gap; it does not rescue *this* hand and I am not claiming it
does.

**VERIFIED** (that `sw_pass` is the honest call and that `sw_2H_jump` is
unreachable in this auction: `cheapest_in_suit: false` fails when 2H is cheapest).

**TEMPLATE.**  If the sibling gap is taken up later: `sw_2$X_long` across
`expand: { X: [C, D, H, S] }` inside the already-templated `sandwich_seat`
context, `when: { unbid_suit: $X, cheapest_in_suit: true }`.

---

## Board 44 — N, call 4 (table A): `1H` should be `P` (converting the double)

**Seat/call that went wrong.**  Table A, N, `P 1D X P — ?` with
`82.QT6.KT865.985` (5 HCP, **five diamonds to the K-T behind the opener**).
`advD_1H` bid a three-card heart suit; 1D doubled is two off (+500 at the other
table, where BEN's N passed).

**The missing agreement.** Advancer passes partner's one-level takeout double
for penalties on trump LENGTH and a trump honour, not on high-card strength —
five of their suit and no four-card major to offer is the whole requirement.

**Why the existing rungs cannot do it.**  `adv_pass_penalty` (priority 30)
demands `hcp: [9, 40]` and `two_of_top3($o)`; K-T-8-6-5 has one of the top three
and five points, fit 0.006.  And because the takeout double `establishes:
{ forcing: one_round }`, `_pass_forbidden` removes PASS from the candidate set
entirely — it is only re-admitted by an **authored, discriminating pass rule
fitting ≥ 0.9** (`decision.py`, `_is_discriminating`).  So the pass is not merely
outranked here: it is not on the ballot.

```yaml
  # context: advance_takeout_double   (expand: { o: [C, D, H, S] })
  # insert as the last rung of that context, before `- id: advance_takeout_double_suits_C`
      - id: adv_pass_stack
        call: P
        priority: 55.5
        when: { standing_bid_level: [1, 1] }
        requires:
          suits: { $o: [5, 13], H: [0, 3], S: [0, 3] }
          hcp: [4, 11]
          features: [ "top_honour($o)" ]
        shows: "penalty pass of the one-level takeout double: five of their suit headed by an honour and no four-card major to offer"
        establishes: { forcing: non_forcing }
        negative_inference_weight: soft
```

**THE ANSWERING SEAT.**  The pass is a sign-off in effect and the doubler's seat
is already authored: after `1$o - X - P - P` the doubler is in
`general_uncontested_continuation` / `general_pull_or_sit` with `adx_*` rungs, and
the standing contract is theirs, doubled.  No new answering context is needed —
which is precisely why this is the cheap end of the file to add to.

**WHAT IT ENDANGERS** (every rung it can outrank in the two live contexts):

* `advD_1H` @53 / `advD_1S` @54 / `advC_1D` @52 / `advH_*`, `advS_*` — the forced
  suit response at the one level; with three small in both majors and five of
  their trumps, +500 beats naming a three-card suit.
* `adv_1NT` @55 — 6-10 with a stopper: a five-card holding in their suit IS the
  stopper, and defending 1DX is worth more than declaring 1NT.
* `adv_pass_penalty` @30 — same call, strictly wider; keep both, this one is the
  weak-hand branch.
* Rungs it does NOT outrank, correctly: `adv_2NT` @56 (11-12 balanced invite),
  `advD_2H_jump`/`advD_2S_jump` @60 (9-11 with a real four-card major),
  `adv_cue` @75 (game-forcing values).
* Fallbacks: none deleted — PASS is already covered by `adv_pass_penalty` in this
  context, so `generate_fallbacks` was never producing it.

**VERIFIED.**  Base: `1H advD_1H fit=1.000`.  Patched: `P adv_pass_stack
fit=1.000 prio=55.5` chosen.  Regressions run and unchanged: a 4-3-3-3 eight
count still bids 1H; `82.QT62.KT865.98` (five diamonds **and** a four-card
heart suit) still bids 1H, because the `H: [0, 3]` gate is sharp.

**TEMPLATE.**  Already templated: the context expands `o: [C, D, H, S]`, so one
rule becomes four.  Do **not** extend it to `advance_reopening_double` or the
two-level doubles without re-measuring — the trump-length bar rises with the level.

---

## Board 79 — S, call 7 (table A): `3C` should be `P`

**Seat/call that went wrong.**  Table A, S, `1H P 1NT X 2D P 2H — ?` with
`AK96.J.AT5.QT762` (14 HCP, 4-1-3-5).  Having doubled 1NT for values, S bid 3C
over their second run-out; 3C was two off vulnerable, -200, where defending
their 2H is worth +100/+200 (DD: E/W take six tricks in hearts).

**The missing agreement.** Once I have doubled for values I have shown my hand;
with no six-card suit I defend at the three level rather than introduce a
five-card suit nobody asked for.

```yaml
  # context: general_competitive_low   (insert before `- id: cl_rebid_jump_C`)
      - id: cl_pass_after_my_double
        call: P
        priority: 27.6
        when: { my_last_call_was_double: true, standing_bid_level: [2, 7] }
        requires:
          hcp: [11, 16]
          evals: { longest_suit_length: [0, 5] }
        shows: "I have already doubled for values: with no six-card suit I defend rather than bid a new suit at the three level"
        establishes: { forcing: non_forcing }
```

**THE ANSWERING SEAT.**  None — it is a pass, and partner's next seat
(`general_balancing_*` / `general_competitive_*`) is already authored.  The
`when` deliberately excludes the one level (`standing_bid_level: [2, 7]`) so it
can never silence a cheap one-level suit bid after a takeout double.

**WHAT IT ENDANGERS**, and why the pass is the better description in each case:

* `cl_new_C3`/`cl_new_C3_hi` @27/27.5 and every `cl_new_*3(_hi)`, `cl_new_*2(_hi)`
  @26–27.5 — a five-card suit at the three level, vulnerable, opposite a partner
  who has already heard my double, is a guess; I have described the hand.
* `cl_new_*1` @25 — cannot be reached: the `standing_bid_level: [2, 7]` gate.
* `cl_pass` @20 — same call, so nothing is lost; this rung simply raises the
  pass above the natural-suit rungs when the double already spoke.
* Rungs it does NOT outrank, correctly: `cl_nt2` @28 / `cl_nt3` @29 (a real
  notrump hand still bids notrump), `cl_rebid_*3` @29 (a **six**-card suit still
  gets rebid — enforced by the sharp `longest_suit_length: [0, 5]`),
  `cl_raise_*2/3/4` @30–32 (supporting partner always beats defending),
  `cl_negative_X` @33, `cl_takeout_X` @36, `cl_doubler_raise*` @33–35.
* The `hcp: [11, 16]` ceiling keeps a 17+ doubler free to bid again, which is the
  one hand type that is *supposed* to act twice.

**VERIFIED.**  Base chooses `3C cl_new_C3_hi`; patched chooses
`P cl_pass_after_my_double fit=1.000 prio=27.6`.  Regressions: with
`AK9.J.AT5.QT7642` (six clubs) the engine still bids 3C — the pass rule drops out
of the candidate list on the sharp longest-suit gate; and a takeout doubler whose
partner has bid spades still raises (`2S cl_doubler_raise_S` @34 wins).

**TEMPLATE.**  Ship the same rung in `general_competitive_high`
(`ch_pass_after_my_double`, priority 27.6, same gates) and in
`general_balancing_low` / `general_balancing_high`
(`ballow_`/`balhigh_pass_after_my_double`).  No suit expansion — the rule is
about a call I made, not about a suit.

---

## Board 113 — S, call 1 (table A): `P` should be `2D`

**Seat/call that went wrong.**  Table A, S, `1S — ?` with `T2.A.KT972.QT964`
(9 HCP, **5-5 in the minors, a stiff ace and a doubleton**).  `oc1S_pass`.  We
never entered the auction and they made 4S for -420; at the other table the same
cards pushed N/S to 4D.

**The missing agreement.** A two-level overcall may be made on 8-10 high-card
points when the hand is 5-5 — with two five-card suits the shape is the values,
and the trick-taking hand belongs in the auction on the first round or never.

(Michaels / unusual notrump are scope-excluded and I am not re-proposing them:
this is a natural overcall of the better minor, which the file already speaks.)

```yaml
  # context: overcalls_of_1S   (insert before `- id: oc1S_2H`)
      - id: oc1S_2D_shape
        call: 2D
        priority: 64.5
        requires:
          suits: { D: [5, 13], S: [0, 2] }
          hcp: [8, 10]
          any_of:
            - suits: { C: [5, 13] }
            - suits: { H: [5, 13] }
        shows: "shapely two-level overcall: five diamonds and a second five-card suit, 8-10"
        establishes: { forcing: non_forcing }
```

**THE ANSWERING SEAT.**  Not a force — `non_forcing`, a natural overcall.  The
advance is already authored (`advance_overcall`, `cl_raise_D2/D3/D4`,
`cl_new_*`), which is exactly why the natural overcall is the right vehicle for
this hand and a new two-suited convention is not.

**WHAT IT ENDANGERS:**

* `oc1S_pass` @25 — the hand it describes is precisely a hand that has something
  to say; a 5-5 nine-count that passes never gets another cheap turn.
* `oc1S_3D_jump` @59 / `oc1S_3D_preempt` @58 — both demand a **six**-card suit;
  neither fits a 5-5 and neither is legal bridge on it.
* `oc1S_2D` @65 — deliberately left ABOVE this rung: the sound 11-17 overcall
  stays the primary reading of 2D, and the two bands are disjoint so they never
  both fit.
* `oc1S_X` @72 and `oc1S_1NT` @82 — untouched and still higher; a takeout double
  or a 15-18 notrump is a better description whenever it fits.
* Fallback: 2D was already covered by `oc1S_2D`, so no fallback is deleted.

**VERIFIED.**  Base: `P oc1S_pass fit=1.000` (2D fits only 0.409).  Patched:
`2D oc1S_2D_shape fit=1.000 prio=64.5` chosen.  Regression: `T2.A76.KT972.Q64`
(five diamonds, no second five-card suit, same 9 HCP) still passes.

**TEMPLATE.**  Six rules, one per two-level overcall that exists: `oc1S_2C_shape`,
`oc1S_2D_shape`, `oc1S_2H_shape`; `oc1H_2C_shape`, `oc1H_2D_shape`;
`oc1D_2C_shape`.  (Over 1C every overcall is at the one level, where the 8-16
band already admits these hands.)  The four `overcalls_of_1x` contexts are not
templated, so these are written out; each keeps `suits: { <their suit>: [0, 2] }`.

---

## Board 144 — S, call 2 (table A): `P` should be `4H`

**Seat/call that went wrong.**  Table A, S, `1H X — ?` with `6542.98762.3.982`
(**0 HCP, five-card heart support, a singleton**).  `rdx_pass`.  N/S hold ten
hearts and 4H makes ten tricks; we crawled to 3H two rounds later for +170 while
the other table collected 590.

**The missing agreement.** Over their takeout double of partner's major, five
trumps and a bust is a jump to the Law level — four of the major immediately,
before they find their fit.

```yaml
  # context: resp_1M_over_X_jordan   (expand: { M: [H, S] }); insert after `jordan_preempt`
      - id: jordan_lott_game
        call: 4$M
        priority: 63
        requires:
          suits: { $M: [5, 13] }
          hcp: [0, 7]
          evals: { lott_total_trumps: [10, 13] }
        shows: "ten trumps and no defence: the Law level at once over their takeout double"
        establishes: { forcing: sign_off, agreed_suit: $M }
```

**THE ANSWERING SEAT.**  `forcing: sign_off` + `agreed_suit: $M`: opener's seat
after `1$M - X - 4$M - act` is `general_competitive_high` / `general_pull_or_sit`,
both authored, and `partner_signed_off` correctly silences further invention.
This is a contract, not a question — no new answering context.

**WHAT IT ENDANGERS:**

* `jordan_preempt` 3$M @62 — the Law says bid to the level of the fit; with ten
  trumps that level is four, and three gives them a free look at the four level.
* `jordan_raise` 2$M @60 — three-card-support band; a five-card raise is not it.
* `rdx_pass` @20 (sibling context `resp_1x_over_X`) — passing with five trumps
  and a singleton hands them the auction.
* Rungs it does NOT outrank, correctly: `jordan_2NT` @80 and `rdx_XX` @75 — a
  limit raise or better still wants to invite or punish, and the `hcp: [0, 7]`
  ceiling means those hands never reach this rung.
* Fallback: `4$M` was not a covered call in this context before, so this rung
  does delete the code fallback for four of the major after `1$M - X`.  That
  fallback is generated only for hands with no fitting rule, and the sharp
  `lott_total_trumps` gate (tolerance 0.4) means anything short of ten combined
  trumps scores ≈0.03, so the suppression cannot reach a hand this rung wants.

**VERIFIED.**  Base: `P rdx_pass fit=1.000` (3H `jordan_preempt` only 0.134).
Patched: `4H jordan_lott_game fit=1.000 prio=63` chosen.  Regressions:
`6542.9876.32.982` (only **four** trumps) still passes — 4H falls to fit 0.029 on
the sharp LOTT gate; `K542.987.QT2.982` (three trumps, 6 HCP) still bids 2H.

**TEMPLATE.**  Already templated: `expand: { M: [H, S] }` gives both majors from
one rule.  The natural extension — the same rung after their **overcall**
(`resp_1M_over_2x`) — should be a separate proposal and measured separately.

---
