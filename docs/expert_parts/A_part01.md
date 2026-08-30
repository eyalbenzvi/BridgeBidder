# Expert A — competitive / matchpoint duplicate — dossier part 1 (38 boards)

<!-- SUMMARY-PLACEHOLDER -->

## Board 173 — margin -15

**Seat/call that went wrong.** Table A, call 3, **N bids 4C** (`awj_4_SC`) over
`1S - 3C(partner) - P`, holding `J.AQ953.KJ52.A54` (15 HCP, stiff spade).  We
buried a nine-card heart fit worth eleven tricks and let E play 4S; BEN's N/S
bid 4H at the other table for +650.  (S's 3C weak jump on `9.KT42.74.KQJT32`
is defensible and BEN's pass is a style call — I do not indict it; the loss is
manufactured one call later.)

**The missing agreement (one sentence).** After partner's weak jump overcall a
new suit by advancer is natural and forcing for one round — `advance_weak_jump_overcall`
has exactly three rungs (5m, 4m, 3NT) and no way to say "I have my own suit",
so a 15-count with AQ953 must raise the barrage.

**EXACT YAML.**  Two rungs into the existing context (`src/bridgebidder/systems/two_over_one.yaml`,
context `advance_weak_jump_overcall`, after `awj_3NT_$o$j`):

```yaml
      - id: awj_newH_$o$j
        call: 3H
        priority: 56.5
        when: { unbid_suit: H }
        requires: { hcp: [12, 21], suits: { H: [5, 13] } }
        shows: "natural and forcing: a real five-card heart suit and game values"
        establishes: { forcing: one_round }
      - id: awj_newS_$o$j
        call: 3S
        priority: 56.5
        when: { unbid_suit: S }
        requires: { hcp: [12, 21], suits: { S: [5, 13] } }
        shows: "natural and forcing: a real five-card spade suit and game values"
        establishes: { forcing: one_round }
```

**THE ANSWERING SEAT** (mandatory — the new suit is a force).  New context,
placed immediately after `advance_weak_jump_overcall`:

```yaml
  - id: advance_wj_new_suit_reply
    description: "Weak jump overcaller answers advancer's forcing new suit"
    expand_pairs:
      - { o: S, j: C, M: H }
      - { o: S, j: D, M: H }
      - { o: H, j: C, M: S }
      - { o: H, j: D, M: S }
      - { o: D, j: C, M: H }
      - { o: D, j: C, M: S }
    pattern: "1$o - 3$j - P - 3$M - P - ?"
    rules:
      - id: awjr_raise_$o$j$M
        call: 4$M
        priority: 62
        requires: { suits: { $M: [3, 13] } }
        shows: "three-card support for partner's forcing major"
        establishes: { forcing: sign_off, agreed_suit: $M }
      - id: awjr_3NT_$o$j$M
        call: 3NT
        priority: 60
        requires: { suits: { $M: [0, 2] }, features: [ "stopper($o)" ] }
        shows: "no fit for the major but their suit stopped: nine tricks"
        establishes: { forcing: sign_off }
      - id: awjr_rebid_$o$j$M
        call: 4$j
        priority: 58
        requires: { suits: { $M: [0, 2], $j: [6, 13] } }
        shows: "no fit and no stopper: back to my own long suit"
        establishes: { forcing: sign_off, agreed_suit: $j }
```

**WHAT IT ENDANGERS** (every rung in `advance_weak_jump_overcall`, above and below):

* `awj_3NT_$o$j` (57, above mine) — untouched: it still wins whenever it fits
  >= 0.9, and with a genuine stopper and a flat 14+ nine tricks in notrump is
  the better description than a forcing three of a major.
* `awj_5_$o$j` (56, **below** mine) — a 19+ total-point hand with a five-card
  major now bids the major first; that is better bridge, because 5C on a
  4-loser major-suit hand is exactly the contract we are trying not to reach,
  and 5m is still reached through the answering ladder.
* `awj_4_$o$j` (55, **below** mine) — the barrage raise loses only hands with a
  genuine five-card major AND 12+ HCP; on those the fit we hold is the major,
  not the minor, and the raise pre-empts our own side.
