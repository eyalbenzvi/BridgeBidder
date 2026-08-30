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

## Thumb rules: encoding the folklore

A round dedicated to bridge maxims - the compressed expert judgment every
partnership plays by.  The audit first, because most of the canon turned out
to be already in the system: rule of 20 and 15 openings, LOTT raise gates,
higher-of-five-five, support-with-support (raise priorities), balancing a
king lighter, no notrump with a void (semi_balanced), never pulling a doubled
contract.  The card-play maxims (eight-ever-nine-never, second-hand-low) are
out of scope by construction.

What was genuinely missing, now added:

- **"If 3NT is one of the logical options, bid it."**  With a MINOR agreed in
  a game force there was no notrump preference at all - the landing contexts
  covered majors and no-fit only, so the engine bid five of a minor with 3NT
  cold.  `gf_minor_3NT` prefers nine tricks over eleven whenever every suit
  our side has not shown is stopped (the new `weakest_unshown_stopper`
  evaluator - the honest version of "3NT is an option").
- **Fourth suit forcing**, the tool that makes the maxim reachable: with
  three suits on the table and no clear bid, the fourth suit is artificial,
  game-forcing, and asks for a stopper so 3NT can be bid from the right
  side.  "No clear natural bid" is gated in, not assumed: no fit for
  opener's second suit, no stopper in the fourth suit, no six-card suit of
  your own, and genuine game values (13+, because the bid forces to game -
  the first draft said 12 and an eleven-count invite went through it).

Two negative results, both kept in the file as comments:

- **"Don't preempt twice" was tried and REVERTED.**  As a 10-HCP floor on
  the generic suit rebids it silenced nine-count overcallers competing at
  the two level: a measured 10-IMP loss.  The maxim is about free rebids by
  a preempt opener, and the rulebook currently cannot distinguish "I opened
  a preempt" from "I bid this suit once".
- The first version of the minor-game landing **violated its own maxim**: 
  its 5m sign-off fired over partner's freely chosen 3NT and pulled it to
  five of a minor.  It is gated to the raise position now (a new
  `standing_bid_strain` condition: the standing bid is the agreed minor).

The deepest fix of the round came out of chasing a single bad board: **trump
counting was soft**.  `lott_total_trumps` used the default Gaussian
tolerance, so a seven-card "fit" scored 0.8 against an eight-trump gate and
the engine raised to game on 4-3 fits past an available 3NT.  Trumps are
counted, not estimated - a near-miss on a countable quantity is a different
bid.  The sigma is sharp now, which tightened every LOTT gate in the book at
once.

Fixed corpus: -1427 -> -1359, the best result yet (from -1474 at the round's
start, +115 total).  Hold-out seed, never used for tuning: -1.05/board.
The overall arc of the maxim round: the folklore was mostly already there;
the wins came from the two structural gaps (minor-game 3NT, fourth suit)
and from one representation bug the maxims flushed out.

## The 10,000-board round

A ten-thousand-board match (seed 777) pins the baseline down to about
±0.02 IMPs/board - tight enough to trust small movements.  It was launched
on the committed system and used as the high-precision "before"; each fix
was then adjudicated on the fixed 1000-board corpus as usual.

Three fixes, all found by reading the corpus's worst boards, all of the same
species - **a strength range with no rule**:

- **Opposite the 18-19 2NT jump rebid, responders above 13 HCP had no rule
  at all.**  3NT was bid on 35 combined while BEN bid the making 6NT.  The
  arithmetic opposite a shown 18-19 is exact: 15+ bids 6NT directly (with a
  controls gate - the corpus also produced a 33-combined 6NT missing two
  aces), 13-14 invites quantitatively, opener accepts on 19.
- **A positive response to 2C was raised with the generic four-level rule**,
  which partner read as fast arrival: a 24-count played 4H with twelve
  tricks on top.  Opener's raise of a positive is THREE - slam territory by
  definition - putting the auction on the cue/keycard floor.  That board
  now bids 6H.
- **An 18-count had no 3NT bid.**  The generic notrump band ran 13-17, and
  18-19 balanced hands in ordinary continuations had nowhere to go - the
  reverse-auction board from two rounds back (opener passing a preference
  at the three level with 18) was this bug, not a reverse problem.  Band
  widened to 19; the same board now bids 6D making.

One non-fix worth recording: advancer passing partner's takeout double of a
preempt looked like a bug on the worst-board list (a doubled 3H making),
but the count said 9 such tables, the doubled contract DOWN on 7 of them,
net -9 IMPs.  Passing the double is usually the right call there; the two
visible disasters were the price of correct discipline, and no rule was
changed.

Fixed corpus across the round: -1359 -> -1333 -> -1281.

### The 10,000-board verdict

Both ten-thousand-board matches ran on the identical deals (seed 777), one
on the system as the round began and one after the fixes:

|  | before | after |
|---|---|---|
| total margin | -13342 | **-12988** |
| per board | -1.334 | **-1.299** |
| boards won / lost | 1992 / 3859 | 1976 / 3830 |

The paired reading is the trustworthy one: the fixes touched **120 of the
10,000 boards**, and on exactly those boards the round gained **+354 IMPs**
(71 improved, 41 worse).  Since the other 9,880 boards are bit-identical,
that +354 carries essentially no sampling noise - it is the round's true
value, +0.035 IMPs per board.

Two calibration lessons from running at this scale:

- The 1000-board corpus numbers were optimistic in level but right in
  direction: it showed +78 for these fixes where the 10k shows +35 per
  thousand.  Small corpora overweight their own hot boards; the paired 10k
  is the number to quote.
- The headline "-1.48/board" of the early matches and today's "-1.30" are
  not directly comparable either - different seeds, different noise.  The
  like-for-like series is the fixed corpus (-1.474 at its start, -1.281
  now) and this paired 10k.

Where the engine stands after the round: **-1.30 IMPs/board against BEN**,
down from about -1.47 when head-to-head play began.  Roughly a quarter of
the original deficit is gone, all of it from reading the match's own boards
and fixing what they showed - and the largest remaining pocket is still
slam depth (BEN bids five slams for our one), which is a structure problem,
not a threshold problem.

## The trump-setting round: routing auctions onto the slam floor

The known target from the 10k round - the raise structure jumps straight to
game, so the cue/RKC machinery that exists is rarely REACHED - held up under
tracing.  After `1S - 2C - 2S` a seventeen-count with three-card support had
no authored rebid at all, so the generic toolkit's game raise fired: a
NON-FORCING 4S, auction over, slam never sniffed.  The whole family of
positions where a 2/1 game force should set trumps below game was missing.

Authored this round, all of one theme:

- **Responder's trump-setting raise in 2/1 auctions**: over opener's 2M
  rebid, 2NT rebid, second suits, and the 1S - 2H pair, 3M = 3+ trumps and
  13+, game-forcing, slam-friendly.  **Fast arrival carries the negative
  inference**: the flat 12-13 minimum jumps to 4M directly, so the cheap
  raise promises real values - its shown floor of 13 is what lets opener's
  cue gate (14 own, 28 combined) open opposite it.
- **Opener's strong jump rebid** (`1M - 2m - 3M`, and `1S - 2H - 3S`): a
  self-sufficient six-card suit with 15+ sets trumps from opener's side.
  The board that taught it: `1S - 2H - 2S - 2NT - 3NT` passed out with 6S
  cold, the 17-count having hidden behind a 12-21 rebid.
- **Wide game raises were shadowing the slam rules by priority.**  The
  specific contexts' 4M raises read 13-40 (or 19-40), so a 19-count jumped
  to game while the RKC rule (priority 46) sat unreachable behind priority
  54.  Every such raise is now capped where the keycard gate opens opposite
  the shown range: 18 opposite a 12-15 raise, 24 opposite a 6-9 raise or a
  1-level response, 20 opposite a limit raise.
