# Expert B — constructive / team-IMP review of `docs/dossier_575757/part03.md`

38 boards, -299 IMPs.  Read through the constructive lens: the uncontested
2/1 machinery, opener's and responder's rebid ladders, the invitational /
game boundary, trial bids, control-showing below game, and the shape-showing
that separates a minimum from a slam-going hand BEFORE game is reached.

## Summary

| | |
|---|---|
| boards reviewed | **38** |
| proposals (one per board) | **31** |
| NOTHING-WRONG | **7** (85, 113, 20, 306, 538, 544, 897) |
| VERIFIED (proposed `requires` traced through the live `EvalContext` at the real seat) | **26** |
| UNTESTED | 5 |
| negative prototypes reported rather than shipped | 2 (boards 376, 897) |

### The three agreements that matter most in this slice

1. **`fourth_suit_reply` is a starved answering seat** (board 945).  The
   fourth suit is the file's one game-forcing *ask* below 2NT and it has
   exactly two answers — "I have a stopper" and "I have three-card support".
   Opener holding neither (5-5, no stopper) tops out at **fit 0.349**, the
   soft-miss lottery hands him a three-card raise he does not have, and
   responder then asks for keycards on a 27-count.  A force whose answering
   seat cannot describe the answer is worse than no force at all.  Fix: two
   natural rungs and a floor, in the seat that already exists.

2. **The invitational rung is missing, so the game bid wins by default.**
   Boards 100, 325, 353, 488, 503, 528, 997 are all one species: at the
   decision the ladder offers a pass at fit 1.00 and a *game* at fit 1.00 or
   0.946, and nothing in between, so priority alone decides between "no
   interest" and "eleven tricks".  Round 17's density thesis, at the three
   level: **`uc_minor_game_5$m` outranks a fit-1.00 long-suit game try that
   is already in the file** (board 488), and `uc_raise_$M4` outranks the
   invitation on a doubleton because the invitation demands three trumps
   while the game bid accepts two (board 325).

3. **Trial bids are still at zero rules and this slice needs them twice**
   (boards 488 and 503, both reaching five of a minor with no try
   available).  Proposal 488 ships the long-suit game try *with the seat
   that answers it* — that is the whole point, and it is why the round-17
   above-game cue measured -9.8.

### Two conventions this slice would create from nothing

* **long-suit / help-suit game try after a minor raise** — `minor_game_try`
  plus `minor_game_try_answer` (boards 488, 503).
* **splinter after the 2C-2NT Stayman major fit** — the first shortness-
  showing slam try anywhere in the 2C tree (board 562).

### Method notes

* Fits below are the *real* fits: every "VERIFIED" line was produced by
  building the seat's live `EvalContext` with `prepare_decision` and scoring
  the proposed `HandConstraint` against the actual hand (`probe()` harness in
  the scratchpad; it never edits the YAML).  Where the proposal is a whole
  context I verified the rung that decides the board, not every rung.
* Every proposal states what it can outrank **below** as well as above.
* Contexts with anchored patterns shadow the generic toolkit for the calls
  they define, so each new anchored context below carries the shadowed
  generic rung verbatim and a `requires: {}` floor.  Contexts written
  `"... - P - ?"` do not need that and say so.

---
