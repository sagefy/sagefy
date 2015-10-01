import pytest

xfail = pytest.mark.xfail

from modules.sequencer.traversal import traverse
from models.user import User
from models.set import Set
import rethinkdb as r


@xfail
def test_traverse(db_conn, units_table, users_table, responses_table,
                  sets_table):
    """
    Expect to take a list of units and traverse them correctly.

    A requires B
    A requires C
    B requires D
    B requires E
    C requires E
    C requires F

    A needs to be diagnosed.
    B needs to be learned.
    C needs to be learned.
    E needs to be learned.
    F is learned and needs review.
    D is learned and does not need review.

    The function should then return...
    diagnose: A
    learn: E, {B, C}
    review: F
    """

    users_table.insert({
        'id': 'A'
    }).run(db_conn)

    units_table.insert([{
        'entity_id': 'A'
    }, {
        'entity_id': 'B'
    }, {
        'entity_id': 'C'
    }, {
        'entity_id': 'D'
    }, {
        'entity_id': 'E'
    }, {
        'entity_id': 'F'
    }]).run(db_conn)

    sets_table.insert({
        'entity_id': 'A',
        'members': [
            {'id': 'A', 'kind': 'unit'},
            {'id': 'B', 'kind': 'unit'},
            {'id': 'C', 'kind': 'unit'},
            {'id': 'D', 'kind': 'unit'},
            {'id': 'E', 'kind': 'unit'},
            {'id': 'F', 'kind': 'unit'},
        ]
    }).run(db_conn)

    responses_table.insert([{
        'user_id': 'A', 'unit_id': 'B', 'learned': 0.0, 'created': r.now()
    }, {
        'user_id': 'A', 'unit_id': 'C', 'learned': 0.0, 'created': r.now()
    }, {
        'user_id': 'A', 'unit_id': 'D', 'learned': 1.0, 'created': r.now()
    }, {
        'user_id': 'A', 'unit_id': 'E', 'learned': 0.0, 'created': r.now()
    }, {
        'user_id': 'A', 'unit_id': 'F', 'learned': 1.0,
        'created': r.time(2004, 11, 3, 'Z')
    }]).run(db_conn)

    set_ = Set.get(entity_id='A')
    user = User.get(id='A')
    buckets = traverse(user, set_)
    assert len(buckets['diagnose']) == 1
    assert buckets['diagnose'][0]['entity_id'] == 'A'
    assert len(buckets['learn']) == 3
    assert buckets['learn'][0]['entity_id'] == 'E'
    assert len(buckets['review']) == 1
    assert buckets['review'][0]['entity_id'] == 'F'


"""
TODO @outline tests
Expect to add no known ability to "diagnose".
Expect to add low ability to "ready".
Expect to add high ability to "review".
Expect to show "done".
Expect to track number of units that depend on the given unit.
"""
