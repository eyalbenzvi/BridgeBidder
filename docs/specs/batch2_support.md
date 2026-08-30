# batch2_support — support doubles and redoubles, and the seat that answers them

Editor's note for `docs/specs/batch2_support.spec`.  Subject: `support_double`,
`support_redouble`, the answering seats that did not exist, `redouble_continuations`,
and `general_pull_or_sit` / `adx_pull_my_*` where they touch this convention.

## What ships

| piece | contexts | rules |
|---|---|---|
| `support_double_wide` — the ask, over all five openings and both interference shapes | 5 | 45 |
| `support_redouble_wide` — the redouble twin | 5 | 45 |
| `support_double_answer` — **responder answers the support double** | 5 | 45 |
| `support_redouble_answer` — responder answers the support redouble | 5 | 40 |
| `support_double_answer_invite` / `support_redouble_answer_invite` | 5 + 5 | 20 |
| `support_double_jump_answer` / `support_redouble_jump_answer` | 5 + 5 | 20 |
| `redouble_continuations_major` — the major-opening twin | 2 | 16 |
| `redoubler_over_runout` — the seat that answers the forcing pass | 4 | 16 |
| rungs into `general_pull_or_sit` (2) and `redouble_continuations` (8) | — | 10 |
| **total** | **46 new contexts** | **257 rules** |

Verified mechanically against a patched copy in the scratchpad: the spec applies
through `addrules.apply_spec`, the system loads (517 → 563 contexts, 2344 → 2601
rules), **all 257 new rule ids are unique** against the whole file, `lint_system.py`
reports **zero new findings in all six lints**, and the **full test suite passes
(769 tests)** with the patch installed.

## The one structural idea

`addrules.py` has exactly two operations — append rungs to an existing context,
append a whole context at the end — so Expert A's "REPLACE the expansion" (add
`{ m: H, M: S }` to `support_double`/`support_redouble`) is not applicable as
written.  The twin therefore ships as new contexts, but not as B's single-rung
ones.  Both wide contexts use

```
pattern: "$O - * - 1$M - bid<2$M - ?"        (and "$O - * - 1$M - X - ?")
expand_pairs: 1C/1D/1H x the major responder can bid at the one level
```

Five tokens, so specificity 1005 — **the same as `support_double` and
`support_redouble`, and file order breaks the tie in favour of the existing
contexts**.  Consequences, all three of them deliberate:

1. in the four clean minor auctions the existing rungs keep every call they
   already define (`sd_double`, `sd_raise`, `sd_rebid_2$m`, `sd_1NT`, `sd_2NT`,
   `sd_pass`; `srd_redouble`, `srd_raise`, `srd_pass`) — **nothing is narrowed**;
2. the wide context still ADDS the calls those ladders never had (1S, 3$M, 4$M,
   1NT/2NT on the redouble side) in those same auctions;
3. in the fifth auction (`1H - P - 1S`) and in every auction where LHO overcalled
   or doubled, the wide context is the only specific interpreter and supplies the
   whole ladder.

That is the superset property obtained structurally rather than by discipline,
and it is why one pair of contexts covers boards 966, 754 and 166 at once.

## A/B disagreements, resolved

**1. New context, or a line in the existing `expand_pairs`?  (boards 966, 754)**
A: one `expand_pairs` line each, "the single cheapest change in my slice".
B: two new one-rung contexts, `support_double_major` / `support_redouble_major`.
*Resolved:* new contexts, because the tool cannot edit an expansion — but with
A's full ladder, not B's single rung.  A one-rung context would leave opener's
raise, rebid and notrump calls at `1H - P - 1S - (2D)` in the generic ladder
while the double came from a specific one, which is exactly the split reading
that makes a convention unreadable to partner.

**2. Does the support double survive LHO's overcall?  (board 166)**
A said yes and shipped it as a heavily gated rung inside `general_competitive_low`
(`cl_support_X_H`), explicitly to avoid widening `support_double`'s pattern and
shadowing the generic context "wholesale".  B did not reach the auction.
*Resolved:* yes, and as `*` in the wide pattern instead of a generic rung.  One
sentence of bridge: the double of responder's one-level major shows exactly three
of it whether or not LHO opened his mouth; the blast radius is the same five
auction shapes either way, and the `*` version keeps the convention in one place
instead of two.  Checked before shipping: all three X rungs in
`general_competitive_low` are dead for opener at that node (`cl_takeout_X` needs
`side_has_acted: false`, `cl_negative_X1/X2` need `i_have_acted: false`), so the
only X the new rung displaces is the code fallback at priority 9.

