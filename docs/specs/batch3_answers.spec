# ============================================================================
# BATCH 3 - THE STARVED ANSWERING SEATS
#
# Round 18, system editor's batch.  Every section below exists because the
# file already ASKS a question it cannot hear the answer to.  Nothing here
# invents a new force without shipping the seat that answers it, and every
# ladder ends in a `requires: {}` rung at the BOTTOM, so no seat this batch
# creates can ever be starved in its turn.
#
# Floor convention used throughout: catch-all rungs sit at priority 44 (a
# pass or a cheapest rebid), the descriptive rungs above them at 50-68.
# 44 clears every generic rung that could otherwise answer a force by
# accident - uc_pass 18, uc_new_* 25-27.5, uc_nt2/nt3 28/29, uc_raise_*
# 30-32, uc_doubler_* 33-35, gf_landing_* 30-38 - and clears them by a
# margin, so a hole in one of MY ladders still lands on MY floor.
# ============================================================================


# ============================================================================
# ITEM 1 - THE CUE-RAISE ANSWERING FAMILY
# Five cue-raise rules, zero answering contexts:
#   r1H1S_cue   1H - (1S) - 2S       agreed H, one_round
#   nx_1m1H_cue 1m - (1H) - 2H       agreed m, one_round
#   nx_1m1S_cue 1m - (1S) - 2S       agreed m, one_round
#   r1M2x_cue   1M - (2x) - 3x       agreed M, one_round
#   advo_cue    (1o) - 1v - P - 2o   agreed v, one_round
# nx3_cue is NOT in this batch: `opener_over_nx3_cue` already answers it.
# ============================================================================

#== CONTEXT
  - id: opener_over_cue_raise_1H1S
    description: "Opener answers responder's cue-bid raise after 1H - (1S) - 2S"
    # Shape before aces.  The splinter and the five-five sit ABOVE the keycard
    # ask deliberately: asking for keycards on a two-suiter is how a pair
    # reaches 6H off two cashing tricks.  No 4NT rung is authored here at all -
    # once a rung below sets game_forced with a suit agreed, the file's single
    # audited `rkc_4NT` (priority 45) becomes live on its own.
    pattern: "1H - 1S - 2S - P - ?"
    rules:
      - id: cra1_splinter_4C
        call: 4C
        priority: 62
        requires:
          suits: { H: [5, 13], C: [0, 1] }
          evals: { total_points: [15, 40] }
        shows: "shortness slam try opposite the cue-bid raise: singleton or void in clubs"
        establishes: { forcing: game_forcing, agreed_suit: H }
        alertable: true
        convention: splinter
      - id: cra1_splinter_4D
        call: 4D
        priority: 62
        requires:
          suits: { H: [5, 13], D: [0, 1] }
          evals: { total_points: [15, 40] }
        shows: "shortness slam try opposite the cue-bid raise: singleton or void in diamonds"
        establishes: { forcing: game_forcing, agreed_suit: H }
        alertable: true
        convention: splinter
      - id: cra1_second_3C
        call: 3C
        priority: 60
        requires:
          suits: { H: [5, 13], C: [5, 13] }
          evals: { total_points: [14, 40] }
        shows: "my real second suit opposite the cue-bid raise: five-five, hearts already agreed, so this is a slam try and not a rescue"
        establishes: { forcing: game_forcing, agreed_suit: H }
      - id: cra1_second_3D
        call: 3D
        priority: 60
        requires:
          suits: { H: [5, 13], D: [5, 13] }
          evals: { total_points: [14, 40] }
        shows: "my real second suit opposite the cue-bid raise: five-five, hearts already agreed, so this is a slam try and not a rescue"
        establishes: { forcing: game_forcing, agreed_suit: H }
      - id: cra1_game_4H
        call: 4H
        priority: 52
        requires:
          evals: { total_points: [14, 40] }
        shows: "accepting the cue-bid raise: game in the agreed major, nothing extra to describe"
        establishes: { forcing: sign_off, agreed_suit: H }
      - id: cra1_min_3H
        call: 3H
        priority: 44
        requires: {}
        shows: "a minimum opening opposite the cue-bid raise: partner passes with a bare limit raise"
        establishes: { forcing: invitational, agreed_suit: H }
        negative_inference_weight: soft

#== CONTEXT
  - id: responder_over_cue_raise_second_1H1S
    description: "Responder answers opener's five-five slam try over the cue-bid raise"
    expand: { x: [C, D] }
    pattern: "1H - 1S - 2S - P - 3$x - P - ?"
    rules:
      - id: crr1_game_$x
        call: 4H
        priority: 44
        requires: {}
        shows: "no slam ambition opposite the five-five: game in the agreed major"
        establishes: { forcing: sign_off, agreed_suit: H }
        negative_inference_weight: soft

#== CONTEXT
  - id: responder_over_cue_raise_splinter_1H1S
    description: "Responder answers opener's shortness slam try over the cue-bid raise"
    expand: { x: [C, D] }
    pattern: "1H - 1S - 2S - P - 4$x - P - ?"
    rules:
      - id: crr1_wasted_$x
        call: 4H
        priority: 46
        requires: { evals: { wasted_in_partner_shortness: [3, 40] } }
        shows: "wasted honours opposite the shown shortness: the agreed game is enough, do not ask"
        establishes: { forcing: sign_off, agreed_suit: H }
      - id: crr1_floor_$x
        call: 4H
        priority: 44
        requires: {}
        shows: "signing off in the agreed game over the shortness slam try"
        establishes: { forcing: sign_off, agreed_suit: H }
        negative_inference_weight: soft

