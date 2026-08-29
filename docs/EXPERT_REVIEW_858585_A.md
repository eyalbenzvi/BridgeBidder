# Expert review A — clusters 1-10 and the worst 15 singles (seed 858585, -710 IMPs)

## Method note

Denominators first. `rule_tables` attributes the whole **board** margin to each table, so
the sum over all 2000 tables is 2x the match margin and the honest baseline a rule must
beat is **-0.71 IMPs per attributed table**. Every rule named in the dossier was re-scored
across all 2000 tables of `reports/e7_before.jsonl` (winners included) before it was
accused; several families turned out to be at or above baseline and are reported as
non-findings.

Every indictment below was reproduced through `choose_bid` / `rank_at`. Nine fixes were
prototyped in a scratch copy of the YAML and re-run through `choose_bid` with the
opponents' (BEN's) passes held fixed; the whole 10,470-decision corpus was then replayed
base-vs-prototype with arbitration disabled, so the "what else does this touch" column is
measured, not asserted. The prototype lints identically to the shipped system
(`collide 0, gap 0, shape 0, sibling 0, soft 0`, `floor` unchanged at 223) and loads
clean (498 contexts / 2156 rules vs 490 / 2122).

Mechanical caveat carried over from round 7: the dossier's `rule` field is the PRIMARY
READING (highest-priority same-call rule), not necessarily the rule whose constraint
matched. On board 478 the 4NT is recorded as `gr_rkc_S` but was produced by
`gr_rkc_general_S`.

---

## CLUSTER 1 — `uc_nt3`, 24 boards, 141 IMPs — **NOTHING-WRONG as a rule / IMPLEMENTATION-BUG upstream** (VERIFIED)

Whole corpus: **69 firings, -61 IMPs, mean -0.88** against a -0.71 baseline. Excess ~ -12
IMPs over the corpus. It fits 1.00 on nearly every board it loses, and DECISIONS has ruled
it a symptom three rounds running. **Do not touch its strength gate.**

Reading all 69 firings, 31 of them are boards where *both* tables reach the identical 3NT
(margin exactly 0). The losers split into two mechanisms, both upstream:

**(a) The `weakest_their_stopper` gate does not gate.** `uc_nt3` (and 26 other rules)
require `weakest_their_stopper: [0.9, 9]`. That evaluator has **no sharp tolerance
registered in `_EVAL_S2`**, while its two siblings `stoppers` and
`weakest_unshown_stopper` both carry 0.3. With the default sigma 4.48 a hand with a
*partial* stopper (Qx / Jxx = 0.5) scores exp(-0.16/4.48) = **0.965** and a hand with **no
stopper at all** (0.0) scores exp(-0.81/4.48) = **0.835**. The gate is decorative.
Reproduced: board 548 (-12) bids 3NT holding Q4 in their clubs; 877 (-8) holding Q3 in
their hearts; 204 (-6) holding Q7 in their spades; 507 (-14, a single below) holding Q5
opposite an eight-card club suit. See FIX 1.

**(b) Ceilings and starved seats feeding it.** Board 863 (-10): a 17-count with six clubs
over partner's negative double has NO rule in `opener_over_negative_double` (see CLUSTER 1b
/ FIX 5). Board 548 (-12): after `1C-X-1D-1H-P-1S-P-2S-P` the doubler holds QJT7.KQT.KQ82.Q4
and a nine-card spade fit, and the only candidates are 3NT (fit 0.96) and pass (1.00) —
every generic raise rung is dead because `lott_total_trumps(S)` counts partner's *shown*
three, giving 7 against a sharp 8-trump gate. That is diagnosed below as an open item, not
fixed.

## CLUSTER 2 — `all-pass`, 31 boards, 115 IMPs — **NOTHING-WRONG** (VERIFIED)

553 tables, -379 IMPs, **mean -0.69** — indistinguishable from the -0.71 corpus baseline.
Sliced by board instead of table: boards where one of our tables passed throughout average
**-0.68**; boards where both tables bid average **-0.74**. The all-pass boards are
*better* than the rest of the match.

This is expected and worth stating: when our side passes throughout at a table, the board
margin is determined entirely by our bidding at the *other* table. The cluster measures
nothing about the passes. The eleven biggest members were read individually; the passes are
in range (board 904's balancing seat holds three of their suit and 11 HCP; board 284's
advancer holds four spades and 8 HCP over a raised 1H). Two genuine seat-starvations exist
in the tail and are reported as non-findings below (board 109, an 11-count with an
eight-card diamond suit in **third seat**, where the light minor opening is gated to seats
1-2 and 4; board 19, 5-4 majors over their 1NT-3C). Both are single boards. **No fix.**

## CLUSTER 3 — `uc_raise_H4`, 12 boards, 75 IMPs — **NOTHING-WRONG** (VERIFIED)
## CLUSTER 4 — `uc_raise_S4`, 9 boards, 54 IMPs — **NOTHING-WRONG** (VERIFIED)

These two are the same rule with the suit letter changed; the constraints are character-for
-character mirrors (`suits: {M:[2,13]}, total_points [11,40], rule_of_26 [25,99],
lott_total_trumps(M) [8,26]`, priority 32). Treating them separately is what makes the
hearts half look bad:

| | firings | board margin | mean |
|---|---|---|---|
| `uc_raise_H4` | 42 | -57 | -1.36 |
| `uc_raise_S4` | 47 | +3 | +0.06 |
| **combined family** | **89** | **-54** | **-0.61** |

