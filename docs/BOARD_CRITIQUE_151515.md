# Round 14 (seed 151515): board-by-board critique, 200 deals

`python3 tools/match_ben.py run --n 200 --seed 151515 --out reports/r14_batch.jsonl`
**-179 IMPs over 200 boards (-0.895/board)**, 42 won / 71 lost / 87 flat,
swings >= 10 IMPs 11 ours to 18 theirs.  Par gap table A -0.12, table B +0.39.

`python3 tools/ben_audit.py run --rows reports/r14_batch.jsonl --out reports/r14_audit.jsonl`
71 losing boards, **742 of our decisions replayed, 183 disagreements (24.7%)**,
98 with BEN >= 0.80 confident, **70 of them the first divergence** in their auction.

Every board we lost was read with `tools/board_critique.py`, worst first.  Every
call at both tables got exactly one verdict.  **559 decisions BEN agreed with are
OK by construction; of the 183 disagreements the great majority are also OK** -
style, a documented system difference, a scope-excluded threshold, or a
consequence of an earlier error.  Twenty fixes came out of the rest, and the
non-findings are recorded at the bottom because three of them were nearly
written up before the numbers were re-read.

Every indictment below was re-ranked through `score_candidates` and the
`requires` block was opened and quoted.  Where a number is quoted it is the
constraint, not the `shows` sentence.

---

## FIX 1 - the direct seat over a three-level preempt cannot bid four of a major

**Board 63 `[a1]`, -15.**  N `AQJT98765.A.Q.85`, dealer W, both vul, after `3C`.
We bid **3S** (`v3_C_S`); BEN bids **4S** at 0.71.  Partner (`4.QJT865.AKJ76.A`,
15 HCP) then had no way to move and 3S made 13 tricks for +260; at the other
table BEN's N/S reached 6S for +1460.

**Mechanism.**  `defense_vs_preempt_C` offers exactly five calls: `v3_C_X`,
`v3_C_3NT`, three three-level overcalls (`suits: [6,13]`, `hcp: [11,40]`,
`suit_quality >= 1.5`, `quick_tricks >= 2`) and `v3_C_pass`.  **There is no
four-level rung at all**, in any of the four `defense_vs_preempt_*` contexts.
An eight-card suit therefore makes the same call as a six-card suit.  This is
round 10's species exactly ("the sandwich seat stops at the two level"), one
context along; the openings already treat eight cards in a major as a 4M
opening.

**Verdict: RULE-WRONG** (a ladder with no top).  **Fix: add a rung** (fills a
hole, subtracts nothing).

```yaml
# AFTER - in each of defense_vs_preempt_C/D/H, above v3_$X_$M (64)
      - id: v3_C_4S
        call: 4S
        priority: 65
        requires:
          suits: { S: [7, 13] }
          evals: { total_points: [13, 40], "suit_quality(S)": [2, 9] }
        shows: "overcalling the preempt at the four level: a seven-card suit and opening values"
        establishes: { forcing: non_forcing }
```
and the `4H` twin over 3C/3D (over 3H only 4S is available; over 3S there is no
four-level major).  A 7+ suit now outranks the three-level overcall, which is
what changes: 7-card suits with 13+ move from 3M to 4M.

---

## FIX 2 - nothing in the generic toolkit RAISES partner's notrump

**Board 90 `[b7]`, -10.**  E `AJ64.AJ84.6.KT93` (13 HCP) after
`P 1D 1H X P 2NT P` - partner opened 1D, we made a negative double, partner
rebid **2NT (18-19)**.  We **passed** (`uc_pass`, fit 1.00, priority 18); BEN
bids 3NT at 0.94.  2NT made 12 tricks.

**Mechanism.**  The whole candidate set is pass, four natural new suits at 0.28,
`uc_nt3` at **0.00** and two doubler-raise rungs at 0.00.  `uc_nt3` is
`hcp: [13,19]` **with `semi_balanced: [1,1]`** and 4-4-1-4 is not semi-balanced,
so the only notrump rule in the context refuses.  Grepping the five generic
contexts: the only notrump rules are `uc_nt1/2/3`, `cl_nt1/2/3`, `ch_nt3`,
`ballow_nt*`, `balhigh_nt*` - **every one of them is a NATURAL notrump about my
own balanced hand and stoppers.  Not one raises a notrump partner has bid.**
Thirty-one combined opposite a shown 18-19 and the engine passes.

**Verdict: RULE-WRONG** (a missing agreement, not a bad rule).  **Fix: add a
rung.**  `we_bid_last: true` + `we_hold_contract: false` is exactly "partner's
bid is the standing contract"; with `standing_bid_strain: [NT]` that is
"partner has bid notrump and nobody has bid over it".

