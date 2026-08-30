# =============================================================================
# batch2_support.spec - SUPPORT DOUBLES AND REDOUBLES, AND THE SEAT THAT
# ANSWERS THEM.  Round 18, system editor batch 2.
#
# The agreement in one sentence: after ANY one-of-a-suit opening in which
# partner responds a new major at the one level, a double or redouble of that
# response by opener shows EXACTLY three-card support - and responder, who now
# knows the trump count, answers it in a ladder of his own instead of reading
# it as a takeout double to be pulled.
#
# Structure.  Nothing here edits an existing context header.  The five
# auctions (1C/1D/1H openings x the major responder can bid at the one level)
# are carried by two WIDE contexts whose patterns tie with `support_double`
# and `support_redouble` on specificity (1000 + 5 tokens) and lose the tie by
# file order, so in the four minor auctions the existing contexts keep every
# call they already define and the wide context only ADDS calls they never
# defined.  In the fifth auction (1H - P - 1S) and in every auction where LHO
# competed, the wide context is the only specific interpreter.  That is the
# superset property, obtained structurally.
#
# Motivating boards: 966 and 754 (the missing major twin - both reviewers,
# independently, same two boards); 266 (responder pulls his own side's support
# double to two of his six-card suit); 774 (the support redouble has no
# answering seat at all); 23 and 991 (`redouble_continuations` has no notrump
# rung and no major-opening twin, `rdc_pass_D` = -6.75/table); 13 (the forcing
# pass of `rdc_pass_$m` is answered by nobody).
# =============================================================================

#== RULES general_pull_or_sit
      # Board 266.  `general_pull_or_sit` answers EVERY double of ours that
      # stands, including the four support doubles the file has been making
      # for several rounds, and `adx_pull_my_$M` (59/60) reads them as takeout
      # doubles to be pulled: six trumps opposite the three partner promised
      # crawled to 2H.  The five support-double auctions are taken over by
      # `support_double_answer` below; this rung is the same agreement for
      # every OTHER auction in which partner's double stands in a suit we have
      # both bid (a raise, then their bid, then partner's double).
      # `general_pull_or_sit` carries no `expand:`, so the two rungs are
      # written out - a `$M` here would be a literal.
      # Denominator: `adx_pull_my_H` -2.20 over 5 tables, `adx_pull_my_*`
      # -3.00 over 15; `adx_sit` +0.15 over 27 and it is ABOVE these at 61,
      # so the trump-stack sit is untouched.
      - id: adx_pull_game_H
        call: 4H
        priority: 63
        when: { my_suit: H, partner_suit: H }
        requires:
          suits: { H: [6, 13] }
          evals: { "lott_total_trumps(H)": [9, 26], total_points: [10, 40] }
        shows: "partner's double supported my own suit: six trumps opposite three is a nine-card fit, so the pull is to game"
        establishes: { forcing: sign_off, agreed_suit: H }
      - id: adx_pull_game_S
        call: 4S
        priority: 63
        when: { my_suit: S, partner_suit: S }
        requires:
          suits: { S: [6, 13] }
          evals: { "lott_total_trumps(S)": [9, 26], total_points: [10, 40] }
        shows: "partner's double supported my own suit: six trumps opposite three is a nine-card fit, so the pull is to game"
        establishes: { forcing: sign_off, agreed_suit: S }

