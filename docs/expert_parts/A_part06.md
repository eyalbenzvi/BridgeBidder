# EXPERT A — competitive / matchpoint duplicate — dossier part 06

38 boards (-122 IMPs), all of them -3 or -4.  **34 proposals, 4 NOTHING-WRONG**
(864, 582, 767, 861).  Every proposal was prototyped by loading a *copy* of
`two_over_one.yaml` with the rung inserted and re-running `score_candidates` /
`fast_decision` on the exact seat, hand, vulnerability and auction from the
dossier; the repo file was never touched.  **All 34 are VERIFIED that
way, with controls**; one (board 76) is additionally flagged UNTESTED-in-corpus
because its whole-corpus denominator is empty, and two more (852, 433) carry
explicit cautions about thin or adverse denominators.

Whole-corpus denominators (`repro.fires_summary('reports/r18_before.jsonl', …)`)
were pulled before demoting anything.  The ones that changed a verdict:

| rule | tables | mean | effect on this review |
|---|---|---|---|
| `v3_D_X` | 5 | **+1.60** | the takeout double of a preempt is a WINNER — board 98's rung was cut back to solid six-card suits only |
| `ballow_reopen_X` | 4 | **+3.75** | board 991's rung was checked to be mutually exclusive with it, not above it |
| `xd_run_S2` | 3 | **+0.67** | board 864 turned into NOTHING-WRONG |
| `open_pass_4th` | 4 | **0.00** | board 76's rung has no corpus support and is labelled speculative |
| `oc1D_1NT` | 7 | -4.57 | board 772 |
| `cl_rebid_jump_H` | 5 | -4.80 | board 850 |
| `cl_new_C3` | 12 | -3.92 | board 774 |
| `ob_1D1H_2C` | 7 | -3.57 | board 918 |
| `sw_2C / sw_2S / sw_2H` | 8 / 2 / 6 | -2.75 / -4.50 / -2.67 | boards 103, 199 |
| `uc_rebid_C3` | 10 | -2.10 | board 474 |
| `uc_nt2` | 21 | -1.57 | board 905 |
| `cl_negative_X2` | 15 | -2.07 | board 852 — CAUTION, my rung widens a losing family |
| `rrevh_2S`, `cl_new_long2_H_hi`, `ch_new_H3_hi` | 0 | — | starved rungs, boards 506 / 646 / 548 |

## Verification method, and one bug reproduced on the way

Every rung was inserted into a **copy** of `two_over_one.yaml` in the scratchpad
and the copy loaded with `load_system(path)`; the decision was then re-run with
`prepare_decision` + `score_candidates` + `fast_decision` on the exact seat,
hand, vulnerability and auction from the dossier.  Nothing in the repo was
edited.

**All 34 rungs were then loaded TOGETHER and run against the whole regression
suite — 516 scenarios in `tests/data/*.yaml`.  Result: 0 baseline failures,
0 patched failures, byte-identical output.  No locked scenario moves.**  (That
is a necessary condition, not a sufficient one; it says the batch is
self-consistent, not that it pays.)

Two rungs failed their first trace and both failures were my own error, worth
recording because they are the two traps the method file names:

* `cl_rebid_game_$M` (board 850) carried `cheapest_in_suit: true`, which makes a
  JUMP to game structurally unreachable — the exact defect the ledger records
  for `cl_raise_lott3_$M`.  Gate removed.
* `cl_doubler_min_raise_$X` (board 774) used `max_their_suit_length`, which
  reads my length in their LONGEST suit and was 3 here; the rule wants my length
  in the suit they have just bid, which is `standing_suit_length`.

**And a live reproduction of open item 5.**  Running the regression sweep for
the baseline and the patched system *in the same Python process* reported two
spurious failures on `harvested.yaml` (`tips_no_blackwood_with_void`,
`expert_veto_holds_with_two_keycards`, both "got 2S want 3D"), which vanish when
each system is run in its own process.  That is `_SETUP_CACHE` keying on
`id(system)` while holding no reference: the first system is collected, the
second lands on the same id, and the cached setup is reused across systems.
**Anyone screening a YAML change by loading two systems in one process is
getting corrupted results.**  Fix item 5 before the next screening run, or fork
per system.

## The three agreements that matter most in this slice

**1. The takeout double of a PREPARED MINOR (boards 23, 512, 803; ~-11 IMPs).**
`oc1C_X` / `oc1D_X` demand at most a doubleton in their suit.  Nobody opens a
three-card major, but everybody opens a three-card minor, so the shortness test
is imported from the wrong opening.  Three seats in 38 boards passed a hand
every expert doubles: 4-3-3-3 thirteen- and fourteen-counts (23, 512) and a
4-4-4-1 ten-count with the singleton in their suit (803).  Two rungs
(`oc1x_X_flat`, `oc1x_X_shape`) across all four `overcalls_of_1x` contexts.
This one is a large behaviour change and deserves its own screened experiment.

**2. THE DISCIPLINE PASS: once I have described my hand, my second voluntary
bid in competition is the file's most expensive habit** (646, 103, 198, 230,
433, 474, 548, 820, 863 — nine boards, ~-30 IMPs).  There is no rung anywhere
in the four generic competitive contexts that says "I have already shown this
hand; pass".  Every ladder ends in a catch-all pass at priority 18-22, *below*
every natural bid, so the engine bids whenever anything fits at all.  The
repair is a family of narrow, high-priority PASS rungs — safe by construction,
because a pass is already covered in every one of those contexts so no code
fallback is deleted, and because a `requires` that only the described hand fits
cannot outrank anything on a hand it does not describe.

**3. THE LAW OF TOTAL TRICKS IS THE TEST IN A CONTESTED AUCTION, `rule_of_26`
IS NOT** (258, 597, 850, 198).  The file already knows this — the comment above
`cl_raise_lott4_$M` says it in as many words — and then never generalises it.
`ch_raise_$M3` still gates the three-level competitive raise on
`rule_of_26 >= 22`, so a nine-trump fit opposite a weak two cannot be raised;
there is no Law raise in a MINOR at any level; and nothing anywhere says that
eight trumps means eight tricks, so the engine competes to three on a 5-3 fit.

---

## Board 646 — table A, call 6, seat N: `2H` (`cl_new_long2_H_hi`)

`P 1S P 1NT P 2D`, N holds `976.AJ7642.7.J87`, 6 HCP, **we are vulnerable**,
partner has passed twice and both opponents are bidding constructively.  2H
here begat the double, the pull, the raise and -300.

**Missing agreement.** Vulnerable, with a passed partner and both opponents
bidding, a six-card suit and eight points is not enough to come in at the two
level — that hand defends.

```yaml
# context: general_competitive_low   (insert before cl_doubler_raise_C)
      - id: cl_pass_outgunned
        call: P
        priority: 34
        when: { side_has_acted: false, we_vulnerable: true, standing_bid_level: [2] }
        requires:
          hcp: [0, 8]
          evals: { longest_suit_length: [5, 7] }
        shows: "vulnerable, partner has passed and both of them are bidding: a weak one-suiter stays out"
        establishes: { forcing: non_forcing }
```

**Answering seat:** none — it is a pass, not a force.

**Endangers.** Above it in this context nothing can fit: `cl_takeout_X` (36) and
`cl_nt2_direct` (37) both need opening values or 16+, which `hcp: [0,8]` denies;
`cl_negative_X2` (33) needs `side_has_acted: true`, which the `when` excludes.
Below it, it outranks exactly the natural two- and three-level suit bids
(`cl_new_*2`/`cl_new_long2_*` at 26/26.5, `cl_new_*3` at 27/27.5) and `cl_pass`
(20) — and on a hand with under 9 HCP, a passed partner and two opponents
bidding, defending is the better description of the hand than a one-suiter is.
It cannot silence a raise (`partner_suit` is impossible with `side_has_acted:
false`) and it deletes no code fallback, because `cl_pass` already covers `P`.

**VERIFIED.** `P cl_pass_outgunned fit=1.000 prio=34` chosen over
`2H cl_new_long2_H_hi fit=1.000 prio=26.5`.  Controls: the same hand NON-vul
still bids 2H; the same shape with 12 HCP (`976.AKJ642.7.J87`) still bids 2H.

**Template.** No suit expansion (it is a pass).  Sibling copy into
`general_competitive_high` as `ch_pass_outgunned` with
`standing_bid_level: [3]` — but only after this one is measured; the
three-level natural rungs already demand 13-14+, so the payoff there is smaller.

---

## Board 774 — table B, call 7, seat E: `3C` (`cl_new_C3_hi`)

`1D P 1H X XX 1S 2H`, E holds `JT85.6.AK4.KQ953`, 13 HCP.  I doubled, partner
was FORCED to name a suit at the one level, and over 2H I invented a new suit
at the three level instead of raising the fit.  2S makes ten tricks
double-dummy; 3C went one down.

**Missing agreement.** The doubler with four-card support and 12-16 raises the
suit partner was forced to name; only 17-19 jumps.

```yaml
# context: general_competitive_low   (insert before cl_doubler_raise_C)
      - id: cl_doubler_min_raise_S
        call: 2S
        priority: 32.5
        when: { partner_suit: S, cheapest_in_suit: true, my_last_call_was_double: true,
                we_hold_contract: false }
        requires:
          suits: { S: [4, 13] }
          evals: { total_points: [12, 16], standing_suit_length: [0, 2] }
        shows: "raising the suit partner was forced to name: 12-16 with four-card support and shortness in the suit they just bid"
        establishes: { forcing: non_forcing, agreed_suit: S }
```

**Answering seat:** none — non-forcing, and `agreed_suit: S` puts partner back
into the existing raise/pass ladders.

**Endangers.** Above: `cl_doubler_raise_S` (34) keeps 17-19, which is the whole
point of the split; `cl_negative_X2` (33) needs `i_have_acted: false` and is
excluded.  Below: `cl_new_C3`/`_hi` (27/27.5, whole-corpus **-3.92 over 12
tables**), `cl_new_long3_C` (27), `cl_raise_S2` (30) — with four trumps and a
singleton in the suit they have just bid, an eight-card fit at the two level is
a better description than a five-card club suit at the three.  No fallback is
deleted: `2S` is already covered by `cl_raise_S2`/`cl_doubler_raise_S`.

**VERIFIED.** `2S cl_doubler_min_raise_S fit=1.000 prio=32.5` chosen;
`cl_doubler_raise_S` sits at fit 0.800 (13 points, band 17-19) as designed.

**Template.** `expand: { X: [C, D, H, S] }` with `partner_suit: $X`,
`suits: { $X: [4,13] }`, id `cl_doubler_min_raise_$X`, and the same four rungs
one level higher (`cl_doubler_min_raise3_$X`) to mirror the existing
`cl_doubler_raise3_$X`.  Same family into `general_uncontested_continuation`
(`uc_doubler_raise_$X` already exists there at 17-19) and
`general_balancing_low`.

