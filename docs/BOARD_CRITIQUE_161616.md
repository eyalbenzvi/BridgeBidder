# Round 15 findings (seed 161616, 1000 deals, -667 IMPs, 322 boards lost)

Method: every board we lost was read through `tools/roundkit/sweep.py`, which
joins the per-decision BEN audit to the match rows, re-resolves **the rule that
actually decided each call**, and groups the 827 disagreements into families.
Two instruments were built this round because the round could not be run
honestly without them; both are described in §0 and both changed verdicts.

Corpus: 10,385 of our decisions, mean board margin **-0.75**, mean OUR par gap
**-0.02**.

---

## 0. Two measurement corrections, before any finding

**(a) `explanation.source_rule_id` is the PRIMARY READING, not the rule that
decided the call.**  `replay.py`, `repro.fires()` and the match rows' `rule`
field all key on it.  It is the highest-priority rule producing the same call —
what the call *means* in the system — and on board 67a it names
`rr_nt_slam3_S` (priority 56, floor **19 HCP**) for a **15-count**, because
`rr_nt_gf3_S` (priority 53.5, band 12-18) matched at fit 1.00 and bid the same
3S.  `rr_nt_slam3_S` has never fired in 10,385 decisions.

I wrote three findings against it before checking.  `sweep.deciding_rule()` now
reconstructs `fast_decision` (keep everything fitting >= 0.9, take the highest
priority among those; otherwise the top blended score) and was validated against
the engine on **598 consecutive decisions with 0 mismatches**.

**(b) A rule must be judged against ITS OWN CONTEXT, not the corpus.**  Par gap
is jointly owned by the whole auction, so a context whose decisions land on
big-swing boards shows a bad gap whatever its rules do.  `opener_rebid_1m_1M`
runs at **-4.04** against a corpus mean of -0.02; `ob_rebid_2D` at -5.62 looked
like a 5.6-point outlier and is 1.6 below its own context, and `ob_rebid_2C`
(-4.18) and `ob_1NT` (-4.16) are **at** it — a within-context shuffle worth
nothing, despite BEN naming 1NT at confidence **1.00** on five separate boards.
`sweep.py --rank-rules` now prints the context-relative delta.

That correction killed five of my own candidates before they were written up:
`ob_rebid_2C`/`ob_1NT` (delta -0.17 / -0.15), `ob_1M1NT_3S` (-1.60),
`rr_nt_gf3_S` (-1.86), `rkc_5C` (-1.08) and **`gr_rkc_general_S` (-0.36)** —
the last of which revises a standing open item: round 8 blamed the keycard ask
over a game raise, and against its own context the ask is not the outlier.

---

## FIX 1 — the takeout doubler has no notrump rebid, anywhere

**Species: starved seat.  This is the round's largest and it holds the biggest
hands in the deck.**

The doubler's second call exists only as a **raise of partner's advance with
four-card support** (`uc_doubler_raise_$X` / `uc_doubler_raise3_$X` /
`uc_doubler_game_$X`, and the `cl_` twins), all gated `suits: { $X: [4, 13] }`.
A hand that doubled and holds a balanced 18-20 with a stopper — the textbook
"double first, then bid notrump, too strong for the 1NT overcall" hand — has
**no call at all** and takes `uc_pass` / `cl_pass` at fit 1.00.

| board | seat | hand | HCP | auction | we bid | BEN | gap |
|---|---|---|---|---|---|---|---|
| 351a | S | `A53.KQ9.AK86.KJT` | **20** | `P P 1S X P 2H P` | P (`uc_pass`) | 2NT 0.83 | **-15** |
| 559a | S | `3.AK32.QJ3.AKQ93` | **19** | `P P 1C X P 1S P` | P (`uc_pass`) | 1NT 0.57 | **-11** |
| 818a | N | `K86.KQ.AK73.AK84` | **20** | `P 1H X P 1S 2H` | P (`cl_pass`) | X 0.88 | **-11** |
| 79a  | N | `AT32.JT4.AKJ8.A2` | 17 | `1H X 2H P P` | 2NT (`ballow_nt2_strong`) | P 0.95 | -12 |

Traced live.  On 351a the whole candidate set is: **P `uc_pass` fit 1.00**, then
4H at 0.349, 3D at 0.349, 3NT at 0.328 — nothing else clears 0.35.  On 559a:
**P fit 1.00**, then 2H at 0.349.  Twenty points, and the only rule that fits is
the catch-all.  `uc_doubler_raise_H` demands four hearts and 351a holds `KQ9`.

**Denominator.**  `uc_pass` decides 54 of the audit's disagreements; the 18 with
13+ HCP run at par gap **-6.22** and board margin **-6.67** against corpus -0.02
/ -0.75.  This is also the mechanism behind FIX 4 below: `oc1H_X` is where the
strong balanced hand goes when the 1NT overcall's stopper gate refuses it, and
then the auction dies.

**Proposed fix (ADDITIVE — a new rung, fills a hole, subtracts nothing).**
A notrump rebid for the doubler, in `general_uncontested_continuation` and its
`general_competitive_low` twin, at a priority above the catch-all pass and below
the natural suit rungs:

