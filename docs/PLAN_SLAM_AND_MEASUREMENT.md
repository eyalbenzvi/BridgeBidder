# The plan: five items, in order

Written after the consolidated expert review (`docs/EXPERT_CONSOLIDATED_REVIEW.md`).
Two independent reviewers converged on one verdict: **six rounds were spent on
2-to-20-board fixes, in the part of the game where the engine is already at
parity, using a test too weak to see them.**  67% of the held-out deficit sits
on the 14% of deals where a slam exists; outside that band the engine runs
-0.18 IMPs a board.

The items are **strictly ordered**.  Item 1 is a precondition for believing any
number produced by items 2-5.  Do not reorder them.

Baselines at the time of writing: review corpus (seed 242424) **-677**,
held out (seed 828282) **-474**, both at commit `70201a7`.

---

## Item 1 — a measurement that can see the effects we care about

**Why first.**  `SE(paired delta) = 5.5 * sqrt(k)` IMPs for a change touching
`k` boards, because unchanged boards are bit-identical (both sides are
deterministic argmaxes).  Fixes touch 2-20 boards, so at a realistic 1 IMP per
changed board the current accept/reject test has **~17% power**.  Round 14's
headline is t=1.94; round 16 reverted on t=-0.62.  Keeping-if-positive on a null
effect pays +17 IMPs a round against an observed +61 across seven rounds.

**Build.**
1. A cached baseline of **20,000 boards** (20 seeds x 1000) at the current
   commit.  One-time, ~2h.
2. `tools/roundkit/screen.py`: given a candidate system, run `replay.py` over
   the cached corpus, collect only the boards where a recorded decision changes,
   and re-play **only those** against BEN.  Unchanged boards contribute exactly
   zero to the paired delta, so this is exact, not an approximation.
3. Report **t and a 95% CI**, never a bare delta.  Refuse to print a verdict
   when `k < 8`.

**Acceptance.**  Screened result on a known change reproduces the full-corpus
paired delta exactly (test on the round-14 fixes, whose numbers are recorded).
Power at 1 IMP/changed board >= 90%.

**Then retire the ratchet.**  The fixed held-out corpus has been the decision
rule sixteen times, so -474 is a running maximum, not an estimate.  Replace it
with: discovery on seeds you may look at freely, acceptance on **fresh seeds
drawn per experiment** from the 20k pool and never reused.

---

## Item 2 — a slam try that is not Blackwood

**This is where 67% of the loss is, and it is one project, not three fixes.**

Evidence: we bid **26 small slams to BEN's 63** and no grands to BEN's 3, and
**23 of our 26 made (88%, against BEN's 65%)** — at an IMP break-even near 50%
that is proof of massive under-bidding.  On 60 sampled seats where we pass our
own game holding 4+ controls and a singleton or void, the candidate set averages
**1.6 non-pass calls, best fit < 0.10 in 46 of 60, >= 0.90 in none.**

Three sub-parts, to be built together and measured together:

- **(a) Above game there is nothing.**  Cue bids are capped below 4M, exist only
  with a major agreed inside a formal game force, and every general context is
  gated `we_hold_contract: false` — which makes *reaching game* the terminal
  state of the whole system.  Author the seat that continues over our own game.
- **(b) The currency is wrong.**  `rule_of_26` credits partner with at most
  *minimum + 2* however wide his range, so a `>= 31` gate needs 17 opposite an
  unlimited hand; after 2C partner's floor is **zero by construction**.  `ltc`
  appears **once** in 14,937 lines against `rule_of_26`'s **104**.  Slam
  decisions want controls, losers and shortness, not points.
- **(c) The ask is undisciplined and the ladder stops.**  17 of our 47 keycard
  asks die at the five level, seven of them down, against BEN's 6 of 64.
  `gst_rkc_*` (Blackwood on a suit partner merely mentioned) fires 10 of 14
  times at board margin -39/-10 and par gap -12.1/-7.86.  **No rule in the file
  bids at the seven level**; 5NT exists only as a runout.

**Discipline.**  Every force, ask and invitation ships WITH the seat that
answers it.  A new context that shadows an existing one carries the shadowed
rule's gates verbatim.  Measure (a), (b), (c) separately once each is complete —
they interact through the same contexts, so a bundle is unattributable.

**Acceptance.**  Slams bid moves toward BEN's rate with a hit rate falling
toward 60-70% (a *falling* hit rate is the success signal here, not a
regression), and the 12-13-trick slice improves on fresh seeds.

---

## Item 3 — per-decision regret, with BEN in the opponents' seats

**Why.**  Par gap is jointly owned by a whole auction and is the direct cause of
the round-15 and round-16 false findings.  This replaces it with a per-decision
number that carries a standard error.

**Build.**  For a decision, substitute each plausible alternative call, roll the
auction out with **BEN in the opponents' seats** (today `engine/arbitration.py`
`rollout` uses our own engine in all four seats while the match is against BEN),
score double-dummy, and report the IMP difference.  Prototyped by the reviewer
at **91 ms/rollout, ~3.5 min per 1000-board corpus, mean -1.16 +/- 0.35 IMPs
over 320 substitutions.**

