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
def notifications_table(app, db_conn, request):
    try:
        g.db.table_create('notifications').run(db_conn)
    except RqlRuntimeError:
        pass
    table = g.db.table('notifications')
    table.delete().run(db_conn)
    return table


@pytest.fixture(scope='module')
def messages_table(app, db_conn, request):
    try:
        g.db.table_create('messages').run(db_conn)
    except RqlRuntimeError:
        pass
    table = g.db.table('messages')
    table.delete().run(db_conn)
    return table
