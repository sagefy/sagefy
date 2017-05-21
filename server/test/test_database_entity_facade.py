import rethinkdb as r
import pytest
from database.entity_base import get_latest_accepted

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

    e = get_latest_accepted('cards', db_conn, 'A')
    assert e['id'] == 'B2'
