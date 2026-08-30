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

## Board 856 — margin -11

**Seat/call that went wrong:** table A, call 4, **North passes 3H** holding
`AKQ9.QT.T6.A9832` (15 HCP, 3 quick tricks, doubleton heart) after
`1C – P – 1D – 3H`.  (The dossier's first divergence is the OPENING call,
1C vs 1NT — opening style is scope-excluded.)

**Missing agreement:** the opener's SECOND double — after I have opened and
they jump-overcall, a double with opening values, shortness in their suit and a
four-card major is takeout, and the file has no such rule anywhere.

`ch_negative_X3` carries `i_have_acted: false`, so it is switched off for the
opener by construction; `ch_penalty_X` demands `standing_suit_length >= 3` and
North has two.  North's whole candidate set is `ch_pass` 1.000, `ch_nt3` 0.772,
`ch_penalty_X` 0.349 — a starved seat.  This is the "no opener's reopening /
second double" open item in `DECISIONS.md`, which that entry says "wants its
own round"; it is not on the do-not-re-propose list.

### YAML — into the EXISTING context `general_competitive_high`

```yaml
      - id: ch_takeout_X_acted
        call: X
        priority: 34
        when: { their_last_bid_suit: true, i_have_acted: true, side_has_acted: true }
        requires:
          hcp: [13, 40]
          evals: { "standing_suit_length": [0, 2], quick_tricks: [2, 12],
                   longest_suit_length: [0, 6] }
          any_of:
            - suits: { S: [4, 13] }
            - suits: { H: [4, 13] }
        shows: "opener's second double: extra values, short in their suit, a four-card major to offer"
        establishes: { forcing: one_round }
```