* `uc_new_H3` / `uc_new_H3_hi` (27/27.5) — these already produce 3H at fit 1.00
  and are simply outranked as they are today; my rung makes the same call with
  a description attached.
* Fallback deletion (round-15 mechanism): my `when` reaches only seats where the
  major is unbid, and the 3M call in this context was previously produced by
  `uc_new_*3`, i.e. it was already covered by a rule — so no code fallback is
  removed here.

**VERIFIED.**  Traced through the patched loader:
N's 3H fires `awj_newH_SC` at fit 1.000 / prio 56.5, beating `awj_4_SC`
(fit 1.000 / 55); S then answers `4H` via `awjr_raise_SCH` at fit 1.000 / 62.
Regression traced: with `J4.AQ54.KJ52.A54` (only four hearts) the advance is
still `4C` (`awj_newH_SC` drops to fit 0.349).  The `awjr_3NT` branch is the
one rung I did not see fire on a constructed hand (both doubleton examples took
`4C`); it is harmless but count it UNTESTED.

**TEMPLATE.**  The two advancer rungs live inside the existing
`expand_pairs` over `{o, j}` (5 contexts) and are guarded by `when: { unbid_suit }`
so the heart rung is dead where hearts are theirs.  Do **not** add `M` to that
context's `expand_pairs` — `(D,C,H)` and `(D,C,S)` would produce two contexts
with the identical pattern `1D - 3C - P - ?` and the later one would be dead.
The answering context takes the 6-way `{o, j, M}` `expand_pairs` shown above.

## Board 439 — margin -15

**Seat/call that went wrong.** Table A, call 1, **N passes** (`v1NT_pass`) over
W's 1NT holding `T9743.5.Q8.AKQ53` — 5-1-2-5, 11 HCP, both black suits.  BEN's
N/S bid 2S at the other table and reached 4S for eleven tricks; we defended 3D.

**The missing agreement (one sentence).** Over their 1NT a **two-suited** hand
is worth a natural two-level overcall on shape alone — every suit rung in
`defense_vs_1NT` carries `features: [good_suit(X)]`, so a 5-5 eleven-count with
a ragged major has no call at all and the seat is starved into `v1NT_pass`.

**EXACT YAML.**  Two rungs into `defense_vs_1NT`, after `v1NT_2S`:

```yaml
      - id: v1NT_2H_5_5
        call: 2H
        priority: 59
        requires:
          hcp: [8, 15]
          suits: { H: [5, 13] }
          any_of: [ { suits: { S: [5, 13] } }, { suits: { D: [5, 13] } }, { suits: { C: [5, 13] } } ]
        shows: "two-suited overcall of 1NT: five hearts and a second five-card suit, 8-15"
        establishes: { forcing: non_forcing }
      - id: v1NT_2S_5_5
        call: 2S
        priority: 59
        requires:
          hcp: [8, 15]
          suits: { S: [5, 13] }
          any_of: [ { suits: { H: [5, 13] } }, { suits: { D: [5, 13] } }, { suits: { C: [5, 13] } } ]
        shows: "two-suited overcall of 1NT: five spades and a second five-card suit, 8-15"
        establishes: { forcing: non_forcing }
```

**THE ANSWERING SEAT.**  Not a force — the call is natural and non-forcing, so
no new context is owed.  I traced the advance anyway: S with `AKJ8.K8632..T864`
raises to **4S** through `uc_raise_S4` (fit 1.000, prio 32), so the conversation
already closes.

**WHAT IT ENDANGERS** (all of `defense_vs_1NT`):

* `v1NT_X` (70) and `v1NT_2H`/`v1NT_2S` (61), `v1NT_2C`/`v1NT_2D` (60) — all
  ABOVE my 59, so a 15-count still doubles and a genuine good six-card suit
  still takes the higher-priority natural rung.
* `v1NT_pass` (30, **below** mine) — this is the only rung my rungs subtract
  from, and only on 8-15 with 5-5.  At matchpoints passing 1NT with two
  five-card suits is the losing action: we own a partscore and there is no
  second chance, because the auction after a 1NT opening dies fast.
* No code fallback is deleted: 2H and 2S are already covered in this context by
  `v1NT_2H`/`v1NT_2S`.
