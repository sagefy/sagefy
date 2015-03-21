from models.user import User
import pytest

xfail = pytest.mark.xfail


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
    users_table.insert({
        'id': 'abcd1234',
        'email': 'test@example.com',
    }).run(db_conn)
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
    assert 'Must have minimum length of 8.' in [e['message'] for e in errors]


def test_user_no_password(app, db_conn, users_table):
    """
    Ensure an password isn't provided ever.
    """
    user, errors = User.insert({
        'name': 'test',
        'email': 'test@example.com',
        'password': 'abcd1234'
    })
    json = user.deliver(access='private')
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
    json = user.deliver()
    assert 'email' not in json
    json = user.deliver(access='private')
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
    assert len(errors) == 0
    assert user['password'] != 'abcd1234'
    assert user['password'].startswith('$2a$')


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


def test_get_email_token(app, db_conn, users_table):
    """
    Expect an email token created so a user can reset their password.
    """
    users_table.insert({
        'id': 'abcd1234',
        'name': 'Dalton',
        'email': 'test@example.com',
        'password': 'abcd1234',
    }).run(db_conn)
    user = User.get(id='abcd1234')
    token = user.get_email_token(send_email=False)
    assert app.redis.get('user_password_token_abcd1234')
    assert token


def test_is_valid_token(app, db_conn, users_table):
    """
    Expect a valid token to be approved.
    Expect an invalid token to not be approved.
    """
    users_table.insert({
        'id': 'abcd1234',
        'name': 'Dalton',
        'email': 'test@example.com',
        'password': 'abcd1234',
    }).run(db_conn)
    user = User.get(id='abcd1234')
    token = user.get_email_token(send_email=False)
    assert user.is_valid_token(token)
    assert not user.is_valid_token('abcd1234')


def test_update_password(app, db_conn, users_table):
    """
    Expect to update a user's password.
    """
    user, errors = User.insert({
        'name': 'Dalton',
        'email': 'test@example.com',
        'password': 'abcd1234',
    })
    pw1 = user['password']
    user.update_password('1234abcd')
    assert pw1 != user['password']


@xfail
def test_get_learning_context(app, db_conn, users_table):
    """
    Expect to get the learning context.
    """

    assert False


@xfail
def test_set_learning_context(app, db_conn, users_table):
    """
    Expect to set the learning context.
    """

    assert False
