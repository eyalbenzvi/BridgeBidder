# Expert review B — clusters 11-20 + worst singles, second opinion on 1-3 (seed 747474)

Method. Every indictment reproduced through choose_bid/score_candidates before being written
down; every prescription prototyped in a scratch copy and re-run on the motivating boards AND
on 400 random self-play boards A/B against the committed system. The whole fix set changes
14 of 400 boards (3.5%). lint_system: 0 collide / 0 gap / 0 shape / 0 sibling / 0 soft.
fuzz_decisions (500 deals) byte-identical to committed: 0 crashes, 0 empty seats.
Note: the dossier has 20 clusters, not 21.

## CLUSTER 11 - uc_raise_H4, 6 boards, 35 IMPs - NOTHING-WRONG (rule) + one MISSING-AGREEMENT upstream
459 (-10) MISSING-AGREEMENT VERIFIED: "2C - P - 2NT - P - ?" has NO CONTEXT. Worse, the 2C
  opening makes clubs a BID suit, so gf_new_3C's unbid_suit:C can never offer a natural club
  rebid. A 22-count with Q97.AKQ6.A.AK974 had NO candidate above fit 0.35 and won the
  soft-miss lottery with 3H on a four-card suit (gf_new_3H, 5+ required, fit 0.349). Partner
  raised 4H on 742. Contract does not change after the fix - correctness fix, 0 IMPs claimed.
866 (-5) NOTHING-WRONG by the rules as written. rr_raise_inv invites on KJ.QJ86.876532.6
  because total_points = 11 (7 HCP + 3 for a SINGLETON CLUB OPPOSITE A 1C OPENER + 1). The
  bridge error is counting shortness in partner's own suit. Global evaluator change; the class
  DECISIONS Phase-3 and the round-6 follow-up both warn against. One board is not enough.
949 (-5), 478 (-8) NOTHING-WRONG.

## CLUSTER 12 - uc_raise_D3, 4 boards, 28 IMPs - IMPLEMENTATION-BUG (priority inversion) VERIFIED
In general_uncontested_continuation the minor ladder is ordered BACKWARDS:
  uc_raise_C3/D3   3m   prio 31   (invitational, rule_of_26 [22,99] - NO CEILING)
  uc_nt3           3NT  prio 29   (game)
  uc_minor_game_5m 5m   prio 28   (game)
  uc_raise_C4/D4   4m   prio 27
The invitational rung outranks both game rungs AND has no top, so with a minor fit the generic
toolkit CAN NEVER BID GAME BY RAISING. Board 387 candidates: 3D fit=1.00 prio=31 / 3NT fit=1.00
/ 5D fit=1.00 / 4D fit=1.00 - three fitting games, and it bids the invitation. Same on 561.
The MAJORS are ordered correctly (uc_raise_$M4 = 32 > uc_raise_$M3 = 31) - the "gate added to
one rule not added to its sibling" species by another name.

