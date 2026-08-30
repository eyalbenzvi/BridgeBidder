# Expert B — constructive / team-IMP review of dossier part 01 (38 boards, -471 IMPs)

Reviewer B: uncontested constructive auctions — the 2/1 machinery, opener's and
responder's rebid ladders, the invitational/game boundary, and the shape- and
control-showing that separates a minimum from a slam-going hand **below game**.

## Summary

| | |
|---|---|
| boards in dossier | 38 |
| proposals with exact YAML | **20** |
| of those, traced through `repro`-equivalent ranking on a patched copy of the file | **18 VERIFIED** |
| proposals that recover the board's IMPs in a full engine-vs-engine rollout | **13** |
| NEGATIVE results reported rather than shipped | **3** (boards 222-alt, 443, 762) |
| NOTHING-WRONG / competitive (reviewer A's territory) | **18** |

**Method note — how "VERIFIED" was obtained.** `choose_bid` accepts a
`system_path`, so every proposal below was written into a *copy* of
`two_over_one.yaml` in scratch, loaded, ranked with `score_candidates`, and
where useful the whole auction was rolled out with the engine in both of our
seats. The repo file was never touched. Two traps were hit and are worth
recording: (1) `choose_bid` defaults to `use_arbitration=True` while
`match_ben` uses `decide_fast`, so a verification harness **must** pass
`use_arbitration: False` or it will report a call the match would never make —
this cost me one wrong reading on board 426; (2) `fast_decision` breaks ties by
`(priority, fit)` among candidates fitting >= 0.9, so two new rungs at the same
priority producing different calls make the decision `is_clear=False` and hand
it to arbitration. Give sibling rungs distinct priorities.

**Do not use `when: { partner_limited: ... }` in any of this.** Round 17 item 5
records that `partner_limited` reads `eval_ctx` where the parameter is named
`ctx`; the first YAML rule to use it raises `NameError`. Several of the
agreements below would be cleaner with it and are written without it.

## The three agreements that matter most in this slice

1. **The help-suit game try does not exist and its answering seat does not
   exist** (board 426, and the whole `1M - 2M` family). `responder_rebid_after_1M_raise`
   has exactly three rungs — pass / 3M / 4M — and the auction
   `1m - 1H - 1S - 2S` has *no context at all*, so opener's game try is decided
   by the generic `uc_raise_S3` at fit 0.946 (13 tables, mean **-1.85**).
   Proposal 426 ships the trial bid **and** the accept/decline seat, and is the
   single most templatable idea in this part.

2. **Every splinter in the file is responder's; opener has none, responder over
   opener's second suit has none, and Stayman has none** (boards 443, 318, 105,
   559). Four separate seats where a 19+ hand with shortness has only a blind
   jump to game. Three of the four recover their board in full when the
   splinter *and* its answering seat are shipped together; the fourth (443)
   correctly declines and is reported as a negative.

3. **A quantitative sequence whose accept rung is keyed to the wrong hand.**
   `qa_pass` fires on 6 tables at mean **-5.50** and `qa_6NT` needs 16 HCP — a
   floor that is right opposite a 15-17 notrump and absurd opposite a 22+ 2C
   opener (board 437), and there is no accept context at all after
   `1m - 2m - 2NT` (board 479). Both seats are starved, both are pure
   arithmetic, and both recover their board.

**A fourth, worth saying because it is a fact about the file rather than a
judgement:** `rrevd_3NT` — game opposite a reverse — **never fires in 1000
boards**, because its floor is 12 HCP when a reverse shows 17+. The generic
`uc_raise_D3` annexes that seat instead, at 14 tables and mean **-3.86**, and
on board 967 it agreed diamonds and launched a keycard ask into a 6D that went
down. A ladder whose rungs are banded against the wrong partner range is
indistinguishable from no ladder.

---

## Board 173 — margin -15

