import pytest

xfail = pytest.mark.xfail


@xfail
def test_get_unit():
    """
    Expect to get the unit information for displaying to a contributor.
    """

    assert False


@xfail
def test_get_unit_404():
    """
    Expect to fail to get an unknown unit (404).
    """

    assert False