## CLUSTER 13 - cue_H_signoff, 2 boards, 26 IMPs - MISSING-AGREEMENT (missing cue rung) VERIFIED
With hearts agreed the authored cues are 3S / 4C / 4D. There is NO 4S RUNG, so once partner has
cued 4D the only remaining cue (spades) cannot be shown. Board 406: North holds .KT963.J976.AK62
- a SPADE VOID, AK clubs, opposite partner's 4D cue. Candidates: 4H fit=1.00 prio=34 / 4NT
fit=0.00 / 4S fit=0.00. 4NT correctly vetoed by the Blackwood no-void prerequisite (2 keycards),
and the cue floor that veto assumes as its alternative DOES NOT REACH THIS POSITION. Exactly the
caveat DECISIONS records ("a tip that names an alternative tool is only sound where that tool
exists"). The file's comment says a cue chain "can never push past 4M"; that invariant costs the
board. A cue above game is standard and is a slam commitment - gate at rule_of_26 >= 30, not 28.
Board 511 (-13) NOTHING-WRONG: no second-round-control cue exists, so 4H is the only honest call.

## CLUSTER 14 - o2ntj_4S, 2 boards, 25 IMPs - MISSING-AGREEMENT (starved seat), LOW VALUE
"1m - 1M - 2NT - 3M - 4M - ?" has NO CONTEXT: candidates are P fit=1.00 prio=8 (the CODE
fallback) and 4NT fit=0.20. Twelve opposite a shown 18-19 is thirty combined and cannot move.
VERIFIED. But filling it scores IDENTICALLY on board 203 (680 either way) and nothing on 756.
ZERO measured IMPs. Ranked last.

## CLUSTER 15 - gf_3NT, 3 boards, 24 IMPs - IMPLEMENTATION-BUG on 154; NOTHING-WRONG on 565/246
Board 154 (-14) VERIFIED: after 1S - P - 2C - (X), opener holding AKT92.J7653.QJ7. (5-5 majors,
CLUB VOID) bids 2NT. Cause: the whole GF landing family - gf_landing_new_suit, gf_landing_minor,
gf_landing_preference_major, gf_landing_nt - uses pattern "... - P - ?" and therefore DOES NOT
MATCH AFTER A DOUBLE. The one GF landing rule with pattern "... - ?" is gf_2NT_natural (prio 33),
which has NO SHAPE GATE WHATSOEVER. So after their double the GF toolkit collapses to notrump.
The reviewer did NOT repair the pattern coverage (a parallel "... - X - ?" context would shadow
general_their_double and could not be made a provable superset without copying ten rules).

## CLUSTER 16 - cue_S_signoff, 3 boards, 24 IMPs - NOTHING-WRONG / structure this engine lacks
835 (-11) VERIFIED starved: after 1S - 4C(splinter) - 4H(our cue) - 4S(partner signs off), the
cue-bidder's candidates are P fit=1.00 prio=8 and 4NT fit=0.00 (vetoed by no-void, 2 keycards,
heart void). Advancer's 4S is CORRECT - QJ93 opposite a shown heart void is wasted, the
wasted_in_partner_shortness principle the system already encodes. The missing tool is
second-round-control cues at the five level - a structure, not a rule. Declines to touch the veto.
995 (-11) judgment. 534 (-2) noise.

## CLUSTER 17 - rkc5D_slam, 2 boards, 24 IMPs - IMPLEMENTATION-BUG (sibling gate not swept) VERIFIED
rkc5H_slam carries, correctly, "the trump queen must be in my hand or the fit long enough to drop
it - a short fit missing the queen is a trump loser, not a finesse." That clause was NEVER GIVEN
TO rkc5D_slam OR rkc5C_slam.
553 (-13): asker holds 4 keycards, so partner's "0 or 3" is 0 - one keycard AND the trump queen
  are missing, in an EIGHT-CARD FIT. 6S bid, made 11. With the swept gate: 5S making 11 = flat.
962 (-11): the 2-keycards-opposite-shown-values branch, AK9853 + JT4 = 9 trumps, no queen; 6S
  bid, made 11. lott_total_trumps(agreed) reads partner's SHOWN length (8), so it signs off.
