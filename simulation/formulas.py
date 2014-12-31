"""
This document contains the formulas for Sagefy's adaptive learning algorithm.
"""

init_learned = 0.4
max_learned = 0.99
init_guess = 0.3
init_slip = 0.15
init_weight = 1
init_transit = 0.1


def update(score, time, prev_time,
           learned, guess, guess_weight, slip, slip_weight, transit):
    """
    Given a learner and a card, update both statistics.

    Input:

    - Score - What what the score (0 - wrong or 1 - correct)?
    - Time - When did the score come in (in seconds)?
    - Prev Time [Previous Card] - When was the last time we saw
        a learner response for this skill?

    - Learned [Learner] - Before seeing the response, how likely did we already
        believe the learner knew the skill?
    - Guess [Card] - Before the response, how likely would a learner who
        didn't know the skill still get the right answer?
    - Slip [Card] - Before the response, how likely woud a learner who
        did know the skill still get a wrong answer?
    - Weight [Card] - How much should we consider previous examples?
    - Transit [Card] - Before seeing the data,
        how likely did we think the learner would learn the skill by seeing
        the card?

    Output:

    - Correct - Before seeing the score, how likely was the learner
        to answer the card well?
        (doesn't update anything)
    - Learned [Learner] - How likely is it that the learner knows the skill?
        (main calculation)
    - Guess [Card] - If the learner doesn't know the skill, how likely are they
        to get the answer right anyways?
        (should come before learned)
    - Slip [Card] - If the learner knows the skill,
        how likely are they to still answer incorrectly?
        (should come before learned)
    - Weight [Card] - How much should we consider previous examples?
        (scale before guess and slip, update after)
    - Transit [Card, 2 Prior] - Given two cards prior,
        what `learned` was then, and what `learned` is now...
        how likely is it the learner learned the skill as the result
        of seeing that card?
        (after learned)
    """

    correct = calculate_correct(learned, guess, slip)

    guess, guess_weight = update_guess(score, learned, guess, guess_weight)
    slip, slip_weight = update_slip(score, learned, slip, slip_weight)

    learned = update_learned(score, learned, guess, slip, transit)

    # TODO prev_transit = update_transit(prev_transit, prev_learned, learned)

    return {
        'correct': correct,
        'learned': learned,
        'guess': guess, 'guess_weight': guess_weight,
        'slip': slip, 'slip_weight': slip_weight,
    }


def calculate_correct(learned, guess, slip):
    """
    Determines how likely the learner will respond to a card well.
    """

    return learned * (1 - slip) + (1 - learned) * guess


def update_guess(score, learned, guess, weight):
    """
    Determines how to update guess given a score.
    """

    weight = scale_weight(weight)
    guess = ((guess * weight + (1 - learned) * (1 - learned) * score)
             / (weight + (1 - learned)))
    weight = weight + (1 - learned)
    return guess, weight


def update_slip(score, learned, slip, weight):
    """
    Determines how to update slip given a score.
    """

    weight = scale_weight(weight)
    # For unknown reasons, learned^3 out performs learned^2
    slip = ((slip * weight + learned * learned * learned * (1 - score))
            / (weight + learned))
    weight = weight + learned
    return slip, weight


def scale_weight(weight):
    """
    Scales back weight so new examples have a chance to shine.
    Guess and slip use weight in calculations.
    """

    return min(weight, 25)


def update_learned(score, learned, guess, slip, transit):
    """
    Given a learner response,
    determines how likely the learner knows the skill.
    TODO: Adjust to time.
    """

    positive = (learned * (1 - slip)
                / (learned * (1 - slip) + (1 - learned) * guess))
    negative = (learned * slip
                / (learned * slip + (1 - learned) * (1 - guess)))
    posterior = score * positive + (1 - score) * negative
    return posterior + (1 - posterior) * transit


def update_transit(transit, weight,
                   prev_card_pre_learned,
                   this_card_post_learned):
    """
    Determines the update to transit, given the `learned` score
    before the card, and the `learned` score after the next cards.
    Note that transit is both on assessment and non-assessment cards.

    Input
    -----
    transit - transit of the card to be updated (the previous card)
    weight - weight of the transit of the card to be updated

    prev_card_pre_learned  (learned before the card to be updated)
    card (whose transit is updated)
    prev_card_post_learned  (learned after the card to be updated)
    card (most recently observed)
    this_card_post_learned  (learned after the most recent card)

    Output
    ------
    transit - updated transit of the previous card
    weight - updated transit weight of the previous card

    TODO Adjust to get it to work
    TODO Adjust to time
    """

    weight = max(weight, 50)
    this_transit = ((this_card_post_learned - prev_card_pre_learned)
                    * prev_card_pre_learned)
    transit = ((transit * weight + this_transit) / (weight + 1))
    weight = weight + 1
    return transit, weight
