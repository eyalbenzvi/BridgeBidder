# Expert review — round 8, seed 858585 — reviewer **B**

Assignment: clusters 11-20 (the dossier has 20 clusters, not 21 — cluster 21
does not exist), the last fifteen "worst single boards"
(621, 717, 740, 55, 82, 154, 296, 371, 397, 473, 518, 642, 665, 676, 709),
and an independent second opinion on clusters 1-3.

---

## 1. Method note

Everything below was reproduced before it was asserted.

* Every indictment was re-asked through `choose_bid` / `rank_at` at the exact
  decision index, and the interpreting context checked with `context_at`.
* Every suspect rule was re-scored across **all 2000 tables**, winners included
  (`rule_summary` / `fires_summary`). Denominators are quoted everywhere.
* Every proposed fix was prototyped in a scratch copy of the YAML and then
  **swept over all 10,470 of our decisions in the corpus** (re-asking each one
  under the prototype and diffing the call). The "changed of 10470" counts below
  are that sweep, not a spot check. This is what makes the ENDANGERS lines
  numeric rather than rhetorical.
* Outcomes were scored with the real double-dummy solver (`EndplayDD`) plus the
  project's own `contract_score` / `imps`, so "this board becomes 0 instead of
  -11" is an exact duplicate score, not an estimate. The harness reproduces
  every recorded `imp_margin` in the corpus.
* One fix needs a six-line engine addition (a `partner_last_call_was_double`
  condition). I patched a copy of `src/bridgebidder` in scratch and verified
  against that; the repo itself was not touched.

Corpus-wide baselines used repeatedly below: the match is **-710 IMPs over 1000
boards**, i.e. **-0.71 IMPs per table** across all 2000 tables. Any family whose
mean is near -0.71 is performing at the engine's average and is not a defect.

Total measured value of the fix list on this corpus: **about +115 IMPs**, of
which +99 is VERIFIED end to end.

---

## 2. Second opinion: clusters 1, 2, 3

These are stated as my own verdicts. I did not try to guess reviewer A.

### Cluster 1 — `uc_nt3` (24 boards, 141 IMPs) — **NOTHING-WRONG (symptom)**

Whole corpus, `uc_nt3` as the last bid: **67 tables, -61 IMPs, 11 wins / 25
losses / 31 flat, mean -0.91.** Firing anywhere: 69 tables, -61.

Two facts settle it:

1. The cluster's headline is 141 IMPs; the rule's *entire* net across all 2000
   tables is **-61**. Most of the 141 is the other table's doing. There is no
   141 to recover here.
2. The dossier lists **23 distinct auction families for 24 boards**. A rule that
   loses in twenty-three different auctions is not a rule with a defect; it is
   the terminal call of twenty-three different starved seats. This is the third
   round running that this rule has topped the list, and DECISIONS records that
   raising its strength gate moved a 1000-board match by **+1**.

Do not touch `uc_nt3`. One concrete upstream sub-case worth its own experiment
(NOT proposed here, because I could not express it): board 548 table B,
`1C X 1D 1H P 1S P 2S P 3NT`. East doubled 1C, bid 1S, partner *raised to 2S*,
and East then bid 3NT with 14 HCP opposite a shown 0-8 advance — 21 combined,
down four. `uc_nt3` fits 1.00 and outranks `uc_pass` 29 to 18. The honest gate
is "partner has raised my suit and we do not have game values", and the DSL has
no condition for "partner raised the suit I bid". It needs an engine condition
before it can be written, and it should be measured alone.

### Cluster 2 — `all-pass` (31 boards, 115 IMPs) — **NOTHING-WRONG**

Whole corpus: **553 tables** (28% of all tables), **-379 IMPs, 95 wins / 156
losses, mean -0.69 per table.**

The mean board margin over *all* 2000 tables is **-0.71**. The all-pass family
therefore performs at **exactly the engine's average — the difference is 0.02
IMPs per table.** It is not a loss concentration; it is a quarter of the corpus,
sampled. Round 7 reached the same conclusion from a different direction.

The 31 dossier boards are the defensive long tail, and reading them confirms it:
board 256 is a correct 4th-seat pass-out that happened to hand BEN a making 4S;
board 284 is our side passing 1H out at one table while our *other* table's
limit raise overbid — the loss is at the table that bid, not the one that
passed.

### Cluster 3 — `uc_raise_H4` (12 boards, 75 IMPs) — **NOTHING-WRONG on the rule; IMPLEMENTATION-BUG one rule downstream (`gst_rkc_$X`)**

Whole corpus: `uc_raise_H4` **41 tables, -44 IMPs, mean -1.07.** Its identical
twin `uc_raise_S4`: **44 tables, +12 IMPs, mean +0.27.** I diffed the two rules
character by character — **the gates are identical** (`suits: {$M: [2,13]}`,
`total_points [11,40]`, `rule_of_26 [25,99]`, `lott_total_trumps($M) [8,26]`,
priority 32). So the 1.34-IMP gap between the twins is the auctions, not the
rule, and there is no sibling asymmetry to repair here.

What the cluster's biggest board does show is a real sibling asymmetry **one
rule away**. Board 856, `1H - P - 1S - P - 2H - P - ?`, South holds
`AKJ754.96.A.AKJ3` (19 HCP, three keycards, a singleton diamond) opposite a
rebid that promises **six** hearts:

```
4H   uc_raise_H4   fit 1.00  prio 32     <- chosen
P    uc_pass       fit 1.00  prio 18
4NT  gst_rkc_H     fit 0.35  prio 46
```

`uc_raise_$M4` carries this comment and a **two**-card trump floor:

> `# lott_total_trumps is the real fit gate; my own length floor is 2 so a
> doubleton opposite a SHOWN six-card suit (weak two, rebid suit, completed
> transfer) still reaches the eight-card game.`

`gst_rkc_$X` — the keycard ask that is supposed to outrank that raise — kept a
**three**-card floor. The relaxation was never swept onto it. Probing the same
auction with `96` replaced by `963` lifts `gst_rkc_H` from 0.35 to **1.00**.
That is fix **#8** below: measured, it changes **1 decision in 10,470**.

Board 50 and board 539 in this cluster are *not* the same thing and I would
leave them: on 50 the ask correctly does not fire (partner has 3 HCP; the 6H
that made 12 double-dummy is a windfall, not a biddable slam), and on 539 the
weak-two opener raising partner's forcing 3H to 4H with 8 points is a judgment
overbid whose only clean gate would be an `i_preempted` discipline that
DECISIONS records as already tried and reverted at -10 IMPs.

---

## 3. Clusters 11-20

### Cluster 11 — `qr3_4NT_quant` (2 boards, 22 IMPs) — **NEEDS-EXCEPTION**

DECISIONS lists this as "a DELETE-THE-RULE candidate nobody has measured".
I measured it.

