"""The bidding-system DSL: YAML knowledge base -> typed rule objects.

The system is DATA.  Each context matches a family of auctions and lists
candidate call rules with constraints, priorities, shown/denied meanings,
forcing implications, and conditions (seat, vulnerability, config flags...).

Template expansion: a context may declare `expand: {M: [H, S]}` and use `$M`
anywhere in its strings; the loader emits one concrete context per combination.
"""

from __future__ import annotations

import itertools
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from ..constraints.model import HandConstraint
from ..domain.calls import Call
from .matcher import CompiledPattern, compile_pattern

FORCING_STATUSES = ("game_forcing", "one_round", "invitational", "non_forcing", "sign_off")


@dataclass(frozen=True)
class Establishes:
    forcing: str = "non_forcing"          # forcing status this call sets
    game_force: bool = False              # auction becomes GF for our side
    agreed_suit: str | None = None        # trump agreement, if any
    asking: str | None = None             # e.g. "keycards" (RKC in progress)

    @staticmethod
    def from_dict(d: dict | None) -> "Establishes":
        d = dict(d or {})
        forcing = d.pop("forcing", "non_forcing")
        if forcing not in FORCING_STATUSES:
            raise ValueError(f"Bad forcing status {forcing!r}")
        e = Establishes(
            forcing=forcing,
            game_force=bool(d.pop("game_force", forcing == "game_forcing")),
            agreed_suit=d.pop("agreed_suit", None),
            asking=d.pop("asking", None),
        )
        if d:
            raise ValueError(f"Unknown establishes keys: {sorted(d)}")
        return e


@dataclass(frozen=True)
class Denial:
    text: str
    constraint: HandConstraint


@dataclass(frozen=True)
class Conditions:
    """Auction-context conditions on a rule (not about the hand)."""

    opening_seat: tuple[int, ...] | None = None    # 1..4
    passed_hand: bool | None = None
    we_vulnerable: bool | None = None
    they_vulnerable: bool | None = None
    we_hold_contract: bool | None = None           # our own last bid stands
    partner_suit: str | None = None                # this suit is partner's
    unbid_suit: str | None = None                  # nobody has shown this suit
    cheapest_in_suit: bool | None = None           # this call is the lowest bid available in its suit
    side_has_acted: bool | None = None             # our side has already made a non-pass call
    their_last_bid_suit: bool | None = None        # the standing contract is a SUIT bid by them
    we_bid_last: bool | None = None                # the standing contract bid is OURS (either seat)
    i_have_acted: bool | None = None               # I myself have already made a non-pass call
    their_bid_level: tuple[int, ...] | None = None # level of the standing bid (theirs or ours)
    my_suit: str | None = None                     # I have bid this suit myself
    config: dict[str, Any] = field(default_factory=dict)

    @staticmethod
    def from_dict(d: dict | None) -> "Conditions":
        d = dict(d or {})
        c = Conditions(
            opening_seat=tuple(d.pop("opening_seat")) if "opening_seat" in d else None,
            passed_hand=d.pop("passed_hand", None),
            we_vulnerable=d.pop("we_vulnerable", None),
            they_vulnerable=d.pop("they_vulnerable", None),
            we_hold_contract=d.pop("we_hold_contract", None),
            partner_suit=d.pop("partner_suit", None),
            unbid_suit=d.pop("unbid_suit", None),
            cheapest_in_suit=d.pop("cheapest_in_suit", None),
            side_has_acted=d.pop("side_has_acted", None),
            their_last_bid_suit=d.pop("their_last_bid_suit", None),
            we_bid_last=d.pop("we_bid_last", None),
            i_have_acted=d.pop("i_have_acted", None),
            their_bid_level=tuple(d.pop("their_bid_level")) if "their_bid_level" in d else None,
            my_suit=d.pop("my_suit", None),
            config=d.pop("config", {}) or {},
        )
        if d:
            raise ValueError(f"Unknown condition keys: {sorted(d)}")
        return c

    @property
    def is_trivial(self) -> bool:
        return (
            self.opening_seat is None
            and self.passed_hand is None
            and self.we_vulnerable is None
            and self.they_vulnerable is None
            and self.we_hold_contract is None
            and self.partner_suit is None
            and self.unbid_suit is None
            and self.cheapest_in_suit is None
            and self.side_has_acted is None
            and self.their_last_bid_suit is None
            and self.we_bid_last is None
            and self.i_have_acted is None
            and self.their_bid_level is None
            and self.my_suit is None
            and not self.config
        )


