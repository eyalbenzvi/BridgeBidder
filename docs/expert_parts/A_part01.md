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

## Board 614 — NOTHING-WRONG (competitive lens)

**Verdict.** The board is **purely constructive** and belongs to the other
reviewer: table B, call 5, W rebids `2C` (`ob_rebid_2C`) on
`5..KQ6.AQJ986532` — an eight-card club suit with a void — and 3NT is reached
instead of 6C/7C.  Nothing in that auction is contested.

**What I checked on the competitive side.**  Table A is four of our passes
against BEN's uncontested 1C-1S-3C-3H-4C-4NT-5S-7NT.  The only competitive seat
worth a second look is S at call 4 (`J87.JT854.T52.K4`, five hearts opposite N's
`Q642.Q932.9874.T` — a nine-card heart fit) after `P 1C P 1S`: a sandwich-seat
2H would find the fit and the sacrifice.  **I reject it**: we are vulnerable
against not, S is a passed hand with 5 HCP and JT854, and the fit is worth four
tricks double-dummy — 2H doubled is -800 against their -520/-1520.  Our passes
are right; the 15 IMPs are entirely their bidding and our own missed slam at the
other table.  `sandwich_seat` and `general_competitive_low` are both correctly
silent here.

**NOTHING-WRONG** from the competitive/matchpoint discipline.

## Board 925 — margin -14

**Seat/call that went wrong.** Table A, call 7, **N passes** (`xd_pass`) after
`1NT - P - 2C - P - 2D - X`, holding `T983.K98.T5.AJ72`.  **2D doubled, four
tricks, -1100**, on a board where the other table played 2NT for -100.

**The missing agreement (one sentence).** A double of opener's **artificial** 2D
denial is not a contract to sit for — the Stayman bidder has 8+ HCP by
definition and simply continues with the invitation he started, but the file has
no context for `1NT - P - 2C - P - 2D - X - ?`, so `general_their_double`'s
"sitting for their double: no better spot to run to" (`xd_pass`, priority 18,
fit 1.00) owns the seat by construction.

**EXACT YAML.**  A new context, placed immediately after
`stayman_invite_accept_2D`:

```yaml
  - id: stayman_2D_doubled
    description: "They double opener's artificial 2D denial: the invitation still has to be made"
    pattern: "1NT - P - 2C - P - 2D - X - ?"
    rules:
      - id: s2Dx_3NT
        call: 3NT
        priority: 61
        requires: { hcp: [10, 15] }
        shows: "game values opposite the notrump and no major fit: nine tricks, their double changes nothing"
        establishes: { forcing: sign_off }
      - id: s2Dx_2NT
        call: 2NT
        priority: 60
        requires: { hcp: [8, 9] }
        shows: "the invitation I started Stayman with: 8-9 balanced, no major fit"
        establishes: { forcing: invitational }
```

**THE ANSWERING SEAT** (mandatory — `s2Dx_2NT` is an invitation, and the
existing acceptor `stayman_invite_accept_2D` has pattern
`1NT - P - 2C - P - 2D - P - 2NT - P - ?`, which the double no longer matches):

```yaml
  - id: stayman_invite_accept_2D_doubled
    description: "Opener over 2NT after 1NT - 2C - 2D doubled"
    pattern: "1NT - P - 2C - P - 2D - X - 2NT - P - ?"
    rules:
      - id: stmix_2D_pass
        call: P
        priority: 60
        requires: { hcp: [15, 15] }
        shows: "declining the invite: minimum 1NT opener"
        establishes: { forcing: sign_off }
      - id: stmix_2D_3NT
        call: 3NT
        priority: 58
        requires: { hcp: [16, 17] }
        shows: "accepting the invite: 16-17"
        establishes: { forcing: sign_off }
```

**WHAT IT ENDANGERS.**  The new context is a *superset*: `general_their_double`
keeps contributing every candidate it did before (traced — `xd_pass`,
`xd_run_S2`, `xd_run_H2`, `xd_run_D3`, `xd_rebid_C3` are all still in the pool),
so nothing is shadowed away.  What my rungs outrank:

* `xd_pass` (18) — the target.  Nobody sits a double of a bid that shows no
  diamonds; there is no such thing as a good 2D contract here.
* `xd_run_S2` (25) / `xd_run_H2` (25) — a run to a five-card major.  `nt_stayman`
  requires *exactly* four cards in a major and denies five, so these can never
  be the right description of a Stayman bidder's hand; my rungs correctly outrank
  them.
* `xd_run_D3` (26) / `xd_rebid_C3` (34) — unreachable shapes for this seat, same
  argument.
* **Fallback deletion:** `2NT` in this seat was previously produced by the code
  fallback (fit 0.134 in the trace).  My rung replaces it with a described call
  in exactly the seat where the fallback was already the only 2NT — an
  improvement, not a subtraction, and `3NT` was not covered at all before.

**VERIFIED.**  Before: `P` (`xd_pass`, fit 1.000 / 18).  After: `2NT`
(`s2Dx_2NT`, fit 1.000 / 60), then S with `AK4.652.QJ4.KQ64` passes via
`stmix_2D_pass` (fit 1.000 / 60) — landing in exactly the 2NT-for-100 the other
table played, i.e. the board goes flat.  Also traced: an 11-count responder
takes `3NT` via `s2Dx_3NT`.

**TEMPLATE.**  The 2H and 2S replies are *natural*, so they do not take the same
rungs and must not be swept in with `expand: { R: [2D, 2H, 2S] }`.  What SHOULD
be templated is the species: every artificial reply in the file that can be
doubled needs a "the double does not change my plan" context —
`1NT - P - 2$T - X - ?` (transfers) already has `transfer_doubled`, and
`2C - P - 2D - X - ?` (the 2C waiting bid) has none.  Author the 2C-tree twin
with the same two rungs and the same answering seat.

## Board 59 — margin -13

**Seat/call that went wrong.** Table A, call 5, **N passes** (`cl_pass`) after
`1D - P - 1S - 2C(partner) - 2S`, holding `T82.T642.8.J9842` — five-card support
for partner's club overcall, a singleton in their first suit, and the opponents
have just announced an eight-card spade fit.  BEN bids 4C.  We passed and E/W
walked into 4S for eleven tricks, -650; 4C is at worst -500 doubled and the
board is a save, not a defeat.

**The missing agreement (one sentence).** **The Law of Total Tricks is
implemented for the majors only** — `cl_raise_lott3_$M`, `cl_raise_lott4_$M`,
`uc_raise_lott4_$M`, `ch_raise_lott4_$M`, `ballow_raise_lott4_$M`,
`balhigh_raise_lott4_$M` are every LOTT rule in the file and all of them are
`expand: { M: [H, S] }`, so a ten-card **minor** fit opposite a competitive
auction has no shape raise at any level.

**EXACT YAML.**  Two rungs into `general_competitive_low`, next to their major
twins (after `cl_raise_lott4_S`):

```yaml
      - id: cl_raise_lott4_C
        call: 4C
        priority: 32
        when: { partner_suit: C }
        requires:
          suits: { C: [4, 13] }
          evals: { "lott_total_trumps(C)": [10, 26], total_points: [0, 10], their_fit: [8, 26] }
        shows: "the Law at the four level in a minor: both sides have a fit and we hold ten-plus trumps, so bid to the level of the fit on shape alone"
        establishes: { forcing: non_forcing, agreed_suit: C }
      - id: cl_raise_lott4_D
        call: 4D
        priority: 32
        when: { partner_suit: D }
        requires:
          suits: { D: [4, 13] }
          evals: { "lott_total_trumps(D)": [10, 26], total_points: [0, 10], their_fit: [8, 26] }
        shows: "the Law at the four level in a minor: both sides have a fit and we hold ten-plus trumps, so bid to the level of the fit on shape alone"
        establishes: { forcing: non_forcing, agreed_suit: D }
```

Note this is **not** the do-not-re-propose item: the excluded change was
*freeing* `cl_raise_lott3_$M`'s `cheapest_in_suit` gate.  These are new
minor-suit siblings of the *four*-level rung, which carries no such gate and
which DECISIONS records at **+12**.

**THE ANSWERING SEAT.**  None owed — `forcing: non_forcing` and it is a
pre-empt/save, not a question.  The overcaller's onward seat is already
`general_competitive_high` / `general_their_double`, both authored.

**WHAT IT ENDANGERS** (rules in `general_competitive_low` producing 4C/4D or
outrankable at 32):

* `cl_raise_C4` / `cl_raise_D4` (27, **below**) — the constructive four-level
  raise, `11+ support points`.  My rung is capped at **10** total points, so the
  two are disjoint by construction and nothing is subtracted.
