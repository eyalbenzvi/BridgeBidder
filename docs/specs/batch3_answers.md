# Batch 3 — the starved answering seats

**Spec:** `docs/specs/batch3_answers.spec` · **Apply with:**
`python3 tools/roundkit/addrules.py --spec docs/specs/batch3_answers.spec --report`

**Size after templating:** 31 authored context blocks and 93 authored rule ids
become **103 concrete contexts and 304 concrete rules**
(517 → 620 contexts, 2344 → 2648 rules).  Verified by building the patched
file and loading it: no duplicate ids, no unbound template vars, every
template var ends its rule id, `call:` never composes a level.

Every section here exists because the file already **asks** a question it
cannot hear the answer to.  Round 17 priced an empty answering seat at
**-9.8 IMPs a seat**; the mechanism is that every generic context ends in a
catch-all pass at fit 1.00, so *any hole in a ladder is a PASS by
construction*.  All eight starved seats in this batch were confirmed empty
before anything was written — `context_at` returning only
`general_uncontested_continuation` / `general_slam_try`, with `uc_pass` at fit
1.000 / priority 18 taking a one-round force.

---

## The floor convention, and why 44

Every ladder in this batch ends in a `requires: {}` rung **at the bottom**, and
that rung sits at **priority 44** (or 40 inside an existing context whose own
rungs run 63-67).  44 is not arbitrary: it clears, by a margin, every generic
rung that could otherwise answer a force by accident —

| generic rung | prio | what it was doing in these seats |
|---|---|---|
| `uc_pass` | 18 | passing one-round forces at fit 1.000 |
| `uc_new_*` 1/2/3 | 25 – 27.5 | inventing a fourth suit at the four level |
| `uc_rebid_*`, `uc_nt2`, `uc_nt3` | 27 – 29 | bidding 2NT over a sign-off |
| `uc_raise_*2/3/4`, `uc_raise_lott4_*` | 30 – 32 | accepting every invitation on 11 support points |
| `uc_doubler_*` | 33 – 35 | — |
| `gf_landing_*` | 30 – 38 | — |

and it sits **below** every descriptive rung in its own context, so the floor
can only ever win when nothing better fits.  This is the round-6
`rkc5H_signoff` lesson applied 31 times.

---

## Item 1 — the cue-raise answering family

Five cue-raise rules, **zero** answering contexts.  `nx3_cue` is *not* in this
batch: `opener_over_nx3_cue` (`1$M - 3$x - 4$x - P - ?`) already answers it.
The `advbal_*_cue` and `aw2*_cue` game-forcing cue advances are also out —
they land in the authored `gf_landing_new_suit` / `gf_landing_nt` ladders, not
in a catch-all pass, so they are not starved.

| force | answering context | floor |
|---|---|---|
| `r1H1S_cue` (2S, agreed H) | `opener_over_cue_raise_1H1S` | `cra1_min_3H` 3H @44 |
| `cra1_second_3C/3D` (GF, 5-5) | `responder_over_cue_raise_second_1H1S` | `crr1_game_$x` 4H @44 |
| `cra1_splinter_4C/4D` (GF, shortness) | `responder_over_cue_raise_splinter_1H1S` | `crr1_floor_$x` 4H @44 |
| `cra1_min_3H` (invitational) | `responder_over_cue_raise_minimum_1H1S` | `crr1_decline_3H` P @44 |
| `nx_1m1H_cue` / `nx_1m1S_cue` (agreed m) | `opener_over_cue_raise_1m_1M` | `cram_min_$m$M` 3m @44 |
| `cram_2NT_$m$M` (invitational) | `responder_over_cue_raise_minor_2NT` | `crrm_pass_$m$M` P @44 |
| `cram_min_$m$M` (non-forcing) | `responder_over_cue_raise_minor_min` | `crrn_pass_$m$M` P @44 |
| `r1M2x_cue` (3x, agreed M) | `opener_over_cue_raise_1M_2x` | `cra2_min_$M$x` 3M @44 |
| `cra2_min_$M$x` (invitational) | `responder_over_cue_raise_1M_2x_min` | `crr2_decline_$M$x` P @44 |
| `advo_cue` (2o, agreed v) | `overcaller_over_cue_raise` | `advcue_sign_$o$v` 2v @44 |
| `advcue_inv_$o$v` (invitational) | `advancer_over_overcall_invite` | `advcr_decline_$o$v` P @44 |

