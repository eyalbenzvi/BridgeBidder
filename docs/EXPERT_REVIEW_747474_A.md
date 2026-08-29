# Expert review A — clusters 1-10 and the worst singles (seed 747474, -726 IMPs)

Method note. The dossier ranks rules by par loss on losing boards only. Before believing
any indictment the reviewer re-scored every candidate rule across all 2000 tables of
reports/e6_before.jsonl (winners included), and reproduced every decision through
choose_bid. Two early hypotheses died on that data and are reported as non-findings.

Mechanical caveat: the dossier's `rule` field is the PRIMARY READING (the highest-priority
same-call rule), not necessarily the rule whose constraint actually matched. Same-call
rules merge into a disjunction and the fit is the max.

## CLUSTER 1 - all-pass, 28 boards, 140 IMPs - NOTHING-WRONG (VERIFIED)
Across all 2000 tables the all-pass family is 548 tables, +1538 IMPs, 264 wins to 84
losses, mean +2.81/table. The single most profitable family in the engine. The 28 losing
boards are the defensive long tail. Board 763: the only non-pass candidate is a penalty
double at fit 0.00; ch_new_C4 is withheld by partner_has_acted:true, which DECISIONS
records as the round-3 repair for a -1100 phantom sacrifice. Board 766: both passes are
in range (a 2-level overcall wants 11-17, the hand has 9). No fix.

## CLUSTER 2 - uc_nt3, 17 boards, 96 IMPs - IMPLEMENTATION-BUG (ceilings upstream) (VERIFIED)
52 last-bids, -217 IMPs, 34 losses / 3 wins. DO NOT touch the strength gate: DECISIONS
already measured 24->26 at +1 IMP. uc_nt3 fits 1.00 on almost every loser; it is the only
rule that fits. The disease is upstream and it is round 6's species - CEILINGS:
  286 (-12) J963.AKQ3.QT.AQ9 18 HCP 4-4 majors  ob1C1D_1H  cap 12-17  fit 0.80 -> 3NT
  599 (-13) K2.AQJ75.A7.A764 18 HCP 5-4        ob_1H1S_2m cap 12-17  fit 0.80 -> 3NT
  683 (-11) 98.AKQ93.AKJ5.A5 21 HCP 5-4        ob_1H1S_2D cap 12-17  fit 0.03 -> 3NT
Board 286 is the clearest indictment: opener bids 3NT over a 1D response holding four
hearts and four spades, because his 18th point puts him one over the ceiling of the only
rule that would have bid 1H. ob1C1D_2NT (18-19 bal) explicitly denies a four-card major,
so 18-19 with a major is a range with no rule.

## CLUSTER 3 - uc_raise_S4, 14 boards, 65 IMPs - NOTHING-WRONG (mostly) + one honesty bug (VERIFIED)
42 last-bids, -139 IMPs. Most is the thin-game dribble DECISIONS already scoped out. No
threshold proposed. But one sub-family is a descriptor-honesty bug: uc_raise_S4's real
gate is lott_total_trumps(S) >= 8 (sharp), counting partner's shown minimum length. On
boards 767 (-9) and 749 (-12) partner had FIVE spades and bid a call that promises SIX.
rr1H1SC_2S requires S:[6,13]; board 767 East held 76542 and bid 2S at fit 0.35 (soft-miss
lottery); West read six, counted 2+6=8 trumps, raised to 4S with KT. 4S made seven tricks.

## CLUSTER 4 - balhigh_reopen_X, 6 boards, 62 IMPs - IMPLEMENTATION-BUG (VERIFIED). HIGHEST VALUE.
18 tables, -89 IMPs, mean -4.94, 13 losses / 4 wins.
ballow_reopen_X (their bid below 3C): hcp [16,40], max_their_suit_length [0,2]. No light branch.
balhigh_reopen_X (their bid 3C and above): the same PLUS hcp [12,40] with
max_their_suit_length [0,1] - "extreme shortness reopens a level lighter."
THE LIGHT BRANCH IS ON THE WRONG SIBLING. Balancing a king lighter is a one- and two-level
agreement; at the three level the double commits partner to the FOUR level, and partner -
who has passed throughout, so adx_pass_min (0-11) fits 1.00 - converts it. Every such
double is a penalty double made on takeout shape, i.e. made BECAUSE we have no trump tricks.
Reproduced: 824 doubles 3S on a stiff king with 14; 181 doubles 4S on a stiff king with 17;
918 doubles 3C holding a CLUB VOID; 6 doubles 3H on Q3. All four contracts made.
  light branch (12-15 + singleton/void): 9 tables, -51 (7 losses, 2 wins of +2)
  16+ branch:                            9 tables, -38 (5 losses, 4 wins)