Whole corpus: **5 tables, -11 IMPs, 1 win / 2 losses / 2 flat.**
`qa_pass` (the decline) fires on **the same 5 tables**. `qa_6NT` (the accept)
**never fires in 2000 tables.** The invite has never once been accepted.

That matters because of the scoring table. 4NT and 3NT score *identically* on
10, 11 and 12 tricks (430/430, 460/460, 490/490). The invite is therefore free
except when exactly nine tricks are available, where it turns +400 into -50 —
and it can only gain by reaching a slam, which the accept gate has never done.
It is a lottery ticket with the prize removed. On the corpus:

| board | now | if 3NT stood |
|---|---|---|
| 338 | +11 | +11 (identical score) |
| 695 | **-10** | **0** |
| 755 | 0 | 0 (identical score) |
| 878 | -12 | -12 (identical score) |
| 980 | 0 | 0 (identical score) |

Deleting the rule and raising its floor measure **the same +10**. I prefer the
floor, because the convention itself is sound and DECISIONS authored it
deliberately; what is wrong is the number. `rule_of_26_sharp: [30, 99]` invites
slam on **thirty** combined points. Thirty combined is a game, not a slam
invitation. Thirty-two is the number that makes "partner needs a little extra
for 33" true. Fix **#6**.

Board 878 is not fixed by this and is not a `qr3` problem: South holds
`95..AQ63.AKQT854` — seven clubs to the AKQT, a **void in partner's suit**, and
the `quant_raise_of_3NT` context offers exactly two calls, 4NT and the fallback
pass. There is no 4C, no 5C, no 6C. BEN bid 6C. That seat is starved of any
suit call at all; authoring it is a separate piece of work and I do not propose
it on one board.

### Cluster 12 — `ch_sac_X` (2 boards, 20 IMPs) — **NOTHING-WRONG**

The headline looks damning: **3 tables, 0 wins, 3 losses, -21 IMPs.** It is
board-margin noise. The question that matters is what the double is worth
*against the alternative call*, and I computed all three double-dummy:

| board | doubled (actual) | if we had passed | if we had bid on |
|---|---|---|---|
| 340 | -15 | -14 | — |
| 982 | -1 | **-3** | — |
| 120 | -5 | **-11** | 5S: 0 |

