from models.follow.notice import Notice


def get_error(errors, name):
    for error in errors:
        if error['name'] == name:
            return error


def test_create(app, db_conn, notices_table):
    """
    Expect to create a notice.
    """
    notice, errors = Notice.insert({
        'user_id': 'abcd1234',
        'kind': 'new_proposal',
        'tags': ['test']
    })
    record = notices_table.filter({'user_id': 'abcd1234'}).run(db_conn)
    record = list(record)[0]
    assert len(errors) == 0
    assert record['user_id'] == 'abcd1234'
    assert record['tags'] == ['test']


def test_validations(app, db_conn, notices_table):
    """
    Expect to only create valid notices.
    - Fail if no user_id
    - Fail if no kind
    - Fail if read not boolean.
    - Fail if tags not list.
    """
    notice, errors = Notice.insert({
        'read': 1234,
        'tags': 'test'
    })
    assert len(errors) == 4
    assert get_error(errors, 'user_id')['message'] == 'Required.'
    assert get_error(errors, 'kind')['message'] == 'Required.'
    assert get_error(errors, 'read')['message'] == 'Must be true or false.'
    assert get_error(errors, 'tags')['message'] == 'Must be a list.'


def test_list(app, db_conn, notices_table):
    """
    Expect to get a list of 10 notices by user ID.
    """
    notices_table.insert([
        {'id': 1, 'user_id': 22, 'kind': 'new_proposal'},
        {'id': 2, 'user_id': 22, 'kind': 'new_proposal'},
        {'id': 3, 'user_id': 22, 'kind': 'new_proposal'},
        {'id': 4, 'user_id': 22, 'kind': 'new_proposal'},
    ]).run(db_conn)
    notices = Notice.list(user_id=22)
    assert len(notices) == 4


def test_list_user(app, db_conn, notices_table):
    """
    Expect to get a only notices of user.
    """
    notices_table.insert([
        {'id': 1, 'user_id': 22, 'kind': 'new_proposal'},
        {'id': 2, 'user_id': 22, 'kind': 'new_proposal'},
        {'id': 3, 'user_id': 24, 'kind': 'new_proposal'},
        {'id': 4, 'user_id': 25, 'kind': 'new_proposal'},
    ]).run(db_conn)
    notices = Notice.list(user_id=22)
    assert len(notices) == 2


def test_list_paginate(app, db_conn, notices_table):
    """
    Expect to paginate lists of notices.
    """
    for i in range(0, 25):
        notices_table.insert({
            'id': i, 'user_id': 22, 'kind': 'new_proposal',
        }).run(db_conn)
    notices = Notice.list(user_id=22)
    assert len(notices) == 10
    notices = Notice.list(user_id=22, skip=20)
    assert len(notices) == 5


def test_list_unread(app, db_conn, notices_table):
    """
    Expect to get a list of unread notices.
    """
    notices_table.insert([
        {'id': 1, 'user_id': 22, 'kind': 'new_proposal', 'read': True},
        {'id': 3, 'user_id': 22, 'kind': 'new_proposal', 'read': False},
        {'id': 4, 'user_id': 22, 'kind': 'new_proposal', 'read': False},
    ]).run(db_conn)
    notices = Notice.list(user_id=22, read=False)
    assert len(notices) == 2
    assert notices[0].id in (3, 4)
    assert notices[1].id in (3, 4)


def test_list_tag(app, db_conn, notices_table):
    """
    Expect to get a list of notices by tag.
    """
    notices_table.insert([
        {'id': 1, 'user_id': 22, 'kind': 'new_proposal',
            'tags': ['apple', 'banana']},
        {'id': 2, 'user_id': 22, 'kind': 'new_proposal',
            'tags': ['orange', 'banana']},
        {'id': 3, 'user_id': 23, 'kind': 'new_proposal',
            'tags': ['apple', 'grape']},
        {'id': 4, 'user_id': 22, 'kind': 'new_proposal',
            'tags': ['apple', 'peach']},
    ]).run(db_conn)
    notices = Notice.list(user_id=22, tag='apple')
    assert len(notices) == 2
    assert 'apple' in notices[0].tags
    assert 'apple' in notices[1].tags


def test_list_empty(app, db_conn, notices_table):
    """
    Expect to get an empty list when run out of notices.
    """
    notices = Notice.list(user_id=22)
    assert len(notices) == 0


def test_mark_as_read(app, db_conn, notices_table):
    """
    Expect to mark a notice as read.
    """
    notice, errors = Notice.insert({
        'user_id': 'abcd1234',
        'kind': 'new_proposal',
        'tags': ['test']
    })
    assert notice.read is False
    notice.mark_as_read()
    assert notice.read is True
    record = notices_table.filter({'user_id': 'abcd1234'}).run(db_conn)
    record = list(record)[0]
    assert record['read'] is True


"""
- TODO: Expect to filter notices by kind.
- TODO: Expect to get the notice body.
- TODO: Expect to get the notice body with other data added in from the db.
- TODO: Expect to mark as unread.
"""