Rescoring the doubled contracts as undoubled gives a measured +45 IMPs if all removed.
Second half: standing_bid_level [3]. YOU CANNOT TAKE OUT A FOUR-LEVEL CONTRACT - partner's
answer is at the five level.

## CLUSTER 5 - uc_nt2, 9 boards, 51 IMPs - NOTHING-WRONG / symptom (VERIFIED)
14 last-bids, -50, 10 losses / 2 wins. Five of nine are one auction, 1m-(1D)-X-P-2NT,
splitting -13/+6 - noise. uc_nt2 fits 1.00 on all of them. No fix.

## CLUSTER 6 - open_1NT, 9 boards, 48 IMPs - NOTHING-WRONG (VERIFIED)
40 last-bids, -54 IMPs, 19 losses to 15 wins, mean -1.35 - the flattest distribution of
any cluster. Chasing these is how rules rot.

## CLUSTERS 7 & 9 - rkc5C_slam / rkc5H_slam (and rkc5D_slam), 86 IMPs - SPLIT (VERIFIED)
Whole-corpus: 27 slams bid, 18 made. <=27 combined HCP: 10 bid, 4 made (40%).
28+: 17 bid, 14 made (82%).
(a) The keycard arithmetic is correct - not proposing to change it. The failures are hands
    that had the aces and not the tricks.
(b) Board 287 (-13) is an upstream bug: East bids 3H over 2C-2D-2S-2NT-3C holding T982 -
    four small hearts - at fit 0.35, because the seat is starved (uc_rebid_D3 wants six
    diamonds and East has AKQ62). West reads five hearts, lott_total_trumps(H) returns 8
    holding AK7, and gst_rkc_H bids 6H on a 4-3 fit. The keycard machinery is downstream
    of a lie. Same species as cluster 3.
(c) Four "losses" are not losses: boards 549, 362, 811, 416 bid a slam that made THIRTEEN
    tricks - the grand was available. DECISIONS deliberately skipped the 5NT king ask.
    ~-46 IMPs of these two clusters is that decision, not a defect.
(d) One real counting gap in the 5D ladder - board 55, see fix 5.

## CLUSTER 8 - fallback, 4 boards, 42 IMPs - MISSING-AGREEMENT (VERIFIED, no patch proposed)
4 tables, -48 IMPs, mean -12. Boards 422 and 101 are the same shape: a game-forced auction
with no landing rung, so the engine walks 3C-3D-4C-4D-4H inventing a suit at each turn.
Board 422 plays 4H in a 1-2 fit holding AKQT63 clubs opposite a strong 2C opening with 2220
available. The fix is a landing context for 2C-2NT(positive) continuations - a whole family.

## CLUSTER 10 - uc_rebid_C3, 4 boards, 36 IMPs - MISSING-AGREEMENT (VERIFIED)
8 tables, -62 IMPs, 7 losses, 0 wins, mean -7.75. Seven of eight are one position:
responder invites with a natural 2NT in a minor-opening auction and OPENER HAS NO CONTEXT
AT ALL, so the generic 3m rebid fires - non-forcing - and is passed out.
1H-1S-2m-2NT has a context; 1m-1M-2m/1S-2NT has none.
Board 500: East holds A632.A2..AKQT654 - 17 HCP, seven clubs, a DIAMOND VOID - and bids 3C,
passed out, with 6C cold (13 tricks). Every uc_rebid_$m4 rung carries cheapest_in_suit:true
and 3C is the cheapest, so the "level follows the values" ladder can never climb.
The reviewer prototyped a four-rung context and CUT IT BACK TO ONE RUNG, because the
pass-versus-3m question genuinely splits the corpus (board 715 wants 3C, board 541 wants
pass) and would be a gate justified by two boards pointing opposite ways.

