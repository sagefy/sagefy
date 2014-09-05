from models.notification import Notification


def get_error(errors, name):
    for error in errors:
        if error['name'] == name:
            return error


def test_create(app, db_conn, notifications_table):
    """
    Expect to create a notification.
    """
    notification, errors = Notification.insert({
        'user_id': 'abcd1234',
        'body': 'Lorem ipsum.',
        'tags': ['test']
    })
    record = notifications_table.filter({'user_id': 'abcd1234'}).run(db_conn)
    record = list(record)[0]
    assert len(errors) == 0
    assert record['user_id'] == 'abcd1234'
    assert record['tags'] == ['test']


def test_validations(app, db_conn, notifications_table):
    """
    Expect to only create valid notifications.
    - Fail if no user_id
    - Fail if no body
    - Fail if read not boolean.
    - Fail if tags not list.
    """
    notification, errors = Notification.insert({
        'read': 1234,
        'tags': 'test'
    })
    assert len(errors) == 4
    assert get_error(errors, 'user_id')['message'] == 'Required.'
    assert get_error(errors, 'body')['message'] == 'Required.'
    assert get_error(errors, 'read')['message'] == 'Must be true or false.'
    assert get_error(errors, 'tags')['message'] == 'Must be a list.'


def test_list(app, db_conn, notifications_table):
    """
    Expect to get a list of 10 notifications by user ID.
    """
    notifications_table.insert([
        {'id': 1, 'user_id': 22, 'body': 'red'},
        {'id': 2, 'user_id': 22, 'body': 'blue'},
        {'id': 3, 'user_id': 22, 'body': 'green'},
        {'id': 4, 'user_id': 22, 'body': 'brown'},
    ]).run(db_conn)
    notifications = Notification.list(user_id=22)
    assert len(notifications) == 4
    assert notifications[0].body in ('red', 'blue', 'green', 'brown')


def test_list_user(app, db_conn, notifications_table):
    """
    Expect to get a only notifications of user.
    """
    notifications_table.insert([
        {'id': 1, 'user_id': 22, 'body': 'red'},
        {'id': 2, 'user_id': 22, 'body': 'blue'},
        {'id': 3, 'user_id': 24, 'body': 'green'},
        {'id': 4, 'user_id': 25, 'body': 'brown'},
    ]).run(db_conn)
    notifications = Notification.list(user_id=22)
    assert len(notifications) == 2
    assert notifications[0].body in ('red', 'blue')
    assert notifications[1].body in ('red', 'blue')


def test_list_paginate(app, db_conn, notifications_table):
    """
    Expect to paginate lists of notifications.
    """
    for i in range(0, 25):
        notifications_table.insert({
            'id': i, 'user_id': 22, 'body': 'red',
        }).run(db_conn)
    notifications = Notification.list(user_id=22)
    assert len(notifications) == 10
    notifications = Notification.list(user_id=22, skip=20)
    assert len(notifications) == 5


def test_list_unread(app, db_conn, notifications_table):
    """
    Expect to get a list of unread notifications.
    """
    notifications_table.insert([
        {'id': 1, 'user_id': 22, 'body': 'red', 'read': True},
        {'id': 3, 'user_id': 22, 'body': 'green', 'read': False},
        {'id': 4, 'user_id': 22, 'body': 'brown', 'read': False},
    ]).run(db_conn)
    notifications = Notification.list(user_id=22, read=False)
    assert len(notifications) == 2
    assert notifications[0].id in (3, 4)
    assert notifications[1].id in (3, 4)


def test_list_tag(app, db_conn, notifications_table):
    """
    Expect to get a list of notifications by tag.
    """
    notifications_table.insert([
        {'id': 1, 'user_id': 22, 'body': 'red', 'tags': ['apple', 'banana']},
        {'id': 2, 'user_id': 22, 'body': 'blue', 'tags': ['orange', 'banana']},
        {'id': 3, 'user_id': 23, 'body': 'green', 'tags': ['apple', 'grape']},
        {'id': 4, 'user_id': 22, 'body': 'brown', 'tags': ['apple', 'peach']},
    ]).run(db_conn)
    notifications = Notification.list(user_id=22, tag='apple')
    assert len(notifications) == 2
    assert 'apple' in notifications[0].tags
    assert 'apple' in notifications[1].tags


def test_list_empty(app, db_conn, notifications_table):
    """
    Expect to get an empty list when run out of notifications.
    """
    notifications = Notification.list(user_id=22)
    assert len(notifications) == 0


def test_mark_as_read(app, db_conn, notifications_table):
    """
    Expect to mark a notification as read.
    """
    notification, errors = Notification.insert({
        'user_id': 'abcd1234',
        'body': 'Lorem ipsum.',
        'tags': ['test']
    })
    assert notification.read is False
    notification.mark_as_read()
    assert notification.read is True
    record = notifications_table.filter({'user_id': 'abcd1234'}).run(db_conn)
    record = list(record)[0]
    assert record['read'] is True
