# Round 13 — one board at a time, one verdict per decision

Method: generate deals, play BEN, and on every board we LOSE, sit in each of our
seats in turn and give the call exactly one verdict — OK / CATEGORY (the
situation was filed as the wrong kind of auction) / EXCEPTION (the rule is right
in general, wrong here) / RULE-WRONG (wrong wherever it fires).  Stop at 20
suggested fixes, then send them to a critical expert.

Corpus: seed 131313.

---

## Board 31 (-13)  N/S bid 5H making 12; BEN's N/S bid 6H.  Table B: all 11 of
our decisions were pure defence and BEN agreed with every one — nothing there.

| decision | verdict |
|---|---|
| a1 N 1C (open_1C), a3 S 1H (r1m_1H), a7 S 4NT (rj4_rkc), a9 N 5C (rkc_5C) | **OK** — 5C is the correct 1430 answer with four keycards |

**FIX 1 — CATEGORY.** `[a13]` N holds four keycards, answered 5C (=1 **or** 4),
and partner signed off in 5H believing it might be one.  N's seat matches **no
context at all** (`contexts: []`) and falls to the code fallback pass at
priority 8.  The 1430 5C reply is ambiguous by construction and the pair that
resolves it is the ANSWERER: with four keycards you must bid on over a sign-off.
An ask shipped without the seat that finishes it — the project's own hard
constraint 3, in the RKC ladder itself.

**FIX 2 — EXCEPTION.** `[a11]` S asks, holds one keycard and the trump queen,
and `rkc5C_slam` requires three or four keycards *in the asker's own hand*, so
S signs off.  The gate is pure arithmetic and ignores the partner model: partner
jumped to 4H showing 19+ support points, S holds 15, and 34+ combined with the
trump queen is not a 5H hand.  The rule is right in general (one keycard
opposite one is two of five) and wrong when partner's shown strength makes the
1-keycard branch untenable.

**FIX 3 — RULE-WRONG.** `[a5]` N rebids 4H on `A.AJT6.AJ8.A8542` — 19 HCP,
singleton spade, four-card support, ~22 support points.  `ob_raise_4H` reads
"19+ support points" with **no upper bound**, so every hand from 19 to 24 blasts
the same game raise, and there is no splinter anywhere in
`opener_rebid_1m_1M` / `opener_rebid_1C_1H_extras`.  BEN splinters 3S at 0.76.
A top rung with no ceiling is wrong as written; the repair must be the rung
above it, not a ceiling on it.  (Noted: not the proximate cause of this board's
loss — the auction reached the ask anyway.)

---

## Board 22 (-10)  We let them play 4S at one table and bid ourselves to a failing
5S at the other.  All four opening/response decisions OK; `rkc5C_signoff` at
`[b13]` is the rule working correctly (three keycards, no trump queen, an
eight-card fit — a trump loser, not a finesse) and is NOT a defect.  `[b15]` is
FIX 1 again: the 5C answerer has no context after the sign-off.

