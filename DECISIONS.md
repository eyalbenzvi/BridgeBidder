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
  descriptive bid otherwise; near-ties break toward higher rule priority.
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
