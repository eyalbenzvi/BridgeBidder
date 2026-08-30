# Expert A (competitive / matchpoint duplicate) — dossier part 4

38 boards, -235 IMPs.  **30 proposals, 8 NOTHING-WRONGs.**  22 proposals were
traced through a patched copy of the system (`load_system()` on a scratch YAML)
and are labelled VERIFIED; the rest are UNTESTED and say so.

## The three agreements that matter most in this slice

1. **There is no way to show a FIT above the cheap raise in any of the four
   generic competitive contexts.**  Every three-level raise rung
   (`cl_raise_*3`, `ballow_raise_*3`, `ch_raise_*3`) carries
   `cheapest_in_suit: true`, so whenever the two-level raise is legal the
   three-level one is not even offered — and there is no cue-bid raise at all,
   although `DECISIONS.md` declares "in competition the cue of their suit is a
   limit raise or better".  A hand with 13+ support points and a real fit has
   exactly two calls available: a 6-12 simple raise, and pass.  Boards **632,
   297, 655, 390, 535** are all this shape, and it is the single biggest hole
   in my slice.  (I prototyped the cue-bid raise itself and it does not pay yet
   — see the NEGATIVE RESULT under board 632.)

2. **Responder's free bid of a new suit over an overcall is `forcing:
   non_forcing`, so opener passes it out** (board 658, `cl_new_H1` and its
   siblings).  The same family — actions our side is entitled to and cannot
   make — supplies boards **758** (no reopening double on shape below 16 HCP),
   **274** (`general_balancing_high` has no penalty double at all), **894**
   (no discriminating weak pass over their takeout double) and **558**.

3. **Obstruction discipline is missing at both ends of the auction.**  No
   preemptive raise of partner's minor over an overcall (**922**); the negative
   double outranks the weak jump shift on a 6-5 hand (**690**, worth 13 IMPs on
   this board alone); no weak two on shape when the suit quality is poor but a
   five-card side suit supplies the tricks (**704**); and the "no preempt with a
   four-card major on the side" veto fires when the preempt is in SPADES, where
   it cannot be preempting past our own major (**425**).

## A mechanism finding that affects every "more descriptive rung" proposal

`prepare_decision` builds the interpretation of a call as an `any_of` over
**every** rule in the winning context that produces it, so partner's shown
minimum is the WEAKEST sibling's promise.  Adding a high-priority
"seven-card suit" rung above a 5-card sibling changes WHAT WE BID and tells
partner **nothing new**: on board 0 `partner_shown_length(H)` came back 5, not
7, and on board 788 `partner_shown_length(S)` came back 4, not 5.  Any proposal
whose value depends on partner READING the new rung must either replace the
sibling or live in its own context.  I have flagged the two proposals of mine
that this bites.

---

## Board 632 — margin -7

**Seat/call that went wrong:** South, call 2 (`1D - (2C) - ?`), `cl_pass`.
Six-card diamond support, a club void, **14 support points** in the raise
context (measured, not estimated) — and the engine passed.

**Missing agreement:** with a genuine nine-plus-card fit and more support points
than the cheap raise can hold, jump to three of partner's suit.

Why the seat is starved: `cl_raise_D2` caps at 12 total points (fit 0.409 here),
`cl_raise_D3` carries `cheapest_in_suit: true` and 2D is the cheap raise so it
is not offered at all, and `cl_raise_D4` wants ten combined trumps (we have 9).
Hole in the ladder ⇒ pass by construction.

```yaml
# context: general_competitive_low, inserted before `- id: cl_raise_C2`
      - id: cl_raise_fit3_$X
        call: 3$X
        priority: 31.5
        when: { partner_suit: $X, cheapest_in_suit: false, we_hold_contract: false }
        requires:
          suits: { $X: [4, 13] }
          evals: { total_points: [13, 40], "lott_total_trumps($X)": [9, 26] }
        shows: "jump raise on the fit: 13+ support points and nine-plus combined trumps - too good for the cheap raise, and the Law says the three level is safe"
        establishes: { forcing: non_forcing, agreed_suit: $X }
