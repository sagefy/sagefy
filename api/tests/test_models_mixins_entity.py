import pytest

xfail = pytest.mark.xfail

import rethinkdb as r
from models.card import Card
from models.set import Set
from models.unit import Unit


def test_latest_accepted_card(db_conn, cards_table):
    """
    Expect to get the latest accepted card version.
    """

    cards_table.insert([{
        'id': 'A1',
        'entity_id': 'A',
        'created': r.time(2004, 11, 3, 'Z'),
        'accepted': True,
    }, {
        'id': 'B2',
        'entity_id': 'A',
        'created': r.time(2005, 11, 3, 'Z'),
        'accepted': True,
    }, {
        'id': 'C3',
        'entity_id': 'B',
        'created': r.time(2006, 11, 3, 'Z'),
        'accepted': True,
    }]).run(db_conn)

    card = Card.get_latest_accepted('A')
    assert card['id'] == 'B2'


def test_latest_accepted(db_conn, units_table):
    """
    Expect to get the latest accepted unit version.
    """

    units_table.insert([{
        'id': 'A1',
        'entity_id': 'A',
        'created': r.time(2004, 11, 3, 'Z'),
        'accepted': True,
    }, {
        'id': 'B2',
        'entity_id': 'A',
        'created': r.time(2005, 11, 3, 'Z'),
        'accepted': True,
    }, {
        'id': 'C3',
        'entity_id': 'B',
        'created': r.time(2006, 11, 3, 'Z'),
        'accepted': True,
    }]).run(db_conn)

    unit = Unit.get_latest_accepted('A')
    assert unit['id'] == 'B2'


def test_latest_accepted_set(db_conn, sets_table):
    """
    Expect to get the latest accepted set version.
    """

    sets_table.insert([{
        'id': 'A1',
        'entity_id': 'A',
        'created': r.time(2004, 11, 3, 'Z'),
        'accepted': True,
    }, {
        'id': 'B2',
        'entity_id': 'A',
        'created': r.time(2005, 11, 3, 'Z'),
        'accepted': True,
    }, {
        'id': 'C3',
        'entity_id': 'B',
        'created': r.time(2006, 11, 3, 'Z'),
        'accepted': True,
    }]).run(db_conn)

    set_ = Set.get_latest_accepted('A')
    assert set_['id'] == 'B2'


def test_get_versions(db_conn, cards_table):
    """
    Expect to get the latest versions of the card.
    """

    cards_table.insert([{
        'id': 'A1',
        'entity_id': 'A',
        'created': r.time(2004, 11, 3, 'Z'),
        'accepted': True,
    }, {
        'id': 'B2',
        'entity_id': 'A',
        'created': r.time(2005, 11, 3, 'Z'),
    }, {
        'id': 'C3',
        'entity_id': 'B',
        'created': r.time(2006, 11, 3, 'Z'),
        'accepted': True,
    }]).run(db_conn)

    card_versions = Card.get_versions('A')
    assert len(card_versions) == 2


def test_list_requires(db_conn, cards_table):
    """
    Expect to list all the prereqs for the entity.
    """

    cards_table.insert([{
        'entity_id': 'abcd',
        'unit_id': 'zytx',
        'created': r.now(),
        'modified': r.now(),
        'accepted': True,
        'kind': 'video',
        'requires': ['zxyz'],
    }, {
        'entity_id': 'abcd',
        'unit_id': 'zytx',
        'created': r.time(1986, 11, 3, 'Z'),
        'modified': r.time(1986, 11, 3, 'Z'),
        'accepted': True,
        'kind': 'video',
    }, {
        'entity_id': 'zxyz',
        'unit_id': 'zytx',
        'created': r.now(),
        'modified': r.now(),
        'accepted': True,
        'kind': 'video',
    }, {
        'entity_id': 'qwer',
        'unit_id': 'zytx',
        'created': r.now(),
        'modified': r.now(),
        'accepted': True,
        'kind': 'choice',
        'requires': ['abcd'],
    }]).run(db_conn)

    cards = Card.list_requires('abcd')

    assert len(cards) == 1
    assert cards[0]['entity_id'] == 'zxyz'


def test_list_required_by(db_conn, cards_table):
    """
    Expect to list all the entity that require the given one.
    """

    cards_table.insert([{
        'entity_id': 'abcd',
        'unit_id': 'zytx',
        'created': r.now(),
        'modified': r.now(),
        'accepted': True,
        'kind': 'video',
        'requires': ['zxyz'],
    }, {
        'entity_id': 'abcd',
        'unit_id': 'zytx',
        'created': r.time(1986, 11, 3, 'Z'),
        'modified': r.time(1986, 11, 3, 'Z'),
        'accepted': True,
        'kind': 'video',
    }, {
        'entity_id': 'zxyz',
        'unit_id': 'zytx',
        'created': r.now(),
        'modified': r.now(),
        'accepted': True,
        'kind': 'video',
    }, {
        'entity_id': 'qwer',
        'unit_id': 'zytx',
        'created': r.now(),
        'modified': r.now(),
        'accepted': True,
        'kind': 'choice',
        'requires': ['abcd'],
    }]).run(db_conn)

    cards = Card.list_required_by('abcd')

    assert len(cards) == 1
    assert cards[0]['entity_id'] == 'qwer'
