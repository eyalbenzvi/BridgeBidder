#== RULES general_competitive_low
      # ---------------------------------------------------------------
      # FAMILY 4 - the reopening double.  `general_balancing_low` has
      # `ballow_reopen_X` (+3.75 over 4 tables) and this context has no twin.
      # Both carry `i_have_acted: true`, which makes them disjoint from
      # `cl_negative_X1`/`X2` (both `i_have_acted: false`) - the negative
      # double is a measured winner and nothing here may reach it.
      # ---------------------------------------------------------------
      - id: cl_raise_pref_H2
        call: 2H
        priority: 33.4
        when: { partner_suit: H, cheapest_in_suit: true, side_has_acted: true,
                i_have_acted: false, standing_bid_level: [2], we_hold_contract: false }
        requires:
          suits: { H: [3, 13] }
          evals: { total_points: [6, 12], partner_shown_max: [0, 18], "lott_total_trumps(H)": [8, 9] }
        shows: "raising partner's overcalled hearts with three-card support: a known eight-card fit beats a responsive double that denies a fit"
        establishes: { forcing: non_forcing, agreed_suit: H }
      - id: cl_raise_pref_S2
        call: 2S
        priority: 33.4
        when: { partner_suit: S, cheapest_in_suit: true, side_has_acted: true,
                i_have_acted: false, standing_bid_level: [2], we_hold_contract: false }
        requires:
          suits: { S: [3, 13] }
          evals: { total_points: [6, 12], partner_shown_max: [0, 18], "lott_total_trumps(S)": [8, 9] }
        shows: "raising partner's overcalled spades with three-card support: a known eight-card fit beats a responsive double that denies a fit"
        establishes: { forcing: non_forcing, agreed_suit: S }
      - id: cl_raise_overcall_C
        call: 2C
        priority: 33.2
        when: { partner_suit: C, cheapest_in_suit: true, side_has_acted: true,
                i_have_acted: false, we_hold_contract: false }
        requires:
          suits: { C: [4, 13] }
          evals: { "partner_shown_length(C)": [5, 13], "lott_total_trumps(C)": [8, 9], total_points: [8, 12] }
        shows: "raise of partner's OVERCALL on four-card support: nine trumps in a suit he has already named beats a double asking him to name another"
        establishes: { forcing: non_forcing, agreed_suit: C }
      - id: cl_raise_overcall_D
        call: 2D
        priority: 33.2
        when: { partner_suit: D, cheapest_in_suit: true, side_has_acted: true,
                i_have_acted: false, we_hold_contract: false }
        requires:
          suits: { D: [4, 13] }
          evals: { "partner_shown_length(D)": [5, 13], "lott_total_trumps(D)": [8, 9], total_points: [8, 12] }
        shows: "raise of partner's OVERCALL on four-card support: nine trumps in a suit he has already named beats a double asking him to name another"
        establishes: { forcing: non_forcing, agreed_suit: D }
      - id: cl_raise_overcall_H
        call: 2H
        priority: 33.2
        when: { partner_suit: H, cheapest_in_suit: true, side_has_acted: true,
                i_have_acted: false, we_hold_contract: false }
        requires:
          suits: { H: [4, 13] }
          evals: { "partner_shown_length(H)": [5, 13], "lott_total_trumps(H)": [8, 9], total_points: [8, 12] }
        shows: "raise of partner's OVERCALL on four-card support: nine trumps in a suit he has already named beats a double asking him to name another"
        establishes: { forcing: non_forcing, agreed_suit: H }
      - id: cl_raise_overcall_S
        call: 2S
        priority: 33.2
        when: { partner_suit: S, cheapest_in_suit: true, side_has_acted: true,
                i_have_acted: false, we_hold_contract: false }
        requires:
          suits: { S: [4, 13] }
          evals: { "partner_shown_length(S)": [5, 13], "lott_total_trumps(S)": [8, 9], total_points: [8, 12] }
        shows: "raise of partner's OVERCALL on four-card support: nine trumps in a suit he has already named beats a double asking him to name another"
        establishes: { forcing: non_forcing, agreed_suit: S }
      # ---------------------------------------------------------------
      # FAMILY 1 - the Law of Total Tricks in a MINOR.  Nine trumps is the
      # three level, ten is the four level; both priced BELOW `cl_raise_$m3`
      # (31) at the three level so `cl_raise_C3` (+3.50 over 6 tables) keeps
      # every hand it fits.
      # ---------------------------------------------------------------
      - id: cl_raise_lott4_C
        call: 4C
        priority: 31.9
        when: { partner_suit: C, is_competitive: true, we_hold_contract: false }
        requires:
          suits: { C: [4, 13] }
          evals: { "lott_total_trumps(C)": [9, 26], their_fit: [7, 26], total_points: [6, 40] }
        shows: "the Law at the four level in a minor: ten trumps ours and a fit theirs, so the level follows the trumps and not the points"
        establishes: { forcing: non_forcing, agreed_suit: C }
      - id: cl_raise_lott4_D
        call: 4D
        priority: 31.9
        when: { partner_suit: D, is_competitive: true, we_hold_contract: false }
        requires:
          suits: { D: [4, 13] }
          evals: { "lott_total_trumps(D)": [9, 26], their_fit: [7, 26], total_points: [6, 40] }
        shows: "the Law at the four level in a minor: ten trumps ours and a fit theirs, so the level follows the trumps and not the points"
        establishes: { forcing: non_forcing, agreed_suit: D }
      - id: cl_raise_lott3_C
        call: 3C
        priority: 30.5
        when: { partner_suit: C, is_competitive: true, we_hold_contract: false }
        requires:
          suits: { C: [5, 13] }
          evals: { "lott_total_trumps(C)": [8, 26], total_points: [3, 9] }
        shows: "preemptive raise of partner's clubs to the level of our fit: five-card support and no defence - the raise is obstruction, not values"
        establishes: { forcing: non_forcing, agreed_suit: C }
      - id: cl_raise_lott3_D
        call: 3D
        priority: 30.5
        when: { partner_suit: D, is_competitive: true, we_hold_contract: false }
        requires:
          suits: { D: [5, 13] }
          evals: { "lott_total_trumps(D)": [8, 26], total_points: [3, 9] }
        shows: "preemptive raise of partner's diamonds to the level of our fit: five-card support and no defence - the raise is obstruction, not values"
        establishes: { forcing: non_forcing, agreed_suit: D }
      # ---------------------------------------------------------------
      # The Law raise on a DOUBLETON opposite a promised six-card suit.
      # `longest_suit_length: [0, 5]` keeps a six-card suit of my own on
      # its own rung (`cl_new_long3_*`, `cl_rebid_*`).
      # ---------------------------------------------------------------
      - id: cl_raise_lott_short_H
        call: 3H
        priority: 31.6
        when: { partner_suit: H, cheapest_in_suit: true, we_hold_contract: false }
        requires:
          suits: { H: [2, 13] }
          evals: { "partner_shown_length(H)": [6, 13], "lott_total_trumps(H)": [8, 26],
                   total_points: [8, 40], longest_suit_length: [0, 5] }
        shows: "Law raise to three with a doubleton: partner has promised six hearts, so two cards are support"
        establishes: { forcing: non_forcing, agreed_suit: H }
      - id: cl_raise_lott_short_S
        call: 3S
        priority: 31.6
        when: { partner_suit: S, cheapest_in_suit: true, we_hold_contract: false }
        requires:
          suits: { S: [2, 13] }
          evals: { "partner_shown_length(S)": [6, 13], "lott_total_trumps(S)": [8, 26],
                   total_points: [8, 40], longest_suit_length: [0, 5] }
        shows: "Law raise to three with a doubleton: partner has promised six spades, so two cards are support"
        establishes: { forcing: non_forcing, agreed_suit: S }
      # ---------------------------------------------------------------
      # The jump raise on a fit: `cheapest_in_suit: false` makes it a JUMP,
      # which is what the ladder has never had.
      # ---------------------------------------------------------------
      - id: cl_raise_fit3_C
        call: 3C
        priority: 31.5
        when: { partner_suit: C, cheapest_in_suit: false, we_hold_contract: false }
        requires:
          suits: { C: [4, 13] }
          evals: { total_points: [13, 40], "lott_total_trumps(C)": [8, 9] }
        shows: "jump raise on the fit: 13+ support points and nine-plus combined trumps - too good for the cheap raise, and the Law says the three level is safe"
        establishes: { forcing: non_forcing, agreed_suit: C }
      - id: cl_raise_fit3_D
        call: 3D
        priority: 31.5
        when: { partner_suit: D, cheapest_in_suit: false, we_hold_contract: false }
        requires:
          suits: { D: [4, 13] }
          evals: { total_points: [13, 40], "lott_total_trumps(D)": [8, 9] }
        shows: "jump raise on the fit: 13+ support points and nine-plus combined trumps - too good for the cheap raise, and the Law says the three level is safe"
        establishes: { forcing: non_forcing, agreed_suit: D }
      - id: cl_raise_fit3_H
        call: 3H
        priority: 31.5
        when: { partner_suit: H, cheapest_in_suit: false, we_hold_contract: false }
        requires:
          suits: { H: [4, 13] }
          evals: { total_points: [13, 40], "lott_total_trumps(H)": [8, 9] }
        shows: "jump raise on the fit: 13+ support points and nine-plus combined trumps - too good for the cheap raise, and the Law says the three level is safe"
        establishes: { forcing: non_forcing, agreed_suit: H }
      - id: cl_raise_fit3_S
        call: 3S
        priority: 31.5
        when: { partner_suit: S, cheapest_in_suit: false, we_hold_contract: false }
        requires:
          suits: { S: [4, 13] }
          evals: { total_points: [13, 40], "lott_total_trumps(S)": [8, 9] }
        shows: "jump raise on the fit: 13+ support points and nine-plus combined trumps - too good for the cheap raise, and the Law says the three level is safe"
        establishes: { forcing: non_forcing, agreed_suit: S }
      # The Law after partner has AGREED my own suit.
      - id: cl_rebid_agreed_law3_C
        call: 3C
        priority: 31.4
        when: { my_suit: C, partner_suit: C, we_bid_last: false, cheapest_in_suit: true, we_hold_contract: false }
        requires:
          suits: { C: [5, 13] }
          evals: { "lott_total_trumps(C)": [8, 26], total_points: [7, 40] }
        shows: "the Law after partner agreed my clubs: five trumps opposite his three - competing to three is right on shape"
        establishes: { forcing: non_forcing, agreed_suit: C }
      - id: cl_rebid_agreed_law3_D
        call: 3D
        priority: 31.4
        when: { my_suit: D, partner_suit: D, we_bid_last: false, cheapest_in_suit: true, we_hold_contract: false }
        requires:
          suits: { D: [5, 13] }
          evals: { "lott_total_trumps(D)": [8, 26], total_points: [7, 40] }
        shows: "the Law after partner agreed my diamonds: five trumps opposite his three - competing to three is right on shape"
        establishes: { forcing: non_forcing, agreed_suit: D }
      - id: cl_rebid_agreed_law3_H
        call: 3H
        priority: 31.4
        when: { my_suit: H, partner_suit: H, we_bid_last: false, cheapest_in_suit: true, we_hold_contract: false }
        requires:
          suits: { H: [5, 13] }
          evals: { "lott_total_trumps(H)": [8, 26], total_points: [7, 40] }
        shows: "the Law after partner agreed my hearts: five trumps opposite his three - competing to three is right on shape"
        establishes: { forcing: non_forcing, agreed_suit: H }
      - id: cl_rebid_agreed_law3_S
        call: 3S
        priority: 31.4
        when: { my_suit: S, partner_suit: S, we_bid_last: false, cheapest_in_suit: true, we_hold_contract: false }
        requires:
          suits: { S: [5, 13] }
          evals: { "lott_total_trumps(S)": [8, 26], total_points: [7, 40] }
        shows: "the Law after partner agreed my spades: five trumps opposite his three - competing to three is right on shape"
        establishes: { forcing: non_forcing, agreed_suit: S }
      # ---------------------------------------------------------------
      # THE CEILING ON THE COMPETITIVE REBID LADDER.  `cl_rebid_jump_$M`
      # (31) is an INVITATION and there is nothing above it, so a
      # four-loser one-suiter invited and was passed.  This rung is gated
      # at SEVEN cards so it can never reach `cl_rebid_jump_$M`'s six-card
      # population - that rule measures +2.00 and is not to be re-priced.
      # ---------------------------------------------------------------
      - id: cl_rebid_game_H
        call: 4H
        priority: 31.2
        when: { my_suit: H, we_hold_contract: false }
        requires:
          suits: { H: [7, 13] }
          evals: { ltc: [0, 5], total_points: [14, 40], "suit_quality(H)": [1.5, 9] }
        shows: "self-sufficient seven-card heart suit and at most five losers: game on playing strength, not an invitation"
        establishes: { forcing: sign_off, agreed_suit: H }
      - id: cl_rebid_game_S
        call: 4S
        priority: 31.2
        when: { my_suit: S, we_hold_contract: false }
        requires:
          suits: { S: [7, 13] }
          evals: { ltc: [0, 5], total_points: [14, 40], "suit_quality(S)": [1.5, 9] }
        shows: "self-sufficient seven-card spade suit and at most five losers: game on playing strength, not an invitation"
        establishes: { forcing: sign_off, agreed_suit: S }
      # ---------------------------------------------------------------
      # FAMILY 7 - advancing a takeout double is one rung wide.  The
      # answering seat is `general_uncontested_continuation`, which already
      # carries `uc_doubler_raise3_$X` (17-19) and `uc_doubler_game_$M`
      # (20+) over the advance - VERIFIED by tracing `1C X P 2H P ?`.
      # ---------------------------------------------------------------
      - id: cl_jumpadv_H2
        call: 2H
        priority: 30.9
        when: { partner_last_call_was_double: true, unbid_suit: H, cheapest_in_suit: false,
                standing_bid_level: [1], i_have_acted: false, we_hold_contract: false }
        requires:
          suits: { H: [5, 13] }
          evals: { total_points: [9, 12] }
        shows: "jump advance of partner's takeout double: 5+ hearts, 9-12, invitational"
        establishes: { forcing: invitational }
      - id: cl_jumpadv_S2
        call: 2S
        priority: 30.9
        when: { partner_last_call_was_double: true, unbid_suit: S, cheapest_in_suit: false,
                standing_bid_level: [1], i_have_acted: false, we_hold_contract: false }
        requires:
          suits: { S: [5, 13] }
          evals: { total_points: [9, 12] }
        shows: "jump advance of partner's takeout double: 5+ spades, 9-12, invitational"
        establishes: { forcing: invitational }
      - id: cl_adv_H1
        call: 1H
        priority: 30.6
        when: { partner_last_call_was_double: true, unbid_suit: H, cheapest_in_suit: true,
                i_have_acted: false, we_hold_contract: false }
        requires:
          suits: { H: [4, 13] }
          evals: { total_points: [6, 40] }
        shows: "advancing partner's takeout double in a four-card major at the one level: no suit quality needed, the double has promised support"
        establishes: { forcing: non_forcing }
      - id: cl_adv_S1
        call: 1S
        priority: 30.6
        when: { partner_last_call_was_double: true, unbid_suit: S, cheapest_in_suit: true,
                i_have_acted: false, we_hold_contract: false }
        requires:
          suits: { S: [4, 13] }
          evals: { total_points: [6, 40] }
        shows: "advancing partner's takeout double in a four-card major at the one level: no suit quality needed, the double has promised support"
        establishes: { forcing: non_forcing }
      # ---------------------------------------------------------------
      # FAMILY 8 - a five-card major beats notrump, and the suit-quality
      # toll is not charged to a hand that has the values.
      # ---------------------------------------------------------------
      - id: cl_free_major_H2
        call: 2H
        priority: 28.6
        when: { unbid_suit: H, cheapest_in_suit: true, partner_has_acted: true,
                i_have_acted: false, we_hold_contract: false }
        requires:
          suits: { H: [5, 13] }
          hcp: [10, 40]
        shows: "a five-card major at the two level outranks notrump: partner has bid and I still have a major to show"
        establishes: { forcing: non_forcing }
      - id: cl_free_major_S2
        call: 2S
        priority: 28.6
        when: { unbid_suit: S, cheapest_in_suit: true, partner_has_acted: true,
                i_have_acted: false, we_hold_contract: false }
        requires:
          suits: { S: [5, 13] }
          hcp: [10, 40]
        shows: "a five-card major at the two level outranks notrump: partner has bid and I still have a major to show"
        establishes: { forcing: non_forcing }
      - id: cl_free_major3_over_nt_H
        call: 3H
        priority: 28.5
        when: { unbid_suit: H, cheapest_in_suit: true, side_has_acted: true,
                i_have_acted: false, standing_bid_strain: [NT], standing_bid_level: [2],
                we_hold_contract: false }
        requires:
          suits: { H: [5, 13] }
          evals: { total_points: [8, 40] }
        shows: "natural hearts over their two-suited notrump overcall: they have located eleven cards elsewhere, so no extra values and no suit-quality test"
        establishes: { forcing: non_forcing }
      - id: cl_free_major3_over_nt_S
        call: 3S
        priority: 28.5
        when: { unbid_suit: S, cheapest_in_suit: true, side_has_acted: true,
                i_have_acted: false, standing_bid_strain: [NT], standing_bid_level: [2],
                we_hold_contract: false }
        requires:
          suits: { S: [5, 13] }
          evals: { total_points: [8, 40] }
        shows: "natural spades over their two-suited notrump overcall: they have located eleven cards elsewhere, so no extra values and no suit-quality test"
        establishes: { forcing: non_forcing }
      # The rebid of my own FIVE-card suit; `cl_rebid_$X2/3` demand six.
      # Priced BELOW `cl_nt3` (29) deliberately.
      - id: cl_rebid5_two_C
        call: 2C
        priority: 28.4
        when: { my_suit: C, cheapest_in_suit: true, we_hold_contract: false }
        requires:
          suits: { C: [5, 13] }
          evals: { total_points: [11, 40], "suit_quality(C)": [2.5, 9] }
        shows: "rebid of my own five-card clubs at the two level: a suit good enough to play opposite a doubleton, and the values for the level"
        establishes: { forcing: non_forcing }
      - id: cl_rebid5_two_D
        call: 2D
        priority: 28.4
        when: { my_suit: D, cheapest_in_suit: true, we_hold_contract: false }
        requires:
          suits: { D: [5, 13] }
          evals: { total_points: [11, 40], "suit_quality(D)": [2.5, 9] }
        shows: "rebid of my own five-card diamonds at the two level: a suit good enough to play opposite a doubleton, and the values for the level"
        establishes: { forcing: non_forcing }
      - id: cl_rebid5_two_H
        call: 2H
        priority: 28.4
        when: { my_suit: H, cheapest_in_suit: true, we_hold_contract: false }
        requires:
          suits: { H: [5, 13] }
          evals: { total_points: [11, 40], "suit_quality(H)": [2.5, 9] }
        shows: "rebid of my own five-card hearts at the two level: a suit good enough to play opposite a doubleton, and the values for the level"
        establishes: { forcing: non_forcing }
      - id: cl_rebid5_two_S
        call: 2S
        priority: 28.4
        when: { my_suit: S, cheapest_in_suit: true, we_hold_contract: false }
        requires:
          suits: { S: [5, 13] }
          evals: { total_points: [11, 40], "suit_quality(S)": [2.5, 9] }
        shows: "rebid of my own five-card spades at the two level: a suit good enough to play opposite a doubleton, and the values for the level"
        establishes: { forcing: non_forcing }
      - id: cl_rebid5_three_C
        call: 3C
        priority: 28.3
        when: { my_suit: C, cheapest_in_suit: true, we_hold_contract: false }
        requires:
          suits: { C: [5, 13] }
          evals: { total_points: [13, 40], "suit_quality(C)": [2.0, 9] }
        shows: "rebid of my own five-card clubs at the three level: a self-sufficient suit and the values for the level"
        establishes: { forcing: non_forcing }
      - id: cl_rebid5_three_D
        call: 3D
        priority: 28.3
        when: { my_suit: D, cheapest_in_suit: true, we_hold_contract: false }
        requires:
          suits: { D: [5, 13] }
          evals: { total_points: [13, 40], "suit_quality(D)": [2.0, 9] }
        shows: "rebid of my own five-card diamonds at the three level: a self-sufficient suit and the values for the level"
        establishes: { forcing: non_forcing }
      - id: cl_rebid5_three_H
        call: 3H
        priority: 28.3
        when: { my_suit: H, cheapest_in_suit: true, we_hold_contract: false }
        requires:
          suits: { H: [5, 13] }
          evals: { total_points: [13, 40], "suit_quality(H)": [2.0, 9] }
        shows: "rebid of my own five-card hearts at the three level: a self-sufficient suit and the values for the level"
        establishes: { forcing: non_forcing }
      - id: cl_rebid5_three_S
        call: 3S
        priority: 28.3
        when: { my_suit: S, cheapest_in_suit: true, we_hold_contract: false }
        requires:
          suits: { S: [5, 13] }
          evals: { total_points: [13, 40], "suit_quality(S)": [2.0, 9] }
        shows: "rebid of my own five-card spades at the three level: a self-sufficient suit and the values for the level"
        establishes: { forcing: non_forcing }
      # ---------------------------------------------------------------
      # FAMILY 3 - THE DISCIPLINE PASS.  Every rung here carries a
      # non-empty `requires` that names the described hand, and every one
      # is priced to outrank only the specific natural bid it replaces.
      # `cl_pass` (20) is untouched and no code fallback is deleted,
      # because P is already covered in this context.
      # ---------------------------------------------------------------
      - id: cl_pass_sandwich_discipline
        call: P
        priority: 27.7
        when: { i_have_acted: false, side_has_acted: false, standing_bid_level: [2],
                we_hold_contract: false }
        requires:
          hcp: [0, 11]
          evals: { their_bidders: [2, 2] }
        shows: "both of them have bid and described and my side has never acted: eleven points is not a three-level entry"
        establishes: { forcing: non_forcing }
      - id: cl_pass_vul_nofit
        call: P
        priority: 27.6
        when: { we_vulnerable: true, side_has_acted: false, standing_bid_level: [2, 3],
                we_hold_contract: false }
        requires:
          hcp: [0, 10]
          evals: { quick_tricks: [0, 1.5], their_fit: [7, 26] }
        shows: "vulnerable, they have found a fit, nobody on our side has bid and I have neither values nor defence: pass"
        establishes: { forcing: non_forcing }
        negative_inference_weight: soft
      - id: cl_pass_after_my_double
        call: P
        priority: 27.55
        when: { my_last_call_was_double: true, standing_bid_level: [2, 3, 4, 5, 6, 7],
                we_hold_contract: false }
        requires:
          hcp: [11, 16]
          evals: { longest_suit_length: [0, 5] }
        shows: "I have already doubled for values: with no six-card suit I defend rather than invent a new suit at the three level"
        establishes: { forcing: non_forcing }
      - id: cl_pass_misfit_H
        call: P
        priority: 26.75
        when: { partner_suit: H, side_has_acted: true, i_have_acted: false,
                standing_bid_level: [2], we_hold_contract: false }
        requires:
          suits: { H: [0, 1] }
          evals: { total_points: [0, 11] }
        shows: "a singleton in partner's overcalled hearts with less than opening values: pass rather than invent a second contract"
        establishes: { forcing: non_forcing }
      - id: cl_pass_misfit_S
        call: P
        priority: 26.75
        when: { partner_suit: S, side_has_acted: true, i_have_acted: false,
                standing_bid_level: [2], we_hold_contract: false }
        requires:
          suits: { S: [0, 1] }
          evals: { total_points: [0, 11] }
        shows: "a singleton in partner's overcalled spades with less than opening values: pass rather than invent a second contract"
        establishes: { forcing: non_forcing }
      - id: cl_pass_silent_over_nt
        call: P
        priority: 26.7
        when: { side_has_acted: false, standing_bid_strain: [NT], we_hold_contract: false }
        requires:
          evals: { total_points: [0, 11] }
        shows: "they have settled in notrump and partner has never bid: a two-level entry on eleven points is a losing action"
        establishes: { forcing: non_forcing }
      # ---------------------------------------------------------------
      # The minor-suit game.  `cl_raise_$m4` tops the ladder out at four of
      # a minor, which buys nothing three does not; `grep cl_minor_game`
      # returns nothing.
      # ---------------------------------------------------------------
      - id: cl_minor_game_5C
        call: 5C
        priority: 27.65
        when: { partner_suit: C, we_hold_contract: false }
        requires:
          suits: { C: [5, 13] }
          evals: { total_points: [15, 40], rule_of_26: [26, 99], "lott_total_trumps(C)": [10, 26] }
        shows: "eleven tricks in clubs: a ten-card fit and the values, where four of a minor buys nothing three does not"
        establishes: { forcing: non_forcing, agreed_suit: C }
      - id: cl_minor_game_5D
        call: 5D
        priority: 27.65
        when: { partner_suit: D, we_hold_contract: false }
        requires:
          suits: { D: [5, 13] }
          evals: { total_points: [15, 40], rule_of_26: [26, 99], "lott_total_trumps(D)": [10, 26] }
        shows: "eleven tricks in diamonds: a ten-card fit and the values, where four of a minor buys nothing three does not"
        establishes: { forcing: non_forcing, agreed_suit: D }
      # Long suits and shape credentials below the honour toll.
      - id: cl_new_long3_lim_H
        call: 3H
        priority: 27.4
        when: { unbid_suit: H, cheapest_in_suit: true, we_hold_contract: false }
        requires:
          suits: { H: [6, 13] }
          evals: { rule_of_26: [21, 99], partner_shown_max: [0, 19] }
        shows: "a six-card heart suit opposite a partner who has already limited himself high: the combined values are known, so the suit is bid on length"
        establishes: { forcing: non_forcing }
      - id: cl_new_long3_lim_S
        call: 3S
        priority: 27.4
        when: { unbid_suit: S, cheapest_in_suit: true, we_hold_contract: false }
        requires:
          suits: { S: [6, 13] }
          evals: { rule_of_26: [21, 99], partner_shown_max: [0, 19] }
        shows: "a six-card spade suit opposite a partner who has already limited himself high: the combined values are known, so the suit is bid on length"
        establishes: { forcing: non_forcing }
      - id: cl_new_void3_C
        call: 3C
        priority: 27.2
        when: { unbid_suit: C, cheapest_in_suit: true, i_have_acted: true, we_hold_contract: false }
        requires:
          suits: { C: [5, 13] }
          evals: { void: [1, 1], total_points: [10, 40] }
        shows: "a five-card second suit is worth the three level when I hold a void"
        establishes: { forcing: non_forcing }
      - id: cl_new_void3_D
        call: 3D
        priority: 27.2
        when: { unbid_suit: D, cheapest_in_suit: true, i_have_acted: true, we_hold_contract: false }
        requires:
          suits: { D: [5, 13] }
          evals: { void: [1, 1], total_points: [10, 40] }
        shows: "a five-card second suit is worth the three level when I hold a void"
        establishes: { forcing: non_forcing }
      - id: cl_new_void3_H
        call: 3H
        priority: 27.2
        when: { unbid_suit: H, cheapest_in_suit: true, i_have_acted: true, we_hold_contract: false }
        requires:
          suits: { H: [5, 13] }
          evals: { void: [1, 1], total_points: [10, 40] }
        shows: "a five-card second suit is worth the three level when I hold a void"
        establishes: { forcing: non_forcing }
      - id: cl_new_void3_S
        call: 3S
        priority: 27.2
        when: { unbid_suit: S, cheapest_in_suit: true, i_have_acted: true, we_hold_contract: false }
        requires:
          suits: { S: [5, 13] }
          evals: { void: [1, 1], total_points: [10, 40] }
        shows: "a five-card second suit is worth the three level when I hold a void"
        establishes: { forcing: non_forcing }
      - id: cl_new_strong2_C
        call: 2C
        priority: 26.8
        when: { unbid_suit: C, cheapest_in_suit: true, side_has_acted: true,
                i_have_acted: false, standing_bid_level: [2], we_hold_contract: false }
        requires:
          suits: { C: [5, 13] }
          evals: { rule_of_26: [21, 99], total_points: [6, 40] }
        shows: "natural clubs opposite a partner who has shown a strong balanced hand: 5+ cards, 6+ points, no honour toll"
        establishes: { forcing: non_forcing }
      - id: cl_new_strong2_D
        call: 2D
        priority: 26.8
        when: { unbid_suit: D, cheapest_in_suit: true, side_has_acted: true,
                i_have_acted: false, standing_bid_level: [2], we_hold_contract: false }
        requires:
          suits: { D: [5, 13] }
          evals: { rule_of_26: [21, 99], total_points: [6, 40] }
        shows: "natural diamonds opposite a partner who has shown a strong balanced hand: 5+ cards, 6+ points, no honour toll"
        establishes: { forcing: non_forcing }
      - id: cl_new_strong2_H
        call: 2H
        priority: 26.8
        when: { unbid_suit: H, cheapest_in_suit: true, side_has_acted: true,
                i_have_acted: false, standing_bid_level: [2], we_hold_contract: false }
        requires:
          suits: { H: [5, 13] }
          evals: { rule_of_26: [21, 99], total_points: [6, 40] }
        shows: "natural hearts opposite a partner who has shown a strong balanced hand: 5+ cards, 6+ points, no honour toll"
        establishes: { forcing: non_forcing }
      - id: cl_new_strong2_S
        call: 2S
        priority: 26.8
        when: { unbid_suit: S, cheapest_in_suit: true, side_has_acted: true,
                i_have_acted: false, standing_bid_level: [2], we_hold_contract: false }
        requires:
          suits: { S: [5, 13] }
          evals: { rule_of_26: [21, 99], total_points: [6, 40] }
        shows: "natural spades opposite a partner who has shown a strong balanced hand: 5+ cards, 6+ points, no honour toll"
        establishes: { forcing: non_forcing }
      - id: cl_new_twosuit_H2
        call: 2H
        priority: 26.6
        when: { unbid_suit: H, cheapest_in_suit: true, we_hold_contract: false }
        requires:
          suits: { H: [5, 13] }
          evals: { total_points: [10, 40] }
          any_of:
            - suits: { S: [5, 13] }
            - suits: { D: [5, 13] }
            - suits: { C: [5, 13] }
        shows: "natural hearts with a second five-card suit: shape is the credential, not suit quality"
        establishes: { forcing: non_forcing }
      - id: cl_new_twosuit_S2
        call: 2S
        priority: 26.6
        when: { unbid_suit: S, cheapest_in_suit: true, we_hold_contract: false }
        requires:
          suits: { S: [5, 13] }
          evals: { total_points: [10, 40] }
          any_of:
            - suits: { H: [5, 13] }
            - suits: { D: [5, 13] }
            - suits: { C: [5, 13] }
        shows: "natural spades with a second five-card suit: shape is the credential, not suit quality"
        establishes: { forcing: non_forcing }
      # The bottom of the ladder: length and values with no honour toll at
      # all, above `cl_pass` (20) and below every rung that asks for more.
      - id: cl_new_values2_C
        call: 2C
        priority: 24.5
        when: { unbid_suit: C, cheapest_in_suit: true, we_hold_contract: false }
        requires:
          suits: { C: [5, 13] }
          evals: { total_points: [10, 40] }
        shows: "natural clubs at the cheapest level on length and values: 5+ cards, 10+ points, no honour requirement"
        establishes: { forcing: non_forcing }
      - id: cl_new_values2_D
        call: 2D
        priority: 24.5
        when: { unbid_suit: D, cheapest_in_suit: true, we_hold_contract: false }
        requires:
          suits: { D: [5, 13] }
          evals: { total_points: [10, 40] }
        shows: "natural diamonds at the cheapest level on length and values: 5+ cards, 10+ points, no honour requirement"
        establishes: { forcing: non_forcing }
      - id: cl_new_values2_H
        call: 2H
        priority: 24.5
        when: { unbid_suit: H, cheapest_in_suit: true, we_hold_contract: false }
        requires:
          suits: { H: [5, 13] }
          evals: { total_points: [10, 40] }
        shows: "natural hearts at the cheapest level on length and values: 5+ cards, 10+ points, no honour requirement"
        establishes: { forcing: non_forcing }
      - id: cl_new_values2_S
        call: 2S
        priority: 24.5
        when: { unbid_suit: S, cheapest_in_suit: true, we_hold_contract: false }
        requires:
          suits: { S: [5, 13] }
          evals: { total_points: [10, 40] }
        shows: "natural spades at the cheapest level on length and values: 5+ cards, 10+ points, no honour requirement"
        establishes: { forcing: non_forcing }

