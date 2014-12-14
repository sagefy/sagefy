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

- Card Guess -- pG

    ???

- Card Slip -- pS

    ???

- Card Quality -- pT [transit] -- both if response and not response

    ???

Auxillary
---------

- Learner-Set Ability -- pLS

    pLS = mean(unit.pL for unit in units)

- Unit Quality -- uQ

    uQ = mean(learner.pL for learner in learners)

- Set Quality -- sQ

    sQ = mean(unit.uQ for unit in units)

- Card Difficulty -- cD

    ???

- Unit Difficulty -- uD

    ???

- Set Difficulty -- sD

    sD = sum(unit.uD for unit in units)

****************************

p0   --   0.5
Learned   pL >= 0.95
Needs review/diagnosis   pB < 0.85

P(AnsG | Correct) = 1 - P(L)
P(AnsG | Incorrect) = 0
P(AnsS | Incorrect) = P(L)
P(AnsS | Correct) = 0

p(C | G, L) = p(L) + (1 - p(L)) * pG
p(I | G, L) = 1 - p(L) + (1 - p(L)) * pG
p(C | S, L) = p(L) - p(L) * p(S)
p(I | S, L) = 1 - p(L) - p(L) * p(S)

p(G | C, L) = p(G) * p(C | G, L) / p(L)
p(G | I, L) = p(G) * p(I | G, L) / (1 - p(L))

P(S | C, L) = P(S) * p(C | S, L) / P(L)
P(S | I, L) = P(S) * p(I | S, L) / (1 - P(L))

"""