#== CONTEXT
  - id: responder_over_cue_raise_minimum_1H1S
    description: "Responder answers opener's minimum 3H over the cue-bid raise"
    pattern: "1H - 1S - 2S - P - 3H - P - ?"
    rules:
      - id: crr1_accept_3H
        call: 4H
        priority: 50
        requires: { evals: { total_points: [12, 40] } }
        shows: "better than the bare limit raise the cue promised: accepting the minimum's invitation"
        establishes: { forcing: sign_off, agreed_suit: H }
      - id: crr1_decline_3H
        call: P
        priority: 44
        requires: {}
        shows: "a bare limit raise opposite a minimum opening: three of the agreed major is the contract"
        establishes: { forcing: sign_off }
        negative_inference_weight: soft

#== CONTEXT
  - id: opener_over_cue_raise_1m_1M
    description: "Opener answers responder's cue-bid raise of the minor after 1m - (1M) - 2M"
    expand_pairs:
      - { m: C, M: H }
      - { m: C, M: S }
      - { m: D, M: H }
      - { m: D, M: S }
    pattern: "1$m - 1$M - 2$M - P - ?"
    rules:
      - id: cram_3NT_$m$M
        call: 3NT
        priority: 58
        requires:
          evals: { total_points: [15, 40], weakest_unshown_stopper: [0.9, 9] }
        shows: "nine tricks opposite the limit-raise cue: the suits we have not shown are stopped"
        establishes: { forcing: sign_off }
      - id: cram_2NT_$m$M
        call: 2NT
        priority: 54
        requires:
          evals: { total_points: [12, 14] }
          features: [ "stopper($M)" ]
        shows: "their suit stopped but only a minimum opening: inviting the notrump game"
        establishes: { forcing: invitational }
      - id: cram_min_$m$M
        call: 3$m
        priority: 44
        requires: {}
        shows: "a minimum opening with no stopper for notrump: three of the agreed minor"
        establishes: { forcing: non_forcing, agreed_suit: $m }
        negative_inference_weight: soft

#== CONTEXT
  - id: responder_over_cue_raise_minor_2NT
    description: "The cue-bidder answers opener's invitational 2NT"
    expand_pairs:
      - { m: C, M: H }
      - { m: C, M: S }
      - { m: D, M: H }
      - { m: D, M: S }
    pattern: "1$m - 1$M - 2$M - P - 2NT - P - ?"
    rules:
      - id: crrm_3NT_$m$M
        call: 3NT
        priority: 50
        requires: { evals: { total_points: [12, 40] } }
        shows: "more than the ten points the cue promised: accepting the notrump invitation"
        establishes: { forcing: sign_off }
      - id: crrm_pass_$m$M
        call: P
        priority: 44
        requires: {}
        shows: "a bare limit raise opposite a minimum: 2NT is high enough"
        establishes: { forcing: sign_off }
        negative_inference_weight: soft

#== CONTEXT
  - id: responder_over_cue_raise_minor_min
    description: "The cue-bidder answers opener's minimum three of the minor"
    expand_pairs:
      - { m: C, M: H }
      - { m: C, M: S }
      - { m: D, M: H }
      - { m: D, M: S }
    pattern: "1$m - 1$M - 2$M - P - 3$m - P - ?"
    rules:
      - id: crrn_3NT_$m$M
        call: 3NT
        priority: 50
        requires:
          evals: { total_points: [13, 40] }
          features: [ "stopper($M)" ]
        shows: "I hold the stopper opener denied: nine tricks beat eleven"
        establishes: { forcing: sign_off }
      - id: crrn_game_$m$M
        call: 5$m
        priority: 48
        requires:
          suits: { $m: [5, 13] }
          evals: { total_points: [15, 40] }
        shows: "no stopper on either side but the values and the trumps for eleven tricks"
        establishes: { forcing: sign_off, agreed_suit: $m }
      - id: crrn_pass_$m$M
        call: P
        priority: 44
        requires: {}
        shows: "opener is minimum and nobody has their suit stopped: three of the minor is the contract"
        establishes: { forcing: sign_off }
        negative_inference_weight: soft

#== CONTEXT
  - id: opener_over_cue_raise_1M_2x
    description: "Opener answers responder's cue-bid raise after 1M - (2x) - 3x"
    expand_pairs:
      - { M: H, x: C }
      - { M: H, x: D }
      - { M: S, x: C }
      - { M: S, x: D }
      - { M: S, x: H }
    pattern: "1$M - 2$x - 3$x - P - ?"
    rules:
      - id: cra2_game_$M$x
        call: 4$M
        priority: 52
        requires: { evals: { total_points: [13, 40] } }
        shows: "accepting the limit-raise-or-better cue: game in the agreed major"
        establishes: { forcing: sign_off, agreed_suit: $M }
      - id: cra2_min_$M$x
        call: 3$M
        priority: 44
        requires: {}
        shows: "a minimum opening opposite the cue: three of the agreed major, partner may pass"
        establishes: { forcing: invitational, agreed_suit: $M }
        negative_inference_weight: soft

#== CONTEXT
  - id: responder_over_cue_raise_1M_2x_min
    description: "The cue-bidder answers opener's minimum three of the major"
    expand_pairs:
      - { M: H, x: C }
      - { M: H, x: D }
      - { M: S, x: C }
      - { M: S, x: D }
      - { M: S, x: H }
    pattern: "1$M - 2$x - 3$x - P - 3$M - P - ?"
    rules:
      - id: crr2_accept_$M$x
        call: 4$M
        priority: 50
        requires: { evals: { total_points: [13, 40] } }
        shows: "better than the limit raise the cue promised: bidding the game opener could not"
        establishes: { forcing: sign_off, agreed_suit: $M }
      - id: crr2_decline_$M$x
        call: P
        priority: 44
        requires: {}
        shows: "a bare limit raise opposite a minimum: three of the major is high enough in competition"
        establishes: { forcing: sign_off }
        negative_inference_weight: soft

