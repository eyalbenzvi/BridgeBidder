# Batch 1 — the generic competitive and balancing ladder

System-editor notes for `docs/specs/batch1_competitive.spec`.
Six existing contexts, **204 new rungs**, no new contexts, no template
variables.

| context | rungs | why it is first |
|---|---|---|
| `general_competitive_low` | 71 | 783 vacuous live decisions (`COVERAGE_R18`), `cl_pass` -0.81 over 707 tables |
| `general_competitive_high` | 36 | 592 vacuous; `ch_pass` **beaten by acting at +1.90 ± 0.66, n = 67, t = 2.9** (`CFR_R18`) |
| `general_balancing_low` | 36 | `ballow_pass` -0.72 over 270 tables |
| `general_balancing_high` | 36 | `balhigh_pass` -0.67 over 767 tables |
| `general_their_double` | 15 | 74 vacuous; `xd_pass` **-1.72 over 88 tables**, the worst pass in the file |
| `general_pull_or_sit` | 10 | `adx_neg_major_$M2` and `_$M3` carry identical gates, so the jump is dead |

## Mechanical constraint that shaped every rung

**None of these six contexts has an `expand:` block**, and adding one would
rewrite every existing rule id in the context. `addrules.py` inserts raw text,
so a `$M` in a rung landing here would never expand. **Every rung is therefore
written out per suit, by hand.** That is why one agreement is two or four
rules and why the batch is 204 rules from about sixty agreements.

A second consequence: a new `pattern: "... - ?"` context is useless here.
`general_competitive_low` is `"... - bid<3C - ?"` (specificity 3) against
`"... - ?"` (specificity 2), and `covered` is built most-specific-first, so a
context appended at the end cannot add a rung for any call the generic already
defines — and the generics define nearly every call. Hence: rungs into the
existing six, nothing else.

---

## Verification actually run

* The whole batch applied to a scratch copy: **517 contexts, 2,548 rules
  (2,344 + 204), loads clean.**
* **All 516 locked scenarios in `tests/data/*.yaml` pass**, against a baseline
  of 516/516. Three decisions moved and all three are inside their accepted
  sets: `r2_no_fallback_4NT_over_their_game` P→X,
  `r3_no_fallback_slam_raise` 5C→P, `ben_no_second_balancing_double` 3H→P.
  The first draft **broke two** locked scenarios and both were real bridge
  errors of mine — see "The two locked scenarios that corrected me" below.
* **53 of the 54 motivating seats** re-decide to the intended call, every one
  at fit 1.000. The one that does not is board 988 (see cuts).
* **Blast radius: 120 changed decisions in 2,606 of our calls over 250 boards
  (4.60%)**, spread over ~45 distinct rungs. **74 of the 120 displace a
  catch-all pass** — `ch_pass` 26, `cl_pass` 24, `balhigh_pass` 15,
  `ballow_pass` 9, `xd_pass` 3 — which is precisely the population
  `COVERAGE_R18` and `CFR_R18` name.
