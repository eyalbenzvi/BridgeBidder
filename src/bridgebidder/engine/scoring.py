"""Duplicate bridge scoring and IMP conversion."""

from __future__ import annotations

from ..domain.auction import Contract
from ..domain.types import Seat, Vulnerability

_TRICK_SCORE = {"C": 20, "D": 20, "H": 30, "S": 30}


def contract_score(contract: Contract, tricks: int, vulnerability: Vulnerability) -> int:
    """Score from declarer's side's point of view."""
    vul = vulnerability.is_vulnerable(contract.declarer)
    need = 6 + contract.level
    dbl = contract.doubled  # 0/1/2
    if tricks < need:
        down = need - tricks
        if dbl == 0:
            return -down * (100 if vul else 50)
        # doubled / redoubled penalties
        mult = 2 if dbl == 2 else 1
        if vul:
            pen = 200 + (down - 1) * 300
        else:
            pen = 100 + (down - 1) * 200 + (max(0, down - 3) * 100)
        return -pen * mult
    # made
    if contract.strain == "NT":
        base = 40 + (contract.level - 1) * 30
    else:
        base = _TRICK_SCORE[contract.strain] * contract.level
    base *= 2 ** dbl
    score = base
    # game / partscore bonus
    score += (500 if vul else 300) if base >= 100 else 50
    if dbl == 1:
        score += 50
    elif dbl == 2:
        score += 100
    # slam bonuses
    if contract.level == 6:
        score += 750 if vul else 500
    elif contract.level == 7:
        score += 1500 if vul else 1000
    # overtricks
    over = tricks - need
    if over > 0:
        if dbl == 0:
            per = 30 if contract.strain in ("NT", "H", "S") else 20
            score += over * per
        else:
            score += over * (200 if vul else 100) * (2 if dbl == 2 else 1)
    return score


def signed_score(contract: Contract | None, tricks: int, vulnerability: Vulnerability, side: str) -> int:
    """Score from `side`'s ("NS"/"EW") point of view; 0 for a passed-out deal."""
    if contract is None:
        return 0
    s = contract_score(contract, tricks, vulnerability)
    return s if contract.declarer.side == side else -s


_IMP_BOUNDS = (
    (20, 0), (50, 1), (90, 2), (130, 3), (170, 4), (220, 5), (270, 6), (320, 7),
    (370, 8), (430, 9), (500, 10), (600, 11), (750, 12), (900, 13), (1100, 14),
    (1300, 15), (1500, 16), (1750, 17), (2000, 18), (2250, 19), (2500, 20),
    (3000, 21), (3500, 22), (4000, 23),
)


def imps(score_diff: int) -> int:
    """Convert a score difference to IMPs (signed)."""
    d = abs(score_diff)
    result = 24
    for bound, imp in _IMP_BOUNDS:
        if d < bound:
            result = imp
            break
    return result if score_diff >= 0 else -result
