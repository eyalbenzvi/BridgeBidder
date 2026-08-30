# Plan: how to add thousands of specific rules

*A proposal, for decision.  Nothing here is started.*

---

## 0. What the last sixteen rounds got wrong, in one paragraph

The loop has been: play 1,000 boards, find a defect, change a rung, measure,
keep if the number improved.  Round 17 measured that loop and it is exhausted.
Every single-rung intervention it made was indistinguishable from zero — the
one rung whose gate replicated out of sample measured **-42 IMPs, t = -0.70**;
a 28-rule closed conversation measured **-41, t = -0.57**; and round 14's +51,
the largest gain since round 10 and the origin of the -474 bar, is **t = 1.73,
CI [-5, +111]**.  The reason is not that the fixes were bad.  It is that a
2,344-rule system is **under-specified**, and a rung added to a subject with
no vocabulary has nothing to attach to.  The unit of work has to change from
*a fix* to *a subject*, and the volume has to go up by a factor of three.

---

## 1. The target, quantified

| | today | target |
|---|---|---|
| contexts | 517 | 1,500 - 2,500 |
| rules | 2,344 | **7,000 - 12,000** |
| rules bidding at the 5 level | 55 | several hundred |
| rules bidding at the 7 level | 0 | dozens |
| trial bids / serious 3NT / mini-splinters / fit jumps / control raises | **0 each** | present |

### The reframe that makes this tractable

**Thousands of rules are hundreds of ideas.**  The DSL already has `expand`
and `expand_pairs`: one authored idea becomes one rule per (suit × seat ×
level × competitive-or-not × vulnerability) it applies to.  Today's 2,344
rules come from far fewer distinct ideas.  So the real programme is

> **author 400-800 *agreements*, and let templating turn them into 7,000-12,000 rules.**

That is a human-scale project.  It is not a human-scale project if each rule
is written by hand.

---

## 2. Five ways to supply rules, ranked by yield per unit of effort

### A. A convention-card audit — cheapest, do first
Take the documented 2/1 Game Forcing convention card and the standard
continuations, and enumerate every agreement on it.  Mark each **present /
partial / absent** in the file.  This is a checklist, not a judgement call, so
it does not depend on anybody's bridge intuition — including mine, which is
the failure mode you just named.

Round 17 ran a five-line version of this by grepping rule ids and found
**trial bids, serious/frivolous 3NT, mini-splinters, fit-showing jumps and
control-showing raises are each at exactly zero rules.**  A full audit will
find dozens more.

*Yield:* the backlog itself, ranked, in a day.  *Cost:* ~1 day.
*Needs an expert?* Only to confirm the list, not to build it.

### B. Distil BEN into rules — highest volume, fully automatic
BEN is a policy we can query at any position, it is trained on expert
auctions, and round 17 made its answers **cached and free**.  So:

1. enumerate auction prefixes that actually occur (from the 12,000-board pool
   plus systematic enumeration of short prefixes);
2. for each, deal 2,000 consistent hands and ask BEN what it bids;
3. per (position, call), fit a **shallow decision tree over the existing
   evaluator vocabulary** — hcp, controls, ltc, suit lengths, shortness,
   stoppers, fit;
4. translate each leaf into a `requires` block and a one-sentence `shows`.

Cost per context: ~2,000 queries ≈ 6 s.  1,500 contexts ≈ **2.5 hours of
compute.**  The output is in the engine's own vocabulary, so it stays
explicable.

**The honest ceiling: distilling BEN converges to BEN, not past it.**  That is
worth **+474 IMPs** from where we stand, and nothing more.  Treat it as the
floor of the programme, not the goal.

### C. Mine real expert auctions — better than B if the data exists
BEN is a lossy compression of a human expert corpus.  Raw expert auctions
(vugraph archives, championship hand records, published system notes) would
let us mine the agreements directly, without BEN's compression and without its
errors.  **Open question: what is actually obtainable and under what licence.**
Worth a half-day of investigation before committing to B alone.

### D. Simulation per case — for positions where convention is silent
Generalise round 17's `slamprobe.py`, which already works: at a position, for
each candidate call, roll the auction out with **our engine in our seats and
BEN in the opponents'**, score double-dummy, and take the IMP-best call.  ~90
ms per rollout.

Use it where A/B/C leave a gap, and to *correct* distilled rules where BEN is
demonstrably wrong.  This is the only mechanism that can beat BEN.

Two known hazards, both already documented: double-dummy rewards a lie whose
partner is misled favourably, and a substituted call is read by partner with
the *unmodified* system, so it measures unilateral deviation.  The fix for
both is **iterated best response** (E).

### E. Iterate to a partnership equilibrium — the finisher
Fix partner's system, optimise my seat, swap, repeat.  This converts
"unilateral deviation" into "partnership agreement" and is how the
answering seats stop being an afterthought.  Expensive; do it last, on a
system that is already dense.

### F. Human experts — spend them on *review*, not authoring
A strong player authoring from scratch produces perhaps 20-40 agreements a
day.  The same player *reviewing* generated rules can clear several hundred.
So: use A to make the checklist, B/C/D to generate, and experts to **accept,
reject or amend** — with a hard requirement that every rejection is recorded
with its reason, so the generator learns.

