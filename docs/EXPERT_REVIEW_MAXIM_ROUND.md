# Expert review of the maxim round — board-by-board verdicts

Reviewer basis: 2/1 GF expert practice (Kantar on Blackwood prerequisites, Bergen/Cohen on
light openings and preempts, Woolsey on competitive discipline). All hands and auctions read
from the dossier; all rule text read from `two_over_one.yaml`. Where I cite an evaluator I
checked its actual implementation (`evaluators.py`), so thresholds below are in the engine's
own units (suit_quality: A/K/Q = 1, J/T = 0.5; quick_tricks: AK=2, AKQ... standard scale;
keycards(X) = four aces + king of X).

The headline finding first, because it drives five boards: **the Blackwood vetoes
(void / worthless doubleton) are missing the classic caveat — the prerequisites apply to the
hand that needs the ANSWER, not to a hand that already holds the answer.** When the asker
holds 3+ keycards for the trump suit himself, partner's reply is unambiguous and no missing
ace can be "the wrong ace": the ask is safe with a void, and correct. On every losing veto
board in this dossier the asker held 3 or 4 keycards; on the one board where the veto GAINED
(926) the asker held only 2. The waiver "asker's own keycards(trump) >= 3 overrides the
void/worthless veto" separates the data perfectly and is textbook, not curve-fitting.

---

## Board 985 | -13 | rkc_4NT vetoed (worthless_doubleton), fallback = Pass of 4H
E: AQ6.AKQ873.K6.95 asked 4NT over partner's 2/1 in clubs and 4H preference; the new
worthless-doubleton veto (95 in clubs) killed the ask and 6H (making) was never bid.

**VERDICT: NEEDS-EXCEPTION (two of them).**
1. `worthless_doubleton` must ignore any suit partner has bid naturally (partner shown
   length >= 4) and the agreed trump suit. xx in partner's 5-card 2/1 suit is not "two fast
   losers no reply can diagnose" — partner's honors sit behind it. Change the evaluator to
   skip suits with `ctx.partner_min_length[s] >= 4`.
2. Add the keycard waiver: E holds SA, HA, HK = 3 keycards for hearts; a hand with 3+
   keycards may always ask. Encode as `any_of: [ {void/worthless gates}, {evals:
   {"keycards(agreed)": [3,5]}} ]` in rkc_4NT and jac_rkc.

## Board 256 | -11 | gst_rkc_S vetoed (void), fallback = op_lr_game 4S
N: A9876..A4.AK8742 over the 3S limit raise. Heart void vetoed 4NT; the fallback was a flat
4S sign-off and a cold 6S (13 tricks) died. No cue floor exists over a limit raise, so the
veto had no better alternative to steer into — exactly the failure mode the authors already
documented for worthless_doubleton on gst ("the veto measurably deleted slams there") and
then re-introduced with the void gate.

**VERDICT: NEEDS-EXCEPTION.** N holds SA, DA, CA = 3 keycards: apply the same waiver
(`keycards(S) >= 3` overrides `void(any)` in gst_rkc_*). With it, 5C (1 keycard = SK) is
unambiguous and 6S is bid. General principle to adopt: a Blackwood veto may only fire when
the context offers a slam-going alternative (cue floor); otherwise the veto IS the slam
decision and needs the count-based waiver.

## Board 272 | -11 | rkc_4NT vetoed (void) -> cue 3S, then the 22-count passed 4H
E: AT8.AKQ83.AK753.(void) — a 22-count with FOUR keycards (SA, HA, HK, DA). The void veto
pushed E into the cue (fine per textbook), but when W signed off 4H, E's only re-try was
4NT — vetoed again — so E passed 4H with 13 tricks on top. Par is 7H.