* Note this is NOT a convention (excluded by the brief) — it is the natural
  overcall with the suit-quality gate relaxed for two-suited shape only.

**VERIFIED.**  `2S` fires `v1NT_2S_5_5` at fit 1.000 / prio 59, beating
`v1NT_pass` (1.000 / 30); `v1NT_2S` itself sits at fit 0.200.  Regressions
traced: `T974.K52.Q83.J65` still passes (my rungs at fit 0.002), and
`AQJ973.52.Q83.65` still bids 2S through `v1NT_2S` (fit 1.000 / 61).

**TEMPLATE.**  Do **not** put `expand: { M: [H, S] }` on `defense_vs_1NT` — the
context has a bare `pattern: "1NT - ?"` and expanding it would create two
contexts with the identical pattern, the second of which is dead by file order.
Write the two rungs out, as above.  The same agreement should later be expanded
to the balancing seat over 1NT (`1NT - P - P - ?`) with the same shape gate and
a 6-14 HCP band.

## Board 951 — margin -15

**Seat/call that went wrong.** Table B, call 10, **E bids 4C** (`balhigh_new_C4`)
on `AT7.QJ92.A.KJ964` after `P 1D X XX 1H 1NT 2H 3NT P P`.  Doubled, five off,
**-1100**.  At table A the same 3NT went **one down**, so passing was worth +50
to us and the whole 15 IMPs is this one call.  (Table A's N pass over 1H is a
correct forcing pass and S's 3NT is a soft-miss at fit 0.409 — a separate,
smaller matter; I am indicting the -1100.)

**The missing agreement (one sentence).** When the opponents bid notrump and it
is passed round to me, two quick tricks are a reason to **defend**, not to run
to the four level — `general_balancing_high` has a full natural four-level suit
ladder at priority 28 and nothing that says "this one we beat".

**EXACT YAML.**  One rung into `general_balancing_high`, immediately before
`balhigh_pass`:

```yaml
      - id: balhigh_defend_their_nt
        call: P
        priority: 28.5
        when: { standing_bid_strain: [NT], we_hold_contract: false }
        requires:
          evals: { quick_tricks: [2, 13] }
        shows: "they bid notrump and it is passed round to me with two quick tricks: defend, do not run to the four level"
        establishes: { forcing: sign_off }
        negative_inference_weight: soft
```

**THE ANSWERING SEAT.**  None owed — the call is a pass that ends the auction.

**WHAT IT ENDANGERS** (everything in `general_balancing_high` my 28.5 can outrank):

* `balhigh_new_C4/D4/H4/S4` (28, **below**) — the target.  Whole-corpus
  denominator run before accusing: `balhigh_new_C4` fires **once** (-15),
  `balhigh_new_S4` once (+6), the other two never.  Two firings is not a
  statistical case, so the case is the bridge: a five-card suit and 14 total
  points opposite a partner who has shown nothing is not a four-level action
  over a game the opponents chose freely.
* `balhigh_new_*1/2/3` (25/26/27, below) — these can only be outranked when the
  standing bid is notrump, and a one-, two- or three-level call cannot be
  cheapest under a standing 3NT, so in practice they are untouched.
* `balhigh_pass` (21, below) — same call, so no behaviour changes; mine simply
  attaches a reason.
* `balhigh_raise_*3/4` (31/32), `balhigh_rebid_*4` (29), `balhigh_reopen_X` (41)
  — all **above** 28.5, so a genuine fit, a six-card rebid or a 16+ reopening
  double still wins.  That is the right order: with a fit you compete, with two
  aces and no fit you defend.
* Fallback: `P` in this context is already covered by `balhigh_pass`, so no code
  fallback disappears.

**VERIFIED.**  Before: `4C` via `balhigh_new_C4` (fit 1.000 / 28).  After: `P`
via `balhigh_defend_their_nt` (fit 1.000 / 28.5).  Regression traced with the
same auction and `72.QJ92.2.KQJT98` (half a quick trick): my rung falls to fit
0.329 and does not suppress the four-level bid.

**TEMPLATE.**  No suit templating — the rung is strain-agnostic by construction.
The same agreement should be **expanded to the low balancing context**
`general_balancing_low` as `ballow_defend_their_nt` (there the standing bid is
1NT or 2NT and the quick-trick floor should be 2.5, because balancing over 1NT
is much more often right), and to `general_competitive_high` for the direct seat
over their 3NT.

