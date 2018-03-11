

from framework.database import make_db_connection, close_db_connection
from config import config


def test_make_and_close_db_connection():
  db_conn = make_db_connection()
  assert not isinstance(db_conn, str)
  close_db_connection(db_conn)


def test_make_db_conn_err():
  prev_host = config['pg_host']
  config['pg_host'] = 'AHHHH!'
  assert not make_db_connection()
  config['pg_host'] = prev_host