#== CONTEXT
  - id: overcaller_over_cue_raise
    description: "The overcaller answers advancer's cue-bid raise (1o) 1v P 2o"
    # Only the RHO-passes shape.  `advance_cue_doubled` already owns
    # "1$o - 1$v - P - 2$o - X - ?" at the same specificity and, being earlier
    # in the file, wins the tie for XX and 2$v - so a `* ` token here would
    # silently lose this ladder's floor after a double.  The doubled branch
    # keeps its own authored retreat.
    expand_pairs:
      - { o: C, v: H }
      - { o: C, v: S }
      - { o: D, v: H }
      - { o: D, v: S }
      - { o: H, v: S }
    pattern: "1$o - 1$v - P - 2$o - P - ?"
    rules:
      - id: advcue_game_$o$v
        call: 4$v
        priority: 56
        requires:
          suits: { $v: [5, 13] }
          evals: { total_points: [14, 40] }
        shows: "a full opening opposite the limit-raise cue: bidding the game"
        establishes: { forcing: sign_off, agreed_suit: $v }
      - id: advcue_inv_$o$v
        call: 3$v
        priority: 52
        requires:
          suits: { $v: [5, 13] }
          evals: { total_points: [11, 13] }
        shows: "a sound overcall opposite a limit raise: competing to the three level and inviting"
        establishes: { forcing: invitational, agreed_suit: $v }
      - id: advcue_sign_$o$v
        call: 2$v
        priority: 44
        requires: {}
        shows: "a minimum overcall: the cheapest rebid of my suit, no game interest"
        establishes: { forcing: non_forcing, agreed_suit: $v }
        negative_inference_weight: soft

#== CONTEXT
  - id: advancer_over_overcall_invite
    description: "Advancer answers the overcaller's invitational three of his suit"
    expand_pairs:
      - { o: C, v: H }
      - { o: C, v: S }
      - { o: D, v: H }
      - { o: D, v: S }
      - { o: H, v: S }
    pattern: "1$o - 1$v - P - 2$o - P - 3$v - P - ?"
    rules:
      - id: advcr_accept_$o$v
        call: 4$v
        priority: 50
        requires: { evals: { total_points: [13, 40] } }
        shows: "the top of the cue-bid raise opposite a sound overcall: bidding the game"
        establishes: { forcing: sign_off, agreed_suit: $v }
      - id: advcr_decline_$o$v
        call: P
        priority: 44
        requires: {}
        shows: "a bare eleven opposite a sound overcall: three of our suit is the contract"
        establishes: { forcing: sign_off }
        negative_inference_weight: soft


# ============================================================================
# ITEM 2 - FOURTH SUIT FORCING: THE THIRD ANSWER AND THE FLOOR
#
# `fourth_suit_reply` had exactly two rungs - "stopper" and "three-card
# support".  Opener with neither (5-5, no stopper, a doubleton in partner's
# suit) topped out at fit 0.349 and the soft-miss lottery handed him
# `fsfr_raise_$F`, a raise he does not hold (board 945: 3S on two spades,
# keycards asked on a 27-count, 5S played).
#
# The reply context's `expand_pairs` cannot be edited by `addrules.py`
# (it appends rules only), so the third answer is written with the EXISTING
# vars plus `when: { my_suit: X, cheapest_in_suit: true }`, which selects
# opener's own suits and the cheapest call in each of them.  The five auctions
# and what each rung reaches:
#   1C-1H-1S-(2D)  my suits C,S  -> 3C / 2S
#   1C-1D-1S-(2H)  my suits C,S  -> 3C / 2S
#   1D-1H-1S-(2C)  my suits D,S  -> 2D / 2S
#   1D-1S-2C-(2H)  my suits D,C  -> 3D / 3C
#   1H-1S-2C-(2D)  my suits H,C  -> 2H / 3C
# Every one of the ten rungs is legal in exactly the auctions it should be:
# `cheapest_in_suit` drops the 3D rung where 2D is available and the engine's
# own legality check drops 2D where the fourth suit has passed it.
# ============================================================================

#== RULES fourth_suit_reply
      # THE THIRD ANSWER: no stopper and no third trump is the commonest hand
      # of the three, and it had no rung at all.  Extra length in one of my own
      # two suits is what partner needs to hear next.  Priced by CHEAPNESS, so
      # a five-five bids the call that leaves partner the most room.
      - id: fsfr_extra_D2_$F
        call: 2D
        priority: 63.5
        when: { my_suit: D, cheapest_in_suit: true }
        requires:
          suits: { D: [5, 13] }
          evals: { "stoppers($FS)": [0, 0.5] }
        shows: "no $FS stopper and no third $RS: five or more diamonds, the game force continues"
        establishes: { forcing: game_forcing }
      - id: fsfr_extra_H2_$F
        call: 2H
        priority: 63
        when: { my_suit: H, cheapest_in_suit: true }
        requires:
          suits: { H: [6, 13] }
          evals: { "stoppers($FS)": [0, 0.5] }
        shows: "no $FS stopper and no third $RS: a sixth heart, the game force continues"
        establishes: { forcing: game_forcing }
      - id: fsfr_extra_S2_$F
        call: 2S
        priority: 62.5
        when: { my_suit: S, cheapest_in_suit: true }
        requires:
          suits: { S: [5, 13] }
          evals: { "stoppers($FS)": [0, 0.5] }
        shows: "no $FS stopper and no third $RS: five or more spades, the game force continues"
        establishes: { forcing: game_forcing }
      - id: fsfr_extra_C3_$F
        call: 3C
        priority: 62
        when: { my_suit: C, cheapest_in_suit: true }
        requires:
          suits: { C: [5, 13] }
          evals: { "stoppers($FS)": [0, 0.5] }
        shows: "no $FS stopper and no third $RS: five or more clubs, the game force continues"
        establishes: { forcing: game_forcing }
      - id: fsfr_extra_D3_$F
        call: 3D
        priority: 61.5
        when: { my_suit: D, cheapest_in_suit: true }
        requires:
          suits: { D: [5, 13] }
          evals: { "stoppers($FS)": [0, 0.5] }
        shows: "no $FS stopper and no third $RS: five or more diamonds, the game force continues"
        establishes: { forcing: game_forcing }
      # THE FLOOR.  A game-forcing ask must never leave its answerer with
      # nothing that fits.  One floor per suit I have actually bid, priced so
      # the CHEAPEST of my own suits wins; at least one is always live and
      # legal, and every one of them fits 1.00.
      - id: fsfr_floor_D2_$F
        call: 2D
        priority: 47.5
        when: { my_suit: D, cheapest_in_suit: true }
        requires: {}
        shows: "nothing to add to the fourth suit: back to my own suit, the game force continues"
        establishes: { forcing: game_forcing }
        negative_inference_weight: soft
      - id: fsfr_floor_H2_$F
        call: 2H
        priority: 47
        when: { my_suit: H, cheapest_in_suit: true }
        requires: {}
        shows: "nothing to add to the fourth suit: back to my own suit, the game force continues"
        establishes: { forcing: game_forcing }
        negative_inference_weight: soft
      - id: fsfr_floor_S2_$F
        call: 2S
        priority: 46.5
        when: { my_suit: S, cheapest_in_suit: true }
        requires: {}
        shows: "nothing to add to the fourth suit: back to my own suit, the game force continues"
        establishes: { forcing: game_forcing }
        negative_inference_weight: soft
      - id: fsfr_floor_C3_$F
        call: 3C
        priority: 43
        when: { my_suit: C, cheapest_in_suit: true }
        requires: {}
        shows: "nothing to add to the fourth suit: back to my own suit, the game force continues"
        establishes: { forcing: game_forcing }
        negative_inference_weight: soft
      - id: fsfr_floor_D3_$F
        call: 3D
        priority: 42.5
        when: { my_suit: D, cheapest_in_suit: true }
        requires: {}
        shows: "nothing to add to the fourth suit: back to my own suit, the game force continues"
        establishes: { forcing: game_forcing }
        negative_inference_weight: soft


