import pytest

xfail = pytest.mark.xfail


@xfail
def test_user(app, db_conn, posts_table):
    """
    Expect a vote to require a user id.
    """
    return False


@xfail
def test_topic(app, db_conn, posts_table):
    """
    Expect a vote to require a topic id.
    """
    return False


@xfail
def test_body(app, db_conn, posts_table):
    """
    Expect a vote to allow, but not require, a body.
    """
    return False


@xfail
def test_kind(app, db_conn, posts_table):
    """
    Expect a vote to always have a kind of vote.
    """
    return False


@xfail
def test_replies(app, db_conn, posts_table):
    """
    Expect a vote to require a replies to id.
    """
    return False


@xfail
def test_response(app, db_conn, posts_table):
    """
    Expect a vote to require a response.
    """
    return False