Against passing, the double is **+7 IMPs net over three tables**. The rule is
paying its way; the boards were lost elsewhere (340 is really "we have no
Michaels and never found an eleven-card spade fit", which is scope-excluded).

I did prototype a `quick_tricks_outside` gate matching the rule's own stated
premise ("they sacrificed over our *game*", which the `when` clause does not
enforce). It kills all three firings and measures **+1, -2 and +5** — i.e.
noise, and it would delete a rule that beats its alternative. Reported, not
proposed. See NON-FINDINGS.

### Clusters 13 & 14 — `adx_pull_C3` / `adx_pull_H3` (5 boards, 37 IMPs) — **NOTHING-WRONG**

Whole `general_pull_or_sit` family across the corpus: **85 firings, -35 IMPs**
— i.e. -0.41 per firing against a corpus average of -0.71. The family is
*better* than the engine's average.

The obvious hypothesis is right in bridge and wrong on the data, and killing it
is the most useful thing in this section. Boards 346 and 55 both bury a
four-card major behind a five-card minor because the ladder's `suit_diff` gates
enforce strict longest-suit order:

* 346: East holds `AQ84.Q.953.QT632` over partner's reopening double of 2H and
  bids **3C** (fit 1.00) instead of **2S** (fit 0.80, one `suit_diff` miss).
* 55: South holds `AQ76.Q6.QJ964.65` over partner's double of 3H and bids **4D**
  instead of **3S**.

A takeout double asks for the majors, so I relaxed `suit_diff(S,D)`,
`suit_diff(S,C)`, `suit_diff(H,D)`, `suit_diff(H,C)` from `[0,13]` to `[-1,13]`
on the six major rungs. Both boards flip as intended. The whole-corpus sweep
found **6 of 85 firings change**, and scored double-dummy:

| board | now | after | delta |
|---|---|---|---|
| 55 | -11 | -10 (3S) | +1 |
| 73 | **+6** | **+2** (3S beats 4C: 8 tricks vs 10) | **-4** |
| 346 | -12 | -10 (2S) | +2 |
| 591 | **+7** | **+5** (3H on T862 beats 3C on K6532) | **-2** |
| 627 | -2 | 0 (speculative — the auction continues) | +2 |
| 415 | 0 | +6 (speculative — the auction continues) | +6 |

Holding the two speculative boards out, the change is **-3**. It is not
supported. The reason is visible in the losing rows: the gate cannot tell
`AQ84` from `T862`, and the 4-4 major is only right when it is a real suit. A
`suit_quality >= 2.0` rider separates all six boards perfectly, which is
precisely why I will not propose it — a threshold that separates four boards
exactly is curve-fitting, not bridge. **KILLED.**

One genuine defect in this family that I could not express: board 186,
`P 1C 2NT P 3D X P 3H P P P`. Partner's `X` was `ch_penalty_X` — a *business*
double, 15+ HCP with three of their trumps — and `adx_pull_H3` pulled it to 3H
on `8642` with three points, for -150 against a partscore. The
`general_pull_or_sit` pattern is `... - X - P - ?` and makes no distinction
between a takeout double and a penalty double. There is no condition for
"partner's double was penalty". Worth an engine condition in a later round;
one board is not enough to justify one now.

### Cluster 15 — `advS_2C` (2 boards, 17 IMPs) — **IMPLEMENTATION-BUG (upstream)**

`advS_2C` is innocent. Both boards are caused by the *double it is advancing*.

* Board 380: West doubles 1S holding **`KQ987`.AQ86.KQ3.6** — five spades.
* Board 779: North doubles 1S holding **`AQ976`**.A82.AK4.Q7 — five spades, 18 HCP.

`oc1S_X` reads:

```yaml
          any_of:
            - hcp: [11, 16]
              suits: { S: [0, 2], H: [3, 4], D: [3, 13], C: [3, 13] }
            - hcp: [17, 40]
              suits: { H: [0, 5] }
```

The **weak** branch requires shortness in their suit (`S: [0,2]`). The **strong**
branch constrains only the *other* major and says nothing about spades at all.
So a 17+ hand with five of their suit doubles for takeout and partner obediently
names the other one. `oc1H_X` has the mirror hole (`S: [0,5]`, nothing about
hearts). `oc1C_X` and `oc1D_X` are complete, because for them both majors are
unbid. This is the round-7 species exactly: a gate on one branch and not its
sibling.

Whole corpus: `oc1S_X` fires **15 times, -20 IMPs**. Exactly **two** of those 15
hold five spades — these two boards — and they carry **-17 of the -20**. The
other thirteen average -0.23. `oc1H_X` fires 16 times and never holds five
hearts; `oc1C_X` 19 times, `oc1D_X` 18 times, one 5-card their-suit case worth
-1 IMP. Fix **#4**.

### Cluster 16 — `ch_new_H4` (2 boards, 17 IMPs) — **NEEDS-EXCEPTION**

Whole-family record is fine: `ch_new_$X4` fires **7 times for +8 IMPs** (S4 +13,
C4 +12, H4 -17). Only board 546 is a disaster, and it is a specific one.

`1S - X - 2S - 3NT - ?`, South holds `KT862.AQJ86.T4.T` — **10 HCP**. Partner has
already raised spades. South bids 4H, gets doubled, goes down five for -1100,
where passing 3NT (which fails) is worth **0 IMPs**.

`ch_new_$X4` bands on `total_points: [14, 40]`. South's ten high-card points
become fourteen through a singleton and a doubleton — shortness that is worth
nothing once partner has shown a fit somewhere else. A four-level new suit in a
competitive auction contracts for ten tricks; that needs honest high cards, not
distribution. Adding `hcp: [12, 40]` alongside the existing total-points band
changes **1 decision in 10,470**. Fix **#3**.

### Cluster 17 — `r1C_1D` (2 boards, 17 IMPs) — **NOTHING-WRONG on the rule; MISSING-AGREEMENT downstream**

`r1C_1D` is a correct 1D response on both boards. Both losses are the seat
*after* it.

* Board 585: `1C - P - 1D - 2C - P - 4S(them) - P P P`. East holds
  `A.J83.Q863.AK542` (14 HCP) opposite a partner who has shown diamonds, and
  passes their jump to game out. Double-dummy: passing = -11, **doubling 4S =
  -4, bidding 5D = -1.** The candidate list at that decision is `cl_pass`
  (fit 1.00, prio 20) and the *code fallback* double (fit 1.00, prio 9).
  `ch_penalty_X` needs three of their trumps and East has a singleton; the
  5-level raise of partner's minor is not offered. There is no authored action
  over their preemptive jump to game. Worth ~+7 to +10; I have no patch I could
  verify inside my budget, so it is **UNTESTED** and listed last.
* Board 917: `P 1C P 1D X P 2S - ?`. North holds `6.872.AQT5432.T3` — a
  **seven**-card diamond suit — and passes 2S out; 3D is worth +6. The ladder is
  `cl_rebid_D3` (6+ cards, 11+ total points, `rule_of_26 >= 22`) and
  `cl_rebid_jump_D` (16-19). A seven-bagger with ten points opposite partner's
  opening bid falls between them. I prototyped a `cl_rebid_long3_$X`
  seven-card rung with the same 11-point floor (so partner's model is not
  weakened — see the ENDANGERS note on fix #1): the hand still misses on
  `total_points`, so **the prototype does not fix its own motivating board.**
  Reported as a non-finding.

### Cluster 18 — `cue_H_signoff` (2 boards, 17 IMPs) — **NOTHING-WRONG**

Board 643, `P 1S P 2H P 3H - ?`, South holds `T75.A87642.A9.A5`: six hearts and
**three aces**, and signs off in 4H (`cue_H_signoff`, `requires: {}`, prio 34,
fit 1.00) while `cue_H_C` fits 0.41. BEN bid 6H making 13.

The obvious repair is that a cue should be gated on controls, not only on
points, so I prototyped `any_of: [ {total_points 14+, rule_of_26 28+},
{controls: [6,12]} ]` on all six major cue rules. **The cue fires (4C) — and the
board does not move.** Partner has no diamond control, signs off honestly in 4H,
and South's twelve high-card points then fail every keycard gate (15+ points,
`rule_of_26_sharp` 31+). Final contract 4H by North instead of 4H by South:
**-11 either way.** Twelve opposite fifteen-to-seventeen is not a slam by any
point count; the 6H that made thirteen tricks did so on a `KJT` heart holding
and a 3-3 break. Negative result, reported, not proposed.

### Cluster 19 — `gf_3NT` (2 boards, 17 IMPs) — **MISSING-AGREEMENT (UNTESTED)**

Board 699: `P P P 2C P 2D P 2S P 3H P 3S P 3NT`. North holds
`5.JT843.T53.AQ74` — a **singleton** in the suit partner has now bid twice
(2C opener, 2S, 3S = seven spades) — and lands in 3NT for down three where 4S
makes ten tricks. The ranking is the signature of a starved seat:

```
3NT  gf_3NT      fit 0.067  prio 34   <- chosen
4S   uc_raise_S4 fit 0.004  prio 32
4H   uc_rebid_H4 fit 0.000
```

Nothing fits at all; `gf_3NT` wins on 0.067. The landing family covers "fit /
no fit" and treats a singleton as no fit, but partner has **rebid his own
suit** — that is a self-sufficient trump holding and the landing is four of the
major whatever I hold. The rung wanted is a `gf_landing` companion gated on
`lott_total_trumps($M) >= 7` with partner's suit rebid, ranked above `gf_3NT`.
I did not have budget to author and sweep it, so it is UNTESTED and not in the
fix list; it is recorded here because the seat is genuinely empty.

### Cluster 20 — `uc_rebid_D3` (2 boards, 16 IMPs) — **MISSING-AGREEMENT**

Board 252 is the cleanest starved seat in my whole slice. `1D - P - 1H - P -
2D - P - 2NT - P - ?`, North holds `92.98.AKQJ976.A7`: **AKQJ976 of diamonds
plus the club ace**, eight tricks in hand, opposite an 11-12 invitational 2NT.
It bids 3D and the auction dies. BEN bid 3NT.

The context that owns this position, `opener_over_invite_2NT_minor`, contains
**exactly one rule** — the 5m sign-off. There is no acceptance, no decline, no
pass. Everything that is not "6+ minor, 16-21, no stopper anywhere" falls
straight through to the generic toolkit, which rebids the minor. An invitation
answered by silence, again. Fix **#5**: +10 on this board, +7 across the three
tables it touches.

Board 6 is the same shape in a competitive auction (`1S 2D 2S 2NT P ?`, West
holds a void and `KQJ9876` and rebids 3D where 5D makes eleven tricks). It is
not the same context and `cheapest_in_suit` blocks the 5-level bid; I have no
verified patch and do not propose one.

---

## 4. The fifteen worst singles

| board | verdict | one line |
|---|---|---|
| **621** | NEEDS-EXCEPTION | keycard ask over partner's game raise with **two** keycards; sign-off is 5S, one level above the 4S we already owned. Fix #2. |
| **717** | NOTHING-WRONG | see below. |
| **740** | NOTHING-WRONG | `adx_sit` converting a takeout double of 3S on `K843`. Whole corpus `adx_sit`: **25 firings, +16 IMPs, 12 wins / 11 losses.** DECISIONS already adjudicated this family (9 tables, doubled contract down on 7). The double itself hides `AKQ942`, and round 7 killed the six-card-suit veto with 113 firings of data. Leave it. |
| **55** | diagnosed, not fixable | the 4-card-major-behind-5-card-minor pull; the fix measured negative corpus-wide (see cluster 13). The second half — the doubler's raise — is fix #1b and does land. |
| **82** | NEEDS-EXCEPTION (untested) | opener passes their unusual 2NT holding 12 HCP and **four-card support** for partner's 1H response. `cl_raise_H3` fits **0.409**: it misses `rule_of_26 >= 20` by one point (13 own + partner's shown 6). A *competitive* raise to the three level with eight trumps is a Law bid; `rule_of_26` is the constructive criterion and DECISIONS itself says "the Law gates competitive raises only". Not proposed as a patch — changing that gate reaches every competitive raise in the book and needs its own experiment. |
| **154** | MISSING-AGREEMENT | `3D X 4D - ?` with `QT9762` and 9 HCP: pass. Fix #1. **+11 VERIFIED.** |
| **296** | MISSING-AGREEMENT | `P 1D 2C X 3C - ?`: opener passes with `AK92` opposite a negative double that promised four spades. Fix #1 authors the rung (carried verbatim from `adx_neg_major_$M3`), but East's 11 HCP misses the shadowed rule's own 12-point floor by one, so **this board does not move**. Stated as a partial. |
| **371** | MISSING-AGREEMENT (untested) | `2NT - 3C - 3D - ?` with 11 HCP: `nt2_stm_3NT` is `requires: {}` and there is no quantitative 4NT rung after Stayman finds no fit. 11 opposite 20-21 is the textbook invite; 6NT was cold (0 IMPs vs -11). Needs its own accept context (`2NT-P-3C-P-3x-P-4NT-P-?`), which is why it is not in the fix list — a ladder without its answering seat has cost this project a cycle before. |
| **397** | NOTHING-WRONG | 4th-seat rule-of-15 1C opening on `Q3.A76.J5.AKQ954`, then the invitational 3C jump rebid, passed by an 8-count. BEN opened 1NT and reached 3NT. Opening 1C with 2-3-2-6 is orthodox; the loss is a style difference on the opening, which is scope-excluded. |
| **473** | NOTHING-WRONG | `1D - 1H - 4H` on a 19-count opposite a 6-count; BEN's 6H makes twelve tricks on **25 combined HCP**. `ob_raise_4$M` is deliberately capped at 24 so monsters reach the keycard rules; 22 support points is inside the cap and 4H is the bid. This is a double-dummy slam, not a biddable one. |
| **518** | diagnosed, not proposed | 6-5 hand (`87.KQJ72.QJ8532.`) bids and rebids the six-card minor and never shows the five-card major; BEN's table played 4H on a nine-card fit. "A ladder that bands by strength forgets to band by shape" — the species DECISIONS names as an un-linted meta-defect. One board here; no patch I could verify. |
| **642** | MISSING-AGREEMENT | 21-count opposite a 3H preempt has no slam try — `rp3_$x` has a game rung and nothing above it, and `gst_rkc` can never fire because `rule_of_26` cannot reach 31 opposite a 4-9 preempt. Fix #2. **+11 VERIFIED**, and it also recovers board 958 (+13). |
| **665** | MISSING-AGREEMENT | `1C 1D X 2D - ?`: opener passes with 12 HCP and `KJ3` of their suit after partner's negative double. 2NT = -10, **3NT = 0** against the recorded -11. Same starved seat as #1 but the call wanted is notrump, not a suit; not covered by my patch. |
| **676** | NOTHING-WRONG | `qr3_6NT` raises 3NT to 6NT with 16 HCP and `rule_of_26_sharp >= 33`; 6NT takes eleven tricks. DECISIONS records that gating `qr3_6NT` on shape killed five cold 6NTs and was reverted. One failed slam on 29 combined is the price of the rule, not evidence against it. |
| **709** | MISSING-AGREEMENT | `1H X 3H - ?` holding **`QT76543`** and passing. Fix #1. **+11 VERIFIED.** |

