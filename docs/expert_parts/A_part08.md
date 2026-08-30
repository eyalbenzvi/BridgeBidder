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

---

## Board 328 — seat N, call 4 (`1D X 1S X`), we passed with a 15-point raise

**Missing agreement.**  Over their double of partner's one-level response,
opener with four-card support and 10+ support points jumps to three — the rung
exists and its total-trumps gate is unreachable.

`xd_jumpraise_$M3` demands `lott_total_trumps >= 9`; a 1S response shows FOUR,
so my four spades plus partner's shown four is **8**, and the gate can never be
cleared on a one-level major response.  `xd_raise_$M2` caps at 9 support points
and `xd_raise_$M3` carries `cheapest_in_suit`, which 3S is not.  A 15-support-point
hand with `AKT5.973.KQ632.6` therefore has no call at all and `xd_pass` (18,
`requires: {}`) takes it.

```yaml
# context: general_their_double — EDIT xd_jumpraise_H3 and xd_jumpraise_S3
      - id: xd_jumpraise_S3
        call: 3S
        priority: 32
        when: { we_bid_last: true, we_hold_contract: false, partner_suit: S, standing_bid_level: [1] }
        requires:
          suits: { S: [4, 13] }
          evals: { total_points: [10, 40], "lott_total_trumps(S)": [8, 26] }   # 9 -> 8
        shows: "jump raise of partner's doubled S: 4+ trumps, 10+ support points"
        establishes: { forcing: non_forcing, agreed_suit: S }
```

**Answering seat.**  Non-forcing; `agreed_suit` is set, so partner's `cl_*` /
`balhigh_*` continuations already read it.

**What it endangers.**  This LOOSENS a gate, so it only adds behaviour.  At 32
it outranks `xd_raise_$M3` (31) and `xd_raise_$M2` (30) — mine needs four
trumps and 10+ points, which the 6-9 raise explicitly denies — and
`xd_run_*` / `xd_second_*` (24-26) and `xd_pass` (18).  `xd_rebid_$X*` (34) is
`my_suit`, mutually exclusive.  It deletes the code fallback for 3S in this
seat, which the rung already covered.

**VERIFIED.**  `3S xd_jumpraise_S3 fit=1.000 score=0.796 prio=32`; N jumps to
3S (BEN bids 2S; double-dummy N/S make exactly nine tricks in spades).  Board
754 unaffected.  Denominators: `xd_jumpraise_S3` +0.83 over 6 firings (feeding
a winner), `xd_pass` -1.72 over 88 (draining a loser).

**Template.**  Both majors (`H`, `S`) — the rungs are already written out.  The
minor twins carry `[9, 26]` too but a 1m response is not a four-card promise,
so leave them.

---

## Board 356 — seat E, call 5 table B (`P 1D 1H 2C P`), we passed with 6 diamonds

**Missing agreement.**  When partner has made a free bid in a new suit in
competition, opener rebids his own six-card suit; the `rule_of_26 < 26` clause
that stops a constructive pair resting in two of a minor must not apply to a
contested auction, where two of my suit is competing rather than resting.

`uc_rebid_D2` carries `not: { evals: { rule_of_26: [26, 99] } }`.  E holds
`AK6.K54.KJT763.5` (14 HCP, six diamonds); partner's free 2C shows 10+, so
`rule_of_26 >= 26` fires the veto, the rung scores **0.100**, and `uc_pass`
(1.000 / 18) takes a seat that has a clear bid.

```yaml
# context: general_uncontested_continuation  (insert before `- id: uc_rebid_D2`)
      - id: uc_rebid_comp_D2
        call: 2D
        priority: 29
        when: { my_suit: D, cheapest_in_suit: true, is_competitive: true }
        requires:
          suits: { D: [6, 13] }
          evals: { total_points: [11, 40], "suit_quality(D)": [1, 9] }
        shows: "rebid of my own six-card D in a contested auction: two of my suit is competing, not resting"
        establishes: { forcing: non_forcing }
```

