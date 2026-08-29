# Expert review B — seed 626262, clusters 11–20 + worst singles from #16 on

Reviewer: external 2/1 coach. Working tree left clean; every experiment run against
`/tmp/.../scratchpad/fix.yaml` (a scratch copy) via `system_path`.
Every board indicted below was reproduced with `choose_bid`; flips were re-verified
against the patched scratch copy where noted **[VERIFIED FLIP]**.

---

## 0. Three cross-cutting mechanisms (read this first)

**(A) The RKC continuations were fixed for the majors and not for the minors, and the
5H branch still ignores the queen the reply just denied.** Cluster 13, cluster 16,
single 686, and (other slice) cluster 6 are all one machine. Detail in §1.

**(B) "Capped at 18/19 because slam belongs to the keycard rules" created ceilings
with nothing above them.** Several responder-rebid ladders now top out at 18, and the
promised escape (`gst_rkc_*`) is *unreachable* from those seats: `gst_rkc_*` carries
`when: { partner_last_suit: <suit>, standing_bid_level: [2,3,4] }` plus
`suits: { <suit>: [3,13] }`. After `1m–1M–1NT`, `1m–1H–1S`, `1m–1M–2m` the standing
bid is at the ONE or TWO level in a suit the big hand usually doesn't hold three of, so
no 4NT candidate is ever generated. A 19–21 count therefore falls off the top of the
ladder into a soft-miss lottery. Boards 142, 578, 729, 296 (45 IMPs in my slice alone;
also 445/493 in the other slice).

**(C) High-priority "toolkit" doubles and pulls beat perfectly-fitting quiet calls.**
On boards 200 / 618 / 706 / 734 / 761 / 980 the *correct* call (`P`, or the sit rule
`adx_pass_min`) scored `match 1.0` and lost the priority race to a double or a pull
whose own gate was a soft miss. `ch_penalty_X` (prio 38) and `adx_pull_*` (prio 54–58)
are the two offenders; both need hard gates, not softer bands. 58 IMPs in my slice.

---

## 1. THE SLAM MACHINERY (clusters 13, 15, 16 + singles 686, 782; read-out on 6/7)

### CLUSTER 13 `rkc5H_slam` — 2 boards, 24 IMPs — **IMPLEMENTATION-BUG**

Mechanism. The 5H reply is an exact statement: *2 keycards and NO trump queen.* The
asker's arithmetic after it is therefore complete. `rkc5H_slam` clause 1
(`keycards(agreed): [3,5]`) bids six on the keycard count alone and never re-reads the
denial of the queen or counts trumps.

* **Board 790 (−11), verified.** W `KJT8.AJ874.AQ8.T` after `1H-2D-2S-3S-4NT-5H`:
  `keycards(S)=3, trump_queen(S)=0, lott_total_trumps(S)=7`. All five keycards are
  present, the queen is known missing and the fit is **seven cards**. Engine bids 6S,
  down one. Book: 5S.
* **Board 126 (−13), verified.** W `Q52.A.AQ32.AKQJ7`: `keycards=3, trump_queen=1,
  lott=8(real 10)`. Every keycard *and* the queen are accounted for — this is a grand
  slam auction and there is no 5NT in the system (see §1d). Engine bids 6S; 7S was cold.

Second-order bug found while testing: `rkc5H_signoff` requires `keycards [0,2]`, and
`keycards` is a **sharp** evaluator (σ²=0.05). With 3 keycards the sign-off scores ~0,
so once clause 1 is tightened the context has *no* positive candidate and 6S wins the
priority race anyway. The sign-off must be the open residual.

Fix (exact):
```yaml
      - id: rkc5H_slam
        requires:
          any_of:
            - evals: { "keycards(agreed)": [2, 5], "trump_queen(agreed)": [1, 1] }
            - evals: { "keycards(agreed)": [2, 5], "lott_total_trumps(agreed)": [10, 26] }
      - id: rkc5H_signoff
        requires: {}          # was: evals: { "keycards(agreed)": [0, 2] }
```
**[VERIFIED FLIP]** 790 → 5S; 126 → 6S unchanged.
Endangers: 2+2 slams in a nine-card fit where the asker holds the queen — unchanged
(clause 1 still fires). It gives up 5-keycard slams in a 7–8 card fit missing the
queen, which is the point.

### CLUSTER 15 `cue_S_signoff` — 2 boards, 24 IMPs — **two different defects**

* **Board 279 (−13) — IMPLEMENTATION-BUG in `gf_pref_3$M`.** Auction
  `1D-1H-1S-2C(FSF)-2NT-?`. S holds `A7.AQ865.KQJ4.T3` — **two** spades and five
  hearts. `gf_pref_3$M` requires `suits: {$M:[3,13]}` *softly*, so a doubleton scores
  ~0.35 and still wins at priority 37; nothing in the GF-landing family lets responder
  **re-show his own five-card major** (`gf_new_3$X` is gated `when: { unbid_suit: $X }`
  and hearts are not unbid). Result: 3S → 4S in a 4–2 fit, eight tricks; 4H was there
  (11 tricks at the other table). Verified: engine chooses 3S with `A7`.
  Fix — two edits in `gf_landing_*`:
  ```yaml
      - id: gf_pref_3$M
        requires:
          suits: { $M: [3, 13] }
          not: { suits: { $M: [0, 2] } }        # negation is sharp: hard-blocks 2 or fewer
  ```
  and a new sibling context (priority 38, above `gf_pref`):
  ```yaml
  - id: gf_landing_own_major
    expand: { M: [H, S] }
    pattern: "... - P - ?"
    when: { agreed_suit: false, game_forced: true }
    rules:
      - id: gf_own_3$M
        call: 3$M
        priority: 38
        when: { i_bid_suit: $M, cheapest_in_suit: true }
        requires: { suits: { $M: [5, 13] } }
        shows: "re-showing my own five-card major in the game force"
        establishes: { forcing: game_forcing }
  ```
