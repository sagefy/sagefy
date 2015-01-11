"""
This document contains the formulas for Sagefy's adaptive learning algorithm.
"""

from math import exp
from pmf import PMF


init_learned = 0.4
max_learned = 0.99
init_guess = 0.3
init_slip = 0.15
init_weight = 1
max_weight = 25
init_transit = 0.1
belief_factor = 708000


class GuessPMF(PMF):
    def likelihood(self, data, hypothesis):
        score, learned, guess, slip = data['score'], data['learned'], data['guess'], data['slip']
        return (score
                * calculate_correct(hypothesis, slip, learned)
                # / calculate_correct(guess, slip, learned)
                + (1 - score)
                * calculate_incorrect(hypothesis, slip, learned)
                # / calculate_incorrect(guess, slip, learned)
                )


class SlipPMF(PMF):
    def likelihood(self, data, hypothesis):
        score, learned, guess, slip = data['score'], data['learned'], data['guess'], data['slip']
        return (score
                * calculate_correct(guess, hypothesis, learned)
                # / calculate_correct(guess, slip, learned)
                + (1 - score)
                * calculate_incorrect(guess, hypothesis, learned)
                # / calculate_incorrect(guess, slip, learned)
                )


def update(score, time, prev_time,
           learned, guess, guess_distro, slip, slip_distro, transit,
           prev_transit, prev_transit_weight, prev_card_pre_learned):
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
    - Transit [Card, 2 Prior] - Given two cards prior,
        what `learned` was then, and what `learned` is now...
        how likely is it the learner learned the skill as the result
        of seeing that card?
        (after learned)
    """

    correct = calculate_correct(guess, slip, learned)

    belief = calculate_belief(learned, time, prev_time)
    learned2 = update_learned(score, learned, guess, slip, transit,
                              time, prev_time)

    guess, guess_distro = update_guess(score, learned, guess, slip, guess_distro)
    slip, slip_distro = update_slip(score, learned, guess, slip, slip_distro)

    this_card_post_learned = learned = learned2

    prev_transit, prev_transit_weight = update_prev_transit(
        prev_transit,
        prev_transit_weight,
        prev_card_pre_learned,
        this_card_post_learned
    )

    return {
        'correct': correct,
        'belief': belief,
        'learned': learned,
        'guess': guess,
        'guess_distro': guess_distro,
        'slip': slip,
        'slip_distro': slip_distro,
        'prev_transit': prev_transit,
        'prev_transit_weight': prev_transit_weight,
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


def update_guess(score, learned, guess, slip, guess_distro):
    """
    Determines how to update guess given a score.
    """
    guess_distro.update({
        'score': score,
        'learned': learned,
        'guess': guess,
        'slip': slip,
    })
    return guess_distro.get_mode(), guess_distro


def update_slip(score, learned, guess, slip, slip_distro):
    """
    Determines how to update slip given a score.
    """
    slip_distro.update({
        'score': score,
        'learned': learned,
        'guess': guess,
        'slip': slip,
    })
    return slip_distro.get_mode(), slip_distro


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

    belief = calculate_belief(learned, time, prev_time)
    learned = learned * belief
    positive = (learned
                * calculate_correct(guess, slip, 1)
                / calculate_correct(guess, slip, learned))
    negative = (learned
                * calculate_incorrect(guess, slip, 1)
                / calculate_incorrect(guess, slip, learned))
    posterior = score * positive + (1 - score) * negative
    return posterior + (1 - posterior) * transit


def update_prev_transit(prev_transit,
                        prev_transit_weight,
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
    """

    prev_transit_weight = max(prev_transit_weight, max_weight)
    # Should `this_transit` be weighted by learned?
    this_transit = this_card_post_learned - prev_card_pre_learned
    prev_transit = ((prev_transit * prev_transit_weight + this_transit)
                    / (prev_transit_weight + 1))
    prev_transit_weight = prev_transit_weight + 1
    return prev_transit, prev_transit_weight
