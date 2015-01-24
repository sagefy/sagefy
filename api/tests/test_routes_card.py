import pytest

xfail = pytest.mark.xfail


@xfail
def test_get_card():
    """
    Expect to get the card information for displaying to a contributor.
    """

    assert False
