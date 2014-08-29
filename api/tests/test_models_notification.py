import pytest


@pytest.mark.xfail
def test_create(app, db_conn, notifications_table):
    """
    Expect to create a notification.
    """
    assert False


@pytest.mark.xfail
def test_validations(app, db_conn, notifications_table):
    """
    Expect to only create valid notifications.
    - Fail if no user_id
    - Fail if no body
    - Fail if read not boolean.
    - Fail if tags not list.
    """
    assert False


@pytest.mark.xfail
def test_list(app, db_conn, notifications_table):
    """
    Expect to get a list of 10 notifications by user ID.
    """
    assert False


@pytest.mark.xfail
def test_list_user(app, db_conn, notifications_table):
    """
    Expect to get a only notifications of user.
    """
    assert False


@pytest.mark.xfail
def test_list_paginate(app, db_conn, notifications_table):
    """
    Expect to paginate lists of notifications.
    """
    assert False


@pytest.mark.xfail
def test_list_unread(app, db_conn, notifications_table):
    """
    Expect to get a list of unread notifications.
    """
    assert False


@pytest.mark.xfail
def test_list_tag(app, db_conn, notifications_table):
    """
    Expect to get a list of notifications by tag.
    """
    assert False


@pytest.mark.xfail
def test_list_empty(app, db_conn, notifications_table):
    """
    Expect to get an empty list when run out of notifications.
    """
    assert False


@pytest.mark.xfail
def test_mark_as_read(app, db_conn, notifications_table):
    """
    Expect to mark a notification as read.
    """
    assert False
