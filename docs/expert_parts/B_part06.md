# Expert B — constructive / team-IMP review of `docs/dossier_575757/part06.md`

38 boards, -122 IMPs.  **27 proposals, 9 NOTHING-WRONGs, 1 proposal withdrawn on
whole-corpus evidence, 1 honest negative** (the agreement is right, the board
does not move).  22 of the 27 were traced through a modified copy of the system
YAML and are labelled **VERIFIED**; the harness is
`scratchpad/B_eyal_p06/proto.py` (`build(edits, out)` writes a patched YAML to a
scratch path, `show()` ranks against it; the repo YAML was never touched).

## Method notes that changed my own conclusions

* **`fires_summary` reversed one verdict and softened three.**  Board 433's
  proposal (a pass rung outranking `ch_new_long3_D`) is **withdrawn**:
  `ch_new_long3_D` runs **+4.33 IMPs a table over 3 tables** — the board in the
  dossier is its only loser and it is the most profitable rung I touched.
  Boards 98, 199 and 883 are marked lower-confidence for the same reason
  (`v3_D_X` +1.60, `sw_2H` -2.67 but the family is small, `bal_X` -0.21).
* **A context that `expand:`s over a variable which does not appear in its
  `pattern` produces N identical contexts and only the first is ever used.**
  My first draft of the board-674 context did this and three quarters of its
  rungs were dead.  Written out per suit instead.  This is a DSL trap worth
  recording; it is not in `DSL_FOR_EXPERTS.md`.
* **`we_hold_contract` does not mean "our side owns the standing bid".**  On
  board 905 the standing bid was partner's 1NT and `we_hold_contract` was
  `False`; `we_bid_last: true` is the condition that means what I wanted.
* **The primary-reading trap is live in this dossier.**  `cl_new_long2_H_hi`
  "decided" board 646 but `fires_summary` says it *never fires* — the recorded
  `rule` field is a different rung of the same call.  Every accusation below is
  re-ranked through `score_candidates`, not read off the dossier row.
* **`partner_limited` is unusable** (round 17 item 5: `NameError` on first use).
  Where I needed "partner has limited himself" I used the `partner_shown_max`
  evaluator, which works and gives clean numbers (7 / 8 / 10 / 11 / 40 on the
  boards below).

## The three agreements that matter most in this slice

1. **A reverse is forcing and there is no answer below 8 points** (board 506).
   `rrevh_2S` / `rrev_2$M` / `rrevd_2S` all floor at `hcp: [8, 40]`, so a
   six-card suit with four points has nothing that fits and `uc_pass` takes a
   one-round force at fit 1.00.  Ships with `opener_after_reverse_signoff`.
   Verified end to end: `1C-1S-2H-2S-P`, where we previously passed 2H out.
2. **Responder has no system over an overcall of our 1NT opening** (boards 674
   and 852).  Both seats fell to `general_competitive_low`, whose negative
   double wants 8+ HCP and whose natural two-level suit bid wants 10+, so an
   8-count with five diamonds and a 7-count with four hearts both passed.  A
   closed conversation — negative double, natural sign-offs, 3NT, catch-all
   pass — plus **the seat that answers the double**.  Verified end to end on
   both boards (2H making eleven; 3H making nine).
3. **Opener's third call after responder's simple preference has no context at
   all** (board 863), so `uc_raise_H4` — a rung written to raise *partner's*
   suit — bid game on a 15-count opposite a preference that showed 6-10.
   `opener_after_major_preference` (pass / 3H try / 4H) plus the seat that
   answers the try.

Honourable mention because of its rate: **`redouble_continuations` exists only
for minor openings and has no notrump rung at all.**  `rdc_pass_D` runs
**-6.75 IMPs a table over 4 tables**, the worst rate of any rung I looked at.
Boards 23 and 991 are the two halves of that hole.

---