#== RULES redouble_continuations
      # Boards 23 and 991.  This context has X, 1H, 1S and a `requires: {}`
      # forcing pass and NOTHING ELSE - no notrump rung at any level and no
      # natural bid once they run past the one level.  `rdc_pass_$m` runs
      # -6.75 IMPs a table over four tables, the worst rate measured in the
      # round, and it is a floor at fit 1.00, so every hand the ladder does
      # not describe lands on it.  Four rungs close the two holes.
      #
      # The four are mutually exclusive with each other by legality: 1NT is
      # only legal over a ONE-level runout, and over a one-level runout the
      # cheapest heart/spade bid is at the one level, so `cheapest_in_suit`
      # switches the two-level major rungs off.  Nothing here can outrank
      # `rdc_X_$m` (57), `rdc_suit_H_$m` (56) or `rdc_suit_S_$m` (55).
      - id: rdc_1NT_$m
        call: 1NT
        priority: 54
        requires:
          hcp: [12, 15]
          evals: { semi_balanced: [1, 1], standing_suit_length: [0, 2] }
        shows: "natural 1NT: a balanced minimum short in the suit they ran to, the redouble owning the auction"
        establishes: { forcing: non_forcing }
      - id: rdc_2NT_$m
        call: 2NT
        priority: 53
        requires:
          hcp: [16, 18]
          evals: { semi_balanced: [1, 1], standing_suit_length: [0, 2] }
        shows: "natural 2NT: 16-18 balanced, short in the suit they ran to"
        establishes: { forcing: non_forcing }
      # Board 13: once they run to two of a minor the one-level major rungs
      # are illegal and the forcing pass nobody answers is all that is left.
      # `suit_quality` keeps a ragged four-bagger out - the suit has to be
      # worth playing opposite a redouble that promised 10+.
      - id: rdc_2H_$m
        call: 2H
        priority: 51
        when: { unbid_suit: H, cheapest_in_suit: true }
        requires:
          suits: { H: [4, 13] }
          hcp: [12, 40]
          evals: { "suit_quality(H)": [2, 9] }
        shows: "natural at the two level over their runout: a real four-card major and opening values"
        establishes: { forcing: non_forcing }
      - id: rdc_2S_$m
        call: 2S
        priority: 51
        when: { unbid_suit: S, cheapest_in_suit: true }
        requires:
          suits: { S: [4, 13] }
          hcp: [12, 40]
          evals: { "suit_quality(S)": [2, 9] }
        shows: "natural at the two level over their runout: a real four-card major and opening values"
        establishes: { forcing: non_forcing }

#== CONTEXT
  # ---------------------------------------------------------------------------
  # 1.  THE ASK, everywhere it belongs (boards 966, 166).
  #
  # `support_double` is `pattern: "1$m - P - 1$M - bid<2$M - ?"` over the four
  # (minor, major) pairs, so after 1H - P - 1S - (2D) opener holding exactly
  # three spades has no support call and `cl_pass` takes the seat at fit 1.00,
  # and after 1C - (1D) - 1H - (1S) the convention is switched off because
  # LHO spoke.  This context is the same convention with `$O` over the three
  # openings that can be followed by a one-level major response and `*` over
  # LHO's call.  Five tokens, so it TIES with `support_double` and sorts after
  # it: in the four clean minor auctions `sd_double`, `sd_raise`,
  # `sd_rebid_2$m`, `sd_1NT`, `sd_2NT` and `sd_pass` keep their calls and only
  # the calls they never defined (1S, 3$M, 4$M) are added.
  # ---------------------------------------------------------------------------
  - id: support_double_wide
    description: "Support double after any 1-bid and a one-level major response, LHO having passed or acted"
    expand_pairs:
      - { O: 1C, s: C, M: H }
      - { O: 1C, s: C, M: S }
      - { O: 1D, s: D, M: H }
      - { O: 1D, s: D, M: S }
      - { O: 1H, s: H, M: S }
    pattern: "$O - * - 1$M - bid<2$M - ?"
    rules:
      - id: sdw_double_$O$M
        call: X
        priority: 85
        requires: { suits: { $M: [3, 3] }, hcp: [12, 21] }
        shows: "support double: exactly 3-card $M support, any strength"
        establishes: { forcing: one_round }
        alertable: true
        convention: support_double
      # With the double reserved for exactly three, the direct raise PROMISES
      # four - that negative inference is the whole convention, and it is why
      # the raise ladder belongs in this context rather than in the generic
      # competitive one, whose 2$M/3$M rungs estimate a fit this seat knows.
      - id: sdw_raise_$O$M
        call: 2$M
        priority: 80
        requires: { suits: { $M: [4, 13] }, evals: { total_points: [12, 15] } }
        shows: "raise: 4+ $M support, minimum (the support double would show exactly three)"
        establishes: { forcing: non_forcing, agreed_suit: $M }
      - id: sdw_jump_$O$M
        call: 3$M
        priority: 79
        requires: { suits: { $M: [4, 13] }, evals: { total_points: [16, 18] } }
        shows: "jump raise: 4+ $M support and extras, inviting game over their bid"
        establishes: { forcing: invitational, agreed_suit: $M }
      - id: sdw_game_$O$M
        call: 4$M
        priority: 78
        requires: { suits: { $M: [4, 13] }, evals: { total_points: [19, 40] } }
        shows: "4+ $M support and enough for game opposite a response"
        establishes: { forcing: sign_off, agreed_suit: $M }
      # Board 730's agreement on the double side: their overcall does not stop
      # opener showing his own four-card major at the one level.  Inert in the
      # M = S rows (spades are partner's suit) and whenever they overcalled in
      # spades, both by `unbid_suit`.
      - id: sdw_1S_$O$M
        call: 1S
        priority: 70
        when: { unbid_suit: S, cheapest_in_suit: true }
        requires:
          suits: { S: [4, 13] }
          evals: { total_points: [10, 19] }
          not: { suits: { $M: [3, 13] } }
        shows: "four+ spades at the one level: their bid does not stop opener showing his own major"
        establishes: { forcing: one_round }
      - id: sdw_rebid_$O$M
        call: 2$s
        priority: 55
        requires:
          suits: { $s: [6, 13] }
          hcp: [12, 15]
          not: { suits: { $M: [3, 13] } }
        shows: "6+ $s, minimum, fewer than 3 $M"
        establishes: { forcing: non_forcing }
      - id: sdw_1NT_$O$M
        call: 1NT
        priority: 54
        requires:
          hcp: [12, 14]
          balanced: true
          features: [ "stopper(their)" ]
          not: { suits: { $M: [3, 13] } }
        shows: "12-14 balanced with a stopper, fewer than 3 $M"
        establishes: { forcing: non_forcing }
      - id: sdw_2NT_$O$M
        call: 2NT
        priority: 53
        requires:
          hcp: [15, 18]
          evals: { semi_balanced: [1, 1] }
          features: [ "stopper(their)" ]
          not: { suits: { $M: [3, 13] } }
        shows: "15-18 balanced with a stopper, fewer than 3 $M"
        establishes: { forcing: non_forcing }
      # THE FLOOR.  `requires: {}` at the bottom of the ladder: this context is
      # the most specific interpreter for P in these auctions, so without it a
      # minimum with a doubleton in partner's major would have no pass at all.
      - id: sdw_pass_$O$M
        call: P
        priority: 15
        requires: {}
        shows: "minimum with no support, no stopper and no rebid: pass"
        establishes: { forcing: non_forcing }
        negative_inference_weight: soft

