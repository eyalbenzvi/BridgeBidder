# Adversarial critique of the twenty round-13 fixes (seed 131313)

Reviewer: external, adversarial. Assignment: kill what will not survive a corpus
it has never seen, reshape what is right-but-wrongly-repaired, ship only what
can be defended with a denominator.

**Result: 6 SHIP/RESHAPE-with-a-rung, 3 RESHAPE-to-text-only, 11 KILL.**
The six behavioural survivors, prototyped together, change **5 calls on 5 of the
2,000 tables** of `reports/e10_before.jsonl`. That is the honest ceiling of this
batch. Nothing here is a scoring lever; the value is four starved seats closed
and eleven confidently-argued hypotheses proved wrong.

Nothing in the repo was modified except this file.

---

## 1. Method note

**Instruments built** (all in the scratch directory, none in the repo):

- `corpus.py` → `corpus_e10.jsonl`: all **10,355** decisions we made across all
  **2,000 tables** of `reports/e10_before.jsonl` (seed 242424, -804; winners
  included), each re-asked through `prepare_decision` + `score_candidates` and
  recorded with its matched contexts, its full candidate ranking with fits and
  priorities, and 13 evaluators including the new `their_shown_hcp / their_fit /
  their_bidders / partner_shown_max`. Every denominator below is computed on
  this table.
- `law.jsonl` / `oc.jsonl`: targeted rescans (per-suit `lott_total_trumps`,
  `their_fit`, `suit_quality`) for the Law and overcall slices.
- `build.py` + `replay.py`: a prototype YAML built by asserted surgical edits,
  replayed decision-by-decision **in a separate process** (`_SETUP_CACHE` is
  keyed on `id(system)`), and diffed against a baseline replay.
- `lintproto.py`: `tools/lint_system.py` pointed at the prototype.

**Two denominators are quoted throughout.** `mean` is the board IMP margin of
the tables a slice touches; corpus baseline **-0.80**. `our gap` is the par gap
**signed for us** — `a_par_gap` at table A, **minus** `b_par_gap` at table B,
because the recorded field is always N/S-signed; corpus baseline **-0.378**.
A slice whose `mean` is bad but whose `our gap` is at or above baseline is a
hard-board population, not a defect. Getting that sign wrong reverses several
of the verdicts below, and it reverses the reading of `general_pull_or_sit`,
the sandwich seat and `cl_new_*2` in particular.

**Caveat on the denominator corpus.** `e10_before.jsonl` was played by the
round-11 system; the committed YAML is post-round-12. Replaying it under the
current system reproduces 10,311 of 10,355 decisions; the 44 differences are
round-12's own fixes (the preempt quality floor, the Law rungs, `ob_1NT`'s
priority). Denominators are therefore accurate to ~0.4% and no conclusion below
turns on those 44.

**Sanity.** Six of the twenty findings misquote the rule they indict. They are
flagged individually; three of the eleven kills rest on the correction alone.

---

## 2. Verdicts

### FIX 1 — the RKC 5C answerer has no seat — **SHIP (structure only, reach 0/2000)**

Verified. At board 31 `[a13]` the seat matches `contexts: []` and falls to the
code fallback at priority 8. Constraint 3, inside the RKC ladder itself.

**Denominator.** Auctions where our 4NT drew a reply and the asker then signed
off or bid on: **33 of 2,000 tables**. Of those the reply was 5C and the asker
signed off at five of the agreed suit on **6** tables (boards 288a, 350b, 425b,
729a, 802b, 875a). **All six answerers hold exactly ONE keycard.** The slam rung
therefore fires on **0 of 2,000**; the six become explanations rather than
fallbacks. Sell it as explainability, not as IMPs.

```yaml
# AFTER — new context, inserted immediately before `rkc_continue_after_5D`
  - id: rkc_5C_answerer
    description: "The 5C (1 or 4) answerer over the asker's sign-off"
    expand: { A: [H, S] }
    pattern: "... - 4NT - P - 5C - P - 5$A - P - ?"
    when: { agreed_suit: $A }
    rules:
      - id: rkc5C_ans_slam_$A
        call: 6$A
        priority: 60
        requires: { evals: { "keycards(agreed)": [4, 5] } }
        shows: "four keycards opposite a sign-off that feared one: nothing is missing - bidding the slam"
        establishes: { forcing: sign_off, agreed_suit: $A }
      - id: rkc5C_ans_pass_$A
        call: P
        priority: 55
        requires: {}
        shows: "one keycard: partner's sign-off stands"
        establishes: { forcing: sign_off }
```

The pass rung is a **complete** fallback (`requires: {}`), not the mirror of the
slam gate — round 6's `rkc5H_signoff` lesson. Board 31 `[a13]` now bids 6H at
fit 1.00; board 22 `[b15]` correctly passes.

- **VERIFIED** (prototype: board 31 flips to 6H; six corpus tables relabel, call unchanged).
- **ENDANGERS**: nothing measurable. It defines P and 6$A in a seat where no
  context existed. The lint's `floor`/`collide`/`gap`/`sibling`/`soft` counts are
  unchanged.
- **HIGH-VARIANCE: no.** Bundle freely.

---

### FIX 2 — a strength branch on `rkc5C_slam` — **KILL**

The proposal is the mirror of `rkc5D_slam`'s two-keycard branch, and the mirror
does not hold. `rkc5D`'s branch works because **zero keycards opposite shown
values is not credible**. FIX 2 needs **one keycard opposite 19 support points
is not credible**, which is false: `KQx / KQJx / KQJ / KQx` is nineteen points
with one keycard and is a common hand.

**Denominator.** In the six 5C-reply auctions above the ASKER holds 2, 2, 3, 2,
2, 3 keycards. **Not one asker in 2,000 tables holds the single keycard the
branch is about.** Reach 0/2000, on a false inference.

