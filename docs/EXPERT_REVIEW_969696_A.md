# Expert review A — clusters 1-10 and the worst 15 singles (seed 969696, -952 IMPs)

## Method note

**Denominator first.** `rule_tables` assigns the whole *board* margin to each attributed
table, so the sum over all 2000 tables is twice the match margin and the honest baseline a
rule must beat is **-0.952 IMPs per attributed table**. Every rule named below was
re-scored across all 2000 tables of `reports/e8_before.jsonl` (winners included) before it
was accused. Four of my ten clusters come out **at or above** that baseline and are
reported as non-findings.

**Mechanical caveat, and it mattered a great deal this round.** The dossier's `rule` field
is the PRIMARY READING — the highest-priority same-call rule — not the rule whose
constraint actually matched. I re-ranked every one of the 21 doubles attributed to
`ch_penalty_X` and found that **seven of them were produced by `ch_negative_X3`**, a rule
one priority band below it. Split by the rule that actually matched, `ch_penalty_X` is at
baseline (-1.00/firing) and `ch_negative_X3` is the worst double in the book
(-4.57/firing). Cluster 4's headline belongs to a rule the dossier never names.

**Everything below was reproduced through `choose_bid` / `rank_at`.** Fixes 1-4 were
prototyped in scratch copies of the YAML and the **entire 10,405-decision corpus was
replayed base-versus-prototype with arbitration disabled** for each, so every "what else
does this touch" number is measured, not asserted; FIX 5 is verified as a hole through
`rank_at` and `context_at` but was not prototyped. The combined prototype of fixes 1-4
(502 contexts / 2238 rules against the shipped 498 / 2182) gives:

* `python3 -m pytest -q` → **693 passed** (identical to baseline);
* `tools/lint_system.py` → `collide 0, gap 0, shape 0, sibling 0, soft 0`; `floor` 218 → 222
  (the four advisory entries are the four expansions of the new context, which carries no
  pass — the same shape as its existing sibling `opener_neg_double_over_raise`);
* `tools/fuzz_decisions.py --n 300 --strict` → byte-identical to baseline (0 crashes,
  the same 2 starved anchored contexts).

**Three prototypes were measured worse and are reported as negative results rather than
shipped** (§NON-FINDINGS 6, 7 and 8).

---

# CLUSTERS

## CLUSTER 1 — `all-pass`, 27 boards, 136 IMPs — **NOTHING-WRONG** (VERIFIED)

Whole corpus: **510 tables, -356 IMPs, mean -0.70** against a -0.952 baseline — above it.
Sliced by board instead of by table the reading is even flatter:

| slice | boards | mean |
|---|---|---|
| a board where one of our tables passed throughout | 500 | **-0.71** |
| a board where we bid at both tables | 500 | **-1.19** |

The all-pass boards are the *better* half of the corpus. This is expected and worth
restating for the record: when our side passes throughout at one table, that board's margin
is decided entirely by our bidding at the *other* table, so the cluster measures nothing
about the passes. DECISIONS has now ruled this family neutral in rounds 5, 7 and 8 with
essentially the same numbers. **No fix, no boards read individually beyond the four the
dossier prints, all of which are in-range defensive passes.**

## CLUSTER 2 — `uc_nt3`, 16 boards, 94 IMPs — **NOTHING-WRONG / symptom, fifth round running** (VERIFIED)

Whole corpus: **47 firings, -56 IMPs, mean -1.19**. Excess over baseline across the whole
corpus is **-11 IMPs**, against a 94-IMP cluster headline. The 47 firings are spread over
**31 distinct three-call auction families**; the worst single is -13 and the median is -1.
It fits 1.00 on nearly every board it loses, because it is the only descriptive bid the
generic toolkit offers once the authored ladder has run out.

DECISIONS records that raising its strength gate measured **+1 IMP over 1000 boards** and
that it has been a symptom for four rounds. This corpus is the fifth. **Do not touch it.**
Its two biggest members are upstream holes already on the open list: board 858 is
`1C - (1NT overcall) - P - 2NT - P - 3NT` where the advance of our own 1NT overcall is
under-authored, and board 790 is `1C - P - 1S - P - 3NT` on AKJ.AT.K5.AT9752 — a hand whose
real problem is that the 6-card club suit has no strong rebid in that seat, not that 3NT is
mis-gated.

## CLUSTER 3 — `rkc5C_signoff`, 6 boards, 68 IMPs — **IMPLEMENTATION-BUG on one board; the rest belongs to the ASK** (VERIFIED)

Whole corpus: **12 tables, -55 IMPs, mean -4.58**. I re-derived the asker's keycard count,
trump queen and fit length for every one:

| board | keycards in hand | trump Q | fit | result |
|---|---|---|---|---|
| 55 | **4** | no | 4+4 | **-13 — signed off holding ALL FIVE keycards** |
| 599 | 3 | no | 3+4 | -13 — one keycard genuinely missing, 7-card fit |
| 413 | 3 | no | 4+4 | -12 — 6H is NOT making; 5H down 1 was already too high |
| 649 | 1 | no | 3+5 | -10 — sign-off correct; the ask was the error |
| 954 | 2 | no | 6+2 | -10 — sign-off correct (two keycards missing) |
| 993 | 2 | no | 5+3 | -10 — sign-off correct |
| 246 | 2 | yes | 3+4 | **+11** — sign-off correct |
| 491/493/535/788/828 | 1-3 | — | — | 0 / +2 / 0 / 0 / 0 |

Only **board 55 is a defect of the continuation**, and it is a clean one. 5C shows *one or
four* keycards. Holding four myself, partner's reply can only be one — four would make
seven — so **every keycard is present** and the hand signs off in 5H anyway. The blocker is
the trump-queen clause that round 7 swept from `rkc5H_slam` onto `rkc5C_slam` and
`rkc5D_slam`. Its premise, stated in the file's own comment, is *"a keycard is already
unaccounted for, so the trump QUEEN cannot be missing as well"* — and that premise is
**false when the count says nothing is unaccounted for**. Unlike 5H, the 5C and 5D replies
say nothing whatever about the queen; it may be opposite. Reproduced: `rkc5C_slam` fits
**0.082** on board 55 and `rkc5C_signoff` (a bare `requires: {}`) fits 1.00. See FIX 1
(VERIFIED, +13, and it fixes board 657 in the 5D twin for another +11).

The other four losses (413, 649, 954, 993, -42 IMPs) are boards where the sign-off is the
correct call and the ask took us from a making 4M to a failing 5M. That is the
keycard-ask-over-a-standing-game problem, and it is the item DECISIONS records as measured
**-17 held-out** when gated. I am not re-proposing a gate; the whole-corpus picture is in
§NON-FINDINGS 1.

