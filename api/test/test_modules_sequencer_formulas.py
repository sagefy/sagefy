# from modules.sequencer.formulas import update, calculate_correct, \
#     calculate_incorrect, calculate_difficulty, update_guess, update_slip, \
#     calculate_belief, update_learned

import pytest

xfail = pytest.mark.xfail


@xfail
def test_update(app):
    """
    Expect to update entity information based on learner response.
    """

    assert False


@xfail
def test_correct(app):
    """
    Expect to calculate probability of correct.
    """

    assert False


@xfail
def test_incorrect(app):
    """
    Expect to calculate probability of incorrect.
    """

    assert False


@xfail
def test_difficulty(app):
    """
    Expect to calculate average difficulty of card.
    """

    assert False


@xfail
def test_guess(app):
    """
    Expect to update card guess based on learner response.
    """

    assert False


@xfail
def test_slip(app):
    """
    Expect to update card slip based on learner response.
    """

    assert False


@xfail
def test_belief(app):
    """
    Expect to update belief based on learner response time.
    """

    assert False


@xfail
def test_learned(app):
    """
    Expect to update learned based on learner response.
    """

    assert False


"""
Expect to estimate learner-set ability.
Expect to calculate unit quality.
Expect to calculate set quality.
Expect to calculate unit difficulty.
Expect to calculate set difficulty.
"""
