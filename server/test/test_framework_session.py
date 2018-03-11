from framework.session import get_current_user, log_in_user, log_out_user
from framework.redis_conn import red
from conftest import user_id, create_user_in_db, log_in
from database.user import get_user
from modules.util import convert_slug_to_uuid, convert_uuid_to_slug


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
  assert user['id'] == convert_slug_to_uuid(user_id)


def test_log_in_user(db_conn):
  """
  Expect to log in as a user.
  """

  create_user_in_db(db_conn)
  user = get_user(db_conn, {'id': user_id})
  token = log_in_user(user)
  assert token
  assert red.get(token).decode() == convert_uuid_to_slug(user_id)


def test_log_out_user(db_conn):
  """
  Expect to log out as a user.
  """

  create_user_in_db(db_conn)
  user = get_user(db_conn, {'id': user_id})
  token = log_in_user(user)
  assert red.get(token).decode() == convert_uuid_to_slug(user_id)
  log_out_user({
    'cookies': {'session_id': token},
    'db_conn': db_conn,
  })
  assert red.get(token) is None
