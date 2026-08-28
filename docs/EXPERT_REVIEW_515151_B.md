# Expert review — seed 515151, clusters 11-20 + worst singles #16-30
# Reviewer B (external; 2/1 GF).  Every indictment below was reproduced through
# `choose_bid`, and every prescription was *implemented in a scratch copy of the
# YAML and re-run on the board that motivated it* before being written down.
# The whole prescribed set was then run against `tools/lint_system.py`
# (194 findings, all advisory `floor`, identical to baseline; collide/gap/soft = 0),
# `tools/fuzz_decisions.py --n 200` (2071 decisions, 0 crashes, 0 empty seats,
# 1 starved context also present at baseline) and `pytest` (639 passed).
# The working tree was reverted; nothing here is committed.

---------------------------------------------------------------------------
## Two cross-cutting findings first (they explain boards in five of my clusters)

### X1. `uc_pass` / `ch_pass` / `cl_pass` defeat the forcing-pass filter.  IMPLEMENTATION-BUG.

`engine/decision.py`:

```python
or any(sc.fit >= 0.9 and not sc.candidate.is_fallback for sc in passes)
```

This is the round-4 relaxation, authored so advancer can *convert* partner's
takeout double.  But the generic toolkit's floor passes are `requires: {}` —
they fit **1.00 on every hand** and they are authored rules, not fallbacks.  So
the relaxation is satisfied in essentially every position where a generic
context matches, and a one-round force can be passed out by any hand for which
no specific rule scores above ~0.85.  (`uc_pass` at priority 18 blends to
0.754; a fit-0.80 bid at priority 60 blends to 0.63.)

Reproduced, board 794 — `1S (X) 2NT (P)`, opener holds `T6543.AT.KJ63.A2`:
the engine **passes partner's alertable, artificial, one-round-forcing Jordan
2NT** with `uc_pass`, and 2NT played from the 5-0 side went for 300.

Fix (one line, verified: 639 tests still pass, board 794 no longer passes):

```python
or any(sc.fit >= 0.9 and not sc.candidate.is_fallback
       and not sc.candidate.constraint.is_trivial for sc in passes)
```

`HandConstraint.is_trivial` already exists.  The genuine "sit for the double"
passes all carry real gates (`adx_sit` needs `standing_suit_length >= 4` and
`suit_quality(their) >= 1.5`), so the intended behaviour is untouched.

### X2. The self-rebid ladder's 3- and 4-level rungs are unreachable.  IMPLEMENTATION-BUG.

`uc_rebid_X2` is capped by `not: { evals: { rule_of_26: [26,99] } }`;
`uc_rebid_X3` (r26 >= 22) and `uc_rebid_X4` (r26 >= 26) are meant to be the
stronger rungs.  But all three carry `when: { cheapest_in_suit: true }`, and
`cheapest_in_suit` means *the lowest legal level in that strain*
(`inference/engine.py:157-167`).  In an uncontested auction the 2-level is
always still available, so the 3- and 4-level rungs **can never fire** — and
the 2-level rung is gated off at r26 >= 26.  A hand with a good six-card suit
and partnership game values therefore has **no rebid of its own suit at all**.

Reproduced, board 462: `(P) (P) 1D 1H (P) 2C (P)` — the 1H overcaller holds
`J8.AKQJ43.KT.J76` (15 HCP, AKQJ43).  2H is blocked by the r26 cap, 3H is not
"cheapest", so the engine raises partner's clubs on `J76` (`uc_raise_C3`, 3C,
priority 31 beating 3NT at 29 by 0.006).  3C made 11; the other table's 3NT
made 11 for 630.

Fix: drop `cheapest_in_suit` from the `*3` and `*4` rungs of `uc_rebid_*`
(and, for consistency, `cl_rebid_*`/`ch_rebid_*`/`balhigh_rebid_*` — the level
is chosen by the value bands, which is exactly what the rule's own comment
says).  Verified: board 462 then offers 3H at fit 1.00.
Second half of the same board (below, F6) is needed to make it *win*.

Note while you are there: with `cheapest_in_suit` removed, `uc_rebid_H3`
(r26 >= 22) and `uc_rebid_H4` (r26 >= 26) overlap for r26 >= 26.  Cap the `*3`
rung with `not: { evals: { rule_of_26: [26,99] } }` so the ladder is exclusive,
*or* give `*4` a priority one higher.  (Left overlapping in my test run; the
list order picked 3H, which was the right call, but that is luck.)

---------------------------------------------------------------------------
## CLUSTER 11 — `rmr_3NT` | 4 boards | 30 IMPs
### VERDICT: MISSING-AGREEMENT (3 boards) + slam depth (1 board)

**Mechanism.**  Context `responder_after_minor_rebid` (`1m - P - 1M - P - 2m - P - ?`)
ladders responder's *strength* contiguously — `rmr_2M` 6-10, `rmr_2NT` 11-12,
`rmr_3NT` 13-18 — but its **shape** ladder dead-ends: the only rule that
mentions responder's own six-card major is `rmr_2M`, capped at 10 HCP.  A
responder with a six-card major and 11+ therefore has 3NT and nothing else.
This is a hole the `gap` lint cannot see: the *strength* bands are contiguous;
what is missing is a shape rung inside them.

Reproduced (all three):

| board | responder | engine | 3S offered? |
|---|---|---|---|
| 20 | `AJT643.J87.K6.AQ` 15 HCP, 6 spades | 3NT | **no candidate at all** |
| 190 | `AT8642.KQ4.K63.Q` 14 HCP, 6 spades | 3NT | no |
| 199 | `AK8542.K.T8.A432` 14 HCP, 6 spades | 3NT | no |

Best alternative offered on board 20 was 2NT at fit 0.134; 2S (`rmr_2M`) scored
0.004.  All three played 3NT down one with the spade partscore/game cold.

**Fix** — two rules in `responder_after_minor_rebid`, after `rmr_3NT`:

```yaml
      - id: rmr_3$M
        call: 3$M
        priority: 57
        requires: { hcp: [11, 15], suits: { $M: [6, 13] } }
        shows: "6+ $M, invitational or better opposite the minimum rebid"
        establishes: { forcing: invitational, agreed_suit: $M }
      - id: rmr_4$M
        call: 4$M
        priority: 58
        requires: { hcp: [16, 21], suits: { $M: [6, 13] } }
        shows: "6+ $M, game values"
        establishes: { forcing: sign_off, agreed_suit: $M }
```

Verified: boards 20 / 190 / 199 all now bid **3S**.  I deliberately made the
11-15 rung invitational rather than splitting 11-13/14+ into game: on board 190
partner holds a singleton spade and 4S is down one, so the wide invitational
band is worth more than the extra game.  (Measured on the three boards: 3S
recovers roughly 8+6+1 IMPs; a 14+-bids-game split recovers 13+0+1.)