* **Board 711 (−11) — MISSING-AGREEMENT.** `1S-2NT-3C(shortness)-4C(cue)-4S`. W's 4S is
  an *honest* denial (no diamond control). E then holds `T962.T87.AKQT.A3` — four
  trumps, AKQ tight opposite partner's known 4th diamond, the club ace — and **passes
  by `fallback`**: the only candidate above zero was 4NT at fit 0.018. There is no
  "cue-bidder's second move over partner's return to game" rule. 6S was cold.
  Fix: in the `cue_bidding_S` context add
  ```yaml
      - id: cue_S_reraise_4NT
        call: 4NT
        priority: 44
        when: { partner_last_bid: 4S, i_cued: true }
        requires:
          evals: { controls: [5, 12], "keycards(agreed)": [2, 5], "lott_total_trumps(agreed)": [9, 26] }
        shows: "I cued and partner returned to game: my extras justify the keycard ask"
        establishes: { forcing: one_round, asking: keycards }
  ```
  (if `i_cued` is not an available `when:` key, gate on `standing_bid_level: [4]` +
  `agreed_suit: S` + `we_bid_last: false` and require `controls: [5,12]`.)

### CLUSTER 16 `rkc5C_signoff` — 2 boards, 24 IMPs — **NEEDS-EXCEPTION on the ASK**

Both boards are the same disaster: 4NT asked, `5C` reply (= 1 keycard), two keycards
missing, forced sign-off at **5M above a making 4M**. In both the asker held exactly
**two** keycards, so the 5C reply was always going to be fatal.

* **Board 601 (−12), verified.** E `KJ3.AKJT6.KQ43.K` after `1H-1S-2H-3S`:
  `hcp 20, total_points 23, controls 6, keycards(H) 2, lott 8, rule_of_26 = 31.0` —
  *exactly* on the sharp `[31,99]` boundary. Note where the 23 comes from: the
  **singleton club KING** is worth 3 HCP *and* 3 shortness points = 6 points for one
  card. Partner's box is `hcp 0–40, min_total_points 6` (a competitive single raise),
  so `partner_mid = 8`. Real combined values: 25 HCP. 5H went one down; 4H made.
* **Board 973 (−12), verified.** N `AQ87.JT42.AK73.5` after `1C-1H-3H`: `keycards(H) 2,
  controls 5, rule_of_26 35`. Genuine 31 combined — but three keycards between the
  hands. 5H down one; 4H made at the other table.

Mechanism. `gst_rkc_*` gates on *values* (`total_points`, `controls`, `rule_of_26`) and
on the *fit* (`lott ≥ 8`) but **never on the asker's own keycard count**. With two
keycards in hand the 5C reply forces the partnership to the five level missing two —
Kantar's first law of Blackwood ("don't ask a question whose answer you can't stand")
in its purest form.

Fix (all four `gst_rkc_*`, and `rkc_4NT`):
```yaml
          any_of:
            # 3+ keycards: no reply can leave two missing
            - evals: { "keycards(<suit>)": [3, 5] }
            # exactly 2: only ask when 5-of-the-suit is a safe landing, i.e. a
            # big fit or a partner who has promised real values
            - evals: { "keycards(<suit>)": [2, 2], "lott_total_trumps(<suit>)": [10, 26] }
            - evals: { "keycards(<suit>)": [2, 2], rule_of_26_sharp: [33, 99] }
```
Boards recovered: 601, 973 (24). Endangers: 2-keycard asks opposite a big fit still
work; it removes the 2-keycard ask opposite a limited raise, which is exactly the
losing population here. Measure this one on its own run.

### 1d. **MISSING-AGREEMENT: the system cannot bid a grand slam.**

`grep "5NT" two_over_one.yaml` returns only the five minor-suit *sign-off* rules; there
is no kings-ask and no 7-level placement anywhere. Boards where BEN bid seven and we
bid six or four: **126 (−13, mine)**, 847 (−17), 498 (−14), 7 (−14), 913 (−14) — ~72
IMPs of grand slams across the dossier, none of them reachable in principle.

Fix (minimum viable, in the `rkc_continue_after_5H` / `_5S` contexts):
```yaml
      - id: rkc5H_kings_5NT
        call: 5NT
        priority: 62
        requires:
          evals: { "keycards(agreed)": [3, 5], "trump_queen(agreed)": [1, 1],
                   rule_of_26_sharp: [34, 99] }
        shows: "all five keycards and the queen: asking for kings"
        establishes: { forcing: one_round, asking: kings }
```
plus a `... - 5NT - P - ?` reply context (`6C`=0 kings, `6D`=1, `6H`=2, `6S`=3 — or
step-wise "bid your cheapest king") and an asker context that places 6 or 7. Board 126:
W has `keycards 3 + queen + rule_of_26 35` → 5NT → E shows no king → 7S is still right
on the club suit, so the placement rule should also read `solid_suit`/`controls`.
Endangers: this is the highest-variance addition on the list — gate it hard
(all five keycards *plus* the queen *plus* 34+) and measure alone.

### 1e. `rkc_4NT` has no trump-fit gate at all — **IMPLEMENTATION-BUG (family divergence)**

All four `gst_rkc_*` carry `"lott_total_trumps(<suit>)": [8,26]` and `suits: {<suit>:[3,13]}`.
`rkc_4NT` — the *game-forced, suit-agreed* ask — carries neither.
**Board 919 (−17, cluster 6, other slice, verified):** S `A432.AK75.AJ65.Q` after
`2H-X-3H-3S-4S`, `lott_total_trumps(S) = 6`. The engine asked for keycards and bid **6S
in a 4–3 fit**, ten tricks, while 6D (a nine-card fit) was the par contract.

Fix: add `"lott_total_trumps(agreed)": [8, 26]` to `rkc_4NT.requires.evals`.
**[VERIFIED FLIP]** 919 → the 4NT candidate disappears (engine passes 4S).
Endangers: 2C-positive auctions where partner's *shown* length understates the suit
(board 126 reads lott 8 against a real 10 and survives); if a measured run shows losses,
7 is the safer threshold.

### 1f. The minor-suit RKC continuations never received the major-suit fixes — **IMPLEMENTATION-BUG**

| reply | major rule | minor rule | agree? |
|---|---|---|---|
| 5C (1/4) | `rkc5C_slam` `[3,5]` | `rkc5C_slam_C/_D` `[3,5]` | yes |
| 5D (0/3) | `rkc5D_slam` 2-clause count | `rkc5D_slam_C/_D` 2-clause count | yes |
| 5H (2, no Q) | `rkc5H_slam` 3-clause (fixed last round) | `rkc5H_slam_C/_D` bare `[3,5]` | **NO** |
| 5S (2 + Q) | `rkc5S_slam_S/_H` **`[2,5]`** | `rkc5S_slam_C/_D` **`[3,5]`** | **NO** |

