"""BridgeBidder: a 2/1 Game Forcing bridge bidding engine.

Public API:
    choose_bid(request: dict) -> dict
    explain_bid(request: dict) -> dict
"""

from .api import choose_bid, explain_bid

__all__ = ["choose_bid", "explain_bid"]
__version__ = "0.1.0"
