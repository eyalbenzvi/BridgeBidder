# Expert verdicts B: clusters 11-21 + worst single boards from #16 (board 719) onward
Seed 303030 dossier. Reviewer: external 2/1 expert. Every non-obvious indictment below
was reproduced against the live engine (`choose_bid`, `use_arbitration: False`); repro
notes inline. The dossier has no cluster 21; assignment covers clusters 11-20.

---

## CLUSTER 11 — `open_1D` | 5 boards | 33 IMPs — SPLIT VERDICT

**Mechanism.** "We opened 1D and never bid again" is four different auctions. Only one is
a rule defect.

- **Board 319 (-10): NEEDS-EXCEPTION.** 1D - (4S) - P - (P) - ? W holds `-.AJ73.AKJ74.T963`
  (13 HCP, spade void, 4-5-4 the other suits). Reproduced: P chosen, reopening X scored
  0.134 — the reopening double's 16+ HCP gate. Over a 4-level preempt of our opening, a
  void in their suit *is* the extra king. Par is -200 (5Dx-1 vs 4S= -620).
  **Fix:** in the high-level reopening double (`balhigh_reopen_X`), add a shape branch:
  `any_of: [ <current 16+ branch>, { hcp: [12, 40], evals: { "suit_length(their)": [0, 1] } } ]`.
  Endangers: phantom 4-level actions on 12-counts — the ≤1-card gate is the guard; measure.
- **Board 880 (-7): MISSING-AGREEMENT (optional, small).** After 1D - (1NT overcall),
  responder with `T9632.KQ8.-.J7642` (5 HCP, 5-5 blacks) has no weak natural 2-level bid
  (repro: cl_new rules want 10+ pts; P wins). A narrow `resp-over-their-1NT` context
  (2-level new suit = 5+ cards, 4-9, non-forcing) recovers part. Low priority.
- **Boards 150 (-6), 794 (-5), 957 (-5): NOTHING-WRONG.** 150 is BEN responding on 4 HCP;
  794 is a normal sell-out to 2H holding three trumps and a flat-ish 13 (repro: X scored
  0.349, defensibly so). These are the opening/thin-response style knobs DECISIONS.md has
  measured neutral. Do not chase.

---

## CLUSTER 12 — `uc_rebid_D2` | 3 boards (516, 565, 675) | 30 IMPs — MISSING-AGREEMENT

**Mechanism (reproduced, board 516).** There is NO authored context for responder's rebid
after `1C - P - 1D - P - 1M - P - ?` (grep: contexts exist for `1C - P - 1D - P - ?` and
for 1m-1M families only). The generic toolkit fills it, and `uc_rebid_D2`
(yaml ~9788: `total_points: [11, 40]`, **no ceiling**, non-forcing) swallows every
diamond hand from 11 points to a 16-count with 8 solid diamonds (516: `2.A.AKT98752.K87`
rebid 2D, passed out in 2D with 13 tricks — the engine offered literally nothing else:
5C/1S/3NT/2NT all matched 0.0). All three boards are this exact auction.

**Fix (author a context).** New group, pattern `1C - P - 1D - P - 1(H|S) - P - ?`:
- `rjd_pass` / `rjd_1NT`: floor, 6-10 (1NT only over 1H with spades stopped-ish; else pass/2D).
- `rjd_2D`: 6+ D, `total_points: [6, 10]`, non-forcing (the cap is the point).
- `rjd_3D`: 6+ D, `total_points: [11, 40]`, `forcing: one_round` — opener bids 3NT with
  the majors stopped or raises; this alone turns 516/565/675 into 3NT/5D/6D auctions.
- `rjd_2NT` 11-12 / `rjd_3NT` 13-16 with `weakest_unshown_stopper`.
**Hygiene (generic):** add `not: { evals: { rule_of_26: [26, 99] } }` to `uc_rebid_$s2`
family so game-going hands can never stall at the 2-level anywhere else.
Endangers: nothing visible — today these hands have no bid at all above 2D.

---

## CLUSTER 13 — `oc1H_1S` | 3 boards | 26 IMPs — NEEDS-EXCEPTION (the competitive-raise seam)

**Mechanism (reproduced on 84 and 552).** Advancer raises of an overcall have a dead zone
at 10-11 support points:
- `cl_raise_$M2` requires `total_points: [6, 9]` — an 8-HCP hand with a stiff ace
  (552: `KT4.A.Q6432.9743`) computes 10-11 and *fails the ceiling* (2S matched 0.134).
