# Expert review A — CATEGORIES in the COMPETITIVE half (corpus seed 242424)

Reviewer A. Assignment: the rows of `reports/ben_audit_242424.jsonl` with
`first_divergence == true and ben_conf >= 0.80` **in which the opponents had
already made a non-pass call before our decision** — 179 of the 278 rows,
**-1020 IMPs** (the other 99 rows carry -637).

Nothing in the repo was modified except this file.

---

## 1. Method note

**What I built.**

- `filt.py` — the seat arithmetic that splits the 278 into 179 competitive /
  99 uncontested. Opponent = the two seats adjacent to ours; "competitive"
  means at least one of them has made a non-pass call in the prefix.
- `scan.py` / `scan2.py` / `scan3.py` — every one of the 179 decisions re-asked
  through `prepare_decision` + `score_candidates`, recording the full candidate
  ranking, the matched context, the `EvalContext` (including the new
  `their_*` fields), and the hand evaluators.
- **`corpus.py` — the artifact that did the real work.** All **10,355**
  decisions we made across all **2,000 tables** of `reports/e10_before.jsonl`
  (winners included), each with its auction features, its matched context, its
  `lott_total_trumps` per suit, and `their_min_hcp / their_max_fit /
  their_shown_count / is_competitive`. Every denominator below is computed on
  this table, not on the audit rows.
- Two denominators are quoted throughout. **`mean`** is the board IMP margin of
  the tables the slice touches (corpus baseline **-0.80**). **`gap`** is our
  side's par gap — `imps(score - par)`, signed for us — which controls for the
  boards being hard; corpus baseline **-0.38**. A slice whose `mean` is bad but
  whose `gap` is at baseline is a *hard-board* population, not a defect.
- `replay.py` / `one.py` / `diff2.py` — re-run all 10,355 decisions under a
  prototype YAML in a **separate process** and diff decision-by-decision. This
  is the "what does it subtract" instrument.
- `dd.py` — `EndplayDD` + `signed_score` + `imps`, so a flipped decision can be
  scored double-dummy and turned back into a board margin. BEN is not runnable
  here (no `torch`), so a full re-match is impossible; where a flip ends the
  auction I give the DD board margin, and I give it **twice** — once assuming
  the opponents never double our new contract and once assuming they always do.
  The truth is between. I state which number is which everywhere.

**Two things the method itself found, worth recording.**

1. **The first-divergence filter systematically hides the Law category.** Only
   **2** of the 179 rows are at a position where partner has bid a major and we
   hold ten-plus disclosed trumps, and in **both** the opponents have not yet
   confirmed their own fit. The Law position mostly arises at our *second or
   third* call, by which time we have already diverged, so the audit ranks it
   nowhere. The whole-corpus scan finds 16 tables at **-5.81**. For this class
   of category the audit is the wrong instrument and `corpus.py` is the right
   one.
2. **`prepare_decision`'s `_SETUP_CACHE` is keyed on `id(system)`**
   (`inference/engine.py`). Loading a baseline and a prototype in one process
   can collide after a GC and produce false diffs. Every prototype number below
   was re-measured in isolated processes. Anyone prototyping two YAMLs in one
   interpreter should clear that cache; I lost a measurement to it.

**Sanity.** The replay reproduces the recorded call on 10,354/10,355 decisions
under the committed system, so the harness agrees with the match.

---

## 2. THE CATEGORIES

### CATEGORY 1 — "The Law at the four level is a category, not a context"

**Bridge.** With ten trumps between us in a contested auction where the
opponents have also found a fit, four of the major is right on shape — whether
it makes or it is a save — and that is true wherever in the auction the
position arises: over their raise, over their game bid, in the reopening seat,
and after RHO has passed.

**Detection.** Exactly the seed's predicate, already in the vocabulary:

    when:    { partner_suit: $M, is_competitive: true }
    evals:   { "lott_total_trumps($M)": [10, 26], their_fit: [8, 26] }
    suits:   { $M: [4, 13] }

**What is wrong today.** The seed rung `cl_raise_lott4_H/S` exists **only in
`general_competitive_low`**. The same position reached one call later, or from
the balancing seat, or after RHO passes, lands in a different generic context —
and there the only four-level raise is again the combined-values one
(`total_points >= 11` **and** `rule_of_26 >= 25`), so the hand falls to the
context's catch-all pass. Concretely:

| context | four-level raise available | Law rung? |
|---|---|---|
| `general_competitive_low` | `cl_raise_S4` (`rule_of_26 >= 25`) | **yes** — the seed fix |
| `general_competitive_high` | `ch_raise_S4` (`rule_of_26 >= 25`) | `ch_raise_lott_S4`, **crippled** (see below) |
| `general_balancing_high` | `balhigh_raise_S4` (`rule_of_26 >= 25`) | **no** |
| `general_balancing_low` | `ballow_raise_S4` (`rule_of_26 >= 25`) | **no** |
| `general_uncontested_continuation` | `uc_raise_S4` (`rule_of_26 >= 25`) | **no** |

And `ch_raise_lott_H4/S4`, the one Law rung outside `cl_`, is a textbook
instance of *"a gate given to one rule and not its siblings"*:

```yaml
      - id: ch_raise_lott_S4          # today
        call: 4S
        priority: 32
        when: { partner_suit: S, we_vulnerable: false }     # <-- vul gate
        requires:
          suits: { S: [5, 13] }                             # <-- 5 trumps
          evals: { "lott_total_trumps(S)": [10, 26], total_points: [6, 40] }
```

`cl_raise_lott4_S` has neither the vulnerability gate nor the five-trump floor.
Board 862 table B is vulnerable, so the one Law rung the high context owns is
switched off on the very hand the category was named for.

**Evidence (whole corpus, 2,000 tables, baseline mean -0.80 / gap -0.38).**
Slice = *contested, partner has bid a suit, our disclosed combined trumps in it
>= 10, a four-level raise is legal, and we passed*:

| slice | tables | IMPs | mean |
|---|---|---|---|
| all suits | 36 | -111 | **-3.08** |
| **major fit** | 16 | -93 | **-5.81** |
| minor fit | 20 | -18 | -0.90 |
| major **and** `their_fit >= 8` | 10 | -78 | **-7.80** |
| major, `their_fit >= 8`, by context: `general_competitive_high` | 5 | -46 | -9.20 |
| ... `general_balancing_high` | 3 | -23 | -7.67 |
| ... `general_balancing_low` | 1 | -3 | -3.00 |
| ... `general_uncontested_continuation` | 1 | -6 | -6.00 |
| ... `general_competitive_low` | 0 | 0 | — |

Two readings matter. **The minors are not a defect** (-0.90, i.e. baseline) —
do not extend the Law rung to `4C/4D`. And **`general_competitive_low` is now
empty**, which is the seed fix working; every remaining table is in a context
that has no Law rung.

**Exact YAML — additive, four contexts, eight rungs.** Insert immediately before
`ch_raise_S2` / `balhigh_raise_S2` / `ballow_raise_S2` / `uc_raise_S2`
respectively (`$M` shown; write the H and S twins out, template vars must end
the id):

```yaml
      # THE LAW AT THE FOUR LEVEL, in the seat where the auction actually
      # reaches it.  `<pfx>_raise_S4` tests COMBINED VALUES (rule_of_26 >= 25),
      # which is the right test in a constructive auction and the wrong one in
      # a contested one.  When they have shown an eight-card fit and we have
      # ten trumps, the four level is right on shape.  Gates copied verbatim
      # from `cl_raise_lott4_S` so the category has ONE reading everywhere.
      - id: ch_raise_lott4_S
        call: 4S
        priority: 32
        when: { partner_suit: S, is_competitive: true }
        requires:
          suits: { S: [4, 13] }
          evals: { "lott_total_trumps(S)": [10, 26], total_points: [11, 40], their_fit: [8, 26] }
        shows: "the Law at the four level: they have a fit and so have we, ten-plus trumps our way - the four level is right on shape, not on combined points"
        establishes: { forcing: non_forcing, agreed_suit: S }
```

with `ch_` replaced by `balhigh_`, `ballow_`, `uc_` for the other three, and the
`H` twin in each. `is_competitive: true` is what keeps the `uc_` copy out of
uncontested auctions — the one place this rung has no business firing.