**FIX 4 — RULE-WRONG.** `[b7]` E holds `KQT632.86.QJ9.QJ`, **11 HCP with six
spades**, opposite a 12-14 rebid, and bids a GAME-FORCING 3S.  The ladder over
a 1NT rebid is `rr_nt_pass` 6-10, `rr_nt_2$M` 6+M/6-10, `rr_nt_2NT` 11-12 but
explicitly `not: { $M: [6,13] }`, `rr_nt_gf3_$M` 5+M/**12**-18,
`rr_nt_4$M` 6+M/13-18.  **Eleven with a six-card major fits nothing**: pass,
2S and 3S all fit 0.80 and the soft-miss lottery hands it to the highest
priority, which is the game force.  Two defects in one place:
  * the invitational call with a six-card major does not exist; and
  * `rr_nt_gf3_$M` establishes a GAME FORCE from **12** opposite a 12-14 rebid,
    i.e. on 24 combined points.  A hand that may belong in a partscore cannot
    be forcing to game.
BEN bids 2D at 0.98.  The 3S drove partner to RKC and a failing 5S.

**FIX 5 — CATEGORY.** `[a8]` S holds `74.KQ742.A543.62` — 9 HCP, a bare
ten total points — vulnerable, and bids 2H after `1C - (P) - 1S - (P) - 1NT -
(P) - 2D`.  BEN passes at **0.99**.  `cl_new_H2` reads "natural H at the
cheapest level: 5+ cards, 10+ points" and fits 1.00.  But this is not a
competitive auction: `is_competitive` is **False**, our side has never bid, and
the opponents have exchanged four constructive calls showing `their_min_hcp=15`
and `their_max_fit=7`.  Entering at the two level, vulnerable, on a minimum,
opposite a partner who has passed twice and into a disclosed fit, is a free shot
at -200.  `general_competitive_low` files "they are having an auction and I have
not spoken" identically with "we are both competing", and the ten-point floor
that is right for the second is much too low for the first.

---

## Board 30 (-7)  We bid 4H down two, vulnerable, at one table and played 3C at
the other holding an eight-card spade fit.

`[a0]` `[a2]` `[a4]` `[a8]` `[a10]` `[b1]` `[b5]` `[b11]`: **OK**.
`[a6]` N invites with `J5.JT83.AQT95.54` — 8 HCP and two doubletons, which the
support-point rule correctly totals at 10 opposite partner's shown 10-21.  BEN
passes at 0.88 and 4H went two down, but the arithmetic is textbook (void 5,
singleton 3, doubleton 1) and raising its floor is threshold tuning, which
DECISIONS already measured at -0.025 +/- 0.062.  **OK — a defensible
judgment call, recorded in the residue rather than as a fix.**

**FIX 6 — RULE-WRONG.** `[b3]` After `1D - (P) - 1H - ?` E holds
`AQ76.A2.832.K962` — 13 HCP, **four spades and four clubs, the two unbid
suits**: the textbook sandwich takeout double.  `sw_X` requires
`suits: { $o: [0, 2] }` — *shortness in opener's suit* — or 17+, so E fits 0.35
and passes.  That is the DIRECT-seat takeout requirement, where only one suit
has been bid, transplanted into a seat where **both** opponents have named a
suit.  In the sandwich seat a double is takeout of both of them, i.e. it shows
length in the two unbid suits; length in opener's suit is neither necessary nor
sufficient.  BEN doubles at 0.65.  E/W hold an eight-card spade fit and never
found it.

**FIX 7 — RULE-WRONG.** `[b9]` Advancing partner's balancing double, W holds
`T832.Q64.4.QJT87`: four spades, five clubs.  `adx_pull_C3` and `adx_pull_S2`
carry the **same `shows` text** — "pulling the double to the cheapest 4+ suit" —
but the club rung fits 1.00 on five cards where the spade rung fits 0.80 on
four, so the ladder bids a MINOR at the THREE level in preference to a MAJOR at
the TWO.  It says cheapest and implements longest.  Partner held `AQ76`: 2S was
the eight-card major fit, one level lower.  BEN bids 2S.  (Independently found
by reviewer A last round: `general_pull_or_sit`, par gap -4.05 over 84 tables.)

---

## Board 36 (-6)  S holds a six-card heart suit and 17 HCP opposite a weak two
and the pair played 3NT down one.  Par was +650.

Everything else **OK**; `[a6]` and `[a8]` are downstream of the one defect.

**FIX 8 — EXCEPTION.** `[a2]` Opposite N's weak 2D, S holds
`KQT9.AJ9872.Q3.A` — 17 HCP with **six good hearts** — and bids the 2NT feature
ask.  BEN bids 2H at **0.98**.  `rw2_2NT_ask` ("strong inquiry (15+), asking for
a feature") has **no shape condition at all**: priority 70 against the natural
forcing new suit `rw2_new_D_$M` at 63, so it fires on every 15+ hand, including
one holding a self-sufficient six-card major.  The ask is for hands that want to
play in partner's suit or in notrump; with your own six-card major you bid it.
Downstream, the ask continuation has no rung for "my own major" either, so
after 3S the hearts could never be shown and 3NT was the only game available.

---

## Board 9 (-5)  We defended well at one table (+110) and went for 300 in a
balancing 2NT at the other.

`[a1]` `[a5]` `[a7]` `[b0]` `[b2]` `[b4]` `[b6]` `[b8]` `[b12]`: **OK**.
`[a3]` N runs a doubled 1NT to its own five-card spade suit; BEN plays a 2C
scramble we do not play.  A system difference, not a defect, and it produced
+110.

**FIX 9 — RULE-WRONG.** `[b10]` W holds `K96.T93.KJ5.AKQJ`, 17 HCP.  W has
already doubled 1NT for penalty; the opponents ran 2C - 2D - 2S and **partner
passed at every turn**.  W now bids 2NT and goes three down for -300 where
defending 2S was a plus.  The rule is `ballow_nt2_strong`, whose own `shows`
text reads *"natural 2NT: 17-21 balanced with their suit stopped, **partner
still unlimited**"* — and it carries **no condition of any kind on partner**.
The engine's own model at that moment says partner is 0-11.  A rule that states
a condition in its explanation and does not implement it is wrong wherever it
fires; the condition is now expressible (`when: { partner_limited: false }`).
BEN passes at 0.89.

---

## Board 25 (-5)  We defended 1NT for +90 at one table and bid 3NT down one at
the other on 23 combined points.

`[a3]` N passes over 1D with 14 balanced and three diamonds; the 1NT overcall
needs 15 and the takeout double needs shortness, so there is no action — and
passing a flat 14 over 1D is normal.  BEN doubles at 0.98 but **OK**, and the
contrast is useful: `oc1D_X`'s shortness requirement is right in the DIRECT
seat, which is exactly why FIX 6 is about the sandwich seat only.
`[a1]` `[a5]` `[a7]` `[a9]` `[a11]` `[b0]` `[b2]` `[b4]` `[b6]` `[b12]`: **OK**.
`[b8]` E raises to 2S on a flat 3-4-3-3 eight-count with three trumps where BEN
bids 1NT at 1.00 — a matter of style, **OK**.

**FIX 10 — RULE-WRONG.** `[b10]` W holds `AQ93.73.A9842.KJ`, 14 HCP, opposite a
partner who has bid `1H` over their takeout double — a call the engine itself
reads as **6-9** — and bids 3NT.  That is 20-23 combined for a nine-trick game.
`uc_nt3` requires `hcp: [13, 19]` and **nothing about partner at all**: no
`rule_of_26`, no reference to `partner_max_hcp`, which the engine has known all
along.  BEN passes at 0.95.
**Caution for the reviewer:** DECISIONS rules `uc_nt3` a symptom four rounds
running and records that raising its *strength gate* measured +1 over 1000
boards.  This is a different proposal — a combined-values condition against
partner's shown CEILING, which was not expressible until this round — but it
touches a protected rule and must be measured alone.

---

## Board 4 (-4)

`[a0]` `[a2]` `[a4]` `[a8]` `[b1]` `[b5]`: **OK**.  `[b3]` W doubles their 2S
jump overcall holding 2-6-1-4; `nxj_X` reads "support for the unbid suits" and
six hearts and four clubs *is* that, and "a double must not hide a six-card
suit" was measured across 113 firings and killed in round 8.  **OK.**

**FIX 11 — RULE-WRONG.** `[a6]` S holds `A97542.AJ2.982.4` — six spades — after
`(P) 1D 1S (2H) 2S (3D)`.  Partner has raised, so we hold a **nine-card fit**,
and the auction is competitive with both opponents bidding.  We pass.  Both
three-level rungs miss: `ch_raise_S3` and `ch_rebid_S3` each carry
`rule_of_26: [22, 99]` and the estimator reads **20** (12 total points plus
partner's midpoint 8), so both fit 0.41.  Their `lott_total_trumps` gate — which
they *do* disclose — is satisfied at 9.
The defect is one of honesty as much as of bridge: **`shows` reads "3+ trumps,
10+ support points, 8+ combined trumps" and says nothing about a combined-values
test, while the constraint carries one.** Either the sentence or the gate is
wrong, and a rule whose explanation omits the gate that actually decides it
cannot be reasoned about.  Same species as FIX 9.
**Caution for the reviewer:** reviewer A measured "the Law at the THREE level"
last round at 62 tables, par gap +2.60 — i.e. *dead* — so this must not be sold
as a Law fix.  The claim here is narrower: disclose the gate or drop it.

---

## Boards 10 (-4) and 35 (-2) — no fixes

**Board 10.** Par is -800: the opponents own the deal and we escaped for -4.
`[a2]` N overcalls 2C over their 1NT on `Q95.AJ.62.KQ6432` (six clubs, 11) — a
normal action, BEN passes at 0.89, **OK**.  `[b1]` W opens 1D on a 5-4-2-2
sixteen-count where BEN opens 1NT at 0.80; the hand is not balanced by the
system's own definition and opening style is scope-excluded in DECISIONS.
**OK.**  `[b3]` E raises to 2D holding six spades and a void in their suit — a
distortion, but BEN's alternative is *pass*, not 2S, and a new suit at the two
level over an overcall would promise 10+.  Judgment, **OK**.  Everything else
BEN agreed with.

**Board 35.** `[a1]` N passes over 1H with a flat 13 and three hearts; BEN
doubles at 0.91, but `oc1H_X` correctly requires shortness in the DIRECT seat —
the same rule that is right here and wrong in the sandwich seat (FIX 6).
**OK.**  `[b2]` E answers their takeout double with 1NT on a 3-2-4-4 seven-count
whose points are four jacks and a ten; `rx_H_1NT` says "6-9 balanced" and that
is what E holds.  BEN passes at 0.99 and the texture argument is real, but the
rule is by the book and the board cost 2 IMPs.  **OK.**

---

# Batch 1 summary: 9 losing boards of 40, **11 suggested fixes**

Decisions examined: 109 across both tables of the nine boards.  BEN agreed with
us on 79 of them.  Of the 30 disagreements, 19 were ruled OK — style, a
scope-excluded threshold, or a rule that is correct in its own seat.

---

# Batch 2 (boards 41-100): 16 more losing boards

## Board 44 (-13)  Par is -1430 to E/W; we were E/W at table B and went one down
in 4S.  Table A was seven consecutive passes and BEN agreed with every one.

`[b1]` `[b3]` `[b9]`: **OK** — and `[b5]` E rebids 2C on 1-3-4-5 with 15, where
2D would be a reverse promising 17.  Correct, BEN's 1NT notwithstanding.

**FIX 12 — CATEGORY.** `[b7]` W holds `AT9763.AKQ9.73.9` — **six spades and
four hearts** — after `1C - 1S - 2C`, and bids 4S.  The whole
`responder_after_minor_rebid` ladder is one-suited: `rmr_4S` "6+ S, game
values", `rmr_3S` invitational, `rmr_3NT`, `rmr_2NT` — **there is no rung for a
second suit anywhere in it**, so a 6-4 hand is filed as a one-suiter with game
values and the four-card major is never shown.  BEN bids 3H at 0.61.  Same
species as the standing open item "a 6-5 hand rebids the six-card minor and
never shows the five-card major", one context along.

---

## Board 54 (-11)  We took +50 defending 4H where BEN's N/S made 4S for +620.

`[a0]` S passes a 10-count that makes the rule of 20; opening style is
scope-excluded and BEN's 1C is only 0.60.  **OK.**  `[a2]` `[a4]` `[b1]` `[b3]`
**OK**.  `[a8]` is downstream of `[a6]`.

**FIX 13 — EXCEPTION.** `[a6]` N holds `K98765.53.J72.AK` — six spades, 11 HCP.
We overcalled 1S, partner cue-bid 2H (`advo_cue`, "good raise of the overcall,
11+"), and RHO jumped to 4H.  **We have a nine-card fit opposite a limit raise
and we pass.**  BEN bids 4S at 0.92.
The arithmetic, traced: `total_points` 13, `lott_total_trumps(S)` **9**,
`rule_of_26` **24**.  `ch_raise_S4` needs `rule_of_26 >= 25` and misses by one —
partner passed as dealer, so the model caps partner at 11, the cue-bid floors
them at 11, and the midpoint is exactly 11.  A combined-values test decided a
purely competitive question, again.
The Law rung added in round 12, `ch_raise_lott4_S`, would cover it — but its
`their_fit >= 8` gate reads **5**, because W overcalled 1H and then jumped to 4H
**alone**, so the opponents never mechanically "showed" a fit.  That gate was
right on the boards that motivated it and is too literal here: **a voluntary
jump to game is itself the announcement of a fit or a self-sufficient suit**,
and the total-trick count is high whether or not a second opponent confirmed it.
Expressible as `when: { standing_bid_level: [4, 5] }` as an alternative to the
`their_fit` branch.
**Caution for the reviewer:** without `their_fit >= 8` the four-level Law rung
measured **+1** over 1000 boards in round 12 and with it **+12**.  Any loosening
must be measured alone and must not simply restore the coin flip.

---

## Board 56 (-10)  Table A: nine consecutive passes, BEN agreed with all of them.

**FIX 14 — CATEGORY.** `[b7]` After `1D - 1S - 2H`, W holds
`Q9752.T76.2.AKQ8` — 11 HCP, five spades, four clubs — and **passes partner's
reverse**.  BEN bids 3C at 0.99.
Traced: the engine knows the call is forcing (`pass_forbidden` is **True**,
`last_forcing: one_round`).  There is **no `responder_after_reverse` context at
all**, so the seat falls to `general_uncontested_continuation`, whose cheapest
natural rung `uc_new_C3` demands **14+ points**.  Nothing fits above the
`FORCED_BID_MIN_FIT` floor of 0.30 — the best bid is 0.14 — so the forced-pass
relaxation in `decision.py` re-admits the catch-all `uc_pass` and it wins at fit
1.00.  The relaxation is behaving as designed; the hole it is papering over is
that a force was authored without the seat that answers it.  Third instance of
that species this round (FIX 1, FIX 8's continuation, this).

---

## Board 86 (-10)

`[a0]` `[a2]` `[a6]` `[a8]` `[a10]` `[b3]` `[b11]` `[b13]`: **OK**.
`[a4]` BEN doubles their 3C at 0.89 where we pass; the penalty double fits 0.41
and DECISIONS already records the competitive-double family as measured.  **OK.**
`[b1]` W passes `Q97653.Q7.J.JT76` where BEN makes a weak jump overcall — the
known open item measured at -24 held out in round 11.  **OK.**
`[b7]` `[b9]` are downstream.

**FIX 15 — CATEGORY.** `[b5]` After `1C - (P) - (P) - X - (2C)`, W advances
partner's balancing double with 2S on **seven HCP**, and the rule that fires is
`cl_new_S2`: *"natural S at the cheapest level: 5+ cards, **10+ points**"*.  The
distributional count just reaches ten, so partner reads a free 10+ overcall,
and E — 18 HCP — asks for keycards and lands in 5S, one down.  The position is
not a free natural overcall: it is the **advance of partner's takeout double**,
where a suit response promises nothing and is capped, not floored.  The engine
has an `adx_*` ladder for exactly this (`general_pull_or_sit`) but it is only
reachable when RHO passes; the moment RHO competes, the advance is filed as an
ordinary competitive new suit and its meaning inverts.

---

## Boards 49 (-9) and 87 (-8)

`[a1]` (49) and `[b0]` `[b2]` (87): opening style, scope-excluded.  **OK.**
Board 87 table A was four passes with BEN agreeing throughout.

**More evidence for FIX 5.** `[a5]` (49) S holds `AKJT3.T4.QT8.J84`, 11 HCP, and
bids 2S over `(P) (P) 1NT (P) 2C` — into a Stayman auction, opposite a partner
who has already passed.  BEN passes at **1.00**, the highest confidence in the
corpus.  We were doubled for -500.  Same rule (`cl_new_$X2`), same shape of
error as board 22 `[a8]`: a ten-point floor written for a competitive auction,
applied to a seat that is injecting itself into the opponents' constructive one.
**Two losing boards, BEN at 0.99 and 1.00.**

**More evidence for FIX 10.** `[b6]` (87) E bids 3NT on 15 HCP after
`(P) (P) 1C (1D) 1H (2D)` — partner's one-level response in competition may be
six — via `cl_nt3`, "natural 3NT: 13-19 balanced, their suits stopped".  BEN
passes at 0.78.  **The generic three-notrump rules `uc_nt3` and `cl_nt3` bid a
nine-trick game off a raw HCP band with no reference to what partner has shown,
and it has now cost three boards in one hundred** (25, 49, 87).

**FIX 16 — CATEGORY.** `[b4]`/`[b6]` (49) E advances partner's 1NT overcall with
an invitational 2NT on nine HCP; W holds a **minimum 15** and accepts with 3NT,
two down.  W's seat matches no specific context — the invitation lands in
`general_uncontested_continuation` and is answered by `uc_nt3` (13-19 balanced),
which accepts across the **entire** band.  **An invitation whose answering seat
is a rule that always says yes is not an invitation.**  This is the FIX 1 / FIX
14 species seen from the other side: there, a force had no answering seat and
was passed; here an invitation has none and is always accepted.

---

## Boards 99 (-6), 67 (-4), 57 (-3), 97 (-3)

**FIX 17 — RULE-WRONG.** A one-level overcall is blocked by suit quality on
hands that must bid.  Two boards, BEN at 0.96 and 1.00:
  * 99 `[a5]` N holds `K8762.J9.J5.KQT7` (11 HCP, five spades) after
    `(P)(P) 1D (P) 1H` and passes.  `sw_1S` requires
    `suit_quality(S): [1.5, 9]` — its sibling `oc1D_1S`, the same call one seat
    earlier, requires only `[1, 9]`.  **A gate given to one rule and not its
    sibling, in the direction that makes the cheaper call harder than the
    dearer one.**
  * 67 `[a1]` N holds `K6.K5.T96542.AQ7` — **twelve HCP and six diamonds** —
    over 1C, and passes, because `oc1C_1D`'s `suit_quality(D): [1, 9]` reads
    below one on `T96542`.  BEN overcalls 1D at **1.00**.
A one-level overcall risks nothing and its purpose is partly the lead; a
texture gate written for the two level has been applied to it.

**FIX 18 — CATEGORY.** 67 `[b4]` W holds `AQ.A8.KQ83.K8642` — **seventeen
HCP** — opened 1C, LHO overcalled 1D, partner passed, RHO passed, and W
**passes it out at the one level**.  `ballow_X` cannot fire (see FIX 19) and
nothing else does.  The seat is filed as `general_balancing_low`, "balancing
opposite a passing partner" — but this is *opener's reopening seat*: we have
already promised 12+ and hold 17, so partner's silence limits partner, not us.
The standing DECISIONS open item ("no opener's reopening/second double") now has
a losing board attached and a plain one-level instance.

**FIX 19 — RULE-WRONG.** 57 `[a7]` N holds `J84.AJ63.K92.KQ7`, 13 HCP, after
`(P)(P) 1S (P) 2S (P)(P)` and passes it out.  BEN doubles at 0.89.  `ballow_X`
reads *"balancing double: values are marked opposite a passing partner"* and its
constraint is `hcp 11+ with standing_suit_length <= 2`, **or** `9+ with <= 1` —
i.e. it silently demands shortness in their suit, which the sentence never
mentions.  The balancing double is precisely the double you make **without**
shortness: partner is marked with values and the auction is dying.  Text and
constraint disagree, same species as FIX 9 and FIX 11.

**FIX 20 — CATEGORY.** 97 `[a5]` S opened 1D, LHO overcalled 1H, partner
responded 1S, RHO bid 2H.  S holds `Q53.AK42.K863.43` — 13 HCP with **exactly
three-card spade support** — the textbook support-double position.  BEN doubles
at **1.00**.  We pass: the live contexts are `['general_competitive_low',
'general_slam_try']` and the best non-pass candidate is `cl_raise_S2` (6-9
support points) at fit 0.80.
The `support_double` context exists — `pattern: "1$m - P - 1$M - bid<2$M - ?"` —
but it requires **LHO to have passed**.  Once LHO overcalls, which is the
commonest way this position arises, the convention silently disappears and a
thirteen-count with three trumps has no call at all.

### Non-finding worth recording

On three losing boards (25 `[a3]`, 35 `[a1]`, 57 `[a3]`) BEN makes a direct-seat
takeout double at 0.98 / 0.91 / 0.95 on a **flat 13 with three cards in their
suit**, where `oc1x_X` correctly requires shortness and we pass.  Three
high-confidence disagreements, one consistent shape, and I believe our rule is
right and BEN is simply more aggressive than the system's stated style.  Listed
so the reviewer can overrule me with data rather than rediscover it.

---

# TOTAL: 20 suggested fixes from 25 losing boards (100 deals, seed 131313)

397 of our decisions examined across both tables.  BEN agreed with 290.  Of the
107 disagreements, 87 were ruled OK — style, a scope-excluded threshold, a rule
that is correct in its own seat, or a consequence of an earlier error.

By verdict: **CATEGORY 8** (1, 12, 14, 15, 16, 18, 20, and 5) ·
**EXCEPTION 3** (2, 8, 13) · **RULE-WRONG 9** (3, 4, 6, 7, 9, 10, 11, 17, 19).

Recurring species, in order of how often they appeared:
1. **A force, an ask or an invitation authored without the seat that answers
   it** — FIX 1 (RKC 5C answerer), FIX 14 (reverse), FIX 16 (2NT invite), and
   the continuation half of FIX 8.  Four instances in one hundred deals.
2. **A rule whose `shows` sentence does not state the gate that actually
   decides it** — FIX 9, FIX 11, FIX 19.  This is an explainability defect
   first and a bidding defect second.
3. **A combined-values test deciding a competitive question** — FIX 11, FIX 13.
4. **A gate given to one rule and not its sibling** — FIX 6, FIX 17.
5. **The generic notrump and pass floors ignoring the partner model** — FIX 10,
   FIX 16.
