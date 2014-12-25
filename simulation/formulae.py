"""
This document does ...
"""

from math import exp


init_learned = 0.4
max_learned = 0.99
init_belief = 0.5
max_belief = 0.95
init_guess = 0.2
max_guess = 0.4
init_slip = 0.05
max_slip = 0.2
init_transit = 0.05
belief_k = 0.00001  # The factor that alters the impact of time on belief
# TODO: What should `belief_k` be?


def update(score, time,
           learned, belief, guess, slip, transit,
           prev_time, prev_learned, prev_transit):
    """
    Given a learner and a card, update both statistics.

    Input:

    - Score - What what the score (0 - wrong or 1 - correct)?
    - Time - When did the score come in (in seconds)?
    - Learned [Learner] - Before seeing the response, how likely did we already
        believe the learner knew the skill?
    - Belief [Learner] - How confident were we in the prior `learned`?
    - Guess [Card] - Before the response, how likely would a learner who
        didn't know the skill still get the right answer?
    - Slip [Card] - Before the response, how likely woud a learner who
        did know the skill still get a wrong answer?
    - Transit [Card] - Before seeing the data,
        how likely did we think the learner would learn the skill by seeing
        the card?
    - Prev Time [Previous Card] - When was the last time we saw
        a learner response for this skill?
    - Prev Learned [2 Prior, Learner] - Two cards prior, before that,
        what did we think about `learned`?
    - Prev Transit [2 Prior, Card] - Two cards prior, before that, what was the
        transit for the card?

    Output:

    - Correct - Before seeing the score, how likely was the learner
        to answer the card well?
        (doesn't update anything)
    - Belief [Learner] - Given the amount of time since the last response,
        how much confidence should we put in `learned`?
        (should be the first update)
    - Guess [Card] - If the learner doesn't know the skill, how likely are they
        to get the answer right anyways?
        (should come before learned)
    - Slip [Card] - If the learner knows the skill,
        how likely are they to still answer incorrectly?
        (should come before learned)
    - Learned [Learner] - How likely is it that the learner knows the skill?
        (main calculation)
    - Transit [Card, 2 Prior] - Given two cards prior,
        what `learned` was then, and what `learned` is now...
        how likely is it the learner learned the skill as the result
        of seeing that card?
        (after learned)
    """

    # Note: The ordering must be as follows...
    correct = compute_correct(learned, guess, slip)
    # TODO belief = compute_belief(prev_time, time, learned, belief)
    guess = compute_guess(score, learned, guess)
    slip = compute_slip(score, learned, slip)
    learned = compute_learned(score, learned, guess, slip, transit)
    # TODO prev_transit = compute_transit(prev_transit, prev_learned, learned)

    return {
        'correct': correct,
        'learned': learned,
        'belief': learned,  # TODO belief,
        'guess': guess,
        'slip': slip,
        'prev_transit': prev_transit,
    }


def compute_correct(learned=init_learned, guess=init_guess, slip=init_slip):
    """
    Determines how likely the learner will respond to a card well.
    """
    return learned * (1 - slip) + (1 - learned) * guess


def compute_belief(prev_time, time, learned=init_learned, belief=init_belief):
    """
    Determines how likely we believe in `learned`, given the time since the
    last response.
    Note: Intentionally `prev_time - time`, as this produces a negative number.
    TODO: Adjust.
    """
    # strength = 2 * learned * belief / (learned + belief)
    # return exp(belief_k * (prev_time - time) / strength)
    return exp(belief_k * (prev_time - time) / learned)


def compute_guess(score, learned=init_learned, guess=init_guess):
    """
    Determines how to update guess, given a score.
    Based on the following observation:
    - P(Answer is a Guess | Correct) = 1 - P(Learned)

    TODO: Adjust.
    TODO: Alternatively, make use of `belief`.
    """
    guess += score * ((max_guess - guess) * (1 - learned)) ** 2
    guess -= (1 - score) * (guess * (1 - learned)) ** 2
    return guess


def compute_slip(score, learned=init_learned, slip=init_slip):
    """
    Determines how to update slip, given a score.
    Based on the following observation:
    - P(Answer is a Slip | Incorrect) = P(Learned)

    TODO: Alternatively, make use of `belief`.
    TODO: Adjust.
    """
    slip -= score * (slip * learned) ** 2
    slip += (1 - score) * ((max_slip - slip) * learned) ** 2
    return slip


def compute_learned(score, learned=init_learned, guess=init_guess,
                    slip=init_slip, transit=init_transit):
    """
    Given a learner response,
    determines how likely the learner knows the skill.
    TODO: Alternatively, this computation can also make use of `belief`.
    """
    positive = (learned * (1 - slip)
                / (learned * (1 - slip) + (1 - learned) * guess))
    negative = (learned * slip
                / (learned * slip + (1 - learned) * (1 - guess)))
    posterior = score * positive + (1 - score) * negative
    return posterior + (1 - posterior) * transit


def compute_transit(prev_transit, prev_learned, learned):
    """
    Determines the update to transit, given the `learned` score
    before the card, and the `learned` score after two additional cards.
    Note that transit is both on assessment and non-assessment cards.

    [prev_learned] A [...] B [...] C [learned]

    TODO: Alternatively, make use of `belief`.
    TODO: Adjust.
    """
    delta = learned / prev_learned - 1
    sign = 1 if delta > 0 else -1
    return prev_transit + sign * min((prev_transit * delta) ** 2, 0.01)