**Ordering inside `opener_over_cue_raise_1H1S`, and what each rung outranks.**
splinter 62 > second suit 60 > game 52 > minimum 44.

* 62/60 above 52: with a singleton or a five-five you *describe the shape*
  before you count anything.  Expert A reported the reverse order as a
  **negative result** — with the keycard ask on top, the engine asked
  immediately on the board-559 hand and bid 6H off two cashing tricks.
* 52 above 44: 14+ total points opposite a promised limit raise is a game,
  and the 44 rung is only "I have no other description".
* **No 4NT rung is authored anywhere in this family.**  The cue raise sets
  `agreed_suit` but not `game_forced`, so `rkc_ask` is dark; the moment a rung
  below sets `game_forcing` with a suit agreed, the file's **single audited
  `rkc_4NT` (priority 45)** goes live on its own.  DECISIONS records the cost
  of having two different floors for one convention; this batch adds none.
  That is why the responder-side floors sit at 44 — one point under `rkc_4NT`,
  so the ask wins when it fits and the floor catches everything else.
* `crr1_wasted_$x` at **46** is deliberately placed *above* `rkc_4NT` (45):
  with three or more points wasted opposite the shown shortness, the agreed
  game is enough and you must not ask.

**What this family outranks in each seat:** `uc_raise_H4` (32, and it fires on
30 tables at mean -0.70 — not a bad rule, an empty seat), `uc_raise_H3` (31),
`uc_rebid_H3` (29), `uc_new_D3` (27), `uc_pass` (18).  Each of them prices the
hand without knowing partner has already promised 10+ and agreed the suit.
4C and 4D at the 1H-1S-2S node were previously reachable only through the code
fallback; the new context defines them, which deletes that fallback there, and
the 3H floor at fit 1.00 is what makes that safe.

**A/B disagreement resolved.**  A proposed second-suit rungs and a 4NT ask;
B proposed splinters and a 3H floor.  Both are shipped, in B's order for the
shape rungs and with A's negative result honoured for the ask — *describe the
two-suiter or the singleton first, and let the one audited RKC floor decide
whether to ask at all.*

**Pattern-specificity decision, `overcaller_over_cue_raise`.**  Expert B wrote
the pattern with a `*` token so one context would own both the pass and the
competitive branch.  **Cut to `"1$o - 1$v - P - 2$o - P - ?"`.**
`advance_cue_doubled` already owns `"1$o - 1$v - P - 2$o - X - ?"` at the same
specificity (1006) and, being earlier in the file, wins the tie — so a `*`
pattern would have silently lost this ladder's `requires: {}` floor after a
double, exactly the failure mode the batch exists to remove.  The doubled
branch keeps its own authored retreat (`advcueX_XX` / `advcueX_retreat`).

**Motivating boards:** 559 (A part 1, B part 1), 580 (A part 1), 655 (B part 4).
Trace 559: `P 1H (1S) 2S P` → **4C** `cra1_splinter_4C` fit 1.000/62 (was
`uc_raise_H4` 1.000/32); responder → 4H or, with the values, `rkc_4NT`.

---

## Item 2 — `fourth_suit_reply` is starved

