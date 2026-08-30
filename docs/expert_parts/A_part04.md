# Expert A (competitive / matchpoint duplicate) — dossier part 4

38 boards, -235 IMPs.  **30 proposals, 8 NOTHING-WRONGs.**  23 proposals were
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

## Board 0 — margin -6

**Seat/call:** West, call 3 — `2D (P) (P) ?` with `K83.KJ98742.6.KT`,
**seven hearts**, 10 HCP.  We doubled (`ballow_X`, priority 40, which outranks
every natural bid in the context at 25-33).

**Missing agreement:** in the balancing seat a SEVEN-card suit names its own
trumps; the takeout double asks partner to choose among three suits I do not
hold.

(This is deliberately not the idea round 7 killed with whole-corpus data — that
was "a takeout double must not hide a SIX-card suit", and doubles with 6+ suits
measured *better* than those without.  Seven is a different animal and the rung
is additive, not a gate: `ballow_X` keeps every hand it has now except the
seven-card one-suiters.)

```yaml
# context: general_balancing_low, inserted before `- id: ballow_raise_C2`
      - id: ballow_new_long7_$M
        call: 2$M
        priority: 42
        when: { unbid_suit: $M, cheapest_in_suit: true }
        requires: { suits: { $M: [7, 13] }, evals: { total_points: [8, 40], "suit_quality($M)": [1, 9] } }
        shows: "natural $M in the balancing seat with a SEVEN-card suit: a one-suiter names its own trumps - the double would ask partner to pick a suit I do not hold"
        establishes: { forcing: non_forcing }
```

**Answering seat:** none required (non-forcing).  **But see the negative result
below** — the follow-up is where this board is actually lost.

**What it endangers:** `ballow_X` (40) and `ballow_reopen_X`/`X2` (41) — on a
seven-card suit, naming trumps beats asking; `ballow_nt2_balance` (33),
`ballow_nt2_strong` (30), `ballow_raise_*` (30-32 — mine requires the suit to be
UNBID, so it cannot be partner's), `ballow_rebid_*` (29 — `unbid_suit` also
excludes a suit I have bid myself), `ballow_new_$M2`/`long2_$M` (26, same call,
5+/6+ — mine is the seven-card version and strictly narrower).  2$M is already
covered, so no fallback is deleted.

**VERIFIED** for the call: base `X`; patched `2H` (`ballow_new_long7_H`,
fit 1.000).  Regression: the same hand with only six hearts still bids 2H via
the ordinary `ballow_new_H2` at priority 26 (i.e. the double no longer wins, but
that was already true — `ballow_X` fits and outranks it; my rung leaves the
six-card case exactly as it was).

### NEGATIVE RESULT on the same board — the `shows`-union ceiling

I then tried to close the conversation with an answering rung
(`uc_raise_long3_$M`: raise partner's KNOWN 6+ suit on a doubleton to the level
of the fit, priority 31.5, `partner_shown_length($M) >= 6`,
`lott_total_trumps($M) >= 9`).  It scored **fit 0.000**, because
`partner_shown_length(H)` comes back **5**: the interpretation of `2H` is an
`any_of` over `ballow_new_H2` (5+), `ballow_new_long2_H` (6+) and my new rung
(7+), and partner's shown minimum is the weakest of them.  East therefore bids
2NT and we play 2NT instead of 4H making eleven.  **A high-priority "long suit"
rung changes what we bid and tells partner nothing**; to make the seven-card
balancing overcall pay, it has to be its own call in its own context (a jump, or
a separate balancing-2NT-style scheme), not a rung sharing 2$M with two weaker
siblings.  Reported, not shipped as a closed conversation.

**Template:** `expand: { M: [H, S] }` here; the minor twin needs the three-level
call and is not worth it in the balancing seat.  Same rung in
`general_balancing_high` as `balhigh_new_long7_$M` at `call: 3$M`.

---

## Board 55 — margin -6

