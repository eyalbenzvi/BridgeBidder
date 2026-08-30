# The system DSL, for a reviewer who must write exact YAML

`src/bridgebidder/systems/two_over_one.yaml` IS the bidding system.  517
contexts, 2,344 rules, no bridge logic in the Python.  A proposal is only
implementable if it is written in this vocabulary, so this file is the
vocabulary.

## A context

```yaml
  - id: nt_transfer_accept_H
    description: "Opener completes the hearts transfer"
    pattern: "1NT - P - 2D - P - ?"
    rules:
      - id: tr_super_3H
        call: 3H
        priority: 60
        requires: { suits: { H: [4, 5] }, hcp: [17, 17] }
        shows: "super-accept: 4 hearts, maximum"
        establishes: { forcing: non_forcing }
```

### `pattern` grammar

Tokens separated by ` - `; leading passes are stripped before matching, and
the pattern MUST end in `?`.

| token | meaning |
|---|---|
| `1H`, `P`, `X`, `XX`, `2NT` | that exact call |
| `(1H\|1S)` or `1(H\|S)` | alternation |
| `*` | any single call |
| `bid`, `bid<=3S`, `bid<2H`, `bid>=2C` | any contract bid, optionally bounded |
| `act` | any non-pass call (bid, X or XX) |
| `...` | prefix wildcard — **only as the first token** |
| `?` | the decision point — **only as the last token** |

**Specificity decides which context owns a decision.**  `specificity =
(0 if the pattern starts with "..." else 1000) + number of tokens`, highest
wins, ties broken by file order (earlier wins).  So `"... - ?"` is the LEAST
specific pattern in the file and always sorts last — a context written that
way can never steal a call from a context that already defines it.  That is
the structural way to obtain the superset property.

`also_patterns: ["..."]` adds extra shapes a context owns.

### Templating — this is how 400 ideas become 2,000+ rules

```yaml
    expand: { M: [H, S] }              # cartesian product over the keys
    expand_pairs:                       # explicit combinations
      - { T: D, M: H }
      - { T: H, M: S }
```

`$M` substitutes anywhere in any string of the context.  `$oM` is
automatically the OTHER major (H<->S) and `$om` the other minor (C<->D).
Context ids become `id[H]`, `id[D,H]`, etc.

**Two hard rules that have cost this project cycles:**

* a template var must **END** a rule id: `id: foo_$M` is fine, `id: foo_$M_bar`
  is NOT;
* `call: $L$X` does **not** expand — write the level out (`call: 3$M`).

## A rule

| field | meaning |
|---|---|
| `id` | unique; template var last if any |
| `call` | `1S`, `3NT`, `P`, `X`, `XX` |
| `priority` | float.  Higher wins **among candidates fitting >= 0.9** |
| `requires` | a HandConstraint — the hand this rule describes |
| `shows` | one sentence, shown to the user; must match `requires` |
| `denies` | explicit denials (rarely needed — negatives are derived) |
| `establishes` | `{forcing: …, game_force: bool, agreed_suit: S, asking: keycards}` |
| `when` | conditions about the AUCTION, not the hand |
| `alertable`, `announce`, `convention` | disclosure |
| `negative_inference_weight` | `strong` (default) or `soft` |

`forcing` is one of `non_forcing`, `one_round`, `game_forcing`, `sign_off`,
`invitational` — exactly those five.

### `requires` — the HandConstraint

```yaml
requires:
  hcp: [12, 15]                       # closed interval
  suits: { S: [5, 13], H: [0, 2] }
  evals: { ltc: [0, 6], controls: [5, 12] }
  features: [ ... ]
  shapes: [ "4441", "5+332" ]
  any_of: [ {...}, {...} ]            # disjunction of constraints
  all_of: [ {...} ]
  not: { ... }
  balanced: true                      # sugar for evals: {balanced: [1,1]}
  semi_balanced: true
```

**Evaluators available to `evals:`** (a suit-parametrised one takes the suit
from the rule's own template var, e.g. `suit_length` is addressed through
`suits:`; the rest are plain numbers):

