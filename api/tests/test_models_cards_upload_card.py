import pytest

xfail = pytest.mark.xfail


@xfail
def test_x(app):
    """
    Expect ...
    """

    assert False