## WORST SINGLE BOARDS
144 (-13) IMPLEMENTATION-BUG (ceiling). After 1NT-2C-2S responder holds KQ2.AQ62.A843.K2 -
    18 HCP, no spade fit - and PASSES 2S. stm_3NT_nofit caps at 15 and stm_rkc_4NT needs a
    4-4 fit, so 16+ with no fit has no rule and uc_pass fits 1.00. 6NT is cold. VERIFIED.
55 (-13) IMPLEMENTATION-BUG (counting gap). RKC 5D reply. South holds ONE keycard,
    rule_of_26 = 38, partner has shown 19+. Partner's "0 or 3" cannot be 0 - the pair holds
    4 of 5 - but rkc5D_slam has branches only for 4+ and for exactly 2, so the requires:{}
    signoff fits 1.00. VERIFIED; fix verified -> 6H (makes 12).
969 (-13) IMPLEMENTATION-BUG. West responds 1H holding SIX SPADES AND SIX HEARTS. r1m_1H
    accepts suit_diff(H,S) >= 0; r1m_1S demands >= 1. "Higher of equal length" is already
    the system's opening rule and was never carried to the responses. 6S made 12 at the
    other table. VERIFIED; fix verified -> 1S, 4-4 still 1H, 5-4 each way unchanged.
974 (-14) MISSING-AGREEMENT. Partner's negative/responsive double of 2S is PASSED FOR
    PENALTY by the 2C overcaller holding AJ7642 and two small spades; 2SX made 9 (-670).
    general_pull_or_sit has adx_pull_my_S/H but NO adx_pull_my_C/D; every minor pull rung
    carries i_have_acted:false. VERIFIED; fix verified -> 3C.
83 (-10) MISSING-AGREEMENT (ladder without its answer). After 2NT-3H-3S-3NT (choice of
    games) OPENER HAS NO CONTEXT AT ALL: 4S fits 0.00 and the seat falls to fallback pass
    with three spades and an eight-card fit. The 1NT analogue nt_transfer_3NT_choice exists.
560 (-13) MISSING-AGREEMENT. The takeout doubler (17 HCP, KQJ52) opposite a minimum 3C
    advance has only uc_pass at 1.00. uc_doubler_game_$M exists FOR THE MAJORS ONLY. 6C was
    there. VERIFIED starvation; no patch proposed (needs an answering rung).
987 (-11) MISSING-AGREEMENT. South holds JT3.AK965.4.KJ43 over their weak 2D and PASSES.
    defend_weak_two defines exactly three calls - X, 2NT, and vw2_pass at PRIORITY 30 with
    hcp [0,14]. There is NO NATURAL OVERCALL IN THE CONTEXT; the generic cl_new_H2 fits 1.00
    but sits at priority 26. VERIFIED. Corpus evidence mixed - medium confidence.
20 (-13) NEEDS-EXCEPTION. South asks the weak-two feature 2NT holding a SPADE VOID opposite
    partner's six spades, then bids 3NT. 3H (natural, forcing) fits 1.00 and loses on
    priority. You cannot ask for a feature in a suit you will never play. VERIFIED.
709 (-16) DELETE-THE-RULE candidate (flagged, not patched). qr3_4NT_quant is 7 tables,
    -67 IMPs, ZERO WINS. Board 709 invites 6NT with a nine-card club fit and plays 4NT while
    6C makes 13. Not patched because DECISIONS records that a semi_balanced gate on this rule
    killed five cold 6NTs.
283 (-15) / 403 (-13) NEEDS-EXCEPTION, LOW CONFIDENCE - and the reviewer MEASURED THE WHOLE
    FAMILY AND IT DOES NOT HOLD UP: doubles with a 6+ suit average -2.00/table, doubles
    without average -2.54. Reported, NOT prescribed.
10, 491, 769, 781 NOTHING-WRONG (known pocket: slam over 1NT/2C with a minor or 6-card major).
636, 663 NOTHING-WRONG (3NT vs 5m - DECISIONS: correct percentage bridge).
125, 168, 315, 447, 469, 582, 133, 381, 742, 60 NOTHING-WRONG.
158 (-10) MISSING-AGREEMENT (noted, not prescribed): r1sr_1NT is -41 over 7 tables; the
    missing rung is a minimum diamond preference.