**Board 717 in full**, because it looks like a bug and is not. `P 1C P 1S P 1NT
P ?`, North holds `AT987.A5.AQ74.A2` (17 HCP, five spades, four aces) and bids a
quantitative 4NT; partner declines with 13; 6S was cold. There is a real sibling
inconsistency here — `rr_nt_3NT` denies a **five**-card major, `rr_nt_4NT` denies
only a **six**-card one — so the 4NT (prio 55) beats `rr_nt_gf3_S` (prio 53.5)
by a point and a half and the 5-3 fit is never explored. I patched it and
followed the auction through:

```
1C - P - 1S - P - 1NT - P - 3S - P - 4S - P - 4NT - P - 5D - P - 5S
```

North has four keycards and correctly signs off in 5S, because the reply denied
the trump queen and the shown fit is eight cards (round 6 added that clause and
measured it positive). **5S making twelve scores 680; the 4NT it replaced,
making twelve, scores 690.** The "fix" measures **-1 IMP on its own motivating
board.** Reported in NON-FINDINGS rather than shipped. `rr_nt_4NT` fires **once
in 2000 tables**, so nothing here is worth a gate.

---

## 5. FIX LIST (priority order)

### FIX 1 — the advance of partner's takeout double when RHO bids over it
**+31 IMPs · VERIFIED · 3 changed decisions of 10,470 · HIGH-VARIANCE: no**

Boards 154 (-11 → 0), 709 (-11 → 0), 526 (+2 → +11). Also the mechanism behind
296 and, with the second half, 55.

`general_pull_or_sit` covers `... - X - P - ?`. When RHO **bids** over partner's
double there is no advance context at all: the seat falls to
`general_competitive_high`, whose new-suit rungs demand `total_points: [14,40]`
— a floor calibrated for a partner who *overcalled*. Facing a takeout double the
advance is owed, and a seven-card major with nine points had no call:

```
board 709   N  QT76543.K98..986   after 1H - X - 3H
    P    ch_pass       fit 1.00  prio 22   <- chosen
    (no spade bid offered at any level)
```

**1a. Engine (six lines, mirrors the existing `my_last_call_was_double`).**

`src/bridgebidder/system/dsl.py`, after
`    my_last_call_was_double: bool | None = None    # my most recent non-pass call was X`
add
```python
    partner_last_call_was_double: bool | None = None  # partner's most recent non-pass call was X
```
and in `Conditions.from_dict`, after
`            my_last_call_was_double=d.pop("my_last_call_was_double", None),`
add
```python
            partner_last_call_was_double=d.pop("partner_last_call_was_double", None),
```

`src/bridgebidder/inference/engine.py`, immediately after the
`my_last_call_was_double` block (`if was_x != cond.my_last_call_was_double: return False`):
```python
    if cond.partner_last_call_was_double is not None:
        last = None
        for i, c in enumerate(auction.calls):
            if auction.seat_of_call(i) == seat.partner and not c.is_pass:
                last = c
        was_x = last is not None and last.kind == "double"
        if was_x != cond.partner_last_call_was_double:
            return False
```

