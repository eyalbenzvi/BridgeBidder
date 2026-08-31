"""Rule-patch service: read, modify, and write the bidding system YAML.

Patches are applied in-memory for preview/replay and optionally written to disk
when a proposal is accepted.
"""

from __future__ import annotations

import copy
from pathlib import Path
from typing import Any

import yaml

from bridgebidder.system.dsl import parse_system, BiddingSystem

YAML_PATH: Path = (
    Path(__file__).parents[4] / "src" / "bridgebidder" / "systems" / "two_over_one.yaml"
)


# ---------------------------------------------------------------------------
# YAML I/O
# ---------------------------------------------------------------------------


def load_system_yaml() -> dict:
    """Load two_over_one.yaml as a raw dict."""
    with open(YAML_PATH, "r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def write_system_yaml(yaml_data: dict) -> None:
    """Write back to two_over_one.yaml."""
    with open(YAML_PATH, "w", encoding="utf-8") as fh:
        yaml.dump(yaml_data, fh, allow_unicode=True, sort_keys=False)


# ---------------------------------------------------------------------------
# Patch application
# ---------------------------------------------------------------------------


def _find_context(yaml_data: dict, context_id: str) -> dict | None:
    for ctx in yaml_data.get("contexts", []):
        if ctx.get("id") == context_id:
            return ctx
    return None


def _find_rule(ctx: dict, rule_id: str) -> dict | None:
    for rule in ctx.get("rules", []):
        if rule.get("id") == rule_id:
            return rule
    return None


def _set_nested(d: dict, dotted_path: str, value: Any) -> None:
    """Set a value at a dotted key path, creating intermediate dicts as needed."""
    parts = dotted_path.split(".")
    for part in parts[:-1]:
        if part not in d or not isinstance(d[part], dict):
            d[part] = {}
        d = d[part]
    d[parts[-1]] = value


def _get_nested(d: dict, dotted_path: str) -> Any:
    parts = dotted_path.split(".")
    for part in parts:
        if not isinstance(d, dict):
            raise KeyError(dotted_path)
        d = d[part]
    return d


def apply_patches_to_yaml(yaml_data: dict, patches: list[dict]) -> dict:
    """Apply a list of patch objects to the raw YAML dict.

    Returns a deep-copied modified version (does NOT mutate the input).

    Supported patch types
    ----------------------
    modify_rule
        {"type": "modify_rule", "context_id": str, "rule_id": str,
         "field": str, "after": value}
        ``field`` is a dotted path such as "requires.hcp", "priority",
        "shows", or "requires.suits.H".

    add_exception
        {"type": "add_exception", "context_id": str, "rule_id": str,
         "not_block": dict}
        Adds a ``not_`` sub-constraint to the rule's ``requires`` dict.

    add_rule
        {"type": "add_rule", "context_id": str,
         "after_rule_id": str | None, "rule": dict}
        Inserts a new rule dict into the context's rules list, optionally
        after a named rule (appended to end if after_rule_id is None or not
        found).
    """
    data = copy.deepcopy(yaml_data)

    for patch in patches:
        ptype = patch.get("type")
        ctx_id = patch.get("context_id")
        ctx = _find_context(data, ctx_id) if ctx_id else None

        if ptype == "modify_rule":
            if ctx is None:
                raise ValueError(f"Context {ctx_id!r} not found")
            rule = _find_rule(ctx, patch["rule_id"])
            if rule is None:
                raise ValueError(f"Rule {patch['rule_id']!r} not found in context {ctx_id!r}")
            _set_nested(rule, patch["field"], patch["after"])

        elif ptype == "add_exception":
            if ctx is None:
                raise ValueError(f"Context {ctx_id!r} not found")
            rule = _find_rule(ctx, patch["rule_id"])
            if rule is None:
                raise ValueError(f"Rule {patch['rule_id']!r} not found in context {ctx_id!r}")
            requires = rule.setdefault("requires", {})
            not_block = patch["not_block"]
            # Merge into an existing not_ list or create one.
            existing = requires.get("not_")
            if existing is None:
                requires["not_"] = not_block
            elif isinstance(existing, list):
                existing.append(not_block)
            else:
                # existing is a single dict — convert to list
                requires["not_"] = [existing, not_block]

        elif ptype == "add_rule":
            if ctx is None:
                raise ValueError(f"Context {ctx_id!r} not found")
            rules: list = ctx.setdefault("rules", [])
            new_rule = patch["rule"]
            after_id = patch.get("after_rule_id")
            if after_id:
                for i, r in enumerate(rules):
                    if r.get("id") == after_id:
                        rules.insert(i + 1, new_rule)
                        break
                else:
                    rules.append(new_rule)
            else:
                rules.append(new_rule)

        else:
            raise ValueError(f"Unknown patch type: {ptype!r}")

    return data


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------


def preview_patch(patch: dict) -> dict:
    """Validate a single patch without writing to disk.

    Returns {"ok": True} or {"ok": False, "error": str}.
    """
    try:
        yaml_data = load_system_yaml()
        patched = apply_patches_to_yaml(yaml_data, [patch])
        # Try parsing the result to catch DSL errors.
        parse_system(patched)
        return {"ok": True}
    except Exception as exc:
        return {"ok": False, "error": str(exc)}


# ---------------------------------------------------------------------------
# In-memory helpers
# ---------------------------------------------------------------------------


def get_system_for_patches(patches: list[dict]) -> BiddingSystem:
    """Apply patches in-memory and return a parsed BiddingSystem (no disk write)."""
    yaml_data = load_system_yaml()
    patched = apply_patches_to_yaml(yaml_data, patches)
    return parse_system(patched)


def context_rule_ids(context_id: str, system: BiddingSystem | None = None) -> set[str]:
    """Every concrete rule id belonging to `context_id`, template variants included.

    A context declared with `expand:` becomes one concrete context per
    combination -- `resp_1M` turns into `resp_1M[H]` and `resp_1M[S]` -- so a
    patch naming the raw context has to match all of its expansions.
    """
    system = system or parse_system(load_system_yaml())
    out: set[str] = set()
    for ctx in system.contexts:
        if ctx.id == context_id or ctx.id.startswith(f"{context_id}["):
            out.update(r.id for r in ctx.rules)
    return out


def get_touched_rule_ids(patches: list[dict]) -> set[str]:
    """Rule ids whose presence on a board means the board must be replayed.

    The corpus pre-check skips any board none of whose recorded calls came
    from one of these rules, so an id missing here is a board silently scored
    as unchanged.

    `add_rule` is the case that needs care.  A brand-new rule has an id that
    appears on no board in the pool -- the pool predates it -- so matching on
    the new id alone marks *nothing* as touched and the test reports a
    confident "0 boards changed" for a rule that may fire everywhere.  What a
    new rule can actually do is win a decision away from whatever rule wins it
    today, and that can only happen where its context is live; so the whole
    context is what has to be replayed.
    """
    ids: set[str] = set()
    system: BiddingSystem | None = None
    for patch in patches:
        ptype = patch.get("type")
        if ptype in ("modify_rule", "add_exception"):
            rid = patch.get("rule_id")
            if rid:
                ids.add(rid)
        elif ptype == "add_rule":
            ctx_id = patch.get("context_id")
            if ctx_id:
                if system is None:
                    system = parse_system(load_system_yaml())
                ids |= context_rule_ids(ctx_id, system)
            rid = (patch.get("rule") or {}).get("id")
            if rid:
                ids.add(rid)
    return ids


def touches_fallback(patches: list[dict]) -> bool:
    """Whether any patch could fire where no rule fires today.

    A board records `rule: null` for a call the engine made with no matching
    rule.  Adding a rule can capture exactly those positions, and they match no
    id at all, so the pre-check has to let them through explicitly.
    """
    return any(p.get("type") == "add_rule" for p in patches)
