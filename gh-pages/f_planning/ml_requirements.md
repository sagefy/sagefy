---
title: Machine Learning Requirements
layout: default
---

## Sequencer

_Determines the optimal order to present cards, units, and sets to the learner._

## Core Attributes

- Learner to Unit Efficacy
    - How well does the learner know the unit?
    - Use responses to assessment cards.
    - Measure: Bayesian Knowledge Tracing
- Card Difficulty
    - How likely is any learner to get the right (objective) or a good (subjective) answer?
    - Measure: TODO
- Card Quality
    - How much is the card is likely to improve any learner's efficacy?
    - Possibly, also consider learner retention characteristics.
    - More important on non-assessment cards.
    - Measure: TODO

## Composed Attributes

- Learner to Card Efficacy -- called `likelihood` below
    - How likely is the learner to answer well?
    - Measure: Item Response Theory
- Learner to Set Efficacy
    - How likely is the learner to know the set?
    - Composition of Learner to Unit Efficacy
- Unit Difficulty
    - How difficult is it for a typical learner to gain proficiency?
    - Translate to time
- Set Difficulty
    - Same as unit difficulty
- Unit Quality
    - TODO: What question should we ask?
- Set Quality
    - TODO: What question should we ask?
    - Value would be used by recommender system.
- Also consider learner-specific card difficulty.
- Also consider learner-specific card quality.

## Process

- Diagnosis [Knowledge Spaces] -- Determine how much the learner knows about a unit.
    - Starting at the end of the set,
      makes a guess about the learner's efficacy about each unit.
    - Any unit with a low efficacy, then assess the prerequisite efficacy
- Primary
    - Low (0-65%): Focus on high quality non-assessment cards,
        mixed in with high (60-80%) likelihood cards.
        - If a learner makes a significant gain, move to another unit.
    - Mid (65-85%): Focus on middle likelihood (50%) cards of at least moderate quality.
        - If there is a decline in efficacy, intervene with a non-assessment card.
        - If a learner makes a significant gain, move to another unit.
    - High (85%+): Focus on mid-to-low likelihood (30-50%)
    - What levels are low, mid, and high? What confidence to assert?
    - Prefer to follow card prerequisite chains.
    - Account for card prerequisites.
    - Require 85% as a prerequisite.
- Review [Spaced Learning]
    - Given an learner to unit efficacy, how long is the learner likely to retain the information?
    - Determine intervals (time) for review per unit.
    - More time will impact efficacy more greatly.

## Other Applications

- Recommend new units to the learner.
- Filter spam and low quality content.
- Mark down low quality discussion.
- Matching up learners with other learners and mentors.
- Alter cards based on size of group (single, two, three...)
- Features: tags, kinds and formats, other learner performance, etc.
- Deal with asynchronous assessment
- Determine when the learner should take a break.
- Given unit difficulties, determine time to complete a set.
- Assess validity of cards, units, and sets.
