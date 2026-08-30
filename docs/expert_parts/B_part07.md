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

## Board 907 — margin -3 — NOTHING-WRONG (competitive board)

Both divergences are overcall judgement: table A call 3, S passes 1H holding
`J8754.K.A965.A65` where `oc1H_1S` fits **0.757** (a 12-count with a ragged
five-card suit fails the overcall's suit-quality gate by a shade); table B call
4, W raises 1H to 2H over the 1S overcall.  Neither seat is constructive; the
competitive reviewer owns both.

**What I checked in my discipline.**  There is no uncontested constructive seat
on this board — E/W never get a free auction, and our side never opens.  The
only constructive-flavoured rung that fires is `r1H1S_raise`, and a three-card
raise of partner's opened major over a 1S overcall is what it should be.

**Constructive-discipline observation, offered but not proposed:** the
`oc1H_1S` gate is a *suit-quality* gate on a hand whose merit is its 5-4-3-1
shape and its two aces.  Every constructive raise ladder in this file is
already stated in `total_points` (shape-inclusive); the overcall ladder is
stated in HCP plus suit quality alone.  That asymmetry is worth an audit by the
competitive reviewer, not a rung from me.

**VERIFIED** (traced the seat; no proposal).  **TEMPLATE:** n/a.

---

## Board 937 — margin -3 — NOTHING-WRONG (competitive board)

Table A call 3: partner overcalled 1D, RHO bid 1H, and N doubled with
`JT63.74.Q873.KT9` — six HCP, four spades, **four-card diamond support**.
`cl_negative_X1` (33) outranks `cl_raise_D2` (30) and both fit 1.000.

**What I checked.**  The choice between showing the unbid major and raising
partner's suit with four-card support is advancer discipline in a contested
auction — the other reviewer's lane, and the natural repair (a jump raise to
the level of the fit) runs straight into `cl_raise_lott3_$M`, which
`DECISIONS.md` puts on the do-not-re-propose list.  I traced the seat and there
is no constructive rung involved.

**Constructive-discipline observation:** the *general* principle that this
board violates — with four-card support and a minimum, support the suit before
you invent a second one — is exactly the principle that boards 899 and 900 make
into rungs.  Advancer's ladder has no support-first rung at all; that is a
context-level backlog item, not a rung.

**VERIFIED** (traced).  **TEMPLATE:** n/a.

---

## Board 947 — margin -3 — NOTHING-WRONG (competitive board)

Table A call 3: S advances partner's 1H overcall with `AKT874.64.T4.864`
(7 HCP, six spades) over the 1NT sandwich, bidding 2S at
`cl_new_long2_S_hi` fit 1.000.  Table B: E passes throughout the
`1D (1H) P (1S) 2D` auction where BEN competes to 3D.

**What I checked.**  Both seats are competitive advances.  The one seat with a
constructive flavour is table B call 6 — responder's competitive preference
after opener rebids his six-card diamond suit — and that decision is made by
`uc_pass` in `general_uncontested_continuation`, which `ROUND_METHOD.md`
already records as dispatched on RHO's last call rather than on whether the
auction is contested.  Routing it is on the do-not-re-propose list.

**Constructive-discipline observation:** `cl_new_long2_S` says "a SIX-card
suit, 8+ points" and fires on a 7-count.  That is the soft-miss lottery, not a
gate; the same phenomenon I convert into a fit-1.00 decision on board 320.

**VERIFIED** (traced).  **TEMPLATE:** n/a.

---

## Board 2 — margin -2 — NOTHING-WRONG (competitive board)

Table A call 6: N passes 2H holding `KQT.KQ.K9752.K62` after overcalling 1NT;
BEN balances 3D.  Table B call 9: W rebids 3H over N's 3D.  Both are
balancing/competitive judgement.

**What I checked, and a negative result worth recording.**  My first hypothesis
was that the 1NT *overcall* has no responding structure — the same species as
boards 360 and 395.  It is false: I traced `1H - 1NT - P - ?` and the ladder is
authored (`adv1n_2D_H`, `adv1n_2S_H`, `adv1n_2NT_H`, `adv1n_3NT_H`, priorities
54-58), and it correctly passes S's `762.653.AQ8.JT98` and correctly bids 3NT
on a 12-count with both majors.  **The 1NT-overcall advance ladder is present
and healthy; do not spend a round on it.**

**VERIFIED** (traced both seats and two probe hands).  **TEMPLATE:** n/a.

---

## Board 112 — margin -2 — NOTHING-WRONG (competitive board)

Table A call 2: S passes 1C holding `AT43.97653.J.KT4`; BEN overcalls 1H.
`oc1C_1H` fits **0.329** — a five-card heart suit headed by the nine.  This is
the overcall's suit-quality gate again (see board 907) and belongs to the
competitive reviewer.

**What I checked in my discipline.**  Neither side has an uncontested
constructive auction on this board; our only calls are passes and a 1NT
advance.  No constructive rung fires anywhere.

**VERIFIED** (traced).  **TEMPLATE:** n/a.

---

## Board 152 — margin -2

**Seat/call that went wrong:** S, call 2 — `P` (`r1H_pass`) on
`J7543.63.AT63.T5` opposite partner's 1H opening.  Partner then reopened with a
double of 1NT holding 17 and we played 1NT doubled making, -180, against BEN's
-100.  Table B, where BEN held our cards, ran `1H - 1S - 3C - 3S - 4S`.

**The missing agreement.**  With a five-card spade suit, at most two hearts and
five HCP, responder bids 1S rather than passing: the one-level response is
nearly free, and passing 1H on a doubleton buries a spade fit and leaves opener
guessing with 17.

### YAML — one additive rung in `resp_1H`, immediately above `r1H_pass`

```yaml
      - id: r1H_1S_light
        call: 1S
        priority: 71
        requires: { suits: { S: [5, 13], H: [0, 2] }, hcp: [5, 5] }
        shows: "light one-level response: five spades, at most two hearts, five HCP"
        establishes: { forcing: one_round }
        negative_inference_weight: soft
```

