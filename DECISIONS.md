# Design & Bridge-Judgment Decisions

Every non-trivial decision made while building the engine, with a one-line
rationale. Bridge-style choices are exposed as config flags where noted.

## Bridge system content (2/1 Game Forcing)

- **1NT opening 15-17, may contain a 5-card major** (`nt_with_5M: true`,
  flag): mainstream modern 2/1 practice; the flag switches to the
  no-5-card-major style.
- **Forcing 1NT played as semi-forcing** (`forcing_nt: semi`, flag): opener
  passes with a balanced minimum; the flag value `full` makes it one-round
  forcing and alertable. Semi-forcing is the growing mainstream default.
- **2/1 in a minor promises 3+ cards** (`two_over_one_suit_length: 3`, flag):
  a 12+ hand with no major and no support must have a bid; 3-card 2C is the
  standard workaround. Flag value 4 tightens it.
- **1D response to 1C is Walsh-style**: with a balanced hand and no 4-card
  major respond NT by strength; 1D promises 5+ diamonds or an unbalanced
  hand. Keeps the NT response ladder meaningful.
- **Better minor openings**: 1D on 4+ (or exactly 3=3 shapes with 3 diamonds
  when clubs are shorter), 1C otherwise; 4-4 minors open 1D, 3-3 open 1C —
  the textbook treatment.
- **5-5 in the majors opens 1S; 5-5 blacks open the higher suit**: standard
  "higher of equal length".
- **Minor raises are NOT inverted**: 2m = 6-10 with 4+ (simple), 3m = limit
  10-12 with 5+. Chosen for simplicity; inverted minors would be a system
  file change only.
- **Jump raise 1M-3M = limit with 3+ trumps** (not Bergen): keeps the raise
  ladder simple; 4-trump limit raises also go through 3M.
- **Jacoby 2NT**: 4+ trumps, GF, no shortness (splinters carry shortness).
  Opener rebids: 3-of-new-suit = shortness, 3M = 15+ extras, 3NT = 14-15
  no shortness, 4M = 12-13 minimum.
- **Splinters**: double-jump new suit, 4+ trumps, 9-13 HCP, GF.
- **Weak twos are disciplined**: exactly 6 cards, 5-10 HCP non-vul with a
  good suit (2 of top 3 or 3 of top 5); vulnerable tightens to 7-10 with 2
  of the top 3. No weak two with a 4-card major on the side.
- **Weak-two responses**: RONF (raise-only-non-force); 2NT is the strong
  (15+) feature inquiry.
- **Preempts at the 3-level**: 7+ cards, 4-9 HCP, good suit, seats 1-3 only.
- **Rule of 20 light openings restricted to seats 1-2** and to decent suit
  quality; rule of 15 governs 4th-seat borderline openings.
- **Strong 2C**: 22+ HCP or 18+ with <= 3.5 losers; 2D response is waiting
  (soft negative inference only); 2H/2S/2NT are natural positives (8+).
  2C-2D-2NT = 22-24 with systems on.
- **Negative doubles through 3S**: over a 1H overcall X shows exactly 4
  spades (1S = 5+); over 1S it shows 4+ hearts; over 2-level and 3-level
  overcalls it shows the unbid major(s) with 7-8+ points.
- **Support doubles/redoubles**: after 1m - P - 1M and interference below
  2M, X/XX = exactly 3-card support, any strength (the canonical
  negative-inference case: any other rebid denies exactly 3).
- **Cue-bid raises**: in competition the cue of their suit is a limit raise
  or better of partner's suit (alertable).
- **Jordan 2NT** over their takeout double: limit raise or better with 4+
  trumps; redouble = 10+ otherwise.
- **Overcalls**: 1-level 8-16 with a decent 5+ suit; 2-level 11-17 with a
  good 5+ suit; jump overcalls weak (6 cards, 5-10). **No Michaels or
  unusual NT** — a direct cue of their opening is left undiscussed to keep
  the file focused; adding it is a data change.
- **Takeout doubles**: opening values with shortness (<= 2) in their suit and
  3+ cards in the unbid suits, or any 17+. Advances: cheapest suit 0-8,
  jumps 9-11 invitational, cue = GF, 1NT 6-10 with a stopper.
- **Defense to their 1NT: natural** (X = penalty 15+, 2-level bids natural
  6+/good 5+ suits, 8-15). Chosen over DONT/Cappelletti for explainability;
  it is one YAML block to swap.
- **RKC Blackwood 1430** once a suit is agreed in a GF auction (5C = 1/4,
  5D = 0/3, 5H = 2 no Q, 5S = 2 + Q); 4NT is quantitative over NT openings
  and when no suit is agreed. Continuations: signoff at 5M missing two
  keycards, slam with the pool holding 4+.
- **Simple preference after 1M - 1NT - 2m**: 2M = 2-3 trumps 6-9, pass with
  a fit for the second suit, 2NT = 10-11, 3M = 3-card limit raise.
- **No Drury, no new-minor-forcing, no 4th-suit-forcing, no Smolen, no
  minor-suit Stayman**: scoped out; undiscussed continuations fall back to
  natural rules and are flagged `is_undiscussed_fallback`.
