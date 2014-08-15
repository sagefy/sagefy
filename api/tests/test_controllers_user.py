from passlib.hash import bcrypt
import json
import rethinkdb as r
import pytest


def create_user_in_db(users_table, db_conn):
    return users_table.insert({
        'id': 'abcd1234',
        'name': 'test',
        'email': 'test@example.com',
        'password': bcrypt.encrypt('abcd1234'),
        'created': r.now(),
        'modified': r.now()
    }).run(db_conn)


def login(c):
    return c.post('/api/users/login', data=json.dumps({
        'name': 'test',
        'password': 'abcd1234'
    }), content_type='application/json', follow_redirects=True)


def logout(c):
    return c.post('/api/users/logout', data=json.dumps({}),
                  content_type='application/json',
                  follow_redirects=True)


def test_user_get(app, db_conn, users_table):
    """
    Ensure a user can be retrieved by ID.
    """
    create_user_in_db(users_table, db_conn)
    response = app.test_client().get('/api/users/abcd1234')
    assert 'test' in response.data


def test_user_get_failed(app, db_conn, users_table):
    """
    Ensure a no user is returned when ID doesn't match.
    """
    response = app.test_client().get('/api/users/abcd1234')
    assert 'errors' in response.data


def test_user_login(app, db_conn, users_table):
    """
    Ensure a user can login.
    """
    create_user_in_db(users_table, db_conn)
    with app.test_client() as c:
        response = login(c)
        assert 'test@example.com' in response.data


def test_user_login_none(app, db_conn, users_table):
    """
    Ensure a user can't login if no user by name.
    """
    with app.test_client() as c:
        response = login(c)
        assert 'errors' in response.data


def test_user_login_password_fail(app, db_conn, users_table):
    """
    Ensure a user can't login if password is wrong.
    """
    create_user_in_db(users_table, db_conn)
    response = app.test_client().post('/api/users/login', data=json.dumps({
        'name': 'test',
        'password': '1234abcd'
    }), content_type='application/json', follow_redirects=True)
    assert 'errors' in response.data


def test_user_logout(app, db_conn, users_table):
    """
    Ensure a user can log out.
    """
    create_user_in_db(users_table, db_conn)
    with app.test_client() as c:
        with c.session_transaction() as sess:
            sess['user_id'] = 'abcd1234'
            sess['_fresh'] = True
        response = logout(c)
        assert response.status_code == 204


def test_user_get_current(app, db_conn, users_table):
    """
    Ensure the current user can be retrieved.
    """
    create_user_in_db(users_table, db_conn)
    with app.test_client() as c:
        with c.session_transaction() as sess:
            sess['user_id'] = 'abcd1234'
            sess['_fresh'] = True
        response = c.get('/api/users/current')
        assert 'test' in response.data


def test_user_get_current_failed(app, db_conn, users_table):
    """
    Ensure no user is returned when logged out.
    """
    response = app.test_client().get('/api/users/abcd1234')
    assert 'errors' in response.data


def test_user_create(app, db_conn, users_table):
    """
    Ensure a user can be created.
    """
    response = app.test_client().post('/api/users/', data=json.dumps({
        'name': 'test',
        'email': 'test@example.com',
        'password': 'abcd1234',
    }), content_type='application/json')
    assert 'test' in response.data


def test_user_create_failed(app, db_conn, users_table):
    """
    Ensure a user will fail to create when invalid.
    """
    response = app.test_client().post('/api/users/', data=json.dumps({}),
                                      content_type='application/json')
    assert 'errors' in response.data


@pytest.mark.xfail
def test_user_update(app, db_conn, users_table):
    """
    Ensure a user can be updated.
    """
    create_user_in_db(users_table, db_conn)
    with app.test_client() as c:
        with c.session_transaction() as sess:
            sess['user_id'] = 'abcd1234'
            sess['_fresh'] = True
        response = c.put('/api/users/abcd1234', data=json.dumps({
            'email': 'other@example.com'
        }), content_type='application/json')
        assert 'other@example.com' in response.data


def test_user_update_none(app, db_conn, users_table):
    """
    Ensure a user won't update if not exist.
    """
    response = app.test_client().put('/api/users/abcd1234', data=json.dumps({
        'email': 'other@example.com'
    }), content_type='application/json')
    assert 'errors' in response.data


def test_user_update_self_only(app, db_conn, users_table):
    """
    Ensure a user can only update herself.
    """
    users_table.insert({
        'id': '1234abcd',
        'name': 'other',
        'email': 'other@example.com',
        'password': bcrypt.encrypt('1234abcd'),
    }).run(db_conn)
    create_user_in_db(users_table, db_conn)
    with app.test_client() as c:
        with c.session_transaction() as sess:
            sess['user_id'] = 'abcd1234'
            sess['_fresh'] = True
        response = c.put('/api/users/1234abcd', data=json.dumps({
            'email': 'other@example.com'
        }), content_type='application/json')
        assert 'errors' in response.data


def test_user_update_invalid(app, db_conn, users_table):
    """
    Ensure a user won't update if invalid.
    """
    create_user_in_db(users_table, db_conn)
    with app.test_client() as c:
        with c.session_transaction() as sess:
            sess['user_id'] = 'abcd1234'
            sess['_fresh'] = True
        response = c.put('/api/users/abcd1234', data=json.dumps({
            'email': 'other'
        }), content_type='application/json')
        assert 'errors' in response.data
