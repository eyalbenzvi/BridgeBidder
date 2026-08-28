# E3 verdicts (reviewer A): clusters 1-10 + first 15 worst single boards
Seed 303030. Method: every indicted mechanism below was reproduced through `choose_bid`
(boards 978, 853, 344B, 506 both seats, 443, 573, 171, 596, 925, 130, 576, 364, 762,
961, 909, 716 both seats, 381, 857, 95 both seats, 89, 591, 819, 548, 375, 149, 949,
986, 636, 756, 261) — diagnoses are engine behaviour, not conjecture. No fix from
EXPERT_REVIEW_100_BOARDS.md or EXPERT_REVIEW_919191.md is re-recommended; where a
previous review's recommendation was evidently NOT implemented it is flagged as such.

The headline: three structural species carry most of my assigned deficit —
1. **Partner's double has no generic pull/sit ladder** (clusters 4, 9, parts of 7,
   singles 375, 845; also explains cluster 14). Advancers sit doubled contracts with
   voids, 7-card side suits, singleton trumps. The reviews authored ladders for four
   specific patterns; every new pattern re-opens the hole. It needs the GENERIC context.
2. **`gf_3NT` has no stopper or shape test** (cluster 3, board 344): in a game force it
   outranks (priority 34 vs 29) the fit-1.0 natural suit rebid on any no-fit hand,
   including 6-card suits and stiff-in-partner's-suit hands.
3. **Game-placement rules shadow the slam machinery at range seams** (clusters 6, 8, 10;
   singles 149, 949, 819, 548, 591): uncapped game raises outrank RKC by priority, the
   RKC 5H/5S replies are mis-counted, and soft rule_of_26 gates fire quantitative raises
   on 27-29 combined.

---

## CLUSTER 1: `all-pass` (43 boards, -192) — SPLIT: mostly NOTHING-WRONG; two upstream diseases
`all-pass` means our side never bid at the damaged table; the cluster is dominated by
defensive boards where BEN's constructive (and double-dummy-friendly) auction won. Verdicts
by example:
- **Board 344 (-16): IMPLEMENTATION-BUG at the OTHER table (gf_3NT), plus a recorded scope
  cost.** Table B reproduced: after 1D - P - 2C(GF), E (T54.A9.Q97543.KQ) chose `gf_3NT`
  over the fit-1.0 `uc_rebid_D2` (blended 0.787) — priority 34 vs 29, no stopper asked
  (spades Txx wide open), 3NT-1 with 6D cold. Fix under CLUSTER 3 (Fix C). Table A's
  missed 6S save on a 7-HCP 5-5 freak is the documented "no Michaels" scope decision
  (yaml line 21, review-2 board 56) — leave recorded, not chased.
- **Board 261 (-12): NOTHING-WRONG.** BEN doubled 3C directly on an 11-count with three
  small hearts; `v3_C_X` (14+ short, or 18+) is mainstream discipline. Reproduced: X fit
  0.047. Style variance; the pass-out-seat-lighter idea was already flagged "measure,
  risky" by review 1 (its board 33) — this is DIRECT seat, even less attractive.
- **Board 808 (-11): NOTHING-WRONG.** BEN preempts 3H on J876432 (J-high, 4 HCP); our
  preempt quality gates were measured. Our defensive passes are all normal.
- **Board 857 (-10): NOTHING-WRONG (style seam).** Reproduced: N over 1H holds 10 HCP,
  KJ842 — `oc1H_2D` (11-17) fit 0.8, one point off, lost to pass. The "off-by-one seam
  turns into a pass" species is known; a 10-count vul 2-level overcall is a knob, not a
  bug. (Table B's 2H rebid on a 14-count 7-bagger is worth an eyebrow — `ob_1H1S_2H` vs
  `_3H` split by total_points 16 — but the damage table was A.)
- Remainder (39 boards, mostly -1..-6): long-tail defensive variance. No rule change.

## CLUSTER 2: `uc_nt3` (18 boards, -115) — SPLIT: uc_nt3 is a symptom; four upstream holes
- **Board 302 (-13): NEEDS-EXCEPTION (semi_balanced starves 4441/5431 slam hands).**
  N (K72.AKT9.AKT63.9, 17) opposite a 15-17 1NT passed 3NT via `fallback`: `qr3_6NT` and
  `qr3_4NT_quant` both hard-fail `semi_balanced: [1,1]` on 3=4=5=1, and no other rule
  exists ≥3NT. Range-with-no-rule. Fix: in `quant_raise_of_3NT`, relax the shape gate to
  `any_of: [ {evals: {semi_balanced: [1,1]}}, {evals: {singleton_or_void: [1,1], controls: [5,12]}} ]`
  on `qr3_4NT_quant`/`qr3_6NT` (a strong hand with one singleton may still invite/blast
  on 33+). Measure-first — this widens a measured NT-raise family.
- **Board 961 (-12): MISSING-AGREEMENT — no advance ladder for the double of a 3-level
  preempt.** Reproduced: after 3H - P - P - X - P, S (J63.J83.KT9.KQJ6) has zero advance
  rules; `uc_nt3` won on J83 "stopper" (soft gate). BEN's advancer bid 4C → 4S. Covered
  by Fix A (the generic pull ladder gives S 4C; 3S/pull outranks the 3NT punt). Twin of
  single board 375.
