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

## Board 253 — margin -10

**Seat/call that went wrong:** table A, call 7, **North passes 3S** holding
`T8.83.K62.A76542` (7 HCP, an ace and a king, doubleton spade) after
`2H – X – P – 3C – P – 3S – P`.  4S makes eleven (+650); we stopped in 3S (+200).

**Missing agreement:** when the takeout doubler names a suit of his own at the
three level over my FORCED minimum advance, he is showing six of them and a big
hand — my doubleton is the eighth trump, and with the top of my 0-8 range plus
two controls I raise to game.

North's seat has no context: it falls to `general_uncontested_continuation`,
and `uc_raise_S4` fits **0.034** because `lott_total_trumps(S)` counts partner's
SHOWN five plus my two = seven.  This is the "after partner raises my own suit
every generic raise rung is dead" species from `DECISIONS.md`, in the
double-then-bid seat.  The conversation `vw2_X` → `aw2H_3C` → *(doubler's suit)*
→ **nothing** is opened by the file and never closed.

### YAML — a NEW context, immediately BEFORE `advance_weak2_double_raised`

```yaml
  - id: advance_double_doubler_suit
    description: "The doubler named a suit of his own over my forced advance"
    expand_pairs:
      - { W: D, M: H }
      - { W: D, M: S }
      - { W: H, M: S }
    pattern: "2$W - X - P - bid - P - 3$M - P - ?"
    rules:
      - id: adds_game_$M
        call: 4$M
        priority: 60
        requires:
          suits: { $M: [2, 13] }
          evals: { total_points: [6, 40], controls: [2, 12] }
        shows: "the doubler bid his own suit at the three level, so he holds six: my doubleton is the eighth trump"
        establishes: { forcing: non_forcing, agreed_suit: $M }
      - id: adds_pass_$M
        call: P
        priority: 55
        requires: {}
        shows: "minimum for the forced advance: leave the doubler in his own suit"
        establishes: { forcing: sign_off, agreed_suit: $M }
```

**Answering seat:** none — the pass rung IS the closure, and `adds_game_$M`
names game.  Both carry `agreed_suit`, so if they compete over us the
`ch_raise_*` ladder reads the auction correctly.

**What it endangers.**  Specificity 1008 vs `general_uncontested_continuation`'s
2, so this context takes over `P` and `4$M` on exactly these three auction
shapes:
* `uc_pass` (18) — replaced by `adds_pass_$M`, which is `requires: {}` and fits
  1.00 on every hand, so the seat cannot be starved.
* `uc_raise_$M4` (32) and `uc_raise_lott4_$M` (32) — both are already dead here
  (0.034 and 0.000) because the LOTT gate counts partner's shown five; mine is
  the rule that knows a doubler who then bids has six.
* `uc_rebid_C4` (29), `uc_nt3` (29) and `gst_rkc_S` (46) keep their calls (4C,
  3NT, 4NT) — my context defines neither, so they are still supplied by the
  generic contexts.
* **No fallback hazard:** P and 4S were both already covered in this seat.

**VERIFIED,** with a control: North bids `4S` at fit 1.000 / prio 60,
`clear=True`; a 2-HCP advancer (`T8.83.732.876542`) passes at
`adds_pass_S` 1.000 with `adds_game_S` at 0.002.

**Template:** `expand_pairs` over the three (weak-two suit, doubler's higher
suit) combinations.  A fuller version would add the `4$M`-over-a-two-level
advance and the minor cases; those seats are equally empty but no board in this
slice reaches them.

---

## Board 255 — margin -10

**Seat/call that went wrong:** table A, call 3, **South bids 3D**, VULNERABLE,
holding `KQJ.6.QJT985.J52` (10 HCP, one quick trick) after `2H – P – 2NT`.
They then bid 4H for -650; passing leaves it at -200 or better.

**Missing agreement: this is the SAME agreement as board 12, and this board is
its second independent confirmation.**  Vulnerable, they have a fit, nobody on
our side has bid, and I hold under two quick tricks and less than an opening
bid — a bare six-card suit is not an entry into the auction.

The mechanism is identical too, down to the rule: the dossier says `cl_new_D3`
(fit 0.409) and the actual decider is **`cl_new_long3_D_hi`** at 27.5 / fit
1.000 — `QJT985` scores `suit_quality` 2.0 and the hand has 12 total points,
so the six-card rung's 11-point / 1.0-quality calibration passes it, with no
vulnerability term anywhere in the gate.

### YAML

Exactly the rung proposed on board 12 — `cl_vul_discipline_pass`, priority 27.6
in `general_competitive_low`.  Repeated here so the section is self-contained:

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

**VERIFIED on this board too.**  South passes at fit 1.000 / prio 27.6,
`clear=True`, with `cl_new_long3_D_hi` 1.000/27.5 immediately behind.  Two
boards, one rung, both traced — that is the strongest single piece of evidence
in my slice, and it is a two-board population rather than a one-board one.

**Endangers / template:** as board 12.  Ten HCP is the top of my band, so this
board sits exactly on the ceiling; if the consolidator wants margin, `hcp:
[0, 10]` is the number to test at 11, not the quick-trick gate.

**Two further competitive observations on this board, neither proposed.**
(i) At table B West passes as dealer on `4.KJT952.73.QT94` where BEN opens 2H
at 0.98 — vulnerable weak-two style, and opening thresholds are scope-excluded.
(ii) At table A call 5 North holds six spades and 10 HCP and passes partner's
3D; BEN bids 3S, which would have held it to -200.  That seat becomes moot if
South never bids 3D, which is what the rung above does.

---

## Board 269 — margin -10

**Seat/call that went wrong:** table A, call 3, **North PASSES** holding
`A9743.AQ6.AT74.5` — **14 HCP and five spades** — after `P – 1D(partner) – 2C`.
Passing partner's opening with 14 HCP is the largest single error in my slice.

**Missing agreement:** responder's free bid of a new suit over an overcall is
about values and length, not suit texture — with 11+ opposite a partner who has
bid, `A9743` is a two-level bid.

`cl_new_S2` / `cl_new_S2_hi` demand `suit_quality(S) >= 1.5`; `A9743` scores
**1.0**, a half-point miss that drops them to 0.757 and hands the seat to
`cl_pass` at 1.000.  That texture gate is calibrated for an OVERCALL, where
suit quality really is the constraint; `general_competitive_low` is also where
responder's free bid lands, and there partner has already promised an opening
bid, so texture is the wrong test.

### YAML — into the EXISTING context `general_competitive_low`

```yaml
      - id: cl_free_major_S2
        call: 2S
        priority: 28.5
        when: { unbid_suit: S, cheapest_in_suit: true, partner_has_acted: true,
                i_have_acted: false }
        requires:
          suits: { S: [5, 13] }
          hcp: [10, 40]
        shows: "a five-card major at the two level outranks notrump: partner has bid and I still have a major to show"
        establishes: { forcing: non_forcing }
```

with the twin `cl_free_major_H2` (2H, same gates), and the MINOR pair
`cl_free_minor_C2` / `cl_free_minor_D2` written identically but at priority
**26.7** — a minor does not outrank the notrump bid, a major does.  Board 400
in this same slice is the board that fixes the priority at 28.5; see there.

**Answering seat:** none.  Deliberately `forcing: non_forcing` rather than the
`one_round` a new suit "should" be: every other `cl_new_*` rung in this context
is non-forcing, opener's rebid after a free bid has no authored ladder, and
round 17's rule is that a force without an answering seat is worth less than
nothing.  The bid still gets partner to the right strain, which is the whole
loss on this board.

**What it endangers, in `general_competitive_low`:**
* `cl_new_S2` / `cl_new_S2_hi` (26 / 26.5) — same call, so nothing changes
  except which `shows` is reported and that the texture gate stops vetoing.
* `cl_new_long2_S` / `_hi` (26 / 26.5) — same call again.
* `cl_pass` (20) — the target.
* `cl_nt2` (2NT, 28) — outranked, and deliberately: see board 400, where
  exactly this priority order is what was wrong.  A hand with a five-card major
  bids the major; the notrump call denies one.
* `cl_nt3` (29), `cl_negative_X2` (33), `cl_takeout_X` (36), `cl_raise_*`
  (30-32) all sit ABOVE it and keep their hands.  `cl_negative_X2` carries
  `longest_suit_length: [0, 4]`, so a five-card major disqualifies it anyway and
  the two rungs never compete — **checked in the ranking**.
* **No fallback hazard:** 2S is already covered by `cl_new_S2`.

**VERIFIED.**  North bids `2S` at fit 1.000 / prio 28.5, `clear=True`, with
`cl_new_S2_hi` 0.757/26.5 behind it.

**Template:** two majors at 28.5 and two minors at 26.7 inside
`general_competitive_low`, and the same four in `general_competitive_high`
at the three and four levels (`ch_free_3H` / `ch_free_3S` already exist for the
majors — they carry the same `suit_quality >= 1.5` texture gate and want the
same treatment; the minors were never written at all).  No `expand:` exists in
these contexts, so they are longhand.

---

## Board 396 — margin -10

**Seat/call that went wrong:** table B, call 5, **East passes** holding
`AJT732.974.A3.A5` (13 HCP, six spades, six controls) after
`P – 1S – 3H – 3S(partner) – P`.  4S makes ten (+620); we played 3S.

**Missing agreement:** when partner raises my six-card major in a contested
auction, nine trumps with fourteen support points and five controls is a game —
the combined-points test counts partner's SHOWN minimum, and a competitive
raise deliberately understates it.

This is the `DECISIONS.md` open item "after partner RAISES my own suit every
generic raise rung is dead", measured on this board: `uc_raise_S4` (32) needs
`rule_of_26 >= 25` and East has **23**, fit 0.409; `uc_rebid_S4` (29) needs 26,
fit 0.134; `uc_raise_lott4_S` (32) needs their fit and ten trumps, fit 0.034.
Three game rungs, all dead, and `uc_pass` at 1.000 takes the seat.

### YAML — into the EXISTING context `general_uncontested_continuation`

```yaml
      - id: uc_rebid_game_S4
        call: 4S
        priority: 32.5
        when: { my_suit: S, partner_suit: S, cheapest_in_suit: true, is_competitive: true }
        requires:
          suits: { S: [6, 13] }
          evals: { "lott_total_trumps(S)": [9, 26], total_points: [14, 40],
                   controls: [5, 12], ltc: [0, 7] }
        shows: "partner raised my six-card major in competition: nine trumps, fourteen support points and five controls is a game, whatever the point-count test says about his minimum"
        establishes: { forcing: non_forcing, agreed_suit: S }
      - id: uc_rebid_game_H4
        call: 4H
        priority: 32.5
        when: { my_suit: H, partner_suit: H, cheapest_in_suit: true, is_competitive: true }
        requires:
          suits: { H: [6, 13] }
          evals: { "lott_total_trumps(H)": [9, 26], total_points: [14, 40],
                   controls: [5, 12], ltc: [0, 7] }
        shows: "partner raised my six-card major in competition: nine trumps, fourteen support points and five controls is a game, whatever the point-count test says about his minimum"
        establishes: { forcing: non_forcing, agreed_suit: H }
```

`is_competitive: true` is copied from `uc_raise_lott4_$M`, the one rung
`DECISIONS.md` records as porting cleanly into this context (at +12).  It keeps
the rung out of constructive auctions, where `rule_of_26` is the right test.

**Answering seat:** none — it names game and is `non_forcing` with an agreed
suit, so partner's only remaining decisions (pass, or a further raise if they
compete) are already authored in `ch_raise_*`.