#== RULES general_competitive_high
      # ---------------------------------------------------------------
      # `ch_pass` is beaten by acting at +1.90 +/- 0.66 over n = 67
      # (CFR_R18) and carries 592 vacuous decisions (COVERAGE_R18).  The
      # repair is vocabulary to ACT, which is what most of this block is;
      # the three PASS rungs are narrow, described hands only.
      # ---------------------------------------------------------------
      - id: ch_raise_over_jump_H4
        call: 4H
        priority: 32.2
        when: { partner_suit: H, we_vulnerable: false, standing_bid_level: [4],
                their_last_bid_suit: true, we_hold_contract: false }
        requires:
          suits: { H: [4, 13] }
          evals: { "lott_total_trumps(H)": [9, 26], total_points: [6, 40] }
        shows: "they leapt to game to shut us out: with four trumps and nine combined we take the push rather than defend undoubled"
        establishes: { forcing: non_forcing, agreed_suit: H }
      - id: ch_raise_over_jump_S4
        call: 4S
        priority: 32.2
        when: { partner_suit: S, we_vulnerable: false, standing_bid_level: [4],
                their_last_bid_suit: true, we_hold_contract: false }
        requires:
          suits: { S: [4, 13] }
          evals: { "lott_total_trumps(S)": [9, 26], total_points: [6, 40] }
        shows: "they leapt to game to shut us out: with four trumps and nine combined we take the push rather than defend undoubled"
        establishes: { forcing: non_forcing, agreed_suit: S }
      # ---------------------------------------------------------------
      # FAMILY 1 (high) - the Law in a minor, and the raise of partner's
      # PREEMPT, which does not exist anywhere in the file.
      # ---------------------------------------------------------------
      - id: ch_raise_lott4_C
        call: 4C
        priority: 31.9
        when: { partner_suit: C, is_competitive: true, we_hold_contract: false }
        requires:
          suits: { C: [4, 13] }
          evals: { "lott_total_trumps(C)": [9, 26], their_fit: [7, 26], total_points: [6, 40] }
        shows: "the Law at the four level in a minor: ten trumps ours and a fit theirs, so the level follows the trumps"
        establishes: { forcing: non_forcing, agreed_suit: C }
      - id: ch_raise_lott4_D
        call: 4D
        priority: 31.9
        when: { partner_suit: D, is_competitive: true, we_hold_contract: false }
        requires:
          suits: { D: [4, 13] }
          evals: { "lott_total_trumps(D)": [9, 26], their_fit: [7, 26], total_points: [6, 40] }
        shows: "the Law at the four level in a minor: ten trumps ours and a fit theirs, so the level follows the trumps"
        establishes: { forcing: non_forcing, agreed_suit: D }
      - id: ch_raise_preempt3_C
        call: 3C
        priority: 31.6
        when: { partner_suit: C, cheapest_in_suit: true, i_preempted: false, we_hold_contract: false }
        requires:
          suits: { C: [2, 13] }
          evals: { "partner_shown_length(C)": [6, 13], "lott_total_trumps(C)": [8, 26], total_points: [8, 40] }
        shows: "raising partner's preempt to the level of the fit: two trumps opposite a known six make eight, and eight trumps belong at the three level"
        establishes: { forcing: non_forcing, agreed_suit: C }
      - id: ch_raise_preempt3_D
        call: 3D
        priority: 31.6
        when: { partner_suit: D, cheapest_in_suit: true, i_preempted: false, we_hold_contract: false }
        requires:
          suits: { D: [2, 13] }
          evals: { "partner_shown_length(D)": [6, 13], "lott_total_trumps(D)": [8, 26], total_points: [8, 40] }
        shows: "raising partner's preempt to the level of the fit: two trumps opposite a known six make eight, and eight trumps belong at the three level"
        establishes: { forcing: non_forcing, agreed_suit: D }
      - id: ch_raise_preempt3_H
        call: 3H
        priority: 31.6
        when: { partner_suit: H, cheapest_in_suit: true, i_preempted: false, we_hold_contract: false }
        requires:
          suits: { H: [2, 13] }
          evals: { "partner_shown_length(H)": [6, 13], "lott_total_trumps(H)": [8, 26], total_points: [8, 40] }
        shows: "raising partner's preempt to the level of the fit: two trumps opposite a known six make eight, and eight trumps belong at the three level"
        establishes: { forcing: non_forcing, agreed_suit: H }
      - id: ch_raise_preempt3_S
        call: 3S
        priority: 31.6
        when: { partner_suit: S, cheapest_in_suit: true, i_preempted: false, we_hold_contract: false }
        requires:
          suits: { S: [2, 13] }
          evals: { "partner_shown_length(S)": [6, 13], "lott_total_trumps(S)": [8, 26], total_points: [8, 40] }
        shows: "raising partner's preempt to the level of the fit: two trumps opposite a known six make eight, and eight trumps belong at the three level"
        establishes: { forcing: non_forcing, agreed_suit: S }
      # ---------------------------------------------------------------
      # The Law also says when to STOP.  Eight trumps is eight tricks, so
      # over their three-level action we defend.  Gated on
      # `partner_shown_max` so it can never fire opposite an unlimited
      # partner, and priced above `ch_raise_$M3` (31) - the rule it
      # replaces - but below `ch_raise_$M4` (32), so a genuine ten-trump
      # hand still bids game.
      # ---------------------------------------------------------------
      - id: ch_sell_out_H
        call: P
        priority: 31.5
        when: { partner_suit: H, standing_bid_level: [3], we_bid_last: false,
                i_have_acted: true, their_last_bid_suit: true, we_hold_contract: false }
        requires:
          suits: { H: [3, 13] }
          evals: { "lott_total_trumps(H)": [0, 8], partner_shown_max: [0, 11], total_points: [0, 15] }
        shows: "partner's raise showed his hand, we hold only eight hearts and I have no extras: the Law says sell out"
        establishes: { forcing: sign_off }
      - id: ch_sell_out_S
        call: P
        priority: 31.5
        when: { partner_suit: S, standing_bid_level: [3], we_bid_last: false,
                i_have_acted: true, their_last_bid_suit: true, we_hold_contract: false }
        requires:
          suits: { S: [3, 13] }
          evals: { "lott_total_trumps(S)": [0, 8], partner_shown_max: [0, 11], total_points: [0, 15] }
        shows: "partner's raise showed his hand, we hold only eight spades and I have no extras: the Law says sell out"
        establishes: { forcing: sign_off }
      # Competing to three in a suit BOTH of us have bid.
      - id: ch_compete_agreed3_C
        call: 3C
        priority: 31.4
        when: { my_suit: C, partner_suit: C, is_competitive: true, cheapest_in_suit: true,
                we_hold_contract: false }
        requires:
          suits: { C: [4, 13] }
          evals: { total_points: [7, 12], "lott_total_trumps(C)": [7, 26] }
        shows: "they have outbid our agreed fit: with four trumps opposite partner's raise the Law says compete to three"
        establishes: { forcing: non_forcing, agreed_suit: C }
      - id: ch_compete_agreed3_D
        call: 3D
        priority: 31.4
        when: { my_suit: D, partner_suit: D, is_competitive: true, cheapest_in_suit: true,
                we_hold_contract: false }
        requires:
          suits: { D: [4, 13] }
          evals: { total_points: [7, 12], "lott_total_trumps(D)": [7, 26] }
        shows: "they have outbid our agreed fit: with four trumps opposite partner's raise the Law says compete to three"
        establishes: { forcing: non_forcing, agreed_suit: D }
      - id: ch_compete_agreed3_H
        call: 3H
        priority: 31.4
        when: { my_suit: H, partner_suit: H, is_competitive: true, cheapest_in_suit: true,
                we_hold_contract: false }
        requires:
          suits: { H: [4, 13] }
          evals: { total_points: [7, 12], "lott_total_trumps(H)": [7, 26] }
        shows: "they have outbid our agreed fit: with four trumps opposite partner's raise the Law says compete to three"
        establishes: { forcing: non_forcing, agreed_suit: H }
      - id: ch_compete_agreed3_S
        call: 3S
        priority: 31.4
        when: { my_suit: S, partner_suit: S, is_competitive: true, cheapest_in_suit: true,
                we_hold_contract: false }
        requires:
          suits: { S: [4, 13] }
          evals: { total_points: [7, 12], "lott_total_trumps(S)": [7, 26] }
        shows: "they have outbid our agreed fit: with four trumps opposite partner's raise the Law says compete to three"
        establishes: { forcing: non_forcing, agreed_suit: S }
      # The Law three-level raise, priced BELOW `ch_raise_$X3` (31) so it
      # only inherits the hands the values rung declines.
      - id: ch_raise_lott3_H
        call: 3H
        priority: 30.6
        when: { partner_suit: H, cheapest_in_suit: true, is_competitive: true, we_hold_contract: false }
        requires:
          suits: { H: [3, 13] }
          evals: { "lott_total_trumps(H)": [9, 26], partner_shown_max: [0, 11], total_points: [5, 40] }
        shows: "the Law at the three level opposite a limited partner: nine trumps our way, so three of the major is right on shape"
        establishes: { forcing: non_forcing, agreed_suit: H }
      - id: ch_raise_lott3_S
        call: 3S
        priority: 30.6
        when: { partner_suit: S, cheapest_in_suit: true, is_competitive: true, we_hold_contract: false }
        requires:
          suits: { S: [3, 13] }
          evals: { "lott_total_trumps(S)": [9, 26], partner_shown_max: [0, 11], total_points: [5, 40] }
        shows: "the Law at the three level opposite a limited partner: nine trumps our way, so three of the major is right on shape"
        establishes: { forcing: non_forcing, agreed_suit: S }
      - id: ch_raise_lott3_C
        call: 3C
        priority: 30.55
        when: { partner_suit: C, cheapest_in_suit: true, is_competitive: true, we_hold_contract: false }
        requires:
          suits: { C: [5, 13] }
          evals: { "lott_total_trumps(C)": [8, 26], total_points: [3, 9] }
        shows: "preemptive raise of partner's clubs to the level of our fit: five-card support and no defence"
        establishes: { forcing: non_forcing, agreed_suit: C }
      - id: ch_raise_lott3_D
        call: 3D
        priority: 30.55
        when: { partner_suit: D, cheapest_in_suit: true, is_competitive: true, we_hold_contract: false }
        requires:
          suits: { D: [5, 13] }
          evals: { "lott_total_trumps(D)": [8, 26], total_points: [3, 9] }
        shows: "preemptive raise of partner's diamonds to the level of our fit: five-card support and no defence"
        establishes: { forcing: non_forcing, agreed_suit: D }
      - id: ch_shape_game_H
        call: 4H
        priority: 30.5
        when: { unbid_suit: H, side_has_acted: true, i_have_acted: false, we_hold_contract: false }
        requires:
          suits: { H: [6, 13] }
          evals: { standing_suit_length: [0, 1], "suit_quality(H)": [1.5, 9],
                   "lott_total_trumps(H)": [8, 26], rule_of_26: [22, 99] }
        shows: "six-card heart suit with a void or singleton in the suit they have jumped in: game on shape"
        establishes: { forcing: non_forcing, agreed_suit: H }
      - id: ch_shape_game_S
        call: 4S
        priority: 30.5
        when: { unbid_suit: S, side_has_acted: true, i_have_acted: false, we_hold_contract: false }
        requires:
          suits: { S: [6, 13] }
          evals: { standing_suit_length: [0, 1], "suit_quality(S)": [1.5, 9],
                   "lott_total_trumps(S)": [8, 26], rule_of_26: [22, 99] }
        shows: "six-card spade suit with a void or singleton in the suit they have jumped in: game on shape"
        establishes: { forcing: non_forcing, agreed_suit: S }
      # Our minor is AGREED and they have bid one more.  `ch_raise_$m4`
      # re-tests the fit from scratch and cannot reach this position.
      - id: ch_compete_agreed4_C
        call: 4C
        priority: 30.2
        when: { my_suit: C, partner_suit: C, cheapest_in_suit: true, is_competitive: true,
                standing_bid_level: [3], we_hold_contract: false }
        requires:
          suits: { C: [3, 13] }
          evals: { total_points: [10, 40], "lott_total_trumps(C)": [7, 26] }
        shows: "our clubs are agreed and they have bid one more: competing to the level of the fit"
        establishes: { forcing: non_forcing, agreed_suit: C }
      - id: ch_compete_agreed4_D
        call: 4D
        priority: 30.2
        when: { my_suit: D, partner_suit: D, cheapest_in_suit: true, is_competitive: true,
                standing_bid_level: [3], we_hold_contract: false }
        requires:
          suits: { D: [3, 13] }
          evals: { total_points: [10, 40], "lott_total_trumps(D)": [7, 26] }
        shows: "our diamonds are agreed and they have bid one more: competing to the level of the fit"
        establishes: { forcing: non_forcing, agreed_suit: D }
      # ---------------------------------------------------------------
      # DISCIPLINE PASSES.  Both are narrow and both are priced to
      # outrank only the natural rungs at 27-30 that they replace.
      # ---------------------------------------------------------------
      - id: ch_pass_described
        call: P
        priority: 29.6
        when: { i_have_acted: true, side_has_acted: true, standing_bid_level: [3],
                we_bid_last: false, we_hold_contract: false }
        requires:
          hcp: [14, 17]
          evals: { balanced: [1, 1], longest_suit_length: [0, 5] }
        shows: "I have already shown a balanced 14-17 and hold no six-card suit: their three-level balance gets no second bid from me"
        establishes: { forcing: sign_off }
      - id: ch_pass_opposite_preempt
        call: P
        priority: 30.4
        when: { side_has_acted: true, i_have_acted: false, we_hold_contract: false }
        requires:
          hcp: [0, 15]
          evals: { partner_shown_max: [0, 10], longest_suit_length: [0, 5],
                   "suit_length(partner)": [0, 1] }
        shows: "misfit with partner's preempt: a singleton in his suit, no six-card suit of my own and no game force - a free bid at the three level turns his plus into a minus"
        establishes: { forcing: sign_off }
      - id: ch_pass_limited_A
        call: P
        priority: 27.6
        when: { partner_has_acted: true, their_last_bid_suit: true, we_hold_contract: false }
        requires:
          evals: { partner_shown_max: [0, 8], total_points: [0, 17] }
        shows: "partner is limited to eight and I hold at most seventeen: twenty-five is not there, so stop bidding"
        establishes: { forcing: sign_off }
      # ---------------------------------------------------------------
      # Shape rungs the point floors were suppressing.
      # ---------------------------------------------------------------
      - id: ch_second_major_H3
        call: 3H
        priority: 29.5
        when: { unbid_suit: H, cheapest_in_suit: true, i_have_acted: true, we_hold_contract: false }
        requires:
          suits: { H: [4, 13] }
          evals: { longest_suit_length: [5, 5], total_points: [16, 40] }
        shows: "my second suit over their preempt: five of my own and four hearts with extras - a 4-4 major fit beats notrump on a doubleton stopper"
        establishes: { forcing: non_forcing }
      - id: ch_second_major_S3
        call: 3S
        priority: 29.5
        when: { unbid_suit: S, cheapest_in_suit: true, i_have_acted: true, we_hold_contract: false }
        requires:
          suits: { S: [4, 13] }
          evals: { longest_suit_length: [5, 5], total_points: [16, 40] }
        shows: "my second suit over their preempt: five of my own and four spades with extras - a 4-4 major fit beats notrump on a doubleton stopper"
        establishes: { forcing: non_forcing }
      - id: ch_second65_H
        call: 4H
        priority: 29.45
        when: { my_suit: S, unbid_suit: H, cheapest_in_suit: true, we_hold_contract: false }
        requires:
          suits: { H: [5, 13], S: [6, 13] }
          evals: { total_points: [12, 40], "suit_quality(H)": [1.0, 9] }
        shows: "six-five come alive: six spades and five hearts, showing the second suit instead of naming the first a third time"
        establishes: { forcing: non_forcing }
      - id: ch_second65_S
        call: 4S
        priority: 29.45
        when: { my_suit: H, unbid_suit: S, cheapest_in_suit: true, we_hold_contract: false }
        requires:
          suits: { S: [5, 13], H: [6, 13] }
          evals: { total_points: [12, 40], "suit_quality(S)": [1.0, 9] }
        shows: "six-five come alive: six hearts and five spades, showing the second suit instead of naming the first a third time"
        establishes: { forcing: non_forcing }
      - id: ch_rebid_shape_C3
        call: 3C
        priority: 29.2
        when: { my_suit: C, cheapest_in_suit: true, i_have_acted: true, we_hold_contract: false }
        requires:
          suits: { C: [6, 13] }
          evals: { total_points: [12, 40], singleton_or_void: [1, 1], "suit_quality(C)": [1, 9] }
        shows: "rebidding my six-card suit over their preemptive jump: opening values and a shortage - combined values are the wrong test once they have taken my room"
        establishes: { forcing: non_forcing }
      - id: ch_rebid_shape_D3
        call: 3D
        priority: 29.2
        when: { my_suit: D, cheapest_in_suit: true, i_have_acted: true, we_hold_contract: false }
        requires:
          suits: { D: [6, 13] }
          evals: { total_points: [12, 40], singleton_or_void: [1, 1], "suit_quality(D)": [1, 9] }
        shows: "rebidding my six-card suit over their preemptive jump: opening values and a shortage - combined values are the wrong test once they have taken my room"
        establishes: { forcing: non_forcing }
      - id: ch_rebid_shape_H3
        call: 3H
        priority: 29.2
        when: { my_suit: H, cheapest_in_suit: true, i_have_acted: true, we_hold_contract: false }
        requires:
          suits: { H: [6, 13] }
          evals: { total_points: [12, 40], singleton_or_void: [1, 1], "suit_quality(H)": [1, 9] }
        shows: "rebidding my six-card suit over their preemptive jump: opening values and a shortage - combined values are the wrong test once they have taken my room"
        establishes: { forcing: non_forcing }
      - id: ch_rebid_shape_S3
        call: 3S
        priority: 29.2
        when: { my_suit: S, cheapest_in_suit: true, i_have_acted: true, we_hold_contract: false }
        requires:
          suits: { S: [6, 13] }
          evals: { total_points: [12, 40], singleton_or_void: [1, 1], "suit_quality(S)": [1, 9] }
        shows: "rebidding my six-card suit over their preemptive jump: opening values and a shortage - combined values are the wrong test once they have taken my room"
        establishes: { forcing: non_forcing }

