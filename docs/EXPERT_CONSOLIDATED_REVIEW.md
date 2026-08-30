# Consolidated review: two experts, ten ideas, one conclusion

Commissioned after rounds 15 and 16 produced **zero** net movement.  A bridge
authority reviewed the *system*; an algorithms and ML engineer reviewed the
*machinery and the measurement*.  Neither saw the other's brief or report.

Full reports: `docs/EXPERT_BRIDGE_REVIEW.md`, `docs/EXPERT_ALGORITHMS_REVIEW.md`.

---

## The conclusion both arrive at, from opposite ends

**We have spent six rounds making 2-to-20-board fixes, in the part of the game
where we are already at parity, using a test too weak to see them.**

The bridge expert solved every board double-dummy and split the corpora by how
many tricks are actually available:

| deals where the best side can take… | e10: n / IMPs / per board | held: n / IMPs / per board |
|---|---|---|
| **12 or 13 (a slam is there)** | **137 / -267 / -1.95** | **144 / -320 / -2.22** |
| exactly 11 | 210 / -27 / -0.13 | 217 / **+127** / +0.59 |
| 10 or fewer | 653 / -383 / -0.59 | 639 / -281 / -0.44 |

**67% of the held-out -474 sits on the 14% of deals where a slam exists.**
Outside that band the engine runs **-0.18 IMPs a board** — near parity with a
neural net trained on expert auctions.

The supporting count is starker than the IMPs: we bid **26 small slams to BEN's
63**, no grand slams to BEN's 3 — and **23 of our 26 made, 88%**, against BEN's
65%.  The IMP break-even for bidding a small slam is about 50%.  An 88% hit rate
is not accuracy, it is proof of **massive under-bidding**: we bid only the ones
that cannot fail.  The slam machinery is sound; it almost never runs.

The algorithms expert, without seeing any of that, showed why six rounds of
partscore fixes could not have been validated even if they were real.  Unchanged
boards are bit-identical (both sides are deterministic argmaxes), so only changed
boards carry signal:

```
SE(paired delta) = 5.5 * sqrt(k) IMPs   for a fix touching k boards
```

Our fixes touch 2-20 boards.  At a realistic 1 IMP per changed board and k=15,
**the accept/reject test has 17% power.**  Consequences, all in our own record:

- Round 14's headline +51 is **t = 1.94** — best of ~20 candidates, in the
  fourteenth round of selection on the same 1000 boards.
- Round 16 reverted arbitration on **t = -0.62**, a measurement that cannot
  separate -13 from +30.  Its "level vs strain inversion" is two draws from one
  distribution.
- **Keeping-if-positive on a null effect pays +17 IMPs a round.**  Held out went
  -535 to -474 across seven rounds: **+61**, against a selection expectation of
  **~+85**.  Rounds 1-5 are unambiguously real; **at most one of the last eleven
  is individually distinguishable from noise.**

And the fixed held-out corpus has been the decision rule sixteen times, so -474
is a running maximum of a ratcheted walk, not an estimate of strength.

**The two findings explain each other.**  The measurement is blind at the scale
we were working, and we were working at that scale because the per-context
par-gap ranking pointed there — an instrument that is structurally blind to a
*uniformly* bad context, which is exactly what every slam context is.

---

## Consolidated plan, in order

### 1. Fix the measurement first (algorithms #1) — one round, ~2h compute

Screen with `replay.py` and re-play **only the boards a change actually
touches**.  Power at 1 IMP/changed board goes **17% -> 93%** and each experiment
gets **~3x cheaper**.  Build a 20,000-board cached baseline; report a t-statistic
and a CI, never a bare delta.

Nothing below is worth doing until this is in place, because nothing below can
be validated without it.

**In flight:** round 10 (`d775ad0`) vs HEAD on five fresh seeds never used as a
decision rule — the only unbiased estimate of what rounds 11-16 bought.

