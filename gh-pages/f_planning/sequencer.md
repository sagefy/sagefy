---
title: Sequencer
layout: default
---

This document covers the terms, parameters, flow, and formula for the primary learning engine of Sagefy.

Terms
-----

**Sequencer** - Determines the optimal ordering of cards, units, or other activity to present to the learner.

Also see [data structure](/data_structure).

**Ability** - Refers to the learner's ability towards a particular card, unit, or set.

**Quality** - Refers to the ability of the card, unit, or set to improve the learner's ability.

**Difficulty** - Refers to how likely either the specific learner or the general learner to respond well.

**Assessment Cards** - Cards which have an assessment element, such as choosing an answer or typing in an answer.

Parameters
----------

All parameters have a best-guess (a.k.a. mean, mu) and a confidence in that prediction (a.k.a. deviation, sigma).

**Learner-Card Ability** 

- _Definition_ - How likely is the learner to respond to the given card well? (Only applies to assessment cards.)
- _When_ - Selecting the next card. Assessing Learner-Unit Ability.
- _Factors_ - Learner-unit ability, card difficulty, guess, slip.
- _Formula_ - ???

**Learner-Unit Ability** 

- _Definition_ - How likely is the learner to respond well to a typical card within the unit?
- _When_ - **Primary parameter**. Diagnostic assessment. When to change units. When unit is complete. When to review. Forming completion tree.
- _Factors_ - Prior, response, learner-card ability, guess, slip.
- _Formula_ - ???

**Learner-Set Ability** 

- _Definition_ - How well does the learner know the set? Measured as the average of the unit efficacies for the units defined as part of the set.
- _When_ - Searching for sets. Time to complete estimates.
- _Factors_ - Learner-unit ability.
- _Formula_ - ???

**Card Quality** 

- _Definition_ - How much is the card is likely to improve the typical learner's ability?
- _When_ - Selecting the next card.
- _Factors_ - ???
- _Formula_ - ???

**Unit Quality** 

- _Definition_ - How likely is the typical learner to gain significant ability within this unit?
- _When_ - Computing set quality.
- _Factors_ - ???
- _Formula_ - ???

**Set Quality** 

- _Definition_ - How likely is the typical learner to gain significant ability within this set? Measured as the average of the unit qualities for units defined as part of the set.
- _When_ - Searching for a sets.
- _Factors_ - ???
- _Formula_ - ???

**Card Difficulty** 

- _Definition_ - How likely is the typical learner to answer well? (Only applies to assessment cards.)
- _When_ - Computing learner-unit ability. Selecting the next card.
- _Factors_ - Learner-unit ability, guess, slip.
- _Formula_ - ???

**Unit Difficulty** 

- _Definition_ - How difficult is it for a typical learner to gain proficiency? A function of time.
- _When_ - Time to complete estimates.
- _Factors_ - ???
- _Formula_ - ???

**Set Difficulty** 

- _Definition_ - How difficult is it for a typical learner to gain proficiency? A function of time. Measured as the sum of unit difficulty for units defined as part of the set.
- _When_ - Time to complete estimates.
- _Factors_ - ???
- _Formula_ - ???

Flow
----

---------------

Previous
---------

### Process

- Diagnosis [Knowledge Spaces] -- Determine how much the learner knows about a unit.
    - Starting at the end of the set,
      makes a guess about the learner's ability about each unit.
    - Any unit with a low ability, then assess the prerequisite ability
- Primary
    - Low (0-65%): Focus on high quality non-assessment cards,
        mixed in with high (60-80%) likelihood cards.
        - If a learner makes a significant gain, move to another unit.
    - Mid (65-85%): Focus on middle likelihood (50%) cards of at least moderate quality.
        - If there is a decline in ability, intervene with a non-assessment card.
        - If a learner makes a significant gain, move to another unit.
    - High (85%+): Focus on mid-to-low likelihood (30-50%)
    - What levels are low, mid, and high? What confidence to assert?
    - Prefer to follow card prerequisite chains in a sequence.
    - Account for card prerequisites.
    - Require 85% as a prerequisite.
- Review [Spaced Learning]
    - Given an learner to unit ability, how long is the learner likely to retain the information?
    - Determine intervals (time) for review per unit.
    - More time will impact ability more greatly.

Story Mode

### Set Selection

I come to the site, I sign in.

Dashboard is empty. Links to search sets.

I search sets for "American Sign Language". I see ordering of sets matching, estimates for difficulty (or time). I can click to see a map of the units involved in a tree diagram.

I click one and add it to my sets. It will appear on my dashboard, along with my overall completion percent. A link to the tree diagram is present. I will see if I need to continue or review any particular set.

I click to go into the set. First I see the diagram of the units. I can open the diagram at any time from the menu. In the diagram, the current unit is highlighted. The menu also has a discussion link, and a link to return to the dashboard. The discussion link can go up the chain; I can discuss the card, unit, and sets from within a card.

### Diagnostic Assessment

The page says I will take a diagnostic assessment. It estimates how long it will take to complete the diagnostic assessment. It says it will start with the hardest questions first and work back.

I start the diagnostic assessment. The system picks a unit near the end of the set. It asks me a difficult question.

The questions are all synchronous assessment. The system continues to ask me questions from the last units in the set until it is 75% confident in its finding. For any units I am at less than 85% ability, it diagnoses the prerequisite unit. Prerequisite units do not have to be explicitly defined in the set, just within other units. The system shows my progress on screen towards completing the diagnostic assessment. If I leave, I can come back later and finish the assessment. If I've already completed units previously, it will use those ratings. Questions do not present feedback in diagnostic assessment.

When there are no units left with prerequisites and below 85%, the diagnostic assessment ends. Again I see the tree within the metrics for each unit.

### Main Loop

Now if I continue or return to the set, I am in the primary learning loop.

It starts from the furthest branches. I first choose which unit to start with. It emphasizes one of the units by default. It shows the learning objective and estimated difficulty (time) for each unit.

I practice with the unit. I can see my progress on the unit at the bottom of the screen. I receive feedback on questions with assessment.

If I have low ability, the system will add more high quality non-assessment cards, like videos. It also uses assessment cards that I am highly likely to answer correctly (60-80%).

If I have moderate ability, the system focuses on medium likelihood cards (50%). Non-assessment cards are shown if I get multiple answers incorrect.

If I have high ability, the system focuses on lower likelihood cards.

If I gain more than 20% or reach 85% ability, the system recommends I switch to a different unit.

The set is complete when all cards have 85% ability and confidence.

At the end of the set, I'm encouraged to find a new set.

### Review

The system will monitor the last time I interacted with the units in the set. Using spaced repetition, it reminds me when I should review the units. The more time since the last review, the greater it will impact my ability score. The more time since the last review, the confidence will decrease.
