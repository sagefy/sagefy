import pytest

xfail = pytest.mark.xfail


@xfail
def test_user(app, db_conn, posts_table):
    """
    Expect a post to require a user id.
    """
    return False


@xfail
def test_topic(app, db_conn, posts_table):
    """
    Expect a post to require a topic id.
    """
    return False


@xfail
def test_body(app, db_conn, posts_table):
    """
    Expect a post to require a body.
    """
    return False


@xfail
def test_kind(app, db_conn, posts_table):
    """
    Expect a post to have a kind.
    """
    return False


@xfail
def test_replies(app, db_conn, posts_table):
    """
    Expect a post to allow a replies to id.
    """
    return False
