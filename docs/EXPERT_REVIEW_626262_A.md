# Expert review E5 — reviewer A: clusters 1-10 + worst singles 1-15
# Corpus: seed 626262, 1000 boards, -754 IMPs.  Dossier: e5_dossier.md
#
# All diagnoses below were reproduced through `choose_bid` (≈55 decisions).
# Candidate fixes were prototyped in a scratch copy of the YAML
# (scratchpad/w/p.yaml) and re-checked with tools/lint_system.py and
# tools/fuzz_decisions.py --n 300 (both clean: 0 collide / 0 gap / 0 shape /
# 0 soft, sibling 4 -> 2, 0 empty seats).  The working tree was not touched.

---------------------------------------------------------------------------
## Recurring themes (read this first)

**T1 — The forced-continuation backstop is unconstrained and therefore wins.**
`inference/fallback.py`'s last resort adds *the cheapest legal bid* with
`HandConstraint()` — fit 1.00, priority 1.0, blended score 0.703. Any real
candidate that merely fits well (0.8 → 0.63) loses to it. In a game force
below game, where pass is filtered out, this is the engine's *normal* outcome
whenever the authored ladders miss. Boards 707 (-17), 188 (-13), 730 (-12),
651 (-6) — **~48 IMPs in my slice alone** — are the engine bidding the
cheapest nonsense (4H holding QJT9876 spades; 4H holding a singleton heart,
which then got read as a trump agreement and drove to a 6-1 slam).

**T2 — `we_hold_contract` is true once PARTNER bids game, which switches off
every slam rule.** `inference/engine.py:142` returns True when "partner made
it and game is already reached". `gst_rkc_*`, all five general contexts and
the cue contexts are gated `we_hold_contract: false`, so after partner raises
us to 4M the seat has **zero candidates** and the `fallback` pass is the only
call. Boards 778, 395, 358 (and the fuzzer's own standing complaint,
`responder_after_1m1M_game_raise`).

**T3 — the generic ladders are strength-only; the shape rung is missing.**
`cl_new_$S1/2/3`, `ballow_new_$S1/2/3` read 4+@6 / 5+@10 / 5+@14 points with
`suit_quality >= 1.5` at every rung. A six-card suit with 8-13 points — the
single most common competitive hand there is — has no bid, and the catch-all
pass takes it. Cluster 1 is mostly this.

**T4 — `rule_of_26` gates are unreachable when partner has passed.** Partner's
floor is 0, so `rule_of_26 >= 22/24/26` on a *competitive* rebid can never be
met, and 16-20 point hands with a six-card suit pass out partscores (boards 1,
376, 5, 105). rule_of_26 is a constructive test being used as a competitive one.

**T5 — checkback is the largest single scoped-out convention.** Prior reviews
saw it as 1-IMP boards and left it out (DECISIONS.md; EXPERT_REVIEW_100 board
70, 919191 board 23). This corpus prices it properly: boards 217, 501, 970,
650, 913 in my slice plus cluster 11 (654, 328, 267) = **~86 IMPs**. The
919191 review's own board-76 fix (`rr_3$M_GF`) was written up but never
implemented — it is not in the YAML today.

---------------------------------------------------------------------------
## CLUSTER 1 — `all-pass`, 22 boards, 114 IMPs — SPLITS

### 1a. MISSING-AGREEMENT — the direct 4th seat over (1x) P (2x)
Six of the 22 boards are the family `1S P 2S` (×4) / `1H P 2H` (×2). In that
seat our side has not acted, so `cl_nt1/2/3` are all hard-blocked by
`when: {side_has_acted: true}` (the balancing twin `ballow_nt2_balance` DOES
exist — the sibling is simply missing on the competitive side), `cl_takeout_X`
demands `max_their_suit_length <= 2`, and the only suit bids are the
strength-only ladder (T3). Every remaining candidate lands at 0.8 and the
0.9 cliff turns it into `cl_pass`.

Reproduced:
* **B214** E `A73.KQ9.AJ62.AQ3` (19 HCP) over `1S P 2S` → **P**; X 0.349
  (3 spades), 3D 0.349. Nineteen balanced passes out a 2-level partscore.
* **B180** W `32.8.AQ9764.KQT5` (11 HCP, 6-4) over `1S P 2S` → **P**;
  X 0.8 (11 vs hcp 12), 3D 0.8 (13 tp vs 14). Two 0.8s, no bid.
* **B969** N `KJT984.3.Q53.954` over `1H P 2H` → **P** (2S needs 10 tp, has 9).
* **B940** N `JT8652.A3.A9.743` over `1NT P 2D` → **P** (2S blocked on
  `suit_quality(S)` 1.0 < 1.5 with a six-card suit).

**Fix (all verified in the scratch copy):**
1. New rule in `general_competitive_low`, mirroring `ballow_nt2_balance`:
   ```yaml
   - id: cl_nt2_direct
     call: 2NT
     priority: 37
     when: { their_last_bid_suit: true, side_has_acted: false, standing_bid_level: [2] }
     requires:
       hcp: [16, 21]
       evals: { weakest_their_stopper: [0.9, 9], semi_balanced: [1, 1] }
     shows: "natural 2NT over their two-level contract: 16-21 balanced, stopped"
     establishes: { forcing: non_forcing }
   ```
   (priority 37 so it outranks the widened `cl_takeout_X` at 36 — with 19
   balanced and three of their trumps, 2NT is the call, not a takeout double.)
