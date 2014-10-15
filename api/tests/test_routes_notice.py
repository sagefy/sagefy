from test_routes_user import create_user_in_db, login, logout
import json
from models.notice import Notice


def test_list(app, db_conn, users_table, notices_table):
    """
    Expect to get a list of 10 notices by user ID.
    """
    create_user_in_db(users_table, db_conn)
    for i in range(0, 10):
        Notice.insert({
            'user_id': 'abcd1234',
            'body': 'b',
        })
    with app.test_client() as c:
        response = login(c)
        response = c.get('/api/notices/')
        assert response.status_code == 200
        response = json.loads(response.data.decode('utf-8'))
        assert len(response['notices']) == 10
        assert 'user_id' in response['notices'][0]
        logout(c)


def test_list_no_user(app, db_conn):
    """
    Expect to get an error if not logged in.
    """
    with app.test_client() as c:
        response = c.get('/api/notices/')
        assert response.status_code == 401


def test_list_paginate(app, db_conn, users_table, notices_table):
    """
    Expect to paginate lists of notices.
    """
    create_user_in_db(users_table, db_conn)
    for i in range(0, 25):
        Notice.insert({
            'user_id': 'abcd1234',
            'body': 'b',
        })
    with app.test_client() as c:
        response = login(c)
        response = c.get('/api/notices/')
        response = json.loads(response.data.decode('utf-8'))
        assert len(response['notices']) == 10
        response = c.get('/api/notices/?skip=20')
        response = json.loads(response.data.decode('utf-8'))
        assert len(response['notices']) == 5
        logout(c)


def test_mark(app, db_conn, users_table, notices_table):
    """
    Expect to mark a notice as read.
    """
    create_user_in_db(users_table, db_conn)
    notice, errors = Notice.insert({
        'user_id': 'abcd1234',
        'body': 'b',
    })
    nid = notice.id
    with app.test_client() as c:
        response = login(c)
        response = c.put('/api/notices/%s/read/' % nid)
        assert response.status_code == 200
        response = json.loads(response.data.decode('utf-8'))
        assert response['notice']['read'] is True
        record = notices_table.get(nid).run(db_conn)
        assert record['read'] is True
        logout(c)


def test_mark_no_user(app, db_conn, notices_table):
    """
    Expect to error on not logged in when marking as read.
    """
    notice, errors = Notice.insert({
        'user_id': 'abcd1234',
        'body': 'b',
    })
    nid = notice.id
    with app.test_client() as c:
        response = c.put('/api/notices/%s/read/' % nid)
        assert response.status_code == 401
        record = notices_table.get(nid).run(db_conn)
        assert record['read'] is False


def test_mark_no_notice(app, db_conn, users_table, notices_table):
    """
    Expect to error on no notice in when marking as read.
    """
    create_user_in_db(users_table, db_conn)
    with app.test_client() as c:
        response = login(c)
        response = c.put('/api/notices/abcd1234/read/')
        assert response.status_code == 404
        response = json.loads(response.data.decode('utf-8'))
        logout(c)


def test_mark_not_owned(app, db_conn, users_table, notices_table):
    """
    Expect to error when not own notice when marking as read.
    """
    create_user_in_db(users_table, db_conn)
    notice, errors = Notice.insert({
        'user_id': '1234abcd',
        'body': 'b',
    })
    nid = notice.id
    with app.test_client() as c:
        response = login(c)
        response = c.put('/api/notices/%s/read/' % nid)
        assert response.status_code == 403
        record = notices_table.get(nid).run(db_conn)
        assert record['read'] is False
        logout(c)
