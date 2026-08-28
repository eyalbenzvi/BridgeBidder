# Expert review: all 40 losing boards of the 100-board BEN match (-130 IMPs)

Method: every board was read against the actual rule text in
`src/bridgebidder/systems/two_over_one.yaml`; where the mechanism was not obvious from the
text, the decision was **reproduced through `choose_bid`** (boards 38, 26, 36, 65, 1, 12,
92, 23, 77, 30, 66) so the diagnosis below is the engine's real behaviour, not a guess.
Verdicts: IMPLEMENTATION-BUG / NEEDS-EXCEPTION / MISSING-AGREEMENT / DELETE-RULE /
NOTHING-WRONG.

A note on attribution: most of the passes below are attributed to `uc_pass` / `cl_pass` /
`balhigh_pass` etc. Those rules are innocent — they are the permissive floor doing its job.
The diseases are upstream, and they cluster: the same five holes account for well over half
the recoverable IMPs (see Fix list).

---

### Board 13 (-12) — MISSING-AGREEMENT
Table B: W (AK7.6.KQJT83.JT8, 14 HCP, solid-ish 6-card minor) heard partner open 1NT and
had nothing between 3NT (`nt_3NT`) and nothing: the system has no minor-suit slam route
over 1NT (already recorded as a known gap in DECISIONS.md, ~7 slams/1000). BEN bid the
cold 6D. **Fix (author):** over 1NT, with a 6+ card minor headed by 2 of the top 3 and
11+ HCP, a slam-try route: simplest inside the current toolkit is a quantitative 4NT
(hand re-valued: 6-card good minor counts ~3 extra points) plus opener's accept; the full
fix is 2S/3m minor machinery. This is the single biggest authored-structure item.

### Board 38 (-12) — IMPLEMENTATION-BUG
Table B: 1D-1H-2H-4NT(`gst_rkc_H`)-5H(`rkc_5H`, 2 keycards no Q)-**5S(`fallback`)**.
Reproduced: with hearts agreed, asker holding 2 keycards, the only in-context rules are
`rkc5H_slam` (needs 3+ keycards in hand), `rkc5H_signoff` = **5H, illegal over the 5H
reply**, and `rkc5H_pass_signoff` = P — which is **filtered out because `rkc_5H`
establishes `forcing: one_round`**, and the engine hard-filters pass over a forcing call.
Zero legal candidates → the forced-continuation backstop invented 5S (7 tricks).
**Fix:** in `rkc_response`, the 5H reply must not be one-round-forcing on the asker when
the reply *is* the sign-off spot: split `rkc_5H` by `agreed_suit` (with H agreed,
`establishes: { forcing: non_forcing }`), or exempt an explicitly-authored pass rule in the
interpreting context from the forcing-pass filter. Same latent bug for the 5S reply with
spades agreed (`rkc5S_pass_signoff`, priority 40 — verify the filter there too).

### Board 23 (-11) — MISSING-AGREEMENT
Table A: 1H (N) - 1NT overcall (E) - **P (S, `cl_pass`)** with J84.JT863.K.Q874: 5-card
heart support, ~10 support points, and no context exists for "partner opened, they
overcalled 1NT" (no `1$M - 1NT - ?` pattern in the file; reproduced — best alternative was
a 0.8-fit 2H that lost to the perfect-fit pass). NS own 4H (+620/650) and a penalty of
1NT (par +500); we defended 1NT undoubled. **Fix (author):** context `1$M - 1NT - ?`:
X = penalty/values (9+ HCP); 2$M = 5-8 with 3+ support; jump raises preemptive per LOTT
(5 trumps → game-level with shape); new suits natural non-forcing.

### Board 84 (-11) — IMPLEMENTATION-BUG
Table B: 2H - 2NT(ask) - **3NT (`feat_H_3NT`)** on AKT532 and Q52 — "solid suit" fired on
a two-honor suit. Two encodings misfired: (a) `suit_quality(H) >= 3` counts T as 0.5, so
AKT532 = 2.5 and the *soft* sigma let 2.5 pass a gate meant to mean AKQ; (b) the hand
(10 HCP, no outside A/K feature) fits **no** reply exactly — `feat_H_min` is hcp [5,7]
only — the classic range-with-no-rule species, so the least-bad soft match won.
**Fix:** (1) `feat_*_3NT`: require a genuinely solid suit — add `features:
["two_of_top3($W)"]` **and** raise the gate to `suit_quality($W): [3, 9]` with a sharp
sigma, or better add a `top3_honors(suit)` evaluator and require [3,3]; (2) widen
`feat_*_min` to `hcp: [5, 10]` so a maximum with no feature has an honest 3-of-suit reply
(feature rules at priority 60 still outrank it in-range).

