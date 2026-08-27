"""Public API: choose_bid and explain_bid.

Both take JSON-shaped dicts (validated with pydantic) and return JSON-shaped
dicts, so the CLI is a thin wrapper.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field, field_validator

from .domain.auction import Auction
from .domain.calls import Call
from .domain.cards import Hand
from .domain.types import Seat, Vulnerability
from .engine.decision import choose
from .engine.explain import build_explanation
from .inference.engine import prepare_decision
from .system.dsl import BiddingSystem, load_system


class CallInput(BaseModel):
    call: str
    explanation: dict | None = None  # {text: str, constraints?: {...}}


class AuctionStateInput(BaseModel):
    dealer: str
    vulnerability: str = "None"
    seat: str
    calls: list[CallInput | str] = Field(default_factory=list)

    @field_validator("calls", mode="before")
    @classmethod
    def _normalize_calls(cls, v: Any) -> Any:
        out = []
        for item in v or []:
            if isinstance(item, str):
                out.append({"call": item})
            else:
                out.append(item)
        return out


class ChooseBidInput(BaseModel):
    hand: str
    auction_state: AuctionStateInput
    system_path: str | None = None
    config: dict[str, Any] | None = None
    use_arbitration: bool = True
    arbitration_budget: float = 8.0


class ExplainBidInput(BaseModel):
    auction_state: AuctionStateInput
    candidate: str
    hand: str | None = None  # optional; not needed to explain
    system_path: str | None = None
    config: dict[str, Any] | None = None


def _build_auction(state: AuctionStateInput) -> tuple[Auction, Seat, dict[int, dict]]:
    auction = Auction(
        dealer=Seat(state.dealer.upper()),
        vulnerability=Vulnerability.parse(state.vulnerability),
    )
    explanations: dict[int, dict] = {}
    for i, ci in enumerate(state.calls):
        assert isinstance(ci, CallInput)
        auction.add(Call.parse(ci.call))
        if ci.explanation:
            explanations[i] = ci.explanation
    return auction, Seat(state.seat.upper()), explanations


def _load(system_path: str | None, config: dict | None) -> BiddingSystem:
    return load_system(system_path, config_overrides=config)


def choose_bid(request: dict) -> dict:
    """Choose a call for the given hand and auction state."""
    req = ChooseBidInput.model_validate(request)
    system = _load(req.system_path, req.config)
    hand = Hand.parse(req.hand)
    auction, seat, explanations = _build_auction(req.auction_state)
    if auction.next_seat != seat:
        raise ValueError(
            f"It is {auction.next_seat.value}'s turn to call, but the request is for seat {seat.value}"
        )
    decision = choose(
        system, auction, seat, hand,
        explanations=explanations,
        use_arbitration=req.use_arbitration,
        arbitration_budget=req.arbitration_budget,
    )
    setup = decision.setup
    explanation = build_explanation(setup, decision.chosen.call)
    alternatives = [
        {
            "call": str(sc.call),
            "match_score": round(sc.fit, 3),
            "blended_score": round(sc.score, 3),
            "expected_imp_delta": sc.expected_imp_delta,
            "shows": sc.candidate.shows,
        }
        for sc in decision.ranked[:5]
        if str(sc.call) != str(decision.chosen.call)
    ]
    analysis = setup.analysis
    return {
        "chosen_call": str(decision.chosen.call),
        "confidence": decision.confidence,
        "explanation": explanation,
        "alternatives": alternatives,
        "partner_model": analysis.partner_model(seat),
        "opponent_models": analysis.opponent_models(seat),
        "arbitration": decision.arbitration,
        "log": decision.log,
    }


def explain_bid(request: dict) -> dict:
    """Explain what a candidate call would show in the given auction state."""
    req = ExplainBidInput.model_validate(request)
    system = _load(req.system_path, req.config)
    auction, seat, explanations = _build_auction(req.auction_state)
    if auction.next_seat != seat:
        raise ValueError(
            f"It is {auction.next_seat.value}'s turn to call, but the request is for seat {seat.value}"
        )
    call = Call.parse(req.candidate)
    if not auction.is_legal(call):
        raise ValueError(f"{call} is not a legal call in this auction")
    setup = prepare_decision(system, auction, explanations, perspective=seat)
    return build_explanation(setup, call)
