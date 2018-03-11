# pylint: disable=too-many-arguments
"""
This document contains the formulas for Sagefy's adaptive learning algorithm.
"""

from math import exp
from modules.sequencer.params import belief_factor


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
  return calculate_incorrect(guess, slip, 0.5)


def calculate_belief(learned, time_delta):
  """
  How much should we believe in learned, given the amount of time that
  has passed?
  """

  return exp(-1 * time_delta * (1 - learned) / belief_factor)


def update_learned(score, learned, guess, slip, transit, time_delta):
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
