import pytest

xfail = pytest.mark.xfail


@xfail
def test_user_id(app, db_conn, topics_table):
    """
    Expect a topic to require a user id.
    """
    return False


@xfail
def test_name(app, db_conn, topics_table):
    """
    Expect a topic to require a name.
    """
    return False


@xfail
def test_entity(app, db_conn, topics_table):
    """
    Expect a topic to require an entity kind and id.
    """
    return False