#== CONTEXT
  # ---------------------------------------------------------------------------
  # 2.  THE REDOUBLE, everywhere it belongs (board 754).
  #
  # `support_redouble` is `1$m - P - 1$M - X - ?`, minor-only and LHO-silent.
  # Same construction as above: five tokens, ties with it, sorts after it, so
  # `srd_redouble` / `srd_raise` / `srd_pass` keep XX, 2$M and P in the four
  # clean minor auctions and this context supplies them everywhere else, plus
  # the calls that family never had at all (1S, 1NT, 2NT, 3$M, 4$M, the
  # six-card rebid).  Denominator: `srd_redouble` runs -3.33 over 3 tables,
  # which is why the twin ships only WITH the answering context below.
  # ---------------------------------------------------------------------------
  - id: support_redouble_wide
    description: "Support redouble after RHO doubles a one-level major response to any 1-bid"
    expand_pairs:
      - { O: 1C, s: C, M: H }
      - { O: 1C, s: C, M: S }
      - { O: 1D, s: D, M: H }
      - { O: 1D, s: D, M: S }
      - { O: 1H, s: H, M: S }
    pattern: "$O - * - 1$M - X - ?"
    rules:
      - id: srw_redouble_$O$M
        call: XX
        priority: 85
        requires: { suits: { $M: [3, 3] }, hcp: [12, 21] }
        shows: "support redouble: exactly 3-card $M support"
        establishes: { forcing: one_round }
        alertable: true
        convention: support_redouble
      - id: srw_raise_$O$M
        call: 2$M
        priority: 80
        requires: { suits: { $M: [4, 13] }, evals: { total_points: [12, 15] } }
        shows: "raise: 4+ $M support, minimum (the support redouble would show exactly three)"
        establishes: { forcing: non_forcing, agreed_suit: $M }
      - id: srw_jump_$O$M
        call: 3$M
        priority: 79
        requires: { suits: { $M: [4, 13] }, evals: { total_points: [16, 18] } }
        shows: "jump raise: 4+ $M support and extras, inviting game over their double"
        establishes: { forcing: invitational, agreed_suit: $M }
      - id: srw_game_$O$M
        call: 4$M
        priority: 78
        requires: { suits: { $M: [4, 13] }, evals: { total_points: [19, 40] } }
        shows: "4+ $M support and enough for game opposite a response"
        establishes: { forcing: sign_off, agreed_suit: $M }
      # Board 730 exactly: `Q742..AKJT62.T53` rebid 2D over the double holding
      # four spades and a void in partner's hearts, because this seat offered
      # only XX, a raise and a pass.
      - id: srw_1S_$O$M
        call: 1S
        priority: 70
        when: { unbid_suit: S, cheapest_in_suit: true }
        requires:
          suits: { S: [4, 13] }
          evals: { total_points: [10, 19] }
          not: { suits: { $M: [3, 13] } }
        shows: "four+ spades at the one level: the double does not stop opener showing his own major"
        establishes: { forcing: one_round }
      - id: srw_rebid_$O$M
        call: 2$s
        priority: 55
        requires:
          suits: { $s: [6, 13] }
          hcp: [12, 15]
          not: { suits: { $M: [3, 13] } }
        shows: "6+ $s, minimum, fewer than 3 $M"
        establishes: { forcing: non_forcing }
      # No stopper clause: they have doubled, not bid, so there is no suit to
      # stop.  This is the notrump rung the whole support-redouble family was
      # missing - the same hole `redouble_continuations` has.
      - id: srw_1NT_$O$M
        call: 1NT
        priority: 54
        requires:
          hcp: [12, 14]
          balanced: true
          not: { suits: { $M: [3, 13] } }
        shows: "12-14 balanced, fewer than 3 $M: the natural notrump rebid survives the double"
        establishes: { forcing: non_forcing }
      - id: srw_2NT_$O$M
        call: 2NT
        priority: 53
        requires:
          hcp: [18, 21]
          evals: { semi_balanced: [1, 1] }
          not: { suits: { $M: [3, 13] } }
        shows: "18-19 balanced, fewer than 3 $M"
        establishes: { forcing: non_forcing }
      - id: srw_pass_$O$M
        call: P
        priority: 15
        requires: {}
        shows: "minimum with no support and no rebid: pass"
        establishes: { forcing: non_forcing }
        negative_inference_weight: soft

