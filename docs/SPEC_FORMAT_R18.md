# The spec format the implementer applies

Write your batch as ONE file, `docs/specs/<name>.spec`, in this format:

```
#== RULES <existing_context_id>
      - id: some_rule_$M
        call: 3$M
        priority: 41
        when: { partner_suit: $M }
        requires: { suits: { $M: [4, 13] } }
        shows: "..."
        establishes: { forcing: non_forcing, agreed_suit: $M }
#== CONTEXT
  - id: some_new_context
    description: "..."
    expand: { M: [H, S] }
    pattern: "... - ?"
    rules:
      - id: snc_pass_$M
        call: P
        priority: 20
        requires: {}
        shows: "..."
        establishes: { forcing: non_forcing }
```

Rules are indented SIX spaces, contexts TWO — exactly as in
`src/bridgebidder/systems/two_over_one.yaml`. `tools/roundkit/addrules.py`
applies the whole file in one transaction and refuses to write anything if any
assert fails.

**Non-negotiable, every one of these has cost a cycle:**

* a template var must END a rule id (`id: foo_$M`, never `id: foo_$M_bar`);
* `call: $L$X` does not expand — write the level out;
* `expand:` over a variable that does not appear in the `pattern` emits N
  identical contexts and only the first is ever used;
* `cheapest_in_suit: true` on a rung that describes a JUMP makes it
  unreachable — the file already has three such dead rules;
* a `requires: {}` rung fits **1.00** and eats every rung below its priority,
  so it belongs at the BOTTOM of its ladder;
* a new context appended at the end of the file cannot take a call from an
  equally specific context that already exists (file order breaks the tie),
  and `pattern: "... - ?"` is the least specific pattern in the file — that is
  how you get the superset property structurally;
* but a context placed after a generic one **cannot add a rung for a call the
  generic already defines**, because `covered` is built most-specific-first;
* every force, ask and invitation ships with the seat that ANSWERS it, in the
  same spec.

Ids must be unique against the whole existing file. Check with:

```bash
grep -c "id: YOUR_ID" src/bridgebidder/systems/two_over_one.yaml
```
