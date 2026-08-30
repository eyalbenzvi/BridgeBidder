# An expert bridge review of the engine's agreements

Read as a bridge player, not as a programmer.  Nothing in the repository was
changed except this file.

Everything below is computed on **both** measurement corpora and quoted on both:
`reports/e10_final.jsonl` (seed 242424, 1000 boards, **-677**) and
`reports/held_final.jsonl` (seed 828282, 1000 boards, **-474**).  Where a number
does not replicate I say so and drop the claim — three of my first six candidate
findings died that way and they are recorded in §7.

---

## 0. The one number this review is built on

Every board was solved double-dummy (`endplay`, all 20 contracts, both corpora)
and the corpus split by **how many tricks the best-placed side can actually
take**:

| deals where the best side can take… | e10: n / IMPs / per board | held: n / IMPs / per board |
|---|---|---|
| **12 or 13 tricks (a slam is there)** | **137 / -267 / -1.95** | **144 / -320 / -2.22** |
| exactly 11 | 210 / -27 / -0.13 | 217 / **+127** / +0.59 |
| 10 or fewer | 653 / -383 / -0.59 | 639 / -281 / -0.44 |

**On the held-out corpus, 67% of the entire -474 deficit sits on the 14% of
deals where somebody can make twelve tricks.**  Outside that band the engine is
-154 IMPs over 856 boards — **-0.18 a board**, which is close to parity with a
neural net trained on expert auctions.  On the review corpus the same slice is
39% of the loss.  The direction and the per-board magnitude replicate; the
share differs only because e10 is a worse corpus overall.

The supporting count is starker than the IMPs:

| | e10 ours / BEN | held ours / BEN |
|---|---|---|
| small slams bid | **30 / 61** | **26 / 63** |
| …of which made | 18 / 35 | **23 / 41** |
| grand slams bid | **0 / 2** | **0 / 3** |
| contracts declared | 904 / 1047 | 905 / 1047 |
| calls at the 6 level | 30 / 59 | 26 / 62 |

Held out, **23 of the 26 slams we bid made — 88%.**  BEN's hit rate is 65%.  At
IMPs the break-even for bidding a non-vulnerable small slam instead of game is
about 50% (vulnerable, about 45%).  An 88% hit rate is not accuracy, it is
**evidence of massive under-bidding**: we only bid the ones that cannot fail.
The slam machinery this project has built is *sound*.  It almost never runs.

Sixteen rounds have been spent on rule-level defects in competitive and
responding contexts.  On the held-out corpus those contexts are collectively
worth about a fifth of an IMP a board.  The money is in one place and it has a
bridge name: **the partnership cannot investigate a slam.**

---

## The five ideas, ranked by expected value

---

## 1. Give the partnership a slam try that is not Blackwood — above game, and with a minor

### The bridge

Once trumps are agreed and the auction has reached game, a strong pair still has
three things to say: *I have a control you don't know about* (a five-level cue),
*I have more than I have shown, decide* (five of the agreed suit as a general
try), and *I am asking* (Blackwood).  This engine has only the third.  Its cue
ladder is deliberately capped — the file says so in a comment: "a cue chain can
never push past 4M" — and `cue_bidding_S` / `cue_bidding_H` exist **only** with
a major agreed, **only** inside a formal `game_forced` auction, and **only**
while the standing bid is at the three or four level.  There is no cue with a
minor agreed, none in a competitive auction that reached game without a formal
game force, and none above game.  Everything else in the file is additionally
gated `we_hold_contract: false`, which is the harvest-loop's "never bid over
your own side's contract" guard.  That guard is right for a competitive
partscore and catastrophic for a slam auction: it makes *reaching game* the
event that ends the partnership's conversation.

### The evidence

Take the seat where a hand that any expert would move on has to pass.
`repro.rank` on the real positions:

