from passlib.hash import bcrypt
from conftest import create_user_in_db
import routes.user
import pytest
from database.user import get_user, get_email_token

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
    user = get_user({'id': 'abcd1234'}, db_conn)
    pw1 = user['password']
    get_email_token(user, send_email=False)

    request = {
        'params': {
            'token': 'qza',
            'password': 'qwer1234'
        },
        'db_conn': db_conn
    }
    code, response = routes.user.create_password_route(request, 'abcd1234')
    assert code == 403
    user = get_user({'id': 'abcd1234'}, db_conn)
    assert user['password'] == pw1


def test_user_create_password_ok(db_conn, users_table):
    """
    Expect a user to be able to reset their password.
    """

    create_user_in_db(users_table, db_conn)
    user = get_user({'id': 'abcd1234'}, db_conn)
    pw1 = user['password']
    token = get_email_token(user, send_email=False)

    request = {
        'params': {
            'token': token,
            'password': 'qwer1234'
        },
        'db_conn': db_conn
    }
    code, response = routes.user.create_password_route(request, 'abcd1234')
    assert code == 200
    user = get_user({'id': 'abcd1234'}, db_conn)
    assert user['password'] != pw1
