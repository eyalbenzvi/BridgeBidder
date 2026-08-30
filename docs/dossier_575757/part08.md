# Lost boards part 8 of 8 (36 boards, -41 IMPs)

Sorted worst-first across the whole match.

## Board 936 — margin -2 IMPs

dealer **N**, vul **EW**, par(N/S) **-130**

    N  K5432.QT6.A2.T73   (9 HCP)
    E  Q9.AJ75.KQJ86.J5   (14 HCP)
    S  AJT76.983.7.A642   (9 HCP)
    W  8.K42.T9543.KQ98   (8 HCP)

Double-dummy tricks:

| declarer | C | D | H | S | NT |
|---|---|---|---|---|---|
| N | 6 | 3 | 4 | 8 | 7 |
| E | 6 | 10 | 9 | 5 | 6 |
| S | 6 | 3 | 4 | 8 | 7 |
| W | 6 | 10 | 9 | 5 | 6 |

Table A (**we are N/S**): 3D by E (10 tricks), N/S score -130  
Table B (**we are E/W**): 3S by S (8 tricks), N/S score -50  
IMP margin for us: **-2**

### Table A — we are NS, BEN is EW

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | N | P | US | open_pass | P (1.00) |
| 1 | E | 1D | BEN |  |  |
| 2 | S | 1S | US | oc1D_1S | 1S (0.98) |
| 3 | W | 2D | BEN |  |  |
| 4 | N | 2S | US | cl_raise_S2 | 2S (0.58) |
| 5 | E | 3D | BEN |  |  |
| 6 | S | P | US | ch_pass | P (0.77) |
| 7 | W | P | BEN |  |  |
| 8 | N | P | US | balhigh_pass | 3S (0.91) **≠** ← FIRST DIVERGENCE |

### Table B — we are EW, BEN is NS

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | N | P | BEN |  |  |
| 1 | E | 1D | US | open_1D | 1D (1.00) |
| 2 | S | 1S | BEN |  |  |
| 3 | W | 2D | US | nx_1m1S_raise | 2D (0.95) |
| 4 | N | 2S | BEN |  |  |
| 5 | E | 3D | US | cl_raise_D3 | 3D (0.92) |
| 6 | S | P | BEN |  |  |
| 7 | W | P | US | uc_pass | P (0.99) |
| 8 | N | 3S | BEN |  |  |
| 9 | E | P | US | ch_pass | P (0.50) |
| 10 | S | P | BEN |  |  |
| 11 | W | P | US | balhigh_pass | 4D (0.53) **≠** ← FIRST DIVERGENCE |

### First divergence: table A, call 8, seat N

auction so far: `P 1D 1S 2D 2S 3D P P`, hand `K5432.QT6.A2.T73`

| call | rule | fit | score | prio | shows |
|---|---|---|---|---|---|
| P | balhigh_pass **← DECIDED** | 1.000 | 0.763 | 21.0 | nothing worth reopening on: passing it out |
| 4S | balhigh_raise_lott4_S | 0.640 | 0.509 | 32.0 | the Law at the four level: they have a fit and so have we, ten-plus tr |
| 3S | balhigh_raise_S3 | 0.409 | 0.325 | 31.0 | competitive raise of partner's S: 3+ trumps, 10+ support points, 8+ co |
| 3S | balhigh_rebid_S3 | 0.279 | 0.220 | 29.0 | rebid of my own S: 6+ cards, values for the level opposite partner's s |
| 4S | balhigh_raise_S4 | 0.003 | 0.002 | 32.0 | competitive raise of partner's S: 11+ support points, a real trump fit |
| 3NT | balhigh_nt3 | 0.001 | 0.001 | 29.0 | natural 3NT: 13-19 balanced with a stopper in their suit |
| 3H | balhigh_new_H3 | 0.000 | 0.000 | 27.0 | natural H at the cheapest level: 5+ cards, 14+ points |
| 4C | balhigh_new_C4 | 0.000 | 0.000 | 28.0 | natural C at the cheapest level: 5+ cards, 14+ points |
| X | balhigh_reopen_X | 0.000 | 0.000 | 41.0 | reopening double: 16+, short in their suit, our side already in |
| 4NT | gst_rkc_S | 0.000 | 0.000 | 46.0 | RKC Blackwood 1430 for S: slam values opposite partner's shown range |

---

## Board 954 — margin -2 IMPs

dealer **S**, vul **EW**, par(N/S) **-500**

    N  5.J4.T9652.A7532   (5 HCP)
    E  T43.A9762.AKJ3.K   (15 HCP)
    S  AK8762.QT.Q4.QT6   (13 HCP)
    W  QJ9.K853.87.J984   (7 HCP)

Double-dummy tricks:

| declarer | C | D | H | S | NT |
|---|---|---|---|---|---|
| N | 7 | 6 | 3 | 6 | 4 |
| E | 5 | 7 | 9 | 6 | 9 |
| S | 7 | 6 | 3 | 6 | 4 |
| W | 5 | 7 | 9 | 6 | 9 |

Table A (**we are N/S**): 3S by S (6 tricks), N/S score -150  
Table B (**we are E/W**): 2S by S (6 tricks), N/S score -100  
IMP margin for us: **-2**

### Table A — we are NS, BEN is EW

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | S | 1S | US | open_1S | 1S (1.00) |
| 1 | W | P | BEN |  |  |
| 2 | N | P | US | r1S_pass | P (0.99) |
| 3 | E | 2H | BEN |  |  |
| 4 | S | 2S | US | o4b_rebid_S | 2S (0.99) |
| 5 | W | 3H | BEN |  |  |
| 6 | N | P | US | ch_pass | P (0.99) |
| 7 | E | P | BEN |  |  |
| 8 | S | 3S | US | balhigh_rebid_S3 | P (0.99) **≠** ← FIRST DIVERGENCE |
| 9 | W | P | BEN |  |  |
| 10 | N | P | US | uc_pass | P (0.97) |
| 11 | E | P | BEN |  |  |

### Table B — we are EW, BEN is NS

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | S | 1S | BEN |  |  |
| 1 | W | P | US | oc1S_pass | P (1.00) |
| 2 | N | P | BEN |  |  |
| 3 | E | X | US | bal_X | 2H (0.99) **≠** ← FIRST DIVERGENCE |
| 4 | S | 2S | BEN |  |  |
| 5 | W | P | US | cl_pass | P (0.99) |
| 6 | N | P | BEN |  |  |
| 7 | E | P | US | ballow_pass | P (0.75) |

### First divergence: table A, call 8, seat S

auction so far: `1S P P 2H 2S 3H P P`, hand `AK8762.QT.Q4.QT6`

| call | rule | fit | score | prio | shows |
|---|---|---|---|---|---|
| 3S | balhigh_rebid_S3 **← DECIDED** | 1.000 | 0.787 | 29.0 | rebid of my own S: 6+ cards, values for the level opposite partner's s |
| P | balhigh_pass | 1.000 | 0.763 | 21.0 | nothing worth reopening on: passing it out |
| X | balhigh_reopen_X | 0.047 | 0.039 | 41.0 | reopening double: 16+, short in their suit, our side already in |
| 3NT | balhigh_nt3 | 0.000 | 0.000 | 29.0 | natural 3NT: 13-19 balanced with a stopper in their suit |

---

## Board 987 — margin -2 IMPs

dealer **W**, vul **EW**, par(N/S) **-110**

    N  A83.83.J76.AQT42   (11 HCP)
    E  KT952.A.T953.K86   (10 HCP)
    S  J76.KQ952.A8.J53   (11 HCP)
    W  Q4.JT764.KQ42.97   (8 HCP)

Double-dummy tricks:

| declarer | C | D | H | S | NT |
|---|---|---|---|---|---|
| N | 8 | 3 | 6 | 4 | 6 |
| E | 5 | 9 | 7 | 8 | 5 |
| S | 8 | 4 | 6 | 4 | 7 |
| W | 5 | 9 | 7 | 8 | 5 |

Table A (**we are N/S**): 2NT by N (6 tricks), N/S score -100  
Table B (**we are E/W**): 3C by N (8 tricks), N/S score -50  
IMP margin for us: **-2**

### Table A — we are NS, BEN is EW

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | W | P | BEN |  |  |
| 1 | N | P | US | open_pass | 1C (0.56) **≠** ← FIRST DIVERGENCE |
| 2 | E | 1S | BEN |  |  |
| 3 | S | 2H | US | oc1S_2H | P (0.96) **≠** |
| 4 | W | P | BEN |  |  |
| 5 | N | 2NT | US | uc_nt2 | 3NT (0.43) **≠** |
| 6 | E | P | BEN |  |  |
| 7 | S | P | US | uc_pass | 3H (0.34) **≠** |
| 8 | W | P | BEN |  |  |

### Table B — we are EW, BEN is NS

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | W | P | US | open_pass | P (1.00) |
| 1 | N | 1C | BEN |  |  |
| 2 | E | 1S | US | oc1C_1S | 1S (0.98) |
| 3 | S | 2H | BEN |  |  |
| 4 | W | P | US | cl_pass | P (1.00) |
| 5 | N | 3C | BEN |  |  |
| 6 | E | P | US | ch_pass | P (1.00) |
| 7 | S | P | BEN |  |  |
| 8 | W | P | US | balhigh_pass | P (1.00) |

### First divergence: table A, call 1, seat N

auction so far: `P`, hand `A83.83.J76.AQT42`

| call | rule | fit | score | prio | shows |
|---|---|---|---|---|---|
| P | open_pass **← DECIDED** | 1.000 | 0.760 | 20.0 | fewer than opening values |
| 1C | open_1C | 0.800 | 0.735 | 73.0 | opening, 3+ clubs (better minor), no 5-card major, 12-21 HCP |
| 1C | open_1C_rule20 | 0.800 | 0.730 | 71.0 | 5+ clubs, light opening satisfying the rule of 20 |
| 1D | open_1D | 0.114 | 0.105 | 74.0 | opening, 3+ diamonds (better minor), no 5-card major, 12-21 HCP |
| 1NT | open_1NT | 0.028 | 0.027 | 92.0 | 15-17 balanced (may contain a 5-card major) |
| 1S | open_1S | 0.012 | 0.011 | 81.0 | 5+ spades, 12-21 HCP |
| 1S | open_1S_rule20 | 0.009 | 0.008 | 79.0 | 5+ spades, light opening satisfying the rule of 20 |
| 3C | open_3C_nv | 0.006 | 0.005 | 60.0 | preempt: 7+ clubs, 3-9 HCP |
| 1D | open_1m_rule20 | 0.005 | 0.004 | 72.0 | 5+ diamonds, light opening satisfying the rule of 20 |
| 2S | open_weak_2S_nv | 0.000 | 0.000 | 66.0 | weak two: 6 spades, 5-10 HCP |
| 2D | open_weak_2D_nv | 0.000 | 0.000 | 64.0 | weak two: 6 diamonds, 5-10 HCP |
| 1H | open_1H | 0.000 | 0.000 | 80.0 | 5+ hearts, 12-21 HCP |
| 1H | open_1H_rule20 | 0.000 | 0.000 | 78.0 | 5+ hearts, light opening satisfying the rule of 20 |
| 3S | open_3S_nv | 0.000 | 0.000 | 60.0 | preempt: 7+ spades, 3-9 HCP |

---

## Board 993 — margin -2 IMPs

dealer **E**, vul **None**, par(N/S) **-450**

    N  JT2.A8743.JT2.A9   (10 HCP)
    E  54.QJ2.AK964.QT8   (12 HCP)
    S  86.KT65.Q53.J765   (6 HCP)
    W  AKQ973.9.87.K432   (12 HCP)

Double-dummy tricks:

| declarer | C | D | H | S | NT |
|---|---|---|---|---|---|
| N | 4 | 4 | 6 | 2 | 3 |
| E | 9 | 9 | 6 | 11 | 9 |
| S | 4 | 4 | 6 | 2 | 3 |
| W | 9 | 9 | 6 | 11 | 9 |

Table A (**we are N/S**): 4S by W (11 tricks), N/S score -450  
Table B (**we are E/W**): 3NT by E (9 tricks), N/S score -400  
IMP margin for us: **-2**

### Table A — we are NS, BEN is EW

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | E | 1D | BEN |  |  |
| 1 | S | P | US | oc1D_pass | P (1.00) |
| 2 | W | 1S | BEN |  |  |
| 3 | N | P | US | sw_pass | P (0.98) |
| 4 | E | 1NT | BEN |  |  |
| 5 | S | P | US | cl_pass | P (1.00) |
| 6 | W | 2C | BEN |  |  |
| 7 | N | P | US | cl_pass | P (0.99) |
| 8 | E | 3NT | BEN |  |  |
| 9 | S | P | US | ch_pass | P (1.00) |
| 10 | W | 4S | BEN |  |  |
| 11 | N | P | US | ch_pass | P (1.00) |
| 12 | E | P | BEN |  |  |
| 13 | S | P | US | balhigh_pass | P (1.00) |

### Table B — we are EW, BEN is NS

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | E | 1D | US | open_1D | 1D (1.00) |
| 1 | S | P | BEN |  |  |
| 2 | W | 1S | US | r1m_1S | 1S (1.00) |
| 3 | N | P | BEN |  |  |
| 4 | E | 1NT | US | ob_1NT | 1NT (1.00) |
| 5 | S | P | BEN |  |  |
| 6 | W | 3S | US | rr_nt_gf3_S | 2C (0.97) **≠** ← FIRST DIVERGENCE |
| 7 | N | P | BEN |  |  |
| 8 | E | 3NT | US | oac3_3NT_S | 4S (0.93) **≠** |
| 9 | S | P | BEN |  |  |
| 10 | W | P | US | fallback | P (1.00) |
| 11 | N | P | BEN |  |  |

### First divergence: table B, call 6, seat W

auction so far: `1D P 1S P 1NT P`, hand `AKQ973.9.87.K432`

