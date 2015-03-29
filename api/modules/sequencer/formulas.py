"""
This document contains the formulas for Sagefy's adaptive learning algorithm.
"""

from math import exp
from modules.sequencer.params import init_transit, belief_factor, \
    adjust_slip, adjust_guess


def update(score, time, prev_time,
           learned, guess, guess_distro, slip, slip_distro):
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
    - * * *
    - Transit [Previous Card]
    - Transit Weight [Previous Card]
    - Learned [Previous Card, before update]

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

    transit = init_transit

    correct = calculate_correct(guess, slip, learned)

    belief = calculate_belief(learned, time, prev_time)

    learned2 = update_learned(score, learned, guess, slip, transit,
                              time, prev_time)
    guess2, guess_distro = update_guess(
        score, learned, guess, slip, transit, guess_distro)
    slip2, slip_distro = update_slip(
        score, learned, guess, slip, transit, slip_distro)

    learned, guess, slip = learned2, guess2, slip2

    return {
        'correct': correct,
        'belief': belief,
        'learned': learned,
        'guess': guess,
        'guess_distro': guess_distro,
        'slip': slip,
        'slip_distro': slip_distro,
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


def update_guess(score, learned, guess, slip, transit, guess_distro):
    """
    Determines how to update guess given a score.
    """

    guess_distro.update({
        'score': score,
        'learned': learned,
        'guess': guess,
        'slip': slip,
    })
    return guess_distro.get_value() * adjust_guess, guess_distro


def update_slip(score, learned, guess, slip, transit, slip_distro):
    """
    Determines how to update slip given a score.
    """

    slip_distro.update({
        'score': score,
        'learned': learned,
        'guess': guess,
        'slip': slip,
    })
    return slip_distro.get_value() * adjust_slip, slip_distro


def calculate_belief(learned, time, prev_time):
    """
    How much should we believe in learned, given the amount of time that
    has passed?
    """

    return exp(-1 * (time - prev_time) * (1 - learned)
               / belief_factor)


def update_learned(score, learned, guess, slip, transit,
                   time, prev_time):
    """
    Given a learner response,
    determines how likely the learner knows the skill.
    """

    learned *= calculate_belief(learned, time, prev_time)
    posterior = (score
                 * learned
                 * calculate_correct(guess, slip, 1)
                 / calculate_correct(guess, slip, learned)
                 + (1 - score)
                 * learned
                 * calculate_incorrect(guess, slip, 1)
                 / calculate_incorrect(guess, slip, learned))
    return posterior + (1 - posterior) * transit
