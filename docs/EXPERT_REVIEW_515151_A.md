# Expert verdicts — seed 515151, clusters 1-10 + worst singles 1-15
Reviewer E4 (external, 2/1 GF). Every indictment below was reproduced with
`choose_bid(..., use_arbitration=False)`; every prescribed fix was prototyped in
a scratch copy of the YAML and re-verified. Prototype diff:
`/tmp/claude-0/.../scratchpad/final.diff` (338 added / 59 removed lines).

**Verification of the whole prescribed patch set**
- `pytest tests/` — 639 passed (baseline 639).
- `tools/lint_system.py` — collide 0, gap 0, soft 0 (unchanged); floor 194 -> 200,
  all six new findings being the "`... - ?` overlay context offers no pass" class
  that every existing `gf_landing_*` / `general_slam_try` context already reports.
- `tools/fuzz_decisions.py --n 200` — 0 crashes, 0 empty seats, same single
  starved context as baseline (`responder_after_1m1M_game_raise[C,S]`).

---

## 0. The mechanism behind half of this dossier

Three engine facts compose into one failure mode that explains cluster 1, most of
cluster 2, all of cluster 4, cluster 6, cluster 9 and five of the fifteen singles.

1. `fast_decision` picks, among candidates with **fit >= 0.9**, the one with the
   highest **priority** — fit above 0.9 is not a tie-breaker, and hand strength is
   not consulted at all.
2. Every generic toolkit context ends in a catch-all pass with
   `requires: {}` (`ballow_pass`/`balhigh_pass` 21, `uc_pass` 18, `cl_pass`,
   `ch_pass`, `xd_pass` 18). `requires: {}` scores **fit 1.0 for every hand**.
3. Fallback candidates are priority 8-10.

Consequence: **whenever an authored ladder has a hole, the catch-all pass wins by
construction** — not because passing was judged right, but because it is the only
thing that "fits". A 19-count facing a 2C rebid, a 20-count in the balancing seat,
an 18-count over a 1NT response and a 15-count with a self-sufficient 7-card suit
all pass, each with a sane call sitting at fit 0.8-0.4 right underneath.

This is why "all-pass" and "uc_nt3" are correlational labels. The right reading is
**"the seat had no rule"**, and the correct fixes are almost all *missing contexts*,
not changes to the named rule. Two structural notes for the record:

- `v1NT_pass` (hcp [0,14]) and `vw2_pass` (hcp [0,14]) already carry HCP ceilings.
  The general-toolkit passes do not. Putting a ceiling on `ballow_pass` would be a
  blunt systemic backstop; I do **not** recommend it (it would force action in the
  many auctions where our side has already competed). Fix the ladders instead.
- Suit-length constraints written under `suits:` are **soft** (sigma^2 0.95, a
  one-card miss scores 0.35). Any rule that is the last thing standing therefore
  fires on a hand a card short. That is the second half of the cluster-8 story.

Recurring themes across the four prior reviews that recur again here: (a) contexts
that exist only for the 1-level version of an auction (`advance_overcall`,
`opener_over_negative_double`, `responder_after_jump_raise`); (b) `suit_length(their)`
used where the *standing* strain was meant; (c) notrump rules out-prioritising the
natural major at the same height.

---

## CLUSTER 1 — `all-pass`, 36 boards, 210 IMPs
### VERDICT: splits three ways. 1a IMPLEMENTATION-BUG, 1b MISSING-AGREEMENT, 1c MISSING-AGREEMENT.

**1a — IMPLEMENTATION-BUG: the balancing double reads the wrong suit.**
`ballow_X` / `balhigh_X` gate shortness on `evals: { "suit_length(their)": [0, 2] }`.
`suit_length(their)` resolves to the opponents' **first shown suit**, not the strain
they have landed in — the identical trap the `max_their_suit_length` and
`standing_suit_length` docstrings were written to fix elsewhere in this file.

Board 921 (11 IMPs), `1D-P-1H-P-2H-P-P-?`, N `K973.5.Q8.AJ8743`: the balancing double
is gated on N's **diamonds**. Worse, a control hand:

```
K983.J8.KQ925.A9  (14 HCP, doubleton in the suit they are playing)  over 1D-P-1H-P-2H-P-P
  chosen: P    X fit 0.000   <- textbook reopening double scores ZERO
```
after the swap:
```
  chosen: X    (fit 1.000)
```

FIX: in both `ballow_X` and `balhigh_X` replace
`evals: { "suit_length(their)": [0, 2] }` with `evals: { standing_suit_length: [0, 2] }`,
and give `ballow_X` the shortness relaxation `balhigh_reopen_X` already has:
```yaml
        requires:
          any_of:
            - hcp: [11, 40]
              evals: { standing_suit_length: [0, 2] }
            - hcp: [9, 40]
              evals: { standing_suit_length: [0, 1] }
```
Recovers board 921 and, by inspection of the auction families, most of the
`1D P 1H` / `1D P 1S` / `1C P 1D` / `1H P 2C` / `1S P 2C` group (13 of the 36).
ENDANGERS: reopening doubles now fire holding length in a suit they bid *earlier*;
that is correct bridge but will produce more 1-level competition on part-score deals.

**1b — MISSING-AGREEMENT: no balancing notrump above 14.**
`ballow_nt2` (11-12) and `ballow_nt3` (13-19) both carry `when: { side_has_acted: true }`,
which is exactly false in the pure balancing seat. `ballow_nt1` stops at 14. So a
15-21 balanced hand with their suit stopped has **no notrump call at all**, and
`ballow_pass` takes it.

