# EXPERT A — competitive / matchpoint duplicate — dossier part 8 of 8

36 boards (the dossier header says 36; the brief said 34), all at -1 or -2 IMPs.
**26 proposals, 10 NOTHING-WRONG.**  Every proposal below was traced through a
patched **copy** of the system in the scratchpad (`choose_bid(system_path=…)`);
the repo was not modified.  VERIFIED means I ran it and the seat changed its
call; the ranking lines quoted are real output.

## The three agreements that matter most in this slice

1. **The support double and the support redouble exist only after a MINOR
   opening.**  `support_double` / `support_redouble` are
   `pattern: "1$m - P - 1$M - …"`, so after `1H - P - 1S - (X)` and
   `1H - P - 1S - (2D)` the opener has no support call at all and the generic
   `xd_*` / `cl_*` ladders take the seat (boards **754**, **966**).  Adding
   `{ m: H, M: S }` to the two expansions fixes both boards and is the single
   cheapest change in my slice.  Denominator caution: `srd_pass` never fires in
   2000 tables, so this family is barely exercised today.

2. **The pass-out seat has no Law-based three-level competitive raise, and the
   `their_fit >= 8` gate that would carry one is unreachable.**  A 1m opening
   shows 3 and its raise shows 4, so `their_fit` maxes at **7** when the
   opponents' fit is a minor — every `*_raise_lott4_$M` rung in the file is
   therefore dark in exactly the auctions (1m-2m-3m) where the Law matters most.
   Boards **936**, **795**, **748**, and the same arithmetic (partner's SHOWN
   minimum) blocks `xd_jumpraise_$M3` on board **328** and `balhigh_raise_D3`
   on board **226**.

