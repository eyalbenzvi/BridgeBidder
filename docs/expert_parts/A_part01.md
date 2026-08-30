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

