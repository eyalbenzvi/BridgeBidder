# Expert review — round 9, seed 969696 — reviewer B

Assignment: clusters 11-20, the last fifteen "worst single boards", and an
independent second opinion on clusters 3, 4 and 6.

---

## 1. Method note

**The honest denominator.** 1000 boards, 2000 attributed tables, board margin
`-952`. Summing the board margin over every attributed table gives
**-1904 IMPs over 2000 tables = -0.952 IMPs per attributed table.** That is the
number every per-rule mean below is compared against. A family at -1.0 is
*average*, not a defect.

**What I verified and how.**

- Every indictment was reproduced through `choose_bid` / `rank_at` before it was
  written down, with `seat_of` checked each time.
- Every suspect rule was re-scored across all 2000 tables with
  `rule_summary` / `fires_summary` *and*, where the dossier attribution looked
  suspicious, by re-ranking the actual decision to find out which rule really
  chose the call (see the warning below).
- **Every proposed fix was prototyped in a scratch copy of the YAML and swept
  across the whole corpus** — I re-asked every one of our 10,405 decisions (or a
  provably-sufficient subset) under both the shipped system and the prototype and
  counted *every* decision that changed, not just the motivating one. Sweeps were
  run with `use_arbitration: False`, because self-play runs fast-path only; one
  early sweep that left arbitration on produced a phantom diff (board 821) that
  vanished when it was turned off.
- Outcomes were scored with the real double-dummy solver (`endplay`, already
  installed) plus the engine's own `contract_score`/`imps`, re-deriving each
  board's recorded margin first as a check that the arithmetic was right.
- A combined prototype carrying eight of the nine fixes was built and swept over
  all 10,405 decisions: **18 decisions change, and 17 of them are the intended
  ones.** The eighteenth (board 65) is analysed below and is a correctness
  improvement worth 0 to -1 IMPs.

**A warning that changed two of my verdicts.** The dossier's `rule` field is the
*primary reading* — the highest-priority same-call rule — not the rule whose
constraint actually matched. On **two of my clusters the headline rule never
fired at all**:

| dossier cluster | rule that actually chose the call | tables | IMPs | mean |
|---|---|---|---|---|
| 4 `ch_penalty_X` | `ch_negative_X3` on 7 of 21 | 7 | -32 | -4.6 |
| 4 `ch_penalty_X` | `ch_penalty_X` itself | 14 | -14 | **-1.00** |
| 11 `ballow_nt2_strong` | `ballow_nt2` (11-12!) on 4 of 7 | 4 | -20 | -5.00 |
| 11 `ballow_nt2_strong` | `ballow_nt2_strong` itself | 3 | -7 | -2.33 |

In both cases the cluster's damage is in the *other* rule, and in both cases the
headline rule is at or near the corpus baseline. Anyone triaging by the dossier
field alone would have gated the wrong rule.

---

## 2. Second opinion: clusters 3, 4 and 6

These are Reviewer A's primary assignment. What follows is my own reading,
formed from the boards and from whole-corpus rescoring. I have not tried to
guess what A concluded.

### CLUSTER 3 — `rkc5C_signoff` (6 boards / 68 IMPs) — **IMPLEMENTATION-BUG**

Whole corpus: `rkc5C_signoff` 12 tables, **-55 IMPs**, 2 wins / 6 losses, mean
-4.58. Its 5D twin `rkc5D_signoff` is 3 tables, -22, mean -7.33.

**The mechanism.** Round 7 swept `rkc5H_slam`'s trump-queen clause onto
`rkc5C_slam` and `rkc5D_slam`. The clause's own comment states its premise:

> *"a keycard is already unaccounted for, so the trump QUEEN cannot be missing
> as well unless the fit is long enough to drop it."*

That premise is **true for the 5H reply** (5H = exactly two keycards *without*
the queen, so a keycard is missing whenever the asker holds fewer than three)
and **false in two branches of the other two replies**:

- 5C shows **1 or 4**. Holding **four myself**, partner's reply can only be 1 —
  **all five keycards are present** and nothing is missing but the queen.
- 5D shows **0 or 3**. Holding **two** opposite shown values (the rule's own
  `keycards 2 + rule_of_26 ≥ 28` branch), the reply can only be 3 — again **all
  five keycards are present**.

In both of those positions the clause vetoes a slam on a card that is a finesse
at worst, and the asker *knows* no keycard is missing.

Verified on the two corpus boards where it bites:

| board | asker | keycards in hand | total known | shipped | correct | DD |
|---|---|---|---|---|---|---|
| 55 | `.AK64.AQJ963.A64` | **4** (5C reply ⇒ partner 1) | **5 of 5** | 5H | 6H | 12 tricks, **+13** |
| 657 | `AJT93.KQ43.AK2.9` | 2, r26 32 (5D reply ⇒ partner 3) | **5 of 5** | 5S | 6S | 13 tricks, **+11** |