- **Board 628 (-12): MISSING-AGREEMENT — asker's continuation after the weak-2 feature
  reply.** After 2S - P - 2NT(ask) - P - 3S(feat_S_min) - P - ?, W (15, Q75/Q6 side suits)
  had no context; generic `uc_nt3` bid a stopper-less 3NT-5. Fix (author): context
  `2$W - P - 2NT - P - 3$W - P - ?`: P = the floor opposite a minimum (rule `w2ask_pass`,
  `requires: {}`, priority 50); `w2ask_4$W` raise with `evals: {total_points: [15,40]}`;
  3NT only via `evals: {weakest_unshown_stopper: [0.9,9]}` SHARP + hcp [15,19]. Mirror
  for the feature replies (3x contexts) if absent.
- **Board 101 (-12): MISSING-AGREEMENT — no pull of 3NT with a 7-card major.** N
  (9.AKJT986.KT32.J) bid a free 3H, S chose 3NT (defensible with Qx), N passed via
  `fallback`. Fix I below (qr3_4$M pull rule). Partial recovery (4H, not BEN's 6H).
- Remainder: tails of the same species. Verdict for the rule itself: keep `uc_nt3`; its
  weakest_their_stopper gate should be SHARP (a J83 "quarter stopper" soft-passed on 961)
  — same counting-claim doctrine as cl_nt2. One-line change, included in Fix E.

## CLUSTER 3: `gf_3NT` (15 boards, -109) — IMPLEMENTATION-BUG (gate) + MISSING-AGREEMENT (2C tree)
Mechanism, reproduced twice (344B, 506): `gf_3NT` (priority 34) requires only
hcp 0-17 + `lott_total_trumps: [0,7]` + `stopper(their)` (vacuous uncontested). It
therefore outranks every fit-1.0 natural rebid (priority 29 generics) for ANY no-fit hand
in a GF: E on 506 (12 HCP, AQJT7 clubs, T7 diamonds) bid 3NT instead of 3C; N on 748
(4 HCP, 5 hearts, stiff spade) bid 3NT; N on 207 (4=1=5=3, stiff in partner's hearts) bid
3NT; W on 222 (KQT743 hearts!) bid 3NT over 2NT instead of 3H. The 2C boards compound it:
there is no responder-rebid context after `2C - P - 2D - P - 2M/3m`, so the generics are
all responder has.
**Fix C (mechanical):**
1. `gf_3NT` add `evals: { weakest_unshown_stopper: [0.9, 9] }` — the same honest "is 3NT
   an option" gate `gf_minor_3NT` already carries. Make it sharp (counting claim).
2. `gf_3NT` add `not: { evals: { longest_suit_length: [6, 13] } }` — with a rebiddable
   6-card suit the suit rebid (uc_rebid_*, fit 1.0) must win (board 222, 344B).
3. (Secondary, author) responder's rebid context `2C - P - 2D - P - 2$M - P - ?`:
   raise 3$M with 3+ trumps (GF, agreed_suit — feeds the existing cue/RKC floor); cheapest
   new 5-card suit natural GF at `total_points: [4, 40]` (opposite 2C everything is worth
   showing — the generic `uc_new_*` 10/14-point floors are what starved boards 748/207);
   2NT = no suit, no stopper claim ("second negative"-ish, `requires: {}` floor).
4. Opener over responder's 3NT with a two-suited monster (506: W passed with 20 and 5-6
   shape; `qr3_*` semi_balanced-blocked): add to `quant_raise_of_3NT` a natural
   `qr3_4$s_nat`: `when: {my_suit: $s}`, `requires: {suits: {$s: [6,13]},
   evals: {total_points: [20,40]}}`, forcing one_round — with partner's reply floor
   (raise/preference contexts already generic). Expect partial recovery on the 2C
   monsters; the gate fixes (1-2) are the reliable money.
Boards recovered (estimate): 506, 207, 748, 222, 344 + tail — 50-70 IMPs touched.
Endangers: GF hands with no stopper and no 6-card suit now route via `gf_2NT_natural`
(forcing, exists, priority 33) — verify it keeps a floor; fallback remains.

## CLUSTER 4: `ch_penalty_X` (5 boards, -55) — SPLIT: IMPLEMENTATION-BUG (evaluator) + MISSING-AGREEMENT (the sit/pull ladder)
- **Bug:** `ch_penalty_X` gates "trump length" on `suit_length(their)` which reads their
  FIRST suit. Board 799: W doubled 4H holding a HEART VOID — the [3,13] gate read his
  four CLUBS (their first suit). This is the documented first-suit-only residue
  (DECISIONS: "stoppers(their) still reads only their first suit everywhere except...").
  Fix: new sharp evaluator `standing_suit_length` = my cards in the strain of the current
  standing bid; `ch_penalty_X` replace `"suit_length(their)": [3,13]` with
  `"standing_suit_length": [3, 13]`. A penalty double's trump tricks live in the suit
  being doubled, not the first suit they bid.
- **Missing:** in all five boards the double was left in (or the auction died) because
  advancer had no pull rule: 443 E sat 3SX with a spade VOID and five hearts (reproduced:
  4H does not exist, uc_pass wins); 165 W sat 3SX with SEVEN hearts and 1 HCP; 238 W sat
  3SX with a spade void, 6-4 red; 799 E sat 4HX with SEVEN spades (A-seventh!). Fix A
  (generic pull/sit context) covers all four.
Verdict on the rule: keep — its own gates (15+, QT 3+, trump length) are measured
doctrine; fix the evaluator and give advancer the ladder.
Boards recovered: 443, 165, 238, 799 (~48 of 55).

## CLUSTER 5: `uc_rebid_D3` (6 boards, -50) — MISSING-AGREEMENT (three small "invitation/continuation answered by silence" contexts); the rule itself is innocent
The generic minimum rebid wins whenever the specific continuation seat has no context:
- **573 (-11):** doubler's rebid missing. 1D - 2H - X - P - 3D - P - ? left W (13,
  KJ42 hearts) with nothing (reproduced: 3NT hard-blocked by `semi_balanced` on 4=4=1=4,
  uc_pass won). Fix (author): context `1$m - 2$y - X - P - 3$m - P - ?` (expand over the
  2-level-overcall pairs): `nxdr_3NT`: `requires: {hcp: [12, 40], evals:
  {weakest_their_stopper: [0.9, 9]}}` (NO semi_balanced — partner's 6-card minor is the
  source of tricks), priority 60; `nxdr_pass` floor `requires: {}` priority 50; 3$M with
  5+ cards. The classic "X then 3NT" agreement.