337 (-10) IMPLEMENTATION-BUG (UNTESTED). r1H1S_2NT fired holding a HEART VOID and six
    spades. Needs a trump-length gate. Not reproduced.

# FIX LIST (priority order)

1. balhigh_reopen_X - the light branch belongs to the LOW-level sibling, and a four-level
   contract cannot be taken out. VERIFIED. ~line 10390.
   when: add standing_bid_level: [3]; requires: hcp [16,40], max_their_suit_length [0,2],
   longest_suit_length [0,5]; DELETE the light 12-40/[0,1] branch.
   Removes the double on 824(-11), 8(-10), 181(-10), 358(-9), 766(-8), 550(-5), 312(-4),
   509(-4); converts 918(-14) to a natural 3D. Measured recovery +25 IMPs plus board 8.
   ENDANGERS: 757 (+2) and 870 (+2) become passes. All four 3-level winners retained.

2. Ceilings on opener's cheap ONE-LEVEL new-suit rebid: 17 -> 19. VERIFIED on board 286.
   ob1C1D_1H (~12194) hcp [12,19]; ob1C1D_1S (~12200) hcp [12,19];
   ob_1C1H_1S (~1858) hcp [10,19]; ob_1D1H_1S (~1876) hcp [10,19].
   Bridge: a ONE-LEVEL rebid in a new suit is not limited to 17.
   DELIBERATELY NOT applied to ob_1D1H_2C / ob_1D1S_2C, whose 18-21 band is already covered
   by the 3C jump shift - widening those would DELETE the jump shift (priority 58 vs 57).
   ENDANGERS: generic 3NT/2NT by 18-19 hands holding an unbid four-card major. The 18-19
   balanced 2NT rules already deny a four-card major and sit at lower priority - verified.

3. 1H-1S: the 18-21 jump shift, WITH THE SEAT THAT ANSWERS IT. VERIFIED (hole-fill; no
   measured IMP gain on this corpus - the final contract is still 3NT on 599/683).
   New: ob_1H1S_3C_jump (3C, prio 48, C[4,13], hcp[18,21], not S[4,13], GF)
        ob_1H1S_3D_jump (3D, prio 47, D[4,13], hcp[18,21], not S[4,13]/C[5,13], GF)
   New context responder_after_major_jump_shift, pattern "1H - P - 1S - P - 3$m - P - ?",
   expand m:[C,D], rungs rmjs_6NT_$m / rmjs_4H_$m / rmjs_3NT_$m (3NT carries the full band
   with no shape gate so the new context cannot create a hole).

4. Stayman: responder with 18+ and no fit has no rule. VERIFIED.
   stayman_resp_after_2M (~669) and stayman_resp_after_2D (~649):
   add stm_6NT_nofit (6NT, prio 59, hcp[18,21], $M[0,3], controls[4,12]);
   widen stm_3NT_nofit band [10,15] -> [10,17]; same pair in the 2D-denial context.
   Board 144 (-13) verified P -> 6NT. ENDANGERS: nothing - 6NT is a new rung above an
   existing ceiling and the 3NT widening only reaches hands that currently have NO rule.
   Residual hole NOT fixed: 16-17 WITH a 4-4 fit that fails stm_rkc_4NT's gates.

5. RKC 5D: the one-keycard count. VERIFIED. rkc5D_slam (~4779) + the two minor siblings.
   Add branch: hcp [12,40], keycards(agreed) [1,1], rule_of_26 [31,99].
   Bridge: with one keycard in my hand and a partner who has shown nineteen-plus, "zero or
   three" can only be three - four of five are present and one is missing.
   Board 55 (-13) verified 5H -> 6H, makes twelve. ENDANGERS: nothing subtractive.

6. general_pull_or_sit: I can take partner's double out into my own MINOR. VERIFIED. (~5389)
   adx_pull_my_D (3D, prio 58.5, when my_suit:D + cheapest_in_suit + their_last_bid_suit,
   requires D[5,13]) and adx_pull_my_C (3C, same shape).
   Board 974 (-14) verified P -> 3C. adx_sit/adx_pass_min is -113 over 31 tables.
   ENDANGERS: weak-hand conversions by a player holding five of a minor he has bid. The
   trump-stack sit (adx_sit, prio 61) still outranks it - verified.

