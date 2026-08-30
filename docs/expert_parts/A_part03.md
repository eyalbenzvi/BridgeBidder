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