- **Responder may move over opener's 19+ double raise to game** (`1m - 1M -
  4M - 4NT`): the raise is a sign-off only from opener's side, and twelve
  facing nineteen is exactly the keycard gate.  Without the rule the
  position was dead whatever responder held.
- **Slam arithmetic opposite opener's strong narrow rebids**, the same
  species as the 10k round's "opposite the 18-19 2NT jump": quantitative
  4NT invites and direct 6NT over the 16-18 jump rebid, the 18-21 jump
  shift, and the 12-14 1NT rebid, each with an accept rule keyed to the
  top of opener's range.
- **Reverse continuations (minimal)**: responder's 5+ major rebid over the
  2D reverse is forcing, opener raises with three, and the existing keycard
  rules take it from there.  Board 279's `3NT+13 tricks` now bids
  `1C - 1H - 2D - 2H - 3H - 4NT - 6H` (BEN bids the grand; most of the
  loss recovered).

Two authoring lessons, both paid for in IMPs on the fixed corpus:

- **WHICH suit a generic 4NT agrees must be decided by something partner
  can see.**  With partner having shown two suits, the four gst_rkc rules
  tied on priority and file order picked clubs; staggering the priorities
  toward the majors instead cost a measured **53 IMPs in one thousand
  boards** - priority is hand-blind, so a hand with ONE spade "agreed"
  partner's spades and played 6S off three while 6C had thirteen tricks.
  The honest disambiguator is auction-visible: **partner's last suit bid**
  (a new `partner_last_suit` when-condition), which read every wrecked
  board correctly.  The reply and the final contract hang on the agreed
  suit, and the asker's holding is invisible across the table.
- **A split range must keep its backstop.**  The first draft of the
  quantitative splits carved 3NT down to the low band and gated the
  invites on shape, so a 4-4-4-1 fifteen-count fell between rules and
  wandered into a generic 3D with 6NT cold - the exact "range with no
  rule" species this project keeps rediscovering.  The 3NT rules keep
  their full band now and the invites simply outrank them in-band.

Measured on the fixed corpus (seed 828282), all steps paired on identical
deals: **-1281 -> -1262 (+19)**; 20 boards' auctions changed, 7 improved,
1 worse.  The one loss is board 308: the capped limit raise now asks
keycards holding 21 total, finds four of five, and bids a 6H that BEN also
bids at the other table - it happens to be off the trump queen and a
finesse.  Bidding the same fifty-percent slam as the opponent is the
correct IMP position; the +13 we used to collect there was BEN's variance,
not our skill.

The changed positions are rare (about 2% of boards) but worth ~10 IMPs
each.  The machinery now composes end to end: trump set below game, cues
with negative inference, keycards, placement - every link exercised by the
corpus.

Hold-out check (seed 606060, never used for any fitting): -1.215/board,
in line with the fixed corpus - the resliced bands broke nothing broad.

## Notrump discipline: stoppers asked for, invites answered

Re-ranking rules by par cost after the trump-setting round left `uc_nt3`
(the generic natural 3NT) on top again: -377 IMPs over 70 uses.  The last
time this rule topped the list, raising its strength gate did nothing -
the rule is a symptom.  Reading its eighteen losing boards found three real
diseases upstream, none of them about strength:

- **The generic 2NT/3NT never asked for a stopper.**  In competitive
  auctions they bid 3NT with the overcalled suit wide open.  The gate is a
  new `weakest_their_stopper` evaluator: `stoppers(their)` reads only their
  FIRST suit - the same trap `lott_total_trumps` fell into - so a
  two-suited opposition left the second suit ungated.  Vacuously satisfied
  when they have shown nothing, so constructive auctions are untouched.
- **Stayman-invite acceptance did not exist** (`1NT - 2C - 2D - 2NT - ?`).
  The generic 13-19 3NT covered the position and "accepted" with any
  opener, so 15-facing-8 played hopeless games.  Now 15 declines and 16-17
  accepts - and over the 2H reply the auction carries a free inference:
  Stayman promised a four-card major and 2NT denied hearts, so responder
  holds exactly four spades and opener's four spades are a known 4-4 fit,
  offered via 3S/4S on the way.
- **Opener's answer to the 10-11 preference invite** (`1M - 1NT - 2m -
  2NT - ?`) was the same hole: pass 12-13, 3NT on 14+, and a 6+ major
  re-offers itself at the matching level.

Fixed corpus, paired: **-1262 -> -1248 (+14)**; 15 boards changed, 8 up,
4 down.  The two biggest "losses" are windfalls correctly given back: a
23-combined 3NT we used to blast that happened to make, and a
stopper-less 3NT that partner's hand happened to cover.  Both are bets
the odds say not to take.

Session so far on the fixed corpus: -1281 -> -1248.

## RKC 5D: the 0-or-3 reply is a counting problem

The RKC continuations after the ambiguous 5D reply (0 or 3 keycards) used
an hcp-18 gate to decide between slam and signoff.  Reading the corpus's
six such auctions showed the gate wrong in both directions: two making
slams were signed off (Jacoby auctions, 30-33 combined, asker under 18),
and an 18-count asker holding three keycards would have bid a slam
missing two aces - it escaped by one point.

The honest rule is arithmetic, since only five keycards exist:

- **Three or more in the asker's hand: partner's "0 or 3" can only be 0.**
  Two keycards are missing; sign off, whatever the point count.
- **Four or more in hand: at most one is missing.**  Bid the slam.
- **Exactly two in hand: genuinely ambiguous**, and partner's shown
  strength decides - opposite a sound raise or extras (12+ hcp of my own
  and 28 combined), zero keycards is not credible; opposite nothing
  shown, it may truly be zero, so stay low.

Both slam branches live in one `any_of` rule so the recorded explanation
stays honest whichever applies (a two-rule version cited "four keycards
in hand" while holding two - the same primary-reading-by-priority
artifact the `partner_last_suit` fix addressed).

All four corpus boards trace correctly.  The 1000-board adjudicating
match for this change was stopped on request before finishing, so it is
committed test-verified but UNMEASURED - the next session should re-run
seed 828282 (last measured state -1248) before building further.

## Where this session leaves the engine

Fixed corpus (seed 828282): **-1281 -> -1248** across two measured rounds
(trump-setting raises +19, notrump discipline +14), the RKC counting
rewrite pending measurement on top.  Hold-out seed 606060: -1.215/board.
Tests 546 -> 569.  Known remaining slam pockets, in observed-size order:
minor-suit slam machinery over 1NT openings (no minor transfers, ~7
missed slams per 1000), minor-agreed cue bids (the cue contexts cover
majors only), and the thin-game invitation dribble (uc_raise family,
-5/-6 a board - judgment, not structure; the Phase 3 result warns
against tuning it).  `stoppers(their)` still reads only their first suit
everywhere except the two generic notrump rules now gated on
`weakest_their_stopper`; sweeping the remaining uses is safe-looking but
unmeasured, so it was left alone.

## The bidding-tips round: the expert canon as gates

A 138-item list of codeable judgment rules (Bergen, Kantar, Klinger,
Woolsey and standard practice) was audited tip by tip against the system;
the full disposition of every tip lives in docs/BIDDING_TIPS_AUDIT.md.
Sixty-three were already implemented, ten were added, the rest are
partial, deferred (mostly evaluation-model re-weightings that would touch
every measured rule at once), or inapplicable (matchpoints modes,
probability estimates the engine expresses through simulation instead).

Added, all test-verified and match-UNMEASURED (no-more-deals instruction;
the next session should re-run seed 828282, last measured at -1248):

- **Rule of 22**: the rule-of-20 light openings also demand two quick
  tricks, so a queen-jack collection stays closed.
- **Preempt vetoes**: 2.5+ quick tricks OUTSIDE the suit veto every
  preempt (16 rules); the 3-level preempts also deny a side 4-card major.
- **Third-seat light openings** (9-11, good 5-7 card major): part
  obstruction, part lead direction, gated on a lead-worthy suit.
- **Preempt once**: a new `i_preempted` engine condition (first call was
  a 2+-level opening or a jump overcall) drives a discipline pass above
  the generic toolkit; forcing continuations and authored rebids are
  unaffected.  This is the honest version of the maxim whose crude
  10-HCP-floor form was measured at -10 IMPs and reverted.
- **Blackwood prerequisites**: no direct 4NT ask with a void anywhere;
  no ask with a worthless doubleton where the cue-bid floor exists.
- **Duplication shutdown**: a new `wasted_in_partner_shortness`
  evaluator (K/Q/J points opposite shown shortness, aces exempt) signs
  off in game over Jacoby shortness replies and splinters.

Two textbook-vs-corpus conflicts were settled for the corpus, and the
adjustment is the round's real lesson.  The strict all-suits quick-trick
veto killed two MEASURED preempt scenarios (a ragged seven-bagger with
AK tight, a vulnerable weak two with KQJ-and-an-ace); AK inside your own
suit is offence, so the veto counts outside tricks only and allows
exactly two.  And the worthless-doubleton Blackwood veto, applied
naively to every ask, deleted measured slams in the positions that have
no cue-bid floor to fall back on - a tip that names an alternative tool
is only sound where that tool exists.

## The expert review: every losing board adjudicated

The maxim round's -46 was handed, board by board, to an external bridge
expert (a fresh-eyes reviewer with no stake in the rules as written; the
full verdict document is docs/EXPERT_REVIEW_MAXIM_ROUND.md).  Every board
with a negative delta got one of four verdicts - implementation bug,
needs exception, delete the rule, nothing wrong - and the verdicts were
implemented mechanically.  What the expert found:

- **The keycard waiver (the centerpiece, ~-38 of the -46).**  The
  Blackwood prerequisites protect an asker who needs to identify WHICH
  cards partner holds; a hand holding 3+ keycards itself gets an
  unambiguous answer and may ask with a void or a small doubleton.  On
  every losing veto board the asker held 3-4 keycards; on the veto's one
  winning board, exactly 2.  The waiver separates the data perfectly and
  is textbook, not curve-fitting.
- **Rule of 22 split by suit.**  Every losing quick-trick pass held a 5+
  major or 5-5 majors; every winning pass was a quacky minor hand.  The
  majors now open on 1.5 quick tricks, the minors keep 2.0, and a 7+
  card suit waives the gate entirely (an 11-count with an 8-bagger had
  NO legal opening - a hole found by a board the gate happened to WIN).
- **Vetoes need quality gates and floors.**  The preempt side-major veto
  now fires only for a REAL major (4+ cards, 1.5+ quality) - it was
  passing seven-baggers to protect Q9874.  The third-seat light opening
  no longer swallows weak-two hands (5-card suits or 11-counts only) and
  passed-hand raises stay at two opposite it.  A context that defines a
  call must carry a floor rule for it (the splinter-wasted context had
  shadowed the generic 4M sign-off into oblivion), boolean vetoes are
  sharp now (a 0.8 soft-match against [0,0] bought a vetoed 4NT), the
  worthless-doubleton evaluator exempts suits partner bid naturally, and
  the minor RKC escape is 6m in the fit, never an unstopped 5NT (-500 on
  a board where 6C was -100).  A hand strong enough for a (vetoed) slam
  ask never ends below game: the raised-minor game acceptance covers the
  floor beneath the gst vetoes.
- **Nothing-wrong boards (~-20) were left alone**: sound openings that
  woke the opponents into their par game, quacky passes that lost to an
  opponent error.  Chasing variance is how rules rot.

Measured on seed 828282: **-1294 -> -1190**, and against the last
pre-maxim measured state **-1248 -> -1190 (+58)** - the best fixed-corpus
reading the engine has recorded.  35 boards changed, 12 up, 10 down
against the pre-maxim state.  The round's meta-lesson: a maxim imported
from the canon is a hypothesis, not a rule; the corpus convicts or
acquits, and an expert reading the convictions finds the CAVEAT the
textbook stated one paragraph below the maxim.

## The expert loop, round 2: a fresh 100 boards, all 40 losses adjudicated

The new working method, run end to end: play a fresh 100-board match
(seed 909090: -130 IMPs, 40 boards lost), hand EVERY losing board to an
external bridge expert with the rule text and engine mechanics, implement
the verdicts, and replay the identical boards.  The verdict document is
docs/EXPERT_REVIEW_100_BOARDS.md: 9 implementation bugs, 12 exceptions,
14 missing agreements, 5 nothing-wrong, 0 deletions - and the expert
reproduced eleven non-obvious boards through choose_bid before judging,
which overturned one of its own early reads.

The five clusters that carried most of the 130 lost IMPs:

- **"The weak two was doubled" had no rules on either side**: advancer
  passed takeout doubles of weak twos on three small trumps, responder
  never raised a doubled weak two on a five-card fit.  Both families
  authored (advances with the penalty pass gated on trump quality, LOTT
  raises, responsive doubles).
- **The big hand had no second action**: side_has_acted:false on the
  balancing doubles (the anti-triple-double guard) also silenced 17-23
  counts after a runout.  New reopening doubles keyed on the new
  my_last_call_was_double engine condition - false for the first reopen
  at 16+, TRUE for a second double at 19+ (the first draft's guard
  blocked the exact 23-count it was built for).  The doubler's raises of
  a minimum advance (17-19 raise, 20+ game) were also authored, in BOTH
  generic families after a reproduction showed the uncontested context,
  not the competitive one, interprets the position.
- **The RKC 5H reply was unpassable**: forcing:one_round on the reply
  plus the forcing-pass filter left the asker ZERO legal candidates with
  hearts agreed, and the backstop invented 5S on a four-card suit.  New
  agreed-suit reply contexts make 5-of-the-agreed-major non-forcing.
- **Invitations answered by silence**: no acceptance rules after
  1H-1S-2m-2NT or 1M-1NT-2x-3x; both authored (the second one is why a
  17-count with ~20 support passed a cold game - the sharp LOTT gate can
  only count partner's SHOWN three trumps, and the fix is the specific
  context, not weakening the gate).
- **First-suit-only residue**: cl_nt1/2/3 and ballow_nt1/2/3 swept to
  weakest_their_stopper; cl_takeout_X gates on a new sharp
  max_their_suit_length (it fit 1.00 holding FOUR cards in their second
  suit); cl_nt1 gained the side_has_acted guard it alone lacked.

Plus the singles: feature-ask replies fixed (a maximum with no feature
had no reply at all, and "solid suit" now means two of the top three
plus quality 3); 4th-seat rule-of-15 openings for all suits (only
spades existed); 6-card suit beats a 1NT rebid; 5332 opposite 2NT plays
3NT not the 5-2 fit; the balancing-double advance ladder (a king
lighter, majors first); 3-level negative doubles and free bids; the
quantitative minor route over 1NT; chunky 5-card majors overcall
instead of doubling; assorted small gates (xd_second honors, xd_rebid
LOTT, rr_run i_have_acted - the penalty doubler was running from its
own double, mixed-raise floor 8, cl_nt2 gate).

Two eval-model additions: `max_their_suit_length` (sharp) and the
`my_last_call_was_double` condition.  Five boards ruled NOTHING-WRONG
were left untouched.

**Replaying the identical 100 boards: -130 -> +50 (+180 IMPs; 28 boards
improved, 4 worse).**  The caveat is stated plainly: these are the boards
the expert reviewed, so the paired +180 is an in-sample number; the
held-out fixed corpus (seed 828282) is the honest generalization check
and is recorded below.

Held-out check, fixed corpus seed 828282 (none of these boards were seen
by the expert): **-1190 -> -1058 (+132 IMPs paired; 149 boards' auctions
changed, 59 up, 47 down)** - the round generalizes, and it is the largest
single-round gain the project has recorded.  Like-for-like series since
head-to-head play began: -1.474 -> -1.058.

## The expert loop, round 3 (seed 919191) - and the loop audits itself

Before this round's review, a counterfactual answered "what did the last
round's fixes do to THIS fresh corpus": 14 boards changed, net -47 - the
+132 held-out gain coexisted with real rough edges, and the diff named
them (a 4-level balancing rebid freed of its rule_of_26 gate turned into
a phantom sacrifice; the new reopening double got passed out by an
advancer with no advance context; the new 1NT-overcall penalty double and
advance rules misfired once each).  The loop's own next iteration caught
all of them: every one appeared in this round's dossier and was fixed on
expert verdict.  That is the argument for fresh-corpus rounds.

The round itself: 100 new deals (-128, 38 boards lost), every loss
adjudicated (docs/EXPERT_REVIEW_919191.md; the expert reproduced ~24
decisions through choose_bid): 8 implementation bugs, 8 exceptions, 12
missing agreements, 13 nothing-wrong, 0 deletions.  Implemented:

- **The doubled-cue hole**: retreat/pull floors so the pair never plays
  its own doubled artificial cue (-800 and -500 on this corpus alone).
- **Advance ladders for every live takeout double** - the recurring
  species: the double of a raised major, the reopening double (last
  round's own addition), and the new 4-level double of a raised weak
  two, each shipped WITH its advances this time.
- **partner_has_acted** (new when-condition) gates the 4-level balancing
  rebids: a balance needs a partner with cards, else it is a phantom
  sacrifice (-1100 once).
- **_their_suits no longer counts their cue of OUR suit** (engine):
  their 2S cue of our opened spades read as "their suit" and zeroed a
  16-count's reopening double - poisoning every their-suit gate in cue
  auctions.
- **The slam floor over their jump overcall** (nx3_cue, 16+ support,
  with opener's sign-off floor authored in the same breath), the
  reverse-continuation family for the minor trees (2NT forcing over a
  reverse; opener answers), opener's rebids over the negative double and
  over their raise of it, the minor slam probe over the 18-19 2NT rebid,
  advances of our 1NT overcall, the sit-for-the-penalty-double floor
  (the double itself is non_forcing now: marking it one-round had the
  filter deleting opener's pass and rescuing the opponents), competitive
  invitational jump rebids, priority repairs (7-5 hands jumped past the
  capped minimum rebid; 2NT over a weak two outranks the off-shape
  double), sandwich hygiene (never "overcall" THEIR suit; a 6-card suit
  overcalls instead of doubling), and LOTT obstruction raises (4-trump
  3-level over their cue; 5-trump NV 4-level over their preemptive jump).

Measured: same 100 boards **-128 -> +30 (+158 paired; 20 up, 4 down)**;
held-out fixed corpus seed 828282 **-1058 -> -982 (+76 paired)** - the
first reading below one IMP per board.  Like-for-like series since
head-to-head play began: -1.474 -> -0.982.

## Round 4: the TRIAGED thousand (seed 303030)

Scaling the expert loop from 100 to 1000 deals meant 368 losing boards -
too many to read one by one, and most of them variance.  The answer was
triage (`tools/triage_match.py`): cluster the losses by the rule that
made our last bid at the table where we did worse against par, then hand
two expert reviewers the twenty biggest clusters (with example boards and
the full member list) plus the thirty worst singles - about 100 boards of
reading covering the great majority of the recoverable IMPs.  Verdict
documents: docs/EXPERT_REVIEW_303030_{A,B}.md.

The clustering earns its keep by making the *nothing-wrong* verdict
reliable: with 43 boards in the "all-pass" cluster the reviewer could see
that the family is a defensive long tail, not a defect, and say so.  Both
reviewers reproduced their diagnoses through `choose_bid` (~55 decisions
between them) before prescribing.

What the round found and fixed:

- **A generic pull/sit floor under EVERY takeout double.**  Three reviews
  running have hit the same species from different angles: a sound double
  answered by an advancer with no matching rule, who "sat" it with two
  small trumps.  Authored ladders kept covering one pattern at a time;
  this is the floor beneath all of them.  Sitting is now a positive
  decision (a real trump stack behind the bid), pulling to a 4+ card suit
  the default.  Two supporting changes: the new sharp
  `standing_suit_length` evaluator (`suit_length(their)` reads their
  FIRST suit, so a double of 4H was gated on club length), and a
  decision-layer relaxation - an AUTHORED pass rule that fits now
  survives the forcing-pass filter, because converting partner's double
  is a positive action and the old "nothing fits anywhere" escape could
  never reach it (some four-card-suit pull always soft-fits).
- **"Our artificial call got doubled", twice more**: doubled Jacoby
  transfers and the strong 2C under interference (which had no contexts
  at all - a 23-count defended their two-level contract).  Plus the
  fallback invariant recommended a review ago and never implemented:
  never pass out our own doubled artificial call.
- **A real interpretation bug**: over 1C the call 2C was defined twice in
  one context (the 6-10 raise and the 2/1), so the readings merged into a
  disjunction and a nine-count raise was read as possibly GAME FORCING.
- **Slam machinery**: the 5H/5S keycard replies are exact counts (2+2
  with the queen is six - the same arithmetic the 5D rewrite got two
  rounds ago); `gf_3NT` gated on stoppers and shape (at priority 34 it
  was beating fit-1.0 natural rebids with six-card suits); `rjr_game`
  lowered below the keycard ask; counting claims moved to a new sharp
  `rule_of_26_sharp`.
- The competitive-raise seam at 10-11 support points, the Jordan 2NT
  reply ladder, Stayman placement reading WHICH major opener showed, and
  ten authored continuation contexts.

**A cost of scale worth recording.**  The class-wide invariant broke a
position no board in the dossier covered: with the fallback pass withheld
and doubled Stayman entirely unauthored, a seat could end up with ZERO
candidates and the match aborted on `no legal candidate`.  The repair is
two-part and general - the forced-continuation backstop now also fires
when the pass is withheld, and a final safety net restores the pass if
nothing else could be generated - plus the authored Stayman escape.  A
fix that changes a whole class needs a floor for the whole class, not for
the boards that motivated it.

Measured: the same 1000 boards **-1117 -> -808 (+309 paired; 80 boards
up, 59 down)**, and the held-out fixed corpus **-982 -> -826 (+156
paired)** - the largest held-out gain of any round so far.  Like-for-like
since head-to-head play began: **-1.474 -> -0.826 IMPs/board.**

On method: the triaged thousand cost roughly twice a 100-board round
(two experts, ~480k agent tokens, four 1000-board matches) and returned
+156 held-out against the +76 and +132 of the two 100-board rounds.  Its
real advantage is not volume but *confidence*: a defect seen in eight
boards is diagnosed correctly, and a variance board seen once is
correctly left alone.

## The lint suite: stop rediscovering the same four defects

Three consecutive expert reviews found the same defect species by hand.
Reviewer attention is the scarce resource in this loop, so those species
are now machine-detected (`tools/lint_system.py`, `tools/fuzz_decisions.py`,
locked by `tests/test_lints.py`):

- **collide** - one context defining a call two incompatible ways.  Same-call
  rules merge into a disjunction, so the reading partner decodes is the
  union: over 1C the 2C response was both the 2/1 and a 6-10 raise, and a
  nine-count drove to five of a minor.  The detector is validated against
  the pre-fix system, where it rediscovers that exact bug in a second.
- **gap** - an interior strength band no rule in a band-laddered context
  covers.  "Range with no rule" is the most recurring defect in the
  project's history and it is silent, because the permissive pass floor
  swallows the hole.
- **soft** - a boolean or counting evaluator used as a gate without a sharp
  tolerance registered.  This found a live bug immediately: `two_of_top3`
  was gating twenty-four rules - every "two of the top three" penalty pass,
  every chunky-major double denial - and a hand WITHOUT the honours scored
  0.8 against the [1,1] gate, so none of those gates actually gated.
  Sharpened, along with `three_of_top5` and `good_suit`.
- **fuzz** - random self-play auctions looking for a seat with ZERO
  candidates (the doubled-Stayman abort that killed a twelve-minute match)
  and for anchored contexts whose hands fall through to an invented
  fallback.  3,000 decisions run clean in about a minute.

Two lessons from building them.  The first drafts of `floor` and `gap`
reported 1605 and 4 findings, all noise: static shadow analysis per call is
hopeless because the generic toolkit defines nearly every call, and a
strength band stated across `any_of` branches is not a gap.  A lint whose
output nobody reads is worse than no lint, so `floor` was narrowed to the
one verifiable shape (a context where every rule is gated and no pass is
offered, so it can produce nothing) and is advisory, not enforced.  The
second: a detector that cannot be shown to catch its motivating bug is not
evidence of anything - hence the fixture in `tests/fixtures/`.

## Round 5 (triaged 1000, seed 515151): starved seats, not bad rules

The finding that reframed the dossier, and the most useful sentence any
review has produced about this engine: `fast_decision` picks by priority
among candidates fitting >= 0.9, and every generic context ends in a
catch-all pass with `requires: {}` - which fits **1.00 on every hand** at
priority 18-21, above every fallback.  So **any hole in an authored ladder
becomes a pass by construction.**  The two biggest clusters ("all-pass",
192 IMPs, and `uc_nt3`, 112) are not bad rules; they are *starved seats*,
and most of the round's fixes are missing contexts rather than exceptions.

Both reviewers reproduced every indictment through `choose_bid`, and one
of them prototyped its whole fix set in a scratch copy and re-ran the
motivating boards before prescribing - which is why so much of it landed
unchanged.

Applied: new contexts for opener's rebid over a 1NT response, responder
after 1D-1S-2C, and GF landing; `general_pull_or_sit` re-gated by LENGTH
rather than suit rank (it was ordering pulls S>H>D>C, so 4=6 in the majors
bid the spades) with the weak-hand pass restored and negative-double
auctions excluded; `ballow_X`/`balhigh_X` reading the STANDING suit rather
than the opponents' first (a textbook 14-count reopening double of 2H
scored 0.000 because the rule read the doubler's diamonds); the keycard
asks no longer double-counting the sharp LOTT gate; the 2/1 over 1H
denying four spades; five-card rungs on the competitive 2NT ladder; and
own-long-suit rungs in three ladders.

Two bugs of my own, found by verifying an expert's report rather than
trusting it:

- **The round-4 forcing-pass relaxation was defeated by its own escape
  hatch.**  It admitted any authored pass fitting >= 0.9, and the generic
  floors are authored rules with `requires: {}` - so one-round forces
  could be passed out wholesale, including alertable artificial ones.  The
  relaxation now demands a DISCRIMINATING pass (one whose constraint says
  something about the hand); the trump-stack conversion it was built for
  is unaffected.
- **A round-3 edit had silently not applied.**  Opener bid 3NT over
  partner's Jordan 2NT holding AQ932 and a known nine-card fit, because
  the ladder still demanded six cards: the fix script had matched concrete
  suit letters (`oc2nt_3H`) against template-var rule ids (`oc2nt_3$M`)
  and changed nothing while reporting success.  Jordan promises four-card
  support, so it has its own anchored context now.  **Every scripted edit
  must assert that it applied** - an edit that reports success and changes
  nothing is invisible for a whole round.

Measured: same 1000 boards **-1365 -> -1143 (+222 paired; 61 up, 36 down)**;
held-out fixed corpus **-826 -> -700 (+126 paired)**.  Like-for-like since
head-to-head play began: **-1.474 -> -0.700 IMPs/board.**

Both reviewers independently named the same two meta-species the current
lints do not catch, and both proposed detectors: *a ladder that bands by
strength forgets to band by shape* (four contexts here had no rung for
responder's own long suit - invisible to the `gap` lint, which sees
strength only), and *a gate added to one rule is not added to its
siblings* (four instances this round).  Those are the next two lints.

## Expert round 6 (triaged 1000, seed 626262)

Both reviewers, working the same triaged clusters independently, named the
same species: **ceilings**.  A dozen ladders capped their top rung at 18 and
had nothing above it, so a 19- or 20-count found no rule that fitted and the
soft model handed the hand to whichever sign-off missed by the fewest
points.  `r1sr_4H` signed off in game with 33 combined; `rmr_newsuit_D`
capped a forcing new suit at 12; `fsf_$F`'s shape gates ("no clear natural
bid") shut out hands whose alternative was not a better natural call but a
game two levels below the hand.  A ceiling is not a safety limit; above it
there is no floor, only whatever the fallback machinery invents.

Also fixed, each verified on the board that found it:

- **`rkc5H_slam` ignored the queen the reply had just denied.**  5H says
  *two keycards without the trump queen*.  Counting to five keycards cannot
  conjure it: in a seven-card fit it is a trump loser.  The slam now needs
  the queen in hand or a fit long enough to drop it - and its **sign-off had
  to become a complete fallback**, because a signoff gated as the exact
  mirror of the slam rule left the seat with no fitting candidate at all,
  and the declined slam won the soft-miss lottery anyway.
- **A "feature" is one top honour.**  All nine `feat_*` replies to the
  weak-two 2NT ask were gated `two_of_top3` while their own `shows:` text
  said "ace or king", so every maximum whose outside card was a bare ace
  answered "minimum, no feature".  New `top_honour` evaluator.
- **A takeout double must not hide a six-card suit** (`vw2_X`, `oc1D_X`,
  `oc1H_X`): the double asks partner to pick, and with six of my own there
  is nothing to pick.  The strong branch still doubles first and bids after.

### The overfitting, and what it cost to find it

The first fix set measured **+223 on the corpus the experts read and -66 on
the held-out corpus**.  Three "add a gate" fixes, each argued from two or
three boards, were deleting whole families of correct auctions elsewhere:

1. `qr3_6NT` / `qr3_4NT_quant` gained `semi_balanced`.  Five cold 6NTs died.
   Thirty-three combined points *with a long running suit* is the best 6NT
   hand there is, not a disqualified one.
2. `slam_try_over_game_raise` is a **more specific context** than the general
   keycard one, so it interprets 4NT after every game raise - and its
   narrower gate did not add slam tries, it deleted the asks that already
   worked (three cold slams stopped in game).  A new context that shadows an
   old one must carry the old gates verbatim as a rung, so it can only ever
   be a superset.
3. The 3$M checkback ladder was authored **without the seat that answers
   it**.  Opener's reply fell to the generic toolkit and bid 4C over a
   game-forcing 3S.  A ladder and its answering context are one fix.

**A gate justified on two boards needs the held-out corpus before it is
kept.**  A fix that *adds* a rung can only fill a hole; a fix that *adds a
gate to an existing rule*, or *adds a more specific context*, subtracts
behaviour everywhere it reaches, and the corpus that motivated it is the one
place it is guaranteed to look good.  Those two classes now get measured
separately.

Measured, after the three repairs: same 1000 boards **-754 -> -584 (+170
paired; 48 up, 29 down)**; held-out fixed corpus **-700 -> -639 (+61
paired)**.  Like-for-like since head-to-head play began: **-1.474 -> -0.639
IMPs/board.**

### Two measured experiments on the points estimators (round 6 follow-up)

Expert B's §2 argued the `rule_of_26` question directly, and its verdict was
*against* the obvious reading: measured across six slam boards, the estimator's
mean error is **-0.25** - it is not systematically pessimistic, and "repairing
only its pessimism would make things worse".  What B did name is a **units
mismatch**: `floor = max(partner_min_hcp, partner_min_points)` mixes an HCP
floor with a total-points floor.  Each claim was run as its own experiment on
the held-out corpus, with nothing else in it.

**Experiment 1 - the units-mismatch repair (`floor + 1.5` opposite an
unbounded opening): -20 IMPs. REVERTED.**  23 boards changed, 5 up, 10 down.
B flagged the risk direction correctly: it makes `rule_of_26` fire *more*
often, and `rule_of_26` is the acceptance gate on families the same review
found already over-bidding.  The estimator is not the lever.

**Experiment 2 - the singleton-honour double count: +1 IMP.  KEPT, on
explainability, not on score.**  15 boards changed, 7 up, 3 down: noise.
`shortness_points` credits a singleton 3 whatever the card is, so a raw sum
made a singleton KING worth **six points** - three for the honour and three
for the shortness that renders it nearly worthless.  The score does not care;
`explain_bid` should not justify a bid with points that do not exist, so the
correction stays and a unit test locks it.

B's literal one-line version of experiment 2 (`total_points` -> `adjusted_hcp`
in the fit branch) was **not** what got implemented, and the reason is worth
recording: `adjusted_hcp` also carries a *+0.5 bonus for honours in a long
suit*, which makes hands **stronger** - the opposite direction from B's own
evidence, both of whose boards need hands to get weaker.  It broke a measured
scenario by accepting a limit raise the corpus had established should be
declined.  Implemented narrowly instead: deduct 1 for a stiff K/Q/J outside
trumps, the single holding where the two accountings actually overlap.

**An expert's diagnosis and an expert's patch are separate artifacts.**  The
diagnosis here was right and the patch reached past it; the tests caught the
difference.

## Expert round 7 (triaged 1000, seed 747474)

Baseline **-726 IMPs**, 316 losing boards, 20 clusters, two independent expert
reviews (`docs/EXPERT_REVIEW_747474_{A,B}.md`).

Measured, core batch: same 1000 boards **-726 -> -580 (+146 paired; 31 up, 14
down)**; held-out fixed corpus **-639 -> -627 (+12 paired)**.  Like-for-like
since head-to-head play began: **-1.474 -> -0.627 IMPs/board.**

The two corpora agreed in sign for the first time in three rounds.  That is the
point of the round-6 pre-brief, which both reviewers were given as a hard
constraint: state what a gate SUBTRACTS, make a shadowing context a provable
superset, ship a ladder with the seat that answers it.

### The species this round: a gate given to one sibling and not the other

- **`balhigh_reopen_X` carried a light 12-point branch that its low-level twin
  `ballow_reopen_X` does not have.**  Backwards: balancing a king lighter is a
  one- and two-level agreement, and at the three level the double commits
  partner to the FOUR level, so partner - who has passed throughout - converts
  it and every light one became a penalty double made on takeout shape.  The
  rule is now capped at the three level too: you cannot take a four-level
  contract out for takeout.  18 tables, -89 IMPs whole-corpus.
- **The generic MINOR ladder ranked its uncapped invitational rung above both
  game rungs**, so with a minor fit the toolkit could never bid game by raising.
  The major ladder was already ordered correctly.  Re-ranked rather than capped:
  a ceiling would have opened a hole for the catch-all pass to swallow.
- **The RKC trump-queen clause existed only on the 5H reply** and was never
  swept onto 5C/5D - shipped with the complete-fallback signoff it requires,
  which is not optional: without it the seat is empty and the engine invents a
  call.
- **`rr1H1SC_2S` had an identical untouched sibling `rr1H1SD_2S`.**

### Ceilings again (round 6's species, still paying)

A one-level new-suit rebid capped at 17 left 18-19 WITH a four-card major no
rule at all, so an 18-count holding 4-4 in the majors bid a generic 3NT.
Stayman's ladder stopped at 15, so an 18-count with no fit passed 2S with 6NT
cold.  Five starved seats were authored, each with the context that answers it.

### What the reviewers refused to do, which is why the held-out number held

Both spent as much effort killing hypotheses as proposing fixes, and both
re-scored suspect rules across ALL 2000 tables (winners included) before
accusing them:

- **The largest cluster was not a bug.**  `all-pass` (28 losing boards, 140
  IMPs) is the single most profitable family in the engine: +1538 IMPs, 264 wins
  to 84 losses.  The losing boards are the defensive long tail.
- **`uc_nt3` is a symptom for the third round running** - it fits 1.00 on nearly
  every board it loses.  Do not tighten it again.
- **"A takeout double must not hide a six-card suit" does not generalise** to
  the remaining siblings: measured across 113 firings, doubles WITH a 6+ suit
  average **-2.00**/table, WITHOUT **-2.54**.  Killed.
- One reviewer prototyped a priority demotion, **measured it worse on its own
  motivating board, and reported the negative result** instead of shipping it.

### The shadowing trap, caught a second time - by a test

The deferred batch's first version added natural suit overcalls of a weak two.
That new context took over interpreting `2S` at those auctions, and its narrower
gate DELETED a better-fitting reading: a 17-count's 2S fell from fit 0.76 to
0.33, so the engine began reporting a genuine X-versus-2S judgment as "clear".
A locked arbitration test caught it.  Fixed by carrying the shadowed generic
gate verbatim as a companion rung, so the context can only be a superset - the
rule round 6 wrote down, applied.

**A context that DEFINES a call takes over interpreting it.**  That is the whole
lesson, and it now has two scalps.

### Deferred, deliberately: measured on its own

Both reviewers independently marked the weak-two natural overcalls as needing
their own measurement (one measured the affected population as genuinely split,
+38 of wins against -78 of losses).  Measured alone on the held-out corpus:
**-627 -> -621, +6 IMPs over 9 changed boards (4 up, 3 down).  Noise.**

**Kept, on structure rather than score**, the same call as round 6's
singleton-honour fix: the defence to a weak two had NO natural suit overcall at
all, while its sibling - the defence to a three-level preempt - has a full set;
`vw2_pass` at priority 30 outranked the generic toolkit's overcall at 26, so an
eleven-count with KQJ95 passed 2D out.  That is a hole in the convention card,
it is explicable in one sentence of bridge, and the superset guards mean the new
contexts cannot subtract a reading.  The score does not care either way.

Round 7 final held-out standing: **-621 (-0.621 IMPs/board)**.

The method is now written down in `docs/ROUND_METHOD.md` so a session with no
memory of these rounds can run one correctly.

## Expert round 8 (triaged 1000, seed 858585)

Baseline **-710 IMPs**, 322 losing boards, 20 clusters, two independent expert
reviews (`docs/EXPERT_REVIEW_858585_{A,B}.md`).

Measured: same 1000 boards **-710 -> -527 (+183 paired; 20 up, 1 down)**;
held-out fixed corpus **-621 -> -612 (+9 paired; 7 up, 5 down)**.  Like-for-like
since head-to-head play began: **-1.474 -> -0.612 IMPs/board.**

Both reviewers ruled the three biggest clusters NOTHING-WRONG, independently and
from the same data: `all-pass` is 553 tables at a mean of **-0.69** against a
corpus-wide table mean of **-0.71** - a quarter of the corpus, sampled, not a
loss concentration; `uc_nt3`'s entire net across 2000 tables is **-61** against
a cluster headline of 141, spread over **23 distinct auction families** (a
symptom for the fourth round running); and `uc_raise_H4` (-1.07/table) and
`uc_raise_S4` (+0.27) are character-for-character identical rules, so the gap
between the twins is the auctions, not a sibling asymmetry.  Between them the
two reviewers killed eighteen hypotheses with data.

### The species this round: an invitation nobody could accept

Four separate positions turned out to be a bid that forces or invites, authored
without the seat that answers it - round 6's "a ladder and its answering context
are one fix", found four more times:

- **`rmr_4NT` and `nt2_tr_slam`** are quantitative invitations, and no context
  matched their auctions at all, so opener's only candidate was the code
  fallback pass.  Every invitation was declined by construction.  Three sibling
  quantitative raises in the file (`rjsq`, `rrntq`, `rjrbq`) already ship with
  their accept context; these two did not.  Both authored, plus the missing
  `nt2_tr_6NT` rung ABOVE the invite - 15 opposite a shown 20-21 is 35 combined,
  which is a slam, not an invitation.
- **`r1c1d_3D_$M` is forcing one round** and had no answering seat, so opener's
  best non-pass candidate fitted 0.28 - below the documented 0.3 "nothing fits
  anywhere" threshold - and the escape hatch legally passed the force out.  A
  19-count's forcing jump died in 3D with 6NT cold.
- **`opener_over_invite_2NT_minor` contained exactly one rule**, the 5m sign-off,
  so every hand that was not "6+ minor, 16-21, no stopper" fell to the generic
  toolkit and rebid the minor.  AKQJ976 opposite an 11-12 invite is nine tricks
  and was bidding 3D.

### Ceilings and sibling gates, still paying (rounds 6 and 7's species)

- **Stayman's ladder has a ceiling on the FIT half only.**  With a 4-4 fit the
  rungs ran 8-9 / 10-15 / 15-17 and stopped; the no-fit half of the same context
  was given its 18-21 rung a round ago and this half was never swept, so 18
  opposite a 15-17 notrump with a known eight-card fit passed 2H.  The same rule
  was also missing the round-6 keycard waiver every other ask carries.
- **`resp_preempt_*` topped out at the game raise**, so every slam opposite a
  seven-card suit was signed off by construction.  BOTH reviewers found this hole
  independently and proposed different gates; the merged rule takes the counted
  nine-card fit plus **four** of the five keycards, because the three-keycard
  draft bid a 6S with eleven tricks (a measured -12) and the alternative gate
  excluded that board only by a one-point total-points margin.  Opposite a hand
  that has shown 4-9 HCP, three keycards is not enough for the reply to keep you
  out of a slam off an ace.
- **`ob_1H1S_3H` states its gate in raw HCP and ranks below the simple rebid**,
  while its exact sibling over the 1NT response uses playing points plus suit
  quality and outranks it.  15 HCP with seven hearts and a singleton is an
  eighteen-point hand and was rebidding "minimum".
- **`gst_rkc_$X` kept a three-card trump floor its own game raise had dropped
  to two** opposite a SHOWN six-card suit.
- **`opener_over_negative_double` capped every rung at 16**, so 17-19 had no
  rule and the generic 3NT took the hand.
- **The strong branch of `oc1S_X`/`oc1H_X` never constrained THEIR suit.**  The
  weak branch demands shortness; the strong branch constrained only the other
  major, so a seventeen-count holding AQ976 doubled 1S for takeout and heard
  partner name hearts.  Exactly two of 31 firings hold five of their suit and
  they carry -17 of the family's -20.

### The advance that is owed when they compete

`general_pull_or_sit` covers `... - X - P - ?` only.  When RHO **bids** over
partner's takeout double there was no advance context at all, so the seat fell
to `general_competitive_high`, whose new-suit rungs demand 14+ total points - a
floor calibrated for a partner who OVERCALLED - and a seven-card major with nine
points had no call.  Authored with a new `partner_last_call_was_double` engine
condition (the mirror of `my_last_call_was_double`), the negative-double answer
carrying `adx_neg_major_$M`'s gates verbatim so it can only be a superset, and
the doubler's missing three-level game raise: his 17-19 rungs are all
`cheapest_in_suit`-gated and therefore unreachable once the advance is already at
the three level, so a seventeen-count facing a forced advance passed.

The 8-point floor on the new rungs is not cosmetic and is worth recording:
same-call rules merge into a disjunction for the partner model, so a rung with no
floor lowers partner's shown minimum for that call **everywhere**.  Without it a
cold 4S elsewhere in the corpus turned into a pass, because partner's 3S dropped
from a shown 10 to a shown 0 and `rule_of_26` stopped opening.

### Measured as their own experiments, and what that decided

Five changes were held out of the batch and measured alone on the held-out
corpus, either because a reviewer flagged them high-variance or because the two
reviewers disagreed.  Three were kept and two were reverted, and both reverts
are the round's real lesson.

**REVERTED - the keycard ask over a game raise (-17 held-out).**  This is the one
place the two reviews contradicted each other, and the disagreement was the
signal.  B measured the family at 16 asks for -35 IMPs, observed correctly that
after a 4M game raise the sign-off is 5M - one level above the contract we
already owned, so the ask is weakly dominated unless it reaches a slam - and
proposed gating it on three keycards, worth +14 on the review corpus.  A refused
to propose any gate there, having tried and rejected three separators (HCP does
not separate: losers 18/13/15/13/14, winners 16/16; keycards-in-hand does not
separate: losers 3/2/2/2/2, winners 2/2) and having noted that the only thing
that does separate - partner's fast-arrival cap - is invisible because
`total_points` has a floor channel in the partner model but no ceiling.
Measured alone on the held-out corpus the gate is **-17**, and the mechanism is
exactly the one this file already warns about: `gr_rkc_general_$M` exists as the
round-6 superset guard, so gating it does not add slam tries, it **deletes the
asks that already worked** - three cold slams (boards 25, 68, 660, all making
twelve tricks) stopped in game to save two five-level sign-offs.  The file's own
comment on that rung says so in as many words.  A was right, and the reason the
project runs two independent reviewers is that one of them refused.

**REVERTED - a sharp tolerance for `weakest_their_stopper` (-9 held-out).**  The
diagnosis is certainly correct and is recorded as a confirmed open item: the
evaluator gates 27 rules - every generic natural notrump in a competitive
auction - on `[0.9, 9]`, and it has **no sharp tolerance registered** in
`_EVAL_S2` while both its siblings `stoppers` and `weakest_unshown_stopper`
carry 0.3.  On the default sigma a hand with NO stopper in their suit scores
**0.835** against that gate and a partial stopper (Qx/Jxx) **0.965**, so none of
those gates actually gate; the engine bids 3NT saying "their suits stopped"
while holding Q4.  But the repair as applied is a class-wide gate with no floor
beneath it: measured, the wins are real (four hopeless notrumps not bid) and the
losses are the seat left behind picking a worse suit contract - 2H becoming 4H
down, a 4S off five where 5D made.  A predicted this precisely ("real
correctness repair, real risk of trading bad games for starved seats").  A fix
that changes a whole class needs a floor for the whole class, which is round 4's
lesson; the seats it starves have to be authored first.

**KEPT on a neutral held-out number**, all three measured at exactly 0 held-out
and positive on the review corpus, the same call as round 6's singleton-honour
fix and round 7's weak-two overcalls: the 12-HCP floor on a four-level new suit
in competition (+15 review; shortness turned a ten-count into a "fourteen" and it
bid 4H over their 3NT for -1100), the takeout-double repair above (+17 review),
and a shape rung on the jump-shift reply ladder (+4 review; banded by strength,
never by shape, so 5-5 with a singleton had only the catch-all 3NT).

### An expert's patch reached one point past the diagnosis, and a test caught it

B's `qr3_4NT_quant` finding is sound and settles a DELETE-THE-RULE candidate this
file has carried for two rounds: the invite fired five times in 2000 tables and
was declined five times, the accept rung has **never** fired, and 4NT and 3NT
score identically on ten, eleven and twelve tricks - so the only thing the invite
could do was turn a making 3NT into a failing 4NT, which is what it did.  The
proposed floor of 32 combined broke a locked regression scenario.  Measured
across all five firings plus the scenario, the losing invite reads **30**, the
winning one **31**, and the canonical 17-opposite-16 case the convention was
authored for reads **31** exactly.  The floor is 31: it excludes the only losing
invite, keeps the winner, and keeps the convention.  Round 6 recorded that "an
expert's diagnosis and an expert's patch are separate artifacts"; this is the
same lesson a second time, and the regression suite is what caught it.

### Method note

The two corpora agreed in sign for the second round running, and the review
corpus's +183 against the held-out +9 is the usual and expected gap: the review
corpus is where the fixes were found.  The held-out gain is small and inside the
noise of a single 1000-board match, which is the honest reading of a round whose
biggest three clusters were correctly ruled NOT to be defects.  Both reviewers
were briefed with round 6's shadowing lesson as a hard constraint and both spent
as much effort killing hypotheses as proposing fixes - eighteen non-findings
between them, including four prototypes each reviewer built, measured worse, and
reported rather than shipped.

## Expert round 9 (triaged 1000, seed 969696)

Baseline **-952 IMPs** on the review corpus, 370 losing boards, 20 clusters, two
independent expert reviews (`docs/EXPERT_REVIEW_969696_{A,B}.md`).  The -952 is a
harder corpus draw than round 8's -710 and is not a regression: the like-for-like
series is the held-out corpus.

Measured: same 1000 boards **-952 -> -788 (+164 paired; 23 up, 4 down)**;
held-out fixed corpus **-612 -> -576 (+36 paired; 15 up, 7 down)**.  Like-for-like
since head-to-head play began: **-1.474 -> -0.576 IMPs/board.**  The best held-out
gain since round 5.

### The dossier named the wrong rule, twice, and both reviewers caught it

The triage tool attributes a cluster to the **primary reading** - the
highest-priority same-call rule - not to the rule whose constraint actually
matched.  Both reviewers independently re-ranked the decisions to find the real
chooser, and on two clusters the headline rule had never fired at all:

| dossier cluster | rule that actually chose | tables | mean |
|---|---|---|---|
| 4 `ch_penalty_X` | `ch_penalty_X` itself | 14 | **-1.00** (baseline) |
| 4 `ch_penalty_X` | `ch_negative_X3`, hidden beneath it | 7 | **-4.57** |
| 11 `ballow_nt2_strong` | `ballow_nt2` (an 11-12 rule) | 4 | -5.00 |

Anyone triaging by the dossier field alone would have gated the wrong rule.  This
is now the standard first step of a review, and it should stay one.

### What both reviewers found independently: the trump-queen clause's premise

Round 7 swept `rkc5H_slam`'s trump-queen clause onto the 5C and 5D replies.  The
clause's own comment states its premise - *"a keycard is already unaccounted for,
so the trump QUEEN cannot be missing as well"* - and that premise is **provably
false** in two branches:

- **5C shows one or four.**  Holding four myself, partner's reply can only be one
  (four would make seven), so **every keycard is present** and the reply has said
  nothing whatever about the queen.
- **5D shows zero or three.**  Holding two opposite shown values, the reply can
  only be three - again all five present.

In both positions the clause vetoed a slam on a card that is a finesse at worst,
and the asker *knew* nothing was missing.  Both rewrites are provable supersets.
Two boards, +24 in sample; on the held-out corpus it is 1-for-2 (a cold 6S bid,
a 6H off the queen going down), net -1 - noise, kept on the arithmetic.

### A ceiling, a starved seat, and two bands that disagreed

- **The 2NT overcall of their weak two had no answering seat at all**, so it was
  passed out on every one of its six firings - once with eleven points opposite
  the shown fifteen and 3NT making twelve tricks.  +23 held-out on its own.
- **`opener_over_invite_2NT_minor`'s two accept rungs used different floors** -
  3NT accepted from 14, the minor game only from 16 - so 14-15 with a six-card
  minor and a suit wide open had no choice but notrump.
- **`rmr_2M` demanded SIX cards**, so 5-4-4-0 with a void in opener's rebid minor
  had no call and the soft-miss lottery invited in notrump on nine points.
- **The minor game-force landing had only the 3NT and 5m halves** of its own
  documented design ("3NT without a fit, 4M with one"), and 3NT outranked the
  generic toolkit's raise, so a counted eight-card major fit lost to notrump.
- **Higher of equal length was never carried above the one level.**  The 2-, 3-,
  4- and 5-level new-suit rungs are flat in priority within a level, so two suits
  of equal length both fit 1.00 and file order (C, D, H, S) handed the auction to
  the LOWEST one: a 21-count 5-5 in hearts and diamonds bid 4D.  Forty
  strict-subset twins at +0.5 priority, so no reading is deleted.
- **Opener's answer to a negative double existed for the two-level overcall
  only** and was never given its one-level twin, which is the commoner auction.
- **3NT opposite a preempt demanded a stopper in PARTNER'S suit** - the one suit
  that needs none, since it is the source of tricks - and said nothing about the
  three the defence is about to lead.  One went down six.
- **The competitive-raise seam at 11-13.**  Every three-level raise rung carries
  `cheapest_in_suit: true` and is therefore not offered while the two-level raise
  is legal, and the two-level rungs capped at 9-10 - so a hand with 11-13 support
  points had no raise at all.  "Range with no rule", the most recurring defect in
  this project's history.

### The bundled batch measured -19, and decomposition is why the round survived

The nine-fix main batch measured **+123 in sample and -19 held out**.  Rather than
revert the batch, every fix whose changed boards could be attributed was measured
alone against the same held-out corpus.  The decomposition was exact:

| | held-out |
|---|---|
| core (six fixes) | **+23** |
| the four-level pull ladder | **-22** |
| 2NT Stayman over interference | **-12** |
| the responsive double made non-forcing | **-8** |
| **bundled total** | **-19** |

+23 - 22 - 12 - 8 = -19, so nothing was hiding.  All three losers were reverted
and the core kept.  **A batch that measures negative is not necessarily a batch
of bad fixes**; without the decomposition this round would have thrown away a
+23 core to escape a -42 tail.

The three reverts are worth recording individually, because each was argued well
and lost to the corpus anyway:

- **The four-level pull (-22).**  The seat was provably empty - a hand with seven
  diamonds and a singleton spade could not pull partner's double of 3S and
  converted it for penalties.  But the reviewer's own ENDANGERS line named the
  reason it fails: *there is still no condition for "partner's double was
  PENALTY"*, so the new rungs pull business doubles too, and on the held-out
  corpus that is exactly what they did - a 4CX down six became a 4D of ours.
  The fix is sound only once that condition exists.
- **2NT Stayman over interference (-12).**  Structurally unarguable - a 20-count
  sat for a double of an ARTIFICIAL 3C, and the 1NT ladder has carried this twin
  for rounds.  Its author measured it at zero on its own board and asked for it
  as a structure keep.  Held out it is -12 on one board, where sitting collected
  500.  Reverted on the number, and recorded as the strongest remaining
  structural gap in the file.
- **The responsive double made non-forcing (-8).**  Same shape: the forcing-pass
  filter deletes the doubler's pass and above the three level there is nothing
  below game to bid, so the fallback invented a 4NT.  Held out, letting the
  doubler pass let a 4HX make.

### Measured alone, and what that settled

- **Sweeping the three negative doubles onto `standing_suit_length`: -40 held
  out. REVERTED.**  The *diagnosis* is a genuine engine-level finding and stands:
  `_their_suits` seeds itself LHO-before-RHO, so `suit_length(their)` means "my
  LHO's suit", not "their first suit" as the file's comments and this document
  both say.  Reproduced on three synthetic auctions.  Round 4 fixed exactly this
  once, for a different rule, by adding `standing_suit_length`.  But sweeping the
  three negative doubles onto it costs 40 IMPs held out (1 board up, 7 down), so
  the evaluator's misnaming is now a documented open item rather than a repair.
- **The keycard ask over a standing game, again.**  Both reviewers reached the
  cluster from different directions and both refused to gate it.  One tested the
  separator nobody had tried - a floor of two keycards on the *asker* - and found
  the metric degenerate (8 asks with <=1 keycard for -25, 46 with >=2 for -167,
  and only 3 of the 8 are genuine keycard asks).  Round 8 measured a gate there
  at -17 held out.  It stays unfixed, deliberately, for the second round running.
- **Kept on a neutral held-out number** (the round 6 / 7 / 8 precedent): the
  one-level negative-double twin (+2 held out, all PASS->bid), the competitive
  raise seam (+1 held out, 8 boards up to 3 down), and the six-card-major slam
  invitation over the 18-19 2NT rebid (0 boards changed held out, +21 in sample,
  2 up and 0 down).

### Two authoring lessons paid for in this round

- **A second rule defining a call steals the PRIMARY READING from the first.**
  The six-card-major slam invitation was first written as its own rung at
  priority 56.5.  It worked, and it also made a 4-3-3-3 fourteen-count's
  quantitative 4NT report as *"31+ combined with a six-card spade suit"* - a
  locked scenario caught it.  Folded into the existing quantitative rule as an
  `any_of` branch instead: one rule, one reading, no priority contest.  But
  folding it in at the same priority silently lost the fix, because the rule tied
  with the 4M game jump and **on a tie the lower call wins** - so the invitation
  could never be reached by any hand that also fitted the game bid, which is
  every hand the branch exists for.  Priority 56.5 on the merged rule, and the
  reason is now a comment.
- **`.` matches newlines under `re.S`.**  A scripted extraction of one rule block
  used `re.S` and silently swallowed the rest of the file into a sandbox; the
  loader's duplicate-context-id guard caught it instantly.  Scripted edits now
  assert the SIZE of what they extracted, not only that they applied.

### Where the round leaves the engine

Held-out **-576 (-0.576 IMPs/board)**, tests 693 -> 708, lints and fuzz unchanged.
The largest identified pockets that remain are unchanged in character: grand
slams the system cannot bid (one reviewer quantified them at **-50 IMPs on this
corpus alone**, 5% of the whole margin), the keycard ask over a standing game,
and the `weakest_their_stopper` / `suit_length(their)` pair of evaluators that
are both known to misread and both measured negative when repaired naively.

### Round 9 follow-up: a twice-bid suit in a game force is agreed

Read from one board rather than a triage cluster (852, -15 on the review
corpus).  After `1H - (P) - 2D - (3S) - P - (P) - 4D - (P)` North held
`A74.AT972.74.A75` and rebid **4H on a five-card suit opposite a partner with a
heart VOID** - doubled, down four, -500, while the other table played 3NT for
+660.  It looked like a judgment error and was a starved seat: the ranking was
4H at fit **0.279**, 5D at **0.00** and 4NT at 0.00, with pass filtered by the
game force.  One non-zero candidate, so the soft-miss lottery took it.

Three chained defects, and the first is the real one:

- **The diamond suit was never "agreed".**  South had bid diamonds twice, the
  second time at the four level in a game force, and any partnership plays that
  as trumps - but the rule that interpreted the 4D was the generic
  `balhigh_rebid_D4`, which sets no `agreed_suit`.  `gf_landing_minor` is gated
  `when: { agreed_suit: $m, game_forced: true }`, so the entire landing family -
  the machinery written for exactly this position, "with a minor agreed in a GF:
  nine tricks beat eleven" - never went live.  Its `gf_game_5$m` rung
  (`total_points: [0, 17]`) fits this hand at 1.00 and bids the 5D that was
  wanted.
- **`uc_minor_game_5D` is written for a different auction.**  Its gate is
  `total_points: [17, 40]` and its text reads "accepting to game in the raised
  minor: 17+ opposite the raise".  In a GAME FORCE there is nothing to accept -
  the pair is already committed - so demanding 17 points to bid a game you are
  obliged to reach is a range with no rule.  This turned out **not** to need its
  own repair: `game_forced` is a context-level condition and not available on a
  rule, and the GF-reachable rung already exists inside the landing context.
  Fixing the agreement fixes this by routing.
- **`uc_rebid_H4` fires on a five-card suit** (it asks for six) and checks
  nothing about partner's length in it.  It only bit because the first two left
  the seat empty.

**The fix: `establishes: { agreed_suit: $X }` on the 24 generic own-suit rebid
rungs at the FOUR and FIVE level**, and at those levels only - at the two and
three level a rebid is competitive noise, but at the four level you are choosing
the contract.  One sentence of bridge, and it is what any partnership assumes.

### The sibling floor that fix exposed, and why measuring in two steps mattered

Applied alone the fix measured **+18 held out and -6 on the review corpus** -
the two corpora disagreeing in sign, which is the signature of a change that is
noise on net.  Reading the losing boards showed they were not variance: setting
`agreed_suit` **re-routes the auction out of `general_slam_try` and into
`rkc_ask`**, and the two contexts state the same convention with different
floors:

| | total_points | reached when |
|---|---|---|
| `gst_rkc_$X` | **15+** | no suit formally agreed |
| `rkc_4NT` | **17+** | a suit IS agreed |

So **agreeing a suit made the keycard ask harder.**  A 15-count with a nine-card
club fit asked keycards right up until partner's rebid set trumps, and then
signed off in five of a minor: board 901's cold 6C became 5C, board 58's 6C
became 5C.  That is the recurring species - one convention, two floors, and
which one applies decided by nothing but which context claimed the auction.

Reconciled to 15 (the sibling that several measured rounds have run on, and
which DECISIONS records as one of the most profitable families in the engine):

| | held-out | review corpus |
|---|---|---|
| the agreement fix alone | +18 | **-6** |
| **plus the reconciled RKC floor** | **+18** | **+8** |

Both corpora agree in sign once the pre-existing inconsistency is repaired.  The
motivating board goes -15 -> -2, board 409 (the same disease, `2C - 2D - 3D -
3S - 4D - 4H`) -13 -> 0, and board 901's slam is preserved.

**The lesson worth keeping is about the method, not the bridge.**  The first
measurement was a -6 that would ordinarily have been reverted as noise.  Reading
*why* the losing boards lost - rather than accepting the number - found a defect
that had nothing to do with the change being tested, was worth +14 on its own,
and had been sitting in the file across every round that measured the keycard
families.  A fix that measures flat is sometimes a fix standing on top of a
second bug.

## Round 10: the triage method is replaced by a per-DECISION audit

The expert-triage loop had stopped working, and the project's own numbers say so.
`tools/triage_match.py` clusters losing boards by **the rule that made our last
bid**, an attribution this file has called correlational since round 3.  Across
rounds 5-9 it kept nominating the same generic terminal rules - `uc_nt3` topped
the list five rounds running, `all-pass` is a quarter of the corpus - and every
one of them was re-scored across all 2000 tables and ruled NOT a defect.  Expert
budget went on proving big clusters innocent.  Round 9's triage-driven batch
measured **-19 held out** and survived only because it was decomposed fix by fix.

Meanwhile the two most valuable findings of the last two rounds came from reading
ONE board at ONE decision (boards 231 and 852).  The signal was never the cluster;
it was the decision.

### The replacement: `tools/ben_audit.py`

For every call we made on every board we LOST, BEN is asked what it would call
**from the same seat, holding the same thirteen cards, after the identical
auction**.  One decision, two bidders, everything else held fixed.  Two things
make it sharper than a disagreement count:

- **Weighted by the IMPs on the board**, not merely counted.
- **First divergence.**  After our call differs from BEN's, every later decision
  in that auction is conditioned on our own earlier choice and BEN's later
  opinions answer a different question.  The FIRST confident disagreement is the
  causally meaningful one; the rest are downstream, and are ranked separately.

On seed 171717: 318 losing boards, **3,296 of our decisions replayed, 807
disagreements, 392 with BEN >= 0.80 confident, 264 of those the first divergence
in their auction** - and the resulting ranking has almost nothing in common with
what triage produced.  The top families were `open_pass` (15 decisions, -87 IMPs),
`cl_pass`, `r1m_1H`, `oc1C_pass`, `sw_pass`: all of them *specific decisions with
a named alternative*, none of them reachable by last-rule clustering, because a
pass that leads to a bad board is labelled "all-pass" and dismissed as the
defensive long tail.

Denominators still matter and still killed hypotheses: `sw_pass` fires on 216
tables at a mean of **-0.52** against a corpus baseline of -0.811, and `r1m_1H`
on 80 tables at **-0.03**.  Both families are healthy - the defects were specific
missing rungs inside them, not the rules.

### What it found, all four verified through `choose_bid`

- **Third seat has no light MINOR opening.**  `open_1S_rule20_third` and
  `open_1H_rule20_third` exist; the minors never got the twin, so eleven points
  with five clubs and two quick tricks passed out where BEN opens 1C at
  confidence **1.00**.  The `sibling` lint cannot see it because the two rules
  differ in other gates.  (Reviewer A diagnosed this in round 8 from one board
  and did not propose it; a second corpus has now confirmed it.)
- **Higher of equal length was never carried from the openings to the
  responses.**  Five-five and six-six in the majors both answered 1H.  Both
  `r1m_1H` and `r1m_1S` were soft-missing their `suit_diff` gate by exactly one
  card - **0.8 apiece** - and 1H won on priority alone, 76 to 75.  Worth
  recording precisely: **reviewer A proposed this exact repair in round 7,
  DECISIONS records it as VERIFIED, and it was never implemented.**  No scenario
  was locked, so nothing caught it, and the corpus has re-found it twice since.
  Priority only separates candidates that both fit >= 0.9, so the fix has to make
  the equal-length case *fit*, not merely outrank; it is now a branch of
  `r1m_1S` at priority 77 (one rule, one reading).
- **The weak jump overcall is capped at SEVEN cards and was the top of the
  ladder.**  `oc1$o_2$X_jump` reads `suits: [6, 7]`, and there was no rung above
  it, so an eight- or nine-card suit had no overcall at all: one hand held
  KT9876542 of hearts over 1C and passed it out.  Preemptive overcalls added at
  the three level (7+) and four level (8+), gates mirrored from the opening
  preempts.
- **The sandwich seat stops at the two level.**  Good 5+ cards and 11-17, and
  nothing else - so a seven-card suit on a weak hand had nothing to bid.  The
  preemptive jump is the sandwich seat's most useful call and it was the one call
  the context did not have.

A fifth candidate was **rejected**: `r1m_1H` answering 1H on a 6-diamond 4-heart
five-count where BEN bids 1D at 1.00.  That is Walsh, which this system plays by
documented choice - bypassing diamonds with a weak hand and a four-card major is
the agreement, not a bug.  Similarly `sw_pass` on a hand where BEN bids 2S over
their 1S is a CUE bid; Michaels and the unusual notrump are scope-excluded.

### One authoring trap, twice

`cheapest_in_suit: true` was copied onto the new preempt rungs from their
neighbours, and **a preempt is a jump by definition** - the gate excluded every
one of them, so the first version of both fixes changed nothing on their own
motivating boards.  The traces caught it immediately.  This is the third round in
a row where a scripted edit applied cleanly and did nothing useful, and the third
time tracing the board rather than trusting the edit is what found it.

### Measured, and the ratio is the point

| | in sample | held out |
|---|---|---|
| round 8 (triage) | +183 | +9 |
| round 9 (triage) | +164 | +36 |
| **round 10 (per-decision audit)** | **+22** | **+23** |

Held-out **-558 -> -535 (+23 paired; 4 up, 3 down)**, review corpus **-811 ->
-789 (+22 paired; 8 up, 4 down)**.  Like-for-like since head-to-head play began:
**-1.474 -> -0.535 IMPs/board.**

The in-sample number is small and that is the finding.  Triage produced gains of
5x to 20x its held-out value, which is the signature of fixes fitted to the
corpus that found them.  This round's in-sample and held-out gains are **the same
size**, because a decision where an expert bidder confidently disagrees with us,
holding our cards in our auction, is a defect wherever it occurs - not a property
of the boards it was found on.

## Round 11 (seed 242424): a round that mostly produced negative results

Fresh 1000 deals, seed 242424: **-804 IMPs (-0.804/board)**, 219 boards won, 331
lost, 450 flat, swings >= 10 IMPs 44 ours to 88 theirs.  Per-decision audit:
**3,427 of our decisions replayed, 856 disagreements, 418 with BEN >= 0.80
confident, 278 of them a first divergence.**

Three candidates were found, verified through `choose_bid`, implemented and
measured.  Two were reverted on the held-out corpus and the third is worth ~1
IMP.  The round's value is the two negative results, both of which correct a
belief this project was operating on.

### The headline negative: a rule that "never fires" is not necessarily unreachable

`open_pass` topped the ranking again (-169 IMPs over 28 first-divergences), but
its hands are rule-of-20 threshold cases, which DECISIONS scopes out.  Below it
sat what looked like a clean structural bug: **the weak jump overcall is
unreachable by construction.**  `oc1$o_2$X_jump` states gates strictly NARROWER
than the simple overcall beside it - exactly 6-7 cards against 5+, 5-10 HCP
against 8-16, plus a good-suit requirement - and sat at priority 59-60 against
that rule's 71.  Whenever a one-level overcall was legal, which is most of the
time, both fitted 1.00 and the LESS descriptive call won on priority alone.
Across 2000 tables the twelve rules fired **eight times between them**, and
`oc1C_2S_jump` never fired at all.  Four boards in the audit had us overcall 1S
on a six-card suit where BEN jumps, at 0.92-0.97 confidence.

Re-ranked so the jump wins where its own gates are met: **-24 IMPs held out.**
REVERTED.

The diagnosis was right and the inference from it was wrong, and the correction
is worth stating because it will come up again.  The jump was **already reachable
for the hands it is for**: with 5-7 HCP the simple overcall (8-16) does not fit
>= 0.9, so the jump was the only candidate and did fire.  The only thing the
re-ranking changed was the **8-10 HCP overlap** - and on that population the
corpus says the one-level overcall is the better call.  Eight firings in 2000
tables is not evidence of dead code; it is evidence that 5-7 HCP with a good
six-card suit is a rare hand.  **Before concluding a rule is unreachable, check
whether the hands it describes are simply uncommon.**

### The second negative: the gate was broken and freeing it does not pay

`cl_raise_lott3_$M` - "preemptive raise to the LOTT level: 4 trumps, weak" -
carries `cheapest_in_suit: true`, and **a preemptive raise TO THE LEVEL OF THE
FIT is a jump by definition**, so the rung was unreachable whenever the cheap
raise was legal.  This is exactly the trap round 10 found on the sandwich
preempts, where removing the same gate measured +23.  Two audit boards convict
it precisely: six spades opposite a 1S overcall is eleven trumps and the Law
says 4S (BEN, 0.95) - we passed; a yarborough with four trumps opposite a 1H
overcall is nine trumps and the Law says 3H (BEN, 0.81) - we passed.

Freed, extended to a four-level rung for eleven trumps, and with the obstruction
floor lowered from 3 to 0 (obstruction is FOR weak hands), both boards match BEN
exactly and the review corpus gains **+19**.  Held out it measures **-3**, twice.
REVERTED.

The changed boards are unsystematic (-5, -3, +1, +1, +3) - noise, not a
disaster - so the honest reading is that the *gate* is genuinely broken and the
*rung behind it* does not pay against this opponent.  Unblocking it is not the
fix; the rung's content needs rethinking.  Recorded as an open item rather than
a repair, because leaving a known-unreachable rule in place is a real if minor
debt.

### What shipped

**The sandwich seat has no weak jump overcall.**  The direct seat has one (6
cards, 5-10, good suit); the sandwich seat's two-level rung is the STRONG 11-17
overcall, so a seven-count with six good spades had nothing between a one-level
bid it did not qualify for and a pass - and passed, where BEN bids 2S at
confidence 0.99.  A sibling gap, additive, and the `cheapest_in_suit: false`
condition is what makes it a jump (in this seat the opponents have bid two
suits, so a two-level call is only sometimes one).

Measured: held out **-535 -> -535 (0 IMPs, one board changed)**, review corpus
**-804 -> -803 (+1)**.  Kept on structure at zero measured cost, the same call
as round 7's weak-two overcalls and round 8's three neutral keeps.

### Method note: the audit's ranking is only as good as the verification

The per-decision audit did its job - all three candidates reproduced exactly,
and the two that failed did so on the held-out corpus rather than in testing.
But this round is the counterweight to round 10's result: a confident BEN
disagreement is a **lead**, and two of the three leads here were either a style
difference the corpus does not reward (the weak jump overlap) or a real defect
whose repair does not pay (the LOTT rung).  Round 10's 1:1 in-sample to held-out
ratio was not a promise that every audit finding generalises; it was one round's
result.  The discipline that mattered here was decomposition: the bundle
measured **-28** held out, and decomposing it (-24, -3, +0) is the only reason
the round shipped anything at all rather than reverting a mixed batch wholesale.

## Round 12 (seed 242424 re-review): the engine could not say "competitive"

Not a new corpus.  The owner's diagnosis reframed the problem and the round
tested it: *every board where we lose IMPs may be a **categorization** problem
- if East on board 862 had categorized the auction as competitive, then 4S
follows immediately from the Law.  The missing thing is not a rule, it is a
name for what kind of auction this is.*

The measurement that motivated it: of the 278 decisions in the round-11 audit
where BEN confidently disagreed with our first divergence, **BEN's call already
existed as a candidate in 255 (92%)**, at fit >= 0.9 in 105, and **half were
settled by `priority`** - a static number that sees neither the hand nor the
auction.  The engine usually has the right rule and picks a different one.

But they do **not** cluster: 278 decisions spread over **223 distinct rule
pairs**, 186 of them singletons.  The largest apparent pattern (17 decisions,
-89 IMPs: the catch-all pass beating an available opening at fit 0.70-0.89)
dies on the denominator - 138 tables corpus-wide at mean **-0.70 against a
corpus mean of -0.80**, i.e. above baseline.  Per-pair patching has no
denominator; a category does.

### The gap, and closing it

`Auction.is_competitive` ("both sides have made a non-pass call") existed and
was read by exactly one thing: the code fallback.  Worse, the inference engine
has always maintained a **full descriptor for each opponent** - from East's
seat on 862 it knows South is 10-21 with 3+ clubs and North 10+ with 5+ hearts
- and every bit of it was dropped at the `EvalContext` boundary.  The system
could say "partner has values"; it had no way to say "they have values".

Additive, neutral defaults: `EvalContext` gains `is_competitive`,
`their_shown_count`, `their_min_hcp`, `their_min_length`, `their_max_fit`
(from `analysis.descriptors[lho|rho]`), plus `partner_max_hcp` and
`partner_min_length` reached through new evaluators.  Evaluators
`their_shown_hcp`, `their_fit`, `their_bidders`, `partner_shown_length`,
`partner_shown_max`.  Rule-level `when` keys `is_competitive` and
`partner_limited`; context-level `when: is_competitive` and `also_patterns`.

### The seed category, and the correction the measurement forced

`cl_raise_$X4` - the only four-level competitive raise - is gated on
`rule_of_26 >= 25`, a **combined-values** test.  That is the right question in
a constructive auction and the wrong one in a competitive one.  Board 862's
East, eleven trumps and 14 total points, made 24, fitted 0.80, and lost to the
catch-all pass at 1.00.

Gated on our own ten trumps alone the new Law rung measured **+1 over 1000
boards**: one good save (+11) against four boards pushed from a making 3H to a
failing 4H.  Ten trumps *our way* is not the Law.  Adding `their_fit >= 8` -
the Law is about TOTAL trumps, so bidding one more is only right when **both**
sides have a fit - kept both wins and removed all four losses: **+12**.  Board
862 itself now correctly passes, because 4S doubled goes for 800 against their
making 4H; the gate defers the category one round, to the moment they raise.

### What shipped

| experiment | paired | held out |
|---|---|---|
| `cl_raise_lott4_$M`, `their_fit >= 8` | -804 -> -792 (+12) | -535 (0 boards) |
| the same rung in the four other contexts (reviewer A) | -792 -> -780 (+12) | -535 (0 boards) |
| reviewer B items 1-3 | -780 -> -744 (+36) | -535 -> **-532** (+3) |
| **round total** | **-804 -> -744 (+60)** | **-535 -> -532 (+3)** |

1. **The Law at the four level is a category, not a context.**  The seed rung
   lived only in `general_competitive_low`; the same position one call later,
   or from the balancing seat, lands elsewhere and meets the combined-values
   ladder again.  Reviewer A measured the slice (contested, ten disclosed
   trumps in partner's major, four-level raise legal, we passed) at **16 tables
   / -93 IMPs / mean -5.81**, and with `their_fit >= 8` at **10 tables / -7.80**
   - none of them in `general_competitive_low`.  Eight rungs added to
   `general_competitive_high`, `general_balancing_high`, `general_balancing_low`
   and `general_uncontested_continuation`, gates copied verbatim so the category
   reads the same everywhere, `is_competitive: true` keeping the `uc_` copy out
   of an uncontested auction.  **The minors measured -0.90, i.e. baseline - the
   rung was deliberately not extended there.**
2. **Seven cards is the suit quality.**  `<=10 HCP with a seven-card suit` is
   the worst-behaved sub-population in the whole opening decision: **8 tables at
   mean -6.00** against a corpus mean of -0.80, invisible inside `open_pass`'s
   769 firings.  The suit-quality floor on the eight three-level preempts drops
   (nv 1 -> 0, vul 1.5 -> 1).  The HCP bands are untouched, so partner's shown
   minimum does not move; the exactly-six weak-two population measured **-0.69,
   better than baseline**, and was left alone.
3. **The ask has been answered.**  Partner opened a weak two and has therefore
   promised six trumps, so my doubleton is the eighth.  `w2ac_game_$W` asked how
   long MY suit was and a 17-count signed off in three.  New rung
   `w2ac_game8_$W` at priority 54.5 - under `w2ac_3NT_$W` so nine tricks still
   beat eleven in a minor, over the sign-off.  A gate given to one rule and not
   its siblings, for the fourth round running.
4. **The limit bid beats the second suit.**  `ob_1D1S_2C` (57) and `ob_1NT` (55)
   both fit 1.00 on a semi-balanced 12-14 with 4-4 minors, and the undescriptive
   call won on priority alone.  Reviewer B proposed a new rung at 57.5;
   its `requires` are character-for-character `ob_1NT`'s, so it is a re-rank in
   additive clothing that splits one call into two readings and drops a denial
   from the explanation.  Shipped as the one-line equivalent instead:
   **`ob_1NT` priority 55 -> 57.5**.  Same six tables change, one reading.

### The reverted experiment, and it is the round's most important result

Reviewer B's headline was the largest measured population in either review, and
the diagnosis is **correct**: `general_uncontested_continuation`, described in
the file as *"General constructive agreements in an uncontested auction"*, has
`pattern: "... - P - ?"` - which means *"RHO passed"*, not *"the auction is
uncontested"*.  One call changes the toolkit:

```
1H (1S) 2H     - ?  ->  general_competitive_low
1H (1S) 2H (P) - ?  ->  general_uncontested_continuation
```

Whole corpus: a `uc_*` rule decides a **competitive** auction on **465 tables at
mean -1.14** (CI [-1.57,-0.72], excluding the -0.804 corpus mean); on a
genuinely uncontested auction, 126 tables at **-0.67**, better than baseline.
`uc_pass` is 86% competitive.  Excess loss on the misapplied slice ~ **-156**.

Routing them - `also_patterns: ["... - bid - P - ?"]` on both competitive
contexts plus `when: { is_competitive: true }` - measured **-59 paired and -106
held out**, changed 231 boards, and broke **five locked regression scenarios**:
the doubler's raise of a three-level advance, the refusal to bid game opposite a
preemptive raise, a takeout double with their second suit.  A context that
DEFINES a call takes over interpreting it, so every behaviour authored in the
uncontested continuation silently disappeared.  Fourth scalp for the shadowing
trap and the most expensive one.

**A correct categorization diagnosis does not license a toolkit swap.**  The
repair is to port individual rungs under `when: { is_competitive: true }` - what
`uc_raise_lott4_$M` does, at +12 - not to re-route the context.  The engine
capability (`also_patterns`, context-level `is_competitive`) is kept; its use
here is recorded in the file as measured-negative.

### Method notes

- **First-divergence ranking is blind to defects that only occur late.**
  `uc_pass` - the catch-all of the largest misapplied population in the engine -
  appears in the confident first-divergence list **once**, at -1 IMP.  A
  downstream pass is almost never the first divergence.  Both reviewers found
  their largest categories by whole-corpus scan, not from the audit rows.
- **A category is only worth its denominator.**  Two of the three shipped
  categories reach fewer than ten tables per 2000.  The round's +60 paired is
  real and its +3 held out is honest: these are correct bridge, narrowly
  reached.  What generalises is the vocabulary, not the rungs.
- `prepare_decision`'s `_SETUP_CACHE` is keyed on `id(system)`; loading a
  baseline and a prototype in one process can collide after a GC and produce
  false diffs.  Prototype in separate processes.

## Round 13 (seed 131313): one board at a time, one verdict per decision

A different loop, asked for directly: generate deals, play BEN, and on **every
board we lose**, sit in each of our seats in turn and give the call exactly one
verdict — **OK** / **CATEGORY** (the situation was filed as the wrong kind of
auction) / **EXCEPTION** (the rule is right in general, wrong here) /
**RULE-WRONG** (wrong wherever it fires).  Accumulate twenty suggested fixes,
then hand them to an adversarial expert, apply what survives, measure.

`tools/board_critique.py` is the instrument.  `ben_audit.py` ranks leads across
a corpus; this does the opposite — one board, every call we made, its candidate
set with fits and priorities, the live contexts, what the engine believed about
partner *and* about the opponents, and BEN's call from the same seat.

100 deals, seed 131313: **-25 IMPs**, 25 boards lost.  **397 of our decisions
examined; BEN agreed with 290.**  Of the 107 disagreements **87 were ruled OK** —
style, a scope-excluded threshold, a rule correct in its own seat, or a
consequence of an earlier error.  Twenty fixes: 8 CATEGORY, 3 EXCEPTION,
9 RULE-WRONG.

### The critique killed eleven of the twenty, and six of the kills are on me

**Six findings misquoted the rule they indicted.**  Three kills rest on that
alone:

- **FIX 3** claimed `ob_raise_4$M` has "no upper bound".  It is
  `total_points: [19, 24]`, capped, with the reason in a comment.  I read the
  `shows` text ("19+ support points") and did not open the constraint.
- **FIX 10** claimed `uc_nt3` says "nothing about partner at all".  It carries
  `rule_of_26: [24, 99]`, and `rule_of_26` uses partner's midpoint, so it
  already reads the ceiling.  The real failure on that board is a 0.5-point soft
  miss scoring 0.946; sharpening it reaches 3 tables / -2 IMPs.
- **FIX 15 and FIX 18** named the PRIMARY READING rather than the rule that
  matched.  Board 86 was decided by `cl_new_long2_S_hi` (floor **8**, six-card
  suit), not `cl_new_S2` (floor 10, fit 0.31); board 67's seat is governed by
  `ballow_reopen_X`, which exists and correctly declines with four of their suit.

ROUND_METHOD has warned about the primary-reading trap since round 8 and I walked
into it three times in one round.  **Re-rank every indictment through
`score_candidates` before writing it down** is now a step, not advice.

The other five kills are data, not misreading:

- **FIX 5** (a floor on `cl_new_$X2` when our side has never bid): the named
  category — we are silent, they have had a constructive auction — is **21
  tables at mean -0.19 / par gap +2.43**, above baseline, and the point floor is
  *anti*-correlated: the 10-11 band scores -0.70 and the 12+ band -1.80.
- **FIX 13** (loosen `their_fit >= 8` when they have jumped to game) **does not
  flip its own board** — `ch_raise_lott4_S` scores 0.011 there and fails the
  sharp `lott >= 10` gate too — and the slice it would add is 8 tables at mean
  -0.75 against a corpus mean of -0.80.  The restored coin flip, exactly.
- **FIX 17** (overcall suit-quality siblings): the sandwich ladder is uniformly
  +0.5 quality at both levels **by design**; the blocked population is 11 tables
  at par gap +1.00.
- **FIX 2**, **FIX 8**, **FIX 12**, **FIX 20**: each dies on its own
  denominator.

Two measurement notes from the critique worth as much as the fixes:
**`par_gap` in the match rows is N/S-signed at BOTH tables** — read at face value
it inverts the verdict on three of these families; ours is `+a_par_gap` and
`-b_par_gap`, baseline **-0.378**.  And **`is_unbid_suit` has no sharp
tolerance**: the first rule to use it leaks two wrong doubles, because a suit
that IS bid still scores 0.8 against a `[1,1]` gate.

### What shipped

| bundle | own deals (131313) | review (242424) | held out (828282) |
|---|---|---|---|
| A — three `shows` repairs | 0 decisions change | 0 | 0 |
| B — three starved seats | 0 decisions change | 0 | 0 |
| C — two starved seats | | -744 -> -738 (+6) | -532 -> -525 (+7) |
| FIX 6 alone — the sandwich double | | -738 -> **-729** (+9) | -525 (0 boards) |
| **round total** | **-25 -> +8 (+33)** | **-744 -> -729 (+15)** | **-532 -> -525 (+7)** |

**Bundle A — 46 sentences that did not state the gate that decides them.**
44 raise rungs carry `rule_of_26` and not one disclosed it; ten four-level rungs
said "13+ support points" while requiring 11; `cl_raise_C3/D3` said "10+" while
requiring 8; `ballow_nt2_strong` claimed "partner still unlimited" with no
condition on partner; `ballow_X` and `balhigh_X` said "values are marked
opposite a passing partner" while silently demanding shortness in their suit.
Each sentence is now **regenerated from the rule's own numbers**, so it cannot
drift again.  Replay: **0 of 10,346 decisions change** (`shows` is read only by
`explain.py`).  This is the round's largest edit and it is worth shipping on the
user's standing rule that explainability outranks score — and because three of
this round's own findings were caused by trusting these sentences.

**Bundle B — three seats that did not exist.**  (a) The 1430 **5C reply shows
one OR four keycards**, so a sign-off at five of the agreed suit is the asker
assuming one; with four, only the answerer knows — and that seat matched **no
context at all**.  (b) `ob_1m1S_2H_reverse` is expanded over both minors and only
the 1C twin ever got an answering context, so responder **passed a forcing
reverse**: `pass_forbidden` was set, nothing fit above the 0.30 forced-bid floor,
and the catch-all took it at 1.00.  (c) The advance of a takeout double said
"pulling to the cheapest 4+ suit" and implemented *longest*, bidding a minor at
the three level over a major at the two.  All three reach **0 of 2,000 tables**;
shipped on structure at zero measured cost, the round 7 / 8 / 11 precedent.

**Bundle C — two invitations nobody could decline.**  (a) `adv1n_2NT_$o` invites
opposite a 15-18 overcall and had no answering context, so `uc_nt3` (13-19
balanced) accepted it — four firings in 2,000, **four acceptances**, -12 IMPs.
The new context declines on a minimum 15 and accepts from 16, which is this
file's own sibling threshold; a 17 threshold would have flipped one more review
board and deleted the family's only winner, and choosing it for that reason is
fitting the corpus, not stating an agreement.  (b) **Eleven with a six-card major
opposite a 12-14 rebid fitted nothing** — pass, 2M and the game-forcing 3M all
soft-miss by one and the lottery hands it to the *game force*.  There is nowhere
to invite (3M is the force, 2NT explicitly denies six), so the sign-off's
ceiling goes 10 -> 11.  A ceiling, not a floor: partner's shown minimum does not
move.

**FIX 6, measured alone — the sandwich seat is not the direct seat.**  `sw_X`
demanded shortness in *opener's* suit, which is the direct-seat requirement in a
seat where **both** opponents have named a suit.  A double there is takeout of
both, and what it promises is length in the two unbid suits.  New evaluator
`weakest_unbid_length` (sharp), added as a second `any_of` branch at the same
12-point floor.  With three suits still unbid — they responded 1NT — the branch
is unsatisfiable, which is right: that is a one-suited auction.  Three tables in
2,000, all currently losing; +9 review, held-out untouched.

### The species this round found, with counts

1. **A force, an ask or an invitation authored without the seat that answers
   it** — four instances in one hundred deals (the RKC 1-or-4 answerer, the 1D
   reverse, the 2NT invite over a 1NT overcall, and the forcing new suit over a
   weak two the critique found while killing FIX 8).  This is now the most
   common defect species in the file, ahead of "range with no rule".
2. **A rule whose `shows` sentence does not state the gate that decides it** —
   46 of them, and they cost this round three false findings.

## Round 14 (seed 151515): the round's biggest win came from a broken test

Same loop as round 13, run on 200 deals instead of 100: play BEN, sit in every
seat on every board we lose, give each call exactly one verdict, accumulate
twenty fixes, hand them to one adversarial expert, apply survivors in asserted
sub-batches, keep or revert on the held-out corpus.

200 deals, seed 151515: **-179 IMPs**, 71 boards lost.  Twenty findings written
up in `reports/r14_findings.md`; three more were killed in my own draft on
arithmetic or denominator grounds before they were written down, and the large
majority of BEN's disagreements were again ruled **OK**.

The critique (`docs/EXPERT_CRITIQUE_151515.md`) returned **7 SHIP, 5 RESHAPE,
8 KILL**.

### Measured

| step | own deals (151515) | review (242424) | held out (828282) |
|---|---|---|---|
| baseline | -179 | -729 | -525 |
| Bundle A — four rungs that reach nothing | 0 decisions change | 0 | 0 |
| Bundle B — six repairs, all attributable | -125 (+54) | -699 (+30) | -502 (+23) |
| FIX 2 alone — raising partner's notrump | | -674 (+25) | -500 (+2) |
| FIX 2 re-ranked 28.5 -> 26.5 | | -677 (-3) | **-474 (+26)** |
| FIX 8 — gating the negative double | | -672 (+2) | -505 (**-5**) reverted |
| FIX 18 — the strong balanced overcall | | -672 (+2) | -501 (**-1**) reverted |
| **round total** | **-179 -> -114 (+65)** | **-729 -> -677 (+52)** | **-525 -> -474 (+51)** |

### The lesson: a locked scenario is a measurement, and it was worth +26

FIX 2 added `uc_nt_raise3` — nothing in the generic toolkit *raised* partner's
notrump, so thirteen points opposite a shown 18-19 passed at fit 1.00.  Both the
reviewer and I put it at priority **28.5**, reasoning only about the rung
directly above it: "under `uc_nt3`, so the natural reading stays primary."
Neither of us looked *below*.  The natural three-level suit rungs live at 27.0
and 27.5, so the new raise outranked every one of them and the full test suite
broke a **round-9 locked scenario**: 5-5 in the majors opposite partner's 2NT
raised to game instead of bidding three spades.

The bridge is not subtle once stated: *a raise is what you bid when there is
nothing left to describe.*  Re-ranked to **26.5**, directly above `uc_pass`
among the calls that are legal over a standing 2NT.  Whole-corpus blast radius
**2 decisions**, both plainly right — a 5-4 major hand with a stiff diamond now
bids 3S instead of 3NT, and a six-card diamond suit rebids 3D — and the held-out
corpus moved **+26 on five boards, five up and none down**.  That single
re-ranking is the largest held-out gain of the round, and it exists only because
`pytest` was run before the numbers were believed.

**The rule this adds to the method: a new rung must be priced against the rungs
BELOW it, not only the one above.**  A rung placed too high subtracts every
more descriptive call it outranks, which is the "adds a gate" hazard wearing a
different hat.  It is now in ROUND_METHOD's guardrails.

### What shipped

**Bundle A — four rungs that reach nothing (0 of 10,346 decisions).**
Shipped on structure at zero measured cost, the round 7 / 8 / 11 / 13 precedent.
(a) `1NT - 2C - 2D` had a ladder of 2NT/8-9, 3NT/10-17, 6NT/18+, so **16-17
opposite a 15-17 notrump — 31-34 combined, the textbook quantitative zone — had
only the game bid**; `stm_2D_4NT` invites and the new context
`stayman_quant_opener_decides` is the seat that answers it (constraint 3, still
the file's commonest defect).  (b) `rjrb_3M` re-ranked 54 -> 55.5: its two
siblings both *deny* a six-card major in that context and `rjrb_3NT` never got
the denial, so six of a major fitted both at 1.00 and the less descriptive call
won on a static number.  (c) the 2C positive demanded two of the top three,
which is five-card calibration — **six cards headed by one honour is a
positive**.  (d) `opener_over_bail`: `1NT - P - 3$m` had no answering seat.

**Bundle B — six repairs, every changed call scorable on its own board.**
(a) `nt_after_super_accept` — the super-accept of a transfer is a force to at
least three of the major and **the responder's seat did not exist**, so a bust
and a game hand were both passed by the catch-all.  (b) A four-level major over
their preempt on seven cards, or eight, or thirteen points with a quality suit:
the ladder stopped at the three level.  (c) The negative doubler's answering
rungs demanded **12** while the double itself promises 11 — a gate given to one
sibling and not the other, swept across `adx_neg_major_*` and
`ch_neg_major_*`.  (d) `r2c_place_4H` / `r2c_place_4S` placed the contract in
the major *opener* named without checking which major that was; `standing_bid_strain`
now says so.  (e) A **void** cannot be shown after a transfer, so 3NT won the
choice of games holding one; `tr_3NT_choice` now evaluates `void(any)` and
`tr_game_void_$M` is the floor rung beneath it.  (f) From the critique's own
residue, worth more than the fix that exposed it: **`cl_new_H1` bid a four-card
heart suit ahead of a six-card spade suit**, because both rungs sit at priority
30 and the tie broke on call rank.  Round 10 fixed exactly this for
`r1m_1H`/`r1m_1S` and it was never swept into `general_competitive_low`.
`suit_diff(H,S)` closes it; 4-4 still goes up the line.

**FIX 2, measured alone and then re-ranked** — above.

### Reverted on the held-out number

- **FIX 8** (`nxj_X`, the negative double of a jump overcall, is `hcp: [8, 40]`
  and **nothing else** at priority 70, above everything in its context, with a
  `shows` sentence claiming "support for unbid suits").  The diagnosis is right
  and the gate does not pay: capping the longest suit at five and demanding a
  four-card unbid major measured **-5 held out** on four changed boards, one up
  and one down.  The reviewer predicted the shape — two of the nine replacement
  calls land below the 0.9 fast path, so the seats behind the deleted double are
  unauthored, exactly the `weakest_their_stopper` revert of round 8.  Reverted
  to the **text-only repair**: the sentence now states the only gate that
  decides the rule.  Author the landing seats first, then re-measure.
- **FIX 18** (a strong balanced 11-14 / 12-14 notrump rung with `i_have_acted`)
  measured **-1 held out** on ten changed boards, four up and four down — a
  restored coin flip on a small population.  The reviewer called it "the weakest
  survivor on the numbers and the strongest on the bridge" and offered no
  fallback.  Reverted on the number; the diagnosis is now an open item.

### Killed by the review, with the number that killed it

| fix | the number |
|---|---|
| **4** takeout double of a weak two tolerates three | the branch is 3-4 tables at board mean **+0.00** against a corpus mean of -0.73, and it turns a `KQT76` five-card overcall into a takeout double |
| **9** drop the one-level suit-quality gate | 3 tables, **our gap +1.67** against -0.34; and removing it makes the engine bid the **shorter** major — round 10's defect re-created |
| **10** a weak two-level rebid rung in seven families | 12 call changes, **7 of them our own raises collapsing to pass**, because partner's shown minimum for a two-level own-suit rebid drops 11 -> 6 across **28 rules** |
| **14** suit-quality floor on the weak jump shift | the rule is **1 table of 2,000, +1 IMP**; the gate reaches 0; and the named twin does not exist |
| **16** four-level new suits in the uncontested toolkit | 15 call changes, **6 displacing `balhigh_pass`** — round 12 measured that routing at -59 paired / -106 held out |
| **17** a solo keycard ask in a game force | **0 of its 12 firings is a 2C auction**, the position it was written for; slice mean +2.08 against -0.73 |
| **19** preemptive overcall of their 1NT | `defense_vs_1NT` is 129 tables at mean -0.33 / gap **+2.91**, above baseline on both metrics |
| **20** open the longer minor with 6-5 | population **1 of 2,000**, currently **+11 IMPs**, and the patch is vetoed by `open_1D`'s own `not:` clause |

### Three measurement facts the critique established

- **`fast_decision`, not `score_candidates`, is the engine's choice.**  Ranking
  by blended score mislabels **25 of 10,346** decisions — every one a rule at fit
  0.946/0.965 beating a fit-1.00 pass on priority.  `repro.rank_at()` returns
  score order; reading its first row as "what we bid" is the primary-reading trap
  with a different mechanism.
- **Board margin and par gap disagree in both directions, and the par gap is the
  attributable one.**  `nxj_X`'s doubles without a major win +3.50 a table and sit
  at par gap -6.33; FIX 18's sandwich firings win +2.43 at par gap +2.57.  Quote
  both, always.  Corrected baselines: review **-0.729**, our par gap **-0.338**.
- **`weakest_their_stopper` still does not gate** and was load-bearing in two of
  this round's proposals.  It is a reason to distrust any new rule that leans on
  it, not merely an open item.

## Round 15 (seed 161616, 1000 deals): the rule-level defect supply is exhausted

1000 deals, seed 161616: **-667 IMPs (-0.667/board)**, 206 won / 322 lost / 472
flat.  Every one of the 322 lost boards was read.  827 BEN disagreements,
grouped by the rule that actually decided the call.  Six fixes to one
adversarial reviewer: **1 SHIP, 1 RESHAPE-as-structure, 4 KILL.**

**Held out: -474 -> -474.  The round moved nothing, and that is the finding.**

| | own deals (161616) | review (242424) | held out (828282) |
|---|---|---|---|
| baseline | -667 | -677 | -474 |
| Bundle A — two rungs, 0 reach on both corpora | 3 boards change | **-677 (0)** | **-474 (0)** |
| the doubler's own suit, measured alone | | -677 (+0) | **-476 (-2)** reverted |
| **round total** | | **-677** | **-474** |

### Two measurement corrections, and both changed verdicts before any fix was written

**(a) `explanation.source_rule_id` is the PRIMARY READING, not the deciding
rule.**  `replay.py`, `repro.fires()` and the match rows' `rule` field all key on
it.  It is the highest-priority rule producing the same call - what the call
*means* - and on board 67a it names `rr_nt_slam3_S` (floor **19 HCP**) for a
**15-count**, because `rr_nt_gf3_S` (12-18) matched at 1.00 and bid the same 3S.
`rr_nt_slam3_S` has never fired in 10,385 decisions.  Three findings were written
against it before the check.  `sweep.deciding_rule()` reconstructs
`fast_decision` and the reviewer verified it independently: **20,731 decisions,
0 call and 0 rule mismatches.**

**(b) A rule must be judged against ITS OWN CONTEXT.**  Par gap is jointly owned
by the whole auction, so a context landing on big-swing boards shows a bad gap
whatever its rules do.  `opener_rebid_1m_1M` runs at -4.04 against a corpus
-0.02, so `ob_rebid_2C` (-4.18) and `ob_1NT` (-4.16) are **at** their own
baseline - a within-context shuffle worth nothing, despite BEN naming 1NT at
confidence **1.00** on five separate boards.  That killed five of my own
candidates, including `gr_rkc_general_S` at delta -0.36, which **revises a
standing open item**: round 8 blamed the keycard ask over a game raise, and
against its own context the ask is not the outlier - the context is.

The reviewer then corrected (b) twice: `rule_context_map()` pools `$`-expansions
under one label, and the rule is inside its own baseline, so the arithmetic is
wrong even where the conclusions survive.  **And used alone the yardstick is
blind to a uniformly bad context, which is where the IMPs are.**  See below.

### The mechanism worth more than the round: an added rung deletes the code fallback

`prepare_decision` builds `covered` from every rule whose `when` holds and whose
call is legal - **fit is never consulted** - and `generate_fallbacks` then only
generates candidates for calls NOT covered.  So **adding a rung removes the code
fallback for that call in every seat its `when` reaches, whether or not the hand
fits the rung.**  Traced on board 691a: a fit-**1.00** fallback 4H replaced by a
rung fitting **0.00**, and the seat handed to a fit-**0.066** keycard ask.

The guardrail "a fix that ADDS a rung fills a hole and is safe" is therefore
false as stated.  It becomes: **a new rung is safe only where no fallback covered
its call, or where the rung fits every hand the fallback caught** - and that has
to be measured, because `when` is auction-only and fit is hand-dependent, so no
`when` can restrict the suppression to the hands the rung wants.

This also explains part of why additive fixes have under-delivered held out
relative to their in-sample blast radius: the radius counts the seats the rung
*wins*, not the seats where it silently removed the fallback.

### What shipped

**Bundle A - two rungs, 0 decisions changed on BOTH measurement corpora.**  Kept
on structure at provably zero cost (the round 7/8/11/13/14 precedent).

- **The advance of a takeout double had no jump.**  `adx_pull_$X3` caps at
  **eleven** total points, so twelve with six spades headed by AKQ took the
  three-level pull as a soft-miss lottery pick at fit **0.409** - the whole
  candidate set was four rules and not one of them fitted - and made twelve
  tricks in 3S.  `adx_pull_S4`/`H4`, deliberately **not** `cheapest_in_suit`
  (over a preempt this IS a jump and the gate excludes jumps), with the family's
  `suit_diff` clauses carried verbatim - without them a locked lint test fails,
  which the lint knew before the corpus did.
- **The balancing 2NT denied no shape** where its one-level sibling `ballow_nt1`
  denies a six-card major, so a bare fifteen with five spades balanced 2NT
  instead of bidding the suit.  Stated as a **range**, not a shape: from
  seventeen the notrump is worth more than the suit because 2S would be a
  non-forcing underbid, so the strong sibling `ballow_nt2_strong` needs no sweep
  and the species is not re-created one rule along.

### Reverted on the held-out number

**The takeout doubler cannot rebid his own suit.**  `uc_new_$X` stops at the
three level and `uc_rebid_$X4` is gated `my_suit: $X`, which a doubler never
satisfies - he has bid no suit - so an eighteen-count with a six-card suit has
four candidates of which exactly one fits, `uc_pass` at 1.00, and passes.  Boards
2a and 485a; **round 14's reviewer named both by number and round 15's named them
again.**  Population 11 tables at board margin -5.45 and par gap -7.64 against a
stage-matched +0.10, replicating on both corpora.

Built with `standing_bid_level: [1, 2, 3]` so that it does not delete the code
fallback for its call (above) - which is also the right bridge, since over
partner's four-level bid a new suit is a cue, not "here is my suit".  Measured
alone: review +0 on two changed boards, **held out -2 on the one board it
reached.**  Reverted.  The diagnosis is right; what the rung lacks is a reason to
prefer four of a six-card suit to defending, opposite an unlimited partner.

### Killed by the review, with the number

| fix | the number that killed it |
|---|---|
| the doubler's notrump rebid | its `when` is `we_bid_last: false` and the standing bid is **ours in 20/20 e10 and 23/23 r15** of the positions it targets: **0 call changes on 2,000 tables**.  Repaired, it still reaches 1 of its own 4 boards - and one of those hands is **22 HCP, not the 20 I printed** |
| cap the reopening double's shape | **0 of the 4 independent firings is 5-5**; the alternative `longest_suit_length: [0,4]` makes 3 changes, all to `balhigh_pass` at fit 1.00, including a table we win +3 |
| the 16+ takeout double | proposes no repair, and its stated partner changes 0 calls; the par-gap split replicates but the **board-margin split inverts** on the independent corpus |
| a strong natural overcall of their 1NT | **the YAML does not load** (`defense_vs_1NT` has no `expand:`); the natural rungs need **five** cards not six, so widening the band **changes 0 calls** - it was a re-rank, not an additive rung |
| deny a five-card major on the balancing 2NT (as written) | the rule **decides nothing in 2,000 independent tables**, and **both HCP counts in my evidence table were wrong** (15 and 15, not 14 and 13 - both hands inside the rule's own band) |

Three of the five kills rest on errors of mine: two miscounted hands, a `when`
that cannot fire, and YAML that does not parse.  Round 13 lost six findings to
misquoted rules and made re-ranking a step; this round the missing step is
**load the file and count the hand before writing the number down.**

### The wall, stated as a number

The six fixes, all shipped in their best form, would change **one call on 2,000
independent tables**.  Rounds 13, 14 and 15 measured -525, -474, -474.  The
per-decision audit finds rule-level defects and the rule-level defects are gone.
Where -667 actually lives, computed on both corpora:

| population | n (of ~10,350) | our par gap | stage baseline |
|---|---|---|---|
| **decided by a code fallback - no rule at all** | **456 (4.4%)** | **-3.89** | +0.46 |
| `general_uncontested_continuation` | 736 | -2.12 | |
| the five responding contexts together | 475 | **-3.0 to -4.6** | |
| `open_2C` | 16 | **-7.44** | deferred four rounds |

The fallback population alone is ≈ **-2,000 attributable gap-points**, larger
than every named family combined, replicating to within 0.3 across corpora, and
nothing has ever ruled on it.  The responding contexts are ≈ -1,700 more, and
**no rule inside them is indictable** because every rung in a uniformly bad
context sits at its own baseline - the blind spot of correction (b), stated as a
number.  The next round should not look for another rule.

## Round 16: the two populations where the engine has no agreement

Round 15 ended at the number it started at, so round 16 stopped looking for
another rule and measured the two places the engine itself reports as having no
agreement.  **Both experiments produced negative results, and both negatives
correct a standing belief** - one of them a recommendation from round 15's own
review that would have cost the next round.

Nothing shipped.  Held out stays **-474**; the engine's default behaviour is
byte-for-byte unchanged (whole-corpus replay: 0 of 10,358 decisions).

### Experiment 1: the code fallback is NOT the largest attributable population

`tools/roundkit/holes.py` scans a corpus and reports both populations against a
**stage-matched** baseline - the corpus mean par gap is a mixture running from
-0.34 on the opening call to over +1 by the sixth, so comparing a late-auction
slice to the corpus mean flatters the slice.

Round 15's review reported the code fallback as **456 decisions at par gap -3.89
against a stage-matched +0.46, about -2,000 attributable gap-points, larger than
every named family combined**, and recommended starting round 16 there.  The
scan reproduces the number exactly: **470 of 10,358 (4.5%), gap -3.90 against
+0.43, total -2,035.**

**It is not attributable.  461 of the 470 are CLOSING passes** - the last calls
of an auction that is already over - and the hands are ordinary: `A82.K93.KQ97.J54`
passing partner's 3NT, `AK.642.KQJ52.K43` passing partner's 6S.  The comparison
that looks damning survives the stage control and still means nothing:

| closing calls in the corpus | n | par gap | stage | delta |
|---|---|---|---|---|
| made by an **authored rule** | 2605 | +1.28 | +0.37 | **+0.91** |
| made by the **fallback** | 461 | -3.83 | +0.43 | **-4.26** |

That five-point difference is **selection, not causation**: a fallback pass
*marks* an auction that has left the authored system, and those are the auctions
we bid badly long before the final pass.  Authoring pass rungs for these contexts
would have produced the identical calls at fit 1.00 and changed nothing.

**Nine** of the 470 are live seats where the auction continues.  That is the real
size of the hole, and it is not worth a round.

The instrument stays, because the *method* is right even though this answer was
no: `--fallbacks` grouped by `(context, call)` is a map of where the system runs
out, and `holes.py` now applies the closing-call test automatically.

### Experiment 2: simulation arbitration, measured for the first time

`match_ben.py` has always called `decide_fast`, which **discards
`fast_decision`'s `is_clear` flag**, so every match number in this file - every
round, every held-out verdict since head-to-head play began - is fast-path only,
and the simulation arbitration inside `choose()` had never been run against BEN.
It is the double-dummy rollout this project has repeatedly wished for and already
had: sample deals consistent with the auction, roll each candidate out, score the
final contracts double-dummy, compare in IMPs, and overturn the fast pick only on
a t-test at 1.5 stderr and at least 0.4 IMPs.

**How often it would even be consulted: 92 of 10,358 decisions (0.9%)** - not the
"about half" that round 12's finding (half of confident disagreements settled by
priority) had left everyone assuming.  And it splits into two different things:

| | n | par gap | stage | delta | total |
|---|---|---|---|---|---|
| genuine **priority tie** (two candidates fit >= 0.9 at equal priority) | 34 | -2.47 | -0.25 | -2.22 | -76 |
| **soft-miss lottery** (nothing fits at all; blended score decides) | 58 | -6.05 | -0.16 | -5.90 | **-342** |

So the "a static number that sees neither hand nor auction breaks the tie" story
is the *small* half.  The expensive half is the seat where no rule fits.

Measured with `--arbitrate` on both corpora:

| | before | after | delta | boards changed |
|---|---|---|---|---|
| review (242424) | -677 | **-651** | **+26** | 18 (7 up, 3 down) |
| **held out (828282)** | -474 | **-487** | **-13** | 18 (5 up, **9 down**) |

**Reverted on the held-out number.**  `--arbitrate` stays as an opt-in flag with
the numbers recorded, so nobody runs this experiment blind again.

The held-out losses have a clean-looking signature - arbitration talked us out of
four making games into partscores taking the same tricks (919: 4H making 11 ->
2H making 11, -10; 298: 3NT making 10 -> 3D making 10, -7) - and the obvious
refinement is to let it choose the strain but not the level.  **That hypothesis
is killed by the independent corpus:**

| | level changed | strain only |
|---|---|---|
| held out | 10 boards, **-28** | 8 boards, **+15** |
| review | 9 boards, **+28** | 9 boards, **-2** |

Both halves invert in sign between corpora.  This is round 15's FIX 4 kill
verbatim - a split that replicates on one metric and inverts on the other - and
the honest reading is that arbitration on a 0.9% population is **noise**, not a
lever with a fixable flaw.  A likely contributing cause, worth recording for
anyone who returns to it: `rollout` finishes the auction with `decide_fast` for
**all four seats**, so the simulation models the opponents with our own engine
while the match is played against BEN.

### What the round establishes

The two largest "the engine has no agreement" populations are now measured, and
neither is where the losses are.  Combined with round 15, three of the four
places the last two rounds nominated as the biggest remaining holes - the code
fallback, the keycard ask over a game raise, and the priority tie - have each
dissolved on a denominator.  The soft-miss lottery (58 decisions at -5.90) is the
one that survived both rounds and it has never been attacked directly.