```

**Answering seat:** none needed — `forcing: non_forcing`.  Traced anyway:
`1D (2C) 3D (P)` puts opener in `general_uncontested_continuation`, where
`uc_pass` fits 1.00 and he passes with the 13-count.  3D makes 11.

**What it endangers** (every rule in `general_competitive_low` it can outrank):
`cl_raise_$X3` (31, same call, but that rung is unreachable whenever the cheap
raise is legal, which is exactly when mine fires); `cl_raise_$X2` (30 — a
different, weaker hand: mine starts a point above its ceiling); `cl_new_*3(_hi)`
(27/27.5 — a nine-card fit is a better description than a new suit);
`cl_rebid_jump_*` (31 — I have not bid a suit of my own); `cl_nt2`/`cl_nt3`
(28/29 — a 4-13 shape with a void is not a notrump hand).  It does NOT reach
`cl_negative_X1/X2` (33), `cl_takeout_X` (36) or the doubler rungs (33-35).
Fallback risk: 3-of-partner's-suit is already covered in this context by
`cl_raise_$X3`, so no code fallback is deleted.

**VERIFIED.**  Base: `P` (`cl_pass`, fit 1.000).  Patched: `3D`
(`cl_raise_fit3_D`, fit 1.000, prio 31.5).  Regression: `742.Q942.K7642.9`
(9 support points) still bids 2D at `cl_raise_D2` fit 1.000; board 297's North
is unaffected.

**Template:** `expand: { X: [C, D, H, S] }`, and the identical block belongs in
`general_balancing_low`, `general_balancing_high` and `general_competitive_high`
(ids `ballow_raise_fit3_$X`, `balhigh_raise_fit3_$X`, `ch_raise_fit3_$X`) — the
`cheapest_in_suit` blockage is in all four ladders.

### NEGATIVE RESULT — the cue-bid raise, prototyped and NOT shipped

`DECISIONS.md` declares cue-bid raises, and `nx_1m1H_cue`, `nx_1m1S_cue`,
`r1M2x_cue`, `advo_cue` and `adv_cue` all exist — but **no generic competitive
context has one**, so `1D - (2C)` and every other auction that falls through has
no cue at all.  I built it: a new `competitive_cue_raise` context,
`pattern: "... - ?"` (least specific, so it can only ADD a call),
`when: { is_competitive: true, we_hold_contract: false }`,
`expand_pairs` over the 12 (their-suit, partner-suit) pairs, rungs
`call: 2$T` / `3$T` with
`when: { their_last_bid_suit: true, standing_bid_strain: [$T], cheapest_in_suit: true, partner_suit: $M, i_have_acted: false }`
and `establishes: { forcing: one_round, agreed_suit: $M }`.

It fires cleanly (board 632 South bids 3C at fit 1.000).  **The answering seat
then bids 3NT with `T3` in clubs** (`uc_nt3`, fit 0.835 — `weakest_their_stopper`
does not gate), because `uc_raise_D3`'s `lott_total_trumps >= 8` counts partner's
shown minimum of 3 plus opener's own 4 = 7 and scores 0.082.  This is the
round-17 empty-seat pattern exactly: the question exists, the answer does not.
**Do not ship the cue raise until the "partner has agreed MY suit" ladder is
authored** — that is a closed-conversation project, not a rung.

---

## Board 707 — margin -7

**Seat/call:** the FIRST divergence (North passing `1D` on `K64.T765.874.Q65`,
5 HCP with four hearts) is a **constructive** responding decision — `r1m_pass`
is 0-5 and `r1m_1H` is 6+, and this is the "five responding contexts are a
uniform hole" open item.  Not my discipline.

**My competitive observation, call 7:** South holds `9875.A.AKQJ93.A7`
(18 HCP, `total_points` 20, AKQJ93) and, after partner passed and RHO reopened
with a takeout double, rebid **2D** at `xd_rebid_D2`.  There is no way to show
extras: `xd_rebid_D3` is doubly blocked — `cheapest_in_suit: true` (2D is the
cheap rebid) and `lott_total_trumps(D) >= 9` counting a partner who has shown
nothing.

**Missing agreement:** over their double, when partner has passed my opening,
the JUMP rebid of a self-sufficient six-card suit shows the extras his pass
denied.

```yaml
# context: general_their_double, inserted before `- id: xd_raise_C2`
      - id: xd_rebid_jump_$X
        call: 3$X
        priority: 35
        when: { we_bid_last: true, my_suit: $X, cheapest_in_suit: false, partner_has_acted: false }
        requires:
          suits: { $X: [6, 13] }
          evals: { total_points: [17, 40], "suit_quality($X)": [1.5, 9] }
        shows: "jump rebid of my own doubled $X: a self-sufficient six-card suit and 17+ - the extras partner's pass denied"
        establishes: { forcing: non_forcing }
