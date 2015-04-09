from passlib.hash import bcrypt
import json
from models.user import User
from conftest import create_user_in_db, log_in, log_out
import rethinkdb as r
import pytest

xfail = pytest.mark.xfail


def test_user_get(db_conn, users_table):
    """
    Ensure a user can be retrieved by ID.
    """
    create_user_in_db(users_table, db_conn)
    response = app.test_client().get('/api/users/abcd1234/')
    assert 'test' in response.data.decode()


def test_user_get_failed(db_conn, users_table):
    """
    Ensure a no user is returned when ID doesn't match.
    """
    response = app.test_client().get('/api/users/abcd1234/')
    assert 'errors' in response.data.decode()


def test_get_user_posts(db_conn, session, posts_table):
    """
    Expect to get user's 10 latest posts when requested in addition.
    """

    posts_table.insert([{
        'created': r.now(),
        'modified': r.now(),
        'user_id': 'abcd1234',
        'topic_id': 'fj2Ojfdskl2',
        'body': '''A Modest Proposal for Preventing the Children of Poor
            People From Being a Burthen to Their Parents or Country, and
            for Making Them Beneficial to the Publick.''',
        'kind': 'post',
    }, {
        'created': r.now(),
        'modified': r.now(),
        'user_id': 'gjrklj15431',
        'topic_id': 'fj2Ojfdskl2',
        'body': '''A Modest Proposal for Preventing the Children of Poor
            People From Being a Burthen to Their Parents or Country, and
            for Making Them Beneficial to the Publick.''',
        'kind': 'post',
    }, {
        'created': r.now(),
        'modified': r.now(),
        'user_id': 'abcd1234',
        'topic_id': 'fj2Ojfdskl2',
        'body': '''A Modest Proposal for Preventing the Children of Poor
            People From Being a Burthen to Their Parents or Country, and
            for Making Them Beneficial to the Publick.''',
        'kind': 'post',
    }]).run(db_conn)

    response = session.get('/api/users/abcd1234/?posts')
    response = json.loads(response.data.decode())
    assert 'posts' in response
    assert len(response['posts']) == 2


def test_get_user_sets(db_conn, session, users_sets_table,
                       users_table,  sets_table):
    """
    Expect to get user's sets, if requested and allowed.
    """

    users_table.get('abcd1234').update({
        'settings': {'view_sets': 'public'}
    }).run(db_conn)

    sets_table.insert([{
        'entity_id': 'A1',
        'name': 'A',
        'body': 'Apple',
        'created': r.now(),
        'modified': r.now(),
        'canonical': True,
    }, {
        'entity_id': 'B2',
        'name': 'B',
        'body': 'Banana',
        'created': r.now(),
        'modified': r.now(),
        'canonical': True,
    }]).run(db_conn)

    users_sets_table.insert({
        'user_id': 'abcd1234',
        'set_ids': [
            'A1',
            'B2',
        ],
        'created': r.now(),
        'modified': r.now(),
    }).run(db_conn)

    response = session.get('/api/users/abcd1234/?sets')
    response = json.loads(response.data.decode())
    assert 'sets' in response
    assert len(response['sets']) == 2


def test_get_user_follows(db_conn, session, users_table, follows_table):
    """
    Expect to get user's follows, if requested and allowed.
    """

    users_table.get('abcd1234').update({
        'settings': {'view_follows': 'public'}
    }).run(db_conn)

    follows_table.insert([{
        'id': 'JIkfo034n',
        'user_id': 'abcd1234',
        'entity': {
            'kind': 'card',
            'id': 'JFlsjFm',
        },
        'created': r.now(),
        'modified': r.now(),
    }]).run(db_conn)

    response = session.get('/api/users/abcd1234/?follows')
    response = json.loads(response.data.decode())
    assert 'follows' in response
    assert len(response['follows']) == 1


def test_user_log_in(db_conn, users_table):
    """
    Ensure a user can log in.
    """
    create_user_in_db(users_table, db_conn)
    with app.test_client() as c:
        response = log_in(c)
        assert 'test@example.com' in response.data.decode()


def test_user_log_in_none(db_conn, users_table):
    """
    Ensure a user can't log in if no user by name.
    """
    with app.test_client() as c:
        response = log_in(c)
        assert 'errors' in response.data.decode()


