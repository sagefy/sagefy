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
import json

from test_config import config
import framework.index as framework
framework.update_config(config)

from framework.database import setup_db, \
    make_db_connection, close_db_connection
from framework.database import db as g_db

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


def log_in(c):
    return c.post('/api/users/log_in/', data=json.dumps({
        'name': 'test',
        'password': 'abcd1234'
    }), content_type='application/json')


def log_out(c):
    return c.post('/api/users/log_out/', data=json.dumps({}),
                  content_type='application/json')


@pytest.fixture(scope='session')
def db_conn(request):
    db_conn, db = make_db_connection()
    request.addfinalizer(lambda: close_db_connection())
    return db_conn


@pytest.fixture
def log_in_user(app, request, db_conn, users_table):
    create_user_in_db(users_table, db_conn)
    session_token = log_in()
    request.addfinalizer(lambda: log_out())
    return session_token


def table(name, request, db_conn):
    """
    Ensure the table is freshly empty after use.
    """
    table = g_db.table(name)
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
