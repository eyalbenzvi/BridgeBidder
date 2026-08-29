# Expert review B — CATEGORIES, the uncontested half + second opinion (seed 242424, -804 IMPs)

## 1. Method note

**Primary set.** `reports/ben_audit_242424.jsonl`, filtered to
`first_divergence == true and ben_conf >= 0.80` = **278 rows, -1657 IMPs**. Split by
whether either opponent had made a non-pass call *before* our decision (computed from
`full_auction[:index]`, not the `auction` field, which writes the literal string
`(open)` for an empty auction — that off-by-one is worth knowing about):

| | rows | IMPs |
|---|---|---|
| opponents had already acted (reviewer A) | 179 | -1020 |
| **our side's auction still uncontested (mine)** | **99** | **-637** |
| ...of which nobody had bid yet (opening decisions) | 35 | -194 |
| ...of which our side had bid (constructive) | 64 | -443 |

**Denominators.** Every rule named below was re-scored across all 2000 tables of
`reports/e10_before.jsonl` (winners included) with `fires_summary`, and I quote a 95%
confidence interval against the corpus mean of **-0.804 IMPs per attributed table**.
Several headline families turn out to contain -0.804 in their interval and are reported
as non-findings.

**Verification.** Every VERIFIED item was prototyped in a scratch copy of the YAML
(`system_path` is a first-class `choose_bid` argument) and then the **whole 10,300-decision
corpus was replayed base-vs-prototype with arbitration disabled**, so the "what else does
this touch" column is measured, not asserted. All six prototypes lint identically to the
shipped system (`floor 222, gap 0, shape 0, sibling 0, soft 0`) and load clean.

**Mechanical facts I had to establish before I could reason, all reproduced:**

- `open_pass` at fit 1.000 / priority 20 scores **0.760**. Any opening candidate scoring
  below 0.760 loses to it. A gate missed by one point gives fit 0.800 → score 0.716 → pass.
  That is why every hole in the opening ladder is a pass and not a bad bid.
- `rule_of_26` does **not** become meaningless opposite an unlimited partner. Reading
  `evaluators.py`: `partner_mid = (floor + min(max(pmax, floor), floor+4)) / 2`, so with
  `partner_max_hcp = 40` it collapses to `floor + 2`. It becomes an **own-points test
  wearing a combined-values name** — an explainability defect, not a numeric one. (See
  NON-FINDING N1.)
- `lott_total_trumps` reads `partner_min_length`, which is 6 after a weak two. It is the
  correct fit test opposite any shown six-card suit, and the generic raises already use it.
- Contexts are additive but **per-call**: `make_setup` builds `covered` from each matching
  context in specificity/file order and skips a call an earlier context already defines.
  So a *new context* with the same pattern shadows or is shadowed. A *new rung inside an
  existing context* always competes. Every fix below is a new rung inside an existing
  context, for that reason.

---

## 2. THE CATEGORIES

Ordered by expected IMPs.

---

### CATEGORY 1 — **"Contested" is a property of the auction, not of the last call.** The generic toolkit is dispatched on what RHO just did.

**The bridge, in one sentence.** An auction in which the opponents have bid is a
competitive auction for the rest of its life, whether or not the last thing RHO did was
pass — but the engine files it as constructive the moment RHO passes.

**Detection.** `general_uncontested_continuation` — described in the file as *"General
constructive agreements in an uncontested auction"* — has `pattern: "... - P - ?"`. That
pattern means **"RHO's last call was a pass"**, not "the auction is uncontested". Its
sibling `general_competitive_low` has `pattern: "... - bid<3C - ?"`, i.e. "RHO just bid".
So the toolkit is chosen by RHO's last call alone.

Traced, same hand, same auction, one opponent call different:

```
1H (1S) 2H     - ?   ->  contexts: ['general_competitive_low', 'general_slam_try']
1H (1S) 2H (P) - ?   ->  contexts: ['general_uncontested_continuation', 'general_slam_try']
```

The only thing that changed is that the opponent passed. The competitive toolkit — with
its Law rungs, its `their_fit` gate, its obstruction rungs — becomes unreachable, and the
constructive toolkit takes over: `rule_of_26 >= 25` combined-values tests, `total_points`
floors of 10/14 on a new suit, a notrump ladder whose stopper gate the file itself
describes as *"vacuously satisfied in uncontested auctions"*, and finally `uc_pass`
(`requires: {}`, priority 18).

**Whole-corpus measurement** (2000 tables of `e10_before`, each table counted once per
category, `is_competitive` read from the live `EvalContext` at the decision):

| a `uc_*` rule decided our call | tables | IMPs | mean | 95% CI |
|---|---|---|---|---|
| in a **COMPETITIVE** auction | **465** | -531 | **-1.14** | [-1.57, -0.72] |
| in a genuinely uncontested auction | 126 | -84 | **-0.67** | [-1.58, +0.24] |

and for its catch-all alone:

| `uc_pass` fired | tables | IMPs | mean | 95% CI |
|---|---|---|---|---|
| all | 431 | -573 | -1.33 | [-1.76, -0.90] |
| `is_competitive = true` | **370 (86%)** | -506 | **-1.37** | [-1.82, -0.92] |
| `is_competitive = false` | 61 | -67 | -1.10 | [-2.40, +0.21] |

Read that twice. **The "uncontested continuation" toolkit is doing a competitive job on
79% of the tables it touches, and that is the only slice whose confidence interval
excludes the corpus mean.** On the job it was written for it is *better* than baseline
(-0.67). Excess loss on the misapplied slice ≈ **-156 IMPs over the corpus** (465 ×
(1.14 - 0.804)); on `uc_pass` alone ≈ **-209 IMPs**.

This is the board-862 diagnosis, generalised: *the missing thing is not a rule, it is a
name for what kind of auction this is.* Sample firings (all `uc_pass`, all with an
opponent bid in the auction): 516a `1C (1D) 1H (P)` -12; 922b `(2H) 3C (P)` -11; 500a
`1S (2S) 3S (P)` -10; 410b `(3D) 3S (P)` -10; 923b `1D (P) 1S (2C) X (P) 2S (P)` -10.

