"""
PMF, or Probability Mass Function.
"""

from modules.sequencer.formulas import calculate_correct, calculate_incorrect
from modules.sequencer.params import adjust_guess, adjust_slip


def init_pmf(hypotheses=None):
  """
  Create a new PMF, given a list of hypotheses.
  Internally, hypotheses is a dict of hypo: probability.
  """

  if isinstance(hypotheses, (tuple, list)):
    hypotheses = {hypothesis: 1 for hypothesis in hypotheses}
  elif isinstance(hypotheses, dict):
    hypotheses = hypotheses
  else:
    hypotheses = {}
  return normalize_pmf(hypotheses)


def update_pmf(hypotheses, data, likelihood):
  """
  Main update function. Updates each hypothesis based on the
  data provided.

  **likelihood**: What is the likelihood of getting this data,
          given the particular hypothesis?
  """

  assert callable(likelihood), "No method implemented."
  hypotheses = {hypothesis:
                probability * likelihood(data, hypothesis)
                for hypothesis, probability
                in hypotheses.items()}
  return normalize_pmf(hypotheses)


def normalize_pmf(hypotheses):
  """
  Make sure that all hypotheses sum up to 1.
  """

  total = sum(probability
              for hypothesis, probability
              in hypotheses.items())
  hypotheses = {hypothesis:
                probability / total
                for hypothesis, probability
                in hypotheses.items()}
  return hypotheses


def get_pmf_value(hypotheses):
  """
  Turns the distribution into a single value.
  Tends to fall inbetween the mode and the mean,
  but fares better earlier on than either.
  """

  return sum(hypothesis * probability
             for hypothesis, probability
             in hypotheses.items())


def get_guess_pmf_likelihood(data, hypothesis):
  """
  Given new data and one of the guess hypotheses,
  update the probability of that hypothesis.
  """

  score, learned, slip = \
    data['score'], data['learned'], data['slip']
  return (score
          * calculate_correct(hypothesis, slip, learned)
          + (1 - score)
          * calculate_incorrect(hypothesis, slip, learned))


def get_guess_pmf_value(hypotheses):
  """
  The PMF tends to overestimate guess,
  even though correlation is decent,
  so let's trim it down a bit.
  TODO-3 Why does this PMF overestimate guess?
  """

  return get_pmf_value(hypotheses) * adjust_guess


def get_slip_pmf_likelihood(data, hypothesis):
  """
  Given new data and one of the slip hypotheses,
  update the probability of that hypothesis.
  """

  score, learned, guess = \
    data['score'], data['learned'], data['guess']
  return (score
          * calculate_correct(guess, hypothesis, learned)
          + (1 - score)
          * calculate_incorrect(guess, hypothesis, learned))


def get_slip_pmf_value(hypotheses):
  """
  The PMF tends to overestimate guess,
  even though correlation is decent,
  so let's trim it down a bit.
  TODO-3 Why does this PMF overestimate slip?
  """

  return get_pmf_value(hypotheses) * adjust_slip


"""
TODO-3 How to write a PMF for `transit`.
Perhaps someone more savvy than me can figure it out.

What I do know is:

  transit = (learned_post - learned_pre) / (1 - learned_pre)
"""