def test_user_log_in_password_fail(db_conn, users_table):
    """
    Ensure a user can't log in if password is wrong.
    """
    create_user_in_db(users_table, db_conn)
    response = app.test_client().post('/api/users/log_in/', data=json.dumps({
        'name': 'test',
        'password': '1234abcd'
    }), content_type='application/json')
    assert 'errors' in response.data.decode()


def test_user_log_out(db_conn, users_table):
    """
    Ensure a user can log out.
    """
    create_user_in_db(users_table, db_conn)
    with app.test_client() as c:
        log_in(c)
        response = log_out(c)
        assert response.status_code == 204


def test_user_get_current(session):
    """
    Ensure the current user can be retrieved.
    """
    response = session.get('/api/users/current/')
    assert 'test' in response.data.decode()


def test_user_get_current_failed(db_conn, users_table):
    """
    Ensure no user is returned when logged out.
    """
    response = app.test_client().get('/api/users/abcd1234/')
    assert 'errors' in response.data.decode()


def test_user_create(db_conn, users_table):
    """
    Ensure a user can be created.
    """
    response = app.test_client().post('/api/users/', data=json.dumps({
        'name': 'test',
        'email': 'test@example.com',
        'password': 'abcd1234',
    }), content_type='application/json')
    assert 'test' in response.data.decode()


def test_user_create_failed(db_conn, users_table):
    """
    Ensure a user will fail to create when invalid.
    """
    response = app.test_client().post('/api/users/', data=json.dumps({}),
                                      content_type='application/json')
    assert 'errors' in response.data.decode()


def test_user_update(session):
    """
    Ensure a user can be updated.
    """
    response = session.put('/api/users/abcd1234/', data=json.dumps({
        'email': 'other@example.com'
    }), content_type='application/json')
    assert 'other@example.com' in response.data.decode()


def test_user_update_none(db_conn, users_table):
    """
    Ensure a user won't update if not exist.
    """
    response = app.test_client().put('/api/users/abcd1234/', data=json.dumps({
        'email': 'other@example.com'
    }), content_type='application/json')
    assert 'errors' in response.data.decode()


def test_user_update_self_only(db_conn, users_table, session):
    """
    Ensure a user can only update herself.
    """
    users_table.insert({
        'id': '1234abcd',
        'name': 'other',
        'email': 'other@example.com',
        'password': bcrypt.encrypt('1234abcd'),
    }).run(db_conn)
    response = session.put('/api/users/1234abcd/', data=json.dumps({
        'email': 'other@example.com'
    }), content_type='application/json')
    assert 'errors' in response.data.decode()


def test_user_update_invalid(db_conn, users_table, session):
    """
    Ensure a user won't update if invalid.
    """
    response = session.put('/api/users/abcd1234/', data=json.dumps({
        'email': 'other'
    }), content_type='application/json')
    assert 'errors' in response.data.decode()


def test_user_token(db_conn, users_table):
    """
    Expect to create a token so the user can get a new password.
    """
    create_user_in_db(users_table, db_conn)
    with app.test_client() as c:
        response = c.post('/api/users/token/', data=json.dumps({
            'email': 'other'
        }), content_type='application/json')
        assert response.status_code == 404
        response = c.post('/api/users/token/', data=json.dumps({
            'email': 'test@example.com'
        }), content_type='application/json')
        assert response.status_code == 204


def test_user_create_password_fail(db_conn, users_table):
    """
    Expect a user to be able to reset their password.
    """
    create_user_in_db(users_table, db_conn)
    user = User.get(id='abcd1234')
    pw1 = user['password']
    user.get_email_token(send_email=False)
    with app.test_client() as c:
        response = c.post('/api/users/password/', data=json.dumps({
            'id': 'abcd1234',
            'token': 'qza',
            'password': 'qwer1234'
        }), content_type='application/json')
        assert response.status_code == 403
        user.sync()
        assert user['password'] == pw1


def test_user_create_password_ok(db_conn, users_table):
    """
    Expect a user to be able to reset their password.
    """
    create_user_in_db(users_table, db_conn)
    user = User.get(id='abcd1234')
    pw1 = user['password']
    token = user.get_email_token(send_email=False)
    with app.test_client() as c:
        response = c.post('/api/users/password/', data=json.dumps({
            'id': 'abcd1234',
            'token': token,
            'password': 'qwer1234'
        }), content_type='application/json')
        assert response.status_code == 200
        user.sync()
        assert user['password'] != pw1