**Seat/call:** table A call 1, S bids 3C over 1S (`oc1S_3m_jump`); then N's 4C
(`awj_4_SC`) over the weak jump. **Purely competitive** — the whole board is a
weak jump overcall and its advance. Reviewer A's territory.

What I checked: `oc1S_3m_jump` fits 1.000 on `9.KT42.74.KQJT32` and DECISIONS
already records (round 11) that re-ranking the weak jump overcall measured
**-24 held out**; that is on the do-not-re-propose list and I am not touching it.

**Best constructive-discipline observation.** `advance_weak_jump_overcall`
(`1$o - 3$j - P - ?`) carries **three** rules. N holds `J.AQ953.KJ52.A54` — 15
HCP, a five-card major, a fit for the jump — and the only descriptive call
available is a raise. This is the *advancer's* version of the trial-bid hole:
after a preemptive jump, advancer needs a **fit-showing / game-try** rung (a new
suit at the three level = a real suit plus a fit, forcing one round) and the
seat that answers it. I have not authored it here because the board is
competitive and any rung in that context prices against the preemptor's
discipline, which is A's call.

**VERDICT: NOTHING-WRONG (competitive).**

---

## Board 439 — margin -15

**Seat/call:** table A call 1, N passes 1NT holding `T9743.5.Q8.AKQ53`
(`v1NT_pass`, fit 1.000). **Purely competitive** — defence to their 1NT, which
DECISIONS scopes as "natural, chosen over DONT/Cappelletti for explainability".

What I checked: the whole candidate set. `v1NT_2S` needs 5+ spades and 8-15 and
fits 0.200 (it is gated on a *usually six* reading); `v1NT_2C` fits 0.349. Both
soft-miss and the catch-all pass at 1.000 wins. The seat is starved, not
mis-ruled.

**Best constructive-discipline observation.** The two-suiter is the hand type
the file's own DECISIONS entry says it declined to author ("no Michaels or
unusual NT"), and the same gap shows here in the defence to 1NT: with 5-5 there
is no call. That is a convention-card decision, not a rung.

**VERDICT: NOTHING-WRONG (competitive; scope-excluded convention).**

---

## Board 951 — margin -15

**Seat/call:** table A call 5, N passes over `P 1D X XX 1H` (`rdc_pass_D`,
"forcing pass: partner's redouble owns the auction"). **Competitive.**

What I checked: `cl_nt1` and `cl_nt2` both fit 1.000 underneath it, so the seat
is not starved — the forcing pass simply outranks them at priority 50. BEN's 1NT
is a judgement call, not a missing agreement.

**Best constructive-discipline observation.** The redouble family
(`redouble_continuations`, 4 rules) has no **strength-showing** rung: after
`1m - X - XX`, our side owns the auction and the next constructive decision is
whether we are playing a partscore, a game or a penalty, and the only tool is a
forcing pass. A three-rung ladder (cheapest suit = to play, jump = a real suit
with values, 1NT = a stopper and 8-11) would give the pass a meaning by
contrast. Not authored: the family is competitive throughout.

**VERDICT: NOTHING-WRONG (competitive).**

---

## Board 305 — margin -14

**Seat/call:** table A call 3, N passes 5D over `3D P 5D` (`ch_pass`). The
whole board is a preempt and a raise to five. **Purely competitive.**

What I checked: `ch_pass` at fit 1.000 against `ch_penalty_X` at 0.047 — a
two-candidate seat. There is no constructive machinery in this auction at all.

**Best constructive-discipline observation.** `resp_preempt_D` has six rules and
none of them is a **control-showing raise**: over partner's 3D preempt the only
raises are by level, so a hand that wants to say "I have first-round control of
your short suits and enough tricks" cannot. That is the constructive half of the
preemptive family and it is at zero rules, the same as trial bids.

**VERDICT: NOTHING-WRONG (competitive).**

---

## Board 614 — margin -14

**Seat/call:** table B call 5, W rebids **2C** on `5..KQ6.AQJ986532` after
`1C - 1S` (`ob_rebid_2C`, fit 1.000). Eight clubs, **three losers**, and the
system's only jump rebid needs 16-18 HCP.