#== RULES general_balancing_low
      # ---------------------------------------------------------------
      # `ballow_reopen_X` measures +3.75 over 4 tables and is not touched.
      # Everything added here either lowers the FLOOR into that winning
      # family or gives the balancer his own suit, which the double never
      # promised.  `ballow_X` measures -2.91 over 11 tables, so a rung that
      # outranks IT is routing hands out of a loser.
      # ---------------------------------------------------------------
      - id: ballow_own7_C
        call: 2C
        priority: 41.9
        when: { unbid_suit: C, cheapest_in_suit: true, side_has_acted: false, we_hold_contract: false }
        requires: { suits: { C: [7, 13] }, evals: { total_points: [8, 40], "suit_quality(C)": [1, 9] } }
        shows: "natural clubs in the balancing seat with a SEVEN-card suit: a one-suiter names its own trumps - the double would ask partner to pick a suit I do not hold"
        establishes: { forcing: non_forcing }
      - id: ballow_own7_D
        call: 2D
        priority: 41.9
        when: { unbid_suit: D, cheapest_in_suit: true, side_has_acted: false, we_hold_contract: false }
        requires: { suits: { D: [7, 13] }, evals: { total_points: [8, 40], "suit_quality(D)": [1, 9] } }
        shows: "natural diamonds in the balancing seat with a SEVEN-card suit: a one-suiter names its own trumps"
        establishes: { forcing: non_forcing }
      - id: ballow_own7_H
        call: 2H
        priority: 41.9
        when: { unbid_suit: H, cheapest_in_suit: true, side_has_acted: false, we_hold_contract: false }
        requires: { suits: { H: [7, 13] }, evals: { total_points: [8, 40], "suit_quality(H)": [1, 9] } }
        shows: "natural hearts in the balancing seat with a SEVEN-card suit: a one-suiter names its own trumps"
        establishes: { forcing: non_forcing }
      - id: ballow_own7_S
        call: 2S
        priority: 41.9
        when: { unbid_suit: S, cheapest_in_suit: true, side_has_acted: false, we_hold_contract: false }
        requires: { suits: { S: [7, 13] }, evals: { total_points: [8, 40], "suit_quality(S)": [1, 9] } }
        shows: "natural spades in the balancing seat with a SEVEN-card suit: a one-suiter names its own trumps"
        establishes: { forcing: non_forcing }
      - id: ballow_own6_C
        call: 2C
        priority: 41.6
        when: { unbid_suit: C, cheapest_in_suit: true, side_has_acted: false, we_hold_contract: false }
        requires: { suits: { C: [6, 13] }, evals: { total_points: [8, 16], "suit_quality(C)": [2.0, 9] } }
        shows: "a good six-card club suit in the balancing seat: bidding my own suit rather than asking for partner's"
        establishes: { forcing: non_forcing }
      - id: ballow_own6_D
        call: 2D
        priority: 41.6
        when: { unbid_suit: D, cheapest_in_suit: true, side_has_acted: false, we_hold_contract: false }
        requires: { suits: { D: [6, 13] }, evals: { total_points: [8, 16], "suit_quality(D)": [2.0, 9] } }
        shows: "a good six-card diamond suit in the balancing seat: bidding my own suit rather than asking for partner's"
        establishes: { forcing: non_forcing }
      - id: ballow_own6_H
        call: 2H
        priority: 41.6
        when: { unbid_suit: H, cheapest_in_suit: true, side_has_acted: false, we_hold_contract: false }
        requires: { suits: { H: [6, 13] }, evals: { total_points: [8, 16], "suit_quality(H)": [2.0, 9] } }
        shows: "a good six-card heart suit in the balancing seat: bidding my own suit rather than asking for partner's"
        establishes: { forcing: non_forcing }
      - id: ballow_own6_S
        call: 2S
        priority: 41.6
        when: { unbid_suit: S, cheapest_in_suit: true, side_has_acted: false, we_hold_contract: false }
        requires: { suits: { S: [6, 13] }, evals: { total_points: [8, 16], "suit_quality(S)": [2.0, 9] } }
        shows: "a good six-card spade suit in the balancing seat: bidding my own suit rather than asking for partner's"
        establishes: { forcing: non_forcing }
      - id: ballow_balance_major_H
        call: 2H
        priority: 41.4
        when: { unbid_suit: H, cheapest_in_suit: true, side_has_acted: false, we_hold_contract: false }
        requires:
          suits: { H: [5, 13] }
          evals: { total_points: [8, 13], "suit_quality(H)": [1, 9] }
        shows: "balancing in my five-card major rather than doubling: a double promises three cards in every unbid suit, and partner will pass a suit"
        establishes: { forcing: non_forcing }
      - id: ballow_balance_major_S
        call: 2S
        priority: 41.4
        when: { unbid_suit: S, cheapest_in_suit: true, side_has_acted: false, we_hold_contract: false }
        requires:
          suits: { S: [5, 13] }
          evals: { total_points: [8, 13], "suit_quality(S)": [1, 9] }
        shows: "balancing in my five-card major rather than doubling: a double promises three cards in every unbid suit, and partner will pass a suit"
        establishes: { forcing: non_forcing }
      - id: ballow_raise_brake_H2
        call: 2H
        priority: 32.6
        when: { partner_suit: H, cheapest_in_suit: true, we_hold_contract: false }
        requires:
          suits: { H: [3, 13] }
          evals: { "lott_total_trumps(H)": [7, 8], rule_of_26: [23, 27], total_points: [10, 40] }
        shows: "eight trumps and a game count that rests on partner's unshown maximum: compete, do not bid game"
        establishes: { forcing: non_forcing, agreed_suit: H }
      - id: ballow_raise_brake_S2
        call: 2S
        priority: 32.6
        when: { partner_suit: S, cheapest_in_suit: true, we_hold_contract: false }
        requires:
          suits: { S: [3, 13] }
          evals: { "lott_total_trumps(S)": [7, 8], rule_of_26: [23, 27], total_points: [10, 40] }
        shows: "eight trumps and a game count that rests on partner's unshown maximum: compete, do not bid game"
        establishes: { forcing: non_forcing, agreed_suit: S }
      - id: ballow_raise_brake_H3
        call: 3H
        priority: 32.5
        when: { partner_suit: H, cheapest_in_suit: true, we_hold_contract: false }
        requires:
          suits: { H: [3, 13] }
          evals: { "lott_total_trumps(H)": [7, 8], rule_of_26: [23, 27], total_points: [10, 40] }
        shows: "eight trumps and a game count that rests on partner's unshown maximum: invite at three, do not bid four"
        establishes: { forcing: non_forcing, agreed_suit: H }
      - id: ballow_raise_brake_S3
        call: 3S
        priority: 32.5
        when: { partner_suit: S, cheapest_in_suit: true, we_hold_contract: false }
        requires:
          suits: { S: [3, 13] }
          evals: { "lott_total_trumps(S)": [7, 8], rule_of_26: [23, 27], total_points: [10, 40] }
        shows: "eight trumps and a game count that rests on partner's unshown maximum: invite at three, do not bid four"
        establishes: { forcing: non_forcing, agreed_suit: S }
      # The Law in the pass-out seat: the four-level minor twin the majors
      # have had all along, and the three-level rung nobody has.
      - id: ballow_raise_lott4_C
        call: 4C
        priority: 31.9
        when: { partner_suit: C, is_competitive: true, we_hold_contract: false }
        requires:
          suits: { C: [4, 13] }
          evals: { "lott_total_trumps(C)": [9, 26], their_fit: [7, 26], total_points: [6, 40] }
        shows: "the Law at the four level in a minor: ten trumps ours and a fit theirs"
        establishes: { forcing: non_forcing, agreed_suit: C }
      - id: ballow_raise_lott4_D
        call: 4D
        priority: 31.9
        when: { partner_suit: D, is_competitive: true, we_hold_contract: false }
        requires:
          suits: { D: [4, 13] }
          evals: { "lott_total_trumps(D)": [9, 26], their_fit: [7, 26], total_points: [6, 40] }
        shows: "the Law at the four level in a minor: ten trumps ours and a fit theirs"
        establishes: { forcing: non_forcing, agreed_suit: D }
      - id: ballow_raise_lott3_H
        call: 3H
        priority: 30.6
        when: { partner_suit: H, is_competitive: true, cheapest_in_suit: true, we_hold_contract: false }
        requires:
          suits: { H: [4, 13] }
          evals: { total_points: [5, 11], "lott_total_trumps(H)": [9, 26] }
        shows: "the Law at the three level: four trumps opposite partner's overcall, nine combined - the level follows the fit, not the points"
        establishes: { forcing: non_forcing, agreed_suit: H }
      - id: ballow_raise_lott3_S
        call: 3S
        priority: 30.6
        when: { partner_suit: S, is_competitive: true, cheapest_in_suit: true, we_hold_contract: false }
        requires:
          suits: { S: [4, 13] }
          evals: { total_points: [5, 11], "lott_total_trumps(S)": [9, 26] }
        shows: "the Law at the three level: four trumps opposite partner's overcall, nine combined - the level follows the fit, not the points"
        establishes: { forcing: non_forcing, agreed_suit: S }
      - id: ballow_raise_lott3_C
        call: 3C
        priority: 30.55
        when: { partner_suit: C, is_competitive: true, cheapest_in_suit: true, we_hold_contract: false }
        requires:
          suits: { C: [3, 13] }
          evals: { "lott_total_trumps(C)": [9, 26], total_points: [8, 40] }
        shows: "the Law in the pass-out seat: nine combined trumps, so three of partner's minor is our level - do not sell out to their two-level contract"
        establishes: { forcing: non_forcing, agreed_suit: C }
      - id: ballow_raise_lott3_D
        call: 3D
        priority: 30.55
        when: { partner_suit: D, is_competitive: true, cheapest_in_suit: true, we_hold_contract: false }
        requires:
          suits: { D: [3, 13] }
          evals: { "lott_total_trumps(D)": [9, 26], total_points: [8, 40] }
        shows: "the Law in the pass-out seat: nine combined trumps, so three of partner's minor is our level - do not sell out to their two-level contract"
        establishes: { forcing: non_forcing, agreed_suit: D }
      # ---------------------------------------------------------------
      # The balancer's own six-card suit at the three level.  TWO rungs,
      # because A and B are both right in different auctions: `own6` is
      # priced on the suit, `law3` on the opponents' fit.
      # ---------------------------------------------------------------
      - id: ballow_rebid_own6_C
        call: 3C
        priority: 29.6
        when: { my_suit: C, cheapest_in_suit: true, we_hold_contract: false }
        requires:
          suits: { C: [6, 13] }
          evals: { total_points: [9, 15], "suit_quality(C)": [2.5, 9] }
          features: [ "three_of_top5(C)" ]
        shows: "rebid of my own good six-card clubs in the balancing seat: playing strength of my own, not combined values"
        establishes: { forcing: non_forcing }
      - id: ballow_rebid_own6_D
        call: 3D
        priority: 29.6
        when: { my_suit: D, cheapest_in_suit: true, we_hold_contract: false }
        requires:
          suits: { D: [6, 13] }
          evals: { total_points: [9, 15], "suit_quality(D)": [2.5, 9] }
          features: [ "three_of_top5(D)" ]
        shows: "rebid of my own good six-card diamonds in the balancing seat: playing strength of my own, not combined values"
        establishes: { forcing: non_forcing }
      - id: ballow_rebid_own6_H
        call: 3H
        priority: 29.6
        when: { my_suit: H, cheapest_in_suit: true, we_hold_contract: false }
        requires:
          suits: { H: [6, 13] }
          evals: { total_points: [9, 15], "suit_quality(H)": [2.5, 9] }
          features: [ "three_of_top5(H)" ]
        shows: "rebid of my own good six-card hearts in the balancing seat: playing strength of my own, not combined values"
        establishes: { forcing: non_forcing }
      - id: ballow_rebid_own6_S
        call: 3S
        priority: 29.6
        when: { my_suit: S, cheapest_in_suit: true, we_hold_contract: false }
        requires:
          suits: { S: [6, 13] }
          evals: { total_points: [9, 15], "suit_quality(S)": [2.5, 9] }
          features: [ "three_of_top5(S)" ]
        shows: "rebid of my own good six-card spades in the balancing seat: playing strength of my own, not combined values"
        establishes: { forcing: non_forcing }
      - id: ballow_pass_partner_silent
        call: P
        priority: 29.5
        when: { i_have_acted: true, partner_has_acted: false, standing_bid_level: [2],
                their_last_bid_suit: true, we_bid_last: false, we_hold_contract: false }
        requires:
          hcp: [12, 17]
          evals: { longest_suit_length: [0, 6] }
        shows: "partner has never acted over their two-level bid: without eighteen points or a seventh card there is no third bid"
        establishes: { forcing: sign_off }
      - id: ballow_rebid_law3_C
        call: 3C
        priority: 29.4
        when: { my_suit: C, we_bid_last: false, cheapest_in_suit: true, we_hold_contract: false }
        requires:
          suits: { C: [6, 13] }
          evals: { total_points: [8, 40], their_fit: [8, 26] }
        shows: "the Law in the balancing seat: they have found an eight-card fit and I have a sixth trump, so competing to three is right on shape"
        establishes: { forcing: non_forcing }
      - id: ballow_rebid_law3_D
        call: 3D
        priority: 29.4
        when: { my_suit: D, we_bid_last: false, cheapest_in_suit: true, we_hold_contract: false }
        requires:
          suits: { D: [6, 13] }
          evals: { total_points: [8, 40], their_fit: [8, 26] }
        shows: "the Law in the balancing seat: they have found an eight-card fit and I have a sixth trump, so competing to three is right on shape"
        establishes: { forcing: non_forcing }
      - id: ballow_rebid_law3_H
        call: 3H
        priority: 29.4
        when: { my_suit: H, we_bid_last: false, cheapest_in_suit: true, we_hold_contract: false }
        requires:
          suits: { H: [6, 13] }
          evals: { total_points: [8, 40], their_fit: [8, 26] }
        shows: "the Law in the balancing seat: they have found an eight-card fit and I have a sixth trump, so competing to three is right on shape"
        establishes: { forcing: non_forcing }
      - id: ballow_rebid_law3_S
        call: 3S
        priority: 29.4
        when: { my_suit: S, we_bid_last: false, cheapest_in_suit: true, we_hold_contract: false }
        requires:
          suits: { S: [6, 13] }
          evals: { total_points: [8, 40], their_fit: [8, 26] }
        shows: "the Law in the balancing seat: they have found an eight-card fit and I have a sixth trump, so competing to three is right on shape"
        establishes: { forcing: non_forcing }
      - id: ballow_major_first_H
        call: 1H
        priority: 27.5
        when: { unbid_suit: H, cheapest_in_suit: true, we_hold_contract: false }
        requires:
          suits: { H: [4, 13] }
          evals: { total_points: [11, 16], "suit_quality(H)": [2.0, 9] }
        shows: "a good four-card heart suit at the one level: showing the major before rebidding notrump"
        establishes: { forcing: non_forcing }
      - id: ballow_major_first_S
        call: 1S
        priority: 27.5
        when: { unbid_suit: S, cheapest_in_suit: true, we_hold_contract: false }
        requires:
          suits: { S: [4, 13] }
          evals: { total_points: [11, 16], "suit_quality(S)": [2.0, 9] }
        shows: "a good four-card spade suit at the one level: showing the major before rebidding notrump"
        establishes: { forcing: non_forcing }