The same rung belongs in `general_competitive_low` (`cl_takeout_X_acted`, at
34, above `cl_negative_X2`'s 33) for the two-level case.

**Answering seat: it already exists and is fully populated.**
`general_pull_or_sit` (`... - X - P - ?`) answers any double of theirs that
stands: `adx_sit` (trump stack, 61), `adx_neg_major_H2/H3/S2/S3` (62),
`adx_pull_my_*` (58.5-60), `adx_nt` (56), `adx_pass_min` (52).  Nothing new is
needed, which is exactly the round-17 test this proposal has to pass.

**What it endangers, in `general_competitive_high`:**
* `ch_penalty_X` (X, 38) — stays above, and the two are disjoint on shape:
  mine needs 0-2 in their suit, the penalty double 3+, and
  `standing_suit_length` carries sharp `_S2_SUIT` tolerance, so the split is
  real rather than soft.
* `ch_negative_X3` (X, 33) — disjoint by `i_have_acted`.
* `ch_nt3` (3NT, 29) — with a doubleton in their suit and no stopper, three
  notrump on a guess is the worse description; the double lets partner choose.
* `ch_new_S3` / `_hi` (27 / 27.5) and `ch_rebid_C4` (29) — bidding my
  four-card spade suit at the three level unilaterally commits to a 4-3 fit
  when partner has bid neither major; the double offers both.
* `ch_pass` (22).
* **No fallback hazard:** X is already covered here by `ch_penalty_X`.

**VERIFIED.**  North doubles at fit 1.000, prio 34, `clear=True`
(`ch_pass` 1.000/22, `ch_penalty_X` 0.349/38).

**Template:** no `expand` in this context; write the rung once here and once in
`general_competitive_low`.  The `any_of` covers both majors, so no per-suit
expansion is needed.  Do NOT template it into `general_balancing_*`: there the
double already has a balancing reading and a third meaning really would collide.

---

## Board 866 — margin -11 — NOTHING-WRONG (on the competitive axis)

**What I checked.**  Both auctions are wholly uncontested: E/W hold 6 and 2 HCP
and never have a call, and every one of our E/W calls at table B is a pass at
fit 1.000 over a BEN N/S slam auction.  There is no overcall, no balancing seat
and no competitive decision on the board.

The loss is constructive: South opens `1D` on `AT.AK.AKQ97.T763` (20 HCP,
`open_2C` fits 0.836, `open_2NT` 0.000 because the hand is 2=2=5=4), and the
2NT/2C opening question plus `ob_1D1H_3C_jump` are the other reviewer's.

---

## Board 909 — margin -11 — NOTHING-WRONG (on the competitive axis)

**What I checked.**  Table A: we are N/S with 5 and 6 HCP and pass at fit 1.000
in the direct seat over 1D (`oc1D_pass`), in the sandwich seat over 1NT
(`sw_pass`) and twice over their 3D/3NT (`ch_pass`); BEN passes every one of
them at 1.00 confidence.  Table B the auction is our own and uncontested.

The divergence is East's pass of partner's `3D` jump rebid on
`A96.K32.Q98.JT95` where 3NT is right — the responder-after-a-jump-rebid
ladder in `general_uncontested_continuation` (`uc_nt3` demands 13-19 and East
has 10, fit 0.134).  Constructive, and `uc_nt3`'s strength gate is explicitly
scope-excluded, so I propose nothing here.

---

## Board 953 — margin -11

**Seat/call that went wrong:** table B, call 2, **West passes 1C** holding
`AT8543.3.QJ953.5` (6=1=5=1, 7 HCP, 10 total points, LTC 6) after `P – 1C`.

**Missing agreement:** a one-level overcall is a matter of shape and losers,
not of high cards — a 6-5 two-suiter with six losers is an overcall on seven
points, and the file's minimum-HCP floor leaves it with no call at all.

`oc1C_1S` demands 8 HCP (fit 0.800 on seven); `oc1C_2S_jump` demands the
`good_suit(S)` feature, which `AT8543` fails, and a feature miss scores a flat
0.200.  So `oc1C_pass` at 1.000 wins and N/S bid an uncontested 4H for +450.

### YAML — into the EXISTING context `overcalls_of_1C`

```yaml
      - id: oc1C_1S_shape
        call: 1S
        priority: 69
        requires:
          suits: { S: [6, 13] }
          hcp: [6, 10]
          evals: { ltc: [0, 6], total_points: [9, 40], "suit_quality(S)": [1, 9] }
        shows: "shapely one-level overcall: six spades in a two-suiter, six losers or fewer"
        establishes: { forcing: non_forcing }
```

**Answering seat:** none — `non_forcing`, and the advance of a simple overcall
(`advance_overcall*`, `cl_raise_*`) already exists.  The 6-10 HCP floor keeps
partner's shown minimum for 1S honest, because same-call rules merge into a
disjunction in the partner model.

**What it endangers, in `overcalls_of_1C`:**
* `oc1C_1S` (1S, 71) — same call, higher priority, so an 8-16 hand keeps the
  primary reading; mine only picks up 6-7 counts.
* `oc1C_1D` (1D, 70) — with 6-5 the six-card major is the overcall, not the
  five-card minor; and at 7 HCP `oc1C_1D` does not fit either.
* `oc1C_2S_jump` (60) — **checked explicitly.**  DECISIONS records that
  re-ranking the weak jump overcall measured -24 held out because "the jump was
  already reachable below 8 HCP … and on the 8-10 overlap the one-level call is
  better".  The `ltc <= 6` gate is what keeps me out of its population: a
  one-suited `KQJ983.542.72.94` has LTC 8, scores my rung 0.046, and still bids
  2S by `oc1C_2S_jump` at fit 1.000 (**verified**).
* `oc1C_3S_preempt` (58), `oc1C_pass` (25).
* **No fallback hazard:** 1S is already covered by `oc1C_1S`.

**VERIFIED.**  West bids `1S` at fit 1.000 / prio 69, `clear=True`; the
one-suited control still bids 2S.

**Template:** as on board 532 the four overcall contexts are longhand, so this
is one rung per (opened suit, six-card overcall suit) pair — 12 in total —
unless the four contexts are refactored onto `expand_pairs`.  A NEW context
cannot carry it: 1S is already `covered` by the earlier context and a later
context's rule for a covered call is silently dropped.

**Also worth recording, and it is a guardrail hit.**  The dossier names
`cl_raise_lott4_H` as the decider of North's 4H at table A.  It is not:
`cl_raise_lott4_H` fits **0.034**, and the actual chooser is **`cl_raise_H4`**
at fit 1.000 (13 support points with the club singleton counted opposite the
agreed heart suit, `rule_of_26` exactly 25).  4H is also the right contract —
4H by South makes eleven — so there is nothing wrong with that call at all.
The board was lost to `gr_rkc_H` (4NT), which `fires_summary` puts at
**7 tables, -20 IMPs, mean -2.86** across the whole corpus; that is the
keycard-ask-over-a-game-raise population, and a gate on it is on the
do-not-re-propose list.

---

## Board 957 — margin -11

**Seat/call that went wrong:** table A, call 9, **South bids 3S** holding
`KT8.432.Q9.KQJ72` after `P – P – 1H – 1S – P – 2H – X – 2S – P`.  3S went
three down doubled-value (-300); BEN passes.

**Missing agreement:** when they double our cue-bid raise and partner makes the
FORCED retreat to his overcalled suit, the cue-bidder passes — the retreat
shows nothing (`advcueX_retreat` is literally `requires: {}`), so the values
the cue bid already promised must not be shown a second time.

The seat has no context of its own, so it falls to
`general_uncontested_continuation` (the "`... - P - ?` means RHO passed"
dispatch bug) and `uc_raise_S3` raises again on 12 support points and three
trumps as though nothing had happened.  This is a two-step conversation the
file opens (`advo_cue`) and never closes.

### YAML — a NEW context, immediately BEFORE `advance_cue_doubled_pull`

```yaml
  - id: advance_cue_doubled_retreat
    description: "Partner made the forced retreat from our doubled cue-raise"
    expand_pairs:
      - { o: C, v: H }
      - { o: C, v: S }
      - { o: D, v: H }
      - { o: D, v: S }
      - { o: H, v: S }
    pattern: "1$o - 1$v - P - 2$o - X - 2$v - P - ?"
    rules:
      - id: advcueXr_pass_$v
        call: P
        priority: 62
        requires: {}
        shows: "the cue bid already showed the raise and the retreat showed nothing: pass"
        establishes: { forcing: sign_off, agreed_suit: $v }
      - id: advcueXr_raise_$v
        call: 3$v
        priority: 63
        requires:
          suits: { $v: [4, 13] }
          evals: { total_points: [14, 40], "lott_total_trumps($v)": [9, 26] }
        shows: "extras beyond the cue-bid raise and a fourth trump: one more try"
        establishes: { forcing: non_forcing, agreed_suit: $v }
      - id: advcueXr_game_$v
        call: 4$v
        priority: 64
        requires:
          suits: { $v: [4, 13] }
          evals: { total_points: [17, 40], "lott_total_trumps($v)": [9, 26] }
        shows: "the cue-bid raise was an underbid: bid the game"
        establishes: { forcing: non_forcing, agreed_suit: $v }
```

**Answering seat:** this IS the answering seat — it closes the conversation
`advo_cue` → `advcueX_retreat` → *(nothing)*.  Every rung is `non_forcing` or
`sign_off`, so no new question is opened.

**What it endangers.**  The pattern has eight tokens, so specificity 1008
against `general_uncontested_continuation`'s 2: this context now OWNS `P`, `3v`
and `4v` on exactly these five auctions and the following rules lose them there:
* `uc_raise_S3` / `uc_raise_H3` (31) — the cue bid already showed 10+ support
  points; repeating them opposite a retreat that showed nothing is bidding the
  same values twice.
* `uc_raise_S4` / `uc_raise_H4` (32) — same sentence one level higher; my
  `advcueXr_game_$v` reaches game only on 17+ support points, which is a hand
  that genuinely underbid with the cue.
* `uc_pass` (18) — replaced by `advcueXr_pass_$v`, which fits 1.00 on every
  hand exactly as `uc_pass` did, so the seat cannot be starved.
* `uc_nt2`/`uc_nt3`/`uc_new_*` are untouched (different calls, still supplied by
  the generic context).
* **Fallback:** the new context covers P / 3v / 4v; 3v and 4v were already
  covered by `uc_raise_*` in the same seat, and P by `uc_pass`, so no code
  fallback is deleted.

**VERIFIED.**  South passes at fit 1.000, prio 62, `clear=True`;
`advcueXr_raise_S` fits 0.012 on this hand and `advcueXr_game_S` 0.000.

**Template:** `expand_pairs` over the five (opened minor-or-heart, overcalled
suit) combinations, copied verbatim from `advance_cue_doubled` /
`advance_cue_doubled_pull` so the three contexts stay in step.

---

## Board 12 — margin -10

**Seat/call that went wrong:** table A, call 8, **North bids 3D**, VULNERABLE,
holding `QJ7.7.A97543.Q83` (9 HCP, one quick trick) after
`P – P – P – 1NT – P – 2H – P – 2S`.  3S then made ten tricks (-170) where
BEN's pass left them in 3NT three down (+300).

**Missing agreement:** vulnerable, with the opponents having found a fit and
nobody on our side having bid, a bare six-card suit with no honour strength is
not an entry into the auction — the vulnerable three-level phantom is a
matchpoint discipline the file has nowhere.

**Guardrail hit:** the dossier names `cl_new_D3`.  It is not the decider —
`cl_new_D3` fits **0.102**.  The actual chooser is **`cl_new_long3_D_hi`**
(prio 27.5, fit 1.000): a SIX-card suit, 11+ total points, `suit_quality >= 1.0`,
and `A97543` scores exactly 1.0.  Its own file comment records the threshold was
tuned on a 400-board A/B and that at 11/1.0 "it bid 3S on JT8754 and got
doubled" — the calibration has no vulnerability term at all.

### YAML — into the EXISTING context `general_competitive_low`

```yaml
      - id: cl_vul_discipline_pass
        call: P
        priority: 27.6
        when: { we_vulnerable: true, side_has_acted: false, standing_bid_level: [2, 3] }
        requires:
          hcp: [0, 10]
          evals: { quick_tricks: [0, 1.5], their_fit: [7, 26] }
        shows: "vulnerable, they have a fit, nobody on our side has bid and I have neither values nor defence: pass"
        establishes: { forcing: non_forcing }
        negative_inference_weight: soft
```

`negative_inference_weight: soft` matters: this pass must not teach the partner
model that a passing hand denies a six-card suit.

**Answering seat:** none — it is a pass.

**What it endangers, in `general_competitive_low`:**
* `cl_new_long3_$X` / `_hi` (27 / 27.5) and `cl_new_$X2` / `$X3` (26-27.5) —
  every natural entry at the two and three level, but ONLY when vulnerable,
  with under 11 HCP, under two quick tricks, and after they have shown a fit.
  That is precisely the population the -170 came from: partner is not marked
  with values, we have no defence, and the level is theirs.
* `cl_nt2` / `cl_nt3` (28 / 29), `cl_raise_*` (30-32), `cl_negative_X2` (33),
  `cl_takeout_X` (36) all sit ABOVE it and are untouched — a raise of partner's
  suit needs `partner_suit`, which cannot hold when `side_has_acted: false`.
* `cl_pass` (20) — same call, so no fallback consequence at all.
* **Non-vulnerable behaviour is unchanged** — verified: the identical hand at
  EW vulnerability still bids 3D by `cl_new_long3_D_hi` at fit 1.000.

**VERIFIED.**  North passes at fit 1.000 / prio 27.6, `clear=True`, vulnerable;
bids 3D unchanged non-vulnerable.

**Template:** one rung, no expansion (the gates are suit-free).  Its twin
belongs in `general_competitive_high` (`ch_vul_discipline_pass`, priority 27.6,
`standing_bid_level: [3, 4]`) where the same phantom is one level dearer.  I
would NOT put it in the balancing contexts: in the passout seat the whole point
is to reopen, and the hand types differ.

**Note on the dossier's first divergence:** North's opening pass on the same
hand (`open_weak_2D_vul` fits 0.757 on 9 HCP with `A97543`) is an
opening-style threshold and is scope-excluded.

---

## Board 90 — margin -10

**Seat/call that went wrong:** table A, call 6, **North raises to 4H** holding
`KT53.AQJT9.AQ2.6` after `P – P – 1H – 1NT – 2H – P`.  4H made nine (-50);
3H makes nine (+140), and BEN passes 2H.

**Missing agreement:** when RHO's overcall has ANNOUNCED 15-18, partner's raise
is obstruction and the combined-points test is a fiction — three of the major
is the limit unless my own hand is worth game opposite a bust.

`uc_raise_H4` fits 1.000 because with hearts agreed North counts 19 total points
and `rule_of_26` reaches 25.5 against a partner whose shown minimum is 5.  But
East has announced 15, North holds 16, so partner and West share nine: the
arithmetic that licenses game has already been contradicted by the auction.
`their_shown_hcp` is in the evaluator registry and **no rule in the file uses
it for this**.

### YAML — into the EXISTING context `general_uncontested_continuation`

```yaml
      - id: uc_raise_capped_H3
        call: 3H
        priority: 32.5
        when: { partner_suit: H, cheapest_in_suit: true }
        requires:
          suits: { H: [4, 13] }
          evals: { their_shown_hcp: [15, 40], total_points: [11, 20],
                   "lott_total_trumps(H)": [8, 9] }
        shows: "they have announced 15+, so partner's raise is obstruction and three of the major is the limit"
        establishes: { forcing: non_forcing, agreed_suit: H }
      - id: uc_raise_capped_S3
        call: 3S
        priority: 32.5
        when: { partner_suit: S, cheapest_in_suit: true }
        requires:
          suits: { S: [4, 13] }
          evals: { their_shown_hcp: [15, 40], total_points: [11, 20],
                   "lott_total_trumps(S)": [8, 9] }
        shows: "they have announced 15+, so partner's raise is obstruction and three of the major is the limit"
        establishes: { forcing: non_forcing, agreed_suit: S }
```

**Answering seat:** none — `non_forcing`, and 3H is already a rung partner's
model reads (`uc_raise_H3`), so nothing new is being asked.

**What it endangers, in `general_uncontested_continuation`:**
* `uc_raise_H4` / `uc_raise_S4` (32) — the target.  One sentence: partner's
  raise over a strong-notrump overcall promised nothing, and their announced
  15-18 has already spent the points my raise to game would need.
* `uc_raise_lott4_H` / `_S` (32) — **explicitly protected.**  The Law raise to
  four is right when they have a fit and we hold ten trumps; my
  `lott_total_trumps: [8, 9]` band excludes exactly that, and
  `lott_total_trumps` carries sharp tolerance 0.4, so a ten-trump hand scores
  my rung 0.082 and the Law raise keeps it.
* `uc_raise_H3` / `uc_raise_S3` (31) — same call, so no behaviour changes.
* `gst_rkc_H` (46) is above and untouched — but note it fits 0.000 here anyway.
* **No fallback hazard:** 3H/3S are already covered by `uc_raise_H3`/`_S3`.
* The `total_points: [11, 20]` ceiling is the escape hatch: a 21+ hand still
  bids game through `uc_raise_$M4`, because 21 misses my band and scores 0.8,
  below the fast path.

**VERIFIED.**  North bids `3H` at fit 1.000 / prio 32.5, `clear=True`
(`uc_raise_H4` 1.000/32 immediately behind).

**Template:** the explicit `_H` / `_S` pair above.  The same pair belongs in
`general_competitive_low` (`cl_raise_capped_$M3`) and
`general_competitive_high`, where the identical arithmetic runs.

---

## Board 94 — margin -10

**Seat/call that went wrong:** table B, call 7, **East bids 2C** holding
`9.AKT6.6432.AK75` (14 HCP, 4 quick tricks) after `P – 1C – 1S – X – P – 1NT – P`.
BEN bids 3NT at 0.84; 3NT by West makes nine.

**Missing agreement:** after my negative double and partner's notrump REBID —
which is a limited natural description with their suit stopped, not a response —
I raise to game on values alone; I do not need a stopper of my own.

`uc_nt3` is unreachable (East is 1=4=4=4 with a stiff spade: `balanced` 0,
`stopper(S)` 0, fit 0.000).  `uc_nt_raise3` exists but its `when` pins
`standing_bid_level: [2]`, with a file comment saying a ONE-level notrump from
partner is a response rather than a description — true of a 1NT *response*,
false of the 1NT *rebid over a negative double*, which is the classic 12-14
balanced with a stopper.  That is a sibling gap, not a judgment call.

What actually chose 2C is worth recording on its own: `uc_doubler_raise_C`
("raise of the advance: 17-19 with 4-card support") fits **1.000** because with
clubs agreed East's singleton spade lifts 14 HCP to 17 total points — and its
`when` never checks that partner's SUIT is the standing bid, so it retreats
below partner's own notrump.

### YAML — into the EXISTING context `general_uncontested_continuation`

```yaml
      - id: uc_nt_raise3_after_X
        call: 3NT
        priority: 34.5
        when: { we_bid_last: true, standing_bid_strain: [NT], standing_bid_level: [1],
                my_last_call_was_double: true }
        requires: { evals: { rule_of_26: [25, 99] } }
        shows: "raising partner's notrump rebid to game: my double showed the values and partner has shown their suit stopped"
        establishes: { forcing: sign_off }
```

The twin belongs in `general_competitive_low` (`cl_nt_raise3_after_X`) for the
case where they bid again over partner's 1NT.

**Answering seat:** none — `forcing: sign_off` names the final contract.

**What it endangers.**  The `when` is very narrow: partner's ONE-level notrump
is the standing bid and my last call was a double.  Inside that window it
outranks —
* `uc_doubler_raise_$X` (2C/2D/2H/2S, 34) — a retreat to partner's minor below
  his own notrump, on a hand that has 25+ combined and a stopper shown.
* `uc_doubler_raise3_$X` (33), `uc_raise_$X2/3` (30/31), `uc_nt3` (29),
  `uc_nt2` (28), `uc_minor_game_5$m` (28), `uc_new_*` (26-27.5), `uc_pass` (18)
  — all of which describe less than "we have the values for the only game
  available, and partner has said the suit they bid is stopped".
* Below 25 combined the rung does not fit, so the minimum negative doubler is
  untouched — **verified**: an 8-HCP `9.AK76.6432.7532` still bids 2C by
  `uc_raise_C2`, my rung at fit 0.004.
* **No fallback hazard:** 3NT is already covered here by `uc_nt3`.

**VERIFIED.**  East bids `3NT` at fit 1.000 / prio 34.5, `clear=True`.

**Template:** one rung here and one in `general_competitive_low`; the `when`
carries no suit, so no expansion.  If a consolidator prefers, the cleaner form
is to relax `uc_nt_raise3`'s `standing_bid_level` to `[1, 2]` **only** under an
added `my_last_call_was_double: true` sibling — but that is the same rule
written twice, and the sibling lint prefers two explicit rungs.

---

## Board 133 — margin -10

**Seat/call that went wrong:** table A, call 5, **South passes 4S out** holding
`53.KT963.AKQJ2.Q` (15 HCP, 17 total points, five losers, `suit_quality(D)`
3.5) after `2S – X(mine) – 4S – P – P`.  5D by South makes eleven (+600);
we took +150 defending.

**Missing agreement:** the takeout doubler whose partner could not answer must
not sell out to their raised preempt — with five losers and a strong five-card
suit, bid it at the five level; partner's pass over 4S was "no opinion", not a
conversion.

South's whole candidate set in that seat is **two** rules: `balhigh_pass`
(1.000) and `balhigh_reopen_X2` (0.028, needs 19+).  The reason is structural:
`general_balancing_high` has **no five-level rung of any kind**, while its
sibling `general_competitive_high` has the complete family
(`ch_new_$X5`, `ch_new_$X5_hi`, `ch_rebid_$X5`).  A sibling gap of exactly the
species the lint was written for.

### YAML — into the EXISTING context `general_balancing_high`

```yaml
      - id: balhigh_doubler_own_C5
        call: 5C
        priority: 30
        when: { unbid_suit: C, cheapest_in_suit: true, my_last_call_was_double: true,
                partner_has_acted: false }
        requires:
          suits: { C: [5, 13] }
          evals: { total_points: [16, 40], ltc: [0, 6], "suit_quality(C)": [2, 9] }
        shows: "the doubler bids his own suit at the five level: five losers and a strong suit, the double is still working"
        establishes: { forcing: non_forcing, agreed_suit: C }
      - id: balhigh_doubler_own_D5
        call: 5D
        priority: 30
        when: { unbid_suit: D, cheapest_in_suit: true, my_last_call_was_double: true,
                partner_has_acted: false }
        requires:
          suits: { D: [5, 13] }
          evals: { total_points: [16, 40], ltc: [0, 6], "suit_quality(D)": [2, 9] }
        shows: "the doubler bids his own suit at the five level: five losers and a strong suit, the double is still working"
        establishes: { forcing: non_forcing, agreed_suit: D }
      - id: balhigh_doubler_own_H5
        call: 5H
        priority: 30
        when: { unbid_suit: H, cheapest_in_suit: true, my_last_call_was_double: true,
                partner_has_acted: false }
        requires:
          suits: { H: [5, 13] }
          evals: { total_points: [16, 40], ltc: [0, 6], "suit_quality(H)": [2, 9] }
        shows: "the doubler bids his own suit at the five level: five losers and a strong suit, the double is still working"
        establishes: { forcing: non_forcing, agreed_suit: H }
```

**Answering seat:** none — `non_forcing` with `agreed_suit`, which is what keeps
partner out of a suitless game force if they double us.  Partner's raise/pass
ladder over a named suit already exists in the same context.

**What it endangers, in `general_balancing_high`:**
* `balhigh_pass` (21) — the target; selling out with 17 support points, a
  solid five-card suit and five losers is the error the board measures.
* `balhigh_reopen_X2` / `balhigh_reopen_X` / `balhigh_X` (40 / 41) stay ABOVE
  it: a 19+ hand with no suit still doubles again, which is right.
* `balhigh_new_$X4` (28), `balhigh_rebid_$X4` (29), `balhigh_raise_*` (27-32)
  are all at a LOWER level and are unaffected — none of them is legal over 4S,
  and where they are legal `cheapest_in_suit` keeps my five-level rung out.
* **Fallback hazard — real, and the one I would screen.**  5C/5D/5H are not
  currently covered anywhere in `general_balancing_high`, so these rungs delete
  the code fallback for those calls in every `... - bid>=3C - P - P - ?` seat
  where the suit is unbid, cheapest, my last call was a double and partner has
  not acted.  That is a narrow window, but it is the round-15 mechanism and
  should be measured, not assumed.

**VERIFIED.**  South bids `5D` at fit 1.000 / prio 30, `clear=True`.

**Template:** three explicit rungs as above (5S is unreachable in this seat by
construction — if spades were unbid and cheapest, they would be at the four
level).  The same three belong in `general_competitive_high` as
`ch_doubler_own_$X5` for the case where they bid again rather than pass.

**Checked and rejected.**  BEN's alternative — North bidding `5C` over 4S on
`7.AJ2.T3.AT87652` — is a LOSER: 5C by North is ten tricks double-dummy, so it
is -100 against the +150 we actually scored.  `advance_weak2_double_raised`
does lack any minor advance (`aw2r_4S_$W` / `aw2r_4H_$W` / responsive X only),
which is a genuine hole, but this board is not the evidence for filling it.

---

## Board 174 — margin -10 — NOTHING-WRONG (on the competitive axis)

**What I checked.**  Table A we are N/S with `963.A875.94.K762` (7 HCP) and
`JT54.J943.A85.85` (6 HCP) against an uncontested `1D – 1H – 3C – 3NT`: the
direct seat over 1D (`oc1D_pass`), the sandwich seat over 1H (`sw_pass`) and
both seats over 3C/3NT (`ch_pass`) are all fit 1.000, and BEN passes every one
of them at 1.00.  Neither hand has a five-card suit or eight points.  Table B
the auction is ours and uncontested throughout.

The divergence is West's `2C` rebid on `AQ8.Q.QJ632.AQ93` (17 HCP) where the
3C jump shift is right — `ob_1D1H_3C_jump` demands 18+ and fits 0.800, a
one-point soft miss beaten by `ob_1D1H_2C` at 1.000.  That is a constructive
ceiling in the opener's-rebid family and belongs to the other reviewer.

---

## Board 175 — margin -10

**Seat/call that went wrong:** table B, call 6, **East bids 4D** holding
`KJT9.KJ3.KQ5.A84` (17 HCP, every unshown suit stopped) after
`2D – P – 2NT – P – 3S – P`.  3NT makes eleven (+660); 4D made twelve for +170.

**Missing agreement: four of a MINOR is not a game.**  `w2ac_game_$W` bids
`4$W` at priority 56 and the context expands `W` over `[D, H, S]`, so opposite a
weak two in DIAMONDS the ask's own answer is a contract nobody can score a game
in — and it outranks `w2ac_3NT_$W` (55), which is the only game the hand has.

The file already knows this.  The comment on `w2ac_game8_$W` says in as many
words: "loosening `w2ac_game_$W` in place also loosens the MINOR, where nine
tricks beat eleven and 3NT is right".  The rung was never split.

### YAML — into the EXISTING context `weak2_ask_continuation`

```yaml
      - id: w2ac_3NT_over_2D
        call: 3NT
        priority: 56.5
        when: { partner_suit: D }
        requires: { hcp: [14, 40], evals: { weakest_unshown_stopper: [0.9, 9] } }
        shows: "nine tricks opposite the weak two in a minor: four of a minor is not a game"
        establishes: { forcing: sign_off }
      - id: w2ac_game5_over_2D
        call: 5D
        priority: 55.5
        when: { partner_suit: D, cheapest_in_suit: true }
        requires:
          suits: { D: [3, 13] }
          evals: { total_points: [18, 40], "lott_total_trumps(D)": [9, 26] }
        shows: "eleven tricks opposite the weak two in a minor when notrump is not safe"
        establishes: { forcing: sign_off, agreed_suit: D }
```

Both rungs are self-selecting: `when: { partner_suit: D }` holds only in the
`[D]` expansion of the context, so the `[H]` and `[S]` copies are inert and the
major ladder is untouched.  `weakest_unshown_stopper` is the right stopper
evaluator here — it carries 0.3 sharp tolerance in `_EVAL_S2`, unlike
`weakest_their_stopper`, which `DECISIONS.md` records as not gating at all.

**Answering seat:** none — both are `forcing: sign_off`, they name the final
contract, and the ask has already been answered.

**What it endangers, in `weak2_ask_continuation`:**
* `w2ac_game_$W` (56) — only in the `[D]` expansion, and only on hands with
  14+ and every unshown suit stopped.  One sentence: 4D scores 130 and 3NT
  scores 400, so with nine tricks and the suits stopped the notrump game is the
  only contract worth reaching.
* `w2ac_3NT_$W` (55) — same call, so no behaviour changes; mine only lifts it
  above the minor "game" rung.
* `w2ac_game8_$W` (54.5) and `w2ac_sign_$W` (54) — both describe less: `game8`
  is the same 4D, `sign` is 3D, and a 17-count with stoppers is not signing off.
* Without stoppers my 3NT rung does not fit and the existing ladder decides
  exactly as before.
* **No fallback hazard:** 3NT is already covered by `w2ac_3NT_$W`; 5D is a new
  call in this context, but the `when` (partner's suit is diamonds and 5D is
  cheapest) plus the 18-point floor make the window tiny.

**VERIFIED.**  East bids `3NT` at fit 1.000 / prio 56.5, `clear=True`
(`w2ac_game_D` 1.000/56 immediately behind).

**Template:** the two rungs are written once inside the existing
`expand: { W: [D, H, S] }` context and self-select on `partner_suit: D`; there
is no 2C weak two, so diamonds is the whole minor case.  The same split is owed
to any other ask-continuation ladder that bids `4$W` over an expansion
containing a minor — `lint_system.py --only sibling` should be pointed at it.

---
