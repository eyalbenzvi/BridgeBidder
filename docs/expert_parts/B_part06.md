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

## Board 23 — margin -3

**Seat/call:** table B, call 4, W **passes** on `K63.98.AQJT7.Q76` after
`1D - X - XX - 1H`.  `rdc_pass_D` ("forcing pass") at fit 1.000 — and it is the
only rung in `redouble_continuations` that fits, because the context has
**X, 1H, 1S and pass, and no notrump rung at all.**

**Missing agreement:** a balanced minimum with their runout suit short and a
stopper bids notrump; the forcing pass is for hands with nothing to say, not for
hands with a notrump bid.

**YAML** — context `redouble_continuations` (`expand: { m: [C, D] }`):

```yaml
      - id: rdc_1NT_$m
        call: 1NT
        priority: 54
        requires:
          hcp: [12, 15]
          evals: { semi_balanced: [1, 1], standing_suit_length: [0, 2] }
        shows: "natural 1NT: a balanced minimum with their runout suit short, the redouble owning the auction"
        establishes: { forcing: non_forcing }
      - id: rdc_2NT_$m
        call: 2NT
        priority: 53
        requires:
          hcp: [16, 18]
          evals: { semi_balanced: [1, 1], standing_suit_length: [0, 2] }
        shows: "natural 2NT: 16-18 balanced with their runout suit short"
        establishes: { forcing: non_forcing }
```

Note on the gate: I deliberately did **not** use `stopper(their)` or
`weakest_their_stopper`.  `suit_length(their)` resolves to LHO's suit, and on
this auction LHO is the *doubler* and has no suit at all;
`weakest_their_stopper` has no sharp tolerance and does not gate.
`standing_suit_length` is the evaluator that means "their runout suit", and
round 4 added it for exactly this reason.

**Answering seat:** 1NT and 2NT are `non_forcing`, so nothing is forced; the
redoubler's next call is owned by `general_after_redouble`, unchanged.  The
invitational content lives in the two disjoint bands, so partner can raise on
values — the same treatment `bal_1NT` / `bal_2NT` already gets.

**What it endangers:** `rdc_pass_$m` (50) — the rung that lost the board;
`rdc_suit_S_$m` (55) and `rdc_suit_H_$m` (56) are *above* 54 and keep priority,
so a genuine four-card major is still bid first, which is right.  `rdc_X_$m`
(57) is above and keeps priority, so a penalty pass/double with length in their
suit is untouched (and `standing_suit_length: [0, 2]` makes the two rules
mutually exclusive anyway).  Fallback: 1NT/2NT were **not** covered in this
context, so this rung does delete the generic `FALLBACK` notrump for those
calls in this seat — an improvement, since the fallback shows "11-14 with
stoppers (undiscussed)" and this shows a band.

**VERIFIED.**  W now bids 1NT (BEN: 1NT 0.73).

**Honest denominator:** `rdc_pass_D` **-6.75 over 4 tables**.  Small n, terrible
rate, and the mechanism is visible rather than inferred (a four-rung context
with no notrump).

**Template:** `expand: { m: [C, D] }`, the context's own expansion.  The two
new major contexts from board 991 want the same pair of rungs
(`rdc1h_2NT` / `rdc1s_2NT`, since 1NT is not available there).

---

## Board 27 — margin -3

