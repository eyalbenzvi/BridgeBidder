# Lost boards part 7 of 8 (38 boards, -80 IMPs)

Sorted worst-first across the whole match.

## Board 900 — margin -3 IMPs

dealer **N**, vul **NS**, par(N/S) **+140**

    N  AJT4.K9542.J6.74   (9 HCP)
    E  Q52.AJ63.T94.J63   (8 HCP)
    S  K6.QT8.KQ72.K985   (13 HCP)
    W  9873.7.A853.AQT2   (10 HCP)

Double-dummy tricks:

| declarer | C | D | H | S | NT |
|---|---|---|---|---|---|
| N | 6 | 6 | 8 | 6 | 7 |
| E | 6 | 6 | 4 | 6 | 6 |
| S | 6 | 6 | 9 | 7 | 7 |
| W | 6 | 6 | 4 | 6 | 5 |

Table A (**we are N/S**): 2D by S (6 tricks), N/S score -200  
Table B (**we are E/W**): 3H by N (8 tricks), N/S score -100  
IMP margin for us: **-3**

### Table A — we are NS, BEN is EW

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | N | P | US | open_pass | P (1.00) |
| 1 | E | P | BEN |  |  |
| 2 | S | 1D | US | open_1D | 1D (1.00) |
| 3 | W | P | BEN |  |  |
| 4 | N | 1H | US | r1m_1H | 1H (1.00) |
| 5 | E | P | BEN |  |  |
| 6 | S | 2C | US | ob_1D1H_2C | 1NT (1.00) **≠** ← FIRST DIVERGENCE |
| 7 | W | P | BEN |  |  |
| 8 | N | 2D | US | r1d1h2c_2D | P (0.99) **≠** |
| 9 | E | P | BEN |  |  |
| 10 | S | P | US | uc_pass | P (0.98) |
| 11 | W | P | BEN |  |  |

### Table B — we are EW, BEN is NS

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | N | P | BEN |  |  |
| 1 | E | P | US | open_pass | P (1.00) |
| 2 | S | 1D | BEN |  |  |
| 3 | W | P | US | oc1D_pass | P (1.00) |
| 4 | N | 1H | BEN |  |  |
| 5 | E | P | US | sw_pass | P (1.00) |
| 6 | S | 1NT | BEN |  |  |
| 7 | W | P | US | cl_pass | P (1.00) |
| 8 | N | 2H | BEN |  |  |
| 9 | E | P | US | cl_pass | P (1.00) |
| 10 | S | 3H | BEN |  |  |
| 11 | W | P | US | ch_pass | P (1.00) |
| 12 | N | P | BEN |  |  |
| 13 | E | P | US | balhigh_pass | P (1.00) |

### First divergence: table A, call 6, seat S

auction so far: `P P 1D P 1H P`, hand `K6.QT8.KQ72.K985`

| call | rule | fit | score | prio | shows |
|---|---|---|---|---|---|
| 2C | ob_1D1H_2C **← DECIDED** | 1.000 | 0.874 | 58.0 | second suit: 4+ clubs, 10-17 |
| 1NT | ob_1NT | 1.000 | 0.872 | 57.5 | balanced minimum 12-14, no fit |
| 2H | ob_raise_2H | 0.349 | 0.328 | 80.0 | raise: 4 H support, minimum (12-15) |
| 2D | ob_rebid_2D | 0.349 | 0.297 | 50.0 | rebid: 5+ (usually 6) D, minimum |
| 3H | ob_raise_3H | 0.143 | 0.133 | 78.0 | jump raise: 4 H support, invitational (16-18) |
| 1S | ob_1D1H_1S | 0.015 | 0.013 | 60.0 | 4+ spades, 10-17 |
| 3C | ob_1D1H_3C_jump | 0.004 | 0.003 | 57.0 | jump shift: 4+ clubs, 18+, game forcing |
| 2NT | ob_2NT | 0.004 | 0.003 | 56.0 | jump: balanced 18-19, no fit |
| 3D | ob_rebid_3D | 0.002 | 0.002 | 49.0 | jump rebid: 6+ good D, 16-18 |
| 4H | ob_raise_4H | 0.001 | 0.001 | 76.0 | game raise: 4 H support, 19+ support points |
| 3NT | uc_nt3 | 0.000 | 0.000 | 29.0 | natural 3NT: 13-19 balanced, their suits stopped |

---

## Board 907 — margin -3 IMPs

dealer **W**, vul **EW**, par(N/S) **-100**

    N  Q962.876.QJ2.Q97   (7 HCP)
    E  A.QJT95.KT3.K842   (13 HCP)
    S  J8754.K.A965.A65   (12 HCP)
    W  KT3.A432.874.JT3   (8 HCP)

Double-dummy tricks:

| declarer | C | D | H | S | NT |
|---|---|---|---|---|---|
| N | 4 | 7 | 4 | 8 | 5 |
| E | 9 | 6 | 9 | 5 | 8 |
| S | 4 | 7 | 4 | 8 | 4 |
| W | 8 | 6 | 9 | 5 | 8 |

Table A (**we are N/S**): 3H by E (9 tricks), N/S score -140  
Table B (**we are E/W**): 3S by S (8 tricks), N/S score -50  
IMP margin for us: **-3**

### Table A — we are NS, BEN is EW

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | W | P | BEN |  |  |
| 1 | N | P | US | open_pass | P (1.00) |
| 2 | E | 1H | BEN |  |  |
| 3 | S | P | US | oc1H_pass | 1S (1.00) **≠** ← FIRST DIVERGENCE |
| 4 | W | 2C | BEN |  |  |
| 5 | N | P | US | cl_pass | P (1.00) |
| 6 | E | 2D | BEN |  |  |
| 7 | S | P | US | cl_pass | P (0.83) |
| 8 | W | 2H | BEN |  |  |
| 9 | N | P | US | cl_pass | P (1.00) |
| 10 | E | P | BEN |  |  |
| 11 | S | X | US | ballow_X | P (0.55) **≠** |
| 12 | W | P | BEN |  |  |
| 13 | N | 2S | US | adx_pull_S2 | 2S (1.00) |
| 14 | E | 3H | BEN |  |  |
| 15 | S | P | US | ch_pass | P (0.95) |
| 16 | W | P | BEN |  |  |
| 17 | N | P | US | balhigh_pass | P (0.99) |

### Table B — we are EW, BEN is NS

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | W | P | US | open_pass | P (1.00) |
| 1 | N | P | BEN |  |  |
| 2 | E | 1H | US | open_1H | 1H (1.00) |
| 3 | S | 1S | BEN |  |  |
| 4 | W | 2H | US | r1H1S_raise | 2S (0.61) **≠** ← FIRST DIVERGENCE |
| 5 | N | 2S | BEN |  |  |
| 6 | E | 3H | US | cl_raise_lott3_H | 3H (0.54) |
| 7 | S | 3S | BEN |  |  |
| 8 | W | P | US | ch_pass | P (0.78) |
| 9 | N | P | BEN |  |  |
| 10 | E | P | US | balhigh_pass | P (1.00) |

### First divergence: table A, call 3, seat S

auction so far: `P P 1H`, hand `J8754.K.A965.A65`