`negative_inference_weight: soft` matters: opener must not credit responder
with the six HCP `r1H_1S` promises.

### THE ANSWERING SEAT

`forcing: one_round`, and the seat that answers it is **already authored** —
`opener_rebid_1H_1S` has thirteen rungs (raises at 80/78/76, 1NT at 55, 2NT at
54, the 2H/3H rebids, the second suits and the jump shifts).  I traced N's
`AQ.KJ752.J4.AQ74` through it: opener rebids `2C` (`ob_1H1S_2m`), and S passes.
No new answering context is needed, which is precisely why this is a cheap
rung: the conversation already exists, only the entry to it was missing.

### WHAT IT ENDANGERS

* `r1H_pass` (15, 0-5 HCP).  Subtracted for exactly the 5-HCP hands with five
  spades and a doubleton or shorter heart.  That is the whole agreement.
* `r1H_1S` (72) sits **above** it, so every 6+ hand is still read by the
  existing rule and the new rung never takes a hand the old one describes.
* `r1H_single_raise` (60) and `r1H_1NT` (40) are outranked — but both require
  three-card heart support or deny four spades, and my `requires` denies three
  hearts, so neither can fit the same hand.
* `r1H_2C` / `r1H_2D` (75/76) and the splinters/Jacoby (89/90) all outrank it;
  a game-forcing hand is unaffected.

### VERIFIED

Prototyped against a patched copy.  BEFORE: `P` (`r1H_pass` 1.000/15;
`r1H_1S` 0.800/72 — a one-point soft miss).  AFTER: `1S`
(`r1H_1S_light` 1.000/71).  A four-count with the same shape still passes
(new rung fits 0.409).

### TEMPLATE

