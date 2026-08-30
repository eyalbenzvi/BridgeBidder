# Expert B — constructive / team-IMP review of `docs/dossier_575757/part06.md`

38 boards, -122 IMPs.  **27 proposals, 9 NOTHING-WRONGs, 1 proposal withdrawn on
whole-corpus evidence, 1 honest negative** (the agreement is right, the board
does not move).  22 of the 27 were traced through a modified copy of the system
YAML and are labelled **VERIFIED**; the harness is
`scratchpad/B_eyal_p06/proto.py` (`build(edits, out)` writes a patched YAML to a
scratch path, `show()` ranks against it; the repo YAML was never touched).

## Method notes that changed my own conclusions

* **`fires_summary` reversed one verdict and softened three.**  Board 433's
  proposal (a pass rung outranking `ch_new_long3_D`) is **withdrawn**:
  `ch_new_long3_D` runs **+4.33 IMPs a table over 3 tables** — the board in the
  dossier is its only loser and it is the most profitable rung I touched.
  Boards 98, 199 and 883 are marked lower-confidence for the same reason
  (`v3_D_X` +1.60, `sw_2H` -2.67 but the family is small, `bal_X` -0.21).
* **A context that `expand:`s over a variable which does not appear in its
  `pattern` produces N identical contexts and only the first is ever used.**
  My first draft of the board-674 context did this and three quarters of its
  rungs were dead.  Written out per suit instead.  This is a DSL trap worth
  recording; it is not in `DSL_FOR_EXPERTS.md`.
* **`we_hold_contract` does not mean "our side owns the standing bid".**  On
  board 905 the standing bid was partner's 1NT and `we_hold_contract` was
  `False`; `we_bid_last: true` is the condition that means what I wanted.
* **The primary-reading trap is live in this dossier.**  `cl_new_long2_H_hi`
  "decided" board 646 but `fires_summary` says it *never fires* — the recorded
  `rule` field is a different rung of the same call.  Every accusation below is
  re-ranked through `score_candidates`, not read off the dossier row.
* **`partner_limited` is unusable** (round 17 item 5: `NameError` on first use).
  Where I needed "partner has limited himself" I used the `partner_shown_max`
  evaluator, which works and gives clean numbers (7 / 8 / 10 / 11 / 40 on the
  boards below).

## The three agreements that matter most in this slice

1. **A reverse is forcing and there is no answer below 8 points** (board 506).
   `rrevh_2S` / `rrev_2$M` / `rrevd_2S` all floor at `hcp: [8, 40]`, so a
   six-card suit with four points has nothing that fits and `uc_pass` takes a
   one-round force at fit 1.00.  Ships with `opener_after_reverse_signoff`.
   Verified end to end: `1C-1S-2H-2S-P`, where we previously passed 2H out.
2. **Responder has no system over an overcall of our 1NT opening** (boards 674
   and 852).  Both seats fell to `general_competitive_low`, whose negative
   double wants 8+ HCP and whose natural two-level suit bid wants 10+, so an
   8-count with five diamonds and a 7-count with four hearts both passed.  A
   closed conversation — negative double, natural sign-offs, 3NT, catch-all
   pass — plus **the seat that answers the double**.  Verified end to end on
   both boards (2H making eleven; 3H making nine).
3. **Opener's third call after responder's simple preference has no context at
   all** (board 863), so `uc_raise_H4` — a rung written to raise *partner's*
   suit — bid game on a 15-count opposite a preference that showed 6-10.
   `opener_after_major_preference` (pass / 3H try / 4H) plus the seat that
   answers the try.

Honourable mention because of its rate: **`redouble_continuations` exists only
for minor openings and has no notrump rung at all.**  `rdc_pass_D` runs
**-6.75 IMPs a table over 4 tables**, the worst rate of any rung I looked at.
Boards 23 and 991 are the two halves of that hole.

---

## Board 646 — margin -4