```

**Answering seat:** none — non-forcing, and it describes a hand partner already
knows the shape of.

**What it endangers:** `xd_rebid_$X3` (34, same call — mine is the reachable
version of it and starts three points above `xd_rebid_$X2`'s floor);
`xd_rebid_$X2` (34 — 11+ with the same six cards, a genuinely weaker hand);
`xd_raise_*`/`xd_jumpraise_*` (30-32 — I am rebidding my own suit, not raising
partner's, and `my_suit` makes the two disjoint); `xd_second_*`/`xd_run_*`
(24-26); `xd_XX_extras` (23 — with a solid six-card suit, naming trumps beats
announcing strength, which is the comment already in the file).  3-of-my-own-suit
is covered by `xd_rebid_$X3`, so no fallback is deleted.

**VERIFIED** for the call: base `2D`, patched `3D` (`xd_rebid_jump_D`, fit
1.000).  Regression: a 12-count with the same shape still bids 2D (mine fits
0.409).  **Honest note: this is worth 0 IMPs on board 707** — 2D+2 and 3D+1 are
both +130.  The board is lost in the constructive responding seat.

**Template:** `expand: { X: [C, D, H, S] }`.

---

## Board 758 — margin -7

**Seat/call:** North, call 6 — `1D - (1H) - P - (P) - ?` with
`AQ95.Q8.6532.AQ2`, 14 HCP, a doubleton in their suit and three-plus cards in
every unbid suit.  We bid **1NT** (`ballow_nt1`, fit 0.965 on a `Q8` "stopper").

**Missing agreement:** the opener's REOPENING DOUBLE on opening values — the
file only has one at 16+ (`ballow_reopen_X`), and `ballow_X` is switched off by
`side_has_acted: false` once we have opened.

```yaml
# context: general_balancing_low, inserted before `- id: ballow_X`
      - id: ballow_reopen_X_shape
        call: X
        priority: 39
        when: { their_last_bid_suit: true, side_has_acted: true, we_bid_last: false,
                my_last_call_was_double: false, we_hold_contract: false }
        requires:
          hcp: [11, 15]
          evals: { max_their_suit_length: [0, 2], weakest_unbid_length: [3, 13], longest_suit_length: [0, 5] }
        shows: "reopening double on shape: opening values, at most a doubleton in their suit and three-plus cards in every unbid suit"
        establishes: { forcing: one_round }
```

**THE ANSWERING SEAT — and it needed repair too.**  `advance_reopening_double`
(`1$o - bid - P - P - X - P - ?`) exists, but **it has no one-level advance**:
`adreo_suit_S_$o` is `call: 2S` with `cheapest_in_suit: true`, and over a 1H
overcall the cheapest spade bid is 1S, so the rung is unreachable and South's
five spades came out as **2C**.  The proposal ships with the missing rungs:

```yaml
# context: advance_reopening_double, inserted before `- id: adreo_suit_C_$o`
      - id: adreo_suit_S1_$o
        call: 1S
        priority: 59
        when: { unbid_suit: S, cheapest_in_suit: true }
        requires: { suits: { S: [4, 13] }, evals: { total_points: [0, 8] } }
        shows: "cheapest advance of the reopening double: 0-8"
        establishes: { forcing: non_forcing }
      - id: adreo_suit_H1_$o
        call: 1H
        priority: 58
        when: { unbid_suit: H, cheapest_in_suit: true }
        requires: { suits: { H: [4, 13] }, evals: { total_points: [0, 8] } }
        shows: "cheapest advance of the reopening double: 0-8"
        establishes: { forcing: non_forcing }
      - id: adreo_suit_D1_$o
        call: 1D
        priority: 56
        when: { unbid_suit: D, cheapest_in_suit: true }
        requires: { suits: { D: [4, 13] }, evals: { total_points: [0, 8] } }
        shows: "cheapest advance of the reopening double: 0-8"
        establishes: { forcing: non_forcing }
