import pytest

xfail = pytest.mark.xfail

import rethinkdb as r
from models.card import Card


@xfail
def test_entity_id(app, db_conn, cards_table):
    """
    Expect a card to require an entity_id.
    """
    return False


@xfail
def test_previous_version_id(app, db_conn, cards_table):
    """
    Expect a card to allow a previous version id.
    """
    return False


@xfail
def test_language(app, db_conn, cards_table):
    """
    Expect a card to require a language.
    """
    return False


@xfail
def test_unit_id(app, db_conn, cards_table):
    """
    Expect a card to require a unit id.
    """
    return False


@xfail
def test_name(app, db_conn, cards_table):
    """
    Expect a card to require a name.
    """
    return False


@xfail
def test_canonical(app, db_conn, cards_table):
    """
    Expect a card version canoncial to be a boolean.
    """
    return False


@xfail
def test_tags(app, db_conn, cards_table):
    """
    Expect a card to allow tags.
    """
    return False


@xfail
def test_kind(app, db_conn, cards_table):
    """
    Expect a card to have a kind.
    """
    return False


def test_latest_canonical(app, db_conn, cards_table):
    """
    Expect to get the latest canonical card version.
    """

    cards_table.insert([{
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

    card = Card.get_latest_canonical('A')
    assert card['id'] == 'B2'
