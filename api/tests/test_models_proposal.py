import pytest

xfail = pytest.mark.xfail


@xfail
def test_user_id(app, db_conn, posts_table):
    """
    Expect a proposal to require a user id.
    """

    return False


@xfail
def test_topic(app, db_conn, posts_table):
    """
    Expect a proposal to require a topic id.
    """

    return False


@xfail
def test_body(app, db_conn, posts_table):
    """
    Expect a proposal to require a body.
    """

    return False


@xfail
def test_kind(app, db_conn, posts_table):
    """
    Expect a proposal to have a kind.
    """

    return False


@xfail
def test_replies(app, db_conn, posts_table):
    """
    Expect a proposal to allow a replies to id.
    """

    return False


@xfail
def test_entity(app, db_conn, posts_table):
    """
    Expect a proposal to require an entity version id.
    """

    return False


@xfail
def test_name(app, db_conn, posts_table):
    """
    Expect a proposal to require a name.
    """

    return False


@xfail
def test_status(app, db_conn, posts_table):
    """
    Expect a proposal to require a status.
    """

    return False


@xfail
def test_action(app, db_conn, posts_table):
    """
    Expect a proposal to require an action.
    """

    return False
