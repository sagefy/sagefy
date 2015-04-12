# via https://stackoverflow.com/a/11158224
import os
import sys
import inspect
currentdir = os.path.dirname(
    os.path.abspath(
        inspect.getfile(
            inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import pytest
import rethinkdb as r
from passlib.hash import bcrypt

from test_config import config
import framework.index as framework
framework.update_config(config)

from framework.database import setup_db, \
    make_db_connection, close_db_connection
import framework.database
import framework.session

setup_db()


def create_user_in_db(users_table, db_conn):
    return users_table.insert({
        'id': 'abcd1234',
        'name': 'test',
        'email': 'test@example.com',
        'password': bcrypt.encrypt('abcd1234'),
        'created': r.now(),
        'modified': r.now()
    }).run(db_conn)


def log_in():
    return framework.session.log_in_user({'id': 'abcd1234'})


def log_out(session_id):
    return framework.session.log_out_user({
        'cookies': {'session_id': session_id}
    })


@pytest.fixture(scope='session')
def db_conn(request):
    db_conn, db = make_db_connection()
    request.addfinalizer(lambda: close_db_connection())
    return db_conn


@pytest.fixture
def session(request, db_conn, users_table):
    create_user_in_db(users_table, db_conn)
    session_id = log_in()
    request.addfinalizer(lambda: log_out(session_id))
    return session_id


def table(name, request, db_conn):
    """
    Ensure the table is freshly empty after use.
    """
    table = framework.database.db.table(name)
    request.addfinalizer(lambda: table.delete().run(db_conn))
    return table


@pytest.fixture
def users_table(request, db_conn):
    return table('users', request, db_conn)


@pytest.fixture
def notices_table(request, db_conn):
    return table('notices', request, db_conn)


@pytest.fixture
def topics_table(request, db_conn):
    return table('topics', request, db_conn)


@pytest.fixture
def posts_table(request, db_conn):
    return table('posts', request, db_conn)


@pytest.fixture
def cards_table(request, db_conn):
    return table('cards', request, db_conn)


@pytest.fixture
def units_table(request, db_conn):
    return table('units', request, db_conn)


@pytest.fixture
def sets_table(request, db_conn):
    return table('sets', request, db_conn)


@pytest.fixture
def follows_table(request, db_conn):
    return table('follows', request, db_conn)


@pytest.fixture
def users_sets_table(request, db_conn):
    return table('users_sets', request, db_conn)


@pytest.fixture
def responses_table(request, db_conn):
    return table('responses', request, db_conn)
