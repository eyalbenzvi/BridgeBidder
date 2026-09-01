"""Rule-patch service: read, modify, and write the bidding system YAML.

Patches are applied in-memory for preview/replay and optionally written to disk
when a proposal is accepted.
"""

from __future__ import annotations

import copy
import difflib
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
    """Write back to two_over_one.yaml.

    Kept for callers that already hold a plain dict.  Prefer
    `apply_and_write`, which preserves the file's comments.
    """
    with open(YAML_PATH, "w", encoding="utf-8") as fh:
        yaml.dump(yaml_data, fh, allow_unicode=True, sort_keys=False)


def _port_change(original: str, base: str, patched: str) -> str:
    """Apply the base->patched difference onto `original`.

    `base` and `patched` are two dumps of the same document, so they differ
    only by the patch.  `original` and `base` differ only by the formatting
    the dumper does not reproduce.  Rewriting just the hunks keeps the rest of
    the file exactly as its author wrote it, so an accepted proposal reviews
    as the handful of lines it really changed.

    If a hunk cannot be located in the original -- the patch landed inside a
    region the dumper reformatted -- this returns the full dump rather than
    guessing.  A correct file with an ugly diff beats a mangled one.
    """
    o = original.splitlines(keepends=True)
    b = base.splitlines(keepends=True)
    p = patched.splitlines(keepends=True)

    # base line -> original line, for the lines the two agree on
    b2o: dict[int, int] = {}
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(
            None, b, o, autojunk=False).get_opcodes():
        if tag == "equal":
            for k in range(i2 - i1):
                b2o[i1 + k] = j1 + k
    b2o[len(b)] = len(o)

    edits: list[tuple[int, int, list[str]]] = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(
            None, b, p, autojunk=False).get_opcodes():
        if tag == "equal":
            continue
        # A hunk boundary often lands on a line the dumper reformatted, which
        # has no counterpart in the original.  Widen outwards to the nearest
        # lines the two texts do agree on, and rewrite that slightly larger
        # region instead -- a few reformatted lines around the change, rather
        # than the whole file.
        lo, hi = i1, i2
        while lo > 0 and lo not in b2o:
            lo -= 1
        while hi < len(b) and hi not in b2o:
            hi += 1
        if lo not in b2o or hi not in b2o:
            return patched
        edits.append((b2o[lo], b2o[hi], p[j1 - (i1 - lo):j2 + (hi - i2)]))

    out = list(o)
    last_start = len(out)
    for start, end, lines in reversed(edits):
        if end > last_start:                  # widened hunks collided
            return patched
        out[start:end] = lines
        last_start = start
    return "".join(out)


def apply_and_write(patches: list[dict]) -> dict:
    """Apply patches to the rulebook on disk, keeping the file readable.

    `two_over_one.yaml` is a hand-written, hand-formatted document: 16,683
    lines of which 2,230 are comments explaining why each rule is the way it
    is.  PyYAML cannot round-trip any of that.  Loading and re-dumping the
    file through `yaml.safe_load`/`yaml.dump` deletes every comment and
    reflows the rest to 32,395 lines -- so accepting one three-line proposal
    would land as a whole-file rewrite with the documentation gone and a diff
    nobody could review.  That is not a patch, it is a data-loss event with an
    innocuous button on it.

    `ruamel.yaml` in round-trip mode preserves comments, key order and most
    formatting, so an accepted proposal shows up as the few lines it actually
    changed.  It is a hard requirement rather than a nicety: without it this
    refuses to write, because silently shipping the destructive version is
    the worse failure.

    Returns {"changed_lines": int, "total_lines": int}.
    """
    try:
        from ruamel.yaml import YAML
    except ImportError as exc:
        raise RuntimeError(
            "Writing the rulebook needs ruamel.yaml (pip install ruamel.yaml). "
            "Without it the whole file is reformatted and every comment in it "
            "is lost, so this refuses to write.") from exc

    import io

    rt = YAML()
    rt.preserve_quotes = True
    rt.width = 4096                 # do not re-wrap long `shows` lines
    rt.indent(mapping=2, sequence=4, offset=2)

    def dump(obj) -> str:
        buf = io.StringIO()
        rt.dump(obj, buf)
        return buf.getvalue()

    before = YAML_PATH.read_text(encoding="utf-8")
    doc = rt.load(io.StringIO(before))

    # Dump the document BEFORE patching as well.  ruamel keeps comments but
    # still normalises small things the file writes by hand -- `{ a: 1 }`
    # comes back as `{a: 1}` -- and on a 16,000-line rulebook that alone is a
    # 9,700-line diff wrapped around a two-line change, which no reviewer can
    # read.  Both dumps carry that normalisation identically, so the
    # difference between them is exactly the patch, and porting it onto the
    # original text leaves every untouched line byte-for-byte as it was.
    base = dump(doc)
    patched = apply_patches_to_yaml(doc, patches, inplace=True)
    parse_system(patched)                     # fail before touching the file
    after = _port_change(before, base, dump(patched))

    kept = sum(1 for line in after.splitlines() if line.strip().startswith("#"))
    had = sum(1 for line in before.splitlines() if line.strip().startswith("#"))
    if had and kept < had * 0.9:
        raise RuntimeError(
            f"refusing to write: the rewrite would drop {had - kept} of {had} "
            f"comment lines")

    tmp = YAML_PATH.with_suffix(".yaml.new")
    tmp.write_text(after, encoding="utf-8")
    tmp.replace(YAML_PATH)                    # atomic: never a half-written rulebook

    diff = sum(1 for line in difflib.unified_diff(
        before.splitlines(), after.splitlines(), n=0)
        if line[:1] in "+-" and not line.startswith(("---", "+++")))
    return {"changed_lines": diff, "total_lines": len(after.splitlines())}


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


