---
layout: docs
title: Planning> Sequencer
---

<script
src="//cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML">
</script>

This document covers the terms, parameters, flow, and formula for the primary learning engine of Sagefy.

Also see [Planning: Sequencer Background](Planning-Sequencer-Background) and [Planning: Sequencer Guess Slip](Planning-Sequencer-Guess-Slip).

Terms
-----

Also see [Data Structure](Data-Structure) for definitions of **card**, **unit**, and **subject**.

**Sequencer** - Determines the optimal ordering of cards, units, or other activity to present to the learner.

**Ability** - Refers to the learner's ability towards a particular card, unit, or subject.

**Quality** - Refers to the ability of the card, unit, or subject to improve the learner's ability.

**Difficulty** - Refers to how likely either the specific learner or the general learner to respond well.

**Scored Cards** - Cards which have an response element, such as choosing an answer or typing in an answer.

Requirements
------------

I write these requirements with the assumption of using Bayesian Knowledge Tracing. In BKT, the following formulas are assumed:

  correct = learned * (1 - slip) + (1 - learned) * guess
  incorrect = learned * slip + (1 - learned) * (1 - guess)

  learned0 = (
    score
    * learned
    * calc_correct(1, guess, slip)
    / calc_correct(learned, guess, slip)
    + (1 - score)
    * learned
    * calc_incorrect(1, guess, slip)
    / calc_incorrect(learned, guess, slip)
  )
  learned = learned0 + (1 - learned0) * transit

- correct: the probability of the learner getting the answer correct
- incorrect: the probability of the learner getting the answer incorrect
- learned: the probability that the learner knows the skill
- guess: the probability the learner will answer correctly given learned == 0
- slip: the probability the learner will answer incorrectly given learned == 1
- learned0: learned before accounting for transit (Hidden Markov Model)
- transit: the probability the learner has learned the skill by seeing the card

Requirements:

- `guess`, `slip`, and `transit` should be **unique** to each card (item), not to each skill (unit). We need to be able to choose cards that suit the learner's current `learned` for the skill. We also need to be able to monitor high quality v low quality cards.
- `guess`, `slip`, and `transit` should update **per response**. We will be much more capable of scaling out if we can avoid having to do any large all-at-once type of calculations.
  - `guess` should increase with correct answers and decrease with incorrect answers, proportional to `1 - learned`.
  - `slip` should increase with incorrect answers and decrease with correct answers, proportional to `learned`.
  - `transit` should increase if the following card gets a correct answer, and decrease if the following card gets an incorrect answer. `transit` should be based on `learned` and `correct`.
- The model for estimating `guess`, `slip`, and `transit` should beat static guesses (such as 0.3, 0.1, and 0.05). We want to ensure the model produces real results.
- We need to know a way of letting the user know, based on what `learned` was and how much time has passed, when the learner should review the unit. We can call this parameter `belief`.
- `learned` should be able to account for time. If a learner doesn't answer in a long time, our prediction of `learned` should go down.
- We'll want to avoid having to look at previous responses and statistics too much, as it would cost in terms of database queries. Preferably, all the results of calculation should be stored in a key-value store and not in the main database.
- We need aggregates to help learners with:
  1. Searching for new subjects
  2. Estimating time to complete units and subjects

Parameters
----------

The formulas given below are based on the _Bayesian update_ (`guess`, `slip`) and _weighted mean_ (`transit`) strategy. Other strategies may include _static parameters_ and _Bayesian updates_.

**Learner-Card Ability** - $$p(correct)$$

- _Definition_ - How likely is the learner to respond to the given card well? (Only applies to scored cards.)
- _When_ - Selecting the next card. Assessing Learner-Unit Ability.
- _Factors_ - Learner-unit ability, card difficulty, guess, slip.
- _Formula_ - `learned * (1 - slip) + (1 - learned) * guess`

**Learner-Unit Ability** - $$p(learned)$$ with $$p(belief)$$

- _Definition_ - How likely is the learner to respond well to a typical card within the unit?
- _When_ - Diagnostic assessment. When to change units. When unit is complete. When to review. Forming completion tree.
- _Factors_ - Prior, response, learner-card ability, card difficulty, guess, slip. (Retention: should degrade learner-unit ability's confidence over time.)
- _Formula_ -
  - 1) `learned = learned * (slip || 1 - slip) / (p(correct) || p(incorrect))`
  - 2) `learned = learned + (1 - learned) * transit`

