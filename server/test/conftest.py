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
from datetime import datetime

from test_config import config
import framework.index as framework
framework.update_config(config)

from framework.database import make_db_connection, close_db_connection
import framework.session
from database.user import insert_user


def create_user_in_db(db_conn):
    return insert_user(db_conn, {
        'id': 'abcd1234',
        'name': 'test',
        'email': 'test@example.com',
        'password': bcrypt.encrypt('abcd1234'),
        'created': datetime.utcnow(),
        'modified': datetime.utcnow()
    })


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
