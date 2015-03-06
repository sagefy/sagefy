import pytest

xfail = pytest.mark.xfail


@xfail
def test_get_unit():
    """
    Expect to get the unit information for displaying to a contributor.
    """

    assert False

    # TODO provide model data
    # TODO join through requires
    # TODO join through sets
    # TODO list of topics
    # TODO list of versions
    # TODO sequencer data: learners, quality, difficulty


@xfail
def test_get_unit_404():
    """
    Expect to fail to get an unknown unit (404).
    """

    assert False
