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

## Board 326 — margin -11

**Seat/call:** table A call 0, S **passes** on `Q7542.AQT53.K87.` — 11 HCP, 5-5
in the majors, rule of 20 satisfied (11 + 10 = 21). `open_pass` fits 1.000 and
scores 0.760; `open_1S` fits 0.800 and scores **0.754**. The whole board turns
on six thousandths of blended score.

What I checked: `open_1S_rule20` fits 0.757, not 1.000, because it carries a
suit-quality requirement that Q7542 fails. So the light-opening rung exists and
the *shape* hand cannot reach it.

**Opening-style / rule-of-20 thresholds are on the do-not-re-propose list**, so I
am not proposing a change. The observation worth recording is narrower and is not
a threshold: the rule-of-20 rungs gate on **suit quality of the suit being
opened**, which is the right test for a one-suiter and the wrong test for a
**two-suiter**, where the playing strength comes from the second suit. A 5-5
eleven-count is a mainstream opening on shape whatever the spot cards are. If
anyone reopens the light-opening question, that is the axis — not the point
count.

**VERDICT: NOTHING-WRONG (scope-excluded); the finding is that the rule-of-20
rungs have no two-suiter branch.**

---

## Board 381 — margin -11

**Seat/call:** table A call 3, N passes in the sandwich seat on
`.A9653.KQJ872.T4` (`sw_pass`, fit 1.000; `sw_2D` fits 0.800). **Purely
competitive.**

What I checked: `sw_2D` requires "good 5+ diamonds, 11-17" and N has KQJ872 with
10 HCP — one point under the floor — so the catch-all pass wins the soft-miss
lottery. A textbook 6-5 with a void.

**Best constructive-discipline observation.** Same axis as board 326: the
sandwich ladder bands on HCP with a `good_suit` gate and has no **shape** branch,
so a 6-5 with a void has to borrow points it does not have. Every family in this
part that loses a board to a one-point soft miss loses it because the rung is
banded on high cards where the hand's value is distributional. That is the
single most common mechanism I saw across the 38 boards, constructive and
competitive alike.

**VERDICT: NOTHING-WRONG (competitive).**

---

## Board 384 — margin -11

**Seat/call:** table A call 4, N answers partner's negative double with **2S**
on `AQT65.J3.AK3.KT6` — 17 HCP, five spades — via `adx_neg_major_S2`, whose band
is `hcp: [11, 40]` with no upper limit and whose 3S twin carries the identical
band plus `cheapest_in_suit: true`, so it is unreachable. `adx_neg_major_S2`
fires on **4 tables at mean -3.75**. Partner then jumps to game on eleven, N
cannot tell a minimum from a maximum, asks for keycards, and we play 6S for
eleven tricks.

**The missing agreement.** The answer to a negative double is banded: cheapest
with a minimum, **jump with 16+ and a five-card suit**.

### YAML — into the existing context `general_pull_or_sit`

```yaml
      - id: adx_neg_major_jump_H
        call: 3H
        priority: 63
        when: { unbid_suit: H, their_last_bid_suit: true, i_have_acted: true, standing_bid_level: [2, 2] }
        requires: { suits: { H: [5, 13] }, hcp: [16, 40] }
        shows: "jump answer to the negative double: a five-card heart suit and 16+"
        establishes: { forcing: invitational, agreed_suit: H }
      - id: adx_neg_major_jump_S
        call: 3S
        priority: 63
        when: { unbid_suit: S, their_last_bid_suit: true, i_have_acted: true, standing_bid_level: [2, 2] }
        requires: { suits: { S: [5, 13] }, hcp: [16, 40] }
        shows: "jump answer to the negative double: a five-card spade suit and 16+"
        establishes: { forcing: invitational, agreed_suit: S }
```

Note the deliberate absence of `cheapest_in_suit` — that gate is what makes the
existing `adx_neg_major_$M3` rungs dead, since 2S is always the cheap spade bid
when the standing bid is 2H.