The 5S line is the one that cost real IMPs. **Single 686 (−12), verified:** N
`KQT8.AK2.KJ3.K42` after `1C-1S-2C-4NT-5S`: `keycards(C)=2`, partner has shown 2 + the
club queen ⇒ four keycards, one missing, queen present, eight trumps ⇒ **6C is the book
bid**. `rkc5S_slam_C` demanded 3 in hand, so the hand fell to `rkc5S_signoff_C_nt` →
**5NT** (which also outranks the 6C fallback at 56 vs 55). 6C makes.

Fix: `rkc5S_slam_C` and `rkc5S_slam_D` → `"keycards(agreed)": [2, 5]`;
`rkc5H_slam_C` and `rkc5H_slam_D` → copy the corrected `rkc5H_slam` `any_of` from §1
(and make their `_signoff_C/_D` residuals `requires: {}`).
**[VERIFIED FLIP]** 686 → 6C. Endangers: nothing — this is arithmetic, and the majors
already run on it.

### 1g. Read-out on clusters 6 and 7 (not my verdicts)

* **Cluster 6 `rkc5C_slam` (3 boards, 41 IMPs).** 919 is §1e (4–3 fit, fixed by the lott
  gate). **534** (S `AKJ82.A4.Q3.KQT2`, 1S–3S–4NT–5C–6S, eleven tricks): `keycards(S)=3`,
  partner's 5C = 1 ⇒ four keycards, one missing — bidding six on that count is *normal*
  bridge; what failed is the **values**: 19 + 7 = 26 HCP. `rule_of_26 = 31.5` (see §2).
  **58** (2C–2D–2H–2S–3H–4H–4NT–5C–6H): same shape — 3 keycards, one missing, but 27 HCP.
  I would not touch `rkc5C_slam` (its arithmetic is right); I would tighten the **ask**
  (§ cluster 16 fix, and note both boards pass that fix's `rule_of_26_sharp ≥ 33`
  clause only because of the double-count in §2).
* **Cluster 7 `qr3_4NT_quant` (3 boards, 35 IMPs).** 153 and 763 are hands stopping in
  4NT after a 3NT that should have been passed or driven; 379 is a 4NT quantitative on
  a hand with a seven-card club suit (`A.KT3.J4.AKQ7642`) — a suit hand, not a
  quantitative-raise hand. Suggest the other reviewer add
  `evals: { semi_balanced: [1,1] }` to `qr3_4NT_quant` and check the `qa_*` acceptance
  ladder; it is a *different* disease from the RKC family and should not be bundled
  with these fixes when measuring.

---

## 2. The `rule_of_26` / "31 combined points" question — evidence

The assignment asks whether the 2.5-point-pessimism claim justifies repairing the
estimator and re-measuring the 31 gate. **My boards say the estimator is not the lever,
and repairing only its pessimism would make things worse.** Measured on the six slam
boards in and adjacent to my slice (`rule_of_26` at the decision seat vs. the two hands'
actual total points, and vs. actual combined HCP):

| board | est. `rule_of_26` | actual combined total pts | actual combined HCP | slam? |
|---|---|---|---|---|
| 919 | 33.0 | 33 | 29 | no (4–3 fit) |
| 534 | 31.5 | 31 | 26 | no |
| 973 | 35.0 | 34 | 26 | no |
| 601 | 31.0 | 29 | 25 | no |
| 126 | 35.0 | 36 | 29 | **yes, grand** |
| 790 | 32.0 | 36 | 30 | no (no queen) |

Mean estimator error ≈ **−0.25** — it is *not* systematically pessimistic in these
positions. The claimed pessimism is real but **local to one case**: when partner's box
is an unbounded suit bid (`hcp [12,40]`, board 790), the `floor+4` cap forces
`partner_mid = 14` against a true ~18. When partner has made a *limiting* call —
a single raise, a limit raise, a jump raise, a 1NT rebid, a minor rebid, which is the
population that actually reaches `gst_rkc_*` — `floor = min_total_points`, which
**already contains partner's distributional points**, and the sum then double-counts
the same fit from both sides. Boards 534 and 919 land at 31–33 on 26 and 29 HCP.

The real bug in the estimator is a **units mismatch**, not a bias:
`floor = max(partner_min_hcp, partner_min_points)` mixes an HCP floor with a
total-points floor, and the result is added to *my* `total_points`. Recommended repair
(and it should be measured on its own run, with nothing else in it):
```python
# evaluators.py rule_of_26
hcp_floor  = ctx.partner_min_hcp
pts_floor  = ctx.partner_min_points
# an unbounded suit bid implies ~1.5 distributional points partner has not shown
floor = max(hcp_floor + (1.5 if ctx.partner_max_hcp >= 25 else 0.0), pts_floor)
partner_mid = (floor + min(max(ctx.partner_max_hcp, floor), floor + 4)) / 2
```
**But note the direction of the risk:** this makes `rule_of_26` fire *more* often
opposite unlimited openings, and `rule_of_26` is the acceptance gate on
`cl_raise_H4/S4`, `cl_raise_D4`, `rkc_4NT`, `gst_rkc_*` and (indirectly, through
`total_points`) on `op_lr_game`. Cluster 18 below shows those families already
**over**-bidding. If this repair is made, it must be paired with the `total_points`
fix in §5 (singleton honours) or measured with cluster-18 boards as a tripwire.

The second, larger accounting error is in `total_points` itself: `shortness_points`
credits a singleton **3** regardless of what the card is, and `total_points` uses raw
`hand.hcp` rather than the already-implemented `adjusted_hcp` (which deducts 1 for a
stiff K/Q/J and 0.5 for Qx/Jx). A singleton king is therefore worth **six points**.
Board 601's ask and board 29's game acceptance both fire *exactly on the boundary*
because of a stiff king. One-line fix: `total_points` → `adjusted_hcp(hand, ctx) +
shortness_points(...)` in the fit branch. Board 601: `total_points 23 → 22`,
`rule_of_26 31 → 30` ⇒ ask blocked. Board 29: `14 → 13.5` ⇒ game acceptance blocked.

