
from modules.sequencer.formulas import calculate_correct, \
  calculate_incorrect, \
  calculate_difficulty, \
  calculate_belief, \
  update_learned


def test_calculate_correct():
  assert calculate_correct(guess=0, slip=0, learned=0.5) == 0.5
  assert calculate_correct(guess=1, slip=1, learned=0.5) == 0.5
  assert calculate_correct(guess=0, slip=1, learned=0.5) == 0
  assert calculate_correct(guess=1, slip=0, learned=0.5) == 1
  assert calculate_correct(guess=0.25, slip=0.05, learned=0.9) == 0.88
  assert calculate_correct(guess=0.25, slip=0.05, learned=0.5) == 0.6
  assert calculate_correct(guess=0.25, slip=0.05, learned=0.1) == 0.32


def test_calculate_incorrect():
  assert calculate_incorrect(guess=0, slip=0, learned=0.5) == 0.5
  assert calculate_incorrect(guess=1, slip=1, learned=0.5) == 0.5
  assert calculate_incorrect(guess=0, slip=1, learned=0.5) == 1
  assert calculate_incorrect(guess=1, slip=0, learned=0.5) == 0
  assert calculate_incorrect(guess=0.25, slip=0.05, learned=0.9) == 0.12
  assert calculate_incorrect(guess=0.25, slip=0.05, learned=0.5) == 0.4
  assert calculate_incorrect(guess=0.25, slip=0.05, learned=0.1) == 0.68


def test_calculate_difficulty():
  assert calculate_difficulty(guess=1, slip=1) == float("inf")
  assert calculate_difficulty(guess=0.25, slip=0.5) == 0.625
  assert calculate_difficulty(guess=0.25, slip=0.05) == 0.4
  assert calculate_difficulty(guess=0, slip=0) == 0.5
  assert calculate_difficulty(guess=1, slip=0) == 0
  assert calculate_difficulty(guess=0, slip=1) == 1


def test_calculate_belief():
  assert calculate_belief(0.5, 60) > 0.99
  assert calculate_belief(0.5, 60 * 60) > 0.99
  assert calculate_belief(0.5, 60 * 60 * 24) > 0.94
  assert calculate_belief(0.5, 60 * 60 * 24 * 7) > 0.65
  assert calculate_belief(0.9, 60 * 60 * 24 * 7) > 0.91
  assert calculate_belief(0.99, 60 * 60 * 24 * 7) > 0.99
  assert calculate_belief(0.5, 60 * 60 * 24 * 365) < 0.01


def test_update_learned():
  value = update_learned(
    score=1,
    learned=0.5,
    guess=0.25,
    slip=0.05,
    transit=0.05,
    time_delta=60 * 60
  )
  assert value > 0.8 and value < 0.81


############################################################################


def guess_likelihood(score, guess, slip, learned):
  if score == 1:
    return calculate_correct(1, slip, learned)
  if score == 0:
    return calculate_incorrect(1, slip, learned)


def guess_normal(score, guess, slip, learned):
  if score == 1:
    return calculate_correct(guess, slip, learned)
  if score == 0:
    return calculate_incorrect(guess, slip, learned)


def slip_likelihood(score, guess, slip, learned):
  if score == 1:
    return calculate_correct(guess, 1, learned)
  if score == 0:
    return calculate_incorrect(guess, 1, learned)


def slip_normal(score, guess, slip, learned):
  if score == 1:
    return calculate_correct(guess, slip, learned)
  if score == 0:
    return calculate_incorrect(guess, slip, learned)


def update_guess(score, guess, slip, learned):
  return (guess
          * guess_likelihood(score, guess, slip, learned)
          / guess_normal(score, guess, slip, learned))


def update_slip(score, guess, slip, learned):
  return (slip
          * slip_likelihood(score, guess, slip, learned)
          / slip_normal(score, guess, slip, learned))


# ### TESTS ### #

def test_guess_correct():
  """If a learner answers correctly,
     guess should go up or stay the same."""

  assert update_guess(1, 0.3, 0.1, 0.7) >= 0.3
  assert update_guess(1, 0.1, 0.3, 0.7) >= 0.1
  assert update_guess(1, 0.01, 0.01, 0.01) >= 0.01
  assert update_guess(1, 0.49, 0.49, 0.99) >= 0.49


