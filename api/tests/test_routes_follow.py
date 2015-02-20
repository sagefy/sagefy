import pytest

xfail = pytest.mark.xfail


@xfail
def test_follow():
    """
    Expect to follow an entity.
    """

    assert False


@xfail
def test_follow_401():
    """
    Expect to fail to follow entity if not logged in.
    """

    assert False


@xfail
def test_follow_404():
    """
    Expect to fail to follow entity if not found entity.
    """

    assert False


@xfail
def test_follow_409():
    """
    Expect to fail to follow entity if already followed.
    """

    assert False


@xfail
def test_follow_400():
    """
    Expect to fail to follow entity if the request is nonsense.
    """

    assert False


@xfail
def test_unfollow():
    """
    Expect to unfollow an entity.
    """

    assert False


@xfail
def test_unfollow_401():
    """
    Expect to fail to unfollow an entity if not logged in.
    """

    assert False


@xfail
def test_unfollow_404():
    """
    Expect to fail to unfollow an entity if no entity.
    """

    assert False


@xfail
def test_unfollow_409():
    """
    Expect to fail to unfollow an entity if not followed.
    """

    assert False


@xfail
def test_unfollow_400():
    """
    Expect to fail to unfollow an entity if request is nonsense.
    """

    assert False


@xfail
def test_get_follows():
    """
    Expect to get a list of follows for user.
    """

    assert False


@xfail
def test_get_follows_401():
    """
    Expect fail to to get a list of follows for user if not logged in.
    """

    assert False


@xfail
def test_get_follows_400():
    """
    Expect fail to to get a list of follows for user if nonsense params.
    """

    assert False
