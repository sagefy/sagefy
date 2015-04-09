import json
from models.notice import Notice
import pytest

xfail = pytest.mark.xfail


def test_list(db_conn, session, notices_table):
    """
    Expect to get a list of 10 notices by user ID.
    """
    for i in range(0, 10):
        Notice.insert({
            'user_id': 'abcd1234',
            'kind': 'new_proposal',
        })
    response = session.get('/api/notices/')
    assert response.status_code == 200
    response = json.loads(response.data.decode())
    assert len(response['notices']) == 10
    assert 'user_id' in response['notices'][0]


def test_list_no_user(db_conn):
    """
    Expect to get an error if not logged in.
    """
    with app.test_client() as c:
        response = c.get('/api/notices/')
        assert response.status_code == 401


def test_list_paginate(db_conn, session, notices_table):
    """
    Expect to paginate lists of notices.
    """
    for i in range(0, 25):
        Notice.insert({
            'user_id': 'abcd1234',
            'kind': 'new_proposal',
        })

    response = session.get('/api/notices/')
    response = json.loads(response.data.decode())
    assert len(response['notices']) == 10
    response = session.get('/api/notices/?skip=10')
    response = json.loads(response.data.decode())
    assert len(response['notices']) == 10
    response = session.get('/api/notices/?skip=20')
    response = json.loads(response.data.decode())
    assert len(response['notices']) == 5


def test_mark(db_conn, session, notices_table):
    """
    Expect to mark a notice as read.
    """
    notice, errors = Notice.insert({
        'user_id': 'abcd1234',
        'kind': 'new_proposal',
    })
    nid = notice['id']
    response = session.put('/api/notices/%s/read/' % nid)
    assert response.status_code == 200
    response = json.loads(response.data.decode())
    assert response['notice']['read'] is True
    record = notices_table.get(nid).run(db_conn)
    assert record['read'] is True


def test_mark_no_user(db_conn, notices_table):
    """
    Expect to error on not logged in when marking as read.
    """
    notice, errors = Notice.insert({
        'user_id': 'abcd1234',
        'kind': 'new_proposal',
    })
    nid = notice['id']
    with app.test_client() as c:
        response = c.put('/api/notices/%s/read/' % nid)
        assert response.status_code == 401
        record = notices_table.get(nid).run(db_conn)
        assert record['read'] is False


def test_mark_no_notice(db_conn, session, notices_table):
    """
    Expect to error on no notice in when marking as read.
    """
    response = session.put('/api/notices/abcd1234/read/')
    assert response.status_code == 404
    response = json.loads(response.data.decode())


def test_mark_not_owned(db_conn, session, notices_table):
    """
    Expect to error when not own notice when marking as read.
    """
    notice, errors = Notice.insert({
        'user_id': '1234abcd',
        'kind': 'new_proposal',
    })
    nid = notice['id']
    response = session.put('/api/notices/%s/read/' % nid)
    assert response.status_code == 403
    record = notices_table.get(nid).run(db_conn)
    assert record['read'] is False


@xfail
def test_add_notices(db_conn, session, notices_table):
    """
    Expect to add body to notices.
    """

    assert False


@xfail
def test_mark_unread(db_conn, session, notices_table):
    """
    Expect to mark as unread.
    """

    assert False
