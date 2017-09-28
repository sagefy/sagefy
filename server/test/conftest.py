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
from test_config import config
import framework.index as framework
framework.update_config(config)
from framework.database import make_db_connection, close_db_connection
import framework.session
from database.user import insert_user


def create_user_in_db(db_conn):
    return insert_user(db_conn, {
        'name': 'test',
        'email': 'test@example.com',
        'password': 'abcd1234',
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


@pytest.fixture(autouse=True)
def wipe_db(db_conn, request):
    for tablename in reversed((
        'users',
        'units_entity_id',
        'units',
        'cards_entity_id',
        'cards',
        'cards_parameters',
        'subjects_entity_id',
        'subjects',
        'topics',
        'posts',
        'follows',
        'notices',
        'users_subjects',
        'responses',
    )):
        cur = db_conn.cursor()
        try:
            with cur:
                cur.execute(
                    "DELETE FROM {tablename};"
                    .format(tablename=tablename)
                )
                db_conn.commit()
        except Exception:
            db_conn.rollback()


@pytest.fixture
def session(db_conn, request):
    create_user_in_db(db_conn)
    session_id = log_in()
    request.addfinalizer(lambda: log_out(session_id))
    return session_id
