# Expert review: all 38 losing boards of the seed-919191 BEN match (-128 IMPs)

Method: every board read against the live rule text in
`src/bridgebidder/systems/two_over_one.yaml`; the non-obvious mechanisms were reproduced
through `choose_bid` (boards 71, 89-by-symmetry, 6, 87, 83, 84, 65, 14, 57 both tables,
93, 69, 79, 38, 11, 77, 72, 76, 56, 62, 34, 27, 81, 18, 44) — diagnoses below are engine
behaviour, not conjecture. None of the fixes from EXPERT_REVIEW_100_BOARDS.md are
re-recommended; several of that review's *themes* recur and are flagged as such.

Recurring themes from the previous review that are back in new clothes:
1. **"A new call with no advance/continuation context is a trap"** — the reopening double
   authored by the previous review's fix #2 fired on board 69 and was promptly *passed out
   by advancer with a doubleton trump and 1 HCP* because nobody authored its advances. The
   same species (a live takeout double with no advance ladder) is boards 79 and 87.
2. **"Range-with-no-rule turns into a pass"** — boards 14, 72, 77 are all invitational or
   game-going positions where the only in-range call was the pass floor.
3. **Priority inversions between two perfect-fit rules** — boards 11, 83, 62, 77, 57(A):
   a generic or aggressive rule at fit 1.0 outranks the textbook call at fit 1.0.

---

### Board 14 (-15) — MISSING-AGREEMENT
Table A: 1S - 1NT - 2NT(18-19, correct) - **P (N, `uc_pass`)** on 4.QT7.KT2.AQT942 —
11 HCP with a 6-card club suit passed opener's 18-19 rebid. Reproduced: there is no
`1$M - P - 1NT - P - 2NT - P - ?` context at all; 3NT's generic rule scored 0.0 and 3C
("14+ points") 0.8, so the pass floor won a game-going auction. BEN bid 6C (par 1440).
**Fix (author):** context `1$M - P - 1NT - P - 2NT - P - ?`: P = 0-5; 3NT = 6-11 balanced-ish
(floor rule, `requires: {hcp: [6, 12]}`); 3$m natural slam probe with `suits: {$m: [6,13]}` +
`two_of_top3($m)` + hcp 9+ (opener raises to 6m/3NT). The 3NT floor alone recovers only
~2 IMPs here; the 6m probe is the real money and pairs with the previous review's fix #8.

### Board 57 (-15) — NEEDS-EXCEPTION (table B, the disaster) + two minors at table A
Table B: after 1H - (1S us) - 2S(cue) - 3H - 4H by them, with partner silent throughout, W
(AQ8765..KQ3.QT98, 13 HCP, vul) **balanced 4S (`balhigh_rebid_S4`)** over their freely-bid
game — 4SX-4 vul = -1100 instead of defending 4H (par says it fails). Reproduced: the rule's
`total_points: [14,40]` is a static gate; "values opposite partner's shown range" is not
enforced — partner has shown nothing and the opponents' auction was constructive, so this is
a phantom sacrifice, not a balance. **Fix:** add a `partner_has_acted: true` `when:`-condition
to `balhigh_rebid_C4/D4/H4/S4` and `balhigh_new_C4/D4/H4/S4` (engine: add `partner_has_acted`
as a trivial mirror of `i_have_acted` over `seat.partner`). Board 62(B) shows why the gate
must be partner-acted and not vulnerability: there the same family bid 4S *after partner's
X showed spades* and it earned par. Table A minors: (a) `oc1S_X` (12 HCP, 2=3=3=5) beat a
perfect-fit `oc1S_2C` — the 13-16 branch soft-admits 12-counts with no heart tolerance;
consider requiring 4 cards in the unbid major in the min branch (measure first); (b) `ch_nt3`
fired at rule_of_26 = 23 vs its [24,99] soft gate — make that gate sharp, as was already done
for `cl_nt2`.

### Board 89 (-15) — IMPLEMENTATION-BUG (the doubled-cue hole, twin of board 71)
Table A: 1D - (1H us) - P - 2D (`advo_cue`, correct limit-raise cue) - X - **P (N,
`xd_pass`)** - P - **P (S, `fallback`)** — we played our own artificial cue-bid, doubled,
in a 2-2 diamond "fit": 2DX-4 = -800 with 4H cold. Reproduced (via board 71, identical
mechanism): once they double the cue, the `xd` context takes over and knows nothing about
`agreed_suit`; `xd_pass` ("sitting for their double") fits 1.0 for the overcaller, and the
cue-bidder's next turn has ZERO matching rules, so the fallback backstop passes out the
doubled cue. **Fix:** author context `1$o - 1$v - P - 2$o - X - ?` (expand over the
`advance_overcall` pairs): `advcueX_retreat` = 2$v, priority 60, `requires: {}` (mandatory
floor — the cue promised support, retreating is never wrong), plus `advcueX_XX` (17+,
penalty interest); and context `1$o - 1$v - P - 2$o - X - P - P - ?`: 2$v floor for the
cue-bidder. Engine hardening worth doing at the same time: the fallback layer must never
select P when the standing doubled bid is our own side's alertable/cue call.