**The missing agreement (one sentence).** Opener's jump rebid of his own minor
should be reachable on *playing strength* — a seven-plus card suit with at most
five losers — not only on high-card points.

### YAML — into the existing context `opener_rebid_1m_1M`

```yaml
      - id: ob_rebid_shape3_$m
        call: 3$m
        priority: 51
        requires:
          suits: { $m: [7, 13] }
          hcp: [11, 15]
          evals: { ltc: [0, 5] }
          not: { suits: { $M: [4, 13] } }
        shows: "jump rebid on playing strength: a seven-card $m, at most five losers"
        establishes: { forcing: invitational }
```

**The answering seat.** `responder_after_jump_rebid` (`1$m - P - 1$M - P - 3$m - P - ?`)
already exists, but every rung in it is banded 10-16 / 14-15 / 16-21-and-
`semi_balanced`, so partner E (`AKT93.AK76.AJ3.7`, 19 HCP, 5-4-3-1) had **no
candidate above fit 0.349** — a pure soft-miss lottery. The trial bid is worth
nothing without this, so it ships in the same proposal:

```yaml
      - id: rjrb_3NT_strong
        call: 3NT
        priority: 58
        requires: { hcp: [17, 21], evals: { weakest_unshown_stopper: [0.9, 9] } }
        shows: "17+ opposite the jump rebid: the nine-trick game, slam still possible"
        establishes: { forcing: sign_off }
      - id: rjrb_5$m
        call: 5$m
        priority: 59
        requires: { suits: { $m: [3, 13] }, evals: { total_points: [17, 40] } }
        shows: "17+ with real support for the jumped minor: the eleven-trick game"
        establishes: { forcing: sign_off, agreed_suit: $m }
```

**What it endangers.**
* `ob_rebid_2$m` (prio 50) — a seven-card suit with three losers is not a
  "minimum rebid"; the six-card 12-15 hands it was written for miss the new
  rung's length gate and still fit 1.000 (traced: `5.732.KQ6.AQJ865` still bids 2C).
* `ob_rebid_3$m` (49) — different band (16-18 HCP with six cards); untouched.
* `ob_raise_2$M/3$M/4$M` (80/78/76) — all deny-gated by `not: {suits: {$M: [4,13]}}`.
* `ob_1NT` (57.5) / `ob_2NT` (56) — both need `semi_balanced` / `balanced`,
  which a 7+ suit cannot be.
* 3$m is already covered by `ob_rebid_3$m`, so **no code fallback is deleted**.
* `rjrb_3NT_strong` (58) outranks `rjrb_3NT` (55, 10-16) and `rjrb_3M` (55.5) —
  disjoint bands. `rjrb_5$m` (59) outranks both only with 3+ card support and
  17+, which no existing rung describes.
* Whole-corpus denominator before accusing: `ob_rebid_2C` fires on **12 tables,
  mean -2.17**; the rung takes a narrow shape slice out of it.

**VERIFIED.** Patched copy: W now bids 3C (fit 1.000, prio 51); E answers 3NT at
fit **1.000** instead of choosing among candidates whose best fit was 0.349.

**Honest negative on the IMPs.** The rolled-out auction becomes
`1C - 1S - 3C - 3NT` — the *same contract* as today (3NT by E, thirteen tricks),
so the board's -14 is **not recovered**. BEN reached 7NT; the file has **zero**
seven-level rules and the 5NT king ask is scope-excluded. My first draft shipped
the jump rebid *without* `rjrb_3NT_strong` and the auction ran to 4C for +190
instead of +520 — **strictly worse**. That is the density thesis in miniature:
the rebid is right bridge and is a measurable loss until the seat that answers
it can hold a 19-count.

