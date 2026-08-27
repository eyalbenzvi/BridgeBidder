"""Corpus quality gate.

A fixed, seeded corpus of self-played boards with hard thresholds, so any
future change that degrades bidding quality fails the build rather than being
discovered by the next harvest round.  Thresholds are set at the level the
engine actually achieves, with a little headroom for noise; tighten them when
the engine improves, and never loosen them to make a change pass.
"""

import random

import pytest

from bridgebidder.domain.auction import Auction
from bridgebidder.domain.cards import FULL_DECK, Hand
from bridgebidder.domain.types import Seat, Vulnerability
from bridgebidder.engine.dd import get_dd
from bridgebidder.engine.decision import decide_fast
from bridgebidder.engine.scoring import imps, signed_score
from bridgebidder.engine.selfplay import self_play
from bridgebidder.inference.engine import analyze, prepare_decision
from bridgebidder.system.dsl import load_system

CORPUS_SEED = 90210
CORPUS_SIZE = 120
VULS = [Vulnerability.NONE, Vulnerability.NS, Vulnerability.EW, Vulnerability.BOTH]

# achieved levels, with headroom; these are ceilings, never to be relaxed
MAX_PAR_LOSS_PER_BOARD = 7.5      # achieved ~5.7
MAX_FALLBACK_PER_BOARD = 0.60     # achieved ~0.25
MAX_MISBID_RATE = 0.030           # achieved ~0.012 of non-pass calls
MIN_FIT_FOR_MISBID = 0.5


@pytest.fixture(scope="module")
def corpus():
    system = load_system()
    dd = get_dd()
    rng = random.Random(CORPUS_SEED)
    out = []
    for i in range(CORPUS_SIZE):
        deck = list(FULL_DECK)
        rng.shuffle(deck)
        deal = {s: Hand(deck[j * 13:(j + 1) * 13]) for j, s in enumerate(Seat)}
        out.append((deal, Seat.from_index(i % 4), VULS[(i // 4) % 4]))
    return system, dd, out


def test_corpus_has_no_hard_failures(corpus):
    """Every board bids to a legal, terminating auction that replays identically."""
    system, _, boards = corpus
    for i, (deal, dealer, vul) in enumerate(boards):
        auction = self_play(system, deal, dealer, vul)
        assert auction.is_complete, f"board {i} did not terminate"
        check = Auction(dealer=dealer, vulnerability=vul)
        for call in auction.calls:
            seat = check.next_seat
            setup = prepare_decision(system, check, perspective=seat)
            assert check.is_legal(call), f"board {i}: illegal {call}"
            # replay determinism: the sampler depends on this
            assert str(decide_fast(setup, deal[seat])) == str(call), \
                f"board {i}: replay diverged at {check}"
            check.add(call)


def test_corpus_bidding_quality_thresholds(corpus):
    """Par loss, undiscussed calls and misbids all stay under their ceilings."""
    system, dd, boards = corpus
    par_loss = fallbacks = misbids = non_pass = 0
    from endplay.dds import calc_dd_table, par as dd_par
    from endplay.types import Deal, Player, Vul
    vmap = {Vulnerability.NONE: Vul.none, Vulnerability.NS: Vul.ns,
            Vulnerability.EW: Vul.ew, Vulnerability.BOTH: Vul.both}
    pmap = {Seat.N: Player.north, Seat.E: Player.east,
            Seat.S: Player.south, Seat.W: Player.west}

    for deal, dealer, vul in boards:
        auction = self_play(system, deal, dealer, vul)
        analysis = analyze(system, auction)
        prefix = Auction(dealer=dealer, vulnerability=vul)
        for ann in analysis.annotations:
            interp = ann.interpretation
            if not ann.call.is_pass:
                non_pass += 1
                setup = prepare_decision(system, prefix, perspective=ann.seat)
                cand = next((c for c in setup.candidates if c.call == ann.call), None)
                ctx = setup.candidate_ctx(cand) if cand else setup.eval_ctx
                if interp.constraint.fit(deal[ann.seat], ctx) < MIN_FIT_FOR_MISBID:
                    misbids += 1
                if interp.is_fallback:
                    fallbacks += 1
            prefix.add(ann.call)

        contract = auction.contract
        tricks = dd.tricks(deal, contract.declarer, contract.strain) if contract else 0
        ns = signed_score(contract, tricks, vul, "NS")
        pbn = "N:" + " ".join(str(deal[s]) for s in (Seat.N, Seat.E, Seat.S, Seat.W))
        p = int(dd_par(calc_dd_table(Deal(pbn)), vmap[vul], pmap[dealer]).score)
        par_loss += max(0, imps(p - ns)) + max(0, imps(ns - p))

    n = len(boards)
    assert par_loss / n <= MAX_PAR_LOSS_PER_BOARD, \
        f"par loss {par_loss / n:.2f} exceeds {MAX_PAR_LOSS_PER_BOARD}"
    assert fallbacks / n <= MAX_FALLBACK_PER_BOARD, \
        f"undiscussed calls {fallbacks / n:.2f}/board exceeds {MAX_FALLBACK_PER_BOARD}"
    assert misbids / max(1, non_pass) <= MAX_MISBID_RATE, \
        f"misbid rate {misbids / max(1, non_pass):.3f} exceeds {MAX_MISBID_RATE}"