| call | rule | fit | score | prio | shows |
|---|---|---|---|---|---|
| P | oc1H_pass **← DECIDED** | 1.000 | 0.775 | 25.0 | nothing suitable over 1H |
| 1S | oc1H_1S | 0.757 | 0.692 | 71.0 | overcall: 5+ spades, 8-16 |
| X | oc1H_X | 0.349 | 0.320 | 72.0 | takeout double: opening values, short hearts, no five-card major (or a |
| 2D | oc1H_2D | 0.264 | 0.237 | 65.0 | 2-level overcall: 5+ good diamonds, 11-17 |
| 2S | oc1H_2S_jump | 0.029 | 0.025 | 60.0 | weak jump overcall: 6 spades, 5-10 |
| 2C | oc1H_2C | 0.011 | 0.010 | 65.0 | 2-level overcall: 5+ good clubs, 11-17 |
| 3S | oc1H_3S_preempt | 0.002 | 0.002 | 58.0 | preemptive overcall: seven-card s suit, 3-10 |
| 3D | oc1H_3D_jump | 0.001 | 0.001 | 59.0 | weak jump overcall: 6+ diamonds, 5-10 |
| 4S | oc1H_4S_preempt | 0.000 | 0.000 | 59.0 | preemptive overcall: eight-card s suit, 3-10 |
| 3D | oc1H_3D_preempt | 0.000 | 0.000 | 58.0 | preemptive overcall: seven-card d suit, 3-10 |
| 3C | oc1H_3m_jump | 0.000 | 0.000 | 59.0 | weak jump overcall: 6+ clubs, 5-10 |
| 1NT | oc1H_1NT | 0.000 | 0.000 | 82.0 | 1NT overcall: 15-18 balanced with a heart stopper |
| 3C | oc1H_3C_preempt | 0.000 | 0.000 | 58.0 | preemptive overcall: seven-card c suit, 3-10 |

---

## Board 937 — margin -3 IMPs

dealer **E**, vul **EW**, par(N/S) **-500**

    N  JT63.74.Q873.KT9   (6 HCP)
    E  AK98.Q85.9.QJ632   (12 HCP)
    S  52.KT2.AKT42.A54   (14 HCP)
    W  Q74.AJ963.J65.87   (8 HCP)

Double-dummy tricks:

| declarer | C | D | H | S | NT |
|---|---|---|---|---|---|
| N | 4 | 8 | 3 | 4 | 4 |
| E | 9 | 5 | 10 | 8 | 6 |
| S | 3 | 8 | 3 | 4 | 4 |
| W | 9 | 5 | 10 | 8 | 6 |

Table A (**we are N/S**): 2H by W (10 tricks), N/S score -170  
Table B (**we are E/W**): 3D by S (8 tricks), N/S score -50  
IMP margin for us: **-3**

### Table A — we are NS, BEN is EW

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | E | 1C | BEN |  |  |
| 1 | S | 1D | US | oc1C_1D | 1D (0.99) |
| 2 | W | 1H | BEN |  |  |
| 3 | N | X | US | cl_negative_X1 | 3D (0.41) **≠** ← FIRST DIVERGENCE |
| 4 | E | XX | BEN |  |  |
| 5 | S | P | US | rr_pass | 1NT (0.45) **≠** |
| 6 | W | 2H | BEN |  |  |
| 7 | N | P | US | cl_pass | P (0.79) |
| 8 | E | P | BEN |  |  |
| 9 | S | P | US | ballow_pass | P (0.61) |

### Table B — we are EW, BEN is NS

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | E | 1C | US | open_1C | 1C (1.00) |
| 1 | S | 1D | BEN |  |  |
| 2 | W | 1H | US | cl_new_H1 | 1H (1.00) |
| 3 | N | 3D | BEN |  |  |
| 4 | E | P | US | ch_pass | P (1.00) |
| 5 | S | P | BEN |  |  |
| 6 | W | P | US | balhigh_pass | P (0.99) |

### First divergence: table A, call 3, seat N

auction so far: `1C 1D 1H`, hand `JT63.74.Q873.KT9`

| call | rule | fit | score | prio | shows |
|---|---|---|---|---|---|
| X | cl_negative_X1 **← DECIDED** | 1.000 | 0.799 | 33.0 | negative double: 6+ HCP with a major they have not bid |
| 2D | cl_raise_D2 | 1.000 | 0.790 | 30.0 | competitive raise of partner's D: 3+ trumps, 6-9 support points, 7+ co |
| P | cl_pass | 1.000 | 0.760 | 20.0 | no bid describes this hand: passing is the general agreement |
| 1S | cl_new_S1 | 0.757 | 0.598 | 30.0 | natural S at the cheapest level: 4+ cards, 6+ points |
| 1NT | cl_nt1 | 0.342 | 0.267 | 27.0 | natural 1NT: 8-11 balanced with a stopper in their suit |
| 2NT | cl_nt2 | 0.000 | 0.000 | 28.0 | natural 2NT: 11-12 balanced with a stopper in their suit |
| 4D | cl_raise_D4 | 0.000 | 0.000 | 27.0 | competitive raise of partner's D: 11+ support points, a real trump fit |
| 3NT | cl_nt3 | 0.000 | 0.000 | 29.0 | natural 3NT: 13-19 balanced with a stopper in their suit |

---

## Board 947 — margin -3 IMPs

dealer **W**, vul **None**, par(N/S) **+140**

    N  95.KQJ87.96.AQJ9   (13 HCP)
    E  632.9532.AJ8.KT3   (8 HCP)
    S  AKT874.64.T4.864   (7 HCP)
    W  QJ.AT.KQ7532.752   (12 HCP)

Double-dummy tricks:

| declarer | C | D | H | S | NT |
|---|---|---|---|---|---|
| N | 8 | 5 | 9 | 9 | 6 |
| E | 4 | 8 | 3 | 3 | 6 |
| S | 8 | 5 | 9 | 9 | 6 |
| W | 4 | 8 | 4 | 3 | 6 |

Table A (**we are N/S**): 3D by W (8 tricks), N/S score +50  
Table B (**we are E/W**): 2S by S (9 tricks), N/S score +140  
IMP margin for us: **-3**

### Table A — we are NS, BEN is EW

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | W | 1D | BEN |  |  |
| 1 | N | 1H | US | oc1D_1H | 1H (1.00) |
| 2 | E | 1NT | BEN |  |  |
| 3 | S | 2S | US | cl_new_S2 | P (0.88) **≠** ← FIRST DIVERGENCE |
| 4 | W | 3D | BEN |  |  |
| 5 | N | P | US | ch_pass | P (0.58) |
| 6 | E | P | BEN |  |  |
| 7 | S | P | US | balhigh_pass | P (1.00) |

### Table B — we are EW, BEN is NS

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | W | 1D | US | open_1D | 1D (1.00) |
| 1 | N | 1H | BEN |  |  |
| 2 | E | P | US | nx_1m1H_pass | 1NT (0.65) **≠** ← FIRST DIVERGENCE |
| 3 | S | 1S | BEN |  |  |
| 4 | W | 2D | US | cl_rebid_D2 | 2D (0.92) |
| 5 | N | P | BEN |  |  |
| 6 | E | P | US | uc_pass | 3D (0.61) **≠** |
| 7 | S | 2S | BEN |  |  |
| 8 | W | P | US | cl_pass | P (0.99) |
| 9 | N | P | BEN |  |  |
| 10 | E | P | US | ballow_pass | 3D (0.94) **≠** |

### First divergence: table A, call 3, seat S

auction so far: `1D 1H 1NT`, hand `AKT874.64.T4.864`

| call | rule | fit | score | prio | shows |
|---|---|---|---|---|---|
| 2S | cl_new_long2_S_hi **← DECIDED** | 1.000 | 0.779 | 26.5 | natural S at the cheapest level: a SIX-card suit, 8+ points (my longes |
| 2S | cl_new_long2_S | 1.000 | 0.778 | 26.0 | natural S at the cheapest level: a SIX-card suit, 8+ points |
| P | cl_pass | 1.000 | 0.760 | 20.0 | no bid describes this hand: passing is the general agreement |
| 2S | cl_new_S2_hi | 0.800 | 0.624 | 26.5 | natural S at the cheapest level: 5+ cards, 10+ points (my longest suit |
| 2S | cl_new_S2 | 0.800 | 0.622 | 26.0 | natural S at the cheapest level: 5+ cards, 10+ points |
| 2H | cl_raise_H2 | 0.349 | 0.276 | 30.0 | competitive raise of partner's H: 3+ trumps, 6-9 support points, 7+ co |
| X | FALLBACK | 0.004 | 0.003 | 9.0 | takeout-flavored cooperative double (undiscussed) |
| 2NT | cl_nt2 | 0.003 | 0.002 | 28.0 | natural 2NT: 11-12 balanced with a stopper in their suit |
| 2C | cl_new_C2 | 0.001 | 0.001 | 26.0 | natural C at the cheapest level: 5+ cards, 10+ points |
| 2C | cl_new_C2_hi | 0.000 | 0.000 | 26.5 | natural C at the cheapest level: 5+ cards, 10+ points (my longest suit |
| 2C | cl_new_long2_C | 0.000 | 0.000 | 26.0 | natural C at the cheapest level: a SIX-card suit, 8+ points |
| 4H | cl_raise_H4 | 0.000 | 0.000 | 32.0 | competitive raise of partner's H: 11+ support points, a real trump fit |
| 3NT | cl_nt3 | 0.000 | 0.000 | 29.0 | natural 3NT: 13-19 balanced with a stopper in their suit |
| 2C | cl_new_long2_C_hi | 0.000 | 0.000 | 26.5 | natural C at the cheapest level: a SIX-card suit, 8+ points (my longes |

---

## Board 2 — margin -2 IMPs

dealer **S**, vul **None**, par(N/S) **+100**

    N  KQT.KQ.K9752.K62   (16 HCP)
    E  J9853.T4.JT63.54   (2 HCP)
    S  762.653.AQ8.JT98   (7 HCP)
    W  A4.AJ9872.4.AQ73   (15 HCP)

Double-dummy tricks:

| declarer | C | D | H | S | NT |
|---|---|---|---|---|---|
| N | 8 | 9 | 4 | 7 | 6 |
| E | 5 | 4 | 8 | 6 | 5 |
| S | 8 | 9 | 4 | 7 | 6 |
| W | 5 | 4 | 8 | 6 | 5 |

Table A (**we are N/S**): 2H by W (8 tricks), N/S score -110  
Table B (**we are E/W**): 4D by N (9 tricks), N/S score -50  
IMP margin for us: **-2**

### Table A — we are NS, BEN is EW

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | S | P | US | open_pass | P (1.00) |
| 1 | W | 1H | BEN |  |  |
| 2 | N | 1NT | US | oc1H_1NT | 1NT (0.79) |
| 3 | E | P | BEN |  |  |
| 4 | S | P | US | uc_pass | P (0.98) |
| 5 | W | 2H | BEN |  |  |
| 6 | N | P | US | cl_pass | 3D (0.83) **≠** ← FIRST DIVERGENCE |
| 7 | E | P | BEN |  |  |
| 8 | S | P | US | ballow_pass | P (0.67) |

### Table B — we are EW, BEN is NS

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | S | P | BEN |  |  |
| 1 | W | 1H | US | open_1H | 1H (1.00) |
| 2 | N | 1NT | BEN |  |  |
| 3 | E | P | US | cl_pass | P (1.00) |
| 4 | S | P | BEN |  |  |
| 5 | W | 2H | US | ballow_rebid_H2 | 2H (0.75) |
| 6 | N | 3D | BEN |  |  |
| 7 | E | P | US | ch_pass | P (0.96) |
| 8 | S | P | BEN |  |  |
| 9 | W | 3H | US | balhigh_rebid_H3 | P (0.91) **≠** ← FIRST DIVERGENCE |
| 10 | N | P | BEN |  |  |
| 11 | E | P | US | uc_pass | P (0.97) |
| 12 | S | 4D | BEN |  |  |
| 13 | W | P | US | ch_pass | P (0.99) |
| 14 | N | P | BEN |  |  |
| 15 | E | P | US | balhigh_pass | P (0.96) |

### First divergence: table A, call 6, seat N

auction so far: `P 1H 1NT P P 2H`, hand `KQT.KQ.K9752.K62`

| call | rule | fit | score | prio | shows |
|---|---|---|---|---|---|
| P | cl_pass **← DECIDED** | 1.000 | 0.760 | 20.0 | no bid describes this hand: passing is the general agreement |
| X | FALLBACK | 1.000 | 0.727 | 9.0 | takeout-flavored cooperative double (undiscussed) |
| 3D | cl_new_D3_hi | 0.757 | 0.593 | 27.5 | natural D at the cheapest level: 5+ cards, 14+ points (my longest suit |
| 3D | cl_new_D3 | 0.757 | 0.592 | 27.0 | natural D at the cheapest level: 5+ cards, 14+ points |
| 3D | cl_new_long3_D_hi | 0.349 | 0.273 | 27.5 | natural D at the cheapest level: a SIX-card suit, 11+ points (my longe |
| 3D | cl_new_long3_D | 0.349 | 0.273 | 27.0 | natural D at the cheapest level: a SIX-card suit, 11+ points |
| 2S | cl_new_S2 | 0.015 | 0.012 | 26.0 | natural S at the cheapest level: 5+ cards, 10+ points |
| 3C | cl_new_C3 | 0.011 | 0.009 | 27.0 | natural C at the cheapest level: 5+ cards, 14+ points |
| 2S | cl_new_S2_hi | 0.006 | 0.005 | 26.5 | natural S at the cheapest level: 5+ cards, 10+ points (my longest suit |
| 3NT | cl_nt3 | 0.004 | 0.003 | 29.0 | natural 3NT: 13-19 balanced with a stopper in their suit |
| 2NT | cl_nt2 | 0.004 | 0.003 | 28.0 | natural 2NT: 11-12 balanced with a stopper in their suit |
| 3C | cl_new_C3_hi | 0.001 | 0.001 | 27.5 | natural C at the cheapest level: 5+ cards, 14+ points (my longest suit |
| 3C | cl_new_long3_C | 0.000 | 0.000 | 27.0 | natural C at the cheapest level: a SIX-card suit, 11+ points |
| 2S | cl_new_long2_S | 0.000 | 0.000 | 26.0 | natural S at the cheapest level: a SIX-card suit, 8+ points |

---

## Board 112 — margin -2 IMPs

dealer **N**, vul **None**, par(N/S) **+110**

    N  Q7.AJT.T8632.Q87   (9 HCP)
    E  J652.Q2.KQ4.AJ63   (13 HCP)
    S  AT43.97653.J.KT4   (8 HCP)
    W  K98.K84.A975.952   (10 HCP)

Double-dummy tricks:

| declarer | C | D | H | S | NT |
|---|---|---|---|---|---|
| N | 6 | 6 | 8 | 6 | 6 |
| E | 7 | 7 | 5 | 6 | 6 |
| S | 6 | 6 | 8 | 6 | 6 |
| W | 7 | 7 | 5 | 6 | 6 |

Table A (**we are N/S**): 1NT by W (6 tricks), N/S score +50  
Table B (**we are E/W**): 2H by S (8 tricks), N/S score +110  
IMP margin for us: **-2**

### Table A — we are NS, BEN is EW

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | N | P | US | open_pass | P (1.00) |
| 1 | E | 1C | BEN |  |  |
| 2 | S | P | US | oc1C_pass | 1H (0.65) **≠** ← FIRST DIVERGENCE |
| 3 | W | 1D | BEN |  |  |
| 4 | N | P | US | sw_pass | P (1.00) |
| 5 | E | 1S | BEN |  |  |
| 6 | S | P | US | cl_pass | P (1.00) |
| 7 | W | 1NT | BEN |  |  |
| 8 | N | P | US | cl_pass | P (1.00) |
| 9 | E | P | BEN |  |  |
| 10 | S | P | US | ballow_pass | P (1.00) |

### Table B — we are EW, BEN is NS

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | N | P | BEN |  |  |
| 1 | E | 1C | US | open_1C | 1C (1.00) |
| 2 | S | 1H | BEN |  |  |
| 3 | W | 1NT | US | nx_1m1H_1NT | 1NT (0.94) |
| 4 | N | 2H | BEN |  |  |
| 5 | E | P | US | cl_pass | P (0.82) |
| 6 | S | P | BEN |  |  |
| 7 | W | P | US | ballow_pass | P (0.91) |

### First divergence: table A, call 2, seat S

auction so far: `P 1C`, hand `AT43.97653.J.KT4`

| call | rule | fit | score | prio | shows |
|---|---|---|---|---|---|
| P | oc1C_pass **← DECIDED** | 1.000 | 0.775 | 25.0 | nothing suitable over 1C |
| 1S | oc1C_1S | 0.349 | 0.319 | 71.0 | overcall: 5+ spades, 8-16 |
| 1H | oc1C_1H | 0.329 | 0.301 | 71.0 | overcall: 5+ hearts, 8-16 |
| 2H | oc1C_2H_jump | 0.070 | 0.061 | 60.0 | weak jump overcall: 6 hearts, 5-10 |
| 2S | oc1C_2S_jump | 0.003 | 0.003 | 60.0 | weak jump overcall: 6 spades, 5-10 |
| 3H | oc1C_3H_preempt | 0.001 | 0.001 | 58.0 | preemptive overcall: seven-card h suit, 3-10 |
| X | oc1C_X | 0.000 | 0.000 | 72.0 | takeout double: opening values, short clubs, support for the other sui |
| 4H | oc1C_4H_preempt | 0.000 | 0.000 | 59.0 | preemptive overcall: eight-card h suit, 3-10 |
| 3S | oc1C_3S_preempt | 0.000 | 0.000 | 58.0 | preemptive overcall: seven-card s suit, 3-10 |
| 4S | oc1C_4S_preempt | 0.000 | 0.000 | 59.0 | preemptive overcall: eight-card s suit, 3-10 |
| 1D | oc1C_1D | 0.000 | 0.000 | 70.0 | overcall: 5+ diamonds, 8-16 |
| 1NT | oc1C_1NT | 0.000 | 0.000 | 82.0 | 1NT overcall: 15-18 balanced with a club stopper |
| 2D | oc1C_2D_jump | 0.000 | 0.000 | 60.0 | weak jump overcall: 6 diamonds, 5-10 |
| 3D | oc1C_3D_preempt | 0.000 | 0.000 | 58.0 | preemptive overcall: seven-card d suit, 3-10 |

---

## Board 152 — margin -2 IMPs

dealer **N**, vul **EW**, par(N/S) **+110**

    N  AQ.KJ752.J4.AQ74   (17 HCP)
    E  T982.T4.Q95.K982   (5 HCP)
    S  J7543.63.AT63.T5   (5 HCP)
    W  K6.AQ98.K872.J63   (13 HCP)

Double-dummy tricks:

| declarer | C | D | H | S | NT |
|---|---|---|---|---|---|
| N | 7 | 8 | 8 | 8 | 7 |
| E | 6 | 5 | 5 | 4 | 6 |
| S | 7 | 8 | 8 | 8 | 7 |
| W | 6 | 5 | 5 | 5 | 7 |

Table A (**we are N/S**): 1NTX by W (7 tricks), N/S score -180  
Table B (**we are E/W**): 4S by S (8 tricks), N/S score -100  
IMP margin for us: **-2**

### Table A — we are NS, BEN is EW

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | N | 1H | US | open_1H | 1H (0.95) |
| 1 | E | P | BEN |  |  |
| 2 | S | P | US | r1H_pass | 1S (0.92) **≠** ← FIRST DIVERGENCE |
| 3 | W | 1NT | BEN |  |  |
| 4 | N | X | US | o4b_X_H | P (0.57) **≠** |
| 5 | E | P | BEN |  |  |
| 6 | S | P | US | adx_pass_min | 2S (0.91) **≠** |
| 7 | W | P | BEN |  |  |

### Table B — we are EW, BEN is NS

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | N | 1H | BEN |  |  |
| 1 | E | P | US | oc1H_pass | P (1.00) |
| 2 | S | 1S | BEN |  |  |
| 3 | W | P | US | sw_pass | P (0.58) |
| 4 | N | 3C | BEN |  |  |
| 5 | E | P | US | ch_pass | P (1.00) |
| 6 | S | 3S | BEN |  |  |
| 7 | W | P | US | ch_pass | P (1.00) |
| 8 | N | 4S | BEN |  |  |
| 9 | E | P | US | ch_pass | P (1.00) |
| 10 | S | P | BEN |  |  |
| 11 | W | P | US | balhigh_pass | P (1.00) |

### First divergence: table A, call 2, seat S

auction so far: `1H P`, hand `J7543.63.AT63.T5`

| call | rule | fit | score | prio | shows |
|---|---|---|---|---|---|
| P | r1H_pass **← DECIDED** | 1.000 | 0.745 | 15.0 | 0-5 HCP: too weak to respond |
| 1S | r1H_1S | 0.800 | 0.733 | 72.0 | 4+ spades, 6+ HCP, forcing one round |
| 2H | r1H_single_raise | 0.349 | 0.307 | 60.0 | single raise: 3+ hearts, 6-9 support points |
| 1NT | r1H_1NT | 0.080 | 0.066 | 40.0 | 1NT response: 6-11 HCP, denies 4 spades and a simple raise (semi-forci |
| 3H | r1H_limit_raise | 0.001 | 0.001 | 62.0 | limit raise: 3+ hearts, 10-13 support points (a shapely 4-trump hand m |
| 4C | r1H_splinter_4C | 0.000 | 0.000 | 89.0 | splinter: 4+ hearts, singleton/void in clubs, game-going raise |
| 4H | r1H_game_raise_preempt | 0.000 | 0.000 | 63.0 | preemptive game raise: 5+ hearts, weak with shortness |
| 2D | r1H_2D | 0.000 | 0.000 | 76.0 | 2/1 game forcing: 4+ diamonds, 12+ HCP |
| 2C | r1H_2C | 0.000 | 0.000 | 75.0 | 2/1 game forcing: 3+ clubs, 12+ HCP |
| 4D | r1H_splinter_4D | 0.000 | 0.000 | 89.0 | splinter: 4+ hearts, singleton/void in diamonds, game-going raise |
| 3NT | uc_nt3 | 0.000 | 0.000 | 29.0 | natural 3NT: 13-19 balanced, their suits stopped |
| 2NT | r1H_jacoby_2NT | 0.000 | 0.000 | 90.0 | Jacoby 2NT: 4+ hearts, game-forcing raise, no shortness |
| 3S | r1H_splinter_3S | 0.000 | 0.000 | 89.0 | splinter: 4+ hearts, singleton/void in spades, game-going raise |

---

## Board 168 — margin -2 IMPs

dealer **N**, vul **EW**, par(N/S) **+130**

    N  .AK96.T5.AT97654   (11 HCP)
    E  KQ8.J3.KQJ982.82   (12 HCP)
    S  J7432.85.A763.J3   (6 HCP)
    W  AT965.QT742.4.KQ   (11 HCP)

Double-dummy tricks:

| declarer | C | D | H | S | NT |
|---|---|---|---|---|---|
| N | 10 | 5 | 5 | 4 | 4 |
| E | 2 | 7 | 7 | 8 | 5 |
| S | 10 | 5 | 5 | 4 | 4 |
| W | 2 | 7 | 7 | 8 | 5 |

Table A (**we are N/S**): 4C by N (10 tricks), N/S score +130  
Table B (**we are E/W**): 3D by E (7 tricks), N/S score +200  
IMP margin for us: **-2**

### Table A — we are NS, BEN is EW

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | N | 1C | US | open_1C | 1C (1.00) |
| 1 | E | 1D | BEN |  |  |
| 2 | S | 1S | US | cl_new_S1 | 1S (1.00) |
| 3 | W | 2H | BEN |  |  |
| 4 | N | 3C | US | cl_rebid_jump_C | 3C (0.65) |
| 5 | E | 3D | BEN |  |  |
| 6 | S | P | US | ch_pass | P (0.72) |
| 7 | W | P | BEN |  |  |
| 8 | N | 4C | US | balhigh_rebid_C4 | P (0.83) **≠** ← FIRST DIVERGENCE |
| 9 | E | P | BEN |  |  |
| 10 | S | P | US | uc_pass | P (0.97) |
| 11 | W | P | BEN |  |  |

### Table B — we are EW, BEN is NS

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | N | 1C | BEN |  |  |
| 1 | E | 1D | US | oc1C_1D | 1D (0.99) |
| 2 | S | 1S | BEN |  |  |
| 3 | W | 2H | US | cl_new_H2 | 2H (0.74) |
| 4 | N | 3C | BEN |  |  |
| 5 | E | 3D | US | ch_rebid_D3 | 3D (0.54) |
| 6 | S | P | BEN |  |  |
| 7 | W | P | US | uc_pass | P (0.89) |
| 8 | N | P | BEN |  |  |

### First divergence: table A, call 8, seat N

auction so far: `1C 1D 1S 2H 3C 3D P P`, hand `.AK96.T5.AT97654`

| call | rule | fit | score | prio | shows |
|---|---|---|---|---|---|
| 4C | balhigh_rebid_C4 **← DECIDED** | 1.000 | 0.787 | 29.0 | rebid of my own C: 6+ cards, values for the level opposite partner's s |
| P | balhigh_pass | 1.000 | 0.763 | 21.0 | nothing worth reopening on: passing it out |
| X | balhigh_reopen_X | 0.000 | 0.000 | 41.0 | reopening double: 16+, short in their suit, our side already in |
| 3NT | balhigh_nt3 | 0.000 | 0.000 | 29.0 | natural 3NT: 13-19 balanced with a stopper in their suit |
| 3S | balhigh_raise_S3 | 0.000 | 0.000 | 31.0 | competitive raise of partner's S: 3+ trumps, 10+ support points, 8+ co |
| 4S | balhigh_raise_S4 | 0.000 | 0.000 | 32.0 | competitive raise of partner's S: 11+ support points, a real trump fit |
| 4S | balhigh_raise_lott4_S | 0.000 | 0.000 | 32.0 | the Law at the four level: they have a fit and so have we, ten-plus tr |
| 4NT | gst_rkc_S | 0.000 | 0.000 | 46.0 | RKC Blackwood 1430 for S: slam values opposite partner's shown range |

---

## Board 195 — margin -2 IMPs

dealer **W**, vul **None**, par(N/S) **-100**

    N  AK853.Q954.K62.6   (12 HCP)
    E  Q92.T32.AQJ73.84   (9 HCP)
    S  T64.AKJ6.T98.J95   (9 HCP)
    W  J7.87.54.AKQT732   (10 HCP)

Double-dummy tricks:

| declarer | C | D | H | S | NT |
|---|---|---|---|---|---|
| N | 1 | 6 | 8 | 8 | 1 |
| E | 9 | 7 | 4 | 5 | 7 |
| S | 1 | 1 | 8 | 8 | 1 |
| W | 9 | 7 | 4 | 5 | 7 |

Table A (**we are N/S**): 3C by W (9 tricks), N/S score -110  
Table B (**we are E/W**): 3S by N (8 tricks), N/S score -50  
IMP margin for us: **-2**

### Table A — we are NS, BEN is EW

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | W | 3C | BEN |  |  |
| 1 | N | P | US | v3_C_pass | 3S (0.88) **≠** ← FIRST DIVERGENCE |
| 2 | E | P | BEN |  |  |
| 3 | S | P | US | balhigh_pass | P (1.00) |

### Table B — we are EW, BEN is NS

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | W | P | US | open_pass | 3C (0.68) **≠** ← FIRST DIVERGENCE |
| 1 | N | 1S | BEN |  |  |
| 2 | E | P | US | oc1S_pass | P (1.00) |
| 3 | S | 2S | BEN |  |  |
| 4 | W | 3C | US | cl_new_C3 | 3C (0.75) |
| 5 | N | P | BEN |  |  |
| 6 | E | P | US | uc_pass | P (0.90) |
| 7 | S | 3S | BEN |  |  |
| 8 | W | P | US | ch_pass | P (0.86) |
| 9 | N | P | BEN |  |  |
| 10 | E | P | US | balhigh_pass | P (0.75) |

### First divergence: table A, call 1, seat N

auction so far: `3C`, hand `AK853.Q954.K62.6`

| call | rule | fit | score | prio | shows |
|---|---|---|---|---|---|
| P | v3_C_pass **← DECIDED** | 1.000 | 0.790 | 30.0 | nothing suitable over their preempt |
| X | v3_C_X | 0.409 | 0.373 | 70.0 | takeout double of the 3-level preempt |
| 3S | v3_C_S | 0.349 | 0.311 | 64.0 | overcalling the preempt: good 6+ S, 13+ |
| 4S | v3_C_4S | 0.015 | 0.013 | 65.0 | overcalling the preempt at the four level: eight of them, or seven wit |
| 3H | v3_C_H | 0.011 | 0.010 | 64.0 | overcalling the preempt: good 6+ H, 13+ |
| 3D | v3_C_D | 0.000 | 0.000 | 64.0 | overcalling the preempt: good 6+ D, 13+ |
| 4H | v3_C_4H | 0.000 | 0.000 | 65.0 | overcalling the preempt at the four level: eight of them, or seven wit |
| 3NT | v3_C_3NT | 0.000 | 0.000 | 66.0 | to play: 16-21 with a stopper |

---

## Board 206 — margin -2 IMPs

dealer **S**, vul **Both**, par(N/S) **-660**

    N  T653.Q742.J65.J4   (4 HCP)
    E  AQJ4.3.AK8742.75   (14 HCP)
    S  87.JT65.Q.AKT932   (10 HCP)
    W  K92.AK98.T93.Q86   (12 HCP)

Double-dummy tricks:

| declarer | C | D | H | S | NT |
|---|---|---|---|---|---|
| N | 5 | 1 | 5 | 1 | 1 |
| E | 7 | 11 | 7 | 11 | 11 |
| S | 5 | 1 | 5 | 1 | 1 |
| W | 7 | 11 | 7 | 11 | 11 |

Table A (**we are N/S**): 2S by E (11 tricks), N/S score -200  
Table B (**we are E/W**): 4D by E (11 tricks), N/S score -150  
IMP margin for us: **-2**

### Table A — we are NS, BEN is EW

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | S | 1C | US | open_1C | 1C (0.55) |
| 1 | W | X | BEN |  |  |
| 2 | N | P | US | rdx_pass | P (0.89) |
| 3 | E | 2S | BEN |  |  |
| 4 | S | P | US | cl_pass | P (1.00) |
| 5 | W | P | BEN |  |  |
| 6 | N | P | US | ballow_pass | P (1.00) |

### Table B — we are EW, BEN is NS

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | S | 1C | BEN |  |  |
| 1 | W | P | US | oc1C_pass | X (0.82) **≠** ← FIRST DIVERGENCE |
| 2 | N | 1H | BEN |  |  |
| 3 | E | 2D | US | sw_2D | 2D (0.80) |
| 4 | S | 2H | BEN |  |  |
| 5 | W | 3D | US | cl_raise_D3 | 3D (0.68) |
| 6 | N | P | BEN |  |  |
| 7 | E | 4D | US | uc_raise_D4 | P (0.92) **≠** |
| 8 | S | P | BEN |  |  |
| 9 | W | P | US | uc_pass | P (0.98) |
| 10 | N | P | BEN |  |  |

### First divergence: table B, call 1, seat W

auction so far: `1C`, hand `K92.AK98.T93.Q86`

| call | rule | fit | score | prio | shows |
|---|---|---|---|---|---|
| P | oc1C_pass **← DECIDED** | 1.000 | 0.775 | 25.0 | nothing suitable over 1C |
| X | oc1C_X | 0.349 | 0.320 | 72.0 | takeout double: opening values, short clubs, support for the other sui |
| 1H | oc1C_1H | 0.349 | 0.319 | 71.0 | overcall: 5+ hearts, 8-16 |
| 1NT | oc1C_1NT | 0.134 | 0.127 | 82.0 | 1NT overcall: 15-18 balanced with a club stopper |
| 1S | oc1C_1S | 0.015 | 0.014 | 71.0 | overcall: 5+ spades, 8-16 |
| 1D | oc1C_1D | 0.011 | 0.010 | 70.0 | overcall: 5+ diamonds, 8-16 |
| 2H | oc1C_2H_jump | 0.006 | 0.005 | 60.0 | weak jump overcall: 6 hearts, 5-10 |
| 3H | oc1C_3H_preempt | 0.000 | 0.000 | 58.0 | preemptive overcall: seven-card h suit, 3-10 |
| 2D | oc1C_2D_jump | 0.000 | 0.000 | 60.0 | weak jump overcall: 6 diamonds, 5-10 |
| 2S | oc1C_2S_jump | 0.000 | 0.000 | 60.0 | weak jump overcall: 6 spades, 5-10 |
| 4H | oc1C_4H_preempt | 0.000 | 0.000 | 59.0 | preemptive overcall: eight-card h suit, 3-10 |
| 3S | oc1C_3S_preempt | 0.000 | 0.000 | 58.0 | preemptive overcall: seven-card s suit, 3-10 |
| 3D | oc1C_3D_preempt | 0.000 | 0.000 | 58.0 | preemptive overcall: seven-card d suit, 3-10 |
| 4S | oc1C_4S_preempt | 0.000 | 0.000 | 59.0 | preemptive overcall: eight-card s suit, 3-10 |

---

## Board 227 — margin -2 IMPs

dealer **W**, vul **None**, par(N/S) **-130**

    N  A87.T942.J5.9843   (5 HCP)
    E  K543.J75.QT64.76   (6 HCP)
    S  QJT2.K3.K32.AQT2   (15 HCP)
    W  96.AQ86.A987.KJ5   (14 HCP)

Double-dummy tricks:

| declarer | C | D | H | S | NT |
|---|---|---|---|---|---|
| N | 7 | 3 | 4 | 5 | 5 |
| E | 6 | 10 | 8 | 8 | 8 |
| S | 7 | 3 | 5 | 5 | 5 |
| W | 6 | 10 | 8 | 8 | 8 |

Table A (**we are N/S**): 2H by N (4 tricks), N/S score -200  
Table B (**we are E/W**): 2D by W (10 tricks), N/S score -130  
IMP margin for us: **-2**

### Table A — we are NS, BEN is EW

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | W | 1D | BEN |  |  |
| 1 | N | P | US | oc1D_pass | P (1.00) |
| 2 | E | 1S | BEN |  |  |
| 3 | S | X | US | sw_X | 1NT (0.79) **≠** ← FIRST DIVERGENCE |
| 4 | W | P | BEN |  |  |
| 5 | N | 2H | US | advsw_D1S_H | 2H (0.98) |
| 6 | E | P | BEN |  |  |
| 7 | S | P | US | uc_pass | P (0.98) |
| 8 | W | P | BEN |  |  |

### Table B — we are EW, BEN is NS

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | W | 1D | US | open_1D | 1D (1.00) |
| 1 | N | P | BEN |  |  |
| 2 | E | 1S | US | r1m_1S | 1S (1.00) |
| 3 | S | 1NT | BEN |  |  |
| 4 | W | P | US | sd_pass | P (0.95) |
| 5 | N | P | BEN |  |  |
| 6 | E | 2D | US | ballow_raise_D2 | P (0.92) **≠** ← FIRST DIVERGENCE |
| 7 | S | P | BEN |  |  |
| 8 | W | P | US | uc_pass | 3D (0.36) **≠** |
| 9 | N | P | BEN |  |  |

### First divergence: table A, call 3, seat S

auction so far: `1D P 1S`, hand `QJT2.K3.K32.AQT2`

| call | rule | fit | score | prio | shows |
|---|---|---|---|---|---|
| X | sw_X **← DECIDED** | 0.409 | 0.373 | 70.0 | takeout of their suits: shortness in opener's suit, or four cards in e |
| P | sw_pass | 0.409 | 0.323 | 30.0 | nothing suitable between two bidding opponents |
| 2C | sw_2C | 0.349 | 0.313 | 66.0 | sandwich 2-level overcall: good 5+ clubs, 11-17 |
| 1NT | FALLBACK | 0.028 | 0.021 | 10.0 | natural NT, 6-11 HCP, stoppers in their suit(s) (undiscussed) |
| 2H | sw_2H | 0.000 | 0.000 | 66.0 | sandwich 2-level overcall: good 5+ hearts, 11-17 |
| 3C | sw_3C | 0.000 | 0.000 | 69.5 | sandwich preemptive jump: seven-card c suit, 3-10 |
| 3H | sw_3H | 0.000 | 0.000 | 69.5 | sandwich preemptive jump: seven-card h suit, 3-10 |

---

## Board 241 — margin -2 IMPs

dealer **E**, vul **None**, par(N/S) **+920**

    N  .T9.AT83.AJ97532   (9 HCP)
    E  KJ9753.Q83.74.64   (6 HCP)
    S  AQT8.K72.KQJ652.   (15 HCP)
    W  642.AJ654.9.KQT8   (10 HCP)

Double-dummy tricks:

| declarer | C | D | H | S | NT |
|---|---|---|---|---|---|
| N | 8 | 11 | 6 | 6 | 8 |
| E | 4 | 0 | 6 | 7 | 4 |
| S | 9 | 12 | 7 | 6 | 9 |
| W | 4 | 0 | 6 | 7 | 4 |

Table A (**we are N/S**): 3S by E (7 tricks), N/S score +100  
Table B (**we are E/W**): 4D by S (12 tricks), N/S score +170  
IMP margin for us: **-2**

### Table A — we are NS, BEN is EW

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | E | 2S | BEN |  |  |
| 1 | S | 3D | US | vw2_shadow3_D | 3D (0.93) |
| 2 | W | 3S | BEN |  |  |
| 3 | N | P | US | ch_pass | 4D (0.55) **≠** ← FIRST DIVERGENCE |
| 4 | E | P | BEN |  |  |
| 5 | S | P | US | balhigh_pass | P (0.52) |

### Table B — we are EW, BEN is NS

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | E | 2S | US | open_weak_2S_nv | 2S (0.97) |
| 1 | S | 3D | BEN |  |  |
| 2 | W | 3H | US | ch_free_3H | 3S (0.60) **≠** ← FIRST DIVERGENCE |
| 3 | N | 4D | BEN |  |  |
| 4 | E | P | US | ch_pass | P (0.99) |
| 5 | S | P | BEN |  |  |
| 6 | W | P | US | balhigh_pass | P (0.91) |

### First divergence: table A, call 3, seat N

auction so far: `2S 3D 3S`, hand `.T9.AT83.AJ97532`

| call | rule | fit | score | prio | shows |
|---|---|---|---|---|---|
| P | ch_pass **← DECIDED** | 1.000 | 0.766 | 22.0 | no bid describes this hand over their high-level contract |
| 4D | ch_raise_D4 | 0.082 | 0.064 | 27.0 | competitive raise of partner's D: 11+ support points, a real trump fit |
| 4C | ch_new_C4_hi | 0.055 | 0.043 | 28.5 | natural C at the cheapest level: 5+ cards, 14+ points (my longest suit |
| 4C | ch_new_C4 | 0.055 | 0.043 | 28.0 | natural C at the cheapest level: 5+ cards, 14+ points |
| 4H | ch_new_H4 | 0.000 | 0.000 | 28.0 | natural H at the cheapest level: 5+ cards, 14+ points |
| X | ch_negative_X3 | 0.000 | 0.000 | 33.0 | negative double at the three level: 10+ HCP with a major they have not |
| 3NT | ch_nt3 | 0.000 | 0.000 | 29.0 | natural 3NT: 13-19 balanced with a stopper in their suit |
| X | ch_penalty_X | 0.000 | 0.000 | 38.0 | penalty double of their high contract: defensive tricks and trump leng |
| 4H | ch_new_H4_hi | 0.000 | 0.000 | 28.5 | natural H at the cheapest level: 5+ cards, 14+ points (my longest suit |
| 4NT | gst_rkc_D | 0.000 | 0.000 | 46.0 | RKC Blackwood 1430 for D: slam values opposite partner's shown range |

---

## Board 252 — margin -2 IMPs

dealer **N**, vul **Both**, par(N/S) **-1100**

    N  95.Q62.QJT952.T7   (5 HCP)
    E  AJT8.KT43.3.A943   (12 HCP)
    S  Q.AJ875.K8764.J6   (11 HCP)
    W  K76432.9.A.KQ852   (12 HCP)

Double-dummy tricks:

| declarer | C | D | H | S | NT |
|---|---|---|---|---|---|
| N | 1 | 9 | 7 | 1 | 1 |
| E | 12 | 4 | 5 | 12 | 12 |
| S | 1 | 9 | 7 | 1 | 1 |
| W | 12 | 4 | 5 | 12 | 11 |

Table A (**we are N/S**): 4S by W (12 tricks), N/S score -680  
Table B (**we are E/W**): 5C by E (12 tricks), N/S score -620  
IMP margin for us: **-2**

### Table A — we are NS, BEN is EW

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | N | P | US | open_pass | P (0.70) |
| 1 | E | 1C | BEN |  |  |
| 2 | S | 1H | US | oc1C_1H | 2NT (0.98) **≠** ← FIRST DIVERGENCE |
| 3 | W | 1S | BEN |  |  |
| 4 | N | 2H | US | cl_raise_H2 | P (0.97) **≠** |
| 5 | E | 2S | BEN |  |  |
| 6 | S | 3H | US | cl_raise_lott3_H | P (0.94) **≠** |
| 7 | W | 4S | BEN |  |  |
| 8 | N | P | US | ch_pass | P (0.99) |
| 9 | E | P | BEN |  |  |
| 10 | S | P | US | balhigh_pass | P (1.00) |

### Table B — we are EW, BEN is NS

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | N | P | BEN |  |  |
| 1 | E | 1C | US | open_1C | 1C (1.00) |
| 2 | S | 2NT | BEN |  |  |
| 3 | W | 3C | US | cl_raise_C3 | 3S (0.60) **≠** ← FIRST DIVERGENCE |
| 4 | N | 4D | BEN |  |  |
| 5 | E | P | US | ch_pass | P (0.71) |
| 6 | S | P | BEN |  |  |
| 7 | W | 5C | US | uc_minor_game_5C | P (0.71) **≠** |
| 8 | N | P | BEN |  |  |
| 9 | E | P | US | fallback | P (0.94) |
| 10 | S | P | BEN |  |  |

### First divergence: table A, call 2, seat S

auction so far: `P 1C`, hand `Q.AJ875.K8764.J6`

| call | rule | fit | score | prio | shows |
|---|---|---|---|---|---|
| 1H | oc1C_1H **← DECIDED** | 1.000 | 0.913 | 71.0 | overcall: 5+ hearts, 8-16 |
| 1D | oc1C_1D | 1.000 | 0.910 | 70.0 | overcall: 5+ diamonds, 8-16 |
| P | oc1C_pass | 1.000 | 0.775 | 25.0 | nothing suitable over 1C |
| 2D | oc1C_2D_jump | 0.056 | 0.049 | 60.0 | weak jump overcall: 6 diamonds, 5-10 |
| 2H | oc1C_2H_jump | 0.056 | 0.049 | 60.0 | weak jump overcall: 6 hearts, 5-10 |
| 3H | oc1C_3H_preempt | 0.012 | 0.010 | 58.0 | preemptive overcall: seven-card h suit, 3-10 |
| 3D | oc1C_3D_preempt | 0.009 | 0.008 | 58.0 | preemptive overcall: seven-card d suit, 3-10 |
| X | oc1C_X | 0.005 | 0.005 | 72.0 | takeout double: opening values, short clubs, support for the other sui |
| 4H | oc1C_4H_preempt | 0.000 | 0.000 | 59.0 | preemptive overcall: eight-card h suit, 3-10 |
| 1S | oc1C_1S | 0.000 | 0.000 | 71.0 | overcall: 5+ spades, 8-16 |
| 1NT | oc1C_1NT | 0.000 | 0.000 | 82.0 | 1NT overcall: 15-18 balanced with a club stopper |
| 2S | oc1C_2S_jump | 0.000 | 0.000 | 60.0 | weak jump overcall: 6 spades, 5-10 |
| 3S | oc1C_3S_preempt | 0.000 | 0.000 | 58.0 | preemptive overcall: seven-card s suit, 3-10 |
| 4S | oc1C_4S_preempt | 0.000 | 0.000 | 59.0 | preemptive overcall: eight-card s suit, 3-10 |

---

## Board 262 — margin -2 IMPs

dealer **S**, vul **NS**, par(N/S) **-420**

    N  3.742.T97.AKJT32   (8 HCP)
    E  AT75.AQT8.A863.6   (14 HCP)
    S  KQJ84.3.QJ54.Q84   (11 HCP)
    W  962.KJ965.K2.975   (7 HCP)

Double-dummy tricks:

| declarer | C | D | H | S | NT |
|---|---|---|---|---|---|
| N | 8 | 6 | 3 | 5 | 5 |
| E | 5 | 6 | 10 | 7 | 7 |
| S | 8 | 6 | 3 | 5 | 5 |
| W | 5 | 6 | 10 | 7 | 7 |

Table A (**we are N/S**): 2H by E (10 tricks), N/S score -170  
Table B (**we are E/W**): 3C by N (8 tricks), N/S score -100  
IMP margin for us: **-2**

### Table A — we are NS, BEN is EW

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | S | P | US | open_pass | 1S (0.85) **≠** ← FIRST DIVERGENCE |
| 1 | W | P | BEN |  |  |
| 2 | N | P | US | open_pass | P (0.69) |
| 3 | E | 1D | BEN |  |  |
| 4 | S | 1S | US | oc1D_1S | 1S (1.00) |
| 5 | W | X | BEN |  |  |
| 6 | N | 2C | US | xd_run_C2 | P (0.91) **≠** |
| 7 | E | 2H | BEN |  |  |
| 8 | S | P | US | cl_pass | 2S (0.41) **≠** |
| 9 | W | P | BEN |  |  |
| 10 | N | P | US | ballow_pass | P (1.00) |

### Table B — we are EW, BEN is NS

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | S | 1S | BEN |  |  |
| 1 | W | P | US | oc1S_pass | P (1.00) |
| 2 | N | 1NT | BEN |  |  |
| 3 | E | P | US | sw_pass | P (0.94) |
| 4 | S | 2D | BEN |  |  |
| 5 | W | P | US | cl_pass | P (1.00) |
| 6 | N | 3C | BEN |  |  |
| 7 | E | P | US | ch_pass | P (0.98) |
| 8 | S | P | BEN |  |  |
| 9 | W | P | US | balhigh_pass | P (1.00) |

### First divergence: table A, call 0, seat S

auction so far: `(opening)`, hand `KQJ84.3.QJ54.Q84`

| call | rule | fit | score | prio | shows |
|---|---|---|---|---|---|
| P | open_pass **← DECIDED** | 1.000 | 0.760 | 20.0 | fewer than opening values |
| 1S | open_1S | 0.800 | 0.754 | 81.0 | 5+ spades, 12-21 HCP |
| 1S | open_1S_rule20 | 0.757 | 0.710 | 79.0 | 5+ spades, light opening satisfying the rule of 20 |
| 2S | open_weak_2S_vul | 0.279 | 0.251 | 66.0 | weak two: 6 decent spades, 7-10 HCP (vulnerable) |
| 1D | open_1D | 0.080 | 0.074 | 74.0 | opening, 3+ diamonds (better minor), no 5-card major, 12-21 HCP |
| 1C | open_1C | 0.028 | 0.026 | 73.0 | opening, 3+ clubs (better minor), no 5-card major, 12-21 HCP |
| 1D | open_1m_rule20 | 0.011 | 0.011 | 72.0 | 5+ diamonds, light opening satisfying the rule of 20 |
| 3S | open_3S_vul | 0.006 | 0.005 | 60.0 | preempt: 7+ decent spades, 5-9 HCP (vulnerable) |
| 1C | open_1C_rule20 | 0.000 | 0.000 | 71.0 | 5+ clubs, light opening satisfying the rule of 20 |
| 2D | open_weak_2D_vul | 0.000 | 0.000 | 64.0 | weak two: 6 decent diamonds, 7-10 HCP (vulnerable) |
| 4S | open_4S | 0.000 | 0.000 | 61.0 | preempt: 8+ spades, 3-10 HCP |
| 3D | open_3D_vul | 0.000 | 0.000 | 60.0 | preempt: 7+ decent diamonds, 5-9 HCP (vulnerable) |
| 2C | open_2C | 0.000 | 0.000 | 96.0 | strong artificial: 22+ HCP or equivalent playing strength |
| 1NT | open_1NT | 0.000 | 0.000 | 92.0 | 15-17 balanced (may contain a 5-card major) |

---

## Board 266 — margin -2 IMPs

dealer **S**, vul **EW**, par(N/S) **+450**

    N  J983.KQ9853.7.QJ   (9 HCP)
    E  AT5.7.KJT8652.A6   (12 HCP)
    S  4.A62.A94.KT5432   (11 HCP)
    W  KQ762.JT4.Q3.987   (8 HCP)

Double-dummy tricks:

| declarer | C | D | H | S | NT |
|---|---|---|---|---|---|
| N | 9 | 3 | 11 | 5 | 7 |
| E | 2 | 10 | 2 | 8 | 4 |
| S | 9 | 3 | 11 | 4 | 7 |
| W | 2 | 10 | 2 | 8 | 4 |

Table A (**we are N/S**): 4H by N (11 tricks), N/S score +450  
Table B (**we are E/W**): 4SX by W (8 tricks), N/S score +500  
IMP margin for us: **-2**

### Table A — we are NS, BEN is EW

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | S | 1C | US | open_1C | 1C (1.00) |
| 1 | W | P | BEN |  |  |
| 2 | N | 1H | US | r1m_1H | 1H (1.00) |
| 3 | E | 2D | BEN |  |  |
| 4 | S | X | US | sd_double | X (1.00) |
| 5 | W | P | BEN |  |  |
| 6 | N | 2H | US | adx_pull_my_H | 4H (0.49) **≠** ← FIRST DIVERGENCE |
| 7 | E | 3D | BEN |  |  |
| 8 | S | P | US | ch_pass | P (0.89) |
| 9 | W | P | BEN |  |  |
| 10 | N | 4H | US | balhigh_raise_H4 | 3H (0.76) **≠** |
| 11 | E | P | BEN |  |  |
| 12 | S | P | US | fallback | P (1.00) |
| 13 | W | P | BEN |  |  |

### Table B — we are EW, BEN is NS

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | S | 1C | BEN |  |  |
| 1 | W | 1S | US | oc1C_1S | P (0.54) **≠** ← FIRST DIVERGENCE |
| 2 | N | 2H | BEN |  |  |
| 3 | E | 4S | US | cl_raise_lott4_S | 2S (0.40) **≠** |
| 4 | S | P | BEN |  |  |
| 5 | W | P | US | fallback | P (1.00) |
| 6 | N | X | BEN |  |  |
| 7 | E | P | US | xd_pass | P (0.99) |
| 8 | S | P | BEN |  |  |
| 9 | W | P | US | fallback | P (1.00) |

### First divergence: table A, call 6, seat N

auction so far: `1C P 1H 2D X P`, hand `J983.KQ9853.7.QJ`

| call | rule | fit | score | prio | shows |
|---|---|---|---|---|---|
| 2H | adx_pull_my_H **← DECIDED** | 1.000 | 0.877 | 59.0 | pulling partner's double back to my own suit |
| P | adx_pass_min | 1.000 | 0.856 | 52.0 | no suit worth pulling to and no trump stack: partner's double stands |
| 4H | uc_raise_H4 | 1.000 | 0.796 | 32.0 | raise of partner's H: 11+ support points, a real trump fit, and the va |
| 2S | adx_neg_major_S2 | 0.409 | 0.363 | 62.0 | answering partner's negative double in the major it promised |
| 4H | uc_raise_lott4_H | 0.011 | 0.009 | 32.0 | the Law at the four level: they have a fit and so have we, ten-plus tr |
| P | adx_sit | 0.000 | 0.000 | 61.0 | sitting the double: real trumps behind them |
| 2NT | adx_nt | 0.000 | 0.000 | 56.0 | natural answer to the double: 9-12 with their suit stopped |
| 3NT | uc_nt3 | 0.000 | 0.000 | 29.0 | natural 3NT: 13-19 balanced, their suits stopped |
| 3C | uc_raise_C3 | 0.000 | 0.000 | 27.0 | raise of partner's C: 3+ trumps, 10+ support points, 8+ combined trump |
| 5C | uc_minor_game_5C | 0.000 | 0.000 | 28.0 | accepting to game in the raised minor: 17+ opposite the raise |
| 4C | uc_raise_C4 | 0.000 | 0.000 | 27.0 | raise of partner's C: 11+ support points, a real trump fit, and the va |
| 4NT | gst_rkc_C | 0.000 | 0.000 | 46.0 | RKC Blackwood 1430 for C: slam values opposite partner's shown range |

---

## Board 273 — margin -2 IMPs

dealer **E**, vul **None**, par(N/S) **+130**

    N  8743.AQ987.8.A43   (10 HCP)
    E  52.T2.T2.KQJT976   (6 HCP)
    S  J9.65.AKQJ764.85   (11 HCP)
    W  AKQT6.KJ43.953.2   (13 HCP)

Double-dummy tricks:

| declarer | C | D | H | S | NT |
|---|---|---|---|---|---|
| N | 5 | 10 | 7 | 6 | 8 |
| E | 8 | 2 | 5 | 5 | 2 |
| S | 5 | 10 | 7 | 6 | 8 |
| W | 8 | 2 | 6 | 5 | 2 |

Table A (**we are N/S**): 3D by S (10 tricks), N/S score +130  
Table B (**we are E/W**): 3S by W (5 tricks), N/S score +200  
IMP margin for us: **-2**

### Table A — we are NS, BEN is EW

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | E | 3C | BEN |  |  |
| 1 | S | 3D | US | v3_C_D | 3D (0.79) |
| 2 | W | P | BEN |  |  |
| 3 | N | P | US | uc_pass | 3H (0.48) **≠** ← FIRST DIVERGENCE |
| 4 | E | P | BEN |  |  |

### Table B — we are EW, BEN is NS

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | E | 3C | US | open_3C_nv | 3C (0.96) |
| 1 | S | 3D | BEN |  |  |
| 2 | W | 3S | US | ch_free_3S | P (0.47) **≠** ← FIRST DIVERGENCE |
| 3 | N | P | BEN |  |  |
| 4 | E | P | US | uc_pass | P (0.44) |
| 5 | S | P | BEN |  |  |

### First divergence: table A, call 3, seat N

auction so far: `3C 3D P`, hand `8743.AQ987.8.A43`

| call | rule | fit | score | prio | shows |
|---|---|---|---|---|---|
| P | uc_pass **← DECIDED** | 1.000 | 0.754 | 18.0 | no bid describes this hand: nothing further to show |
| 3H | uc_new_H3_hi | 0.134 | 0.105 | 27.5 | natural H at the cheapest level: 5+ cards, 14+ points (my longest suit |
| 3H | uc_new_H3 | 0.134 | 0.105 | 27.0 | natural H at the cheapest level: 5+ cards, 14+ points |
| 3S | uc_new_S3 | 0.004 | 0.003 | 27.0 | natural S at the cheapest level: 5+ cards, 14+ points |
| 3S | uc_new_S3_hi | 0.003 | 0.002 | 27.5 | natural S at the cheapest level: 5+ cards, 14+ points (my longest suit |
| 3NT | uc_nt3 | 0.000 | 0.000 | 29.0 | natural 3NT: 13-19 balanced, their suits stopped |
| 5D | uc_minor_game_5D | 0.000 | 0.000 | 28.0 | accepting to game in the raised minor: 17+ opposite the raise |
| 4D | uc_raise_D4 | 0.000 | 0.000 | 27.0 | raise of partner's D: 11+ support points, a real trump fit, and the va |
| 4NT | gst_rkc_D | 0.000 | 0.000 | 46.0 | RKC Blackwood 1430 for D: slam values opposite partner's shown range |

---

## Board 282 — margin -2 IMPs

dealer **S**, vul **EW**, par(N/S) **-120**

    N  87.AQJT2.842.K93   (10 HCP)
    E  AQ42.984.73.AQ74   (12 HCP)
    S  J93.73.AQT95.JT6   (8 HCP)
    W  KT65.K65.KJ6.852   (10 HCP)

Double-dummy tricks:

| declarer | C | D | H | S | NT |
|---|---|---|---|---|---|
| N | 5 | 6 | 6 | 4 | 4 |
| E | 7 | 6 | 6 | 8 | 7 |
| S | 5 | 6 | 6 | 4 | 4 |
| W | 8 | 7 | 7 | 8 | 8 |

Table A (**we are N/S**): 1NT by S (4 tricks), N/S score -150  
Table B (**we are E/W**): 2H by N (6 tricks), N/S score -100  
IMP margin for us: **-2**

### Table A — we are NS, BEN is EW

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | S | P | US | open_pass | P (1.00) |
| 1 | W | P | BEN |  |  |
| 2 | N | 1H | US | open_1H | 2H (0.99) **≠** ← FIRST DIVERGENCE |
| 3 | E | P | BEN |  |  |
| 4 | S | 1NT | US | r1H_1NT | 1NT (1.00) |
| 5 | W | P | BEN |  |  |
| 6 | N | P | US | ob_1M1NT_pass | P (0.94) |
| 7 | E | P | BEN |  |  |

### Table B — we are EW, BEN is NS

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | S | P | BEN |  |  |
| 1 | W | P | US | open_pass | P (1.00) |
| 2 | N | 2H | BEN |  |  |
| 3 | E | P | US | vw2_pass | X (0.58) **≠** ← FIRST DIVERGENCE |
| 4 | S | P | BEN |  |  |
| 5 | W | P | US | ballow_pass | P (0.97) |

### First divergence: table A, call 2, seat N

auction so far: `P P`, hand `87.AQJT2.842.K93`

| call | rule | fit | score | prio | shows |
|---|---|---|---|---|---|
| 1H | open_1H_third_light **← DECIDED** | 1.000 | 0.925 | 75.0 | third-seat light opening: 5+ good hearts, 9-11 |
| P | open_pass | 1.000 | 0.760 | 20.0 | fewer than opening values |
| 1H | open_1H | 0.409 | 0.385 | 80.0 | 5+ hearts, 12-21 HCP |
| 1H | open_1H_rule20_third | 0.409 | 0.382 | 78.0 | 5+ hearts, third-seat light opening satisfying the rule of 20 |
| 2H | open_weak_2H_nv | 0.349 | 0.312 | 65.0 | weak two: 6 hearts, 5-10 HCP |
| 1C | open_1C | 0.041 | 0.038 | 73.0 | opening, 3+ clubs (better minor), no 5-card major, 12-21 HCP |
| 1D | open_1D | 0.014 | 0.013 | 74.0 | opening, 3+ diamonds (better minor), no 5-card major, 12-21 HCP |
| 3H | open_3H_nv | 0.012 | 0.010 | 60.0 | preempt: 7+ hearts, 3-9 HCP |
| 1NT | open_1NT | 0.004 | 0.004 | 92.0 | 15-17 balanced (may contain a 5-card major) |
| 1C | open_1C_rule20_third | 0.000 | 0.000 | 71.0 | 5+ c, third-seat light opening satisfying the rule of 20 |
| 4H | open_4H | 0.000 | 0.000 | 61.0 | preempt: 8+ hearts, 3-10 HCP |
| 1D | open_1D_rule20_third | 0.000 | 0.000 | 72.0 | 5+ d, third-seat light opening satisfying the rule of 20 |
| 1S | open_1S | 0.000 | 0.000 | 81.0 | 5+ spades, 12-21 HCP |
| 2D | open_weak_2D_nv | 0.000 | 0.000 | 64.0 | weak two: 6 diamonds, 5-10 HCP |

---

## Board 289 — margin -2 IMPs

dealer **E**, vul **None**, par(N/S) **+140**

    N  KQ963.A9632.3.K4   (12 HCP)
    E  AT742.T54.74.A83   (8 HCP)
    S  85.K87.AJ8652.Q9   (10 HCP)
    W  J.QJ.KQT9.JT7652   (10 HCP)

Double-dummy tricks:

| declarer | C | D | H | S | NT |
|---|---|---|---|---|---|
| N | 4 | 7 | 9 | 8 | 6 |
| E | 8 | 6 | 4 | 5 | 7 |
| S | 4 | 7 | 9 | 8 | 6 |
| W | 8 | 6 | 4 | 5 | 7 |

Table A (**we are N/S**): 3D by S (7 tricks), N/S score -100  
Table B (**we are E/W**): 2D by S (7 tricks), N/S score -50  
IMP margin for us: **-2**

### Table A — we are NS, BEN is EW

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | E | P | BEN |  |  |
| 1 | S | 2D | US | open_weak_2D_nv | 2D (0.98) |
| 2 | W | P | BEN |  |  |
| 3 | N | 2S | US | rw2_new_D_S | P (0.88) **≠** ← FIRST DIVERGENCE |
| 4 | E | P | BEN |  |  |
| 5 | S | 3D | US | uc_rebid_D3 | 3H (0.32) **≠** |
| 6 | W | P | BEN |  |  |
| 7 | N | P | US | uc_pass | P (0.97) |
| 8 | E | P | BEN |  |  |

### Table B — we are EW, BEN is NS

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | E | P | US | open_pass | P (1.00) |
| 1 | S | 2D | BEN |  |  |
| 2 | W | P | US | vw2_pass | P (0.95) |
| 3 | N | P | BEN |  |  |
| 4 | E | P | US | ballow_pass | P (0.63) |

### First divergence: table A, call 3, seat N

auction so far: `P 2D P`, hand `KQ963.A9632.3.K4`

| call | rule | fit | score | prio | shows |
|---|---|---|---|---|---|
| 2S | rw2_new_D_S **← DECIDED** | 1.000 | 0.889 | 63.0 | new suit opposite the weak two: 5+ S, 12+, forcing one round |
| P | rw2_pass | 1.000 | 0.820 | 40.0 | nothing to say opposite a weak two |
| 2H | rw2_new_D_H | 0.329 | 0.293 | 63.0 | new suit opposite the weak two: 5+ H, 12+, forcing one round |
| 2NT | rw2_2NT_ask | 0.134 | 0.122 | 70.0 | strong inquiry (15+), asking for a feature |
| 3D | rw2_raise3 | 0.015 | 0.013 | 60.0 | raise to play / furthering the preempt (RONF) |
| 3C | rw2_new_D_C | 0.000 | 0.000 | 63.0 | new suit opposite the weak two: 5+ C, 12+, forcing one round |
| 3NT | uc_nt3 | 0.000 | 0.000 | 29.0 | natural 3NT: 13-19 balanced, their suits stopped |
| 5D | uc_minor_game_5D | 0.000 | 0.000 | 28.0 | accepting to game in the raised minor: 17+ opposite the raise |
| 4D | uc_raise_D4 | 0.000 | 0.000 | 27.0 | raise of partner's D: 11+ support points, a real trump fit, and the va |
| 4NT | gst_rkc_D | 0.000 | 0.000 | 46.0 | RKC Blackwood 1430 for D: slam values opposite partner's shown range |

---

## Board 320 — margin -2 IMPs

dealer **N**, vul **None**, par(N/S) **-450**

    N  AJ854.QT.QT94.J5   (10 HCP)
    E  K6.KJ863.A3.AK92   (18 HCP)
    S  QT972.74.K86.T74   (5 HCP)
    W  3.A952.J752.Q863   (7 HCP)

Double-dummy tricks:

| declarer | C | D | H | S | NT |
|---|---|---|---|---|---|
| N | 2 | 5 | 2 | 7 | 2 |
| E | 11 | 8 | 11 | 6 | 10 |
| S | 2 | 5 | 2 | 7 | 2 |
| W | 11 | 8 | 11 | 6 | 10 |

Table A (**we are N/S**): 4SX by N (7 tricks), N/S score -500  
Table B (**we are E/W**): 4H by E (11 tricks), N/S score -450  
IMP margin for us: **-2**

### Table A — we are NS, BEN is EW

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | N | P | US | open_pass | P (1.00) |
| 1 | E | 1H | BEN |  |  |
| 2 | S | P | US | oc1H_pass | P (1.00) |
| 3 | W | 2H | BEN |  |  |
| 4 | N | 2S | US | cl_new_S2 | P (0.98) **≠** ← FIRST DIVERGENCE |
| 5 | E | 4H | BEN |  |  |
| 6 | S | 4S | US | ch_raise_lott_S4 | 4S (0.89) |
| 7 | W | P | BEN |  |  |
| 8 | N | P | US | fallback | P (1.00) |
| 9 | E | X | BEN |  |  |
| 10 | S | P | US | xd_pass | P (1.00) |
| 11 | W | P | BEN |  |  |
| 12 | N | P | US | fallback | P (1.00) |

### Table B — we are EW, BEN is NS

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | N | P | BEN |  |  |
| 1 | E | 1H | US | open_1H | 1H (1.00) |
| 2 | S | P | BEN |  |  |
| 3 | W | 3H | US | r1H_limit_raise | 2H (0.86) **≠** ← FIRST DIVERGENCE |
| 4 | N | P | BEN |  |  |
| 5 | E | 4H | US | op_lr_game | 3NT (0.92) **≠** |
| 6 | S | P | BEN |  |  |
| 7 | W | P | US | fallback | P (1.00) |
| 8 | N | P | BEN |  |  |

### First divergence: table A, call 4, seat N

auction so far: `P 1H P 2H`, hand `AJ854.QT.QT94.J5`

| call | rule | fit | score | prio | shows |
|---|---|---|---|---|---|
| 2S | cl_new_S2_hi **← DECIDED** | 1.000 | 0.779 | 26.5 | natural S at the cheapest level: 5+ cards, 10+ points (my longest suit |
| 2S | cl_new_S2 | 1.000 | 0.778 | 26.0 | natural S at the cheapest level: 5+ cards, 10+ points |
| P | cl_pass | 1.000 | 0.760 | 20.0 | no bid describes this hand: passing is the general agreement |
| X | cl_takeout_X | 0.409 | 0.331 | 36.0 | takeout-flavoured double: opening values, short in their suit |
| 2S | cl_new_long2_S_hi | 0.349 | 0.272 | 26.5 | natural S at the cheapest level: a SIX-card suit, 8+ points (my longes |
| 2S | cl_new_long2_S | 0.349 | 0.272 | 26.0 | natural S at the cheapest level: a SIX-card suit, 8+ points |
| 3D | cl_new_D3 | 0.047 | 0.037 | 27.0 | natural D at the cheapest level: 5+ cards, 14+ points |
| 3D | cl_new_D3_hi | 0.019 | 0.015 | 27.5 | natural D at the cheapest level: 5+ cards, 14+ points (my longest suit |
| 3D | cl_new_long3_D | 0.015 | 0.012 | 27.0 | natural D at the cheapest level: a SIX-card suit, 11+ points |
| 3D | cl_new_long3_D_hi | 0.006 | 0.005 | 27.5 | natural D at the cheapest level: a SIX-card suit, 11+ points (my longe |
| 2NT | cl_nt2_direct | 0.000 | 0.000 | 37.0 | natural 2NT over their two-level contract: 16-21 balanced, stopped |
| 3C | cl_new_C3 | 0.000 | 0.000 | 27.0 | natural C at the cheapest level: 5+ cards, 14+ points |
| 3C | cl_new_long3_C | 0.000 | 0.000 | 27.0 | natural C at the cheapest level: a SIX-card suit, 11+ points |
| 3C | cl_new_C3_hi | 0.000 | 0.000 | 27.5 | natural C at the cheapest level: 5+ cards, 14+ points (my longest suit |

---

## Board 347 — margin -2 IMPs

dealer **W**, vul **EW**, par(N/S) **+420**

    N  KQ4.JT85.84.A863   (10 HCP)
    E  JT953.62.72.T975   (1 HCP)
    S  2.AK974.KQJ53.42   (13 HCP)
    W  A876.Q3.AT96.KQJ   (16 HCP)

Double-dummy tricks:

| declarer | C | D | H | S | NT |
|---|---|---|---|---|---|
| N | 7 | 9 | 10 | 6 | 9 |
| E | 5 | 3 | 2 | 7 | 4 |
| S | 7 | 9 | 10 | 6 | 9 |
| W | 5 | 3 | 2 | 7 | 4 |

Table A (**we are N/S**): 3D by S (9 tricks), N/S score +110  
Table B (**we are E/W**): 3H by N (10 tricks), N/S score +170  
IMP margin for us: **-2**

### Table A — we are NS, BEN is EW

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | W | 1NT | BEN |  |  |
| 1 | N | P | US | v1NT_pass | P (1.00) |
| 2 | E | 2H | BEN |  |  |
| 3 | S | 3D | US | cl_new_D3 | 2S (0.66) **≠** ← FIRST DIVERGENCE |
| 4 | W | P | BEN |  |  |
| 5 | N | P | US | uc_pass | P (0.82) |
| 6 | E | P | BEN |  |  |

### Table B — we are EW, BEN is NS

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | W | 1NT | US | open_1NT | 1NT (1.00) |
| 1 | N | P | BEN |  |  |
| 2 | E | 2H | US | nt_transfer_S | 2H (1.00) |
| 3 | S | 2S | BEN |  |  |
| 4 | W | P | US | cl_pass | X (0.61) **≠** ← FIRST DIVERGENCE |
| 5 | N | 3H | BEN |  |  |
| 6 | E | P | US | ch_pass | P (1.00) |
| 7 | S | P | BEN |  |  |
| 8 | W | P | US | balhigh_pass | P (0.98) |

### First divergence: table A, call 3, seat S

auction so far: `1NT P 2H`, hand `2.AK974.KQJ53.42`

| call | rule | fit | score | prio | shows |
|---|---|---|---|---|---|
| 3D | cl_new_D3 **← DECIDED** | 1.000 | 0.781 | 27.0 | natural D at the cheapest level: 5+ cards, 14+ points |
| P | cl_pass | 1.000 | 0.760 | 20.0 | no bid describes this hand: passing is the general agreement |
| 3D | cl_new_D3_hi | 0.800 | 0.626 | 27.5 | natural D at the cheapest level: 5+ cards, 14+ points (my longest suit |
| 3D | cl_new_long3_D | 0.349 | 0.273 | 27.0 | natural D at the cheapest level: a SIX-card suit, 11+ points |
| 3D | cl_new_long3_D_hi | 0.279 | 0.218 | 27.5 | natural D at the cheapest level: a SIX-card suit, 11+ points (my longe |
| X | cl_takeout_X | 0.000 | 0.000 | 36.0 | takeout-flavoured double: opening values, short in their suit |
| 3C | cl_new_C3 | 0.000 | 0.000 | 27.0 | natural C at the cheapest level: 5+ cards, 14+ points |
| 2NT | cl_nt2_direct | 0.000 | 0.000 | 37.0 | natural 2NT over their two-level contract: 16-21 balanced, stopped |
| 3C | cl_new_long3_C | 0.000 | 0.000 | 27.0 | natural C at the cheapest level: a SIX-card suit, 11+ points |
| 3C | cl_new_C3_hi | 0.000 | 0.000 | 27.5 | natural C at the cheapest level: 5+ cards, 14+ points (my longest suit |
| 3C | cl_new_long3_C_hi | 0.000 | 0.000 | 27.5 | natural C at the cheapest level: a SIX-card suit, 11+ points (my longe |

---

## Board 360 — margin -2 IMPs

dealer **N**, vul **EW**, par(N/S) **+450**

    N  AQ73.A9.J74.AT76   (15 HCP)
    E  9.643.AQT986.K84   (9 HCP)
    S  KJ84.QJ872.K32.5   (10 HCP)
    W  T652.KT5.5.QJ932   (6 HCP)

Double-dummy tricks:

| declarer | C | D | H | S | NT |
|---|---|---|---|---|---|
| N | 6 | 7 | 10 | 11 | 9 |
| E | 6 | 5 | 3 | 2 | 4 |
| S | 6 | 7 | 10 | 11 | 8 |
| W | 6 | 5 | 3 | 2 | 4 |

Table A (**we are N/S**): 3NT by N (9 tricks), N/S score +400  
Table B (**we are E/W**): 4S by N (11 tricks), N/S score +450  
IMP margin for us: **-2**

### Table A — we are NS, BEN is EW

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | N | 1NT | US | open_1NT | 1NT (1.00) |
| 1 | E | 2C | BEN |  |  |
| 2 | S | 2H | US | cl_new_H2 | 2D (0.87) **≠** ← FIRST DIVERGENCE |
| 3 | W | P | BEN |  |  |
| 4 | N | 3NT | US | uc_nt3 | 2NT (0.96) **≠** |
| 5 | E | P | BEN |  |  |
| 6 | S | P | US | fallback | 4H (0.45) **≠** |
| 7 | W | P | BEN |  |  |

### Table B — we are EW, BEN is NS

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | N | 1NT | BEN |  |  |
| 1 | E | 2D | US | v1NT_2D | 2C (0.72) **≠** ← FIRST DIVERGENCE |
| 2 | S | 2H | BEN |  |  |
| 3 | W | P | US | cl_pass | P (0.99) |
| 4 | N | 2NT | BEN |  |  |
| 5 | E | P | US | cl_pass | P (1.00) |
| 6 | S | 3NT | BEN |  |  |
| 7 | W | P | US | ch_pass | P (1.00) |
| 8 | N | 4C | BEN |  |  |
| 9 | E | P | US | ch_pass | P (1.00) |
| 10 | S | 4H | BEN |  |  |
| 11 | W | P | US | ch_pass | P (1.00) |
| 12 | N | 4S | BEN |  |  |
| 13 | E | P | US | ch_pass | P (1.00) |
| 14 | S | P | BEN |  |  |
| 15 | W | P | US | balhigh_pass | P (1.00) |

### First divergence: table A, call 2, seat S

auction so far: `1NT 2C`, hand `KJ84.QJ872.K32.5`

| call | rule | fit | score | prio | shows |
|---|---|---|---|---|---|
| 2H | cl_new_H2_hi **← DECIDED** | 1.000 | 0.779 | 26.5 | natural H at the cheapest level: 5+ cards, 10+ points (my longest suit |
| 2H | cl_new_H2 | 1.000 | 0.778 | 26.0 | natural H at the cheapest level: 5+ cards, 10+ points |
| P | cl_pass | 1.000 | 0.760 | 20.0 | no bid describes this hand: passing is the general agreement |
| X | cl_negative_X2 | 0.349 | 0.279 | 33.0 | negative double at the two level: 8+ HCP with a major they have not bi |
| 2H | cl_new_long2_H_hi | 0.349 | 0.272 | 26.5 | natural H at the cheapest level: a SIX-card suit, 8+ points (my longes |
| 2H | cl_new_long2_H | 0.349 | 0.272 | 26.0 | natural H at the cheapest level: a SIX-card suit, 8+ points |
| 2S | cl_new_S2 | 0.349 | 0.272 | 26.0 | natural S at the cheapest level: 5+ cards, 10+ points |
| 2S | cl_new_S2_hi | 0.279 | 0.218 | 26.5 | natural S at the cheapest level: 5+ cards, 10+ points (my longest suit |
| 2S | cl_new_long2_S | 0.015 | 0.012 | 26.0 | natural S at the cheapest level: a SIX-card suit, 8+ points |
| 2S | cl_new_long2_S_hi | 0.012 | 0.009 | 26.5 | natural S at the cheapest level: a SIX-card suit, 8+ points (my longes |
| 2D | cl_new_D2 | 0.011 | 0.009 | 26.0 | natural D at the cheapest level: 5+ cards, 10+ points |
| 2D | cl_new_D2_hi | 0.001 | 0.000 | 26.5 | natural D at the cheapest level: 5+ cards, 10+ points (my longest suit |
| 2D | cl_new_long2_D | 0.000 | 0.000 | 26.0 | natural D at the cheapest level: a SIX-card suit, 8+ points |
| 2D | cl_new_long2_D_hi | 0.000 | 0.000 | 26.5 | natural D at the cheapest level: a SIX-card suit, 8+ points (my longes |

---

## Board 372 — margin -2 IMPs

dealer **N**, vul **NS**, par(N/S) **+600**

    N  AK95.A9.K654.943   (14 HCP)
    E  JT642.J53.9.AK86   (9 HCP)
    S  73.QT642.AQJT2.5   (9 HCP)
    W  Q8.K87.873.QJT72   (8 HCP)

Double-dummy tricks:

| declarer | C | D | H | S | NT |
|---|---|---|---|---|---|
| N | 5 | 11 | 10 | 6 | 8 |
| E | 8 | 2 | 2 | 6 | 5 |
| S | 5 | 11 | 10 | 6 | 8 |
| W | 8 | 2 | 2 | 6 | 5 |

Table A (**we are N/S**): 1SX by E (6 tricks), N/S score +100  
Table B (**we are E/W**): 2D by N (11 tricks), N/S score +150  
IMP margin for us: **-2**

### Table A — we are NS, BEN is EW

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | N | 1D | US | open_1D | 1D (1.00) |
| 1 | E | 1S | BEN |  |  |
| 2 | S | X | US | nx_1m1S_X | X (0.71) |
| 3 | W | P | BEN |  |  |
| 4 | N | P | US | adx_sit | 1NT (0.98) **≠** ← FIRST DIVERGENCE |
| 5 | E | P | BEN |  |  |

### Table B — we are EW, BEN is NS

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | N | 1D | BEN |  |  |
| 1 | E | 1S | US | oc1D_1S | 1S (0.96) |
| 2 | S | X | BEN |  |  |
| 3 | W | 2C | US | xd_run_C2 | P (1.00) **≠** ← FIRST DIVERGENCE |
| 4 | N | P | BEN |  |  |
| 5 | E | P | US | uc_pass | P (0.51) |
| 6 | S | 2D | BEN |  |  |
| 7 | W | P | US | cl_pass | P (1.00) |
| 8 | N | P | BEN |  |  |
| 9 | E | P | US | ballow_pass | 3C (0.64) **≠** |

### First divergence: table A, call 4, seat N

auction so far: `1D 1S X P`, hand `AK95.A9.K654.943`

| call | rule | fit | score | prio | shows |
|---|---|---|---|---|---|
| P | adx_sit **← DECIDED** | 1.000 | 0.883 | 61.0 | sitting the double: real trumps behind them |
| 1NT | onx_nt_DS | 1.000 | 0.874 | 58.0 | 12-14 balanced with their suit stopped |
| 3NT | uc_nt3 | 0.409 | 0.322 | 29.0 | natural 3NT: 13-19 balanced, their suits stopped |
| 2D | onx_rebid_DS | 0.349 | 0.304 | 57.0 | 5+ D, minimum |
| 3D | onx_jump_DS | 0.143 | 0.125 | 59.0 | jump rebid: 5+ D with 16-19, invitational |
| P | adx_pass_min | 0.134 | 0.115 | 52.0 | no suit worth pulling to and no trump stack: partner's double stands |
| 2NT | onx_jumpnt_DS | 0.028 | 0.025 | 58.5 | jump: 18-19 balanced with their suit stopped |
| 2H | onx_major_DS | 0.015 | 0.013 | 60.0 | supporting the major the double implied: 4 cards, minimum |
| 2C | uc_new_C2 | 0.001 | 0.001 | 26.0 | natural C at the cheapest level: 5+ cards, 10+ points |
| 2C | uc_new_C2_hi | 0.000 | 0.000 | 26.5 | natural C at the cheapest level: 5+ cards, 10+ points (my longest suit |
| 4H | uc_raise_H4 | 0.000 | 0.000 | 32.0 | raise of partner's H: 11+ support points, a real trump fit, and the va |
| 4H | uc_raise_lott4_H | 0.000 | 0.000 | 32.0 | the Law at the four level: they have a fit and so have we, ten-plus tr |

---

## Board 392 — margin -2 IMPs

dealer **N**, vul **EW**, par(N/S) **+140**

    N  AKJ6.K42.A8.T752   (15 HCP)
    E  52.A765.QT72.QJ6   (9 HCP)
    S  Q983.QT8.K64.843   (7 HCP)
    W  T74.J93.J953.AK9   (9 HCP)

Double-dummy tricks:

| declarer | C | D | H | S | NT |
|---|---|---|---|---|---|
| N | 8 | 6 | 7 | 9 | 7 |
| E | 5 | 7 | 6 | 4 | 6 |
| S | 8 | 6 | 7 | 9 | 7 |
| W | 5 | 7 | 6 | 4 | 6 |

Table A (**we are N/S**): 1NT by N (7 tricks), N/S score +90  
Table B (**we are E/W**): 3S by N (9 tricks), N/S score +140  
IMP margin for us: **-2**

### Table A — we are NS, BEN is EW

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | N | 1NT | US | open_1NT | 1NT (1.00) |
| 1 | E | P | BEN |  |  |
| 2 | S | P | US | nt_pass | 2C (1.00) **≠** ← FIRST DIVERGENCE |
| 3 | W | P | BEN |  |  |

### Table B — we are EW, BEN is NS

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | N | 1NT | BEN |  |  |
| 1 | E | P | US | v1NT_pass | P (1.00) |
| 2 | S | 2C | BEN |  |  |
| 3 | W | P | US | cl_pass | P (1.00) |
| 4 | N | 2S | BEN |  |  |
| 5 | E | P | US | cl_pass | P (1.00) |
| 6 | S | 3S | BEN |  |  |
| 7 | W | P | US | ch_pass | P (1.00) |
| 8 | N | P | BEN |  |  |
| 9 | E | P | US | balhigh_pass | P (1.00) |

### First divergence: table A, call 2, seat S

auction so far: `1NT P`, hand `Q983.QT8.K64.843`

| call | rule | fit | score | prio | shows |
|---|---|---|---|---|---|
| P | nt_pass **← DECIDED** | 1.000 | 0.775 | 25.0 | weak hand, no 5-card major |
| 2C | nt_stayman | 0.800 | 0.764 | 85.0 | Stayman: at least one 4-card major, invitational+ values |
| 2H | nt_transfer_S | 0.349 | 0.335 | 87.0 | Jacoby transfer to spades (5+ spades, any strength) |
| 2NT | nt_2NT_inv | 0.080 | 0.070 | 60.0 | invitational, 8-9 HCP, no 4-card major |
| 2S | uc_new_S2_hi | 0.035 | 0.028 | 26.5 | natural S at the cheapest level: 5+ cards, 10+ points (my longest suit |
| 2S | uc_new_S2 | 0.035 | 0.028 | 26.0 | natural S at the cheapest level: 5+ cards, 10+ points |
| 2D | nt_transfer_H | 0.015 | 0.014 | 88.0 | Jacoby transfer to hearts (5+ hearts, any strength) |
| 3NT | nt_3NT | 0.013 | 0.012 | 62.0 | to play, 10-15 HCP, no 4-card major |
| 3C | nt_3C_bail | 0.000 | 0.000 | 46.0 | weak bail: 6+ clubs, no game interest opposite 15-17 |
| 3D | nt_3D_bail | 0.000 | 0.000 | 46.0 | weak bail: 6+ diamonds, no game interest opposite 15-17 |
| 4NT | nt_4NT_quant | 0.000 | 0.000 | 64.0 | quantitative slam invitation, 16-17 HCP (not Blackwood) |
| 6NT | nt_6NT | 0.000 | 0.000 | 63.0 | to play: 18-20 HCP balanced opposite 15-17 |
| 4NT | nt_4NT_quant_minor | 0.000 | 0.000 | 63.0 | quantitative slam invitation: 12-15 with a running 6+ card minor |

---

## Board 395 — margin -2 IMPs

dealer **W**, vul **EW**, par(N/S) **+140**

    N  K42.AQJ.KQ92.T95   (15 HCP)
    E  AJ7.KT973.7.KQ72   (13 HCP)
    S  T9853.85.AJT5.A4   (9 HCP)
    W  Q6.642.8643.J863   (3 HCP)

Double-dummy tricks:

| declarer | C | D | H | S | NT |
|---|---|---|---|---|---|
| N | 5 | 8 | 5 | 9 | 7 |
| E | 7 | 4 | 8 | 4 | 5 |
| S | 5 | 9 | 4 | 9 | 7 |
| W | 7 | 4 | 8 | 4 | 5 |

Table A (**we are N/S**): 2H by E (8 tricks), N/S score -110  
Table B (**we are E/W**): 4S by N (9 tricks), N/S score -50  
IMP margin for us: **-2**

### Table A — we are NS, BEN is EW

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | W | P | BEN |  |  |
| 1 | N | 1NT | US | open_1NT | 1NT (1.00) |
| 2 | E | 2H | BEN |  |  |
| 3 | S | P | US | cl_pass | 2S (0.90) **≠** ← FIRST DIVERGENCE |
| 4 | W | P | BEN |  |  |
| 5 | N | P | US | ballow_pass | P (1.00) |

### Table B — we are EW, BEN is NS

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | W | P | US | open_pass | P (1.00) |
| 1 | N | 1NT | BEN |  |  |
| 2 | E | P | US | v1NT_pass | 2H (0.87) **≠** ← FIRST DIVERGENCE |
| 3 | S | 2H | BEN |  |  |
| 4 | W | P | US | cl_pass | P (1.00) |
| 5 | N | 2S | BEN |  |  |
| 6 | E | P | US | cl_pass | P (0.98) |
| 7 | S | 3D | BEN |  |  |
| 8 | W | P | US | ch_pass | P (1.00) |
| 9 | N | 4S | BEN |  |  |
| 10 | E | P | US | ch_pass | P (1.00) |
| 11 | S | P | BEN |  |  |
| 12 | W | P | US | balhigh_pass | P (1.00) |

### First divergence: table A, call 3, seat S

auction so far: `P 1NT 2H`, hand `T9853.85.AJT5.A4`

| call | rule | fit | score | prio | shows |
|---|---|---|---|---|---|
| P | cl_pass **← DECIDED** | 1.000 | 0.760 | 20.0 | no bid describes this hand: passing is the general agreement |
| X | cl_negative_X2 | 0.349 | 0.279 | 33.0 | negative double at the two level: 8+ HCP with a major they have not bi |
| 2NT | cl_nt2 | 0.342 | 0.268 | 28.0 | natural 2NT: 11-12 balanced with a stopper in their suit |
| 2S | cl_new_S2_hi | 0.329 | 0.257 | 26.5 | natural S at the cheapest level: 5+ cards, 10+ points (my longest suit |
| 2S | cl_new_S2 | 0.329 | 0.256 | 26.0 | natural S at the cheapest level: 5+ cards, 10+ points |
| 2S | cl_new_long2_S_hi | 0.264 | 0.206 | 26.5 | natural S at the cheapest level: a SIX-card suit, 8+ points (my longes |
| 2S | cl_new_long2_S | 0.264 | 0.206 | 26.0 | natural S at the cheapest level: a SIX-card suit, 8+ points |
| 3NT | cl_nt3 | 0.023 | 0.018 | 29.0 | natural 3NT: 13-19 balanced with a stopper in their suit |
| 3D | cl_new_long3_D | 0.012 | 0.009 | 27.0 | natural D at the cheapest level: a SIX-card suit, 11+ points |
| 3D | cl_new_D3 | 0.010 | 0.008 | 27.0 | natural D at the cheapest level: 5+ cards, 14+ points |
| 3D | cl_new_long3_D_hi | 0.005 | 0.004 | 27.5 | natural D at the cheapest level: a SIX-card suit, 11+ points (my longe |
| 3D | cl_new_D3_hi | 0.004 | 0.003 | 27.5 | natural D at the cheapest level: 5+ cards, 14+ points (my longest suit |
| 3C | cl_new_C3 | 0.000 | 0.000 | 27.0 | natural C at the cheapest level: 5+ cards, 14+ points |
| 3C | cl_new_long3_C | 0.000 | 0.000 | 27.0 | natural C at the cheapest level: a SIX-card suit, 11+ points |

---

## Board 411 — margin -2 IMPs

dealer **W**, vul **EW**, par(N/S) **-100**

    N  QJ2.T84.AQT64.Q3   (11 HCP)
    E  T764.A.92.KJT862   (8 HCP)
    S  AK93.QJ53.873.95   (10 HCP)
    W  85.K9762.KJ5.A74   (11 HCP)

Double-dummy tricks:

| declarer | C | D | H | S | NT |
|---|---|---|---|---|---|
| N | 4 | 8 | 7 | 8 | 5 |
| E | 9 | 3 | 5 | 4 | 4 |
| S | 4 | 8 | 7 | 8 | 5 |
| W | 9 | 4 | 5 | 4 | 4 |

Table A (**we are N/S**): 3D by N (8 tricks), N/S score -50  
Table B (**we are E/W**): passed out, N/S score +0  
IMP margin for us: **-2**

### Table A — we are NS, BEN is EW

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | W | 1H | BEN |  |  |
| 1 | N | 2D | US | oc1H_2D | P (0.92) **≠** ← FIRST DIVERGENCE |
| 2 | E | P | BEN |  |  |
| 3 | S | 3D | US | uc_raise_D3 | 3D (0.42) |
| 4 | W | P | BEN |  |  |
| 5 | N | P | US | uc_pass | P (1.00) |
| 6 | E | P | BEN |  |  |

### Table B — we are EW, BEN is NS

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | W | P | US | open_pass | 1H (0.96) **≠** ← FIRST DIVERGENCE |
| 1 | N | P | BEN |  |  |
| 2 | E | P | US | open_pass | P (0.96) |
| 3 | S | P | BEN |  |  |

### First divergence: table A, call 1, seat N

auction so far: `1H`, hand `QJ2.T84.AQT64.Q3`

| call | rule | fit | score | prio | shows |
|---|---|---|---|---|---|
| 2D | oc1H_2D **← DECIDED** | 1.000 | 0.895 | 65.0 | 2-level overcall: 5+ good diamonds, 11-17 |
| P | oc1H_pass | 1.000 | 0.775 | 25.0 | nothing suitable over 1H |
| 3D | oc1H_3D_jump | 0.279 | 0.245 | 59.0 | weak jump overcall: 6+ diamonds, 5-10 |
| X | oc1H_X | 0.122 | 0.112 | 72.0 | takeout double: opening values, short hearts, no five-card major (or a |
| 1S | oc1H_1S | 0.015 | 0.014 | 71.0 | overcall: 5+ spades, 8-16 |
| 3D | oc1H_3D_preempt | 0.012 | 0.010 | 58.0 | preemptive overcall: seven-card d suit, 3-10 |
| 1NT | oc1H_1NT | 0.006 | 0.005 | 82.0 | 1NT overcall: 15-18 balanced with a heart stopper |
| 2C | oc1H_2C | 0.000 | 0.000 | 65.0 | 2-level overcall: 5+ good clubs, 11-17 |
| 2S | oc1H_2S_jump | 0.000 | 0.000 | 60.0 | weak jump overcall: 6 spades, 5-10 |
| 3S | oc1H_3S_preempt | 0.000 | 0.000 | 58.0 | preemptive overcall: seven-card s suit, 3-10 |
| 3C | oc1H_3m_jump | 0.000 | 0.000 | 59.0 | weak jump overcall: 6+ clubs, 5-10 |
| 4S | oc1H_4S_preempt | 0.000 | 0.000 | 59.0 | preemptive overcall: eight-card s suit, 3-10 |
| 3C | oc1H_3C_preempt | 0.000 | 0.000 | 58.0 | preemptive overcall: seven-card c suit, 3-10 |

---

## Board 417 — margin -2 IMPs

dealer **E**, vul **None**, par(N/S) **+140**

    N  KT6.5.AJ95.Q6432   (10 HCP)
    E  5.KQJT943.832.95   (6 HCP)
    S  A932.86.KQ4.KJT8   (13 HCP)
    W  QJ874.A72.T76.A7   (11 HCP)

Double-dummy tricks:

| declarer | C | D | H | S | NT |
|---|---|---|---|---|---|
| N | 10 | 10 | 5 | 9 | 5 |
| E | 3 | 3 | 8 | 4 | 7 |
| S | 10 | 10 | 5 | 9 | 5 |
| W | 3 | 3 | 8 | 4 | 7 |

Table A (**we are N/S**): 3H by E (8 tricks), N/S score +50  
Table B (**we are E/W**): 4C by N (10 tricks), N/S score +130  
IMP margin for us: **-2**

### Table A — we are NS, BEN is EW

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | E | 3H | BEN |  |  |
| 1 | S | P | US | v3_H_pass | X (0.95) **≠** ← FIRST DIVERGENCE |
| 2 | W | P | BEN |  |  |
| 3 | N | P | US | balhigh_pass | P (0.95) |

### Table B — we are EW, BEN is NS

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | E | 3H | US | open_3H_nv | 3H (0.96) |
| 1 | S | X | BEN |  |  |
| 2 | W | P | US | xd_pass | 4H (0.73) **≠** ← FIRST DIVERGENCE |
| 3 | N | 4C | BEN |  |  |
| 4 | E | P | US | ch_pass | P (1.00) |
| 5 | S | P | BEN |  |  |
| 6 | W | P | US | balhigh_pass | 4H (0.50) **≠** |

### First divergence: table A, call 1, seat S

auction so far: `3H`, hand `A932.86.KQ4.KJT8`

| call | rule | fit | score | prio | shows |
|---|---|---|---|---|---|
| P | v3_H_pass **← DECIDED** | 1.000 | 0.790 | 30.0 | nothing suitable over their preempt |
| X | v3_H_X | 0.800 | 0.728 | 70.0 | takeout double of the 3-level preempt |
| 3NT | v3_H_3NT | 0.027 | 0.024 | 66.0 | to play: 16-21 with a stopper |
| 4C | v3_H_C | 0.015 | 0.013 | 64.0 | overcalling the preempt: good 6+ C, 13+ |
| 3S | v3_H_S | 0.011 | 0.010 | 64.0 | overcalling the preempt: good 6+ S, 13+ |
| 4D | v3_H_D | 0.000 | 0.000 | 64.0 | overcalling the preempt: good 6+ D, 13+ |
| 4S | v3_H_4S | 0.000 | 0.000 | 65.0 | overcalling the preempt at the four level: eight of them, or seven wit |

---

## Board 475 — margin -2 IMPs

dealer **W**, vul **EW**, par(N/S) **-100**

    N  Q85.T864.KT6.J52   (6 HCP)
    E  762.AJ932.J7.A97   (10 HCP)
    S  AT.Q7.AQ942.K843   (15 HCP)
    W  KJ943.K5.853.QT6   (9 HCP)

Double-dummy tricks:

| declarer | C | D | H | S | NT |
|---|---|---|---|---|---|
| N | 7 | 8 | 5 | 5 | 7 |
| E | 5 | 5 | 8 | 8 | 6 |
| S | 7 | 8 | 5 | 5 | 7 |
| W | 5 | 5 | 7 | 8 | 6 |

Table A (**we are N/S**): 3NT by S (7 tricks), N/S score -100  
Table B (**we are E/W**): 3D by S (8 tricks), N/S score -50  
IMP margin for us: **-2**

### Table A — we are NS, BEN is EW

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | W | P | BEN |  |  |
| 1 | N | P | US | open_pass | P (1.00) |
| 2 | E | P | BEN |  |  |
| 3 | S | 1D | US | open_1D_rule15 | 1D (1.00) |
| 4 | W | 1S | BEN |  |  |
| 5 | N | X | US | nx_1m1S_X | X (0.99) |
| 6 | E | P | BEN |  |  |
| 7 | S | 2D | US | onx_rebid_DS | 2C (0.93) **≠** ← FIRST DIVERGENCE |
| 8 | W | P | BEN |  |  |
| 9 | N | P | US | uc_pass | P (1.00) |
| 10 | E | 2S | BEN |  |  |
| 11 | S | 3NT | US | cl_nt3 | P (0.55) **≠** |
| 12 | W | P | BEN |  |  |
| 13 | N | P | US | fallback | P (0.99) |
| 14 | E | P | BEN |  |  |

### Table B — we are EW, BEN is NS

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | W | P | US | open_pass | P (1.00) |
| 1 | N | P | BEN |  |  |
| 2 | E | P | US | open_pass | P (0.92) |
| 3 | S | 1D | BEN |  |  |
| 4 | W | 1S | US | oc1D_1S | 1S (0.91) |
| 5 | N | X | BEN |  |  |
| 6 | E | P | US | xd_pass | P (0.60) |
| 7 | S | 2C | BEN |  |  |
| 8 | W | P | US | cl_pass | P (1.00) |
| 9 | N | 2D | BEN |  |  |
| 10 | E | 2S | US | cl_raise_S2 | 2S (0.94) |
| 11 | S | 3D | BEN |  |  |
| 12 | W | P | US | ch_pass | P (0.99) |
| 13 | N | P | BEN |  |  |
| 14 | E | P | US | balhigh_pass | P (0.91) |

### First divergence: table A, call 7, seat S

auction so far: `P P P 1D 1S X P`, hand `AT.Q7.AQ942.K843`

| call | rule | fit | score | prio | shows |
|---|---|---|---|---|---|
| 2D | onx_rebid_DS **← DECIDED** | 1.000 | 0.871 | 57.0 | 5+ D, minimum |
| 3NT | uc_nt3 | 1.000 | 0.787 | 29.0 | natural 3NT: 13-19 balanced, their suits stopped |
| 3D | onx_jump_DS | 0.800 | 0.702 | 59.0 | jump rebid: 5+ D with 16-19, invitational |
| 1NT | onx_nt_DS | 0.800 | 0.699 | 58.0 | 12-14 balanced with their suit stopped |
| 2C | uc_new_C2 | 0.264 | 0.206 | 26.0 | natural C at the cheapest level: 5+ cards, 10+ points |
| 2NT | onx_jumpnt_DS | 0.134 | 0.117 | 58.5 | jump: 18-19 balanced with their suit stopped |
| 2C | uc_new_C2_hi | 0.108 | 0.084 | 26.5 | natural C at the cheapest level: 5+ cards, 10+ points (my longest suit |
| 2H | onx_major_DS | 0.015 | 0.013 | 60.0 | supporting the major the double implied: 4 cards, minimum |
| 4H | uc_raise_H4 | 0.000 | 0.000 | 32.0 | raise of partner's H: 11+ support points, a real trump fit, and the va |
| 4H | uc_raise_lott4_H | 0.000 | 0.000 | 32.0 | the Law at the four level: they have a fit and so have we, ten-plus tr |

---

## Board 516 — margin -2 IMPs

dealer **N**, vul **NS**, par(N/S) **-90**

    N  AKQ74.T92.J95.A5   (14 HCP)
    E  8.Q64.AKQ4.T8732   (11 HCP)
    S  5.J73.T8632.KJ96   (5 HCP)
    W  JT9632.AK85.7.Q4   (10 HCP)

Double-dummy tricks:

| declarer | C | D | H | S | NT |
|---|---|---|---|---|---|
| N | 5 | 7 | 5 | 3 | 6 |
| E | 8 | 5 | 7 | 7 | 7 |
| S | 5 | 7 | 5 | 3 | 6 |
| W | 8 | 5 | 7 | 7 | 7 |

Table A (**we are N/S**): 2H by W (7 tricks), N/S score +50  
Table B (**we are E/W**): 3H by W (7 tricks), N/S score +100  
IMP margin for us: **-2**

### Table A — we are NS, BEN is EW

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | N | 1S | US | open_1S | 1S (1.00) |
| 1 | E | X | BEN |  |  |
| 2 | S | 2D | US | xd_run_D2 | P (1.00) **≠** ← FIRST DIVERGENCE |
| 3 | W | 2H | BEN |  |  |
| 4 | N | P | US | cl_pass | 3D (0.74) **≠** |
| 5 | E | P | BEN |  |  |
| 6 | S | P | US | ballow_pass | P (1.00) |

### Table B — we are EW, BEN is NS

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | N | 1S | BEN |  |  |
| 1 | E | X | US | oc1S_X | X (0.98) |
| 2 | S | P | BEN |  |  |
| 3 | W | 3H | US | advS_3H_jump | 2H (0.90) **≠** ← FIRST DIVERGENCE |
| 4 | N | P | BEN |  |  |
| 5 | E | P | US | uc_pass | P (0.73) |
| 6 | S | P | BEN |  |  |

### First divergence: table A, call 2, seat S

auction so far: `1S X`, hand `5.J73.T8632.KJ96`

| call | rule | fit | score | prio | shows |
|---|---|---|---|---|---|
| 2D | xd_run_D2 **← DECIDED** | 1.000 | 0.775 | 25.0 | running to my own D: 5+ cards |
| P | rdx_pass | 1.000 | 0.760 | 20.0 | weak |
| 2C | xd_run_C2 | 0.349 | 0.270 | 25.0 | running to my own C: 5+ cards |
| 2S | jordan_raise | 0.015 | 0.013 | 60.0 | single raise, slightly wider than uncontested |
| XX | rdx_XX | 0.004 | 0.003 | 75.0 | redouble: 10+ HCP, interest in penalizing |
| 2H | rx_S_2H | 0.000 | 0.000 | 62.0 | new suit over their double: 5+ H, 9-11, non-forcing |
| 3S | jordan_preempt | 0.000 | 0.000 | 62.0 | preemptive raise: 4+ trumps, weak |
| 1NT | rx_S_1NT | 0.000 | 0.000 | 58.0 | 6-9 balanced over their takeout double |
| 2NT | jordan_2NT | 0.000 | 0.000 | 80.0 | Jordan 2NT: 4+ S, limit raise or better |

---

## Board 625 — margin -2 IMPs

dealer **E**, vul **None**, par(N/S) **-80**

    N  Q82.K8.K873.J542   (9 HCP)
    E  6.9752.J942.KT87   (4 HCP)
    S  K97.QT643.AT6.Q9   (11 HCP)
    W  AJT543.AJ.Q5.A63   (16 HCP)

Double-dummy tricks:

| declarer | C | D | H | S | NT |
|---|---|---|---|---|---|
| N | 5 | 7 | 6 | 6 | 6 |
| E | 7 | 6 | 6 | 7 | 5 |
| S | 5 | 7 | 6 | 6 | 6 |
| W | 7 | 6 | 6 | 7 | 6 |

Table A (**we are N/S**): 2S by W (7 tricks), N/S score +50  
Table B (**we are E/W**): 3S by W (7 tricks), N/S score +100  
IMP margin for us: **-2**

### Table A — we are NS, BEN is EW

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | E | P | BEN |  |  |
| 1 | S | P | US | open_pass | 1H (0.85) **≠** ← FIRST DIVERGENCE |
| 2 | W | 1S | BEN |  |  |
| 3 | N | P | US | oc1S_pass | P (1.00) |
| 4 | E | P | BEN |  |  |
| 5 | S | 1NT | US | bal_1NT | 2H (0.89) **≠** |
| 6 | W | 2S | BEN |  |  |
| 7 | N | P | US | cl_pass | P (0.82) |
| 8 | E | P | BEN |  |  |
| 9 | S | P | US | ballow_pass | P (1.00) |

### Table B — we are EW, BEN is NS

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | E | P | US | open_pass | P (1.00) |
| 1 | S | 1H | BEN |  |  |
| 2 | W | 1S | US | oc1H_1S | 1S (1.00) |
| 3 | N | X | BEN |  |  |
| 4 | E | P | US | xd_pass | P (1.00) |
| 5 | S | 2H | BEN |  |  |
| 6 | W | 3S | US | cl_rebid_jump_S | 2S (0.97) **≠** ← FIRST DIVERGENCE |
| 7 | N | P | BEN |  |  |
| 8 | E | P | US | uc_pass | P (1.00) |
| 9 | S | P | BEN |  |  |

### First divergence: table A, call 1, seat S

auction so far: `P`, hand `K97.QT643.AT6.Q9`

| call | rule | fit | score | prio | shows |
|---|---|---|---|---|---|
| P | open_pass **← DECIDED** | 1.000 | 0.760 | 20.0 | fewer than opening values |
| 1H | open_1H | 0.800 | 0.752 | 80.0 | 5+ hearts, 12-21 HCP |
| 1H | open_1H_rule20 | 0.800 | 0.747 | 78.0 | 5+ hearts, light opening satisfying the rule of 20 |
| 2H | open_weak_2H_nv | 0.279 | 0.250 | 65.0 | weak two: 6 hearts, 5-10 HCP |
| 1D | open_1D | 0.080 | 0.074 | 74.0 | opening, 3+ diamonds (better minor), no 5-card major, 12-21 HCP |
| 1NT | open_1NT | 0.028 | 0.027 | 92.0 | 15-17 balanced (may contain a 5-card major) |
| 1C | open_1C | 0.028 | 0.026 | 73.0 | opening, 3+ clubs (better minor), no 5-card major, 12-21 HCP |
| 3H | open_3H_nv | 0.006 | 0.005 | 60.0 | preempt: 7+ hearts, 3-9 HCP |
| 1S | open_1S | 0.005 | 0.005 | 81.0 | 5+ spades, 12-21 HCP |
| 1S | open_1S_rule20 | 0.004 | 0.003 | 79.0 | 5+ spades, light opening satisfying the rule of 20 |
| 1D | open_1m_rule20 | 0.001 | 0.001 | 72.0 | 5+ diamonds, light opening satisfying the rule of 20 |
| 4H | open_4H | 0.000 | 0.000 | 61.0 | preempt: 8+ hearts, 3-10 HCP |
| 1C | open_1C_rule20 | 0.000 | 0.000 | 71.0 | 5+ clubs, light opening satisfying the rule of 20 |
| 2S | open_weak_2S_nv | 0.000 | 0.000 | 66.0 | weak two: 6 spades, 5-10 HCP |

---

## Board 660 — margin -2 IMPs

dealer **N**, vul **NS**, par(N/S) **+110**

    N  A86.J82.9743.J84   (6 HCP)
    E  KQT72.K74.AT8.97   (12 HCP)
    S  43.AQT6.KQ62.AT5   (15 HCP)
    W  J95.953.J5.KQ632   (7 HCP)

Double-dummy tricks:

| declarer | C | D | H | S | NT |
|---|---|---|---|---|---|
| N | 7 | 9 | 8 | 6 | 7 |
| E | 6 | 4 | 5 | 7 | 6 |
| S | 7 | 9 | 8 | 6 | 7 |
| W | 6 | 4 | 5 | 7 | 5 |

Table A (**we are N/S**): 2S by E (7 tricks), N/S score +50  
Table B (**we are E/W**): 3D by N (9 tricks), N/S score +110  
IMP margin for us: **-2**

### Table A — we are NS, BEN is EW

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | N | P | US | open_pass | P (1.00) |
| 1 | E | 1S | BEN |  |  |
| 2 | S | X | US | oc1S_X | X (0.65) |
| 3 | W | 2S | BEN |  |  |
| 4 | N | P | US | cl_pass | P (0.99) |
| 5 | E | P | BEN |  |  |
| 6 | S | P | US | ballow_pass | X (0.94) **≠** ← FIRST DIVERGENCE |

### Table B — we are EW, BEN is NS

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | N | P | BEN |  |  |
| 1 | E | 1S | US | open_1S | 1S (1.00) |
| 2 | S | X | BEN |  |  |
| 3 | W | 2S | US | jordan_raise | 2S (0.97) |
| 4 | N | P | BEN |  |  |
| 5 | E | P | US | uc_pass | P (1.00) |
| 6 | S | X | BEN |  |  |
| 7 | W | P | US | xd_pass | P (1.00) |
| 8 | N | 3D | BEN |  |  |
| 9 | E | P | US | ch_pass | P (0.86) |
| 10 | S | P | BEN |  |  |
| 11 | W | P | US | balhigh_pass | 3S (0.57) **≠** ← FIRST DIVERGENCE |

### First divergence: table A, call 6, seat S

auction so far: `P 1S X 2S P P`, hand `43.AQT6.KQ62.AT5`

| call | rule | fit | score | prio | shows |
|---|---|---|---|---|---|
| P | ballow_pass **← DECIDED** | 1.000 | 0.763 | 21.0 | nothing worth reopening on: passing it out |
| 3D | ballow_new_D3 | 0.349 | 0.273 | 27.0 | natural D at the cheapest level: 5+ cards, 14+ points |
| 3H | ballow_new_H3 | 0.349 | 0.273 | 27.0 | natural H at the cheapest level: 5+ cards, 14+ points |
| 2NT | ballow_nt2_strong | 0.342 | 0.270 | 30.0 | natural 2NT: 17-21 balanced with their suit stopped |
| X | ballow_reopen_X2 | 0.028 | 0.023 | 41.0 | a SECOND double: 19+, still nothing to say but takeout |
| 3C | ballow_new_C3 | 0.015 | 0.012 | 27.0 | natural C at the cheapest level: 5+ cards, 14+ points |
| 3D | ballow_new_long3_D | 0.015 | 0.012 | 27.0 | natural D at the cheapest level: a SIX-card suit, 11+ points |
| 3H | ballow_new_long3_H | 0.015 | 0.012 | 27.0 | natural H at the cheapest level: a SIX-card suit, 11+ points |
| 2NT | ballow_nt2 | 0.003 | 0.002 | 28.0 | natural 2NT: 11-12 balanced with a stopper in their suit |
| 3C | ballow_new_long3_C | 0.000 | 0.000 | 27.0 | natural C at the cheapest level: a SIX-card suit, 11+ points |
| 3NT | ballow_nt3 | 0.000 | 0.000 | 29.0 | natural 3NT: 13-19 balanced with a stopper in their suit |

---

## Board 735 — margin -2 IMPs

dealer **W**, vul **Both**, par(N/S) **+120**

    N  QJ3.AJ5.K83.AK32   (18 HCP)
    E  76.QT43.AJ9.QJ94   (10 HCP)
    S  KT8.9872.QT74.86   (5 HCP)
    W  A9542.K6.652.T75   (7 HCP)

Double-dummy tricks:

| declarer | C | D | H | S | NT |
|---|---|---|---|---|---|
| N | 7 | 8 | 8 | 7 | 8 |
| E | 6 | 4 | 5 | 5 | 5 |
| S | 7 | 8 | 8 | 7 | 8 |
| W | 6 | 4 | 5 | 5 | 5 |

Table A (**we are N/S**): 1C by N (7 tricks), N/S score +70  
Table B (**we are E/W**): 2NT by N (8 tricks), N/S score +120  
IMP margin for us: **-2**

### Table A — we are NS, BEN is EW

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | W | P | BEN |  |  |
| 1 | N | 1C | US | open_1C | 1C (1.00) |
| 2 | E | P | BEN |  |  |
| 3 | S | P | US | r1m_pass | 1H (1.00) **≠** ← FIRST DIVERGENCE |
| 4 | W | P | BEN |  |  |

### Table B — we are EW, BEN is NS

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | W | P | US | open_pass | P (1.00) |
| 1 | N | 1C | BEN |  |  |
| 2 | E | P | US | oc1C_pass | P (1.00) |
| 3 | S | 1H | BEN |  |  |
| 4 | W | P | US | sw_pass | P (0.93) |
| 5 | N | 2NT | BEN |  |  |
| 6 | E | P | US | cl_pass | P (1.00) |
| 7 | S | P | BEN |  |  |
| 8 | W | P | US | ballow_pass | P (1.00) |

### First divergence: table A, call 3, seat S

auction so far: `P 1C P`, hand `KT8.9872.QT74.86`

| call | rule | fit | score | prio | shows |
|---|---|---|---|---|---|
| P | r1m_pass **← DECIDED** | 1.000 | 0.745 | 15.0 | 0-5 HCP: too weak to respond |
| 1H | r1m_1H | 0.800 | 0.742 | 76.0 | 4+ hearts, 6+ HCP (up the line), or a six-card suit on 3+ |
| 1S | r1m_1S | 0.114 | 0.106 | 77.0 | 4+ spades longer than hearts, five-five in the majors, or a six-card s |
| 1NT | r1m_1NT | 0.080 | 0.067 | 45.0 | 6-10 HCP, no 4-card major |
| 1D | r1C_1D | 0.028 | 0.026 | 74.0 | 4+ diamonds (5+ or unbalanced), 6+ HCP, no 4-card major (Walsh style) |
| 2NT | r1m_2NT | 0.000 | 0.000 | 54.0 | invitational: 11-12 balanced, no 4-card major |
| 2C | r1m_2over1 | 0.000 | 0.000 | 70.0 | 2/1 game forcing: 4+ clubs, 12+ HCP |
| 3NT | r1m_3NT | 0.000 | 0.000 | 55.0 | 13-15 balanced, no 4-card major |
| 3C | r1m_raise3 | 0.000 | 0.000 | 52.0 | limit raise: 5+ C support, 10-12 HCP, no 4-card major |
| 4C | uc_raise_C4 | 0.000 | 0.000 | 27.0 | raise of partner's C: 11+ support points, a real trump fit, and the va |
| 5C | uc_minor_game_5C | 0.000 | 0.000 | 28.0 | accepting to game in the raised minor: 17+ opposite the raise |

---

## Board 739 — margin -2 IMPs

dealer **W**, vul **None**, par(N/S) **+400**

    N  Q8.AT4.KQT7.AKJ8   (19 HCP)
    E  AJT9.J3.A9.97543   (10 HCP)
    S  K75.9765.853.QT2   (5 HCP)
    W  6432.KQ82.J642.6   (6 HCP)

Double-dummy tricks:

| declarer | C | D | H | S | NT |
|---|---|---|---|---|---|
| N | 8 | 8 | 8 | 5 | 9 |
| E | 5 | 4 | 5 | 7 | 4 |
| S | 8 | 8 | 8 | 5 | 9 |
| W | 5 | 4 | 5 | 7 | 4 |

Table A (**we are N/S**): 1D by N (8 tricks), N/S score +90  
Table B (**we are E/W**): 2NT by N (9 tricks), N/S score +150  
IMP margin for us: **-2**

### Table A — we are NS, BEN is EW

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | W | P | BEN |  |  |
| 1 | N | 1D | US | open_1D | 1D (1.00) |
| 2 | E | P | BEN |  |  |
| 3 | S | P | US | r1m_pass | 1H (1.00) **≠** ← FIRST DIVERGENCE |
| 4 | W | P | BEN |  |  |

### Table B — we are EW, BEN is NS

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | W | P | US | open_pass | P (1.00) |
| 1 | N | 1D | BEN |  |  |
| 2 | E | P | US | oc1D_pass | P (1.00) |
| 3 | S | 1H | BEN |  |  |
| 4 | W | P | US | sw_pass | P (1.00) |
| 5 | N | 2NT | BEN |  |  |
| 6 | E | P | US | cl_pass | P (1.00) |
| 7 | S | P | BEN |  |  |
| 8 | W | P | US | ballow_pass | P (1.00) |

### First divergence: table A, call 3, seat S

auction so far: `P 1D P`, hand `K75.9765.853.QT2`

| call | rule | fit | score | prio | shows |
|---|---|---|---|---|---|
| P | r1m_pass **← DECIDED** | 1.000 | 0.745 | 15.0 | 0-5 HCP: too weak to respond |
| 1H | r1m_1H | 0.800 | 0.742 | 76.0 | 4+ hearts, 6+ HCP (up the line), or a six-card suit on 3+ |
| 1S | r1m_1S | 0.114 | 0.106 | 77.0 | 4+ spades longer than hearts, five-five in the majors, or a six-card s |
| 1NT | r1m_1NT | 0.080 | 0.067 | 45.0 | 6-10 HCP, no 4-card major |
| 2D | r1D_raise2 | 0.028 | 0.024 | 50.0 | simple raise: 4+ diamond support, 6-10 HCP, no 4-card major |
| 2NT | r1m_2NT | 0.000 | 0.000 | 54.0 | invitational: 11-12 balanced, no 4-card major |
| 2C | r1m_2over1 | 0.000 | 0.000 | 70.0 | 2/1 game forcing: 4+ clubs, 12+ HCP |
| 3D | r1m_raise3 | 0.000 | 0.000 | 52.0 | limit raise: 5+ D support, 10-12 HCP, no 4-card major |
| 3NT | r1m_3NT | 0.000 | 0.000 | 55.0 | 13-15 balanced, no 4-card major |
| 4D | uc_raise_D4 | 0.000 | 0.000 | 27.0 | raise of partner's D: 11+ support points, a real trump fit, and the va |
| 5D | uc_minor_game_5D | 0.000 | 0.000 | 28.0 | accepting to game in the raised minor: 17+ opposite the raise |

---

## Board 848 — margin -2 IMPs

dealer **N**, vul **None**, par(N/S) **-90**

    N  K95.JT85.J4.KQ92   (10 HCP)
    E  Q74.AK6.AQ63.J43   (16 HCP)
    S  AT63.Q4.T9872.75   (6 HCP)
    W  J82.9732.K5.AT86   (8 HCP)

Double-dummy tricks:

| declarer | C | D | H | S | NT |
|---|---|---|---|---|---|
| N | 6 | 7 | 6 | 7 | 6 |
| E | 7 | 6 | 7 | 6 | 7 |
| S | 6 | 7 | 6 | 7 | 6 |
| W | 7 | 6 | 7 | 6 | 7 |

Table A (**we are N/S**): 2NT by E (7 tricks), N/S score +50  
Table B (**we are E/W**): 3NT by E (7 tricks), N/S score +100  
IMP margin for us: **-2**

### Table A — we are NS, BEN is EW

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | N | P | US | open_pass | P (1.00) |
| 1 | E | 1NT | BEN |  |  |
| 2 | S | P | US | v1NT_pass | P (1.00) |
| 3 | W | 2C | BEN |  |  |
| 4 | N | P | US | cl_pass | P (1.00) |
| 5 | E | 2D | BEN |  |  |
| 6 | S | P | US | cl_pass | P (1.00) |
| 7 | W | 2NT | BEN |  |  |
| 8 | N | P | US | cl_pass | P (1.00) |
| 9 | E | P | BEN |  |  |
| 10 | S | P | US | ballow_pass | P (1.00) |

### Table B — we are EW, BEN is NS

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | N | P | BEN |  |  |
| 1 | E | 1NT | US | open_1NT | 1NT (1.00) |
| 2 | S | P | BEN |  |  |
| 3 | W | 2C | US | nt_stayman | 2C (1.00) |
| 4 | N | P | BEN |  |  |
| 5 | E | 2D | US | stayman_2D | 2D (1.00) |
| 6 | S | P | BEN |  |  |
| 7 | W | 2NT | US | stm_2D_2NT | 2NT (1.00) |
| 8 | N | P | BEN |  |  |
| 9 | E | 3NT | US | stmi_2D_3NT | P (0.63) **≠** ← FIRST DIVERGENCE |
| 10 | S | P | BEN |  |  |
| 11 | W | P | US | fallback | P (1.00) |
| 12 | N | P | BEN |  |  |

### First divergence: table B, call 9, seat E

auction so far: `P 1NT P 2C P 2D P 2NT P`, hand `Q74.AK6.AQ63.J43`

| call | rule | fit | score | prio | shows |
|---|---|---|---|---|---|
| 3NT | stmi_2D_3NT **← DECIDED** | 1.000 | 0.874 | 58.0 | accepting the invite: 16-17 |
| P | stmi_2D_pass | 0.800 | 0.704 | 60.0 | declining the invite: minimum 1NT opener |
| 3D | uc_rebid_D3 | 0.015 | 0.012 | 27.0 | rebid of my own D: 6+ cards, values for the level opposite partner's s |
| 3H | uc_new_H3 | 0.015 | 0.012 | 27.0 | natural H at the cheapest level: 5+ cards, 14+ points |
| 3S | uc_new_S3 | 0.011 | 0.009 | 27.0 | natural S at the cheapest level: 5+ cards, 14+ points |
| 3H | uc_new_H3_hi | 0.009 | 0.007 | 27.5 | natural H at the cheapest level: 5+ cards, 14+ points (my longest suit |
| 3S | uc_new_S3_hi | 0.009 | 0.007 | 27.5 | natural S at the cheapest level: 5+ cards, 14+ points (my longest suit |
| 3C | uc_new_C3 | 0.005 | 0.004 | 27.0 | natural C at the cheapest level: 5+ cards, 14+ points |
| 3C | uc_new_C3_hi | 0.001 | 0.001 | 27.5 | natural C at the cheapest level: 5+ cards, 14+ points (my longest suit |

---

## Board 899 — margin -2 IMPs

dealer **W**, vul **None**, par(N/S) **+100**

    N  KJT2.J74.AT7.K62   (12 HCP)
    E  85.K92.KJ53.AT74   (11 HCP)
    S  A64.6.Q842.QJ983   (9 HCP)
    W  Q973.AQT853.96.5   (8 HCP)

Double-dummy tricks:

| declarer | C | D | H | S | NT |
|---|---|---|---|---|---|
| N | 9 | 7 | 4 | 8 | 5 |
| E | 4 | 5 | 8 | 5 | 7 |
| S | 9 | 7 | 4 | 8 | 5 |
| W | 4 | 5 | 8 | 5 | 7 |

Table A (**we are N/S**): 3H by W (8 tricks), N/S score +50  
Table B (**we are E/W**): 3C by N (9 tricks), N/S score +110  
IMP margin for us: **-2**

### Table A — we are NS, BEN is EW

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | W | P | BEN |  |  |
| 1 | N | 1C | US | open_1C | 1C (1.00) |
| 2 | E | P | BEN |  |  |
| 3 | S | 1D | US | r1C_1D | 3C (0.83) **≠** ← FIRST DIVERGENCE |
| 4 | W | 2H | BEN |  |  |
| 5 | N | P | US | cl_pass | P (1.00) |
| 6 | E | 3H | BEN |  |  |
| 7 | S | P | US | ch_pass | P (0.64) |
| 8 | W | P | BEN |  |  |
| 9 | N | P | US | balhigh_pass | P (0.99) |

### Table B — we are EW, BEN is NS

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | W | P | US | open_pass | P (0.53) |
| 1 | N | 1C | BEN |  |  |
| 2 | E | P | US | oc1C_pass | P (1.00) |
| 3 | S | 3C | BEN |  |  |
| 4 | W | P | US | ch_pass | P (0.99) |
| 5 | N | P | BEN |  |  |
| 6 | E | P | US | balhigh_pass | P (1.00) |

### First divergence: table A, call 3, seat S

auction so far: `P 1C P`, hand `A64.6.Q842.QJ983`

| call | rule | fit | score | prio | shows |
|---|---|---|---|---|---|
| 1D | r1C_1D **← DECIDED** | 1.000 | 0.922 | 74.0 | 4+ diamonds (5+ or unbalanced), 6+ HCP, no 4-card major (Walsh style) |
| 1NT | r1m_1NT | 1.000 | 0.835 | 45.0 | 6-10 HCP, no 4-card major |
| 3C | r1m_raise3 | 0.800 | 0.685 | 52.0 | limit raise: 5+ C support, 10-12 HCP, no 4-card major |
| 1S | r1m_1S | 0.349 | 0.325 | 77.0 | 4+ spades longer than hearts, five-five in the majors, or a six-card s |
| 2C | r1m_2over1 | 0.134 | 0.122 | 70.0 | 2/1 game forcing: 4+ clubs, 12+ HCP |
| P | r1m_pass | 0.028 | 0.021 | 15.0 | 0-5 HCP: too weak to respond |
| 1H | r1m_1H | 0.000 | 0.000 | 76.0 | 4+ hearts, 6+ HCP (up the line), or a six-card suit on 3+ |
| 4C | uc_raise_C4 | 0.000 | 0.000 | 27.0 | raise of partner's C: 11+ support points, a real trump fit, and the va |
| 5C | uc_minor_game_5C | 0.000 | 0.000 | 28.0 | accepting to game in the raised minor: 17+ opposite the raise |
| 2NT | r1m_2NT | 0.000 | 0.000 | 54.0 | invitational: 11-12 balanced, no 4-card major |
| 3NT | r1m_3NT | 0.000 | 0.000 | 55.0 | 13-15 balanced, no 4-card major |

---

## Board 920 — margin -2 IMPs

dealer **N**, vul **EW**, par(N/S) **-620**

    N  A95.832.QJ764.T3   (7 HCP)
    E  T732.T7.953.AQJ2   (7 HCP)
    S  KQ.KJ965.8.98764   (9 HCP)
    W  J864.AQ4.AKT2.K5   (17 HCP)

Double-dummy tricks:

| declarer | C | D | H | S | NT |
|---|---|---|---|---|---|
| N | 5 | 5 | 6 | 3 | 4 |
| E | 8 | 8 | 7 | 10 | 8 |
| S | 5 | 5 | 6 | 3 | 4 |
| W | 8 | 8 | 7 | 10 | 8 |

Table A (**we are N/S**): 2S by W (10 tricks), N/S score -170  
Table B (**we are E/W**): 2NT by W (8 tricks), N/S score -120  
IMP margin for us: **-2**

### Table A — we are NS, BEN is EW

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | N | P | US | open_pass | P (1.00) |
| 1 | E | P | BEN |  |  |
| 2 | S | P | US | open_pass | 2H (0.99) **≠** ← FIRST DIVERGENCE |
| 3 | W | 1NT | BEN |  |  |
| 4 | N | P | US | v1NT_pass | P (1.00) |
| 5 | E | 2C | BEN |  |  |
| 6 | S | 2H | US | cl_new_H2 | P (0.81) **≠** |
| 7 | W | P | BEN |  |  |
| 8 | N | P | US | uc_pass | P (0.77) |
| 9 | E | X | BEN |  |  |
| 10 | S | P | US | xd_pass | P (1.00) |
| 11 | W | 2S | BEN |  |  |
| 12 | N | P | US | cl_pass | P (0.70) |
| 13 | E | P | BEN |  |  |
| 14 | S | P | US | ballow_pass | P (1.00) |

### Table B — we are EW, BEN is NS

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | N | P | BEN |  |  |
| 1 | E | P | US | open_pass | P (1.00) |
| 2 | S | 2H | BEN |  |  |
| 3 | W | 2NT | US | vw2_2NT | 2NT (0.90) |
| 4 | N | P | BEN |  |  |
| 5 | E | P | US | a2nw_pass_H | P (0.56) |
| 6 | S | P | BEN |  |  |

### First divergence: table A, call 2, seat S

auction so far: `P P`, hand `KQ.KJ965.8.98764`

| call | rule | fit | score | prio | shows |
|---|---|---|---|---|---|
| P | open_pass **← DECIDED** | 1.000 | 0.760 | 20.0 | fewer than opening values |
| 1H | open_1H_rule20_third | 0.640 | 0.598 | 78.0 | 5+ hearts, third-seat light opening satisfying the rule of 20 |
| 2H | open_weak_2H_nv | 0.349 | 0.312 | 65.0 | weak two: 6 hearts, 5-10 HCP |
| 1H | open_1H_third_light | 0.329 | 0.305 | 75.0 | third-seat light opening: 5+ good hearts, 9-11 |
| 1H | open_1H | 0.134 | 0.126 | 80.0 | 5+ hearts, 12-21 HCP |
| 3H | open_3H_nv | 0.015 | 0.013 | 60.0 | preempt: 7+ hearts, 3-9 HCP |
| 1C | open_1C | 0.013 | 0.012 | 73.0 | opening, 3+ clubs (better minor), no 5-card major, 12-21 HCP |
| 1C | open_1C_rule20_third | 0.005 | 0.005 | 71.0 | 5+ c, third-seat light opening satisfying the rule of 20 |
| 3C | open_3C_nv | 0.001 | 0.001 | 60.0 | preempt: 7+ clubs, 3-9 HCP |
| 4H | open_4H | 0.000 | 0.000 | 61.0 | preempt: 8+ hearts, 3-10 HCP |
| 1S | open_1S_third_light | 0.000 | 0.000 | 76.0 | third-seat light opening: 5+ good spades, 9-11 |
| 1S | open_1S_rule20_third | 0.000 | 0.000 | 79.0 | 5+ spades, third-seat light opening satisfying the rule of 20 |
| 1S | open_1S | 0.000 | 0.000 | 81.0 | 5+ spades, 12-21 HCP |
| 1D | open_1D | 0.000 | 0.000 | 74.0 | opening, 3+ diamonds (better minor), no 5-card major, 12-21 HCP |

---

## Board 928 — margin -2 IMPs

dealer **N**, vul **None**, par(N/S) **-100**

    N  Q3.K842.74.A9873   (9 HCP)
    E  A86.JT976.J65.KJ   (10 HCP)
    S  954.Q3.AKQT9.Q54   (13 HCP)
    W  KJT72.A5.832.T62   (8 HCP)

Double-dummy tricks:

| declarer | C | D | H | S | NT |
|---|---|---|---|---|---|
| N | 8 | 8 | 6 | 5 | 6 |
| E | 3 | 5 | 6 | 8 | 6 |
| S | 8 | 8 | 6 | 5 | 6 |
| W | 3 | 5 | 6 | 8 | 6 |

Table A (**we are N/S**): 2S by W (8 tricks), N/S score -110  
Table B (**we are E/W**): 3C by N (8 tricks), N/S score -50  
IMP margin for us: **-2**

### Table A — we are NS, BEN is EW

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | N | P | US | open_pass | P (1.00) |
| 1 | E | P | BEN |  |  |
| 2 | S | 1D | US | open_1D | 1D (1.00) |
| 3 | W | 1S | BEN |  |  |
| 4 | N | X | US | nx_1m1S_X | X (1.00) |
| 5 | E | P | BEN |  |  |
| 6 | S | 2D | US | onx_rebid_DS | 1NT (0.60) **≠** ← FIRST DIVERGENCE |
| 7 | W | P | BEN |  |  |
| 8 | N | P | US | uc_pass | P (0.94) |
| 9 | E | 2S | BEN |  |  |
| 10 | S | P | US | cl_pass | P (0.97) |
| 11 | W | P | BEN |  |  |
| 12 | N | P | US | ballow_pass | P (0.61) |

### Table B — we are EW, BEN is NS

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | N | P | BEN |  |  |
| 1 | E | P | US | open_pass | P (1.00) |
| 2 | S | 1D | BEN |  |  |
| 3 | W | 1S | US | oc1D_1S | 1S (0.87) |
| 4 | N | X | BEN |  |  |
| 5 | E | P | US | xd_pass | P (0.71) |
| 6 | S | 1NT | BEN |  |  |
| 7 | W | P | US | cl_pass | P (1.00) |
| 8 | N | P | BEN |  |  |
| 9 | E | 2S | US | ballow_raise_S2 | 2S (0.95) |
| 10 | S | P | BEN |  |  |
| 11 | W | P | US | uc_pass | P (1.00) |
| 12 | N | 3C | BEN |  |  |
| 13 | E | P | US | ch_pass | P (0.71) |
| 14 | S | P | BEN |  |  |
| 15 | W | P | US | balhigh_pass | P (0.99) |

### First divergence: table A, call 6, seat S

auction so far: `P P 1D 1S X P`, hand `954.Q3.AKQT9.Q54`

| call | rule | fit | score | prio | shows |
|---|---|---|---|---|---|
| 2D | onx_rebid_DS **← DECIDED** | 1.000 | 0.871 | 57.0 | 5+ D, minimum |
| 1NT | onx_nt_DS | 0.835 | 0.729 | 58.0 | 12-14 balanced with their suit stopped |
| 3NT | uc_nt3 | 0.342 | 0.269 | 29.0 | natural 3NT: 13-19 balanced, their suits stopped |
| 3D | onx_jump_DS | 0.134 | 0.118 | 59.0 | jump rebid: 5+ D with 16-19, invitational |
| 2H | onx_major_DS | 0.015 | 0.013 | 60.0 | supporting the major the double implied: 4 cards, minimum |
| 2C | uc_new_C2 | 0.011 | 0.009 | 26.0 | natural C at the cheapest level: 5+ cards, 10+ points |
| 2NT | onx_jumpnt_DS | 0.003 | 0.003 | 58.5 | jump: 18-19 balanced with their suit stopped |
| 2C | uc_new_C2_hi | 0.001 | 0.001 | 26.5 | natural C at the cheapest level: 5+ cards, 10+ points (my longest suit |
| 4H | uc_raise_H4 | 0.000 | 0.000 | 32.0 | raise of partner's H: 11+ support points, a real trump fit, and the va |
| 4H | uc_raise_lott4_H | 0.000 | 0.000 | 32.0 | the Law at the four level: they have a fit and so have we, ten-plus tr |

---

## Board 933 — margin -2 IMPs

dealer **E**, vul **NS**, par(N/S) **-420**

    N  KJ42.KT5.T654.Q7   (9 HCP)
    E  Q983.63.AQJ7.A65   (13 HCP)
    S  6.QJ98742.82.K92   (6 HCP)
    W  AT75.A.K93.JT843   (12 HCP)

Double-dummy tricks:

| declarer | C | D | H | S | NT |
|---|---|---|---|---|---|
| N | 2 | 3 | 8 | 3 | 3 |
| E | 11 | 10 | 5 | 10 | 7 |
| S | 2 | 3 | 8 | 3 | 3 |
| W | 11 | 10 | 5 | 10 | 7 |

Table A (**we are N/S**): 3S by E (10 tricks), N/S score -170  
Table B (**we are E/W**): 3H by S (8 tricks), N/S score -100  
IMP margin for us: **-2**

### Table A — we are NS, BEN is EW

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | E | 1D | BEN |  |  |
| 1 | S | 3H | US | oc1D_3H_preempt | 3H (0.67) |
| 2 | W | X | BEN |  |  |
| 3 | N | P | US | xd_pass | 4H (0.50) **≠** ← FIRST DIVERGENCE |
| 4 | E | 3S | BEN |  |  |
| 5 | S | P | US | ch_pass | P (1.00) |
| 6 | W | P | BEN |  |  |
| 7 | N | P | US | balhigh_pass | P (0.98) |

### Table B — we are EW, BEN is NS

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | E | 1D | US | open_1D | 1D (1.00) |
| 1 | S | 3H | BEN |  |  |
| 2 | W | P | US | ch_pass | X (0.98) **≠** ← FIRST DIVERGENCE |
| 3 | N | P | BEN |  |  |
| 4 | E | P | US | balhigh_pass | P (0.77) |

### First divergence: table A, call 3, seat N

auction so far: `1D 3H X`, hand `KJ42.KT5.T654.Q7`

| call | rule | fit | score | prio | shows |
|---|---|---|---|---|---|
| P | xd_pass **← DECIDED** | 1.000 | 0.754 | 18.0 | sitting for their double: no better spot to run to |
| 4H | FALLBACK | 0.409 | 0.301 | 12.0 | raise: 3+ H, about 12-+ support points |
| 3S | xd_run_S3 | 0.015 | 0.012 | 26.0 | running to my own S: 6+ cards |
| 3NT | FALLBACK | 0.001 | 0.001 | 10.0 | natural NT, 14-19 HCP, stoppers in their suit(s) (undiscussed) |
| 4NT | gst_rkc_H | 0.000 | 0.000 | 46.0 | RKC Blackwood 1430 for H: slam values opposite partner's shown range |

---

## Board 934 — margin -2 IMPs

dealer **S**, vul **NS**, par(N/S) **-420**

    N  A63.KJ732.64.985   (8 HCP)
    E  JT82.AQ8.T3.AQ76   (13 HCP)
    S  5.T96.AKQ9752.43   (9 HCP)
    W  KQ974.54.J8.KJT2   (10 HCP)

Double-dummy tricks:

| declarer | C | D | H | S | NT |
|---|---|---|---|---|---|
| N | 3 | 8 | 8 | 3 | 7 |
| E | 9 | 4 | 5 | 10 | 5 |
| S | 3 | 8 | 8 | 3 | 7 |
| W | 9 | 4 | 5 | 10 | 5 |

Table A (**we are N/S**): 3S by W (10 tricks), N/S score -170  
Table B (**we are E/W**): 3D by S (8 tricks), N/S score -100  
IMP margin for us: **-2**

### Table A — we are NS, BEN is EW

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | S | 3D | US | open_3D_vul | 3D (0.98) |
| 1 | W | P | BEN |  |  |
| 2 | N | P | US | rp3_D_pass | P (0.88) |
| 3 | E | X | BEN |  |  |
| 4 | S | P | US | xd_pass | P (1.00) |
| 5 | W | 3S | BEN |  |  |
| 6 | N | P | US | ch_pass | P (1.00) |
| 7 | E | P | BEN |  |  |
| 8 | S | P | US | balhigh_pass | P (1.00) |

### Table B — we are EW, BEN is NS

| # | seat | call | whose | deciding rule | BEN would call |
|---|---|---|---|---|---|
| 0 | S | 3D | BEN |  |  |
| 1 | W | P | US | v3_D_pass | P (1.00) |
| 2 | N | P | BEN |  |  |
| 3 | E | P | US | balhigh_pass | X (0.95) **≠** ← FIRST DIVERGENCE |

### First divergence: table B, call 3, seat E

auction so far: `3D P P`, hand `JT82.AQ8.T3.AQ76`

| call | rule | fit | score | prio | shows |
|---|---|---|---|---|---|
| P | balhigh_pass **← DECIDED** | 1.000 | 0.763 | 21.0 | nothing worth reopening on: passing it out |
| X | balhigh_X | 0.800 | 0.656 | 40.0 | balancing double: values are marked opposite a passing partner, with a |
| 3S | balhigh_new_S3 | 0.211 | 0.165 | 27.0 | natural S at the cheapest level: 5+ cards, 14+ points |
| 3NT | FALLBACK | 0.160 | 0.117 | 10.0 | natural NT, 14-19 HCP, stoppers in their suit(s) (undiscussed) |
| 3H | balhigh_new_H3 | 0.012 | 0.009 | 27.0 | natural H at the cheapest level: 5+ cards, 14+ points |

---