# ============================================================================
# ITEM 3 - THE FORCING NEW SUIT OPPOSITE A WEAK TWO
#
# A named open item and the fourth instance of the species.  `rw2_new_$W_$X`
# is `forcing: one_round` (5+ suit, 12+ HCP, 0-2 in opener's suit) and
# `2$W - P - <new suit> - P - ?` matches no context: the generic toolkit
# invents a rebid, responder passes it, and 2D-2S-3D-P dies at -100 where
# 2D-2S-3D-3H-P is +140.
#
# The raise branch and the rebid branch are separate contexts because the
# raise call differs: with a major the raise is cheap and right, with a minor
# it would be 4C/4D, past 3NT, and is deliberately not authored.
# ============================================================================

#== CONTEXT
  - id: opener_after_weak2_new_major
    description: "Weak-two opener answers responder's forcing new major"
    expand_pairs:
      - { W: D, X: H, R: 2H, A: 3H, K: DH }
      - { W: D, X: S, R: 2S, A: 3S, K: DS }
      - { W: H, X: S, R: 2S, A: 3S, K: HS }
      - { W: S, X: H, R: 3H, A: 4H, K: SH }
    pattern: "2$W - P - $R - P - ?"
    rules:
      - id: w2a_raise_$K
        call: $A
        priority: 60
        requires: { suits: { $X: [3, 13] } }
        shows: "three-card support for the forcing new suit: the fit partner asked about"
        establishes: { forcing: non_forcing, agreed_suit: $X }
      - id: w2a_rebid_$K
        call: 3$W
        priority: 44
        requires: {}
        shows: "no third card in partner's suit: rebidding the six-card suit the weak two promised"
        establishes: { forcing: non_forcing }
        negative_inference_weight: soft

#== CONTEXT
  - id: opener_after_weak2_new_minor
    description: "Weak-two opener answers responder's forcing new minor"
    # No raise rung: the raise would be 4C or 4D, past 3NT, and a weak two with
    # three of partner's minor has nothing to say that is worth that room.
    expand_pairs:
      - { W: D, R: 3C, K: DC }
      - { W: H, R: 3C, K: HC }
      - { W: H, R: 3D, K: HD }
      - { W: S, R: 3C, K: SC }
      - { W: S, R: 3D, K: SD }
    pattern: "2$W - P - $R - P - ?"
    rules:
      - id: w2b_rebid_$K
        call: 3$W
        priority: 44
        requires: {}
        shows: "rebidding the six-card suit the weak two promised: the whole hand is already shown"
        establishes: { forcing: non_forcing }
        negative_inference_weight: soft

#== CONTEXT
  - id: responder_after_weak2_rebid
    description: "Responder after the weak-two opener rebids his own suit"
    expand_pairs:
      - { W: D, R: 2H, K: DH }
      - { W: D, R: 2S, K: DS }
      - { W: D, R: 3C, K: DC }
      - { W: H, R: 2S, K: HS }
      - { W: H, R: 3C, K: HC }
      - { W: H, R: 3D, K: HD }
      - { W: S, R: 3C, K: SC }
      - { W: S, R: 3D, K: SD }
      - { W: S, R: 3H, K: SH }
    pattern: "2$W - P - $R - P - 3$W - P - ?"
    rules:
      - id: w2r_second_H_$K
        call: 3H
        priority: 56
        when: { unbid_suit: H, cheapest_in_suit: true }
        requires: { suits: { H: [5, 13] } }
        shows: "a second five-card suit: partner may prefer it to his own six"
        establishes: { forcing: non_forcing }
      - id: w2r_second_S_$K
        call: 3S
        priority: 55
        when: { unbid_suit: S, cheapest_in_suit: true }
        requires: { suits: { S: [5, 13] } }
        shows: "a second five-card suit: partner may prefer it to his own six"
        establishes: { forcing: non_forcing }
      - id: w2r_3NT_$K
        call: 3NT
        priority: 52
        requires:
          hcp: [15, 40]
          evals: { weakest_unshown_stopper: [0.9, 9] }
        shows: "no fit anywhere but the values and the stoppers for nine tricks"
        establishes: { forcing: sign_off }
      - id: w2r_pass_$K
        call: P
        priority: 44
        requires: {}
        shows: "opener has a minimum with no fit: three of his own suit is where we play"
        establishes: { forcing: sign_off }
        negative_inference_weight: soft

