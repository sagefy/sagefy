---
layout: docs
title: Cards & Subjects
---

_There are two types of entities in Sagefy: cards and subjects._

- A **card** is a single learning activity.

  > Examples: a 3-minute video or a multiple choice question.

- A **subject** is a collection of cards and other subjects.

  > Like a course, but at any scale. Such as “Measures of Central
  > Tendency”, “Intro to Statistics”, or even a complete statistics program.

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
    shape="plaintext"
  ]
  edge [
    fontsize=10
    color="#cccccc"
    fontcolor="#666666"
  ]

  desc [label="Subject:\nDescriptive Statistics", group=g0]
  central [label="Subject:\nCentral Tendency", group=g0]
  hist [label="Subject:\nHistograms", group=g0]
  std [label="Subject:\nStandard Deviation", group=g0]
  mmm [label="Subject:\nMean, Median, Mode", group=g1]
  ran [label="Subject:\nRanges", group=g1]
  dist [label="Subject:\nDistributions", group=g1]
  vid [label="Video Card:\nMean, Median, Mode", group=g2]
  choice [label="Choice Card:\nFind the Mean", group=g2]
  embed [label="Embed Card:\nSelect the Mean", group=g2]

  desc -> { central, hist, std }
  central -> { mmm, ran, dist }
  mmm -> { vid, choice, embed }

  { hist, central } -> std [style="dotted", weight=-1, constraint=false, arrowhead=odot]
  mmm -> ran [style="dotted", weight=-1, constraint=false, arrowhead=odot]
  { mmm, ran } -> dist [style="dotted", weight=-1, constraint=false, arrowhead=odot]
}
-->

<style>svg{max-width:100%;}</style>

