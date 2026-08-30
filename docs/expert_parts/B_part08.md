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
