import pytest

xfail = pytest.mark.xfail

import rethinkdb as r
from models.set import Set


@xfail
def test_entity(app, db_conn, sets_table):
    """
    Expect a set to require an entity_id.
    """
    assert False


@xfail
def test_previous(app, db_conn, sets_table):
    """
    Expect a set to allow a previous version id.
    """
    assert False


@xfail
def test_language(app, db_conn, sets_table):
    """
    Expect a set to require a language.
    """
    assert False


@xfail
def test_name(app, db_conn, sets_table):
    """
    Expect a set to require a name.
    """
    assert False


@xfail
def test_body(app, db_conn, sets_table):
    """
    Expect a set to require a body.
    """
    assert False


@xfail
def test_canonical(app, db_conn, sets_table):
    """
    Expect a set canonical to be a boolean.
    """
    assert False


@xfail
def test_tags(app, db_conn, sets_table):
    """
    Expect a set to allow tags.
    """
    assert False


@xfail
def test_members(app, db_conn, sets_table):
    """
    Expect a set to record a list of members.
    """
    assert False


def test_latest_canonical(app, db_conn, sets_table):
    """
    Expect to get the latest canonical card version.
    """

    sets_table.insert([{
        'id': 'A1',
        'entity_id': 'A',
        'created': r.time(2004, 11, 3, 'Z'),
    }, {
        'id': 'B2',
        'entity_id': 'A',
        'created': r.time(2005, 11, 3, 'Z'),
    }, {
        'id': 'C3',
        'entity_id': 'B',
        'created': r.time(2006, 11, 3, 'Z'),
    }]).run(db_conn)

    set_ = Set.get_latest_canonical('A')
    assert set_['id'] == 'B2'