## CLUSTER 4 — `ch_penalty_X`, 5 boards, 60 IMPs — **the dossier names the wrong rule. IMPLEMENTATION-BUG in `ch_negative_X3`** (VERIFIED)

`ch_penalty_X` has **priority 38** and `ch_negative_X3` **priority 33**, both defining `X`
in `general_competitive_high`. The higher priority makes the penalty double the *primary
reading* for every three-level double in that context, whatever actually matched. Splitting
the 21 attributed doubles by the rule that actually fitted:

| matching rule | firings | IMPs | mean |
|---|---|---|---|
| `ch_penalty_X` | 14 | **-14** | **-1.00** (baseline) |
| `ch_negative_X3` | **7** | **-32** | **-4.57** |

`ch_penalty_X` is not the problem. Across all our doubles in the corpus classified the same
way, the negative-double family reads: `cl_negative_X1` 13 firings -2, `cl_negative_X2` 9
firings -11, `ch_negative_X3` 7 firings -32 — **29 firings, -45, mean -1.55**.

Two separate mechanisms are at work inside `ch_negative_X3`:

**(a) It measures the wrong suit — an implementation bug with a precedent in this file.**
All three negative-double siblings gate on `"suit_length(their)": [0, 3]`, and
`_resolve_suit("their")` returns `ctx.their_suits[0]`. That list is **not in bidding
order**: `_their_suits` seeds itself from `_shown_suits_of(analysis, [seat.lho, seat.rho])`,
so it enumerates by *seat*, LHO before RHO. Reproduced directly:

```
dealer N, seat S, auction P 1S(E) P 2C(W) P P  ->  their_suits == ['C', 'S']
dealer N, seat S, auction P 1H(E) P 2C(W) P P  ->  their_suits == ['C', 'H']
dealer N, seat S, auction P 1S(E) P 2H(W) P P  ->  their_suits == ['H', 'S']
```

In every one of those the opponents bid the *first* suit at their first turn and it comes
out second. `(their)` therefore means "my LHO's suit", not "their first suit" as the file's
comments (and DECISIONS) say. Board 664 is the consequence: `2H - (2S) - P - (3D) - P -
(3S) - X` with **T762** in the suit being doubled. `suit_length(their)` reads *diamonds*
(AQ, two cards) and the rule fits **1.00**. DECISIONS already fixed exactly this once —
round 4's `standing_suit_length` was added because *"`suit_length(their)` reads their FIRST
suit, so a double of 4H was gated on club length"* — and the three negative doubles were
never swept. This is round 7's named species, a gate given to one rule and not its
siblings. See FIX 2.

**(b) A "negative double" made at a seat that already had a turn, opposite a preempt.**
Boards 169 (`3D(partner preempt) - P - P - X - P - 3S - X`, -12) and 664 (partner opened a
weak 2H, I passed once, -11) and 14 (partner made a weak 3D jump overcall, -13) are not
negative-double positions at all: a negative double is responder's *first* action over an
overcall of partner's opening. `i_have_acted` counts only non-pass calls, so a hand that has
already passed at a prior turn still qualifies. There is no when-condition that expresses
"this is my first turn" or "partner preempted", and `passed_hand` is the wrong tool — it is
true for the perfectly normal `P - 1C - (1S) - X`. FIX 2 removes board 664 only; the
remaining -25 across boards 14 and 169 is diagnosed and **not fixed**, with the exact
missing condition named in §NON-FINDINGS 5.

