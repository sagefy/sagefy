# pylint: disable=wrong-import-position,wrong-import-order,protected-access
import uuid

# via https://stackoverflow.com/a/11158224
import os
import sys
import inspect
sys._called_from_test = True
currentdir = os.path.dirname(
  os.path.abspath(
    inspect.getfile(
      inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from framework.database import make_db_connection, close_db_connection
from framework.session import log_in_user, log_out_user
import pytest
from modules.util import convert_slug_to_uuid


user_id = uuid.uuid4()


def create_user_in_db(db_conn):
  from raw_insert import raw_insert_users
  raw_insert_users(db_conn, [{
    'id': convert_slug_to_uuid(user_id),
    'name': 'test',
    'email': 'test@example.com',
    'password': 'abcd1234',
  }])


def log_in():
  return log_in_user({'id': user_id})


def log_out(session_id):
  return log_out_user({
    'cookies': {'session_id': session_id}
  })


@pytest.fixture(scope='session')
def db_conn(request):
  db_conn = make_db_connection()
  request.addfinalizer(lambda: close_db_connection(db_conn))
  return db_conn


@pytest.fixture(autouse=True)
def wipe_db(db_conn, request):
  query = ''.join([
    "DELETE FROM {tablename};"
    .format(tablename=tablename)
    for tablename in reversed((
      'users',
      'units_entity_id',
      'units',
      'cards_entity_id',
      'cards',
      'cards_parameters',
      'subjects_entity_id',
      'subjects',
      'topics',
      'posts',
      'follows',
      'notices',
      'users_subjects',
      'responses',
    ))
  ])
  cur = db_conn.cursor()
  try:
    with cur:
      cur.execute(query)
      db_conn.commit()
  except Exception:
    db_conn.rollback()


@pytest.fixture
def session(db_conn, request):
  create_user_in_db(db_conn)
  session_id = log_in()
  request.addfinalizer(lambda: log_out(session_id))
  return session_id