- **Jacoby-reply 4NT ask needs 17+ total points and 4+ controls**; with less
  responder signs off in game.

## Engine / architecture decisions

- **Auction patterns strip leading passes**; seat position and passed-hand
  status are rule *conditions* (`when:`) instead of pattern tokens. Keeps
  patterns short and seat logic explicit.
- **Template expansion in the loader** (`expand`, `expand_pairs`, `$VAR`,
  derived `$oM` = other major): the engine stays generic; symmetric contexts
  are written once. `expand_pairs` exists because transfers pair (2D->H,
  2H->S) and a cross product would create wrong combinations.
- **Most-specific context wins**: matching contexts are ordered by anchored >
  open-prefix (`...`) and token count, then file order; the first context
  defining a call interprets it. Negative inference stays *within* the
  interpreting context (cross-context denials are unsound).
- **Same-call rules combine as a disjunction** (anyOf) for descriptor
  updates; the highest-priority same-call rule is the "primary" reading used
  for forcing status / alerts.
- **Negative inference is perspective-aware**: rule-based denials are applied
  only to the side known to play this system (the API caller's side; all
  four seats in self-play). Opponents get positive natural readings plus any
  supplied explanations, never our system's denials.
- **Opponent explanations override** the rule-derived constraint for that
  call when structured constraints are supplied; text-only explanations are
  recorded but do not constrain.
- **Soft fit uses Gaussian boundary penalties** calibrated so 1 HCP outside
  a range scores ~0.8 and one card of suit length ~0.35 (length promises
  matter more). Negations are sharp (matching a denied condition ~0.1):
  "close to what was denied" must not be penalized.
- **Fast path**: any candidate with fit >= 0.9 wins by rule priority
  (priorities encode systemic preference); otherwise the blended
  fit-priority score decides, and a margin < 0.25 sends the top 2-4
  plausible candidates (fit floor 0.25/top-0.35) to simulation arbitration.
  The fit floor exists because double-dummy rollouts reward systemic lies
  (partner bids as if the rule were true), so implausible bids must not be
  simulated.
- **Arbitration overturns the fast pick only when statistically clear**
  (mean IMP gain > 1.5 stderr AND >= 0.4 IMPs), preferring the more
  descriptive bid otherwise; near-ties break toward higher rule priority and
  then the tighter descriptor box (the reading partner decodes most
  accurately - a cheap entropy proxy).
- **Sampler design**: partner's calls are verified by exact engine replay
  (this enforces all negative inference automatically); opponents' hands are
  checked against their descriptors (explanations + natural readings) since
  they do not play our system; my own calls are given. Suit-length-biased
  constructive dealing for partner when the descriptor binds, rejection
  sampling otherwise, hard wall-clock budget with graceful degradation
  (near-miss deals returned, flagged `degraded`).
- **Replay determinism**: the sampler/rollout policy is the fast path only,
  with deterministic tie-breaks; `prepare_decision` snapshots the auction
  and is cached per (auction, perspective, explanations).
- **DD evaluator behind a Protocol**: `EndplayDD` (real DDS, batched
  `calc_all_tables` prefetch, per-deal cache) with `HeuristicDD`
  (HCP+fit+shape trick estimate) as the documented fallback; `set_dd()`
  swaps implementations. endplay installed fine in this environment, so the
  real solver is the default.
- **Fallback layer is code, not YAML**: pass (weak before we act, "any hand"
  after), cheapest raise by support points, new suits through the 3-level
  (forcing one round below the 3-level in uncontested constructive
  auctions), cheapest natural NT with stoppers, takeout/penalty-flavored
  doubles, and a forced-continuation backstop. No cue-bid fallbacks —
  inventing conventional meanings is worse than passing.
- **Game-force discipline**: pass is filtered (not merely discouraged) when
  it would end a GF auction below game or drop partner's forcing call;
  generic GF landing rules (3NT without a fit, 4M with one) guarantee
  termination.
- **Scoring**: full duplicate scoring + standard IMP table; rollout deals
  are scored from the deciding side's perspective against the fast-path
  baseline call.
- **4th-seat pass-out rule** (hcp <= 12 failing rule of 15) is soft for
  negative inference: passed-out hands should not be hard-constrained.
- **Weak-two/preempt seat restrictions**: no weak twos/preempts in 4th seat
  (pass or open at the 1-level instead).
- **Opponents' unexplained passes** are read through our pass rules
  (positive constraint only, e.g. < opening values before any bid). Slightly
  aggressive but the standard practical assumption for sampling.

## Harvest-loop decisions (tools/harvest.py fix rounds)

- **Par-based oracle with a slam discount**: boards are scored against
  double-dummy par; par slams on freak shape (par >= 900 with modest HCP) are
  logged but deferred - chasing DD-only slams would make the system reckless.
- **Never bid over your own side's undisturbed contract** in a competitive
  auction (or once game is reached): stops the engine pulling its own doubled
  contracts. Uncontested constructive auctions keep fallback continuations so
  invitations stay biddable.