### Board 92 (-11) — MISSING-AGREEMENT
Table A: 2S - X (`vw2_X`, fine) - P - **P (N, `uc_pass`)** on 653.K98.Q874.JT4 — advancer
converted a takeout double of a weak two into a penalty pass with three small trumps.
Reproduced: every advance candidate scored 0.0 — there is **no `2$W - X - P - ?` context
at all** (only `1$o - X - P - ?` exists). -670. **Fix (author):** advances of the double
of a weak two: cheapest suit 0-8 (3-level), jump 9-11, cue GF, 2NT natural 8-11 with
stopper, penalty pass only with `suits: {$W: [4,13]}` + `two_of_top3($W)`.

### Board 7 (-10) — NEEDS-EXCEPTION
Table B: 1C - 1D - **3NT (`uc_nt3`)** by W with 18 balanced and four spades. The authored
`ob1C1D_2NT` (18-19 jump) *denies a 4-card major*, `ob1C1D_1S` caps at 17, `ob1C1D_1NT`
caps at 14 — an 18-19 balanced hand with a 4-card major after 1C-1D has no rule, so the
generic 3NT ate it and the auction died (6C cold; BEN bid it). **Fix:** drop the
`not: {suits: {S/H: [4,13]}}` from `ob1C1D_2NT` — over a Walsh 1D, 18-19 balanced rebids
2NT even holding a major (responder with a major would have bid it). Honest caveat: even
after 2NT this 29-HCP 6C is not certain to be reached; expect partial recovery only.

### Board 25 (-10) — NEEDS-EXCEPTION
Table A: 2NT - 3H - 3S - **4S (`nt2_tr_4S`)** on JT632.J97.QJ5.87 (4 HCP, 5332). The
transfer-continuation 4M rule takes any 5+ suit at hcp 3+, and outranks (60 vs 56) the
choice-of-games 3NT which is the textbook call with exactly 5 and a balanced hand (BEN:
3NT +400; we played the 5-2 fit, -50). **Fix:** `nt2_tr_4$M` requires
`any_of: [ {suits: {$M: [6,13]}}, {suits: {$M: [5,13]}, evals: {singleton_or_void: [1,1]}} ]`;
`nt2_tr_3NT` keeps `$M: [5,5]` + `semi_balanced`, floor lowered to `hcp: [4, 40]`.

### Board 28 (-10) — IMPLEMENTATION-BUG (priority inversion) + NEEDS-EXCEPTION
Table A: 1D - 1H - 1S - **1NT (`r1sr_1NT`)** on 7.Q98542.T8.A964 — responder rebid 1NT
with a singleton spade and six hearts. `r1sr_2H` ("to play: 6+ hearts", hcp 6-9) exists in
the same context and fits 1.0 — but sits at **priority 49 below `r1sr_1NT` at 50**. -300
in 1NT while 2H/3H makes (BEN +140). **Fix:** raise `r1sr_2H` to priority 56 (above 1NT
and 2NT), or add `not: {suits: {H: [6,13]}}` to `r1sr_1NT`/`r1sr_2NT`. Secondary (table
B): our sandwich 1NT (`cl_nt1`) on a flat 12 — see the cl_nt1 fix under board 99.

### Board 30 (-10) — MISSING-AGREEMENT
Table A: 1H - 1S - 2D - 2NT(11-12 invite, `rr1H1SD_2NT`) - **P (N, `uc_pass`)** with 17.
Reproduced: no acceptance rule exists for opener over responder's natural 2NT invite after
a two-suited rebid, and the generic `uc_nt3` is blocked by `semi_balanced` (opener is
1-5-4-3). Same species as the two invite-answer contexts already authored (1M-1NT-2m-2NT
and Stayman-invite). **Fix (author):** context `1H - P - 1S - P - 2D - P - 2NT - P - ?`
(expand over the 1M-1x-2y family): P = 12-13; 3NT = 14+; 3-of-a-suit = shapely minimum.
Cluster with board 66 — "invitations answered by silence".

### Board 54 (-10) — NOTHING-WRONG
Table B: after 1D - (1S overcall by partner), E jumped 3NT (`uc_nt3`) on 16 balanced with
AK-fourth in their suit — a mainstream expert action that happened to lose to the 6-2
spade fit double-dummy (3NT 8 tricks, 4S 10). No gate that would redirect this hand to a
cue-then-raise exists without inventing machinery the deficit does not justify. Leave it.

### Board 77 (-10) — MISSING-AGREEMENT
Table A: 1C - X (S, 19) - P - 1S (advancer, 0-8) - **P (S, `uc_pass`)**. Reproduced: the
doubler's rebid family does not exist (no `1$o - X - P - <advance> - P - ?` context); best
candidate was a 0.41-fit 4S. The textbook agreement — double-then-raise shows 17+ — is
absent, so a 19-count with four trumps passed 1S with game on (BEN's doubler jumped to
game on the same cards). **Fix (author):** doubler's rebids after a minimum advance:
raise = 17-19 with 4+ support (jump raise at 19+/20 support pts), cue = GF, new suit =
17+ 5+ cards, 1NT/2NT = 18-19/20-21 balanced. Priority above the generic pass floor.