Prototype (fix 1 below) re-asked at **all 24 tables in the corpus that reach a
5C or 5D continuation**: exactly those two change. **+24 IMPs, VERIFIED, zero
other movement.** The repair is a strict superset (a branch is added where the
clause's premise is false; nothing is removed).

**The rest of cluster 3 is not this bug and is not fixable.** Boards 413, 599,
649, 954, 993 all sign off correctly by the arithmetic (three or fewer keycards
known present); their loss is upstream — the ask itself, from `gr_rkc_*` /
`oac3_4NT_S` over a raise that had already reached game, so the sign-off is one
level above the contract we owned. That is precisely the family round 8 measured
at **-17 held-out** when gated. I re-tested the one separator nobody has tried
(a floor of two keycards on the *asker*): 8 asks with ≤1 keycard for -25 IMPs,
46 with ≥2 for -167 — the metric is degenerate for quantitative 4NTs and only 3
of the 8 are genuine keycard asks. **No conviction; do not gate the ask.**

### CLUSTER 4 — `ch_penalty_X` (5 boards / 60 IMPs) — **NOTHING-WRONG for the rule**

`ch_penalty_X` fires on 21 tables. Re-ranking each one to find the actual
chooser splits them cleanly:

- **`ch_penalty_X` really chose the double on 14 tables: -14 IMPs, mean -1.00**,
  against a corpus baseline of -0.95. Five of those tables are wins (+15, +8,
  +7, +6, +4). The doubles that *were* left in split 5 beaten / 4 made. **This
  rule is average. It is not the cluster.**
- On the other **7 tables the double was made by `ch_negative_X3`** (the
  three-level negative/responsive double, priority 33) while `ch_penalty_X`
  (priority 38) supplied the *primary reading*: **-32 IMPs, mean -4.6.**

Three of the five dossier boards are in the second group (14, 169, 664 = -36 of
the -60).

**Mechanism, verified on board 14.** South holds `T75.AKJ6.J2.Q862` and doubles
3S. `ch_penalty_X` fits **0.009**; `ch_negative_X3` fits 1.00 and is the rule
that chooses. But `choose_bid`'s explanation reads:

```
shows: 'penalty double of their high contract: defensive tricks and trump length'
source_rule_id: ch_penalty_X
partner_model: hcp [10,11], suit_lengths all [0,13], shown_suits []
```

The four-card major the negative double promised is *gone from the partner
model*, and partner is told the double is for penalties. North, holding a
**singleton spade** and seven diamonds, passes; 3SX makes for -730.

I tried the obvious repair and it did **not** work — see NON-FINDINGS: raising
`ch_negative_X3` above `ch_penalty_X` fixes the reading on all 7 tables and
**changes not one decision**, because advancer's problem is elsewhere.

**The real, mechanical defect behind boards 14 and 169** is in the advance
context: `general_pull_or_sit`'s "pull to my own suit" rungs
(`adx_pull_my_S/H/D/C`) exist **only at the two and three level** — the minors
have a single rung each, written as the literal `3C`/`3D`. Over their **3S** the
diamond bidder has no pull at all, so a seven-card suit with a singleton in their
suit converts a takeout double for penalties. This is the same species
DECISIONS already records for `strong_2C_reopen` ("writes its natural rebids as
literal 3-level calls"). Fix 9 below; **VERIFIED, 161 relevant decisions swept,
3 change, +6 to +13.**

### CLUSTER 6 — `rkc5H_slam` (4 boards / 50 IMPs) — **NOTHING-WRONG**

Whole corpus: 6 tables, -50, 0 wins / 4 losses, mean -8.33. That looks damning
until the boards are read.

I tabulated **all 25 slam bids** made by the RKC continuation family (every
reply, every strain) with the asker's keycards, trump queen, counted fit,
rule_of_26 and the double-dummy result. They split in two:

**(a) Grand-slam misses — 4 boards, -48 IMPs.** Boards 189, 116, 45, 726: *we
bid six and made thirteen; BEN bid seven.* Nothing is wrong with the six-bid.
This is the documented open item "the system cannot bid a grand slam". Board
116 is the cluster's own -13.

**(b) Slams that failed — 6 boards, -69 IMPs.** No separator exists:

| separator | losers | flat/winners |
|---|---|---|
| `rule_of_26` | 31, 32, 31, 30, 33, 36 | 34, 27, 31, 30, 31, 31, 32, 35, … |
| keycards in hand | 2+Q, 2+Q, 3, 3+Q, 3+Q, 3+Q | 2+Q, 2+Q, 3+Q, 4, 3, 2, … |
| counted trumps | **8, 8, 9, 9, 8, 7** | 10, 9, 8, 9, 9, 9, 8, 8, 8, 9, 9, 8, 9 |

Trumps look like a separator. **I tested it and it is a disaster.** Of the 12
slam bids in the corpus that are *flat* (0 IMPs), every one is flat because BEN
bid the identical slam — and four of those (631, 227, 985, 325) sit in an
eight-card fit and **make**, as does the +10 board 425. A `lott ≥ 9` gate would
save four failing slams (~+47) and delete five making ones (~-58). **Killed.**

Points do not separate either: the losers read 31/32 and the flat ones read
31/31. This is round 8's `gr_rkc` finding restated on a different rule, and the
same conclusion follows: the only honest separator is a `max_total_points`
ceiling channel in the partner model, which does not exist. Bidding the same
fifty-percent slam BEN bids is the correct IMP position.

---

## 3. My clusters

### CLUSTER 11 — `ballow_nt2_strong` (5 boards / 37) — **NOTHING-WRONG (mis-attributed)**

Real chooser split (see §1): `ballow_nt2_strong` 3 tables / -7 / mean -2.33
(n=3, one of them a +10 win); `ballow_nt2` — the **11-12** balanced 2NT —
4 tables / -20 / mean -5.00.

Two structural observations, neither of which I am willing to convert into a
gate on this evidence:

1. **`ballow_nt2` can never be the primary reading of 2NT in this context.**
   `ballow_nt2_strong` (17-21, priority 30) outranks it (28) wherever it is a
   candidate, so partner decodes the balancing 2NT as a powerhouse when it can
   be a bare eleven. `rule_summary('ballow_nt2')` returns *"no tables"* even
   though the rule chose the call four times — an attribution artifact worth
   knowing about.
2. **`ballow_nt2_strong` fires on hands that have already described
   themselves.** Boards 198 and 360 are structurally identical: overcall 1NT
   (15-18), pass, then bid 2NT again with the same hand — a bid that shows
   nothing new and costs a level. Its sibling `ballow_nt2_balance` carries
   `side_has_acted: false`; the strong rung carries only `side_has_acted: true`
   and nothing about *me*, though its own `shows` text says "partner still
   unlimited". An `i_have_acted: false` gate would kill all three firings, one of
   which is the +10 win. **Three tables is not a mandate. No fix proposed;
   recorded as an explainability defect.**

The `ballow_nt2` half is real, and its cause is diagnosed under the worst
singles (board 295) as the **competitive-raise seam** — see fix 10.

### CLUSTER 12 — `fallback` (4 boards / 30) — **MISSING-AGREEMENT (two starved seats), partly fixable**

`fallback` as a last bid: 6 tables, -36. But it *fires* on 458 tables for -187,
**mean -0.41 — better than the corpus baseline of -0.95.** The code fallback
layer is not the problem; the four dossier boards are four different starved
seats.

Two of them are the same seat and are fixable in one token. Boards **54** and
**912**: we make a takeout double of their weak two, they raise, partner makes a
**responsive double**, and the doubler has **exactly one candidate — the code
fallback "forced continuation (undiscussed)"**. It invents 4NT (down six) and 4H
on a four-card suit (down four).

```
board 54  P 2S X 4S X P → N holds A9.KQ752.K8.JT76, one candidate: FALLBACK 4NT
board 912 2D X 4D X P   → E holds 743.AJ64.4.AKJ63, one candidate: FALLBACK 4H
```

`aw2r_responsive_X` is marked `forcing: one_round`, so the forcing-pass filter
deletes the pass; every pull rung in `general_pull_or_sit` is gated
`i_have_acted: false` and the doubler *has* acted; `adx_sit` needs four trumps.
Result: zero authored candidates. **This is exactly the repair DECISIONS records
from round 3** ("the double itself is non_forcing now: marking it one-round had
the filter deleting opener's pass and rescuing the opponents"), never swept onto
this rule. Whole corpus: `aw2r_responsive_X` fires 5 times for **-31 IMPs**, and
the doubler's answer is 4NT / 3NT / 3S / 3S / 4H — **never a pass**. Fix 4:
**+19 VERIFIED, 2490 doubled-auction decisions swept, exactly 2 change.**

Boards 409 and 794 are the already-documented `2C - 2D` continuation walk and
the redouble family; not re-opened here.

### CLUSTER 13 — `gf_minor_3NT` (3 boards / 26) — **NEEDS-EXCEPTION**

Whole corpus: 4 tables, -16, mean -4.00 (1 win, 3 losses).

Board 1 is the clean defect. After `1H - 2C - 3C` North holds
`A8.T73.AK7.Q8765` — **three-card support for partner's shown five-card major**,
14 total points. Ranking:

```
3NT  gf_minor_3NT  fit 1.00  prio 37   <- chosen
4H   uc_raise_H4   fit 1.00  prio 32
```

3NT makes **seven** tricks; 4H makes **eleven**, and BEN bid it at the other
table. DECISIONS describes the design as *"generic GF landing rules (3NT without
a fit, 4M with one)"* — but the minor-landing context contains only the 3NT and
5m halves, and the 4M half lives in the generic toolkit five priority points
lower. The maxim "if 3NT is a logical option, bid it" has its caveat one line
below it in every textbook: **nine tricks beat eleven, they do not beat ten in
an eight-card major fit.**

Fix 8 adds the missing rung inside the same context. **VERIFIED: 1638 decisions
whose standing bid is a two/three/four-level minor were swept; exactly one
changes (+11).**

Board 15 is a different, unrepaired problem (opener bids 3NT having already bid
2NT, and `weakest_unshown_stopper` is vacuously 1.00 because all four suits have
been mentioned). Board 186 is a one-level judgment loss; board 875 (+10) is the
maxim working.

### CLUSTER 14 — `gf_game_5C` (2 boards / 26) — **NOTHING-WRONG / known gap**

4 tables, -14, mean -3.50 (one +12, one 0). Board 619 signs off in 5C with 6C
cold — `rule_of_26` reads 27, so `rkc_4NT` (31+) correctly declines to ask; the
missing machinery is a slam floor in `gf_landing_minor`, which is the same
"minor-agreed cue bids" gap DECISIONS already lists. Board 638 bids 5C rather
than 3NT because `weakest_unshown_stopper` reads 0.5 — that is the *conservative*
side of the stopper evaluator whose sharpening measured **-9 held-out** in round
8. Neither is a defect of `gf_game_5C`. No fix.

### CLUSTER 15 — `open_1C` (4 boards / 24) — **NOTHING-WRONG**

`open_1C` fires on **200 tables** for -266, mean **-1.33**. Openings only occur
on hands with values, which are the volatile boards; 0.4 IMPs below a
whole-corpus baseline over 200 firings is not a signal. Every dossier board is a
downstream matter:

- 595: `r1m_pass` on a five-HCP hand with five hearts. That family is **24
  firings, +8 IMPs, mean +0.33 — above baseline.** Pass fits 1.00, 1H fits 0.80,
  blended scores 0.745 vs 0.742. Variance, not a rule.
- 19: advancer holds `T6543` and the natural-overcall rung demands
  `suit_quality ≥ 1.5`. That gate is doing its job.
- 606, 542: unavoidable.

### CLUSTER 16 — `ch_raise_H4` (3 boards / 24) — **NOTHING-WRONG**

5 tables, -24, mean -4.80 — but board 839 carries -12 of it and the raise is
*correct there*: our 4H makes eleven tricks (BEN bid and made it at the other
table); we lost because the opponents ran to 4S and **we had no double**. That
is the documented open item "no takeout or cooperative double above the three
level" — `general_competitive_high` defines `X` only as `ch_penalty_X`, whose
`standing_suit_length ≥ 3` gate reads 0 for the hand with the heart fit.

Remove board 839 and the rule is 4 tables / -12 / mean -3.0 on two one-level
judgment losses (100: 19 total points opposite a shown 6-10, 8 trumps; 479: nine
trumps, the Law's own recommendation) and two flat boards. No fix.

One explainability nit for the implementer: `ch_raise_H4`/`ch_raise_S4` say
`shows: "13+ support points"` while the gate reads `total_points: [11, 40]`.

### CLUSTER 17 — `nt2_3NT` (3 boards / 24) — **NOTHING-WRONG (rule) / MISSING-AGREEMENT (structure)**

6 tables, -11, mean **-1.83** — essentially baseline, and one of the six is a
+13 board. Boards 487 (5 HCP) and 635 (4 HCP) are textbook raises of a 20-21
2NT and simply went down.

Board 636 is structural and not a rule defect: West holds
`3.9.8642.KQJ9876` — a **seven-card club suit with two singletons** — and the
only rungs over a 2NT opening are Stayman, the two major transfers, 3NT, 4NT and
pass. 3NT made eleven; BEN bid the cold **6C**. This is the "no minor transfers
over notrump openings" gap DECISIONS already lists, and a self-contained repair
is not available: 5C scores *worse* than 3NT here (620 vs 660), so only a slam
auction recovers the board, and that means a new convention plus its answering
seat. **Named, not prescribed.**

### CLUSTER 18 — `uc_raise_H4` (6 boards / 23) — **NOTHING-WRONG (confirmed)**

Whole corpus: **34 tables as last bid, +30 IMPs, mean +0.88**; 37 firings, +32,
mean +0.86. Against a corpus baseline of **-0.95**, this family is **1.8 IMPs
per table above average** — one of the profitable families in the engine. Its
twin `uc_raise_S4` is 44 tables at -0.34, also above baseline. Confirmed and
closed.

### CLUSTER 19 — `oim2n_3NT_S2C` (2 boards / 22) — auditing last round's own fix

This context (`opener_over_invite_2NT_minor`) was added in round 8. My verdict:
**NARROW IT BY ONE RUNG — do not revert, do not re-gate the rung the dossier
blames.**

**Whole-corpus numbers first.** The whole context fires 8 times in 2000 tables.
The three `oim2n_3NT_*` rungs: **5 tables, -19 IMPs, mean -3.8**; the pass rungs
3 tables; the `oim2n_5m` sign-off has **never fired**. Every firing, with the
`any_of` branch that matched:

| board | opener | HCP | shape | branch | result | IMPs |
|---|---|---|---|---|---|---|
| 106 | `JT7.8.AQ98.AKJ93` | 15 | 3-1-4-5 | 1 (`hcp 14-21`) | 3NT -1 | -11 |
| 197 | `6.AK73.K.AJT7543` | 15 | 1-4-1-7 | 1 (`hcp 14-21`) | 3NT -2 | -11 |
| 881 | `3.T8.Q972.AKJT43` | 10 | 1-2-4-6 | 2 (running minor) | 3NT -3 | -3 |
| 953 | `K8.2.J94.AKJT762` | 11 | 2-1-3-7 | 2 (running minor) | 3NT = | **+10** |
| 24 | `AT.T72.KQJT86.J7` | 12 | 2-3-6-2 | 2 (running minor) | 3NT -1 | -4 |

**Branch 2 — the rung with no point floor — is the one that looks indefensible
and the one the corpus REFUSES to convict.** It has no HCP requirement at all
(`6+ minor` plus `suit_quality ≥ 3`), and `suit_quality` counts A/K/Q as 1 and
J/T as 0.5, so `AKJT43`, `KQJT86` and `AKJT762` all score exactly 3.0 — the gate
admits far weaker suits than the `AKQJ976` (3.5) the round-8 comment was written
for. On boards 881, 953 and 24 this rung **beats a `oim2n_pass` rung that fits
1.00**, accepting an 11-12 invitation on 10, 11 and 12 HCP — 21, 22 and 23
combined. It is bad bridge. But its three firings are **+3 IMPs net**, and I
measured the repair against double-dummy:

| floor added to branch 2 | 881 | 953 | 24 | net |
|---|---|---|---|---|
| `hcp ≥ 12` | +1..+3 | **-10** | 0 | **-7 to -9** |
| `hcp ≥ 13` | +1..+3 | **-10** | +4 | **-3 to -5** |

**Negative result: gating branch 2 loses IMPs on this corpus. Leave it alone.**
(Recorded so nobody re-derives it.)

**Branch 1 carries the whole loss (-22 of the -25) and one rung is genuinely
mis-banded.** The context's two accept rungs use *different floors*: 3NT accepts
from **14**, the minor game `oim2n_5m` accepts only from **16**, and the pass
declines 10-13. So **14-15 with a six-card minor and a suit wide open has no
choice but notrump.** Board 197 is exactly that hand: 1-4-1-7 with 15 HCP and a
singleton king of diamonds; 5C fits **0.80**, missing the floor by one point, and
3NT wins on priority. 5C makes eleven tricks at the other table.

This is a sibling-band asymmetry inside one context, fixable in two characters,
and explicable in one sentence: *with opening values, a six-card minor and no
stopper, the game is five of the minor, not 3NT.* **Fix 6: 374 decisions over a
standing 2NT swept; exactly one changes; +11 VERIFIED.**

Board 106 is *not* an `oim2n` defect. Responder holds `AQ853.T643.K752.` — 5-4-4-0
with a **void in opener's club suit** and nine points — and **nothing in
`responder_after_minor_rebid` fits above 0.41**; the soft-miss lottery picks
`rmr_2NT` (11-12) on a nine-count. The hole is that responder's own-major rebid
`rmr_2M` demands **six** cards; five and a void in the rebid minor is the
textbook escape and there is no rung for it. Fix 7 (**+11 VERIFIED, 809
decisions swept, one change**).

**Verdict on last round's fix: sound, keep it.** The context did the job it was
authored for (it never once fell through to the generic minor rebid). Its rough
edges are one mis-banded sibling and one starved seat upstream — not a symptom
of the fix itself.

### CLUSTER 20 — `r2ntj_4M` (2 boards / 22) — **MISSING-AGREEMENT (a ceiling)**

2 tables, -22, mean -11.00. Its notrump sibling `r2ntj_3NT` is +10 over 4 tables.

`responder_after_2NT_jump` is **banded by strength and never by shape above the
game jump.** Opposite a shown 18-19 the arithmetic is exact and the file says so,
but both slam rungs are notrump ones: `r2ntj_4NT_quant` requires
`semi_balanced`, `r2ntj_6NT` requires 15+ and five controls. A **six-card major**
gets only `r2ntj_4M` (6-13 HCP) and signs off by construction:

| board | responder | HCP | total pts | `rule_of_26` | bid | available |
|---|---|---|---|---|---|---|
| 219 | `AKQT765.T5..Q753` | 11 | 14 | **32.5** | 4S | 6S/6NT = 12 tricks |
| 615 | `643.AKJ853.T9.A9` | 12 | 14 | **32.5** | 4H | 6H = 13, 6NT = 12 |

Note that a **five**-card major gets the forcing `r2ntj_3$M` and a **six**-card
major does not — backwards, since six trumps is the better slam holding.

**The obvious repair is already dead and I confirmed why.** DECISIONS records
"widening `r2ntj_3$M` to six-card majors (measured worse)". Tracing the
answering seat shows the reason: `opener_choice_after_2NT_jump_3M` contains only
`o2ntj_3NT` (no support) and `o2ntj_4S` (three-card support) — **two sign-offs
and no slam rung** — so on board 219 opener, holding two spades, would answer
3S with **3NT**, strictly worse than 4S. A ladder and its answering context are
one fix; that widening shipped without one.

The route that *does* have an answering seat is the quantitative 4NT, which
`opener_accepts_quant_over_2NT_jump` already answers. Fix 5 adds one rung at
priority 56.5 (above the game jump, below both existing slam rungs).
**VERIFIED: 10 decisions in this context corpus-wide, exactly 2 change, both to
4NT → 6NT, both making: +11 and +10.** Flagged HIGH-VARIANCE — see the strain
caveat in the fix list.

Board **647** (a worst single) is the same species one context over:
`rmr_4$M` in `responder_after_minor_rebid` is the only rung for a six-card major,
`rmr_4NT` requires `semi_balanced`, and `T.AJT953.AK.KQ53` (17 HCP, 1-6-2-4)
jumped to 4H with 6H cold. I did not prototype that twin; it is named in the fix
list as the obvious follow-on.

---

## 4. The worst single boards

| board | IMPs | verdict | what it is |
|---|---|---|---|
| **657** | -11 | IMPLEMENTATION-BUG | RKC 5D queen clause with all five keycards known — **fix 1, +11** |
| **0** | -10 | NEEDS-EXCEPTION | `rp3_D_game` bids 3NT opposite a preempt with a suit wide open — **fix 2, +10** |
| **23** | -10 | MISSING-AGREEMENT | our 2NT overcall of a weak two has no answering seat — **fix 3, +10** |
| **664** | -11 | see cluster 4 | `ch_negative_X3` read as a penalty double; they escaped to 4S |
| **295** | -11 | MISSING-AGREEMENT | the competitive-raise seam — **fix 10** |
| **581** | -11 | NOTHING-WRONG | four-round competitive auction, both tables in the same strain |
| **607** | -11 | MISSING-AGREEMENT | a 17-count that overcalled 2H on five cards has no second bid: every generic own-suit rebid rung requires **six** |
| **270** | -11 | MISSING-AGREEMENT | same species: 5-5 with a **void** in their suit, overcalled 2S, cannot bid 4S over their 4H |
| **540** | -11 | MISSING-AGREEMENT | responder has no raise after their **cue** of our opened major (the cue-raise is unavailable, the natural raise is their suit) |
| **760** | -11 | NOTHING-WRONG | competitive judgment; both tables in hearts/spades at different levels |
| **840** | -11 | MISSING-AGREEMENT | after they double our preemptive jump raise, opener with 12 and a nine-card fit has no LOTT 4S |
| **866** | -11 | NOTHING-WRONG | 5D reply with three keycards in hand: two are missing, the sign-off is right |
| **883** | -11 | MISSING-AGREEMENT | `sandwich_seat` has natural 1- and 2-level overcalls and **no preemptive jump**: `52.AQJ98763..A87` — an **eight**-card suit — bid 2H |
| **889** | -11 | known open item | no action over their preemptive jump to the five level |
| **647** | -11 | MISSING-AGREEMENT | `rmr_4$M` ceiling — see cluster 20 |

The three that are cheap and verified (657, 0, 23) are fixes 1-3. The recurring
species in the rest is worth naming for the implementer, because it is one
sentence: **the generic toolkit lets a five-card suit be bid once and never
again** — `cl_rebid_$X`, `ch_rebid_$X`, `ballow_rebid_$X`, `balhigh_rebid_$X` all
require six cards, while the *new*-suit rungs beside them accept five. A
seventeen-count with a good five-card suit, and a 5-5 hand with a void in their
suit, therefore have no second call. I did not prototype it (it is a 16-rule
class change and needs its own experiment), but boards 270 and 607 are 22 IMPs
of evidence and the repair shape is an `any_of` branch — *five cards with real
extras* — not a relaxation of the six-card rung.

---

## 5. FIX LIST (deduplicated, priority order)

All line numbers are from `src/bridgebidder/systems/two_over_one.yaml` as
shipped. Every "VERIFIED" entry was prototyped in a scratch copy and swept over
the corpus with arbitration off; the sweep size and the number of changed
decisions is stated for each. A combined prototype carrying fixes 1, 3, 5, 6, 7,
8, 9 plus fix 2 was swept over **all 10,405 of our decisions: 18 change.**

---

### FIX 1 — the RKC trump-queen clause must not veto when no keycard is missing

**Rules:** `rkc5C_slam`, `rkc5D_slam` (context `rkc_continue_after_5C`,
`rkc_continue_after_5D`).
**Boards:** 55 (-13), 657 (-11). **IMPs at stake: 24.**
**VERIFIED** — 24 tables reaching a 5C/5D continuation swept; exactly these two
change; 6H makes 12 and 6S makes 13 double-dummy.

BEFORE (`rkc5C_slam`):
```yaml
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
        shows: "all/most keycards present: bidding the small slam"
```
AFTER:
```yaml
        requires:
          any_of:
            # FOUR in hand: partner's "1 or 4" can only be 1, so all five
            # keycards are present and nothing is missing but the queen -
            # a finesse at worst, not a second loser.
            - evals: { "keycards(agreed)": [4, 5] }
            # THREE in hand: partner holds one, so a keycard IS missing and
            # the trump queen cannot be missing as well unless the fit is
            # long enough to drop it.
            - all_of:
                - evals: { "keycards(agreed)": [3, 3] }
                - any_of:
                    - evals: { "trump_queen(agreed)": [1, 1] }
                    - evals: { "lott_total_trumps(agreed)": [9, 26] }
        shows: "all/most keycards present: bidding the small slam"
```

BEFORE (`rkc5D_slam`):
```yaml
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
AFTER:
```yaml
          any_of:
            # TWO in hand opposite shown values: the reply can only be 3, so
            # all five keycards are present and only the queen is unknown.
            - hcp: [12, 40]
              evals: { "keycards(agreed)": [2, 2], rule_of_26: [28, 99] }
            # The two branches below leave exactly one keycard unaccounted
            # for, so the trump QUEEN cannot be missing as well unless the fit
            # is long enough to drop it.
            - all_of:
                - any_of:
                    # four in hand: partner's 0-or-3 is 0, one is missing
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

**ENDANGERS:** nothing removed — both rewrites are provable supersets of the
originals (every conjunction that satisfied the old form satisfies the new one).
It bids six in the "all five keycards, queen unknown" position, which is the
textbook 1430 action. The only cost is variance on the queen: 8-card fits
missing the queen are roughly a finesse. Corpus says 2 for 2.
**`rkc5H_slam` is deliberately untouched** — the 5H reply genuinely denies the
queen, so its clause's premise holds.
**HIGH-VARIANCE: no** (it removes a gate whose premise is provably false, rather
than adding one), though the sample is two boards.

---

### FIX 2 — 3NT opposite a preempt needs the *outside* suits stopped

**Rules:** `rp3_C_game`, `rp3_D_game`, `rp3_C_pass`, `rp3_D_pass`
(contexts `resp_preempt_C`, `resp_preempt_D`).
**Boards:** 0 (-10), 297 (-5), 924 (-3). **IMPs at stake: 24.**
**VERIFIED** — 190 decisions in three-level-preempt auctions swept; exactly
these three change; new contracts score +10, +5, +9.

The rule demands `stopper(partner)` — a stopper in the **one suit that needs
none**, since partner's seven-bagger is the source of tricks — and says nothing
about the three suits the defence is about to lead. Board 0: `AKQ5.Q732.K8.J93`
bid 3NT over 3D holding `J93` of clubs and went **down six** while 3D made ten.

The separator is perfect on the corpus:

| board | `weakest_unshown_stopper` | result |
|---|---|---|
| 0 | **0.5** | 3NT -6 |
| 297 | **0.5** | 3NT -3 |
| 924 | **0.5** | 3NT -3 |
| 381 (the family's only winner, a **4S** rung) | 1.0 | +12 |

`weakest_unshown_stopper` is registered sharp (`_EVAL_S2 = 0.3`), unlike its
sibling `weakest_their_stopper`, so this gate actually gates — that is the
difference from round 8's reverted experiment.

BEFORE (shown for `D`; `C` is identical):
```yaml
      - id: rp3_D_game
        call: 3NT
        priority: 64
        requires: { evals: { total_points: [15, 40] }, features: [ "stopper(partner)" ] }
        shows: "bidding game opposite the preempt"
        establishes: { forcing: sign_off }
      - id: rp3_D_pass
        call: P
        priority: 40
        requires: { evals: { total_points: [0, 14] } }
        shows: "no game opposite a preempt"
```
AFTER:
```yaml
      # The rule demanded a stopper in PARTNER'S suit - the one suit that
      # needs none, since it is the source of tricks - and said nothing about
      # the three suits the opponents are about to lead.  3NT opposite a
      # preempt is nine tricks on a long minor plus stoppers; without them the
      # defence simply cashes (one went down SIX).  The sign-off below gains
      # the matching branch so a 15-count with a hole is not left with nothing
      # that fits.  The 4H/4S siblings keep their gate as written: a stopper
      # argument is about notrump, not about a major-suit game.
      - id: rp3_D_game
        call: 3NT
        priority: 64
        requires:
          evals: { total_points: [15, 40], weakest_unshown_stopper: [0.9, 9] }
          features: [ "stopper(partner)" ]
        shows: "bidding game opposite the preempt: the outside suits are stopped"
        establishes: { forcing: sign_off }
      - id: rp3_D_pass
        call: P
        priority: 40
        requires:
          any_of:
            - evals: { total_points: [0, 14] }
            - evals: { weakest_unshown_stopper: [0, 0.5] }
        shows: "no game opposite a preempt"
```

**ENDANGERS:** this is a **gate**, and it SUBTRACTS every 3NT opposite a
three-level minor preempt where an unshown suit is unstopped. On this corpus that
is all three firings and all three were losses, but the floor matters: without the
matching branch on `rp3_$X_pass` (whose 14-point ceiling would leave a 15-count
with nothing fitting) the seat would be empty and the fallback would invent a
call — round 6's lesson. `rp3_H_game`/`rp3_S_game` are deliberately **not**
changed: they bid 4H/4S, where a stopper argument does not apply. Applying it to
two of four siblings is justified by the *call*, not by the hand.
**HIGH-VARIANCE: yes** (three boards) — but the separation is exact and the
bridge is not arguable.

---

### FIX 3 — the 2NT overcall of a weak two has no answering seat

**New context** `advance_2NT_over_weak_two`.
**Boards:** 23 (-10), 204 (-10), 118 (+1), 948 (-1). **IMPs at stake: 22.**
**VERIFIED** — 210 decisions in `2X - 2NT` auctions swept; exactly four change;
+10, +10, +6, -4.

`vw2_2NT` is a **15-18 balanced notrump overcall with a stopper** and nothing
answers it. Confirmed with `context_at`: after `2S - 2NT - P - ?` the only live
context is `general_uncontested_continuation`, whose catch-all `uc_pass`
(`requires: {}`, priority 18) fits **1.00**. So the overcall was **passed out on
all six of its firings in the corpus** (6 tables, -19 IMPs, mean -3.17) — once
with eleven points opposite the shown fifteen and 3NT making twelve tricks.

Insert immediately before `- id: preemptor_discipline`:
```yaml
  # `vw2_2NT` is a 15-18 balanced notrump overcall of their weak two and NOTHING
  # answered it: the seat fell through to the generic toolkit, whose catch-all
  # pass fits 1.00 at priority 18, so the overcall was passed out on all six of
  # its firings in the review corpus - once with eleven points opposite the
  # shown fifteen and 3NT cold.  An overcall that describes a notrump opening
  # needs the raise that answers it.  Deliberately two rungs and no Stayman:
  # an asking bid would need its own answering seat.
  - id: advance_2NT_over_weak_two
    description: "Advancing partner's natural 2NT overcall of their weak two"
    expand: { X: [D, H, S] }
    pattern: "2$X - 2NT - P - ?"
    rules:
      - id: a2nw_3NT_$X
        call: 3NT
        priority: 55
        requires: { hcp: [8, 40] }
        shows: "game opposite the 15-18 notrump overcall"
        establishes: { forcing: sign_off }
      - id: a2nw_pass_$X
        call: P
        priority: 20
        requires: {}
        shows: "not enough for game opposite 15-18"
        establishes: { forcing: sign_off }
        negative_inference_weight: soft
```

**ENDANGERS:** the new context takes over interpreting `3NT` and `P` at that
node. Superset discipline is satisfied: the 3NT rung (`hcp 8+`, no shape or
stopper requirement) is strictly broader than the `uc_nt3` reading it replaces
(13-19, balanced, stoppers), and the pass rung is `requires: {}` at low priority
so the seat can never be starved. `C` is excluded from the expansion so the
strong-2C tree is untouched.
The floor is the one judgment call: **8** measures **+22** on this corpus, **9**
measures **+16** (it keeps board 948's -4 but gives back board 204's +10).
8 is standard opposite a 15-18 notrump.
**HIGH-VARIANCE: no** (four boards, three up, and the seat is provably starved).

---

### FIX 4 — a responsive double at the four level cannot be one-round forcing

**Rule:** `aw2r_responsive_X`.
**Boards:** 54 (-6), 912 (-8). **IMPs at stake: 19.**
**VERIFIED** — 2490 decisions in auctions containing a double swept; exactly two
change; the doubler passes and 4SX / 4DX both go down.

BEFORE:
```yaml
        shows: "responsive double: 8+ opposite the takeout double, no trump stack"
        establishes: { forcing: one_round }
        convention: responsive_double
```
AFTER:
```yaml
        shows: "responsive double: 8+ opposite the takeout double, no trump stack"
        # Non-forcing, for the reason round 3 recorded about the penalty
        # double: marked one_round, the forcing-pass filter deletes the
        # doubler's pass, and above the three level there is nothing below
        # game to bid - so the seat had ZERO authored candidates and the code
        # fallback invented 4NT (down six) and a four-card 4H (down four).
        establishes: { forcing: non_forcing }
        convention: responsive_double
```

**ENDANGERS:** the doubler may now convert a responsive double instead of being
forced to bid. On the three corpus firings at the **three** level (218, 352, 477)
a discriminating rule still fits and the call is unchanged; the pass only wins
where nothing else fits at all — precisely the case the fallback was papering
over. The negative inference that the responsive double demands an answer is
weakened; that is the price, and it is the same price round 3 paid deliberately.
**HIGH-VARIANCE: no.**

---

### FIX 5 — a six-card major opposite the 18-19 2NT rebid has no slam try

**New rule** `r2ntj_slam_inv_$M` in `responder_after_2NT_jump`.
**Boards:** 219 (-11), 615 (-11). **IMPs at stake: 22.**
**VERIFIED** — all 10 decisions in this context corpus-wide swept; exactly two
change; both reach `4NT - 6NT`, making twelve tricks each (+11, +10).

Insert immediately before `- id: r2ntj_4M`:
```yaml
      # Banded by strength, never by SHAPE: the two rungs above the game jump
      # are notrump ones gated on `semi_balanced`/controls, so a SIX-card major
      # opposite a shown 18-19 - 31+ combined by the same arithmetic the
      # notrump rungs use - had only the fast-arrival 4$M and signed off by
      # construction.  Same invitation, same answering context
      # (opener_accepts_quant_over_2NT_jump); the floor is rule_of_26_sharp 31,
      # which opposite a shown 18 means 13 of my own.
      - id: r2ntj_slam_inv_$M
        call: 4NT
        priority: 56.5
        requires:
          suits: { $M: [6, 13] }
          evals: { rule_of_26_sharp: [31, 99] }
        shows: "quantitative: 31+ combined with a six-card $M, opener bids slam with 19"
        establishes: { forcing: non_forcing }
        alertable: true
```

**ENDANGERS:** it takes 6+-major hands with `rule_of_26_sharp ≥ 31` out of the
4M game jump. Priority 56.5 is chosen deliberately: above `r2ntj_4M` (56), below
`r2ntj_3$M` and `r2ntj_6NT` (57), so the five-card offer and the direct 6NT are
untouched. The floor is `rule_of_26_sharp ≥ 31` — an explicit floor, so
partner's shown minimum for 4NT does not drop (constraint 7).
**The honest caveat: the answer is 6NT, not 6M.** Opener is balanced 18-19 by
definition of the 2NT rebid, so notrump is a defensible strain, and both corpus
boards make twelve tricks in it — but with a 7-2-0-4 hand (board 219) the major
is the safer strain and the existing accept rule cannot know responder holds six.
A companion `q2ntj_6$M` rung would be the complete version and is *not* proposed,
because the 4NT disjunction does not promise the six-card suit.
**HIGH-VARIANCE: yes** (two boards, and a new alertable meaning for 4NT).
**Do not ship the alternative** — routing these hands through a *keycard* 4NT
instead is intercepted by `opener_accepts_quant_over_2NT_jump`, which is the more
specific context; I built that prototype and watched it happen.

---

### FIX 6 — the two accept rungs of `opener_over_invite_2NT_minor` use different floors

**Rule:** `oim2n_5m_$M$R`.
**Board:** 197 (-11). **IMPs at stake: 11.**
**VERIFIED** — 374 decisions over a standing 2NT swept; exactly one changes; 5C
makes eleven tricks (+11).

BEFORE:
```yaml
      - id: oim2n_5m_$M$R
        call: 5$m
        priority: 61
        requires:
          suits: { $m: [6, 13] }
          hcp: [16, 21]
```
AFTER:
```yaml
      - id: oim2n_5m_$M$R
        call: 5$m
        priority: 61
        requires:
          suits: { $m: [6, 13] }
          # Same floor as the 3NT accept beside it.  The context's rungs
          # decline at 10-13 and accept at 14, so a 16 here left 14-15 with a
          # six-card minor and a suit WIDE OPEN no choice but notrump: 1-4-1-7
          # with a stiff king bid 3NT for down two while 5C made eleven.
          hcp: [14, 21]
```

**ENDANGERS:** hands with 14-15 HCP, a six-card minor and **no stopper in an
unshown suit** now play 5m instead of 3NT. That population is exactly one board
in 2000 tables here, and the stopper condition (`weakest_unshown_stopper ≤ 0.5`,
sharp) is what keeps it narrow. It cannot reach a hand that has a stopper.
**HIGH-VARIANCE: no** (a band alignment inside one context, not a new gate).

---

### FIX 7 — responder's own five-card major has no rebid over opener's minor rebid

**Rule:** `rmr_2M` (context `responder_after_minor_rebid`).
**Board:** 106 (-11). **IMPs at stake: 11.**
**VERIFIED** — 809 decisions over a standing 2C/2D swept; exactly one changes;
the auction becomes `1C - 1S - 2C - 2S - 4S` and 4S makes eleven (+11).

BEFORE:
```yaml
      - id: rmr_2M
        call: 2$M
        priority: 52
        requires: { hcp: [6, 10], suits: { $M: [6, 13] } }
        shows: "to play: 6+ $M"
        establishes: { forcing: sign_off }
```
AFTER:
```yaml
      # Banded by strength, never by SHAPE: the only rebid of responder's own
      # major demanded SIX cards, so 5-4-4-0 with a VOID in opener's rebid
      # minor had no call at all - nothing here fitted above 0.41 and the
      # soft-miss lottery invited in notrump on nine points.  Five and a
      # singleton-or-void in the minor is the textbook escape; the floor is
      # unchanged at 6 so partner's shown minimum for 2$M does not move.
      - id: rmr_2M
        call: 2$M
        priority: 52
        requires:
          any_of:
            - hcp: [6, 10]
              suits: { $M: [6, 13] }
            - hcp: [6, 10]
              suits: { $M: [5, 13], $m: [0, 1] }
        shows: "to play: 6+ $M, or five with no fit for the rebid minor"
        establishes: { forcing: sign_off }
```

**ENDANGERS — measured, and worth stating plainly.** Same-call rules merge into a
disjunction, so this **lowers partner's shown length for 2$M from six to five**
wherever the second branch can apply. In the combined sweep that showed up on
exactly one board: **65**, where partner really did hold five hearts
(`J953.87542.AJ2.8` — `rmr_2M` had fired on a soft miss), `lott_total_trumps(H)`
correctly falls from 8 to 7, and our 4H on a **5-2 fit** (down three) becomes
3NT. Delta **0 to -1 IMPs**, and the new reading is the truthful one. The HCP
floor of 6 is unchanged, so nothing partner relies on for strength moves.
**HIGH-VARIANCE: no.**

---

### FIX 8 — the minor GF landing has no "4M with a fit" half

**New rules** `gf_maj4H_$m`, `gf_maj4S_$m` in `gf_landing_minor`.
**Board:** 1 (-11). **IMPs at stake: 11.**
**VERIFIED** — 1638 decisions whose standing bid is a two/three/four-level minor
swept; exactly one changes; 4H makes eleven (+11).

Insert immediately before `- id: gf_minor_3NT`:
```yaml
      # The maxim's own caveat, one line below it in every textbook: nine
      # tricks beat eleven, but they do not beat TEN in an eight-card major
      # fit.  This context had only the 3NT and 5m halves of the documented
      # design ("3NT without a fit, 4M with one"), and 3NT at priority 37
      # outranked the generic toolkit's 4M raise at 32 - so a three-card
      # raise of partner's shown five-card major was overruled by notrump.
      - id: gf_maj4H_$m
        call: 4H
        priority: 38
        when: { standing_bid_strain: [$m] }
        requires:
          evals: { "lott_total_trumps(H)": [8, 26], total_points: [13, 40] }
        shows: "eight combined hearts and the values for game: the major fit beats notrump"
        establishes: { forcing: sign_off, agreed_suit: H }
      - id: gf_maj4S_$m
        call: 4S
        priority: 38
        when: { standing_bid_strain: [$m] }
        requires:
          evals: { "lott_total_trumps(S)": [8, 26], total_points: [13, 40] }
        shows: "eight combined spades and the values for game: the major fit beats notrump"
        establishes: { forcing: sign_off, agreed_suit: S }
```

**ENDANGERS:** it takes 3NT away from hands with a **counted** eight-card major
fit and 13+ support points, in the raise position only (`standing_bid_strain`
keeps it out of the "partner freely chose 3NT" position, exactly as the existing
comment on `gf_minor_3NT` requires). `lott_total_trumps` is sharp, so a seven-card
"fit" cannot sneak in, and the 13-point floor is the same one `uc_raise_H4`
already uses — the very rule that was losing on priority. 1638 decisions swept,
one change.
**HIGH-VARIANCE: no** (one board, but the population is precisely bounded and the
subtracted behaviour is the one the design document says should not exist).

---

### FIX 9 — the "pull to my own suit" ladder stops at the three level

**New rules** `adx_pull_my_D4`, `adx_pull_my_C4`, `adx_pull_my_H4`,
`adx_pull_my_S4` in `general_pull_or_sit`.
**Boards:** 14 (-13), 169 (-12), 870 (-1). **IMPs at stake: 6 to 13** (the wide
range is because the opponents may double the pull; even doubled, 4D-2 beats
3SX-making on board 14).
**VERIFIED** — 161 decisions matching `... - X - P - ?` swept; exactly three
change.

Insert immediately after `adx_pull_my_C`:
```yaml
      # The "my own suit" pull ladder had ONLY a three-level rung, written as
      # the literal 3C/3D, so over their 3S (or any four-level bid) the seat
      # that had actually bid the suit could not pull at all: seven diamonds
      # and a singleton spade converted a takeout double of 3S for penalties
      # and it made.  `cheapest_in_suit` keeps exactly one of the two rungs
      # live at a time, so this can only fill a hole.
      - id: adx_pull_my_D4
        call: 4D
        priority: 58.5
        when: { my_suit: D, cheapest_in_suit: true, their_last_bid_suit: true }
        requires: { suits: { D: [5, 13] } }
        shows: "pulling partner's double back to my own suit"
        establishes: { forcing: non_forcing }
      - id: adx_pull_my_C4
        call: 4C
        priority: 58.5
        when: { my_suit: C, cheapest_in_suit: true, their_last_bid_suit: true }
        requires: { suits: { C: [5, 13] } }
        shows: "pulling partner's double back to my own suit"
        establishes: { forcing: non_forcing }
      - id: adx_pull_my_H4
        call: 4H
        priority: 58.5
        when: { my_suit: H, cheapest_in_suit: true, their_last_bid_suit: true }
        requires: { suits: { H: [5, 13] } }
        shows: "pulling partner's double back to my own suit"
        establishes: { forcing: non_forcing }
      - id: adx_pull_my_S4
        call: 4S
        priority: 58.5
        when: { my_suit: S, cheapest_in_suit: true, their_last_bid_suit: true }
        requires: { suits: { S: [5, 13] } }
        shows: "pulling partner's double back to my own suit"
        establishes: { forcing: non_forcing }
```

**ENDANGERS:** pulling at the **four** level is a bigger commitment than at the
three, and the file's own open item stands — *there is still no condition for
"partner's double was PENALTY"*, so these rungs will pull a business double.
`adx_sit` (priority 61) still outranks them, so a real trump stack still sits.
The gates are copied **verbatim** from the three-level twins so the ladder can
only be a superset of itself; giving the four-level rungs an extra shortness gate
its three-level twin lacks would create precisely the sibling asymmetry this
project keeps finding.
**HIGH-VARIANCE: no** (three boards, all improved, and the seat was demonstrably
empty).

---

### FIX 10 — the competitive-raise seam at 11-13 support points — **MEASURE THIS ONE ALONE**

**Rules:** the sixteen `{cl,ch,ballow,balhigh}_raise_{C,D,H,S}2` rungs.
**Boards:** 295 (-11), 832 (-6), 815 (-13), 598 (-12), 676 (-6). **UNTESTED for
score** (the call is verified; the resulting contracts are not).

**The diagnosis is solid.** All four generic competitive families band their
raises 6-9 at the two level (`cl_raise_H2`/`cl_raise_S2` alone read 6-10, from
round 4's seam fix, never swept to the other fourteen) and 10+ at the three
level — but **every three-level raise rung carries `cheapest_in_suit: true`, so
whenever the two-level raise is legal the three-level one is not offered at
all.** A hand with 11-13 support points therefore has **no raise**. Verified on
board 295: South holds `Q986.AJ82.AT6.86`, has doubled 1C for takeout, partner
has advanced 1S, RHO has bid 2H — four-card support, thirteen points, and
`cl_raise_S2` fits **0.409** because it caps at 10 while `cl_raise_S3` is not
`cheapest_in_suit`. South passes; BEN's side bids and makes 4S.

Candidate patch (widen the ceiling only; the 6-point floor is untouched, so
partner's shown minimum does not move):
```yaml
          evals: { total_points: [6, 12], "lott_total_trumps(S)": [7, 26] }
```
applied to all sixteen two-level raise rungs.

**Measured behaviour: 15 of 10,405 decisions change.** Eleven are a pass becoming
a raise, and the ones I could read are right (295 → 2S, 832 → 2S, 815 → 2D with
QJT9 and twelve points opposite partner's diamond overcall, 598 → 2S, 676 → 2S).
Two look wrong (791: a raise on `T72` where a five-card diamond suit was being
shown; 222: 1NT becoming 2C). I could not score the downstream contracts without
a match run.

**ENDANGERS:** the two-level raise stops distinguishing a 7-count from a
12-count, which is exactly what the three-level rung was for. The *better* repair
is to make the jump raise reachable rather than to widen the simple one — and I
tried that and it failed; see NON-FINDINGS.
**HIGH-VARIANCE: yes. Give it its own held-out measurement.**

---

### Named but not prescribed

- **`rmr_4$M`'s ceiling** (board 647, -11): the exact twin of fix 5 one context
  over. `responder_after_minor_rebid` gives a six-card major only the 4M game
  jump; `rmr_4NT` requires `semi_balanced`, and `T.AJT953.AK.KQ53` (1-6-2-4,
  17 HCP) is not. The answering context `rmrq_*` already exists (it was authored
  last round), so the same one-rung shape applies. Not prototyped.
- **The five-card suit that can only be bid once** (boards 270, 607; 22 IMPs):
  `cl_rebid_$X`, `ch_rebid_$X`, `ballow_rebid_$X`, `balhigh_rebid_$X` all demand
  six cards while the new-suit rungs beside them accept five, so a 17-count that
  overcalled on a good five-bagger, and a 5-5 hand with a **void** in their suit,
  have no second call. Repair shape: an `any_of` branch for five cards with real
  extras, not a relaxation of the six-card rung. 16 rules; its own experiment.
- **No preemptive jump in the sandwich seat** (board 883, -11): `sandwich_seat`
  has 1- and 2-level natural overcalls and a takeout double; `52.AQJ98763..A87`
  — an **eight**-card suit — bid 2H.
- **No double above the three level** (boards 839, 889): already on the DECISIONS
  open list; two more boards of evidence.

---

## 6. NON-FINDINGS — hypotheses I killed, with the data

1. **A point floor on `oim2n_3NT`'s "running minor" branch — measured NEGATIVE.**
   The rung genuinely has no HCP requirement and accepts an 11-12 invitation on
   ten points. Scored double-dummy against the alternative call: a floor of 12
   nets **-7 to -9**, a floor of 13 nets **-3 to -5**, because it turns board
   953's **+10** into a flat. Three firings, +3 net as shipped. Do not gate it.

2. **A trump-count gate on the RKC slam rules — measured NEGATIVE.** `lott ≥ 9`
   separates the six failing slams from the flat ones on this corpus, but the
   flat boards are flat *because BEN bid the same slam*: boards 631, 227, 985 and
   325 sit in eight-card fits and **make**, and board 425 (+10) does too. The
   gate saves ~+47 and deletes ~-58. Round 8's `gr_rkc` conclusion holds: no
   honest separator exists in HCP, in keycards, or in trumps.

3. **Raising `ch_negative_X3` above `ch_penalty_X` — measured NEUTRAL.** The
   diagnosis is right (the negative double is announced to partner as a penalty
   double, with the promised four-card major erased from the partner model) and
   the priority swap fixes the reading on all seven affected tables — and
   **changes not one decision**, because advancer's problem is the missing
   four-level pull, not the label. Nothing between priority 33 and 38 exists in
   that context, so the swap can never change a *call*; it is an explainability
   repair worth zero IMPs. Ship it or don't; do not expect a number.

4. **Making the jump raise reachable (removing `cheapest_in_suit` from the
   sixteen level-3 raise rungs) — measured WRONG.** 22 of 10,405 decisions
   change and several are indefensible bridge: board 81, holding
   `4.QJT743.4.AK942`, bids **3C** (a jump raise of partner's clubs) instead of
   showing the six-card heart suit at the one level, because priority 31 outranks
   the natural 1-level bid at 26; board 791 raises to 3H on `T72`; board 941 bids
   3D on a hand that should pass. The seam is real (fix 10) but this is not the
   way to close it.

5. **`uc_raise_H4` is above baseline.** 34 tables as last bid, **+30 IMPs, mean
   +0.88** against a corpus baseline of **-0.95**. Its twin `uc_raise_S4` is
   -0.34 over 44 tables, also above baseline. Confirmed with the denominator, as
   briefed; no further budget spent.

6. **`ch_penalty_X` is not the cluster-4 defect.** Restricted to the 14 tables
   where it actually chose the call: **-14 IMPs, mean -1.00** against a baseline
   of -0.95, with five winning tables including a +15. The doubles that were left
   in were beaten five times and made four.

7. **`open_1C` is not a defect.** 200 firings, mean -1.33 on hands that by
   definition have opening values. Its most-blamed downstream rule, `r1m_pass`,
   is **24 firings at +0.33 — above baseline**.

8. **`nt2_3NT` is at baseline.** 6 tables, -11, mean -1.83, including a +13. The
   one recoverable board (636) needs a minor-suit convention over 2NT plus its
   answering seat; a natural 5m sign-off would score *worse* than the 3NT it
   replaces (620 vs 660), so the cheap version is not merely unproven, it is
   wrong.

9. **`fallback` is not a defect.** It fires on 458 tables at mean **-0.41**,
   better than the corpus baseline. Every dossier board under it is a starved
   seat somewhere else.

10. **A keycard floor on the 4NT asker — no conviction.** I tabulated all 54 of
    our 4NT bids by `keycards(agreed)`: 8 with ≤1 (-25 IMPs) against 46 with ≥2
    (-167). Only three of the eight are genuine keycard asks (the rest are
    quantitative 4NTs where the evaluator reads a meaningless 1), and those three
    are -10 / 0 / 0. Not enough to gate anything.

11. **Widening `r2ntj_3$M` to six-card majors** was already killed by DECISIONS;
    I confirmed **why**, which is worth recording: its answering context
    `opener_choice_after_2NT_jump_3M` contains only `o2ntj_3NT` and `o2ntj_4S`,
    two sign-offs and no slam rung, so on board 219 opener (holding two spades)
    answers 3S with **3NT** — strictly worse than the 4S the widening replaced.
    The widening shipped without the seat that answers it.

12. **An `i_have_acted: false` gate on `ballow_nt2_strong`** — declined. It is
    the right bridge (boards 198 and 360 are the same hand bidding 1NT and then
    2NT again, showing nothing new), but the rule's three firings are +10, -10,
    -7 and the gate kills all three including the winner. Three tables is not a
    mandate.