- `cl_raise_$M3` requires `rule_of_26: [22, 99]` — opposite an overcall whose shown
  minimum is ~8, an 11-count computes 19-20 and fails (84: `A43.T82.AK84.965` over their
  preemptive 3H, 3S matched 0.80 and lost to P; we sold to 3H-3 with 4S/6S our way).
So we sell out precisely on the hands every competitive-bidding text says must raise.

**Fix (exact):**
1. `cl_raise_H2`/`cl_raise_S2` (and the C/D twins if desired): `total_points: [6, 9]` → `[6, 10]`.
2. `cl_raise_H3`/`cl_raise_S3`: `rule_of_26: [22, 99]` → `[20, 99]` (keep the
   `total_points: [10, 40]` and LOTT-8 gates — they are the guard).
3. `cl_raise_lott3_$M`: `total_points: [3, 9]` → `[3, 10]` (mixed raise).
Covers boards 84, 552 here plus singles 190 and 312 below. Endangers: overboard raises
opposite minimum overcalls — trump/LOTT gates hold; re-measure the paired corpus.
- **Board 426 (-10): MISSING-AGREEMENT, honest cost, low priority.** 1H - (1S, on a
  17-count 6-bagger) - P - P - P. Advancer (`Q3.T7632.64.AKQ5`, 10 HCP, no heart stopper)
  has no sound systemic action (repro: 2NT 0.835 was the nearest miss, and it is stopperless
  anyway). BEN advanced a stopperless 1NT and got lucky. The principled patch is a
  power-double agreement for 17+ overcalls — heavy machinery for one board; record it,
  don't build it.

---

## CLUSTER 14 — `ballow_reopen_X` | 3 boards | 26 IMPs — SPLIT VERDICT

- **Board 166 (-11): MISSING-AGREEMENT — opener's action over the 4th-seat balance.**
  1D - P - P - (1S) - ? with `8.AKQ3.KQ65.AT98` (19 HCP). Reproduced: the engine's
  *undiscussed* "takeout-flavored cooperative double" matched **1.0** but its undiscussed
  discount (blended 0.727) loses to `cl_pass`; there is no authored context at all for
  `1$x - P - P - <their balance> - ?`. A 19-count sold at the one level; par 650 (4H).
  **Fix (author):** context `1$x - P - P - 1$y - ?` (and 2$y): `obal_X` = takeout of their
  suit, `hcp: [15, 40]`, ≤2 their suit, priority above cl_pass; `obal_1NT` 18-19 with
  stopper; suit rebids as today. Endangers: doubling with dead-minimum openers — the 15
  floor guards.
- **Board 742 (-10): MISSING-AGREEMENT — the adreo pattern anchor.** Advance context for
  reopening doubles exists (`advance_reopening_double`) but its pattern is exactly
  `1$o - bid - P - P - X - P - ?`. Board 742's auction 1S - 1NT - 2S - P - P - X - P - ?
  (their raise intervened) does not match, so advancer with `T.A632.Q987643.3` **passed a
  takeout-flavored double at the two level holding a 7-card suit** (repro: 3D matched
  0.003 — `cl_new_D3` wants 14+ pts) → 2Sx made +670 against us.
  **Fix:** add patterns to the same rule ladder: `1$o - bid - <their raise> - P - P - X - P - ?`
  and `1$o - 1NT - 2$o - P - P - X - P - ?` (this is the third instance of review-919191's
  theme "every double needs an advance ladder"; the ladder itself already exists — reuse it
  verbatim with `total_points: [0, 8]` suit pulls mandatory).
- **Board 871 (-5): NOTHING-WRONG.** Passing 2C-X out for +500 with `J9864` of their suit
  behind them, against a par that demands bidding a 26-point slam after their preempt, is
  a normal result.

---

## CLUSTER 15 — `gf_game_5C` | 4 boards | 26 IMPs — IMPLEMENTATION-BUG (call collision)

