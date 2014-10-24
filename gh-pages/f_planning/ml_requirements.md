---
title: Machine Learning Requirements
layout: default
---

Sequencer
---------

_Determines the optimal order to present cards, units, and sets to the learner._

### Core Attributes

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

### Composed Attributes

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

### Process

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
    - Prefer to follow card prerequisite chains in a sequence.
    - Account for card prerequisites.
    - Require 85% as a prerequisite.
- Review [Spaced Learning]
    - Given an learner to unit efficacy, how long is the learner likely to retain the information?
    - Determine intervals (time) for review per unit.
    - More time will impact efficacy more greatly.

Sequencer, Story Mode
---------------------

### Set Selection

I come to the site, I sign in.

Dashboard is empty. Links to search sets.

I search sets for "American Sign Language". I see ordering of sets matching, estimates for difficulty (or time). I can click to see a map of the units involved in a tree diagram.

I click one and add it to my sets. It will appear on my dashboard, along with my overall completion percent. A link to the tree diagram is present. I will see if I need to continue or review any particular set.

I click to go into the set. First I see the diagram of the units. I can open the diagram at any time from the menu. In the diagram, the current unit is highlighted. The menu also has a discussion link, and a link to return to the dashboard. The discussion link can go up the chain; I can discuss the card, unit, and sets from within a card.

### Diagnostic Assessment

The page says I will take a diagnostic assessment. It estimates how long it will take to complete the diagnostic assessment. It says it will start with the hardest questions first and work back.

I start the diagnostic assessment. The system picks a unit near the end of the set. It asks me a difficult question.

The questions are all synchronous assessment. The system continues to ask me questions from the last units in the set until it is 75% confident in its finding. For any units I am at less than 85% efficacy, it diagnoses the prerequisite unit. Prerequisite units do not have to be explicitly defined in the set, just within other units. The system shows my progress on screen towards completing the diagnostic assessment. If I leave, I can come back later and finish the assessment. If I've already completed units previously, it will use those ratings. Questions do not present feedback in diagnostic assessment.

When there are no units left with prerequisites and below 85%, the diagnostic assessment ends. Again I see the tree within the metrics for each unit.

### Main Loop

Now if I continue or return to the set, I am in the primary learning loop.

It starts from the furthest branches. I first choose which unit to start with. It emphasizes one of the units by default. It shows the learning objective and estimated difficulty (time) for each unit.

I practice with the unit. I can see my progress on the unit at the bottom of the screen. I receive feedback on questions with assessment.

If I have low efficacy, the system will add more high quality non-assessment cards, like videos. It also uses assessment cards that I am highly likely to answer correctly (60-80%).

If I have moderate efficacy, the system focuses on medium likelihood cards (50%). Non-assessment cards are shown if I get multiple answers incorrect.

If I have high efficacy, the system focuses on lower likelihood cards.

If I gain more than 20% or reach 85% efficacy, the system recommends I switch to a different unit.

The set is complete when all cards have 85% efficacy and confidence.

At the end of the set, I'm encouraged to find a new set.

### Review

The system will monitor the last time I interacted with the units in the set. Using spaced repetition, it reminds me when I should review the units. The more time since the last review, the greater it will impact my efficacy score. The more time since the last review, the confidence will decrease.

Other Applications
------------------

- Recommend new sets to the learner.
- Filter spam and low quality content.
- Mark down low quality discussion.
- Matching up learners with other learners and mentors.
- Alter cards based on size of group (single, two, three...)
- Features: tags, kinds and formats, other learner performance, etc.
- Deal with asynchronous assessment
- Determine when the learner should take a break.
- Given unit difficulties, determine time to complete a set.
- Assess validity of cards, units, and sets.

#### Side note - Six diverse sample subjects for planning examples

- Japanese Art History
- American Sign Language
- Online Broadcast Journalism
- Physical Therapy
- Classical Guitar
- Statistics