#== RULES general_balancing_high
      # ---------------------------------------------------------------
      # `balhigh_pass` runs 767 tables at -0.67 - the pass-out seat as a
      # whole is at baseline, so the repair is vocabulary in BOTH
      # directions: a double priced in shape, a penalty double, a Law
      # raise in a minor, and three narrow disciplinary passes.
      # ---------------------------------------------------------------
      - id: balhigh_no_defence_pass
        call: P
        priority: 41.5
        when: { their_last_bid_suit: true, side_has_acted: true, we_bid_last: false,
                my_last_call_was_double: false, i_have_acted: true, we_hold_contract: false }
        requires:
          evals: { standing_suit_length: [0, 1], longest_suit_length: [0, 6] }
        shows: "I have already bid my hand and I am void or singleton in their trump suit: a double now would be made because I have no trump tricks, so defend quietly"
        establishes: { forcing: sign_off }
        negative_inference_weight: soft
      - id: balhigh_rebid_H5
        call: 5H
        priority: 33.0
        when: { my_suit: H, standing_bid_level: [5], cheapest_in_suit: true, we_hold_contract: false }
        requires:
          suits: { H: [5, 13] }
          evals: { total_points: [15, 40], standing_suit_length: [0, 1] }
        shows: "over their five-level preempt: a void or singleton in their suit and my own five-card major with opening values - bid it, do not defend a contract I cannot beat"
        establishes: { forcing: non_forcing, agreed_suit: H }
      - id: balhigh_rebid_S5
        call: 5S
        priority: 33.0
        when: { my_suit: S, standing_bid_level: [5], cheapest_in_suit: true, we_hold_contract: false }
        requires:
          suits: { S: [5, 13] }
          evals: { total_points: [15, 40], standing_suit_length: [0, 1] }
        shows: "over their five-level preempt: a void or singleton in their suit and my own five-card major with opening values - bid it, do not defend a contract I cannot beat"
        establishes: { forcing: non_forcing, agreed_suit: S }
      - id: balhigh_lott_push_H
        call: 4H
        priority: 32.5
        when: { partner_suit: H, is_competitive: true, i_have_acted: true, we_hold_contract: false }
        requires:
          suits: { H: [5, 13] }
          evals: { "lott_total_trumps(H)": [10, 26], their_fit: [7, 26], total_points: [6, 40] }
        shows: "the Law push after they compete one more: my raise already showed the hand, ten trumps our way and eight theirs, so nobody sells out at the three level"
        establishes: { forcing: non_forcing, agreed_suit: H }
      - id: balhigh_lott_push_S
        call: 4S
        priority: 32.5
        when: { partner_suit: S, is_competitive: true, i_have_acted: true, we_hold_contract: false }
        requires:
          suits: { S: [5, 13] }
          evals: { "lott_total_trumps(S)": [10, 26], their_fit: [7, 26], total_points: [6, 40] }
        shows: "the Law push after they compete one more: my raise already showed the hand, ten trumps our way and eight theirs, so nobody sells out at the three level"
        establishes: { forcing: non_forcing, agreed_suit: S }
      - id: balhigh_raise_lott4_C
        call: 4C
        priority: 31.9
        when: { partner_suit: C, is_competitive: true, i_have_acted: true, we_hold_contract: false }
        requires:
          suits: { C: [4, 13] }
          evals: { "lott_total_trumps(C)": [9, 26], their_fit: [7, 26], total_points: [6, 40] }
        shows: "the Law at the four level in our agreed minor: ten trumps our way and they have a fit too"
        establishes: { forcing: non_forcing, agreed_suit: C }
      - id: balhigh_raise_lott4_D
        call: 4D
        priority: 31.9
        when: { partner_suit: D, is_competitive: true, i_have_acted: true, we_hold_contract: false }
        requires:
          suits: { D: [4, 13] }
          evals: { "lott_total_trumps(D)": [9, 26], their_fit: [7, 26], total_points: [6, 40] }
        shows: "the Law at the four level in our agreed minor: ten trumps our way and they have a fit too"
        establishes: { forcing: non_forcing, agreed_suit: D }
      - id: balhigh_raise_lott3_H
        call: 3H
        priority: 30.6
        when: { partner_suit: H, cheapest_in_suit: true, is_competitive: true, we_hold_contract: false }
        requires:
          suits: { H: [4, 13] }
          evals: { "lott_total_trumps(H)": [9, 26], their_fit: [7, 26], total_points: [5, 40] }
        shows: "the Law at the three level: they have found a fit and so have we, nine-plus trumps our way"
        establishes: { forcing: non_forcing, agreed_suit: H }
      - id: balhigh_raise_lott3_S
        call: 3S
        priority: 30.6
        when: { partner_suit: S, cheapest_in_suit: true, is_competitive: true, we_hold_contract: false }
        requires:
          suits: { S: [4, 13] }
          evals: { "lott_total_trumps(S)": [9, 26], their_fit: [7, 26], total_points: [5, 40] }
        shows: "the Law at the three level: they have found a fit and so have we, nine-plus trumps our way"
        establishes: { forcing: non_forcing, agreed_suit: S }
      - id: balhigh_raise_lott3_C
        call: 3C
        priority: 30.55
        when: { partner_suit: C, cheapest_in_suit: true, is_competitive: true, we_hold_contract: false }
        requires:
          suits: { C: [4, 13] }
          evals: { "lott_total_trumps(C)": [9, 26], their_fit: [7, 26], total_points: [5, 40] }
        shows: "the Law at the three level in a minor: they have found a fit and so have we, nine-plus trumps our way"
        establishes: { forcing: non_forcing, agreed_suit: C }
      - id: balhigh_raise_lott3_D
        call: 3D
        priority: 30.55
        when: { partner_suit: D, cheapest_in_suit: true, is_competitive: true, we_hold_contract: false }
        requires:
          suits: { D: [4, 13] }
          evals: { "lott_total_trumps(D)": [9, 26], their_fit: [7, 26], total_points: [5, 40] }
        shows: "the Law at the three level in a minor: they have found a fit and so have we, nine-plus trumps our way"
        establishes: { forcing: non_forcing, agreed_suit: D }
      - id: balhigh_rebid_lott3_H
        call: 3H
        priority: 30.5
        when: { my_suit: H, cheapest_in_suit: true, is_competitive: true, partner_has_acted: true,
                we_hold_contract: false }
        requires:
          suits: { H: [4, 13] }
          evals: { "lott_total_trumps(H)": [9, 26], total_points: [11, 40] }
        shows: "competing to the level of our own nine-card heart fit after they balance"
        establishes: { forcing: non_forcing, agreed_suit: H }
      - id: balhigh_rebid_lott3_S
        call: 3S
        priority: 30.5
        when: { my_suit: S, cheapest_in_suit: true, is_competitive: true, partner_has_acted: true,
                we_hold_contract: false }
        requires:
          suits: { S: [4, 13] }
          evals: { "lott_total_trumps(S)": [9, 26], total_points: [11, 40] }
        shows: "competing to the level of our own nine-card spade fit after they balance"
        establishes: { forcing: non_forcing, agreed_suit: S }
      # ---------------------------------------------------------------
      # DISCIPLINE PASSES.  `balhigh_pass_repeat_$X` and
      # `balhigh_pass_silent_partner` both carry `longest_suit_length` or
      # HCP ceilings that keep them off the hands the solo-rebid rungs
      # below describe, so the two families never contend.
      # ---------------------------------------------------------------
      - id: balhigh_pass_repeat_C
        call: P
        priority: 30.1
        when: { my_suit: C, i_have_acted: true, standing_bid_level: [4], we_hold_contract: false }
        requires:
          hcp: [0, 11]
          evals: { quick_tricks: [0, 2] }
        shows: "I have already shown this suit and partner could not raise it: at the four level I defend"
        establishes: { forcing: sign_off }
      - id: balhigh_pass_repeat_D
        call: P
        priority: 30.1
        when: { my_suit: D, i_have_acted: true, standing_bid_level: [4], we_hold_contract: false }
        requires:
          hcp: [0, 11]
          evals: { quick_tricks: [0, 2] }
        shows: "I have already shown this suit and partner could not raise it: at the four level I defend"
        establishes: { forcing: sign_off }
      - id: balhigh_pass_repeat_H
        call: P
        priority: 30.1
        when: { my_suit: H, i_have_acted: true, standing_bid_level: [4], we_hold_contract: false }
        requires:
          hcp: [0, 11]
          evals: { quick_tricks: [0, 2] }
        shows: "I have already shown this suit and partner could not raise it: at the four level I defend"
        establishes: { forcing: sign_off }
      - id: balhigh_pass_repeat_S
        call: P
        priority: 30.1
        when: { my_suit: S, i_have_acted: true, standing_bid_level: [4], we_hold_contract: false }
        requires:
          hcp: [0, 11]
          evals: { quick_tricks: [0, 2] }
        shows: "I have already shown this suit and partner could not raise it: at the four level I defend"
        establishes: { forcing: sign_off }
      - id: balhigh_doubler_own_C5
        call: 5C
        priority: 30.05
        when: { unbid_suit: C, cheapest_in_suit: true, my_last_call_was_double: true,
                partner_has_acted: false, we_hold_contract: false }
        requires:
          suits: { C: [5, 13] }
          evals: { total_points: [16, 40], ltc: [0, 6], "suit_quality(C)": [2, 9] }
        shows: "the doubler bids his own suit at the five level: five losers and a strong suit, the double is still working"
        establishes: { forcing: non_forcing, agreed_suit: C }
      - id: balhigh_doubler_own_D5
        call: 5D
        priority: 30.05
        when: { unbid_suit: D, cheapest_in_suit: true, my_last_call_was_double: true,
                partner_has_acted: false, we_hold_contract: false }
        requires:
          suits: { D: [5, 13] }
          evals: { total_points: [16, 40], ltc: [0, 6], "suit_quality(D)": [2, 9] }
        shows: "the doubler bids his own suit at the five level: five losers and a strong suit, the double is still working"
        establishes: { forcing: non_forcing, agreed_suit: D }
      - id: balhigh_doubler_own_H5
        call: 5H
        priority: 30.05
        when: { unbid_suit: H, cheapest_in_suit: true, my_last_call_was_double: true,
                partner_has_acted: false, we_hold_contract: false }
        requires:
          suits: { H: [5, 13] }
          evals: { total_points: [16, 40], ltc: [0, 6], "suit_quality(H)": [2, 9] }
        shows: "the doubler bids his own suit at the five level: five losers and a strong suit, the double is still working"
        establishes: { forcing: non_forcing, agreed_suit: H }
      # ---------------------------------------------------------------
      # A seven-card minor and a six-card major have no four-level rebid
      # when partner never had room to speak.  Banded at 14+ so the
      # disciplinary passes below cannot reach them.
      # ---------------------------------------------------------------
      - id: balhigh_rebid_solo_H4
        call: 4H
        priority: 29.6
        when: { my_suit: H, cheapest_in_suit: true, partner_has_acted: false,
                i_have_acted: true, we_hold_contract: false }
        requires:
          suits: { H: [6, 13] }
          evals: { total_points: [14, 40], "suit_quality(H)": [1.5, 9] }
        shows: "rebidding my own long hearts at the four level in the passout seat: partner never had room to speak"
        establishes: { forcing: non_forcing, agreed_suit: H }
      - id: balhigh_rebid_solo_S4
        call: 4S
        priority: 29.6
        when: { my_suit: S, cheapest_in_suit: true, partner_has_acted: false,
                i_have_acted: true, we_hold_contract: false }
        requires:
          suits: { S: [6, 13] }
          evals: { total_points: [14, 40], "suit_quality(S)": [1.5, 9] }
        shows: "rebidding my own long spades at the four level in the passout seat: partner never had room to speak"
        establishes: { forcing: non_forcing, agreed_suit: S }
      - id: balhigh_rebid_solo_C4
        call: 4C
        priority: 29.55
        when: { my_suit: C, cheapest_in_suit: true, partner_has_acted: false,
                i_have_acted: true, we_hold_contract: false }
        requires:
          suits: { C: [7, 13] }
          evals: { total_points: [14, 40], "suit_quality(C)": [1.5, 9] }
        shows: "a seven-card club suit named again at the four level: a trump proposal, not a competitive noise bid"
        establishes: { forcing: non_forcing, agreed_suit: C }
      - id: balhigh_rebid_solo_D4
        call: 4D
        priority: 29.55
        when: { my_suit: D, cheapest_in_suit: true, partner_has_acted: false,
                i_have_acted: true, we_hold_contract: false }
        requires:
          suits: { D: [7, 13] }
          evals: { total_points: [14, 40], "suit_quality(D)": [1.5, 9] }
        shows: "a seven-card diamond suit named again at the four level: a trump proposal, not a competitive noise bid"
        establishes: { forcing: non_forcing, agreed_suit: D }
      - id: balhigh_pass_declined_C
        call: P
        priority: 29.5
        when: { my_suit: C, partner_suit: C, we_bid_last: false, partner_has_acted: true,
                i_have_acted: true, their_last_bid_suit: true, standing_bid_level: [3],
                we_hold_contract: false }
        requires:
          suits: { C: [5, 6] }
          evals: { total_points: [0, 14] }
        shows: "partner has already passed their three-level bid holding the values he showed: the four level is his decision, and I have no unshown seventh trump and no extra values"
        establishes: { forcing: sign_off }
      - id: balhigh_pass_declined_D
        call: P
        priority: 29.5
        when: { my_suit: D, partner_suit: D, we_bid_last: false, partner_has_acted: true,
                i_have_acted: true, their_last_bid_suit: true, standing_bid_level: [3],
                we_hold_contract: false }
        requires:
          suits: { D: [5, 6] }
          evals: { total_points: [0, 14] }
        shows: "partner has already passed their three-level bid holding the values he showed: the four level is his decision, and I have no unshown seventh trump and no extra values"
        establishes: { forcing: sign_off }
      - id: balhigh_pass_declined_H
        call: P
        priority: 29.5
        when: { my_suit: H, partner_suit: H, we_bid_last: false, partner_has_acted: true,
                i_have_acted: true, their_last_bid_suit: true, standing_bid_level: [3],
                we_hold_contract: false }
        requires:
          suits: { H: [5, 6] }
          evals: { total_points: [0, 14] }
        shows: "partner has already passed their three-level bid holding the values he showed: the four level is his decision, and I have no unshown seventh trump and no extra values"
        establishes: { forcing: sign_off }
      - id: balhigh_pass_declined_S
        call: P
        priority: 29.5
        when: { my_suit: S, partner_suit: S, we_bid_last: false, partner_has_acted: true,
                i_have_acted: true, their_last_bid_suit: true, standing_bid_level: [3],
                we_hold_contract: false }
        requires:
          suits: { S: [5, 6] }
          evals: { total_points: [0, 14] }
        shows: "partner has already passed their three-level bid holding the values he showed: the four level is his decision, and I have no unshown seventh trump and no extra values"
        establishes: { forcing: sign_off }
      - id: balhigh_pass_silent_partner
        call: P
        priority: 29.4
        when: { partner_has_acted: false, side_has_acted: true, we_hold_contract: false }
        requires:
          hcp: [0, 15]
          evals: { longest_suit_length: [0, 5] }
        shows: "partner has never bid, we have no known fit and I have no long suit of my own: their contract stands"
        establishes: { forcing: sign_off }
      - id: balhigh_rebid_solo_H3
        call: 3H
        priority: 29.05
        when: { my_suit: H, cheapest_in_suit: true, partner_has_acted: false, we_hold_contract: false }
        requires:
          suits: { H: [6, 13] }
          evals: { total_points: [17, 40], "suit_quality(H)": [1, 9] }
        shows: "rebidding my own six-card hearts at the three level opposite a silent partner: extra values, not just extra shape"
        establishes: { forcing: non_forcing }
      - id: balhigh_rebid_solo_S3
        call: 3S
        priority: 29.05
        when: { my_suit: S, cheapest_in_suit: true, partner_has_acted: false, we_hold_contract: false }
        requires:
          suits: { S: [6, 13] }
          evals: { total_points: [17, 40], "suit_quality(S)": [1, 9] }
        shows: "rebidding my own six-card spades at the three level opposite a silent partner: extra values, not just extra shape"
        establishes: { forcing: non_forcing }
      - id: balhigh_defend_their_nt
        call: P
        priority: 28.5
        when: { standing_bid_strain: [NT], we_hold_contract: false }
        requires:
          evals: { quick_tricks: [2, 13] }
        shows: "they bid notrump and it is passed round to me with two quick tricks: defend, do not run to the four level"
        establishes: { forcing: sign_off }
        negative_inference_weight: soft
      - id: balhigh_pref_C3
        call: 3C
        priority: 28.4
        when: { partner_suit: C, cheapest_in_suit: true, is_competitive: true,
                i_have_acted: true, we_hold_contract: false }
        requires:
          suits: { C: [4, 13] }
          evals: { total_points: [10, 40] }
        shows: "returning to partner's clubs with four-card support when they have taken the auction up"
        establishes: { forcing: non_forcing, agreed_suit: C }
      - id: balhigh_pref_D3
        call: 3D
        priority: 28.4
        when: { partner_suit: D, cheapest_in_suit: true, is_competitive: true,
                i_have_acted: true, we_hold_contract: false }
        requires:
          suits: { D: [4, 13] }
          evals: { total_points: [10, 40] }
        shows: "returning to partner's diamonds with four-card support when they have taken the auction up"
        establishes: { forcing: non_forcing, agreed_suit: D }

