"""Two latent engine bugs diagnosed in round 17 and fixed in round 18.

Both are invisible in normal play, which is why they survived seventeen rounds:
one only fires when a YAML rule uses a `when` condition nothing currently uses,
the other only fires when a system object is garbage-collected and its address
is reused.
"""

import gc
import weakref
from pathlib import Path

import pytest

from bridgebidder.domain.auction import Auction
from bridgebidder.domain.calls import Call
from bridgebidder.domain.types import Seat, Vulnerability
from bridgebidder.inference.engine import (
    _conditions_hold,
    _system_token,
    build_eval_ctx,
    prepare_decision,
)
from bridgebidder.api import choose_bid
from bridgebidder.system.dsl import Conditions, load_system


def _auction(calls, dealer=Seat.N, vul=Vulnerability.NONE):
    a = Auction(dealer=dealer, vulnerability=vul)
    for c in calls:
        a.add(Call.parse(c))
    return a


def test_partner_limited_condition_is_evaluable():
    """`when: {partner_limited: true}` must not raise.

    The condition read a name (`eval_ctx`) that does not exist in its own
    function, whose parameter is `ctx`, so the FIRST YAML rule to use it would
    have raised NameError at decision time.  Round 18's experts propose rules
    that use it, so it has to work.
    """
    system = load_system()
    auction = _auction(["1H", "P", "1NT", "P"])          # partner's 1NT is limited
    setup = prepare_decision(system, auction, perspective=Seat.N)
    ctx = build_eval_ctx(setup.analysis, auction, Seat.N)

    # both branches must return a bool rather than raising
    yes = _conditions_hold(Conditions(partner_limited=True), auction, Seat.N,
                           system, ctx, Call.parse("2H"))
    no = _conditions_hold(Conditions(partner_limited=False), auction, Seat.N,
                          system, ctx, Call.parse("2H"))
    assert isinstance(yes, bool) and isinstance(no, bool)
    assert yes != no                                     # exactly one holds
    # a 1NT response caps partner, so `partner_limited: true` is the true branch
    assert yes is True

    # and it must still be evaluable when no eval context is supplied at all
    assert _conditions_hold(Conditions(partner_limited=False), auction, Seat.N,
                            system, None, Call.parse("2H")) is True


def test_setup_cache_token_is_never_reused():
    """The decision cache must not key on a reusable identity.

    `_SETUP_CACHE` keyed on `id(system)` while holding no reference to the
    system, so once one was collected a rebuilt system could be allocated at
    the same address and inherit the dead one's cached decisions.
    `tools/tune.py` rebuilds systems in a loop, which is exactly that.
    """
    # `config_overrides` rebuilds the system object, which is exactly what
    # `tools/tune.py:211` does in a loop.
    a = load_system(config_overrides={"nt_with_5M": True})
    b = load_system(config_overrides={"nt_with_5M": False})
    assert a is not b
    assert _system_token(a) != _system_token(b)
    assert _system_token(a) == _system_token(a)           # stable

    dead_token = _system_token(b)
    ref = weakref.ref(b)
    del b
    gc.collect()
    if ref() is not None:                                 # pragma: no cover
        pytest.skip("system not collected; the token invariant is untestable here")

    c = load_system(config_overrides={"nt_with_5M": True})
    assert _system_token(c) != dead_token                 # never handed out twice

def test_two_systems_in_one_process_do_not_alias(tmp_path):
    """Two different systems must not share cached decisions.

    This is the end-to-end version of the token test above, and it is the
    shape the bug actually took in practice: a round-18 reviewer prototyping
    against a patched COPY of the YAML got results from the wrong system in
    the same process, which produced two phantom regression failures.
    `tools/tune.py` and every "screen a patched copy" workflow do exactly this.
    """
    base_path = Path("src/bridgebidder/systems/two_over_one.yaml")
    text = base_path.read_text()

    # make the rule that decides this seat unfittable, so the two systems MUST
    # disagree - demoting its priority would not do, since it is the only
    # candidate above the 0.9 fast path and priority never gets consulted
    anchor = "      - id: oc1D_X\n        call: X\n        priority: 72\n        requires:"
    assert text.count(anchor) == 1
    patched = tmp_path / "patched.yaml"
    patched.write_text(text.replace(anchor, anchor + "\n          hcp: [30, 40]"))

    def ask(system_path):
        req = {"hand": "KJ4.AQ52.KQ9.A83",
               "auction_state": {"dealer": "N", "vulnerability": "None",
                                 "seat": "E", "calls": ["1D"]}}
        if system_path:
            req["system_path"] = str(system_path)
        return choose_bid(req)["chosen_call"]

    # interleaved, so a stale cache entry would be caught in either direction
    first_base = ask(None)
    first_mod = ask(patched)
    second_base = ask(None)
    second_mod = ask(patched)

    assert first_base == "X"                       # the takeout double
    assert first_mod == "1NT"                      # it no longer fits
    assert second_base == first_base
    assert second_mod == first_mod