**Learner-Subject Ability**

- _Definition_ - How well does the learner know the subject?
- _When_ - Searching for subjects. Time to complete estimates.
- _Factors_ - Learner-unit ability.
- _Formula_ - `sum(learner-unit ability) / count(units)`

**Card Quality** - $$p(transit)$$

- _Definition_ - How much is the card is likely to improve the typical learner's ability?
- _When_ - Selecting the next card.
- _Factors_ - Prior, learner-unit ability, unit learning curve (difficulty), time.
- _Formula_ - `transit = (weight * transit + instance-transit) / (weight + instance-weight)`

**Unit Quality**

- _Definition_ - How likely is the typical learner to gain significant ability within this unit?
- _When_ - Computing subject quality.
- _Factors_ - Learner-unit ability.
- _Formula_ - `mean_learner_unit_ability * (num_learners / (num_learners + min_learners))` where mean_learner_unit_ability is the average of ability of all learners who have participated with the unit

**Subject Quality**

- _Definition_ - How likely is the typical learner to gain significant ability within this subject?
- _When_ - Searching for a subjects.
- _Factors_ - Unit quality.
- _Formula_ - `sum(unit quality per unit) / count(units)` mean of the units contained.

**Card Difficulty** - $$p(guess)$$ and $$p(slip)$$

- _Definition_ - How likely is the typical learner to answer well? (Only applies to scored cards.)
  - **Guess** - How likely is the typical learner, without ability, to randomly guess towards a good answer? (Only applies to scored cards.)
  - **Slip** - How likely is the typical learner, with ability, to answer poorly? (Only applies to scored cards.)
- _When_ - Computing learner-unit ability. Selecting the next card.
- _Factors_ - Prior, response, learner-unit ability, guess, slip.
- _Formula_ -
  - Guess and Slip both use a PMF. The hypotheses are 0 to 1 with a step of 0.01. Each update, we update each hypothesis by `prior * likelihood`, then we normalize the PMF so its probabilities to 1.
  - `guess[hypothesis] = prior * (score * correct(learned, hypothesis, slip) + (1 - score) * incorrect(learned, hypothesis, slip))`
  - `slip[hypothesis] = prior * (score * correct(learned, guess, hypothesis) + (1 - score) * incorrect(learned, guess, hypothesis))`
  - `difficulty = 0.5 * guess + 0.5 * (1 - slip)`

**Unit Difficulty**

- _Definition_ - How many cards does it take for a learner to typically get to learned state?
- _When_ - Time to complete estimates.
- _Factors_ - Responses, learned.
- _Formula_ - When the learner first hits 99% p(learned), how many cards has the learner done so far? Take the average.

**Subject Difficulty**

- _Definition_ - How difficult is it for a typical learner to gain proficiency?
- _When_ - Time to complete estimates.
- _Factors_ - Unit difficulty.
- _Formula_ - `sum(unit difficulty per unit)`

Flow
----