This is exactly the shape of repair `DECISIONS` records as the one that works
in this context — port an individual rung under `when: { is_competitive: true }`
(`uc_raise_lott4_$M`, +12) rather than re-routing the context.

**Answering seat.**  Non-forcing; partner continues in `general_competitive_low`.

**What it endangers.**  Same priority (29) and same call as `uc_rebid_D2`, so a
tie between them is resolved by fit and both describe the same hand; it
outranks `uc_new_$X2` (26/26.5), `uc_nt2` (28) and `uc_pass` (18).  It stays
below `uc_raise_$M4` (32) and every authored asking bid.  It deletes the code
fallback for 2D in competitive seats where I have a six-card diamond suit —
already covered by `uc_rebid_D2`'s `when`.

**VERIFIED.**  `2D uc_rebid_comp_D2 fit=1.000 score=0.787 prio=29`; E rebids 2D
(BEN's call).

**Template.**  `expand: { X: [C, D, H, S] }`-equivalent, all four suits, at the
two AND three levels (`uc_rebid_$X3` carries the same `rule_of_26` shape).

**Also checked, and NOT proposed:** table A's `cl_raise_H2` on
`9543.Q83.Q4.JT96` (5 HCP).  It fits 1.000 and the raise is textbook Law
bridge; `cl_raise_H2` is one of the best-measured rules in the engine (+2.10 a
table over 10 firings).  Raising its floor would accuse a winner.

---

## Board 361 — NOTHING-WRONG (competitive lens)

**What I checked.**  `P P 1S P 1NT P` — a completely uncontested opener's-rebid
choice (`ob_1M1NT_2S` on `KQJ654.QJ84.Q.Q7` vs BEN's 2H).  E/W bid unopposed at
both tables; there is no competitive seat.  The 5-4 second-suit-versus-six-card-
rebid question belongs to the constructive reviewer.

---

## Board 401 — NOTHING-WRONG (competitive lens)

**What I checked.**  `P 1C P 1H P 1NT P` — responder's rebid with a 5-6
two-suiter (`AKT75.J97632.K2.`), decided by `rr_nt_second_S`.  Uncontested at
both tables (E/W never make a call).  This is the documented
`nt_after_transfer` / responder-rebid family, not mine.

---

## Board 427 — seat N, call 9 (`P P 1D P 1H P 1NT P P`), we balanced 2C

**Missing agreement.**  A five-card suit is enough to balance when only ONE
opponent has bid; when both have bid and limited each other, the reopening bid
needs six.

`ballow_new_$X2` (5+ cards, 10+ points) has no condition on how many opponents
have described their hands.  Here they have bid 1D-1H-1NT — a full,
fit-less, 23-25-point auction — and we bid 2C on `J765.KJ2.4.AJT42` into it.
Double-dummy: N/S take **three** club tricks.

```yaml
# context: general_balancing_low — EDIT the four ballow_new_$X2 rungs
      - id: ballow_new_C2
        call: 2C
        priority: 26
        when: { unbid_suit: C, cheapest_in_suit: true }
        requires:
          suits: { C: [5, 13] }
          evals: { total_points: [10, 40], "suit_quality(C)": [1.5, 9], their_bidders: [1, 1] }   # <- added
        shows: "natural C at the cheapest level: 5+ cards, 10+ points, and only one opponent has described a hand"
        establishes: { forcing: non_forcing }
```

**What it SUBTRACTS.**  Five-card two-level balances after BOTH opponents have
bid.  Those hands pass, or use `ballow_new_long2_$X` (the six-card rung, 8+
points), which is untouched.  That is the standard discipline: over a two-sided
auction you need a sixth card or a double.

**Answering seat.**  n/a.

**What it endangers.**  Nothing outranked (it is a gate); released hands fall to
`ballow_new_long2_$X` (26), `ballow_reopen_X` (41) or `ballow_pass` (21).

**VERIFIED.**  N passes (`ballow_new_C2` drops to 0.800).  **HONEST CAUTION:**
`ballow_new_C2` fires twice in the corpus at **-0.50 a table**, above the -0.73
baseline.  The bridge is right, the measured motivation is one board.  Lowest
priority on my list.

**Template.**  All four suits (`C`, `D`, `H`, `S`) in `general_balancing_low`
only.  Do NOT copy it to `balhigh_new_*`: at the three level the six-card rung
is already the only sane one.

---

## Board 551 — seat N, call 1 (`1S`), we passed a 5-5 with 10 HCP

**Missing agreement.**  A two-level overcall on a 5-5 two-suiter is worth a king
less than a one-suited overcall, because the second suit is a second chance.

`5.KQT87.KQ643.32` is 10 HCP / 12 total points with five good hearts and five
diamonds; `oc1S_2H` and `oc1S_2D` both want 11-17 and both score **0.800**, so
`oc1S_pass` (1.000 / 25) takes the seat and we defended 3S making twelve for
-230, vulnerable.

```yaml
# context: overcalls_of_1S  (insert before `- id: oc1S_3m_jump`)
      - id: oc1S_2H_twosuit
        call: 2H
        priority: 64
        requires:
          suits: { H: [5, 13] }
          hcp: [9, 16]
          evals: { "suit_quality(H)": [1.5, 9] }
          any_of: [ { suits: { D: [5, 13] } }, { suits: { C: [5, 13] } } ]
        shows: "two-level overcall on a 5-5 two-suiter: a king lighter, because the shape replaces the values"
        establishes: { forcing: non_forcing }
```

This is a NATURAL agreement, not Michaels: it names the suit it holds, so
advancer's existing machinery answers it unchanged.

**Answering seat.**  The existing `advance_of_overcall` / `cl_*` ladders — the
call is an ordinary natural two-level overcall and partner needs nothing new.

**What it endangers.**  At 64 it sits BELOW `oc1S_2H`/`oc1S_2D` (65), so a
genuine 11-17 one-suiter is untouched, and below `oc1S_X` (72) and `oc1S_1NT`
(82).  It outranks `oc1S_3$X_jump` (59) and `oc1S_3$X_preempt` (58) — a 5-5
nine-count belongs at the two level, not in a weak jump that hides half the
hand — and `oc1S_pass` (25).

**VERIFIED.**  `2H oc1S_2H_twosuit fit=1.000 score=0.892 prio=64`; N overcalls
2H (double-dummy N/S make eight tricks in hearts; +110 instead of -230).

**CAUTION.**  `oc1S_pass` runs -0.01 a table over 105 firings, i.e. slightly
ABOVE the corpus baseline: taking hands out of it is not free.  The gate is
tight (5-5 AND a good five-card suit AND 9+), which is what keeps it honest.

**Template.**  `expand`-equivalent across all four overcall contexts
(`oc1C_`, `oc1D_`, `oc1H_`, `oc1S_`) and both two-level suits in each — roughly
a dozen rungs from one idea.

---

## Board 555 — SCOPE-EXCLUDED, with a negative prototype result

**What I checked.**  The first divergence is `oc1C_1H` versus `oc1C_2H_jump` on
`9543.AKQ854.T.94` — the simple overcall outranking the weak jump overcall.
Round 11 re-ranked exactly that and measured **-24 held out**; it is on the
do-not-re-propose list.

**My own prototype, and its NEGATIVE result.**  The downstream damage on this
board is the ladder-walk `2D - 2H - 3D - 3H - 4D`, and I suspected the cause:
`uc_rebid_$X4` establishes `agreed_suit` (the file's own comment explains why),
while `uc_rebid_$X3`, `cl_rebid_$X3`, `ballow_rebid_$X3` and `balhigh_rebid_$X3`
establish only `forcing: non_forcing`.  I patched `agreed_suit` onto all sixteen
three-level rebids and re-traced S's call over 3H: **no change** —
`4D uc_rebid_D4 fit=1.000 score=0.787 prio=29` still wins, because an eight-card
suit with 14+ points fits its own rung whatever suit is agreed.  Reporting the
negative rather than shipping it.  The repair the walk actually needs is a
"partner has now named his suit twice" condition, which the `when:` vocabulary
cannot express today.

---

## Board 631 — seat S, call 3 (`2D 2NT P`), we bid 3NT with a 4-4 major fit

**Missing agreement.**  There is no Stayman opposite our 2NT overcall of a weak
two, so the advancer with a four-card major can only guess 3NT.

`advance_2NT_over_weak_two` contains exactly two rungs — `a2nw_3NT_$X` (8+) and
`a2nw_pass_$X`.  S holds `J8.K854.Q3.KT953` opposite a 15-18 2NT with five
hearts; 4H makes ten tricks (+620), 3NT makes nine (+600).

**A closed conversation: the ask, the answer, and both continuations.**

```yaml
# context: advance_2NT_over_weak_two  (insert before `- id: a2nw_3NT_$X`)
      - id: a2nw_stayman_$X
        call: 3C
        priority: 60
        requires:
          hcp: [8, 40]
          any_of: [ { suits: { H: [4, 13] } }, { suits: { S: [4, 13] } } ]
        shows: "Stayman opposite the 15-18 notrump overcall: game values with a four-card major"
        establishes: { forcing: game_forcing }
        alertable: true
        convention: stayman
```

```yaml
# THE ANSWERING SEAT (new context)
  - id: a2nw_stayman_answer
    description: "Answering 3C Stayman opposite our 2NT overcall of their weak two"
    expand: { X: [D, H, S] }
    pattern: "2$X - 2NT - P - 3C - P - ?"
    rules:
      - id: a2nws_3H_$X
        call: 3H
        priority: 60
        requires: { suits: { H: [4, 13] } }
        shows: "four (or more) hearts"
        establishes: { forcing: game_forcing }
      - id: a2nws_3S_$X
        call: 3S
        priority: 59
        requires: { suits: { S: [4, 13] } }
        shows: "four (or more) spades, denying four hearts"
        establishes: { forcing: game_forcing }
      - id: a2nws_3D_$X
        call: 3D
        priority: 40
        requires: {}
        shows: "no four-card major"
        establishes: { forcing: game_forcing }

# THE CONTINUATIONS (new contexts) — the landing, so nothing is passed out
  - id: a2nw_stayman_after_major
    description: "Advancer continues after the Stayman answer"
    expand_pairs:
      - { X: D, M: H }
      - { X: D, M: S }
      - { X: H, M: H }
      - { X: H, M: S }
      - { X: S, M: H }
      - { X: S, M: S }
    pattern: "2$X - 2NT - P - 3C - P - 3$M - P - ?"
    rules:
      - id: a2nwsa_4$M
        call: 4$M
        priority: 60
        requires: { suits: { $M: [4, 13] } }
        shows: "the 4-4 major fit: game"
        establishes: { forcing: sign_off, agreed_suit: $M }
      - id: a2nwsa_3NT
        call: 3NT
        priority: 50
        requires: {}
        shows: "no fit for the answer: 3NT"
        establishes: { forcing: sign_off }

  - id: a2nw_stayman_after_3D
    description: "Advancer continues after the no-major answer"
    expand: { X: [D, H, S] }
    pattern: "2$X - 2NT - P - 3C - P - 3D - P - ?"
    rules:
      - id: a2nwsd_3NT_$X
        call: 3NT
        priority: 50
        requires: {}
        shows: "no major fit: 3NT"
        establishes: { forcing: sign_off }
```

Every answering rung ends in a `requires: {}` catch-all (`a2nws_3D_$X`,
`a2nwsa_3NT`, `a2nwsd_3NT_$X`), so no hole in the ladder can become a pass of a
game force.

**What it endangers.**  `a2nw_stayman_$X` at 60 outranks `a2nw_3NT_$X` (55) and
`a2nw_pass_$X` (20).  It requires a four-card major, so the balanced 8-count
with no major still bids 3NT and the 0-7 hand still passes — the two existing
rungs keep every hand they should have.  The three new contexts define decision
points that were previously unauthored (they fell to
`general_uncontested_continuation`), so they subtract only guesses.

**VERIFIED end to end.**  `3C a2nw_stayman_D 1.000/60` → `3H a2nws_3H_D
1.000/60` → `4H a2nwsa_4H 1.000/60`.  The board reaches 4H.

**Template.**  Already templated: `expand: { X: [D, H, S] }` on ask and answer,
`expand_pairs` on the continuation.  The same three-context shape should be
copied to the 2NT overcall of a THREE-level preempt if that context is ever
authored.

---

## Board 642 — seat N, call 6 (`P 1C X 1H P 2H`), we passed with 21 HCP

**Missing agreement.**  The takeout doubler's SECOND double, after they bid and
raise, is takeout and shows 19+ — the rung exists in both balancing contexts
(`ballow_reopen_X2`, `balhigh_reopen_X2`) and nowhere in the competitive one.

Every X in `general_competitive_low` is gated `side_has_acted: false`
(`cl_takeout_X`) or `i_have_acted: false` (`cl_negative_X1/X2`), so a hand that
has already doubled can never double again: `KQ.AJ6.AKQ3.Q963`, 21 HCP, has
only the code fallback X at priority 9 and passes.

```yaml
# context: general_competitive_low  (insert before `- id: cl_negative_X1`)
      - id: cl_reopen_X2
        call: X
        priority: 36
        when: { their_last_bid_suit: true, side_has_acted: true, we_bid_last: false,
                my_last_call_was_double: true, we_hold_contract: false }
        requires:
          hcp: [19, 40]
          evals: { standing_suit_length: [0, 3], longest_suit_length: [0, 5] }
        shows: "a SECOND double: 19+, still nothing to say but takeout"
        establishes: { forcing: one_round }
```

I used `standing_suit_length` (my length in the suit actually being doubled)
rather than the balancing twins' `max_their_suit_length`: with 21 HCP and four
cards in their FIRST suit but three in the one they have just raised, the
takeout double is still right, and `max_their_suit_length` would veto it.

**THE ANSWERING SEAT.**  It is a force, so it ships with its answer — and the
answer already exists: `cl_doubler_raise_$X` (34), `cl_doubler_raise3_$X` (33)
and `cl_doubler_game_$M` (35) are gated `my_last_call_was_double: true` and read
partner's advance, and the advance itself is `cl_new_$X1` / `cl_adv_$M1`
(board 765) / `cl_jumpadv_$M2` (board 689) in the same context.  Nothing new is
required; I traced that the advancing seat has rules.

**What it endangers.**  At 36 it ties `cl_takeout_X` (`side_has_acted: false`,
mutually exclusive) and outranks `cl_doubler_game_$M` (35),
`cl_doubler_raise_$X` (34) and `cl_negative_X$L` (33, `i_have_acted: false`,
mutually exclusive).  The two live conflicts are the doubler's raises: my rung
needs 19+ AND at most three of the suit being doubled AND no five-card suit,
which is precisely the hand with no fit to raise into.  Below it, everything in
the 25-32 natural band.  It deletes the code fallback X in this narrow seat —
which is the point: the fallback X was the only double available and it fires
at priority 9.

**VERIFIED.**  `X cl_reopen_X2 fit=1.000 score=0.808 prio=36`; N doubles (BEN's
call).

**Template.**  One rung; the `when` is suit-agnostic.  The same rung belongs in
`general_competitive_high` (there is no `chigh_reopen_X2` either) — same body,
`standing_suit_length: [0, 3]`, priority 36.

---

## Board 643 — seat N, call 5 (`P 1D 2C P P`), we passed it out with 14 HCP

**Missing agreement.**  The opener reopens with a double from 13, not from 16 —
partner may pass it, and against a two-level overcall that is often the whole
plus score.

`ballow_reopen_X` has a 16+ floor; `Q762.AJ.AQ942.J9` is 14 HCP / 15 total
points with a doubleton club and scores 0.409.  We defended 2C making seven for
+50; the double collects +100.  This is the documented open item ("no opener's
reopening/second double") in its balancing form.

```yaml
# context: general_balancing_low  (insert before `- id: ballow_X`)
      - id: ballow_reopen_X_opener
        call: X
        priority: 41
        when: { their_last_bid_suit: true, side_has_acted: true, we_bid_last: false,
                my_last_call_was_double: false, we_hold_contract: false, i_have_acted: true }
        requires:
          hcp: [13, 15]
          evals: { max_their_suit_length: [0, 2], longest_suit_length: [0, 5] }
        shows: "opener reopens with a double: opening values, short in their suit - partner may pass it"
        establishes: { forcing: one_round }
```

`i_have_acted: true` is what distinguishes it from `ballow_reopen_X`: I have
already shown a suit, so partner knows my shape and my range, and 13 is enough.

**THE ANSWERING SEAT.**  `establishes: { forcing: one_round }`, so partner must
answer.  The seat is `general_pull_or_sit` (`pattern: "... - X - P - ?"`) plus
the advance-of-a-double rungs in `general_competitive_low`
(`cl_new_$X1`, `cl_adv_$M1`, `cl_jumpadv_$M2`) and the doubler's own follow-ups
(`cl_doubler_raise_$X` / `cl_doubler_game_$M`).  All exist; I traced that the
seat after the double has candidates and does not fall to a fit-1.00 pass.

**What it endangers.**  It shares priority 41 with `ballow_reopen_X` (16+) — the
two bands are disjoint, so the pair is a ladder, not a contest.  Below it:
`ballow_X` (40, `side_has_acted: false`, mutually exclusive), `ballow_nt2_strong`
(30), `ballow_rebid_$X2` (29), `ballow_nt2` (28), `ballow_new_$X2` (26),
`ballow_pass` (21).  The live risk is the 13-15 opener with a doubleton in their
suit who would rather rebid a six-card suit — mine outranks `ballow_rebid_$X2`,
and I accept that: at the two level, with shortness in their suit, the double
that partner can convert is the better matchpoint action.  It deletes the code
fallback X in every seat its `when` reaches, which is exactly this seat.

**VERIFIED.**  `X ballow_reopen_X_opener fit=1.000 score=0.823 prio=41`; N
doubles (BEN's call).  Denominator: `ballow_reopen_X` runs **+3.75 a table over
four firings** — this rung routes hands INTO the engine's best-measured double.

**Template.**  One rung.  Its high twin belongs in `general_balancing_high`
too, but only with `standing_bid_level: [3]` copied from `balhigh_reopen_X`,
whose comment records why the four level must be excluded.

---

## Board 689 — seat N, call 3 (`1C X 1H`), we advanced 1S with 10 points

**Missing agreement.**  The advance of a takeout double is level-showing: 0-8
bids the suit cheaply, 9-11 JUMPS, 12+ cues.  The file has only the cheap bid.

`cl_new_S1` says "4+ cards, 6+ points" and nothing else; `KT653.A73.Q.JT92`
(10 HCP, 12 total points, five spades) bids 1S and the doubler, with no way to
know, passes it out.

```yaml
# context: general_competitive_low  (insert before `- id: cl_raise_C2`)
      - id: cl_jumpadv_H2
        call: 2H
        priority: 31
        when: { partner_last_call_was_double: true, unbid_suit: H, cheapest_in_suit: false, standing_bid_level: [1] }
        requires:
          suits: { H: [5, 13] }
          evals: { total_points: [9, 12] }
        shows: "jump advance of partner's takeout double: 5+ hearts, 9-11, invitational"
        establishes: { forcing: invitational }
      - id: cl_jumpadv_S2
        call: 2S
        priority: 31
        when: { partner_last_call_was_double: true, unbid_suit: S, cheapest_in_suit: false, standing_bid_level: [1] }
        requires:
          suits: { S: [5, 13] }
          evals: { total_points: [9, 12] }
        shows: "jump advance of partner's takeout double: 5+ spades, 9-11, invitational"
        establishes: { forcing: invitational }
```

`cheapest_in_suit: false` plus `standing_bid_level: [1]` is what makes it a
jump: over a one-level bid the cheapest spade call is 1S, so 2S is the jump.

**THE ANSWERING SEAT.**  It is an INVITATION, so the answer ships with it — and
it already exists: `cl_doubler_raise_$X` (34, raise to three) and
`cl_doubler_game_$M` (35, bid the game) are gated `my_last_call_was_double:
true` and are exactly the doubler's accept/decline.  I traced the doubler's seat
and it has candidates; no new context is required.

**What it endangers.**  At 31 it outranks `cl_new_$M1` (30), `cl_adv_$M1` (30.5,
my board-765 rung) and `cl_raise_$X2` (30) — mine needs a FIVE-card suit and
9-12 points, which the simple advance's "4+ cards, 6+" explicitly includes and
therefore under-describes — and everything below (`cl_new_*` 25-27.5,
`cl_nt*` 27-29, `cl_pass` 20).  It stays below `cl_negative_X$L` (33),
`cl_doubler_*` (33-35) and `cl_takeout_X` (36).  It deletes the code fallback
for 2H/2S in this seat; `cl_new_$M2` already covered those calls.

**VERIFIED.**  `2S cl_jumpadv_S2 fit=1.000 score=0.793 prio=31`; N jumps to 2S
(BEN's call; double-dummy N/S make nine tricks in spades).  Denominator:
`cl_new_S1` runs -1.00 a table over 12 firings.

**Template.**  Both majors at the two level as written; the minor and
three-level jumps (`3C`/`3D` over a two-level overcall) are the same idea and
should be added in the same batch, with `standing_bid_level: [2]`.

---

## Board 730 — seat S, call 4 (`1D P 1H X`), we rebid 2D with four spades

**Missing agreement.**  Over their double of partner's one-level response,
opener with four cards in the fourth suit bids it at the one level; that free
bid takes precedence over repeating a six-card minor.

The support-redouble context owns this seat and offers exactly three calls
(XX with three-card support, 2$M with four, pass with a minimum).  With
`Q742..AKJT62.T53` — a heart VOID — S has neither, so `xd_rebid_D2` (34) takes
it and we play 2D.  Double-dummy: N/S make ten tricks in spades.

```yaml
# context: support_redouble  (insert before `- id: srd_raise`)
      - id: srd_new_S1
        call: 1S
        priority: 82
        when: { unbid_suit: S, cheapest_in_suit: true }
        requires:
          suits: { S: [4, 13], $M: [0, 2] }
          evals: { total_points: [11, 40] }
        shows: "the fourth suit at the one level over their double: 4+ spades, fewer than three $M, opening values"
        establishes: { forcing: non_forcing }
```

`suits: { $M: [0, 2] }` keeps it strictly below the convention it must not
displace: with three-card support the redouble is the call.

**Answering seat.**  Non-forcing; responder continues in
`general_after_redouble` / `general_competitive_low`, the same seats that answer
`srd_raise` today.

**What it endangers.**  At 82 it sits below `srd_redouble` (85) — three-card
support outranks a four-card side suit, which is the whole point of the
convention — and above `srd_raise` (80, four-card support: my `$M: [0, 2]`
gate makes them disjoint) and `srd_pass` (30).  Because the rung only exists
where `$M = H` (there is no one-level bid above 1S), it cannot fire in the
M=S instances at all.

**VERIFIED.**  `1S srd_new_S1 fit=1.000 score=0.946 prio=82`; S bids 1S (BEN's
call).

**Template.**  It is already inside the `expand`, so one rung becomes four (or
five, with the board-754 extension).  Its two-level sibling — the fourth suit
at the two level with 5+ cards — is the natural companion and belongs in the
same batch.
