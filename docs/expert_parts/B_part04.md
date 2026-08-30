# Expert B — constructive / team-IMP review of dossier part 4

**Scope.** All 38 boards of `docs/dossier_575757/part04.md`, read through the
constructive-auction lens: the 2/1 machinery, opener's and responder's rebid
structures, the invitational/game boundary, game tries, and the shape-showing
that separates a minimum from a slam-going hand *before game is reached*.

**Counts.** 38 boards · **31 proposals** (each with exact YAML) · **7
NOTHING-WRONG** (boards 93, 116, 272, 274, 704 — opening-style thresholds,
scope-excluded; 343, 894 — purely competitive with the observation recorded).
20 of the 31 proposals are **VERIFIED** — I traced the seat through
`repro.rank()` / `repro.ask()` and quote the fit and priority that decided it.

## The three agreements that matter most in this slice

1. **Responder's invitational jump rebid over opener's second suit has no
   answering seat at all.** `r1d1h2c_3H` and `r1d2c_3S` establish
   `forcing: invitational` and then land in `general_uncontested_continuation`,
   where `uc_pass` fits **1.000** and opener passes a live invitation with a
   fitting hand. VERIFIED on boards 132 and 563; both were cold games passed
   out at the three level. This is the round-17 finding in its purest form —
   the machinery is at the three level, and the question exists while the
   answer does not. Proposal: the `opener_over_responder_jump_rebid` context
   (§Board 132), plus a game-forcing tier so 14+ never has to invite.

2. **The invitational/game-force boundary at exactly 12 HCP is decided by
   priority, not by bridge.** `r1m_2over1` / `r1H_2C` sit at priority 70-75
   with a floor of 12 HCP; `r1m_2NT` (11-12 balanced) and `r1H_limit_raise`
   (8-11 HCP, 10-13 support points) both fit or nearly fit the same hands but
   sit at 54 and 62. A flat 12-count with three-card support or no fit is
   force-fed into a game force it cannot survive. VERIFIED on boards 348 and
   782. Proposal: two re-priced rungs, `r1m_2NT_flat` and
   `r1H_limit_raise_flat` (§Boards 348, 782).

3. **Trial bids and help-suit game tries are still at zero rules, and the one
   rung that stands in for them — `op_after_raise_inv` (3M on 17-18 total
   points) — cannot say WHERE the help is needed.** Proposal: a complete
   help-suit-try conversation (opener's try, responder's accept/decline,
   both templated over both majors and all three trial suits) in §Board 188.

Two further structural species recur and are worth naming once:

* **`cheapest_in_suit: true` on a JUMP rung makes the rung unreachable** —
  the documented `cl_raise_lott3_$M` bug, found again on `cl_raise_D3`
  (board 632), `xd_rebid_D3` (board 707) and their whole sibling families.
  Every constructive jump raise in competition is dead code for this reason.
* **`lott_total_trumps` counts partner's SHOWN minimum**, so after a PASS it
  is zero and after a one-level major response it is four; every rung gated on
  8+ or 9+ combined trumps is unreachable in exactly the seats where opener
  wants to raise or jump (boards 658, 707).

---
