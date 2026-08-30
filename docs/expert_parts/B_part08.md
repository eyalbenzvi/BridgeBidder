# Expert B — constructive / team-IMP review of `docs/dossier_575757/part08.md`

**Slice:** 36 boards (the file's header says 36; the brief said 34), all at
-1 or -2 IMPs — the tail of the match.  Every board read through the
constructive lens: uncontested 2/1 machinery, opener's and responder's rebid
structures, the forcing notrump, the invitational/game boundary, and the
shape- and support-showing that has to happen **below game**.

## Summary

| | count |
|---|---|
| boards reviewed | 36 |
| YAML proposals (new rungs / new contexts / one re-rank) | **15** |
| NOTHING-WRONG (constructive call was right, or the board is purely competitive) | 21 |
| new contexts proposed (all of them answering seats) | 6 |
| starved constructive seats found and traced with `repro.rank()` | **7** |

**Everything below is UNTESTED as a rung** — the repo is read-only for me, so I
could not install a rule and re-run `rank()`.  What I *did* run is stated per
board: the live context list, the whole candidate set, and the numeric value of
every evaluator my gate leans on.  Where I write VERIFIED it refers to those
traces (starvation, fit values, evaluator numbers), never to the new rule.

### The three agreements that matter most in this slice

1. **The support double / redouble does not exist after a major opening**
   (boards 966, 754).  `support_double`'s pattern is `1$m - P - 1$M - bid<2$M
   - ?` and `support_redouble`'s is `1$m - P - 1$M - X - ?` — both minor-only.
   After `1H - P - 1S - (2D)` opener with exactly three spades has no way to
   say so and passes; after `1H - P - 1S - (X)` likewise.  Worse: **no seat in
   the file answers a support double at all**, including the four minor
   versions that have been shipped for rounds.  `1D - P - 1S - 2C - X - P - ?`
   lands in `general_pull_or_sit`, which reads our own support double as a
   takeout double to be pulled (`adx_pull_my_S`, fit 1.000).  That is the
   round-17 empty-seat shape exactly: an authored `forcing: one_round` call
   with no answering context.

2. **Three constructive seats in the commonest auction in bridge are
   unauthored** and fall to the `uc_*` generic (boards 995, 401, 993, 361):
   * `1m - 1M - 1NT - 2X - ?` — opener's answer to responder's second suit →
     `uc_nt2` at fit 1.000.
   * `1D - 1M - 2C - 2D - ?` — opener's answer to responder's preference →
     `uc_nt3`, which jumped to 3NT on 14 HCP with `K8` in the unbid suit.
   * `1S - 1NT - 2H - ?` — responder's preference after opener's second suit →
     `uc_raise_H4` at fit 1.000, i.e. a generic four-level raise on 8 HCP.
   Each of these is a five-rung context.  They are cheap and they are the
   territory round 17 said slam machinery actually lives in.

3. **The invitational/game boundary is decided by HCP where it should be
   decided by shape** (boards 993, 401).  `rr_nt_gf3_$M` turns a 12-count with
   a six-card major into a game-forcing *ask* for three-card support, and
   `rr_nt_4$M` needs 13 HCP.  A 6-4 or 6-5 hand with a singleton and 11-12 HCP
   — 14 total points, five losers — is a game and has no rung that says so.
   One templated rule (`rr_nt_shape4_$M`) covers boards 993 and 401 and would
   have gained on both.

### Negative results I am reporting rather than shipping

* **Board 401's authored answer scores worse than the accident.**  If the
  opener's seat after `1C - 1H - 1NT - 2S` is authored correctly, opener passes
  2S with 3-2 in the majors and a minimum; 2S makes ten (+170), while the
  starved seat's `uc_nt2` → 3NT made nine (+400).  The seat still has to be
  authored — but on this board the hole is worth +230 and I say so.
* **Board 285: my first draft was a forcing 3$M rung, and I withdrew it.**
  `rmr_3$M` already means "invitational, 10-12"; a second, forcing meaning on
  the same call gives opener a seat he cannot answer soundly.  What is left is
  a one-line re-rank, which is smaller and safe.
* **Board 279: the mini-splinter I propose does not fire on the board's own
  hand** (opener holds three-card support, not four).  Reported as the family
  agreement, not as a fix for that board.
* **Board 936's obvious repair is on the do-not-re-propose list.**
  `cl_raise_lott3_$M`'s `cheapest_in_suit` block is explicitly excluded, so my
  rung is a *different* rule in a different context (`general_balancing_high`),
  where the raise is not a jump and the gate therefore does not sterilise it.

---

## Board 936 — margin -2

**Seat/call that went wrong.** North, call 8: `P 1D 1S 2D 2S 3D P P` → we pass
with `K5432.QT6.A2.T73`.  BEN bids 3S (0.91).  We have already raised partner's
1S overcall to 2S; we hold a **fifth** trump and they have shown a fit.

**The missing agreement.** In the balancing seat over their three-level
contract, a competitive raise of partner's suit is priced in TRUMPS, not in
combined points: with nine-plus of our trumps against their eight-plus, bid one
more.

**Traced (VERIFIED).**  `context_at` → `general_balancing_high`.  Evaluators on
the actual hand at the actual node: `lott_total_trumps(S) = 10`,
`their_fit = 7`, `total_points = 10`, `rule_of_26 = 20`.  `balhigh_raise_S3`
(prio 31) misses only on `rule_of_26 >= 22` → fit **0.409**;
`balhigh_raise_lott4_S` (prio 32) misses only on `their_fit >= 8` → fit
**0.640**.  So the Law rung exists at the FOUR level and not at the three, and
the three-level rung tests the wrong currency.  Pass wins at fit 1.000 / prio 21.

**EXACT YAML** — new rung inside the existing context `general_balancing_high`,
alongside `balhigh_raise_lott4_$M`:

```yaml
      - id: balhigh_raise_lott3_$M
        call: 3$M
        priority: 31.5
        when: { partner_suit: $M, cheapest_in_suit: true }
        requires:
          suits: { $M: [4, 13] }
          evals:
            "lott_total_trumps($M)": [9, 26]
            total_points: [8, 14]
            their_fit: [7, 26]
        shows: "the Law at the three level: nine-plus of our trumps against their eight, so one more is cheap"
        establishes: { forcing: non_forcing, agreed_suit: $M }
```

`general_balancing_high` is not templated; ship it as
`expand: { M: [C, D, H, S] }` on a small sibling context, or write the four
rungs out beside the existing `balhigh_raise_*3` block.  **TEMPLATE:**
`expand: { M: [C, D, H, S] }` — and the identical rung belongs in
`general_balancing_low` and in `general_competitive_high` (the same seat one
round earlier).  Do **not** touch `cl_raise_lott3_$M`; that is excluded.

**THE ANSWERING SEAT.**  None required: `establishes: { forcing: non_forcing }`,
so partner's pass is the authored `balhigh_pass` / `ch_pass` at fit 1.000.  This
is a competitive raise, not a force.

**WHAT IT ENDANGERS.**
* `balhigh_raise_$M3` (prio 31) — loses the seat for hands with four-plus
  trumps and nine-plus combined trumps but under 22 combined points; when both
  sides have a fit the Law, not the point count, decides the three level.
* `balhigh_pass` (prio 21) — loses the seat whenever the rung fits; passing out
  their three-level contract holding a nine-card fit is the error the board
  records.
* `balhigh_raise_lott4_$M` (prio 32) still outranks at ten trumps **and**
  `their_fit >= 8`, so the four-level Law bid is untouched.
* `balhigh_rebid_$M3` (prio 29) describes MY OWN six-card suit; `when:
  partner_suit: $M` separates them structurally.

**VERIFIED / UNTESTED.**  Starvation, candidate set and all four evaluator
values VERIFIED by trace; the rung itself UNTESTED.

---

## Board 954 — margin -2

**Seat/call.** South, call 8: `1S P P 2H 2S 3H P P` → `balhigh_rebid_S3` bids
3S on `AK8762.QT.Q4.QT6`; BEN passes (0.99).  We go -150 instead of -100.

**Purely competitive** — a balancing-seat rebid decision.  NOTHING-WRONG from
my discipline.

**What I checked.**  The constructive half of this auction is sound: `open_1S`,
`r1S_pass` (partner has 0-5), `o4b_rebid_S` at 2S.  The defect, if there is
one, is that `balhigh_rebid_S3` ("6+ cards, values for the level opposite
partner's shown range") has no channel for *partner has already passed my
opening*, which caps the partnership at ~18 and makes the three level a pure
gamble.  That is a **gate**, and a gate subtracts everywhere it reaches, so I
am not proposing it on one -2 IMP board.  The constructive-discipline
observation worth recording: opener's second-round rebid ladder is banded on
his own hand alone in every balancing context, and `partner_limited` — the
`when:` key that would express it — is the one that raises `NameError`
(round 17, item 5, unfixed).  Fix that bug first and this class becomes
expressible.

---

## Board 987 — margin -2

**Seat/call.** North, call 1: pass in first seat with `A83.83.J76.AQT42`
(11 HCP, five clubs).  BEN opens 1C (0.56 — itself a coin flip).

**Scope-excluded**: opening style / rule-of-20 thresholds are on the
do-not-re-propose list, and `open_1C` already fits 0.800 here, so this is the
soft-miss lottery on the opening bid, not a missing agreement.
NOTHING-WRONG.

**Constructive observation.**  The interesting call is number 5, where North
(having overcalled nothing) bids 2NT through `uc_nt2` after `P 1S 2H P`.  That
is the fourth appearance in this slice alone of a live constructive seat being
decided by the generic notrump ladder.  `uc_nt2` is a standing open item
(-3.11/-2.48 board margin, a third of its firings below the 0.9 fast path);
nothing in this board adds to that indictment, and I am not re-litigating it.

---

## Board 993 — margin -2

**Seat/call that went wrong.** West, call 6: `1D P 1S P 1NT P` → we bid **3S**
(`rr_nt_gf3_S`, "5+ S, game forcing: asking for three-card support") on
`AKQ973.9.87.K432`.  Opener, with a doubleton spade, correctly answers 3NT and
we play 3NT for nine tricks (+400) while BEN plays 4S for eleven (+450).

**The missing agreement.** A six-card major with a singleton and fourteen total
points opposite a 12-14 rebid is a GAME IN THE MAJOR, not a request for
three-card support — shape, not high cards, decides the invitational/game
boundary here.

**Traced (VERIFIED).**  Evaluators on the hand at the node: `hcp = 12`,
**`total_points = 14`**, **`singleton_or_void = 1`**, `dist_points = 2`,
`ltc = 5`.  The context is `responder_rebid_after_1NT_rebid`.  Its ladder is
banded on raw HCP only: `rr_nt_2$M` 6-11 (sign-off), `rr_nt_gf3_$M` 12-18 (the
ask), `rr_nt_4$M` 13-18 (game).  A five-loser hand at 12 HCP therefore asks.

**EXACT YAML** — new rung inside the existing context
`responder_rebid_after_1NT_rebid` (`expand: { m: [C, D], M: [H, S] }` already
present, so this templates into 4 rules for free):

```yaml
      - id: rr_nt_shape4_$M
        call: 4$M
        priority: 53.7
        requires:
          suits: { $M: [6, 13] }
          evals: { total_points: [13, 19], singleton_or_void: [1, 4], ltc: [0, 6] }
        shows: "6+ $M with a singleton and the losers for game: shape, not points, opposite the 12-14 rebid"
        establishes: { forcing: sign_off, agreed_suit: $M }
```

`singleton_or_void` carries sharp tolerance (0.05 in `_EVAL_S2`), so the shape
clause really gates; `ltc` carries 1.4, so a six-loser hand misses cleanly.

**THE ANSWERING SEAT.** None required — `forcing: sign_off, agreed_suit: $M` is
a contract.  Partner's pass is the authored catch-all at fit 1.000.  (Contrast
the rung it replaces, `rr_nt_gf3_$M`, which IS an ask and whose answering
context `opener_after_check3` exists — it is what bid 3NT here, correctly.)

**WHAT IT ENDANGERS.**
* `rr_nt_gf3_$M` (53.5) — loses the seat for 6+ major, singleton, 13+ total
  points; with a singleton opposite a balanced 12-14, three-card support is not
  the question, ten tricks in the major is.
* `rr_nt_4$M` (53) — subsumed for the shapely half of its band; identical call,
  so nothing is lost.
* `rr_nt_3NT` (54) denies a five-card major and so cannot collide.
* `rr_nt_slam3_$M` (56) and `rr_nt_4NT` (55) are both above it and keep 19+ and
  the quantitative invite.
* `rr_nt_2$M` (51, 6-11) is below it and keeps every hand under 13 total points.

**TEMPLATE.**  `expand: { m: [C, D], M: [H, S] }` (inherited).  The identical
rung belongs in the hand-twin context `responder_rebid_after_1H_1S_1NT`
(`rrh_nt_*`), which has the same ladder and the same hole — that is a sibling
gap of the species the `sibling` lint was written for.

**Secondary hole recorded, not proposed here.**  `rr_nt_second_$oM` shows a
second suit only when it is the OTHER MAJOR.  With `1D - 1S - 1NT` and six
spades / four clubs there is no `2C` rung at all: the best candidate in the
whole file is `uc_new_C2` at fit 0.264 / prio 26.  BEN bids 2C at 0.97.  A
`rr_nt_secondm_$X` sibling is owed; it needs the answering context proposed on
board 401.

**VERIFIED / UNTESTED.**  Candidate set and evaluator values VERIFIED; rung
UNTESTED.

---

## Board 995 — margin -2

**Seat/call that went wrong.** North, call 9: `P 1D P 1H P 2C P 2D P` → opener
bids **3NT** on `K8.A2.AQJT4.T763` (14 HCP).  BEN bids 3D (0.70).  We play 3NT
for six tricks, -150.

**The missing agreement.** After `1m - 1M - 2om - 2m` (responder's preference
back to opener's first suit, showing 6-10 and a doubleton) opener has a five-rung
ladder — pass with 11-14, 2NT with 15-16 and the fourth suit stopped, 3NT with
17-19, three of the long minor with six of them and extras — and none of it
exists.

**Traced (VERIFIED).**  `context_at` → `['general_uncontested_continuation',
'general_slam_try']`.  **There is no context for this node at all.**  Candidates:
`uc_nt3` fit 1.000 prio 29 (wins), `uc_pass` fit 1.000 prio 18, `uc_nt2` 0.409,
`uc_rebid_D3` 0.349.  `uc_nt3`'s "their suits stopped" clause is vacuously true
in an uncontested auction, so a 14-count with `K8` in the only unbid suit jumps
to game with no stopper test whatsoever.  Note `weakest_unshown_stopper` on this
hand is **0.0** — the honest test exists and no rule at this node consults it.

**EXACT YAML** — a NEW context.  It is more specific than
`general_uncontested_continuation`, so it takes over every call it defines;
that is why the ladder is complete (pass included) rather than a single rung.

```yaml
  - id: opener_after_preference
    description: "Opener's third call after 1D - 1M - 2C - 2D (responder's preference)"
    expand: { M: [H, S] }
    pattern: "1D - P - 1$M - P - 2C - P - 2D - P - ?"
    rules:
      - id: oap_pass_$M
        call: P
        priority: 50
        requires: { hcp: [11, 14] }
        shows: "minimum: the preference has found the spot"
        establishes: { forcing: sign_off }
      - id: oap_2NT_$M
        call: 2NT
        priority: 53
        requires:
          hcp: [15, 16]
          evals: { weakest_unshown_stopper: [0.9, 9], semi_balanced: [1, 1] }
        shows: "15-16 with the unshown suits stopped: inviting game"
        establishes: { forcing: invitational }
      - id: oap_3NT_$M
        call: 3NT
        priority: 54
        requires:
          hcp: [17, 19]
          evals: { weakest_unshown_stopper: [0.9, 9] }
        shows: "17-19 with the unshown suits stopped: game opposite the 6-10 preference"
        establishes: { forcing: sign_off }
      - id: oap_3D_$M
        call: 3D
        priority: 52
        requires: { suits: { D: [6, 13] }, hcp: [15, 18] }
        shows: "6+ diamonds and extras: inviting game in the long suit"
        establishes: { forcing: invitational, agreed_suit: D }
      - id: oap_3$M
        call: 3$M
        priority: 55
        requires: { suits: { $M: [3, 13] }, hcp: [15, 18] }
        shows: "belated three-card support and extras: inviting game in the major"
        establishes: { forcing: invitational, agreed_suit: $M }
```

On the board: `hcp = 14`, so `oap_pass_H` fits 1.000 and wins — we pass 2D,
which is +90/-50 territory instead of -150.

**THE ANSWERING SEAT — SHIPS WITH IT.**  `oap_2NT_$M`, `oap_3D_$M` and
`oap_3$M` are all invitations, so:

```yaml
  - id: responder_over_preference_invite
    description: "Responder answers opener's 2NT invite after the preference"
    expand: { M: [H, S] }
    pattern: "1D - P - 1$M - P - 2C - P - 2D - P - 2NT - P - ?"
    rules:
      - id: rop_pass_$M
        call: P
        priority: 50
        requires: { hcp: [6, 8] }
        shows: "minimum preference: declining"
        establishes: { forcing: sign_off }
      - id: rop_3NT_$M
        call: 3NT
        priority: 55
        requires: { hcp: [9, 12] }
        shows: "maximum preference: accepting"
        establishes: { forcing: sign_off }
      - id: rop_3$M
        call: 3$M
        priority: 56
        requires: { suits: { $M: [6, 13] }, hcp: [8, 12] }
        shows: "a sixth card in my major: correcting the invite to the suit"
        establishes: { forcing: invitational, agreed_suit: $M }
```

I traced responder's seat over the 3D and 3$M invitations: `uc_pass` fits 1.000
there, so those two are not starved and need no extra context.  The 2NT invite
is: the best candidate at `1D-1M-2C-2D-2NT-P-?` is `uc_pass` 1.000 / prio 18
with `uc_nt_raise3` at 0.605 — an invitation nobody could accept, which is the
round-8 species.  Hence the context above.

**WHAT IT ENDANGERS.**  Only the generic toolkit, which this node currently
owns by default: `uc_nt3` (29) and `uc_nt2` (28) lose the 3NT/2NT calls at this
node — one sentence: after a preference, opener's strength is the only unknown
left, and a ladder banded 11-14 / 15-16 / 17-19 says it, whereas the generic
notrump rungs are banded 13-19 / 11-12 and consult no stopper.  `uc_pass` (18)
loses the pass — replaced by `oap_pass_$M`, the same call with a stated range.
`uc_rebid_D3` (27) loses 3D — replaced by a rung that requires six diamonds
rather than "values for the level".  Nothing above 29 is touched, so
`gst_rkc_D` (46) and the slam-try family are unaffected.

**TEMPLATE.**  `expand: { M: [H, S] }` as written.  The same context is owed for
`1C - 1M - 2D - 2C`? — no: `1C - 1M - 2D` is a reverse and belongs to the reverse
family.  The true siblings are `1D - 1M - 2C - 2D` (this one) and the
major-opening twin `1H - 1S - 2m - 2H`, which has the same hole.

**VERIFIED / UNTESTED.**  Starvation, candidate set and
`weakest_unshown_stopper = 0.0` VERIFIED by trace; the context UNTESTED.

---

## Board 1 — margin -1

**Seat/call.** North, call 3: `1C 1D 1S` → `cl_nt1` bids 1NT on
`QJ954.KQ8.62.JT2` at fit **0.965** (below the fast path — a soft-miss pick).
BEN passes (0.52 — itself undecided).

**Purely competitive** (advancing partner's 1D overcall over their 1S).
NOTHING-WRONG.

**What I checked, and the one constructive point.**  `cl_nt1` shows "8-11
balanced with a stopper in their suit"; the hand is 5-3-2-3 with `QJ954` in
THEIR suit.  So the rule is describing a hand it does not hold, and it won by
0.965 against `cl_pass` at 1.000 only because 0.965 clears nothing — this is the
soft-miss lottery at 0.946-0.965, the standing open item.  The constructive
observation: a 5-card holding in the opponents' suit is precisely the hand that
should not bid notrump and *should* have a natural call, and none of
`cl_new_S1`-style rungs exists over an overcall in my own suit.  Rung-level
repair here is the excluded species (a gate on `cl_nt1`); the right unit of work
is the whole advance ladder, which is a subject, not a rung.

---

## Board 187 — margin -1

**Seat/call.** North, call 1: over 1D we double on `9.Q96.AKQ76.AJ94`
(16 HCP, five diamonds — *their* suit).  BEN bids 1NT (0.66).

**Purely competitive** (choice of overcall).  NOTHING-WRONG from my discipline.

**What I checked.**  `oc1D_X` fits 0.800 and wins on priority 72 over
`oc1D_pass` (0.800, prio 25); `oc1D_1NT` fits 0.000 because the hand is
1-3-5-4, not balanced.  The doubling-with-length-in-their-suit question was
settled with whole-corpus data in round 7 (doubles WITH a 6+ suit average
-2.00/table, WITHOUT -2.54) and is on the do-not-re-propose list.  Nothing
constructive is at stake: the auction dies at 1NT.

---

## Board 213 — margin -1

**Seat/call.** East, call 0: pass in first seat with `Q9643.K.AJ.J9765`
(11 HCP, 5-5 blacks).  `open_1S` fits 0.800, `open_1S_rule20` 0.574.

**Scope-excluded** — opening style / rule-of-20 thresholds.  NOTHING-WRONG.

**Constructive observation.**  Both openings are *below* the fast path here, so
the seat is decided by the blended score against `open_pass` at 1.000; a 5-5
eleven-count in second seat is exactly the population the rule-of-20 rung was
written for and it scores 0.574 because `rule_of_20` is 21 against a gate that
wants more.  A shape channel (5-5 majors/blacks opens light) would be a real
agreement, but opening thresholds are excluded and I will not spend the board
on them.

---

## Board 226 — margin -1

**Seat/call.** North, call 6: `1D P 1S 3C P P` → pass on `AQ64.752.AQ83.93`
(12 HCP, four-card support for partner's diamonds).  BEN bids 3D (0.76).

**Competitive** (balancing over their preempt).  NOTHING-WRONG on the
constructive calls; the same species as board 936.

**What I checked.**  `balhigh_raise_D3` fits **0.082** — it wants
`lott_total_trumps(D) >= 8` and ten support points, and partner's 1D promises
only three diamonds, so the counted fit is seven.  `balhigh_nt3` fits 0.668 with
no club stopper worth the name.  The constructive point: opener rebid nothing
(he passed 3C at `ch_pass` with 14 HCP and four diamonds), so responder is
guessing about a fit that both hands know exists.  The agreement that would fix
it is not in the balancing seat at all — it is **opener's obligation to compete
over a preempt when he holds a fifth trump**, i.e. the same missing Law channel
as board 936, one seat earlier.  My board-936 rung, templated into
`general_competitive_high`, covers this node too.

---

## Board 263 — margin -1

**Seat/call.** South, call 3: over 1C we overcall 1S on `AKQJT.J8763.Q7.7`
(13 HCP, 5-5 majors).  BEN bids 2C (0.97 — a Michaels cue, which we do not
play).

**Purely competitive**, and the divergence is a convention we have deliberately
scoped out (Michaels / unusual notrump are on the do-not-re-propose list).
NOTHING-WRONG.

**What I checked.**  `oc1C_1S` fits 1.000 and is the correct natural call in our
system; `oc1C_1H` fits 0.757.  With 5-5 the higher suit first is right and the
file does it.  There is no constructive seat on this board — the auction is
`P P 1C 1S 3C P P P`.

---

## Board 279 — margin -1

**Seat/call.** West, call 4: `1C P 1H P` → `ob_rebid_2C` rebids 2C on
`4.J97.AQT5.AKJ93` (15 HCP, 1=3=4=5).  BEN bids 1NT (0.88).

**NOTHING-WRONG on the call.**  1NT with a singleton spade is not a rebid I will
endorse against BEN's 0.88; `ob_1NT` correctly fits 0.000 here because the hand
is not semi-balanced, and 2C (5+ clubs, minimum) is the mainstream call.
`ob_1C1H_2D_reverse` fits 0.409 and should: 4-5 in the minors with 15 is not a
reverse.  The 1 IMP is 2C-making-nine (+110) against 1NT-making-nine (+150).

**The family agreement this board names, which does NOT fire on this hand.**
`opener_rebid_1m_1M`'s raise ladder is `2$M` 12-15, `3$M` 16-18, `4$M` 19-24 —
**pure point count, no shape channel at all.**  Mini-splinters are at zero rules
in the file.  Opener with four-card support, a singleton and 15-17 has no way to
separate himself from a 4-3-3-3 twelve-count until game has already been bid.
The board's West holds only three hearts, so the rung below would not have
fired; I am proposing it as the family agreement and saying so.

**EXACT YAML** — new context (only the `1m - 1H` half templates cleanly: after
`1$m - 1S`, `2H` is already the reverse `ob_1m1S_2H_reverse`):

```yaml
  - id: opener_minisplinter_1m_1H
    description: "1m - 1H - 2S: mini-splinter, four hearts and short spades"
    expand: { m: [C, D] }
    pattern: "1$m - P - 1H - P - ?"
    rules:
      - id: ob_mini_2S_$m
        call: 2S
        priority: 79
        requires:
          suits: { H: [4, 13], S: [0, 1] }
          evals: { total_points: [15, 18], singleton_or_void: [1, 4] }
        shows: "mini-splinter: 4+ hearts, a singleton or void in spades, 15-18 support points"
        establishes: { forcing: one_round, agreed_suit: H }
        alertable: true
        convention: mini_splinter
```

**THE ANSWERING SEAT — SHIPS WITH IT.**  A mini-splinter is an invitation with
a shape attached; the whole value is responder's ability to devalue wasted
spade honours:

```yaml
  - id: responder_over_minisplinter
    description: "Responder answers the 1m - 1H - 2S mini-splinter"
    expand: { m: [C, D] }
    pattern: "1$m - P - 1H - P - 2S - P - ?"
    rules:
      - id: rms_3H_$m
        call: 3H
        priority: 55
        requires: { hcp: [6, 8] }
        shows: "minimum response: declining the mini-splinter"
        establishes: { forcing: sign_off, agreed_suit: H }
      - id: rms_4H_$m
        call: 4H
        priority: 58
        requires:
          hcp: [9, 13]
          evals: { wasted_in_partner_shortness: [0, 1] }
        shows: "accepting: nothing wasted opposite the spade shortness"
        establishes: { forcing: sign_off, agreed_suit: H }
      - id: rms_3S_$m
        call: 3S
        priority: 57
        requires: { hcp: [9, 13], evals: { wasted_in_partner_shortness: [2, 12] } }
        shows: "values, but wasted in spades: 3H or 4H is opener's choice"
        establishes: { forcing: invitational, agreed_suit: H }
      - id: rms_cue_4$m
        call: 4$m
        priority: 60
        requires: { hcp: [14, 40], evals: { controls: [4, 12] } }
        shows: "slam interest opposite the shortness: cue-bidding the first-round control"
        establishes: { forcing: game_forcing, agreed_suit: H }
      - id: rms_floor_$m
        call: 3H
        priority: 40
        requires: {}
        shows: "no other description: three hearts is the landing spot"
        establishes: { forcing: sign_off, agreed_suit: H }
```

The `requires: {}` floor is the round-6 `rkc5H_signoff` lesson: no seat starved.

**WHAT IT ENDANGERS.**
* `uc_new_S2` / `uc_new_S2_hi` (prio 26/26.5) lose the 2S call at this node —
  they read a jump by OPENER as "natural spades, 5+ cards", which opener cannot
  hold (with 5 spades and 4 hearts he opens 1S).
* `ob_raise_3$M` (78) is directly below it: a 15-18 hand with four trumps and a
  stiff spade is described far better by naming the shortness than by a number.
* `ob_raise_2$M` (80) still outranks it, so the plain 12-15 minimum raise is
  untouched — the new rung's `total_points >= 15` floor cannot reach it.
* `ob_1C1H_1S` / `ob_1D1H_1S` (60) show FOUR spades; my rung requires 0-1, so
  they are structurally disjoint.
* `ob_raise_4$M` (76) keeps 19+.

**TEMPLATE.**  `expand: { m: [C, D] }` as written.  The natural extensions, in
order of confidence: the same rung in `opener_rebid_1H_1S` (`1H - 1S - 3m` as
the short-suit jump) and the full splinter one level higher (`3S`, 19+), which
would give the file its first shortness channel in the commonest auction of all.

**VERIFIED / UNTESTED.**  Candidate set at the node VERIFIED (the dossier's own
table, re-read); everything else UNTESTED.  **Explicit negative:** it does not
fire on this board's hand.

---

## Board 285 — margin -1

**Seat/call.** West, call 6: `1D P 1S P 2D P` → `rmr_4S` bids 4S on
`AQJT94.KQ.KQ.765` (17 HCP, six spades).  BEN bids 3S (0.89).  4S made ten
(+620); BEN's 3NT made eleven (+660).

**NOTHING-WRONG on the call** — 4S with a chunky six-card major and 17 opposite
a 12-15 minor rebid is the expert bid, and 3NT beat it by a double-dummy trick,
not by a better auction.

**But the board exposes a real inversion, and that is my proposal.**
In `responder_after_minor_rebid` the ladder is:

| rule | call | band | prio |
|---|---|---|---|
| `rmr_4$M` | 4$M | 6+ major, **13-40** | **58** |
| `rmr_3$M` | 3$M | 6+ major, 10-12 | 57 |
| `rmr_4NT` | 4NT | 17-19 semi-balanced, quantitative | **56** |

Traced on this hand: `hcp = 17`, `total_points = 19`, `semi_balanced = 1.0`,
`controls = 4`, `ltc = 6`.  **`rmr_4NT` fits 1.000 and loses on priority to a
sign-off.**  Since a six-card major is the commonest shape that produces a slam
opposite a six-card minor, the context's ONLY slam try is unreachable exactly
where it is most wanted — the round-14 `uc_nt_raise3` error (pricing a rung
against the one above it and not the ones below) with the signs reversed.

**EXACT YAML** — a one-line re-rank plus a ceiling that keeps the sign-off
primary for the hands that should sign off:

```yaml
      - id: rmr_4$M
        call: 4$M
        priority: 55.5          # was 58
        requires: { suits: { $M: [6, 13] }, hcp: [13, 40] }
        shows: "6+ $M, game values"
        establishes: { forcing: sign_off, agreed_suit: $M }
```

Nothing else changes: `rmr_4NT` (56) now outranks it, and `rmr_4NT`'s own gate
(17-19 AND semi-balanced) is what confines the change to the slam-try
population.  13-16, and every 17-19 that is not semi-balanced, still bid 4$M.

**THE ANSWERING SEAT — ALREADY EXISTS, and I checked it.**
`context_at('1D P 1S P 2D P 4NT P')` → **`quant_accept_after_minor_rebid[D,S]`**,
with `rmrq_accept` (6NT, fit 1.000, prio 60) and `rmrq_decline` (P, fit 1.000,
prio 55).  This is the rare case where the ask, the answer and the sign-off are
all authored and only the priority stops the conversation happening.

**WHAT IT ENDANGERS.**  `rmr_4$M` is the rung being moved, so price it against
everything it now sits below and above: `rmr_4NT` (56) takes 17-19
semi-balanced — one sentence: 29-34 combined points opposite a limited rebid is
a slam invitation, not a game.  `rmr_3$M` (57) is above it but banded 10-12, so
disjoint.  `rmr_3NT` (55) is now only half a point below: a 13-18 hand with six
of a major and no slam interest must still prefer the major, and it does,
because 55.5 > 55.  `rmr_gf3_$m` (57) needs a minor fit and 19+, untouched.

**WITHDRAWN (negative result).**  My first draft added a *forcing* 3$M rung at
16-19.  I withdrew it: `rmr_3$M` already means "invitational, 10-12", and a
second meaning on the same call leaves opener a seat he cannot answer soundly —
he would have to guess which band he faces before choosing between pass and 4M.

**VERIFIED / UNTESTED.**  The inversion, the fit of `rmr_4NT` (1.000) and the
existence of the answering context are all VERIFIED by trace.  The re-rank
itself UNTESTED; it is the cheapest change in this whole part and should be
screened on its own.

---

## Board 286 — margin -1

**Seat/call.** North, call 2: over their 1NT we pass with `98742.AJ72.AK6.3`
(12 HCP, 5-4 majors, singleton club).  BEN bids 2D (0.93 — a transfer/two-suited
call in whatever defence BEN plays).

**Purely competitive**, and the divergence is a convention we scoped out on
purpose ("Defense to their 1NT: natural", DONT/Cappelletti explicitly rejected
for explainability).  NOTHING-WRONG.

**What I checked.**  `v1NT_2S` fits 0.200 (it wants 5+, usually 6, spades and
8-15 — the shape is there, the "usually 6" is not), `v1NT_X` 0.134, `v1NT_2H`
0.070.  Nothing in the natural defence describes 5-4 majors, which is precisely
the hand every two-suited defence was invented for.  This is a convention
addition, not a constructive gap, and it is excluded.

---

## Board 295 — margin -1

**Seat/call that went wrong.** West, call 8: `1D P 1S P 2D P 2NT P` → opener
PASSES the invitational 2NT on `JT7.42.AQJ863.K9` (11 HCP, six diamonds,
`42` in hearts).  BEN bids 3D (0.43).  We play 2NT for nine tricks; the
constructive point stands regardless of the trick count.

**The missing agreement.** Declining an invitational 2NT is not the same as
passing it: with a six-card minor and a side suit wide open, three of the minor
is the decline.

**Traced (VERIFIED).**  Context `opener_over_invite_2NT_minor[D,S,2D]`.  It has
exactly three rungs — `oim2n_5m` (6+ minor, 14-21, no stopper), `oim2n_3NT`
(accept, 14-21), `oim2n_pass` (decline, 10-13).  Evaluators on this hand:
`hcp = 11`, **`weakest_unshown_stopper = 0.0`** (hearts `42`),
`suit_quality(D) = 2.5`, `total_points = 13`.  So the context can decline only
by passing, and the one rung that consults the stopper needs 14+.

**EXACT YAML** — a fourth rung in the existing context (its
`expand_pairs` already covers the five (m, M, R) combinations):

```yaml
      - id: oim2n_3m_$M$R
        call: 3$m
        priority: 51
        requires:
          suits: { $m: [6, 13] }
          hcp: [10, 13]
          evals: { weakest_unshown_stopper: [0, 0.5] }
        shows: "declining the invite, but not in notrump: 6+ $m with a side suit wide open"
        establishes: { forcing: sign_off, agreed_suit: $m }
```

`weakest_unshown_stopper` carries sharp tolerance 0.3 in `_EVAL_S2` (it is
`weakest_THEIR_stopper` that does not gate), so this clause really gates.

**THE ANSWERING SEAT.**  `forcing: sign_off` — and I checked it rather than
assuming: at `1D P 1S P 2D P 2NT P 3D P`, responder's `uc_pass` fits **1.000**,
so the seat is covered and no new context is needed.

**WHAT IT ENDANGERS.**
* `oim2n_pass_$M$R` (50) — loses the 10-13 hands with six of the minor and an
  unstopped suit; one sentence: partner invited game in notrump and I am telling
  him notrump is the wrong strain, which is more information than a pass.
* `oim2n_3NT_$M$R` (58) and `oim2n_5m_$M$R` (61) are both above it and both
  floored at 14, so the accept and the minor game are untouched.
* It defines a call (`3$m`) that the generic toolkit currently supplies through
  `uc_rebid_$m3`; that rung reads "6+ cards, values for the level", which is the
  same hand described worse.

**TEMPLATE.**  `expand_pairs` inherited — five rules for free.  The twin worth
authoring next is the same decline after a MAJOR opening's 2NT invite.

**VERIFIED / UNTESTED.**  Context, rung inventory and all four evaluator values
VERIFIED; rung UNTESTED.

---

## Board 328 — margin -1

**Seat/call.** North, call 4: `1D X 1S X` → `xd_pass` sits for their double on
`AKT5.973.KQ632.6` (12 HCP, four-card spade support for partner's 1S).  BEN
bids 2S (0.98).

**Competitive** (their second double of our free response).  NOTHING-WRONG on
the constructive machinery, but this is the same species as boards 730 and 754
and I record it as such.

**What I checked.**  `xd_raise_S2` fits **0.000** — it wants "3+ trumps, 6-9
support points", and this hand has twelve, so the *minimum* raise denies a hand
too good for it while nothing above it fits either (`xd_jumpraise_S3` needs
"4+ trumps, 10+" and fits 0.082 because it also demands a jump).  The result is
a hole between 9 and 10 support points in the doubled-auction raise ladder, and
a hole is a pass by construction.  The general repair is the one I propose on
board 730: **opener's whole natural rebid structure is unauthored after RHO
doubles responder's one-level response**, and `general_after_their_double`'s
run/rebid rungs are standing in for it.  I put the proposal on 730 because
there the missing call (a four-card major at the one level) is unambiguous.

---

## Board 356 — margin -1

**Seat/call.** North, call 4: `P 1D 1H 2C` → `cl_raise_H2` raises partner's
heart overcall to 2H on `9543.Q83.Q4.JT96` (5 HCP, three
trumps).  BEN passes (1.00).

**Purely competitive** (advancing an overcall in a live auction).
NOTHING-WRONG from my discipline.

**What I checked.**  `cl_raise_H2` fits 1.000 on "3+ trumps, 6-9 support points,
7+ combined trumps" — the hand has 5 HCP and `Q83`, i.e. six support points at
best, so it is inside the band by the softest possible margin and the raise is a
judgment call, not a defect.  Nothing constructive is at stake; the auction is
competitive from call 2 onwards.

---

## Board 361 — margin -1

**Seat/call that went wrong.** West, call 6: `P P 1S P 1NT P` → `ob_1M1NT_2S`
rebids 2S on `KQJ654.QJ84.Q.Q7` (13 HCP, **6-4** in the majors).  BEN bids 2H
(0.99).  We play 2S for eight tricks (+110); the 2H route plays 3H for nine
(+140).

**The missing agreement.** With six spades and four hearts and a minimum,
opener's rebid over the forcing notrump is 2H — responder can pass it, raise it,
or take a two-level preference back to spades, and the file forbids exactly this
hand from bidding it.

**Traced (VERIFIED).**  The rule that should own the call,
`ob_1S1NT_2H`, carries `not: { suits: { S: [6, 13] } }` — an explicit denial of
the 6-4 shape — and fits **0.100**.  Evaluators: `hcp = 13`,
`total_points = 15`, `good_suit(S) = 1.0`.  So `ob_1M1NT_3S` (16-19 playing
strength) misses by one point at fit 0.800 and `ob_1M1NT_2S` wins at 1.000.
The context's own comment says the 5-4 rung was authored because "a 5-4 major
hand had nothing to say and the generic 3NT took over: on the BEN match that
jump was the single most expensive call in the rulebook" — the 6-4 hand is the
same argument, one card longer.

**EXACT YAML** — an additive sibling in the existing context
`opener_rebid_1S_1NT_second_major` (do NOT relax `ob_1S1NT_2H`'s denial; a new
rung is additive, a widened gate is not):

```yaml
      - id: ob_1S1NT_2H_64
        call: 2H
        priority: 54.5
        requires:
          suits: { S: [6, 13], H: [4, 4] }
          evals: { total_points: [12, 15] }
        shows: "six spades and exactly four hearts, minimum: the second suit first, spades are still there at the two level"
        establishes: { forcing: non_forcing }
```

**THE ANSWERING SEAT — SHIPS WITH IT, and it is currently starved.**
I traced `1S - P - 1NT - P - 2H - P - ?` with the board's own responder hand
(`3.AT52.8742.AJ94`): `context_at` → `['general_uncontested_continuation',
'general_slam_try']`, and the winner is **`uc_raise_H4` at fit 1.000, prio 32** —
a four-level raise on nine points opposite a shown minimum.  That is the whole
reason 2H is dangerous today and the reason the 6-4 denial was probably written.

```yaml
  - id: responder_over_second_suit_1M1NT
    description: "Responder's preference after 1S - 1NT - 2H (or 1H - 1NT - 2m)"
    pattern: "1S - P - 1NT - P - 2H - P - ?"
    rules:
      - id: rss_pass_H
        call: P
        priority: 52
        requires: { suits: { H: [3, 13] }, hcp: [6, 8] }
        shows: "hearts are as good as anything: passing the second suit"
        establishes: { forcing: sign_off }
      - id: rss_2S
        call: 2S
        priority: 54
        requires: { suits: { S: [2, 13] }, hcp: [6, 10] }
        shows: "preference back to the six-card suit: 6-10"
        establishes: { forcing: sign_off, agreed_suit: S }
      - id: rss_3H
        call: 3H
        priority: 56
        requires: { suits: { H: [4, 13] }, hcp: [9, 11] }
        shows: "four-card support for the second suit, maximum: inviting game"
        establishes: { forcing: invitational, agreed_suit: H }
      - id: rss_3S
        call: 3S
        priority: 55
        requires: { suits: { S: [3, 13] }, hcp: [9, 11] }
        shows: "three-card support for the six-card suit, maximum: inviting game"
        establishes: { forcing: invitational, agreed_suit: S }
      - id: rss_floor
        call: P
        priority: 40
        requires: {}
        shows: "no better description: the second suit stands"
        establishes: { forcing: sign_off }
```

On the board this puts responder in 3H (four trumps, 9 HCP) and opener, a dead
minimum, passes — 3H for nine tricks, which is BEN's +140.

**WHAT IT ENDANGERS.**
* `ob_1M1NT_2$M` (54) — loses 6-4 minimums; one sentence: with 6-4 the second
  suit is free, because spades are still available at the two level and a
  preference costs nothing.
* `ob_1M1NT_3$M` (56) is above it and keeps 16-19; `ob_1M1NT_4$M` (57) keeps
  20+; `ob_1M1NT_2C`/`2D` (52/53) are below it and describe 3-card and 4-card
  minors, which a 6-4 major hand should never prefer.
* The new answering context takes P, 2S, 3H and 3S from
  `general_uncontested_continuation` at that node — and that is the point: it
  removes `uc_raise_H4`'s fit-1.000 four-level raise on nine points.
* `ob_1S1NT_2H` (53.5) is untouched: my rung requires six spades, its denial
  excludes them, so the two are disjoint by construction.

**TEMPLATE.**  The 2H rung is single-suit by nature (`1H - 1NT - 2S` would be a
reverse), so no expansion.  The ANSWERING context should be templated across
every `1M - 1NT - <second suit>` node:
`expand_pairs: [{M: S, X: 2C}, {M: S, X: 2D}, {M: S, X: 2H}, {M: H, X: 2C}, {M: H, X: 2D}]`
with `pattern: "1$M - P - 1NT - P - $X - P - ?"` — that seat is starved for all
five, not only for 2H, and it is where the 1NT-rebid family loses its boards.

**VERIFIED / UNTESTED.**  The 0.100 fit, the explicit 6-card denial, the
evaluator values and the starved answering seat (including `uc_raise_H4` at fit
1.000) are all VERIFIED by trace.  Both new pieces UNTESTED.

---

## Board 401 — margin -1

**Seat/call that went wrong.** South, call 9: `P 1C P 1H P 1NT P 2S P` → opener
bids **2NT through `uc_nt2`** on `J93.AK.963.AT985`.  There is no context for
this node.  (Responder's 2S at call 7 is `rr_nt_second_S`, fit 1.000, which is a
legal authored call — the problem is that nothing answers it.)

**The missing agreement.** `rr_nt_second_$oM` — responder's 5-4 second suit
after opener's 1NT rebid — is an authored, non-forcing, shape-showing call with
**no answering seat**, so opener guesses in the generic notrump ladder.

**Traced (VERIFIED).**  `context_at('P 1C P 1H P 1NT P 2S P')` →
`['general_uncontested_continuation', 'general_slam_try']`.  Candidates:
`uc_nt2` 1.000/28 (wins), `uc_raise_C3` ... `uc_pass` 1.000/18,
`uc_rebid_C3` 0.279, `uc_nt3` 0.107.  I traced the same node with a 1D opening
(`1D P 1S P 1NT P 2C P`, board 993's opener): same context list,
`uc_nt2` 1.000/28 and `uc_raise_C3` 1.000/27 — opener **raises responder's
second suit as if it were a natural minor opening**.

**EXACT YAML** — two small contexts, because the preference costs a level in one
direction and not the other (this is why one templated context cannot do it):

```yaml
  - id: opener_over_second_suit_higher
    description: "Opener after 1m - 1H - 1NT - 2S (responder's 5-4, second suit above the first)"
    expand: { m: [C, D] }
    pattern: "1$m - P - 1H - P - 1NT - P - 2S - P - ?"
    rules:
      - id: oss_hi_3H_$m
        call: 3H
        priority: 54
        requires: { suits: { H: [3, 3], S: [0, 2] }, hcp: [14, 14] }
        shows: "maximum with three hearts and a doubleton spade: correcting to the five-card suit"
        establishes: { forcing: non_forcing, agreed_suit: H }
      - id: oss_hi_3S_$m
        call: 3S
        priority: 55
        requires: { suits: { S: [4, 13] }, hcp: [14, 14] }
        shows: "maximum with four-card support for the second suit: inviting game"
        establishes: { forcing: invitational, agreed_suit: S }
      - id: oss_hi_pass_$m
        call: P
        priority: 50
        requires: {}
        shows: "the 12-14 rebid is limited and partner has chosen a spot: pass"
        establishes: { forcing: sign_off }

  - id: opener_over_second_suit_lower
    description: "Opener after 1m - 1S - 1NT - 2H (responder's 5-4, second suit below the first)"
    expand: { m: [C, D] }
    pattern: "1$m - P - 1S - P - 1NT - P - 2H - P - ?"
    rules:
      - id: oss_lo_2S_$m
        call: 2S
        priority: 54
        requires: { suits: { S: [3, 3], H: [0, 2] } }
        shows: "three spades and a doubleton heart: preference back to the five-card suit"
        establishes: { forcing: sign_off, agreed_suit: S }
      - id: oss_lo_3H_$m
        call: 3H
        priority: 55
        requires: { suits: { H: [4, 13] }, hcp: [14, 14] }
        shows: "maximum with four-card support for the second suit: inviting game"
        establishes: { forcing: invitational, agreed_suit: H }
      - id: oss_lo_pass_$m
        call: P
        priority: 50
        requires: {}
        shows: "the 12-14 rebid is limited and partner has chosen a spot: pass"
        establishes: { forcing: sign_off }
```

Both `pass` rungs carry `requires: {}` so the seat can never starve (round 6's
`rkc5H_signoff` lesson).

**THE ANSWERING SEAT.**  `oss_hi_3S_$m` / `oss_lo_3H_$m` are invitations, and
their answering seat is responder's — who is already limited at 6-11 by the 1NT
response's context, so `uc_pass` at fit 1.000 covers the decline and the accept
is a jump to game that `gf_landing_major` covers once a major is agreed.  I did
not verify that pair by trace and flag it as the weakest link in this proposal:
if the round wants belt and braces, add a three-rung
`1$m - P - 1$M - P - 1NT - P - 2$oM - P - 3$X - P - ?` context (pass / 4$X).

**WHAT IT ENDANGERS.**
* `uc_nt2` (28) and `uc_nt3` (29) lose 2NT/3NT at these two nodes — one
  sentence: opener has already shown 12-14 balanced, so a second notrump bid
  adds nothing that partner does not know, while a preference names the strain.
* `uc_raise_C3` / `uc_raise_D3` (27) lose the three-level minor raise there —
  responder's 2S/2H is a second SUIT, not a raise, and reading it as one is the
  actual bug this board exhibits.
* `uc_pass` (18) is replaced by a pass with a stated meaning, same call.
* Nothing above 30 is defined by either context, so `gst_rkc_*` (46) and the
  slam-try family are untouched.

**TEMPLATE.**  `expand: { m: [C, D] }` on each (4 rules + 4 rules).  The twin for
the major-opening auction (`1H - 1S - 1NT - 2m`) has the same hole.

**NEGATIVE RESULT, stated plainly.**  Authoring this seat correctly makes THIS
board worse: opener holds `J93` and a minimum, so `oss_hi_pass_C` fires and we
play 2S for ten tricks (+170) instead of the accidental 3NT for nine (+400).
The board is nonetheless won by board 993's rung — `rr_nt_shape4_$M` fires on
responder's hand here too (`total_points = 14`, void in clubs → `singleton_or_void
= 1`, six hearts), producing **4H** at call 7 for ten tricks and +420, which
ties the board.  I would ship the two together and screen them as one subject.

**VERIFIED / UNTESTED.**  The starvation, both candidate sets and responder's
evaluator values VERIFIED by trace; both contexts UNTESTED.

---

## Board 427 — margin -1

**Seat/call.** North, call 5: `P P 1D P 1H` → `sw_pass` in the sandwich seat on
`J765.KJ2.4.AJT42`.  BEN bids 1NT (0.99), which we do not have as an agreement
there (`FALLBACK` fits 0.000).

**Purely competitive** (sandwich seat).  NOTHING-WRONG.

**What I checked.**  `sw_2C` fits 0.800 and loses to `sw_pass` at 1.000 —
"good 5+ clubs, 11-17" against `AJT42` and ten points, so the miss is the suit
quality plus a point.  Our later 2C at call 9 (`ballow_new_C2`) is the same call
one round later and BEN passes it.  There is no constructive seat here; both
sides are bidding.

---

## Board 551 — margin -1

**Seat/call.** North, call 1: over 1S we pass on `5.KQT87.KQ643.32`
(10 HCP, 5-5 reds).  BEN bids 2S (0.92 — Michaels again, scoped out).

**Purely competitive** and the divergence is an excluded convention.
NOTHING-WRONG.

**What I checked.**  `oc1S_2D` and `oc1S_2H` both fit 0.800 (the 11-17 floor,
missed by one) and both lose to `oc1S_pass` at 1.000.  Two five-card suits and
ten points is precisely the hand a two-suited overcall exists for, and we have
ruled that out by design; picking one red suit at the two level on 10 HCP
vulnerable is not clearly better than passing.

---

## Board 555 — margin -1

**Seat/call.** North, call 1: over 1C we overcall 1H on `9543.AKQ854.T.94`
(9 HCP, six hearts).  BEN bids 2H (0.87, the weak jump).

**Competitive at the entry.**  NOTHING-WRONG — and the re-ranking of the weak
jump overcall against the simple overcall is explicitly on the do-not-re-propose
list (round 11 measured it at -24 held out).

**The constructive observation, which is real.**  Look at what happens *after*
the overcall: `1C 1H P 2D P 2H P 3D P 3H P 4D`.  Every one of those calls is
`uc_rebid_*` — the generic toolkit — because **there is no context for the
overcaller's rebid after advancer bids a new suit**, and none for advancer's
rebid after that.  The two hands invent a suit each turn and land in 4D on a
6-5 fit that was known from call 3.  The file has eleven `advance_*` contexts
for advancing a takeout DOUBLE and none for advancing an overcall constructively.
That is a whole subject at zero, in the same species as the trial bid and the
fit-showing jump, and it is too big for one board in this slice; I record it as
the largest unauthored constructive subject I found in part 8 and recommend it
be scoped as its own subject rather than a rung.

---

## Board 631 — margin -1

**Seat/call.** North, call 1: over their 2D we bid 2NT on `AQ3.AJT93.AJT.82`
(16 HCP, five hearts).  BEN bids 2H (0.99).

**Purely competitive** (defence to a weak two).  NOTHING-WRONG.

**What I checked.**  `vw2_2NT` fits 1.000 (15-18 balanced with a stopper) and
`vw2D_over_2H` also fits 1.000 (natural overcall, good 5+ H, 11-16); 2NT wins on
priority 72 against 64.  Both descriptions are true of the hand, so this is a
genuine priority tie between two correct readings, not a hole — the species the
round-16 note calls "a real judgment call", and the 5-3-3-2 16-count with a
five-card major genuinely splits expert opinion.  I will not move a priority on
one -1 IMP board.

---

## Board 642 — margin -1

**Seat/call.** North, call 6: `P 1C X 1H P 2H` → `cl_pass` on
`KQ.AJ6.AKQ3.Q963` (21 HCP, having already doubled).  BEN doubles again (0.65).

**Purely competitive** (the doubler's second action).  NOTHING-WRONG.

**What I checked.**  The only X candidate is the code FALLBACK at prio 9 /
fit 0.349 — i.e. **the doubler's second double is unauthored**, which is the
standing open item "no opener's reopening/second double" wearing the advancer's
hat.  It is on the deferred list with its own reason (adding a third meaning to
X in a context that already defines two is a `collide` risk and wants its own
round), so I am not proposing it here.  Nothing constructive is at stake.

---

## Board 643 — margin -1

**Seat/call.** North, call 5: `P 1D 2C P P` → `ballow_pass` on
`Q762.AJ.AQ942.J9` (14 HCP).  BEN reopens with a double (0.56).

**Purely competitive** (balancing after our opening is overcalled and passed
round).  NOTHING-WRONG.

**What I checked.**  `ballow_reopen_X` fits 0.409 — it demands **16+**, and the
reopening double after our own opening is exactly the 12-15 hand's call.  That
ceiling-from-below is a real defect of the same species as the ones this project
has paid for, but it is a competitive rung and belongs to the other reviewer.
The constructive half of the board (opener's 1D) is correct.

---

## Board 689 — margin -1

**Seat/call.** North, call 3: `1C X 1H` → `cl_new_S1` bids 1S on
`KT653.A73.Q.JT92` (10 HCP, five spades) as advancer of partner's takeout
double.  BEN bids 2S (0.37 — itself unconfident).

**Purely competitive** (advancing a takeout double over their free bid).
NOTHING-WRONG.

**What I checked.**  `cl_new_S1` fits 1.000 on "4+ cards, 6+ points"; the hand
has five spades and ten points, so the *jump* advance (9-11 invitational) is
what BEN wants and `advance_*` contexts supply it only after a double of a
weak two or a balancing double, not after a double of a one-bid followed by a
free bid.  That is a competitive sibling gap; I flag it and leave it.

---

## Board 730 — margin -1

**Seat/call that went wrong.** South, call 4: `1D P 1H X` → `xd_rebid_D2` bids
2D on `Q742..AKJT62.T53` (10 HCP, **four spades**, a heart VOID, six diamonds).
BEN bids 1S (0.65).  We play 2D for ten tricks (+130); the 1S route reaches 3S
for ten (+170).

**The missing agreement.** When RHO doubles responder's one-level major, opener
still has a four-card major of his own to show at the one level — the support
redouble context owns the seat and offers only XX, a raise and a pass.

**Traced (VERIFIED).**  Context `support_redouble[D,H]` owns the node.  Its
whole rule list is `srd_redouble` (exactly 3 $M — the hand has zero, fit 0.000),
`srd_raise` (4+ $M — 0.000) and `srd_pass` (12-14 and 0-2 $M — fit 0.409 on
`hcp = 10`).  Everything else the seat needs comes from the generic
`general_after_their_double`: `xd_rebid_D2` 1.000/34, `xd_run_S1` 0.349/**24**
("running to my own S: 5+ cards" — it demands five, and it is *running*, not
showing).  Evaluators: `hcp = 10`, `total_points = 12`.

**EXACT YAML** — one additive rung in the existing `support_redouble` context
(`expand: { m: [C, D], M: [H, S] }` already present; the `when:` guard makes the
M=S copies structurally inert rather than nonsense):

```yaml
      - id: srd_1S_$m$M
        call: 1S
        priority: 70
        when: { unbid_suit: S }
        requires:
          suits: { S: [4, 13] }
          not: { suits: { $M: [3, 13] } }
          evals: { total_points: [10, 19] }
        shows: "four+ spades at the one level: the double does not stop opener showing his own major"
        establishes: { forcing: one_round }
```

Priority 70 sits below `srd_redouble` (85) and `srd_raise` (80), so three-card
and four-card support still take precedence — showing support is more urgent
than showing a second suit — and above `srd_pass` (30) and everything generic.

**THE ANSWERING SEAT.**  `forcing: one_round`, and I checked where the answer
lands: responder's seat after `1D P 1H X 1S P` is `general_competitive_low`,
where `cl_raise_S*`, `cl_rebid_H*` and `cl_nt*` all exist and fit — the seat is
populated, unlike the support-double seat on board 966.  No new context needed;
if the round wants one, it is the same shape as the `sda_*` context proposed on
board 966.

**WHAT IT ENDANGERS.**
* `xd_run_S1` (24) loses the 1S call at this node — one sentence: with four
  spades and opening values this is a suit being SHOWN, not a hand running, and
  the rung that says "running, 5+ cards" mis-describes it in both halves.
* `srd_pass` (30) loses 10-19 hands with four spades and fewer than three
  cards in responder's major; passing partner's doubled one-bid with a
  four-card major of your own and a void in his suit is the error on the board.
* `srd_redouble` (85) and `srd_raise` (80) are untouched — my `not:` clause
  denies three-plus support, which is exactly what those two show.
* `xd_rebid_$m2` (34) keeps every hand without four spades.

**TEMPLATE.**  `expand: { m: [C, D], M: [H, S] }` inherited (4 rules, 2 live).
The exact twin is owed in `support_double` for the non-doubled interference
case: `1D - P - 1H - (2C) - 2S`? — no, at the two level that is a reverse; the
one-level version is the whole agreement.

**VERIFIED / UNTESTED.**  Context ownership, the three-rung inventory, both
fits and both evaluator values VERIFIED by trace; rung UNTESTED.

---

## Board 748 — margin -1

**Seat/call.** North, call 4: `1NT P 2H P` → `tr_accept_2S` completes the
transfer on `A872.AJ5.A4.Q932` (15 HCP, **four** spades, a doubleton diamond).
BEN bids 2NT (0.97) — a super-accept in whatever structure BEN plays.

**The missing agreement.** The super-accept is one point wide.
`tr_super_3S` requires `hcp: [17, 17]` **exactly**, so a fifteen- or
sixteen-count with four trumps and a ruffing value has no way to tell partner
about the ninth trump before he passes at the two level.

**Traced (VERIFIED).**  Candidates at the node: `tr_accept_2S` fit 1.000 /
prio 55 (wins), `tr_super_3S` fit **0.409**.  Evaluators on the hand:
`hcp = 15`, `total_points = 15`, `controls = 6`, `shortness_points = 1`
(one doubleton; a 4-3-3-3 scores 0).

**EXACT YAML** — a second rung in each of the two (untemplated) transfer-accept
contexts, `nt_transfer_accept_H` and `nt_transfer_accept_S`:

```yaml
      # in nt_transfer_accept_S ("1NT - P - 2H - P - ?")
      - id: tr_super_ruff_S
        call: 3S
        priority: 58
        requires:
          suits: { S: [4, 5] }
          hcp: [15, 16]
          evals: { shortness_points: [1, 12] }
        shows: "super-accept: four spades and a ruffing value, 15-16 - the ninth trump is worth a level"
        establishes: { forcing: non_forcing, agreed_suit: S }

      # in nt_transfer_accept_H ("1NT - P - 2D - P - ?")
      - id: tr_super_ruff_H
        call: 3H
        priority: 58
        requires:
          suits: { H: [4, 5] }
          hcp: [15, 16]
          evals: { shortness_points: [1, 12] }
        shows: "super-accept: four hearts and a ruffing value, 15-16 - the ninth trump is worth a level"
        establishes: { forcing: non_forcing, agreed_suit: H }
```

`shortness_points` has no sharp tolerance (default sigma), so a 4-3-3-3
fifteen-count scores ~0.80 against it — **below the 0.9 fast path** — while
`tr_accept_2$M` sits at fit 1.000 and therefore still wins on the fast path for
those hands.  The soft gate is doing exactly the job it should here; I checked
that interaction rather than assuming it.

**THE ANSWERING SEAT — ALREADY EXISTS.**  `nt_after_super_accept`
(`1NT - P - 2$T - P - 3$M - P - ?`) with `trsa_game_$M` (4$M, hcp 5-40) and
`trsa_pass_$M` (`requires: {}`).  It was authored in an earlier round for
exactly this reason, so the conversation closes.  On this board responder holds
`QJ9653.4.QJT6.J8` (7 HCP, six spades) and would bid 4S.

**WHAT IT ENDANGERS.**
* `tr_accept_2$M` (55, `requires: {}`) loses the seat for 15-16 with four
  trumps and a doubleton — the whole point, and the mainstream agreement.
* `tr_super_3$M` (60) is above it and keeps the 17-count, so nothing is
  subtracted there.
* Downstream, `trsa_game_$M` now fires opposite 15-16 rather than only 17, so
  responder reaches game on 5 HCP opposite 15 with a nine-card fit.  **That is
  the risk in this proposal and I am not hiding it**: on this very board 4S is
  one down double-dummy (nine tricks) and only won because -100 beat -140.  If
  the round wants the safer version, floor the new rung at `hcp: [16, 16]`
  instead of 15-16, which keeps the answering ladder's arithmetic honest at the
  cost of not firing here.

**TEMPLATE.**  These two contexts are not templated in the file; write both
rungs out as above.  The 2NT-opening twins (`nt2_tr_accept`) and the 2C twin
(`r2c_tr_accept`) have the same one-rung ladder and the same hole.

**VERIFIED / UNTESTED.**  Fits, evaluator values and the existence of the
answering context VERIFIED by trace; rungs UNTESTED.

---

## Board 754 — margin -1

**Seat/call that went wrong.** South, call 4: `1H P 1S X` → `xd_pass` sits on
`AKJ.Q6543.762.A4` (14 HCP, **exactly three spades**).  BEN redoubles (1.00).

**The missing agreement.** The support redouble applies after a MAJOR opening
too: `1H - P - 1S - (X)`, XX = exactly three spades.  Ours is minor-only.

**Traced (VERIFIED).**  `support_redouble`'s pattern is `1$m - P - 1$M - X - ?`
with `expand: { m: [C, D], M: [H, S] }`, so `1H - P - 1S - X` matches no
support context and falls to `general_after_their_double`: `xd_pass` 1.000/18
wins, `xd_rebid_H2` 0.349, and **XX is not offered at all** — it appears nowhere
in the candidate list.  Evaluators: `hcp = 14`, `total_points = 15`, spades
exactly 3.  This is the pure sibling gap the `sibling` lint was built for; it
misses it because the gap is between two CONTEXTS, not two rules.

**EXACT YAML** — a new one-rung context, deliberately one rung so it shadows
nothing else (`general_after_their_double` keeps every other call at this node):

```yaml
  - id: support_redouble_major
    description: "Support redouble after 1H - 1S - (X): exactly 3-card spade support"
    pattern: "1H - P - 1S - X - ?"
    rules:
      - id: srdM_redouble
        call: XX
        priority: 85
        requires: { suits: { S: [3, 3] }, hcp: [12, 21] }
        shows: "support redouble: exactly 3-card spade support"
        establishes: { forcing: one_round }
        alertable: true
        convention: support_redouble
```

`1H - P - 1S` is the only major-opening auction in which responder bids a new
major at the one level, so this is the complete twin — one rule, not four.

**THE ANSWERING SEAT.**  Ships with board 966's `support_double_answer` context,
whose `expand_pairs` includes the `1H / 1S` row; add a matching row for the
redouble (`$o - P - 1$M - X - XX - * - ?`).  Without it responder lands in
`general_pull_or_sit` and reads our support redouble as a takeout redouble to be
pulled, which is board 966's traced failure exactly.

**WHAT IT ENDANGERS.**
* Nothing in the file defines XX at this node, so no rung is outranked.  The one
  thing it DOES subtract is the **code fallback for XX** in every seat this
  context's pattern reaches (round 15's mechanism: `covered` is built without
  consulting fit).  The pattern is five tokens and exact, so the blast radius is
  one auction shape and the fallback it removes is the undiscussed redouble —
  acceptable, and stated rather than assumed.
* `xd_pass` (18) loses nothing: it is a different call.

**TEMPLATE.**  None (single auction).  What SHOULD be templated is the answering
context on board 966.

**VERIFIED / UNTESTED.**  The absent context, the absent XX candidate and the
hand's exact three-card support VERIFIED by trace; rung UNTESTED.

---

## Board 765 — margin -1

**Seat/call.** North, call 3: `1C X 1H` -> `cl_new_D2_hi` bids 2D on
`A974.7.AQ874.T93` (10 HCP, four spades, five diamonds) as advancer of
partner's takeout double.  BEN doubles (1.00 - the responsive double).

**Purely competitive.**  NOTHING-WRONG, and the fix BEN wants is on the
do-not-re-propose list: a non-forcing responsive double was measured at -8 held
out in round 9 and reverted.

**What I checked.**  `cl_new_S1` (four spades at the one level, the call most
experts would make opposite a takeout double) fits **0.757** and loses to two
diamond rungs at fit 1.000 — the four-card major is outscored by the five-card
minor because the minor rung's length gate is satisfied exactly.  That is the
soft-fit model preferring the longer suit over the strain partner asked for,
and it is a scoring-model question, not a rule question.

---

## Board 768 — margin -1

**Seat/call.** North, call 0: pass in first seat with `A93.83.KJ972.K74`
(11 HCP, five diamonds).  `open_1D` fits 0.800, `open_1m_rule20` 0.800; both
lose to `open_pass` at 1.000.

**Scope-excluded** (opening style / rule-of-20 thresholds).  NOTHING-WRONG.

**Constructive observation.**  Two boards in this slice (987, 768) and one more
(213) are the same shape: an eleven-count with a five-card suit where both
opening rungs sit at 0.800 and the pass sits at 1.000.  The population is worth
naming even though the threshold itself is excluded — it is not a judgment call
being made, it is a rung missing its own gate by exactly one point, three times.

---

## Board 795 — margin -1

**Seat/call.** South, call 7: `P 1S 2D 2S 3D P P` → `balhigh_pass` on
`KJT5.T743.T5.Q53` (6 HCP, four-card spade support).  BEN bids 3S (0.89).

**Competitive** — and it is board 936 again, from the responder's seat instead
of the advancer's.  NOTHING-WRONG as a separate finding.

**What I checked.**  `balhigh_raise_S3` fits **0.018** (it wants ten support
points; the hand has seven) and `balhigh_raise_lott4_S` 0.002.  My board-936
rung `balhigh_raise_lott3_$M` as written has `total_points: [8, 14]` and would
NOT fire here either — seven points with four trumps opposite a one-level
opening is the classic Law hand, and the honest version of the rung would floor
at 6 with `lott_total_trumps >= 9`.  I am recording the disagreement between the
two boards rather than widening the gate to fit both: 936 (a fifth trump
opposite an OVERCALL) and 795 (a fourth trump opposite an OPENING) are different
risks, and if the round ships only one band, ship 8-14 and lose this board.

---

## Board 857 — margin -1

**Seat/call that went wrong.** North, call 11: `P P P 2C X 2D P 3D P 3S P` →
`uc_rebid_D4` bids **4D** on `A7.AK.AKQT975.K7` (23 HCP).  BEN bids 3NT (0.44).
We then drive to 5D for eleven tricks (+400); BEN's table plays 4S for ten
(+420).

**The missing agreement.** In a game force with no fit, a hand too strong for
the 3NT rung has no landing call at all: `gf_3NT` is capped at **17 HCP**, so
the 2C opener — the one hand in the system that is always above it — falls
through to the generic toolkit and rebids his suit for the third time.

**Traced (VERIFIED).**  `context_at` → `['general_uncontested_continuation',
'general_slam_try']` plus the `gf_landing_*` family.  Evaluators on the hand at
the node: **`hcp = 23`**, `weakest_unshown_stopper = **1.0**`,
`lott_total_trumps = 7`, `longest_suit_length = 7`, `suit_quality(D) = 3.5`.
`gf_3NT`'s three gates are `hcp: [0, 17]` (fails on 23),
`lott_total_trumps: [0, 7]` (passes), `weakest_unshown_stopper: [0.9, 9]`
(passes) and `not: longest_suit_length [6, 13]` (fails).  Both failures are
about the same hand type — the strong hand with a running suit — and it is the
2C opener's whole population.  This is the documented open item "after a 2C
opening partner's shown minimum is ZERO, so every combined-point gate is
unreachable" in its HCP-ceiling form.

**EXACT YAML** — a companion rung in the SAME context (`gf_landing_nt`), so no
new shadowing at all:

```yaml
      - id: gf_3NT_big
        call: 3NT
        priority: 34.5
        requires:
          hcp: [18, 40]
          evals: { lott_total_trumps: [0, 7], weakest_unshown_stopper: [0.9, 9] }
        shows: "no fit and every unshown suit stopped, with the values to bid game unilaterally: 3NT"
        establishes: { forcing: non_forcing }
```

The `longest_suit_length` denial is deliberately absent: at 18+ with no fit and
everything stopped, a long suit is where the tricks come from, and the reason
`gf_3NT` denies it (an 11-17 hand should show its suit first) does not apply to
a hand that has already shown it.

**THE ANSWERING SEAT.**  `forcing: non_forcing` on a game contract — partner's
pass is `gf_landing_*`/`uc_pass` at fit 1.000, and the 4$M pull is `gf_maj4H/4S`
and `gf_game_4$A`, all authored.  No new context.

**WHAT IT ENDANGERS.**
* `gf_3NT` (34) — nothing: its band is 0-17 and mine is 18-40, disjoint by
  construction, and I placed mine half a point higher only so the strong reading
  is the primary one on the explanation.
* `uc_rebid_$m4` (29) and `uc_nt3` (29) lose the seat for 18+ game-forced hands
  with everything stopped — one sentence: rebidding the same suit a third time
  in a game force describes nothing partner does not know, and 3NT names a
  contract.
* `gf_pref_3$M` (37) and `gf_new_3$X` (36) both remain above it, so three-card
  support for partner's major and a genuine five-card suit still win — which is
  right: 3NT is the *landing*, not the first choice.
* `gf_minor_3NT` (37) carries `when: standing_bid_strain: [$m]` and is not live
  at this node.

**TEMPLATE.**  None — `gf_landing_nt` is a single generic context and the rung
is generic with it.  What IS owed and is bigger than this board: a real
`opener_after_2C_positive` landing ladder, the standing open item.

**VERIFIED / UNTESTED.**  Both failing gates, all four evaluator values and the
winning candidate VERIFIED by trace; rung UNTESTED.

---

## Board 932 — margin -1

**Seat/call.** North, call 4: `P 1C 1S 2D` → `cl_negative_X2` doubles on
`K42.KQ42.J87.T42` (6 HCP, three-card spade support).  BEN bids 2S (0.90).

**Purely competitive.**  NOTHING-WRONG.

**What I checked.**  `cl_negative_X2` fits 1.000 on "8+ HCP with a major they
have not bid" — the hand has **six**, so the rule is describing a hand it does
not hold and won on priority 33 over `cl_raise_S2` at fit 1.000 / prio 30.
This is the `nxj_X` species (a double that promises points and nothing else,
ranked above every natural call), and the standing open item says the gate does
not pay: round 14 measured a longest-suit cap plus a four-card-unbid-major
requirement at -5 held out and reverted it.  I will not re-propose it.  The
constructive observation is the one the open item ends with: **author the
landing seats first** — here, a raise ladder that can outrank a double when the
support is real.

---

## Board 960 — margin -1

**Seat/call.** North, call 0: pass in first seat with `J.T87652.Q2.KQJ5`
(9 HCP, six hearts headed by the ten).  `open_weak_2H_nv` fits 0.757 (it wants
a good suit — two of the top three, or three of the top five — and `T87652` is
neither), so the disciplined weak two correctly declines and pass wins at 1.000.

**NOTHING-WRONG** — the weak-two discipline is a documented system choice
("exactly 6 cards, 5-10 HCP non-vul with a good suit") and the hand fails it on
suit quality, not on a missing rung.

**Constructive observation.**  The rest of the board is a redouble auction
(`1D X XX`), which is the other reviewer's territory.  One constructive note:
after our `rdx_XX` the seat at call 6 is `rdc_pass_D`, and BEN wants 1NT — the
redouble family's landing ladder is thin in the same way the 2C tree's is, and
both are known.

---

## Board 961 — margin -1

**Seat/call.** North, call 7: `P 1S P 2C P 2H P` → `gf_3NT` bids 3NT on
`A7.AT.Q952.KQJ95` (16 HCP).  BEN bids 3D (0.78).  3NT made nine (+400); BEN's
4H made ten (+420).

**NOTHING-WRONG.**  I traced every gate and the 3NT is honest: `hcp = 16`
(inside `[0, 17]`), **`weakest_unshown_stopper = 1.0`** — both unshown suits
(`Q952`, `KQJ95`) genuinely stopped — `longest_suit_length = 5` (so the
six-card-suit denial does not bite), `lott_total_trumps = 7` (no eight-card fit
with either of partner's suits: `A7` and `AT`).  Opposite a hand that has shown
five-plus spades and four-plus hearts, 3NT with a doubleton honour in each and
both minors stopped is the expert call; 4H beat it by one double-dummy trick in
a 5-2 fit.

**The constructive observation worth recording.**  `responder_21_after_second_suit_1S`
has exactly TWO rungs — set spades with three-card support, raise hearts with
four — and `gf_3NT` at priority 34 catches everything else.  There is no
fourth-suit rung, so a 16-count with 5-4 in the minors cannot describe itself
below 3NT even when the partnership is at 28+ combined points.  A rung shaped
like

```yaml
      - id: r21ss_fourth_D$x
        call: 3D
        priority: 69
        requires:
          suits: { D: [4, 13] }
          evals: { total_points: [16, 40] }
          not: { any_of: [ { suits: { S: [3, 13] } }, { suits: { H: [4, 13] } } ] }
        shows: "the fourth suit at the three level: 16+, no fit for either major, still looking"
        establishes: { forcing: game_forcing }
```

is what the "too good for 3NT" hand needs, and it is exactly the below-game
slam machinery round 17 asked for.  **I am NOT proposing it on this board**,
for two reasons I would rather state than bury: (1) it needs its own answering
seat (`1S - 2C - 2H - 3D - P - ?` is unauthored), and (2) on this hand it turns
a made 3NT into a guess, so the board is evidence against it, not for it.  It
belongs in a subject-sized batch with the 2/1 continuation ladder, screened
together.

---

## Board 966 — margin -1

**Seat/call that went wrong.** South, call 4: `1H P 1S 2D` → `cl_pass` passes on
`JT9.AK987.T75.A4` (12 HCP, five hearts, **exactly three spades**).  BEN doubles
(1.00) — the support double.  We defend 2D for five tricks (+150); the support-
double route reaches 3S for ten (+170).

**The missing agreement.** The support double is minor-only in this file.  After
`1H - P - 1S - (2D)`, opener with exactly three spades has no way to say so, and
responder can never distinguish a 4-3 fit from a 5-3 one.

**Traced (VERIFIED).**  `support_double`'s pattern is
`1$m - P - 1$M - bid<2$M - ?` with `expand_pairs` over `{C,D} x {H,S}` — four
combinations, none of them a major opening.  So `1H - P - 1S - 2D - ?` matches
no support context and falls to `general_competitive_low`: `cl_pass` 1.000/20
wins, `cl_raise_S2` 0.800, `cl_nt2` 0.668, and the only X candidate is the code
FALLBACK ("takeout-flavored cooperative double, undiscussed") at prio 9.
Evaluators: `hcp = 12`, `total_points = 13`, spades exactly 3.

**AND THE BIGGER FINDING: no seat in the file answers a support double, in any
of the five auctions.**  I traced responder's seat at
`1H P 1S 2D X P ?` with the board's own hand (`AK632.T5.963.KJT`):

```
ctx: ['general_pull_or_sit', 'general_uncontested_continuation', 'general_slam_try']
  2S adx_pull_my_S      fit=1.000 prio=60.0   <-- reads OUR support double as a
 2NT adx_nt             fit=0.835 prio=56.0       takeout double to be PULLED
   P adx_pass_min       fit=0.800 prio=52.0
```

That is the round-17 empty-seat shape on a call the file has been making for
several rounds: `sd_double` is `establishes: { forcing: one_round }`, alertable,
`convention: support_double`, and the seat that answers it does not exist.

**EXACT YAML — the ask.**  A new one-rung context, deliberately one rung so it
shadows nothing else at that node:

```yaml
  - id: support_double_major
    description: "Support double after 1H - 1S - (their bid below 2S)"
    pattern: "1H - P - 1S - bid<2S - ?"
    rules:
      - id: sdM_double
        call: X
        priority: 85
        requires: { suits: { S: [3, 3] }, hcp: [12, 21] }
        shows: "support double: exactly 3-card spade support, any strength"
        establishes: { forcing: one_round }
        alertable: true
        convention: support_double
```

**EXACT YAML — THE ANSWERING SEAT, for all five auctions at once.**  This is the
part that is not optional, and it fixes the four existing minor versions as well
as the new major one:

```yaml
  - id: support_double_answer
    description: "Responder after opener's support double (exactly 3-card support known)"
    expand_pairs:
      - { o: 1C, M: H }
      - { o: 1C, M: S }
      - { o: 1D, M: H }
      - { o: 1D, M: S }
      - { o: 1H, M: S }
    pattern: "$o - P - 1$M - bid<2$M - X - * - ?"
    rules:
      - id: sda_two_$o$M
        call: 2$M
        priority: 60
        requires: { suits: { $M: [5, 13] }, evals: { total_points: [6, 9] } }
        shows: "an eight-card fit is now known: competing to the two level"
        establishes: { forcing: non_forcing, agreed_suit: $M }
      - id: sda_three_$o$M
        call: 3$M
        priority: 61
        requires: { suits: { $M: [5, 13] }, evals: { total_points: [10, 12] } }
        shows: "an eight-card fit and invitational values"
        establishes: { forcing: invitational, agreed_suit: $M }
      - id: sda_four_$o$M
        call: 4$M
        priority: 62
        requires: { suits: { $M: [5, 13] }, evals: { total_points: [13, 40] } }
        shows: "an eight-card fit and the values for game"
        establishes: { forcing: sign_off, agreed_suit: $M }
```

Deliberately no `pass` and no four-card-support rungs: with only four cards in
the major the fit is 4-3 and the generic ladder should keep the seat, so this
context subtracts as little as possible.  On the board, responder holds five
spades and `total_points = 12` (traced), so `sda_three[1H,S]` fires and we reach 3S
for ten tricks — BEN's +170.

**Note on the evaluator, checked.**  I did NOT gate the answering rungs on
`lott_total_trumps`: at that node today it reads **5** for responder, because
partner's shown minimum for spades is zero until the support double exists as a
rule.  Once `sdM_double` / `sd_double` are in the tree the inference engine sets
partner's minimum spade length to 3 and the number becomes 8 — but a gate that
depends on the rule being installed to be satisfiable is the trap round 8
recorded, so the rungs count MY OWN length instead.

**WHAT IT ENDANGERS.**
* `cl_pass` (20) at `1H - 1S - (bid<2S)` loses the seat whenever opener holds
  exactly three spades and opening values — which is the entire agreement.
* The code fallback for `X` at that node is deleted (round 15's mechanism).  It
  was `prio 9 / "undiscussed"`, so what replaces it is strictly better defined,
  and the pattern is five tokens so the blast radius is one auction shape.
* In `support_double_answer`: `cl_raise_$M2` (30), `cl_raise_$M3` (31),
  `cl_raise_$M4` (32) and `cl_raise_lott*` lose 2$M/3$M/4$M **only in auctions
  where partner has just made a support double**, i.e. only where the trump
  count is exactly known — one sentence: a raise ladder that estimates the fit
  is strictly worse than one that has been told it.
* `adx_pull_my_$M` (60) loses those same three calls at those nodes, and that is
  the defect: it is pulling a double that was never takeout.
* `adx_pass_min` (52) and `adx_sit` (61) keep the pass, so a hand that wants to
  defend still can.
* Nothing in the new context outranks a slam-try or keycard rung (all >= 46 live
  in different contexts and are unaffected at the two and three level).

**TEMPLATE.**  The ask: none needed (`1H - 1S` is the only major-opening auction
where responder bids a new major at the one level), so one rule.  The answer:
`expand_pairs` over the five (opening, major) rows as written — 15 rules from
one idea, and it closes a conversation that has been half-authored for several
rounds.  The support REDOUBLE twin (board 754) adds a sixth row with `X - XX`
in the pattern.

**VERIFIED / UNTESTED.**  The minor-only pattern, the absent X rung, the
starved answering seat (`adx_pull_my_S` at fit 1.000), and both hands'
evaluator values are all VERIFIED by trace.  Both new pieces UNTESTED.

---

## Closing notes for whoever consolidates

* **Ship boards 966 + 754 as one subject.**  The ask, the twin and the shared
  answering context are one conversation; shipping the doubles without the
  `sda_*` context reproduces round 17's -9.8-IMPs-a-seat mechanism exactly, on a
  call the file already makes four ways.
* **Ship boards 993 + 401 as one subject.**  `rr_nt_shape4_$M` is one rule that
  gains on both; the two `opener_over_second_suit_*` contexts are the answering
  seat that `rr_nt_second_$oM` has never had.  Screen them together — 401 says
  the seat alone loses.
* **Ship boards 361 + 995 as one subject.**  Both are the 1NT-rebid family:
  opener's 6-4 second suit with the seat that answers it, and opener's third
  call after the preference with the seat that answers *that*.  Together they
  remove four `uc_*` decisions from live constructive nodes.
* **Board 285's re-rank is the cheapest change in this part** (one number) and
  the only one whose answering context already exists and was verified.  It is a
  good candidate for a standalone screen.
* **Two things I checked and refused to propose**, both because they are
  excluded or previously measured: freeing `cl_raise_lott3_$M` (board 936 — I
  built a different rule in a different context instead), and gating
  `cl_negative_X2` / `nxj_X` on shape (board 932, measured -5 held out in
  round 14).
* **The biggest unauthored constructive subject in part 8 is not in any of my
  proposals**: there is no context anywhere for the **overcaller's rebid after
  advancer bids a new suit** (board 555), against eleven `advance_*` contexts
  for advancing a takeout double.  That is a subject, and it should be scoped as
  one.