#== CONTEXT
  # ---------------------------------------------------------------------------
  # 3.  THE ANSWERING SEAT FOR THE SUPPORT DOUBLE - the part that makes the
  #     ask worth anything (boards 966, 266).
  #
  # Traced before this context: `1D - P - 1S - 2C - X - P - ?` lands in
  # `general_pull_or_sit`, and `adx_pull_my_S` at fit 1.000 / prio 60 PULLS our
  # own support double.  `sd_double` is +0.20 over 5 tables; the six
  # `adx_pull_my_*` rungs that answer it are -3.00 over 15.  That gap is the
  # finding of the round, and it applies to the four minor auctions that have
  # shipped for rounds as much as to the new major one.
  #
  # Seven tokens, specificity 1007, so it owns 2$M / 3$M / 4$M / P / 2NT at
  # exactly the nodes where partner's double showed exactly three trumps.  The
  # `*` in the sixth token covers RHO passing AND RHO bidding again.
  # Every rung counts MY OWN length, never `lott_total_trumps`: partner's
  # shown minimum is an inference produced by the very rule being installed,
  # and a gate that needs its own rule to be satisfiable is the round-8 trap.
  # ---------------------------------------------------------------------------
  - id: support_double_answer
    description: "Responder answers opener's support double: exactly three-card support is known"
    expand_pairs:
      - { O: 1C, M: H }
      - { O: 1C, M: S }
      - { O: 1D, M: H }
      - { O: 1D, M: S }
      - { O: 1H, M: S }
    pattern: "$O - * - 1$M - bid<2$M - X - * - ?"
    rules:
      # Six of mine opposite the three he promised is a nine-card fit and ten
      # tricks - board 266, where we crawled to 2H and got there two rounds
      # late.
      - id: sda_game6_$O$M
        call: 4$M
        priority: 66
        requires: { suits: { $M: [6, 13] }, evals: { total_points: [10, 40] } }
        shows: "the support double marked a nine-card fit: six trumps and 10+ points is a game"
        establishes: { forcing: sign_off, agreed_suit: $M }
      - id: sda_game5_$O$M
        call: 4$M
        priority: 65
        requires: { suits: { $M: [5, 13] }, evals: { total_points: [13, 40] } }
        shows: "an eight-card fit and the values for game"
        establishes: { forcing: sign_off, agreed_suit: $M }
      - id: sda_law3_$O$M
        call: 3$M
        priority: 64
        requires: { suits: { $M: [6, 13] }, evals: { total_points: [6, 9] } }
        shows: "nine trumps between us and no game values: the Law says three"
        establishes: { forcing: non_forcing, agreed_suit: $M }
      - id: sda_inv3_$O$M
        call: 3$M
        priority: 63
        requires: { suits: { $M: [5, 13] }, evals: { total_points: [10, 12] } }
        shows: "an eight-card fit and invitational values"
        establishes: { forcing: invitational, agreed_suit: $M }
      - id: sda_two_$O$M
        call: 2$M
        priority: 62
        requires: { suits: { $M: [5, 13] }, evals: { total_points: [6, 9] } }
        shows: "an eight-card fit is now known: competing to the two level"
        establishes: { forcing: non_forcing, agreed_suit: $M }
      # The sit.  `adx_sit` (61) is the rung this context covers away, so it is
      # reproduced here at its own priority, in the currency that is safe in a
      # competed auction: `standing_suit_length` is the suit of the standing
      # bid, where `suit_quality(their)` would resolve to LHO's suit.
      - id: sda_sit_$O$M
        call: P
        priority: 61
        requires: { evals: { standing_suit_length: [4, 13], total_points: [6, 40] } }
        shows: "four of their trumps behind the bidder: partner's double is left in"
        establishes: { forcing: sign_off }
      # THE DISCRIMINATING PASS, and the reason the convention pays.  Opener
      # promised exactly three, so with exactly four of my own the fit is 4-3:
      # defending partner's double beats declaring a seven-card fit at the two
      # level.  It has to be a gated rule rather than the floor, because
      # `sd_double` is `forcing: one_round` and the decision layer drops a
      # `requires: {}` pass under a live one-round force.
      - id: sda_defend_$O$M
        call: P
        priority: 59
        requires: { suits: { $M: [4, 4] }, evals: { total_points: [0, 8] } }
        shows: "only a 4-3 fit opposite the promised three and no extras: partner's double stands"
        establishes: { forcing: sign_off }
      - id: sda_nt2_$O$M
        call: 2NT
        priority: 58
        requires:
          hcp: [9, 12]
          evals: { semi_balanced: [1, 1] }
          features: [ "stopper(their)" ]
        shows: "natural answer to the double: 9-12 balanced with their suit stopped"
        establishes: { forcing: non_forcing }
      - id: sda_floor_$O$M
        call: P
        priority: 40
        requires: {}
        shows: "nothing to add over partner's double"
        establishes: { forcing: sign_off }
        negative_inference_weight: soft

