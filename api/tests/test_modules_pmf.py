import pytest

xfail = pytest.mark.xfail


@xfail
def test_create():
    """
    Expect to create a new PMF with given hypotheses.
    """

    assert False


@xfail
def test_update():
    """
    Expect to update a PMF with given data.
    """

    assert False


@xfail
def test_likelihood():
    """
    Expect to require and use a likelihood function to update.
    """

    assert False


@xfail
def test_normalize():
    """
    Expect all the probabilities of the PMF to add up to 1.
    """

    assert False


@xfail
def test_get_value():
    """
    Expect to get a single number representing the best fit for the PMF.
    """

    assert False