## Board 305 — margin -14

**Seat/call that went wrong.** Table B, call 2, **W passes** (`rp3_D_pass`) over
partner's `3D` preempt holding `A.KQT982.A963.92` — four-card support, a
singleton, eleven trumps between the hands.  BEN bids 5D, which makes eleven
tricks (+600).  Instead we passed, N reopened with a double, S bid 4S and W then
invented `5H` (`ch_new_H5`) for -500.  Fixing call 2 removes the whole auction.
(Table A's pass over 5D is correct — 5D makes, so BEN's double would have been
-650; I do not indict `ch_pass` there.)

**The missing agreement (one sentence).** **The pre-emptive raise of partner's
preempt to the level of the fit does not exist anywhere in the file** — all four
`resp_preempt_*` contexts contain only a forcing new suit (15+), a keycard ask,
a game bid gated on `stopper(partner)` and a pass, so a hand with four-card
support and a shortage has no raise at all and passes a 3D preempt out.

**EXACT YAML.**  One rung into `resp_preempt_D`, before `rp3_D_pass`:

```yaml
      - id: rp3_D_lott5
        call: 5D
        priority: 63
        requires:
          suits: { D: [4, 13] }
          evals: { "lott_total_trumps(D)": [11, 26], singleton_or_void: [1, 1] }
        shows: "the Law opposite the preempt: eleven trumps and a shortage, so eleven tricks - bid them before they find their major"
        establishes: { forcing: sign_off, agreed_suit: D }
```

**THE ANSWERING SEAT.**  None owed — `forcing: sign_off`, the raise ends our
side's constructive auction by design.  It is a pre-empt, not a question.

**WHAT IT ENDANGERS** (every rung in `resp_preempt_D`):

* `rp3_D_rkc` (66) and `rp3_D_game` (64), **above** mine — a 19-count with four
  keycards still asks, and a 15+ hand with every side suit stopped still bids
  3NT.  Verified: `AQ3.KQ8.A93.K942` still takes 3NT at fit 1.000.
* `rp3_D_C/H/S` (62, **below** mine) — these all carry `D: [0, 2]`, so they can
  never fit a hand with four-card support; the ordering is moot in practice, and
  where it is not, a four-card fit for a seven-card suit outranks a five-card
  suit of my own.
* `rp3_D_pass` (40, **below**) — the target.  Passing a preempt out with eleven
  trumps and a singleton is how the opponents get to play a comfortable major
  partscore or game; this is the single most valuable thing a preempt responder
  ever does.
* `uc_raise_D4` (27) and `uc_minor_game_5D` (28) from the generic toolkit are
  outranked; they fit 0.055 and 0.000 on this hand and were never the reading.
* **Fallback note:** this rung covers `5D` in a seat where it was previously
  covered only by `uc_minor_game_5D`, i.e. already covered — no code fallback is
  deleted.

**VERIFIED.**  Before: `P` (`rp3_D_pass`, fit 1.000 / 40).  After: `5D`
(`rp3_D_lott5`, fit 1.000 / 63).  Both regressions traced (three-card support
with no shortage still passes; the strong balanced hand still bids 3NT).

**TEMPLATE.**  The four `resp_preempt_*` contexts are separate contexts with no
`expand`, so write the rung out four times with explicit ids:

* `rp3_C_lott5` — `call: 5C`, `suits: { C: [4, 13] }`, `lott_total_trumps(C) >= 11`;
* `rp3_D_lott5` — as above;
* `rp3_H_lott4` — `call: 4H`, `suits: { H: [3, 13] }`, `lott_total_trumps(H) >= 10`,
  `singleton_or_void: [1, 1]`, priority 63 (below `rp3_H_game`'s 64 so the
  constructive 15-count keeps its reading);
* `rp3_S_lott4` — the spade twin.

It should also be expanded to the **contested** version — `3$W - act - ?` and
`3$W - P - act - ?` — where the same Law raise is worth more, and to the
four-level preempt responses.  That is the second half of the agreement and is
where most of its value is.

