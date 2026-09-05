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

## Reading a lost board as an expert would: seed 501, board 786

An experiment in method rather than a round of fixes.  The question was
whether an LLM, asked the way a bridge expert is asked, finds what a human
expert finds on a lost board - after all the statistical attribution
(rule-level regret, BEN-disagreement clusters, last-bid blame) had stopped
paying.  One board, tried eight ways.

The board: none vulnerable, South deals with KQ9 K74 73 KJ965 and opens
1C; West overcalls 1D, North (J53 QJT85 986 A8) bids 1H, East makes a
negative double.  Our South **passed** (`xd_pass`, "sitting for their
double") and E/W bought it in 2D, down one, while BEN's South redoubled -
a support redouble - and N/S played 2H making.  Three IMPs, and the kind of
board any club player reads at a glance.

What the eight probes found, all run *blind* - four hands and the auction,
no rules, no BEN, no double-dummy, tools forbidden:

- **Whole-auction judgment** ("which N/S call would an expert panel
  reject?"): Opus and Sonnet both named South's pass and both named the
  support redouble as the call, with the reason ("by agreement pass denies
  three-card support, so North can never compete").  Haiku named the pass
  too but proposed 2H - it did not know the convention.  Model tier is not
  cosmetic here.
- **Recall instead of judgment** ("what are opener's standard agreements
  after 1m - (1x) - 1M - (X)?"): a correct system-card table, including the
  key fact that the support redouble is triggered by responder's one-level
  suit being doubled *whether or not LHO overcalled first*.  That sentence
  is the whole bug.
- **Decomposed reasoning** (six forced steps before a verdict) and
  **multiple choice** (rank P / XX / 2H / 1NT / 2C): both landed on XX;
  the panel-style ranking gave XX 10, Pass 5, 2H 4, and correctly called
  1NT the outright error (no diamond stopper, denies the support).
- **Graded capability probes**: every single-call interpretation and every
  hand-evaluation item was answered correctly.  On this board there was no
  level at which the model broke.
- **The engine as calculator**: 120 deals sampled consistent with the
  auction from South's seat, each candidate rolled out by the engine and
  scored double-dummy: 2H +0.80 IMPs over pass, XX -0.17, 1NT -0.35.  The
  negative number for XX is not bridge - it is the engine not knowing what
  its own redouble means, so partner mis-continued in every rollout.  The
  calculator measures the *current system's* handling of a call, and is
  blind to a call the system has never defined.  Useful for thresholds,
  useless for holes.
- **LLM writes the rule, the engine answers**: the `support_double` and
  `support_redouble` patterns were widened from `1$m - P - 1$M - ...` to
  `1$m - (P|bid<1$M) - 1$M - ...`.  The first replay against BEN then
  showed the next two holes at once: North "raised clubs" on a fallback
  instead of rebidding the known eight-card major, and South answered
  partner's minimum 2H with a natural 2NT on a 12-count - the board got
  *worse*, -3 to -6.  Two continuation contexts (`after_support_redouble_
  responder`, `after_support_redouble_opener`) closed them; the board is
  now 2H at both tables.  Six regression scenarios added.
- **Fine-tuning on expert panel commentary**: not testable on one board;
  noted as the fallback if prompting had failed.  It did not.

Verdict on the fix, paired on identical deals (only boards whose auction
changed count):

| corpus | changed boards | better / worse | net |
|---|---|---|---|
| seed 501, 1000 boards | 5 | 1 / 0 | +3 |
| seed 9001, 2000 boards (fresh) | 7 | 3 / 2 | +20 |

Small - the trigger is rare, about four boards in a thousand - and positive.
The two losers are downstream judgment calls of the ordinary kind (opener
passing 2D with a minimum instead of pushing with 3C; a generic 4NT firing
after a simple raise), not the species just fixed.

Two conclusions worth more than the IMPs:

1. **The expert read is reproducible when the question is posed as bridge,
   not as data.**  Every probe that saw only the deal and the auction found
   the flaw and named the convention.  Every earlier method that saw rule
   ids, fit scores and BEN distributions did not, because the flaw was a
   *missing* rule and there is no signal in the absence of a row.
2. **"Write the rule and replay" is the loop that finds the holes behind
   the hole.**  The first fix exposed two more within one auction.  A human
   would have found them by playing the board out; the engine finds them in
   a second, and the failing calls come tagged with the rule that made them.


## The blind-review round: 120 lost boards, 145 flags, one rule batch

The method from the board-786 experiment, run at the scale the plateau
demanded.  `tools/blind_review.py` packed the first 120 lost boards of the
seed-9001 match (two tables each, 240 prompts) into the starved prompt -
four hands, our auction, which pair is under review, nothing else - and
sent them to the strong model.  145 tables came back flagged, 95 clean.
`blind_review.py context` then replayed every flagged decision through the
engine and printed what it had seen: the candidates, their fits, the rule
that won, and whether the call the reviewer wanted existed at all.  Thirty-
nine of the 145 wanted calls were **not a candidate** - no rule offered them.

Reading the 145 with the engine's view alongside sorted them into about
twenty-five species.  Four of the first twenty-nine were reviewer errors
(a miscounted 5-count "must respond with 6+", a 1H-1S-2D called a reverse,
an 8-count called 7, a 25-count told to bid 22-24) - a false-positive rate
of roughly one in seven, all of them arithmetic, none of them bridge.

### What was authored

Nine new contexts, each for a position the generic toolkit had been
standing in for:

- advancer after our overcall is doubled (`advance_1level/2level_overcall_
  doubled`): the generic "their double" rules read a negative double as
  penalty - advancer sat with five trumps, ran on a 3-count, raised on
  responder's scale (b0010B, b0167B, b0228A, b0243A, b0306A)
- opener after partner's negative double, three shapes of it (RHO passes,
  RHO bids again, the double was of a weak jump): a 14-count jumped to 4S,
  an 11-count with four hearts passed, a forcing double was passed
  (b0189B, b0224A, b0127A, b0156A, b0341B)
- responder after our weak two is overcalled or doubled (b0031A made a
  "negative double" with four trumps; b0053B bid 4C on AKQJ653 of hearts)
- advancing the takeout double of a weak two or a preempt, with a
  **penalty pass** that outranks the forced suit bid when the hand holds
  the trumps (b0039A, b0031B, b0200B)
- opener after Jordan 2NT in the contested auction (b0011A: a generic 3C
  set clubs as trumps and the keycard answer was given for clubs)
- opener over partner's 1NT in competition, opener after a simple raise of
  the minor, a lead-directing (not takeout) double of their Stayman reply

And about forty edits to generic rules, the largest being:

- **a natural 2NT is not 11-12 from a player who opened or overcalled.**
  Six flags were openers bidding "11-12 2NT" on 11-13 counts.  A new
  `my_role` condition (opener / responder / overcaller / advancer / silent)
  gates the 11-12 rules and adds 18-19 and 16-18 versions.
- penalty doubles of their high contract count trumps in the *standing*
  strain, not their first suit (one rule became four, one per strain), and
  only once our side has acted
- balancing doubles need takeout shape (no 6+ suit, not a light two-suiter,
  never with four of their suit); the negative double of a jump overcall
  promises the unbid major; limit raises with three trumps need the high
  cards, shortness points do not substitute; the 18-19 jump rebid's
  responder context now also exists after a major opening; quantitative
  4NT opposite 22-24 and after 2NT-Stayman; longest suit first over their
  overcall and over their double; weak jump shifts over the double; the
  1M-1NT (semi-forcing) pass is 12-13 only; 3NT in a game force is not the
  call with a six-card major; running from partner's doubled contract is
  for weak hands; sandwich overcalls are never in their suit.

### What was tried and taken out

Three "extras-showing" doubles - opener reopening with 15+ and shortness,
a competitive double with extras, an action double of their game - were
authored from six flags and cost **-116 IMPs on the held-out corpus**,
with `fallback` firing 73 times behind them: partner had no agreement for
answering a reopening double, so the answers came from the fallback layer
(a 1S response on a doubleton, a 4S raise of that).  Same lesson as the
board-786 iteration, from the other side: a new call is a liability until
its continuations exist.  Removed; the six scenarios with them.  The 29-to-
20 board-level split of that failed version is recorded here so the next
attempt starts from the continuations.

One engine change besides `my_role`: a rule may declare `penalty_pass:
true`, and such a pass converts partner's one-round force when the hand
fits it outright.  Before this no authored penalty pass could fire while
any bid fitted at 0.3 - the existing `adv_pass_penalty` had been dead code.

### Verdict

Paired on identical deals, only boards whose auction changed:

| corpus | changed | better / worse / flat | net |
|---|---|---|---|
| seed 501, 1000 boards (held out) | 194 | 79 / 50 / 65 | **+147** |
| seed 9001, 2000 boards (the flags' source) | 449 | 169 / 126 / 154 | **+270** |
| seed 4242, 2000 boards (fresh) | 424 | 155 / 128 / 141 | **+180** |

Between +0.09 and +0.15 IMPs per board on corpora the fixes never saw,
against a whole-project history of -1.47 to -1.30.  Roughly one board in
five changed its auction; the worse-boards list is dominated by penalty
passes that used to collect 500 by accident, penalty doubles the old
first-suit bug happened to get right, and slam tries the generic RKC gate
still fires on minimum raises (b0339A, b0258B, board 192 here) - that gate
is the next structural item.

### Verifying this round with a cheap operator

Everything a reviewer without bridge judgement needs is mechanical:

1. `pytest` - 612 tests, 68 of them `tests/data/blind_review_9001.yaml`,
   one per flagged board with the hand, the auction and the accepted calls
2. `python tools/adjudicate.py --before reports/<corpus>.jsonl --seed <n>`
   on any corpus with a "before" file - exit 0 means the paired net is
   non-negative; the printout lists every changed board, worst first
3. `python tools/blind_review.py context --dir reports/review9001` - the
   engine's view of each flagged decision after the change: the wanted
   call should now be a candidate with fit near 1.0

What still needs a bridge player: reading the worst changed boards the
adjudicator prints, and deciding which of them are the price of correct
discipline and which are the next species.

## Blind-review round 2: seed 4242, 117 flags

Same protocol on the round-1 rules: the first 120 lost boards of the fresh
seed-4242 match, 240 blind prompts, **117 flagged, 123 clean** (round 1 had
145 / 95 on the same-sized sample - the flag rate fell by a fifth).  Twenty-
seven wanted calls were not a candidate.

### Authored

Twelve contexts: opener over the 1NT response to a minor (a 16-count with
5-4 had passed 1NT); opener and advancer after their takeout double and a
free response; responder over a three-level preempt of our minor (the
pairs the existing 1M and jump-overcall contexts did not cover); responder
after opener's support double; responder after opener's simple raise (3M
invitations on 7-counts came from the generic raise); opener accepting a
2NT invitation with an unbalanced 16; responder to 2C after opener's major
rebid (3M = raise with values, 4M = fast arrival); Stayman over partner's
1NT overcall and the overcaller's answer; advancer after partner overcalls
their weak two; opener's splinter after 1m - 1M and responder's answer to
it; natural overcalls of their weak two (the pass-out rule had outranked
every generic suit bid, so a 14-count with AQJT86 passed 2D).

Gates: a 2/1 in a minor is not made holding five spades over 1H; the
redouble over their double is not made with a void in partner's suit; the
weak pass outranks running; opener's jump raise needs 15 HCP; penalty
passes of a weak two want real trumps; takeout doubles are not made with
a six-card suit to bid (four overcall contexts, the 3-level defence, the
1NT defence); the higher of 5-5 majors is overcalled first; the cue-bid
raise needs 10 HCP; placing the contract after 2C-Stayman uses the major
opener showed; the support-double 2NT is balanced; a good six-card suit is
also shown before 3NT in a game force; natural 3NT in an ordinary
continuation runs to 21; sandwich 1NT (15-18, both suits stopped) and a
seven-card suit at the two level; quantitative 4NT over the 1NT rebid.

### Tried and taken out, again

Third-seat light openings with a five-card major (three flags) cost -8 and
-10 on held-out boards and, worse, lowered partner's *shown minimum* on
every third-seat opening, which pushed unrelated game raises below their
gates (board 1340: a 4H raise fell to 0.8 fit because opener might now
hold 10).  Removed.  The negative-double gate "not with four of partner's
suit" removed a working double and left nothing behind it on board 476;
reverted.  Two other first drafts were corrected by the seed-9001 read
rather than removed: the 2C - 2D - 2M raise now carries values (with a bust
it is fast arrival), because the un-gated 3M had erased the information
the slam try was reading; and the three-level balance on a five-card suit
is a first-action rule only (a 1NT overcaller re-entering at the three
level was doubled for -13).

### Verdict

| corpus | changed | better / worse / flat | net |
|---|---|---|---|
| seed 501, 1000 (held out) | 90 | 37 / 19 / 34 | **+72** |
| seed 9001, 2000 (held out) | 202 | 63 / 57 / 82 | **-3** |
| seed 4242, 2000 (the flags' source) | 229 | 67 / 59 / 103 | **+76** |

Positive on two of three, flat on the third; a third of round 1's per-board
gain.  The first draft of this round read -73 on seed 9001 before the
corrections above; the held-out read is what turned it.  Note for the next
round: several "changed" boards on 9001 changed only because BEN answered an
identical auction prefix differently between runs (boards 1411, 1461, 549),
so the paired count carries a little BEN noise of its own.

The method's yield is falling as it should: round 1 found whole missing
structures, round 2 found their neighbours.  What the flags now keep
naming and the rules do not yet address: the generic RKC gate firing over
minimum raises (three more boards), and hand-evaluation questions (light
openings, aggressive preemptive raises) where the reviewer and the corpus
disagree and the corpus should win.

## Blind-review round 3: 500 lost boards, 516 flags, the species table

The scale the user asked for: a fresh 2000-board match (seed 31337), its
first **500 lost boards**, both tables each, 1000 blind prompts.  516 tables
flagged, 484 clean.  At this size nobody reads 516 verdicts one by one, so
`blind_review.py species` groups them: the context and rule that made the
flagged call, and what kind of call the reviewer wanted (raise / rebid /
cue / new suit / notrump / double / pass), with the count, the IMPs and
whether the wanted call existed as a candidate.  497 located flags fell into
264 species; the top thirty carried the round.

What the table said, in one line: **the engine passes too much.**  The
largest species were all "pass where a bid was wanted" - the generic pass in
uncontested continuations (16 wanted notrump, 13 a raise, 12 a new suit),
in competition (14 new suit, 9 raise), at the high level (13 new suit, 7
raise, 5 rebid), in the balancing seats (13 doubles) - and the pass-out
rules of the overcall contexts (14 openings, 11 overcalls, 3 over a weak
two, 3 in the sandwich seat).

### Authored

Nine contexts.  The one with the widest reach is a floor under every
takeout double: `advance_any_takeout_double` ("... - X - P - ?", for the
doubler's partner who has not yet bid) answers a balancing double, a
reopening double, a double over their raise or over a preempt - the direct-
seat advance contexts existed, everything else fell to the generic pass
(twelve flags with three small trumps).  It carries an authored penalty
pass for four good trumps.  Then: opener's reopening double over their
three-level-or-higher preempt after two passes (with the advance floor in
place this time, the double has a continuation); responder's rebid over
opener's second suit after 1D - 1M - 2C; the advancer's placement after the
1NT overcall's Stayman reply; responder over opener's 2NT rebid of the 1NT
response; opener after raising and being re-invited; the Ogust asker's
continuation (a 20-count had passed the reply); the penalty doubler of 1NT
after their runout; opener over a doubled 2C.

Gates: one-level overcalls need no suit quality with six cards or with
12+; two-level overcalls take a six-card suit on 10 or any five on 15+;
overcalls of a weak two take an eight-card suit on 8 or a good five on 14;
rule-of-20 openings with two five-card suits need no suit quality; natural
3NT in an ordinary continuation is allowed a singleton with 16+ but never a
known eight-card major fit or their suit unstopped; a first-action 1NT
between two bidding opponents is the sandwich 1NT, so the 8-11 rule is for
responders and advancers; the overcaller's 16-18 2NT is gone (six flags of a
described hand re-describing itself); the two-level negative double is not
made with four of partner's suit; the takeout-flavoured double is short in
the suit doubled (one rule per strain); the negative double of 1S over 1H
needs both minors and no long suit, and natural 2C/2D exist beside it;
four-level new suits in competition take six cards, three-level ones six
with 9+; a seven-card suit rebids itself in competition without a point
count; a preemptive game raise with five trumps and a weak hand; support
doubles after 1H - 1S and 1C - 1D; Stayman and transfers are answered over
their double.

### Verdict

| corpus | changed | better / worse / flat | net |
|---|---|---|---|
| seed 501, 1000 (held out) | 202 | 91 / 60 / 51 | **+200** |
| seed 9001, 2000 (held out) | 364 | 147 / 130 / 87 | **+169** |
| seed 4242, 2000 (held out) | 372 | 158 / 122 / 92 | **+217** |
| seed 31337, 2000 (the flags' source) | 458 | 200 / 140 / 118 | **+486** |

The largest round so far on held-out deals: +586 over the 5000 boards that
never contributed a flag, about +0.12 IMPs per board, on top of rounds 1 and
2.  Reading five hundred boards instead of a hundred and twenty did not
change what the method finds; it changed how confidently a species could be
told from a one-off, and it made the "passes too much" diagnosis visible as
a shape rather than as anecdotes.

Reviewer arithmetic errors were again about one in seven, and again all of
them counting (a 14 called 15, a 9 called 11, a 10 called 11); three
scenarios accept the system's call because of them.

## Blind-review round 4: seed 8080, 500 boards, 489 flags

Same protocol as round 3 on the round-3 rules: a fresh 2000-board match
(seed 8080), 500 lost boards, 1000 blind prompts.  **489 flagged, 511
clean** - the first round where more tables came back clean than flagged.
438 located flags in 275 species; the top species were still passes where
a bid was wanted, and for the first time several were rules from the
previous round misfiring.

### Round-3 rules corrected by this round's flags

- The reopening double over their preempt had been written on "... - bid -
  P - P" and fired on freely bid games (a 4H reached after 1D - X - P - 1H
  - 1S - 4H was doubled on a singleton trump).  It is now "1x - bid>=3C - P
  - P": their direct jump over our opening only, and responder has a
  context to answer it.
- The advance floor under takeout doubles let a 4-count pull partner's
  penalty double of 3S.  Suit answers are now for a silent hand at the one
  and two levels; the pass-out-seat doubles of weak twos and preempts got
  their own copies of the direct-seat advance contexts.
- The semi-forcing 1NT pass (12-13) needed a shape gate: not with a
  six-card major or a second minor to show (two harvested BEN scenarios),
  but yes with 5-4 in the majors when 2S would be a reverse.

### Authored

- **Fast arrival.**  In a game force the generic four-level raise now
  requires a minimum; with 15+ the raise is to three (slam interest).  Four
  flags had 15-counts jumping to game and ending the auction.
- Opener over the simple raise in competition (pass 12-15, invite 16-17,
  game 18+); opener accepting a 2NT invitation directly over the minor,
  after rebidding it, or in competition, with a six-card source of tricks
  counting as acceptance; responder over the 18-19 rebid of 1NT to a major,
  and over the jump rebid when RHO overcalled; Stayman placement after
  their double; the doubler raising advancer's suit with four trumps; the
  preemptive jump raise of partner's suit in competition (four trumps,
  weak, shape, LOTT) beside the cheapest-level competitive raise; natural
  2H/2D beside the negative double over their two-level overcall; garbage
  Stayman; a five-card major before 1NT when advancing a double; sandwich
  one-level overcalls on six cards or 11+; natural 3NT counting 26 with
  partner's minimum rather than with length points; game in a major after
  2NT - Stayman only in the major opener showed.
- `game_forced` is now also a rule-level `when` condition.

### Verdict

| corpus | changed | better / worse / flat | net |
|---|---|---|---|
| seed 501, 1000 (held out) | 90 | 43 / 27 / 20 | **+58** |
| seed 9001, 2000 (held out) | 176 | 88 / 54 / 34 | **+155** |
| seed 4242, 2000 (held out) | 176 | 78 / 56 / 42 | **+137** |
| seed 8080, 2000 (the flags' source) | 179 | 90 / 50 / 39 | **+258** |

+350 on the 5000 held-out boards, +0.07 per board; fewer boards changed
than in round 3 (the round-3 rules had already taken the broad species).
Four rounds together, on the held-out corpora that saw none of the flags:
seed 501 has gone from -1180 to -703 IMPs per thousand, seed 9001 from
-2193 to -1602 per two thousand, seed 4242 from -2252 to -1642.  Against
the -1.30 per board the project stood at when the blind review began, the
held-out corpora now read about -0.75.