**Bottom line:** I would *not* re-measure the 31 threshold. The four losing slam boards
in my slice were lost to (i) a 4–3 fit, (ii) a denied trump queen, (iii) three keycards
between the hands, (iv) a minor-suit continuation that never got the major's fix — all
of which are counting facts that no points threshold can express.

---

## 3. Remaining cluster verdicts

### CLUSTER 11 `rr_nt_3NT` — 3 boards, 26 IMPs — **MISSING-AGREEMENT (no New Minor Forcing)**

`responder_rebid_after_1NT_rebid` (`1m – 1M – 1NT – ?`) contains exactly five rungs:
pass / 2NT / 3NT / 4NT-quant / 2M-or-4M-with-six. There is **no checkback**, so
responder with a **five-card major and game values** must blast 3NT and the 5-3 fit is
never found. All three boards are that hand:

* 654 (−13): E `T3.AQJ43.Q985.AQ`, 5 hearts / 15 HCP → 3NT (8 tricks); 4H made 11.
* 328 (−11): S `AQ642.KQ764.T3.Q`, **5-5 majors** / 11 HCP → 3NT (7 tricks); 4S made 10.
* 267 (−2): E `J32.AQT53.84.AK3`, 5 hearts → 3NT; 4H made 12.

Same disease drives cluster 2's 501 (−12) and 970 (−11) in the other slice — BEN's
auctions there are literally `1C-1S-1NT-2D-...-4S`, i.e. NMF. Worth ~50 IMPs total.

Fix — two new contexts (written out for `1D`; mirror for `1C` with `2C`→`2D`):
```yaml
  - id: new_minor_forcing_1D
    description: "Checkback after 1D - 1M - 1NT"
    expand: { M: [H, S] }
    pattern: "1D - P - 1$M - P - 1NT - P - ?"
    rules:
      - id: nmf_1D_2C_$M
        call: 2C
        priority: 58            # above rr_nt_3NT (54) and rr_nt_2NT (52)
        requires:
          evals: { total_points: [11, 18] }
          any_of:
            - suits: { $M: [5, 13] }
            - suits: { H: [4, 4], S: [4, 13] }
        shows: "new minor forcing: 11+, asking for three-card support or a four-card major"
        establishes: { forcing: one_round, asking: checkback }
        alertable: true
        convention: new_minor_forcing

  - id: new_minor_forcing_reply_1D
    expand: { M: [H, S] }
    pattern: "1D - P - 1$M - P - 1NT - P - 2C - P - ?"
    rules:
      - id: nmfr_1D_3$M
        call: 2$M            # raise on the cheapest available step
        priority: 66
        requires: { suits: { $M: [3, 3] } }
        shows: "three-card support for responder's major"
        establishes: { forcing: one_round, agreed_suit: $M }
      - id: nmfr_1D_2NT
        call: 2NT
        priority: 60
        requires: { hcp: [12, 14] }
        shows: "minimum 1NT rebid, no third card in the major"
        establishes: { forcing: one_round }
```
plus responder's placement (`3NT` with no fit, `4$M` with the fit). Endangers: 2C now
carries an artificial meaning after `1D-1M-1NT`, so any natural club rebid there must
be re-routed (there is none in the current ladder — check `lint --only collide`).

### CLUSTER 12 `cl_new_C3` — 4 boards, 25 IMPs — **NOTHING-WRONG with the rule; two upstream defects**

`cl_new_C3` (5+ clubs, 14+ points, non-forcing 3C) is a correct toolkit call. The
boards are three different auctions:

* **576 (−9) and 997 (−7): MISSING-AGREEMENT — no "they ran from our penalty double".**
  Both auctions are *we double their 1NT for penalty → partner passes it → they run →
  we bid our own suit at the three level*. With the balance of power (23–25 combined
  facing a limited 1NT opener) the partnership should be **doubling the runout**, which
  is what wins these boards (+400/+430 vs the +110/+150 we scored). Fix: a
  `runout_double` context, `pattern: "1NT - X - P - P - bid - ?"`, `X` priority 60,
  `requires: { hcp: [14,40] }`, `establishes: { forcing: non_forcing }`, plus an
  advancer rule that sits.
* **786 (−8): see §5 F12** — N's takeout double of 1D was made with a **spade void**.
* **799 (−1):** noise.

### CLUSTER 14 `r1sr_4H` — 2 boards, 24 IMPs — **IMPLEMENTATION-BUG (ceiling, theme B)**

`responder_after_1S_rebid` (`1m – 1H – 1S – ?`) bands every rung at 18: `r1sr_3NT`
`hcp [13,18]`, `r1sr_game` `total_points [13,18]`. **`r1sr_4H` alone is `hcp [13,40]`.**

* **578 (−11), verified.** N `K9.AKQJ42.K52.KJ` = **20 HCP, six hearts** → `r1sr_4H`
  signs off in 4H. Twelve tricks; the other table bid 6NT.
* **142 (−13), verified.** N `K875.AK752.AT2.A` = **19 HCP, 4-5-3-1**. *Every* rung is
  capped at 18, so the whole context misses: best candidate 2D (FSF) at fit 0.152, 4S at
  0.134, and 4H wins the soft-miss lottery at priority 58. `gst_rkc_S` cannot fire
  (standing bid is 1S, level 1 ⇒ blocked by `standing_bid_level: [2,3,4]`), and
  `fsf_$F` is blocked twice over (`suits:{S:[0,3]}` — N has four; `longest_suit_length:
  [0,5]` on 578 — N has six). 33 combined HCP, and we stopped in 4H.

Fix:
1. `r1sr_4H`: `hcp: [13, 40]` → `hcp: [13, 18]` (parity with its siblings).
2. Open the game-force route for the 19+ hand — add to `fsf_$F.requires`:
   ```yaml
          any_of:
            - evals: { total_points: [13, 18] }
              suits: { $BS: [0, 3] }
            - evals: { total_points: [19, 40] }      # 19+ forces; shape gates waived
   ```
   and drop `suits: {$BS:[0,3]}` / `longest_suit_length: [0,5]` out of the top-level
   `requires` into the first branch. This puts 142 and 578 into a game force from which
   `rkc_ask` (`when: agreed_suit + game_forced`) becomes reachable.