**1b. YAML — `general_competitive_high` (line ~10203, immediately BEFORE `- id: ch_new_C4`).**

BEFORE: nothing (the rungs do not exist).
AFTER — eight rungs, `$X` written out because this context is not templated:
```yaml
      # Partner made a TAKEOUT DOUBLE and they bid over it.  The advance is
      # still owed: partner has opening values and shortness in their suit, so
      # a real suit of mine is a bid, not a 14-point bid.  The generic new-suit
      # rungs below demand 14+ total points - calibrated for a partner who
      # OVERCALLED - and left a seven-card major with nine points no call at
      # all, so the catch-all pass swallowed it.
      - id: ch_advance_x3_C
        call: 3C
        priority: 28.5
        when: { unbid_suit: C, cheapest_in_suit: true, partner_last_call_was_double: true,
                i_have_acted: false }
        requires:
          suits: { C: [6, 13] }
          evals: { "suit_quality(C)": [1.5, 9], total_points: [8, 40] }
        shows: "answering partner's takeout double in my own suit, forced by the double"
        establishes: { forcing: non_forcing }
```
…and the same rule seven more times, as `ch_advance_x4_C` (`call: 4C`),
`ch_advance_x3_D` / `ch_advance_x4_D`, `ch_advance_x3_H` / `ch_advance_x4_H`,
`ch_advance_x3_S` / `ch_advance_x4_S`, substituting the suit letter throughout.

Then, immediately after those, the negative-double answer, with the gates of
`adx_neg_major_$M3` carried **verbatim** so it can only be a superset of the
rule it mirrors (six rules: 2H/3H/4H, 2S/3S/4S):
```yaml
      # ... and the NEGATIVE double promised the unbid major, so opener answers
      # it in that major with four cards, exactly as adx_neg_major_$M does when
      # they pass instead of competing.  Gates carried verbatim from that rule.
      - id: ch_neg_major_3S
        call: 3S
        priority: 30
        when: { unbid_suit: S, cheapest_in_suit: true, partner_last_call_was_double: true,
                i_have_acted: true }
        requires: { suits: { S: [4, 13] }, hcp: [12, 40] }
        shows: "answering partner's negative double in the major it promised"
        establishes: { forcing: non_forcing, agreed_suit: S }
```

**1c. YAML — `general_uncontested_continuation` (line ~11378, immediately BEFORE `- id: uc_doubler_game_H`), the companion the advance needs.**

The doubler's 17-19 raise rungs (`uc_doubler_raise_$M` / `uc_doubler_raise3_$M`)
are all gated `cheapest_in_suit: true`, so when partner's advance is **already at
the three level** — the normal case over a preempt — their call is no longer the
cheapest bid in the suit and only the 20+ jump remains. A seventeen-count passes.
That is a ceiling; this is the rung above it:
```yaml
      # When partner's advance is already at the THREE level (the normal case
      # over a preempt) the 17-19 raise rungs below are unreachable - their
      # call is no longer the cheapest bid in the suit - so a seventeen-count
      # facing a forced advance had only the 20+ jump and passed.  A ceiling
      # again: this is the rung above it, gated on the LOTT fit rather than on
      # four-card support, because partner's advance already promised length.
      - id: uc_doubler_game3_H
        call: 4H
        priority: 35
        when: { partner_suit: H, my_last_call_was_double: true, we_hold_contract: false,
                standing_bid_level: [3] }
        requires:
          suits: { H: [3, 13] }
          evals: { total_points: [17, 40], "lott_total_trumps(H)": [8, 26] }
        shows: "raising partner's three-level advance to game: 17+ and a real fit"
        establishes: { forcing: sign_off, agreed_suit: H }
```
plus the identical `uc_doubler_game3_S` (`call: 4S`, `partner_suit: S`,
`suits: { S: [3, 13] }`, `lott_total_trumps(S)`).

Verified auctions:
* 154: `3D X 4D 4S P P P` — 4S by East, **0 IMPs** (was -11).
* 709: `1H X 3H 3S P 4S…` — 4S (or 5S after the keycard ask; both score 680), **0 IMPs** (was -11).
* 526: `1C 2S P P X P 3H P 4H` — **+11** (was +2).

**ENDANGERS.** This is where the `total_points: [8, 40]` floor comes from, and
it is not cosmetic. Same-call rules merge into a disjunction for the partner
model, so a rung with **no** point floor lowers partner's shown minimum for that
call *everywhere*, whatever hand partner actually held. With no floor the sweep
showed board 218 regressing by 10 IMPs: `uc_raise_S4` needs `rule_of_26 >= 25`,
partner's 3S dropped from a shown 10 to a shown 0, and a cold 4S turned into a
pass. Floors of 9, 10 and 11 all protect 218 but lose board 709; **8 protects
218 and keeps both target boards**, and the full 10,470-decision sweep at 8
shows exactly the three changes above and nothing else. The six-card requirement
(rather than five) is the second guard: it keeps the new rungs off the five-card
advances the existing ladder already handles.

---

### FIX 2 — a keycard ask opposite partner's three-level preempt
**+24 IMPs · VERIFIED · 2 changed decisions of 15 `rp3_*` firings · HIGH-VARIANCE: no**

Boards 642 (-11 → 0) and 958 (-13 → 0; that is reviewer A's single, but the fix
is here).

All four `resp_preempt_$x` contexts have three forcing new-suit rungs, a game
rung and a pass — and **nothing above the game rung.** A 21-count opposite a
seven-card suit has no slam try, and the generic `gst_rkc_$X` can never rescue
it because its `rule_of_26_sharp: [31, 99]` gate cannot be reached opposite a
preempt's shown 4-9. Board 642, East `AK53.AK.AKJ75.Q8`:

```
4H   rp3_H_game   fit 1.00  prio 64   <- chosen
4NT  gst_rkc_H    fit 0.029 prio 46
```

**YAML** — in each of `resp_preempt_C` / `_D` / `_H` / `_S` (lines ~8434, 8476,
8518, 8560), immediately BEFORE `- id: rp3_$x_game`:

BEFORE: nothing.
AFTER (shown for hearts; repeat with C, D, S):
```yaml
      - id: rp3_H_4NT
        call: 4NT
        priority: 65
        requires:
          suits: { H: [2, 13] }
          evals: { total_points: [20, 40], "keycards(H)": [2, 5] }
        shows: "RKC 1430 for H: slam values opposite the preempt"
        establishes: { forcing: one_round, agreed_suit: H, asking: keycards }
        alertable: true
        convention: rkc_1430
```

