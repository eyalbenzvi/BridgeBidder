# The 12,000-deal pool and its data

`reports/` is gitignored and the container is ephemeral, which is how round 17
lost its pool. This directory is the durable copy.

## Restore it in a fresh session

```bash
mkdir -p reports/pool
for f in data/pool/*.gz; do gunzip -c "$f" > "reports/pool/$(basename ${f%.gz})"; done
gunzip -c data/ben_cache.sqlite.gz > reports/ben_cache.sqlite
gunzip -c data/r18_before_575757.jsonl.gz > reports/r18_before.jsonl
gunzip -c data/e10_before_242424.jsonl.gz > reports/e10_before.jsonl
gunzip -c data/held_before_828282.jsonl.gz > reports/held_before.jsonl
```

Then the screen works immediately, at ~98% BEN cache hits:

```bash
python3 tools/roundkit/screen.py run --pool reports/pool --label "..." --jobs 3
```

## What is here

| file | what it is |
|---|---|
| `pool/seed501..512.jsonl.gz` | **the 12,000-board pool.** 12 files × 1000 boards, played at commit `e97dd06` (the round-17 head, == round 18's baseline) |
| `ben_cache.sqlite.gz` | BEN's memoised answers, content-addressed. Makes a replay of the pool essentially free — without it, ~15 min per 1000 boards |
| `r18_before_575757.jsonl.gz` | seed 575757, **-489 IMPs**, the round-18 review corpus (302 lost boards) |
| `e10_before_242424.jsonl.gz` | seed 242424, **-677** |
| `held_before_828282.jsonl.gz` | seed 828282, **-474**, the historic held-out corpus |

## The pool's baseline scores (round-17 head)

| seed | score | seed | score |
|---|---|---|---|
| 501 | -769 | 507 | -618 |
| 502 | -406 | 508 | -644 |
| 503 | -743 | 509 | -627 |
| 504 | -280 | 510 | -907 |
| 505 | -470 | 511 | -757 |
| 506 | -999 | 512 | -638 |
| | | **total** | **-7858** (-654.8 / 1000) |

## One row per board — the schema

Each line of a pool file is one board, self-contained:

```
board, dealer, vul, hands{N,E,S,W}, par_ns,
a_score_ns, a_contract, a_auction, a_our_calls[{seat,call,rule,n}],
b_score_ns, b_contract, b_auction, b_our_calls[...],
imp_margin,          # + = we win
a_par_gap, b_par_gap # N/S-signed at BOTH tables: ours is +a_par_gap and -b_par_gap
```

Table A = we are N/S (BEN sits E/W); table B = we are E/W. `a_our_calls[].rule`
is the **primary reading** (the highest-priority rule producing that call), NOT
necessarily the rule that chose it — use `roundkit/sweep.deciding_rule()` for
the chooser. That distinction has produced false findings three times.

## The deals themselves are reproducible without any of this

They are a pure function of the seed, so a new session can regenerate the 52
cards of every board with no BEN, no engine and no solver:

```python
import random
from bridgebidder.domain.cards import FULL_DECK
from bridgebidder.domain.types import Seat
rng = random.Random(SEED)                 # 501..512
for bi in range(1000):
    deck = list(FULL_DECK)
    rng.shuffle(deck)                     # deal order matters: shuffle per board, one rng
    deal = {s: deck[j*13:(j+1)*13] for j, s in enumerate(Seat)}
    dealer, vul = Seat.from_index(bi % 4), VULS[(bi // 4) % 4]
```

What is *not* reproducible for free is the played data — BEN's auctions, the
contracts, the double-dummy tricks and the scores. That is what the two
gzipped artefacts above buy you.

## Seeds already used — do not reuse for a fresh corpus

7, 131313, 151515, 161616, 171717, 242424, 303030, 313131, 323232, 343434,
353535, 363636, 401-407, 501-512, 515151, 575757, 626262, 747474, 828282,
858585, 919191, 969696.