### Board 2 (-9) — MISSING-AGREEMENT (two halves, same family)
Table A: 2S - X - **P (N, `xd_pass`)** holding KQT92 of spades (5-card support, 11-card
fit): no "partner's weak two was doubled" raise context exists (`2$W - X - ?` absent) —
the preemptive 4S (LOTT, 11 trumps) is the standard action and BEN made it at the other
table. Table B: after 2S - X - 4S, advancer E (11 HCP, AJ9-third of hearts) had no rule
either and sold out to 4S-2 with 6H cold. **Fix (author):** (a) context `2$W - X - ?`:
raise to 3$W 3-8 pts/3 trumps, 4$W with 4+ trumps any weak hand or LOTT 10+;
XX = 10+ defense; (b) advancer-over-their-jump: at matching level, X = responsive
values, 5-of-our-suit with fit + 8+ opposite the 17+/shape double.

### Board 67 (-9) — NEEDS-EXCEPTION
Table A: (3D) - **P (N, `v3_D_pass`)** on AK86.KJ8753.7.74 — 12 HCP, good-enough 6-card
heart suit, textbook 3H overcall (BEN bid it, +480 their way). `v3_D_H` requires
`hcp: [13,40]` **and** `good_suit(H)` (2 of top 3 / 3 of top 5) — KJ8753 fails the honor
census the same way KJ9xxxx failed the preempt gate before it was relaxed. **Fix:** in the
six `v3_*_suit` overcall rules replace `features: [good_suit($s)]` with
`evals: {"suit_quality($s)": [1.5, 9]}` and lower `hcp` to `[12, 40]`.

### Board 16 (-8) — MISSING-AGREEMENT (the "second double" hole)
Table B: 1D - P - P - X (W, 23!) - 2D - P - P - **P (W, `ballow_pass`)**. Reproduced (via
boards 1/12, same mechanism): `ballow_X`/`balhigh_X` carry `side_has_acted: false` — added
to stop triple-doubling — so once our side has acted there is NO authored reopening
double left; the fallback X fits 1.0 but ranks below the pass floor. A 23-count sold out
to 2D with 4H makeable. **Fix:** author `ballow_reopen_X` / `balhigh_reopen_X`:
`when: {their_last_bid_suit: true, side_has_acted: true, we_bid_last: false}`,
`requires: {hcp: [16, 40], evals: {"suit_length(their)": [0, 2]}}`, priority ~41; to keep
the anti-repeat property, add a `my_last_call_was_double: false` engine condition (or gate
on `hcp` 19+ for a second double by the same hand). Recovers with boards 1, 12, 65.

### Board 18 (-7) — NEEDS-EXCEPTION
Table B: 1H - P - P - X - **2D (`xd_second_D2`)** on T754 — opener volunteered a
4-card 10-spot suit at the two level over the balancing double instead of passing with a
balanced 15-count; -150 in 2D. The rule's intent (steer to the right strain over their
balance) is fine but needs a real suit. **Fix:** add
`evals: {"suit_quality($s)": [1, 9]}` to the `xd_second_*` family (an honor in the suit),
leaving pass for balanced hands. Table A (selling to 3H on 23 combined) was correct —
par is -100.

### Board 24 (-7) — MISSING-AGREEMENT (minor)
Table A: 1D - (2S) - X(neg, shows hearts) - (3S) - **3NT (`ch_nt3`)** on a flat 14 with
AT-doubleton stopper and J84 of partner's shown hearts; 4H makes, 3NT -2. No rule prefers
the known 5-3/4-3 major fit once they raise; the competitive 3NT outranked everything.
**Fix (author):** after our negative X showed a major and they raise, opener bids that
major at the cheapest level with 3+ card support and 13+ (priority above `ch_nt3`).
Table B's failure to raise partner's 1S overcall over their negative X (Q94, 10 HCP,
`xd_pass`) is the same "advance over their X" hole as board 2(b) — one authored context
fixes both.

### Board 53 (-7) — MISSING-AGREEMENT
Table A: 1S - P - P - X (balancing) - P - **2NT (`uc_nt2`)** on A62.KJ93.AT97.T6 (12,
four hearts). The advance-of-takeout-double contexts are anchored `1$o - X - P - ?` and do
not match the balancing shape `1$o - P - P - X - P - ?`, so no cue/jump-in-major advance
existed and the generic 2NT buried the 4-4 heart fit (3NT -1; 4H/2H+2 the winning spot).
**Fix (author):** an advance context for the balancing double (same ladder as the direct
one shifted ~3 points: cue = 13+, jump suit = 10-12, 2NT natural 11-13).