**The floor, per hard constraint 7.** 11 points, matching the sibling
`<pfx>_raise_$M4` in every one of the four contexts. Partner's shown minimum for
4M therefore does not move anywhere. In `general_competitive_high` the minimum
is *already* 6 (via `ch_raise_lott_S4`), so 11 is strictly conservative there.

**VERIFIED.** Prototype `p1.yaml`, replayed over all 10,355 decisions:

```
p1: 4/10355 decisions change; 4 tables, recorded IMPs -34, mean -8.50
   308a n= 6 S  P 1H 1S 2S 3S 4H          AQ98732.KJ4.J.65   P(ch_pass)      -> 4S(ch_raise_lott4_S)
   458b n= 7 E  1H 1S 2H 2S 4H P P        Q87652.7.A62.Q84   P(balhigh_pass) -> 4S(balhigh_raise_lott4_S)
   805a n= 7 N  1D 1S 2H 2S 3H P 4H       QJ743.Q3.85.KJT8   P(ch_pass)      -> 4S(ch_raise_lott4_S)
   862b n= 7 E  1C 1S 2H P 3H P 4H        AQ9763.T6.K3.KT2   P(ch_pass)      -> 4S(ch_raise_lott4_S)
```

**Four decisions change out of 10,355, and all four are the target position.**
Zero collateral. Double-dummy on the four boards:

| board | 4S tricks | board margin now | undoubled | doubled |
|---|---|---|---|---|
| 308a | 9 | -8 | **+0** | -3 |
| 458b | 9 | -11 | **-5** | -7 |
| 805a | 8 | +0 | **+6** | -2 |
| 862b | 7 | -15 | **-13** | -16 |
| **net** | | | **+22** | **+6** |

So: **+22 if they never double the save, +6 if they always do.** Both are
positive, which is the honest way to state it. 862b is the weakest of the four
(4S is down three double-dummy) and is the one the coordinator's `+1` measurement
of the un-gated seed rung was warning about.

**One further observation on the seed rung, offered as a finding.** The
`their_fit >= 8` gate now on `cl_raise_lott4_$M` excludes **both** of the
audit's own ten-trump boards — 610a (`P 1C 1S 2H`, BEN bids 4S at 0.95, -13) and
923b — because at the moment BEN acts, each opponent has shown only one suit and
`their_max_fit` reads 5. The gate does not delete the category; it **defers** it
one round, to the moment they raise. That moment is in
`general_competitive_high`, not `general_competitive_low` — which is precisely
why the seed fix on its own changes nothing after their raise and why this
category is its necessary completion.

**ENDANGERS.** (a) Partner's model: nothing, floor 11 matches every sibling.
(b) It bids 4M on hands that would otherwise defend, so a bad save costs the
double. The `their_fit >= 8` gate is the safety: with 18+ total trumps someone
is making something. (c) `ch_raise_lott_S4` and the new `ch_raise_lott4_S` are
same-call rules and merge into a disjunction; the new rung is *not* a subset of
the old (4 trumps vs 5, any vul vs NV), so 4S in `general_competitive_high`
becomes "6+ with five trumps NV, **or** 11+ with four trumps and 18 total
trumps, **or** the combined-values raise". That is three readings of one call and
it is the price. If the implementer prefers two, delete `we_vulnerable: false`
and lower `suits` to `[4, 13]` on `ch_raise_lott_$M4` instead and skip the `ch_`
rung — a widening, not a subtraction, and it reaches the same three boards.

**HIGH-VARIANCE: no** for the structure (it is a sibling gap in four contexts,
found by whole-corpus scan, not by two boards); **yes** for the size (four
tables in sample).

---

### CATEGORY 2 — "Once they have found a fit, repeating my own suit above the two level is bidding my hand twice"

