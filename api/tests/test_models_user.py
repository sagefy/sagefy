from models.user import User


def test_user_name_required(app, db_conn):
    """
    Ensure a name is required.
    """
    user = User()
    errors = user.validate()
    assert len(errors) > 0
    assert 'name' in [e['name'] for e in errors]


def test_user_name_unique(app, db_conn, users_table):
    """
    Ensure a name is unique.
    """
    users_table.insert({'name': 'test'}).run(db_conn)
    user, errors = User.insert({
        'name': 'test',
        'email': 'test@example.com',
        'password': 'abcd1234'
    })
    assert len(errors) > 0
    assert 'name' in [e['name'] for e in errors]
    assert 'Must be unique.' in [e['message'] for e in errors]


def test_user_email_required(app, db_conn):
    """
    Ensure an email is required.
    """
    user = User()
    errors = user.validate()
    assert len(errors) > 0
    assert 'email' in [e['name'] for e in errors]


def test_user_email_unique(app, db_conn, users_table):
    """
    Ensure an email is unique.
    """
    users_table.insert({'email': 'test@example.com'}).run(db_conn)
    user, errors = User.insert({
        'name': 'test',
        'email': 'test@example.com',
        'password': 'abcd1234'
    })
    assert len(errors) > 0
    assert 'email' in [e['name'] for e in errors]
    assert 'Must be unique.' in [e['message'] for e in errors]


def test_user_email_format(app, db_conn):
    """
    Ensure an email is formatted.
    """
    user = User({'email': 'other'})
    errors = user.validate()
    assert 'email' in [e['name'] for e in errors]
    assert 'Must be an email.' in [e['message'] for e in errors]


def test_user_password_required(app, db_conn):
    """
    Ensure a password is required.
    """
    user = User()
    errors = user.validate()
    assert len(errors) > 0
    assert 'password' in [e['name'] for e in errors]


def test_user_password_minlength(app, db_conn):
    """
    Ensure an password is long enough.
    """
    user = User({'password': 'abcd'})
    errors = user.validate()
    assert 'password' in [e['name'] for e in errors]
    assert 'Minimum length of 8.' in [e['message'] for e in errors]


def test_user_no_password(app, db_conn, users_table):
    """
    Ensure an password isn't provided ever.
    """
    user, errors = User.insert({
        'name': 'test',
        'email': 'test@example.com',
        'password': 'abcd1234'
    })
    json = user.deliver(private=True)
    assert 'password' not in json


def test_user_email_current(app, db_conn, users_table):
    """
    Ensure an email is only provided when current user.
    """
    user, errors = User.insert({
        'name': 'test',
        'email': 'test@example.com',
        'password': 'abcd1234'
    })
    json = user.deliver(private=False)
    assert 'email' not in json
    json = user.deliver(private=True)
    assert 'email' in json


def test_user_password_encrypt(app, db_conn, users_table):
    """
    Ensure a password is encrypted before going into db.
    """
    user, errors = User.insert({
        'id': 'abcd1234',
        'name': 'test',
        'email': 'test@example.com',
        'password': 'abcd1234'
    })
    assert user.password.bundle().startswith('$2a$')
    assert len(errors) == 0
    assert user.password.get() != 'abcd1234'
    assert user.password.get().startswith('$2a$')


def test_user_password_validate(app, db_conn, users_table):
    """
    Ensure a password can be validated.
    """
    user, errors = User.insert({
        'id': 'abcd1234',
        'name': 'test',
        'email': 'test@example.com',
        'password': 'abcd1234'
    })
    assert not user.is_password_valid('1234abcd')
    assert user.is_password_valid('abcd1234')


def test_url(app, db_conn, users_table):
    """
    Expect a model to provide URLs.
    """
    user, errors = User.insert({
        'name': 'test',
        'email': 'test@example.com',
        'password': 'abcd1234'
    })
    with app.test_request_context('/'):
        assert user.get_url().startswith('/api/users/')