**THE ANSWERING SEAT.** The jump is invitational and it is answered by rungs that
already exist (`uc_doubler_game_S` raises to game, `uc_pass` declines). The
mechanism that pays here is the **negative inference**, and it is worth spelling
out because it is why this rung fixes the board: once N has shown 16+, partner's
raise to game is *limited*, `rule_of_26_sharp` for N drops below `gr_rkc_S`'s
floor of 30, and the keycard ask stops firing **without any gate being added to
it**. Describing before asking is what turns the ask off.

**What it endangers.**
* `adx_neg_major_S2` / `_H2` (62) — outranked only at 16+ with a five-card suit;
  the 11-15 hands the rules were written for (the file's comment ties the floor
  to the 11-HCP takeout double) still fit 1.000 and still bid two.
* `adx_neg_major_S3` / `_H3` (62) — same call as my rung; they carry
  `cheapest_in_suit: true` and are unreachable at this node, so nothing is taken.
* `adx_pull_my_S3` / `adx_pull_H3` (60/57) and the rest of the pull ladder — all
  below, and all describe a hand *pulling* the double rather than answering it.
* `adx_sit` (61) — above my rung, so a genuine trump stack still sits.
* 3S/3H were already covered here by the `_S3` / `_H3` rungs, so **no code
  fallback is deleted**.

**VERIFIED and the board is recovered.** N bids 3S at fit 1.000 / prio 63.
Rolled out: `1NT - (2H) - X - P - 3S - P - 4S - P - P`, eleven tricks. Table A
goes from 6S-down-one (-50) to **+450**; the board's -11 goes to zero.

**TEMPLATE.** The two rules as written cover both majors. The same "band the
answer to the double" idea belongs in `advance_takeout_double_suits_*`
(four contexts) and `advance_reopening_double`, where the cheapest-suit advance
is likewise 0-8 with a jump at 9-11 but nothing above.

---

## Board 385 — margin -11

**Seat/call:** table A call 5, S bids **3S** on `T4.KQJ.AQ93.KT63` after his own
takeout double and advancer's **game-forcing cue** 2S (`gf_pref_3S`, fit 0.349
— another soft-miss). The cue `adv_cue` is `forcing: game_forcing` and
**nothing in the file answers it**: `1$o - X - P - 2$o - P - ?` has no context,
so the generic game-force landing rules decide, and "preference to partner's
major" put us in a 4-3 spade game.

This is the same defect as board 559 in the doubler's seat rather than opener's:
a force with no answering seat.

### YAML — two new contexts

```yaml
  - id: doubler_over_advance_cue_suit
    description: "The takeout doubler answers advancer's game-forcing cue: a real suit"
    expand: { o: [C, D, H, S], X: [C, D, H, S] }
    pattern: "1$o - X - P - 2$o - P - ?"
    rules:
      - id: dacs_3$X
        call: 3$X
        priority: 60
        when: { unbid_suit: $X, cheapest_in_suit: true }
        requires: { suits: { $X: [5, 13] } }
        shows: "answering the game-forcing cue with my real suit: 5+ $X"
        establishes: { forcing: game_forcing }

  - id: doubler_over_advance_cue_nt
    description: "The takeout doubler answers advancer's game-forcing cue: notrump"
    expand: { o: [C, D, H, S] }
    pattern: "1$o - X - P - 2$o - P - ?"
    rules:
      - id: dacn_3NT_$o
        call: 3NT
        priority: 55
        requires: { hcp: [14, 40], evals: { weakest_unshown_stopper: [0.9, 9] } }
        shows: "game-forcing values opposite the cue, their suit stopped: 3NT"
        establishes: { forcing: sign_off }
      - id: dacn_floor_$o
        call: 3NT
        priority: 20
        requires: {}
        shows: "no better description opposite the game-forcing cue"
        establishes: { forcing: sign_off }
        negative_inference_weight: soft
```