Endangers: more artificial 2-level bids by 19+ hands; the FSF reply ladder already exists.

### CLUSTER 17 `pref_2NT` — 2 boards, 23 IMPs — **MISSING-AGREEMENT (incomplete ladder)**

`responder_preference_after_1M_1NT_2m` has four rungs: pass / 2M preference /
2NT invite / 3M limit raise. It has **no raise of opener's second suit** and **no rebid
of responder's own five-card major**, so a fitting hand is forced into 2NT — and the
authored rule (prio 54) shadows the toolkit call that scores a perfect 1.0.

* **868 (−10), verified.** E `76.JT765.AQT2.A4` after `1S-1NT-2D`: `3D` (raise of
  partner's D, 8-card fit) scored **match 1.0 / blended 0.793**; `pref_2NT` (prio 54)
  won over `cl_raise_D3` (prio 27). 2NT, seven tricks.
* **23 (−13), verified.** E `K3.AT643.J75.K93` after `1S-1NT-2D`: `2H` (own five-card
  major) scored **match 1.0 / blended 0.778** and lost the same way.
  Second half of this board: opener W `AJ874.Q.AQT94.75` then **passed** the 2NT invite —
  `opn_pass` is gated `hcp: [12,13]` and W is a 5-5 thirteen-count worth 15–16.

Fix (three edits in that context + one in `opener_over_pref_2NT`):
```yaml
      - id: pref_raise_3$x
        call: 3$x
        priority: 53
        requires: { suits: { $x: [4, 13] }, evals: { total_points: [10, 12] } }
        shows: "raise of opener's second suit: four-card fit, invitational"
        establishes: { forcing: invitational, agreed_suit: $x }
      # only for the M=S rows of expand_pairs
      - id: pref_own_2H
        call: 2H
        priority: 56
        requires: { suits: { H: [5, 13] }, evals: { total_points: [10, 12] } }
        shows: "five hearts, invitational: the 1NT response concealed them"
        establishes: { forcing: invitational }
```
and `opn_pass` / `opn_3NT`: `hcp: [12,13]` → `evals: { total_points: [12,13] }`,
`hcp: [14,18]` → `evals: { total_points: [14,20] }`.
Boards recovered: 23, 868 (23). Endangers: 2NT invites now need 10–12 with no fit and
no fifth major — a narrower rule, which is correct.

### CLUSTER 18 `op_lr_game` — 4 boards, 23 IMPs — **NEEDS-EXCEPTION**

All four are `1M – 3M(limit) – 4M`, nine tricks, other table +3M. Verified values at
the decision seat:

| board | hcp | total_points | LTC | result |
|---|---|---|---|---|
| 29  | **11** | 14.0 (stiff **K** = 3+3) | 8 | 4S, 9 tricks |
| 623 | 14 | 15.0 | 7 | 4S, 7 tricks |
| 174 | 14 | 16.0 | 6 | 4S, 9 tricks |
| 233 | 12 | 17.0 (**void** opposite partner's six-bagger) | 5 | 4H, 9 tricks |

`op_lr_game` gates on `total_points: [14,20]` alone. The limit raise is itself
`total_points [10,13] / hcp [8,11]`, so both hands are crediting the same fit's
distribution — board 29 accepts a game on an **11-count** because one card (the stiff
heart king) is worth six points.

Fix (two edits, and measure them separately):
1. `evaluators.total_points`, fit branch: `hand.hcp` → `adjusted_hcp(hand, ctx)`.
   Board 29 → 13.5, below the 14 floor. (Also drops board 601's `rule_of_26` below 31.)
2. `op_lr_game.requires.evals`: add `ltc: [0, 7]`. Klinger's arithmetic: a limit raise
   is 8 losers, 24 − (7+8) = 9 tricks — accepting with 8 losers is a systematic loser.
   Board 29 (LTC 8) and 623 (LTC 7 but tp 15) — use `ltc: [0,6]` to catch 623 too and
   measure; `[0,7]` is the conservative version.
Boards recovered: 29, 623 (11 of the 23) with `ltc: [0,6]`; 174/233 stay (they are
genuinely close). Endangers: this is a **high-volume** rule — every `1M-3M` auction —
so measure it on its own run before keeping it.

### CLUSTER 19 `rmr_3NT` — 2 boards, 23 IMPs — **IMPLEMENTATION-BUG (ceiling, theme B)**

* **729 (−10), verified.** N `AQT4.KT6.AQ965.A` after `1C-1S-2C`: **19 HCP**.
  `rmr_3NT` is `hcp [13,18]`; nothing else in the context scores above 0.015; the
  1-point soft miss wins and we play 3NT (twelve tricks) while 6D/6NT was there.
  `gst_rkc_C` cannot fire: N holds one club (`suits: {C:[3,13]}` fails).
* **378 (−13).** E has 17 opposite a 12–14 minor rebid — a genuine quantitative
  position with no quantitative rung.

Fix: add the missing top rung to `responder_rebid_after_minor_rebid`:
```yaml
      - id: rmr_4NT
        call: 4NT
        priority: 56
        requires: { hcp: [17, 19], evals: { semi_balanced: [1, 1] } }
        shows: "quantitative: 17-19 opposite the 12-14 minor rebid, inviting slam"
        establishes: { forcing: non_forcing }
        alertable: true
      - id: rmr_3$m_gf
        call: 3$m
        priority: 57
        requires: { suits: { $m: [4, 13] }, evals: { total_points: [19, 40] } }
        shows: "19+ with a real fit for the rebid minor: game force, slam interest"
        establishes: { forcing: game_forcing, agreed_suit: $m }
```
(the second rung makes `rkc_ask` reachable). Note this shares a call with `rmr_3m`
(10–12) — disjoint bands, but run `lint --only collide` after.

### CLUSTER 20 `ch_penalty_X` — 2 boards, 23 IMPs — **IMPLEMENTATION-BUG (call collision) + NEEDS-EXCEPTION**

Two distinct failures, both verified:

**(a) `ch_penalty_X` owns the call `X` in the negative-double seat.** Board **618 (−11)**:
E `A542.A932.KJ54.8` over `(P) 1D (3C)` — 4-4 majors, singleton club, 13 HCP: the
textbook negative double. `explain_bid` on that X returns
`source_rule_id: ch_penalty_X`, `forcing: non_forcing` — because `ch_penalty_X`
(priority 38) outranks `ch_negative_X3` (priority 33) in the *same context* and the most
specific context defining the call interprets it. Partner therefore passed the 4C
runout and we never found 4H (made ten at the other table). `lint --only collide`
reports 0 findings here: the two rules' gates look disjoint on paper
(`standing_suit_length [3,13]` vs `suit_length(their) [0,3]`) but those two evaluators
read **different suits** in a two-suit auction, and the softness lets a 13-count pass a
`[15,40]` floor.

**(b) It doubles freely-bid contracts without trump tricks.** Board **980 (−12)**: W
`AKJ532.AT8.A84.4` doubles 3H holding a **six-card spade suit** — 3HX made, −530; `3S`
was available at fit 0.409 and `P` at a full 1.0. Single **200 (−12)**: W
`QT3.AJT.KJ4.AQJ5` doubles 4H with `AJT` — `standing_suit_length` exactly 3,
`quick_tricks` exactly 3.0, both on the boundary; 4HX made, −590. In all three the
correct call scored `match 1.0` and lost the priority race.

Fix — split the rule and hard-gate it:
```yaml
      - id: ch_penalty_X
        call: X
        priority: 38
        when: { standing_bid_level: [4, 5, 6, 7] }   # NEW: at the 3 level the
                                                    # negative double owns X
        requires:
          hcp: [15, 40]
          evals: { quick_tricks: [3, 12] }
          any_of:                                    # NEW: trump TRICKS, not length
            - evals: { "standing_suit_length": [4, 13] }
            - evals: { "standing_suit_length": [3, 3], "two_of_top3(standing)": [1, 1] }
          not: { evals: { longest_suit_length: [6, 13] } }   # NEW: with a six-bagger, bid it
      - id: ch_penalty_X3                             # NEW: 3-level penalty doubles
        call: X                                       # only by a hand that has described
        priority: 37
        when: { standing_bid_level: [3], i_have_acted: true }
        requires:
          hcp: [15, 40]
          evals: { quick_tricks: [3, 12], "standing_suit_length": [4, 13] }
```
This needs one evaluator addition — `_resolve_suit` gains
`if arg == "standing": return ctx.standing_strain if ctx.standing_strain not in (None, "NT") else None`
(exactly mirroring `standing_suit_length`, which was added for this reason).
Boards recovered: 618, 980, 200 (35). Endangers: direct 3-level penalty doubles by an
undescribed hand become impossible — that is the intent; the negative double is far
more valuable there.

---

## 4. Worst single boards — assigned from #16 (board 200) onward

* **200 (−12) — IMPLEMENTATION-BUG.** See cluster 20(b). Fixed by the same edit.
* **220 (−12) — NOTHING-WRONG (flag only).** `1S-2S-3S-4S`, E `AQ8.Q53.Q2.T7542`,
  total_points 11 opposite a 14-count try: 24 HCP, 5-3 fit, close game that failed.
  Worth flagging that `rgt_accept` is gated `total_points: [8, 40]` opposite a **6-9**
  raise — the game try is a formality, since an 8 always accepts. Suggest
  `rgt_accept: [10,40]` / `rgt_decline: [0,9]` (still gapless) and measure; it does not
  recover this board.
* **686 (−12) — IMPLEMENTATION-BUG.** §1f. **[VERIFIED FLIP 5NT → 6C.]**
* **706 (−12) — IMPLEMENTATION-BUG.** `adx_pull_S4` pulls partner's reopening double of
  4H to 4S on `JT9864.J643.9.87` — **3 HCP**, `suit_quality(S) = 1.0`. 4SX, −800. The
  sit rule `adx_pass_min` scored **match 1.0 / blended 0.856** and lost on priority
  (54 vs 52). See fix F5. **[VERIFIED FLIP → P.]**
* **782 (−12) — MISSING-AGREEMENT.** `2NT–3H(transfer)–3S–3NT`: responder has offered a
  choice of games showing exactly five spades; opener E `KJ3.AQ4.K543.AK3` holds **three
  spades** and has no rule to take it — every alternative scores **0.0** and he passes
  by `fallback`. (The only 4S rule in that context, "pulling 3NT to the seven-card
  major", needs seven.) 6S was cold. Fix:
  ```yaml
      - id: nt2_tr_choose_4$M
        call: 4$M
        priority: 62
        requires: { suits: { $M: [3, 13] } }
        shows: "three-card support: taking the choice of games to the 5-3 fit"
        establishes: { forcing: sign_off, agreed_suit: $M }
  ```
  in the `2NT - 3(H|S) - 3(S|H) - 3NT - ?` context, for both majors.
* **149 (−11) — MISSING-AGREEMENT.** `(2S) X (P) 2NT (P) ?` — the takeout doubler N
  `KJ95.A6532.A53.A` (17 HCP, five hearts) **passes** advancer's natural 2NT. `3H`
  scored 0.757 and lost to the pass. There is no "doubler's rebid over advancer's 2NT"
  context. 4H made ten at the other table. Fix: add
  `pattern: "2$W - X - P - 2NT - P - ?"` with `adv2nt_3$M` (call 3M, priority 55,
  `requires: { suits: {$M:[5,13]}, hcp: [16,40] }`) and `adv2nt_3NT` (`hcp [17,40]`,
  stopper).
* **181 (−11) — NEEDS-EXCEPTION.** S `Q985432.J8.A52.Q` — a **seven-card** spade suit —
  passes out `(1NT)`. The natural overcall is gated `hcp: [8,15]`; 7 HCP is a one-point
  soft miss (0.2) and `v1NT_pass` wins. Fix: make the floor shape-aware,
  `any_of: [ {hcp:[8,15]}, {hcp:[6,15], suits:{S:[6,13]}} ]` on each `v1NT_2$X`.
  4S made ten at the other table.
* **295 (−11) — MISSING-AGREEMENT (LOTT sacrifice).** `(1H) 1S (2S) 3S (4H) ?` with
  nine spades between the hands and their vulnerable game bid — `ch_pass` passes out
  4H; par is NS +300, i.e. 4SX down two is the winning action. There is no
  "bid one more with a nine-card fit over their game" rule. Same missing rule as 761.
* **296 (−11) — IMPLEMENTATION-BUG (ceiling, theme B).** N `AKJ986.AKJ6.A.92` = **20 HCP**
  after `1S-1NT`. The jump rebid `ob_1M1NT_3S` is `hcp [16,19]` → fit 0.134 at 20; the
  hand falls through to `ob_1M1NT_4S`. Verified. Fix: widen the jump-rebid band to
  `[16,21]` (or gate on `total_points`), so 20-counts make a forcing jump rebid instead
  of blasting game.
* **453 (−11) — MEASURE (evidence for §2, pessimism direction).** E `AJ952.AJ64.AJ5.8`
  (15 HCP, 5 spades) **passes** partner's competitive `3S` LOTT raise. `cl_raise_S4`
  scored 0.409, missing only on `rule_of_26: [25,99]` — because a *LOTT* raise is a
  shape statement whose `min_total_points` floor is deliberately tiny. Combined-points
  is the wrong gate for accepting a Law raise. Fix:
  `cl_raise_S4/H4`: `rule_of_26: [25,99]` → `any_of: [ {evals:{rule_of_26:[25,99]}},
  {evals:{"lott_total_trumps($M)":[10,26]}}, {evals:{ltc:[0,6]}} ]`. 3S made twelve.
* **473 (−11) — IMPLEMENTATION-BUG.** The weak-two feature-ask replies are gated
  `features: [ "two_of_top3(C)" ]` — **two of the top three honours** — while the
  `shows:` text says *"feature (ace or king)"*. S `K3.Q96532.8.AJT3` holds the **club
  ace** and answers `3H` "minimum weak two, no outside feature" (`AJT3` → two_of_top3 = 0).
  Affects all nine `feat_{D,H,S}_{C,D,H,S}` rules. Fix, no new evaluator needed:
  ```yaml
        requires:
          hcp: [8, 10]
          any_of:
            - evals: { "two_of_top3(C)": [1, 1] }
            - suits: { C: [2, 13] }
              evals: { "control_in(C)": [1, 2] }     # A or K with 2+ cards
  ```
* **502 (−11) — NEEDS-EXCEPTION.** W `AJ.Q42.K9.AJT943` doubles `(2S)` for **takeout**
  holding a six-card club suit and a doubleton diamond. `vw2_X` (priority 70) has no
  shape requirement whatsoever beyond "0–2 in their suit" on the 13–16 branch; the
  natural `3C` scored **match 1.0** and lost. Fix:
  ```yaml
          any_of:
            - hcp: [13, 16]
              suits: { $W: [0, 2] }
              evals: { longest_suit_length: [0, 5] }   # with a six-bagger, overcall it
            - hcp: [17, 40]
  ```
  Same species as cluster 12's board 786 (`oc1D_X` doubled 1D with a **spade void**) —
  add the mirror gate there.
* **518 (−11) — MISSING-AGREEMENT.** W overcalled `2D` over 1NT on
  `Q.T83.AKJ9642.T8` (**seven** diamonds) and then, over `2H`/`2NT`, **passes**: the
  toolkit's `cl_new_D3` is `when: { unbid_suit: D }` and D is *our* suit, and the only
  self-rebid rule (`invitational jump rebid in competition, 6+ good D, 16-19`) scores
  0.134 on a 10-count. Ten trumps between the hands; they made 4H+1. Fix: add a
  weak/LOTT self-rebid to the toolkit —
  `cl_rebid_own_3$X`, priority 28, `when: { i_bid_suit: $X, cheapest_in_suit: true }`,
  `requires: { suits: {$X:[6,13]}, evals: {"lott_total_trumps($X)": [9,26]} }`.
* **734 (−11) — IMPLEMENTATION-BUG.** `adx_pull_S3` pulls partner's reopening double of
  3D to 3S on `K853.976.AT.6432` — a flat 7-count with a four-card suit,
  `suit_quality(S) = 1.0`. −200 instead of +200. Sit rule scored 1.0 / 0.856 and lost on
  priority. See F5. **[VERIFIED FLIP → P.]**
* **761 (−11) — MISSING-AGREEMENT.** Partner opens 4H, they sacrifice in 5C, and W
  `K86543.A6.A765.5` **doubles** (`ch_sac_X`: `quick_tricks` exactly 2.5,
  `max_their_suit_length` 1 — both on the boundary). With the heart ace opposite an
  eight-card preempt, 5H is the bid; +100 instead of +450/+500. `P` was the only other
  candidate: there is **no "bid one more over their sacrifice" rule**. Same gap as 295.
  Fix: add ahead of `ch_sac_X`
  ```yaml
      - id: ch_sac_bid_5$M
        call: 5$M
        priority: 46
        when: { partner_suit: $M, standing_bid_level: [5], we_bid_last: false }
        requires:
          suits: { $M: [2, 13] }
          evals: { "control_in($M)": [2, 2], "lott_total_trumps($M)": [10, 26] }
        shows: "first-round control of our own suit and a huge fit: bidding over their save"
        establishes: { forcing: sign_off, agreed_suit: $M }
  ```

---

## 5. Fix list (deduplicated, prioritised)

Ordered by (IMPs recovered in this dossier) × (confidence) ÷ (risk). "Verified" =
the flip was reproduced against a patched scratch copy.

| # | change | files / ids | boards recovered | endangers |
|---|---|---|---|---|
| **F1** | `rkc5S_slam_C`, `rkc5S_slam_D`: `"keycards(agreed)": [3,5]` → `[2,5]`. `rkc5H_slam_C/_D`: copy the corrected `rkc5H_slam` `any_of` (F2); their `_signoff_C/_D` → `requires: {}` | yaml 4877, 4901, 4829, 4853 | **686 (12) — verified** | nothing: the majors already run on this arithmetic |
| **F2** | `rkc5H_slam` → `any_of: [{kc [2,5], trump_queen [1,1]}, {kc [2,5], lott [10,26]}]`; `rkc5H_signoff` → `requires: {}` | yaml 4651, 4664 | **790 (11) — verified**; 126 unchanged | gives up 5-keycard slams in a 7–8 card fit with the queen missing (correct) |
| **F3** | `ch_penalty_X`: add `when: { standing_bid_level: [4,5,6,7] }`, the `any_of` trump-trick test, `not: {longest_suit_length [6,13]}`; add `ch_penalty_X3` gated `i_have_acted: true`; add `"standing"` to `_resolve_suit` | yaml ~8850; evaluators.py `_resolve_suit` | **618 (11), 980 (12), 200 (12) = 35** | removes direct 3-level penalty doubles by an undescribed hand (intended) |
| **F4** | `adx_pull_*` (12 rules): add `"suit_quality($X)": [1.5, 9]`; optionally drop their priorities below `adx_pass_min` (52) | yaml 5282–5390 | **706 (12), 734 (11) — verified** | pulls to Qxxxx/Jxxxxx become impossible; the pull to KJxxx (quality 1.5) survives |
| **F5** | `rkc_4NT`: add `"lott_total_trumps(agreed)": [8, 26]` | yaml 4498 | **919 (17, other slice) — verified** | 2C-positive auctions where shown length understates the fit; use 7 if a run shows losses |
| **F6** | `responder_preference_after_1M_1NT_2m`: add `pref_raise_3$x` and `pref_own_2H`; `opn_pass`/`opn_3NT` gate on `total_points` not `hcp` | yaml ~5985, 6010 | **23 (13), 868 (10) = 23** | narrows the 2NT invite (correct) |
| **F7** | New Minor Forcing after `1m – 1M – 1NT` (two new contexts per minor + responder placement) | new, near yaml 2331 | **654 (13), 328 (11), 267 (2) = 26**; plus 501/970 (23) in cluster 2 | 2C/2D after `1m-1M-1NT` becomes artificial — check `lint --only collide` |
| **F8** | Ceiling repair (theme B): `r1sr_4H` `[13,40]`→`[13,18]`; `ob_1M1NT_3S` `[16,19]`→`[16,21]`; `fsf_$F` shape gates waived at `total_points ≥ 19`; add `rmr_4NT` + `rmr_3$m_gf` | yaml 6627, ~2400, 5703, ~2470 | **142 (13), 578 (11), 729 (10), 296 (11) = 45** | more artificial 2-level FSF and forcing jumps; the reply ladders already exist |
| **F9** | `nt2_tr_choose_4$M` after `2NT – transfer – accept – 3NT` | new, in the `nt2_tr_*` block | **782 (12)** | none: currently a zero-candidate seat |
| **F10** | `gf_pref_3$M`: `not: { suits: { $M: [0,2] } }`; new `gf_own_3$M` rung | yaml 5826 + new | **279 (13)** | 3-card preferences unaffected |
| **F11** | `gst_rkc_*` + `rkc_4NT`: require the asker's own keycards (`3+`, or `2` with a ten-card fit or 33+) | yaml 5421–5478, 4492 | **601 (12), 973 (12) = 24**; also brakes 534/58 in cluster 6 | some genuine 2-keycard asks opposite big hands; **measure alone** |
| **F12** | Weak-two feature replies: `two_of_top3` → "ace or king" (`any_of` with `control_in` and 2+ cards) | yaml 7647–7720 (9 rules) | **473 (11)** | the ask now gets an answer more often — intended |
| **F13** | `vw2_X` 13–16 branch: add `longest_suit_length: [0,5]`; mirror on `oc1D_X`/`oc1H_X` | yaml ~4448 | **502 (11), 786 (8) = 19** | strong (17+) takeout doubles with a long suit still allowed |
| **F14** | `evaluators.total_points`: use `adjusted_hcp(hand, ctx)` instead of `hand.hcp` in the fit branch | evaluators.py:87 | **29 (6)**; helps 601, and it is the accounting half of §2 | **high volume** — every `total_points` gate shifts by 0.5–1.5; measure alone |
| **F15** | `op_lr_game`: add `ltc: [0, 6]` | yaml ~5480 | **29 (6), 623 (5) = 11** | very high volume (every `1M-3M`); measure alone |
| **F16** | LOTT "bid one more" over their game/sacrifice: `ch_sac_bid_5$M`; and a nine-trump sacrifice rule over their freely-bid game | new, near `sacrifice_double_over_our_game` | **761 (11), 295 (11) = 22** | phantom saves — gate hard on `lott ≥ 10` and first-round control |
| **F17** | Grand-slam machinery: 5NT kings-ask after the 5H/5S replies + reply context + 7-level placement | new, in `rkc_continue_after_*` | **126 (13)**; 847/498/7/913 (59) in the other slice | highest variance on the list — gate on all five keycards + queen + 34; measure alone |
| **F18** | "They ran from our penalty double of 1NT" — reopening/penalty `X` context | new | **576 (9), 997 (7) = 16** | doubling runouts with the balance of power is standard |
| **F19** | Doubler's rebid over advancer's 2NT; overcaller's LOTT self-rebid of a 6+ suit; `cl_raise_S4/H4` Law-raise acceptance | new + yaml 8640/8660 | **149 (11), 518 (11), 453 (11) = 33** | more competitive bidding at the 3–4 level |
| **F20** | `rule_of_26` units repair (+1.5 for an unbounded partner box) — §2 | evaluators.py:104 | none directly | **must be paired with F14**; alone it pushes cluster 18 further into over-bidding. Re-measure the 31 threshold only after F1–F5 and F11 are in |
| **F21** | `rgt_accept` `[8,40]` → `[10,40]`, `rgt_decline` `[0,7]` → `[0,9]` | yaml ~6510 | none in this dossier | flagged only: an 8-point acceptance makes the game try meaningless |

### Recommended first batch (low risk, high certainty, all arithmetic or zero-candidate seats)
F1, F2, F5, F4, F9, F3, F12 — **~110 IMPs** across boards 686, 790, 919, 706, 734, 782,
618, 980, 200, 473, and none of them changes a strength band.

### Second batch (structure, medium risk)
F6, F7, F8, F10, F13, F18, F19 — **~170 IMPs**; run `tools/lint_system.py --only collide`
after F7 and F8 (both add rules sharing a call with an existing rung).

### Measure alone
F11, F14, F15, F17, F20 — each changes a high-volume gate or opens a new level of
bidding. In particular **do not** re-measure the "31 combined" line until F1–F5 and F11
are in; on the six slam boards I could measure, `rule_of_26` was accurate to −0.25 on
average, and every slam we lost was lost to a counting fact (a 4–3 fit, a denied trump
queen, three keycards, an un-updated minor-suit continuation) that no points threshold
can express.