### Board 65 (-7) — IMPLEMENTATION-BUG (priority inversion) + the board-16 hole
Table A: 1H - P - P - ? with KQ7.A54.KJ6.AQJ9 (20 balanced, heart stopper): reproduced —
`bal_2NT` (19-21 balanced, the exact description; BEN's choice, → 3NT +400) fits 1.0 but
loses to `bal_X` (priority 70 vs 65). Then over E's 1S runout the balancer passed for the
board-16 reason (no second action once side_has_acted). S's earlier pass with 10 HCP was
correct (my first read of 13 was wrong — verified by engine). **Fix:** raise `bal_2NT`
priority above `bal_X` (e.g. 71), or add `not: {hcp: [19,21], evals: {balanced: [1,1]},
features: ["stopper($o)"]}` to `bal_X`'s strong branch. Plus the board-16 reopen-X fix.

### Board 93 (-7) — NEEDS-EXCEPTION (minor)
Table A: 1S - **X (`oc1S_X`)** on K.AKQJ9.QJ.J9743 — the strong (17+) branch of the
takeout double permits a 5-card major, so a hand with AKQJ9 doubled instead of bidding
2H (the 11-17 `oc1S_2H` fits perfectly but sits at priority 65 vs 72). The rest of the
board is mostly BEN's lighter style (opening A7543.7643.KT7.A in first seat). **Fix:** in
each `oc1x_X` strong branch add `not: {suits: {$M: [5,13]}, features: ["two_of_top3($M)"]}`
for the unbid major(s) — with a chunky 5-carder the suit bid beats the double; a bad
5-carder may still double.

### Board 12 (-6) — MISSING-AGREEMENT (board-16 cluster) + IMPLEMENTATION-BUG (minor)
Table A: P - P - 1C - (3D) - P - P - **P (S, 20 HCP!)**: reproduced — the fallback
reopening X fits 1.0 and still ranks below `balhigh_pass`; no authored second action for
opener over a passed-around jump overcall (board-16 fix covers it; here it is worth
+650 vs +400). Table B: our W with 7 diamonds overcalled **1D** (`oc1C_1D`) because the
weak-jump rules demand `suits: {D: [6, 6]}` — *exactly six, sharp* — so every 7-carder
falls through to a 1-level overcall. **Fix:** (a) board-16 reopen-X; (b) widen the
`oc1x_2y_jump` length to `[6, 7]` (or author 3-level double-jump preempt overcalls for
7-carders, NV quality `suit_quality >= 1`).

### Board 66 (-6) — MISSING-AGREEMENT
Table B: 1S - 1NT - 2H - 3H (invite) - **P (E, `uc_pass`)** with 17 and a stiff club
(~20 support). Reproduced: `uc_raise_H4` is killed by the sharp
`lott_total_trumps(H): [8,26]` — partner's generic 3H raise shows only 3+ trumps, so the
*shown* count is 7 even though the real fit is 8 — and no specific acceptance context
exists for a raise of opener's second suit. **Fix (author):** context
`1$M - P - 1NT - P - 2$x - P - 3$x - P - ?`: 4$x/4$M(game) with 15+ total, pass 12-14.
(Do not weaken the generic lott gate — it was made sharp for good reasons.) Cluster with
board 30.

### Board 83 (-6) — NEEDS-EXCEPTION
Table A: 1S - 2D(partner) - P - **P (S, `uc_pass`)** on J3.Q754.952.AJ42 — 9 support
points, 3-card support: the competitive 3-level raise `cl_raise_D3` needs
`total_points: [10, 40]`, so the standard mixed raise (6-9 with 3 trumps, 8 combined) has
no home and the 0.8-fit raise lost to the perfect-fit pass; at the other table BEN's
overcaller balanced back to 3D and made it (+110 vs our -110). **Fix:** lower the
`cl_raise_C3/D3` (minor) total_points floor to [8, 40] when `lott_total_trumps >= 8` (the
gate already present). Endangers little: LOTT still caps it.

### Board 36 (-5) — IMPLEMENTATION-BUG
Table A: 1D - P - 1S - P - 2C - **X (S, `cl_takeout_X`)** on J6.QT96.AK86.Q86 — 12 flat
with FOUR cards in their first suit. Reproduced: the rule fit **1.00** because
`suit_length(their)` reads only ONE of their suits (here spades, where S held two); with
three suits shown by the opponents the "short in their suit" gate is nearly vacuous.
Partner then had no advance rules for this X and the *fallback* bid 2D — their opened
suit — instead of the 5-card heart suit. **Fix:** (1) add an aggregate evaluator
`max_their_suit_length` (max holding over all their shown suits) and gate `cl_takeout_X`
on `[0, 2]`; (2) fallback layer: never offer a new-suit advance in a suit the opponents
have bid naturally.

### Board 40 (-5) — NEEDS-EXCEPTION
Table A: after 1H - 1S - (2C) - 2D - (3C) - 3D - P, N jumped **5D (`uc_minor_game_5D`)**
on 12 HCP/16 support opposite a 10+ competitive raise (~28 combined, 10 tricks). Unlike
every other game-level raise in the file, `uc_minor_game_5C/5D` has **no `rule_of_26`
gate** — only `total_points: [17,40]` + lott — so it accepts to an 11-trick game on
partscore values. **Fix:** add `rule_of_26: [29, 99]` to `uc_minor_game_5C` and `_5D`
(and keep them ranked below the `gf_minor_3NT` preference). Board recovers ~5.

### Board 51 (-5) — NOTHING-WRONG
4S on 25-26 combined after 1C - 1S - (1NT) - 2S: `uc_raise_S4`'s `rule_of_26: [25,99]`
fired exactly as designed; BEN invited and stopped, and double-dummy said 9 tricks. This
is the "thin-game dribble" the project has twice measured as tuning-neutral (Phase 3; the
24→26 NT-gate revert). Do not chase it on one board.

### Board 99 (-5) — IMPLEMENTATION-BUG
Table A: 1H - X - 1S - **1NT (S, `cl_nt1`)** on 43.K762.QJ654.Q4 — no spade stopper.
`cl_nt1/cl_nt2/cl_nt3` (and the `ballow_nt*` copies) still gate on `stoppers(their)`,
which reads only their FIRST suit (hearts, stopped) — exactly the unswept residue
DECISIONS.md flags ("stoppers(their) still reads only their first suit everywhere except
the two generic notrump rules"). Partner then trusted "8-11 with stoppers" and drove to a
hopeless 3NT (`cl_nt3`). Also `cl_nt1`, unlike nt2/nt3, lacks `side_has_acted: true`, which
is how it fired as a live *sandwich* 1NT on flat 8-12 hands (boards 28, 77). **Fix:**
in `cl_nt1/2/3` and `ballow_nt1/2/3` replace the `stoppers(their)`+`stopper(their)` pair
with `weakest_their_stopper: [0.9, 9]` (as `uc_nt2/3` already do), and add
`when: {side_has_acted: true}` to `cl_nt1`.

### Board 6 (-4) — NOTHING-WRONG
Both tables landed one trick from par (-80/-70 vs par -80); the "silent" 18-count at
table A scored par by passing — acting would have done worse double-dummy. 4 IMPs of
partscore-wobble variance. Leave every rule alone.

### Board 15 (-4) — MISSING-AGREEMENT (board 92's twin)
Table A: 2D - X - P - **P (N, `uc_pass`)** on Q985.QJ73.T.QT86 — advancer passed the
takeout double of a weak two with a stiff trump (it lucked into +500, but the vul game
was on: BEN +630). Identical hole to board 92: no `2$W - X - P - ?` context. Same fix.

### Board 26 (-4) — MISSING-AGREEMENT
Table B: passed out with E holding AJ32.T92.AQ542.5 — 11 HCP, rule of 15 = 15.
Reproduced: the only 4th-seat rule-of-15 opening in the file is `open_1S_rule15`
(**5+ spades only**); `open_pass` (0-11) fits 1.0 and won. BEN opened 1D and made +140.
**Fix (author):** `open_1D_rule15` (and 1C/1H analogues): `when: {opening_seat: [4]}`,
`requires: {hcp: [10, 11], evals: {rule_of_15: [15, 30]}}` + better-minor/major-length
conditions mirroring the 1st/2nd-seat shape gates.

### Board 5 (-3) — MISSING-AGREEMENT (board 2 cluster)
Table B: 2S - X - **P (E, `xd_pass`)** with KQ4-third of spades and 11 HCP — the
missing "partner's weak two was doubled" raise ladder again (3S here blocks BEN's 3H,
worth ~3). Covered by the board-2(a) fix.

### Board 9 (-3) — NEEDS-EXCEPTION
Table A: 1H - (1S) - P - P - **1NT (S, `ballow_nt1`)** with SIX hearts (987642). The
6-card rebid `ballow_rebid_H2` exists but requires `suit_quality(H): [1, 9]` and this
suit has literally no honor → 0.8 fit lost to the 1.0-fit 1NT (semi_balanced admits
6322). A reopening 2H on six trumps beats 1NT on any suit quality. **Fix:** drop the
`suit_quality` floor from the `*_rebid_*2` (cheapest own-suit rebid) rules — six cards
is the credential; and/or add `not: {suits: {H:[6,13]}} / {S:[6,13]}` style 6-card-suit
denial to `ballow_nt1`/`cl_nt1`.

### Board 33 (-3) — NEEDS-EXCEPTION (low confidence)
Table B: our N-hand equivalent (12 HCP, doubleton heart) passed out BEN's 3H where BEN's
N doubled our identical 3H and reached +140. `balhigh_X` requires 14+ over a 3-level
preempt even in the pass-out seat; "a king lighter" balancing says 11-12 with perfect
shape is normal there. **Fix (small, measure it):** in `balhigh_X` add a pass-out-seat
branch `hcp: [12, 40]` with `suit_length(their): [0, 2]`. Risky — only 3 IMPs here.

### Board 39 (-3) — MISSING-AGREEMENT
Table B: 1D - (3C jump overcall) - **P (E, `ch_pass`)** on AT985.Q652.5.AJ7 — 11 HCP,
5-4 majors, stiff diamond. The system card says "negative doubles through 3S" but the
generic `cl_negative_X2` stops at `standing_bid_level: [2]`, and the free 3S needs 14+
points; nothing fired and 4S (+420) was missed. (N's earlier failure to preempt 3C over
1D on a 7-card suit is the board-12(b) jump-overcall length issue plus its quality gate.)
**Fix:** add `cl_negative_X3` (standing_bid_level [3], hcp [10, 40], same shape gates) —
and a free-bid rule: new 5-card major at the 3-level over their jump overcall, 10+ HCP,
`suit_quality >= 1.5`.

### Board 42 (-3) — NEEDS-EXCEPTION (cosmetic)
Table B: after partner's sandwich X of 1D-P-1S showing the round suits, W advanced 2C
from 4-4 (J763 clubs vs Q852 hearts) because clubs is cheapest; the major is the standard
preference. Net swing on the board ~0 (both tables were one down). **Fix:** in
`advsw_*` pairs, prefer the heart advance on equal length (add
`evals: {"suit_diff(H,C)": [0, 13]}` to the 2H rule and give it the higher priority).
Otherwise this board is variance.

### Board 48 (-3) — IMPLEMENTATION-BUG
Table B: 1NT - X (us, penalty) - P - P - XX(SOS) - **2H (W, `rr_run_H2`)** — the PENALTY
DOUBLER ran from his own double. The `rr_run_*` family ("answering partner's takeout
double after their redouble") keys only on `we_bid_last: false`, which is also true of
the doubler himself, and it cannot tell a takeout double from a penalty double of 1NT.
**Fix:** add `i_have_acted: false` to every `rr_run_*` `when:` clause — the runner must
be the hand that has not yet chosen a call; the 1NT-doubler then passes (or doubles the
runout) as intended.

### Board 52 (-3) — NEEDS-EXCEPTION
Table A: 1S - (2C) - 2S - (X responsive) - **3S (`xd_rebid_S3`)** on a 5-card suit and a
flat minimum (the rule text demands 6+ sharp — the call got through on the blended path,
worth an engine trace) at unfavourable, 8 trumps at the 9-trick level; -200 against
their 3H making 140. **Fix:** add `evals: {"lott_total_trumps($s)": [9, 26]}` to
`xd_rebid_*3` (LOTT is exactly the tool for this call), which also stops the 5-card
firing; and verify why a sharp `suits: {S: [6,13]}` miss survived candidate selection.

### Board 1 (-2) — MISSING-AGREEMENT (board-16 cluster)
Table B: 1H - (3D) - P - P - **P (E, `balhigh_pass`)** with 17 and six hearts.
Reproduced: the fallback reopening X fits 1.0 but ranks below the pass; the authored
`balhigh_X` is blocked by `side_has_acted: false`; the own-suit rebid 3H sits at 0.8 fit
(its `rule_of_26: [22,99]` reads partner as 0) and loses the blend. The board-16
reopen-X fix covers it; additionally, drop `rule_of_26` from the `ballow/balhigh_rebid_*`
rules (in a balancing seat partner's shown floor is always ~0, so the gate blocks every
reopening rebid; `total_points` already scales the level).

### Board 8 (-2) — NEEDS-EXCEPTION (minor)
Table A: after 1D - (X) - 1H - (X) - P - 1S - P - 2S, S volunteered **2NT (`cl_nt2`)**
on 12 opposite a 6-count 1H bidder (rule_of_26 = 20 vs the [21,99] gate — a soft
one-point miss fired anyway), minus 200. **Fix:** make the `rule_of_26` gate on
`cl_nt2/cl_nt3` effectively sharp (competitive free NT bids are counting claims, not
estimates) — e.g. raise `cl_nt2`'s gate to [22, 99] so a one-point soft miss still fails.
Low priority; 2 IMPs.

### Board 10 (-1) — NOTHING-WRONG
BEN's 11-HCP 3D overcall of our disciplined vul weak two happened to land on its feet
(down 2 undoubled vs our -140 defending 2S). Both of our calls were textbook. Variance.

### Board 70 (-1) — NOTHING-WRONG
We bid 1D - 1S - 1NT - 4S (making) with the 6-4; BEN checked back, found the 4-4 hearts,
and made one more trick. New-minor-forcing/checkback is a deliberately scoped-out
convention (DECISIONS.md); one IMP on one board does not reopen that decision.

---

## Fix list (deduplicated, priority order)

Recoverable ≈ 75-90 of the 130 IMPs are touched by items 1-8; the rest is variance or
style. "Endangers" = boards/behaviours to re-measure after the change (run the fixed
corpus paired, as usual).

**1. Author the "double of a weak two" family — `2$W - X - P - ?` and `2$W - X - ?`**
(MISSING; boards 92, 15, 2, 5; ~25-27 IMPs)
   - Advance context `2$W - X - P - ?`: cheapest-suit advance 0-8 (any 4+ suit, majors
     first), jump 9-11, cue GF, 2NT 8-11 w/ stopper; penalty pass ONLY with
     `suits: {$W: [4,13]}` + `features: ["two_of_top3($W)"]`.
   - Preemptor's-side context `2$W - X - ?`: 3$W = 3+ trumps 0-8 pts; 4$W = 4+ trumps
     (LOTT 10) any strength or 5+ trumps; XX = 10+.
   - Also the advancer-over-their-jump continuation (2$W - X - 4$W - ?): X = responsive
     8+, 5-level suit bid with 4+ card fit and 8+.
   - Endangers: nothing existing (the position currently has zero rules). Watch the
     DECISIONS precedent that passing the double of a *3-level* preempt is often right —
     that logic does NOT carry to the 2-level without trump tricks.

**2. Re-open the "big hand's second action" — reopening double once our side has acted**
(MISSING; boards 16, 12, 1, 65-second-half, plus 77's cousin; ~15-20 IMPs)
   - New `ballow_reopen_X` / `balhigh_reopen_X`:
     `when: {their_last_bid_suit: true, side_has_acted: true, we_bid_last: false}`,
     `requires: {hcp: [16, 40], evals: {"suit_length(their)": [0, 2]}}`, priority ~41.
     Needs a small engine condition to prevent the historical repeat-double loop:
     `my_last_call_was_double: false` (or restrict to hands 19+ for a second double).
   - Drop `rule_of_26` from `ballow_rebid_*` / `balhigh_rebid_*` (reopening seats read
     partner as 0, so the gate blocks every legitimate reopening rebid — board 1).
   - Endangers: the original "same hand doubled three times" bug — the new when-condition
     is the guard; re-measure doubles-made stats.

**3. Doubler's rebids after a minimum advance — `1$o - X - P - <suit> - P - ?`**
(MISSING; board 77, board 24(b) via the same review; ~10-12 IMPs)
   - Raise advance's suit: 17-19 w/ 4+ support (single raise), 20+ or 19 w/ shape: jump
     raise/game; cue = GF; new suit 17+ 5-carder; 1NT 18-19 bal.
   - Endangers: light reopening doubles hearing a 0-8 advance — keep the raise floors
     honest (17+), nothing below that acts.

**4. RKC 5H/5S reply must be passable when it is the sign-off spot**
(IMPLEMENTATION-BUG; board 38; 12 IMPs)
   - Split `rkc_5H` (and check `rkc_5S`) by `agreed_suit`: when the reply equals
     5-of-the-agreed-suit, `establishes: {forcing: non_forcing}` so
     `rkc5H_pass_signoff` survives the forcing-pass filter. Alternative: the filter
     exempts a pass rule defined in the most-specific interpreting context.
   - Endangers: nothing — today the position emits a literal nonsense bid (5S on a
     4-card suit at the five level).

**5. Responder's actions over their 1NT overcall — context `1$M - 1NT - ?`**
(MISSING; board 23; 11 IMPs)
   - X = penalty, 9+ HCP; 2$M = 3+ support 5-8; 3$M preemptive 4+ support; new suit
     natural NF; jump to game per LOTT with 5 trumps.
   - Endangers: nothing existing (position has no rules).

**6. Invite acceptances in second-suit auctions**
(MISSING; boards 30, 66; ~10-14 IMPs)
   - `1$M - P - 1$x - P - 2$y - P - 2NT - P - ?`: pass 12-13, 3NT 14+, suit rebids with
     shape (mirror the authored 1M-1NT-2m-2NT block).
   - `1$M - P - 1NT - P - 2$x - P - 3$x - P - ?`: 4$x/4$M with 15+ total, pass 12-14.
   - Endangers: nothing; these are pure range-with-no-rule holes (the engine literally
     passes 17-19-counts over invitations there today).

**7. Weak-two feature-ask replies** (IMPLEMENTATION-BUG; board 84; 11 IMPs)
   - `feat_*_3NT`: solid suit for real — `features: ["two_of_top3($W)"]` plus
     `suit_quality($W): [3, 9]` with sharp sigma (or a new `top3_honors` evaluator = 3).
   - `feat_*_min`: widen to `hcp: [5, 10]` (max-no-feature rebids the suit; feature rules
     still outrank in 8-10).
   - Endangers: none visible; current behaviour wrong-sides and wrong-strains maxima.

**8. Minor-suit slam route over 1NT** (MISSING; board 13; 12 IMPs but structural)
   - Minimum viable: over 1NT, quantitative 4NT allowed with 12-14 HCP + 6-card minor
     headed by 2 of top 3 (hand re-valued as 16+); opener's accept already exists.
     Full fix is minor transfers — larger job, known on the roadmap.
   - Endangers: quantitative auctions where the 6-card minor doesn't run — keep the
     two_of_top3 gate.

**9. Generic NT rules: stopper and seat discipline** (IMPLEMENTATION-BUG; boards 99, 28B,
77B, 9; ~6-9 IMPs)
   - `cl_nt1/2/3`, `ballow_nt1/2/3`: replace `stoppers(their)` + `stopper(their)` with
     `weakest_their_stopper: [0.9, 9]` (finishing the sweep DECISIONS already flags).
   - `cl_nt1`: add `when: {side_has_acted: true}` (no live sandwich 1NT on 8-11).
   - `ballow_nt1`/`cl_nt1`: deny a 6-card major (`not: {any_of: [{suits:{H:[6,13]}},
     {suits:{S:[6,13]}}]}`); drop the `suit_quality` floor from `*_rebid_*2` own-suit
     rebids (six cards is the credential — board 9).
   - Endangers: constructive NT bids where their second suit is genuinely irrelevant —
     `weakest_their_stopper` is vacuous uncontested, so exposure is small; this exact
     change was pre-approved-in-principle but unmeasured.

**10. Transfer continuation over 2NT** (NEEDS-EXCEPTION; board 25; 10 IMPs)
   - `nt2_tr_4$M`: require 6+ trumps or 5 + singleton/void (see board 25 for exact YAML).
   - `nt2_tr_3NT`: floor `hcp: [4, 40]`.
   - Endangers: 5332 hands with 6+ HCP that now play 4M when opener has 3 — opener's
     choice-of-games context (`opener_choice_after...`) must cover the 3NT pull; verify
     it does.

**11. Responder rebid priority: 6-card suit beats 1NT** (IMPLEMENTATION-BUG; board 28;
~7 IMPs)
   - `r1sr_2H` priority 49 → 56 (or add `not: {suits: {H: [6, 13]}}` to `r1sr_1NT` and
     `r1sr_2NT`). Check the expanded sibling contexts for the same inversion.

**12. `cl_takeout_X` measures the wrong suit; fallback advances in their suit**
(IMPLEMENTATION-BUG; board 36; ~5 IMPs)
   - Add evaluator `max_their_suit_length` (max holding across all `ctx.their_suits`),
     gate `cl_takeout_X` on `[0, 2]` (sharp).
   - Fallback layer: exclude opponents' naturally-bid suits from new-suit advances.

**13. Balancing 2NT outranks the balancing double on 19-21 balanced**
(IMPLEMENTATION-BUG; board 65; ~4 IMPs) — `bal_2NT` priority 65 → 71.

**14. 4th-seat rule-of-15 openings for all suits** (MISSING; board 26; 4 IMPs)
   - Clone `open_1S_rule15` into 1D/1C/1H versions, `hcp: [10, 11]`,
     `rule_of_15: [15, 30]`, seats [4], with the standard shape gates.

**15. Preempt-defense overcall quality** (NEEDS-EXCEPTION; board 67; ~6-9 IMPs)
   - `v3_*_C/D/H/S` overcalls: `hcp: [12, 40]`, replace `good_suit` with
     `suit_quality: [1.5, 9]`. Endangers: 4-level minor overcalls on ratty suits — keep
     the 6-card sharp length.

**16. Jump-overcall coverage for 7-card suits** (boards 12(b), 39(b); ~3 IMPs)
   - `oc1x_2y_jump`: length `[6, 6]` → `[6, 7]`; or author 3-level double-jump preempt
     overcalls (7 cards, 5-10 HCP, NV `suit_quality >= 1`).

**17. Minor game acceptance needs combined values** (NEEDS-EXCEPTION; board 40; 5 IMPs)
   - `uc_minor_game_5C/5D`: add `rule_of_26: [29, 99]`.

**18. Small, one-board items** (apply cheaply, expect ~2-6 IMPs total)
   - `xd_second_*`: add `suit_quality($s): [1, 9]` (board 18).
   - `xd_rebid_*3`: add `lott_total_trumps($s): [9, 26]`; trace why a sharp 6-card
     requirement fired on a 5-card suit (board 52).
   - `rr_run_*`: add `i_have_acted: false` (board 48).
   - `cl_negative_X3` for 3-level jump overcalls + a 3-level free-bid rule (board 39).
   - `oc1x_X` strong branch: deny a good 5-card major (board 93).
   - Negative-X-showed-a-major, they raise → opener supports with 3 (board 24).
   - Advance of the balancing double (cue/jump ladder −3 points) (board 53).
   - `cl_raise_C3/D3` floor 10 → 8 with the existing LOTT-8 gate (board 83).
   - `advsw` equal-length ties to the major (board 42).
   - `cl_nt2` rule_of_26 sharp/[22,99] (board 8).
   - `balhigh_X` pass-out seat 12+ vs 3-level preempts (board 33) — measure before keeping.

**Deliberately NOT chased (NOTHING-WRONG):** boards 54, 51, 6, 10, 70 — mainstream calls
that lost to double-dummy or to a scoped-out convention, and the thin-game/threshold
knobs the project has already measured as neutral. No DELETE-RULE verdicts this round:
every misfiring rule above has a sound core and a mechanical repair.

**One engine-level observation** (not a rule fix): several boards (23, 26, 83, 1, 9) were
decided by a descriptive rule at fit ~0.8 (one soft point off) losing the blend to a
perfect-fit permissive pass at priority ~20. That is the round-5 design working as
specified, but it means every off-by-one range seam turns into a pass — which is why the
range-widening fixes above (not blend re-tuning) are the right lever.