**THE ANSWERING SEAT for `dacs_3$X`.** It is game-forcing with a named suit, and
`gf_landing_*` plus `cue_bidding_*` already answer a game force with a shown
suit; the rollout confirms the auction terminates properly rather than drifting.

**What it endangers.** Specificity 1006, so these contexts own 3C/3D/3H/3S/3NT at
this node. Below them: `gf_pref_3S` (37) and `gf_new_3$X` (36) — the doubler's
own five-card suit is a strictly better description than "preference" to a suit
advancer merely cued; `uc_nt2` (28) and `uc_nt3` (29) are a different call or
outranked. `dacn_floor_$o` with `requires: {}` keeps the 3NT seat alive. Note the
duplicate-3NT hazard: only the *first* expanded `$X` context could own 3NT, which
is why 3NT lives in its own `expand: { o }` context — a template detail that
would otherwise bite.

**VERIFIED and the board is recovered.** Rolled out, the auction becomes
`1S - X - P - 2S - P - 3NT` (ten tricks) instead of
`… 3S - P - 4S` (eight tricks). Table A goes from -100 to **+430**; the board's
-11 goes to zero. (Also traced on a doubler holding a real six-card club suit —
`A7.KJ4.65.KQJ652` — which correctly bids 3C at fit 1.000.)

**TEMPLATE.** As written: `expand: { o, X }` gives 16 contexts × 1 rule plus 4
contexts × 2 rules. The same missing answering seat exists behind
`advance_cue_doubled`'s cue and behind `advo_cue`; see board 559 for the full
list of unanswered cues.

---

## Board 422 — margin -11

**Seat/call:** table A call 4, S runs to **2D** on `4.72.QJ97632.T85`
(3 HCP) over their takeout double of our 1S (`xd_run_D2`, fit 1.000; `rdx_pass`
also 1.000, prio 20). **Purely competitive** — a runout, decided on priority
between two fit-1.000 rules.

What I checked: both candidates fit perfectly; there is no missing rung, only a
ranking question, and running with a seven-card suit and three points is
defensible bridge that happens to have gone badly here.

**Best constructive-discipline observation.** The system has no **weak jump
response** over the double: `resp_1M_over_X_jordan` gives 2NT (limit+), a
preemptive raise and a redouble, but a seven-card suit with 3 HCP has to choose
between a quiet 2D and a pass. In an uncontested auction that hand bids 3D
(preemptive); over a double it cannot. Sibling gap between the contested and
uncontested responding ladders.

**VERDICT: NOTHING-WRONG (competitive).**

---

## Board 426 — margin -11

**Seat/call:** table A call 10, N bids **3S** on `K986.8.A42.KJ432` after
`1C - 1H - 1S - 2S` — via `uc_raise_S3` at **fit 0.946**, i.e. a generic
support-count raise scraping over the fast-path threshold. `uc_raise_S3` fires
on **13 tables at mean -1.85**.

The auction `1$m - 1H - 1S - 2S` — responder has raised opener's **second**
suit — **has no context in the file at all**. And the one place where the same
decision *is* authored, `responder_rebid_after_1M_raise` (`1M - 2M`), has
exactly three rungs: pass, 3M, 4M. **There is no help-suit game try anywhere in
the system**; round 17 counted it at zero rules and this is what that costs: the
only game try available is a raise, which tells partner nothing about *where*
the values are needed.

**The missing agreement.** Three of a new suit below the agreed major is a
help-suit game try: shortness or losers there, spades agreed, 14-18 support
points — and partner accepts on help in that suit or on a maximum.

### YAML — new context (opener's trial bid)