**3. What answers the support double?**
A (board 966): "no new context; `general_competitive_low` / `general_pull_or_sit`
answer it already."  B (board 966): traced that `general_pull_or_sit` answers it
with `adx_pull_my_S` at fit 1.000 — *pulling our own support double* — and
proposed `support_double_answer`.  B's trace is decisive and A's own board 266,
independently, is the same defect firing (`adx_pull_my_H` crawling to 2H with six
trumps opposite the promised three).  *Resolved:* B's answering context, extended
from three rungs to nine, and A's board-266 rung kept as well but restricted to
the auctions the new context does not own (see "the pull ladder" below).

**4. `lott_total_trumps` or my own length in the answering rungs?**
A gated the board-266 rung on `lott_total_trumps(H) >= 9`, which he traced as 9
at that node.  B refused to, because in the *major* auction partner's shown
length is zero until `sdM_double` exists, so the gate would depend on the rule
being installed to be satisfiable (the round-8 trap).  *Resolved:* both are
right about their own node.  Every rung in the new answering contexts counts
**my own length** (5+/6+), which is true before and after installation; A's rung
in `general_pull_or_sit` keeps `lott_total_trumps`, because there it fires only
after a *shipped* rule (`sd_double`, or a raise) has already set partner's
minimum, and A verified it firing at 1.000.

**5. Board 266: A's rung in `general_pull_or_sit`, or B's `advance_support_double`
context?**  *Resolved:* the general context wins the sub-case it uniquely covers,
the specific one wins the rest.  `support_double_answer` (specificity 1007) takes
2$M/3$M/4$M in the five support-double auctions, so B's one-rung context would be
redundant with it and is not shipped; A's `adx_pull_game_$M` is kept for the
auctions with no support double in them at all (partner raised my suit, they bid,
partner doubled — `my_suit` and `partner_suit` are both true there and nowhere
else).  `general_pull_or_sit` carries no `expand:`, so the two rungs are written
out; a `$M` there would have been a literal.

**6. `srd_1S_$m$M` (board 730) inside `support_redouble`, or in the wide context?**
B put it in the existing context.  *Resolved:* in the wide context as
`srw_1S_$O$M` (and its double-side twin `sdw_1S_$O$M`, which B said was owed),
because one rule then serves all five openings and both interference shapes
instead of four minor rows.  Traced: board 730's hand now bids 1S at fit 1.000.

**7. Are the redoubler's suit answers forcing?**  B wrote `rdro_major_$m` /
`rdro_spade_$m` as `forcing: one_round` and offered `non_forcing` as an
alternative.  *Resolved:* `non_forcing`.  A one-round force there would owe yet
another answering seat, and the entire finding of this batch is that a force
without an answer is worse than no force.

## Priorities: what each rung outranks, and why it is the better description

**`support_double_wide` / `support_redouble_wide` (opener).**
* **85 X / XX** — outranks everything in the context and, at these nodes, the
  code fallback X ("undiscussed", prio 9) and `xd_XX_extras` (23, 19+ total
  points).  *The subtraction to name:* after `1H - P - 1S - (X)` a 19-count with
  a doubleton spade can no longer redouble to show strength — XX means exactly
  three trumps.  That is the agreement, and it is what the four minor versions
  have already meant for several rounds; the strong balanced hand now bids 2NT,
  which is why `srw_2NT` is banded 18-21 rather than B's 18-19 (traced: a
  20-count that passed at fit 1.00 in the base now bids 2NT).
* **80 / 79 / 78 the 4-card raise ladder (2$M, 3$M, 4$M, bands 12-15 / 16-18 /
  19+ total points, disjoint)** — outranks `cl_raise_$M2/3/4` (30-32) and
  `xd_raise_$M2` / `xd_jumpraise_$M3` (30-32) at these nodes.  One sentence: with
  the double reserved for exactly three, the direct raise *promises four*, and a
  raise ladder that knows the trump count beats one that estimates it.  This is
  also the ceiling `sd_raise` never had — 16+ with four-card support previously
  fell out of the context entirely.