- **Fallback raises**: banded to the next raise level when uncontested (with a
  separate jump-to-game raise needing real extras), full-range in competition,
  and 5-level+ competitive raises require Law-of-Total-Tricks trumps.
- **A one-round force may be passed when nothing fits at all** (fit < 0.3 on
  every bid): converting partner's takeout double beats inventing a call. A
  game force is still never passed below game.
- **Sandwich-seat actions authored** (X = shortness in opener's suit 12-16 or
  any 17+; natural overcalls) and **balancing-seat reopenings** (a king light).
- **Pass-rule ranges widened** where self-play produced self-contradictory
  descriptors (e.g. a 13-count with no suitable action passing over 1S).
- Uncontested continuation gaps found by harvesting are now authored: replies
  to jump raises, 2NT jump rebids, minor rebids, 1S second suit, game tries,
  jump rebids, Stayman over interference and after 2NT, opener jump shifts.

### Round 2 harvest decisions

- **Never bid over your OWN last contract bid** (keyed on the seat, not the
  side): pulling your own doubled contract is the single most expensive
  self-play error. Partner's bid silences us only once game is reached, so
  responder can still act after RHO doubles partner's opening - an earlier,
  side-keyed version of this guard muted responder entirely.
- **Fallback notrump never above 3NT**: at the 4-level and beyond NT is
  conventional, so an invented natural 4NT is always wrong (one cost 1100).
- **New suits over their takeout double need an honor** in the suit, so
  equal-length choices go to the better suit rather than blindly up the line.
- **New suits opposite a weak two are forcing** (RONF), 5+ cards and 12+ HCP
  with a doubleton or shorter in partner's suit.
- Content authored from harvested gaps: responder's natural actions over
  their takeout double (new suits, 1NT, simple and preemptive raises),
  advancing partner's sandwich double, and responder's rebid opposite a
  two-suited opener (1H - 1S - 2m).
- **Harvester detector fixes**: misbids are scored in the *candidate* context
  (support points need the trump suit the call agrees, else every good raise
  looked like a misbid), and a doubled contract that still beat par is scored
  as a successful sacrifice, not a disaster.

### Round 3 harvest decisions

- **RKC requires partnership slam values** (`rule_of_26 >= 31`), not just a
  big hand of my own: a 22-count opposite an uninformative waiting bid was
  driving to a 27-point slam.
- **Fallback raises never above the game level**: slam raises need real
  machinery (control bids, keycards), never a generic point count.
- **Fallback raise bands are contiguous**: an earlier "jump to game needs
  extras" tweak left 12-17 support points with no bid, so hands in the hole
  jumped to game on a poor fit score. The game raise now starts exactly where
  the cheap band ends.
- **Weak-two game raises need 3+ trumps** (and 17+ points on the point-count
  branch): 14 HCP with a doubleton was raising 2H to 4H.
- **Opener may be too strong to invite**: with a 6+ card major and 20+
  playing strength, opener bids game rather than making an invitational jump
  rebid that responder can pass with 7 points.
- Content authored from harvested gaps: opener's answers to Stayman and
  transfers after 2C - 2D - 2NT (systems on) and the placements after them;
  responder over opener's invitational jump rebid after any 1-level response.

### Round 4 harvest decisions (200-board batch)

- **Fallback raises cap at the 4-level for every suit**: with a minor fit the
  game is 3NT, so an invented 5m "game raise" is always wrong (one went for
  500 doubled). Slam raises still need real machinery.
- **Opener's minimum rebids accept light openings** (10-15, not 12-15): a
  rule-of-20 opening with 10 HCP previously had no honest rebid.
- **1m - 3NT covers 13-17 balanced** (mainstream range), so a 17-count is not
  forced into a call that shows less.
- **Takeout doubles of a 3-level preempt tolerate three small** in their suit
  (14-17, or any 18+): requiring a doubleton left classic takeout shapes with
  no bid.
- **Weak-two game raises and competitive raises** got the missing top of the
  ladder: a game raise over their preemptive overcall (11+ support points).
- Whole structures authored from this batch: responses to partner's 3-level
  preempt (forcing new suit, game, pass) and the preemptor's rebid; opener's
  answer to the 2NT feature ask over a weak two; and a full defense to their
  3-level preempts (takeout double, natural 3NT, 6+ suit overcalls).

### Round 5: general agreements as data (200-board batch)

The goal of this round was to drive the *undiscussed* (fallback) call rate
toward zero. Grouping 200 boards' fallbacks by structural family showed 60%
were ordinary competitive positions and 24% ordinary uncontested
continuations - not exotic gaps, just the generic toolkit every partnership
plays without discussion. That toolkit is now system DATA:

- **Three auction-relative suit predicates** (`is_partner_suit`,
  `is_their_suit`, `is_unbid_suit`) let the DSL say "raise partner's suit" or
  "bid a natural unbid suit" without naming a concrete suit.