**Interaction with FIX 1**: if both shipped, the asker would bid slam first and
FIX 1's rung could never fire — i.e. FIX 2 replaces a provable arithmetic
resolution with a guess. Ship FIX 1, kill FIX 2.

---

### FIX 3 — `ob_raise_4$M` has "no upper bound"; add an opener's splinter — **KILL**

**The finding misreads the rule.** It quotes the `shows` text. The `requires` is
`total_points: [19, 24]`, capped, with a comment in the file saying why ("capped
at 24 so a monster reaches the keycard rules").

**Denominator.** `ob_raise_4H/4S`: **8 tables, +0 IMPs, mean +0.00** against a
corpus mean of -0.80 — the best-behaved raise family in the file. The whole
context `opener_rebid_1m_1M` is 130 decisions at mean -0.56 / our gap **+0.21**,
above baseline on both. Hands with 4-card support, a singleton or void and 19+:
**4 tables**.

An opener's splinter is a new convention and needs the seat that answers it
(constraint 3). BEN's 3S is 0.76 — a lead, not a verdict. Its own round, if ever.

---

### FIX 4 — 11 HCP with a six-card major fits nothing — **RESHAPE, then SHIP**

Diagnosis **verified and reproduced twice**. At board 22 `[b7]` three candidates
tie at fit 0.80 — `rr_nt_gf3_S` (12-18), `rr_nt_2S` (6-10), `rr_nt_pass` (6-10) —
and the soft-miss lottery hands it to the highest priority, the game force.
The identical hole exists in the `1H - 1S - 1NT` twin and **it costs 12 IMPs on
the held-out corpus**: board 585 `[b8]`, `A98652.T3.AT8.QJ`, 11 HCP with six
spades, bids `rrh_nt_3S` and plays 3NT down one where 4S was cold
(imps **-12**, our gap **-12**).

**The repair as proposed is half wrong.** Raising `rr_nt_gf3_$M`'s floor from 12
to 13 is a GATE on a family that is **3 tables, +7 IMPs** — currently positive —
and it is threshold tuning (DECISIONS: -0.025 ± 0.062 held out). Do not touch it.

There is nowhere to invite: 3M is the game force and 2NT explicitly denies six.
The only additive repair inside the system is to let the sign-off cover the
eleven-count.

```yaml
# BEFORE
      - id: rr_nt_2$M
        requires: { suits: { $M: [6, 13] }, hcp: [6, 10] }
        shows: "6+ $M, to play"
# AFTER
      - id: rr_nt_2$M
        requires: { suits: { $M: [6, 13] }, hcp: [6, 11] }
        shows: "6+ $M, 6-11, to play - with no invitational 3$M available, eleven signs off"
```
and the identical edit on `rrh_nt_2S`. **Ceiling, not floor**: partner's shown
minimum for 2M does not move (constraint 7).

- **Denominator**: the two contexts are **31 tables, -2 IMPs, mean -0.06** — a
  healthy family with one hole. The change reaches **1 table in 2,000** (585b).
- **VERIFIED**: board 22 `[b7]` → 2S at fit 1.00; board 585 `[b8]` → 2S. Scored
  double-dummy (spades take 10 tricks, from table A's 4S), 2S+2 vulnerable is
  +170 against the 3NT-1 we scored, and the board margin moves **-12 → -10 (+2)**.
- **ENDANGERS**: 11-counts with a six-card major that would have made game now
  stop in a partscore. There is one such hand in 2,000 tables and it went down.
- **HIGH-VARIANCE: no.** Bundle.

---

### FIX 5 — a floor on `cl_new_$X2` when our side has never bid — **KILL**

The brief asked whether the categorical framing survives as something other than
a threshold change. **It does not, and the corpus says the threshold points the
wrong way.**

`cl_new_*2` fires on **60 of 2,000 tables**, -54 IMPs, mean -0.90, our gap +1.10.
Sliced exactly as the finding frames it — *our side has made no call and the
opponents have exchanged three or more constructive calls*:

| slice | tables | IMPs | mean | our gap |
|---|---|---|---|---|
| corpus baseline | 2000 | | **-0.80** | **-0.38** |
| all `cl_new_*2` | 60 | -54 | -0.90 | +1.10 |
| **we silent, they 3+ calls** (the category) | **21** | **-4** | **-0.19** | **+2.43** |
| we have acted | 25 | -15 | -0.60 | -0.12 |

The category the finding names is the **healthiest** slice of the family: mean
-0.19 against -0.80, par gap +2.43 against -0.38. And the floor is anti-correlated
with the result:

| total points | tables | mean | our gap |
|---|---|---|---|
| 10-11 (what a raised floor deletes) | 23 | **-0.70** | **+3.30** |
| 12+ (what it keeps) | 25 | **-1.80** | **-1.00** |

Raising the floor removes the better half. Two losing boards at BEN 0.99 and
1.00 are the tail of a 21-table population that is two IMPs a table above
baseline. **KILL**, and the categorical framing dies with the threshold.

---

### FIX 6 — the sandwich double is takeout of BOTH their suits — **RESHAPE, then SHIP ALONE**

Diagnosis correct. `sw_X` demands `suits: { $o: [0,2] }` — shortness in
**opener's** suit — which is the direct-seat requirement transplanted into a seat
where both opponents have named a suit. Board 30 `[b3]`, `AQ76.A2.832.K962`,
fits 0.35 and passes.

**Denominator, and it is the only sandwich slice that is genuinely below
baseline.** The sandwich seat is 331 decisions at mean -0.71 / our gap **+2.90** —
one of the healthiest families in the engine. Within it:

| slice | tables | IMPs | mean | our gap |
|---|---|---|---|---|
| sandwich passes, all | 279 | -202 | -0.72 | +2.90 |
| 12-16, ≤3 in *each* of their suits (loose) | 6 | -42 | -7.00 | -0.17 |
| **12-16, 4+ in BOTH unbid suits (strict)** | **3** | **-22** | **-7.33** | **-3.67** |

Take the **strict** form. The loose form adds three tables whose par gap averages
**+7.7** — passing was right on them, and two of them hold three cards in an
unbid suit, which is not a takeout double of two suits. One of the three (board
22b) is `1S - P - 1NT`, where only one suit has been bid at all.

The clean expression needs one predicate the file does not have. Two options:

**Preferred — one new evaluator, one sentence of bridge:**

```python
# evaluation/evaluators.py
@register_evaluator("weakest_unbid_length")
def weakest_unbid_length(hand, ctx):
    """My length in the SHORTEST suit nobody has bid (0 if every suit is bid).
    'Four cards in every unbid suit' is what a double of two bid suits promises."""
    shown = set(ctx.partner_suits) | set(ctx.their_suits) | ({ctx.agreed_suit} if ctx.agreed_suit else set())
    unbid = [s for s in "SHDC" if s not in shown]
    return float(min((hand.suit_length(s) for s in unbid), default=0))
# constraints/model.py  _EVAL_S2
    "weakest_unbid_length": _S2_SUIT,      # counted, not estimated
```
```yaml
# sw_X, BEFORE
          any_of:
            - hcp: [12, 16]
              suits: { $o: [0, 2] }
              evals: { longest_suit_length: [4, 13] }
            - hcp: [17, 40]
        shows: "takeout of their suits: shortness in opener's suit (or any 17+)"
# sw_X, AFTER
          any_of:
            - hcp: [12, 16]
              suits: { $o: [0, 2] }
              evals: { longest_suit_length: [4, 13] }
            # SANDWICH is not the direct seat: BOTH opponents have named a suit,
            # so the double is takeout of both and what it promises is length in
            # the two UNBID suits.  Shortness in opener's suit is neither
            # necessary nor sufficient here.  Floor stays 12, so partner's shown
            # minimum for the double does not move.  With three suits unbid
            # (they responded 1NT) the branch is unsatisfiable, which is correct:
            # that is a one-suited auction and the direct-seat test applies.
            - hcp: [12, 16]
              evals: { weakest_unbid_length: [4, 13] }
            - hcp: [17, 40]
        shows: "takeout of their suits: shortness in opener's suit, or four cards in each unbid suit (or any 17+)"
```

**Fallback with no engine change** — a six-branch `any_of` over the suit pairs
using `is_unbid_suit`, **plus** `"is_unbid_suit": 0.05` in `_EVAL_S2`. That
sharpness is **not optional and I measured it**: with the default sigma the
prototype fires two extra doubles — board 364b `J7.K4.J9763.AKQ8` (two spades in
an unbid suit) and 552b `KQ7.A873.A6.J764` (three) — because a suit that IS bid
scores 0.8 against a `[1,1]` gate. That is the `soft` lint species, live.

- **VERIFIED**: board 30 `[b3]` doubles at fit 1.00; whole-corpus replay changes
  exactly **3 calls** (97a, 966b, 997a), all inside the slice, all currently
  losing tables. Lints unchanged.
- **ENDANGERS**: the branch does not deny a five-card major, so 5-4 in the unbid
  suits with a chunky major will now double instead of overcalling (priority 70
  vs 68). None of the three corpus hands is such a hand; the six-card denial
  already on the rule still applies. It also widens what partner reads `X` as in
  a seat where `X` currently fires 13 times (mean -0.08).
- **HIGH-VARIANCE: YES** — three tables. **Measure alone.**

---

### FIX 7 — the pull ladder says "cheapest" and implements "longest" — **RESHAPE, SHIP on structure (reach 0/2000)**

Verified exactly. Board 30 `[b9]`: `3C` (`adx_pull_C3`, five clubs) fits 1.00 and
`2S` (`adx_pull_S2`, four spades) fits 0.80, so 3C wins the fast path even
though 2S is a level cheaper and a major. The `suit_diff(X,·) >= 0` gates are
round 5's deliberate repair (4-vs-6 in the majors) and must stay; what is missing
is the level.

Repair only the **two-level major** rungs, where a level is actually saved:

```yaml
# adx_pull_S2, BEFORE
        requires: { suits: { S: [4, 13] }, evals: { total_points: [0, 11], "suit_diff(S,H)": [0, 13], "suit_diff(S,D)": [0, 13], "suit_diff(S,C)": [0, 13] } }
        shows: "pulling the double to the cheapest 4+ suit"
# adx_pull_S2, AFTER
        requires: { suits: { S: [4, 13] }, evals: { total_points: [0, 11], "suit_diff(S,H)": [0, 13], "suit_diff(S,D)": [-1, 13], "suit_diff(S,C)": [-1, 13] } }
        shows: "pulling the double to the cheapest 4+ suit - a four-card major at the two level beats a five-card minor at the three"
```
and the `adx_pull_H2` twin (`suit_diff(H,S)` stays `[0,13]`, so 4=4 majors still
go to spades). Leave `adx_pull_S3/H3` alone: at the three level the major is
*higher*, not cheaper, and bidding higher on shorter is not the maxim.

- **Denominator**: `general_pull_or_sit` is 111 tables, mean -0.93, our gap -3.60.
  Pulls to a minor with a 4+ major available: 8 tables — four are
  `adx_pull_my_*` (my own bid suit, correctly unchanged) and the rest are at the
  three or four level where no level is saved. **The widened rungs fire on 0 of
  2,000 tables.**
- **VERIFIED**: board 30 `[b9]` → 2S at fit 1.00, priority 58 over 3C's 55;
  whole-corpus replay changes nothing.
- **ENDANGERS**: at equal level (standing bid 1NT/2C) a four-card spade now beats
  a five-card diamond. That is still the textbook advance of a takeout double,
  but it is a real widening of the reading.
- **HIGH-VARIANCE: no** (it cannot move a number). Bundle.

---

### FIX 8 — the feature ask fires with a self-sufficient six-card major — **KILL**

The bridge is right and the repair is unsafe in both directions.

**Denominator.** `rw2_2NT_ask` fires **15 times in 2,000 tables**, -13 IMPs, mean
-0.87 — baseline. Exactly **one** of the fifteen holds a six-card major (board
948a, `AKJT873…` over 2D) and **that table won +6 IMPs**. The population the fix
exists for is one table and it is a winner.

**And the destination is a starved seat.** `rw2_new_*` — the forcing new suit
opposite a weak two — fires **once in 2,000 tables**, and the weak-two opener has
no answering context: `2D - P - 2H - P - ?` lands in
`general_uncontested_continuation`, where a seven-card weak two (`J8.4.KJT8762.932`)
**passes the force out** at `uc_pass` fit 1.00. The finding's own second half
says as much ("the ask continuation has no rung for my own major") and the same
objection applies with more force to the alternative. Routing 15+ hands out of a
working ask into a one-firing family with no answering seat is constraint 3 in
reverse.

Recorded as an open item: *the forcing new suit over a weak two has no answering
context and is passed out.* Fix that first; then re-open this.

---

### FIX 9 — `ballow_nt2_strong` states "partner still unlimited" and does not implement it — **RESHAPE to text-only**

The explainability half is correct and worth fixing. The gate is **backwards on
the data**.

`partner_limited` is `partner_max_hcp <= 17`. Split the eight firings on it:

| | tables | IMPs | mean | our gap |
|---|---|---|---|---|
| all `ballow_nt2_strong` | 8 | -11 | -1.38 | -2.25 |
| partner **limited** — the gate deletes these | 4 | **0** | **+0.00** | -1.50 |
| partner **unlimited** — the gate keeps these | 4 | **-11** | **-2.75** | **-3.00** |

`when: { partner_limited: false }` deletes the half that costs nothing and keeps
the half that costs eleven IMPs. Board 9 `[b10]` does flip (partner_max_hcp is
11, confirmed), and it is one of the four that are collectively neutral.

Ship the sentence, not the gate:

```yaml
# BEFORE
        shows: "natural 2NT: 17-21 balanced with their suit stopped, partner still unlimited"
# AFTER
        shows: "natural 2NT: 17-21 balanced with their suit stopped"
```

- **VERIFIED** (zero behavioural change by construction). **ENDANGERS**: nothing.
- **HIGH-VARIANCE: no.** Bundle.

---

### FIX 10 — `uc_nt3` has no combined-values test — **KILL (the finding is factually wrong)**

`uc_nt3` reads

```yaml
        requires:
          hcp: [13, 19]
          evals: { rule_of_26: [24, 99], semi_balanced: [1, 1], weakest_their_stopper: [0.9, 9] }
```

It **does** carry `rule_of_26`, and `rule_of_26` uses the **midpoint** of
partner's shown range — `(floor + min(max, floor+4)) / 2` — so it already reads
partner's ceiling. `cl_nt3` is identical. The proposal is not new; the whole
premise is a misreading.

On board 25 `[b10]` the true mechanism is different and much narrower:
`total_points` 16 + partner's midpoint 7.5 = **23.5** against a gate of 24. It
misses by **half a point**, scores **0.946**, clears the 0.9 fast-path threshold
and wins on priority. The only honest repair is `rule_of_26 → rule_of_26_sharp`
(σ 0.4, already registered), which would score it 0.46 and hand the seat to
`uc_pass`.

**Denominator for that repair:**

| | tables | IMPs | mean | our gap |
|---|---|---|---|---|
| `uc_nt3`, all | 39 | -39 | -1.00 | -5.51 |
| `uc_nt3` with `rule_of_26 < 24` (all it deletes) | **3** | **-2** | -0.67 | -4.00 |
| `cl_nt3`, all | 8 | -3 | -0.38 | -7.75 |
| `cl_nt3` with `rule_of_26 < 24` | **0** | | | |

Three tables in 2,000, worth two IMPs, two of which made 3NT. `cl_nt3` — the
finding's "more evidence" — has **no** such firing and runs at -0.38, above
baseline. Fifth round running that `uc_nt3` is a symptom. **KILL.**

---

### FIX 11 — `ch_raise_S3` states a gate it does not carry — **RESHAPE to a text sweep**

The honesty half is right and **bigger than the finding says**: I counted the
whole file. **25 three-level raise rungs carry `rule_of_26` and not one of them
mentions it** (`cl_raise_$X3`, `ch_raise_$X3`, `ballow_`, `balhigh_`, `uc_`,
`xd_`, `cl_raise_lott3_S`). Separately, **10 four-level rungs say "13+ support
points" while requiring `total_points: [11, 40]`**, and `cl_raise_C3/D3` say
"10+" while requiring 8. A rule whose explanation contradicts its constraint
cannot be reasoned about — that is exactly why three of this round's twenty
findings misquote the rule they indict.

The content half must not ship. The slice — *contested, we passed, a three-level
major raise soft-missing* — is **37 tables, -70 IMPs, mean -1.89 but our gap
+0.68** against a baseline of -0.38. Above baseline on the attributable metric;
consistent with reviewer A's "62 tables, par gap +2.60, dead". Dropping the gate
is the Law at the three level and it is measured dead.

```yaml
# BEFORE (×20 identical strings, plus 4 xd_ and cl_raise_lott3_S)
        shows: "competitive raise of partner's S: 3+ trumps, 10+ support points, 8+ combined trumps"
# AFTER
        shows: "competitive raise of partner's S: 3+ trumps, 10+ support points, 8+ combined trumps, and the values for the level opposite partner's shown range"
# BEFORE (×10)
        shows: "competitive raise of partner's S: 13+ support points and a real trump fit opposite partner's shown range"
# AFTER
        shows: "competitive raise of partner's S: 11+ support points and a real trump fit opposite partner's shown range"
```

- **VERIFIED** (zero behavioural change). **ENDANGERS**: nothing.
- **HIGH-VARIANCE: no.** Bundle with FIX 9 and FIX 19.

---

### FIX 12 — `responder_after_minor_rebid` has no second-suit rung — **KILL as a lever**

Structurally true: with `$m` and `$M` fixed, the context has `rmr_newsuit_D` for
one unbid suit and nothing for the other major, so 6-4 is filed as a one-suiter.

**Denominator.** The whole context is **18 tables** in 2,000. Hands with a 5+
bid major and a 4+ other major: **3** (boards 557a, 854a, 917a), of which one has
game values (854a, 12 HCP, +0 IMPs). Board 44's 4S on `AT9763.AKQ9.73.9` is
defensible bridge anyway and BEN is only 0.61.

Adding a forcing 3H there needs the seat that answers it — and `rmr_newsuit_D`,
the rung it would copy, **already has no answering seat**. This is the standing
open item "a 6-5 hand rebids the six-card minor and never shows the five-card
major", one context along; it belongs in that round, not this one.

**Worth reporting as residue**, because it is the worst family I measured that
is *not* on the list: `responder_after_minor_rebid` is 18 tables, mean **-2.78**,
our gap **-5.00**, and the damage is at the top, not the side: board 418b bids
`rmr_4H` holding **23 HCP** opposite a 12-15 rebid (35+ combined, -11), board
314b bids `rmr_4H` on 19 (-13), board 996a bids `rmr_3m` on 19 (-13). `rmr_4NT`
requires `semi_balanced`, so a 19-23 count with a five-card suit has no slam
route. That is the round-6 ceiling species and it is worth four times what the
second-suit rung is worth.

---

### FIX 13 — loosen `their_fit >= 8` when they have jumped to game — **KILL, and it does not flip its own board**

Traced at board 54 `[a6]`. `ch_raise_lott4_S` scores **0.011**, and it fails on
**two** gates, not one: `their_fit` reads 5 **and `lott_total_trumps(S)` reads 9
against a sharp `[10, 26]`**. Removing or widening the `their_fit` branch leaves
the rung at ~0.04. **The proposed repair provably does not do what it is
proposed to do on the only board offered for it.** What actually decides the
seat is `ch_raise_S4` at fit 0.80 (`rule_of_26` 24 vs 25) losing to `ch_pass` at
1.00 — nine trumps, which round 12 measured and declined.

And the loosening is a coin flip, as the caution predicted. Whole corpus, *we
passed holding ten disclosed trumps in partner's major with 11+ total points*:

| slice | tables | IMPs | mean | our gap |
|---|---|---|---|---|
| all | 16 | -61 | -3.81 | -0.25 |
| `their_fit >= 8` (the shipped gate) | 5 | -36 | **-7.20** | +1.40 |
| `their_fit < 8` **and** standing bid at the 4/5 level (what FIX 13 adds) | **8** | -6 | **-0.75** | -2.88 |

The added population's board margin is **-0.75 against a corpus mean of -0.80** —
baseline, i.e. the coin flip that `their_fit >= 8` removed when it turned +1 into
+12. **KILL.**

---

### FIX 14 — a force with no answering seat: the reverse — **SHIP (structure only, reach 0/2000)**

The finding overstates it ("there is **no** `responder_after_reverse` context at
all") and the narrower truth makes the fix provably safe. Three such contexts
exist — `1C-1H-2D`, `1C-1S-2D`, `1C-1S-2H`. `ob_1m1S_2H_reverse` is expanded over
**both** minors, so `1D - 1S - 2H` is a reverse this system bids, and it is the
one twin that never got its answering context. A sibling gap, not a missing
family.

Reproduced at board 56 `[b7]`: contexts are `['general_uncontested_continuation',
'general_slam_try']`, `pass_forbidden` is set, the best non-pass candidate is
`uc_new_C3` at **0.143**, and `uc_pass` takes it at fit 1.00.

```yaml
# AFTER — verbatim clone of `responder_reverse_1C1S2H`, inserted before
# `opener_over_reverse_2NT`; nothing else claims this auction, so it can only add
  - id: responder_reverse_1D1S2H
    description: "Responder over the 1D - 1S - 2H reverse"
    pattern: "1D - P - 1S - P - 2H - P - ?"
    rules:
      - id: rrevd_2S
        call: 2S
        priority: 66
        requires: { suits: { S: [5, 13] }, hcp: [8, 40] }
        shows: "5+ spades opposite the reverse (forcing one round)"
        establishes: { forcing: one_round }
      - id: rrevd_3H
        call: 3H
        priority: 65
        requires: { suits: { H: [4, 13] }, hcp: [8, 40] }
        shows: "raising the reverse suit: 4+ hearts (game forcing)"
        establishes: { forcing: game_forcing, agreed_suit: H }
      - id: rrevd_2NT
        call: 2NT
        priority: 64
        requires: { hcp: [8, 11], evals: { semi_balanced: [1, 1] } }
        shows: "8-11 balanced opposite the reverse (forcing one round)"
        establishes: { forcing: one_round }
      - id: rrevd_3NT
        call: 3NT
        priority: 63
        requires: { hcp: [12, 40], evals: { weakest_unshown_stopper: [0.9, 9] } }
        shows: "game values opposite the reverse"
        establishes: { forcing: non_forcing }
```

- **Denominator**: `ob_1m1S_2H_reverse` fires 4 times in 2,000 tables and **all
  four are the 1C twin**. `1D - P - 1S - P - 2H - P - ?` occurs **0 times**.
  Ship it for correctness; claim nothing.
- **VERIFIED**: board 56 `[b7]` → 2S at fit 1.00. Whole-corpus replay: no change.
- **ENDANGERS**: nothing. The `floor` lint gains one advisory finding — identical
  to the one its 1C sibling already carries (222 → 223); `collide`, `gap`,
  `shape`, `sibling`, `soft` all stay at 0.
- **HIGH-VARIANCE: no.** Bundle.

---

### FIX 15 — the advance of a takeout double filed as a free overcall — **KILL (wrong rule)**

The finding indicts `cl_new_S2` ("5+ cards, **10+ points**"). Re-ranked, board 86
`[b5]` is decided by **`cl_new_long2_S_hi` — "a SIX-card suit, 8+ points" — at fit
1.00**; `cl_new_S2` scores **0.31**. The dossier field records the *primary
reading* (the highest-priority same-call rule), not the rule that matched. That
is round 9's trap, and it should be the first step of every review.

So the premise fails: the floor that fired is 8, not 10, the hand has 8 total
points and six spades, and showing a six-card major over partner's balancing
double is not "a free 10+ overcall" — it is the advance. The meaning did not
invert.

Adding a capped `cl_advance_x*` family would drop partner's shown minimum for
`2S` in `general_competitive_low` toward zero (constraint 7 — the round-8 rungs
carry an 8-point floor for exactly this reason), which is the floor the matched
rule already has.

What actually went wrong on board 86 is downstream: `gst_rkc_S` asked keycards
opposite an 8-point advance. That is the keycard-ask family, twice measured and
twice left unfixed. Residue, not a fix.

---

### FIX 16 — an invitation whose answering seat always says yes — **SHIP**

Verified and the cleanest constraint-3 instance of the round. `adv1n_2NT_$o`
("invite opposite 15-18") has no matching context; the overcaller's seat lands in
`general_uncontested_continuation` and `uc_nt3` (13-19 balanced) accepts across
the whole band.

**Denominator.** `adv1n_2NT_*` fires **4 times in 2,000 tables** — boards 323a,
569a, 678b, 791a — **-12 IMPs, mean -3.00, our gap -4.75**, and the invitation was
**accepted 4 times out of 4**. Overcaller's HCP: 18, 16, 15, 16.

```yaml
# AFTER — inserted before `opener_over_penalty_X_of_1NT`
  - id: advance_1NT_overcall_invite
    description: "The 1NT overcaller answers the 8-9 invitational 2NT"
    expand: { o: [C, D, H, S] }
    pattern: "1$o - 1NT - P - 2NT - P - ?"
    rules:
      - id: a1ninv_3NT_$o
        call: 3NT
        priority: 55
        requires: { hcp: [16, 40] }
        shows: "accepting the invitation: 16-18 of the 15-18 overcall"
        establishes: { forcing: sign_off }
      - id: a1ninv_pass_$o
        call: P
        priority: 50
        requires: {}
        shows: "a minimum 15 opposite 8-9: declining the invitation"
        establishes: { forcing: sign_off }
```

The pass rung is a complete fallback, so on 15 it is the only candidate fitting
≥ 0.9 and wins; on 16+ the 3NT rung outranks it. The 16 threshold is the file's
own sibling (`stayman_invite_accept_*`: 15 declines, 16-17 accepts). **Be explicit:
at 16 this does NOT flip board 49 — West holds 16 there, not the "minimum 15" the
finding states.** A 17 threshold would flip it and would also delete the family's
one winner (569a, +6). Choosing 17 because it flips the review board is fitting;
choosing 16 is the file's stated style. Ship 16.

- **VERIFIED**: whole-corpus replay changes **1 call** — board 678b, 15 HCP,
  3NT → P. Double-dummy: the same eight tricks make 2NT (+120) instead of failing
  3NT (-50); board margin **-6 → -2 (+4)**. The other three relabel only.
- **ENDANGERS**: this is a **narrower context shadowing `uc_nt3`** for that call,
  so state what it subtracts: exactly the 3NT accept on 13-15 balanced in this
  auction. 13-14 is impossible opposite a 15-18 overcall, so it subtracts the
  15-accept and nothing else. It also removes 4 of `uc_nt3`'s 39 firings, so any
  later re-measurement of `uc_nt3` must be taken after this.
- **HIGH-VARIANCE: no.** Bundle with FIX 4.

---

### FIX 17 — a suit-quality gate given to one rule and not its sibling — **KILL (both halves)**

**(a) `sw_1S` [1.5,9] vs `oc1D_1S` [1,9] is not a sibling asymmetry.** I read the
whole ladder: the sandwich seat is **uniformly half a point tighter** than the
direct seat — one level 1.5 vs 1.0 (`sw_1S/1H` vs `oc*_1S/1H`), two level 2.0 vs
1.5 (`sw_2x` vs `oc*_2x`). That is a consistent design for the seat where both
opponents have bid, not a gate someone forgot to copy. And the data agrees:
sandwich passes are **279 tables, mean -0.72, our gap +2.90**, one of the
healthiest families in the corpus.

**(b) The one-level quality block.** Whole corpus, *direct seat, we passed,
8-16 HCP, a 5+ suit ranking above theirs, `suit_quality` below the gate*:

| slice | tables | IMPs | mean | our gap |
|---|---|---|---|---|
| direct-seat overcall passes, all | 460 | -393 | -0.85 | **+2.40** |
| blocked by suit quality at the one level | **11** | -17 | -1.55 | **+1.00** |
| … of which six-card suits | 1 | -8 | -8.00 | -9.00 |

Eleven tables at a par gap a point and a half **above** baseline. The six-card
case — board 67's species — is a single table. This is threshold tuning on a
family that DECISIONS scopes out and that measures above baseline. **KILL.**

---

### FIX 18 — opener's reopening double — **KILL (wrong rule, and the board is not a defect)**

The finding says "`ballow_X` cannot fire and nothing else does". **`ballow_reopen_X`
exists** — *"reopening double: 16+, short in their suit, our side already in"*,
priority 41, gated `side_has_acted: true`. It is the rule that governs, and on
board 67 `[b4]` it scores 0.015 because West holds **KQ83 of their suit**.

And the board is not a defect. West is 4-3-3-3-ish with 17 balanced and four
diamonds, opposite a partner who **passed our 1C opening** and is therefore
0-5 in the engine's own model. Twenty-two combined with four of their trumps:
passing 1D out is the bridge. The finding cites no BEN call for this decision.

The slice *we opened, they overcalled, the auction died back to us, 15+, we
passed* is **8 tables, mean -1.50, our gap -1.75** — mildly negative, and most of
its members hold a five-card major of their own, for which a reopening double is
the wrong tool. DECISIONS is right that opener's reopening double "wants its own
round": adding a third meaning of `X` to a context that already defines two is
the `collide` species. Leave the open item where it is; it now has one board
attached to it that is not evidence for it.

---

### FIX 19 — `ballow_X` silently demands shortness — **RESHAPE to text-only**

Text half correct: the constraint is `11+ with standing_suit_length <= 2` or
`9+ with <= 1`, and the sentence says only "values are marked opposite a passing
partner".

Widening it is not indicated. `ballow_X` already fires on **20 tables, -24 IMPs,
mean -1.20, our gap -3.40** — below baseline on both, so this is a losing rule
being asked to fire more often. And the population it would newly reach —
*balancing seat, we passed, `ballow_X` soft-missing, 12+ HCP* — is **6 tables,
mean -2.50, our gap +0.17**, above the -0.38 baseline on the attributable metric.

The review's own non-finding declines exactly this action in the direct seat
("BEN doubles a flat 13 with three in their suit; I believe our rule is right").
Consistency requires declining it in the balancing seat too.

```yaml
# BEFORE
        shows: "balancing double: values are marked opposite a passing partner"
# AFTER
        shows: "balancing double: values are marked opposite a passing partner, with at most a doubleton in their suit (a singleton at 9+)"
```

- **VERIFIED** (zero behavioural change). **ENDANGERS**: nothing.
- **HIGH-VARIANCE: no.** Bundle with FIX 9 and FIX 11.

---

### FIX 20 — the support double disappears when LHO overcalls — **KILL**

Two independent reasons.

**The convention would be pointless there.** The system's stated agreement is
"after `1m - P - 1M` and interference below 2M". Over a 1H overcall the system's
own negative double shows exactly four spades and **`1S` promises 5+**. A support
double distinguishes three-card from four-card support when responder's 1M might
be four; once responder's 1S is five, three-card support is already an eight-card
fit and the call is a raise, not a convention. Extending `X` into
`general_competitive_low`, which already defines it two ways, is the `collide`
species.

**And the mechanical cause is elsewhere.** Traced at board 97 `[a5]`: S holds
`Q53.AK42.K863.43`, 12 HCP (not 13). Scored **in the candidate's own context**
with spades agreed the hand is **13 support points**, and `cl_raise_S2` bands
`[6, 12]` — a one-point miss, fit 0.80, beaten by `cl_pass` at 1.00. Meanwhile
`cl_raise_S3` carries `cheapest_in_suit: true` and 2S is legal, so it is never
offered. That is the round-9 competitive-raise seam at a higher band, and its
population is **3 tables, -3 IMPs, mean -1.00, our gap +0.00** — at baseline.
Round 11 measured freeing `cl_raise_$X3` from `cheapest_in_suit` at **0**.

Nothing here is worth a rule. `sd_double` itself is 16 tables at mean -1.44 /
our gap -4.50; if anything the convention is under-performing where it already
applies.

---

## 3. Interactions between the twenty

- **FIX 1 × FIX 2** — same board, opposite seats. FIX 2 would pre-empt FIX 1 and
  substitute a guess for arithmetic. Ship 1, kill 2.
- **FIX 5 × FIX 15** — both indict `cl_new_$X2`. Board 86's matcher is
  `cl_new_long2_S` (floor 8), so FIX 5's floor-raising would not even have
  touched FIX 15's board. Both killed.
- **FIX 10 × FIX 16** — both touch `uc_nt3`. FIX 16 removes 4 of its 39 firings
  by shadowing one auction; FIX 10 would have sharpened it globally. With FIX 10
  killed there is no conflict, but any future `uc_nt3` measurement must be taken
  **after** FIX 16 lands, or the two will be confounded.
- **FIX 6 × FIX 17** — both touch the sandwich seat. If both shipped, the double
  (priority 70) would still take the 4-4 hands and the loosened overcall
  (priority 68) would take five-card suits — no contradiction, but 17 is killed,
  so the seat gets one change, not two.
- **FIX 11 × FIX 13 × FIX 20** — three instances of "a combined-values test
  decides a competitive question". All three content repairs are killed on
  denominators; only FIX 11's text sweep ships, and it makes the species visible
  in 35 `shows` strings so it stops being rediscovered by hand.
- **FIX 4 × FIX 12** — different contexts, no interaction.

---

## 4. ORDER OF WORK

**Bundle A — zero behavioural change, no measurement needed.** Verify with a
replay diff of **0** decisions, then commit.

1. FIX 11 — the `shows` sweep: append the `rule_of_26` clause to the 25
   three-level raise rungs; correct "13+" → "11+" on the 10 four-level rungs
   (and "10+" → "8+" on `cl_raise_C3/D3`).
2. FIX 9 — drop "partner still unlimited" from `ballow_nt2_strong`.
3. FIX 19 — state the shortness requirement in `ballow_X`.

**Bundle B — structure, reach 0/2000, cannot move a number.** One measurement
together, expected exactly 0 boards changed; keep on structure at zero cost
(the round 7 / 8 / 11 precedent).

4. FIX 1 — the RKC 5C answerer's context.
5. FIX 14 — the `1D - 1S - 2H` reverse twin.
6. FIX 7 — the two-level major pull.

**Bundle C — two starved seats, one table each, both determinable.** Measure
together; expected **+2 and +4** on the review corpus, 2 boards changed.

7. FIX 16 — the 1NT-overcall invite's answering context (+4 on board 678b).
8. FIX 4 — the eleven-count with a six-card major (+2 on board 585b).

**Single — MUST NOT be bundled.**

9. FIX 6 — the sandwich double. Three tables in 2,000, all currently losing, par
   gap -3.67. It is a **widening of a double** in the healthiest family in the
   engine (par gap +2.90), it is justified on three boards (constraint 4), and it
   needs an engine change (`weakest_unbid_length`, or a sharp tolerance for
   `is_unbid_suit` — I measured that without it two wrong doubles leak). Measure
   it **alone** on the held-out corpus, and revert on the number.

**Do not run Bundle C and the FIX 6 single in one match.** Bundle C's two boards
are attributable; FIX 6's three are not, and round 9's decomposition is the only
reason that round shipped anything.

**Before any of it**: `python3 -m pytest -q`, `tools/lint_system.py`,
`tools/fuzz_decisions.py --n 300 --strict`. The prototype's lint deltas are
`floor` 222 → 223 (the new reverse context inherits its 1C sibling's advisory
finding) and nothing else.

---

## 5. Killed, and why — the negative results

| fix | verdict | the number that killed it |
|---|---|---|
| **2** RKC 5C strength branch | KILL — false inference | 0 of 2,000 askers hold one keycard after a 5C reply; "one keycard opposite 19 points" is a normal hand, unlike "zero opposite values" |
| **3** `ob_raise_4$M` uncapped / splinter | KILL — misquoted | the rule is `total_points: [19, 24]`, capped, with the reason in a comment; the family is 8 tables at mean **+0.00** vs -0.80 |
| **5** floor on `cl_new_$X2` | KILL — the category is above baseline | the named slice is 21 tables at mean **-0.19 / gap +2.43**; the 10-11 point band scores **-0.70** and the 12+ band **-1.80**, so the floor points the wrong way |
| **8** shape gate on `rw2_2NT_ask` | KILL — 1 firing, and it wins | 1 of 15 firings holds a six-card major, worth **+6**; and the destination (`rw2_new_*`, 1 firing in 2,000) has no answering seat and is passed out |
| **10** combined values on `uc_nt3` | KILL — misquoted | the rule carries `rule_of_26: [24,99]` and it uses partner's **midpoint**; the real failure is a 0.5-point soft miss scoring 0.946, and sharpening it reaches **3 tables / -2 IMPs**; `cl_nt3` reaches **0** |
| **12** second suit in `responder_after_minor_rebid` | KILL as a lever | 3 of 18 tables; the family's real damage is a 23-count bidding `rmr_4H` — a ceiling, not a shape gap |
| **13** loosen `their_fit >= 8` | KILL — does not flip its own board | `ch_raise_lott4_S` scores **0.011** at board 54 and fails the **sharp `lott >= 10`** gate too; the added slice is 8 tables at mean **-0.75** against a corpus mean of -0.80 |
| **15** advance filed as a free overcall | KILL — wrong rule | the matcher is `cl_new_long2_S_hi` ("a SIX-card suit, 8+ points", fit 1.00); `cl_new_S2` scores 0.31 |
| **17** overcall suit-quality siblings | KILL — not a sibling gap | the sandwich ladder is uniformly +0.5 quality at both levels by design; the blocked population is 11 tables at par gap **+1.00** vs -0.38 |
| **18** opener's reopening double | KILL — wrong rule, and no defect | `ballow_reopen_X` exists and correctly declines with KQ83 of their suit opposite a partner the engine reads as 0-5 |
| **20** support double over an overcall | KILL — pointless there, and misdiagnosed | responder's free 1S promises 5+, so exactly-three support is already an eight-card fit; the mechanical cause is a 13-support-point hand missing `cl_raise_S2` by one, a 3-table slice at par gap **0.00** |

Three further negative results worth keeping:

- **The dossier's rule field is the primary reading, not the matcher.** It named
  the wrong rule in FIX 15 and FIX 18, and half of FIX 10's premise. Re-rank
  every indictment through `score_candidates` before writing it down.
- **`par_gap` in the match rows is N/S-signed at both tables.** Read at face
  value it inverts the verdict on `general_pull_or_sit`, the sandwich seat and
  `cl_new_*2`. Our gap is `+a_par_gap` and `-b_par_gap`; the corpus baseline is
  **-0.378**, which is the number reviewer A quoted.
- **`is_unbid_suit` has no sharp tolerance** and is used by no rule today. The
  first rule to use it leaks: measured, two extra sandwich doubles fire on hands
  with two and three cards in an "unbid" suit. Same species as `two_of_top3` in
  round 5.

### Residue — audit rows and families these twenty do not explain

- **The forcing new suit opposite a weak two is passed out.** `rw2_new_*` is
  `forcing: one_round` and `2$W - P - <new suit> - P - ?` has no context; a
  seven-card weak two passes it at `uc_pass` fit 1.00. Fourth instance of
  round 6's species, found while killing FIX 8.
- **`responder_after_minor_rebid` has a ceiling, not a shape hole.** 18 tables,
  mean **-2.78**, our gap **-5.00**; 19- and 23-counts sign off in `rmr_4H` /
  `rmr_3m` because `rmr_4NT` demands `semi_balanced`. Bigger than anything on
  this list.
- **The keycard ask over a light advance.** Board 86's -10 is `gst_rkc_S` asking
  opposite an 8-point advance of a balancing double, not the advance itself. Same
  family as the twice-measured, twice-unfixed ask over a game raise.
- **`ballow_nt2_strong` bids losing 2NTs on both sides of every separator I
  tried** (partner limited / unlimited, 8 tables, both halves negative in par
  gap). If the family is ever worth deleting, that is the argument — not a gate.