**Why the audit does not show this.** `uc_pass` appears in the confident first-divergence
list exactly **once** (968b, -1 IMP). A downstream pass is almost never the *first*
divergence, so the audit's ranking cannot see the largest single categorization defect in
the engine. That is a methodological finding in its own right and belongs in
`ROUND_METHOD.md`: **first-divergence ranking is blind to defects that only ever occur
late in an auction.**

**What changes once it is recognised.** The competitive rungs must be reachable when the
auction is competitive and RHO happened to pass. The DSL now expresses the predicate:
rule-level `when: { is_competitive: true }`.

The safe shape is **new rungs inside `general_uncontested_continuation`**, not a new
context (a second context with `pattern: "... - P - ?"` either shadows the existing one or
is shadowed by it, per the `covered` mechanism above — constraint 2's trap).

**Exact YAML (seed rung, the Law at the four level — mirror of `cl_raise_lott4_$M`):**

before — `general_uncontested_continuation` has only the combined-values raise:

```yaml
      - id: uc_raise_S4
        call: 4S
        priority: 32
        when: { partner_suit: S }
        requires:
          suits: { S: [2, 13] }
          evals: { total_points: [11, 40], rule_of_26: [25, 99], "lott_total_trumps(S)": [8, 26] }
```

after — add, immediately above `uc_pass` (H twin identical):

```yaml
      - id: uc_raise_lott4_H
        call: 4H
        priority: 32
        when: { partner_suit: H, is_competitive: true }
        requires:
          suits: { H: [4, 13] }
          evals: { "lott_total_trumps(H)": [10, 26], total_points: [11, 40] }
        shows: "the Law at the four level: ten-plus combined trumps in a contested auction - the four level is right on shape, not on combined points"
        establishes: { forcing: non_forcing, agreed_suit: H }
      - id: uc_raise_lott4_S
        call: 4S
        priority: 32
        when: { partner_suit: S, is_competitive: true }
        requires:
          suits: { S: [4, 13] }
          evals: { "lott_total_trumps(S)": [10, 26], total_points: [11, 40] }
        shows: "the Law at the four level: ten-plus combined trumps in a contested auction - the four level is right on shape, not on combined points"
        establishes: { forcing: non_forcing, agreed_suit: S }
```

The 11-point floor matches `uc_raise_S4`, so partner's shown minimum for 4M does not move
(constraint 7). No `cheapest_in_suit` — a four-level raise is a jump (constraint 8).

**Evidence / VERIFIED.** Whole-corpus replay: **2 tables of 10,355 decisions change**
(47b `P 1C 1H P 2C X 2H P`, currently -10, pass → 4H; 363b, currently +6, pass → 4H).
Lints identically. **The seed rung is VERIFIED and worth little on its own** — that is
the honest result. The category's value is the diagnosis and the port; one rung out of a
twenty-rung toolkit recovers one rung's worth.

**ENDANGERS.** The seed rung endangers one +6 board. The *port* — carrying the whole
`general_competitive_low` rung set into this context under `is_competitive: true` — is a
large behavioural change over 465 tables and MUST be measured as its own experiment,
decomposed (round 11's lesson). Do not bundle it.

**HIGH-VARIANCE: yes** for the port. No for the seed rung.

**Cheaper alternative worth costing first:** allow `is_competitive` as a **context-level**
`when` key and give `general_competitive_low/high` a second pattern `... - bid - P - ?`.
That reaches the same population without duplicating rules. It needs a DSL change; see
§4.

---

### CATEGORY 2 — **A preempt is a SHAPE bid and every gate on it is a strength or quality gate.** Seven cards with no opening bid available is the worst-performing population in the whole opening decision.

**The bridge, in one sentence.** Seven of them *is* the suit quality and *is* the reason
to bid; a preempt that needs five high-card points and two of the top three is not a
preempt, it is an opening bid with a long suit.

**Detection.** Opening decision (`opening_seat: [1,2,3]`), `longest_suit_length >= 7`, and
no opening rung fits. Mechanically the hole is exact:

- `open_weak_2$X` demands `suits: { $X: [6, 6] }` — **exactly six**.
- `open_3$X_nv` demands `hcp: [3, 9]` + `suit_quality >= 1.0`; `open_3$X_vul` demands
  `hcp: [5, 9]` + `suit_quality >= 1.5`; both veto on a side major of 4+ cards with
  `suit_quality >= 1.5`.
- `open_4H/4S` demand eight cards.

So with seven cards there is **no rung at all** if the hand is (a) too weak for the
three-level floor, (b) too strong for the three-level *ceiling* of 9, (c) below the
quality bar, or (d) holds four to the queen-ten in a major.

**Whole-corpus measurement.** `open_pass` fires on 769 of 2000 tables at mean -0.657,
95% CI [-0.99, -0.33] — **above** the corpus mean of -0.804 (see §3, second opinion).
Sliced:

| opening pass, by hand | tables | IMPs | mean |
|---|---|---|---|
| all | 769 | -505 | -0.66 |
| 11 HCP with `rule_of_20 >= 19` (the band DECISIONS scopes out) | 87 | -80 | -0.92 |
| <=10 HCP with **exactly six** of a suit | 84 | -58 | **-0.69** |
| **<=10 HCP with SEVEN+ of a suit** | **8** | **-48** | **-6.00** |

Eight tables at -6.00 against a corpus mean of -0.80. It is the single worst-behaved
sub-population I can find anywhere in the opening decision, and it is invisible to the
family denominator because it is 1% of `open_pass`'s firings. Note the discipline the
same table enforces: the **exactly-six weak-two population is at -0.69, better than
baseline** — do not touch the weak twos.

The eight tables, with the gate that blocked each:

| board | hand | vul | blocked by | IMPs |
|---|---|---|---|---|
| 212a | `9753.Q987654.J.K` | vul | `suit_quality(H) = 1.0 < 1.5` | -13 |
| 614a | `JT97432.K4.65.98` | vul | `hcp 4 < 5` **and** quality 1.0 | -11 |
| 410a | `QT64.9.AKT7642.4` | nv | side-major veto (`QT64`, quality 1.5) | -10 |
| 272a | `7.A3.T987654.JT8` | nv | `suit_quality(D) = 0.5 < 1.0` | -6 |
| 872b | `64.K8.T4.AQJT954` | vul | `hcp 10 > 9` — a **ceiling** | -4 |
| 397a | `J.965.QJT8743.96` | vul | `hcp 4 < 5` | -3 |
| 329b | `J5.72.KT98632.T8` | vul | `hcp 4 < 5` | -2 |
| 146b | `A54.62.J876542.8` | nv | `suit_quality(D) = 0.5 < 1.0` | +1 |

Two of these are confident first divergences in my primary set (614a -11, BEN 2S at 0.94;
410a -10, BEN 3D at 0.92).

**Exact YAML.** Three independent widenings, listed so they can be measured separately
(round 11: decomposition is why that round shipped anything).

**(2a) Seven cards is the suit quality.** `open_3$X_nv` `1 → 0`, `open_3$X_vul`
`1.5 → 1.0`, all eight rules. Before / after, one example:

```yaml
      - id: open_3H_vul
        requires:
          suits: { H: [7, 13] }
          not: { suits: { S: [4, 13] }, evals: { "suit_quality(S)": [1.5, 9] } }
          hcp: [5, 9]
-         evals: { "suit_quality(H)": [1.5, 9], "quick_tricks_outside(H)": [0, 2] }
+         evals: { "suit_quality(H)": [1, 9], "quick_tricks_outside(H)": [0, 2] }
```

This is a band widening, not a new gate. **The HCP band is untouched, so partner's shown
minimum for 3X does not move** (constraint 7) — only the suit-quality expectation
loosens, which is what the rule's own `shows` text already implies for a seven-bagger.

**(2b) A preempt has no floor and no ceiling worth defending.**

```yaml
-         hcp: [3, 9]     # open_3$X_nv
+         hcp: [0, 11]
-         hcp: [5, 9]     # open_3$X_vul
+         hcp: [3, 11]
```

**This one DOES move the partner model**: the shown range for a three-level preempt goes
from 3-9 to 0-11 (nv). `rule_of_26` opposite it drops by ~1.5 points and
`partner_min_points` drops to 0, so advancer will bid game slightly less often. Round 11
lowered an obstruction floor from 3 to 0 elsewhere and measured -3 held out, so **this
half is the risky half and must be its own experiment.**

**(2c) The side-major veto is about a real major.** `suit_quality(H|S) >= 1.5 → >= 2.5` in
the veto clause of the eight three-level rules — "four to the queen-ten is not a suit
worth passing a seven-bagger for", which is the same sentence the file already uses to
justify the 4-card/1.5 form.

**VERIFIED.** Whole-corpus replay of all three together: **8 of 10,322 decisions change,
and they are exactly the eight tables above.** Every one is currently a PASS; the only one
that is not a current loser is 146b (+1). Decomposed — the three gates appear only on
rules requiring `suits: {X: [7,13]}` in an opening seat, so the decomposition was swept
over the 71 opening decisions in the corpus that hold a 7+ card suit, and the combined
version was then swept over all 10,322: (2a) changes 3 tables (-18), (2b) a further 4
(-20), (2c) a further 1 (-10); 63 of the 71 are untouched by any of them. Lints
identically (`floor 222, gap 0, shape 0, sibling 0, soft 0`).

**ENDANGERS.** (2a) and (2c) subtract nothing — they only widen, and the replay confirms
no existing call changes. (2b) lowers partner's shown minimum for every three-level
preempt everywhere; that is a real subtraction on the advancing seat and is why it is
listed separately. Board 146b (+1) becomes a preempt and may go the other way.

**HIGH-VARIANCE: (2a) no, (2c) yes (one board), (2b) yes (partner-model change).**

---

### CATEGORY 3 — **The ask has been answered: after a limited partner replies, I am captain, and the ladder above the ask ignores both the reply and the fit partner already promised.**

**The bridge, in one sentence.** Partner opened a weak two, so partner has six trumps —
my doubleton is the eighth — and partner has answered my ask, so nothing above the answer
should still be asking.

**Detection.** Context `weak2_ask_continuation`, `pattern: "2$W - P - 2NT - P - bid - P - ?"`.
Partner's `partner_min_length[$W] = 6` and `partner_max_hcp <= 10`. Two rungs are gated on
the wrong test:

```yaml
      - id: w2ac_game_$W
        requires: { suits: { $W: [3, 13] }, evals: { total_points: [15, 40] } }   # <- MY length
      - id: w2ac_sign_$W
        requires: {}                                                              # <- catch-all
```

`w2ac_game_$W` asks *how long is my suit*, opposite a partner who has already promised
six. The generic raise learned this lesson and says so in its own comment —
`uc_raise_S4`: *"my own length floor is 2 so a doubleton opposite a SHOWN six-card suit
(weak two, rebid suit, completed transfer) still reaches the eight-card game"* — and the
weak-two ask ladder never got the sweep. **A gate given to one rule and not its siblings
(constraint 6), for the third round running.**

**Evidence.** Board 296b, `(P) 2S (P) 2NT (P) 3C (P)`, W holds `A6.AK853.AT62.T3` — 17
HCP, two spades, and partner has just shown a club feature (a maximum). `w2ac_game_S`
fits **0.349** on the trump gate alone; `w2ac_sign_S` (`requires: {}`) fits 1.00 and we
sign off in 3S. BEN bids 4S at 0.89. **-10 IMPs.**

Whole corpus: the `w2ac_*` family fires on 10 tables, -19 IMPs, mean -1.90 against -0.804
(`w2ac_game_S` 3 tables -13; `w2ac_game_H` 4 tables +11; `w2ac_sign_S` 1 table -10;
`w2ac_3NT_S` 1 table +11; `w2ac_sign_H`, `w2ac_sign_D` never fire). Small family, sharp
defect.

**Exact YAML — additive rung, not a widening.** `w2ac_game_$W` is left alone (widening it
would also loosen the **minor**, where 4D is not game and 3NT is the right contract — the
replay proved that: an experimental widening pushed board 198b from a correct 3NT to 4D).

```yaml
      - id: w2ac_game8_$W
        call: 4$W
        priority: 54.5
        when: { partner_suit: $W, is_competitive: false }
        requires:
          suits: { $W: [2, 13] }
          evals: { total_points: [15, 40], "lott_total_trumps($W)": [8, 26], longest_suit_length: [0, 5] }
        shows: "placing the game opposite the weak two: partner showed six, so my doubleton is the eighth trump"
        establishes: { forcing: sign_off, agreed_suit: $W }
```

placed immediately **above** `w2ac_sign_$W`. Three deliberate choices:

- **priority 54.5**, i.e. below `w2ac_3NT_$W` (55) and above `w2ac_sign_$W` (54): with a
  minor, nine tricks still beat eleven, so 3NT keeps precedence and only the sign-off is
  displaced.
- **`total_points: [15, 40]`** identical to the sibling, so partner's shown minimum for
  4$W does not move (constraint 7). Only the promised trump length moves, 3 → 2, and the
  sharp `lott_total_trumps >= 8` makes that exact rather than soft.
- **`longest_suit_length: [0, 5]`** — with six of my own I bid my suit, I do not place
  partner's.

**VERIFIED.** Whole-corpus replay: **2 tables of 10,354 decisions change.**

```
296b  A6.AK853.AT62.T3   'P 2S P 2NT P 3C P'    3S -> 4S    (board -10)
371a  K3.KQ97.AKQ9.AT4   'P 2S P 2NT P 3NT P'   P  -> 4S    (board -10)
```

Both are currently -10 boards. **No current winner is endangered.** Lints identically.
(371a is the pure form of the category: we asked with 21 HCP, partner answered, and we
passed our own ask's answer.)

**ENDANGERS.** Takes the 3-of-the-suit sign-off away from a 15+ hand with a doubleton and
no six-card suit of its own, in a context that fires 10 times per 2000 tables. Nothing
else.

**HIGH-VARIANCE: no** (two boards, but the change is a strict superset of correct
behaviour and the replay bounds it at two tables).

**Companion, measured and NOT recommended as a bundle.** The ladder also has no rung above
`w2ac_game_$W`: on 43b, `2S (P) 2NT (P) 3S (P)` with `KQJ9.J82.A.AKQT7` (19 HCP, four
trumps, a running club suit), BEN bids 4NT at 0.92 and **4NT already exists as a candidate
at fit 1.00** via `gst_rkc_S` — it loses on priority, 46 to 56. Adding
`w2ac_rkc_$W` (4NT, priority 57, `total_points >= 19`, `lott >= 8`,
`longest_suit_length <= 5`) fixes it and I verified it: **11 of 10,345 decisions change,
board margin -6 in total, and two of the eleven are current +11 winners** (230b, 881a).
That is a coin-flip dressed as a fix. Reported, **HIGH-VARIANCE: yes**, measure alone or
not at all.

---

### CATEGORY 4 — **The limit bid beats the second suit: opener's rebid ladder ranks by call, not by whether the hand is balanced.**

**The bridge, in one sentence.** With a balanced minimum and no fit, 1NT names the hand in
one call; the cheap second suit is what you bid when you cannot.

**Detection.** Both calls fit 1.00 and `priority` — a static number that sees neither the
hand nor the auction — decides. `opener_rebid_1D_1S_2C`'s `ob_1D1S_2C` is priority **57**
and requires only `hcp: [10,17], C: [4,13], D: [4,13]`; `ob_1NT` in
`opener_rebid_1m_1M[D,S]` is priority **55** and requires `hcp: [12,14]` +
`semi_balanced`. A 4-4 minor two-suiter that is also semi-balanced satisfies both, so the
undescriptive call wins by two points of priority.

**Evidence.** Board 493b, `1D (P) 1S (P)`, E holds `A6.AJ2.T942.A742` — 2-3-4-4, 12 HCP.
We bid 2C; BEN bids 1NT at **1.00**. -6 IMPs. Board 320b, same shape family, -11. Board
236b, -7.

**Exact YAML — additive same-call rung at higher priority** (the pattern round 10 used to
repair `r1m_1S`: make the right case *fit and outrank*, rather than gating the wrong one):

```yaml
      - id: ob_1NT_flat_$M
        call: 1NT
        priority: 57.5
        # THE LIMIT BID BEATS THE SECOND SUIT.  With a semi-balanced minimum
        # and no fit, 1NT names the hand; the cheap second minor is for
        # unbalanced hands and outranked it on priority alone.
        requires:
          hcp: [12, 14]
          evals: { semi_balanced: [1, 1] }
          not: { suits: { $M: [4, 13] } }
        shows: "balanced minimum 12-14, no fit"
        establishes: { forcing: non_forcing }
```

inserted immediately above `ob_1NT` in `opener_rebid_1m_1M`. Gates are **verbatim** those
of `ob_1NT`, so the merged partner model for 1NT is unchanged (constraint 7): same call,
same band, same shape.

**VERIFIED.** Whole-corpus replay: **6 tables of 10,337 decisions change**, all of them
`1D - 1S - ?` with 4-4 minors and a semi-balanced 12-14:

```
236b A9.85.QJT65.AKT9  -7   2C -> 1NT      493b A6.AJ2.T942.A742   -6   2C -> 1NT
320b A2.76.J9764.AK84  -11  2C -> 1NT      328a AT.A8.96432.AQT4    0   2C -> 1NT
743b K5.Q2.AQ953.Q543   0   2C -> 1NT      878a AQ.J85.A654.K985    0   2C -> 1NT
```

Three current losers (-24 between them), three neutral, **no current winner endangered.**
Lints identically.

**ENDANGERS.** This is a re-rank in additive clothing and I am saying so plainly: it
**subtracts `1D - 1S - 2C` from every semi-balanced 12-14 with 4-4 minors**, six tables in
this corpus. That is the intent and it is one sentence of bridge, but it is a subtraction,
not a pure addition.

**HIGH-VARIANCE: no** (six tables, one coherent shape class).

---

### CATEGORY 5 — **Trumps agreed in a game force: the currency should change from points to controls, shortness and losers, and it never does.** (UNTESTED — needs a build)

**The bridge, in one sentence.** Once we have a trump suit and are going to game, high-card
points stop being the question and shortness opposite partner's values starts being it.

**Detection.** `agreed_suit: <suit>` and `game_forced: true` — both already supported as
**context-level** `when` keys, so the predicate costs nothing.

**The evidence that the currency never changes** (counts of evaluator mentions across the
whole 14,350-line system):

| evaluator | mentions |
|---|---|
| `hcp:` | 726 |
| `total_points` | 539 |
| `rule_of_26` | 115 |
| `controls` | **24 — every one of them in the slam zone, always as `[4,12]`** |
| `wasted_in_partner_shortness` | **2** |
| `ltc` | **1** (the 2C opening) |

The engine switches currency exactly once, at the 33-point slam threshold. Between "we
have a fit" and "we are asking for keycards" it counts points.

Concretely, `opener_rebid_1S_2H` — a game force with a heart fit — contains **two** rungs
for the fit:

```yaml
      - id: ob_1S2H_raise3H
        call: 3H
        priority: 80
        requires: { suits: { H: [3, 13] } }        # fits 1.00 on EVERY hand with three hearts
      - id: ob_1S2H_4H
        requires: { suits: { H: [4, 13] }, hcp: [12, 14], evals: { singleton_or_void: [0, 0] } }
```

`ob_1S2H_raise3H` has no strength gate and no shape gate at all, so a 12-count and a
20-count with a singleton make the identical call, at fit 1.00 and priority 80 — nothing
can outrank it. **Opener has no splinter after a 2/1 anywhere in the system**: the only
`convention: splinter` rules are responder's immediate raises of 1H/1S.

Boards, all of them rows where BEN's call **has no rule in the system at all** (I checked
every candidate; `ben_fit = None`):

| board | auction | hand | ours | BEN | IMPs |
|---|---|---|---|---|---|
| 982a | `1S (P) 2H (P)` | `J5432.A64.AJ94.A` (three aces, singleton ace of clubs) | 3H | **4C** (0.84) | -12 |
| 705a | `(P) 1NT (P) 2C (P) 2H (P)` | `8.KT87.AK7.AQT42` (singleton spade) | 4NT | **3S** (0.99) | -11 |
| 483a | `(P) 1S (P) 2C (P)` | `AQJT986.AJ7.J8.2` (seven-card suit, 13 HCP) | 2S | **4S** (0.96) | -10 |
| 70a | `1S (P) 2C (P)` | `KQJT87.3.Q3.KJ85` (6-4, four-card club fit) | 2S | **3C** (0.94) | -12 |

Whole corpus: `ob_1S2H_raise3H` 5 tables -12 (mean -2.40); `ob_2over1_2S` **3 tables -35,
mean -11.67** — the worst per-table mean of any rule in my primary set, though on a tiny
denominator; `ob_2over1_raise` 1 table +0; `ob_2over1_2H` 3 tables +1.

483a also shows a plain ceiling in the same family: `ob_2over1_jump3$M` (the only rung
above the quiet 2M rebid) requires `hcp: [15, 21]`, and `AQJT986.AJ7.J8.2` is 13 HCP with
about six losers. **In a game force with a self-sufficient seven-card suit the right test
is losers, not high cards** — `ltc` exists and is used once in the entire system.

**What should exist.** Opener's splinter after a 2/1, plus the answering seat
(constraint 3 — `opener_after_splinter_wasted` is the template and already uses
`wasted_in_partner_shortness: [4, 40]`):

```yaml
  # inside opener_rebid_1S_2H, above ob_1S2H_raise3H
      - id: ob_1S2H_splinter_C
        call: 4C
        priority: 81
        requires:
          suits: { H: [3, 13] }
          evals: { singleton_or_void: [1, 1], "suit_length(C)": [0, 1], total_points: [12, 40] }
        shows: "splinter: hearts agreed in the game force, club shortness"
        establishes: { forcing: game_forcing, agreed_suit: H }
        convention: splinter
      # ... _D twin (4D), and the answering context
  - id: responder_after_opener_splinter
    description: "Responder over opener's splinter: duplication check"
    pattern: "1S - P - 2H - P - 4$x - P - ?"
    rules:
      - id: roas_wasted_$x
        call: 4H
        priority: 60
        requires: { evals: { wasted_in_partner_shortness: [4, 40] } }
        shows: "wasted honours opposite the shortness: no slam, minimum game"
        establishes: { forcing: sign_off, agreed_suit: H }
      - id: roas_cue_$x
        call: 4NT
        priority: 61
        requires: { evals: { wasted_in_partner_shortness: [0, 3], controls: [4, 12] } }
        shows: "no duplication and the controls: keycard"
        establishes: { forcing: one_round, agreed_suit: H, asking: rkc }
```

and, separately, an `any_of` widening of the existing jump rebid so playing strength can
substitute for high cards:

```yaml
      - id: ob_2over1_jump3$M
-       requires: { suits: { $M: [6, 13] }, hcp: [15, 21] }
+       requires:
+         suits: { $M: [6, 13] }
+         any_of:
+           - { hcp: [15, 21] }
+           - { evals: { ltc: [0, 6], "suit_quality($M)": [3, 9] } }
```

**UNTESTED.** I did not prototype this: it is four new contexts plus an answering ladder,
its motivating evidence is four boards, and the families it touches fire 3-5 times per
2000 tables. **Its value is the diagnosis** — `ltc: 1`, `wasted_in_partner_shortness: 2`,
`controls` slam-only — not my guess at the rungs.

**ENDANGERS.** A 4C/4D splinter at priority 81 pre-empts every 4C/4D the generic toolkit
offers in that auction; and constraint 3 means it cannot ship without the answering seat.

**HIGH-VARIANCE: yes.**

---

## 3. SECOND OPINION — the two largest loss concentrations in the whole audit

Computed by summing `imp_margin` over all 278 confident first-divergence rows grouped by
`rule`:

```
-169  28 open_pass        -79  14 cl_pass         -44   7 sw_pass
 -38   6 uc_pass          -33   4 oc1C_1S         -32   5 oc1C_pass
```

### 3.1 `open_pass` (-169 IMPs, 28 rows) — **NOTHING-WRONG as a family. I agree with round 11.** One real sub-species inside it.

Whole corpus: **769 of 2000 tables, -505 IMPs, mean -0.657, 95% CI [-0.99, -0.33]**.
The corpus mean is -0.804. The interval contains it, and the point estimate is **better**
than baseline. A family that fires on 38% of tables and beats the corpus average is not a
loss concentration; it is the corpus.

The audit rows decompose cleanly, and I computed `hcp` / `rule_of_20` for all 28:

| sub-species | audit rows | audit IMPs | whole-corpus slice | mean |
|---|---|---|---|---|
| 11 HCP, `rule_of_20` 18-21 | **19** | **-99** | 87 tables | -0.92 |
| 6-card weak two blocked by a floor or a quality bar | 2 | -14 | (inside the 84-table exactly-six slice) | -0.69 |
| third-seat FIVE-card weak two (BEN's style, not ours) | 4 | -25 | — | — |
| no six-card-minor preempt exists | 1 | -10 | — | — |
| **7-card suit, no rung fits** | **2** | **-21** | **8 tables** | **-6.00** |

**The 11-count band is confirmed dead as a lever, with a number.** 87 tables at -0.92
against -0.80 is a *total* excess of about **-10 IMPs across the whole 1000-board match**,
and only if every one of the 87 were repaired for free. That is inside the noise of the
coordinate-descent result DECISIONS already records (-0.025 ± 0.062 held out). Round 11's
verdict — "its hands are rule-of-20 threshold cases, which DECISIONS scopes out" — is
correct and I would not spend another cycle on it.

**But the family verdict was doing double duty.** The 7-card slice is 1% of `open_pass`'s
firings and 10% of its losses, at 7.5× the baseline loss rate, and it is a structural hole
(exactly-six weak twos, an HCP floor *and ceiling* on a shape bid) rather than a
threshold. See CATEGORY 2, VERIFIED, 8 tables, blast radius 8 of 10,322 decisions.
**Verdict: NOTHING-WRONG as a family; CATEGORIZATION DEFECT in the 7-card sub-population.**

### 3.2 `cl_pass` (-79 IMPs, 14 rows) — **NOTHING-WRONG. The rule is not the defect.**

Whole corpus: **718 of 2000 tables, -600 IMPs, mean -0.836, 95% CI [-1.20, -0.47]**.
The interval contains -0.804 comfortably. `cl_pass` decides more than a third of all our
tables; its excess over baseline is about **-23 IMPs total**, i.e. under 3% of the match.
Attributing -79 IMPs of first divergences to it is the same attribution error `ROUND_METHOD`
already records for `uc_nt3` and `all-pass`: a `requires: {}` catch-all that fits 1.00 on
every hand is where a starved seat *lands*, not what caused it.

Reading all 14 rows, **seven of them (-32 IMPs) are auctions where BEN doubles**: 638a
(0.95), 214a (0.99), 217b (0.90), 446b (0.96), 495a (1.00), 359b (0.86), 375b (0.99). The
defect they name is the **missing double**, and DECISIONS already records that the
four-level pull, the responsive double and the 2NT-Stayman twin were each measured
individually in round 9 at -22, -12 and -8 held out and each reverted, and that the pull
needs a "partner's double was PENALTY" condition first. **Do not re-open them without
that condition.** Of the remaining seven, four (610a `QT9652.853.65.J8` with 3 HCP; 677b
`92.9762.654.8632` with **0 HCP**; 187b; 260b) are Law/obstruction calls that belong to
reviewer A's half and to CATEGORY 1's toolkit question.

**Verdict: NOTHING-WRONG as a rule. Content defect upstream (no cooperative double above
the partscore level), already diagnosed and already measured negative.**

### 3.3 The concentration the audit's own ranking cannot see

Because both headline clusters are innocent, I ran the same test on the other two generic
passes:

| | tables | mean | 95% CI | contains -0.804? |
|---|---|---|---|---|
| `open_pass` | 769 | -0.657 | [-0.99, -0.33] | yes |
| `sw_pass` | 279 | -0.724 | [-1.31, -0.14] | yes |
| `cl_pass` | 718 | -0.836 | [-1.20, -0.47] | yes |
| **`uc_pass`** | **431** | **-1.329** | **[-1.76, -0.90]** | **NO** |

`uc_pass` is the only generic terminal in the engine that is statistically distinguishable
from the corpus, and it contributes **one** row to the confident first-divergence ranking
(968b, -1 IMP). CATEGORY 1 is what is inside it.

---

## 4. IMPORTANT GAP — vocabulary I want, and what I would do with it

The opponent fields landed mid-review and I used `is_competitive` in three of the five
categories above. Two things are still missing, both about **our own side's inferred
state**, which `EvalContext` computes and then drops.

### 4.1 `is_competitive` as a **context-level** `when` key (cheapest, highest value)

`ContextWhen` accepts only `agreed_suit, game_forced, asking, we_hold_contract`. Adding
`is_competitive` there lets CATEGORY 1 be fixed by **routing** rather than by duplicating
twenty rungs:

```yaml
  - id: general_competitive_low
-   pattern: "... - bid<3C - ?"
+   patterns: [ "... - bid<3C - ?", "... - bid<3C - P - ?" ]
    when: { we_hold_contract: false, is_competitive: true }
```

(or, if multi-pattern contexts are not supported, a second context carrying the first's
rungs verbatim). The `covered` mechanism means the routing must be resolved at context
level; at rule level I have to copy every rung. **This is the single change with the
largest measured population behind it: 465 tables, mean -1.14 vs -0.804.**

### 4.2 `partner_limited` — expose `partner_max_hcp` to rules

`EvalContext.partner_max_hcp` is maintained correctly (I read 40 after a 1S response, 10
after a weak two, 17 after a 1NT opening) and **no rule can see it**. I want either an
evaluator `partner_shown_max` or a rule-level `when: { partner_limited: true|false }`
(true iff `partner_max_hcp <= 17`).

Uses, in order of measured value:

1. **`uc_pass` is live opposite an unlimited partner.** Split by partner's ceiling at the
   moment we passed: `partner_max_hcp = 40` gives **82 tables at mean -2.27, CI
   [-3.32, -1.22]**; partner limited gives 349 tables at -1.11. Passing when partner has
   not yet limited themselves is 2.8× the corpus loss rate. I would not *gate* `uc_pass`
   (deleting the catch-all is how you get an engine that cannot bid), but
   `when: { partner_limited: false }` on a new **descriptive** rung set — "partner is
   unlimited, so say something" — is expressible only with this field, and the field also
   makes the population mechanically findable for the next round.
2. **Captaincy.** CATEGORY 3's rule of thumb — *after partner limits, the unlimited seat
   places the contract; invitations from the limited seat are noise* — is currently
   inexpressible. Rows 711a (`(P)(P)(P) 1H (P) 2H (P)`, we invite with 13 HCP opposite a
   6-9 raise, BEN passes at 0.92) and 90a, 377b, 132a (BEN passes at 0.96-1.00) are all
   one seat inviting into a limited partner.
3. **Honesty of `rule_of_26`.** With `partner_max_hcp = 40` the evaluator silently becomes
   `total_points + partner_min + 2`. A rule that wants a genuine combined test should be
   able to say `when: { partner_limited: true }` and a rule that does not should not be
   allowed to advertise one. This is constraint 10 (never trade explainability for score).

### 4.3 `partner_shown_length(suit)` as an evaluator

`lott_total_trumps` bundles my length with partner's, which is right for a raise and wrong
for everything else. CATEGORY 3's rung wants to say *"partner promised six"* directly —
today the only way to say it is to add my own length to it and compare to 8, which is why
`w2ac_game_$W` was written with a 3-card floor in the first place. `partner_min_length` is
already in `EvalContext`; expose it.

### 4.4 What I did **not** need

I did not need `their_min_hcp` or `their_max_fit` anywhere in the uncontested half —
by construction. `is_competitive` did all the work, and it did it as a *negative*
(`is_competitive: false` in CATEGORY 3, to keep a constructive rung from leaking into
competitive auctions). Worth recording: the most valuable of the new fields, for my half,
is the cheapest one.

---

## 5. RESIDUE — the 99 rows my categories do not explain

Honest partition of the primary set. "Explained" means a category above names the
mechanism, not that I shipped a fix.

**Opening decisions (35 rows, -194):**

| species | rows | IMPs | verdict |
|---|---|---|---|
| 11 HCP, `rule_of_20` 18-21 | 19 | -99 | **NOT a defect** — 87-table slice at -0.92 vs -0.80; scope-excluded, confirmed numerically (§3.1) |
| 7-card suit with no rung | 2 | -21 | **CATEGORY 2**, VERIFIED |
| third-seat five-card weak two | 4 | -25 | **BEN's style, not a defect.** A five-card weak two in third seat is a partnership agreement this system does not play; DECISIONS scopes convention additions out |
| 6-card weak two blocked (239a by `hcp 6 < 7` vul; 669a by `suit_quality(H) 1.0 < 1.5` vul) | 2 | -14 | **Genuinely close.** The exactly-six population measures -0.69, *better* than baseline. Do not widen the weak twos to reach two boards |
| no six-card-minor preempt exists (485b, BEN 3C on `KJT763`) | 1 | -10 | **Missing content**, but 3C on six is BEN being aggressive; low confidence |
| weak jump overcall vs simple overcall (970a, 261b) | 2 | -12 | **MEASURED NEGATIVE** — round 11 re-ranked exactly this and got -24 held out. Do not re-open |
| 1NT opening with a 5-card suit / 15-count style (179b, 562a) | 2 | -6 | style |
| other single boards | 3 | -7 | judgment |

**Constructive uncontested (64 rows, -443):**

| species | rows | IMPs | verdict |
|---|---|---|---|
| ladder banded by strength, never by shape (148b, 456a, 320b, 649a, 839b, 582b, 133b) | 7 | -60 | **partly CATEGORY 4/5.** 320b VERIFIED by the CATEGORY 4 prototype. The rest need rungs the file's own comment already names (`rmr_2M`: *"Banded by strength, never by SHAPE"*) — see below |
| GF with a fit: no shortness, no top rung (982a, 70a, 483a, 705a) | 4 | -45 | **CATEGORY 5**, UNTESTED |
| Walsh: 1D vs a 4-card major (539b, 853b, 163a, 135b, 885b, 552a) | 6 | -36 | **NOT a defect.** DECISIONS: *"1D response to 1C is Walsh-style"* is a documented agreement, and round 10 already rejected this exact BEN disagreement. **One exception**: 853b holds `K8763.82.A98763.` — five spades and **six** diamonds. Walsh is about *four*-card majors; with 6-5 the longer suit is bid first. That is a genuine shape hole worth one rung |
| 1NT-opening structure and style (115a Texas, 705a, 652b, 558b, 879b, 773b, 718b, 7b) | 7 | -40 | mostly convention differences (Texas transfers do not exist here). `nt_transfer_H` fires 13 tables at -2.54 and deserves its own look next round |
| 2C responses / the known missing landing ladder | 3 | -28 | **blocked on a known open item**, see below |
| responder jump shift absent (314b, 422a, 953a) | 3 | -31 | **missing content.** Responder has no jump shift, weak or strong, over *any* uncontested opening — while responder over an *overcall* has one (`nx_1m1S_wj_H`). A sibling gap. But 314b/422a are defensible 2/1 auctions and only 953a (11 HCP, six clubs, soft-missing into a **game force** at fit 0.80) is clearly wrong |
| semi-forcing 1NT passed (22a, 900a) | 2 | -20 | **NOT a defect.** `forcing_nt: semi` is a documented flag; `ob_1M1NT_pass` is `when: { config: { forcing_nt: semi } }` and both hands are flat 13-counts. BEN plays it forcing |
| opener's rebid: limit bid vs second suit (493b, 66b, 917a) | 3 | -12 | **CATEGORY 4** (493b VERIFIED; 66b is 11 HCP so `ob_1NT` still soft-misses; 917a is 1-4-5-3 and BEN's 1NT is dubious) |
| responder passes 1H/1D with 6 HCP and a void (955b, 112b) | 2 | -19 | close judgment; `r1H_pass` requires `hcp: [0,5]` and both hands have 5-6 with a void |
| remaining singles | 24 | -152 | judgment calls and BEN noise. Median -3 |

**On the 2C responses.** `r2c_2NT_positive` (`hcp: [8,40]`, `balanced`, priority 55 over
2D's 50) is the biggest single rule in my constructive set: 319a -13, 782a -13, 213b -2,
all three hands **exactly 8 HCP and flat**. Whole corpus it fires 10 tables at mean
**-1.90** against `r2c_2D_waiting`'s 6 tables at -0.50. It is tempting. **I am not
proposing it**, because reading the ten firings shows the loss is downstream: the auctions
after 2NT are `3C-3D-3S-4NT-5D-5S` and `3C-3D-4NT-5D-6D` — exactly the walk DECISIONS
already records as an open item (*"`2C - 2NT` positive continuations have no landing
ladder"*). Narrowing the response would hide the hole rather than fix it, and it is a
threshold change, which the project has measured at -0.025 ± 0.062. **Author the landing
ladder first, then re-measure the response.**

**Count.** Of 99 rows: **31 rows / -155 IMPs are ruled NOT defects** with data (11-count
band, Walsh, semi-forcing NT, weak jump overcall, third-seat weak twos); **18 rows /
-159 IMPs** are named by a category above, 8 of them with a verified prototype; the
remaining **50 rows / -323 IMPs** are missing content, close judgment or BEN noise. I
would rather report that ratio than pad the category list.

---

## 6. NON-FINDINGS — hypotheses I killed, with the data

**N1. "`rule_of_26` is nearly meaningless opposite an unlimited partner."** FALSE as
stated. The evaluator caps partner's estimate at `floor + 4`, so with `partner_max_hcp =
40` it returns `total_points + partner_min + 2` — a well-defined, conservative number, not
noise. What is true is narrower and worth recording: **opposite an unlimited partner a
`rule_of_26` gate is an own-points gate wearing a combined-values name.** For a rung
gated `rule_of_26 >= 25` opposite a 1S response (`partner_min_hcp = 6`) that is exactly
`total_points >= 17`. That is an explainability defect (constraint 10), not a scoring one,
and it is fixed by renaming the gate, not by changing the number. Opposite a preempt the
evaluator behaves correctly: after a weak two it computes `(5 + 9)/2 = 7`, a genuine
midpoint.

**N2. "Sign-off and invitational rungs are live inside a game force."** FALSE on this
corpus. I replayed all 10,300 of our decisions and looked for a call whose rule
`establishes` an invitational or sign-off meaning made while `sides[side].game_forced` was
true. **Four firings in 2000 tables**, and both rules involved (`rkc5H_pass_signoff`,
`qa_pass`) are passes *after a keycard reply*, where a sign-off is correct. `make_setup`
already computes `pass_forbidden` in a game force and it works. The hypothesis is sound
bridge and the engine already implements it.

**N3. "The post-agreement ladders test raw points."** TRUE (CATEGORY 5) but **do not fix
it by gating.** 102 of the system's 157 3NT rules carry no shape or stopper requirement at
all. Adding `semi_balanced` or a stopper gate to that family is precisely the round-6
failure mode (a `semi_balanced` gate killed five cold 6NTs) and DECISIONS records the
`weakest_their_stopper` repair at -9 held out. The additive form — give 3NT a *competitor*
at higher priority (the six-card major rebid, the fourth suit) — is the only safe shape,
and the families concerned are tiny: the whole `rr1H1S*` responder-rebid family fires on
**9 tables in 2000** (-24). Round 11's lesson applies directly: a rule that rarely fires
may describe a rare hand.

**N4. "The weak-two ask ladder should widen `w2ac_game_$W` itself."** MEASURED WORSE. My
first prototype widened the existing rung to `suits: { $W: [2,13] }` + `lott >= 8`.
Corpus replay: 11 tables changed, and three of them got *worse bridge* — board 198b went
from a correct 3NT to **4D** (four of a minor is not game), 948a from 3S to 4D holding
`AKJ873` of spades, 369a from 3NT to 4H. **A prototype I measured worse on its own
motivating family.** The shipped version (CATEGORY 3) is a separate rung at priority 54.5
below the 3NT rung, with `longest_suit_length: [0,5]`, and changes exactly 2 tables.

**N5. "The generic uncontested toolkit is bad."** FALSE — it is good at its job and is
being given the wrong job. On genuinely uncontested auctions the `uc_*` family measures
**-0.67 over 126 tables**, better than the -0.804 corpus mean. This is the reason
CATEGORY 1 is a *routing* fix and not a rewrite, and it is the strongest argument I have
that categorization, not content, is where the remaining IMPs are.

**N6. "Third seat needs a five-card weak two."** Not proposed. Four audit rows, -25 IMPs,
BEN 0.86-0.95 — but it is a partnership agreement, not a repair, and the exactly-six
population already measures better than baseline (-0.69 over 84 tables). Adding it would
also lower partner's shown length for 2M **everywhere**, which is constraint 7's exact
trap.

---

## 7. Fix list, in the order I would measure them

| # | category | change | replay blast radius | at stake | risk |
|---|---|---|---|---|---|
| 1 | CAT 2a | preempt suit-quality widening | 3 of 10,322 | -18 | low, VERIFIED |
| 2 | CAT 3 | `w2ac_game8_$W` | 2 of 10,354 | -20 | low, VERIFIED |
| 3 | CAT 4 | `ob_1NT_flat_$M` | 6 of 10,337 | -24 | low, VERIFIED (a re-rank; states its subtraction) |
| 4 | CAT 2c | side-major veto 1.5 → 2.5 | 1 of 10,322 | -10 | HIGH-VARIANCE (one board) |
| 5 | CAT 2b | preempt HCP band 3-9 → 0-11 / 5-9 → 3-11 | 4 of 10,322 | -20 | HIGH-VARIANCE (moves the partner model) |
| 6 | CAT 1 | seed Law rungs under `is_competitive: true` | 2 of 10,355 | -4 | low, VERIFIED, low value |
| 7 | CAT 1 | **context-level `is_competitive` + route the competitive toolkit** | ~465 tables | ~-156 excess | HIGH-VARIANCE, needs a DSL change, **the largest measured population in the review** |
| 8 | CAT 5 | opener's splinter after a 2/1 + answering seat | unmeasured | -45 | HIGH-VARIANCE, UNTESTED |

Items 1-3 are additive, verified and bounded at 11 tables between them; the only current
winner any of them touches is board 146b (+1), which item 1 turns into a 3D preempt.
Items 4-5 are the same category as item 1 but each needs its own held-out number — item 5
because it moves partner's shown minimum for every three-level preempt. Item 6 is only the
proof that the mechanism of item 7 works; **item 7 is the finding.**