**Mechanism (reproduced, board 878).** Over a **1C** opening the call 2C is defined twice
in the same context: `r1m_2over1` (2/1 GF, 12+, priority 70) and `r1m_raise2` (simple
raise, 6-10, priority 50) — the yaml's own comment at ~line 1163 admits the expansion
covers 2C "incorrectly" for the 1C opening but only fixed the 1D side (`resp_1D_2C_gf`).
The engine merges them into `any_of`; a 9-HCP no-major raise hand (`QT9.876.KJ5.QJ73`)
matches the raise branch at 1.0 and the call is then **interpreted as game-forcing**
(source rule r1m_2over1, `establishes: game_forcing`). Repro: 2C chosen over a 1.0-fit
1NT. The phantom game force then marches 21-24 combined HCP to `gf_game_5C` (the
`gf_minor_3NT` stopper gate correctly says no 3NT — five clubs is all that's left).
Boards 878/470/962 are all `1C - 2C - 3C - 5C`.

**Fix (exact):** make 2C-over-1C single-meaning. Move `r1m_raise2` out of the
`expand: {m: [C, D]}` group into a 1D-only group (pattern `"1D - P - ?"`, call 2D), the
mirror of the existing `resp_1D_2C_gf` override. The 6-10 club-raise hands fall into
`r1m_1NT` (verified: it already matches 1.0) or 3C. Endangers: nothing — today those
hands create phantom game forces.
- Board 182 (-3) is the soft-floor cousin (`r1H_2C` on 11 HCP); leave it — sharpening the
  2/1 floor globally is a style knob the project has measured.

---

## CLUSTER 16 — `ch_new_C4` | 2 boards | 26 IMPs — NEEDS-EXCEPTION

**Mechanism (reproduced, board 282).** `ch_new_C4` (yaml ~8468: 5+ C, 14+ pts, quality
gate, priority 28) happily introduces a **fresh suit at the four level, vulnerable, over
their freely-bid 3NT, with a partner who has passed throughout** (`KQ763.J7.3.AK983`
after 1NT - 2S - 3D - P - 3NT: 4C chosen over a 1.0-fit P; 4Cx -1100 vs par +110).
This is the exact disease review-919191 fix #3 cured on `balhigh_new_*4` /
`balhigh_rebid_*4` via `partner_has_acted` — the `ch_new_*4` family never got the gate.

**Fix (exact):** add `partner_has_acted: true` to the `when:` of `ch_new_C4/D4/H4/S4`
(the condition exists and is already used at yaml 9271+). Board 282 recovered whole.
Board 289 (-9) survives partly: partner had acted, and the residual error is choosing 4C
over 3S on a 6-0-2-5 hand (suit-quality preference); accept the partial — no clean gate
without new machinery. Endangers: legitimate lone 4-level two-suiter actions — rare, and
the balhigh twins already measured fine with the same gate.

---

## CLUSTER 17 — `open_2C` | 2 boards | 25 IMPs — MISSING-AGREEMENT (severe) + the doubled-artificial invariant

**Mechanism (reproduced, both boards).** Every authored 2C continuation context begins
`2C - P - ...`. With ANY interference there is nothing:
- Board 557: 2C - (X) - P - (P) - ? opener (`AJ65.AKQJ6.AT6.K`, 23 HCP) has no rule;
  `fallback` **passed out our own doubled artificial 2C**. Repro: P chosen, best
  alternative 0.015.
- Board 220: 2C - (3H) - P - (P) - ? opener (20 HCP, solid diamonds) passes: reopening X
  is blocked by the (correct) 6-card-suit gate, and 4D needs `rule_of_26: 26` which can
  never be met when partner has shown nothing. Sold out to 3H with 6D cold.

**Fix (author four contexts):**
- `2C - X - ?`: `r2cX_pass` = waiting, 0+ (requires {}); `r2cX_XX` = 5+ HCP values (opt).
- `2C - X - P - P - ?`: opener's mandatory rebid ladder — natural suits (5+ cards,
  priority 60, requires {} on the cheapest = the floor), 2NT 22-24 w/ stopper sense.
- `2C - bid - ?`: `r2co_pass` = double negative floor (requires {}); X = 5+ HCP any;
  natural 5+ suits 5+ HCP.
- `2C - bid - P - P - ?`: opener MUST act: X = takeout-flavored (≤2 their suit), suit
  bids natural one-round forcing with `requires: {}` floor on the cheapest suit, 3NT with
  stopper. No pass rule in this context at all.
**Engine (re-raised from review-919191, still unimplemented — verified by grep):** the
fallback layer must never pass when the standing doubled bid is our own side's
alertable/artificial call. Board 557 is the second match in a row to hit it (cluster 18
is the third face of the same hole). Endangers: nothing; today the engine defends 2Cx
with 23 opposite a waiting hand.

---

## CLUSTER 18 — `nt_transfer_H` | 2 boards (649, 499) | 25 IMPs — IMPLEMENTATION-BUG (context hole; also covers single board 95, -15)