**Seat/call:** table A, call 6, N bids **2H** on `976.AJ7642.7.J87` after
`1S - P - 1NT - P - 2D`.  Deciding rule `cl_new_long2_H_hi` at fit 1.000
(`total_points` = 8.0: six HCP plus the singleton diamond clears the 8-point
floor).

**Missing agreement:** when both opponents have bid and described a fit and my
side has never acted, an eleven-count is not an entry at the two or three
level — passing is the agreement, not the absence of one.

**YAML** — context `general_competitive_low` (no `expand:`, so written out):

```yaml
      - id: cl_pass_sandwich_discipline
        call: P
        priority: 27.7
        when: { i_have_acted: false, side_has_acted: false, standing_bid_level: [2] }
        requires: { hcp: [0, 11], evals: { their_bidders: [2, 2] } }
        shows: "both of them have bid and described and my side has never acted: eleven points is not a three-level entry"
        establishes: { forcing: non_forcing }
```

**Answering seat:** none needed — it is a pass and it ends nothing; partner is
still free to balance, and `bal_*` / `ballow_*` own that seat unchanged.

**What it endangers** (everything in `general_competitive_low` it can outrank,
in the seats its `when` reaches — my side silent, both of them having bid, the
standing bid at the two level):
* `cl_new_long2_$X` / `_hi` (26.0/26.5) — a six-card suit and eight *total*
  points opposite a partner who could not act over two bidding opponents is a
  bad two-level entry; this is the rung that lost the board.
* `cl_new_$X2` / `_hi` (26.0/26.5), `cl_new_$X3` / `cl_new_long3_$X` / `_hi`
  (27.0/27.5) — same sentence one level higher, and worse.
* It does **not** reach `cl_nt2` (28), `cl_nt3` (29), `cl_rebid_*` (29),
  `cl_raise_*` (30-32), `cl_negative_X*` (33) or `cl_takeout_X` (36); a hand
  with a stopper and a notrump bid, or a genuine takeout shape, is untouched.
* Fallback note: `P` is already covered by `cl_pass`, so no code fallback is
  deleted.

**VERIFIED.**  N now passes (BEN: P 1.00).  The same rung also fixes board 199
(below) — two boards, one agreement.

**Template:** none needed on suit; it is suit-blind.  Expand across the
competitive contexts instead: the identical rung belongs in
`general_competitive_high` (`ch_pass_sandwich_discipline`, priority 27.7, same
`when` with `standing_bid_level: [3, 4]`) and in `general_after_balancing_low`
if that seat can arise with our side still silent.

---

## Board 774 — margin -4

**Seat/call:** NOTHING-WRONG on the calls that were made.  Table A's `2H` by N
on `K7.QJT75.732.742` after `1D - P - 1H - X - XX - 1S` is a free bid with five
hearts opposite a redouble; the engine and BEN agree (0.94).  Table B's `3C`
is the competitive reviewer's board.

**But the support redouble has no answering seat**, and that is a constructive
defect worth shipping from here: `srd_redouble` is `establishes: {forcing:
one_round}` and there is no context for `1$m - P - 1$M - X - XX - P - ?`.  It
survived this board only because RHO bid 1S and the generic competitive ladder
took the seat.

**Missing agreement:** after opener's support redouble (exactly three-card
support, 12-21) responder rebids his major with five, signs off in two of the
major with four, or shows extras — the redouble is one-round forcing and
someone has to answer it.

**YAML** — new context (specificity 1000+6; the seat is currently unauthored,
so this shadows nothing that defines a call there):