**Bridge.** A rebid of my own suit is a *values* call in an uncontested auction
("am I worth another try opposite partner's shown range?") and a *level* call in
a contested one ("whose hand is it, and do we have the trumps to own the three
level?"). When the opponents have disclosed an eight-card fit and partner has
neither supported me nor given me a fit, three or four of my own suit is not a
call, it is a guess — and the extra trick belongs to them.

**Detection.**

    evals: { their_fit: [8, 26] }               # they have disclosed a fit
    evals: { "lott_total_trumps($X)": [0, 7] }  # partner has not supported me
    suits: { $X: [0, 6] }                       # and my suit is not self-sufficient

**What is wrong today.** Every generic own-suit rebid rung — 44 of them,
`{cl,ch,ballow,balhigh,uc}_rebid_$X{3,4,5}` — is gated on
`total_points` + `rule_of_26` + `suit_quality`. Not one of them knows anything
about the opponents. `uc_rebid_H3`:

```yaml
      - id: uc_rebid_H3               # today
        call: 3H
        priority: 29
        when: { my_suit: H, cheapest_in_suit: true }
        requires:
          suits: { H: [6, 13] }
          evals: { total_points: [11, 40], rule_of_26: [22, 99], "suit_quality(H)": [1, 9] }
```

`rule_of_26 >= 22` is the same wrong test as `rule_of_26 >= 25` on board 862,
pointing the other way: on 862 the combined-values test kept us *out* of a bid
the shape demanded; here it lets us *in* to a bid the shape forbids.

**Evidence (whole corpus).** Note the par gaps: this is the slice where `gap`
earns its keep.

| family | tables | IMPs | mean | **gap** |
|---|---|---|---|---|
| baseline | 2000 | -1608 | -0.80 | -0.38 |
| `uc_rebid_*` | 35 | -91 | -2.60 | **-5.14** |
| — of which `*3` | 22 | -80 | -3.64 | -5.82 |
| `balhigh_rebid_*` | 19 | -46 | -2.42 | **-4.42** |
| — of which `*4` | 12 | -35 | -2.92 | -4.92 |
| `ch_rebid_*` | 11 | -51 | -4.64 | **-3.91** |
| `ballow_rebid_*` | 15 | +16 | +1.07 | +1.07 |
| `cl_rebid_*` | 40 | -115 | -2.88 | **-0.53** |

Three families are 10x baseline **on par gap**, which says the auctions landed
far from the best available spot, not that the boards were hard. `cl_rebid_*`
looks equally bad on IMPs and is at baseline on gap — those are hard boards and
I do **not** accuse them. `ballow_rebid_*` is fine. The category is the
**three-level-and-above rebid in the high and continuation contexts**, ~65
tables.

The same population read from the reopening seat, which is where it hurts most:

| balancing seat (`... - bid - P - P - ?`) | tables | mean | gap |
|---|---|---|---|
| they have disclosed a fit, **we passed** | 385 | -1.14 | **+1.55** |
| they have disclosed a fit, **we bid** | 43 | -2.56 | **-3.47** |

**Exact YAML.** An `any_of` on the 44 rungs — a widening in form, a
restriction in effect, so I state it as a restriction:

```yaml
      - id: uc_rebid_H3
        call: 3H
        priority: 29
        when: { my_suit: H, cheapest_in_suit: true }
        requires:
          suits: { H: [6, 13] }
          evals: { total_points: [11, 40], rule_of_26: [22, 99], "suit_quality(H)": [1, 9] }
          # Repeat your own suit above the two level only while the opponents
          # have NOT found a fit, or you have found one of your own, or the
          # suit is its own trump support.
          any_of:
            - evals: { their_fit: [0, 7] }
            - evals: { "lott_total_trumps(H)": [8, 26] }
            - suits: { H: [7, 13] }
        shows: "rebid of my own H: 6+ cards, values for the level opposite partner's shown range"
        establishes: { forcing: non_forcing }
```

The third branch matters and was learned from a failed first draft: without it
the gate passed a hand holding **AKQJT95** of spades (board 192a), which is the
opposite of the intended bridge.

**VERIFIED as a subtraction; UNPROVEN as a gain.** Prototype `p3.yaml`:

```
p3: 16/10355 decisions change; 15 tables, recorded IMPs -27, mean -1.80
```

All 16 are `<rebid> -> P`. Double-dummy on the 13 where our call was the last
non-pass in the auction: **net +9 IMPs**, distributed +7 / +9 / +2 / +1 / -2 /
-6 / rest 0. That is noise-sized in sample, which for this project is the
signature of something that will measure flat or slightly negative held out.

**ENDANGERS.** It subtracts 15 tables of behaviour out of 2,000 — every one of
them a three-, four- or five-level rebid of our own suit into an opponents'
disclosed fit with no support from partner. Two of the fifteen (581b, 753b) are
boards we *won*, and double-dummy says neither result changes (the contract was
theirs either way). It also lowers what a 3-level rebid **shows** — partner may
now infer "or they had a fit and I could not bid", which is one more sentence of
bridge, not a worse one.

**HIGH-VARIANCE: yes.** Measure it as its own experiment; it is 44 rules and
+9 in sample.

---

### CATEGORY 3 — "The level at which I must answer partner's takeout double is part of the decision"

**Bridge.** A takeout double of 1C asks partner to bid at the one or two level
and is close to a command. A takeout double of 3C asks partner to bid at the
*four* level and is optional: with no fit and no values you pass and take the
penalty. Those are two different calls and the system answers both with the same
ladder.

**Detection.** `general_pull_or_sit` (`... - X - P - ?`) plus the level of the
standing bid — `standing_bid_level` is already a rule-level `when` key.

**What is wrong today.** In `general_pull_or_sit` the pull rungs are written out
per level and **carry identical `requires`**:

```yaml
      - id: adx_pull_C2 ... requires: { suits: { C: [4, 13] }, evals: { total_points: [0, 11], ... } }
      - id: adx_pull_C3 ... requires: { suits: { C: [4, 13] }, evals: { total_points: [0, 11], ... } }
      - id: adx_pull_C4 ... requires: { suits: { C: [5, 13] }, evals: { total_points: [0, 11], ... } }
```

A four-point hand answering a double of 1C bids 2C; the *same rule content* has
a four-point hand answering a double of 3C bid **4C**. `adx_pass_min`
(`total_points: [0, 11]`) sits at priority **52**, below every pull rung
(54-60), so the pull always wins and the pass is unreachable in exactly the
position where it is the bid.

**Evidence (whole corpus).**

| slice | tables | IMPs | mean | gap |
|---|---|---|---|---|
| baseline | 2000 | -1608 | -0.80 | -0.38 |
| `general_pull_or_sit` (all) | 84 | -84 | -1.00 | **-4.05** |
| — standing bid at the 1 level | 8 | +21 | +2.62 | -4.62 |
| — standing bid at the 2 level | 51 | -35 | -0.69 | -3.80 |
| — **standing bid at the 3 level** | 22 | -67 | **-3.05** | -3.59 |
| — level >= 2 and we bid | 58 | -67 | -1.16 | -4.26 |

The failure mode reads straight off the boards: 110a partner doubles 3S with 14,
advancer bids **4C** on `Q4.A65.965.AJ964` and goes two down (-13); 485a partner
doubles 3C with 18, advancer bids 3S on `AQT43.Q982.984.2` (-10); 616b partner
doubles 3C with **20**, advancer bids 3D on a four-count (-6); 625a, 2a, 935a,
166a, 303b are the same shape.

Whole-corpus context: our takeout double of a three-level preempt
(`v3_$X_X`) fires on 13 tables at mean **-2.85**, gap **-6.31**, against
`v3_$X_pass` on 24 tables at gap -0.92. It is not that the double is wrong; it
is that nothing can answer it.

**Exact YAML — additive, one rung.** A named pass whose priority is chosen to
outrank *only* the four-level pulls (54) and nothing else:

```yaml
      - id: adx_pass_four
        call: P
        priority: 54.5
        when: { their_last_bid_suit: true }
        requires:
          evals: { total_points: [0, 9] }
        shows: "partner's double of a preempt is optional: under ten points, four of a suit is not an answer - pass and defend"
        establishes: { forcing: sign_off }
```

Every two- and three-level pull (55-60) and every pull to my own five-card suit
(58-60) still outranks it, so it can only fire where the cheapest pull is at the
four level. It ships with the seat that answers it: none is needed — pass ends
our side's obligation and partner's double already established `one_round`.

**VERIFIED as a subtraction; the outcome is noise.** Prototype `p4.yaml`:

```
p4: 4/10355 decisions change; 4 tables, recorded IMPs -15, mean -3.75
   207a  P 1D 2D P 3S X P    KT.Q942.53.KT652   4C(adx_pull_C4) -> P
   429a  ... 3H X P          T3.6.JT2.Q986532   4C(adx_pull_C4) -> P
   625a  3S P P X P          Q432.J.T52.KQ653   4C(adx_pull_C4) -> P
   935a  P P 3S X P          QT.K8732.93.K985   4H(adx_pull_H4) -> P
```

Double-dummy: **+16, -9, +11, -10 — net +8 on four tables.** That is a coin
flip. I am reporting the *category* (the pull ladder is level-blind, and that is
a defect anybody can read off the YAML) and reporting honestly that my
prototype's own boards do not prove the repair.

**ENDANGERS.** Four tables in 2,000. It lowers what a four-level pull shows to
"10+ support points", which is the point. If measured negative, the residual
value is the diagnosis, not the rung.

**HIGH-VARIANCE: yes**, emphatically — justified on four boards.

---

## 3. The opponent vocabulary: what I used, and what I still want

The gap named in the brief is closed — `is_competitive`, `their_shown_count`,
`their_min_hcp`, `their_min_length`, `their_max_fit`, the evaluators
`their_fit / their_shown_hcp / their_bidders`, and the rule-level `when` key
`is_competitive`. **Category 1 and Category 2 are both written in it and could
not have been written without it.** Confirming the brief's own thesis: the
engine has held a full opponent model since it was written and no rule could see
it.

Four additions I would ask for next, each with the use I would put it to:

1. **`their_fit_suit: str | None`** — *which* suit their fit is in. With it,
   `lott_total_trumps($M) + their_fit` is the Law's actual **total trumps**, and
   the whole Law family collapses to one honest evaluator:
   ```yaml
   evals: { total_trumps: [18, 26] }     # "the Law says someone makes four"
   ```
   instead of the two-part `lott >= 10 and their_fit >= 8` proxy I had to use.
   Register it as SHARP in `_EVAL_S2` alongside `lott_total_trumps`: total
   trumps are counted, not estimated.

2. **`their_max_hcp: float`** — the *ceiling* of what they have promised.
   `their_min_hcp` alone cannot distinguish "they opened 3S on air" (min 5, max
   10) from "they have opened and responded" (min 20, max 40). Both read as
   "they have acted". The category I could not write for want of it is *"they
   have preempted, not bid"* — where our thin values are worth more, not less.

3. **`partner_is_limited: bool`** (or expose `partner_max_hcp` through an
   evaluator). `EvalContext` carries `partner_max_hcp` and **no evaluator reads
   it** — `rule_of_26` reads only the floor and caps the midpoint at floor+2. So
   no rule can say "partner has preempted and his range must not feed a
   combined-values test". I tested that hypothesis and it is **not** a defect
   concentration on this corpus (see NON-FINDINGS 5), but the field is one line
   and the next corpus may say otherwise.

4. **`we_are_pushed: bool`** — our side opened the auction and they have since
   disclosed a fit. Cheap (it is `is_competitive` plus who made the first bid)
   and it is the only clean way to name the brief's "Law auctions where WE are
   being pushed". I measured that population and it argues for bidding *less*
   (NON-FINDINGS 8), which is itself a rule worth being able to write.

---

## 4. Residue — the 179 rows my categories do NOT explain

My three categories account for **3** of the 179 audit rows directly (the
`adx_*` advances, -21 IMPs). That is not a failure of the categories; it is the
first-divergence artifact described in the method note — Category 1's 16 tables
and Category 2's 65 tables are almost all at our *second* call. The honest
accounting of what the 179 rows actually are:

| species | rows | IMPs | verdict |
|---|---|---|---|
| **we doubled, BEN did not** | 24 | -126 | see below — genuinely close, and BEN is not right |
| **BEN doubled, we did not** | 26 | -154 | same population, mirrored — see NON-FINDINGS 7 |
| we bid, BEN passed (other) | 44 | -210 | ~15 are Category 2's disease at a first call; the rest are judgment |
| we passed, BEN bid (other) | 30 | -168 | mixed; 6 are the 3-level preempt seat |
| bid-vs-bid, different suit/level | 27 | -182 | mostly which of two suits to name |
| **MEASURED — weak jump overcall overlap** | 12 | -87 | round 11 measured the repair at **-24 held out**. Not re-proposed. |
| **SCOPE — conventions we do not play** | 13 | -72 | BEN's 2C/2NT over 1NT, its 1NT in the sandwich seat: Cappelletti / unusual NT, scope-excluded |
| advance of partner's X at the four level | 3 | -21 | **Category 3** |

The two double columns are the largest species in the set and they **cancel**:
26 rows where BEN doubles and we do not (-154) against 24 where we double and
BEN does not (-126). A category that says "double more" and a category that says
"double less" cannot both be right, and the corpus (NON-FINDINGS 7) says
neither is. I read this species as **genuinely close judgment**, and the 50 rows
/ -280 IMPs as the honest cost of not having a hand evaluator that knows the
difference between 13 flat and 13 with a fifth trump. That is a quarter of my
half of the corpus, and I have nothing structural to say about it.

Two smaller residues worth naming rather than fixing:

- **BEN is wrong at least some of the time here.** Board 923b and 862a both have
  BEN at 0.80-0.95 for a call that double-dummy makes worse. `first_divergence`
  plus high confidence is a lead, and on 4 of the 20 rows I DD-checked, the lead
  was bad.
- **Nine rows are `general_their_double` (`xd_*`) run-outs** — pulling partner's
  penalty double, the known open item "there is no condition for *partner's
  double was PENALTY*". I did not develop it; the corpus slice is
  `general_their_double` at gap **+1.75** on the Law population, i.e. those seats
  are not obviously broken, and DECISIONS records the four-level pull measured
  at -22 held out.

---

## 5. NON-FINDINGS — category hypotheses I killed, with the data

The brief named six things to test rather than assume. Five of them are dead on
this corpus. Each line is the whole-corpus denominator; baseline is mean -0.80,
gap -0.38.

1. **The Law at the THREE level. DEAD.** Nine disclosed trumps, a three-level
   raise legal, and we passed: **62 tables, mean -0.44, gap +2.60** — better
   than baseline on both. Restricted to their-fit-shown-and-a-major: 6 tables,
   mean +0.83. This independently confirms round 11's revert of
   `cl_raise_lott3_$M` from a different direction: the *gate* on that rung is
   genuinely broken (`cheapest_in_suit` excludes a jump) and the *population
   behind it does not lose*. Do not unblock it.

2. **The Law in the MINORS. DEAD.** Same predicate as Category 1 but a minor
   fit: **20 tables, -18 IMPs, mean -0.90.** Baseline. Do not write
   `cl/ch_raise_lott4_C/D`. (This is why Category 1 is majors-only.)

3. **The Law at the FIVE level. STRUCTURALLY REAL, NOT WORTH FIXING.** There is
   **no five-level raise of partner's suit anywhere in the system** — not in
   `cl_`, `ch_`, `ballow_`, `balhigh_` or `uc_`; `ch_new_$X5` and
   `ch_rebid_$X5` exist, `ch_raise_$X5` does not. So `1H - (4S) - ?` with ten
   hearts has no 5H. But the population is **31 tables at mean -1.00** — not
   distinguishable from baseline. A real hole that does not pay.

4. **The misfit auction. DEAD.** Both opponents have promised values
   (`their_min_hcp >= 20`), neither side has disclosed a fit, competitive:
   **40 tables, mean -0.45**; the sub-slice where we bid on anyway: 9 tables,
   mean -0.56. Better than baseline in both. "Competing further in a misfit is
   wrong, and our ladders still climb" is a good bridge maxim and is not a
   defect concentration in this engine.

5. **`rule_of_26`-gated rungs firing opposite a preemptive partner. DEAD.**
   The 24 competitive raise rungs gated on `rule_of_26` fire on **78 tables at
   mean -0.65** — better than baseline. Opposite a partner whose shown maximum
   is 11 or less: **18 tables at -1.39**, which on 18 tables is not a signal.
   The mechanism is also weaker than it looks: `rule_of_26` caps partner's
   midpoint at floor+2, so a weak two contributes 7, not 12.

6. **The reopening/balancing seat IS a distinct category — and it says bid
   LESS, not more.** Balancing decisions split by `their_fit`:
   fit disclosed 419 tables gap +1.16 vs no fit 771 tables gap +1.89; and within
   the fit-disclosed half, **we passed: 385 tables gap +1.55; we bid: 43 tables
   gap -3.47.** Balancing into a fit they have already shown is the single worst
   thing our balancing contexts do. Category 2 subtracts the largest coherent
   slice of it (the own-suit rebid); the rest is 26 different rules with one or
   two firings each and I have no single named category for it.

7. **The missing competitive / reopening double. DEAD, and the sign is
   backwards.** Both `cl_negative_X1/X2` carry `i_have_acted: false` and
   `cl_takeout_X` carries `side_has_acted: false`, so once both members of our
   partnership have acted **no rule defines X** and the code fallback double
   loses to the catch-all pass on priority. Six audit rows want that double
   (375b at BEN 0.99, 638a at 0.95, 217b, 359b, 495a, 223a). The corpus says
   no: in that exact position (competitive, both of us have acted, their suit
   stands, level <= 3) **we passed with 12+ on 108 tables at mean -0.21** — well
   above baseline — while **the 20 tables where we did double are mean -1.10,
   gap -3.45.** Doubling more there loses.

8. **"They have found a fit and we have not" as a reason to compete. DEAD.**
   Competitive, `their_fit >= 8`: 366 tables at mean -1.6, but the par gap is
   -0.28 — these are boards where they have the balance of power, not boards we
   misbid. Split by who opened: we opened and they found a fit, 109 tables mean
   **-1.95** but **gap -0.70**; and when we bid on there, gap **-2.90** on 39
   tables. "Law auctions where WE are being pushed" argues for passing.

9. **The missing double of a NOTRUMP contract. STRUCTURALLY REAL, DEAD ON
   NUMBERS.** Every balancing/takeout double rung in the generic contexts —
   `ballow_X`, `ballow_reopen_X/X2`, `balhigh_X`, `balhigh_reopen_X/X2`,
   `cl_takeout_X` — carries `when: { their_last_bid_suit: true }`. When their
   contract is notrump, **no rule defines X at all** (boards 984b and 415a show
   the fallback double at fit 1.00 losing to the catch-all pass). But: their NT
   stands and we passed, **495 tables at mean -0.50**; balancing over their NT,
   259 tables at -0.61; `1NT - P - P - ?` specifically, **69 tables at -0.06**.
   All better than baseline. A clean hole with no money in it.

10. **"The catch-all pass over their preempt is starving a big hand." DEAD.**
    `balhigh_pass` with 15+ HCP: 30 tables at mean **-0.27**; with 17+: 15
    tables at **+0.33**. The known open item "19 HCP with a void passed their
    3S" is a real sentence about one board and not a concentration. (What *is*
    a concentration in that area is Category 3 — the seat that answers the
    double we do make.)