### 2. Build a slam try that is not Blackwood (bridge #1, #2, #3) — multi-round

This is one project, not three fixes, and it is where 67% of the loss is.

- **Above game there is nothing.**  On 60 sampled seats where we pass our own
  game holding 4+ controls and a singleton or void, the candidate set averages
  **1.6 non-pass calls, best fit < 0.10 in 46 of 60, and >= 0.90 in none.**  Cue
  bids are capped below 4M, exist only with a major agreed inside a formal game
  force, and every general context is gated `we_hold_contract: false`.
- **The currency is wrong.**  `rule_of_26` credits partner with at most
  *minimum + 2* however wide his range, so a `>= 31` gate needs 17 opposite an
  unlimited hand; after 2C partner's floor is **zero by construction**, which is
  why `open_2C` / `resp_2C` have resisted four rounds.  `ltc` appears **once** in
  14,937 lines; `rule_of_26` **104 times**.
- **The ask is undisciplined and the ladder stops.**  17 of our 47 keycard asks
  die at the five level, seven of them down, against BEN's 6 of 64.  `gst_rkc_*`
  — Blackwood on a suit partner merely mentioned — fires 10 of 14 times at board
  margin -39 / -10 and par gap -12.1 / -7.86.  **No rule in the file bids at the
  seven level**; 5NT exists only as a runout.

### 3. Per-decision regret, with BEN in the opponents' seats (algorithms #2)

Replaces par gap — jointly owned by a whole auction, and the direct cause of the
round-15 and round-16 false findings — with a per-decision number that has a
standard error.  Prototyped at **91 ms/rollout, ~3.5 min per 1000-board corpus,
mean -1.16 +/- 0.35 IMPs over 320 substitutions.**  It also fixes the arbitration
path's opponent model for free (today `rollout` finishes auctions with our own
engine in all four seats while the match is against BEN).

This is the steering signal the slam project needs.

### 4. Retire a guardrail in code (algorithms #3) — cheap

Make the code fallback unconditional and widen `interpret_call` to match.
Prototyped: 60 live decisions change, the soft-miss population drops **108 -> 21
(-81%)**, and "adding a rung deletes the fallback for that call" stops being a
trap authors must remember.

### 5. Everything else — later, and only after (1)

Learning the priorities as a pairwise ranking problem (algorithms #4: 2,413
contested decisions, ~150 identifiable parameters); one calibrated objective
instead of the 0.9 cliff plus max static priority (algorithms #5, blast radius
2,521 decisions); the Law reaching zero (bridge #4 — real, but its own
decomposition puts partscores near parity); vulnerability and form of scoring
(bridge #5 — good bridge, effect not demonstrable on this corpus, and ranked
last by its own author).

---

## Hypotheses that died on the data

Worth as much as the ideas, because each is a round nobody now has to spend.

| hypothesis | the number that killed it |
|---|---|
| open the 11-counts like BEN | frequency gap huge and replicating (37.8% vs 69.1%) but the **IMP effect inverts between corpora** |
| play less notrump | we are **+65** on boards where we chose 3NT over an eight-card major fit |
| double more like BEN | we already double **32% more**; `oc1H_X`/`oc1S_X` run 3 wins to 12 losses |
| the "gates that don't gate" family | only **32 of 6,810** gates on winning candidates were violated-yet-chosen — <= 0.3% of decisions; `suit_diff`, the largest-looking leak at 758 evaluations, produced **zero** |
| the code fallback is the biggest hole | 461 of 470 are closing passes (round 16) |
| threshold tuning | -0.025 +/- 0.062 held out (documented) |

## Two bugs found in passing

- `partner_limited` raises `NameError` — a landmine for the first YAML rule to use it.
- `_SETUP_CACHE` is keyed on `id(system)` while holding no reference to it: unsound for any tuning or learning loop that rebuilds systems, and `tools/tune.py:211` does exactly that.
