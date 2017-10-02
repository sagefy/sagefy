from modules.sequencer.traversal import traverse, \
    match_unit_dependents, order_units_by_need, judge
from database.user import get_user
from datetime import datetime, timezone
from database.subject import get_latest_accepted_subject
from database.unit import get_latest_accepted_unit, list_latest_accepted_units
from raw_insert import raw_insert_users, raw_insert_units, \
    raw_insert_responses, raw_insert_subjects


def add_test_subject(db_conn):
    """
    Add doesn't require anything.
    Multiply requires add.
    Subtract requires add.
    Divide requires multiply.

    Add is done,
    Subtract needs review,
    Multiply needs to be learned,
    Divide needs to be diagnosed.
    """

    raw_insert_users(db_conn, [{
        'id': 'user'
    }])

    raw_insert_units(db_conn, [{
        'entity_id': 'add',
        'status': 'accepted',
        'created': datetime.utcnow()
    }, {
        'entity_id': 'subtract',
        'require_ids': ['add'],
        'status': 'accepted',
        'created': datetime.utcnow()
    }, {
        'entity_id': 'multiply',
        'require_ids': ['add'],
        'status': 'accepted',
        'created': datetime.utcnow()
    }, {
        'entity_id': 'divide',
        'require_ids': ['multiply', 'subtract'],
        'status': 'accepted',
        'created': datetime.utcnow()
    }])

    raw_insert_responses(db_conn, [{
        'user_id': 'user', 'unit_id': 'add', 'learned': 0.99,
        'created': datetime.utcnow()
    }, {
        'user_id': 'user', 'unit_id': 'multiply', 'learned': 0.0,
        'created': datetime.utcnow()
    }, {
        'user_id': 'user', 'unit_id': 'subtract', 'learned': 0.99,
        'created': datetime(2004, 11, 3, tzinfo=timezone.utc)
    }])

    raw_insert_subjects(db_conn, {
        'entity_id': 'fghj4567',
        'status': 'accepted',
        'created': datetime(2004, 11, 1, tzinfo=timezone.utc),
        'members': [
            {'id': 'add', 'kind': 'unit'},
            {'id': 'subtract', 'kind': 'unit'},
            {'id': 'multiply', 'kind': 'unit'},
            {'id': 'divide', 'kind': 'unit'},
        ]
    })


def test_traverse(db_conn):
    """
    Expect to take a list of units and traverse them correctly.
    Basic test.
    """

    add_test_subject(db_conn)
    subject = get_latest_accepted_subject(db_conn, entity_id='fghj4567')
    assert subject is not None
    user = get_user(db_conn, {'id': 'user'})
    buckets = traverse(db_conn, user, subject)
    assert buckets['learn'][0]['entity_id'] in ('subtract', 'multiply')
    assert buckets['learn'][1]['entity_id'] in ('subtract', 'multiply')
    assert buckets['blocked'][0]['entity_id'] == 'divide'


"""
TODO-3 more traversal tests

traverse
--------
Expect if a node is done, any nodes it requires are left out.
If one node is done, and one is not, continue to the lower node.
Traverse should output units in order.
"""


def test_judge_diagnose(db_conn):
    """
    Expect to add no known ability to "diagnose".
    """

    add_test_subject(db_conn)
    unit = get_latest_accepted_unit(db_conn, entity_id='divide')
    user = get_user(db_conn, {'id': 'user'})
    assert judge(db_conn, unit, user) == "diagnose"


def test_judge_review(db_conn):
    """
    Expect to add older, high ability to "review".
    """

    add_test_subject(db_conn)
    unit = get_latest_accepted_unit(db_conn, entity_id='subtract')
    user = get_user(db_conn, {'id': 'user'})
    assert judge(db_conn, unit, user) == "review"


def test_judge_learn(db_conn):
    """
    Expect to add known low ability to "learn".
    """

    add_test_subject(db_conn)
    unit = get_latest_accepted_unit(db_conn, entity_id='multiply')
    user = get_user(db_conn, {'id': 'user'})
    assert judge(db_conn, unit, user) == "learn"


def test_judge_done(db_conn):
    """
    Expect to show "done".
    """

    add_test_subject(db_conn)
    unit = get_latest_accepted_unit(db_conn, entity_id='add')
    user = get_user(db_conn, {'id': 'user'})
    assert judge(db_conn, unit, user) == "done"


def test_match_unit_dependents(db_conn):
    """
    Expect to order units by the number of depending units.
    """

    add_test_subject(db_conn)
    units = list_latest_accepted_units(db_conn, [
        'add', 'subtract', 'multiply', 'divide',
    ])
    deps = match_unit_dependents(units)
    assert len(deps['add']) == 3
    assert len(deps['multiply']) == 1
    assert len(deps['subtract']) == 1
    assert len(deps['divide']) == 0


def test_order(db_conn):
    """
    Expect to order units by the number of depending units.
    """

    add_test_subject(db_conn)
    units = list_latest_accepted_units(db_conn, [
        'add', 'subtract', 'multiply', 'divide',
    ])
    units = order_units_by_need(units)
    entity_ids = [unit['entity_id'] for unit in units]
    assert entity_ids[0] == 'add'
    assert entity_ids[1] in ('subtract', 'multiply')
    assert entity_ids[2] in ('subtract', 'multiply')
    assert entity_ids[3] == 'divide'
