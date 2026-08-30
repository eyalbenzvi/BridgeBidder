# Adversarial critique of the six round-15 fixes (seed 161616)

Reviewer: external, adversarial. Brief: kill what will not survive a corpus it has
never seen; a fix that ships must be one I could not break.

**Result: 1 SHIP (reshaped), 1 RESHAPE-as-structure-only, 4 KILL.**

The one survivor changes **0 calls on the 2,000 tables of `reports/e10_before.jsonl`**
and **1 call on its own corpus**, worth a determinable **+11**. Five of the six
reach zero or near-zero on an independent corpus, and **two of them cannot fire at
all**: FIX 1's `when` clause excludes 43 of the 43 positions it was written for, and
FIX 5's YAML does not load.

Nothing in the repo was modified except this file. Every prototype below was applied
with `yamledit`, replayed, and reverted with `git checkout`; the tree is clean.

---

## 1. What I built, and the corpora

**`myindex.py`** — an exact whole-corpus index. Every decision we made on every table
of a match file is re-asked through `prepare_decision` + **`fast_decision` itself**
(not a reconstruction), and recorded with the chosen call, **the rule object the
engine actually chose**, its fit and priority, the full candidate list, the board
margin and the par gap signed for us. Built for both corpora:

| corpus | seed | tables | our decisions | board margin/table | our par gap/table | our par gap/decision |
|---|---|---|---|---|---|---|
| `reports/e10_before.jsonl` | 242424 | 2,000 | **10,346** | **-0.73** | **-0.34** | **-0.02** |
| `reports/r15_batch.jsonl` | 161616 | 2,000 | **10,385** | -0.67 | -0.29 | -0.02 |

`e10_before.jsonl` is the independent corpus every denominator below is computed on.
**Caveat, and it is new:** e10 was recorded *before* round 14 shipped, so **21 of its
10,346 decisions no longer reproduce** under the committed system — every one of them
a round-14 fix (`uc_nt_raise3` ×9, `trsa_game_H` ×2, `v3_D_4S`/`v3_D_4H`,
`cl_new_S1` ×2, `adx_neg_major_*` ×3, `r2c_place_3NT`, `tr_game_void_S`). The
*decisions* I re-derive are current; the *outcomes* attached to those ~20 tables are
stale. 0.2% of the corpus, and none of it touches any of the six. `r15_batch.jsonl`
reproduces with 0 mismatches.

**Prototype harness** — `yamledit` edit → whole-corpus re-index of both corpora in
separate processes (`_SETUP_CACHE` is keyed on `id(system)`) → per-decision diff →
`git checkout`. Every verdict marked VERIFIED was run this way. Limitation, same as
last round's: the replay re-asks each decision against the *recorded* auction, so a
changed call's downstream consequences are not counted.

---

## 2. Audit of the two measurement corrections in §0

### (a) `deciding_rule()` — **CORRECT, and stronger than claimed**

I did not take the 598-decision validation on trust. I replayed **20,731 decisions
across both corpora** through `fast_decision` itself and compared, per decision, both
the **call** and the **rule id** against `sweep.deciding_rule()`:

| | e10 | r15 |
|---|---|---|
| call mismatches | **0 / 10,346** | **0 / 10,385** |
| deciding-rule mismatches | **0 / 10,346** | **0 / 10,385** |
| decisions where the match row's `rule` field names a different rule | 407 | 386 |
| decisions with more than 12 candidates (`rank_at`'s default `top=12`) | 3,919 | 3,934 |

Three things I checked that could have broken it and did not:

- **`fast_decision` dedupes by call before filtering on fit; `deciding_rule` does
  not.** `_dedupe_by_call` keeps the first candidate per call in *score* order, and
  score is `fit * (0.7 + 0.003 * priority)`, so a same-call rule with a lower priority
  and a higher fit can survive dedupe while a higher-priority one is dropped. It is
  arithmetically possible for that to change the engine's pick; on 20,731 decisions
  it never does.
- **`rank_at`'s `top=12` truncation.** 38% of decisions have more than 12 candidates,
  so `index_corpus` is reading a truncated list. Re-running `deciding_rule` on the
  *untruncated* list gives the same answer every time: no candidate that clears
  fit 0.9 ever ranks below 12th on score.
- **`pass_forbidden` and the forced-bid floor.** These live inside `score_candidates`,
  which `rank_at` calls, so they are already applied. The match itself runs
  `decide_fast` with no `explanations` and no arbitration (`tools/match_ben.py:75`),
  which is exactly what `repro.ask()` reproduces — there is no arbitration path to
  misattribute.

**Verdict: §0(a) is right, and the brief understates it. Quote 20,731/0, not 598/0.**

### (b) The context-relative yardstick — **the effect is real; the implementation has two bugs, and used alone the yardstick is blind to the biggest defects in the corpus**

**The effect is real, and I can prove it harder than the brief does.** Per-context
mean par gap, computed independently on two different 1,000-deal corpora, for the 25
contexts with n ≥ 30 in both: **r = +0.971**. Context means run from `rkc_response`
-7.50/-7.34 to `sandwich_seat[D]` +2.84/+1.92 and reproduce across seeds almost
exactly. A rule's context is a genuine, stable confounder. §0(b)'s premise stands.

**Bug 1 — `rule_context_map()` pools every `$`-expansion under one label.** It does
`m.setdefault(r.id, cid)`, and an expanded context shares its rule ids across
expansions, so `ob_1NT` — which decides in `opener_rebid_1m_1M[C,S]`, `[C,H]`,
`[D,H]` and `[D,S]` — is filed under whichever expansion the loader emitted first,
and `by_ctx` then pools all four expansions into that one bucket. `--rank-rules`
prints `opener_rebid_1m_1M[C,H] … /ctx 66`; that expansion actually contains **21**
decisions. Consequence: the ctxgap the tool prints is a pooled family average, not
the rule's own context.

**Bug 2 — the rule is inside its own baseline.** For a rule that is a large share of
its context this drives the delta toward zero by construction. Leave-one-out
(`ctxgap` recomputed with the rule's own decisions removed) versus what the finding
quotes, on r15:

| rule | finding's DELTA | own expansion, LOO (r15) | same, e10 |
|---|---|---|---|
| `ob_1NT` | -0.15 | **-3.54** | +1.00 |
| `ob_rebid_2C` | -0.17 | -0.53 | -2.30 |
| `rr_nt_gf3_S` | -1.86 | **-6.38** | +2.86 |
| `rkc_5C` | -1.08 | -2.01 | -1.43 |
| `gr_rkc_general_S` | -0.36 | -0.79 | -8.50 (n=4, ctx-excl n=1) |
| `ob_1M1NT_3S` | -1.60 | -4.32 | -3.92 (n=1) |

Five candidates were killed on numbers that are wrong by 2 to 5 points. **The
conclusions still hold** — on the independent corpus `ob_1NT` runs at **+1.00** and
`rr_nt_gf3_S` at **+2.86** relative to their own contexts — so §0(b) reached the right
answer for arithmetic that does not support it. Fix the tool before the next round
uses it: group by `rule.context_id` (which `index_corpus` already has in the
candidate) and exclude the rule from its own baseline.

**The revision of the standing open item needs restating.** `gr_rkc_general_S`'s
-0.36 is 7 of 13 decisions compared against themselves. Done properly, across all
suits and both corpora:

| slice | e10 n | e10 imp | e10 gap | r15 n | r15 imp | r15 gap |
|---|---|---|---|---|---|---|
| `gr_rkc_general_*` (the ask) | 9 | **+1.33** | -7.89 | 12 | -0.92 | -8.00 |
| `slam_try_over_game_raise`, ask removed | 10 | -2.10 | -7.40 | 10 | +1.30 | -5.80 |

The finding's conclusion survives and gets *stronger*: on the independent corpus the
ask **wins +1.33 a table** while the rest of its context loses -2.10, and its par-gap
delta is **-0.49**. Round 8's indictment of the keycard ask over a game raise is
correctly retired. But note what that actually says: **nothing in that context is the
outlier because the whole context is 7 points below the corpus.**

**And that is the yardstick's failure mode, which §0(b) does not state.** A
context-relative delta can only ever find the worst rung *inside* a context. It is
structurally blind to a context that is uniformly bad — and on this corpus the
uniformly bad contexts are where the IMPs are (§7, Residue 2). Used alone, §0(b)
guarantees the round never looks at them. It has to be paired with a context-level
ranking, which the tool does not print.

### (c) A third correction the brief needs: **the corpus mean par gap is a mixture, and it is the wrong baseline for both ends of the auction**

The per-decision corpus mean of **-0.02** is not the per-table baseline of **-0.34**.
The difference is systematic — mean par gap by *which of our calls it is*:

| our call number | 1st | 2nd | 3rd | 4th | 5th | 6th+ |
|---|---|---|---|---|---|---|
| mean par gap, e10 | -0.34 | -0.34 | -0.30 | -0.18 | +0.12 | **+1.36** |
| mean par gap, r15 | -0.28 | -0.28 | -0.24 | -0.12 | +0.14 | **+1.03** |

Long auctions have better par gaps, and only long auctions have late decisions, so
"-0.02" is a length-weighted average that belongs to no decision. Against it an
opening or an overcall is over-indicted by ~0.3 and a fifth-or-later call is
*under*-indicted by up to 1.4. Every one of the six fixes except FIX 4 lives late in
the auction, so **the finding's own slices are worse than it says**, not better.
Every table below quotes a **stage-matched baseline**: the mean gap of all decisions
made at the same ordinal position.

---

## 3. Verdicts

### FIX 1 — the takeout doubler has no notrump rebid — **KILL AS WRITTEN. The diagnosis is real; the patch cannot fire, and the half that pays is a different rule.**

**The population is real and it replicates.** Our own pass (`uc_pass`/`cl_pass`)
after our own takeout double, holding 13+:

| | n | imp/decision | our gap | stage-matched baseline | W/L |
|---|---|---|---|---|---|
| **e10 (independent)** | **32** | **-3.25** | **-3.16** | **+0.10** | 6/20 |
| r15 (own corpus) | 40 | -2.30 | -3.85 | +0.01 | 5/23 |

That is the largest replicated population in the round and the finding deserves
credit for it. Note two things it does not say. First, its headline denominator
(-6.22 gap, -6.67 margin on 18 decisions) is computed on **audit rows only** — the
decisions BEN disagreed with — which is selection on the outcome; the whole-corpus
figure is -5.25/-3.85. Second, by §0(b)'s own yardstick `uc_pass` is **above** its
context on both corpora (delta **+0.81** e10, **+1.15** r15): the rule is not the
outlier, the *slice* is, and against `general_uncontested_continuation`'s own -2.12
the slice is only -3.13 — most of the damage belongs to round 12's documented
"`uc_*` decides competitive auctions" open item, not to a missing notrump rung.

**The rung cannot fire. VERIFIED, twice.**

Its `when` is `we_bid_last: false, their_last_bid_suit: true` — the standing bid is
theirs. But `general_uncontested_continuation`'s pattern is `... - P - ?`: RHO has
just passed, so the standing bid is *partner's advance*. Counted over the whole
corpus:

| | standing bid is OURS | standing bid is THEIRS |
|---|---|---|
| `uc_pass` after my double, 13+, e10 | **20 / 20** | 0 |
| `uc_pass` after my double, 13+, r15 | **23 / 23** | 0 |

Prototyped exactly as written (2NT rung in `general_uncontested_continuation` plus
the `cl_` mirror): **0 call changes on 2,000 e10 tables.** On its own corpus, 3
changes — **none of them a motivating board**:

```
106a  QJ2.AQ9.A5.KQJ63  1C P P 1D X P P 1H    P(cl_pass)        -> 2NT(cl_doubler_nt2)
462a  K3.AQ5.AKT854.QT  P 1NT X P P 2S        3D(cl_new_D3_hi)  -> 2NT(cl_doubler_nt2)   <- a natural bid in a SIX-card suit
509a  A3.A72.KJ865.AQ5  1NT X P P XX P 2C P 2D  P(cl_pass)      -> 2NT(cl_doubler_nt2)   <- a table we WIN +5
```

**Even with the `when` repaired it reaches 1 of its own 4 boards.** Checked hand by
hand against the proposed `requires`:

| board | why it does not fire |
|---|---|
| 351a `A53.KQ9.AK86.KJT` | fires, once `we_bid_last: true` replaces `false` |
| 559a `3.AK32.QJ3.AKQ93` | **`semi_balanced` = 0.0** (1-4-3-5). The gate excludes it outright |
| 818a `K86.KQ.AK73.AK84` | **22 HCP, not the 20 the brief prints.** Against `hcp: [18, 21]` that is fit 0.80, below the 0.9 fast path |
| 79a `AT32.JT4.AKJ8.A2` | not a starved seat at all: it is `ballow_nt2_strong` bidding 2NT at fit 0.965, and **BEN's call there is PASS at 0.95** — the row argues *against* the fix |

**And the notrump rung is the small half.** Classifying the 13+ population by what
the hand actually wanted to bid:

| | e10 n | e10 imp | e10 gap | r15 n | r15 imp | r15 gap |
|---|---|---|---|---|---|---|
| semi-balanced 18+ → wants a **notrump** rebid | **3** | -2.67 | -5.00 | 6 | -3.17 | -9.00 |
| holds a **5+ card suit of its own** → wants a suit rebid | **11** | **-5.45** | **-7.64** | 13 | -3.69 | -3.38 |
| neither | 6 | -1.50 | -1.00 | 4 | -0.50 | -2.50 |

Two of the three e10 notrump-shaped hands have partner's advance at the **four
level**, where a notrump rebid is 4NT and does not exist. The reachable notrump
population on the independent corpus is **one table in two thousand**.

**ENDANGERS** (if a repaired version were shipped anyway): priority 34.5 sits above
`uc_doubler_raise_$X` (34) and `uc_doubler_raise3_$X` (33), so an 18-19 semi-balanced
hand with four-card support for partner's advance would bid 2NT instead of raising —
round 14's price-against-the-rungs-below hazard, in the same shape. It also leans on
`weakest_their_stopper`, which does not gate.

**HIGH-VARIANCE: yes** (1 reachable table held out).
**VERIFIED** (prototype, both corpora, plus hand-by-hand gate arithmetic).

**What to do instead** — the 11-table half, prototyped, in Residue 1 below. It is
the same finding round 14's reviewer left in *its* residue ("the takeout doubler
rebids his own long suit at the four level over partner's minimum advance — boards
2a, 485a, 110a"), and boards 2a and 485a are still sitting in this corpus, still
passing.

---

### FIX 2 — `ballow_nt2_balance` denies no shape — **RESHAPE, ship only inside a zero-reach structure bundle. Claim nothing on score.**

**The rule decides nothing at all in 2,000 independent tables.**

| | e10 | r15 |
|---|---|---|
| `ballow_nt2_balance` decides | **0 decisions** | 4 decisions |
| … with a 5+ card major | — | 2 |
| … with a 6+ card major | — | **0** |
| imp / gap | — | -8.00 / -7.25 (stage baseline -0.18) |
| context `general_balancing_low` | +0.21 gap | +0.48 gap |

VERIFIED prototype of the gate exactly as proposed: **0 call changes on e10**, 2 on
r15 — both motivating boards, both landing on `ballow_new_S2` at fit **1.00**, so the
landing claim is correct. A gate that reaches 0 on the corpus it was not found on can
only subtract held out. That is round 14's FIX 14 kill criterion verbatim.

**Two corrections to the finding.** The HCP counts are both wrong: 613a
`KQ732.A3.A83.Q43` is **15**, not 14; 741a `QJ963.A52.AKJ.83` is **15**, not 13. Both
hands sit exactly on the floor of the rule's own `hcp: [15, 21]`, i.e. they are
legitimate balancing 2NTs on range, not the 13-14 overbids the table implies.
Correcting the count weakens the finding rather than strengthening it.

**And the fix commits the species it names.** The true sibling of
`ballow_nt2_balance` is not `ballow_nt1` (a *one*-level rung) but
`ballow_nt2_strong` — same context, same call, same `standing_bid_level: [2]`, same
`weakest_their_stopper` + `semi_balanced` pair, **and no shape condition either**:

```yaml
      - id: ballow_nt2_strong
        call: 2NT
        priority: 30
        when: { side_has_acted: true, their_last_bid_suit: true, standing_bid_level: [2] }
        requires:
          hcp: [17, 21]
          evals: { weakest_their_stopper: [0.9, 9], semi_balanced: [1, 1] }
```

It decides 7 e10 / 9 r15 decisions at gap -2.57 / -4.78 — a *larger* population than
the rule being fixed. Gating one and not the other re-creates "a gate given to one
sibling and not the other" one rule along. But sweeping the denial onto the strong
sibling would be bad bridge: with 19 balanced and five spades you cannot bid a
non-forcing 2S. Which shows the diagnosis is a **range** statement, not a shape one.
Express it that way, so it says one sentence of bridge and needs no sibling sweep:

```yaml
# ballow_nt2_balance, AFTER - replacing the finding's unconditional `not:`
        requires:
          hcp: [15, 21]
          evals: { weakest_their_stopper: [0.9, 9], semi_balanced: [1, 1] }
          any_of:
            # From 17 the notrump is worth more than the suit and 2S would be
            # a non-forcing underbid; on a bare 15-16 the five-card major is
            # the better description.  ballow_nt1 denies SIX at the one level;
            # this is the two-level statement of the same idea.
            - hcp: [17, 21]
            - not: { any_of: [ { suits: { H: [5, 13] } }, { suits: { S: [5, 13] } } ] }
```

- **VERIFIED** for the finding's own form (0 e10 / 2 r15). The band-conditional form
  above is the same 2 boards (both are 15-counts) and the same 0 on e10.
- **ENDANGERS**: a 15-16 balancing hand with a five-card major stops showing 15-21
  balanced and shows 5+ and 10+ instead — partner's read of the 2S widens downward.
- **HIGH-VARIANCE: no** — because its reach held out is zero. Bundle with structure.

---

### FIX 3 — `balhigh_reopen_X` doubles on 5-5 two-suiters — **KILL**

**The named shape reaches 0 of 2,000 independent tables.** Every hand the rule
decides on e10, with its shape:

```
134b  A762.K6.AQ.AT874   17   5-4-2-2   (-6, gap -6)   P 1C 3D P P
294b  AJ864.QJ.AQ82.K4   17   5-4-2-2   (-7, gap -10)  1H X P 1S 2C 2S 3H P P
560b  42.AQT6.AKQJ.K74   19   4-4-3-2   (+0, gap -7)   P 1D 3S P P
865a  74.K6.AKQ84.AKJ9   20   5-4-2-2   (+3, gap +2)   P 1D P 1H 2S P 3S P P
```

Not one is 5-5. A second-longest-suit cap of 4 — the fix the finding actually wants —
changes **nothing** here.

**And it is 2 of 6 on its own corpus, not 4.** The finding's evidence table lists
454b (5-3-5-0), 500b (1-2-5-5), 236b (3-2-5-3) and 551a (4-5-4-0). Only **454b and
500b** are 5-5; 236b is 5-3-3-2 and 551a is 5-4-4-0, and both would survive the
proposed cap untouched. The fix is a two-board gate.

**The offered alternative is worse, and I measured it.** `longest_suit_length: [0, 5]
→ [0, 4]`, VERIFIED:

| corpus | call changes | what they become |
|---|---|---|
| **e10** | **3** | **all three become `balhigh_pass` at fit 1.00** — 134b, 294b, and **865a, a table we currently win +3 at par gap +2.00** |
| r15 | 5 | 3 become `balhigh_pass`; only the two genuine 5-5s (454b → `balhigh_new_D3`, 500b → `balhigh_new_C4`) find a bid |

So on the corpus it was not found on, the crude version deletes the double from three
hands with a *single* five-card suit — the shape the finding does not accuse — and
silences the seat entirely on all three. The seat behind the deleted double is
`balhigh_pass` (`requires: {}`, priority 21), which is the round-14 FIX 8 shape:
the replacement is a catch-all, not an agreement.

**Sibling problem.** `yamledit` refused my first edit because the `requires` block is
**character-identical in two rules**: `ballow_reopen_X` carries the same
`hcp: [16, 40]` + `max_their_suit_length: [0, 2]` + `longest_suit_length: [0, 5]`.
It decides 7 e10 / 4 r15 decisions at gap -4.71 / -4.75, i.e. it is just as bad.
Gating the high one alone creates the asymmetry the round keeps finding.

**Precedent.** DECISIONS, round 7, with whole-corpus data: "a takeout double must not
hide a six-card suit" was killed — doubles WITH a 6+ suit average -2.00/table, WITHOUT
-2.54. Length gates on doubles have been measured negative in this file before.

| slice | n | imp | gap | stage baseline | ctx `general_balancing_high` gap | delta |
|---|---|---|---|---|---|---|
| e10 | 4 | -2.50 | -5.25 | -0.09 | +2.35 | **-7.60** |
| r15 | 6 | -6.00 | -7.50 | +0.05 | +2.67 | -10.17 |

The delta is real and replicates. The *shape hypothesis* does not. **KILL.**
**VERIFIED. HIGH-VARIANCE: yes** (0 reachable tables held out for the precise form; 3
subtractions including a winner for the crude one).

---

### FIX 4 — the takeout double above 15 HCP is a different animal — **KILL as a fix; keep as the round's best-replicated diagnosis**

The finding explicitly proposes no repair and asks that it be measured with FIX 1.
FIX 1 as written changes **0 calls**, so there is nothing to measure it with.

**The par-gap half of the claim replicates; the board-margin half does not.**

| slice | e10 n | e10 imp | e10 gap | r15 n | r15 imp | r15 gap |
|---|---|---|---|---|---|---|
| corpus | 10,346 | -0.77 | -0.02 (stage -0.34 here) | 10,385 | -0.75 | -0.02 |
| `oc1H_X` all | 11 | -2.18 | -3.45 | 20 | -2.25 | -3.65 |
| `oc1H_X` 16+ | 9 | -1.89 | **-4.89** | 9 | -4.33 | -7.78 |
| `oc1H_X` 10-15 | 2 | -3.50 | +3.00 | 11 | -0.55 | -0.27 |
| `oc1{H,S}_X` 16+ (pooled, n usable) | **11** | **-1.73** | **-5.36** | 13 | -3.08 | -7.08 |
| `oc1{H,S}_X` 10-15 | 13 | -2.31 | -2.46 | 16 | -0.19 | +0.88 |

On the independent corpus the strong double is **-5.36 gap against a stage-matched
-0.34** — a genuine, replicated, 11-table hole. But its **board margin is better than
the weak double's** (-1.73 vs -2.31), which is the reverse of r15. The two metrics
disagree, and the finding's "the 10-15 half is at or above baseline on both metrics"
is an r15-only reading.

`oc1H_1NT` is not the answer either: it decides 3 e10 tables at **imp +3.00**, and
widening it is the fourth attempt in this file to author a strong balanced overcall
(round 8's `weakest_their_stopper` repair, -9 held out; round 14's FIX 18, -1 held
out and reverted; round 14's residue). DECISIONS says the seats behind those hands
must be authored first. That is Residue 1, not this.

**KILL as a fix. HIGH-VARIANCE: n/a. VERIFIED** (denominator only; there is nothing
to prototype).

---

### FIX 5 — `defense_vs_1NT` has no strong natural overcall — **KILL, four times over**

**1. The YAML does not load.** `defense_vs_1NT` has no `expand:` block, so `$M` never
expands:

```
ValueError: Bad strain '$M'
  bridgebidder/domain/calls.py:37, from BidRule.from_dict -> Call.parse("2$M")
AssertionError: SYSTEM FAILED TO LOAD after edit
```

The id `v1NT_2$M_strong` also violates ROUND_METHOD's "template vars must END a rule
id". Fourth round running for a patch that does not do what it says on the file.

**2. It misquotes the rules it indicts.** "The natural rungs … demand **six** cards"
is true of `v1NT_2C`/`v1NT_2D` and **false of both majors**:

```yaml
      - id: v1NT_2S
        requires: { suits: { S: [5, 13] }, hcp: [8, 15], features: [ "good_suit(S)" ] }
      - id: v1NT_2H
        requires: { suits: { H: [5, 13] }, hcp: [8, 15], features: [ "good_suit(H)" ] }
```

The barrier for a good five-card major is the **15 HCP ceiling**, not length.

**3. It is a re-rank wearing additive clothing, and I measured that.** Raising the
ceiling on all four natural rungs to 18 — the direct reading of the diagnosis —
changes **0 calls on e10 and 0 on r15**, because `v1NT_X` sits at priority 70 above
them at 60/61 and both fit ≥ 0.9, so the double wins on priority regardless of band.
The only thing that moves a call is the priority **71**. The fix is therefore not
"ADDITIVE: a strong natural rung"; it is a subtraction of the penalty double, and it
should be judged as one.

**4. The family is healthy and the double is above baseline on the corpus it was not
found on.**

| slice | e10 n | e10 imp | e10 gap | r15 n | r15 imp | r15 gap |
|---|---|---|---|---|---|---|
| `defense_vs_1NT` context | 129 | -0.33 | **+2.91** | 139 | -0.19 | +2.78 |
| `v1NT_X` | **3** | **+0.00** | **+2.00** | 9 | -0.67 | -2.33 |
| `v1NT_2S` | 8 | -1.62 | +0.75 | 4 | -2.75 | +4.00 |
| `v1NT_2H` | 6 | -2.33 | -0.83 | 7 | -1.00 | +3.29 |

Above the stage-matched baseline (-0.34) on both metrics on the independent corpus.
This is round 14's FIX 19 — killed on `defense_vs_1NT` being "129 tables, mean -0.33,
gap +2.91" — with the same numbers a corpus later.

**5. Corrected so it loads (two explicit rungs at priority 71), VERIFIED:** **0 call
changes on e10.** On r15, 3 changes: two motivating boards (214b, 550b) and one
collateral — **224a `KJT953.J63.AK.A2`, a table we currently win +4 at par gap
+4.00**, whose penalty double becomes 2S. The other two motivating boards are
unreachable: 462a is a **diamond** hand (the rung is majors only) and 410b's `J8752`
fails `good_suit`, which is sharp at 0.05. **The fix reaches 2 of its own 4 boards
and buys a winner's double with them.**

**KILL. VERIFIED. HIGH-VARIANCE: yes** (0 reach held out, and it subtracts a call in
the healthiest family measured).

---

### FIX 6 — the advance of a takeout double has no jump — **RESHAPE, then SHIP. The only survivor.**

The diagnosis is right and the seat is genuinely empty. Board 970b, East
`AKQT92.J75.J87.9` over `3C - X - P`, the **entire** candidate set:

```
   3S  adx_pull_S3   fit 0.409  prio 58
   3H  adx_pull_H3   fit 0.019  prio 57
   3D  adx_pull_D3   fit 0.019  prio 56
   3NT uc_nt3        fit 0.000  prio 29
```

Four candidates, top fit **0.409**; the passes are filtered because partner's double
is `forcing: one_round`. This is not "a range with no rule" — `adx_pull_S3` is
`total_points: [0, 11]` and the hand is over it, so the call is a **soft-miss lottery
pick at 0.409**, which the finding does not say. Two of the four r15 firings (90b,
970b) are below the fast path.

| slice | e10 n | e10 imp | e10 gap | stage baseline | ctx `general_pull_or_sit` gap | delta |
|---|---|---|---|---|---|---|
| `adx_pull_S3` | 4 | **-5.00** | **-7.25** | +0.21 | -3.87 | -3.38 |
| same, r15 | 4 | -7.25 | -10.00 | -0.03 | -2.95 | -7.05 |

Replicates on both corpora. **The new rung's reach on e10 is 0**: none of the four
e10 hands holds six spades with 12+ points.

**Two things must change before it ships.** The finding gives no YAML; mine, and both
corrections were forced by the tools:

```yaml
# general_pull_or_sit, AFTER - inserted immediately after adx_pull_S3
      - id: adx_pull_S4
        call: 4S
        priority: 58
        # NOT cheapest_in_suit: over a three-level preempt this is a JUMP, and
        # cheapest_in_suit excludes jumps - the rung would be unreachable.
        when: { unbid_suit: S, their_last_bid_suit: true, i_have_acted: false }
        requires:
          suits: { S: [6, 13] }
          # suit_diff carried from the rest of the adx_pull family: without it
          # `tools/lint_system.py --only sibling` reports the rung and
          # tests/test_lints.py::test_rule_families_are_gated_consistently FAILS.
          evals: { total_points: [12, 40], "suit_quality(S)": [2, 9],
                   "suit_diff(S,H)": [0, 13], "suit_diff(S,D)": [0, 13], "suit_diff(S,C)": [0, 13] }
        shows: "jump to game in my own six-card suit opposite the takeout double: 12+ points and a good suit"
        establishes: { forcing: sign_off, agreed_suit: S }
# ... and the identical H twin (adx_pull_H4, call 4H, priority 57) after adx_pull_H3.
```

- **VERIFIED.** Whole-corpus replay: **0 call changes on 2,000 e10 tables**, 1 on r15
  (board 970b, `3S` → `4S` at fit 1.00). `tools/lint_system.py`: 223 findings, gap 0,
  shape 0, sibling 0, soft 0 — identical to the committed system. `pytest`: **759
  passed**. My *first* version, without the `suit_diff` clauses, produced 2 `sibling`
  lints and broke `test_rule_families_are_gated_consistently` — round 14's "run the
  full suite before you believe a number", live, on my own prototype.
- **Determinable value +11, computed exactly.** Board 970 is E/W vulnerable; East
  takes **12** tricks in spades double-dummy. Table B goes 3S+3 (-230 for N/S) to
  4S+2 (-680); table A is BEN's 3NT+2 (-660). `imps(sa - sb)`: -10 → **+1**. The
  opponents passed throughout, so the contract is determined — unless BEN's South,
  holding `J8.83.K4.AT87543`, saves in 5C over 4S, which takes six tricks and would
  make it better still.
- **ENDANGERS: nothing measurable.** The bands are disjoint (`adx_pull_S3` caps at 11
  total points, this floors at 12), the seat has no fit-≥0.9 candidate to displace,
  and `adx_sit`/`adx_pass_min` are unreachable there because pass is forbidden. The
  one real hazard is the fallback-suppression mechanism in §4 below; it produced 0
  changes here on both corpora, which is the check, not the assumption.
- **HIGH-VARIANCE: yes on the number** (one board, and the rung is 0/2000 held out),
  **no on the mechanism**. Ship it as structure with a determinable board attached;
  do not promise IMPs held out.

---

## 4. The measurement fact that matters most: **an added rung deletes the code fallback for its call, and "additive is safe" is false as stated**

`prepare_decision` builds `covered` from every rule whose `when` holds and whose call
is legal — **fit is never consulted** (`inference/engine.py:483-490`) — and
`generate_fallbacks` then generates "generic candidates for calls NOT covered by
system rules". So adding a rung removes the code fallback for that call in every seat
its `when` reaches, whether or not the hand fits the rung.

I hit this with my own prototype and traced it. Board 691a, North
`A.A93.J98.Q75432` after `1S X P 2S 3S P P 4D P`:

```
BASELINE                        WITH FOUR NEW uc_doubler_own_$X4 RUNGS
  4H  FALLBACK  fit 1.00 p1       4NT gst_rkc_D          fit 0.066 p46   <- chosen
  4NT gst_rkc_D fit 0.066 p46     5D  uc_minor_game_5D   fit 0.047 p28
  5D  uc_minor  fit 0.047 p28     4H  uc_doubler_own_H4  fit 0.000 p28.5
```

The fit-1.00 fallback is deleted by a rung that fits **0.00**, and a **fit-0.066
keycard ask** takes the seat. Round 14's reviewer saw the same fit-0.066 `gst_rkc_D`
on the same board 691a from a different fix and reported it as a curiosity; this is
the mechanism.

The consequences are general:

- The guardrail "a fix that ADDS a rung fills a hole and is safe" needs amending to
  **"a new rung is safe only where no fallback covered its call, or where the rung
  fits every hand the fallback caught"** — and that has to be measured, because the
  `when` clause is auction-only and the fit is hand-dependent, so no `when` can
  restrict the suppression to the hands the rung wants.
- The fallback is not a rare backstop. It decides **456 of 10,346 e10 decisions and
  474 of 10,385 r15 decisions** — 4.5% of everything we do — at fit 1.00 by
  construction. See Residue 2.
- It explains part of why additive fixes have under-delivered held out relative to
  their in-sample blast radius: the blast radius counts the seats the rung *wins*,
  not the seats where it silently removed the fallback and let a soft-miss through.

Every survivor in this review was re-checked for it. FIX 6: 0 changes on both
corpora, so it does not bite. Residue 1: it does bite, and that is why Residue 1 is
not shipped.

---

## 5. Audit of the "Ruled OK" section

Whole-corpus, both corpora, stage-matched. **Six of the nine rulings are right and I
confirm them. Two are wrong, and one is right but badly understated.**

| ruled OK | whole-corpus e10 | whole-corpus r15 | verdict |
|---|---|---|---|
| `cl_pass -> X` | `cl_pass` 1,004 decisions, imp -0.72, gap **+2.29** vs stage -0.18 | 1,006, -0.70, **+2.76** | **RIGHT** — and stronger than the finding says; above baseline on the attributable metric on both corpora |
| `open_pass` | 849 decisions, imp -0.59, gap **+1.11** vs stage -0.34 | 866, -0.70, **+0.79** | **RIGHT.** Also: **0 firings with 12+ HCP** on either corpus — there is no opening-values pass to find |
| `rkc_5C` | 13 decisions, gap -8.31; ctx `rkc_response` -7.50; LOO delta **-1.43** | 19, -8.42; ctx -7.34; LOO **-2.01** | **RIGHT as a rule.** But see Residue 2: the *context* is -7.50/-7.34 on 30/41 decisions and nobody has ruled on it |
| `rw2_2NT_ask` | 15 decisions, imp -0.27, gap -2.20, LOO delta **-4.60** | 11, -1.09, **-5.45**, LOO **-11.45** | the finding kills its own *proposed exception* correctly; the **rule** is 4.6-11.5 below its context on both corpora and is left standing. Residue 4 |
| `uc_raise_S3` | 13, imp -0.77, gap -0.46, delta +1.65 | 17, -2.41, -2.65, delta -0.02 | **RIGHT** |
| **`uc_nt2`** | **18 decisions, imp -3.11, gap -4.56** vs stage **-0.20**, delta -2.44 | **27, -2.48, -3.93**, delta -1.30 | **WRONG — let go on the wrong number.** The finding's "(7, -0.71)" counts *audit disagreements*, not the rule's population. This is 18/27 tables on two independent corpora at four times the corpus board margin, and it is larger than any population the six fixes propose to change |
| `cl_new_S2_hi` | 12, imp -0.67, gap +2.17 | 17, -1.88, +0.65 | **RIGHT** |
| `cl_new_C3_hi` | 10, imp **-4.10**, gap -0.40 | 4, +0.75, +4.50 | **half wrong.** The finding quotes the r15 gap (+0.33) only. On e10 the board margin is -4.10 against -0.77 on 10 tables with 1 win and 7 losses. The two metrics disagree, so it is a "not enough", not a "not a defect" |
| `sw_X` | 16, imp -0.88, gap **+0.94** vs stage -0.34 | 12, -0.83, -1.42 | **RIGHT** — and the independent corpus is kinder to it than r15 |
| `open_2C` | 16, imp -0.19, gap **-7.44**, delta -6.67 | 19, -1.89, **-6.58**, delta -5.90 | **right that it is not a rule to tune; badly understated as "ruled OK."** -7 par gap on ~17 tables replicating across two corpora is the largest single *replicated* rule-level hole named anywhere in the findings, and it has been deferred as an open item for three rounds |

**`uc_nt2` is the one you let go wrongly, and here is the mechanism.** It is the
generic 11-12 balanced 2NT with `rule_of_26: [21, 99]`, `semi_balanced`,
`weakest_their_stopper` — and no shape denial, unlike `ballow_nt1` and `cl_nt1`,
which both deny a six-card major.

| slice | e10 n | e10 imp | e10 gap | r15 n | r15 imp | r15 gap |
|---|---|---|---|---|---|---|
| `uc_nt2` all | 18 | -3.11 | -4.56 | 27 | -2.48 | -3.93 |
| … holding a 6+ card suit | 2 | -4.50 | -7.00 | 2 | -4.50 | -1.50 |
| … **fired below the 0.9 fast path** | **6 (33%)** | -3.83 | **-9.17** | **7 (26%)** | -2.86 | **-8.43** |
| … clean (fit ≥ 0.9, no six-bagger) | 11 | -3.00 | -2.45 | 18 | -2.11 | -2.44 |

A third of its firings are soft-miss lottery picks at 0.409/0.8/0.835/0.946, and
those run at -9.17 gap. Board 934b bids 2NT holding `KJ.QJ6.AQJT92.62` — **six
diamonds** — at fit 0.409. Board 70a bids it over `1S P 2C P 2S P` at 0.409, i.e.
the generic toolkit annexing an opener's-rebid seat. This is a bigger and better
replicated family than five of the six fixes and it was dismissed on an audit count.

---

## 6. ORDER OF WORK

Only one fix survives, so most of this is about what to measure *instead*.

**Bundle A — zero reach on the independent corpus; one measurement, expect 0 boards
changed held out. Keep on structure at zero measured cost (the round 7/8/11/13/14
precedent).**

1. **FIX 6 (reshaped)** — `adx_pull_S4` / `adx_pull_H4` with the `suit_diff` family
   gates and *without* `cheapest_in_suit`. 0 e10 changes, 1 r15 board, **+11**
   determinable.
2. **FIX 2 (reshaped to the band-conditional form)** — 0 e10 changes, 2 r15 boards.

These two cannot confound each other: different contexts
(`general_pull_or_sit` / `general_balancing_low`), different calls (4S/4H vs 2NT),
different auctions (advancing a takeout double vs balancing over a weak two), and
**their changed sets are empty on the corpus the number will be read on**, so any
held-out movement is attributable to neither and the bundle is a null-check on the
harness. Verify with a whole-corpus replay diff of 0 before spending a match.
Run `pytest`, `lint_system.py`, `fuzz_decisions.py --n 300 --strict` first — my FIX 6
prototype broke a locked lint test in its first form.

**Singles — must be measured alone if attempted at all.**

3. **Residue 1, `uc_doubler_own_$X4`** — the 11-table half of FIX 1. 3 e10 changes,
   2 r15. **Do not ship it as prototyped**: one of the three e10 changes is the
   fallback-suppression regression on 691a (§4). It needs either a rung that also
   catches the hands the 4H fallback was catching, or an explicit decision that the
   two good boards outweigh 691a. Alone, because it changes what a four-level suit
   bid MEANS in the most-fired context in the engine.
4. **`uc_nt2`** (§5) — 18/27 tables, the largest thing this round did not rule on.
   Alone, because it is a notrump rung in `general_uncontested_continuation` and
   would confound anything else touching that context, including Residue 1.

**Do not bundle 3 with 4.** Both live in `general_uncontested_continuation`; Residue 1
adds four-level candidates and `uc_nt2` re-bands 2NT, and round 14's FIX 2 × FIX 18
note is the precedent.

**Nothing else should be measured.** FIX 1 as written, FIX 3 (either form), FIX 4 and
FIX 5 either cannot fire or subtract from a population that is above baseline on the
independent corpus. Spending a match on them costs a round.

**One cross-fix interaction worth recording even though both are killed:** FIX 1 as
written and FIX 5 both change board **462a** — FIX 1 turns our natural 3D on
`AKT854` into 2NT, FIX 5 was written to reach that board and does not. Had both
shipped, the r15 numbers would have been unattributable.

---

## 7. KILLED, AND WHY — the negative results, with the number

| fix | verdict | the number that killed it |
|---|---|---|
| **1** the doubler's notrump rebid | **KILL as written** | the `when` is `we_bid_last: false`, and the standing bid is **ours in 20/20 e10 and 23/23 r15** of the positions it targets. Prototype: **0 call changes on 2,000 e10 tables**; 3 on r15, **none of them a motivating board**, one a table we win +5, one displacing a natural 3D on a six-card suit. With the `when` repaired it still reaches **1 of its own 4 boards**: 559a is `semi_balanced` **0.0**, 818a is **22 HCP** (not the 20 printed) so fit 0.80 against `[18,21]`, and 79a is `ballow_nt2_strong` with **BEN calling PASS at 0.95**. The half that pays is the doubler's own suit: **11 e10 tables at imp -5.45 / gap -7.64** vs 3 for notrump |
| **3** cap the reopening double's shape | **KILL** | **0 of the 4 e10 firings is 5-5** (5-4-2-2, 5-4-2-2, 4-4-3-2, 5-4-2-2), and only **2 of the 6 r15 firings** are, so the precise fix reaches **0/2000** held out. The offered alternative `longest_suit_length: [0,4]` makes **3 e10 changes, all three to `balhigh_pass` at fit 1.00**, including **865a which we currently win +3 at gap +2.00**. And `ballow_reopen_X` carries a character-identical `requires`, so gating one is the sibling asymmetry the finding names |
| **4** the 16+ takeout double | **KILL as a fix** | it proposes no repair and asks to be measured with FIX 1, which changes **0 calls**. On e10 the par-gap split replicates (**-5.36 vs -2.46**) but the board-margin split **inverts** (16+ is -1.73, 10-15 is -2.31), so "at or above baseline on both metrics" is r15-only |
| **5** a strong natural overcall of 1NT | **KILL** | the YAML **does not load** (`defense_vs_1NT` has no `expand:`; `Call.parse("2$M")` → `ValueError: Bad strain '$M'`); `v1NT_2H`/`v1NT_2S` require **five** cards, not six, so the barrier is the 15 ceiling; **raising that ceiling to 18 changes 0 calls on both corpora**, proving the fix is the priority 71, i.e. a **re-rank, not an additive rung**; corrected so it loads it makes **0 e10 changes** and 3 on r15, one of which (**224a, +4 IMPs, par gap +4.00**) loses a winning penalty double; and `defense_vs_1NT` is **129 decisions at gap +2.91** on e10 — round 14's FIX 19 kill, verbatim |
| **2** deny a 5-card major on the balancing 2NT | **KILL as written / structure only** | the rule **never decides anything in 2,000 e10 tables**; the gate's reach held out is **0**; both HCP counts in the evidence table are wrong (**15 and 15**, not 14 and 13, i.e. both hands are inside the rule's own `hcp: [15,21]`); and the true sibling `ballow_nt2_strong` — same call, same context, same level, **also no shape gate**, 7/9 decisions at gap -2.57/-4.78 — is untouched, re-creating the species |

Three further negative results from my own prototypes, reported rather than shipped:

- **`uc_doubler_own_$X4` (Residue 1) regresses board 691a** through fallback
  suppression (§4): 4H at fit **1.00** is replaced by a keycard ask at fit **0.066**.
  Good bridge, 3 e10 changes, and not shippable as written.
- **`v1NT_2C/2D/2H/2S` ceiling 15 → 18: 0 call changes on both corpora.** A band
  extension under a higher-priority rule that already fits is invisible. Worth
  remembering the next time a fix is justified as "widening the band".
- **`adx_pull_S4`/`H4` without `suit_diff` breaks a locked lint test.** Two `sibling`
  findings and `test_rule_families_are_gated_consistently` fails. The lint knew
  before the corpus did.

---

## 8. RESIDUE — what the six do not explain about -667

The six fixes, all six of them shipped in their best form, would change **1 call on
2,000 independent tables**. Here is where -667 actually lives. Everything below is
computed on both corpora and quoted where it replicates.

**1. The doubler cannot rebid his own suit, and the four-level new suit does not
exist in the uncontested toolkit.** `uc_new_$X` stops at the three level and
`uc_rebid_$X4` requires `my_suit: $X`, which a doubler never satisfies. Board 485a,
`9.K.AKQ532.AQ985` — 18 HCP, 6-5 in the minors — after `P P 3C X P 3S P` has a
candidate set of **four rules, one of which fits**: `uc_pass` at 1.00. Board 2a,
`AQ6.KJ84.AKQT95.` (19, 6 diamonds), the same. The population is **11 e10 tables at
imp -5.45 / gap -7.64 against a stage-matched +0.10**, and 13 on r15. Round 14's
reviewer named it in *its* residue and named boards 2a and 485a by number; a round
later they are still passing. Prototyped
(`uc_doubler_own_C4/D4/H4/S4`, priority 28.5, `when: { my_last_call_was_double: true,
we_bid_last: true, we_hold_contract: false, unbid_suit: $X, cheapest_in_suit: true }`,
`suits: {$X:[6,13]}`, `total_points: [16,40]`, `suit_quality($X): [2,9]`): **3 e10
changes, 2 r15 changes**, both boards 2a and 485a flip to 4D at fit 1.00 — and the
third e10 change is the 691a fallback regression. **This is the round's most valuable
unshipped item and it needs the §4 problem solved first.**

**2. The code fallback is the largest attributable population in the engine, and
nothing has ever ruled on it.**

| | e10 | r15 |
|---|---|---|
| decisions decided by a code fallback | **456 (4.4%)** | **474 (4.6%)** |
| board margin / decision | -0.51 | -0.26 |
| our par gap | **-3.89** | **-4.17** |
| stage-matched baseline gap | +0.46 | +0.41 |
| total attributable gap | **≈ -1,980** | **≈ -2,170** |

Four and a half percent of our calls are made with **no rule at all**, four points
below where decisions at that stage sit. It is bigger than every named family
combined, it replicates to within 0.3, and §4 shows that every "additive" fix quietly
edits it. The next round should start by dumping the fallback population grouped by
`(context, call)` — that is a map of every hole in the file, produced by the engine
itself.

**3. The responding family is a uniform three-to-four point hole and the
context-relative yardstick cannot see it.** Contexts ranked by total attributable par
gap (n × distance from the corpus mean), e10, with the r15 replication beside it:

| context | n (e10) | gap (e10) | imp (e10) | n (r15) | gap (r15) |
|---|---|---|---|---|---|
| FALLBACK | 456 | -3.89 | -0.51 | 474 | -4.17 |
| `general_uncontested_continuation` | 736 | -2.12 | -1.05 | 777 | -2.63 |
| `resp_1m[D]` | 121 | **-4.12** | -0.61 | 121 | -2.93 |
| `resp_1H` | 78 | **-4.64** | -0.97 | 70 | -2.91 |
| `general_pull_or_sit` | 84 | -3.87 | -0.87 | 94 | -2.95 |
| `resp_1NT` | 90 | -3.54 | +0.23 | 97 | -3.55 |
| `resp_1m[C]` | 100 | -3.00 | +0.16 | 104 | -3.41 |
| `resp_1S` | 86 | -2.93 | -0.76 | 93 | -3.65 |
| `rkc_response` | 30 | **-7.50** | -0.93 | 41 | -7.34 |
| `opener_rebid_1H_1S` | 30 | -6.07 | -2.37 | 24 | -3.12 |
| `general_slam_try` | 10 | **-12.10** | -3.90 | 11 | -7.73 |
| `resp_2C` | 15 | -7.87 | -0.60 | 18 | -6.33 |
| `slam_try_over_game_raise[H]` | 14 | -7.93 | -1.57 | 9 | -8.56 |
| `quant_raise_of_3NT` | 11 | -9.09 | +1.09 | 6 | -8.50 |
| `gf_landing_nt` | 10 | -9.00 | -0.70 | 17 | -7.59 |

The five responding contexts are **475 decisions at -3 to -4.6 on both corpora** —
about -1,700 attributable gap-points, the largest coherent *bridge-shaped*
concentration in the file — and not one rule inside them shows up on `--rank-rules`,
because every rung in a uniformly bad context sits at its own baseline. This is the
blind spot of §0(b) stated as a number. `opener_rebid_1H_1S`, which round 14's
reviewer flagged as the largest non-slam family, is still there at -6.07.

**4. The soft-miss lottery, quantified whole-corpus for the first time.**

| | e10 | r15 |
|---|---|---|
| decisions with no candidate at fit ≥ 0.9 | **109 (1.1%)** | 102 (1.0%) |
| board margin / decision | **-1.91** | -2.30 |
| our par gap | **-5.72** | -6.52 |
| stage-matched baseline | -0.17 | -0.10 |
| losing tables with at least one such decision | 42 of 652 (6%) | 31 of 644 (5%) |

One percent of decisions, at **5.7 points of par gap each** — roughly -620
attributable gap-points, replicating to within 0.8. This is the population where the
engine has no agreement at all and picks the least-bad miss. It overlaps Residue 2
(the fallback fits 1.00, so a fallback decision is *not* in this count — these are
109 seats where even the fallback was absent or worse). Two of `uc_nt2`'s worst
firings and both of FIX 6's are in it.

**5. `rw2_2NT_ask` was left standing while its own proposed exception was killed.**
15 e10 / 11 r15 decisions, imp -0.27 / -1.09, gap -2.20 / -5.45, and **leave-one-out
against its own context -4.60 / -11.45**. The finding correctly refuted the
singleton-versus-void hypothesis on its own numbers and then filed the rule under
"ruled OK". The rule is 4.6 to 11.5 points below its context on two independent
corpora; the hypothesis was wrong, not the indictment.

**6. `open_2C` deserves better than "the documented open item".** 16 e10 / 19 r15
decisions at gap **-7.44 / -6.58** against a stage-matched -0.34/-0.29, delta -6.67 /
-5.90. It replicates almost exactly across seeds, which none of the six fixes' slices
does. DECISIONS already knows why (`r2c_2D_waiting` is `requires: {}`, so partner's
shown minimum after a 2C opening is zero by construction, and every
`rule_of_26_sharp >= 31` gate in the file is unreachable). It has been deferred in
rounds 12, 13, 14 and now 15. It is the single largest replicated rule-level hole in
the corpus and it should be the next round's subject rather than its footnote.

---

## Appendix — what the brief got factually wrong

| claim | what the file or the corpus says |
|---|---|
| FIX 1, 818a is "20 HCP" | **22.** `K86.KQ.AK73.AK84` = 3+5+7+7. Against `hcp: [18,21]` that is fit 0.80, below the fast path |
| FIX 1, "`uc_pass` … the 18 with 13+ HCP run at par gap -6.22 / board margin -6.67" | that is the **audit-disagreement subset**, selected on the outcome. Whole-corpus, after our own double at 13+: **-4.70 gap / -3.00 margin** (r15), **-5.25 / -3.85** (e10) |
| FIX 1, board 79a listed as a starved seat | it is `ballow_nt2_strong` bidding 2NT at fit 0.965, and **BEN's call is PASS at 0.95** |
| FIX 2, 613a is "14 HCP", 741a is "13" | **15 and 15.** Both sit exactly on `ballow_nt2_balance`'s own floor |
| FIX 2, `ballow_nt1` is "its one-level sibling" | its same-call, same-level, same-context sibling is **`ballow_nt2_strong`**, which also has no shape gate and decides more |
| FIX 3, "lets **5-5** through, which is the shape that most wants to bid" | of the 6 r15 firings, **2** are 5-5; of the 4 e10 firings, **0** are |
| FIX 5, the natural rungs "demand **six** cards" | `v1NT_2H` and `v1NT_2S` demand **five**. Only the minors demand six |
| FIX 5, "the fix is **ADDITIVE**" | a band widening changes **0 calls**; the effect is entirely the priority 71, i.e. a subtraction of the double |
| FIX 5, the YAML | **does not load.** `defense_vs_1NT` has no `expand:`; `id: v1NT_2$M_strong` also breaks the "template vars must END a rule id" rule |
| §0(b), "`ob_1NT` delta -0.15 … `rr_nt_gf3_S` -1.86 … `gr_rkc_general_S` -0.36" | computed against a **pooled** `$`-expansion baseline that includes the rule itself. Own expansion, leave-one-out: **-3.54, -6.38, -0.79** on r15. The conclusions survive on the independent corpus; the arithmetic does not |
| §0, "validated … on 598 consecutive decisions" | **20,731 decisions, 0 call mismatches and 0 rule mismatches.** Under-claimed |
| throughout, "corpus mean par gap -0.02" | that is a per-**decision** mixture. Per table it is **-0.34**, and it runs from -0.34 at our first call to **+1.36** at our sixth. Every late-auction slice in the findings is worse than stated |