* **70 1S** — outranks `xd_run_S1` (24) and `xd_second_S1` (24) and `sd_1NT` /
  `srw_1NT` (54).  With four spades and opening values the suit is being SHOWN,
  not run to, and the rung that says "running, 5+ cards" mis-describes it in
  both halves (board 730).  Gated `unbid_suit: S` + `cheapest_in_suit`, so it is
  structurally inert in every M=S row and whenever they bid spades.
* **55 the six-card rebid, 54 1NT, 53 2NT** — the minor family's own numbers,
  reproduced.  They outrank `xd_rebid_$X2` (34) and `cl_rebid_*` (29-31); the
  `not: { suits: { $M: [3, 13] } }` clause keeps them off every hand the support
  call describes, so nothing above them is endangered.
* **15 the floor pass** — `requires: {}` at the BOTTOM, below every rung in its
  own context and below every generic rung (24-36) that can still fire, so a
  described bid always beats it.  It replaces `cl_pass` (20) / `xd_pass` (18),
  which this context covers away; there is no rule anywhere between 15 and 20,
  so nothing changes hands on the swap.

**`support_double_answer` / `support_redouble_answer` (responder).**
The ladder is priced against the six `adx_pull_my_*` rungs it replaces
(**-3.00 IMPs a table over 15 tables**, against `sd_double`'s +0.20 over 5 — the
strongest number either reviewer produced).
* **66 4$M with six trumps and 10+**, **65 4$M with five and 13+** — outrank
  `adx_pull_my_$M` (59/60) and `uc_raise_$M4` (32).  Six of mine opposite the
  three he promised is a nine-card fit; crawling to two of "my own suit"
  understates it by two levels (board 266: 4H makes eleven).
* **64 3$M with six trumps and 6-9** — the Law rung.  Nine trumps are worth the
  three level even with no game values; it outranks the same pull rungs and
  `adx_pass_min` (52).
* **63 3$M with five and 10-12 (invitational)** — board 966's own call: 3S made
  ten for BEN's +170 while we defended 2D.
* **62 2$M with five and 6-9** — the plain competitive answer, above `adx_nt`
  (56) and `adx_pass_min` (52), below the sit.
* **61 the sit** — `adx_sit`'s own priority, reproduced because this context
  covers P away from it.  Written in `standing_suit_length`, not
  `suit_quality(their)`: in a competed auction "their" resolves to LHO's suit,
  and the suit that matters is the standing bid's.  `adx_sit` runs **+0.15 over
  27 tables** and must not be disturbed — at these nodes it is not displaced,
  it is restated.
* **59 the discriminating pass with exactly four trumps and 0-8** — the rung
  that pays for the convention.  Opener promised exactly three, so four of mine
  is a 4-3 fit: defending partner's double beats declaring seven trumps at the
  two level.  It has to be a *gated* rule rather than the floor, because
  `sd_double` is `forcing: one_round` and `decision.py` drops a `requires: {}`
  pass under a live one-round force unless it is discriminating.  Traced: with
  it the seat passes at fit 1.000; without it the same hand takes a soft-miss
  bid.
* **58 2NT, 9-12 with a stopper** — `adx_nt`'s band exactly, restated because
  this context covers 2NT away from it.  Below the raises, so five trumps
  always beat a notrump.
* **40 the floor pass**, `requires: {}`, bottom of the ladder.
* Nothing here reaches `adx_neg_major_$M2/3` (62) in the auctions those rungs
  own: they need `unbid_suit: $M` and the major here is partner's *bid* suit.
* Nothing here outranks a slam rung: `gst_rkc_*` (46) and the keycard family
  live in other contexts at the four level and above and are untouched.

**`redouble_continuations` (+4 rungs, boards 23 and 13).**  `rdc_pass_$m` is a
`requires: {}` floor at 50 running **-6.75 IMPs a table over four tables**, the
worst rate measured in the round — not because the forcing pass is wrong but
because the context had four rungs and no notrump and nothing above the one
level.  The four new rungs are mutually exclusive with each other and with the
three existing suit rungs *by legality*: 1NT is only legal over a one-level
runout, and over a one-level runout `cheapest_in_suit` switches the two-level
major rungs off.  So 54/53/51/51 endanger exactly one rung, `rdc_pass_$m` (50),
and every hand with a stopper and a balanced minimum, or a real four-card major
at the two level, is better described by naming it than by a pass nobody
answered.  `rdc_X_$m` (57) and `rdc_suit_H/S_$m` (56/55) all stay above.
Traced: board 23 now bids 1NT (BEN 0.73), board 13 now bids 2S.