<svg width="748" height="263pt" viewBox="0 0 561.47 263.2" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"><g id="graph0" class="graph" transform="scale(1 1) rotate(0) translate(4 259.2)"><title>workflow</title><polygon fill="#fff" stroke="transparent" points="-4,4 -4,-259.2 557.472,-259.2 557.472,4 -4,4"/><g id="node1" class="node"><title>desc</title><text text-anchor="middle" x="390.985" y="-240.4"  font-size="12" fill="#333">Subject:</text><text text-anchor="middle" x="390.985" y="-226"  font-size="12" fill="#333">Descriptive Statistics</text></g><g id="node2" class="node"><title>central</title><text text-anchor="middle" x="286.985" y="-167.6"  font-size="12" fill="#333">Subject:</text><text text-anchor="middle" x="286.985" y="-153.2"  font-size="12" fill="#333">Central Tendency</text></g><g id="edge1" class="edge"><title>desc-&gt;central</title><path fill="none" stroke="#ccc" d="M364.741,-218.4295C351.6851,-209.2904 335.7311,-198.1226 321.6799,-188.2867"/><polygon fill="#ccc" stroke="#ccc" points="323.4193,-185.232 313.2198,-182.3646 319.405,-190.9666 323.4193,-185.232"/></g><g id="node3" class="node"><title>hist</title><text text-anchor="middle" x="390.985" y="-167.6"  font-size="12" fill="#333">Subject:</text><text text-anchor="middle" x="390.985" y="-153.2"  font-size="12" fill="#333">Histograms</text></g><g id="edge2" class="edge"><title>desc-&gt;hist</title><path fill="none" stroke="#ccc" d="M390.9846,-218.4295C390.9846,-210.5836 390.9846,-201.2426 390.9846,-192.5328"/><polygon fill="#ccc" stroke="#ccc" points="394.4847,-192.3646 390.9846,-182.3646 387.4847,-192.3647 394.4847,-192.3646"/></g><g id="node4" class="node"><title>std</title><text text-anchor="middle" x="498.985" y="-167.6"  font-size="12" fill="#333">Subject:</text><text text-anchor="middle" x="498.985" y="-153.2"  font-size="12" fill="#333">Standard Deviation</text></g><g id="edge3" class="edge"><title>desc-&gt;std</title><path fill="none" stroke="#ccc" d="M418.2376,-218.4295C431.9235,-209.2041 448.6761,-197.9117 463.3673,-188.0087"/><polygon fill="#ccc" stroke="#ccc" points="465.4046,-190.8564 471.7404,-182.3646 461.492,-185.0519 465.4046,-190.8564"/></g><g id="edge10" class="edge"><title>central-&gt;std</title><path fill="none" stroke="#ccc" stroke-dasharray="1,5" d="M313.8426,-182.3243C325.8686,-189.4605 340.5676,-196.7841 354.9846,-200.4 386.0232,-208.1848 395.857,-207.8211 426.9846,-200.4 439.3906,-197.4423 452.0801,-191.9836 463.282,-186.1773"/><ellipse fill="none" stroke="#ccc" cx="466.889" cy="-184.232" rx="4" ry="4"/></g><g id="node5" class="node"><title>mmm</title><text text-anchor="middle" x="180.985" y="-94.8"  font-size="12" fill="#333">Subject:</text><text text-anchor="middle" x="180.985" y="-80.4"  font-size="12" fill="#333">Mean, Median, Mode</text></g><g id="edge4" class="edge"><title>central-&gt;mmm</title><path fill="none" stroke="#ccc" d="M260.2363,-145.6295C246.9293,-136.4904 230.6686,-125.3226 216.3471,-115.4867"/><polygon fill="#ccc" stroke="#ccc" points="217.949,-112.3409 207.7243,-109.5646 213.986,-118.1111 217.949,-112.3409"/></g><g id="node6" class="node"><title>ran</title><text text-anchor="middle" x="286.985" y="-94.8"  font-size="12" fill="#333">Subject:</text><text text-anchor="middle" x="286.985" y="-80.4"  font-size="12" fill="#333">Ranges</text></g><g id="edge5" class="edge"><title>central-&gt;ran</title><path fill="none" stroke="#ccc" d="M286.9846,-145.6295C286.9846,-137.7836 286.9846,-128.4426 286.9846,-119.7328"/><polygon fill="#ccc" stroke="#ccc" points="290.4847,-119.5646 286.9846,-109.5646 283.4847,-119.5647 290.4847,-119.5646"/></g><g id="node7" class="node"><title>dist</title><text text-anchor="middle" x="371.985" y="-94.8"  font-size="12" fill="#333">Subject:</text><text text-anchor="middle" x="371.985" y="-80.4"  font-size="12" fill="#333">Distributions</text></g><g id="edge6" class="edge"><title>central-&gt;dist</title><path fill="none" stroke="#ccc" d="M308.4337,-145.6295C318.8024,-136.749 331.4075,-125.9531 342.6492,-116.3249"/><polygon fill="#ccc" stroke="#ccc" points="345.224,-118.7279 350.5424,-109.5646 340.6705,-113.4114 345.224,-118.7279"/></g><g id="edge11" class="edge"><title>hist-&gt;std</title><path fill="none" stroke="#ccc" stroke-dasharray="1,5" d="M426.844,-164C429.9379,-164 433.0318,-164 436.1257,-164"/><ellipse fill="none" stroke="#ccc" cx="440.315" cy="-164" rx="4" ry="4"/></g><g id="edge12" class="edge"><title>mmm-&gt;ran</title><path fill="none" stroke="#ccc" stroke-dasharray="1,5" d="M241.0237,-91.2C244.2964,-91.2 247.5692,-91.2 250.842,-91.2"/><ellipse fill="none" stroke="#ccc" cx="254.977" cy="-91.2" rx="4" ry="4"/></g><g id="edge13" class="edge"><title>mmm-&gt;dist</title><path fill="none" stroke="#ccc" stroke-dasharray="1,5" d="M212.1228,-109.5468C225.9759,-116.687 242.7909,-124.0074 258.9846,-127.6 283.2827,-132.9905 291.0938,-134.5776 314.9846,-127.6 324.6703,-124.7712 334.2765,-119.7397 342.7651,-114.3031"/><ellipse fill="none" stroke="#ccc" cx="346.295" cy="-111.919" rx="4" ry="4"/></g><g id="node8" class="node"><title>vid</title><text text-anchor="middle" x="59.985" y="-22"  font-size="12" fill="#333">Video Card:</text><text text-anchor="middle" x="59.985" y="-7.6"  font-size="12" fill="#333">Mean, Median, Mode</text></g><g id="edge7" class="edge"><title>mmm-&gt;vid</title><path fill="none" stroke="#ccc" d="M150.4512,-72.8295C134.9745,-63.5179 115.9977,-52.1004 99.4283,-42.1314"/><polygon fill="#ccc" stroke="#ccc" points="100.8813,-38.921 90.5082,-36.7646 97.2725,-44.9191 100.8813,-38.921"/></g><g id="node9" class="node"><title>choice</title><text text-anchor="middle" x="180.985" y="-22"  font-size="12" fill="#333">Choice Card:</text><text text-anchor="middle" x="180.985" y="-7.6"  font-size="12" fill="#333">Find the Mean</text></g><g id="edge8" class="edge"><title>mmm-&gt;choice</title><path fill="none" stroke="#ccc" d="M180.9846,-72.8295C180.9846,-64.9836 180.9846,-55.6426 180.9846,-46.9328"/><polygon fill="#ccc" stroke="#ccc" points="184.4847,-46.7646 180.9846,-36.7646 177.4847,-46.7647 184.4847,-46.7646"/></g><g id="node10" class="node"><title>embed</title><text text-anchor="middle" x="288.985" y="-22"  font-size="12" fill="#333">Embed Card:</text><text text-anchor="middle" x="288.985" y="-7.6"  font-size="12" fill="#333">Select the Mean</text></g><g id="edge9" class="edge"><title>mmm-&gt;embed</title><path fill="none" stroke="#ccc" d="M208.2376,-72.8295C221.9235,-63.6041 238.6761,-52.3117 253.3673,-42.4087"/><polygon fill="#ccc" stroke="#ccc" points="255.4046,-45.2564 261.7404,-36.7646 251.492,-39.4519 255.4046,-45.2564"/></g><g id="edge14" class="edge"><title>ran-&gt;dist</title><path fill="none" stroke="#ccc" stroke-dasharray="1,5" d="M314.8752,-91.2C318.1285,-91.2 321.3818,-91.2 324.6351,-91.2"/><ellipse fill="none" stroke="#ccc" cx="328.722" cy="-91.2" rx="4" ry="4"/></g></g></svg>

For more details and examples, [check out this 3-minute overview video](https://youtu.be/Gi99QbiSuWs).

## Card Requirements

- A card must have a name.
- A card must belong to a single subject.
- A card must belong to a single subject of the same language.
- ~~A card can have before and after cards (prerequisites). These cannot form a cycle.~~
- Each card kind has its own requirements.
- For more card kinds, see [Card Kinds](/card-kinds).

## Subject Requirements

- A subject must have a name.
- A subject must have a written goal.
- A subject's goal can be anywhere from narrow to broad.
- Subjects may only contain cards and subjects of the same language.
- A subject may have a single parent.
- A subject may have many children
- A subject can have before and after subjects (prerequisites). These cannot form a cycle.

What's next? [Continue to "Want to Help?"](/want-to-help).
