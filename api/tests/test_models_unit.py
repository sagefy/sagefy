import pytest

xfail = pytest.mark.xfail

import rethinkdb as r
from models.unit import Unit


@xfail
def test_entity_id(app, db_conn, units_table):
    """
    Expect a unit to require an entity_id.
    """
    assert False


@xfail
def test_previous(app, db_conn, units_table):
    """
    Expect a version previous_id to be a string or None.
    """
    assert False


@xfail
def test_language(app, db_conn, units_table):
    """
    Expect a unit to require a language.
    """
    assert False


@xfail
def test_name(app, db_conn, units_table):
    """
    Expect a unit to require a name.
    """
    assert False


@xfail
def test_body(app, db_conn, units_table):
    """
    Expect a unit to require a body.
    """
    assert False


@xfail
def test_canonical(app, db_conn, units_table):
    """
    Expect a unit canonical to be a boolean.
    """
    assert False


@xfail
def test_tags(app, db_conn, units_table):
    """
    Expect a unit to allow tags.
    """
    assert False


@xfail
def test_requires(app, db_conn, units_table):
    """
    Expect a unit to allow requires ids.
    """
    assert False


def test_latest_canonical(app, db_conn, units_table):
    """
    Expect to get the latest canonical card version.
    """

    units_table.insert([{
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

    unit = Unit.get_latest_canonical('A')
    assert unit['id'] == 'B2'
