from passlib.hash import bcrypt
import json
from models.user import User
from conftest import create_user_in_db, log_in, log_out


def test_user_get(app, db_conn, users_table):
    """
    Ensure a user can be retrieved by ID.
    """
    create_user_in_db(users_table, db_conn)
    response = app.test_client().get('/api/users/abcd1234/')
    assert 'test' in response.data.decode()


def test_user_get_failed(app, db_conn, users_table):
    """
    Ensure a no user is returned when ID doesn't match.
    """
    response = app.test_client().get('/api/users/abcd1234/')
    assert 'errors' in response.data.decode()


def test_user_log_in(app, db_conn, users_table):
    """
    Ensure a user can log in.
    """
    create_user_in_db(users_table, db_conn)
    with app.test_client() as c:
        response = log_in(c)
        assert 'test@example.com' in response.data.decode()


def test_user_log_in_none(app, db_conn, users_table):
    """
    Ensure a user can't log in if no user by name.
    """
    with app.test_client() as c:
        response = log_in(c)
        assert 'errors' in response.data.decode()


def test_user_log_in_password_fail(app, db_conn, users_table):
    """
    Ensure a user can't log in if password is wrong.
    """
    create_user_in_db(users_table, db_conn)
    response = app.test_client().post('/api/users/log_in/', data=json.dumps({
        'name': 'test',
        'password': '1234abcd'
    }), content_type='application/json')
    assert 'errors' in response.data.decode()


def test_user_log_out(app, db_conn, users_table):
    """
    Ensure a user can log out.
    """
    create_user_in_db(users_table, db_conn)
    with app.test_client() as c:
        log_in(c)
        response = log_out(c)
        assert response.status_code == 204


def test_user_get_current(c_user):
    """
    Ensure the current user can be retrieved.
    """
    response = c_user.get('/api/users/current/')
    assert 'test' in response.data.decode()


def test_user_get_current_failed(app, db_conn, users_table):
    """
    Ensure no user is returned when logged out.
    """
    response = app.test_client().get('/api/users/abcd1234/')
    assert 'errors' in response.data.decode()


def test_user_create(app, db_conn, users_table):
    """
    Ensure a user can be created.
    """
    response = app.test_client().post('/api/users/', data=json.dumps({
        'name': 'test',
        'email': 'test@example.com',
        'password': 'abcd1234',
    }), content_type='application/json')
    assert 'test' in response.data.decode()


def test_user_create_failed(app, db_conn, users_table):
    """
    Ensure a user will fail to create when invalid.
    """
    response = app.test_client().post('/api/users/', data=json.dumps({}),
                                      content_type='application/json')
    assert 'errors' in response.data.decode()


def test_user_update(c_user):
    """
    Ensure a user can be updated.
    """
    response = c_user.put('/api/users/abcd1234/', data=json.dumps({
        'email': 'other@example.com'
    }), content_type='application/json')
    assert 'other@example.com' in response.data.decode()


def test_user_update_none(app, db_conn, users_table):
    """
    Ensure a user won't update if not exist.
    """
    response = app.test_client().put('/api/users/abcd1234/', data=json.dumps({
        'email': 'other@example.com'
    }), content_type='application/json')
    assert 'errors' in response.data.decode()


def test_user_update_self_only(db_conn, users_table, c_user):
    """
    Ensure a user can only update herself.
    """
    users_table.insert({
        'id': '1234abcd',
        'name': 'other',
        'email': 'other@example.com',
        'password': bcrypt.encrypt('1234abcd'),
    }).run(db_conn)
    response = c_user.put('/api/users/1234abcd/', data=json.dumps({
        'email': 'other@example.com'
    }), content_type='application/json')
    assert 'errors' in response.data.decode()


def test_user_update_invalid(app, db_conn, users_table, c_user):
    """
    Ensure a user won't update if invalid.
    """
    response = c_user.put('/api/users/abcd1234/', data=json.dumps({
        'email': 'other'
    }), content_type='application/json')
    assert 'errors' in response.data.decode()


def test_user_token(app, db_conn, users_table):
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


def test_user_create_password_fail(app, db_conn, users_table):
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


def test_user_create_password_ok(app, db_conn, users_table):
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
