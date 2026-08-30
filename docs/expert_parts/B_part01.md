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

## Board 59 — margin -13

**Seat/call:** table B call 6, E bids **4NT** (`gst_rkc_S`) on
`KQ96.Q5.KJT532.A` after `1D P 1S 2C 2S 4C`; we play 6S for eleven tricks.
The auction is competitive throughout, so it is A's board — but the losing call
is a *slam* call and the reason it is made is constructive.

What I checked (whole-corpus denominators first):
`gst_rkc_S` fires on **4 tables, mean -3.25**; `gst_rkc_D` **4 tables, -2.75**;
`gst_rkc_H` 1 table +11; `gst_rkc_C` 2 tables **+8.50**. The family is not
uniformly bad — the minors are its winners — so it must not be swept.

**The constructive observation, and it is a sibling defect.**
`gst_rkc_$X` requires `controls: [4, 12]`. Its sibling `gr_rkc_$M` — the same
1430 ask one context along — requires `controls: [5, 12]`. E holds exactly
**four** controls (K♠, K♦, A♣), so it clears one floor and would fail the other.
That is round 7's species: *a gate given to one sibling and not the other.*
And underneath it there is nothing: `cue_bidding_S` / `cue_bidding_H` carry
`when: { agreed_suit: …, game_forced: true }` at context level, so in a
**competitive** auction where partner has merely raised, the file's only slam
move is a blind 4NT — there is no control-showing rung below game at all.

I attempted the additive repair (a `4$M` "four controls is not enough to ask"
rung at priority 47 in `general_slam_try`) and **it is unreachable**: 4S at that
node is owned by `general_competitive_high` (`... - bid>=3C - ?`, specificity 3)
which outranks `general_slam_try` (`... - ?`, specificity 1), so the rung never
becomes a candidate. Traced. Reported as a negative rather than shipped.

The implementable form is therefore a **gate**, which subtracts, and I flag it
as such rather than pretending it is additive:

```yaml
# in general_slam_try, all four gst_rkc_$X: controls [4, 12] -> [5, 12]
```

It subtracts the ask on every four-control hand in all four suits. Given the
denominators above (`gst_rkc_C` +8.50 on two tables) it must be measured as its
**own** experiment, and I would measure it split by suit.

**VERDICT: competitive board; the constructive finding is the control-floor
sibling mismatch. UNTESTED as shipped (the additive route was traced and is
blocked).**

---

## Board 105 — margin -13

**Seat/call:** table B call 6, W bids **4S** on `KQ32.K4.8.AJ8643` after
`1NT - 2C - 2S` (`stm_raise_4S`, fit 1.000, prio 72). Singleton diamond, a
six-card side suit, and a known 4-4 major fit — and the only rungs above the
game raise are `stm_rkc_4NT` (15-21 HCP) and `stm_6NT_nofit`. `stm_raise_4S`
fires on **2 tables, mean -6.50**.

**The missing agreement.** After Stayman finds the 4-4 fit, a jump to four of a
minor is a splinter: the fit, shortness there, and slam interest.

### YAML — into the existing context `stayman_resp_after_2M`

```yaml
      - id: stm_splinter_4C
        call: 4C
        priority: 74
        requires: { suits: { $M: [4, 4], C: [0, 1] }, hcp: [11, 17], evals: { controls: [3, 12] } }
        shows: "splinter: the 4-4 fit, singleton or void in clubs, slam try"
        establishes: { forcing: game_forcing, agreed_suit: $M }
        alertable: true
        convention: splinter
      - id: stm_splinter_4D
        call: 4D
        priority: 74
        requires: { suits: { $M: [4, 4], D: [0, 1] }, hcp: [11, 17], evals: { controls: [3, 12] } }
        shows: "splinter: the 4-4 fit, singleton or void in diamonds, slam try"
        establishes: { forcing: game_forcing, agreed_suit: $M }
        alertable: true
        convention: splinter
```

**THE ANSWERING SEAT** (new context — a splinter is a force and is worth nothing
without it):

```yaml
  - id: opener_after_stayman_splinter
    description: "1NT opener answers responder's splinter after Stayman"
    expand_pairs:
      - { M: H, X: C }
      - { M: H, X: D }
      - { M: S, X: C }
      - { M: S, X: D }
    pattern: "1NT - P - 2C - P - 2$M - P - 4$X - P - ?"
    rules:
      - id: sspl_wasted_4$M
        call: 4$M
        priority: 47
        requires: { evals: { wasted_in_partner_shortness: [3, 40] } }
        shows: "wasted honours opposite the splinter: the agreed game is enough"
        establishes: { forcing: sign_off, agreed_suit: $M }
      - id: sspl_rkc_$M
        call: 4NT
        priority: 45
        requires:
          evals: { controls: [4, 12], wasted_in_partner_shortness: [0, 2] }
          any_of:
            - evals: { "void(any)": [0, 0], worthless_doubleton: [0, 0] }
            - evals: { "keycards($M)": [3, 5] }
        shows: "RKC 1430 for $M opposite the splinter: no duplication"
        establishes: { forcing: one_round, agreed_suit: $M, asking: keycards }
        alertable: true
        convention: rkc_1430
      - id: sspl_signoff_4$M
        call: 4$M
        priority: 34
        requires: {}
        shows: "signing off in the agreed game over the splinter"
        establishes: { forcing: sign_off, agreed_suit: $M }
        negative_inference_weight: soft
```

**What it endangers.**
* `stm_rkc_4NT` (73) — *below* the splinter now. With a singleton, describing
  the shortness first is strictly better than a blind ask, and the 4NT rung
  keeps every hand without shortness.
* `stm_raise_4$M` (72) — outranked only by a hand with a singleton/void and 11+;
  a flat 10-15 still fits 1.000 and still bids game.
* `stm_raise_3$M` (70, 8-9) / `stm_3NT_nofit` / `stm_2NT_nofit` / `stm_6NT_nofit`
  — all require either a lower band or no fit; untouched.
* 4C/4D were **not** previously covered at this node, so the new rungs delete
  the code fallback for 4C/4D there. On a hand with no shortness they fit ~0,
  and the fallback for those calls was never the chosen call in the corpus;
  stated rather than assumed.
* The answering context carries `sspl_signoff_4$M` with `requires: {}` so it can
  only ever be a superset of the seat it shadows.

**VERIFIED.** W bids 4D at fit 1.000 / prio 74. Rolled out:
`1NT - 2C - 2S - 4D - 4NT - 5S - 6S`, twelve tricks. Table B goes from +710 to
**+1460** and the board's -13 is **fully recovered**.

**TEMPLATE.** Already `expand: { M: [H, S] }` (4 rules) plus 4 answering
contexts × 3 rules. Same idea belongs in `nt2_stayman_placement` (2NT opening)
and in `r2c_2NT_stayman_reply` (the 2C-2D-2NT tree), which are the same
conversation one level up.

---

## Board 122 — margin -13

