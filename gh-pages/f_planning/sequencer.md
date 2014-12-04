---
title: Sequencer
layout: default
---

This document covers the terms, parameters, flow, and formula for the primary learning engine of Sagefy.

Terms
-----

Also see [data structure](/data_structure) for definitions of **card**, **unit**, and **set**.

**Sequencer** - Determines the optimal ordering of cards, units, or other activity to present to the learner.

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
- _Formula_ - ??? (Basically, IRT.)

**Learner-Unit Ability [!!!]**

- _Definition_ - How likely is the learner to respond well to a typical card within the unit?
- _When_ - Diagnostic assessment. When to change units. When unit is complete. When to review. Forming completion tree.
- _Factors_ - Prior, response, learner-card ability, card difficulty, guess, slip. (Retention: should degrade learner-unit ability's confidence over time.)
- _Formula_ - ??? (Basically, BKT.)

**Learner-Set Ability**

- _Definition_ - How well does the learner know the set?
- _When_ - Searching for sets. Time to complete estimates.
- _Factors_ - Learner-unit ability.
- _Formula_ - sum(learner-unit ability) / count(units)  [V2: Use probability distribution]

**Card Quality**

- _Definition_ - How much is the card is likely to improve the typical learner's ability?
- _When_ - Selecting the next card.
- _Factors_ - Prior, learner-unit ability, unit learning curve (difficulty), time.
- _Formula_ - ??? (Look for significant changes in the learning acceleration.)

**Unit Quality**

- _Definition_ - How likely is the typical learner to gain significant ability within this unit?
- _When_ - Computing set quality.
- _Factors_ - Learner-unit ability.
- _Formula_ - sum(learner-unit ability per learner) / count(learners engaged)  [V2: Use probability distribution]

**Set Quality**

- _Definition_ - How likely is the typical learner to gain significant ability within this set?
- _When_ - Searching for a sets.
- _Factors_ - Unit quality.
- _Formula_ - sum(unit quality per unit) / count(units)  [V2: Use probability distribution]

**Card Difficulty**

- _Definition_ - How likely is the typical learner to answer well? (Only applies to assessment cards.)
- _When_ - Computing learner-unit ability. Selecting the next card.
- _Factors_ - Prior, response, learner-unit ability, guess, slip.
- _Formula_ - ??? (A simple method would be a percentage of good answers.)

**Card Guess**

- _Definition_ -  How likely is the typical learner, without ability, to randomly guess towards a good answer? (Only applies to assessment cards.)
- _When_ - ???
- _Factors_ - Prior, learner-unit ability, response, history of incorrects.
- _Formula_ - ??? (Contextual... one right answer in many wrongs is likely a guess.)

**Card Slip**

- _Definition_ - How likely is the typical learner, with ability, to answer poorly? (Only applies to assessment cards.)
- _When_ - ???
- _Factors_ - Prior, learner-unit-ability, response, history of corrects.
- _Formula_ - ??? (Contextual... one wrong answer in many rights is likely a slip.)

**Unit Difficulty**

- _Definition_ - How difficult is it for a typical learner to gain proficiency? A function of time.
- _When_ - Time to complete estimates.
- _Factors_ - Prior, time, learning/forgetting curve.
- _Formula_ - ??? (Should reflect a learning curve.)

**Set Difficulty**

- _Definition_ - How difficult is it for a typical learner to gain proficiency?
- _When_ - Time to complete estimates.
- _Factors_ - Unit difficulty.
- _Formula_ - sum(unit difficulty per unit)  [V2: Use probability distribution]

Flow
----

![Flowchart](https://docs.google.com/drawings/d/1fmdT0vqWPsq-oUG0IPRprckGw8wn9_QmO9tCe63yS80/pub?w=850&h=699)

### Set Selection

I come to the site, I sign in. Brings me to empty list of sets. Links to search sets.

I search sets. I see ordering of sets matching, estimates for difficulty (or time). I can click to see a map of the units involved in a tree diagram.

I click one and add it to my sets. It will appear on my list of sets, along with my overall completion percent. A link to the tree diagram is present. I will see if I need to continue or review any particular set.

### Menu

I can open the diagram at any time from the menu. In the diagram, the current unit is highlighted. The menu also has a discussion link, and a link to return to the list of sets. The discussion link can go up the chain; I can discuss the card, unit, and sets from within a card.

### Diagnosis

I click to go into the set. First I see the diagram of the units.

The page says I will take a diagnostic assessment. It estimates how long it will take to complete the diagnostic assessment. It says it will start with the hardest questions first and work back.

I start the diagnostic assessment. The system picks a unit near the end of the set.

The questions are all synchronous assessment. The system continues to ask me questions from the last units in the set until it is confident in its finding. For any units I am at less than proficient ability, it diagnoses the required units. Required units do not have to be explicitly defined in the set, just within other units. The system shows my progress on screen towards completing the diagnostic assessment. If I leave, I can come back later and finish the assessment. If I've already completed units previously, it will use those ratings. Questions do not present feedback in diagnostic assessment.

When there are no units left with requires below proficiency, the diagnostic assessment ends. Again I see the tree within the metrics for each unit.

### Learning

It starts from the furthest branches. I first choose which unit to start with. It emphasizes one of the units by default. It shows the learning objective and estimated difficulty (time) for each unit.

I practice with the unit. I can see my progress on the unit at the bottom of the screen. I receive feedback on questions with assessment.

If I have low ability, the system will add more high quality non-assessment cards, like videos. It also uses assessment cards that I am highly likely to answer correctly. If I have moderate ability, the system focuses on medium likelihood cards. Non-assessment cards are shown if I get multiple answers incorrect. If I have high ability, the system focuses on lower likelihood cards. The system prefers to follow require chains in sequence for cards. If I gain significantly or reach proficient ability, the system recommends I switch to a different unit.

The set is complete when all cards have proficient ability with confidence. I'm encouraged to find a new set.

### Retention

The system will monitor the last time I interacted with the units in the set. Using spaced repetition, it reminds me when I should review the units. The more time since the last review, the greater it will impact my ability score. The more time since the last review, the confidence will decrease.
