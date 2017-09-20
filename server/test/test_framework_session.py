import pytest
from conftest import create_user_in_db, log_in
from framework.session import get_current_user, log_in_user, log_out_user
from database.user import get_user
from framework.redis import redis


xfail = pytest.mark.xfail


def test_get_current_user(db_conn):
    """
    Expect to get the current user given session info.
    """

    create_user_in_db(db_conn)
    token = log_in()
    user = get_current_user({
        'cookies': {'session_id': token},
        'db_conn': db_conn,
    })
    assert user
    assert user['id'] == 'abcd1234'


def test_log_in_user(db_conn):
    """
    Expect to log in as a user.
    """

    create_user_in_db(db_conn)
    user = get_user(db_conn, {'id': 'abcd1234'})
    token = log_in_user(user)
    assert token
    assert redis.get(token).decode() == 'abcd1234'


def test_log_out_user(db_conn):
    """
    Expect to log out as a user.
    """

    create_user_in_db(db_conn)
    user = get_user(db_conn, {'id': 'abcd1234'})
    token = log_in_user(user)
    assert redis.get(token).decode() == 'abcd1234'
    log_out_user({
        'cookies': {'session_id': token},
        'db_conn': db_conn,
    })
    assert redis.get(token) is None