*Estimated expert budget for a full pass:* **10-20 expert-days.**

---

## 3. The pipeline

```
convention-card audit  ─┐
BEN distillation       ─┼─→  agreement spec  ─→  templated YAML  ─→  gates
expert-corpus mining   ─┤     (400-800)          (7k-12k rules)
simulation per case    ─┘
```

**Gate 1 — mechanical, per rule, seconds.**  Loads; ids unique; template vars
end ids; `lint_system.py` finding count does not rise; the rule fires at least
once in the 12,000-board pool (a rule that never fires is not a rule).

**Gate 2 — structural, per subject.**  Every force, ask and invitation ships
with the seat that answers it.  Round 17 measured what happens otherwise: a
cue bid with no answering seat costs **-9.8 IMPs a seat**, and that number was
measuring an empty seat, not a bad call.  This must be an automated invariant,
not a discipline note.

**Gate 3 — agreement with the corpus, per subject, minutes.**  On the pool:
does the new subject reduce GUESSES (nothing fits ≥ 0.9) and NOTHING (code
fallback)?  Does BEN agreement go up?  These are cheap proxies, computed
without playing a single new board.

**Gate 4 — IMPs, per subject, ~8 minutes.**  `roundkit/screen.py` on the
12,000-board pool: exact paired delta, t, 95% bootstrap CI.  **A subject is
big enough to measure; a rung never was.**  This is the one asset round 17
actually shipped and it is what makes bulk authoring safe.

**Gate 5 — the whole build.**  Before/after on fresh seeds, reported once.

---

## 4. Three structural repairs that must land before bulk authoring

Without these, adding thousands of rules will silently *subtract* behaviour.

1. **Make the code fallback unconditional.**  Today `covered` is built without
   consulting fit, so *adding a rung deletes the generic fallback for that
   call in every seat the rung's `when` reaches*.  At 7,000 rules this trap
   fires constantly.  Prototyped; round 17 measured its blast radius at **216
   changed decisions per 1,000 boards** with both halves applied.  Unmeasured
   in IMPs — that is a one-hour job with the screen.
2. **A shadowing invariant.**  Automated check that no new context reduces
   another's coverage, replacing the "carry the shadowed rule's gates
   verbatim" discipline note that has failed repeatedly.
3. **Priority conflict detection.**  Round 17 broke two locked scenarios with
   one rung because a new rule outranked the rungs *below* it.  At scale this
   needs a tool, not a reviewer.

---

## 5. Three candidate programmes

| | **Conservative** | **Balanced (recommended)** | **Aggressive** |
|---|---|---|---|
| supply | A + F | A + B + D + F | A + B + C + D + E + F |
| new rules | ~1,500 | ~5,000 | ~10,000 |
| expert days | 15-25 | 10-20 (review only) | 20-40 |
| compute | trivial | ~1 day | ~1 week |
| ceiling | limited by expert throughput | **BEN parity, then past it via D** | past BEN |
| risk | slow; may not reach density | distillation inherits BEN's errors | large blast radius, hard to attribute |
| first measurable result | 3-4 weeks | **~1 week** | 3-4 weeks |

**Why I recommend Balanced.**  A gives a ranked backlog in a day and needs no
bridge judgement from me.  B is nearly free and closes the gap to BEN, which
is worth the entire remaining deficit.  D is the only route past BEN and it
already works.  Experts are spent where they are most efficient — reviewing.
E is deferred until there is a dense system for it to converge on.

---

## 6. What I need you to decide

1. **Programme:** conservative, balanced, or aggressive?
2. **BEN's parity ceiling:** is "reach BEN, then beat it with simulation" an
   acceptable first target, or do you want to skip distillation and go
   straight to expert-plus-simulation?
3. **Expert access:** do we have one, and for roughly how many days?  This
   decides whether experts author or only review.
4. **Expert-corpus data:** should I spend half a day finding out what raw
   expert auction data is obtainable and under what licence, before we commit
   to distilling BEN?
5. **Order:** land the three structural repairs first (my recommendation, ~1
   day), or start generating immediately and repair in parallel?
6. **Explainability:** the project rule has been "never trade explainability
   for score".  Distilled rules are decision-tree leaves translated into the
   existing evaluator vocabulary — readable, but not authored by a human.
   Is that acceptable, and does an expert have to sign off on each one?

---

## 7. What round 17 leaves behind that this plan uses

* `roundkit/screen.py` — exact paired delta, t and CI, at 1/5 the cost of a
  match; verified against a full run to the IMP.  **Gate 4.**
* `ben_cache.py` — BEN memoised; a cached replay never loads the model.
  **Makes B affordable.**
* `roundkit/slamprobe.py` — counterfactual rollout with BEN in the opponents'
  seats, ~90 ms.  **Is D, already working.**
* `roundkit/cfr.py` — per-decision regret, same machinery, unrun.
* `roundkit/coverage.py` — the KNOWS / GUESSES / NOTHING bucketing that
  produces the ranked backlog.  **Written, never run — Gate 3.**
* A 12,000-board cached pool whose seeds have never been a decision rule.