```yaml
      - id: uc_doubler_nt2
        call: 2NT
        priority: 34.5
        when: { my_last_call_was_double: true, we_hold_contract: false,
                we_bid_last: false, their_last_bid_suit: true }
        requires:
          hcp: [18, 21]
          evals: { weakest_their_stopper: [0.9, 9], semi_balanced: [1, 1] }
        shows: "double first, then notrump: 18-21 balanced with their suit stopped, too strong for the 1NT overcall"
        establishes: { forcing: invitational }
```
plus the 1NT twin when the advance is still at the one level, and the `cl_`
mirror.  **ENDANGERS**: it leans on `weakest_their_stopper`, which has no sharp
tolerance (standing open item) — a hand with no stopper still scores 0.835, so
the rung will fire a little wider than it reads.  Measure alone.

---

## FIX 2 — `ballow_nt2_balance` denies no shape; its one-level sibling does

**Species: a gate given to one sibling and not the other.**

`ballow_nt1` (priority 27) carries
`not: { any_of: [ { suits: { H: [6, 13] } }, { suits: { S: [6, 13] } } ] }`.
Its two-level twin `ballow_nt2_balance` (priority 33) carries **no shape
condition at all**, so a five-card major balances 2NT instead of bidding the
suit.

| board | hand | HCP | auction | we bid | BEN | gap |
|---|---|---|---|---|---|---|
| 613a | `KQ732.A3.A83.Q43` | 14 | `2D P P` | 2NT | **2S 0.99** | -6 |
| 741a | `QJ963.A52.AKJ.83` | 13 | `2D P P` | 2NT | **2S 0.99** | -5 |

**Denominator.** 4 decisions, **0 on boards we won / 4 lost**, board margin
**-8.00** a decision against the context's -0.63, par gap **-7.25** against the
context's **+0.48** — a context-relative delta of **-7.73**, the third worst in
the corpus at n>=4.

**Landing verified**: on both boards `ballow_new_S2` (5+ spades, 10+ points,
quality) fits **1.00** at priority 26, so denying the 2NT sends them to 2S and
nothing is starved.  (The other two firings are `weakest_their_stopper`
casualties — 243a balances 2NT on `J654` of their suit at fit 0.96 — which is
the standing open item, not this fix.)

```yaml
# ballow_nt2_balance, add (the sibling's own clause, one card looser because
# at the two level a FIVE-card major is already worth more than 2NT):
          not: { any_of: [ { suits: { H: [5, 13] } }, { suits: { S: [5, 13] } } ] }
```

---

## FIX 3 — `balhigh_reopen_X` doubles on 5-5 two-suiters that partner converts

The rule's own comment says it: at the three level "the double commits partner
to the FOUR level and partner — who has passed throughout — converts it".  It
gates `max_their_suit_length: [0,2]` and `longest_suit_length: [0,5]`, so it
denies a six-card suit — and lets **5-5** through, which is the shape that most
wants to bid and least wants to defend.

| board | hand | shape | auction | gap |
|---|---|---|---|---|
| 454b | `AKQJ8.K43.AT543.` | 5-3-5-0 | `1C 1S 3C P P` | **-14** |
| 500b | `8.A2.KQ642.AKJ42` | 1-2-5-5 | `P 1D 1S X P 3D 3S P P` | **-15** |
| 236b | `J84.QJ.AKJ62.A85` | 3-2-5-3 | `P P 1H X 2H P P 3D 3H P P` | -10 |
| 551a | `A985.AKQ86.QJ94.` | 4-5-4-0 | `1C 1H 3C P P` | -4 |

**Denominator.** 6 decisions, **0 on boards we won / 5 lost**, board margin
**-6.00** against the context's -0.98, par gap -7.50 against **+2.67** — a
context-relative delta of **-10.17, the worst in the corpus at n>=4.**

**Proposed fix.**  A second-longest-suit cap, which is the shape statement the
comment already makes: a hand that can defend has one long suit, not two.
Needs `second_longest_suit_length` in `_EVAL_S2` (sharp), or, if a new evaluator
is out of scope, `longest_suit_length: [0, 4]` — which subtracts more and must
be measured as the alternative.  **This ADDS A GATE: it subtracts the double on
every 5-5 hand it reaches, and the seat behind it must be checked.**

---

## FIX 4 — the takeout double above 15 HCP is a different animal, and loses

`oc1H_X` fires 20 times.  Split on strength:

| slice | n | mean par gap | mean board margin |
|---|---|---|---|
| corpus | 10385 | -0.02 | -0.75 |
| `overcalls_of_1H` context | 129 | +0.78 | -1.32 |
| `oc1H_X`, all | 20 | -3.65 | -2.25 |
| **`oc1H_X` at 16+ HCP** | **9** | **-10.3** | — |
| `oc1H_X` at 10-15 HCP | 11 | **+1.8** | — |

The 16+ half: 69a (18, -15), 79a (17, -12), 329a (17, -12), 120b (17, -11),
818a (20, -11), 236b (15, -10), 282b (12, -10), 677a (17, -6), 78b (12, -6).
The 10-15 half is at or above baseline on both metrics.

