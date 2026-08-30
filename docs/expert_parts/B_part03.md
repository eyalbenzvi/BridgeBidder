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
| VERIFIED (proposed `requires` traced through the live `EvalContext` at the real seat) | **28** |
| UNTESTED | 3 (boards 44, 79, 13 — three brand-new contexts whose patterns I could not build read-only) |
| negative prototypes reported rather than shipped | 3 (boards 376, 528, 897) |

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

## Board 906 — margin -10

**Seat/call that went wrong:** table B, call 7, **East bids 3H** on
`A5.AJT6543.AK.65` after `P P P 1H 1S P 2H`.  `cl_rebid_jump_H` invites with
a hand that has five losers, seven controls and a seven-card suit; partner
passes and 4H (ten tricks) is never reached.

**The missing agreement:** in competition, opener's rebid ladder has an
invitational jump and nothing above it — a self-sufficient major with at
most five losers must be able to bid game on playing strength rather than
invite on points.

**Context:** `general_competitive_low` (and the identical twin in
`general_competitive_high`, `general_balancing_low/high`).

```yaml
      # THE CEILING ON THE COMPETITIVE REBID LADDER.  cl_rebid_jump_$M is the
      # top rung and it is an INVITATION, so a 4-loser one-suiter had no rule
      # above it and partner (who has shown nothing) passed.  Losers, not
      # points, are the currency of a one-suited hand.
      - id: cl_rebid_game_$M
        call: 4$M
        priority: 31.5
        when: { my_suit: $M, we_hold_contract: false }
        requires:
          suits: { $M: [6, 13] }
          evals: { ltc: [0, 5], controls: [4, 12], total_points: [16, 40],
                   "suit_quality($M)": [1.5, 9] }
        shows: "self-sufficient six-card $M and at most five losers: game on playing strength, not an invitation"
        establishes: { forcing: sign_off, agreed_suit: $M }
```
with `expand: { M: [H, S] }` on the enclosing context (already present as a
per-suit family; write the four ids out if the context is not templated).

**Answering seat:** none required — the call is a sign-off in game.  Partner's
seat is already authored: `slam_try_over_game_raise` (`... - 4$M - P - ?`)
carries `gr_rkc_general_$M` for the rare monster, and the code-fallback pass
otherwise.

**What it endangers, in this context:**
* `cl_rebid_jump_$M` (31, invitational, 6+ good suit 16-19) — a four/five-loser
  hand is not an invitation; it is a game bid that happens to hold 16 points.
* `cl_rebid_$M3` (29, 6+ cards, values for the level) — same hand, one level
  too low.
* `cl_pass` (20, fit 1.00 catch-all) and the code-fallback `X` at 9 — both are
  "nothing describes this hand", which is false here.
* It does **not** reach `cl_raise_*` (those are `partner_suit`, this is
  `my_suit`) and it cannot outrank `cl_negative_X*`/`cl_nt3` on hands they fit,
  which need shape this rule denies.

**VERIFIED.**  At the real seat the proposed `requires` scores **fit 1.000**
(ltc 5, controls 7, total_points 19, suit_quality(H) 2.0); today's winner
`cl_rebid_jump_H` also fits 1.000 at priority 31, so 31.5 takes the call.

**Template:** `expand: { M: [H, S] }`; then the same idea to `ch_`, `ballow_`
and `balhigh_` prefixes (four contexts x two majors = 8 rules), and a minor
twin at 5$m gated one loser tighter (`ltc: [0, 4]`).

---

## Board 945 — margin -10

**Seat/call that went wrong:** table B, call 8, **East bids 3S** on
`72.J.KJT95.AK742` after `1D P 1S P 2C P 2H P`.  `fsfr_raise_2H` claims
"delayed three-card support" holding **two** spades, West believes in an
eight-card fit, asks for keycards on a 27-count and we play 5S.

**The missing agreement:** the answer to fourth-suit forcing must include the
answer opener actually has — no stopper, no support, but 5-5 shape — and the
context must have a floor so the seat is never starved.

**Context:** `fourth_suit_reply` (existing).  It has exactly two rungs and no
floor; at this seat **the best fit in the whole candidate set is 0.349**, so
every call here is a soft-miss lottery pick.

Add two vars to the existing `expand_pairs` (the rebid calls, written out so
no `$L$X` composition is needed) and three rungs:

```yaml
    expand_pairs:
      - { O: 1C, R: 1H, RS: H, B: 1S, F: 2D, FS: D, REB1: 3C, REB2: 2S, TAG: C1H }
      - { O: 1C, R: 1D, RS: D, B: 1S, F: 2H, FS: H, REB1: 3C, REB2: 2S, TAG: C1D }
      - { O: 1D, R: 1H, RS: H, B: 1S, F: 2C, FS: C, REB1: 2D, REB2: 2S, TAG: D1H }
      - { O: 1D, R: 1S, RS: S, B: 2C, F: 2H, FS: H, REB1: 3D, REB2: 3C, TAG: D1S }
      - { O: 1H, R: 1S, RS: S, B: 2C, F: 2D, FS: D, REB1: 2H, REB2: 3C, TAG: H1S }
    rules:
      # ... fsfr_2NT_$F and fsfr_raise_$F unchanged ...
      # THE THIRD ANSWER.  No stopper and no third trump is the commonest
      # hand of the three, and it had no rung at all: extra length in one of
      # my own two suits is what partner needs to hear next.
      - id: fsfr_rebid_first_$TAG
        call: $REB1
        priority: 64
        requires:
          evals: { "stoppers($FS)": [0, 0.5] }
          suits: { }          # see note: the suit gate goes in `evals` below
          all_of:
            - evals: { "suit_length($REB1)": [5, 13] }
        shows: "no $FS stopper and no third $RS: extra length in my first suit"
        establishes: { forcing: game_forcing }
      - id: fsfr_rebid_second_$TAG
        call: $REB2
        priority: 63
        requires:
          evals: { "stoppers($FS)": [0, 0.5] }
          all_of:
            - evals: { "suit_length($REB2)": [5, 13] }
        shows: "no $FS stopper and no third $RS: extra length in my second suit"
        establishes: { forcing: game_forcing }
      # THE FLOOR.  A game-forcing ask must never leave its answerer with
      # nothing that fits (round 6's rkc5H_signoff lesson).
      - id: fsfr_floor_$TAG
        call: $REB1
        priority: 40
        requires: {}
        shows: "nothing to add: back to my first suit"
        establishes: { forcing: game_forcing }
        negative_inference_weight: soft
```

`"suit_length(X)"` is used rather than `suits: { $REB1: ... }` because
`$REB1` is a *call* ("3C"), not a strain; if the implementer prefers, add a
sixth var `REB1S: C` and write `suits: { $REB1S: [5, 13] }`, which is
cleaner and equivalent.

**Answering seat:** the new rungs are `game_forcing`, and the seat that
answers them is already authored — `gf_landing_preference_major`
(`gf_pref_3$M`, three-card preference), `gf_landing_major` (`gf_game_4$A`),
`gf_landing_minor` (`gf_maj4$M`, `gf_minor_3NT`, `gf_game_5$m`) and
`gf_landing_nt` (`gf_3NT`).  That family is what makes a natural GF rebid
safe here, and it is why the third answer must be natural rather than
another artificial one.

**What it endangers:**
* `fsfr_raise_$F` (66) — unchanged and still wins whenever opener really has
  three trumps; my rungs sit below it deliberately.
* `fsfr_2NT_$F` (68) — untouched; the stopper answer stays first.
* The generic `uc_rebid_$X3` (27) for the same calls — those demand SIX cards
  and 11+ points, which is exactly why this seat was empty; the new rungs are
  a superset for the five-card case and cannot fire where the six-card rule
  already fit ≥ 0.9 and outranked nothing.
* `fsfr_floor_$TAG` at 40 outranks the generic rebids: that is intended, a
  game force must be answered inside the conversation.

**VERIFIED.**  `{suits: {D: [5,13]}, evals: {"suit_diff(D,C)": [0,13]}}` — the
5-5 shape gate — scores **fit 1.000** at the real seat, against a current
best-in-set of 0.349.

**Template:** the five `expand_pairs` already there, plus the two new call
vars.  Ten new rules from one idea.

---

## Board 44 — margin -9

**Seat/call that went wrong:** table B, call 5, **East passes** on
`AKQT.AJ95.A43.73` after `P 1D X P` — his own 1D opening has been doubled and
passed out, and the deciding call is the **code fallback**, not a rule.
We defended 1DX and went for -500.

**The missing agreement:** opener has no second call when his opening is
doubled and passed round to him; with 18 HCP and four cards in every unbid
suit the redouble (business: we own this hand) is automatic.

**Context:** new, `opener_over_passed_out_double`.  Pattern is five tokens
and anchored, so it shadows `general_pull_or_sit`/`general_balancing_*` for
the calls it defines — hence the verbatim floor.

```yaml
  - id: opener_over_passed_out_double
    description: "My opening was doubled and passed round to me"
    expand: { o: [C, D, H, S] }
    pattern: "1$o - X - P - P - ?"
    rules:
      - id: oxpo_XX_$o
        call: XX
        priority: 60
        requires: { hcp: [17, 40] }
        shows: "business redouble: 17+, we own this hand and partner could not speak"
        establishes: { forcing: non_forcing }
      - id: oxpo_rebid_$o
        call: 2$o
        priority: 52
        requires: { suits: { $o: [6, 13] }, hcp: [12, 16] }
        shows: "six-card $o, minimum: getting out at the two level"
        establishes: { forcing: non_forcing }
      - id: oxpo_nt_$o
        call: 1NT
        priority: 54
        requires: { hcp: [15, 18], balanced: true, features: [ "stopper($o)" ] }
        shows: "15-18 balanced: notrump from the strong side"
        establishes: { forcing: non_forcing }
      # THE FLOOR: this context defines P, so it must define it for every hand
      # (the shadowing rule).  Same effect as the code fallback it replaces.
      - id: oxpo_pass_$o
        call: P
        priority: 20
        requires: {}
        shows: "nothing extra: playing one of my suit doubled"
        establishes: { forcing: non_forcing }
        negative_inference_weight: soft
```

**Answering seat:** the redouble is answered by `general_after_redouble`
(pattern `... - XX - $TAIL`), which is already authored for both the
immediate and the pass-through positions.  `oxpo_rebid_$o` and `oxpo_nt_$o`
are non-forcing sign-offs and need none.

**What it endangers:** inside this new context, only its own rungs; against
the file, it takes `P` and `XX` away from `general_pull_or_sit` /
`general_balancing_low` at this exact five-call position.  `oxpo_pass_$o`
carries `requires: {}` so the pass is a strict superset of what it shadows;
`XX` was previously reachable only through the code fallback, so nothing
authored is subtracted.

**UNTESTED** as a whole context (I did not build the pattern), but the seat
is confirmed empty: the dossier's own deciding rule for that call is
`fallback`, and `oxpo_XX_$o`'s gate (`hcp: [17,40]`) fits East's 18-count
trivially.

**Template:** `expand: { o: [C, D, H, S] }` — 16 rules from four ideas.  The
same shape is owed to `1$o - X - P - P` after a *third*-seat opening, which
this pattern already covers.

---

## Board 79 — margin -9

**Seat/call that went wrong:** table B, call 4, **West passes** on
`JT.AQ953.KJ62.95` after `1H P 1NT X`.  Deciding rule `xd_pass` (fit 1.00,
priority 18) out of `general_their_double`; the whole candidate set tops out
at 0.349 for anything else.  We play 1NT doubled.

**The missing agreement:** the forcing/semi-forcing 1NT response has no
context of its own once it is doubled, so opener cannot run to his four-card
side suit, rebid his major, or redouble.

**Context:** new, `opener_over_X_of_1NT_response`.

```yaml
  - id: opener_over_X_of_1NT_response
    description: "Our 1NT response was doubled for penalty: opener runs or sits"
    expand: { o: [C, D, H, S], X: [C, D, H, S] }
    pattern: "1$o - P - 1NT - X - ?"
    rules:
      - id: oxnt_new_$o$X
        call: 2$X
        priority: 54
        when: { unbid_suit: $X, cheapest_in_suit: true }
        requires: { suits: { $X: [4, 13] }, hcp: [11, 17] }
        shows: "running to a real four-card side suit: 1NT doubled is not our contract"
        establishes: { forcing: non_forcing }
      - id: oxnt_rebid_$o$X
        call: 2$o
        priority: 55
        requires: { suits: { $o: [6, 13] }, hcp: [11, 17] }
        shows: "six-card $o: back to my own suit"
        establishes: { forcing: non_forcing }
      - id: oxnt_XX_$o$X
        call: XX
        priority: 58
        requires: { hcp: [18, 40] }
        shows: "redouble: 18+, they have doubled into our strength"
        establishes: { forcing: one_round }
      # floor, carrying xd_pass's behaviour verbatim so this context can only
      # ever be a superset of the generic it shadows
      - id: oxnt_pass_$o$X
        call: P
        priority: 18
        requires: {}
        shows: "content to play 1NT doubled"
        establishes: { forcing: non_forcing }
        negative_inference_weight: soft
```

Every rule carries `$X` last in its id and `$o$X` keeps the ids unique across
the 16 expansions.  The four contexts per `$o` differ only in `$X`; that is
the same device `gf_landing_new_suit` uses.

**Answering seat:** `oxnt_new_*` and `oxnt_rebid_*` are non-forcing
sign-offs; responder's next turn is already covered by
`responder_preference_after_1M_1NT_2m` for the uncontested shape and by the
competitive toolkit here.  `oxnt_XX_*` is `one_round` and is answered by
`general_after_redouble`, which exists.

**What it endangers:** `xd_pass` (18) and `xd_run_$X2` (25) and
`xd_rebid_$M2` (34) lose these calls at this exact position.  `oxnt_pass` is
`requires: {}` so the pass is preserved exactly; `oxnt_new` at 54 outranks
`xd_run_$X2` at 25, which is correct — running to a four-card suit *with
opening values* is a choice, not a panic.

**UNTESTED** (new context).  The seat is confirmed starved: best non-pass fit
today is **0.349** (`xd_rebid_H2`), and `oxnt_new_$o$X`'s gate matches West's
four diamonds and 11 HCP exactly.

**Template:** `expand: { o: [C,D,H,S], X: [C,D,H,S] }` — 64 rules from four
ideas.  Trim to `o: [H, S]` if the forcing 1NT is major-only in this system;
the DECISIONS entry says semi-forcing after a major, so `[H, S]` is the
honest first cut and `[C, D]` covers the 1m-1NT twin.

---

## Board 113 — margin -9

