#!/usr/bin/env python3
"""BEN bidding worker — runs inside its own virtualenv, speaks JSON on stdio.

BEN (github.com/lorserker/ben) is a neural bidder trained on a large corpus of
expert auctions.  It is NOT a source of truth: it is a strong second opinion,
and where it disagrees with us that is a lead to investigate, not a verdict.

Isolation: BEN pins numpy<2.1 while this project needs 2.4 for endplay, so BEN
lives in a separate venv and is driven over a pipe.  Only the ONNX bidder is
used (no TensorFlow): the network is the one from BEN's own 2/1 Game Forcing
configuration, which is the same system our engine plays.

Protocol: one JSON request per line on stdin, one JSON response per line out.
  request  {"hands": {"N": "AQ52.KJ4.T92.873", ...}, "dealer": "N",
            "vuln_ns": 0, "vuln_ew": 0, "auction": ["1H", "P"]}
  response {"bid": "2H", "top": [["2H", 0.71], ["3H", 0.11], ...]}
"""

import json
import sys

BEN_SRC = "/tmp/ben/src"
BEN_MODEL = "/tmp/ben/models/onnx/bidder.onnx"
sys.path.insert(0, BEN_SRC)

import numpy as np                      # noqa: E402
import onnxruntime as ort               # noqa: E402
from bidding import bidding             # noqa: E402
from bidding import binary as bbinary   # noqa: E402

N_CARDS = 24        # n_cards_bidding from BEN-21GF.conf
NS = EW = 1         # system ids: both sides play 2/1 GF
N_BIDS = 4          # the encoding includes my own previous call
SEATS = ["N", "E", "S", "W"]

_parse_hand = bbinary.parse_hand_f(N_CARDS)
_session = ort.InferenceSession(BEN_MODEL, providers=["CPUExecutionProvider"])
_input_name = _session.get_inputs()[0].name


def _features(hand_str, vuln_ns, vuln_ew, auction, seat_i, dealer_i):
    """Rebuild BEN's 193-feature vector for every turn this seat has had.

    The model is sequential: it is fed the seat's whole bidding history and
    predicts each call in turn, so the prediction at the final step is the
    call it would make now.  Normalisation and padding follow BEN's own
    DealData exactly - hcp is (hcp - 10) / 4, shape is (len - 3.25) / 1.75,
    and the auction is left-padded so that index i belongs to seat i % 4.
    """
    hand = _parse_hand(hand_str).astype(np.float32)
    hcp = ((bbinary.get_hcp(hand) - 10) / 4).reshape((1, 1)).astype(np.float32)
    shape = ((bbinary.get_shape(hand) - 3.25) / 1.75).reshape((1, 4)).astype(np.float32)
    v_we = vuln_ns if seat_i % 2 == 0 else vuln_ew
    v_them = vuln_ew if seat_i % 2 == 0 else vuln_ns
    ns_ew = np.array([[NS, EW]] if seat_i % 2 == 0 else [[EW, NS]], dtype=np.float32)
    vuln = np.array([[float(v_we), float(v_them)]], dtype=np.float32)

    padded = ["PAD_START"] * dealer_i + list(auction)

    def at(j):
        return padded[j] if 0 <= j < len(padded) else "PAD_START"

    # This seat's turns are the indices congruent to seat_i (mod 4) that fall
    # at or after the dealer: earlier slots are PAD_START placeholders and are
    # NOT turns.  Feeding them as steps corrupts the sequential model's state.
    steps = []
    i = seat_i if seat_i >= dealer_i else seat_i + 4
    while i <= len(padded):
        steps.append(np.concatenate((
            ns_ew, vuln, hcp, shape, hand,
            bidding.encode_bid(at(i - 4)).astype(np.float32),
            bidding.encode_bid(at(i - 3)).astype(np.float32),
            bidding.encode_bid(at(i - 2)).astype(np.float32),
            bidding.encode_bid(at(i - 1)).astype(np.float32),
        ), axis=1))
        i += 4
    return np.array(steps, dtype=np.float32).reshape((1, len(steps), 193))


def to_ben(call):
    """Our call strings -> BEN's vocabulary."""
    if call in ("P", "PASS"):
        return "PASS"
    return call.replace("NT", "N")


def from_ben(call):
    if call == "PASS":
        return "P"
    return call.replace("N", "NT") if call.endswith("N") else call


def bid(req):
    auction = [to_ben(c) for c in req["auction"]]
    dealer_i = SEATS.index(req["dealer"])
    seat_i = (dealer_i + len(auction)) % 4
    hand_str = req["hands"][SEATS[seat_i]]
    x = _features(hand_str, req.get("vuln_ns", 0), req.get("vuln_ew", 0),
                  auction, seat_i, dealer_i)
    probs = _session.run(None, {_input_name: x})[0][0, -1, :]
    order = np.argsort(probs)[::-1]
    legal = []
    for idx in order:
        b = bidding.ID2BID[int(idx)]
        if b in ("PAD_START", "PAD_END"):
            continue
        if b == "PASS" or bidding.can_bid(b, auction):
            legal.append((from_ben(b), float(probs[idx])))
        if len(legal) >= 5:
            break
    if not legal:
        return {"bid": "P", "top": []}
    return {"bid": legal[0][0], "top": [[b, round(p, 4)] for b, p in legal]}


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            print(json.dumps(bid(json.loads(line))), flush=True)
        except Exception as e:  # never kill the worker on one bad board
            print(json.dumps({"error": f"{type(e).__name__}: {e}"}), flush=True)


if __name__ == "__main__":
    main()
