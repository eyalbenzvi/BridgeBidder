# Expert B — constructive / team-IMP review of dossier part 4

**Scope.** All 38 boards of `docs/dossier_575757/part04.md`, read through the
constructive-auction lens: the 2/1 machinery, opener's and responder's rebid
structures, the invitational/game boundary, game tries, and the shape-showing
that separates a minimum from a slam-going hand *before game is reached*.

**Counts.** 38 boards · **31 proposals** (each with exact YAML) · **7
NOTHING-WRONG** (boards 93, 116, 272, 274, 704 — opening-style thresholds,
scope-excluded; 343, 894 — purely competitive with the observation recorded).
20 of the 31 proposals are **VERIFIED** — I traced the seat through
`repro.rank()` / `repro.ask()` and quote the fit and priority that decided it.

## The three agreements that matter most in this slice

1. **Responder's invitational jump rebid over opener's second suit has no
   answering seat at all.** `r1d1h2c_3H` and `r1d2c_3S` establish
   `forcing: invitational` and then land in `general_uncontested_continuation`,
   where `uc_pass` fits **1.000** and opener passes a live invitation with a
   fitting hand. VERIFIED on boards 132 and 563; both were cold games passed
   out at the three level. This is the round-17 finding in its purest form —
   the machinery is at the three level, and the question exists while the
   answer does not. Proposal: the `opener_over_responder_jump_rebid` context
   (§Board 132), plus a game-forcing tier so 14+ never has to invite.

2. **The invitational/game-force boundary at exactly 12 HCP is decided by
   priority, not by bridge.** `r1m_2over1` / `r1H_2C` sit at priority 70-75
   with a floor of 12 HCP; `r1m_2NT` (11-12 balanced) and `r1H_limit_raise`
   (8-11 HCP, 10-13 support points) both fit or nearly fit the same hands but
   sit at 54 and 62. A flat 12-count with three-card support or no fit is
   force-fed into a game force it cannot survive. VERIFIED on boards 348 and
   782. Proposal: two re-priced rungs, `r1m_2NT_flat` and
   `r1H_limit_raise_flat` (§Boards 348, 782).

3. **Trial bids and help-suit game tries are still at zero rules, and the one
   rung that stands in for them — `op_after_raise_inv` (3M on 17-18 total
   points) — cannot say WHERE the help is needed.** Proposal: a complete
   help-suit-try conversation (opener's try, responder's accept/decline,
   both templated over both majors and all three trial suits) in §Board 188.

Two further structural species recur and are worth naming once:

* **`cheapest_in_suit: true` on a JUMP rung makes the rung unreachable** —
  the documented `cl_raise_lott3_$M` bug, found again on `cl_raise_D3`
  (board 632), `xd_rebid_D3` (board 707) and their whole sibling families.
  Every constructive jump raise in competition is dead code for this reason.
* **`lott_total_trumps` counts partner's SHOWN minimum**, so after a PASS it
  is zero and after a one-level major response it is four; every rung gated on
  8+ or 9+ combined trumps is unreachable in exactly the seats where opener
  wants to raise or jump (boards 658, 707).

---

## Board 632 — S, call 2 (`1D (2C) ?` with `742.Q942.AK7642.`)

**Went wrong:** S passed (`cl_pass`, fit 1.000, prio 20) holding a six-card
diamond fit headed by AK and 9 HCP.

**Missing agreement (one sentence).** With three or more trumps, ten-plus
support points and nine-plus combined trumps, the raise is a JUMP — the
fit-showing/mixed raise — and the engine has none, because `cl_raise_D3`
carries `cheapest_in_suit: true` and a jump is by definition not the cheapest
call in the suit.

Diagnosis: `cl_raise_D2` is banded `total_points: [6, 12]`; this hand is a void
and a six-card fit above that, so it fits **0.409**. `cl_raise_D3` (8+ points,
`rule_of_26 >= 22`, 8+ trumps) is the right description and never appears in
the candidate list at all — its `when` gate rules it out structurally. This is
the same defect as the documented `cl_raise_lott3_$M` bug but on a *different*
rule with different content, so freeing it is not the round-11 experiment.

```yaml
# in context general_competitive_low, beside cl_raise_D2 / cl_raise_D3
      - id: cl_fitjump_$M
        call: 3$M
        priority: 30.5
        when: { partner_suit: $M, cheapest_in_suit: false }
        requires:
          suits: { $M: [3, 13] }
          evals:
            total_points: [10, 40]
            rule_of_26: [22, 99]
            "lott_total_trumps($M)": [9, 26]
        shows: "fit-showing jump raise of partner's $M: 10+ support points, nine-plus combined trumps"
        establishes: { forcing: non_forcing, agreed_suit: $M }
```
`expand: { M: [C, D, H, S] }` — the agreement is identical in all four suits
and the rule id ends in the template var. The minor half is the one this board
needs; the major half is the standard mixed raise.

**Answering seat.** None required: `establishes: forcing: non_forcing`, so this
is a competitive placement, not a question. Partner's continuation is already
covered by `general_competitive_high` / `general_balancing_high`.

**Endangers** (everything in `general_competitive_low` whose call this rung can
outrank at the same fit): `cl_pass` (20) — a six-card fit with ten support
points is not "no bid describes this hand"; `cl_new_*3` (27/27.5) and
`cl_nt2`/`cl_nt3` (28/29) — with a known nine-card fit the raise is a better
description than a new suit or a notrump guess; `cl_raise_$M2` (30) — this rung
starts one point above where that one ends, so the two do not overlap. It is
deliberately placed BELOW `cl_raise_D3` (31), `cl_raise_lott3` (32),
`cl_negative_X` (33) and `cl_takeout_X` (36), all of which describe hands this
rung does not claim.

**VERIFIED** — `rank()` reproduces the dossier: `cl_raise_D2` 0.409,
`cl_raise_D3` absent from the candidate set.

**Template:** `expand: { M: [C, D, H, S] }`; a `we_vulnerable` split is NOT
recommended (the LOTT gate already carries the safety).

---

## Board 707 — S, call 7 (`1D - P - P - (X) ?` with `9875.A.AKQJ93.A7`)

**Went wrong:** S rebid 2D (`xd_rebid_D2`, fit 1.000, prio 34) with **18 HCP
and AKQJ93** — the same call the rule gives an eleven-count.

