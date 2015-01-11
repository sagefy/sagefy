import pytest

xfail = pytest.mark.xfail


@xfail
def test_something(app, db_conn, user_sets_table):
    """
    Expect to have tests
    """

    return False