**Seat/call:** table A call 4, S passes 4H over `P 1C 1S 4H` (`ch_pass`, fit
1.000). **Purely competitive** — a preemptive jump to game over our overcall.

What I checked: every four-spade candidate (`ch_raise_lott_S4`,
`ch_raise_S4`, `ch_raise_lott4_S`) fits <= 0.029 on `T973.6..QT83.AT86` — S has
four spades and nine points opposite a one-level overcall. The seat is starved
of a *four-card-support* raise at the four level; every rung there demands five
trumps or 11+ support points.

**Best constructive-discipline observation.** The LOTT raises are all
length-gated at five trumps. The constructive counterpart — "four trumps and a
ruffing value opposite a shown five-card suit is nine combined and the Law says
bid four" — has no rung anywhere in the competitive families. That is a
`lott_total_trumps` question and it is A's to price.

**VERDICT: NOTHING-WRONG (competitive).**

---

## Board 185 — margin -13

**Seat/call:** table B call 6, W bids **4H** on `A8.AJ97.AKQ.KJ86` (22 HCP!)
after `1H - 2NT(Jacoby) - 3D(shortness)`, via `jac_wasted_signoff` (fit 1.000,
prio 47). The rule's escape clause is `any_of: [semi_balanced, total_points <= 18]`
and a 2-4-3-4 twenty-two-count satisfies the **first** branch, so the ceiling is
open at the top. `jac_wasted_signoff` fires on **3 tables, mean -4.33**.

**The missing agreement.** Wasted honours opposite partner's shortness stop a
15-19 hand; they do not stop a 22-count with seven controls, which is still
worth a slam move.

### YAML — into the existing context `responder_after_jacoby_reply`

```yaml
      - id: jac_waste_but_max
        call: 4NT
        priority: 48
        requires:
          evals: { total_points: [21, 40], controls: [7, 12], "lott_total_trumps(agreed)": [8, 26] }
          any_of:
            - evals: { "void(any)": [0, 0], worthless_doubleton: [0, 0] }
            - evals: { "keycards(agreed)": [3, 5] }
        shows: "wasted honours, but 21+ with seven controls: the hand is too big to sign off"
        establishes: { forcing: one_round, asking: keycards }
        alertable: true
        convention: rkc_1430
```

**THE ANSWERING SEAT** already exists in full — `rkc_response_agreed_H`,
`rkc_continue_after_5C/5D/5H/5S`, `rkc_5C_answerer`. Nothing new is needed and
that is why this rung is cheap.

**What it endangers.**
* `jac_wasted_signoff` (47) — only for 21+ with seven controls; the locked
  scenario the signoff was written for (a flat nineteen with KQx opposite the
  shortness) is at most six controls and is untouched. The 21/7 pair is
  deliberately double-gated so a shapely twenty cannot slip through.
* `jac_rkc` (45) — identical call, wider band; still fires for 17-20.
* `jac_place_4$M` (40), `cue_H_S/C/D` (44/43.5/43) — all outranked only inside
  the new rung's band, where a 22-count cueing at the three level then hearing a
  sign-off is a worse outcome than asking.
* 4NT is already covered here by `jac_rkc`, so **no fallback is deleted**.

**VERIFIED.** W now bids 4NT at fit 1.000, and the rollout runs
`1H - 2NT - 3D - 4NT - 5S - 6H` instead of `… 4H - 4NT - 5D - 6H`.

**Honest negative on the IMPs.** Same contract, so the board's **-13 is not
recovered**: BEN bid 7H and made it. Thirty-seven combined points with all four
aces and four kings is a grand, and reaching it needs the 5NT king ask, which is
on the do-not-re-propose list. The rung fixes the *description* (a 22-count no
longer signs off in game at fit 1.000) and shortens the auction; it does not fix
the board, and I am not going to claim it does.

**TEMPLATE.** Already `expand: { M: [H, S] }`. The identical ceiling exists on
`spl_wasted_4$M` in `opener_after_splinter_wasted` (there the cap is an explicit
`total_points: [0, 18]`, so that one is *closed* and correct) — the pair should
be made consistent by giving `opener_after_splinter_wasted` the same 21+
override, six more rules from the same idea.

---

## Board 222 — margin -13

**Seat/call:** table B call 7, E bids **4S** on `AKQ832.AKJT.K72.` after
`1C - 1S - 2C` (`rmr_4S`: "6+ S, game values", `hcp: [13, 40]`). Twenty points,
6-4 in the majors, a void — and the ladder's only rung above 3NT is an
uncapped sign-off. `rmr_4S` fires on **2 tables, mean -7.00**.

Two things are wrong at once and they are the same thing:
`responder_after_minor_rebid` has `rmr_newsuit_D` (a forcing new suit) **only
for diamonds** — a textbook sibling gap; and `rmr_4$M` runs to 40 while every
other rung in the context was deliberately capped (the file's own comments say
so). So a 6-4 twenty-count has neither a second suit to show nor a rung above
game. This is the DECISIONS open item "`responder_after_minor_rebid` has a
ceiling, not a shape hole … larger than anything round 13 shipped."

**The missing agreement.** After opener's minimum minor rebid, responder's
*other* major is a forcing new suit, and with 17+ and a two-suiter it is shown
before the game is chosen.

### YAML — into the existing context `responder_after_minor_rebid`

```yaml
      - id: rmr_newsuit_$oM
        call: 2$oM
        priority: 56
        requires: { suits: { $oM: [4, 13] }, hcp: [9, 16] }
        shows: "new suit over the minor rebid: 4+ $oM, forcing"
        establishes: { forcing: one_round }
      - id: rmr_newsuit_extras_$oM
        call: 2$oM
        priority: 59
        requires: { suits: { $oM: [4, 13], $M: [5, 13] }, hcp: [17, 21] }
        shows: "two-suited with extras: the second suit is shown before the game is chosen (forcing)"
        establishes: { forcing: game_forcing }
```

**THE ANSWERING SEAT.** Both rungs are forcing. The seat that answers them is
`opener_rebid_1m_1M`'s successor — and it already exists as the generic
game-force landing family (`gf_landing_new_suit`, `gf_landing_major`,
`gf_landing_preference_major`, `gf_landing_nt`), which is what carried the
verified rollout below: opener raised to 3H and the auction continued
`3S - 4D - 4S - 4NT - 5D - 6H` entirely out of existing rungs. No new answering
context is required, and that was checked by rolling the auction out, not
assumed.

**What it endangers.**
* `rmr_4$M` (58) — outranked only by a 17-21 hand that is *also* 5+/4+ in the
  two majors. Verified: `AKQ832.KJ.K72.72` (a 15-count with no second suit)
  still bids 4S at fit 1.000.
* `rmr_3NT` (55) / `rmr_2NT` (53) / `rmr_3$M` (57) / `rmr_3$m` (54) / `rmr_pass`
  (50) — all in lower bands.
* `rmr_4NT` (56, 17-19 `semi_balanced`) — a 6-4 hand is not semi-balanced, so
  the two never compete.