**What it endangers, in `general_uncontested_continuation`:**
* `uc_raise_S4` / `uc_raise_lott4_S` (32) — same call, so nothing changes for
  hands they already fit; mine only picks up the hands they both miss.
* `uc_rebid_S4` (29), `uc_rebid_S3` (29), `uc_nt3` (29) — 3NT on a 6-3-2-2
  hand with a nine-card major fit and a preempt against us is the worse
  contract; `uc_nt3` fits 0.668 here, i.e. it is a soft-miss candidate, and
  outranking it is the point.
* `uc_pass` (18) — the target.
* **No fallback hazard:** 4S/4H are already covered by `uc_raise_$M4`.
* Controls, not points, is the honest separator, and `controls` carries sharp
  tolerance 1.4 — **verified** with a control hand: a minimum
  `AJT732.974.32.J5` (three controls) still passes, my rung at fit 0.000.

**VERIFIED.**  East bids `4S` at fit 1.000 / prio 32.5, `clear=True`.

**Template:** the `_H` / `_S` pair above; the minors are deliberately excluded
(four of a minor is not a game — see board 175).  The same pair belongs in
`general_competitive_low` and `general_competitive_high`, where an opener whose
major has been raised faces the identical dead ladder.

**Also checked, and NOT proposed.**  West's `3S` raise on `Q85.Q.QJ864.9762`
(the dossier's first divergence, `nx3_raise` fit 1.000 at 68) is a normal
competitive raise of a 1S opening over a weak jump overcall.  BEN passes at
0.91, but a three-card raise with seven points over a preempt is standard, and
the board is lost by East's failure to accept it, not by West's making it.

---

## Board 400 — margin -10

**Seat/call that went wrong:** table A, call 2, **South bids 2NT** holding
`AT5.QJT32.AT2.84` (11 HCP, **five hearts**) after `1C(partner) – 2D`.
North holds four hearts and 21 HCP; 6H makes thirteen.

**Missing agreement:** a five-card major outranks the notrump bid — over their
overcall, responder with 5+ in an unbid major bids the major, and the natural
2NT denies one.

`cl_nt2` (28) and `cl_new_H2` / `_hi` (26 / 26.5) BOTH fit 1.000; the priority
order decides, and it is the wrong way round.  Nothing about South's hand is
mis-described — this is purely a ranking hole, which is why it was invisible to
every rule-level yardstick.

### YAML — into the EXISTING context `general_competitive_low`

```yaml
      - id: cl_free_major_H2
        call: 2H
        priority: 28.5
        when: { unbid_suit: H, cheapest_in_suit: true, partner_has_acted: true,
                i_have_acted: false }
        requires:
          suits: { H: [5, 13] }
          hcp: [10, 40]
        shows: "a five-card major at the two level outranks notrump: partner has bid and I still have a major to show"
        establishes: { forcing: non_forcing }
      - id: cl_free_major_S2
        call: 2S
        priority: 28.5
        when: { unbid_suit: S, cheapest_in_suit: true, partner_has_acted: true,
                i_have_acted: false }
        requires:
          suits: { S: [5, 13] }
          hcp: [10, 40]
        shows: "a five-card major at the two level outranks notrump: partner has bid and I still have a major to show"
        establishes: { forcing: non_forcing }
```

**This is the same pair as board 269** — one rung, two boards, and the two
boards fix its priority from opposite directions: 269 says it must beat
`cl_pass` even on a ragged suit, 400 says it must beat `cl_nt2`.

**Answering seat:** none — `non_forcing`, and opener's rebid over a free bid is
already handled by the `uc_*` / `cl_*` ladders.

**What it endangers, in `general_competitive_low`:**
* `cl_nt2` (2NT, 28) — the target.  One sentence of bridge: with a five-card
  major and a partner who has opened, the major is the contract to explore and
  notrump is what you bid when you have not got one.
* `cl_new_H2` / `_hi` / `cl_new_long2_H` / `_hi` (26-26.5) — same call, so no
  behaviour changes; mine merely lifts 2H above 2NT and drops the texture gate.
* `cl_nt3` (29), `cl_raise_$m3` (31), `cl_negative_X2` (33) stay above.
  `cl_negative_X2` carries `longest_suit_length: [0, 4]`, so it and my rung can
  never both fit — **checked in the ranking**, it scores 0.349 here.
* `cl_pass` (20).
* **No fallback hazard:** 2H/2S already covered by `cl_new_$M2`.

**VERIFIED.**  South bids `2H` at fit 1.000 / prio 28.5, `clear=True`, with
`cl_nt2` 1.000/28 immediately behind — and the identical rung fixes board 269.

**Template:** the two majors at 28.5, the two minors at 26.7 (a minor does NOT
outrank the notrump bid), and the same four in `general_competitive_high` at
the three level.

---

## Board 408 — margin -10

**Seat/call that went wrong:** table A, call 4, **North passes** holding
`Q9864.K54.6.9865` (5 HCP, **five spades**) after `P – P – 1D(partner) – X`.

**Missing agreement:** over their takeout double, responder's one-level bid of
a FIVE-card major needs length, not points — four HCP is enough, because the
bid is non-forcing, takes up their room, and is the last chance to find the
major fit before the double's advance arrives.

`rx_D_1S` demands 6-9 HCP; North has five, fit 0.800, and `rdx_pass` at 1.000
takes the seat.  A five-point hand with a five-card major is the single most
common hand type in this position, and the ladder's floor was written for a
FOUR-card suit.

### YAML — into the EXISTING context `resp_over_double_D`

```yaml
      - id: rx_D_1S_five
        call: 1S
        priority: 61.5
        requires:
          suits: { S: [5, 13] }
          hcp: [4, 9]
          evals: { "suit_quality(S)": [1, 9] }
        shows: "new suit over their double: a FIVE-card major is worth the one level on four points"
        establishes: { forcing: non_forcing }
      - id: rx_D_1H_five
        call: 1H
        priority: 61.5
        requires:
          suits: { H: [5, 13] }
          hcp: [4, 9]
          evals: { "suit_quality(H)": [1, 9] }
        shows: "new suit over their double: a FIVE-card major is worth the one level on four points"
        establishes: { forcing: non_forcing }
```

Priority **61.5**, i.e. BELOW the four-card rungs at 62 — with 6-9 HCP the
existing reading stays primary and mine only picks up the 4-5 counts.

**Answering seat:** none — `non_forcing`, and opener's rebid after
`1D – X – 1S` already lands in the authored opener-rebid family.  The 4-9 HCP
floor keeps partner's shown minimum for 1S honest in the disjunctive partner
model (the existing rung's floor of 6 would otherwise be silently lowered to
nothing).

**What it endangers, in `resp_over_double_D`:**
* `rx_D_1S` / `rx_D_1H` (62) — same calls, higher priority, untouched.
* `rdx_pass` (20) — the target.
* `rx_D_1NT` (58), `rx_D_raise` (60), `rx_D_preempt` (61) — all sit below 61.5,
  so a 5-point hand with five spades AND four diamonds now bids 1S rather than
  raising.  One sentence: at the one level the major is free and the raise is
  not, and partner can still return to diamonds.  If a consolidator disagrees,
  60.5 (under the raise, over 1NT) is the conservative alternative — the board
  is fixed either way, because the raise does not fit this hand (one diamond).
* `rdx_XX` (75) is above and unaffected.
* **No fallback hazard:** 1S/1H already covered.

**VERIFIED.**  North bids `1S` at fit 1.000 / prio 61.5, `clear=True`.

**Template:** the same two rungs in each of `resp_over_double_C`,
`resp_over_double_D`, `resp_over_double_H` (spades only) and
`resp_over_double_S` (hearts only) — the contexts are longhand with no
`expand:`, so six rungs in all.

---

## Board 482 — margin -10 — NOTHING-WRONG (on the competitive axis)

**What I checked.**  `1NT – P – ?` with East and West holding 7 and 3 HCP:
`v1NT_pass` at fit 1.000 in the direct seat (BEN 1.00) and `cl_pass` / `ch_pass`
at 1.000 for the rest of BEN's slam auction at table B.  West's
`QT943.653.43.JT8` is the only shapely hand either opponent holds and it is a
3-count at neither vulnerability favourable; the only tool that would act on it
is a two-suited notrump defence (DONT / Cappelletti), and conventions of that
family are explicitly scope-excluded.

The loss is North's `3NT` on `K7.J72.AQ82.KQ94` (15 HCP, 4-4 in the minors)
opposite a 15-17 notrump — 30-32 combined with a running club fit, and
`nt_4NT_quant` fits 0.800 one point under its floor.  A notrump-ladder ceiling,
constructive, and the other reviewer's.

---

## Board 545 — margin -10 — NOTHING-WRONG (on the competitive axis)

**What I checked.**  Table A is `1NT – 3NT` by BEN with our two hands holding 8
and 5 HCP: `v1NT_pass`, `ch_pass` and `balhigh_pass` all at fit 1.000, BEN
agreeing at 1.00 on every one.  Table B the auction is entirely ours and N/S
never bid, so there is no competitive decision on the board at all.

The loss is the E/W constructive auction `1D – 2C – 2NT – 3NT – 4NT` reaching
a notrump slam try with nine tricks: East's `64.A87.AKQ986.Q7` is a 15-count
with a six-card suit that BEN opens 1NT, and then `uc_nt2` annexes opener's
rebid in a 2/1 game force — which `DECISIONS.md` already names twice ("there is
no context for opener's rebid after a 2/1 in a MINOR", and `uc_nt2`'s own open
item).  Both are on the constructive side of the line.

---

## Board 598 — margin -10 — NOTHING-WRONG (on the competitive axis)

**What I checked.**  Both auctions are uncontested.  Our E/W hands are
`43.AT95.J72.J832` (6 HCP) and `AT52.J63.QT43.T5` (7 HCP); the direct seat over
1H (`oc1H_pass`), the sandwich seat over 1NT (`sw_pass`) and the seats over 2S
(`cl_pass`) are all fit 1.000 with BEN at 1.00.  Neither hand has a five-card
suit or the values for a balancing action.

The loss is opener's rebid: South holds `KQJ6.KQ742.5.AK6` (18 HCP, 5-4 in the
majors) and `ob_1M1NT_2C` wins the seat at fit **0.800** — a soft-miss pick —
where `2S` is the bid.  Worth flagging to the constructive reviewer that the
chooser here is below the 0.9 fast path, so this is one of the soft-miss-lottery
decisions `DECISIONS.md` says run seven points of par gap worse than clean ones.