The answering seat already exists and needs no new work: `rkc_response` is
`pattern: "... - 4NT - P - ?"` gated on `when: { asking: keycards }`, and the
continuations key off `agreed_suit`. Verified end to end:
* 642: `P 3H P 4NT P 5C P 6H P P P` — 6H making 13. **0 IMPs** (was -11).
* 958: `3S P 4NT P 5D P 6S P P P` — 6S making 13. **0 IMPs** (was -13).

**ENDANGERS.** Purely additive — a new rung in an existing context, so it cannot
subtract a reading. It does add a 4NT interpretation at `3x - P - ?`, which the
context previously did not define; the `20+ total points and 2+ keycards` gate
is why only 2 of 15 `rp3_*` firings move. Everything else is untouched.

---

### FIX 3 — a four-level new suit in competition needs high cards, not shape points
**+15 IMPs · VERIFIED · 1 changed decision of 10,470 · HIGH-VARIANCE: yes (one board)**

Board 546 (-15 → 0).

`src/bridgebidder/systems/two_over_one.yaml`, lines 10203-10238, all four rules.

BEFORE (shown for hearts; identical edit for `ch_new_C4`, `ch_new_D4`, `ch_new_S4`):
```yaml
      - id: ch_new_H4
        call: 4H
        priority: 28
        when: { unbid_suit: H, cheapest_in_suit: true, partner_has_acted: true }
        requires:
          suits: { H: [5, 13] }
          evals: { total_points: [14, 40], "suit_quality(H)": [1.5, 9] }
```
AFTER:
```yaml
      - id: ch_new_H4
        call: 4H
        priority: 28
        when: { unbid_suit: H, cheapest_in_suit: true, partner_has_acted: true }
        requires:
          suits: { H: [5, 13] }
          # A four-level new suit contracts for ten tricks.  Shortness points
          # turned a TEN-count into a fourteen and it bid 4H over their 3NT with
          # partner having already raised spades: doubled, down five, -1100.
          hcp: [12, 40]
          evals: { total_points: [14, 40], "suit_quality(H)": [1.5, 9] }
```

**ENDANGERS.** It is a gate, so it subtracts. Measured: the four rules fire 7
times in the corpus for +8 IMPs net, and the full 10,470-decision sweep changes
**exactly one** — board 546. It also narrows the descriptor for a four-level new
suit (partner now reads 12+ HCP as well as 14+ total points); the sweep says no
other seat's decision moves because of that. HIGH-VARIANCE is *yes* on the
justification (one board), even though the measured blast radius is one decision.

---

### FIX 4 — a strong takeout double must not hold five cards of THEIR suit
**+11 to +17 IMPs · VERIFIED · 2 changed decisions of 31 firings · HIGH-VARIANCE: yes (two boards)**

Boards 779 (-8 → 0, verified end to end) and 380 (-9 → between -5 and 0).

Lines 3900-3915 (`oc1S_X`) and 3829-3844 (`oc1H_X`).

BEFORE (`oc1S_X`):
```yaml
            - hcp: [17, 40]
              suits: { H: [0, 5] }
              not: { suits: { H: [5, 13] }, evals: { "two_of_top3(H)": [1, 1] } }
```
AFTER:
```yaml
            # The WEAK branch above demands shortness in their suit; the strong
            # branch constrained only the OTHER major and said nothing about
            # spades, so a seventeen-count with AQ976 doubled 1S for takeout and
            # heard partner name hearts.  You do not take out a suit you hold
            # five of.
            - hcp: [17, 40]
              suits: { S: [0, 4], H: [0, 5] }
              not: { suits: { H: [5, 13] }, evals: { "two_of_top3(H)": [1, 1] } }
```
BEFORE (`oc1H_X`):
```yaml
            - hcp: [17, 40]
              suits: { S: [0, 5] }
              not: { suits: { S: [5, 13] }, evals: { "two_of_top3(S)": [1, 1] } }
```
AFTER:
```yaml
            - hcp: [17, 40]
              suits: { S: [0, 5], H: [0, 4] }
              not: { suits: { S: [5, 13] }, evals: { "two_of_top3(S)": [1, 1] } }
```

Verified: board 779 becomes `1S - 1NT - P - 2NT - P - 3NT`, 3NT by North,
**0 IMPs** (was -8). Board 380: West passes 1S (a trap pass with `KQ987` and 16
HCP); the rest of that auction is BEN's, and both plausible landings (1S or 2S
by South) score -5 or 0 against the recorded -9.

**ENDANGERS.** A gate. Whole corpus: `oc1S_X` fires 15 times (-20 IMPs),
`oc1H_X` 16 times (-28). The sweep changes **2 of those 31**, and both are the
losing boards; the other 29 are bit-identical. No hand in 2000 tables doubles 1H
holding five hearts, so the `oc1H_X` half is sibling hygiene with zero measured
effect — include it anyway so the `sibling` lint stays quiet.

---

### FIX 5 — opener must answer the 2NT invitation after a minor opening
**+7 IMPs · VERIFIED · 3 changed decisions of 10,470 · HIGH-VARIANCE: no**

Board 252 (-10 → 0), 454 (0 → +1), 901 (+4 → 0).

`opener_over_invite_2NT_minor` (line 7380) contains **one rule**. Add the rest of
the ladder, after `- id: oim2n_5m_$M$R`'s `establishes:` line (7398):

BEFORE: nothing follows `oim2n_5m_$M$R`.
AFTER:
```yaml
      # The context had ONE rule - the 5m sign-off - so every other hand fell
      # to the generic toolkit, which rebids the minor at the three level and
      # ends the auction.  An invite has to be answered: accept with 14+ (or
      # with a running minor whose tricks are already counted), decline with a
      # minimum.  AKQJ976 opposite an 11-12 invite is nine tricks and bid 3D.
      - id: oim2n_3NT_$M$R
        call: 3NT
        priority: 58
        requires:
          any_of:
            - hcp: [14, 21]
            - suits: { $m: [6, 13] }
              evals: { "suit_quality($m)": [3, 9] }
        shows: "accepting the 11-12 invite"
        establishes: { forcing: sign_off }
      - id: oim2n_pass_$M$R
        call: P
        priority: 50
        requires: { hcp: [10, 13] }
        shows: "declining the invite: minimum opener"
        establishes: { forcing: sign_off }
        negative_inference_weight: soft
```

**ENDANGERS.** Additive rungs, but the context now **defines 3NT** at these
auctions and therefore takes over interpreting it from `uc_nt3` (13-19 balanced,
stoppers). The band is deliberately wider than what it shadows in the direction
that matters — 14+ *or* a running six-card minor, with no shape or stopper
requirement — so it cannot refuse a hand `uc_nt3` would have accepted at these
five patterns. Full sweep: 3 changed decisions. Board 901 is the price: a
15-count with `KQ8764` accepts and 3NT fails by a trick (-4). Board 252 (+10) and
454 (+1) pay for it. Do **not** raise the 14 to 16 to make 901 go away — that is
the threshold-tuning trap, and 14 is the textbook number.