```yaml
# AFTER - in general_uncontested_continuation, immediately after uc_nt3
      - id: uc_nt_raise3
        call: 3NT
        priority: 28.5          # under uc_nt3, so the natural reading stays primary
        when: { we_bid_last: true, we_hold_contract: false, standing_bid_strain: [NT],
                standing_bid_level: [1, 2] }
        requires: { evals: { rule_of_26: [25, 99] } }
        shows: "raising partner's notrump to game: 25+ combined opposite the range partner has shown"
        establishes: { forcing: sign_off }
```

---

## FIX 3 - the doubler cannot answer his own partner on the points he doubled with

**Board 6 `[b5]`, -14.**  W `75.AK65.KJ7.8432`, **11 HCP**, after
`1S X 2S X P`: we doubled 1S for takeout, partner made a responsive double of
their raise, and we **passed it out** (`adx_pass_min`, fit 1.00).  2SX made ten
tricks, -670.

**Mechanism, and it is a floor mismatch between a call and its own follow-up.**
`oc1S_X`'s weak branch is **`hcp: [11,16]`** with 3-4 hearts - the hand doubled
at exactly its floor, fit 1.00.  `adx_neg_major_H3` ("answering partner's
negative double in the major it promised") requires **`hcp: [12,40]`**, so it
scores **0.80** and loses to `adx_pass_min` (`total_points: [0,11]`, fit 1.00,
priority 52).  The hand that qualified to double on eleven is one point short of
being allowed to answer.  This is round 9's `gst_rkc` / `rkc_4NT` species -
one agreement, two floors, and which applies decided by nothing.

**Verdict: RULE-WRONG.**  **Fix: reconcile the floor downward to the double's
own** (a widening; it cannot delete a reading).

```yaml
# adx_neg_major_H2 / H3 / S2 / S3, BEFORE
        requires: { suits: { H: [4, 13] }, hcp: [12, 40] }
# AFTER
        requires: { suits: { H: [4, 13] }, hcp: [11, 40] }
        # the takeout double that produced this auction has an 11-HCP floor
        # (oc1S_X, oc1H_X): a doubler who qualified on eleven must be able to
        # answer partner's responsive double on eleven.
```

---

## FIX 4 - the takeout double of a weak two is stricter than the double of a preempt

**Board 72 `[b1]`, -9.**  E `K42.KJT.K74.A872` (14 HCP, 3-3-3-4) after `2S`.
We **passed** (`vw2_pass`, fit 1.00); BEN doubles at 0.88.

**Mechanism, quoted from both rules.**

| | HCP | their suit | |
|---|---|---|---|
| `v3_C_X` (double of a **3-level preempt**) | 14-17 | **[0, 3]** | or any 18+ |
| `vw2_X` (double of a **weak two**) | 13-16 | **[0, 2]** | or any 17+ |

The double of the *higher* preempt tolerates three of their suit; the double of
the *lower* one does not.  That is backwards - at the two level you are one
level safer, not less - and it costs the commonest takeout shape there is.
`vw2_X` scored **0.349** here.

**Verdict: RULE-WRONG** (a gate given to one sibling and not the other, for the
sixth round running).  **Fix: add a branch** mirroring the preempt double
verbatim, one point dearer, keeping the six-card-suit denial the weak-two
double already carries.

```yaml
# vw2_X, AFTER - third any_of branch
            - hcp: [14, 16]
              suits: { $W: [0, 3] }
              evals: { longest_suit_length: [0, 5] }
```

---

## FIX 5 - the Stayman 2D-denial ladder has no quantitative invitation

**Board 51 `[a7]`, -11.**  S `AT.KQT8.AQ843.Q3` - **17 HCP** - after
`P 1NT P 2C P 2D P`.  We bid **3NT** (`stm_2D_3NT`, `hcp: [10,17]`, fit 1.00);
BEN bids 3D.  3NT made 13 tricks for +520; BEN's N/S bid 6NT at the other table.

**Mechanism.**  `stayman_resp_after_2D` has three rungs: 2NT `[8,9]`,
3NT `[10,17]`, 6NT `[18,21]`.  Seventeen opposite a 15-17 notrump is **32-34
combined**, which is the textbook quantitative zone, and the ladder jumps
straight from "game, 10-17" to "slam, 18+".  Its own sibling half has the route:
`stm_rkc_4NT` gives the 4-4 fit a 15-21 slam try.  The no-fit half was never
swept - the same asymmetry round 8 found in this very context in the other
direction.

**Verdict: RULE-WRONG** (a ceiling).  **Fix: add the rung AND the seat that
answers it** - the existing `nt_quant_opener_decides` is anchored
`1NT - P - 4NT - P - ?` and does not match a Stayman auction, so without the
answering context the invitation is declined by the code fallback (constraint 3,
the file's most common defect species).

```yaml
# stayman_resp_after_2D, AFTER - between 3NT (62) and 6NT (64)
      - id: stm_2D_4NT
        call: 4NT
        priority: 63
        requires: { hcp: [16, 17], evals: { controls: [3, 12] } }
        shows: "quantitative: 16-17 opposite a 15-17 notrump is 31-34, inviting slam"
        establishes: { forcing: invitational }
        alertable: true
# AFTER - a new context, the seat that answers it
  - id: stayman_quant_opener_decides
    description: "Opener over the quantitative 4NT after 1NT - 2C - 2D"
    pattern: "1NT - P - 2C - P - 2D - P - 4NT - P - ?"
    rules:
      - id: stmq_6NT
        call: 6NT
        priority: 60
        requires: { hcp: [17, 17] }
        shows: "accepting the quantitative invite: a maximum notrump"
        establishes: { forcing: sign_off }
      - id: stmq_pass
        call: P
        priority: 55
        requires: {}
        shows: "declining the quantitative invite: not a maximum"
        establishes: { forcing: sign_off }
```
The accept threshold and the complete-fallback decline are copied verbatim from
`nt_quant_opener_decides`, so the two statements of the same convention agree
(FIX 3's species, avoided).  `stm_2D_3NT`'s band is left alone: capping it at 15
would be threshold tuning, and the new rung outranks it in-band.

---

## FIX 6 - responder places the contract in a major opener has just denied

**Board 82 `[a10]`, -7.**  N `643.J754.T65.J97` after
`2C P 2D P 2NT P 3C P 3D P`.  Opener's **3D denies both majors**.  We bid
**4H** (`r2c_place_4H`, fit 1.00) into a 4-2 fit; seven tricks, -150.

**Mechanism.**  `r2c_after_stayman_reply` has
`pattern: "2C - P - 2D - P - 2NT - P - 3C - P - 3(D|H|S) - P - ?"` - one context
for all three of opener's answers - and its rules read only responder's own
shape:

```yaml
      - id: r2c_place_4H
        requires: { suits: { H: [4, 13] } }        # nothing about opener's answer
```

The alternation in the pattern throws away the one fact the auction just
established.  DECISIONS records this defect being fixed for the 1NT Stayman
ladder in round 4 ("Stayman placement reading WHICH major opener showed"); the
2C twin was never swept.

**Verdict: RULE-WRONG.**  **Fix: two `when` conditions** (`standing_bid_strain`
is already in the DSL and used by five rules).  The 3NT rung stays a complete
fallback, so no seat is starved.

```yaml
      - id: r2c_place_4H
        call: 4H
        when: { standing_bid_strain: [H] }
        requires: { suits: { H: [4, 13] } }
      - id: r2c_place_4S
        call: 4S
        when: { standing_bid_strain: [S] }
        requires: { suits: { S: [4, 13] } }
```

---

## FIX 7 - the transfer super-accept has no answering seat

**Board 88 `[a8]`, -6.**  N `KQ3.J9762.94.Q74` (7 HCP, five hearts) after
`P P 1NT P 2D P 3H P` - partner **super-accepted** (`tr_super_3H`:
`suits: {H: [4,5]}, hcp: [17,17]`, "4 hearts, maximum").  We **passed**
(`uc_pass`, fit 1.00).  4H makes ten tricks at the other table; +170 against
+420.

**Mechanism.**  `nt_after_transfer` is anchored
`1NT - P - 2$T - P - 2$M - P - ?` - **the simple acceptance only**.  After the
super-accept the seat matches no context at all; the toolkit's `uc_raise_H4`
wants `11+ support points` and scores **0.409** on eight, so the catch-all pass
takes it at 1.00.  Seventeen plus eight with a **nine-card fit** is a game, and
the super-accept exists precisely to say so.

**Verdict: RULE-WRONG** (a bid that promises a maximum, authored without the
seat that answers it - the file's most common defect species, fifth instance).
**Fix: add the context.**

```yaml
  - id: nt_after_super_accept
    description: "Responder after opener's super-accept of the transfer"
    expand_pairs: [ { M: H, T: D }, { M: S, T: H } ]
    pattern: "1NT - P - 2$T - P - 3$M - P - ?"
    rules:
      - id: trsa_game_$M
        call: 4$M
        priority: 60
        requires: { hcp: [5, 40] }
        shows: "accepting: a nine-card fit opposite a maximum is a game"
        establishes: { forcing: sign_off, agreed_suit: $M }
      - id: trsa_pass_$M
        call: P
        priority: 55
        requires: {}
        shows: "a bust: even opposite the maximum there is no game"
        establishes: { forcing: sign_off }
```

---

## FIX 8 - the negative double of a jump overcall promises nothing at all

**Board 194 `[a2]`, -2** (`J2.AQ7.98732.QJ5`, after `1C 2S`) and
**board 129 `[b2]`, -10** (`42.KQ5.J975.AJ73`, after `1D 2H`).  Both doubled;
both hold **three cards in the unbid major**; BEN passes 0.94 and 0.67.  On 194
partner bid 3H and we played a 4-3 fit for -150.

**Mechanism, quoted in full:**

```yaml
      - id: nxj_X
        call: X
        priority: 70
        requires: { hcp: [8, 40] }
        shows: "negative double of the jump overcall: support for unbid suits"
```

The sentence says "support for unbid suits"; the constraint is **8+ HCP and
nothing else**, at priority 70 - above everything in the context.  Its own
sibling one context away, `cl_negative_X1`, states the same convention properly
(`suit_length(their) <= 3`, `longest_suit_length <= 4`, `any_of` four hearts or
four spades).  Fit was **1.00** on both boards.

**Verdict: RULE-WRONG** (the rule does not implement its own sentence).  **Fix:
carry the sibling's shape gates verbatim.**  This SUBTRACTS the doubles made
without a four-card unbid major - which is what it is for.

```yaml
# nxj_X, AFTER
        requires:
          hcp: [8, 40]
          evals: { longest_suit_length: [0, 5] }
          any_of:
            - suits: { H: [4, 13] }
            - suits: { S: [4, 13] }
        shows: "negative double of the jump overcall: 8+ HCP with four cards in an unbid major"
```
(The context is expanded over the opened minor and the jump suit, so a jump in
one major leaves the other as the only major branch that can be satisfied; with
both majors bid the rule becomes unreachable, which is correct - there is
nothing to take out to.)

---

## FIX 9 - a four-card major cannot be bid at the one level without honours

**Board 5 `[a3]`, -7.**  N `T873.84.AQT3.KT4` (10 HCP) after `P 1C 1D`.
We bid **1NT** (`cl_nt1`, "8-11 balanced with a stopper", fit 1.00); BEN bids
**1S at 1.00**.

**Mechanism.**  `cl_new_S1` is

```yaml
        when: { unbid_suit: S, cheapest_in_suit: true }
        requires:
          suits: { S: [4, 13] }
          evals: { total_points: [6, 40] }
          any_of:
            - evals: { "suit_quality(S)": [1.5, 9] }
            - suits: { S: [5, 13] }
```
so a **four**-card major at the one level needs 1.5 suit quality; `T873` has
none, and the rung scores **0.349**.  The negative double is genuinely
unavailable (`cl_negative_X1` demands `suit_length(their) <= 3` and we hold four
diamonds), so the hand has one honest call and cannot make it.  A one-level
response is where four-card majors are shown; suit quality is a two-level
question, and the file already says so - `cl_new_S2` demands five cards, and the
quality branch exists to stop three-card "suits" at higher levels.

**Verdict: RULE-WRONG.**  **Fix: drop the quality requirement at the ONE level
for the two majors only** (a widening).

```yaml
# cl_new_S1 / cl_new_H1, AFTER
        requires:
          suits: { S: [4, 13] }
          evals: { total_points: [6, 40] }
        shows: "natural S at the one level: 4+ cards, 6+ points - the level where a four-card major is shown"
```

---

## FIX 10 - rebidding my own six-card suit at the two level needs eleven points

**Board 199 `[a9]`, -6** (N `JT9763.KJT.654.8`, 6 HCP, after
`1C P P X 1H 1S P P 2C`; we passed, `cl_rebid_S2` scored **0.028**) and
**board 128 `[b7]`, -1** (W `QT.Q87532.K42.82`, 6 HCP, after
`P 1C P 1H 1S 2C P`; we passed, `uc_rebid_H2` scored **0.409**; BEN bids 2H at
0.97).

**Mechanism, quoted:**

```yaml
      - id: cl_rebid_S2            # and uc_rebid_S2, and the six other twins
        requires:
          suits: { S: [6, 13] }
          evals: { total_points: [11, 40], "suit_quality(S)": [1, 9] }
        shows: "rebid of my own S: 6+ cards, values for the level opposite partner's shown range"
```
A flat **11-point floor** to repeat a six-card suit at the two level, and a
`shows` sentence claiming a partner-relative test the constraint does not make
(only the `uc_` twins carry the `not rule_of_26 >= 26` veto).  Repeating a
six-card suit at the two level is the cheapest sign-off in bridge, not a
values bid: 6-10 with six of my own has **no rule**, which is this project's
most recurring defect.

**Verdict: RULE-WRONG** (range with no rule).  **Fix: add a weak rung** rather
than lowering the existing floor, so the strong reading survives.

```yaml
# AFTER - beside each *_rebid_$X2, priority 28.5
      - id: cl_rebid_S2_weak
        call: 2S
        priority: 28.5
        when: { my_suit: S, cheapest_in_suit: true }
        requires:
          suits: { S: [6, 13] }
          evals: { total_points: [6, 10], "suit_quality(S)": [1, 9] }
        shows: "rebid of my own S at the two level: 6+ cards, 6-10 - a sign-off, not a values bid"
        establishes: { forcing: sign_off }
```
**What it costs:** same-call rules merge, so partner's shown minimum for a
two-level rebid of our own suit drops from 11 to 6.  That is the true meaning of
the call and it is stated deliberately (constraint 7).

---

## FIX 11 - a six-card major loses to 3NT on priority alone

**Board 108 `[b7]`, -12.**  W `KT6.KT9876.AQ.KT` (15 HCP, six hearts) after
`P 1D P 1H P 3D P` - partner's 16-18 jump rebid.  Two candidates **both fit
1.00**: `rjrb_3NT` at priority **55** and `rjrb_3M` ("6+ H, forcing") at **54**.
Priority alone chose notrump; we played 4NT for -720 against BEN's -1460 6H.

**Verdict: RULE-WRONG** (a ranking, not a range).  **Fix: one number** - the
round-12 `ob_1NT` precedent, where the same disease was cured by re-ranking
rather than by splitting a call in two.

```yaml
# rjrb_3$M, BEFORE: priority 54
# rjrb_3$M, AFTER:  priority 55.5
```
**What it subtracts:** hands that hold both a six-card major and a flat 3NT now
show the major.  That is the whole point; with six of a major and a game force,
notrump is what you bid when you have nothing else to say.

---

## FIX 12 - the choice-of-games 3NT is offered with a void

**Board 111 `[a7]`, -6.**  S `.J7652.AKQT95.J4` - a **spade void** - after
`P 1NT P 2D P 2H P`.  We bid **3NT** (`tr_3NT_choice`, fit **1.00**).

**Mechanism.**  `tr_3NT_choice` is `hcp: [10,15], suits: {$M: [5,5]}` and
nothing else.  DECISIONS records "no notrump with a void" as a system principle
implemented through `semi_balanced`; this rung has neither gate, and the
`void(any)` evaluator it would need is already in the file (`stm_rkc_4NT`,
`gst_rkc_$X`).

**Verdict: EXCEPTION** (the rule is right in general; a void is the stated
exception).  **Fix: the narrow gate, not `semi_balanced`** - 5-4-3-1 hands
should keep offering the choice of games.

```yaml
# tr_3NT_choice, AFTER
        requires: { hcp: [10, 15], suits: { $M: [5, 5] }, evals: { "void(any)": [0, 0] } }
        shows: "game values, exactly 5 $M and no void: choice of games (opener corrects to 4$M with 3+)"
```
**What it subtracts:** exactly the 5-card-major transfer hands with a void, one
in this corpus.  They fall to a natural bid in the long side suit.

---

## FIX 13 - the positive response to 2C demands two of the top three with six cards

**Board 185 `[a3]`, -11.**  N `KJ9763.J863.2.KT` - 8 HCP, **six** spades -
after `P 2C P`.  We bid **2D** waiting (fit 1.00); BEN bids **2S at 0.97**.
Table A stopped in 4H; table B, where BEN's responder gave the positive, reached
6H (+980 against +480).

**Mechanism.**  `r2c_2S_positive` is
`suits: {S: [5,13]}, hcp: [8,40], features: ["two_of_top3(S)"]` and `KJ9763`
holds one of the top three, so it scores **0.20** and `r2c_2D_waiting`
(`requires: {}`) wins at 1.00.  DECISIONS states the agreement as "2H/2S/2NT are
natural positives (8+)"; the top-three requirement is an undocumented extra, and
it is calibrated for a five-card suit.

**Verdict: RULE-WRONG.**  **Fix: length is quality** - widen the feature to a
disjunction, leaving the five-card requirement untouched.

```yaml
# r2c_2S_positive / r2c_2H_positive, AFTER
        requires:
          suits: { S: [5, 13] }
          hcp: [8, 40]
          any_of:
            - features: [ "two_of_top3(S)" ]
            - suits: { S: [6, 13] }
              features: [ "top_honour(S)" ]
        shows: "positive: 8+ HCP with five good spades, or six headed by an honour"
```

---

## FIX 14 - the weak jump shift has no suit-quality floor

**Board 22 `[a2]`, -11.**  N `T.T97543.KT6.T52` - **4 HCP**, hearts `T97543` -
after `1D 1S`, vulnerable.  We bid **3H** (`nx_1m1S_wj_H`, fit 1.00); BEN passes
at **1.00**.  4S made eleven tricks at both tables; the jump gave them the room
and cost the board.

**Mechanism.**  `nx_1m1S_wj_H` is `suits: {H: [6,13]}, hcp: [0,8]` - six cards
and a point ceiling, **no quality gate and no vulnerability condition**.  Every
one of the file's eight three-level preempts carries a quality floor (round 12
set it at 0 non-vulnerable / 1 vulnerable) and a quick-trick veto.  The jump
shift is the same bid from a different seat and carries neither.

**Verdict: RULE-WRONG** (a gate given to one family and not its sibling).
**Fix: copy the preempt family's floor verbatim.**

```yaml
# nx_1m1S_wj_H (and the 1H twin nx_1m1H_wj_S), AFTER
        requires:
          suits: { H: [6, 13] }
          hcp: [0, 8]
          evals: { "suit_quality(H)": [1, 9] }
        shows: "weak jump shift: a real six-card suit, less than a free bid"
```
Vulnerability is left out on purpose: a single flat floor is one sentence, and
the preempt family's split floor is a second experiment.

---

## FIX 15 - opener bids on over responder's weak three-level bail

**Board 96 `[b7]`, -3.**  W `KQ876.A86.A43.Q8` (16 HCP) after `P P P 1NT P 3C P`
- partner's `nt_3C_bail` is "weak bail: 6+ clubs, 0-7, **sign_off**".  We bid
**3S** (`uc_new_S3`, "5+ cards, 14+ points", fit 1.00, priority 27, over
`uc_pass` at priority 18) and played 3S for five tricks.

**Mechanism.**  `1NT - P - 3$m - P - ?` matches no context, so opener's seat
falls to the generic toolkit, which has no notion that partner has signed off:
`we_hold_contract` is keyed on **my own** last bid, deliberately (round 2), so
partner's sign-off is unprotected.

**Verdict: CATEGORY** (a sign-off filed as an ordinary continuation).  **Fix:
add the answering seat.**  It defines only `P`, so it cannot delete a reading -
it simply puts a pass above the invented bids.

```yaml
  - id: opener_over_bail
    description: "Opener over responder's weak three-level bail out of 1NT"
    expand: { m: [C, D] }
    pattern: "1NT - P - 3$m - P - ?"
    rules:
      - id: ntbail_pass_$m
        call: P
        priority: 60
        requires: {}
        shows: "partner has signed off in a long minor with a bust: pass"
        establishes: { forcing: sign_off }
```

---

## FIX 16 - the uncontested toolkit has no new suit at the four level

**Board 63 `[a3]`, -15.**  S `4.QJT865.AKJ76.A` - **15 HCP**, 6-5 in hearts and
diamonds - after `3C 3S P`, opposite partner's 3S overcall of a preempt (shown
"good 6+ S, 13+").  Twenty-eight combined and we **passed** (`uc_pass` 1.00);
the whole candidate list is five calls, the best of which scores **0.029**.

**Mechanism.**  `general_uncontested_continuation` has `uc_new_$X1`, `uc_new_$X2`
and `uc_new_$X3` - and nothing at the four level.  When the auction opens at
three (a preempt, an overcall of one), the toolkit's only new suits are already
below the standing bid, so the seat has no natural call in a suit at all.  The
same hole exists in `general_competitive_low`; `general_competitive_high` has
`ch_new_$X4` and `ch_new_$X5`, which is where the shape came from.

**Verdict: RULE-WRONG** (a ladder with no top).  **Fix: add the rung**, gates
copied verbatim from `ch_new_H4` so the two statements agree.

```yaml
# AFTER - in general_uncontested_continuation, beside uc_new_$X3
      - id: uc_new_H4
        call: 4H
        priority: 28
        when: { unbid_suit: H, cheapest_in_suit: true }
        requires: { suits: { H: [5, 13] }, evals: { total_points: [14, 40] } }
        shows: "natural H at the four level: 5+ cards, 14+ points"
        establishes: { forcing: non_forcing }
```
(and the C/D/S twins.)

---

## FIX 17 - in a game force opposite an unlimited partner no slam gate can open

**Board 74 `[b9]`, -13.**  W `Q.AT7.AK953.AKQ6` - **23 HCP, four controls** -
after `P 2C P 2D P 3D P 3H P`.  We raised to **4H** (`uc_raise_H4`, "11+ support
points", fit 1.00).  BEN's E/W bid 6H at the other table; -680 against -1430.

**Mechanism.**  `gst_rkc_H` scores **0.00**.  Its gate is

```yaml
          evals: { total_points: [15, 40], controls: [4, 12], rule_of_26_sharp: [31, 99],
                    "lott_total_trumps(H)": [8, 26] }
```
and `rule_of_26_sharp` reads partner's **shown minimum**.  Partner responded
`2D` waiting (`requires: {}`, "says nothing yet") and then `gf_new_3H` ("no
point floor: partner has the values").  Partner's floor is **zero by
construction**, so 23 + 0 can never reach 31: **after a 2C opening, every
combined-values slam gate in the file is unreachable, whatever the opener
holds.**  This is reviewer B's round-12 observation ("trumps agreed in a game
force: the currency should stop being points") with a mechanism attached.

**Verdict: CATEGORY** (a game force filed as an ordinary constructive auction).
**Fix: a second rung whose currency is my own hand**, at a lower priority so the
existing rule keeps the primary reading.

```yaml
# AFTER - in general_slam_try, beside gst_rkc_$X
      - id: gst_rkc_solo_S
        call: 4NT
        priority: 45.5
        when: { partner_suit: S, partner_last_suit: S, standing_bid_level: [2, 3, 4], we_hold_contract: false }
        requires:
          suits: { S: [2, 13] }
          evals: { total_points: [21, 40], controls: [4, 12], "lott_total_trumps(S)": [8, 26] }
          any_of:
            - evals: { "void(any)": [0, 0] }
            - evals: { "keycards(S)": [3, 5] }
        shows: "RKC 1430 for S: twenty-one points and an eight-card fit in my own hand, opposite a partner who has shown no minimum"
        establishes: { forcing: one_round, agreed_suit: S, asking: keycards }
```

---

## FIX 18 - a natural 1NT rebid tops out at ten points

**Board 163 `[a5]`, -6.**  N `T94.QT2.AK7.KQ84` - **14 HCP, balanced, diamonds
stopped** - after `P 1C 1D 1S P`: we opened 1C, they overcalled 1D, partner bid a
free 1S, RHO passed.  We **passed** (`uc_pass` 1.00); BEN bids **1NT at 1.00**.
Partner played 1S making eleven tricks.

**Mechanism.**  The notrump ladder is `uc_nt1` **`hcp: [6,10]`**, `uc_nt2`
`[11,12]`, `uc_nt3` `[13,19]` with `rule_of_26 >= 24`.  The bands are written for
a RESPONDER choosing a level by strength; for an opener rebidding after a
one-level response the cheapest notrump is 1NT whatever he holds, and 12-14
balanced has **no rung on any level**: 1NT is capped at 10, 2NT is an 11-12
invitation, and 3NT needs 24 combined which 14 opposite a free response does not
reach (`uc_nt3` scored **0.409** here).

**Verdict: RULE-WRONG** (range with no rule).  **Fix: add the rung** rather than
raise `uc_nt1`'s ceiling, so the 6-10 reading survives.

```yaml
# AFTER - beside uc_nt1 (and the cl_nt1 twin)
      - id: uc_nt1_strong
        call: 1NT
        priority: 27.5
        requires:
          hcp: [11, 14]
          evals: { semi_balanced: [1, 1], weakest_their_stopper: [0.9, 9] }
        shows: "natural 1NT: 11-14 balanced with their suits stopped - the cheapest notrump, not the strongest"
        establishes: { forcing: non_forcing }
```

---

## FIX 19 - no preemptive overcall of their 1NT

**Board 24 `[a2]`, -7.**  S `KQT8732.Q6.2.J62` - **seven** spades - after
`P 1NT`.  We bid **2S** (`v1NT_2S`, "5+ spades (usually 6), 8-15", fit 1.00);
BEN bids **3S at 0.95**.  We played 2S; BEN's side bought it in 3S at the other
table and we lost the partscore battle both ways.

**Mechanism.**  `defense_vs_1NT` is X, four two-level natural overcalls and a
pass.  **The ladder stops at the two level** - round 10's species again, and the
one place where preemption is most valuable, because the 1NT opener's partner
has the most to lose from a level.

**Verdict: RULE-WRONG** (a ladder with no top).  **Fix: add the rung.**

```yaml
# AFTER - in defense_vs_1NT, beside v1NT_2$X
      - id: v1NT_3S
        call: 3S
        priority: 62
        requires: { suits: { S: [7, 13] }, hcp: [6, 15], evals: { "suit_quality(S)": [1.5, 9] } }
        shows: "preemptive: a seven-card suit over their notrump"
        establishes: { forcing: non_forcing }
```
(and the H/D/C twins.)

---

## FIX 20 - a five-card major is opened ahead of a longer minor

**Board 114 `[b3]`, -6.**  E `AJT65..KJ7542.AK` - **six** diamonds, five spades,
17 HCP - in fourth seat.  We opened **1S** (`open_1S`, "5+ spades, 12-21", fit
1.00, priority 81); BEN opens **1D at 0.99**.  `open_1D` scores **0.10**,
because it requires "no 5-card major".

**Mechanism.**  The openings compare a major against the *other* major
("higher of equal length") but never against a minor: `open_1S`/`open_1H` fire on
any five-card major, and `open_1D`/`open_1C` deny one.  With 6-5 the textbook is
to open the longer suit, and after `1D` the spades are shown at the one level
over any one-level response - there is no reverse problem in the diamond case.

**Verdict: RULE-WRONG**, and the narrowest honest form is the diamond case only.
**Fix: one branch, the 6-5 shape with a diamond suit.**

```yaml
# open_1D, AFTER - an additional any_of branch (the existing branches keep
# "no 5-card major"); and open_1S/open_1H gain the matching denial so exactly
# one of the two fires:
            - suits: { D: [6, 13] }
              hcp: [12, 21]
              evals: { "suit_diff(D,S)": [1, 13], "suit_diff(D,H)": [1, 13] }
        shows: "opening the longer suit: six diamonds, longer than my five-card major"
```
**HIGH VARIANCE, and it must be measured alone.**  This is the most-fired rule
family in the file; the reviewer should check the whole-corpus population of
6-5 hands before anything ships.

---

# Verdicts that are OK, and the three findings they killed

The discipline that matters is being willing to say OK.  These were all read
carefully and left alone.

- **Board 17 `[b6]` - `stm_2NT_nofit` invites with 11.**  It does not.
  `Q873.KT4.AT63.83` is **nine** HCP, not eleven, and the rule is `hcp: [8,9]`
  with game from 10 in `stm_3NT_nofit`.  I had this written down as a band
  error before counting the hand.  **OK.**
- **Board 25 `[b6]` - no slam try with a 4-4 fit after Stayman.**
  `QJ87.96.AK43.A54` is **14**; `stm_raise_4$M` is `[10,15]` and
  `stm_rkc_4NT` opens at 15.  Fourteen opposite 15-17 is 29-31, which is a game.
  **OK** - and it is why FIX 5 is written for the no-fit half only.
- **Boards 122 `[a16]`, 146 `[b7]`, 160 - the Law at the three level.**  Three
  boards where we passed holding a big fit and BEN raised.  Round 13 measured
  this exact slice (contested, we passed, a three-level major raise soft-missing)
  at **37 tables, our gap +0.68 against a baseline of -0.38** and killed it.
  **OK**, three times.
- **Boards 3 `[b2]`, 91 `[a3]` - `r1m_1S` where BEN responds 1D.**  Walsh, a
  documented system choice; round 10 rejected the same lead.  **OK.**
- **Board 129 `[a1]` - BEN jump-overcalls where we overcall one.**  Round 11
  measured the re-rank at **-24 held out**.  **OK.**
- **Board 22 `[b11]`, board 86-species - `gr_rkc_S` asking over a game raise.**
  Twice measured (round 8: -17 held out; round 9: no separator survives).
  **OK**, deliberately, for the fourth round running.
- **Board 22 `[b13]/[b15]` - our 5C reply and the 6S over it.**  1430 against
  BEN's 3014, and the asker held three keycards opposite a shown one-or-four, so
  4 of 5 are present.  A system difference and correct arithmetic; the slam was
  off a finesse.  **OK.**
- **Board 92 `[b7]` - `uc_nt3` bids 3NT holding `93` in their bid suit.**  Real,
  and it is the standing `weakest_their_stopper` open item: the evaluator has no
  sharp tolerance, so no stopper scores 0.835 against `[0.9,9]`.  Round 8
  measured the one-line repair at **-9 held out** and reverted it because the
  seats behind the deleted notrumps are unauthored.  **OK** until those seats
  exist.
- **Boards 3 `[a3]`, 123 `[a3]`, 128 `[a4]`, 160 `[b3]` - `sw_pass` where BEN
  overcalls.**  The sandwich seat is uniformly half a point tighter on suit
  quality than the direct seat by design, and round 13 measured the whole family
  at **279 tables, our gap +2.90**, one of the healthiest in the engine.  **OK.**
- **Board 6 `[b1]` - `oc1S_X` on a 2-4-3-4 eleven-count where BEN passes.**  A
  textbook takeout shape; BEN's 0.88 pass is style, and the damage came from
  FIX 3's seat two calls later.  **OK.**
- **Board 130 `[a0]`, board 56 `[a0]` - 1D on a balanced 15 where BEN opens
  1NT.**  Opening style, scope-excluded.  **OK.**
- **Board 187 `[a1]`, board 135 `[a1]`, board 172 `[a2]` - BEN bids 2NT
  (unusual) or a Michaels cue.**  Both conventions are scope-excluded by
  DECISIONS.  **OK.**
- **Board 134 - we pass a quantitative 4NT with 18 and BEN's table bids 6NT.**
  BEN, asked in our seat, does not confidently disagree (conf < 0.5), and the
  accept rule is keyed to 19 - the top of the shown range.  A one-point
  judgment, i.e. threshold tuning, measured at -0.025 +/- 0.062.  **OK.**
- **Boards 80, 176 `[a0]`, 196 `[a0]` - `open_pass` where BEN opens.**
  Rule-of-20 threshold cases; scope-excluded three rounds running.  **OK.**
