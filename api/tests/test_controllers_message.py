import pytest
import rethinkdb as r
from test_controllers_user import create_user_in_db, login, logout
import json
from models.message import Message


def test_list_login(app, db_conn, messages_table):
    """
    Expect to require login to list messages.
    """
    with app.test_client() as c:
        response = c.get('/api/messages/')
        assert response.status_code == 401


def test_list_member(app, db_conn, users_table, messages_table):
    """
    Expect to require user to be member to list messages.
    """
    create_user_in_db(users_table, db_conn)
    with app.test_client() as c:
        login(c)
        response = c.get('/api/messages/', data=json.dumps({
            'to_user_id': '5687abvd',
        }), content_type='application/json')
        assert response.status_code == 403
        assert json.loads(response.data.decode('utf-8'))\
            ['errors'][0]['message'] == \
            'Not own message.'
        logout(c)


def test_list_messages(app, db_conn, users_table, messages_table):
    """
    Expect to list messages.
    """
    create_user_in_db(users_table, db_conn)
    Message.insert({'from_user_id': 'a', 'to_user_id': 'abcd1234',
                    'name': 'a', 'body': 'b'})
    Message.insert({'from_user_id': 'b', 'to_user_id': 'abcd1234',
                    'name': 'ra', 'body': 'rb'})
    Message.insert({'from_user_id': 'abcd1234', 'to_user_id': 'd',
                    'name': 'da', 'body': 'qb'})
    Message.insert({'from_user_id': 'c', 'to_user_id': 'd',
                    'name': 'ca', 'body': 'gb'})
    with app.test_client() as c:
        login(c)
        response = c.get('/api/messages/', data=json.dumps({
            'to_user_id': 'abcd1234',
        }), content_type='application/json')
        assert response.status_code == 200
        response = json.loads(response.data.decode('utf-8'))
        assert len(response['messages']) == 2
        assert response['messages'][0]['to_user_id'] == 'abcd1234'
        logout(c)


def test_list_paginate(app, db_conn, users_table, messages_table):
    """
    Expect to paginate listed messages.
    """
    for i in range(0, 25):
        Message.insert({'from_user_id': 'a', 'to_user_id': 'abcd1234',
                        'name': 'a%s' % i, 'body': 'b%s' % i})
    create_user_in_db(users_table, db_conn)
    with app.test_client() as c:
        login(c)
        response = c.get('/api/messages/', data=json.dumps({
            'to_user_id': 'abcd1234',
        }), content_type='application/json')
        response = json.loads(response.data.decode('utf-8'))
        assert len(response['messages']) == 10
        response = c.get('/api/messages/', data=json.dumps({
            'to_user_id': 'abcd1234',
            'skip': 20,
        }), content_type='application/json')
        response = json.loads(response.data.decode('utf-8'))
        assert len(response['messages']) == 5
        logout(c)


def test_get_login(app, db_conn, messages_table):
    """
    Expect to require login to get a message.
    """
    with app.test_client() as c:
        response = c.get('/api/messages/abcd1234')
        assert response.status_code == 401


def test_get_none(app, db_conn, users_table, messages_table):
    """
    Expect to 404 if no matching message.
    """
    create_user_in_db(users_table, db_conn)
    with app.test_client() as c:
        login(c)
        response = c.get('/api/messages/abcd1234')
        assert response.status_code == 404
        logout(c)


def test_get_member(app, db_conn, users_table, messages_table):
    """
    Expect to require user to be member to get message.
    """
    message, errors = Message.insert({
        'to_user_id': '56',
        'from_user_id': '89',
        'name': 'a',
        'body': 'b',
    })
    create_user_in_db(users_table, db_conn)
    with app.test_client() as c:
        login(c)
        response = c.get('/api/messages/%s' % message.id)
        assert response.status_code == 403
        logout(c)


def test_get(app, db_conn, users_table, messages_table):
    """
    Expect to get a message.
    """
    message, errors = Message.insert({
        'to_user_id': 'abcd1234',
        'from_user_id': '89',
        'name': 'a',
        'body': 'b',
    })
    create_user_in_db(users_table, db_conn)
    with app.test_client() as c:
        login(c)
        response = c.get('/api/messages/%s' % message.id)
        assert response.status_code == 200
        response = json.loads(response.data.decode('utf-8'))
        assert response['message']['name'] == 'a'
        logout(c)


def test_mark_login(app, db_conn, messages_table):
    """
    Expect to require login to mark message as read.
    """
    with app.test_client() as c:
        response = c.put('/api/messages/abcd1234/read')
        assert response.status_code == 401


def test_mark_none(app, db_conn, users_table, messages_table):
    """
    Expect to 404 if no matching message when marking as read.
    """
    create_user_in_db(users_table, db_conn)
    with app.test_client() as c:
        login(c)
        response = c.put('/api/messages/abcd1234/read')
        assert response.status_code == 404
        logout(c)


def test_mark_member(app, db_conn, users_table, messages_table):
    """
    Expect to require own message to mark as read.
    """
    message, errors = Message.insert({
        'to_user_id': '56',
        'from_user_id': '89',
        'name': 'a',
        'body': 'b',
    })
    create_user_in_db(users_table, db_conn)
    with app.test_client() as c:
        login(c)
        response = c.put('/api/messages/%s/read' % message.id)
        assert response.status_code == 403
        logout(c)


def test_mark(app, db_conn, users_table, messages_table):
    """
    Expect to mark a message as read.
    """
    message, errors = Message.insert({
        'to_user_id': 'abcd1234',
        'from_user_id': '89',
        'name': 'a',
        'body': 'b',
    })
    record = messages_table.get(message.id).run(db_conn)
    assert record['read'] is False
    create_user_in_db(users_table, db_conn)
    with app.test_client() as c:
        login(c)
        response = c.put('/api/messages/%s/read' % message.id)
        assert response.status_code == 200
        response = json.loads(response.data.decode('utf-8'))
        assert response['message']['name'] == 'a'
        record = messages_table.get(message.id).run(db_conn)
        assert record['read'] is True
        logout(c)


def test_create_login(app, db_conn, messages_table):
    """
    Expect to require login to create a message.
    """
    with app.test_client() as c:
        response = c.post('/api/messages/', data=json.dumps({
            'to_user_id': '5678',
            'name': 'Yo!',
            'body': 'How\'s it goin\'?',
        }), content_type='application/json')
        assert response.status_code == 401


def test_create_error(app, db_conn, users_table, messages_table):
    """
    Expect to show errors if error when insert message.
    """
    create_user_in_db(users_table, db_conn)
    with app.test_client() as c:
        login(c)
        response = c.post('/api/messages/', data=json.dumps({
            'to_user_id': '5678',
        }), content_type='application/json')
        assert response.status_code == 400
        response = json.loads(response.data.decode('utf-8'))
        assert len(response['errors']) == 2
        logout(c)


def test_create(app, db_conn, users_table, messages_table):
    """
    Expect to create a message.
    With the correct from user.
    """
    create_user_in_db(users_table, db_conn)
    with app.test_client() as c:
        login(c)
        response = c.post('/api/messages/', data=json.dumps({
            'to_user_id': '5678',
            'name': 'Yo!',
            'body': 'How\'s it goin\'?',
        }), content_type='application/json')
        assert response.status_code == 200
        response = json.loads(response.data.decode('utf-8'))
        assert response['message']['name'] == 'Yo!'
        logout(c)
