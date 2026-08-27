"""Critical invariant tests.

1. Self-consistency: any auction the engine produces in (fast-path) self-play
   is exactly reproduced by replaying the same deal.  The consistent-deal
   sampler relies on this.
2. In a game-forcing auction the engine never passes below game.
3. explain_bid on the engine's chosen call agrees with choose_bid's own
   explanation.
"""

import random

import pytest

from bridgebidder.api import choose_bid, explain_bid
from bridgebidder.domain.auction import Auction
from bridgebidder.domain.calls import Call
from bridgebidder.domain.cards import FULL_DECK, Hand
from bridgebidder.domain.types import Seat, Vulnerability
from bridgebidder.engine.decision import decide_fast
from bridgebidder.engine.selfplay import self_play
from bridgebidder.inference.engine import analyze, prepare_decision
from bridgebidder.system.dsl import load_system

SYSTEM = load_system()


def random_deal(rng):
    deck = list(FULL_DECK)
    rng.shuffle(deck)
    return {s: Hand(deck[i * 13:(i + 1) * 13]) for i, s in enumerate(Seat)}


VULS = [Vulnerability.NONE, Vulnerability.NS, Vulnerability.EW, Vulnerability.BOTH]


@pytest.mark.parametrize("seed", range(40))
def test_selfplay_replay_consistency(seed):
    """Replay every call of a self-played auction: the engine must repeat itself."""
    rng = random.Random(seed)
    deal = random_deal(rng)
    dealer = Seat.from_index(seed % 4)
    vul = VULS[seed % 4]
    auction = self_play(SYSTEM, deal, dealer, vul)

    prefix = Auction(dealer=dealer, vulnerability=vul)
    for call in auction.calls:
        seat = prefix.next_seat
        setup = prepare_decision(SYSTEM, prefix, perspective=seat)
        replayed = decide_fast(setup, deal[seat])
        assert str(replayed) == str(call), (
            f"deal seed {seed}: replay diverged at {prefix}: got {replayed}, expected {call}"
        )
        prefix.add(call)


@pytest.mark.parametrize("seed", range(60))
def test_never_pass_out_below_game_when_game_forced(seed):
    """Whenever a self-played auction became game-forced for a side, that side
    must not have let the auction die below game."""
    rng = random.Random(1000 + seed)
    deal = random_deal(rng)
    dealer = Seat.from_index(seed % 4)
    auction = self_play(SYSTEM, deal, dealer, VULS[(seed // 4) % 4])
    analysis = analyze(SYSTEM, auction)

    contract = auction.contract
    if contract is None:
        return
    side = contract.declarer.side
    if not analysis.sides[side].game_forced:
        return
    lb = auction.last_bid
    game_reached = (
        (lb.strain == "NT" and lb.level >= 3)
        or (lb.strain in ("H", "S") and lb.level >= 4)
        or (lb.strain in ("C", "D") and lb.level >= 5)
    )
    doubled = contract.doubled > 0
    assert game_reached or doubled or contract.declarer.side != side, (
        f"seed {seed}: game-forced side stopped below game: {auction}"
    )


def _gf_position_request(hand, calls, seat):
    return {
        "hand": hand,
        "auction_state": {"dealer": "N", "seat": seat, "calls": calls},
        "use_arbitration": False,
    }


def test_gf_never_pass_direct():
    """Even with a dead-minimum hand, responder cannot pass a GF auction below game."""
    # 1S - 2C (GF) - 2S; responder must keep bidding
    r = choose_bid(_gf_position_request("A5.64.K842.AKJ32", ["1S", "P", "2C", "P", "2S", "P"], "S"))
    assert r["chosen_call"] != "P"
    # opener likewise after 2/1 and a rebid
    r = choose_bid(_gf_position_request("AQ752.K64.Q4.K93", ["1S", "P", "2C", "P", "2NT", "P", "3NT", "P"], "N"))
    # 3NT is game: pass is now fine
    assert r["chosen_call"] == "P"


@pytest.mark.parametrize("seed", range(25))
def test_explain_matches_choose(seed):
    """explain_bid(chosen call) must equal choose_bid's explanation."""
    rng = random.Random(2000 + seed)
    deal = random_deal(rng)
    dealer = Seat.from_index(seed % 4)
    # walk a self-played auction and compare at 3 random positions
    auction = self_play(SYSTEM, deal, dealer)
    prefix = []
    positions = []
    a = Auction(dealer=dealer)
    for call in auction.calls:
        positions.append((list(prefix), a.next_seat, str(call)))
        prefix.append(str(call))
        a.add(call)
    for calls, seat, _ in rng.sample(positions, min(3, len(positions))):
        req = {
            "hand": str(deal[seat]),
            "auction_state": {"dealer": dealer.value, "seat": seat.value, "calls": calls},
            "use_arbitration": False,
        }
        chosen = choose_bid(req)
        explained = explain_bid({
            "auction_state": req["auction_state"],
            "candidate": chosen["chosen_call"],
        })
        assert explained == chosen["explanation"], (
            f"seed {seed}: explain_bid disagrees with choose_bid at {calls}"
        )