![Flowchart](https://docs.google.com/drawings/d/1fmdT0vqWPsq-oUG0IPRprckGw8wn9_QmO9tCe63yS80/pub?w=850&h=699)

![Endpoint Flowchart](/f_planning/sequencer_endpoints.png)

### Subject Selection

I come to the site, I sign in. Brings me to empty list of subjects. Links to search subjects.

I search subjects. I see ordering of subjects matching, estimates for difficulty (or time). I can click to see a map of the units involved in a tree diagram.

I click one and add it to my subjects. It will appear on my list of subjects, along with my overall completion percent. A link to the tree diagram is present. I will see if I need to continue or review any particular subject.

### Menu

I can open the diagram at any time from the menu. In the diagram, the current unit is highlighted. The menu also has a discussion link, and a link to return to the list of subjects. The discussion link can go up the chain; I can discuss the card, unit, and subjects from within a card.

### Diagnosis

I click to go into the subject. First I see the diagram of the units.

The page says I will take a diagnostic assessment. It estimates how long it will take to complete the diagnostic assessment. It says it will start with the hardest questions first and work back.

I start the diagnostic assessment. The system picks a unit near the end of the subject.

The questions are all immediately scored. The system continues to ask me questions from the last units in the subject until it is confident in its finding. For any units I am at less than proficient ability, it diagnoses the required units. Required units do not have to be explicitly defined in the subject, just within other units. The system shows my progress on screen towards completing the diagnostic assessment. If I leave, I can come back later and finish the assessment. If I've already completed units previously, it will use those ratings. Questions do not present feedback in diagnostic assessment.

When there are no units left with requires below proficiency, the diagnostic assessment ends. Again I see the tree within the metrics for each unit.

### Learning

It starts from the furthest branches. I first choose which unit to start with. It emphasizes one of the units by default. It shows the learning objective and estimated difficulty (time) for each unit.

I practice with the unit. I can see my progress on the unit at the bottom of the screen. I receive feedback on scored questions.

If I have low ability, the system will add more high quality unscored cards, like videos. It also uses scored cards that I am highly likely to answer correctly. If I have moderate ability, the system focuses on medium likelihood cards. Unscored cards are shown if I get multiple answers incorrect. If I have high ability, the system focuses on lower likelihood cards. The system prefers to follow require chains in sequence for cards. If I gain significantly or reach proficient ability, the system recommends I switch to a different unit.

The subject is complete when all cards have proficient ability with confidence. I'm encouraged to find a new subject.

### Retention

The system will monitor the last time I interacted with the units in the subject. Using spaced repetition, it reminds me when I should review the units. The more time since the last review, the greater it will impact my ability score. The more time since the last review, the confidence will decrease.

Graph Traversal
---------------

We collect the subject of units that the learner will be participating in. We will need to diagnose any units which have either never been seen by the learner. We will also need to diagnose any units that have been viewed, but we are no longer confident in the ability score due to time.

The following is an example of this process, known as a graph traversal.

<img src="https://docs.google.com/drawings/d/12mrz9ZmpfGYQLmELoaJVg3ft5fj0cNRzcVJ7E9hEFH0/pub?w=714&amp;h=745">

The algorithm makes use of depth first search. We start near the end of the tree, and walk our way down as we diagnose. We record each node in one of three lists: Diagnose, Ready, and Learned.

First, we start at node "A". We diagnose an L (low score). Because it is a low score, we will continue to traverse the tree. "A" is appended to list Diagnose.

Next, we will continue to node "C". This is because we have higher confidence in "C" than "B". "C" is already diagnosed. "C" is appended to list Ready. We note that "C" has one dependency, "A".

Third, we continue to node "F" (depth-first search). We are confident that the learner knows node "F", and therefore we start on the other side of the chain. "F" is appended to Learned. Although "I" is required by "F", because we are confident in high ability for "F", "I" will never be diagnosed.

Because "C" has no other requires, we go back to "B". We find it is a low ability. Append to Ready, 1 dependent: A.

We know more about "E" than "D", so we continue to "E". We find "E" is a low ability. Append to Ready, 2 dependents: A and B.

We already know "G", so it is appended to Learned.

We diagnose "H", and find it is low ability. Append to Ready, 3 dependents: "A", "B", and "E". If "F" had not been learned, unit "H" would have 4 dependencies instead of 3.  The algorithm considers how many nodes _depend_ on the given node, rather than how deep in the graph the node is.

Finally, we diagnose node "D" with low ability. Append to Ready, and there are 2 dependents: "A" and "B".

<img src="https://docs.google.com/drawings/d/1oN1fy2vK_LVBE4ZZY3-ycQD286-dj4reHW8NbtB5rVA/pub?w=714&amp;h=745">

We also have the following lists:

  Diagnose: []
  Ready: [A, C, B, E, H, D]
  Learned: [F, G]

We are now ready to starting the learning process.

The following is overly simplistic; most learners will not 'learn' a unit in their first attempt at it. If at any time the unit composition changes, when we come back to the tree, we will need to diagnose any new units. Additionally, as it will be spaced out, learners will need to have some units reviewed intermittently to keep the confidence scores up.

In the ready list, A, B, and E have requires, so those are not options to the learner yet. The available ready nodes are C, D, and H.

"H" has the most dependents, so that would be recommended as the starting place for the learner. Let's say, however, the learner choose to learn unit "D" first.

Now the remaining subject is C and H. The learner chooses H. So now the remaining subject is E and C. Let's say the learner chooses C.

Now, the only option remaining is E. After E, the learner would do B, then A.