- **Suit role and level are hard `when:` gates, not soft hand features.**
  A first draft expressed them as `features:`, which the fit model treats as a
  soft 0.2 penalty - so "raise partner's suit" fired in suits partner never
  bid, including the opponents'. Because these are facts about the auction and
  not about the hand, they belong in `when:`: new conditions `partner_suit`,
  `unbid_suit`, `cheapest_in_suit` and `we_hold_contract`.
- **`cheapest_in_suit`** reproduces in data the fallback layer's rule that only
  the lowest available bid in a suit is offered; without it the engine invented
  4-level "natural" bids when the 2-level was free.
- **The general pass is permissive** (any hand, priority below the general
  bids). This mirrors what the fallback layer actually did and is what keeps
  the engine from acting on hands no bid describes: a general bid must fit
  essentially perfectly to beat pass, while a specific rule still wins on a
  partial fit.
- **`we_hold_contract: false`** gates all five general contexts, so the
  discipline against bidding over our own contract survives the move from code
  into data.

Result on the same 200 boards: undiscussed calls fell from 2.30 to 0.26 per
board (-89%), average IMPs lost against par improved from 6.91 to 6.24, and
absurd contracts fell from 7 to 4.

**Harvester detector fix (important for reading earlier rounds):** the
`par_loss` back-stop flag was suppressed whenever a board carried *any* other
issue - including purely informational `fallback` entries. Boards with an
undiscussed call therefore never reported a par loss, so the headline
"actionable issue" rate in rounds 1-4 was understated and moved whenever the
fallback rate moved. The flag now ignores fallback entries. Re-scored
consistently, the same 200 boards read 52% before this round and 47% after.

### Round 6: partner-aware raises (200-board batch)

- **General raises are partner-aware.** The level-3 and game-level general
  raises now gate on `rule_of_26` (my total points plus partner's shown range)
  instead of a fixed support-point band. A fixed band bid game opposite a
  *preemptive* raise (3-8 HCP) and equally failed to bid it opposite a
  cue-bid raise, so this one change fixed both the overbidding and the
  underbidding halves of the par-loss residue.
- **The Law of Total Tricks gates competitive raises only, not game raises.**
  Requiring nine combined trumps for a game raise suppressed normal 5-3 major
  games; the Law is a competitive-judgment tool, not a constructive one.
- **Partner's strength is tracked in support points as well as HCP.** 145 of
  the system's rules state strength as `total_points` rather than `hcp`, so
  the partner model's HCP box read zero for them and `rule_of_26` was blind.
  `HandConstraint.min_total_points()` now derives a sound lower bound
  (conjunction takes the strongest, disjunction the weakest), the descriptor
  exposes it, and `rule_of_26` uses whichever bound is more informative.
- **With a minor fit the game is 3NT**: general game-level raises in a minor
  rank below the natural 3NT rule.
- Content authored from this batch: responder's continuations after a 2NT
  opening transfer is completed (this position had no rules at all, so
  responder passed 3-of-a-major holding a game-going hand), and opener's
  action over responder's competitive invitational 2NT.

## Phase 1-2: an attributable yardstick, and strain selection

- **Par is the wrong optimisation target on its own.** It bakes in the
  opponents' double-dummy sacrifices and perfect defence, neither of which our
  bidding controls, which is why the par gap plateaus no matter what is fixed.
  The harvester now also reports a **constructive gap**: on *uncontested*
  auctions only, our score against the best contract available to our own side
  on that deal, split into a **level gap** (right strain, wrong level) and a
  **strain gap** (a different strain scored better). The whole of that number
  is attributable to our bidding, so it can genuinely be driven down.
- **Not every strain gap is a bug.** Bidding 3NT rather than five of a minor
  is correct percentage bridge even on the deals where double-dummy prefers
  the minor; chasing those would make the engine worse in real play. Only the
  cases where a *major* fit was buried were treated as defects.
- **A shapely raise needs a home**: a 4-trump hand worth 13 support points but
  under 11 HCP was too good for the limit raise (10-12) and too weak for
  Jacoby 2NT (11+ HCP), so it had no raise at all and responded 1NT - burying
  a nine-card fit. The limit raise now spans 10-13 support points.
- **Show a five-card major over opener's 18-19 2NT jump** (and opener picks the
  5-3 fit with three-card support), instead of raising straight to 3NT.

## Phase 3: threshold calibration - a negative result

`tools/tune.py` searches the system's point thresholds by coordinate descent
against a 400-board training corpus and re-checks every accepted move on a
400-board held-out corpus.  (Double-dummy tables depend on the deal, not the
system, so they are cached once; each candidate setting then costs ~10s
instead of ~2 minutes.)

The search reported a train gap of 5.63 -> 5.33 and a test gap of 5.91 ->
5.73, which looked like a win.  It was not:

- **Two of the five chosen values broke the regression suite.** The search
  lowered the game-raise threshold until the engine bid game opposite a
  *preemptive* raise - the exact bug fixed in round 6 - and dropped the
  1m-3NT threshold so an invitational 12-count jumped to game.  The tests
  encode bridge correctness the double-dummy metric cannot see, so those two
  values were rejected outright.