The file's one game-forcing ask below 2NT had exactly two answers — "stopper"
and "three-card support".  Opener with neither (5-5, no stopper, a doubleton
in partner's suit) topped out at **fit 0.349** across the whole candidate set,
the soft-miss lottery handed him `fsfr_raise_$F`, and on board 945 he bid 3S
holding **two** spades; partner believed an eight-card fit, asked for keycards
on a 27-count and we played 5S.

**Mechanical constraint that changed the design.**  `addrules.py` appends
*rules*; it cannot edit a context's `expand_pairs`.  Expert B's proposal added
three new template vars (`REB1`, `REB2`, `TAG`) to the existing pairs, which is
not applicable.  The third answer is therefore written with the **existing**
vars plus `when: { my_suit: X, cheapest_in_suit: true }`, which is exactly
"the cheapest call in a suit I have actually bid":

| auction | my suits | rungs that survive the `when` |
|---|---|---|
| `1C-1H-1S-(2D)` | C, S | 3C / 2S |
| `1C-1D-1S-(2H)` | C, S | 3C / 2S |
| `1D-1H-1S-(2C)` | D, S | 2D / 2S |
| `1D-1S-2C-(2H)` | D, C | 3D / 3C |
| `1H-1S-2C-(2D)` | H, C | 2H / 3C |

`cheapest_in_suit` drops the 3D rung wherever 2D is available, and the engine's
own legality check drops 2D wherever the fourth suit has already passed it, so
exactly one rung per suit is ever live.  Ten rungs, five expansions, **50
rules**, no `expand_pairs` edit.

**Priced by cheapness, not by first-versus-second suit** (2D 63.5 > 2H 63 >
2S 62.5 > 3C 62 > 3D 61.5, floors 47.5/47/46.5/43/42.5).  Expert B ranked the
first suit above the second; the template cannot distinguish them, and cheapest
is the better rule anyway — it leaves partner the most room.  The one visible
consequence: board 945's hand now bids **3C** rather than B's 3D.  Both fit
1.000, both say "five-five, no heart stopper"; 3C keeps 3D and 3NT alive.

**What it endangers.**  `fsfr_2NT_$F` (68) and `fsfr_raise_$F` (66) both stay
above: the stopper answer is still first, and a genuine third trump is still
the more important message.  What changes is that `fsfr_raise_$F` can no
longer win at fit 0.349 — verified, board 945 now shows `fsfr_extra_C3_2H`
1.000/62 with the raise sitting at 0.349 below it.  Below: `uc_rebid_C3` /
`uc_rebid_D3` (27) demand six cards and 11+ points, which is why this seat was
empty; the new rungs are a superset for the five-card case.  Defining these
five calls deletes the code fallback for them at this node — the five floors,
each at fit 1.00, are what makes that safe.

**Answering seat:** already authored.  The new rungs are `game_forcing` and
land in `gf_landing_preference_major` / `gf_landing_major` /
`gf_landing_minor` / `gf_landing_nt`, which is why the third answer had to be
**natural** rather than another artificial one.

**Motivating board:** 945 (B part 3).

---

## Item 3 — the forcing new suit opposite a weak two

A **named open item** in `ROUND_METHOD.md` and the fourth instance of the
species.  `rw2_new_$W_$X` is `forcing: one_round` and `2$W - P - <new suit> -
P - ?` matched no context: the generic toolkit invented `uc_rebid_D3`,
responder passed it at `uc_pass`, and `2D-2S-3D-P` died at **-100** where
`2D-2S-3D-3H-P` is **+140**.

Four contexts, 27 concrete, 67 rules, and every branch ends in `requires: {}`:

| force | answering context | floor |
|---|---|---|
| `rw2_new_*` into a **major** | `opener_after_weak2_new_major` (4 pairs) | `w2a_rebid_$K` 3W @44 |
| `rw2_new_*` into a **minor** | `opener_after_weak2_new_minor` (5 pairs) | `w2b_rebid_$K` 3W @44 |
| `w2a_rebid` / `w2b_rebid` | `responder_after_weak2_rebid` (9 pairs) | `w2r_pass_$K` P @44 |
| `w2r_second_H/S` | `opener_after_weak2_second_suit` (6 pairs) | `w2s_pass_$K` P @44 |
| `w2a_raise` | `responder_after_weak2_raise` (3 pairs) | `w2g_pass_$K` P @44 |

**Two corrections to the reviewer's version, both correctness.**

1. **Illegal calls.**  B's second-suit table contained
   `{ W: H, R: 2S, Y: 3D }` and `{ W: S, R: 3D, Y: 3H }` — after `2H-2S-3H`
   you cannot bid 3D, and after `2S-3D-3S` you cannot bid 3H.  Rewritten as
   two `when`-gated rungs, `3H` and `3S`, each with
   `when: { unbid_suit: <suit>, cheapest_in_suit: true }`.  Illegal ones are
   dropped by the engine, ours-already-bid ones by `unbid_suit` (a hard
   auction gate, unlike the `is_unbid_suit` *evaluator*, which does not gate).
   Result: the five legal second-suit branches survive, the four impossible
   ones simply have no rung, and the pass floor covers them.
2. **The minor raise is cut.**  B's single context raised the new suit at
   `$A`, which for a minor is 4C/4D — past 3NT.  Split into a major context
   (raise + floor) and a minor context (floor only): a weak two with three of
   partner's minor has nothing to say that is worth that much room.

**Duplicate-pattern hazard removed.**  B's `responder_after_weak2_rebid` and
`responder_weak2_second_suit` carried the *same* pattern for overlapping pairs,
which would have produced two concrete contexts with identical patterns.
Merged into one nine-pair context.

**What it outranks:** `uc_rebid_D3` (27), `uc_nt2` (28), `uc_nt3` (29),
`uc_raise_S3/S4` (31/32), `uc_pass` (18) — the entire generic toolkit at three
seats, every rung of which is describing a hand it has no information about
(`uc_rebid_D3` shows "values for the level opposite partner's shown range", and
opposite a weak two there is no such range).  The two `requires: {}` sign-offs
delete the code fallback for P and 3W in these auctions; both fit 1.00 on every
hand.  Regression: `2D-P-3D-P-?` (plain raise) and `2D-P-2NT-P-?` (feature ask)
are byte-identical — still `uc_pass` and `feat_D_S`.

**Motivating board:** 289 (B part 7).  Traced end to end:
`P 2D P 2S P` → **3S** `w2a_raise_DS` (with three spades) or **3D**
`w2a_rebid_DS` (with two); then `3H` `w2r_second_H_DS` 1.000/56; then
`w2s_pass_DSH` 1.000/44, or `w2s_raise_DSH` 4H on a maximum with four.

---

## Item 4 — a reverse is forcing with no answer below 8 points

Every `rrev*` rung floors at `hcp: [8, 40]`, so a 4-count with six spades fit
nothing above **0.028** and `uc_pass` took a one-round force at fit 1.00.
`rrevh_2S` never fires in the whole corpus.

Six rungs into the three existing reverse contexts:

* `rrev_min_2$M` / `rrevh_min_2S` / `rrevd_min_2S` — 5+ suit, **0-7**,
  priority 67.  Disjoint from `rrevh_2S` (66, 8+), so nothing moves; the call
  becomes a two-way reading, which is a *gain* in negative inference.
* `rrev_floor_$M` (3C) / `rrevh_floor_3C` / `rrevd_floor_3D` — `requires: {}`
  at priority **40**, a preference to opener's first suit.  40 is below every
  authored rung in those contexts (63-67) and far above `uc_pass` (18).

**Disagreement with myself, resolved: one call, one meaning.**  A first draft
gave the preference two rungs — a forcing 8+ version at 59 and the 0-7 floor —
so that a strong hand with nothing else to say kept the auction alive.  **Cut.**
The forcing version would have been answered by `opener_over_reverse_preference_*`,
whose floor is a *pass*, i.e. it would have re-created the exact defect this
item exists to remove.  The residue it served — 8-11, unbalanced, no five-card
suit, no four-card support and no stopper — is very rare, and the current
behaviour there is a pass of the reverse, which is strictly worse.  Recorded as
a knowingly accepted narrow loss.

Answering seats (all new, all with a `requires: {}` floor):

| force | answering context |
|---|---|
| `rrevh_min_2S` / `rrevd_min_2S` (0-7) | `opener_over_reverse_weak_rebid` — 4S @56 (20+), 3S @52 (18-19, invitational), P @44 |
| `oarw_inv_$m` (invitational) | `responder_over_reverse_weak_raise` — 4S @50, P @44 |
| `rrev_min_2$M` (0-7, the 1C-1M-2D reverse) | `opener_over_reverse_2M_weak` — **P @44 only** |
| `orev_raise_3$M` (**pre-existing**, one_round) | `responder_over_reverse_raise` — 4M @50, P @44 |
| `rrev_floor_$M` (3C preference) | `opener_over_reverse_preference_2D` — 3NT @52 (19+, stoppers), P @44 |
| `rrevh_floor_3C` / `rrevd_floor_3D` | `opener_over_reverse_preference_2H` — 3NT @52, P @44 |

**The `covered` trap, handled explicitly.**  `opener_over_reverse_2M_weak`
deliberately does **not** define 3$M.  `opener_raise_after_reverse` already
defines it at the same specificity (1009) and, being earlier in the file, owns
the call — a rung for 3$M here would be silently dropped, because `covered` is
built most-specific-first and ties break on file order, and every new context
is appended at the end.  A 4$M rung was also cut for the same reason: it would
have been unreachable behind `orev_raise_3$M`'s priority 66 at fit 1.00, and
the file already carries three dead rules of that kind.  What the context adds
is the one call that context never had — the pass.

**Bonus:** `responder_over_reverse_raise` closes a force that already existed
and that nobody reported.  Verified: `1C-1H-2D-2H-3H-P-?` returned only the
generic contexts and `uc_nt3` bid **3NT** at fit 1.000.

**Motivating board:** 506 (B part 6).  `P 1C P 1S P 2H P` → **2S**
`rrevh_min_2S` 1.000/67 (was `uc_pass` 1.000/18); the same hand without a
five-card suit → **3C** `rrevh_floor_3C` 1.000/40.

---

## Item 5 — responder's invitational jump rebid has no answering seat

`r1d1h2c_3H` and `r1d2c_3S` establish `forcing: invitational`; at opener's seat
`context_at` returned only the two generic contexts and `uc_pass` fit **1.000**
at priority 18.  Two cold games passed out at the three level.

**(a) The seat that hears it.**  `opener_over_responder_jump_rebid`, four
pairs: `1D-1H-2C`, `1D-1S-2C`, `1H-1S-2C`, `1H-1S-2D`.
`orjr_game_$K` 4M @54 (a doubleton and extras, or three-card support and any
opening) > `orjr_3NT_$K` @52 (0-1 in the long suit, 14+, semi-balanced) >
`orjr_pass_$K` P @44 `requires: {}`.
It takes `uc_pass` (18), `uc_rebid_C4`/`uc_rebid_D4` (29) and `uc_raise_H4`
(32) in this seat: passing a live invitation is not "nothing further to show",
and inventing a fourth suit at the four level is worse than answering the
question asked.  Because the context defines P, 3NT and 4M here it deletes the
code fallback for those three calls — the `requires: {}` pass is what makes
that safe.

**Two reviewer pairs cut.**  Expert B included `{ o: C, R: 1H, B: 2D }` and
`{ o: C, R: 1S, B: 2D }`.  Those are **reverses** (17-21).  A `requires: {}`
pass floor at opener's seat opposite a reverse is a bug, not a floor, and the
3M call it would answer is not authored on the responder side anyway.

**(b) The tier above the invitation**, so 14+ never has to ask a question whose
answer it knows: `r1d1h2c_4H` and `r1d2c_4S` at **60**, one point above the
existing 3M jump at 59.  With six cards and game values, bidding the game is a
better description than a jump partner may pass.  Untouched below:
`r1d2c_3NT` (57), `_2NT` (56), `_2S` (55), `_2D` (54), `_pass` (50); above,
`fsf_2H` (65) still wins with slam interest, which is right.

**(c) The jump rebid `responder_rebid_1H_1S_2C` / `_2D` never had.**  Those
contexts could only offer a to-play 2S (6-10) or 3NT with a six-card spade suit
and 11+.  Added `rr1H1SC_3S` / `rr1H1SD_3S` @57.5 (11-13, invitational) and
`rr1H1SC_4S` / `rr1H1SD_4S` @58 (14-18, sign-off), both gated `H: [0, 2]` so
they are disjoint from `rr1H1SC_3H` (62, 4+ hearts) and `rr1H1SC_4H` (63, 3+
hearts).  Half (a) then has something to answer in those two auctions too.

**Motivating boards:** 132 and 563 (B part 4).  132: opener → **P**
`orjr_pass_DHC` on a 12-count with a stiff heart (correct — B reported the
same, and noted that on 563 it is half (b) that pays).  563: responder →
**4S** `r1d2c_4S` 1.000/60, replacing the passed-out 3S.

---

## Item 6 — four more unauthored constructive seats

| seat | context(s) | what it displaces |
|---|---|---|
| `1M - 1NT - 2M` | `opener_over_1NT_rebid_to_play` (+ the explicit `1H-1S` twin) | `uc_nt2` (28) bidding 2NT over a sign-off, -300 |
| `1m - 1M - 2m - 2M` | `opener_over_minor_rebid_preference` | `uc_raise_S3` (31) raising a sign-off |
| `1m - (act) - 2m` | `opener_over_competitive_minor_raise` | `uc_nt2` (28) again, -300 |
| `2M - 3M` (competitive) | `answer_raise_invitation` | `uc_raise_H4` (32) accepting every invitation on 11 support points |

Each raise rung is itself an invitation, so each ships its own answering
context — `responder_over_1NT_rebid_raise` (+ the `1H-1S` twin) and
`responder_over_minor_rebid_raise`, both 4M-accept @50 over a `requires: {}`
pass @44.  Expert B flagged both as owed and shipped neither.

**`opener_over_competitive_minor_raise` deliberately does not define 2NT.**
`uc_nt2` is still offered; it simply loses to a fit-1.00 pass at 44 instead of
winning by default.  That is the smallest possible subtraction.  Its 3NT rung
was widened from B's `hcp: [18, 21]` to `[18, 40]`: an upper bound there is the
band-hole species this round exists to remove — a 22-count fell straight
through to the pass floor.  Verified.

**`answer_raise_invitation` — the specificity decision.**  Pattern
`"... - 1$M - P - 2$M - P - 3$M - P - ?"`, specificity **8**: above every
generic context (`general_uncontested_continuation` and
`general_competitive_low/high` are all 3) and below every anchored one, so
`responder_over_game_try` (1007) still owns the uncontested `1M-2M-3M` game
try — verified unchanged.  Both rungs carry
`when: { partner_last_suit: $M }`.  Expert B reported the two prototypes that
made both guards necessary: a five-token `"... - 2$M - P - 3$M - P - ?"` with
no `when` took 4M and P in auctions where the *opponents* bid 2M and 3M
(board 385 went 4S → 3NT, board 389 went P → 4NT in a 2C auction).

**Cut: the minor twin** of `answer_raise_invitation`
(`"... - 1$m - P - 2$m - P - 3$m - P - ?"`).  Five of a minor is not the right
accept and 3NT needs stoppers this shape cannot promise; it is a different
agreement and does not belong in a floor-shaped context.

**Motivating boards:** 300, 151, 508, 4 (all B part 5).  All four now decide
on the new floor: `o2ms_pass_1H1S`, `omrp_pass_CS`, `ocmr_pass_C`,
`ari_decline_H`, each at fit 1.000 / 44.

---

## What was cut, in one list

| cut | why |
|---|---|
| `*` token in `overcaller_over_cue_raise` | ties with `advance_cue_doubled` at 1006 and loses on file order, taking the floor with it |
| A 4NT rung in every cue-raise context | the file has one audited RKC floor (`rkc_4NT`, 45); a second would repeat the defect DECISIONS records |
| B's two illegal second-suit entries after a weak two | 3D over 3H and 3H over 3S are not legal calls |
| The minor raise `4C`/`4D` after a weak two | past 3NT, on a hand that has already shown everything |
| B's duplicate-pattern weak-two contexts | two concrete contexts with the same pattern |
| A forcing 8+ reading of the reverse preference | its answering seat's floor is a pass — the defect being fixed |
| `3$M` and `4$M` in `opener_over_reverse_2M_weak` | already owned by `opener_raise_after_reverse`; a rung there is silently dropped or dead |
| The two reverse pairs in `opener_over_responder_jump_rebid` | a `requires: {}` pass opposite a 17-21 reverse is a bug |
| `nx3_cue`, `advbal_*_cue`, `aw2*_cue` answering contexts | not starved: `opener_over_nx3_cue` and the `gf_landing_*` family already answer them |
| The minor twin of `answer_raise_invitation` | 5m is the wrong accept; a different agreement |
| A `establishes: agreed_suit` on any jump shift | Expert B part 1's explicit warning (prototype reached 6S on a 6-0 fit) — no rung in this batch does it |

---

## Trace list for the implementer

Run each with `repro.rank` + `sweep.deciding_rule` against the patched file.
All were run before this spec was written and all pass.

```
559  P 1H 1S 2S P            9.AKT732.AQT87.6  -> 4C   cra1_splinter_4C      1.000/62
945  1D P 1S P 2C P 2H P     72.J.KJT95.AK742  -> 3C   fsfr_extra_C3_2H      1.000/62
289  P 2D P 2S P             KQ8642.4.KJ73.62  -> 3S   w2a_raise_DS          1.000/60
289  P 2D P 2S P 3D P        AJ953.KQT85.4.A7  -> 3H   w2r_second_H_DS       1.000/56
506  P 1C P 1S P 2H P        QJ9753.73.J973.9  -> 2S   rrevh_min_2S          1.000/67
506' P 1C P 1S P 2H P        QJ97.73.J973.964  -> 3C   rrevh_floor_3C        1.000/40
132  1D P 1H P 2C P 3H P     98.6.AQJT7.AJ983  -> P    orjr_pass_DHC         1.000/44
563  1D P 1S P 2C P          AK8743.KT7.A86.4  -> 4S   r1d2c_4S              1.000/60
300  1H P 1S P 1NT P 2S P    85.K9765.A96.KQ6  -> P    o2ms_pass_1H1S        1.000/44
151  P 1C P 1S P 2C P 2S P   KJ2.8.A98.AJ9874  -> P    omrp_pass_CS          1.000/44
508  P P 1C 1D 2C P          T764.KQJT.AQ.963  -> P    ocmr_pass_C           1.000/44
4    P 1C 1D 1H P 2H P 3H P  A87.KT92.Q65.A72  -> P    ari_decline_H         1.000/44
```

Regressions that must NOT move: `rrevh_2S` / `rrevh_2NT` / `rrevh_3NT` on 8+
hands; `rgt_accept` on `1H-2H-3H`; `uc_pass` on the plain weak-two raise;
`feat_D_S` on the feature ask; `fsfr_2NT_$F` with a stopper and
`fsfr_raise_$F` with three-card support; `orev_raise_3H` on `1C-1H-2D-2H`;
`advcueX_XX` on the doubled cue.  All verified unchanged.