#== CONTEXT
  # ---------------------------------------------------------------------------
  # 4.  THE ANSWERING SEAT FOR THE SUPPORT REDOUBLE (board 774).
  #
  # `srw_redouble` / `srd_redouble` are `forcing: one_round` and there is no
  # context anywhere for `1$m - P - 1$M - X - XX - ?`; the seat falls to
  # `general_uncontested_continuation`, whose only fitting rung on a six-count
  # is `uc_pass` at fit 1.00.  Same ladder as the double's answer, minus the
  # two rungs that need a suit of theirs to exist (the sit and the 2NT with a
  # stopper): they doubled, they did not bid.
  # ---------------------------------------------------------------------------
  - id: support_redouble_answer
    description: "Responder answers opener's support redouble: exactly three-card support is known"
    expand_pairs:
      - { O: 1C, M: H }
      - { O: 1C, M: S }
      - { O: 1D, M: H }
      - { O: 1D, M: S }
      - { O: 1H, M: S }
    pattern: "$O - * - 1$M - X - XX - * - ?"
    rules:
      - id: sra_game6_$O$M
        call: 4$M
        priority: 66
        requires: { suits: { $M: [6, 13] }, evals: { total_points: [10, 40] } }
        shows: "the support redouble marked a nine-card fit: six trumps and 10+ points is a game"
        establishes: { forcing: sign_off, agreed_suit: $M }
      - id: sra_game5_$O$M
        call: 4$M
        priority: 65
        requires: { suits: { $M: [5, 13] }, evals: { total_points: [13, 40] } }
        shows: "an eight-card fit and the values for game"
        establishes: { forcing: sign_off, agreed_suit: $M }
      - id: sra_law3_$O$M
        call: 3$M
        priority: 64
        requires: { suits: { $M: [6, 13] }, evals: { total_points: [6, 9] } }
        shows: "nine trumps between us and no game values: the Law says three"
        establishes: { forcing: non_forcing, agreed_suit: $M }
      - id: sra_inv3_$O$M
        call: 3$M
        priority: 63
        requires: { suits: { $M: [5, 13] }, evals: { total_points: [10, 12] } }
        shows: "five-card major and invitational values opposite the three-card raise"
        establishes: { forcing: invitational, agreed_suit: $M }
      - id: sra_two_$O$M
        call: 2$M
        priority: 62
        requires: { suits: { $M: [5, 13] }, evals: { total_points: [6, 10] } }
        shows: "five-card major opposite the promised three: the 5-3 fit at the two level"
        establishes: { forcing: non_forcing, agreed_suit: $M }
      # The discriminating pass again: with exactly four trumps and a minimum
      # the seven-card fit plays at the one level redoubled, and the redouble
      # is a one-round force, so an ungated pass would be dropped by the
      # decision layer and this seat would have to invent a bid.
      - id: sra_sit_$O$M
        call: P
        priority: 59
        requires: { suits: { $M: [4, 4] }, evals: { total_points: [6, 9] } }
        shows: "only four in the major and no extras: the redouble stands and we play here"
        establishes: { forcing: sign_off }
      # The 10-12 balanced hand with only four trumps: 1$M redoubled is a
      # seven-card fit and the invitation has to be made somewhere.  There is
      # no stopper clause because they doubled rather than bid.
      - id: sra_nt2_$O$M
        call: 2NT
        priority: 58
        requires: { hcp: [10, 12], evals: { semi_balanced: [1, 1] } }
        shows: "10-12 balanced with only four in the major: inviting rather than playing the seven-card fit"
        establishes: { forcing: invitational }
      - id: sra_floor_$O$M
        call: P
        priority: 40
        requires: {}
        shows: "nothing to add over partner's redouble"
        establishes: { forcing: sign_off }
        negative_inference_weight: soft