- **e10 board 192, table A.**  `1S (3C) 3D (4C) 4S (P)` — South holds
  `842.AKT2.AKT952.`: a **club void in the opponents' suit, AK AK, 14 HCP**,
  opposite a partner who opened 1S and jumped to 4S over 4C.  Candidate set,
  in full: `P` (code fallback, fit **1.00**) and `4NT` (`gr_rkc_general_S`, fit
  **0.00**).  We played 4S making thirteen; BEN bid 6S.  **-11.**
- **e10 board 266, table B.**  `1H (3D) 4D (P) 4H (P)` — East holds
  `Q9432.AT85..AK54`: a **diamond void**, the ace of the agreed suit, AK of
  clubs, and East has already shown a limit raise or better with the 4D cue.
  Candidate set: `P` at 1.00, `4NT` at 0.00.  6H was cold.  **-13.**
- **e10 board 677, table A.**  `(P) 1D (1H) 1S (3H) 3S (P) 4S (P)` — South
  holds `KT54.Q83.AJT2.KT` opposite a partner who has bid spades twice
  freely.  `P` at 1.00, `4NT` at 0.004.  6S made twelve.  **-13.**

That is not three anecdotes; it is the shape of the whole population.  Our
passes of our own side's game contract number **456 (e10) / 432 (held)**.
Restrict to hands with **4+ controls and a singleton or void** — the shape that
wants to move — and there are **71 / 73** of them, at par gap **-6.62 / -4.78**
against **-3.30 / -2.91** for the rest of the same population, and board margin
**-2.07 / -0.82** against **-0.25 / +0.11**.

I then re-scored 60 of those 71 seats through the engine.  **Mean number of
non-pass candidates offered: 1.6.**  In 46 of 60 the best non-pass call fits
below **0.10**; in 57 of 60 below 0.50; in **0 of 60** does any non-pass call
fit 0.90.  Five seats have no non-pass candidate at all.  The only calls the
engine ever offers there are 4NT (50 of 60), 6NT (19), 6H (5) and a return to
game (6).  **There is no slam try in the file above the four level.**

And the counterfactual is measured, not imagined: **28 (e10) / 25 (held) boards
where a slam is double-dummy cold, BEN bid it and we stopped — -166 and -219
IMPs.**  When we *do* bid one BEN missed, we gain: 5 boards **+37**, 4 boards
**+50**.

### What changes in the file

Two new rungs and one relaxation, all additive in the seats that matter:

1. **`slam_try_over_game_raise` needs more than `gr_rkc_$M`.**  Add a five-level
   cue ladder to it — `5C` / `5D` / `5H` showing first-round control cheapest-first
   with the agreed suit as trumps, priority just under the keycard ask, gated on
   `control_in($X): [2,2]` plus a partnership test (see idea 2) — and a
   **"five of the agreed suit" general slam try** at the bottom of the ladder
   ("more than I have shown, bid six with a maximum"), with the answering seat
   authored in the same batch.  The existing `cue_S_signoff` / `cue_H_signoff`
   pattern gives the negative inference for free.
2. **Extend `cue_bidding_*` to the minors** (`cue_bidding_C`, `cue_bidding_D`)
   and drop the `game_forced: true` requirement in favour of
   `agreed_suit + standing_bid_level >= 3`, so a competitive auction that has
   agreed a suit at the three or four level can still cue.
3. **Carve `we_hold_contract: false` for slam machinery only.**  The guard
   should read "never bid over our own contract *below game*"; above game the
   correct guard is "never bid over our own contract unless the call is a cue,
   a keycard ask, or a general slam try".

### What it endangers, and how far it reaches

It removes "pass" from about **70 seats per 2000 tables** (3.5% of tables,
one seat each), and it puts us at the five level on hands where four was making.
That is the real risk and it is the same one that killed round 8's keycard
experiments: **a slam try that partner cannot decline safely is worse than no
slam try.**  Mitigations that must ship in the same batch: the five-level cue
ladder must live only when the agreed suit is a **major** or the standing
contract is already at the five level (so declining costs nothing), and the
"five of the agreed suit" try must be gated on the *pair* having the trumps
(`lott_total_trumps(agreed) >= 9`), not on my own values.  Per §4 of
ROUND_METHOD, every one of these rungs deletes the code fallback for its call in
every seat its `when` reaches — here that fallback is a pass, so the suppression
is exactly the intended behaviour, but it must still be replayed before it is
believed.

