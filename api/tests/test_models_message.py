from models.message import Message
import pytest


@pytest.mark.xfail
def test_insert(app, db_conn, messages_table):
    """
    Expect a message to require from, to, name, and body.
    """
    assert False


@pytest.mark.xfail
def test_read_default(app, db_conn, messages_table):
    """
    Expect read to default to false.
    """
    assert False


@pytest.mark.xfail
def test_list(app, db_conn, messages_table):
    """
    Expect to get a list of messages to user.
    """
    assert False


@pytest.mark.xfail
def test_list_from(app, db_conn, messages_table):
    """
    Expect to get a list of messages from user.
    """
    assert False


@pytest.mark.xfail
def test_list_unread(app, db_conn, messages_table):
    """
    Expect to get unread messages to user.
    """
    assert False


@pytest.mark.xfail
def test_tagged(app, db_conn, messages_table):
    """
    Expect to get messages by tag.
    """
    assert False


@pytest.mark.xfail
def test_paginate(app, db_conn, messages_table):
    """
    Expect to paginate messages.
    """
    assert False


@pytest.mark.xfail
def test_empty(app, db_conn, messages_table):
    """
    Expect to get no messages matching parameters.
    """
    assert False


@pytest.mark.xfail
def test_read(app, db_conn, messages_table):
    """
    Expect to mark a message as read.
    """
    assert False