`oc1H_1NT` exists at priority 82 and requires `hcp: [15,18], balanced: true,
features: [stopper(H)]`, so it refuses `AT32.JT4.AKJ8.A2` (17, `JT4`),
`KQT.93.AQ32.AQJ5` (17, `93`) and `K86.KQ.AK73.AK84` (**20**, outside the band).
Those hands then double — and FIX 1 shows they have nothing to say afterwards.

**FIX 4 is FIX 1's other half and should be measured with it, not against it.**
Standing alone I do not propose gating `oc1H_X`: that would starve the hands
exactly as round 14's FIX 8 starved `nxj_X`.

---

## FIX 5 — `defense_vs_1NT` has no strong natural overcall

`v1NT_X` is `requires: { hcp: [15, 40] }` and **nothing else**, at priority 70,
above every natural call.  The natural rungs (`v1NT_2C/2D/2H/2S`, priority 60-61)
demand **six** cards and cap at **15** HCP, so a 16-17 count with a good
five-card major has only the penalty double.

| slice | n | mean par gap |
|---|---|---|
| `defense_vs_1NT` context | 139 | +2.78 |
| `v1NT_X`, all | 9 | -2.33 |
| … with a 5+ card suit | 4 | **-7.25** |
| … balanced (4-card max) | 3 | **+2.0** |

The four: 214b `AQT65.AKJ9.T.KJ3` (17, gap -8), 462a `K3.AQ5.AKT854.QT`
(17, -9), 550b `AQ8542.A.AQ42.82` (16, -6), 410b `J8752.AT5.J.AKQT` (15, -6).

**Gating the double is NOT the fix and I checked**: ranked live, the natural
rungs on those hands fit **0.13 / 0.13 / 0.80 / 0.20** — every one below the 0.9
fast path.  Denying the double starves the seat, which is round 14's FIX 8
verbatim.  The fix is **ADDITIVE**: a strong natural rung.

```yaml
      - id: v1NT_2$M_strong
        call: 2$M
        priority: 71
        requires:
          suits: { $M: [5, 13] }
          hcp: [15, 19]
          features: [ "good_suit($M)" ]
        shows: "natural: a good five-card major with 15-19 - too much shape to defend 1NT"
        establishes: { forcing: non_forcing }
```
**ENDANGERS**: ranked above `v1NT_X`, so it subtracts the penalty double on
every 15-19 hand with a good five-card major.  The three balanced doubles that
currently run at +2.0 are untouched (they have no five-card suit).

---

## FIX 6 — the advance of a takeout double has no jump

`adx_pull_my_S3` / `adx_pull_S3` bid three of the suit and there is no
four-level rung, so a good hand cannot distinguish itself from a bust.

Board 970b, E `AKQT92.J75.J87.9` — **six spades headed by AKQ, 10 HCP**, over
partner's double of 3C — bids 3S.  BEN 4S at 0.76.  gap **-15**.

**Denominator.** `adx_pull_S3`: 4 decisions, **0 won / 4 lost**, par gap -10.00
against the context's -2.95 (delta **-7.05**), board margin -7.25 against -1.22.
Small, and three of the four are genuine minimums where 3S is right — this is a
**range with no rule**, so the fix is the missing top rung, not a change to 3S.

---

## Ruled OK, with the number

- **`cl_pass` -> X, 15 decisions, -90 IMPs** — the largest family by count and
  par gap **-0.07**, i.e. at baseline.  The board margin and the attributable
  metric disagree and the gap is the one that owns the decision.
- **`open_pass`, 25 decisions** — mean gap -2.08 with +15, +12, +7, +6, +4
  among them; opening-style thresholds are scope-excluded (ROUND_METHOD).
- **`rkc_5C`, 8 disagreements at BEN 0.90-1.00** — seven are **correct 1430
  answers** (verified by counting keycards on each hand); DECISIONS already
  records "our 1430 answers disagree with BEN's 3014 … that is a system
  difference, not a bug".  The eighth, 932b, is the grand-slam open item.
- **`rw2_2NT_ask`, 11 firings, delta -6.12** — I proposed extending its
  own comment's void rule to singletons.  Killed on its own numbers: the four
  singleton firings mean **-5.75**, the seven non-singleton firings mean
  **-5.14**.  No separation; the comment's principle does not extend.
- **`uc_raise_S3` (8, gap -0.62), `uc_nt2` (7, -0.71), `cl_new_S2_hi`
  (+4.67), `cl_new_C3_hi` (+0.33), `oc1C_1H` (+2.80)** — at or above baseline.
- **`sw_X`** — 12 firings, board margin -0.83 against a corpus -0.75.  The par
  gap looks bad (-1.42 vs +2.72) but the margin says baseline; not enough.
- **`open_2C`, 19 firings, delta -5.90, 3 won / 8 lost** — real and large, and
  it is the documented open item ("2C-2NT positive-response continuations have
  no landing ladder"), not a rule to tune.  The bad half is shapely 18-21
  two-suiters, but balanced 22+ counts are equally bad, so the opening
  condition is not what separates them.