Board 782 (15 IMPs, the cluster's worst), E `AK9.AKJ.Q983.K83` = **20 HCP, AKJ in
their suit**, balancing over 2H-P-P: `chosen: P`, best alternative X at fit 0.349
(AKJ is three cards, so `suit_length(their)` blocks the double too). EW have 6NT.

FIX: add to `general_balancing_low`, immediately above `ballow_nt2`:
```yaml
      - id: ballow_nt2_balance
        call: 2NT
        priority: 33
        when: { their_last_bid_suit: true, side_has_acted: false, standing_bid_level: [2] }
        requires:
          hcp: [15, 21]
          evals: { weakest_their_stopper: [0.9, 9], semi_balanced: [1, 1] }
        shows: "balancing 2NT over their two-level contract: 15-21 balanced, stopped"
        establishes: { forcing: non_forcing }
```
`standing_bid_level: [2]` keeps it to the classic position (over a 1-level bid the
11-14 `ballow_nt1` is the right call and the strong hand doubles). Verified: board
782 now bids 2NT. Covers the `2H P P` (4), `2D P P` (3), `2S P P` (3) families.
ENDANGERS: a 15-count with a singleton somewhere will now bid 2NT where pass was
scoring 0 IMPs; `semi_balanced` is a sharp gate (sigma^2 0.08) so shape is honestly
policed.

**1c — MISSING-AGREEMENT: third seat has no rule-of-20 opening.**
`open_1S_rule20` / `open_1H_rule20` are `when: { opening_seat: [1, 2] }`. The third-seat
substitute demands `suit_quality >= 2.5`, a **higher** bar than the first-seat rule's
1.5. So a hand that opens light in first chair is passed out in third — where partner
is a passed hand and the case for opening is stronger, not weaker.
Board 750 (12 IMPs), N `5.AQ952.J4.AT754`, seat 3, rule of 20 = 21, two aces:
`chosen: P` (1H at fit 0.80). Passed out; the other table made 4H.

FIX: add seat-3 twins capped at seven cards (an eight-bagger must still preempt —
this is the exact regression `tests/data/harvested.yaml::ben_four_level_preempt_on_eight`
guards, and it caught my first attempt):
```yaml
      - id: open_1S_rule20_third      # and open_1H_rule20_third, priority 78
        call: 1S
        priority: 79
        requires:
          suits: { S: [5, 7] }
          hcp: [10, 11]
          evals: { rule_of_20: [20, 33], quick_tricks: [1.5, 12], "suit_diff(S,H)": [0, 13], suit_quality(S): [1.5, 9] }
        when: { opening_seat: [3] }
```
Recovers board 750 and the three passed-out (`''` family) boards.
ENDANGERS: more third-seat 10-11 counts open; DECISIONS records opening-style knobs
as measured-neutral, so treat this as the *consistency* repair it is, not a style bet.

---

## CLUSTER 2 — `uc_nt3`, 18 boards, 112 IMPs
### VERDICT: splits. 2a IMPLEMENTATION-BUG (priority inversion), 2b IMPLEMENTATION-BUG (redundant trump floor), 2c MISSING-AGREEMENT (advancing a non-major overcall / 1NT overcall).

**2a — the notrump ladder out-ranks the natural major at the same height.**
In `general_uncontested_continuation`: `uc_new_*1` 25, `*2` 26, `*3` 27;
`uc_nt1` 27, `uc_nt2` 28, `uc_nt3` 29. Notrump therefore beats a one-level major
for every hand that fits both.
Board 350 (13 IMPs), E `KT.AQ973.97.AJ76` advancing partner's 1D overcall:
`chosen: 3NT` with `1H` sitting at **fit 1.000**. 3NT went for 8 tricks.

FIX: `uc_new_H1` and `uc_new_S1` priority `25 -> 30` (above `uc_nt3`'s 29).
Verified: board 350 now bids 1H. Leave the minors at 25 — with a balanced hand
notrump *should* beat a minor.
ENDANGERS: a 4-card major at the one level now precedes 3NT in every undiscussed
continuation. That is the textbook order; the cost is one extra round of bidding.

**2b — `uc_raise_H4`/`uc_raise_S4` demand three trumps of my own although
`lott_total_trumps` already counts the fit.** The rules carry both
`suits: { M: [3, 13] }` and `lott_total_trumps(M): [8, 26]`. A doubleton opposite a
*shown six-card suit* is an eight-card fit, and the LOTT gate proves it; the own-length
floor merely deletes the game.
Board 126 (12 IMPs), N `K7.AT9.AJT863.QT` after `2S-P-3D-P-3S-P`: 4S at fit 0.349,
`chosen: 3NT` (8 tricks; 4S makes 10).
Board 172 (12 IMPs), E `K53.T6.AQT.AKJ97` after `1NT-P-2D-P-2H-P-3H-P`: 4H at fit 0.349,
`chosen: 3NT` (8 tricks; 4H makes 10).

FIX: in `uc_raise_H4` and `uc_raise_S4` change `suits: { M: [3, 13] }` to
`suits: { M: [2, 13] }`, keeping `lott_total_trumps(M): [8, 26]` (sharp, sigma^2 0.4)
as the real gate. Verified: 126 -> 4S, 172 -> 4H.
ENDANGERS: nothing I can find — the LOTT eval counts partner's *shown minimum*, so a
doubleton can only reach 8 opposite a shown six-bagger.

**2c — no context for advancing a minor-suit or 2-level overcall, and none for
showing a major opposite a 1NT overcall.**
`advance_overcall` is `expand_pairs` over 1-level **major** overcalls only, so
`1C - 1D - P - ?` (board 350) falls to the generic toolkit. `advance_1NT_overcall`
caps every suit bid at `hcp: [0, 7]` and then offers only 2NT (8-9) and 3NT (10-15):
board 140 (12 IMPs), N `AK852.J762.J2.83` — 8 HCP, 5-4 in the majors — has literally
no way to mention spades and bids 2NT; the 5-3 spade game was cold.

FIX (not prototyped, larger authoring job): (i) add `advance_overcall_minor`
(`1$o - 1D - P - ?` and `1$o - 2$m - P - ?`) mirroring `advo_raise` / `advo_cue` /
`advo_1NT`; (ii) add to `advance_1NT_overcall`
`adv1n_3H_$o` / `adv1n_3S_$o` (`suits: { M: [5,13] }, hcp: [8,11]`, invitational) and
`adv1n_4H_$o` / `adv1n_4S_$o` (`suits: { M: [5,13] }, hcp: [12,15]`). 2a alone already
rescues board 350.

---

## CLUSTER 3 — `uc_raise_H4`, 8 boards, 66 IMPs
### VERDICT: splits. 3a IMPLEMENTATION-BUG + MISSING-AGREEMENT (board 599), 3b MISSING-AGREEMENT (956), 3c NOTHING-WRONG-ENOUGH / threshold (337, 46).

**3a — the wrong major, from a tie-break.** Board 599 (13 IMPs),
`P-1H-P-1S-P-3S-P-?`, S `KQ753.J72.A82.A3`. `uc_raise_S4` (4S) and `uc_raise_H4` (4H)
**both** score fit 1.000 at priority 32; `fast_decision`'s final tie-break is
`-call_rank`, i.e. the cheaper bid, so the engine *corrects partner's raise of my
spades back to his hearts*. Par was 2210.

Root cause is a missing context: `responder_after_jump_raise` is
`expand: { m: [C, D], M: [H, S] }` over `1$m - P - 1$M - P - 3$M - P - ?` — the
**major-opening** case `1H - P - 1S - P - 3S - P - ?` is not covered.

FIX: change that context to
```yaml
    expand_pairs:
      - { m: C, M: H }
      - { m: C, M: S }
      - { m: D, M: H }
      - { m: D, M: S }
      - { m: H, M: S }
```
Verified: board 599 now bids 4S. Flag for the maintainers: the underlying hazard —
two same-priority `uc_raise_*4` rules resolving by *cheapness* rather than by fit or
by which suit the auction agreed — will recur wherever partner has shown two suits.

**3b — no context for responder's rebid after `1M - 1NT - 2(second suit)`.**
`responder_preference_after_1M_1NT_2m` covers only the minor second suit. Board 956
(13 IMPs), `1S-P-1NT-P-2H-P-?`, W `J4.Q842.KJT.AT92` blasts 4H via `uc_raise_H4`; the
other table found 6H. FIX: extend that context (or add a twin) for a second **major**,
with the standard ladder — pass / 2S preference / 3H invitational / 4H.

**3c — boards 337 and 46 are threshold cases, and I am not indicting them.**
337: S holds 21 HCP and a spade void opposite a 3H raise; `gst_rkc_H` fails only on
`rule_of_26_sharp` = 30.0 against its `[31, 99]` gate (all other gates pass, keycards 4).
46: the overcaller's 4H is a one-point overbid of `rule_of_26 >= 25`. DECISIONS records
these knobs as repeatedly measured-neutral; leave them.

---

## CLUSTER 4 — `gf_3NT`, 6 boards, 63 IMPs
### VERDICT: MISSING-AGREEMENT (a starved seat), not a defect in `gf_3NT`.

After a 2C opening and a natural suit rebid the auction is game-forced, so the pass is
filtered out — and **no candidate fits at all**. Board 593 (14 IMPs), N
`9865.J9876.KQ.J4` after `2C-P-2D-P-3D-P`: every alternative scores 0.000 and `gf_3NT`
wins on **fit 0.067**. `gf_3NT`'s own honesty gates are working correctly
(`weakest_unshown_stopper` = 0.0, `lott_total_trumps` = 7); it is simply the least-bad
of nothing. Same on 574 (5 hearts), 316 and 229 (5 clubs, 3-4 HCP).

The generic toolkit cannot serve this seat because its new-suit rules carry point
floors (`uc_new_*2` 10+, `uc_new_*3` 14+) that are meaningless opposite a 22-count.

FIX: two small overlay contexts giving the game force a truthful floor.
```yaml
  - id: gf_landing_new_suit
    expand: { X: [C, D, H, S] }
    pattern: "... - P - ?"
    when: { agreed_suit: false, game_forced: true }
    rules:
      - id: gf_new_2$X            # and gf_new_3$X, same body at 3$X
        call: 2$X
        priority: 36
        when: { unbid_suit: $X, cheapest_in_suit: true }
        requires: { suits: { $X: [5, 13] } }
        shows: "five-card suit shown in the game force (no point floor: partner has the values)"
        establishes: { forcing: game_forcing }

  - id: gf_landing_preference_major
    expand: { M: [H, S] }
    pattern: "... - P - ?"
    when: { agreed_suit: false, game_forced: true }
    rules:
      - id: gf_pref_3$M
        call: 3$M
        priority: 37
        when: { partner_last_suit: $M, cheapest_in_suit: true }
        requires: { suits: { $M: [3, 13] } }
        shows: "preference to partner's major in the game force"
        establishes: { forcing: game_forcing, agreed_suit: $M }
```
Verified: 593 -> 3H, 574 -> 3H, 316 -> 3C, 229 -> 3S (all four now bid a suit rather
than a wide-open 3NT). **Keep the preference rule majors-only** — my first version
included minors and broke two regression scenarios
(`fallback::gf_landing_3NT_no_fit`, `harvested::r6_3NT_preferred_to_minor_game_raise`,
whose maxim is "with a minor fit the game is 3NT"). Both pass with the majors-only form.
ENDANGERS: any game force with an unbid five-card suit now shows it before bidding
3NT. That is standard, but it lengthens auctions and exposes more information.

---

## CLUSTER 5 — `uc_raise_S4`, 6 boards, 47 IMPs
### VERDICT: splits. 5a MISSING-AGREEMENT (717), 5b NEEDS-EXCEPTION but threshold-bound (428, 151, 899) — low priority.

**5a — board 717 (6 IMPs): no context for opener's decision over a completed
transfer plus an invitational 2NT.** `1NT-P-2H-P-2S-P-2NT-P-?` is covered by
`nt_2NT_opener_decides` only in the *direct* 2NT case. W `K85.AQ94.JT3.KQJ`
(15-17, three spades) reaches `uc_raise_S4` and jumps to 4S; 3S at fit 1.000 sits one
priority point below. 4S took nine tricks. FIX: add `nt_after_transfer_invite`
(`1NT - P - 2$t - P - 2$M - P - 2NT/3$M - P - ?`) with the standard four answers —
pass / 3M / 3NT / 4M by range and support. This also subsumes board 172 (cluster 2b).

**5b — boards 428 (13), 151 (11), 899 (11): the monster signs off in 4M.**
`uc_raise_S4` has an open-ended `total_points: [11, 40]`, so a 17-19 count lands in
game; the only escape, `gst_rkc_S` (priority 46), needs `rule_of_26_sharp >= 31` and
`controls >= 4`, and on each board it misses by roughly one point. There is no cue-bid
floor because `cue_bidding_S/H` require `game_forced: true`. The honest fix is to open
the cue contexts to an agreed suit at the three level with `rule_of_26 >= 28` even
without a formal game force. **That is a threshold change, which DECISIONS says has
measured neutral repeatedly — I flag it and do not recommend acting on it this round.**

---

## CLUSTER 6 — `ob_1D1S_2C`, 5 boards, 44 IMPs
### VERDICT: MISSING-AGREEMENT. Add the missing context; `ob_1D1S_2C` is innocent.

`1D - P - 1S - P - 2C - P - ?` has **no context**. `responder_after_minor_rebid` covers
only `1m - 1M - 2m` (opener *repeating* his minor). So responder falls through to
`uc_pass`. Board 645 (13 IMPs), W `AKQ3.AQ5.KQ6.Q54` — **19 HCP** — passes 2C; best
alternative 2H at fit 0.435. Board 356: 9 HCP with three diamonds passes rather than
taking a preference; 2C went for seven tricks.

FIX: add
```yaml
  - id: responder_after_1D1S_2C
    pattern: "1D - P - 1S - P - 2C - P - ?"
    rules:
      - id: r1d2c_pass   {P,  50, hcp [6,9],  suits {C:[4,13]}}
      - id: r1d2c_2D     {2D, 54, hcp [6,10], suits {D:[2,13]}, agreed_suit D}
      - id: r1d2c_2S     {2S, 55, hcp [6,10], suits {S:[6,13]}}
      - id: r1d2c_2NT    {2NT,56, hcp [11,12], semi_balanced}
      - id: r1d2c_3NT    {3NT,57, hcp [13,15], semi_balanced}
      - id: r1d2c_3S     {3S, 59, hcp [13,40], suits {S:[6,13]}}
```
(The 2H fourth-suit-forcing call is already supplied at higher specificity by
`fourth_suit_forcing`/`fsf_2H`, priority 65 — do **not** duplicate it here; my first
draft did and it was shadowed.)
Verified: 645 -> 2H (FSF), 414 -> 2H (FSF), 356 -> 2D, 200 -> 2D. All five boards.
ENDANGERS: nothing outside this exact auction.

---

## CLUSTER 7 — `open_1D`, 6 boards, 42 IMPs
### VERDICT: splits. 7a MISSING-AGREEMENT (242), 7b NEEDS-EXCEPTION (444, 467, 504).

**7a — board 242 (11 IMPs): responder passes 1D holding `J98.KT76543..742`** — eight
hearts and a **void in partner's suit**. `r1m_pass` (hcp [0,5]) fits 1.000; `r1m_1H`
needs 6 HCP and scores 0.409. There is no weak/long-suit response and no weak jump
shift in `resp_1m`.

FIX: widen the length branch of the existing rules rather than adding a colliding one:
```yaml
      - id: r1m_1H
        requires:
          all_of:
            - any_of:
                - suits: { H: [4, 13] }
                  evals: { "suit_diff(H,S)": [0, 13] }
                - suits: { H: [4, 4], S: [4, 4] }
            - any_of:
                - hcp: [6, 40]
                - hcp: [3, 40]
                  suits: { H: [6, 13] }
```
(and the analogous `any_of` on `r1m_1S`). Verified: 242 -> 1H, while a 4-HCP hand with
only four hearts still passes.
ENDANGERS: 3-5 counts with a six-bagger now respond, so partner may drive to a bad
game. The `hcp: [3, 40]` floor keeps genuine trash out.

**7b — boards 444, 467, 504: after opening 1D we go silent over their preempt.**
467: we open 1D on `KQT9..AKQT974.7-card diamonds`, they bid 2NT then 4H, and we pass.
444: 1D on a 7-4 hand, they reach 4H, we pass twice. The generic `ch_*` toolkit's
own-suit rebids ("values for the level opposite partner's shown range") evaluate to
**0.000** when partner has shown nothing. Same defect as single board 11 below — see
fix **F13**.

---

## CLUSTER 8 — `adx_pull_S3`, 4 boards, 41 IMPs  *(the rule the last review added)*
### VERDICT: IMPLEMENTATION-BUG and MIS-GATED, three separate defects. **NOT delete-rule.** Two of the four boards are innocent symptoms.

The principle behind the rule is right and is confirmed by the data: board 629 and
board 53 are correct pulls (5-card suit, weak hand, partner's takeout double) and the
IMPs there were lost upstream — on 629 by our 18-count doubling 3H instead of bidding
the 3NT that par says makes, on 53 by later passivity. **Any fix must preserve those
two, and mine does.** The cure overshot in three specific ways:

**8-i — the pulls are ordered by SUIT RANK, not by length.** `adx_pull_S* = 58`,
`H* = 57`, `D* = 56`, `C* = 55`, and every one of them says "pulling the double to the
cheapest 4+ suit". Board 248 (12 IMPs), E `A986.T98432..T73`: four spades, **six
hearts**, and the engine bids 3S.

**8-ii — `suits: { X: [4, 13] }` is soft, so tripletons pull.** Board 325 (9 IMPs),
S `853.743.AK7654.T`: three spades, six diamonds, and S is the **weak-2D opener**
pulling partner's *penalty* double of a 3C overcall. 3S scored fit 0.35 and won only
because nothing else scored at all — `general_pull_or_sit` is the most specific context
defining `P`, so `adx_sit` (which needs a 4-card trump stack **and** `suit_quality(their) >= 1.5`)
was the *only* pass candidate, at fit 0.000. The context removed the ability to pass.

**8-iii — the context also catches auctions that are not "advance partner's double".**
`pattern: "... - X - P - ?"` matches `1C - (2H) - X(negative) - P - ?`, where the
opener's job is to bid the major the double promised. Single board 125 (12 IMPs) is
exactly this: W holds `QT74.J.AK.KQT864`, partner's negative double promised spades,
and the pull ladder is what the engine consults.

FIXES (all four verified together):
1. **Order by length.** To each of the twelve `adx_pull_{S,H,D,C}{2,3,4}` rules add the
   three relational gates, e.g. for spades
   `"suit_diff(S,H)": [0, 13], "suit_diff(S,D)": [0, 13], "suit_diff(S,C)": [0, 13]`.
2. **Drop `standing_suit_length: [0, 2]` from the pull rules.** Advancing a takeout
   double you bid your suit whatever your length in theirs; `adx_sit` (priority 61)
   already owns the trump-stack case. Leaving it in makes board 629's correct 3S score
   0.349 and lose to the new pass floor.
3. **Add the missing floor pass** (this is what makes the soft 4-card gate safe):
```yaml
      - id: adx_pass_min
        call: P
        priority: 52
        requires: { evals: { total_points: [0, 11] } }
        shows: "no suit worth pulling to and no trump stack: partner's double stands"
        establishes: { forcing: sign_off }
```
   Priority 52 sits **below** the 54-58 pulls, so a genuine 4-card pull still wins on
   priority; the pass only takes over when every pull is soft-failing. This restores the
   ability to sit without reopening the -670 hole the last review closed.
4. **Gate the unbid-suit pulls on `i_have_acted: false`.** A player who has already
   described his hand (the preemptor on board 325, the opener on board 125) does not
   pull. `adx_pull_my_*` (keyed on `my_suit`) still lets an overcaller retreat to his
   own suit, so nothing legitimate is lost.
5. **Answer a negative double properly** — add to the same context, priority 62,
   `adx_neg_major_{H,S}{2,3}` with
   `when: { unbid_suit: M, cheapest_in_suit: true, their_last_bid_suit: true, i_have_acted: true }`
   and `requires: { suits: { M: [4, 13] }, hcp: [12, 40] }`.

Results: 248 -> **3H**, 325 -> **P**, 629 -> 3S (unchanged), 53 -> 3S (unchanged),
125 -> **2S**. 21 of the cluster's 41 IMPs plus single 125's 12.
ENDANGERS: (4) silences a pull by anyone who has bid, including a 1NT opener whose
partner doubles — but such a hand has `my_suit`/`adx_nt` routes. (3) will convert a few
"bid something" hands into passes; the `total_points: [0, 11]` ceiling keeps 12+ counts
bidding.

---

## CLUSTER 9 — `r1m_1NT`, 5 boards, 40 IMPs
### VERDICT: MISSING-AGREEMENT — clean, and the cheapest 40 IMPs in the dossier.

There is no `opener_rebid_1m_1NT` context. `opener_rebid_1M_1NT` exists for major
openings; after `1C/1D - P - 1NT - P` opener falls to `uc_pass`. On all five boards
opener holds **16-19** and passes 1NT:
320 (12) `KQJ2.6.AJ754.AK6`; 557 (10) `J.KJ42.A54.AKQ75`; 506 (6) `AJ6.AK4.AT6542.6`;
602 (6) `QJ4.A943.AK965.A`. Board 320's alternatives top out at 2S / fit 0.349.

FIX:
```yaml
  - id: opener_rebid_1m_1NT
    expand: { m: [C, D] }
    pattern: "1$m - P - 1NT - P - ?"
    rules:
      - id: or1mn_pass_$m       {P,   50, hcp [12,16]}
      - id: or1mn_rebid_$m      {2$m, 52, hcp [12,15], suits {$m:[6,13]}}
      - id: or1mn_jump_$m       {3$m, 54, hcp [16,19], suits {$m:[6,13]}, invitational}
      - id: or1mn_2NT_$m        {2NT, 56, hcp [18,19], semi_balanced, invitational}
      - id: or1mn_reverse_H_$m  {2H,  58, hcp [17,40], suits {H:[4,13]}, when unbid_suit H + cheapest_in_suit, one_round}
      - id: or1mn_reverse_S_$m  {2S,  58, hcp [17,40], suits {S:[4,13]}, when unbid_suit S + cheapest_in_suit, one_round}
```
Verified: 320 -> 2S, 557 -> 2H, 506 -> 3D, 602 -> 2H. All five boards.
ENDANGERS: nothing — the seat currently has no authored rule at all, and `or1mn_pass_$m`
supplies the floor so the lint's "floor" species does not fire.

---

## CLUSTER 10 — `open_1C`, 6 boards, 35 IMPs
### VERDICT: splits. 10a MISSING-AGREEMENT (841), 10b covered by cluster-1a/1b (43, 153, 146).

**10a — board 841 (14 IMPs): responder passes `1C - (1S)` holding `2.AJT6432.98432.`**
— seven hearts, five diamonds, 2 HCP. `nx_1m1S_pass` (hcp [0,8]) fits 1.000; the
negative double scores 0.80 and the 2H free bid needs 10+. There is no weak jump.
FIX: add to `resp_1m_over_1S`
```yaml
      - id: nx_1m1S_wj_H
        call: 3H
        priority: 56
        requires: { suits: { H: [6, 13] }, hcp: [0, 8] }
        shows: "weak jump shift: 6+ hearts, less than a free bid"
        establishes: { forcing: non_forcing }
```
Verified: 841 -> 3H. Mirror it in `resp_1m_over_1H` (`2S`/`3S` for spades) for symmetry.
ENDANGERS: it is a new (standard) agreement — partner must read 3H as weak, which the
`shows` text and negative inference deliver.

**10b — boards 43, 153, 146: we open, they overcall, and we never speak again with
16-19.** Board 43: W opens 1C with 19 HCP, they bid 1H-2H, W passes. Board 153: S opens
1C with 16 HCP and passes out their 1NT overcall. These are the *same* balancing hole as
cluster 1a/1b, one seat over; the `standing_suit_length` swap plus the balancing-2NT rule
address the mechanism. A penalty double of a **balanced** 1NT overcall by a 16+ opener
is still missing: consider extending `defense_vs_1NT`'s `v1NT_X` to the
"our 1-opening was overcalled 1NT" position.

---

# WORST SINGLE BOARDS 1-15

**86 (16) — IMPLEMENTATION-BUG. The jump raise of a doubled overcall is unreachable.**
`1D-(1S by us)-X(negative)-P-?`, E `KT73.KQ965.3.643` = four trumps and 11 support
points. `xd_raise_S2` (6-9) and `xd_raise_S3` (10+) **both** carry
`when: { cheapest_in_suit: true }`, and over the double only 2S is cheapest — so the
10+ band is dead and `xd_pass` (fit 1.000) takes the auction. FIX: add
```yaml
      - id: xd_jumpraise_S3        # and C3/D3/H3
        call: 3S
        priority: 32
        when: { we_bid_last: true, we_hold_contract: false, partner_suit: S, standing_bid_level: [1] }
        requires:
          suits: { S: [4, 13] }
          evals: { total_points: [10, 40], "lott_total_trumps(S)": [9, 26] }
```
Verified: 86 -> 3S. Also fixes board 538. ENDANGERS: more competitive 3-level bidding
after a negative double; the `standing_bid_level: [1]` gate keeps it to the jump.

**609 (14) — NEEDS-EXCEPTION.** N holds `AKQJ9872..53.AT9` over their 3H and doubles;
`3S` is sitting at **fit 1.000 / blended 0.892**, but `v3_H_X` (priority 70) outranks
`v3_H_S` and takes it, after which N has no candidate but pass over 4H. A takeout double
must deny a self-sufficient one-suiter. FIX: add to each `v3_*_X`
`evals: { longest_suit_length: [0, 6] }`, or an `any_of` waiver excluding
`longest_suit_length >= 7` with `suit_quality >= 2.5`.

**77 (13) — NEEDS-EXCEPTION (a systemic lie feeding the slam gate).** `2C-P-2D-P-3C-P-?`,
E `T6.JT3.975.KT964` (3 HCP) raises to 4C via `uc_raise_C4`, whose `requires` claims
`total_points: [11, 40]`. That claim is what `rule_of_26_sharp` then reads on W's side,
unlocking RKC and 6C for down two. FIX: give the game force a **truthful** minor raise —
add to `gf_landing_new_suit`
```yaml
      - id: gf_raise_4$m
        call: 4$m
        priority: 38
        when: { partner_last_suit: $m, cheapest_in_suit: true }
        requires: { suits: { $m: [4, 13] }, evals: { total_points: [0, 10] } }
        shows: "raise of partner's minor in the game force: no extra values"
```
so the 3-count stops advertising eleven points. (Prescribed, not prototyped.)

**314 (13) — NOTHING-WRONG / marginal.** Our 3D weak jump overcall on a 7-card suit at
favourable let EW cue-bid to 6S; the other table's 4D shut them out at 4S. If anything,
`oc1S_3D_jump` should have a 7-card twin at the 4-level
(`oc1S_4D_jump`, `suits: {D:[7,13]}, hcp: [4,9]`, they-vulnerable). Small, low confidence.

**538 (13) — same defect as 86.** E `8632.AK9.7.A9874`, four spades and 15 support
points opposite partner's doubled 1S overcall, runs to 2C because the jump raise does not
exist (`xd_raise_S2` fit 0.004, `xd_run_C2` fit 1.000). Verified fixed by the 86 patch:
538 -> 3S.

**591 (13) — NEEDS-EXCEPTION.** `1S - P - 4D(splinter) - P - ?`, W `AKQT6.4.KJT72.A4`.
`spl_wasted_4S` fires because `wasted_in_partner_shortness` counts K/Q/J opposite shown
shortness regardless of **length**: KJT72 opposite a stiff is a suit to establish, not
wasted paper. 6S was there. FIX: in `wasted_in_partner_shortness`, do not count honours
in a suit where I hold five or more cards (or gate `spl_wasted_4$M` on
`"suit_length(<short suit>)": [0, 4]`). This is an evaluator change — coordinate with
whoever owns `evaluators.py`.

**685 (13) — NEEDS-EXCEPTION, two layers.** `1D-P-1H-P-4H-P-4NT-P-5C-P-?`: N asked RKC
holding **one** keycard, got the ambiguous 1-or-4 answer, and signed off in 5H opposite
a hand that held four keycards. A 1430 ask is unreadable from a one-keycard hand. FIX:
gate `rj4_rkc` (and the other direct asks) with `evals: { "keycards(agreed)": [2, 5] }`.
Secondary: `ob_raise_4H` should not fire on a 12-count 4-card raise — it consumed the
whole auction before the 19-count could describe itself.

**703 (13) — NOTHING-WRONG at the indicted call.** Our 1S sandwich overcall was fine;
the loss is that nobody sacrificed in 4S over their 4H (par 200). This is the
save-over-their-game machinery, which the file only has for the mirror position
(`sacrifice_double_over_our_game`). Low confidence, out of scope for a mechanical fix.

**731 (13) — NEEDS-EXCEPTION, two rules.** `2NT-P-?` with `KT.K93.AJ982.Q74`: the engine
bids 4NT quantitative holding a five-card diamond suit (3C Stayman at fit 0.349). Then W
with 20 HCP and three aces passes. FIX: (i) add
`evals: { semi_balanced: [1, 1] }` and `not: { any_of: [ { suits: { D: [5,13] } }, { suits: { C: [5,13] } } ] }`
to `nt2_4NT_quant`; (ii) let the acceptance count controls —
`any_of: [ { hcp: [21, 21] }, { hcp: [20, 21], evals: { controls: [7, 12] } } ]`.

**925 (13) — MISSING-AGREEMENT.** There is no context for responder after **our** 1NT
opening is overcalled. `1NT - (2S) - ?` with `5.AKQJ2.9632.976` falls to `cl_pass`; the
other table bid 3H and made eleven tricks in 4H. FIX: add
`resp_1NT_over_overcall` (`1NT - bid - ?`) with the minimum ladder — natural new suit at
the cheapest level with 5+ (no point floor above 6), a competitive raise of 1NT to 2NT
with 11-12 and a stopper, X for penalty with 10+, pass otherwise. (Lebensohl is a
bigger change and not needed to recover these boards.)

**11 (12) — NEEDS-EXCEPTION.** `2D-P-2NT-3S-P-P-4D-?`, S `AQT7543.K72..AQ9`: seven
spades, 15 HCP, and **fit 0.000** for 4S. Every generic own-suit rebid
(`ch_rebid_S4`, `ballow_rebid_S4`, ...) counts "values for the level **opposite
partner's shown range**", and partner has shown nothing, so a self-sufficient suit is
zeroed out. FIX (this also covers cluster 7b, boards 444/467/504): give those rules an
`any_of` waiver
```yaml
          any_of:
            - evals: { total_points: [<existing floor>, 40], rule_of_26: [<existing>, 99] }
            - suits: { <suit>: [7, 13] }
              evals: { "suit_quality(<suit>)": [2.5, 9] }
```
so a seven-card suit with two of the top three bids on its own playing strength.

**15 (12) — NEEDS-EXCEPTION, two rules.** E holds `965.AQT8654.K4.8` over `1C-(2S)` and
makes a **negative double** with seven hearts, then passes 3C (3H at fit 0.409 both
times). FIX: (i) add to `nxj_X`
`not: { any_of: [ { suits: { H: [6, 13] } }, { suits: { S: [6, 13] } } ] }` — a
self-sufficient major is bid, not doubled; (ii) waive the 14-point floor on the generic
`*_new_M3` rules for a six-card suit:
`any_of: [ { evals: { total_points: [14, 40] } }, { suits: { M: [6, 13] }, evals: { total_points: [9, 40] } } ]`.

**125 (12) — IMPLEMENTATION-BUG, fixed by cluster 8 fix 5.** `general_pull_or_sit`
was interpreting the opener's answer to a negative double of a 2-level overcall.
Verified: 125 -> 2S (the major the double promised) instead of 3C. 4S was cold.

**143 (12) — IMPLEMENTATION-BUG (the cluster-2a inversion, competitive side).**
`1C-(1D)-?` with `76543.86.AQ5.A43`: `cl_new_S1` is priority 25 and additionally
demands `suit_quality(S) >= 1.5`, which a ragged five-bagger fails; `cl_nt1` (priority 27)
takes it with fit 1.000. FIX: bump `cl_new_H1`/`cl_new_S1` to priority 30 and waive the
quality floor for a five-card suit:
```yaml
          evals: { total_points: [6, 40] }
          any_of:
            - evals: { "suit_quality(S)": [1.5, 9] }
            - suits: { S: [5, 13] }
```
Verified: 143 -> 1S.

**217 (12) — NEEDS-EXCEPTION.** `1C-(2D)-2H-(4D)-?`, E `AQJ8.AJ.K5.A8632` = **19 HCP**,
passes. `ch_raise_H4` scores 0.029 (two trumps against a `[3,13]` floor, and
`lott_total_trumps(H)` = 7 against a sharp `[8,26]`); `ch_penalty_X` scores 0.349 because
it wants trump **length** and E has a doubleton. FIX: (i) apply the cluster-2b relaxation
(`suits: { M: [2, 13] }`) to `ch_raise_H4`/`ch_raise_S4` as well; (ii) give
`ch_penalty_X` a balance-of-power branch:
`any_of: [ { evals: { standing_suit_length: [4, 13] } }, { hcp: [18, 40] } ]` — with 19
opposite an overcall you double their four-level contract on values.

---

# FIX LIST (deduplicated, prioritized)

Ranked by (IMPs recovered on verified boards) x (confidence) / (risk).
F1-F9 are prototyped and jointly verified: `pytest tests/` 639 passed, lint
collide/gap/soft all 0, fuzz 0 crashes. F10-F17 are prescribed, not prototyped.

| # | Change | Boards recovered (verified) | Endangers |
|---|---|---|---|
| **F1** | `opener_rebid_1m_1NT` — new context, `1$m - P - 1NT - P - ?`, six rules incl. a `P` floor (cluster 9) | 320, 557, 506, 602 (+1) — **40 IMPs** | nothing; seat had no rule |
| **F2** | `responder_after_1D1S_2C` — new context, six rules incl. a `P` floor (cluster 6) | 645, 414, 356, 200 (+1) — **44 IMPs** | nothing outside this auction |
| **F3** | `gf_landing_new_suit` + `gf_landing_preference_major` (majors only!) (cluster 4) | 593, 574, 316, 229 — **51 IMPs** | longer GF auctions; the minors-only variant breaks two regression scenarios — keep majors-only |
| **F4** | `general_pull_or_sit`: length-ordering `suit_diff` gates on all 12 pulls; drop `standing_suit_length: [0,2]`; `i_have_acted: false` on the unbid-suit pulls; new `adx_pass_min` (P, 52, `total_points [0,11]`); new `adx_neg_major_{H,S}{2,3}` (62) (cluster 8 + single 125) | 248, 325, 125 — **33 IMPs**, and 629/53 verified unchanged | a hand that has bid can no longer pull to an unbid suit; a few "bid something" hands become passes |
| **F5** | `ballow_X`/`balhigh_X`: `suit_length(their)` -> `standing_suit_length`; add the 9-HCP/singleton branch to `ballow_X` (cluster 1a) | 921 + most of the 13-board `1x P 1y` group — **~40 IMPs est.** | more 1- and 2-level reopening; correct but noisier |
| **F6** | `ballow_nt2_balance` — 2NT, 15-21, stopper, `standing_bid_level: [2]`, `side_has_acted: false` (cluster 1b) | 782 + the `2H/2D/2S P P` families — **~35 IMPs est.** | 15-counts with a stiff now bid 2NT; `semi_balanced` is sharp |
| **F7** | `uc_raise_H4`/`uc_raise_S4` (and `ch_raise_*4`, `cl_raise_*4`): own-length floor `[3,13]` -> `[2,13]`, LOTT stays the gate (cluster 2b, single 217) | 126, 172 — **24 IMPs** | none found; LOTT counts partner's shown minimum |
| **F8** | `uc_new_H1`/`uc_new_S1` 25 -> 30; `cl_new_H1`/`cl_new_S1` 25 -> 30 **and** waive `suit_quality` for a 5-card suit (cluster 2a, single 143) | 350, 143 — **25 IMPs** | majors precede 3NT everywhere in the generic toolkit |
| **F9** | `responder_after_jump_raise`: `expand_pairs` adding `{m: H, M: S}` (cluster 3a) | 599 — **13 IMPs** | none |
| **F10** | `xd_jumpraise_{C,D,H,S}3` in `general_their_double`, `standing_bid_level: [1]` (singles 86, 538) | 86, 538 — **29 IMPs** | livelier 3-level competition after a negative double |
| **F11** | `open_1S_rule20_third` / `open_1H_rule20_third`, `suits: [5,7]`, `opening_seat: [3]` (cluster 1c) | 750 + 3 passed-out — **~20 IMPs** | more 3rd-seat 10-11 openings; the `[5,7]` cap is load-bearing (an 8-bagger must still preempt) |
| **F12** | `resp_1m`: `any_of` length branch (`hcp [3,40]` with a 6-card suit) on `r1m_1H`/`r1m_1S`; `nx_1m1S_wj_H`/`_S` weak jumps (clusters 7a, 10a) | 242, 841 — **25 IMPs** | 3-5 counts now respond and preempt |
| **F13** | Self-sufficient-suit waiver on every generic own-suit rebid (`*_rebid_M3/M4`): `any_of` branch `suits {M:[7,13]}` + `suit_quality >= 2.5`, bypassing the "opposite partner's shown range" term (single 11, cluster 7b) | 11, 444, 467 — **~26 IMPs** | 7-card suits bid to the 4-level unilaterally |
| **F14** | `v3_*_X`: add `evals: { longest_suit_length: [0, 6] }` so a one-suiter overcalls (single 609) | 609 — **14 IMPs** | fewer takeout doubles of preempts from 7-card hands |
| **F15** | `resp_1NT_over_overcall` — new context `1NT - bid - ?` (single 925) | 925 — **13 IMPs** | a new agreement; keep it natural, not Lebensohl |
| **F16** | `rj4_rkc` and the other direct asks: `evals: { "keycards(agreed)": [2, 5] }` (single 685) | 685 — **13 IMPs** | one-keycard hands lose the ask (correct — the 1430 reply is unreadable) |
| **F17** | `nt2_4NT_quant`: `semi_balanced` + no 5-card minor; quantitative acceptance counts controls (single 731); `wasted_in_partner_shortness` exempts my own 5+ card suits (single 591); `nxj_X` denies a 6-card major and the `*_new_M3` 14-point floor is waived for a 6-bagger (single 15); `ch_penalty_X` gains an `hcp: [18,40]` branch (single 217) | 731, 591, 15, 217 — **49 IMPs** | assorted; F17 is a bundle of small independent exceptions, land them one at a time |

**Explicitly NOT recommended** (measured-neutral thresholds, per DECISIONS):
`gst_rkc_*`'s `rule_of_26_sharp: [31, 99]` (clusters 3c, 5b — it misses by exactly one
point on boards 337/428/151/899); `uc_raise_*4`'s `rule_of_26: [25, 99]`;
`balhigh_X`'s 14-HCP floor (board 505); any HCP ceiling on the catch-all
`*_pass` rules. Also **NOTHING-WRONG**: boards 314 and 703, and cluster 8's boards 629
and 53 — the pull was right on both, and the IMPs went elsewhere in the auction.
