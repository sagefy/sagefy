import pytest

xfail = pytest.mark.xfail


@xfail
def test_user(app, db_conn, user_sets_table):
    """
    Expect to require a user ID.
    """

    return False


@xfail
def test_sets(app, db_conn, user_sets_table):
    """
    Expect to require a list of set IDs.
    """

    return False