* `cl_raise_C3` / `cl_raise_C2` (31 / lower, below) — a 4+ card fit with 10
  total trumps AND a known enemy fit belongs at the level of the fit, not one
  below it; that is the entire content of the Law, and the `their_fit >= 8` gate
  (learned the hard way per the file's own comment) means it can only fire when
  the auction is genuinely two-sided.
* `cl_negative_X2` (33, **above**) — untouched; an 8+ HCP hand with an unbid
  major still doubles, which is right, because my rung tops out at 10 total
  points including distribution.
* `cl_pass` (20, below) — the target.
* Fallback: `4C`/`4D` in this context are already covered by `cl_raise_C4` /
  `cl_raise_D4`, so no code fallback is deleted.

**VERIFIED.**  Before: `P` (`cl_pass`, fit 1.000 / 20).  After: `4C`
(`cl_raise_lott4_C`, fit 1.000 / 32).  Two regressions traced: with the same
hand and no enemy fit (`1D - P - 1S - 2C - P`) the rung is not even offered
(the seat is `general_uncontested_continuation` and we still pass), and with
only three-card support (`T823.T642.8.J984`) it falls to fit 0.082 and we pass.

**TEMPLATE.**  This is the single most templatable agreement in my slice.  Add
the minor to **every** LOTT family: `expand: { m: [C, D] }`-style siblings in
`general_competitive_low` (done above), `general_competitive_high`
(`ch_raise_lott4_$m` at the five level, `their_fit >= 8`, 11 total trumps),
`general_balancing_low` / `general_balancing_high`, and
`general_uncontested_continuation` (`uc_raise_lott4_$m`, which is the +12 rung's
missing half).  That is roughly ten new rules from one agreement.

## Board 105 — NOTHING-WRONG (competitive lens)

**Verdict.** Constructive/slam board, and not mine: table B, call 6, W raises
Stayman's `2S` straight to `4S` (`stm_raise_4S`, fit 1.000 / 72) on
`KQ32.K4.8.AJ8643` — 13 HCP, a 4-4 spade fit, a singleton diamond and a
six-card club side suit, opposite a 15-17 notrump.  6S is cold and 4NT
(`stm_rkc_4NT`) is sitting there at fit 0.409.  That is a slam-try/ceiling
question for the constructive reviewer.

**What I checked on the competitive side.**  Every one of our ten calls at table
A is a pass that BEN also makes at 1.00 confidence, against an uncontested
1NT-2C-2S-3H-4C-4D-4NT-5S-6S auction.  The only seat with an argument is N at
call 3 (`T95.QJT3.J6432.7`, 5-4 in the reds, singleton club, **favourable**
vulnerability) over their 2C Stayman.  I checked whether the file has anything
there: **it has no defence to their 1NT-Stayman/transfer auctions at all** — no
context matches `1NT - P - 2C - ?` from the fourth seat, so the decision falls to
`general_competitive_low`.  That is a genuine structural hole and worth a round
of its own (a lead-directing double of Stayman, and a double of a transfer
showing the transferred-to suit).  On **this** hand it changes nothing: 4 HCP
with no five-card suit to direct a lead in is a pass at any vulnerability.

**NOTHING-WRONG** from the competitive/matchpoint discipline.

## Board 122 — margin -13

**Seat/call that went wrong.** Table A, call 4, **S passes** (`ch_pass`) after
`P - 1C - 1S(partner) - 4H`, holding `T973.K.QT83.AT86` — four-card support for
partner's one-level spade overcall, non-vulnerable against vulnerable.  BEN bids
4S.  4S is one down (-50); 4H made for **-620**.

**The missing agreement (one sentence).** Over their **pre-emptive leap to
game** the LOTT branch exists only with FIVE trumps (`ch_raise_lott_$M4`), and
the four-trump branch (`ch_raise_lott4_$M`) demands `their_fit >= 8`, which a
single opponent who has jumped unilaterally has not yet shown — so nine total
trumps at favourable vulnerability has no rung and the seat falls to the
catch-all pass.

**EXACT YAML.**  Two rungs into `general_competitive_high`, next to
`ch_raise_lott_$M4`:

```yaml
      - id: ch_raise_over_jump_H4
        call: 4H
        priority: 31.5
        when: { partner_suit: H, we_vulnerable: false, standing_bid_level: [4], their_last_bid_suit: true }
        requires:
          suits: { H: [4, 13] }
          evals: { "lott_total_trumps(H)": [9, 26], total_points: [6, 40] }
        shows: "they leapt to game to shut us out: with four trumps and nine combined we take the push rather than defend undoubled"
        establishes: { forcing: non_forcing, agreed_suit: H }
      - id: ch_raise_over_jump_S4
        call: 4S
        priority: 31.5
        when: { partner_suit: S, we_vulnerable: false, standing_bid_level: [4], their_last_bid_suit: true }
        requires:
          suits: { S: [4, 13] }
          evals: { "lott_total_trumps(S)": [9, 26], total_points: [6, 40] }
        shows: "they leapt to game to shut us out: with four trumps and nine combined we take the push rather than defend undoubled"
        establishes: { forcing: non_forcing, agreed_suit: S }
```

**THE ANSWERING SEAT.**  None owed — `non_forcing`, and the overcaller's next
seat is `general_their_double` / `general_competitive_high`, both authored.

**WHAT IT ENDANGERS** (everything in `general_competitive_high` at or below 31.5
that produces a four-level call):

* `ch_raise_lott_$M4`, `ch_raise_$M4`, `ch_raise_lott4_$M` (all **32**, above) —
  deliberately left above me, so a five-trump hand, an 11-point hand or a hand
  with a confirmed enemy fit keeps its more specific description.  Verified with
  `T9732.K.QT83.AT8`: `ch_raise_lott_S4` still wins the tie at 32.
* `ch_penalty_X` (38, above) — a hand with real defence still doubles.
* `ch_new_$X5` (28/28.5, **below**) — introducing a new suit at the FIVE level
  is a worse description than raising the fit we already have; the five level
  belongs to the opponents.
* `ch_pass` (22, below) — the target.
* Fallback: `4S`/`4H` are already covered here by three raise rungs each, so
  nothing is removed.

**VERIFIED.**  Before: `P` (`ch_pass`, fit 1.000 / 22).  After: `4S`
(`ch_raise_over_jump_S4`, fit 1.000 / 31.5).  Three regressions traced: three
trumps passes (fit 0.029), **vulnerable** passes (the `when` rules it out), and
five trumps still routes to the existing 32 rung.

**TEMPLATE.**  Written out for both majors above (no `expand` — the context has
none).  It should also be expanded (i) to the **minors** at the same level, with
the same nine-trump floor, and (ii) to their leap to **five** of a minor with a
`standing_bid_level: [5]` twin at the five level for eleven total trumps, which
is the same agreement one level up and is currently absent everywhere.

## Board 185 — NOTHING-WRONG (competitive lens)

**Verdict.** Constructive slam board.  Table B, call 6: W with
`A8.AJ97.AKQ.KJ86` (22 HCP) hears `1H - 2NT(Jacoby) - 3D(shortness)` and signs
off in `4H` through `jac_wasted_signoff` because the AKQ opposite the shown
diamond shortness reads as wasted — but the hand has 22 HCP and four aces, and
the wasted-value test has no strength ceiling on it.  That is the constructive
reviewer's ceiling species, not mine.

**What I checked on the competitive side.**  All nine of our table-A calls are
passes BEN also makes at 1.00 against an uncontested 1H-2NT-3D-3H-4C-4NT-5S-7H
auction; N has 3 HCP and S has 0.  The only competitive idea available is an
obstructive `3C` by N (`97.53.J873.Q9743`, five clubs, **favourable**
vulnerability) over their Jacoby 2NT, to steal the cue-bidding room — and I
note that the file has **no context at all for interfering over their strong
artificial responses** (`1$M - P - 2NT - ?` is decided by
`general_competitive_low`).  I do **not** propose it here: against a 22-count
opposite a 15-count it changes nothing but the size of the penalty, and a
three-HCP overcall at the three level is exactly the discipline failure this
project keeps paying for.

**NOTHING-WRONG** from the competitive/matchpoint discipline.

## Board 222 — NOTHING-WRONG (competitive lens)

**Verdict.** Constructive board.  Table B, call 3: E responds `1S` (`r1m_1S`,
fit 1.000 / 77) to partner's 1C on `AKQ832.AKJT.K72.` — 20 HCP, 6-4 in the
majors, a void.  A one-level response caps the hand and the auction died in 4S
missing a cold 6NT/6C.  The strong jump shift / reverse machinery is the
constructive reviewer's ground.

**What I checked on the competitive side.**  Every table-A call of ours is a
pass BEN also makes at 1.00, against an uncontested 1C-2S-3C-3S-3NT-6NT auction.
N holds `J9754.8732.T65.A` (5 HCP, 5-4 in the majors) **vulnerable against
vulnerable** and the only competitive idea on the board is a direct 1S overcall
over W's 1C.  I checked `overcalls_of_1C`: `oc1C_1S` is correctly not fitted
(five ragged spades and 5 HCP at unfavourable is a pass in any system), and BEN
passes at 1.00 too.  Nothing in `sandwich_seat`, `balancing_seat` or
`general_competitive_low` should have fired.

**NOTHING-WRONG** from the competitive/matchpoint discipline.

## Board 301 — margin -13

**Seat/call that went wrong.** Table B, call 4, **E bids 3NT** (`ch_nt3`) after
`1S - P - 1NT - 3C`, holding `AK732.A542.K5.K4` (17 HCP, 5-4 in the majors, K-x
in their suit).  3NT took seven tricks, **+200 to N/S**, where 4H (W has
`J9763` — a nine-card heart fit) makes eleven.

**The missing agreement (one sentence).** Over their pre-empt, opener's **second
suit** has no rung: `ch_new_H3` demands a FIVE-card suit, so a 5-4 hand can only
choose between rebidding its own suit and 3NT, and `ch_nt3` at priority 29 —
whose "stopper in their suit" gate is `weakest_their_stopper`, the evaluator
that does not gate — takes every one of them.

**EXACT YAML.**  Two rungs into `general_competitive_high`, immediately before
`ch_nt3`:

```yaml
      - id: ch_second_major_H3
        call: 3H
        priority: 29.5
        when: { unbid_suit: H, cheapest_in_suit: true, i_have_acted: true }
        requires:
          suits: { H: [4, 13] }
          evals: { longest_suit_length: [5, 5], total_points: [16, 40] }
        shows: "my second suit over their preempt: five of my own and four hearts with extras - a 4-4 major fit beats notrump on a doubleton stopper"
        establishes: { forcing: non_forcing }
      - id: ch_second_major_S3
        call: 3S
        priority: 29.5
        when: { unbid_suit: S, cheapest_in_suit: true, i_have_acted: true }
        requires:
          suits: { S: [4, 13] }
          evals: { longest_suit_length: [5, 5], total_points: [16, 40] }
        shows: "my second suit over their preempt: five of my own and four spades with extras - a 4-4 major fit beats notrump on a doubleton stopper"
        establishes: { forcing: non_forcing }
```

**THE ANSWERING SEAT.**  `non_forcing`, so none is strictly owed — and I traced
it anyway: W with `.J9763.AJT8642.J` answers **4H** through `uc_raise_H4` (fit
1.000 / 32).  The conversation closes without any new context.

**WHAT IT ENDANGERS** (everything in `general_competitive_high` at 29-29.5):

* `ch_penalty_X` (38, above) — untouched, and correctly so: verified that a flat
  15-count with a real club stopper still doubles 3C.
* `ch_nt3` (29, **below** mine) — the target.  It loses only hands with **exactly
  a five-card suit plus a four-card unbid major and 16+ total points**; on those,
  partner's 1NT response can hide four of my second suit and 3NT off a doubleton
  king in their suit is the losing matchpoint contract.
* `ch_rebid_$M3` (29, below) — a 6-4 hand keeps it, because my `longest_suit_length: [5, 5]`
  gate is exact.  Verified with a 6-4 hand: `ch_rebid_S3` still wins.
* `ch_new_H3`/`_hi` (27/27.5, below) — the five-card version; mine is a superset
  description with an extra-values floor, and where both fit (5-5) bidding the
  second suit is the same call.
* `ch_pass` (22, below).
* Fallback: `3H`/`3S` in this context are already covered by `ch_new_*3`, so no
  code fallback is deleted; `i_have_acted: true` further confines the `when` to
  the seat that has already bid a suit.

**VERIFIED.**  Before: `3NT` (`ch_nt3`, fit 1.000 / 29).  After: `3H`
(`ch_second_major_H3`, fit 1.000 / 29.5), and W raises to `4H`.  Both regressions
traced (6-4 keeps `ch_rebid_S3`; the flat stopper hand is unaffected).

**TEMPLATE.**  Written out for both majors.  Expand the same agreement (i) to
`general_competitive_low` as `cl_second_major_$M2` at the two level with a
14-point floor, (ii) to the **minors** at the three level with a 17-point floor,
and (iii) to `general_balancing_high`.  It is the "bid your shape, not your
stopper, when their preempt has taken your room" agreement and it is missing in
all four generic competitive contexts.

## Board 443 — NOTHING-WRONG (competitive lens)

**Verdict.** Constructive board.  Table B, call 4: W with `AK64.QJT8.AQ52.A`
(20 HCP, four-card heart support, a stiff ace) raises 1H straight to `4H`
(`ob_raise_4H`, "19+ support points", fit 1.000 / 76) and the 6H that makes
thirteen tricks is never in the picture.  The missing tool is a control-showing
or splinter raise, which the round-17 correction names explicitly (mini-splinters
0, control-showing raises 0) — constructive reviewer's ground.

**What I checked on the competitive side.**  All eight of our table-A calls are
passes BEN also makes at 1.00 against an uncontested 1D-1H-4C-4D-4NT-5D-6H
auction; N has 6 HCP and S has 5, neither with a suit.  `oc1D_pass` and `sw_pass`
are the correct rungs, and `general_competitive_high` should be, and is, silent
over their cue-bidding.

**NOTHING-WRONG** from the competitive/matchpoint discipline.

## Board 559 — margin -13

**Seat/call that went wrong.** Table A, call 5, **N bids 4H** (`uc_raise_H4`)
after `P - 1H - 1S - 2S(partner's cue-bid raise) - P`, holding
`9.AKT732.AQT87.6` — a 6-5 with two singletons opposite a hand that has just
promised a limit raise or better in hearts.  We played 4H for thirteen tricks
(+710); BEN's N/S bid 6H (+1460).

**The missing agreement (one sentence).** `r1H1S_cue` is
`forcing: one_round, agreed_suit: H` and **there is no context matching
`1H - 1S - 2S - P - ?`** — the cue-bid raise is another starved forcing seat, so
opener's answer is decided by `general_uncontested_continuation`, whose best
offer is a game raise at priority 32 and which cannot say "I am five-five".

**EXACT YAML.**  Two new contexts, placed after `resp_1H_over_1S`:

```yaml
  - id: opener_over_cue_raise_H
    description: "Opener answers partner's cue-bid raise after (1S) over our 1H"
    pattern: "1H - 1S - 2S - P - ?"
    rules:
      - id: ocr_H_second_D
        call: 3D
        priority: 60
        requires:
          suits: { H: [5, 13], D: [5, 13] }
        shows: "my real second suit opposite the cue-bid raise: five-five, and the fit is already agreed so this is a slam try, not a rescue"
        establishes: { forcing: game_forcing, agreed_suit: H }
      - id: ocr_H_second_C
        call: 3C
        priority: 60
        requires:
          suits: { H: [5, 13], C: [5, 13] }
        shows: "my real second suit opposite the cue-bid raise: five-five, and the fit is already agreed so this is a slam try, not a rescue"
        establishes: { forcing: game_forcing, agreed_suit: H }
      - id: ocr_H_rkc
        call: 4NT
        priority: 58
        requires:
          suits: { H: [5, 13] }
          evals: { total_points: [19, 40], "keycards(H)": [3, 5] }
        shows: "keycard ask: partner has promised a limit raise or better and I have the values to play a slam"
        establishes: { forcing: one_round, agreed_suit: H, asking: keycards }
        alertable: true
        convention: rkc_1430
      - id: ocr_H_game
        call: 4H
        priority: 52
        requires:
          suits: { H: [5, 13] }
          evals: { total_points: [14, 40] }
        shows: "accepting the cue-bid raise: game, no second suit to show"
        establishes: { forcing: sign_off, agreed_suit: H }
      - id: ocr_H_min
        call: 3H
        priority: 50
        requires:
          suits: { H: [5, 13] }
          evals: { total_points: [12, 13] }
        shows: "a minimum opening opposite the cue-bid raise: partner may pass with a bare limit raise"
        establishes: { forcing: invitational, agreed_suit: H }
```

**THE ANSWERING SEAT** (mandatory — `ocr_H_second_*` is game-forcing and
`ocr_H_min` is an invitation):

```yaml
  - id: opener_cue_second_reply_H
    description: "Responder after opener shows a second suit over the cue-bid raise"
    expand: { x: [C, D] }
    pattern: "1H - 1S - 2S - P - 3$x - P - ?"
    rules:
      - id: ocs_H_rkc_$x
        call: 4NT
        priority: 60
        requires:
          suits: { H: [3, 13] }
          evals: { total_points: [14, 40], "keycards(H)": [2, 5] }
        shows: "partner is five-five with the fit agreed: asking for keycards"
        establishes: { forcing: one_round, agreed_suit: H, asking: keycards }
        alertable: true
        convention: rkc_1430
      - id: ocs_H_game_$x
        call: 4H
        priority: 50
        requires:
          suits: { H: [3, 13] }
        shows: "no slam interest opposite the five-five: game in the agreed major"
        establishes: { forcing: sign_off, agreed_suit: H }
```

The 4NT then lands in the **existing** `rkc_response_agreed_H` /
`rkc_continue_after_5D` machinery, so the conversation is closed with no further
authoring.  `ocr_H_min`'s invitation is answered by responder's existing
`general_uncontested_continuation` raise ladder (3H is a pass-or-4H decision at
`uc_raise_H4` / `uc_pass`), which is authored.

**WHAT IT ENDANGERS.**  The new contexts are supersets — `general_uncontested_continuation`
still contributes every candidate it did (traced).  Within them:

* `ocr_H_second_*` (60) is deliberately placed **above** `ocr_H_rkc` (58): with a
  five-five and two singletons you describe the shape before you count aces, and
  keycard asking on a two-suiter is how a pair reaches 6H off two cashing tricks.
  I tried the other order first and report it as a negative: with RKC at 62 the
  engine asked immediately on this hand.
* `uc_raise_H4` (32) / `uc_raise_H3` (31) / `uc_rebid_H3` (29) / `uc_new_D3` (27)
  are all outranked.  Each of them describes the hand worse: the cue bid has
  already agreed hearts and promised 10+, so a raise adds nothing, and 3D is the
  same call my rung makes but with a meaning attached.
* **Fallback:** `3C`, `3D`, `3H`, `4H`, `4NT` were all already covered in this
  seat by `uc_*` rungs, so no code fallback is deleted.

**VERIFIED — the whole conversation, not just the entry.**  Walked the auction
with our engine in both N/S seats and the opponents passing:
`P 1H (1S) 2S P 3D P 4NT P 5D P 6H` — `ocr_H_second_D` (1.000/60), then
`ocs_H_rkc_D` (1.000/60), then the existing `rkc_5D` and `rkc5D_slam`.
**6H makes thirteen tricks**, which is the +1460 the other table scored, i.e.
the board goes flat.

**TEMPLATE.**  `expand` over the responder context only (`x: [C, D]`).  The
agreement itself must be expanded to every cue-bid raise in the file: the
two-level overcall twins (`1$M - 2$x - 3$x - P - ?` answering `r1M2x_cue`) and
the minor-opening cue raises.  Each needs the same five-rung opener context and
the same two-rung answering context — roughly 60 rules for the family, which is
exactly the density the round-17 correction asks for, and all of it in
*contested* auctions below game.

## Board 679 — margin -13

**Seat/call that went wrong.** Table A, call 5, **N bids 2NT** (`adv1n_2NT_D`)
opposite partner's 1NT overcall, holding `AK952.7642.63.Q4` — five spades and
four hearts.  We played 3NT for eight tricks (-100); S has `KJ985` and 4H makes
eleven (+650 at the other table).  The root is one rung earlier in the *system*,
not in the auction: N had no way to ask.

**The missing agreement (one sentence).** **There is no Stayman (and no
transfer) after a 1NT overcall** — `advance_1NT_overcall` contains three weak
0-7 sign-offs, an 8-9 invitational 2NT and a 10-15 3NT, so every 4-4 and 5-4
major fit opposite a 15-18 overcall is unfindable by construction.

**EXACT YAML.**  One rung into `advance_1NT_overcall`, plus the two contexts
that make it a closed conversation:

```yaml
      - id: adv1n_2C_$o
        call: 2C
        priority: 60
        when: { unbid_suit: C, cheapest_in_suit: true }
        requires:
          hcp: [8, 40]
          any_of: [ { suits: { H: [4, 13] } }, { suits: { S: [4, 13] } } ]
        shows: "Stayman opposite the 1NT overcall: at least one four-card major, invitational values or better"
        establishes: { forcing: one_round }
        alertable: true
        convention: stayman
```

**THE ANSWERING SEAT** (mandatory — 2C is `forcing: one_round`):

```yaml
  - id: advance_1NT_overcall_stayman
    description: "The 1NT overcaller answers Stayman"
    expand: { o: [C, D, H, S] }
    pattern: "1$o - 1NT - P - 2C - P - ?"
    rules:
      - id: a1nst_2H_$o
        call: 2H
        priority: 61
        when: { unbid_suit: H }
        requires: { suits: { H: [4, 13] } }
        shows: "four or more hearts"
        establishes: { forcing: non_forcing }
      - id: a1nst_2S_$o
        call: 2S
        priority: 60
        when: { unbid_suit: S }
        requires: { suits: { S: [4, 13] } }
        shows: "four or more spades, denying four hearts"
        establishes: { forcing: non_forcing }
      - id: a1nst_2D_$o
        call: 2D
        priority: 55
        when: { unbid_suit: D }
        requires: {}
        shows: "no four-card major to show"
        establishes: { forcing: non_forcing }
      - id: a1nst_2NT_$o
        call: 2NT
        priority: 54
        requires: {}
        shows: "no four-card major to show, and the cheap denial is not available"
        establishes: { forcing: non_forcing }

  - id: advance_1NT_stayman_fit
    description: "Advancer after the 1NT overcaller shows a major"
    expand_pairs:
      - { o: C, M: H }
      - { o: C, M: S }
      - { o: D, M: H }
      - { o: D, M: S }
      - { o: H, M: S }
      - { o: S, M: H }
    pattern: "1$o - 1NT - P - 2C - P - 2$M - P - ?"
    rules:
      - id: a1nsf_game_$o$M
        call: 4$M
        priority: 60
        requires: { suits: { $M: [4, 13] }, evals: { total_points: [9, 40] } }
        shows: "the fit is found: game opposite the 15-18 overcall"
        establishes: { forcing: sign_off, agreed_suit: $M }
      - id: a1nsf_invite_$o$M
        call: 3$M
        priority: 58
        requires: { suits: { $M: [4, 13] }, evals: { total_points: [8, 8] } }
        shows: "the fit is found but only eight points: inviting"
        establishes: { forcing: invitational, agreed_suit: $M }
      - id: a1nsf_3NT_$o$M
        call: 3NT
        priority: 56
        requires: { suits: { $M: [0, 3] }, hcp: [10, 15] }
        shows: "no fit after all: game in notrump"
        establishes: { forcing: sign_off }
      - id: a1nsf_2NT_$o$M
        call: 2NT
        priority: 54
        requires: { suits: { $M: [0, 3] }, hcp: [8, 9] }
        shows: "no fit after all: the invitation stands"
        establishes: { forcing: invitational }
```

(`a1nsf_invite_$o$M`'s 3M invitation is answered by the overcaller's existing
`general_uncontested_continuation` raise ladder; the 2NT invitation keeps its
existing acceptor `advance_1NT_overcall_invite` only when 2C was not used, which
is a gap worth closing in the same batch — a `1$o - 1NT - P - 2C - P - 2$M - P - 2NT - P - ?`
twin of `a1ninv_*`.)

**WHAT IT ENDANGERS.**

* `adv1n_2S_$o` (58) / `adv1n_2H_$o` (57) / `adv1n_2D_$o` (56) — all carry
  `hcp: [0, 7]`, and my rung has an 8-point floor, so the sets are disjoint.
* `adv1n_2NT_$o` (55) and `adv1n_3NT_$o` (54), **below** mine — these lose exactly
  the hands with a four-card major, which is the whole point: 3NT on a 5-4 major
  hand opposite a 15-18 overcall is the losing matchpoint contract, and this board
  is the demonstration (-100 versus +650).
* Fallback: `2C` in this seat was previously covered by `uc_new_C2`, so nothing
  is deleted.
* The `when: { unbid_suit: C }` guard means the rung is silent over a 1C opening,
  where 2C is not available — that is the one expansion of the four that is
  structurally dead, correctly.

**VERIFIED — the whole conversation.**  `P P 1D 1NT P` → N bids `2C`
(`adv1n_2C_D`, 1.000/60); S answers `2H` (`a1nst_2H_D`, 1.000/61); N bids `4H`
(`a1nsf_game_DH`, 1.000/60).  4H makes eleven tricks, i.e. the +650 the other
table scored.

**TEMPLATE.**  `expand: { o: [C, D, H, S] }` on the two new contexts (matching
the existing `advance_1NT_overcall`), plus the six-way `expand_pairs` shown.  The
matching **transfer** structure (2D/2H showing the major) is the natural second
half and should be authored in the same batch; so should the same Stayman for the
**balancing** 1NT overcall (`1$o - P - P - 1NT - P - ?`), which has the same hole.

## Board 761 — margin -13

**Seat/call that went wrong.** Table A, call 9, **S doubles 3S**
(`balhigh_reopen_X`) on `A.874.AKJ96.KQ85` after `1S - X - 2S - P - P - 3D - 3S - P - P`.
That is our side's **third** action on the same hand, partner has never made a
call, and 3S doubled made ten tricks: **-930**, where the other table played 3S
undoubled for -170.

**The missing agreement (one sentence).** When I have already doubled for
takeout *and* then bid a suit of my own, and partner has still never found a
call, a further double is not takeout — partner has denied the values to answer
the first one, so the hand is a defensive hand and the auction is over.

**EXACT YAML.**  One rung into `general_balancing_high`, immediately before
`balhigh_reopen_X`.  Its `when` is `balhigh_reopen_X`'s own `when` plus two
clauses, so its firing set is a strict subset of that rule's:

```yaml
      - id: balhigh_partner_silent_pass
        call: P
        priority: 41.5
        when: { their_last_bid_suit: true, side_has_acted: true, we_bid_last: false,
                my_last_call_was_double: false, we_hold_contract: false,
                partner_has_acted: false, i_have_acted: true }
        requires:
          evals: { longest_suit_length: [0, 6] }
        shows: "I have already doubled and then bid my own suit and partner has never found a call: a third action is a phantom, so defend"
        establishes: { forcing: sign_off }
        negative_inference_weight: soft
```

**THE ANSWERING SEAT.**  None owed — it is a pass that ends the auction.

**WHAT IT ENDANGERS.**  Because the `when` is a subset of `balhigh_reopen_X`'s,
the only rules it can outrank are those that could fire in that same seat:

* `balhigh_reopen_X` (41) and `balhigh_reopen_X2` (41) — the target.  The 16+ and
  19+ reopening doubles are right when partner may still have a hand; they are
  wrong when partner has passed my takeout double **and** their raise.
* `balhigh_rebid_$X4` (29), `balhigh_nt3` (29), `balhigh_new_$X3/4` (27/28) — a
  fourth call in a third strain opposite a partner who has passed twice is a
  worse description than defending.  The `longest_suit_length: [0, 6]` clause
  deliberately steps aside for a genuine seven-card suit (verified: fit drops to
  0.015 and the rung stops competing).
* `balhigh_pass` (21) — same call.
* Fallback: `P` is already covered by `balhigh_pass`; nothing is deleted.

**VERIFIED.**  Before: `X` (`balhigh_reopen_X`, fit 1.000 / 41) — the -930.
After: `P` (`balhigh_partner_silent_pass`, fit 1.000 / 41.5), which reproduces
the other table's 3S-for-170 and flattens the board.  Two regressions traced:
with partner having acted (`1S X 2D P 3S P P`) the rung is not offered at all,
and with a seven-card diamond suit it stands down.

**TEMPLATE.**  Add the identical rung to `general_balancing_low`
(`ballow_partner_silent_pass`, same `when`, priority just above
`ballow_reopen_X`) — that is where the same species costs a partscore instead of
a game — and to `general_competitive_high` for the direct seat.  No suit or
vulnerability expansion: the agreement is about the auction, not the cards.

## Board 762 — margin -13

**Seat/call that went wrong.** Table A, call 4, **S passes** (`balhigh_pass`)
after `1S - 5D - P - P`, holding `AJT93.A2..AQ8652` — a **diamond void**, 15
HCP, 5-6 in the black suits.  5S makes eleven double-dummy (+650); we took +100
defending.

**The missing agreement (one sentence).** The **five-level balancing seat is
empty**: over their leap to 5D the only two candidates in the whole engine are
`balhigh_pass` at fit 1.00 and a code-fallback double — `balhigh_reopen_X`
carries `standing_bid_level: [3]`, and every `balhigh_new_*` / `balhigh_rebid_*`
rung tops out at the four level.

**EXACT YAML.**  Two rungs into `general_balancing_high`, before `balhigh_pass`:

```yaml
      - id: balhigh_rebid_H5
        call: 5H
        priority: 33
        when: { my_suit: H, standing_bid_level: [5], cheapest_in_suit: true, we_hold_contract: false }
        requires:
          suits: { H: [5, 13] }
          evals: { total_points: [15, 40], standing_suit_length: [0, 1] }
        shows: "over their five-level preempt: a void or singleton in their suit and my own five-card major with opening values - bid it, do not defend a contract I cannot beat"
        establishes: { forcing: non_forcing, agreed_suit: H }
      - id: balhigh_rebid_S5
        call: 5S
        priority: 33
        when: { my_suit: S, standing_bid_level: [5], cheapest_in_suit: true, we_hold_contract: false }
        requires:
          suits: { S: [5, 13] }
          evals: { total_points: [15, 40], standing_suit_length: [0, 1] }
        shows: "over their five-level preempt: a void or singleton in their suit and my own five-card major with opening values - bid it, do not defend a contract I cannot beat"
        establishes: { forcing: non_forcing, agreed_suit: S }
```

Note `standing_suit_length`, not `suit_length(their)` — the documented trap is
that the latter resolves to LHO's suit, and this rung must read the suit of the
**standing bid**.

**THE ANSWERING SEAT.**  `non_forcing` with `agreed_suit`, so none is owed:
partner's raise/pass ladder over a five-level major is
`general_competitive_high` / `general_their_double`, both authored.

**WHAT IT ENDANGERS.**  In this seat, literally nothing else fits: the traced
candidate list before the patch is `balhigh_pass` (21) and a fallback `X` (9).

* `balhigh_pass` (21, below) — the target.
* The code-fallback `X` (9) — my rung does NOT cover `X`, so that fallback
  survives; the round-15 suppression mechanism is not triggered for the double.
* `balhigh_reopen_X`/`X2` (41, above) — untouched and unreachable here by their
  own `standing_bid_level: [3]` gate.
* `balhigh_raise_*4` (32) is below 33 but needs `partner_suit`, which does not
  exist when partner has never bid.

**VERIFIED.**  Before: `P` (`balhigh_pass`, fit 1.000 / 21).  After: `5S`
(`balhigh_rebid_S5`, fit 1.000 / 33), which makes eleven tricks.  Regression
traced: give S three small diamonds instead of the void and the rung drops to
fit 0.015 and we pass.

**NEGATIVE RESULT / SCOPE NOTE.**  The other half of this board is table B,
where W (`.9876.AKJ98653.7`, seven diamonds, spade void) overcalls `1D`
(`oc1C_1D`, priority 71) instead of pre-empting, exactly as
`oc1C_3D_preempt` (58) sits below it.  That is the same species as the
do-not-re-propose item "re-ranking the weak jump overcall" (round 11 measured
**-24 held out**), so **I do not propose it.**

**TEMPLATE.**  Write out the two majors as above; add the minor twins
(`balhigh_rebid_$m5` over a five-level major preempt) and — much more
importantly — expand the whole *level* : the file has 55 rules that bid at the
five level and the balancing seat over a five-level contract owns none of them.
A `standing_bid_level: [5]` sibling of the reopening double, of the raise ladder
and of the natural notrump belongs in the same batch.

## Board 886 — margin -13

**Seat/call that went wrong.** Table B, call 5, **W bids 3C** (`cl_new_C3`)
after `1H - X(mine) - P - 2D - 2H`, holding `QJ643.J.AK.AQJ73` — 18 HCP, 5-5 in
the black suits, having already doubled 1H for takeout.  The auction then went
`3H` by N, and W reopened with another double for **3H doubled making, -730**;
BEN bids `2S` and the board is a partscore fight.

**The missing agreement (one sentence).** After my takeout double, my own
**five-card major at the two level** must outrank my five-card minor at the
three level — the generic toolkit's priority ladder rises with the *level*
(`cl_new_C3` 27 beats `cl_new_S2_hi` 26.5), so with 5-5 the engine
systematically bids the higher contract in the lower-ranking suit.

**EXACT YAML.**  Two rungs into `general_competitive_low`, before `cl_new_C3`:

```yaml
      - id: cl_doubler_major_H2
        call: 2H
        priority: 27.8
        when: { unbid_suit: H, cheapest_in_suit: true, my_last_call_was_double: true }
        requires:
          suits: { H: [5, 13] }
          evals: { total_points: [15, 40] }
        shows: "the five-card major my takeout double concealed, with the extras that justify bidding it: a major at the two level beats a minor at the three"
        establishes: { forcing: non_forcing }
      - id: cl_doubler_major_S2
        call: 2S
        priority: 27.8
        when: { unbid_suit: S, cheapest_in_suit: true, my_last_call_was_double: true }
        requires:
          suits: { S: [5, 13] }
          evals: { total_points: [15, 40] }
        shows: "the five-card major my takeout double concealed, with the extras that justify bidding it: a major at the two level beats a minor at the three"
        establishes: { forcing: non_forcing }
```

This is **not** the excluded item "a takeout double must not hide a six-card
suit": it adds no gate to the double and forbids nothing.  It is a rung that
lets the doubler *show* the major afterwards.

**THE ANSWERING SEAT.**  `non_forcing`; partner's raise/pass ladder in
`general_competitive_low` and `general_competitive_high` is authored.

**WHAT IT ENDANGERS** (everything at or below 27.8 in `general_competitive_low`,
and only when my last call was a takeout double):

* `cl_negative_X2` (33) / `cl_doubler_raise3_$m` (33) / `cl_raise_*` (30-32) — all
  **above** me, so a genuine fit for partner's response still wins.  That is the
  right order: raising partner beats showing my own suit.
* `cl_new_C3`/`_hi` (27/27.5, **below**) — the target.  Bidding 3C over 2H when
  I hold five spades commits the partnership to the three level in the minor and
  makes the 5-3 spade fit unfindable.
* `cl_new_S2`/`_hi` (26/26.5, below) — same call as mine; mine just carries the
  extras and the doubler's identity, so nothing behaves differently.
* `cl_nt2` (28) is **above** 27.8, so a balanced doubler with a stopper still
  bids notrump.
* Fallback: `2S` and `2H` are already covered by `cl_new_*2` here.

**VERIFIED.**  Before: `3C` (`cl_new_C3`, fit 1.000 / 27) — the call that leads
to the -730.  After: `2S` (`cl_doubler_major_S2`, fit 1.000 / 27.8), with
`cl_new_C3` still at fit 1.000 immediately below it.

**SECOND OBSERVATION on the same board (table A, call 2).**  N runs to `2C`
(`xd_run_C2`, "running to my own C") over W's **takeout** double of partner's
1H, on `9.97.QJ94.KT8542`.  The run rungs in `general_their_double` were written
for escaping a *penalty* double and they outrank `rdx_pass` (25 versus 20) in the
responder-over-a-takeout-double seat, where nothing needs escaping.  The right
repair is a `resp_over_double_$M` weak-hand rung at priority 26 rather than a
`when` gate on the runs; I flag it rather than propose it because
`general_their_double` is the context the ledger warns hardest about and one
board is not a case.

**TEMPLATE.**  Both majors written out.  Expand to `general_competitive_high`
(`ch_doubler_major_$M3`) and to `general_balancing_low`
(`ballow_doubler_major_$M2`), with the same `my_last_call_was_double` guard.

## Board 26 — margin -12

**Seat/call that went wrong.** Table B, call 5, **W bids 4C** (`adx_pull_C4`)
answering partner's takeout double of `3H`, holding `AQ82.54.82.T8543` — four
spades and five clubs.  4C went one down; E holds `KT973` and 4S makes ten
tricks the other way.  (Table A's `2H` weak two on `6.AK9876.J53.Q92` is a
style call BEN grades at 0.84 for 3H; I do not indict it.)

**The missing agreement (one sentence).** When answering a takeout double, a
**four-card major at the three level** beats a longer minor at the four level —
`adx_pull_S3` carries `suit_diff(S,C) >= 0`, so with 4-5 in spades and clubs the
three-level major pull scores 0.800, misses the fast path by a tenth, and the
four-level minor wins at fit 1.00.

**EXACT YAML.**  Two rungs into `general_pull_or_sit`, after `adx_pull_S3`.
Same `when` as `adx_pull_S3`, with the `suit_diff` clauses removed:

```yaml
      - id: adx_pull_major_H3
        call: 3H
        priority: 58.6
        when: { unbid_suit: H, cheapest_in_suit: true, their_last_bid_suit: true, i_have_acted: false }
        requires: { suits: { H: [4, 13] }, evals: { total_points: [0, 11] } }
        shows: "answering the takeout double with a four-card major at the three level rather than a longer minor at the four"
        establishes: { forcing: non_forcing }
      - id: adx_pull_major_S3
        call: 3S
        priority: 58.5
        when: { unbid_suit: S, cheapest_in_suit: true, their_last_bid_suit: true, i_have_acted: false }
        requires: { suits: { S: [4, 13] }, evals: { total_points: [0, 11] } }
        shows: "answering the takeout double with a four-card major at the three level rather than a longer minor at the four"
        establishes: { forcing: non_forcing }
```

Hearts is a tenth higher than spades so a 4-4 hand answers in the **cheaper**
major and the pair is never left with a priority tie (`is_clear = False`, which
DECISIONS prices at -76 gap-points across the corpus).

**THE ANSWERING SEAT.**  `non_forcing`; the doubler's continuation over the
answer is `general_competitive_high`, authored.

**WHAT IT ENDANGERS** (every rung in `general_pull_or_sit` at or below 58.6):

* `adx_sit` (61, **above**) — real trumps behind them still sit.  Untouched.
* `adx_neg_major_*` (62, above) — untouched.
* `adx_pull_S4` (58) and `adx_pull_S3` (58) — mine is the same call as the
  three-level one with the suit-length comparison dropped; the doubler asked for
  a **major**, so answering in the four-card major is what the double meant.
* `adx_pull_C4`/`D4` (54, **below**) — the target.  Verified they survive where
  they should: with `A82.54.82.KT8543` (three spades, six clubs) the engine still
  bids 4C and my rung falls to fit 0.349.
* `adx_pass_min` (52, below) — a hand with 0-11 and a four-card major should
  answer, not pass; that is what a takeout double is for.
* Fallback: `3S`/`3H` are already covered here by `adx_pull_$X3`.

**VERIFIED.**  Before: `4C` (`adx_pull_C4`, fit 1.000 / 54).  After: `3S`
(`adx_pull_major_S3`, fit 1.000 / 58.5), with the regression traced.

**TEMPLATE.**  Both majors written out (the context has no `expand`).  Expand to
the **two-level** answer (`adx_pull_major_$M2`, the same agreement over a doubled
weak two — `advance_weak2_double_*` has its own contexts and needs the same
comparison removed) and to the **four-level** answer over a doubled four-level
preempt, which has no rung at all.

## Board 43 — margin -12

**Seat/call that went wrong.** Table A, call 5, **N passes** (`cl_pass`) after
`P - P - 1C - 1H(partner) - 1S`, holding `KT876.KT9.K7632.` — three-card support
for partner's heart overcall, a **club void**, and eight total trumps.  BEN bids
2H.  We passed, E/W bought it in 4C for -130; N/S make ten tricks in hearts.

**The missing agreement (one sentence).** There is a **seam in the competitive
raise ladder at 13+ support points**: `cl_raise_$M2` caps at 12, `cl_raise_$M3`
carries `cheapest_in_suit: true` and is therefore never offered while the cheap
raise is legal, and `cl_raise_$M4` needs `rule_of_26 >= 25` which a one-level
overcall's shown minimum cannot reach — so a 13-15 support-point raise has no
rung anywhere and the seat falls to the catch-all pass.

**EXACT YAML.**  Two rungs into `general_competitive_low`, before `cl_raise_H4`:

```yaml
      - id: cl_raise_jump_H3
        call: 3H
        priority: 31.5
        when: { partner_suit: H }
        requires:
          suits: { H: [3, 13] }
          evals: { total_points: [13, 40], "lott_total_trumps(H)": [8, 26] }
        shows: "jump raise of partner's overcall: thirteen support points and a real fit, too good for the cheap raise and not enough combined values for game"
        establishes: { forcing: invitational, agreed_suit: H }
      - id: cl_raise_jump_S3
        call: 3S
        priority: 31.5
        when: { partner_suit: S }
        requires:
          suits: { S: [3, 13] }
          evals: { total_points: [13, 40], "lott_total_trumps(S)": [8, 26] }
        shows: "jump raise of partner's overcall: thirteen support points and a real fit, too good for the cheap raise and not enough combined values for game"
        establishes: { forcing: invitational, agreed_suit: S }
```

Deliberately **no** `cheapest_in_suit` gate — that gate is what makes the
existing three-level rung unreachable, and this rung is a *jump*, so the gate
would make it unreachable too.  This is **not** the excluded item "freeing
`cl_raise_lott3_$M`": that rung is the weak/shape LOTT raise (3-10 points) and
stays exactly as it is; mine is the constructive 13+ raise, a different hand.

**THE ANSWERING SEAT** (`forcing: invitational`, so it is owed).  The overcaller
over a jump raise lands in `general_competitive_high` / `general_uncontested_continuation`,
which already contain `ch_raise_$M4` / `uc_raise_$M4` (game with extras) and the
pass rungs — I traced that the overcaller's seat is populated and did **not**
have to author it.  If the consolidator wants the invitation answered explicitly,
the rung is `ch_accept_jump_raise_$M` at 4$M with `total_points: [14, 40]` and
`partner_last_suit: $M`.

**WHAT IT ENDANGERS** (`general_competitive_low`, at or below 31.5):

* `cl_raise_$M4` (32, **above**) — a hand with the combined values for game still
  bids game; my rung cannot outrank it.
* `cl_negative_X1/2` (33, above) — untouched.
* `cl_raise_lott3_$M` (32, above) and `cl_raise_lott4_$M` (32, above) — the
  shape/Law raises keep precedence, which is right: with ten trumps you bid the
  level of the fit whatever your points.
* `cl_raise_$M3` (31, **below**) — unreachable today because of its own
  `cheapest_in_suit`; where it is reachable (the cheap raise illegal) it starts at
  10 points and mine at 13, so the bands do not overlap in practice.
* `cl_raise_$M2` (30, below) — capped at 12; verified: a nine-support-point
  version of the same hand still bids 2H and my rung falls to fit 0.800.
* `cl_new_*`, `cl_nt*` (26-29, below) — a three-card fit with 13 support points
  and a void is better described by the raise than by a second suit.
* Fallback: `3H`/`3S` are already covered by `cl_raise_$M3` and `cl_new_*3`.

**VERIFIED.**  Before: `P` (`cl_pass`, fit 1.000 / 20).  After: `3H`
(`cl_raise_jump_H3`, fit 1.000 / 31.5).  Regression traced at nine support points.

**SCOPE NOTE.**  The two other divergences on this board — S's simple `1H`
overcall where BEN wants the weak jump `2H`, and W's `nxj_X` — are both on the
do-not-re-propose list (re-ranking the weak jump overcall, round 11: -24 held
out; and the `nxj_X` gate, round 14: -5 held out).  I leave them alone.

**TEMPLATE.**  Both majors written out.  Expand to the **minors**
(`cl_raise_jump_$m3` — same seam, and note board 59's finding that the minor half
of every raise family is missing), to `general_competitive_high`
(`ch_raise_jump_$M4`) and to `general_balancing_low`.

## Board 314 — margin -12

**Seat/call that went wrong.** Table A, call 4, **S passes** (`cl_pass`) after
`P - P - 1C(partner) - 2C(their cue)`, holding `J5.A98.762.QJ763` — five-card
support for partner's opening minor.  W then leapt to 4S for eleven tricks,
-650, with nothing from us on the way.  BEN bids 3C.

**The missing agreement (one sentence).** The **preemptive (Law) raise of a
minor does not exist**: `cl_raise_lott3_$M` is `expand: { M: [H, S] }`, so a
weak hand with four or five trumps in partner's minor has only the constructive
`cl_raise_C3` (8+ support points), which this hand misses by a fraction —
fit 0.800, one tenth under the fast path — and the seat drops to pass.

**EXACT YAML.**  Two rungs into `general_competitive_low`, immediately after
`cl_raise_lott3_S`:

```yaml
      - id: cl_raise_lott3_C
        call: 3C
        priority: 32
        when: { partner_suit: C, cheapest_in_suit: true }
        requires:
          suits: { C: [4, 13] }
          evals: { "lott_total_trumps(C)": [8, 26], total_points: [3, 10] }
        shows: "preemptive raise of partner's minor to the LOTT level: four-plus trumps, weak - the raise is obstruction, not values"
        establishes: { forcing: non_forcing, agreed_suit: C }
      - id: cl_raise_lott3_D
        call: 3D
        priority: 32
        when: { partner_suit: D, cheapest_in_suit: true }
        requires:
          suits: { D: [4, 13] }
          evals: { "lott_total_trumps(D)": [8, 26], total_points: [3, 10] }
        shows: "preemptive raise of partner's minor to the LOTT level: four-plus trumps, weak - the raise is obstruction, not values"
        establishes: { forcing: non_forcing, agreed_suit: D }
```

Note this does **not** touch the excluded item: `cl_raise_lott3_$M`'s
`cheapest_in_suit` gate stays exactly where it is, and round 11's "free it"
experiment is not repeated.  In a *minor* the gate is usually satisfied anyway,
because their overcall or cue has already used up the two level — verified here:
3C is the cheapest club bid over their 2C and the rung fires.

**THE ANSWERING SEAT.**  `non_forcing`, obstruction; opener's continuation is
`general_competitive_high`, authored.

**WHAT IT ENDANGERS** (`general_competitive_low`, at or below 32):

* `cl_negative_X2` (33, **above**) — an 8+ HCP hand with an unbid major still
  makes the negative double.  Untouched.
* `cl_raise_C3`/`D3` (31, **below**) — the constructive raise.  My band tops out
  at 10 total points and it starts at 8, so on the 8-10 overlap two calls are
  identical (3C either way) and only the `shows` differs; above 10 the
  constructive rung wins on fit.  Verified with a 14-count: `cl_raise_C3` still
  takes it at fit 1.000.
* `cl_raise_C2`/`D2` (30, below) — where the cheap raise is legal the
  `cheapest_in_suit` gate keeps my rung out, exactly as for the major twins.
* `cl_new_*`, `cl_nt*` (26-29, below) — a five-card fit for partner's opening
  outranks a two-level notrump on 8 HCP.
* `cl_pass` (20, below) — the target.
* Fallback: `3C`/`3D` are already covered by `cl_raise_$m3`.

**VERIFIED.**  Before: `P` (`cl_pass`, fit 1.000 / 20).  After: `3C`
(`cl_raise_lott3_C`, fit 1.000 / 32).  Two regressions traced (three-card support
falls to fit 0.082 and passes; a 14-count keeps the constructive raise).

**TEMPLATE.**  Written out for both minors.  This is the second half of board
59's finding and they should ship together: **every** LOTT family in the file is
`expand: { M: [H, S] }` and needs its `{ m: [C, D] }` twin — `cl_raise_lott3/4`,
`ch_raise_lott/lott4`, `ballow_raise_lott4`, `balhigh_raise_lott4`,
`uc_raise_lott4`.  That is ten rules from one agreement.

## Board 318 — NOTHING-WRONG (competitive lens)

**Verdict.** Constructive slam board.  Table A, call 6: N with
`AQ83.KQT53.K74.A` (18 HCP, four-card spade support for partner's 1S rebid)
bids fourth-suit-forcing `2C` at fit **0.435** — a soft-miss lottery pick, the
population DECISIONS names as the one surviving hypothesis — and the auction
ends in 4NT for +720 where 6S makes thirteen.  `fsf_2C` versus a splinter or a
control-showing raise is the constructive reviewer's ground, and the
round-17 correction (control-showing raises: 0 rules) names exactly this seat.

**What I checked on the competitive side.**  Table B is seven of our passes, all
of which BEN also makes at 1.00, against an uncontested 1D-1H-1S-4NT-5H-6S.  E
holds 5 HCP and W holds 3 **vulnerable against vulnerable**; `oc1D_pass`,
`sw_pass`, `cl_pass` and `ch_pass` are each the correct rung, and a lead-directing
or sacrificial action with a six-card club suit headed by the queen at
unfavourable is exactly the discipline failure this project pays for.

**NOTHING-WRONG** from the competitive/matchpoint discipline.

## Board 479 — NOTHING-WRONG (competitive lens)

**Verdict.** Uncontested game force.  Table A, call 7: S with `853.K32.A94.AKT9`
bids `3C` (`uc_raise_C3`) at fit **0.082** after `1C - 2C - 2NT` — a textbook
soft-miss lottery: the whole candidate set tops out at 0.082 and the engine
takes the least-bad misfit, then drives to 5C for -100 where 3NT makes ten.
That is the `gf_landing_*` family and the scoring-model question DECISIONS says
has never been attacked directly; it is not a competitive board.

**What I checked on the competitive side.**  All five of our table-B calls are
passes BEN also makes at 1.00; E has 3 HCP and W 11 balanced **vulnerable
against vulnerable** with no suit worth showing, and `oc1C_pass` / `cl_pass` /
`ch_pass` / `balhigh_pass` are each right.  One structural note for the round,
since it is in my lane: **the whole `gf_landing_*` family uses
`pattern: "... - P - ?"`,** which means "RHO passed", so after any competitive
call — a double included — the game-force landing ladder is unreachable and the
seat falls to `uc_*` or the code fallback.  DECISIONS already lists this; this
board is its uncontested twin and shows the ladder is thin even when nobody
interferes.

**NOTHING-WRONG** from the competitive/matchpoint discipline.

## Board 580 — margin -12

**Seat/call that went wrong.** Table A, call 2, **S doubles** (`cl_negative_X2`)
after `1H(partner) - 2S`, holding `6.T986.AT85.AK43` — **four-card heart
support**, a singleton spade, 11 HCP.  A negative double denies a fit for
partner's suit; we then defended 4S doubled for +800 while the other table bid
the cold 6H for +1460.

**The missing agreement (one sentence).** `resp_1M_over_2x`'s `expand_pairs` is
`(H,C) (H,D) (S,C) (S,D) (S,H)` — **the pair `(M: H, x: S)` is missing**, so
`1H - 2S - ?` has no responder context at all: no cue-bid raise, no competitive
raise, no shaped negative double, and the seat is annexed by the generic
`cl_negative_X2` at priority 33.

(The pair cannot simply be added to the existing `expand_pairs`: with `M: H` and
`x: S`, `$oM` is spades — *their* suit — so `r1M2x_X` would demand four cards in
the suit they just bid.  It needs its own context.)

**EXACT YAML.**  A new context, placed after `resp_1M_over_2x`:

```yaml
  - id: resp_1H_over_2S
    description: "Responder after 1H - (2S) jump overcall"
    pattern: "1H - 2S - ?"
    rules:
      - id: r1H2S_cue
        call: 3S
        priority: 74
        requires: { suits: { H: [3, 13] }, evals: { total_points: [10, 40] } }
        shows: "cue-bid raise: limit raise or better in hearts"
        establishes: { forcing: one_round, agreed_suit: H }
        alertable: true
        convention: cue_raise
      - id: r1H2S_X
        call: X
        priority: 72
        requires:
          hcp: [8, 40]
          not: { suits: { H: [3, 13] } }
          any_of: [ { suits: { C: [4, 13], D: [4, 13] } }, { suits: { C: [5, 13] } }, { suits: { D: [5, 13] } } ]
        shows: "negative double: the minors, no heart fit"
        establishes: { forcing: one_round }
        convention: negative_double
      - id: r1H2S_raise
        call: 3H
        priority: 70
        requires: { suits: { H: [3, 13] }, evals: { total_points: [6, 9] } }
        shows: "competitive raise to the three level"
        establishes: { forcing: non_forcing, agreed_suit: H }
      - id: r1H2S_2NT
        call: 2NT
        priority: 55
        requires: { hcp: [10, 12], features: [ "stopper(S)" ], not: { suits: { H: [3, 13] } } }
        shows: "10-12 with a spade stopper"
        establishes: { forcing: invitational }
      - id: r1H2S_pass
        call: P
        priority: 20
        requires: { hcp: [0, 7] }
        shows: "nothing to say"
        establishes: { forcing: non_forcing }
        negative_inference_weight: soft
```

**THE ANSWERING SEAT** (mandatory — `r1H2S_cue` is `forcing: one_round`, and
`1H - 2S - 3S - P - ?` matches no context today):

```yaml
  - id: opener_over_cue_raise_H_jump
    description: "Opener answers the cue-bid raise after (2S) over our 1H"
    pattern: "1H - 2S - 3S - P - ?"
    rules:
      - id: ocj_H_rkc
        call: 4NT
        priority: 60
        requires:
          suits: { H: [5, 13] }
          evals: { total_points: [18, 40], "keycards(H)": [3, 5] }
        shows: "keycard ask: partner has promised a limit raise or better and my hand plays for a slam"
        establishes: { forcing: one_round, agreed_suit: H, asking: keycards }
        alertable: true
        convention: rkc_1430
      - id: ocj_H_game
        call: 4H
        priority: 52
        requires:
          suits: { H: [5, 13] }
          evals: { total_points: [13, 40] }
        shows: "accepting the cue-bid raise: game in the agreed major"
        establishes: { forcing: sign_off, agreed_suit: H }
      - id: ocj_H_min
        call: P
        priority: 40
        requires:
          evals: { total_points: [0, 12] }
        shows: "a dead minimum: no game opposite a limit raise once they have taken the three level"
        establishes: { forcing: sign_off, agreed_suit: H }
```

The 4NT lands in the existing `rkc_response_agreed_H` / `rkc_continue_after_5H`
machinery, so the conversation is closed with no further authoring.

**WHAT IT ENDANGERS.**  The new responder context is a superset —
`general_competitive_low` still contributes `cl_raise_H4`, `cl_new_*`, `cl_pass`
etc. (traced).  What my rungs outrank:

* `cl_negative_X2` (33) — the target.  A negative double with four-card support
  for partner's major is a definitional error, not a judgement call.
* `cl_raise_H4` (32) / `cl_raise_H3` (31) / `cl_raise_lott4_H` (32) — a limit
  raise or better should cue, not guess a level; and the weak raises stay
  reachable below 10 total points through `r1H2S_raise` at 70 (which is above
  them, so the *described* raise wins).
* `cl_pass` (20) — a 0-7 hand keeps passing through `r1H2S_pass`.
* **Fallback:** `3S`, `3H`, `2NT`, `X` and `P` in this seat were all already
  covered by `general_competitive_low` rungs, so no code fallback is deleted.

**VERIFIED — the whole conversation.**  Before: `X` (`cl_negative_X2`, fit
1.000 / 33).  After, walked with our engine in both N/S seats:
`1H (2S) 3S P 4NT P 5H P 6H` — `r1H2S_cue` (1.000/74), `ocj_H_rkc` (1.000/60),
then the existing `rkc_5H_agreed` and `rkc5H_slam`.  **6H makes thirteen
tricks**, i.e. the +1460 the other table scored.

**NEGATIVE RESULT, reported rather than shipped.**  My first idea for this board
was a rung letting N bid `5H` over their `4S` instead of `ch_penalty_X` (a
self-sufficient seven-card suit outranking the penalty double).  It is wrong on
the arithmetic: 4S doubled four down non-vulnerable is **+800** and 5H making
thirteen is **+710**.  The double is the better *partscore* decision; the 12 IMPs
are lost two calls earlier, at the negative double.  I dropped it.

**SCOPE NOTE.**  Table B's `oc1H_1S` (BEN wants the weak jump 2S) is the
excluded weak-jump-overcall ranking; not proposed.

**TEMPLATE.**  `resp_1H_over_2S` covers the one one-major-over-the-other jump
that the existing `expand_pairs` cannot express.  The same shape recurs and
should be authored in the same batch: `1H - 3S - ?`, `1S - 3H - ?`,
`1$m - 2$M - ?` and `1$m - 3$M - ?` all lack a cue-raise, and every one of them
needs the matching `opener_over_cue_raise_*` answering context — the cue-bid
raise is the single most common competitive convention in the file and only two
of its dozen positions are authored.

## Board 959 — margin -12

**Seat/call that went wrong.** Table A, call 3, **S bids 1S** (`sw_1S`,
"sandwich overcall: good 5+ spades, 8-16") in the sandwich seat after
`1D - P - 1H`, holding `AKQJT854..2.J932` — an **eight-card solid spade suit**
and a heart void.  BEN bids 4S.  N/S make twelve tricks in spades; we defended
4H for +100 instead of scoring +680.

**The missing agreement (one sentence).** The sandwich seat's pre-emptive ladder
**stops at the three level** — `sw_3S` is "seven-card suit, 3-10" and an
eight-card suit with 11 HCP scores 0.800 against it, so the whole pre-emptive
family misses the fast path and a one-level overcall at fit 1.00 wins; the
direct seat has `oc1$o_4$M_preempt` for exactly this hand and the sandwich seat
has no four-level rung at all.

**EXACT YAML.**  Two rungs into `sandwich_seat`, after `sw_3S`:

```yaml
      - id: sw_4H
        call: 4H
        priority: 69.7
        when: { unbid_suit: H }
        requires:
          suits: { H: [8, 13] }
          evals: { total_points: [5, 40], "suit_quality(H)": [2, 9] }
        shows: "sandwich preemptive jump to game: an eight-card major between two bidding opponents"
        establishes: { forcing: sign_off, agreed_suit: H }
      - id: sw_4S
        call: 4S
        priority: 69.7
        when: { unbid_suit: S }
        requires:
          suits: { S: [8, 13] }
          evals: { total_points: [5, 40], "suit_quality(S)": [2, 9] }
        shows: "sandwich preemptive jump to game: an eight-card major between two bidding opponents"
        establishes: { forcing: sign_off, agreed_suit: S }
```

**THE ANSWERING SEAT.**  `forcing: sign_off` — a pre-empt to game asks nothing,
and partner's onward seat is `general_competitive_high` / `general_their_double`,
both authored.

**WHAT IT ENDANGERS** (every rung in `sandwich_seat` my 69.7 can outrank):

* `sw_X` (70, **above**) — a takeout of both their suits still wins; my rung
  requires an eight-card suit, which is not a takeout hand anyway.
* `sw_3S`/`sw_3C` (69.5, below) — the seven-card version.  Mine requires **eight**
  cards, so the two are disjoint on length.  Verified: with a seven-card suit the
  engine's answer is unchanged.
* `sw_2S_jump` (69, below) — six cards; disjoint.
* `sw_1S`/`sw_2S` (68/66, below) — the target.  A one-level overcall on an
  eight-card solid suit against two bidding opponents hands them the auction; the
  whole value of the hand is pre-emptive.
* `sw_pass` (30, below).
* Fallback: `4S`/`4H` in this seat were not covered by any `sandwich_seat` rung
  before, so this **does** delete the code fallback for those calls in this
  context.  That is acceptable and I checked it: the `when: { unbid_suit }` plus
  the eight-card gate means the rung is only offered where a four-level major
  jump is legal at all, and the fallback layer's own four-level offering in a
  contested sandwich seat is `quiet`.

**VERIFIED.**  Before: `1S` (`sw_1S`, fit 1.000 / 68).  After: `4S` (`sw_4S`, fit
1.000 / 69.7).  Regression traced with a seven-card suit: unchanged.

**TEMPLATE.**  Both majors written out inside the existing
`expand: { o: ... }` of `sandwich_seat`, guarded by `when: { unbid_suit }`.
Expand the same idea to the **minors** at the five level (`sw_5C`/`sw_5D` on a
nine-card suit) and — more valuable — to the **balancing** seat, which likewise
tops out at three: `ballow_4$M_preempt` does not exist.

## Board 967 — NOTHING-WRONG (competitive lens)

**Verdict.** Constructive board.  Table A, call 7: S with `QJ75.2.T653.AQT6`
raises partner's **reverse** to `3D` through `uc_raise_D3` (priority 27) while
the context's own `rrevd_3NT` (63) sits at fit 0.134 and `rrevd_2S` (66) at
0.349 — the generic toolkit annexing a reverse auction — and the pair then
Blackwoods into 6D for -100 where 3NT makes ten.  Responder's ladder over a
reverse, and the keycard ask that should not have fired, are the constructive
reviewer's ground.

**What I checked on the competitive side.**  All five of our table-B calls are
passes BEN also makes at 1.00 in an uncontested 1D-1S-2H-3NT auction; E has 7 HCP
with `K8743` clubs and W 7 with `A9842` spades, both **non-vulnerable against
vulnerable** — the one vulnerability where a light overcall is tempting.  I
checked both: `oc1D_pass` is right for E (a five-card club suit headed by the
king at the two level over 1D is the classic losing overcall), and `sw_pass` is
right for W (`A9842` in the sandwich seat over 1D-P-1S, with spades **bid on my
left**, is not an overcall in any system).  Both seats are correctly silent.

**NOTHING-WRONG** from the competitive/matchpoint discipline.