#== RULES general_their_double
      # ---------------------------------------------------------------
      # `xd_pass` fires 88 times at -1.72: this context has no four-level
      # raise of ANY kind, so when partner preempts and they double the
      # only 4M candidate is the code fallback.  The four-level Law raise
      # below is the whole point of this block.
      # ---------------------------------------------------------------
      - id: xd_jump_own_C
        call: 3C
        priority: 34.5
        when: { we_bid_last: true, my_suit: C, cheapest_in_suit: false, partner_has_acted: false }
        requires:
          suits: { C: [6, 13] }
          evals: { total_points: [17, 40] }
          features: [ "three_of_top5(C)" ]
        shows: "jump rebid of my own doubled clubs: a six-card suit I can play opposite nothing, 17+ - the extras partner's pass denied"
        establishes: { forcing: non_forcing }
      - id: xd_jump_own_D
        call: 3D
        priority: 34.5
        when: { we_bid_last: true, my_suit: D, cheapest_in_suit: false, partner_has_acted: false }
        requires:
          suits: { D: [6, 13] }
          evals: { total_points: [17, 40] }
          features: [ "three_of_top5(D)" ]
        shows: "jump rebid of my own doubled diamonds: a six-card suit I can play opposite nothing, 17+ - the extras partner's pass denied"
        establishes: { forcing: non_forcing }
      - id: xd_jump_own_H
        call: 3H
        priority: 34.5
        when: { we_bid_last: true, my_suit: H, cheapest_in_suit: false, partner_has_acted: false }
        requires:
          suits: { H: [6, 13] }
          evals: { total_points: [17, 40] }
          features: [ "three_of_top5(H)" ]
        shows: "jump rebid of my own doubled hearts: a six-card suit I can play opposite nothing, 17+ - the extras partner's pass denied"
        establishes: { forcing: non_forcing }
      - id: xd_jump_own_S
        call: 3S
        priority: 34.5
        when: { we_bid_last: true, my_suit: S, cheapest_in_suit: false, partner_has_acted: false }
        requires:
          suits: { S: [6, 13] }
          evals: { total_points: [17, 40] }
          features: [ "three_of_top5(S)" ]
        shows: "jump rebid of my own doubled spades: a six-card suit I can play opposite nothing, 17+ - the extras partner's pass denied"
        establishes: { forcing: non_forcing }
      - id: xd_raise_lott4_C
        call: 4C
        priority: 33.0
        when: { we_bid_last: true, we_hold_contract: false, partner_suit: C }
        requires:
          suits: { C: [4, 13] }
          any_of:
            - evals: { "lott_total_trumps(C)": [10, 26], total_points: [5, 40] }
            - evals: { "lott_total_trumps(C)": [8, 26], total_points: [12, 40] }
        shows: "the Law after they double: ten combined trumps make four of the suit our level whether it makes or it is a save"
        establishes: { forcing: non_forcing, agreed_suit: C }
      - id: xd_raise_lott4_D
        call: 4D
        priority: 33.0
        when: { we_bid_last: true, we_hold_contract: false, partner_suit: D }
        requires:
          suits: { D: [4, 13] }
          any_of:
            - evals: { "lott_total_trumps(D)": [10, 26], total_points: [5, 40] }
            - evals: { "lott_total_trumps(D)": [8, 26], total_points: [12, 40] }
        shows: "the Law after they double: ten combined trumps make four of the suit our level whether it makes or it is a save"
        establishes: { forcing: non_forcing, agreed_suit: D }
      - id: xd_raise_lott4_H
        call: 4H
        priority: 33.0
        when: { we_bid_last: true, we_hold_contract: false, partner_suit: H }
        requires:
          suits: { H: [3, 13] }
          any_of:
            - evals: { "lott_total_trumps(H)": [10, 26], total_points: [5, 40] }
            - evals: { "lott_total_trumps(H)": [8, 26], total_points: [12, 40] }
        shows: "the Law after they double: ten combined trumps make four of the major our level whether it makes or it is a save"
        establishes: { forcing: non_forcing, agreed_suit: H }
      - id: xd_raise_lott4_S
        call: 4S
        priority: 33.0
        when: { we_bid_last: true, we_hold_contract: false, partner_suit: S }
        requires:
          suits: { S: [3, 13] }
          any_of:
            - evals: { "lott_total_trumps(S)": [10, 26], total_points: [5, 40] }
            - evals: { "lott_total_trumps(S)": [8, 26], total_points: [12, 40] }
        shows: "the Law after they double: ten combined trumps make four of the major our level whether it makes or it is a save"
        establishes: { forcing: non_forcing, agreed_suit: S }
      # Three small trumps in a completely flat hand is not a raise: it
      # only tells them how high to bid.  Priced above `xd_raise_$m2` (30)
      # and below `xd_raise_$m3` (31), so a real raise is untouched.
      - id: xd_pass_flat_C
        call: P
        priority: 30.5
        when: { we_bid_last: true, we_hold_contract: false, partner_suit: C }
        requires:
          suits: { C: [0, 3] }
          shapes: [ "4333" ]
          evals: { total_points: [0, 10] }
        shows: "three small trumps in a completely flat hand: no ruffing value, so do not tell them how high to bid"
        establishes: { forcing: non_forcing }
      - id: xd_pass_flat_D
        call: P
        priority: 30.5
        when: { we_bid_last: true, we_hold_contract: false, partner_suit: D }
        requires:
          suits: { D: [0, 3] }
          shapes: [ "4333" ]
          evals: { total_points: [0, 10] }
        shows: "three small trumps in a completely flat hand: no ruffing value, so do not tell them how high to bid"
        establishes: { forcing: non_forcing }
      # They doubled our own agreed partscore: a minimum passes rather
      # than running to a new suit.  Outranks `xd_second_$X2/3` (25/26).
      - id: xd_pass_agreed_C
        call: P
        priority: 26.5
        when: { my_suit: C, partner_suit: C, we_bid_last: true, we_hold_contract: true }
        requires:
          evals: { total_points: [0, 16] }
        shows: "they doubled our agreed clubs: a minimum passes rather than running to a new suit"
        establishes: { forcing: non_forcing, agreed_suit: C }
      - id: xd_pass_agreed_D
        call: P
        priority: 26.5
        when: { my_suit: D, partner_suit: D, we_bid_last: true, we_hold_contract: true }
        requires:
          evals: { total_points: [0, 16] }
        shows: "they doubled our agreed diamonds: a minimum passes rather than running to a new suit"
        establishes: { forcing: non_forcing, agreed_suit: D }
      - id: xd_pass_agreed_H
        call: P
        priority: 26.5
        when: { my_suit: H, partner_suit: H, we_bid_last: true, we_hold_contract: true }
        requires:
          evals: { total_points: [0, 16] }
        shows: "they doubled our agreed hearts: a minimum passes rather than running to a new suit"
        establishes: { forcing: non_forcing, agreed_suit: H }
      - id: xd_pass_agreed_S
        call: P
        priority: 26.5
        when: { my_suit: S, partner_suit: S, we_bid_last: true, we_hold_contract: true }
        requires:
          evals: { total_points: [0, 16] }
        shows: "they doubled our agreed spades: a minimum passes rather than running to a new suit"
        establishes: { forcing: non_forcing, agreed_suit: S }
      - id: xd_nt_extras
        call: 3NT
        priority: 23.5
        when: { we_bid_last: true, we_hold_contract: false }
        requires:
          evals: { total_points: [18, 40], semi_balanced: [1, 1] }
        shows: "extra values and a balanced hand: bidding the notrump game through their double rather than passing partner's call around"
        establishes: { forcing: sign_off }