### Does it pay against a *bot*?

Yes, and more than against a human field.  BEN bids twice as many slams as we
do and gets 65% of them home; a bot opponent will not double our failures and
will not find the killing lead against a thin slam any better than double-dummy
already says.  The IMP asymmetry is brutal and one-directional: missing a cold
slam is -11 to -13 every time, bidding a failing one is -5 to -6.  We are on the
wrong side of a 2:1 payoff.

---

## 2. Change the currency of every slam decision from points to tricks

### The bridge

The engine has exactly one way to talk about combined strength, and it is
`rule_of_26`: my total points plus a *midpoint estimate* of partner's shown
range.  Open `evaluation/evaluators.py`:

```
floor = max(ctx.partner_min_hcp, ctx.partner_min_points)
partner_mid = (floor + min(max(ctx.partner_max_hcp, floor), floor + 4)) / 2
```

**Partner is never credited with more than two points above his announced
minimum**, however wide his range.  Opposite a 1S opening (12-21) partner is
worth 14.  So a slam gate written as `rule_of_26 >= 31` demands **17 total
points of my own** — and every slam gate in the file is written that way:
`gst_rkc_*` wants `total_points >= 15, controls >= 4, rule_of_26_sharp >= 31`;
`gr_rkc_general_$M` wants `total_points >= 17, controls >= 4, rule_of_26 >= 31`;
even the *cue bids* want `rule_of_26 >= 28`.  Board 192's South — 14 HCP, a
void, four top honours, a five-loser hand — is not close.  This is why the
slam-try context ranks worst in the file: it is not that the rules are wrong,
it is that they are gated on a quantity that cannot see a fit.

That is also bad bridge on its own terms.  Once trumps are agreed, points stop
being the right currency.  Every strong partnership switches to **losers,
controls and fit**: nine combined trumps with two aces and a singleton is a slam
try on 25 combined HCP, and 32 balanced HCP with two fast losers in the same
suit is not.  The file already has the evaluators — `ltc`, `controls`,
`quick_tricks`, `lott_total_trumps`, `void`, `singleton`, `top_honour`,
`wasted_in_partner_shortness` — and **`ltc` is used exactly once in 14,937
lines** (the 2C opening), while `rule_of_26` is used **104 times**.

### The evidence

- The gate arithmetic above, which is a fact about the code, not an opinion.
- **After a 2C opening partner's shown minimum is zero by construction**
  (`r2c_2D_waiting` is `requires: {}`), so `rule_of_26` credits a 2C opener's
  partner with **2 points**, and every `rule_of_26_sharp >= 31` gate in the file
  is unreachable in the strongest auction the system has.  `resp_2C` and
  `open_2C` have been the file's worst-replicating families for four rounds
  (`open_2C`: 16 / 19 decisions at par gap **-7.44 / -6.58**) and this is why.
  e10 board 782: `2C P 2NT P 3D P 3H P 4D P 5D` — 21 HCP opposite a positive
  response stops in 5D with twelve tricks and a 1440 par.  **-13.**
- The population from idea 1 (71 / 73 seats, gap -6.62 / -4.78) is the same
  population: those hands fail `rule_of_26`, not `controls`.

### What changes in the file

1. **A new evaluator, not a change to `rule_of_26`.**  `rule_of_26` gates 104
   rules including ordinary game raises; touching it would move every game
   threshold in the system and is exactly the sort of wide edit that has cost
   this project whole rounds.  Register instead something like
   `partnership_tricks` — my losers, reduced by partner's shown minimum length
   in the agreed suit and by my controls, or equivalently a "combined losers"
   count — and use it **only** in the slam gates (`gst_rkc_*`,
   `gr_rkc_*`, `cue_*`, and the new rungs from idea 1).