---

### FIX 6 — the quantitative 4NT over 3NT invites on thirty combined points
**+10 IMPs · VERIFIED · 2 changed decisions of 5 firings · HIGH-VARIANCE: no**

Board 695 (-10 → 0); board 338 changes call but not score.

Line 6130.

BEFORE:
```yaml
      - id: qr3_4NT_quant
        call: 4NT
        priority: 39
        requires:
          hcp: [15, 40]
          evals: { rule_of_26_sharp: [30, 99] }
```
AFTER:
```yaml
      - id: qr3_4NT_quant
        call: 4NT
        priority: 39
        requires:
          hcp: [15, 40]
          # Thirty combined is a GAME, not a slam invitation.  At 30 the invite
          # fired five times in 2000 tables and was declined five times
          # (qa_6NT has never fired); 4NT and 3NT score identically on 10, 11
          # and 12 tricks, so the only thing the invite could do was turn a
          # making 3NT into a failing 4NT, which is what it did.  32 is the
          # number that makes "partner needs a little extra for 33" true.
          evals: { rule_of_26_sharp: [32, 99] }
```

**ENDANGERS.** A gate on a rule that fires 5 times in 2000 tables. It subtracts
two of the five: board 695 (which is the whole gain) and board 338 (whose 4NT+1
and 3NT+2 both score 460, so the board is unchanged at +11). The other three
firings still pass the new floor. If the implementer prefers, **deleting
`qr3_4NT_quant` outright measures identically (+10)** — but that removes a
convention DECISIONS authored on purpose, and the accept side (`qa_6NT`) is worth
keeping reachable.

---

### FIX 7 — the keycard ask over partner's game raise must be able to bid the slam
**+14 IMPs · VERIFIED (call-level) · 10 changed decisions of 16 asks · HIGH-VARIANCE: yes**

Board 621 (-12 → 0), plus 389 (-13 → 0), 478 (-13 → 0), 270 (+3 → +5) against
847 (+13 → 0) and 892 (+13 → 0).

This is the largest single pocket I found and also the least certain, so here is
the whole measurement. `gr_rkc_$M` + `gr_rkc_general_$M` fire on **16 tables for
-35 IMPs.** For each one I computed, double-dummy, what the board would have
scored had the auction simply stopped at the game raise:

| board | keycards in hand | actual | stop in game |
|---|---|---|---|
| 846 | 1 | 0 | 0 |
| 916 | 1 | 0 | **+13** |
| 270 | 2 | +3 | +5 |
| 478 | 2 | **-13** | 0 |
| 522 | 2 | 0 | 0 |
| 559 | 2 | -13 | -13 |
| 621 | 2 | **-12** | 0 |
| 892 | 2 | **+13** | 0 |
| 389 | 2 | **-13** | 0 |
| 977 | 2 | 0 | 0 |
| 108 | 3 | 0 | 0 |
| 361 | 3 | 0 | 0 |
| 396 | 3 | -13 | 0 |
| 435 | 3 | 0 | 0 |
| 639 | — | 0 | 0 |
| 847 | 2 | **+13** | 0 |

The arithmetic behind it: after a **4M game raise** the sign-off is **5M**, one
level *above* the contract we already owned. 5M is weakly dominated — on 10, 11
and 12 tricks 4M and 5M score identically or 4M wins, and on exactly ten tricks
4M is +620 and 5M is -100. So the ask can only gain by reaching a making slam.
On this corpus the sign-off branch (nine tables) is **0 wins, -14 IMPs**, and the
slam branch is **2 for 5**.

With two keycards in hand a 5C reply ("1 or 4") means three or six, so two may be
missing and the sign-off at the five level is forced. Three or more makes the
cheap replies usable.

Lines 5904-5936, **both** rules.

BEFORE (`gr_rkc_$M`):
```yaml
        requires:
          suits: { $M: [5, 13] }
          evals: { total_points: [17, 40], controls: [5, 12], rule_of_26_sharp: [30, 99] }
          any_of:
            - evals: { "void(any)": [0, 0] }
            - evals: { "keycards($M)": [3, 5] }
```
AFTER:
```yaml
        requires:
          suits: { $M: [5, 13] }
          # Over a GAME RAISE the sign-off is 5M - one level above the contract
          # we already owned - so the ask is weakly dominated unless it can
          # reach the slam.  With two keycards the cheapest reply (1 or 4) may
          # leave two missing and the five level is forced; three makes every
          # reply usable.  Whole corpus: sign-offs 0 wins / -14 IMPs.
          evals: { total_points: [17, 40], controls: [5, 12], rule_of_26_sharp: [30, 99],
                   "keycards($M)": [3, 5] }
          any_of:
            - evals: { "void(any)": [0, 0] }
            - evals: { "keycards($M)": [3, 5] }
```
BEFORE (`gr_rkc_general_$M`):
```yaml
          evals: { total_points: [17, 40], controls: [4, 12], rule_of_26: [31, 99],
                   "lott_total_trumps(agreed)": [8, 26] }
```
AFTER:
```yaml
          evals: { total_points: [17, 40], controls: [4, 12], rule_of_26: [31, 99],
                   "lott_total_trumps(agreed)": [8, 26], "keycards(agreed)": [3, 5] }
```

**ENDANGERS — read this before applying.** `gr_rkc_general_$M` exists *precisely*
as the superset guard round 6 paid a cycle for: `slam_try_over_game_raise` is a
more specific context than the general keycard one, so it interprets 4NT after
every game raise, and gating it narrows the ask rather than adding one. Gating it
is therefore doing the thing DECISIONS warns against — deliberately, with a
measurement. It removes **10 of the 16 asks**; two of those (847, 892) are
slams that made, worth -26, and four are recovered losses worth +40. The net on
this corpus is **+14**, which is inside one standard deviation of a 1000-board
match. **Measure this fix on its own experiment**, and if the held-out corpus is
flat or negative, revert it rather than the batch. The `keycards >= 4` variant
(which is the only threshold that *guarantees* no five-level sign-off) measures
**+40** on this corpus but removes the ask entirely from every table here, and I
do not recommend shipping a rule that deletes a convention.

---

### FIX 8 — `gst_rkc_$X` kept a three-card trump floor its own raise had dropped
**+3 IMPs · VERIFIED · 1 changed decision of 10,470 · HIGH-VARIANCE: no**

Board 856 (-14 → -11; BEN bid the grand, which this engine cannot).

Lines 5838-5895, all four rules.