#== RULES general_pull_or_sit
      # ---------------------------------------------------------------
      # `adx_neg_major_$M2` and `adx_neg_major_$M3` carry IDENTICAL gates
      # at priority 62, so the jump answer to the negative double is dead.
      # These are the rungs that discriminate.  Both are `non_forcing`,
      # not invitational: the doubler is capped by his own negative double,
      # so a pass is a complete answer and no seat can be starved.
      # ---------------------------------------------------------------
      - id: adx_pull_game_H
        call: 4H
        priority: 63.0
        when: { my_suit: H, partner_suit: H }
        requires:
          suits: { H: [6, 13] }
          evals: { "lott_total_trumps(H)": [9, 26], total_points: [10, 40] }
        shows: "partner's double showed support for my own hearts: six trumps opposite three is a nine-card fit, so the pull is to game"
        establishes: { forcing: sign_off, agreed_suit: H }
      - id: adx_pull_game_S
        call: 4S
        priority: 63.0
        when: { my_suit: S, partner_suit: S }
        requires:
          suits: { S: [6, 13] }
          evals: { "lott_total_trumps(S)": [9, 26], total_points: [10, 40] }
        shows: "partner's double showed support for my own spades: six trumps opposite three is a nine-card fit, so the pull is to game"
        establishes: { forcing: sign_off, agreed_suit: S }
      - id: adx_neg_major_jump_H
        call: 3H
        priority: 62.8
        when: { unbid_suit: H, their_last_bid_suit: true, i_have_acted: true, cheapest_in_suit: false }
        requires:
          suits: { H: [5, 13] }
          hcp: [16, 40]
        shows: "jump answer to the negative double: a five-card heart suit and a maximum, so partner can raise to game and stop"
        establishes: { forcing: non_forcing, agreed_suit: H }
      - id: adx_neg_major_jump_S
        call: 3S
        priority: 62.8
        when: { unbid_suit: S, their_last_bid_suit: true, i_have_acted: true, cheapest_in_suit: false }
        requires:
          suits: { S: [5, 13] }
          hcp: [16, 40]
        shows: "jump answer to the negative double: a five-card spade suit and a maximum, so partner can raise to game and stop"
        establishes: { forcing: non_forcing, agreed_suit: S }
      # ---------------------------------------------------------------
      # `adx_sit` demands `their_last_bid_suit`, so it can never sit for a
      # double of NOTRUMP - the answering seat for the penalty double of
      # their 1NT overcall (`cl_penalty_X_over_nt`) did not exist.  This
      # rung is NOT `requires: {}`: a bust still runs, at `adx_pull_weak`.
      # ---------------------------------------------------------------
      - id: adx_sit_nt
        call: P
        priority: 62.5
        when: { standing_bid_strain: [NT], i_have_acted: true }
        requires:
          evals: { total_points: [8, 40] }
        shows: "partner's double of their notrump is for penalty: I have bid my hand and hold my share of the pack, so I sit for it"
        establishes: { forcing: sign_off }
      - id: adx_sit_four
        call: P
        priority: 61.5
        when: { their_last_bid_suit: true, standing_bid_level: [1] }
        requires:
          evals: { standing_suit_length: [4, 13], total_points: [10, 40] }
        shows: "sitting the double at the one level: four trumps behind the opener and defensive values - four small is the whole credential"
        establishes: { forcing: sign_off }
      # A four-card major at the three level beats a longer minor at the
      # four.  `adx_pull_S3` compares raw suit lengths and loses the major.
      - id: adx_pull_major_H3
        call: 3H
        priority: 58.6
        when: { unbid_suit: H, cheapest_in_suit: true, their_last_bid_suit: true, i_have_acted: false }
        requires:
          suits: { H: [4, 13] }
          evals: { total_points: [0, 11] }
        shows: "answering the takeout double with a four-card major at the three level rather than a longer minor at the four"
        establishes: { forcing: non_forcing }
      - id: adx_pull_major_S3
        call: 3S
        priority: 58.6
        when: { unbid_suit: S, cheapest_in_suit: true, their_last_bid_suit: true, i_have_acted: false }
        requires:
          suits: { S: [4, 13] }
          evals: { total_points: [0, 11] }
        shows: "answering the takeout double with a four-card major at the three level rather than a longer minor at the four"
        establishes: { forcing: non_forcing }
      # Running from partner's double of their notrump with a bust.
      - id: adx_pull_weak_H2
        call: 2H
        priority: 53.0
        when: { unbid_suit: H, cheapest_in_suit: true, standing_bid_strain: [NT] }
        requires:
          suits: { H: [5, 13] }
          evals: { total_points: [0, 8] }
        shows: "running from partner's double of their notrump: a five-card suit is a better trump suit than a bust is a defence"
        establishes: { forcing: sign_off }
      - id: adx_pull_weak_S2
        call: 2S
        priority: 53.0
        when: { unbid_suit: S, cheapest_in_suit: true, standing_bid_strain: [NT] }
        requires:
          suits: { S: [5, 13] }
          evals: { total_points: [0, 8] }
        shows: "running from partner's double of their notrump: a five-card suit is a better trump suit than a bust is a defence"
        establishes: { forcing: sign_off }
