"""Explanation layer: build structured BidExplanation objects."""

from __future__ import annotations

from ..constraints.model import HandConstraint
from ..domain.calls import Call
from ..domain.cards import SUITS
from ..inference.engine import DecisionSetup, Interpretation, interpret_call


def _shows_block(constraint: HandConstraint, text: str) -> dict:
    box = constraint.box()
    suits = {
        s: [int(box.suit(s)[0]), int(box.suit(s)[1])]
        for s in SUITS
        if box.suit(s) != (0.0, 13.0)
    }
    features = list(constraint.features)
    for c in constraint.all_of:
        features.extend(c.features)
    return {
        "hcp": [int(box.hcp[0]), int(box.hcp[1]) if box.hcp[1] < 40 else 99],
        "suits": suits,
        "features": features,
        "text": text,
    }


def build_explanation(setup: DecisionSetup, call: Call, interp: Interpretation | None = None) -> dict:
    """Structured BidExplanation for `call` at this auction position."""
    interp = interp or interpret_call(setup, call)
    shows_text = interp.shows_text or str(call)

    denies: list[dict] = []
    if interp.primary_rule:
        for d in interp.primary_rule.denies:
            denies.append({"text": d.text, "constraint": d.constraint.to_dict()})
    # auto-derived denials from skipped higher-priority rules (negative inference)
    for r in interp.skipped_rules:
        denies.append({
            "text": f"not: {r.shows}" if r.shows else f"would have bid {r.call}",
            "constraint": {"not": r.requires.to_dict()},
            "derived_from_rule": r.id,
            "weight": r.negative_inference_weight,
        })

    return {
        "call": str(call),
        "shows": _shows_block(interp.constraint, shows_text),
        "denies": denies,
        "forcing_status": interp.establishes.forcing,
        "alertable": interp.alertable,
        "announce": interp.announce,
        "convention": interp.convention,
        "source_rule_id": interp.source_rule_id,
        "is_undiscussed_fallback": interp.is_fallback,
        "constraint": interp.constraint.to_dict(),
    }