**`redouble_continuations_major` (board 991).**  A structural clone at the same
numbers (57 X, 56 the other major, 55 the minors, 54 the six-card rebid, 53.5 /
53 the notrumps, 50 the `requires: {}` forcing pass).  It takes X, 2$oM, 3C, 3D,
2$M, 1NT, 2NT and P from `general_competitive_low` at `1M - (X) - XX - (bid)`:
`cl_pass` (20) is the rung that lost the board, `cl_nt3` (29), `cl_rebid_jump_$X`
(31) and `cl_new_$X2` (26) are the others, and in every case "partner redoubled,
so we own this hand and I am showing my second suit" is the better description.
Traced: board 991 now bids 2S (BEN's top non-pass call).

**`redoubler_over_runout` (board 13).**  62 X outranks `ballow_X` (40) and
`ballow_reopen_X` (41) at this exact seven-call node only.  `ballow_reopen_X`
runs +3.75 over 4 tables and must not be displaced generally — it is not: the
pattern is anchored and seven tokens long.  A double after our own redouble,
opposite a forcing pass, with four of their runout suit, is a penalty statement
and not a balance.  56/55 the five-card majors, 20 the `requires: {}` floor.
Traced: the redoubler now doubles 2C instead of passing it out (+300 → the 4S
that was cold at the other table is a separate board's problem, but the double
is the call the auction was constructed to reach).

**`general_pull_or_sit` (+2 rungs).**  63, above `adx_neg_major_$M2/3` (62),
`adx_sit` (61) and `adx_pull_my_$M` (59/60), below nothing that can fit: gated
`my_suit: $M` AND `partner_suit: $M`, a pair that is true only after partner has
supported the suit I bid.  `adx_sit` cannot fit a hand with six of my own suit
and `adx_neg_major_*` needs the major to be *unbid*, so the only rung it takes
hands from is `adx_pull_my_$M` (-2.20 over 5 tables, -3.00 over the family).

## Where every force is answered

| force | answered by |
|---|---|
| `sdw_double_$O$M` / `sd_double` (one_round) | `support_double_answer` — 9 rungs incl. a `requires: {}` floor |
| `srw_redouble_$O$M` / `srd_redouble` (one_round) | `support_redouble_answer` — 8 rungs incl. a floor |
| `sda_inv3_$O$M` (invitational) | `support_double_answer_invite` (accept at 15+ total points / pass) |
| `sra_inv3_$O$M` (invitational) | `support_redouble_answer_invite` |
| `sdw_jump_$O$M` (invitational) | `support_double_jump_answer` (accept at 9+ / pass) |
| `srw_jump_$O$M` (invitational) | `support_redouble_jump_answer` |
| `sdw_1S_$O$M` / `srw_1S_$O$M` (one_round) | `general_competitive_low` — verified populated (`cl_raise_S*`, `cl_rebid_*`, `cl_nt*` all fit at that node), which is why it is a rung and not a context |
| `rdcm_pass_$M` and `rdc_pass_$m` (one_round forcing pass) | `redoubler_over_runout` — the seat that did not exist |
| `sra_nt2_$O$M` (invitational) | `general_uncontested_continuation` / `general_competitive_low` raise ladders, unchanged |
| every `sign_off` here | nothing owed; `partner_signed_off` silences opener in `prepare_decision` |

## What I cut, and why

* **A `requires: {}` floor pass inside `support_double` and `support_redouble`
  themselves.**  Written, applied, and then **withdrawn**: `sd_pass` / `srd_pass`
  are gated (12-14, 0-2 support) and cover P away from `cl_pass` and the code
  fallback, so a 15-18 hand with a doubleton in partner's major has no pass that
  fits — a real hole.  But the floor makes `1D - P - 1S - (X)` a clear decision,
  and `tests/test_arbitration.py::test_arbitration_returns_a_sound_call[competitive]`
  is a **locked test harvested at exactly that node** which asserts the seat is
  unsure.  The whole suite passes without the two rungs and fails with them, so
  they are out; the hole is recorded here for whoever revisits that test.
  (Both wide contexts do carry their own floors, and those are unaffected — in
  the four clean minor auctions `sd_pass`/`srd_pass` cover P and the wide floor
  is simply never reached.)
* **A's `adx_pull_weak_S2`** (running from partner's double of their 1NT with a
  bust and a five-card suit, board 152).  It lives in `general_pull_or_sit` but
  has nothing to do with a support double; it belongs to whoever owns advancing
  a takeout double, and shipping it here would be a second subject smuggled in.