def test_guess_incorrect():
  """If a learner answers incorrectly,
     guess should go down or stay the same."""

  assert update_guess(0, 0.3, 0.1, 0.7) <= 0.3
  assert update_guess(0, 0.1, 0.3, 0.7) <= 0.1
  assert update_guess(0, 0.01, 0.01, 0.01) <= 0.01
  assert update_guess(0, 0.49, 0.49, 0.99) <= 0.49


def test_guess_learner():
  """A learner with a low learned tells us more about guess
    than a learner with a high learned when the answer is correct."""

  assert update_guess(1, 0.3, 0.1, 0.2) > \
    update_guess(1, 0.3, 0.1, 0.8)
  assert update_guess(1, 0.01, 0.01, 0.01) > \
    update_guess(1, 0.01, 0.01, 0.99)
  assert update_guess(1, 0.49, 0.49, 0.01) > \
    update_guess(1, 0.49, 0.49, 0.99)


def test_guess_range():
  """Guess should always be > 0 and < 1."""

  assert 1 > update_guess(0, 0.3, 0.1, 0.7) > 0
  assert 1 > update_guess(0, 0.01, 0.01, 0.01) > 0
  assert 1 > update_guess(0, 0.49, 0.49, 0.99) > 0
  assert 1 > update_guess(0, 0.01, 0.01, 0.99) > 0
  assert 1 > update_guess(0, 0.49, 0.49, 0.01) > 0
  assert 1 > update_guess(1, 0.3, 0.1, 0.7) > 0
  assert 1 > update_guess(1, 0.01, 0.01, 0.01) > 0
  assert 1 > update_guess(1, 0.49, 0.49, 0.99) > 0
  assert 1 > update_guess(1, 0.01, 0.01, 0.99) > 0
  assert 1 > update_guess(1, 0.49, 0.49, 0.01) > 0


def test_slip_correct():
  """If a learner answers correctly,
     slip should go down or stay the same."""

  assert update_slip(1, 0.3, 0.1, 0.7) <= 0.1
  assert update_slip(1, 0.1, 0.3, 0.7) <= 0.3
  assert update_slip(1, 0.01, 0.01, 0.01) <= 0.01
  assert update_slip(1, 0.49, 0.49, 0.99) <= 0.49


def test_slip_incorrect():
  """If a learner answers incorrectly,
     slip should go up or stay the same."""

  assert update_slip(0, 0.3, 0.1, 0.7) >= 0.1
  assert update_slip(0, 0.1, 0.3, 0.7) >= 0.3
  assert update_slip(0, 0.01, 0.01, 0.01) >= 0.01
  assert update_slip(0, 0.49, 0.49, 0.99) >= 0.49


def test_slip_learner():
  """A learner with a high learned tells us more about slip
     than a learner with a low learned when the answer is incorrect."""

  assert update_slip(0, 0.3, 0.1, 0.2) < update_slip(0, 0.3, 0.1, 0.8)
  assert update_slip(0, 0.01, 0.01, 0.01) < update_slip(0, 0.01, 0.01, 0.99)
  assert update_slip(0, 0.49, 0.49, 0.01) < update_slip(0, 0.49, 0.49, 0.99)


def test_slip_range():
  """Slip should always be > 0 and < 1."""

  assert 1 > update_slip(0, 0.3, 0.1, 0.7) > 0
  assert 1 > update_slip(0, 0.01, 0.01, 0.01) > 0
  assert 1 > update_slip(0, 0.49, 0.49, 0.99) > 0
  assert 1 > update_slip(0, 0.01, 0.01, 0.99) > 0
  assert 1 > update_slip(0, 0.49, 0.49, 0.01) > 0
  assert 1 > update_slip(1, 0.3, 0.1, 0.7) > 0
  assert 1 > update_slip(1, 0.01, 0.01, 0.01) > 0
  assert 1 > update_slip(1, 0.49, 0.49, 0.99) > 0
  assert 1 > update_slip(1, 0.01, 0.01, 0.99) > 0
  assert 1 > update_slip(1, 0.49, 0.49, 0.49) > 0