```yaml
  - id: responder_after_support_redouble
    description: "Responder after opener's support redouble, RHO silent"
    expand: { m: [C, D], M: [H, S] }
    pattern: "1$m - P - 1$M - X - XX - P - ?"
    rules:
      - id: rasr_2$M
        call: 2$M
        priority: 62
        requires: { suits: { $M: [5, 13] }, evals: { total_points: [6, 10] } }
        shows: "five-card major opposite the promised three: the 5-3 fit at the two level"
        establishes: { forcing: non_forcing, agreed_suit: $M }
      - id: rasr_3$M
        call: 3$M
        priority: 63
        requires: { suits: { $M: [5, 13] }, evals: { total_points: [11, 12] } }
        shows: "five-card major and invitational values opposite the three-card raise"
        establishes: { forcing: invitational, agreed_suit: $M }
      - id: rasr_4$M
        call: 4$M
        priority: 64
        requires: { suits: { $M: [5, 13] }, evals: { total_points: [13, 40] } }
        shows: "five-card major and game values opposite the three-card raise"
        establishes: { forcing: sign_off, agreed_suit: $M }
      - id: rasr_pass_$M
        call: P
        priority: 55
        requires: {}
        shows: "only four in the major and no extras: the redouble stands"
        establishes: { forcing: sign_off }
```

**Answering seat for the invitation:** `rasr_3$M` is invitational, so it ships
with its own answer:

```yaml
  - id: opener_over_support_redouble_invite
    description: "Opener answers responder's invitational raise after the support redouble"
    expand: { m: [C, D], M: [H, S] }
    pattern: "1$m - P - 1$M - X - XX - P - 3$M - P - ?"
    rules:
      - id: osri_4$M
        call: 4$M
        priority: 62
        requires: { evals: { total_points: [15, 40] } }
        shows: "accepting: more than a minimum opposite the invitation"
        establishes: { forcing: sign_off, agreed_suit: $M }
      - id: osri_pass_$M
        call: P
        priority: 60
        requires: {}
        shows: "declining: a minimum opening with only three-card support"
        establishes: { forcing: sign_off, agreed_suit: $M }
```

**What it endangers:** the seat currently falls to
`general_uncontested_continuation` (`... - P - ?`), whose only fitting rung on a
six-count is `uc_pass` at fit 1.00 — a starved seat.  The new context also
carries a `requires: {}` pass, so no hand is left without a call (round 6's
`rkc5H_signoff` lesson).  Above it, nothing: `srd_*` lives one call earlier.

**UNTESTED** — the seat does not occur on this board (RHO bid 1S), so I could
not trace it end to end and will not label it VERIFIED.

**Template:** `expand: { m: [C, D], M: [H, S] }` as written — four contexts each.
The support *double* twin (`1$m - P - 1$M - bid<2$M - X - P - ?`) needs the
same treatment and is the obvious companion.

---

## Board 803 — margin -4

**Seat/call:** table A, call 1, N **passes** over 1C on `AQ85.9852.AT74.6`.
`oc1C_X` fits only 0.800 because its `any_of` branch wants `hcp: [12, 16]`.

**Missing agreement:** 4-4-4-1 with the singleton in their suit is worth the
missing king — a ten-count with perfect takeout shape doubles.

**YAML** — context `overcall_1C` (and its `1D` / `1H` / `1S` siblings):

```yaml
      - id: oc1C_X_4441
        call: X
        priority: 72.4
        requires:
          shapes: [ "4441" ]
          suits: { C: [0, 1] }
          hcp: [10, 16]
        shows: "4-4-4-1 with the singleton in their suit: perfect shape is worth the missing king"
        establishes: { forcing: one_round }
```

**Answering seat:** already authored — `advance_takeout_double_C` and the
`adx_*` family answer a takeout double of 1C, and the double is
`forcing: one_round` exactly as `oc1C_X` already is, so partner's model is
unchanged.  No new seat is required.

**What it endangers:** it outranks `oc1C_X` (72) only on hands that fit both,
which is the empty set (`oc1C_X` needs 12+ or 15+; this needs 10-16 with 4-4-4-1
and a stiff club — the 12-16 overlap makes the same call).  Below it,
`oc1C_1S` / `oc1C_1D` (70/71) — with 4-4-4-1 a one-suit overcall buries two
suits; `oc1C_pass` (25) — the rung that lost the board.  Fallback: X is already
covered by `oc1C_X`, so nothing is deleted.

**VERIFIED.**  N now doubles (BEN: X 0.79).  Control: a 4-4-3-2 ten-count with
the same honours still passes.