---

## Board 803 — table A, call 1, seat N: `P` (`oc1C_pass`)

Over 1C, N holds `AQ85.9852.AT74.6` — 4-4-4-1 with the singleton in their suit,
10 HCP, nobody vulnerable.  `oc1C_X` wants 11-16 and misses by exactly one
point (fit 0.800), so the hand passes.  BEN doubles at 0.79.

**Missing agreement.** Perfect 4-4-4-1 takeout shape with the singleton in
their suit is worth a king: the double starts at 10, not 11.

```yaml
# context: overcalls_of_1C   (insert before oc1C_1NT)
      - id: oc1C_X_shape
        call: X
        priority: 69
        requires:
          hcp: [9, 11]
          suits: { C: [0, 1], S: [4, 4], H: [4, 4], D: [4, 4] }
        shows: "takeout double a king light: perfect 4-4-4-1 with the singleton in their suit"
        establishes: { forcing: one_round }
```

**Answering seat.** `forcing: one_round` — the answering seat is
`advance_takeout_double` + `advance_takeout_double_suits_C`, which already
exist and already carry the 0-8 / 9-11 / cue ladders.  Nothing new is needed;
the double promises a *king less* than before, so the advance's own bands are
unchanged (they are stated in advancer's points, not in combined values).

**Endangers.** Above: `oc1C_1NT` (82) — a 15-18 balanced cannot be 4-4-4-1 with
a singleton, so no collision.  Below: `oc1C_1S`/`oc1C_1H` (71) and `oc1C_1D`
(70) all need a five-card suit, which `4-4-4-1` makes impossible; `oc1C_pass`
(25, whole corpus -0.32 over 125 tables) is the rung it actually takes over.
Deliberately placed at **69, below every natural overcall**, so a hand that has
a real suit still bids it.

**VERIFIED.** `X oc1C_X_shape fit=1.000 prio=69` chosen over `P oc1C_pass
fit=1.000`.  Control: a 14-count with five spades still bids 1S at 71.

**Template.** Four copies, one per context: `oc1C_X_shape`, `oc1D_X_shape`
(`suits: { D: [0,1], S: [4,4], H: [4,4], C: [4,4] }`), `oc1H_X_shape`,
`oc1S_X_shape`.  These contexts are not templated in the file, so this is four
hand-written rungs, not an `expand`.

---

## Board 864 — NOTHING-WRONG

**What I checked.** Table B call 5 (E `2S`, `xd_run_S2`, BEN wants 2H): running
a doubled 1NT to a five-card suit rather than a three-card one is correct
bridge, and BEN's 2H is *two tricks worse double-dummy* (E takes 7 in spades,
5 in hearts).  `xd_run_S2` runs **+0.67 over 3 tables** whole-corpus.  Table A:
N's 19-count doubled the balancing 1NT (`o4b_X_C`, right), then passed E's 2H
runout — but N does not get to act over 2H (S and W are in between), and by the
time N speaks the standing bid is W's 2S, which makes eight tricks
double-dummy, so both the penalty double (-470) and 3C (-100 vs -110) are
worse than the pass.  BEN agrees with every N/S call at table A.

The board was lost to card-play/par, not to an agreement.  The best
competitive observation I have is negative and worth recording: the runout
ladder `xd_run_$X` has no comparative test between a bad five and a decent
four, and I looked for one here and could not justify it — 2D (a 9872 fourth)
happens to be the winning runout double-dummy on this deal only.

---

## Board 883 — table A, call 5, seat N: `P` (`cl_pass`)

`1S P P X 2S`.  Partner balanced with a takeout double, RHO rebid 2S, and N —
`5.QJ63.842.KJT65`, 7 HCP, singleton spade, five clubs — passed.  3C by N makes
nine tricks: +110 instead of -110.

**Missing agreement.** When they bid over partner's takeout double the advance
is not cancelled: with a five-card suit and a singleton in their suit I still
answer the double.

```yaml
# context: general_competitive_low   (insert before cl_doubler_raise_C)
      - id: cl_advance_x2_C
        call: 2C
        priority: 28.5
        when: { unbid_suit: C, cheapest_in_suit: true, partner_last_call_was_double: true,
                i_have_acted: false, side_has_acted: true }
        requires: { suits: { C: [4, 13] }, evals: { total_points: [0, 11] } }
        shows: "answering partner's takeout double in my own suit, forced by the double"
        establishes: { forcing: non_forcing }
      - id: cl_advance_x3_C
        call: 3C
        priority: 28.5
        when: { unbid_suit: C, cheapest_in_suit: true, partner_last_call_was_double: true,
                i_have_acted: false, side_has_acted: true }
        requires: { suits: { C: [4, 13] }, evals: { total_points: [0, 11] } }
        shows: "answering partner's takeout double in my own suit, forced by the double"
        establishes: { forcing: non_forcing }
```

This is a **pure sibling gap**: `ch_advance_x3_$X` / `ch_advance_x4_$X` already
exist verbatim in `general_competitive_high` at priority 28.5, and
`general_competitive_low` — the context that owns every one- and two-level
auction, i.e. most of them — never got them.  The YAML above is the
low-context twin with the levels shifted down.