**Board 529 is a different animal** — `1C - 1S - 2C - 3NT`, responder 16 HCP
5-4-2-2, 3NT made 11 while the other table found 6C.  3NT is the right call on
that hand; the loss is slam depth (see F1/F2 below), not this context.

---------------------------------------------------------------------------
## CLUSTER 12 — `uc_rebid_D4` | 2 boards | 30 IMPs
### VERDICT: MISSING-AGREEMENT (the generic ladder has no top and no landing)

Both boards are 32-point double fits that died at the four level.  Traced
call-by-call:

**Board 377** `1D - 1S - 2D - 3C - 3D - 4C - 4D - P`, E/W hold 32 HCP with a
7-card and a 6-card suit; 4D made 13.  Reproducing every decision: responder
W (`AK53.85.K.AKQ652`, 19 HCP) has, at its final turn, exactly three
candidates — 4S at 0.015, 4NT at 0.000, 5D at 0.000 — and passes.  There is no
`uc_rebid_C5` (the ladder stops at 4), `uc_minor_game_5C` needs *partner's*
minor, and `gst_rkc_C` needs `partner_last_suit: C` (partner bid diamonds).
So a 19-count with AKQ-sixth has literally no legal descriptive call.

**Board 830** is the competitive twin: opener holds `86.A7.AKQ9843.A2`
(17 HCP, AKQ-seventh) opposite partner's *free* 4C over a 3H preempt, and
`uc_rebid_D4` — `total_points: [14, 40]`, no upper cap — signs off in 4D.

**Mechanism, stated generally:** `uc_new_X3` and `uc_rebid_X4` are the top of
the generic toolkit; both are `non_forcing` with an **open-ended top point
band**, and there is no rung above them.  The pair therefore ping-pongs its two
suits up to the four level and then one of them passes with a hand no rule
describes.  The named rule is the last rung, not the disease.

**Fix (in priority order, cheapest first):**
1. `uc_new_C3/D3/H3/S3` (a new suit at the three level, 14+ total points, in an
   uncontested constructive auction) should be `forcing: one_round`, not
   `non_forcing`.  A 14+ new suit at the 3-level that partner may pass is not a
   playable agreement.
2. Cap `uc_rebid_X4` at the point where the slam machinery must take over —
   `total_points: [14, 21]` — mirroring the cap DECISIONS records for the
   specific-context 4M raises ("capped where the keycard gate opens").
3. Add the fifth rung for one's own six-card suit in an uncontested GF-ish
   auction (`uc_rebid_C5/D5`, 6+ cards, `rule_of_26 >= 30`), so the 19-count on
   board 377 has *something*.

I did **not** verify 1-3 end to end (both boards need three or four correct
decisions in a row, and after the first change the auction diverges).  I would
implement 1 and 2 and measure; 3 only if the pair still strands.  Cluster 12 is
2 freak boards — do not spend more than that on it.

---------------------------------------------------------------------------
## CLUSTER 13 — `cl_raise_H4` | 3 boards | 29 IMPs
### VERDICT: IMPLEMENTATION-BUG in `general_slam_try` (the named rule is the symptom)

