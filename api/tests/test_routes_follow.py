import pytest

xfail = pytest.mark.xfail


@xfail
def test_follow():
    """
    Expect to follow an entity.
    """

    assert False
    # TODO 401, 404, 409, 400


@xfail
def test_unfollow():
    """
    Expect to unfollow an entity.
    """

    assert False
    # TODO 401, 404, 409, 400


@xfail
def test_get_follows():
    """
    Expect to get a list of follows for user.
    """

    assert False
    # TODO 401, 400
