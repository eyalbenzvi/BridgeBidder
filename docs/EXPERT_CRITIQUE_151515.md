# Adversarial critique of the twenty round-14 fixes (seed 151515)

Reviewer: external, adversarial. Assignment: kill what will not survive a corpus
it has never seen, reshape what is right-but-wrongly-repaired, ship only what can
be defended with a denominator.

**Result: 7 SHIP, 5 RESHAPE-then-ship, 8 KILL.**
The twelve survivors, prototyped, change **34 calls on 33 of the 2,000 tables** of
`reports/e10_before.jsonl`; nine of those tables are attributable board-by-board
and are worth an estimated **+32 IMPs**, and the other 24 sit in three
single-measurement experiments that could go either way. The eight kills include
the two largest changes in the file.

Nothing in the repo was modified except this document.

---

## 1. Method, and three corrections to the brief

**Instruments built** (all in the scratch directory, none in the repo):

- `corpus.py` → `corpus_e10.jsonl`: all **10,346** decisions we made across all
  **2,000 tables** of `reports/e10_before.jsonl`, each re-asked through
  `prepare_decision` + **`fast_decision`**, recorded with its matched contexts,
  its full candidate ranking with fits and priorities, `pass_forbidden`, and the
  clear/unclear flag. Every denominator below is computed on this table.
- `replayp.py` + `runproto.sh`: a prototype YAML built by asserted surgical
  `yamledit` edits, replayed decision-by-decision **in eight separate processes**
  (`_SETUP_CACHE` is keyed on `id(system)`), diffed against the baseline. Twenty-two
  seconds per whole-corpus blast radius; every verdict below that says VERIFIED
  was run this way.
- `dd.py`: `EndplayDD` + the engine's own scoring, for board-level IMP estimates.
- `lintp.py`: `tools/lint_system.py` pointed at a prototype.

**Correction 1 — the corpus is exact, and its baselines are not the ones in the
brief.** All 10,346 decisions reproduce under the committed system with **0
mismatches**, so unlike round 13's copy nothing here is accurate only to 0.4%.
But `e10_before.jsonl` as shipped is **-729 IMPs**, not the round-11 file's -804.
Recomputed from this file:

| baseline | value |
|---|---|
| per-table board margin (2,000 tables) | **-0.729** |
| our par gap, `+a_par_gap` / `-b_par_gap` | **-0.338** |

The brief's -0.80 / -0.378 are the round-13 numbers. Every table below uses
**-0.73 / -0.34**. No verdict turns on the 0.07, but the numbers should stop
being quoted from a superseded file.

**Correction 2 — `score_candidates` order is not the engine's choice, and
`repro.py` will mislead a reviewer who forgets it.** `fast_decision` takes
`_dedupe_by_call`, keeps everything with fit >= 0.9, and picks the **highest
priority** among those — not the top blended score. Ranking the corpus by
`score_candidates` order mislabels **25 of 10,346 decisions**, every one of them
a rule at fit 0.946/0.965 that legitimately beats a fit-1.00 `*_pass` on
priority. `rank_at()` returns the score order. Read the priority column.

**Correction 3 — six of the twenty findings misquote or misdescribe what they
indict.** They are flagged individually; **four of the eight kills rest partly or
wholly on the correction**:

| fix | the claim | what the file says |
|---|---|---|
| 1 | "There is no four-level rung at all, in any of the four `defense_vs_preempt_*` contexts" | `v3_H_C` (4C), `v3_H_D` (4D), `v3_S_C`, `v3_S_D`, **`v3_S_H` (4H, 6+ hearts, 11+)** are all four-level rungs |
| 5 | the decline rung is "copied verbatim from `nt_quant_opener_decides`" | `quant_decline_P` is `hcp: [15, 16]`; the proposal is `requires: {}` (which is *better* — round 6's complete-fallback lesson — but it is not verbatim) |
| 8 | "carry the sibling's shape gates verbatim" | the sibling `cl_negative_X1` is `longest_suit_length: [0, 4]` plus `suit_length(their): [0, 3]`; the proposal is `[0, 5]` and neither of the others |
| 14 | "the 1H twin `nx_1m1H_wj_S`" | **that rule does not exist.** `resp_1m_over_1H` has no weak jump shift at all — the sibling gap runs the other way |
| 14 | "copy the preempt family's floor verbatim" | the preempt floor is **0 non-vul / 1 vul**; a flat 1 is the *vulnerable* floor applied everywhere, i.e. stricter than the sibling |
| 20 | the patch is "an additional `any_of` branch" | `open_1D`'s `not: { any_of: [H5+, S5+] }` is a **sibling of** `any_of`, applied conjunctively, so the branch as written is vetoed and the edit changes nothing. Third round running for "the edit applied and did nothing" |

**A limitation to state up front.** The blast radius is measured per decision
against the recorded auction; it does not re-run the auction, so a changed call's
downstream consequences are not in the count. Where a change is our last call and
the opponents passed it out I compute the double-dummy IMP swing exactly and say
so; everywhere else the direction is a judgement.

---

## 2. Verdicts

### FIX 1 — the direct seat cannot bid four of a major over a three-level preempt — **RESHAPE, then SHIP**

**The premise is overstated and the patch misses its own best case.** Four-level
rungs do exist (see Correction 3); the true hole is narrower and real: over 3C and
3D the majors have only a *three*-level rung, and over 3H spades have only 3S, so
an eight-card suit makes the same call as a six-card one.

**Denominator.** `defense_vs_preempt_*` is **39 tables, -114 IMPs, mean -2.92,
our gap -3.33** — below baseline on both, and the worst-behaved non-slam family
of the four contexts I measured in this seat. Inside it, *direct seat, 7+ card
major*: **2 tables, -19 IMPs, mean -9.50, our gap -13.00**.

**The proposed gate excludes the stronger of the two boards.** `suit_quality`
counts A/K/Q as 1 and J/T as 0.5, so board 410b's `AJ987532` — an **eight**-card
spade suit — scores 1.5 against the proposed `[2, 9]` and does not fire. The
finding's own argument ("the openings already treat eight cards in a major as a
4M opening") points at length, and `open_4S` carries **no quality gate at all**.
Carry that branch across:

```yaml
# AFTER - inserted immediately before v3_$X_pass in defense_vs_preempt_C
# and defense_vs_preempt_D (4S and 4H), and defense_vs_preempt_H (4S only;
# over 3S the four-level heart rung v3_S_H already exists)
      - id: v3_C_4S
        call: 4S
        priority: 65
        requires:
          suits: { S: [7, 13] }
          any_of:
            # open_4S's own comment: "Eight of them is a four-level preempt,
            # not a three-level one" - and open_4S carries no quality gate.
            - suits: { S: [8, 13] }
            - evals: { total_points: [13, 40], "suit_quality(S)": [2, 9] }
        shows: "overcalling the preempt at the four level: eight of them, or seven with opening values and a good suit"
        establishes: { forcing: non_forcing }
```

- **VERIFIED.** Own board 63 `[a1]` → 4S at fit 1.00 (as written it also flips).
  Whole-corpus replay: **2 call changes**, exactly the two tables above. As
  written it changes only one. Lints unchanged (223 floor, everything else 0).
- **Determinable value.** Board 410b: our W bids 4S over 3D instead of 3S. 4S by
  W takes 10 tricks double-dummy; table A's BEN E/W already play 4S making, so
  `b_score_ns` goes -170 → -620 and the board margin goes **-10 → 0 (+10)**.
  Board 199a is directional, not determinable (BEN's E bid 5D over our 3H and may
  bid it over 4H too): **0 to +9**.
- **ENDANGERS.** This is a rung that *displaces* a call, not one that fills a
  hole: at priority 65 over 64 every 7+ major with the values now bids four
  instead of three, and partner can no longer stop in a partscore. On this corpus
  that is two hands, both of them 7- and 8-baggers.
- **HIGH-VARIANCE: yes** (2 tables). Bundle only with the other attributable
  singles; revert on the number.

---

### FIX 2 — nothing in the generic toolkit RAISES partner's notrump — **RESHAPE, then SHIP ALONE**

Diagnosis **verified**: I grepped all five generic contexts. `uc_nt1/2/3`,
`cl_nt1/2/3`, `ch_nt3`, `ballow_nt*`, `balhigh_nt*` are every one of them a
natural notrump about my own balanced hand. Nothing raises partner's. Own board
90 `[b7]` flips from `uc_pass` to 3NT at fit 1.00. The `when` clause is sound:
`we_bid_last` is "our side made the standing bid" (engine.py:206) and
`we_hold_contract` is "*I* made it" (engine.py:142), so the pair means "partner's
bid stands, below game".

**But `standing_bid_strain: [NT]` is not "partner has shown a balanced hand", and
the rung has no shape gate, no stopper gate and no floor of its own.** As written
(`standing_bid_level: [1, 2]`) it fires on **18 of 2,000 tables**, and six of
them are partner's *1NT*, which in this system is the semi-forcing response, the
6-10 response over an overcall, or opener's 12-14 rebid. On board 582b it makes
an 18-count with **5-5 in spades and diamonds and a singleton heart** bid 3NT over
partner's semi-forcing 1NT, displacing `ob_1M1NT_2D` — which was itself sitting at
fit 0.409, i.e. it papers over an authored starved seat.

Restrict it to the two level, where partner's notrump is always a limited natural
one (an 18-19 jump rebid, or a natural/invitational 2NT):

```yaml
# AFTER - immediately after uc_nt3's `establishes:` line, before the comment block
      - id: uc_nt_raise3
        call: 3NT
        priority: 28.5          # under uc_nt3, so the natural reading stays primary
        when: { we_bid_last: true, we_hold_contract: false, standing_bid_strain: [NT],
                standing_bid_level: [2] }
        requires: { evals: { rule_of_26: [25, 99] } }
        shows: "raising partner's notrump to game: 25+ combined opposite the range partner has shown"
        establishes: { forcing: sign_off }
```

`standing_bid_level: [1]` is deliberately dropped: a one-level notrump from
partner is a *response*, not a description of a balanced hand, and 17 opposite a
shown 6-10 reaches `rule_of_26` 25 on partner's midpoint alone.

**Denominator.**

| slice | tables | IMPs | mean | our gap |
|---|---|---|---|---|
| corpus baseline | 2000 | -1458 | **-0.73** | **-0.34** |
| as written (levels 1-2) | 18 | -47 | -2.61 | -6.56 |
| **level 2 only (shipped)** | **12** | **-30** | **-2.50** | **-6.75** |
| the six level-1 firings it drops | 6 | -17 | -2.83 | -6.17 |

- **VERIFIED** (prototype, 12 call changes, lints unchanged).
- **ENDANGERS**, three things, all real. (a) **Constraint 5**: 3NT in
  `general_uncontested_continuation` currently reads "13-19 balanced, their suits
  stopped"; it will now also read "any hand with 25 combined". (b) At priority
  28.5 the raise outranks every `uc_new_*` rung, so board 622b's `AK653.K543.7.AJ3`
  stops showing its five-card spade suit and raises notrump instead. I kept 28.5
  rather than tuning it under 27.5 because choosing the number that spares 622b
  and not 97b is fitting the corpus; `uc_nt3` at 29 already outranks the new suits,
  so 28.5 is the consistent choice. (c) Seven of the twelve firings are
  **competitive** auctions reached through `general_uncontested_continuation`'s
  `... - P - ?` pattern — round 12's documented misapplication. If the measurement
  comes back negative, the decomposition to try is `when: { is_competitive: false }`,
  which costs the motivating board (90b is competitive) but keeps the five
  constructive firings.
- Three of the twelve fire at fit **0.946** — half a point of `rule_of_26` — so a
  quarter of the effect is soft-miss lottery, not agreement.
- **HIGH-VARIANCE: yes.** **Measure alone.**

---

### FIX 3 — the doubler cannot answer on the points he doubled with — **RESHAPE (sweep the siblings), then SHIP**

Verified by quotation. `oc1S_X` / `oc1H_X` weak branch: `hcp: [11, 16]`.
`adx_neg_major_$M$L`: `hcp: [12, 40]`. Round 9's `gst_rkc` / `rkc_4NT` species
exactly — one agreement, two floors, and which applies decided by nothing.

**The fix must also sweep `ch_neg_major_*`**, whose own file comment says "Gates
carried verbatim from that rule, so this can only be a superset of the auction it
mirrors". Leaving it at 12 makes that comment false and recreates the asymmetry
one context along.

```yaml
# adx_neg_major_H2 / H3 / S2 / S3 and ch_neg_major_H2 / H3 / H4 / S2 / S3 / S4
# BEFORE
        requires: { suits: { H: [4, 13] }, hcp: [12, 40] }
# AFTER
        # The takeout double that produced this auction has an 11-HCP floor
        # (oc1S_X, oc1H_X): a doubler who qualified on eleven must be able to
        # answer partner's responsive double on eleven.
        requires: { suits: { H: [4, 13] }, hcp: [11, 40] }
```

- **Denominator / reach**: **3 tables of 2,000** (650a twice, 974b), board margins
  0, 0, -1. `general_pull_or_sit` as a whole is unchanged elsewhere.
- **VERIFIED**: own board 6 `[b5]` → 3H at fit 1.00 (the finding implies 2H; the
  auction is at the three level). Whole-corpus replay 3 call changes, lints
  unchanged.
- **ENDANGERS**: constraint 5 — partner's shown minimum for 2H/3H/2S/3S in
  `general_pull_or_sit` and `general_competitive_high` drops from 12 to 11. That is
  one point, and it makes two statements of one convention agree.
- **HIGH-VARIANCE: no.** Bundle.

---

### FIX 4 — the takeout double of a weak two is stricter than the double of a preempt — **KILL**

The two `requires` blocks are quoted correctly and the asymmetry is real. The
inference from it is not.

**The asymmetry is a design, not an oversight.** At the three level partner's
answer to a takeout double is at the four level and *passing is expensive*, so
the double must tolerate three of their suit. At the two level partner answers at
the two level and you have alternatives — 2NT with a stopper, a natural overcall,
or a pass. "One level safer" argues for being able to afford *more* shape
discipline, not less.

**And the data does not want the extra branch.** Prototyped exactly as proposed:

| slice | tables | IMPs | mean | our gap |
|---|---|---|---|---|
| corpus baseline | 2000 | | -0.73 | -0.34 |
| all `vw2_*` firings | 86 | -69 | -0.80 | -1.15 |
| the new branch, as written | 4 | **+0** | **+0.00** | -2.75 |
| … denying a five-card suit | 3 | **+0** | **+0.00** | -3.67 |

**Board margin +0.00 against a corpus mean of -0.73, and two of the three tables
currently win +3 apiece.** That is not a defect population.

Worse, as written the branch keeps `longest_suit_length: [0, 5]`, so board 896a —
`KQT76.A86.J2.A65`, 14 HCP with **KQT76 of spades** over 2H — stops
overcalling 2S and doubles instead. DECISIONS records that exact repair twice
("The takeout doubles allowed a five-card major… they deny one now"; "chunky
5-card majors overcall instead of doubling"). A fix that re-opens a
twice-closed defect to reach a three-table population at baseline is not a fix.

**KILL.** It also widens a double, which is a standing high-variance trigger.

---

### FIX 5 — the Stayman 2D ladder has no quantitative invitation — **SHIP (structure only, reach 0/2000)**

Verified: `stayman_resp_after_2D` is 2NT `[8,9]`, 3NT `[10,17]`, 6NT `[18,21]`.
16-17 opposite a 15-17 notrump is 31-34 and has only the game bid. Its own sibling
half has `stm_rkc_4NT` at 15-21. Round 8's ceiling species, in this very context,
in the other direction.

Ship the rung **and** its answering seat; the existing `nt_quant_opener_decides`
is anchored `1NT - P - 4NT - P - ?` and does not match a Stayman auction.

```yaml
# stayman_resp_after_2D, AFTER - inserted after stm_2D_3NT
      - id: stm_2D_4NT
        call: 4NT
        priority: 63
        requires: { hcp: [16, 17], evals: { controls: [3, 12] } }
        shows: "quantitative: 16-17 opposite a 15-17 notrump is 31-34, inviting slam"
        establishes: { forcing: invitational }
        alertable: true

# AFTER - a new context, inserted immediately before `stayman_resp_after_2M`
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
      # a COMPLETE fallback, not the mirror of the accept gate - round 6's
      # rkc5H_signoff lesson.  (The finding calls this "verbatim" from
      # nt_quant_opener_decides; that rule is hcp: [15, 16].  The complete
      # fallback is the better of the two and the difference is deliberate.)
      - id: stmq_pass
        call: P
        priority: 55
        requires: {}
        shows: "declining the quantitative invite: not a maximum"
        establishes: { forcing: sign_off }
```

- **Denominator**: `stayman_resp_after_2D` is **8 tables, +3 IMPs, mean +0.38,
  our gap -2.00**. **Not one of the eight hands holds 16 or 17 HCP.** The rung
  fires on **0 of 2,000 tables**; the new context is reached 0 times.
- **VERIFIED**: own board 51 `[a7]` → 4NT at fit 1.00, and the answering seat
  works (North's 16-count passes at `stmq_pass` fit 1.00). Whole-corpus replay:
  **0 call changes**. Lints unchanged (223, contexts 512 → 513).
- **It does not fix its own board, and I want that on the record.** Board 51's
  opener holds exactly 16, so the invite is declined; 3NT+4 (+520) becomes 4NT+2
  (+490), i.e. **-1 IMP**. The board was lost to the 17/16 split, which DECISIONS
  records as the deliberate design of every quantitative raise in the file, not to
  the missing rung. Sell this as a ceiling closed, not as IMPs.
- **ENDANGERS**: 16-17 balanced with a four-card major no longer bids 3NT in this
  auction. 31-34 combined is the textbook invitational zone and the invite's floor
  (31) matches `qr3_4NT_quant`'s round-8 repaired floor exactly.
- **HIGH-VARIANCE: no.** Bundle with the other zero-reach structure.

---

### FIX 6 — responder places the contract in a major opener has just denied — **SHIP**

Verified verbatim: `r2c_place_4H` is `requires: { suits: { H: [4, 13] } }` and the
pattern's `3(D|H|S)` alternation throws away opener's answer. A plain
implementation bug, the same one DECISIONS records fixing for the 1NT Stayman
ladder in round 4 and never sweeping to the 2C twin.

```yaml
# r2c_place_4H, BEFORE
        requires: { suits: { H: [4, 13] } }
# r2c_place_4H, AFTER
        when: { standing_bid_strain: [H] }
        requires: { suits: { H: [4, 13] } }
# r2c_place_4S, AFTER
        when: { standing_bid_strain: [S] }
        requires: { suits: { S: [4, 13] } }
```

- **Denominator**: `r2c_after_stayman_reply` is reached **1 time in 2,000 tables**
  (board 695a) and that one table is the defect: `T87.8532.5432.76`, a **zero**-count,
  bids 4H over opener's 3D into a 4-2 fit. -3 IMPs, our gap -7.00.
- **VERIFIED**: own board 82 `[a10]` → 3NT. Whole-corpus replay: 1 call change.
  `r2c_place_3NT` is `requires: {}` so the seat cannot be starved. Lints unchanged.
- **Board value: 0.** Double-dummy, 3NT by North also goes two down for -200, so
  board 695's margin stays -3. Ship it because it is a bug, not because it scores.
- **ENDANGERS**: nothing. It deletes exactly the four-level bid in a suit opener
  has denied.
- **HIGH-VARIANCE: no.** Bundle.

---

### FIX 7 — the transfer super-accept has no answering seat — **SHIP. This is the best fix in the batch.**

Verified. `nt_after_transfer` is anchored `1NT - P - 2$T - P - 2$M - P - ?` — the
simple acceptance only. After `tr_super_3H` / `tr_super_3S` (4-5 trumps, a
maximum) the seat matches no context at all and `uc_raise_H4` wants 11+ support
points, so eight points opposite a shown nine-card fit passes at `uc_pass` fit 1.00.
Constraint 4, sixth instance in the file's history.

```yaml
# AFTER - a new context, inserted immediately before `nt_after_transfer`
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

- **Denominator**: `tr_super_3H` / `tr_super_3S` fire on **2 tables of 2,000** —
  **-10 IMPs, mean -5.00, our gap -10.00 — and both are passed out.** The
  super-accept has a 100% failure rate in this corpus.
- **VERIFIED**: own board 88 `[a8]` → 4H at fit 1.00. Whole-corpus replay: 2 call
  changes, both of them the two super-accepts. Lints unchanged (512 → 514 contexts).
- **Determinable value +20, and both halves are exact** — in both auctions the
  opponents pass throughout, so the contract is fully determined:
  - board 341a: 3H by South making 10 → 4H by South making 10. NS vul: +170 → +620
    against the other table's +170. Margin **0 → +10**.
  - board 652b: 3H by East making 10 → 4H by East making 10. Both vul: `b_score_ns`
    -170 → -620 against table A's -620. Margin **-10 → 0 (+10)**.
- **ENDANGERS**: a 5-7 count opposite a super-accept now bids game where it used
  to pass. Opposite a shown 17 with four-card support that is 22+ and a nine-card
  fit; the `trsa_pass` rung is a complete fallback so nothing is starved.
- **HIGH-VARIANCE: no** (both boards determinable and in the same direction).
  Bundle.

---

### FIX 8 — the negative double of a jump overcall promises nothing at all — **SHIP AS WRITTEN, ALONE, and revert on the number**

Verified by quotation and it is the most under-gated rule I found: `nxj_X` is
`requires: { hcp: [8, 40] }` at **priority 70**, above everything in its context,
with a `shows` sentence claiming "support for unbid suits". Both motivating boards
fit 1.00 on three-card majors.

**Denominator, whole family.**

| slice | tables | IMPs | mean | our gap |
|---|---|---|---|---|
| corpus baseline | 2000 | | -0.73 | **-0.34** |
| all `nxj_X` firings | 15 | -15 | -1.00 | **-6.80** |
| … with a 4+ card unbid major | 9 | -36 | -4.00 | -7.11 |
| … with **no** four-card major | 6 | **+21** | **+3.50** | -6.33 |
| **removed by the fix** | **7** | **+14** | **+2.00** | -7.29 |
| kept by the fix | 8 | -29 | -3.63 | -6.38 |

**Read that honestly: the doubles the fix deletes are the ones currently winning
on board margin, and the ones it keeps are the ones losing.** On the attributable
metric the two halves are indistinguishable (-7.29 against -6.38) and both are
twenty times worse than the -0.34 baseline, so the board-margin split is two
tables (+13, +10) of variance inside a uniformly bad family. I ship it anyway, on
three grounds, and I say plainly that it is the riskiest survivor.

1. The seven deleted doubles are made on a **seven-card club suit**, two six-card
   diamond suits, a 6-5 two-suiter, and **four hands with no four-card major at
   all**. None of them is a negative double under any definition of the convention.
2. The damage is not at the doubler's own table — it is in the partner model.
   Board 194's partner bid 3H over the double holding three hearts and played a
   4-3 fit for -150. A rule whose reading is a lie poisons every seat after it.
3. Constraint 9: the `shows` sentence states a gate the constraint does not carry.

**Keep the proposed `[0, 5]`, not the sibling's `[0, 4]`, and say why.** I measured
both. `cl_negative_X1` lives at the *one* level, where a five-card suit is cheap
to bid; over a jump overcall it costs a level, so a hand with four of an unbid
major and a five-card minor must still double. `[0, 4]` fires four extra times and
two of those are wrong (583a `T9.A943.T5.AQJ43` and 855a `A87.JT652.A52.QT` lose
their double and land on `cl_nt2`).

```yaml
# nxj_X, BEFORE
        requires: { hcp: [8, 40] }
        shows: "negative double of the jump overcall: support for unbid suits"
# nxj_X, AFTER
        requires:
          hcp: [8, 40]
          # The one-level sibling cl_negative_X1 caps the longest suit at FOUR;
          # over a jump overcall a five-card suit costs a level to show, so the
          # cap is five here.  Six of my own and there is nothing to take out to.
          evals: { longest_suit_length: [0, 5] }
          any_of:
            - suits: { H: [4, 13] }
            - suits: { S: [4, 13] }
        shows: "negative double of the jump overcall: 8+ HCP with four cards in an unbid major"
```

- **VERIFIED**: both own boards flip (194 `[a2]`, 129 `[b2]`). Whole-corpus
  replay: **7 call changes**. Lints unchanged.
- **ENDANGERS**, and this is the second warning: **the seat behind the deleted
  double is thinly authored.** On board 194a the best remaining candidate is
  `cl_nt2` at fit **0.668** — a soft-miss lottery, not an agreement. Two of the
  nine replacement calls land below the 0.9 fast-path threshold. This is the same
  shape as the `weakest_their_stopper` revert (round 8, -9 held out): a correct
  class-wide gate whose starved seats have not been authored.
- **HIGH-VARIANCE: yes.** **Measure alone.** If it goes negative, the fallback is
  the text-only repair (fix the `shows` sentence, keep the rule) — that is the
  round-13 precedent for a correct diagnosis whose gate does not pay.

---

### FIX 9 — a four-card major cannot be bid at the one level without honours — **KILL (and the residue it exposed ships instead)**

`cl_new_S1` is quoted correctly. The argument — "quality is a two-level question"
— is decent bridge. Both halves of the repair fail.

**(a) It is a threshold removal on an above-baseline slice.** Prototyped, dropping
the `any_of` quality branch from `cl_new_S1`/`cl_new_H1` reaches **3 tables**
(13b, 112b, 247a): **-4 IMPs, mean -1.33, our gap +1.67** — a point and a half
*above* the -0.34 baseline on the attributable metric, on three tables, one of
which currently wins +5. DECISIONS scopes threshold moves out at -0.025 +/- 0.062.

**(b) Removing the gate makes the engine bid the SHORTER major.** `cl_new_S1` and
`cl_new_H1` are both priority 30, so once both fit 1.00 the tie breaks on
`_sort_key`'s call rank and **1H wins**. Board 269b, `T8642.K732.Q4.A7`, currently
bids 1S on five spades and would bid 1H on four hearts. That is round 10's
`r1m_1H` / `r1m_1S` defect, re-created.

**KILL.** But (b) exposed something the twenty do not contain, and it is worth
more than the fix was — see **Residue 1**: the tie already misfires *today* on two
tables, and the one-line guard that fixes it is shipped there.

---

### FIX 10 — rebidding my own six-card suit at the two level needs eleven points — **KILL. This is the largest thing in the batch and it is the round-8 floor lesson run backwards.**

The `requires` blocks are quoted correctly and the hole is real: 6-10 with six of
my own has no two-level rebid. The finding also states the cost in one line —
"partner's shown minimum for a two-level rebid of our own suit drops from 11 to 6"
— and then ships it across **28 rules in seven generic families**. I measured what
that costs.

**Prototyped: 12 call changes on 2,000 tables — and only five of them are the new
sign-off.** The other seven are *our own bids collapsing* because partner's 2M/2m
no longer promises anything:

| board | today | with FIX 10 | board margin today |
|---|---|---|---|
| 508a | `uc_raise_H4` **4H** | `uc_pass` **P** | **+10** |
| 516a | `uc_raise_H4` 4H | `uc_pass` P | -12 |
| 298a | `uc_raise_H4` 4H | `uc_nt2` 2NT | 0 |
| 301a | `uc_raise_D3` 3D | `uc_pass` P | -1 |
| 764a | `cl_raise_D3` 3D | `cl_pass` P | -2 |
| 770a | `uc_raise_S3` 3S | `uc_pass` P | 0 |

The changed slice is **12 tables, -28 IMPs, mean -2.33, our gap -3.92** — a bad
population, which is why the finding found it — but the *mechanism* of the change
is the deletion of five raises and a game, including a table we currently win by
ten.

DECISIONS, round 8, in as many words: *"same-call rules merge into a disjunction
for the partner model, so a rung with no floor lowers partner's shown minimum for
that call **everywhere**. Without it a cold 4S elsewhere in the corpus turned into
a pass, because partner's 3S dropped from a shown 10 to a shown 0 and `rule_of_26`
stopped opening."* That is this fix, deliberately, times twenty-eight.

**KILL.** The hole is real and there is no floor-preserving way to express it in
this engine — `total_points` has a floor channel in the partner model and no
ceiling. Record it as an open item alongside the keycard-ask ceiling problem,
which is the same missing channel.

---

### FIX 11 — a six-card major loses to 3NT on priority alone — **SHIP (structure, reach 0/2000)**

Verified exactly. `rjrb_3NT` priority 55 and `rjrb_3M` priority 54, both
`hcp: [10, 16]`, and 3M additionally demands six cards — so a hand that satisfies
both fits 1.00 twice and the *less* descriptive call wins on a static number.

**The sibling argument is stronger than the finding makes it.** `rjrb_6NT` and
`rjrb_4NT` in the same context **both carry `not: { suits: { $M: [6, 13] } }`** —
the file already agrees that with six of a major you do not bid notrump. Only
`rjrb_3NT` was never given it. The priority move is the one-line equivalent that
does not split a call into two readings (round 12's `ob_1NT` precedent).

```yaml
# rjrb_3M, BEFORE
        priority: 54
# rjrb_3M, AFTER
        # rjrb_6NT and rjrb_4NT both deny a six-card major in this very context;
        # rjrb_3NT never got the denial, so the six-card hand fitted both at 1.00
        # and lost on a static number.  Re-ranked rather than gated, so 3NT keeps
        # its full band as the backstop.
        priority: 55.5
```

- **Denominator**: `rjrb_3M` fires **0 times** and `rjrb_3NT` **once** in 2,000
  tables. Whole-corpus replay: **0 call changes**.
- **VERIFIED**: own board 108 `[b7]` → 3H at fit 1.00. Lints unchanged.
- **ENDANGERS**: a hand with both a six-card major and a flat 3NT now shows the
  major. That is the intent, and the 3NT band is untouched.
- **HIGH-VARIANCE: no.** Bundle.

---

### FIX 12 — the choice-of-games 3NT is offered with a void — **RESHAPE (it needs a floor), then SHIP**

Verified: `tr_3NT_choice` is `hcp: [10, 15], suits: { $M: [5, 5] }` and nothing
else, and `void(any)` is already in the file.

**As proposed the gate starves the seat and loses ten IMPs on its only firing.**
Prototyped: board 709a's `KQ764.QT9.K8654.` falls to `tr_2NT_inv` at fit **0.80** —
the finding predicts it "falls to a natural bid in the long side suit", but
`nt_after_transfer` has no natural side-suit rung. Double-dummy, 3NT by South makes
nine for +600 and 2NT by South makes nine for +120 against the other table's +600:
the board goes **0 → -10**.

A veto needs a floor for the whole class (round 4's lesson). Give the void hand
the call it should have been making:

```yaml
# tr_3NT_choice, BEFORE
        requires: { hcp: [10, 15], suits: { $M: [5, 5] } }
        shows: "game values, exactly 5 $M: choice of games (opener corrects to 4$M with 3+)"
# tr_3NT_choice, AFTER
        requires: { hcp: [10, 15], suits: { $M: [5, 5] }, evals: { "void(any)": [0, 0] } }
        shows: "game values, exactly 5 $M and no void: choice of games (opener corrects to 4$M with 3+)"

# AFTER - the floor the veto needs, inserted immediately after tr_3NT_choice
      - id: tr_game_void_$M
        call: 4$M
        priority: 58.5
        requires: { hcp: [10, 15], suits: { $M: [5, 5] }, evals: { "void(any)": [1, 4] } }
        shows: "game values, exactly 5 $M and a void: no notrump with a void, so play the major"
        establishes: { forcing: sign_off, agreed_suit: $M }
```

- **Denominator**: `tr_3NT_choice` fires on **5 tables, +0 IMPs, mean +0.00, our
  gap -6.00**. Board margin at baseline, par gap well below it. The gate reaches
  **1 table**.
- **VERIFIED**: own board 111 `[a7]` → 4H at fit 1.00; whole-corpus replay 1 call
  change. Double-dummy on 709a: 4S by South takes eleven, +650 against +600, board
  **0 → +2**. Lints unchanged.
- **ENDANGERS**: exactly the 5-card-major transfer hands with a void, which now
  play a possible 5-2 fit instead of a notrump. Opposite a 1NT opener who has
  accepted the transfer that is 5-2 at worst; with a void, notrump is the worse bet.
- **HIGH-VARIANCE: no** (one table, determinable). Bundle.

---

### FIX 13 — the positive response to 2C demands two of the top three — **SHIP (structure only, reach 0/2000)**

Verified: `r2c_2S_positive` carries `features: ["two_of_top3(S)"]`, which is
sharp (round 5), so `KJ9763` scores 0.20 and `r2c_2D_waiting` (`requires: {}`)
takes it at 1.00. DECISIONS states the agreement as "2H/2S/2NT are natural
positives (8+)"; the top-three requirement is an undocumented extra calibrated
for a five-card suit.

```yaml
# r2c_2S_positive / r2c_2H_positive, BEFORE
        requires: { suits: { S: [5, 13] }, hcp: [8, 40], features: [ "two_of_top3(S)" ] }
        shows: "positive: 5+ good spades, 8+ HCP"
# AFTER
        requires:
          suits: { S: [5, 13] }
          hcp: [8, 40]
          any_of:
            - features: [ "two_of_top3(S)" ]
            # length is quality: the top-three test is calibrated for a five-card
            # suit, and a sixth card is worth more than a second honour.
            - suits: { S: [6, 13] }
              features: [ "top_honour(S)" ]
        shows: "positive: 8+ HCP with five good spades, or six headed by an honour"
```

- **Denominator**: `r2c_2S_positive` and `r2c_2H_positive` fire **0 times** in
  2,000 tables. Whole-corpus replay: **0 call changes**.
- **VERIFIED**: own board 185 `[a3]` → 2S at fit 1.00. Lints unchanged.
- **ENDANGERS**: it widens a **game-forcing** call, so partner's read of 2S/2H
  loosens from "five with two of the top three" to "…or six with one". That is
  what the system says it plays. Claim nothing on score.
- **HIGH-VARIANCE: no** (reach 0). Bundle.

---

### FIX 14 — the weak jump shift has no suit-quality floor — **KILL**

Three independent reasons, and the first is fatal.

1. **The rule fires once in 2,000 tables and that table wins.** `nx_1m1S_wj_H`:
   **1 table, +1 IMP, mean +1.00, our gap +1.00** — above baseline on both.
   Round 11's lesson, verbatim: *"Before concluding a rule is unreachable, check
   whether the hands it describes are simply uncommon."*
2. **The gate reaches 0 of 2,000 tables**, verified by prototype — it cannot pay
   and can only subtract on the held-out corpus.
3. **The twin it names does not exist, and the sibling argument runs the other
   way.** There is no `nx_1m1H_wj_S`; `resp_1m_over_1H` has no weak jump shift at
   all. And "copy the preempt family's floor verbatim" is not what a flat 1 does —
   the preempt floor is 0 non-vul and 1 vul, so a flat 1 is *stricter* than the
   sibling in the seat the motivating board was not in.

**KILL.** The missing 2S jump over `1m - (1H)` is recorded in the residue as an
additive finding.

---

### FIX 15 — opener bids on over responder's weak three-level bail — **SHIP (structure, reach 0/2000)**

Verified: `1NT - P - 3$m - P - ?` matches no context, `nt_3C_bail` /
`nt_3D_bail` are `forcing: sign_off` with 0-7 HCP, and `we_hold_contract` is keyed
on my own last bid by design, so partner's sign-off is unprotected. Own board 96
`[b7]` bids `uc_new_S3` and plays 3S for five tricks.

```yaml
# AFTER - a new context, inserted immediately before `nt_after_transfer`
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

- **Denominator**: `nt_3C_bail` fires **2 times**, `nt_3D_bail` 0. Whole-corpus
  replay: **0 call changes, 1 relabel** (board 925a already passes, now with an
  agreement instead of a catch-all). Lints unchanged (512 → 514).
- **VERIFIED**: own board 96 `[b7]` → P at fit 1.00.
- **ENDANGERS**, and it is not nothing: a pass at priority 60 with `requires: {}`
  **silences opener at that seat completely**, including with 20 HCP. Opposite a
  partner who has shown 0-7 with six of a minor that is right essentially always,
  and it is one sentence of bridge. But it is a total subtraction on a
  two-table population, so it belongs in the zero-reach bundle where it can be
  reverted cheaply.
- **HIGH-VARIANCE: no.** Bundle.

---

### FIX 16 — the uncontested toolkit has no new suit at the four level — **KILL**

The hole is real. The rung is not the repair.

**Prototyped: 15 call changes on 2,000 tables, and six of them are positions the
BALANCING contexts own.** `general_uncontested_continuation`'s pattern is
`... - P - ?`, which means "RHO passed", not "the auction is uncontested" — so a
four-level rung at priority 28 outranks `balhigh_pass` (21) and takes over the
balancing seat on boards 109b, 617a, 808a, 911b, 924b, 991b. Round 12 measured
routing `uc_` rules into competitive seats at **-59 paired and -106 held out** and
recorded the repair as "port individual rungs under `when: { is_competitive: … }`,
not a toolkit swap". This is the swap, from the other end.

Two more concrete failures in the same fifteen:

- board 419b, `52.6.AKT73.AQJ73` after `1D - P - 3D - P`: `uc_minor_game_5D`
  (5D, fit 1.00) is displaced by `uc_new_C4` on the tie at priority 28. Bidding a
  new minor at the four level over partner's raise of our own suit is not a
  natural bid, it is a cue we do not play.
- board 691a: the new candidate changes the candidate set enough that a
  **`gst_rkc_D` 4NT at fit 0.066** becomes the pick, replacing a fallback 4H.
- five of the fifteen (28b, 282b, 429a, 625a, 924b) bid a new suit at the four
  level over **partner's own** three- or four-level bid.

Changed slice: 15 tables, -43 IMPs, mean -2.87, our gap -5.93. The population is
bad; the change is a coin flip inside it, with a documented anti-pattern attached.

**KILL.** The half of this that is right — *the takeout doubler rebids his own
long suit at the four level over partner's minimum advance* (boards 2a, 485a,
110a) — is a rule in a different context with a `partner_last_call_was_double`
gate, and it needs its own round.

---

### FIX 17 — in a game force opposite an unlimited partner no slam gate can open — **KILL, and it does not reach the position it was written for**

**The premise is true and important.** `r2c_2D_waiting` is `requires: {}`, so
after a 2C opening partner's shown floor is zero by construction and
`rule_of_26_sharp >= 31` is unreachable whatever the opener holds. That belongs in
the open items.

**The patch has nothing to do with it.** Prototyped across all four suits:
**12 call changes on 2,000 tables, and not one of the twelve auctions starts with
2C.** Round 13's FIX 13 in a different costume: the repair provably does not do
what it is proposed to do on the position it was proposed for.

What it does instead:

| | tables | IMPs | mean | our gap |
|---|---|---|---|---|
| corpus baseline | 2000 | | **-0.73** | -0.34 |
| `gst_rkc_solo_*` firings | 12 | **+25** | **+2.08** | -3.83 |

**Board margin +2.08 against a corpus mean of -0.73 — these are tables we
currently do well on**, and three of them (451b twice, 716b) are +11 each. Board
451b currently makes a winning penalty double of 3H and would instead ask for
keycards.

And five of the twelve — 322b, 909a, 930b, 215b, 716b — are **keycard asks
opposite a partner who has shown 0-8**, because the advance of a takeout double
carries no floor. That is the family DECISIONS has measured negative twice (round
8: a gate on it, -17 held out; round 9: two reviewers, no separator survives) and
that the round-13 critique flagged as live residue. A rung whose only requirement
is 21 points of my own and eight trumps *counting partner's forced advance* is the
most permissive keycard ask anyone has proposed here.

**KILL.**

---

### FIX 18 — a natural 1NT rebid tops out at ten points — **RESHAPE (gate it to the rebidder's seat), then SHIP ALONE**

The `uc_` ladder is quoted correctly: 1NT `[6,10]`, 2NT `[11,12]`, 3NT `[13,19]`
with `rule_of_26 >= 24`, so 12-14 balanced rebidding after a one-level response has
no rung anywhere. (The finding's "cl_nt1 twin" is `[8, 11]`, not `[6, 10]`, so the
competitive twin has to be banded 12-14 or it overlaps at 11.)

**As written it fires 16 times, and seven of them are the sandwich seat** — the
family this findings document itself rules NOTHING-WRONG, and which measures
**331 tables, mean -0.65, our gap +2.69**, one of the healthiest in the engine.
A 12-14 balanced hand would start overcalling 1NT in a seat where 1NT shows 15-18;
board 364b would bid "natural 1NT with their suits stopped" holding **five of
their diamonds**, because `weakest_their_stopper` still does not gate.

| slice | tables | IMPs | mean | our gap |
|---|---|---|---|---|
| corpus baseline | 2000 | | -0.73 | -0.34 |
| **as written** | 16 | -9 | **-0.56** | **+1.50** |
| … the 7 sandwich-seat firings | 7 | +19 | +2.71 | +2.57 |
| **with `i_have_acted: true` (shipped)** | **6** | **-28** | **-4.67** | **0.00** |

As written the slice is above baseline on **both** metrics and would have been an
automatic kill. Gated to the seat the finding is actually about — a hand that has
already bid, rebidding — it is 6 tables at mean -4.67, and four of the six are
textbook: board 516a passes `K985.QT.Q84.KQT8` after `1C (1D) 1H (P)`, for -12.

```yaml
# AFTER - beside uc_nt1 (band 11-14) and cl_nt1 (band 12-14; cl_nt1 is 8-11,
# not 6-10, so 11 would overlap)
      - id: uc_nt1_strong
        call: 1NT
        priority: 27.5
        # i_have_acted keeps this out of the SANDWICH seat, where a natural 1NT
        # shows 15-18 and where the whole family measures above baseline.  This
        # is the rebidder's cheapest notrump, not an entry into the auction.
        when: { i_have_acted: true }
        requires:
          hcp: [11, 14]
          evals: { semi_balanced: [1, 1], weakest_their_stopper: [0.9, 9] }
        shows: "natural 1NT: 11-14 balanced with their suits stopped - my own rebid, the cheapest notrump, not the strongest"
        establishes: { forcing: non_forcing }
```

- **VERIFIED**: own board 163 `[a5]` → 1NT at fit 1.00. Whole-corpus replay: 6
  call changes. Lints unchanged.
- **ENDANGERS**: constraint 5 — 1NT in these two contexts now reads as a
  disjunction of the responder's 6-10/8-11 and the rebidder's 11-14. The `when`
  clause is auction-visible, so partner can separate them; without it the two
  readings merge into a 6-14 blob and 1NT stops meaning anything. It also displaces
  a 2NT (board 920a) that was firing at fit 0.80.
- The slice's par gap is **0.00**, i.e. at baseline. That is the argument against
  it and the reason it must not be bundled.
- **HIGH-VARIANCE: yes.** **Measure alone.**

---

### FIX 19 — no preemptive overcall of their 1NT — **KILL**

The ladder does stop at the two level. The family does not want the rung.

| slice | tables | IMPs | mean | our gap |
|---|---|---|---|---|
| corpus baseline | 2000 | | **-0.73** | **-0.34** |
| `defense_vs_1NT` seats | 129 | -43 | **-0.33** | **+2.91** |
| `v1NT_pass` | 111 | -16 | -0.14 | +3.28 |
| `v1NT_2S`/`2H`/etc. | 8 | -13 | -1.62 | +0.75 |
| the new rung's reach | **2** | **+0** | **+0.00** | **+5.00** |

**Above baseline on both metrics at every level of zoom.** This is the
round-13 FIX 17 shape exactly: a healthy family, a two-table slice, and a
proposal that is really a re-rank — at priority 62 over 61 it replaces a made
two-level overcall with a three-level preempt on both of the tables it touches,
one of which (837b) sits at par gap +10.

**KILL.**

---

### FIX 20 — a five-card major is opened ahead of a longer minor — **KILL, twice over**

**First, the patch as written changes nothing.** `open_1D`'s
`not: { any_of: [ {suits: {H: [5,13]}}, {suits: {S: [5,13]}} ] }` is a sibling of
its `any_of`, applied conjunctively, so an extra `any_of` branch is vetoed by the
five-card major denial before it is ever reached. I had to restructure the whole
`requires` block into a nested `any_of` to make it fire at all — third round
running for "a scripted edit applied cleanly and did nothing useful".

**Second, the population is one table and it currently wins.** The finding
correctly demands the whole-corpus count before anything ships. Here it is:
*opening seat, 6+ diamonds strictly longer than a five-card major* is
**1 table of 2,000** — board 451b, `AT.AK862.AJ9852.` — which currently opens 1H,
**wins +11 IMPs, and has a par gap of 0.00**. We are already at par there.

And the bridge is contested: with 6-5 and a strong hand most authorities open the
major precisely because the rebid is easy, and the change requires a mirror denial
on `open_1S`/`open_1H`, i.e. a **gate on the two most-fired rules in the file** to
capture one hand in a thousand boards.

**KILL.**

---

## 3. Interactions between the twenty

- **FIX 2 × FIX 18** — both add a notrump rung to `general_uncontested_continuation`
  (and FIX 18 also to `general_competitive_low`). Their changed sets are disjoint on
  this corpus, but FIX 2 sits at priority 28.5, immediately above `uc_nt2` (28),
  and FIX 18 pulls hands *out* of `uc_nt2` (board 920a). **Do not bundle.**
- **FIX 8 × FIX 18** — both change what a call means in `general_competitive_low`.
  FIX 8's deleted doubles land on `cl_nt2`/`cl_nt3`, which FIX 18 re-bands. Board
  194a's replacement is `cl_nt2` at fit 0.668 and would move again. **Do not bundle.**
- **FIX 2 × FIX 16 (killed)** — FIX 16's `uc_new_$X4` at priority 28 would have
  competed directly with `uc_nt_raise3` at 28.5 on the same seats.
- **FIX 10 (killed) × everything** — it moves partner's shown minimum for a
  two-level suit rebid, which feeds `rule_of_26` and therefore every raise, every
  notrump gate and both keycard families. Had it shipped in a bundle it would have
  confounded every other measurement in the round.
- **FIX 1 × FIX 19 (killed)** — the same structural move (a jump rung ranked above
  an existing overcall) in two different families. One family is at -2.92/-3.33 and
  the other at -0.33/+2.91. That contrast is the whole argument for both verdicts
  and is worth keeping as a worked example.
- **FIX 7 × FIX 12** — adjacent transfer contexts. `nt_after_super_accept`'s
  pattern (`1NT - P - 2$T - P - 3$M - P - ?`) and `nt_after_transfer`'s
  (`… - 2$M - P - ?`) cannot both match an auction, so there is no shadowing. Safe
  to bundle.
- **FIX 5 × FIX 13** — both in the 2C/Stayman region, different contexts, no
  shared call. Safe.
- **FIX 17 (killed) × the standing keycard open item** — this is the third attempt
  in three rounds to widen a keycard ask, and the third to be refused. It should be
  the last one attempted before the partner model gains a `total_points` ceiling.

---

## 4. ORDER OF WORK

**Bundle A — reach 0/2000, cannot move a number.** One measurement together;
expect **0 boards changed**. Keep on structure at zero measured cost (the round
7 / 8 / 11 / 13 precedent). Verify with a whole-corpus replay diff of 0 before
spending a match on it.

1. **FIX 5** — the Stayman quantitative 4NT **and** `stayman_quant_opener_decides`.
2. **FIX 11** — `rjrb_3M` priority 54 → 55.5.
3. **FIX 13** — length-is-quality on the 2C positives.
4. **FIX 15** — `opener_over_bail`.

**Bundle B — small, determinable, board-by-board attributable.** 9 tables, and
every changed call can be scored double-dummy on its own board. Expected
**+30 to +32** on the review corpus.

5. **FIX 7** — the super-accept answerer (2 tables, **+20**, both exact).
6. **FIX 1 (reshaped)** — the four-level major over a preempt (2 tables,
   **+10** exact on 410b, 0 to +9 on 199a).
7. **FIX 3 (with the `ch_neg_major_*` sweep)** — 3 tables, flat.
8. **FIX 6** — `standing_bid_strain` on the 2C Stayman placement (1 table, 0).
9. **FIX 12 (reshaped, with the 4$M floor)** — 1 table, **+2**.

**Singles — each MUST be measured alone.**

10. **FIX 2 (reshaped, `standing_bid_level: [2]`)** — 12 tables. It widens the
    3NT reading in the most-fired context in the engine and seven of its firings
    are competitive auctions reached through `... - P - ?`. If negative, decompose
    on `is_competitive`.
11. **FIX 8** — 7 tables. It removes half the firings of a convention, two of
    the tables it removes currently win +13 and +10, and two of the seats behind
    the deleted double land below the 0.9 fast-path threshold. If negative, fall
    back to the text-only repair.
12. **FIX 18 (reshaped, `i_have_acted: true`)** — 6 tables at par gap 0.00, i.e.
    at baseline on the attributable metric. This is the weakest survivor on the
    numbers and the strongest on the bridge.

**Pairs that must NOT be bundled**, with the reason: **2 with 18** and **8 with
18** (both listed above) — all three touch the meaning of a notrump or a double
in the same two generic contexts, and round 9's decomposition is the only reason
that round shipped anything.

**Do not run Bundle B and any single in one match.** Bundle B's nine tables are
attributable; the singles' twenty-four are not.

**Before any of it**: `python3 -m pytest -q`, `tools/lint_system.py`,
`tools/fuzz_decisions.py --n 300 --strict`. I linted every survivor prototype
individually: `collide` 0, `gap` 0, `shape` 0, `sibling` 0, `soft` 0, `floor` 223
— **identical to the committed system in every case**, including the three new
contexts.

---

## 5. KILLED, AND WHY — the negative results

| fix | verdict | the number that killed it |
|---|---|---|
| **4** takeout double of a weak two tolerates three | KILL — the asymmetry is a design | the branch reaches **3-4 tables at board mean +0.00** against a corpus mean of -0.73, two of them currently winning +3; and as written it turns board 896a's `KQT76` five-card spade overcall into a takeout double, the defect DECISIONS records closing twice |
| **9** drop the one-level suit-quality gate | KILL — threshold move on an above-baseline slice | 3 tables, **our gap +1.67** against -0.34; and removing the gate makes `cl_new_H1` and `cl_new_S1` tie at fit 1.00, so board 269b's **five spades become four hearts** — round 10's `r1m_1H`/`r1m_1S` defect, re-created |
| **10** a weak two-level rebid rung in seven families | KILL — the floor lesson, run backwards | 12 call changes, **7 of them our own raises collapsing to pass**, including a table we currently win by **+10**, because partner's shown minimum for a two-level own-suit rebid drops 11 → 6 across 28 rules |
| **14** suit-quality floor on the weak jump shift | KILL — the rule fires once and wins | `nx_1m1S_wj_H`: **1 table of 2,000, +1 IMP, our gap +1.00**; the gate reaches **0**; and the named twin `nx_1m1H_wj_S` **does not exist** |
| **16** four-level new suits in the uncontested toolkit | KILL — it annexes the balancing seat | 15 call changes, **6 of them displacing `balhigh_pass`** (round 12 measured that routing at -59 paired / -106 held out); plus `uc_minor_game_5D` displaced on 419b and a **fit-0.066** keycard ask on 691a |
| **17** a solo keycard ask in a game force | KILL — does not reach its own position | **0 of its 12 firings is a 2C auction**; the slice's board mean is **+2.08** against -0.73 with three tables at +11; and **5 of 12** are keycard asks opposite a partner who has shown 0-8 — the family measured negative in rounds 8 and 9 |
| **19** preemptive overcall of their 1NT | KILL — the family is healthy | `defense_vs_1NT` is **129 tables, mean -0.33, our gap +2.91**, above baseline on both; the rung reaches **2 tables**, both flat, one at par gap +10, and both changes replace a made two-level overcall with a three-level preempt |
| **20** open the longer minor with 6-5 | KILL — one table, and it wins | the whole-corpus population is **1 of 2,000** (board 451b), currently **+11 IMPs at par gap 0.00**; and the patch as written is vetoed by `open_1D`'s own `not:` clause and changes nothing |

Three further negative results worth keeping:

- **`fast_decision`, not `score_candidates`, is the engine's choice.** Ranking by
  blended score mislabels 25 of 10,346 decisions — every one a rule at fit
  0.946/0.965 beating a fit-1.00 pass on priority. `repro.rank_at()` returns the
  score order; a reviewer who reads its first row as "what we bid" will indict the
  wrong rule, which is the primary-reading trap with a different mechanism.
- **A slice can be above baseline on board margin and far below it on par gap, and
  the two disagree in both directions.** `nxj_X`'s doubles *without* a major win
  +3.50/table and sit at par gap -6.33; FIX 18's sandwich firings win +2.43/table
  at par gap +2.57. When they disagree, the par gap is the attributable one and the
  board margin is the one that will show up in the match. Quote both, always.
- **`weakest_their_stopper` still does not gate,** and it is now load-bearing in
  two of this round's proposals (FIX 18's new rung and FIX 8's replacement calls,
  which include a `cl_nt3` 3NT on `KT2` of their bid suit). Round 8 measured the
  one-line repair at -9 held out. It stays an open item, but it should be counted
  as a reason to distrust any new rule that leans on it.

---

## 6. Residue — what the twenty do not explain

1. **`cl_new_H1` bids a four-card heart suit ahead of a longer spade suit.**
   Both rungs are priority 30, so once both fit 1.00 the tie breaks on call rank
   and **1H wins**. Live today on two tables: board 181a bids 1H holding
   **KJ8762** of spades, board 344a bids 1H holding **T8763**. Round 10 fixed this
   for `r1m_1H`/`r1m_1S` and it was never swept into `general_competitive_low`.
   The one-line repair, measured at **2 call changes, lints unchanged**:
   ```yaml
   # cl_new_H1, BEFORE
             evals: { total_points: [6, 40] }
   # cl_new_H1, AFTER          (4-4 still goes up the line: both fit, 1H wins the tie)
             evals: { total_points: [6, 40], "suit_diff(H,S)": [0, 13] }
   ```
   This is worth more than FIX 9 was and it is not in the twenty.
2. **`resp_1m_over_1H` has no weak jump shift at all.** `1C - (1H) - 2S` on a
   six-card suit and under a free bid has no rule; the `1S` overcall context has
   `nx_1m1S_wj_H`. An additive sibling gap, the mirror of the one FIX 14 imagined.
3. **FIX 17's premise is a real open item even though its patch is dead.** After a
   2C opening, `r2c_2D_waiting` is `requires: {}` and `gf_new_3$X` has no point
   floor, so partner's shown minimum is **zero by construction** and every
   `rule_of_26_sharp >= 31` gate in the file is unreachable however strong the
   opener is. The repair belongs inside the 2C tree — `resp_2C` measures
   **15 tables, mean -0.60, our gap -7.87** — not in `general_slam_try`.
4. **`general_uncontested_continuation` still decides balancing-seat auctions.**
   Six of FIX 16's fifteen firings displaced `balhigh_pass`. Round 12's open item,
   re-confirmed from a new direction, and any future `uc_*` rung must be checked
   for it before it is written.
5. **The slam families are still the largest par-gap concentration in the corpus,
   and none of the twenty touches them.** Whole-corpus, by the context of the rule
   that actually chose (>= 8 tables):

   | context | tables | mean | our gap |
   |---|---|---|---|
   | `general_slam_try` | 10 | -3.90 | **-12.10** |
   | `rkc_response_agreed_H` | 9 | -5.00 | -9.67 |
   | `opener_rebid_after_2over1_minor` | 10 | -4.70 | -9.10 |
   | `rkc_continue_after_5H` | 13 | -3.46 | -8.00 |
   | `slam_try_over_game_raise` | 19 | -0.47 | -7.63 |
   | `rkc_response` | 30 | -0.93 | -7.50 |
   | **`opener_rebid_1H_1S`** | **30** | **-2.37** | **-6.07** |

   `opener_rebid_1H_1S` is the largest **non-slam** negative family in the corpus
   and nothing in this round or the last three looks at it.
6. **`nt_after_transfer` has no natural second-suit rung**, so a 5-6 hand after a
   transfer must choose between 3NT and four of the five-card major (FIX 12's
   board 709a is 5-5). The reshaped FIX 12 gives it the major; showing the second
   suit is still impossible.
7. **The soft-miss lottery is live at 0.946 in the notrump family.** Three of
   FIX 2's twelve firings, and all 25 of the score-order mislabels in §1, turn on
   half a point of `rule_of_26` clearing the 0.9 threshold. Sharpening it was
   measured at 3 tables / -2 IMPs in round 13 and killed; the residue is that a
   measurable fraction of the engine's notrump decisions are decided by a rounding
   margin rather than by an agreement.

---

## Editor's note — what actually happened when the survivors were applied

Added after the fact; the review above is the reviewer's document, unedited.

| survivor | verdict on the held-out number |
|---|---|
| Bundle A (FIX 5, 11, 13, 15) | 0 of 10,346 decisions change, as predicted. Kept on structure. |
| Bundle B (FIX 7, 1, 3, 6, 12, + Residue 1) | review +30, held out **+23**. Kept. Prediction was "+30 to +32" on review — exact. |
| FIX 2, at the reviewer's priority 28.5 | review +25, held out +2. Kept, then **re-ranked** — see below. |
| FIX 2, re-ranked to 26.5 | review -3, held out **+26**. The round's largest single gain. |
| FIX 8 | review +2, held out **-5** (4 boards, 1 up 1 down). **Reverted** to the reviewer's own fallback, the text-only repair. |
| FIX 18 | review +2, held out **-1** (10 boards, 4 up 4 down). **Reverted**; no fallback existed. |

**The one thing the review got wrong, and it was worth +26.** FIX 2's priority
of 28.5 was justified as "under `uc_nt3`, so the natural reading stays primary"
— reasoning only about the rung *above*. The natural three-level suit rungs sit
at 27.0 and 27.5, so the new raise outranked all of them, and `pytest` broke a
locked round-9 scenario: 5-5 in the majors opposite partner's 2NT raised to game
instead of bidding three spades. A raise is what you bid when there is nothing
left to describe. Re-ranked to 26.5 (above `uc_pass`, below every natural
three-level bid): 2 decisions change corpus-wide, both plainly right, and the
held-out corpus moved +26 on five boards with none against.

Both I and the reviewer made the same omission, so it is now a guardrail in
`ROUND_METHOD.md`: **price a new rung against the rungs below it, not only the
one above.**

Round totals: own deals -179 -> -114 (+65), review -729 -> -677 (+52), held out
**-525 -> -474 (+51)**.