```yaml
  - id: opener_trial_after_second_suit_raise
    description: "Opener's help-suit game try after responder raises the second suit"
    expand: { m: [C, D] }
    pattern: "1$m - P - 1H - P - 1S - P - 2S - P - ?"
    rules:
      - id: otr_trial_3C
        call: 3C
        priority: 53
        requires:
          suits: { S: [4, 13], C: [3, 6] }
          evals: { total_points: [14, 18] }
          not: { evals: { "two_of_top3(C)": [1, 1] } }
        shows: "help-suit game try: club losers, spades agreed, 14-18 support points"
        establishes: { forcing: invitational, agreed_suit: S }
        alertable: true
      - id: otr_trial_3D
        call: 3D
        priority: 52.5
        requires:
          suits: { S: [4, 13], D: [3, 6] }
          evals: { total_points: [14, 18] }
          not: { evals: { "two_of_top3(D)": [1, 1] } }
        shows: "help-suit game try: diamond losers, spades agreed, 14-18 support points"
        establishes: { forcing: invitational, agreed_suit: S }
        alertable: true
      - id: otr_trial_3H
        call: 3H
        priority: 52
        requires:
          suits: { S: [4, 13], H: [3, 6] }
          evals: { total_points: [14, 18] }
          not: { evals: { "two_of_top3(H)": [1, 1] } }
        shows: "help-suit game try: heart losers, spades agreed, 14-18 support points"
        establishes: { forcing: invitational, agreed_suit: S }
        alertable: true
      - id: otr_game_4S
        call: 4S
        priority: 54
        requires: { suits: { S: [4, 13] }, evals: { total_points: [19, 40] } }
        shows: "bidding the game opposite the raise"
        establishes: { forcing: sign_off, agreed_suit: S }
      - id: otr_pass
        call: P
        priority: 50
        requires: {}
        shows: "no game try: passing the raise"
        establishes: { forcing: sign_off }
        negative_inference_weight: soft
```

*(The three trial priorities are 53 / 52.5 / 52 rather than all 53 on purpose:
`fast_decision` marks a decision unclear when two fit-1.000 candidates producing
different calls tie on priority, and that hands the seat to arbitration —
which `match_ben` does not run. My first draft tied them at 53 and the harness
reported a pass. Give sibling rungs distinct priorities.)*

**THE ANSWERING SEAT — this is the half that makes the trial bid worth
anything:**

```yaml
  - id: responder_answers_trial_bid
    description: "Responder accepts or declines opener's help-suit game try"
    expand_pairs:
      - { m: C, x: C }
      - { m: C, x: D }
      - { m: C, x: H }
      - { m: D, x: C }
      - { m: D, x: D }
      - { m: D, x: H }
    pattern: "1$m - P - 1H - P - 1S - P - 2S - P - 3$x - P - ?"
    rules:
      - id: rtb_accept_$x
        call: 4S
        priority: 55
        requires:
          any_of:
            - suits: { $x: [0, 2] }
              evals: { total_points: [8, 40] }
            - evals: { "top_honour($x)": [1, 1], total_points: [8, 40] }
            - evals: { total_points: [10, 40] }
        shows: "accepting the game try: help in $x, or a maximum raise"
        establishes: { forcing: sign_off, agreed_suit: S }
      - id: rtb_decline_$x
        call: 3S
        priority: 50
        requires: {}
        shows: "declining the game try: no help in $x and a minimum raise"
        establishes: { forcing: sign_off, agreed_suit: S }
        negative_inference_weight: soft
```

**What it endangers.** The trial context has specificity 1009 and takes 3C, 3D,
3H, 4S and P away from `general_uncontested_continuation` at this node.
Priced downward as well as upward: `uc_raise_S3` (31) and `uc_raise_S4` (32) are
what it replaces, and a raise by level is a strictly worse description than
naming the suit where the values are needed; `uc_rebid_C3` (27) and `uc_new_D3`
(27) lose 3C/3D here, and `otr_pass` with `requires: {}` plus `otr_game_4S`'s
bare 19+ band mean neither the pass seat nor the game seat can be starved.
`uc_pass` (18) is displaced by `otr_pass` at the same meaning. The answering
context likewise carries `rtb_decline_$x` at `requires: {}`.