The family is *above* the -0.71 baseline. The H/S split is noise across 89 tables. Success
rate of the games it reaches: **52 made, 37 failed (58%)** — normal IMP game bidding, not
overbidding. DECISIONS explicitly scopes out tuning this family ("the thin-game invitation
dribble ... judgment, not structure; the Phase 3 result warns against tuning it") and the
coordinate-descent threshold search measured -0.025 +/- 0.062 held-out. **No fix, no
threshold proposed.**

The two worst members are not raise problems: board 856 (-14) is a grand slam the system
cannot bid (scope-excluded), board 389 (-13) is the keycard ask over a game raise
(CLUSTER 3b below).

## CLUSTER 5 — `ob_1H1S_2H`, 3 boards, 26 IMPs — **IMPLEMENTATION-BUG (sibling gate never swept)** (VERIFIED). HIGHEST-VALUE FIX IN MY SLICE.

Whole corpus: **6 firings, -40 IMPs, mean -6.67** — the worst per-firing family I found.
Every one of the six is opener with a long, strong heart suit rebidding 2H.

```
239 (-10) J.AKQT84.JT2.AT2  14 HCP, 6 hearts, stiff spade   2H passed out; 4H makes
451 ( -6) J7.AKT982.A5.K73  14 HCP, 6 hearts                2H passed out; 4H makes
730 (-10) K5.AKQT975.Q.J95  15 HCP, SEVEN hearts            2H passed out; 4H makes
856 (-14) .AKQJT732.J85.62  11 HCP, EIGHT hearts, void S    2H -> 4H (BEN bid 7H)
450 (  0) 8.AQT973.KQJ95.J  13 HCP, 6-5                     2H-2S-3H-3S-4H
962 (  0) JT.AKJT864.A7.J2  13 HCP, 7 hearts                2H-2NT-3H-4H
```

`ob_1H1S_3H` requires **`hcp: [16,18]`**. Its exact sibling one context away —
`ob_1M1NT_3$M`, the same jump rebid over the 1NT response — requires
**`total_points: [16,19]` plus `good_suit($M)`**, and it outranks the simple rebid
(priority 56 vs 54) instead of sitting under it (51 vs 52). Neither the points measure nor
the priority ordering was ever swept onto the 1H-1S ladder, so a 15-count with seven
hearts and a singleton (18 playing points) rebids "minimum" and gets passed. This is round
7's named species — *a gate added to one sibling and not the other*.

FIX 2 makes the gate a strict superset (`any_of` of the old HCP band and the sibling's
points+quality band) and moves the priority above the 2H rung, exactly mirroring
`ob_1M1NT_*`. Verified: all six firings re-run, 239 and 451 now reach 4H (+16 IMPs
combined), 730 reaches 3H (score-neutral), 450 and 962 reach the same 4H by a shorter
route, 856 unchanged.

## CLUSTER 6 — `rkc5C_slam`, 2 boards, 26 IMPs — **NOTHING-WRONG** (VERIFIED)

8 tables, **+0 IMPs**, 2 wins / 2 losses, mean +0.00 — above baseline. Board 735 (-13) is
6H versus BEN's 7H: the system cannot bid a grand slam, which DECISIONS lists as
scope-excluded. Board 396 (-13) is not a `rkc5C_slam` failure either — with three keycards
in hand and a 1-or-4 reply the count is four of five and six is the book bid; the error was
asking at all (CLUSTER 3b). **No fix.**

## CLUSTER 7 — `cl_new_D3`, 5 boards, 25 IMPs — **NOTHING-WRONG** (VERIFIED)

The dossier's "12 tables, -24" is the *last-bid* attribution and it drops board 602, where
the same rule fired and the board won +13. Counting every firing: **13 tables, -11 IMPs,
mean -0.85** — baseline. No fix to `cl_new_D3`.

The two worst members are separate diseases, both reproduced:
* 888 (-11): the 19-count with a **spade void** passes their 3S, because
  `general_competitive_high` defines `X` only as `ch_penalty_X` (trump tricks required,
  fit 0.00 on a void) and the code fallback double is suppressed once a rule defines the
  call. This is the reopening-double hole DECISIONS already lists as needing its own
  round; adding a second meaning for `X` in that context is a `collide` risk. Not proposed.
* 402 (-7): the balancing doubler with AKJ opposite partner's 2H advance cannot raise —
  `cl_doubler_raise3_H` needs FOUR-card support and 17-19, and `cl_raise_H3`'s sharp
  8-trump LOTT gate reads 3 + partner's shown 4 = 7. Same mechanism as board 548. Diagnosed
  as an open item below, not fixed.

## CLUSTER 8 — `open_1NT`, 7 boards, 25 IMPs — **NOTHING-WRONG** (VERIFIED)

26 last-bid tables, **+3 IMPs, mean +0.12**; 113 firings anywhere, mean -0.34. Both above
baseline. Five of the seven members are "our 1NT was passed out for 6-8 tricks while BEN's
side found a partscore" — variance. The one real hole is board 293 (-11) and it is not the
opening: after `1NT - (2C) - ?` **there is no context at all** for responder (`context_at`
returns only `general_competitive_low`), so an 11-count with KQJ7 in their suit passes at
blended 0.760 against `cl_nt2`'s 0.627. Authoring "systems on over interference" would
SHADOW `general_competitive_low` for those calls and must therefore carry its gates
verbatim; that is a round of its own. Reported, not proposed.

## CLUSTER 9 — `r2ntj_4M`, 2 boards, 22 IMPs — **MISSING-AGREEMENT, but my prototype measured NEGATIVE. NOT PROPOSED.**

2 tables, -22, mean -11.0. Both are `1D - 1S - 2NT(18-19) - 4S` with a long spade suit and
a slam on: 80 (AKQJ63.Q94.6.Q92, 14 HCP) and 273 (KJ98642.7.Q.AJ97, 11 HCP, seven spades).
`r2ntj_3$M` demands **exactly five** cards, so a six- or seven-card suit has only the 4M
sign-off (6-13) and the 6NT rung (15+, 5 controls).

I widened `r2ntj_3$M` to accept 6+ with 10-14 and re-ran both boards:
* 273: `3S - 4S` — same contract, no gain.
* 80: `3S - 3NT` — **worse** (opener holds two spades; 3NT+3 replaces 4S+2).

The reason it cannot work inside the constraint language: merging the two hand types into
one call makes `min_total_points` of the disjunction 6, so opener's `rule_of_26` never
opens and `o2ntj_4$M` signs off in game. Separating them needs a call the system does not
have (4NT is already the quantitative raise here; inventing a meaning for 4-of-the-other
-major is exactly what DECISIONS forbids). **Reported as a negative result; no fix.**

## CLUSTER 10 — `uc_nt2`, 7 boards, 22 IMPs — **NOTHING-WRONG / symptom** (VERIFIED)

21 firings, -34 IMPs, mean -1.62, spread over 13 different auction families with margins of
-1 to -9. It fits 1.00 or 0.8 on all of them and is the only bid on offer. Six of the
firings are the advance of partner's overcall, where `advance_overcall` has only three
rules (raise / cue / 1NT) and the generic toolkit legitimately supplies the natural 2NT.
The `weakest_their_stopper` repair (FIX 1) touches five of these firings and removes the
worst two. **No fix to the rule.**

---

# Worst singles 1-15

### 836 (-15) — `rmjs_3NT_C` — **IMPLEMENTATION-BUG (a ladder banded by strength, never by shape)** (VERIFIED)
`P 1H P 1S P 3C P ?` with **AQT73.T2.9.KQT76** — 5-5 with a singleton diamond — bids 3NT
and goes down three. `responder_after_major_jump_shift` has exactly three rules: 6NT (14+
balanced), 4H (3-card support), 3NT (**anything 6-21**). There is no rung for responder's
own five-card suit and none for supporting the jump-shift suit, so a 5-5 hand with a stiff
has only the catch-all. FIX 6 adds one rung (5+ spades AND a singleton/void → 3S), keeping
3NT's full band underneath so nothing is subtracted. Verified: 3NT -> `3S - 4S` making 12,
+4 IMPs (BEN bid 6S; we do not reach it).

### 507 (-14) — `balhigh_nt3` — **IMPLEMENTATION-BUG, same as CLUSTER 1(a)** (VERIFIED)
3NT bid holding **Q5** opposite an eight-card club suit the opponents have bid at the three
level; down four. `weakest_their_stopper` = 0.5 scores 0.965 today. With the sibling sigma
(FIX 1) the call becomes a reopening double and the auction runs
`X - 3H - 4NT - 5S - 6H`, and 6H makes exactly 12 tricks (BEN's table made 12 in 4H).
Swing measured at the contract level: -14 -> +13.

### 776 (-14) — **NOTHING-WRONG** (VERIFIED)
`P 1C 1H 2C 2H 3C 4H 5C` — our LOTT raise to 4H pushed them into a 5C that made twelve
tricks. par(NS) is -100, i.e. the deal belongs to them. Competitive variance.

### 884 (-14) — `c2r_X` — **NEEDS-EXCEPTION, HIGH-VARIANCE** (VERIFIED, not prototyped)
`2C - (5C) - P - P - ?` holding **AKQJ9.KQJ84.AQ.T**. `strong_2C_reopen` writes its natural
suit rebids as literal `3H`/`3S`/`3D`, which are illegal over a 5C overcall, so the only
legal rule left is the takeout double at priority 58. The 24-count doubles for +500 with
6S (2210) on. This is round 7's `balhigh_reopen_X` lesson in a different context — you
cannot take a five-level contract out for takeout. 1 table, -14 IMPs whole corpus. A fix
needs explicit 4-level and 5-level natural rungs *above* the double's priority; I did not
prototype it because the population is one board. Listed last in the fix list and flagged
HIGH-VARIANCE.

### 929 (-14) — **NOTHING-WRONG** (VERIFIED)
`1H - 2H(passed-hand raise) - 4H` with AT.KJ8754.AJ8.AK (22 total points). BEN bid 7H via
2C and took 13. `op_after_raise_game` is already capped at 24 precisely so a monster reaches
the keycard rules (DECISIONS, trump-setting round); 22 opposite a 6-9 raise is a game, not a
slam. 13 tables, -11 IMPs, mean -0.85 — baseline. The grand slam is scope-excluded.

### 62 (-13) — **NOTHING-WRONG** (VERIFIED)
`1S - 1NT - 4S` with AK9743.QJ8.A.AK7 (22 total points) opposite a semi-forcing 1NT capped
at 11. 4S making 12 is the book result; BEN's 6H came from a 2C opening. `ob_1M1NT_4S`:
4 tables, -2 IMPs. No structural gap that a capped partner can exploit.

### 389 (-13), 478 (-13) — `gr_rkc_$M` — **NEEDS-EXCEPTION. MEASURED; RECOMMEND AS ITS OWN EXPERIMENT, NOT SHIPPED.**
See CLUSTER 3b below. Both are keycard asks over partner's game raise that ended one level
too high.

### 395 (-13) — `r1c1d_3D_H` — **MISSING-AGREEMENT (a forcing ladder with no answering seat)** (VERIFIED)
`P 1C P 1D P 1H P 3D P` and opener **passes** with AJ65.K643..AT974. `r1c1d_3D_$M` is
`establishes: {forcing: one_round}`, but there is no context matching
`1C - P - 1D - P - 1$M - P - 3D - P - ?`; `context_at` returns only
`general_uncontested_continuation`, whose best non-pass candidate fits **0.279**. Because
that is below 0.3, the documented "a one-round force may be passed when nothing fits at
all" escape hatch fires and the force dies. A 19-count's forcing jump was passed out in 3D
with 6NT cold. FIX 4 authors the answering context (three rungs, the 3NT a complete
fallback so the seat can never starve again). Verified: `3D - 3NT - 6NT`, +13 IMPs.

### 515 (-13) — `stm_rkc_4NT` — **IMPLEMENTATION-BUG (ceiling + sibling waiver missing)** (VERIFIED). SECOND-HIGHEST VALUE.
`1NT - 2C - 2H - ?` holding **T4.KQ94.AQJ5.AK6** — 18 HCP and a four-card heart fit — and
responder **passes**. Two defects in one rule:
1. **Ceiling.** With a 4-card fit the ladder is 3M (8-9), 4M (10-15), 4NT RKC (15-17). An
   18+ hand with the fit has no rule at all. The *no-fit* half of the same context was
   given its 18-21 rung last round (`stm_6NT_nofit`, and its comment even says "the ladder
   stopped at 15") — the fit half was never swept.
2. **The keycard waiver is missing.** `stm_rkc_4NT` carries a bare
   `worthless_doubleton: [0,0]` veto (sharp). T4 is a worthless doubleton, so the ask fits
   **0.000**. Every other keycard ask in the file carries the round-6 waiver
   `any_of: [ {void 0, worthless_doubleton 0}, {keycards >= 3} ]`; this hand holds three.
FIX 3 widens the band to 15-21 and adds the waiver verbatim from `gr_rkc_general_$M`. Both
changes are strict widenings. Verified: `4NT - 5H - 6H` making 13, +13 IMPs.

### 559 (-13) — **NOTHING-WRONG** (VERIFIED)
Jacoby auction, 4NT, 5H (two keycards, no queen), sign-off in 5S; BEN bid 6S and it made.
The asker (AJ953.Q5.82.AKJ9) holds **two** keycards and no trump queen, so four of five are
present and the trump KING is missing as well as the queen. Signing off is right; 6S made
because the defenders' KQ fell doubleton. Chasing this is chasing variance.

### 655 (-13) — `nt2_tr_slam` — **MISSING-AGREEMENT (invite with nobody to accept it) + ceiling** (VERIFIED)
`2NT - 3D - 3H - 4NT - P P P`. Two defects:
1. Responder holds **16 HCP** opposite a shown 20-21 — that is 36-37 combined, and the only
   slam rung in `nt2_after_transfer` is an *invitation* spanning 11-40.
2. There is **no context** answering `2NT - P - 3$T - P - 3$M - P - 4NT - P - ?`, so
   opener's only candidate is the code fallback pass. The invitation was declined by
   construction. Three sibling quantitative raises in the file (`rjsq`, `rrntq`, `rjrbq`)
   do ship with their accept context; these do not.
FIX 7 adds the 6NT rung *above* the invite (no cap on the invite, so no band is orphaned)
and authors the accept context. Verified: 6NT making 13, +13 IMPs.

### 958 (-13) — `rp3_S_game` — **IMPLEMENTATION-BUG (ceiling)** (VERIFIED)
`3S - P - ?` holding **AT6.AKJ8.AT.A754** — 20 HCP, all four aces, three-card support
opposite a seven-card suit — and the top rung of `resp_preempt_S` is the 4S game raise
(`total_points [15,40]`). Every slam opposite a preempt is signed off by construction.
FIX 8 adds a keycard rung to all four `resp_preempt_*` contexts, gated on the **counted**
fit (`lott_total_trumps >= 9`) and on holding **four of the five keycards myself** — with
three the reply cannot keep you out of a slam off an ace, which is exactly how my first
draft lost board 957. Verified: 958 `4NT - 5D - 6S` making 13 (+13) and 642
`4NT - 5C - 6H` making 13 (+11); with the 4-keycard floor, board 957 no longer asks and
stays at its (correct) 4S.

### 988 (-13) — **NOTHING-WRONG** (VERIFIED)
Stayman 4-4 heart fit, 4NT, 5H (two keycards without the queen), pass. All five keycards
are present and only the trump queen is missing in an **eight**-card fit.
`rkc5H_slam`'s second clause (queen in hand OR a nine-card fit) is round 6's deliberate,
measured decision — "a short fit missing the queen is a trump loser, not a finesse" — and
re-opening it on one board is exactly the variance-chasing DECISIONS warns against.
`rkc5H_signoff`+`rkc5H_pass_signoff`: 4 tables, -13 IMPs, and **all four are this one
board**. No fix.

### 269 (-12) — `rmr_4NT` — **MISSING-AGREEMENT (invite with nobody to accept it)** (VERIFIED)
`1C - 1H - 2C - 4NT - P P P`. Identical species to 655: `rmr_4NT` is a quantitative
invitation and no context matches `1$m - P - 1$M - P - 2$m - P - 4NT - P - ?`, so opener
passes from the code fallback. FIX 7 authors it. Gated on `total_points >= 15` rather than
HCP so a hand whose value is a running suit can accept — measured on the two corpus
firings: board 269's AJ7.A82.8.A98752 (13 HCP, three aces, six clubs) accepts and 6NT makes
(+14), and board 403's Q4.82.AKJ6542.Q2 (12 HCP, seven diamonds) also accepts and 6NT makes
(the board was already +11 and gets better).

---

## CLUSTER 3b — the keycard ask over a game raise (`slam_try_over_game_raise`): a measured loss I am NOT proposing a gate for

This is the largest concentrated deficit I found and it is worth recording precisely even
though I could not find a fix that survives the round-6 discipline.

| family | firings | board margin | mean |
|---|---|---|---|
| `gr_rkc_$M` + `gr_rkc_general_$M` (over a game raise) | **14** | **-48** | **-3.43** |
| `gst_rkc_C/D/H/S` (general slam try, standing bid at 2-4) | 11 | **+29** | +2.64 |

The general slam try is one of the most profitable families in the engine. The version over
a **game raise** is the worst. The mechanism is a bridge fact the constraint language cannot
see: over a 3-level standing bid the ask is free, but over partner's 4M the sign-off is at
the **five** level, one higher than the game we already own.

Nine of the fourteen sign off in 5M and score identically to 4M (5S making 11 = 4S+1). The
damage is entirely in three boards where the answer pushed us past a making game
(621: 5S down 1 where 4S made 10, -12) or into a slam off a keycard (396, 478, both 6S
down 1). Counterfactually passing 4M on all fourteen is worth about +48 IMPs on this corpus
(+13/+13/+12/+12/+13 against -13 on board 892 and -3 on 270).

I tried and rejected three separators:
* **HCP floor.** Does not separate: the losers hold 18, 13, 15, 13, 14; the winners 16, 16.
* **Keycards in hand.** Does not separate: losers 3, 2, 2, 2, 2; winners 2, 2.
* **`rule_of_26` / `total_points` thresholds.** This is threshold tuning, which DECISIONS
  scopes out ("the numbers are not the lever", -0.025 +/- 0.062 held-out).

What *does* separate on inspection is a fact about the auction rather than the hand: on
396 partner returned to game **over my own cue-bid** (`cue_S_signoff` — declining slam),
and on 478 partner's 4S was `r21_fast4_SD`, whose `shows` explicitly reads "fast arrival:
minimum flat game force, no slam interest". Both negative inferences exist in the rulebook
and neither reaches the ask, because `r21_fast4_$M$x` states its cap as
`total_points: [12,13]` — a *floor* channel only. `rule_of_26` reads
`max(partner_min_hcp, partner_min_points)` and then `min(partner_max_hcp, floor+4)`, with
`partner_max_hcp` still 40, so the cap is invisible and the midpoint reads 14 instead of
12.5. Repairing that is an estimator change, and DECISIONS records that the last estimator
repair measured **-20 and was reverted**.

**Verdict: NEEDS-EXCEPTION, diagnosed, deliberately not fixed this round.** If it is to be
attempted, it should be a single isolated experiment measured on the held-out corpus, and
the honest form is a `max_total_points` channel in the partner model, not a threshold.

---

# FIX LIST (priority order)

Every fix below was applied to a scratch copy and the whole corpus (10,470 decisions)
replayed base-vs-prototype with arbitration off. FIXES 2-8 together change **15 decisions**
across 1000 boards; 11 boards improve, 4 are score-neutral, **0 get worse**. Estimated
review-corpus value **+109 IMPs**. That number is in-sample by construction; the held-out
corpus decides.

---

## FIX 1 — register a sharp tolerance for `weakest_their_stopper` (engine, one line)

**VERIFIED (mechanism + whole-corpus impact); HIGH-VARIANCE: no; MEASURE ALONE: yes.**

`src/bridgebidder/constraints/model.py`, `_EVAL_S2`.

BEFORE
```python
    "stoppers": 0.3,
    "weakest_unshown_stopper": 0.3,
```
AFTER
```python
    "stoppers": 0.3,
    "weakest_unshown_stopper": 0.3,
    # Same 0/0.5/1 stopper scale as its two siblings above, and used as a
    # [0.9, 9] gate on 27 rules - every generic natural notrump in a
    # competitive auction.  On the default sigma a hand with NO stopper in
    # their suit scored 0.835 against it and a partial stopper (Qx/Jxx)
    # 0.965, so none of those gates actually gated.
    "weakest_their_stopper": 0.3,
```

*Boards / IMPs.* 548 (-12), 507 (-14), 877 (-8), 204 (-6), 810 (-7), 658 (-3), 401 (-7),
822 (-6), 318 (-1) — the fifteen decisions it changes sit on boards carrying **-58 IMPs**
today. Reproduced end-to-end on four of them: 507 becomes `X - 3H - 4NT - 5S - 6H` making
(-14 -> +13); 548 passes 2S instead of playing 3NT-4 (-12 -> about -6); 877 and 204 stop
bidding hopeless games.

*Whole-corpus denominator.* The family (27 rules: `uc_nt1/2/3`, `cl_nt*`, `ch_nt*`,
`ballow_nt*`, `balhigh_nt*`, `adx_nt`, `onx_nt`, `dma_3NT`, `c2r_3NT`, ...) fires on **133
tables**; sharpening changes **15 of the 133 decisions (11%)**. The evaluator returns 1.0
vacuously when the opponents have shown no suit, so **uncontested notrump bidding is
untouched** — all fifteen changes are competitive auctions.

*ENDANGERS.* This is a gate that currently does not bite and will start biting, i.e. it
SUBTRACTS notrump contracts. Twelve of the fifteen replacements are a PASS, and the brief's
own rule applies: a hole becomes a pass by construction. Two boards that are currently
positive are touched — 327 (+1, `onx_nt` 1NT on Jxx of their suit becomes a 3-card heart
raise) and 787 (+5, `cl_nt1` 1NT on Jxx becomes a pass). On board 548 the pass is still not
the right call (4S is). So: real correctness repair, real risk of trading bad games for
starved seats. **Ship it as its own experiment**, paired, before or after the rest.

---

## FIX 2 — `ob_1H1S_3H`: sweep the sibling's gate and priority onto the 1H-1S ladder

**VERIFIED; HIGH-VARIANCE: no (6 firings, 5 boards of evidence, strict superset).**

`src/bridgebidder/systems/two_over_one.yaml` line 2028, context `opener_rebid_1H_1S`.

BEFORE
```yaml
      - id: ob_1H1S_3H
        call: 3H
        priority: 51
        requires: { suits: { H: [6, 13] }, hcp: [16, 18], not: { suits: { S: [4, 13] } } }
        shows: "jump rebid: 6+ good hearts, 16-18"
        establishes: { forcing: invitational }
```
AFTER
```yaml
      # Sibling sweep from ob_1M1NT_3$M, which states the same jump rebid in
      # PLAYING points plus suit quality and outranks the simple rebid.  Stated
      # in raw HCP and ranked below 2H, this rung could not be reached by the
      # hands it exists for: 15 HCP with seven hearts and a singleton is an
      # eighteen-point hand and was rebidding "minimum".  The old band is kept
      # as an any_of branch so the rule can only ever be a superset.
      - id: ob_1H1S_3H
        call: 3H
        priority: 52.5
        requires:
          suits: { H: [6, 13] }
          not: { suits: { S: [4, 13] } }
          any_of:
            - { hcp: [16, 18] }
            - { evals: { total_points: [16, 19] }, features: [ "good_suit(H)" ] }
        shows: "jump rebid: 6+ good hearts, 16-19 playing strength"
        establishes: { forcing: invitational }
```

*Boards / IMPs.* 239 (-10 -> 0), 451 (-6 -> 0), 730 (-10, unchanged in score), 450 and 962
(0, same final contract by a shorter route), 856 (unchanged). **+16 IMPs.**

*ENDANGERS.* Priority 52.5 sits above `ob_1H1S_2H` (52) and below `ob_1H1S_4H` (53), so the
only behaviour subtracted is the *simple* 2H rebid on hands worth 16-19 playing points with
a good six-card suit — which is the intent. Verified that the 8-card-suit hand
(`.AKQT9543.AT.Q64`, board 0) still bids 4H, which an earlier draft at priority 53 broke.
Corpus-wide it changes 5 decisions and nothing outside this context.

---

## FIX 3 — `stm_rkc_4NT`: raise the ceiling and add the keycard waiver

**VERIFIED; HIGH-VARIANCE: no (strict widening, subtracts nothing).**

`two_over_one.yaml` line 677, context `stayman_resp_after_2M`.

BEFORE
```yaml
      - id: stm_rkc_4NT
        call: 4NT
        priority: 73
        requires:
          suits: { $M: [4, 4] }
          hcp: [15, 17]
          evals: { controls: [4, 12], "void(any)": [0, 0], worthless_doubleton: [0, 0] }
```
AFTER
```yaml
      # Two repairs, both widenings.  (1) CEILING: with a 4-4 fit the ladder ran
      # 8-9 / 10-15 / 15-17 and stopped, so 18+ opposite a 15-17 notrump - 33+
      # combined with a known eight-card fit - had NO rule and passed 2H.  The
      # no-fit half of this same context was given its 18-21 rung a round ago
      # and this half was never swept.  (2) Every other keycard ask in the file
      # carries the round-6 waiver: a hand holding three keycards itself gets an
      # unambiguous answer and may ask with a worthless doubleton.
      - id: stm_rkc_4NT
        call: 4NT
        priority: 73
        requires:
          suits: { $M: [4, 4] }
          hcp: [15, 21]
          evals: { controls: [4, 12] }
          any_of:
            - evals: { "void(any)": [0, 0], worthless_doubleton: [0, 0] }
            - evals: { "keycards($M)": [3, 5] }
```

*Boards / IMPs.* 515 (-13 -> 0): `1NT - 2C - 2H - 4NT - 5H - 6H` making 13. **+13.**

*ENDANGERS.* Nothing is removed: both changes widen. It adds keycard asks on 18-21 hands
with a 4-4 major fit (33-38 combined — correct) and on 15-17 hands holding three keycards
and a worthless doubleton (the round-6 waiver, already the standard everywhere else). One
decision changes corpus-wide.

---

## FIX 4 — author the answering seat for `r1c1d_3D_$M` (a forcing bid nobody could answer)

**VERIFIED; HIGH-VARIANCE: no (pure hole-fill, one board of evidence but zero subtraction).**

`two_over_one.yaml`, NEW context. Insert immediately before `quant_accept_after_1NT_rebid`
(line 7418).

BEFORE: no context matches `1C - P - 1D - P - 1$M - P - 3D - P - ?`; `general_uncontested_
continuation` supplies a best non-pass fit of 0.279, below the 0.3 "nothing fits at all"
threshold, so the one-round force is legally passed out.

AFTER
```yaml
  # r1c1d_3D_$M is FORCING one round and had no answering seat at all, so
  # opener's best non-pass fit was 0.28 and the one-round-force escape hatch
  # passed it out - a 19-count's forcing jump died in 3D with 6NT on.
  - id: opener_over_1C1D_3D_jump
    description: "Opener over responder's forcing 3D jump rebid (1C - 1D - 1M - 3D)"
    expand: { M: [H, S] }
    pattern: "1C - P - 1D - P - 1$M - P - 3D - P - ?"
    rules:
      - id: o1c1d3d_rebid_$M
        call: 3$M
        priority: 59
        requires: { suits: { $M: [5, 13] } }
        shows: "5+ $M opposite the forcing jump"
        establishes: { forcing: game_forcing }
      - id: o1c1d3d_4D_$M
        call: 4D
        priority: 58
        requires: { suits: { D: [3, 13] } }
        shows: "diamond support opposite the forcing jump: setting trumps"
        establishes: { forcing: game_forcing, agreed_suit: D }
      - id: o1c1d3d_3NT_$M
        call: 3NT
        priority: 56
        requires: {}
        shows: "no fit for the running diamonds and no second suit: 3NT"
        establishes: { forcing: sign_off }
```

*Boards / IMPs.* 395 (-13 -> 0): `3D - 3NT - 6NT` making 13. **+13.**

*ENDANGERS.* A new context that DEFINES 3M / 4D / 3NT at this position takes over
interpreting them. The 3NT rung is `requires: {}` — a complete fallback — so the seat can
never be starved and no strength band is orphaned. The position is currently a dead pass,
so there is no behaviour to subtract.

---

## FIX 5 — `opener_over_negative_double`: the 17-19 band has no rule

**VERIFIED; HIGH-VARIANCE: no (pure rung addition above an intact minimum band).**

`two_over_one.yaml` line 4225, context `opener_over_negative_double`.

BEFORE — the whole context is four rungs, every one capped at minimum strength:
`onx_major1` 1oM 12-16, `onx_major` 2oM 12-16, `onx_nt` 1NT 12-14, `onx_rebid` 2m 12-15.
A 17-19 opener has nothing, so the generic `uc_nt3` takes the hand.

AFTER — append after `onx_rebid_$m$M`:
```yaml
      # CEILING: every rung above capped at 16, so a 17-19 opener over the
      # negative double had no rule at all and the generic 3NT took the hand
      # (down three on a six-card club suit with no spade stopper).  Two rungs,
      # both jumps, both ADDED above the minimum band - the 12-16 rungs keep
      # their full range underneath.
      - id: onx_jump_$m$M
        call: "3$m"
        priority: 59
        requires: { suits: { $m: [5, 13] }, hcp: [16, 19] }
        shows: "jump rebid: 5+ $m with 16-19, invitational"
        establishes: { forcing: invitational }
      - id: onx_jumpnt_$m$M
        call: 2NT
        priority: 58.5
        requires: { hcp: [18, 19], balanced: true, evals: { weakest_their_stopper: [0.9, 9] } }
        shows: "jump: 18-19 balanced with their suit stopped"
        establishes: { forcing: invitational }
```

*Boards / IMPs.* 863 (-10): `1C - (1S) - X - P` with K7.QJ.KQ5.KQJ764 bids 3C instead of
3NT-3 vulnerable (-300). About **+10**. Corpus-wide the position arises 21 times and this
is the only 17+ hand in it, so the rung is authored on principle as much as on evidence.

*ENDANGERS.* Board 7 also changes: a 16-count with AQ954 now jumps to 3C instead of 2C.
Replayed: 3C passed out making 10 = 130, identical to 2C+2 = 130. Nothing else moves. The
12-16 rungs are untouched, so no band is subtracted.

---

## FIX 6 — `responder_after_major_jump_shift`: band by shape as well as by strength

**VERIFIED; HIGH-VARIANCE: yes (one board of evidence; it is a new rung, but it displaces
the catch-all 3NT on a population this corpus barely samples).**

`two_over_one.yaml` line 7350, context `responder_after_major_jump_shift`. Insert before
`rmjs_3NT_$m`.

AFTER
```yaml
      # Banded by strength, never by SHAPE: a 5-5 hand with a singleton had only
      # the catch-all 3NT and bid it with a stiff diamond (down three, 6S cold).
      # The 3NT rung keeps its full 6-21 band underneath, so this can only add.
      - id: rmjs_3S_$m
        call: 3S
        priority: 56
        requires: { suits: { S: [5, 13] }, evals: { singleton_or_void: [1, 2] } }
        shows: "five spades and a singleton: showing the suit instead of bidding notrump"
        establishes: { forcing: game_forcing }
```

*Boards / IMPs.* 836 (-15 -> -11): `3C - 3S - 4S` making 12 instead of 3NT-3. **+4.**

*ENDANGERS.* It subtracts the 3NT catch-all from responders holding five spades **and** a
singleton/void — hands that should not be bidding notrump opposite an unlimited
game-forcing jump shift. The answering seat is the generic toolkit, which produced a sound
`uc_raise_S4` 4S on the motivating board; if this is kept, opener's context for
`1H - 1S - 3m - 3S` should be authored in the same round (HARD CONSTRAINT 3). One decision
changes corpus-wide.

---

## FIX 7 — two quantitative 4NT invitations that nobody could accept

**VERIFIED; HIGH-VARIANCE: no (pure hole-fill; three sibling accept-contexts already exist).**

`two_over_one.yaml`, NEW contexts + one new rung. Insert the contexts before
`quant_accept_after_1NT_rebid` (line 7418); the rung goes in `nt2_after_transfer`
(line 12604).

BEFORE: `rmr_4NT` and `nt2_tr_slam` are `establishes: {forcing: invitational}` and no
context matches their auctions, so opener's only candidate is the code fallback pass
(priority 8, `is_undiscussed_fallback`). Every invitation was declined by construction.
Compare `rjsq_*` (`1D-1M-3C-4NT`), `rrntq_*` (`1m-1M-1NT-4NT`) and `rjrbq_*`
(`1m-1M-3m-4NT`), which do ship with their answering seat.

AFTER (a) — new contexts:
```yaml
  # A quantitative 4NT is only an invitation if somebody can ACCEPT it.  Three
  # of the file's quantitative raises already ship with their answering seat
  # (rjsq/rrntq/rjrbq); these two did not.
  - id: quant_accept_after_minor_rebid
    description: "Opener answers the quantitative 4NT over his 12-15 minor rebid"
    expand: { m: [C, D], M: [H, S] }
    pattern: "1$m - P - 1$M - P - 2$m - P - 4NT - P - ?"
    rules:
      - id: rmrq_accept
        call: 6NT
        priority: 60
        requires: { evals: { total_points: [15, 40] } }
        shows: "maximum for the 12-15 minor rebid: accepting the slam invite"
        establishes: { forcing: sign_off }
      - id: rmrq_decline
        call: P
        priority: 55
        requires: {}
        shows: "minimum for the minor rebid: declining"
        establishes: { forcing: sign_off }

  - id: quant_accept_after_2NT_transfer
    description: "Opener answers the quantitative 4NT after the completed 2NT transfer"
    expand_pairs: [ { M: H, T: D }, { M: S, T: H } ]
    pattern: "2NT - P - 3$T - P - 3$M - P - 4NT - P - ?"
    rules:
      - id: nt2trq_accept_$M
        call: 6NT
        priority: 60
        requires: { hcp: [21, 40] }
        shows: "maximum 2NT opening: accepting the slam invite"
        establishes: { forcing: sign_off }
      - id: nt2trq_decline_$M
        call: P
        priority: 55
        requires: {}
        shows: "minimum 2NT opening: declining"
        establishes: { forcing: sign_off }
```

AFTER (b) — the missing rung above the invite, in `nt2_after_transfer`, immediately before
`nt2_tr_slam`:
```yaml
      # 15 opposite a shown 20-21 is 35-36 combined: the invite is not the bid,
      # the slam is.  Added as a RUNG ABOVE the invite (not as a cap on it) so
      # no strength band is left without a rule.
      - id: nt2_tr_6NT
        call: 6NT
        priority: 59
        requires: { hcp: [15, 40], evals: { semi_balanced: [1, 1] } }
        shows: "33+ combined opposite 20-21: bidding the slam"
        establishes: { forcing: sign_off }
```

*Boards / IMPs.* 269 (-12 -> about +2, 6NT making 12 against BEN's 6C), 655 (-13 -> 0,
6NT making 13), 403 (+11 and improving: 6NT makes exactly the 12 tricks 4NT took, while
BEN's 6D went down). **+27 or better.**

*ENDANGERS.* The two decline rungs are `requires: {}` complete fallbacks, so neither seat
can starve. `rmrq_accept` is gated on `total_points >= 15` rather than raw HCP deliberately:
board 269's 13-count has three aces and a six-card suit and board 403's 12-count has a
seven-card running suit, and both slams make — an HCP-only gate would decline both. The
`nt2_tr_6NT` rung only takes hands away from `nt2_tr_slam`, whose band (11-40) still covers
everything underneath.

---

## FIX 8 — `resp_preempt_*`: no rung above the game raise

**VERIFIED; HIGH-VARIANCE: yes (3 firings; the 4-keycard floor is calibrated on them).**

`two_over_one.yaml` lines 8440 / 8482 / 8524 / 8566 — contexts `resp_preempt_C`,
`resp_preempt_D`, `resp_preempt_H`, `resp_preempt_S`. Insert before each `rp3_$X_pass`.
Shown for spades; the other three are identical with the suit letter changed (sibling
discipline — all four or none).

AFTER
```yaml
      # The ladder topped out at the game raise: a 20-count with a nine-card fit
      # opposite a SEVEN-card suit had no rung above 4S, so every slam opposite a
      # preempt was signed off by construction.  Gated on the COUNTED fit and on
      # holding four of the five keycards myself - opposite a hand that has shown
      # 4-9 HCP, three keycards is not enough for the reply to keep you out of a
      # slam off an ace (that draft lost board 957).
      - id: rp3_S_rkc
        call: 4NT
        priority: 66
        requires:
          suits: { S: [2, 13] }
          evals: { total_points: [19, 40], "lott_total_trumps(S)": [9, 26],
                   "keycards(S)": [4, 5] }
        shows: "keycard ask opposite the preempt: a nine-card fit and four of the five keycards"
        establishes: { forcing: one_round, agreed_suit: S, asking: keycards }
        alertable: true
        convention: rkc_1430
```

*Boards / IMPs.* 958 (-13 -> 0, `4NT - 5D - 6S` making 13) and 642 (-11 -> 0,
`4NT - 5C - 6H` making 13). **+24.** The reply and continuation contexts already exist
(`rkc_replies`, `rkc_continue_after_5C/5D`), so the ladder ships with its answering seat.

*ENDANGERS.* It adds asks on hands that previously bid game, i.e. it can only push the
contract UP. With `keycards >= 3` my first draft also fired on board 957
(KJ7.T8.AKT5.AQJ9, three keycards) and bid a 6S that had only eleven tricks — a measured
-12. The 4-keycard floor removes exactly that board and keeps both winners; it is
calibrated on three data points and must be treated as high-variance.

---

## FIX 9 — `strong_2C_reopen` cannot bid above the three level

**UNTESTED (reproduced, not prototyped); HIGH-VARIANCE: yes (one board).**

`two_over_one.yaml` line 881, context `strong_2C_reopen`. Its natural suit rungs are
written as literal `3C`/`3D`/`3H`/`3S`, so over a four- or five-level overcall none of them
is a legal candidate and `c2r_X` (priority 58) is the only rule left. On board 884 a 24-count
holding AKQJ9.KQJ84.AQ.T doubled 5C for +500 with 6S (2210) available. Round 7 wrote the
same lesson for `balhigh_reopen_X`: you cannot take a high-level contract out for takeout.

Proposed shape (an implementer should write the levels out — `call: $L$X` does not expand):
add `c2r_high_$X` rungs at 4H/4S/5C/5D/5H/5S with `when: { unbid_suit: $X,
cheapest_in_suit: true }`, `requires: { suits: { $X: [5, 13] }, evals: { suit_quality($X):
[3, 9] } }` and **priority 59**, above `c2r_X`, so that only at the four level and above
does a self-sufficient suit outrank the double.

*Boards / IMPs.* 884, -14. `c2r_X`: **1 table, -14 IMPs whole corpus** — that is the entire
denominator, which is why this is last and flagged.

*ENDANGERS.* Priority 59 means a five-card suit of quality 3 outranks the reopening double
at the four level and above. At the one-to-three level nothing changes (those rungs stay at
56, below the double). I did not prototype this and would not ship it without one.

---

# NON-FINDINGS (hypotheses killed, with the data)

1. **"`all-pass` is a defect."** 553 tables, mean -0.69 against a -0.71 baseline; sliced by
   board, boards containing an all-pass table average -0.68 versus -0.74 for boards where
   both tables bid. The attribution is meaningless anyway — when our side never bids, the
   board margin measures our bidding at the *other* table.

2. **"`uc_raise_H4` bids too many thin games."** Its mirror `uc_raise_S4` is +0.06/table on
   47 firings with a character-identical constraint; combined the family is 89 firings at
   -0.61, *better* than baseline, and the games it reaches are 52 made / 37 failed (58%).
   No threshold proposed; DECISIONS records the coordinate-descent search at
   -0.025 +/- 0.062 held-out.

3. **"`uc_nt3`'s strength gate."** Not re-proposed. 69 firings, mean -0.88 against -0.71 —
   ~12 IMPs of excess across the whole corpus, and it fits 1.00 on nearly every loser.

4. **"`cl_new_D3` is a bad rule."** The dossier's -24 is the last-bid slice and drops board
   602 (+13). All 13 firings: -11 IMPs, mean -0.85 — baseline.

5. **"`open_1NT` is opening too often."** 26 last-bid tables +3 (+0.12), 113 firings -0.34.
   Both above baseline.

6. **Widening `r2ntj_3$M` to six-card majors (cluster 9): PROTOTYPED AND MEASURED WORSE.**
   Board 273 reached the same 4S; board 80 reached 3NT instead of 4S — a downgrade — because
   opener holds two spades. The structural reason is that merging the 5-card and 6-card hand
   types into one call drops the disjunction's `min_total_points` to 6, so opener's
   `rule_of_26` can never open. Reported rather than shipped.

7. **A gate on the keycard ask over a game raise (`gr_rkc_$M`).** The loss is real and large
   (14 firings, -48, against +29 for the general slam try over 11) but neither HCP
   (losers 18/13/15/13/14, winners 16/16) nor keycards-in-hand (losers 3/2/2/2/2, winners
   2/2) separates the population, and the only thing that does — partner's fast-arrival or
   sign-off cap — is invisible to `rule_of_26` because `total_points` has a floor channel in
   the partner model but no ceiling. Threshold tuning is scope-excluded and the last
   estimator repair measured -20. Documented in CLUSTER 3b; not proposed.

8. **Re-opening the RKC 5H trump-queen clause (board 988).** All five keycards, eight-card
   fit, queen missing. `rkc5H_signoff` + `rkc5H_pass_signoff` account for 4 tables and -13
   IMPs *all on this one board*. Round 6 decided this deliberately and measured it. Left
   alone.

9. **`ob_1H1S_3H` at priority 53.** My first draft used 53, which ties `ob_1H1S_4H` and
   demoted board 0's eight-card suit from 4H to 3H. Caught by the corpus replay; 52.5 fixes
   it. Reported because it is exactly the failure mode a priority change invites.

10. **`rp3_$X_rkc` at `keycards >= 3`.** First draft; it fired on board 957
    (KJ7.T8.AKT5.AQJ9) and bid a 6S with eleven tricks available, -12. Raised to 4.

---

# Open items diagnosed but NOT fixed (for a future round)

* **After partner RAISES my own suit, every generic raise rung is dead.** `uc_raise_$M3/4`
  and `cl_raise_$M3` gate on `lott_total_trumps >= 8` (sharp), which counts partner's
  *shown minimum*. A simple raise promises three, and my own suit-bid promised four, so the
  counted total is 7 and both the invitational and the game rung score ~0.08. Board 548
  (-12): the doubler holds QJT7 opposite a five-card raise, a nine-card fit, 14 HCP, and
  his only candidates are 3NT (0.96) and pass (1.00). Board 402 (-7) is the same shape from
  the balancing double. A rung gated on `when: { partner_suit: $M, my_suit: $M }` with a
  7-trump floor would express "partner raised the suit I bid" honestly; it needs its own
  measurement.
* **No context for responder over their overcall of our 1NT** (`1NT - bid - ?`). Board 293
  (-11). Authoring it shadows `general_competitive_low` and must carry its gates verbatim.
* **No takeout/cooperative double above the three level.** `general_competitive_high`
  defines `X` only as `ch_penalty_X`, and because a rule defines the call the code fallback
  double is suppressed. Board 888 (-11): 19 HCP and a spade VOID passes their 3S. This is
  the `collide` risk DECISIONS already flags for the reopening double.
* **Third seat has no light minor opening.** `open_1m_rule20` / `open_1C_rule20` are gated
  `opening_seat: [1, 2]`, the rule-of-15 openings cover seat 4, and the third-seat light
  openings cover **majors only**. Board 109 (-4): A.T97.AQJT8632.9 — 11 HCP and an
  eight-card diamond suit in third seat — passes out, with `open_1D` at fit 0.80/blended
  0.738 losing to `open_pass` at 0.760. Extending the two rule-of-20 minor openings to
  `opening_seat: [1, 2, 3]` is a pure hole-fill; one board of evidence.