| call | rule | fit | score | prio | shows |
|---|---|---|---|---|---|
| 3S | rr_nt_gf3_S **← DECIDED** | 1.000 | 0.860 | 53.5 | 5+ S, game forcing: asking for three-card support |
| 4S | rr_nt_4S | 0.800 | 0.687 | 53.0 | 6+ S, game values |
| 2S | rr_nt_2S | 0.800 | 0.682 | 51.0 | 6+ S, 6-11, to play - with no invitational 3S available, eleven signs  |
| P | rr_nt_pass | 0.409 | 0.348 | 50.0 | no game interest opposite 12-14 |
| 2C | uc_new_C2 | 0.264 | 0.206 | 26.0 | natural C at the cheapest level: 5+ cards, 10+ points |
| 2NT | rr_nt_2NT | 0.100 | 0.086 | 52.0 | invitational 11-12 |
| 3NT | rr_nt_3NT | 0.080 | 0.069 | 54.0 | to play |
| 2C | uc_new_C2_hi | 0.035 | 0.028 | 26.5 | natural C at the cheapest level: 5+ cards, 10+ points (my longest suit |
| 2H | rr_nt_second_H | 0.000 | 0.000 | 51.5 | 5-4: the second suit, to play |
| 3S | rr_nt_slam3_S | 0.000 | 0.000 | 56.0 | 5+ S with slam values opposite the 12-14 rebid |
| 2D | uc_raise_D2 | 0.000 | 0.000 | 30.0 | raise of partner's D: 3+ trumps, 6-9 support points, 7+ combined trump |
| 4NT | rr_nt_4NT | 0.000 | 0.000 | 55.0 | quantitative: 17-18 opposite the 12-14 rebid, inviting slam |
| 5D | uc_minor_game_5D | 0.000 | 0.000 | 28.0 | accepting to game in the raised minor: 17+ opposite the raise |
| 4D | uc_raise_D4 | 0.000 | 0.000 | 27.0 | raise of partner's D: 11+ support points, a real trump fit, and the va |

---

## Board 995 — margin -2 IMPs

dealer **W**, vul **None**, par(N/S) **-140**

    N  K8.A2.AQJT4.T763   (14 HCP)
    E  AQT3.73.985.KJ92   (10 HCP)
    S  J75.QT64.K73.854   (6 HCP)
    W  9642.KJ985.62.AQ   (10 HCP)

Double-dummy tricks:

| declarer | C | D | H | S | NT |
|---|---|---|---|---|---|
| N | 5 | 7 | 4 | 3 | 6 |
| E | 7 | 6 | 9 | 9 | 7 |
| S | 5 | 7 | 4 | 3 | 6 |
| W | 7 | 6 | 9 | 9 | 7 |

Table A (**we are N/S**): 3NT by N (6 tricks), N/S score -150  
Table B (**we are E/W**): 3D by N (7 tricks), N/S score -100  
IMP margin for us: **-2**

### Table A — we are NS, BEN is EW

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | W | P | BEN |  |  |
| 1 | N | 1D | US | open_1D | 1D (1.00) |
| 2 | E | P | BEN |  |  |
| 3 | S | 1H | US | r1m_1H | 1H (1.00) |
| 4 | W | P | BEN |  |  |
| 5 | N | 2C | US | ob_1D1H_2C | 2C (1.00) |
| 6 | E | P | BEN |  |  |
| 7 | S | 2D | US | r1d1h2c_2D | 2D (0.97) |
| 8 | W | P | BEN |  |  |
| 9 | N | 3NT | US | uc_nt3 | 3D (0.70) **≠** ← FIRST DIVERGENCE |
| 10 | E | P | BEN |  |  |
| 11 | S | P | US | fallback | P (1.00) |
| 12 | W | P | BEN |  |  |

### Table B — we are EW, BEN is NS

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | W | P | US | open_pass | P (0.93) |
| 1 | N | 1D | BEN |  |  |
| 2 | E | P | US | oc1D_pass | P (1.00) |
| 3 | S | 1H | BEN |  |  |
| 4 | W | P | US | sw_pass | P (1.00) |
| 5 | N | 2C | BEN |  |  |
| 6 | E | P | US | cl_pass | P (1.00) |
| 7 | S | 2D | BEN |  |  |
| 8 | W | P | US | cl_pass | P (1.00) |
| 9 | N | 3D | BEN |  |  |
| 10 | E | P | US | ch_pass | P (1.00) |
| 11 | S | P | BEN |  |  |
| 12 | W | P | US | balhigh_pass | P (1.00) |

### First divergence: table A, call 9, seat N

auction so far: `P 1D P 1H P 2C P 2D P`, hand `K8.A2.AQJT4.T763`

| call | rule | fit | score | prio | shows |
|---|---|---|---|---|---|
| 3NT | uc_nt3 **← DECIDED** | 1.000 | 0.787 | 29.0 | natural 3NT: 13-19 balanced, their suits stopped |
| P | uc_pass | 1.000 | 0.754 | 18.0 | no bid describes this hand: nothing further to show |
| 2NT | uc_nt2 | 0.409 | 0.321 | 28.0 | natural 2NT: 11-12 balanced, their suits stopped |
| 3D | uc_rebid_D3 | 0.349 | 0.273 | 27.0 | rebid of my own D: 6+ cards, values for the level opposite partner's s |
| 3D | uc_raise_D3 | 0.082 | 0.064 | 27.0 | raise of partner's D: 3+ trumps, 10+ support points, 8+ combined trump |
| 2H | uc_raise_H2 | 0.012 | 0.009 | 30.0 | raise of partner's H: 3+ trumps, 6-9 support points, 7+ combined trump |
| 3C | uc_rebid_C3 | 0.011 | 0.009 | 27.0 | rebid of my own C: 6+ cards, values for the level opposite partner's s |
| 5D | uc_minor_game_5D | 0.000 | 0.000 | 28.0 | accepting to game in the raised minor: 17+ opposite the raise |
| 2S | uc_new_S2 | 0.000 | 0.000 | 26.0 | natural S at the cheapest level: 5+ cards, 10+ points |
| 4H | uc_raise_H4 | 0.000 | 0.000 | 32.0 | raise of partner's H: 11+ support points, a real trump fit, and the va |
| 2S | uc_new_S2_hi | 0.000 | 0.000 | 26.5 | natural S at the cheapest level: 5+ cards, 10+ points (my longest suit |
| 4D | uc_raise_D4 | 0.000 | 0.000 | 27.0 | raise of partner's D: 11+ support points, a real trump fit, and the va |
| 4NT | gst_rkc_D | 0.000 | 0.000 | 46.0 | RKC Blackwood 1430 for D: slam values opposite partner's shown range |

---

## Board 1 — margin -1 IMPs

dealer **E**, vul **None**, par(N/S) **-140**

    N  QJ954.KQ8.62.JT2   (9 HCP)
    E  T863.9765.A.AKQ6   (13 HCP)
    S  .AJT2.QJT753.983   (8 HCP)
    W  AK72.43.K984.754   (10 HCP)

Double-dummy tricks:

| declarer | C | D | H | S | NT |
|---|---|---|---|---|---|
| N | 4 | 6 | 5 | 4 | 5 |
| E | 8 | 6 | 7 | 9 | 8 |
| S | 4 | 6 | 5 | 4 | 5 |
| W | 8 | 6 | 7 | 9 | 8 |

Table A (**we are N/S**): 2S by W (9 tricks), N/S score -140  
Table B (**we are E/W**): 2D by S (6 tricks), N/S score -100  
IMP margin for us: **-1**

### Table A — we are NS, BEN is EW

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | E | 1C | BEN |  |  |
| 1 | S | 1D | US | oc1C_1D | 1D (0.81) |
| 2 | W | 1S | BEN |  |  |
| 3 | N | 1NT | US | cl_nt1 | P (0.52) **≠** ← FIRST DIVERGENCE |
| 4 | E | 2S | BEN |  |  |
| 5 | S | P | US | cl_pass | 3D (0.73) **≠** |
| 6 | W | P | BEN |  |  |
| 7 | N | P | US | ballow_pass | P (1.00) |

### Table B — we are EW, BEN is NS

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | E | 1C | US | open_1C | 1C (1.00) |
| 1 | S | 1D | BEN |  |  |
| 2 | W | 1S | US | cl_new_S1 | 1S (1.00) |
| 3 | N | P | BEN |  |  |
| 4 | E | P | US | uc_pass | 2S (0.82) **≠** ← FIRST DIVERGENCE |
| 5 | S | 2D | BEN |  |  |
| 6 | W | P | US | cl_pass | P (0.97) |
| 7 | N | P | BEN |  |  |
| 8 | E | P | US | ballow_pass | 2S (0.72) **≠** |

### First divergence: table A, call 3, seat N

auction so far: `1C 1D 1S`, hand `QJ954.KQ8.62.JT2`

| call | rule | fit | score | prio | shows |
|---|---|---|---|---|---|
| P | cl_pass | 1.000 | 0.760 | 20.0 | no bid describes this hand: passing is the general agreement |
| 1NT | cl_nt1 **← DECIDED** | 0.965 | 0.754 | 27.0 | natural 1NT: 8-11 balanced with a stopper in their suit |
| X | cl_negative_X1 | 0.349 | 0.279 | 33.0 | negative double: 6+ HCP with a major they have not bid |
| 2D | cl_raise_D2 | 0.349 | 0.276 | 30.0 | competitive raise of partner's D: 3+ trumps, 6-9 support points, 7+ co |
| 2NT | cl_nt2 | 0.162 | 0.127 | 28.0 | natural 2NT: 11-12 balanced with a stopper in their suit |
| 2H | cl_new_H2 | 0.015 | 0.012 | 26.0 | natural H at the cheapest level: 5+ cards, 10+ points |
| 2H | cl_new_H2_hi | 0.002 | 0.002 | 26.5 | natural H at the cheapest level: 5+ cards, 10+ points (my longest suit |
| 3NT | cl_nt3 | 0.001 | 0.001 | 29.0 | natural 3NT: 13-19 balanced with a stopper in their suit |
| 2H | cl_new_long2_H | 0.000 | 0.000 | 26.0 | natural H at the cheapest level: a SIX-card suit, 8+ points |
| 2H | cl_new_long2_H_hi | 0.000 | 0.000 | 26.5 | natural H at the cheapest level: a SIX-card suit, 8+ points (my longes |
| 4D | cl_raise_D4 | 0.000 | 0.000 | 27.0 | competitive raise of partner's D: 11+ support points, a real trump fit |

---

## Board 187 — margin -1 IMPs

dealer **W**, vul **EW**, par(N/S) **+110**

    N  9.Q96.AKQ76.AJ94   (16 HCP)
    E  QT54.543.543.KQ8   (7 HCP)
    S  KJ8632.T72.9.753   (4 HCP)
    W  A7.AKJ8.JT82.T62   (13 HCP)

Double-dummy tricks:

| declarer | C | D | H | S | NT |
|---|---|---|---|---|---|
| N | 8 | 7 | 6 | 8 | 6 |
| E | 5 | 6 | 5 | 5 | 7 |
| S | 8 | 7 | 6 | 8 | 6 |
| W | 5 | 6 | 5 | 5 | 7 |

Table A (**we are N/S**): 1NT by W (7 tricks), N/S score -90  
Table B (**we are E/W**): 3S by N (8 tricks), N/S score -50  
IMP margin for us: **-1**

### Table A — we are NS, BEN is EW

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | W | 1D | BEN |  |  |
| 1 | N | X | US | oc1D_X | 1NT (0.66) **≠** ← FIRST DIVERGENCE |
| 2 | E | 1S | BEN |  |  |
| 3 | S | P | US | cl_pass | P (0.84) |
| 4 | W | 1NT | BEN |  |  |
| 5 | N | P | US | cl_pass | P (0.71) |
| 6 | E | P | BEN |  |  |
| 7 | S | P | US | ballow_pass | P (0.99) |

### Table B — we are EW, BEN is NS

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | W | 1D | US | open_1D | 1D (1.00) |
| 1 | N | 1NT | BEN |  |  |
| 2 | E | P | US | cl_pass | P (1.00) |
| 3 | S | 2H | BEN |  |  |
| 4 | W | P | US | cl_pass | P (1.00) |
| 5 | N | 2S | BEN |  |  |
| 6 | E | P | US | cl_pass | P (1.00) |
| 7 | S | 3S | BEN |  |  |
| 8 | W | P | US | ch_pass | P (1.00) |
| 9 | N | P | BEN |  |  |
| 10 | E | P | US | balhigh_pass | P (1.00) |

### First divergence: table A, call 1, seat N

auction so far: `1D`, hand `9.Q96.AKQ76.AJ94`

| call | rule | fit | score | prio | shows |
|---|---|---|---|---|---|
| X | oc1D_X **← DECIDED** | 0.800 | 0.733 | 72.0 | takeout double: opening values, short diamonds, no five-card major (or |
| P | oc1D_pass | 0.800 | 0.620 | 25.0 | nothing suitable over 1D |
| 2C | oc1D_2C | 0.349 | 0.312 | 65.0 | 2-level overcall: 5+ good clubs, 11-17 |
| 1H | oc1D_1H | 0.015 | 0.014 | 71.0 | overcall: 5+ hearts, 8-16 |
| 1NT | oc1D_1NT | 0.000 | 0.000 | 82.0 | 1NT overcall: 15-18 balanced with a diamond stopper |
| 3C | oc1D_3C_jump | 0.000 | 0.000 | 59.0 | weak jump overcall: 6+ clubs, 5-10 |
| 3C | oc1D_3C_preempt | 0.000 | 0.000 | 58.0 | preemptive overcall: seven-card c suit, 3-10 |
| 1S | oc1D_1S | 0.000 | 0.000 | 71.0 | overcall: 5+ spades, 8-16 |
| 2H | oc1D_2H_jump | 0.000 | 0.000 | 60.0 | weak jump overcall: 6 hearts, 5-10 |
| 3H | oc1D_3H_preempt | 0.000 | 0.000 | 58.0 | preemptive overcall: seven-card h suit, 3-10 |
| 4H | oc1D_4H_preempt | 0.000 | 0.000 | 59.0 | preemptive overcall: eight-card h suit, 3-10 |
| 2S | oc1D_2S_jump | 0.000 | 0.000 | 60.0 | weak jump overcall: 6 spades, 5-10 |
| 3S | oc1D_3S_preempt | 0.000 | 0.000 | 58.0 | preemptive overcall: seven-card s suit, 3-10 |
| 4S | oc1D_4S_preempt | 0.000 | 0.000 | 59.0 | preemptive overcall: eight-card s suit, 3-10 |

---

## Board 213 — margin -1 IMPs

dealer **E**, vul **NS**, par(N/S) **-140**

    N  K87.962.875.KT32   (6 HCP)
    E  Q9643.K.AJ.J9765   (11 HCP)
    S  JT.AT753.KQT2.Q8   (12 HCP)
    W  A52.QJ84.9643.A4   (11 HCP)

Double-dummy tricks:

| declarer | C | D | H | S | NT |
|---|---|---|---|---|---|
| N | 5 | 6 | 7 | 4 | 6 |
| E | 8 | 6 | 5 | 9 | 7 |
| S | 5 | 6 | 7 | 4 | 6 |
| W | 8 | 6 | 5 | 9 | 6 |

Table A (**we are N/S**): 3S by E (9 tricks), N/S score -140  
Table B (**we are E/W**): 2H by S (7 tricks), N/S score -100  
IMP margin for us: **-1**

### Table A — we are NS, BEN is EW

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | E | 1S | BEN |  |  |
| 1 | S | 2H | US | oc1S_2H | 2H (0.76) |
| 2 | W | 3H | BEN |  |  |
| 3 | N | P | US | ch_pass | P (0.98) |
| 4 | E | 3S | BEN |  |  |
| 5 | S | P | US | ch_pass | P (1.00) |
| 6 | W | P | BEN |  |  |
| 7 | N | P | US | balhigh_pass | P (1.00) |

### Table B — we are EW, BEN is NS

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | E | P | US | open_pass | 1S (0.93) **≠** ← FIRST DIVERGENCE |
| 1 | S | 1H | BEN |  |  |
| 2 | W | P | US | oc1H_pass | P (1.00) |
| 3 | N | 2H | BEN |  |  |
| 4 | E | P | US | cl_pass | 2S (0.50) **≠** |
| 5 | S | P | BEN |  |  |
| 6 | W | P | US | ballow_pass | P (1.00) |

### First divergence: table B, call 0, seat E

auction so far: `(opening)`, hand `Q9643.K.AJ.J9765`

| call | rule | fit | score | prio | shows |
|---|---|---|---|---|---|
| P | open_pass **← DECIDED** | 1.000 | 0.760 | 20.0 | fewer than opening values |
| 1S | open_1S | 0.800 | 0.754 | 81.0 | 5+ spades, 12-21 HCP |
| 1S | open_1S_rule20 | 0.574 | 0.538 | 79.0 | 5+ spades, light opening satisfying the rule of 20 |
| 2S | open_weak_2S_nv | 0.279 | 0.251 | 66.0 | weak two: 6 spades, 5-10 HCP |
| 1C | open_1C | 0.080 | 0.074 | 73.0 | opening, 3+ clubs (better minor), no 5-card major, 12-21 HCP |
| 1C | open_1C_rule20 | 0.033 | 0.030 | 71.0 | 5+ clubs, light opening satisfying the rule of 20 |
| 3C | open_3C_nv | 0.006 | 0.005 | 60.0 | preempt: 7+ clubs, 3-9 HCP |
| 3S | open_3S_nv | 0.006 | 0.005 | 60.0 | preempt: 7+ spades, 3-9 HCP |
| 1D | open_1D | 0.000 | 0.000 | 74.0 | opening, 3+ diamonds (better minor), no 5-card major, 12-21 HCP |
| 4S | open_4S | 0.000 | 0.000 | 61.0 | preempt: 8+ spades, 3-10 HCP |
| 1D | open_1m_rule20 | 0.000 | 0.000 | 72.0 | 5+ diamonds, light opening satisfying the rule of 20 |
| 1NT | open_1NT | 0.000 | 0.000 | 92.0 | 15-17 balanced (may contain a 5-card major) |
| 2C | open_2C | 0.000 | 0.000 | 96.0 | strong artificial: 22+ HCP or equivalent playing strength |
| 2D | open_weak_2D_nv | 0.000 | 0.000 | 64.0 | weak two: 6 diamonds, 5-10 HCP |

---

## Board 226 — margin -1 IMPs

dealer **S**, vul **None**, par(N/S) **+420**

    N  AQ64.752.AQ83.93   (12 HCP)
    E  87.63.J6.AQJT854   (8 HCP)
    S  KJ2.AK94.KT75.62   (14 HCP)
    W  T953.QJT8.942.K7   (6 HCP)

Double-dummy tricks:

| declarer | C | D | H | S | NT |
|---|---|---|---|---|---|
| N | 6 | 10 | 9 | 10 | 6 |
| E | 7 | 2 | 3 | 3 | 3 |
| S | 6 | 10 | 9 | 10 | 6 |
| W | 7 | 2 | 3 | 3 | 3 |

Table A (**we are N/S**): 3C by E (7 tricks), N/S score +100  
Table B (**we are E/W**): 3D by S (10 tricks), N/S score +130  
IMP margin for us: **-1**

### Table A — we are NS, BEN is EW

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | S | 1D | US | open_1D | 1D (1.00) |
| 1 | W | P | BEN |  |  |
| 2 | N | 1S | US | r1m_1S | 1S (1.00) |
| 3 | E | 3C | BEN |  |  |
| 4 | S | P | US | ch_pass | P (0.75) |
| 5 | W | P | BEN |  |  |
| 6 | N | P | US | balhigh_pass | 3D (0.76) **≠** ← FIRST DIVERGENCE |

### Table B — we are EW, BEN is NS

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | S | 1D | BEN |  |  |
| 1 | W | P | US | oc1D_pass | P (1.00) |
| 2 | N | 1S | BEN |  |  |
| 3 | E | 3C | US | sw_3C | 3C (0.97) |
| 4 | S | P | BEN |  |  |
| 5 | W | P | US | uc_pass | P (0.99) |
| 6 | N | 3D | BEN |  |  |
| 7 | E | P | US | ch_pass | P (1.00) |
| 8 | S | P | BEN |  |  |
| 9 | W | P | US | balhigh_pass | P (0.99) |

### First divergence: table A, call 6, seat N

auction so far: `1D P 1S 3C P P`, hand `AQ64.752.AQ83.93`

| call | rule | fit | score | prio | shows |
|---|---|---|---|---|---|
| P | balhigh_pass **← DECIDED** | 1.000 | 0.763 | 21.0 | nothing worth reopening on: passing it out |
| 3NT | balhigh_nt3 | 0.668 | 0.525 | 29.0 | natural 3NT: 13-19 balanced with a stopper in their suit |
| 3D | balhigh_raise_D3 | 0.082 | 0.065 | 31.0 | competitive raise of partner's D: 3+ trumps, 10+ support points, 8+ co |
| X | balhigh_reopen_X | 0.028 | 0.023 | 41.0 | reopening double: 16+, short in their suit, our side already in |
| 3S | balhigh_rebid_S3 | 0.015 | 0.012 | 29.0 | rebid of my own S: 6+ cards, values for the level opposite partner's s |
| 3H | balhigh_new_H3 | 0.000 | 0.000 | 27.0 | natural H at the cheapest level: 5+ cards, 14+ points |
| 5D | uc_minor_game_5D | 0.000 | 0.000 | 28.0 | accepting to game in the raised minor: 17+ opposite the raise |
| 4D | balhigh_raise_D4 | 0.000 | 0.000 | 27.0 | competitive raise of partner's D: 11+ support points, a real trump fit |
| 4NT | gst_rkc_D | 0.000 | 0.000 | 46.0 | RKC Blackwood 1430 for D: slam values opposite partner's shown range |

---

## Board 263 — margin -1 IMPs

dealer **W**, vul **NS**, par(N/S) **-130**

    N  752.T52.KT843.82   (3 HCP)
    E  84.AKQ.J62.AKQ95   (19 HCP)
    S  AKQJT.J8763.Q7.7   (13 HCP)
    W  963.94.A95.JT643   (5 HCP)

Double-dummy tricks:

| declarer | C | D | H | S | NT |
|---|---|---|---|---|---|
| N | 3 | 6 | 8 | 8 | 4 |
| E | 10 | 7 | 5 | 5 | 8 |
| S | 3 | 6 | 8 | 8 | 4 |
| W | 10 | 7 | 5 | 5 | 8 |

Table A (**we are N/S**): 3C by E (10 tricks), N/S score -130  
Table B (**we are E/W**): 3S by N (8 tricks), N/S score -100  
IMP margin for us: **-1**

### Table A — we are NS, BEN is EW

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | W | P | BEN |  |  |
| 1 | N | P | US | open_pass | P (1.00) |
| 2 | E | 1C | BEN |  |  |
| 3 | S | 1S | US | oc1C_1S | 2C (0.97) **≠** ← FIRST DIVERGENCE |
| 4 | W | 3C | BEN |  |  |
| 5 | N | P | US | ch_pass | P (1.00) |
| 6 | E | P | BEN |  |  |
| 7 | S | P | US | balhigh_pass | P (0.97) |

### Table B — we are EW, BEN is NS

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | W | P | US | open_pass | P (1.00) |
| 1 | N | P | BEN |  |  |
| 2 | E | 1C | US | open_1C | 1C (1.00) |
| 3 | S | 2C | BEN |  |  |
| 4 | W | P | US | cl_pass | 3C (0.82) **≠** ← FIRST DIVERGENCE |
| 5 | N | 3S | BEN |  |  |
| 6 | E | P | US | ch_pass | X (0.58) **≠** |
| 7 | S | P | BEN |  |  |
| 8 | W | P | US | balhigh_pass | P (0.99) |

### First divergence: table A, call 3, seat S

auction so far: `P P 1C`, hand `AKQJT.J8763.Q7.7`

| call | rule | fit | score | prio | shows |
|---|---|---|---|---|---|
| 1S | oc1C_1S **← DECIDED** | 1.000 | 0.913 | 71.0 | overcall: 5+ spades, 8-16 |
| P | oc1C_pass | 1.000 | 0.775 | 25.0 | nothing suitable over 1C |
| 1H | oc1C_1H | 0.757 | 0.692 | 71.0 | overcall: 5+ hearts, 8-16 |
| 2S | oc1C_2S_jump | 0.047 | 0.041 | 60.0 | weak jump overcall: 6 spades, 5-10 |
| X | oc1C_X | 0.043 | 0.039 | 72.0 | takeout double: opening values, short clubs, support for the other sui |
| 2H | oc1C_2H_jump | 0.009 | 0.008 | 60.0 | weak jump overcall: 6 hearts, 5-10 |
| 3S | oc1C_3S_preempt | 0.002 | 0.002 | 58.0 | preemptive overcall: seven-card s suit, 3-10 |
| 3H | oc1C_3H_preempt | 0.001 | 0.001 | 58.0 | preemptive overcall: seven-card h suit, 3-10 |
| 1D | oc1C_1D | 0.000 | 0.000 | 70.0 | overcall: 5+ diamonds, 8-16 |
| 4H | oc1C_4H_preempt | 0.000 | 0.000 | 59.0 | preemptive overcall: eight-card h suit, 3-10 |
| 4S | oc1C_4S_preempt | 0.000 | 0.000 | 59.0 | preemptive overcall: eight-card s suit, 3-10 |
| 1NT | oc1C_1NT | 0.000 | 0.000 | 82.0 | 1NT overcall: 15-18 balanced with a club stopper |
| 2D | oc1C_2D_jump | 0.000 | 0.000 | 60.0 | weak jump overcall: 6 diamonds, 5-10 |
| 3D | oc1C_3D_preempt | 0.000 | 0.000 | 58.0 | preemptive overcall: seven-card d suit, 3-10 |

---

## Board 279 — margin -1 IMPs

dealer **W**, vul **NS**, par(N/S) **-420**

    N  AJ853.64.J83.852   (6 HCP)
    E  K96.AT853.964.T4   (7 HCP)
    S  QT72.KQ2.K72.Q76   (12 HCP)
    W  4.J97.AQT5.AKJ93   (15 HCP)

Double-dummy tricks:

| declarer | C | D | H | S | NT |
|---|---|---|---|---|---|
| N | 3 | 3 | 3 | 5 | 3 |
| E | 10 | 10 | 10 | 8 | 9 |
| S | 3 | 3 | 3 | 5 | 4 |
| W | 9 | 10 | 10 | 7 | 9 |

Table A (**we are N/S**): 1NT by W (9 tricks), N/S score -150  
Table B (**we are E/W**): 2C by W (9 tricks), N/S score -110  
IMP margin for us: **-1**

### Table A — we are NS, BEN is EW

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | W | 1C | BEN |  |  |
| 1 | N | P | US | oc1C_pass | P (1.00) |
| 2 | E | 1H | BEN |  |  |
| 3 | S | P | US | sw_pass | P (0.99) |
| 4 | W | 1NT | BEN |  |  |
| 5 | N | P | US | cl_pass | P (1.00) |
| 6 | E | P | BEN |  |  |
| 7 | S | P | US | ballow_pass | P (1.00) |

### Table B — we are EW, BEN is NS

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | W | 1C | US | open_1C | 1C (1.00) |
| 1 | N | P | BEN |  |  |
| 2 | E | 1H | US | r1m_1H | 1H (1.00) |
| 3 | S | P | BEN |  |  |
| 4 | W | 2C | US | ob_rebid_2C | 1NT (0.88) **≠** ← FIRST DIVERGENCE |
| 5 | N | P | BEN |  |  |
| 6 | E | P | US | rmr_pass | P (0.99) |
| 7 | S | P | BEN |  |  |

### First divergence: table B, call 4, seat W

auction so far: `1C P 1H P`, hand `4.J97.AQT5.AKJ93`

| call | rule | fit | score | prio | shows |
|---|---|---|---|---|---|
| 2C | ob_rebid_2C **← DECIDED** | 1.000 | 0.850 | 50.0 | rebid: 5+ (usually 6) C, minimum |
| 2D | ob_1C1H_2D_reverse | 0.409 | 0.358 | 58.0 | reverse: 4+ diamonds, longer clubs, 17+ |
| 3H | ob_raise_3H | 0.349 | 0.326 | 78.0 | jump raise: 4 H support, invitational (16-18) |
| 4H | ob_raise_4H | 0.279 | 0.259 | 76.0 | game raise: 4 H support, 19+ support points |
| 3C | ob_rebid_3C | 0.279 | 0.236 | 49.0 | jump rebid: 6+ good C, 16-18 |
| 2H | ob_raise_2H | 0.047 | 0.044 | 80.0 | raise: 4 H support, minimum (12-15) |
| 1S | ob_1C1H_1S | 0.000 | 0.000 | 60.0 | 4+ spades, 10-17, unbalanced or 4-4-x-x |
| 1NT | ob_1NT | 0.000 | 0.000 | 57.5 | balanced minimum 12-14, no fit |
| 2NT | ob_2NT | 0.000 | 0.000 | 56.0 | jump: balanced 18-19, no fit |
| 3NT | uc_nt3 | 0.000 | 0.000 | 29.0 | natural 3NT: 13-19 balanced, their suits stopped |

---

## Board 285 — margin -1 IMPs

dealer **E**, vul **Both**, par(N/S) **-1440**

    N  K62.83.J92.AJT43   (9 HCP)
    E  .AJ72.AT7654.KQ2   (14 HCP)
    S  8753.T9654.83.98   (0 HCP)
    W  AQJT94.KQ.KQ.765   (17 HCP)

Double-dummy tricks:

| declarer | C | D | H | S | NT |
|---|---|---|---|---|---|
| N | 4 | 0 | 3 | 2 | 1 |
| E | 9 | 12 | 10 | 10 | 11 |
| S | 4 | 0 | 3 | 2 | 1 |
| W | 9 | 12 | 10 | 10 | 12 |

Table A (**we are N/S**): 3NT by E (11 tricks), N/S score -660  
Table B (**we are E/W**): 4S by W (10 tricks), N/S score -620  
IMP margin for us: **-1**

### Table A — we are NS, BEN is EW

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | E | 1D | BEN |  |  |
| 1 | S | P | US | oc1D_pass | P (1.00) |
| 2 | W | 2S | BEN |  |  |
| 3 | N | P | US | cl_pass | P (1.00) |
| 4 | E | 3D | BEN |  |  |
| 5 | S | P | US | ch_pass | P (1.00) |
| 6 | W | 3S | BEN |  |  |
| 7 | N | P | US | ch_pass | P (1.00) |
| 8 | E | 3NT | BEN |  |  |
| 9 | S | P | US | ch_pass | P (1.00) |
| 10 | W | P | BEN |  |  |
| 11 | N | P | US | balhigh_pass | P (1.00) |

### Table B — we are EW, BEN is NS

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | E | 1D | US | open_1D | 1D (1.00) |
| 1 | S | P | BEN |  |  |
| 2 | W | 1S | US | r1m_1S | 2S (0.93) **≠** ← FIRST DIVERGENCE |
| 3 | N | P | BEN |  |  |
| 4 | E | 2D | US | ob_rebid_2D | 2D (0.99) |
| 5 | S | P | BEN |  |  |
| 6 | W | 4S | US | rmr_4S | 3S (0.89) **≠** |
| 7 | N | P | BEN |  |  |
| 8 | E | P | US | fallback | P (0.96) |
| 9 | S | P | BEN |  |  |

### First divergence: table B, call 2, seat W

auction so far: `1D P`, hand `AQJT94.KQ.KQ.765`

| call | rule | fit | score | prio | shows |
|---|---|---|---|---|---|
| 1S | r1m_1S **← DECIDED** | 1.000 | 0.931 | 77.0 | 4+ spades longer than hearts, five-five in the majors, or a six-card s |
| 2C | r1m_2over1 | 0.349 | 0.318 | 70.0 | 2/1 game forcing: 4+ clubs, 12+ HCP |
| 1H | r1m_1H | 0.000 | 0.000 | 76.0 | 4+ hearts, 6+ HCP (up the line), or a six-card suit on 3+ |
| 1NT | r1m_1NT | 0.000 | 0.000 | 45.0 | 6-10 HCP, no 4-card major |
| 3NT | r1m_3NT | 0.000 | 0.000 | 55.0 | 13-15 balanced, no 4-card major |
| 3D | r1m_raise3 | 0.000 | 0.000 | 52.0 | limit raise: 5+ D support, 10-12 HCP, no 4-card major |
| 2D | r1D_raise2 | 0.000 | 0.000 | 50.0 | simple raise: 4+ diamond support, 6-10 HCP, no 4-card major |
| 2NT | r1m_2NT | 0.000 | 0.000 | 54.0 | invitational: 11-12 balanced, no 4-card major |
| 5D | uc_minor_game_5D | 0.000 | 0.000 | 28.0 | accepting to game in the raised minor: 17+ opposite the raise |
| P | r1m_pass | 0.000 | 0.000 | 15.0 | 0-5 HCP: too weak to respond |
| 4D | uc_raise_D4 | 0.000 | 0.000 | 27.0 | raise of partner's D: 11+ support points, a real trump fit, and the va |

---

## Board 286 — margin -1 IMPs

dealer **S**, vul **Both**, par(N/S) **+620**

    N  98742.AJ72.AK6.3   (12 HCP)
    E  J5.T.T8732.AQT64   (7 HCP)
    S  AT63.9843.Q4.875   (6 HCP)
    W  KQ.KQ65.J95.KJ92   (15 HCP)

Double-dummy tricks:

| declarer | C | D | H | S | NT |
|---|---|---|---|---|---|
| N | 5 | 5 | 9 | 10 | 6 |
| E | 8 | 8 | 4 | 3 | 6 |
| S | 5 | 5 | 9 | 10 | 6 |
| W | 8 | 8 | 4 | 3 | 6 |

Table A (**we are N/S**): 3C by W (8 tricks), N/S score +100  
Table B (**we are E/W**): 2H by S (9 tricks), N/S score +140  
IMP margin for us: **-1**

### Table A — we are NS, BEN is EW

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | S | P | US | open_pass | P (1.00) |
| 1 | W | 1NT | BEN |  |  |
| 2 | N | P | US | v1NT_pass | 2D (0.93) **≠** ← FIRST DIVERGENCE |
| 3 | E | 2S | BEN |  |  |
| 4 | S | P | US | cl_pass | P (1.00) |
| 5 | W | 3C | BEN |  |  |
| 6 | N | P | US | ch_pass | P (1.00) |
| 7 | E | P | BEN |  |  |
| 8 | S | P | US | balhigh_pass | P (1.00) |

### Table B — we are EW, BEN is NS

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | S | P | BEN |  |  |
| 1 | W | 1NT | US | open_1NT | 1NT (1.00) |
| 2 | N | 2D | BEN |  |  |
| 3 | E | P | US | cl_pass | P (0.54) |
| 4 | S | 2H | BEN |  |  |
| 5 | W | P | US | cl_pass | P (1.00) |
| 6 | N | P | BEN |  |  |
| 7 | E | P | US | ballow_pass | 3C (0.73) **≠** ← FIRST DIVERGENCE |

### First divergence: table A, call 2, seat N

auction so far: `P 1NT`, hand `98742.AJ72.AK6.3`

| call | rule | fit | score | prio | shows |
|---|---|---|---|---|---|
| P | v1NT_pass **← DECIDED** | 1.000 | 0.790 | 30.0 | nothing suitable over 1NT |
| 2S | v1NT_2S | 0.200 | 0.177 | 61.0 | natural: 5+ spades (usually 6), 8-15 |
| X | v1NT_X | 0.134 | 0.122 | 70.0 | penalty double of 1NT: 15+ |
| 2H | v1NT_2H | 0.070 | 0.062 | 61.0 | natural: 5+ hearts (usually 6), 8-15 |
| 2D | v1NT_2D | 0.000 | 0.000 | 60.0 | natural: 6+ diamonds, 8-15 |
| 2NT | FALLBACK | 0.000 | 0.000 | 10.0 | natural NT, 11-14 HCP, stoppers in their suit(s) (undiscussed) |
| 2C | v1NT_2C | 0.000 | 0.000 | 60.0 | natural: 6+ clubs, 8-15 |

---

## Board 295 — margin -1 IMPs

dealer **W**, vul **NS**, par(N/S) **-420**

    N  654.K765.T74.QJ7   (6 HCP)
    E  AQ832.AJ8.95.T54   (11 HCP)
    S  K9.QT93.K2.A8632   (12 HCP)
    W  JT7.42.AQJ863.K9   (11 HCP)

Double-dummy tricks:

| declarer | C | D | H | S | NT |
|---|---|---|---|---|---|
| N | 7 | 2 | 7 | 2 | 2 |
| E | 5 | 10 | 5 | 10 | 9 |
| S | 7 | 2 | 7 | 2 | 2 |
| W | 5 | 10 | 5 | 10 | 9 |

Table A (**we are N/S**): 3S by E (10 tricks), N/S score -170  
Table B (**we are E/W**): 2NT by E (9 tricks), N/S score -150  
IMP margin for us: **-1**

### Table A — we are NS, BEN is EW

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | W | 1D | BEN |  |  |
| 1 | N | P | US | oc1D_pass | P (1.00) |
| 2 | E | 1S | BEN |  |  |
| 3 | S | X | US | sw_X | P (0.47) **≠** ← FIRST DIVERGENCE |
| 4 | W | XX | BEN |  |  |
| 5 | N | 2H | US | rr_run_H2 | 2H (1.00) |
| 6 | E | 3S | BEN |  |  |
| 7 | S | P | US | ch_pass | P (1.00) |
| 8 | W | P | BEN |  |  |
| 9 | N | P | US | balhigh_pass | P (1.00) |

### Table B — we are EW, BEN is NS

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | W | 1D | US | open_1D | 1D (0.85) |
| 1 | N | P | BEN |  |  |
| 2 | E | 1S | US | r1m_1S | 1S (1.00) |
| 3 | S | P | BEN |  |  |
| 4 | W | 2D | US | ob_rebid_2D | 2D (1.00) |
| 5 | N | P | BEN |  |  |
| 6 | E | 2NT | US | rmr_2NT | 3D (0.65) **≠** ← FIRST DIVERGENCE |
| 7 | S | P | BEN |  |  |
| 8 | W | P | US | oim2n_pass_S2D | 3D (0.43) **≠** |
| 9 | N | P | BEN |  |  |

### First divergence: table A, call 3, seat S

auction so far: `1D P 1S`, hand `K9.QT93.K2.A8632`

| call | rule | fit | score | prio | shows |
|---|---|---|---|---|---|
| X | sw_X **← DECIDED** | 1.000 | 0.910 | 70.0 | takeout of their suits: shortness in opener's suit, or four cards in e |
| P | sw_pass | 1.000 | 0.790 | 30.0 | nothing suitable between two bidding opponents |
| 1NT | FALLBACK | 0.800 | 0.584 | 10.0 | natural NT, 6-11 HCP, stoppers in their suit(s) (undiscussed) |
| 2C | sw_2C | 0.329 | 0.296 | 66.0 | sandwich 2-level overcall: good 5+ clubs, 11-17 |
| 2H | sw_2H | 0.264 | 0.237 | 66.0 | sandwich 2-level overcall: good 5+ hearts, 11-17 |
| 3C | sw_3C | 0.005 | 0.004 | 69.5 | sandwich preemptive jump: seven-card c suit, 3-10 |
| 3H | sw_3H | 0.000 | 0.000 | 69.5 | sandwich preemptive jump: seven-card h suit, 3-10 |

---

## Board 328 — margin -1 IMPs

dealer **N**, vul **EW**, par(N/S) **+140**

    N  AKT5.973.KQ632.6   (12 HCP)
    E  763.AK4.A875.J32   (12 HCP)
    S  QJ42.QJ2.JT.QT87   (9 HCP)
    W  98.T865.94.AK954   (7 HCP)

Double-dummy tricks:

| declarer | C | D | H | S | NT |
|---|---|---|---|---|---|
| N | 5 | 8 | 5 | 9 | 6 |
| E | 8 | 5 | 7 | 4 | 6 |
| S | 5 | 8 | 5 | 9 | 6 |
| W | 8 | 5 | 7 | 4 | 6 |

Table A (**we are N/S**): 2H by E (7 tricks), N/S score +100  
Table B (**we are E/W**): 2S by S (9 tricks), N/S score +140  
IMP margin for us: **-1**

### Table A — we are NS, BEN is EW

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | N | 1D | US | open_1D | 1D (1.00) |
| 1 | E | X | BEN |  |  |
| 2 | S | 1S | US | rx_D_1S | 1S (1.00) |
| 3 | W | X | BEN |  |  |
| 4 | N | P | US | xd_pass | 2S (0.98) **≠** ← FIRST DIVERGENCE |
| 5 | E | 2H | BEN |  |  |
| 6 | S | P | US | cl_pass | P (0.99) |
| 7 | W | P | BEN |  |  |
| 8 | N | P | US | ballow_pass | 2S (0.73) **≠** |

### Table B — we are EW, BEN is NS

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | N | 1D | BEN |  |  |
| 1 | E | P | US | oc1D_pass | X (0.86) **≠** ← FIRST DIVERGENCE |
| 2 | S | 1S | BEN |  |  |
| 3 | W | P | US | sw_pass | P (1.00) |
| 4 | N | 2S | BEN |  |  |
| 5 | E | P | US | cl_pass | P (1.00) |
| 6 | S | P | BEN |  |  |
| 7 | W | P | US | ballow_pass | P (1.00) |

### First divergence: table A, call 4, seat N

auction so far: `1D X 1S X`, hand `AKT5.973.KQ632.6`

| call | rule | fit | score | prio | shows |
|---|---|---|---|---|---|
| P | xd_pass **← DECIDED** | 1.000 | 0.754 | 18.0 | sitting for their double: no better spot to run to |
| 2D | xd_rebid_D2 | 0.349 | 0.280 | 34.0 | rebid of my own doubled D: 6+ cards, 11+ points |
| 3S | xd_jumpraise_S3 | 0.082 | 0.065 | 32.0 | jump raise of partner's doubled S: 4+ trumps, 10+ support points |
| 2H | xd_run_H2 | 0.015 | 0.011 | 25.0 | running to my own H: 5+ cards |
| 2S | xd_raise_S2 | 0.000 | 0.000 | 30.0 | raise of partner's doubled S: 3+ trumps, 6-9 support points |
| 1NT | FALLBACK | 0.000 | 0.000 | 10.0 | natural NT, 6-11 HCP, stoppers in their suit(s) (undiscussed) |
| 2C | xd_run_C2 | 0.000 | 0.000 | 25.0 | running to my own C: 5+ cards |

---

## Board 356 — margin -1 IMPs

dealer **N**, vul **NS**, par(N/S) **-400**

    N  9543.Q83.Q4.JT96   (5 HCP)
    E  AK6.K54.KJT763.5   (14 HCP)
    S  QT87.AJT76.A8.82   (11 HCP)
    W  J2.92.952.AKQ743   (10 HCP)

Double-dummy tricks:

| declarer | C | D | H | S | NT |
|---|---|---|---|---|---|
| N | 4 | 2 | 7 | 7 | 3 |
| E | 9 | 11 | 6 | 6 | 8 |
| S | 4 | 2 | 6 | 7 | 3 |
| W | 9 | 10 | 6 | 5 | 7 |

Table A (**we are N/S**): 3D by E (11 tricks), N/S score -150  
Table B (**we are E/W**): 2C by W (9 tricks), N/S score -110  
IMP margin for us: **-1**

### Table A — we are NS, BEN is EW

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | N | P | US | open_pass | P (1.00) |
| 1 | E | 1D | BEN |  |  |
| 2 | S | 1H | US | oc1D_1H | 1H (1.00) |
| 3 | W | 2C | BEN |  |  |
| 4 | N | 2H | US | cl_raise_H2 | P (1.00) **≠** ← FIRST DIVERGENCE |
| 5 | E | 3D | BEN |  |  |
| 6 | S | P | US | ch_pass | P (0.70) |
| 7 | W | P | BEN |  |  |
| 8 | N | P | US | balhigh_pass | P (1.00) |

### Table B — we are EW, BEN is NS

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | N | P | BEN |  |  |
| 1 | E | 1D | US | open_1D | 1D (1.00) |
| 2 | S | 1H | BEN |  |  |
| 3 | W | 2C | US | cl_new_C2 | 2C (0.96) |
| 4 | N | P | BEN |  |  |
| 5 | E | P | US | uc_pass | 2D (0.71) **≠** ← FIRST DIVERGENCE |
| 6 | S | P | BEN |  |  |

### First divergence: table A, call 4, seat N

auction so far: `P 1D 1H 2C`, hand `9543.Q83.Q4.JT96`

| call | rule | fit | score | prio | shows |
|---|---|---|---|---|---|
| 2H | cl_raise_H2 **← DECIDED** | 1.000 | 0.790 | 30.0 | competitive raise of partner's H: 3+ trumps, 6-9 support points, 7+ co |
| P | cl_pass | 1.000 | 0.760 | 20.0 | no bid describes this hand: passing is the general agreement |
| X | cl_negative_X2 | 0.134 | 0.107 | 33.0 | negative double at the two level: 8+ HCP with a major they have not bi |
| 2S | cl_new_long2_S_hi | 0.001 | 0.001 | 26.5 | natural S at the cheapest level: a SIX-card suit, 8+ points (my longes |
| 2S | cl_new_long2_S | 0.001 | 0.001 | 26.0 | natural S at the cheapest level: a SIX-card suit, 8+ points |
| 2S | cl_new_S2_hi | 0.000 | 0.000 | 26.5 | natural S at the cheapest level: 5+ cards, 10+ points (my longest suit |
| 2S | cl_new_S2 | 0.000 | 0.000 | 26.0 | natural S at the cheapest level: 5+ cards, 10+ points |
| 4H | cl_raise_lott4_H | 0.000 | 0.000 | 32.0 | the Law at the four level: they have a fit and so have we, ten-plus tr |
| 2NT | cl_nt2 | 0.000 | 0.000 | 28.0 | natural 2NT: 11-12 balanced with a stopper in their suit |
| 4H | cl_raise_H4 | 0.000 | 0.000 | 32.0 | competitive raise of partner's H: 11+ support points, a real trump fit |
| 3NT | cl_nt3 | 0.000 | 0.000 | 29.0 | natural 3NT: 13-19 balanced with a stopper in their suit |
| 4NT | gst_rkc_H | 0.000 | 0.000 | 46.0 | RKC Blackwood 1430 for H: slam values opposite partner's shown range |

---

## Board 361 — margin -1 IMPs

dealer **E**, vul **EW**, par(N/S) **-140**

    N  T72.63.AKJ96.T82   (8 HCP)
    E  3.AT52.8742.AJ94   (9 HCP)
    S  A98.K97.T53.K653   (10 HCP)
    W  KQJ654.QJ84.Q.Q7   (13 HCP)

Double-dummy tricks:

| declarer | C | D | H | S | NT |
|---|---|---|---|---|---|
| N | 6 | 8 | 4 | 4 | 7 |
| E | 5 | 5 | 9 | 8 | 5 |
| S | 6 | 8 | 4 | 4 | 7 |
| W | 5 | 5 | 9 | 8 | 5 |

Table A (**we are N/S**): 3H by W (9 tricks), N/S score -140  
Table B (**we are E/W**): 2S by W (8 tricks), N/S score -110  
IMP margin for us: **-1**

### Table A — we are NS, BEN is EW

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | E | P | BEN |  |  |
| 1 | S | P | US | open_pass | P (1.00) |
| 2 | W | 1S | BEN |  |  |
| 3 | N | P | US | oc1S_pass | P (1.00) |
| 4 | E | 1NT | BEN |  |  |
| 5 | S | P | US | sw_pass | P (1.00) |
| 6 | W | 2H | BEN |  |  |
| 7 | N | P | US | cl_pass | P (1.00) |
| 8 | E | 3H | BEN |  |  |
| 9 | S | P | US | ch_pass | P (1.00) |
| 10 | W | P | BEN |  |  |
| 11 | N | P | US | balhigh_pass | P (1.00) |

### Table B — we are EW, BEN is NS

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | E | P | US | open_pass | P (1.00) |
| 1 | S | P | BEN |  |  |
| 2 | W | 1S | US | open_1S | 1S (1.00) |
| 3 | N | P | BEN |  |  |
| 4 | E | 1NT | US | r1S_1NT | 1NT (1.00) |
| 5 | S | P | BEN |  |  |
| 6 | W | 2S | US | ob_1M1NT_2S | 2H (0.99) **≠** ← FIRST DIVERGENCE |
| 7 | N | P | BEN |  |  |
| 8 | E | P | US | uc_pass | P (0.93) |
| 9 | S | P | BEN |  |  |

### First divergence: table B, call 6, seat W

auction so far: `P P 1S P 1NT P`, hand `KQJ654.QJ84.Q.Q7`

| call | rule | fit | score | prio | shows |
|---|---|---|---|---|---|
| 2S | ob_1M1NT_2S **← DECIDED** | 1.000 | 0.862 | 54.0 | 6+ S, minimum |
| 3S | ob_1M1NT_3S | 0.800 | 0.694 | 56.0 | jump rebid: 6+ good S, 16-19 playing strength |
| 2H | ob_1S1NT_2H | 0.100 | 0.086 | 53.5 | second suit: five spades and 4+ hearts, 12-17 |
| 2C | ob_1M1NT_2C | 0.035 | 0.030 | 52.0 | 3+ clubs, 12-17, no 6-card major |
| 4S | ob_1M1NT_4S | 0.028 | 0.024 | 57.0 | too strong to invite: bidding game opposite 6-11 |
| 2D | ob_1M1NT_2D | 0.000 | 0.000 | 53.0 | 4+ diamonds, 12-17 |
| P | ob_1M1NT_pass | 0.000 | 0.000 | 55.0 | balanced minimum: passing the semi-forcing 1NT |
| 3NT | uc_nt3 | 0.000 | 0.000 | 29.0 | natural 3NT: 13-19 balanced, their suits stopped |
| 2NT | ob_1M1NT_2NT | 0.000 | 0.000 | 51.0 | jump: 18-19 balanced |

---

## Board 401 — margin -1 IMPs

dealer **E**, vul **None**, par(N/S) **+420**

    N  AKT75.J97632.K2.   (11 HCP)
    E  2.Q854.QJT4.KQ74   (10 HCP)
    S  J93.AK.963.AT985   (12 HCP)
    W  Q864.T.A875.J632   (7 HCP)

Double-dummy tricks:

| declarer | C | D | H | S | NT |
|---|---|---|---|---|---|
| N | 6 | 5 | 10 | 10 | 9 |
| E | 6 | 7 | 3 | 2 | 3 |
| S | 6 | 5 | 10 | 10 | 9 |
| W | 7 | 7 | 3 | 2 | 3 |

Table A (**we are N/S**): 3NT by S (9 tricks), N/S score +400  
Table B (**we are E/W**): 4S by N (10 tricks), N/S score +420  
IMP margin for us: **-1**

### Table A — we are NS, BEN is EW

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | E | P | BEN |  |  |
| 1 | S | 1C | US | open_1C | 1C (1.00) |
| 2 | W | P | BEN |  |  |
| 3 | N | 1H | US | r1m_1H | 1H (0.94) |
| 4 | E | P | BEN |  |  |
| 5 | S | 1NT | US | ob_1NT | 1NT (1.00) |
| 6 | W | P | BEN |  |  |
| 7 | N | 2S | US | rr_nt_second_S | 2D (0.60) **≠** ← FIRST DIVERGENCE |
| 8 | E | P | BEN |  |  |
| 9 | S | 2NT | US | uc_nt2 | 3NT (0.65) **≠** |
| 10 | W | P | BEN |  |  |
| 11 | N | 3NT | US | uc_nt3 | 4H (0.29) **≠** |
| 12 | E | P | BEN |  |  |
| 13 | S | P | US | fallback | P (0.97) |
| 14 | W | P | BEN |  |  |

### Table B — we are EW, BEN is NS

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | E | P | US | open_pass | P (1.00) |
| 1 | S | 1C | BEN |  |  |
| 2 | W | P | US | oc1C_pass | P (1.00) |
| 3 | N | 1H | BEN |  |  |
| 4 | E | P | US | sw_pass | P (1.00) |
| 5 | S | 1NT | BEN |  |  |
| 6 | W | P | US | cl_pass | P (1.00) |
| 7 | N | 2D | BEN |  |  |
| 8 | E | P | US | cl_pass | P (1.00) |
| 9 | S | 3NT | BEN |  |  |
| 10 | W | P | US | ch_pass | P (1.00) |
| 11 | N | 4S | BEN |  |  |
| 12 | E | P | US | ch_pass | P (1.00) |
| 13 | S | P | BEN |  |  |
| 14 | W | P | US | balhigh_pass | P (1.00) |

### First divergence: table A, call 7, seat N

auction so far: `P 1C P 1H P 1NT P`, hand `AKT75.J97632.K2.`

| call | rule | fit | score | prio | shows |
|---|---|---|---|---|---|
| 2S | rr_nt_second_S **← DECIDED** | 1.000 | 0.854 | 51.5 | 5-4: the second suit, to play |
| 2H | rr_nt_2H | 1.000 | 0.853 | 51.0 | 6+ H, 6-11, to play - with no invitational 3H available, eleven signs  |
| 3H | rr_nt_gf3_H | 0.800 | 0.688 | 53.5 | 5+ H, game forcing: asking for three-card support |
| P | rr_nt_pass | 0.800 | 0.680 | 50.0 | no game interest opposite 12-14 |
| 4H | rr_nt_4H | 0.409 | 0.352 | 53.0 | 6+ H, game values |
| 2NT | rr_nt_2NT | 0.100 | 0.086 | 52.0 | invitational 11-12 |
| 3NT | rr_nt_3NT | 0.041 | 0.035 | 54.0 | to play |
| 2D | uc_new_D2 | 0.000 | 0.000 | 26.0 | natural D at the cheapest level: 5+ cards, 10+ points |
| 3H | rr_nt_slam3_H | 0.000 | 0.000 | 56.0 | 5+ H with slam values opposite the 12-14 rebid |
| 2D | uc_new_D2_hi | 0.000 | 0.000 | 26.5 | natural D at the cheapest level: 5+ cards, 10+ points (my longest suit |
| 4NT | rr_nt_4NT | 0.000 | 0.000 | 55.0 | quantitative: 17-18 opposite the 12-14 rebid, inviting slam |
| 2C | uc_raise_C2 | 0.000 | 0.000 | 30.0 | raise of partner's C: 3+ trumps, 6-9 support points, 7+ combined trump |
| 5C | uc_minor_game_5C | 0.000 | 0.000 | 28.0 | accepting to game in the raised minor: 17+ opposite the raise |
| 4C | uc_raise_C4 | 0.000 | 0.000 | 27.0 | raise of partner's C: 11+ support points, a real trump fit, and the va |

---

## Board 427 — margin -1 IMPs

dealer **W**, vul **EW**, par(N/S) **+420**

    N  J765.KJ2.4.AJT42   (10 HCP)
    E  T3.765.AKQT3.K65   (12 HCP)
    S  AKQ4.Q84.9875.93   (11 HCP)
    W  982.AT93.J62.Q87   (7 HCP)

Double-dummy tricks:

| declarer | C | D | H | S | NT |
|---|---|---|---|---|---|
| N | 10 | 6 | 6 | 10 | 6 |
| E | 3 | 7 | 6 | 3 | 6 |
| S | 10 | 6 | 6 | 10 | 6 |
| W | 3 | 7 | 6 | 3 | 6 |

Table A (**we are N/S**): 2C by N (10 tricks), N/S score +130  
Table B (**we are E/W**): 2S by S (10 tricks), N/S score +170  
IMP margin for us: **-1**

### Table A — we are NS, BEN is EW

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | W | P | BEN |  |  |
| 1 | N | P | US | open_pass | P (0.98) |
| 2 | E | 1D | BEN |  |  |
| 3 | S | P | US | oc1D_pass | P (1.00) |
| 4 | W | 1H | BEN |  |  |
| 5 | N | P | US | sw_pass | 1NT (0.99) **≠** ← FIRST DIVERGENCE |
| 6 | E | 1NT | BEN |  |  |
| 7 | S | P | US | cl_pass | P (1.00) |
| 8 | W | P | BEN |  |  |
| 9 | N | 2C | US | ballow_new_C2 | P (1.00) **≠** |
| 10 | E | P | BEN |  |  |
| 11 | S | P | US | uc_pass | P (0.81) |
| 12 | W | P | BEN |  |  |

### Table B — we are EW, BEN is NS

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | W | P | US | open_pass | P (1.00) |
| 1 | N | P | BEN |  |  |
| 2 | E | 1D | US | open_1D | 1D (1.00) |
| 3 | S | P | BEN |  |  |
| 4 | W | 1H | US | r1m_1H | 1H (1.00) |
| 5 | N | 1NT | BEN |  |  |
| 6 | E | X | US | sd_double | X (1.00) |
| 7 | S | 2S | BEN |  |  |
| 8 | W | P | US | cl_pass | P (0.99) |
| 9 | N | P | BEN |  |  |
| 10 | E | P | US | ballow_pass | P (0.97) |

### First divergence: table A, call 5, seat N

auction so far: `P P 1D P 1H`, hand `J765.KJ2.4.AJT42`

| call | rule | fit | score | prio | shows |
|---|---|---|---|---|---|
| P | sw_pass **← DECIDED** | 1.000 | 0.790 | 30.0 | nothing suitable between two bidding opponents |
| 2C | sw_2C | 0.800 | 0.718 | 66.0 | sandwich 2-level overcall: good 5+ clubs, 11-17 |
| X | sw_X | 0.409 | 0.373 | 70.0 | takeout of their suits: shortness in opener's suit, or four cards in e |
| 1S | sw_1S | 0.115 | 0.104 | 68.0 | sandwich overcall: good 5+ spades, 8-16 |
| 2S | sw_2S | 0.023 | 0.021 | 66.0 | sandwich 2-level overcall: good 5+ spades, 11-17 |
| 3C | sw_3C | 0.015 | 0.013 | 69.5 | sandwich preemptive jump: seven-card c suit, 3-10 |
| 2S | sw_2S_jump | 0.003 | 0.003 | 69.0 | sandwich weak jump overcall: 6+ s, 5-10 |
| 3S | sw_3S | 0.000 | 0.000 | 69.5 | sandwich preemptive jump: seven-card s suit, 3-10 |
| 1NT | FALLBACK | 0.000 | 0.000 | 10.0 | natural NT, 6-11 HCP, stoppers in their suit(s) (undiscussed) |

---

## Board 551 — margin -1 IMPs

dealer **W**, vul **NS**, par(N/S) **-980**

    N  5.KQT87.KQ643.32   (10 HCP)
    E  T764.6.JT52.AJ75   (6 HCP)
    S  K92.AJ532.987.Q6   (10 HCP)
    W  AQJ83.94.A.KT984   (14 HCP)

Double-dummy tricks:

| declarer | C | D | H | S | NT |
|---|---|---|---|---|---|
| N | 0 | 8 | 8 | 1 | 2 |
| E | 12 | 5 | 4 | 12 | 8 |
| S | 0 | 8 | 8 | 1 | 2 |
| W | 12 | 5 | 4 | 12 | 8 |

Table A (**we are N/S**): 3S by W (12 tricks), N/S score -230  
Table B (**we are E/W**): 4H by S (8 tricks), N/S score -200  
IMP margin for us: **-1**

### Table A — we are NS, BEN is EW

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | W | 1S | BEN |  |  |
| 1 | N | P | US | oc1S_pass | 2S (0.92) **≠** ← FIRST DIVERGENCE |
| 2 | E | 2S | BEN |  |  |
| 3 | S | P | US | cl_pass | P (1.00) |
| 4 | W | 3C | BEN |  |  |
| 5 | N | P | US | ch_pass | P (1.00) |
| 6 | E | 3S | BEN |  |  |
| 7 | S | P | US | ch_pass | P (1.00) |
| 8 | W | P | BEN |  |  |
| 9 | N | P | US | balhigh_pass | P (1.00) |

### Table B — we are EW, BEN is NS

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | W | 1S | US | open_1S | 1S (1.00) |
| 1 | N | 2S | BEN |  |  |
| 2 | E | 3S | US | cl_raise_lott3_S | X (0.33) **≠** ← FIRST DIVERGENCE |
| 3 | S | 4H | BEN |  |  |
| 4 | W | P | US | ch_pass | 4S (0.57) **≠** |
| 5 | N | P | BEN |  |  |
| 6 | E | P | US | balhigh_pass | P (0.75) |

### First divergence: table A, call 1, seat N

auction so far: `1S`, hand `5.KQT87.KQ643.32`

| call | rule | fit | score | prio | shows |
|---|---|---|---|---|---|
| P | oc1S_pass **← DECIDED** | 1.000 | 0.775 | 25.0 | nothing suitable over 1S |
| 2D | oc1S_2D | 0.800 | 0.716 | 65.0 | 2-level overcall: 5+ good diamonds, 11-17 |
| 2H | oc1S_2H | 0.800 | 0.716 | 65.0 | 2-level overcall: 5+ good hearts, 11-17 |
| 3D | oc1S_3D_jump | 0.349 | 0.306 | 59.0 | weak jump overcall: 6+ diamonds, 5-10 |
| 3H | oc1S_3H_jump | 0.349 | 0.306 | 59.0 | weak jump overcall: 6+ hearts, 5-10 |
| X | oc1S_X | 0.097 | 0.089 | 72.0 | takeout double: opening values, short spades, no five-card major (or a |
| 3D | oc1S_3D_preempt | 0.015 | 0.013 | 58.0 | preemptive overcall: seven-card d suit, 3-10 |
| 3H | oc1S_3H_preempt | 0.015 | 0.013 | 58.0 | preemptive overcall: seven-card h suit, 3-10 |
| 4H | oc1S_4H_preempt | 0.000 | 0.000 | 59.0 | preemptive overcall: eight-card h suit, 3-10 |
| 2C | oc1S_2C | 0.000 | 0.000 | 65.0 | 2-level overcall: 5+ good clubs, 11-17 |
| 3C | oc1S_3m_jump | 0.000 | 0.000 | 59.0 | weak jump overcall: 6+ clubs, 5-10 |
| 1NT | oc1S_1NT | 0.000 | 0.000 | 82.0 | 1NT overcall: 15-18 balanced with a spade stopper |
| 3C | oc1S_3C_preempt | 0.000 | 0.000 | 58.0 | preemptive overcall: seven-card c suit, 3-10 |

---

## Board 555 — margin -1 IMPs

dealer **W**, vul **EW**, par(N/S) **+420**

    N  9543.AKQ854.T.94   (9 HCP)
    E  JT76.J932.87.865   (2 HCP)
    S  AK.7.AKJ96432.Q3   (17 HCP)
    W  Q82.T6.Q5.AKJT72   (12 HCP)

Double-dummy tricks:

| declarer | C | D | H | S | NT |
|---|---|---|---|---|---|
| N | 6 | 11 | 10 | 8 | 7 |
| E | 6 | 0 | 1 | 4 | 0 |
| S | 6 | 11 | 10 | 8 | 7 |
| W | 6 | 0 | 1 | 4 | 0 |

Table A (**we are N/S**): 4D by S (11 tricks), N/S score +150  
Table B (**we are E/W**): 3H by N (10 tricks), N/S score +170  
IMP margin for us: **-1**

### Table A — we are NS, BEN is EW

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | W | 1C | BEN |  |  |
| 1 | N | 1H | US | oc1C_1H | 2H (0.87) **≠** ← FIRST DIVERGENCE |
| 2 | E | P | BEN |  |  |
| 3 | S | 2D | US | uc_new_D2 | 2D (0.82) |
| 4 | W | P | BEN |  |  |
| 5 | N | 2H | US | uc_rebid_H2 | 2H (0.83) |
| 6 | E | P | BEN |  |  |
| 7 | S | 3D | US | uc_rebid_D3 | 3D (0.39) |
| 8 | W | P | BEN |  |  |
| 9 | N | 3H | US | uc_rebid_H3 | 3H (0.38) |
| 10 | E | P | BEN |  |  |
| 11 | S | 4D | US | uc_rebid_D4 | 4D (0.36) |
| 12 | W | P | BEN |  |  |
| 13 | N | P | US | uc_pass | P (0.61) |
| 14 | E | P | BEN |  |  |

### Table B — we are EW, BEN is NS

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | W | 1C | US | open_1C | 1C (1.00) |
| 1 | N | 2H | BEN |  |  |
| 2 | E | P | US | nxj_pass | P (1.00) |
| 3 | S | 3D | BEN |  |  |
| 4 | W | P | US | ch_pass | P (1.00) |
| 5 | N | 3H | BEN |  |  |
| 6 | E | P | US | ch_pass | P (1.00) |
| 7 | S | P | BEN |  |  |
| 8 | W | P | US | balhigh_pass | P (1.00) |

### First divergence: table A, call 1, seat N

auction so far: `1C`, hand `9543.AKQ854.T.94`

| call | rule | fit | score | prio | shows |
|---|---|---|---|---|---|
| 1H | oc1C_1H **← DECIDED** | 1.000 | 0.913 | 71.0 | overcall: 5+ hearts, 8-16 |
| 2H | oc1C_2H_jump | 1.000 | 0.880 | 60.0 | weak jump overcall: 6 hearts, 5-10 |
| P | oc1C_pass | 1.000 | 0.775 | 25.0 | nothing suitable over 1C |
| 3H | oc1C_3H_preempt | 0.349 | 0.305 | 58.0 | preemptive overcall: seven-card h suit, 3-10 |
| 1S | oc1C_1S | 0.115 | 0.105 | 71.0 | overcall: 5+ spades, 8-16 |
| 4H | oc1C_4H_preempt | 0.015 | 0.013 | 59.0 | preemptive overcall: eight-card h suit, 3-10 |
| 2S | oc1C_2S_jump | 0.003 | 0.003 | 60.0 | weak jump overcall: 6 spades, 5-10 |
| X | oc1C_X | 0.000 | 0.000 | 72.0 | takeout double: opening values, short clubs, support for the other sui |
| 3S | oc1C_3S_preempt | 0.000 | 0.000 | 58.0 | preemptive overcall: seven-card s suit, 3-10 |
| 4S | oc1C_4S_preempt | 0.000 | 0.000 | 59.0 | preemptive overcall: eight-card s suit, 3-10 |
| 1D | oc1C_1D | 0.000 | 0.000 | 70.0 | overcall: 5+ diamonds, 8-16 |
| 1NT | oc1C_1NT | 0.000 | 0.000 | 82.0 | 1NT overcall: 15-18 balanced with a club stopper |
| 2D | oc1C_2D_jump | 0.000 | 0.000 | 60.0 | weak jump overcall: 6 diamonds, 5-10 |
| 3D | oc1C_3D_preempt | 0.000 | 0.000 | 58.0 | preemptive overcall: seven-card d suit, 3-10 |

---

## Board 631 — margin -1 IMPs

dealer **W**, vul **NS**, par(N/S) **+630**

    N  AQ3.AJT93.AJT.82   (16 HCP)
    E  T9742.72.K9.Q764   (5 HCP)
    S  J8.K854.Q3.KT953   (9 HCP)
    W  K65.Q6.876542.AJ   (10 HCP)

Double-dummy tricks:

| declarer | C | D | H | S | NT |
|---|---|---|---|---|---|
| N | 9 | 7 | 10 | 7 | 9 |
| E | 4 | 6 | 3 | 6 | 3 |
| S | 9 | 7 | 10 | 6 | 10 |
| W | 4 | 6 | 3 | 6 | 3 |

Table A (**we are N/S**): 3NT by N (9 tricks), N/S score +600  
Table B (**we are E/W**): 4H by N (10 tricks), N/S score +620  
IMP margin for us: **-1**

### Table A — we are NS, BEN is EW

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | W | 2D | BEN |  |  |
| 1 | N | 2NT | US | vw2_2NT | 2H (0.99) **≠** ← FIRST DIVERGENCE |
| 2 | E | P | BEN |  |  |
| 3 | S | 3NT | US | a2nw_3NT_D | 3C (0.49) **≠** |
| 4 | W | P | BEN |  |  |
| 5 | N | P | US | fallback | P (0.75) |
| 6 | E | P | BEN |  |  |

### Table B — we are EW, BEN is NS

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | W | P | US | open_pass | 2D (0.92) **≠** ← FIRST DIVERGENCE |
| 1 | N | 1NT | BEN |  |  |
| 2 | E | P | US | v1NT_pass | P (1.00) |
| 3 | S | 2C | BEN |  |  |
| 4 | W | P | US | cl_pass | P (0.64) |
| 5 | N | 2H | BEN |  |  |
| 6 | E | P | US | cl_pass | P (1.00) |
| 7 | S | 4H | BEN |  |  |
| 8 | W | P | US | ch_pass | P (1.00) |
| 9 | N | P | BEN |  |  |
| 10 | E | P | US | balhigh_pass | P (1.00) |

### First divergence: table A, call 1, seat N

auction so far: `2D`, hand `AQ3.AJT93.AJT.82`

| call | rule | fit | score | prio | shows |
|---|---|---|---|---|---|
| 2NT | vw2_2NT **← DECIDED** | 1.000 | 0.916 | 72.0 | 15-18 balanced with a stopper |
| 2H | vw2D_over_2H | 1.000 | 0.892 | 64.0 | natural overcall of the weak two: good 5+ H, 11-16 |
| 2H | vw2_shadow_DH | 1.000 | 0.778 | 26.0 | natural H at the cheapest level: 5+ cards, 10+ points |
| X | vw2_X | 0.800 | 0.728 | 70.0 | takeout double of the weak two |
| P | vw2_pass | 0.409 | 0.323 | 30.0 | nothing to say over the preempt |
| 2S | vw2D_over_2S | 0.015 | 0.013 | 64.0 | natural overcall of the weak two: good 5+ S, 11-16 |
| 2S | vw2_shadow_DS | 0.015 | 0.012 | 26.0 | natural S at the cheapest level: 5+ cards, 10+ points |
| 3C | vw2_shadow3_C | 0.000 | 0.000 | 26.0 | natural C at the cheapest level: 5+ cards, 14+ points |
| 3C | vw2_over3_C | 0.000 | 0.000 | 64.0 | overcalling the weak two at the three level: good 6+ C, 11+ |

---

## Board 642 — margin -1 IMPs

dealer **S**, vul **None**, par(N/S) **+130**

    N  KQ.AJ6.AKQ3.Q963   (21 HCP)
    E  A74.9754.J962.T7   (5 HCP)
    S  J9832.T8.T8.J842   (2 HCP)
    W  T65.KQ32.754.AK5   (12 HCP)

Double-dummy tricks:

| declarer | C | D | H | S | NT |
|---|---|---|---|---|---|
| N | 10 | 8 | 7 | 8 | 8 |
| E | 3 | 5 | 6 | 4 | 5 |
| S | 10 | 8 | 7 | 8 | 8 |
| W | 3 | 5 | 6 | 4 | 5 |

Table A (**we are N/S**): 2H by E (6 tricks), N/S score +100  
Table B (**we are E/W**): 1NT by N (8 tricks), N/S score +120  
IMP margin for us: **-1**

### Table A — we are NS, BEN is EW

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | S | P | US | open_pass | P (1.00) |
| 1 | W | 1C | BEN |  |  |
| 2 | N | X | US | oc1C_X | X (0.99) |
| 3 | E | 1H | BEN |  |  |
| 4 | S | P | US | cl_pass | P (0.76) |
| 5 | W | 2H | BEN |  |  |
| 6 | N | P | US | cl_pass | X (0.65) **≠** ← FIRST DIVERGENCE |
| 7 | E | P | BEN |  |  |
| 8 | S | P | US | ballow_pass | P (0.70) |

### Table B — we are EW, BEN is NS

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | S | P | BEN |  |  |
| 1 | W | 1C | US | open_1C | 1C (1.00) |
| 2 | N | X | BEN |  |  |
| 3 | E | P | US | rdx_pass | 1H (0.98) **≠** ← FIRST DIVERGENCE |
| 4 | S | 1S | BEN |  |  |
| 5 | W | P | US | cl_pass | P (1.00) |
| 6 | N | 1NT | BEN |  |  |
| 7 | E | P | US | cl_pass | P (1.00) |
| 8 | S | P | BEN |  |  |
| 9 | W | P | US | ballow_pass | P (1.00) |

### First divergence: table A, call 6, seat N

auction so far: `P 1C X 1H P 2H`, hand `KQ.AJ6.AKQ3.Q963`

| call | rule | fit | score | prio | shows |
|---|---|---|---|---|---|
| P | cl_pass **← DECIDED** | 1.000 | 0.760 | 20.0 | no bid describes this hand: passing is the general agreement |
| 3D | cl_new_D3_hi | 0.349 | 0.273 | 27.5 | natural D at the cheapest level: 5+ cards, 14+ points (my longest suit |
| 3D | cl_new_D3 | 0.349 | 0.273 | 27.0 | natural D at the cheapest level: 5+ cards, 14+ points |
| 3NT | cl_nt3 | 0.328 | 0.258 | 29.0 | natural 3NT: 13-19 balanced with a stopper in their suit |
| X | FALLBACK | 0.349 | 0.254 | 9.0 | takeout-flavored cooperative double (undiscussed) |
| 3D | cl_new_long3_D_hi | 0.015 | 0.012 | 27.5 | natural D at the cheapest level: a SIX-card suit, 11+ points (my longe |
| 3D | cl_new_long3_D | 0.015 | 0.012 | 27.0 | natural D at the cheapest level: a SIX-card suit, 11+ points |
| 2S | cl_new_S2 | 0.000 | 0.000 | 26.0 | natural S at the cheapest level: 5+ cards, 10+ points |
| 2S | cl_new_S2_hi | 0.000 | 0.000 | 26.5 | natural S at the cheapest level: 5+ cards, 10+ points (my longest suit |
| 2S | cl_new_long2_S | 0.000 | 0.000 | 26.0 | natural S at the cheapest level: a SIX-card suit, 8+ points |
| 2NT | cl_nt2 | 0.000 | 0.000 | 28.0 | natural 2NT: 11-12 balanced with a stopper in their suit |
| 2S | cl_new_long2_S_hi | 0.000 | 0.000 | 26.5 | natural S at the cheapest level: a SIX-card suit, 8+ points (my longes |

---

## Board 643 — margin -1 IMPs

dealer **W**, vul **None**, par(N/S) **+90**

    N  Q762.AJ.AQ942.J9   (14 HCP)
    E  AJT5.3.KJ7.A8752   (13 HCP)
    S  K9.QT986.T8.QT43   (7 HCP)
    W  843.K7542.653.K6   (6 HCP)

Double-dummy tricks:

| declarer | C | D | H | S | NT |
|---|---|---|---|---|---|
| N | 6 | 7 | 6 | 6 | 7 |
| E | 7 | 6 | 6 | 7 | 6 |
| S | 6 | 7 | 6 | 6 | 7 |
| W | 7 | 6 | 6 | 7 | 6 |

Table A (**we are N/S**): 2C by E (7 tricks), N/S score +50  
Table B (**we are E/W**): 1NT by S (7 tricks), N/S score +90  
IMP margin for us: **-1**

### Table A — we are NS, BEN is EW

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | W | P | BEN |  |  |
| 1 | N | 1D | US | open_1D | 1D (1.00) |
| 2 | E | 2C | BEN |  |  |
| 3 | S | P | US | cl_pass | P (0.99) |
| 4 | W | P | BEN |  |  |
| 5 | N | P | US | ballow_pass | X (0.56) **≠** ← FIRST DIVERGENCE |

### Table B — we are EW, BEN is NS

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | W | P | US | open_pass | P (1.00) |
| 1 | N | 1D | BEN |  |  |
| 2 | E | P | US | oc1D_pass | 2C (0.91) **≠** ← FIRST DIVERGENCE |
| 3 | S | 1H | BEN |  |  |
| 4 | W | P | US | sw_pass | P (1.00) |
| 5 | N | 1S | BEN |  |  |
| 6 | E | P | US | cl_pass | P (0.73) |
| 7 | S | 1NT | BEN |  |  |
| 8 | W | P | US | cl_pass | P (1.00) |
| 9 | N | P | BEN |  |  |
| 10 | E | P | US | ballow_pass | P (0.83) |

### First divergence: table A, call 5, seat N

auction so far: `P 1D 2C P P`, hand `Q762.AJ.AQ942.J9`

| call | rule | fit | score | prio | shows |
|---|---|---|---|---|---|
| P | ballow_pass **← DECIDED** | 1.000 | 0.763 | 21.0 | nothing worth reopening on: passing it out |
| X | ballow_reopen_X | 0.409 | 0.337 | 41.0 | reopening double: 16+, short in their suit, our side already in |
| 2D | ballow_rebid_D2 | 0.349 | 0.275 | 29.0 | rebid of my own D: 6+ cards, values for the level opposite partner's s |
| 2S | ballow_new_S2 | 0.264 | 0.206 | 26.0 | natural S at the cheapest level: 5+ cards, 10+ points |
| 2NT | ballow_nt2_strong | 0.112 | 0.088 | 30.0 | natural 2NT: 17-21 balanced with their suit stopped |
| 2S | ballow_new_long2_S | 0.015 | 0.012 | 26.0 | natural S at the cheapest level: a SIX-card suit, 8+ points |
| 2NT | ballow_nt2 | 0.010 | 0.008 | 28.0 | natural 2NT: 11-12 balanced with a stopper in their suit |
| 2H | ballow_new_H2 | 0.000 | 0.000 | 26.0 | natural H at the cheapest level: 5+ cards, 10+ points |
| 3NT | ballow_nt3 | 0.000 | 0.000 | 29.0 | natural 3NT: 13-19 balanced with a stopper in their suit |
| 2H | ballow_new_long2_H | 0.000 | 0.000 | 26.0 | natural H at the cheapest level: a SIX-card suit, 8+ points |

---

## Board 689 — margin -1 IMPs

dealer **E**, vul **None**, par(N/S) **+300**

    N  KT653.A73.Q.JT92   (10 HCP)
    E  Q92.J.JT9.AK8543   (11 HCP)
    S  AJ7.Q652.A632.Q7   (13 HCP)
    W  84.KT984.K8754.6   (6 HCP)

Double-dummy tricks:

| declarer | C | D | H | S | NT |
|---|---|---|---|---|---|
| N | 7 | 4 | 7 | 9 | 8 |
| E | 6 | 8 | 6 | 4 | 4 |
| S | 7 | 4 | 7 | 9 | 9 |
| W | 6 | 8 | 6 | 4 | 4 |

Table A (**we are N/S**): 2C by E (6 tricks), N/S score +100  
Table B (**we are E/W**): 2S by N (9 tricks), N/S score +140  
IMP margin for us: **-1**

### Table A — we are NS, BEN is EW

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | E | 1C | BEN |  |  |
| 1 | S | X | US | oc1C_X | X (0.97) |
| 2 | W | 1H | BEN |  |  |
| 3 | N | 1S | US | cl_new_S1 | 2S (0.37) **≠** ← FIRST DIVERGENCE |
| 4 | E | 2C | BEN |  |  |
| 5 | S | P | US | cl_pass | P (0.67) |
| 6 | W | P | BEN |  |  |
| 7 | N | P | US | ballow_pass | 2S (0.56) **≠** |

### Table B — we are EW, BEN is NS

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | E | 1C | US | open_1C | 1C (0.92) |
| 1 | S | X | BEN |  |  |
| 2 | W | 1D | US | rx_C_1D | 1H (0.93) **≠** ← FIRST DIVERGENCE |
| 3 | N | 1S | BEN |  |  |
| 4 | E | 2C | US | cl_rebid_C2 | 2C (0.65) |
| 5 | S | P | BEN |  |  |
| 6 | W | P | US | uc_pass | 2H (0.43) **≠** |
| 7 | N | 2S | BEN |  |  |
| 8 | E | P | US | cl_pass | P (0.98) |
| 9 | S | P | BEN |  |  |
| 10 | W | P | US | ballow_pass | P (0.73) |

### First divergence: table A, call 3, seat N

auction so far: `1C X 1H`, hand `KT653.A73.Q.JT92`

| call | rule | fit | score | prio | shows |
|---|---|---|---|---|---|
| 1S | cl_new_S1 **← DECIDED** | 1.000 | 0.790 | 30.0 | natural S at the cheapest level: 4+ cards, 6+ points |
| P | cl_pass | 1.000 | 0.760 | 20.0 | no bid describes this hand: passing is the general agreement |
| X | cl_negative_X1 | 0.122 | 0.097 | 33.0 | negative double: 6+ HCP with a major they have not bid |
| 1NT | cl_nt1 | 0.000 | 0.000 | 27.0 | natural 1NT: 8-11 balanced with a stopper in their suit |
| 2NT | cl_nt2 | 0.000 | 0.000 | 28.0 | natural 2NT: 11-12 balanced with a stopper in their suit |
| 3NT | cl_nt3 | 0.000 | 0.000 | 29.0 | natural 3NT: 13-19 balanced with a stopper in their suit |
| 2D | cl_new_D2 | 0.000 | 0.000 | 26.0 | natural D at the cheapest level: 5+ cards, 10+ points |
| 2D | cl_new_long2_D | 0.000 | 0.000 | 26.0 | natural D at the cheapest level: a SIX-card suit, 8+ points |
| 2D | cl_new_D2_hi | 0.000 | 0.000 | 26.5 | natural D at the cheapest level: 5+ cards, 10+ points (my longest suit |
| 2D | cl_new_long2_D_hi | 0.000 | 0.000 | 26.5 | natural D at the cheapest level: a SIX-card suit, 8+ points (my longes |

---

## Board 730 — margin -1 IMPs

dealer **S**, vul **EW**, par(N/S) **+420**

    N  AT65.J9752.97.A9   (9 HCP)
    E  J83.AKQ.Q843.Q62   (14 HCP)
    S  Q742..AKJT62.T53   (10 HCP)
    W  K9.T8643.5.KJ874   (7 HCP)

Double-dummy tricks:

| declarer | C | D | H | S | NT |
|---|---|---|---|---|---|
| N | 5 | 10 | 5 | 10 | 8 |
| E | 8 | 3 | 7 | 2 | 4 |
| S | 5 | 10 | 5 | 10 | 8 |
| W | 7 | 3 | 7 | 2 | 4 |

Table A (**we are N/S**): 2D by S (10 tricks), N/S score +130  
Table B (**we are E/W**): 3S by S (10 tricks), N/S score +170  
IMP margin for us: **-1**

### Table A — we are NS, BEN is EW

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | S | 1D | US | open_1D | 1D (0.79) |
| 1 | W | P | BEN |  |  |
| 2 | N | 1H | US | r1m_1H | 1H (1.00) |
| 3 | E | X | BEN |  |  |
| 4 | S | 2D | US | xd_rebid_D2 | 1S (0.65) **≠** ← FIRST DIVERGENCE |
| 5 | W | P | BEN |  |  |
| 6 | N | P | US | uc_pass | P (0.60) |
| 7 | E | P | BEN |  |  |

### Table B — we are EW, BEN is NS

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | S | 1D | BEN |  |  |
| 1 | W | P | US | oc1D_pass | P (0.94) |
| 2 | N | 1H | BEN |  |  |
| 3 | E | P | US | sw_pass | X (0.45) **≠** ← FIRST DIVERGENCE |
| 4 | S | 1S | BEN |  |  |
| 5 | W | P | US | cl_pass | P (1.00) |
| 6 | N | 3S | BEN |  |  |
| 7 | E | P | US | ch_pass | P (1.00) |
| 8 | S | P | BEN |  |  |
| 9 | W | P | US | balhigh_pass | P (1.00) |

### First divergence: table A, call 4, seat S

auction so far: `1D P 1H X`, hand `Q742..AKJT62.T53`

| call | rule | fit | score | prio | shows |
|---|---|---|---|---|---|
| 2D | xd_rebid_D2 **← DECIDED** | 1.000 | 0.802 | 34.0 | rebid of my own doubled D: 6+ cards, 11+ points |
| P | srd_pass | 0.409 | 0.323 | 30.0 | minimum, fewer than 3 H |
| 1S | xd_run_S1 | 0.349 | 0.269 | 24.0 | running to my own S: 5+ cards |
| 2C | xd_run_C2 | 0.015 | 0.011 | 25.0 | running to my own C: 5+ cards |
| XX | srd_redouble | 0.000 | 0.000 | 85.0 | support redouble: exactly 3-card H support |
| 1NT | FALLBACK | 0.000 | 0.000 | 10.0 | natural NT, 6-11 HCP, stoppers in their suit(s) (undiscussed) |
| 2H | srd_raise | 0.000 | 0.000 | 80.0 | raise: 4+ H support |
| 3H | xd_jumpraise_H3 | 0.000 | 0.000 | 32.0 | jump raise of partner's doubled H: 4+ trumps, 10+ support points |

---

## Board 748 — margin -1 IMPs

dealer **N**, vul **Both**, par(N/S) **+140**

    N  A872.AJ5.A4.Q932   (15 HCP)
    E  KT4.Q9832.K72.T6   (8 HCP)
    S  QJ9653.4.QJT6.J8   (7 HCP)
    W  .KT76.9853.AK754   (10 HCP)

Double-dummy tricks:

| declarer | C | D | H | S | NT |
|---|---|---|---|---|---|
| N | 5 | 5 | 3 | 9 | 6 |
| E | 6 | 7 | 9 | 4 | 6 |
| S | 5 | 5 | 3 | 9 | 6 |
| W | 6 | 7 | 9 | 4 | 6 |

Table A (**we are N/S**): 3H by E (9 tricks), N/S score -140  
Table B (**we are E/W**): 4S by S (9 tricks), N/S score -100  
IMP margin for us: **-1**

### Table A — we are NS, BEN is EW

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | N | 1NT | US | open_1NT | 1NT (1.00) |
| 1 | E | P | BEN |  |  |
| 2 | S | 2H | US | nt_transfer_S | 2H (0.64) |
| 3 | W | P | BEN |  |  |
| 4 | N | 2S | US | tr_accept_2S | 2NT (0.97) **≠** ← FIRST DIVERGENCE |
| 5 | E | P | BEN |  |  |
| 6 | S | P | US | tr_pass_weak | 3S (0.84) **≠** |
| 7 | W | X | BEN |  |  |
| 8 | N | P | US | xd_pass | P (0.92) |
| 9 | E | 3H | BEN |  |  |
| 10 | S | P | US | ch_pass | 3S (0.62) **≠** |
| 11 | W | P | BEN |  |  |
| 12 | N | P | US | balhigh_pass | 3S (0.62) **≠** |

### Table B — we are EW, BEN is NS

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | N | 1NT | BEN |  |  |
| 1 | E | P | US | v1NT_pass | P (1.00) |
| 2 | S | 2H | BEN |  |  |
| 3 | W | P | US | cl_pass | P (0.80) |
| 4 | N | 2NT | BEN |  |  |
| 5 | E | P | US | cl_pass | P (1.00) |
| 6 | S | 4S | BEN |  |  |
| 7 | W | P | US | ch_pass | P (1.00) |
| 8 | N | P | BEN |  |  |
| 9 | E | P | US | balhigh_pass | P (1.00) |

### First divergence: table A, call 4, seat N

auction so far: `1NT P 2H P`, hand `A872.AJ5.A4.Q932`

| call | rule | fit | score | prio | shows |
|---|---|---|---|---|---|
| 2S | tr_accept_2S **← DECIDED** | 1.000 | 0.865 | 55.0 | completing the transfer (forced) |
| 3S | tr_super_3S | 0.409 | 0.360 | 60.0 | super-accept: 4 spades, maximum |
| 3C | uc_new_C3 | 0.264 | 0.206 | 27.0 | natural C at the cheapest level: 5+ cards, 14+ points |
| 3C | uc_new_C3_hi | 0.211 | 0.165 | 27.5 | natural C at the cheapest level: 5+ cards, 14+ points (my longest suit |
| 3H | uc_new_H3 | 0.015 | 0.012 | 27.0 | natural H at the cheapest level: 5+ cards, 14+ points |
| 3H | uc_new_H3_hi | 0.005 | 0.004 | 27.5 | natural H at the cheapest level: 5+ cards, 14+ points (my longest suit |
| 2NT | uc_nt2 | 0.004 | 0.003 | 28.0 | natural 2NT: 11-12 balanced, their suits stopped |
| 3D | uc_new_D3 | 0.000 | 0.000 | 27.0 | natural D at the cheapest level: 5+ cards, 14+ points |
| 4S | uc_raise_S4 | 0.000 | 0.000 | 32.0 | raise of partner's S: 11+ support points, a real trump fit, and the va |
| 3NT | uc_nt3 | 0.000 | 0.000 | 29.0 | natural 3NT: 13-19 balanced, their suits stopped |
| 3D | uc_new_D3_hi | 0.000 | 0.000 | 27.5 | natural D at the cheapest level: 5+ cards, 14+ points (my longest suit |

---

## Board 754 — margin -1 IMPs

dealer **S**, vul **None**, par(N/S) **+140**

    N  97432.K2.J8.K853   (7 HCP)
    E  Q6.A987.AQT.QT62   (14 HCP)
    S  AKJ.Q6543.762.A4   (14 HCP)
    W  T85.JT.K9543.J97   (5 HCP)

Double-dummy tricks:

| declarer | C | D | H | S | NT |
|---|---|---|---|---|---|
| N | 6 | 6 | 7 | 9 | 7 |
| E | 6 | 7 | 6 | 4 | 6 |
| S | 6 | 6 | 7 | 9 | 7 |
| W | 6 | 7 | 6 | 4 | 6 |

Table A (**we are N/S**): 2D by W (7 tricks), N/S score +50  
Table B (**we are E/W**): 1NT by S (7 tricks), N/S score +90  
IMP margin for us: **-1**

### Table A — we are NS, BEN is EW

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | S | 1H | US | open_1H | 1H (1.00) |
| 1 | W | P | BEN |  |  |
| 2 | N | 1S | US | r1H_1S | 1S (1.00) |
| 3 | E | X | BEN |  |  |
| 4 | S | P | US | xd_pass | XX (1.00) **≠** ← FIRST DIVERGENCE |
| 5 | W | 2D | BEN |  |  |
| 6 | N | P | US | cl_pass | P (0.81) |
| 7 | E | P | BEN |  |  |
| 8 | S | P | US | ballow_pass | 2S (0.85) **≠** |

### Table B — we are EW, BEN is NS

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | S | 1H | BEN |  |  |
| 1 | W | P | US | oc1H_pass | P (1.00) |
| 2 | N | 1S | BEN |  |  |
| 3 | E | P | US | sw_pass | X (0.51) **≠** ← FIRST DIVERGENCE |
| 4 | S | 1NT | BEN |  |  |
| 5 | W | P | US | cl_pass | P (1.00) |
| 6 | N | P | BEN |  |  |
| 7 | E | P | US | ballow_pass | P (1.00) |

### First divergence: table A, call 4, seat S

auction so far: `1H P 1S X`, hand `AKJ.Q6543.762.A4`

| call | rule | fit | score | prio | shows |
|---|---|---|---|---|---|
| P | xd_pass **← DECIDED** | 1.000 | 0.754 | 18.0 | sitting for their double: no better spot to run to |
| 2H | xd_rebid_H2 | 0.349 | 0.280 | 34.0 | rebid of my own doubled H: 6+ cards, 11+ points |
| 1NT | FALLBACK | 0.134 | 0.098 | 10.0 | natural NT, 6-11 HCP, stoppers in their suit(s) (undiscussed) |
| 2D | xd_run_D2 | 0.015 | 0.011 | 25.0 | running to my own D: 5+ cards |
| 2S | xd_raise_S2 | 0.000 | 0.000 | 30.0 | raise of partner's doubled S: 3+ trumps, 6-9 support points |
| 2C | xd_run_C2 | 0.000 | 0.000 | 25.0 | running to my own C: 5+ cards |
| 3S | xd_jumpraise_S3 | 0.000 | 0.000 | 32.0 | jump raise of partner's doubled S: 4+ trumps, 10+ support points |

---

## Board 765 — margin -1 IMPs

dealer **E**, vul **Both**, par(N/S) **+630**

    N  A974.7.AQ874.T93   (10 HCP)
    E  J6.KJ83.2.KQJ762   (11 HCP)
    S  KT53.AQT6.965.A4   (13 HCP)
    W  Q82.9542.KJT3.85   (6 HCP)

Double-dummy tricks:

| declarer | C | D | H | S | NT |
|---|---|---|---|---|---|
| N | 8 | 10 | 7 | 10 | 10 |
| E | 5 | 3 | 5 | 2 | 3 |
| S | 8 | 10 | 7 | 10 | 10 |
| W | 5 | 3 | 6 | 2 | 3 |

Table A (**we are N/S**): 3D by N (10 tricks), N/S score +130  
Table B (**we are E/W**): 3S by N (10 tricks), N/S score +170  
IMP margin for us: **-1**

### Table A — we are NS, BEN is EW

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | E | 1C | BEN |  |  |
| 1 | S | X | US | oc1C_X | X (0.94) |
| 2 | W | 1H | BEN |  |  |
| 3 | N | 2D | US | cl_new_D2 | X (1.00) **≠** ← FIRST DIVERGENCE |
| 4 | E | 2H | BEN |  |  |
| 5 | S | 3D | US | cl_doubler_raise3_D | P (0.94) **≠** |
| 6 | W | P | BEN |  |  |
| 7 | N | P | US | uc_pass | P (0.38) |
| 8 | E | P | BEN |  |  |

### Table B — we are EW, BEN is NS

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | E | P | US | open_pass | 1C (0.93) **≠** ← FIRST DIVERGENCE |
| 1 | S | 1D | BEN |  |  |
| 2 | W | P | US | oc1D_pass | P (1.00) |
| 3 | N | 1S | BEN |  |  |
| 4 | E | 2C | US | sw_2C | 2C (0.63) |
| 5 | S | 2S | BEN |  |  |
| 6 | W | P | US | cl_pass | P (0.98) |
| 7 | N | 3S | BEN |  |  |
| 8 | E | P | US | ch_pass | P (1.00) |
| 9 | S | P | BEN |  |  |
| 10 | W | P | US | balhigh_pass | P (1.00) |

### First divergence: table A, call 3, seat N

auction so far: `1C X 1H`, hand `A974.7.AQ874.T93`

| call | rule | fit | score | prio | shows |
|---|---|---|---|---|---|
| 2D | cl_new_D2_hi **← DECIDED** | 1.000 | 0.779 | 26.5 | natural D at the cheapest level: 5+ cards, 10+ points (my longest suit |
| 2D | cl_new_D2 | 1.000 | 0.778 | 26.0 | natural D at the cheapest level: 5+ cards, 10+ points |
| P | cl_pass | 1.000 | 0.760 | 20.0 | no bid describes this hand: passing is the general agreement |
| 1S | cl_new_S1 | 0.757 | 0.598 | 30.0 | natural S at the cheapest level: 4+ cards, 6+ points |
| X | cl_negative_X1 | 0.349 | 0.279 | 33.0 | negative double: 6+ HCP with a major they have not bid |
| 2D | cl_new_long2_D_hi | 0.349 | 0.272 | 26.5 | natural D at the cheapest level: a SIX-card suit, 8+ points (my longes |
| 2D | cl_new_long2_D | 0.349 | 0.272 | 26.0 | natural D at the cheapest level: a SIX-card suit, 8+ points |
| 1NT | cl_nt1 | 0.000 | 0.000 | 27.0 | natural 1NT: 8-11 balanced with a stopper in their suit |
| 2NT | cl_nt2 | 0.000 | 0.000 | 28.0 | natural 2NT: 11-12 balanced with a stopper in their suit |
| 3NT | cl_nt3 | 0.000 | 0.000 | 29.0 | natural 3NT: 13-19 balanced with a stopper in their suit |

---

## Board 768 — margin -1 IMPs

dealer **N**, vul **None**, par(N/S) **-420**

    N  A93.83.KJ972.K74   (11 HCP)
    E  T8.Q94.AQT85.JT6   (9 HCP)
    S  654.AJ62.64.Q852   (7 HCP)
    W  KQJ72.KT75.3.A93   (13 HCP)

Double-dummy tricks:

| declarer | C | D | H | S | NT |
|---|---|---|---|---|---|
| N | 4 | 4 | 3 | 4 | 3 |
| E | 8 | 8 | 10 | 9 | 9 |
| S | 5 | 4 | 3 | 4 | 3 |
| W | 8 | 8 | 10 | 9 | 9 |

Table A (**we are N/S**): 2H by W (10 tricks), N/S score -170  
Table B (**we are E/W**): 2S by W (9 tricks), N/S score -140  
IMP margin for us: **-1**

### Table A — we are NS, BEN is EW

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | N | P | US | open_pass | 1D (0.89) **≠** ← FIRST DIVERGENCE |
| 1 | E | P | BEN |  |  |
| 2 | S | P | US | open_pass | P (1.00) |
| 3 | W | 1S | BEN |  |  |
| 4 | N | 2D | US | oc1S_2D | P (0.99) **≠** |
| 5 | E | P | BEN |  |  |
| 6 | S | P | US | uc_pass | P (0.99) |
| 7 | W | 2H | BEN |  |  |
| 8 | N | P | US | cl_pass | P (1.00) |
| 9 | E | P | BEN |  |  |
| 10 | S | P | US | ballow_pass | P (0.97) |

### Table B — we are EW, BEN is NS

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | N | 1D | BEN |  |  |
| 1 | E | P | US | oc1D_pass | P (1.00) |
| 2 | S | 1H | BEN |  |  |
| 3 | W | X | US | sw_X | 1S (1.00) **≠** ← FIRST DIVERGENCE |
| 4 | N | P | BEN |  |  |
| 5 | E | 2C | US | advsw_D1H_C | 2D (0.72) **≠** |
| 6 | S | P | BEN |  |  |
| 7 | W | 2S | US | uc_new_S2 | P (0.65) **≠** |
| 8 | N | P | BEN |  |  |
| 9 | E | P | US | uc_pass | P (0.34) |
| 10 | S | P | BEN |  |  |

### First divergence: table A, call 0, seat N

auction so far: `(opening)`, hand `A93.83.KJ972.K74`

| call | rule | fit | score | prio | shows |
|---|---|---|---|---|---|
| P | open_pass **← DECIDED** | 1.000 | 0.760 | 20.0 | fewer than opening values |
| 1D | open_1D | 0.800 | 0.738 | 74.0 | opening, 3+ diamonds (better minor), no 5-card major, 12-21 HCP |
| 1D | open_1m_rule20 | 0.800 | 0.733 | 72.0 | 5+ diamonds, light opening satisfying the rule of 20 |
| 2D | open_weak_2D_nv | 0.279 | 0.249 | 64.0 | weak two: 6 diamonds, 5-10 HCP |
| 1C | open_1C | 0.037 | 0.034 | 73.0 | opening, 3+ clubs (better minor), no 5-card major, 12-21 HCP |
| 1NT | open_1NT | 0.028 | 0.027 | 92.0 | 15-17 balanced (may contain a 5-card major) |
| 1S | open_1S | 0.012 | 0.011 | 81.0 | 5+ spades, 12-21 HCP |
| 1S | open_1S_rule20 | 0.009 | 0.008 | 79.0 | 5+ spades, light opening satisfying the rule of 20 |
| 3D | open_3D_nv | 0.006 | 0.005 | 60.0 | preempt: 7+ diamonds, 3-9 HCP |
| 1C | open_1C_rule20 | 0.002 | 0.001 | 71.0 | 5+ clubs, light opening satisfying the rule of 20 |
| 2S | open_weak_2S_nv | 0.000 | 0.000 | 66.0 | weak two: 6 spades, 5-10 HCP |
| 1H | open_1H | 0.000 | 0.000 | 80.0 | 5+ hearts, 12-21 HCP |
| 1H | open_1H_rule20 | 0.000 | 0.000 | 78.0 | 5+ hearts, light opening satisfying the rule of 20 |
| 3C | open_3C_nv | 0.000 | 0.000 | 60.0 | preempt: 7+ clubs, 3-9 HCP |

---

## Board 795 — margin -1 IMPs

dealer **W**, vul **EW**, par(N/S) **-140**

    N  AQ642.J96.A96.J4   (12 HCP)
    E  98.AK82.K7432.K7   (13 HCP)
    S  KJT5.T743.T5.Q53   (6 HCP)
    W  73.Q5.QJ8.AT9862   (9 HCP)

Double-dummy tricks:

| declarer | C | D | H | S | NT |
|---|---|---|---|---|---|
| N | 3 | 3 | 4 | 7 | 6 |
| E | 9 | 10 | 9 | 6 | 7 |
| S | 3 | 3 | 4 | 7 | 6 |
| W | 9 | 10 | 9 | 6 | 7 |

Table A (**we are N/S**): 3D by E (10 tricks), N/S score -130  
Table B (**we are E/W**): 3S by N (7 tricks), N/S score -100  
IMP margin for us: **-1**

### Table A — we are NS, BEN is EW

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | W | P | BEN |  |  |
| 1 | N | 1S | US | open_1S | 1S (1.00) |
| 2 | E | 2D | BEN |  |  |
| 3 | S | 2S | US | r1M2x_raise | 2S (0.76) |
| 4 | W | 3D | BEN |  |  |
| 5 | N | P | US | ch_pass | P (0.66) |
| 6 | E | P | BEN |  |  |
| 7 | S | P | US | balhigh_pass | 3S (0.89) **≠** ← FIRST DIVERGENCE |

### Table B — we are EW, BEN is NS

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | W | P | US | open_pass | P (0.99) |
| 1 | N | 1S | BEN |  |  |
| 2 | E | P | US | oc1S_pass | 2D (0.94) **≠** ← FIRST DIVERGENCE |
| 3 | S | 2S | BEN |  |  |
| 4 | W | 3C | US | cl_new_C3 | P (1.00) **≠** |
| 5 | N | P | BEN |  |  |
| 6 | E | P | US | uc_pass | P (0.40) |
| 7 | S | 3S | BEN |  |  |
| 8 | W | P | US | ch_pass | P (1.00) |
| 9 | N | P | BEN |  |  |
| 10 | E | P | US | balhigh_pass | 4C (0.55) **≠** |

### First divergence: table A, call 7, seat S

auction so far: `P 1S 2D 2S 3D P P`, hand `KJT5.T743.T5.Q53`

| call | rule | fit | score | prio | shows |
|---|---|---|---|---|---|
| P | balhigh_pass **← DECIDED** | 1.000 | 0.763 | 21.0 | nothing worth reopening on: passing it out |
| 3S | balhigh_raise_S3 | 0.018 | 0.014 | 31.0 | competitive raise of partner's S: 3+ trumps, 10+ support points, 8+ co |
| 4S | balhigh_raise_lott4_S | 0.002 | 0.002 | 32.0 | the Law at the four level: they have a fit and so have we, ten-plus tr |
| 3S | balhigh_rebid_S3 | 0.000 | 0.000 | 29.0 | rebid of my own S: 6+ cards, values for the level opposite partner's s |
| 4S | balhigh_raise_S4 | 0.000 | 0.000 | 32.0 | competitive raise of partner's S: 11+ support points, a real trump fit |
| 3H | balhigh_new_H3 | 0.000 | 0.000 | 27.0 | natural H at the cheapest level: 5+ cards, 14+ points |
| 4C | balhigh_new_C4 | 0.000 | 0.000 | 28.0 | natural C at the cheapest level: 5+ cards, 14+ points |
| 3NT | balhigh_nt3 | 0.000 | 0.000 | 29.0 | natural 3NT: 13-19 balanced with a stopper in their suit |
| X | balhigh_reopen_X | 0.000 | 0.000 | 41.0 | reopening double: 16+, short in their suit, our side already in |
| 4NT | gst_rkc_S | 0.000 | 0.000 | 46.0 | RKC Blackwood 1430 for S: slam values opposite partner's shown range |

---

## Board 857 — margin -1 IMPs

dealer **E**, vul **EW**, par(N/S) **+420**

    N  A7.AK.AKQT975.K7   (23 HCP)
    E  Q5.94.J863.AQ985   (9 HCP)
    S  KT8632.7532.42.3   (3 HCP)
    W  J94.QJT86..JT642   (5 HCP)

Double-dummy tricks:

| declarer | C | D | H | S | NT |
|---|---|---|---|---|---|
| N | 4 | 11 | 6 | 10 | 8 |
| E | 9 | 2 | 5 | 2 | 2 |
| S | 4 | 11 | 6 | 10 | 7 |
| W | 9 | 2 | 6 | 2 | 2 |

Table A (**we are N/S**): 5D by S (11 tricks), N/S score +400  
Table B (**we are E/W**): 4S by N (10 tricks), N/S score +420  
IMP margin for us: **-1**

### Table A — we are NS, BEN is EW

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | E | P | BEN |  |  |
| 1 | S | P | US | open_pass | P (0.93) |
| 2 | W | P | BEN |  |  |
| 3 | N | 2C | US | open_2C | 2C (0.90) |
| 4 | E | X | BEN |  |  |
| 5 | S | 2D | US | c2x_2D | P (0.42) **≠** ← FIRST DIVERGENCE |
| 6 | W | P | BEN |  |  |
| 7 | N | 3D | US | gf_new_3D | 2NT (0.96) **≠** |
| 8 | E | P | BEN |  |  |
| 9 | S | 3S | US | gf_new_3S | 3S (0.50) |
| 10 | W | P | BEN |  |  |
| 11 | N | 4D | US | uc_rebid_D4 | 3NT (0.44) **≠** |
| 12 | E | P | BEN |  |  |
| 13 | S | 5D | US | gf_game_5D | P (0.70) **≠** |
| 14 | W | P | BEN |  |  |
| 15 | N | P | US | fallback | P (0.56) |
| 16 | E | P | BEN |  |  |

### Table B — we are EW, BEN is NS

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | E | P | US | open_pass | P (1.00) |
| 1 | S | P | BEN |  |  |
| 2 | W | P | US | open_pass | P (0.99) |
| 3 | N | 2C | BEN |  |  |
| 4 | E | P | US | cl_pass | X (0.91) **≠** ← FIRST DIVERGENCE |
| 5 | S | 2D | BEN |  |  |
| 6 | W | P | US | cl_pass | P (1.00) |
| 7 | N | 2NT | BEN |  |  |
| 8 | E | P | US | cl_pass | P (1.00) |
| 9 | S | 3H | BEN |  |  |
| 10 | W | P | US | ch_pass | P (0.99) |
| 11 | N | 3S | BEN |  |  |
| 12 | E | P | US | ch_pass | P (1.00) |
| 13 | S | 4S | BEN |  |  |
| 14 | W | P | US | ch_pass | P (1.00) |
| 15 | N | P | BEN |  |  |
| 16 | E | P | US | balhigh_pass | P (1.00) |

### First divergence: table A, call 5, seat S

auction so far: `P P P 2C X`, hand `KT8632.7532.42.3`

| call | rule | fit | score | prio | shows |
|---|---|---|---|---|---|
| 2D | c2x_2D **← DECIDED** | 1.000 | 0.868 | 56.0 | waiting, as without the double |
| P | c2x_pass | 1.000 | 0.865 | 55.0 | waiting over their double (the 2C force stands) |
| 2S | xd_run_S2 | 1.000 | 0.775 | 25.0 | running to my own S: 5+ cards |
| 2H | xd_run_H2 | 0.349 | 0.270 | 25.0 | running to my own H: 5+ cards |
| XX | c2x_XX | 0.004 | 0.003 | 57.0 | redouble: a positive opposite the strong 2C |
| 3C | xd_run_C3 | 0.000 | 0.000 | 26.0 | running to my own C: 6+ cards |
| 2NT | FALLBACK | 0.000 | 0.000 | 10.0 | natural NT, 11-14 HCP, stoppers in their suit(s) (undiscussed) |

---

## Board 932 — margin -1 IMPs

dealer **N**, vul **NS**, par(N/S) **-130**

    N  K42.KQ42.J87.T42   (9 HCP)
    E  7.J9.A653.KQJ983   (11 HCP)
    S  Q9653.A765.9.A76   (10 HCP)
    W  AJT8.T83.KQT42.5   (10 HCP)

Double-dummy tricks:

| declarer | C | D | H | S | NT |
|---|---|---|---|---|---|
| N | 3 | 3 | 8 | 7 | 5 |
| E | 8 | 10 | 5 | 5 | 7 |
| S | 3 | 3 | 8 | 7 | 5 |
| W | 8 | 10 | 5 | 5 | 7 |

Table A (**we are N/S**): 3D by W (10 tricks), N/S score -130  
Table B (**we are E/W**): 2S by S (7 tricks), N/S score -100  
IMP margin for us: **-1**

### Table A — we are NS, BEN is EW

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | N | P | US | open_pass | P (1.00) |
| 1 | E | 1C | BEN |  |  |
| 2 | S | 1S | US | oc1C_1S | 1S (0.97) |
| 3 | W | 2D | BEN |  |  |
| 4 | N | X | US | cl_negative_X2 | 2S (0.90) **≠** ← FIRST DIVERGENCE |
| 5 | E | 3D | BEN |  |  |
| 6 | S | P | US | ch_pass | P (0.57) |
| 7 | W | P | BEN |  |  |
| 8 | N | P | US | balhigh_pass | P (0.99) |

### Table B — we are EW, BEN is NS

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | N | P | BEN |  |  |
| 1 | E | 1C | US | open_1C | 1C (0.99) |
| 2 | S | 1S | BEN |  |  |
| 3 | W | 1NT | US | nx_1m1S_1NT | 2D (0.79) **≠** ← FIRST DIVERGENCE |
| 4 | N | 2S | BEN |  |  |
| 5 | E | P | US | cl_pass | 3C (0.64) **≠** |
| 6 | S | P | BEN |  |  |
| 7 | W | P | US | ballow_pass | 3D (0.64) **≠** |

### First divergence: table A, call 4, seat N

auction so far: `P 1C 1S 2D`, hand `K42.KQ42.J87.T42`

| call | rule | fit | score | prio | shows |
|---|---|---|---|---|---|
| X | cl_negative_X2 **← DECIDED** | 1.000 | 0.799 | 33.0 | negative double at the two level: 8+ HCP with a major they have not bi |
| 2S | cl_raise_S2 | 1.000 | 0.790 | 30.0 | competitive raise of partner's S: 3+ trumps, 6-9 support points, 7+ co |
| P | cl_pass | 1.000 | 0.760 | 20.0 | no bid describes this hand: passing is the general agreement |
| 2H | cl_new_H2_hi | 0.279 | 0.218 | 26.5 | natural H at the cheapest level: 5+ cards, 10+ points (my longest suit |
| 2H | cl_new_H2 | 0.279 | 0.217 | 26.0 | natural H at the cheapest level: 5+ cards, 10+ points |
| 2NT | cl_nt2 | 0.046 | 0.036 | 28.0 | natural 2NT: 11-12 balanced with a stopper in their suit |
| 2H | cl_new_long2_H_hi | 0.015 | 0.012 | 26.5 | natural H at the cheapest level: a SIX-card suit, 8+ points (my longes |
| 2H | cl_new_long2_H | 0.015 | 0.012 | 26.0 | natural H at the cheapest level: a SIX-card suit, 8+ points |
| 4S | cl_raise_S4 | 0.000 | 0.000 | 32.0 | competitive raise of partner's S: 11+ support points, a real trump fit |
| 3NT | cl_nt3 | 0.000 | 0.000 | 29.0 | natural 3NT: 13-19 balanced with a stopper in their suit |
| 4S | cl_raise_lott4_S | 0.000 | 0.000 | 32.0 | the Law at the four level: they have a fit and so have we, ten-plus tr |
| 4NT | gst_rkc_S | 0.000 | 0.000 | 46.0 | RKC Blackwood 1430 for S: slam values opposite partner's shown range |

---

## Board 960 — margin -1 IMPs

dealer **N**, vul **None**, par(N/S) **+140**

    N  J.T87652.Q2.KQJ5   (9 HCP)
    E  87543.Q4.94.T876   (2 HCP)
    S  QT96.J93.AKJT5.2   (11 HCP)
    W  AK2.AK.8763.A943   (18 HCP)

Double-dummy tricks:

| declarer | C | D | H | S | NT |
|---|---|---|---|---|---|
| N | 7 | 9 | 9 | 6 | 8 |
| E | 6 | 4 | 4 | 6 | 5 |
| S | 7 | 9 | 9 | 6 | 8 |
| W | 6 | 4 | 4 | 6 | 5 |

Table A (**we are N/S**): 2S by E (6 tricks), N/S score +100  
Table B (**we are E/W**): 3H by N (9 tricks), N/S score +140  
IMP margin for us: **-1**

### Table A — we are NS, BEN is EW

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | N | P | US | open_pass | 2H (0.78) **≠** ← FIRST DIVERGENCE |
| 1 | E | P | BEN |  |  |
| 2 | S | 1D | US | open_1D | 1D (0.93) |
| 3 | W | X | BEN |  |  |
| 4 | N | XX | US | rdx_XX | 1H (0.63) **≠** |
| 5 | E | 1S | BEN |  |  |
| 6 | S | P | US | rdc_pass_D | 1NT (0.95) **≠** |
| 7 | W | 1NT | BEN |  |  |
| 8 | N | P | US | cl_pass | 2H (0.80) **≠** |
| 9 | E | 2S | BEN |  |  |
| 10 | S | P | US | cl_pass | P (0.84) |
| 11 | W | P | BEN |  |  |
| 12 | N | P | US | ballow_pass | P (0.62) |

### Table B — we are EW, BEN is NS

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | N | 2H | BEN |  |  |
| 1 | E | P | US | vw2_pass | P (1.00) |
| 2 | S | 3H | BEN |  |  |
| 3 | W | P | US | ch_pass | 3NT (0.77) **≠** ← FIRST DIVERGENCE |
| 4 | N | P | BEN |  |  |
| 5 | E | P | US | balhigh_pass | P (1.00) |

### First divergence: table A, call 0, seat N

auction so far: `(opening)`, hand `J.T87652.Q2.KQJ5`

| call | rule | fit | score | prio | shows |
|---|---|---|---|---|---|
| P | open_pass **← DECIDED** | 1.000 | 0.760 | 20.0 | fewer than opening values |
| 2H | open_weak_2H_nv | 0.757 | 0.678 | 65.0 | weak two: 6 hearts, 5-10 HCP |
| 3H | open_3H_nv | 0.349 | 0.307 | 60.0 | preempt: 7+ hearts, 3-9 HCP |
| 1H | open_1H_rule20 | 0.160 | 0.149 | 78.0 | 5+ hearts, light opening satisfying the rule of 20 |
| 1H | open_1H | 0.134 | 0.126 | 80.0 | 5+ hearts, 12-21 HCP |
| 4H | open_4H | 0.015 | 0.013 | 61.0 | preempt: 8+ hearts, 3-10 HCP |
| 1C | open_1C | 0.013 | 0.012 | 73.0 | opening, 3+ clubs (better minor), no 5-card major, 12-21 HCP |
| 1C | open_1C_rule20 | 0.007 | 0.007 | 71.0 | 5+ clubs, light opening satisfying the rule of 20 |
| 1D | open_1D | 0.000 | 0.000 | 74.0 | opening, 3+ diamonds (better minor), no 5-card major, 12-21 HCP |
| 3C | open_3C_nv | 0.000 | 0.000 | 60.0 | preempt: 7+ clubs, 3-9 HCP |
| 1D | open_1m_rule20 | 0.000 | 0.000 | 72.0 | 5+ diamonds, light opening satisfying the rule of 20 |
| 1NT | open_1NT | 0.000 | 0.000 | 92.0 | 15-17 balanced (may contain a 5-card major) |
| 1S | open_1S_rule20 | 0.000 | 0.000 | 79.0 | 5+ spades, light opening satisfying the rule of 20 |
| 1S | open_1S | 0.000 | 0.000 | 81.0 | 5+ spades, 12-21 HCP |

---

## Board 961 — margin -1 IMPs

dealer **E**, vul **None**, par(N/S) **+420**

    N  A7.AT.Q952.KQJ95   (16 HCP)
    E  964.KJ96.J86.A32   (9 HCP)
    S  KJ532.Q8753.A.76   (10 HCP)
    W  QT8.42.KT743.T84   (5 HCP)

Double-dummy tricks:

| declarer | C | D | H | S | NT |
|---|---|---|---|---|---|
| N | 10 | 8 | 10 | 10 | 9 |
| E | 2 | 5 | 3 | 3 | 4 |
| S | 10 | 8 | 10 | 10 | 9 |
| W | 2 | 5 | 3 | 3 | 4 |

Table A (**we are N/S**): 3NT by N (9 tricks), N/S score +400  
Table B (**we are E/W**): 4H by S (10 tricks), N/S score +420  
IMP margin for us: **-1**

### Table A — we are NS, BEN is EW

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | E | P | BEN |  |  |
| 1 | S | 1S | US | open_1S | 1S (0.74) |
| 2 | W | P | BEN |  |  |
| 3 | N | 2C | US | r1S_2C | 2C (1.00) |
| 4 | E | P | BEN |  |  |
| 5 | S | 2H | US | ob_1S2x_2H | 2H (1.00) |
| 6 | W | P | BEN |  |  |
| 7 | N | 3NT | US | gf_3NT | 3D (0.78) **≠** ← FIRST DIVERGENCE |
| 8 | E | P | BEN |  |  |
| 9 | S | P | US | fallback | P (0.96) |
| 10 | W | P | BEN |  |  |

### Table B — we are EW, BEN is NS

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | E | P | US | open_pass | P (1.00) |
| 1 | S | 1S | BEN |  |  |
| 2 | W | P | US | oc1S_pass | P (1.00) |
| 3 | N | 2C | BEN |  |  |
| 4 | E | P | US | cl_pass | P (1.00) |
| 5 | S | 2H | BEN |  |  |
| 6 | W | P | US | cl_pass | P (1.00) |
| 7 | N | 3D | BEN |  |  |
| 8 | E | P | US | ch_pass | P (1.00) |
| 9 | S | 4H | BEN |  |  |
| 10 | W | P | US | ch_pass | P (1.00) |
| 11 | N | P | BEN |  |  |
| 12 | E | P | US | balhigh_pass | P (1.00) |

### First divergence: table A, call 7, seat N

auction so far: `P 1S P 2C P 2H P`, hand `A7.AT.Q952.KQJ95`

| call | rule | fit | score | prio | shows |
|---|---|---|---|---|---|
| 3NT | gf_3NT **← DECIDED** | 1.000 | 0.802 | 34.0 | no fit found and the unshown suits stopped: choosing 3NT |
| 3S | r21ss_set3_SC | 0.349 | 0.319 | 71.0 | setting trumps: 3+ spades, 13+, game forcing (slam interest possible) |
| 3D | gf_new_3D | 0.349 | 0.282 | 36.0 | five-card suit shown in the game force (no point floor: partner has th |
| 3C | uc_rebid_C3 | 0.349 | 0.273 | 27.0 | rebid of my own C: 6+ cards, values for the level opposite partner's s |
| 4S | uc_raise_S4 | 0.082 | 0.065 | 32.0 | raise of partner's S: 11+ support points, a real trump fit, and the va |
| 2NT | uc_nt2 | 0.028 | 0.022 | 28.0 | natural 2NT: 11-12 balanced, their suits stopped |
| 3H | r21ss_raise2nd_HC | 0.015 | 0.014 | 70.0 | raising the second suit: 4+ hearts, 13+, game forcing |
| 2S | uc_raise_S2 | 0.010 | 0.008 | 30.0 | raise of partner's S: 3+ trumps, 6-9 support points, 7+ combined trump |
| 4H | uc_raise_H4 | 0.000 | 0.000 | 32.0 | raise of partner's H: 11+ support points, a real trump fit, and the va |
| 4NT | gst_rkc_H | 0.000 | 0.000 | 46.0 | RKC Blackwood 1430 for H: slam values opposite partner's shown range |

---

## Board 966 — margin -1 IMPs

dealer **S**, vul **NS**, par(N/S) **+620**

    N  AK632.T5.963.KJT   (11 HCP)
    E  85.QJ32.AKJ42.Q8   (13 HCP)
    S  JT9.AK987.T75.A4   (12 HCP)
    W  Q74.64.Q8.976532   (4 HCP)

Double-dummy tricks:

| declarer | C | D | H | S | NT |
|---|---|---|---|---|---|
| N | 7 | 8 | 9 | 10 | 8 |
| E | 5 | 5 | 3 | 1 | 2 |
| S | 7 | 8 | 9 | 10 | 8 |
| W | 5 | 5 | 3 | 1 | 2 |

Table A (**we are N/S**): 2D by E (5 tricks), N/S score +150  
Table B (**we are E/W**): 3S by N (10 tricks), N/S score +170  
IMP margin for us: **-1**

### Table A — we are NS, BEN is EW

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | S | 1H | US | open_1H | 1H (1.00) |
| 1 | W | P | BEN |  |  |
| 2 | N | 1S | US | r1H_1S | 1S (1.00) |
| 3 | E | 2D | BEN |  |  |
| 4 | S | P | US | cl_pass | X (1.00) **≠** ← FIRST DIVERGENCE |
| 5 | W | P | BEN |  |  |
| 6 | N | P | US | ballow_pass | P (0.41) |

### Table B — we are EW, BEN is NS

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | S | 1H | BEN |  |  |
| 1 | W | P | US | oc1H_pass | P (1.00) |
| 2 | N | 1S | BEN |  |  |
| 3 | E | 2D | US | sw_2D | 2D (0.93) |
| 4 | S | X | BEN |  |  |
| 5 | W | 3C | US | xd_run_C3 | P (0.97) **≠** ← FIRST DIVERGENCE |
| 6 | N | 3S | BEN |  |  |
| 7 | E | P | US | ch_pass | P (0.96) |
| 8 | S | P | BEN |  |  |
| 9 | W | P | US | balhigh_pass | P (1.00) |

### First divergence: table A, call 4, seat S

auction so far: `1H P 1S 2D`, hand `JT9.AK987.T75.A4`

| call | rule | fit | score | prio | shows |
|---|---|---|---|---|---|
| P | cl_pass **← DECIDED** | 1.000 | 0.760 | 20.0 | no bid describes this hand: passing is the general agreement |
| 2S | cl_raise_S2 | 0.800 | 0.632 | 30.0 | competitive raise of partner's S: 3+ trumps, 6-9 support points, 7+ co |
| 2NT | cl_nt2 | 0.668 | 0.523 | 28.0 | natural 2NT: 11-12 balanced with a stopper in their suit |
| 2H | cl_rebid_H2 | 0.349 | 0.275 | 29.0 | rebid of my own H: 6+ cards, values for the level opposite partner's s |
| X | FALLBACK | 0.349 | 0.254 | 9.0 | takeout-flavored cooperative double (undiscussed) |
| 3NT | cl_nt3 | 0.090 | 0.070 | 29.0 | natural 3NT: 13-19 balanced with a stopper in their suit |
| 3H | cl_rebid_jump_H | 0.047 | 0.037 | 31.0 | invitational jump rebid in competition: 6+ good H, 16-19 |
| 4S | cl_raise_S4 | 0.002 | 0.002 | 32.0 | competitive raise of partner's S: 11+ support points, a real trump fit |
| 3C | cl_new_C3 | 0.000 | 0.000 | 27.0 | natural C at the cheapest level: 5+ cards, 14+ points |
| 3C | cl_new_C3_hi | 0.000 | 0.000 | 27.5 | natural C at the cheapest level: 5+ cards, 14+ points (my longest suit |
| 3C | cl_new_long3_C | 0.000 | 0.000 | 27.0 | natural C at the cheapest level: a SIX-card suit, 11+ points |
| 3C | cl_new_long3_C_hi | 0.000 | 0.000 | 27.5 | natural C at the cheapest level: a SIX-card suit, 11+ points (my longe |
| 4S | cl_raise_lott4_S | 0.000 | 0.000 | 32.0 | the Law at the four level: they have a fit and so have we, ten-plus tr |
| 4NT | gst_rkc_S | 0.000 | 0.000 | 46.0 | RKC Blackwood 1430 for S: slam values opposite partner's shown range |

---
