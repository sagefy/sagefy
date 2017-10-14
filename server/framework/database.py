"""
On each request, we create and close a new connection.
"""

import psycopg2
import psycopg2.extras
from modules.util import pick


config = {
    'host': 'localhost',
    'dbname': 'sagefy',
    'user': 'postgres',
    'port': 5432,
}


psycopg2.extras.register_uuid()


def make_db_connection():
    """
    Create a database connection.
    """

    db_config = pick(config, ('host', 'dbname', 'user', 'port'))
    print('db_config', db_config)
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