- **909 (-11):** opener's answer to the competitive 2NT invite missing. After
  1D - 1H - 2NT(nx_1m1H_2NT) - P - ?, W (14, AKJ973 diamonds) reproduced choosing 3D
  (uc_rebid_D3, non-forcing decline) over the 0.835-fit 3NT. Fix (author): context
  `1$m - 1$v - 2NT - P - ?`: `o2ntc_3NT` hcp [13,40] OR (hcp [11,12] + 6-card suit
  quality 2+) priority 60; pass floor 11-12; 3$m only as a true minimum misfit escape.
  Same species as the two invite-answer contexts authored in review 1 (its fix 6) —
  this is the contested-auction branch they did not cover.
- **829 (-10):** borderline NOTHING-WRONG (12 opposite 11-12, decline is normal; DD paid
  BEN's 3NT because AKQJ84 ran). The eyebrow is `ob_1NT` firing on 2=3=6=2 — its
  `semi_balanced` soft-admitted a two-doubleton 6-card hand. Optional hygiene: make
  `semi_balanced` sharp on `ob_1NT`; low confidence, small.
- **620 (-8):** the sandwich-advancer's X (showing spades) was never read — N rebid 3D
  with QJ84 of spades. Same "respond to partner's double" family; the specific context
  `1$x - <sandwich> - <raise> - X - P - ?` is a genuine gap but rare; fold into Fix A's
  generic ladder (X was theirs-doubled? no — here partner doubled their 2H: Fix A's
  pattern matches, N holds 2 hearts → pulls to its cheapest 4-card suit = 3S). Verify.
Boards recovered: 573, 909, 620 (~30 of 50).

## CLUSTER 6: `qr3_4NT_quant` (4 boards, -50) — NEEDS-EXCEPTION (make the counting claim sharp)
Reproduced (171, 716): the quantitative raise fires on 27-29 true combined because
`rule_of_26: [30, 99]` is SOFT and the length-points in a 6-card minor inflate my side of
the sum (board 171: 15 HCP counted ~17-18; partner's rjrb_3NT floor 10). Three of the four
boards are "we raised a making/failing 3NT to a minus 4NT on ~28 combined" (716 -14,
842 -13, 171 -12); board 930 is BEN blasting a 28-HCP 6NT that happened to make —
NOTHING-WRONG.
**Fix E (this rule's share):** make `rule_of_26` SHARP on `qr3_4NT_quant` and `qr3_6NT`
(exact precedent: `cl_nt2`/`ch_nt3` gates made sharp — "competitive free NT bids are
counting claims, not estimates"; a slam invite is the purest counting claim in the file).
Optionally raise the 4NT gate 30 → 31 while at it (33 is the target; inviting needs
partner's decline to still be safe at 4NT — that wants 31 floor).
Also note: on 716/171 the 3NT bidder had already heard MY 16-18 jump; if slam were on,
the unlimited hand would move. The sharp gate happens to kill exactly these seats (my
side of the sum tops out at 18+10=28 and 19+10=29). No shadow contexts needed.
Boards recovered: 716, 842, 171 (~39 of 50). Endangers: true-30 borderline invites the
soft gate used to sneak through — measure; the doctrine says give those up.

## CLUSTER 7: `fallback` (5 boards, -48) — SPLIT (fallback is never the disease)
- **596 (-14): MISSING-AGREEMENT + engine hazard.** Reproduced: after their
  1C-1H-3H-4H, our balancing X (balhigh_X, forcing one_round), advancer W
  (T63.42.QJT87532.-) had ZERO candidates — pass is filtered by the forcing X, no rule
  covers 5D — and the backstop invented **4S on a 3-card suit**: -1100. Fix A gives W the
  5D pull (own-8-card-suit rule, standing_suit_length H = 2). Engine hardening: the
  fallback layer must never invent a NEW suit at the 4+ level when a 6+ card suit is
  available in hand (cheap invariant: among zero-candidate escapes prefer the longest
  suit) — today it picked spades over an 8-card diamond suit.
- **298 (-11): MISSING-AGREEMENT (GF preference), partial.** 1S-2C(GF)-2S-3C-3S-4C then
  fallback 4D/4H wandering: responder (Ax of spades, 16) has no "preference to 4S with a
  doubleton opposite a shown 6-card suit" rule, so both hands recursed own-suit generics.
  Fix (author, small): generic rule `uc_pref_game_4$M`: `when: {partner_suit: $M,
  game_forced: true}`, `requires: {suits: {$M: [2,3]}, evals: {"lott_total_trumps($M)":
  [8,26], total_points: [0,17]}}`, priority 36, non_forcing. (BEN's 6S on these cards is
  DD-flattered; expect the game, not the slam.)
- **381 (-10): NEEDS-EXCEPTION (overcall quality waiver), measure-first.** Reproduced: N
  (J87542.AK74.K5.K, 12) over 1C — `oc1C_1S` fit 0.757, blocked only by
  `suit_quality(S): [1,9]` vs J-high; pass won. A 12-count with a 6-card major is a
  1-level overcall in any expert book regardless of pips. Fix K: to each 1-level
  `oc1x_1H/1S` add an `any_of` waiver branch: `{suits: {$s: [6,13]}, hcp: [10,16]}` or
  `{suits: {$s: [5,13]}, hcp: [13,16]}` (six cards is the credential — the file's own
  board-9 doctrine; with full opening values, any five). Endangers measured overcall
  style: run paired before keeping. Also covers board 845's W (J9873, 14).
- **759 (-10): NEEDS-EXCEPTION.** `aw2r_responsive_X` fired on a 5-HCP hand with six
  diamonds (S: Q.K963.T76432.KT) — review 2 added the no-5-card-major denial but no
  values floor. Fix: add `hcp: [8, 40]` (sharp-ish) and `not: {evals:
  {longest_suit_length: [6,13]}}` to `aw2r_responsive_X`; with S passing, N defends 4S
  instead of inventing 4NT via fallback (the doubler's 17-count has no second double
  below 19 by design — correct).
- **161 (-3):** tail, leave.

## CLUSTER 8: `cue_H_signoff` (4 boards, -46) — NOTHING-WRONG (with one recorded option)
All four are 25-30 HCP shape slams (925: 26-29 w/ void; 2: 25!; 674: 27; 130: 30) that
BEN blasts and double-dummy rewards. Reproduced 925 and 130: the cue machinery worked as
designed — cues exchanged, signoff denied the missing controls, and the 4NT ask was
correctly blocked (925: void + only 2 keycards = the measured Blackwood veto; 130: r26 29
vs the measured [31,99] gate, fit 0.8). On 925 the slam needs the club ace onside; on 2
it is a 25-point double-fit freak. DECISIONS measured the r26-31 line and logs "par slams
on freak shape are deferred"; chasing these makes the system reckless. Do not change
`cue_H_signoff` or the cue contexts.
Recorded option (do NOT implement without a paired run): board 130 is the only one inside
touching distance — an `any_of` branch on `gst_rkc_*` allowing r26 [30,99] when
`controls: [6,12]` (three aces do the queen-and-king work the 31st point stands for).
Expected value unclear; the sharp-r26 change in Fix E pushes the other way deliberately.

## CLUSTER 9: `balhigh_reopen_X` (3 boards, -41) — KEEP THE RULE; MISSING-AGREEMENT (its advances, again)
Special-attention verdict: **do not delete, do not gate further.** In all three boards the
double itself was textbook (364: 17 balanced short in hearts; 576: 16 with both minors...
S's X after the 2NT ask is takeout of diamonds with hearts known — fine; 762: 16 with
their hearts KJ tight — aggressive third action but it had a making spot). Every IMP was
lost one seat later: the ADVANCER sat with 0-2 trumps (364: W sat 3HX with a singleton
heart and KJT97 clubs; 576: N sat 3DX with a SINGLETON diamond and six hearts; 762: E sat
3HX with 74 and five spades). Reproduced all three: zero advance candidates — the ladder
review 2 authored is anchored to the single pattern `1$o - bid - P - P - X - P - ?`
(`adreo_*`), which none of these auctions match (1NT opening; weak-2 ask; long
competitive prefix).
This is the third review in a row finding the same species. The per-pattern approach has
now failed three times; the fix must be generic (Fix A). Corroboration from cluster 14
(ballow_reopen_X, other reviewer's assignment): board 742's advancer sat 2SX with a
singleton spade and SEVEN diamonds (-870); board 166's advancer sat with four hearts and
the 4H game on. Same fix, same context.
Boards recovered: 364, 576, 762 (+166, 742) — ~41 (+21) IMPs touched, partial on 364
(4C reaches +130..+600, not BEN's 6C).

## CLUSTER 10: `rjr_game` (5 boards, -37) — IMPLEMENTATION-BUG (priority shadow of RKC)
Reproduced board 978: after 1C - 1H - 3H(16-18), E (AQT.AT43.AKT752.-, 17 HCP) had
`gst_rkc_H` at **fit 1.0** — and lost to `rjr_game` (fit 1.0, priority 55 vs 46). The
exact species DECISIONS already names ("wide game raises were shadowing the slam rules by
priority") — this context was missed by that sweep: `rjr_game` is `total_points: [8, 40]`
uncapped. Board 853 is the same seat with 14 total (r26 30 → 4NT correctly stays out;
that 6H is a 28-30 shape slam — acceptable miss). Boards 730/547 are 8-counts accepting
16-18 invitations to 24-26 games that DD failed — the thin-game knob, measured neutral
twice; leave.
**Fix D (this cluster's share):** `rjr_game` priority 55 → 45 (one point below
`gst_rkc_*`'s 46). Nothing else in the context competes (rjr_pass is 0-7 only), the 4M
floor remains reachable for RKC-vetoed hands (rjr_game still spans [8,40]), and a
fit-1.0-vs-fit-1.0 tie now resolves to the ask exactly when the measured r26-31 gate
opens. Boards recovered: 978, 853-no-change, ~11-15 IMPs.

---

## WORST SINGLE BOARDS (first 15)

- **B95 (-15) — IMPLEMENTATION-BUG / MISSING-AGREEMENT (doubled transfer played).**
  Reproduced both seats: 1NT - P - 2H(transfer) - X - P(xd_pass, W) - P - ? leaves E with
  ZERO candidates; fallback PASSED — we played our own doubled artificial 2H, -800-class.
  Twin of review-2's doubled-cue hole; the engine invariant that review recommended
  ("fallback must never pass when the standing doubled bid is our own side's alertable
  call") is evidently NOT implemented — implement it. Author: context
  `1NT - P - 2$t - X - ?` (t = D,H): `trX_complete` = accept the transfer with 3+ in the
  target suit, priority 60; `trX_XX` = 5 good cards in the doubled suit; P = doubleton
  (systemic). And `1NT - P - 2$t - X - P - P - ?`: `trXpp_retreat` = the target suit,
  priority 60, `requires: {}` (mandatory floor). Also recovers cluster 18 (boards 649,
  499, -25, outside my assignment).
- **B89 (-13) — NEEDS-EXCEPTION + MISSING-AGREEMENT.** Reproduced: `ob_1M1NT_4S`
  (requires suits S:[6,13], total 20+) fired holding FIVE spades — the requires-suits
  bound soft-admitted 5 (same unexplained softness review 1 flagged on board 52; worth an
  engine trace). And the honest call (3C jump shift, 18-19, 5-4) does not exist —
  `ob_1M1NT_2C` caps at 17, so the 19-count had no home. Fix G: add
  `evals: {"suit_quality($M)": [1.5, 9]}` to `ob_1M1NT_4$M` and (author)
  `ob_1M1NT_js_3$x`: jump shift in a new suit, `suits: {$x: [4,13]}`,
  `total_points: [18, 21]`, forcing one_round, priority 58 — with responder's simple
  preference floor in a matching context.
- **B149 (-13) & B949 (-13) — IMPLEMENTATION-BUG (RKC 5H/5S replies mis-counted).**
  Reproduced both. The 5H reply shows EXACTLY 2 keycards without the Q; asker (149) held
  2 keycards + the trump Q = four of five accounted, queen located — 6S is the book bid;
  `rkc5H_slam` demands `keycards(agreed): [3,5]` ("all five") so `rkc5H_signoff` fired.
  Identical on 949 with the 5S reply (2 + Q): `rkc5S_slam_S` also demands [3,5]. This is
  the same counting disease the 5D rewrite fixed, unapplied to the exact replies. Fix B:
  `rkc5H_slam` requires → `any_of: [ {evals: {"keycards(agreed)": [3,5]}},
  {evals: {"keycards(agreed)": [2,2], "trump_queen(agreed)": [1,1]}},
  {evals: {"keycards(agreed)": [2,2], "lott_total_trumps(agreed)": [10,26]}} ]`
  (missing exactly one keycard; the queen — held, or covered by a 10-card fit).
  `rkc5S_slam_S`/`rkc5S_slam_H`: `keycards(agreed): [3,5]` → `[2,5]` (the reply carried
  the queen; 2 in hand = one keycard missing = bid it). Endangers nothing: the replies
  are exact counts, these slams are at worst off one ace.
- **B392 (-13) — NOTHING-WRONG.** 1NT-2D-2H-3NT-4H is the textbook sequence; 6H on 29
  is a DD-flattered blast by BEN. Below the measured slam line.
- **B581 (-13) — NOTHING-WRONG (slam-depth structure).** 1H-2H-4H on a 14-HCP 6-5;
  26-27 combined. BEN's limit-raise+blast won a shape slam. Deferred by doctrine.
- **B591 (-13) — NEEDS-EXCEPTION (sharp r26 on RKC).** Reproduced: `gst_rkc_H` (4NT)
  CHOSE over the fit-1.0 4H raise — S's r26 opposite a 6-10 preference (made on a
  DOUBLETON, soft-admitted by rr1H1SD_2H's H:[3,13]) is ~30, a soft miss of the [31,99]
  gate that still outranked the raise; 5H-1 where 4H = par 620. Fix E: make
  `rule_of_26: [31, 99]` SHARP on all four `gst_rkc_*` rules — RKC is the purest counting
  claim in the file; a near-miss on a countable quantity is a different animal (the
  file's own doctrine). Endangers: 0.8-fit shape asks (cluster 8's board 130 never fired
  anyway); measure.
- **B756 (-13) — MISSING-AGREEMENT (advance of partner's weak jump overcall), partial.**
  Reproduced: W (19) over 1H - 3C(partner, weak) - P bid `uc_new_D3` (non-forcing, passed
  out at 3D+2) — `uc_minor_game_5C` r26 29-gate reads a weak-jump floor of ~5 → 26.
  Fix (author): context `1$o - 3$m - P - ?` (partner's jump overcall): `advwj_5$m`:
  `requires: {suits: {$m: [2,13]}, evals: {total_points: [19, 40]}}` priority 62 (playing
  tricks opposite a 7-card suit, not r26); `advwj_4$m` [13,18]; 3NT with
  `weakest_unshown_stopper` sharp + their suit stopped; P floor. Recovers 5C (+400/+600),
  not BEN's 6C.
- **B819 (-13) — NEEDS-EXCEPTION (Stayman-fit slam seam).** Reproduced: after
  1NT - 2C - 2S, E with **17** and four spades PASSED — `stm_raise_4$M` caps hcp at 15
  (E's 17 → 0.8) and the RKC route also mis-scored; both lost to uc_pass 1.0. The
  one-point-seam species. Fix D (share): `stm_raise_4$M` hcp [10,15] → [10,17] (keeps the
  floor), and add `stm_rkc_4NT` in the same `1NT - P - 2C - P - 2$M - P - ?` context:
  `requires: {suits: {$M: [4,4]}, hcp: [15, 17], evals: {controls: [4,12]}}`,
  `establishes: {agreed_suit: $M, asking: keycards, forcing: one_round}`, priority 73
  (above the 4M raise) — 15-17 opposite 15-17 is 30-34, the classic ask-or-cue zone.
- **B845 (-13) — split: Fix K (J9873 five-card 14-count overcall blocked by quality) and
  Fix A** (E sat the balancing X of 2H with AJ4 tripleton — actually the deeper miss was
  the pattern `1H - P - 2H - P - P - X - P - ?` having no advance ladder; the generic
  context covers it — E bids 3C).
- **B868 (-13) — NOTHING-WRONG.** 2C-2D-2NT-Stayman-4S on 30 combined flat; 6S is a
  DD-friendly 5-4 blast below the 33 line. Leave.
- **B949 — see B149.**
- **B986 (-13) — MISSING-AGREEMENT (the uncontested strong jump rebid twin).**
  Reproduced: E (17, AKQJ752) after 1H - P - 1S - P - 2H - P - ? rebid `uc_rebid_S2`
  ([11,40], non-forcing) — the wander 2S/3S/3H/4H followed. Review 2 authored
  `cl_rebid_jump_*` (16-19 jump rebid) for the COMPETITIVE family only. Fix (author):
  `uc_rebid_jump_$s3` twin in the uncontested toolkit: jump own-suit rebid (not
  cheapest_in_suit), `suits: {$s: [6,13]}`, `evals: {total_points: [16,40],
  "suit_quality($s)": [2,9]}`, forcing one_round, priority 31; and cap `uc_rebid_$s2`
  with `not: {evals: {total_points: [16,40], "suit_quality($s)": [2,9]}}`. Partial (game
  the right way up; the 7NT par is out of reach).
- **B375 (-12) — MISSING-AGREEMENT.** Reproduced: 3C - X - P - ? with 5 spades and 1 HCP:
  ZERO candidates, uc_pass sat the takeout double, 3CX made -670. The advance families
  exist for 2-level and 4-level weak bids; the 3-LEVEL was skipped. Covered by Fix A
  (generic ladder; or if the team prefers per-pattern: clone the `2$W - X - P - ?` ladder
  as `3$W - X - P - ?`). Recovers 375 and 961.
- **B548 (-12) — MISSING-AGREEMENT (opener over the 2NT response).** Reproduced: E
  (19, 4=4=4=1) PASSED the 11-12 2NT response — `uc_nt3` hard-blocked by semi_balanced,
  no `1$m - P - 2NT - P - ?` context exists. Fix F: author it: `o2nt_3NT`:
  `hcp: [13, 40]`, `requires` nothing else (partner promised balanced 11-12 with
  stoppers), priority 60; `o2nt_pass` hcp [0,12] floor; `o2nt_4NT_quant` hcp [18,40]
  sharp-r26 31+; `o2nt_3$x` shapely natural tries. 19 opposite 11-12 = 30-31: 3NT floor
  recovers most of the board (+600 vs +180); the quant route may find 6D some days.
- **B636 (-12) — MISSING-AGREEMENT (redouble continuations).** Reproduced: after
  1C - X - XX - 1H, opener (KQT3.AJ.93.KJT85, 14) jumped 3NT via `cl_nt3` while the
  fit-1.0 1S (uc_new_S1, priority 25) lost on priority. After partner's 10+ XX the
  auction belongs to us: author `1$m - X - XX - <their 1-level bid> - ?`:
  `rdxc_1$M`: 4+ cards natural, `requires: {suits: {$M: [4,13]}}`, priority 60;
  `rdxc_X`: penalty, `standing_suit_length: [4,13]` + quality; `rdxc_pass`: forcing-ish
  floor priority 55 (partner speaks again); NO notrump jump below 18. 4S (par 620)
  becomes reachable via 1S - raise.

---

# FIX LIST (deduplicated, priority order)

**A. Generic pull/sit context for partner's double** — the structural fix
(clusters 4 & 9 + boards 596, 845, 375, 961, 620; corroborated by cluster 14)
   - Engine: new SHARP evaluator `standing_suit_length` = cards held in the strain of the
     standing (doubled) bid. (Also fixes `ch_penalty_X`, below.)
   - New context, generic pattern `... - X - P - ?` (partner doubled, RHO passed),
     `when: { we_hold_contract: false }`, placed so every existing authored advance
     context shadows it per-call:
     - `adx_pull_$s` (each strain, each level 2-5 via cheapest_in_suit): 4+ cards
       (5+ at the 4-level), `evals: {standing_suit_length: [0, 2], total_points: [0, 11]}`,
       priority 55-59 (majors first), non_forcing. Include `my_suit` variants (6+ cards,
       requires {} beyond length) so a preemptor/overcaller retreats to his own suit.
     - `adx_nt`: natural, `weakest_their_stopper: [0.9, 9]` sharp, hcp 9-12.
     - `adx_sit` P: priority 61, `requires: {evals: {standing_suit_length: [3, 13]}}`
       plus `features: ["two_of_top3(standing)"]`-equivalent (trump quality — the
       review-1 doctrine for penalty passes). Without it, pass falls to the generic
       floors only when no pull rule matches.
   - Boards recovered: 443(-14), 165(-12), 238(-11), 799(-11), 364(-15), 576(-14),
     762(-12), 596(-14), 845(-13 part), 375(-12), 961(-12), 620(-8 part) ≈ **145 IMPs
     touched** (expect 60-90 realized; several are partial).
   - Endangers: genuine penalty conversions (the trump-quality sit gate is the guard);
     interactions with authored negative-double interpretation contexts (they shadow
     per-call — verify with the `1$m - 1$M - X - P - ?` family); re-measure doubles-made.

**B. RKC 5H/5S reply counting** (boards 149, 949; 26 IMPs)
   - `rkc5H_slam`: keycards [3,5] → `any_of` [3,5] OR ([2,2] + trump_queen [1,1]) OR
     ([2,2] + lott_total_trumps(agreed) [10,26]).
   - `rkc5S_slam_S`, `rkc5S_slam_H`: keycards [3,5] → [2,5].
   - Endangers: nothing — the replies are exact counts; worst case is off one keycard,
     the standard position.

**C. `gf_3NT` gates** (cluster 3 + board 344B; ~60 IMPs touched)
   - Add `evals: { weakest_unshown_stopper: [0.9, 9] }` (sharp) and
     `not: { evals: { longest_suit_length: [6, 13] } }` to `gf_3NT`.
   - (Author, second wave) responder rebids after `2C - P - 2D - P - 2$M`: raise w/ 3+,
     cheap 5-card suits at total_points 4+, 2NT floor.
   - (Author, optional) `qr3_4$s_nat` in `quant_raise_of_3NT`: 6+ own suit, 20+ total,
     forcing — opener's monster moves over 3NT (board 506).
   - Endangers: stopper-less GF hands re-route via `gf_2NT_natural`/suit generics —
     confirm floors; re-measure the 3NT frequency.

**D. Game raises stop shadowing the slam machinery** (cluster 10, board 819; ~25 IMPs)
   - `rjr_game` priority 55 → 45 (below gst_rkc 46).
   - `stm_raise_4$M` hcp [10,15] → [10,17]; add `stm_rkc_4NT` (4-4 fit, hcp [15,17],
     controls [4,12], agreed_suit $M, priority 73) in `1NT - P - 2C - P - 2$M - P - ?`.
   - Endangers: RKC-vetoed voids etc. keep their 4M floor (ranges deliberately still
     overlap — cap by priority, not by range: the file's own "split range keeps its
     backstop" lesson).

**E. Sharp rule_of_26 on the counting claims** (cluster 6, board 591, uc_nt3 hygiene;
~50 IMPs)
   - `qr3_4NT_quant`, `qr3_6NT`: rule_of_26 sharp (and consider 30 → 31 on the 4NT).
   - `gst_rkc_C/D/H/S`: rule_of_26 [31,99] sharp.
   - `uc_nt3`: weakest_their_stopper [0.9, 9] sharp (board 961's J83 "stopper").
   - Endangers: borderline-30/31 invites and shape asks the soft gates used to admit —
     doctrine says drop them; run paired.

**F. "Invitation/response answered by silence", round 3** (boards 548, 909, 573; ~34 IMPs)
   - Context `1$m - P - 2NT - P - ?`: 3NT hcp [13,40]; pass [0,12]; 4NT quant 18+ sharp;
     shapely 3$x tries.
   - Context `1$m - 1$v - 2NT - P - ?` (competitive twin): 3NT 13+ or 11-12 with a
     quality 6-card minor; pass floor.
   - Context `1$m - 2$y - X - P - 3$m - P - ?` (doubler's rebid over the minimum):
     3NT 12+ with their suit stopped (no semi_balanced); pass floor; 3$M 5+.
   - Endangers: nothing existing — uc_pass owns all three seats today.

**G. `ob_1M1NT` strong rebids** (board 89; 13 IMPs)
   - `ob_1M1NT_4$M`: add `evals: {"suit_quality($M)": [1.5, 9]}`; trace why
     `suits: {$M: [6,13]}` soft-admitted a 5-card suit (recurring, see review-1 board 52).
   - Author `ob_1M1NT_js_3$x` jump shift: 4+ suit, total [18,21], forcing one_round,
     priority 58, with responder's preference floor context.

**H. Doubled-transfer retreat + fallback invariant** (board 95; 15 IMPs, plus cluster 18's
25 outside this assignment)
   - Contexts `1NT - P - 2$t - X - ?` (complete with 3+; XX with 5 good; pass = 2) and
     `1NT - P - 2$t - X - P - P - ?` (mandatory retreat floor, requires {}).
   - Engine: implement the review-2 invariant that was recommended but is still absent —
     fallback may never PASS when the standing doubled bid is our own alertable call; and
     when inventing a forced bid, prefer the hand's longest suit (596's 4S-on-T63 with an
     8-card diamond suit in hand).

**I. Pull partner's 3NT with a freak major** (board 101; ~8 of 12 IMPs)
   - In `quant_raise_of_3NT`: `qr3_4$M`: `when: {my_suit: $M}`, `requires: {suits:
     {$M: [7,13]}, evals: {total_points: [0,14]}}` → 4$M sign_off, priority 41.
   - Endangers: pulling a making 3NT — with seven of them, the odds are the pull's.

**J. Small authored contexts** (~35 IMPs total, all currently pass-floor seats)
   - Redouble continuations `1$m - X - XX - <bid> - ?` (board 636): natural 1-level
     4-card suits, penalty X, forcing pass floor; no 3NT jump under 18.
   - Advance of partner's weak jump overcall `1$o - 3$m - P - ?` (board 756): 5$m on
     19+ total, 4$m 13-18, stopper-gated 3NT, pass floor.
   - `uc_rebid_jump_$s3` uncontested strong jump rebid + cap `uc_rebid_$s2` at 15 when
     quality 2+ (board 986) — mirrors the authored `cl_rebid_jump_*`.
   - Weak-2 ask continuation `2$W - P - 2NT - P - 3$W - P - ?` (board 628): pass floor,
     raise 15+, 3NT only with unshown suits stopped (sharp).
   - `aw2r_responsive_X`: add `hcp: [8, 40]` and deny a 6+ suit (board 759).
   - `uc_pref_game_4$M` GF doubleton preference (board 298).
   - `ch_penalty_X`: `"suit_length(their)": [3,13]` → `"standing_suit_length": [3,13]`
     (board 799 doubled hearts holding a heart void; the gate read clubs).
   - Optional hygiene: sharp `semi_balanced` on `ob_1NT` (board 829).

**K. 1-level overcall quality waiver — STYLE, measure before keeping** (boards 381,
845-part; ~15 IMPs)
   - `oc1x_1H/1S`: `any_of` waiver: 6+ cards with hcp 10-16, or 5+ cards with hcp 13-16,
     no suit_quality gate in the waiver branches.
   - Endangers the measured overcall discipline; this is the only fix here that brushes a
     measured style knob — paired run mandatory, revert if negative.

**Deliberately NOT chased (NOTHING-WRONG):** cluster 8 entire (25-30 HCP shape slams
behind the measured r26-31 line; the cue/signoff machinery behaved exactly as designed on
every reproduced board); cluster 1's defensive long tail and boards 261, 808, 857
(opponent style and one-point overcall seams, measured territory); singles 392, 581, 868
(sub-33 blast slams DD happened to pay), 930 (BEN's 28-HCP 6NT), 829 (correct
invite-decline, DD paid the other room). The slam gap these boards represent is the
known structural pocket; the honest lever is Fixes B/D/E (count correctly, stop shadowing
the ask), not loosening the measured 31-point line.