def _del_nested(d: dict, dotted_path: str) -> None:
    """Remove a dotted key path if present, pruning containers left empty."""
    parts = dotted_path.split(".")
    stack = [d]
    for part in parts[:-1]:
        nxt = stack[-1].get(part)
        if not isinstance(nxt, dict):
            return
        stack.append(nxt)
    stack[-1].pop(parts[-1], None)
    for parent, key in zip(reversed(stack[:-1]), reversed(parts[:-1])):
        if parent.get(key) == {}:
            parent.pop(key, None)


# ---------------------------------------------------------------------------
# The editor's vocabulary -> the DSL's
# ---------------------------------------------------------------------------
#
# The rule editor speaks in what the user sees: an HCP range, four suit
# lengths, a priority, a shows line, a forcing status -- and it reports edits
# as a diff, {field: {before, after}}, because that is what it needs in order
# to show what changed.  The YAML speaks in `requires.hcp`, `requires.suits.H`,
# `establishes.forcing`.  Nothing translated between them, so every one of the
# three editor buttons failed at the preview call: modify_rule died on a
# missing 'field', add_exception on a missing 'not_block', add_rule on
# "Unknown rule keys: ['constraint', 'forcing_status']".
#
# The translation belongs here rather than in the browser: a stored proposal
# should record what the user meant, so it can still be read and re-applied
# after the YAML's shape has moved on.

FORCING_STATUSES = ("game_forcing", "one_round", "invitational",
                    "non_forcing", "sign_off")
FULL_HCP = [0, 37]
FULL_SUIT = [0, 13]
SUIT_KEYS = ("S", "H", "D", "C")

_UI_FIELD_PATHS = {
    "hcp": "requires.hcp",
    "shows": "shows",
    "priority": "priority",
    "forcing_status": "establishes.forcing",
}


def _after(value: Any) -> Any:
    """Unwrap the editor's {before, after} diff entries."""
    if isinstance(value, dict) and "after" in value:
        return value["after"]
    return value


def _check_forcing(status: Any) -> str:
    if status not in FORCING_STATUSES:
        raise ValueError(
            f"Unknown forcing status {status!r}; expected one of "
            f"{', '.join(FORCING_STATUSES)}")
    return status


def ui_changes_to_ops(changes: dict) -> list[tuple[str, Any]]:
    """Editor diff -> [(dotted YAML path, new value)].

    A suit reset to its full range is a deletion, not an assignment: writing
    `S: [0, 13]` back into `requires` states a constraint that constrains
    nothing, and it then shows up in the editor next time as though the rule
    had always cared about spades.
    """
    ops: list[tuple[str, Any]] = []
    for key, raw in changes.items():
        value = _after(raw)
        if key in _UI_FIELD_PATHS:
            if key == "forcing_status":
                value = _check_forcing(value)
            ops.append((_UI_FIELD_PATHS[key], value))
        elif key.startswith("length_"):
            suit = key[len("length_"):].upper()
            if suit not in SUIT_KEYS:
                raise ValueError(f"Bad suit in change key {key!r}")
            ops.append((f"requires.suits.{suit}",
                        None if list(value) == FULL_SUIT else list(value)))
        else:
            raise ValueError(f"Unknown editor field {key!r}")
    return ops


