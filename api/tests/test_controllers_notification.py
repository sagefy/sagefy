import pytest


@pytest.mark.xfail
def test_list(app, db_conn, notifications_table):
    """
    Expect to get a list of 10 notifications by user ID.
    """
    assert False


@pytest.mark.xfail
def test_list_no_user(app, db_conn):
    """
    Expect to get an error if not logged in.
    """
    assert False


@pytest.mark.xfail
def test_list_paginate(app, db_conn, notifications_table):
    """
    Expect to paginate lists of notifications.
    """
    assert False


@pytest.mark.xfail
def test_mark(app, db_conn, notifications_table):
    """
    Expect to mark a notification as read.
    """
    assert False


@pytest.mark.xfail
def test_mark_no_user(app, db_conn, notifications_table):
    """
    Expect to error on not logged in when marking as read.
    """
    assert False


@pytest.mark.xfail
def test_mark_no_notification(app, db_conn, notifications_table):
    """
    Expect to error on no notification in when marking as read.
    """
    assert False


@pytest.mark.xfail
def test_mark_not_owned(app, db_conn, notifications_table):
    """
    Expect to error when not own notification when marking as read.
    """
    assert False
