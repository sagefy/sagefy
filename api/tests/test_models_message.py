from models.message import Message


def test_insert(app, db_conn, messages_table):
    """
    Expect a message to require from, to, name, and body.
    """
    message, errors = Message.insert({
        'from_user_id': '1',
        'to_user_id': '2',
        'name': 'Yo!',
        'body': 'How\'s it going?',
    })
    assert len(errors) == 0
    record = messages_table.get(message.id.get()).run(db_conn)
    assert record['from_user_id'] == '1'
    assert record['name'] == 'Yo!'


def test_read_default(app, db_conn, messages_table):
    """
    Expect read to default to false.
    """
    message, errors = Message.insert({
        'from_user_id': '1',
        'to_user_id': '2',
        'name': 'Yo!',
        'body': 'How\'s it going?',
    })
    assert message.read.get() is False


def test_list(app, db_conn, messages_table):
    """
    Expect to get a list of messages to user.
    """
    messages_table.insert([
        {'from_user_id': 'a', 'to_user_id': 'b', 'name': 'a', 'body': 'b'},
        {'from_user_id': 'b', 'to_user_id': 'a', 'name': 'ra', 'body': 'rb'},
        {'from_user_id': 'a', 'to_user_id': 'd', 'name': 'da', 'body': 'qb'},
        {'from_user_id': 'c', 'to_user_id': 'd', 'name': 'ca', 'body': 'gb'},
    ]).run(db_conn)
    messages = Message.list()
    assert len(messages) == 4


def test_list_from(app, db_conn, messages_table):
    """
    Expect to get a list of messages from user.
    """
    messages_table.insert([
        {'from_user_id': 'a', 'to_user_id': 'b', 'name': 'a', 'body': 'b'},
        {'from_user_id': 'b', 'to_user_id': 'a', 'name': 'ra', 'body': 'rb'},
        {'from_user_id': 'a', 'to_user_id': 'd', 'name': 'da', 'body': 'qb'},
        {'from_user_id': 'c', 'to_user_id': 'd', 'name': 'ca', 'body': 'gb'},
    ]).run(db_conn)
    assert len(Message.list(from_user_id='a')) == 2
    assert len(Message.list(from_user_id='b')) == 1
    assert len(Message.list(from_user_id='d')) == 0


def test_list_unread(app, db_conn, messages_table):
    """
    Expect to get unread messages to user.
    """
    messages_table.insert([
        {'from_user_id': 'a', 'to_user_id': 'a',
         'name': 'a', 'body': 'b', 'read': True},
        {'from_user_id': 'b', 'to_user_id': 'a',
         'name': 'ra', 'body': 'rb', 'read': False},
        {'from_user_id': 'a', 'to_user_id': 'a',
         'name': 'da', 'body': 'qb', 'read': True},
        {'from_user_id': 'c', 'to_user_id': 'a',
         'name': 'ca', 'body': 'gb', 'read': False},
    ]).run(db_conn)
    messages = Message.list(to_user_id='a', read=False)
    assert len(messages) == 2


def test_tagged(app, db_conn, messages_table):
    """
    Expect to get messages by tag.
    """
    messages_table.insert([
        {'from_user_id': 'a', 'to_user_id': 'b',
         'name': 'a', 'body': 'b', 'tags': ['a', 'b']},
        {'from_user_id': 'b', 'to_user_id': 'a',
         'name': 'ra', 'body': 'rb', 'tags': ['a', 'c']},
        {'from_user_id': 'a', 'to_user_id': 'd',
         'name': 'da', 'body': 'qb', 'tags': ['b', 'c']},
        {'from_user_id': 'c', 'to_user_id': 'd',
         'name': 'ca', 'body': 'gb', 'tags': ['c', 'd']},
    ]).run(db_conn)
    assert len(Message.list(tag='a')) == 2
    assert len(Message.list(tag='b')) == 2
    assert len(Message.list(tag='c')) == 3
    assert len(Message.list(tag='d')) == 1
    assert len(Message.list(tag='e')) == 0


def test_paginate(app, db_conn, messages_table):
    """
    Expect to paginate messages.
    """
    for i in range(0, 25):
        messages_table.insert({
            'id': str(i), 'from_user_id': 'a', 'to_user_id': 'b',
            'body': 'red', 'name': 'b',
        }).run(db_conn)
    messages = Message.list()
    assert len(messages) == 10
    messages = Message.list(skip=20)
    assert len(messages) == 5


def test_empty(app, db_conn, messages_table):
    """
    Expect to get no messages matching parameters.
    """
    assert len(Message.list()) == 0


def test_read(app, db_conn, messages_table):
    """
    Expect to mark a message as read.
    """
    message, errors = Message.insert({
        'from_user_id': '1',
        'to_user_id': '2',
        'name': 'Yo!',
        'body': 'How\'s it going?',
    })
    record = messages_table.get(message.id.get()).run(db_conn)
    assert message.read.get() is False
    assert record['read'] is False
    message.mark_as_read()
    record = messages_table.get(message.id.get()).run(db_conn)
    assert message.read.get() is True
    assert record['read'] is True
