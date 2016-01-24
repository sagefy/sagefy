from passlib.hash import bcrypt
from models.user import User
from conftest import create_user_in_db
import rethinkdb as r
import routes.user
import pytest

xfail = pytest.mark.xfail


def test_user_get(db_conn, users_table):
    """
    Ensure a user can be retrieved by ID.
    """

    create_user_in_db(users_table, db_conn)
    request = {'params': {}, 'db_conn': db_conn}
    code, response = routes.user.get_user_route(request, 'abcd1234')
    assert response['user']['name'] == 'test'


def test_user_get_failed(db_conn, users_table):
    """
    Ensure a no user is returned when ID doesn't match.
    """

    request = {'params': {}, 'db_conn': db_conn}
    code, response = routes.user.get_user_route(request, 'abcd1234')
    assert 'errors' in response


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

    request = {
        'params': {'posts': True},
        'cookies': {'session_id': session},
        'db_conn': db_conn
    }
    code, response = routes.user.get_user_route(request, 'abcd1234')
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
        'status': 'accepted',
    }, {
        'entity_id': 'B2',
        'name': 'B',
        'body': 'Banana',
        'created': r.now(),
        'modified': r.now(),
        'status': 'accepted',
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

    request = {
        'params': {'sets': True},
        'cookies': {'session_id': session},
        'db_conn': db_conn
    }
    code, response = routes.user.get_user_route(request, 'abcd1234')
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

    request = {
        'params': {'follows': True},
        'cookies': {'session_id': session},
        'db_conn': db_conn
    }
    code, response = routes.user.get_user_route(request, 'abcd1234')
    assert 'follows' in response
    assert len(response['follows']) == 1


def test_user_log_in(db_conn, users_table):
    """
    Ensure a user can log in.
    """

    create_user_in_db(users_table, db_conn)
    request = {
        'params': {'name': 'test', 'password': 'abcd1234'},
        'db_conn': db_conn
    }
    code, response = routes.user.log_in_route(request)
    assert 'test@example.com' == response['user']['email']


def test_user_log_in_none(db_conn, users_table):
    """
    Ensure a user can't log in if no user by name.
    """

    request = {
        'params': {'name': 'test', 'password': 'abcd1234'},
        'db_conn': db_conn
    }
    code, response = routes.user.log_in_route(request)
    assert 'errors' in response


def test_user_log_in_password_fail(db_conn, users_table):
    """
    Ensure a user can't log in if password is wrong.
    """

    create_user_in_db(users_table, db_conn)
    request = {
        'params': {'name': 'test', 'password': '1234abcd'},
        'db_conn': db_conn
    }
    code, response = routes.user.log_in_route(request)
    assert 'errors' in response


def test_user_log_out(db_conn, users_table):
    """
    Ensure a user can log out.
    """

    create_user_in_db(users_table, db_conn)
    request = {
        'params': {'name': 'test', 'password': 'abcd1234'},
        'db_conn': db_conn
    }
    code, response = routes.user.log_in_route(request)
    assert code == 200
    session_id = response['cookies']['session_id']
    request = {'cookies': {'session_id': session_id}}
    code, response = routes.user.log_out_route(request)
    assert code == 200
    assert 'cookies' in response


def test_user_get_current(session, db_conn):
    """
    Ensure the current user can be retrieved.
    """

    request = {'cookies': {'session_id': session}, 'db_conn': db_conn}
    code, response = routes.user.get_current_user_route(request)
    assert response['user']['name'] == 'test'


def test_user_get_current_failed(db_conn, users_table):
    """
    Ensure no user is returned when logged out.
    """

    code, response = routes.user.get_current_user_route({})
    assert code == 401


def test_user_create(db_conn, users_table):
    """
    Ensure a user can be created.
    """

    request = {
        'params': {
            'name': 'test',
            'email': 'test@example.com',
            'password': 'abcd1234',
        },
        'db_conn': db_conn
    }
    code, response = routes.user.create_user_route(request)
    assert code == 200
    assert response['user']['name'] == 'test'


def test_user_create_failed(db_conn, users_table):
    """
    Ensure a user will fail to create when invalid.
    """

    request = {
        'params': {},
        'db_conn': db_conn
    }
    code, response = routes.user.create_user_route(request)
    assert 'errors' in response


def test_user_update(session, db_conn):
    """
    Ensure a user can be updated.
    """

    request = {
        'params': {
            'email': 'other@example.com'
        },
        'cookies': {
            'session_id': session,
        },
        'db_conn': db_conn
    }
    code, response = routes.user.update_user_route(request, 'abcd1234')
    assert code == 200
    assert response['user']['email'] == 'other@example.com'


def test_user_update_none(db_conn, users_table):
    """
    Ensure a user won't update if not exist.
    """

    request = {
        'params': {
            'email': 'other@example.com'
        },
        'cookies': {
            'session_id': 'fjsknl',
        },
        'db_conn': db_conn
    }
    code, response = routes.user.update_user_route(request, 'abcd1234')
    assert 'errors' in response


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

    request = {
        'params': {
            'email': 'other@example.com'
        },
        'cookies': {
            'session_id': session,
        },
        'db_conn': db_conn
    }
    code, response = routes.user.update_user_route(request, '1234abcd')
    assert 'errors' in response


def test_user_update_invalid(db_conn, users_table, session):
    """
    Ensure a user won't update if invalid.
    """

    request = {
        'params': {
            'email': 'other'
        },
        'cookies': {
            'session_id': session,
        },
        'db_conn': db_conn
    }
    code, response = routes.user.update_user_route(request, 'abcd1234')
    assert 'errors' in response


def test_user_token_fail(db_conn, users_table):
    """
    Expect to create a token so the user can get a new password.
    """

    create_user_in_db(users_table, db_conn)
    request = {'params': {'email': 'other'}, 'db_conn': db_conn}
    code, response = routes.user.create_token_route(request)
    assert code == 404


def test_user_token_success(db_conn, users_table):
    """
    Expect to create a token so the user can get a new password.
    """

    create_user_in_db(users_table, db_conn)
    request = {'params': {'email': 'test@example.com'}, 'db_conn': db_conn}
    code, response = routes.user.create_token_route(request)
    assert code == 200


def test_user_create_password_fail(db_conn, users_table):
    """
    Expect a user to be able to reset their password.
    """

    create_user_in_db(users_table, db_conn)
    user = User.get(db_conn, id='abcd1234')
    pw1 = user['password']
    user.get_email_token(send_email=False)

    request = {
        'params': {
            'token': 'qza',
            'password': 'qwer1234'
        },
        'db_conn': db_conn
    }
    code, response = routes.user.create_password_route(request, 'abcd1234')
    assert code == 403
    user.sync(db_conn)
    assert user['password'] == pw1


def test_user_create_password_ok(db_conn, users_table):
    """
    Expect a user to be able to reset their password.
    """

    create_user_in_db(users_table, db_conn)
    user = User.get(db_conn, id='abcd1234')
    pw1 = user['password']
    token = user.get_email_token(send_email=False)

    request = {
        'params': {
            'token': token,
            'password': 'qwer1234'
        },
        'db_conn': db_conn
    }
    code, response = routes.user.create_password_route(request, 'abcd1234')
    assert code == 200
    user.sync(db_conn)
    assert user['password'] != pw1
