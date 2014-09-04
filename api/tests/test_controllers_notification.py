from test_controllers_user import create_user_in_db, login, logout
import json
from models.notification import Notification


def test_list(app, db_conn, users_table, notifications_table):
    """
    Expect to get a list of 10 notifications by user ID.
    """
    create_user_in_db(users_table, db_conn)
    for i in range(0, 10):
        Notification.insert({
            'user_id': 'abcd1234',
            'body': 'b',
        })
    with app.test_client() as c:
        response = login(c)
        response = c.get('/api/notifications/')
        assert response.status_code == 200
        response = json.loads(response.data)
        assert len(response['notifications']) == 10
        assert 'user_id' in response['notifications'][0]
        logout(c)


def test_list_no_user(app, db_conn):
    """
    Expect to get an error if not logged in.
    """
    with app.test_client() as c:
        response = c.get('/api/notifications/')
        assert response.status_code == 401


def test_list_paginate(app, db_conn, users_table, notifications_table):
    """
    Expect to paginate lists of notifications.
    """
    create_user_in_db(users_table, db_conn)
    for i in range(0, 25):
        Notification.insert({
            'user_id': 'abcd1234',
            'body': 'b',
        })
    with app.test_client() as c:
        response = login(c)
        response = c.get('/api/notifications/')
        response = json.loads(response.data)
        assert len(response['notifications']) == 10
        response = c.get('/api/notifications/', data=json.dumps({
            'skip': 20,
        }), content_type='application/json')
        response = json.loads(response.data)
        assert len(response['notifications']) == 5
        logout(c)


def test_mark(app, db_conn, users_table, notifications_table):
    """
    Expect to mark a notification as read.
    """
    create_user_in_db(users_table, db_conn)
    notification, errors = Notification.insert({
        'user_id': 'abcd1234',
        'body': 'b',
    })
    nid = notification.id
    with app.test_client() as c:
        response = login(c)
        response = c.put('/api/notifications/%s/read' % nid)
        assert response.status_code == 200
        response = json.loads(response.data)
        assert response['notification']['read'] is True
        record = notifications_table.get(nid).run(db_conn)
        assert record['read'] is True
        logout(c)


def test_mark_no_user(app, db_conn, notifications_table):
    """
    Expect to error on not logged in when marking as read.
    """
    notification, errors = Notification.insert({
        'user_id': 'abcd1234',
        'body': 'b',
    })
    nid = notification.id
    with app.test_client() as c:
        response = c.put('/api/notifications/%s/read' % nid)
        assert response.status_code == 401
        record = notifications_table.get(nid).run(db_conn)
        assert record['read'] is False


def test_mark_no_notification(app, db_conn, users_table, notifications_table):
    """
    Expect to error on no notification in when marking as read.
    """
    create_user_in_db(users_table, db_conn)
    with app.test_client() as c:
        response = login(c)
        response = c.put('/api/notifications/abcd1234/read')
        assert response.status_code == 404
        response = json.loads(response.data)
        logout(c)


def test_mark_not_owned(app, db_conn, users_table, notifications_table):
    """
    Expect to error when not own notification when marking as read.
    """
    create_user_in_db(users_table, db_conn)
    notification, errors = Notification.insert({
        'user_id': '1234abcd',
        'body': 'b',
    })
    nid = notification.id
    with app.test_client() as c:
        response = login(c)
        response = c.put('/api/notifications/%s/read' % nid)
        assert response.status_code == 403
        record = notifications_table.get(nid).run(db_conn)
        assert record['read'] is False
        logout(c)
