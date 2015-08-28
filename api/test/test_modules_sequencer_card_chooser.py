import pytest

xfail = pytest.mark.xfail


@xfail
def test_update(app):
    """
    Expect to choose an appropriate card.
    """

    assert False