**VERIFIED.** N bids 3C (fit 1.000, prio 53); S with `QT75.AT42.QT5.97` — a
doubleton club, i.e. a ruffing value — accepts with 4S (fit 1.000, prio 55).
Rolled out: `1C - 1H - 1S - 2S - 3C - 4S`, **ten tricks**. Table A goes from
3S (+170) to **4S (+420)**.

**Honest accounting of the board.** Board 426's -11 was lost at *table B*, to a
balancing double (`ballow_X`) of 2S that turned +140 into +670 for the other
side — a competitive defect, A's territory. The trial bid gains about 250 points
at table A, i.e. roughly a third of the margin. I am proposing it anyway,
because it is the largest missing agreement in my discipline anywhere in this
dossier and this is the board that exposes it.

**TEMPLATE — the biggest one in this part.** The identical three-rung idea goes
into:
* `responder_rebid_after_1M_raise` (`1$M - P - 2$M - P - ?`, `expand: { M: [H, S] }`)
  with the three non-trump suits — this is the canonical 1M-2M trial bid and it
  is simply absent; and its answering context
  `"1$M - P - 2$M - P - 3$x - P - ?"` alongside the existing
  `responder_over_game_try`, which today answers only the 3M raise;
* `responder_rebid_after_raise` (`1$m - 1$M - 2$M`), opener's game try after
  raising responder's major;
* `opener_after_limit_raise` (`1$M - 3$M`), where 3NT / four-of-a-minor as a
  "shall we?" is the same conversation one level up.

Counting the contexts: about **10 trial contexts × 3 rungs + 10 answering
contexts × 2 rungs ≈ 50 rules from one agreement**, in a subject that today has
**zero**.

---

## Board 436 — margin -11

**Seat/call:** table A call 4, N **passes** 1H on `KJ9863.J8.T.8654` — a
six-card spade suit and 5 HCP. `r1H_pass` requires `hcp: [0, 5]` and fits 1.000;
`r1H_1S` requires 6+ and fits 0.800. `r1H_pass` fires on **2 tables at mean
-6.50**.

The file already knows this is wrong and fixed it one context along:
`r1m_1H` carries an explicit second branch — *"a SIX-card major answers a minor
opening on any values: passing 1D with eight hearts and a diamond void is not a
style choice"* — with `hcp: [3, 40]` on a six-card suit. `resp_1H` and `resp_1S`
never got it. Pure sibling gap.

**The missing agreement.** A six-card spade suit answers 1H on any values.

### YAML — into the existing context `resp_1H` (and its `resp_1S` twin)

```yaml
      - id: r1H_1S_sixcard
        call: 1S
        priority: 71
        requires: { suits: { S: [6, 13] }, hcp: [3, 5] }
        shows: "a six-card spade suit answers 1H on any values: 3-5 HCP"
        establishes: { forcing: one_round }
```

**THE ANSWERING SEAT.** 1S is `forcing: one_round` and the seat that answers it
— `opener_rebid_1H_1S`, 11 rules — already exists. Checked in the rollout: opener
rebids 2D and the auction lands correctly.

**What it endangers.**
* `r1H_1S` (72) — one point higher in priority and 6-40 HCP, so it keeps every
  hand it has today; the new rung is strictly the band below it, and the two
  cannot both fit.
* `r1H_pass` (15) — the rung being displaced, and only for hands with six
  spades. Verified: `KJ98.J83.T2.8654` (four spades, 4 HCP) still bids 2H /
  passes as before, at fit 1.000.
* `r1H_single_raise` (60), `r1H_1NT` (40) — both require heart support or deny
  four spades; untouched.
* 1S is already covered by `r1H_1S`, so **no code fallback is deleted**.