2. **Re-express the slam gates as a disjunction**: `rule_of_26_sharp >= 31`
   **or** (`lott_total_trumps(agreed) >= 9` and `controls >= 5` and combined
   losers <= 5).  A disjunction can only add hands, which is the safest shape of
   edit available here.
3. **Give `r2c_2D_waiting` a floor** — or, better, publish 2C's own strength
   into the partner model so responder's `rule_of_26` is not computed against
   zero.  DECISIONS already records that the repair belongs inside the 2C tree.

### What it endangers

Everything gated on the new disjunction becomes reachable on hands that
previously could not ask.  Blast radius is bounded by the 47 / 42 keycard asks
plus the ~35 cue bids per corpus, so on the order of **80-120 decisions per 1000
boards**, and it interacts directly with idea 3 — a widened gate on an
undisciplined ask makes the "asked and had to stop at five" failure *more*
common, so ideas 2 and 3 must ship together or not at all.

### Does it pay against a *bot*?

The mechanism is certain (the cap is arithmetic); the sign is likely but not
guaranteed, because it works through the gates in ideas 1 and 3.  My honest
estimate is that on its own it is worth little and as the enabler of idea 1 it
is worth most of idea 1's number.

---

## 3. Discipline the keycard ask, and finish the ladder above it

### The bridge

The rule every good partnership plays is: **do not ask for keycards unless you
know what you will do with every answer.**  Blackwood is a decision tool, not a
slam try.  The engine uses 4NT as its *only* slam try (idea 1), and the bill
arrives at the five level.

At the other end the ladder simply stops.  There is **no rule anywhere in the
file with `call: 7`** — the engine cannot bid a grand slam, as DECISIONS
already notes — and 5NT appears five times, every one of them as a *runout*
(`rkc5D_signoff_nt_C`, "keycards missing: 5NT, notrump-shaped"), never as the
king ask.  So after 4NT-5X the only two continuations are "six of the fit" or
"give up", and the pair has no way to check for the thirteenth trick.

### The evidence

| | e10 ours / BEN | held ours / BEN |
|---|---|---|
| 4NT keycard asks | 47 / 64 | 42 / 59 |
| …auctions that **stopped at the five level** | **17** / 6 | **17** / 3 |
| …of those, contracts that went **down** | 7 | — |
| …auctions that reached six or seven | 24 / 57 | 20 / 56 |

**More than a third of our keycard asks end at the five level**, against BEN's
9% and 5%.  Whole-corpus, our 47 asks carry a board margin of **-25 IMPs** and
a par gap of **-356**.  The biggest single offender is `gr_rkc_H` — the ask over
partner's raise to game — 14 firings, **nine** of them landing at the five level
(three down), par gap -7.93, board margin -1.57 a decision.

And there is one family that should simply go:

| `gst_rkc_*` (4NT because *partner once bid a suit*) | e10 | held |
|---|---|---|
| firings | 10 | 14 |
| board margin, total | **-39** | **-10** |
| par gap, mean | **-12.10** | **-7.86** |

`gst_rkc_S` alone: 3 firings, **-8.00 board margin a decision**, 0 wins, 2
losses.  e10 board 802b, West holds `K642.K2.AK5.AQT2` after
`1C - 1H - 1S - 3S`: eighteen points, four *small* spades, no ace in the agreed
suit — and bids Blackwood.  e10 board 319a, `2C - 2NT - 3C - 3S`, no suit agreed
at all, 4NT, then 5S, then down.  This is Blackwood on a suit partner merely
mentioned, and it is the clearest DELETE candidate in the file.

Grand slams are real but small: 27 / 33 deals in the two corpora have thirteen
tricks available, worth **-52 / -75** IMPs.  Worth a rung, not a round.

### What changes in the file

1. **Delete or re-gate `gst_rkc_C/D/H/S`.**  If they survive at all they need a
   real agreement — partner has bid the suit twice, or I have raised it, or
   `lott_total_trumps >= 9` **and** `keycards(agreed) >= 2` **and** a control in
   every side suit.  The hands they currently catch should route to the new
   slam-try rungs from idea 1, which is why this must not ship alone.