#== CONTEXT
  # ---------------------------------------------------------------------------
  # 5.  The seat that answers `sda_inv3_$O$M` - responder's invitational raise
  #     opposite the promised three.  Nine tokens; the two `*`s let the
  #     opponents keep bidding without losing opener the seat.
  # ---------------------------------------------------------------------------
  - id: support_double_answer_invite
    description: "Opener answers responder's invitational raise after the support double"
    expand_pairs:
      - { O: 1C, M: H }
      - { O: 1C, M: S }
      - { O: 1D, M: H }
      - { O: 1D, M: S }
      - { O: 1H, M: S }
    pattern: "$O - * - 1$M - bid<2$M - X - * - 3$M - * - ?"
    rules:
      - id: sdai_game_$O$M
        call: 4$M
        priority: 62
        requires: { evals: { total_points: [15, 40] } }
        shows: "accepting: more than a minimum opposite the invitation, with three known trumps"
        establishes: { forcing: sign_off, agreed_suit: $M }
      - id: sdai_pass_$O$M
        call: P
        priority: 40
        requires: {}
        shows: "declining: a minimum opening with only three-card support"
        establishes: { forcing: sign_off, agreed_suit: $M }
        negative_inference_weight: soft

#== CONTEXT
  # ---------------------------------------------------------------------------
  # 6.  The same answer on the redouble side (`sra_inv3_$O$M`).
  # ---------------------------------------------------------------------------
  - id: support_redouble_answer_invite
    description: "Opener answers responder's invitational raise after the support redouble"
    expand_pairs:
      - { O: 1C, M: H }
      - { O: 1C, M: S }
      - { O: 1D, M: H }
      - { O: 1D, M: S }
      - { O: 1H, M: S }
    pattern: "$O - * - 1$M - X - XX - * - 3$M - * - ?"
    rules:
      - id: srai_game_$O$M
        call: 4$M
        priority: 62
        requires: { evals: { total_points: [15, 40] } }
        shows: "accepting: more than a minimum opposite the invitation, with three known trumps"
        establishes: { forcing: sign_off, agreed_suit: $M }
      - id: srai_pass_$O$M
        call: P
        priority: 40
        requires: {}
        shows: "declining: a minimum opening with only three-card support"
        establishes: { forcing: sign_off, agreed_suit: $M }
        negative_inference_weight: soft

