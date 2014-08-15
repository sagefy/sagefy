from passlib.hash import bcrypt


def create_user_in_db(users_table, db_conn):
    return users_table.insert({
        'id': 'abcd1234',
        'name': 'test',
        'email': 'test@example.com',
        'password': bcrypt.encrypt('abcd1234'),
    }).run(db_conn)


def login(app):
    return app.test_client().post('/api/users/login', data={
        'name': 'test',
        'password': 'abcd1234'
    }, follow_redirects=True)


def logout(app):
    return app.test_client().post('/api/users/logout', follow_redirects=True)


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
    assert '404' in response.data


def test_user_login(app, db_conn, users_table):
    """
    Ensure a user can login.
    """
    create_user_in_db(users_table, db_conn)
    response = login(app)
    assert 'logged_in' in response.data
    logout(app)


def test_user_login_none(app, db_conn, users_table):
    """
    Ensure a user can't login if no user by name.
    """
    response = login(app)
    assert '404' in response.data


def test_user_login_password_fail(app, db_conn, users_table):
    """
    Ensure a user can't login if password is wrong.
    """
    create_user_in_db(users_table, db_conn)
    response = app.test_client().post('/api/users/login', data={
        'name': 'test',
        'password': '1234abcd'
    }, follow_redirects=True)
    assert '404' in response.data


def test_user_logout(app, db_conn, users_table):
    """
    Ensure a user can log out.
    """
    create_user_in_db(users_table, db_conn)
    login(app)
    response = logout(app)
    assert '204' in response.data


def test_user_get_current(app, db_conn, users_table):
    """
    Ensure the current user can be retrieved.
    """
    create_user_in_db(users_table, db_conn)
    login(app)
    response = app.test_client().get('/api/users/abcd1234')
    assert 'test' in response.data


def test_user_get_current_failed(app, db_conn, users_table):
    """
    Ensure no user is returned when logged out.
    """
    response = app.test_client().get('/api/users/abcd1234')
    assert '404' in response.data


def test_user_create(app, db_conn, users_table):
    """
    Ensure a user can be created.
    """
    response = app.test_client().post('/api/users', data={
        'name': 'test',
        'email': 'test@example.com',
        'password': 'abcd1234',
    })
    assert 'test' in response.data


def test_user_create_failed(app, db_conn, users_table):
    """
    Ensure a user will fail to create when invalid.
    """
    response = app.test_client().post('/api/users')
    assert 'errors' in response.data


def test_user_update(app, db_conn, users_table):
    """
    Ensure a user can be updated.
    """
    create_user_in_db(users_table, db_conn)
    login(app)
    response = app.test_client().put('/api/users/abcd1234', data={
        'email': 'other@example.com'
    })
    assert 'other@example.com' in response.data


def test_user_update_none(app, db_conn, users_table):
    """
    Ensure a user won't update if not exist.
    """
    response = app.test_client().put('/api/users/abcd1234', data={
        'email': 'other@example.com'
    })
    assert '404' in response.data


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
    login(app)
    response = app.test_client().put('/api/users/1234abcd', data={
        'email': 'other@example.com'
    })
    assert '401' in response.data


def test_user_update_invalid(app, db_conn, users_table):
    """
    Ensure a user won't update if invalid.
    """
    create_user_in_db(users_table, db_conn)
    login(app)
    response = app.test_client().put('/api/users/abcd1234', data={
        'email': 'other'
    })
    assert 'errors' in response.data
