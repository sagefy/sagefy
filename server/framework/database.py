"""
On each request, we create and close a new connection.
"""

from config import config
import psycopg2
import psycopg2.extras


psycopg2.extras.register_uuid()


def make_db_connection():
  """
  Create a database connection.
  """

  db_config = {
    'host': config['pg_host'],
    'dbname': config['pg_dbname'],
    'user': config['pg_user'],
    'port': config['pg_port'],
  }
  try:
    db_conn = psycopg2.connect(**db_config)
    return db_conn
  except (Exception, psycopg2.DatabaseError) as error:
    print("I cannot connect to PostgresQL.")
    print(error)


def close_db_connection(db_conn):
  """
  Close the DB connection.
  """

  db_conn.close()