#== CONTEXT
  - id: opener_after_weak2_second_suit
    description: "The weak-two opener answers responder's second suit"
    expand_pairs:
      - { W: D, R: 2S, Y: 3H, Z: H, G: 4H, K: DSH }
      - { W: D, R: 3C, Y: 3H, Z: H, G: 4H, K: DCH }
      - { W: D, R: 3C, Y: 3S, Z: S, G: 4S, K: DCS }
      - { W: D, R: 2H, Y: 3S, Z: S, G: 4S, K: DHS }
      - { W: H, R: 3C, Y: 3S, Z: S, G: 4S, K: HCS }
      - { W: H, R: 3D, Y: 3S, Z: S, G: 4S, K: HDS }
    pattern: "2$W - P - $R - P - 3$W - P - $Y - P - ?"
    rules:
      - id: w2s_raise_$K
        call: $G
        priority: 52
        requires:
          suits: { $Z: [4, 13] }
          hcp: [8, 10]
        shows: "a maximum weak two with four-card support for the second suit: bidding the game"
        establishes: { forcing: sign_off, agreed_suit: $Z }
      - id: w2s_pass_$K
        call: P
        priority: 44
        requires: {}
        shows: "the weak two has shown its whole hand already: passing the second suit"
        establishes: { forcing: sign_off }
        negative_inference_weight: soft

#== CONTEXT
  - id: responder_after_weak2_raise
    description: "Responder after the weak-two opener raises the forcing new suit"
    expand_pairs:
      - { W: D, R: 2H, A: 3H, G: 4H, X: H, K: DH }
      - { W: D, R: 2S, A: 3S, G: 4S, X: S, K: DS }
      - { W: H, R: 2S, A: 3S, G: 4S, X: S, K: HS }
    pattern: "2$W - P - $R - P - $A - P - ?"
    rules:
      - id: w2g_game_$K
        call: $G
        priority: 50
        requires: { evals: { total_points: [15, 40] } }
        shows: "the fit is there and I have more than the twelve the new suit promised: game"
        establishes: { forcing: sign_off, agreed_suit: $X }
      - id: w2g_pass_$K
        call: P
        priority: 44
        requires: {}
        shows: "a bare twelve opposite three-card support from a weak two: three is high enough"
        establishes: { forcing: sign_off }
        negative_inference_weight: soft


# ============================================================================
# ITEM 4 - THE REVERSE THAT IS FORCING WITH NO ANSWER BELOW 8 POINTS
#
# Every `rrev*` rung floors at hcp 8, so a 4-count with six spades fits
# nothing above 0.028 and `uc_pass` takes a one-round force at fit 1.00
# (board 506).  `rrevh_2S` never fires in the whole corpus.
#
# The agreement: a reverse is forcing, so responder always bids - with a
# five-card suit he rebids it cheaply to show 0-7, otherwise he takes a
# preference to opener's FIRST suit.  The preference is authored twice per
# context, once at 8+ as a one-round force and once as the `requires: {}`
# floor, so the same call has one meaning per strength band and the seat can
# never be starved.
# ============================================================================

#== RULES responder_reverse_rebid_major
      - id: rrev_min_2$M
        call: 2$M
        priority: 67
        requires: { suits: { $M: [5, 13] }, hcp: [0, 7] }
        shows: "5+ $M under eight points: the cheap rebid a forcing reverse must not be passed with"
        establishes: { forcing: non_forcing }
      - id: rrev_floor_$M
        call: 3C
        priority: 40
        requires: {}
        shows: "under eight points and nothing to rebid: preference to opener's first suit"
        establishes: { forcing: non_forcing, agreed_suit: C }
        negative_inference_weight: soft

#== RULES responder_reverse_1C1S2H
      - id: rrevh_min_2S
        call: 2S
        priority: 67
        requires: { suits: { S: [5, 13] }, hcp: [0, 7] }
        shows: "5+ spades under eight points: the cheap rebid a forcing reverse must not be passed with"
        establishes: { forcing: non_forcing }
      - id: rrevh_floor_3C
        call: 3C
        priority: 40
        requires: {}
        shows: "under eight points and nothing to rebid: preference to opener's first suit"
        establishes: { forcing: non_forcing, agreed_suit: C }
        negative_inference_weight: soft

#== RULES responder_reverse_1D1S2H
      - id: rrevd_min_2S
        call: 2S
        priority: 67
        requires: { suits: { S: [5, 13] }, hcp: [0, 7] }
        shows: "5+ spades under eight points: the cheap rebid a forcing reverse must not be passed with"
        establishes: { forcing: non_forcing }
      - id: rrevd_floor_3D
        call: 3D
        priority: 40
        requires: {}
        shows: "under eight points and nothing to rebid: preference to opener's first suit"
        establishes: { forcing: non_forcing, agreed_suit: D }
        negative_inference_weight: soft