**NOTHING-WRONG.**  Purely a preempt-style board and outside my discipline.
Checked: W holds `JT6.K976542.T2.2` in first seat, vulnerable — 4 HCP,
`suit_quality(H)` = 1.0, `total_points` = 7.0.  `open_3H_vul` wants
`hcp: [5, 9]` and a decent suit, so it fits 0.800 and loses to `open_pass` at
fit 1.000; `open_weak_2H_vul` fits 0.035.  Both refusals are the system's own
documented discipline ("preempts at the 3-level: 7+ cards, 4-9 HCP, **good
suit**"; K9765 42 is not a good suit vulnerable).

Constructive-discipline observation, recorded not proposed: the vulnerable
three-level preempt has a *floor* at 5 HCP and the weak two a floor at 7, so a
seven-card suit with four points has no opening call at any level when
vulnerable.  That is the "ceiling" species upside down and it is a real hole,
but its repair is opening style, which the brief scopes out.

---

## Board 76 — margin -3

**NOTHING-WRONG.**  Fourth-seat rule-of-15 threshold on `86.AT.KJ9864.Q43`;
`open_1D` fits 0.409 and `open_1D_rule15` 0.134 against `open_pass_4th` at
1.000.  Opening-style / rule-of-20 thresholds are on the do-not-re-propose
list, and nothing constructive happens after the pass-out.

---

## Board 78 — margin -3

**Seat/call:** table A, call 8, S bids **3D** on `AK.53.AT9875.A85` after
`1D - 1H - P - P - 2D - 2H - P - P`.  `ballow_rebid_D3` at fit 1.000,
priority 29.  This is opener's **third** bid and partner has never made a call.

**Missing agreement:** partner has passed my opening and passed my rebid; with
fewer than seventeen points and no seventh card there is no third bid.

**YAML** — context `general_after_balancing_low` (the `ballow_*` context):

```yaml
      - id: ballow_pass_partner_silent
        call: P
        priority: 29.5
        when: { i_have_acted: true, partner_has_acted: false, standing_bid_level: [2], their_last_bid_suit: true }
        requires:
          hcp: [12, 16]
          evals: { longest_suit_length: [0, 6] }
        shows: "partner has never acted over their two-level bid: without seventeen points or a seventh card there is no third bid"
        establishes: { forcing: sign_off }
```

**Answering seat:** none — a sign-off pass.

**What it endangers,** in the seats its `when` reaches (I have bid, partner never
has, the standing bid is theirs at the two level):
* `ballow_rebid_$X3` (29) — the rung that lost the board; a fourth call in the
  same suit opposite a partner who could not make a first one.
* `ballow_new_$X3` / `ballow_new_long3_$X` (27) — introducing a *new* suit at the
  three level opposite a silent partner is worse still.
* `ballow_nt2` (28) and `ballow_nt3` (29) — same argument; if I had 17 the rung
  does not fit and they are free.
* It does **not** reach `ballow_nt2_strong` (30), `ballow_reopen_X` (41), or
  any rung above 29.5, so a genuine 17+ reopening double or strong notrump is
  untouched — and the `hcp: [12, 16]` band makes those hands miss the rung
  anyway.
* Fallback: `P` is covered by `ballow_pass`, so nothing is deleted.

**VERIFIED.**  S now passes (BEN: P 0.75).  Control: the same shape with 19 HCP
still bids 3D (`ballow_rebid_D3`, the new rung at fit 0.0 on the hcp band).
The same rung **also fixes board 230** (below) — two boards, one agreement.

**Honest denominator:** `ballow_rebid_D3` **-1.50 over 2 tables**,
`ballow_new_C3` **-0.25 over 4** — both small.  The agreement is worth having on
explainability; do not expect it to move the number on its own.

**Template:** none on suit.  The identical rung belongs in
`general_after_balancing_high` with `standing_bid_level: [3, 4]`.

---

## Board 98 — margin -3

**Seat/call:** table A, call 2, N doubles on `AKQJ93.AJ5..7632` over `P - 3D`.
`v3_D_X` (70) and `v3_D_S` (64) both fit 1.000; priority alone chose the double,
and partner bid nothing while E jumped to 5D.

**Missing agreement:** with a self-sufficient six-card major and a void in their
suit you name the trump suit; the takeout double is for hands that can stand any
answer, and this one cannot stand a diamond answer it has no diamonds for.

**YAML** — context `defense_vs_preempt_D` (and its C / H / S siblings):

```yaml
      - id: v3_D_S_solid
        call: 3S
        priority: 71
        requires:
          suits: { S: [6, 13], D: [0, 1] }
          hcp: [13, 40]
          evals: { "suit_quality(S)": [3.5, 9] }
        shows: "a self-sufficient six-card spade suit and a void in theirs: name the trump suit, do not ask"
        establishes: { forcing: non_forcing }
```

**Answering seat:** already authored — the overcall of a preempt is answered by
the same advance machinery that answers `v3_D_S` today, and the new rung makes
the identical call with a narrower meaning.  No new seat.

**What it endangers:** `v3_D_X` (70) — only on 13+ hands with a 3.5-quality
six-card major and at most a singleton in their suit.  `v3_D_3NT` (66) — with a
running major and a void in their suit, 3NT is a worse contract than the major
(this board: 3S makes eleven, 3NT makes six).  `v3_D_4S` (65) is above nothing
it should not be; `v3_D_S` (64) makes the same call.

**VERIFIED.**  N now bids 3S (BEN: 3S 0.97).

**LOW CONFIDENCE, and the reason is a whole-corpus denominator:** `v3_D_X` runs
**+1.60 over 5 tables** — it is a *profitable* rung and this carve-out takes
hands out of it.  The gate is deliberately narrow (six-card suit, quality 3.5+,
at most a singleton in their suit, 13+) so that it reaches only the hands where
the double is structurally wrong.  If a consolidator wants to cut one proposal
from this file, cut this one.

**Template:** `expand_pairs` over the four preempt suits × the two majors —
`{o: C, M: H}`, `{o: C, M: S}`, `{o: D, M: H}`, `{o: D, M: S}`, `{o: H, M: S}`,
`{o: S, M: H}` — six rules, if the `defense_vs_preempt_*` contexts are merged;
today they are four hand-written contexts and this is six hand-written rungs.

---

## Board 103 — margin -3

**NOTHING-WRONG.**  Table A, call 3: S overcalls 2C on `KJ9.9762.K.AQJT5`
(14 HCP, `suit_quality(C)` = 3.0) in the sandwich seat after `1S - P - 1NT`.
`sw_2C` requires "good 5+ clubs, 11-17" and fits 1.000; the hand is exactly what
the agreement describes and BEN's pass is a judgement call, not a system gap.
The board was lost to the play (six tricks in 2C), not to the auction.

Recorded for the competitive reviewer: `sw_2C` runs **-2.75 over 8 tables** and
`sw_2S` **-4.50 over 2** — the whole sandwich family is losing money, and that
is a *family* verdict, not something a rung on this board can carry.

---

## Board 166 — margin -3

**Seat/call:** table A, call 4, S **passes** on `AT8.Q74.A3.QJT32` after
`1C - 1D - 1H - 1S`.  `cl_pass` at fit 1.000; the code `FALLBACK` X sits under
it at priority 9.

**Missing agreement:** the support double.  The file HAS it — `sd_double`,
"exactly 3-card $M support, any strength", priority 85 — but its context is
`pattern: "1$m - P - 1$M - bid<2$M - ?"`, which requires **LHO to have passed**.
The moment LHO overcalls, the agreement disappears and opener has no way to show
exactly three-card support.  This is a `when`-shaped hole in the file's own
canonical negative-inference convention.

**YAML** — rungs inside `general_competitive_low` (no `expand:` there, so four
rules; the `when` gate is what keeps it narrow):

```yaml
      - id: cl_support_X_CH
        call: X
        priority: 36.5
        when: { my_suit: C, partner_last_suit: H, standing_bid_level: [1], their_last_bid_suit: true }
        requires: { suits: { H: [3, 3] }, hcp: [12, 21] }
        shows: "support double: exactly three hearts for partner's free one-level response"
        establishes: { forcing: non_forcing }
        alertable: true
        convention: support_double
      - id: cl_support_X_CS
        call: X
        priority: 36.5
        when: { my_suit: C, partner_last_suit: S, standing_bid_level: [1], their_last_bid_suit: true }
        requires: { suits: { S: [3, 3] }, hcp: [12, 21] }
        shows: "support double: exactly three spades for partner's free one-level response"
        establishes: { forcing: non_forcing }
        alertable: true
        convention: support_double
      - id: cl_support_X_DH
        call: X
        priority: 36.5
        when: { my_suit: D, partner_last_suit: H, standing_bid_level: [1], their_last_bid_suit: true }
        requires: { suits: { H: [3, 3] }, hcp: [12, 21] }
        shows: "support double: exactly three hearts for partner's free one-level response"
        establishes: { forcing: non_forcing }
        alertable: true
        convention: support_double
      - id: cl_support_X_DS
        call: X
        priority: 36.5
        when: { my_suit: D, partner_last_suit: S, standing_bid_level: [1], their_last_bid_suit: true }
        requires: { suits: { S: [3, 3] }, hcp: [12, 21] }
        shows: "support double: exactly three spades for partner's free one-level response"
        establishes: { forcing: non_forcing }
        alertable: true
        convention: support_double
```

**Answering seat.**  Deliberately `forcing: non_forcing`, **not** the
`one_round` that `sd_double` uses, and the choice is the whole design: in a
competitive auction partner must be free to pass the double for penalties, and
authoring a new one-round force into the busiest generic context in the file
without a dedicated answering seat is precisely the -9.8-IMPs-a-seat mistake
round 17 measured.  The seat that answers it is
`general_competitive_low` / `_high` itself: partner's `cl_raise_$M2/3/4` rungs
now read the double as three-card support, `cl_pass` converts it, and both
already exist.  If a later round wants the force, it must ship
`1$m - bid - 1$M - bid - X - P - ?` with it.

**What it endangers,** in the seats its `when` reaches (I bid a minor, partner's
last suit is a major, RHO's bid is theirs at the one level):
* `cl_takeout_X` (36) — with exactly three cards in partner's major, "short in
  their suit, opening values" is the wrong description and support is the right
  one.  `cl_takeout_X` fires **once** in the corpus, at -10.
* the code `FALLBACK` X at priority 9 — deleted in these seats, and replaced by
  a described call rather than "takeout-flavored cooperative double
  (undiscussed)".  This is the one genuine subtraction and it is an upgrade.
* It does **not** reach `cl_nt2_direct` (37) or anything above.
* Below it, nothing changes: the rungs at 33-35 are doubler-side raises and
  negative doubles whose `when` cannot co-occur with "I opened a minor and
  partner responded".

**VERIFIED.**  S now doubles (BEN: X 1.00).  Control: with **four** hearts the
support double correctly does not fire (fit 0.349) and the raise ladder keeps
the seat.

**Template:** four hand-written rules as above (the context has no `expand:`).
If `general_competitive_low` is ever given `expand_pairs`, this collapses to one
rule over `{m: C, M: H}`, `{m: C, M: S}`, `{m: D, M: H}`, `{m: D, M: S}` — and
the same four belong in `general_competitive_high` for RHO's two-level actions
below 2 of the major, which is where the real support double lives.

---

## Board 198 — margin -3

**Seat/call:** table A, call 10, N bids **3H** on `AKJ.87532.54.AJ7` after
`P - P - 1H - P - 2H - P - P - X - P - 3C`.  `ch_raise_H3` at fit 1.000,
priority 31 — a rung written to raise **partner's** suit, applied to a suit N
opened himself, over a partner who has already limited himself with a simple
raise.  `partner_shown_max` = 11, `total_points` = 14,
`lott_total_trumps(H)` = 8.

**Missing agreement:** partner's raise already showed his hand; with only eight
trumps and no extras the Law says sell out rather than compete to the three
level.

**YAML** — context `general_competitive_high`, two rules (no `expand:`):

```yaml
      - id: ch_sell_out_H
        call: P
        priority: 31.5
        when: { my_suit: H, partner_last_suit: H, their_last_bid_suit: true }
        requires: { evals: { partner_shown_max: [0, 11], total_points: [0, 15], "lott_total_trumps(H)": [0, 8] } }
        shows: "partner's raise showed his hand, we hold only eight trumps and I have no extras: the Law says sell out"
        establishes: { forcing: sign_off }
      - id: ch_sell_out_S
        call: P
        priority: 31.5
        when: { my_suit: S, partner_last_suit: S, their_last_bid_suit: true }
        requires: { evals: { partner_shown_max: [0, 11], total_points: [0, 15], "lott_total_trumps(S)": [0, 8] } }
        shows: "partner's raise showed his hand, we hold only eight trumps and I have no extras: the Law says sell out"
        establishes: { forcing: sign_off }
```

**Answering seat:** none — a sign-off pass.

**What it endangers:**
* `ch_raise_$M3` (31) — only where I bid the suit myself, partner raised it,
  we hold eight trumps and I hold at most fifteen total points.  Outside that
  the rung does not fit and `ch_raise_H3` (+/-: **-2.33 over 3 tables**) is free.
* `ch_free_3$M` (30), `ch_neg_major_*` (30), `ch_rebid_*` (29), `ch_nt3` (29),
  `ch_new_*` (27-28.5) — all below and all describe a hand with something more.
* It does **not** reach `ch_raise_$M4` / `ch_raise_lott4_$M` (32) — and that
  matters, because `ch_raise_lott4_S` runs **+3.57 over 7 tables** and must not
  be touched — nor `ch_negative_X3` (33) or `ch_penalty_X` (38).
* Fallback: `P` is covered by `ch_pass`, so nothing is deleted.

**VERIFIED.**  N now passes (BEN: P 0.83).  Control: give N a **sixth** heart
(nine trumps) and `ch_raise_H3` fires again, as it should.

**Template:** two rules as written; if `general_competitive_high` ever gets
`expand: { M: [H, S] }` this is one rule.  The minor twin
(`ch_sell_out_$m` with a nine-trump ceiling) is the obvious companion but wants
its own evidence — a minor partscore battle is a different animal.

---

## Board 199 — margin -3

**Seat/call:** table A, call 7, S bids **3H** on `AT.QJT963.K3.652` after
`1S - P - 1NT - P - 2D - P - 2S` — having correctly passed at call 3 when
`sw_2H` did not fit (10 HCP against an 11-17 band).  `cl_new_long3_H_hi`
at fit 1.000.

**Missing agreement:** the same one as board 646 — both of them have bid and
described a fit, my side has never acted, and a ten-count with a six-card suit
is not a three-level entry after passing at the two level.

**YAML:** identical rung to board 646, `cl_pass_sandwich_discipline` in
`general_competitive_low`.  One agreement, two boards.

**Answering seat:** none — a pass.

**What it endangers:** as listed on board 646.  For this board specifically it
outranks `cl_new_long3_H` / `_hi` (27.0 / 27.5), both of which report
**"never fires"** in the whole-corpus primary reading — i.e. this family is
never the recorded rule and its real behaviour is invisible to
`fires_summary`.  Stated as a caveat, not as support.

**VERIFIED.**  S now passes (BEN: P 1.00).

**Prototype I tried and am NOT shipping:** a looser sandwich overcall
(`sw_2H_long`: six-card suit, 8-16, `suit_quality >= 2`, priority 65.5) fires on
this hand and would have bid 2H at call 3, which BEN prefers (0.67).  It is
withdrawn on the whole-corpus denominator: `sw_2H` runs **-2.67 over 6 tables**,
`sw_2C` **-2.75 over 8**, `sw_2S` **-4.50 over 2**.  Adding *more* sandwich
overcalls to a family losing 2.7 IMPs a table is the wrong direction, and the
pass rung fixes the board from the other end.

**Template:** as board 646.

---

## Board 230 — margin -3

**Seat/call:** table A, call 4, S bids **3C** on `A2.A96.QT8.AJT84` after
`1NT - 2D - P - P` — reopening on his own 1NT opening with a five-card suit
after partner could not act.  `ballow_new_C3` at fit 1.000.

**Missing agreement:** the same one as board 78 — partner has never acted over
their two-level bid, so without seventeen points or a seventh card there is no
third bid.  (There is also a genuine *inference* defect underneath it, recorded
below: `partner_shown_max` reads **40** here, so the engine does not know that
responder's pass over a 2D overcall of our 1NT limits him at all.  That is a
partner-model repair, not a rule, and I am not proposing it.)

**YAML:** identical rung to board 78, `ballow_pass_partner_silent`.

**Answering seat:** none — a sign-off pass.

**What it endangers:** as listed on board 78.  Here specifically it outranks
`ballow_new_C3` (27) and `ballow_new_long3_C` (27), both of which describe a
hand with somewhere to play; against a silent partner and a 15-count facing a
two-level overcall, staying at the two level is the better description.
`ballow_nt2_strong` (30) is above the rung and untouched, so a 17-21 balanced
reopening notrump is still available.

**VERIFIED.**  S now passes (BEN: P 0.96).

**Template:** as board 78.

---

## Board 258 — margin -3

**Seat/call:** table A, call 2, N **passes** on `75.Q95.Q965.KQJ2` after
`2D - 2S`.  `cl_pass` at 1.000; `cl_raise_D3` fits **0.028** and `cl_raise_D4`
**0.000**, because both are gated on high-card values
(`total_points`, `rule_of_26`) when the hand in question is a ten-count with
**four-card support opposite a six-card weak two — ten trumps.**
`partner_shown_max` = 10, `lott_total_trumps(D)` = 10.

**Missing agreement:** the Law of Total Tricks.  Opposite a partner who is
limited to ten points, the level is set by the number of trumps, not by the
number of points; the file has **zero** rules that say so at the three level and
its four-level Law rungs (`cl_raise_lott4_$M`) are majors-only and additionally
gated on values.

**YAML** — context `general_competitive_low`, written out per suit (I show
diamonds; the same four-suit set is the proposal):

```yaml
      - id: cl_raise_law_D3
        call: 3D
        priority: 30.6
        when: { partner_last_suit: D }
        requires: { evals: { "lott_total_trumps(D)": [9, 9], partner_shown_max: [0, 10], total_points: [6, 40] } }
        shows: "the Law opposite a limited partner: nine trumps, compete to the three level"
        establishes: { forcing: non_forcing, agreed_suit: D }
      - id: cl_raise_law_D4
        call: 4D
        priority: 31.6
        when: { partner_last_suit: D }
        requires: { evals: { "lott_total_trumps(D)": [10, 26], partner_shown_max: [0, 10], total_points: [6, 40] } }
        shows: "the Law opposite a limited partner: ten trumps, compete to the four level"
        establishes: { forcing: non_forcing, agreed_suit: D }
```

**Answering seat:** both are `non_forcing` raises that set `agreed_suit`, and
the seat that answers a raise of a preempt already exists — partner is a limited
hand who has told his story and passes; `cl_pass` / `ch_pass` / `uc_pass` all
fit 1.00 for him.  Setting `agreed_suit` is deliberate: it is what makes the
`gf_landing` and keycard families reachable if the auction ever gets that far,
and it stops a later rung inventing a different trump suit.

**What it endangers — and the priorities are chosen defensively:**
* At **30.6** the three-level Law raise sits **below** `cl_raise_$X3` (31), and
  at **31.6** the four-level one sits **below** `cl_raise_$X4` /
  `cl_raise_lott4_$X` (32).  That is on purpose: `ch_raise_lott4_S` runs
  **+3.57 over 7 tables** and `ch_raise_S3` **+1.83 over 6** — these are
  profitable families and the new rung must not outrank them.  Where the
  existing rung fits >= 0.9 it still wins; where it does not (this board:
  0.028), the fast path fails and the blended score hands the seat to the Law
  rung at fit 1.000.
* Below: `cl_raise_$X2` (30), `cl_new_$X2/3` (26-27.5), `cl_pass` (20) — the
  rung that lost the board.
* Fallback: 3D/4D are already covered by `cl_raise_$X3/4` in this context, so
  nothing is deleted.

**VERIFIED.**  N now bids 4D (BEN: 4D 0.62), the contract BEN reached at the
other table.

**Template:** eight rules in `general_competitive_low` (four suits × two levels)
and eight in `general_competitive_high`; `expand: { X: [C, D, H, S] }` if those
contexts are ever templated.  This is the single largest templating opportunity
in my slice: **control-showing and Law-based raises are two of the five
conventions round 17 counted at zero rules.**

---

## Board 344 — margin -3

**NOTHING-WRONG.**  Third-seat opening judgement on `.AT2.KT543.K9865` (10 HCP,
spade void): `open_1D_rule20_third` fits 1.000 and BEN would open 2D.
Opening-style and rule-of-20 thresholds are on the do-not-re-propose list, and
the rest of the auction (`rx_D_1S`, then two passes) is correct given the 1D.

---

## Board 433 — margin -3 — **PROPOSAL WITHDRAWN, and this is the round's most useful negative**

**Seat/call:** table A, call 3, N bids **3D** on `T.74.AJT9872.KQ5` after
`P - 2S - 3C`.  `ch_new_long3_D_hi` at fit 1.000, priority 27.5.
`partner_shown_max` = 10, `total_points` = 13, `lott_total_trumps(D)` = 7 —
partner is limited, I have thirteen, and there is no fit anywhere.

**The agreement I drafted:** do not introduce a new suit at the three level
opposite a limited partner without a fit or fourteen points —
`ch_pass_limited_B` (priority 27.6, `partner_shown_max: [0, 11]`,
`total_points: [0, 15]`).  It works: **traced, N passes** (BEN: P 0.99).

**Why it is withdrawn.**  `fires_summary('reports/r18_before.jsonl',
'ch_new_long3_D')` returns **+13 IMPs over 3 tables, mean +4.33** — the rung it
would outrank is the most profitable thing I measured in this whole slice, and
this board is its only loser.  A rung placed above it takes two winners with the
loser.  Round 17 asked reviewers to re-score a suspect rule across all its
firings before accusing it; this is what that instruction is for.

**What I ship instead:** nothing for this board.  Marked **NOTHING-WRONG on the
evidence**, with the diagnosis recorded so a later round with a bigger
denominator can revisit it.

The *narrower* sibling `ch_pass_limited_A` (`partner_shown_max: [0, 8]`,
`total_points: [0, 17]`) survives and is proposed on board 548 — a weak two
shows a maximum of ten, so A cannot reach the preempt-advance seats where
`ch_new_long3_*` earns its money.  That separation was the point of splitting
the two bands.

---

## Board 474 — margin -3

**Seat/call:** table B, call 7, E bids **3C** on `Q97.Q.76.AJT8753` after
`P - 1H - X - 2C - P - 2H - P`.  `uc_rebid_C3` at fit 1.000.  The auction went
wrong one call earlier, at call 3: `xd_run_C2` shows **"running to my own C: 5+
cards"** and carries **no point band whatsoever**, so opener cannot tell three
points from ten and rebids his own suit; E then bids clubs again.

**Missing agreement:** the runout from their takeout double is a two-tier
structure — the cheap suit bid is 0-7, and a **jump** in the suit shows a
six-card suit and 8-10, a one-bid hand that partner must pass.  This is an
invitational structure the file simply does not have; today the whole 0-10 range
makes the same call, and the existing `xd_run_$X3` is unreachable because it
carries `cheapest_in_suit: true` and a jump is by definition not the cheapest
bid (the same broken gate `DECISIONS` records on `cl_raise_lott3_$M`).

**YAML** — context `general_after_their_double` (the `xd_*` context):

```yaml
      - id: xd_run_jump_C
        call: 3C
        priority: 27
        when: { we_bid_last: true, we_hold_contract: false, unbid_suit: C }
        requires:
          suits: { C: [6, 13] }
          evals: { total_points: [10, 14] }
        shows: "jump runout: a six-card club suit and 8-10 points, a one-bid hand - partner must pass"
        establishes: { forcing: sign_off }
      - id: xd_run_jump_D
        call: 3D
        priority: 27
        when: { we_bid_last: true, we_hold_contract: false, unbid_suit: D }
        requires:
          suits: { D: [6, 13] }
          evals: { total_points: [10, 14] }
        shows: "jump runout: a six-card diamond suit and 8-10 points, a one-bid hand - partner must pass"
        establishes: { forcing: sign_off }
```

**THE ANSWERING SEAT — and it is what makes the difference.**  Prototyped
without it, the jump changed nothing: E jumped to 3C and opener bid 3H anyway
(`uc_rebid_H3`, fit 1.000), because no seat reads a jump runout.  That is the
round-17 lesson reproduced exactly, so the answering context ships with it:

```yaml
  - id: opener_over_jump_runout
    description: "Opener after responder's jump runout from their takeout double"
    expand_pairs:
      - { M: H, m: C }
      - { M: H, m: D }
      - { M: S, m: C }
      - { M: S, m: D }
    pattern: "1$M - X - 3$m - P - ?"
    rules:
      - id: oojr_3$M
        call: 3$M
        priority: 62
        requires: { suits: { $M: [6, 13] }, evals: { total_points: [17, 40] } }
        shows: "17+ with a genuine six-card major: correcting above the jump"
        establishes: { forcing: non_forcing, agreed_suit: $M }
      - id: oojr_3NT_$m
        call: 3NT
        priority: 61
        requires: { hcp: [16, 21], evals: { semi_balanced: [1, 1], "suit_length($m)": [2, 13] } }
        shows: "16+ balanced with a fit for the jump suit: nine tricks"
        establishes: { forcing: sign_off }
      - id: oojr_pass_$m
        call: P
        priority: 60
        requires: {}
        shows: "the jump runout showed 8-10 and one suit: pass"
        establishes: { forcing: sign_off, agreed_suit: $m }
```

**What it endangers:**
* The jump rung deletes the code fallback for 3C/3D in the seats its `when`
  reaches, because `xd_run_$X3`'s own `cheapest_in_suit` gate means 3C is
  **not** currently covered when 2C is legal.  That is the one genuine
  subtraction; it replaces an undiscussed fallback with a described call.
* `xd_run_$X2` (25) and `xd_run_$X1` (24) keep every hand below ten total
  points — the bands are disjoint by construction, so the cheap runout is
  untouched for the hands it was written for.
* `rdx_XX` (75) and `rx_$M_1$N` (62) are far above and unaffected; the jump only
  ever wins where nothing above it fits.
* The answering context is 1000+4 specific in a seat previously owned by
  `general_uncontested_continuation` (`... - P - ?`), whose `uc_rebid_H3` bid
  the losing 3H.  It carries a `requires: {}` pass, so no hand is starved.

**VERIFIED end to end.**  `P - 1H - X - 3C - P - P`: E jumps, W passes, we play
3C, which makes nine tricks double-dummy against the 3H that went two down.

**Honest denominators:** `xd_run_C2` **-3.00 over 9 tables**, `uc_rebid_C3`
**-2.10 over 10** — both halves of this auction lose money at present.

**Template:** two rungs above become eight with the majors
(`xd_run_jump_H` / `_S` at the two and three level as the level allows); the
answering context as written is `expand_pairs` over four combinations, and the
minor-opening twin (`1$m - X - 2$M - P - ?`) is the obvious next four.

---

## Board 506 — margin -3 — **the most important agreement in this slice**

**Seat/call:** table B, call 7, E **passes** on `QJ9753.73.J973.9` after
`P - 1C - P - 1S - P - 2H - P`.  **Partner reversed.  A reverse is
`forcing: one_round`.  We passed it.**

`responder_reverse_1C1S2H` has four rungs — `rrevh_2S` (5+ spades, **8+**),
`rrevh_3H` (4+ hearts, **8+**), `rrevh_2NT` (**8-11** balanced), `rrevh_3NT`
(**12+**).  Every one floors at eight points.  A four-count with six spades
fits nothing above 0.028 and `uc_pass` takes the force at fit 1.00.  This is
the fourth instance of the starved-forcing-seat species the method file records,
and `rrevh_2S` **never fires** in the whole corpus.

**Missing agreement:** a reverse is forcing, so responder always bids: with a
five-card suit he rebids it at the cheapest level to show 0-7, and with no
five-card suit he takes a preference to opener's first suit at the three level.

**YAML** — context `responder_reverse_1C1S2H` (and its two siblings, see
Template):

```yaml
      - id: rrevh_2S_min
        call: 2S
        priority: 67
        requires: { suits: { S: [5, 13] }, hcp: [0, 7] }
        shows: "5+ spades, under 8 points: the cheap rebid a forcing reverse must not be passed with"
        establishes: { forcing: non_forcing }
      - id: rrevh_3C_min
        call: 3C
        priority: 58
        requires: { hcp: [0, 7] }
        shows: "under 8 points and no five-card suit: preference to opener's first suit"
        establishes: { forcing: non_forcing, agreed_suit: C }
```

**THE ANSWERING SEAT** — opener has 17-21 and has just been told 0-7, and
nothing in the file reads that:

```yaml
  - id: opener_after_reverse_signoff
    description: "Opener after responder's minimum rebid over the reverse"
    expand_pairs:
      - { O: 1C, R: 2H, M: S }
      - { O: 1D, R: 2H, M: S }
      - { O: 1C, R: 2D, M: H }
      - { O: 1C, R: 2D, M: S }
    pattern: "$O - P - 1$M - P - $R - P - 2$M - P - ?"
    rules:
      - id: oars_4$M
        call: 4$M
        priority: 63
        requires: { suits: { $M: [3, 13] }, evals: { total_points: [20, 40] } }
        shows: "a big reverse with a fit: game in partner's suit even opposite a bust"
        establishes: { forcing: sign_off, agreed_suit: $M }
      - id: oars_3$M
        call: 3$M
        priority: 62
        requires: { suits: { $M: [3, 13] }, evals: { total_points: [18, 19] } }
        shows: "three-card support and a maximum reverse: inviting the 0-7 rebid to game"
        establishes: { forcing: invitational, agreed_suit: $M }
      - id: oars_pass_$M
        call: P
        priority: 60
        requires: {}
        shows: "the reverse has been answered with 0-7: this is the partscore"
        establishes: { forcing: sign_off, agreed_suit: $M }
```

(`oars_3$M` is itself an invitation; the seat that answers **it** is the same
`responder_reverse_*` family one call later and wants a two-rung
`1$O - P - 1$M - P - $R - P - 2$M - P - 3$M - P - ?` context — pass with 0-4,
4$M with 5-7.  I have not written it out because the 18-19 branch is rare
enough that shipping the pass and the game first is the safer order; flag it as
the one loose end in this proposal.)

**What it endangers:**
* `rrevh_2S` (66) — disjoint band (8+ against 0-7), so nothing moves; the two
  rungs together turn one call into a two-way reading, which is a *gain* in
  negative inference, not a loss.
* `rrevh_2NT` (64) and `rrevh_3NT` (63) — both want 8+, so the new rungs cannot
  outrank them on a hand they fit.
* `rrevh_3H` (65) — a weak hand with four hearts now has a choice between 3H
  (game-forcing raise, 8+) and 3C; the bands separate them.
* The generic `uc_*` toolkit loses the seat, which is the entire point: it was
  answering a one-round force with a catch-all pass.
* The answering context is 1000+9 specific over a seat previously owned by
  `general_uncontested_continuation`; it carries a `requires: {}` pass so no
  hand is starved.

**VERIFIED end to end.**  `1C - P - 1S - P - 2H - P - 2S - P - P`: responder
bids 2S at fit 1.000, opener passes, we play 2S making nine double-dummy where
we previously passed 2H out.

**Template:** `rrevh_2S_min` / `rrevh_3C_min` are one authored idea that must be
cloned into all three reverse contexts —
`responder_reverse_1C1S2H` (2S / 3C), `responder_reverse_1D1S2H`
(`rrevd_2S_min` / `rrevd_3D_min`) and `responder_reverse_rebid_major`
(`rrev_2$M_min` / `rrev_3C_min`, which is already `expand: { M: [H, S] }` and
therefore two rules from one).  Six rules from one agreement, plus the four
answering contexts above.

---

## Board 512 — margin -3

**Seat/call:** table A, call 2, S **passes** on `8632.AQJ.KJ4.K85` over
`P - 1C`.  `oc1C_1NT` fits 0.800 (14 against a 15-18 band) and `oc1C_X` 0.349
(K85 is three clubs, not the "short clubs" the double wants), so `oc1C_pass`
at 1.000 wins the seat with a 14-count and a four-card major.

**Missing agreement:** a takeout double of a **minor** does not need shortness
when the hand is balanced with a four-card major — 13-16 flat with at most three
of their minor is a double, not a pass.

**YAML** — context `overcall_1C` (and its `1D` sibling):

```yaml
      - id: oc1C_X_bal
        call: X
        priority: 72.5
        requires:
          hcp: [13, 16]
          suits: { C: [0, 3] }
          evals: { balanced: [1, 1] }
          any_of: [ { suits: { H: [4, 13] } }, { suits: { S: [4, 13] } } ]
        shows: "balanced 13-16 with a four-card major and no club length: the double, not a pass"
        establishes: { forcing: one_round }
```

**Answering seat:** already authored — `advance_takeout_double_C` / the `adx_*`
family, and the double is `forcing: one_round` exactly as `oc1C_X` already is.
No new seat.

**What it endangers:** `oc1C_X` (72) — same call, and the new rung's band is
inside the old rung's, so it changes the *reading* (balanced with a major)
rather than the call.  `oc1C_1S` (71) — with only four spades a one-level
overcall is a lie in this system (`5+ spades`).  `oc1C_1NT` (82) is above it and
untouched, so 15-18 balanced still bids notrump.  `oc1C_pass` (25) — the rung
that lost the board.  Fallback: X is covered by `oc1C_X`, so nothing is deleted.
It must be ranked **72.5**, not 72.4, to sit clear of board 803's
`oc1C_X_4441` and avoid an `is_clear=False` priority tie — the two `requires`
are disjoint (4-4-4-1 is not `balanced`) so the tie is unreachable, but the
separation costs nothing.

**VERIFIED.**  S now doubles (BEN: X 0.97).

**Honest denominator:** `oc1C_pass` runs **-0.32 over 125 tables** and
`oc1D_pass` **-0.74 over 137** — the passing seats over a minor opening are the
two largest populations I touched and they sit at or near the corpus baseline.
Boards 512 and 803 together take a handful of hands out of them.  Small, sound,
low-variance.

**Template:** two rules (`oc1C_X_bal`, `oc1D_X_bal`); `expand: { o: [C, D] }`
if the two contexts are merged.  Do **not** extend it to the majors — over
1H/1S the shortness requirement is what makes the double safe.

---

## Board 548 — margin -3

**Seat/call:** table A, call 8, N bids **3H** on `K82.AT974.Q5.AQ5` after
`1NT - P - 2H - P - 2S - P - P - 3D`.  `ch_new_H3_hi` at fit 1.000.  Partner
transferred to spades and then **passed** — `partner_shown_max` = 7 — and I have
`total_points` = 16.  Twenty-three is not a game and 3H is not a partscore we
own; it is a third bid on a hand that has already been fully described by the
1NT opening.

**Missing agreement:** partner is limited to eight and I hold at most seventeen:
twenty-five is not there, so stop bidding.

**YAML** — context `general_competitive_high`:

```yaml
      - id: ch_pass_limited_A
        call: P
        priority: 27.6
        when: { partner_has_acted: true, their_last_bid_suit: true }
        requires: { evals: { partner_shown_max: [0, 8], total_points: [0, 17] } }
        shows: "partner is limited to eight and I hold at most seventeen: twenty-five is not there, so stop bidding"
        establishes: { forcing: sign_off }
```

**Answering seat:** none — a sign-off pass.

**What it endangers:**
* `ch_new_$X3` / `ch_new_long3_$X` / `_hi` (27.0 / 27.5) — introducing a new suit
  at the three level opposite a partner limited to eight.  **Note the
  denominator carefully:** `ch_new_long3_D` runs **+4.33 over 3 tables** and is
  the most profitable rung in this slice — but its winners are preempt
  advances, where `partner_shown_max` is **10**, so the `[0, 8]` band cannot
  reach them.  That separation is the reason this rung is banded at 8 and its
  looser twin (board 433) is withdrawn.
* `ch_advance_x3/x4_$X` (28.5) and `ch_new_$X4` (28) sit **above** 27.6 and are
  untouched.
* `ch_nt3` (29), `ch_rebid_*` (29), `ch_raise_*` (30-32), `ch_negative_X3` (33),
  `ch_penalty_X` (38) all keep priority.
* Fallback: `P` is covered by `ch_pass`, so nothing is deleted.

**VERIFIED.**  N now passes (BEN: P 0.99).

**Caveat stated:** `ch_new_H3_hi` and `ch_new_H3` both report **"never fires"**
in the corpus primary reading, so this rung's own family is invisible to
`fires_summary` and I cannot give it a denominator.  Judge it on the bridge.

**Template:** none on suit.  The `general_competitive_low` twin
(`cl_pass_limited_A`, priority 27.8 — above `cl_new_$X3_hi`'s 27.5 and below
`cl_nt2`'s 28) is the companion.

---