**VERIFIED and the board is recovered.** N bids 1S at fit 1.000 / prio 71.
Rolled out: `1H - 1S - 2D - 2S - 4S`, **eleven tricks**. Table A goes from
1H-making-nine (+140) to **4S (+650)**; the board's -11 goes to zero.

**TEMPLATE.** `resp_1H` gets the 1S rung; `resp_1S` needs the mirror question
asked (there the cheapest six-card suit response is 2H/2C/2D, so the rung is
`hcp: [3, 5], suits: { $X: [6, 13] }` at the two level and it wants its own
`when: { cheapest_in_suit: true }`). Also `resp_1m`'s **spade** branch already
has it while `r1C_1D` does not. Four rules, and the grep that finds the rest is
"which responding rungs have an HCP floor with no six-card-suit escape".

---

## Board 437 — margin -11

**Seat/call:** table B call 12, E **passes** partner's quantitative 4NT holding
`A952.QT54.K4.Q87` — eleven points opposite a **2C opener**. `qa_pass` fires on
**6 tables at mean -5.50**; `qa_6NT` requires 16 HCP, a floor that is correct
opposite a 15-17 notrump and meaningless opposite 22+. We stopped in 4NT with
6NT cold.

This is the DECISIONS open item "`2C - 2NT` positive-response continuations have
no landing ladder" and "after a 2C opening, partner's shown minimum is ZERO by
construction" in one board: the arithmetic that should decide it (22 + 11 = 33)
is unavailable to every `rule_of_26` gate in the 2C tree.

**The missing agreement.** After 2C and a balanced positive, the combined count
is known to within a point or two: eight or nine is 3NT, ten invites, eleven or
more is the slam — and the invitation must be accepted by a hand that has
already promised 22.

### YAML — two new contexts

```yaml
  - id: responder_2C_positive_2NT_continuation
    description: "Responder after 2C - 2NT (balanced positive) and opener's suit rebid"
    pattern: "2C - P - 2NT - P - bid - P - ?"
    rules:
      - id: r2cp_6NT
        call: 6NT
        priority: 58
        requires: { hcp: [11, 40], evals: { controls: [3, 12], semi_balanced: [1, 1] } }
        shows: "eleven opposite a 2C opener and a positive: 33+ combined, bidding the slam"
        establishes: { forcing: sign_off }
      - id: r2cp_4NT
        call: 4NT
        priority: 57
        requires: { hcp: [9, 10], evals: { semi_balanced: [1, 1] } }
        shows: "quantitative: nine or ten opposite the 2C opener, inviting the slam"
        establishes: { forcing: invitational }
        alertable: true
      - id: r2cp_3NT
        call: 3NT
        priority: 56
        requires: { hcp: [0, 8] }
        shows: "the minimum positive: nine tricks opposite the 2C opener"
        establishes: { forcing: sign_off }
      - id: r2cp_floor_3NT
        call: 3NT
        priority: 25
        requires: {}
        shows: "no better description opposite the 2C opener: 3NT"
        establishes: { forcing: sign_off }
        negative_inference_weight: soft

  - id: opener_2C_accepts_quant
    description: "The 2C opener answers the quantitative 4NT after 2C - 2NT"
    pattern: "2C - P - 2NT - P - bid - P - 4NT - P - ?"
    rules:
      - id: q2c_6NT
        call: 6NT
        priority: 40
        requires: { hcp: [23, 40] }
        shows: "accepting: 23+ opposite the eight-plus positive"
        establishes: { forcing: sign_off }
      - id: q2c_pass
        call: P
        priority: 30
        requires: {}
        shows: "declining: a bare 22 for the 2C opening"
        establishes: { forcing: sign_off }
        negative_inference_weight: soft
```