```

**What it endangers** — priority 39 is deliberately BELOW `ballow_reopen_X`/`X2`
(41) and `ballow_X` (40) so the strong and the pass-out-seat doubles stay
primary.  It outranks: `ballow_nt2_balance` (33), `ballow_raise_*` (30-32 — I
have no fit, that is why I am doubling), `ballow_rebid_*` (29), `ballow_nt3/2/1`
(29/28/27 — a 4-2-4-3 fourteen with `Q8` in their suit is not a notrump hand),
and all the natural suit rungs (25-27 — I have no five-card suit, by gate).
X is already covered in this context, so no fallback is deleted.  The 1-level
advances outrank nothing: they fill empty calls.

**VERIFIED.**  Base: North bids `1NT`, South then answers `2C`.  Patched: North
`X` (`ballow_reopen_X_shape`, fit 1.000), South `1S` (`adreo_suit_S1_D`, fit
1.000).  N/S make nine tricks in spades; the table played 2H by East for -170.

**Template:** the double: none needed (no suit in it) — but the identical rung
belongs in `general_balancing_high` as `balhigh_reopen_X_shape` gated
`standing_bid_level: [2]` (its 16+ sibling is capped at level 3 for good
reasons).  The advances: already `expand: { o: [C, D, H, S] }`.

---

## Board 788 — margin -7

**Seat/call:** North, call 4 — `(P) 1H X (P) ?` with `KJ986.986.AT5.54`,
five spades and 8 HCP (9 total points).  We bid **1S** (`advH_1S`, 0-8);
`advH_2S_jump` demands 9-11 HCP and missed by one, fit 0.800.

**Missing agreement:** the advance of a takeout double is measured in SUPPORT
points against a partner who has promised three-plus cards, so a fifth trump is
worth the jump.

```yaml
# context: advance_takeout_double_suits_H, before `- id: advH_2S_jump`
      - id: advH_2S_jump5
        call: 2S
        priority: 60.5
        requires: { suits: { S: [5, 13] }, evals: { total_points: [7, 11] } }
        shows: "jump advance on a fifth trump: 5+ spades and 7-11 support points opposite a double that promised support"
        establishes: { forcing: invitational }