@dataclass(frozen=True)
class BidRule:
    id: str
    call: Call
    priority: float
    requires: HandConstraint
    shows: str
    denies: tuple[Denial, ...] = ()
    establishes: Establishes = Establishes()
    alertable: bool = False
    announce: str | None = None
    convention: str | None = None
    negative_inference_weight: str = "strong"  # strong | soft
    when: Conditions = Conditions()
    context_id: str = ""

    @staticmethod
    def from_dict(d: dict, context_id: str, index: int) -> "BidRule":
        d = dict(d)
        call = Call.parse(str(d.pop("call")))
        denies = tuple(
            Denial(text=x["text"], constraint=HandConstraint.from_dict(x.get("constraint")))
            for x in d.pop("denies", []) or []
        )
        niw = d.pop("negative_inference_weight", "strong")
        if niw not in ("strong", "soft"):
            raise ValueError(f"Bad negative_inference_weight {niw!r}")
        rule = BidRule(
            id=str(d.pop("id", f"{context_id}.{index}.{call}")),
            call=call,
            priority=float(d.pop("priority", 50)),
            requires=HandConstraint.from_dict(d.pop("requires", None)),
            shows=str(d.pop("shows", "")),
            denies=denies,
            establishes=Establishes.from_dict(d.pop("establishes", None)),
            alertable=bool(d.pop("alertable", False)),
            announce=d.pop("announce", None),
            convention=d.pop("convention", None),
            negative_inference_weight=niw,
            when=Conditions.from_dict(d.pop("when", None)),
            context_id=context_id,
        )
        if d:
            raise ValueError(f"Unknown rule keys in {rule.id}: {sorted(d)}")
        return rule


@dataclass(frozen=True)
class ContextWhen:
    """Conditions on the auction state for a whole context (used mainly by
    open-prefix conventions like RKC)."""

    agreed_suit: bool | str | None = None   # True = some suit agreed; "H" = hearts agreed
    game_forced: bool | None = None
    asking: str | None = None               # active ask, e.g. "keycards"
    we_hold_contract: bool | None = None    # our own last bid still stands

    @staticmethod
    def from_dict(d: dict | None) -> "ContextWhen":
        d = dict(d or {})
        w = ContextWhen(
            agreed_suit=d.pop("agreed_suit", None),
            game_forced=d.pop("game_forced", None),
            asking=d.pop("asking", None),
            we_hold_contract=d.pop("we_hold_contract", None),
        )
        if d:
            raise ValueError(f"Unknown context-when keys: {sorted(d)}")
        return w

    @property
    def is_trivial(self) -> bool:
        return (self.agreed_suit is None and self.game_forced is None
                and self.asking is None and self.we_hold_contract is None)


@dataclass(frozen=True)
class Context:
    id: str
    pattern: str
    compiled_pattern: CompiledPattern
    rules: tuple[BidRule, ...]
    description: str = ""
    when: ContextWhen = ContextWhen()

    def rules_for_call(self, call: Call) -> list[BidRule]:
        return [r for r in self.rules if r.call == call]


@dataclass
class BiddingSystem:
    name: str
    config: dict[str, Any]
    contexts: list[Context]
    defense_notes: str = ""

    def context_ids(self) -> list[str]:
        return [c.id for c in self.contexts]


_VAR_RE = re.compile(r"\$([A-Za-z_][A-Za-z0-9_]*)")


def _substitute(obj: Any, env: dict[str, str]) -> Any:
    if isinstance(obj, str):
        def rep(m: re.Match) -> str:
            name = m.group(1)
            if name not in env:
                raise ValueError(f"Unbound template var ${name}")
            return env[name]

        return _VAR_RE.sub(rep, obj)
    if isinstance(obj, dict):
        return {_substitute(k, env): _substitute(v, env) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_substitute(x, env) for x in obj]
    return obj


# Built-in derived template vars: when a var binds a suit letter, $VAR_bid1
# etc. are not provided; instead YAML authors use helper maps below.
_OTHER_MAJOR = {"H": "S", "S": "H"}
_OTHER_MINOR = {"C": "D", "D": "C"}