- **The remaining three were statistically indistinguishable from zero.** A
  paired before/after comparison on the same boards gives a held-out gap
  change of **-0.025 +/- 0.062 IMPs**; even on the training boards it is only
  -0.17 +/- 0.12.  The apparent gain was noise plus the two rejected knobs.

The whole tuning was therefore **reverted**.  The finding is worth keeping:
the textbook thresholds are already close to optimal, and the level gap is not
a threshold problem.  It is an information problem - with limited bidding
space the engine often cannot know enough about partner's hand to place the
contract exactly - and no amount of tuning the numbers will address that.

Method note: report *paired* statistics when comparing two systems on the same
boards.  Unpaired means on 400 boards have a standard error near 0.3 IMPs,
which is larger than any effect being chased here.

## Phase 4: arbitration audit

Self-play runs fast-path-only, so the simulation arbitration path had never
been measured end to end.  On 120 held-out boards:

- Only **3.1% of decisions** are unclear enough to invoke it, and it overturns
  the fast path on about a third of those - 11 decisions in 120 boards.
- Replaying the *real* deal from those positions, arbitration's choice is worth
  **+0.82 +/- 1.24 IMPs** per overturned decision: the right sign, not
  significant, and about +0.08 IMPs/board over a whole corpus.
- Its own simulation predicted 2-11 IMP gains for those same choices, so the
  self-evaluation is substantially optimistic.  This is expected - the rollouts
  assume partner reads every call exactly as the rule intends - and it is why
  arbitration only overturns the fast pick on a clear statistical margin.

Arbitration is correct, stays inside its time budget and does no harm; it is
simply not a scoring lever.  `tests/test_arbitration.py` now covers it
end to end so the subsystem cannot rot unnoticed.

## Corpus quality gate

`tests/test_corpus_gate.py` fixes a 120-board seeded corpus with hard ceilings
(par loss, undiscussed calls, misbid rate) plus full legality, termination and
replay-determinism checks.  Achieved at the time of writing: par 5.78 (ceiling
7.5), undiscussed 0.23/board (0.60), misbid rate 0.012 (0.030).  Tighten the
ceilings when the engine improves; never loosen them to make a change pass.

## A better evaluation method: comparison against BEN

Double-dummy par turned out to be a poor teacher.  It judges the *final
contract* against an omniscient oracle, so it cannot distinguish bidding
badly from bidding well with information the partnership could not have; it
attributes a whole board to nothing in particular; and because both sides run
the same rulebook in self-play, systematic biases cancel and become invisible.
Six rounds of it produced real bug fixes but a flat average.

`tools/compare_ben.py` replaces it.  BEN (github.com/lorserker/ben) is a
neural bidder trained on a large corpus of expert auctions.  At every decision
our engine makes, BEN is asked what it would call from the same seat, with the
same hand and the same auction.  Disagreements are recorded with the rule that
produced our call and BEN's confidence.

Why this is a better signal: BEN encodes *human expert judgement*, which is
precisely what the rulebook is trying to capture and precisely what a
double-dummy oracle cannot express.  And a disagreement points at one
decision, made by one named rule, with a hand and an auction attached.

**BEN is not a source of truth.**  It is statistical, it offers no
explanations, and it is sometimes wrong.  The unit of evidence is therefore
never a single disagreement - it is a *cluster*: the same rule disagreeing the
same way many times with BEN confident each time.  A one-off, or a
disagreement where BEN itself is unsure, is discarded.

Engineering notes.  BEN pins numpy<2.1 while endplay here needs 2.4, so BEN
runs in its own virtualenv driven over a pipe, using only its ONNX bidder (no
TensorFlow).  The model is BEN's own 2/1 Game Forcing network, so the
comparison is like-for-like.  The worker imports BEN's own feature encoders
rather than reimplementing them.

A validation lesson worth recording: the first run looked plausible but was
wrong.  BEN's auction array is left-padded with `PAD_START` up to the dealer,
and the model is *sequential*, so counting a phantom turn for seats before the
dealer corrupted its hidden state - contaminating three quarters of all
boards.  It was caught only by asking BEN to bid one fixed 14-count from all
four seats and noticing it "passed" in some of them.  Any oracle must be
validated on known answers per seat, per vulnerability, before its
disagreements are believed.

### What the comparison found immediately

- **11-HCP hands were being opened.**  `open_pass` covered 0-10 and the
  openings 12-21, so an 11-count fitted neither and rule priority alone
  decided - it opened.  BEN passes these at 95%+ confidence.  `open_pass` now
  covers 0-11; rule-of-20 openings still fire because they match exactly.
- **The general takeout double had nothing to take out.**  It was doubling
  *notrump* contracts, and doubling after our side had already described its
  hand.  "Short in their suit" was vacuously true when the opponents had
  shown no suit at all.  A new `their_last_bid_suit` condition requires a suit
  to take out, and `side_has_acted: false` keeps the takeout double an entry
  into the auction rather than a continuation.

Agreement with BEN over 300 boards: **72.4% -> 75.8%** from those two fixes.

### What 1000 deals found next