**Answering seat:** none — non-forcing; the doubler's continuations
(`cl_doubler_raise_$X`, and board 774's new minimum band) already answer it.

**Endangers.** Above: `cl_negative_X2` (33) and `cl_takeout_X` (36) are
excluded by `partner_last_call_was_double`/`i_have_acted`.  Below:
`cl_new_C2`/`C3` (26/27, which want 10+ and 14+ points and are exactly what
starves this seat), `cl_raise_*` (30/31, which need `partner_suit` and a double
names none), and `cl_pass` (20).  With 0-11 and a four-card unbid suit opposite
a takeout double, naming the suit is what the double asked for.

**VERIFIED.** `3C cl_advance_x3_C fit=1.000 prio=28.5` chosen over `P cl_pass
fit=1.000`.

**Template.** `expand: { X: [C, D, H, S] }`, ids `cl_advance_x2_$X` and
`cl_advance_x3_$X` — eight rungs, an exact mirror of the eight that already
exist one context along.

---

## Board 905 — table A, call 7, seat N: `2NT` (`uc_nt2`)

`P P 1D 1S P 1NT P`.  I overcalled 1S on `QJ763.T5.A986.A3`, partner advanced
1NT, and I raised to 2NT with a five-card spade suit and 11 HCP.  -50 against
+90 at the other table.  `uc_nt2` is a standing open item (21 tables, -1.57)
and, unlike `cl_nt1`/`ballow_nt1`, it denies no shape at all.

**Missing agreement.** The overcaller with a five-card suit rebids the suit
over partner's notrump advance; 2NT denies a rebiddable suit.

```yaml
# context: general_uncontested_continuation   (insert before uc_doubler_raise_C)
      - id: uc_rebid_five_S
        call: 2S
        priority: 28.5
        when: { my_suit: S, cheapest_in_suit: true, i_have_acted: true }
        requires:
          suits: { S: [5, 5] }
          evals: { total_points: [10, 15], "suit_quality(S)": [0.5, 9] }
        shows: "rebidding the five-card suit I bid rather than notrump: partner's notrump advance is not a fit"
        establishes: { forcing: non_forcing }
```

**Answering seat:** none — non-forcing sign-off in a known 5-2 or better.

**Endangers.** Above: `uc_nt3` (29) keeps 13-19 balanced, and `uc_rebid_S2`
(29) keeps the six-card version — both correctly outrank the five-card rebid.
Below: `uc_nt2` (28, the target), `uc_new_*2` (26/26.5).  Every more specific
opener's-rebid context (`opener_rebid_1M_1NT` at 51-57 etc.) is far above 28.5,
so no constructive sequence moves.

**VERIFIED.** `2S uc_rebid_five_S fit=1.000 prio=28.5` chosen over
`2NT uc_nt2 fit=1.000 prio=28`.

**Template.** `expand: { X: [C, D, H, S] }` → `uc_rebid_five_$X` at the two and
three levels, and the same four rungs into `general_competitive_low`
(`cl_rebid_five_$X`) and `general_balancing_low`, where the identical hole
exists.

---

## Board 918 — table B, call 5, seat W: `2C` (`ob_1D1H_2C`)

`P 1D P 1H P`, W holds `J8.T53.AKJ3.KQ52` — 2=3=4=4, 14 HCP, balanced.
`ob_1D1H_2C` (58) beats `ob_1NT` (57.5) by half a point with both at fit 1.000,
so the engine conceals a balanced 12-14 behind a four-card second suit.
Whole-corpus `ob_1D1H_2C` is **-3.57 over 7 tables**.

This is a constructive board and the other reviewer owns it; the competitive
reason it belongs here is that hiding a balanced minimum behind a two-level
minor gives the opponents a cheap, safe entry the 1NT rebid denies them.

**Missing agreement.** With a balanced 12-14 and no fit, 1NT describes the hand
before a four-card second suit does.

```yaml
# context: opener_rebid_1m_1M   (expand: { m: [C, D], M: [H, S] }; insert before ob_1NT)
      - id: ob_1NT_flat
        call: 1NT
        priority: 58.5
        requires:
          hcp: [12, 14]
          evals: { balanced: [1, 1] }
          not: { suits: { $M: [4, 13] } }
        shows: "balanced 12-14 with no fit: 1NT describes the hand before a four-card second suit does"
        establishes: { forcing: non_forcing }
```

Note the `not: { suits: { $M: [4,13] } }` is copied verbatim from `ob_1NT` so
the rung can never be a superset that swallows a four-card raise.

**Answering seat:** none — `responder_rebid_after_1NT_rebid` already answers a
1NT rebid, which is precisely why 1NT is the better call: 2C has a much thinner
answering ladder.

**Endangers.** Above: `ob_raise_*` (76-80) and `ob_1D1H_1S` (60) still win — a
four-card major is shown before notrump (control run below).  Below:
`ob_1D1H_2C` (58, the target), `ob_1NT` (57.5, same call), `ob_1D1H_3C_jump`
(57, 18+, cannot fit 12-14), `ob_2NT` (56, 18-19), `ob_rebid_2D` (50, needs
5+ and `balanced` denies a 6-card suit here only if the hand is genuinely
balanced — a 6-3-2-2 is not `balanced`, so the six-card rebid survives).

**VERIFIED.** `1NT ob_1NT_flat fit=1.000 prio=58.5` chosen over `2C
ob_1D1H_2C fit=1.000 prio=58`.  Control: `KQ85.T53.AKJ3.Q2` (four spades) still
bids `1S ob_1D1H_1S` at 60.

**Template.** The context is already `expand: { m: [C,D], M: [H,S] }`, so one
rung becomes four.  The identical half-point inversion exists in
`opener_rebid_1H_1S` — check `ob_1H1S_2m` against `ob_1NT` there before
shipping.

---

## Board 991 — table A, call 7, seat S: `P` (`ballow_pass`)

`P 1H X XX 2D P P`.  Partner opened, I redoubled, they ran to 2D and it came
back to me holding `753.A3.AJ92.J865` — 10 HCP and **AJ92 of their trump suit**
— and I passed it out undoubled for +500.  2D doubled, vulnerable, three down,
is +800; the other table made +630.

**Missing agreement.** After our redouble their escape does not get to play
undoubled: with four of their trumps and defensive values the reopening double
is penalty.

```yaml
# context: general_balancing_low   (insert before ballow_reopen_X2)
      - id: ballow_pen_X
        call: X
        priority: 42
        when: { their_last_bid_suit: true, side_has_acted: true, we_bid_last: false,
                i_have_acted: true, we_hold_contract: false }
        requires:
          hcp: [9, 40]
          evals: { standing_suit_length: [4, 13], quick_tricks: [2, 12] }
        shows: "penalty double of the suit they ran to: four of their trumps and defensive values, our side already committed"
        establishes: { forcing: non_forcing }
```

`standing_suit_length` — not `suit_length(their)` — is deliberate: the known
trap is that `suit_length(their)` resolves to LHO's suit, and here I need my
length in the suit of the STANDING bid.

**Answering seat.** `forcing: non_forcing`, and the seat that must not misread
it is partner, who is already served by `general_pull_or_sit`
(`pattern: "... - X - P - ?"`).  That context's `adx_sit` / `adx_pull_*` rungs
answer a penalty double correctly today.  Nothing new is required — this is the
one place in the slice where the answering seat already exists and is why I was
willing to add a double at all.

**Endangers.** Above it: nothing (42 is the new top of this context).  Below:
`ballow_reopen_X`/`_X2` (41).  **These cannot collide**: both require
`max_their_suit_length: [0,2]`, and the standing suit IS one of their suits, so
a hand with four of it can never satisfy them.  That matters, because
`ballow_reopen_X` runs **+3.75 over 4 tables** and must not be displaced.  Then
`ballow_X` (40, needs `side_has_acted: false`, excluded), and the whole natural
ladder at 27-34 — with four of their trumps and two quick tricks, defending
doubled beats a two-level scramble.  No fallback deleted: `X` is already
covered here by `ballow_X`/`ballow_reopen_X`.

**VERIFIED.** `X ballow_pen_X fit=1.000 prio=42` chosen over `P ballow_pass
fit=1.000`.

**Template.** No suit expansion.  Sibling into `general_balancing_high` as
`balhigh_pen_X` (same gates, `standing_suit_length: [4,13]`), and consider the
direct-seat twin in `general_competitive_low` only after this one is measured —
the direct seat has a live LHO and the double is far more dangerous there.

---

## Board 23 — table A, call 1, seat N: `P` (`oc1D_pass`)

Over 1D, N holds `AQ52.763.K43.KJ2` — 13 HCP, 4-3-3-3 with the four-card major.
`oc1D_X` demands `D: [0,2]`; N has three, fit 0.349.  BEN doubles at **0.97**.
`oc1D_pass` runs -0.74 over 137 tables.

**Missing agreement.** Nobody opens a three-card major but everybody opens a
three-card minor: the takeout double of 1C or 1D may hold three of their suit,
provided there is no long suit and at least three cards everywhere else.

```yaml
# context: overcalls_of_1D   (insert before oc1D_1NT)
      - id: oc1D_X_flat
        call: X
        priority: 69
        requires:
          hcp: [12, 16]
          suits: { D: [3, 3], S: [3, 4], H: [3, 4], C: [3, 4] }
        shows: "takeout double of their prepared minor: 12-16, three cards in their suit and at least three in every other"
        establishes: { forcing: one_round }
```

**Answering seat.** `forcing: one_round`; answered by
`advance_takeout_double` + `advance_takeout_double_suits_D`, which exist.  The
double now promises three, not two, of their suit — advancer's bands do not
move because they are expressed in advancer's own points and suit lengths.

**Endangers.** Above: `oc1D_1NT` (82) still wins with 15-18 balanced and a
stopper (verified control), which is right — 1NT is the more descriptive call
on those.  `oc1D_X` (72) still wins with genuine shortness.  Below: every
natural overcall (70-71) needs a five-card suit, and `suits: {S: [3,4], H:
[3,4], C: [3,4]}` makes one impossible; the rung it actually takes over is
`oc1D_pass` (25).

**This is the largest behaviour change I propose.**  Every 12-16 hand with
exactly three of their minor and no five-card suit starts doubling instead of
passing, in all four `overcalls_of_1x` contexts.  It should be screened as its
own experiment, not bundled.

**VERIFIED.** `X oc1D_X_flat fit=1.000 prio=69` chosen; controls: a 5-spade
14-count still overcalls 1S; a balanced 16 with a diamond stopper still bids
1NT at 82.

**Template.** Four hand-written copies (`oc1C_X_flat`, `oc1D_X_flat`,
`oc1H_X_flat`, `oc1S_X_flat`) — but for the two MAJOR openings the shortness
requirement is genuine bridge and the rung should be dropped, so in practice
this is **two rungs, over the two minors only**.  See board 512 for the 1C twin.

---

## Board 27 — table B, call 0, seat W: `P` (`open_pass`)

`JT6.K976542.T2.2` — a seven-card heart suit, 4 HCP, first seat, **vulnerable**.
`open_3H_vul` wants 5-9 (fit 0.800) and `open_weak_2H_vul` wants exactly six
(fit 0.035), so the hand between the two rungs passes.  BEN opens 2H at 0.73.

**Missing agreement.** A seven-card suit too weak in points for a vulnerable
three-level preempt opens a weak two — the six-card ceiling on the weak two is
a maximum only when the three-level preempt is actually available.

```yaml
# context: openings   (insert before open_1NT)
      - id: open_weak_2H_vul7
        call: 2H
        priority: 59
        requires:
          suits: { H: [7, 13], S: [0, 3] }
          hcp: [3, 6]
          evals: { "quick_tricks_outside(H)": [0, 2] }
        shows: "weak two on a seven-card suit whose quality will not stand the vulnerable three level"
        establishes: { forcing: non_forcing }
        when: { we_vulnerable: true, opening_seat: [1, 2, 3] }
```

**Answering seat.** `resp_weak2` (`2$W - P - ?`) already answers a weak two,
and `resp_weak2_newsuit_H` and `weak2_feature_answer_H` already answer the
continuations.  The rung deliberately reuses the weak-two vocabulary rather
than inventing a call precisely so the answering ladder is already built — the
round-17 lesson applied.

**Endangers.** Deliberately placed at **59, BELOW `open_3H_vul` (60)**, so a
five-to-nine-count with a good suit still preempts at the three level on the
fast path; `open_3H_vul` runs **+5.00 over its 1 table** and must not move.
Above 59 and reachable: `open_weak_2H_vul` (65) keeps the six-card hands,
`open_4H` (61) keeps the eight-card hands, `open_1H` (80) keeps the openers.
Below: `open_pass` (20), the rung it takes over.  The `S: [0,3]` guard is
copied from `open_weak_2H_vul` verbatim so no four-card-major hand slips in.

**VERIFIED.** `2H open_weak_2H_vul7 fit=1.000 prio=59` chosen over
`P open_pass fit=1.000`; `3H open_3H_vul` sits at 0.800 exactly as before.

**Template.** `expand: { W: [D, H, S] }` with `id: open_weak_2$W_vul7` and the
matching other-major guard.  No non-vulnerable twin is needed: `open_3W_nv`
already accepts 3-9 HCP, so the gap is a vulnerability artefact.

---

## Board 76 — table B, call 3, seat W: `P` (`open_pass_4th`)

`P P P`, W holds `86.AT.KJ9864.Q43`, 10 HCP, six diamonds, vulnerable both.
Rule of 15 fails on two spades, so the board is passed out for 0 while the
other table let the same hand play 2D for +110.

**Missing agreement.** Fourth seat with a six-card suit and 9-11 opens a weak
two and buys the contract, rather than passing the board out — the rule of 15
governs one-level openings, where partner will respond, not preempts.

```yaml
# context: openings   (insert before open_1NT)
      - id: open_weak_2D_fourth
        call: 2D
        priority: 63
        requires:
          suits: { D: [6, 6], H: [0, 3], S: [0, 3] }
          hcp: [9, 11]
          evals: { "suit_quality(D)": [1, 9], "quick_tricks_outside(D)": [0, 3] }
        shows: "fourth-seat weak two: a six-card suit and 9-11, buying the contract cheaply rather than passing the board out"
        establishes: { forcing: non_forcing }
        when: { opening_seat: [4] }
```

**Answering seat.** `resp_weak2` again — no new machinery.

**Endangers.** Above: `open_1D` (74) and `open_1D_rule15` (75) still win at 12+
or when the rule of 15 is satisfied; the `hcp: [9,11]` ceiling was chosen (down
from 12) precisely so it can never race the one-level opening.  `open_weak_2D_vul`
(64) still wins with 7-10 and a good suit.  Below: `open_pass_4th` (22) and
`open_pass` (20).  The `S: [0,3]` guard means we never open a weak two holding
the spades we would rather defend with.

**UNTESTED-in-corpus, VERIFIED-in-engine.** The trace is clean —
`2D open_weak_2D_fourth fit=1.000 prio=63` chosen, and the control
`KJ864.A.KJ9864.3` (five spades) still opens 1S at 81.  But **`open_pass_4th`
runs 0.00 over 4 tables whole-corpus**, so there is no evidence at all that
this population is losing money; this is the most speculative rung in my list
and should be screened separately or dropped.

**Template.** `expand: { W: [D, H, S] }` → `open_weak_2$W_fourth`, with the
higher-major guard adjusted per suit.  A fourth-seat 2S is much safer than a
fourth-seat 2D (we own the spades); if only one ships, ship 2S.

---

## Board 78 — table B, call 1, seat W: `X` (`v1NT_X`)

Over their 1NT, W holds `.AKQJ87.J632.KQT` — a void, a six-card suit headed by
AKQJ, and 16 HCP.  `v1NT_2H` is capped at 15 (fit 0.800), so the only rung left
is the penalty double, and partner with no defence in hearts had to sit.
`v1NT_X` runs -1.00 over 5 tables.

**Missing agreement.** A one-suiter with a void has playing strength, not
defence: over their notrump the ceiling on the natural suit overcall is 19, not
15, and the strong one-suiter bids rather than doubles.

```yaml
# context: defense_vs_1NT   (insert before v1NT_X)
      - id: v1NT_2H_big
        call: 2H
        priority: 71
        requires:
          suits: { H: [6, 13] }
          hcp: [16, 19]
          features: [ "good_suit(H)" ]
        shows: "natural: a strong six-card one-suiter, 16-19 - too much playing strength to defend 1NT doubled"
        establishes: { forcing: non_forcing }
```

**Answering seat.** Non-forcing.  `advance_1NT_overcall` is for *our* 1NT
overcall; the advance of a natural two-level overcall of their notrump falls to
`general_competitive_low`'s raise/new-suit/pass ladder, which is authored.  The
rung shows 16-19, one band above `v1NT_2H`'s 8-15, so partner's raise arithmetic
is well defined.

**Endangers.** Above: `v1NT_X` (70) — with a void and a solid six-bagger,
bidding is the better description, and the double is retained for everything
that is not a good six-card suit at 16-19.  Below: `v1NT_2H` (61, the 8-15
band), `v1NT_pass` (30).  It is the only rung above the double in this context,
so a balanced 16-19 still doubles for penalty — which is the double's real job.

**VERIFIED.** `2H v1NT_2H_big fit=1.000 prio=71` chosen over `X v1NT_X
fit=1.000 prio=70`.

**Template.** `expand: { X: [C, D, H, S] }` → `v1NT_2$X_big`, keeping the
six-card floor for all four (the existing 2H/2S rungs take a good five at 8-15;
the strong version should demand six, because it is bidding over a double it
could have made).

---

## Board 98 — table A, call 2, seat N: `X` (`v3_D_X`)

Over their 3D preempt, N holds `AKQJ93.AJ5..7632` — a solid six-card spade suit
and a VOID in their suit, 15 HCP.  `v3_D_X` (70) outranks `v3_D_S` (64) with
both at fit 1.000, so we doubled; partner had nothing to say, E bid 5D and 4S
(cold, eleven tricks) was never found.

**Missing agreement.** A self-sufficient six-card major over their preempt is
an overcall, not a takeout double — the double asks partner to choose, and there
is nothing to choose.

```yaml
# context: defense_vs_preempt_D   (insert before v3_D_X)
      - id: v3_D_S_solid
        call: 3S
        priority: 71
        requires:
          suits: { S: [6, 13] }
          hcp: [13, 40]
          evals: { "two_of_top3(S)": [1, 1], "suit_quality(S)": [2.5, 9] }
        shows: "a self-sufficient six-card major over their preempt: overcall it, do not double for takeout"
        establishes: { forcing: non_forcing }
```

**Answering seat.** Non-forcing; `advance_overcall` and the generic raise
ladders answer a three-level overcall today.

**Endangers.** `v3_D_X` (70) — and this is the one demotion in my list that
needed the whole-corpus check, because **`v3_D_X` runs +1.60 over 5 tables: it
is a winner.**  That is why the gate is `two_of_top3` AND `suit_quality >= 2.5`
AND six cards: it can only fire on a suit that plays for itself opposite a void,
which is exactly the hand the double misdescribes.  Below: `v3_D_3NT` (66),
`v3_D_4S` (65), `v3_D_S` (64, same call), `v3_D_pass` (30).

**VERIFIED.** `3S v3_D_S_solid fit=1.000 prio=71` chosen; `X v3_D_X` remains
at fit 1.000 prio 70 for every hand that does not have the solid suit.

**Template.** `expand_pairs` over (their preempt suit, my suit) across the four
`defense_vs_preempt_*` contexts, which are not templated: 3 overcall suits ×
4 contexts, at whichever level is cheapest — realistically ship the two MAJOR
versions only (`v3_x_S_solid`, `v3_x_H_solid`), because a solid minor over a
preempt is a 3NT hand, not an overcall.

---

## Board 103 — table A, call 3, seat S: `2C` (`sw_2C`)

`1S P 1NT` and S, `KJ9.9762.K.AQJT5`, 14 HCP, **vulnerable**, comes in with 2C
in the sandwich seat holding a stiff king, four hearts and a five-card minor.
Down two, -200.  Whole corpus: `sw_2C` **-2.75/8**, `sw_2S` **-4.50/2**,
`sw_2H` **-2.67/6**; `sw_pass` -0.49/247.

**Missing agreement.** Vulnerable, between two bidding opponents, a five-card
suit and fewer than fifteen points stays out — the sandwich two-level overcall
needs six cards or a real hand.

```yaml
# context: sandwich_seat   (expand: { o: [C, D, H, S] }; insert before sw_X)
      - id: sw_pass_vul
        call: P
        priority: 67
        when: { we_vulnerable: true }
        requires:
          hcp: [10, 14]
          evals: { longest_suit_length: [0, 5] }
        shows: "vulnerable between two bidding opponents, a five-card suit and fewer than fifteen points stays out"
        establishes: { forcing: non_forcing }
```

**Answering seat:** none.

**Endangers.** The priority is chosen to the half-point.  Above 67 and
untouched: `sw_X` (70), the preemptive jumps `sw_3$X` (69.5) and `sw_2$X_jump`
(69), and the **one-level** overcalls `sw_1S`/`sw_1H` (68) — a five-card suit
biddable at the one level still gets bid.  Below 67 and silenced: exactly the
two-level overcalls `sw_2C/2D/2H/2S` (66) and board 199's new `sw_2H_long`
(66.5, which needs six cards and so cannot fit a `longest_suit_length: [0,5]`
hand anyway).  `sw_pass` (30) keeps the rest.

**VERIFIED.** `P sw_pass_vul fit=1.000 prio=67` chosen over `2C sw_2C
fit=1.000 prio=66`.  Two controls, both from this same slice:
board 582's `AKQ95.K96.T8.K96` (15 HCP) still bids `2S sw_2S`, and a vulnerable
12-count with five spades over `1C P 1D` still bids `1S sw_1S` at 68.

**Template.** The context is already `expand: { o: [C,D,H,S] }`, so one rung is
four.  No non-vulnerable twin — the whole point is the vulnerability.

---

## Board 166 — table A, call 4, seat S: `P` (`cl_pass`)

`1C 1D 1H 1S`.  I opened 1C, partner responded 1H over an overcall, RHO bid 1S,
and I passed with `AT8.Q74.A3.QJT32` — exactly three hearts and 13 HCP.  BEN
doubles at **1.00**: it is a support double.

**Missing agreement.** The support double does not disappear because the
auction was already competitive — `1C (1D) 1H (1S) X` still shows exactly three
hearts.

The cause is structural: `support_double`'s pattern is
`"1$m - P - 1$M - bid<2$M - ?"`, so the second call must be a PASS.  Widening
that context's pattern would shadow `general_competitive_low` wholesale (the
round-6 and round-12 trap), so the rung goes inside the generic context
instead:

```yaml
# context: general_competitive_low   (insert before cl_doubler_raise_C)
      - id: cl_support_X_H
        call: X
        priority: 34
        when: { partner_last_suit: H, their_last_bid_suit: true, side_has_acted: true,
                i_have_acted: true, standing_bid_level: [1], we_hold_contract: false }
        requires: { suits: { H: [3, 3] }, hcp: [12, 18] }
        shows: "support double: exactly three cards in the major partner bid at the one level"
        establishes: { forcing: non_forcing }
        convention: support_double
        alertable: true
```

**Answering seat.** Non-forcing and purely descriptive, but the seat that reads
it is responder, whose next turn falls to `general_competitive_low`'s raise
ladder — and the double having promised exactly three makes the direct raise
promise four, which is the canonical negative inference and already how
`support_double` is documented in `DECISIONS.md`.  The `support_double` context
also contains `sd_1NT`, `sd_raise`, `sd_rebid_2C`; none of them is reachable
here, which is why this is a rung and not a context.

**Endangers.** Above: `cl_takeout_X` (36) needs `side_has_acted: false`,
excluded.  Below: `cl_negative_X2`/`X1` (33) need `i_have_acted: false`,
excluded; `cl_raise_H2` (30) is the rung it takes over, and taking it over is
the entire content of the agreement.  **It deletes the code fallback `X` in
this seat** — measured: with two hearts or four hearts the fallback X
disappears and `cl_pass` takes the seat.  That subtraction is inert here,
because in the dossier's own candidate table the fallback X scored **0.727
against `cl_pass`'s 0.760** and was already losing.

**VERIFIED.** `X cl_support_X_H fit=1.000 prio=34` chosen over `P cl_pass
fit=1.000`.  Controls run: (a) the genuine `1C P 1H 1S` auction still goes to
the specific `support_double` context and `sd_double` at priority 85 — the new
rung does not shadow it; (b) two-heart and four-heart versions of the hand pass,
as above.

**Template.** `expand: { M: [H, S] }` → `cl_support_X_$M`, plus the redouble
twin `cl_support_XX_$M` (`when: { ..., their_last_bid_suit: false }`, `call: XX`)
to mirror `support_redouble`.  Four rungs.

---

## Board 198 — table A, call 10, seat N: `3H` (`ch_raise_H3`)

`P P 1H P 2H P P X P 3C`.  I opened, partner raised, I PASSED the raise
(limiting myself), they balanced with a double and ran to 3C — and I then
competed to 3H on `AKJ.87532.54.AJ7` with eight combined trumps.  Down two
vulnerable, -200.  `ch_raise_H3` runs -2.33 over 3 tables.

**Missing agreement.** Eight trumps between us is worth eight tricks: having
already passed partner's raise, I do not compete to the three level.

```yaml
# context: general_competitive_high   (insert before ch_penalty_X)
      - id: ch_pass_lott_H
        call: P
        priority: 31.5
        when: { partner_suit: H, standing_bid_level: [3], we_bid_last: false, i_have_acted: true }
        requires:
          suits: { H: [3, 13] }
          evals: { "lott_total_trumps(H)": [0, 8], total_points: [0, 15] }
        shows: "eight trumps between us is worth eight tricks: over their three-level action I defend"
        establishes: { forcing: non_forcing }
```

`lott_total_trumps` is registered with sharp tolerance (`_EVAL_S2` 0.4), so
`[0, 8]` really does exclude nine trumps rather than leaning.

**Answering seat:** none.

**Endangers.** Above: `ch_penalty_X` (38) and `ch_negative_X3` (33) both
survive, so a trump stack still doubles.  Below: `ch_raise_$M3` (31, the
target), `ch_rebid_$M3` (29), `ch_nt3` (29), `ch_new_*3` (27/27.5).  The
`total_points: [0,15]` ceiling is what keeps a 16+ hand free to bid game — a
16-count with an eight-card fit should still be looking for 4H.

**VERIFIED.** `P ch_pass_lott_H fit=1.000 prio=31.5` chosen over
`3H ch_raise_H3 fit=1.000 prio=31`.

**Template.** `expand: { X: [C, D, H, S] }` → `ch_pass_lott_$X`.  The
`general_competitive_low` twin should demand `lott_total_trumps <= 7` at the
two level, not 8 — eight trumps ARE worth the two level, which is why the
low-context version is a different rung and not a copy.

---

## Board 199 — table A, call 3, seat S: `P` (`sw_pass`)