---

## Board 606 — margin -10 — NOTHING-WRONG (on the competitive axis)

**What I checked.**  Both auctions are uncontested; our E/W hands are
`A987.JT2.43.AT76` and `5432.764.A6.KQ52`, nine points each, and every one of
our calls is a pass at fit 1.000 that BEN also makes at 1.00 — the direct seat
over 1D (`oc1D_pass`), the sandwich seat over 1S (`sw_pass`), and `cl_pass` /
`ch_pass` afterwards.  Neither hand has a five-card suit or a takeout shape.

The loss is North's `2D` preference on `KQJT6.A9853.J7.9` — 5-5 in the majors
with a singleton and 11 HCP, where 4H is cold — and `r1d2c_2D` wins it at fit
**0.800**, another sub-fast-path chooser.  Responder's second bid with 5-5 in
the majors is constructive.

---

## Board 622 — margin -10

**Seat/call that went wrong:** table A, call 6, **North passes 2S** holding
`KQJT6..T83.J9742` (7 HCP, five spades, **a heart void**, a second five-card
suit) after `1NT – P – 2H – P – 2S – P`.  3NT makes ten; 2S made ten for +170.

**Missing agreement:** opposite a strong notrump, a completed transfer with
exactly five of the major and a VOID is worth an invitation on seven points —
the void is two tricks of playing strength that the HCP floor cannot see.