**Honest denominator:** `oc1C_pass` runs **-0.32 over 125 tables** and
`oc1C_X` **+0.00 over 11** — this is a carve-out from a population sitting at
baseline, so expect a small effect, not a large one.

**Template:** `expand: { o: [C, D, H, S] }` if the four `overcall_1$o` contexts
are ever merged; today they are separate, so four hand-written twins with
`suits: { <their suit>: [0, 1] }`.

---

## Board 864 — margin -4

**NOTHING-WRONG.**  Checked: table B call 5, E runs to `2S` on
`JT972.AT2.9872.5` after `1C - P - P - 1NT - X`.  `xd_run_S2` fits 1.000 on a
genuine five-card suit and `xd_pass` fits 1.000 too; running is right and BEN's
`2H` would be a three-card suit.  `xd_run_S2` runs **+0.67 over 3 tables**.
No constructive machinery is involved — the auction never gets past the runout.

The only constructive-discipline observation I have is that the runout ladder
is length-only by design (`xd_run_*` carries no point band at all), which is
the same defect I attack on board 474; the fix there covers this family too.

---

## Board 883 — margin -4

**Seat/call:** table A, call 3, S doubles on `AT73.A85.AJ3.Q93` after
`1S - P - P`.  `bal_X` fits 1.000 through its `hcp: [15, 40]` branch, which
carries **no shape condition at all** — so a takeout double is made holding
four cards in their suit.

**Missing agreement:** with three or more cards in their suit a takeout double
is a lie; a balancing 1NT with a stopper describes 15-18 as well as it
describes 11-14.

**YAML** — context `balancing_seat` (`expand: { o: [C, D, H, S] }`, already
templated):

```yaml
      - id: bal_1NT_strong
        call: 1NT
        priority: 72
        requires:
          hcp: [15, 18]
          suits: { $o: [3, 13] }
          evals: { semi_balanced: [1, 1] }
          features: [ "stopper($o)" ]
        shows: "balancing 1NT with extras: 15-18 balanced WITH length in their suit, where a takeout double would be a lie"
        establishes: { forcing: non_forcing }
```

**Answering seat:** the advance of a balancing 1NT is non-forcing, so no new
forcing seat is created; but the rung widens `bal_1NT`'s range from 11-14 to
"11-14 or 15-18 with length in their suit", and the advancer's invitational
ladder over a balancing 1NT should be widened with it.  Minimum companion:

```yaml
  - id: advance_balancing_1NT
    description: "Advancing partner's balancing 1NT"
    expand: { o: [C, D, H, S] }
    pattern: "1$o - P - P - 1NT - P - ?"
    rules:
      - id: ab1nt_2NT_$o
        call: 2NT
        priority: 56
        requires: { hcp: [10, 11] }
        shows: "invitational opposite the balancing notrump"
        establishes: { forcing: invitational }
      - id: ab1nt_3NT_$o
        call: 3NT
        priority: 57
        requires: { hcp: [12, 40] }
        shows: "game opposite the balancing notrump"
        establishes: { forcing: sign_off }
      - id: ab1nt_pass_$o
        call: P
        priority: 50
        requires: {}
        shows: "nothing extra: the balancing notrump plays"
        establishes: { forcing: sign_off }
```

**What it endangers:** `bal_X` (70) — only on 15-18 semi-balanced hands with
three or more of their suit and a stopper, which is precisely where the double
misdescribes; `bal_2NT` (71) is untouched because it wants 19-21;
`bal_1NT` (66) is untouched because its band is 11-14; `bal_S_2C/2D/2H` (64)
are untouched because they want a five-card suit.  Fallback: 1NT is already
covered by `bal_1NT`, so nothing is deleted.

**VERIFIED.**  S now bids 1NT.  Two controls pass: a 15-count with a *doubleton*
in their suit still doubles (fit 0.349 on the new rung), and a 17-count with a
doubleton still doubles.