**TEMPLATE.** Already `expand: { m: [C, D], M: [H, S] }` (4 rules) and
`expand: { m: [C, D], M: [H, S] }` on the answering context (8 rules). The same
"jump on losers, not on points" idea should be templated into
`opener_rebid_1M_1NT`, `or1mn_jump_$m` and `opener_rebid_after_2over1_minor`.

---

## Board 925 — margin -14

**Seat/call:** table A call 7, N passes their double of opener's Stayman answer
(`xd_pass`, "sitting for their double: no better spot to run to"). We played
**2D doubled, four tricks, -1100**.

This is a competitive interruption, but the seat it eats is a *constructive*
one: `1NT - P - 2C - P - 2D - X - ?` is the invitational decision after Stayman,
and the generic runout context annexes it. `xd_pass` fires on **88 tables at
mean -1.72**, so it is not a bad rule — it is a catch-all standing where a
ladder should be.

**The missing agreement.** Their double of opener's Stayman answer does not
change responder's hand: the ladder is redouble with values, 2NT invitational,
3NT to play, and pass only as a floor.

### YAML — two new contexts (append at file end)

```yaml
  - id: stayman_answer_doubled_2D
    description: "Responder after their double of opener's 2D answer to Stayman"
    pattern: "1NT - P - 2C - P - 2D - X - ?"
    rules:
      - id: sad2d_XX
        call: XX
        priority: 60
        requires: { hcp: [10, 40] }
        shows: "redouble: our hands own this and their double was a mistake"
        establishes: { forcing: one_round }
      - id: sad2d_3NT
        call: 3NT
        priority: 58
        requires: { hcp: [10, 17] }
        shows: "game opposite the 15-17 notrump: their double changes nothing"
        establishes: { forcing: sign_off }
      - id: sad2d_2NT
        call: 2NT
        priority: 57
        requires: { hcp: [8, 9] }
        shows: "invitational: 8-9 opposite 15-17, their double changes nothing"
        establishes: { forcing: invitational }
      - id: sad2d_pass
        call: P
        priority: 30
        requires: {}
        shows: "no better description: sitting for the double"
        establishes: { forcing: non_forcing }
        negative_inference_weight: soft
```

**THE ANSWERING SEAT** (the 2NT is an invitation, so it ships here):

```yaml
  - id: stayman_invite_accept_2D_doubled
    description: "Opener over the invitational 2NT when their double intervened"
    pattern: "1NT - P - 2C - P - 2D - X - 2NT - P - ?"
    rules:
      - id: sadi_3NT
        call: 3NT
        priority: 55
        requires: { hcp: [16, 17] }
        shows: "accepting the invitation: 16-17"
        establishes: { forcing: sign_off }
      - id: sadi_pass
        call: P
        priority: 50
        requires: {}
        shows: "declining the invitation: a bare 15"
        establishes: { forcing: sign_off }
        negative_inference_weight: soft
```

**What it endangers.** The new context has specificity 1000+7 and therefore
takes 2NT / 3NT / XX / P away from `general_their_double` at this exact node.
`sad2d_pass` carries `requires: {}` so the pass seat can never be starved
(round 6's `rkc5H_signoff` lesson), and `xd_run_S2` / `xd_run_H2` / `xd_run_D3`
/ `xd_rebid_C3` are untouched because this context does not define those calls.
Below it: `xd_pass` (18) is the rung being outranked — a hand that asked Stayman
has at least invitational values and a doubleton in the suit opener names, so
sitting for the double is the *worst* description available, not the safe one.

**VERIFIED.** Patched copy: N bids 2NT at fit 1.000. Rolled out, the contract
becomes **2NT down one (-100)** instead of **2DX -1100**; the board moves from
-14 to roughly level with table B.

**TEMPLATE.** `expand: { R: [D, H, S] }` on the pattern
`"1NT - P - 2C - P - 2$R - X - ?"` (with the 2$R fit-raise rung added for the
major answers), plus the same pair for the 2NT opening
(`"2NT - P - 3C - P - 3$R - X - ?"`). Six contexts, ~20 rules from one idea.

---
