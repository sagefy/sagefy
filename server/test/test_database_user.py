from database.user import insert_user, update_user, get_user, \
    is_password_valid, get_avatar, get_learning_context, \
    set_learning_context, get_email_token, is_valid_token, deliver_user, \
    update_user_password
import json
from framework.redis import redis


def test_user_name_required(db_conn):
    """
    Ensure a name is required.
    """
    user = {}
    user, errors = insert_user(user, db_conn)
    assert len(errors) > 0
    assert 'name' in [e['name'] for e in errors]


def test_user_name_unique(db_conn, users_table):
    """
    Ensure a name is unique.
    """
    users_table.insert({'name': 'test'}).run(db_conn)
    user = {
        'name': 'test',
        'email': 'test@example.com',
        'password': 'abcd1234'
    }
    user, errors = insert_user(user, db_conn)
    assert len(errors) > 0
    assert 'name' in [e['name'] for e in errors]
    assert 'Must be unique.' in [e['message'] for e in errors]


def test_user_email_required(db_conn):
    """
    Ensure an email is required.
    """
    user = {}
    user, errors = insert_user(user, db_conn)
    assert len(errors) > 0
    assert 'email' in [e['name'] for e in errors]


def test_user_email_unique(db_conn, users_table):
    """
    Ensure an email is unique.
    """
    users_table.insert({
        'id': 'abcd1234',
        'email': 'test@example.com',
    }).run(db_conn)
    user, errors = insert_user({
        'name': 'test',
        'email': 'test@example.com',
        'password': 'abcd1234'
    }, db_conn)
    assert len(errors) > 0
    assert 'email' in [e['name'] for e in errors]
    assert 'Must be unique.' in [e['message'] for e in errors]


def test_user_email_format(db_conn):
    """
    Ensure an email is formatted.
    """
    user = {'email': 'other'}
    user, errors = insert_user(user, db_conn)
    assert 'email' in [e['name'] for e in errors]
    assert 'Must be an email.' in [e['message'] for e in errors]


def test_user_password_required(db_conn):
    """
    Ensure a password is required.
    """
    user = {}
    user, errors = insert_user(user, db_conn)
    assert len(errors) > 0
    assert 'password' in [e['name'] for e in errors]


def test_user_password_minlength(db_conn):
    """
    Ensure an password is long enough.
    """
    user = {'password': 'abcd'}
    user, errors = insert_user(user, db_conn)
    assert 'password' in [e['name'] for e in errors]
    assert 'Must have minimum length of 8.' in [e['message'] for e in errors]


def test_user_no_password(db_conn, users_table):
    """
    Ensure an password isn't provided ever.
    """
    user, errors = insert_user({
        'name': 'test',
        'email': 'test@example.com',
        'password': 'abcd1234'
    }, db_conn)
    json = deliver_user(user, access='private')
    assert 'password' not in json


def test_user_email_current(db_conn, users_table):
    """
    Ensure an email is only provided when current user.
    """
    user, errors = insert_user({
        'name': 'test',
        'email': 'test@example.com',
        'password': 'abcd1234'
    }, db_conn)
    json = deliver_user(user)
    assert 'email' not in json
    json = deliver_user(user, access='private')
    assert 'email' in json


def test_user_password_encrypt(db_conn, users_table):
    """
    Ensure a password is encrypted before going into db.
    """
    user, errors = insert_user({
        'id': 'abcd1234',
        'name': 'test',
        'email': 'test@example.com',
        'password': 'abcd1234'
    }, db_conn)
    assert len(errors) == 0
    assert user['password'] != 'abcd1234'
    assert user['password'].startswith('$2a$')


def test_user_password_validate(db_conn, users_table):
    """
    Ensure a password can be validated.
    """
    user, errors = insert_user({
        'id': 'abcd1234',
        'name': 'test',
        'email': 'test@example.com',
        'password': 'abcd1234'
    }, db_conn)
    assert not is_password_valid(user['password'], '1234abcd')
    assert is_password_valid(user['password'], 'abcd1234')


