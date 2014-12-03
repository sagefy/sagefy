import pytest

xfail = pytest.mark.xfail


@xfail
def test_follow():
    """
    Expect to follow an entity.
    """

    return False


@xfail
def test_unfollow():
    """
    Expect to unfollow an entity.
    """

    return False