#== CONTEXT
  - id: opener_over_reverse_weak_rebid
    description: "Opener after responder's 0-7 spade rebid over the 2H reverse"
    expand: { m: [C, D] }
    pattern: "1$m - P - 1S - P - 2H - P - 2S - P - ?"
    rules:
      - id: oarw_game_$m
        call: 4S
        priority: 56
        requires:
          suits: { S: [3, 13] }
          evals: { total_points: [20, 40] }
        shows: "a big reverse with a fit: the game is there even opposite a bust"
        establishes: { forcing: sign_off, agreed_suit: S }
      - id: oarw_inv_$m
        call: 3S
        priority: 52
        requires:
          suits: { S: [3, 13] }
          evals: { total_points: [18, 19] }
        shows: "three-card support and a maximum reverse: inviting the 0-7 rebid to game"
        establishes: { forcing: invitational, agreed_suit: S }
      - id: oarw_pass_$m
        call: P
        priority: 44
        requires: {}
        shows: "the reverse has been answered with 0-7: this is the partscore"
        establishes: { forcing: sign_off }
        negative_inference_weight: soft

#== CONTEXT
  - id: responder_over_reverse_weak_raise
    description: "The 0-7 responder answers opener's invitational raise over the reverse"
    expand: { m: [C, D] }
    pattern: "1$m - P - 1S - P - 2H - P - 2S - P - 3S - P - ?"
    rules:
      - id: rarw_game_$m
        call: 4S
        priority: 50
        requires: { evals: { total_points: [6, 40] } }
        shows: "the top of the 0-7 rebid opposite an 18-19 reverse: accepting"
        establishes: { forcing: sign_off, agreed_suit: S }
      - id: rarw_pass_$m
        call: P
        priority: 44
        requires: {}
        shows: "a genuine bust: three of the major is where an 18-19 reverse belongs"
        establishes: { forcing: sign_off }
        negative_inference_weight: soft

#== CONTEXT
  - id: opener_over_reverse_2M_weak
    description: "Opener after responder's cheap major rebid over the 1C - 1M - 2D reverse"
    # 3$M is NOT authored here: `opener_raise_after_reverse` already defines it
    # at the same specificity and, being earlier in the file, owns the call.
    # This context adds only the pass that context never had.
    expand: { M: [H, S] }
    pattern: "1C - P - 1$M - P - 2D - P - 2$M - P - ?"
    rules:
      - id: oarm_pass_$M
        call: P
        priority: 44
        requires: {}
        shows: "no third card in partner's suit opposite a rebid that may be 0-7: this is the partscore"
        establishes: { forcing: sign_off }
        negative_inference_weight: soft

#== CONTEXT
  - id: responder_over_reverse_raise
    description: "Responder answers opener's forcing raise of his rebid major after the reverse"
    # Closes a force that already existed: `orev_raise_3$M` is
    # `forcing: one_round` and its seat returned only the generic contexts,
    # where `uc_nt3` bid 3NT at fit 1.000.
    expand: { M: [H, S] }
    pattern: "1C - P - 1$M - P - 2D - P - 2$M - P - 3$M - P - ?"
    rules:
      - id: rorr_game_$M
        call: 4$M
        priority: 50
        requires: { evals: { total_points: [7, 40] } }
        shows: "the fit is eight cards and I am not a bust: game in the agreed major"
        establishes: { forcing: sign_off, agreed_suit: $M }
      - id: rorr_pass_$M
        call: P
        priority: 44
        requires: {}
        shows: "a bust opposite the reverse: three of the agreed major is high enough"
        establishes: { forcing: sign_off }
        negative_inference_weight: soft

#== CONTEXT
  - id: opener_over_reverse_preference_2D
    description: "Opener after responder's club preference over the 1C - 1M - 2D reverse"
    expand: { M: [H, S] }
    pattern: "1C - P - 1$M - P - 2D - P - 3C - P - ?"
    rules:
      - id: oarp_3NT_$M
        call: 3NT
        priority: 52
        requires:
          evals: { total_points: [19, 40], weakest_unshown_stopper: [0.9, 9] }
        shows: "nineteen or more with everything stopped: nine tricks opposite the preference"
        establishes: { forcing: sign_off }
      - id: oarp_pass_$M
        call: P
        priority: 44
        requires: {}
        shows: "the preference may be a bust and nothing is stopped: three of my first suit"
        establishes: { forcing: sign_off }
        negative_inference_weight: soft

#== CONTEXT
  - id: opener_over_reverse_preference_2H
    description: "Opener after responder's minor preference over the 1m - 1S - 2H reverse"
    expand: { m: [C, D] }
    pattern: "1$m - P - 1S - P - 2H - P - 3$m - P - ?"
    rules:
      - id: oarq_3NT_$m
        call: 3NT
        priority: 52
        requires:
          evals: { total_points: [19, 40], weakest_unshown_stopper: [0.9, 9] }
        shows: "nineteen or more with everything stopped: nine tricks opposite the preference"
        establishes: { forcing: sign_off }
      - id: oarq_pass_$m
        call: P
        priority: 44
        requires: {}
        shows: "the preference may be a bust and nothing is stopped: three of my first suit"
        establishes: { forcing: sign_off }
        negative_inference_weight: soft


# ============================================================================
# ITEM 5 - RESPONDER'S INVITATIONAL JUMP REBID HAS NO ANSWERING SEAT
#
# `r1d1h2c_3H` and `r1d2c_3S` are `forcing: invitational`; at opener's seat
# `context_at` returns only the two generic contexts and `uc_pass` fits 1.000
# at priority 18.  Two cold games passed out at the three level (boards 132
# and 563).
#
# Two halves: (a) the seat that hears the invitation, and (b) the tier above
# the invitation, so a hand with game values never has to ask a question whose
# answer it already knows.  The 1H - 1S - 2m contexts get the jump rebid they
# never had at all, so half (a) has something to answer there too.
#
# The two REVERSE pairs a reviewer proposed (1C-1H-2D, 1C-1S-2D) are CUT: over
# a 17-21 reverse a `requires: {}` pass floor at opener's seat is a bug, not a
# floor.
# ============================================================================