* `rmr_newsuit_D` (56) is untouched for `$oM = H` and for `$oM = S` the call is
  2S, a different call entirely; the two never collide.
* 2H/2S at this node: for `1m - 1S - 2m` the call 2H was **not** previously
  covered, so the code fallback for 2H there is deleted. That fallback was a
  natural-suit generation; the rung fits every hand it caught that has four
  hearts, and misses (correctly) the hands with three.

**VERIFIED and the board is recovered.** E bids 2H at fit 1.000 / prio 59.
Rolled out: `1C - 1S - 2C - 2H - 3H - 3S - 4D - 4S - 4NT - 5D - 6H`, and 6H by E
makes exactly twelve. Table B goes from +650 to **+1430**; the board's -13 goes
to roughly zero.

### NEGATIVE RESULT, reported rather than shipped

My first proposal for this board was a **responder's strong jump shift**
(`1C - 2S` = a good five-plus major and 17+), which is a real hole — `resp_1m`
has no jump shift at all. I built it with its answering context
(`opener_after_jump_shift_1m`, four rungs). It fired correctly at fit 1.000 /
prio 79 and every regression passed. But with `establishes: { agreed_suit: $M }`
the rollout reached **6S on a 6-0 fit** (-100 where we had been +650, i.e.
**-17 instead of -13**); with the agreement removed it reached 4H — a 4-3 fit
that happened to make twelve. A jump shift must not agree its own suit, and even
correctly written it is a call whose partner cannot yet know the fit. I am
recording it as a negative rather than shipping it, and the `rmr` sibling repair
above is strictly better: it recovers the board and touches four rules.

**TEMPLATE.** Already `expand: { m: [C, D], M: [H, S] }` → 8 new rules. The same
"the other major is a forcing new suit" gap should be checked in
`responder_rebid_1D_1H_2C`, `responder_after_1D1S_2C` and
`responder_rebid_1H_1S_2C/2D`, which are the same conversation with the suits
permuted.

---

## Board 301 — margin -13

**Seat/call:** table B call 4, E bids 3NT over `1S P 1NT 3C` (`ch_nt3`, fit
1.000, 13-19 balanced with a stopper). E is `AK732.A542.K5.K4` — 5-4 in the
majors, not balanced. **Competitive** (their jump overcall).

What I checked: `ch_new_H3` fits 0.264 and `ch_new_H3_hi` 0.108 because both
demand 14+ points *and* the "my longest suit" variant demands length E does not
have; `ch_rebid_S3` fits 0.349. So the 3NT wins a soft-miss lottery among
natural calls, exactly the `uc_nt3`/`ch_nt3` species DECISIONS records.

**Best constructive-discipline observation.** `ch_nt3` requires
`balanced`-ish shape only through its `shows`, not through its `requires` —
the family's notrump rungs deny no shape (DECISIONS says this of `uc_nt2`
explicitly, "unlike `ballow_nt1` and `cl_nt1` it denies no shape"). The
constructive counterpart that would beat it here is a **second-suit rung with no
point floor once partner has responded**, the competitive twin of
`gf_new_3$X`. Not authored: it is a competitive context and the `uc_nt3`
strength gate is on the do-not-re-propose list.

**VERDICT: NOTHING-WRONG (competitive); the notrump-versus-second-suit
lottery is a known open item, not a new finding.**

---

## Board 443 — margin -13

**Seat/call:** table B call 4, W raises to **4H** on `AK64.QJT8.AQ52.A` after
`1D - 1H` (`ob_raise_4H`, fit 1.000, "19+ support points"). Four-card support,
twenty HCP, a **singleton ace of clubs** — and opener has no shortness-showing
raise anywhere in the file. BEN bids 4C.

**The missing agreement.** Opener's double jump in a new suit after a one-level
major response is a splinter: four-card support, shortness there, 19+.

### YAML — into the existing context `opener_rebid_1m_1M`

```yaml
      - id: ob_splinter_4$om
        call: 4$om
        priority: 77
        requires:
          suits: { $M: [4, 13], $om: [0, 1] }
          evals: { total_points: [19, 40] }
        shows: "splinter raise: 4+ $M support, singleton or void in $om, 19+ support points"
        establishes: { forcing: game_forcing, agreed_suit: $M }
        alertable: true
        convention: splinter
```

**THE ANSWERING SEAT** (new context; a splinter is a force):

```yaml
  - id: responder_after_opener_splinter
    description: "Responder answers opener's splinter raise 1m - 1M - 4om"
    expand: { m: [C, D], M: [H, S] }
    pattern: "1$m - P - 1$M - P - 4$om - P - ?"
    rules:
      - id: rsp_wasted_4$M
        call: 4$M
        priority: 47
        requires: { evals: { wasted_in_partner_shortness: [3, 40] } }
        shows: "wasted honours opposite the shown shortness: the agreed game is enough"
        establishes: { forcing: sign_off, agreed_suit: $M }
      - id: rsp_rkc_$M
        call: 4NT
        priority: 45
        requires:
          evals: { total_points: [10, 40], controls: [3, 12], wasted_in_partner_shortness: [0, 2] }
          any_of:
            - evals: { "void(any)": [0, 0], worthless_doubleton: [0, 0] }
            - evals: { "keycards($M)": [3, 5] }
        shows: "RKC 1430 for $M opposite the splinter: no duplication"
        establishes: { forcing: one_round, agreed_suit: $M, asking: keycards }
        alertable: true
        convention: rkc_1430
      - id: rsp_signoff_4$M
        call: 4$M
        priority: 34
        requires: {}
        shows: "signing off in the agreed game over the splinter"
        establishes: { forcing: sign_off, agreed_suit: $M }
        negative_inference_weight: soft
```

**What it endangers.** This is the one place in my slice where the rung being
outranked is a **profitable** rule, and it has to be said plainly:
`ob_raise_4H` fires on **10 tables at mean +2.10**. The splinter is therefore
gated at 19+ *and* a singleton/void, so it takes only the shapely top of that
population; `ob_raise_3$M` (78, 16-18) is above it in priority and untouched;
`ob_raise_2$M` (80, 12-15) likewise. 4C/4D at this node were not covered, so the
code fallback for those calls is deleted in every `1m - 1M` seat — a
19-plus-with-shortness gate is the whole of what replaces it, and every other
hand there fits ~0.00, which is the failure mode round 15 traced on board 691a.
Verified that a 16-18 hand with the same shortness still bids 3H, and a 20-count
with no shortness still bids 4H.

**VERIFIED (the machinery); NEGATIVE on the board's IMPs.** W bids 4C at fit
1.000; responder E (`J5.A7632.76.KJ98`) answers **4H** — `rsp_wasted_4$M` at fit
1.000, because KJ98 opposite a singleton is four points of dead paper — and the
auction stops in game exactly as it does today. BEN's E cued 4D holding **no
diamond control at all** and got to a 6H that needed a favourable lie. So the
splinter is right bridge, is on round 17's zero-list, describes the hand
correctly, and **does not recover this board**. Reported, not dressed up.

