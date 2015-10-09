"""
This document contains the formulas for Sagefy's adaptive learning algorithm.
"""

from math import exp
from modules.sequencer.params import init_transit, belief_factor


def update(score, time_delta, learned,
           guess_distribution, slip_distribution):
    """
    Given a learner and a card, update both statistics.

    Input:

    - Score - What what the score (0 - wrong or 1 - correct)?
    - Time - When did the score come in (in seconds)?
    - Prev Time [Previous Card] - When was the last time we saw
        a learner response for this skill?
    - * * *
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
        (scale before guess, slip, transit, update after)
    - Transit [Card (Prior)] - How likely is it the learner
        learned the skill as the result of seeing that card?
        (after learned)
    """

    guess = guess_distribution.get_value()
    slip = slip_distribution.get_value()
    transit = init_transit

    learned2 = update_learned(score, learned,
                              guess, slip, transit,
                              time_delta)
    guess_distribution.update({
        'score': score,
        'learned': learned,
        'guess': guess,
        'slip': slip,
    })
    slip_distribution.update({
        'score': score,
        'learned': learned,
        'guess': guess,
        'slip': slip,
    })

    return {
        'learned': learned2,
        'guess_distribution': guess_distribution,
        'slip_distribution': slip_distribution,
    }


def calculate_correct(guess, slip, learned):
    """
    Determines how likely the learner will respond to a card well.
    """

    return learned * (1 - slip) + (1 - learned) * guess


def calculate_incorrect(guess, slip, learned):
    """
    Determines how likely the learner will respond to a card not well.
    """

    return learned * slip + (1 - learned) * (1 - guess)


def calculate_difficulty(guess, slip):
    """
    How hard is this card for the typical learner?
    """

    # If guess + slip is greater than 1, then we have a degenerate card...
    # where the right answer lowers learned, and the wrong answer increases it
    if guess + slip > 1:
        return float("inf")
    return calculate_correct(guess, slip, 0.5)


def calculate_belief(learned, time_delta):
    """
    How much should we believe in learned, given the amount of time that
    has passed?
    """

    return exp(-1 * time_delta * (1 - learned) / belief_factor)


def update_learned(score, learned, guess, slip, transit,
                   time_delta):
    """
    Given a learner response,
    determines how likely the learner knows the skill.
    """

    learned *= calculate_belief(learned, time_delta)
    posterior = (score
                 * learned
                 * calculate_correct(guess, slip, 1)
                 / calculate_correct(guess, slip, learned)
                 + (1 - score)
                 * learned
                 * calculate_incorrect(guess, slip, 1)
                 / calculate_incorrect(guess, slip, learned))
    return posterior + (1 - posterior) * transit