2. `cl_takeout_X` — allow three of their suit when too strong to pass:
   ```yaml
   requires:
     any_of:
       - hcp: [12, 40]
         evals: { max_their_suit_length: [0, 2] }
       - hcp: [17, 40]
         evals: { max_their_suit_length: [0, 3] }
   ```
3. Shape rung on the generic new-suit ladders (also fixes T3 elsewhere):
   for each `$S` in C,D,H,S and each of `general_competitive_low` /
   `general_balancing_low`, add beside `*_new_$S2` and `*_new_$S3`
   ```yaml
   - id: cl_new_long2_$S           # priority 26; 3-level twin: cl_new_long3_$S, priority 27
     call: 2$S
     when: { unbid_suit: $S, cheapest_in_suit: true }
     requires:
       suits: { $S: [6, 13] }
       evals: { total_points: [8, 40], "suit_quality($S)": [1, 9] }   # 3-level: [11, 40]
     shows: "natural $S at the cheapest level: a SIX-card suit, 8+ points"
   ```
   Verified after: B214 → **2NT**, B180 → **3D**, B969 → **2S**, B940 → **2S**.
   B652 still passes (9 tp vs the 11 floor) — deliberately left.
**Endangers:** more 2- and 3-level competition on six-card suits. The
quality floor drops from 1.5 to 1.0 only on the *six-card* rung, so
`J98654` (0.5) is still silent. Watch doubled partscores.

### 1b. NOTHING-WRONG — the rest of the cluster
Boards 492, 79, 872, 656, 863, 305, 757, 494, 499 are a defensive long tail:
11-count balanced hands with four of their trumps in the balancing seat, 4th
seat rule-of-15 passes, and 10-count 5-4-3-1s that fail rule-of-20 by one.
These are the opening-style / balancing knobs DECISIONS.md records as
measured-neutral. Leave them.

### 1c. (mis-attributed) B217 is a checkback board — see Fix list #1.
The dossier tags table A; table A is two 7-counts defending, nothing to do.
The engine defect is at table B: `1C-1S-1NT-P` with `JT732.KJ83.J.A82`,
2NT 0.8 / 2S 0.349 / 2H 0.349 → **P**; 4S was cold.

---------------------------------------------------------------------------
## CLUSTER 2 — `uc_nt3`, 16 boards, 102 IMPs — SPLITS (mostly MISSING-AGREEMENT)

`uc_nt3` (3NT, 13-19, semi-balanced, priority 29) is the generic catch-all
that eats every hole in an authored NT-rebid ladder. The boards are three
different holes:

### 2a. MISSING CONTEXT: `1H - P - 1S - P - 1NT - P - ?` (B501, -12)
`responder_rebid_after_1NT_rebid` expands only `m: [C,D]`, so the very common
major-major version has **no context at all**. Reproduced: N
`AKJ64.Q6.A84.T72` (14 HCP, 5 spades) → **3NT** (`uc_nt3`); BEN checked back
and made 4S. **Fix:** author the twin context (rules given in Fix list #1).
Verified after: → **3S** (GF), opener answers **4S**.

### 2b. MISSING AGREEMENT: no checkback anywhere (B970, -11)
`grep -i checkback|new.minor` over the YAML returns nothing. B970 N
`KQ765.K62.3.A974` after `1C-1S-1NT` → **2NT** then 3NT; opener holds
`A94.…` with three spades. **Fix:** Fix list #1.

### 2c. INTERIOR BAND GAP at the top of the 1S rebid (B766, -12)
E `AKJ2.J2.97.AKQ96` (19 HCP, 4=2=2=5) after `1C-P-1H-P`: `ob_1C1H_1S` reads
`10-17` → fit **0.8**; `ob_2NT` needs `balanced: true` (this is 4-2-2-5);
`ob_rebid_3C` needs six clubs. Nothing fits, so `uc_nt3` fires 3NT at fit
1.00 with `97` in diamonds. **Fix:** widen `ob_1C1H_1S` (and the `1D-1H-1S`
twin) to `hcp: [10, 19]`, or author the 19+ jump-shift `2S`. This is the
lint's "interior strength-band gap" species escaping because the gap is
across *rules of different calls*, not inside one call's ladder.
**Endangers:** nothing — 1S is not forcing and a 19-count must show a suit.

### 2d. MISSING CONTEXT: advancing a BALANCING double of a weak two (B10, -9)
`advance_weak2_double_H` is patterned `2H - X - P - ?`; the auction
`2H - P - P - X - P - ?` matches nothing, so `uc_nt3` bid 3NT holding
`K2.K974.QJ9.AJ63` — **four of their trumps and 14 HCP**, the textbook
convert-for-penalty. 3NT went for six tricks. **Fix:** add contexts
`2$W - P - P - X - P - ?` (expand W: D,H,S) cloning
`advance_weak2_double_$W`, and give them a top rule
`aw2bal_sit_$W`: `call: P, priority: 66, requires: {suits: {$W: [4,13]}, hcp: [8,40]}`
("converting the balancing double with four trumps"). Also add the same
`sit` rule to the existing direct `advance_weak2_double_*` contexts.
**Endangers:** passing a takeout double for penalty is right with four
trumps and wrong with three — the gate is length, keep it at 4.

---------------------------------------------------------------------------
## CLUSTERS 3 & 4 — `uc_raise_S4` / `uc_raise_H4`, 19 boards, 127 IMPs — SPLIT

### 3a. IMPLEMENTATION-BUG (T2): after partner's game raise the seat is DEAD
B778 S `AQJ42.85.A.AQJ92` (18 HCP, 5-5) after `1S X XX P 2C P 4S P`:
`choose_bid` returns **P (`fallback`) with an EMPTY alternatives list** —
literally zero candidates. Same for B395 N `AKJ32..AQ76.A987` (18 HCP, heart
void) after `…2D P 4S P`, and B358 N `A6..AQ974.AKQT74` after partner's 4H
(with a **void in hearts**). Both tables' opponents bid the slam.

**Fix (verified):** a new pattern-anchored context that does not go through
`we_hold_contract`:
```yaml
- id: slam_try_over_game_raise
  description: "Partner raised my major to game: the keycard ask must still exist"
  expand: { M: [H, S] }
  pattern: "... - 4$M - P - ?"
  rules:
    - id: gr_rkc_$M
      call: 4NT
      priority: 46
      when: { partner_last_suit: $M, my_suit: $M }
      requires:
        suits: { $M: [5, 13] }
        evals: { total_points: [17, 40], controls: [5, 12], rule_of_26_sharp: [30, 99] }
        any_of:
          - evals: { "void(any)": [0, 0] }
          - evals: { "keycards($M)": [3, 5] }
      shows: "RKC 1430 for $M: slam values opposite partner's raise to game"
      establishes: { forcing: one_round, agreed_suit: $M, asking: keycards }
      alertable: true
      convention: rkc_1430
```
(`my_suit`/`partner_last_suit` must sit on the RULE's `when:` — `ContextWhen`
only accepts agreed_suit/game_forced/asking/we_hold_contract.)
Verified: B778 → **4NT**, B395 → **4NT**, B870's minimum opener
`KQ9864..J84.AJ53` correctly still **P**, B919's 7-card fit correctly still
**P**. Also closes the fuzzer's standing `responder_after_1m1M_game_raise`
complaint for the general case. **Endangers:** 4NT over partner's game raise
is now possible with 17+ and 5 controls — the `suits: [5,13]` gate keeps it to
the hand that OWNS the suit, and 5S/5H replies are already passable.

### 3b. IMPLEMENTATION-BUG (priority): `uc_raise_$M4` shadows a fit-1.0 suit bid
B395 S `954.AQ9543.K.QT3` after `1S-1NT-2D`: **2H fits 1.00** (`uc_new_H2`,
priority 26) but `uc_raise_S4` (priority 32) fires **4S** on three small
trumps, killing the auction with a six-card heart suit never shown.
**Fix:** in `general_uncontested_continuation`, move `uc_raise_$S4` below the
descriptive calls — priority 24 (under `uc_new_$S1/2/3` at 25/26/27) — or
gate it `not: {evals: {longest_suit_length: [6,13]}}` when the long suit is
unbid. The cheaper of the two: renumber. Precedent: DECISIONS.md's
"wide game raises were shadowing the slam rules by priority" round.
**Endangers:** slower auctions to 4M; the 3-level raise and the specific
contexts still carry the game raises.

### 3c. NOTHING-WRONG / thin-game
B364 (12 HCP with 7 solid hearts opposite a limit+ cue → 4H), B487 (14
opposite a balancing 2H → 4H), B953, B780, B159. Judgment; DECISIONS.md
records the `uc_raise` thin-game dribble as measured-neutral. Leave.

---------------------------------------------------------------------------
## CLUSTER 5 — `fallback`, 6 boards, 61 IMPs — IMPLEMENTATION-BUG (T1)

Every board is the unconstrained backstop out-scoring a real candidate:

* **B707 (-17)** `1S-2D-2S-3D-3S-4D-?`, N `QJT9876.AK9.4.93`. `uc_rebid_S4`
  fits **0.8** (14-point floor); pass is forbidden; the backstop's **4H**
  fits 1.00 → 4HX-5. The right call, 4S, was on the list at 0.8.
* **B188 (-13)** S `QJT7.9.T98.KQT75` in a 2C game force: every candidate
  0.00, backstop bids **4H on a singleton**, which is then read as a heart
  agreement and drives 6HX.
* **B730 (-12) / B651 (-6)** the doubler answering partner's responsive /
  balancing double at the four level: `general_pull_or_sit`'s whole
  `adx_pull_*` family is gated `i_have_acted: false`, and its levels stop at
  4, so `2H X 4H X P ?` offers **exactly three candidates**: `adx_sit`,
  `adx_pass_min` and the backstop. It bid **4S on three small** instead of 5C.
* **B635 (-18)** `gst_rkc_C` asked keycards for clubs on partner's *opening*
  1C (never rebid), then the 5C reply had no minor continuation and the
  backstop bid **5D**, passed out for six tricks.

**Fixes:**
1. *(engine, decision.py — the general insurance)* demote the unconstrained
   backstop so it can never beat a real candidate. In `score_candidates`:
   ```python
   if cand.is_fallback and cand.priority <= 1.0 and not _is_discriminating(cand):
       score *= 0.35     # "forced continuation (undiscussed)" is a last resort,
                         # not a fit-1.00 winner (boards 707, 188)
   ```
   With this, B707 picks 4S (0.63 > 0.35·0.703).
2. *(data)* add the missing five-level rungs to `general_competitive_high`
   (`ch_new_$S5` 6+/14+, `ch_rebid_$S5` 6+/14+ with rule_of_26) — the context
   currently has **no 5-level rule of any kind**, so once they reach 4S our
   side is mute (see also B105 below).
3. *(data)* add an `axr_*` family to `general_pull_or_sit`: the `adx_pull_*`
   ladder cloned with `i_have_acted: true`, no `total_points` cap (the bid is
   forced), and levels 2-5. This is the "advance ladder for every live
   takeout double" species for the *doubler answering a responsive double*.
4. *(data)* `gst_rkc_C` / `gst_rkc_D`: require partner to have actually shown
   the minor — add `when: {partner_last_suit: $m}` (already there) **plus**
   `requires: {suits: {$m: [5,13]}}` or a `lott_total_trumps($m): [9,26]`
   floor. Asking for keycards in a suit that may be three cards long is what
   produced B635.
**Endangers:** (1) is the only engine change I propose and it is one line;
it can only ever move a decision *away* from an undiscussed call, but re-run
the fixed corpus because some of those undiscussed calls will have been
lucky.

---------------------------------------------------------------------------
## CLUSTER 6 — `rkc5C_slam`, 3 boards, 41 IMPs — NEEDS-EXCEPTION

The 1430 arithmetic in `rkc5C_slam` is **correct** ("3+ in hand and partner
shows 1-or-4 ⇒ at most one missing"). What is missing is a TRUMP FIT gate.

* **B919 (-17)** S `A432.AK75.AJ65.Q` asks with **four** spades opposite N's
  `Q85` — a **seven-card trump suit** at the six level. `rkc_4NT` (the
  `rkc_ask` context) has `total_points / controls / rule_of_26` and **no
  `lott_total_trumps` gate at all**, while its sibling `gst_rkc_*` has one
  (`[8,26]`). That is the lint's "family member missing a sibling's gate"
  species escaping across contexts.
* B534 (9 trumps, 29 HCP) and B58 (8 trumps, **25 HCP**) are the values half.

**Fix:** add to `rkc_4NT`
```yaml
evals: { total_points: [17, 40], controls: [4, 12], rule_of_26: [31, 99],
         "lott_total_trumps(agreed)": [8, 26] }
```
Verified: B919 now passes 4S. For B58's 25-HCP slam, additionally gate the
slam-bidding step: `rkc5C_slam` (and `rkc5D_slam`) add
`evals: { rule_of_26_sharp: [31, 99] }`.
**Endangers:** the lott gate uses partner's *shown* length, so a 4NT ask over
a raise that showed nothing may now be blocked — re-check the slam count.

---------------------------------------------------------------------------
## CLUSTER 7 — `qr3_4NT_quant`, 3 boards, 35 IMPs — SPLITS

### 7a. NEEDS-EXCEPTION: the quantitative NT raises have no shape gate (B379)
`qr3_4NT_quant` requires only `hcp >= 15` and `rule_of_26_sharp >= 30`.
B379 S `A.KT3.J4.AKQ7642` — 17 HCP, **seven clubs, singleton spade** — raised
partner's 3NT to a quantitative 4NT and played it for down one where 3NT was
making. The same rule family produced worst-single **B852 (-14)**: `qr3_6NT`
bid 6NT holding `K83..KQ83.AKJT96`, a **void**, for nine tricks.
**Fix:** add `semi_balanced: [1, 1]` to the `evals` of both `qr3_4NT_quant`
and `qr3_6NT`. Verified: B379 → **P** (matches BEN's +400), B852 → **P**
(matches the other table's 3NT). **Endangers:** 6-3-2-2 quantitative raises
survive (semi_balanced covers 6322); genuine 5-4-2-2 slam invites survive.

### 7b. NOTHING-WRONG / known pocket
B153 (15 opposite 14 declining a quantitative 4NT — correct on points; the
6NT was lucky) and B763 (the miss is a **minor-suit** slam, 6C, which
DECISIONS.md already lists as an open pocket: "minor-agreed cue bids — the
cue contexts cover majors only"). No new recommendation.

---------------------------------------------------------------------------
## CLUSTER 8 — `ch_nt3`, 3 boards, 33 IMPs — IMPLEMENTATION-BUG

**This is the un-swept half of a fix DECISIONS.md explicitly deferred**
("`stoppers(their)` still reads only their first suit everywhere except the
two generic notrump rules now gated on `weakest_their_stopper`; sweeping the
remaining uses is safe-looking but unmeasured, so it was left alone").

B956 (-11) reproduces it exactly. S `KQ83.AJT9.32.A75`, auction
`P 1D X 1S 2C X 3C P P 3D`, their suits `['S','D']`:
```
weakest_their_stopper = 0.0      # 32 in their bid-and-rebid diamonds
ch_nt3 constraint fit = 1.00     # because ch_nt3 still gates on
                                 # stoppers(their) + features:[stopper(their)]
```
3NT, five tricks. `ch_nt1/2/3` (general_competitive_high) and
`balhigh_nt1/2/3` (general_balancing_high) are the six rules still on the old
evaluator — the two contexts where a two-suited opposition is most likely.

**Fix (verified):** in all six rules replace
`evals: { "stoppers(their)": [1, 1], … }` + `features: [ "stopper(their)" ]`
with `evals: { weakest_their_stopper: [0.9, 9], … }`.
After: B956 → **P** (3NT drops to 0.789). Lint/fuzz clean.
**Endangers:** fewer competitive 3NTs; this is exactly the change that was
measured as a gain for the two low-level twins, so expect the same sign.

B345 and B368 are only partly this: on B345 (W `K73.K9876.Q8.KQ9`) the spade
stopper is real and the miss is *preferring 3NT to 4H with a five-card
major*. If Fix list #1 lands, consider also giving `ch_nt3`/`uc_nt3`
`not: {evals: {longest_suit_length: [6,13]}}` — I did **not** test that and
do not recommend it blind.

---------------------------------------------------------------------------
## CLUSTER 9 — `open_1D`, 5 boards, 29 IMPs — INTERIOR BAND GAP (T4)

The cluster label is a red herring: these are boards where our *only* call
was the opening bid, because the reopening toolkit has a hole at 16-20.

* **B1 (-4)** W `AQ82.Q7.KQJT72.A` (17 HCP, six diamonds) after `1D 2C P P`
  → **P**. `ballow_rebid_D2` reads `total_points: [11,15]` → fit **0.004**;
  `ballow_rebid_D3` is gated `cheapest_in_suit` (2D is cheaper) so it is
  never offered; `ballow_reopen_X` is gated `longest_suit_length: [0,5]`
  → 0.349. **A 17-count with a six-card suit has no legal call.**
* **B376 (-11)** E `AT83.AK.AK873.Q9` (19 HCP) after `1D 2S P P` → **P**;
  3NT 0.64 (rule_of_26 24 unreachable opposite a silent partner), 3D 0.349
  (five diamonds vs the 6+ rung), X 0.015 (four spades).
* **B5 (-5)** W `A42.J.AKQT75.A72` (17 HCP, six diamonds) over `1D 2H P 3H`
  → **P**; 4D 0.028, blocked by `rule_of_26: [26,99]` with partner at floor 0.
* **B327 (-8)** is a different bug — see Fix list #7.

**Fixes (verified):**
1. `cl_rebid_$S2` / `ballow_rebid_$S2` / `ch_rebid_$S2` (16 rules):
   `total_points: [11, 15]` → `[11, 40]`. The cheapest rebid of my own
   six-card suit is right with any strength when nothing better exists.
   Verified: B1 → **2D**; a minimum `J82.Q7.KQJT72.A5` still bids 2D, and a
   sub-minimum still passes.
2. New rule in `general_balancing_low`, twin of `ballow_nt2_balance` for the
   case where OUR side opened:
   ```yaml
   - id: ballow_nt2_strong
     call: 2NT
     priority: 30
     when: { side_has_acted: true, their_last_bid_suit: true, standing_bid_level: [2] }
     requires:
       hcp: [17, 21]
       evals: { weakest_their_stopper: [0.9, 9], semi_balanced: [1, 1] }
     shows: "natural 2NT: 17-21 balanced with their suit stopped, partner still unlimited"
   ```
   Verified: B376 → **2NT**.
3. *(lower confidence, untested)* the T4 root: on **competitive** rebids
   replace the bare `rule_of_26` gate with
   `any_of: [ {evals: {rule_of_26: [N,99]}}, {evals: {total_points: [16,40]}} ]`.
   That is what B5 needs. I would land 1 and 2 first and re-measure.
**Endangers:** (1) means we reopen more often at the two level with big
hands. The `cheapest_in_suit` gate keeps it to one call.

---------------------------------------------------------------------------
## CLUSTER 10 — `uc_nt2`, 7 boards, 27 IMPs — SPLITS (small)

### 10a. INTERIOR GAP in the raise ladder (B78, -6)
E `76.KJ832.AJ76.Q8` (12 HCP, four-card support) after `1D-1H-2C`:
`uc_raise_D2` reads `[6,9]`, `uc_raise_D3` is blocked by
`lott_total_trumps(D) >= 8` (4 + partner's shown 3 = 7). **10-13 with a
known seven-card fit has no raise**, so `uc_nt2` bids 2NT with `76` in
spades. **Fix (verified):** widen the cheapest raise
`uc_raise_$S2: total_points [6, 9] → [6, 13]`. The 3-level rung outranks it
(31 > 30) whenever the LOTT gate is met, so this only fires where the
3-level is blocked. Verified: B78 → **2D**. **Endangers:** nothing visible;
the cheapest raise is the natural catch-all preference.

### 10b. NOTHING-WRONG / judgment (B878, B926, B818, B250, B456)
`uc_nt2` invites 2NT over partner's own limited call with 11-12 (a 4-3 fit
after a 10-12 jump advance; a 2S overcall of their 15-17 1NT). Each is a
1-8 IMP judgment call and the combined-values arithmetic is honest
(`rule_of_26 >= 21`). If you want to touch it, raise that floor to 23 — but
that is a knob, and DECISIONS.md warns against tuning this family.

---------------------------------------------------------------------------
## WORST SINGLE BOARDS 1-15

**B358 (-17) — IMPLEMENTATION-BUG (T2).** N `A6..AQ974.AKQT74` passes
partner's 4H holding a **void in hearts**: zero candidates after the game
raise. Fix list #2.

**B847 (-17) — MISSING-AGREEMENT.** `2C-2D-2NT-3D-3H-?` with
`942.K6543.KQ63.K` (8 HCP opposite 22-24 = 30-32 with a 5-4 fit). The
context `r2c_after_transfer_completed` offers only `4$M` and `3NT`;
everything else scores ≤0.015. **Fix:** add a slam rung there —
`r2c_tr_4NT` (call 4NT quantitative, `hcp: [8,40]`, priority above
`r2c_tr_4M`) and/or `r2c_tr_cue` — mirroring `quant_raise_of_3NT`.
7H was cold; expect partial recovery.

**B680 (-16) — MISSING-AGREEMENT.** After our 1NT overcall and partner's
natural 2H advance, W `AKQ86.KQ.T83.AJ8` **pulled to 2S** via the generic
`uc_new_S2` (priority 26 > `uc_pass` 18) because `advance_1NT_overcall` has
no opener-side follow-up context. N doubled and `xd_XX_extras` **redoubled**:
2SXX, five tricks, -1000. **Fix:** author `1NT-overcaller over the advance`
(`… - 1NT - P - 2$x - P - ?`): pass with a minimum, raise with a fit, 2NT/3NT
with extras — and never a new suit below the advance's level. Cheap
insurance meanwhile: `xd_XX_extras` should deny a doubleton in the doubled
strain (`not: {evals: {"suit_length(standing)": [0,2]}}`) — redoubling a
penalty double of a 5-2 fit is never right.

**B105 (-15) — MISSING-AGREEMENT.** E `4.T942.T.AKQJ754` over their 4S,
holding **AKQJ754** and having opened 1C with partner's double standing:
only candidate is a penalty X at 0.00 → **P**. `general_competitive_high`
has **no five-level rules at all**. Fix list #5 (`ch_new_$S5`/`ch_rebid_$S5`).
With the rung added, 5C reaches 0.107 — still blocked by
`rule_of_26: [26,99]`, so this board also needs the T4 relief, or a length
branch: `any_of: [ {evals: {rule_of_26: [26,99]}}, {suits: {$S: [7,13]}, evals: {total_points: [12,40]}} ]`.

**B7 (-14) — IMPLEMENTATION-BUG (priority/band).** E `A65.KQT9.AKQ965.`
(20 HCP) over the Jacoby shortness reply: **4NT, 3S, 4C and 4D all fit
1.00**, and `jac_wasted_signoff` (priority 47, `requires:
wasted_in_partner_shortness >= 4`) beat all of them with **4H**. The
duplication shutdown has no upper cap, so a 20-count signs off. **Fix
(verified):** `requires: { evals: { wasted_in_partner_shortness: [4, 40],
total_points: [0, 18] } }`. After: → **4NT**. **Endangers:** 19+ hands with
genuinely wasted paper now cue/ask; the cue chain's own denials handle it.

**B498 (-14) — NEEDS-EXCEPTION.** N `K3.AK763.A6.AKQT` (22 HCP) over
responder's 3H preference: the cue bids `cue_H_C`/`cue_H_D` fit **0.8** and
`rkc_4NT` **0.028**, both blocked by `rule_of_26(_sharp)` — because after a
2C opening and a **waiting 2D**, responder's floor is ~3 and the combined
arithmetic under-counts by ten. `cue_H_signoff` (4H, `requires: {}`) wins.
7H was cold. **Fix:** in `cue_bidding_H`/`cue_bidding_S` and `rkc_4NT`,
make the partnership gate a disjunction with an own-hand gate:
```yaml
all_of:
  - any_of: [ {evals: {rule_of_26: [28, 99]}}, {evals: {total_points: [21, 40]}} ]
```
(`rkc_4NT`: 31 / 22). A hand with 21+ of its own is in slam range whatever
partner has shown. **Endangers:** more cue chains from 21-counts; the cue is
one-round forcing and `cue_*_signoff` still ends them.

**B852 (-14) — NEEDS-EXCEPTION.** `qr3_6NT` with a void. Cluster 7a fix,
verified.

**B913 (-14) — MISSING-AGREEMENT.** W `QT.AK9854.A.AK98` (19 HCP, six
hearts) after `1D-1H-1NT`: the context tops out at `rr_nt_4$M` (13-18) and
`rr_nt_4NT` (17-18, semi-balanced), so 19+ with a six-card major has no
rung and `rr_nt_4H` fits softly and wins. Fix list #1's `rr_nt_slam3_$M`
gets W to **3H** (verified); reaching 7H additionally needs the opener's
answer context to route into RKC.

**B158 (-13) — MISSING-AGREEMENT (known pocket).** `2NT-3C-3D-?` with
`8654.K.AK8754.J3` (10 HCP, six diamonds opposite 20-21): every alternative
≤0.023, so `nt2_stm_3NT`. This is the "minor-suit slam machinery over strong
NT openings" pocket DECISIONS.md already names, in its 2NT form. **Fix:**
add to `nt2_stayman_placement` a `4$m` natural slam try
(`suits: {$m: [6,13]}, hcp: [8,40]`) and a `4NT` quantitative.

**B188 (-13) — IMPLEMENTATION-BUG (T1) + downstream.** The backstop bid 4H
on a singleton (see Cluster 5); the 6-1 "fit" then satisfied every keycard
gate. Fix list #4 (backstop demotion) is the root; the `lott` gate added to
`rkc_4NT` does **not** catch this one, because partner's 4H bid credits three
hearts to the model.

**B445 (-13) — NEEDS-EXCEPTION (slam machinery, low confidence).** I first
read this as a bad 1NT opening; it is not — N `AK85.QT7.A5.AJ97` is **18**
HCP, so `open_1NT` correctly scores 0.8 and 1C-then-2NT (`ob_2NT`, 18-19) is
the right auction. The loss is downstream: after `1C-1H-2NT-3H`, `o2ntj_4H`
signs off in game with 18 opposite a 3H that showed 5+ hearts and
invitational-plus — 29 combined with a 5-3 fit, and 6H made. **Fix:** give
`opener_over_2NT_jump`-family (`o2ntj_*`) a slam rung the way
`opener_after_limit_raise` was capped — `o2ntj_4$M` add
`not: {evals: {total_points: [18,40]}}`, and author `o2ntj_4NT` (RKC, 3+
support, 18+, controls 5+). Untested; land fix-list items 2 and 9 first,
since both feed the same arithmetic.

**B493 (-13) — NOTHING-WRONG.** `1H-3H-4NT-5H` (two keycards, no trump
queen) and `rkc5H_pass_signoff` stops in 5H. Four of five keycards but the
trump queen missing on a 4-4-…-9-card fit with 28 combined: signing off is
the percentage action. BEN's 6H made. Variance.

**B682 (-13) — NEEDS-EXCEPTION (small).** W `KT82.K864.AKJ.KQ` (19, 4-4-3-2)
raised partner's forced 3S advance of a takeout double of 3C to **4S**
(`uc_doubler_game_S`, `total_points >= 20`, W has exactly 20) for down two,
where 3NT (which BEN played, making) scored **0.134** — blocked by
`rule_of_26` again (T4). **Fix:** give the doubler's game raise a shape gate
— `not: {evals: {semi_balanced: [1,1]}}` or require five trumps — so a
4-4-3-2 19-count offers 3NT instead. Low confidence, low value; land the
T4 relief first and re-check.

**B772 (-13) — NOTHING-WRONG.** EW hold a 5-5 diamond fit that only a
two-suited overcall would find, and "no Michaels/unusual NT" is a documented
scope decision (`system.defense_notes`). W's 3H on the six-bagger was
reasonable. Reopening the two-suited scope is a bigger decision than this
board justifies.

**B119 (-12) — MISSING-AGREEMENT (known pocket).** S `Q2.AQ5.A.8765432`
(10 HCP, **seven clubs**) raised 1NT to 3NT via `nt_3NT` (`hcp: [10,15]`,
"no 4-card major" — no shape gate). `resp_1NT` has no minor transfer and no
3C/3D natural slam try; 6C was cold. This is exactly the "~7 missed slams
per 1000" pocket in DECISIONS.md. **Fix (minimum viable):** add
`not: {any_of: [{suits: {C: [6,13]}}, {suits: {D: [6,13]}}]}` to `nt_3NT`
and author `nt_3C_natural` / `nt_3D_natural` (6+ minor, 9-14, forcing) with
an opener's-answer context. **Endangers:** 3NT on a running seven-card minor
is sometimes right — keep the denial at 6+, not 5+.

---------------------------------------------------------------------------
# FIX LIST (deduplicated, priority order)

Estimated recoverable IMPs are for **my slice only** and assume the paired
re-run confirms sign; as always, land, measure, keep what pays.

**1. The 1NT-rebid checkback family** — MISSING-AGREEMENT; boards 217, 501,
970, 650, 913 (+ cluster 11: 654, 328, 267). **~86 IMPs.** Reverses the
"checkback is scoped out" decision, and completes EXPERT_REVIEW_919191's
board-76 fix, which was written up and never implemented.
   * In `responder_rebid_after_1NT_rebid` (`1$m - P - 1$M - P - 1NT - P - ?`):
     ```yaml
     - id: rr_nt_second_$oM      # 2$oM, priority 51.5
       requires: { suits: { $oM: [4,13], $M: [5,13] }, hcp: [6,11] }
       shows: "5-4: the second suit, to play"
     - id: rr_nt_gf3_$M          # 3$M, priority 53.5
       requires: { suits: { $M: [5,13] }, hcp: [12,18] }
       establishes: { forcing: game_forcing }
     - id: rr_nt_slam3_$M        # 3$M, priority 56
       requires: { suits: { $M: [5,13] }, hcp: [19,40] }
       establishes: { forcing: game_forcing }
     ```
     and tighten `rr_nt_3NT`'s denial from `{$M: [6,13]}` to `{$M: [5,13]}`
     (otherwise 3NT at priority 54 keeps winning).
   * New context `responder_rebid_after_1H_1S_1NT`, pattern
     `1H - P - 1S - P - 1NT - P - ?`, with the same ladder plus a heart
     preference rung (`2H` 6-10 / `3H` 11-12 / `4H` 13-18 with 3+ hearts).
   * **Required companion (the board-69 trap):** an opener's-answer context
     `1$m - P - 1$M - P - 1NT - P - 3$M - P - ?`:
     `4$M` (3+ support, priority 60), `3NT` (doubleton, 58),
     `4NT` (3+ support and 14+, RKC). Without it the reply falls to the
     generic toolkit and lands on things like 4D (verified on B328).
   * Verified after: B501→3S→4S, B970→3S→4S, B654→3H→4H, B328→3H,
     B217→2H, B913→3H, B650→3S; a flat 14 with no five-card major still
     bids 3NT.
   * **Endangers:** three-level game forces where 3NT was making. The 12-HCP
     floor on `rr_nt_gf3_$M` is the risk knob.

**2. Slam try over partner's game raise** — IMPLEMENTATION-BUG (T2); boards
778, 395, 358, plus the fuzzer's standing complaint. **~46 IMPs.**
New context `slam_try_over_game_raise` exactly as printed in Cluster 3a.
**Endangers:** 4NT over partner's game raise; gated to the hand holding the
five-card suit with 17+ and 5 controls, and verified silent on a minimum.

**3. Sweep `stoppers(their)` → `weakest_their_stopper`** —
IMPLEMENTATION-BUG; boards 956, 368 (+ every future two-suited 3NT).
**~20 IMPs.** Six rules: `ch_nt1/2/3`, `balhigh_nt1/2/3`. Delete the
`features: [ "stopper(their)" ]` lines with them. This is the sweep
DECISIONS.md deferred as "safe-looking but unmeasured"; board 956 is the
measurement. **Endangers:** fewer competitive 3NTs (same sign as the
already-measured low-level twins).

**4. Demote the unconstrained forced-continuation backstop** —
IMPLEMENTATION-BUG (T1); boards 707, 188, 730, 651. **~48 IMPs.**
One line in `engine/decision.py::score_candidates` (Cluster 5, fix 1), plus
the two data companions: `ch_new_$S5`/`ch_rebid_$S5` in
`general_competitive_high`, and the `axr_*` (`i_have_acted: true`,
levels 2-5, no point cap) clone of `adx_pull_*` in `general_pull_or_sit`.
**Endangers:** the engine now prefers a 0.8-fitting real bid to an invented
one — this can only reduce undiscussed calls, but some of them were lucky.

**5. The direct 4th seat over (1x) P (2x) + the six-card shape rung** —
MISSING-AGREEMENT; cluster 1a, boards 214, 180, 969, 940 (+ tail).
**~30 IMPs.** `cl_nt2_direct` (2NT 16-21, priority 37), the `cl_takeout_X`
`any_of` (three of their suit at 17+), and `*_new_long2_$S`/`*_new_long3_$S`
(six cards, 8/11 points, quality floor 1.0) in `general_competitive_low` and
`general_balancing_low`. All four boards verified. **Endangers:** more
2-/3-level competition; watch doubled partscores.

**6. Reopening/competitive rebid of my own six-card suit is capped at 15** —
INTERIOR BAND GAP; boards 1, 376. **~15 IMPs.** `*_rebid_$S2`
`total_points: [11,15] → [11,40]` (16 rules) and the new `ballow_nt2_strong`
(2NT 17-21, priority 30). Both verified.

**7. Two mis-set bands, both verified:**
   * `jac_wasted_signoff` add `total_points: [0,18]` — board 7, **14 IMPs**.
   * `qr3_4NT_quant` and `qr3_6NT` add `semi_balanced: [1,1]` — boards 379,
     852, **24 IMPs**.
   * `uc_raise_$S2` `total_points: [6,9] → [6,13]` — board 78 and the
     10-13-with-a-seven-card-fit gap generally, **~6 IMPs**.
   * `ob_1C1H_1S` (and the `1D-1H` twin) `hcp: [10,17] → [10,19]` — board
     766, **12 IMPs** (untested end-to-end; the 0.8 fit is confirmed).

**8. `rkc_4NT` is missing its sibling's trump-fit gate** — NEEDS-EXCEPTION;
cluster 6, boards 919, 534, 58. **~30 IMPs at risk, expect partial.** Add
`"lott_total_trumps(agreed)": [8, 26]` to `rkc_4NT` (verified: B919 stops in
4S) and, if the values half is to be closed too, `rule_of_26_sharp: [31,99]`
to `rkc5C_slam`/`rkc5D_slam`.

**9. Own-hand disjunction on the slam gates** — NEEDS-EXCEPTION; boards 498,
plus every 2C-then-waiting-2D auction. **~14 IMPs.** In `cue_bidding_H/S`
and `rkc_4NT`, replace the bare `rule_of_26` gate with
`any_of: [ {rule_of_26: [N,99]}, {total_points: [21,40]} ]` (22 for RKC).
Untested; land after 2 and 8 so the interactions are visible.

**10. Advancing a BALANCING double of a weak two; converting with four
trumps** — MISSING-AGREEMENT; board 10 (+ tail). **~9 IMPs.** New contexts
`2$W - P - P - X - P - ?` cloning `advance_weak2_double_$W`, and an
`aw2*_sit` pass rule (4+ of their suit, 8+ HCP, priority above the pulls)
added to both the balancing and the direct versions.

**11. Small, individually argued** (see the board entries): the 1NT
overcaller's follow-up context + the `xd_XX_extras` doubleton denial (B680,
16); `r2c_tr_4NT` after a completed 2C transfer (B847, 17); minor-suit slam
tries over 1NT/2NT (B119, B158, B763 — the pocket DECISIONS.md already
names, ~36 IMPs across three boards); `r1m_1$M` responding on 5 HCP with a
five-card major and a singleton (B327, 8 IMPs — verified: add
`- hcp: [5,40], suits: {$M: [5,13]}, evals: {singleton_or_void: [1,1]}` to
the `any_of`; a flat five-count still passes); `uc_raise_$M4` priority below
the descriptive `uc_new_*` rungs (B395).

## What I did NOT recommend, and why
* Opening-style / rule-of-20 / thin-game thresholds (boards 79, 656, 863,
  305, 494, 487, 364) — DECISIONS.md records these as repeatedly neutral.
* Michaels / unusual NT (B772) and minor-suit transfers as a *convention*
  addition — documented scope decisions; the minor-suit **slam try** in
  fix 11 is the narrow version that does not widen the convention card.
* Board 493, 153 — genuinely correct decisions that lost to the cards.