2. **Add a "will I bid it" precondition to every keycard ask**: I must hold
   enough that partner's *worst* legal reply still leaves me bidding six, i.e.
   an explicit `keycards(agreed) >= 2` floor plus a control/loser test, so a
   4NT that can only end at five is never made.  (Round 8 measured a bare
   `keycards >= 3` gate at -17 held out — it deleted three cold slams.  The
   floor must be paired with the alternative slam try from idea 1, which is
   precisely what round 8 did not have.)
3. **Make 5NT the king ask** in `rkc_continue_after_5*` (keeping a distinct
   runout for the notrump-shaped hands), and **author one 7-level rung**: seven
   of the agreed suit when the pair holds all five keycards and the trump queen.

### What it endangers

Deleting `gst_rkc_*` removes 10-14 slam entries per 1000 boards, three of which
we currently win; a bare deletion is a **net loss** unless idea 1's rungs are
already there.  The keycard floor removes asks — the exact experiment that
measured -17 held out in round 8.  Reach: ~50 decisions per 1000 boards.

### Does it pay against a *bot*?

The deletion half is the safest positive-expectation edit in this review; the
discipline half only pays if idea 1 lands first.  Ranked third because of that
ordering, not because it is smaller.

---

## 4. Make the Law of Total Tricks reach zero, and preempt like a modern pair

### The bridge

The engine is systematically passive, and it is passive in a very specific way:
it does not compete to the level its trump length entitles it to.  With nine
trumps you bid to three, with ten to four, **whatever your points**, because the
Law is about shape and the hand that most needs to bid is the one with no
defence.  The engine's competitive raise ladder is banded on *points*: the
cheap raise `cl_raise_$M2` floors at **6 total points**, and the raise to the
level of the fit `cl_raise_lott3_$M` floors at **3** and carries
`cheapest_in_suit: true`.  So the classic hand — four trumps, a bust, partner
has overcalled — has no bid at all.

The same conservatism shows in the opening preempts.  The weak two demands
**exactly** six cards, 5-10 HCP, two of the top three, and **no four-card major
on the side**; the three-level preempt demands seven cards and 4-9.  A modern
partnership, especially at IMPs and especially non-vulnerable or in third seat,
opens far more of these.

### The evidence

Bidding volume, both corpora, over 2000 tables each:

| | e10 ours / BEN | held ours / BEN |
|---|---|---|
| passes | 6459 / **5722** | 6410 / **5811** |
| calls at the 2 level | 974 / 1227 | 1015 / 1195 |
| calls at the 3 level | 698 / 867 | 745 / 880 |
| calls at the 4 level | 382 / 496 | 331 / 459 |
| preemptive openings (2D/2H/2S/3x) | **89 / 125** | — |
| contracts declared | 904 / **1047** | 905 / **1047** |