`nt_after_transfer` already knows voids matter: `tr_3NT_choice` excludes them
(`"void(any)": [0, 0]`) and `tr_game_void_$M` was written specifically to give
the void hand a floor at game values.  The rung was never given its
*invitational* twin, so a 7-count with a void falls to `tr_pass_weak`
(0-7 HCP) at fit 1.000 while `tr_2NT_inv` (8-9) misses by one at 0.800.
That is the ceiling/floor species with the void clause attached.

### YAML — into the EXISTING context `nt_after_transfer`

```yaml
      - id: tr_2NT_inv_void
        call: 2NT
        priority: 56.5
        requires:
          suits: { $M: [5, 5] }
          hcp: [5, 9]
          evals: { "void(any)": [1, 1] }
        shows: "invitational on shape: exactly five $M and a void opposite 15-17"
        establishes: { forcing: invitational }
```

**THE ANSWERING SEAT — checked, and it already exists and answers correctly.**
`establishes: { forcing: invitational }` is the same establishment
`tr_2NT_inv` already makes, so opener's seat after `1NT – P – 2H – P – 2S – P –
2NT – P` is unchanged: I traced South's actual hand `T8.AQJT.AJ94.KQT` through
it and it bids **3NT** by `uc_nt3` at fit 1.000, `clear=True`.  That is the
+630 contract.  No new seat is owed.

**What it endangers, in `nt_after_transfer`:**
* `tr_pass_weak` (P, 55) — the target.  A five-card major with a void opposite
  15-17 is not a sign-off hand; the void is worth the two points the HCP count
  is missing.
* `tr_2NT_inv` (2NT, 56) — same call, so no behaviour changes; on 8-9 with a
  void both fit and mine reports the better `shows`.
* `tr_3M_inv` (3M, 57), `tr_3NT_choice` (58), `tr_game_void_$M` (58.5),
  `tr_4$M` (59) all stay ABOVE it — a six-card suit, or 10-15 HCP, still
  outranks the shape invitation, which is right.
* The `[5, 5]` length band (sharp `_S2_SUIT`) keeps six-card hands on
  `tr_3M_inv`, and `"void(any)": [1, 1]` is sharp (0.05), so a singleton hand
  scores ~0.0 and is untouched.
* **No fallback hazard:** 2NT is already covered by `tr_2NT_inv`.

**VERIFIED.**  North bids `2NT` at fit 1.000 / prio 56.5, `clear=True`, and
South then bids 3NT.

**Template:** written once inside the existing
`expand_pairs: [ {M: H, T: D}, {M: S, T: H} ]`, so it becomes two rungs.
The honest caveat: this is a shape-revaluation agreement rather than a
competitive one, so it straddles my brief and the other reviewer's.

---

## Board 636 — margin -10

**Seat/call that went wrong:** table B, call 7, **West passes 3H** holding
`AJ84..AK65.AQT85` (18 HCP, 4.5 quick tricks, a heart VOID) after
`P – 2H – P – 3C – P – 3H – P`.  3NT by West makes nine (+600); we took +170.

**Missing agreement:** after my forcing new suit opposite partner's weak two,
his simple rebid of his own suit is a MINIMUM answer, not a pass-out — with 16+,
three quick tricks and every side suit held, I place the contract in 3NT.

`DECISIONS.md` names this exact species: "the forcing new suit opposite a weak
two is passed out — `rw2_new_*` is `forcing: one_round` and
`2$W - P - <new suit> - P - ?` has no context".  This board is the next station
down the same line: the file HAS an answer to the new suit (opener rebids his
suit through `uc_rebid_H3`), and the ASKER's placement seat is the one that is
empty.  West's whole candidate set is `uc_pass` 1.000, `uc_rebid_C4` 0.349,
`uc_new_S3` 0.349 — a starved seat at the end of a conversation the file itself
opened.

Note the file was right about the entry: `rw2_2NT_ask` deliberately excludes a
void in partner's suit ("you cannot ask about a suit you will never play"), so
3C is the intended call.  It is the third question, not the first, that has no
answer.

### YAML — a NEW context, immediately BEFORE `resp_weak2`

```yaml
  - id: resp_weak2_new_suit_rebid
    description: "Opener rebid his weak two after my forcing new suit: place the contract"
    expand: { W: [D, H, S] }
    pattern: "2$W - P - bid - P - 3$W - P - ?"
    rules:
      - id: rw2c_3NT_$W
        call: 3NT
        priority: 62
        requires:
          hcp: [16, 40]
          evals: { weakest_unshown_stopper: [0.9, 9], quick_tricks: [3, 12] }
        shows: "the rebid was a minimum: nine tricks in notrump with every side suit held"
        establishes: { forcing: sign_off }
      - id: rw2c_game_$W
        call: 4$W
        priority: 61
        when: { standing_bid_strain: [H, S] }
        requires:
          suits: { $W: [2, 13] }
          evals: { total_points: [17, 40], "lott_total_trumps($W)": [8, 26] }
        shows: "the rebid was a minimum but the fit is there: bid the major game"
        establishes: { forcing: sign_off, agreed_suit: $W }
      - id: rw2c_pass_$W
        call: P
        priority: 55
        requires: {}
        shows: "nothing more opposite the minimum rebid of the weak two"
        establishes: { forcing: sign_off, agreed_suit: $W }