### Board 69 (-14) — MISSING-AGREEMENT + NEEDS-EXCEPTION
Table B: 1H (us) - (2S) - P - (P) - X (`ballow_reopen_X`, the rule added by the previous
review's fix #2, firing exactly as specified: 16 HCP, 2 spades) - P - **P (E, `uc_pass`)**
on 92.K.86432.JT432 — advancer passed the reopening takeout double at the two level with
two small trumps and 1 HCP; 2SX made +2, -670. Reproduced: every advance candidate scored
0.0 — the new double was authored without an advance ladder (theme 1). **Fix (author):**
context `1$M - <their overcall> - P - P - X - P - ?`: cheapest 4+ suit 0-8 (here 3C),
jump 9-11, 2NT natural with stopper, penalty pass ONLY with `suits: {their: [4,13]}` +
`two_of_top3(their)`. Secondary NEEDS-EXCEPTION: `ballow_reopen_X`/`balhigh_reopen_X`
should add `evals: {longest_suit_length: [0, 5]}` — W held AT8743 of hearts and the 3H
rebid (fit 1.0, `ballow_rebid_H3`) describes the hand far better than a 16-point double
(priority 41 currently beats the rebid's 29).

### Board 79 (-13) — MISSING-AGREEMENT (same family as board 69)
Table A: 1H - P - 2H - X (`cl_takeout_X`, legitimate) - P - **P (N, `uc_pass`)** on
97.KJ4.87654.A76 — advancer passed the takeout double of a raised suit with KJx of trumps
and a 5-card diamond suit; 2HX made, -670. Reproduced: 3D scored 0.0 ("5+ cards, 14+
points" is the only generic) — there is no `1$M - P - 2$M - X - P - ?` advance context.
**Fix (author):** that context, same ladder as board 69's (cheapest suit 0-8 mandatory-ish,
2NT 9-11 w/ stopper, penalty pass only with 4+ good trumps). This is the third distinct
"partner's live takeout double has no advance context" hole — see Fix list #2 for the
consolidated treatment.

### Board 93 (-13) — NEEDS-EXCEPTION (honest partial recovery only)
Table A: 2H - X(fine) - 4H - **X (N, `aw2r_responsive_X`)** on KT9854.A5.4.A642 — a
responsive double holding a 6-card spade suit (reproduced: 4S's generic scored 0.8 and lost).
S then had to invent 4S via `fallback`. We made 12 in 4S; BEN bid 6S. **Fix:**
`aw2r_responsive_X` add `not: {suits: {S: [5, 13]}}` / `{H: [5,13]}` (deny a 5+ card unbid
major) and author `aw2r_4S` in the `2H - X - 4H - ?` context: `suits: {S: [5,13]}, hcp
[8,40]` → 4S. Reaching the actual slam after 2H-X-4H needs cue machinery this system does
not have in that auction; expect to recover the soundness, not the 13 IMPs.

### Board 94 (-13) — MISSING-AGREEMENT
Table A: 1S - (3D) - **4S (`nx3_game_raise`)** on AT962.8.2.AKQJ76 — 13 HCP, 5 trumps,
solid 6-card side suit, ~18-19 support points: this hand is a slam raise, but
`nx3_game_raise` (total_points [11,40], sign_off) is the ceiling of the context. BEN cued
4D and bid 6S (par ~1440). **Fix (author):** in `neg_double_3level_M`: `nx3_cue` = 4$x
(their suit), `requires: {suits: {$M: [4,13]}, evals: {total_points: [16, 40]}}`,
`establishes: {agreed_suit: $M, forcing: game_forcing}`, priority 71; cap `nx3_game_raise`
with `not: {evals: {total_points: [16,40]}}`. Must be authored WITH opener's reply context
`1$M - 3$x - 4$x - P - ?` (4$M = minimum floor; 4NT RKC with extras — the rkc_* machinery
already interprets the replies) or it becomes another board-69 trap.

### Board 71 (-12) — IMPLEMENTATION-BUG
The reproduced twin of board 89: 1C - (1H us) - P - 2C (`advo_cue`) - X - **P (S,
`xd_pass`; 2NT fit 1.0 lost on priority, 2H "6+ cards" 0.35)** - P - **P (N, `fallback`,
zero candidates)** — our doubled cue played in 2CX-2 vul, -500, with 2H making. Same fix
as board 89 (one authored context pair covers both, ~27 IMPs between them).

### Board 76 (-12) — MISSING-AGREEMENT (scope-boundary, partial recovery)
Table B: 1C - 1H - 1NT - **4NT (`rr_nt_4NT`, quantitative)** - P (decline, correct on raw
HCP) with W holding AT2.KQ976.A7.AJ2 (19, FIVE hearts) opposite 1NT; 6H/6NT cold on the
5-3 fit (E: AJ2 support). Reproduced: the only heart rebid in the context requires 6
("4H: 6+ H, game values", fit 0.35) — with checkback deliberately scoped out there is no
5-card-major game-forcing route at all. **Fix (author):** in `1$m - P - 1$M - P - 1NT - P - ?`
add `rr_3$M_GF`: `suits: {$M: [5,13]}, hcp: [16,40]`, `establishes: {forcing: game_forcing,
agreed_suit: $M (on opener's raise)}`, plus opener's answer context (4$M with 3+ support /
3NT with 2). The 12 IMPs need the follow-up RKC to engage from W's 19; expect partial
recovery, but today a 19-count cannot even show the suit.

### Board 6 (-11) — IMPLEMENTATION-BUG (evaluator)
Table B: 1S (us, W: AQJ43.5.A873.AJ6, 16) - 2H - P - 2S(their cue of OUR suit) - P - 3H -
P - P - **P (W, `balhigh_pass`)**. Reproduced: `balhigh_reopen_X` scored **0.0** because
`max_their_suit_length` counts spades among "their suits" — the opponents' 2S *cue of our
own opened suit* — and W holds five of them. `_their_suits()` in `inference/engine.py`
(line ~325) appends every strain an opponent has bid. **Fix:** in `_their_suits`, skip a
call whose strain was already bid naturally by OUR side earlier in the auction (a cue, not
a suit they hold). With the X restored, E (5 spades) bids 3S over it and EW reach the
spade partial/game double-dummy par owns (-200 for NS). Needs Fix-list #2's advance ladder
to cash fully.

### Board 38 (-11) — NEEDS-EXCEPTION
Table B: 1C - (1S us) - 4C - **P (E, `ch_pass`)** on AQ973.875.T72.K5 — five-card support
for partner's overcall, LOTT 10, NV vs vul, and 4S (making, +420) scored 0.003 because
`ch_raise_S4` demands `rule_of_26: [25,99]` (partner's shown floor ~8 puts the hand at 18).
Values-raise logic is the wrong tool over their preemptive jump raise. **Fix:** in
`ch_raise_$s4` (majors at least) replace the requires with
`any_of: [ {evals: {total_points: [11,40], rule_of_26: [25,99], lott_total_trumps($s): [8,26]}},
{suits: {$s: [5,13]}, evals: {"lott_total_trumps($s)": [10,26], total_points: [6,40]}} ]`,
gating the new LOTT branch `when: {we_vulnerable: false}`. Endangers: NV 5-trump raises
pushed into doubled minus positions — LOTT-10 at the 4-level is standard, keep it NV-only
and re-measure.

### Board 56 (-11) — MISSING-AGREEMENT (deliberately-scoped area; optional)
N held QT9843.QJ9842.. (6-6 majors, 5 HCP) and passed at every turn (reproduced: sandwich
1H/1S fit 0.134 on the 8-16 hcp floor; opening 3H/3S preempts need 7 cards). Michaels/
unusual NT are scoped out by design (yaml line 21), so a 6-6 freak has no entry anywhere,
and BEN's N drove to the par 4H (+450) from the same cards. **Fix (narrow, optional):** add
an extreme-shape branch to the 1-level overcall/sandwich suit rules: `any_of` alternative
`{suits: {$s: [6,13]}, evals: {two_suiter_6_6-ish...}}` — concretely, a dedicated
`oc_freak`/`sw_freak` rule: two 6-card suits, hcp [4,16], bid the higher. Low confidence;
this is the one place a real convention (Michaels) is the honest answer — flag for a
DECISIONS revisit rather than forcing it through natural rules.

### Board 62 (-11) — NEEDS-EXCEPTION (minor) + variance
Table B: over 1D - P - 1H, E (AQJ973.8.83.AK74, 15) chose **X (`sw_X`)** over the fit-1.0
1S/2S overcalls (reproduced: priority 70 vs 68/66) — a six-card-major hand described as
three-suited. The table still scrambled to +200 (= par) thanks to W's 4S, so the margin
here is table A, where par requires a 3-HCP 7-6 freak (N) to sacrifice in 5CX — not
reachable by sane rules; that half is variance. **Fix (hygiene):** add
`not: {evals: {longest_suit_length: [6, 13]}}` to `sw_X` (both branches) — with a 6-card
suit the overcall wins; same doctrine as the previous review's `oc1x_X` fix.

### Board 87 (-11) — MISSING-AGREEMENT
Table A: 2H - P - 4H - **P (S, `ch_pass`)** on AK.J8.AT872.A962 — 15 HCP, 4 quick tricks,
doubleton heart; reproduced: the only double in reach is `ch_penalty_X` (requires 3+ trumps
by design — that gate is measured and right) so there is NO takeout-flavoured double of
their raised weak two at the 4-level. BEN's S doubled, N (7 spades) bid 4S: +620 our way
gone. **Fix (author):** context `2$W - P - 4$W - ?` (and `2$W - 3$W - ?`): X = takeout,
`hcp: [14, 40]`, `evals: {quick_tricks: [2.5, 12], max_their_suit_length: [0, 2]}`,
`establishes: {forcing: one_round}`; plus its advance context `2$W - P - 4$W - X - P - ?`
(cheapest suit / 4S-with-5+ mandatory, penalty pass only with trump stack) so it does not
become the next board-69. N's silence with QJT8752 and 3 HCP vul at the same table is a
defensible discipline call — do not chase it.

### Board 77 (-10) — IMPLEMENTATION-BUG (priority) 
Table B: 1C - P - 1S - P - 2C - P - **P (W, `rmr_pass`)** on QJ76.854.AQJ76.8 — 10 HCP
with a singleton club and a 2D call at fit 1.0 (reproduced: the generic "natural D, 5+
cards, 10+ points" matched perfectly, blended 0.778, but `rmr_pass` — hcp [6,10], fit 1.0,
priority 50 — outranks every generic). 3NT by E (+600 at BEN's table) never got started.
**Fix:** in `responder_after_minor_rebid`: tighten `rmr_pass` to
`requires: {hcp: [6, 9], suits: {$m: [2, 13]}}` (never pass a 10-count or a singleton-support
hand), and author the new-suit escape: `rmr_newsuit` for the `m: C` expansion — 2D,
`suits: {D: [5,13]}, hcp: [9, 12]`, forcing one round, priority 56 — with opener's
NT-with-stopper answer left to the existing generics (E is 15 with hearts Q76: `uc_nt2/3`
will carry it toward 2NT/3NT).

### Board 34 (-9) — NEEDS-EXCEPTION (same rule as board 57B)
Table A: after our light 1H opening they bid 1NT - 3NT unmolested; S (10 HCP, 6 hearts)
**balanced 4H over the freely-bid 3NT (`balhigh_rebid_H4`, reproduced fit 1.0)** with
partner silent: 4HX-3, -500 vs -430 for defending. The `partner_has_acted: true` gate from
board 57's fix covers this exactly. Small money here (~1-2 IMPs — par was already minus)
but the same rule produced -1100 on board 57; one fix, two boards.

### Board 29 (-7) — NOTHING-WRONG
Our S passed 1H with AK4.T98.Q543.A74 (13 flat, three trumps, no shape); BEN's identical
hand doubled and won the partscore race double-dummy. A 4-3-3-3 13-count with no support
for a takeout of hearts is a mainstream pass (the previous review deliberately kept the
shortness gate sharp). Style variance; leave it.

### Board 44 (-7) — NOTHING-WRONG
1H - 3H (limit, 3 trumps, 10 support) - 4H on 11 with 5-5: both calls are inside normal
ranges (reproduced: limit raise chosen over 2H by design); 8 tricks was the double-dummy
verdict. This is the thin-invite/thin-accept knob the project has twice measured as
tuning-neutral. Do not chase.

### Board 65 (-7) — MISSING-AGREEMENT
Table A: 1D - (2H) - X(neg) - (4H) - **P (S, `ch_pass`)** on AJ64.Q.AKT982.T3 — partner's
negative double *promised* spades, opener holds AJ64 and a stiff heart, and 4S (making;
par shows a NS grand!) scored 0.349 because the only spade rule wants 5+ cards; N's later
`balhigh_pass` with 14 is blocked by the (correct) anti-repeat guard on his neg X. The
previous review filed this species as small (its board 24); it is now a 7-IMP recurring
hole. **Fix (author):** context `1$x - 2$y - X - <their raise> - ?`: opener bids the
major the double implied with `suits: {$M: [4,13]}` at the level required (game over 4H),
`total_points: [13, 40]`; X = extras with ≤1 of theirs and 2.5+ quick tricks.

### Board 83 (-7) — IMPLEMENTATION-BUG (priority), small recovery
Table A: over their (light, 5-card) 2H, S (QT.AQT94.Q87.AK6 — FIVE hearts) chose
**X (`vw2_X`)** while `vw2_2NT` sat at fit 1.0 (reproduced: X's 17+ branch soft-admits the
16-count and priority 70 beats 68; the 13-16 branch is properly sharp-blocked by the
5-card heart holding). Advancer's 3C ladder then worked as authored. **Fix:** raise
`vw2_2NT` priority 68 → 72 (a 15-18 balanced hand with their suit stopped is always better
described by 2NT; genuinely strong hands still fall to X because 2NT's hcp cap
soft-blocks them). Honest accounting: recovery is ~1-2 IMPs (2NT+1; the rest of the margin
is BEN's 5-card weak-two style and their 1NT game at the other table).

### Board 11 (-6) — IMPLEMENTATION-BUG (priority inversion)
Table A: 1S - 1NT - **2S (`ob_1M1NT_2S`)** on AQJT862.KJ432.A. — reproduced: 4S
(`ob_1M1NT_4$M`, total_points 20+, fit 1.0) and 3S (fit 1.0) both LOSE to the minimum 2S
at priority 54 vs 51/50. A 7-5 twenty-total-points hand signed off in 2S+4. **Fix:**
priorities `ob_1M1NT_3$M`: 50 → 56 and `ob_1M1NT_4$M`: 51 → 57, and add
`evals: {total_points: [10, 15]}` to `ob_1M1NT_2$M` so the minimum rebid stops claiming
hands the jumps describe. (Same shape as the previous review's board-28 responder fix.)

### Board 12 (-6) — NOTHING-WRONG
1C - 1H - 1S - 3S(inv, 4 trumps, ~10 support) - 4S(14, accept): a normal invite-accept
chain that double-dummy scored 9 tricks. Thin-game knob, measured neutral twice. Leave.

### Board 18 (-6) — NEEDS-EXCEPTION (minor)
Table A: 1D - (1S us) - 2S(their cue) - **P (S, `cl_pass`)** with Q832 of spades and ~6
support points: the pre-emptive 3S over their cue-raise (LOTT 9) has no rule —
`cl_raise_S3` wants 10+ points (fit 0.001). **Fix:** add a 4-trump LOTT branch to the
competitive 3-level raise of partner's overcall when the standing bid is their cue/raise:
`any_of` alternative `{suits: {$v: [4,13]}, evals: {"lott_total_trumps($v)": [9,26],
total_points: [3, 9]}}`. Worth ~2 IMPs here; standard obstruction.

### Board 36 (-6) — NOTHING-WRONG
1H - (X) - 2H - (2S) - 4H on 16 with a void and 5-5: a normal shape-accept that
double-dummy held to 9 tricks while BEN's game-try sequence stopped in 3H. Thin-game
knob again. Leave.

### Board 46 (-3) — NOTHING-WRONG
Table A passed out with two 11-counts that fail rule-of-20/15 by a point. Opening-style
threshold, measured neutral. (Table B's light `oc1H_X` on 10 flat is worth an eyebrow but
cost nothing against par.)

### Board 52 (-6) — NOTHING-WRONG
1S - 1NT - 2S - P on 8 HCP with a doubleton: declining to invite on 8 opposite 12-15 is
mainstream; BEN's 3S-4S on the same cards was rewarded double-dummy. Thin-invite knob.

### Board 67 (-6) — NEEDS-EXCEPTION
Table B: 1S - P - 1NT - (2C) - **2S (`cl_rebid_S2`)** on AQ9852.9.AK72.KJ — a 17-count
with a 6-card suit made the same rebid a 12-count would; the competitive context has no
invitational jump (BEN, uncontested, rebid 3S and was raised to the making 4S).
**Fix:** author `cl_rebid_S3_jump` (and family): in the competitive-low context, jump
rebid of opener's 6+ suit with `total_points: [16, 19]`, `suit_quality: [1.5, 9]`,
priority above `cl_rebid_$s2`; `cl_rebid_$s2` gains `not: {evals: {total_points: [16,40]}}`.

### Board 72 (-6) — MISSING-AGREEMENT (reverse continuations)
Table A: 1C - 1S - 2H(reverse, 17+) - **2NT (`uc_nt2`, non-forcing!)** - **P (N,
`uc_pass`, with 17)**. Reproduced: no `1$m - P - 1$M - P - 2$y(reverse) - P - ?` context
exists; the generic 2NT is non-forcing so opener passed a game-going auction at 2NT+3.
**Fix (author):** responder-over-reverse context: 2NT = 8-11 `forcing: one_round`; 3NT =
12+ with stoppers; raises natural GF-ish; PLUS opener's answer context
`... 2NT - P - ?`: 3NT floor with 16+ (any shape — he reversed), suit rebids with 6-5.
Same "invitation answered by silence" family the previous review fixed for the 1M trees
(its fix #6); this is the minor-reverse branch it did not cover.

### Board 27 (-5) — MISSING-AGREEMENT
Table A: 1H - 1NT(us, 15-18) - P - **P (N, `uc_pass`)** on J9872.AT42.93.63 — advancer of
the 1NT overcall has no context (`1$M - 1NT - ?` covers only the opener's-side responder;
reproduced: 2S scored 0.009). 2S plays +110 (par); we defended 2C. **Fix (author):**
context `1$o - 1NT - P - ?`: natural 2-level suits to play 0-7 (5+ cards), 2NT invite
8-9, 3NT 10+; cheapest-cue Stayman-ish only if you want the full gadget — the natural
ladder captures the par here.

### Board 92 (-5) — NOTHING-WRONG
Opener's 2D rebid (4=3=5=1, KQJ94) over the negative double is at least as normal as
BEN's stiff-club 1NT; double-dummy happened to pay 1NT. No rule change is safe on this
evidence.

### Board 84 (-4) — MISSING-AGREEMENT
Table A: 1D - (1H) - X - P - **2NT (S, `uc_nt2`)** on QT7.Q6.KQJ65.QJ2 (12, Qx stopper) —
reproduced: no opener-rebid-over-negative-double context exists, so the generics fought
and the 11-12 "natural 2NT" outbid the fit-0.35 alternatives a full level too high;
2NT-3 vul. **Fix (author):** context `1$m - 1$M - X - P - ?`: 1-level other major with
3-4 cards; cheapest NT = 12-14 with stopper; 2$m = 5+ minimum; jumps = 17+. (Board 92
shows the same position going right by luck of the generics — author the floor so it is
not luck.)

### Board 7 (-2) — IMPLEMENTATION-BUG (template hygiene)
Table A: 1S - P - 1NT - **2S (N, `sw_2S`)** on AQ942 of THEIR OPENED SUIT — the sandwich
suit-overcall rules never exclude $o, so when $o = S the 2S rule happily bids the
opponents' suit naturally; -200. **Fix:** add `when: {unbid_suit: $s}` (as the ch_new_*/
balhigh_new_* rules already do) to `sw_1H/1S/2C/2D/2H/2S`. Two IMPs here, nonsense-class
bug.

### Board 19 (-2) — NOTHING-WRONG
Both tables landed in normal partscore scraps within an IMP or two of par. Variance.

### Board 81 (-2) — NEEDS-EXCEPTION (cheap insurance)
Table A: 1H - (1NT) - X(penalty, r1NTo_X) - P - **2NT (S, `uc_nt2`)** — opener PULLED
partner's penalty double of their 1NT overcall on a flat 12. No `1$M - 1NT - X - P - ?`
context exists, so the generic grabbed it. **Fix (author):** that context with a pass
floor: P = default (defend 1NTX), suit bids only with 6+ cards or extreme shape,
priority above the generics. Cost here was 2 IMPs; the failure mode (rescuing opponents
from a penalty double) is worth insuring against.

### Board 99 (-2) — NOTHING-WRONG
2H - 3H(invite on 10) - 4H(accept on 12): knob territory, measured neutral. Leave.

### Board 23 (-1) — NOTHING-WRONG
We bid 1C-1S-1NT-3NT (+400); BEN checked back into the 5-3 spade fit for +420. Checkback
is deliberately scoped out (DECISIONS); 1 IMP does not reopen it (same verdict as the
previous review's board 70).

### Board 48 (-1) — NOTHING-WRONG
Both tables reached a major-suit game on the 6-5 hand; BEN's choice of the 4-4 spade fit
out-scored our 6-2 hearts by a double-dummy trick. Variance.

### Board 55 (-3) — NOTHING-WRONG
W's pass of an 11-count that fails rule-of-20 (19) is the opening-style knob; the rest of
the board followed. Measured neutral; leave.

---

## Fix list (deduplicated, priority order)

Roughly 90-100 of the 128 IMPs pass through items 1-6. As always: implement, then re-run
the paired corpus; "Endangers" names what to watch.

**1. The doubled-cue hole — our artificial cue must never be passed out doubled**
(IMPLEMENTATION-BUG; boards 89, 71; ~27 IMPs)
   - New context `1$o - 1$v - P - 2$o - X - ?` (expand over `advance_overcall`'s pairs):
     `advcueX_retreat`: call 2$v, priority 60, `requires: {}`, shows "minimum overcall,
     retreating from the doubled cue", `establishes: {forcing: non_forcing, agreed_suit: $v}`;
     `advcueX_XX`: priority 65, `requires: {hcp: [15, 40]}`.
   - New context `1$o - 1$v - P - 2$o - X - P - P - ?`: `advcueXpp_retreat`: call 2$v,
     priority 60, `requires: {}` (the cue-bidder's mandatory pull).
   - Engine hardening: the fallback/backstop layer must exclude P whenever the standing
     doubled bid is our own side's alertable (cue) call.
   - Endangers: nothing — today the engine literally plays 2-of-a-cue doubled.

**2. Advance ladders for every live takeout double (the board-69 lesson, generalized)**
(MISSING; boards 79, 69, 87-second-half, 6-second-half; ~25-30 IMPs)
   Three contexts, one shared ladder (cheapest 4+ suit 0-8 at priority 55 with per-suit
   `suit_diff` tie-breaks exactly as `advS_*`/`advH_*` already do; jump = 9-11; NT natural
   with `weakest_their_stopper: [0.9, 9]`; penalty pass ONLY with
   `suits: {their: [4, 13]}` + `features: ["two_of_top3(their)"]`):
   - `1$M - P - 2$M - X - P - ?` (board 79)
   - `1$M - <2-level overcall> - P - P - X - P - ?` (board 69 — the advance of
     `ballow_reopen_X`); mirror for the balhigh pattern
   - `2$W - P - 4$W - X - P - ?` (board 87, pairs with fix #6)
   - Endangers: converting real penalty passes — the two_of_top3 gate is the guard.

**3. 4-level balancing sacrifices need a partner who has bid**
(NEEDS-EXCEPTION; boards 57, 34; ~14-16 IMPs)
   - Engine: add `partner_has_acted` `when:`-condition (mirror of `i_have_acted` over
     `seat.partner`).
   - Add `partner_has_acted: true` to `balhigh_rebid_C4/D4/H4/S4` and
     `balhigh_new_C4/D4/H4/S4`.
   - Endangers: legitimate one-man saves at favorable — board 62(B) stays legal because
     partner had doubled; re-measure sacrifice frequency.

**4. `_their_suits` counts their cue of OUR suit** (IMPLEMENTATION-BUG, engine;
board 6, latent everywhere `max_their_suit_length`/`stoppers(their)` is used; ~8-11 IMPs)
   - In `inference/engine.py::_their_suits`, before appending `c.strain`, skip it when an
     earlier call in the same strain was made by OUR side (their bid is then a cue).
   - Endangers: auctions where both sides genuinely bid the same suit naturally — rare,
     and the cue reading is right nearly always.

**5. Reopening doubles prefer the 6-card suit** (NEEDS-EXCEPTION; board 69; folded into
#2's board) — add `evals: {longest_suit_length: [0, 5]}` to `ballow_reopen_X` and
`balhigh_reopen_X`. Endangers: 16+ 6-4 hands that wanted to show both; the suit rebid is
still the percentage action.

**6. Takeout double of their raised weak two at the 4-level** (MISSING; board 87; ~11 IMPs)
   - Context `2$W - P - 4$W - ?` (and `2$W - 3$W - ?`): X = `hcp: [14, 40]`,
     `evals: {quick_tricks: [2.5, 12], max_their_suit_length: [0, 2]}`, forcing one round.
   - Ship together with its advance context (#2 third bullet).
   - Endangers: the measured "penalty doubles need trump tricks" doctrine — this X is
     takeout, its advance ladder must make pulling the default.

**7. Slam raise over their 3-level jump overcall** (MISSING; boards 94, 93-cousin;
~13-26 IMPs at stake, expect partial)
   - `nx3_cue` (4$x cue): `suits: {$M: [4,13]}, evals: {total_points: [16, 40]}`,
     `establishes: {agreed_suit: $M, forcing: game_forcing}`, priority 71; cap
     `nx3_game_raise` with `not: {evals: {total_points: [16, 40]}}`.
   - Opener's reply context `1$M - 3$x - 4$x - P - ?`: 4$M floor (minimum), 4NT RKC with
     16+ or a source of tricks (the rkc_* reply machinery already exists).
   - Also board 93: `aw2r_responsive_X` add `not: {any_of: [{suits: {S: [5,13]}},
     {suits: {H: [5,13]}}]}` and add `aw2r_4S`/`aw2r_4H` (5+ suit, 8+) to `2$W - X - 4$W - ?`.
   - Endangers: nothing today reaches these slams; watch for 4$x cues left in.

**8. `rmr_pass` swallows 10-counts with singleton support** (IMPLEMENTATION-BUG/priority;
board 77; ~7-10 IMPs)
   - `rmr_pass`: `requires: {hcp: [6, 9], suits: {$m: [2, 13]}}`.
   - Add `rmr_newsuit` (m=C expansion): 2D, `suits: {D: [5,13]}, hcp: [9, 12]`,
     `forcing: one_round`, priority 56.
   - Endangers: rebidding on misfit 9-counts — the 5-card-suit gate is the guard.

**9. Reverse continuations** (MISSING; board 72; ~6 IMPs)
   - Context `1$m - P - 1$M - P - 2$y(reverse) - P - ?`: 2NT = 8-11 forcing one round;
     3NT = 12+ w/ stoppers; raise/preference rules; pass floor only 0-5.
   - Context `... - 2NT - P - ?`: opener 3NT with 16+ (no `semi_balanced` gate — he
     reversed; that gate is what silenced the 17-count), suit rebids with extra shape.

**10. `ob_1M1NT` jump rebids outranked by the minimum rebid** (IMPLEMENTATION-BUG;
board 11; ~5-6 IMPs) — priorities: `ob_1M1NT_3$M` 50 → 56, `ob_1M1NT_4$M` 51 → 57; add
`evals: {total_points: [10, 15]}` to `ob_1M1NT_2$M`.

**11. Opener's rebid family over the negative double** (MISSING; board 84, insurance for
92; ~4 IMPs) — context `1$m - 1$M - X - P - ?`: other major 1-level w/ 3+; cheapest NT
12-14 w/ stopper; 2$m 5+ minimum; jumps 17+; pass floor rare (their X may be pulled).

**12. Opener supports the negative double's major over their game raise** (MISSING;
board 65, previous review's board 24 recurring; ~5-7 IMPs) — context
`1$x - 2$y - X - <raise to game> - ?`: bid the implied major with 4 cards and 13+ total
points at the required level; X = 14+, ≤1 of theirs, 2.5+ quick tricks.

**13. Responder's continuation over the 18-19 2NT rebid** (MISSING; board 14; ~2 IMPs
now, slam upside) — context `1$M - P - 1NT - P - 2NT - P - ?`: 3NT floor 6-12; P 0-5;
3$m slam probe with 6+ good minor, 9+.

**14. Competitive jump rebid with 16-18 and a 6-card suit** (MISSING; board 67; ~4 IMPs)
— `cl_rebid_$s3_jump` per board-67 text; cap `cl_rebid_$s2` at total_points 15.

**15. LOTT branch for the 4-level raise of partner's overcall over their preempt**
(NEEDS-EXCEPTION; board 38; ~11 IMPs) — `ch_raise_H4/S4` `any_of` per board-38 text,
LOTT-10 branch gated `we_vulnerable: false`. Endangers: NV phantom saves; measure.

**16. Advance of our 1NT overcall** (MISSING; board 27; ~4 IMPs) — context
`1$o - 1NT - P - ?`: natural 2-level suits 0-7, 2NT 8-9, 3NT 10+.

**17. Small, one-board items** (~6-8 IMPs total)
   - `sw_X`: add `not: {evals: {longest_suit_length: [6, 13]}}` (board 62).
   - `sw_1H/1S/2C/2D/2H/2S`: add `when: {unbid_suit: $s}` — never bid THEIR suit as a
     sandwich "overcall" (board 7).
   - `vw2_2NT` priority 68 → 72 (board 83).
   - `1$M - 1NT - X - P - ?` context with a pass floor — opener does not pull the penalty
     double (board 81).
   - 4-trump LOTT raise over their cue of partner's overcall (board 18).
   - `ch_nt3`: make `rule_of_26: [24, 99]` sharp, mirroring the earlier `cl_nt2` change
     (board 57A).
   - `oc1S_X`/`oc1H_X` 13-16 branch: consider requiring 4 cards in the unbid major
     (board 57A) — style-tightening, measure before keeping.

**Deliberately NOT chased (NOTHING-WRONG):** boards 29, 44, 12, 36, 52, 92, 99, 19, 23,
48, 46, 55, and board 62's table-A half — opening-style and thin-invite knobs the project
has measured as neutral, double-dummy strain luck, a scoped-out convention worth 1 IMP,
and a par that demands a 3-HCP freak sacrifice. Board 56 is recorded as the honest cost
of the "no Michaels" scope decision rather than a rule defect. No DELETE-RULE verdicts:
every misfiring rule has a sound core; the two worst offenders (`balhigh_rebid_*4`,
`xd_pass`-over-our-cue) need a gate and a context, not deletion.

**Engine-level observations (not rule fixes):**
- The forced-continuation backstop can pass out our own doubled artificial call (board
  89/71) — a one-line invariant in the fallback layer is cheap insurance beyond fix #1.
- `_their_suits` treating cues as natural (fix #4) silently poisons every
  `max_their_suit_length` / `stoppers(their)` / `suit_length(their)` gate in competitive
  auctions where they cue us; board 6 is just the one that cost visibly this match.
- Theme worth a checklist item for future authored calls: **every new call needs (a) an
  interpretation context for partner including a floor, and (b) an advance/continuation
  ladder** — fixes #1, #2, #6, #7, #9, #11 are all instances of calls (some added by the
  previous review) whose partners had nothing to say.
