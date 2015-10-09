import pytest

xfail = pytest.mark.xfail

from modules.sequencer.pmf import PMF


def test_create():
    """
    Expect to create a new PMF with given hypotheses.
    """

    test = {0: 0.25, 0.5: 0.25, 0.75: 0.25, 1: 0.25}

    a = PMF(tuple(test.keys()))
    assert a.hypotheses == test
    b = PMF(test)
    assert b.hypotheses == test
    c = PMF()
    assert c.hypotheses == {}


def test_likelihood_and_update():
    """
    Expect to update a PMF with given data,
    require and use a likelihood function to update.
    """

    class X(PMF):
        def likelihood(self, data, hypothesis):
            return hypothesis

    x = X((0, 0.5, 0.75, 1))
    x.update({})
    assert x.hypotheses == {
        0: 0.0,
        0.5: 2/9,
        0.75: 1/3,
        1: 4/9
    }


def test_normalize():
    """
    Expect all the probabilities of the PMF to add up to 1.
    """

    a = PMF()
    a.hypotheses = {0: 1, 1: 1}
    a.normalize()
    assert a.hypotheses[0] == 0.5


def test_get_value():
    """
    Expect to get a single number representing the best fit for the PMF.
    """

    a = PMF((0, 0.5, 0.75, 1))
    assert a.get_value() == 0.5625