**TEMPLATE.** `expand: { m: [C, D], M: [H, S] }` gives 4 rules + a 4-context ×
3-rule answering family. The other-major splinter (`1D - 1H - 3S`,
`1C - 1S - 4H`, …) needs a second small context because its level varies with
the pair; write it as `expand_pairs` over (m, M, short-suit) with the level
spelled out, since `call: $L$X` does not expand.

---

## Board 559 — margin -13

**Seat/call:** table A call 5, N bids **4H** on `9.AKT732.AQT87.6` after
`P 1H 1S 2S P` (`uc_raise_H4`, fit 1.000, prio 32 — a *generic* rung). Partner
has just made a **cue-bid raise** (`r1H1S_cue`, "limit raise or better in
hearts", `forcing: one_round`) and **no context in the file answers it.**

That is the mandate's central defect, stated as a fact: the file contains **five**
cue-raise rules — `r1H1S_cue`, `nx_1m1H_cue`, `nx_1m1S_cue`, `r1M2x_cue`,
`advo_cue` — and **zero** contexts whose pattern answers any of them. Every one
is a force landing in `general_uncontested_continuation`, where the best rung is
a raise by level. `uc_raise_H4` fires on **30 tables at mean -0.70**; it is not a
bad rule, it is standing in an empty seat.

**The missing agreement.** Opposite the cue-bid raise, opener's jump to four of a
side suit is shortness with slam interest; three of the major is a minimum;
four of the major is game with nothing extra.

### YAML — new context (opener answers the cue-bid raise)

```yaml
  - id: opener_after_cue_raise_1H1S
    description: "Opener answers responder's cue-bid raise 1H - (1S) - 2S"
    pattern: "1H - 1S - 2S - P - ?"
    rules:
      - id: ocr_splinter_4C
        call: 4C
        priority: 50
        requires: { suits: { H: [5, 13], C: [0, 1] }, evals: { total_points: [14, 40] } }
        shows: "shortness slam try opposite the cue-bid raise: singleton or void in clubs"
        establishes: { forcing: game_forcing, agreed_suit: H }
        alertable: true
        convention: splinter
      - id: ocr_splinter_4D
        call: 4D
        priority: 50
        requires: { suits: { H: [5, 13], D: [0, 1] }, evals: { total_points: [14, 40] } }
        shows: "shortness slam try opposite the cue-bid raise: singleton or void in diamonds"
        establishes: { forcing: game_forcing, agreed_suit: H }
        alertable: true
        convention: splinter
      - id: ocr_game_4H
        call: 4H
        priority: 45
        requires: { evals: { total_points: [14, 40] } }
        shows: "accepting the limit raise: game, no slam try"
        establishes: { forcing: sign_off, agreed_suit: H }
      - id: ocr_min_3H
        call: 3H
        priority: 44
        requires: { evals: { total_points: [12, 13] } }
        shows: "minimum opening: partner passes with a bare limit raise"
        establishes: { forcing: invitational, agreed_suit: H }
      - id: ocr_floor_3H
        call: 3H
        priority: 20
        requires: {}
        shows: "no better description opposite the cue-bid raise"
        establishes: { forcing: invitational, agreed_suit: H }
        negative_inference_weight: soft
```

**THE ANSWERING SEAT for the splinter** (the force inside the force):

```yaml
  - id: responder_after_cue_raise_splinter_1H
    description: "Responder answers opener's shortness slam try over the cue-bid raise"
    expand: { X: [C, D] }
    pattern: "1H - 1S - 2S - P - 4$X - P - ?"
    rules:
      - id: rcrs_wasted_4H
        call: 4H
        priority: 47
        requires: { evals: { wasted_in_partner_shortness: [3, 40] } }
        shows: "wasted honours opposite the shortness: the agreed game is enough"
        establishes: { forcing: sign_off, agreed_suit: H }
      - id: rcrs_rkc
        call: 4NT
        priority: 45
        requires:
          evals: { controls: [3, 12], wasted_in_partner_shortness: [0, 2], total_points: [11, 40] }
          any_of:
            - evals: { "void(any)": [0, 0], worthless_doubleton: [0, 0] }
            - evals: { "keycards(H)": [3, 5] }
        shows: "RKC 1430 for hearts opposite the shortness slam try"
        establishes: { forcing: one_round, agreed_suit: H, asking: keycards }
        alertable: true
        convention: rkc_1430
      - id: rcrs_signoff_4H
        call: 4H
        priority: 34
        requires: {}
        shows: "signing off in the agreed game"
        establishes: { forcing: sign_off, agreed_suit: H }
        negative_inference_weight: soft
```

**What it endangers.** The new context has specificity 1005 and therefore takes
3H, 4H, 4C and 4D away from `general_uncontested_continuation` at this node.
Priced against the rungs **below** as well as above: `uc_raise_H3` (31) and
`uc_raise_H4` (32) are replaced by `ocr_min_3H` / `ocr_game_4H`, whose bands are
the same shape but keyed to *partner having promised a limit raise or better*
rather than to a generic support count; `ocr_floor_3H` with `requires: {}` means
the 3H seat can never be starved, and `ocr_game_4H` with a bare
`total_points: [14, 40]` means the 4H seat cannot be either. `uc_new_D3` (27),
`uc_rebid_H3` (29) and the natural three-level calls are not defined here and
fall through unchanged — verified in the candidate list.

**VERIFIED and the board is recovered.** N bids 4C at fit 1.000 / prio 50 (with
`ocr_game_4H` right behind at 1.000/45, so the choice is `is_clear`). Rolled
out: `1H - (1S) - 2S - 4C - 4H - 4NT - 5H - 6H`, thirteen tricks. Table A goes
from +710 to **+1460** and the board's -13 goes to zero.

**TEMPLATE.** This is the highest-yield expansion in my slice, because the same
empty seat exists behind **every** cue raise:
`"1$m - 1H - 2H - P - ?"` and `"1$m - 1S - 2S - P - ?"` (`expand: { m: [C, D] }`,
answering `nx_1m1H_cue` / `nx_1m1S_cue`), `"1$M - 2$x - 3$x - P - ?"`
(`r1M2x_cue`), and `"1$o - 1$v - P - 2$o - P - ?"` (`advo_cue`). Five contexts ×
five rungs plus five answering contexts × three — about **forty rules from one
agreement**, and every one of them is a seat that today passes a force out or
hands it to a generic raise.

---

## Board 679 — margin -13

**Seat/call:** table A call 3, S overcalls **1NT** on `QT.KJ985.K85.AKJ` over
1D (`oc1D_1NT`, prio 82, fit 1.000) instead of 1H. **Competitive** — overcall
selection.

What I checked: `oc1D_1H` fits 0.800 (17 HCP against a 8-16 band) and
`oc1D_X` fits 1.000 at prio 72, so the 1NT wins on priority, not on fit. With a
good five-card major and 17 balanced-ish, the 1NT overcall is a legitimate style
choice, and DECISIONS fixes the 1NT overcall range at 15-18 deliberately.

**Best constructive-discipline observation.** The consequence is constructive:
after a 1NT overcall the file has `advance_1NT_overcall` (5 rules) and
`advance_1NT_overcall_invite` (2 rules) — **no Stayman and no transfers**, so a
5-3 major fit behind a 1NT overcall is unfindable, which is what happened
(2NT then 3NT, five tricks, while 4H was cold on the other table's cards). The
agreement that pays here is "systems on over a 1NT overcall", not a change to
the overcall.

**VERDICT: NOTHING-WRONG on the call (competitive); the real gap is the
seven-rule advance ladder behind it.**

---

## Board 761 — margin -13

**Seat/call:** table A call 5, S bids 3D in the balancing seat on
`A.874.AKJ96.KQ85` after `1S X 2S P P` (`ballow_new_D3`). **Purely
competitive** — a reopening decision after our own takeout double was passed.

What I checked: `ballow_reopen_X2` ("a SECOND double: 19+") fits 0.409 on a
17-count, `ballow_pass` 1.000, `ballow_new_D3` 1.000. Nothing is starved; this
is a judgement between three fitting calls.

**Best constructive-discipline observation.** `ballow_reopen_X2`'s 19+ floor is
a **ceiling defect in reverse**: the second double is the only way to show
17-18 with three-suited shape, and the band starts one point above the hands
that hold it. Same species as the ceilings in rounds 6 and 7, in the balancing
family rather than a constructive one.

**VERDICT: NOTHING-WRONG (competitive).**

---

## Board 762 — margin -13

**Seat/call:** table A call 0, S opens **1S** on `AJT93.A2..AQ8652` — five
spades and **six clubs** (`open_1S`, fit 1.000, prio 81). BEN opens 1C at 0.99.
The system's opening rules cover 5-5 ("higher of equal length") but say nothing
about 6-5, and the textbook rule is *bid the longer suit first*.

### YAML — into the existing context `openings`

```yaml
      - id: open_1C_six_five
        call: 1C
        priority: 82
        requires:
          suits: { C: [6, 13] }
          hcp: [12, 21]
          evals: { "suit_diff(C,S)": [1, 13], "suit_diff(C,H)": [1, 13] }
        shows: "six-plus clubs longer than the five-card major: the longer suit is bid first"
        establishes: { forcing: one_round }
      - id: open_1D_six_five
        call: 1D
        priority: 82
        requires:
          suits: { D: [6, 13] }
          hcp: [12, 21]
          evals: { "suit_diff(D,S)": [1, 13], "suit_diff(D,H)": [1, 13] }
        shows: "six-plus diamonds longer than the five-card major: the longer suit is bid first"
        establishes: { forcing: one_round }
```

**And the rebid it requires** (into `opener_rebid_1m_1NT`) — because a 6-5
opener who cannot show the major on the second round has gained nothing:

```yaml
      - id: or1mn_shape_H_$m
        call: 2H
        priority: 59
        when: { unbid_suit: H, cheapest_in_suit: true }
        requires: { suits: { H: [5, 13], $m: [6, 13] }, hcp: [12, 21] }
        shows: "six-five: the five-card heart suit is shown on shape, not on strength"
        establishes: { forcing: one_round }
      - id: or1mn_shape_S_$m
        call: 2S
        priority: 59
        when: { unbid_suit: S, cheapest_in_suit: true }
        requires: { suits: { S: [5, 13], $m: [6, 13] }, hcp: [12, 21] }
        shows: "six-five: the five-card spade suit is shown on shape, not on strength"
        establishes: { forcing: one_round }
```

**What it endangers.** `open_1S` fires on **148 tables at mean +0.15** — a large
and healthy population, and the new rung takes only hands with a *strictly
longer* minor. Verified: `AJT93.A2.4.AQ865` (6-5 by one card short of the gate,
i.e. 5-5) still opens 1S at fit 1.000, and the new rung soft-misses at 0.279.
`open_1S_rule20` (79), `open_1H` (80), `open_1NT` (92), `open_2C` (96) are all
either above it or shape-incompatible. `or1mn_shape_$M` (59) outranks
`or1mn_reverse_$M` (58) only on genuine 6-5 shape; the 17+ reverse keeps every
4-card-major hand.

**VERIFIED as a call; NEGATIVE as a change.** S does open 1C (fit 1.000, prio
82) and does rebid 2S. But the *undisturbed rollout* then runs
`1C - 1NT - 2S - 2NT - 3C` and dies in a partscore where opening 1S reaches 4S.
The reason is that `1m - 1NT - 2M` (opener's shape reverse) has **no responder
context at all**, so responder invites in notrump and opener retreats. So: the
opening rule is right, BEN agrees with it, and **it measures worse until the
`1$m - P - 1NT - P - 2$M - P - ?` ladder exists**. Reported as a negative and
paired with the prerequisite rather than shipped alone. (The real table A auction
was interrupted by a 5D overcall, so the rollout is the cleanest evidence
available, and it says don't ship half of this.)

**TEMPLATE.** The two opening rules are already the whole family (majors are
covered by "higher of equal length"). The prerequisite is a new context
`"1$m - P - 1NT - P - 2$M - P - ?"`, `expand: { m: [C, D], M: [H, S] }`, four
contexts × four rungs (preference to the minor, false preference, 2NT, raise).

---

## Board 886 — margin -13

**Seat/call:** table A call 2, N runs to **2C** on `9.97.QJ94.KT8542` over their
takeout double of our 1H (`xd_run_C2`). **Purely competitive** (a runout).

What I checked: `rdx_pass` fits 0.800 (its band tops at some HCP the six-count
just clears), `jordan_raise` 0.349, `xd_run_C2` 1.000. BEN passes. The runout
ladder has no "pass with a misfit and no values" rung above the run.

**Best constructive-discipline observation.** The constructive fact underneath
is that N holds a **singleton in partner's suit** and the runout rules are
length-gated only on the run suit — nothing consults the fit with opener. A run
that leaves a 6-1 fit for a 5-1 fit is the same defect as a raise that ignores
`lott_total_trumps`. That is one gate on `xd_run_$X`, and it is A's to price
because it subtracts in a competitive family.

**VERDICT: NOTHING-WRONG (competitive).**

---

## Board 26 — margin -12

**Seat/call:** table A call 2, N opens a weak **2H** in third seat on
`6.AK9876.J53.Q92` (10 HCP, `open_weak_2H_nv`, fit 1.000). BEN bids 3H.

What I checked: DECISIONS fixes the weak two as "exactly 6 cards, 5-10 HCP
non-vul with a good suit", and `open_3H_nv` requires seven. A six-card suit
cannot preempt at the three level in this system by construction, so the call is
the system's, not a defect. Opening-style thresholds are on the
do-not-re-propose list.

**Best constructive-discipline observation.** The board is then lost in the
*answering* seat: after `2H - X - P - 2S` our side has `weak2_our_side_doubled`
(3 rules) and nothing that distinguishes a maximum weak two with a side ace from
a minimum. The constructive counterpart of a preempt is the **feature/ask**
structure, and `weak2_feature_answer_H` exists only over 2NT — there is no rung
at all after the opponents act. Same species as the missing cue-raise answers.

**VERDICT: NOTHING-WRONG on the opening (scope-excluded); the gap is the
doubled-weak-two answering ladder.**

---

## Board 43 — margin -12

**Seat/call:** table A call 3, S overcalls **1H** on `J3.AJ7653.Q4.T52` over 1C
(`oc1C_1H`, fit 1.000); BEN bids 2H (weak jump). **Purely competitive.**

What I checked: `oc1C_2H_jump` fits 0.200 (six hearts but the "6 hearts" gate
reads exactly six and the 5-10 band clips an 8-count with a poor suit) and the
one-level overcall fits 1.000. DECISIONS round 11: re-ranking the weak jump
overcall measured **-24 held out**; excluded.

**Best constructive-discipline observation.** Board 43's real cost is at call 9,
where N raises to 3H via `balhigh_raise_H3` after three passes — i.e. our side's
constructive raise happened *two rounds late* because nothing let N raise
immediately. The constructive agreement that would matter is a **fit-showing
jump by advancer** (`1C - 1H - (1S) - 3D` = diamonds and a heart fit), which is
one of the five conventions round 17 counted at zero rules.

**VERDICT: NOTHING-WRONG (competitive); fit-showing jumps by advancer are the
zero-rule family this board wants.**

---

## Board 314 — margin -12

**Seat/call:** table A call 4, S passes over `P P 1C 2C` holding
`J5.A98.762.QJ763` (`cl_pass`, fit 1.000; `cl_raise_C3` fits 0.800 and loses).
**Purely competitive** — a two-suited cue overcall of our 1C.

What I checked: the whole ladder. `cl_raise_C3` misses its own gate by about a
point (`8+ support points, 8+ combined trumps`) and the catch-all pass wins the
soft-miss lottery. This is the "hole in a ladder is a PASS by construction"
mechanism, not a bad rung.

**Best constructive-discipline observation.** Their 2C here is a Michaels-style
cue that our system does not define (DECISIONS scopes Michaels out), so our
`when: { their_last_bid_suit: … }` machinery reads it as natural clubs and the
raise rung is being asked to raise a suit the opponents "have". The constructive
consequence is that `lott_total_trumps` is computed against a phantom. Worth
knowing; not a rung.

**VERDICT: NOTHING-WRONG (competitive).**

---

## Board 318 — margin -12

**Seat/call:** table A call 6, N bids **2C** — fourth suit forcing at **fit
0.435** — on `AQ83.KQT53.K74.A` after `1D - 1H - 1S`. `fsf_2C` fires on **2
tables, mean -6.00**, and it is winning here only because every rung in
`responder_after_1S_rebid` is capped at 18 and N has 21 support points. The
file's own comment on `r1sr_game` says "capped at 18: nineteen-plus opposite an
opening hand is slam territory and belongs to the keycard rules" — but **no
keycard rule is a candidate at this node**, so the cap opens onto nothing.

**The missing agreement.** With four-card support for opener's second suit, 19+
support points and a singleton, responder splinters instead of inventing the
fourth suit.

### YAML — into the existing context `responder_after_1S_rebid`

```yaml
      - id: r1sr_splinter_4$om
        call: 4$om
        priority: 60
        requires: { suits: { S: [4, 13], $om: [0, 1] }, evals: { total_points: [19, 40] } }
        shows: "splinter: 4+ spades, singleton or void in $om, 19+ support points, slam try"
        establishes: { forcing: game_forcing, agreed_suit: S }
        alertable: true
        convention: splinter
```

(`$om` is the *unbid* minor: after `1D - 1H - 1S` the only splinterable suit is
clubs, and after `1C - 1H - 1S` it is diamonds. The template derives it.)

**THE ANSWERING SEAT** (new context):

```yaml
  - id: opener_after_responder_splinter_1S
    description: "Opener answers responder's splinter over the 1S rebid"
    expand: { m: [C, D] }
    pattern: "1$m - P - 1H - P - 1S - P - 4$om - P - ?"
    rules:
      - id: osp_wasted_4S
        call: 4S
        priority: 47
        requires: { evals: { wasted_in_partner_shortness: [3, 40] } }
        shows: "wasted honours opposite the splinter: the agreed game is enough"
        establishes: { forcing: sign_off, agreed_suit: S }
      - id: osp_rkc_4NT
        call: 4NT
        priority: 45
        requires:
          evals: { controls: [3, 12], wasted_in_partner_shortness: [0, 2], total_points: [12, 40] }
          any_of:
            - evals: { "void(any)": [0, 0], worthless_doubleton: [0, 0] }
            - evals: { "keycards(S)": [3, 5] }
        shows: "RKC 1430 for spades opposite the splinter: no duplication"
        establishes: { forcing: one_round, agreed_suit: S, asking: keycards }
        alertable: true
        convention: rkc_1430
      - id: osp_signoff_4S
        call: 4S
        priority: 34
        requires: {}
        shows: "signing off in the agreed game over the splinter"
        establishes: { forcing: sign_off, agreed_suit: S }
        negative_inference_weight: soft
```

**What it endangers.**
* `r1sr_4H` (58) — six hearts and 13-18; the splinter needs 19+ **and**
  shortness, so the bands are disjoint.
* `r1sr_game` (55, 4S, 13-18) — fires on **1 table at +13**, i.e. it is a winner
  and must not be disturbed; the 19+ gate keeps it entirely.
* `r1sr_raise_inv` (54, 10-12), `r1sr_3NT` (53, no spade fit), `r1sr_2NT`,
  `r1sr_1NT`, `r1sr_2H`, `r1sr_3H`, `r1sr_raise` (52), `r1sr_pass` (48) — all in
  lower bands or explicitly denying the spade fit.
* `fsf_2C` (65) is in a different context and a different call and is untouched
  for the hands it describes (game values with no clear natural bid); it simply
  stops winning at fit 0.435 when something fits 1.000.
* 4C/4D were not covered at this node, so their code fallback is deleted there.

**VERIFIED and the board is recovered.** N bids 4C at fit 1.000 / prio 60.
Rolled out: `1D - 1H - 1S - 4C - 4NT - 5S - 6S`, thirteen tricks. Table A goes
from 4NT (+720) to **6S (+1460)**; the board's -12 goes to zero.

**TEMPLATE.** `expand: { m: [C, D] }` here, and the identical rung belongs in
every "responder over opener's new second suit" context —
`responder_rebid_1H_1S_2C`, `responder_rebid_1H_1S_2D`,
`responder_reverse_rebid_major`, `responder_after_1D1S_2C`,
`responder_rebid_1D_1H_2C`. Six contexts, ~12 rules plus their answering
contexts, from one agreement.

---

## Board 479 — margin -12

**Seat/call:** table A call 7, S bids **3C** at **fit 0.082** on
`853.K32.A94.AKT9` after `1C - 2C - 2NT` (`uc_raise_C3`). The top fit in the
whole candidate set is 0.082 — the seat is *starved*, and this is the DECISIONS
open item "there is no context for opener's rebid after a 2/1 in a MINOR"
seen from the other side: `responder_21_after_2NT` is patterned `1$M - …`, so
the entire `1m - 2m - 2NT` conversation is unauthored.

**The missing agreement.** Opposite opener's 12-14 balanced rebid in a
minor-suit game force, responder chooses 3NT, or sets the minor with 17+, or
invites slam quantitatively — exactly as he already does after a major opening.

### YAML — new contexts (the minor twin of `responder_21_after_2NT`)

```yaml
  - id: responder_21m_after_2NT
    description: "Responder's rebid after 1m - 2m - 2NT (the minor twin of responder_21_after_2NT)"
    expand_pairs:
      - { m: C, x: C }
      - { m: D, x: C }
    pattern: "1$m - P - 2$x - P - 2NT - P - ?"
    rules:
      - id: r21m_set3_$m$x
        call: 3$m
        priority: 62
        requires: { suits: { $m: [4, 13] }, evals: { total_points: [17, 40] } }
        shows: "setting the minor: 4+ $m and 17+, game forcing with slam interest"
        establishes: { forcing: game_forcing, agreed_suit: $m }
      - id: r21m_quant_$m$x
        call: 4NT
        priority: 61
        requires: { hcp: [18, 21], evals: { semi_balanced: [1, 1] } }
        shows: "quantitative: 18+ opposite the 12-14 notrump rebid, inviting slam"
        establishes: { forcing: invitational }
        alertable: true
      - id: r21m_3NT_$m$x
        call: 3NT
        priority: 60
        requires:
          hcp: [12, 17]
          not: { evals: { longest_suit_length: [6, 13] } }
        shows: "the nine-trick game opposite opener's balanced minimum"
        establishes: { forcing: sign_off }
      - id: r21m_floor_$m$x
        call: 3NT
        priority: 25
        requires: {}
        shows: "no better description: the game force lands in 3NT"
        establishes: { forcing: sign_off }
        negative_inference_weight: soft
```

**THE ANSWERING SEAT for the quantitative 4NT:**

```yaml
  - id: opener_accepts_quant_21m
    description: "Opener answers the quantitative 4NT after 1m - 2m - 2NT"
    expand_pairs:
      - { m: C, x: C }
      - { m: D, x: C }
    pattern: "1$m - P - 2$x - P - 2NT - P - 4NT - P - ?"
    rules:
      - id: qa21m_6NT_$m$x
        call: 6NT
        priority: 40
        requires: { hcp: [14, 40] }
        shows: "accepting the slam invite: the top of the 12-14 rebid"
        establishes: { forcing: sign_off }
      - id: qa21m_pass_$m$x
        call: P
        priority: 30
        requires: {}
        shows: "declining: a minimum for the 2NT rebid"
        establishes: { forcing: sign_off }
        negative_inference_weight: soft
```

The **3$m** rung is also a force; its answering seat already exists —
`gf_landing_minor` (`when: { agreed_suit: $m, game_forced: true }`) supplies
3NT / 4M / 5m, and `cue_bidding_*` plus `rkc_ask` supply the slam machinery once
the suit is agreed. Checked, not assumed.

**What it endangers.** Specificity 1007, so this context takes 3NT, 4NT and 3$m
away from `gf_landing_nt` (`gf_3NT`, prio 34 — fires on 22 tables, mean -0.95),
`uc_nt3`, `uc_raise_C3` (11 tables, mean -0.73) and `gf_landing_minor` **at this
node only**. `r21m_floor_$m$x` with `requires: {}` guarantees the 3NT seat is
never starved, which is the whole superset discipline. `gf_game_5C` (3 tables,
mean -2.33) no longer gets reached from here, which is the point: it was
producing 5C on hands worth 3NT.

**VERIFIED and the board is recovered.** S bids 3NT at fit **1.000** (from
0.082). Rolled out: `1C - 2C - 2NT - 3NT`, ten tricks, table A goes from
5C-down-one (-100) to **+630**; the board's -12 goes to zero.

**TEMPLATE.** `expand_pairs` over the two real minor 2/1s. The sibling gap that
produced this — a `1$M`-only pattern where `1$m` also occurs — should be swept
across `opener_rebid_after_2over1_minor`, `responder_21_after_2M` and
`responder_21_after_second_suit_*`, which are all patterned on a major opening
only.

---

## Board 580 — margin -12

**Seat/call:** table A call 2, S doubles their 2S on `6.T986.AT85.AK43`
(`cl_negative_X2`, fit 1.000, prio 33) with `cl_raise_H4` and `cl_raise_H3` also
at fit 1.000 just below. **Purely competitive** — a negative double versus a
raise, decided on three points of priority.

What I checked: three rules fit 1.000 and the choice is priority alone. That is
the "genuine priority tie" population DECISIONS round 16 sized at 34 of 92
unclear decisions, worth -76 gap-points — small, and re-ranking it is a
competitive judgement.

**Best constructive-discipline observation.** S holds four-card support for
partner's opened major and a singleton in their suit: the constructive
description is a **fit-showing / mixed raise**, and the file's competitive raise
ladder is banded only by support points, with no rung that says "four trumps and
a singleton". That is the mini-splinter — zero rules — in its competitive form.

**VERDICT: NOTHING-WRONG (competitive); the mini-splinter is what this hand
wants.**

---

## Board 959 — margin -12

**Seat/call:** table A call 3, S bids **1S** in the sandwich seat on
`AKQJT854..2.J932` — an eight-card suit — via `sw_1S` (fit 1.000, prio 68);
`sw_3S` (seven-card preemptive jump) fits 0.800 and `sw_2S_jump` 0.800. BEN bids
4S. **Purely competitive.**

What I checked: the sandwich ladder tops out at a seven-card jump to three; there
is no eight-card rung, so an eight-bagger soft-misses every jump and the
one-level overcall wins on fit. That is a **ceiling** in the length dimension
rather than the strength dimension — rounds 6 and 7's species with a different
axis. The repair is one rung (`sw_4$X`, eight cards, 3-10) and it is A's
context.

**VERDICT: NOTHING-WRONG constructively (competitive family); the finding is a
length ceiling in `sandwich_seat`.**

---

## Board 967 — margin -12

**Seat/call:** table A call 7, S bids **3D** on `QJ75.2.T653.AQT6` after
`1D - 1S - 2H` (opener's **reverse**) — via the generic `uc_raise_D3`, which
fires on **14 tables at mean -3.86**. It agreed diamonds, which unlocked
`gst_rkc_D`, which produced 6D down one.

The reason the generic rung got the seat is arithmetic: `responder_reverse_1D1S2H`
has four rungs, and `rrevd_3NT` — the one that describes this hand — requires
**12+ HCP** opposite a bid that promises **17+**. `rrevd_3NT` **never fires in
1000 boards**. `rrevd_2NT` needs `semi_balanced` and S is 4-1-4-4.

**The missing agreement.** Opposite a reverse, eight or nine points is already
game values: the 3NT rung must be banded against opener's shown 17+, not against
a generic opening.

### YAML — into the existing context `responder_reverse_1D1S2H`

```yaml
      - id: rrevd_3NT_min
        call: 3NT
        priority: 63.5
        requires: { hcp: [8, 11], evals: { weakest_unshown_stopper: [0.9, 9] }, suits: { H: [0, 3] } }
        shows: "game opposite the 17+ reverse: 8-11 with the unshown suit stopped"
        establishes: { forcing: sign_off }
```

**THE ANSWERING SEAT.** 3NT is a sign-off, so none is owed; `opener_over_reverse_2NT`
and the generic quiet contexts already handle opener's pass. Checked in the
rollout — the auction ends there.

**What it endangers.**
* `rrevd_3NT` (63) — same call, disjoint band (12+). It never fires today, so
  nothing is taken from it in practice.
* `rrevd_2NT` (64) — 8-11 **and** `semi_balanced`; my rung is above it in
  priority only for the shapely 8-11 hands the 2NT explicitly denies, which is
  the whole point. A genuinely balanced 9-count still fits 2NT at 1.000 and
  2NT's priority is higher, so it keeps them. *(This is the one place I priced
  upward as well as downward and it matters: 64 > 63.5, so `rrevd_2NT` wins its
  own hands.)*
* `rrevd_2S` (66) and `rrevd_3H` (65) — both above it; a five-card spade suit or
  four-card heart support still takes precedence, correctly.
* `uc_raise_D3` (27) is the rung **below** that this displaces, and that is the
  intended effect: raising opener's first suit to three after a reverse is the
  least descriptive call available and it was setting trumps by accident.
* 3NT is already covered here, so no fallback is deleted.

**VERIFIED and the board is recovered.** S bids 3NT at fit 1.000 / prio 63.5.
Rolled out: `1D - 1S - 2H - 3NT`, ten tricks. Table A goes from 6D-down-one
(-100) to **+630**; the board's -12 goes to zero.

**TEMPLATE.** The same wrong-band defect is in the sibling reverse contexts —
`responder_reverse_rebid_major` (`1C - 1$M - 2D`, `expand: { M: [H, S] }`),
`responder_reverse_1C1S2H` and `responder_after_1S_rebid`'s notrump rungs. Four
contexts, four rules, one idea: **band responder against what opener promised,
not against a generic opening.** I would run that as a sweep across the file —
`rrevd_3NT` never firing is exactly the signature to grep for.

---

## Board 212 — margin -11

**Seat/call:** table A call 4, N passes over `1D P 1H 3C` on
`A982.AJ6.A87543.` (`ch_pass`, fit 1.000; `ch_rebid_D3` fits 0.409). **Purely
competitive** — their preemptive jump overcall over our 1D.

What I checked: every constructive-looking candidate. `ch_rebid_D3` needs six
diamonds and "values for the level"; N has six diamonds and 13 HCP and fits
0.409, so the band, not the shape, is what misses. `ch_new_S3` fits 0.264 (four
spades against a 5+ gate).

**Best constructive-discipline observation.** N is 4-3-6-0 with a **void** in
their suit and four spades — the perfect hand for a **support double / three-suit
takeout** over the preempt, and `neg_double_3level_m` has two rules. The
constructive fact is that opener's rebid ladder disappears entirely once RHO
jumps: the `ch_*` family is banded on points with no shape vocabulary, so a
6-4 with a void is described by a pass.

**VERDICT: NOTHING-WRONG (competitive).**

---

## Board 292 — margin -11

**Seat/call:** table B call 7, W bids **4NT** on `763.A4.AQJT87.Q7` after
`1H - 2D - 3H` (`rkc_4NT`, fit 1.000, prio 45); we play 6H for ten tricks.
`rkc_4NT` fires on **10 tables at mean -0.40**, so the rule is roughly neutral
overall and must not be swept — but this seat is exactly where the mandate says
the information exchange fails: hearts are agreed at the *three* level, four
different calls fit 1.000, and the highest-priority one is the ask.

**The missing agreement.** With a doubleton trump and no extra controls, the
game is the limit: bidding it directly is *fast arrival* and denies the slam try
that a cue would show.

### YAML — into the existing context `cue_bidding_H` (and its `_S` twin)

```yaml
      - id: cue_H_fast4H
        call: 4H
        priority: 46
        when: { standing_bid_level: [3, 3], we_hold_contract: false }
        requires:
          suits: { H: [2, 2] }
          evals: { total_points: [12, 16], controls: [0, 4] }
        shows: "fast arrival: a doubleton trump, no extra controls - the game is the limit"
        establishes: { forcing: sign_off, agreed_suit: H }
```

**THE ANSWERING SEAT.** 4H is a sign-off in the agreed suit, so nothing is owed
— and that is the point of the rung: it *closes* a conversation that today opens
one nobody can finish. Partner's seat over 4H is
`slam_try_over_game_raise` / the quiet contexts, both already authored.

**What it endangers.**
* `rkc_4NT` (45) — the rung directly below. Priced explicitly: a hand with a
  **doubleton** trump and at most four controls holds neither the trump length
  nor the control count that makes a keycard answer useful, and 1430 replies
  from a partner who cannot know which two cards you are missing are how this
  file reaches 6H on ten tricks.
* `cue_H_S` (44), `cue_H_C` (43.5), `cue_H_D` (43) — all require 14+ total
  points *and* a first-round control in the cue suit; a hand that has one and
  fits their band will usually also exceed `controls: [0, 4]` and keep cueing.
  This rung deliberately takes only the flat minimum.
* `cue_H_signoff` (34, `requires: {}`) — same call, and it stays as the floor,
  so the 4H seat is never starved (it fires on 5 tables at **mean +2.20**, i.e.
  signing off in the agreed game is one of the more profitable things this
  engine does, which is corroborating evidence for the rung).
* 4H is already covered here, so no fallback is deleted.

**VERIFIED and the board is recovered.** W bids 4H at fit 1.000 / prio 46;
rolled out the auction is `1H - 2D - 3H - 4H`, ten tricks. Table B goes from
6H-down-two to **4H making**; the board's -11 goes to zero.

**TEMPLATE.** Twin it into `cue_bidding_S` (`cue_S_fast4S`, identical). And the
generalisation worth authoring properly is the other half of the same
convention: **serious / frivolous 3NT** — currently **zero rules**. In this exact
context 3NT is available over a three-level agreement and is the natural place
for "game values, slam interest to be decided", with the cue rungs meaning
"serious". That is a four-context, ~12-rule agreement (`cue_bidding_H`,
`cue_bidding_S`, and the two minor equivalents that do not yet exist) and it is
the single named convention in round 17's zero-list that this slice touches most
often.

---
