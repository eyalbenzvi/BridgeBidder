# BridgeBidder — a 2/1 Game Forcing bidding engine

A production-quality bridge bidding engine (library + CLI, no GUI). The
bidding system is **data** (a YAML knowledge base for 2/1 Game Forcing); the
engine layers inference, auction-consistent sampling and double-dummy
simulation arbitration on top of it, and every call comes with a structured,
alert-ready explanation — including automatically derived *negative*
inferences ("no support double, so not exactly 3 spades").

## Quick start

```bash
pip install -e ".[dd,test]"      # endplay (real double-dummy solver) + pytest
pytest                            # full test suite
bid choose examples/choose_opening.json
bid explain examples/explain_support_double.json
python demo.py                    # self-play 5 random deals with explanations
```

## The two public operations

### 1. `choose_bid` — pick a call

```python
from bridgebidder import choose_bid

result = choose_bid({
    "hand": "AQ52.KJ4.T92.873",              # Spades.Hearts.Diamonds.Clubs
    "auction_state": {
        "dealer": "N",
        "vulnerability": "None",              # None | NS | EW | Both
        "seat": "S",                          # engine bids for this seat
        "calls": [
            {"call": "1H"},
            {"call": "2D", "explanation": {   # opponent's alert, used as a constraint
                "text": "Multi-style, weak with 6 diamonds",
                "constraints": {"suits": {"D": [6, 13]}, "hcp": [4, 10]},
            }},
        ],
    },
})
```

Output (JSON-shaped dict):

```json
{
  "chosen_call": "2H",
  "confidence": "clear",                  // "judgment" = simulation arbitration ran
  "explanation": { ...BidExplanation... },
  "alternatives": [
    {"call": "3H", "match_score": 0.62, "expected_imp_delta": -0.8, "shows": "..."}
  ],
  "partner_model":  {"hcp": [12, 21], "suit_lengths": {"S": [0,13], "H": [5,13], ...}},
  "opponent_models": {"E": {...}, "W": {...}},
  "arbitration": { "n_deals": 44, "imp_deltas": {...}, "winner": "2H" }   // when it ran
}
```

### 2. `explain_bid` — what would this call show?

```python
from bridgebidder import explain_bid

explanation = explain_bid({
    "auction_state": {"dealer": "N", "seat": "N",
                      "calls": ["1D", "P", "1S", "2C"]},
    "candidate": "2D",
})
```

Structured `BidExplanation`:

```json
{
  "call": "2D",
  "shows": {"hcp": [12, 15], "suits": {"D": [6, 13]}, "features": [],
             "text": "6+ D, minimum, fewer than 3 S"},
  "denies": [
    {"text": "not: support double: exactly 3-card S support, any strength",
     "constraint": {"not": {"hcp": [12, 21], "suits": {"S": [3, 3]}}},
     "derived_from_rule": "sd_double", "weight": "strong"}
  ],
  "forcing_status": "non_forcing",
  "alertable": false,
  "convention": null,
  "source_rule_id": "support_double[D,S].2D",
  "is_undiscussed_fallback": false
}
```

The `denies` list is **derived automatically** from higher-priority rules the
player skipped — no hand-written denial lists.

### CLI

```bash
bid choose input.json          # or:  cat input.json | bid choose
bid explain input.json
bid choose --no-arbitration input.json   # deterministic fast path only
```

Example inputs live in `examples/`.

## Architecture

```
src/bridgebidder/
  domain/        cards, hands, calls, auction legality/turn/contract
  evaluation/    pluggable evaluator registry: hcp, total_points, rule_of_20,
                 rule_of_15/26, ltc, suit_quality, stoppers, controls, ...
                 (register_evaluator adds one with zero engine changes)
  constraints/   HandConstraint: interval + feature + shape constraints with
                 anyOf/not combinators, exact satisfaction, SOFT degree-of-fit
                 (sigmoid boundaries), intersection, and coarse Box summaries
  system/        the DSL: YAML -> contexts (auction patterns) -> BidRule;
                 template expansion ($M, expand_pairs), pattern matcher
                 ("1(H|S) - P - ?", "bid<2H", "..." open prefix)
  inference/     per-player HandDescriptors: positive constraints, priority-
                 ordered negative inference, explanation overrides; the
                 fallback layer (engine never lacks a candidate); the
                 DecisionSetup used identically by choosing, explaining,
                 replay and rollouts (this shared path IS the consistency
                 invariant)
  engine/        decision pipeline (fast path -> arbitration), the
                 auction-consistent sampler, DD evaluation (endplay DDS with
                 a heuristic fallback), duplicate scoring + IMPs, self-play
  systems/       two_over_one.yaml — the 2/1 GF knowledge base (~140 contexts)
  api.py, cli.py public operations
```

