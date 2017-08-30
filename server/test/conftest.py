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
from passlib.hash import bcrypt

from test_config import config
import framework.index as framework
framework.update_config(config)

from framework.database import make_db_connection, close_db_connection
import framework.session


def create_user_in_db(db_conn, users_table):
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
    db_conn = make_db_connection()
    request.addfinalizer(lambda: close_db_connection(db_conn))
    return db_conn


@pytest.fixture
def session(db_conn, request, users_table):
    create_user_in_db(db_conn, users_table)
    session_id = log_in()
    request.addfinalizer(lambda: log_out(session_id))
    return session_id


def table(db_conn, name, request):
    """
    Ensure the table is freshly empty after use.
    """
    table = r.table(name)
    table.delete().run(db_conn)
    request.addfinalizer(lambda: table.delete().run(db_conn))
    return table


@pytest.fixture
def users_table(db_conn, request):
    return table(db_conn, 'users', request)


@pytest.fixture
def notices_table(db_conn, request):
    return table(db_conn, 'notices', request)


@pytest.fixture
def topics_table(db_conn, request):
    return table(db_conn, 'topics', request)


@pytest.fixture
def posts_table(db_conn, request):
    return table(db_conn, 'posts', request)


@pytest.fixture
def cards_table(db_conn, request):
    return table(db_conn, 'cards', request)


@pytest.fixture
def cards_parameters_table(db_conn, request):
    return table(db_conn, 'cards_parameters', request)


@pytest.fixture
def units_table(db_conn, request):
    return table(db_conn, 'units', request)


@pytest.fixture
def subjects_table(db_conn, request):
    return table(db_conn, 'subjects', request)


@pytest.fixture
def follows_table(db_conn, request):
    return table(db_conn, 'follows', request)


@pytest.fixture
def users_subjects_table(db_conn, request):
    return table(db_conn, 'users_subjects', request)


@pytest.fixture
def responses_table(db_conn, request):
    return table(db_conn, 'responses', request)