The first 1000-deal run said 77.0% agreement and, crucially, said the
previous round's general-notrump fix had changed *nothing*.  It had not: the
ten rules had ended up with two `evals:` keys under one `requires:`, and YAML
keeps only the last, so the added `rule_of_26` gate was discarded on load.
The rulebook is hand-edited data, so the loader now rejects duplicate mapping
keys instead of silently dropping a constraint.  With the gate actually live,
the general-notrump rules went from 252 confident disagreements to 121.

The rest of the round came from reading the *undiscussed fallbacks* rather
than the disagreements - a fallback is the engine saying it has no agreement
at all, which is a stronger signal than a disagreement with a statistical
bidder.  Of 174, eighty were one hole:

- **Nothing covered "they doubled our call."**  Every generic context
  required the standing call to be a bid or a pass, so opener re-acting over
  a balancing double, advancer over a penalty double of partner's overcall,
  and the runout from a doubled 1NT all had no agreements.
  `general_their_double` covers them, split by role, because the two roles
  are different auctions: over a balancing double of my own partscore a
  second suit is constructive and four cards of any quality will do, while
  over a penalty double of partner's call a suit of mine is an escape and
  needs real length.  Both redoubles rank *below* the descriptive calls -
  with a suit to show, showing it beats announcing strength.
- **Balancing doubles had no "our side has been silent" gate**, which is the
  premise of the bid, so the same hand doubled twice and three times in one
  auction.  Sixty-two confident disagreements, gone with one condition.
- **Preempts required two of the top three honours**, which refuses to
  preempt on KJ9xxxx and QJTxxxx - most seven-card suits.  Quality is a
  matter of degree and of vulnerability now.  Eight-card majors had no
  opening at all; 4H and 4S are openings.
- **Negative doubles existed only over major overcalls**, so `1C-(1D)` and
  every two-level overcall had none.  One generic rule covers the negative
  and responsive double both - our side has acted, they have bid a suit, it
  is my first call, I have no five-card suit of my own, and I hold a major
  they have not bid.

Two supporting fixes fell out of the same reading.  A suit I have bid myself
was still counted as "unbid", so a new-suit rule could fire in my own suit;
and a game raise in a *minor* could outrank a one-level bid in my own longer
major, so it now requires the minor to be my longest suit.

Over 1000 deals, same seed: agreement 77.0% -> 77.7%, confident
disagreements 1537 -> 1336, undiscussed fallbacks 174 -> 136.

**A negative result worth recording.**  The negative-double rule *costs*
about 0.3 points of BEN agreement on a held-out seed (76.0% -> 75.7%).  It
is kept anyway.  A 2/1 system without negative doubles over a minor overcall
is not the system it claims to be, and the disagreement is about *where* BEN
doubles rather than *whether* the convention exists - which is exactly the
kind of question a statistical bidder is not entitled to settle.  The same
applies to the keycard responses: our 1430 answers disagree with BEN's 3014
about ten times per thousand deals, and that is a system difference, not a
bug.

**And a caution about the headline number.**  Agreement moved 0.7 points
while whole families of errors disappeared, because fixing one call changes
every call after it: the same 1000 deals produced 10,175 decisions before
and 9,485 after.  Cluster movement, not the percentage, is what these rounds
are measured by.

### A second thousand deals, on a seed nothing was fitted to

Read on a fresh corpus (seed 20260828) the engine started at 76.9%.  Three
findings needed no judgement at all, because the corpus convicted the rules
rather than suggesting improvements to them:

- **`xd_XX_values` was deleted.**  It was authored the previous round on
  principle - "partner's call was doubled and I hold values, so redouble" -
  with no evidence behind it.  31 disagreements, 27 with BEN confident, 16 of
  those saying simply "pass".  A redouble of a double aimed at partner is a
  specialised call, not a general agreement.  Authoring on principle is how
  the rulebook gets written; the corpus is what decides whether the principle
  was real.
- **The takeout doubles allowed a five-card major.**  The engine doubled 1D
  holding AKJT5 and then heard partner name spades.  They deny one now (six,
  in the strong branch, where the suit is worth showing on its own).
- **The game-level major raise took three trumps flat**, and jumped to game
  on 4-3 fits.  It counts *combined* trumps now - the same test read
  correctly, since three are plenty opposite a rebid six-card suit and too
  few opposite a four-card response.

The redouble had left exactly the hole the double had (no generic pattern
matches a trailing XX), and it was the largest single fallback family: 55 of
131.  `general_after_redouble` covers both positions, split by role.

Two gaps were structural rather than mistaken.  **Repeating my own suit was
missing from the generic toolkit entirely** - only the doubled and redoubled
families had the rule - so 79 confident disagreements were the engine passing
with six of a suit it had already bid.  And **opener's rebids started at 12
HCP while the openings start at 10** under the rule of 20, so a light opener
with four spades hidden behind a six-card minor rebid the minor.

The rebid rule is worth recording as a two-step lesson.  Authored with a flat
point requirement it made things *worse* - 132 confident disagreements, and
overall agreement fell.  It was rebidding to game over partner's preemptive
raise: the same partner-blindness that round 6 fixed for the raises.  With
the values counted opposite partner's shown range it is a clear gain.  A new
rule that scores worse is not necessarily a wrong idea, but it is always an
unfinished one.