#== CONTEXT
  # ---------------------------------------------------------------------------
  # 7.  The seat that answers `sdw_jump_$O$M` - opener's invitational jump
  #     raise with FOUR-card support over their bid.  Responder has already
  #     shown 6+ and a four-card major; opposite 16-18 he needs about nine.
  # ---------------------------------------------------------------------------
  - id: support_double_jump_answer
    description: "Responder answers opener's invitational jump raise in the competitive one-level auction"
    expand_pairs:
      - { O: 1C, M: H }
      - { O: 1C, M: S }
      - { O: 1D, M: H }
      - { O: 1D, M: S }
      - { O: 1H, M: S }
    pattern: "$O - * - 1$M - bid<2$M - 3$M - * - ?"
    rules:
      - id: sdja_game_$O$M
        call: 4$M
        priority: 62
        requires: { evals: { total_points: [9, 40] } }
        shows: "accepting the jump raise: nine-plus points opposite four trumps and extras"
        establishes: { forcing: sign_off, agreed_suit: $M }
      - id: sdja_pass_$O$M
        call: P
        priority: 40
        requires: {}
        shows: "declining the jump raise: a minimum response"
        establishes: { forcing: sign_off, agreed_suit: $M }
        negative_inference_weight: soft

#== CONTEXT
  # ---------------------------------------------------------------------------
  # 8.  The same answer on the redouble side (`srw_jump_$O$M`).
  # ---------------------------------------------------------------------------
  - id: support_redouble_jump_answer
    description: "Responder answers opener's invitational jump raise after their double"
    expand_pairs:
      - { O: 1C, M: H }
      - { O: 1C, M: S }
      - { O: 1D, M: H }
      - { O: 1D, M: S }
      - { O: 1H, M: S }
    pattern: "$O - * - 1$M - X - 3$M - * - ?"
    rules:
      - id: srja_game_$O$M
        call: 4$M
        priority: 62
        requires: { evals: { total_points: [9, 40] } }
        shows: "accepting the jump raise: nine-plus points opposite four trumps and extras"
        establishes: { forcing: sign_off, agreed_suit: $M }
      - id: srja_pass_$O$M
        call: P
        priority: 40
        requires: {}
        shows: "declining the jump raise: a minimum response"
        establishes: { forcing: sign_off, agreed_suit: $M }
        negative_inference_weight: soft

