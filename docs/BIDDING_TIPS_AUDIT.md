# Bidding-Tips Audit (138 codeable judgment rules)

Status of every tip from the expert-canon list against this engine.
Statuses: **IMPL** (already implemented - mechanism cited), **ADDED**
(implemented in the tips round), **PART** (partially covered - what exists
and what is missing), **DEFER** (not implemented - reason), **N/A** (the
engine expresses this some other way, or the mode does not exist).

Ground rules used throughout: additions must not weaken anything a match
has already measured; where a tip contradicted a *measured* regression
scenario, the corpus outranked the textbook and the tip was adjusted
(noted inline).  Deferred evaluation-model changes (re-weighting every
decision's point count) are avoided because they change hundreds of
measured rules at once and can only be adjudicated by match play.

## A. Static evaluation
| # | Status | Where / why |
|---|--------|-------------|
| 1 | IMPL | `hcp` evaluator (4-3-2-1) is the base of every gate |
| 2 | PART | `adjusted_hcp` exists (honor-location adjustments) but is not wired into decision rules; the soft-fit Gaussian boundaries play the equivalent role. Global re-wiring needs match measurement |
| 3 | PART | `adjusted_hcp` deducts stiff K/Q/J (-1) and bare Qx/Jx (-0.5); same wiring caveat |
| 4 | PART | `adjusted_hcp` credits 2+ honors in a 5+ suit; same caveat |
| 5 | PART | same evaluator, same caveat |
| 6 | DEFER | no ten/nine credit; `suit_quality` counts T/J at 0.5 for suit-quality gates, which covers the suit-texture half |
| 7 | DEFER | no 4-3-3-3 deduction (evaluation-model change) |
| 8 | PART | 4-4-4-1 cannot open light (rule-of-20 rules demand a 5-card suit); no general downgrade |
| 9 | IMPL | `dist_points` (+1 per card past the fourth) inside `total_points` |
| 10 | PART | `suit_quality` gates on light openings, weak twos, preempts |
| 11 | IMPL | `quick_tricks` evaluator; now load-bearing (rules 13, 37/88) |
| 12 | IMPL | `rule_of_20`, seats 1-2, plus suit-quality gate |
| 13 | ADDED | rule of 22: all four rule-of-20 openings now require `quick_tricks >= 2` |
| 14 | IMPL | `rule_of_15`, 4th seat |

## B. Dynamic re-evaluation
| # | Status | Where / why |
|---|--------|-------------|
| 15 | IMPL | `shortness_points` (5/3/1) via `total_points` once a trump fit exists |
| 16 | IMPL | `total_points` switches to shortness only with an agreed suit and 3+ support |
| 17 | DEFER | no deduction for shortness in partner's suit (narrow; raise rules demand length instead) |
| 18 | PART | no honor-location re-weighting; partner-range arithmetic (`rule_of_26`) carries the strength half |
| 19 | DEFER | no positional (over/under) honor adjustment |
| 20 | PART | penalty doubles gate on trump length + quick tricks, not honor quality in their suit |
| 21 | ADDED | `wasted_in_partner_shortness` evaluator: K/Q/J points in a suit partner shows short (aces exempt); drives the new Jacoby/splinter signoffs |
| 22 | PART | `ltc` evaluator exists (gates the 2C opening); the LTC level formula is not used globally |
| 23 | DEFER | no cover-card evaluator |
| 24 | IMPL | `lott_total_trumps` (sharp) gates every competitive raise level |
| 25 | DEFER | no 6-4/5-5 bid-one-more bonus (fallback raise bands partially) |
| 26 | PART | "20+ playing strength" gates opener's too-strong-to-invite rebid; not a global switch |
| 27 | DEFER | no offensive/defensive HCP split |
| 28 | N/A | the sampler and simulation arbitration do exactly this inference; it is not a rule |
| 29 | PART | LOTT sharpness + suit-quality on some raises; no universal trump-texture gate |
| 30 | DEFER | no mirrored-shape penalty |

## C. Opening constraints
| # | Status | Where / why |
|---|--------|-------------|
| 31 | DEFER | needs rebid lookahead the engine does not do |
| 32 | IMPL | light openings demand suit quality; 5-5 opens the higher; spades favored by the S-before-H rule order |
| 33 | ADDED | `open_1S/1H_third_light`: 9-11 HCP, 5-7 cards, suit quality 2.5+ (lead-worthy), seat 3 only |
| 34 | IMPL | rule-of-15 pass-outs |
| 35 | IMPL | seat gates throughout (light 1-2, third-seat light ADDED, 4th constructive) |
| 36 | IMPL | vacuously: light openings require a 5-card suit, so 4-4-4-1 never opens light |
| 37 | ADDED | see 88 |
| 38 | DEFER | conflicts with a measured decision (opener rebids accept 10-15 so light openers keep an honest rebid) |

## D. Responding and supporting
| # | Status | Where / why |
|---|--------|-------------|
| 39 | IMPL | raise priorities above new-suit/NT throughout the response contexts |
| 40 | IMPL | immediate raise structure (raises, limit raises, Jacoby, splinters) |
| 41 | DEFER | no ace-based threshold shift (micro-tuning; Phase-3 warning) |
| 42 | IMPL | support points + `rule_of_26` do exactly this |
| 43 | IMPL | preemptive game raise, preemptive jump raises over their double, LOTT levels |
| 44 | IMPL | weak-pass rules; the fallback layer never rescues |
| 45 | IMPL | up-the-line responses, Walsh 1D |
| 46 | DEFER | no their-suit HCP discount |
| 47 | DEFER | no fitting-honor multiplier |
| 48 | PART | the permissive general pass plus `rule_of_26` keep the inviter quiet; no explicit flag |
| 49 | N/A | no lookahead; the GF/forcing discipline protects the failure case |
| 50 | IMPL | competitive raises full-range (a measured harvest-round decision) |
| 51 | IMPL | competitive raise priority (30/31) above generic new suits (27) |
| 52 | IMPL | preemptive raise over their double; redouble = values |
| 53 | IMPL/PART | cheapest-suit advance 0-8 exists; the penalty-pass trump gate is implicit (pass discipline), not explicit |
| 54 | IMPL | raise priorities |

## E. Rebid constraints
| # | Status | Where / why |
|---|--------|-------------|
| 55 | PART | general pass + `rule_of_26` gates; no explicit "new information" test |
| 56 | IMPL | generic suit rebids require 6+ cards |
| 57 | IMPL | by rule design (jump rebids with extras forcing, minimum rebids limited) |
| 58 | IMPL | limit bids and fast arrival throughout |
| 59 | PART | priorities + partner-range arithmetic approximate it; no limited-hand flag |
| 60 | DEFER | specific priority comparison not audited |
| 61 | N/A | the soft-fit model IS this ordering: hcp misses cost least, major-length misses most |
| 62 | IMPL | fallback terminates at the lowest playable spot; a force may be passed on total misfit |

## F. Overcalls and balancing
| # | Status | Where / why |
|---|--------|-------------|
| 63 | PART | `suit_quality` gates approximate SQT; no explicit length+honors >= tricks formula |
| 64 | IMPL | 1-level overcalls 8-16, decent 5+ suit |
| 65 | IMPL/DEFER | 11-17 good suit implemented; vulnerable tightening deferred (measured rule) |
| 66 | IMPL | 5+ cards required everywhere |
| 67 | DEFER | no spade-specific loosening |
| 68 | PART | overcaller continuations gated by `rule_of_26`; note the reverted "don't preempt twice" floor (see DECISIONS) |
| 69 | IMPL | advancer raise on 3 + modest values |
| 70 | DEFER | no their-suit concentration veto on overcalls |
| 71 | IMPL | balancing seat authored "a king light" |
| 72 | IMPL | implicit and sound: the partner model carries the balancer's lighter shown range, so `rule_of_26` adds the king back automatically |
| 73 | IMPL | balancing double keyed on shortness in their suit |
| 74 | IMPL | the same shortness gate vetoes reopening with length |
| 75 | DEFER | no push-them-into-game model |
| 76 | IMPL | by architecture: rules fire at the first legal turn; sandwich + balancing seats authored |

## G. Doubles
| # | Status | Where / why |
|---|--------|-------------|
| 77 | IMPL | takeout doubles: shortness <= 2 + support for unbid suits, or 17+ |
| 78 | PART | the 17+ override branch exists; no graduated +3 rule |
| 79 | IMPL | `ch_penalty_X`: 3+ quick tricks AND 3+ trumps (the measured business-double fix); positional "over" refinement deferred |
| 80 | IMPL | by absence: no low-level penalty double exists to misfire |
| 81 | IMPL | same rule (trump tricks required) |
| 82 | IMPL | same rule covers slam doubles (3 QT is stricter than the tip) |
| 83 | PART | several contexts prefer X with flat extras by priority |
| 84 | IMPL | 3+ trump length required implies no void |
| 85 | PART | LOTT gates bias to defending; no explicit 4-trump rule |
| 86 | IMPL | never pull own doubled contract; advancer pass discipline (measured) |

## H. Preempts - making them
| # | Status | Where / why |
|---|--------|-------------|
| 87 | PART | vulnerability tightens HCP floor and suit quality on every preempt; no 2-3-4 playing-trick count |
| 88 | ADDED | `quick_tricks_outside(suit) <= 2` on all 16 preempt openings. Evidence-adjusted from the tip: AK inside the long suit is offence, and two measured scenarios keep preempts holding exactly 2.0 outside |
| 89 | ADDED | side 4-card-major veto on the 3-level preempts (weak twos already had it) |
| 90 | ADDED | `preemptor_discipline` context on the new `i_preempted` engine condition: no voluntary second bid; forcing continuations unaffected. Properly implements the maxim whose crude version (a 10-HCP floor) was measured at -10 IMPs and reverted |
| 91 | IMPL | seats 1-3 only; no 4th-seat preempts (rule-of-15 constructive instead) |
| 92 | IMPL | preemptive jump raises straight to the LOTT level |

## I. Preempts - facing and fighting them
| # | Status | Where / why |
|---|--------|-------------|
| 93 | PART | responses to preempts use total-point/trick branches, not pure cover cards |
| 94 | IMPL | LOTT raises of partner's preempt |
| 95 | IMPL | RONF: no invitational machinery over preempts exists |
| 96 | IMPL | preemptive raise over the double (harvest round 2) |
| 97 | IMPL/PART | takeout of a preempt authored 14-17/18+ with 3-small tolerance; QT re-weighting partial |
| 98 | PART | as 97 |
| 99 | PART | 5-level competitive raises demand LOTT trumps; no make-probability model |

## J. Competitive partscore logic (LOTT)
| # | Status | Where / why |
|---|--------|-------------|
| 100 | IMPL | `lott_total_trumps` gates at 7/8/10 for the 2/3/4+ levels |
| 101 | PART | the 3-level competitive raise also asks 10+ support points; relaxing it means re-measuring a tuned rule |
| 102 | PART | as 101, from the other side |
| 103 | DEFER | no LOTT adjustment terms |
| 104 | DEFER | as 103 |
| 105 | DEFER | their combined trumps are not modeled |
| 106 | IMPL | jump raises go to the LOTT level in one call |
| 107 | IMPL | shortness triggers on balance/reopen; length passes |
| 108 | IMPL | 5-level raises require the trumps |
| 109 | DEFER | no flat-max/shapely-min switch |
| 110 | N/A | the DSL has no score arithmetic; simulation arbitration prices these |
| 111 | PART | takeout X blocked when long in their suit; no explicit trap-pass rule |

## K. Slam bidding
| # | Status | Where / why |
|---|--------|-------------|
| 112 | PART | controls gates on every ask; the unbid-suit fast-loser check is the doubleton veto below |
| 113 | ADDED | void veto on ALL direct 4NT asks; worthless-doubleton (xx/Jx) veto where the cue floor exists (`rkc_4NT`, `jac_rkc`). In the no-cue positions the doubleton veto measurably deleted slams and was scoped out - the corpus outranks the textbook |
| 114 | PART | asks gated to 2+ level with signoff room; no general response-forces-past-contract check |
| 115 | IMPL | the cue-bid machinery is exactly this (cheapest-first + skip-denial via negative inference) |
| 116 | ADDED | `jac_wasted_signoff` / `spl_wasted_4M`: 4+ wasted K/Q/J points opposite shown shortness sign off in game |
| 117 | ADDED | the evaluator exempts aces (working opposite anything) |
| 118 | N/A | no probability estimates; simulation arbitration approximates on close calls |
| 119 | IMPL | 6NT needs `rule_of_26 >= 33` + controls; the quantitative 4NT ladder covers the split counts |
| 120 | PART | strain comparison happens in arbitration rollouts, not rules |
| 121 | DEFER | no trump-solidity gate on 8-card-fit slams |
| 122 | IMPL | accept/decline pairs end quantitative sequences |
| 123 | DEFER | no preempt-in-auction slam tightening |
| 124 | IMPL | RKC signoff branches; unresolved auctions land in game, not slam |

## L. Scoring and vulnerability
| # | Status | Where / why |
|---|--------|-------------|
| 125 | IMPL | vulnerability branches on weak twos and preempts |
| 126-127 | N/A | IMPs only; thresholds come from measured match play, not success estimates |
| 128-130 | N/A | no matchpoints mode |
| 131 | IMPL | `gf_minor_3NT` (3NT over 5m when stopped) and the major-game landing rules are exactly this |
| 132 | IMPL | no casual partscore doubles exist; the one penalty double demands 3 QT + trumps |
| 133 | N/A | no probability model |
| 134 | IMPL | arbitration optimizes IMP delta of the final contract |
| 135 | PART | fourth-suit-forcing right-sides 3NT; no general right-siding rule |
| 136 | IMPL | near-ties break to higher priority then the tighter descriptor; cues cheapest-first |
| 137 | IMPL | fast arrival + direct game landings |
| 138 | IMPL | the permissive general pass is the null action |

## Tally
IMPL 63 · ADDED 10 · PART 33 · DEFER 22 · N/A 10.

The ADDED set (this round, test-verified, match-UNMEASURED per the no-more-
deals instruction): rule of 22; preempt quick-trick veto (outside-suit form);
3-level preempt side-major veto; third-seat light openings; preemptor
discipline (`i_preempted`); Blackwood void/worthless-doubleton prerequisites;
Jacoby and splinter duplication signoffs (`wasted_in_partner_shortness`);
plus two new engine conditions/evaluators supporting them.  The next match
round should re-run seed 828282 (last measured -1248) before further work.