**What it endangers.** Specificity 1007 / 1011, so these own 3NT, 4NT and 6NT at
those nodes and nothing else — the natural suit calls (`gf_new_3$X`, the raises,
the cue and keycard machinery) still come from their own contexts and were
checked in the candidate list. Rungs displaced: `gf_3NT` (34, 22 tables, mean
-0.95) loses 3NT here, which is exactly the intent — its `hcp: [0, 17]` band
cannot tell 8 from 15 opposite a 22-count; `qr3_4NT_quant` (39) and `qa_pass`
(30) lose this node to a ladder that counts from the right base.
`r2cp_floor_3NT` and `q2c_pass` both carry `requires: {}` so neither seat can be
starved.

**VERIFIED and the board is recovered.** E bids 6NT at fit 1.000 / prio 58.
Rolled out: `2C - 2NT - 3D - 6NT`, twelve tricks. Table B goes from 4NT (+490)
to **6NT (+990)**; the board's -11 goes to zero.

**TEMPLATE.** The same base-22 arithmetic belongs on every 2C continuation:
`r2c_after_2NT` (2C-2D-2NT systems-on, which has 3NT at a bare `not 4-card
major` and nothing above), `r2c_2NT_stayman_reply`, `r2c_after_stayman_reply`
and `r2c_after_transfer_completed`. About five contexts × four rungs, and it is
the cheapest way to make the 2C tree — `open_2C` replicates at **-7.44 / -6.58**
and has been deferred four rounds — bid its own hands.

---

## Board 449 — margin -11

**Seat/call:** table B call 12, E bids **4NT** on `AQ9532.A72.3.A74` over
partner's raise to game after a long constructive auction
(`1S - 2D - 2S - 3D - 3S - 4S`); `gr_rkc_S`, fit 1.000, prio 46. We play 6S for
eleven tricks. Denominator first: `gr_rkc_S` fires on **9 tables at mean +0.22**
and `gr_rkc_H` on **7 at mean -2.86** — the family is roughly break-even, which
is why DECISIONS records that *no gate on it has survived* (`keycards >= 3`
measured -17 held out and deleted three cold slams).

So I am not proposing a gate. I am proposing the **trick-currency rung above
it**, which is the one form of this that has never been tried:

**The missing agreement.** Losing-trick count, not points: partner's raise to
game is about seven losers, so opposite it a six-loser hand has eleven tricks
and a five-loser hand has twelve. Six losers passes; five asks.

### YAML — into the existing context `slam_try_over_game_raise`

```yaml
      - id: gr_losers_pass_$M
        call: P
        priority: 47
        when: { partner_last_suit: $M, my_suit: $M }
        requires: { evals: { ltc: [6, 13] } }
        shows: "six or more losers opposite the raise to game: eleven tricks, not twelve"
        establishes: { forcing: sign_off, agreed_suit: $M }
      - id: gr_pass_floor_$M
        call: P
        priority: 8.5
        requires: {}
        shows: "nothing more to say over partner's game raise"
        establishes: { forcing: sign_off }
        negative_inference_weight: soft
```

The second rung is **not optional** and is the round-15 lesson made concrete:
adding a P rung deletes the code fallback for P in every seat this context's
`when` reaches, so a five-loser hand that fails the first rung would have *no
pass candidate at all*. `gr_pass_floor_$M` restores it unconditionally.

**THE ANSWERING SEAT.** A pass ends the auction; none is owed.

**What it endangers.**
* `gr_rkc_$M` (46) and `gr_rkc_general_$M` (45) — the two rungs below. Verified
  that a five-loser hand still asks: `AKQ932.A72.3.AK4` at the identical node
  bids 4NT at fit 1.000 while `gr_losers_pass_S` soft-misses at 0.057.
* The code fallback pass (prio 8) at this node — replaced by
  `gr_pass_floor_$M` at 8.5 with identical, unconditional behaviour.
* Nothing else lives in this context.

**VERIFIED and the board is recovered.** E passes at fit 1.000 / prio 47.
Rolled out: `1S - 2D - 2S - 3D - 3S - 4S - P`, eleven tricks. Table B goes from
6S-down-one (+50 to them) to **4S (+450 to us)**; the board's -11 goes to zero.