3. **Advancing a takeout double is one rung wide.**  `cl_new_$X1` ("4+ cards,
   6+ points", priority 30) is the whole vocabulary: there is no jump advance
   (board **689**), a four-card major loses to a longer minor because of a
   suit-quality floor partner has already promised to cover (board **765**),
   and the responsive double outranks the raise (board **932**) even though
   `cl_raise_S2`/`cl_raise_H2` are among the most profitable rules in the
   engine (+3.12 and +2.10 a table over 18 firings, against a corpus mean of
   -0.73).

## Whole-corpus denominators I pulled before accusing anything

`repro.fires_summary("reports/r18_before.jsonl", …)`, corpus mean **-0.73**:

| rule | tables | mean | reading |
|---|---|---|---|
| `oc1D_X` | 17 | **-3.18** | the takeout-double length gate is worth having |
| `rdx_XX` | 7 | **-4.43** | responder's redouble over a takeout double is a losing rule |
| `cl_negative_X2` | 15 | -2.07 | supports promoting the raise above it |
| `sw_X` | 23 | -1.70 | vs `sw_1S` -0.50: the re-rank moves hands the right way |
| `xd_pass` | 88 | -1.72 | `general_their_double` is a starved context |
| `balhigh_rebid_S3` | 3 | -4.67 | small n, but every firing lost |
| `cl_raise_S2` / `cl_raise_H2` | 8 / 10 | **+3.12 / +2.10** | the competitive raise is a winner: route hands INTO it |
| `ballow_reopen_X` | 4 | **+3.75** | the reopening double is a winner: a lower floor routes hands in |
| `xd_jumpraise_S3` | 6 | +0.83 | loosening its unreachable gate feeds a winner |
| `cl_nt1` | 3 | **+0.67** | **my board-1 gate accuses a rule running above baseline** |
| `c2x_2D` | 3 | **-0.33** | **above baseline; my board-857 rung is weakly motivated** |
| `ballow_new_C2` | 2 | **-0.50** | **above baseline; my board-427 gate is weakly motivated** |
| `v1NT_pass` | 130 | **+0.02** | **above baseline; the board-286 convention takes hands out of a non-losing rule** |
| `balhigh_pass` | 767 | -0.67 | the pass-out seat as a whole is AT baseline |
| `sw_pass` | 247 | -0.49 | the sandwich pass is above baseline — do not open the sandwich floor |

Those four bold cautions are the honest brake on my own list: they are the
proposals I would ship LAST and only inside a measured batch.

---

## Board 936 — seat N, call 8 (`P 1D 1S 2D 2S 3D P P`), we passed 3D out

**Missing agreement.**  In the pass-out seat, when they have found a fit and we
hold ten trumps with partner's overcalled major, we compete to three on shape,
not on points.

`balhigh_raise_S3` wants 10+ support points AND `rule_of_26 >= 22`; the only
shape-based rung is `balhigh_raise_lott4_$M` at the FOUR level.  There is
nothing at the three.

```yaml
# context: general_balancing_high  (insert before `- id: balhigh_raise_S2`)
      - id: balhigh_raise_lott3_H
        call: 3H
        priority: 30.5
        when: { partner_suit: H, cheapest_in_suit: true, is_competitive: true }
        requires:
          suits: { H: [4, 13] }
          evals: { "lott_total_trumps(H)": [9, 26], their_fit: [7, 26], total_points: [5, 40] }
        shows: "the Law at the three level: they have found a fit and so have we, nine-plus trumps our way"
        establishes: { forcing: non_forcing, agreed_suit: H }
      - id: balhigh_raise_lott3_S
        call: 3S
        priority: 30.5
        when: { partner_suit: S, cheapest_in_suit: true, is_competitive: true }
        requires:
          suits: { S: [4, 13] }
          evals: { "lott_total_trumps(S)": [9, 26], their_fit: [7, 26], total_points: [5, 40] }
        shows: "the Law at the three level: they have found a fit and so have we, nine-plus trumps our way"
        establishes: { forcing: non_forcing, agreed_suit: S }
```

**`their_fit: [7, 26]`, not 8, is the load-bearing number.**  With `[8, 26]` the
rung scores **0.800** on this exact hand and the seat still passes: a 1D opening
shows three and a 2D raise shows four, so the file can never see an eight-card
minor fit.  I traced both versions.

**Answering seat.**  None needed — non-forcing, and it establishes `agreed_suit`
so the existing `cl_*` / `balhigh_*` continuations read it.

**What it endangers** (priority 30.5 in `general_balancing_high`):
`balhigh_raise_S2` (30) — a 6-9 raise is a lower call, and mine needs four
trumps and a nine-card total, which the two-level raise does not;
`balhigh_nt3` (29) — a 13-19 balanced hand with four-card support and a stopper
now raises instead of bidding 3NT, which is the same choice `balhigh_raise_S3`
(31) already makes above me; `balhigh_new_$X3` (27) and `balhigh_nt2` (28) —
both are worse descriptions of a nine-card fit; `balhigh_pass` (21).  It cannot
reach `balhigh_rebid_$X3` (29), whose `my_suit` gate is mutually exclusive with
`partner_suit`.  It also deletes the code fallback for 3H/3S in this seat — but
those calls are already covered by `balhigh_raise_$M3`, so nothing is lost.

**VERIFIED.**  `3S balhigh_raise_lott3_S fit=1.000 score=0.791 prio=30.5` beats
`P balhigh_pass fit=1.000 prio=21`.  Board 795 verified on the same rung.
`balhigh_rebid_S3` (board 954) and `balhigh_raise_D3` (board 226) unchanged.

**Template.**  `expand: { M: [H, S] }` if the balancing families are ever
templated; today they are written out longhand, so ship two rungs.  Do NOT
extend to the minors here — three of a minor is not a matchpoint destination.

---

## Board 954 — seat S, call 8 (`1S P P 2H 2S 3H P P`), we bid 3S

**Missing agreement.**  Opposite a partner who has never bid, a three-level
rebid of my own suit against their fit needs extra VALUES, not just a sixth
card — the four-level twin already knows this and the three-level one does not.

`balhigh_rebid_$X4` carries `partner_has_acted: true`; `balhigh_rebid_$X3`
(11+ total points, no ceiling, no partner condition) does not.  Classic
round-7 species: a gate on one rule and not its sibling.

```yaml
# context: general_balancing_high — EDIT the four existing rungs
      - id: balhigh_rebid_C3      # and D3, H3, S3, all four
        call: 3C
        priority: 29
        when: { my_suit: C, cheapest_in_suit: true, partner_has_acted: true }   # <- added
```
```yaml
# and RE-AUTHOR the band the gate removes (insert before `- id: balhigh_new_C1`)
      - id: balhigh_rebid_solo_S3
        call: 3S
        priority: 29
        when: { my_suit: S, cheapest_in_suit: true, partner_has_acted: false }
        requires:
          suits: { S: [6, 13] }
          evals: { total_points: [17, 40], "suit_quality(S)": [1, 9] }
        shows: "rebidding my own six-card suit at the three level opposite a silent partner: extra values, not just extra shape"
        establishes: { forcing: non_forcing }
```

**What it SUBTRACTS** (this is a gate, so I owe you the subtraction): every
three-level rebid of a six-card suit made opposite a partner who has passed
throughout, from 11 to 16 total points.  Those hands now pass.  That is the
correct matchpoint discipline — partner could not act over their overcall, they
have a fit, and we are bidding three over three alone.  The 17+ hands are
re-authored above so the ceiling species is not re-created; a 16+ hand short in
their suit still has `balhigh_reopen_X` (41).

**Answering seat.**  n/a (a sign-off band becomes a pass).

**What it endangers.**  Nothing new: the solo rung sits at the same 29 as the
rule it replaces, below `balhigh_raise_lott3_$M` (30.5, my board-936 rung,
`partner_suit`, mutually exclusive) and `balhigh_reopen_X` (41).

**VERIFIED.**  S now passes (`P balhigh_pass 1.000/21`, `3S
balhigh_rebid_solo_S3 0.409/29`).  Board 936 unaffected.  Denominator:
`balhigh_rebid_S3` fires 3 times for -4.67 a table — small n, all losses.

**Template.**  Write the gate on all four suits; the solo rung is only worth
authoring for the majors (`H`, `S`) — three of a minor opposite a silent
partner is never the answer.

---

## Board 987 — NOTHING-WRONG (competitive lens)

**What I checked.**  The first divergence is N's opening pass with
`A83.83.J76.AQT42` (11 HCP, rule of 20 = 19) — opening-style thresholds are
scope-excluded.  The competitive call is N's 2NT advance of partner's two-level
overcall: `uc_nt2 fit=1.000 prio=28` with a spade stopper (A83) and 11 HCP
opposite a 2H overcall showing 11-17.  That is the standard advance and I will
not manufacture a rung to beat it.

**Observation for the record.**  This decision is taken by
`general_uncontested_continuation` in a fully contested auction — the confirmed
open item (`... - P - ?` means "RHO passed", not "nobody competed").  The safe
repair pattern is a `when: { is_competitive: true }` port of an individual rung,
which is what I do on board 356; here there is no rung worth porting because
2NT is already the right call.

---

## Board 993 — NOTHING-WRONG (competitive lens)

**What I checked.**  The divergence is table B, seat W, `1D P 1S P 1NT P`: a
purely constructive rebid choice (`rr_nt_gf3_S` 3S vs BEN's 2C checkback) — the
other reviewer's board.  The one competitive candidate is table A, seat N in the
sandwich seat over `1D - 1S` holding `JT2.A8743.JT2.A9`: `sw_1H` demands
`suit_quality(H) >= 1.5` and A8743 scores 1.0, so N passes.  **I prototyped
dropping the quality floor at the ONE level and rejected it**: double-dummy has
N/S making six tricks in hearts and the opponents own the hand (par -450, which
table A already achieved), so entering there is a losing action.  A NEGATIVE
result on my own idea, reported rather than shipped.  `sw_pass` runs +0.24 above
the corpus mean over 247 tables, which says the same thing.

---

## Board 995 — NOTHING-WRONG (competitive lens)

**What I checked.**  Uncontested throughout (`P 1D P 1H P 2C P 2D P`); the call
in question is `uc_nt3` bidding 3NT on `K8.A2.AQJT4.T763` instead of 3D.  That
is a 3NT-versus-5m / `uc_nt3` strength question, both on the do-not-re-propose
list.  No competitive seat exists on this board: E/W never bid.

---

## Board 1 — seat N, call 3 (`1C 1D 1S`), we bid 1NT

**Missing agreement.**  A natural notrump advance of partner's overcall denies
four or more cards in the suit on my RIGHT — with five spades over 1S the hand
is a trap pass, not a notrump hand.

```yaml
# context: general_competitive_low — EDIT cl_nt1
      - id: cl_nt1
        call: 1NT
        when: { side_has_acted: true }
        priority: 27
        requires:
          hcp: [8, 11]
          evals: { weakest_their_stopper: [0.9, 9], semi_balanced: [1, 1], standing_suit_length: [0, 3] }   # <- added
          not: { any_of: [ { suits: { H: [6, 13] } }, { suits: { S: [6, 13] } } ] }
        shows: "natural 1NT: 8-11 balanced with a stopper in their suit and no length in RHO's"
        establishes: { forcing: non_forcing }
```

`standing_suit_length` is the right evaluator here (`suit_length(their)`
resolves to LHO's suit — the documented trap) and it carries sharp tolerance
(`_S2_SUIT = 0.95`), so five cards scores ~0.12 against `[0, 3]` and really does
gate.  In `general_competitive_low` the standing bid is always RHO's, so the
gate means exactly one sentence of bridge.

**What it SUBTRACTS.**  1NT advances holding 4+ of RHO's suit.  Those hands
pass (or double later for penalties), which is what the hand is worth.

**Answering seat.**  n/a.

**What it endangers.**  Nothing outranked: this is a gate, and the hands it
releases fall to `cl_pass` (20) or `cl_negative_X1` (33), both of which
describe a five-card trap holding better than a notrump bid does.

**VERIFIED.**  N now passes.  **HONEST CAUTION:** `cl_nt1` fires 3 times in the
corpus for **+0.67 a table**, i.e. above the -0.73 baseline.  The bridge is
unimpeachable; the measured motivation is not.  Ship it inside a batch, not
alone.

**Template.**  Apply the same clause to the siblings `cl_nt2`, `cl_nt3`,
`ballow_nt*` and `balhigh_nt*` only if the batch measures positive — the
`sibling` lint will otherwise flag the asymmetry.

---

## Board 187 — seat N, call 1 (`1D`), we doubled with five diamonds

**Missing agreement.**  A takeout double promises at most four cards in their
suit at EVERY strength — the 17+ branch of `oc1D_X` tests the majors and the
`not two_of_top3` clause but never looks at diamonds at all, so `9.Q96.AKQ76.AJ94`
(1-3-5-4, 16 HCP) doubles 1D with five of them and a singleton in the suit
partner will name.

```yaml
# context: overcalls_of_1D — EDIT oc1D_X, add a top-level gate above the any_of
      - id: oc1D_X
        call: X
        priority: 72
        requires:
          evals: { standing_suit_length: [0, 4] }        # <- added
          any_of:
            - hcp: [11, 16]
              suits: { D: [0, 2], S: [3, 4], H: [3, 4], C: [3, 13] }
              evals: { longest_suit_length: [0, 5] }
            - hcp: [17, 40]
              suits: { S: [0, 5], H: [0, 5] }
              not: { any_of: [ { suits: { S: [5, 13] }, evals: { "two_of_top3(S)": [1, 1] } },
                               { suits: { H: [5, 13] }, evals: { "two_of_top3(H)": [1, 1] } } ] }
        shows: "takeout double: opening values, at most four of their suit, no five-card major (or any 17+)"
```

**What it SUBTRACTS.**  Takeout doubles made with five or more of the suit
doubled.  There is no bridge argument for those; the hand passes and waits.
`[0, 4]` rather than `[0, 3]` deliberately leaves the 17-count with a flat four
of their suit alone — that is a style question, five is not.

**Answering seat.**  n/a (this removes a force; nothing new is asked).

**What it endangers.**  Nothing is outranked; `oc1D_pass` (25) and `oc1D_2C`
(65) pick up the released hands.

**VERIFIED.**  `X` drops to fit 0.279 and N passes.  Denominator: `oc1D_X`
fires **17 times at -3.18 a table** against a -0.73 baseline — the strongest
measured motivation of anything in my slice.

**Template.**  `expand`-equivalent across the four overcall contexts:
`oc1C_X`, `oc1D_X`, `oc1H_X`, `oc1S_X` — same clause, same number.  Also the
sandwich `sw_X` if the batch measures positive.

---

## Board 213 — seat E, call 4 (`P 1H P 2H`), we passed with 5-5

**Missing agreement.**  A 5-5 two-suiter competes over their major raise on
SHAPE; the suit-quality floor on the natural two-level bid is a one-suiter's
credential and a two-suiter does not need it.

`Q9643.K.AJ.J9765` (11 HCP, 13 total points) scores `cl_new_S2 fit=0.757`
purely because `suit_quality(S)` is 1.0 against a `[1.5, 9]` floor, so
`cl_pass` (fit 1.000, prio 20) takes the seat on the fast path.

```yaml
# context: general_competitive_low  (insert before `- id: cl_raise_C2`)
      - id: cl_new_twosuit_S2
        call: 2S
        priority: 26.6
        when: { unbid_suit: S, cheapest_in_suit: true }
        requires:
          suits: { S: [5, 13] }
          evals: { total_points: [10, 40] }
          any_of:
            - suits: { H: [5, 13] }
            - suits: { D: [5, 13] }
            - suits: { C: [5, 13] }
        shows: "natural S with a second five-card suit: shape is the credential, not suit quality"
        establishes: { forcing: non_forcing }
      - id: cl_new_twosuit_H2
        call: 2H
        priority: 26.6
        when: { unbid_suit: H, cheapest_in_suit: true }
        requires:
          suits: { H: [5, 13] }
          evals: { total_points: [10, 40] }
          any_of:
            - suits: { S: [5, 13] }
            - suits: { D: [5, 13] }
            - suits: { C: [5, 13] }
        shows: "natural H with a second five-card suit: shape is the credential, not suit quality"
        establishes: { forcing: non_forcing }
```

**Answering seat.**  n/a — non-forcing natural.

**What it endangers.**  At 26.6 it outranks only `cl_new_$X2` /
`cl_new_long2_$X` (26 / 26.5), which are the SAME call and a strictly weaker
description of the same hand, and `cl_pass` (20).  It stays below
`cl_new_$X3` (27), `cl_nt2` (28), `cl_rebid_$X2` (29), `cl_raise_$X2` (30) and
every double (33-36), so a hand with a fit for partner, a stopper, or a takeout
shape still makes the better call.  It deletes the code fallback for 2S/2H in
this seat, which `cl_new_$X2` already covered.

**VERIFIED.**  `2S cl_new_twosuit_S2 fit=1.000 score=0.780 prio=26.6` and E bids
2S (BEN's call).

**Template.**  `expand: { X: [C, D, H, S] }`-equivalent across the four suits
and across the `cl_` / `ballow_` / `balhigh_` families — the two-suiter is the
same hand in all three seats.

---

## Board 226 — seat N, call 6 (`1D P 1S 3C P P`), we passed their preempt out

**Missing agreement.**  In the pass-out seat, responder returns to opener's
minor with four-card support; the total-trumps gate on `balhigh_raise_D3`
counts partner's SHOWN minimum of three for a 1D opening, so 4+3 = 7 can never
clear its `lott_total_trumps >= 8`.

```yaml
# context: general_balancing_high  (insert before `- id: balhigh_new_C1`)
      - id: balhigh_pref_C3
        call: 3C
        priority: 28.5
        when: { partner_suit: C, cheapest_in_suit: true, is_competitive: true, i_have_acted: true }
        requires:
          suits: { C: [4, 13] }
          evals: { total_points: [10, 40] }
        shows: "returning to partner's suit with four-card support when they have taken the auction up"
        establishes: { forcing: non_forcing, agreed_suit: C }
      - id: balhigh_pref_D3
        call: 3D
        priority: 28.5
        when: { partner_suit: D, cheapest_in_suit: true, is_competitive: true, i_have_acted: true }
        requires:
          suits: { D: [4, 13] }
          evals: { total_points: [10, 40] }
        shows: "returning to partner's suit with four-card support when they have taken the auction up"
        establishes: { forcing: non_forcing, agreed_suit: D }
```

`i_have_acted: true` is what makes it a PREFERENCE rather than a raise: I have
already bid a suit of my own, so returning to partner's is a choice of trumps,
not a show of values.

**Answering seat.**  n/a — non-forcing, and `agreed_suit` is established so the
existing continuations read it.

**What it endangers.**  **28.5 is deliberately BELOW `balhigh_nt3` (29)** — I
placed it at 30.5 first and rejected that: a 13-19 balanced hand with a stopper
belongs in 3NT, and 30.5 stole those.  It therefore outranks only
`balhigh_new_$X3` (27), `balhigh_nt2` (28) and `balhigh_pass` (21); a
six-card-suit rebid (`balhigh_rebid_$X3`, 29), 3NT (29), a full-values raise
(`balhigh_raise_$m3`, 31) and the reopening double (41) all still win.

**VERIFIED.**  `3D balhigh_pref_D3 fit=1.000 score=0.785 prio=28.5`; N bids 3D
(BEN's call; double-dummy N/S make ten tricks in diamonds).

**Template.**  Minors only (`C`, `D`).  For a major partner suit the LOTT rung
from board 936 already covers the same hand better.

---

## Board 263 — seat W, call 4 (`P P 1C 2C`), we passed with five-card support

**Missing agreement.**  With five-card support for partner's opened minor and a
hand with no defence, raise to the level of our fit at once — the Law raise
exists for the majors and not for the minors.

`cl_raise_lott3_$M` is templated `M: [H, S]`; with `963.94.A95.JT643` (5 HCP,
five clubs) `cl_raise_C3` needs 8+ points and `rule_of_26 >= 22` and scores
0.012.

```yaml
# context: general_competitive_low  (insert before `- id: cl_raise_C2`)
      - id: cl_raise_lott3_C
        call: 3C
        priority: 32
        when: { partner_suit: C, cheapest_in_suit: true, is_competitive: true }
        requires:
          suits: { C: [5, 13] }
          evals: { "lott_total_trumps(C)": [8, 26], total_points: [3, 9] }
        shows: "preemptive raise to the level of our fit: five-card support, no defence, eight-plus trumps"
        establishes: { forcing: non_forcing, agreed_suit: C }
      - id: cl_raise_lott3_D
        call: 3D
        priority: 32
        when: { partner_suit: D, cheapest_in_suit: true, is_competitive: true }
        requires:
          suits: { D: [5, 13] }
          evals: { "lott_total_trumps(D)": [8, 26], total_points: [3, 9] }
        shows: "preemptive raise to the level of our fit: five-card support, no defence, eight-plus trumps"
        establishes: { forcing: non_forcing, agreed_suit: D }
```

Note the difference from the blocked major twin: this rung is reachable because
over a two-level overcall **3C IS the cheapest club bid**, so `cheapest_in_suit`
is satisfied.  The documented defect ("a preemptive raise to the level of the
fit is a jump") only bites when a cheaper raise exists.

**Answering seat.**  n/a — preemptive and non-forcing, `agreed_suit` set so
partner's `cl_*` continuations read it.

**What it endangers.**  At 32 it outranks `cl_raise_$m3` (31, 8+ points — mine
requires 3-9, so the two bands are complementary rather than competing),
`cl_raise_$m2` (30), `cl_new_*` (25-27.5) and `cl_pass` (20).  It stays below
`cl_negative_X2` (33) and `cl_takeout_X` (36).  Because it caps at 9 total
points it cannot steal a constructive hand's call.

**VERIFIED.**  `3C cl_raise_lott3_C fit=1.000 score=0.796 prio=32`; W raises.

**DECLARED RISK.**  `cl_raise_lott3_$M` (the major twin) was freed in round 11
and measured **+19 in sample, -3 held out, twice**, and "freeing" it is on the
do-not-re-propose list.  This is a NEW rung for the minors, not that unblocking,
but it is the same content and I flag it: ship only inside a batch that can be
attributed, and expect it to be the first candidate for reversion.

**Template.**  `expand: { m: [C, D] }` if the family is ever templated.

---

## Board 279 — NOTHING-WRONG (competitive lens)

**What I checked.**  `1C P 1H P` — nobody has competed and nobody will.  The
call is opener's rebid choice (`ob_rebid_2C` on `4.J97.AQT5.AKJ93` vs BEN's
1NT), a constructive-family question.  No competitive seat exists on the board:
N/S pass throughout at both tables.

---

## Board 285 — NOTHING-WRONG (competitive lens)

**What I checked.**  `1D P` — W's choice between `r1m_1S` and a strong jump
shift on `AQJT94.KQ.KQ.765` (17 HCP, six spades).  Uncontested responding
structure, and the second divergence (`rmr_4S` vs 3S) is the documented
`responder_after_minor_rebid` ceiling.  Both are the constructive reviewer's.
N/S never bid at either table.

---

## Board 286 — seat N, call 2 (`P 1NT`), we passed with 5-4 in the majors

**Missing agreement.**  We have no two-suited defence to their 1NT, so a 12-count
with five spades and four hearts (`98742.AJ72.AK6.3`) has no call: `v1NT_2S`
demands `good_suit(S)` and effectively six, and 98742 is not a suit.  Double-dummy
has N/S making **4S** (par +620); we defended 3C for +100.

**This is my highest-risk proposal and I flag it as such.**  It is a convention
addition, the same species as the excluded Michaels/unusual-notrump item, and
`v1NT_pass` runs **+0.02 a table over 130 firings** — above the -0.73 baseline.
It ships with its answering context or not at all.

```yaml
# context: defense_vs_1NT  (insert before `- id: v1NT_2C`)
      - id: v1NT_2C_majors
        call: 2C
        priority: 63
        requires:
          hcp: [10, 15]
          any_of:
            - suits: { S: [5, 13], H: [4, 13] }
            - suits: { H: [5, 13], S: [4, 13] }
        shows: "both majors, at least 5-4, 10-15"
        establishes: { forcing: one_round }
        alertable: true
        convention: nt_defense_majors
```

**THE ANSWERING SEAT** — a new context, which is the whole point:

```yaml
  - id: advance_1NT_2C_majors
    description: "Advancing the 2C overcall of their 1NT (both majors)"
    pattern: "1NT - 2C - P - ?"
    rules:
      - id: a1nt2c_4S
        call: 4S
        priority: 62
        requires: { suits: { S: [4, 13] }, evals: { total_points: [13, 40] } }
        shows: "four-card spade support and the values for game"
        establishes: { forcing: sign_off, agreed_suit: S }
      - id: a1nt2c_4H
        call: 4H
        priority: 61
        requires: { suits: { H: [4, 13] }, evals: { total_points: [13, 40] } }
        shows: "four-card heart support and the values for game"
        establishes: { forcing: sign_off, agreed_suit: H }
      - id: a1nt2c_3S
        call: 3S
        priority: 55
        requires: { suits: { S: [4, 13] }, evals: { total_points: [9, 12] } }
        shows: "four-card spade support, invitational"
        establishes: { forcing: invitational, agreed_suit: S }
      - id: a1nt2c_3H
        call: 3H
        priority: 54
        requires: { suits: { H: [4, 13] }, evals: { total_points: [9, 12] } }
        shows: "four-card heart support, invitational"
        establishes: { forcing: invitational, agreed_suit: H }
      - id: a1nt2c_2S
        call: 2S
        priority: 45
        requires: { suits: { S: [4, 13] } }
        shows: "four-card spade support: partner is at least 5-4 in the majors"
        establishes: { forcing: non_forcing, agreed_suit: S }
      - id: a1nt2c_2H
        call: 2H
        priority: 40
        requires: {}
        shows: "picking hearts: partner has at least four"
        establishes: { forcing: non_forcing, agreed_suit: H }
```

`a1nt2c_2H` has `requires: {}` on purpose: it is the catch-all that makes the
ladder hole-free, so no advancer hand can fall through to a pass of an
artificial 2C.  That is the specific failure mode the brief names (-9.8 IMPs a
seat for an unanswered force).

**What it endangers.**  `v1NT_2C_majors` at 63 outranks the natural
`v1NT_2C` (60, 6+ clubs) — the two `requires` are disjoint, so this is a
labelling change, not a contest; it stays below `v1NT_X` (70).  The new context
has specificity 1000+4 and takes over `1NT - 2C - P - ?` from
`general_uncontested_continuation`; because the ladder ends in a `requires: {}`
rung, it can only ever be a superset in the sense that matters — no hand loses a
call.

**VERIFIED end to end.**  N bids `2C v1NT_2C_majors fit=1.000/63`; S advances
`2S a1nt2c_2S fit=1.000/45` with four spades, and `2H a1nt2c_2H` with three.

**Template.**  `expand`-equivalent for the answering context if you also want
`1NT - 2C - X - ?` and `1NT - 2C - bid - ?`; I did not author those and the
generic contexts cover them.

---

## Board 295 — NOTHING-WRONG (competitive lens)

**What I checked.**  S's sandwich double of `1D - P - 1S` on
`K9.QT93.K2.A8632` satisfies BOTH surviving branches of `sw_X`: opener's suit
is two cards long (branch 1) and the weakest unbid suit is four cards long
(branch 2, the branch the file itself calls the correct test).  Getting
redoubled was variance; BEN's alternative is a **0.47-confidence** pass, the
weakest signal in my slice.

**Observation.**  `sw_X`'s branch 1 is the direct-seat test that its own comment
declares "neither necessary nor sufficient here", and `sw_X` runs -1.70 a table
over 23 firings against a -0.49 for `sw_pass`.  That branch is the rung to
watch, but this board does not indict it — the hand qualifies under branch 2 as
well, so deleting branch 1 would not change the call.  Traced and confirmed.
