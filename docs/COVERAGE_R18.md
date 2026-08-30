# The ranked authoring backlog, measured (round 18)

`tools/roundkit/coverage.py` was written in round 17 and never run.  Run here
on the 575757 corpus (10,335 of our decisions), it produced a finding about
its own instrument before it produced one about the file.

## The instrument was wrong, and the correction is the finding

As written it bucketed every decision as KNOWS (a rule fits >= 0.9 and wins),
GUESSES (a rule wins below the fast-path threshold — the soft-miss lottery) or
NOTHING (the code fallback decides).  On that scale the file looks healthy:

```
KNOWS  94.5%    GUESSES 1.0%    NOTHING 4.5%     backlog 5.5%
```

**That number is an artefact.**  A rule whose `requires` is empty fits **1.00
against every hand**, so every catch-all pass and every unconditioned sign-off
— precisely the starved seats this round exists to find — was being counted as
an agreement.  Splitting them out as **VACUOUS**:

| bucket | all decisions | live decisions only |
|---|---|---|
| KNOWS — a rule with real content fits >= 0.9 | 5,735 (55.5%) | 5,519 (76.0%) |
| **VACUOUS — the winning rule requires nothing** | **4,031 (39.0%)** | **1,633 (22.5%)** |
| GUESSES — soft-miss lottery | 105 (1.0%) | 103 (1.4%) |
| NOTHING — code fallback | 464 (4.5%) | 9 (0.1%) |
| **authoring backlog** | **4,600 (44.5%)** | **1,745 (24.0%)** |

"Live only" drops calls that merely end an auction already over, which is
round 16's lesson (a closing call inherits the auction's par gap and explains
nothing) and is the honest denominator.  It also confirms that lesson from the
other side: **463 of the 464 code-fallback decisions are closing passes.**

**So the real number is that about a quarter of our live decisions are made by
a rule that describes no hand.**  That is the density thesis, quantified, on
the same corpus the round's rules were found on.

## The backlog by context, live decisions only

| context | vacuous | guess | none | knows |
|---|---|---|---|---|
| `general_competitive_low` | 783 | 1 | 0 | 255 |
| `general_competitive_high` | 592 | 0 | 0 | 85 |
| `general_uncontested_continuation` | 89 | 16 | 0 | 314 |
| `general_their_double` | 74 | 0 | 0 | 65 |
| `resp_2C` | 17 | 0 | 0 | 3 |
| `nt_transfer_accept_S` | 16 | 0 | 0 | 1 |
| `nt_transfer_accept_H` | 12 | 0 | 0 | 0 |
| `cue_bidding_S` | 10 | 0 | 0 | 6 |
| `gf_landing_nt` | 0 | 8 | 0 | 14 |
| `sandwich_seat[C]` | 0 | 6 | 0 | 101 |
| `general_after_redouble` | 5 | 0 | 0 | 13 |
| `opener_rebid_1M_1NT[S]` | 0 | 5 | 0 | 21 |
| `cue_bidding_H` | 5 | 0 | 0 | 0 |

Two of the four generic competitive contexts account for **1,375 of the 1,745
backlog decisions**.  `general_competitive_low` and `general_competitive_high`
are where the file runs out of vocabulary, by a factor of five over anything
else, and the repair there is more rungs rather than a better rung.

Read with the whole-file counts from round 17 — trial bids 0, serious 3NT 0,
mini-splinters 0, fit-showing jumps 0, control-showing raises 0, seven-level
rules 0 — this is the ranked authoring list the scaling plan asked for.
