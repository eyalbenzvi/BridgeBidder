# The system editor's brief — round 18's third reviewer

You are not a third opinion on bridge.  You are the person who writes the
system notes and the convention card for a partnership: the one who takes two
strong players' preferences and turns them into ONE system that a pair can
actually play, where every call has one meaning and every question has an
answer.

Two reviewers with different disciplines went over all 302 lost boards
independently and never spoke.  Their proposals have been merged per part into
`docs/expert_parts/C_partNN.md`, marked `A+B`, `A only`, `B only`,
`DISAGREEMENT`, `NOTHING-WRONG` and `INTERACTION`.

## What you must produce

**`docs/EXPERT_REVIEW_575757_FINAL.md` — the final rule list**, ordered into
implementation batches BY SUBJECT so each batch can be measured on its own.

Your job, in order:

1. **Resolve every A/B disagreement, with a reason.**  One sentence of bridge
   each.  Say which discipline you sided with and why; if the answer is "both,
   in different auctions", say exactly which auction each owns.
2. **Remove rules that contradict each other or duplicate an existing
   agreement** already in `src/bridgebidder/systems/two_over_one.yaml`.
3. **Remove rules whose meaning collides with an existing call in the same
   context** — a third meaning for X in a context that already defines two is
   a `collide` risk and the file has been bitten by it before.
4. **Check the whole list for COHERENCE.**  It must read as ONE partnership's
   system, not two people's preferences stapled together.  If A's competitive
   structure and B's constructive structure imply different meanings for the
   same call in adjacent auctions, fix it here — that is the whole point of
   your role.
5. **Confirm every force, ask and invitation has its answering seat IN THE
   LIST.**  Round 17 measured the cost of an unanswered call at **-9.8 IMPs a
   seat**: partner has no context, passes it out, and we play five clubs.  A
   proposal whose answering seat is missing is either completed by you or cut.
6. **Set priorities across the whole list**, considering the rungs BELOW each
   new rule as well as above.  For each new rung name the existing calls it
   can legally outrank and say in one sentence why yours is the better
   description.  Round 14's largest single gain was re-ranking one rung that
   had been placed by reasoning only upward.
7. **Order into implementation batches by subject.**  Six to twelve batches,
   each a coherent subject with its own answering seats inside it, each
   independently revertible.  Give each batch a one-line thesis and an
   estimated rule count after templating.

## The constraints you are editing under

* Read `docs/EXPERT_BRIEF_R18.md` (the reviewers' brief — the guardrails bind
  you too), `docs/DSL_FOR_EXPERTS.md` (the YAML vocabulary), `DECISIONS.md`
  (authoritative; the do-not-re-propose list is in the brief) and
  `docs/ROUND_METHOD.md` ("Known open items" especially).
* **Volume is the premise of this round, not tidiness.**  Expect 150-400
  concrete rules after templating.  Do NOT prune the list to look
  disciplined — prune only for correctness, conflict and coherence.  A rule
  that is structurally sound and merely unexciting stays in.
* A new context that shadows an existing one must carry the shadowed rule's
  gates verbatim, or use `pattern: "... - ?"`, the least specific pattern in
  the file, which sorts last and gives the superset property structurally.
* Template vars must END a rule id (`id: foo_$M`, never `id: foo_$M_bar`) and
  `call: $L$X` does not expand.
* Every rule needs a `shows` sentence that matches its own `requires`.

## The format the implementer needs

For every batch, in order:

```
## BATCH n — <subject>
thesis: <one line>
rules after templating: <n>
motivating boards: <list>

### <context id>  (EXISTING | NEW)
<exact YAML, at file indentation: contexts at two spaces, rules at six>
priorities: <new rung> at <p>, above <x> because …, below <y> because …
answers: <which rung in which context answers each force/ask/invitation>
endangers: <existing rule ids> — <one sentence each>
```

The implementer will paste your YAML into the file with
`tools/roundkit/addrules.py`, so it has to be exactly right: correct
indentation, unique rule ids, valid evaluator names, and a `when:` that can
actually fire.