**This is the riskiest proposal in my slice and I want that on the record.**
It is the one place where I am pushing on a population that DECISIONS says
resists every gate, the LTC threshold is a bright line drawn on textbook
arithmetic rather than on this corpus, and `gr_rkc_S`'s +0.22 mean means real
winners live inside the band I am outranking. **Measure it as its own
experiment**, and split the result by suit — `gr_rkc_H` (-2.86) and `gr_rkc_S`
(+0.22) do not behave alike.

**TEMPLATE.** Already `expand: { M: [H, S] }` (4 rules). The same
losers-not-points idea is the honest form of round 17's reverted
`gr_rkc_tricks_$M` and belongs equally on `gst_rkc_$X` in `general_slam_try`,
whose control floor is a point of sibling inconsistency (see board 59).

---

## Board 485 — margin -11

**Seat/call:** table A call 3, N passes their 5H sacrifice over our 4S opening
(`ch_pass`, fit 1.000; `ch_sac_X` fits 0.011). **Purely competitive** — a
preempt, a sacrifice and a decision whether to double it.

What I checked: the seat has exactly **two** candidates. `ch_sac_X` requires
"quick tricks, no trump length" and N holds `5.A754.KJ8652.K9` — four hearts, so
the trump-length denial is what fails, correctly. The whole conversation after
our 4S opening consists of one rule.

**Best constructive-discipline observation.** `resp_preempt_S` (six rules) and
the 4-level opening have no **constructive** continuation at all: after
`P - 4S - (5H)` our side's only vocabulary is pass or a sacrifice double. The
constructive counterpart — partner of a preemptor with a fit and controls
deciding between defending and bidding on — is the same zero-rule family as the
control-showing raise (board 305).

**VERDICT: NOTHING-WRONG (competitive).**

---

## Appendix — what I would ship first, and in what order

Ordered by (recovered IMPs in this dossier) × (confidence that the rung is safe
off-corpus), with the answering seats bundled where they belong:

1. **The cue-raise answering family** (board 559). Five unanswered cue raises,
   ~40 rules, and the seat currently passes a one-round force to a generic
   raise. Highest yield per idea in the part.
2. **The trial-bid family** (board 426). Zero rules today, ~50 from one
   agreement, and it is the convention round 17 named first.
3. **The four splinters** (443 opener, 318 responder-over-second-suit, 105
   Stayman, 559 over the cue raise) with their four answering contexts. Three of
   four recover their board outright.
4. **The band-against-what-partner-promised sweep** (967, 437, 479). Three
   boards recovered, and `rrevd_3NT` never firing in 1000 boards is a
   grep-able signature for the rest.
5. **The sibling gaps** (222 `rmr_newsuit_$oM`, 436 `r1H_1S_sixcard`, 925
   Stayman-doubled). Small, cheap, each recovers its board.
6. **Ceilings** (185 Jacoby, 614 jump rebid). Right bridge, neither recovers its
   board; ship them for the description, not for the number, and say so.
7. **Measure separately:** 449's `gr_losers_pass_$M`, 59's control-floor sibling
   repair, and 762's 6-5 opening (which must not ship without the
   `1m - 1NT - 2M` responder ladder).

Three things I would tell whoever implements this:

* **Give sibling rungs distinct priorities.** Two fit-1.000 candidates producing
  different calls at equal priority make `fast_decision` report `is_clear=False`,
  and `match_ben` never runs arbitration, so the result is whatever the blended
  score happens to like.
* **Every new `P` rung needs an unconditional `P` floor beside it**, because a
  rung deletes the code fallback for its call. Board 449's proposal ships two
  rules for that reason and one of them does nothing except exist.
* **Verify with `use_arbitration: False`.** `choose_bid` defaults to `True`;
  the match does not. I lost one reading to this and it looked like a bad rule.
