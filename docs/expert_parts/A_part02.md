# Expert A (competitive / matchpoint duplicate) — dossier part 2

38 boards, -389 IMPs.  One agreement per board, in dossier order.
Everything labelled **VERIFIED** was traced through a patched *copy* of
`two_over_one.yaml` in the scratchpad (`fast_decision` + `score_candidates`);
the repo file is untouched.

*(summary written at the end of the pass — see "Summary" below)*

---

## Board 487 — margin -11

**Seat/call that went wrong:** table A, call 3, **South passes 4H** holding
`AJT8543.T.K83.K2` after `2H – P – 4H`.  (Call 1, North's pass of 2H, is the
dossier's first divergence; I treat it as secondary — see the note at the end.)

**Missing agreement:** over an opponent's weak two raised straight to game,
a hand with a self-sufficient seven-card suit bids game in its own suit — the
raised-preempt context contains a takeout double and *nothing else*.

`context_at` at that seat returns exactly two candidates: `ch_pass` (fit 1.000)
and `drw4_X_H` (fit 0.102).  There is no natural call in the file for
`2W – P – 4W – ?`.  This is a textbook starved seat.

### YAML — into the EXISTING context `double_raised_weak_two` (`2$W - P - 4$W - ?`)

```yaml
      - id: drw4_own_S_$W
        call: 4S
        priority: 62
        when: { unbid_suit: S, cheapest_in_suit: true }
        requires:
          suits: { S: [7, 13] }
          evals: { total_points: [11, 40], "suit_quality(S)": [1.5, 9], ltc: [0, 7] }
        shows: "self-sufficient seven-card spade suit: bid game in my own suit"
        establishes: { forcing: non_forcing }
      - id: drw4_own_H_$W
        call: 4H
        priority: 62
        when: { unbid_suit: H, cheapest_in_suit: true }
        requires:
          suits: { H: [7, 13] }
          evals: { total_points: [11, 40], "suit_quality(H)": [1.5, 9], ltc: [0, 7] }
        shows: "self-sufficient seven-card heart suit: bid game in my own suit"
        establishes: { forcing: non_forcing }
      - id: drw4_own_H5_$W
        call: 5H
        priority: 61
        when: { unbid_suit: H, cheapest_in_suit: true }
        requires:
          suits: { H: [8, 13] }
          evals: { total_points: [12, 40], "suit_quality(H)": [1.5, 9], ltc: [0, 5] }
        shows: "eight-card heart suit over their raised preempt: five level on shape"
        establishes: { forcing: non_forcing }
      - id: drw4_own_C_$W
        call: 5C
        priority: 61
        when: { unbid_suit: C, cheapest_in_suit: true }
        requires:
          suits: { C: [8, 13] }
          evals: { total_points: [12, 40], "suit_quality(C)": [1.5, 9], ltc: [0, 5] }
        shows: "eight-card club suit over their raised preempt: five level on shape"
        establishes: { forcing: non_forcing }
      - id: drw4_own_D_$W
        call: 5D
        priority: 61
        when: { unbid_suit: D, cheapest_in_suit: true }
        requires:
          suits: { D: [8, 13] }
          evals: { total_points: [12, 40], "suit_quality(D)": [1.5, 9], ltc: [0, 5] }
        shows: "eight-card diamond suit over their raised preempt: five level on shape"
        establishes: { forcing: non_forcing }
```

The same five rungs belong verbatim in `double_raised_weak_two_3`
(`2$W - 3$W - ?`) at one level lower (`3S`/`3H`/`4C`/`4D`), where the seat is
equally empty.

**Answering seat:** none needed — every rung is `non_forcing` and names the
final contract.  That is deliberate: `advance_double_of_raised_weak_two` only
answers the DOUBLE, and round 17's lesson says do not open a conversation
whose answer does not exist.  These rungs close one instead.

**What it endangers, in `double_raised_weak_two`:**
* `drw4_X_$W` (X, prio 60) — a takeout double asks partner to pick a suit;
  with seven of my own there is nothing to pick.  This is the same sentence
  the file already writes on `vw2_X` ("with a six-card suit of my own there is
  nothing to pick, so overcall it instead"), so the ladder stays coherent.
* `ch_pass` (prio 22, `general_competitive_high`) — passing a raised preempt
  with a seven-card suit and opening values converts a game into a defence of
  their partscore-plus.
* **Fallback hazard: real but narrow.**  4S/4H/5C/5D are NOT currently covered
  in this context, so these rungs delete the code fallback for those calls in
  every `2W – P – 4W – ?` seat.  The `when: {unbid_suit, cheapest_in_suit}`
  gates and the 7/8-card floors mean the rungs fit almost nothing else, so the
  suppression bites on hands that would previously have been given a fallback
  4S — i.e. exactly the hands this rung is for.  Worth screening on its own.

**VERIFIED.**  With `drw4_own_S_$W` inserted, South bids `4S` at fit 1.000,
prio 62 (`ch_pass` 1.000/22, `drw4_X_H` 0.102/60).  4S by South makes 10 tricks
on the double-dummy table — +620 instead of +50.

**Template:** the context already carries `expand: { W: [D, H, S] }`, so each
rung above is written once and becomes three.  Illegal combinations
(4S when $W = S) are dropped by the legality filter, and `cheapest_in_suit`
keeps 5H off the `2D`/`2H` auctions.

**Secondary note (North, call 1).**  `vw2_X` demands 13 HCP; North holds 12 HCP
/ 13 total points, 2=2=4=5, and fits it 0.800 — a one-point soft miss that the
fit-1.00 `vw2_pass` beats.  A shapely light branch,

```yaml
      - id: vw2_X_shapely
        call: X
        priority: 63
        requires:
          suits: { $W: [0, 2] }
          evals: { total_points: [13, 16], longest_suit_length: [0, 5],
                   quick_tricks: [2, 12] }
        shows: "takeout double of the weak two on distributional opening values"
        establishes: { forcing: one_round }
```

also makes North double (**VERIFIED**, fit 1.000).  It must sit at **63**, i.e.
BELOW `vw2H_over_2S` / `vw2_over3_$X` (64), not above them: at 68 it outranks
the natural overcalls and a 13-count with a good five-card spade suit doubles
2H instead of bidding 2S.  I prefer the South-seat rung as this board's
proposal because it is a starved seat rather than a threshold.

---

## Board 532 — margin -11

**Seat/call that went wrong:** table B, call 3, **West passes 1S** holding
`AQT632.A9753.K9.` (6=5=2=0, 13 HCP, 16 total points, LTC 4) after `P – P – 1S`.

**Missing agreement:** a two-level overcall may be made on a ragged five-card
suit when the hand is 6-5 (or 5-5) with opening values — length and losers, not
honours, justify the two level.

`oc1S_2H` demands `suit_quality(H) >= 1.5`; A9753 scores **1.0**, so the rule
fits 0.757 and `oc1S_pass` at fit 1.000 wins.  East holds `KQJ82` of hearts:
2H finds a ten-card fit worth twelve double-dummy tricks.

### YAML — into the EXISTING context `overcalls_of_1S`

```yaml
      - id: oc1S_2H_shape
        call: 2H
        priority: 63
        requires:
          suits: { H: [5, 13] }
          hcp: [11, 17]
          evals: { total_points: [13, 40], ltc: [0, 6] }
        shows: "2-level overcall on shape: 5+ hearts, 13+ total points, six losers or fewer"
        establishes: { forcing: non_forcing }
```

**Answering seat:** none — `non_forcing`, and the advance ladder for a simple
overcall (`cl_raise_*`, `ch_raise_*`, `advance_*`) already exists and reads a
2H overcall the same way whichever rung produced it.  Note the `shows` floor
matters: same-call rules merge into a disjunction for the partner model, so
the 11 HCP / 13 total-point floor keeps partner's shown minimum for 2H intact.

**What it endangers, in `overcalls_of_1S`:**
* `oc1S_2H` (2H, 65) — same call, higher priority, so it still wins whenever
  the suit is good; mine only picks up the ragged ones.
* `oc1S_2C` / `oc1S_2D` (65) — a hand with a good minor still overcalls the
  minor on priority; mine only outranks them when their own quality gate fails,
  and then the major is the right suit anyway.
* `oc1S_3H_jump` (59) / `oc1S_3H_preempt` (58) — those describe 5-10 HCP; my
  13-point floor cannot reach them.
* `oc1S_pass` (25) — passing with 6-5 and opening values sells out the hand.
* **No fallback hazard:** 2H is already `covered` in this context by
  `oc1S_2H`, so `generate_fallbacks` behaviour is unchanged.  This is the
  cheapest possible shape of new rung and I use it wherever I can below.

**VERIFIED.**  West bids `2H` at fit 1.000 / prio 63 (`oc1S_pass` 1.000/25,
`oc1S_2H` 0.757/65).

**Template:** the four overcall contexts (`overcalls_of_1C/1D/1H/1S`) are
written longhand, with no `expand:`, and a NEW context cannot supply this rung
— a call already `covered` by an earlier context is dropped, so a sibling
context defining 2H would never be reached.  Either (a) hand-write the rung in
all four contexts for each of the three non-opened suits (12 rungs), or
(b) refactor the four contexts into one with
`expand_pairs: [{O: C, X: D}, {O: C, X: H}, … ]` — 12 pairs — which is the
better long-term shape and is how `defense_vs_weak2_overcalls3` is already
written.

---

## Board 751 — margin -11 — NOTHING-WRONG (on the competitive axis)

**What I checked.**  Both auctions are uncontested from our side: at table A we
pass throughout with `754.Q73.T974.963` (2 HCP) and `632.J9852..AQT54` (7 HCP,
both vulnerable); at table B we hold both hands of an uncontested 1C opening.
The dossier's first divergence — East responding `1S` on `AQJ9.AK6.AJ8532.`
(4=3=6=0, 19 HCP) where 1D/2D is right — is a **constructive** defect in
`resp_1m`, outside my brief.

The one competitive observation available: at table A, call 3, South is in the
**sandwich seat** (`1C – P – 1D – ?`) with 5-5 in hearts and clubs and a
diamond void, and `sw_pass` is chosen at fit 1.000.  Both vulnerable with 7
HCP, passing is right, and BEN passes too (0.92).  The file has no two-suited
sandwich action at all, but Michaels / unusual notrump are explicitly
scope-excluded, so I make no proposal here.

**VERIFIED** only in the sense that I re-ran the seat; no rung proposed.

---

## Board 837 — margin -11

**Seat/call that went wrong:** table A, call 3, **North passes 3D** holding
`J9763.KJT864..J2` (5=6=0=2, 6 HCP) after `1D – 1NT – 3D`.

**Missing agreement:** over their preemptive raise, a six-card major with a
void in the suit they have jumped in is worth game opposite a partner who has
shown 15+ — bid 4H, do not pass.

`ch_free_3H` demands 10+ total points; North has 9, fits 0.800, and loses to
`ch_pass` at 1.000.  Even at 3H the hand is underbid: partner's 1NT overcall is
15-18 and North's void is the whole hand.  4H makes **twelve** tricks.

### YAML — into the EXISTING context `general_competitive_high`

```yaml
      - id: ch_shape_game_H
        call: 4H
        priority: 30.5
        when: { unbid_suit: H, side_has_acted: true, i_have_acted: false }
        requires:
          suits: { H: [6, 13] }
          evals: { "standing_suit_length": [0, 1], "suit_quality(H)": [1.5, 9],
                   "lott_total_trumps(H)": [8, 26], rule_of_26: [22, 99] }
        shows: "six-card major with a void or singleton in the suit they have jumped in: game on shape"
        establishes: { forcing: non_forcing, agreed_suit: H }
      - id: ch_shape_game_S
        call: 4S
        priority: 30.5
        when: { unbid_suit: S, side_has_acted: true, i_have_acted: false }
        requires:
          suits: { S: [6, 13] }
          evals: { "standing_suit_length": [0, 1], "suit_quality(S)": [1.5, 9],
                   "lott_total_trumps(S)": [8, 26], rule_of_26: [22, 99] }
        shows: "six-card major with a void or singleton in the suit they have jumped in: game on shape"
        establishes: { forcing: non_forcing, agreed_suit: S }
```

`standing_suit_length` is the right evaluator here and `suit_length(their)`
is not: `_their_suits` seeds LHO-before-RHO, so on this auction it would
resolve to the wrong opponent's suit.  It also carries sharp tolerance
(`_S2_SUIT`), so the void/singleton gate really gates.

**Answering seat:** none — `non_forcing` and it names game.  `establishes:
agreed_suit` is what keeps the pair out of a suitless game force if they double
us.

**What it endangers, in `general_competitive_high`:**
* `ch_free_3H` (3H, 30) — with six of a major and a void in the suit they
  jumped in, three of the major is an invitation partner will pass.
* `ch_neg_major_H4` (4H, 30) — same call, so no behaviour changes; only the
  `shows` sentence differs, and mine is the more specific description.
* `ch_new_H4` / `ch_new_H4_hi` (4H, 28 / 28.5) — same call again.
* `ch_rebid_H4` (4H, 29) — gated `my_suit: H`, mine `unbid_suit: H`; disjoint.
* `ch_negative_X3` (33) and `ch_penalty_X` (38) stay ABOVE it, deliberately: a
  10+ HCP three-suited hand still doubles, and a trump stack still defends.
* `ch_pass` (22).
* **No fallback hazard:** 4H and 4S are already covered in this context by
  `ch_new_H4` / `ch_new_S4`.

**VERIFIED.**  North bids `4H`, fit 1.000, prio 30.5, `clear=True`
(`ch_pass` 1.000/22, `ch_free_3H` 0.800/30).

**Template:** written as the explicit `_H` / `_S` pair above, matching the
file's own idiom in this context (`ch_free_3H` / `ch_free_3S`,
`ch_raise_lott4_H` / `_S`).  The same pair belongs in
`general_balancing_high`, where the identical hand in the passout seat has the
same problem.

---
