import pytest

xfail = pytest.mark.xfail


@xfail
def test_user_id(app, db_conn, posts_table):
    """
    Expect a flag to require a user id.
    """
    return False


@xfail
def test_topic_id(app, db_conn, posts_table):
    """
    Expect a flag to require a topic id.
    """
    return False


@xfail
def test_body(app, db_conn, posts_table):
    """
    Expect a flag to require a body.
    """
    return False


@xfail
def test_kind(app, db_conn, posts_table):
    """
    Expect a flag to have a kind.
    """
    return False


@xfail
def test_replies(app, db_conn, posts_table):
    """
    Expect a flag to allow a replies to id.
    """
    return False


@xfail
def test_reason(app, db_conn, posts_table):
    """
    Expect a flag to require a reason.
    """
    return False


@xfail
def test_status(app, db_conn, posts_table):
    """
    Expect a flag to require a status.
    """
    return False
