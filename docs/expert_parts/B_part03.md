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