#== CONTEXT
  # ---------------------------------------------------------------------------
  # 9.  `redouble_continuations` FOR THE MAJOR OPENINGS (board 991).
  #
  # `redouble_continuations` is `expand: { m: [C, D] }`: after 1H - (X) - XX -
  # (2D) the whole family is dark and `cl_pass` takes the seat - N passed a
  # 17-count with four spades.  A structural clone, one context over the two
  # majors, with the notrump rungs board 23 showed the minor family needed and
  # the same `requires: {}` forcing pass at the bottom.  `$oM` is the other
  # major, so one rung serves 2S over 1H and 2H over 1S.
  # ---------------------------------------------------------------------------
  - id: redouble_continuations_major
    description: "Opener after 1M - (X) - XX - (their runout)"
    expand_pairs:
      - { O: 1H, M: H }
      - { O: 1S, M: S }
    pattern: "$O - X - XX - bid - ?"
    rules:
      - id: rdcm_X_$M
        call: X
        priority: 57
        requires: { hcp: [12, 40], evals: { standing_suit_length: [3, 13] } }
        shows: "penalty: partner showed 10+, we own this hand"
        establishes: { forcing: non_forcing }
      - id: rdcm_second_$M
        call: 2$oM
        priority: 56
        when: { unbid_suit: $oM, cheapest_in_suit: true }
        requires: { suits: { $oM: [4, 13] } }
        shows: "natural second suit: the redouble keeps the auction ours"
        establishes: { forcing: non_forcing }
      - id: rdcm_3C_$M
        call: 3C
        priority: 55
        when: { unbid_suit: C, cheapest_in_suit: true }
        requires: { suits: { C: [5, 13] } }
        shows: "natural second suit at the three level: 5+ clubs"
        establishes: { forcing: non_forcing }
      - id: rdcm_3D_$M
        call: 3D
        priority: 55
        when: { unbid_suit: D, cheapest_in_suit: true }
        requires: { suits: { D: [5, 13] } }
        shows: "natural second suit at the three level: 5+ diamonds"
        establishes: { forcing: non_forcing }
      - id: rdcm_rebid_$M
        call: 2$M
        priority: 54
        when: { cheapest_in_suit: true }
        requires: { suits: { $M: [6, 13] } }
        shows: "rebidding my six-card major"
        establishes: { forcing: non_forcing, agreed_suit: $M }
      - id: rdcm_1NT_$M
        call: 1NT
        priority: 53.5
        requires:
          hcp: [12, 15]
          evals: { semi_balanced: [1, 1], standing_suit_length: [0, 2] }
        shows: "natural 1NT: a balanced minimum short in the suit they ran to"
        establishes: { forcing: non_forcing }
      - id: rdcm_2NT_$M
        call: 2NT
        priority: 53
        requires:
          hcp: [16, 18]
          evals: { semi_balanced: [1, 1], standing_suit_length: [0, 2] }
        shows: "natural 2NT: 16-18 balanced, short in the suit they ran to"
        establishes: { forcing: non_forcing }
      - id: rdcm_pass_$M
        call: P
        priority: 50
        requires: {}
        shows: "forcing pass: partner's redouble owns the auction"
        establishes: { forcing: one_round }

#== CONTEXT
  # ---------------------------------------------------------------------------
  # 10.  THE SEAT THAT ANSWERS THE FORCING PASS (board 13).
  #
  # `rdc_pass_$m` and the new `rdcm_pass_$M` are `forcing: one_round` and the
  # redoubler's own next turn has no context: `general_balancing_low` takes it
  # and `ballow_pass` fits 1.00, so the "forcing" pass was passed out at the
  # table - 2C undoubled for +300 with 4S cold.  This is the seat, over all
  # four openings.  The suit rungs are deliberately `non_forcing`: a one-round
  # force here would owe a further seat, and the whole point of this batch is
  # that a force without an answer is worse than no force.
  # ---------------------------------------------------------------------------
  - id: redoubler_over_runout
    description: "The redoubler answers opener's forcing pass over their runout"
    expand: { O: [1C, 1D, 1H, 1S] }
    pattern: "$O - X - XX - bid - P - P - ?"
    rules:
      - id: rdro_X_$O
        call: X
        priority: 62
        requires: { hcp: [9, 40], evals: { standing_suit_length: [4, 13] } }
        shows: "penalty double: four-plus of their runout suit behind the runner, opposite a forcing pass"
        establishes: { forcing: non_forcing }
      - id: rdro_2H_$O
        call: 2H
        priority: 56
        when: { unbid_suit: H, cheapest_in_suit: true }
        requires: { suits: { H: [5, 13] }, hcp: [9, 40] }
        shows: "five-card heart suit: naming our fit rather than defending"
        establishes: { forcing: non_forcing }
      - id: rdro_2S_$O
        call: 2S
        priority: 55
        when: { unbid_suit: S, cheapest_in_suit: true }
        requires: { suits: { S: [5, 13] }, hcp: [9, 40] }
        shows: "five-card spade suit: naming our fit rather than defending"
        establishes: { forcing: non_forcing }
      - id: rdro_pass_$O
        call: P
        priority: 20
        requires: {}
        shows: "no penalty and no suit: letting them play it undoubled"
        establishes: { forcing: non_forcing }
        negative_inference_weight: soft