**Mechanism (reproduced, board 649, both seats).** They double our Jacoby transfer
(lead-directing). No context `1NT - P - 2$T - X - ?` exists, so the generic
"our bid was doubled" runout (`xd_pass`) has opener pass; then no context
`1NT - P - 2$T - X - P - P - ?` exists either, so **the transfer bidder passes out 2Dx
via `fallback` holding six hearts and a singleton diamond** (repro: P chosen with zero
alternatives above 0.35). -300/-500 a pop vs 4H cold; board 95 is the identical hole on
a doubled 2H transfer. This is the doubled-cue hole (919191 fix #1) wearing a new hat.

**Fix (author, mirror of `advance_cue_doubled`):**
- Context `1NT - P - 2D - X - ?` (and 2H twin): `xfrX_accept_2H` = complete with 3+
  hearts, priority 60; `xfrX_pass` = exactly 2 hearts (shows the doubleton, requires {}
  floor via the pair); `xfrX_XX` = 4+ good diamonds, to play (optional).
- Context `1NT - P - 2D - X - P - P - ?`: `xfrXpp_2H`: priority 60, `requires: {}` —
  responder's mandatory completion. Same pair for spades.
- Plus the engine invariant above (cheap insurance for the next artificial call).
Endangers: nothing — there is no correct line today. ~40 IMPs across the dossier.

---

## CLUSTER 19 — `ballow_rebid_S2` | 2 boards | 24 IMPs — NEEDS-EXCEPTION (two gates)

- **Board 479 (-10):** 1S - (2D) - P - (P) - ? with `AJT765.AKJ8.-.A64` (17 HCP, 6-4,
  ~20 total). Reproduced: reopening X correctly deferred to the suit rebid (the measured
  6-card-suit gate), but `ballow_rebid_S2` has `total_points: [11, 40]` — no ceiling —
  and the 3S/4S siblings sit at the same priority 29, so the cheapest wins and a
  20-total-point hand reopened a non-forcing 2S, passed out with 12 tricks.
  **Fix:** cap `ballow_rebid_$M2`/`$m2` at `total_points: [11, 15]`; set
  `ballow_rebid_*3` to `[16, 40]` (reopening jump = 16-18) — the exact mirror of
  review-919191 fix #14 (`cl_rebid_$s2` cap), which was implemented; the ballow family
  was missed. Endangers: 3-level reopenings on shapely 16s — quality gate already there.
- **Board 155 (-14):** after our balancing 2S (correct) they ran to 4H; overcaller
  (`AKQT743.Q.98.K74`, favorable vul) must take the 4S push (both sides make ~10).
  Reproduced: 4S matched 0.0 — `ch_rebid_S4` demands `rule_of_26: [26, 99]`, unreachable
  when partner has never bid. **Fix:** add a self-sufficient-suit branch to
  `ch_rebid_$M4`: `any_of: [ <current>, { suits: { $M: [7, 13] }, evals:
  { "suit_quality($M)": [2, 9], total_points: [11, 40] } } ]`, optionally
  `we_vulnerable: false`. Endangers: phantom saves at unfavorable — the 7-card +
  two-of-top-three-quality + vul gates guard; measure.

---

## CLUSTER 20 — `open_1NT` | 6 boards | 24 IMPs — MOSTLY NOTHING-WRONG + one small hole

Verdict split:
- **Board 579 (-4): MISSING-AGREEMENT (cheap).** `nt_pass` already (correctly) refuses to
  pass with a 6-card minor (`not: D [6,13]` is in the rule), but **no bail-out bid
  exists** — repro with `83.932.KJT653.T4`: P wins anyway with 2NT-inv at 0.028 the best
  "alternative". Add `nt_3D_signoff` / `nt_3C_signoff` (or 2NT-relay if preferred): 6+
  suit, 0-7 HCP, sign-off. Zero risk.
- **Boards 741 (-7), 825 (-6), 676 (-4), 187 (-2), 626 (-1): NOTHING-WRONG.** These are
  BEN's double-dummy-friendly 2-level interference nibbles over our 1NT. Repro on 741:
  the 2-level negative double correctly refuses with 4 cards of their suit; the "game"
  par requires bidding 24-HCP 4-4 games. Thin-game knobs; measured neutral twice. A full
  lebensohl/stolen-bid complex is the only real cure and is a scope decision, not a bug.

---

# SINGLE BOARDS (from 16th listed onward)

### Board 719 (-12) — MISSING-AGREEMENT (low priority)
1C - (2H wjo) - P - P - X - P - 2S - P - ? Doubler (`KT.A6.K852.AKT97`, 17) passed the
0-8 advance (repro: P; 3D 0.264 best). This is review-100boards board-77's "doubler's
rebid after a minimum advance" family, not yet extended to the **reopening** double.
Fix: context `1$x - <jump overcall> - P - P - X - P - <advance> - P - ?`: raise = 16-18,
2NT natural 18-19 w/ stopper. Partial recovery only (par 600 needs 3NT from the right side).

### Board 822 (-12) — NEEDS-EXCEPTION (cue machinery on a unilateral trump "agreement")
1H - 2D - 3H: `ob_2over1_jump3$M` establishes `agreed_suit: H` unilaterally; responder
`Q2.2.KQJT643.A96` (ONE heart) then lives in the cue context, where repro shows 4C
(cue_H_C) chosen — `cue_H_*` gates check controls and points but never trump tolerance —
and RKC lands 6H on the 6-1 (down 2; 3NT/6D cold). Fix: (1) add `suits: { $A: [2, 13] }`
to every `cue_$A_$x` rule (hearts and spades files); (2) add an escape in the same
context: `cue_$A_bail_3NT`, priority 45, `requires: { suits: { $A: [0, 1] } }`, shows
"no tolerance for the jump-set trump suit, offering 3NT" — for 822 responder bids 3NT
(makes 13 from his side at the other table). Endangers: hands that should raise on Hx —
the [2,13] gate keeps them in the cue lane.

### Board 921 (-12) — NEEDS-EXCEPTION (small; the big half belongs to cluster 3's gf_3NT stopper fix)
`open_2C` branch 2 (`hcp: [18, 21], ltc: [0, 3.5]`) catches a 20-HCP **minor two-suiter
with two stray singleton honors** (`K.Q.AQ954.AKQ654`, LTC 3) — repro: 2C chosen over a
1.0-fit 1C. 2C then wrong-sides everything and responder's stopper-less `gf_3NT` (other
reviewer's cluster) finished the -500. Fix: gate branch 2 to hands that can catch up:
add `any_of: [ { suits: { H: [5, 13] } }, { suits: { S: [5, 13] } } ]` inside the 18-21
branch (strong minor hands open 1m and jump — the systemically sound route). Endangers:
1m openings passed out on 20-counts — rule-of-15/20 openers make that near-impossible.

### Board 190 (-11) — covered by the CLUSTER 13 seam fix
Advancer `AT7.Q765.QJ763.5` (10-11 support pts, 4 trumps) had no raise of the 1H
overcall (repro: 2H and 4H both 0.134 — the [6,9] ceiling / rule_of_26 gap). The
cl_raise_$M2→[6,10] + lott3→[3,10] changes give the immediate 2H; we then compete to 3H
in tempo instead of dying and re-guessing later. Same verdict, same fix, no new item.

### Board 312 (-11) — covered by the CLUSTER 13 seam fix
1D - (1H) - 2D - ? advancer `AK84.AT832.T9.93` (11 HCP, FIVE trumps) — repro: 4H 0.409
(rule_of_26 25), no 3-level raise reachable. With the seam fix the hand raises (3H via
cl_raise_H3 at rule_of_26 20 = 11+3 dist +8 shown); BEN's table shows 4H making. Consider
also a 5-trump `any_of` on `cl_raise_$M4` (`suits: {$M: [5,13]}, total_points: [11,40]`)
— optional, measure.

### Board 346 (-11) — IMPLEMENTATION-BUG (mis-modeled context) + DELETE-RULE
The Jordan-2NT reply ladder (`oc2nt_*`, yaml ~10645) is written as if 2NT were a natural
invite: `oc2nt_3$M`/`4$M` demand a **6+ card** major ("correcting to our suit"),
`oc2nt_3NT`/`oc2nt_pass` require `not 6+$M`. But `jordan_2NT` *shows 4+ trump support
and establishes agreed_suit* — the fit is certain, and opener opened the major, so the
6-card gates are nonsense. Repro: opener `AJ75.Q9832.AJ6.6` (12 HCP, 5 hearts, stiff
club) bid 3NT over Jordan; -150 vs 4H/5C +450.
**Fix:** `oc2nt_3$M`: drop the 6-card gate, `total_points: [12, 14]`, sign-off-ish;
`oc2nt_4$M`: drop the 6-card gate, `total_points: [15, 40]`; **DELETE `oc2nt_3NT` and
`oc2nt_pass`** (passing a one-round-forcing Jordan 2NT should be impossible; 3NT with a
known 9-card major fit is anti-system — if kept at all, gate it 4-3-3-3 18-19).
Endangers: nothing — the current rules can only fire wrongly.

### Board 353 (-11) — NEEDS-EXCEPTION (same 4-level raise gate as cluster 13 / board 155)
(1S) - 3H wjo - (3S) - ? advancer `A2.J92.AQJ32.KJ3` (16 HCP, 3 trumps): repro: 4H
matched 0.80 (rule_of_26 25 unreachable opposite a wjo's shown ~5) and lost to
`ch_new_D4` at ≥0.9 — we bid 4D, and partner passed the "new suit" with six hearts.
Fix: in `ch_raise_lott_H4`/`ch_raise_$M4` (yaml ~8143/8167), relax `rule_of_26` 25 → 22
when `suits: { $M: [3, 13] }` (an `any_of` branch). The cluster-16 `partner_has_acted`
gate does NOT block this 4D (partner acted), so the raise branch must win on merit; with
the relax it matches 1.0 at higher priority than ch_new_D4 (28). Endangers: 4M on 16
opposite trash wjos — that is the textbook action anyway (Woolsey), and vul gates can be
added if the corpus objects.

### Board 589 (-11) — MISSING-AGREEMENT (opener's rebid over the simple minor raise)
1D - P - 2D - P - ? with `JT.AJ6.AK43.AQT2` (19). Repro: `uc_raise_D3` (priority 31)
outranks `uc_nt3` (29) and a 19-count **re-raised to a non-forcing 3D**, +150 vs 3NT+3.
No context `1$m - P - 2$m - P - ?` exists (verified by pattern grep). Fix (author):
`omr_2NT` = 17-19 natural try (stopper-soft — partner promised nothing outside);
`omr_3NT` = 18-19 with `weakest_unshown_stopper: [0.9, 9]`; `omr_stop_try_$x` optional;
floor = pass 12-16. Recovers ~6 of 11 (2NT+4 vs 3D+3); the DD 3NT on JT-tight spades is
not a target to chase.

### Board 654 (-11) — NOTHING-WRONG
1C by `KQ2.AJT8.AJ4.KJ2` passed out; responder had 4 HCP with 7 diamonds. Responding on
4 HCP is the thin-response knob DECISIONS.md has measured twice as neutral. BEN's +630
is DD-friendly. Record, do not chase.

### Board 679 (-11) — MISSING-AGREEMENT (asker's rebid after the weak-two 2NT ask)
2H - P - 2NT - P - 3H(min) - P - ? asker `AK974.K.A852.AQ9` (19): repro shows the
context does not exist (grep: `2H - P - 2NT - P - ?` is the last authored node), so
`uc_new_S3` fired (natural, non-forcing) and opener passed 3S with one spade... +170 vs
+710. Fix (author): context `2$W - P - 2NT - P - 3<any> - P - ?`: `ask_4$W` = 2+ trumps
or 14+ total, to play; `ask_3NT` = 14-19, no trump-fit requirement (partner's suit is
the source of tricks); floor pass only over a minimum reply with pure invite. Also give
the weak-two bidder the mirror context so a further new suit is never passed.

### Board 690 (-11) — IMPLEMENTATION-BUG (one-line)
`nt2_stayman_placement` (yaml ~5695, pattern `2NT - P - 3C - P - 3(D|H|S) - P - ?`):
`nt2_stm_4H` (priority 60) requires only "I hold 4 hearts" — it never checks WHICH major
opener answered. With 4-4 majors opposite a 3S reply, responder bid 4H into the void
(repro'd from the dossier auction; the yaml text is unambiguous). Fix:
`nt2_stm_4H`: add `when: { standing_bid_strain: [H] }`; `nt2_stm_4S`: add
`when: { standing_bid_strain: [S] }`. (The 1NT-Stayman twin uses paired expansion and is
safe.) Endangers: nothing.

### Board 789 (-11) — NOTHING-WRONG
1D - P - 1S - (2D cue) - X(support) - (3H) - 4S, making 12. A 27-HCP two-fit slam that
BEN reached via DD-informed Blackwood. Our fast-arrival 4S on a 12-count is normal.
Variance / thin-slam knob.

### Board 802 (-11) — NEEDS-EXCEPTION (the strong-splinter orphan)
Responder `K642.AK54.KQ94.6` (17, stiff club): `r1S_jacoby_2NT` requires
`singleton_or_void: [0, 0]`, splinters are capped `hcp: [9, 13]` — so a 15+ hand with
shortness has NO game-forcing raise route; repro: 4C splinter still chosen (soft fit,
nothing else above 0.1), opener then read it as 9-13 and signed off (`spl_wasted`
evaluator itself is correct — verified it does not count aces). Fix: in
`r1$M_jacoby_2NT`, replace the shortness gate with
`any_of: [ { evals: { singleton_or_void: [0, 0] } }, { hcp: [15, 40] } ]` — big hands
start Jacoby regardless of shape (standard: splinters are limited). Endangers: Jacoby
continuations must tolerate a hidden stiff on the 15+ branch — they do (opener describes,
responder places).

### Board 836 (-11) — MISSING-AGREEMENT (the sacrifice double)
Our freely-bid 4H, they save 5C, both our hands pass (repro: opener's X = 0.122, blocked
by the reopening double's 6-card-suit gate — right gate, wrong context). +100 vs par
+300 (5Cx-2). Fix: a dedicated rule in the ch layer: `ch_sac_X`: `when: { agreed_suit:
<ours set>, we_hold_contract: false }`, requires `hcp: [13, 40]`, `evals: { quick_tricks:
[2, 12] }`, no trump-length requirement and NO 6-card-suit veto — when they outbid our
freely-bid game, X is the default and pass would be forcing. Endangers: doubling
makeable saves — quick-trick gate guards; measure.

### Board 840 (-11) — MISSING-AGREEMENT (flagged risky; measure before keeping)
They cue-jumped to 4S (Michaels-style, majors) over our 1C-1D; we held 9-10 combined
diamonds plus a 6-card club source and sold to 4S-making with 5D cold (repro: 5D scored
~0; no 5-level minor competition rule exists). Fix (optional): `ch_raise_lott_$m5`:
5$m over their 4$M with `lott_total_trumps($m): [9, 26]`, `total_points: [10, 40]`, and
a second-suit/shape gate. This is the classic 5-level-belongs-to-the-opponents coin-flip;
implement behind a measurement, or accept as honest cost.

---

# FIX LIST (deduplicated, priority order)

~150-170 of the ~250 assigned IMPs pass through items 1-6. "Recovers" counts dossier
boards in MY assignment only; several items also patch boards in the other reviewer's half.

**1. Doubled-transfer contexts + the doubled-artificial engine invariant**
(IMPLEMENTATION-BUG; cluster 18: 649 -13, 499 -12; also board 95 -15 in the other half;
2C face: board 557 -15 → shared with #2. ~40 IMPs)
   - New contexts `1NT - P - 2D - X - ?` / `1NT - P - 2H - X - ?`: accept with 3+ cards
     in responder's major (priority 60); pass = exactly 2 (floor); optional XX = to play.
   - New contexts `1NT - P - 2$T - X - P - P - ?`: mandatory completion, `requires: {}`,
     priority 60.
   - Engine: fallback layer must never choose P when the standing doubled bid is our own
     side's alertable/artificial call (re-raised from 919191 — verified still absent).
   - Endangers: nothing; the current line is playing the transfer suit doubled in a 6-1.

**2. 2C-opening interference contexts** (MISSING-AGREEMENT; cluster 17: 557 -15, 220 -10;
~25 IMPs)
   - `2C - X - ?` (waiting pass floor, optional XX); `2C - X - P - P - ?` (opener rebids,
     cheapest suit `requires: {}`); `2C - bid - ?` (pass = double-negative floor, X =
     values, suits natural); `2C - bid - P - P - ?` (opener MUST act: takeout-flavored X,
     natural forcing suits with a `requires: {}` floor, 3NT w/ stopper; no pass rule).
   - Endangers: nothing — today a 23-count defends their contract at the two level.

**3. Kill the 1C/2C call collision** (IMPLEMENTATION-BUG; cluster 15: 878 -12, 470 -6,
962 -5; ~23 IMPs + latent phantom game forces)
   - Move `r1m_raise2` out of the `{m: [C, D]}` expansion into a 1D-only group
     (mirror of `resp_1D_2C_gf`). 6-10 club hands land in the already-1.0 `r1m_1NT`.
   - Endangers: nothing.

**4. The competitive-raise seam** (NEEDS-EXCEPTION; cluster 13: 84 -12, 552 -4; singles
190 -11, 312 -11, 353 -11; ~49 IMPs gross, expect partial)
   - `cl_raise_H2`/`cl_raise_S2`: `total_points` `[6, 9]` → `[6, 10]`.
   - `cl_raise_H3`/`cl_raise_S3`: `rule_of_26` `[22, 99]` → `[20, 99]`.
   - `cl_raise_lott3_$M`: `total_points` `[3, 9]` → `[3, 10]`.
   - `ch_raise_lott_H4`/`ch_raise_S4` family: `any_of` branch relaxing `rule_of_26`
     25 → 22 with 3+ trumps (board 353/155-family).
   - `ch_rebid_$M4`: `any_of` branch `{ suits: { $M: [7, 13] }, "suit_quality($M)":
     [2, 9], total_points: [11, 40] }` (board 155's 4S push), optionally NV-only.
   - Endangers: overbidding opposite minimum overcalls/wjos — trump+LOTT gates remain;
     this is the one item to re-measure most carefully.

**5. Responder-rebid context after 1C - 1D - 1M** (MISSING-AGREEMENT; cluster 12: 516,
565, 675; ~30 IMPs)
   - New context `1C - P - 1D - P - 1(H|S) - P - ?` with capped 2D (6-10), forcing 3D
     (11+), 2NT/3NT ladder as specced in the cluster block.
   - Generic hygiene: `uc_rebid_$s2` add `not: { evals: { rule_of_26: [26, 99] } }`.
   - Endangers: nothing visible.

**6. Rewrite the Jordan-2NT reply ladder** (IMPLEMENTATION-BUG + DELETE-RULE; board 346;
11 IMPs) — drop the 6-card gates from `oc2nt_3$M`/`oc2nt_4$M` (make them 12-14 / 15+),
delete `oc2nt_3NT` and `oc2nt_pass`. Endangers: nothing.

**7. `nt2_stm_4H`/`4S` strain linkage** (IMPLEMENTATION-BUG; board 690; 11 IMPs) —
`when: { standing_bid_strain: [H] }` / `[S]` respectively. One line each.

**8. ballow rebid caps** (NEEDS-EXCEPTION; cluster 19 board 479; 10 IMPs) —
`ballow_rebid_$M2/$m2` capped `[11, 15]`; `ballow_rebid_*3` floored `[16, 40]`
(mirror of the implemented cl_rebid cap from 919191 #14).

**9. `partner_has_acted` on `ch_new_*4`** (NEEDS-EXCEPTION; cluster 16 board 282;
17 IMPs) — one `when:` key on four rules; the balhigh twins already carry it.

**10. Opener over the 4th-seat balance + adreo pattern generalization**
(MISSING-AGREEMENT; cluster 14: 166 -11, 742 -10; ~21 IMPs)
   - Context `1$x - P - P - <their bid> - ?`: takeout X 15+, 1NT 18-19, suit rebids.
   - `advance_reopening_double`: add patterns `1$o - bid - <raise> - P - P - X - P - ?`
     and `1$o - 1NT - 2$o - P - P - X - P - ?` reusing the existing ladder.

**11. Cue-bid trump tolerance + 3NT bail** (NEEDS-EXCEPTION; board 822; 12 IMPs) —
`suits: { $A: [2, 13] }` on all `cue_$A_$x`; new `cue_$A_bail_3NT` with `$A: [0, 1]`.

**12. Jacoby-2NT accepts 15+ hands with shortness** (NEEDS-EXCEPTION; board 802;
11 IMPs) — `any_of` on the shortness gate as specced. Splinters stay 9-13.

**13. Weak-two ask continuation context** (MISSING-AGREEMENT; board 679; 11 IMPs) —
`2$W - P - 2NT - P - 3<any> - P - ?`: 4$W / 3NT / invite-pass; plus opener's mirror.

**14. Sacrifice double over our freely-bid game** (MISSING-AGREEMENT; board 836;
~5-8 IMPs) — `ch_sac_X` as specced; quick-trick gated.

**15. Shape branch on the 4-level reopening double** (NEEDS-EXCEPTION; cluster 11
board 319; 10 IMPs) — `balhigh_reopen_X` `any_of` with `{ hcp: [12, 40],
"suit_length(their)": [0, 1] }`.

**16. Small / optional (measure or accept):**
   - `nt_3$m_signoff` weak 6-card-minor bail over 1NT (board 579; 4 IMPs, zero risk).
   - Responder's weak natural 2-level suit over their 1NT overcall (board 880; 7 IMPs).
   - `open_2C` 18-21 branch requires a 5+ major (board 921; ~4 of its 12 IMPs).
   - Doubler's rebid after advance of a reopening X (board 719; partial).
   - 5-level minor LOTT competition over their 4M (board 840; coin-flip — measure).

**Deliberately NOT chased (NOTHING-WRONG):** cluster 11 boards 150/794/957, cluster 14
board 871, cluster 20 boards 741/825/676/187/626, singles 654 and 789 — thin-response,
thin-game and balancing style knobs the project has twice measured neutral, DD-friendly
BEN aggression, and a 27-HCP slam. The "no Michaels" scope decision is respected
(boards 190/840 show BEN profiting from two-suited jumps; the losses there are recovered
through the raise-seam and 5-level items instead, not by adding the convention).

**Recurring engine-level theme (third match running):** every artificial call needs (a)
a partner interpretation with a floor, (b) an advance/continuation ladder, and (c) a
plan for being doubled. Clusters 17 and 18 are both instances of (c); the invariant in
fix #1 closes the class, not just the instance.