`1S P 1NT`, S holds `AT.QJT963.K3.652` — a six-card heart suit, 10 HCP.
`sw_2H` wants 11-17 (fit 0.800) so we passed; BEN bids 2H.  Note this is the
*opposite* error to board 103 in the same context, and the two proposals are
built to coexist.

**Missing agreement.** The sandwich overcall's point floor drops when the suit
is six long — length is the reason to bid, and eight points with six good ones
is enough.

```yaml
# context: sandwich_seat   (expand: { o: [C, D, H, S] }; insert before sw_X)
      - id: sw_2H_long
        call: 2H
        priority: 66.5
        when: { unbid_suit: H }
        requires: { suits: { H: [6, 13] }, hcp: [8, 17], evals: { "suit_quality(H)": [1, 9] } }
        shows: "sandwich overcall on a SIX-card suit: 8-17"
        establishes: { forcing: non_forcing }
```

**Answering seat:** none — non-forcing; the generic advance ladders answer it.

**Endangers.** Above: `sw_X` (70), the jumps (69/69.5), the one-level overcalls
(68), and **board 103's `sw_pass_vul` (67)** — which cannot fit a six-card hand
because of its `longest_suit_length: [0,5]` gate, so the two rungs are disjoint
by construction.  Below: `sw_2H` (66, the 11-17 five-card version, same call)
and `sw_pass` (30).

**VERIFIED.** `2H sw_2H_long fit=1.000 prio=66.5` chosen over `P sw_pass
fit=1.000`; `sw_2H` sits at 0.800 as before.

**Template.** The context is already expanded over `o`, and the rung should be
written for all four suits: `sw_2C_long`, `sw_2D_long`, `sw_2H_long`,
`sw_2S_long` — four hand-written rungs,
`when: { unbid_suit: <suit> }` each, exactly as the existing `sw_2C`/`sw_2D`/
`sw_2H`/`sw_2S` are.  Do NOT add a second key to the context's `expand:` — that
is a cartesian product and would quadruple the contexts.

---

## Board 230 — table A, call 4, seat S: `3C` (`ballow_new_C3`)

`1NT 2D P P`.  I opened 1NT, they overcalled 2D, **partner passed**, RHO
passed, and I reopened with 3C on `A2.A96.QT8.AJT84`.  Down two, -200.

**Missing agreement.** After 1NT I have already described the hand and partner
has already declined to compete: I have nothing to reopen with.

```yaml
# context: general_balancing_low   (insert before ballow_reopen_X2)
      - id: ballow_pass_described
        call: P
        priority: 34
        when: { i_have_acted: true, we_bid_last: false, we_hold_contract: false }
        requires:
          hcp: [15, 17]
          evals: { balanced: [1, 1] }
        shows: "I have already shown a balanced 15-17 and partner could not act: there is nothing to reopen with"
        establishes: { forcing: non_forcing }
```

The `hcp: [15,17] + balanced` pair is the honest way to say "I am the hand that
opened or overcalled 1NT" without a `when` for it; it catches the 1NT overcaller
too, where the same captaincy logic applies.

**Answering seat:** none.