### Decision pipeline

1. Generate candidates: all legal rule calls in the matched contexts plus
   generic fallbacks (flagged `is_undiscussed_fallback`).
2. Soft-score each candidate's constraints against the hand (a 1-HCP miss
   scores ~0.8, a missing trump ~0.35; rule-of-20 branches rescue borderline
   openings via `anyOf`).
3. Fast path: a candidate fitting >= 0.9 wins by rule priority (~80-95% of
   decisions, < 50 ms).
4. Otherwise the top 2-4 *plausible* candidates go to simulation
   arbitration: sample auction-consistent deals, roll out each candidate to
   the end of the auction with the engine playing all four seats, score the
   final contracts double-dummy, convert to IMPs, and pick the winner (with
   a significance check that prefers the more descriptive call on ties).

### Auction-consistent sampling

`sample_consistent_deals` fixes your hand, deals the other 39 cards (biased
toward partner's descriptor box), then **replays the auction**: partner's
calls must be exactly reproduced by the engine's deterministic policy —
which enforces every positive *and negative* inference automatically —
while opponents' hands must satisfy their explanation-derived constraints
plus loose natural readings. Time-budgeted with graceful degradation.

The canonical test: after `1D - P - 1S - (2C) - 2D`, no sampled deal gives
opener exactly 3 spades (he would have made a support double).

## Testing

```bash
pytest                       # 400+ tests
pytest tests/test_regression.py   # 179 data-driven auction scenarios
```

- unit tests for every domain type, evaluator and constraint operation
- 179 regression scenarios in `tests/data/*.yaml` (openings by seat and
  vulnerability, 2/1 sequences, the whole 1NT structure, weak twos,
  competitive auctions, support/negative doubles, RKC, fallbacks)
- invariants: self-play/replay consistency, never passing a game force out
  below game, `explain_bid == choose_bid`'s explanation
- properties: 500 random deals of full self-play terminate legally
- sampling distribution tests, performance budgets, and 22 frozen
  explanation snapshots (`python tests/test_snapshots.py --regen`)

## Extending the system

**Add a convention** — edit `systems/two_over_one.yaml` only:

```yaml
- id: michaels_cue
  expand: { M: [H, S] }
  pattern: "1$M - ?"
  rules:
    - id: michaels_2$M
      call: 2$M
      priority: 75
      requires: { suits: { $oM: [5, 13] }, any_of: [ {suits: {C: [5,13]}}, {suits: {D: [5,13]}} ] }
      shows: "Michaels: 5-5 in the other major and a minor"
      establishes: { forcing: one_round }
      alertable: true
      convention: michaels
```

Rules support `priority`, `requires` (a HandConstraint), `shows`, explicit
`denies`, `establishes` (forcing status / game force / agreed suit / active
ask), `alertable`, `announce`, `convention`, `negative_inference_weight`
(strong|soft) and `when` conditions (opening seat, passed hand,
vulnerability, config flags).

Rule conditions (`when:`) cover auction facts rather than hand facts:
`opening_seat`, `passed_hand`, `we_vulnerable`, `they_vulnerable`,
`we_hold_contract`, `partner_suit`, `unbid_suit`, `cheapest_in_suit` and
`config` flags. Use them for anything decided by the auction — a soft
`requires:` feature would only *discourage* a structurally wrong call, while a
`when:` gate rules it out.

**Add an evaluator** — zero engine changes:

```python
from bridgebidder.evaluation import register_evaluator

@register_evaluator("prime_cards")
def prime_cards(hand, ctx):
    return sum(1 for c in hand.cards if c.rank >= 13)
```

then reference `prime_cards` in any rule's `evals`.

**Add a whole system**: write another YAML file and pass
`system_path` in the API request (or point the CLI input's `system_path`
field at it). Config flags (`forcing_nt`, `two_over_one_suit_length`,
`nt_with_5M`) can be overridden per request via `config`.

**Swap the double-dummy engine**: implement the 3-method `DDEvaluator`
protocol and call `bridgebidder.engine.dd.set_dd(...)`.

## Style decisions

Every bridge-judgment and engineering decision is logged with a rationale in
[DECISIONS.md](DECISIONS.md).
