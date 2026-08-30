# Expert B — constructive / team-IMP review of dossier part 01 (38 boards, -471 IMPs)

Reviewer B: uncontested constructive auctions — the 2/1 machinery, opener's and
responder's rebid ladders, the invitational/game boundary, and the shape- and
control-showing that separates a minimum from a slam-going hand **below game**.

## Summary

| | |
|---|---|
| boards in dossier | 38 |
| proposals with exact YAML | **20** |
| of those, traced through `repro`-equivalent ranking on a patched copy of the file | **18 VERIFIED** |
| proposals that recover the board's IMPs in a full engine-vs-engine rollout | **13** |
| NEGATIVE results reported rather than shipped | **3** (boards 222-alt, 443, 762) |
| NOTHING-WRONG / competitive (reviewer A's territory) | **18** |

**Method note — how "VERIFIED" was obtained.** `choose_bid` accepts a
`system_path`, so every proposal below was written into a *copy* of
`two_over_one.yaml` in scratch, loaded, ranked with `score_candidates`, and
where useful the whole auction was rolled out with the engine in both of our
seats. The repo file was never touched. Two traps were hit and are worth
recording: (1) `choose_bid` defaults to `use_arbitration=True` while
`match_ben` uses `decide_fast`, so a verification harness **must** pass
`use_arbitration: False` or it will report a call the match would never make —
this cost me one wrong reading on board 426; (2) `fast_decision` breaks ties by
`(priority, fit)` among candidates fitting >= 0.9, so two new rungs at the same
priority producing different calls make the decision `is_clear=False` and hand
it to arbitration. Give sibling rungs distinct priorities.

**Do not use `when: { partner_limited: ... }` in any of this.** Round 17 item 5
records that `partner_limited` reads `eval_ctx` where the parameter is named
`ctx`; the first YAML rule to use it raises `NameError`. Several of the
agreements below would be cleaner with it and are written without it.

## The three agreements that matter most in this slice

1. **The help-suit game try does not exist and its answering seat does not
   exist** (board 426, and the whole `1M - 2M` family). `responder_rebid_after_1M_raise`
   has exactly three rungs — pass / 3M / 4M — and the auction
   `1m - 1H - 1S - 2S` has *no context at all*, so opener's game try is decided
   by the generic `uc_raise_S3` at fit 0.946 (13 tables, mean **-1.85**).
   Proposal 426 ships the trial bid **and** the accept/decline seat, and is the
   single most templatable idea in this part.

2. **Every splinter in the file is responder's; opener has none, responder over
   opener's second suit has none, and Stayman has none** (boards 443, 318, 105,
   559). Four separate seats where a 19+ hand with shortness has only a blind
   jump to game. Three of the four recover their board in full when the
   splinter *and* its answering seat are shipped together; the fourth (443)
   correctly declines and is reported as a negative.

3. **A quantitative sequence whose accept rung is keyed to the wrong hand.**
   `qa_pass` fires on 6 tables at mean **-5.50** and `qa_6NT` needs 16 HCP — a
   floor that is right opposite a 15-17 notrump and absurd opposite a 22+ 2C
   opener (board 437), and there is no accept context at all after
   `1m - 2m - 2NT` (board 479). Both seats are starved, both are pure
   arithmetic, and both recover their board.

**A fourth, worth saying because it is a fact about the file rather than a
judgement:** `rrevd_3NT` — game opposite a reverse — **never fires in 1000
boards**, because its floor is 12 HCP when a reverse shows 17+. The generic
`uc_raise_D3` annexes that seat instead, at 14 tables and mean **-3.86**, and
on board 967 it agreed diamonds and launched a keycard ask into a 6D that went
down. A ladder whose rungs are banded against the wrong partner range is
indistinguishable from no ladder.

---
