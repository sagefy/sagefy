from database.notice import insert_notice, list_notices, mark_notice_as_read, \
    mark_notice_as_unread, get_notice_body, deliver_notice


def get_error(errors, name):
    for error in errors:
        if error['name'] == name:
            return error


def test_create(db_conn, notices_table):
    """
    Expect to create a notice.
    """

    notice, errors = insert_notice({
        'user_id': 'abcd1234',
        'kind': 'create_proposal',
        'tags': ['test']
    }, db_conn)
    record = notices_table.filter({'user_id': 'abcd1234'}).run(db_conn)
    record = list(record)[0]
    assert len(errors) == 0
    assert record['user_id'] == 'abcd1234'
    assert record['tags'] == ['test']


def test_validations(db_conn, notices_table):
    """
    Expect to only create valid notices.
    - Fail if no user_id
    - Fail if no kind
    - Fail if read not boolean.
    - Fail if tags not list.
    """
    notice, errors = insert_notice({
        'read': 1234,
        'tags': 'test'
    }, db_conn)
    assert len(errors) == 4
    assert get_error(errors, 'user_id')['message'] == 'Required.'
    assert get_error(errors, 'kind')['message'] == 'Required.'
    assert get_error(errors, 'read')['message'] == 'Must be true or false.'
    assert get_error(errors, 'tags')['message'] == 'Must be a list.'


def test_list(db_conn, notices_table):
    """
    Expect to get a list of 10 notices by user ID.
    """
    notices_table.insert([
        {'id': 1, 'user_id': 22, 'kind': 'create_proposal'},
        {'id': 2, 'user_id': 22, 'kind': 'create_proposal'},
        {'id': 3, 'user_id': 22, 'kind': 'create_proposal'},
        {'id': 4, 'user_id': 22, 'kind': 'create_proposal'},
    ]).run(db_conn)
    notices = list_notices({'user_id': 22}, db_conn)
    assert len(notices) == 4


def test_list_user(db_conn, notices_table):
    """
    Expect to get a only notices of user.
    """
    notices_table.insert([
        {'id': 1, 'user_id': 22, 'kind': 'create_proposal'},
        {'id': 2, 'user_id': 22, 'kind': 'create_proposal'},
        {'id': 3, 'user_id': 24, 'kind': 'create_proposal'},
        {'id': 4, 'user_id': 25, 'kind': 'create_proposal'},
    ]).run(db_conn)
    notices = list_notices({'user_id': 22}, db_conn)
    assert len(notices) == 2


def test_list_paginate(db_conn, notices_table):
    """
    Expect to paginate lists of notices.
    """
    for i in range(0, 25):
        notices_table.insert({
            'id': i, 'user_id': 22, 'kind': 'create_proposal',
        }).run(db_conn)
    notices = list_notices({'user_id': 22}, db_conn)
    assert len(notices) == 10
    notices = list_notices({'user_id': 22, 'skip': 20}, db_conn)
    assert len(notices) == 5


def test_list_unread(db_conn, notices_table):
    """
    Expect to get a list of unread notices.
    """
    notices_table.insert([
        {'id': 1, 'user_id': 22, 'kind': 'create_proposal', 'read': True},
        {'id': 3, 'user_id': 22, 'kind': 'create_proposal', 'read': False},
        {'id': 4, 'user_id': 22, 'kind': 'create_proposal', 'read': False},
    ]).run(db_conn)
    notices = list_notices({'user_id': 22, 'read': False}, db_conn)
    assert len(notices) == 2
    assert notices[0]['id'] in (3, 4)
    assert notices[1]['id'] in (3, 4)


def test_list_tag(db_conn, notices_table):
    """
    Expect to get a list of notices by tag.
    """
    notices_table.insert([
        {'id': 1, 'user_id': 22, 'kind': 'create_proposal',
            'tags': ['apple', 'banana']},
        {'id': 2, 'user_id': 22, 'kind': 'create_proposal',
            'tags': ['orange', 'banana']},
        {'id': 3, 'user_id': 23, 'kind': 'create_proposal',
            'tags': ['apple', 'grape']},
        {'id': 4, 'user_id': 22, 'kind': 'create_proposal',
            'tags': ['apple', 'peach']},
    ]).run(db_conn)
    notices = list_notices({'user_id': 22, 'tag': 'apple'}, db_conn)
    assert len(notices) == 2
    assert 'apple' in notices[0]['tags']
    assert 'apple' in notices[1]['tags']


def test_list_empty(db_conn, notices_table):
    """
    Expect to get an empty list when run out of notices.
    """
    notices = list_notices({'user_id': 22}, db_conn)
    assert len(notices) == 0


def test_notices_kind(db_conn, notices_table):
    """
    Expect to filter notices by kind.
    """

    notices_table.insert([
        {'id': 1, 'user_id': 22, 'kind': 'create_proposal',
            'tags': ['apple', 'banana']},
        {'id': 2, 'user_id': 22, 'kind': 'accepted_proposal',
            'tags': ['orange', 'banana']},
        {'id': 3, 'user_id': 22, 'kind': 'create_proposal',
            'tags': ['apple', 'grape']},
        {'id': 4, 'user_id': 22, 'kind': 'new_topic',
            'tags': ['apple', 'peach']},
    ]).run(db_conn)
    notices = list_notices({'user_id': 22, 'kind': 'create_proposal'}, db_conn)
    assert len(notices) == 2
    assert notices[0]['kind'] == 'create_proposal'
    assert notices[1]['kind'] == 'create_proposal'


def test_notice_body(db_conn, notices_table):
    """
    Expect to get the notice body.
    """

    notice, errors = insert_notice({
        'user_id': 'abcd1234',
        'kind': 'create_proposal',
        'tags': ['test'],
        'data': {
            'user_name': 'A',
            'proposal_name': 'B',
            'entity_kind': 'C',
            'entity_name': 'D',
        }
    }, db_conn)
    body = get_notice_body(notice)
    assert body == "A created a new proposal, B, for C D."


def test_deliver_notice(db_conn, notices_table):
    """
    Expect to get the notice body.
    """

    notice, errors = insert_notice({
        'user_id': 'abcd1234',
        'kind': 'create_proposal',
        'tags': ['test'],
        'data': {
            'user_name': 'A',
            'proposal_name': 'B',
            'entity_kind': 'C',
            'entity_name': 'D',
        }
    }, db_conn)
    fields = deliver_notice(notice)
    assert fields['user_id'] == 'abcd1234'
    assert fields['body'] == "A created a new proposal, B, for C D."


def test_mark_as_read(db_conn, notices_table):
    """
    Expect to mark a notice as read.
    """

    notice, errors = insert_notice({
        'user_id': 'abcd1234',
        'kind': 'create_proposal',
        'tags': ['test']
    }, db_conn)
    assert notice['read'] is False
    notice, errors = mark_notice_as_read(notice, db_conn)
    assert len(errors) == 0
    assert notice['read'] is True
    record = notices_table.filter({'user_id': 'abcd1234'}).run(db_conn)
    record = list(record)[0]
    assert record['read'] is True


def test_mark_unread(db_conn, notices_table):
    """
    Expect to mark as unread.
    """

    notice, errors = insert_notice({
        'user_id': 'abcd1234',
        'kind': 'create_proposal',
        'tags': ['test'],
        'read': True
    }, db_conn)
    assert notice['read'] is True
    notice, errors = mark_notice_as_unread(notice, db_conn)
    assert len(errors) == 0
    assert notice['read'] is False
    record = notices_table.filter({'user_id': 'abcd1234'}).run(db_conn)
    record = list(record)[0]
    assert record['read'] is False