Across three seeds, before -> after this round:

| corpus | before | after |
|---|---|---|
| seed 20260828 (fresh) | 76.9% | 78.5% |
| seed 42 | 77.7% | 78.9% |
| seed 99 | 75.7% | 77.7% |

Confident disagreements on the fresh corpus: 1417 -> 1305.  Undiscussed
fallbacks: 131 -> 91.

## Playing BEN head to head

Agreement percentages measure imitation, not results.  `tools/match_ben.py`
plays a duplicate teams match instead: every deal is dealt twice with the
same dealer and vulnerability, our engine holding N/S at one table and E/W
at the other, so the deal's own luck cancels and the margin between the two
tables is the difference between the two bidders.  Contracts are scored
double-dummy, so play never enters into it.

**First match, 1000 boards: we lost by 1484 IMPs, 1.48 per board.**  184
boards won, 388 lost, 428 flat.  That is a decisive result, not a close one,
and worth stating plainly: BEN bids better than this engine does.

Where the deficit actually was:

- **Slams: -529 IMPs, a third of the whole margin.**  117 boards had a slam
  available.  BEN bid 37 of them; we bid 6.  Holding the slam cards we
  stopped at the four level 61 times.
- **Our penalty doubles: 53 of them, 26 made.**  Doubling a contract that
  makes half the time is a losing bet, and it cost about 200 IMPs.  BEN
  doubled 7 times in the same 2000 auctions.
- **We were outbid.**  BEN declared 1105 contracts to our 883.

Three fixes came out of the first match.  The RKC continuations turned out
to be authored for an agreed MAJOR only, so with a minor agreed the engine
asked for keycards and then had no rule for the answer - on one board it
signed off in 5S with clubs agreed.  The generic penalty double of a high
contract asked for *shortness* in their suit, which is a takeout shape, and
then left the double in as a penalty; a business double needs trump tricks.

And a bug worth its own paragraph: **the opponents' suits were not being
tracked at all** unless one of our own contexts happened to interpret their
call.  Every "their suit" evaluator therefore read as vacuously satisfied -
no stopper needed, no length held, short in their suit - across most
competitive auctions.  A suit an opponent has bid is a suit they have shown,
whether or not a rule of ours described the call.

A second bug of the same kind: `lott_total_trumps` took no suit argument and
read partner's FIRST shown suit, so every LOTT gate in a rule about a
different suit was measuring the wrong fit.  Seventy-two gates now name
their suit.

**Second and third matches: -1414 and -1421.**  The doubles fell from 53 to
34 and the slams rose from 11 to 26 (made 46%), but the total moved by 4%
and then stopped.  That is the honest headline: the fixes were real and the
match barely noticed.

The reason is in the breakdown.  On the 298 boards where both tables reach
the identical contract we are +14 IMPs - dead level, as expected.  The
deficit is spread almost evenly across every other bucket: one level lower,
one level higher, two levels either way.  There is no single systematic
error left to correct.  The two concentrations that remain are slams (-436,
needing cue-bidding and control-showing machinery this engine does not have)
and strain selection at the same level (-121 over 58 boards, most of it
choosing notrump where BEN chooses a suit).

A negative result about slam bidding is worth recording precisely.  The
obvious fix - let the engine ask for keycards in the position where it
currently jumps to game - cannot be gated on strength.  Measured on the
corpus, the hands that SHOULD bid game were *stronger in points* than the
hands with a slam on.  What separates them is the fit: nine trumps counting
partner's shown length.  Gated that way the slam try is sound and improved
the slam boards by 33 IMPs; gated on points it fired on hands that belong in
game, including over our own doubled contract.

What this measurement is good for, and what it is not: it is the first
metric here that is genuinely adversarial and zero-sum, so it cannot be
gamed by bidding more of anything.  It is also slow (five minutes per 1000
boards) and noisy at the level of individual changes - a 60-IMP move over
1000 boards is roughly one standard deviation, so a single run cannot
adjudicate a small change.  Use it for direction and for the big buckets;
use the decision-level comparison for anything finer.

### A second head-to-head, and what three rounds of fixes did not do

A fresh 1000 boards on a seed nothing had been tuned against: **-1474 IMPs,
1.47 per board**, 195 won to 390 lost.  Statistically identical to the first
corpus, so the measurement is stable.

Attributing each table's loss against par to the rule that made our last bid
put one item far out in front: the generic `uc_nt3`, "natural 3NT, 13-17
balanced", was the final bid on 96 tables and carried -487 IMPs, -5.07 per
use.  Reading those boards found a real hole behind it - `1S - 1NT - 2H`
does not exist, because the opener-rebid context is expanded over both
majors and 1H - 1NT - 2S would be a reverse, so a hand with five spades and
four hearts had no way to show the second major and jumped to 3NT instead.