#== CONTEXT
  - id: opener_over_responder_jump_rebid
    description: "Opener over responder's invitational jump rebid of his own suit"
    expand_pairs:
      - { Q: 1D, R: 1H, B: 2C, M: H, K: DHC }
      - { Q: 1D, R: 1S, B: 2C, M: S, K: DSC }
      - { Q: 1H, R: 1S, B: 2C, M: S, K: HSC }
      - { Q: 1H, R: 1S, B: 2D, M: S, K: HSD }
    pattern: "$Q - P - $R - P - $B - P - 3$M - P - ?"
    rules:
      - id: orjr_game_$K
        call: 4$M
        priority: 54
        requires:
          any_of:
            - suits: { $M: [2, 13] }
              evals: { total_points: [14, 40] }
            - suits: { $M: [3, 13] }
              evals: { total_points: [12, 40] }
        shows: "accepting: a doubleton and extras, or three-card support and any opening"
        establishes: { forcing: sign_off, agreed_suit: $M }
      - id: orjr_3NT_$K
        call: 3NT
        priority: 52
        requires:
          suits: { $M: [0, 1] }
          evals: { total_points: [14, 40], semi_balanced: [1, 1] }
        shows: "no fit for the long suit but the values for game: offering notrump instead"
        establishes: { forcing: sign_off }
      - id: orjr_pass_$K
        call: P
        priority: 44
        requires: {}
        shows: "declining the invitation: a dead minimum with no fit"
        establishes: { forcing: sign_off }
        negative_inference_weight: soft

#== RULES responder_rebid_1D_1H_2C
      # the tier that means 14+ never has to invite at all
      - id: r1d1h2c_4H
        call: 4H
        priority: 60
        requires:
          suits: { H: [6, 13] }
          evals: { total_points: [14, 40] }
        shows: "6+ hearts and game values: bidding the game rather than inviting it"
        establishes: { forcing: sign_off, agreed_suit: H }

#== RULES responder_after_1D1S_2C
      - id: r1d2c_4S
        call: 4S
        priority: 60
        requires:
          suits: { S: [6, 13] }
          evals: { total_points: [14, 40] }
        shows: "6+ spades and game values: bidding the game rather than inviting it"
        establishes: { forcing: sign_off, agreed_suit: S }

#== RULES responder_rebid_1H_1S_2C
      # this context had NO jump rebid of responder's own suit at all: a
      # six-card spade suit with 11+ and no heart fit could only choose between
      # a to-play 2S (6-10) and 3NT.
      - id: rr1H1SC_4S
        call: 4S
        priority: 58
        requires:
          suits: { S: [6, 13], H: [0, 2] }
          evals: { total_points: [14, 18] }
        shows: "6+ spades, no heart fit, game values: bidding the game"
        establishes: { forcing: sign_off, agreed_suit: S }
      - id: rr1H1SC_3S
        call: 3S
        priority: 57.5
        requires:
          suits: { S: [6, 13], H: [0, 2] }
          evals: { total_points: [11, 13] }
        shows: "6+ spades, no heart fit, invitational"
        establishes: { forcing: invitational }

#== RULES responder_rebid_1H_1S_2D
      - id: rr1H1SD_4S
        call: 4S
        priority: 58
        requires:
          suits: { S: [6, 13], H: [0, 2] }
          evals: { total_points: [14, 18] }
        shows: "6+ spades, no heart fit, game values: bidding the game"
        establishes: { forcing: sign_off, agreed_suit: S }
      - id: rr1H1SD_3S
        call: 3S
        priority: 57.5
        requires:
          suits: { S: [6, 13], H: [0, 2] }
          evals: { total_points: [11, 13] }
        shows: "6+ spades, no heart fit, invitational"
        establishes: { forcing: invitational }


# ============================================================================
# ITEM 6 - FOUR MORE UNAUTHORED CONSTRUCTIVE SEATS
#
#   1M - 1NT - 2M     board 300: `uc_nt2` bids 2NT over a sign-off, -300
#   1m - 1M - 2m - 2M board 151: `uc_raise_S3` raises a sign-off, one off
#   1m - (act) - 2m   board 508: `uc_nt2` bids 2NT over a competitive raise
#   2M - 3M           board 4:   `uc_raise_H4` accepts every invitation on 11
#
# The first two ship a raise rung, which is itself an invitation, so each
# ships its own answering context as well.
# ============================================================================

#== CONTEXT
  - id: opener_over_1NT_rebid_to_play
    description: "Opener hears responder's to-play 2M after the 1NT rebid"
    expand: { m: [C, D], M: [H, S] }
    pattern: "1$m - P - 1$M - P - 1NT - P - 2$M - P - ?"
    rules:
      - id: o2mp_raise_$m$M
        call: 3$M
        priority: 52
        requires:
          suits: { $M: [3, 13] }
          evals: { total_points: [14, 40] }
        shows: "a maximum 1NT rebid with real support for the six-card suit: inviting"
        establishes: { forcing: invitational, agreed_suit: $M }
      - id: o2mp_pass_$m$M
        call: P
        priority: 44
        requires: {}
        shows: "responder signed off in his own suit; a 12-14 rebid that already denied support has nothing to add"
        establishes: { forcing: sign_off }
        negative_inference_weight: soft

#== CONTEXT
  - id: opener_over_1NT_rebid_to_play_1H1S
    description: "Opener hears responder's to-play 2S after 1H - 1S - 1NT"
    pattern: "1H - P - 1S - P - 1NT - P - 2S - P - ?"
    rules:
      - id: o2ms_raise_1H1S
        call: 3S
        priority: 52
        requires:
          suits: { S: [3, 13] }
          evals: { total_points: [14, 40] }
        shows: "a maximum 1NT rebid with real spade support: inviting"
        establishes: { forcing: invitational, agreed_suit: S }
      - id: o2ms_pass_1H1S
        call: P
        priority: 44
        requires: {}
        shows: "responder signed off in his own suit; the 1NT rebid has nothing to add"
        establishes: { forcing: sign_off }
        negative_inference_weight: soft