I checked N's pass first (the dossier's first divergence): `r1m_1H` fits 0.800
on a 5-count with `T765`. Passing a 3-4-3-3 five-count is normal bridge and I
do not think BEN's 1H is an agreement worth buying — see board 558, where the
same rule misses on a hand that *should* respond. **NOTHING-WRONG on the
response; the constructive defect is one call later.**

**Missing agreement.** After partner has passed and they balance with a double,
opener's rebid ladder has no strength tier, because the jump rung
(`xd_rebid_D3`) is doubly unreachable: `cheapest_in_suit: true` (2D is the
cheapest diamond call, so 3D can never satisfy it) and
`lott_total_trumps(D) >= 9`, which counts partner's shown minimum — zero after
a pass.

```yaml
# in context general_their_double, beside xd_rebid_D2 / xd_rebid_D3
      - id: xd_jump_own_$X
        call: 3$X
        priority: 34.5
        when: { we_bid_last: true, my_suit: $X, cheapest_in_suit: false }
        requires:
          suits: { $X: [6, 13] }
          evals: { total_points: [17, 40] }
          features: [ "three_of_top5($X)" ]
        shows: "jump rebid of my own doubled $X: a six-card suit I can play opposite nothing, 17+ points"
        establishes: { forcing: non_forcing }
```
`expand: { X: [C, D, H, S] }`.

**Answering seat.** `forcing: non_forcing` and partner is a passed hand, so no
question is asked. The seat that hears it is `general_their_double` /
`general_competitive_high` for the opponents' side and
`general_uncontested_continuation` for partner, both of which already answer a
three-level contract of ours.