```

`when: { standing_bid_strain: [H, S] }` on the raise makes it self-selecting:
in the `[D]` expansion the standing bid is 3D and the rung is inert, so the
file never bids "4D for game" (board 175's defect).

**Answering seat:** this IS the answering seat, and every rung is `sign_off`,
so the conversation closes.  `rw2c_pass_$W` is `requires: {}` and fits 1.00 on
every hand, so the seat can never be starved by the new context.

**What it endangers.**  Specificity 1007 against
`general_uncontested_continuation`'s 2, so this context takes `P`, `3NT` and
`4$W` on exactly these auctions:
* `uc_pass` (18) — replaced by `rw2c_pass_$W`, same call, same universal fit.
* `uc_nt3` (29) — replaced for 3NT; it fits 0.000 here anyway, because it
  demands `balanced` and the asker with a void never is.  That is the whole
  reason the seat was starved.
* `uc_raise_$W4` (32) / `uc_raise_lott4_$W` (32) — replaced for 4$W in the
  major case; both are dead for the same LOTT-counts-partner's-minimum reason.
* `uc_rebid_C4` (29) and `uc_new_S3` (27) keep their calls — my context defines
  neither, so the generic rungs still supply them.
* **Fallback: 3NT and 4$W were already covered** in this seat by `uc_nt3` and
  `uc_raise_$W4`, and P by `uc_pass`, so no code fallback is deleted.

**VERIFIED,** with a control: West bids `3NT` at fit 1.000 / prio 62,
`clear=True`; a 12-count `AJ84.2.K652.QT85` passes at `rw2c_pass_H` 1.000 with
`rw2c_3NT_H` out of the running.

**Template:** the existing `expand: { W: [D, H, S] }`, three contexts from one.
The sibling shape — opener rebids at the FOUR level, or answers the new suit
with a new suit of his own — is equally empty and wants the same treatment in
a later round.

---
