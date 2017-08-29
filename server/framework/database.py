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
    'password': 'postgres',
}


psycopg2.extras.register_uuid()


def make_db_connection():
    """
    Create a database connection.
    """

    try:
        db_conn = psycopg2.connect(
            **pick(config, ('host', 'dbname', 'user', 'password'))
        )
    except (Exception, psycopg2.DatabaseError) as error:
        print("I cannot connect to PostgresQL.")
        print(error)
    return db_conn


def close_db_connection(db_conn):
    """
    Close the DB connection.
    """

    db_conn.close()