**Endangers:** `xd_rebid_D2` (34) — with 17+ and three of the top five, a
second bid at the same level under-describes and invites them to balance
cheaply; `xd_XX_extras` (23) — a self-sufficient suit beats an announcement of
strength (the file's own comment says exactly this); `xd_pass` (18). It is
below `xd_run_*` (26)? No — it is ABOVE them at 34.5, which is correct: those
describe a hand running to a NEW suit, this one repeats a suit already bid.

**VERIFIED** — traced `["P","P","P","1D","P","P","X"]`: `xd_rebid_D2` fit 1.000
prio 34 decides; `xd_rebid_D3` never enters the candidate set.

**Template:** `expand: { X: [C, D, H, S] }`.

---

## Board 758 — N, call 6 (`(1D) 1H P P ?` — balancing, `AQ95.Q8.6532.AQ2`)

**Mostly competitive** — the choice between a reopening double and 1NT belongs
to the other reviewer. The constructive-discipline observation is real though
and it is a **priority inversion**: `ballow_new_S1` fits **1.000** at priority
25 and `ballow_nt1` fits 0.965 at priority 27, so a 1NT rebid outranks a
four-card major at the one level. Constructive ordering is the opposite: show
the major first; notrump is what you bid when you have nothing to show.

```yaml
# in context general_balancing_low, beside ballow_new_S1
      - id: ballow_major_first_$M
        call: 1$M
        priority: 27.5
        when: { unbid_suit: $M, cheapest_in_suit: true }
        requires:
          suits: { $M: [4, 13] }
          evals: { total_points: [11, 16], "suit_quality($M)": [2.0, 9] }
        shows: "a good four-card $M at the one level: showing the major before rebidding notrump"
        establishes: { forcing: non_forcing }
```
`expand: { M: [H, S] }`.

**Answering seat.** Non-forcing; partner answers in
`general_uncontested_continuation`, which already has raise and preference
rungs for a one-level major.

**Endangers:** `ballow_nt1` (27) — with four good spades and 11-16 the suit is
the better description and keeps the major fit findable; `ballow_new_S1` (25),
which it supersedes on exactly the hands it claims; `ballow_pass` (21). It stays
BELOW `ballow_nt2` (28), `ballow_nt2_balance` (33) and `ballow_reopen_X` (41),
which describe stronger or shapelier hands.

**UNTESTED** as a rung (the fit numbers above are VERIFIED from the dossier's
own candidate table).

**Template:** `expand: { M: [H, S] }`.

---

## Board 788 — N, call 4 (`(1H) X P ?` with `KJ986.986.AT5.54`)

**Went wrong:** N advanced 1S (`advH_1S`, "0-8, spades (forced)", fit 1.000,
prio 54) with **five** spades and 8 HCP; `advH_2S_jump` needs 9-11 and fits
0.800.

**Missing agreement.** The jump advance of a takeout double is banded on HCP
alone, so a five-card suit with 8 points has to make the same call as a
four-card suit with 2 — the mixed advance (a fifth trump is worth the extra
level) has no rung.

```yaml
# in context advance_takeout_double_suits_H (and its C/D/S siblings)
      - id: advH_2S_five
        call: 2S
        priority: 61
        requires:
          suits: { S: [5, 13] }
          hcp: [7, 11]
          evals: { total_points: [9, 13] }
        shows: "mixed jump advance: a five-card spade suit and 7-11, a level more than a courtesy response"
        establishes: { forcing: invitational }
```

**THE ANSWERING SEAT** — this establishes `invitational`, so it ships with the
seat that answers it. `1H - X - P - 2S - P - ?` has no context today:

```yaml
  - id: doubler_over_jump_advance
    description: "The doubler over partner's invitational jump advance"
    expand_pairs:
      - { o: H, v: S }
      - { o: S, v: H }
      - { o: C, v: D }
      - { o: D, v: C }
    pattern: "1$o - X - P - 2$v - P - ?"
    rules:
      - id: dja_pass_$v
        call: P
        priority: 50
        requires: {}
        shows: "minimum takeout double: passing the invitational advance"
        establishes: { forcing: sign_off }
        negative_inference_weight: soft
      - id: dja_raise_$v
        call: 3$v
        priority: 52
        requires: { suits: { $v: [4, 13] }, evals: { total_points: [15, 17] } }
        shows: "four-card support and 15-17: pressing the invitation"
        establishes: { forcing: invitational, agreed_suit: $v }
      - id: dja_game_$v
        call: 4$v
        priority: 54
        requires: { suits: { $v: [3, 13] }, evals: { total_points: [18, 40] } }
        shows: "accepting the invitational advance: 18+ opposite 7-11"
        establishes: { forcing: sign_off, agreed_suit: $v }
```
The `requires: {}` pass is the round-6 `rkc5H_signoff` lesson: every sign-off in
a new context must fit 1.00 so the seat can never be starved.

**Endangers** in `advance_takeout_double_suits_H`: `advH_1S` (54) — with five
spades and 8 points, the one-level advance loses the level partner needs;
`adv_1NT` (55) — a five-card major beats a notrump advance; `advH_2S_jump`
(60), whose 9-11 band this rung extends downward on shape alone; `adv_2NT` (56).
It stays BELOW `adv_cue` (75), the game-forcing advance, and
`adx_pull_S4` (58) is a different call. The new CONTEXT is a
`1$o - X - P - 2$v - P - ?` pattern with four tokens plus a leading digit, so
specificity 1005 — it owns a seat that today falls into
`general_uncontested_continuation`; every call it defines (P, 3$v, 4$v) is one
that context also produces, and the `requires: {}` pass keeps it a superset for
the pass.

**VERIFIED** for the diagnosis (the dossier's candidate table is reproduced by
`rank()`); the new context is **UNTESTED**.

**Template:** the `expand_pairs` above (both majors as the doubled suit and
both minors, i.e. the four "cheapest jump advance" pairs).

---

## Board 894 — N, call 2 (`1D (X) ?` with `JT9.J853.J.J9874`)

**Purely competitive** — running from a takeout double is the other reviewer's
territory, and the deciding rule `xd_run_C2` is a competitive rung.

The constructive-discipline observation, recorded because it is a **sibling-gate
asymmetry** of exactly the species the lint suite exists for: every
`xd_rebid_*` rung carries `evals: { total_points: [11, 40] }` (or 14+ for the
jump), and every `xd_run_*` rung carries **no strength or quality gate at all**
— `requires: { suits: { C: [5, 13] } }` and nothing else. A 4-HCP hand with
`J9874` therefore removes partner's opening to two clubs at fit 1.000, ahead of
a pass that also fits 1.000.

The repair is a GATE, so I state what it subtracts: adding
`evals: { "suit_quality(C)": [1.5, 9] }` to `xd_run_C2` (and its D/H/S twins)
removes the run from every hand whose five-card suit is headed by nothing,
handing those seats back to `rdx_pass` at fit 1.000 — i.e. it converts a
lead-directing removal into a pass on roughly the weakest quarter of its
population. That is the right direction on this board and I would want it
measured on its own, not bundled: `fires_summary(..., "xd_run_C2")` is the
honest denominator and I have not run it.

**NOTHING-WRONG within the constructive discipline.**

---

## Board 922 — N, call 2 (`1D (1S) ?` with `2.T6.98764.KQ832`)

**Went wrong:** N passed (`nx_1m1S_pass`, fit 1.000, prio 20) with five-card
diamond support, a singleton in their suit and 5-5 shape.

**Missing agreement.** `resp_1m_over_1S` has a simple raise (6-10) and a cue
raise (10+) and **no preemptive or mixed jump raise**, so a hand with nine
combined trumps and a singleton in their suit — the classic shape for taking
away the whole one level — has nothing but a pass.

```yaml
# in contexts resp_1m_over_1S and resp_1m_over_1H
      - id: nx_1m1S_preempt3_$m
        call: 3$m
        priority: 54
        requires:
          suits: { $m: [5, 13] }
          hcp: [3, 7]
          evals: { "lott_total_trumps($m)": [9, 26] }
          features: [ "singleton_or_void(any)" ]
        shows: "preemptive jump raise: five-card support, shortness, less than a free bid"
        establishes: { forcing: non_forcing, agreed_suit: $m }
```
(`resp_1m_over_1S` already carries `expand: { m: [C, D] }`; the template var
ends the id.)

**Answering seat.** Non-forcing and weak: opener's continuation is
`general_competitive_*`, which already prices a three-level minor contract of
ours. No question is asked, so no new context is owed.

**Endangers:** `nx_1m1S_pass` (20) — a nine-card fit with a stiff in their suit
is not "nothing to say"; `nx_1m1S_1NT` (50) — no stopper and a singleton; the
weak jump shift `nx_1m1S_wj_H` (56) is ABOVE it, correctly, because a six-card
suit of my own outranks support. It sits below `nx_1m1S_raise` (55) so the
constructive 6-10 raise is never stolen — the two bands do not overlap
(3-7 vs 6-10 only touches at 6-7, and there the shortness and fifth trump
decide, which is the standard treatment).

**UNTESTED** (the dossier's candidate table is the evidence).

**Template:** `expand: { m: [C, D] }` in both `resp_1m_over_*` contexts; the
major-suit analogue belongs in `resp_1H_over_1S` and is the same idea.

---

## Board 988 — S, call 10 (`1H (X) 2H (2S) 3H (3S) P P ?` with `76.KT9863.AK5.K4`)

**Went wrong:** S bid 4H (`balhigh_rebid_H4`, fit 1.000, prio 29) after already
bidding 3H on the same values.

**Missing agreement.** Partner's 2H was a `jordan_raise` — a LIMITED call — so
the combined values are known within a point or two; but
`balhigh_rebid_$M4`'s only test is "6+ cards and values for the level opposite
partner's shown range", which contains no combined-values arithmetic, unlike
its own sibling `balhigh_raise_$M4` (`rule_of_26`-gated). One shown limit raise
plus a 13-count is 23-25, and that is a partscore.

```yaml
# in context general_balancing_high, beside balhigh_rebid_H4
      - id: balhigh_rebid_hold_$M
        call: P
        priority: 29.5
        when: { i_have_acted: true, we_bid_last: false, partner_limited: true }
        requires:
          evals: { rule_of_26: [0, 24] }
        shows: "partner's raise was limited and the combined count is short of game: no fourth bid on the same values"
        establishes: { forcing: sign_off }
```

**Caveat, stated rather than buried:** `partner_limited` is the `when` key that
round 17's item 5 diagnosed as raising `NameError` (`eval_ctx` vs `ctx` in the
evaluator). **This rung cannot ship until that one-line fix lands**, and it
would be the first rule in the file to use the key. If the fix is not in scope,
drop `partner_limited` and keep `i_have_acted: true, we_bid_last: false`; the
`rule_of_26` ceiling then carries the whole gate.

**Answering seat.** A pass ends the auction; none owed.

**Endangers:** `balhigh_rebid_$M4` (29), `balhigh_nt3` (29) and
`balhigh_new_*4` (28) — all of which bid a fourth time on values partner has
already been told about; it stays below `balhigh_raise_*4` (32), which is
raising PARTNER and is a different hand, and below `balhigh_reopen_X` (41).
Note the direction of the trade: this rung SUBTRACTS four-level contracts from
a population that also contains makeable games, so it wants measuring alone.

**UNTESTED**, and flagged as blocked on the `partner_limited` repair.

**Template:** `expand: { M: [H, S] }`.

---

## Board 0 — W, call 3 (`(2D) P P ?` with `K83.KJ98742.6.KT`)

**Competitive** (a balancing action over a weak two). The constructive
observation is a priority inversion of the same species as board 758:
`ballow_X` (fit 1.000, prio 40), `ballow_new_H2` (1.000, 26) and
`ballow_new_long2_H` (1.000, 26) all fit, and the takeout double outranks a
natural SEVEN-card heart suit by fourteen points of priority. Partner then bids
2NT and we play a 4-3 notrump with a running major.

```yaml
# in context general_balancing_low, beside ballow_new_long2_H
      - id: ballow_own_suit_first_$M
        call: 2$M
        priority: 41.5
        when: { unbid_suit: $M, cheapest_in_suit: true }
        requires:
          suits: { $M: [6, 13] }
          evals: { total_points: [8, 16], "suit_quality($M)": [2.0, 9] }
        shows: "a good six-card $M in the balancing seat: bidding my own suit rather than asking for partner's"
        establishes: { forcing: non_forcing }
```
`expand: { M: [H, S] }`.

**Answering seat.** Non-forcing; `advance_*` and
`general_uncontested_continuation` already answer a natural two-level overcall.

**Endangers:** `ballow_X` (40) — with six or seven good hearts, a double that
asks partner to pick a suit is a worse description than naming it;
`ballow_nt2_balance` (33); `ballow_new_H2` / `ballow_new_long2_H` (26), which it
supersedes on the hands it claims; `ballow_pass` (21). It stays below nothing
in this context that describes a stronger hand — 41.5 is the top of the ladder,
which is why the six-card and suit-quality gates are both required.

**UNTESTED.**

**Template:** `expand: { M: [H, S] }`; a `expand: { M: [C, D, H, S] }` variant
at 41.0 for the minors is defensible but weaker (a minor partscore is worth
less than partner's best major).

---

## Board 55 — E, call 6 (`1S - P - 1NT - P - ?` with `AKT972.6.T.AKT42`)

**Went wrong:** E bid 4S (`ob_1M1NT_4S`, "too strong to invite", fit 1.000,
prio 57) with a **6-5** hand and 14 HCP, burying a nine-card club fit. We went
down one in 4S for +50 to them; the club partscore is cold for eleven tricks.

**Missing agreement.** `ob_1M1NT_2C` and `ob_1M1NT_2D` both carry
`not: { suits: { $M: [6, 13] } }`, so **opener may never show a second suit
once he holds six of his major** — every 6-4 and 6-5 hand in the file is
forced to choose between repeating the major and jumping. That is the single
most common two-suited shape in the game and it has no rung.

```yaml
  - id: opener_rebid_1M_1NT_two_suited
    description: "Opener's 6-4 / 6-5 second suit over the (semi-)forcing 1NT"
    expand_pairs:
      - { M: H, m: C }
      - { M: H, m: D }
      - { M: S, m: C }
      - { M: S, m: D }
    pattern: "1$M - P - 1NT - P - ?"
    rules:
      # 6-5: the second suit is bid whatever the strength - a 6-5 hand that
      # jumps to game has told partner about eleven of his thirteen cards
      # and asked him about none of his.
      - id: ob_1M1NT_65_$M$m
        call: 2$m
        priority: 57.5
        requires:
          suits: { $M: [6, 13], $m: [5, 13] }
          hcp: [12, 21]
        shows: "6-5: six $M and five $m, showing both suits before choosing a level"
        establishes: { forcing: non_forcing }
      # 6-4: below the invitational jump rebid, above the simple repeat.
      - id: ob_1M1NT_64_$M$m
        call: 2$m
        priority: 55.5
        requires:
          suits: { $M: [6, 13], $m: [4, 4] }
          hcp: [12, 17]
          evals: { total_points: [12, 19] }
        shows: "6-4: six $M and a four-card $m, offering the second suit at the two level"
        establishes: { forcing: non_forcing }
```

**Answering seat — already authored, and I checked it.**
`responder_preference_after_1M_1NT_2m` owns `1$M - P - 1NT - P - 2$x - P - ?`
with `pref_pass` (4+ in the second suit, 6-9), `pref_2$M` (preference on a
doubleton, 6-9), `pref_2NT` and `pref_3M_limit`. VERIFIED: on this deal W's
`.Q7532.QJ94.Q765` gives `pref_pass` fit **1.000** and we play 2C, which makes
eleven tricks — a ~200-point swing on the board.

**Endangers**, in `opener_rebid_1M_1NT`: `ob_1M1NT_4$M` (57) — a 6-5 hand must
describe itself before committing to a strain; `ob_1M1NT_3$M` (56) — same
argument for the invitational jump; `ob_1M1NT_pass` (55, `balanced: true`, no
overlap); `ob_1M1NT_2$M` (54) — with a four-card side suit, repeating six is
the less informative of two available descriptions; `ob_1M1NT_2C`/`2D` (52/53),
which this rung exists to reach at all. It does NOT touch
`ob_1S1NT_2H` (53.5), a different call. Because `ob_1M1NT_2C`/`2D` already
define the call 2C/2D in this seat, **no code fallback is deleted** by adding
these rungs — the round-15 hazard does not apply here.

**VERIFIED** — the diagnosis and the answering seat both traced; the new rungs
themselves are UNTESTED as YAML.

**Template:** the `expand_pairs` above (both majors × both minors). Do **not**
fold `m` into the existing context's `expand:` — that would duplicate every
existing rule id across two same-pattern context instances; a separate context
is how `opener_rebid_1S_1NT_second_major` already solves the same problem.

---

## Board 83 — W, call 4 (`1S - P - 1NT - P - ?` with `AJ6532.3.A3.KJ76`)

**Same agreement as board 55** — a 6-4 hand (six spades, four clubs, 13 HCP)
with no way to show the second suit, so `ob_1M1NT_2S` takes it at fit 1.000.
The `ob_1M1NT_64_$M$m` rung above covers it exactly.

**Honest negative, reported rather than shipped.** I traced the continuation:
after `1S - 1NT - 2C`, responder's `QT.J962.J9.AT542` gives `pref_2S` fit
**1.000** at priority 55 and `pref_pass` fit **1.000** at 52, so the engine
takes the preference and we play 2S — the same contract we already reach. **The
agreement does not flip this board.** The nine-card club fit is only findable
if the preference ladder also learns that five cards in opener's second suit
outrank a doubleton in his first, and I checked that too: making
`pref_pass` outrank `pref_2S` on five-card length lands in 2C making twelve
(+170) against the 2S making eleven (+200) we already score, i.e. it is worse.
Board 83 is a deal where 4S makes eleven tricks on 21 HCP and no constructive
auction finds it. **Proposal stands on board 55's evidence, not this one.**

**VERIFIED** (both the diagnosis and the negative).

---

## Board 93 — E, call 0 (opening `KT98.T543.A.A765`, 11 HCP)

**NOTHING-WRONG.** The divergence is whether to open a flat 4-4-1-4 eleven-count
in first seat; `open_1C` fits 0.800 against a 12 HCP floor and `open_pass` fits
1.000. That is an **opening-style / rule-of-20 threshold**, explicitly on the
do-not-re-propose list in `EXPERT_BRIEF_R18.md` and in `DECISIONS.md`.

Checked, so it is not an omission: the rest of our auction (pass, pass, pass) is
forced once we do not open, and neither table reaches a constructive decision
after that. There is no invitational, game-try or slam-machinery seat on this
board.

---

## Board 116 — N, call 0 (opening `95.K9843.AK954.T`, 10 HCP)

**NOTHING-WRONG.** `open_1H_rule20` fits 0.757 on a 10-count 5-5; the rule-of-20
threshold is scope-excluded. Checked downstream: our only other calls are
`oc1H_pass`, `sw_pass` and three `ch_pass`es against a 1H-1S-3S-4S auction we
have no values to enter. No constructive seat exists for us on this deal.

---

## Board 132 — E, call 8 (`1D - P - 1H - P - 2C - P - 3H - P - ?` with `98.6.AQJT7.AJ983`)

**Went wrong:** opener PASSED responder's `r1d1h2c_3H`, an
`establishes: { forcing: invitational }` call, with a fitting 12-count. 4H makes
twelve tricks.

**Missing agreement — the headline of this slice.** Responder's jump rebid of
his own six-card suit over opener's second suit is an invitation, and **no
context in the file answers it.** VERIFIED: at that seat `context_at` returns
`['general_uncontested_continuation', 'general_slam_try']` and the candidate
list is `uc_pass` fit **1.000** prio 18, then `uc_rebid_C4`/`uc_rebid_D4` at
0.349. The invitation is passed out by construction — the round-17 empty-seat
mechanism, one level lower down.

Two rungs, and they are one fix:

```yaml
  # (a) the seat that ANSWERS the invitation
  - id: opener_over_responder_jump_rebid
    description: "Opener over responder's invitational jump rebid of his own suit"
    expand_pairs:
      - { o: D, R: 1H, B: 2C, M: H }
      - { o: D, R: 1S, B: 2C, M: S }
      - { o: C, R: 1H, B: 2D, M: H }
      - { o: C, R: 1S, B: 2D, M: S }
      - { o: H, R: 1S, B: 2C, M: S }
      - { o: H, R: 1S, B: 2D, M: S }
    pattern: "1$o - P - $R - P - $B - P - 3$M - P - ?"
    rules:
      - id: orjr_pass_$o$M
        call: P
        priority: 50
        requires: {}
        shows: "declining the invitation: a dead minimum with no fit"
        establishes: { forcing: sign_off }
        negative_inference_weight: soft
      - id: orjr_game_$o$M
        call: 4$M
        priority: 54
        requires:
          any_of:
            - suits: { $M: [2, 13] }
              evals: { total_points: [14, 40] }
            - suits: { $M: [3, 13] }
              evals: { total_points: [12, 40] }
        shows: "accepting: a doubleton and extras, or three-card support and any opening"
        establishes: { forcing: sign_off, agreed_suit: $M }
      - id: orjr_3NT_$o$M
        call: 3NT
        priority: 52
        requires:
          suits: { $M: [0, 1] }
          evals: { total_points: [14, 40], semi_balanced: [1, 1] }
        shows: "no fit for the long suit but the values for game: offering notrump"
        establishes: { forcing: sign_off }
```

```yaml
  # (b) the tier that means 14+ never has to invite at all - in
  #     responder_rebid_1D_1H_2C, responder_after_1D1S_2C and their siblings
      - id: r1d1h2c_4H
        call: 4H
        priority: 60
        requires:
          suits: { H: [6, 13] }
          evals: { total_points: [14, 40] }
        shows: "6+ hearts and game values: bidding the game rather than inviting it"
        establishes: { forcing: sign_off, agreed_suit: H }
```
(and `r1d2c_4S` identically in `responder_after_1D1S_2C`, priority 60, suits
`S: [6, 13]`.)

**THE ANSWERING SEAT** is (a); it is not optional and it is the whole point of
the proposal. The `requires: {}` pass is the round-6 sign-off floor, so the seat
can never be starved.

**Endangers.** In the new context, nothing exists to endanger — it is virgin
seat. What it takes from `general_uncontested_continuation` is `uc_pass` (18),
`uc_rebid_C4`/`uc_rebid_D4` (29) and `uc_raise_H4` (32): passing a live
invitation is not "nothing further to show", and inventing a fourth suit at the
four level is worse than answering the question asked. **Because the new
context DEFINES P, 3NT and 4$M in this seat, it deletes the code fallback for
those three calls there** — the `requires: {}` pass is what makes that safe.
In (b), `r1d1h2c_4H` at 60 outranks `r1d1h2c_3H` (59): with 14+ playing points
and a six-card suit, bidding the game is a better description than asking a
question whose answer you already know. It leaves `r1d1h2c_3NT` (57),
`r1d1h2c_2NT` (56) and `r1d1h2c_2H` (55) untouched — none of them describes a
six-card major with game values.

**VERIFIED** — `ask()` at that seat returns `P`, decided by `uc_pass` at fit
1.000; `rank()` output quoted above.

**Template:** the `expand_pairs` list covers every "1m - 1M - 2x" and
"1H - 1S - 2x" shape in which responder can jump-rebid below game. Add
`{ o: H, R: 1S, B: 2C, M: S }` and `{ o: H, R: 1S, B: 2D, M: S }` only after
`responder_rebid_1H_1S_2C`/`2D` gain the 3S jump rebid they currently lack —
today those two contexts have no such rung at all, which is a separate hole in
the same family.

---

## Board 188 — N, call 4 (`1H (2D) 2H P ?` with `.AQ843.K92.KQJ83`)

**Went wrong:** N blasted 4H (`uc_raise_H4`, fit 1.000, prio 32) opposite a
6-9 competitive raise, holding 0-5-3-5 with a spade void. 4H makes nine.

**Missing agreement — this is the mandate board.** *Trial bids / help-suit game
tries: 0 rules.* Opposite a single raise the file's only invitation is
`op_after_raise_inv` — 3M on 17-18 total points — which cannot say **where**
the help is needed, so a 5-5 hand with a void has to choose between a blind
game and a blind invitation. Here 3C names the second suit and asks the one
question that decides the hand.

The closed conversation, both halves:

```yaml
  # (a) opener's help-suit try, in responder_rebid_after_1M_raise
  #     (pattern "1$M - P - 2$M - P - ?")
      - id: op_trial_$M$x
        call: 3$x
        priority: 53
        requires:
          suits: { $M: [5, 13], $x: [3, 13] }
          evals:
            total_points: [15, 18]
            "suit_quality($x)": [0, 2.0]
        shows: "help-suit game try: 15-18 with $M agreed and losers in $x - three small or Qxx opposite is the difference"
        establishes: { forcing: invitational, agreed_suit: $M }
        alertable: true
```
```yaml
  # (b) THE ANSWERING SEAT - it does not exist today
  - id: responder_over_help_suit_try
    description: "Responder answers opener's help-suit game try"
    expand_pairs:
      - { M: H, x: C }
      - { M: H, x: D }
      - { M: S, x: C }
      - { M: S, x: D }
      - { M: S, x: H }
    pattern: "1$M - P - 2$M - P - 3$x - P - ?"
    rules:
      - id: rhst_decline_$M$x
        call: 3$M
        priority: 50
        requires: {}
        shows: "no help in $x: signing off in the agreed major"
        establishes: { forcing: sign_off, agreed_suit: $M }
        negative_inference_weight: soft
      - id: rhst_accept_$M$x
        call: 4$M
        priority: 55
        requires:
          any_of:
            - suits: { $x: [0, 1] }
              evals: { total_points: [7, 40] }
            - suits: { $x: [3, 13] }
              features: [ "top_honour($x)" ]
              evals: { total_points: [7, 40] }
        shows: "help where it was asked for - shortness, or an honour in $x - and a maximum raise"
        establishes: { forcing: sign_off, agreed_suit: $M }
      - id: rhst_cue_$M$x
        call: 4$x
        priority: 56
        requires:
          suits: { $x: [3, 13] }
          features: [ "control_in($x)" ]
          evals: { total_points: [9, 40], controls: [3, 12] }
        shows: "maximum with the ace of $x: accepting and showing the control below game"
        establishes: { forcing: game_forcing, agreed_suit: $M }
```
Rung (b3) is the piece round 17 says is missing everywhere: a **control shown
below game**, in an auction that is still at the three level. Opener's reply to
it is `general_slam_try` / `rkc_ask`, which already exist.

**Endangers.** (a) outranks `op_after_raise_inv` (52) — naming the suit is
strictly more informative than a general try on the same values — and
`op_after_raise_pass` (50); it stays BELOW `op_after_raise_game` (54), so 19+
still bids game directly. (b) is virgin seat; it takes 3$M and 4$M from
`general_uncontested_continuation`'s `uc_raise_$M3` (31) and `uc_raise_$M4`
(32), which price the hand without knowing a question was asked, and it deletes
the code fallback for 3$M / 4$M / 4$x in that seat — the `requires: {}`
sign-off is what makes that safe.

**Honest caveat about THIS board.** Board 188's own seat is `1H (2D) 2H P` — a
competitive auction routed to `general_uncontested_continuation` because RHO
passed — so the pure `1$M - P - 2$M - P - ?` context above does not reach it.
Porting the try under `when: { is_competitive: true }` is the
`uc_raise_lott4_$M` pattern (the one port that measured +12), and I recommend
it as a second rung `uc_trial_$M$x` at priority 32.5; I do **not** recommend
the round-12 wholesale reroute, which measured -106. I also checked the deal:
S holds `K964.J92.43.AT64`, so a 3C try is ACCEPTED (the club ace is exactly the
help asked for) and we still reach 4H. **The agreement is right and this board
still loses** — reported as a negative rather than shipped as a fix.

**UNTESTED** as YAML; the diagnosis and the acceptance trace are VERIFIED.

**Template:** the five `expand_pairs` above — every trial suit that is below
three of the agreed major. `3$oM` over 1H-2H is impossible (3S outranks 3H) and
is correctly absent.

---

## Board 191 — S, call 3 (`(1D) P (1S) ?` with `Q.T8432.A2.AKQT8`)

**Competitive** (the sandwich seat). Constructive observation: `sw_X` (fit
1.000, prio 70) outranks `sw_2C` (fit 1.000, prio 66), so a takeout double of
BOTH their suits is preferred to naming a self-sufficient AKQT8 with a stiff
queen in one of their suits. Partner then bids the suit we do not have.

```yaml
# in context sandwich_seat, beside sw_2C
      - id: sw_own_suit_$v
        call: 2$v
        priority: 70.5
        when: { unbid_suit: $v, cheapest_in_suit: true }
        requires:
          suits: { $v: [5, 13] }
          evals: { total_points: [11, 17], "suit_quality($v)": [3.0, 9] }
          not: { evals: { "suit_length(H)": [4, 13] } }
        shows: "sandwich overcall on a suit that plays opposite a void: five cards, three of the top five"
        establishes: { forcing: non_forcing }
```
(The `not:` clause is the honest half — a takeout double is still right when the
unbid major is four long; drop it and this rung would eat every sandwich
double.)

**Answering seat.** `advance_overcall` (`1$o - 1$v - P - ?`) already owns the
seat that answers a two-level sandwich overcall.

**Endangers:** `sw_X` (70) on exactly the hands where the suit is solid and the
unbid major is not held; `sw_2C`/`sw_2D`/`sw_2H`/`sw_2S` (66), which it
supersedes; `sw_pass` (30). It leaves `sw_3x` (69.5, the preemptive jump) alone.

**UNTESTED.**

**Template:** `expand: { v: [C, D, H, S] }` inside `sandwich_seat`.

---

## Board 247 — N, call 5 (`P 1D (2S) X P ?` with `9.T52.KJT86.AQJ5`)

**NOTHING-WRONG.** Checked: partner's `nxj_X` promised the unbid major, we hold
`T52` in it, so `adx_neg_major_H3` correctly fits only 0.349; `adx_nt` fits
0.000 for want of a spade stopper; `adx_pull_my_D` at fit 1.000 is a normal
minimum rebid of a five-card suit that partner's double invited. BEN's 3C
(0.81) is a style choice between two four-plus minors, not an agreement the
file lacks — and the -6 came from 3D going one down, not from the auction.

The one constructive item I would note without proposing it: this context has
no rung for the **5-4 minor two-suiter** (3C after opening 1D), and if it ever
gets one it must sit below `adx_neg_major_$M3` (62), not above.

---

## Board 267 — N, call 9 (`1NT - P - 2D - P - 2H - P - ?` with `Q972.QT987.K2.53`)

**Went wrong:** N passed the completed transfer (`tr_pass_weak`, fit 1.000,
prio 55) holding **five hearts AND four spades**. Opener has three hearts and
a 16-count; 4H makes ten tricks and we played 2H.

**Missing agreement.** `nt_after_transfer` has no second-suit rung at all — a
documented open item — so every 5-4 hand after a transfer must choose between
a weak pass, a notrump invitation that denies the second suit, and a jump in the
five-card suit. The 5-4 hand is the commonest shape opposite a 1NT opening and
it has nothing to say.

```yaml
# in context nt_after_transfer  (expand_pairs [{M:H,T:D},{M:S,T:H}])
      - id: tr_second_$oM
        call: 2$oM
        priority: 57.5
        requires:
          suits: { $M: [5, 13], $oM: [4, 13] }
          hcp: [7, 10]
        shows: "five $M and four $oM, invitational values: opener passes, corrects, or bids game"
        establishes: { forcing: invitational }
        alertable: true
```
(For M=H the call is 2S, a live invitation below game. For M=S the call would be
3H, so the S half wants priority 57.5 too but with `hcp: [8, 10]` — a level
higher costs a point.)

**THE ANSWERING SEAT — new, and it ships here.**

```yaml
  - id: nt_opener_over_second_suit
    description: "Opener over responder's 5-4 second suit after a completed transfer"
    expand_pairs: [ { M: H, T: D, N: S }, { M: S, T: H, N: H } ]
    pattern: "1NT - P - 2$T - P - 2$M - P - 2$N - P - ?"
    rules:
      - id: ntoss_pass_$M
        call: P
        priority: 50
        requires: {}
        shows: "minimum with length in the second suit: leaving it there"
        establishes: { forcing: sign_off }
        negative_inference_weight: soft
      - id: ntoss_3$M
        call: 3$M
        priority: 54
        requires: { suits: { $M: [3, 13] }, hcp: [15, 15] }
        shows: "three-card fit for the first suit, minimum: back to the major at the three level"
        establishes: { forcing: invitational, agreed_suit: $M }
      - id: ntoss_4$M
        call: 4$M
        priority: 56
        requires: { suits: { $M: [3, 13] }, hcp: [16, 17] }
        shows: "three-card fit and a maximum: game in the five-card major"
        establishes: { forcing: sign_off, agreed_suit: $M }
      - id: ntoss_4$N
        call: 4$N
        priority: 55
        requires: { suits: { $N: [4, 13], $M: [0, 2] }, hcp: [16, 17] }
        shows: "four-card fit for the second suit and a maximum: game there instead"
        establishes: { forcing: sign_off, agreed_suit: $N }
      - id: ntoss_3NT
        call: 3NT
        priority: 53
        requires: { suits: { $M: [0, 2], $N: [0, 3] }, hcp: [16, 17] }
        shows: "maximum, no fit for either major: notrump game"
        establishes: { forcing: sign_off }
```

**Endangers.** In `nt_after_transfer`: `tr_pass_weak` (55) — a 5-4 seven-count
opposite 15-17 is not a sign-off, it is a hand with a second chance;
`tr_2NT_inv` (56) — that rung requires `$M: [5, 5]` and says nothing about the
other major, so it describes the same hand worse; it stays below
`tr_3NT_choice` (58), `tr_game_void_$M` (58.5) and `tr_4$M` (59), all of which
are game-going. The new CONTEXT (pattern of 8 tokens, specificity 1008) takes
P / 3$M / 4$M / 4$N / 3NT in that seat away from
`general_uncontested_continuation`; the `requires: {}` pass keeps it a superset
for the sign-off.

**VERIFIED, both ends.** `rank()` reproduces `tr_pass_weak` at 1.000; and I
traced the seat after a hypothetical 2S — today `context_at` returns only
`general_uncontested_continuation`, where `uc_raise_H4` and `uc_raise_S4` BOTH
fit 1.000 at priority 32 and the cheaper call wins the tie. On this deal that
happens to be 4H (the winning contract, +420), but it is a coin flip decided by
call order, not by an agreement — which is exactly why the answering context
must ship with the invitation.

**Template:** the two `expand_pairs` above.

---

## Board 272 — N, call 0 (opening `T4.AQ852.JT6.A87`, 11 HCP)

**NOTHING-WRONG.** `open_1H` fits 0.800 against a 12 HCP floor; opening a
5-3-3-2 eleven-count is an opening-style threshold and is scope-excluded.
Checked the rest of our auction: `oc1D_1H` and `xd_jumpraise_H3` are both
competitive calls after we did not open, and there is no invitational or
game-try seat for us on the deal.

---

## Board 274 — S, call 0 (opening `J53..Q9874.AKT65`, 10 HCP)

**NOTHING-WRONG.** `open_1m_rule20` fits 1.000 and chose 1D on a 3-0-5-5
ten-count — the rule-of-20 threshold, scope-excluded, and BEN's pass is the
minority view. The constructive observation I would record: with 5-5 and a
void, `open_1D` vs `open_1C` matters more than whether to open at all, and the
file opens the HIGHER minor here, which leaves 2C available as a natural rebid
— that is right and I would not change it.

---

## Board 297 — N, call 3 (`(1C) 1D (1S) ?` with `J5.AQJ6.Q853.654`)

**Went wrong:** N doubled (`cl_negative_X1`, fit 1.000, prio 33) holding
**four-card support for partner's overcall**. `cl_raise_D2` fits 1.000 at
priority 30 and loses the tie by three points.

**Missing agreement.** The generic double rung is called `cl_negative_X1` and
its `shows` says "negative double" — a call that presupposes our side OPENED.
In this seat partner OVERCALLED, so the same 10-count with four diamonds and
four hearts should raise: a fit is a fact, the other major is a hope.

```yaml
# in context general_competitive_low, beside cl_raise_D2
      - id: cl_raise_advance_$M
        call: 2$M
        priority: 33.5
        when: { partner_suit: $M, cheapest_in_suit: true, i_have_acted: false }
        requires:
          suits: { $M: [4, 13] }
          evals: { total_points: [8, 11], "lott_total_trumps($M)": [8, 26] }
        shows: "raising partner with four-card support: a known eight-card fit outranks a double promising a suit I may never play"
        establishes: { forcing: non_forcing, agreed_suit: $M }
```
`expand: { M: [C, D, H, S] }`.

This is **not** the scope-excluded "non-forcing responsive double" — it is the
opposite change, moving the natural raise above the double rather than
redefining the double.

**Answering seat.** Non-forcing; partner's continuation is
`general_competitive_high` / `general_balancing_*`, already authored.

**Endangers:** `cl_negative_X1`/`cl_negative_X2` (33) on exactly the hands with
four-card support and 8-11 — that is the intended trade and it is one sentence
of bridge; `cl_raise_$M2` (30) which it supersedes; `cl_nt1` (27), `cl_nt2`
(28), `cl_new_*` (26/26.5), `cl_pass` (20). It stays below `cl_takeout_X` (36)
and `cl_nt2_direct` (37), which describe stronger hands.

**VERIFIED** for the diagnosis (dossier candidate table reproduced); the rung is
UNTESTED.

**Template:** `expand: { M: [C, D, H, S] }`.

---

## Board 343 — S, call 3 (`(1C) P (1H) ?` with `AQ5.AT6.J76.KT87`)

**NOTHING-WRONG.** A 3-3-3-4 fourteen-count between two bidding opponents with
no five-card suit and no shortness: `sw_pass` at 0.800 is the best fit in the
context and `sw_X` at 0.349 correctly fails the shortness test. BEN's double
carries only 0.50 confidence. Checked the downstream seats too — every later
call of ours on this board is a forced pass over their 1S-3S auction. There is
no constructive seat here.

---

## Board 348 — S, call 2 (`1D - P - ?` with `QJ.AQ4.K542.T976`)

**Went wrong:** S bid 2C (`r1D_2C_gf`, "2/1 game forcing", fit 1.000, prio 70-71)
on a **flat twelve-count with two honour-doubletons and no source of tricks**.
We then bid 2NT-3D-5D and went down; the field plays 2NT.

**Missing agreement — the invitational/game-force boundary.** `r1m_2NT`
("invitational: 11-12 balanced, no 4-card major") fits this hand at **1.000**;
it loses purely on priority, 54 against 70. In 2/1 Game Forcing the two-over-one
promises game values, and a 4-3-3-2/4-4-3-2 twelve-count with QJ tight is the
canonical hand that must invite instead.

```yaml
# in contexts resp_1m and resp_1D_2C_gf (one rung, sited in resp_1m)
      - id: r1m_2NT_flat
        call: 2NT
        priority: 72
        requires:
          hcp: [11, 12]
          balanced: true
          evals: { longest_suit_length: [0, 4], singleton_or_void: [0, 0] }
          not: { any_of: [ { suits: { H: [4, 13] } }, { suits: { S: [4, 13] } } ] }
        shows: "invitational 11-12 balanced with no five-card suit: too flat for a game force"
        establishes: { forcing: invitational }
```

**THE ANSWERING SEAT — already authored, and I traced it.**
`opener_over_2NT_response` (`1$m - P - 2NT - P - ?`) has `o2nresp_pass_$m`
(0-12), `o2nresp_3NT_$m` (13-17) and `o2nresp_quant_$m` (18-21). VERIFIED: with
N's `974.JT.AT98.AK54` the engine passes at fit **1.000** and we play 2NT — the
exact +150 the other table scored. **This board flips.**

**Endangers**, in `resp_1m` / `resp_1D_2C_gf`: `r1D_2C_gf` (71) and
`r1m_2over1` / `r1D_2C_gf3` (70) — a flat 12 with no five-card suit is an
invitation, not a game force, and that is the whole content of the rung; it is
placed BELOW `r1m_1H` (76) and `r1m_1S` (77), so a four-card major is still bid
first (and the `not:` clause makes the point explicit); it supersedes
`r1m_2NT` (54) on the hands it claims and leaves `r1m_3NT` (55, 13-15),
`r1m_raise3` (52, five-card support) and `r1m_1NT` (45, 6-10) alone. The
`longest_suit_length <= 4` clause is the load-bearing one: a 12-count with a
five-card minor still has a source of tricks and still bids the two-over-one.

**VERIFIED end to end.**

**Template:** `expand: { m: [C, D] }` is already on `resp_1m`, so the rung is
written once and covers both minors. The major analogue is board 782 below.

---