def test_get_email_token(db_conn, users_table):
    """
    Expect an email token created so a user can reset their password.
    """

    users_table.insert({
        'id': 'abcd1234',
        'name': 'Dalton',
        'email': 'test@example.com',
        'password': 'abcd1234',
    }).run(db_conn)
    user = get_user({'id': 'abcd1234'}, db_conn)
    token = get_email_token(user, send_email=False)
    assert redis.get('user_password_token_abcd1234')
    assert token


def test_is_valid_token(db_conn, users_table):
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
    user = get_user({'id': 'abcd1234'}, db_conn)
    token = get_email_token(user, send_email=False)
    assert is_valid_token(user, token)
    assert not is_valid_token(user, 'abcd1234')


def test_update_user(db_conn, users_table):
    """
    Expect to update a user's data.
    """

    user, errors = insert_user({
        'name': 'Dalton',
        'email': 'test@example.com',
        'password': 'abcd1234',
    }, db_conn)
    user2, errors2 = update_user(user, {
        'email': 'abcd@example.com'
    }, db_conn)
    assert len(errors2) == 0
    assert user['name'] == user2['name']
    assert user['email'] != user2['email']


def test_update_password(db_conn, users_table):
    """
    Expect to update a user's password.
    """

    user, errors = insert_user({
        'name': 'Dalton',
        'email': 'test@example.com',
        'password': 'abcd1234',
    }, db_conn)
    pw1 = user['password']
    user, errors = update_user_password(user,
                                        {'password': '1234abcd'}, db_conn)
    assert pw1 != user['password']


def test_get_learning_context(db_conn, users_table):
    """
    Expect to get the learning context.
    """

    users_table.insert({
        'id': 'abcd1234',
        'name': 'Dalton',
        'email': 'test@example.com',
        'password': 'abcd1234',
    }).run(db_conn)

    user = get_user({'id': 'abcd1234'}, db_conn)

    redis.set('learning_context_abcd1234', json.dumps({
        'card': {'entity_id': 'A'},
        'unit': {'entity_id': 'B'},
        'set': {'entity_id': 'C'},
    }))
    assert get_learning_context(user) == {
        'card': {'entity_id': 'A'},
        'unit': {'entity_id': 'B'},
        'set': {'entity_id': 'C'},
    }

    redis.delete('learning_context_abcd1234')
    assert get_learning_context(user) == {}


def test_set_learning_context(db_conn, users_table):
    """
    Expect to set the learning context.
    """

    users_table.insert({
        'id': 'abcd1234',
        'name': 'Dalton',
        'email': 'test@example.com',
        'password': 'abcd1234',
    }).run(db_conn)

    user = get_user({'id': 'abcd1234'}, db_conn)

    set_learning_context(user, card={'entity_id': 'A'})
    assert get_learning_context(user) == {
        'card': {'entity_id': 'A'}
    }

    set_learning_context(user, unit={
        'entity_id': 'B',
        'name': 'Banana',
        'body': "Banana",
    }, set={
        'entity_id': 'C',
        'name': 'Coconut',
    })
    assert get_learning_context(user) == {
        'card': {
            'entity_id': 'A',
        },
        'unit': {
            'entity_id': 'B',
            'name': 'Banana',
            'body': "Banana",
        },
        'set': {
            'entity_id': 'C',
            'name': 'Coconut',
        }
    }

    set_learning_context(user, set=None)
    assert get_learning_context(user) == {
        'card': {
            'entity_id': 'A',
        },
        'unit': {
            'entity_id': 'B',
            'name': 'Banana',
            'body': "Banana",
        },
    }

    set_learning_context(user, card=None, unit=None)
    assert get_learning_context(user) == {}


def test_get_avatar():
    """
    Expect to get a URL for a user's avatar.
    """

    email = 'test@example.com'
    url = get_avatar(email)
    assert url.startswith('https://www.gravatar.com/avatar/' +
                          '55502f40dc8b7c769880b10874abc9d0')
