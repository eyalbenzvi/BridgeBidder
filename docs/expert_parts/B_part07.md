# Expert B — constructive / team-IMP bidding — dossier part 07

*(38 boards.  One agreement per board, or NOTHING-WRONG with what was checked.
Written to the mandate of round 17: slam and game machinery lives at the two,
three and four level, in the constructive sequences that separate a minimum
from a slam-going hand BEFORE game is reached.)*

## Summary

*(filled in at the end)*

---

## Authoring note that governs every proposal below (measured, not assumed)

`prepare_decision` (`inference/engine.py:486-493`) walks the live contexts
**most specific first** and skips any rule whose call a more specific context
already covered.  Two consequences I hit immediately and that every proposal
here is written around:

* **You cannot add a rung for a call the generic context already defines by
  putting a new context after it.**  I prototyped exactly that for board 900
  (a 2H rung in a new `1$m - P - 1H - P - 1NT - P - ?` context placed *after*
  `responder_rebid_after_1NT_rebid`, same token count, later file order) and it
  produced **no candidate at all** — the generic context had already covered
  `2H`.  A new context must be placed EARLIER in the file than the one it adds
  to, and then it OWNS that call.
* **Owning a call means carrying the shadowed rungs verbatim.**  Every new
  context below lists, for each call it claims, the rung it displaces.
* **A sign-off with `requires: {}` fits 1.00 and therefore beats every rung
  below `priority` that fits under 0.9.**  It must sit at the BOTTOM of its
  ladder or it silently becomes the ladder.  Prototyped and corrected on
  board 900's answering context.

---

## Board 900 — margin -3

**Seat/call that went wrong:** S, call 6 — `2C` (`ob_1D1H_2C`) on
`K6.QT8.KQ72.K985`, a 13-count 2=3=4=4.  Then N, call 8, `2D`, and we play
2D down two for -200 while BEN's table plays 3H down one.

**The missing agreement.**  With a balanced 12-14 and no fit, opener's 1NT
rebid is the limit bid and outranks the second minor (the file already says so
in a comment on `ob_1NT` and never applied it to the 1D-1H ladder); and
responder's 2S over that 1NT is a **reverse** promising invitational values, so
a 5-4 nine-count passes 1NT instead of going to the two level.

The board pays for both halves together: `1D-1H-1NT-P` is +90 (S makes seven
tricks in notrump double dummy) against our -200.

### YAML

Half A — one number.  `ob_1NT` was deliberately raised to 57.5 to beat
`ob_1D1S_2C` (57); its sibling `ob_1D1H_2C` was left at 58 and is the only
second-suit rung in the family that still outranks the limit bid.

```yaml
# context: opener_rebid_1D_1H_extras
      - id: ob_1D1H_2C
        call: 2C
        priority: 57          # was 58 — sibling sweep of the ob_1NT re-rank
```

Half B — a new context, placed IMMEDIATELY BEFORE
`responder_rebid_after_1NT_rebid` so that it owns `2S` and `2H` in the
1m-1H-1NT shape.  It carries `rr_nt_2H` verbatim (the rung it displaces).

```yaml
  - id: responder_rebid_1NT_H_reverse
    description: "After 1m - 1H - 1NT, 2S is a reverse (invitational); 2H is the six-card sign-off"
    expand: { m: [C, D] }
    pattern: "1$m - P - 1H - P - 1NT - P - ?"
    rules:
      - id: rr1nth_2S_reverse
        call: 2S
        priority: 52.5
        requires: { suits: { S: [4, 13], H: [5, 13] }, hcp: [11, 12] }
        shows: "5-4 majors, invitational: responder's reverse promises extras"
        establishes: { forcing: invitational }
        alertable: true
      - id: rr1nth_2H
        call: 2H
        priority: 51.0
        requires: { suits: { H: [6, 13] }, hcp: [6, 11] }
        shows: "6+ hearts, 6-11, to play"
        establishes: { forcing: sign_off }
```

### THE ANSWERING SEAT

`2S` is an invitation, so the seat that answers it ships with it.  Today that
seat is **empty** — I traced it: no context matches
`1D - P - 1H - P - 1NT - P - 2S - P - ?` and the generic toolkit answers the
invitation with **4H at fit 1.00 (`uc_raise_H4`, priority 32)** on a 12-count
with three hearts.  That is the round-17 failure mode exactly.

