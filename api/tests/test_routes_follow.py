import pytest

xfail = pytest.mark.xfail


@xfail
def test_follow():
    """
    Expect to follow an entity.
    """

    assert False


@xfail
def test_unfollow():
    """
    Expect to unfollow an entity.
    """

    assert False