```

**THE ANSWERING SEAT:** the jump is `invitational`, and it is answered by rungs
that already exist — `uc_raise_S3`/`uc_raise_S4` (31/32) in
`general_uncontested_continuation` when RHO passes, `cl_raise_S3`/`S4` when he
competes.  Traced: South (`AQT5.Q2.Q963.KQ2`, 15 HCP) bids **4S** at
`uc_raise_S4`.  That is one level too high on this layout (nine tricks); the
cause is `rule_of_26` reading partner's shown minimum as 7 and still fitting —
an existing ceiling problem in `uc_raise_S4`, not a defect of the new rung, but
it caps the gain at about +1 IMP instead of +6.  **This is one of the two
proposals bitten by the `shows`-union mechanism** (`partner_shown_length(S)`
comes back 4, not 5, because `advH_2S_jump` shares the call).

**What it endangers:** `advH_2S_jump` (60, same call, 4+ and 9-11 — mine is the
five-card version and the two overlap only at 9-11 with five, where they mean
the same thing); `adv_1NT` (55) and `adv_2NT` (56) — with five spades opposite a
takeout double, notrump is the wrong strain; `advH_1S`/`advH_2D`/`advH_2C`
(50-54, the 0-8 forced advances — mine starts at 7 support points, so the
overlap is the 7-8 band with a FIFTH trump, where the jump is the better
description); `adv_cue` (75) and `adv_pass_penalty` (30) are untouched (higher /
different shape).  2S is already covered, so no fallback is deleted.

**VERIFIED.**  Base `1S`; patched `2S` (`advH_2S_jump5`, fit 1.000).
Regressions: a four-card six-count still bids 1S; a five-card three-count still
bids 1S (mine fits 0.409).

**Template:** the same rung in all four advance contexts —
`advC_2H_jump5`/`advC_2S_jump5`, `advD_2H_jump5`/`advD_2S_jump5`, `advH_2S_jump5`,
`advS_3H_jump5`; plus the three-level minor versions those contexts lack
entirely (a five-card minor advance has no jump at all).

---

## Board 894 — margin -7

**Seat/call:** North, call 2 — `1D (X) ?` with `JT9.J853.J.J9874`, **4 HCP**.
We bid **2C** at `xd_run_C2` ("running to my own C: 5+ cards", no point floor,
priority 25 in `general_their_double`, which outranks `rdx_pass` at 20 in the
more specific `resp_1x_over_X`).

**Missing agreement:** over their takeout double of partner's opening, a bust
passes — the run is for a misfit that has somewhere better to go, and a
two-level bid on 4 HCP hands them a free description of the whole deal.

```yaml
# context: resp_1x_over_X, inserted before `- id: rdx_pass`
      - id: rdx_pass_weak
        call: P
        priority: 27
        requires:
          hcp: [0, 5]
          evals: { total_points: [0, 6], longest_suit_length: [0, 5] }
        shows: "too weak to act over their takeout double: partner is still there and will reopen - running to a five-card suit at the two level on a bust only helps them find their fit"
        establishes: { forcing: non_forcing }
```

**Answering seat:** none — it is a pass.  Note the placement: an identical rung
in `general_their_double` does NOT work, because `resp_1x_over_X` is more
specific and already covers `P`, so the generic one is skipped by the
`covered` set.  (I tried it; that is why the rule is where it is.)

**What it endangers:** `xd_run_$X1/2/3` (24-26 — a run needs a hand worth
playing somewhere, and the six-card floor is preserved by
`longest_suit_length: [0, 5]`); `xd_second_$X*` (24-26); `rdx_pass` (20, same
call, strictly more general).  It does NOT reach `rdx_XX` (75), `rx_D_*`
(58-62) or the Jordan rungs — all of which need real values and outrank it.
**Guardrail check:** this is a *discriminating* authored pass, which
`score_candidates` will accept even when pass is forbidden.  It is gated to
0-5 HCP, so the only forces it could convert are ones partner made opposite a
known bust; and after a takeout double of our opening no force from partner is
outstanding.

**VERIFIED.**  Base `2C`; patched `P` (`rdx_pass_weak`, fit 1.000).
Regressions: the same shape with 8 HCP still bids 2C; a 4-HCP hand with SEVEN
clubs still runs to 2C (`longest_suit_length` gate).

**Template:** already inside `expand: { o: [C, D, H, S] }`.  A sibling belongs
in `resp_over_double_C/D/H/S` if those contexts ever grow a run.

---

## Board 922 — margin -7

**Seat/call:** North, call 2 — `1D (1S) ?` with `2.T6.98764.KQ832`,
5 HCP, **five-card diamond support and a singleton spade**.  `nx_1m1S_pass`
fit 1.000; `nx_1m1S_raise` (2D, 6-10) fit 0.800.  BEN bids 3D.

**Missing agreement:** `resp_1m_over_1H` and `resp_1m_over_1S` have a simple
raise, a cue-raise and a weak jump shift, but **no preemptive raise** — the
commonest competitive call there is.

```yaml
# context: resp_1m_over_1S (and resp_1m_over_1H), before `- id: nx_1m1S_1NT`
      - id: nx_1m1S_preempt
        call: 3$m
        priority: 56
        requires:
          suits: { $m: [5, 13] }
          evals: { total_points: [3, 9], "lott_total_trumps($m)": [8, 26], max_their_suit_length: [0, 1] }
        shows: "preemptive raise: five-card support, a singleton or void in their suit, less than a constructive raise - the Law level, bid at once"
        establishes: { forcing: non_forcing, agreed_suit: $m }