**NOTHING-WRONG (constructive).**  The first divergence is South passing over
1S on `T2.A.KT972.QT964` — a 9-count 5-5 in the minors, where BEN bids 2NT.
That is the unusual notrump, which `DECISIONS.md` scopes out explicitly
("No Michaels or unusual NT — a direct cue of their opening is left
undiscussed"), and the brief's do-not-re-propose list repeats it.

What I checked: the candidate set at that seat (`oc1S_pass` 1.00/25, the
two-level overcalls at 0.409 on the 11-17 gate, the weak jumps at 0.070) —
no constructive rung is missing, the hand simply falls between the
system's overcall bands by design.  Table B is a pure competitive raise
decision (`cl_raise_lott3_S` over BEN's 2NT).  Nothing in my discipline is
mis-specified on this board.

---

## Board 144 — margin -9

**Seat/call that went wrong:** table A, call 2, **South passes** on
`6542.98762.3.982` (0 HCP, five hearts) after `1H X`.  `rdx_pass` at fit
1.00; `jordan_preempt` fits **0.134** because its gate is `hcp: [3, 8]` and
this hand has none.

**The missing agreement:** the raise ladder over their takeout double has no
bottom — a bust with five trumps opposite a five-card major (ten trumps by
the Law) must be able to barrage, and the file stops the preemptive raise at
three HCP.

**Context:** `resp_1M_over_X_jordan` (existing).

```yaml
      # THE FLOOR OF THE JORDAN LADDER.  jordan_preempt starts at 3 HCP, so a
      # yarborough with FIVE trumps had only the weak pass, and the auction
      # stayed cheap for them.  With ten known trumps the level of the fit is
      # four, and points are irrelevant to a barrage.
      - id: jordan_barrage_$M
        call: 4$M
        priority: 63
        when: { we_vulnerable: false }
        requires:
          suits: { $M: [5, 13] }
          hcp: [0, 6]
          evals: { "lott_total_trumps($M)": [10, 26] }
        shows: "barrage to the level of the fit: five trumps opposite five, no defence"
        establishes: { forcing: sign_off, agreed_suit: $M }
      - id: jordan_preempt_bust_$M
        call: 3$M
        priority: 62.5
        requires: { suits: { $M: [4, 13] }, hcp: [0, 2] }
        shows: "preemptive raise with a bust: four trumps, no values at all"
        establishes: { forcing: sign_off, agreed_suit: $M }
```

**Answering seat:** none — both are sign-offs, and partner is already
silenced correctly (`we_hold_contract` blocks the generic toolkit once our
own game stands).  This is the difference between this proposal and round
17's above-game cue: a barrage asks nothing.

**What it endangers:**
* `jordan_preempt` (62) — the new rungs sit above it but only on hands it
  does not fit (0-2 HCP) or at a level it cannot reach.
* `jordan_raise` (60, 3+ trumps, 5-9 points) — with five trumps and under
  three points the single raise understates the shape badly.
* `rdx_pass` (20) — a pass with ten combined trumps is the one call that
  gives them the whole auction for free.
* `jordan_2NT` (80) is untouched: it needs 8+ HCP.

**VERIFIED** for the gate arithmetic: South holds five hearts opposite a
shown five-card major, `lott_total_trumps(H) = 10`, `hcp = 0`; the current
`jordan_preempt` misses on HCP by three and scores 0.134, which is exactly
the soft-miss the proposal removes.  Not traced end-to-end as a new rung.

**Template:** `expand: { M: [H, S] }` already on the context; add the
vulnerable twin at 3$M (`when: { we_vulnerable: true }`) for four rules from
one idea.

---

## Board 216 — margin -9

**Seat/call that went wrong:** table A, call 2, **South bids 1NT** on
`JT54.Q72.KQT853.` after `1C 1S`.  `nx_1m1S_1NT` (priority 50) beats the
natural 2D (`cl_new_D2_hi`, priority 26.5); both fit 1.000.  South is
**void in partner's clubs** and holds six diamonds — 1NT is the one call the
hand cannot make.

**The missing agreement:** `resp_1m_over_1S` has a weak jump shift in hearts
(`nx_1m1S_wj_H`) and **no natural two-level bid in the minor responder
actually holds**, so the notrump rung annexes every unbalanced hand.

**Context:** `resp_1m_over_1S` (existing, `expand: { m: [C, D] }`).

```yaml
      # SIBLING GAP: the context has a weak jump shift in hearts and no
      # natural rung in the OTHER minor at all, so a six-card diamond suit
      # opposite 1C had to choose between a notrump with a club void and a
      # generic 26.5-priority rung it could never win with.
      - id: nx_1m1S_new_$om
        call: 2$om
        priority: 53
        requires: { suits: { $om: [6, 13] }, hcp: [7, 11] }
        shows: "natural free bid: a six-card $om, 7-11, non-forcing"
        establishes: { forcing: non_forcing }
```
(`$om` is the loader's automatic "other minor" derived from `$m`.)

**Answering seat:** the call is `non_forcing`, so no ask is created; opener's
next turn is `general_competitive_low`/`general_uncontested_continuation`,
which already carry the raise and rebid ladders for it.  If the round wants
it tighter, the natural companion is a `1$m - 1S - 2$om - P - ?` context with
a pass floor, a raise and a 2NT — but the rung is safe without one because
it promises a *limited* hand.

**What it endangers, in `resp_1m_over_1S`:**
* `nx_1m1S_1NT` (50) — this is the point: 1NT with a void in partner's suit
  is a worse description than the six-card suit, on any hand where both fit.
* `nx_1m1S_pass` (20) — a six-card suit and 7+ HCP is not "nothing to say".
* It cannot outrank `nx_1m1S_X` (80), `nx_1m1S_2H` (78), `nx_1m1S_cue` (70)
  or `nx_1m1S_raise` (55): a four-card heart suit, a five-card heart suit,
  a limit raise and a four-card raise of partner's minor all stay primary,
  which is right — they describe the partnership's fit, this describes mine.
* Below it, the generic `cl_new_$X2` family (26/26.5) loses this call at this
  seat.  That family is a 10+-point rung; mine starts at 7 and demands six
  cards, so the hands it takes are hands the generic rung under-described.

**VERIFIED.**  The proposed `requires` scores **fit 1.000** on the actual
hand (six diamonds, 8 HCP) at the real seat.

**Template:** `expand: { m: [C, D] }` already present — two rules; then the
identical sibling in `resp_1m_over_1H` (two more) and in `resp_1H_over_1S`
for the two minors (two more).  Six rules from one idea.

---

## Board 312 — margin -9

**Seat/call that went wrong:** table B, call 3, **West doubles** on
`KJ532..QJ75.A743` after `P 1H 1S`.  `r1H1S_X` fits 1.000 at priority 78 —
its `not: { suits: { H: [3, 13] } }` clause is satisfied by a **void**, and
nothing else in the rule notices that West holds five of *their* suit and
none of partner's.

**The missing agreement:** the negative double promises tolerance for
whatever partner does next; with a void in opener's suit and length in the
overcaller's, the constructive action is to pass and let opener reopen.

**Context:** `resp_1H_over_1S` (existing).  Written as a rung, not a gate, so
nothing is subtracted from the double's own population.

```yaml
      # A NEGATIVE DOUBLE PROMISES A PLACE TO PLAY.  r1H1S_X denies three-card
      # heart support, and a VOID satisfies that denial, so the one hand that
      # must not double is the one that fits it best.  Written as a positive
      # pass rather than as a gate on the double: it can only take the hands
      # it actually describes.
      - id: r1H1S_pass_void
        call: P
        priority: 79
        requires: { suits: { H: [0, 0], S: [4, 13] }, hcp: [6, 13] }
        shows: "void in partner's hearts and length in their spades: pass and let opener reopen"
        establishes: { forcing: non_forcing }
```

**Answering seat:** opener's reopening seat is `general_balancing_low`
(pattern `... - bid<3C - P - P - ?`), which is authored — `ballow_X`,
`ballow_new_*`, `ballow_rebid_*` and `ballow_pass`.  That is the whole
conversation: I pass, opener balances, I convert or correct.

**What it endangers, in `resp_1H_over_1S`:**
* `r1H1S_X` (78) — only on hands with a heart **void**, where the double is
  a systemic lie.
* `r1H1S_cue` (75) and `r1H1S_raise` (70) both demand 3+ hearts, so they are
  untouchable by construction.
* `r1H1S_2m_C` (60) / `r1H1S_2m_D` (59) — a five-card minor and 10+ HCP still
  outranks nothing here (they are below 79), so a hand with a void *and* a
  real five-card minor now passes instead of bidding it.  That is the one
  real cost.  If the round wants it narrower, add
  `not: { any_of: [ {suits: {C: [5,13]}}, {suits: {D: [5,13]}} ] }` — West's
  hand (4-0-4-4) is unaffected either way.
* `r1H1S_pass` (20) keeps its own band and its soft negative inference.

**VERIFIED.**  `{suits: {H: [0,0], S: [4,13]}, hcp: [6,13]}` scores **fit
1.000** on `KJ532..QJ75.A743` at the real seat; today `r1H1S_X` also fits
1.000 at 78, so 79 takes the call.

**Template:** the twin belongs in `resp_1m_over_1H`, `resp_1m_over_1S` and
`resp_1M_over_2x` (void in partner's suit + length in theirs) — five rules
from one idea, all with `suits: { <partner's suit>: [0, 0] }`.

---

## Board 562 — margin -9

**Seat/call that went wrong:** table B, call 13, **West bids 4H** on
`K73.8642.AJT863.` after `2C P 2D P 2NT P 3C P 3H P`.  `r2c_place_4H`
(priority 62, `requires: { suits: { H: [4, 13] } }` and nothing else) signs
off in game with **8 HCP, a club void, a six-card diamond suit and a 4-4
heart fit opposite 22-24**.  Thirteen tricks were available.

**The missing agreement:** the 2C tree has no shortness-showing slam try
anywhere.  Once Stayman has found the 4-4 major fit opposite a known 22-24,
a jump to four of a new suit must be a splinter — the first rule in the file
that says "I have a fit, a void, and slam interest" before game is reached.

**Context:** `r2c_after_stayman_reply` (existing).

```yaml
      # THE FIRST SLAM TRY IN THE 2C TREE.  r2c_place_4H reads FOUR HEARTS and
      # nothing else, so an 8-count with a void and a six-card side suit signs
      # off in game opposite a known 22-24.  A jump to four of a new suit here
      # is a splinter: fit, shortness, slam interest - and it is priced above
      # the sign-off precisely because the sign-off describes nothing.
      - id: r2cs_splinter_4C
        call: 4C
        priority: 63
        when: { standing_bid_strain: [H] }
        requires:
          suits: { H: [4, 13], C: [0, 1] }
          evals: { total_points: [6, 40] }
        shows: "splinter: four hearts opposite 22-24, singleton or void in clubs, slam interest"
        establishes: { forcing: game_forcing, agreed_suit: H }
        alertable: true
        convention: splinter
      - id: r2cs_splinter_4D
        call: 4D
        priority: 63
        when: { standing_bid_strain: [H] }
        requires:
          suits: { H: [4, 13], D: [0, 1] }
          evals: { total_points: [6, 40] }
        shows: "splinter: four hearts opposite 22-24, singleton or void in diamonds, slam interest"
        establishes: { forcing: game_forcing, agreed_suit: H }
        alertable: true
        convention: splinter
      - id: r2cs_splinter_S4C
        call: 4C
        priority: 63
        when: { standing_bid_strain: [S] }
        requires:
          suits: { S: [4, 13], C: [0, 1] }
          evals: { total_points: [6, 40] }
        shows: "splinter: four spades opposite 22-24, singleton or void in clubs, slam interest"
        establishes: { forcing: game_forcing, agreed_suit: S }
        alertable: true
        convention: splinter
      - id: r2cs_splinter_S4D
        call: 4D
        priority: 63
        when: { standing_bid_strain: [S] }
        requires:
          suits: { S: [4, 13], D: [0, 1] }
          evals: { total_points: [6, 40] }
        shows: "splinter: four spades opposite 22-24, singleton or void in diamonds, slam interest"
        establishes: { forcing: game_forcing, agreed_suit: S }
        alertable: true
        convention: splinter
      - id: r2cs_splinter_4H
        call: 4H
        priority: 63
        when: { standing_bid_strain: [S] }
        requires:
          suits: { S: [4, 13], H: [0, 1] }
          evals: { total_points: [6, 40] }
        shows: "splinter: four spades opposite 22-24, singleton or void in hearts, slam interest"
        establishes: { forcing: game_forcing, agreed_suit: S }
        alertable: true
        convention: splinter
```
(The context is not templated, so the five rules are written out.  A cleaner
refactor is a sibling context with `expand_pairs` over `{M, SH, call}`.)

**THE ANSWERING SEAT — shipped in the same proposal.**

```yaml
  - id: opener_over_2C_stayman_splinter
    description: "The 2C opener judges the splinter: duplication or working values"
    expand_pairs:
      - { M: H, J: 4C }
      - { M: H, J: 4D }
      - { M: S, J: 4C }
      - { M: S, J: 4D }
      - { M: S, J: 4H }
    pattern: "2C - P - 2D - P - 2NT - P - 3C - P - 3$M - P - $J - P - ?"
    rules:
      # the oldest slam maxim, and the one the file already encodes for the
      # 1M-2NT splinters (jac_wasted_signoff): K/Q/J opposite the shown
      # shortness are dead paper.
      - id: o2css_wasted_$J
        call: 4$M
        priority: 55
        requires: { evals: { wasted_in_partner_shortness: [4, 40] } }
        shows: "wasted honours opposite the shortness: signing off in game"
        establishes: { forcing: sign_off, agreed_suit: $M }
      - id: o2css_rkc_$J
        call: 4NT
        priority: 60
        requires:
          evals: { controls: [7, 12], "keycards($M)": [2, 5],
                   wasted_in_partner_shortness: [0, 3] }
        shows: "RKC 1430 for $M: no duplication opposite the splinter"
        establishes: { forcing: one_round, agreed_suit: $M, asking: keycards }
        alertable: true
        convention: rkc_1430
      # the floor: a slam try must never starve its answerer
      - id: o2css_signoff_$J
        call: 4$M
        priority: 34
        requires: {}
        shows: "signing off in the agreed game over the splinter"
        establishes: { forcing: sign_off, agreed_suit: $M }
        negative_inference_weight: soft
```
The keycard reply ladder (`rkc_response_agreed_H/S`, `rkc_continue_after_5*`,
`rkc_5C_answerer`) is already authored, so the conversation closes.

**What it endangers:**
* `r2c_place_4H` (62) / `r2c_place_4S` (61) — only on hands with a genuine
  singleton or void; those hands are exactly the ones the sign-off
  mis-describes.
* `r2c_place_3NT` (55, `requires: {}`) — never outranked, still the floor.
* `gf_new_3$X` (36) and the generic `uc_rebid_$X4` (29) lose 4C/4D at this
  seat; both were describing a natural suit, which the splinter is not, and
  neither fitted this hand (`uc_rebid_C4` fit 0.000).
* The new answering context is anchored at 13 tokens, the most specific in
  the file at that position; `o2css_signoff_$J` with `requires: {}` gives it
  the superset property for 4$M.

**VERIFIED.**  `{suits: {H: [4,13], C: [0,1]}, evals: {total_points: [6,40]}}`
scores **fit 1.000** on `K73.8642.AJT863.` at the real seat (total_points 13,
void in clubs), against `r2c_place_4H` at 1.000/62 — so priority 63 takes it.

**Template:** as written for the 2C tree; the identical idea belongs in
`stayman_resp_after_2M` and `nt2_stayman_placement` (the 1NT and 2NT Stayman
fits), which would take the count to ~15 rules from one agreement.

---

## Board 867 — margin -9

**Seat/call that went wrong:** table B, call 2, **East bids 1S** on
`AQJT872.6.9542.5` after `1C 1H`.  `nx_1m1H_1S` fits 1.000 at priority 78 —
a *forcing* one-level response on a seven-card suit and 7 HCP, which leaves
the auction cheap; North then bid 4H and we never got back in.

**The missing agreement:** `resp_1m_over_1H` has **no preemptive jump of any
kind** (its sibling `resp_1m_over_1S` has `nx_1m1S_wj_H`), so a seven-card
suit under a free bid's values has to make a forcing bid it does not want.

**Context:** `resp_1m_over_1H` (existing, `expand: { m: [C, D] }`).

```yaml
      # SIBLING GAP (the file's own recurring species): resp_1m_over_1S has a
      # weak jump shift and this context has none, so a SEVEN-card suit with
      # 7 HCP made a forcing one-level bid.  Two rungs: the weak jump for six,
      # the game preempt for seven.
      - id: nx_1m1H_wj_S
        call: 2S
        priority: 56
        requires: { suits: { S: [6, 6] }, hcp: [0, 8] }
        shows: "weak jump shift: six spades, less than a free bid"
        establishes: { forcing: non_forcing }
      - id: nx_1m1H_pre_S4
        call: 4S
        priority: 79
        requires: { suits: { S: [7, 13] }, hcp: [4, 9], features: [ "good_suit(S)" ] }
        shows: "preemptive game bid: seven good spades, less than an opening bid"
        establishes: { forcing: sign_off, agreed_suit: S }
```

**Answering seat:** none — 4S is a sign-off, and `slam_try_over_game_raise`
already owns partner's seat over our four-level major.  The 2S weak jump is
`non_forcing` and is answered by the generic competitive toolkit.

**What it endangers, in `resp_1m_over_1H`:**
* `nx_1m1H_1S` (78) — only on **seven**-card suits with 4-9 HCP, where the
  forcing one-level response is the losing action against a fitting
  opposition.
* `nx_1m1H_X` (80) is untouched (it demands exactly four spades).
* `nx_1m1H_cue` (70), `nx_1m1H_raise` (55), the notrump ladder (50/51/52) —
  all below 79, but all deny four+ spades or demand a club fit, so the
  overlap is empty in practice.
* `nx_1m1H_pass` (20) — a seven-card suit is not "nothing to say".
* The 2S rung at 56 sits **below** the 1S rung at 78 deliberately: it can only
  fire when 1S does not fit, i.e. under 6 HCP.  That is the sibling's exact
  design.

**VERIFIED.**  `{suits: {S: [7,13]}, hcp: [4,9], features: ["good_suit(S)"]}`
scores **fit 1.000** on `AQJT872.6.9542.5` at the real seat.

**Template:** `expand: { m: [C, D] }` — four rules; the heart twin in
`resp_1m_over_1S` (`nx_1m1S_pre_H4`) makes eight.

---

## Board 898 — margin -9

**Seat/call that went wrong:** table B, call 1, **West bids 2S** on
`AK97652.2.763.T3` over 1D.  `oc1D_2S_jump` ("weak jump overcall: **6**
spades, 5-10") fits **1.000** with **seven** spades and outranks
`oc1D_3S_preempt` ("preemptive overcall: seven-card s suit"), which also fits
1.000, on priority 60 vs 58.

**The missing agreement:** the length band on the jump overcall is open at the
top (`[6, 13]` in the constraint, "6" in the sentence), so the seven-card
description never wins its own hand.

**Context:** `overcalls_of_1$o` (four contexts, not templated).  Written as a
new rung rather than as a cap on the jump, because *re-ranking the weak jump
overcall* is on the do-not-re-propose list and I am deliberately not touching
its band or its position relative to the one-level overcall.

```yaml
      # LENGTH IS THE DESCRIPTION.  oc1D_2S_jump's sentence says six and its
      # constraint says 6+, so the SEVEN-card hand fitted the six-card rule at
      # 1.00 and the seven-card rule never won its own population.  This adds
      # the seven-card reading above it; the six-card jump keeps its whole band
      # and its priority relative to everything else, so nothing is subtracted.
      - id: oc1D_3S_preempt7
        call: 3S
        priority: 61
        requires:
          suits: { S: [7, 13] }
          hcp: [3, 10]
          features: [ "good_suit(S)" ]
        shows: "preemptive overcall on a SEVEN-card spade suit: 3-10"
        establishes: { forcing: sign_off }
```

**Answering seat:** `advance_weak_jump_overcall` (`1$o - 3$j - P - ?`) is
already authored and is exactly the right seat for a three-level preempt —
which is part of the case: today the 2S version lands in the generic
competitive toolkit instead.

**What it endangers, in `overcalls_of_1D`:**
* `oc1D_2S_jump` (60) — only on seven-card suits; six-card hands are
  untouched.
* `oc1D_1S` (71) is *above* this rung and keeps every hand it fits — that is
  the round-11 finding (the one-level call wins the 8-10 overlap) preserved
  intact, deliberately.
* `oc1D_4S_preempt` (59) still owns eight-card suits.
* `oc1D_pass` (25) — a seven-card suit is a preempt, not a pass.

**Explicit adjacency warning:** DECISIONS lists "re-ranking the weak jump
overcall" as measured-negative.  That measurement was *the jump against the
simple overcall on the 8-10 band*.  This rung leaves that comparison exactly
as it is and only separates six cards from seven.  If the round is not
comfortable with the distinction, drop this proposal and record board 898 as
NOTHING-WRONG — the rest of the auction is competitive.

**VERIFIED** for the ranking claim (`oc1D_2S_jump` 1.000/60 vs
`oc1D_3S_preempt` 1.000/58 on the actual hand, so priority alone decides);
**UNTESTED** as a shipped rung.

**Template:** the same rung in all four `overcalls_of_1$o` contexts for all
three non-opened suits — up to 12 rules from one idea.

---

## Board 997 — margin -9

**Seat/call that went wrong:** table A, call 9, **South passes** on
`K4.QJ654.A.AK875` after `P 1H P 1S P 2C P 2S P`.  17 HCP, 19 support points,
four losers, a doubleton spade honour opposite a shown six-card spade suit —
and the deciding rule is **`uc_pass`, fit 1.00, priority 18**, because
nothing else in the seat reaches 0.35.  We played 2S making eleven.

**The missing agreement:** opener has no context at all for his third call
after responder's two-level rebid of his own major.  Pass / invite / raise to
game does not exist; the generic toolkit's `uc_raise_S4` demands **eight**
combined trumps and responder has only *promised* five, so it fits 0.082.

**Context:** new, `opener_over_responder_2S_rebid`.

```yaml
  - id: opener_over_responder_2S_rebid
    description: "Opener's third call after 1H - 1S - 2m - 2S (responder rebids his own spades)"
    expand: { x: [C, D] }
    pattern: "1H - P - 1S - P - 2$x - P - 2S - P - ?"
    rules:
      # LOSERS, NOT TRUMPS.  Responder has PROMISED five spades (the rule that
      # made the call shows six), so every generic raise gated on eight
      # counted trumps is dead here - which is why this seat scored 0.082 for
      # its best bid and passed a 19-point hand.
      - id: otp_game_4S
        call: 4S
        priority: 40
        requires:
          suits: { S: [2, 13] }
          evals: { total_points: [18, 40], "lott_total_trumps(S)": [7, 26], ltc: [0, 5] }
        shows: "18+ support points and at most five losers opposite the rebid spades: game"
        establishes: { forcing: sign_off, agreed_suit: S }
      - id: otp_invite_3S
        call: 3S
        priority: 39
        requires:
          suits: { S: [2, 13] }
          evals: { total_points: [15, 17], "lott_total_trumps(S)": [7, 26] }
        shows: "15-17 opposite the rebid spades: inviting game"
        establishes: { forcing: invitational, agreed_suit: S }
      # SUPERSET RUNGS: this context is anchored and therefore shadows the
      # generic toolkit for 4S, 3S and P.  These three carry the shadowed
      # rules' gates verbatim so the context can only ever be a superset.
      - id: otp_raise_general_4S
        call: 4S
        priority: 32
        requires:
          suits: { S: [2, 13] }
          evals: { total_points: [11, 40], rule_of_26: [25, 99], "lott_total_trumps(S)": [8, 26] }
        shows: "raise of partner's S: 11+ support points, a real trump fit, and the values for the level"
        establishes: { forcing: non_forcing, agreed_suit: S }
      - id: otp_raise_general_3S
        call: 3S
        priority: 31
        requires:
          suits: { S: [3, 13] }
          evals: { total_points: [10, 40], rule_of_26: [22, 99], "lott_total_trumps(S)": [8, 26] }
        shows: "raise of partner's S: 3+ trumps, 10+ support points, 8+ combined trumps"
        establishes: { forcing: non_forcing, agreed_suit: S }
      - id: otp_pass
        call: P
        priority: 18
        requires: {}
        shows: "nothing further to show: passing the preference"
        establishes: { forcing: sign_off }
        negative_inference_weight: soft
```

**THE ANSWERING SEAT for `otp_invite_3S`, shipped with it:**

```yaml
  - id: responder_over_late_spade_invite
    description: "Responder answers opener's 3S invitation after 1H - 1S - 2m - 2S"
    expand: { x: [C, D] }
    pattern: "1H - P - 1S - P - 2$x - P - 2S - P - 3S - P - ?"
    rules:
      - id: rlsi_accept_4S
        call: 4S
        priority: 55
        requires:
          any_of:
            - suits: { S: [6, 13] }
              evals: { total_points: [9, 40] }
            - evals: { total_points: [11, 40] }
        shows: "accepting: a sixth spade or a maximum for the two-level rebid"
        establishes: { forcing: sign_off, agreed_suit: S }
      - id: rlsi_decline
        call: P
        priority: 50
        requires: {}
        shows: "declining: minimum for the spade rebid"
        establishes: { forcing: sign_off }
        negative_inference_weight: soft
```

**What it endangers:**
* `uc_raise_S4` (32) and `uc_raise_S3` (31) lose 4S/3S at this position; both
  are carried verbatim as `otp_raise_general_*`, so the coverage is a strict
  superset.
* `uc_pass` (18) loses P; `otp_pass` is `requires: {}` at the same priority,
  so it is behaviourally identical for every hand the new rungs do not fit.
* `uc_rebid_H3` (29) / `uc_rebid_C3` (27) / `uc_nt3` (29) are different calls
  and are **not** shadowed — opener with 6-5 or with a stopper can still bid
  3H, 3C or 3NT, and they outrank nothing new because my invitational rung
  sits at 39 above them.  That is the one judgement in this proposal: with
  four losers and a doubleton spade honour, the eight-card major fit beats
  rebidding a five-card side suit.

**VERIFIED.**  `otp_game_4S`'s `requires` scores **fit 1.000** on
`K4.QJ654.A.AK875` at the real seat (total_points 19 with spades agreed,
`lott_total_trumps(S)` 7, ltc 4); today's whole candidate set tops out at
`uc_pass` 1.000/18 with `uc_raise_S4` at 0.082.

**Template:** `expand: { x: [C, D] }` (four rules x 2 = 10 rules over the two
contexts).  1H-1S is the only auction of this shape at the one level, so no
major expansion exists; the analogous seats after `1$m - 1$M - 2$m - 2$M`
(`responder_after_minor_rebid`'s partner) want the same treatment.

---

## Board 7 — margin -8

**Seat/call that went wrong:** table A, call 3, **South doubles** on
`J97.A54.J.QT8653` after `P 1D 2H`.  `nxj_X` — "negative double of the jump
overcall: **8+ HCP, no shape shown**", priority 70, the only positive rule in
`neg_double_3level_m` — takes a hand whose only feature is six clubs.  West
jumped to 4H and North had to guess (4S).

**The missing agreement:** `neg_double_3level_m` has exactly **two** rules,
`nxj_X` and `nxj_pass`.  DECISIONS says of it: *"two of the nine replacement
calls score below the 0.9 fast path, so author the landing seats first, then
re-measure."*  This is that authoring.

**Context:** `neg_double_3level_m` (existing).  Add per-pair vars naming the
two unbid suits and the cheapest call in each.

```yaml
    expand_pairs:
      - { m: C, j: 2H, A: S, CA: 2S, B: D, CB: 3D, TAG: C2H }
      - { m: C, j: 2S, A: H, CA: 3H, B: D, CB: 3D, TAG: C2S }
      - { m: D, j: 2H, A: S, CA: 2S, B: C, CB: 3C, TAG: D2H }
      - { m: D, j: 2S, A: H, CA: 3H, B: C, CB: 3C, TAG: D2S }
      - { m: C, j: 3H, A: S, CA: 3S, B: D, CB: 4D, TAG: C3H }
      - { m: C, j: 3S, A: H, CA: 4H, B: D, CB: 4D, TAG: C3S }
      - { m: D, j: 3S, A: H, CA: 4H, B: C, CB: 4C, TAG: D3S }
```

This board's rung is the **lower** unbid suit at the three level — responder's
own six-card suit, named instead of doubled:

```yaml
      # A SIX-CARD SUIT IS SHAPE, AND nxj_X SHOWS NONE.  The generic
      # cl_new_long3_$X rung scores 0.800 here (it wants 11+ points) and sits
      # at priority 27, so the shapeless double takes every hand in the
      # context.  This is the landing seat DECISIONS asks for.
      - id: nxj_natural_lo_$TAG
        call: $CB
        priority: 71
        requires: { suits: { $B: [6, 13] }, hcp: [7, 11] }
        shows: "natural $B: a six-card suit and 7-11, non-forcing - the suit, not the double"
        establishes: { forcing: non_forcing }
```

**Answering seat:** the call is `non_forcing` and limited, so it creates no
ask.  Opener's seat over it is `general_competitive_high` /
`opener_neg_double_over_raise`, both authored, and the limited range is what
makes that safe — this is deliberately not a forcing rung.

**What it endangers, in `neg_double_3level_m`:**
* `nxj_X` (70) — only on hands with a six-card suit in the lower unbid suit
  and 7-11 HCP.  DECISIONS records that *gating* the double measured -5 and
  was reverted; this does not gate it, it gives the hand a better rule to
  fit, which is the remedy that entry actually prescribes.
* `nxj_pass` (20) — a six-card suit and 7+ is not "nothing to say".
* Below it, the generic `cl_new_long3_$X` (27) and `cl_new_$X3` (27) lose
  this call here; both were describing the same suit with a higher point
  floor and neither could ever win against priority 70.

**VERIFIED.**  `{suits: {C: [6,13]}, hcp: [7,11]}` scores **fit 1.000** on
`J97.A54.J.QT8653` at the real seat; today `nxj_X` fits 1.000 at 70 and the
best natural club rung is `cl_new_long3_C_hi` at 0.800/27.5.

**Template:** the seven `expand_pairs` above — seven rules; with board 114's
companion rung (the higher unbid suit) fourteen, and with the notrump and
raise rungs the context needs a full ladder of about 35.

---

## Board 13 — margin -8

**Seat/call that went wrong:** table A, call 7, **North passes** on
`9765.AKJ4.2.K643` after `P 1D X XX 2C P P`.  Eleven HCP, four of their
runout suit, opposite a partner who has redoubled — and the auction dies in
2C undoubled for +300 while 4S was cold at the other table.

(The dossier flags call 5, South's forcing pass, first; South's pass is
correct system — `rdc_pass_$m` is exactly what a redouble auction wants.  The
seat that fails is the **redoubler's own next turn**, and it has no context:
`redouble_continuations` is `1$m - X - XX - bid - ?`, five tokens, and North
is speaking at seven.)

**The missing agreement:** after our redouble and their runout, opener's pass
is forcing — so the redoubler must have a defined set of answers, above all
the penalty double.  He has none; `general_balancing_low` takes the seat and
passes.

**Context:** new, `redoubler_over_runout`.

```yaml
  - id: redoubler_over_runout
    description: "The redoubler answers opener's forcing pass over their runout"
    expand: { m: [C, D] }
    pattern: "1$m - X - XX - bid - P - P - ?"
    rules:
      # THE WHOLE POINT OF A REDOUBLE.  Partner's pass is forcing; with length
      # in the suit they have run to, the redoubler doubles, and that is the
      # call the auction was constructed to reach.
      - id: rdro_X_$m
        call: X
        priority: 62
        requires:
          hcp: [9, 40]
          evals: { standing_suit_length: [4, 13] }
        shows: "penalty double: four-plus of their runout suit behind the runner"
        establishes: { forcing: non_forcing }
      - id: rdro_major_$m
        call: 2H
        priority: 56
        when: { unbid_suit: H, cheapest_in_suit: true }
        requires: { suits: { H: [5, 13] }, hcp: [9, 40] }
        shows: "five-card heart suit: naming our fit rather than defending"
        establishes: { forcing: one_round }
      - id: rdro_spade_$m
        call: 2S
        priority: 55
        when: { unbid_suit: S, cheapest_in_suit: true }
        requires: { suits: { S: [5, 13] }, hcp: [9, 40] }
        shows: "five-card spade suit: naming our fit rather than defending"
        establishes: { forcing: one_round }
      # floor: this context defines P, so it must define it for every hand
      - id: rdro_pass_$m
        call: P
        priority: 20
        requires: {}
        shows: "no penalty and no suit: letting them play it undoubled"
        establishes: { forcing: non_forcing }
        negative_inference_weight: soft
```

**Answering seat:** the double is answered by `general_pull_or_sit`
(`... - X - P - ?`), the file's authored sit/pull ladder — that is the seat
that decides whether opener converts, and it exists.  `rdro_major_$m` /
`rdro_spade_$m` are `one_round` and are answered by
`general_uncontested_continuation`'s raise ladder plus `gf_landing_*`; if the
round wants that tighter, make them `non_forcing` instead.

**What it endangers:** at this exact seven-call position it takes X, 2H, 2S
and P from `general_balancing_low` (`ballow_X` 40, `ballow_new_*` 26-27,
`ballow_pass` 21).  `rdro_pass_$m` carries `requires: {}` so the pass is
preserved; `rdro_X_$m` at 62 outranks `ballow_X` at 40, which is right — a
double after our own redouble is a penalty statement, not a balance.

**UNTESTED** (new context).  What I did verify: the seat today produces
`ballow_pass` at fit 1.00 with no authored alternative, and North's holding
(`K643` in their runout suit, 11 HCP) satisfies `hcp: [9,40]` and
`standing_suit_length: [4,13]` exactly.

**Template:** `expand: { m: [C, D] }` — eight rules; extend to
`expand: { m: [C, D, H, S] }` once the major-opening redouble tree exists
(sixteen).

---

## Board 376 — margin -8

**Seat/call that went wrong:** table A, call 8, **North bids 3C** on
`AJT82.9.2.KQJ832` after `1S P 1NT P 2C P 2NT P`.  The deciding rule is
`uc_rebid_C3` out of the generic toolkit: `opener_over_pref_2NT` — the
context written specifically to answer that invitational 2NT — has **no rung
this hand can fit**, because `opn_pass` needs 12-13 HCP (North has 11, the
system's own light opening), `opn_3$M` needs six spades and North has five.

**The missing agreement:** opener's answer to the invitational 2NT has no
shape rung: a 6-5 minimum can neither pass nor accept, only correct to its
long suit, and that correction does not exist.

**Context:** `opener_over_pref_2NT` (existing).

```yaml
      # THE SHAPE ANSWER.  opn_pass / opn_3NT / opn_3$M / opn_4$M are all
      # point-count answers with a six-card-major escape; the 6-5 and 5-6
      # minimums that the light-opening rules create have no rule at all and
      # fall through to the generic toolkit.
      - id: opn_3$x
        call: 3$x
        priority: 57.5
        requires:
          suits: { $x: [6, 13] }
          hcp: [11, 14]
          not: { suits: { $M: [6, 13] } }
        shows: "6+ $x with a minimum: correcting the invitational notrump to the long minor"
        establishes: { forcing: sign_off }
      # and the floor the ceiling created: the light opener's decline
      - id: opn_pass_light
        call: P
        priority: 59.5
        requires: { hcp: [10, 11], not: { suits: { $M: [6, 13] } }, not: { suits: { $x: [6, 13] } } }
        shows: "declining the invite with a light opening"
        establishes: { forcing: sign_off }
```
(the double `not:` is not legal in one block — write the second as
`all_of: [ { not: { suits: { $M: [6, 13] } } }, { not: { suits: { $x: [6, 13] } } } ]`.)

**Answering seat:** `opn_3$x` is a sign-off; responder's seat over it is
`general_uncontested_continuation` with `we_hold_contract` false, and the
correct action (pass) is `uc_pass` at fit 1.00.  If the round wants it
authored, a `1$M - P - 1NT - P - 2$x - P - 2NT - P - 3$x - P - ?` context with
a pass floor, a 3NT and a 5$x is four more rules.

**What it endangers:** `opn_pass` (60) and `opn_3NT` (58) both deny a
six-card major only, so a 6-5 hand could previously fit `opn_3NT` on 14 HCP;
at 57.5 my rung sits **below** 3NT and only takes hands 3NT does not fit.
Below it, the generic `uc_rebid_$x3` (27) loses the call — which is the
point, it was making an authored decision by accident.

**NEGATIVE RESULT, reported rather than hidden.**  I first tried the rung the
board seems to ask for — responder's invitational jump in his own six-card
major after the forcing 1NT (`pref_3$oM` on `76.AQ7432.A973.T`).  It fires
cleanly (fit 1.000) but the double-dummy table says hearts take **six**
tricks from either side while 3C takes nine: the rung would turn +110 into
-100 on this board.  The agreement is standard and probably right in general,
but this board is evidence against it and I am not shipping it on this
board's authority.

**VERIFIED.**  `{suits: {C: [6,13]}, hcp: [11,14], not: {suits: {S: [6,13]}}}`
scores **fit 1.000** on `AJT82.9.2.KQJ832` at the real seat.  Note that the
proposal is **board-neutral here** (3C is what we already bid); it converts a
generic-toolkit accident into an authored call, which is the density point,
not an IMP claim.  The board's actual loss is table B's balancing double —
the competitive reviewer's lane.

**Template:** the four `expand_pairs` already on the context — eight rules.

---

## Board 488 — margin -8

**Seat/call that went wrong:** table B, call 7, **West bids 5C** on
`862.AK752..KQJ98` after `P P 1S 2C P 3C P`.  `uc_minor_game_5C`
(fit **0.946**, priority 28) beats `uc_new_H3` (fit **1.000**, priority 27.5)
on the fast path: the hand's own five-card heart suit — a perfect long-suit
game try — is already in the candidate set and loses to blasting eleven
tricks.

**The missing agreement:** **trial bids are at zero rules in this file.**  A
new suit after partner has raised our minor is a long-suit game try, not a
natural bid, and it must outrank five of the minor.

**Context:** new, `minor_game_try`.  Written `"... - P - ?"` — the same
device the cue contexts use — so it ties with the generic toolkit on
specificity and wins on file order, without shadowing anything anchored.

```yaml
  - id: minor_game_try
    description: "A new suit after partner raises our minor is a long-suit game try"
    expand_pairs:
      - { m: C, X: D, TAG: CD }
      - { m: C, X: H, TAG: CH }
      - { m: C, X: S, TAG: CS }
      - { m: D, X: H, TAG: DH }
      - { m: D, X: S, TAG: DS }
    pattern: "... - P - ?"
    when: { agreed_suit: $m }
    rules:
      # ELEVEN TRICKS ARE EXPENSIVE.  uc_minor_game_5$m is the only positive
      # move over partner's three-level raise, so every hand with the values
      # blasts.  A real second suit asks the two questions that decide the
      # hand: have you a stopper (bid 3NT) or a fit (raise)?
      - id: mgt_try_$TAG
        call: 3$X
        priority: 28.5
        when: { standing_bid_level: [3], standing_bid_strain: [$m],
                cheapest_in_suit: true, we_hold_contract: false, unbid_suit: $X }
        requires:
          suits: { $X: [4, 13] }
          evals: { total_points: [14, 40], "lott_total_trumps($m)": [8, 26] }
        shows: "long-suit game try: a real $X suit opposite the $m raise - 3NT with a stopper, five with a fit"
        establishes: { forcing: one_round, agreed_suit: $m }
        alertable: true
        convention: long_suit_game_try
```

**THE ANSWERING SEAT — shipped with it, and this is the whole reason the
proposal exists:**

```yaml
  - id: minor_game_try_answer
    description: "Answering the long-suit game try in our agreed minor"
    expand_pairs:
      - { m: C, X: D, TAG: CD }
      - { m: C, X: H, TAG: CH }
      - { m: C, X: S, TAG: CS }
      - { m: D, X: H, TAG: DH }
      - { m: D, X: S, TAG: DS }
    pattern: "... - P - ?"
    when: { agreed_suit: $m }
    rules:
      - id: mgta_3NT_$TAG
        call: 3NT
        priority: 44
        when: { partner_last_suit: $X, standing_bid_level: [3], we_hold_contract: false }
        requires:
          features: [ "stopper($X)" ]
          evals: { weakest_unshown_stopper: [0.9, 9] }
        shows: "a $X stopper opposite the game try: nine tricks, not eleven"
        establishes: { forcing: sign_off }
      - id: mgta_5$TAG
        call: 5$m
        priority: 43
        when: { partner_last_suit: $X, standing_bid_level: [3], we_hold_contract: false }
        requires:
          suits: { $X: [3, 13] }
          evals: { total_points: [11, 40], "lott_total_trumps($m)": [9, 26] }
        shows: "no stopper but real help in $X and a maximum raise: five of the minor"
        establishes: { forcing: sign_off, agreed_suit: $m }
      # the floor: an invitation must never starve its answerer
      - id: mgta_decline_$TAG
        call: 4$m
        priority: 34
        when: { partner_last_suit: $X, standing_bid_level: [3], we_hold_contract: false }
        requires: {}
        shows: "declining the game try: one more in the agreed minor"
        establishes: { forcing: sign_off, agreed_suit: $m }
        negative_inference_weight: soft
```

**What it endangers:**
* `uc_minor_game_5$m` (28) — exactly the intended demotion; it keeps every
  hand without a four-card side suit.
* `uc_new_$X3` / `uc_new_$X3_hi` (27 / 27.5) — the same call, now read as a
  try rather than as a natural suit; that reading is only imposed where our
  minor is *agreed*, so no natural three-level bid is lost elsewhere.
* `uc_rebid_$m4` (29) — a fourth-level rebid of the agreed suit is a weaker
  description than naming the second suit.
* `uc_pass` (18) and `uc_nt3` (29): 3NT stays available to the *answerer*,
  where it belongs.
* In the answering context, `mgta_decline` at 34 outranks `uc_pass` (18) but
  is a **bid**, so it can never end the auction below the level partner asked
  about — that is the round-6 `rkc5H_signoff` lesson applied.

**VERIFIED.**  `mgt_try_$TAG`'s `requires` scores **fit 1.000** on
`862.AK752..KQJ98` at the real seat (five hearts, total_points ≥ 14,
`lott_total_trumps(C)` 8), against `uc_minor_game_5C` at 0.946.

**Template:** the five `expand_pairs` — five try rules and fifteen answering
rules from one agreement.  The **major-suit twin is the bigger prize** and is
not in this slice's boards: the same three rungs after `1$M - P - 2$M - P - ?`
(help-suit game try) and the answering seat inside
`responder_over_game_try`, which today has exactly two rules.

---

## Board 544 — margin -8

**NOTHING-WRONG (constructive).**  The first divergence is West passing out
`2H P P` on `A.AQ96.KJ43.AJ84`; BEN doubles.

What I checked: the balancing seat over a weak two falls to
`general_balancing_low`, where `ballow_X` scores **0.015** and
`ballow_nt2_balance` **0.000** — but both misses are correct, not defects.
West is **1-4-4-4 with four cards in their own suit**; a takeout double
holding four hearts is the call the file's `max_their_suit_length` gate
exists to forbid, and 2NT needs a balanced hand this is not.  `ballow_pass`
at 1.00 is a defensible expert action; BEN's double is the aggressive one and
the double-dummy record does not settle it (E/W's best spot is 3NT or 4S,
neither of which a takeout double reliably finds opposite a passed partner).

Table A is a weak-two opening that got doubled — the competitive reviewer's
lane.  I have no constructive agreement to add here that I would defend.

---

## Board 797 — margin -8

**Seat/call that went wrong:** table B, call 8, **East bids 3NT** on
`A864.A85.K53.A72` after `1NT P 2C P 2S P 3S P`.  `uc_nt3` at fit 0.946 out
of the *generic* toolkit — because
**`1NT - 2C - 2M - 3M` has no context at all.**  Stayman found a guaranteed
4-4 spade fit, responder invited in it, and opener answered in notrump.  4S
takes ten tricks; 3NT takes six.

**The missing agreement:** the file has `stayman_invite_accept_2D/2H/2S` for
responder's **2NT** invitation and nothing for responder's **raise of the
major** — the commoner and more informative invitation of the two.

**Context:** new, `stayman_raise_accept_$M`.

```yaml
  - id: stayman_raise_accept
    description: "1NT opener over responder's invitational raise of the Stayman major"
    expand: { M: [H, S] }
    pattern: "1NT - P - 2C - P - 2$M - P - 3$M - P - ?"
    rules:
      # 2$M promised four and the raise promised four: the fit is CERTAIN, so
      # the only question is strength - and notrump is not one of the answers.
      - id: stra_accept_max_$M
        call: 4$M
        priority: 55
        requires: { hcp: [16, 17] }
        shows: "accepting the raise: maximum 1NT with a known 4-4 fit"
        establishes: { forcing: sign_off, agreed_suit: $M }
      - id: stra_accept_shape_$M
        call: 4$M
        priority: 54
        requires:
          hcp: [15, 15]
          any_of:
            - evals: { singleton_or_void: [1, 1] }
            - evals: { controls: [6, 12] }
            - suits: { $M: [5, 13] }
        shows: "accepting on shape: a good 15 - a ruffing value, six controls, or a fifth trump"
        establishes: { forcing: sign_off, agreed_suit: $M }
      # SUPERSET RUNG: this context defines 4$M, so it must keep the generic
      # raise it shadows.
      - id: stra_general_4$M
        call: 4$M
        priority: 32
        requires:
          suits: { $M: [2, 13] }
          evals: { total_points: [11, 40], rule_of_26: [25, 99], "lott_total_trumps($M)": [8, 26] }
        shows: "raise of partner's $M: the values for the level opposite the shown range"
        establishes: { forcing: non_forcing, agreed_suit: $M }
      - id: stra_decline_$M
        call: P
        priority: 50
        requires: {}
        shows: "declining the raise: a flat minimum 1NT"
        establishes: { forcing: sign_off }
        negative_inference_weight: soft
```

**Answering seat:** none — both branches are sign-offs, and partner's seat
over our four-level major is `slam_try_over_game_raise`, already authored.

**What it endangers:** at this exact nine-call position the context takes 4$M
and P from `general_uncontested_continuation` (`uc_raise_$M4` 32, `uc_pass`
18).  `stra_general_4$M` carries `uc_raise_$M4`'s gate verbatim and
`stra_decline_$M` is `requires: {}`, so the context is a strict superset.
`uc_nt3` (29) keeps 3NT and can still win when nothing here fits ≥ 0.9 — but
`stra_decline_$M` at priority 50 with fit 1.00 always outranks it, which is
the fix: **opposite a known 4-4 major fit, notrump is never the answer.**

**VERIFIED.**  `stra_accept_shape_$M`'s `requires` scores **fit 1.000** on
`A864.A85.K53.A72` (15 HCP, 7 controls) at the real seat; today `uc_nt3` wins
at 0.946/29 over `uc_raise_S4` at 0.605.

**Template:** `expand: { M: [H, S] }` — eight rules; the identical context is
owed after `2NT - 3C - 3$M - 4$M` (the 2NT Stayman twin) and after
`1NT - 2$T - 2$M - 3$M` (raise of a completed transfer), which takes it to
about 24 rules from one agreement.

---

## Board 897 — margin -8

**NOTHING-WRONG (constructive), with a negative prototype reported.**

The first divergence is North raising to 3H on `QJT.KJ94.865.T83`
(four trumps opposite a weak two, ten combined) over their strong 2NT.
`cl_raise_lott3_H` fits 1.000 and that is the file's own stated agreement —
raise to the level of the fit — applied correctly.  BEN's pass is a
judgement call about their strong enquiry, not a systemic disagreement.

**Prototype I tried and am not shipping.**  The obvious "improvement" is the
four-level barrage: with ten combined trumps the Law says 4H, and
`cl_raise_lott4_H` fits **0.000** here only because its `their_fit: [8, 26]`
gate demands a fit the opponents have not yet shown.  I priced a sibling
without that gate.  Double-dummy: North/South take **seven** hearts, so 4H is
three off — against 4S making ten at the other table, the barrage turns
-420 into roughly -500.  **Negative; do not ship.**  The Law raise over a
*strong* enquiry needs the opponents' values in the gate, and
`their_shown_hcp` is the evaluator for it if anyone returns to this.

What else I checked: `cl_raise_H3`'s 10-point gate (correctly missed),
`cl_new_long3_*` (all 0.000 — North has no suit).  No constructive rung is
missing in this seat.

---

## Board 15 — margin -7

**Seat/call that went wrong:** table B, call 2, **East bids 1H** on
`KQT52.KQT75.Q42.` over 1C.  `oc1C_1H` and `oc1C_1S` **both fit 1.000 at
priority 71**; the tie is broken by call order, so the engine overcalls the
*lower* of two five-card suits.  East later had to bid 2S in the balancing
seat to find the fit at all.

**The missing agreement:** the opening rules encode "5-5 opens the higher"
(`suit_diff`); the overcall rules never got the twin, so with two five-card
suits the overcall is chosen by the bidding ladder rather than by agreement.

**Context:** `overcalls_of_1C` and `overcalls_of_1D` (the only two where a
1H/1S tie is possible at the same level).

```yaml
      # SIBLING GAP: open_1S already encodes "higher of equal length" through
      # suit_diff, and the overcall family never got it - so oc1$o_1H and
      # oc1$o_1S tied at 1.00/71 and the cheaper call won by accident.  A
      # duplicate rung with the shape clause, half a point above.
      - id: oc1C_1S_hi
        call: 1S
        priority: 71.5
        requires:
          suits: { S: [5, 13] }
          hcp: [8, 16]
          evals: { "suit_diff(S,H)": [0, 13], "suit_quality(S)": [1, 9] }
        shows: "overcall: 5+ spades, 8-16, spades at least as long as hearts (higher of equal length)"
        establishes: { forcing: non_forcing }
```
(copy the exact `requires` of the context's own `oc1$o_1S` and add only the
`suit_diff` clause, so the rung is that rule plus one shape statement.)

**Answering seat:** none created — a simple overcall, answered by
`advance_overcall` and the advance families, all authored.

**What it endangers:** `oc1C_1H` (71) on 5-5 and 5-4 hands only, which is the
whole content of the agreement; `oc1C_1S` (71) is its own superset and keeps
every hand.  Nothing below it is reachable (`oc1C_pass` 25, the jumps at 60,
the preempts at 58) because they all require shape or strength this rule
denies.

**VERIFIED.**  The proposed `requires` scores **fit 1.000** on
`KQT52.KQT75.Q42.` at the real seat, and the tie it breaks is confirmed:
`oc1C_1H` 1.000/71 and `oc1C_1S` 1.000/71 today.

**Template:** two contexts x one rung = two rules.  The same idea for the
2-level overcalls (`oc1$o_2$X` pairs) adds four more.

---

## Board 20 — margin -7

**NOTHING-WRONG (constructive).**  The divergence is South's 2H over their
1NT on `K85.QJT842.KQT.2` where BEN bids 2C.  That is the defence-to-1NT
family, which `DECISIONS.md` fixes as **natural** by an explicit design
choice ("chosen over DONT/Cappelletti for explainability; it is one YAML
block to swap"), and BEN's 2C is a conventional two-suited call our system
does not play.

What I checked: `v1NT_2H` fits 1.000 on its own terms (six hearts, 8-15);
`v1NT_pass` 1.000; `v1NT_X` 0.028.  There is no constructive rung missing —
the two systems simply differ, and the fix would be a convention swap, not an
agreement.

---

## Board 60 — margin -7

**Seat/call that went wrong:** table A, call 8, **North bids 4C** on
`Q.K7.AK5.AKQT543` after `2C P 2D P 3C P 3S P`.  `uc_rebid_C4` (fit 1.000,
priority 29) out of the generic toolkit; South then had to bid 5C and we went
two down while 3NT was ten tricks.

**The missing agreement:** the game-force landing family's 3NT rung
(`gf_3NT`) is written for a *weak* game-force hand — `hcp: [0, 17]` and
`not: { longest_suit_length: [6, 13] }` — so the one hand that most obviously
belongs in 3NT, a 21-count with a running seven-card minor and every side
suit stopped, is **explicitly excluded** (it scores 0.003).  The 2C tree has
no landing ladder, and this is the missing rung.

**Context:** `gf_landing_nt` (existing; `pattern: "... - P - ?"`, so it
shadows nothing anchored).

```yaml
      # gf_3NT is the WEAK game-force hand's 3NT: capped at 17 and forbidden a
      # six-card suit, because at priority 34 it was beating fit-1.0 natural
      # rebids.  The strong hand's 3NT was never written, so a 21-count with a
      # running seven-card minor rebid it at the four level and we played 5C.
      # A source of tricks plus stoppers IS nine tricks; that is the gate.
      - id: gf_3NT_source
        call: 3NT
        priority: 36
        requires:
          hcp: [16, 40]
          evals: { longest_suit_length: [6, 13], quick_tricks: [4, 13],
                   weakest_unshown_stopper: [0.9, 9] }
        shows: "a long running suit, four-plus quick tricks and every unshown suit stopped: nine tricks"
        establishes: { forcing: non_forcing }
```

**Answering seat:** `quant_raise_of_3NT` (`... - 3NT - P - ?`) is authored and
owns partner's seat over a natural 3NT, including the quantitative raise; so
does `quant_3NT_accept`.  The conversation closes.

**What it endangers:**
* `gf_3NT` (34) — same call, and the two bands barely meet: `gf_3NT` denies a
  six-card suit outright, so the overlap is empty for every hand this rule
  describes.
* `uc_rebid_$X4` (29) and `uc_new_$X3/_hi` (27 / 27.5) — nine tricks beat
  eleven, and the file already states that maxim in `gf_minor_3NT`; this
  extends it to the no-agreed-suit case.
* `gf_maj4$M` (38) and `gf_pref_3$M` (37) sit **above** it, so a known
  eight-card major fit still beats notrump — the exact correction
  `gf_landing_minor`'s comment records having to make once already.
* `gf_new_3$X` (36) ties; give the new rung 36.5 if the implementer wants the
  natural five-card suit to stay primary on hands that fit both.

**VERIFIED.**  `{hcp: [16,40], evals: {longest_suit_length: [6,13],
quick_tricks: [4,13], weakest_unshown_stopper: [0.9,9]}}` scores **fit 1.000**
on `Q.K7.AK5.AKQT543` at the real seat (21 HCP, 7-card suit, 4.5 quick
tricks, every unshown suit stopped); today the whole seat is `uc_rebid_C4`
1.000/29 with `gf_3NT` at 0.003.

**Template:** one rule, no expansion — `gf_landing_nt` is not templated.  The
matching rung for the *agreed-minor* case already exists (`gf_minor_3NT`);
what is still owed is the same idea inside `r2c_opener_rebid`'s
continuations, which is the 2C tree's documented open item.

---

## Board 85 — margin -7

**NOTHING-WRONG (constructive).**  The divergence is East passing in first
seat on `A7542.K.73.KT972` (10 HCP, 5-5 blacks) where BEN opens 1S.
`open_1S_rule20` scores **0.757** — a soft-miss just under the 0.9 fast path,
so `open_pass` at 1.00 takes it.

This is an opening-style threshold and the brief's do-not-re-propose list
names "opening-style / rule-of-20 thresholds" explicitly.  What I checked
beyond that: the rest of table B is BEN's auction entirely (we pass
throughout), and table A is a 1NT overcall and a competitive raise, neither
of which is a constructive-machinery question.

The one thing worth recording for whoever owns the scoring model: this is a
textbook instance of **the soft-miss lottery deciding an opening bid** —
0.757 is not a near-miss on a judgement, it is the difference between opening
and passing a 5-5 ten-count, and it is settled by a Gaussian rather than by an
agreement.  That is a scoring-model finding, not a rule finding.

---

## Board 100 — margin -7

**Seat/call that went wrong:** table A, call 6, **South bids 4H** on
`K862.K9752.954.K` after `1D 1S X P 2H P`.  `uc_raise_H4` (fit 1.000,
priority 32) and `uc_raise_H3` (fit 1.000, priority 31) both fit; **priority
alone decides between an invitation and a game bid** on a nine-count opposite
a partner who has just made the cheapest possible reply to a negative double.

**The missing agreement:** after my own negative double, opener's cheapest bid
of the major I promised is a **minimum** — and there is no rule anywhere that
says so, so the raise ladder treats it like a free bid.

**Context:** `general_uncontested_continuation` (existing).

```yaml
      # I DOUBLED; PARTNER WAS FORCED.  Opener's cheapest bid of the major my
      # negative double promised is a MINIMUM, and the generic raise ladder
      # reads it as a free bid: uc_raise_$M4 and uc_raise_$M3 both fit 1.00 on
      # a nine-count and priority alone chose game.  This is the invitation
      # that separates them, and it is more specific than either.
      - id: uc_advance_invite3_$M
        call: 3$M
        priority: 33.5
        when: { partner_suit: $M, partner_last_suit: $M, my_last_call_was_double: true,
                cheapest_in_suit: true, we_hold_contract: false, standing_bid_level: [2] }
        requires:
          suits: { $M: [4, 13] }
          evals: { total_points: [8, 12], "lott_total_trumps($M)": [8, 26] }
        shows: "invitational raise of the major my negative double promised: 8-12 opposite opener's minimum reply"
        establishes: { forcing: invitational, agreed_suit: $M }
```

**THE ANSWERING SEAT — shipped with it:**

```yaml
  - id: opener_over_negative_double_invite
    description: "Opener answers the invitational raise of the major his minimum reply named"
    expand_pairs:
      - { m: C, y: H, oM: S }
      - { m: D, y: H, oM: S }
      - { m: C, y: S, oM: H }
      - { m: D, y: S, oM: H }
    pattern: "1$m - 1$y - X - P - 2$oM - P - 3$oM - P - ?"
    rules:
      - id: ondi_accept_$m$y
        call: 4$oM
        priority: 55
        requires: { evals: { total_points: [15, 40] } }
        shows: "accepting: more than the minimum my cheapest reply promised"
        establishes: { forcing: sign_off, agreed_suit: $oM }
      - id: ondi_decline_$m$y
        call: P
        priority: 50
        requires: {}
        shows: "declining: the minimum I already showed"
        establishes: { forcing: sign_off }
        negative_inference_weight: soft
```

**What it endangers, in `general_uncontested_continuation`:**
* `uc_raise_$M4` (32) — only inside 8-12 support points, in this one auction,
  where the game bid is the over-bid the board punished.
* `uc_raise_$M3` (31) — same call, wider gate; mine is the more specific
  reading of the same hand and its `when` restricts it to the sequence.
* `uc_doubler_raise3_$M` (33) and `uc_doubler_game3_$M` (35) — both need
  17-19 or 17+ and four-card support **as the doubler raising an advance**;
  33.5 sits between them, so a 17-count still reaches its own rungs.
* `uc_pass` (18) — a nine-count with four-card support opposite a forced bid
  is not "nothing further to show".

**VERIFIED.**  `{suits: {H: [4,13]}, evals: {total_points: [8,12],
"lott_total_trumps(H)": [8,26]}}` scores **fit 1.000** on `K862.K9752.954.K`
at the real seat (total_points 11, nine combined trumps).

**Template:** `expand: { M: [H, S] }` on the generic family (two rules) and
the four `expand_pairs` on the answering context (eight rules).

---

## Board 107 — margin -7

**Seat/call that went wrong:** table A, call 5, **North passes** on
`QT42.K32.Q754.Q9` after `1C P 1D 2H P`.  Partner has overcalled 2H in the
sandwich seat; North holds three trumps and nine points.  `uc_raise_H3` scores
**0.004** — its `rule_of_26: [22, 99]` gate is computed against partner's
*midpoint* (7, because a sandwich overcall is recorded as 5-17), so the raise
is unreachable however good the fit is.  `uc_pass` at 1.00 takes it.

**The missing agreement:** the advance of partner's overcall has no raise
ladder of its own.  It borrows the constructive one, which is keyed to a
combined-points estimate; opposite an overcall the honest currency is
**counted trumps**, which the file already has (`lott_total_trumps`).

**Context:** `general_uncontested_continuation` (and the `cl_`/`ch_` twins).

```yaml
      # AN OVERCALL IS NOT AN OPENING.  uc_raise_$M3's rule_of_26 gate reads
      # partner's MIDPOINT, and an overcall's recorded range is so wide that
      # the midpoint is seven - so a three-card raise opposite a two-level
      # overcall scored 0.004 and the seat passed.  Opposite an overcall the
      # test is the counted fit plus my own values, and nothing else.
      - id: uc_advance_raise3_$M
        call: 3$M
        priority: 31.5
        when: { partner_suit: $M, partner_last_suit: $M, cheapest_in_suit: true,
                is_competitive: true, we_hold_contract: false, i_have_acted: false }
        requires:
          suits: { $M: [3, 13] }
          evals: { total_points: [8, 12], "lott_total_trumps($M)": [8, 26] }
        shows: "raise of partner's overcall: eight counted trumps and 8-12 - the Law, not a points estimate"
        establishes: { forcing: non_forcing, agreed_suit: $M }
```

**Answering seat:** `non_forcing` and limited, so none is created; the
overcaller's continuation is already covered by `general_competitive_high`
and `general_balancing_*`.

**What it endangers:**
* `uc_raise_$M3` (31) — same call, and mine is a superset of the hands it
  cannot reach because of the estimator; on hands where both fit, they say
  the same thing.
* `uc_raise_$M2` (30) — with eight counted trumps and 8+ points the two level
  understates the hand.
* `uc_new_$X2/_hi` (26 / 26.5) — a three-card raise of a shown five-card suit
  beats naming a four-card suit of my own.
* `uc_pass` (18).
* It sits **below** `uc_raise_$M4` (32) and `uc_raise_lott4_$M` (32), so the
  game raise and the Law raise keep every hand they fit.

**VERIFIED** for the diagnosis (`uc_raise_H3` 0.004, `uc_pass` 1.000/18 at the
real seat; the eval context shows `partner_min_hcp` 5 / `partner_max_hcp` 17
which is what collapses `rule_of_26`); **UNTESTED** as a shipped rung —
North's `lott_total_trumps(H)` is 8 and `total_points` 9, both inside the
proposed bands, but I did not trace the rung end-to-end.

**Template:** `expand: { M: [H, S] }` plus a minor twin at 3$m — four rules
per family, three families (`uc_`, `cl_`, `ch_`) = twelve.

---

## Board 114 — margin -7

**Seat/call that went wrong:** table A, call 6, **North passes** on
`AK4.4.AQT98.AKT3` after `P P 1D 2H X 3H`.  Twenty HCP opposite a negative
double that promised 8+, and the deciding rule is **`ch_pass`, fit 1.00,
priority 22**: `opener_neg_double_over_raise` has exactly two rungs, both
"bid the major partner's double implied with four of them", and North has
three spades.  Best fit in the whole seat: **0.349**.

**The missing agreement:** opener has no game force after his partner's
negative double.  Twenty points opposite eight is 28 combined and the hand
must be able to say so — the cue of their suit is the call, and it is the
control-showing force below game that this project keeps finding missing.

**Context:** `opener_neg_double_over_raise` (existing) and its one-level twin
`opener_neg_double_over_raise_1`.

```yaml
      # THE CEILING AGAIN.  Both rungs demand four cards in the implied major,
      # so a 20-count with three of them had NO RULE and passed 28 combined
      # points out at the three level.  The cue of their suit is the game
      # force; it says "I have the values, you choose the strain", which is
      # exactly what a hand with three-card support and no stopper wants.
      - id: onxr_cue3_$m$y
        call: 3$y
        priority: 62
        when: { cheapest_in_suit: true, their_last_bid_suit: true, we_hold_contract: false }
        requires: { evals: { total_points: [18, 40] } }
        shows: "cue of their suit: 18+ opposite the negative double, game forcing, no clear natural bid"
        establishes: { forcing: game_forcing }
        alertable: true
        convention: cue_bid
      - id: onxr_cue4_$m$y
        call: 4$y
        priority: 61
        when: { cheapest_in_suit: true, their_last_bid_suit: true, we_hold_contract: false }
        requires: { evals: { total_points: [18, 40] } }
        shows: "cue of their suit at the four level: 18+ opposite the negative double, game forcing"
        establishes: { forcing: game_forcing }
        alertable: true
        convention: cue_bid
```

**THE ANSWERING SEAT — shipped with it.**  Round 17 priced an unanswered cue
at **-9.8 IMPs a seat**, so this half is not optional:

```yaml
  - id: responder_over_opener_cue
    description: "Responder answers opener's game-forcing cue after the negative double"
    expand_pairs:
      - { m: C, y: H, oM: S }
      - { m: D, y: H, oM: S }
      - { m: C, y: S, oM: H }
      - { m: D, y: S, oM: H }
    pattern: "1$m - 2$y - X - bid - $c - P - ?"
    rules:
      - id: roc_major_$m$y
        call: 4$oM
        priority: 60
        when: { cheapest_in_suit: true }
        requires: { suits: { $oM: [4, 13] } }
        shows: "the major my double promised, at game"
        establishes: { forcing: sign_off, agreed_suit: $oM }
      - id: roc_minor_$m$y
        call: 5$m
        priority: 52
        requires: { suits: { $m: [4, 13] }, evals: { total_points: [10, 40] } }
        shows: "no major to show: partner's minor at game"
        establishes: { forcing: sign_off, agreed_suit: $m }
      - id: roc_nt_$m$y
        call: 3NT
        priority: 58
        requires: { features: [ "stopper($y)" ], evals: { weakest_unshown_stopper: [0.9, 9] } }
        shows: "their suit stopped: 3NT"
        establishes: { forcing: sign_off }
      # the floor - a game force must never starve its answerer
      - id: roc_floor_$m$y
        call: 3NT
        priority: 34
        requires: {}
        shows: "nothing better to say opposite the cue: 3NT"
        establishes: { forcing: sign_off }
        negative_inference_weight: soft
```
`$c` must be bound per pair to the cue call (`3H`/`4H`/`3S`/`4S`); write two
pattern variants per pair, or use `also_patterns` with both levels.

**What it endangers:**
* `onxr_3_$m$y` (60) and `onxr_4_$m$y` (59) — the cue at 62/61 outranks them
  only on 18+; with four-card support and 13-17 the natural raise still wins,
  and with four-card support and 18+ the cue is better because it keeps 3NT
  and the minor alive.
* `ch_pass` (22), `ch_rebid_$m4` (29), `ch_new_$X4` (28) — all lose the cue
  call at this seat; none of them fitted anything here (best 0.349).
* The answering context is anchored at seven tokens and defines 4$oM, 5$m and
  3NT; `roc_floor_$m$y` with `requires: {}` gives it the superset property for
  3NT, and 4$oM / 5$m were previously only reachable through generic rungs
  that scored 0.000 here.

**VERIFIED.**  `{evals: {total_points: [18,40]}}` scores **fit 1.000** on
`AK4.4.AQT98.AKT3` at the real seat, against a whole-seat best of 0.349.

**Template:** four `expand_pairs` x two levels x two contexts (the 2-level and
1-level twins) = 16 cue rules, plus 16 answering rules.

*(Board 7's companion rung — the natural higher unbid suit,
`nxj_natural_hi_$TAG`, `call: $CA`, `requires: { suits: { $A: [5, 13] },
hcp: [8, 13] }`, priority 71 — is the rung this board's OTHER seat needs:
South's `QJT87.K53.63.QJ6` scores **fit 1.000** against it and 1.000/70 for
the shapeless `nxj_X`.  Ship both together; they share the `expand_pairs`
table given under board 7.)*

---

## Board 217 — margin -7

**Seat/call that went wrong:** table B, call 6, **West bids 4C** on
`QJ8..J62.AQJT862` after `P P 1C 2H X 3H`.  `ch_rebid_C4` at fit **0.946**,
priority 29, beats `ch_pass` at fit 1.000, priority 22 — the fast path takes
the *lower-fitting* higher-priority call.  Eleven HCP with a void in their
suit, driving to the four level opposite a double that promised eight.

**The missing agreement:** the same context as board 114 has no way to say
"minimum".  It has two positive rungs and no floor of its own, so the generic
competitive toolkit's rebid rule owns every hand that is not a four-card
raise — including the minimums.

**Context:** `opener_neg_double_over_raise` (existing).

```yaml
      # THE MINIMUM ANSWER.  This context has two positive rungs and no floor,
      # so a minimum opener fell into the generic ch_ toolkit and rebid a
      # seven-card suit at the four level on eleven points.  Partner's
      # negative double promised eight, not thirteen; with a minimum the
      # constructive action is to let them play it.
      - id: onxr_min_pass_$m$y
        call: P
        priority: 40
        requires: { evals: { total_points: [0, 15] } }
        shows: "minimum opening opposite the negative double: no game, no four-level rebid"
        establishes: { forcing: non_forcing }
      # and the superset floor, because this context now defines P
      - id: onxr_pass_floor_$m$y
        call: P
        priority: 22
        requires: {}
        shows: "no bid describes this hand over their high-level contract"
        establishes: { forcing: non_forcing }
        negative_inference_weight: soft
```

**Answering seat:** none — a pass.  (And that is the point: this rung stops a
*conversation* from starting that the file cannot finish.)

**What it endangers:**
* `ch_rebid_$m4` (29) and `ch_new_$X4` (28) at this seat, on 0-15 total points
  — exactly the population the board shows over-bidding.
* `onxr_3_$m$y` (60) and `onxr_4_$m$y` (59) keep every hand they fit: 40 is
  well below them, so four-card support with 13+ still bids the major.
* Board 114's `onxr_cue3/4_$m$y` at 61/62 also stay above it, so an 18-count
  is not silenced.
* `ch_pass` (22) loses P here; `onxr_pass_floor_$m$y` carries the same
  priority and `requires: {}`, so the behaviour is preserved exactly for
  hands outside 0-15.

**VERIFIED.**  `{evals: {total_points: [0,15]}}` scores **fit 1.000** on
`QJ8..J62.AQJT862` at the real seat (total_points **14**), so priority 40
takes the call from `ch_rebid_C4`'s 0.946/29.

**Template:** four `expand_pairs` x two contexts (2-level and 1-level twins)
= 16 rules from one idea.

---

## Board 306 — margin -7

**NOTHING-WRONG (constructive).**  The first divergence is South passing in
first seat on `QJT32.J.J.AT9652` where BEN opens 1C — an opening-style
threshold, on the do-not-re-propose list, and `open_1S` is at 0.800 /
`open_1S_rule20` at 0.757, another soft-miss-lottery opening.

What I checked downstream: South balanced with 2C, North raised to 3C
(`cl_raise_C3`, correct), and over their 3H the last decision is
`balhigh_pass` where BEN bids 4C.  That is a Law-of-Total-Tricks competitive
judgement in the balancing seat — the competitive reviewer's lane — and I
note only that it is the **same rung shape as board 357's**: once our minor
is agreed and they bid one more, no rule lets us bid one more back.  Board
357 carries that proposal; duplicating it here would not add an agreement.

---

## Board 325 — margin -7

**Seat/call that went wrong:** table A, call 9, **South bids 4H** on
`9873.K5.AKJ53.54` after `P 1D P 1H 1S P P 2H P`.  `uc_raise_H4` fits 1.000
on a **doubleton** (its floor is `suits: { H: [2, 13] }`, so a doubleton
opposite a shown six-card suit reaches game), while `uc_raise_H3` demands
**three** trumps and therefore scores 0.349.  South then heard 4NT from
partner and we played 5H one down.

**The missing agreement:** the raise ladder lets a doubleton bid game but not
invite.  Opposite a partner who has rebid his own suit in the balancing seat,
twelve support points with two trumps is an invitation, and the invitation
does not exist.

**Context:** `general_uncontested_continuation` (existing).

```yaml
      # THE MISSING MIDDLE.  uc_raise_$M4's floor is a DOUBLETON (deliberately -
      # so a doubleton opposite a shown six-card suit reaches game) while
      # uc_raise_$M3 demands three trumps.  The consequence is that a hand with
      # exactly two trumps can bid GAME but cannot INVITE, and on this board it
      # did.  This is the invitation, and it is the more specific description.
      - id: uc_raise_doubleton3_$M
        call: 3$M
        priority: 32.5
        when: { partner_suit: $M, partner_last_suit: $M, cheapest_in_suit: true,
                we_hold_contract: false }
        requires:
          suits: { $M: [2, 2] }
          evals: { total_points: [10, 13], "lott_total_trumps($M)": [8, 26] }
        shows: "invitational raise on a doubleton: partner has rebid the suit, I have 10-13 and two trumps"
        establishes: { forcing: invitational, agreed_suit: $M }
```

**THE ANSWERING SEAT — shipped with it.**  Partner has to be able to accept or
decline; without that seat the invitation is a round-17 empty cue.

```yaml
  - id: answer_doubleton_raise_invite
    description: "Partner answers the three-level invitational raise of his own suit"
    expand: { M: [H, S] }
    pattern: "... - 3$M - P - ?"
    when: { partner_last_suit: $M }
    rules:
      - id: adri_accept_$M
        call: 4$M
        priority: 40
        when: { my_suit: $M, we_hold_contract: false }
        requires:
          suits: { $M: [6, 13] }
          evals: { total_points: [13, 40] }
        shows: "accepting: a sixth trump and more than the minimum I have shown"
        establishes: { forcing: sign_off, agreed_suit: $M }
      # SUPERSET RUNGS.  "... - 3$M - P - ?" is four tokens against the
      # generic toolkit's three, so this context is MORE specific and takes
      # 4$M and P away from it.  Both generics are therefore carried verbatim.
      - id: adri_general_4$M
        call: 4$M
        priority: 32
        requires:
          suits: { $M: [2, 13] }
          evals: { total_points: [11, 40], rule_of_26: [25, 99], "lott_total_trumps($M)": [8, 26] }
        shows: "raise of partner's $M: the values for the level opposite the shown range"
        establishes: { forcing: non_forcing, agreed_suit: $M }
      - id: adri_decline_$M
        call: P
        priority: 18
        requires: {}
        shows: "declining: the minimum I have already shown"
        establishes: { forcing: sign_off }
        negative_inference_weight: soft
```

**What it endangers, in `general_uncontested_continuation`:**
* `uc_raise_$M4` (32) — only on **exactly two** trumps with 10-13 support
  points; three-card support and everything from 14 up still bids game.
* `uc_raise_lott4_$M` (32) — needs four trumps, disjoint by construction.
* `uc_raise_$M3` (31) — the same call with three-plus trumps; the two bands
  are disjoint on length.
* `uc_nt2` (28) / `uc_nt3` (29) / `uc_rebid_$X3` (27) — all lose to 32.5 on
  hands where mine fits; with two trumps, 10-13 and a shown six-card suit,
  the fit is the description and notrump is not.
* In the answering context, `adri_general_4$M` and `adri_decline_$M` restore
  the shadowed generics exactly.

**VERIFIED.**  `{suits: {H: [2,2]}, evals: {total_points: [10,13],
"lott_total_trumps(H)": [8,26]}}` scores **fit 1.000** on
`9873.K5.AKJ53.54` at the real seat (total_points 12, eight counted trumps),
against `uc_raise_H4` 1.000/32 and `uc_raise_H3` 0.349.

**Template:** `expand: { M: [H, S] }` on both (two + six rules), and the minor
twin at 3$m for four more.

---

## Board 353 — margin -7

**Seat/call that went wrong:** table A, call 7, **North bids 2C** on
`AK6.9.K432.K8764` after `P P P 1C P 1S P`.  `ob_rebid_2C` at fit 1.000,
priority 50.  North holds **exactly three spades and a singleton heart** — a
sixteen-support-point hand with a ruffing value — and the only raise rungs in
`opener_rebid_1m_1M` demand **four**-card support, so `ob_raise_2S` scores
0.279 and `ob_raise_3S` 0.349.  We played 2NT for 180; 4S makes eleven.

**The missing agreement:** opener's **three-card raise of responder's major
with a side singleton or void** — the standard unbalanced-hand raise, absent
from the file.  Without it every 3-1-4-5 and 3-1-5-4 minimum has to rebid a
five-card minor and the major fit is never found.

**Context:** `opener_rebid_1m_1M` (existing, `expand: { m: [C, D], M: [H, S] }`).

```yaml
      # THE THREE-CARD RAISE.  ob_raise_2$M / 3$M / 4$M all demand FOUR-card
      # support, so a 3-1-4-5 minimum with a ruffing value had to rebid a
      # five-card minor and responder's five-card major was never raised.
      # Shortness is what makes three cards enough, so shortness is the gate.
      - id: ob_raise3_2$M
        call: 2$M
        priority: 51
        requires:
          suits: { $M: [3, 3] }
          evals: { total_points: [12, 15], singleton_or_void: [1, 1] }
        shows: "three-card raise with a ruffing value: 12-15 support points, a side singleton or void"
        establishes: { forcing: non_forcing, agreed_suit: $M }
      - id: ob_raise3_3$M
        call: 3$M
        priority: 51.5
        requires:
          suits: { $M: [3, 3] }
          evals: { total_points: [16, 18], singleton_or_void: [1, 1] }
        shows: "three-card jump raise with a ruffing value: 16-18 support points, invitational"
        establishes: { forcing: invitational, agreed_suit: $M }
```

**Answering seat:** both are already authored.  The 2$M raise is answered by
`responder_rebid_after_raise` (`rr_raise_pass` / `rr_raise_inv` /
`rr_raise_game`); the 3$M jump raise by `responder_after_jump_raise`
(`rjr_game` / `rjr_pass`), whose `expand_pairs` already covers all five
(m, M) combinations.  Responder's `JT972.AT7.AQ6.95` is 11 total points and
takes `rjr_game` — 4S.

**What it endangers, in `opener_rebid_1m_1M`:**
* `ob_rebid_2$m` (50) — three-card support plus a ruffing value is a better
  description than a five-card minor; that is the whole agreement.
* `ob_rebid_3$m` (49) — same, one level higher.
* It sits **below** `ob_1NT` (57.5), `ob_2NT` (56) and both reverses (57/58):
  `ob_1NT` and `ob_2NT` are gated `semi_balanced`/`balanced`, which a
  singleton hand can never satisfy (both are registered sharp at s2 = 0.08),
  so the overlap is empty; a genuine reverse with 17+ still wins, which is
  correct.
* It cannot reach `ob_raise_2$M` / `3$M` / `4$M` (80/78/76) — the four-card
  raises keep every hand they fit.

**VERIFIED.**  `{suits: {S: [3,3]}, evals: {total_points: [16,18],
singleton_or_void: [1,1]}}` scores **fit 1.000** on `AK6.9.K432.K8764` at the
real seat (total_points **16** with spades agreed, singleton heart), against
`ob_rebid_2C` 1.000/50.

**Template:** `expand: { m: [C, D], M: [H, S] }` already on the context —
**eight rules** from one idea.  The same agreement is owed in
`opener_rebid_1H_1S` (the 1H-1S auction) for two more.

---

## Board 357 — margin -7

**Seat/call that went wrong:** table A, call 11, **North passes** on
`JT82.T6.AQJ3.A93` after `P 1C 1H X P 2C 2H 3C P P 3H`.  Clubs are **already
agreed** (North raised to 3C two rounds ago), the eval context confirms
`agreed_suit: C` with eight counted trumps and thirteen support points — and
`ch_raise_C4` scores **0.000** because it insists the minor be my longest
suit and that we hold **ten** trumps.  `ch_pass` at 1.00 takes it.

**The missing agreement:** once a suit is agreed by both partners, a further
competitive raise is about the agreement, not about re-qualifying the fit.
The file has no "bid one more in our agreed minor" rung anywhere.

**Context:** `general_competitive_high` (and the `cl_` / `balhigh_` twins).

```yaml
      # THE AGREEMENT IS ALREADY MADE.  ch_raise_$m4 re-tests the fit from
      # scratch - ten counted trumps AND the minor must be my longest suit -
      # so once partner and I have BOTH bid the minor there is no rung that
      # lets us bid one more when they compete.  This is that rung, and its
      # `when` restricts it to the position where the agreement exists.
      - id: ch_compete_agreed_4$m
        call: 4$m
        priority: 30
        when: { agreed_suit: $m, partner_suit: $m, cheapest_in_suit: true,
                we_hold_contract: false, standing_bid_level: [3] }
        requires:
          suits: { $m: [3, 13] }
          evals: { total_points: [10, 40], "lott_total_trumps($m)": [7, 26] }
        shows: "our minor is agreed and they have bid one more: competing to the level of the fit"
        establishes: { forcing: non_forcing, agreed_suit: $m }
```

**Answering seat:** `non_forcing` and limited; partner's seat is
`general_competitive_high` / `general_balancing_high`, both authored, and the
call cannot be read as a slam try because `agreed_suit` was already set.

**What it endangers, in `general_competitive_high`:**
* `ch_pass` (22) — with eight agreed trumps and thirteen points, passing
  their three-level contract is the losing action.
* `ch_new_$X4` / `_hi` (28 / 28.5) — naming a *new* suit at the four level on
  a hand that has already agreed one is a worse description.
* `ch_nt3` (29) — it fits 0.668 here, below the fast path, and 3NT opposite a
  minimum minor raise with no stopper in their suit is a guess; my rung is at
  30 and only takes hands where it fits ≥ 0.9.
* `ch_raise_$m4` (27) — a strict subset (ten trumps, longest suit); it keeps
  every hand it fits.
* `ch_penalty_X` (38) stays above it, so a genuine trump stack still doubles.

**VERIFIED.**  `{suits: {C: [3,13]}, evals: {total_points: [10,40],
"lott_total_trumps(C)": [7,26]}}` scores **fit 1.000** on `JT82.T6.AQJ3.A93`
at the real seat (total_points 13, eight counted clubs, `agreed_suit: C`),
against a whole-seat best of `ch_pass` 1.000/22 and `ch_nt3` 0.668.

**Template:** `expand: { m: [C, D] }` across `cl_`, `ch_` and `balhigh_` = six
rules.  The major twin is unnecessary (4$M is game and
`uc_raise_lott4_$M`/`ch_raise_lott4_$M` already own it).

---

## Board 388 — margin -7

**Seat/call that went wrong:** table A, call 4, **North bids 3S** on
`AJT82.2.Q93.Q985` after `P 1H 2C 3H`.  `ch_free_3S` at fit 1.000, priority
30 — a free bid in a five-card suit, when North holds **four-card support for
partner's overcalled clubs** and they have shown a nine-card heart fit.
South then had to guess and bid 5C doubled for -200.

**The missing agreement:** `ch_raise_lott_$M4` exists ("raise to the LOTT
level: 5+ trumps, ten combined, non-vul") and **has no minor twin**, so the
Law raise of partner's minor overcall does not exist.  `ch_raise_C4` demands
11+ support points and ten combined trumps and scores 0.066.

**Context:** `general_competitive_high` (existing).

```yaml
      # SIBLING GAP: the Law raise exists for majors (ch_raise_lott_$M4) and
      # has no minor twin, so a nine-card club fit opposite an overcall,
      # against a shown nine-card heart fit, had to bid a five-card spade suit
      # instead.  Shape, not points - the same gate as the major version, one
      # trump lower because a minor fit is worth less on defence.
      - id: ch_raise_lott_4$m
        call: 4$m
        priority: 30.5
        when: { partner_suit: $m, is_competitive: true, we_hold_contract: false }
        requires:
          suits: { $m: [4, 13] }
          evals: { "lott_total_trumps($m)": [9, 26], total_points: [6, 40], their_fit: [8, 26] }
        shows: "the Law in a minor: they have a fit and so have we, nine-plus trumps our way"
        establishes: { forcing: non_forcing, agreed_suit: $m }
```

**Answering seat:** `non_forcing`; partner's seat over it is
`general_competitive_high` and `slam_try_over_game_raise` does not apply
(4$m is not game), so the code fallback pass finishes the auction — which is
correct for a shape bid.

**What it endangers, in `general_competitive_high`:**
* `ch_free_3S` (30) — the whole point: with four-card support and a
  nine-card fit shown against us, the fit is the bid.
* `ch_new_$X3` / `_hi` (27 / 27.5), `ch_new_long3_$X` (27) — same reasoning.
* `ch_pass` (22).
* `ch_raise_$m4` (27) — a strict subset (11+ points, ten trumps, my longest
  suit); it keeps every hand it fits.
* `ch_negative_X3` (33) and `ch_penalty_X` (38) stay **above** it, so a
  genuine takeout or trump stack still doubles — deliberate: my rung is a
  shape statement, not a values statement, and it must not pre-empt a double.

**VERIFIED.**  `{suits: {C: [4,13]}, evals: {"lott_total_trumps(C)": [9,26],
total_points: [6,40], their_fit: [8,26]}}` scores **fit 1.000** on
`AJT82.2.Q93.Q985` at the real seat (four clubs + partner's shown five = nine,
their shown fit nine), against `ch_free_3S` 1.000/30 and `ch_raise_C4` 0.066.

**Template:** `expand: { m: [C, D] }` in `cl_`, `ch_` and `balhigh_` = six
rules.

---

## Board 432 — margin -7

**Seat/call that went wrong:** table B, call 3, **West doubles** on
`KQT42.Q.AQ942.Q5` after `P 1H 3C`.  `nx3_negx` — "negative double through
3S: **4+** cards in the other major" — fits 1.000 at priority 70 with
**five** spades and fifteen points.  Partner pulled to 3H, West then had to
bid 3S anyway at fit 0.43, and the auction ended a level too high with the
wrong declarer.

**The missing agreement:** `neg_double_3level_M` has no natural rung in the
other major at all.  The double is defined as 4+, so the five-card hand — the
one that should simply bid the suit — has nowhere else to go.

**Context:** `neg_double_3level_M` (existing, five `expand_pairs`).

```yaml
      # FOUR IS A DOUBLE, FIVE IS A BID.  nx3_negx reads "4+ cards in the
      # other major", so the five-card hand fits it perfectly and the suit is
      # never named.  This is the natural rung; the double keeps its whole
      # band underneath and loses only the hands it over-describes.
      - id: nx3_natural_$oM
        call: 3$oM
        priority: 71
        when: { cheapest_in_suit: true }
        requires:
          suits: { $oM: [5, 13] }
          hcp: [8, 40]
          not: { suits: { $M: [3, 13] } }
        shows: "natural: five-plus cards in the other major, 8+, forcing one round"
        establishes: { forcing: one_round }
```

**THE ANSWERING SEAT — shipped with it:**

```yaml
  - id: opener_over_nx3_natural
    description: "Opener answers responder's free bid of the other major over their preempt"
    expand_pairs:
      - { M: H, x: C, oM: S }
      - { M: H, x: D, oM: S }
      - { M: S, x: C, oM: H }
      - { M: S, x: D, oM: H }
      - { M: S, x: H, oM: H }
    pattern: "1$M - 3$x - 3$oM - P - ?"
    rules:
      - id: on3n_raise_$M$x
        call: 4$oM
        priority: 60
        requires: { suits: { $oM: [3, 13] }, evals: { total_points: [13, 40] } }
        shows: "three-card support and the values: game in partner's major"
        establishes: { forcing: sign_off, agreed_suit: $oM }
      - id: on3n_rebid_$M$x
        call: 4$M
        priority: 55
        requires: { suits: { $M: [6, 13] }, evals: { total_points: [13, 40] } }
        shows: "no support: my own six-card major at game"
        establishes: { forcing: sign_off, agreed_suit: $M }
      - id: on3n_nt_$M$x
        call: 3NT
        priority: 56
        requires: { features: [ "stopper($x)" ], evals: { total_points: [13, 40] } }
        shows: "their suit stopped: 3NT"
        establishes: { forcing: sign_off }
      # floor: a one-round force must never starve its answerer
      - id: on3n_floor_$M$x
        call: 3NT
        priority: 34
        requires: {}
        shows: "nothing better opposite the free bid: 3NT"
        establishes: { forcing: sign_off }
        negative_inference_weight: soft
```
The last `expand_pairs` entry (`M: S, x: H`) makes `$oM` = H, which collides
with `$x`; drop that pair from the answering context — over `1S - 3H` the
"other major" is hearts and the natural rung does not apply.

**What it endangers, in `neg_double_3level_M`:**
* `nx3_negx` (70) — only with **five** of the other major; four-card hands
  are untouched.
* `nx3_cue` (71) ties: give the natural rung 70.5 if the round wants the
  16+ slam-try cue to keep priority on hands that fit both (it demands
  four-card support for opener's major, so the overlap is small).
* `nx3_game_raise` (69), `nx3_raise` (68), `nx3_3NT` (60), `nx3_pass` (20) —
  all describe support for opener or a stopper; a five-card major of my own
  outranks each.

**VERIFIED.**  `{suits: {S: [5,13]}, hcp: [8,40]}` scores **fit 1.000** on
`KQT42.Q.AQ942.Q5` at the real seat, against `nx3_negx` 1.000/70.

**Template:** five `expand_pairs` on the natural rung, four on the answering
context = 21 rules from one agreement.

---

## Board 455 — margin -7

**Seat/call that went wrong:** table B, call 6, **East bids 2D** on
`KT.J.AJT983.J975` after `P P 1D 1S X P`.  The deciding rule is
`onx_rebid_DS` at fit **0.409** — every rung in `opener_over_negative_double`
is gated `hcp: [12, ...]` and East opened a **third-seat rule-of-20 light**
hand with ten.  The whole seat is a soft-miss lottery.

**The missing agreement:** the system opens 10- and 11-counts by the rule of
20 and by the third-seat light rules, and opener's rebid ladders after a
negative double do not cover the hands opener is allowed to hold.
(`opener_rebid_1C_1H_extras` records this exact repair — *"Floor 10, not 12:
the system opens 10- and 11-counts by the rule of 20, and opener's rebids
have to cover the hands opener actually opens"* — and the negative-double
family never got it.)

**Context:** `opener_over_negative_double` (existing, four `expand_pairs`).

```yaml
      # THE LIGHT OPENER'S REBID.  Every rung here starts at 12 HCP, but the
      # system opens ten- and eleven-counts by the rule of 20 and in third
      # seat, so a light opener facing a negative double had NO rule and the
      # seat became a soft-miss lottery (best fit 0.409).  Same idea, and the
      # same wording, as opener_rebid_1C_1H_extras' "floor 10, not 12".
      - id: onx_rebid_light_$m$M
        call: "2$m"
        priority: 56.5
        requires: { suits: { $m: [6, 13] }, hcp: [10, 11] }
        shows: "six-card $m, light opening: the minimum rebid the rule-of-20 openings need"
        establishes: { forcing: non_forcing }
      - id: onx_major_light_$m$M
        call: "1$oM"
        priority: 60.5
        when: { cheapest_in_suit: true }
        requires: { suits: { $oM: [4, 13] }, hcp: [10, 11] }
        shows: "bidding the major the double implied, light opening"
        establishes: { forcing: non_forcing }
```

**Answering seat:** already authored — responder's seat over opener's answer
to a negative double is `general_uncontested_continuation` /
`general_competitive_low`, and both rungs are `non_forcing` and limited, so
they create no ask.

**What it endangers, in `opener_over_negative_double`:**
* Nothing above: `onx_major_$m$M` (60) and `onx_major1_$m$M` (61) keep their
  12-16 band; my light rungs sit at 60.5/56.5 with a **disjoint** 10-11 band,
  so on no hand do both fit.
* Below: `onx_nt_$m$M` (58) and `onx_rebid_$m$M` (57) — also disjoint bands.
* Against the file: the generic `uc_new_$X2` / `cl_new_$X2` (26 / 26.5) lose
  these calls at this seat; they were scoring 0.115 and 0.015 respectively,
  i.e. they never described the hand either.

**VERIFIED.**  `{suits: {D: [6,13]}, hcp: [10,11]}` scores **fit 1.000** on
`KT.J.AJT983.J975` at the real seat, against `onx_rebid_DS` 0.409 and a
whole-seat best of 0.409.

**Template:** four `expand_pairs` x two rungs = eight rules; the same floor
repair is owed to `opener_neg_double_over_raise` and
`opener_neg_double_over_raise_1` (whose `total_points: [13, 40]` gates have
the same problem) for eight more.

---

## Board 503 — margin -7

**Seat/call that went wrong:** table A, call 7, **South bids 3D** on
`KQT873..JT6.T852` after `1C 1H P 1S P 2D P`.  `uc_raise_D3` (fit 1.000,
priority 27) raises partner's second suit with three small; South's own
**six-card spade suit** has no rule — `uc_rebid_S2` fits **0.134** because it
demands 11+ total points and South has seven.

**The missing agreement:** the generic rebid ladder has an 11-point floor, so
a weak hand with a six-card suit cannot repeat it and instead raises
something.  A six-card suit is a description; three small in partner's second
suit is not.

**Context:** `general_uncontested_continuation` (and its `cl_`, `ch_`,
`ballow_`, `balhigh_` twins).

```yaml
      # THE FLOOR OF THE REBID LADDER.  uc_rebid_$X2 starts at 11 total
      # points, so a six-card suit with a weak hand had nothing and raised
      # partner's second suit on three small.  Repeating a six-card suit at
      # the TWO level costs nothing and names the trump suit.
      - id: uc_rebid_weak_$X2
        call: 2$X
        priority: 30.5
        when: { my_suit: $X, cheapest_in_suit: true, we_hold_contract: false }
        requires:
          suits: { $X: [6, 13] }
          evals: { total_points: [6, 10], "suit_quality($X)": [1, 9] }
        shows: "six-card $X repeated at the two level: weak, but this is where we play"
        establishes: { forcing: non_forcing }
```
with `expand: { X: [C, D, H, S] }` on the enclosing family (write the four
ids out if the context is not templated).

**Answering seat:** `non_forcing` and limited (6-10), so no ask is created;
partner's raise and pass ladders already own the seat.

**What it endangers, in `general_uncontested_continuation`:**
* `uc_raise_$m3` (27) and `uc_raise_$m2` (30) — raising partner's second suit
  with three small when you hold six of your own is the losing description.
* `uc_new_$X2` / `_hi` (26 / 26.5) — a *new* suit; this is my own, already
  bid.
* `uc_pass` (18) — a six-card suit is not "nothing further to show".
* It sits **below** `uc_raise_$M4` (32), `uc_raise_lott4_$M` (32) and
  `uc_raise_$M3` (31): a genuine major-suit fit still outranks repeating a
  minor, which is right.
* It does **not** reach `uc_rebid_$X2` (29) on that rule's own band (11+),
  because the two bands are disjoint.

**VERIFIED.**  `{suits: {S: [6,13]}, evals: {total_points: [6,10],
"suit_quality(S)": [1,9]}}` scores **fit 1.000** at the real seat, against
`uc_rebid_S2` 0.134 and `uc_raise_D3` 1.000/27.

**Template:** `expand: { X: [C, D, H, S] }` across the five generic families
= 20 rules from one idea.

---

## Board 528 — margin -7

**Seat/call that went wrong:** table A, call 10, **South passes** on
`Q642.742.K52.KJ7` after `1C P 1S X 2S P P X P 3H`.  Partner's **support
double** showed exactly three spades, so we hold seven counted trumps and
nine support points, and the opponents have doubled twice and bid a suit.
`ch_raise_S3` scores **0.800** — one point short of its 10-point floor and
one trump short of its eight-trump floor — and `ch_pass` at 1.00 takes it.

**The missing agreement:** the competitive raise ladder is calibrated to a
*raise*, not to a **support double**, and a support double is the file's own
most precise length statement (`DECISIONS.md`: "X/XX = exactly 3-card
support, any strength").  Seven known trumps and a fourth trump of my own is
a competitive raise on the Law; nine points is not the question.

**Context:** `general_competitive_high` (and the `cl_` twin).

```yaml
      # THE SUPPORT DOUBLE IS THE FILE'S MOST PRECISE LENGTH STATEMENT and no
      # raise rung is keyed to it.  ch_raise_$M3 wants ten support points and
      # eight counted trumps; after a support double we know SEVEN exactly,
      # and a fourth trump of my own with nine points is a competitive raise
      # by the Law, not a pass.
      - id: ch_raise_law3_$M
        call: 3$M
        priority: 31.5
        when: { partner_suit: $M, is_competitive: true, cheapest_in_suit: true,
                we_hold_contract: false }
        requires:
          suits: { $M: [4, 13] }
          evals: { total_points: [7, 10], "lott_total_trumps($M)": [7, 26] }
        shows: "competitive raise on four trumps: seven counted, 7-10 points, they are bidding"
        establishes: { forcing: non_forcing, agreed_suit: $M }
```

**Answering seat:** `non_forcing` and limited (7-10); opener's continuation is
`general_competitive_high` / `general_balancing_high`, both authored.

**What it endangers, in `general_competitive_high`:**
* `ch_pass` (22) — with four trumps opposite a shown three and a live
  auction, passing them into 3H is the losing action.
* `ch_raise_$M3` (31) — the same call with a higher floor; the two are
  disjoint at 10 points, and mine only reaches the band the other cannot.
* `ch_nt3` (29), `ch_new_$X3/_hi` (27 / 27.5), `ch_rebid_$M3` (29) — all
  describe something other than the fit we have already found.
* It sits **below** `ch_raise_$M4` (32), `ch_raise_lott_$M4` (32) and
  `ch_penalty_X` (38), so a genuine game raise, a Law-level raise and a trump
  stack all keep their hands.

**VERIFIED.**  `{suits: {S: [4,13]}, evals: {total_points: [7,10],
"lott_total_trumps(S)": [7,26]}}` scores **fit 1.000** on `Q642.742.K52.KJ7`
at the real seat (total_points 9, seven counted trumps).  Note the first
draft of this gate carried `their_fit: [8, 26]` and scored **0.028** — the
opponents' shown fit here is only 4, because they have doubled rather than
raised.  That is a **negative prototype**: `their_fit` is the wrong gate in a
double-and-bid auction, and I removed it rather than shipping it.

**Template:** `expand: { M: [H, S] }` in `cl_`, `ch_` and `balhigh_` = six
rules; the minor twin at 3$m adds six more.

---

## Board 538 — margin -7

**NOTHING-WRONG (constructive).**  The first divergence is West passing in
first seat on `KT3.QJT743.65.73` (6 HCP, six hearts, vulnerable) where BEN
opens a weak 2H.  `open_weak_2H_vul` scores **0.800** — the vulnerable weak
two is disciplined to **7-10 HCP with two of the top three**, an explicit
`DECISIONS.md` agreement ("weak twos are disciplined... vulnerable tightens
to 7-10 with 2 of the top 3"), and `QJT743` has neither seven points nor two
of the top three.

The rule is doing exactly what the system says it should.  Whether the
discipline is right is a preempt-style question and belongs to the
competitive reviewer; nothing in the constructive machinery is missing here.

What else I checked: table B's second decision (East passing partner's
3C preempt with `A864.A85.K53.A72`-shaped values) is the same family as board
587 below and is covered by that proposal; table A is BEN's auction from
call 1 onward.

---

## Board 587 — margin -7

**Seat/call that went wrong:** table A, call 3, **South passes** on
`AKJ8.632.A864.AJ` after `P 3C P`.  Seventeen HCP, the ace of partner's
seven-card suit, spades and diamonds stopped — and `rp3_C_game` (3NT) scores
**0.067** because its gate is `weakest_unshown_stopper: [0.9, 9]`, which
demands **all three** side suits stopped and South's hearts are `632`.
`rp3_C_pass` fits 1.00 and we played 3C for +150 while 3NT is ten tricks.

**The missing agreement:** 3NT opposite a preempt is a **counting** decision —
a source of tricks plus enough stoppers — and the file's only 3NT rung
demands perfection in every side suit.  The practical agreement is: a fitting
top honour in partner's seven-card suit, sixteen-plus, and **two of the three**
side suits stopped.

**Context:** `resp_preempt_C` and `resp_preempt_D` (existing; the major-suit
twins keep their present gate — a stopper argument is about notrump, not
about a major-suit game, which is the file's own note).

```yaml
      # THE ALL-OR-NOTHING STOPPER GATE.  rp3_C_game wants EVERY unshown suit
      # stopped, so a 17-count with a fitting ace in partner's seven-card suit
      # and two of the three side suits stopped scored 0.067 and passed a
      # ten-trick 3NT.  Opposite a preempt 3NT is a counting decision: the
      # source of tricks first, then two stoppers, then the gamble.
      - id: rp3_C_3NT_source
        call: 3NT
        priority: 61
        requires:
          suits: { C: [2, 13] }
          evals: { total_points: [16, 40], "lott_total_trumps(C)": [9, 26] }
          features: [ "top_honour(C)" ]
          any_of:
            - evals: { "stoppers(S)": [1, 1], "stoppers(H)": [1, 1] }
            - evals: { "stoppers(S)": [1, 1], "stoppers(D)": [1, 1] }
            - evals: { "stoppers(H)": [1, 1], "stoppers(D)": [1, 1] }
        shows: "3NT on a source of tricks: a fitting top honour opposite the seven-card suit, 16+, and two of the three side suits stopped"
        establishes: { forcing: sign_off }
```
The `resp_preempt_D` twin is the same rule with C→D and the `any_of` triple
built from S, H, C.  `stoppers` is registered sharp (s2 = 0.3), so these
gates really gate — unlike `weakest_their_stopper`.

**Answering seat:** none — a sign-off in game, and the preemptor's seat over
our 3NT is correctly silent (`we_hold_contract` is true once partner's game
bid stands, so the generic toolkit is switched off and the code fallback
passes).  This is the one place where "no answering seat" is the right
answer rather than the round-17 failure mode.

**What it endangers, in `resp_preempt_C`:**
* `rp3_C_pass` (40) — its `any_of` branch `weakest_unshown_stopper: [0, 0.5]`
  fits **1.00** on exactly the hands this rule is about, which is why the
  seat passed; 61 beats 40 and takes them.
* It sits **below** `rp3_C_D` / `_H` / `_S` (62), so a genuine 5+ side suit
  with 15+ still forces with the new suit first — correct, because that
  auction can still reach 3NT afterwards.
* It sits **below** `rp3_C_rkc` (66), so the nine-card-fit slam try is
  untouched.
* Against the file, `uc_raise_C4` (27) and `uc_minor_game_5C` (28) are
  different calls and unaffected.

**VERIFIED.**  The whole `requires` block above scores **fit 1.000** on
`AKJ8.632.A864.AJ` at the real seat (total_points 17, `lott_total_trumps(C)`
9, `top_honour(C)` 1, `stoppers(S)` 1 and `stoppers(D)` 1, `stoppers(H)` 0),
against `rp3_C_game` 0.067 and `rp3_C_pass` 1.000/40.

**Template:** two rules (C and D contexts — they are not templated).  The
same "source of tricks" idea is owed to `resp_preempt_H` / `resp_preempt_S`
in the *minor-suit-game* form and to the four-level preempt responses; those
are four more rules and a separate agreement.

---

## Closing note for the consolidator

Three of these proposals are the same rung wearing different clothes and
should be merged before implementation:

* **boards 100, 107, 325, 528** all add an invitational or Law-based raise
  into the generic families.  They are four disjoint `when` clauses on one
  idea — *"the raise ladder's gates are calibrated to a constructive auction
  opposite an unlimited partner, and every other auction (a forced reply, an
  overcall, a rebid suit, a support double) needs the counted fit instead of
  the points estimate."*  One family of eight to twelve rules would carry all
  four boards.
* **boards 114 and 217** are the two halves of the same context
  (`opener_neg_double_over_raise`): the cue with 18+, and the pass with a
  minimum.  Ship them together or neither — the cue without the floor makes
  the over-bidding worse, and the floor without the cue silences the monster.
* **boards 7 and 114** share one `expand_pairs` table in
  `neg_double_3level_m`; write it once.

And one thing I could not do from inside the constructive lane, which the
round should note: **boards 85, 306, 353 and 455 all turn on a soft-miss
between 0.40 and 0.80 in a seat whose ladder has a points floor the system's
own opening rules contradict.**  That is not four agreements, it is one
systematic sweep — every `hcp: [12, ...]` floor in an opener-rebid context,
against a system that opens ten-counts by the rule of 20 — and it is
mechanically checkable without any bridge judgement at all.