And, on a first-divergence walk of the paired auctions (the two tables hold the
same cards, so where the auctions first differ we are comparing our call with
BEN's on an identical hand in an identical auction):

| first divergence | e10 n / IMPs | held n / IMPs |
|---|---|---|
| **same strain, BEN bids it one level higher** | **81 / -92** | **92 / -36** |
| same strain, *we* bid it higher | 33 / +3 | 33 / -47 |

BEN outbids us in the same strain **2.5 to 2.8 times as often as we outbid
it**, on both corpora.  The mechanism, traced:

- **e10 board 677, table A**, East holds `92.9762.654.8632` — **zero HCP, four
  hearts** — after `(P) 1D 1H (1S)`.  Partner has overcalled hearts; that is
  nine trumps.  Candidate set: `P` (`cl_pass`, fit **1.00**), `2H`
  (`cl_raise_H2`, fit **0.004**), and three calls at fit 0.00.  **There is no 3H
  in the candidate set at all**, because `cl_raise_lott3_H` is
  `cheapest_in_suit: true` and 2H is legal.  BEN bids 3H.  **-13 IMPs.**
- **e10 board 951**, West holds `T6.6532.74.KT842` in the identical auction.
  `2H` now fits 0.80 — still no 3H.  BEN bids 3H.

Round 11 removed `cheapest_in_suit` from this rung and measured **-3 held out,
twice**.  Note what that experiment did *not* do: it left the floor at **3 total
points** (board 677's hand counts 1, so it still had nothing) and it left
`cl_raise_$M2` at priority 30 outranking the LOTT rung at 32 on trump length
grounds it does not test.  The untried mechanism is the floor and the
discriminator, not the `cheapest_in_suit` flag.

### What changes in the file

1. **`cl_raise_lott3_$M`: `total_points: [0, 8]`, `suits: {$M: [4,13]}`,
   `lott_total_trumps($M) >= 9`, and no `cheapest_in_suit`.**  The bid is
   preemptive by definition; a floor on it is a category error.
2. **Split the ladder on trump length, not on points.**  Four trumps and 0-8 →
   the LOTT rung; three trumps and 6-9 → the cheap raise; the cue-bid raise
   already handles the strong hands.  This is a re-rank as well as a rung, so
   per the round-14 lesson every rule in `general_competitive_low` whose call it
   can outrank must be listed first.
3. **Loosen the preempts where every expert does**: drop the "no four-card major
   on the side" veto in third seat and non-vulnerable, let the non-vulnerable
   weak two start at 4 HCP, and allow a five-card weak two in third seat
   non-vulnerable with a good suit.  These are `when: { we_vulnerable: false,
   opening_seat: [3] }` variants of rules that already exist.

### What it endangers

This is the widest-reaching idea in the review and the only one with a prior
negative attached.  A zero-floor preemptive raise takes hands that currently
pass and puts them at the three level; when partner's overcall was thin and the
Law's trump count is wrong (the Law is an approximation, and it over-states when
the honours are in the short suits), the result is 300 or 500.  It reaches on
the order of **100-150 decisions per 1000 boards**.  It should be measured in
two pieces — the raise floor alone, then the preempt loosening alone — because
they will not fail for the same reason.

### Does it pay against a *bot*?

Genuinely uncertain, and I would measure it last of the four.  Two things argue
for it: BEN's willingness to bid one more is worth -92 / -36 to us on the
first-divergence cell, and buying 143 more contracts a corpus is worth real
IMPs.  One thing argues against: the sub-cell where we pass and BEN acts is
worth -104 held out and -355 on e10, i.e. **it does not replicate**, so
"passivity" as a headline is much weaker on the honest corpus than on the review
corpus.  Ranked fourth for that reason.

---

## 5. The system is colour-blind: vulnerability and form of scoring are absent

### The bridge

At IMPs, vulnerability is the second most important fact at the table after
the cards.  A vulnerable game is worth ~+10 IMPs when it makes and ~-6 when it
fails, so the break-even is about 37%; non-vulnerable it is about 45%.  That is
worth roughly a point either side of the textbook 25-26, and every strong pair
stretches for vulnerable games and stays low non-vulnerable.  Vulnerability also
governs the sacrifice (the 500-against-620 arithmetic), the thin overcall, the
balancing action, the light preempt, and the penalty double of a partscore.

In this file, **26 of 14,937 lines mention vulnerability, in 3 of 517
contexts** — `openings` (23 of them, all weak twos and preempts),
`general_competitive_high` (2), and one advance rule.  Nothing in the game-going
machinery, nothing in the sacrifice machinery, nothing in the doubling
machinery, and nothing anywhere about form of scoring.  A rule-based system can
express this trivially — `when: { we_vulnerable: true }` already parses — which
is what makes the absence conspicuous.

### The evidence, honestly reported

This is the one idea in the review whose *effect* I could not demonstrate:

| 23-26 combined HCP, did the pair bid and buy a game? | e10 | held |
|---|---|---|
| us, vulnerable | 52.5% | 55.6% |
| us, non-vulnerable | 60.1% | 54.3% |
| BEN, vulnerable | 60.6% | 57.0% |
| BEN, non-vulnerable | 57.0% | 58.7% |

On e10 the story is textbook — BEN stretches vulnerable (+3.6 points), we shrink
(-7.6).  On the held-out corpus it vanishes.  By this project's own standard
that is noise, and I am reporting it as such.

What survives is the structural claim: the engine has **no** vulnerability-aware
game, sacrifice or double, and a bridge player reading the file would call that
a missing agreement rather than a style choice.

### What changes in the file

The cheapest honest approximation is a **one-point shift, not a new mechanism**:
add `when: { we_vulnerable: true }` twins to the handful of rules that decide
game — the `rule_of_26 >= 25/26` gates on the general game raises, `uc_nt3`,
the invitational-acceptance rungs — with the threshold one lower, and
non-vulnerable twins one higher.  Roughly 12-20 paired rungs.  Separately, the
four-and-five-level competitive raises (`cl_raise_lott4_$M`,
`balhigh_raise_lott4_$M`) should require more when vulnerable against not, which
is the sacrifice arithmetic in one clause.

### What it endangers

Every rule it twins is a rule that currently decides a game.  Half the twins
subtract (the non-vulnerable ones), which per the round-6 lesson is where these
things go wrong.  Reach: perhaps 150-250 decisions per 1000 boards, most of them
changing nothing because the hand is not on the boundary.

### Does it pay against a *bot*?

Probably a small positive, and it is the idea I would want to measure as a
standalone experiment rather than inside a bundle, because its effect is small,
diffuse and — on this evidence — not yet demonstrated at all.  It is fifth
because it is good bridge with weak evidence, and this project has been burned
by that combination before.

---

## 6. Direct answers to the questions in the brief

**Are the agreements themselves right?**  The 2/1 core is fine and mainstream.
The gaps that matter are not conventions — not Michaels, not NMF, not inverted
minors — they are the *slam-investigation toolkit*, which every serious
partnership has and this one does not: cues above game, cues with a minor,
a general slam try, a king ask, a grand-slam rung.

**Should some of the 2,344 rules be deleted?**  Almost none.  827 of the 1,799
distinct rule ids (46%) never appear as a primary reading in 20,716 decisions,
but that is `$`-expansion covering rare suits, not dead weight, and
ROUND_METHOD's round-11 lesson applies.  The one family I would delete outright
is `gst_rkc_C/D/H/S` (§3).  Note the counter-example that stopped me deleting a
second: `qr3_6NT` and `qr3_4NT_quant` have a par gap of **-8.9 / -4.88** and
look indictable — but their **board margin is +12 (e10) and +28 (held)**.  Par
gap and IMPs disagree in sign; keep them.

**Grand slams.**  Confirmed: zero rules with `call: 7`, and 5NT exists only as a
runout.  Worth -52 / -75 IMPs across the two corpora.  A rung and a king ask,
not a round.

**Where a rule-based system structurally cannot say what a human means.**  It
cannot say "this hand is worth more now that partner has bid my short suit", and
the cheapest honest approximation is a *combined-losers* evaluator used in the
slam gates only (§2).  It also cannot say "partner is unlimited, so I should
make one more try" — because `rule_of_26` collapses an unlimited partner to
minimum-plus-two.  That single line of arithmetic is, in my judgement, the most
consequential bridge error in the repository.

---

## 7. What this system gets RIGHT — and four hypotheses that died on the data

This matters as much as the five ideas, because three of them are things a
reviewer would naturally propose and all three measure zero.

**It gets right:**

- **The competitive partscore engine is close to parity.**  Held out, outside
  the twelve-trick deals, the engine is **-154 IMPs over 856 boards (-0.18 a
  board)** against a neural net trained on expert auctions.  Sixteen rounds of
  work on competitive and responding contexts have very nearly finished that
  job.  The "uniformly bad responding contexts" the last two rounds nominated
  are, on IMPs rather than par gap, close to a solved problem.
- **Slam accuracy when it acts.**  23 of 26 bid slams made held out.  The
  keycard machinery, the 1430 responses, the trump-queen clauses and the runouts
  are all working.  The problem is the trigger, not the tool.
- **Discipline about not bidding over its own contract, below game.**  It is the
  right guard in every competitive partscore; it is only wrong above game.
- **The negative-inference design.**  Cue ladders that deny by skipping are
  exactly how a human reads them, and the file's comments show the author knows
  it.

**Hypotheses that died:**

1. **"Open the eleven-counts."**  The frequency gap is the largest single
   behavioural difference in the corpus and it replicates perfectly —
   **11 HCP: we open 37.8% (73/193), BEN 69.1% (134/194)** on e10;
   **40.9% vs 66.7%** held out.  Its IMP consequence does not replicate at all:
   the first-divergence cell is **-87 IMPs on 58 boards (e10)** and **+35 on 41
   (held)**.  Split by shape (5-4+/singleton versus flat) it inverts again.
   The rule-of-20 openings are a style choice that costs nothing, and
   ROUND_METHOD is right to keep opening thresholds out of scope.
2. **"We play too much notrump."**  We do — **29.9% / 35.3%** of our contracts
   against BEN's **22.8% / 25.4%** — and it is not costing anything.  On the 47
   e10 boards where we played notrump holding a 22+ HCP eight-card major fit,
   we are **+65 IMPs**.  3NT instead of 4M is often the winning percentage
   action, exactly as DECISIONS' phase-2 note says.  Do not chase the strain
   gap.
3. **"Double more, like BEN."**  BEN doubles where we pass on 45 / 41 first
   divergences, the worst-mean cell in the table.  But we already double **32%
   more often than BEN** (275/209 and 279/212), and our doubles of a one-level
   major opening are among the worst rules in the file: `oc1H_X` + `oc1S_X`,
   24 / 21 firings, par gap **-3.79 / -1.43**, board margin **-2.04 / -0.57**,
   3 wins against 12 losses.  The subset of BEN's doubles that we most obviously
   "miss" — balanced 12-14 with three cards in their suit over a one-of-a-suit
   opening — nets **-9 IMPs across its 16 instances**.  Adding takeout doubles
   is a trap.
4. **"Balancing over their preempt is a hole."**  It contains one real and
   spectacular defect — e10 board 617, North holds `KJ6.AKQT6.A3.AQ9`, **23
   HCP**, and passes out `3S P P`, because `balhigh_X` requires
   `standing_suit_length: [0,2]` and the code fallback's natural notrump is
   capped at 19 HCP, so the whole candidate set is {pass at 1.00, X at 0.349,
   3NT at 0.028}.  Fix that ceiling by all means.  But the population does not
   replicate: over their preempt holding 12+, our passes run at par gap
   **-2.76 on e10 and +0.39 held out**.  It is one bug, not a family.

---

## 8. The one thing I think the project has misunderstood about bridge

**Par gap is not a bridge yardstick, and ranking rules on it has been pointing
sixteen rounds of work at the wrong 86% of the deals.**

Par gap is jointly owned by an entire auction and it is dominated by deals with
large absolute scores — which are, overwhelmingly, the deals where twelve tricks
are available.  The project noticed the symptom (§0(b) of the round-15 critique:
"a context landing on big-swing boards shows a bad gap whatever its rules do")
and responded by *normalising it away* — scoring each rule against its own
context, which by construction makes a uniformly bad context invisible.  Both
halves of that are right about the statistics and wrong about the bridge.  The
slam contexts are not innocent bystanders on big-swing boards; the big-swing
boards *are* the slam boards, and we are losing them because we do not bid
slams.

Decomposing IMPs by double-dummy trick availability — three lines of `endplay`
against the corpus that is already on disk — says the same thing in one number
that the last two rounds could not find in 2,344 rules: **-320 of the held-out
-474 is on 144 boards, and on 28 and 25 of those BEN bid a cold slam that we
passed out below game with a void and two aces in hand.**  Rounds 15 and 16 both
concluded "the rule-level defect supply is exhausted" and both were looking at
the wrong denominator.  The rule-level supply *for competitive partscores* is
exhausted.  The system has never had a slam try.
