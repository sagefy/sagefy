"""
Primary
-------

- Learner-Card Ability -- pC

    pC = pL * (1 - pS) + (1 - pL) * pG

- Learner-Unit Ability -- pL

    pL = pL or 0.4
    pLN = score * pL * (1 - pS) / (pL * (1 - pS) + (1 - pL) * pG) + \
          (1 - score) * pL * pS / (pL * pS + (1 - pL) * (1 - pG))

    pL = pLN + (1 - pLN) * pT
        (possible alt: pL = pLN + (1 - pLN) * pT * pB)

- Learner-Unit Confidence -- pB

    pB = pB or 0.5
    str = 2 * pL * pB / (pL + pB)
    pB = pB + exp(k * (t0 - t1) / str) - 1
    k = ???

- Card Guess and Slip -- pG and pS

    if score == 1:
        pG += (0.3 - pG) * (1 - pL) * 0.05
        pS -= pS * pL * 0.05
    else:
        pG -= pG * (1 - pL) * 0.05
        pS += (0.1 - pS) * pL * 0.05

    ... or ...

    if score == 1:
        pG += ((0.3 - pG) * (1 - pL)) ** 2
        pS -= (pS * pL) ** 2
    else:
        pG -= (pG * (1 - pL)) ** 2
        pS += ((0.2 - pS) * pL) ** 2

    ... 1 > score > 0 ...?

    pG = pG + score * ((0.3 - pG) * (1 - pL)) ** 2
            - (1 - score) * (pG * (1 - pL)) ** 2
    pS = pS - score * (pS * pL) ** 2
            + (1 - score) * ((0.2 - pS) * pL) ** 2

- Card Quality -- pT [transit] -- both if response and not response

    (pL0) A  B  C (pL1)

    pT[A]1 += ((pL1 / pL0) - 1 - pT[A]0) * 0.05

    or

    pT[A]1 ±= ((pL1 / pL0) - 1 - pT[A]0) ** 2   ... keep the sign ...

Auxillary
---------

- Learner-Set Ability -- pLS

    pLS = mean(unit.pL for unit in units)

- Unit Quality -- uQ

    uQ = mean(learner.pL for learner in learners)

- Set Quality -- sQ

    sQ = mean(unit.uQ for unit in units)

- Card Time -- cD

    ??? (Doesn't matter.)

- Unit Difficulty/Time -- uD

    ???

- Set Difficulty/Time -- sD

    sD = sum(unit.uD for unit in units)

****************************

p0   --   0.5
s0   --   0.05
g0   --   0.2
t0   --   0.05
Learned   pL >= 0.95
Needs review/diagnosis   pB < 0.85

P(AnsG | Correct) = 1 - P(L)
P(AnsS | Incorrect) = P(L)


"""