def _augment_env(env: dict[str, str]) -> dict[str, str]:
    out = dict(env)
    for k, v in env.items():
        if v in _OTHER_MAJOR:
            out[f"o{k}"] = _OTHER_MAJOR[v]  # $oM = the other major
        if v in _OTHER_MINOR:
            out[f"o{k}"] = _OTHER_MINOR[v]
    return out


def _expand_context(raw: dict) -> list[dict]:
    pairs = raw.pop("expand_pairs", None)
    if pairs:
        out = []
        for env_raw in pairs:
            env = _augment_env({k: str(v) for k, v in env_raw.items()})
            sub = _substitute(raw, env)
            sub["id"] = f"{raw['id']}[{','.join(str(v) for v in env_raw.values())}]"
            out.append(sub)
        return out
    expand = raw.pop("expand", None)
    if not expand:
        return [raw]
    keys = list(expand.keys())
    out = []
    for combo in itertools.product(*[expand[k] for k in keys]):
        env = _augment_env({k: str(v) for k, v in zip(keys, combo)})
        sub = _substitute(raw, env)
        sub["id"] = f"{raw['id']}[{','.join(str(v) for v in combo)}]"
        out.append(sub)
    return out


def parse_system(data: dict) -> BiddingSystem:
    meta = data.get("system", {})
    contexts: list[Context] = []
    for raw_ctx in data.get("contexts", []):
        for concrete in _expand_context(dict(raw_ctx)):
            cid = str(concrete.pop("id"))
            pattern = str(concrete.pop("pattern"))
            description = str(concrete.pop("description", ""))
            when = ContextWhen.from_dict(concrete.pop("when", None))
            rules = tuple(
                BidRule.from_dict(rd, cid, i)
                for i, rd in enumerate(concrete.pop("rules", []) or [])
            )
            if concrete:
                raise ValueError(f"Unknown context keys in {cid}: {sorted(concrete)}")
            contexts.append(
                Context(
                    id=cid,
                    pattern=pattern,
                    compiled_pattern=compile_pattern(pattern),
                    rules=rules,
                    description=description,
                    when=when,
                )
            )
    ids = [c.id for c in contexts]
    dupes = {i for i in ids if ids.count(i) > 1}
    if dupes:
        raise ValueError(f"Duplicate context ids: {sorted(dupes)}")
    return BiddingSystem(
        name=str(meta.get("name", "unnamed")),
        config=dict(meta.get("config", {})),
        contexts=contexts,
        defense_notes=str(meta.get("defense_notes", "")),
    )


class _StrictLoader(yaml.SafeLoader):
    """SafeLoader that refuses duplicate mapping keys.

    Plain YAML silently keeps the last of two identical keys.  In a hand-edited
    rulebook that is a silent constraint deletion: writing `evals:` twice under
    one `requires:` drops the first gate entirely, and the rule keeps firing as
    if the new gate had never been added.  That exact mistake shipped once and
    cost a whole measurement round; it is a parse error now.
    """

    def construct_mapping(self, node, deep=False):
        seen: set = set()
        for key_node, _ in node.value:
            key = self.construct_object(key_node, deep=deep)
            if key in seen:
                raise yaml.constructor.ConstructorError(
                    "while constructing a mapping", node.start_mark,
                    f"duplicate key {key!r}", key_node.start_mark)
            seen.add(key)
        return super().construct_mapping(node, deep=deep)


def default_system_path() -> Path:
    return Path(__file__).resolve().parent.parent / "systems" / "two_over_one.yaml"


_SYSTEM_CACHE: dict[tuple[str, float], BiddingSystem] = {}


def load_system(path: str | Path | None = None, config_overrides: dict | None = None) -> BiddingSystem:
    p = Path(path) if path else default_system_path()
    key = (str(p), p.stat().st_mtime)
    if key not in _SYSTEM_CACHE:
        with open(p) as f:
            data = yaml.load(f, Loader=_StrictLoader)
        _SYSTEM_CACHE[key] = parse_system(data)
    system = _SYSTEM_CACHE[key]
    if config_overrides:
        system = BiddingSystem(
            name=system.name,
            config={**system.config, **config_overrides},
            contexts=system.contexts,
            defense_notes=system.defense_notes,
        )
    return system