7. Opener's answer to the invitational 2NT in the minor tree (THE 5m RUNG ONLY). VERIFIED.
   New context opener_over_invite_2NT_minor, expand_pairs over (m,M,R) =
   (C,H,1S) (C,H,2C) (C,S,2C) (D,H,2D) (D,S,2D),
   pattern "1$m - P - 1$M - P - $R - P - 2NT - P - ?",
   one rung oim2n_5m_$M$R (5$m, prio 61, $m[6,13], hcp[16,21], weakest_unshown_stopper[0,0.5]).
   Board 500 (-16) verified 3C -> 5C; 5C makes thirteen.
   ENDANGERS: trimmed to one rung so it SHADOWS NOTHING - 5C/5D is a call the generic
   toolkit never offers at this node. Verified board 541 unchanged at 3C. The fuller
   pass/3m/3NT ladder was prototyped and WITHDRAWN.

8. defend_weak_two has no natural overcall - the pass floor outranks one. Diagnosis
   VERIFIED, fix UNTESTED. MEDIUM CONFIDENCE - needs the held-out corpus.
   The context defines only vw2_X (70), vw2_2NT (72), vw2_pass (30, hcp[0,14]). Natural
   overcalls come from generic cl_new_* at priority 26 and can NEVER win with <=14 HCP.
   Board 987: 2H fits 1.00 and loses to the pass by 0.01 of blended score.
   Proposed rung vw2_over_$X at priority 31, cheapest level only, 5+ suit, total_points
   [10,40], suit_quality >= 1.5.
   ENDANGERS - PLAINLY: the largest behavioural change in the list and the corpus is
   genuinely split (+38 of wins against -78 of losses in the affected population).
   DO NOT SHIP THIS IN THE SAME MEASUREMENT AS FIXES 1-7.

9. rr1H1SC_2S promises six spades and is bid on five. UNTESTED (diagnosis VERIFIED). ~7673.
   requires: S [5,13] (was [6,13]), H [0,2], total_points [6,10].
   Board 767 (-9). Board 106 (-5) has a genuine six and is unaffected.
   ENDANGERS: the rule becomes a superset so nothing loses a candidate; what changes is what
   partner READS - uc_raise_S4's sharp 8-trump gate now fails on 2+5. Intended.
   NOT proposed: touching the generic uc_rebid_$S3 6-card promise (load-bearing for negative
   inference everywhere).

10. The 2NT transfer's choice-of-games 3NT has no answering seat. UNTESTED (starvation
    VERIFIED). New context nt2_transfer_3NT_choice mirroring nt_transfer_3NT_choice (~1055),
    pattern "2NT - P - 3$T - P - 3$M - P - 3NT - P - ?", expand_pairs (M:H,T:D) (M:S,T:H),
    rungs nt2_choice_4$M (4$M, prio 60, $M[3,5]) and nt2_choice_pass (P, prio 55, $M[0,2]).
    Board 83 (-10). ENDANGERS: nothing; the position currently has no rules at all.

11. The weak-two feature ask with a void in partner's suit. UNTESTED (diagnosis VERIFIED).
    rw2_2NT_ask: add suits { $W: [1,13] }.
    Board 20 (-13). ENDANGERS: only void-in-partner's-suit hands, all of which have a
    fit-1.00 forcing new suit available.

## TWO HYPOTHESES KILLED WITH THE DATA - DO NOT LET THEM BACK IN
1. "A takeout double must not hide a six-card suit" applied to the remaining siblings
   (v3_*_X, oc1C_X, oc1S_X, balhigh_X, ballow_X, cl_takeout_X). Measured across 113
   firings: doubles WITH a 6+ suit average -2.00/table, WITHOUT average -2.54. The gate is
   not supported. Boards 283 and 403 are real losses but the population is not.
2. Tightening uc_nt3's combined-points gate in any form, including deducting distribution
   points from rule_of_26 for notrump. DECISIONS already measured 24->26 at +1 IMP over 51
   changed boards, and the round-6 follow-up measured the estimator repair at -20. uc_nt3
   fits 1.00 on its losers; it is a SYMPTOM of the ceilings in fix 2, not a cause.
