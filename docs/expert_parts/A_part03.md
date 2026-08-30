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
## Board 216 — S, call 2 (table A): `1NT` should be `2D`

**Seat/call that went wrong.**  Table A, S, `1C 1S — ?` with `JT54.Q72.KQT853.`
(8 HCP, **six diamonds K-Q-T-8-5-3 and a void in partner's clubs**).
`nx_1m1S_1NT` bid "6-10 with a spade stopper"; we then bid diamonds anyway two
rounds later and played 3C in a 4-1 fit for -100.

**The missing agreement.** Over their overcall a six-card suit of my own is a free
bid at the two level on 8+ points — the notrump response is for hands whose
longest suit is nothing to talk about.

**Why the rung does not exist.**  `resp_1m_over_1S` has a natural rung for the
unbid MAJOR (`nx_1m1S_2H`, 10+ forcing) and none at all for the other minor, so
2D has to fall back to the generic `cl_new_D2*` at priority 26–26.5 — sixteen
points of priority below a 1NT that lies about the shape.  This is the same
sibling gap `DECISIONS.md` already records for `resp_1m_over_1H` ("no weak jump
shift at all").

```yaml
  # context: resp_1m_over_1S   (expand: { m: [C, D] }); insert before `- id: nx_1m1S_pass`
      - id: nx_1m1S_long_$om
        call: 2$om
        priority: 50.5
        requires:
          suits: { $om: [6, 13] }
          evals: { total_points: [8, 40], "suit_quality($om)": [1.5, 9] }
        shows: "free bid of my own six-card $om over their overcall: a real suit, 8+ points"
        establishes: { forcing: non_forcing }
```

**THE ANSWERING SEAT.**  `non_forcing`, so none is owed — opener's next seat is
`general_competitive_low` / `general_uncontested_continuation`, both authored,
and `agreed_suit` is deliberately NOT established (a six-card minor opposite an
unknown hand is not yet trumps).

**WHAT IT ENDANGERS:**

* `nx_1m1S_1NT` @50 — 1NT with a void in partner's suit and six of my own tells
  partner a story about the wrong hand; my suit is the more useful fact.
* `nx_1m1S_pass` @20 — an eight-count with a six-card suit is not "nothing to say".
* `cl_new_D2`, `cl_new_D2_hi`, `cl_new_long2_D`, `cl_new_long2_D_hi` @26–26.5 —
  same call, same suit, better gate; and because they are in the LESS specific
  `general_competitive_low` they drop out of the candidate list once this rung
  covers 2$om in this context.  **That is the subtraction to watch**: the generic
  rungs describe a 5-card / 10+ hand and my rung a 6-card / 8+ hand, so the
  five-card 10-count that used to reach 2D via `cl_new_D2` now bids 1NT instead.
  Bridge verdict: with five and a stopper 1NT is the standard answer, so the
  subtraction is in the right direction — but it IS a subtraction and should be
  measured, not assumed.
* Rungs it does NOT outrank, correctly: `nx_1m1S_2NT` @51, `nx_1m1S_3NT` @52,
  `nx_1m1S_raise` @55, `nx_1m1S_cue` @70, `nx_1m1S_X` @80.

**VERIFIED.**  Base: `1NT nx_1m1S_1NT fit=1.000`.  Patched: `2D nx_1m1S_long_D
fit=1.000 prio=50.5` chosen.  Regressions: with only five diamonds
(`JT54.Q72.KQ853.7`) the engine still bids 1NT (2D drops to fit 0.349 on the
sharp suit-length gate); with a ragged five-card suit and no stopper it still
passes.

**TEMPLATE.**  `$om` (the other minor) inside the already-templated context, so
one rule becomes two (`nx_1m1S_long_D` over 1C, `nx_1m1S_long_C` over 1D).  The
same rung belongs in `resp_1m_over_1H` (`nx_1m1H_long_$om`, call `2$om`) — that
context has the identical hole.

---

## Board 312 — W, call 3 (table B): `X` should be `P` (the trap pass)

**Seat/call that went wrong.**  Table B, W, `P 1H 1S — ?` with `KJ532..QJ75.A743`
(11 HCP, **five spades sitting over the overcaller, a VOID in partner's hearts**).
`r1H1S_X` made a negative double showing "both minors or a long minor, no heart
fit"; partner pulled to 2H and we played a 5-0 fit for -300, vulnerable.

**The missing agreement.** With four or more good cards in their overcalled suit,
sitting over the overcaller, and no fit for partner, I pass and let partner
reopen — the negative double is for hands that want partner to CHOOSE, and I do
not want him to choose hearts.

```yaml
  # context: resp_1H_over_1S   (insert before `- id: r1H1S_pass`)
      - id: r1H1S_trap_pass
        call: P
        priority: 79
        requires:
          suits: { S: [4, 13], H: [0, 1] }
          hcp: [9, 14]
          evals: { "suit_quality(S)": [1.5, 9] }
        shows: "trap pass: four or more good spades over the overcaller and no heart fit - partner reopens"
        establishes: { forcing: non_forcing }
        negative_inference_weight: soft
```

**THE ANSWERING SEAT — checked, and it exists.**  After `1H - 1S - P - P` opener
is in `general_balancing_low`.  Traced with E's actual hand `A87.AK862.T84.JT`:
the engine bids **1NT (`ballow_nt1`, 10-14 balanced with a spade stopper)**,
which double-dummy takes eight tricks for +120 — against the -300 we actually
scored.  `ballow_reopen_X` @41 is there for the 16+ hands and `ballow_rebid_H2`
@29 for the six-card ones, so the seat is authored in all three shapes.  No new
context is owed.

**WHAT IT ENDANGERS:**

* `r1H1S_X` @78 — the negative double invites partner to bid hearts, and I hold
  none; this is the one hand type the double must not be made on.
* `r1H1S_cue` @75 / `r1H1S_raise` @70 / `r1H1S_preempt` @62 — all require heart
  support (`suits: { H: [3, 13] }` / `[4, 13]`), so they can never co-fit with the
  `H: [0, 1]` gate.
* `r1H1S_2m_C` @60 / `r1H1S_2m_D` @59 — a forcing 10+ new suit at the two level
  commits us to the three level in a misfit; defending 1S is worth more.
* `r1H1S_2NT` @51 / `r1H1S_1NT` @50 — a spade "stopper" of KJ532 is a trump
  stack, not a notrump asset.
* `r1H1S_pass` @20 — same call, weak branch; both stay.
* Fallback: PASS is already covered by `r1H1S_pass`, so nothing is deleted.

**VERIFIED.**  Base: `X r1H1S_X fit=1.000 prio=78`.  Patched: `P r1H1S_trap_pass
fit=1.000 prio=79` chosen.  Regressions: `K532.4.QJ75.A743` (four RAGGED spades,
a singleton heart) still doubles — the trap pass falls to fit 0.757 on
`suit_quality`; `862.K5.QJ75.A743` (no spade holding) still doubles.

**TEMPLATE.**  Ship the mirror in `resp_1m_over_1H` and `resp_1m_over_1S`
(`nx_1m1H_trap_pass`, `nx_1m1S_trap_pass`, with the void/singleton gate on the
opened MINOR relaxed to `[0, 2]` because a minor fit matters less), and in
`resp_1M_over_2x`.  Keep the `hcp: [9, 14]` ceiling everywhere — a 15+ hand
should act, not trap.

---

## Board 562 — NOTHING-WRONG (competitive); the board is lost in the 2C tree

**What I checked.**  Both tables are uncontested.  Table A is twenty-one calls of
which eleven are ours and every one is a pass; N holds `JT85.75.542.AJ62` (6 HCP,
4-2-3-4) opposite `Q62.JT9.97.T9743` (3 HCP) against a 23-count — there is no
overcall, no sacrifice (par is -1510) and `cl_pass` / `ch_pass` are right at every
turn.  The loss is at table B, where `2C - 2D - 2NT - 3C - 3H - 4H` stops in game
with thirteen tricks cold: the documented "the 2C auction has no landing ladder"
open item, and the constructive reviewer's board.

**Secondary observation, offered but NOT proposed as this board's fix.**  There is
**no defence-to-a-strong-2C context anywhere in the file**.  `defense_vs_1NT`
(`1NT - ?`), `defense_vs_weak2D/H/S_overcalls` and `defense_vs_preempt_C/D/H/S`
all exist; their 2C opening falls through to `general_competitive_low`
(`... - bid<3C - ?`), whose ladder is written for competing after a partner has
acted.  For a preempt/defence specialist that is a structural blank, but it costs
nothing here (N is balanced with 6 HCP and pass is the call) and it is a whole
context to author, not a rung, so it does not belong on this board's ticket.

**VERIFIED** only in the negative sense: I traced N's seat and `cl_pass`/`ch_pass`
are the correct calls; I did not prototype a defence-to-2C ladder.

**TEMPLATE.**  If taken up: a new `defense_vs_strong_2C` context,
`pattern: "2C - ?"`, mirroring `defense_vs_preempt_$X`'s rungs with the
lead-directing floor lowered, and — critically — the advance
(`2C - <our overcall> - P - ?`) authored in the same batch.

---

## Board 867 — E, call 2 (table B): `1S` should be `4S`

**Seat/call that went wrong.**  Table B, E, `1C 1H — ?` with `AQJT872.6.9542.5`
(7 HCP, **seven spades A-Q-J-T-8-7-2, six losers, a stiff in each black-suit
partner-and-enemy suit**).  `nx_1m1H_1S` bid a quiet forcing 1S; the auction
drifted and N/S bought it in 4H.  BEN bids 4S at both tables and 4S makes eleven
tricks.

**The missing agreement.** Over their overcall, a seven-card major with six
losers and no slam interest is bid to game at once — the preemptive value of the
jump is worth more than the extra round of description a forcing 1S buys.

```yaml
  # context: resp_1m_over_1H   (expand: { m: [C, D] }); insert before `- id: nx_1m1H_pass`
      - id: nx_1m1H_game_S
        call: 4S
        priority: 79
        requires:
          suits: { S: [7, 13] }
          hcp: [5, 10]
          evals: { ltc: [0, 6], "suit_quality(S)": [2, 9] }
        shows: "seven-card spade suit, six losers, not enough for slam: take the game myself over their overcall"
        establishes: { forcing: sign_off, agreed_suit: S }
```

**THE ANSWERING SEAT.**  `forcing: sign_off` + `agreed_suit: S`: opener's seat is
`general_competitive_high` (`... - bid>=3C - ?`) if they compete and
`general_uncontested_continuation` if they do not, and `partner_signed_off`
correctly suppresses invention.  A game bid is a contract, not a question — no
new context.

**WHAT IT ENDANGERS:**

* `nx_1m1H_1S` @78 — the forcing 1S is the right call with five or six; with
  seven and six losers it gives them two free rounds at the one and two level.
* `nx_1m1H_1NT` @50 / `nx_1m1H_2NT` @51 / `nx_1m1H_3NT` @52 — all carry
  `not: { suits: { S: [4, 13] } }`, so they cannot co-fit.
* `nx_1m1H_raise` @55 / `nx_1m1H_cue` @70 — support for partner's minor; a
  seven-card major outranks a minor fit.
* `nx_1m1H_pass` @20 — passing a seven-card major over a one-level overcall is
  never right.
* Rungs it does NOT outrank, correctly: `nx_1m1H_X` @80 (which demands **exactly
  four** spades and therefore never co-fits).
* Fallback: 4S was **not** a covered call in this context, so this rung deletes
  the code fallback for 4S after `1$m - 1H`.  The sharp `suits: { S: [7, 13] }`
  gate means the suppression only reaches hands with six spades or fewer, whose
  own rungs (`nx_1m1H_1S` at fit 1.00) already outrank any fallback.

**VERIFIED.**  Base: `1S nx_1m1H_1S fit=1.000`.  Patched: `4S nx_1m1H_game_S
fit=1.000 prio=79` chosen.  Regressions: `AQJ872.6.9542.53` (six spades) still
bids 1S — 4S falls to fit 0.171; `AQJT872.6.A542.A` (seven spades but 13 HCP and
slam interest) still bids 1S, because the `hcp: [5, 10]` ceiling is what keeps the
strong hands in the forcing channel.

**TEMPLATE.**  Ship the mirror `nx_1m1S_game_H` (call 4H) in `resp_1m_over_1S`,
and `r1H1S_game_S` / `r1S1H_game_H`-style twins in the major-opening contexts.
Do **not** template it down to the minors (5C/5D on a seven-card suit is a
different and much worse bet).

---

## Board 898 — W, call 1 (table B): `2S` should be `3S`

**Seat/call that went wrong.**  Table B, W, `1D — ?` with `AK97652.2.763.T3`
(7 HCP, **seven spades A-K-9-7-6-5-2**).  `oc1D_2S_jump` (priority 60, "weak jump
overcall: 6 spades, 5-10") outranked `oc1D_3S_preempt` (priority 58,
"preemptive overcall: seven-card s suit, 3-10") — **both fitting 1.000**.  We
preempted one level too low and sold out to 3C; BEN bid 3S at both tables and E/W
make ten tricks in spades.

**The missing agreement.** Preempt to the level of your length: six cards is the
two-level jump, seven the three level, eight the four level — the ladder must be
monotone in suit length, and today it is not.

**Why.**  The file's own comment above `oc1D_3C_preempt` states the design —
"7+ to the three level, 8+ to four" — but `oc1D_2S_jump` carries
`suits: { S: [6, 7] }` **and** the higher priority, so a seven-card suit fits both
rungs and the lower one wins.  The four-level rung is likewise below the
three-level rung (59 vs 58 is right, but both are below 60).

```yaml
  # in each of overcalls_of_1C / overcalls_of_1D / overcalls_of_1H / overcalls_of_1S:
  #   oc1x_3<suit>_preempt :  priority: 58  ->  priority: 60.5
  #   oc1x_4<suit>_preempt :  priority: 59  ->  priority: 61.5
  # (12 three-level rungs and 6 four-level rungs; no other field changes)
      - id: oc1D_3S_preempt
        call: 3S
        priority: 60.5          # was 58
        when: { unbid_suit: S }
        requires:
          suits: { S: [7, 13] }
          hcp: [3, 10]
          evals: { "suit_quality(S)": [1.5, 9], "quick_tricks_outside(S)": [0, 2] }
        shows: "preemptive overcall: seven-card s suit, 3-10"
        establishes: { forcing: non_forcing }
```

**NOT the excluded item.**  `DECISIONS.md` rules out re-ranking **the weak jump
overcall against the SIMPLE overcall** (`oc1x_1S` @71; round 11 measured -24 held
out).  `oc1x_1S` is untouched here and stays at 71 — verified: an eight-card suit
with 11 HCP still chooses 1S.  What moves is the seven-card preempt against the
six-card jump, a different pair of rungs and a different hand type.

**THE ANSWERING SEAT.**  Already authored: `advance_weak_jump_overcall`
(`1$o - 3$j - P - ?`) covers the advance of a three-level preemptive overcall.
This is one reason to prefer the priority lift to a length gate — the seat behind
3S exists and the seat behind a starved hole would not.

**WHAT IT ENDANGERS** (the full list of rungs 60.5 can now outrank):

* `oc1x_2$M_jump` @60 — the six-card weak jump; with seven cards the three level
  is the Law level and the two level under-competes.  It keeps every hand the
  preempt rung rejects (verified: a six-card suit still bids 2S, fit 0.349 for 3S).
* `oc1x_3$m_jump` @59 (six-card minor weak jump at the three level) — same call
  level, longer suit wins.
* `oc1x_4$M_preempt` @59 — lifted **together** to 61.5 so the eight-card rung
  stays above the seven-card one; without that half the change the lift would
  push eight-card hands down to 3S, which is the mistake this fix is about.
* `oc1x_pass` @25 — unaffected.
* Rungs it must NOT outrank, and does not: `oc1x_1$M` @71, `oc1x_X` @72,
  `oc1x_1NT` @82 — a strong hand still overcalls or doubles.  Verified with
  `AKQ9765.A2.A63.3` (15 HCP, seven spades): still 1S.
* No rung is added and no `when` changes, so **no code fallback is deleted**.
  That is the second reason to prefer this shape of fix.

**VERIFIED.**  Base chooses `2S oc1D_2S_jump`; patched chooses
`3S oc1D_3S_preempt fit=1.000 prio=60.5`.  Three regressions run (six-card,
eight-card, strong seven-card) and all behave as described.

**TEMPLATE.**  Not a template — a two-number edit repeated across the four
`overcalls_of_1x` contexts (18 rungs).  The same monotonicity should be checked
in `sandwich_seat` (`sw_*_jump` @69 vs `sw_3*` @68) and in
`defense_vs_weak2*`, which I have not traced.

---

## Board 997 — NOTHING-WRONG (competitive); a constructive opener's-rebid board

**What I checked.**  Table A is uncontested throughout (`P 1H P 1S P 2C P 2S P P`)
and the divergence is opener's rebid with `K4.QJ654.A.AK875` (17 HCP): `2C`
(`ob_1H1S_2m`, "second suit: 4+ clubs") where BEN jumps to 3C, after which we
stop in 2S making eleven with 4S cold.  That is the opener's-rebid ceiling
(`ob_1H1S_3C_jump` demands 18-21 and fits only 0.800 on a 17-count with a
five-card suit and a stiff), and it belongs to the constructive reviewer.

Table B contains three of our competitive decisions and all three are right:
W passes over 1H with `862.A32.J865.Q93` (7 HCP, no suit); E passes in the
**sandwich seat** over `1H - P - 1S` with `J5.K97.KT74.T642` (7 HCP, no
four-card suit worth naming and no shape); and E passes again over 3C.  N/S hold
a 26-count with an eleven-trick spade fit — there is nothing for E/W to compete
with and no sacrifice (they are the vulnerable side).

**Observation.**  The only competitive-discipline note worth recording is the
same sandwich-seat ceiling flagged on board 945: `sw_2H`/`sw_2D` demand 11-17 and
the jump rungs demand `cheapest_in_suit: false`, so the sandwich seat has no
action at all on 5-10 with a six-card suit at the two level.  E does not have
such a hand here, so this board does not motivate it.

**VERIFIED** in the negative sense (I traced E's sandwich seat and W's two
passes; each is the highest-fitting authored call).

---

## Board 7 — S, call 3 (table A): `X` should be `3C`

**Seat/call that went wrong.**  Table A, S, `P 1D 2H — ?` with `J97.A54.J.QT8653`
(8 HCP, **six clubs, a stiff diamond, three ragged spades**).  `nxj_X`, the
negative double of a weak jump overcall, is `requires: { hcp: [8, 40] }` and
**nothing else** at priority 70; partner took it as spades and we played 4S in a
4-3 fit for -200, while the other table made ten tricks in clubs.

**The missing agreement.** A six-card suit of my own is bid, not doubled: over
their weak jump overcall a free three-level bid of my long minor shows the suit
and 9+ points, and the double is reserved for the hands that genuinely want
partner to choose.

**This is the file's own prescription, not a new idea.**  The comment on `nxj_X`
records that round 14's GATE (longest-suit cap + four-card-unbid-major) measured
-5 held out and was reverted **because the landing seats are unauthored — "two of
the nine replacement calls score below the 0.9 fast path"**.  On this exact board
the replacement, `cl_new_long3_C_hi`, scores **0.800**.  So: author the landing
rung to fit 1.00 first.  `neg_double_3level_m` has exactly **two rules** (X and
pass) and is the thinnest competitive context in the file.

```yaml
  # context: neg_double_3level_m   (expand_pairs over m and j); insert before `- id: nxj_pass`
      - id: nxj_new_$om
        call: 3$om
        priority: 71
        when: { unbid_suit: $om, cheapest_in_suit: true }
        requires:
          suits: { $om: [6, 13] }
          evals: { total_points: [9, 40], "suit_quality($om)": [1, 9] }
        shows: "a real six-card $om of my own: over their jump I bid my suit rather than double"
        establishes: { forcing: non_forcing }
      - id: nxj_new_wide_$om
        call: 3$om
        priority: 26.9
        when: { unbid_suit: $om, cheapest_in_suit: true }
        requires:
          suits: { $om: [5, 13] }
          evals: { total_points: [14, 40] }
        shows: "natural $om at the cheapest level: 5+ cards, 14+ points"
        establishes: { forcing: non_forcing }
```

**The second rung is not decoration — it is the superset guarantee.**  Defining
`3$om` in this (more specific) context makes `general_competitive_low`'s
`cl_new_C3` / `cl_new_C3_hi` / `cl_new_long3_C(_hi)` **covered**, so they vanish
from the candidate list.  `nxj_new_wide_$om` carries their band verbatim at
26.9 (they sat at 27–27.5) so the ladder can only be a superset.  Verified: a
5-card / 14-point hand behaves identically before and after.

**THE ANSWERING SEAT.**  `non_forcing`; opener's seat over `1$m - $j - 3$om - act`
is `general_competitive_high`, authored, with `ch_raise_C3/C4`, `ch_new_*`,
`ch_nt3` and `ch_pass`.  No `agreed_suit` is established (a six-card minor
opposite an unlimited opener is not yet trumps).

**WHAT IT ENDANGERS:**

* `nxj_X` @70 — the double promises 8+ HCP and no shape at all; a hand with a
  six-card suit has shape, and the double is precisely the call that mis-describes
  it.  Everything with fewer than six of the other minor still doubles.
* `nxj_pass` @20 — unaffected (its 0-7 band is disjoint).
* `cl_new_C3(_hi)`, `cl_new_long3_C(_hi)` @27–27.5 — replaced by
  `nxj_new_wide_$om` @26.9 with the same gates; that is the whole point.
* `cl_raise_D3` @31 / `cl_raise_D4` @27 (raising partner's opened minor) — these
  are in the generic context and are NOT covered by my rung (different call), so
  a hand with real support still raises.
* No call becomes uncovered, so no fallback is deleted.

**VERIFIED.**  Base: `X nxj_X fit=1.000 prio=70`.  Patched: `3C nxj_new_C
fit=1.000 prio=71` chosen.  Regressions: `KJ97.A54.J.KQ865` (five clubs, 14
points) doubles before and after, with 3C still reachable at the old effective
priority; `KJ97.A542.J4.Q86` (flat nine-count) still doubles.

**TEMPLATE.**  `$om` inside the already-`expand_pairs`ed context gives all seven
`(m, j)` combinations from one pair of rules.  The obvious companions — a natural
unbid-major rung and a raise of partner's minor — belong in the same batch,
because the ledger's whole point is that this context must be filled in, not
poked.  Only after that should the round-14 gate on `nxj_X` be re-measured.

---

## Board 13 — S, call 5 (table A): `P` should be `2S`

**Seat/call that went wrong.**  Table A, S, `P 1D X XX 2C — ?` with
`AKQ2.987.QJT83.Q` (14 HCP, **A-K-Q-2 of spades and five diamonds**).
`rdc_pass_D` — "forcing pass: partner's redouble owns the auction",
`requires: {}`, priority 50 — passed, partner passed it out, and 2C undoubled was
three off for +300 where 4S is cold for +650.

**The missing agreement.** After our redouble and their run-out, opener bids a
real four-card major at the two level; the forcing pass is for hands with nothing
to add, and a suit that plays for four tricks opposite a 10+ redouble is
something to add.

**Why the rung does not exist.**  `redouble_continuations` has natural suit rungs
only at the ONE level (`rdc_suit_H_$m` 1H @56, `rdc_suit_S_$m` 1S @55, both
`cheapest_in_suit: true`).  Once they run to 2C those calls are illegal and the
context's only remaining non-double action is the `requires: {}` forcing pass at
fit 1.00 — a floor, so nothing below it can ever be reached.

```yaml
  # context: redouble_continuations   (expand: { m: [C, D] }); insert before `- id: rdc_pass_$m`
      - id: rdc_2H_$m
        call: 2H
        priority: 51
        when: { unbid_suit: H, cheapest_in_suit: true }
        requires: { suits: { H: [4, 13] }, hcp: [12, 40], evals: { "suit_quality(H)": [2, 9] } }
        shows: "natural at the two level over their run-out: a real four-card major and opening values"
        establishes: { forcing: non_forcing }
      - id: rdc_2S_$m
        call: 2S
        priority: 51
        when: { unbid_suit: S, cheapest_in_suit: true }
        requires: { suits: { S: [4, 13] }, hcp: [12, 40], evals: { "suit_quality(S)": [2, 9] } }
        shows: "natural at the two level over their run-out: a real four-card major and opening values"
        establishes: { forcing: non_forcing }
```

**THE ANSWERING SEAT.**  `non_forcing` and it names a suit, so the redoubler
answers in `general_competitive_low` — `cl_raise_S2/S3/S4` and `cl_raise_lott4_S`
are all live and the actual N hand (`9765.AKJ4.2.K643`, four spades, 11 HCP) has
a raise available.  Contrast the call it replaces: the forcing pass
(`establishes: { forcing: one_round }`) is answered by **nobody** — after
`1D X XX 2C P P` the redoubler is in `general_balancing_low`, where `ballow_pass`
fits 1.00 and passed the "forcing" pass out at the table.  That starved seat is
the real disease; this rung routes around it, and the standalone repair —
a "partner's pass was FORCING, so double or bid" rung in `general_balancing_low` —
cannot be written today because the `when:` vocabulary has
`partner_last_call_was_double` but **no `partner_last_call_was_redouble` and no
"partner's pass was forcing"**.  That missing condition is worth a separate
ticket.

**WHAT IT ENDANGERS:**

* `rdc_pass_$m` @50 — a `requires: {}` floor; every hand with a real four-card
  major and opening values is better described by naming the suit than by a
  forcing pass nobody answers.  Everything else still passes (verified twice).
* `cl_new_S2` @26 / `cl_new_S2_hi` @26.5 / `cl_new_H2*` — same call, generic
  context, and they become covered; their band (5+ cards, 10+ points) is a subset
  of mine except in HCP, so a 10-11 point five-card major over the run-out now
  passes instead of bidding.  With partner having redoubled that is defensible,
  but it is the subtraction to name.
* Rungs it does NOT outrank, correctly: `rdc_X_$m` @57 (the penalty double with
  three of their suit stays primary — on this hand it fits only 0.015 because S
  holds a singleton club), `rdc_suit_H_$m` @56 / `rdc_suit_S_$m` @55 (one-level,
  can never be legal at the same time).

**VERIFIED.**  Base: `P rdc_pass_D fit=1.000 prio=50`.  Patched: `2S rdc_2S_D
fit=1.000 prio=51` chosen.  Regressions: `A652.987.QJT83.Q` (four RAGGED spades)
still passes — 2S falls to fit 0.044 on `suit_quality`; `A65.9872.KJT83.Q` (four
ragged hearts) still passes.

**TEMPLATE.**  `expand: { m: [C, D] }` is already on the context, so two rules
become four.  The same pair belongs in `general_after_redouble` for the
non-minor-opening cases.

---
## Board 376 — W, call 11 (table B): `X` should be `P`

**Seat/call that went wrong.**  Table B, W, `1C P 1H P 1S P 2H P 2S P P — ?` with
`Q9.J8.KJT4.A9654` (11 HCP).  `ballow_X` balanced with a takeout double;
partner (who had passed five times) sat with `KT43` of spades and 2S **made**
doubled, -470.

**The missing agreement.** A takeout double must be short in EVERY suit they have
bid, not only in the last one — with five cards in the suit opener named, the
double is not takeout, and the only unbid suit is the one partner will not have.

**The defect is a sibling gate, the species `DECISIONS.md` records for round 7.**
`ballow_reopen_X` and `balhigh_reopen_X` both carry
`evals: { max_their_suit_length: [0, 2], longest_suit_length: [0, 5] }`.
`ballow_X` and `balhigh_X` — the *commonest* doubles in the file — check only
`standing_suit_length`, i.e. the last bid suit.  W's spades were a doubleton, so
the gate passed while W held **A9654 of the opener's clubs**.

```yaml
  # context: general_balancing_low, rule ballow_X — add one line to `requires`
      - id: ballow_X
        call: X
        priority: 40
        when: { their_last_bid_suit: true, side_has_acted: false }
        requires:
          evals: { max_their_suit_length: [0, 3] }     # <-- NEW
          any_of:
            - hcp: [11, 40]
              evals: { standing_suit_length: [0, 2] }
            - hcp: [9, 40]
              evals: { standing_suit_length: [0, 1] }
        shows: "balancing double: values are marked opposite a passing partner, at most a doubleton in their suit (a singleton at 9+) and no long holding in any suit they bid"
        establishes: { forcing: one_round }
```

**THE ANSWERING SEAT.**  Unchanged — `advance_reopening_double` and
`general_pull_or_sit` already answer the double; this narrows *when* the question
is asked, it does not create a new one.

**WHAT IT SUBTRACTS** (it is a gate, so this is the whole cost):

* Balancing doubles made holding **four or more cards in a suit the opponents bid
  earlier in the auction**.  Those are exactly the doubles partner converts to
  penalties — as here — because he reads the double as promising the unbid suits
  and finds we have none to offer.
* It does **not** touch the three-card case (`[0, 3]`, not `[0, 2]`): a three-card
  holding in their opened minor is normal on a takeout double and is preserved.
  Verified with `Q9.J83.KJT42.A96` (three clubs), which still doubles at fit 1.000.
* It does not reach `ballow_reopen_X`/`ballow_reopen_X2` (they already carry a
  stricter version of the same gate) or `balhigh_X` unless the same line is added
  there, which it should be.
* Nothing becomes uncovered: `X` is still defined by three rules in the context,
  so no code fallback is created or deleted.

**VERIFIED.**  Base: `X ballow_X fit=1.000 prio=40` chosen.  Patched: fit collapses
to **0.015** and `P ballow_pass fit=1.000` is chosen — which is BEN's call at
confidence 0.99 and worth -110 instead of -470.

**TEMPLATE.**  Not a template: the identical line goes on `balhigh_X`
(`general_balancing_high`), whose `requires` is `hcp: [14, 40]` +
`standing_suit_length: [0, 2]` and has the same hole.  Two rules, one line each.
Consider auditing `cl_takeout_X` @36 for the same omission in a separate ticket —
I have not traced it.

---

## Board 488 — S, call 10 (table A): `3S` should be `P`

**Seat/call that went wrong.**  Table A, S, `P P 1S 2S P 2NT P 3C P P — ?` with
`AQJT74.JT.93.A53` (12 HCP, six spades).  `balhigh_rebid_S3` rebid the suit in the
passout seat; partner holds a **singleton spade** and 3S was three off, -150.

**The missing agreement.** In the passout seat, with a partner who has never bid
and no fit anywhere, my own six-card suit is not a reason to compete at the three
level against opponents who have shown a two-suiter and stopped.

**Why the existing floor cannot stop it.**  `balhigh_rebid_S3` is
`total_points`-gated only ("values for the level opposite partner's shown range"),
and opposite a silent partner "partner's shown range" is zero, so a 12-count with
six spades fits it 1.000.  The only pass in the context is `balhigh_pass`
(`requires: {}`, priority 21), a floor that can never outrank anything.

```yaml
  # context: general_balancing_high   (insert before `- id: balhigh_raise_C2`)
      - id: balhigh_pass_silent_partner
        call: P
        priority: 29.5
        when: { partner_has_acted: false, side_has_acted: true }
        requires:
          hcp: [0, 15]
          evals: { lott_total_trumps: [0, 7] }
        shows: "partner has never bid and we have no known fit: their contract stands"
        establishes: { forcing: non_forcing }
```

**THE ANSWERING SEAT.**  None — a pass in the passout seat ends the auction.
`side_has_acted: true` restricts it to auctions where *I* have already bid (so it
never silences a genuine first balancing action), and `partner_has_acted: false`
is the whole premise.

**WHAT IT ENDANGERS:**

* `balhigh_rebid_S3`/`H3`/`D3`/`C3` @29 — repeating my suit at the three level with
  a silent partner and a seven-trump maximum; the sharp `lott_total_trumps: [0, 7]`
  gate means it only fires when we have NO known eight-card fit.
* `balhigh_nt3` @29 — 3NT on 13-15 opposite a partner who never bid is a
  25-point contract on 15 points.  The `hcp: [0, 15]` ceiling is exactly the line:
  with 16+ we still bid (verified: a 17-count with the same shape still bids 3S).
* `balhigh_new_*3` @27, `balhigh_new_*4` @28, `balhigh_nt1/nt2` @27/28,
  `balhigh_pass` @21 — all below it; introducing a new suit at the three level
  opposite silence is the same error one suit over.
* Rungs it does NOT outrank, correctly: `balhigh_raise_*3` @31,
  `balhigh_raise_lott4_*` @32 (these need a partner suit and so cannot co-fire
  with `partner_has_acted: false`), `balhigh_X` @40, `balhigh_reopen_X` @41.
* PASS is already covered by `balhigh_pass`, so no fallback is deleted.

**VERIFIED.**  Base: `3S balhigh_rebid_S3 fit=1.000`.  Patched:
`P balhigh_pass_silent_partner fit=1.000 prio=29.5` chosen — BEN's call at 0.97.
Regression: the same shape with 17 HCP (`AQJT74.JT.K3.AK5`) still bids 3S, the
new pass dropping to fit 0.134.

**TEMPLATE.**  Ship the twin `ballow_pass_silent_partner` in
`general_balancing_low` at priority 29.5 with the identical gates.  Do **not**
put it in `general_competitive_low/high` — there the auction is still live and
passing is not the last word.

---

## Board 544 — W, call 3 (table B): `P` should be `X`

**Seat/call that went wrong.**  Table B, W, `2H P P — ?` with `A.AQ96.KJ43.AJ84`
(**19 HCP, 1-4-4-4**).  `ballow_pass` passed out their weak two.  We scored -100
defending 2H; the other table's E/W bid and made 4S for 450.

**The missing agreement.** In the balancing seat 17+ has to act whatever the
shape — the double is made on strength when it cannot be made on shortness,
exactly as `oc1S_X`'s `hcp: [17, 40]` branch already does in the direct seat.

**The defect is another sibling gap.**  Every direct-seat takeout double in the
file carries a strength branch with no shape condition:
`oc1S_X: any_of: [ {11-16, short spades, 3+ elsewhere}, {17+, ...} ]`.
`ballow_X` has **no such branch** — it requires `standing_suit_length: [0, 2]`
unconditionally, so a 19-count holding A-Q-9-6 of their hearts fits it **0.015**
and the seat falls through to a pass at fit 1.00.

```yaml
  # context: general_balancing_low   (insert before `- id: ballow_raise_C2`)
      - id: ballow_X_strong
        call: X
        priority: 32.5
        when: { their_last_bid_suit: true, side_has_acted: false }
        requires:
          hcp: [17, 40]
          evals: { longest_suit_length: [0, 4] }
        shows: "too strong to pass out: 17+ in the balancing seat with no long suit of my own"
        establishes: { forcing: one_round }
```

**THE ANSWERING SEAT.**  `forcing: one_round`, and the answering seat is authored
in two places: `advance_weak2_double_H` (`2H - X - P - ?`, a full suit/notrump
ladder) and `general_pull_or_sit`.  This is the reason the rung is safe to add —
the conversation it opens already has a second half, which is exactly what round
17's cue-bid experiment did not.

**WHAT IT ENDANGERS** — and the priority is chosen carefully, at **32.5, below the
natural notrump and below any five-card suit**:

* `ballow_pass` @21 — passing out a weak two with 19 HCP is the error.
* `ballow_new_*3` @27, `ballow_nt1` @27, `ballow_nt2`/`ballow_nt3` @28/29,
  `ballow_rebid_*` @29 — all describe hands with a suit or a stopper to show; a
  1-4-4-4 19-count has neither and double is the only call that shows the values.
* `ballow_raise_*` @30-32 — these need a partner suit, and `side_has_acted: false`
  means partner has none.
* Rungs it does NOT outrank, deliberately: **`ballow_nt2_balance` @33**
  (15-21 balanced with a stopper — 2NT is the better call with that hand, verified:
  `A54.AQ96.KJ3.AJ8` still bids 2NT), `ballow_X` @40 and `ballow_reopen_X` @41
  (the shape-based doubles stay primary).
* The `longest_suit_length: [0, 4]` gate is what keeps the natural suit rungs
  alive: verified, `AKJ85.A6.KQ43.J8` (17 HCP, five spades) is unaffected.
* `X` is already covered by three rules here, so no fallback is deleted.

**VERIFIED.**  Base: `P ballow_pass fit=1.000` (X at 0.015).  Patched:
`X ballow_X_strong fit=1.000 prio=32.5` chosen — BEN's call at 0.89.
Regressions: balanced-18 still bids 2NT; five-card-suit-17 unchanged; a 15-count
with the same 1-4-4-4 shape (`A.AQ96.KJ43.QJ84`) — **this one now doubles too**,
because 17 is a soft floor and 15 misses it by two.  That is the honest risk in
this rung and the reason to measure it rather than assume it.

**TEMPLATE.**  Ship the twin `balhigh_X_strong` in `general_balancing_high`
(same gates; `balhigh_X`'s own floor is already 14, so set this one at 18+ there
to keep the bands from overlapping).  No suit expansion.

---

## Board 797 — NOTHING-WRONG (competitive); a soft-miss inside an uncontested Stayman auction

**What I checked.**  Both tables are uncontested from the first call.  At table B
the divergence is E's `3NT` over partner's `3S` invitation after
`1NT P 2C P 2S P 3S P`, with `A864.A85.K53.A72` (15 HCP, **four-card spade
support**).  The candidate list is the textbook soft-miss lottery the ledger
describes: `uc_pass` fit 1.000 @18, `uc_nt3` fit **0.946** @29, `uc_raise_S4`
fit 0.605 @32 — the winner clears the 0.9 fast path by four hundredths and the
call that is right on the cards (4S, ten tricks) is the one that misses.  The
structural cause is that the seat answering a 3M raise after Stayman has no
context (`stayman_invite_accept_2S` covers only the 2NT invitation), so a
game-force landing decision is made by the generic notrump ladder.  That is the
constructive reviewer's board and the documented soft-miss open item.

At table A our three competitive decisions over their 1NT-Stayman auction
(`v1NT_pass` with `J9.K7.AT84.KQ985`, then `cl_pass`, `cl_pass`) are all correct:
S has 13 HCP but a five-card club suit and no fit, both opponents are limited and
bidding, and N holds 4 HCP.  There is no balancing seat (they bid 3S and it was
passed to N, not to S).

**Observation.**  The only competitive note is that our seat over their 1NT
opening is `defense_vs_1NT` and it has no rung at all for a 13-count with a good
five-card minor.  `v1NT_pass` is right at these colours (both vulnerable) but the
context is thin.

**VERIFIED** in the negative sense (traced S's seat over 1NT and N's two passes).

---

## Board 897 — E, call 4 (table B): `P` should be `3S`

**Seat/call that went wrong.**  Table B, E, `P 2H X 3H — ?` with
`A9762.5.KT42.J64` (8 HCP, **five spades, a singleton in their suit**), opposite
partner's takeout double of the weak two.  `ch_pass`.  We defended 3H for +100
where 4S makes ten tricks (BEN bids 3S at 0.68).

**The missing agreement.** After partner's takeout double of a weak two and their
raise, advancer bids his five-card major at the THREE level — the raise does not
release me from answering the double.

**Why the rung does not exist — a starved seat, precisely.**
`advance_weak2_double_raised` (`2$W - X - bid - ?`) has three rules:
`aw2r_4S_$W`, `aw2r_4H_$W` and the responsive double.  Both suit rungs carry
`cheapest_in_suit: true`, and over a raise to **3H** the cheapest spade call is
3S, not 4S — so both are structurally dead and the context can only double or
fall through.  The context was written for `2H - X - 4H - ?` and never for the
commoner `2H - X - 3H - ?`.

```yaml
  # context: advance_weak2_double_raised   (expand: { W: [D, H, S] })
  # insert before `- id: aw2r_responsive_X`
      - id: aw2r_3S_$W
        call: 3S
        priority: 57
        when: { unbid_suit: S, cheapest_in_suit: true }
        requires: { suits: { S: [5, 13] }, hcp: [8, 40] }
        shows: "advance in the long major over their raise"
        establishes: { forcing: non_forcing }
      - id: aw2r_3H_$W
        call: 3H
        priority: 56
        when: { unbid_suit: H, cheapest_in_suit: true }
        requires: { suits: { H: [5, 13] }, hcp: [8, 40] }
        shows: "advance in the long major over their raise"
        establishes: { forcing: non_forcing }
```

**THE ANSWERING SEAT.**  `non_forcing`, and the doubler's seat is
`general_competitive_high` — `ch_raise_S3/S4`, `ch_raise_lott_S4`,
`ch_neg_major_S*` and `ch_pass` are all live, so the 3S advance can be raised to
game or passed.  Gates and bands are copied verbatim from the existing
`aw2r_4S_$W` / `aw2r_4H_$W` so the pair is a strict level-mirror, which is also
what the `sibling` lint wants to see.

**WHAT IT ENDANGERS** — note that this rung takes over `3S`/`3H` in this context,
so the rules it displaces are in the LESS specific `general_competitive_high`:

* `ch_free_3S` @30 ("free bid: 5+ good spades over their jump, 10+", fit 0.606
  here) — becomes covered.  My band (5+ spades, 8+, no suit-quality test) is a
  superset in strength and a subset in quality, so a ragged five-card major with
  12 HCP will now bid 3S where it previously doubled.  Opposite a takeout double
  that is the better call, but it IS the subtraction to name.
* `ch_advance_x3_S` @28.5 ("answering partner's takeout double in my own suit",
  fit 0.264) — same call, strictly worse fit on this hand.
* `aw2r_responsive_X` @55 — it already denies a five-card major
  (`not: { any_of: [ {S: [5,13]}, {H: [5,13]} ] }`), so the two can never co-fit.
  Verified: with only **four** spades the responsive double still wins.
* `ch_pass` @22 — passing partner's takeout double of a weak two with five spades
  is the error.
* Fallback: `3S` was not a covered call in this context, so this rung does delete
  the 3S code fallback after `2$W - X - bid`.  The sharp `suits: { S: [5, 13] }`
  gate keeps the suppression away from every hand the rung wants.

**VERIFIED.**  Base: `P ch_pass fit=1.000`.  Patched: `3S aw2r_3S_H fit=1.000
prio=57` chosen.  Regressions: four spades → responsive double, unchanged;
`2H - X - 4H` → still `4S aw2r_4S_H`, so the four-level twins are untouched.

**A note on table A of the same board, which I checked and am NOT proposing.**
N's `3H` (`cl_raise_lott3_H`, four trumps and 7 HCP with Q-J-T of spades) over
their 2NT overcall of our weak two is the raise the ledger has already ruled on
twice; it also happens to be the wrong side of the Law (partner showed six, I hold
four, so the Law level is FOUR).  Raising to four with three defensive tricks is
not obviously right either, and `cl_raise_lott3_$M` is on the do-not-re-propose
list, so I leave it.  The real hole on this board is the advancer's, above.

---
## Board 15 — E, call 2 (table B): `1H` should be `1S`

**Seat/call that went wrong.**  Table B, E, `P 1C — ?` with `KQT52.KQT75.Q42.`
(12 HCP, **5-5 in the majors, void in their club suit**).  `oc1C_1H` and
`oc1C_1S` both fit **1.000 at priority 71** — an exact tie, broken by file order
in favour of hearts.  E/W belong in spades (nine tricks; at the other table
they played 3S) and after 1H the spade fit was never found.

**The missing agreement.** With two five-card suits, overcall the HIGHER one:
1S first leaves 2H available at the same level, while 1H first makes the spade
suit cost a level to show.  This is the same "higher of equal length" rule the
file already applies to openings ("5-5 in the majors opens 1S").

```yaml
  # context: overcalls_of_1C   (insert before `- id: oc1C_2D_jump`)
      - id: oc1C_1S_two_suited
        call: 1S
        priority: 71.5
        requires:
          suits: { S: [5, 13], H: [5, 13] }
          hcp: [8, 16]
          evals: { "suit_quality(S)": [1, 9] }
        shows: "5-5 in the majors: overcall the higher suit first so both can be shown cheaply"
        establishes: { forcing: non_forcing }
```

**THE ANSWERING SEAT.**  `non_forcing`; the advance is `advance_overcall`
(`1$o - 1$v - P - ?`) and the competitive contexts, all authored.  Nothing new is
owed — and note this rung REMOVES an `is_clear=False` priority tie, which the
ledger measures at -76 gap points across the corpus.

**WHAT IT ENDANGERS:**

* `oc1C_1H` @71 — the tie it breaks.  Both calls describe the hand; only one
  leaves room to describe it twice.
* `oc1C_1S` @71 — same call, wider gate; kept, this is the 5-5 branch on top.
* `oc1C_1D` @70, `oc1C_2H_jump`/`oc1C_2S_jump` @60 (which need six),
  `oc1C_pass` @25 — all strictly worse descriptions of a 5-5 twelve-count.
* Rungs it does NOT outrank, correctly: `oc1C_X` @72 (whose strong branch already
  excludes a good five-card heart suit) and `oc1C_1NT` @82.
* No fallback effect: 1S is already covered by `oc1C_1S`.

**VERIFIED.**  Base: `1H oc1C_1H` (tie).  Patched: `1S oc1C_1S_two_suited
fit=1.000 prio=71.5`.  Regression: 6-4 in hearts and spades (`KQT5.KQT752.Q42.`)
still overcalls 1H — the six-card suit is bid first regardless of rank, which is
correct and is why the rung demands 5+ in BOTH majors rather than "spades ≥ hearts".

**TEMPLATE.**  Four contexts, and inside each one every pair of suits where the
higher can still be bid at the cheapest level: `oc1C_1S_two_suited`,
`oc1D_1S_two_suited`, `oc1D_1H_two_suited`(H over D with 5-5 H/S is the 1S rung),
`oc1H_1S_two_suited`, `oc1H_2D_two_suited`, `oc1S_2H_two_suited`,
`oc1S_2D_two_suited`.  These are not templated contexts, so the family is written
out; the same rule belongs in `sandwich_seat` (which IS templated,
`expand: { o: [C, D, H, S] }`).

---

## Board 20 — N, call 8 (table A): `P` should be `3H`

**Seat/call that went wrong.**  Table A, N, `P 1NT 2H X P 2S P P — ?` with
`763.K963.842.A95` (7 HCP, **four-card support for partner's overcalled hearts**).
`ballow_pass` sold out to 2S, which made nine tricks for -140.  3H makes ten
tricks double-dummy (+140 at the other table): a 280-point swing on one call.

**The missing agreement.** The level of a competitive raise follows the Law, not
the point count: four trumps opposite a partner who has overcalled a five-card
suit is nine combined trumps, and nine trumps belong at the three level whatever
my six or seven points say.

**Why the ladder cannot reach it.**  `general_balancing_low` has
`ballow_raise_H2` (30, "3+ trumps, 6-9 support points") — but 2H is illegal over
their 2S, so the 6-9 branch has **no three-level rung at all**; the next one up,
`ballow_raise_H3` (31), demands `total_points: [10, 40]` and `rule_of_26 >= 22`
and fits **0.001**.  The context jumps straight from a 6-9 raise that cannot be
made to a 10+ raise that does not fit, and the hole is a pass by construction.

```yaml
  # context: general_balancing_low   (insert before `- id: ballow_raise_H4`)
      - id: ballow_raise_lott3_H
        call: 3H
        priority: 31.5
        when: { partner_suit: H, is_competitive: true, cheapest_in_suit: true }
        requires:
          suits: { H: [4, 13] }
          evals: { total_points: [6, 11], "lott_total_trumps(H)": [9, 26] }
        shows: "the Law at the three level: four trumps opposite partner's overcall, nine combined - the level follows the fit, not the points"
        establishes: { forcing: non_forcing, agreed_suit: H }
      - id: ballow_raise_lott3_S
        call: 3S
        priority: 31.5
        when: { partner_suit: S, is_competitive: true, cheapest_in_suit: true }
        requires:
          suits: { S: [4, 13] }
          evals: { total_points: [6, 11], "lott_total_trumps(S)": [9, 26] }
        shows: "the Law at the three level: four trumps opposite partner's overcall, nine combined - the level follows the fit, not the points"
        establishes: { forcing: non_forcing, agreed_suit: S }
```

**THE ANSWERING SEAT.**  `non_forcing` + `agreed_suit`, so partner's seat is
`general_competitive_high`/`general_balancing_high`, both authored, and
`agreed_suit` unlocks the `gf_landing` and slam families should partner be huge.
The rung deliberately does NOT establish an invitation, because a Law raise is a
statement about shape and partner must not treat it as values.

**WHAT IT ENDANGERS:**

* `ballow_pass` @21 — selling out at the two level with nine trumps is the error
  the Law exists to prevent.
* `ballow_nt2` @28 / `ballow_nt3` @29 / `ballow_new_*` @25-27 — bidding notrump or
  a new suit with four-card support for partner's overcalled major is a worse
  description; all fit ≈0 here anyway.
* `ballow_raise_H3` @31 — same call, disjoint band (6-11 vs 10+), so the two
  overlap only at 10-11 where either sentence is true.
* Rungs it does NOT outrank, correctly: `ballow_raise_H4` @32 and
  `ballow_raise_lott4_H` @32 — with TEN trumps the Law level is four, and those
  rungs still own it.
* **Relationship to the do-not-re-propose list.**  `cl_raise_lott3_$M` is excluded
  (round 11 freed its `cheapest_in_suit` gate, measured -3 held out twice).  This
  is a different rung in a different context: `cl_raise_lott3_$M` is a
  **preemptive raise on a weak hand in the direct seat** and was unreachable
  because a Law raise is a jump; `ballow_raise_lott3_$M` is in the **passout
  seat**, where the cheapest raise IS the three level, and its `9+ combined
  trumps` gate is a fit statement rather than a strength one.
* `is_competitive: true` keeps it out of uncontested auctions entirely.

**VERIFIED.**  Base: `P ballow_pass fit=1.000` (the 3H raise fits 0.001).
Patched: `3H ballow_raise_lott3_H fit=1.000 prio=31.5` chosen — BEN's call at
0.67.  Regressions: with only three trumps (`763.K93.8642.A95`) the engine still
passes, the rung falling to fit 0.029 on the sharp LOTT gate; with 11 points and
four trumps it bids 3H, which is what both rungs would have wanted.

**TEMPLATE.**  Two rules as written (H and S).  The minors deserve the same
treatment (`ballow_raise_lott3_C/D`) but at a higher trump bar, and the twins in
`general_balancing_high` are a separate question because the three level is
already behind us there.

---

## Board 60 — NOTHING-WRONG (competitive); and a NEGATIVE result worth recording

**What I checked.**  The 10-IMP hole is table A, where we opened 2C on
`Q.K7.AK5.AKQT543` and walked `2C-2D-3C-3S-4C-5C` into 5C one off with 3NT (ten
tricks) cold.  That is the documented "the 2C auction has no landing ladder" open
item and belongs to the constructive reviewer.

Table B contains our one competitive decision, and **it was a winner**: E
overcalled `2S` on `AK8542.2.QJ62.J6` (11 HCP, six spades) over their strong 2C,
via `cl_new_S2` at priority 26.  BEN would pass (confidence 0.57).  The overcall
pushed N/S out of the notrump game — they signed off in 3C for +110 instead of
the 3NT that makes ten tricks for +630.  **The engine's undisciplined treatment of
their strong 2C gained about 11 IMPs on this board.**

**The negative result, stated plainly.**  On board 562 I noted that the file has
no defence-to-a-strong-2C context at all: their 2C falls into
`general_competitive_low`, which treats it as any other suit bid and lets a
2-level overcall in with 10+ points.  My first instinct was that this wants a
disciplined `defense_vs_strong_2C` context.  **This board is evidence against
that**, and I am recording it rather than shipping it: the loose overcall is
obstructive against a hand that has already announced game values, which is
exactly when obstruction is worth the most.  Any such context must therefore be
LOOSER than the generic ladder, not tighter, and must be measured with the
lead-directing and preemptive wins in the denominator.

A second, structural reason not to write it as a new context: `pattern: "2C - ?"`
has specificity 1002 against `general_competitive_low`'s 3, so it would DEFINE
every call it lists and delete the `cl_*` rungs for those calls — the exact
shadowing trap the ledger records for round 12's `also_patterns` experiment
(-59 paired / -106 held out).

**VERIFIED** in the negative sense: I traced E's 2S and confirmed it is
`cl_new_S2` at fit 1.000, and read the double-dummy table to price it.

---

## Board 85 — N, call 3 (table A): `P` should be `3H`

**Seat/call that went wrong.**  Table A, N, `1S 1NT 2S — ?` with
`3.987653.AT2.854` (4 HCP, **six hearts, a singleton in their suit**) opposite
partner's 15-18 notrump overcall.  `cl_pass`.  They played 2S for eight tricks,
-110; N/S make **ten tricks in hearts** and the other table scored +170 in 3H.

**The missing agreement.** Opposite a partner who has already limited himself
high — a 1NT overcall, a strong notrump opening — my six-card suit is bid on
LENGTH, not on points: the partnership's values are already counted and my job
is to name the trump suit before they buy the hand.

**Why the ladder cannot reach it.**  Every natural three-level rung in
`general_competitive_low` is gated on `total_points` — `cl_new_long3_H` wants
"a SIX-card suit, **11+ points**" — a threshold written for auctions where partner
is unlimited.  With 4 HCP and a six-card suit it fits **0.001** and the seat is a
pass by construction.  Nothing in the file distinguishes "partner is unlimited, so
count your points" from "partner has told me his points, so count your tricks".

```yaml
  # context: general_competitive_low   (insert before `- id: cl_nt1`)
      - id: cl_new_long3_H_opp_limit
        call: 3H
        priority: 27.6
        when: { unbid_suit: H, cheapest_in_suit: true }
        requires:
          suits: { H: [6, 13] }
          evals: { rule_of_26: [21, 99], partner_shown_max: [0, 19] }
        shows: "a six-card H opposite a partner who has already limited himself high: the combined values are known, so the suit is bid on length"
        establishes: { forcing: non_forcing }
      - id: cl_new_long3_S_opp_limit
        call: 3S
        priority: 27.6
        when: { unbid_suit: S, cheapest_in_suit: true }
        requires:
          suits: { S: [6, 13] }
          evals: { rule_of_26: [21, 99], partner_shown_max: [0, 19] }
        shows: "a six-card S opposite a partner who has already limited himself high: the combined values are known, so the suit is bid on length"
        establishes: { forcing: non_forcing }
```

`partner_shown_max: [0, 19]` is the load-bearing gate: the evaluator returns
**40 while partner is unlimited**, so the rung is switched off opposite a takeout
double or an opening bid and switched on opposite a limited notrump.

**THE ANSWERING SEAT.**  `non_forcing`, and partner's seat over
`1S - 1NT - 2S - 3H - act` is `general_competitive_high` / `general_balancing_high`
with the full raise and pass ladder.  A 15-18 hand that likes hearts can raise to
four via `ch_raise_H4`; no new context.

**WHAT IT ENDANGERS:**

* `cl_pass` @20 — passing out their two-level contract holding six trumps and 22+
  combined points is the error.
* `cl_new_long3_H` @27 / `cl_new_long3_H_hi` @27.5 / `cl_new_H3(_hi)` @27/27.5 —
  same call, and my band is a superset only where partner is limited; they keep
  every unlimited-partner auction.
* `cl_nt1` @27 — 1NT is not legal at this height; irrelevant here but the rung
  sits just above it deliberately.
* Rungs it does NOT outrank, correctly: `cl_nt2` @28, `cl_nt3` @29,
  `cl_rebid_*` @29, every raise @30-32, `cl_negative_X` @33, `cl_takeout_X` @36.
  In particular a hand with support for partner still raises.
* No fallback effect: 3H/3S are already covered in this context.

**VERIFIED.**  Base: `P cl_pass fit=1.000` (3H at 0.001).  Patched:
`3H cl_new_long3_H_opp_limit fit=1.000 prio=27.6` chosen.  Regressions: five
hearts instead of six → still pass (fit 0.349, sharp suit gate); the **same hand
opposite a takeout double** (`1S - X - 2S`) → still pass, because
`partner_shown_max` reads 40 and the gate shuts.

**TEMPLATE.**  Two rules here (the majors), and the minors want the same rung one
level lower at `4C`/`4D` only if they are the cheapest call — I would not ship the
minors in the first batch.  The identical pair belongs in
`general_balancing_low`/`_high`.

**Note on the dossier's own first divergence, which I am NOT proposing.**  The
dossier flags table B call 0: E passes `A7542.K.73.KT972` in first seat where BEN
opens 1S at 0.76 (`open_1S_rule20` fits 0.757).  That is an opening-style /
rule-of-20 threshold question and is explicitly scope-excluded.

---

## Board 100 — S, call 6 (table A): `4H` should be `3H`

**Seat/call that went wrong.**  Table A, S, `1D 1S X P 2H P — ?` with
`K862.K9752.954.K` (9 HCP, five hearts, a **singleton king**).  `uc_raise_H4`
jumped to game "11+ support points, a real trump fit, and the values for the
level opposite partner's shown range".  4H was two off, -200; 2H takes eight
tricks and the other table scored +110.

**The missing agreement.** Partner's major after my negative double was FORCED —
it may be four cards and a minimum — so my raise of it is an invitation at the
three level, never a jump to game; only a cue bid of their suit is game-forcing.

**Why the arithmetic goes wrong.**  `uc_raise_H4` gates on
`rule_of_26: [25, 99]`, and `rule_of_26` takes the midpoint of partner's shown
range.  Opposite a 1D opening that midpoint is about 14, so 11 support points
reach exactly 25 and the rung fits 1.000 — but partner's 2H was not a free bid,
it was the answer my double demanded, and it has already denied extras by not
jumping.  The engine has no way to say "partner's last call was compelled".

```yaml
  # context: general_uncontested_continuation   (insert before `- id: uc_raise_H4`)
      - id: uc_raise_H3_after_my_double
        call: 3H
        priority: 32.5
        when: { my_last_call_was_double: true, partner_suit: H, cheapest_in_suit: true }
        requires:
          suits: { H: [4, 13] }
          evals: { total_points: [10, 13] }
        shows: "raising the suit my double asked for: partner's answer was forced, so this is an invitation and not a game bid"
        establishes: { forcing: invitational, agreed_suit: H }
      - id: uc_raise_S3_after_my_double
        call: 3S
        priority: 32.5
        when: { my_last_call_was_double: true, partner_suit: S, cheapest_in_suit: true }
        requires:
          suits: { S: [4, 13] }
          evals: { total_points: [10, 13] }
        shows: "raising the suit my double asked for: partner's answer was forced, so this is an invitation and not a game bid"
        establishes: { forcing: invitational, agreed_suit: S }
```

**THE ANSWERING SEAT — this is an INVITATION, so it ships with its answer.**
Opener, having been forced to bid 2H and now hearing 3H, is in
`general_uncontested_continuation` with `agreed_suit: H` established.  The
accepting rung already exists and fits: `uc_raise_H4` @32 (11+ support points,
`rule_of_26 >= 25`, eight combined trumps) is exactly "accept with extras", and
`uc_pass` @18 is the decline.  Traced: with the actual opener hand
(`Q9.AQJ4.QJ72.T92`, 12 HCP, four trumps) `rule_of_26` opposite a shown 10-13
lands below 25 and opener passes 3H — the contract the cards want.  No new
context, because the invitation lands in a ladder that is already two rungs deep.

**WHAT IT ENDANGERS:**

* `uc_raise_H4` @32 — the jump to game.  On 14+ support points it still wins
  (verified: `K862.K9752.95.AK` still bids 4H), because the `[10, 13]` ceiling on
  my rung is sharp at the top of the band.
* `uc_raise_H3` @31 — same call, wider band; kept below as the general case.
* `uc_raise_lott4_H` @32 — needs ten combined trumps and a known enemy fit; fits
  0.011 here and is untouched on the hands it describes.
* `uc_nt2` @28 / `uc_nt3` @29 / `uc_new_*3` @27-27.5 — inferior descriptions of a
  hand with four-card support for the suit I asked partner to name.
* Rungs it does NOT outrank, correctly: `uc_doubler_raise3_H` @33 and
  `uc_doubler_game_H` @35 (17-19 and 20+ — those are the DOUBLER raising the
  ADVANCE, a different auction, and their floors keep them clear).
* `my_last_call_was_double: true` is what confines the rung to the compelled-answer
  case; it cannot reach an ordinary raise of a freely bid suit.

**VERIFIED.**  Base: `4H uc_raise_H4 fit=1.000 prio=32`.  Patched:
`3H uc_raise_H3_after_my_double fit=1.000 prio=32.5` chosen — BEN passes at 0.86,
so BEN would stop even lower.  Regressions: 14 support points → 4H, unchanged;
four-card support instead of five → 3H, as intended.

**TEMPLATE.**  Two rules (H and S) as written.  The same pair belongs in
`general_competitive_low`/`_high` (`cl_`/`ch_raise_*3_after_my_double`), because
the identical auction with a fourth-hand raise lands there instead.

---
## Board 107 — NOTHING-WRONG (competitive); the board is lost by opener passing a 2NT response

**What I checked.**  The IMPs went at table B, where W opened 1C on
`53.5.KJ6.AKT6543` (**seven clubs headed by A-K-T**), E responded a natural 2NT
(11-12 balanced) and W **passed it** (`o2nresp_pass_C`).  2NT was three off for
-100 while 3C/5C by W is cold (twelve tricks double-dummy).  Passing a 2NT
response with a seven-card suit and a singleton is a constructive-rebid defect
and belongs to the other reviewer.

Table A: N passes twice (`uc_pass`, `ch_pass`) with `QT42.K32.Q754.Q9` (9 HCP,
three-card support for partner's sandwich 2H overcall).  BEN would raise at 0.65
and 0.51 — low confidence, and the cards agree with the pass: N/S take eight
tricks in hearts, so 3H is one off, and par for the board is **-800** to N/S.
There is no competitive error here to price.

**Two observations, neither proposed as this board's fix.**

1. **This is the documented `uc_*` mis-dispatch, in the flesh.**  `context_at`
   returns `general_uncontested_continuation` for a seat where both opponents have
   bid, because its pattern `... - P - ?` means "RHO passed".  The ledger measures
   that population at mean -1.14 against a -0.804 corpus mean and records that the
   wholesale repair measured -59/-106 and was reverted.  Nothing new to add.
2. **The raise arithmetic is worth a number.**  `uc_raise_H3` fits **0.004** on a
   nine-count with three-card support opposite a two-level overcall, because it
   wants `total_points >= 10` AND `rule_of_26 >= 22` AND eight combined trumps at
   once.  A ladder whose lowest three-level raise needs three simultaneous
   thresholds has no rung for the commonest competitive hand there is.  Board 20's
   `ballow_raise_lott3_$M` is my proposed answer to exactly that shape, in the
   context where I could verify it pays; the `uc_*` twin should follow it under
   `when: { is_competitive: true }` (the porting discipline the ledger endorses at
   +12 for `uc_raise_lott4_$M`), but only after board 20's version is measured.

**VERIFIED** in the negative sense (traced both of N's passes and the candidate
ladder behind them).

---

## Board 114 — S, call 4 (table A): `X` should be `2S`

**Seat/call that went wrong.**  Table A, S, `P P 1D 2H — ?` with
`QJT87.K53.63.QJ6` (9 HCP, **five spades Q-J-T-8-7**).  `nxj_X` again — the
negative double of a weak jump overcall, `requires: { hcp: [8, 40] }` and nothing
else.  N holds a 20-count and we stopped in a defence to 3H for +200, where the
other table bid 4S and made twelve tricks for +480.

**The missing agreement.** The negative double of a jump overcall promises
EXACTLY FOUR cards in the unbid major; with five you bid the suit.  This is the
agreement the file already keeps at the one level and nowhere else.

**The asymmetry, stated as a fact about the file.**  `resp_1m_over_1H` splits the
two hands cleanly: `nx_1m1H_X` = "negative double: **exactly 4** spades"
(`suits: { S: [4, 4] }`), `nx_1m1H_1S` = "**5+** spades, forcing".  In
`neg_double_3level_m` the same two hands share one rule with no shape gate at all,
so the five-card major has no call and the double swallows it.

```yaml
  # context: neg_double_3level_m   (expand_pairs over m and j); before `- id: nxj_pass`
      - id: nxj_major_S2
        call: 2S
        priority: 71
        when: { unbid_suit: S, cheapest_in_suit: true }
        requires: { suits: { S: [5, 13] }, hcp: [8, 40] }
        shows: "five or more spades over their jump overcall: I bid my suit; the double promises exactly four"
        establishes: { forcing: non_forcing }
      - id: nxj_major_H2
        call: 2H
        priority: 71
        when: { unbid_suit: H, cheapest_in_suit: true }
        requires: { suits: { H: [5, 13] }, hcp: [8, 40] }
        shows: "five or more hearts over their jump overcall: I bid my suit; the double promises exactly four"
        establishes: { forcing: non_forcing }
```

**THE ANSWERING SEAT.**  `non_forcing` deliberately: the ledger's repeated finding
is that a starved forcing seat is the most expensive object in this file, and
opener's seat over `1$m - 2H - 2S - act` is `general_competitive_low/high`, fully
authored, with `cl_raise_S2/S3/S4`, `cl_raise_lott4_S` and `cl_new_*`.  With N's
actual 20-count `AK4.4.AQT98.AKT3`, `cl_raise_S4` is live and reachable.

**WHAT IT ENDANGERS:**

* `nxj_X` @70 — takes away the double on hands with a five-card unbid major, which
  is precisely what the one-level twins already do.  Everything with four still
  doubles (verified: `QJT8.K532.63.QJ6` still doubles, 2S falling to fit 0.349).
* `cl_new_S2` @26 / `cl_new_S2_hi` @26.5 / `cl_new_long2_S(_hi)` @26/26.5 — these
  become **covered** by the more specific context and drop out.  My band (5+
  spades, 8+ HCP) is a superset of theirs in this auction except in one corner:
  a hand with 7 HCP plus three distribution points reaches `cl_new_S2`'s "10+
  points" but misses my 8-HCP floor.  If that matters, write the gate as
  `evals: { total_points: [8, 40] }` instead of `hcp` and the superset is exact.
* `nxj_pass` @20 and `cl_nt2` @28 — inferior descriptions of a five-card major.
* This pairs with the board-7 proposal (`nxj_new_$om` for the six-card minor).
  **Ship them together**: `neg_double_3level_m` currently has two rules, and the
  ledger's verdict on `nxj_X` is explicitly "author the landing seats first".

**VERIFIED.**  Base: `X nxj_X fit=1.000 prio=70`.  Patched:
`2S nxj_major_S2 fit=1.000 prio=71` chosen — BEN's call at 0.76.

**TEMPLATE.**  Two rules over the seven `(m, j)` pairs the context already
expands.  `cheapest_in_suit: true` + `unbid_suit` makes the pair self-selecting:
over `2H` only the spade rung is legal-and-cheapest, over `3S` neither is, and so
on.  A three-level twin (`nxj_major_S3` over a 3H overcall) belongs in the same
batch.

---

## Board 217 — S, call 5 (table A): `X` should be `2H`

**Seat/call that went wrong.**  Table A, S, `P P 1C 1H 2D — ?` with
`A943.QJ5.K973.93` (10 HCP, **three-card support for partner's heart overcall**).
`cl_negative_X2` — "negative double at the two level: 8+ HCP with a major they
have not bid" — outranked the raise at priority 33 against 30.  We defended 3D for
-110; 3H by N takes nine tricks.

**The missing agreement.** A negative double asks partner to name a major; when
partner has already named one and I hold three of them, I raise.  The double is
for the hands with no fit.

**Why it happens.**  `cl_negative_X2`'s `when` is
`{ their_last_bid_suit: true, side_has_acted: true, i_have_acted: false, standing_bid_level: [2] }`
— `side_has_acted: true` is satisfied when partner **overcalled** just as much as
when partner **opened**, and the constraint asks only for a major "they" have not
bid.  Partner's hearts are not their suit, so a four-card spade holding lets the
double fire straight over a heart fit.  `cl_raise_H2` fits **1.000** and loses on
three points of priority.

```yaml
  # context: general_competitive_low   (insert before `- id: cl_raise_lott3_H`)
      - id: cl_raise_H2_over_overcall
        call: 2H
        priority: 33.5
        when: { partner_suit: H, cheapest_in_suit: true, is_competitive: true }
        requires:
          suits: { H: [3, 13] }
          evals: { total_points: [6, 13], partner_shown_max: [0, 18], "lott_total_trumps(H)": [8, 26] }
        shows: "three-card support for partner's overcall: raise, rather than double for a suit partner has not promised"
        establishes: { forcing: non_forcing, agreed_suit: H }
      - id: cl_raise_S2_over_overcall
        call: 2S
        priority: 33.5
        when: { partner_suit: S, cheapest_in_suit: true, is_competitive: true }
        requires:
          suits: { S: [3, 13] }
          evals: { total_points: [6, 13], partner_shown_max: [0, 18], "lott_total_trumps(S)": [8, 26] }
        shows: "three-card support for partner's overcall: raise, rather than double for a suit partner has not promised"
        establishes: { forcing: non_forcing, agreed_suit: S }
```

`partner_shown_max: [0, 18]` is what confines the rung to an OVERCALL: an overcall
caps partner at 16-17, an opening bid at 21, and an unlimited partner reads 40.
Verified: with partner having **opened** 1H the rung never appears (the auction
lands in `resp_1M_over_2x` and the cue bid still wins).

**THE ANSWERING SEAT.**  `non_forcing` + `agreed_suit: H`, so partner's seat is
`general_competitive_high` with the raise, game and Law rungs live; and
establishing the agreed suit is itself worth something, because the whole
`gf_landing` and slam family is gated on `agreed_suit`.

**WHAT IT ENDANGERS:**

* `cl_negative_X1`/`cl_negative_X2` @33 — the double, on exactly the hands where
  we have a known eight-card fit.  Without three-card support the rung does not
  fit and the double is untouched (verified: with a doubleton heart the engine
  reverts to passing / doubling as before).
* `cl_raise_H2` @30 / `cl_raise_H3` @31 — same suit, same idea; this is the branch
  that has to beat the double, and the lower rungs keep everything else.
* `cl_nt2` @28, `cl_new_S2(_hi)` @26/26.5, `cl_pass` @20 — all inferior with a fit.
* Rungs it does NOT outrank, correctly: `cl_doubler_raise_*` @34,
  `cl_doubler_game_*` @35, `cl_takeout_X` @36, `cl_nt2_direct` @37 — the strong
  hands still speak first.
* No fallback effect: 2H is already covered by `cl_raise_H2` / `cl_new_H2`.

**VERIFIED.**  Base: `X cl_negative_X2 fit=1.000 prio=33`.  Patched:
`2H cl_raise_H2_over_overcall fit=1.000 prio=33.5` chosen — BEN's call at 0.96.
Regressions: two-card support → unchanged; partner having opened → unchanged.

**TEMPLATE.**  Two rules (H and S) here, twins in `general_competitive_high`
(`ch_raise_*2_over_overcall`, and a three-level version since the cheapest raise
is higher there).  The minors do not need it — `cl_negative_X` promises a major,
so it never competes with a minor-suit raise.

---

## Board 306 — N, call 10 (table A): `P` should be `4C`

**Seat/call that went wrong.**  Table A, N, `P 1S P P 2C 2H 3C 3H P P — ?` with
`8.J43.AT985.KJ84` (9 HCP, **four-card support for the club suit I have already
raised**, a singleton spade).  `balhigh_pass` sold out to 3H, -140; N/S make
**eleven tricks in clubs** and the other table scored +150.

**The missing agreement.** When both sides have found a fit and they have outbid
us, the Law says bid four of our minor — and the fact that my own diamonds are
longer than the clubs I have already agreed is irrelevant.

**Why the rung cannot fire.**  `balhigh_raise_C4` carries
`"suit_diff(C, H)": [0, 13], "suit_diff(C, S)": [0, 13]` — "the minor has to be my
longest suit or the major is the bid" — plus `lott_total_trumps(C) >= 10`.  N's
longest suit is diamonds, so the rung fits **0.020**, and there is no
`balhigh_raise_lott4_C/D` at all: the Law-at-the-four-level rungs
(`balhigh_raise_lott4_H`, `..._S`) exist **only for the majors**.  Both halves of
that are sibling gaps.

```yaml
  # context: general_balancing_high   (insert before `- id: balhigh_raise_S2`)
      - id: balhigh_raise_lott4_C
        call: 4C
        priority: 32
        when: { partner_suit: C, is_competitive: true, i_have_acted: true }
        requires:
          suits: { C: [4, 13] }
          evals: { "lott_total_trumps(C)": [9, 26], total_points: [8, 40], their_fit: [8, 26] }
        shows: "the Law at the four level in our agreed minor: nine-plus trumps our way and they have a fit too"
        establishes: { forcing: non_forcing, agreed_suit: C }
      - id: balhigh_raise_lott4_D
        call: 4D
        priority: 32
        when: { partner_suit: D, is_competitive: true, i_have_acted: true }
        requires:
          suits: { D: [4, 13] }
          evals: { "lott_total_trumps(D)": [9, 26], total_points: [8, 40], their_fit: [8, 26] }
        shows: "the Law at the four level in our agreed minor: nine-plus trumps our way and they have a fit too"
        establishes: { forcing: non_forcing, agreed_suit: D }
```

Three gates do the work and each is one sentence of bridge: `i_have_acted: true`
means I have already supported this minor, so its length relative to my own suits
no longer decides anything; `their_fit: [8, 26]` means they have found their fit,
which is what makes the Law bid safe; `lott_total_trumps >= 9` is the fit itself,
and it is sharp.

**THE ANSWERING SEAT.**  `non_forcing`; partner's seat is
`general_competitive_high`/`general_balancing_high`, and `agreed_suit: C` is
established so a big hand can still move.  No question is asked, so nothing is owed.

**WHAT IT ENDANGERS:**

* `balhigh_pass` @21 — passing out their three-level contract with nine trumps and
  eleven tricks available is exactly the error the Law exists to prevent.
* `balhigh_raise_C4` @27 — same call, and this rung is the branch its own
  `suit_diff` gates exclude.  Both stay.
* `balhigh_rebid_C4` @29, `balhigh_new_D4` @28, `balhigh_nt3` @29 — bidding my own
  diamonds (fit 0.409) instead of the agreed club fit is the worse description.
* Rungs it does NOT outrank: `balhigh_reopen_X` @41, `balhigh_X` @40 — a double
  still comes first when it fits.
* Fallback: `4C` is already covered by `balhigh_raise_C4` and `balhigh_rebid_C4`,
  so nothing is deleted.
* **Relationship to board 488's proposal.**  That one adds a PASS rung at 29.5
  gated on `partner_has_acted: false`; this one adds a 4-level raise gated on
  `i_have_acted: true` with partner's suit known.  The two `when`s are mutually
  exclusive, and I checked that they cannot both fire.

**VERIFIED.**  Base: `P balhigh_pass fit=1.000` (4C at 0.020).  Patched:
`4C balhigh_raise_lott4_C fit=1.000 prio=32` chosen — BEN's call at 0.76.
Regression: three-card support (`8.J43.AT9852.KJ8`) still passes, the rung falling
to fit 0.029 on the sharp LOTT gate.

**TEMPLATE.**  Two rules here; the identical pair belongs in
`general_balancing_low` and — under `when: { is_competitive: true }`, the porting
discipline the ledger endorses — in `general_competitive_high`.

---

## Board 325 — S, call 9 (table A): `4H` should be `3H`

**Seat/call that went wrong.**  Table A, S, `P 1D P 1H 1S P P 2H P — ?` with
`9873.K5.AKJ53.54` (11 HCP, **a doubleton in partner's suit**).  `uc_raise_H4`
raised partner's balancing 2H rebid straight to game; that started the keycard
sequence which ended in 5H one off, -100, where 3H takes ten tricks for +170.

**The missing agreement.** A doubleton opposite a six-card suit is eight trumps
and no more; with eleven points and eight known trumps you invite at the three
level and let partner decide, because he has already told you he is minimum.

**Why the rung fires.**  `uc_raise_H4`'s length floor is deliberately
`suits: { H: [2, 13] }` — the comment says "a doubleton opposite a SHOWN six-card
suit still reaches the eight-card game".  That is right when partner's six-card
suit is a *positive* action; it is wrong when the six-card suit was rebid in the
passout seat, which is a minimum by definition.  The engine has no `when` for
"partner's last call was a balancing action", so the honest separator available
today is the trump count itself: eight is not nine.

```yaml
  # context: general_uncontested_continuation   (insert before `- id: uc_raise_H4`)
      - id: uc_raise_H3_doubleton
        call: 3H
        priority: 32.5
        when: { partner_suit: H, cheapest_in_suit: true }
        requires:
          suits: { H: [2, 2] }
          evals: { total_points: [11, 14], "lott_total_trumps(H)": [8, 8] }
        shows: "only a doubleton in partner's suit and just eight known trumps: invite, do not bid the game"
        establishes: { forcing: invitational, agreed_suit: H }
      - id: uc_raise_S3_doubleton
        call: 3S
        priority: 32.5
        when: { partner_suit: S, cheapest_in_suit: true }
        requires:
          suits: { S: [2, 2] }
          evals: { total_points: [11, 14], "lott_total_trumps(S)": [8, 8] }
        shows: "only a doubleton in partner's suit and just eight known trumps: invite, do not bid the game"
        establishes: { forcing: invitational, agreed_suit: S }
```

**THE ANSWERING SEAT — it is an invitation, so here is who answers.**  Partner is
in `general_uncontested_continuation`/`general_competitive_low` with
`agreed_suit: H` set.  `uc_raise_H4` @32 is the acceptance (11+ support points,
`rule_of_26 >= 25`, eight combined trumps) and `uc_pass` @18 the decline; with N's
actual `5.AT9872.6.AKT32` the acceptance is available, which is the right answer
on the cards — 4H is ten tricks.  The rung therefore does not just stop the
overbid, it hands the decision to the hand that knows its own strength.

**WHAT IT ENDANGERS:**

* `uc_raise_H4` @32 — only on the narrow slice `exactly two trumps AND exactly
  eight combined trumps AND 11-14 points`; both length gates are sharp, so a
  three-card raise or nine trumps leaves the rung at fit ≈0.
* `uc_raise_H3` @31 — same call, wider band; kept underneath.
* `uc_nt2` @28 (fit 0.835 here) and `uc_nt3` @29 — a 4-2-5-2 with a doubleton in
  partner's six-card major is not a notrump hand opposite a balancing rebid.
* `uc_rebid_D3` @27, `uc_new_*3` @27-27.5 — repeating my own diamonds after
  partner has bid hearts twice is a worse description.
* Rungs it does NOT outrank, correctly: `gst_rkc_H` @46 (verified: a 16-count with
  the same doubleton still starts keycards — arguably wrong, but it is the
  existing slam machinery and out of my scope), `uc_doubler_*` @33-35.
* Fallback: 3H is already covered by `uc_raise_H3`, so nothing is deleted.

**VERIFIED.**  Base: `4H uc_raise_H4 fit=1.000 prio=32`.  Patched:
`3H uc_raise_H3_doubleton fit=1.000 prio=32.5` chosen — BEN passes at 0.94, so
BEN would stop even lower and the invitation is the compromise.  Regressions:
three-card support → 4H unchanged; 16 points → the keycard ask, unchanged.

**TEMPLATE.**  Two rules (H and S).  Twins belong in `general_competitive_low`
and `general_balancing_low`.  I would NOT extend the idea to the minors, where the
three level is not an invitation to anything.

---
## Board 353 — NOTHING-WRONG (competitive); an opening threshold and a constructive rebid

**What I checked.**  E/W never make a call at either table — the board is
`P P P` round to N at both, and every one of our competitive seats is a pass with
nothing to bid (`oc1S_pass` on `Q4.J8532.985.QJ3`, 6 HCP; `cl_pass`, `ch_pass`,
`balhigh_pass` thereafter, all fit 1.000 and all correct on the cards).

The dossier's first divergence is table A call 1: S passes `JT972.AT7.AQ6.95`
(11 HCP, five spades) in second seat where BEN opens 1S at 0.95 — `open_1S` fits
0.800, `open_1S_rule20` 0.606, and neither clears the fast path.  That is an
opening-style / rule-of-20 threshold and is scope-excluded.  The rest of the
damage (N's `ob_rebid_2C` where BEN rebids 1NT; S's `rmr_2NT` where BEN bids 3C)
is opener's and responder's rebid ladder in a wholly uncontested auction.

**Observation, for the record.**  The board also shows the pattern that the
excluded opening threshold and the constructive rebid interact: S's pass makes N
open 1C in fourth seat under `open_1C_rule15`, and the whole auction is then one
level low.  Nothing in that chain is a competitive-discipline defect.

**VERIFIED** in the negative sense (traced W's and E's four passes).

---

## Board 357 — N, call 11 (table A): `P` should be `4C`

**Seat/call that went wrong.**  Table A, N, `P 1C 1H X P 2C 2H 3C P P 3H — ?` with
`JT82.T6.AQJ3.A93` (12 HCP, **three-card support for the club suit I have already
raised to three**).  `ch_pass`.  They played 3H for -140; N/S take **ten tricks in
clubs** and the other table scored +130 in 4C.

**The missing agreement.** Once I have raised partner's minor, four of that minor
is the competitive continuation over their three-level bid — the length of my own
side suits stopped being relevant the moment I agreed a trump suit.

**Why the rung cannot fire.**  `ch_raise_C4` demands `rule_of_26 >= 25`,
`lott_total_trumps(C) >= 10`, **and** `"suit_diff(C, H)": [0, 13]` +
`"suit_diff(C, S)": [0, 13]` — "the minor has to be my longest suit or the major
is the bid".  N's longest suits are spades and diamonds, so the rung fits
**0.000** even though clubs are the agreed trumps.  The gate is written for the
first raise and is simply wrong on the second.

```yaml
  # context: general_competitive_high   (insert before `- id: ch_raise_S2`)
      - id: ch_raise_agreed_C4
        call: 4C
        priority: 32
        when: { partner_suit: C, is_competitive: true, i_have_acted: true, cheapest_in_suit: true }
        requires:
          suits: { C: [3, 13] }
          evals: { "lott_total_trumps(C)": [8, 26], total_points: [11, 40] }
        shows: "competing to four of the minor I have already agreed: eight-plus trumps and the values - my longer side suits stopped mattering when I raised"
        establishes: { forcing: non_forcing, agreed_suit: C }
      - id: ch_raise_agreed_D4
        call: 4D
        priority: 32
        when: { partner_suit: D, is_competitive: true, i_have_acted: true, cheapest_in_suit: true }
        requires:
          suits: { D: [3, 13] }
          evals: { "lott_total_trumps(D)": [8, 26], total_points: [11, 40] }
        shows: "competing to four of the minor I have already agreed: eight-plus trumps and the values - my longer side suits stopped mattering when I raised"
        establishes: { forcing: non_forcing, agreed_suit: D }
```

`i_have_acted: true` is the whole agreement in one gate: it is what makes "my own
longest suit" irrelevant, and it is what stops this rung from ever being a first
raise.

**THE ANSWERING SEAT.**  `non_forcing` + `agreed_suit`, answered by
`general_competitive_high`/`general_balancing_high`, both authored.  No question
is asked.

**WHAT IT ENDANGERS:**

* `ch_pass` @22 — selling out at the three level with a nine-card fit and ten
  tricks is the error.
* `ch_nt3` @29 (fit 0.668 here — a soft-miss 3NT with `T6` of their suit as the
  "stopper") and `ch_new_D4(_hi)` @28/28.5 — bidding notrump without a heart
  stopper or introducing diamonds after agreeing clubs are both worse.
* `ch_raise_C4` @27 — same call; this rung is exactly the branch its own
  `suit_diff` gates exclude, and both stay.
* `ch_rebid_C4` @29 — needs six clubs of my own; disjoint.
* Rungs it does NOT outrank: `ch_penalty_X` @38, `ch_negative_X3` @33,
  `gst_rkc_C` @46.
* Fallback: 4C already covered by `ch_raise_C4`/`ch_rebid_C4`; nothing deleted.
* **Interaction with boards 306 and 388**, which touch the same family: 306 adds
  `balhigh_raise_lott4_C/D` (`i_have_acted: true` + `their_fit`), 388 adds
  `ch_raise_lott4_C/D` (first raise, four trumps, `their_fit`).  This one is the
  `i_have_acted` branch in the competitive context and needs **no** `their_fit`,
  because on this board E never bid at all and W's hearts are a one-hand suit.
  All three are distinct `when`s; I checked they cannot fire on each other's
  boards.

**VERIFIED.**  Base: `P ch_pass fit=1.000` (4C at 0.000).  Patched:
`4C ch_raise_agreed_C4 fit=1.000 prio=32` chosen — BEN's call at 0.51.
Regression: two-card club support (`JT82.T63.AQJ3.A9`) still passes.

**TEMPLATE.**  Two rules; twins in `general_balancing_high`/`_low` and in
`general_competitive_low`.

---

## Board 388 — N, call 4 (table A): `3S` should be `4C`

**Seat/call that went wrong.**  Table A, N, `P 1H 2C 3H — ?` with
`AJT82.2.Q93.Q985` (9 HCP, **four-card support for partner's 2C overcall, a
singleton in their suit**).  `ch_free_3S` introduced a five-card spade suit; S
then took the push to 5C doubled, -200.  4C makes ten tricks (+130) and the
other table's E/W went one off in 4H.

**The missing agreement.** They have a nine-card heart fit and we have a nine-card
club fit: the Law says four of our suit, and support for partner's overcall
outranks introducing a suit of my own.

**Why the rung cannot fire — a pure sibling gap.**  The context has
`ch_raise_lott4_H` and `ch_raise_lott4_S` ("the Law at the four level: they have a
fit and so have we") and **no minor-suit equivalent at all**.  The only 4C rung is
`ch_raise_C4`, which wants `rule_of_26 >= 25`, ten combined trumps and clubs as my
longest suit; it fits **0.066**.

```yaml
  # context: general_competitive_high   (insert before `- id: ch_raise_S2`)
      - id: ch_raise_lott4_C
        call: 4C
        priority: 32
        when: { partner_suit: C, is_competitive: true }
        requires:
          suits: { C: [4, 13] }
          evals: { "lott_total_trumps(C)": [9, 26], total_points: [8, 40], their_fit: [8, 26] }
        shows: "the Law at the four level in our minor: nine-plus trumps our way and they have a fit too"
        establishes: { forcing: non_forcing, agreed_suit: C }
      - id: ch_raise_lott4_D
        call: 4D
        priority: 32
        when: { partner_suit: D, is_competitive: true }
        requires:
          suits: { D: [4, 13] }
          evals: { "lott_total_trumps(D)": [9, 26], total_points: [8, 40], their_fit: [8, 26] }
        shows: "the Law at the four level in our minor: nine-plus trumps our way and they have a fit too"
        establishes: { forcing: non_forcing, agreed_suit: D }
```

Gates are copied from `ch_raise_lott4_H` verbatim except the trump bar, which
drops from ten to **nine**: four of a minor is one trick lower than four of a
major, so the Law level is reached with one trump fewer.  `their_fit: [8, 26]` is
what makes it a Law bid rather than a guess.

**THE ANSWERING SEAT.**  `non_forcing` + `agreed_suit: C`; partner answers in
`general_competitive_high`, authored.  Crucially it also STOPS a conversation
that was going wrong: with `agreed_suit` set, S's 5C would have had a trump
agreement behind it instead of being `ch_rebid_C5` on a guess.

**WHAT IT ENDANGERS:**

* `ch_free_3S` @30 — "free bid: 5+ good spades over their jump, 10+".  With
  four-card support for partner's suit and a singleton in theirs, supporting is
  the better description; introducing a second suit at the three level invites
  exactly the 5C disaster that followed.
* `ch_negative_X3` @33 — higher, untouched (fit 0.279 here).
* `ch_raise_C4` @27, `ch_new_long3_S(_hi)` @27/27.5, `ch_new_S3(_hi)` @27/27.5,
  `ch_pass` @22 — all below and all worse descriptions of a 5-1-3-4 with support.
* Rungs it does NOT outrank: `ch_penalty_X` @38, `gst_rkc_C` @46.
* Fallback: 4C already covered by `ch_raise_C4`; nothing deleted.

**VERIFIED.**  Base: `3S ch_free_3S fit=1.000 prio=30`.  Patched:
`4C ch_raise_lott4_C fit=1.000 prio=32` chosen — BEN's call at 0.58.
Regression: three-card club support (`AJT82.72.Q93.Q98`) still bids 3S, the rung
falling to fit ≈0 on the sharp LOTT gate.

**TEMPLATE.**  Two rules here; the twins belong in `general_competitive_low`
(`cl_raise_lott4_C/D` — that context has the major pair and the same minor hole)
and in `general_balancing_low`.

---

## Board 432 — W, call 3 (table B): `X` should be `3S`

**Seat/call that went wrong.**  Table B, W, `P 1H 3C — ?` with
`KQT42.Q.AQ942.Q5` (15 HCP, **five spades K-Q-T-4-2 and five diamonds**).
`nx3_negx` — "negative double through 3S: 4+ cards in the other major, 8+ HCP" —
at priority 70, against a natural 3S fitting **1.000** at priority 30.  Partner
pulled to 3H, we corrected to 3S anyway two rounds later, and E/W stopped in a 3S
that takes ten tricks while their side made 4H at the other table.

**The missing agreement.** The negative double of a three-level overcall promises
exactly four cards in the unbid major; with five you bid the suit — the same
split the file already keeps at the one level and does not keep here.

**Same species as boards 7 and 114, one context along.**  `neg_double_3level_M`
(`1$M - 3$x - ?`) gives `nx3_negx` `suits: { $oM: [4, 13] }` — an open-ended
four-or-more — where `nx_1m1H_X` uses `suits: { S: [4, 4] }` and hands the
five-card case to `nx_1m1H_1S`.  Three of my thirty-eight boards are lost to that
one omission across the three negative-double contexts.

```yaml
  # context: neg_double_3level_M   (expand_pairs over M and x); before `- id: nx3_raise`
      - id: nx3_major_3
        call: 3$oM
        priority: 71
        when: { unbid_suit: $oM, cheapest_in_suit: true }
        requires: { suits: { $oM: [5, 13] }, hcp: [8, 40], not: { suits: { $M: [3, 13] } } }
        shows: "five or more $oM over their three-level overcall: I bid my suit; the double promises exactly four"
        establishes: { forcing: non_forcing }
```

The `not: { suits: { $M: [3, 13] } }` clause is copied verbatim from `nx3_negx`
so the rung can never be preferred to a raise of partner's own major — a
three-card fit for opener still takes priority, exactly as it does today.

**THE ANSWERING SEAT.**  `non_forcing`; opener's seat over
`1$M - 3$x - 3$oM - act` is `general_competitive_high`, which has `ch_raise_S3/S4`,
`ch_raise_lott4_S`, `ch_new_*` and `ch_pass`.  I chose `non_forcing` over
`one_round` deliberately: the ledger's most expensive recurring object is a
forcing call with no seat that answers it, and 3S here is a contract proposal,
not a question.

**WHAT IT ENDANGERS:**

* `nx3_negx` @70 — on hands with a five-card unbid major only.  Verified: with
  exactly four spades (`KQT4.Q2.AQ942.Q5`) the double still wins at fit 1.000 and
  the new rung falls to 0.349.
* `ch_free_3S` @30, `ch_new_S3(_hi)` @27/27.5, `ch_new_long3_S(_hi)` @27/27.5 —
  same call from the less specific context; they become covered.  My gate
  (5+ spades, 8+ HCP) is a superset of `ch_new_S3`'s (5+, 14+ points) and of
  `ch_free_3S`'s (5+ good, 10+), so the ladder can only widen.
* `nx3_raise` @?, `nx3_3NT` @60, `nx3_cue` @71, `nx3_game_raise` @69 — the cue and
  the game raise stay above; only the shapeless double moves.
* `nx3_pass` @20 — unaffected.

**VERIFIED.**  Base: `X nx3_negx fit=1.000 prio=70`.  Patched:
`3S nx3_major_3 fit=1.000 prio=71` chosen — BEN's call at 0.85.

**TEMPLATE.**  One rule over the five `(M, x)` pairs the context already expands.
`$oM` resolves to the other major automatically; `unbid_suit` +
`cheapest_in_suit` make it self-selecting (over `1S - 3H` the hearts are theirs,
so nothing fires).  Ship with the boards 7 and 114 rungs as **one batch** —
they are three faces of the same agreement and the ledger's verdict on `nxj_X`
is that its landing seats must be authored before its gate is touched again.

---

## Board 455 — W, call 12 (table B): `P` should be `4D` — and it is board 306's rung

**Seat/call that went wrong.**  Table B, W, `P P 1D 1S X P 2D 2S 3D 3S P P — ?`
with `542.A9873.KQ72.4` (9 HCP, **four-card support for the diamond suit I have
already raised to three**, a singleton club).  `balhigh_pass` sold out to 3S; E/W
make ten tricks in diamonds and 3S by S makes nine, so passing hands back 140 that
4D would have taken.

**The missing agreement — identical to board 306, and this is the point.** In the
passout seat, with a nine-card fit in the minor I have already agreed and an
opposing fit shown, the Law says bid four of it.

**No new YAML.**  The rung proposed on board 306 fixes this board unchanged:

```yaml
  # context: general_balancing_high
      - id: balhigh_raise_lott4_D
        call: 4D
        priority: 32
        when: { partner_suit: D, is_competitive: true, i_have_acted: true }
        requires:
          suits: { D: [4, 13] }
          evals: { "lott_total_trumps(D)": [9, 26], total_points: [8, 40], their_fit: [8, 26] }
        shows: "the Law at the four level in our agreed minor: nine-plus trumps our way and they have a fit too"
        establishes: { forcing: non_forcing, agreed_suit: D }
```

**VERIFIED — on this board, with the board-306 patch and no change to it.**
Base: `P balhigh_pass fit=1.000`, with `balhigh_raise_D4` at **0.066** (blocked by
the same `suit_diff` "the minor must be my longest suit" gate, even though W's
longest suit is hearts and diamonds are the agreed trumps).  Patched:
`4D balhigh_raise_lott4_D fit=1.000 prio=32` chosen — BEN's call at 0.81.

**Why this matters more than a second proposal would.**  Two independent boards in
one 38-board slice, in two different contexts, are lost to the same clause:
`ch_raise_C4`/`balhigh_raise_C4`/`cl_raise_C4` all require the minor to be my
longest suit *and* ten combined trumps *and* `rule_of_26 >= 25`, three
simultaneous thresholds on the one call that has to be available when the auction
gets high.  Boards 306, 357, 388 and 455 are four faces of it.  **If the merge
ships one thing from my slice, ship the minor-suit Law family.**

**WHAT IT ENDANGERS.**  As board 306; and on this board specifically it outranks
`balhigh_new_H4` @28 (fit 0.310 — bidding my own ragged five-card heart suit at
the four level instead of the agreed diamond fit) and `balhigh_pass` @21.

**The dossier's own first divergence** on this board is table B call 2, where E
opens 1D on `KT.J.AJT983.J975` (10 HCP, six diamonds, third seat) and BEN opens
3D: `open_1D_rule20_third` and `open_weak_2D_nv` **both fit 1.000** and the light
opening wins on priority 72 against 64.  That is an opening-style threshold and is
scope-excluded — but I note the shape of it, because "a light third-seat opening
outranks the disciplined weak two on the identical hand" is a priority ordering,
not a threshold, and might be re-examinable under a different heading.

**TEMPLATE.**  As board 306.

---

## Board 503 — S, call 7 (table A): `3D` should be `2S`

**Seat/call that went wrong.**  Table A, S, `1C 1H P 1S P 2D P — ?` with
`KQT873..JT6.T852` (6 HCP, **six spades K-Q-T-8-7-3, a void in their clubs**,
three small in partner's second suit).  `uc_raise_D3` raised diamonds; N then
drove to 5D on a 5-3 fit for -200, where 3D is the limit (+110 at the other table).

**The missing agreement.** Going back to my own six-card suit at the cheapest
level is a preference, not a promise of values — it needs a suit, not points.

**Why the rung cannot fire.**  `uc_rebid_S2` requires
`evals: { total_points: [11, 40] }`.  S has 6 HCP plus three for the void — nine
— so the rebid of a K-Q-T sixth fits **0.134** and the three-card raise of
partner's second suit, at a lower priority but a full fit, wins.  Every
`*_rebid_*2` rung in the file carries the same 11-point floor, which is the floor
for a rebid that *shows extras*; the cheapest repeat of a six-card suit shows none.

```yaml
  # context: general_uncontested_continuation   (insert before `- id: uc_rebid_S3`)
      - id: uc_rebid_S2_pref
        call: 2S
        priority: 29.5
        when: { my_suit: S, cheapest_in_suit: true }
        requires:
          suits: { S: [6, 13] }
          evals: { total_points: [6, 10], "suit_quality(S)": [1, 9] }
        shows: "back to my own six-card S: a preference, not a promise of values"
        establishes: { forcing: non_forcing }
      - id: uc_rebid_H2_pref
        call: 2H
        priority: 29.5
        when: { my_suit: H, cheapest_in_suit: true }
        requires:
          suits: { H: [6, 13] }
          evals: { total_points: [6, 10], "suit_quality(H)": [1, 9] }
        shows: "back to my own six-card H: a preference, not a promise of values"
        establishes: { forcing: non_forcing }
```

The two bands are deliberately disjoint (`[6, 10]` here, `[11, 40]` on
`uc_rebid_S2`), so this is a strict extension downward and never a competitor on
the hands the existing rung describes.

**THE ANSWERING SEAT.**  `non_forcing` and it explicitly does NOT set
`agreed_suit`, so partner is free to pass or correct; his seat
(`general_uncontested_continuation` / `general_competitive_low`) already has the
preference, raise and pass rungs.  The point of the rung is to STOP a
conversation — N's 5D — not to start one.

**WHAT IT ENDANGERS:**

* `uc_raise_D3` @27 (fit 1.000 here) and `uc_raise_D4` @27, `uc_minor_game_5D`
  @28 — raising partner's second suit with three small when I hold a six-card
  major is the error, and it is what let the auction reach five of a minor.
* `uc_nt2` @28 — a hand with a void is not a notrump hand.
* `uc_new_*2` @26-26.5 — introducing a third suit is worse than repeating a
  six-card one.
* `uc_rebid_S2` @29 — same call, disjoint band; both stay.
* Rungs it does NOT outrank: `uc_raise_*3/4` at 31-32 (a real fit still gets
  raised), `uc_nt3` @29 is equal-and-below at 29 so a genuine 3NT hand is
  unaffected in practice (it cannot co-fit a 6-0-3-4).
* Fallback: 2S already covered by `uc_rebid_S2`; nothing deleted.

**VERIFIED.**  Base: `3D uc_raise_D3 fit=1.000 prio=27`.  Patched:
`2S uc_rebid_S2_pref fit=1.000 prio=29.5` chosen — BEN's call at 0.83.
Regression: a four-card spade suit in the same seat still passes, the rung falling
to fit 0.015 on the sharp length gate.

**TEMPLATE.**  Four rules, one per suit, in `general_uncontested_continuation`,
and the same four in `general_competitive_low` (`cl_rebid_*2_pref`) and
`general_balancing_low`.  The three-level versions should NOT get the same
treatment: repeating a six-card suit one level higher does need values.

**Note on the dossier's first divergence, which I am not proposing.**  Table A
call 1: N overcalls 1H on `65.A8632.AKQ52.4` (5-5 in hearts and diamonds) where
BEN bids 2NT.  2NT there is the unusual notrump, which is scope-excluded — and
worth noting, the natural overcall the engine chose is the **higher** of the two
five-card suits, which is what board 15's proposal asks the engine to do
everywhere.  On this board the tie happened to break the right way.

---

## Board 528 — S, call 10 (table A): `P` should be `3S`

**Seat/call that went wrong.**  Table A, S, `1C P 1S X 2S P P X P 3H — ?` with
`Q642.742.K52.KJ7` (9 HCP, **four spades opposite partner's support raise**).
`ch_pass` sold out to 3H, which made nine tricks for -140; 2S/3S by S takes nine
tricks and the other table scored +140.

**The missing agreement.** When partner has raised my suit and they bid three of
theirs, the Law says compete to three of ours — nine trumps, and the count of my
high cards is not what decides it.

**This is a documented open item, repaired at rung level.**  `DECISIONS.md`:
"**After partner RAISES my own suit every generic raise rung is dead**: the sharp
`lott_total_trumps >= 8` gate counts partner's SHOWN minimum, so a simple raise
(3) plus my own bid suit (4) counts 7 and both the invitational and game rungs
score ~0.08."  Here `ch_raise_S3` reaches 0.800 — better than 0.08 but still
under the 0.9 fast path, so a fit-1.000 pass takes the seat.  Rather than change
the evaluator (which reaches everything), the rung below sets its own trump bar at
**seven**, which is what the evaluator actually reports in this position, and adds
`my_suit` + `partner_suit` so it can only ever fire on a suit we have both bid.

```yaml
  # context: general_competitive_high   (insert before `- id: ch_raise_S2`)
      - id: ch_compete_S3_after_raise
        call: 3S
        priority: 31.5
        when: { my_suit: S, partner_suit: S, is_competitive: true, cheapest_in_suit: true }
        requires:
          suits: { S: [4, 13] }
          evals: { total_points: [7, 12], "lott_total_trumps(S)": [7, 26] }
        shows: "they have outbid our agreed fit: with four trumps opposite partner's raise the Law says compete to three"
        establishes: { forcing: non_forcing, agreed_suit: S }
      - id: ch_compete_H3_after_raise
        call: 3H
        priority: 31.5
        when: { my_suit: H, partner_suit: H, is_competitive: true, cheapest_in_suit: true }
        requires:
          suits: { H: [4, 13] }
          evals: { total_points: [7, 12], "lott_total_trumps(H)": [7, 26] }
        shows: "they have outbid our agreed fit: with four trumps opposite partner's raise the Law says compete to three"
        establishes: { forcing: non_forcing, agreed_suit: H }
```

`my_suit: S` **and** `partner_suit: S` together are the safety catch: the rung is
unreachable unless the suit is one I bid and one partner has supported, which is
exactly the population the ledger says is dead.

**THE ANSWERING SEAT.**  `non_forcing` + `agreed_suit`; partner's seat is
`general_balancing_high`/`general_competitive_high` and this is a competitive
statement, not an invitation — the `total_points: [7, 12]` ceiling is what stops
partner reading it as a game try.

**WHAT IT ENDANGERS:**

* `ch_pass` @22 — the error: passing 3H with a known nine-card spade fit.
* `ch_raise_S3` @31 — same call, and this is the branch its own gates cannot
  reach; both stay, and above 12 points the existing rung is the one that fits.
* `ch_nt3` @29, `ch_rebid_S3` @29 — worse descriptions.
* Rungs it does NOT outrank: `ch_raise_S4` @32, `ch_raise_lott_S4` @32,
  `ch_raise_lott4_S` @32 — a TEN-trump hand still bids four; `ch_penalty_X` @38.
* Verified at the four level: with the same hand over `4H` instead of `3H` the
  engine still passes, because 3S is not legal and the four-level rungs keep
  their own (higher) bar.
* Fallback: 3S already covered by `ch_raise_S3`/`ch_rebid_S3`; nothing deleted.

**VERIFIED.**  Base: `P ch_pass fit=1.000` (`ch_raise_S3` 0.800).  Patched:
`3S ch_compete_S3_after_raise fit=1.000 prio=31.5` chosen — BEN's call at 0.64.

**TEMPLATE.**  Two rules; twins in `general_balancing_high` and, at the two level,
in `general_competitive_low`.  The minors want a four-level version, which is the
board-357/388 family.

---

## Board 538 — E, call 3 (table B): `P` should be `3S`

**Seat/call that went wrong.**  Table B, E, `P P 3C — ?` with `J7542.K52.KQ2.A4`
(13 HCP, **five spades, two and a half quick tricks, a doubleton in their suit**)
over their three-level club preempt.  `v3_C_pass`.  We defended 3C, which made ten
tricks for -130; 3S by E is one off for -50.

**The missing agreement.** Over a three-level preempt, a five-card major with
opening values and two quick tricks is bid — the direct seat is the only chance
the hand will get, and passing with 13 points and a suit is what the preempt was
aimed at.

**The hole, exactly.**  `defense_vs_preempt_C` has `v3_C_X` (14-17 with at most
three clubs, or any 18+) and `v3_C_S` (a **six**-card suit, 11+ with a good suit
and two quick tricks).  A thirteen-count with **five** spades fits the double
0.800 and the overcall 0.115 — both under the fast path — so a `requires: {}`-ish
pass at priority 30 and fit 1.000 takes the seat.  The ladder has a one-point gap
between the double's floor and nothing.

```yaml
  # context: defense_vs_preempt_C   (insert before `- id: v3_C_pass`)
      - id: v3_C_S5
        call: 3S
        priority: 63.5
        requires:
          suits: { S: [5, 13], C: [0, 3] }
          hcp: [12, 17]
          evals: { quick_tricks: [2, 12] }
        shows: "overcalling the preempt in a five-card major: opening values and two quick tricks"
        establishes: { forcing: non_forcing }
      - id: v3_C_H5
        call: 3H
        priority: 63.5
        requires:
          suits: { H: [5, 13], C: [0, 3] }
          hcp: [12, 17]
          evals: { quick_tricks: [2, 12] }
        shows: "overcalling the preempt in a five-card major: opening values and two quick tricks"
        establishes: { forcing: non_forcing }
```

Note there is deliberately **no suit-quality gate**.  I prototyped one
(`"suit_quality(S)": [1, 9]`) first and it did **not** fix the board: J-7-5-4-2
scores below the bar and the rung stalls at fit 0.757, under the 0.9 fast path,
leaving the pass in place.  That is a negative result worth recording — over a
preempt the question is "do I have five of them and the values", not "is the suit
pretty"; the quick-trick gate is the honest safety catch and it is registered
sharp (0.9) so it really gates.

**THE ANSWERING SEAT.**  `non_forcing`; the advance is `advance_weak_jump_overcall`
(`1$o - 3$j - P - ?`) and the general competitive contexts.  Since the rung is
capped at 17 HCP it never creates a hand partner must answer.

**WHAT IT ENDANGERS:**

* `v3_C_pass` @30 — the seat it fills.
* `v3_C_S` @64 / `v3_C_H` @64 — six-card versions, still above and still primary.
* `v3_C_4S`/`v3_C_4H` @65, `v3_C_3NT` @66, `v3_C_X` @70 — all above; verified with
  a 17-count (`AKJ72.K52.KQ2.A4`) that the takeout double still wins.
* Fallback: 3S/3H already covered by `v3_C_S`/`v3_C_H`; nothing deleted.

**VERIFIED.**  Base: `P v3_C_pass fit=1.000`.  Patched: `3S v3_C_S5 fit=1.000
prio=63.5` chosen — BEN's call at 0.66.  Regressions: 10 HCP → still pass (fit
0.310); four spades → still pass (0.349); the same shape with only 1.5 quick
tricks → still pass (0.409).

**TEMPLATE.**  Two rules in each of `defense_vs_preempt_C/D/H/S` — eight in all,
minus the pairs where the major IS their suit.  The minors do not want it (four
of a minor over their three-level preempt is a different, worse bet).

**Note on the dossier's first divergence.**  Table B call 1: W passes
`KT3.QJT743.65.73` (6 HCP, six hearts Q-J-T) in second seat, vulnerable, where BEN
opens 2H.  `open_weak_2H_vul` fits 0.800 — a one-point miss on the deliberate
"vulnerable tightens to 7-10 with two of the top three" system decision recorded
in `DECISIONS.md`.  The suit is three of the top five and not two of the top
three, so it fails the design on both counts; I am not proposing to loosen a
documented vulnerability discipline on one board.

---

## Board 587 — S, call 3 (table A): `P` should be `3NT`

**Seat/call that went wrong.**  Table A, S, `P 3C P — ?` with `AKJ8.632.A864.AJ`
(**17 HCP, four quick tricks, the A-J of partner's preempt suit**).
`rp3_C_pass` — "no game opposite a preempt" — at priority 40 and fit 1.000.  We
played 3C for +150; 3NT takes **ten tricks** and the other table scored +430.

**The missing agreement.** Opposite a seven-card preempt you count tricks, not
stoppers: with the ace-jack of partner's suit the suit runs, and four quick tricks
outside plus seven club tricks is nine before the opponents get in.

**Why the existing rung refuses.**  `rp3_C_game` demands
`weakest_unshown_stopper: [0.9, 9]` — a stopper in **every** unbid suit — and the
comment above it explains why: a 3NT that goes down six.  That gate is right for
a hand that is merely strong; it is wrong for a hand whose values ARE the source
of tricks.  S holds `632` of hearts, so the sharp gate fails hard and the rung
fits 0.067.  There is no rung between "stopped everywhere" and "no game", so the
seat is a pass by construction.

```yaml
  # context: resp_preempt_C   (insert before `- id: rp3_C_pass`)
      - id: rp3_C_game_source
        call: 3NT
        priority: 61.5
        requires:
          evals: { total_points: [16, 40], quick_tricks: [4, 12] }
          features: [ "top_honour(C)" ]
        shows: "3NT opposite the preempt: my honour makes partner's suit run and I can count the outside tricks"
        establishes: { forcing: sign_off }
```

The two gates are the whole agreement: `top_honour(C)` is what makes seven club
tricks real (partner has shown 4-9 HCP and a good seven-card suit, so my honour is
the entry-and-solidity card), and `quick_tricks >= 4` is the counting claim —
four immediate winners plus seven in the suit is eleven, and nine is the contract.
`quick_tricks` is registered sharp (0.9), so three-and-a-half really fails.

**THE ANSWERING SEAT.**  `forcing: sign_off` — this is a contract, and partner's
seat (`preemptor_discipline`, `general_uncontested_continuation`) already treats a
sign-off as final via `partner_signed_off`.  No question, nothing owed.

**WHAT IT ENDANGERS — and note the priority is BELOW the forcing new suits, not
above:**

* `rp3_C_pass` @40 — the seat it fills; a 16+ hand with a fitting honour is not
  "no game opposite a preempt".
* `rp3_C_game` @64 — same call, higher, untouched: a hand stopped everywhere still
  reaches 3NT through the existing rung.
* `rp3_C_D`/`rp3_C_H`/`rp3_C_S` @62 — **deliberately left above this rung.**  With
  a five-card side suit and 15+ the forcing new suit is the better exploration,
  and putting 3NT above them would have deleted it.  This is the mistake round 14
  made with `uc_nt_raise3` and I priced against the rungs below AND above.
* `rp3_C_rkc` @66 — the keycard ask (19+ and four keycards) is unaffected.
* `uc_raise_C4` @27, `uc_minor_game_5C` @28 — below, and both fit 0.000 here.
* Fallback: 3NT already covered by `rp3_C_game`; nothing deleted.

**VERIFIED.**  Base: `P rp3_C_pass fit=1.000 prio=40`.  Patched:
`3NT rp3_C_game_source fit=1.000 prio=61.5` chosen — BEN's call, at only 0.40
confidence, but the cards are unambiguous (+430 versus +150).  Regressions: the
same hand with `32` of clubs instead of `AJ` still passes (no top honour, hard
feature miss); a 16-count with only two and a half quick tricks
(`KQJ8.632.KQ64.QJ`) still passes.

**TEMPLATE.**  One rule in each of `resp_preempt_C/D/H/S` — four rules.  The
major-suit versions should use `4$W` rather than 3NT as the companion call and
are a separate proposal; the ledger's rule about authoring the whole conversation
applies, and the 3NT branch is the one that stands alone.

---
