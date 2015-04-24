import pytest

xfail = pytest.mark.xfail


@xfail
def test_get_current_user():
    """
    Expect to get the current user given session info.
    """

    assert False


@xfail
def test_log_in_user():
    """
    Expect to log in as a user.
    """

    assert False


@xfail
def test_log_out_user():
    """
    Expect to log out as a user.
    """

    assert False