**Honest denominator:** `bal_X` runs **-0.21 over 14 tables** — at baseline.
This is a correctness carve-out, not an attack on a losing family; rate it low
expected value and high explainability.

**Template:** `expand: { o: [C, D, H, S] }`, already the context's own
expansion — one authored rung becomes four.

---

## Board 905 — margin -4

**Seat/call:** table A, call 7, N bids **2NT** on `QJ763.T5.A986.A3` after
`P - P - 1D - 1S - P - 1NT - P`.  `uc_nt2` ("11-12 balanced, their suits
stopped") at fit 1.000, priority 28.

**Missing agreement:** my one-level overcall was limited and partner's 1NT
advance showed 6-10; eleven opposite ten is twenty-one, so there is no game and
no second call — the overcaller passes with a minimum and a five-card suit.

**YAML** — context `general_uncontested_continuation`:

```yaml
      - id: uc_pass_over_1NT_advance
        call: P
        priority: 28.5
        when: { i_have_acted: true, we_bid_last: true, standing_bid_level: [1], standing_bid_strain: [NT] }
        requires: { hcp: [8, 13], evals: { longest_suit_length: [5, 5] } }
        shows: "my one-level suit bid was limited and partner's 1NT showed 6-10: there is no game, pass"
        establishes: { forcing: sign_off }
```

(`we_bid_last`, not `we_hold_contract` — on this auction `we_hold_contract` is
`False` even though the standing 1NT is partner's.  That cost me a prototype.)

**Answering seat:** none — it is a sign-off pass that ends the auction.

**What it endangers:**
* `uc_nt2` (28) — the rung that lost the board; an eleven-count opposite a
  6-10 advance cannot make 2NT and cannot invite anything.
* `uc_nt1` (27), `uc_new_$X2/_hi` (26/26.5), `uc_new_$X3/_hi` (27/27.5),
  `uc_raise_$m3/4` (27) — all below 28.5 and all describe a hand that has
  something more to say; this rung says the hand has nothing more.
* It does **not** reach `uc_rebid_$X2/3/4` (29), `uc_nt3` (29, which runs
  **+0.48 over 46 tables** and must not be disturbed), `uc_raise_$M3/4` (31/32)
  or the `uc_doubler_*` family (33-35).
* The `when` also reaches opener's rebid after `1M - P - 1NT - P`, but that seat
  is owned by the more specific `opener_rebid_after_1M_1NT`, whose minimum
  action (`ob_1M1NT_pass`) is the same call — so a leak there is a no-op.
* Fallback: `P` is covered by `uc_pass`, so nothing is deleted.

**VERIFIED.**  N now passes (BEN: P 0.82).  Control: the same hand with a
*sixth* spade still rebids 2S (`uc_rebid_S2`, fit 1.000).

**Honest denominator:** `uc_nt2` runs **-1.57 over 21 tables** and is a standing
open item that three rounds have declined to gate.  This rung does not gate it;
it adds a better description in one narrow seat and leaves the other twenty
firings alone.

**Template:** none on suit.  The same rung belongs in
`general_competitive_low` (`cl_pass_over_1NT_advance`, priority 27.9, below
`cl_nt2`'s 28 would not work — use 28.5 there too) for the case where RHO
competes over the 1NT advance.

---

## Board 918 — margin -4

**Seat/call:** table B, call 5, W rebids **2C** on `J8.T53.AKJ3.KQ52`
(2=3=4=4, 14 HCP) after `1D - P - 1H - P`.  `ob_1D1H_2C` at priority **58**
beats `ob_1NT` at **57.5** — both at fit 1.000.

**Missing agreement:** none is missing — this is a **sibling asymmetry**, the
species round 7 named.  `ob_1NT` was deliberately raised from 55 to 57.5 with
the comment *"THE LIMIT BID BEATS THE SECOND SUIT… `ob_1D1S_2C` (priority 57)
and this rule both fit 1.00 on a 4-4 minor two-suiter that is also
semi-balanced, and the undescriptive call won on priority alone."*  The author
re-ranked `ob_1D1S_2C` to 57 and **left its `1H`-response twin at 58.**

**YAML** — context `opener_rebid_1D_1H_extras`, one number:

```yaml
      - id: ob_1D1H_2C
        call: 2C
        priority: 57          # was 58 — matches its sibling ob_1D1S_2C
        requires: { suits: { C: [4, 13], D: [4, 13] }, hcp: [10, 17], not: { any_of: [ { suits: { H: [4, 13] } }, { suits: { S: [4, 13] } } ] } }
        shows: "second suit: 4+ clubs, 10-17"
        establishes: { forcing: non_forcing }
```

**Answering seat:** unchanged and already authored — `responder_after_1NT_rebid`
answers the 1NT rebid, `responder_rebid_1D_1H_2C` answers the 2C rebid.  This
moves hands between two seats that both exist.

**What it endangers:** `ob_1D1H_2C` loses only hands that are 12-14,
semi-balanced, no four-card major, 4+ clubs and 4+ diamonds — exactly the hands
`ob_1NT` was raised to capture.  At 10-11 and 15-17 `ob_1NT` does not fit, so
2C still wins.  Nothing below 57 changes: `ob_rebid_2$m` (50), `ob_2NT` (56),
`ob_1D1H_3C_jump` (57) — the jump shift now ties at 57 with the simple 2C, but
its `hcp: [18, 21]` and 2C's `[10, 17]` are disjoint, so the tie is unreachable.

**VERIFIED.**  W now rebids 1NT (BEN: 1NT 1.00).

**Honest denominator, and it is the best support in this file:**
`ob_1D1H_2C` runs **-3.57 over 7 tables**; its already-re-ranked sibling
`ob_1D1S_2C` runs **-5.20 over 5**; and `ob_1NT` runs **-0.10 over 30**.
Routing hands out of a -3.6 rung into a -0.1 rung is the whole argument.
Caveat stated honestly: the sibling that *already* lost the priority fight to
1NT still runs at -5.20, so the re-rank alone will not repair that family.

**Template:** none — it is a one-number correction.  The sibling *lint* should
be extended to compare priorities as well as gate presence and bands; this
defect is exactly what that lint exists to catch.

---

## Board 991 — margin -4

**Seat/call:** table A, call 5, N **passes** on `AK64.KQJT2.43.A4` (17 HCP)
after `P - 1H - X - XX - 2D`.  `cl_pass` at fit 1.000; `cl_new_S2` fits only
0.349 because it wants five spades and N has four.

**Missing agreement:** `redouble_continuations` is `expand: { m: [C, D] }` —
**the major openings never got it.**  After partner's redouble the partnership
owns the hand, so opener shows a four-card second suit rather than passing.

**YAML** — two new contexts (the minor family cannot be reused as-is because
`1H`/`1S` are not legal rebids after a major opening):

```yaml
  - id: redouble_continuations_1H
    description: "Opener after 1H - (X) - XX - (their runout)"
    pattern: "1H - X - XX - bid - ?"
    rules:
      - id: rdc1h_X
        call: X
        priority: 57
        requires: { hcp: [12, 40], evals: { standing_suit_length: [3, 13] } }
        shows: "penalty: partner showed 10+ and we own this hand"
        establishes: { forcing: non_forcing }
      - id: rdc1h_2S
        call: 2S
        priority: 56
        when: { unbid_suit: S, cheapest_in_suit: true }
        requires: { suits: { S: [4, 13] } }
        shows: "natural second suit: the redouble keeps the auction ours"
        establishes: { forcing: non_forcing }
      - id: rdc1h_3C
        call: 3C
        priority: 55
        when: { unbid_suit: C, cheapest_in_suit: true }
        requires: { suits: { C: [5, 13] } }
        shows: "natural second suit at the three level: 5+ clubs"
        establishes: { forcing: non_forcing }
      - id: rdc1h_3D
        call: 3D
        priority: 55
        when: { unbid_suit: D, cheapest_in_suit: true }
        requires: { suits: { D: [5, 13] } }
        shows: "natural second suit at the three level: 5+ diamonds"
        establishes: { forcing: non_forcing }
      - id: rdc1h_2H
        call: 2H
        priority: 54
        when: { cheapest_in_suit: true }
        requires: { suits: { H: [6, 13] } }
        shows: "rebidding my six-card major"
        establishes: { forcing: non_forcing, agreed_suit: H }
      - id: rdc1h_pass
        call: P
        priority: 50
        requires: {}
        shows: "forcing pass: partner's redouble owns the auction"
        establishes: { forcing: one_round }

  - id: redouble_continuations_1S
    description: "Opener after 1S - (X) - XX - (their runout)"
    pattern: "1S - X - XX - bid - ?"
    rules:
      - id: rdc1s_X
        call: X
        priority: 57
        requires: { hcp: [12, 40], evals: { standing_suit_length: [3, 13] } }
        shows: "penalty: partner showed 10+ and we own this hand"
        establishes: { forcing: non_forcing }
      - id: rdc1s_2H
        call: 2H
        priority: 56
        when: { unbid_suit: H, cheapest_in_suit: true }
        requires: { suits: { H: [4, 13] } }
        shows: "natural second suit: the redouble keeps the auction ours"
        establishes: { forcing: non_forcing }
      - id: rdc1s_3C
        call: 3C
        priority: 55
        when: { unbid_suit: C, cheapest_in_suit: true }
        requires: { suits: { C: [5, 13] } }
        shows: "natural second suit at the three level: 5+ clubs"
        establishes: { forcing: non_forcing }
      - id: rdc1s_3D
        call: 3D
        priority: 55
        when: { unbid_suit: D, cheapest_in_suit: true }
        requires: { suits: { D: [5, 13] } }
        shows: "natural second suit at the three level: 5+ diamonds"
        establishes: { forcing: non_forcing }
      - id: rdc1s_2S
        call: 2S
        priority: 54
        when: { cheapest_in_suit: true }
        requires: { suits: { S: [6, 13] } }
        shows: "rebidding my six-card major"
        establishes: { forcing: non_forcing, agreed_suit: S }
      - id: rdc1s_pass
        call: P
        priority: 50
        requires: {}
        shows: "forcing pass: partner's redouble owns the auction"
        establishes: { forcing: one_round }
```

**Answering seat:** `rdc1h_pass` is `forcing: one_round`, and the seat that
answers a forcing pass already exists — `general_after_redouble`
(`pattern: "... - XX - $TAIL"`) owns the redoubler's next call, exactly as it
does for the minor family today.  The new contexts are a verbatim structural
clone of `redouble_continuations`, whose forcing pass has had that answer since
it was written; no new answering context is created and none is needed.

**What it endangers:** these patterns are 1000+5 specific, so they take over the
*interpretation* of the seat from `general_competitive_low` (specificity 3).
Traced: candidate generation is **not** exclusive — `cl_nt3` and the rest still
appear in the ranking after the change — so this is additive for generation and
a narrowing only for how partner reads the call.  Rungs it can outrank in the
seats it reaches: `cl_nt3` (29), `cl_rebid_jump_$X` (31), `cl_new_$X2` (26) and
`cl_pass` (20) — and in every case "partner redoubled, so we own the hand and I
am showing my second suit" is the better description.  Every context ends in a
`requires: {}` forcing pass, so no hand is starved.

**VERIFIED.**  N now bids 2S (BEN: 2S 0.32 — its top non-pass call).

**Honest denominator:** `rdc_pass_D` — the minor family's forcing pass — runs
**-6.75 over 4 tables**, the worst rate of anything I measured.  The redouble
family is small and badly broken; that is the case for building it out rather
than tuning it.

**Template:** as written, two contexts.  If the four openings are ever unified,
`expand_pairs` over `{O: 1H, N: S}`, `{O: 1S, N: H}` collapses the second-suit
rung; the level-dependent rungs resist templating because 1H's cheap second
suit is at the two level and 1S's is not.

---
