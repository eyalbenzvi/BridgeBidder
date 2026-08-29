"""Auction pattern matching for system contexts.

Pattern grammar (tokens separated by " - "):
  literal call        "1H", "P", "X", "XX", "2NT"
  alternation         "(1H|1S)", "1(H|S)", "(X|2C)"
  any single call     "*"
  any contract bid    "bid", optionally bounded: "bid<=3S", "bid<2H", "bid>=2C", "bid>1NT"
  any non-pass call   "act"  (bid, X or XX)
  prefix wildcard     "..." (only as the FIRST token; matches any calls, incl. none)
  decision point      "?"   (must be the LAST token)

Patterns are matched against the auction's calls AFTER stripping leading
passes (opening-seat information is carried separately in conditions).
A pattern of just "?" matches the start of the auction (opening position).
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from ..domain.calls import Call

_CMP_RE = re.compile(r"^(bid|act)\s*(<=|>=|<|>)?\s*([1-7](?:C|D|H|S|NT|N))?$")


def _expand_paren(token: str) -> list[str]:
    """Expand "1(H|S)" or "(1H|1S)" into alternatives."""
    m = re.match(r"^(.*)\(([^()]*)\)(.*)$", token)
    if not m:
        return [token]
    pre, alts, post = m.groups()
    out = []
    for alt in alts.split("|"):
        out.extend(_expand_paren(f"{pre}{alt.strip()}{post}"))
    return out


@dataclass(frozen=True)
class TokenMatcher:
    """Matches a single call string."""

    alternatives: tuple[str, ...]  # each: literal call str, or 'bid'/'act' with bound

    def matches(self, call_str: str) -> bool:
        call = Call.parse(call_str)
        for alt in self.alternatives:
            m = _CMP_RE.match(alt)
            if m:
                kind, op, bound = m.groups()
                if kind == "bid" and not call.is_bid:
                    continue
                if kind == "act" and call.is_pass:
                    continue
                if bound:
                    if not call.is_bid:
                        continue
                    b = Call.parse(bound)
                    idx, bidx = call.bid_index, b.bid_index
                    ok = {"<=": idx <= bidx, "<": idx < bidx, ">=": idx >= bidx, ">": idx > bidx}[op]
                    if not ok:
                        continue
                return True
            # literal
            if str(Call.parse(alt)) == str(call):
                return True
        return False


@dataclass(frozen=True)
class CompiledPattern:
    tokens: tuple[TokenMatcher, ...]
    open_prefix: bool  # starts with "..."
    raw: str

    @property
    def specificity(self) -> int:
        return (0 if self.open_prefix else 1000) + len(self.tokens)


def compile_pattern(pattern: str) -> CompiledPattern:
    parts = [p.strip() for p in pattern.split("-")]
    parts = [p for p in parts if p != ""]
    if not parts or parts[-1] != "?":
        raise ValueError(f"Pattern must end with '?': {pattern!r}")
    parts = parts[:-1]
    open_prefix = False
    if parts and parts[0] == "...":
        open_prefix = True
        parts = parts[1:]
    tokens = []
    for p in parts:
        if p == "*":
            tokens.append(TokenMatcher(alternatives=("act", "P")))
            continue
        alts = tuple(a for a in _expand_paren(p))
        # validate literals now (fail fast on typos)
        for a in alts:
            if not _CMP_RE.match(a):
                Call.parse(a)
        tokens.append(TokenMatcher(alternatives=alts))
    return CompiledPattern(tokens=tuple(tokens), open_prefix=open_prefix, raw=pattern)


def pattern_matches(cp: CompiledPattern, stripped_calls: list[str]) -> bool:
    """Match against the auction's call strings (leading passes already stripped)."""
    n, k = len(stripped_calls), len(cp.tokens)
    if cp.open_prefix:
        if n < k:
            return False
        tail = stripped_calls[n - k:]
    else:
        if n != k:
            return False
        tail = stripped_calls
    return all(tok.matches(c) for tok, c in zip(cp.tokens, tail))


def _best_specificity(ctx, stripped_calls: list[str]) -> int | None:
    """Highest specificity among the context's patterns that match, or None.

    A context may declare `also_patterns` - extra auction shapes it owns.  The
    match is the most specific shape that fits, so adding a shape can never
    make an existing match less specific.
    """
    best = None
    for cp in (ctx.compiled_pattern, *getattr(ctx, "compiled_also", ())):
        if pattern_matches(cp, stripped_calls):
            best = cp.specificity if best is None else max(best, cp.specificity)
    return best


def match_all_contexts(contexts, stripped_calls: list[str]) -> list:
    """All matching contexts, most specific first (ties keep file order)."""
    scored = [
        (spec, -i, ctx)
        for i, ctx in enumerate(contexts)
        if (spec := _best_specificity(ctx, stripped_calls)) is not None
    ]
    scored.sort(key=lambda t: (t[0], t[1]), reverse=True)
    return [ctx for _, _, ctx in scored]


def match_context(contexts, stripped_calls: list[str]):
    """Return the best-matching context (most specific pattern; ties broken by
    file order), or None."""
    matches = match_all_contexts(contexts, stripped_calls)
    return matches[0] if matches else None
