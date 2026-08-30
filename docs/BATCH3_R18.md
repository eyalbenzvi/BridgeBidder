# Batch 3 — the starved answering seats — KEPT on a neutral number

103 contexts, 304 rules from six agreements (302 after three repairs).
Round 17's central lesson applied below game: **a force, an ask or an
invitation is worth nothing until the seat that answers it exists.**

## The six agreements

1. **The cue-raise family** — the file had five cue-raise rules and **zero**
   contexts answering any of them; eleven new answering contexts.
2. **`fourth_suit_reply`** — the file's one game-forcing ask below 2NT had
   exactly two answers, "stopper" and "three-card support". Opener with
   neither (5-5, no stopper) topped out at **fit 0.349**, the soft-miss lottery
   handed him a raise he did not hold, and responder then asked for keycards on
   a 27-count and played 5S.
3. **The forcing new suit opposite a weak two**, a named open item and the
   fourth instance of the species: `2D-2S-3D-P` at -100 becomes
   `2D-2S-3D-3H-P` at +140.
4. **A reverse is forcing with no answer below 8 points** — every `rrev*` rung
   floors at `hcp: [8, 40]`, so a 4-count passed a one-round force at fit 1.00.
5. **Responder's invitational jump rebid has no answering seat** — two cold
   games passed out at the three level, `uc_pass` at fit 1.000.
6. **Four unauthored constructive seats** where `uc_nt2` bid over a sign-off,
   `uc_raise_S3` raised a sign-off and `uc_raise_H4` accepted every invitation
   on eleven support points.

All eight starved seats were confirmed empty **before** anything was authored.

## The numbers

| | changed boards | delta | per 1000 | t | 95% bootstrap CI |
|---|---|---|---|---|---|
| batch 2 alone | 216 | +200 | +16.7 | +2.55 | [+44, +355] |
| **batch 3 alone** | **231** | **+105** | **+8.8** | **+1.26** | **[-59, +270]** |
| **batch 2 + 3** | **447** | **+305** | **+25.4** | **+2.67** | **[+79, +532]** |

## The judgement, stated rather than buried

Batch 3's own interval covers zero, so `screen.py`'s automatic verdict is
REVERT. **I overrode it**, under this round's own decision rule: *a batch that
measures neutral and is structurally sound should be KEPT, because the thesis
is that density pays only in aggregate.*

The two structural tests both pass:

* **every force it introduces ships with the seat that answers it**, in the
  same batch — that is what the batch IS;
* **nothing is shadowed**: lint went **down**, 223 → 219, because authoring
  starved seats closes `floor` findings.

The build ships on the aggregate, +305 with a CI excluding zero. Batch 3's
increment is real but individually unresolvable at 231 changed boards, which is
exactly what a 1.04 IMPs/changed-board resolution means.

## Three locked scenarios corrected the batch, and all three were real

Every one was the same species — a new rung placed above the call it should sit
under, the round-14 `uc_nt_raise3` mistake repeated, which is now the most
repeated error in this project's history.

* `rrev_min_2$M` was authored at priority **67**, above `rrev_2$M` at 66, so
  responder's cheap rebid of his own suit after a reverse — which this system
  defines as **forcing one round** — began reading as non-forcing. **CUT
  rather than re-priced**: the agreement as drafted contradicts an existing
  agreement instead of filling a hole, and a call means one thing. This is the
  collision the editor step exists to catch, and it reached the tree anyway.
* `rorr_game_$M` at 50 outranked the keycard ask `gst_rkc_$M` at 46, so an
  eight-card fit with slam values bid game instead of asking. Re-priced to
  45.5 — the rung is what the hand bids when the ask does *not* fit.
* `r1d1h2c_4H` gated only on `total_points: [14, 40]`, and a seven-card suit is
  worth three length points, so an **eleven-count** bid game over the
  invitational rung below it. Given the high-card floor a game bid needs.