```
aces  adjusted_hcp  balanced  control_in  controls  dist_points  good_suit
hcp  is_partner_suit  is_their_suit  is_unbid_suit  keycards  kings
longest_suit_length  lott_total_trumps  ltc  max_their_suit_length
partner_shown_length  partner_shown_max  quick_tricks  quick_tricks_outside
rule_of_15  rule_of_20  rule_of_26  rule_of_26_sharp  semi_balanced
shortness_points  singleton  singleton_or_void  standing_suit_length  stopper
stoppers  suit_diff  suit_length  suit_quality  their_bidders  their_fit
their_shown_hcp  three_of_top5  top_honour  total_points  trump_queen
two_of_top3  void  wasted_in_partner_shortness  weakest_their_stopper
weakest_unbid_length  weakest_unshown_stopper  worthless_doubleton
```

Known evaluator traps, all measured:

* `weakest_their_stopper` has **no sharp tolerance**, so a `[0.9, 9]` gate does
  not gate — no stopper at all scores 0.835.  Do not lean a new rule on it.
* `is_unbid_suit` likewise: a suit that IS bid still scores 0.8 against `[1,1]`.
* `suit_length(their)` resolves to **LHO's** suit, not "their first suit".
  Use `standing_suit_length` when you mean the suit of the standing bid.
* After a 2C opening partner's shown minimum is **zero**, so every
  `rule_of_26_sharp >= 31` gate is unreachable in the 2C tree.

### `when:` — auction conditions (NOT hand facts)

```
opening_seat: [1,2,3,4]      passed_hand: bool          we_vulnerable: bool
they_vulnerable: bool        we_hold_contract: bool     partner_suit: S
unbid_suit: S                cheapest_in_suit: bool     side_has_acted: bool
their_last_bid_suit: bool    we_bid_last: bool          i_have_acted: bool
standing_bid_level: [3,4]    standing_bid_strain: [H,S] my_suit: S
partner_last_suit: S         i_preempted: bool          my_last_call_was_double: bool
partner_last_call_was_double: bool                      partner_has_acted: bool
is_competitive: bool         partner_limited: bool      config: {...}
```

A `when:` gate rules a call OUT structurally.  A soft `requires:` feature only
discourages it.  Use `when:` for anything the auction decides.

## The scoring model — read this twice

Candidates are scored by **soft Gaussian fit** against `requires`.  Then:

> the fast path is **fit >= 0.9 then max priority**; below that the **blended
> score** decides; **every generic context ends in a catch-all pass at fit
> 1.00**, so **any hole in a ladder is a PASS by construction**.

Consequences you must design around:

1. A rule that misses its own gate by one point can still WIN if nothing else
   fits ("the soft-miss lottery").  Only some evaluators have sharp tolerance.
2. `all-pass` / `fallback` in a dossier names a **starved seat**, not a bad rule.
3. Priority only breaks ties among rules that already fit.  Placing a rung
   high enough to outrank a MORE DESCRIPTIVE call below it is the single most
   expensive mistake made in this project.

## How to VERIFY a claim before you write it down

```bash
cd /home/user/BridgeBidder
python3 - <<'PY'
import sys; sys.path.insert(0, "tools/roundkit")
from repro import rank, ask, context_at
from sweep import deciding_rule

hand   = "AQ52.KJ4.QT9.KJ7"      # Spades.Hearts.Diamonds.Clubs
dealer, vul, seat = "N", "None", "N"
calls  = ["P", "1H", "P"]        # the auction so far, FROM THE DEALER

print(ask(hand, dealer, vul, seat, calls)["chosen_call"])
print(context_at(hand, dealer, vul, seat, calls))     # which contexts are live
cands = rank(hand, dealer, vul, seat, calls, top=14)
for c in cands:
    print(f"{c['call']:>4} {c['rule']:<34} fit={c['fit']:.3f} "
          f"score={c['score']:.3f} prio={c['prio']}")
print("DECIDED BY:", deciding_rule(cands)["rule"])
PY
```

`deciding_rule()` is the rule that ACTUALLY chose the call.  The `rule` field
in a match row and `explanation.source_rule_id` are the **primary reading** —
the highest-priority rule producing the same call — and reading them as the
chooser has produced false findings twice.

Whole-corpus denominators, so a rule is never accused on its losers alone:

```python
from repro import rule_summary, fires_summary
print(fires_summary("reports/r18_before.jsonl", "uc_nt3"))   # every table it fired on
```
