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
from flask import g
from app import create_app, make_db_connection
import test_config as config
import rethinkdb as r
from passlib.hash import bcrypt
import json


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
def app(request):
    """
    Manage app context for testing.
    Create an application for running the tests.
    Use a different database for testing.
    """
    app = create_app(config, debug=True, testing=True)
    ctx = app.app_context()
    ctx.push()
    request.addfinalizer(lambda: ctx.pop())
    return app


@pytest.fixture(scope='session')
def db_conn(app, request):
    g.db_conn, g.db = make_db_connection(app)
    request.addfinalizer(lambda: g.db_conn.close())
    return g.db_conn


@pytest.fixture
def c_user(app, request, db_conn, users_table):
    create_user_in_db(users_table, db_conn)
    with app.test_client() as c:
        log_in(c)
        request.addfinalizer(lambda: log_out(c))
        return c


def table(name, request, db_conn):
    """
    Ensure the table is freshly empty after use.
    """
    table = g.db.table(name)
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
