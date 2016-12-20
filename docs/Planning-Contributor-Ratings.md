---
layout: docs
title: Planning> Contributor Ratings
---

The decision for a proposal to become the accepted version is a calculation of a few factors: the reputation of the proposer and voters and the usage of the entity.

![State diagram](https://docs.google.com/drawings/d/1YEmyN7elZebEoPOquy31CTZTP1wnTUjgqMGP4ywpeqM/pub?w=641&h=394)

Entity Calculation
------------------

"Yes" vote power is calculated as the sum of the proposer and the "yes" voters' vote power.

"No" vote power is calculated as the sum of the "no" voters' vote power.

To accept a proposal, the proposal requires `log2(number_of_learners)` in "yes" vote power.

To block a proposal, the proposal requires `log100(number_of_learners)` in "no" vote power.

To unblock a proposal, the amount must be reduced below this amount. Otherwise, the proposer can decline their proposal.

### Example

- Number of Learners, To Accept, To Block
- 1, 0, 0
- 10, 3.32, 0.5
- 100, 6.64, 1
- 1000, 9.97, 1.5
- 10000, 13.28, 2
- 100000, 16.61, 2.5

Contributor Calculation
-----------------------

Each proposal and vote for a proposal in accepted state counts as +1 point. The vote power is calculated as `1 - e ^ (-points / 40)`.

### Example

- Points: Power
- 0: 0
- 5: 0.12
- 10: 0.22
- 20: 0.39
- 50: 0.71
- 100: 0.91
- 150: 0.97
- 200: 0.99
