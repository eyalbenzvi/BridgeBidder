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