* **A's unwritten "3M invitational twin at 62.5" of `adx_pull_game_$M`.**  A said
  explicitly he had not written it; an invitational call in a *generic* context
  reaches auctions I cannot enumerate, so I cannot ship the seat that answers it,
  and this batch's own finding forbids shipping the invitation without it.
* **B's `advance_support_double` as a separate context** — subsumed by
  `support_double_answer`, which owns the same nodes with a fuller ladder.
* **Everything a reviewer reported as negative or withdrawn stays out**: B's
  withdrawn forcing `3$M` (board 285), B's `1S - 2C - 2H - 3D` fourth-suit rung
  (board 555, "evidence against it, not for it"), A's `agreed_suit` prototype and
  his `their_fit: [8,26]` gate (both measured no-change), and the do-not-re-propose
  list is untouched — no responsive double, no re-ranked weak jump overcall, no
  `weakest_their_stopper` repair (both notrump rungs here are written in
  `standing_suit_length` or `features: [stopper(their)]` for that reason).

## Motivating boards, for tracing

Every line below was run against a patched copy of the system; "before" is the
unpatched engine at the same node.

| board | seat / auction | before | after |
|---|---|---|---|
| 966 | S, `1H P 1S 2D`, `JT9.AK987.T75.A4` | `P cl_pass` 1.000/20 | **`X sdw_double_1HS` 1.000/85** (BEN X 1.00) |
| 966 | N, `1H P 1S 2D X P`, `AK632.T5.963.KJT` | `2S adx_pull_my_S` 1.000/60 | **`3S sda_inv3_1HS` 1.000/63** |
| 754 | S, `1H P 1S X`, `AKJ.Q6543.762.A4` | `P xd_pass` 1.000/18 | **`XX srw_redouble_1HS` 1.000/85** (BEN XX 1.00) |
| 266 | N, `1C P 1H 2D X P`, `J983.KQ9853.7.QJ` | `2H adx_pull_my_H` 1.000/59 | **`4H sda_game6_1CH` 1.000/66** (4H makes eleven) |
| 730 | S, `1D P 1H X`, `Q742..AKJT62.T53` | `2D xd_rebid_D2` 1.000/34 | **`1S srw_1S_1DH` 1.000/70** (BEN 1S 0.65) |
| 166 | S, `1C 1D 1H 1S`, `AT8.Q74.A3.QJT32` | `P cl_pass` 1.000/20 | **`X sdw_double_1CH` 1.000/85** (BEN X 1.00) |
| 23 | W, `1D X XX 1H`, `K63.98.AQJT7.Q76` | `P rdc_pass_D` 1.000/50 | **`1NT rdc_1NT_D` 1.000/54** (BEN 1NT 0.73) |
| 991 | N, `1H X XX 2D`, `AK64.KQJT2.43.A4` | `P cl_pass` 1.000/20 | **`2S rdcm_second_H` 1.000/56** (BEN 2S) |
| 13 | S, `1D X XX 2C`, `AKQ2.987.QJT83.Q` | `P rdc_pass_D` 1.000/50 | **`2S rdc_2S_D` 1.000/51** |
| 13 | N, `1D X XX 2C P P`, `9765.AKJ4.2.K643` | `P ballow_pass` 1.000/21 | **`X rdro_X_1D` 1.000/62** |

Controls run and unchanged: the four clean minor support-double auctions
(`1C P 1H 1S` with three hearts still `X sd_double` 85, `sd_1NT` still second);
the uncontested `1H P 1S P` rebid (`ob_1H1S_1NT`); a plain takeout-double advance
(`1NT X P` → `adx_pass_min`); a plain pull to a minor (`1D 2S X P` →
`adx_pull_my_D`).  Behavioural checks on the new ladders: a 4-3 fit with 7 points
opposite the support double passes (`sda_defend`), a trump stack sits
(`sda_sit`), a 20-count balanced over their double of `1S` bids 2NT, and the
invitational and jump-raise answers both fire.