The four boards in the cluster all end `... X - P` with `adx_sit`/`adx_pass_min` converting.
`adx_sit` itself is **36 firings, -32, mean -0.89 — above baseline**; it is not the culprit
(round 8's reviewer B reached the same conclusion from a different corpus).

## CLUSTER 5 — `uc_raise_S4`, 8 boards, 56 IMPs — **NOTHING-WRONG** (VERIFIED)

| | tables | IMPs | mean |
|---|---|---|---|
| `uc_raise_S4` | 44 | -15 | **-0.34** |
| `uc_raise_H4` | 34 | +30 | **+0.88** |
| **combined family** | **78** | **+15** | **+0.19** |

Both halves are above the -0.952 baseline and the family is comfortably above it. The two
rules are character-for-character identical with the suit letter changed, so the H/S split
is the auctions, not a sibling asymmetry — round 8 established that with the opposite sign
(that corpus had hearts losing and spades winning; this one has it the other way round,
which is exactly what noise looks like). DECISIONS scopes out tuning this family and the
coordinate-descent threshold search measured -0.025 ± 0.062 held-out. **No fix.** The
cluster's worst member, board 107 (-14), is a 4S doubled at the *other* table produced by a
2S cue-raise sequence, not by the game raise itself.

## CLUSTER 6 — `rkc5H_slam`, 4 boards, 50 IMPs — **NOTHING-WRONG** (VERIFIED)

6 tables, -50, 0 wins — which looks damning until the boards are read. 5H is an *exact*
count (two keycards, no trump queen), so the rule is doing arithmetic, not judgement:

* **116 (-13):** asker holds 3 keycards, reply shows 2 → **all five present**; we bid 6S and
  made **thirteen**. BEN bid 7S. The trump queen was with the opponents and fell doubleton.
  Our 6S was the book bid; the grand is scope-excluded ("the system cannot bid a grand
  slam"). **Not a defect.**
* **532 (-13)** and **966 (-13):** four of five keycards and the trump queen in hand — the
  textbook 6. Both are keycard asks over partner's *game raise* (`gr_rkc_S` / `gr_rkc_H`),
  the family DECISIONS has already measured and refused to gate. The continuation is
  blameless.
* **561 (-11):** asker holds 3, reply shows 2 → all five keycards **and** the queen in hand,
  8-card fit. 6H took 11 tricks on 28 combined HCP. Blackwood counts controls, not tricks;
  the ask (`rkc_4NT`) let a 28-count through, not the reply.

Bidding a slam with four of five keycards and the trump queen is not a rule defect, and the
one board where BEN got a 13th trick from a doubleton queen is variance. **No fix.**

## CLUSTER 7 — `uc_nt2`, 7 boards, 47 IMPs — **NOTHING-WRONG / symptom** (VERIFIED)

22 firings, **-55 IMPs, mean -2.50**, spread over **17 distinct three-call auction
families** with per-board margins from -13 to +6. Same species as `uc_nt3` and the same
verdict: it is the only descriptive call on offer when the authored ladder has run out, it
fits 1.00 or 0.8 on almost every board it loses, and no single upstream hole accounts for
more than one member. The biggest, board 671 (-12), is not a 2NT problem at all — we bid a
sound 2NT making 9 while BEN, at the other table, collected 800 from a doubled 2D. **No fix
to the rule.**

## CLUSTER 8 — `rkc5C_slam`, 4 boards, 43 IMPs — **NOTHING-WRONG** (VERIFIED)

8 tables, -43, 0 wins. Read board by board:

* **726 (-11):** four keycards in hand, so all five present; we bid 6S and made **thirteen**.
  BEN bid the grand. Scope-excluded.
* **129 (-10), 164 (-11), 505 (-11):** three keycards in hand and a 1-or-4 reply means the
  reply is 1 and exactly **one** keycard is missing. Bidding six missing one keycard is the
  book bid. All three went down one on a side-suit holding (129 lost a club ruff to a void,
  164 was off AQ of diamonds behind Jx, 505 was off an ace and a diamond). All three asks
  came from a *standing game* — 129 over partner's `cue_S_signoff` (partner had already
  declined slam), 505 over partner's `uc_raise_S4` game raise, 164 over a fallback 2S.

The rule executed correct arithmetic every time. The damage is upstream, in the ask, and
that is the measured-dead item. **No fix to `rkc5C_slam`'s counting**; FIX 1 restructures
its trump-queen clause only, and that change makes it *more* willing to bid, never less.

## CLUSTER 9 — `open_1NT`, 10 boards, 43 IMPs — **NOTHING-WRONG** (VERIFIED)

**37 last-bid tables, -31 IMPs, mean -0.84**; **116 firings anywhere, -28, mean -0.24.**
Both above the -0.952 baseline; the 116-firing number is one of the better families in the
engine. Seven of the ten cluster members are "our 1NT was passed out while BEN's side found
a partscore" — variance, and the opening is 15-17 balanced on every one of them.

The one structural item is board 663 (-10) and it is not the opening: after
`1NT - (2C) - ?` responder has **no context at all**, so a 5-count with six of their suit
passes and the hand is never re-opened. That is the open item DECISIONS already carries
("no context for responder over their overcall of our 1NT"); authoring it shadows
`general_competitive_low` and needs the superset discipline. **Reported, not proposed.**

## CLUSTER 10 — `nx_1m1S_X`, 5 boards, 39 IMPs — **MISSING-AGREEMENT, downstream of the double** (VERIFIED)

Whole corpus: **23 firings, -54 IMPs, mean -2.35** (excess ≈ -32). The double itself is
correct on every losing board — 4+ hearts, 6+ HCP, and on boards 436/467 a **spade void**.
Every loss is the seat *after* it:

* **467 (-9):** `1C - (1S) - X - (3S) - ?` and opener holds A764.**K932**.75.AQ3 — thirteen
  points and four-card support for the major the double promised — with **no rule at all**.
  Reproduced: `ch_pass` fits 1.00, `ch_raise_H4` fits **0.134** (it is gated on
  `rule_of_26 >= 25` and a negative double's shown minimum is six points, so the arithmetic
  can never open), `ch_nt3` 0.028. We passed their 3S and 4H was making twelve tricks at the
  other table. The cause is a plain sibling gap: `opener_neg_double_over_raise` covers the
  **two-level** overcall (`1$m - 2$y - X - bid - ?`) and was never given the one-level twin,
  which is much the commoner auction. See **FIX 3** (VERIFIED, 3 decisions changed
  corpus-wide, all of them a PASS becoming a bid).
* **262 (-15):** `1D - (1S) - X - (4S)` and *both* of us pass. The doubler holds AKQJ7 of
  clubs and 16 HCP in the balancing seat; `general_balancing_high` offers him `pass` (1.00)
  and a second reopening double at 0.004 and nothing else. This is the open item "no action
  over their preemptive jump to game", now with a price on it.
* **436 (-10):** opener **converts** the negative double for penalties with KT82 and 11 HCP
  (`adx_sit`, fit 1.00 — `standing_suit_length` 4, `suit_quality` exactly 1.5, both gates on
  their boundary) and 1S doubled makes eight tricks. Converting a takeout double at the
  ONE level needs a trump stack, not four to the ten; but there is no condition for
  "partner's double was negative", which DECISIONS lists as an open item in its mirror
  direction. `adx_sit` as a family is above baseline (36 firings, -0.89), so I will not gate
  it on one board. **Reported, not proposed.**
* **964 (-12):** the doubler holds **7652** of their spades — four cards in the suit being
  doubled. `nx_1m1S_X` has no spade-length denial; a 4-4 hand doubling 1S is a matter of
  style, and the board's loss is 3D doubled at the other table. Not proposed.

---

# WORST SINGLES 1-15

### 231 (-16) — **MISSING-AGREEMENT (no action over their jump to game after our splinter)** (VERIFIED)
`1H - P - 3S(splinter) - 4S - ?` and opener passes with **A.T976542.A7.AT8** — seven hearts
and a known four-card fit with shortness opposite. `ch_pass` fits 1.00; the only other
candidate is `ch_rebid_H5` at **0.757**. 5H makes eleven at the other table; letting them
play 4S cost 620. Same species as board 262. The auction is game-forcing on our side and the
forcing-pass filter does not fire because *their* bid is at the game level. Authoring
"opener over their jump to game in a game-forcing auction" is a family, not a rung, and it
touches the pass filter; **diagnosed, not proposed.**

### 852 (-15) — **NOTHING-WRONG at the indicted seat; the error is two calls later** (VERIFIED)
`1H - P - 2D(2/1 GF) - 3S - ?`: opener's pass with A74.AT972.74.A75 is normal (partner is
forced to speak again, and he did). The bad call is opener's **4H at index 8**, opposite a
partner who has now bid diamonds twice and holds a heart **void**: `uc_rebid_H4` wants six
hearts and opener has five, and it won the soft-miss lottery. That is the generic "rebid my
own suit" rung, which is stated in shape only and has no partner-shape awareness. One board;
I am not proposing a gate on it.