**VERDICT: NEEDS-EXCEPTION.** Same waiver: with 4 keycards in hand the asker KNOWS which
card is missing (here only the CA, facing his own void — worthless to the opponents' cause).
A hand with keycards(agreed) >= 3 must be allowed to ask despite the void. The cue-then-pass
sequence is a secondary symptom and disappears once the waiver exists.

## Board 390 | -11 | open_1H_rule20 vetoed (quick_tricks 1.5 < 2), S passed
S: 5.QJT965.KJ43.A2 — 11 HCP, rule of 20 = 21, but 1.5 QT. Old 1H reached 4H +650; new pass
let EW steal the board (opponents' undoubled save, +150).

**VERDICT: NEEDS-EXCEPTION.** The rule-of-22 gate is too tight for MAJOR-suit shape hands.
Change `quick_tricks` on open_1S_rule20 / open_1H_rule20 to `[1.5, 12]`; keep `[2, 12]` on
open_1m_rule20 (the dossier's winning passes — 170, 519, 752, 195 — are all minor hands, and
the losing passes — 390, 424, 843 — all hold a 5+ major or 5-5 majors). An 11-count with a
good 6-card major and 1.5 QT is an opening bid in every expert's book.

## Board 905 | -11 | splinter-wasted context shadowed 4H; softly-vetoed 4NT won
S: AJ.AKT64.84.A874 over the 4C splinter. S has ZERO wasted points (only the CA, which the
evaluator correctly exempts) so spl_wasted_4H did not fit — but because the new context
DEFINES the call 4H, the generic cue_H_signoff 4H was shadowed out entirely, and rkc_4NT,
carrying a worthless doubleton (84 — a genuine one this time, two fast diamond losers) that
only soft-penalized it to ~0.8, won by default. 6H-1 instead of 4H+1.

**VERDICT: IMPLEMENTATION-BUG.** Two mechanical defects, both must be fixed:
1. Add a catch-all sign-off to `opener_after_splinter_wasted` (call 4$M, `requires: {}`,
   priority ~34, mirroring cue_$M_signoff) so the specific context never deletes the game
   bid it shadows. Any context that claims a call must contain a floor rule for that call.
2. Boolean vetoes must hard-block, not soft-match at 0.8: with the keycard waiver from
   985/256/272 in place, move `void(any)` and `worthless_doubleton` into hard semantics
   (a `when:`-style gate or a dedicated `veto:` section) in rkc_4NT/jac_rkc. On this board
   the veto was RIGHT and the engine bid 4NT anyway — a veto that only leans is not a veto.

## Board 424 | -10 | open_1H_rule20 vetoed (1.5 QT), N passed
N: 4.QT962.KQ532.K8 — 10 HCP 5-5, rule of 20 = 20, 1.5 QT. Old opened, reached 3NT +400;
new pass ended in partner's overreached 4S-1.

**VERDICT: NEEDS-EXCEPTION.** Same fix as 390: majors gate to [1.5, 12]. 5-5 with both
honors concentrated in the long suits is a mandatory light opening (Bergen would open this
in his sleep).

## Board 669 | -10 | rkc5D_signoff_C bid 5NT as a contract: down 5
S: KJ.3.AKT72.AKQ75 asked with clubs agreed, N (1 HCP!) replied 5D = 0. The counting logic
correctly diagnosed two missing keycards and signed off — into 5NT with a singleton heart
opposite nothing, 6 tricks, -500, when 6C was -100 (and old 6C actually scored -100).

**VERDICT: IMPLEMENTATION-BUG in the escape, plus one exception.**
1. The counting sign-off itself is CORRECT (validated at +11/+13 on 691/660) — keep it.
2. The 5NT escape is wrong whenever the asker is unbalanced: 5NT needs stoppers, 6m needs
   only trumps. Change rkc5D_signoff_C (and the 5NT escapes in the 5H/5S continuations for
   minors) to bid 6 of the minor by default, and permit 5NT only when the asker has
   `singleton_or_void: [0,0]` AND `worthless_doubleton: [0,0]`. Down-one in the known
   10-card fit is the least-worst exit; 5NT with an unstopped suit is the most-worst.
3. Upstream: the ask's `rule_of_26: [31, 99]` gate soft-matched against a partner who had
   shown essentially nothing (N held 1 HCP). For MINOR-agreed 4NT asks, where a 0-reply
   strands you past your safety level, that strength gate must hard-block, not lean.

## Board 131 | -7 | third-seat 1H opened (new) where old passed
E: 95.AQJ432.A84.T8 — 11 HCP, 2.5 QT, AQJ-sixth, third seat. A completely normal opening
(it even satisfies rule of 20 + 2 QT). The loss: the old silence had kept BEN out of a cold
4S; opening woke them up to their own par game.

**VERDICT: NOTHING-WRONG.** You do not pass sound openings to keep opponents out of par.
No change.

## Board 342 | -6 | open_1D_rule20 vetoed (1.5 QT), S passed
S: 3.T2.KJ973.KQJ72 — 10 HCP 5-5 minors, 1.5 QT. Old 1D bought a lucky +(-170 vs -420)
because BEN misjudged the crowded auction and stopped in 2S with a 4S hand.

**VERDICT: NOTHING-WRONG.** Rule-of-22 pass on a 10-count 5-5 in the minors is mainstream
discipline, and the dossier's minor-suit ledger for this gate is clearly positive
(170 +11, 519 +5, 752 +5, 195 +2 against this -6 and 181's -2). Keep the 2.0 QT gate for
the minors; the old gain here was opponent error, not a better bid.

## Board 736 | -5 | gst_rkc_D vetoed (void), fallback = uc_pass of 3D
E: KT983.AQ4.AJ942.(void) — 14 HCP 5-5 after partner's 3D raise. E holds only 2 keycards,
so the veto is bridge-correct (there is no slam: 11 tricks). But the fallback PASSED an
invitational raise with ~17 total points; 5D makes exactly, +400 became +150. uc_raise_D4
was blocked by its `lott_total_trumps(D): [10, 26]` gate (only 8 combined shown).

**VERDICT: NEEDS-EXCEPTION — not on the veto, on the floor beneath it.** Add a
game-acceptance rule over partner's minor raise (bid 5m — or 3NT with stoppers — on 17+
total points, 8+ combined trumps, priority above uc_pass). Rule of thumb to encode
system-wide: a hand strong enough to trigger a (vetoed) slam ask must never end below game.

## Board 484 | -4 | open_3D_vul blocked by side-major gate (5-card major), N passed
N: J.Q9874.KQJ6543. — 7-5, 7 HCP. The H: [0,3] gate blocked 3D because of FIVE hearts to
the queen. Passing let EW stroll to 4S; par (-200) requires NS to be bidding diamonds high.

**VERDICT: NEEDS-EXCEPTION.** The 4-card-side-major maxim exists to avoid missing a major
FIT worth more than the preempt; Q9874 is not that suit. Apply the H/S gate only when the
side major is a real suit: block only if `suit_quality(M) >= 1.5` (KQxx(x), AJxx(x) still
blocked; Q9874 = 1.0 and T865 = 0.5 preempt as they should). With a 7-bagger and a bad
5-card major, the 7-bagger is the hand.

## Board 802 | -4 | third-light 1H (priority 75) outranked the weak two (65)
N: Q8.KQJT84.J872.6 — 9 HCP, KQJT84, third seat. Old 2H pushed EW overboard (3S-2, +100);
new 1H let them defend a quiet 3H-1.

**VERDICT: NEEDS-EXCEPTION.** With a 6-card suit in weak-two range the weak two is both
more descriptive and more obstructive; the light 1-bid is for the 5-card-suit hands (and
6-card 11-counts too strong for 2M). Restrict open_1M_third_light so it does not overlap
the weak two: `any_of: [ {suits: {M: [5,5]}}, {hcp: [11,11]} ]` (leave the 6-7 card 9-10
HCP hands to open_weak_2M/open_3M, which fire in seat 3 already).

## Board 843 | -4 | open_1S_rule20 vetoed (1.5 QT), W passed
W: KJT96.KQT52..J63 — 10 HCP 5-5 majors with a void. New pass let NS play 3NT +430; old 1S
had bought -200. (Old's -200 in a 4H overreach still beat conceding 3NT.)

**VERDICT: NEEDS-EXCEPTION.** Same fix as 390/424: majors QT gate to [1.5, 12]. 5-5 in the
majors with two-and-a-half honors per suit and a void is an automatic opening at any table
I've ever coached.

## Board 84 | -3 | third-light 1S opened, passed-hand N jumped to 3S, -100 vs passout
S: KQJ98.KT98.62.J8 opened a textbook third-seat 1S; N (A53.75.T843.KQ76, flat, 3 trumps)
jumped to a limit raise opposite a possibly-9-count and opener correctly declined; 3S-1.

**VERDICT: NEEDS-EXCEPTION — the opening is right, the raise structure isn't.** A
third-seat light-opening style is only sound with a damped passed-hand raise scheme: either
add Drury (2C by a passed hand = fit + limit values, letting opener sign off in 2S) or, as
the minimal patch, cap the passed-hand jump raise: opposite a third-seat opening, 10-11
support points with 3 trumps raises to 2S only. Without this the third-light rules will
keep bleeding -100s exactly like this board.

## Board 459 | -3 | third-light 1S opened (new) where old passed
E: AKT974.T962.KJ.6 — 10 HCP, AKT-sixth, third seat (old rules had NO bid: weak two blocked
by the 4-card heart suit, no light-1 rule). Opening is 100% mandatory; the -3 came from
BEN's good 1NT/3C judgment afterwards.

**VERDICT: NOTHING-WRONG.** This board is evidence FOR the third-light rule: it fixed a
hole where a stone-cold opening bid was being passed. Variance took the 3 IMPs.

## Board 486 | -3 | rkc_4NT vetoed (void) for BOTH hands; cue chain died in 4H
W: .KQJ852.KT97.K54 and E: AT98543.A97..A76 — both hands hold a void, so after the void
veto NEITHER could ever ask, and a 13-trick heart hand stopped in game. E holds SA, HA,
CA = 3 keycards.

**VERDICT: NEEDS-EXCEPTION.** The same keycard waiver rescues it from E's side
(keycards(H) >= 3 overrides the void gate): E asks, hears 5C-showing-HK... hears one
keycard, knows only the DA — facing his own void — is missing, and bids the slam. Third
data point for the waiver; no new machinery needed.

## Board 181 | -2 | open_1C_rule20 vetoed (1.5 QT), E passed
E: 74.K9.QJ6.KQ9843 — quacky 10-count, 6 clubs. Under my split recommendation (minors keep
2.0 QT) this stays a pass, and I endorse that: this is precisely the hand type rule-of-22
exists to keep closed.

**VERDICT: NOTHING-WRONG (for the reviewed rule).** The actual -2 was aggravated by E later
bidding a horror 1NT in a live auction (5 tricks) — a pre-existing competitive-rebid defect
outside this round's rules; worth a separate ticket, not a maxim change.

## Board 448 | -2 | open_1C_rule20 vetoed (1.0 QT), E passed
E: Q872.K4.Q3.KJT95 — 11 HCP, ONE quick trick, queens everywhere.

**VERDICT: NOTHING-WRONG.** Textbook pass; the gate doing exactly its job. Old +130 vs new
+50 is the price of one opponent preempt landing softly. No change.

## Board 357 | -1 | open_3D_vul blocked by side-major gate (T865), S passed
S: .T865.AKQ8754.92 — AKQ-seventh and a void, blocked from 3D by four hearts to the TEN.

**VERDICT: NEEDS-EXCEPTION.** Same fix as 484: gate only majors with suit_quality >= 1.5.
Nobody on earth passes this hand to protect a T865 "major".

---

## Positive-delta boards that carry information

- **926 (+1, gst_rkc_D void veto):** the veto's only win — and the asker held exactly 2
  keycards, so the 3-keycard waiver PRESERVES this gain. Confirms the waiver threshold.
- **106 (+10, jac_wasted_signoff):** KQ8 opposite the 3C shortness reply, signed off in 4S
  instead of the old 5S-1. The duplication maxim working exactly as Kantar teaches. Keep.
- **691 (+11) and 660 (+13), rkc5D_slam counting:** the 0-vs-3 disambiguation by counting
  bid two slams the old hcp-18 gate missed. Keep; this is the round's best rule.
- **242 (+7, open_1C -> pass):** the gain was pure luck (opponents butchered themselves in
  3DX-5), and the board exposes a HOLE: W held Q3.Q.63.AQJ96432 — 11 HCP with an 8-card
  club suit — and the new system has NO opening for it (too strong for 3C's [3,9]/[5,9],
  QT-vetoed out of 1C, no 4C preempt rule). Add an exemption: waive the quick_tricks gate
  on the rule-20 minor openings when the suit is 7+ long, or extend the 3m/add a 4m preempt
  to 11 HCP. This will resurface as a loss in the next thousand boards.
- **318 (+2):** a 5-5 majors 1.5-QT hand that WON by passing (KJ642.QJ932 — ratty suits).
  Under my majors-1.5 change this reopens and the +2 is given back. Accepted: the same
  change recovers 25 IMPs on 390/424/843.
- **519, 752, 170, 195 (+23 combined):** quacky/minor-suit 1.5-QT passes that all won.
  This is why the QT gate should be relaxed ONLY for the major openings.

---

# Per-rule final recommendations

**open_1M_rule20 / open_1m_rule20 quick_tricks [2,12] ("rule of 22")** — KEEP WITH CHANGES.
Change the two MAJOR rules (open_1S_rule20, open_1H_rule20) to `quick_tricks: [1.5, 12]`;
keep the minors at [2, 12]. Add a minor-suit exemption for 7+ card suits (board 242's hole:
an 11-count with an 8-bagger must open something). Dossier ledger after the change: recovers
-11, -10, -4 (390/424/843), retains +11, +5, +5, +2, +2 (170/519/752/195/318-adjusted),
gives back only 318's +2.

**quick_tricks_outside [0,2] preempt veto (weak 2s, 3-level, 4H/4S)** — KEEP AS-IS. Not one
divergent board in the dossier traces to it; the concept (defensive tricks outside the suit
veto the preempt) is sound and evidently well-calibrated.

**3-level preempt side-major gate H/S [0,3]** — KEEP WITH CHANGES. Apply the gate only when
the side major is worth protecting: block the preempt only if `suit_quality(M) >= 1.5`.
Fixes 484 (-4, Q9874) and 357 (-1, T865) while still vetoing preempts holding KQxx/AJxx
side majors, which is the actual maxim.

**open_1S_third_light / open_1H_third_light** — KEEP WITH CHANGES. The rule fixed real
holes (459's AKT974 10-count previously had NO opening) and its two "losses" on correct
openings (131, 459) are variance. Two changes: (1) remove the weak-two overlap — require
5-card suit OR 11 HCP, so 6-card 9-10 counts open 2M as before (fixes 802, -4); (2) damp
the passed-hand raise opposite a third-seat opening — add Drury or cap the 10-11 point
3-card-support raise at 2M (fixes 84, -3, and every future clone of it).

**preemptor_pass (preempt-once discipline)** — KEEP AS-IS. No divergent board in the
dossier involves it; the encoding (keyed on i_preempted, off partner's forcing sequences)
is the right shape and the maxim is unimpeachable.

**rkc_4NT / jac_rkc void(any) + worthless_doubleton vetoes** — KEEP WITH CHANGES (three):
1. Keycard waiver: `any_of` the veto pair with `"keycards(agreed)": [3, 5]`. The classic
   prerequisites protect an asker who needs to identify WHICH cards partner holds; a hand
   holding 3+ keycards itself gets an unambiguous answer and may ask with a void or a small
   doubleton. Recovers 985 (-13), 272 (-11), 486 (-3) and, via gst, 256 (-11), while
   preserving 926 (+1, asker had only 2).
2. Fix the evaluator: `worthless_doubleton` must skip suits partner has shown 4+ cards in,
   and the agreed trump suit (985: 95 in partner's 2/1 club suit is not a flaw).
3. Once 1-2 are in, make the vetoes HARD (when:-level / a hard `veto:` block), not soft
   Gaussian factors: board 905 proved a 0.8 soft-match still buys the contract when the
   sane alternative is shadowed.

**gst_rkc_* / rj4_rkc void gate** — KEEP WITH CHANGES. Same keycard waiver (use explicit
`keycards(C/D/H/S)` since agreed_suit is not yet established at ask time). Additionally,
every context where gst_rkc can be vetoed must have a game-level floor: add an
"accept-to-game" raise of partner's minor (5m/3NT, 17+ total points, 8+ combined trumps,
above uc_pass) so a veto never strands 17+ points below game (736, -5; 256's flat 4S was
the same disease with a luckier floor). rj4_rkc: no dossier data; carry the waiver for
consistency.

**jac_wasted_signoff / spl_wasted_4M (wasted-values sign-off)** — KEEP WITH CHANGES. The
maxim is validated (+10 on 106) and the evaluator's ace-exemption is exactly right. The
required change is mechanical, not bridge: every spl/jac wasted context that defines call
4M must also contain a catch-all 4M sign-off (requires: {}, low priority) so it can never
shadow the generic game bid out of existence (905, -11).

**rkc5D_slam_* (0-or-3 disambiguation by counting)** — KEEP AS-IS. +24 IMPs across 691/660,
and on 669 it also judged correctly (it signed off; the escape crashed). The best rule of
the round.

**rkc5D_signoff_* minor 5NT escapes** — KEEP WITH CHANGES. Default the escape to 6 of the
agreed minor; allow 5NT only when the asker is notrump-shaped (`singleton_or_void: [0,0]`
and `worthless_doubleton: [0,0]`). 6m-1 is a bounded -50/-100; 5NT with an unstopped suit
is -500 (669, -10). Also make the `rule_of_26 >= 31` prerequisite on minor-agreed 4NT asks
hard-blocking: on 669 it soft-matched opposite a 1-count, and with a minor agreed a
0-keycard reply has no safe landing, so the ask must not fire on a leaning fit.

**Engine-level (cross-cutting):**
1. Boolean [0,0] gates as `requires` are unreliable by design (soft-match ~0.8): add hard
   veto semantics and use them for every Blackwood prerequisite.
2. A specific context that defines a call must provide a floor rule for that call
   (905-class shadowing).
3. A veto rule should be required (by convention or by lint) to name its fallback: "veto
   4NT" is only sound bridge when the hand still reaches the right GAME — three of the five
   veto losses were fallbacks landing below the obvious contract.

Net effect if implemented mechanically as written: of the ~-46 IMP regression, roughly
-38 came from the Blackwood-veto family + the 905 shadowing + the 669 escape (all fixed
without touching the maxims' souls), ~-25 from the majors QT gate (fixed by the 1.5 split,
cost ~2 back), ~-9 from preempt/third-seat gating detail (fixed by the quality and overlap
exceptions). The genuinely-nothing-wrong boards (131, 342, 448, 459, 181) total about -20
of variance that no rule change should chase.
