
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
        'created': datetime(2004, 11, 3, tzinfo=timezone.utc),
        'status': 'accepted',
        'kind': 'video'
    }, {
        'id': 'B2',
        'entity_id': 'A',
        'created': datetime(2005, 11, 3, tzinfo=timezone.utc),
        'status': 'accepted',
        'kind': 'video'
    }, {
        'id': 'C3',
        'entity_id': 'B',
        'created': datetime(2006, 11, 3, tzinfo=timezone.utc),
        'status': 'accepted',
        'kind': 'video'
    }]).run(db_conn)

    e = get_latest_accepted(db_conn, 'cards', 'A')
    assert e['id'] == 'B2'
