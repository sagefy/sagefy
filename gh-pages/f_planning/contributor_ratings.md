---
title: Contributor Ratings and Proposal Friction
layout: default
---

<script
src="//cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML">
</script>

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

The following criteria could be considered:

- The number of contributors voting "yes": $$c$$
- The sum of contributor scores: $$s$$
- The number of learners impacted: $$l$$
- The quality of the entity: $$q$$

The number of contributors should grow linearly, while other factors should consider some form of exponential. In particular, the sum of contributors scores would likely be $$s^2$$ while the number of learners may be as high as $$l^{10}$$, and the quality score would tighten approaching 1.

A simple formulation may be:

$$l=10^{\sqrt{\frac{s}{30}}}$$

$$s=(\log_{10}l)^2*30$$

Such results in:

- 75s == 38l
- 125s == 110l
- 250s == 770l
- 500s == 12,092l
- 750s == 100,000l
- 1000s == 593,612l