```yaml
  - id: opener_answers_1NT_reverse_H
    description: "Opener answers responder's invitational 2S reverse over the 1NT rebid"
    expand: { m: [C, D] }
    pattern: "1$m - P - 1H - P - 1NT - P - 2S - P - ?"
    rules:
      - id: oa1ntr_4H
        call: 4H
        priority: 62
        requires: { suits: { H: [3, 13] }, hcp: [13, 14] }
        shows: "three hearts and a maximum: game in the 5-3 fit"
        establishes: { forcing: sign_off, agreed_suit: H }
      - id: oa1ntr_3H
        call: 3H
        priority: 60
        requires: { suits: { H: [3, 13] }, hcp: [12, 12] }
        shows: "three hearts, minimum: preference back to hearts"
        establishes: { forcing: non_forcing, agreed_suit: H }
      - id: oa1ntr_3S
        call: 3S
        priority: 58
        requires: { suits: { S: [3, 3], H: [0, 2] }, hcp: [13, 14] }
        shows: "three spades, no third heart, maximum"
        establishes: { forcing: invitational, agreed_suit: S }
      - id: oa1ntr_3NT
        call: 3NT
        priority: 56
        requires: { suits: { S: [0, 2], H: [0, 2] }, hcp: [13, 14] }
        shows: "maximum, no third card in either major: 3NT"
        establishes: { forcing: sign_off }
      - id: oa1ntr_pass
        call: P
        priority: 54
        requires: {}
        shows: "minimum with no third heart: pass the invitation in spades"
        establishes: { forcing: sign_off }
```

### WHAT IT ENDANGERS

* `ob_1D1H_2C` (58 → 57).  Below `ob_1NT` (57.5): a semi-balanced 12-14 with
  4-4 minors names its whole hand with 1NT, and 2C names four cards.  It is
  still above `ob_2NT` (56, 18-19), `ob_rebid_2D` (50) and `ob_rebid_3D` (49),
  which it should be; it is still below `ob_1D1H_1S` (60), so a four-card
  spade suit is still shown first.  Outside 12-14 semi-balanced, `ob_1NT` does
  not fit and 2C is unchanged.
* `rr_nt_second_S` (51.5) is **displaced for M=H only** — my context owns 2S
  there.  Subtraction, stated: a 6-10 hand with 5 hearts and 4 spades no
  longer bids 2S; it passes 1NT (`rr_nt_pass`, fit 1.00).  That is the whole
  bridge point and it is the +5 IMPs on this board.  The **M=S twin is
  untouched** — after 1m-1S-1NT, 2H is a lower-ranking second suit, not a
  reverse, and `rr_nt_second_H` still fires (traced).
* `rr_nt_2H` (51) is displaced for M=H and carried verbatim as `rr1nth_2H`,
  so the 6+ heart sign-off is a superset, not a subtraction.
* `rr_nt_2NT` (52) is outranked by `rr1nth_2S_reverse` (52.5) on 11-12 with
  5-4 majors.  Showing the second major before notrump is right when a 4-4
  spade fit is still findable.
* In the new answering context, `oa1ntr_pass` sits at the BOTTOM (54) — the
  first draft had it above `oa1ntr_3S`/`oa1ntr_3NT` and, fitting 1.00, it ate
  every maximum.  Corrected and re-traced.

### VERIFIED

Prototyped against a patched copy of the YAML (`load_system(path)`), not the
repo file.  Traced: opener now bids **1NT** (`ob_1NT` 1.000/57.5 over
`ob_1D1H_2C` 1.000/57.0); responder's nine-count now **passes**
(`rr_nt_pass` 1.00; `rr1nth_2S_reverse` 0.409); the 11-12 5-4 hand bids 2S;
a 6-card heart minimum still bids 2H; the M=S twin still bids 2H.  Answering
ladder traced on five hands: 12ct+3H→3H, 14ct+3H→4H, 14ct 3S/2H→3S,
14ct 2-2→3NT, 12ct 3S/2H→P.

### TEMPLATE

`expand: { m: [C, D] }` on both new contexts (done above).  The reverse
agreement does **not** expand to `M: [H, S]` — that is the point: only the
higher-ranking second suit is a reverse.  The `ob_1D1H_2C` re-rank is a
single number, no templating.

---
