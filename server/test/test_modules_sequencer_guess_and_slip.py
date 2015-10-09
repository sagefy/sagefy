import os
import sys
import inspect
currentdir = os.path.dirname(
    os.path.abspath(
        inspect.getfile(
            inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)


from modules.sequencer.formulas import calculate_correct, calculate_incorrect


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