### 45 (-13), 189 (-13) — **NOTHING-WRONG (grand slam, scope-excluded)** (VERIFIED)
Both are Jacoby-2NT auctions where the count says every keycard is present, we bid the small
slam and made **thirteen**, and BEN bid seven. 45's asker holds a club **void** opposite
partner's shortness reply; 189's asker holds a heart void and the only missing keycard is
the heart ace. The tool that resolves both is a king-ask or a void-showing reply, and
DECISIONS records the 5NT king ask as deliberately skipped ("the constraint language has no
cross-hand arithmetic"). Together with boards 116 and 726 this is **-50 IMPs of grand slams
on this corpus, 5% of the whole match margin** — the largest single item in my slice, and it
is structural, not a rule defect.

### 701 (-13) — **MISSING-AGREEMENT (the 2C opener's slam machinery after a forced pull)** (VERIFIED)
`P - 2C - (3H) - P - P - X - P - 3S - P - ?` and a 21-count with **AJ9753** spades raises
partner's forced 3S to 4S and stops. `uc_doubler_game3_S` is a game raise with no rung above
it. Same ceiling species as round 8's `resp_preempt_*`; the difference is that partner's 3S
here is a *forced* pull showing nothing, so a keycard ask opposite it is not obviously
right. One board. **Diagnosed, not proposed.**

### 733 (-13) — **MISSING-AGREEMENT (a doubled Stayman with nobody to answer it)** (VERIFIED)
`2NT - P - 3C(Stayman) - X - ?` and opener **passes 3C doubled** holding K73.**AK754**.AKQ.Q4.
Reproduced: the only matching context is `general_their_double`, whose rungs are the
six-card runouts (`xd_run_$X`, all fit 0.000 here) and `xd_pass` at 1.00. The 1NT Stayman
ladder has an over-interference twin — `stayman_over_interference`, pattern
`1NT - P - 2C - act - ?` — and **the 2NT one was never given one**: `nt2_stayman_rebid` is
anchored `2NT - P - 3C - P - ?`. This is the exact sibling-gap species. See FIX 5, which I
rank last and mark honestly: on its own board it does **not** recover the IMPs, because the
auction already reaches 4H and BEN's 6H needs a diamond-suit evaluation we do not have.

### 735 (-13) — **NOTHING-WRONG-ish / diagnosed** (VERIFIED)
`2C - 2D - 2S - 3S - ?` with KQ854.AKQJ.AK6.2 (22 HCP). `cue_S_signoff` bids 4S; 6S makes on
25 combined because the nine-card fit and AKQJ do the work. The keycard ask is gated
`rule_of_26_sharp >= 31` and 22 opposite a waiting 2D plus a preference cannot reach it.
Lowering that gate is threshold tuning, which DECISIONS scopes out. **No fix.**

### 766 (-13) — **NOTHING-WRONG** (VERIFIED)
`1H - 1S - 3H - 4H`: responder holds A87432.**Q**.J.AKQT8 — a *singleton queen* of trumps —
and signs off in game opposite a 16-18 jump rebid. BEN cue-bid its way to 6H in a **6-1**
fit and it made twelve. Bidding a slam on a stiff trump queen is not something a rulebook
should learn.

### 815 (-13) — **NOTHING-NEW (the `weakest_their_stopper` item)** (VERIFIED)
`ch_nt3` bids 3NT holding **A76** in their diamonds after they have bid diamonds twice, down
three. This is the confirmed open item: `weakest_their_stopper` has no sharp tolerance, so a
partial stopper scores 0.965 and no stopper 0.835 against a `[0.9, 9]` gate. DECISIONS
measured the one-line repair at **-9 held-out** and reverted it because the seats behind the
deleted notrumps are unauthored. I am not re-proposing it; the seats have to come first.

### 975 (-13) — **NOTHING-WRONG at the indicted rule; the sit is on its boundary** (VERIFIED)
`1C - P - 1S - (2H) - X(support double) - P - ?` and advancer passes the **artificial**
support double with QJT7.**95**.KT954.42. Reproduced: the pass comes from `adx_pass_min`
("no suit worth pulling to and no trump stack", `total_points [0,11]`, fit 1.00) and *not*
from `adx_sit`, which fits 0.001 with two hearts. The pull rung `adx_pull_my_S` wants five
spades and advancer has four, so the seat is genuinely empty. A support double showing
exactly three spades cannot be a penalty double, and the generic pull/sit ladder has no way
to know that — the same missing "partner's double was artificial/negative" condition as
board 436. **Diagnosed, not proposed.**

### 980 (-13) — **IMPLEMENTATION-BUG (the generic new-suit ladder ignores "higher of equal length")** (VERIFIED)
`2C - P - 2D - (3S) - ?` with **5.AKQ93.AT983.AK** — 5-5 in hearts and diamonds, 21 HCP —
and the engine bids **4D**. Reproduced: `ch_new_D4` and `ch_new_H4` are *both* priority 28
and *both* fit 1.00 and *both* blend to 0.784; the tie is broken by file order, which runs
C, D, H, S, so the **lowest** suit always wins a tie. Every generic new-suit rung at the two
level and above is flat in priority within its level (the 1-level rungs are correctly
ordered, majors 30 / minors 25 — the sweep was never carried upward). Round 5 fixed exactly
this in `general_pull_or_sit` ("re-gated by LENGTH rather than suit rank — it was ordering
pulls S>H>D>C"); `ch_new_*`, `cl_new_*` and `uc_new_*` never got the same treatment. See
**FIX 4** (VERIFIED, 4 decisions changed corpus-wide, no PASS introduced).

### 207 (-12) — **NOTHING-NEW** (VERIFIED)
`1C - 1H - 2C - 4NT - P`: `rmr_4NT` is the quantitative invite round 8 authored an accept
context for, and the accept (`total_points >= 15`) declines on Q76.8.KT6.AKT852 — eleven HCP
with six clubs. The making contract is **6C**, which a quantitative 4NT cannot reach anyway.
Moving the accept threshold is threshold tuning. **No fix.**

### 477 (-12) — **NEEDS-EXCEPTION, HIGH-VARIANCE, not proposed** (VERIFIED)
At the other table `w2x_raise4` raises our vulnerable weak 2H to 4H over their takeout
double holding **974.T963.963.KQ5** — five points and four trumps. Ten combined trumps make
it the Law level, but at Both-vulnerable it is a phantom: 4H doubled went three down (-800)
against their 620. The obstruction raises elsewhere in the file carry a non-vulnerable gate;
this one does not. One board of evidence, so I am flagging it rather than proposing it.

### 598 (-12) — **MISSING-AGREEMENT (no five-card rebid of my own suit in competition)** (VERIFIED)
`1D - P - 1H - P - 1S - (2C) - ?` and responder passes with K62.**K8762**.AJ2.94, eleven
points and five hearts, missing a cold 4H. Reproduced: `cl_pass` 1.00; `cl_rebid_H2` wants
**six** cards and fits 0.349; `cl_nt2` fits 0.835 on a hand that is neither balanced nor
holding a club stopper. The free-bid rungs (`cl_free_*`) all carry `i_have_acted: false`, so
the player who bid the suit is excluded from them. This is the "banded by strength, never by
shape" species in the generic competitive ladder. It is a *general* context, so a new rung
there reaches everywhere; DECISIONS records that round 8 killed a seven-card version of this
idea. **Diagnosed, not proposed.**

### 109 (-11) — **MISSING-AGREEMENT (no advance context for a two-level overcall)** (VERIFIED)
`1H - 2D - P - ?` and advancer passes with **T86543**.Q3.A.AJ97 — a six-card major and ten
HCP — missing 4S. Reproduced: the matching context is `general_uncontested_continuation`
(!), `uc_pass` fits 1.00 and `uc_new_S2` fits 0.329. `advance_overcall` is anchored
`1$o - 1$v - P - ?` and covers **one-level major overcalls only**, and even there it has
exactly three rules (raise, cue, 1NT) with no rung for advancer's own suit. Round 8's
reviewer A named the three-rule problem; the two-level gap is new. Authoring a full advance
context is a round of its own. **Diagnosed, not proposed.**

---

# FIX LIST (priority order)

Every fix was applied to a scratch copy and the whole corpus (10,405 decisions) replayed
base-versus-prototype with arbitration disabled. Together they change **21 decisions across
1000 boards**. Combined prototype: 693 tests pass, lints clean, fuzz identical.

---

## FIX 1 — the RKC trump-queen clause must not fire when the count says every keycard is present

**VERIFIED. HIGH-VARIANCE: no (strict superset; 2 decisions changed in 10,405).**
`src/bridgebidder/systems/two_over_one.yaml`, contexts `rkc_continue_after_5C` and
`rkc_continue_after_5D`.

*The bridge, in one sentence:* a 5C reply of "one or four" opposite four keycards in my own
hand can only be one, so all five keycards are present and the trump queen — which the reply
never denied — is not a reason to stop at five.

### 1a — `rkc5C_slam`

BEFORE
```yaml
      - id: rkc5C_slam
        call: 6$A
        priority: 60
        requires:
          all_of:
            - evals: { "keycards(agreed)": [3, 5] }
            # sibling of rkc5H_slam, which already carries this and whose
            # clause was never swept onto the other two replies: a keycard is
            # already unaccounted for, so the trump QUEEN cannot be missing as
            # well unless the fit is long enough to drop it.  A short fit
            # missing the queen is a trump loser, not a finesse.
            - any_of:
                - evals: { "trump_queen(agreed)": [1, 1] }
                - evals: { "lott_total_trumps(agreed)": [9, 26] }
```
AFTER
```yaml
      - id: rkc5C_slam
        call: 6$A
        priority: 60
        requires:
          any_of:
            # FOUR keycards in my own hand: partner's "1 or 4" can only be 1
            # (four would make seven), so EVERY keycard is present.  The 5C
            # reply says nothing about the trump queen, so nothing is known to
            # be missing - it may well be opposite, and it is not a reason to
            # stop at five holding all five keycards.
            - evals: { "keycards(agreed)": [4, 5] }
            # THREE in hand: one keycard IS unaccounted for, so the trump
            # queen must not be missing as well unless the fit is long enough
            # to drop it.  A short fit missing the queen is a trump loser,
            # not a finesse.
            - all_of:
                - evals: { "keycards(agreed)": [3, 3] }
                - any_of:
                    - evals: { "trump_queen(agreed)": [1, 1] }
                    - evals: { "lott_total_trumps(agreed)": [9, 26] }
```

### 1b — `rkc5D_slam` (the same restructuring; 5D's "all five present" branch is the two-in-hand one)

BEFORE
```yaml
        requires:
          all_of:
            - any_of:
                # four in hand: partner's 0-or-3 is 0 and at most one is missing
                - evals: { "keycards(agreed)": [4, 5] }
                # two in hand: opposite shown values the reply can only be 3
                - hcp: [12, 40]
                  evals: { "keycards(agreed)": [2, 2], rule_of_26: [28, 99] }
                # ONE in hand opposite a partner who has SHOWN a big hand:
                # zero is not credible, so the reply is three - four of the
                # five are present and exactly one is missing.
                - hcp: [12, 40]
                  evals: { "keycards(agreed)": [1, 1], rule_of_26: [31, 99] }
            # sibling of rkc5H_slam, which already carries this and whose
            # clause was never swept onto the other two replies: a keycard is
            # already unaccounted for, so the trump QUEEN cannot be missing as
            # well unless the fit is long enough to drop it.  A short fit
            # missing the queen is a trump loser, not a finesse.
            - any_of:
                - evals: { "trump_queen(agreed)": [1, 1] }
                - evals: { "lott_total_trumps(agreed)": [9, 26] }
```
AFTER
```yaml
        requires:
          any_of:
            # TWO in hand opposite shown values: the reply can only be 3, so
            # EVERY keycard is present.  Nothing is unaccounted for, so the
            # trump-queen clause below does not apply - 5D said nothing about
            # the queen and it may well be opposite.
            - hcp: [12, 40]
              evals: { "keycards(agreed)": [2, 2], rule_of_26: [28, 99] }
            # The branches that count to FOUR keycards, not five: one is
            # genuinely unaccounted for, so the trump QUEEN must not be
            # missing as well unless the fit is long enough to drop it.
            - all_of:
                - any_of:
                    # four in hand: partner's 0-or-3 is 0 and one is missing
                    - evals: { "keycards(agreed)": [4, 5] }
                    # ONE in hand opposite a partner who has SHOWN a big hand:
                    # zero is not credible, so the reply is three - four of the
                    # five are present and exactly one is missing.
                    - hcp: [12, 40]
                      evals: { "keycards(agreed)": [1, 1], rule_of_26: [31, 99] }
                - any_of:
                    - evals: { "trump_queen(agreed)": [1, 1] }
                    - evals: { "lott_total_trumps(agreed)": [9, 26] }
```

**Boards / IMPs.** Board **55** (-13): `P 1D P 1H P 2H P 4NT P 5C P` — asker holds
`.AK64.AQJ963.A64` (four keycards), `rkc5C_slam` fitted 0.082 and `rkc5C_signoff` 1.00;
after the fix `choose_bid` returns **6H**, which is what BEN bid at the other table and it
makes twelve. Board **657** (-11): `P 1D P 1S P 1NT P 3S P 4S P 4NT P 5D P` — asker holds
`AJT93.KQ43.AK2.9`, two keycards and 17 HCP opposite a raise, so the 0-or-3 reply is 3 and
all five are present; after the fix **6S**, which BEN bid and which makes thirteen. Both
boards go to 0. **+24 IMPs on the review corpus.**

**ENDANGERS.** This is a *widening*: it can only add slams, never delete one, because the
new constraint is a strict superset of the old (old = `kc>=3 AND queen-clause`; new =
`kc>=4 OR (kc==3 AND queen-clause)`). The whole-corpus replay changes exactly **2 of 10,405
decisions** and both are on currently-losing boards. The risk it takes on is bidding six
with all five keycards, no trump queen and a short fit; that is standard practice and this
corpus is 2/2 on it. Same-call disjunction impact is nil — the widened rule is a six-level
sign-off, so nothing downstream decodes it.

---

## FIX 2 — the three negative doubles must measure the suit they are doubling

**VERIFIED (mechanism + blast radius); contract-level outcome UNMEASURED. HIGH-VARIANCE: no,
but MEASURE ALONE: yes (it both adds and subtracts doubles).**
`src/bridgebidder/systems/two_over_one.yaml`, rules `cl_negative_X1`, `cl_negative_X2`,
`ch_negative_X3` — one identical line in each.

*The bridge, in one sentence:* a negative double promises shortness in **the suit they bid**,
not in whichever of their suits happens to be listed first.

BEFORE (all three rules)
```yaml
          evals: { "suit_length(their)": [0, 3], longest_suit_length: [0, 4] }
```
AFTER (all three rules)
```yaml
          # standing_suit_length, not suit_length(their): each of these rules
          # already gates on `their_last_bid_suit: true`, so the suit being
          # doubled IS the standing suit - while `(their)` resolves to
          # their_suits[0], which is seeded LHO-first and is therefore their
          # OTHER suit as often as not.  Round 4 added standing_suit_length for
          # exactly this bug on a different rule and the three negative doubles
          # were never swept.  Both evaluators carry the same sigma (0.95), so
          # nothing about tolerance changes.
          evals: { standing_suit_length: [0, 3], longest_suit_length: [0, 4] }
```

**Boards / IMPs.** `ch_negative_X3` alone is **7 firings, -32 IMPs, mean -4.57** against a
-0.952 baseline. Motivating board **664** (-11): `2H - (2S) - P - (3D) - P - (3S) - ?`
holding **T762**.A762.AQ.632 — four cards in the suit being doubled and ten HCP — and the
rule fits **1.00** because it is reading the diamonds. After the fix the seat passes.

**ENDANGERS / whole-corpus sweep.** 12 of 10,405 decisions change, on boards carrying **-51
IMPs** net today. Reading them one by one:

* **Clear improvements (7):** 202b, 224a, 471a, 511b, **581b (-11)**, **586a (-10)**,
  **664a (-11)** — every one of these stops doubling while holding **four cards in the suit
  being doubled**, and the replacement is a natural bid or a raise of partner's suit
  (581b becomes a 2S raise on KQ72 opposite partner's spade overcall; 586a becomes 1NT on
  A752 of their spades).
* **Clear regression (1):** 676b (-6) — `1D - (1H overcall by partner) - 1S - ?` now doubles
  with Q985 instead of raising partner's hearts to 2H. The negative double's `any_of` does
  not require the promised major to be *unbid*, so it can promise partner's own suit.
* **Ambiguous (4):** 123a, 521a, 544a, 553a — three passes become doubles and one 1S becomes
  a double.

The direction is favourable but it is not a pure widening, so this belongs in its own paired
measurement. I attempted a stronger version (splitting the three rules per major and gating
each on `unbid_suit`), which fixes the 676b regression but costs two *winning* responsive
doubles; it is reported as a measured negative in §NON-FINDINGS 7.

---

## FIX 3 — opener's answer to a negative double when they raise a ONE-level overcall

**VERIFIED. HIGH-VARIANCE: yes (3 firings; one of them is a phantom).**
`src/bridgebidder/systems/two_over_one.yaml`, new context inserted immediately **before**
`opener_over_nx3_cue`.

*The bridge, in one sentence:* the double promised the other major, so when they raise their
overcall opener bids it — the rule that already exists for a two-level overcall, given its
one-level twin.

BEFORE — nothing. `opener_neg_double_over_raise` is anchored `1$m - 2$y - X - bid - ?`; there
is no context matching `1$m - 1$y - X - bid - ?`, so the seat falls to
`general_competitive_high` whose raises are gated on `rule_of_26 >= 25`, unreachable opposite
a double that shows six points.

AFTER
```yaml
  # SIBLING GAP: opener_neg_double_over_raise above covers the TWO-level
  # overcall ("1$m - 2$y - X - bid - ?") and was never given the ONE-level
  # twin, which is much the commoner auction.  After 1C - (1S) - X - (3S)
  # opener had no rung at all: every generic competitive raise is gated on
  # rule_of_26, and a negative double's shown minimum is six points, so a
  # thirteen-count with four-card support fitted 0.13 and the catch-all pass
  # took the hand.  Same rungs, same gates, one level lower in the pattern.
  - id: opener_neg_double_over_raise_1
    description: "Opener bids the implied major over their raise of a 1-level overcall"
    expand_pairs:
      - { m: C, y: H, oM: S }
      - { m: D, y: H, oM: S }
      - { m: C, y: S, oM: H }
      - { m: D, y: S, oM: H }
    pattern: "1$m - 1$y - X - bid - ?"
    rules:
      - id: onxr1_2_$m$y
        call: "2$oM"
        priority: 60
        when: { cheapest_in_suit: true }
        requires: { suits: { $oM: [4, 13] }, evals: { total_points: [13, 40] } }
        shows: "bidding the major partner's double implied"
        establishes: { forcing: non_forcing, agreed_suit: $oM }
      - id: onxr1_3_$m$y
        call: "3$oM"
        priority: 60
        when: { cheapest_in_suit: true }
        requires: { suits: { $oM: [4, 13] }, evals: { total_points: [13, 40] } }
        shows: "bidding the major partner's double implied"
        establishes: { forcing: non_forcing, agreed_suit: $oM }
      - id: onxr1_4_$m$y
        call: "4$oM"
        priority: 59
        when: { cheapest_in_suit: true }
        requires: { suits: { $oM: [4, 13] }, evals: { total_points: [13, 40] } }
        shows: "bidding the major partner's double implied, at the level they force"
        establishes: { forcing: non_forcing, agreed_suit: $oM }
```

**Boards / IMPs.** Board **467** (-9): `1C - (1S) - X - (3S) - ?` with A764.K932.75.AQ3 now
bids **4H**, which the other table bid and made with twelve tricks; the board goes to 0.
Board **593** (0) turns a pass into a 2H. Board **945** (-2) turns a pass into a 4H opposite
a six-point double on 19 combined HCP — a phantom, worth perhaps -4.

**ENDANGERS.** 3 of 10,405 decisions change and **all three are a PASS becoming a bid**, so
nothing existing is subtracted; the same-call disjunction gains a rung with a 13-point floor,
which is at or above every generic rung it sits beside, so partner's shown minimum for those
calls does not fall. The exposure is the 4-level rung firing opposite a minimum negative
double (board 945). The rungs and gates are copied verbatim from the existing two-level
sibling; if the 13-point floor is wrong it is wrong in both, and that is a separate question
worth its own experiment. Flagged HIGH-VARIANCE on a three-firing population.

---

## FIX 4 — "higher of equal length" in the generic new-suit ladders

**VERIFIED. HIGH-VARIANCE: no (4 decisions changed; no PASS introduced; strictly additive).**
`src/bridgebidder/systems/two_over_one.yaml`, contexts `general_competitive_high`,
`general_competitive_low`, `general_uncontested_continuation`.

*The bridge, in one sentence:* bid your longest suit, and with two of equal length bid the
higher — the maxim the one-level rungs already encode (majors 30, minors 25) and the 2-, 3-,
4- and 5-level rungs never received.

The transformation is mechanical: for every rule whose id matches
`^(ch|cl|uc)_new_(long\d_)?[CDHS]\d?$` at level **2 or above**, add a **twin** rule with the
same call, `when:` and `requires:`, id suffixed `_hi`, priority **+0.5**, and one extra
`suit_diff` gate per other suit — `[1, 13]` against every *higher*-ranking suit and
`[0, 13]` against every *lower*-ranking one ("my longest suit, and the highest of those tied
with it"). The original rung is left completely untouched, so the twin can only ever add a
candidate. 44 twins in all. Worked example:

BEFORE (unchanged, kept)
```yaml
      - id: uc_new_S3
        call: 3S
        priority: 27
        when: { unbid_suit: S, cheapest_in_suit: true }
        requires:
          suits: { S: [5, 13] }
          evals: { total_points: [14, 40], "suit_quality(S)": [1.5, 9] }
        shows: "natural S at the cheapest level: 5+ cards, 14+ points"
        establishes: { forcing: non_forcing }
```
AFTER (new twin, inserted directly below it)
```yaml
      # HIGHER OF EQUAL LENGTH.  The 2-, 3-, 4- and 5-level new-suit rungs are
      # flat in priority within a level, so two suits of equal length both fit
      # 1.00 and file order (C, D, H, S) hands the auction to the LOWEST one:
      # a 21-count 5-5 in hearts and diamonds bid 4D.  Round 5 re-gated
      # general_pull_or_sit by length for the same reason and this ladder was
      # never swept.  Stated as a strict-subset twin at +0.5 priority rather
      # than as a gate on the rung itself, because the higher suit is not
      # always available (they may have bid it) and gating the lower rung
      # directly opened five holes in a corpus replay.
      - id: uc_new_S3_hi
        call: 3S
        priority: 27.5
        when: { unbid_suit: S, cheapest_in_suit: true }
        requires:
          suits: { S: [5, 13] }
          evals: { total_points: [14, 40], "suit_quality(S)": [1.5, 9], "suit_diff(S, C)": [0, 13], "suit_diff(S, D)": [0, 13], "suit_diff(S, H)": [0, 13] }
        shows: "natural S at the cheapest level: 5+ cards, 14+ points (my longest suit, higher of equal length)"
        establishes: { forcing: non_forcing }
```
and, for a middle suit (note the `[1, 13]` against the higher suit):
```yaml
      - id: ch_new_H4_hi
        call: 4H
        priority: 28.5
        when: { unbid_suit: H, cheapest_in_suit: true, partner_has_acted: true }
        requires:
          suits: { H: [5, 13] }
          hcp: [12, 40]
          evals: { total_points: [14, 40], "suit_quality(H)": [1.5, 9], "suit_diff(H, C)": [0, 13], "suit_diff(H, D)": [0, 13], "suit_diff(H, S)": [1, 13] }
        shows: "natural H at the cheapest level: 5+ cards, 14+ points (my longest suit, higher of equal length)"
        establishes: { forcing: non_forcing }
```

**Boards / IMPs.** Four decisions change corpus-wide, every one of them a lower suit becoming
a longer-or-higher one:

| board | hand | before | after | today |
|---|---|---|---|---|
| **980** | 5.AKQ93.AT983.AK (5-5 H/D) | 4D | **4H** | **-13** (the other table bid 4H, making 10) |
| **977** | AKJ95.AK754.4.65 (5-5 S/H) | 3H | **3S** | **-7** (the other table played 4S, making 10) |
| **445** | Q.T.AKJT53.AK865 (6 D, 5 C) | 3C | **3D** | **-6** (the other table played 3D, making 11) |
| **421** | KQJ74.85.AK987.K (5-5 S/D) | 3D | **3S** | **+10** |

**ENDANGERS.** The twin's constraint is a strict subset of the rung it sits above, so no
reading is deleted and the same-call disjunction and partner's shown floor are unchanged;
whenever the twin does not fit, the untouched original still does. The exposure is board
**421**, a currently-winning board where partner has jump-overcalled clubs and the 5-5
diamond half is the one that fits him — the maxim is right and the deal is not. Net expected
review-corpus value **+16**, and the maxim is one sentence of bridge.

---

## FIX 5 — the 2NT Stayman ladder needs its over-interference twin

**VERIFIED (the hole); value on its own board **measured to be zero** — ship on structure,
not on score. HIGH-VARIANCE: no (it can only add candidates).**
`src/bridgebidder/systems/two_over_one.yaml`, new context after `nt2_stayman_rebid`.

BEFORE — nothing. `stayman_over_interference` covers `1NT - P - 2C - act - ?`;
`nt2_stayman_rebid` is anchored `2NT - P - 3C - P - ?`, so a double of our 3C Stayman drops
opener into `general_their_double` and he passes 3C doubled.

AFTER
```yaml
  # The 1NT Stayman ladder has an over-interference twin
  # (stayman_over_interference, "1NT - P - 2C - act - ?") and the 2NT one was
  # never given one, so a DOUBLE of our 3C Stayman left opener in
  # general_their_double, whose only rungs are the six-card runouts and the
  # pass: a 20-count with AK754 passed 3C doubled (board 733).  The double does
  # not change the question Stayman asked.  ANSWERS ONLY - the pass, the
  # redouble and the runouts are left where they are, so this context can only
  # add candidates, never shadow one.
  - id: nt2_stayman_over_interference
    description: "Opener answers 3C Stayman after their interference"
    pattern: "2NT - P - 3C - act - ?"
    rules:
      - id: nt2_stm_i_3H
        call: 3H
        priority: 70
        when: { cheapest_in_suit: true }
        requires: { suits: { H: [4, 5] } }
        shows: "4+ hearts (over interference)"
        establishes: { forcing: non_forcing }
      - id: nt2_stm_i_3S
        call: 3S
        priority: 60
        when: { cheapest_in_suit: true }
        requires: { suits: { S: [4, 5] } }
        shows: "4+ spades, denies 4 hearts (over interference)"
        establishes: { forcing: non_forcing }
      - id: nt2_stm_i_4H
        call: 4H
        priority: 59
        when: { cheapest_in_suit: true }
        requires: { suits: { H: [4, 5] } }
        shows: "4+ hearts (their bid consumed the three level)"
        establishes: { forcing: non_forcing }
      - id: nt2_stm_i_4S
        call: 4S
        priority: 58
        when: { cheapest_in_suit: true }
        requires: { suits: { S: [4, 5] } }
        shows: "4+ spades, denies 4 hearts"
        establishes: { forcing: non_forcing }
      - id: nt2_stm_i_3D
        call: 3D
        priority: 50
        when: { cheapest_in_suit: true }
        requires:
          not: { any_of: [ { suits: { H: [4, 13] } }, { suits: { S: [4, 13] } } ] }
        shows: "no 4-card major (over interference)"
        establishes: { forcing: non_forcing }
```

**Ship it WITH the seat that answers it** (hard constraint 3): `nt2_stayman_placement` is
anchored `2NT - P - 3C - P - 3(D|H|S) - P - ?` and will not match once the double is in the
auction. A parallel context `2NT - P - 3C - act - 3(D|H|S) - P - ?` carrying
`nt2_stm_4H` / `nt2_stm_4S` / `nt2_stm_3NT` verbatim must go in the same change.

**Boards / IMPs.** Board **733** (-13). **I measured this one honestly and it does not pay on
its own board**: the current auction already ends in 4H, and BEN's 6H rests on a
JT9654-opposite-AKQ diamond suit that our evaluation has no way to price. The argument for
the fix is the structure — a 20-count sitting for a double of an artificial 3C is a
catastrophe waiting for a different deal, and the file already carries the identical context
one notrump lower. Rank it last and treat it as a **structure keep**, the same call DECISIONS
made for round 6's singleton-honour fix and round 7's weak-two overcalls.

---

# NON-FINDINGS (hypotheses killed, with the data)

1. **"The keycard ask is the disease — gate it."** The whole ask family on this corpus is
   41 tables and **-168 IMPs**, of which `gr_rkc_S` is 10 tables / -67 with **zero wins**. It
   is tempting and it is dead: DECISIONS records `keycards >= 3` measured at **-17 held-out**
   because `gr_rkc_general_$M` is the round-6 superset guard, so gating the specific rung
   deletes asks that already work rather than adding discipline. I looked for a separator on
   this corpus and did not find one: HCP among the losers reads 13/15/16/16/17/18 and among
   the winners 14/16/17/21; keycards-in-hand reads 2/2/3/3/3 among losers and 2/3/3/4 among
   winners. The honest separator remains a `max_total_points` ceiling channel in the partner
   model, which does not exist. **Not proposed.**

2. **"`ch_penalty_X` doubles too much."** 14 firings where it is the rule that actually
   matched, **-14 IMPs, mean -1.00** against a -0.952 baseline. It is at baseline. The
   cluster's damage belongs to `ch_negative_X3` hiding behind it (see cluster 4). **Killed.**

3. **"`adx_sit` converts too many doubles."** 36 firings, -32, **mean -0.89 — above
   baseline**, and `adx_pass_min` is 8 firings at **+2.38**. Two individual conversions are
   clearly wrong (board 436's negative double, board 975's *support* double) but both need a
   condition the engine does not have ("partner's double was artificial or takeout"), and
   tightening the trump-quality gate would subtract from a family that is paying its way.
   **Killed as a family; the two boards are diagnosed above.**

4. **"`uc_nt2` / `uc_nt3` are over-bidding notrump games."** 22 and 47 firings spread over
   17 and 31 distinct auction families respectively, fitting 1.00 on nearly everything they
   lose, with whole-corpus excesses of -34 and -11 IMPs against cluster headlines of 47 and
   94. Both are symptoms of starved seats upstream, for the fifth round running. **Killed.**

5. **"Add `passed_hand: false` to the negative doubles."** It would block board 14 and, worse,
   it would block the entirely normal `P - 1C - (1S) - X`, because `is_passed_hand` means
   "passed before the auction's opening bid" and that is true of every passed hand whose
   partner then opens. The condition actually wanted is "this is my first turn since my side
   entered the auction", which no `when:` key expresses. Boards 14 (-13), 169 (-12) and 912
   (-8) are left unfixed and the missing condition is named for whoever adds it. **Not
   proposed.**

6. **PROTOTYPE MEASURED WORSE — "order the generic new-suit rungs by suit rank."** Bumping
   the priority of the H rungs by 0.2 and the S rungs by 0.4 across all three generic
   contexts is the obvious way to get "higher of equal length", and it is wrong, because
   priority is hand-blind: the corpus replay changed 7 decisions of which **4 were
   regressions** — 1H became 1S on AJ95.**AQJ92**.Q.T73 (five hearts, four spades), on
   QT976.**KQ8754**.2.2 (six hearts) and on a 4-4 up-the-line hand, and 3C became 3S on
   AKQ52..65.**K98632** (six clubs, five spades). FIX 4 exists in its strict-subset twin form
   precisely because of this measurement.

7. **PROTOTYPE MEASURED WORSE — "gate the lower-suit rungs on `suit_diff >= 1` directly."**
   The gate-on-the-rung version of FIX 4 changed 10 decisions, of which **5 turned a bid into
   a PASS** (boards 552, 581, 725, 746, 870): the higher suit is often unavailable because
   they or we have already bid it, so blocking the lower rung leaves the seat empty and the
   catch-all pass swallows it. This is round 4's lesson ("a fix that changes a whole class
   needs a floor for the whole class") reproduced exactly. Rejected in favour of the additive
   twin.

8. **PROTOTYPE MEASURED WORSE — "split the negative doubles per major and gate on
   `unbid_suit`."** This is the correct reading of the rules' own `shows:` text ("a major
   they have not bid") and it repairs FIX 2's one regression (board 676). Measured, it
   changes 17 decisions and costs two *winning* responsive doubles: board 167 (+9, 3C
   doubled three down becomes a 4H that takes nine tricks) and board 764 (+3). A responsive
   double after partner's overcall is a real call even when I hold length in partner's suit,
   and `unbid_suit` cannot tell the two apart. **Reported, not shipped.**

9. **"Board 116 / 45 / 189 / 726 are slam-bidding defects."** All four are hands where the
   count says every keycard is present, we bid the small slam, and we made **thirteen
   tricks** while BEN bid seven. **-50 IMPs on this corpus, and none of it is a rule defect** —
   it is the grand-slam machinery DECISIONS scopes out. Worth restating with the number
   attached, because it is 5% of the whole match margin and the largest single item in my
   slice.

10. **"Board 866's 5S in a six-card fit means `gst_rkc_$X`'s trump floor is too low."**
    Reproduced: at `2C - 2NT - 3C - 3S - ?` **every** candidate fits ≈0.08 (4NT 0.069, 4S
    0.065, 4C 0.015, 3NT 0.004) and there is no pass, because the auction is a game force.
    The seat is starved, not mis-gated — it is the open item "`2C - 2NT` positive-response
    continuations have no landing ladder", and the 4NT won a lottery by 0.004. Tightening the
    ask would only move the lottery. **Not proposed.**