#== CONTEXT
  - id: responder_over_1NT_rebid_raise
    description: "Responder answers opener's maximum raise of his to-play rebid"
    expand: { m: [C, D], M: [H, S] }
    pattern: "1$m - P - 1$M - P - 1NT - P - 2$M - P - 3$M - P - ?"
    rules:
      - id: r2mp_game_$m$M
        call: 4$M
        priority: 50
        requires: { evals: { total_points: [9, 40] } }
        shows: "the top of the to-play rebid opposite a maximum with support: bidding the game"
        establishes: { forcing: sign_off, agreed_suit: $M }
      - id: r2mp_pass_$m$M
        call: P
        priority: 44
        requires: {}
        shows: "the rebid was to play and it still is: three of my suit is high enough"
        establishes: { forcing: sign_off }
        negative_inference_weight: soft

#== CONTEXT
  - id: responder_over_1NT_rebid_raise_1H1S
    description: "Responder answers opener's spade raise after 1H - 1S - 1NT - 2S"
    pattern: "1H - P - 1S - P - 1NT - P - 2S - P - 3S - P - ?"
    rules:
      - id: r2ms_game_1H1S
        call: 4S
        priority: 50
        requires: { evals: { total_points: [9, 40] } }
        shows: "the top of the to-play rebid opposite a maximum with support: bidding the game"
        establishes: { forcing: sign_off, agreed_suit: S }
      - id: r2ms_pass_1H1S
        call: P
        priority: 44
        requires: {}
        shows: "the rebid was to play and it still is: three of my suit is high enough"
        establishes: { forcing: sign_off }
        negative_inference_weight: soft

#== CONTEXT
  - id: opener_over_minor_rebid_preference
    description: "Opener hears responder's to-play 2M after 1m - 1M - 2m"
    expand: { m: [C, D], M: [H, S] }
    pattern: "1$m - P - 1$M - P - 2$m - P - 2$M - P - ?"
    rules:
      - id: omrp_raise_$m$M
        call: 3$M
        priority: 52
        requires:
          suits: { $M: [4, 13] }
          evals: { total_points: [16, 40] }
        shows: "four-card support and a maximum: raising responder's own suit"
        establishes: { forcing: invitational, agreed_suit: $M }
      - id: omrp_pass_$m$M
        call: P
        priority: 44
        requires: {}
        shows: "responder signed off in his own suit with no fit for the rebid minor; the 12-15 rebid has nothing to add"
        establishes: { forcing: sign_off }
        negative_inference_weight: soft

#== CONTEXT
  - id: responder_over_minor_rebid_raise
    description: "Responder answers opener's maximum raise after 1m - 1M - 2m - 2M"
    expand: { m: [C, D], M: [H, S] }
    pattern: "1$m - P - 1$M - P - 2$m - P - 2$M - P - 3$M - P - ?"
    rules:
      - id: rmrp_game_$m$M
        call: 4$M
        priority: 50
        requires: { evals: { total_points: [10, 40] } }
        shows: "the top of the to-play rebid opposite four-card support and a maximum: game"
        establishes: { forcing: sign_off, agreed_suit: $M }
      - id: rmrp_pass_$m$M
        call: P
        priority: 44
        requires: {}
        shows: "the rebid was to play: three of my suit is high enough"
        establishes: { forcing: sign_off }
        negative_inference_weight: soft

#== CONTEXT
  - id: opener_over_competitive_minor_raise
    description: "Opener after partner's competitive raise of my minor in a contested auction"
    # Deliberately does NOT define 2NT: `uc_nt2` is still offered, it simply
    # loses to a fit-1.00 pass at priority 44 instead of winning by default.
    # That is the smallest possible subtraction.
    expand: { m: [C, D] }
    pattern: "1$m - act - 2$m - P - ?"
    rules:
      - id: ocmr_3NT_$m
        call: 3NT
        priority: 54
        requires:
          hcp: [18, 40]
          evals: { weakest_unshown_stopper: [0.9, 9] }
        shows: "18-21 with the unshown suits stopped: game opposite even a competitive raise"
        establishes: { forcing: sign_off }
      - id: ocmr_three_$m
        call: 3$m
        priority: 52
        requires:
          suits: { $m: [6, 13] }
          evals: { total_points: [15, 40] }
        shows: "competing to three of my own six-card minor"
        establishes: { forcing: non_forcing, agreed_suit: $m }
      - id: ocmr_pass_$m
        call: P
        priority: 44
        requires: {}
        shows: "partner's raise was competitive, not constructive: a minimum opening passes"
        establishes: { forcing: sign_off }
        negative_inference_weight: soft

#== CONTEXT
  - id: answer_raise_invitation
    description: "Somebody raised to 2M and partner invited with 3M: the seat that must answer"
    # Anchored on 1$M so the major must have been opened at the one level, and
    # `partner_last_suit` so the invitation must be PARTNER'S - without both,
    # a five-token "... - 2$M - P - 3$M - P - ?" also owned the auctions where
    # the opponents bid 2M and 3M.  `responder_over_game_try` (specificity
    # 1007) still owns the uncontested 1M - 2M - 3M try; this pattern's
    # specificity is 8, above every generic context and below every anchored
    # one, which is exactly the band it should occupy.
    expand: { M: [H, S] }
    pattern: "... - 1$M - P - 2$M - P - 3$M - P - ?"
    rules:
      - id: ari_accept_$M
        call: 4$M
        priority: 55
        when: { partner_last_suit: $M }
        requires:
          suits: { $M: [3, 13] }
          evals: { total_points: [15, 40] }
        shows: "accepting the invitation: a maximum for the raise I already made"
        establishes: { forcing: sign_off, agreed_suit: $M }
      - id: ari_decline_$M
        call: P
        priority: 44
        when: { partner_last_suit: $M }
        requires: {}
        shows: "declining: the raise to two already described this hand"
        establishes: { forcing: sign_off }
        negative_inference_weight: soft