`cl_raise_H4` is the *only* thing that fires because the slam try above it
cannot.  `gst_rkc_H` (priority 46, well above `cl_raise_H4`'s 32) reads:

```yaml
requires:
  suits: { H: [4, 13] }
  evals: { total_points: [17,40], controls: [4,12], rule_of_26_sharp: [31,99],
           "lott_total_trumps(H)": [8,26] }
```

`suits: { H: [4,13] }` **double-counts the trump requirement that
`lott_total_trumps(H) >= 8` already enforces sharply**, and it is a soft gate,
so a three-card raise scores ~0.35 and the rule dies.  This is the mirror image
of the fix DECISIONS records ("the game-level major raise took three trumps
flat … it counts *combined* trumps now"): the combined count was added and the
raw 4-card gate was never removed.

Reproduced, board 652 — `1H (2H) ?`, responder `AQ52.JT3.AK832.A`:
`total_points 19`, `controls 7`, `rule_of_26_sharp 31`, `lott_total_trumps(H) 8`,
`keycards(H) 3` — **every gate passes except the four-card one**, and 4NT scores
0.349 against `cl_raise_H4` at 1.00.  The pair holds all five keycards and 6H
made 13; the other table bid it.

**Fix:** in `gst_rkc_C/D/H/S`, `suits: { X: [4, 13] }` -> `suits: { X: [3, 13] }`.
Verified: board 652 now bids **4NT** (and the 5S/6H continuation is already
authored and correct).  Nothing else in my slice regressed; 639 tests pass.

**Board 45** (`1H (2H) ?` holding `Q.A98643.K.KT532`, 6-card support, 11 total
trumps, 6H cold) is *not* recovered by that fix: `rule_of_26_sharp` reads 30
even counting shortness in the agreed suit, one short of the 31 line.  See the
"31 combined points" section below — I do **not** recommend moving the line.

**Board 387** (-3) is noise.

---------------------------------------------------------------------------
## CLUSTER 14 — `fallback` | 3 boards | 28 IMPs
### VERDICT: splits — one IMPLEMENTATION-BUG (13 IMPs) and one NEEDS-EXCEPTION (15)

### 14a. Board 938: the 2/1 over 1H does not deny four spades.  IMPLEMENTATION-BUG.

Compare, in `resp_over_1S` and `resp_over_1H`:

```yaml
r1S_2C / r1S_2D / r1S_2H:  not: { suits: { S: [4, 13] } }     # denies opener's major
r1H_2C / r1H_2C_4 / r1H_2D: not: { suits: { H: [4, 13] } }     # denies opener's major only
```

Over 1S there is no cheaper major, so denying spade *support* is the whole
story.  Over 1H there *is*: responder must bid 1S before a 2/1 in a minor.  The
denial was never added, and `r1H_2D` has priority **76** against `r1H_1S`'s
**72**, so with both at fit 1.00 the 2/1 wins on priority.

Reproduced: `1H (P) ?` holding `AKQJT987..QJT7.2` — **eight solid spades and a
void in partner's suit** — the engine responds **2D**, with 1S sitting at fit
1.00 in the alternatives.  The auction then went
`2D-3D-3S-4NT-5C-(X)-XX-5D` and played 5D with 6S cold.

**Fix:**

```yaml
# r1H_2C, r1H_2C_4, r1H_2D
not: { any_of: [ { suits: { H: [4, 13] } }, { suits: { S: [4, 13] } } ] }
```

Verified: the hand now responds **1S**, and opener's follow-up (2D, a reverse)
keeps the eight-bagger findable.  This is not a one-board fix — every 12+ hand
with four spades and a longer minor is currently bypassing its major.
(If you want to be conservative, `[5, 13]` instead of `[4, 13]` covers the
disaster class without touching the 4-card-spade judgement call; the 2/1 branch
over 1S denies four, so I recommend four for symmetry.)

### 14b. Boards 373 and 22: the forced continuation invents a four-level three-card suit.  NEEDS-EXCEPTION.

Traced board 373 decision by decision.  `1D-2C-2NT-3C-3D-4C-4D-?` with W
holding `AQJ.J93.3.KJ9752`: the game force forbids pass, every remaining
candidate scores 0.000, and the backstop bids **4H on `J93`** — 4H by W, six
tricks.  Board 22 is identical in shape (2C-2D-3C-3D-4C-4D-**4H** on `KQJ9`
opposite a hand that has bid spades and diamonds).

The pair is genuinely lost (12 opposite 12 with no fit and no stopper on 373),
so I would not chase the auction; I would bound the damage.  DECISIONS already
carries the analogous invariant ("Fallback notrump never above 3NT: at the
4-level and beyond NT is conventional, so an invented natural 4NT is always
wrong").  The sibling invariant is missing:

**Fix (fallback layer, `engine` not YAML):** the forced-continuation backstop
must never invent a *new suit* at the four level or higher in fewer than five
cards; with nothing five-long it should repeat the longest suit already bid by
our side, or bid the cheapest notrump if legal below 4NT.  Both boards then
land in 5C/4D instead of 4H, worth roughly 250-300 points each.

---------------------------------------------------------------------------
## CLUSTER 15 — `r1sr_2NT` | 3 boards | 27 IMPs
### VERDICT: MISSING-AGREEMENT, two distinct holes, both verified fixed

### 15a. Opener has no acceptance of the 2NT invite after `1m - 1H - 1S` (boards 89, 351; 20 IMPs)

The file has an opener-over-invitational-2NT context for
`1M - 1NT - 2x - 2NT`, for `1H - 1S - 2m - 2NT`, and for the Stayman and
2NT-jump trees.  It has **none** for `1m - P - 1H - P - 1S - P - 2NT - P - ?`.
The position therefore falls to the generic toolkit, and `uc_nt3` requires
`semi_balanced`, which a 4-1-5-3 opener is not.

Reproduced (both boards): 3NT scores **exactly 0.000** and opener passes with
13 HCP; both hands are 5-4 with a singleton, both 3NTs make, and par on both
boards *is* 3NT.

**Fix** — a new context (I placed it just before `opener_over_second_suit_raise`):

```yaml
  - id: opener_over_invite_2NT_after_1S
    description: "Opener over responder's 2NT invite after 1m - 1H - 1S"
    expand: { m: [C, D] }
    pattern: "1$m - P - 1H - P - 1S - P - 2NT - P - ?"
    rules:
      - id: oi1s_pass_$m
        call: P
        priority: 60
        requires: { evals: { total_points: [10, 13] } }
        shows: "declining the invite: minimum opener"
        establishes: { forcing: sign_off }
      - id: oi1s_3NT_$m
        call: 3NT
        priority: 58
        requires: { evals: { total_points: [14, 19] } }
        shows: "accepting the invite: 14+ counting the fifth card"
        establishes: { forcing: sign_off }
      - id: oi1s_3$m
        call: 3$m
        priority: 57
        requires: { suits: { $m: [6, 13] }, evals: { total_points: [10, 13] } }
        shows: "6+ $m, minimum: re-offering the long suit"
        establishes: { forcing: sign_off }
```

Note the currency: `total_points`, not `hcp`.  Both losing hands are 13 HCP
with a five-card suit — the textbook "count the fifth card when accepting a
notrump invitation".  A flat 13 still declines (`total_points` 13).
Verified: both boards now bid **3NT**.

### 15b. Responder's own six-card heart suit dead-ends at 9 HCP (board 821; 7 IMPs)

`r1sr_2H` is 6-9 with 6+ hearts and there is no rung above it, while
`r1sr_2NT`/`r1sr_3NT` carry no shape gate at all.  Board 821's responder
(`Q2.AQT873.JT9.K8`, 12 HCP, AQT873) therefore bids **2NT**.  Identical species
to cluster 11.

**Fix** — after `r1sr_2H`:

```yaml
      - id: r1sr_3H
        call: 3H
        priority: 57
        requires: { hcp: [10, 13], suits: { H: [6, 13] } }
        shows: "6+ hearts, invitational"
        establishes: { forcing: invitational, agreed_suit: H }
      - id: r1sr_4H
        call: 4H
        priority: 58
        requires: { hcp: [14, 19], suits: { H: [6, 13] } }
        shows: "6+ hearts, game values"
        establishes: { forcing: sign_off, agreed_suit: H }
```

Verified: board 821 now bids **3H** (was 2NT).  Only partial recovery — the
other table reached 4H opposite a singleton — but the systemic lie is gone.

---------------------------------------------------------------------------
## CLUSTER 16 — `qr3_4NT_quant` | 3 boards | 26 IMPs
### VERDICT: NEEDS-EXCEPTION (the rework did not overshoot; it lacks a shape gate)

`qr3_4NT_quant` requires only `hcp: [15,40]` and `rule_of_26_sharp: [30,99]`.
There is **no shape condition anywhere in the quantitative family**, and the
only escape hatch (`qr3_4H_freak`/`qr3_4S_freak`) is gated at *seven* cards
**and** `total_points: [0, 14]` — i.e. it only rescues weak freaks, never
strong ones.  So the quantitative raise, an agreement about balanced hands,
fires on:

| board | hand raising 3NT | shape |
|---|---|---|
| 221 | `KQ.AKQJT6.A9.AK6` 24 HCP | **six solid hearts** |
| 303 | `J.K52.A6.AKJ7642` 16 HCP | **seven clubs** |
| 677 | `3.KQJ72.AKQ64.K4` 19 HCP | **5-5** |

Board 221 is the recoverable one: 4NT made 12 for 690 where 6H is 1430.

**Fix (verified):**
1. Add to both `qr3_6NT` and `qr3_4NT_quant`:
   `not: { evals: { longest_suit_length: [6, 13] } }`.
   (`semi_balanced` does **not** work — 6-3-2-2 is semi-balanced; I tried it
   first and board 221 was unchanged.)
2. Widen the pull so the excluded hands have somewhere to go — change the two
   freak rules to `suits: { $M: [6, 13] }`, `total_points: [0, 21]`, and add the
   strong branch:

```yaml
      - id: qr3_6H_solid
        call: 6H
        priority: 42
        when: { my_suit: H }
        requires: { suits: { H: [6, 13] },
                    evals: { total_points: [22, 40], "two_of_top3(H)": [1, 1] } }
        shows: "self-sufficient six-card major and slam values: bidding it"
        establishes: { forcing: sign_off, agreed_suit: H }
      # ...and the spade twin
```

Verified: board 221 now bids **6H** (making 12).  Board 303 becomes a pass of
3NT — which scores *the same* as the 4NT+1 it used to make (660 either way), so
the shape gate costs nothing there; reaching its 6C needs real minor slam
machinery, not this rule.  Board 677 (-2) is unchanged and not worth a rule.

**On "did the rework overshoot?"** — No.  The quantitative machinery does
exactly what DECISIONS says it was built to do; it simply was never told it is
a *notrump* agreement.  Note also that on 2 of these 3 boards the call
immediately before `qr3_4NT_quant` is `gf_3NT` (cluster 4, reviewer A's slice)
firing on a 2-count and a 13-count with a singleton in partner's long suit —
the quantitative raise is reasoning off a 3NT that lied.  Fix `gf_3NT` first.

---------------------------------------------------------------------------
## CLUSTER 17 — `rkc5D_slam` | 2 boards | 26 IMPs
### VERDICT: NOTHING-WRONG.  The 5D counting rewrite is vindicated by both boards.

I reproduced every keycard call on both boards.  In each, the arithmetic is
*exactly right* and the engine bids the small slam it is entitled to:

| board | asker | asker's keycards | trump Q | replier | reply | total |
|---|---|---|---|---|---|---|
| 269 | `KJT7.QT95.A8.A62` | 2 (A♦ A♣) | **yes** (Q♥) | 3 (A♠ A♥ K♥) | 5D = 0-or-3 | **5 of 5** |
| 367 | `AQJ532.K62.KT.AK` | 3 (A♠ K♠ A♣) | **yes** (Q♠) | 2 (A♥ A♦) | 5D... | **5 of 5** |

(Board 367's 5D reply is correct: with spades agreed the trump *king* is a
keycard, so `K84.A74.AQ432.T9` holds three, not two.  I checked
`keycards(agreed)` directly: 3.0.  The asker holding 3 then takes the
`keycards 4-5`/`2 + r26>=28` branch — reproduced as 6S, correct by the rule's
own logic since 3+2 = 5.)

So both boards are **6 bid, 7 cold, BEN bid 7**.  That is the grand-slam gap
DECISIONS deliberately scoped out ("The 5NT king ask was considered and
deliberately skipped … without the 7-level decision the ask is pure
information leakage").  The rework did not overshoot in either direction.

**Optional, narrow MISSING-AGREEMENT** if you ever want these 26 IMPs: both
boards land in the *same* decidable state — asker holds **exactly 2 keycards
plus the trump queen** and partner's 5D can only be 3, so all five keycards and
the queen are located and the only open question is the thirteenth trick.  A
rule of the form "over the 5D reply, with 2 keycards + the trump queen + a
9-card fit + `rule_of_26_sharp >= 34`, bid the grand" is expressible without
cross-hand arithmetic.  I would **not** author it on two boards of evidence:
a wrong grand costs a slam swing every time, and grands are rare enough that
1000 boards cannot adjudicate the rule.  Recorded, not recommended.

---------------------------------------------------------------------------
## CLUSTER 18 — `ch_raise_H4` | 3 boards | 25 IMPs
### VERDICT: splits — MISSING-AGREEMENT (board 93, 16 IMPs) + NOTHING-WRONG (230, 598)

### 18a. There is no five-level rung anywhere in the competitive toolkit.

`general_competitive_high` (`... - bid>=3C - ?`) ladders raises and rebids to
the **four level and stops**.  `general_balancing_high` likewise.  So once the
opponents bid four of a major over our four-level suit, our side has *no legal
descriptive call whatsoever*.

Reproduced, board 93 — `1C (1S) 2H (3S) 4H (4S) ?`, W holds
`.QJ9752.K9854.A3`: a **void in their suit**, six hearts, partner has raised to
game in hearts.  The engine's entire candidate list is `P`, `X` (0.000) and
`4NT` (0.000).  It passes; 4S made for -620 where 5H makes (4H made 12 at the
other table).  Boards 422 and 420 are the same hole.

**Fix** — four rules in `general_competitive_high` (mirror them into
`general_balancing_high`):

```yaml
      - id: ch_raise_H5      # and ch_raise_S5
        call: 5H
        priority: 32
        when: { partner_suit: H, cheapest_in_suit: true, we_hold_contract: false }
        requires:
          suits: { H: [4, 13] }
          evals: { "lott_total_trumps(H)": [10, 26], max_their_suit_length: [0, 2],
                   total_points: [8, 40] }
        shows: "five-level LOTT raise: ten combined trumps and shortness in their suit"
        establishes: { forcing: non_forcing, agreed_suit: H }
      - id: ch_rebid_H5      # and ch_rebid_S5
        call: 5H
        priority: 29
        when: { my_suit: H, cheapest_in_suit: true, we_hold_contract: false }
        requires:
          suits: { H: [6, 13] }
          evals: { "lott_total_trumps(H)": [9, 26], max_their_suit_length: [0, 1],
                   total_points: [8, 40] }
        shows: "five-level rebid of my own six-card suit: LOTT trumps, void/stiff in theirs"
        establishes: { forcing: non_forcing }
```

The `max_their_suit_length` gate is the point: at the five level the licence is
shortness in their suit, not points, and that evaluator is already sharp.
Verified: board 93 now bids **5H** (-620 becomes +650).  Board 422 does *not*
flip (five hearts, not six, and the shown LOTT count is 9) and board 420 does
not (partner never bid; LOTT reads 6) — I left both, because loosening the gate
far enough to catch them is exactly how a five-level rule turns into a phantom
sacrifice generator.

### 18b. Boards 230 and 598 — NOTHING-WRONG (with one honesty repair)

`1H - P - 2H - (3C) - 4H` on 16-18 opposite a 6-9 single raise, both down.
`ch_raise_H4` fires at `rule_of_26` exactly 26 against a gate of 25 with
`lott_total_trumps(H)` exactly 8.  This is the thin-game dribble DECISIONS
names and the Phase-3 result warns against tuning.  Leave the numbers alone.

One real defect worth a one-word edit: the rule's `shows:` text says
**"13+ support points"** while `requires` says `total_points: [11, 40]`
(same in `cl_raise_H4/S4`, `ch_raise_S4`).  Partner's model is built from the
constraint, but a human reading the file — or the next reviewer — is misled.
Make the text say 11+.  Also consider `rule_of_26_sharp` instead of
`rule_of_26` on the four-level raises: the soft version scores 0.8 at 24 and
0.6 at 23, so the "25" gate leaks two points in both directions.  That is a
representation fix, not a threshold change — but measure it.

---------------------------------------------------------------------------
## CLUSTER 19 — `cl_new_S2` | 3 boards | 25 IMPs
### VERDICT: MISSING-AGREEMENT — our 1NT opening has no competitive follow-up on either side

All three boards are "we opened 1NT, they overcalled, and the generic
competitive toolkit took over".  Two distinct seats fail:

**Opener's seat (boards 284, 291).**  Having opened 1NT (15-17, five spades),
the engine bids a natural **2S** over their 2H with `cl_new_S2`
("5+ cards, 10+ points").  A 1NT opener has already described the hand; a
2-level suit bid re-describes it as a limited one-suiter and buries 3NT.
Board 284: 2S made 8 where 3NT made 10.  Note the strength trap behind it —
after partner has passed, `cl_nt2` is 11-12 and `cl_nt3` needs
`rule_of_26 >= 24`, so a **16-count 1NT opener has no notrump rebid at all**.

**Responder's seat (board 638).**  Reproduced: `(P) (P) 1NT (2C) ?` holding
`6.QT96.QJT9.AQ73`, 11 HCP opposite 15-17 — the engine **passes**.  The
negative double is correctly refused (four cards in their suit), and
`cl_nt2`/`cl_nt3` are refused because `semi_balanced` reads **0.0** for 1-4-4-4.
3NT was cold at the other table.

**Fix** — one small context, natural methods only (no Lebensohl needed, and
the "no Michaels/no checkback" scope is untouched):

```yaml
  - id: responder_over_1NT_interference
    description: "Responder after their overcall of our 1NT opening"
    pattern: "1NT - bid - ?"
    rules:
      # 2NT/3NT do NOT require semi_balanced: opposite a shown balanced 15-17
      # the notrump decision is arithmetic, and a 4-4-4-1 eleven-count
      # currently has no call at all.
      - id: r1nti_3NT   { hcp: [10,40], evals: { weakest_their_stopper: [0.9,9] } }  -> 3NT, sign_off
      - id: r1nti_2NT   { hcp: [8,9],   evals: { weakest_their_stopper: [0.9,9] } }  -> 2NT, invitational
      - id: r1nti_X     { hcp: [9,40],  evals: { "suit_length(their)": [4,13] } }    -> X, penalty
      - id: r1nti_suit  natural 5+ suit, 6-10, cheapest_in_suit                      -> non_forcing
      - id: r1nti_pass  requires: {}                                                  -> floor
```
(shown schematically; write them out in the file's normal style)

and, for opener's seat, gate the generic new-suit rules with a new engine
condition `i_opened_notrump: false` — or, if you would rather not add a
condition, give `cl_nt2`/`cl_nt3` a branch keyed on partner having passed our
1NT (`hcp: [15,17]`, any `rule_of_26`) so 2NT/3NT beats the 2-level suit bid.

I did not verify these end to end (the context does not exist to patch).
Confidence is high on the diagnosis, moderate on the IMP recovery.

---------------------------------------------------------------------------
## CLUSTER 20 — `pref_2S` | 3 boards | 23 IMPs
### VERDICT: MISSING-AGREEMENT (board 298, 11 IMPs) + judgement (424, 308)

`responder_preference_after_1M_1NT_2m` has `pref_pass`, `pref_2M`, `pref_2NT`
and `pref_3M_limit` — and **no rule for responder's own long suit**.  The 1NT
response denied four *spades*; it said nothing about hearts, so after
`1S - 1NT - 2m` responder's hearts must have a home.  They do not.

Reproduced, board 298: responder holds `52.AKJT952.862.8` — **seven hearts to
the AKJT** — and takes a "simple preference" to 2S on a doubleton
(`pref_2S`, fit 1.00).  The other table played 4H.

**Fix** (only the `M: S` expansions need it):

```yaml
      - id: pref_2H_own
        call: 2H
        priority: 57
        when: { unbid_suit: H, cheapest_in_suit: true }
        requires: { suits: { H: [5, 13] }, hcp: [6, 9] }
        shows: "my own 5+ hearts: to play (1NT denied four spades, not hearts)"
        establishes: { forcing: sign_off }
      - id: pref_3H_own
        call: 3H
        priority: 58
        when: { unbid_suit: H }
        requires: { suits: { H: [6, 13] }, hcp: [7, 11] }
        shows: "my own 6+ hearts, invitational"
        establishes: { forcing: invitational, agreed_suit: H }
```

Verified: board 298 now bids **3H** (was 2S).

Secondary, lower confidence: `pref_pass` requires four of the minor while
`pref_2$M` accepts a doubleton major with no comparison to the minor, so
2-spades-3-clubs prefers 2S instead of passing 2C.  Textbook is
`pref_pass: suits { $x: [3,13] }` plus
`pref_2$M: evals: { "suit_diff($M,$x)": [0,13] }`.  I tested this on board 424
and it makes that board **worse** (passing 2C scores below 2S+3), so I am
**not** recommending it on this evidence.  Board 424's real miss is a 9-count
with AKT failing the 10-11 invite band — a threshold, which DECISIONS says not
to chase.  Board 308 (-2) is noise.

---------------------------------------------------------------------------
# WORST SINGLE BOARDS, #16 onward

### Board 349 (-12) — NOTHING-WRONG
`(P) (P) 1S X (P) 2H (2S) ?` with `QT3.AQ4.AK83.AT2`.  The doubler passes; par
is 3NT.  But the spade holding is QT3 opposite AK9872 — `weakest_their_stopper`
correctly refuses 3NT, `cl_doubler_raise3_H` correctly refuses to raise a
3-card heart advance to a 6-card fit, and +150 defending 2S-3 is a sound
result.  Par 600 here is a double-dummy artefact.  Leave it.

### Board 460 (-12) — IMPLEMENTATION-BUG (missing class floor) + NEEDS-EXCEPTION
Two things.  (a) `general_pull_or_sit` (`... - X - P - ?`) defines **P only via
`adx_sit`**, which needs `standing_suit_length >= 4` with quality.  Being the
more specific context it shadows `uc_pass`/`ch_pass`, so a hand with no trump
stack **must bid** — and here W (`7652.Q.KQ3.Q9752`, 9 HCP) pulled partner's
double of 4H with `uc_minor_game_5C` at fit 0.003, going -500.  This is exactly
the lesson DECISIONS records from round 4 ("a fix that changes a whole class
needs a floor for the whole class").
**Fix (verified):** add a permissive floor to `general_pull_or_sit`:
```yaml
      - id: adx_pass_floor
        call: P
        priority: 20
        requires: {}
        shows: "nothing worth pulling to: partner's double stands"
        establishes: { forcing: sign_off }
        negative_inference_weight: soft
```
At priority 20 it blends to 0.754, so any genuine fit-1.00 pull (priority 54+,
0.86) still wins and `adx_sit` (61) still wins; only garbage-fit pulls lose.
Verified: board 460 now passes.
(b) **Caveat, stated honestly:** on *this* board passing may not gain, because
E's double of 4H was itself dubious — `balhigh_reopen_X`'s light branch
(`hcp 12+` with `max_their_suit_length <= 1`) doubled a freely-bid game with 13
HCP and a stiff.  Gate that branch with `standing_bid_level: [1,2,3]`; the
16+/short branch can keep the full range.  I would ship the floor regardless —
it is a class defect — and the level gate with it.

### Board 620 (-12) — MISSING-AGREEMENT (no stopper-ask with a minor agreed)
`1C - 2C - 3C - ?` holding `985.AQ6.AK8.9642`.  Reproduced: `gf_minor_3NT`
scores 0.067 (no spade stopper — correctly), so the engine bids 5C, down one,
where 3NT from the *other* side makes.  The engine has fourth-suit forcing but
no way to ask for a stopper when only two suits are on the table.
**Fix:** with a minor agreed in a game force and 3NT still live, a bid of an
unbid MAJOR below 3NT is artificial and asks for a stopper there (opener bids
3NT holding one, otherwise repeats/raises the minor).  Same family as the 4SF
that already exists; ~6 rules.  Recovers this board and probably board 405.

### Board 727 (-12) — IMPLEMENTATION-BUG (priority)
`(P) 1C (1D) ?` holding `93.AKJ8.J532.A87`.  Reproduced: the engine jumps to
**3NT** (`cl_nt3`, priority 29) with **1H at fit 1.00** in the alternatives
(`cl_new_H1`, priority 25).  Bidding notrump past a biddable four-card major
at the one level is never right in a competitive auction; the other table found
the 4-4 heart game.
**Fix (verified):** raise `cl_new_H1` and `cl_new_S1` from priority 25 to 30
(above `cl_nt1/2/3` at 27/28/29).  Board 727 then bids **1H**; 639 tests pass.
This is "show a major at the one level before bidding notrump" — canon, and
it costs nothing, since both rules already require the suit.

### Board 794 (-12) — IMPLEMENTATION-BUG, two of them
`1S (X) 2NT` — Jordan, artificial, one-round-forcing — **passed out by opener**
in 2NT with a 5-0 diamond misfit, -300.  Two causes, both verified:
1. X1 above (`uc_pass` defeating the forcing filter).
2. `opener_over_competitive_2NT` has only `oc2nt_3$M` and `oc2nt_4$M`, both
   requiring **six** cards in the major.  A five-card-major opener — i.e. most
   of them — has no reply at all.
**Fix:** X1's one-liner, plus two rules:
```yaml
      - id: oc2nt_five3_$M
        call: 3$M ; priority: 57
        requires: { suits: { $M: [5,5] }, evals: { total_points: [10,14] } }
      - id: oc2nt_five4_$M
        call: 4$M ; priority: 61
        requires: { suits: { $M: [5,5] }, evals: { total_points: [15,40] } }
```
Verified: opener now bids **3S**.  (Secondary observation: `jordan_2NT`
requires `total_points: [10,40]` and this 6-HCP 5-3-0-5 hand reaches 8-11
depending on the agreed suit — a limit raise it is not.  I would raise the
Jordan floor to `total_points: [11,40]` *and* add `hcp: [8,40]`, so shortness
alone cannot manufacture a limit raise.  Untested; the reply rules above fix
the disaster either way.)

### Board 989 (-12) — IMPLEMENTATION-BUG (a gate the sibling rule has and this one lost)
`2H - 2NT - 3H - 4H` with the asker holding `4.8.AKQ86.AQT975` — **one heart**.
`w2ac_game_$W` requires only `total_points: [15, 40]`; DECISIONS records the
matching fix on the direct raise ("Weak-two game raises need 3+ trumps"), and
this rule in `weak2_ask_continuation` never received it.
**Fix (verified):** `requires: { suits: { $W: [3, 13] }, evals: { total_points: [15, 40] } }`.
Board 989 then passes opener's 3H (making, +140) instead of playing 4H down one.

### Board 2 (-11) — IMPLEMENTATION-BUG (priority) + MISSING-AGREEMENT
`1S - 2D - 3D - ?` holding `AQ7.92.A9865.KQ2`.  Reproduced: the engine bids
**5D** (`gf_game_5D`, priority 33, blended 0.799) while **4S and 3S both sit at
fit 1.00** (blended 0.796 and 0.793).  Five of a minor beat four of a major by
three thousandths.  DECISIONS already carries this maxim twice ("with a minor
fit the game is 3NT"; "a game raise in a minor could outrank a one-level bid in
my own longer major") — it was never applied to `gf_game_5$m`.
**Fix (verified):** `gf_game_5$m` priority 33 -> 30.  Board 2 then bids 4S.
**Also missing:** after opener *raises* responder's 2/1 minor (`1S-2D-3D`),
responder's 3-card major support has no trump-setting raise — the family
DECISIONS authored covers opener's 2M rebid, 2NT rebid and second suits, but
not opener's raise.  3S there puts this board on the slam floor where 6S lives.

### Board 85 (-11) — NEEDS-EXCEPTION (the slam gate's own-hand floor)
`1D - 1H - 3H - ?` holding `K9.AQJ65.KJ75.53` opposite a 16-18 jump raise.
Reproduced: `gst_rkc_H` scores **0.80** — every gate passes
(`rule_of_26 34`, `controls 4`, 9-card fit) except `total_points: [17,40]`,
and the hand has **16**.  6H made 12 at the other table.
**Fix (verified):** lower the own-hand floor in `gst_rkc_*` to
`total_points: [15, 40]`.  Board 85 then bids 4NT; 639 tests pass.
Rationale: the gate pair `own >= 17` AND `combined >= 31` double-counts.  The
combined number is the one that decides slam, and opposite a *narrow, strong*
shown range (a 16-18 jump raise) the own-hand floor blocks precisely the hands
the raise is inviting.  See the "31 combined points" note below.

### Board 265 (-11) — MISSING-AGREEMENT (the balancing-high family has no 4-level new suit)
`(3D) X (4D) P P ?` with W holding `KQ87.AK9..AKQ532` — **21 HCP and a
diamond void** — and the engine passes.  Reproduced: the entire candidate list
is `P` and a second `X` at 0.349 (blocked by `longest_suit_length: [0,5]`; W has
six clubs).  `general_balancing_high` ladders new suits only to the **three**
level (`balhigh_new_*1/2/3`), so 4S over their 4D simply does not exist —
whereas the competitive family does have `ch_new_*4`.
**Fix:** mirror `ch_new_C4/D4/H4/S4` into `general_balancing_high`, and add the
doubler's variant (`my_last_call_was_double: true`, `hcp: [19,40]`,
`suits: [4,13]` — a takeout double promised the suit, so four cards suffice
when partner could not act).  I added the competitive-family version and
confirmed it does not fire here only because the context is the *balancing*
one; the same rules in the right context resolve the board.

### Board 281 (-11) — NEEDS-EXCEPTION
`1C - P - 1H - (3S) ?` with opener holding `.J42.AK72.KQJ543` — void in their
suit, six clubs, 14 HCP — and the engine passes.  4C scores 0.409, blocked by
`ch_rebid_C4`'s `rule_of_26: [26, 99]`: partner's 1H response shows 6-10, so
`partner_mid` = 8 and the sum is 24.  The 3S jump overcall is *why* opener must
act; a void in their suit is worth the two points the gate is missing.
**Fix:** add an `any_of` branch to `ch_rebid_C4/D4/H4/S4`:
`{ evals: { rule_of_26: [23,99], max_their_suit_length: [0,0] } }` alongside the
existing 26 branch.  Untested; lower confidence — this is the kind of gate
loosening that has misfired before, so measure it alone.

### Board 401 (-11) — NOTHING-WRONG, and important counter-evidence
`1D-1S-1NT-2C-3C-4NT-5H-6C`, down one.  Reproduced the arithmetic: the pair
holds 4 of 5 keycards, the trump queen is in the asker's hand, 30 combined HCP,
an 8-card club fit — `rkc5H_slam`'s "2+2 with the queen" branch is textbook and
the slam is a normal bet that failed.  Keep it.  Note for the section below:
this hand's `rule_of_26_sharp` is right on the 31 line, so it is the board that
argues *against* lowering it.

### Board 405 (-11) — NOTHING-WRONG / low priority
`(P) 1D (1S) 2C (3S) ?` holding `A2.J83.A8532.K94` (12 HCP).  Reproduced: 3NT
scores 0.80 — one HCP below `ch_nt3`'s 13-19 band — and `ch_raise_C4` is
correctly refused (`lott_total_trumps(C)` = 8 against a gate of 10).  This is a
one-point threshold miss on a hand that is genuinely borderline.  Do not chase.
(The board would also be recovered by board 620's stopper-ask.)

### Board 420 (-11) — NOTHING-WRONG
`(3S) 4D (4S) P P ?` with `.AJ43.AQ8542.QT2`.  5D over 4S is a *sacrifice*
(-300 against -620), and partner has shown nothing — LOTT reads six trumps.
No sound gate reaches this bid; the five-level rules from 18a deliberately do
not.  Accept the loss.

### Board 422 (-11) — MISSING-AGREEMENT (same hole as 18a), not recovered
`1H (2H) 3H (4S) ?`.  Reproduced: only `P` and `X` at 0.007.  5H makes.  But
the shown trump count is 9 (partner's preemptive raise promises four, opener has
five) and the hand is vulnerable — the five-level rung I verified needs ten.
Recording it as the same defect; not prescribing a looser gate on one board.

### Board 462 (-11) — see X2 above.  IMPLEMENTATION-BUG, verified fixed.
Needs **both** halves: X2 (drop `cheapest_in_suit` from the `*3/*4` rungs) and
F6 below (a 3-card minor raise must not outrank showing my own longer major).
With both, the 1H overcaller with `AKQJ43` bids **3H** instead of raising
partner's clubs on `J76`.

---------------------------------------------------------------------------
# On the "31 combined points" slam-try line (DECISIONS records it as measured)

Reviewer A suspected staleness.  My boards bear on it directly, and my reading
is: **do not move the number — repair the three things around it.**

The evidence in my slice, all reproduced:

| board | `rule_of_26_sharp` | what happened | verdict |
|---|---|---|---|
| 652 | **31** (on the line) | blocked only by the redundant 4-card gate | gate bug, not level |
| 85  | 34 | blocked by the *own-hand* `total_points >= 17` floor (had 16) | floor bug, not level |
| 45  | 30 | not asked; 6H cold with **eleven** trumps | level *would* have caught it at 30 |
| 401 | ~31 | asked, bid 6C, **down one** | level is not too high |

Two of the four are blocked by gates that have nothing to do with the level;
the remaining two split one-for-one across it.  That is not evidence for moving
31, and the project's own history (Phase 3) says a one-point move measured on
four boards is noise.

What *is* worth fixing, and is not a threshold change:

1. **`suits: { X: [4,13] }` on `gst_rkc_*` is redundant with the sharp
   `lott_total_trumps(X) >= 8`** and blocks every three-card slam raise
   (board 652).  Verified fix; this is the single highest-value slam change I
   found.
2. **The own-hand `total_points >= 17` floor double-counts the combined gate**
   and blocks 15-16-counts opposite narrow strong ranges (board 85).  Verified
   fix at 15.
3. **`rule_of_26` is a systematically pessimistic estimator, and 31 was
   calibrated against it.**  `evaluators.py:105-117` computes
   `partner_mid = (floor + min(max, floor+4)) / 2`.  A one-of-a-suit opening in
   this system shows 10-21 (rule-of-20 openings lowered the floor), so
   `partner_mid` = **12** — about 2.5 points below what an opening bid is
   actually worth.  Every slam gate that counts partner's *opening* is
   therefore ~2.5 points short, which is exactly board 45's miss (30 vs 31).
   The honest repair is to the estimator, not the threshold: widen the cap
   (`floor+6`, or use the true midpoint of the shown band when the band is
   narrow).  **This changes many rules at once and must be measured on its own
   run** — but it is the reason the 31 line "feels" stale without being wrong.

---------------------------------------------------------------------------
# FIX LIST (deduplicated, prioritised)

Legend: **[V]** = implemented in a scratch YAML/engine copy and re-run on the
motivating board; **[U]** = diagnosed and reproduced, prescription untested.
The whole **[V]** set together passes `pytest` (639), `lint_system.py`
(identical to baseline) and `fuzz_decisions.py --n 200` (clean).

| # | change | boards recovered (IMPs) | endangers |
|---|---|---|---|
| **F1 [V]** | `gst_rkc_C/D/H/S`: `suits: { X: [4,13] }` -> `[3,13]`.  The sharp `lott_total_trumps(X) >= 8` already counts trumps. | 652 (13); opens the slam route on every 3-card raise | More 4NT asks on 5-3 fits.  Guarded by the unchanged 31/controls gates. |
| **F2 [V]** | `r1H_2C`, `r1H_2C_4`, `r1H_2D`: `not: { any_of: [ {suits:{H:[4,13]}}, {suits:{S:[4,13]}} ] }` — over 1H the 2/1 denies four spades. | 938 (13), plus every 12+ hand with 4 spades and a longer minor | Partnerships that deliberately bypass 4-card spades.  Use `[5,13]` if you want the conservative version. |
| **F3 [V]** | New context `opener_over_invite_2NT_after_1S` (`1m-1H-1S-2NT`): pass 10-13, 3NT 14-19 **counting length**, 3m with six. | 89 (10), 351 (10) | Accepting on 13 HCP + a five-card suit.  This is textbook invite acceptance. |
| **F4 [V]** | Missing "my own six-card suit" rungs: `rmr_3$M`/`rmr_4$M`; `r1sr_3H`/`r1sr_4H`; `pref_2H_own`/`pref_3H_own`. | 20 (13), 298 (11), 821 (7), 190 (6), 199 (1) | Slight upward pressure on partscores where 3NT was making anyway.  All three contexts previously had *no* rule for the shape. |
| **F5 [V]** | `general_competitive_high` (mirror into balancing): `ch_raise_H5/S5` (LOTT 10 + `max_their_suit_length <= 2`) and `ch_rebid_H5/S5` (6 cards, LOTT 9, `max_their_suit_length <= 1`). | 93 (16) | Five-level phantom sacrifices.  The shortness gate is what keeps it honest; do not loosen it to catch boards 420/422. |
| **F6 [V]** | X2: drop `cheapest_in_suit` from `uc_/cl_/ch_/balhigh_rebid_*3` and `*4`; **and** add `"suit_diff(m,H)"`/`"suit_diff(m,S)": [0,13]` to `uc_/cl_/ch_raise_C3/D3` (the C4/D4 rules already have it). | 462 (11) | Jump rebids where a simple rebid sufficed — the bands are what pick the level, and the 2-level rung's r26 cap keeps them disjoint.  Also cap the `*3` rung at r26 < 26 so it does not overlap `*4`. |
| **F7 [V]** | X1: `engine/decision.py` — add `and not sc.candidate.constraint.is_trivial` to the authored-pass relaxation. | 794 (12, with F8); stops one-round forces being passed out generally | Positions where the *only* sensible action was a floor pass over a forcing call.  639 tests pass; the real "sit for the double" rules keep their gates. |
| **F8 [V]** | `opener_over_competitive_2NT`: add `oc2nt_five3_$M` (5 cards, 10-14) and `oc2nt_five4_$M` (5 cards, 15+). | 794 (12) | Nothing — the position had no rule for a 5-card major. |
| **F9 [V]** | `w2ac_game_$W`: add `suits: { $W: [3, 13] }`. | 989 (12) | Missing a game opposite a weak two with a doubleton.  DECISIONS already made this call for the direct raise. |
| **F10 [V]** | `qr3_4NT_quant` and `qr3_6NT`: add `not: { evals: { longest_suit_length: [6,13] } }`; widen `qr3_4H/4S_freak` to 6 cards / `total_points [0,21]`; add `qr3_6H/6S_solid` (6+, `two_of_top3`, 22+). | 221 (12) | 6-level pulls of partner's 3NT.  Gated on a genuinely solid suit and 22+ points. |
| **F11 [V]** | `gf_game_5$m`: priority 33 -> 30 (below the generic major raises at 31/32). | 2 (11) | Nothing found; the maxim is already in DECISIONS twice. |
| **F12 [V]** | `general_pull_or_sit`: add permissive `adx_pass_floor` (P, priority 20, `requires: {}`). | 460 (12, partly — see caveat) | Re-loosening the round-4 "sitting is a positive decision" discipline.  Priority 20 keeps every fit-1.00 pull ahead of it.  Ship together with gating `balhigh_reopen_X`'s light branch to `standing_bid_level: [1,2,3]`. |
| **F13 [V]** | `cl_new_H1`/`cl_new_S1`: priority 25 -> 30 (above `cl_nt1/2/3`).  Show a major at the one level before jumping to notrump. | 727 (12) | Notrump contracts we used to reach directly.  The rules already require the suit, so only genuinely-4-card-major hands change. |
| **F14 [V]** | `gst_rkc_*`: own-hand floor `total_points: [17,40]` -> `[15,40]`. | 85 (11) | More keycard asks from the weaker hand.  The 31 combined gate and the controls gate are unchanged, which is what actually bounds it. |
| **F15 [U]** | `general_balancing_high`: add `balhigh_new_$X4` mirroring `ch_new_*4`, plus the doubler's own suit at the 4 level (`my_last_call_was_double`, 19+, 4 cards). | 265 (11) | Four-level balances.  Gate on 19+ and on partner having been unable to act. |
| **F16 [U]** | New context `responder_over_1NT_interference` (natural: 3NT 10+ with a stopper, 2NT 8-9, penalty X with 4 of their suit, natural suits, floor pass) — **and drop the `semi_balanced` requirement from the notrump rules there** (a 4-4-4-1 eleven-count opposite 15-17 currently has no call). | 638 (11), 284 (11) partly | Bidding 3NT on shapely hands opposite 1NT.  Opposite a shown balanced 15-17 that is correct. |
| **F17 [U]** | Stopper-ask with a minor agreed in a GF: a bid of an unbid major below 3NT is artificial and asks. | 620 (12), probably 405 (11) | A new convention; needs its own measurement.  Same shape as the existing 4SF. |
| **F18 [U]** | Fallback layer: the forced-continuation backstop must never invent a *new* suit at the four level or higher in fewer than five cards. | 373 (8), 22 (7) | Nothing — it is a bound on invention, in the same family as "fallback notrump never above 3NT". |
| **F19 [U]** | `uc_new_C3/D3/H3/S3` -> `forcing: one_round`; cap `uc_rebid_X4` at `total_points: [14,21]`. | 377 (15), 830 (15) — partial at best | Runaway uncontested auctions.  Measure alone; these are 2 freak boards. |
| **F20 [U]** | Honesty repairs, no behaviour change intended: `cl_raise_H4/S4`, `ch_raise_H4/S4` `shows:` text says "13+ support points" but requires 11.  Consider `rule_of_26_sharp` on the 4-level raises (the soft version leaks two points either way — a representation fix, not a threshold move, but measure it). | — | — |
| **F21 [U]** | `jordan_2NT`: add `hcp: [8, 40]` alongside `total_points: [10, 40]`, so shortness alone cannot manufacture a limit raise (board 794's 6-count). | 794 (belt and braces) | Passed-hand shapely raises losing their Jordan.  Low priority once F7/F8 are in. |

**Explicitly NOT recommended:**
- Moving the `rule_of_26_sharp >= 31` slam line.  My four binding boards split
  one-for-one across it; the level is not what is broken (see the section above).
- Loosening the five-level gates to catch boards 420/422.
- `pref_pass`/`pref_2$M` re-banding (tested; makes board 424 worse).
- Any move on the thin-game raise thresholds (`ch_raise_H4`, `ch_nt3`'s 13-19).
- Grand-slam machinery for cluster 17, on two boards of evidence.

**Recurring themes across this slice, and the two prior review rounds:**
1. *A ladder that bands by strength forgets to band by shape.*  Clusters 11, 15,
   20 and board 794 are all "responder holds a long suit / a five-card major and
   the context has no rung for it".  The `gap` lint sees strength bands only; a
   shape-rung detector ("a context whose rules never mention my longest suit")
   would have found all four.
2. *A gate added to one rule is not added to its siblings.*  F1 (combined trumps
   added, raw 4-card gate left), F9 (trump gate on the direct raise, not on the
   ask continuation), F2 (denial over 1S, not over 1H), F11 (the minor-vs-major
   maxim applied twice before, not to `gf_game_5$m`).  A lint that groups rules
   by `call`+role and diffs their gate *sets* would catch this species.
3. *Every ladder in the generic toolkit stops at the four level*, and the five
   level is where competitive bridge is decided (F5, F15).