* **Zero cross-agreement priority ties**: no new rung shares a priority with an
  existing rung producing a *different* call in the same context. (Sibling
  rungs of the same agreement in different suits *do* share a priority; that is
  the file's own convention — `cl_raise_C3/D3/H3/S3` are all 31.)
* Vocabulary probed against the live engine before use: `their_bidders`
  returns 2.0, `shapes: ["4333"]` is near-sharp (1.00 vs 0.15 off-shape),
  `features: ["three_of_top5(X)"]` parses, `suit_length(partner)` resolves.
  `when: { agreed_suit: … }` is **not** a legal condition key (`Conditions`
  raises `ValueError`) and `partner_limited` is off-limits per Expert B — both
  appear in proposals and both were rewritten out.

---

## The central tension, and how it is resolved

`CFR_R18` says `ch_pass` **loses to acting** by +1.90 IMPs a seat.
Expert A part 6 says the file's most expensive habit is **bidding twice** and
asks for a family of discipline passes. These look contradictory and are not.

`ch_pass` is the **catch-all** — the seat where nothing describes the hand. The
CFR result says that on those hands the file lacks the vocabulary to act. The
discipline pass is a **narrow, described** pass for a hand that has already
been shown. They are different populations, and the batch treats them
differently:

* Every ACTION rung is priced to describe a hand the ladder could not name.
* Every PASS rung carries a **non-empty `requires` naming the described hand**,
  and is priced to outrank only the specific natural bid it replaces. None is
  `requires: {}`; none sits above the family it is meant to leave alone.
* No code fallback is deleted by any pass rung, because `P` is already covered
  in all six contexts.

In the 250-board blast-radius sample the ratio comes out 74 seats where a
catch-all pass becomes an action, against 21 where a natural bid becomes a
described pass. That is the shape the evidence asks for.

---

## The two locked scenarios that corrected me

Both are in `harvested.yaml` and both broke on the FIRST draft.

1. **`e12_law_four_level_both_sides_have_a_fit`** — `Q87652.7.A62.Q84` after
   `1H (1S) 2H`. Eleven combined trumps; the lock wants **4S**. My
   `cl_raise_pref_S2` (33.4) and `cl_raise_overcall_S` (33.2) both fitted 1.000
   and outranked `cl_raise_lott4_S` (32). That is the project's named worst
   mistake — a partscore raise outranking a more descriptive game raise.
   **Fix: `lott_total_trumps` capped at `[8, 9]` on both.** Ten or more trumps
   belongs to the Law rungs above; a limit raise is a nine-trump bid.
2. **`e12_law_four_level_needs_their_fit_too`** — `AQ9763.T6.K3.KT2` after
   `1C (1S) 2H`; the opponents have shown no fit (`their_fit` = 5) and the lock
   wants **P**. My `cl_raise_fit3_S` fired 3S on eleven trumps.
   **Fix: the same `[8, 9]` cap on `cl_raise_fit3_$X`.**

The cap is now a stated house rule of this batch: **a three-level raise rung is
banded at eight or nine combined trumps; ten or more is priced at the four
level or not at all.**

---

## A/B disagreements, resolved

Board numbers are the reviewers' own.

| # | disagreement | resolution | one sentence of bridge |
|---|---|---|---|
| 1 | **Board 597 / the three-level Law raise.** A (`ch_raise_lott3_S`): 3+ trumps, lott ≥ 9, 6+ points, priority 32 — *above* `ch_raise_$M3`. B (`ch_raise_law_S3`): lott exactly `[9,9]`, `partner_shown_max ≤ 10`, priority 30.6. | **B's gate, A's band, B's priority.** `ch_raise_lott3_$M`: 3+, `lott ≥ 9`, `partner_shown_max: [0, 11]`, 5+ points, **30.6**. | Ten trumps is more reason to bid, not less, so B's closed `[9,9]` is wrong; but the Law raise is a bid opposite a LIMITED partner, and pricing it below `ch_raise_$M3` (31) means it inherits the seat only when the values rung declines. |
| 2 | **Board 632 / the jump raise.** A part 1: 3+ support, 13+, lott ≥ 8, priority 31.5, *invitational*. A part 4: 4+ support, `cheapest_in_suit: false`, non-forcing. B: 3+ support, 10+, `rule_of_26 ≥ 22`, priority 30.5. | **A part 4's**, as `cl_raise_fit3_$X`, non-forcing, plus the `[8, 9]` trump cap. A part 1's and B's are **cut**. | `cheapest_in_suit: false` is what makes it a JUMP, which is the whole missing idea; three-card support at the three level is what `cl_raise_$X3` already does, and B's 10-12 band collides with it. |
| 3 | **Board 297 / raising the overcall.** A: 3+ support, `partner_shown_length ≥ 5`, 8-12, priority 34, four suits. B: 4+ support, 8-11, priority 33.5, majors only. | **Merged**: `cl_raise_overcall_$X`, four suits, **4+ support** (B's floor) **and** `partner_shown_length ≥ 5` (A's credential), 8-12, `lott [8,9]`, priority **33.2**. | Nine trumps in a suit partner has already named beats a double asking him to name another; four-card support is what makes the count nine, so both gates are load-bearing. |
| 4 | **Board 707 / the jump rebid of my doubled suit.** A (`xd_rebid_jump_$X`): 6+, 17+, `suit_quality ≥ 1.5`, `partner_has_acted: false`, priority 35. B (`xd_jump_own_$X`): 6+, 17+, `three_of_top5`, priority 34.5. | **B's id and credential, A's `when`**: `xd_jump_own_$X`, `three_of_top5`, `partner_has_acted: false`, **34.5**. | A suit you will play opposite a passing partner is defined by its top honours, not by a scalar quality score. |
| 5 | **Board 870 / six-five.** A (`ch_second_suit_65_$M`): explicit `my_suit`/`unbid_suit` pairs, 12+. B (`ch_new_65_$M4`): `longest_suit_length: [6,13]`, no `my_suit` gate, 13+. | **A's pairing, B's quality floor**: `ch_second65_$M`, `my_suit` + `unbid_suit`, 6-5 stated in `suits:`, 12+, `suit_quality ≥ 1.0`, 29.45. | Without `my_suit` the rung is not a SECOND suit at all and fires on a hand that has never bid. |
| 6 | **Board 390 / the balancer's own six-card suit at three.** A (`ballow_rebid_law3_$X`): 8+, `their_fit ≥ 8`. B (`ballow_rebid_own6_$X`): 9-15, `suit_quality ≥ 2.5`, `three_of_top5`. | **Both ship** — A at 29.4, B at 29.6, distinct priorities. | They are right in different auctions: B's owns the seat where my suit is the trick source; A's owns the seat where the opponents' known eight-card fit is the reason to compete. |
| 7 | **Board 0 / the balancer's own long suit.** A (`ballow_new_long7_$M`): 7+, quality 1.0, priority 42. B (`ballow_own_suit_first_$M`): 6+, 8-16, quality 2.0, priority 41.5 — which ties A part 5's five-card `ballow_balance_major_$M` at 41.5. | **A three-rung ladder by LENGTH**: 5-card major @41.4, good 6-card any suit @41.6, 7-card any suit @41.9 — all above `ballow_X` (40), none reaching `ballow_reopen_X` (41, disjoint on `side_has_acted`). | The longer the suit the less a takeout double describes the hand, so length is the right ordering variable and it removes the tie at a stroke. |
| 8 | **Board 384 / the jump answer to the negative double.** A: `unbid_suit`, 5+, 16+, priority 63, `forcing: invitational`. B: the same plus `standing_bid_level: [2,2]`. | **A's, made `non_forcing`, with `cheapest_in_suit: false` added.** | The doubler is already capped by his own negative double, so a pass IS a complete answer — writing it `invitational` would open a question in a seat this spec does not author. |
| 9 | **Board 306 / 455 / 388 / 241 — the four-level Law raise in a minor.** A part 1: lott ≥ 10, `their_fit ≥ 8`. A part 3: lott ≥ 9, `their_fit ≥ 8`. A part 6: lott ≥ 10, no `their_fit`, non-vul. A part 7: lott ≥ 9, `their_fit ≥ 9`, shortness. B part 3: lott ≥ 9, `their_fit ≥ 8`, priority 30.5. | **lott ≥ 9, `their_fit ≥ 7`, 6+ points, priority 31.9.** | See below — this one was decided by measurement, not by argument. |
| 10 | **Board 548 — two pass rungs on the same board.** A: `ch_pass_described` (balanced 14-17, no six-card suit). B: `ch_pass_limited_A` (`partner_shown_max ≤ 8`). | **Both ship**, at 29.6 and 27.6. | They describe different hands — "I have shown mine" and "partner has shown his" — and either can be the reason to stop. |
| 11 | **Board 230 / 78 — the balancer with a silent partner.** A (`ballow_pass_described`): 15-17 balanced, priority **34**. B (`ballow_pass_partner_silent`): 12-16, no seventh card, priority 29.5. | **Merged into B's**, band widened to 12-17, `partner_has_acted: false` kept. A's is **cut**. | 29.5 already outranks the `ballow_new_C3` that lost board 230, and A's 34 would have outranked every raise in the context for a hand that has a fit. |
| 12 | **Board 988 — the fourth bid.** A (`balhigh_pass_declined_$X`). B (`balhigh_rebid_hold`, using `when: { partner_limited: … }`). | **A's**; B's is cut because Expert B's own method note forbids `partner_limited`. | — |

### Disagreement 9 in full, because it cost the most

Both experts' four-level minor Law raise is gated on `their_fit`, and
`their_fit` does not read what either of them assumed. On the two boards A part
3 wrote the rung for — **306** (`2H`–`3H` by the opponents) and **455**
(`1S`–`2S`–`3S`) — `their_fit` comes back **7**, not 8, even though their fit is
in a major. A part 8's own agreement #2 says the same thing from the other
side: a 1m opening shows three and its raise four, so `their_fit` tops out at 7
whenever their fit is a minor.

So `their_fit ≥ 8` is close to unreachable and both boards stayed passes.
`their_fit ≥ 7` recovers boards 306, 455, 388 and 241, all at fit 1.000.

The gate cannot be dropped altogether: **B part 3's board 107 negative** is the
Law barrage with no opposing-fit test at all, and it turned -420 into -500.
There `their_fit` was **0** — the opponents had made a strong enquiry, not
found a fit — so `[7, 26]` still refuses it. Seven is the loosest value that
keeps B's brake working.

On the LEVEL: A part 3 wanted nine trumps to bid four. I first ruled "nine is
the three level, ten is the four level" and it cost boards 306 and 455. The
final ruling, and the reason it is right in a minor only: **nine trumps ours
plus a known eight theirs is seventeen total tricks, so someone makes at the
eight-nine split, and four of a minor is one step, not a game.** The existing
`*_raise_lott4_$M` (majors, lott ≥ 10) is untouched.

---

## Every new rung, priced against what is above AND below it

Notation: **↑** = the rung immediately above it that it must not reach,
**↓** = what it can legally outrank, with the reason.

### `general_competitive_low` — 71 rungs

| prio | rungs | ↑ it cannot reach | ↓ it outranks, and why |
|---|---|---|---|
| 36.5 | `cl_takeout_X_agreed` | `cl_nt2_direct` 37 | `cl_takeout_X` 36 — same call; shortness in the suit THEY agreed is a sharper reading than shortness in LHO's first suit |
| 36.4 | `cl_support_X_CH/CS/DH/DS` | 36.5 | `cl_takeout_X` 36, `cl_negative_X*` 33 — exactly three cards in partner's major is the most precise length statement the file has |
| 36.0 | `cl_reopen_X2` | 36.4 | `cl_negative_X*` 33 — but disjoint anyway: this needs `my_last_call_was_double: true`, they need `i_have_acted: false` |
| 35.2 | `cl_penalty_X_over_nt` | 36.0 | `cl_nt2` 28 (which lost board 119), `cl_negative_X*` 33 — disjoint by `standing_bid_strain: [NT]` |
| 34.8 | `cl_reopen_X` | `cl_doubler_game_$M` 35 (moved off the tie) | `cl_negative_X1` 33 (**+1.90, a winner**) — **structurally unreachable**: this rung carries `i_have_acted: true`, `cl_negative_X1/X2` carry `i_have_acted: false` |
| 33.5 | `cl_negative_X2_both` | `cl_doubler_raise_$X` 34 | `cl_negative_X2` 33 — same call; holding five of one major does not deny four of the other |
| 33.4 | `cl_raise_pref_$M2` | 33.5 | `cl_negative_X2` 33 (**-2.07, a loser**) — a known eight-card fit beats a responsive double that denies a fit. Level-gated `[2]`, so `cl_negative_X1` is out of reach |
| 33.2 | `cl_raise_overcall_$X` | 33.4 | **`cl_negative_X1` 33 — the one deliberate outranking of a profitable rule in this batch.** Gated to `partner_shown_length ≥ 5` (partner has OVERCALLED) and 4-card support, so it takes a narrow slice: nine trumps in a named suit. **Flagged for the implementer to screen separately if the batch moves the wrong way.** |
| 32.0 | *(nothing new)* | | |
| 31.9 | `cl_raise_lott4_$m` | `cl_raise_$M4` / `cl_raise_lott4_$M` / `cl_raise_lott3_$M` 32 | `cl_raise_$m3` 31, `cl_raise_$m4` 27 — the Law, priced on trumps rather than on `rule_of_26 ≥ 25` and "my longest suit", which is why 4C fitted 0.000-0.066 on four boards |
| 31.6 | `cl_raise_lott_short_$M` | 31.9 | `cl_raise_$M3` 31 — but it cannot fit there (that needs three trumps, this describes two). `longest_suit_length: [0,5]` keeps a six-card suit of my own on `cl_new_long3_*` / `cl_rebid_*` |
| 31.5 | `cl_raise_fit3_$X` | 31.6 | `cl_raise_$X3` 31, `cl_rebid_jump_$X` 31 (**+2.00, a winner** — disjoint: `partner_suit` vs `my_suit`) — 13+ support points is above `cl_raise_$X3`'s band and `cheapest_in_suit: false` makes it a jump the ladder never had |
| 31.4 | `cl_rebid_agreed_law3_$X` | 31.5 | `cl_raise_$X3` 31 — after partner AGREES my suit the count is known, so shape decides |
| 31.2 | `cl_rebid_game_$M` | 31.4 | `cl_rebid_jump_$M` 31 (**+2.00**) — **gated at SEVEN cards**, so it cannot reach that rule's six-card population; a four-loser one-suiter is a game bid, not an invitation |
| 30.9 | `cl_jumpadv_$M2` | `cl_raise_$X3` 31 (moved off the tie) | `cl_new_$M1` 30, `cl_new_$X2` 26 — the advance ladder was one rung wide |
| 30.6 | `cl_adv_$M1` | 30.9 | `cl_new_$M1` 30, `cl_new_C1/D1` 25 — partner's double promised support, so the four-card major needs no suit-quality toll and beats a longer minor |
| 30.5 | `cl_raise_lott3_$m` | `cl_raise_$X2` 30 is BELOW it | `cl_raise_$m2` 30. **`cl_raise_C3` 31 (+3.50, a winner) is ABOVE it and is never reached**: this rung is capped at 3-9 total points and five-card support, `cl_raise_C3` floors at 8 with `rule_of_26 ≥ 22` |
| 28.6 | `cl_free_major_$M2` | `cl_nt3` 29 | `cl_nt2` 28 — with a five-card major to show, notrump is the wrong strain |
| 28.5 | `cl_free_major3_over_nt_$M` | 28.6 | `cl_nt2` 28, `cl_new_$M3` 27/27.5 — over a two-suited notrump overcall they have located eleven cards, so our major fit needs no extra values |
| 28.4 / 28.3 | `cl_rebid5_two_$X` / `cl_rebid5_three_$X` | **`cl_nt3` 29 deliberately** — Expert A priced these below rather than repair `weakest_their_stopper` | `cl_new_*` 26-27.5, `cl_nt2` 28 (at 28.4 only) — `cl_rebid_$X2/3` demand six cards and a good five-card suit has nowhere to go |
| 27.7 | `cl_pass_sandwich_discipline` | `cl_nt2` 28 | `cl_new_$X3/_hi` 27/27.5, `cl_nt1` 27, `cl_new_$X2` 26 — both of them have bid and described and my side never acted; eleven points is not a three-level entry |
| 27.65 | `cl_minor_game_5$m` | 27.7 | `cl_raise_$m4` 27, `cl_new_$X3_hi` 27.5 — the ladder had no `cl_minor_game` at all |
| 27.6 | `cl_pass_vul_nofit` | 27.65 | the same 26-27.5 band — two boards (12, 255) for one rung, the strongest evidence in Expert A part 2 |
| 27.55 | `cl_pass_after_my_double` | 27.6 | `cl_new_$X3_hi` 27.5 and below. Sits **under** `cl_doubler_raise*` 33-34 and `cl_nt2/3` 28/29, all of which describe the hand better when they fit |
| 27.4 | `cl_new_long3_lim_$M` | 27.5 | `cl_new_$M3` 27, `cl_nt1` 27 — opposite a partner who has limited himself high the combined count is known, so length alone is the credential |
| 27.2 | `cl_new_void3_$X` | 27.4 | `cl_new_$X3` 27, `cl_new_long3_$X` 27 — a void is worth the level a fifth card is not |
| 26.8 | `cl_new_strong2_$X` | `cl_new_$X3` 27 | `cl_new_$X2_hi` 26.5, `cl_new_$X2` 26 — opposite a shown strong balanced hand the honour toll is paid twice |
| 26.75 | `cl_pass_misfit_$M` | 26.8 | `cl_new_$X2_hi` 26.5 and below — a singleton in partner's overcalled major is not a second contract |
| 26.7 | `cl_pass_silent_over_nt` | 26.75 | same band |
| 26.6 | `cl_new_twosuit_$M` | 26.7 | `cl_new_$M2_hi` 26.5, `cl_new_$M2` 26 — same call; 5-5 shape substitutes for the honour toll |
| 24.5 | `cl_new_values2_$X` | `cl_new_C1/D1` 25 | `cl_pass` 20 only — the bottom of the ladder, and the only thing it can ever take is the catch-all |

### `general_competitive_high` — 36 rungs

| prio | rungs | ↑ | ↓ and why |
|---|---|---|---|
| 39.0 | `ch_sac_X_trumps` | — (top of context) | `ch_penalty_X` 38 — same call; at the five and six level three trumps and two quick tricks is the credential, not 15 HCP |
| 37.0 | `ch_takeout_X_shape` | 38 | `ch_negative_X3` 33 (disjoint: `side_has_acted` false vs true) — **the takeout double of a preempt priced in SHAPE**, which is Expert A part 7's first agreement |
| 34.0 | `ch_takeout_X_acted` | 37.0 | `ch_raise_$M4` 32 and below — carries `oc1S_X`'s own "must not hide a five-card major" clause, which is the fix Expert A's whole-batch check forced |
| 32.2 | `ch_raise_over_jump_$M4` | — | `ch_raise_$M4` / `ch_raise_lott4_$M` / `ch_raise_lott_$M4` 32 — same call; they leapt to game to shut us out and nine trumps takes the push |
| 31.9 | `ch_raise_lott4_$m` | 32 | `ch_raise_$m3` 31, `ch_raise_$m4` 27 — the minor twin of `ch_raise_lott4_$M`, which had none |
| 31.6 | `ch_raise_preempt3_$X` | 31.9 | `ch_raise_$X3` 31, `ch_raise_$X2` 30, `ch_free_3$M` 30 — **all four `resp_preempt_*` contexts have no raise of partner's preempt whatsoever**; two trumps opposite a known six make eight |
| 31.5 | `ch_sell_out_$M` (P) | 31.6, and `ch_raise_$M4` 32 — a genuine ten-trump hand still bids game | `ch_raise_$M3` 31, `ch_free_3$M` 30 — eight trumps is eight tricks. `partner_shown_max ≤ 11` means it can never fire opposite an unlimited partner |
| 31.4 | `ch_compete_agreed3_$X` | 31.5 | `ch_raise_$X3` 31 — after a support double we know seven trumps exactly, and a fourth of my own is a competitive raise |
| 30.6 / 30.55 | `ch_raise_lott3_$M` / `ch_raise_lott3_$m` | **`ch_raise_$X3` 31 deliberately** | `ch_free_3$M` 30, `ch_raise_$X2` 30, `ch_nt3` 29 — the Law rung inherits only the hands the values rung declines |
| 30.5 | `ch_shape_game_$M` | 30.55 | `ch_free_3$M` 30, `ch_nt3` 29 — a six-card major and a singleton in their jumped suit is game on shape |
| 30.4 | `ch_pass_opposite_preempt` (P) | 30.5 | `ch_free_3$M` 30, `ch_new_$X3` 27-27.5 — a singleton in partner's preempted suit turns his plus into a minus |
| 30.2 | `ch_compete_agreed4_$m` | 30.4 | `ch_raise_$m3` 31 is above it and untouched; it outranks `ch_nt3` 29, `ch_new_$X4` 28 — `ch_raise_$m4` re-tests the fit from scratch and cannot reach the position where the minor is already agreed |
| 29.6 | `ch_pass_described` (P) | `ch_free_3$M` 30 | `ch_nt3` 29, `ch_rebid_$X*` 29, `ch_advance_x3/x4` 28.5, `ch_new_$X3_hi` 27.5 (**the rung that lost board 548**) |
| 29.5 / 29.45 | `ch_second_major_$M3` / `ch_second65_$M` | 29.6 | `ch_nt3` 29, `ch_rebid_$X4` 29 — a 4-4 major fit beats notrump on a doubleton stopper; six-five shows the five |
| 29.2 | `ch_rebid_shape_$X3` | 29.45 | `ch_rebid_$X3` 29, which demands `rule_of_26 ≥ 22` opposite a shown minimum that cannot reach it |
| 27.6 | `ch_pass_limited_A` (P) | `ch_advance_x3/x4_$X` 28.5, `ch_new_$X4` 28, `ch_nt2` 28 — all untouched | `ch_new_$X3/_hi` 27/27.5. **See "what was cut" for why the band is `[0, 8]` and not `[0, 11]`.** |

### `general_balancing_low` — 36 rungs

`ballow_reopen_X` measures **+3.75 over 4 tables**; `ballow_X` measures
**-2.91 over 11**. Every rung here either lowers the floor into the winner or
outranks the loser, and none reaches `ballow_reopen_X` — the two are disjoint
on `side_has_acted`.

| prio | rungs | ↓ and why |
|---|---|---|
| 42.0 | `ballow_pen_X` | `ballow_reopen_X/X2` 41 — same call; four of their trumps behind the bidder is a penalty double, not a takeout one |
| 41.9 / 41.6 / 41.4 | `ballow_own7_$X` / `ballow_own6_$X` / `ballow_balance_major_$M` | **`ballow_X` 40** (-2.91) and `ballow_new_*` 25-27 — a double promises three cards in every unbid suit; a one-suiter names its own trumps |
| 40.8 | `ballow_reopen_X_opener` | ties nothing; sits just below `ballow_reopen_X` 41 so the 16+ reading stays primary. Routes 13-15 opening hands INTO the +3.75 family |
| 40.5 | `ballow_reopen_X2_shape` | `ballow_X` 40 — a SECOND takeout double at the two level, 15-18 |
| 39.5 | `ballow_X_strong` | `ballow_X` 40 is ABOVE it; it outranks the raise/rebid band 26-33 — `ballow_X` has no 17+ branch, unlike every direct-seat takeout double |
| 39.0 | `ballow_reopen_X_shape` | same — 11-15 with three-plus in every unbid suit |
| 32.6 / 32.5 | `ballow_raise_brake_$M2` / `_$M3` | **`ballow_raise_$M4` and `ballow_raise_lott4_$M` 32** — the whole point: eight trumps and a 25-count that rests on partner's unshown maximum is a competitive raise, not a game bid. `lott_total_trumps: [7, 8]` keeps them off every ten-trump hand. **The two levels carry different priorities** so a decision is never handed to arbitration by a same-priority, different-call tie |
| 31.9 | `ballow_raise_lott4_$m` | `ballow_raise_$m3` 31, `ballow_raise_$m4` 27 |
| 30.6 / 30.55 | `ballow_raise_lott3_$M` / `_$m` | `ballow_nt2_strong` 30, `ballow_raise_$X2` 30 — **`ballow_raise_$X3` 31 is above and untouched** |
| 29.6 | `ballow_rebid_own6_$X` | `ballow_rebid_$X3` 29 (16+ points, a floor a balancing hand rarely has) |
| 29.5 | `ballow_pass_partner_silent` (P) | `ballow_rebid_$X*` 29, `ballow_nt2` 28, `ballow_new_$X3` 27 (**the rung that lost board 230**) |
| 29.4 | `ballow_rebid_law3_$X` | `ballow_rebid_$X3` 29 — the Law reading of the same call, one notch under the suit-quality reading |
| 27.5 | `ballow_major_first_$M` | `ballow_nt1` 27, `ballow_new_$M1` 25 — show the major before rebidding notrump |

### `general_balancing_high` — 36 rungs

| prio | rungs | ↓ and why |
|---|---|---|
| 42.0 | `balhigh_penalty_X` | `balhigh_reopen_X/X2` 41, `balhigh_X` 40 — this context had **no penalty double at all**; a trump stack outranks takeout |
| 41.5 | `balhigh_no_defence_pass` (P) | `balhigh_reopen_X/X2` 41, `balhigh_X` 40 — I have bid my hand and hold a void or singleton in their trumps, so a double now is made on no trump tricks. **Supersedes Expert A's board-761 rung, which is cut** |
| 39.0 | `balhigh_X_shape` | `balhigh_X` 40 is **above**, so the 14+ reading stays primary and this takes only 10-13. Outranks the raise band 27-32 |
| 33.0 | `balhigh_rebid_$M5` | `balhigh_raise_$M4` 32 — over their five-level preempt, a shortage in their suit and my own five-card major is a bid, not a defence |
| 32.5 | `balhigh_lott_push_$M` | `balhigh_raise_$M4`/`lott4_$M` 32 — same call; after my raise already showed the hand, ten ours against eight theirs means nobody sells out at three |
| 31.9 | `balhigh_raise_lott4_$m` | `balhigh_raise_$m3` 31, `balhigh_raise_$m4` 27 |
| 30.6 / 30.55 / 30.5 | `balhigh_raise_lott3_$M` / `_$m` / `balhigh_rebid_lott3_$M` | `balhigh_raise_$X2` 30, `balhigh_nt3`/`rebid_*` 29 — **`balhigh_raise_$X3` 31 is above and untouched** |
| 30.1 | `balhigh_pass_repeat_$X` (P) | `balhigh_rebid_$X4` 29, `balhigh_new_$X4` 28 — I have shown this suit and partner could not raise it |
| 30.05 | `balhigh_doubler_own_$X5` | `balhigh_raise_$X2` 30 sits at 30 and is not tied any more; outranks `balhigh_nt3` 29 and below |
| 29.6 / 29.55 | `balhigh_rebid_solo_$M4` (6+) / `balhigh_rebid_solo_$m4` (**7+**) | `balhigh_rebid_$X4` 29 (which needs `partner_has_acted: true` — disjoint) — a seven-card minor is a trump proposal; four of a minor is not a game, which is why the minors need the extra card |
| 29.5 | `balhigh_pass_declined_$X` (P) | `balhigh_rebid_solo_$M3` 29.05, `balhigh_new_$X3` 27 — **narrowed after the first draft blocked boards 226, 306 and 455**: it now requires `partner_suit: $X` and `suits: {$X: [5, 6]}` and 0-14 points, so it describes one hand instead of "pass at the three level" |
| 29.4 | `balhigh_pass_silent_partner` (P) | the 27-29.05 band. `longest_suit_length: [0, 5]` keeps it off the solo-rebid rungs, which is the direct A-vs-A conflict between boards 488 and 49/954 |
| 29.05 | `balhigh_rebid_solo_$M3` | `balhigh_new_$X3` 27 — 17+ opposite a silent partner |
| 28.5 | `balhigh_defend_their_nt` (P) | `balhigh_new_$X3` 27, `balhigh_nt1` 27 — do not run to the four level from their notrump with two quick tricks |
| 28.4 | `balhigh_pref_$m3` | `balhigh_new_$X3` 27 — returning to partner's minor with four-card support |

### `general_their_double` — 15 rungs

The starved context: `xd_pass` fires 88 times at **-1.72**, and **there is no
four-level raise of any kind**, so when partner preempts and they double, 4M is
reachable only through the code fallback at priority 12.

| prio | rungs | ↓ and why |
|---|---|---|
| 34.5 | `xd_jump_own_$X` | `xd_rebid_$X2/3` 34 — a jump to three on a self-sufficient six-card suit and 17+ says what a cheap rebid cannot |
| 33.0 | `xd_raise_lott4_$X` | `xd_jumpraise_$X3` 32, `xd_raise_$X3` 31, `xd_raise_$X2` 30. **Below `xd_rebid_$X2/3` 34** — my own six-card suit is a better description than a raise |
| 30.5 | `xd_pass_flat_$m` (P) | `xd_raise_$m2` 30 — **and it is below `xd_raise_$m3` 31, so a real raise is untouched**; three small trumps in a 4-3-3-3 only tells them how high to bid |
| 26.5 | `xd_pass_agreed_$X` (P) | `xd_second_$X3` 26, `xd_second_$X2` 25 — they doubled our agreed partscore; a minimum passes rather than running |
| 23.5 | `xd_nt_extras` | `xd_XX_extras` 23, `xd_pass` 18 — 18+ balanced bids the notrump game through their double |

### `general_pull_or_sit` — 10 rungs

| prio | rungs | ↓ and why |
|---|---|---|
| 63.0 | `adx_pull_game_$M` | `adx_neg_major_$M2/3` 62, `adx_sit` 61 — partner's double showed support for MY suit, so six opposite three is a nine-card fit |
| 62.8 | `adx_neg_major_jump_$M` | `adx_neg_major_$M2/$M3` 62 — those two carry **identical gates**, so the jump is dead; `cheapest_in_suit: false` and 5+ cards and 16+ is what discriminates it |
| 62.5 | `adx_sit_nt` (P) | `adx_neg_major_$M*` 62, `adx_pull_*` 53-60. **`adx_sit` cannot sit for a double of NOTRUMP** (it requires `their_last_bid_suit`), so this is the answering seat for `cl_penalty_X_over_nt`. **It is NOT `requires: {}`** — Expert A wrote it that way and it would have eaten the whole context; the 8+ point floor lets a bust still run |
| 61.5 | `adx_sit_four` (P) | `adx_pull_my_*` 58.5-60, `adx_pull_*` 54-58 — `adx_sit` (61) demands a QUALITY holding, so four small trumps behind a one-level opener, the commonest penalty pass there is, scored 0.33 |
| 58.6 | `adx_pull_major_$M3` | `adx_pull_S3/H3` 58/57 and `adx_pull_C4/D4` 54 — `adx_pull_S3` compares raw suit lengths, so a four-card major loses to a five-card minor one level higher |
| 53.0 | `adx_pull_weak_$M2` | `adx_pass_min` 52 — running from partner's double of their notrump with a bust; **priced below `adx_sit_nt` 62.5 on purpose**, so the two resolve by strength and not by luck |

---

## Where every force, ask and invitation is answered

Only four rungs in the batch are anything other than `non_forcing` or
`sign_off`, and every one of them lands in a seat that already has rungs.

| new rung | forcing | answering seat | status |
|---|---|---|---|
| `cl_jumpadv_$M2` | `invitational` | `general_uncontested_continuation` — `uc_doubler_raise3_$X` (17-19), `uc_doubler_game_$M` (20+), `uc_pass` | **TRACED**: `1C X P 2H P ?` with `AQ87.KQ4.K952.J6` returns P with the 2H read as 9-11 and both doubler rungs live in the candidate set |
| `cl_reopen_X`, `cl_reopen_X2`, `cl_takeout_X_agreed`, `cl_negative_X2_both`, `ch_takeout_X_shape`, `ch_takeout_X_acted`, `ballow_X_strong`, `ballow_reopen_X_*`, `balhigh_X_shape` | `one_round` | `general_pull_or_sit` (`... - X - ?`), fully rung with `adx_pull_*`, `adx_neg_major_*`, `adx_sit*`, `adx_nt`, `adx_pass_min` — and this batch adds six more rungs to it | authored |
| `cl_penalty_X_over_nt` | `non_forcing` (penalty) | **`adx_sit_nt`, shipped in this spec.** Expert A's first version of the penalty double LOST the board because opener pulled it to 2C at `uc_rebid_C2` fit 1.00 | shipped together |
| `adx_neg_major_jump_$M` | **downgraded to `non_forcing`** | none needed | see disagreement 8 |

No new question is asked anywhere in this spec that does not already have an
authored answer. The **generic cue-bid raise is deliberately absent** for
exactly this reason — see the cut list.

---

## What was cut, and why

### Cut because a reviewer measured it and said no

| proposal | source | reason |
|---|---|---|
| the generic `competitive_cue_raise` context | A part 4, board 632 | **Expert A's own negative.** The rung fires cleanly and the answering seat then bids 3NT with `T3` in clubs, because `uc_raise_D3` counts partner's shown minimum of three plus opener's four = 7 and scores 0.082. "Do not ship the cue raise until the *partner has agreed MY suit* ladder is authored." Round 17 priced an unanswered force at **-9.8 IMPs a seat** |
| `ballow_cue_try_$M` | B part 4, board 713 | Same species, plus two defects of its own: `call: 3S` is hard-coded while the `when` is `my_suit: $M`, so it would not template; and it is a `one_round` force with no answering seat |
| `ballow_reopen_X_long` | A part 4, board 713 | **Expert A's own negative**: it fires, and partner advances 3C into a 4-3 fit for -100 against the -50 we scored. "I am not shipping it off one board" |
| `cl_advance_x2_C`, `cl_advance_x3_C`, `cl_advance_xjump_C` (advances of a takeout double in a MINOR) | A part 2 board 695, A part 6 board 883 | **Expert A's own negative**, and the most valuable one in the corpus: a takeout double registers **three** suits as partner's suits with a shown minimum of three cards in the suit the opponents OPENED, so every `uc_raise_*` and `uc_minor_game_5$m` goes live in all of them and the advancer's third call is **5C or 5D**. "The agreement is right, the rung is VERIFIED to fire, and it MUST NOT SHIP on its own." The MAJOR advances (`cl_adv_$M1`, `cl_jumpadv_$M2`) **do** ship — they do not route into `uc_minor_game_5$m` |
| `ch_twosuiter_majors_H4` | A part 1, board 326 | Board 326 is one of Expert A part 1's three declared negative results |
| `adx_pull_dead_$M3` | A part 1, board 426 | Board 426 is another of the same three |
| the four-level Law raise **without** a `their_fit` gate | B part 3, board 107 | Measured: -420 becomes -500. The gate is kept at `[7, 26]` in every four-level Law rung in this batch |
| `ch_pass_limited_B` (`partner_shown_max ≤ 11`) | B part 6, board 433 | **Withdrawn by Expert B.** `ch_new_long3_D` runs **+4.33 over 3 tables**. Its narrow sibling `ch_pass_limited_A` (`≤ 8`) ships, because a weak two shows a maximum of ten and the `[0, 8]` band cannot reach the preempt-advance seats where `ch_new_long3_*` earns its money. **Confirmed empirically**: in the 250-board blast-radius run, `ch_pass_limited_A` never displaced any `ch_new_long3_*` rule |

### Cut because it accuses a rule that is profitable on the whole corpus

Expert A part 7's appendix ranks six subtractive proposals and marks three
**"measure alone — accuses a winner"**. All three are out of this batch:

* board 252's six-card-major re-rank, which takes from `cl_raise_C3`
  (**-0.78 / +3.50** over 9/6 tables) — `cl_major6_S3` **cut**;
* board 937's denial on `cl_negative_X1` (**+0.25 / +1.90** over 12/10) — no
  rung in this batch touches `cl_negative_X1`'s `requires`, and the two rungs
  that could have outranked it (`cl_reopen_X`, `cl_raise_pref_$M2`) are made
  structurally disjoint by `i_have_acted` and `standing_bid_level`;
* board 625's gate on `cl_rebid_jump_$M` (**+0.60 / +2.00** over 5/3) — the
  replacement rung `cl_rebid_game_$M` is gated at **seven** cards so it cannot
  reach the six-card population.

`cl_negative_X2_values` and `cl_negative_X2_strong` are also cut: they widen
`cl_negative_X2`, which measures **-2.07 over 15 tables**. Only
`cl_negative_X2_both` ships, because it says something the rule does not
(four-plus in *each* major).

**One deliberate exception, flagged:** `cl_raise_overcall_$X` at 33.2 does
outrank `cl_negative_X1` at 33 on the narrow slice where partner has
**overcalled** (`partner_shown_length ≥ 5`) and I hold four-card support.
Board 297 verifies the change (X → 2D). If the batch measures badly, this is
the first rung to pull.

### Cut as a duplicate or a merge

`cl_raise_jump_$M3`, `cl_fitjump_$M` (→ `cl_raise_fit3_$X`);
`cl_raise_$M2_over_overcall` (→ `cl_raise_pref_$M2`);
`cl_raise_advance_$M` (→ `cl_raise_overcall_$X`);
`cl_raise_lott_S3` (duplicates `cl_raise_$M3`'s own population);
`cl_raise_law_D3/D4`, `ch_raise_law_S3`, `ch_raise_lott3_S` (A part 6's
version) (→ the Law families at 30.55/30.6/31.9);
`xd_rebid_jump_$X` (→ `xd_jump_own_$X`);
`ch_second_suit_65_$M` (→ `ch_second65_$M`);
`ballow_new_long7_$M`, `ballow_own_suit_first_$M` (→ the `ballow_own7`/`own6`/
`balance_major` ladder);
`balhigh_partner_silent_pass` (Expert A: superseded by
`balhigh_no_defence_pass`);
`ballow_pass_described` (→ `ballow_pass_partner_silent`);
`ch_raise_agreed_$m4` (→ `ch_compete_agreed4_$m`);
`balhigh_raise_lott4_C/D` from board 455 (identical to board 306's).

### Cut on mechanics

| proposal | defect |
|---|---|
| `ch_compete_agreed_4$m` (B part 3) | `when: { agreed_suit: $m }` — **`agreed_suit` is not a legal condition key**; `Conditions.from_dict` raises `ValueError: Unknown condition keys`. Rewritten as `my_suit` + `partner_suit` |
| `balhigh_rebid_hold` (B part 4) | uses `when: { partner_limited: … }`, which Expert B's own method note forbids |
| `xd_run_jump_$m` (B part 6) | a no-op: `xd_run_$m3` at 26 already bids 3C/3D on a six-card suit with no point gate, so the new rung produces the same call from the same hands |
| `cl_new_free1_$X` (A part 4) | `establishes: { forcing: one_round }` on a new-suit rung in the most generic context in the file, with no answering seat shipped. This is the -9.8 failure mode by construction |
| `cl_pass_outgunned` (A part 6) | priority **34** on a pass gated only at `hcp: [0, 8]` and a 5-7 card suit: it would outrank `cl_negative_X*` (33) and every raise in the context. Its board is covered by `cl_pass_sandwich_discipline` |
| `cl_pass_live_auction` (A part 4) | third near-copy of the same vulnerable-discipline pass; `cl_pass_vul_nofit` carries the two-board evidence |
| `adx_sit_nt` as written (`requires: {}` at 62.5) | a `requires: {}` rung fits **1.00** and eats every rung below its priority. **Reshaped, not cut**: `total_points: [8, 40]` so `adx_pull_weak_$M2` still owns the bust |
| `balhigh_pass_silent_partner` as written (`lott_total_trumps: [0, 7]`, no suit argument) | with a silent partner that evaluator resolves to nothing and returns 0.0, so the gate always fits and the rung is "pass with under 16". Replaced by `hcp: [0, 15]` + `longest_suit_length: [0, 5]` |

### Not recovered, and stated rather than buried

**Board 988** stays a pass under a *different* rule than intended. Narrowing
`balhigh_pass_declined_$X` (`partner_suit: $X`, `suits: {$X: [5,6]}`, 0-14
points) was necessary — its first form blocked boards 226, 306 and 455 — and
board 988's seat now falls outside it. The board was already a pass, so
nothing regressed; the rung is right bridge in the position it now describes.

---

## Board index for the implementer

| board | seat/call | before → after | rung |
|---|---|---|---|
| 0 | W, `(2D) P P ?` | X → 2H | `ballow_own7_H` |
| 2 | N, `1H 1NT P P 2H ?` | P → X | `cl_reopen_X` |
| 19 | E | 4S → 2S | `ballow_raise_brake_S2` |
| 20 | N | P → 3H | `ballow_raise_lott3_H` |
| 49 | S | P → 4H | `balhigh_rebid_solo_H4` |
| 64 | N | 2H → P | `cl_pass_misfit_S` |
| 79 | S | 3C → P | `cl_pass_after_my_double` |
| 84 | N | 2S → P | `xd_pass_agreed_H` |
| 85 | N | P → 3H | `cl_new_long3_lim_H` |
| 119 | W | 2NT → X | `cl_penalty_X_over_nt` (+ `adx_sit_nt`) |
| 151 | W | X → 2H | `ballow_balance_major_H` |
| 152 | S | P → 2S | `adx_pull_weak_S2` |
| 166 | S | P → X | `cl_support_X_CH` |
| 182 | S | 2C → P | `cl_pass_silent_over_nt` |
| 198 | N | 3H → P | `ch_sell_out_H` |
| 217 | S | X → 2H | `cl_raise_pref_H2` |
| 226 | N | P → 3D | `balhigh_pref_D3` |
| 230 | S | 3C → P | `ballow_pass_partner_silent` |
| 241 | N | P → 4D | `ch_raise_lott4_D` |
| 262 | S | P → 2S | `cl_rebid5_two_S` |
| 263 | W | P → 3C | `cl_raise_lott3_C` |
| 297 | N | X → 2D | `cl_raise_overcall_D` |
| 306 | N | P → 4C | `balhigh_raise_lott4_C` |
| 357 | N | P → 4C | `ch_compete_agreed4_C` |
| 388 | N | 3S → 4C | `ch_raise_lott4_C` |
| 395 | S | P → 2S | `cl_new_strong2_S` |
| 455 | W | P → 4D | `balhigh_raise_lott4_D` |
| 494 | N | P → 3NT | `xd_nt_extras` |
| 528 | S | P → 3S | `ch_compete_agreed3_S` |
| 535 | S | 3H → 3S | `ch_raise_preempt3_S` |
| 544 | W | P → X | `ballow_X_strong` |
| 548 | N | 3H → P | `ch_pass_described` |
| 549 | S | 2D → P | `xd_pass_flat_D` |
| 597 | N | P → 3S | `ch_raise_preempt3_S` |
| 632 | S | P → 3D | `cl_raise_fit3_D` |
| 642 | N | P → X | `cl_reopen_X2` |
| 643 | N | P → X | `ballow_reopen_X_opener` |
| 646 | N | 2H → P | `cl_pass_sandwich_discipline` |
| 655 | N | P → 3H | `cl_rebid_agreed_law3_H` |
| 660 | S | P → X | `ballow_reopen_X2_shape` |
| 674 | N | P → 2D | `cl_new_strong2_D` |
| 689 | N | 1S → 2S | `cl_jumpadv_S2` |
| 707 | S | 2D → 3D | `xd_jump_own_D` |
| 758 | N | 1S → X | `ballow_reopen_X_opener` |
| 765 | N | 2D → 1S | `cl_adv_S1` |
| 784 | N | P → 3S | `cl_free_major3_over_nt_S` |
| 809 | N | P → 3H | `cl_raise_lott_short_H` |
| 870 | S | 4H → 4S | `ch_second65_S` |
| 928 | S | P → 3D | `cl_rebid5_three_D` |
| 932 | N | X → 2S | `cl_raise_pref_S2` |
| 933 | N | P → 4H | `xd_raise_lott4_H` |
| 934 | E | P → X | `balhigh_X_shape` |
| 936 | N | P → 4S | `balhigh_lott_push_S` |

---

## If the batch measures badly, pull in this order

1. `cl_raise_overcall_$X` — the one rung that deliberately outranks a
   profitable rule (`cl_negative_X1`, +1.90).
2. The discipline passes as a block (`cl_pass_*`, `ch_pass_*`, `ballow_pass_*`,
   `balhigh_pass_*`, `xd_pass_*`, 21 rungs). They pull *against* the CFR
   finding, and they are the half of the batch with the weakest independent
   measurement.
3. `their_fit: [7, 26]` back to `[8, 26]` in the four-level Law rungs — this
   costs boards 306, 455, 388 and 241 but restores Expert B's stricter brake.

The Law families (1a, 1b, 2), the reopening doubles, the `general_their_double`
four-level raise and the `general_pull_or_sit` rungs all fill holes with no
measured incumbent and should be the last things pulled.
