---
layout: default
title: Planning> Contributor Ratings
---

The decision for a proposal to become the accepted version is a calculation of a few factors: the reputation of the proposer and voters and the usage of the entity.

<!--
digraph workflow {
  concentrate=true
  compound=true

  graph [
    fontsize=18
    fontcolor="#222222"
    color="#eeeeee"
  ]
  node [
    fontsize=12
    fontcolor="#333333"
    color="#dddddd"
    shape="ellipse"
  ]
  edge [
    fontsize=10
    color="#cccccc"
    fontcolor="#666666"
  ]

  "Create Proposal" -> Pending
  Pending -> { Accepted, Blocked }
  { Pending, Blocked } -> Declined
}
-->

<svg width="210" height="260" viewBox="0 0 210 260" xmlns="http://www.w3.org/2000/svg"><style>.a{fill:none;stroke:#ddd;}.b{fill:#333;text-anchor:middle;}.c{fill:none;stroke:#ccc;}.d{fill:#ccc;stroke:#ccc;}</style><g class="graph" transform="scale(1 1)rotate(0)translate(4 256)"><title> workflow</title><polygon points="-4 4 -4 -256 206 -256 206 4 -4 4" style="fill:#fff;stroke:transparent"/><g class="node"><title> Create Proposal</title><text x="132.2" y="-230.4"  font-size="12.00" class="b"> Create Proposal</text></g><g class="node"><title> Pending</title><text x="132.2" y="-158.4"  font-size="12.00" class="b"> Pending</text></g><g class="edge"><title> Create Proposal-&gt;Pending</title><path d="M132.2-215.8C132.2-208.1 132.2-199 132.2-190.4" class="c"/><polygon points="135.7 -190.4 132.2 -180.4 128.7 -190.4 135.7 -190.4" class="d"/></g><g class="node"><title> Accepted</title><text x="39.2" y="-86.4"  font-size="12.00" class="b"> Accepted</text></g><g class="edge"><title> Pending-&gt;Accepted</title><path d="M112.4-146.7C99.3-136.6 81.9-123.1 67.4-111.8" class="c"/><polygon points="69.2 -108.8 59.2 -105.5 64.9 -114.4 69.2 -108.8" class="d"/></g><g class="node"><title> Blocked</title><text x="132.2" y="-86.4"  font-size="12.00" class="b"> Blocked</text></g><g class="edge"><title> Pending-&gt;Blocked</title><path d="M132.2-143.8C132.2-136.1 132.2-127 132.2-118.4" class="c"/><polygon points="135.7 -118.4 132.2 -108.4 128.7 -118.4 135.7 -118.4" class="d"/></g><g class="node"><title> Declined</title><text x="164.2" y="-14.4"  font-size="12.00" class="b"> Declined</text></g><g class="edge"><title> Pending-&gt;Declined</title><path d="M150.2-146.5C160.2-136.6 171.8-122.9 177.2-108 184.5-87.8 180.3-63.7 174.9-45.5" class="c"/><polygon points="178.1 -44.2 171.6 -35.8 171.5 -46.4 178.1 -44.2" class="d"/></g><g class="edge"><title> Blocked-&gt;Declined</title><path d="M140.1-72.2C143.7-64.1 148-54.3 152.1-45.2" class="c"/><polygon points="155.4 -46.4 156.2 -35.8 149 -43.6 155.4 -46.4" class="d"/></g></g></svg>

## Entity Calculation

"Yes" vote power is calculated as the sum of the proposer and the "yes" voters' vote power.

"No" vote power is calculated as the sum of the "no" voters' vote power.

To accept a proposal, the proposal requires `log5(number_of_learners)` in "yes" vote power.

To block a proposal, the proposal requires `log100(number_of_learners)` in "no" vote power.

To unblock a proposal, the amount must be reduced below this amount. Otherwise, the proposer can decline their proposal.

### Example

| Number of Learners | To Accept | To Block |
| -----------------: | --------: | -------: |
|                  1 |         0 |        0 |
|                 10 |      1.43 |      0.5 |
|                100 |      2.86 |      1.0 |
|               1000 |      4.29 |      1.5 |
|              10000 |      5.72 |      2.0 |
|             100000 |      7.15 |      2.5 |

## Contributor Calculation

Each proposal and vote for a proposal in accepted state counts as +1 point. The vote power is calculated as `1 - e ^ (-points / 40)`.

### Example

| Points | Power |
| -----: | ----: |
|      0 |     0 |
|      5 |  0.12 |
|     10 |  0.22 |
|     20 |  0.39 |
|     50 |  0.71 |
|    100 |  0.91 |
|    150 |  0.97 |
|    200 |  0.99 |