BEFORE (shown for hearts):
```yaml
        requires:
          suits: { H: [3, 13] }
          evals: { total_points: [15, 40], controls: [4, 12], rule_of_26_sharp: [31, 99],
                    "lott_total_trumps(H)": [8, 26] }
```
AFTER:
```yaml
        requires:
          # lott_total_trumps is the real fit gate (sharp, eight combined), and
          # uc_raise_H4 already counts a DOUBLETON opposite a shown six-card
          # suit as a fit.  The ask kept a three-card floor its own raise had
          # dropped, so a nineteen-count with two of partner's rebid suit had
          # a game raise fitting 1.00 and an ask fitting 0.35.
          suits: { H: [2, 13] }
          evals: { total_points: [15, 40], controls: [4, 12], rule_of_26_sharp: [31, 99],
                    "lott_total_trumps(H)": [8, 26] }
```
Same edit for `gst_rkc_C`, `gst_rkc_D`, `gst_rkc_S`.

Verified: board 856 becomes `1H P 1S P 2H P 4NT P 5S P 6H`, six hearts making
thirteen. **-11** (was -14).

**ENDANGERS.** A relaxation, so it can only add asks — and the sharp
`lott_total_trumps >= 8` gate still requires a genuine eight-card fit, so the
doubleton is only admitted opposite a *shown* six-card suit. The full sweep
changes **one decision in 10,470**. Interacts with FIX 7: they touch different
rules (`gst_rkc_$X` vs `gr_rkc_$M`), and the merged prototype sweep shows no
interference.

---

### FIX 9 (UNTESTED, lowest priority) — an action over their preemptive jump to game
**~+7 to +10 IMPs on board 585 · UNTESTED · HIGH-VARIANCE: yes**

Board 585 table B: `1C - P - 1D - 2C - P - 4S - P P P`. East holds
`A.J83.Q863.AK542`, 14 HCP opposite a partner who bid diamonds, and passes.
`ch_penalty_X` requires three of their trumps (East has a singleton) and no
five-level raise of partner's minor is offered, so the only candidates are
`cl_pass` (prio 20) and the code fallback double (prio 9). Double-dummy: pass
= -11, **double = -4, 5D = -1**.

The rung wanted is a cooperative double of their jump to game when partner has
bid a suit and we have opening values with shortness in theirs — i.e. what the
code fallback already offers, promoted into data with a real gate. I could not
author and sweep this inside my budget and I will not hand over YAML I have not
measured. Listed so it is not lost.

---

## 6. NON-FINDINGS — hypotheses killed, with the data that killed them

1. **"Answering a takeout double, a four-card major should beat a five-card
   minor."** Relaxing `suit_diff(S,D)`, `suit_diff(S,C)`, `suit_diff(H,D)`,
   `suit_diff(H,C)` from `[0,13]` to `[-1,13]` on the six major pull rungs flips
   both motivating boards (346, 55) correctly and changes **6 of 85** firings.
   Scored double-dummy the six are +1, **-4**, +2, **-2**, +2, +6 — and the last
   two are boards whose auction certainly continues, so the defensible reading is
   **-3**. The gate cannot tell `AQ84` from `T862`. A `suit_quality >= 2.0`
   rider separates all six perfectly, which is exactly why I refuse to propose
   it. KILLED.

2. **`ch_sac_X` should be deleted or gated** (0 wins / 3 losses / -21 IMPs).
   Against the alternative *call* rather than the board margin, the double is
   **+7 net**: board 340 -15 vs -14 passing, board 982 -1 vs -3 passing, board
   120 -5 vs -11 passing. A `quick_tricks_outside` gate matching the rule's own
   documented premise kills all three firings for a net of +4 and would delete a
   rule that beats its alternative. NOTHING-WRONG.

3. **`rr_nt_4NT` should deny a five-card major** (its sibling `rr_nt_3NT` does).
   This is a real inconsistency and I patched it. Board 717 then runs
   `1C-1S-1NT-3S-4S-4NT-5D-5S`; **5S making twelve scores 680 against the 690 the
   4NT it replaced scored.** The fix measures **-1 IMP on its own motivating
   board**, and the rule fires once in 2000 tables. Reported, not shipped.

4. **The cue-bid gate should count controls, not only points** (board 643: three
   aces, six hearts, `cue_H_C` fits 0.41, `cue_H_signoff` fits 1.00). Adding
   `any_of: [{total_points 14+, rule_of_26 28+}, {controls: [6,12]}]` to all six
   major cue rules **does** make the cue fire — and the contract does not change.
   Partner has no second control, signs off honestly in 4H, and the 12-count then
   fails every keycard gate. 4H by North instead of 4H by South: -11 either way.
   NEGATIVE RESULT.

5. **A seven-card suit should have its own competitive rebid rung**
   (`cl_rebid_long3_$X`, board 917: `AQT5432` passing 2S out). Prototyped with
   the same 11-point floor as `cl_rebid_$X3` so partner's model is not weakened:
   the hand still misses on `total_points` (10) and **the prototype does not fix
   its own motivating board**. Lowering the floor to 8 would fix it and would
   also weaken the descriptor for every three-level suit rebid — the same
   mechanism that cost board 218 ten IMPs in the FIX 1 prototype. NEGATIVE
   RESULT.

6. **`uc_raise_H4` is a bad rule** (cluster 3, mean -1.07/table). Its twin
   `uc_raise_S4` is +0.27/table and the two rules are **character-for-character
   identical**. Not a rule defect. NOTHING-WRONG.

7. **`all-pass` is a loss concentration** (cluster 2). 553 tables, mean **-0.69**
   against a corpus-wide table mean of **-0.71**. It is a quarter of the corpus,
   sampled. NOTHING-WRONG.

8. **`uc_nt3` is fixable** (cluster 1). 67 tables, **-61 IMPs** total against a
   cluster headline of 141, across **23 distinct auction families**. Symptom, for
   the fourth round running. NOTHING-WRONG.

9. **`adx_sit` converts too many takeout doubles** (board 740, 3SX making for
   -730). Whole corpus: **25 firings, +16 IMPs, 12 wins / 11 losses.** And on
   board 740 the alternative rule (`adx_pass_min`, fit 1.00) passes too, so the
   call is Pass whichever rule is credited — there is nothing to fix.
   NOTHING-WRONG.

10. **Board 473's missed 6H is a bidding defect.** 19 opposite 6 — **25 combined
    HCP** — and `ob_raise_4$M`'s cap at 24 support points is deliberate (it is
    what lets monsters reach the keycard rules). A double-dummy slam, not a
    biddable one. NOTHING-WRONG.

---

## 7. Interaction check

All eight proposed YAML fixes were merged into one prototype and re-swept over
all 10,470 decisions: **22 changed, every one of them on an expected board, no
interference between fixes.** FIX 1's engine condition is required only by FIX 1.
The one interaction worth naming is FIX 7 × FIX 8: they touch `gr_rkc_$M` and
`gst_rkc_$X` respectively, different contexts and different patterns, and board
717's auction passes through both without changing.

Suggested batching for measurement: **FIX 7 alone** (it is the only one that
subtracts a whole convention branch, and its corpus gain is inside the noise);
everything else together.
