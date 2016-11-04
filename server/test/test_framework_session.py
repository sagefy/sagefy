import pytest

xfail = pytest.mark.xfail

from conftest import create_user_in_db, log_in
from framework.session import get_current_user, log_in_user, log_out_user
from database.user import get_user
from framework.redis import redis


def test_get_current_user(users_table, db_conn):
    """
    Expect to get the current user given session info.
    """

    create_user_in_db(users_table, db_conn)
    token = log_in()
    user = get_current_user({
        'cookies': {'session_id': token},
        'db_conn': db_conn,
    })
    assert user
    assert user['id'] == 'abcd1234'


def test_log_in_user(users_table, db_conn):
    """
    Expect to log in as a user.
    """

    create_user_in_db(users_table, db_conn)
    user = get_user({'id': 'abcd1234'}, db_conn)
    token = log_in_user(user)
    assert token
    assert redis.get(token).decode() == 'abcd1234'


def test_log_out_user(users_table, db_conn):
    """
    Expect to log out as a user.
    """

    create_user_in_db(users_table, db_conn)
    user = get_user({'id': 'abcd1234'}, db_conn)
    token = log_in_user(user)
    assert redis.get(token).decode() == 'abcd1234'
    log_out_user({
        'cookies': {'session_id': token},
        'db_conn': db_conn,
    })
    assert redis.get(token) is None