def ui_constraint_to_dsl(constraint: dict, *, what: str) -> dict:
    """Editor constraint -> a DSL `requires` block, minus the no-op bounds.

    The form always submits all four suits and a full HCP range, whether or
    not the user touched them.  Carried through literally into an exception
    that becomes `not: {hcp: [0,37], suits: {S: [0,13], ...}}` -- which every
    hand satisfies, so the exception denies the rule to everyone.  Anything
    still at its full range is therefore dropped, and a constraint that says
    nothing at all is refused rather than silently written.
    """
    out: dict = {}
    hcp = constraint.get("hcp")
    if hcp and list(hcp) != FULL_HCP:
        out["hcp"] = list(hcp)
    suits = {}
    for key, rng in (constraint.get("lengths") or constraint.get("suits") or {}).items():
        if rng and list(rng) != FULL_SUIT:
            suits[str(key).upper()] = list(rng)
    if suits:
        out["suits"] = suits
    if not out:
        raise ValueError(
            f"This {what} constrains nothing — every hand would match it. "
            f"Narrow the HCP range or a suit length first.")
    return out


def _merge_exception(requires: dict, block: dict) -> None:
    """Add `block` as a denied shape, accumulating with any already there.

    The DSL key is `not`, and it takes one constraint.  Two exceptions are
    combined as `not: {any_of: [...]}` -- "not A and not B" is exactly "not
    (A or B)".  The previous code wrote `not_` and turned a second exception
    into a list, neither of which the DSL accepts.
    """
    existing = requires.get("not")
    if existing is None:
        requires["not"] = block
    elif isinstance(existing, dict) and set(existing) == {"any_of"}:
        existing["any_of"].append(block)
    else:
        requires["not"] = {"any_of": [existing, block]}


def _fresh_rule_id(ctx: dict, base: str) -> str:
    taken = {r.get("id") for r in ctx.get("rules", []) or []}
    stem = "".join(ch if ch.isalnum() else "_" for ch in base).strip("_")
    candidate = stem
    n = 2
    while candidate in taken:
        candidate = f"{stem}_{n}"
        n += 1
    return candidate


def _get_nested(d: dict, dotted_path: str) -> Any:
    parts = dotted_path.split(".")
    for part in parts:
        if not isinstance(d, dict):
            raise KeyError(dotted_path)
        d = d[part]
    return d


def apply_patches_to_yaml(yaml_data: dict, patches: list[dict],
                          inplace: bool = False) -> dict:
    """Apply a list of patch objects to the raw YAML dict.

    Returns a deep-copied modified version unless `inplace` is set.

    `inplace` exists for the comment-preserving write path.  ruamel's
    CommentedMap carries its comments in side attributes that `copy.deepcopy`
    does not reproduce -- deep-copying the rulebook loses 244 of its 2,230
    comment lines, silently -- so that path loads a fresh document and lets
    the patches mutate it directly.

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
    data = yaml_data if inplace else copy.deepcopy(yaml_data)

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
            if "changes" in patch:               # the editor's diff shape
                ops = ui_changes_to_ops(patch["changes"])
            else:                                # explicit field/after
                ops = [(patch["field"], patch["after"])]
            for path, value in ops:
                if value is None:
                    _del_nested(rule, path)
                else:
                    _set_nested(rule, path, value)

        elif ptype == "add_exception":
            if ctx is None:
                raise ValueError(f"Context {ctx_id!r} not found")
            rule = _find_rule(ctx, patch["rule_id"])
            if rule is None:
                raise ValueError(f"Rule {patch['rule_id']!r} not found in context {ctx_id!r}")
            block = (patch["not_block"] if "not_block" in patch
                     else ui_constraint_to_dsl(patch["constraint"], what="exception"))
            _merge_exception(rule.setdefault("requires", {}), block)

        elif ptype == "add_rule":
            if ctx is None:
                raise ValueError(f"Context {ctx_id!r} not found")
            rules: list = ctx.setdefault("rules", [])
            src = dict(patch["rule"])
            if "constraint" in src or "forcing_status" in src:
                # the editor's shape: a call, a priority, a shows line and a
                # constraint, which is not what BidRule.from_dict reads
                call = str(src.get("call", ""))
                new_rule: dict = {
                    "id": src.get("id") or _fresh_rule_id(
                        ctx, f"{ctx_id}_ui_{call}"),
                    "call": call,
                    "priority": src.get("priority", 50),
                    "shows": src.get("shows", ""),
                    "requires": ui_constraint_to_dsl(
                        src.get("constraint") or {}, what="rule"),
                }
                forcing = src.get("forcing_status")
                if forcing:
                    new_rule["establishes"] = {"forcing": _check_forcing(forcing)}
            else:
                new_rule = src
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