```

**Answering seat:** none — non-forcing and self-limiting.  Traced:
`1D (1S) 3D (P)` leaves South on `uc_pass` with the 18-count, which is right
here (3D makes ten).

**What it endangers:** `nx_1m1S_raise` (55, 2D on 4+ and 6-10 — mine needs a
fifth trump AND a singleton in their suit AND fewer points, so the two are
nearly disjoint and mine is the better description when both fit);
`nx_1m1S_1NT` (50 — a singleton in their suit is not a 1NT hand);
`nx_1m1S_wj_H` (56, same priority, different call and a hand with six hearts);
`nx_1m1S_pass` (20).  It does NOT reach `nx_1m1S_X` (80), `nx_1m1S_2H` (78) or
`nx_1m1S_cue` (70) — all of which promise more.  3-of-the-minor is NOT otherwise
covered in this context, so the code fallback for `3D` is suppressed wherever
the `when` reaches; the `when` here is only "partner opened this minor and they
overcalled 1S", and the fallback layer for a jump in partner's minor is the one
we are replacing.

**VERIFIED.**  Base `P`; patched `3D` (`nx_1m1S_preempt`, fit 1.000).
Regression: the same hand with only four diamonds still passes / raises to 2D.

**Template:** `expand: { m: [C, D] }` in both `resp_1m_over_1H` and
`resp_1m_over_1S`; the major analogue belongs in `resp_1H_over_1S` and
`resp_1M_over_2x` as a jump raise to the level of the fit.

---

## Board 988 — margin -7

**Seat/call:** South, call 10 — `P P 1H (X) 2H (2S) 3H (3S) P P ?` with
`76.KT9863.AK5.K4`.  We bid **4H** (`balhigh_rebid_H4`, fit 1.000) for -200.

**Missing agreement:** partner has already passed their three-level bid holding
the limit raise he showed; the four level is his decision, and I have no
unshown trump or shape to justify overruling him.

```yaml
# context: general_balancing_high, inserted before `- id: balhigh_raise_C2`
      - id: balhigh_pass_declined_$X
        call: P
        priority: 29.5
        when: { my_suit: $X, we_bid_last: false, partner_has_acted: true, i_have_acted: true,
                their_last_bid_suit: true, standing_bid_level: [3], we_hold_contract: false }
        requires:
          suits: { $X: [0, 6] }
          evals: { total_points: [0, 16] }
        shows: "partner has already passed their three-level bid holding the values he showed: the four level is his decision, and I have no unshown seventh trump and no extra values"
        establishes: { forcing: non_forcing }
```

**Answering seat:** none — it is a pass, and it ends the auction.

**What it endangers:** `balhigh_rebid_$X4` (29, the rung that fired — mine sits
half a point above it and describes the same hand better once partner has
declined); `balhigh_rebid_$X3`/`new_$X4`/`nt3` (29/28/29); `balhigh_new_*`
(25-27).  It sits BELOW every raise rung (`balhigh_raise_*` 30-32) on purpose:
a hand with a genuine fit for PARTNER's suit is a different animal and should
still bid.  It is also below `balhigh_X`/`reopen_X` (40/41) and my board-274
penalty double (42), so defending doubled stays available.
**Guardrail check:** a discriminating pass can convert a force.  The gates
require the STANDING bid to be theirs at the three level and that I have already
acted, so partner's last call is a pass and no force of his is outstanding.

**VERIFIED.**  Base `4H` (`balhigh_rebid_H4`, fit 1.000); patched `P`
(`balhigh_pass_declined_H`, fit 1.000, prio 29.5).  -140 instead of -200.

**Template:** `expand: { X: [C, D, H, S] }`, plus the `general_balancing_low`
twin `ballow_pass_declined_$X` with `standing_bid_level: [2]`.  (It does NOT
reach board 713: there partner never acted, so `partner_has_acted: true` fails —
713 gets its own finding.)

---
