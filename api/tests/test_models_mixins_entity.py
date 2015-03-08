import pytest

xfail = pytest.mark.xfail

import rethinkdb as r
from models.card import Card
from models.set import Set
from models.unit import Unit


def test_latest_canonical_card(app, db_conn, cards_table):
    """
    Expect to get the latest canonical card version.
    """

    cards_table.insert([{
        'id': 'A1',
        'entity_id': 'A',
        'created': r.time(2004, 11, 3, 'Z'),
        'canonical': True,
    }, {
        'id': 'B2',
        'entity_id': 'A',
        'created': r.time(2005, 11, 3, 'Z'),
        'canonical': True,
    }, {
        'id': 'C3',
        'entity_id': 'B',
        'created': r.time(2006, 11, 3, 'Z'),
        'canonical': True,
    }]).run(db_conn)

    card = Card.get_latest_canonical('A')
    assert card['id'] == 'B2'


def test_latest_canonical(app, db_conn, units_table):
    """
    Expect to get the latest canonical unit version.
    """

    units_table.insert([{
        'id': 'A1',
        'entity_id': 'A',
        'created': r.time(2004, 11, 3, 'Z'),
        'canonical': True,
    }, {
        'id': 'B2',
        'entity_id': 'A',
        'created': r.time(2005, 11, 3, 'Z'),
        'canonical': True,
    }, {
        'id': 'C3',
        'entity_id': 'B',
        'created': r.time(2006, 11, 3, 'Z'),
        'canonical': True,
    }]).run(db_conn)

    unit = Unit.get_latest_canonical('A')
    assert unit['id'] == 'B2'


def test_latest_canonical_set(app, db_conn, sets_table):
    """
    Expect to get the latest canonical set version.
    """

    sets_table.insert([{
        'id': 'A1',
        'entity_id': 'A',
        'created': r.time(2004, 11, 3, 'Z'),
        'canonical': True,
    }, {
        'id': 'B2',
        'entity_id': 'A',
        'created': r.time(2005, 11, 3, 'Z'),
        'canonical': True,
    }, {
        'id': 'C3',
        'entity_id': 'B',
        'created': r.time(2006, 11, 3, 'Z'),
        'canonical': True,
    }]).run(db_conn)

    set_ = Set.get_latest_canonical('A')
    assert set_['id'] == 'B2'


def test_get_versions(app, db_conn, cards_table):
    """
    Expect to get the latest versions of the card.
    """

    cards_table.insert([{
        'id': 'A1',
        'entity_id': 'A',
        'created': r.time(2004, 11, 3, 'Z'),
        'canonical': True,
    }, {
        'id': 'B2',
        'entity_id': 'A',
        'created': r.time(2005, 11, 3, 'Z'),
    }, {
        'id': 'C3',
        'entity_id': 'B',
        'created': r.time(2006, 11, 3, 'Z'),
        'canonical': True,
    }]).run(db_conn)

    card_versions = Card.get_versions('A')
    assert len(card_versions) == 2