MANDATORY COMPANION: on 400 random boards, gating rkc5C_slam WITHOUT widening rkc5C_signoff to
requires:{} left one seat (board #267, a 3-keycard asker) with NO FITTING CANDIDATE and it
invented 5D out of thin air. Precisely the trap DECISIONS records for rkc5H_signoff. SHIP THE
TWO TOGETHER OR NOT AT ALL.

## CLUSTER 18 - ob_1D1H_2C, 2 boards, 23 IMPs - MISSING-AGREEMENT (missing sibling context) VERIFIED
"1D - P - 1H - P - 2C - P - ?" HAS NO CONTEXT. Its sibling "1D - 1S - 2C" was authored (round 5);
so were 1C-1M-2D, 1C-1S-2H, 1H-1S-2C, 1H-1S-2D. Only the 1H version is missing.
Responder falls to the generic toolkit where two rungs interlock badly: uc_rebid_H2 carries
not:{rule_of_26 >= 26}, and the rung above it, uc_rebid_H3, requires cheapest_in_suit which is
FALSE while 2H is still available. So a hand TOO STRONG for the capped 2-level rebid has no rebid
at all. Board 885: responder holds SEVEN HEARTS and 11 HCP; candidates P fit=1.00 / 2H fit=0.100
/ 2D fit=0.134. It passes 2C, down five, while the other table plays 4H making twelve.
THE BEST FIX IN THIS SLICE.

## CLUSTER 19 - open_1C, 3 boards, 22 IMPs - MISSING-AGREEMENT, medium confidence, NOT PRESCRIBED
271 (-6) VERIFIED: after 1C - (1D) - P - (2D), opener holds T84.AT75.A.AKQ73 - 18 HCP - and the
entire candidate list is P fit=1.00 prio=20 and X fit=1.00 prio=9 (the CODE-fallback double).
cl_takeout_X is gated side_has_acted:false, the negative double is gated to my first call, and
cl_rebid_jump_C wants six clubs. There is no opener's second double. NOT PRESCRIBED: it would add
a THIRD meaning to X in a context that already defines two (collide risk), and three consecutive
reviews have found "a sound double answered by nobody".
417 (-7), 587 (-9) NOTHING-WRONG.

## CLUSTER 20 - uc_new_S2, 2 boards, 21 IMPs - same MISSING-AGREEMENT as cluster 18 (188); 205 NOTHING-WRONG
Board 188 is 1D-1H-2C again: responder bids 2S from the generic toolkit and OPENER PASSES IT with
15 HCP and a fit. The fix does not change this board's contract - the failure is one seat later.
No IMPs claimed for 188.

## Worst singles (spot checks)
267-family / 10 / 55: RKC counting auctions; unchanged by this patch. Board 55's 5H signoff is
  read as "the 5D-reply arithmetic working as designed."  [NOTE: reviewer A DISAGREES and verified
  a fix -> 6H making twelve.]
663 (-11) NOTHING-WRONG: gf_game_5C over gf_minor_3NT because neither unshown suit is stopped.
763 (-11) NEEDS-EXCEPTION, NOT PRESCRIBED: spade void, AQ8754, 12 HCP over 2S-P-3S; candidates
  P 1.00 / X 0.00 / 3NT 0.00. ch_new_C4 is gated partner_has_acted:true - the anti-phantom-
  sacrifice guard added in round 3 at a measured cost of -1100. Will not weaken a guard that
  expensive on one board.

## SECOND OPINION - clusters 1-3
CLUSTER 1 all-pass - MISSING-AGREEMENT (two named holes), NOT a long tail. Disagrees with treating
the cluster as homogeneous; three of its four shown boards have three different causes:
 1. The direct defence to a weak two has NO NATURAL SUIT OVERCALL AT ALL. defense_vs_weak2
    contains exactly vw2_X (70), vw2_2NT (72), vw2_pass (30, hcp 0-14). The SIBLING context
    defense_vs_preempt_$W (3C - ? etc.) WAS authored with v3_*_D/H/S overcall rungs. So over a
    weak two the only suit bid comes from the generic toolkit at priority 26, and vw2_pass at 30
    beats it at fit 1.00. VERIFIED: AKJ95.842.K73.94 over 2D passes.
 2. The high-level competitive context never received the long3 rungs its low-level sibling has.
    cl_new_long2_$X / cl_new_long3_$X ("a SIX-card suit, 11+ points") exist in "... - bid<3C - ?";
    there is NO ch_new_long3_$X in "... - bid>=3C - ?", which only has ch_new_$X3 at 14+ points.
    Board 558 VERIFIED: KQT942.QJ85..K63 over 2D-P-3D scores 3S at fit 0.800 (ONE POINT SHORT of
    the 14 floor) and loses to ch_pass at 1.00. Textbook 3S; the other table played 4S making 11.
 3. Board 766 read as NOTHING-WRONG, against the shape of the cluster: sw_2H misses on
    suit_quality and bidding 2H on T8732 is bad bridge; the ten-card fit is a double-dummy artifact.
CLUSTER 2 uc_nt3 - NOTHING-WRONG (the rule); the disease is upstream and it is NOT strength.
  Concurs with A. Adds: on board 302 the 3NT is bid holding KJ DOUBLETON IN THE SUIT THEY
  OVERCALLED at the one level, and weakest_their_stopper passes it. If anything here is worth a
  measured experiment it is the STOPPER THRESHOLD in their bid suit, not the point range - but
  that is a gate on a rule with 96 IMPs and 17 boards of exposure. DO NOT TIGHTEN IT AGAIN.
CLUSTER 3 uc_raise_S4 - mostly NOTHING-WRONG; one genuine MISSING-AGREEMENT.
  332 (-6) MISSING-AGREEMENT: after 1S - (X) - 2NT(Jordan) - P - 3S(opener's minimum), responder
    holds 10 HCP and RAISES TO 4S OVER PARTNER'S SIGN-OFF. The seat 1$M - X - 2NT - P - 3$M - P - ?
    is unauthored, so uc_raise_S4 fires with rule_of_26 = 25. Authoring the seat is additive/safe.
  749 (-12) NEGATIVE RESULT REPORTED: prototyped splitting uc_raise_S4 so the doubleton rung sits
    at 28 (below 3NT) with its gate otherwise verbatim. The board then bids 4C, not 3NT, because
    uc_rebid_C4 also sits at 29 and wins the tie. REVERTED; DO NOT SHIP. The generic ladder's
    29-tie block needs its own ordering pass first.

# FIX LIST (priority order)
1. Author "1D - P - 1H - P - 2C - P - ?" (responder_rebid_1D_1H_2C), the missing sibling of
   1D-1S-2C. Boards 885 (-12), 775 (-11). ~23 IMPs. VERIFIED END TO END.
   Rungs: r1d1h2c_pass (P,50, hcp[6,9] C[4,13]); r1d1h2c_2D (2D,54, hcp[6,10] D[2,13]);
   r1d1h2c_2H (2H,55, hcp[6,10] H[6,13]); r1d1h2c_2NT (2NT,56, hcp[11,12] semi_balanced);
   r1d1h2c_3NT (3NT,57, hcp[13,15] semi_balanced); r1d1h2c_3H (3H,59, hcp[11,40] H[6,13]).
   Deliberately does NOT define 2S - the generic uc_new_S2 already covers it.
   Answering seat EXISTS (verified 885 -> 3H-4H, 775 -> 2S-4S).
   ENDANGERS: the context now interprets P with a narrow gate copied verbatim from the proven
   r1d2c_pass. A/B 2 of 400 boards, both correct preferences.

2. Sweep rkc5H_slam's trump-queen clause onto rkc5D_slam AND rkc5C_slam, and make rkc5C_signoff
   a COMPLETE fallback (requires:{}). Boards 553 (-13), 962 (-11) + A/B board #267. ~24 IMPs.
   VERIFIED. Overlaps cluster 7 (other reviewer).
   Bridge: a keycard is already missing, so the trump queen cannot be missing too unless the fit
   is nine cards.
   ENDANGERS: slams where the asker holds the keycards but neither the trump queen nor a nine-card
   fit - exactly the hands with a likely trump loser. The requires:{} on rkc5C_signoff is NOT
   OPTIONAL: without it the seat is empty and invents a call. rkc5D_signoff is already {}.

3. Re-rank the generic minor ladder so GAME OUTRANKS THE INVITATION. Boards 387 (-6), 561 (-6);
   also relieves cluster 10. ~12 IMPs. Four one-line priority changes:
   uc_raise_C3 31->27, uc_raise_D3 31->27, uc_rebid_C3 29->27, uc_rebid_D3 29->27.
   New order: uc_nt3 (29) > uc_minor_game_5m (28) > three-level minor rungs (27) > uc_pass (18).
   Bridge: with a minor fit the game is 3NT or five of the minor, so three of a minor is where you
   land when neither is available - not your first choice.
   WHY RE-RANKING AND NOT A CEILING: capping uc_raise_D3 at rule_of_26 <= 28 would open a hole
   (29+ combined, unbalanced, under 17 own points, nine trumps fits nothing) and the catch-all pass
   would swallow it. Re-ranking removes no hand's bid, only its preference order.
   ENDANGERS: A/B 6 of 400 boards, all of that shape (3D/3C -> 3NT x5, 3D -> 5D x1).

4. The missing top cue rung: 4S with hearts agreed (cue_H_S4). Board 406 (-13). ~13 IMPs. VERIFIED
   (1H-3S-4D-4S-4NT-5H-6H, making twelve).
   cue_H_S4: call 4S, prio 42, when standing_bid_level[4,4] + cheapest_in_suit + not we_hold_contract;
   requires H[2,13], control_in(S)[2,2], total_points[14,40], rule_of_26[30,99].
   A cue ABOVE game commits to the five level, so 30 combined, not the 28 the below-game cues use.
   ANSWERING SEAT ALREADY EXISTS - slam_try_over_game_raise offers gr_rkc_general_$M, whose gates
   read keycards(agreed)/lott_total_trumps(agreed), and the cue's agreed_suit:H makes those resolve
   to HEARTS not spades. Verified on 406: 4NT -> 5H -> 6H, not 6S.
   ENDANGERS: breaks the file's stated invariant that a cue chain can never push past 4M. A/B 1 of
   400 boards (#168), a good 5H. The one board to watch on the held-out corpus.

5. Author "2C - P - 2NT - P - ?" (opener_rebid_2C_2NT) so the 2C opener can show real clubs.
   Board 459 (-10) - auction becomes honest but the CONTRACT DOES NOT CHANGE, so 0 IMPs claimed.
   Correctness fix. One rung r2cnt_3C_nat (3C, 56, C[5,13], GF).
   ENDANGERS: only the call 3C at this one auction, today a fit-0.35 lottery ticket.

6. Natural suit overcalls of a weak two (the sibling the 3-level preempt defence already has).
   Cluster 1 family + board 987. VERIFIED at the decision level (AKJ95.842.K73.94 over 2D:
   pass -> 2S). New contexts defense_vs_weak2_overcalls2 (2D->2H/2S; 2H->2S) at priority 64 with
   5+ suit, hcp[11,40], suit_quality >= 2; and defense_vs_weak2_overcalls3 (3-level, 6+ suit,
   quality 1.5, quick_tricks >= 2), gates copied from the measured v3_* 3-level defence.
   NOTE: `call: $L$X` DOES NOT EXPAND - tried it, the rules loaded and produced NO CANDIDATES.
   Worth a loader assertion.
   ANSWERING SEAT EXISTS - the generic competitive raise and new-suit ladders advance a natural
   overcall; none of these is artificial.
   ENDANGERS: we enter more auctions over weak twos. A/B 1 of 400 (#139 neutral) + #295 (mildly
   favourable). Vulnerability is NOT in the gate; if it underperforms, that is the first knob.

7. ch_new_long3_$X: the six-card rung the high-level competitive context never got. Board 558 (-11).
   ~11 IMPs. VERIFIED. Insert in general_competitive_high after ch_new_S3, one per suit:
   call 3$X, prio 27, when unbid_suit + cheapest_in_suit, requires $X[6,13],
   total_points[13,40], suit_quality($X)[1.5,9].
   DEVIATION FROM THE SIBLING, STATED PLAINLY: cl_new_long3_$X uses 11 points and quality 1.0.
   This uses 13 and 1.5, set FROM THE A/B, NOT FROM A BOOK. At 11/1.0 the 400-board run produced
   two clear disasters: #58 bid 3S on JT8754 and reached a 4S that should not exist, and #304 bid
   3S on a 9-count into a 2D-2NT-3H auction and WAS DOUBLED. At 13/1.5 both revert and 558 survives.
   THE FIX IN THIS LIST THAT MOST NEEDS ITS OWN HELD-OUT MEASUREMENT.

8. gf_2NT_natural may not be bid with a void. Board 154 (-14). VERIFIED at the decision level
   (2NT -> 2H); the full table-B auction could not be reproduced (the double came from BEN), so the
   IMP claim is UNVERIFIED. Add requires: evals {stoppers(their): [0.5,99]}, not: {evals: {void:[1,1]}}.
   Bridge: the system's own maxim already says no notrump with a void; this rule was the one place
   it was not enforced. void is registered sharp so this is a real veto. A/B 0 of 400 boards.

9. Author the starved seat "1m - 1M - 2NT - 3M - 4M - ?" (LOWEST PRIORITY; MEASURED VALUE ZERO).
   Boards 203, 756. VERIFIED starved; VERIFIED that filling it changes no score (203: 680 either
   way). ENDANGERS: this context is MORE SPECIFIC than slam_try_over_game_raise at this exact
   auction, so it SHADOWS gr_rkc_$M / gr_rkc_general_$M there. It is a superset in the directions
   that matter but does NOT carry gr_rkc_$M's my_suit/partner_last_suit conditions verbatim - "if
   you keep it, add them as a second rung." Would not spend a measurement cycle on it.

## EXPLICITLY NOT PROPOSED (with reasons)
- A reopening/second takeout double for the opener (cluster 19, board 271). Real hole, VERIFIED.
  Adding a third meaning to X inside a context that already defines two invites the collide defect.
- Tightening uc_nt3 again. Twice ruled a symptom; the one gate change measured +1 IMP.
- The uc_raise_$M4 doubleton demotion (board 749). Prototyped, MADE THE BOARD WORSE, reverted.
- Any change to shortness_points (board 866). Correct diagnosis, global blast radius, and the last
  two points-estimator experiments measured -20 and +1.
- Widening partner_has_acted on ch_new_$X4 (board 763). The guard cost -1100 on its motivating board.
- Repairing the "... - P - ?" pattern on the GF landing family (cluster 15). THE DEEPEST FINDING IN
  THIS SLICE - after any double, the entire GF landing toolkit except gf_2NT_natural is unreachable
  - but every repair either shadows general_their_double or requires copying ten rules verbatim.
  Recorded for the next round as a structural item, not patched here.