That gap is authored now.  The other half of the fix - raising the generic
notrump game gate from 24 to 26, on the theory that we were bidding too many
thin games - **did exactly what it was designed to do and changed nothing**:
`uc_nt3` fell from 96 last bids to 68, our 3NT contracts from 180 to 146,
and their success rate rose from 65% to 73%.  The match went from -1474 to
-1473.

The 51 boards whose contract changed tell the whole story: **27 improved, 21
got worse, net +1 IMP.**  At IMPs, stopping short of a game that makes costs
what bidding one that fails does, and a 65% success rate was never evidence
of overbidding in the first place.  The gate is reverted; the missing rebid
is kept.

The rule-level attribution is therefore **correlational, not causal**.  It
ranks rules by how often they are the last bid on a board that went badly,
and the generic rules are the last bid precisely when the auction has
already gone somewhere no specific agreement covers.  Fixing the rule the
ranking blames does not recover the IMPs, because the rule was a symptom.

Every other slice of the deficit comes out flat:

| slice | our margin |
|---|---|
| both sides competed | -1.47 / board |
| only BEN's side bid | -1.37 / board |
| only our side bid | -1.62 / board |
| games bid | ours 373 at 73% made, BEN 430 at 72% |
| partscores | ours 280 at 67%, BEN 340 at 65% |
| identical contract at both tables | 302 boards, **0 IMPs** |

Our judgement *per contract* matches BEN's almost exactly.  What differs is
volume: BEN declares 1132 contracts to our 851, and on identical cards it
enters 82 more auctions per thousand boards.  But competing more is not the
lever it looks like either - the loss rate is the same whether the board was
contested or not.

So the honest conclusion after three rounds of targeted fixes, each moving
the match by less than 1%: **the deficit is not concentrated anywhere.**  It
is a small, broad, per-decision quality difference that accumulates over
roughly nine decisions a board - which is what a network trained on millions
of expert auctions has over a hand-authored rulebook of 1100 rules.

The one measurement that does point somewhere: our last bid coming from a
**specific** agreement costs -1.81 IMPs per table against par, and from the
**generic** toolkit -2.24.  Closing that gap means authoring specific
contexts for the positions where the generic rules currently fire - the same
slow, unglamorous work every round of this project has converged on, worth
perhaps 300 IMPs of the 1480 if carried to completion.  There is no single
lever left to pull.

## Slam machinery

The match's biggest identifiable pocket (about -530 IMPs of slam boards per
thousand) got its own round.  What was missing was the floor between game
and Blackwood: with a suit agreed in a game force the engine either met the
stiff RKC gate or bid game and stopped, and real slam auctions live in that
gap.

**Cue bids** are authored now: with a major agreed in a game force and the
agreement standing at the three level, a new suit below game shows
first-round control there (ace or void, the new `control_in` evaluator) and
slam interest.  The negative-inference machinery is the whole reason this
encodes naturally - the cues are priority-ordered cheapest-first, so
bidding 4D having skipped 4C *denies* first-round club control, and
returning to game denies whatever was still cheap enough to show.  A cue
shows 14+ opposite the shown range, which feeds the partner model, raises
rule_of_26, and thereby unlocks the existing RKC gate for a partner who
could not have asked directly.  The machinery composes; board 205 of the
match now runs 3C - 4D(cue) - 4NT - 6C, making.

Two authoring lessons from the round:

- **Specificity shadowing.**  The cue contexts first used the fully generic
  pattern and the 4C cue silently lost to "raise partner's club suit"
  whenever the cue suit was one partner had bid naturally - a more specific
  pattern covers the call first.  One token of specificity and file order
  fixed it.  When two contexts can claim the same call, the DSL's coverage
  rules are part of the design, not a detail.
- **Splinters already existed** (authored in the base system) - the gap was
  never the conventions at the front of the auction, it was the machinery at
  the top.

**Quantitative raises of 3NT** close the other slam family: 6NT directly on
33 combined (rule_of_26 against partner's shown minimum), and - since 33 is
invisible when it splits 17/16 - a pass-able 4NT invite that the 3NT bidder
accepts holding the top of the shown range.  4NT directly over 3NT is
quantitative by agreement, never keycards; pattern specificity enforces
exactly that.

**The 5NT king ask was considered and deliberately skipped.**  Choosing
seven over six requires adding partner's shown kings to my own, and the
constraint language has no cross-hand arithmetic.  Without the 7-level
decision the ask is pure information leakage - it can never change the
contract.  A convention that cannot affect the final contract is not worth
its space in the system file.

Measured on the fixed 1000-board corpus: cue layer alone was IMP-neutral
(it fired three times - sound but starved, because the engine's raises jump
straight to game and rarely pass through the position where cues live);
widening the direct slam-try gates to an eight-card fit and rule_of_26 31
plus the notrump quantitative raises moved the match from **-1480 to
-1427**, the first match-level gain in three rounds of slam work.  Slams
bid: 13 -> 14, made 5 -> 7; the changed boards split 6 up, 2 down.

Known gap surfaced in testing, left for the next round: after a reverse
(1D - 1S - 2H) responder with 11 opposite 17+ passed a 3D preference out -
responder's obligations over a reverse are under-authored.

