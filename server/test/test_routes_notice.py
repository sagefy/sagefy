from models.notice import Notice
import routes.notice
import pytest

xfail = pytest.mark.xfail


def test_list(db_conn, session, notices_table):
    """
    Expect to get a list of 10 notices by user ID.
    """
    for i in range(0, 10):
        Notice.insert(db_conn, {
            'user_id': 'abcd1234',
            'kind': 'create_proposal',
            'data': {
                'user_name': '',
                'proposal_name': '',
                'entity_kind': '',
                'entity_name': '',
            }
        })

    request = {
        'cookies': {'session_id': session},
        'params': {},
        'db_conn': db_conn,
    }
    code, response = routes.notice.list_notices_route(request)
    assert code == 200
    assert len(response['notices']) == 10
    assert 'user_id' in response['notices'][0]


def test_list_no_user(db_conn):
    """
    Expect to get an error if not logged in.
    """

    request = {
        'params': {},
        'db_conn': db_conn
    }
    code, response = routes.notice.list_notices_route(request)
    assert code == 401


def test_list_paginate(db_conn, session, notices_table):
    """
    Expect to paginate lists of notices.
    """

    for i in range(0, 25):
        Notice.insert(db_conn, {
            'user_id': 'abcd1234',
            'kind': 'create_proposal',
            'data': {
                'user_name': '',
                'proposal_name': '',
                'entity_kind': '',
                'entity_name': '',
            }
        })

    request = {
        'cookies': {'session_id': session},
        'params': {},
        'db_conn': db_conn,
    }
    code, response = routes.notice.list_notices_route(request)
    assert len(response['notices']) == 10
    request.update({'params': {'skip': 10}})
    code, response = routes.notice.list_notices_route(request)
    assert len(response['notices']) == 10
    request.update({'params': {'skip': 20}})
    code, response = routes.notice.list_notices_route(request)
    assert len(response['notices']) == 5


def test_mark(db_conn, session, notices_table):
    """
    Expect to mark a notice as read.
    """
    notice, errors = Notice.insert(db_conn, {
        'user_id': 'abcd1234',
        'kind': 'create_proposal',
        'data': {
            'user_name': '',
            'proposal_name': '',
            'entity_kind': '',
            'entity_name': '',
        }
    })
    nid = notice['id']

    request = {
        'cookies': {'session_id': session},
        'params': {'read': True},
        'db_conn': db_conn
    }
    code, response = routes.notice.mark_notice_route(request, nid)
    assert code == 200
    assert response['notice']['read'] is True
    record = notices_table.get(nid).run(db_conn)
    assert record['read'] is True


def test_mark_no_user(db_conn, notices_table):
    """
    Expect to error on not logged in when marking as read.
    """
    notice, errors = Notice.insert(db_conn, {
        'user_id': 'abcd1234',
        'kind': 'create_proposal',
        'data': {
            'user_name': '',
            'proposal_name': '',
            'entity_kind': '',
            'entity_name': '',
        }
    })
    nid = notice['id']

    request = {
        'params': {'read': True},
        'db_conn': db_conn
    }
    code, response = routes.notice.mark_notice_route(request, nid)
    assert code == 401
    record = notices_table.get(nid).run(db_conn)
    assert record['read'] is False


def test_mark_no_notice(db_conn, session, notices_table):
    """
    Expect to error on no notice in when marking as read.
    """

    request = {
        'cookies': {'session_id': session},
        'params': {'read': True},
        'db_conn': db_conn,
    }
    code, response = (routes.notice
                      .mark_notice_route(request, 'abcd1234'))
    assert code == 404


def test_mark_not_owned(db_conn, session, notices_table):
    """
    Expect to error when not own notice when marking as read.
    """
    notice, errors = Notice.insert(db_conn, {
        'user_id': '1234abcd',
        'kind': 'create_proposal',
        'data': {
            'user_name': '',
            'proposal_name': '',
            'entity_kind': '',
            'entity_name': '',
        }
    })
    nid = notice['id']

    request = {
        'cookies': {'session_id': session},
        'params': {'read': True},
        'db_conn': db_conn,
    }
    code, response = routes.notice.mark_notice_route(request, nid)
    assert code == 403
    record = notices_table.get(nid).run(db_conn)
    assert record['read'] is False


@xfail
def test_add_notices(db_conn, session, notices_table):
    """
    Expect to add body to notices.
    """

    assert False