11. **The weak jump overcall / preemptive overcall overlap.** Twelve rows of my
    179 (-87 IMPs) are ours-1S vs BEN's-2S/3S on a six- or seven-card suit.
    Round 11 measured the re-ranking at **-24 held out** and reverted it. Not
    re-proposed. I note only that the seven-card cases (110a, 308a) are a
    *shape* argument rather than the 8-10 HCP overlap that was measured, and
    that if anyone revisits it, that is the disjoint slice.

---

## 6. Order of work

| # | category | tables in sample | in-sample estimate | risk |
|---|---|---|---|---|
| 1 | Law at the four level, in the other four contexts | 4 changed / 16 in population | **+22 undoubled, +6 doubled** | low — 4 decisions change out of 10,355, all on target |
| 2 | own-suit rebid into their disclosed fit | 15 changed / 65 in population | **+9** (DD, 13 evaluable) | medium — 44 rules gated; measure alone |
| 3 | advance of a takeout double at the four level | 4 changed | **+8**, distributed +16/-9/+11/-10 | high — noise; ship the diagnosis, measure the rung separately |

Category 1 is the one I would implement. It is the seed category finished: the
same sentence of bridge, the same gates, in the four contexts where the auction
actually arrives at the position, plus the sibling repair on
`ch_raise_lott_$M4` whose vulnerability gate switches the Law off on the very
board the category is named for.