Give the twin to `resp_1S` (`r1S_1H_light` is NOT the analogue — over 1S the
light response would be at the **two** level and is not free; the correct twin
is that `resp_1m`'s `r1m_1S` already carries this branch, see below).  In fact
`r1m_1S` already contains exactly this idea —
`hcp: [5,40], suits: {S:[5,13]}, singleton_or_void: [1,1]` — so this proposal
is the **sibling sweep of a light branch the file already has for one seat and
not the other.**  No `expand` needed: two hand-written rungs, one in `resp_1H`
(above) and its heart twin in `resp_1m` (board 735).

---

## Board 168 — margin -2 — NOTHING-WRONG (competitive board)

Table A call 8: N balances to 4C over `1C (1D) 1S (2H) 3C (3D) P (P)` holding
`.AK96.T5.AT97654` — a spade void and seven clubs; `balhigh_rebid_C4` fits
1.000.  4C made ten tricks for +130; BEN passes 3D for +200.  This is a
pass-or-push decision in a fully competitive auction.

**What I checked.**  The only constructive-flavoured call is N's 3C at call 4
(`cl_rebid_jump_C`), which is a correct jump rebid of a self-supporting suit.
The 4C decision turns on defensive tricks against 3D, which no rung in my
discipline addresses and which `ROUND_METHOD.md` warns is a closing call whose
par gap is inherited, not caused.

**VERIFIED** (traced).  **TEMPLATE:** n/a.

---

## Board 195 — margin -2 — NOTHING-WRONG (competitive board)

Table A call 1: N passes W's 3C preempt holding `AK853.Q954.K62.6`.
`v3_C_X` fits 0.409 and `v3_C_S` 0.349 — a 12-count 5-4 with a stiff club is a
classic problem hand over a three-level preempt and the file has no rung for
it.  Defence to preempts is the competitive reviewer's subject.

**Constructive-discipline observation:** `v3_C_S` demands "good 6+ S, 13+" and
`v3_C_X` opening values with shortness; the 5-4 major two-suiter with 12 has
no rule, so the seat is starved rather than mis-ranked.  Same species as
everything else in this dossier, different subject.

**VERIFIED** (traced).  **TEMPLATE:** n/a.

---

## Board 206 — margin -2 — NOTHING-WRONG (competitive board)

Table B call 1: W passes 1C holding `K92.AK98.T93.Q86` (12 HCP, 4-3-3-3 with
three clubs); BEN doubles.  `oc1C_X` fits 0.349 because the takeout double
demands shortness in their suit.  Table B call 7: E raises to 4D where BEN
passes.  Both competitive.

**What I checked.**  No uncontested constructive seat exists on this board for
either side.  A 4-3-3-3 twelve-count with three cards in their minor is the
textbook "pass and hope" hand and the file's decision to pass it is defensible;
BEN's double is the aggressive style choice, not a system hole.

**VERIFIED** (traced).  **TEMPLATE:** n/a.

---

## Board 227 — margin -2 — NOTHING-WRONG (competitive board)

Table A call 3: S doubles in the sandwich seat (`1D P 1S`) holding
`QJT2.K3.K32.AQT2` — 15 HCP, 4-2-3-4, no shortness anywhere; `sw_X` fits
**0.409** and wins anyway because nothing else fits either (`sw_pass` 0.409,
`sw_2C` 0.349).  This is the soft-miss lottery in the sandwich seat, and
`general_pull_or_sit` / the sandwich family belong to the competitive reviewer.

**Constructive-discipline observation:** the hand's correct description is
"15-17 balanced with their suits stopped", i.e. a **1NT-shaped action in the
sandwich seat**, and the only 1NT candidate on the list is the code fallback at
priority 10 fitting 0.028.  `ROUND_METHOD.md` records the same hole for
`general_uncontested_continuation` ("there is no strong balanced notrump rung
after I have already acted", measured -1 held out and reverted).  The sandwich
seat is the second instance and nobody has measured it.  I am not proposing it:
the round-14 twin measured a coin flip, and the reason given there —
`weakest_their_stopper` does not gate — applies here verbatim.

**VERIFIED** (traced).  **TEMPLATE:** n/a.

---

## Board 241 — margin -2 — NOTHING-WRONG (competitive board)

Table A call 3: N passes `2S 3D 3S` holding `.T9.AT83.AJ97532` — a spade void,
seven clubs, four diamonds and nine HCP opposite partner's three-level overcall
of a weak two.  `ch_raise_D4` fits 0.082, everything else is worse, `ch_pass`
fits 1.000.  This is advancer-over-their-competition, the other reviewer's
subject; the seat is starved, not mis-ranked.

**Constructive-discipline observation:** with a void in their suit and a
four-card fit for partner's overcall this is the exact hand type a
**fit-showing jump** describes, and the vocabulary count says fit-showing jumps
are at **zero rules** in this file.  The general agreement is worth authoring
(4C here = clubs plus diamond support), but its natural home is the
competitive-advance family, so I am flagging rather than writing it.

**VERIFIED** (traced).  **TEMPLATE:** n/a.

---

## Board 252 — margin -2 — NOTHING-WRONG (competitive board)

Table A call 2: S overcalls 1H holding `Q.AJ875.K8764.J6` (11 HCP, 5-5 reds);
BEN bids 2NT (unusual).  `DECISIONS.md` scopes Michaels and the unusual notrump
out of the system explicitly and puts them on the do-not-re-propose list, so
the first divergence is closed by policy.  The rest of the auction
(`cl_raise_H2`, `cl_raise_lott3_H`) is competitive raising, and freeing
`cl_raise_lott3_$M` is also on the do-not-re-propose list.

**What I checked.**  Every one of our five calls on this board is in a
contested auction.  Nothing in the constructive tree fires.

**VERIFIED** (traced).  **TEMPLATE:** n/a.

---

## Board 262 — margin -2 — SCOPE-EXCLUDED (opening style)

Table A call 0: S passes in first seat with `KQJ84.3.QJ54.Q84` — 11 HCP, 5-3-1
shape, rule of 20 = 11 + 5 + 4 = 20.  `open_1S` fits 0.800 and
`open_1S_rule20` 0.757; both soft-miss and pass wins at 1.000.
Opening-style and rule-of-20 thresholds are on the brief's do-not-re-propose
list.

**Constructive-discipline observation, recorded not proposed:** `open_1S_rule20`
soft-missing at 0.757 on a hand that satisfies the rule of 20 exactly is a gate
that does not gate; that is a *constraint-model* fact (the same species as
`weakest_their_stopper`), not a bridge disagreement.  Whoever revisits opening
style should check the tolerance before changing a threshold.

**VERIFIED** (traced).  **TEMPLATE:** n/a.

---

## Board 266 — margin -2

**Seat/call that went wrong:** N, call 6 — `2H` (`adx_pull_my_H`, priority 59,
fit 1.000) on `J983.KQ9853.7.QJ` after `1C - P - 1H - 2D - X - P`.  Partner's X
is a **support double**: it announced *exactly three hearts*.  N holds six.  We
crawled to 2H, they bid 3D, and N only reached 4H two rounds later; the whole
board was worth +450 and BEN's table got +500.

**The missing agreement.**  A support double marks a known nine-card fit, so
responder with six trumps, shortness and 8+ HCP bids the game at once instead
of "pulling" partner's double back to his own suit.

### YAML — a new context placed immediately before `support_redouble`

```yaml
  - id: advance_support_double
    description: "Responder acts after partner's support double confirms exactly three trumps"
    expand_pairs:
      - { m: C, M: H }
      - { m: C, M: S }
      - { m: D, M: H }
      - { m: D, M: S }
    pattern: "1$m - P - 1$M - bid<2$M - X - P - ?"
    rules:
      - id: asd_game_$m$M
        call: 4$M
        priority: 63
        requires:
          suits: { $M: [6, 13] }
          hcp: [8, 40]
          features: [ "singleton_or_void(any)" ]
        shows: "the support double marked a nine-card fit: six trumps, shortness and 8+ HCP"
        establishes: { forcing: sign_off, agreed_suit: $M }
```

The pattern is the support double's own pattern (`support_double` uses
`1$m - P - 1$M - bid<2$M - ?`) with `X - P` appended, so it can only ever match
an auction in which our side actually made a support double.

### THE ANSWERING SEAT

`establishes: { forcing: sign_off }` — a game sign-off needs no answering seat,
and opener is already silenced by `partner_signed_off` in
`prepare_decision`.  This is the one shape of proposal that legitimately ships
alone.

### WHAT IT ENDANGERS

The new context defines **only 4$M**, so nothing in `general_pull_or_sit` is
covered away; every other rung there survives untouched.  What 4$M outranks:

* `adx_pull_my_H` / `adx_pull_my_S` (59) — a crawl to two of my own suit is the
  right call when partner's double was *takeout*; opposite a support double it
  understates a nine-card fit by two levels.
* `adx_neg_major_S2` (62) — cannot fit, it needs four cards in the *unbid*
  major and 11+ HCP.
* `adx_sit` (61) — fits 0.000 here (I have no length in their suit) and its
  whole-corpus record is **27 tables, +4 IMPs, mean +0.15**, so it must not be
  disturbed; it is not.
* `adx_pass_min` (52) and `uc_raise_H4` (32) — both below.

`adx_pull_my_H`'s own record is **5 tables, -11 IMPs, mean -2.20**, so the
population I am taking hands out of is a losing one.

### VERIFIED

Prototyped.  BEFORE `2H` (`adx_pull_my_H` 1.000/59); AFTER **4H**
(`asd_game_CH` 1.000/63).  A 6-3-2-2 hand with the same HCP and no shortness
still bids 2H (new rung fits 0.200).

### TEMPLATE

`expand_pairs` over the four (minor, major) support-double shapes, exactly as
`support_double` itself does — done above.  The same idea also wants a
`support_redouble` twin (`1$m - P - 1$M - X - XX - P - ?`); identical rung,
four more rules.

---

## Board 273 — margin -2 — NOTHING-WRONG at the constructive seat, and a NEGATIVE RESULT

Table A call 3: N passes `3C 3D P` holding `8743.AQ987.8.A43`; BEN bids 3H.
**BEN is wrong here and passing is right:** partner's 3D overcall makes ten
tricks double-dummy (`S` in diamonds = 10) for +130, and three hearts by N
takes seven.  Our table A result was the good one.  The board was lost at
**table B, call 2**, where W free-bids `3S` on `AKQT6.KJ43.953.2` over
`3C - (3D)` and goes four down for -200 — a competitive free bid, the other
reviewer's board.

**What I checked, and the negative result.**  I traced the advancer's seat and
it *is* starved — `1NT/3H/3S` all come from `uc_new_*3` at 27-27.5 with fits of
0.134 or less, and there is no context for advancing a three-level overcall.
I drafted the rung (a natural five-card suit at the cheapest level, 9-13) and
**dropped it**: on this board it converts a +130 into a -50.  A starved seat is
not automatically a losing seat, and this is the cheapest possible reminder.

**VERIFIED** (traced; prototype drafted and rejected on its own board).
**TEMPLATE:** n/a.

---

## Board 282 — margin -2 — SCOPE-EXCLUDED (opening style)

Table A call 2: N opens `1H` in third seat with `87.AQJT2.842.K93`
(`open_1H_third_light`, 1.000/75); BEN opens 2H.  A 10-count with a good
five-card suit in third seat is a genuine style fork and the brief excludes
opening-style thresholds.

**What I checked in my discipline.**  The constructive consequence is real and
worth recording: after the light 1H, S responded 1NT and N passed
(`ob_1M1NT_pass`), so we played 1NT on a 4-3 notrump fit for -150 while the
weak-two auction was passed out for -100.  **The light third-seat opening is
only safe if opener's rebid ladder can retreat.**  `opener_rebid_1M_1NT` does
have a pass rung and used it, so the machinery behaved; the loss is the opening
choice, which is out of scope.

**VERIFIED** (traced).  **TEMPLATE:** n/a.

---

## Board 289 — margin -2 — the largest agreement in this slice

**Seat/call that went wrong:** S, call 5 — `3D` (`uc_rebid_D3`, priority 27,
from `general_uncontested_continuation`) after `P 2D P 2S P`.  N had bid a
**forcing** 2S over the weak two and there is **no context in the file that
answers it**; the generic toolkit invented a rebid, N passed it at `uc_pass`,
and we played 3D two down for -100.

This is a **named open item** in `ROUND_METHOD.md` — "the forcing new suit
opposite a weak two is passed out … fourth instance of the starved-forcing-seat
species, found in round 13 while killing a different fix" — and it is the
purest example in the dossier of round 17's finding that the unit of work is a
**closed conversation**, not a rung.  `rw2_new_$W_$X` is `forcing: one_round`
and nothing on the other side of the table has ever been written.

**The missing agreement.**  The whole three-round conversation after a forcing
new suit opposite a weak two: opener raises with three-card support or rebids
his six-card suit; responder then passes, or shows a second five-card suit;
opener passes that unless he has four-card support and a maximum.

### YAML — four contexts, inserted immediately before `resp_weak2_newsuit_D`

```yaml
  - id: opener_after_weak2_new_suit
    description: "Weak-two opener answers responder's forcing new suit"
    expand_pairs:
      - { W: D, X: H, R: 2H, A: 3H, K: DH }
      - { W: D, X: S, R: 2S, A: 3S, K: DS }
      - { W: D, X: C, R: 3C, A: 4C, K: DC }
      - { W: H, X: S, R: 2S, A: 3S, K: HS }
      - { W: H, X: C, R: 3C, A: 4C, K: HC }
      - { W: H, X: D, R: 3D, A: 4D, K: HD }
      - { W: S, X: C, R: 3C, A: 4C, K: SC }
      - { W: S, X: D, R: 3D, A: 4D, K: SD }
      - { W: S, X: H, R: 3H, A: 4H, K: SH }
    pattern: "2$W - P - $R - P - ?"
    rules:
      - id: w2ans_raise_$K
        call: $A
        priority: 64
        requires: { suits: { $X: [3, 13] } }
        shows: "three-card support for the forcing new suit"
        establishes: { forcing: non_forcing, agreed_suit: $X }
      - id: w2ans_rebid_$K
        call: 3$W
        priority: 55
        requires: {}
        shows: "no third card in partner's suit: rebid the six-card suit"
        establishes: { forcing: non_forcing }

  - id: responder_after_weak2_rebid
    description: "Responder's rebid after the weak-two opener rebids his own suit"
    expand_pairs:
      - { W: D, R: 2H, K: DH }
      - { W: D, R: 2S, K: DS }
      - { W: D, R: 3C, K: DC }
      - { W: H, R: 2S, K: HS }
      - { W: H, R: 3C, K: HC }
      - { W: H, R: 3D, K: HD }
      - { W: S, R: 3C, K: SC }
      - { W: S, R: 3D, K: SD }
      - { W: S, R: 3H, K: SH }
    pattern: "2$W - P - $R - P - 3$W - P - ?"
    rules:
      - id: rw2r_pass_$K
        call: P
        priority: 50
        requires: {}
        shows: "opener has a minimum with no fit: pass the six-card suit"
        establishes: { forcing: sign_off }

  - id: responder_weak2_second_suit
    description: "Responder shows a second five-card suit after the weak-two opener's minimum rebid"
    expand_pairs:
      - { W: D, R: 2S, Y: 3H, Z: H, K: DSH }
      - { W: D, R: 2H, Y: 3S, Z: S, K: DHS }
      - { W: H, R: 2S, Y: 3D, Z: D, K: HSD }
      - { W: S, R: 3D, Y: 3H, Z: H, K: SDH }
      - { W: S, R: 3H, Y: 4D, Z: D, K: SHD }
    pattern: "2$W - P - $R - P - 3$W - P - ?"
    rules:
      - id: rw2sec_$K
        call: $Y
        priority: 52
        requires: { suits: { $Z: [5, 13] } }
        shows: "a second five-card suit: partner may prefer"
        establishes: { forcing: non_forcing }

  - id: opener_after_weak2_second_suit
    description: "The weak-two opener answers responder's second suit"
    expand_pairs:
      - { W: D, R: 2S, Y: 3H, Z: H, G: 4H, K: DSH }
      - { W: D, R: 2H, Y: 3S, Z: S, G: 4S, K: DHS }
      - { W: H, R: 2S, Y: 3D, Z: D, G: 5D, K: HSD }
      - { W: S, R: 3D, Y: 3H, Z: H, G: 4H, K: SDH }
      - { W: S, R: 3H, Y: 4D, Z: D, G: 5D, K: SHD }
    pattern: "2$W - P - $R - P - 3$W - P - $Y - P - ?"
    rules:
      - id: w2sec_raise_$K
        call: $G
        priority: 58
        requires: { suits: { $Z: [4, 13] }, hcp: [9, 10] }
        shows: "a maximum weak two with four-card support for the second suit"
        establishes: { forcing: sign_off, agreed_suit: $Z }
      - id: w2sec_pass_$K
        call: P
        priority: 55
        requires: {}
        shows: "the weak two has shown its hand already: pass the second suit"
        establishes: { forcing: sign_off }
```

### THE ANSWERING SEAT

That *is* the proposal: `rw2_new_$W_$X` was the force, and all four contexts
above are the seats that answer it and the seats that answer those.  Every
branch of the conversation ends in a rung with `requires: {}`, so no seat in it
can ever be starved (the round-6 `rkc5H_signoff` lesson), and every such
catch-all sits at the BOTTOM of its ladder, so it cannot eat the descriptive
rungs above it (the correction I had to make on board 900).

### WHAT IT ENDANGERS

* Nothing inside `resp_weak2`, `resp_weak2_major_game` or the three
  `resp_weak2_newsuit_*` contexts: those are all at the `2$W - P - ?` decision,
  one call earlier.
* `uc_rebid_D3` (27), `uc_nt2` (28), `uc_nt3` (29), `uc_raise_S3/S4` (31/32),
  `uc_pass` (18) — the entire generic toolkit at these three seats.  Every one
  of them is outranked, and every one of them is describing a hand it has no
  information about: `uc_rebid_D3`'s `shows` is "values for the level opposite
  partner's shown range", and opposite a weak two there is no such range.
* **The two `requires: {}` sign-offs cover `P` and `3$W` in these auctions,
  which deletes the code fallback for those calls there.**  Both are covered by
  a rung that fits 1.00 on every hand, so nothing is lost.
* Regression checked: the plain raise auction `2D - P - 3D - P - ?` and the 2NT
  feature ask `2D - P - 2NT - P - ?` are byte-identical (still `uc_pass` and
  `feat_D_H`) — the new patterns require the new suit specifically.

### VERIFIED

Prototyped all four contexts against a patched copy.  Auction BEFORE:
`P 2D P 2S P 3D P P` = 3D two down, -100.  AFTER:
**`P 2D P 2S P 3D P 3H P P`** — 3H by N, which makes nine tricks double dummy,
+140.  Traced each seat: `w2ans_rebid_DS` 1.000/55 (opener has two spades, so
the raise fits 0.349); `rw2sec_DSH` 1.000/52 over `rw2r_pass_DS` 1.000/50;
`w2sec_pass_DSH` 1.000/55 (the 4-card gate keeps the ten-count from raising to
4H, which is one down).

### TEMPLATE

`expand_pairs` as written: 9 + 9 + 5 + 5 = **28 contexts and 34 rules from four
authored ideas.**  This is the templating story in miniature.  The natural
extensions, not written here: the same four contexts for the *raise* branch
(`w2ans_raise` instead of `w2ans_rebid`), and the 2NT-feature-ask
continuation, which has its own `feat_*` answers but no third round.

---

## Board 320 — margin -2

**Seat/call that went wrong:** W, table B, call 3 — `3H` (`r1H_limit_raise`) on
`3.A952.J752.Q863`: **seven** HCP with a singleton spade.  Partner drove to 4H
on the strength of a limit raise and made eleven only because the cards lay
well; the auction that beat us was BEN's 2H.

**Trace the engine actually produced:** `r1H_limit_raise` fit **0.800**,
`r1H_single_raise` fit **0.800**, and the decision came back
**`clear=False`** — this seat is a pure soft-miss lottery, decided by half a
point of priority between two rules that both miss.  `ROUND_METHOD.md` calls
the soft-miss lottery "the one hypothesis that has survived rounds 15 and 16
and it has never been attacked directly."

**Re-scored before accusing, as the brief asks:** `r1H_limit_raise` fires on
**4 tables for +11 IMPs, mean +2.75.**  It is a *profitable* rule and I am not
touching it.  The proposal below takes only hands it does not claim: its own
floor is `hcp: [8,11]`, and my rung caps at 7.

**The missing agreement.**  A four-card raise whose extra values are a
singleton rather than high cards — 4-7 HCP, 10-12 support points — is a
single raise, not a limit raise.

### YAML — one additive rung in `resp_1H`, immediately above `r1H_single_raise`

```yaml
      - id: r1H_raise2_shapely
        call: 2H
        priority: 62.5
        requires:
          suits: { H: [4, 13] }
          hcp: [4, 7]
          evals: { total_points: [10, 12] }
          features: [ "singleton_or_void(any)" ]
        shows: "four-card raise with shortness but only 4-7 HCP: a single raise, not a limit raise"
        establishes: { forcing: non_forcing, agreed_suit: H }
```

### THE ANSWERING SEAT

`forcing: non_forcing, agreed_suit: H` — a limit bid, not a force, so it needs
no new answering context; `responder_rebid_after_1M_raise` and
`opener_after_limit_raise` already exist and are untouched (the hand now goes
to the *2H* branch, which is the better-populated of the two).

### WHAT IT ENDANGERS

* `r1H_limit_raise` (62) — only where it fits **below 0.9**, by construction:
  its HCP floor is 8, mine ceilings at 7, so it never loses a hand it describes.
* `r1H_single_raise` (60) — this is the same call; my rung simply makes the
  decision *fit* instead of winning a lottery, so the call is unchanged and the
  explanation improves.
* `r1H_raise_passed` (63), `r1H_game_raise_preempt` (63, needs 5+ hearts) and
  the splinters/Jacoby (89/90) all outrank it and are unaffected.
* Priced downward as well as upward: nothing below 62.5 in this context can
  describe a four-card raise, so there is no more-descriptive call being
  outranked.

### VERIFIED

Prototyped.  BEFORE: `3H`, `clear=False`, both raises at fit 0.800.
AFTER: **`2H`**, `clear=True`, `r1H_raise2_shapely` fit 1.000.  Regression: the
same shape with 9 HCP still finds `r1H_splinter_3S` / `r1H_limit_raise` at fit
1.000, and my rung drops to 0.107.

### TEMPLATE

`resp_1S` gets the identical twin (`r1S_raise2_shapely`, call 2S, same gates).
Neither context carries an `expand`, so this is two hand-written rungs.

**The generalisation the round asked for, stated but not shipped here:** this
hand type — four trumps, shortness, 6-9 support points — is what a
**mini-splinter** describes, and mini-splinters are at **zero rules** in this
file.  The clean version is `1H - 3C / 3D` and `1S - 3C / 3D / 3H` as
mini-splinters (4+ trumps, singleton or void in the bid suit, 6-9 support
points, `alertable`), with an answering context `1$M - P - 3$x - P - ?`
offering opener 3$M to sign off / 4$M with a fit-suited maximum.  It does not
help *this* board — W's shortness is in spades, which cannot be shown below
hearts — which is exactly why I shipped the raise rung instead and am flagging
the mini-splinter for a subject-sized batch rather than a board.

---

## Board 347 — margin -2 — NOTHING-WRONG (competitive board)

Table A call 3: S bids 3D over `1NT (P) 2H` holding `2.AK974.KQJ53.42`
(13 HCP, 5-5 reds, singleton spade) — `cl_new_D3` fit 1.000 at priority 27.
BEN bids 2S (a cue of the transfer suit).  Competing against a 1NT-transfer
auction with a red two-suiter is the competitive reviewer's subject, and the
tool BEN uses does not exist in this system by decision (`DECISIONS.md`: no
Michaels, no unusual notrump).

**What I checked in my discipline.**  Our only other call is N's pass at
`uc_pass` over 3D, which is correct with `KQ4.JT85.84.A863` — a raise to 4D on
two small would be a fabrication.  No constructive rung fires on this board.

**Constructive-discipline observation:** the same 5-5 two-suiter is the hand
type a **fit-showing jump** and a **mini-splinter** exist to describe in
constructive auctions, both at zero rules.  Third sighting in this dossier
(241, 320, 347).

**VERIFIED** (traced).  **TEMPLATE:** n/a.

---

## Board 360 — margin -2

**Seat/call that went wrong:** N, call 4 — `3NT` (`uc_nt3`, priority 29, from
the generic toolkit) on `AQ73.A9.J74.AT76` after `1NT (2C) 2H (P)`.  N/S hold a
**4-4 spade fit** (N `AQ73`, S `KJ84`) worth eleven tricks; 3NT took nine.

**The missing agreement.**  When our 1NT opening is overcalled and responder
bids a natural major, opener answers it: with four cards in the *other* major
and a doubleton in responder's, bid the second major and look for the 4-4 fit
before settling for notrump.

I traced the seat: `1NT - bid - 2$M - P - ?` has **no context at all**, so
every candidate came from `general_uncontested_continuation` (`uc_nt3` 29,
`uc_pass` 18, `uc_new_S2` 26).  Another empty answering seat.

### YAML — a new context (placed before `nt_transfer_accept_H`)

```yaml
  - id: opener_after_1NT_overcalled_suit
    description: "Opener answers responder's natural new major after our 1NT is overcalled"
    expand_pairs:
      - { M: H, oM: S, B: 2S, A: 3H, G: 4H, K: H }
      - { M: S, oM: H, B: 3H, A: 3S, G: 4S, K: S }
    pattern: "1NT - bid - 2$M - P - ?"
    rules:
      - id: o1nto_other_$K
        call: $B
        priority: 62
        requires: { suits: { $oM: [4, 13], $M: [0, 2] } }
        shows: "no fit for partner's major but four of the other one: offering the second fit"
        establishes: { forcing: non_forcing }
      - id: o1nto_game_$K
        call: $G
        priority: 61
        requires: { suits: { $M: [3, 13] }, hcp: [16, 17] }
        shows: "three-card support and a maximum: game in partner's major"
        establishes: { forcing: sign_off, agreed_suit: $M }
      - id: o1nto_raise_$K
        call: $A
        priority: 60
        requires: { suits: { $M: [3, 13] }, hcp: [15, 15] }
        shows: "three-card support, minimum: competing to the three level"
        establishes: { forcing: non_forcing, agreed_suit: $M }
      - id: o1nto_pass_$K
        call: P
        priority: 50
        requires: {}
        shows: "no fit and nothing to add: partner's suit is our spot"
        establishes: { forcing: sign_off }
```

### THE ANSWERING SEAT

`o1nto_other_$K` is an offer, so it needs an answer.  It is `non_forcing`, and
responder's seat (`1NT - bid - 2$M - P - $B - P - ?`) is **already served**: I
traced S's `KJ84.QJ872.K32.5` over 2S and the existing generic raise ladder
answers it correctly with **4S** (`uc_raise_S4` fit 1.000, 11+ support points
opposite a known four-card holding).  So this proposal ships with a verified
answering seat that costs nothing.  `o1nto_pass_$K` carries `requires: {}` at
the bottom of the ladder so the seat can never be starved.

### WHAT IT ENDANGERS

The context is more specific than `general_uncontested_continuation`, so for
these auctions it **covers** `P` and the four bids it names, deleting those
generic candidates and the code fallback for them:

* `uc_nt3` (29, "13-19 balanced, their suits stopped") — it does not know that
  partner has just named a five-card major, and it bid game in the wrong
  strain.  It still owns 3NT: I did not define 3NT, deliberately, so opener
  with 2-2 in the majors still finds it.
* `uc_pass` (18) is replaced by `o1nto_pass_$K` at fit 1.00 — same call, better
  sentence, no behaviour change on hands with no fit.
* `uc_raise_H3` / `uc_raise_H4` (31/32) are replaced by `o1nto_raise` /
  `o1nto_game`, which gate on opener's *known* 15-17 range instead of on
  generic support points.
* `uc_new_S2` (26) is replaced by `o1nto_other`, which requires four cards and
  a doubleton in partner's suit rather than "5+ cards, 10+ points".

### VERIFIED

Prototyped.  BEFORE `3NT` (`uc_nt3` 1.000/29).  AFTER **`2S`**
(`o1nto_other_H` 1.000/62), and responder then raises to **4S**
(`uc_raise_S4` 1.000) — the eleven-trick spade game, +450, matching BEN's
table exactly.

### TEMPLATE

`expand_pairs` over the two majors, as written.  The natural extension is the
same context for a **minor** response (`1NT - bid - 3$m - P - ?`) and for
responder's *double* of the overcall; both are additive and neither is needed
for this board.  Note what I did NOT propose: a 2NT-Stayman-over-interference
scheme, which `DECISIONS.md` puts on the do-not-re-propose list.  This
agreement is natural bidding only.

---

## Board 372 — margin -2

**Seat/call that went wrong:** N, call 4 — `P` (`adx_sit`, priority 61, fit
1.000) on `AK95.A9.K654.943` after `1D (1S) X (P)`.  Partner's X is a
**negative double** (it promised four hearts and takeout values, not a trump
stack), and opener converted it for penalties on a four-card holding.  1S
doubled came home for -100 to them; BEN's 1NT leads to 2D by N making eleven.

**The missing agreement.**  Opener's pass of a *negative* double is a penalty
conversion and needs five real trumps behind the overcaller; with a balanced
minimum and their suit stopped, opener bids 1NT.

### Why this is not a gate on `adx_sit`

`adx_sit` fires on **27 tables for +4 IMPs, mean +0.15** — it is a
break-even-to-positive rule doing a job (advancer sitting a *takeout* double
with a trump stack) that it does well.  Gating it would subtract from all 27.
Instead, `opener_over_negative_double` is the **more specific context**
(`1$m - 1$M - X - P - ?`, five tokens, specificity 1005 against
`general_pull_or_sit`'s 3), so defining `P` there takes the call away from
`adx_sit` in this auction only, and leaves the other 26 firings alone.

### YAML — two rungs added to `opener_over_negative_double`, above `onx_nt_$m$M`

```yaml
      - id: onx_sit_$m$M
        call: P
        priority: 59.5
        requires:
          evals: { standing_suit_length: [5, 13], "suit_quality(their)": [1.5, 9] }
        shows: "converting the negative double: five real trumps behind the overcaller"
        establishes: { forcing: sign_off }
      - id: onx_pass_min_$m$M
        call: P
        priority: 50
        requires: {}
        shows: "nothing else describes the hand: partner's double stands"
        establishes: { forcing: sign_off }
```

Note `standing_suit_length`, not `suit_length(their)` — round 4's fix; the
overcall is the standing bid and `their` resolves to LHO.

### THE ANSWERING SEAT

Both new rungs are `sign_off`, so no answer is owed.  What the pair guarantees
is the opposite property: `onx_pass_min_$m$M` with `requires: {}` at the BOTTOM
of the ladder replaces the generic pass that the new coverage removes, so the
seat cannot be starved — the failure mode I hit on board 900's first draft.

### WHAT IT ENDANGERS

Defining `P` in this context covers the call and therefore removes, **for
`1m - (1M) - X - (P)` only**:

* `adx_sit` (61) — replaced by `onx_sit` at 59.5, which demands **five** cards
  in their suit instead of four.  Four spades to the AK is a fine defensive
  holding and a poor reason to defend 1S when we have a game.
* `adx_pass_min` (52) — replaced by `onx_pass_min` at 50, `requires: {}`, so
  strictly a superset (the old rule capped at 11 total points).
* Because `onx_sit` is at 59.5 it sits **below** `onx_major_$m$M` (60) and
  `onx_major1_$m$M` (61): the 4-4 major fit the double promised is still found
  before any penalty pass, which is why I did not simply raise `onx_nt` above
  `adx_sit` — that variant, which I built and rejected, made a 13-count with
  four spades bid 1NT instead of 1S.
* `onx_nt_$m$M` (58) keeps its priority and its whole-corpus record of **zero
  firings**: it was a dead rung because `adx_sit` was standing in front of it.

### VERIFIED

Prototyped.  BEFORE `P` (`adx_sit` 1.000/61).  AFTER **`1NT`**
(`onx_nt_DS` 1.000/58; `onx_sit_DS` fits below 0.9 on four spades).
Regressions traced: a genuine `AKQ95` five-card stack still passes
(`onx_sit_DS` 1.000/59.5); four hearts still bids 2H (`onx_major_DS` 1.000/60);
six diamonds with no spade stopper still bids 2D; a 12-count with nothing
fitting still lands on a call rather than nothing.

### TEMPLATE

`expand_pairs` already on the context (four (minor, major) combinations) —
8 new rules from two ideas.  The sibling context
`opener_neg_double_over_raise` (`1$m - 2$y - X - bid - ?`) wants the same pair,
and so does the support-redouble family.

---

## Board 392 — margin -2 — NOTHING-WRONG (and I think BEN is wrong)

Table A call 2: S passes 1NT holding `Q983.QT8.K64.843` — a **4-3-3-3
seven-count**.  BEN bids Stayman and reaches 3S, which happens to make.
`nt_stayman` fit 0.800 (its floor is "invitational+", 8).

**Why I am not proposing a rung.**  Stayman on a flat seven-count with no
ruffing value and no second suit is not the expert call; it is a punt that
found a 4-4 fit worth exactly one more trick than 1NT on this layout.  The
agreement the file has — Stayman promises invitational values, the weak hand
with a four-card major passes 1NT — is the mainstream one, and inverting it to
chase a 4-3-3-3 seven-count would fire on every such hand in the corpus.  The
same reasoning is the *reason* I propose the opposite direction on board 848:
a 4-3-3-3 hand is worth less than its HCP, not more.

**What I checked.**  Traced the seat: `nt_stayman` 0.800/85, `nt_transfer_S`
0.349/87 (needs five spades), `nt_2NT_inv` 0.080/60, `nt_pass` 1.000/25.  The
ladder is complete and correctly ranked; the 8-HCP floor is doing exactly what
it says.

**VERIFIED** (traced).  **TEMPLATE:** n/a.

---

## Board 395 — margin -2

**Seat/call that went wrong:** S, call 3 — `P` (`cl_pass`, priority 20, fit
1.000) on `T9853.85.AJT5.A4` after `(P) 1NT (2H)`.  Nine HCP and a five-card
spade suit opposite a 15-17 opening, and the whole candidate list was
sub-threshold: `cl_negative_X2` 0.349, `cl_nt2` 0.342, `cl_new_S2` **0.329**.
Pass at fit 1.00 wins by construction.

**The missing agreement.**  When our 1NT opening is overcalled, responder's
suit at the cheapest level is natural with a five-card suit and 7-15 — the
generic competitive ladder's "5+ cards, **10+** points" is the wrong floor
opposite a known 15-17, because responder is bidding to a *known* combined
range, not guessing.

This is the responder half of the same missing subject as board 360.

### YAML — a new context (placed before `nt_transfer_accept_H`)

```yaml
  - id: responder_1NT_overcalled_natural
    description: "Responder's natural suit after our 1NT opening is overcalled"
    expand_pairs:
      - { O: 2C, X: D, C1: 2D, K: CD }
      - { O: 2C, X: H, C1: 2H, K: CH }
      - { O: 2C, X: S, C1: 2S, K: CS }
      - { O: 2D, X: H, C1: 2H, K: DH }
      - { O: 2D, X: S, C1: 2S, K: DS }
      - { O: 2H, X: S, C1: 2S, K: HS }
      - { O: 2H, X: D, C1: 3D, K: HD }
      - { O: 2H, X: C, C1: 3C, K: HC }
      - { O: 2S, X: H, C1: 3H, K: SH }
      - { O: 2S, X: D, C1: 3D, K: SD }
      - { O: 2S, X: C, C1: 3C, K: SC }
    pattern: "1NT - $O - ?"
    rules:
      - id: r1ntx_suit_$K
        call: $C1
        priority: 34
        requires: { suits: { $X: [5, 13] }, hcp: [7, 15] }
        shows: "natural: a five-card suit and 7-15 opposite the 15-17 opening"
        establishes: { forcing: non_forcing }
```

### THE ANSWERING SEAT

`non_forcing`, and the seat that answers it is **board 360's proposal** —
`opener_after_1NT_overcalled_suit`, `1NT - bid - 2$M - P - ?`.  The two boards
are one agreement seen from the two sides of the table and should be
implemented together: without 360, responder's 2S here is passed out by opener
at `uc_pass`; without 395, opener's answer has almost nothing to answer.
**This pair is the closed conversation.**

### WHAT IT ENDANGERS

The context defines only the named suit calls, so `cl_pass`, `cl_nt2`,
`cl_nt3`, `cl_negative_X2` and the doubles are all untouched.  What it covers
away, per auction:

* `cl_new_$X2` (26) and `cl_new_$X2_hi` (26.5) — "5+ cards, 10+ points".  My
  band 7-15 is a **superset in strength** of their 10+ for a five-card suit, so
  no hand they describe loses its call.
* `cl_new_long2_$X` (26) and `_hi` (26.5) — "a SIX-card suit, 8+ points".  A
  six-card suit satisfies `[5,13]` and 8 is inside 7-15, so again a superset.
* `cl_negative_X2` (33) is now outranked by 34 on hands with a five-card suit.
  One sentence of bridge: with five spades opposite a known 15-17, naming the
  suit is a better description than a double that promises the unbid majors
  generically.  Verified that a **four**-card spade hand still doubles.
* `cl_pass` (20) — the target.  A nine-count with a five-card suit opposite
  15-17 is not a pass.

### VERIFIED

Prototyped.  BEFORE `P` (`cl_pass` 1.000/20, best bid 0.349).  AFTER **`2S`**
(`r1ntx_suit_HS` 1.000/34).  Regression: `T983.85.AJT5.A43` (four spades) still
doubles at `cl_negative_X2` 1.000/33.

### TEMPLATE

`expand_pairs` over (overcall, responder's suit) — eleven pairs, eleven rules
from one idea, as written.  The obvious extensions: three-level overcalls
(another six pairs), and a `3$X` invitational rung at 16+ once opener's
answering context exists.

---
