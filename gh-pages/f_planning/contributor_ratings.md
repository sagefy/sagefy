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

Proposals V1
------------

A proposal requires two "yes" votes after the initial proposal to be accepted.

A single "no" vote will change the status of the proposal to blocked. One of two things unblock the proposal: the "no" votes changes their vote to "discuss" or "yes", or the original proposer declines their proposal.

![State diagram](https://docs.google.com/drawings/d/1YEmyN7elZebEoPOquy31CTZTP1wnTUjgqMGP4ywpeqM/pub?w=641&h=394)

Proposal V2: Friction
---------------------

All proposals require at least two yes votes in addition to the original proposal.

Proposals that are more likely to impact learners directly should have more friction to acceptance. Below describes the sum of contributor scores needed to approve a proposal, including the original proposer's score. A contributor with a score of -2 or -1 has an effective score of 0. A contributor with a score lower than -2 cannot propose or vote.

Creating a set or a unit, with no other information, should require little approval. Updating or removing a set, unit, or creating, updating or removing a card should factor in the number of learners impacted and the quality of the entity.
