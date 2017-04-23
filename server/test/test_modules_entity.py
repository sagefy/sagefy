import rethinkdb as r

from models.card import Card
from modules import entity

import pytest

xfail = pytest.mark.xfail


def test_get_latest_accepted(db_conn, cards_table):
    """
    Expect to pull the latest accepted
    version out of the database, given a kind and an entity_id.
    """

    cards_table.insert([{
        'id': 'A1',
        'entity_id': 'A',
        'created': r.time(2004, 11, 3, 'Z'),
        'status': 'accepted',
        'kind': 'video'
    }, {
        'id': 'B2',
        'entity_id': 'A',
        'created': r.time(2005, 11, 3, 'Z'),
        'status': 'accepted',
        'kind': 'video'
    }, {
        'id': 'C3',
        'entity_id': 'B',
        'created': r.time(2006, 11, 3, 'Z'),
        'status': 'accepted',
        'kind': 'video'
    }]).run(db_conn)

    e = entity.get_latest_accepted(db_conn, 'card', 'A')

    assert isinstance(e, Card)


def test_get_kind():
    """
    Expect to return kind as string given data.
    """

    kind = entity.get_kind(Card({}))
    assert kind == 'card'


@xfail
def test_get_card_by_kind(db_conn, cards_table):
    """
    Expect to get a card by id and return the proper kind.
    """

    assert False
