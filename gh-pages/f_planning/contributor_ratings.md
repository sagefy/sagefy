---
title: Contributor Ratings and Proposal Friction
layout: default
---

Contributor Rating
------------------

We consider contributor rating based on **proposals** and **votes**.

- ` 0`: I create a proposal
- `-1`: I create a proposal, and it's blocked
- ` 0`: I create a proposal, and I decline it
- `+1`: I create a proposal, and it's accepted
- ` 0`: I vote for a proposal
- `-1`: I vote for a proposal, and it's blocked
- ` 0`: I vote for a proposal, but it's declined
- `+1`: I vote for a proposal, and it's accepted
- ` 0`: I vote against a proposal, and it's blocked
- `+1`: I vote against a proposal, and it's declined by its creator

Note that these are _per status_, not per action. For example, I create a proposal, it's blocked, then I decline it, the result is the 0, not -1.

Proposal Friction
-----------------

Proposals that are more likely to impact learners directly should have more friction to acceptance. Below describes the sum of contributor scores needed to approve a proposal, including the original proposer's score. A contributor with a score of -2 or -1 has an effective score of 0. A contributor with a score lower than -2 cannot propose or vote. All proposals require at least two yes votes in addition to the original proposal.

- Create set: 1
- Create unit: 1
- Create card: [Num Learners] * [Unit Quality] * c0
- Update/delete set: [Num Learners] * [Set Quality] * c1
- Update/delete unit: [Num Learners] * [Unit Quality] * c2
- Update/delete card: [Num Learners (Unit)] * harmonic([Unit Quality], [Card Quality]) * c3
