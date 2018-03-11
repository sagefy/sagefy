
from modules.sequencer.pmf import init_pmf, update_pmf, normalize_pmf, \
  get_pmf_value


def test_init_pmf():
  """
  Expect to create a new PMF with given hypotheses.
  """

  test = {0: 0.25, 0.5: 0.25, 0.75: 0.25, 1: 0.25}
  hypotheses_a = init_pmf(tuple(test.keys()))
  assert hypotheses_a == test
  hypotheses_b = init_pmf(test)
  assert hypotheses_b == test
  hypotheses_c = init_pmf()
  assert hypotheses_c == {}


def test_update_pmf():
  """
  Expect to update a PMF with given data,
  require and use a likelihood function to update.
  """

  def likelihood(data, hypothesis):
    return hypothesis

  hypotheses = init_pmf((0, 0.5, 0.75, 1))
  hypotheses = update_pmf(hypotheses, {}, likelihood)
  assert hypotheses == {
    0: 0.0,
    0.5: 2 / 9,
    0.75: 1 / 3,
    1: 4 / 9,
  }


def test_normalize_pmf():
  """
  Expect all the probabilities of the PMF to add up to 1.
  """

  hypotheses = {0: 1, 1: 1}
  hypotheses = normalize_pmf(hypotheses)
  assert hypotheses[0] == 0.5


def test_get_pmf_value():
  """
  Expect to get a single number representing the best fit for the PMF.
  """

  hypotheses = init_pmf((0, 0.5, 0.75, 1))
  assert get_pmf_value(hypotheses) == 0.5625