**Endangers.** Above: `ballow_reopen_X`/`_X2` (41, 16+ short in their suit,
+3.75/4 whole corpus) and board 991's `ballow_pen_X` (42) all survive — a 1NT
opener with genuine shortness or four of their trumps still doubles.  Below:
`ballow_nt2_balance` (33), `ballow_raise_*` (30-32), `ballow_nt2_strong` (30),
`ballow_new_*3` (27, the target, -0.25 over 4 tables — a thin denominator, so
this rung's value rests on the bridge, not on the corpus), `ballow_pass` (21).

**VERIFIED.** `P ballow_pass_described fit=1.000 prio=34` chosen over
`3C ballow_new_C3 fit=1.000 prio=27`; `ballow_pen_X` correctly sits at 0.349
(three diamonds, not four).

**Template.** No suit expansion.  Sibling `balhigh_pass_described` in
`general_balancing_high`; see board 548 for the `general_competitive_high` twin,
which is the same agreement with a different band.

---

## Board 258 — table A, call 2, seat N: `P` (`cl_pass`)

`2D 2S`.  Partner opened a weak two, they overcalled, and I hold
`75.Q95.Q965.KQJ2` — **four-card support, ten trumps between us**, non-vulnerable.
We passed; 4D down one (-50) beats their 2S making ten (-170).  BEN bids 4D.

**Missing agreement.** The Law raise exists in the majors and not in the minors:
with ten trumps, non-vulnerable, the four level is right on shape.

```yaml
# context: general_competitive_low   (insert before cl_doubler_raise_C)
      - id: cl_raise_lott4_D
        call: 4D
        priority: 32
        when: { partner_suit: D, is_competitive: true, we_vulnerable: false }
        requires:
          suits: { D: [4, 13] }
          evals: { "lott_total_trumps(D)": [10, 26], total_points: [6, 40] }
        shows: "the Law at the four level in a minor: ten trumps our way, so the four level is right on shape"
        establishes: { forcing: non_forcing, agreed_suit: D }
```

Gates copied from `cl_raise_lott4_H` except that `their_fit: [8,26]` is dropped
— opposite a weak two they have not yet *shown* a fit, and waiting for them to
show one is waiting until 4D is no longer available — and `we_vulnerable: false`
is added in its place, copying the discipline of `ch_raise_lott_S4`.

**Answering seat:** none — non-forcing, `agreed_suit: D` set so the pass/pull
family reads it.

**Endangers.** Above: `cl_negative_X2` (33) still wins where it fits (on this
board it is at 0.349); `cl_takeout_X` (36) needs `side_has_acted: false`.
Below: `cl_raise_D3` (31), `cl_raise_D4` (27, the 11+-point version), the
natural three-level suit bids (27/27.5) and `cl_pass` (20).  With ten trumps and
a weak hand, four of the minor is the Law bid whether it makes or it is a save;
the `we_vulnerable: false` gate is what keeps that honest.

**VERIFIED.** `4D cl_raise_lott4_D fit=1.000 prio=32` chosen over `P cl_pass
fit=1.000`.

**Template.** `expand: { m: [C, D] }` → `cl_raise_lott4_$m`, plus the
five-level minor twin `cl_raise_lott5_$m` on eleven trumps (the file has 55
rules at the five level and 0 at the seven; this is one of the cheap ones), and
the same two rungs into `general_competitive_high` and `general_balancing_low`.

---

## Board 344 — table A, call 6, seat S: `P` (`cl_pass`)

`P P 1D X 1S 2H`.  I opened a light third-seat 1D on `.AT2.KT543.K9865` —
5-5 in the minors with a **void in spades** — they doubled, partner bid my void,
they bid 2H, and I passed.  Nothing in the file lets a 5-5 shape speak at the
three level: `cl_new_C3` wants 14+ points and `cl_new_long3_C` wants six cards.

**Missing agreement.** A five-card second suit is worth the three level when I
hold a void — shortness is playing strength, and partner is in my void.

```yaml
# context: general_competitive_low   (insert before cl_doubler_raise_C)
      - id: cl_new_void3_C
        call: 3C
        priority: 27.2
        when: { unbid_suit: C, cheapest_in_suit: true, i_have_acted: true }
        requires:
          suits: { C: [5, 13] }
          evals: { void: [1, 1], total_points: [10, 40] }
        shows: "a five-card second suit is worth the three level when I hold a void"
        establishes: { forcing: non_forcing }
```

**Answering seat:** none — non-forcing; it is a shape correction, and partner's
existing preference/raise ladder answers it.

**Endangers.** Above: `cl_nt3` (29) — a hand with a void is never `balanced`, so
it cannot fit; `cl_rebid_jump_$X` (31) needs six of my own suit.  Below:
`cl_new_C3`/`cl_new_long3_C` (27, same call, so the ordering is cosmetic) and
`cl_pass` (20), the rung it takes over.  Because it demands an actual void, the
population is small and shapely, which is the point.

**VERIFIED.** `3C cl_new_void3_C fit=1.000 prio=27.2` chosen over `P cl_pass
fit=1.000`.

**Template.** `expand: { X: [C, D, H, S] }` → `cl_new_void3_$X`, and the
two-level twin `cl_new_void2_$X`.  Same family into
`general_competitive_high` and `general_balancing_low`.

---

## Board 433 — table A, call 7, seat N: `4D` (`balhigh_rebid_D4`)

`P 2S 3C 3D 4C P P`.  Partner opened a weak two, I bid my own seven-card
diamond suit at the three level (3D makes exactly nine tricks — that call was
fine), they competed to 4C, partner passed it, and I bid **again** at the four
level with `T.74.AJT9872.KQ5`, ten HCP.  Down one, -50.

**Missing agreement.** Opposite a preempt, a suit I have already shown once and
partner could not raise is a partscore: at the four level I defend.

```yaml
# context: general_balancing_high   (insert before balhigh_reopen_X2)
      - id: balhigh_pass_repeat
        call: P
        priority: 30
        when: { my_suit: D, i_have_acted: true, standing_bid_level: [4], we_hold_contract: false }
        requires:
          hcp: [0, 11]
          evals: { quick_tricks: [0, 2] }
        shows: "I have already shown this suit and partner could not raise it: at the four level I defend"
        establishes: { forcing: non_forcing }
```

**Answering seat:** none.

**Endangers.** Above: `balhigh_reopen_X`/`_X2` and the penalty double stay
free, and every raise of partner's suit (32) stays free.  Below:
`balhigh_rebid_$X4` (29, the target, -0.33 over 3 tables — thin, so this rests
on the bridge), `balhigh_new_*4` (28/28.5), `balhigh_nt*`, `balhigh_pass` (21).
The `hcp: [0,11]` and `quick_tricks: [0,2]` ceilings are what leave a real hand
free to bid on.

**VERIFIED.** `P balhigh_pass_repeat fit=1.000 prio=30` chosen over
`4D balhigh_rebid_D4 fit=1.000 prio=29`.

**Template.** `expand: { X: [C, D, H, S] }` → `balhigh_pass_repeat_$X` (var
must END the id, so name it `balhigh_pass_repeat_$X`), and a five-level twin
with `standing_bid_level: [5]`.

---

## Board 474 — table B, call 9, seat W: `3H` (`uc_rebid_H3`)

`P 1H X 2C P 2H P 3C P`.  I opened 1H, they doubled, partner bid 2C, I rebid
2H, partner rebid 3C — a seven-card club suit — and I corrected to 3H holding
`KJ3.KT9863.Q5.KQ`, a doubleton club and 14 HCP.  3C makes nine tricks; 3H made
seven.  `uc_rebid_C3` runs -2.10 over 10 tables and is the *partner's* correct
call here; mine is the error.

**Missing agreement.** When partner bids and rebids a suit I hold two cards in,
that is a misfit auction and a minimum passes — correcting to my own six-card
major at the three level is one round too many.

```yaml
# context: general_uncontested_continuation   (insert before uc_doubler_raise_C)
      - id: uc_pass_misfit_C
        call: P
        priority: 29.5
        when: { partner_suit: C, i_have_acted: true, standing_bid_level: [3],
                we_hold_contract: false }
        requires:
          suits: { C: [0, 2] }
          hcp: [12, 14]
        shows: "partner has bid and rebid a suit I hold two cards in: with a minimum this is a misfit and I pass"
        establishes: { forcing: non_forcing }
```

**Answering seat:** none.

**Endangers.** Above: nothing that can fit a 12-14 with a doubleton in
partner's long suit — `uc_raise_C3`/`C4` (27) need three-card support,
`gst_rkc_*` (46) needs slam values.  Below: `uc_rebid_$M3` (29, the target),
`uc_nt3` (29 — and yes, this rung outranks a 13-19 balanced 3NT; the `hcp:
[12,14]` ceiling is what keeps the 15+ notrump hands free), `uc_new_*3` (27),
`uc_pass` (18).

**VERIFIED.** `P uc_pass_misfit_C fit=1.000 prio=29.5` chosen over
`3H uc_rebid_H3 fit=1.000 prio=29` and `3NT uc_nt3 fit=1.000 prio=29`.

**Template.** `expand: { X: [C, D, H, S] }` → `uc_pass_misfit_$X` (no `my_suit`
in the gate, so four rungs cover all twelve suit pairs), and the same four into
`general_competitive_low` and `general_competitive_high`.

---

## Board 506 — table B, call 7, seat E: `P` (`uc_pass`)

`P 1C P 1S P 2H P` — partner **reversed**, which is forcing, and I passed it out
with `QJ9753.73.J973.9`, four HCP and six spades.  This is the
starved-forcing-seat species for the fifth time in the ledger: `rrevh_2S` wants
8+ and **never fires in the whole corpus**, and the catch-all pass takes a force
at fit 1.000.

**Missing agreement.** The reverse is forcing: with 0-7 and five spades I rebid
my suit rather than pass a force.

```yaml
# context: responder_reverse_1C1S2H   (insert before rrevh_2S)
      - id: rrevh_2S_min
        call: 2S
        priority: 65.8
        requires: { suits: { S: [5, 13] }, hcp: [0, 7] }
        shows: "the reverse is forcing: with 0-7 and five spades I rebid my suit rather than pass a force"
        establishes: { forcing: non_forcing }
```

**Answering seat — and this is the part that must ship with it.**  `establishes:
forcing: non_forcing` is deliberate: it lets opener PASS 2S, which is the whole
safety of the rung.  The seat `1C - P - 1S - P - 2H - P - 2S - P - ?` has **no
context** — it falls to `general_uncontested_continuation`, where `uc_raise_S3`
/ `uc_raise_S4` / `uc_pass` are authored and adequate for a non-forcing 2S.  If
this rung is ever made `one_round` forcing instead, a
`opener_over_reverse_2S` context must ship with it; as written, it must not be.

**Endangers.** Above: `rrevh_2S` (66, the 8+ version, same call — ordering is
cosmetic), `rrevh_3H` (65 is BELOW, see next).  Below: `rrevh_3H` (65, raising
the reverse suit — with two hearts it cannot fit), `rrevh_2NT` (64),
`rrevh_3NT` (63), and the whole `uc_*` toolkit at ≤32 including `uc_pass` (18),
which is the rung it takes over.

**VERIFIED.** `2S rrevh_2S_min fit=1.000 prio=65.8` chosen over
`P uc_pass fit=1.000`.

**Template.** Two hand-written copies: `responder_reverse_1C1S2H` and its clone
`responder_reverse_1D1S2H` (which the file already carries verbatim), plus
`responder_reverse_rebid_major` (`1C - P - 1$M - P - 2D - P - ?`) and
`responder_reverse_1C1S2H`'s heart analogues — every reverse-answering context
has the same 8-point floor and the same starved seat below it.

---

## Board 512 — table A, call 2, seat S: `P` (`oc1C_pass`)

Over 1C, S holds `8632.AQJ.KJ4.K85` — 14 HCP, 4-3-3-3 with the four-card major
and three clubs.  BEN doubles at **0.97**.  Same defect as board 23, other minor.

**Missing agreement.** As board 23: the takeout double of 1C may hold three
clubs.

```yaml
# context: overcalls_of_1C   (insert before oc1C_1NT)
      - id: oc1C_X_flat
        call: X
        priority: 69
        requires:
          hcp: [12, 16]
          suits: { C: [3, 3], S: [3, 4], H: [3, 4], D: [3, 4] }
        shows: "takeout double of their prepared minor: 12-16, three cards in their suit and at least three in every other"
        establishes: { forcing: one_round }
```

**Answering seat.** `advance_takeout_double` + `advance_takeout_double_suits_C`,
both already authored.

**Endangers.** Identical analysis to board 23.  Note in particular that
`oc1C_1NT` (82) still wins on 15-18 balanced with a club stopper: this hand has
14 and misses it (fit 0.800), which is exactly the band the double should own.
It takes over `oc1C_pass` (25, -0.32 over 125 tables).

**VERIFIED.** `X oc1C_X_flat fit=1.000 prio=69` chosen; control with five
spades still gives `1S oc1C_1S` at 71.

**Template.** Ships as one family with board 23: `oc1C_X_flat` and
`oc1D_X_flat` only.  Do **not** write the major-suit versions — over 1H or 1S
the shortness requirement is real bridge.

---

## Board 548 — table A, call 8, seat N: `3H` (`ch_new_H3_hi`)

`1NT P 2H P 2S P P 3D`.  I opened 1NT, partner transferred to spades and PASSED
2S — a sign-off — and when they balanced with 3D I introduced my five-card heart
suit at the three level on `K82.AT974.Q5.AQ5`.  Down two, -200.
`ch_new_H3_hi` **never fires anywhere else in the corpus**.

**Missing agreement.** With a balanced 14-17 already shown and no six-card suit,
their three-level balance gets no second bid from me.

```yaml
# context: general_competitive_high   (insert before ch_penalty_X)
      - id: ch_pass_described
        call: P
        priority: 30
        when: { i_have_acted: true, side_has_acted: true, standing_bid_level: [3],
                we_bid_last: false }
        requires:
          hcp: [14, 17]
          evals: { balanced: [1, 1], longest_suit_length: [0, 5] }
        shows: "I have already shown a balanced 14-17 and hold no six-card suit: their three-level balance gets no second bid from me"
        establishes: { forcing: non_forcing }
```

**Answering seat:** none.

**Endangers.** Above: `ch_penalty_X` (38) and `ch_negative_X3` (33) survive —
a hand with defence still doubles; `ch_raise_$M3` (31) and the LOTT raises (32)
survive, so a genuine fit still competes.  Below: `ch_rebid_*` (29), `ch_nt3`
(29), `ch_new_*3`/`_hi` (27/27.5, the target), `ch_pass` (22).  The
`longest_suit_length: [0,5]` gate is what leaves a six-card suit free to be
rebid; `balanced` is what leaves a shapely 15 free.

**VERIFIED.** `P ch_pass_described fit=1.000 prio=30` chosen over
`3H ch_new_H3_hi fit=1.000 prio=27.5`.  Cross-checked against board 198
(12 HCP, outside the band — unaffected) and board 597 (12 HCP — unaffected).

**Template.** No suit expansion.  This and board 230's `ballow_pass_described`
are the same agreement in two contexts and should ship together, with the
`general_competitive_low` twin `cl_pass_described` (`standing_bid_level: [2]`,
same requires) and `balhigh_pass_described` — four rungs, one idea.

---

## Board 582 — NOTHING-WRONG

**What I checked.** The first divergence is table A call 4, seat S: `1H P 1NT P`
with `732.AQJT8.KQT.54`, passing the semi-forcing 1NT on a 5-3-3-2 twelve-count.
That is the textbook action for `forcing_nt: semi` and I will not propose
changing it; the 1NT went down three on a bad layout.

The competitive half of this board is where the profit was and it must not be
disturbed: at table B our E, `AKQ95.K96.T8.K96`, overcalled 2S in the sandwich
seat over the semi-forcing 1NT and made eight tricks for +110.  I ran that hand
as an explicit control against board 103's `sw_pass_vul` — 15 HCP is outside the
rung's `hcp: [10,14]` band, so `2S sw_2S` still wins at fit 1.000.  Board 582 is
the constraint that set that ceiling.

---

## Board 597 — table A, call 3, seat N: `P` (`ch_pass`)

`P 2S 3D`.  Partner opened a weak two, they overcalled three of a minor, and I
hold `J97.Q72.AJ9.A986` — **three-card support, nine trumps between us**, 12 HCP.
`ch_raise_S3` reaches fit 0.605 and loses to the catch-all, because its gate is
`rule_of_26: [22,99]` and opposite a 5-10 weak two that arithmetic can never get
there.

**Missing agreement.** The three-level competitive raise is a LAW bid — nine
trumps — not a combined-values bid; `rule_of_26` is the wrong test opposite a
preempt.

```yaml
# context: general_competitive_high   (insert before ch_penalty_X)
      - id: ch_raise_lott3_S
        call: 3S
        priority: 32
        when: { partner_suit: S, cheapest_in_suit: true, is_competitive: true }
        requires:
          suits: { S: [3, 13] }
          evals: { "lott_total_trumps(S)": [9, 26], total_points: [6, 40] }
        shows: "the Law at the three level: nine trumps our way, so three of the major is right on shape"
        establishes: { forcing: non_forcing, agreed_suit: S }
```

This is the missing rung of a family the file already believes in: the comment
above `cl_raise_lott4_$M` says in as many words that `rule_of_26` is "the right
test in a constructive auction and the wrong one in a contested one", and the
three-level version was never written.

**Answering seat:** none — non-forcing, `agreed_suit` set.

**Endangers.** Above: `ch_penalty_X` (38) and `ch_negative_X3` (33) survive;
board 198's `ch_pass_lott_$X` (31.5) is **mutually exclusive** with it by
construction (`lott_total_trumps <= 8` versus `>= 9`), which is the whole design
of the pair.  Below: `ch_raise_$M3` (31, the values version, same call),
`ch_new_*` (27-28.5), `ch_pass` (22).

**VERIFIED.** `3S ch_raise_lott3_S fit=1.000 prio=32` chosen over `P ch_pass
fit=1.000`, with `ch_raise_S3` still at 0.605.

**Template.** `expand: { M: [H, S] }` → `ch_raise_lott3_$M`; the minors want the
four-level version instead (board 258).  Also the `general_competitive_low`
twin at the two level with `lott_total_trumps >= 8`.

---

## Board 644 — table A, call 6, seat S: `3NT` (`r2c_nt_3NT`)

`2C P 2D P 2NT P` and S bids 3NT holding `962.632.T63.J763` — **one high card
point**.  Down two, -200.  Constructive board (the other reviewer's territory);
`r2c_nt_3NT` requires only "no four-card major" and has no point floor at all,
which is the documented "after a 2C opening partner's shown minimum is zero"
problem seen from the responder's side.

**Missing agreement.** Twenty-four plus one is not twenty-five: with 0-1
opposite a 22-24 notrump, pass.

```yaml
# context: r2c_after_2NT   (insert before r2c_nt_3NT)
      - id: r2c_nt_pass
        call: P
        priority: 61
        requires: { hcp: [0, 1] }
        shows: "0-1 opposite 22-24: twenty-five is not there, pass 2NT"
        establishes: { forcing: sign_off }
```

**Answering seat:** none — it ends the auction.

**Endangers.** Above: `r2c_nt_stayman` (80) and the transfers (81/82) survive,
so a bust with a five-card major still transfers, which is right and is the
reason the floor is 1 and not 3.  Below: `r2c_nt_3NT` (60, the target,
-1.00 over 3 tables — a thin denominator).

**VERIFIED.** `P r2c_nt_pass fit=1.000 prio=61` chosen over `3NT r2c_nt_3NT
fit=1.000 prio=60`.

**Template.** None — one rung.  The same zero-floor problem exists at
`r2c_2D_waiting` and `gf_new_3$X`; that is a whole-tree job and is out of scope
here.

---

## Board 664 — table B, call 3, seat W: `X` (`v3_S_X`)

Over their 3S, W holds `A9.AJ3.Q865.KQJ8` — a flat 17 with the ace of spades.
`v3_S_X` (70) beats `v3_S_3NT` (66) with both at fit 1.000, partner pulled to
4C, and we went minus.  BEN wants 3NT.  (The dossier's first divergence is our
2S opening at table A; I checked it and a 10-count with `QJ8764` is a weak two
in this system's own terms — `open_weak_2S_nv` is right, and BEN's 3S is not.)

**Missing agreement.** Over a three-level preempt, a balanced 16-21 with their
suit stopped bids 3NT; the takeout double is for hands short in their suit.

```yaml
# context: defense_vs_preempt_S   (insert before v3_S_X)
      - id: v3_S_3NT_flat
        call: 3NT
        priority: 71
        requires:
          hcp: [16, 21]
          suits: { S: [2, 3] }
          features: [ "stopper(S)" ]
          evals: { balanced: [1, 1] }
        shows: "balanced 16-21 with their preempt suit stopped: nine tricks in notrump, not a takeout double"
        establishes: { forcing: sign_off }
```

**Answering seat:** none — sign-off.

**Endangers.** `v3_S_X` (70), and the gate is built so it only fires where the
double is wrong: `suits: {S: [2,3]}` means a singleton or void still doubles
(control run: `8.AKJ3.AQ92.KQ98` with 18 still gives `X v3_S_X` at fit 1.000),
and `balanced` means a shapely 17 still doubles.  Below: `v3_S_3NT` (66, same
call), the four-level overcalls (64), `v3_S_pass` (30).  `v3_S_X`'s whole-corpus
denominator is **1 table, -3.00** — too thin to justify anything on its own,
which is why the gate is narrow and the argument is bridge, not statistics.

**VERIFIED.** `3NT v3_S_3NT_flat fit=1.000 prio=71` chosen over `X v3_S_X
fit=1.000 prio=70`.

**Template.** Four hand-written copies, one per `defense_vs_preempt_*` context
(`v3_C_3NT_flat`, `v3_D_3NT_flat`, `v3_H_3NT_flat`, `v3_S_3NT_flat`), with the
suit letter changed in `suits:` and `features:`.  Interacts with board 98: over
3D a hand can hold both a solid major (98's rung, 71) and a flat 3NT — they
cannot both fit, because `balanced` denies a six-card suit.

---

## Board 674 — table A, call 2, seat N: `P` (`cl_pass`)

`1NT 2C`.  Partner opened a strong notrump, they overcalled 2C, and I hold
`3.A984.KJT42.832` — eight HCP, five diamonds, a singleton spade.  Every rung in
the context wants ten points (`cl_new_D2` at fit 0.800) or a four-card major
without a five-card suit (`cl_negative_X2`, blocked by its own
`longest_suit_length: [0,4]`), so we sold out at the two level with 23 points.

**Missing agreement.** Opposite a partner who has shown a strong balanced hand
the floor for a five-card suit is 6 points, not 10 — the ten-point floor is a
floor for an unlimited partner.

```yaml
# context: general_competitive_low   (insert before cl_doubler_raise_C)
      - id: cl_new_strong2_D
        call: 2D
        priority: 26.8
        when: { unbid_suit: D, cheapest_in_suit: true, side_has_acted: true,
                i_have_acted: false, standing_bid_level: [2] }
        requires:
          suits: { D: [5, 13] }
          evals: { rule_of_26: [21, 99], total_points: [6, 40] }
        shows: "natural D opposite a partner who has shown a strong balanced hand: 5+ cards, 6+ points"
        establishes: { forcing: non_forcing }
```

`rule_of_26 >= 21` is the honest way to say "partner has shown 15+": there is no
`partner_min_hcp` evaluator, and `partner_shown_max` is a ceiling, not a floor.
`rule_of_26` is my total points plus the midpoint of partner's shown range, so
after a 15-17 notrump it adds 16 and after a simple raise it adds 7 — the gate
separates them cleanly.

**Answering seat:** none — non-forcing, and the 1NT opener's continuations fall
to the same context, where the raise ladder is authored.

**Endangers.** Above: `cl_negative_X2` (33) and board 852's
`cl_negative_X2_strong` (33.5) both still win when they fit — a four-card major
without a five-card suit still doubles.  Below: `cl_new_D2`/`_hi` (26/26.5, the
10-point version, same call) and `cl_pass` (20).  The `standing_bid_level: [2]`
and `i_have_acted: false` gates keep it to the seat it is written for.

**VERIFIED.** `2D cl_new_strong2_D fit=1.000 prio=26.8` chosen over `P cl_pass
fit=1.000`.

**Template.** `expand: { X: [C, D, H, S] }` → `cl_new_strong2_$X`, plus the
three-level twin `cl_new_strong3_$X`.  Same four into `general_balancing_low`.

---

## Board 764 — table A, call 8, seat N: `3NT` (`stmi_2S_3NT`)

`1NT P 2C P 2S P 2NT P` and I accept the invite with `KJ83.964.QJ3.AKQ` — a
flat 16 with three jacks and no source of tricks.  Down two.  Constructive
board; the competitive framing is only that a 4-3-3-3 sixteen has no way to
generate a ninth trick against a defence that has already been told everything.

**Missing agreement.** A flat sixteen declines the invite.

```yaml
# context: stayman_invite_accept_2S   (insert before stmi_2S_pass)
      - id: stmi_2S_pass_flat
        call: P
        priority: 61
        requires: { hcp: [16, 16], shapes: [ "4333" ] }
        shows: "declining the invite with a flat sixteen: no source of tricks"
        establishes: { forcing: sign_off }
```

**Answering seat:** none — sign-off.

**Endangers.** Above: nothing in this context.  Below: `stmi_2S_pass` (60, the
15-only decline) and `stmi_2S_3NT` (58, 16-17 accept, -1.50 over 2 tables — a
very thin denominator).  A 17 and every non-4333 sixteen still accept.

**VERIFIED.** `P stmi_2S_pass_flat fit=1.000 prio=61` chosen over
`3NT stmi_2S_3NT fit=1.000 prio=58`.

**Template.** Three hand-written copies: `stayman_invite_accept_2D`,
`_2H`, `_2S` (ids `stmi_2D_pass_flat`, `stmi_2H_pass_flat`,
`stmi_2S_pass_flat`), plus `nt_2NT_opener_decides`.  Board 861 is the 2D twin
and is why I did not also propose a rule there.

---

## Board 767 — NOTHING-WRONG

**What I checked.**  Table B call 4, seat W: `1C P 1H P` with
`QJ6.8.KQ76.AT765` — 3=1=4=5, a **singleton** in partner's hearts.  `ob_rebid_2C`
is right and BEN's 1NT is wrong: a 1NT rebid with a stiff heart is the error,
not the club rebid.  The 3NT two calls later is the documented
`responder_after_minor_rebid` ceiling and belongs to the constructive reviewer.

Table A: we (N/S) never had a competitive entry.  N held `74.9532.AJ95.KQ8`,
ten HCP with no suit and no shortness, while E/W bid 1C-1H-1NT-2D-3D-3NT; the
balancing seat never arrived because they never stopped below game, and a
double at any point is a phantom.  `oc1C_pass` at that seat runs -0.32 over 125
tables and is not indictable here.

No competitive agreement is missing on this board.

---

## Board 772 — table A, call 2, seat S: `1NT` (`oc1D_1NT`)

Over their 1D, S holds `A3.QJ852.KQT.KJT` — 16 HCP with a **five-card heart
suit**.  `oc1D_1NT` (82) beats `oc1D_1H` (71) with both at fit 1.000.  W then
jumped to 4S and the ten-card heart fit (partner held `KJ.KT976.92.9542`) was
never found; 3H makes ten tricks.  `oc1D_1NT` runs **-4.57 over 7 tables**, the
worst overcall family in this slice.

**Missing agreement.** The 1NT overcall denies a five-card major: with 15-18 and
a five-card major, overcall the major, because the opponents will preempt and
the fit has to be found on the first round.

```yaml
# context: overcalls_of_1D   (insert before oc1D_1NT)
      - id: oc1D_1H_5M
        call: 1H
        priority: 83
        requires:
          suits: { H: [5, 13] }
          hcp: [15, 18]
          evals: { "suit_quality(H)": [1, 9] }
        shows: "overcall the five-card major even with 15-18 balanced: the 1NT overcall denies a five-card major"
        establishes: { forcing: non_forcing }
```

This is a deliberate asymmetry with the 1NT OPENING, which in this system may
contain a five-card major (`nt_with_5M: true`) — and the asymmetry is the
agreement.  Partner can use Stayman over an opening; over an overcall the
auction is contested and there is no second chance.

**Answering seat:** none — `advance_overcall` and the raise ladders answer a
one-level overcall.  The overcall now shows 8-18 rather than 8-16, so the
advancer's invitational band widens slightly; if that matters, add a
`oc1D_1H_5M`-specific rebid rung showing 15-18 on the second round.

**Endangers.** `oc1D_1NT` (82) on exactly the hands with a five-card major, and
`oc1D_1H` (71, same call, 8-16).  `suit_quality(H) >= 1` is what stops it firing
on a 5-3-3-2 with `xxxxx`.  Everything else in the context is below 82.

**VERIFIED.** `1H oc1D_1H_5M fit=1.000 prio=83` chosen over `1NT oc1D_1NT
fit=1.000 prio=82`; control `A32.QJ85.KQT.KJT` (four hearts) still bids 1NT.

**Template.** Eight hand-written rungs: two majors × four `overcalls_of_1x`
contexts, minus the two where the major is the opening suit — so
`oc1C_1H_5M`, `oc1C_1S_5M`, `oc1D_1H_5M`, `oc1D_1S_5M`, `oc1H_1S_5M`,
`oc1S_2H_5M` (six).

---

## Board 820 — table A, call 4, seat N: `2D` (`oc1H_2D`)

`P P P 1H` — I had already **passed**, we are **vulnerable**, and I overcalled
2D on `KJ62.K5.KJ874.74`: eleven points, a KJ-fifth suit and no shape.  They
doubled us into 3S and we went -200.  `oc1H_2D` runs -1.22 over 9 tables.

**Missing agreement.** Vulnerable, a five-card suit and fewer than thirteen
points is not a two-level overcall.

```yaml
# context: overcalls_of_1H   (insert before oc1H_1NT)
      - id: oc1H_pass_vul2
        call: P
        priority: 66
        when: { we_vulnerable: true }
        requires:
          hcp: [8, 12]
          evals: { longest_suit_length: [5, 5], quick_tricks: [0, 2] }
        shows: "vulnerable, a five-card suit and fewer than thirteen points is not a two-level overcall"
        establishes: { forcing: non_forcing }
```

**Answering seat:** none.

**Endangers.** The priority is chosen to sit in the gap: above 66 and untouched
are `oc1H_X` (72), `oc1H_1NT` (82) and the ONE-level overcall `oc1H_1S` (71) —
a five-card spade suit still gets bid, because the one level is cheap.  Below 66
and silenced: `oc1H_2C`/`oc1H_2D` (65) only.  The weak jumps (60) and preempts
(58/59) need six and seven cards, which `longest_suit_length: [5,5]` excludes.
`oc1H_pass` (25) keeps everything else.

**VERIFIED.** `P oc1H_pass_vul2 fit=1.000 prio=66` chosen over `2D oc1H_2D
fit=1.000 prio=65`.  (First trace of this rung failed because I fed it a
three-call auction for a four-call seat — corrected and re-run.)

**Template.** Four hand-written copies, one per `overcalls_of_1x` context:
`oc1C_pass_vul2`, `oc1D_pass_vul2`, `oc1H_pass_vul2`, `oc1S_pass_vul2`, each at
a priority one point above that context's two-level overcalls and below its
one-level ones.  In `overcalls_of_1C` and `overcalls_of_1D` the two-level
overcall is much rarer, so the payoff is concentrated in the two major contexts.

---

## Board 850 — table A, call 4, seat S: `3H` (`cl_rebid_jump_H`)

`1H 1S X 2S`.  I opened, they overcalled, partner made a negative double
promising the other major and values, they raised to 2S — and I made an
*invitational* jump to 3H on `82.KJT9542.KJ.AK`: seven trumps, fifteen points,
a doubleton in their suit.  They bid 4S and made it.  `cl_rebid_jump_H` runs
**-4.80 over 5 tables**, the worst rung in this slice.

**Missing agreement.** Seven trumps, fourteen points and a doubleton in their
suit belongs in game NOW — the invitational three-level rebid gives them a free
3S and buys nothing.

```yaml
# context: general_competitive_low   (insert before cl_doubler_raise_C)
      - id: cl_rebid_game_H
        call: 4H
        priority: 32.5
        when: { my_suit: H, is_competitive: true, we_hold_contract: false }
        requires:
          suits: { H: [7, 13] }
          evals: { total_points: [14, 40], standing_suit_length: [0, 2] }
        shows: "seven trumps, fourteen points and a doubleton in their suit: the hand belongs in game now"
        establishes: { forcing: non_forcing, agreed_suit: H }
```

Note there is **no `cheapest_in_suit`** gate — 4H is a jump over 2S and the gate
would make the rung unreachable, which is exactly the trap that
`cl_raise_lott3_$M` fell into and that the ledger already records.  My first
trace failed for precisely that reason and the gate was removed.

**Answering seat:** none — it is a contract, not a question, and
`agreed_suit: H` puts partner into the pull-or-sit family if they compete.

**Endangers.** Above: `cl_takeout_X` (36) needs `side_has_acted: false`;
`cl_negative_X2` (33) needs `i_have_acted: false`.  Below: `cl_rebid_jump_H`
(31, the target), `cl_rebid_H3`/`H4` (29), `cl_nt3` (29, cannot fit a 7-2-2-2),
`cl_pass` (20).  **It deletes the code fallback for 4H** in every seat its
`when` reaches — `my_suit` + `is_competitive` — but 4H is already covered there
by `cl_rebid_H4` and `cl_raise_H4`, so there is no fallback to lose.

**VERIFIED.** `4H cl_rebid_game_H fit=1.000 prio=32.5` chosen over
`3H cl_rebid_jump_H fit=1.000 prio=31`.

**Template.** `expand: { M: [H, S] }` → `cl_rebid_game_$M`.  The minors want
`5$m` on eight trumps, which is a different (and much more dangerous) rung and
should not ship with this one.  Sibling into `general_competitive_high`.

---

## Board 852 — table A, call 4, seat N: `P` (`cl_pass`)

`P P 1NT 2S`.  Partner opened a strong notrump, they overcalled 2S, and I hold
`T2.K964.JT74.QJ9` — **seven** HCP with four hearts.  `cl_negative_X2` demands 8
(fit 0.800), so we sold out.  BEN doubles at 0.98.  Same underlying cause as
board 674, other call.

**Missing agreement.** Opposite a partner who has shown a strong balanced hand
the negative double starts at 6, not 8 — the floor is calibrated for an
unlimited partner.

```yaml
# context: general_competitive_low   (insert before cl_doubler_raise_C)
      - id: cl_negative_X2_strong
        call: X
        priority: 33.5
        when: { their_last_bid_suit: true, side_has_acted: true, i_have_acted: false,
                standing_bid_level: [2] }
        requires:
          hcp: [6, 40]
          evals: { "suit_length(their)": [0, 3], longest_suit_length: [0, 4], rule_of_26: [21, 99] }
          any_of:
            - suits: { H: [4, 13] }
            - suits: { S: [4, 13] }
        shows: "negative double at the two level opposite a strong balanced partner: 6+ HCP with a major they have not bid"
        establishes: { forcing: one_round }
        convention: negative_double
```

Every gate except the HCP floor is copied **verbatim** from `cl_negative_X2`, so
the rung can only ever be a superset of it on the strong-partner hands, plus the
`rule_of_26` gate that defines "strong partner".

**Answering seat.** `forcing: one_round`.  The seat that answers is partner,
served by `general_competitive_high`'s `ch_neg_major_$M2/3/4` family
("answering partner's negative double in the major it promised") — which is
already authored and is why I was willing to lower this floor rather than invent
a new call.

**Endangers.** Above: `cl_takeout_X` (36) needs `side_has_acted: false`.
Below: `cl_negative_X2` (33, same call), the natural bids at 26-31, `cl_pass`
(20).  **CAUTION, and this is the one number that argues against the rung:
`cl_negative_X2` runs -2.07 over 15 tables whole-corpus.**  I am widening a
family that is losing money.  The defence is that its losses are on unlimited-
partner auctions and this rung fires only opposite a shown 15+, but that split
has not been measured and this proposal should be screened on its own.

**VERIFIED.** `X cl_negative_X2_strong fit=1.000 prio=33.5` chosen over
`P cl_pass fit=1.000`; `cl_negative_X2` correctly at 0.800.

**Template.** No suit expansion (the `any_of` covers both majors).  A
three-level twin `cl_negative_X3_strong` in `general_competitive_high` with
`hcp: [8,40]` follows the same argument.

---

## Board 861 — NOTHING-WRONG

**What I checked.**  The first divergence is table B call 10: W accepts the
Stayman invite with `763.AK.AK974.Q32`, 16 HCP **with a five-card diamond
suit** — a legitimate accept (unlike board 764's flat 16, which is why 764 gets
the rung and this board does not).  3NT went down two on the layout.

Competitively: at table A we (N/S) passed throughout a `1NT-2C-2D-2NT` auction.
N held `A42.T7543.Q8.A84` — 10 HCP with `T7543`, which is not a `good_suit(H)`
and so is correctly outside `v1NT_2H`'s gate; entering on that suit against a
strong notrump, vulnerable both, is exactly the action board 103 shows costing
IMPs.  S never had a live seat.  `v1NT_pass` is right here.

No competitive agreement is missing.

---

## Board 863 — table B, call 8, seat W: `4H` (`uc_raise_H4`)

`1H P 1S P 2D P 2H P`.  I opened 1H on `Q9.AQJT9.K832.K7`, partner responded 1S,
I rebid 2D, and partner **preferred** back to 2H — showing two or three hearts
and 6-9.  I then jumped to game.  Down two.  `uc_raise_H4` is scored as a raise
of *partner's* suit even though hearts are mine, so `lott_total_trumps(H)`
counts partner's minimum of two and the eight-trump gate passes.

**Missing agreement.** Partner's preference back to my own suit is not a raise:
eight trumps and a minimum is a partscore.

```yaml
# context: general_uncontested_continuation   (insert before uc_doubler_raise_C)
      - id: uc_pass_preference_H
        call: P
        priority: 32.5
        when: { partner_suit: H, my_suit: H, i_have_acted: true, we_hold_contract: false }
        requires:
          evals: { "lott_total_trumps(H)": [0, 8], total_points: [12, 17] }
        shows: "partner has merely preferred my own suit: eight trumps and a minimum is a partscore"
        establishes: { forcing: non_forcing }
```

The `my_suit: H` AND `partner_suit: H` pair is the whole diagnosis in one line:
it fires only where the "raise" is really a preference to a suit I bid first.

**Answering seat:** none.

**Endangers.** Above: `gst_rkc_H` (46) — a slam hand is untouched; nothing else
in this context is above 32.5 except the doubler's raises (34), which need
`my_last_call_was_double`.  Below: `uc_raise_H4` (32, the target, -0.70 over 30
tables), `uc_raise_H3` (31), `uc_nt3` (29), `uc_rebid_H3` (29), `uc_pass` (18).
The `total_points: [12,17]` band is what leaves an 18+ opener free to drive on,
and `lott_total_trumps <= 8` is sharp, so a genuine nine-card fit still raises.

**VERIFIED.** `P uc_pass_preference_H fit=1.000 prio=32.5` chosen over
`4H uc_raise_H4 fit=1.000 prio=32`.

**Template.** `expand: { X: [C, D, H, S] }` → `uc_pass_preference_$X`, and the
same four into `general_competitive_low`.  This is the mirror image of the
documented open item "after partner RAISES my own suit every generic raise rung
is dead": the rung is not dead, it is firing on the wrong side of the fence.
