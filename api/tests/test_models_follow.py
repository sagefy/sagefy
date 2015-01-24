import pytest

xfail = pytest.mark.xfail


@xfail
def test_user_id(app, db_conn, follows_table):
    """
    A follow should require a user_id.
    """
    assert False


@xfail
def test_entity(app, db_conn, follows_table):
    """
    Expect a follow to require an entity kind and id.
    """
    assert False