**Uses.**  A per-rule regret table with standard errors, replacing
`sweep.py --rank-rules`; and the steering signal for item 2.

**Acceptance.**  The regret table reproduces the sign of the round-14 shipped
fixes and of the round-16 arbitration revert.

---

## Item 4 — make the code fallback unconditional

**Why.**  `covered` is built without consulting fit, so adding a rung silently
deletes the code fallback for that call in every seat the rung's `when` reaches.
This is a trap every author must remember and it has already bitten twice.

**Build.**  Make the fallback unconditional and widen `interpret_call` to match.
Prototyped: **60 live decisions change, the soft-miss population drops 108 -> 21
(-81%).**

**Acceptance.**  Neutral-or-better on fresh seeds, and the guardrail can be
deleted from `ROUND_METHOD.md`.  This is a code change, not a YAML change.

---

## Item 5 — the deferred set

Only after items 1-4, and each measured alone on fresh seeds.

- **Learned priorities** as a pairwise ranking problem: 2,413 contested live
  decisions, 1,054 ordered rule pairs (144 with n>=5), ~150 identifiable
  parameters, signal = item 3's regret, pre-trainable on BEN's argmax.
- **One calibrated objective** (`log fit + priority/T`) replacing the 0.9 cliff
  plus max static priority.  Blast radius 2,521 decisions.  Cheap sub-experiment
  first: widen `is_clear` from an exact float tie (33 decisions) to a priority
  band (250 decisions, stage-adjusted -2.73).
- **The Law of Total Tricks reaching zero**: `cl_raise_lott3_$M` floors at 3
  total points *and* is `cheapest_in_suit`, so nine trumps and a bust has no
  raise at all.  Round 11 freed the flag but never the floor.  Note its own
  decomposition puts partscores near parity, so expect little.
- **Vulnerability and form of scoring**: 26 of 14,937 lines, 3 of 517 contexts.
  Good bridge, effect not demonstrable on this corpus.

---

## Two bugs to fix in passing

- `partner_limited` raises `NameError` — a landmine for the first YAML rule that
  uses it.
- `_SETUP_CACHE` is keyed on `id(system)` while holding no reference to it:
  unsound for any loop that rebuilds systems, and `tools/tune.py:211` does.

## Do not re-propose (each has a number that killed it)

Opening the 11-counts (IMP effect inverts between corpora); playing less
notrump (we are +65 choosing 3NT over an eight-card major fit); doubling more
(we already double 32% more, and `oc1H_X`/`oc1S_X` run 3 wins to 12 losses); the
"gates that don't gate" family (32 of 6,810 gates violated-yet-chosen, <= 0.3% of
decisions); the code fallback as a hole (461 of 470 are closing passes);
threshold tuning (-0.025 +/- 0.062).  Plus everything under "Known open items"
in `ROUND_METHOD.md`.