**Seat/call:** South, call 7 — `P P 1S P 1NT P (2C) ?` with
`Q86.K4.A87652.98`, 9 HCP, `A87652`, **vulnerable**, both opponents bidding and
partner silent.  We bid **2D** (`cl_new_long2_D_hi`, "a SIX-card suit, 8+
points" — no suit-quality gate, no vulnerability gate) and ended in 3D for -200.

**Missing agreement:** this is the sandwich position one round later — both
opponents have bid and partner has passed — and `sandwich_seat` has exactly the
discipline that is missing here (`sw_2C`: "good 5+ clubs, **11-17**"), but the
auction has fallen through to `general_competitive_low`, which has none.

```yaml
# context: general_competitive_low, inserted before `- id: cl_pass`
      - id: cl_pass_live_auction
        call: P
        priority: 26.75
        when: { side_has_acted: false, i_have_acted: false, we_vulnerable: true,
                standing_bid_level: [2], we_hold_contract: false }
        requires:
          hcp: [0, 10]
          evals: { quick_tricks: [0, 1.5], longest_suit_length: [0, 6] }
        shows: "both opponents have bid and my partner has passed: vulnerable, a ten-count with fewer than two quick tricks defends rather than entering at the two level"
        establishes: { forcing: non_forcing }
```

**Answering seat:** none — it is a pass, and `side_has_acted: false` means no
force of ours is outstanding.

**What it endangers:** `cl_new_$X2`/`_hi` and `cl_new_long2_$X`/`_hi`
(26/26.5 — the two-level entry into a live auction, which is exactly what it is
meant to demote, and only when vulnerable with fewer than two quick tricks);
`cl_new_$X1` (25); `cl_pass` (20, same call, strictly more general).  It sits
BELOW `cl_new_*3` (27), `cl_nt1` (27), `cl_nt2` (28), every raise (30+) and every
double (33+), so a fit, a stopper or real values still act.

**VERIFIED.**  Base `2D`; patched `P` (`cl_pass_live_auction`, fit 1.000).
Regression: `Q86.KQ.AK7652.98` (2.5 quick tricks) still bids 2D.

**Template:** none over suits (the rule names no suit).  The honest expansion is
over the vulnerability/level pair: a `we_vulnerable: false` twin with a lower
HCP ceiling is *not* recommended — non-vulnerable, entering is right.  A
`standing_bid_level: [1]` twin is also not recommended: the one-level overcall
is cheap.  **Do not template this one; it is the vulnerable two-level case only.**

---

## Board 83 — margin -6 — NOTHING-WRONG (competitive)

Par is **-800**: East/West were always making game and N/S have no save.  Our
side (N/S at table A) passed throughout on 19 combined HCP; I checked every one
of those passes.  `oc1S_pass` (North, 8 HCP, no five-card suit, `98` in their
suit) is right; `sw_pass` for South after `1S P 1NT` on `K74.AQT8.Q7652.3`
matches BEN; `cl_pass`, `ch_pass` and `balhigh_pass` over 2C/3C/3S/4S are all
right at these colours.  The first divergence is West's constructive rebid over
a semi-forcing 1NT (`ob_1M1NT_2S` versus BEN's 2C) — opener's rebid ladder, not
my discipline.

---

## Board 93 — margin -6 — NOTHING-WRONG (competitive)

The first divergence is East's opening decision on `KT98.T543.A.A765`
(11 HCP, rule of 20 = 19) — **opening-style / rule-of-20 thresholds are
scope-excluded**.  Competitively: at table A South's 1NT overcall on a
15-count over 1C is right; North's three passes over 2S/3S/4S on
`3.62.97642.KJ984` are right (par -650, and a 4-HCP hand with a singleton
spade has no call over their spade auction); South's pass of 4S holding
`QJ.AQJ8.KT53.QT2` behind the 1C opener is right — a penalty double needs
trump tricks, not high cards.  Nothing to propose.

---

## Board 116 — margin -6

**Seat/call:** East, call 1 at table B — `(1H) ?` with `A873.T.Q32.A9643`:
10 HCP, a **singleton** in their suit, four spades, five clubs, three
diamonds.  We passed (`oc1H_pass`); `oc1H_X` fit 0.800 (its band is 11-16).
The auction then needed two more rounds and a balancing double to reach 3S.

**Missing agreement:** shape substitutes for the missing point — a takeout
double with a singleton in their suit and three-plus cards in every other suit
is a 10-count action, not an 11-count action.

```yaml
# context: overcalls_of_1H, inserted before `- id: oc1H_1S`
      - id: oc1H_X_shape
        call: X
        priority: 71.5
        requires:
          hcp: [10, 11]
          suits: { H: [0, 1] }
          evals: { weakest_unbid_length: [3, 13], longest_suit_length: [0, 5] }
        shows: "takeout double on shape: 10-11 with a singleton or void in their suit and three-plus cards in every unbid suit - the shape is worth the missing point"
        establishes: { forcing: one_round }
```

**THE ANSWERING SEAT:** already authored and complete —
`advance_takeout_double[H]` plus `advance_takeout_double_suits_H` (forced
cheapest suit 0-8, jumps 9-11, 1NT/2NT with a stopper, cue GF, penalty pass).
No new answering rungs needed; this is why I am willing to widen a double.

**What it endangers:** `oc1H_X` (72 — deliberately left above, so the 11-16 and
17+ doubles stay primary and mine only fires where the main rung misses);
`oc1H_1S` (71 — with only four spades I have no overcall, and the gate
`longest_suit_length: [0, 5]` keeps a genuine six-card suit out); `oc1H_2C`
(65 — five clubs and 10 HCP is under that rung's floor of 11 anyway);
`oc1H_3m_jump`/`oc1H_3C_preempt` (58/59 — I have opening shape, not a preempt);
`oc1H_pass` (25).  X is already covered, so no fallback is deleted.
**Risk to state plainly:** this widens the takeout double by one point over
every 1M/1m opening once templated, which is a real blast radius; the singleton
and the three-cards-everywhere gates are what keep it honest.

**VERIFIED** for the call: base `P`; patched `X` (`oc1H_X_shape`, fit 1.000).
Regression: the same hand with a DOUBLETON heart passes (mine fits 0.349).
I did NOT simulate the rest of the auction (West holds 15 HCP with five hearts
behind the opener and may convert for penalties), so the IMP effect is unproven.

**Template:** the identical rung in `overcalls_of_1C`, `overcalls_of_1D`,
`overcalls_of_1S` (`oc1C_X_shape`, `oc1D_X_shape`, `oc1S_X_shape`), with
`suits: { C: [0,1] }` etc.

---

## Board 132 — margin -6 — NOTHING-WRONG (competitive)

Uncontested at both tables.  The divergence is West's rebid on
`AK62.AQT987.K62.` after `1D - 1H - 2C`: `r1d1h2c_3H` ("6+ hearts,
invitational or better") versus BEN's 2S, i.e. the missing **reverse / fourth
suit showing the second suit before repeating the first**.  That is
constructive-auction machinery and belongs to the other reviewer.  Nothing our
side could have done competitively: E/W were never opposed.

---

## Board 188 — margin -6

**Seat/call:** North, call 4 — `1H (2D) 2H (P) ?` with `.AQ843.K92.KQJ83`.
We bid **4H** (`uc_raise_H4`, fit 1.000) for -100; 3H makes nine.

**Missing agreement:** at exactly eight or nine trumps, with no fit shown their
way, the Law says three — the four-level raise is a total-trick bid and
without a known fit on their side the trick count does not support it.  (And
the five points that took this hand over `uc_raise_H4`'s bar are a VOID in a
suit nobody has bid, opposite a partner whose values may be sitting in it.)

Note also that `uc_raise_H4` is deciding a *competitive* auction from
`general_uncontested_continuation` — the confirmed open item — and that its
competitive twin `cl_raise_lott4_H` carries `their_fit >= 8`, the Law gate the
file says was learned the hard way.  This rung ports that discipline.

```yaml
# context: general_uncontested_continuation, before `- id: uc_raise_H4`
      - id: uc_raise_law3_$M
        call: 3$M
        priority: 33
        when: { partner_suit: $M, is_competitive: true, cheapest_in_suit: true, we_hold_contract: false }
        requires:
          hcp: [12, 17]
          suits: { $M: [3, 13] }
          evals: { "lott_total_trumps($M)": [8, 9], their_fit: [0, 7] }
        shows: "the Law at the three level: eight or nine trumps our way, no fit shown their way, and my values are high cards rather than a void in a suit nobody has bid - invite, do not bid the game"
        establishes: { forcing: invitational, agreed_suit: $M }
```

**THE ANSWERING SEAT:** `invitational`, answered by rungs already present —
`uc_raise_$M4` (32) accepts, `uc_pass` (18) declines.  Traced: South
(`K964.J92.43.AT64`, 8 HCP) passes at `uc_pass` fit 1.000 and we play 3H making
nine.

**What it endangers:** `uc_raise_$M4` (32 — the game raise, which is the point:
it is demoted only at 8-9 trumps with 12-17 HCP and no fit shown their way);
`uc_raise_$M3` (31, same call, more general); `uc_rebid_$M3` (29);
`uc_new_*3(_hi)` (27/27.5); `uc_nt2`/`uc_nt3` (28/29).  It does NOT reach
`gst_rkc_$M` (46) or anything in `general_slam_try`.  3$M is already covered by
`uc_raise_$M3`, so no fallback is deleted.

**VERIFIED.**  Base `4H`; patched `3H` (`uc_raise_law3_H`, fit 1.000, prio 33).
Regressions, all still `4H` or better: a 10-trump hand (`lott` 10, outside
[8,9]); a 19-HCP hand (outside [12,17], and it finds `gst_rkc_H`).

**Template:** `expand: { M: [H, S] }` — majors only, because at the minors the
"four level" is not game and `uc_raise_$m4` already carries a ten-trump gate.

---

## Board 191 — margin -6

**Seat/call:** South, call 3 — `1D (P) 1S ?` (sandwich seat) with
`Q.T8432.A2.AKQT8`: **5-5 in hearts and clubs**, 15 HCP, a singleton spade.
We doubled (`sw_X`, priority 70) and finished in a 4C/4D muddle for -150.

**Missing agreement:** with 5-5 you bid your suits; the sandwich double is the
hand with support for BOTH unbid suits, and I have length in only two of the
three.

```yaml
# context: sandwich_seat, inserted before `- id: sw_1S`.  The context already
# carries `expand: { o: [C, D, H, S] }`, so a second context-level expansion is
# impossible: the six two-suit combinations are written out.  Shown for one
# pair; the other five are identical with the suit letters swapped.
      - id: sw_two_suiter_CH
        call: 2C
        priority: 71
        when: { unbid_suit: C, cheapest_in_suit: true }
        requires:
          suits: { C: [5, 13], H: [5, 13] }
          hcp: [11, 17]
          evals: { "suit_quality(C)": [1, 9] }
        shows: "sandwich overcall with a 5-5 two-suiter: bid the LOWER suit first and show the second next round - the double asks partner to guess among three suits and I hold only two of them"
        establishes: { forcing: non_forcing }
```

The six ids are `sw_two_suiter_CD`, `_CH`, `_CS`, `_DH`, `_DS`, `_HS`; the call
is always two of the LOWER suit, so the higher one is still available cheaply.

**Answering seat:** none new — non-forcing, advanced by `advance_overcall` /
the generic competitive rungs, exactly as an ordinary `sw_2C` is.

**What it endangers:** `sw_X` (70 — the whole point; the double keeps every
hand that is not 5-5); `sw_1S`/`sw_1H` (68); `sw_2*` (66, same calls, 5+ and
11-17 — mine is the 5-5 version and strictly narrower); `sw_2*_jump` (69) and
`sw_3*` (69.5 — those are preemptive shapes with fewer values); `sw_pass` (30).
2$L is already covered by `sw_2$L`, so no fallback is deleted.

**VERIFIED.**  Base `X` (`sw_X`, fit 1.000, prio 70); patched `2C`
(`sw_two_suiter_CH`, fit 1.000, prio 71); `sw_2C` stays at 66 beneath it.
Honest caveat: BEN's choice here is 2D, a Michaels cue, which is scope-excluded;
my rung reaches the same hand type by a route the system already speaks, and I
did not simulate the rest of the auction (partner holds six spades and three
hearts, so the 2C advance may still land badly).

**Template:** six written-out rules (see above) — the context's existing
`expand: { o: [C, D, H, S] }` blocks a second context-level expansion, and
`unbid_suit` keeps each rule out of the auctions where its suit has been bid.
The same six belong in `general_competitive_low` as `cl_two_suiter_*` for the
live auctions the sandwich context does not own.

---

## Board 247 — margin -6

**Seat/call:** South, call 3 — `(P) 1D (2S) ?` with `QT653.AQJ8.Q2.64`:
11 HCP and **five of their trumps**.  We doubled (`nxj_X`, priority 70, whose
whole constraint is `hcp: [8, 40]`).  North then had to guess and pulled to 3D
for -100.

**Missing agreement:** the trap pass.  With five of their trumps a negative
double is the one call that cannot be right — it asks partner to bid the suit I
want to defend in.  Pass, let partner reopen, and convert.

This is deliberately NOT the round-14 gate on `nxj_X` that measured -5 held out
(a longest-suit cap plus a four-card-unbid-major requirement).  It is a landing
seat — which is exactly what the file's own comment on `nxj_X` asks for
("author the landing seats first") — and its gate is five cards in THEIR suit,
counted, not a shape veto.

```yaml
# context: neg_double_3level_m, inserted before `- id: nxj_pass`
      - id: nxj_pass_trap
        call: P
        priority: 71
        requires:
          hcp: [8, 40]
          evals: { standing_suit_length: [5, 13] }
        shows: "trap pass: FIVE of their trumps sitting over the jump overcall - partner reopens and I convert, and a double asking him to bid my trumps is the one call that cannot be right"
        establishes: { forcing: non_forcing }
```

**THE ANSWERING SEAT — and it is board 758's rung.**  A trap pass is worthless
without a reopening double, and `ballow_reopen_X` needs 16+, so North (11 HCP)
would pass it out.  With `ballow_reopen_X_shape` (board 758) in place the
conversation closes end to end, traced:

* South `P` (`nxj_pass_trap`, fit 1.000)
* North `X` (`ballow_reopen_X_shape`, fit 1.000) on `9.T52.KJT86.AQJ5`
* South `P` (`adreo_pass_penalty_D`, fit 1.000 — the penalty-pass rung that was
  already there and had nothing to convert)

2S doubled, seven tricks, +100 to us against the -100 we scored.  Par is +120.

**What it endangers:** `nxj_X` (70 — only on the five-trump shape); nothing else
in the context (only `nxj_pass` at 20 is below it, same call).  Because
`neg_double_3level_m` is the most specific live context, it also blocks
`cl_pass`, but `P` is covered there anyway.  **Guardrail check:** the pass is
discriminating and could in principle convert a force — but partner's opening
bid is not a force on responder in this system, and the rung requires five cards
in the standing bid's suit.

**VERIFIED.**  Base `X`; patched `P`.  Regressions: four trumps still doubles
(mine fits 0.349); a doubleton still doubles.

**Template:** the identical rung belongs in `neg_double_3level_M` (`nx3_pass_trap`
at priority 72, above `nx3_cue`'s 71) and in `general_competitive_low` /
`general_competitive_high` as `cl_pass_trap` / `ch_pass_trap` above the negative
doubles at 33.

---

## Board 267 — margin -6 — NOTHING-WRONG (competitive)

Uncontested at both tables: `P P P 1NT P 2D P 2H P ?`.  The divergence is
North's transfer follow-up on `Q972.QT987.T83.K2`-shaped hand
(`Q972.QT987.K2.53`): five hearts AND four spades, and `nt_after_transfer` has
no natural second-suit rung, so responder must choose between `tr_pass_weak` and
an invitation.  That is the constructive item already named in
`docs/ROUND_METHOD.md`'s open list; it belongs to the other reviewer.

Competitively: E/W hold 17 HCP and never balanced over `2H`.  I checked —
`cl_pass` is right for East over 2D and 2H (`KT53.K2.T763.K62`: no five-card
suit, no shortness in either major, and balancing over a *completed transfer*
walks into a 15-17 opener on your left).  Nothing to propose.

---

## Board 272 — margin -6

**Seat/call:** South, call 2 — `(P) (1D) ?` with `KJ972.JT976.A7.T`:
**exactly 5-5 in the majors**.  We overcalled **1H**.

**Missing agreement:** with 5-5 you bid the HIGHER suit first, so the second one
is available at the cheapest level next time.  `oc1D_1H` and `oc1D_1S` are both
priority 71 and both fit 1.000, so the tie broke on call rank and the lower suit
won — **the identical defect the file already fixed for `r1m_1H`/`r1m_1S` in
round 10 and for `cl_new_H1` afterwards** (the comment on `cl_new_H1` says so in
so many words); the overcall ladder was never swept.

```yaml
# context: overcalls_of_1D, inserted before `- id: oc1D_1S`
      - id: oc1D_1S_55
        call: 1S
        priority: 71.5
        requires:
          suits: { S: [5, 13], H: [5, 13] }
          hcp: [8, 16]
          evals: { "suit_diff(S,H)": [0, 13], "suit_quality(S)": [1, 9] }
        shows: "overcall with 5-5 in the majors: bid the HIGHER suit first so the auction has room for the second"
        establishes: { forcing: non_forcing }
```

(The additive form is used rather than adding `"suit_diff(H,S)": [1, 13]` to
`oc1D_1H`, because a gate on `oc1D_1H` subtracts the 6-5 hands that genuinely
belong in hearts.)

**Answering seat:** none — the overcall's advances are already authored
(`advance_overcall`, `advance_1NT_overcall`, the `cl_*` ladder in competition).

**What it endangers:** `oc1D_1H` (71 — only on exactly-equal or spade-longer
major two-suiters, where spades is the right suit); `oc1D_1S` (71, same call,
strictly more general); `oc1D_2C`/`2D`/`2H` (65) and the jump overcalls (below),
none of which describe a 5-5 major two-suiter; `oc1D_pass` (25).  1S is already
covered, so no fallback is deleted.

**VERIFIED.**  Base `1H`; patched `1S` (`oc1D_1S_55`, fit 1.000, prio 71.5).

**Template:** the same rung in `overcalls_of_1C`, `overcalls_of_1D` and (as a
2S-over-1H rung) `overcalls_of_1H`: `oc1C_1S_55`, `oc1D_1S_55`, `oc1H_2S_55`.
The sandwich and balancing ladders need it too — `sw_1S`/`sw_1H` are both 68 and
`ballow_new_S1`/`ballow_new_H1` are both 25, so both tie-break to hearts.

---

## Board 274 — margin -6

**Seat/call:** North, call 6 — `1D (1H) X (3H) P (P) ?` with
`AKT4.K432.KT.432`: 13 HCP, **four hearts sitting over the 3H bidder**, three
quick tricks.  We bid **3NT** (`balhigh_nt3`, fit 1.000, no club or heart
stopper — `weakest_their_stopper` does not gate) for -100.  3H doubled is two
off.

**Missing agreement:** `general_balancing_high` has **no penalty double at all**
— only the takeout doubles at 40 and the reopening doubles at 41, both of which
demand at most a doubleton in their suit.  `general_competitive_high` has
`ch_penalty_X`; the balancing twin was never written.

```yaml
# context: general_balancing_high, inserted before `- id: balhigh_X`
      - id: balhigh_penalty_X
        call: X
        priority: 42
        when: { their_last_bid_suit: true, we_bid_last: false, we_hold_contract: false }
        requires:
          hcp: [12, 40]
          evals: { quick_tricks: [3, 12], standing_suit_length: [4, 13] }
        shows: "penalty double in the balancing seat: four-plus of their trumps behind the bidder and three quick tricks - they have preempted into my trump stack and have nowhere to run"
        establishes: { forcing: non_forcing }
```

The four-trump floor (against `ch_penalty_X`'s three) is the balancing-seat
version: partner has passed, so the trumps have to be mine.

**THE ANSWERING SEAT:** `general_pull_or_sit` already owns `... - X - P - ?`.
Traced: South (`J53..Q9874.AKT65`) sits with `adx_pass_min` fit 0.800.  Good —
that is the intended answer, and the pull rungs are there if he has somewhere
to go.

**What it endangers:** `balhigh_reopen_X`/`X2` (41) and `balhigh_X` (40) — all
three are the same call, and mine describes a hand with FOUR of their trumps,
which is precisely the hand the other three deny (`max_their_suit_length: [0,2]`
/ `standing_suit_length: [0,2]`), so they are disjoint by construction;
`balhigh_raise_*` (30-32 — I have no fit); `balhigh_nt3`/`nt2`/`nt1` (29/28/27 —
the rule that fired, and 3NT on `K432` in their suit and `432` in clubs is the
soft-stopper lottery); `balhigh_rebid_*`/`new_*` (25-29).  X is already covered
in this context, so no fallback is deleted.

**VERIFIED.**  Base `3NT`; patched `X` (`balhigh_penalty_X`, fit 1.000, prio 42);
South sits.  Regression: the same hand with only three hearts bids 3NT again
(mine fits 0.349).

**Template:** none over suits.  The `general_balancing_low` twin
(`ballow_penalty_X`, `standing_bid_level: [1, 2]`, `standing_suit_length: [5,13]`
because a low-level penalty double needs more trumps) is the natural companion,
but it is riskier and I would ship the high one first.

---

## Board 297 — margin -6

**Seat/call:** North, call 3 — `1C (1D-ours) 1S ?` with `J5.AQJ6.Q853.654`:
10 HCP with **four-card support for partner's OVERCALL**.  We doubled
(`cl_negative_X1`, priority 33) — a responsive double denying a fit — while
`cl_raise_D2` sat at 30 fitting 1.000.  They redoubled and we finished defending
2S for -140.

**Missing agreement:** raising partner's overcall shows the fit; the responsive
double denies one.  When both fit, the raise wins.

The gate that separates "partner overcalled" from "partner opened" without a
new `when:` is `partner_shown_length`: an overcall promises five, a 1m opening
promises three.

```yaml
# context: general_competitive_low, inserted before `- id: cl_negative_X1`
      - id: cl_raise_overcall_$X
        call: 2$X
        priority: 34
        when: { partner_suit: $X, cheapest_in_suit: true, i_have_acted: false,
                side_has_acted: true, we_hold_contract: false }
        requires:
          suits: { $X: [3, 13] }
          evals: { "partner_shown_length($X)": [5, 13], total_points: [8, 12], "lott_total_trumps($X)": [8, 26] }
        shows: "raise of partner's OVERCALL: three-plus trumps opposite his promised five and 8-12 support points - a known eight-card fit beats a double that asks him to guess"
        establishes: { forcing: non_forcing, agreed_suit: $X }
```

**Answering seat:** none — non-forcing and limited; partner passes or competes
with the rungs he already has.

**What it endangers:** `cl_negative_X1`/`X2` (33 — the point of the rung, and
only when partner has PROMISED five cards in a suit I hold three of);
`cl_raise_$X2` (30, same call, no `partner_shown_length` gate — mine is the
overcall-specific version); `cl_raise_lott3_$X` (32) and `cl_raise_$X3` (31,
both blocked by `cheapest_in_suit` here anyway); `cl_nt1`/`nt2` (27/28);
`cl_new_*` (25-27.5).  It does NOT reach `cl_doubler_*` (33-35) or `cl_takeout_X`
(36).  2$X is already covered, so no fallback is deleted.

**VERIFIED.**  Base `X` (`cl_negative_X1`, fit 1.000, prio 33); patched `2D`
(`cl_raise_overcall_D`, fit 1.000, prio 34).  Regression, and this is the one
that matters: the SAME hand after `1D (1S)` — partner OPENED — still doubles
(`nx_1m1S_X` at 80 in the more specific context), so the negative double is
untouched where it belongs.

**Template:** `expand: { X: [C, D, H, S] }`, plus the `general_competitive_high`,
`general_balancing_low` and `general_balancing_high` twins.

---

## Board 343 — margin -6 — NOTHING-WRONG (competitive)

**The engine's competitive call is right and BEN's is wrong.**  South, in the
sandwich seat after `1C (P) 1H` with `AQ5.AT6.J76.KT87` (14 HCP, 3-3-3-4, no
five-card suit and no shortness anywhere), passed at `sw_pass` fit 0.800; BEN
would double at 0.50 confidence.  Partner holds `87.983.9852.J643` — **one**
HCP.  A takeout double there is a disaster and the file's `sw_X` fit 0.349
correctly says so.  I checked the rest of our calls on both tables:
`oc1C_pass`, `cl_pass` over 1S, `ch_pass` over 3S and `balhigh_pass` are all
right at NS-vulnerable.

The board is lost at table B, where after `1C P 1H X XX 2D 2NT P` West raised
to 3NT on a 13-count opposite an 11-12 `cl_nt2` — the `uc_nt3` ceiling, and
**tightening `uc_nt3`'s strength gate is scope-excluded**.  Nothing to propose.

---

## Board 348 — margin -6 — NOTHING-WRONG (competitive)

Uncontested at both tables.  The divergence is South's response to `1D` on
`QJ.AQ4.K542.T976` — a flat 12-count with 4-4 minors choosing `r1m_2over1` (70)
over `r1m_2NT` (54), both at fit 1.000.  That is the constructive responding
ladder, and it runs into the open item "there is no context for opener's rebid
after a 2/1 in a MINOR" — `1D - P - 2C - P - ?` is unauthored and `uc_nt2`
annexed it, which is exactly what happened on call 4.  Both belong to the other
reviewer.  Our side was never opposed; there is no competitive call to make.

---

## Board 369 — margin -6 — NOTHING-WRONG (competitive)

Uncontested at both tables (`P 1D P 1H P 1NT P 2H P ?`).  South's pass on
`K42.872.AQ84.A83` with three-card support for partner's rebid 2H is a
constructive raise decision: `uc_raise_H3` fits 0.800 and `uc_pass` 1.000, and
the position (`1$m - P - 1$M - P - 1NT - P - 2$M - P - ?`) has **no context of
its own** — opener's seat after responder rebids his major falls all the way to
the generic continuation.  That is a constructive hole worth naming to the other
reviewer.  Competitively there was nothing to do: E/W passed every round and our
side held the auction throughout.

---

## Board 390 — margin -6

**Seat/call:** South, call 12 — `P P 1D (1S) 2C (P) (P) (X) P (2S) (P) (P) ?`
with `J5.J7.K86.KQT875`: **six clubs**, 9 HCP, and `their_fit` measured at
**8** (they have found their spade fit).  We passed it out (`ballow_pass`);
`ballow_rebid_C3` wants 16+ total points and fit 0.028.

**Missing agreement:** the Law in the balancing seat.  They have eight trumps
and I have a sixth one of my own; competing to three is right on shape, not on
points.

```yaml
# context: general_balancing_low, inserted before `- id: ballow_raise_C2`
      - id: ballow_rebid_law3_$X
        call: 3$X
        priority: 29.5
        when: { my_suit: $X, we_bid_last: false, cheapest_in_suit: true, we_hold_contract: false }
        requires:
          suits: { $X: [6, 13] }
          evals: { total_points: [8, 40], their_fit: [8, 26] }
        shows: "the Law in the balancing seat: they have found an eight-card fit and I have a sixth trump, so competing to three is right on shape, not on points"
        establishes: { forcing: non_forcing }
```

`their_fit >= 8` is doing the same job here that it does in `cl_raise_lott4_$M`,
where the file's own comment records that leaving it out measured +1 over 1000
boards: the Law licenses one more level only when BOTH sides have a fit.

**Answering seat:** none — non-forcing, and partner has already passed twice.

**What it endangers:** `ballow_rebid_$X3` (29, same call, 16+ — mine is the
shape-based version eight points lower and is gated on their fit);
`ballow_rebid_$X2`/`$X4` (29); `ballow_new_*3`/`long3` (27 — `my_suit` and
`unbid_suit` make these disjoint); `ballow_nt1`/`nt2` (27/28 — with a sixth
trump and their eight-card fit, notrump is not the strain); `ballow_pass` (21).
It sits BELOW `ballow_raise_*` (30-32), `ballow_nt2_strong` (30),
`ballow_nt2_balance` (33) and every double (39-41).  3$X is already covered by
`ballow_rebid_$X3`, so no fallback is deleted.

**VERIFIED.**  Base `P` (`ballow_pass`, fit 1.000); patched `3C`
(`ballow_rebid_law3_C`, fit 1.000, prio 29.5).  Measured on the board:
`their_fit` 8, `total_points` 12, `lott_total_trumps(C)` 6 (which is why no
raise rung could ever have fired — partner never bid clubs).

**Template:** `expand: { X: [C, D, H, S] }`, plus the `general_balancing_high`
twin at `call: 4$X` (`balhigh_rebid_law4_$X`) — though I would ship the low one
first; the four level needs `their_fit >= 9`.

---

## Board 425 — margin -6

**Seat/call:** South, call 1 — second seat, non-vulnerable, with
`QJ98653.AQ93.4.8`: **seven spades**, 9 HCP.  We passed; `open_3S_nv` fit 0.100.

**Missing agreement:** the "no preempt with a four-card major on the side" veto
exists to stop us preempting past our OWN major — it must not fire when the
preempt is in SPADES, the higher major, where partner can never miss a spade fit
and we can never be preempting past hearts we could otherwise have found.

Measured: `suit_quality(S)` 1.5, `hcp` 9, `quick_tricks_outside(S)` 1.5 — every
gate passes except `not: { suits: { H: [4,13] }, "suit_quality(H)": [1.5, 9] }`,
and `suit_quality(AQ93)` is 2.0.

```yaml
# context: openings, inserted before `- id: open_3S_vul`
      - id: open_3S_over_hearts_nv
        call: 3S
        priority: 59.5
        requires:
          suits: { S: [7, 13], H: [4, 4] }
          hcp: [3, 9]
          evals: { "suit_quality(S)": [0, 9], "quick_tricks_outside(S)": [0, 2] }
        shows: "preempt: 7+ spades, 3-9 HCP, with a four-card heart side suit - the side-major veto exists to stop preempting past our own major, and spades outranks hearts"
        establishes: { forcing: non_forcing }
        when: { we_vulnerable: false, opening_seat: [1, 2, 3] }
```

Priority 59.5 sits *below* `open_3S_nv` (60) on purpose: where the ordinary
preempt fits, it stays primary and this rung is invisible.

**THE ANSWERING SEAT:** `resp_preempt_S` is fully authored (raises, new suits,
3NT, 4S, pass) and needs nothing.  That is why I am willing to widen an opening
preempt.

**What it endangers:** `open_3S_nv` (60 — never, it is above);
`open_weak_2S_nv` (66 — above, and it demands exactly six spades, so disjoint);
`open_1S_rule20` (79) and `open_1S` (81) — both above, so a hand that qualifies
to open one spade still does; `open_4S` (61 — above); `open_pass` (20).  In
practice the only call it takes is the pass.  3S is already covered by
`open_3S_nv`, so no fallback is deleted.

**VERIFIED.**  Base `P`; patched `3S` (`open_3S_over_hearts_nv`, fit 1.000).
Regression: a hand without seven spades still passes.

**Template:** `expand` is not usable (the rule is specifically about spades over
hearts, which is the whole argument).  The vulnerable twin
`open_3S_over_hearts_vul` with `hcp: [5, 9]` is the companion.  **Do NOT
template this to hearts or the minors** — there the veto is doing its job.

---

## Board 445 — margin -6 — NOTHING-WRONG (competitive)

Uncontested at both tables.  The divergence is North's fourth-seat opening on
`A4.JT53.AK653.K8` — 15 balanced, `open_1D` at fit 1.000 versus BEN's 1NT — and
**opening-style thresholds are scope-excluded**.  I did check the one thing that
looked like a bug: `open_1NT` scores **0.000** on a 2-4-5-2 fifteen-count, which
is balanced and in range.  That is worth the other reviewer's eye (the shape is
5-4-2-2, i.e. `balanced` is false by the evaluator's definition — two doubletons
plus a five-card suit — so it is correct, not a bug; I am recording the check so
nobody repeats it).  Competitively E/W never had a call: they hold 16 HCP
between them across two passed hands.

---

## Board 494 — margin -6

**Seat/call:** North, call 6 — `(P) (P) 2NT (P) 3C (X) ?` with
`AQ53.AJ43.A4.AJ8`: 20 HCP, **four hearts and four spades**, and partner has
just asked for a major.  We passed (`xd_pass`, "sitting for their double",
fit 1.000, priority 18) and later passed out 3H for -100 while the other table
made 4S.

**Missing agreement:** `stayman_over_interference` exists for
`1NT - P - 2C - act - ?` and there is **no 2NT twin**, so a doubled 3C Stayman
falls all the way to `general_their_double`, where the only candidates are a
pass and three runouts.

```yaml
# NEW CONTEXT, inserted before `- id: resp_2NT` (specificity 1000+5, so it owns
# this exact auction and shadows only `general_their_double`'s three-token
# `... - X - ?`; the catch-all pass below carries the shadowed `xd_pass`
# verbatim so the context can only ever be a superset)
  - id: nt2_stayman_over_interference
    description: "Opener answers 3C Stayman after their interference"
    pattern: "2NT - P - 3C - act - ?"
    rules:
      - id: nt2_stmi_3H
        call: 3H
        priority: 70
        requires: { suits: { H: [4, 5] } }
        shows: "4+ hearts (over interference)"
        establishes: { forcing: non_forcing }
      - id: nt2_stmi_3S
        call: 3S
        priority: 60
        requires: { suits: { S: [4, 5] } }
        shows: "4+ spades, denies 4 hearts (over interference)"
        establishes: { forcing: non_forcing }
      - id: nt2_stmi_3D
        call: 3D
        priority: 50
        requires: { not: { any_of: [ { suits: { H: [4, 13] } }, { suits: { S: [4, 13] } } ] } }
        shows: "no 4-card major (over interference)"
        establishes: { forcing: non_forcing }
      - id: nt2_stmi_XX
        call: XX
        priority: 55
        requires: { evals: { "stoppers(their)": [1, 9] }, not: { any_of: [ { suits: { H: [4, 13] } }, { suits: { S: [4, 13] } } ] } }
        shows: "no 4-card major, their suit stopped: happy to play it redoubled"
        establishes: { forcing: non_forcing }
      - id: nt2_stmi_pass
        call: P
        priority: 20
        requires: {}
        shows: "nothing to say over their interference"
        establishes: { forcing: non_forcing }
        negative_inference_weight: soft
```

**THE ANSWERING SEAT — two edits, both required.**
`nt2_stayman_placement` only matches when RHO passed, and it has no rung for
"no fit with opener's major but four of my own":

```yaml
# context: nt2_stayman_placement — add the interference shape
    also_patterns: ["2NT - P - 3C - act - 3(D|H|S) - P - ?"]
# ... and one new rung, inserted before `- id: nt2_stm_4H`
      - id: nt2_stm_3S_other
        call: 3S
        priority: 61
        when: { standing_bid_strain: [H] }
        requires: { suits: { S: [4, 13], H: [0, 3] } }
        shows: "no heart fit but four spades of my own: opener may hold four of them too"
        establishes: { forcing: one_round }
```

**What it endangers:** inside its own auction it takes over from
`general_their_double` (`xd_pass` 18, `xd_run_*` 24-26, `xd_XX_extras` 23) —
`nt2_stmi_pass` at priority 20 with `requires: {}` reproduces `xd_pass`, and the
runouts are exactly what a 20-22 balanced opener must never do over a double of
an artificial 3C.  `nt2_stm_3S_other` at 61 outranks `nt2_stm_4H` (60),
`nt2_stm_4S` (59) and `nt2_stm_3NT` (55); it is gated to
`standing_bid_strain: [H]` with fewer than four hearts, so it cannot steal the
fit-raise from a hand that has one.

**VERIFIED end to end.**  `2NT (P) 3C (X) 3H (P) 3S (P) 4S`:
North `3H` (`nt2_stmi_3H`, fit 1.000), South `3S` (`nt2_stm_3S_other`, fit
1.000), North `4S` (`uc_raise_S4`, fit 1.000).  4S makes ten for +620, which is
the other table's score exactly.  Regression: a 4-3-3-3 twenty-count with no
four-card major bids 3D/XX, not pass.

**Template:** none needed; both blocks are literal.

---

## Board 535 — margin -6

**Seat/call:** South, call 3 — `(P) 2S (3C) ?` with `A9.AQ843.T3.Q832`:
partner has opened a weak two showing **exactly six spades**, they have
overcalled 3C, and I hold `A9` — the eighth trump.  We bid **3H**
(`ch_free_3H`, "free bid: 5+ good hearts, 10+") for -100.

**Missing agreement:** raise to the level of the fit opposite partner's KNOWN
six-card suit.  Every raise rung in `general_competitive_high` demands three
trumps of my own (`ch_raise_S3`, fit 0.330 here), which is the right floor when
partner's length is a minimum and the wrong one when he has announced six.
Measured on this board: `partner_shown_length(S)` = 6, `lott_total_trumps(S)` = 8.

```yaml
# context: general_competitive_high, inserted before `- id: ch_raise_C2`
      - id: ch_raise_preempt3_$M
        call: 3$M
        priority: 31.5
        when: { partner_suit: $M, cheapest_in_suit: true, we_hold_contract: false }
        requires:
          suits: { $M: [2, 13] }
          evals: { "partner_shown_length($M)": [6, 13], "lott_total_trumps($M)": [8, 26], total_points: [8, 40] }
        shows: "raise to the level of the fit opposite partner's KNOWN six-card suit: two trumps make eight, and eight trumps belong at the three level"
        establishes: { forcing: non_forcing, agreed_suit: $M }
```

**Answering seat:** none — non-forcing, and `preemptor_discipline`
(`preemptor_pass`, priority 45) already stops partner bidding again.

**What it endangers:** `ch_raise_$M3` (31, same call, 3+ trumps — mine is the
doubleton version and requires partner to have PROMISED six);
`ch_free_3H`/`ch_free_3S` (30 — the rule that fired; introducing a new suit at
the three level opposite a known six-card weak two, on a hand with a fit, is the
classic error); `ch_new_*3(_hi)` (27/27.5); `ch_advance_x3_*` (28.5);
`ch_neg_major_*` (30); `ch_nt2`/`nt3` (28/29); `ch_pass` (22).  It sits below
`ch_negative_X3` (33), `ch_penalty_X` (38) and `ch_raise_*4` (32).  3$M is
already covered, so no fallback is deleted.

**VERIFIED.**  Base `3H` (`ch_free_3H`, fit 1.000, prio 30); patched `3S`
(`ch_raise_preempt3_S`, fit 1.000, prio 31.5).  N/S make nine tricks in spades.

**Template:** `expand: { M: [H, S] }` here (minors would be a 4-level raise and
are not worth it), plus the `general_competitive_low` twin `cl_raise_preempt$M`
at `call: 3$M`.

---

## Board 558 — margin -6

**Seat/call:** the first divergence (North passing `1C` on `A2.J8765.T72.T62`,
5 HCP with five hearts) is the **constructive** responding hole again —
`r1m_pass` is 0-5 and `r1m_1H` is 6+.

**My competitive finding, call 6:** after `1C (P) (P) X XX 1S ?`, North —
holding five hearts opposite a redouble that announced 10+ — had only `cl_pass`.
**`general_after_redouble` stops matching the moment they bid**: its pattern is
`... - XX - $TAIL` with `expand: { TAIL: [ "?", "P - ?" ] }`, so once RHO
competes over our redouble the whole runout/competing ladder disappears and the
generic competitive rungs (which know nothing about the redouble) take over.
That is a structural hole worth a named entry in the open-items list.

**The minimal safe form of the repair, and its price:**

```yaml
# context: general_after_redouble — extend the tail
    expand: { TAIL: [ "?", "P - ?", "bid - ?" ] }
```

**This is a SHADOWING change and must not ship as written.**  `... - XX - bid - ?`
has specificity 4 and beats `general_competitive_low`'s 3, so the new context
would take over interpreting 1C-3S and 1NT and thereby DELETE, in every
they-competed-over-our-redouble auction: `cl_raise_*2/3/4` (27-32),
`cl_raise_lott3/4_*` (32), `cl_new_*` at the two and three level (26-27.5),
`cl_rebid_*` (29) and `cl_nt2`/`cl_nt3` (28/29) — i.e. the whole raise ladder.
`cl_negative_X*`, `cl_takeout_X` and `cl_pass` survive (X and P are not defined
by the `rr_*` rules... `rr_pass` does define P at 18, so `cl_pass` goes too).
To be a superset the extended context must first receive verbatim copies of the
raise, notrump and rebid rungs.

**UNTESTED**, deliberately: this is the same species as the "opener's second
double" and "the game-force landing family after a double" open items — it
**wants its own round**, and I am recording the diagnosis rather than shipping a
one-line pattern change that subtracts a hundred rungs.

**Answering seat:** unchanged (`redouble_continuations` and the generic ladders).

**Template:** none.

---

## Board 563 — margin -6 — NOTHING-WRONG (competitive)

Uncontested at both tables (`P 1D P 1S P 2C P ?`).  The divergence is South's
rebid on `AK8743.KT7.A86.4` — `r1d2c_3S` ("6+ spades, game values") at fit
1.000 against BEN's `fsf_2H` (fourth suit forcing) at 0.152.  Constructive
machinery; the other reviewer's.  E/W had 14 HCP between them and no shape:
`oc1D_pass`, `sw_pass`, `cl_pass` and `ch_pass` were all correct.

---

## Board 570 — margin -6

**Seat/call:** South, call 4 — `(P) (1D) 1H (P) ?` with `932.Q6.K5.KT8653`:
**six clubs**, 8 HCP, and `K5` in their suit.  We bid **1NT**
(`advo_1NT`, "8-11 with a stopper in their suit", priority 55, fit 1.000).
2C is the natural call and `uc_new_C2` was sitting there at priority 26.

**Missing agreement:** `advance_overcall` has a raise, a cue-raise and a 1NT
advance, but **no natural advance in a suit of my own** — so a six-card suit has
to come out through the generic `uc_new_*` rungs twenty-nine priority points
lower, and 1NT on a doubleton king wins every time.

```yaml
# context: advance_overcall, inserted before `- id: advo_1NT`
      - id: advo_new_long2_$L
        call: 2$L
        priority: 56
        when: { unbid_suit: $L, cheapest_in_suit: true }
        requires: { suits: { $L: [6, 13] }, evals: { total_points: [7, 11] } }
        shows: "advance in my own six-card suit: a six-card suit plays better than 1NT on a doubleton stopper"
        establishes: { forcing: non_forcing }
```

**Answering seat:** none — non-forcing, and partner's rebid seat is the generic
continuation, which already has the tools opposite a limited advance.

**What it endangers:** `advo_1NT` (55 — the rule that fired, and only when I
have a six-card side suit); `advo_raise` (60) and `advo_cue` (70) stay above,
so a genuine fit for the overcall still takes priority — correctly, because
supporting partner beats a six-card suit of my own; `adv_2NT` (56 in the sibling
context, different call).  2$L is already covered by `uc_new_$L2`, so no code
fallback is deleted.

**VERIFIED.**  Base `1NT` (`advo_1NT`, fit 1.000, prio 55); patched `2C`
(`advo_new_long2_C`, fit 1.000, prio 56).  N/S make nine tricks in clubs; the
table played 2D by West for -130.

**Template:** `expand` cannot be added (the context already carries
`expand_pairs` over `{o, v}`), so write the four rules out —
`advo_new_long2_C/D/H/S` — with `unbid_suit` keeping each out of partner's and
their suits.  A three-level twin (`advo_new_long3_*`) is the companion for
auctions where the two level is gone.

---

## Board 655 — margin -6

**Seat/call:** North, call 5 — `(1C) 1H (P) 2C (2S) ?` with
`976.AJT84.QJ5.T3`.  Partner cue-bid 2C showing a limit-raise-or-better of my
hearts; they competed to 2S; we **passed** (`cl_pass`, fit 1.000) while
`cl_raise_H3` sat at 0.800 (its floor is 10 support points; I have 8) and
`cl_rebid_H3` at 0.143 (its floor is a sixth heart).

**Missing agreement:** once partner's cue has agreed MY overcalled suit, my
rebid of it in competition is a Law decision, not a values decision: five
trumps opposite his promised three is eight our way, and eight trumps belong at
the three level.

```yaml
# context: general_competitive_low, inserted before `- id: cl_raise_C2`
      - id: cl_rebid_agreed_law3_$X
        call: 3$X
        priority: 31.5
        when: { my_suit: $X, partner_suit: $X, we_bid_last: false,
                cheapest_in_suit: true, we_hold_contract: false }
        requires:
          suits: { $X: [5, 13] }
          evals: { "lott_total_trumps($X)": [8, 26], total_points: [7, 40] }
        shows: "the Law after partner agreed my suit: five trumps opposite his three, eight our way - competing to three is right on shape"
        establishes: { forcing: non_forcing, agreed_suit: $X }
```

The double gate `my_suit: $X` AND `partner_suit: $X` is what makes it safe: it
fires only where I bid the suit and partner has since agreed it (by a raise, a
cue-raise, or a support double), which is exactly the position where the
"raise partner" rungs and the "rebid my own" rungs both mis-describe the hand.

**Answering seat:** none — non-forcing, and partner has already limited himself.

**What it endangers:** `cl_raise_$X3` (31, same call — its 10-point floor is a
constructive test in a contested auction); `cl_rebid_$X3` (29, same call, six
cards); `cl_rebid_jump_$X` (31); `cl_raise_lott3_$X` (32 — stays above, but its
`cheapest_in_suit` gate and 4-trump/3-10-point band make it a different hand);
`cl_nt2` (28); `cl_new_*` (25-27.5).  Below `cl_negative_X*` (33) and
`cl_takeout_X` (36).  3$X is already covered, so no fallback is deleted.

**VERIFIED** for the call: base `P`; patched `3H` (`cl_rebid_agreed_law3_H`,
fit 1.000, prio 31.5).  **Honest note: it probably does not win this board** —
West bids 3S over it either way, and we would finish -140 instead of -140.  The
agreement is right and the position recurs; the board's real cost is at table B,
where East raised a 1S opening to 2S on **4 HCP** (`r1S_single_raise`, fit
1.000, priority 60, against `r1S_pass` fit 1.000 at 15) and West then drove to a
failing 4S.  That single-raise floor is a constructive-ladder question and I
flag it for the other reviewer.

**Template:** `expand: { X: [C, D, H, S] }`, plus the three sibling contexts.

---

## Board 658 — margin -6

**Seat/call:** West, call 5 — `(P) 1C (1D) 1H (P) ?` with `Q54.QJ4.JT.AKT32`,
13 HCP.  **We passed our partner's free bid** (`uc_pass`, fit 1.000, priority
18) and played 1H.

**Missing agreement, and it is the largest correctness finding in my slice:**
responder's new suit at the one level over an overcall is **forcing**.
`cl_new_H1` (and `cl_new_S1`, `cl_new_D1`, `cl_new_C1`) carry
`establishes: { forcing: non_forcing }`, so nothing forbids opener's pass and
`uc_pass` wins at fit 1.00.  Every standard system, and this one's own
`DECISIONS.md` ("negative doubles through 3S ... 1S = 5+"), treats the free bid
as one-round forcing.

The gate that separates responder's free bid (partner opened, still unlimited)
from advancer's free bid (partner overcalled, capped at 16-17) without a new
`when:` is `partner_shown_max`: measured 21 here, ~16 after an overcall.

```yaml
# context: general_competitive_low, inserted before `- id: cl_new_C1`
      - id: cl_new_free1_$X
        call: 1$X
        priority: 30.5
        when: { unbid_suit: $X, cheapest_in_suit: true, side_has_acted: true,
                i_have_acted: false, partner_last_call_was_double: false,
                we_hold_contract: false }
        requires:
          suits: { $X: [4, 13] }
          evals: { total_points: [6, 40], partner_shown_max: [19, 40] }
        shows: "free bid of a new suit at the one level over their overcall: 4+ cards and 6+ points opposite a partner who is still unlimited - forcing for one round"
        establishes: { forcing: one_round }
```

For `$X = H` the rule must also carry `cl_new_H1`'s ordering clause verbatim —
`evals: { "suit_diff(H,S)": [0, 13] }` plus its
`any_of: [ { evals: { "suit_quality(H)": [1.5, 9] } }, { suits: { H: [5, 13] } } ]`
— or the 5-5 defect that comment describes comes back.

**THE ANSWERING SEAT:** the force is one round and its answers are the whole of
`general_uncontested_continuation` / `general_competitive_low`, which are dense
at that level (raises 30-32, rebids 29, notrump 27-29, new suits 25-27.5).
Traced: West now bids **2H** (`uc_raise_H2`, fit 0.800) instead of passing.

**What it endangers — state this one plainly, it is the riskiest proposal here.**
Making a call forcing **removes the pass in every seat the rule's `when`
reaches**, and `cl_new_free1_$X` becomes the PRIMARY reading of 1-of-a-new-suit
(priority 30.5 above `cl_new_$X1`'s 30), so partner may no longer pass it
anywhere in the competitive-low context.  The `when` narrows that to: our side
has acted, I have not, partner's last call was not a double (advancing a takeout
double is a different animal and already owned by the `adv*` contexts), and
partner is unlimited.  Within the context it can outrank `cl_new_$X1` (30, same
call, more general), `cl_new_H1`/`cl_new_S1` (30), `cl_nt1` (27) and every
natural two-/three-level rung (25-29); it stays below every raise at 30 only by
call rank, so **check `cl_raise_$X2` (30) explicitly before shipping** — a hand
with 4-card support and a 4-card side suit must still raise.

**VERIFIED** for the mechanism: base West `P`; patched West `2H`.  I did NOT
measure the blast radius, and this one deserves its own screened experiment.

**Template:** `expand: { X: [C, D, H, S] }` (with the H/S ordering clauses),
plus `general_competitive_high` for the two- and three-level free bids, where
the same non-forcing marking applies.

---

## Board 690 — margin -6 — the biggest single win in my slice

**Seat/call:** North, call 2 — `1D (1S) ?` with `4.J76432.4.AQT86`:
**six hearts and five clubs**, 7 HCP, singletons in both black... in spades and
diamonds.  We doubled (`nx_1m1S_X`, priority 80) and East jumped to 4S; -420.
`nx_1m1S_wj_H` (3H) was sitting there at fit **1.000**, priority 56.

**Missing agreement:** a two-suiter bids, it does not double.  A negative double
asks partner to name a suit; with 6-5 I know where we are playing.

```yaml
# context: resp_1m_over_1S, inserted before `- id: nx_1m1S_X`
      - id: nx_1m1S_wj6_H
        call: 3H
        priority: 81
        requires:
          suits: { H: [6, 13] }
          hcp: [3, 9]
          any_of: [ { suits: { C: [5, 13] } }, { suits: { D: [5, 13] } }, { suits: { S: [5, 13] } } ]
        shows: "weak jump shift with a second suit: six hearts and a five-card side suit, less than a free bid - a two-suiter bids, it does not ask partner to guess"
        establishes: { forcing: non_forcing }
```

**THE ANSWERING SEAT — and it needs one rung.**  Opposite a preemptive jump
showing 6+ cards, every generic raise rung dies on `rule_of_26` (the known open
item): South with `T8.AQT8.KQT73.K5` and four-card support scored
`uc_raise_H4` at fit 0.000 and passed.  Ship this with it:

```yaml
# context: general_uncontested_continuation, before `- id: uc_raise_H4`
      - id: uc_raise_lawpre4_$M
        call: 4$M
        priority: 32.5
        when: { partner_suit: $M, we_hold_contract: false }
        requires:
          suits: { $M: [4, 13] }
          evals: { "lott_total_trumps($M)": [10, 26], total_points: [12, 40] }
        shows: "the Law opposite partner's preemptive jump: ten trumps our way and opening values - bid the game, not the invitation"
        establishes: { forcing: sign_off, agreed_suit: $M }
```

**What it endangers.**  The jump shift: `nx_1m1S_X` (80 — only on the 6-5
shape); `nx_1m1S_2H` (78, 5+ hearts and 10+ HCP — mine caps at 9);
`nx_1m1S_cue` (70), `nx_1m1S_raise` (55), `nx_1m1S_1NT`/`2NT`/`3NT` (50-52) —
all describe hands I do not hold; `nx_1m1S_wj_H` (56, same call, no side-suit
requirement).  3H is already covered, so no fallback is deleted.
The answering rung: `uc_raise_$M4` (32, same call — mine is the Law version and
requires ten counted trumps, which is strictly more information);
`uc_raise_lott4_$M` (32, same call, `their_fit`-gated); `uc_raise_$M3` (31);
everything below.  It does not reach `gst_rkc_$M` (46).

**VERIFIED end to end.**  Base: `X`, then East 4S, -420.  Patched: North `3H`
(`nx_1m1S_wj6_H`, fit 1.000), South `4H` (`uc_raise_lawpre4_H`, fit 1.000).
**4H makes ten: +420 instead of -420.**  Regressions: five hearts and a five-card
side suit still doubles; six hearts with 10+ HCP still doubles.

**Template:** `expand: { m: [C, D] }` in both `resp_1m_over_1H` (as
`nx_1m1H_wj6_S`, `call: 2S`) and `resp_1m_over_1S`; note the open item
"`resp_1m_over_1H` has no weak jump shift at all", which this fills at the same
time.  The answering rung: `expand: { M: [H, S] }` plus the
`general_competitive_low/high` twins.

---

## Board 704 — margin -6

**Seat/call:** North, call 0 — first seat, non-vulnerable, with
`J87652.K.T.QJT75`: **six spades and five clubs**, 7 HCP (10 total points).
We passed; `open_weak_2S_nv` fit 0.757.  The blocker, measured:
`suit_quality(S)` = **0.5** against the rule's `[1, 9]`.  Everything else
passes (`hcp` 7, `quick_tricks_outside(S)` 0.0, exactly six spades, one heart).

**Missing agreement:** the suit-quality bar on a weak two is standing in for
playing tricks — and a five-card side suit supplies them directly.  6-5 comes
alive; a six-card suit with nothing else does not.

```yaml
# context: openings, inserted before `- id: open_weak_2S_vul`
      - id: open_weak_2S_65_nv
        call: 2S
        priority: 65.5
        requires:
          suits: { S: [6, 6], H: [0, 3] }
          hcp: [5, 10]
          evals: { "quick_tricks_outside(S)": [0, 2] }
          any_of: [ { suits: { C: [5, 13] } }, { suits: { D: [5, 13] } } ]
        shows: "weak two on shape: six spades and a five-card minor - the second suit supplies the playing tricks the suit-quality bar was standing in for"
        establishes: { forcing: non_forcing }
        when: { we_vulnerable: false, opening_seat: [1, 2, 3] }
```

Priority 65.5 is deliberately BELOW `open_weak_2S_nv` (66): where the ordinary
disciplined weak two fits, it stays primary.

**THE ANSWERING SEAT:** `resp_weak2`, `resp_weak2_major_game`,
`resp_weak2_newsuit_S`, `weak2_ask_continuation` and `weak2_feature_answer_S`
are all authored, and `preemptor_discipline` stops the opener bidding again.
Nothing new is needed — which is why widening a preempt is affordable here and
was not in the slam family.

**What it endangers:** `open_weak_2S_nv` (66 — above it, untouched);
`open_3S_nv` (60 — a seven-card hand, disjoint by the `S: [6, 6]` gate);
`open_1S_rule20` (79) and `open_1S` (81) — both above, so a hand worth a one-bid
still opens one; `open_1C_rule20` (71) and `open_1C` (73) — also above, and this
hand fails both; `open_pass` (20).  In practice it only takes the pass.  2S is
already covered by `open_weak_2S_nv`, so no fallback is deleted.
**The cost to state:** it legalises a weak two on a poor suit, which is a real
loosening of the "weak twos are disciplined" agreement in `DECISIONS.md`.  The
5-card-side-suit gate is the whole justification and must not be dropped.

**VERIFIED.**  Base `P`; patched `2S` (`open_weak_2S_65_nv`, fit 1.000).
Regression: `J87652.K42.T3.QJ` (no five-card side suit) still passes.

**Template:** `open_weak_2H_65_nv` and `open_weak_2D_65_nv` are the siblings
(with the appropriate other-major cap), plus the vulnerable twins at
`hcp: [7, 10]` — although at these colours I would ship non-vulnerable only.

---

## Board 713 — margin -6 — a sibling-gate finding, and a NEGATIVE prototype

**Seat/call:** South, call 5 — `(P) 1H (2S) (P) (P) ?` with
`A.AKQJ94.A542.93`: 18 HCP, a **singleton ace of spades**, `AKQJ94`.  We bid
**3H** (`ballow_rebid_H3`, fit 1.000) for -50; passing 2S out was worth +100
(they are vulnerable and take seven tricks).

**The finding:** `ballow_reopen_X` scored **0.349** on an 18-count with a
singleton in their suit, because it carries `evals: { longest_suit_length: [0, 5] }`
— "a takeout double must not hide a six-card suit".  **Round 7 ruled against
exactly that clause with whole-corpus data** (doubles WITH a 6+ suit averaged
-2.00 a table, WITHOUT -2.54) and removed it from the sibling rules; it survives
on `ballow_reopen_X`, `ballow_reopen_X2`, `balhigh_reopen_X` and
`balhigh_reopen_X2`.  That is a lint-class inconsistency of the kind the
`sibling` linter exists to catch.

**NEGATIVE PROTOTYPE RESULT — I built the repair and it makes THIS board worse.**
An additive `ballow_reopen_X_long` (16+, `max_their_suit_length: [0, 2]`,
`longest_suit_length: [6, 13]`, priority 41) fires cleanly:

```yaml
# context: general_balancing_low, inserted before `- id: ballow_X`
      - id: ballow_reopen_X_long
        call: X
        priority: 41
        when: { their_last_bid_suit: true, side_has_acted: true, we_bid_last: false,
                my_last_call_was_double: false, we_hold_contract: false }
        requires:
          hcp: [16, 40]
          evals: { max_their_suit_length: [0, 2], longest_suit_length: [6, 13] }
        shows: "reopening double with a long suit of my own: 16+, short in their suit - partner names the strain and I can always correct to my six-card suit"
        establishes: { forcing: one_round }
```

Traced: South now doubles (fit 1.000), and North (`98763.T5.97.KT86`, 3 HCP)
advances **3C** at `adreo_suit_C_H` — a 4-3 club fit, two off for -100, WORSE
than the -50 we scored.  So: the sibling gate is a real defect and the round-7
ruling applies to it, but **board 713 is not the evidence for fixing it**, and I
am not shipping it off one board.  Recommendation: measure it as its own
experiment across all four rules, with the `advance_reopening_double`
one-level advances from board 758 in place first.

**Answering seat:** `advance_reopening_double`, already authored (and repaired
by the board-758 proposal).

**UNTESTED as a gain; VERIFIED as a loss on this board.**

**Template:** the same clause removal / additive twin on all four reopening
doubles.

---

## Board 725 — margin -6

**Seat/call:** North, call 3 — `(P) 1NT (P) ?` with `T7532.Q9542.T83.`:
**exactly 5-5 in the majors**, 2 HCP.  We transferred to hearts (`nt_transfer_H`,
priority 88, fit 1.000) and played 2H for -100; 2S makes nine.

**Missing agreement:** with 5-5 in the majors opposite 1NT you transfer to the
HIGHER suit — you can still show hearts below game, and on a bust you simply
pass 2S.  `nt_transfer_H` (88) and `nt_transfer_S` (87) both fit 1.000 on a 5-5
hand and the tie went to the higher-priority heart transfer.  This is the third
instance in this dossier of the same 5-5 ordering defect (see boards 272 and
191); round 10 fixed it for `r1m_1H`/`r1m_1S` and the sweep never reached the
notrump or overcall ladders.

```yaml
# context: resp_1NT, inserted before `- id: nt_transfer_H`
      - id: nt_transfer_S_55
        call: 2H
        priority: 89
        requires: { suits: { S: [5, 13], H: [5, 13] }, evals: { "suit_diff(S,H)": [0, 0] } }
        shows: "Jacoby transfer to spades with exactly 5-5 in the majors: transfer to the HIGHER suit so hearts can still be shown below game"
        establishes: { forcing: one_round }
        convention: jacoby_transfer
        announce: "transfer"
```

(The additive `suit_diff(S,H): [0, 0]` form is used rather than tightening
`nt_transfer_H`, so 6-5 and 5-4 hands keep the heart transfer.)

**THE ANSWERING SEAT:** unchanged — `nt_transfer_accept_S` completes to 2S, and
`nt_after_transfer` owns responder's rebid.  The transfer is already
`forcing: one_round` and its acceptance is `requires: {}`.

**What it endangers:** `nt_transfer_H` (88, same shape only when 5-5 exactly);
`nt_stayman` (85 — a 5-5 major hand is a transfer hand, not a Stayman hand);
`nt_pass` (25).  It cannot reach `nt_2NT_inv`, `nt_3NT`, the bails or the
quantitative rungs, all of which deny a five-card major.  2H is already covered
by `nt_transfer_S`, so no fallback is deleted.

**VERIFIED.**  Base `2D` (`nt_transfer_H`, fit 1.000, prio 88); patched `2H`
(`nt_transfer_S_55`, fit 1.000, prio 89).  N/S make nine tricks in spades
against seven in hearts.

**Template:** the identical rung in `resp_2NT` (`nt2_transfer_S_55`,
`call: 3H`) and in `r2c_2NT_transfer_reply`; and the same ordering repair is
owed to `sw_1H`/`sw_1S` (both 68), `ballow_new_H1`/`ballow_new_S1` (both 25) and
`oc*_1H`/`oc*_1S` (both 71 — board 272).

---

## Board 782 — margin -6 — NOTHING-WRONG (competitive)

The first divergence is North's response to `1H` on `T63.QT3.KQJ.KJ75` — a flat
4-3-3-3 twelve-count with three-card support choosing `r1H_2C` (2/1 GF,
priority 75, fit 1.000) over `r1H_limit_raise` (62, fit 0.800) and `r1H_1NT`
(40, fit 0.800).  That is the constructive responding ladder — whether a
balanced 12 with three trumps and no ruffing value is a 2/1 or a limit raise —
and it belongs to the other reviewer.

Competitively I checked both of our seats at table B.  `oc1H_pass` for West on
`74.98.T95432.A82` is right.  East's sandwich `2S` on `AKQ95.765.76.Q94` after
`1H P 1NT` (`sw_2S`, "good 5+ spades, 11-17") is a legitimate matchpoint action
at both-vulnerable with `AKQ95` — BEN passes, but the suit is exactly what the
rule's `suit_quality` gate is for, and it cost nothing: we passed thereafter and
N/S bid their own 3H.  The board is lost at table A on a constructive choice.
Nothing to propose.

---

## Summary table

| board | seat/call | agreement | verdict |
|---|---|---|---|
| 632 | S, `cl_pass` over `1D (2C)` | jump raise on the fit (`cl_raise_fit3_$X`) | VERIFIED |
| 707 | S, `xd_rebid_D2` | jump rebid over their double (`xd_rebid_jump_$X`) | VERIFIED (0 IMPs here) |
| 758 | N, `ballow_nt1` | reopening double on shape + the missing 1-level advances | VERIFIED |
| 788 | N, `advH_1S` | jump advance on a fifth trump | VERIFIED |
| 894 | N, `xd_run_C2` | discriminating weak pass over their double | VERIFIED |
| 922 | N, `nx_1m1S_pass` | preemptive raise of partner's minor | VERIFIED |
| 988 | S, `balhigh_rebid_H4` | partner already declined: do not bid it a third time | VERIFIED |
| 0 | W, `ballow_X` | a seven-card suit names its own trumps | VERIFIED (+ negative result) |
| 55 | S, `cl_new_long2_D_hi` | vulnerable two-level discipline in a live auction | VERIFIED |
| 83 | — | — | NOTHING-WRONG |
| 93 | — | — | NOTHING-WRONG |
| 116 | E, `oc1H_pass` | takeout double on shape at 10-11 | VERIFIED (call only) |
| 132 | — | — | NOTHING-WRONG |
| 188 | N, `uc_raise_H4` | the Law at the three level (`uc_raise_law3_$M`) | VERIFIED |
| 191 | S, `sw_X` | with 5-5 bid your suits | VERIFIED |
| 247 | S, `nxj_X` | trap pass + the reopening double that converts it | VERIFIED |
| 267 | — | — | NOTHING-WRONG |
| 272 | S, `oc1D_1H` | 5-5 majors: overcall the higher | VERIFIED |
| 274 | N, `balhigh_nt3` | a penalty double in the balancing-high context | VERIFIED |
| 297 | N, `cl_negative_X1` | raising an overcall beats a responsive double | VERIFIED |
| 343 | — | — | NOTHING-WRONG |
| 348 | — | — | NOTHING-WRONG |
| 369 | — | — | NOTHING-WRONG |
| 390 | S, `ballow_pass` | the Law in the balancing seat (`their_fit >= 8`) | VERIFIED |
| 425 | S, `open_pass` | the side-major veto must not fire in spades | VERIFIED |
| 445 | — | — | NOTHING-WRONG |
| 494 | N, `xd_pass` | 3C Stayman over interference + the placement seat | VERIFIED |
| 535 | S, `ch_free_3H` | raise partner's known six-card suit on a doubleton | VERIFIED |
| 558 | N, `cl_pass` | `general_after_redouble` stops matching once they bid | UNTESTED (own round) |
| 563 | — | — | NOTHING-WRONG |
| 570 | S, `advo_1NT` | natural six-card advance of an overcall | VERIFIED |
| 655 | N, `cl_pass` | the Law once partner has agreed my overcalled suit | VERIFIED (0 IMPs here) |
| 658 | W, `uc_pass` | **the free bid at the one level is FORCING** | VERIFIED (mechanism) |
| 690 | N, `nx_1m1S_X` | 6-5 jump shift + the Law game raise opposite it | VERIFIED, +840 pts |
| 704 | N, `open_pass` | weak two on 6-5 shape | VERIFIED |
| 713 | S, `ballow_rebid_H3` | the six-card veto on the reopening doubles | NEGATIVE result |
| 725 | N, `nt_transfer_H` | 5-5 majors: transfer to the higher | VERIFIED |
| 782 | — | — | NOTHING-WRONG |

## The one cross-cutting repair I would ship first

**The 5-5 ordering defect** (boards 272, 725, and 191 by family).  Round 10
fixed `r1m_1H`/`r1m_1S`, and a later round fixed `cl_new_H1`/`cl_new_S1` with a
comment saying the sweep was never done.  It still has not been:
`oc*_1H`/`oc*_1S` are both 71, `sw_1H`/`sw_1S` both 68, `ballow_new_H1`/`_S1`
both 25, `balhigh_new_H1`/`_S1` both 25, `ch_new_H1`/`_S1` both 25, and
`nt_transfer_H`/`nt_transfer_S` are 88/87 — in every one of those pairs a 5-5
hand ties at fit 1.000 and the LOWER suit wins on call rank.  Six two-line
additive rungs, zero conventions invented, and every one of them is the same
sentence of bridge the file already writes.
