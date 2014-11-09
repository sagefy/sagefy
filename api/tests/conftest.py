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
from rethinkdb.errors import RqlRuntimeError


@pytest.fixture(scope='session')
def app(request):
    """
    Create an application for running the tests.
    Use a different database for testing.
    """
    app = create_app(config, debug=True, testing=True)
    # Manage app context for testing
    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return app


@pytest.fixture(scope='function')
def db_conn(app, request):
    g.db_conn, g.db = make_db_connection(app)

    def teardown():
        g.db_conn.close()

    request.addfinalizer(teardown)
    return g.db_conn

##########
# TODO: For below functions, figure out a way to reduce this to one function
##########


@pytest.fixture(scope='module')
def users_table(app, db_conn, request):
    try:
        g.db.table_create('users').run(db_conn)
    except RqlRuntimeError:
        pass
    table = g.db.table('users')
    table.delete().run(db_conn)
    return table


@pytest.fixture(scope='module')
def notices_table(app, db_conn, request):
    try:
        g.db.table_create('notices').run(db_conn)
    except RqlRuntimeError:
        pass
    table = g.db.table('notices')
    table.delete().run(db_conn)
    return table


@pytest.fixture(scope='module')
def topics_table(app, db_conn, request):
    try:
        g.db.table_create('topics').run(db_conn)
    except RqlRuntimeError:
        pass
    table = g.db.table('topics')
    table.delete().run(db_conn)
    return table


@pytest.fixture(scope='module')
def posts_table(app, db_conn, request):
    try:
        g.db.table_create('posts').run(db_conn)
    except RqlRuntimeError:
        pass
    table = g.db.table('posts')
    table.delete().run(db_conn)
    return table
