import pytest

xfail = pytest.mark.xfail

from modules.sequencer.traversal import traverse, \
    match_unit_dependents, order_units_by_need, judge
from models.user import User
from models.unit import Unit
from models.set import Set
import rethinkdb as r


def add_test_set(db_conn,
                 users_table=None, units_table=None, responses_table=None,
                 sets_table=None):
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

    if users_table:
        users_table.insert({
            'id': 'user'
        }).run(db_conn)

    if units_table:
        units_table.insert([{
            'entity_id': 'add',
            'status': 'accepted',
            'created': r.now()
        }, {
            'entity_id': 'subtract',
            'require_ids': ['add'],
            'status': 'accepted',
            'created': r.now()
        }, {
            'entity_id': 'multiply',
            'require_ids': ['add'],
            'status': 'accepted',
            'created': r.now()
        }, {
            'entity_id': 'divide',
            'require_ids': ['multiply', 'subtract'],
            'status': 'accepted',
            'created': r.now()
        }]).run(db_conn)

    if responses_table:
        responses_table.insert([{
            'user_id': 'user', 'unit_id': 'add', 'learned': 0.99,
            'created': r.now()
        }, {
            'user_id': 'user', 'unit_id': 'multiply', 'learned': 0.0,
            'created': r.now()
        }, {
            'user_id': 'user', 'unit_id': 'subtract', 'learned': 0.99,
            'created': r.time(2004, 11, 3, 'Z')
        }]).run(db_conn)

    if sets_table:
        sets_table.insert({
            'entity_id': 'set',
            'status': 'accepted',
            'members': [
                {'id': 'add', 'kind': 'unit'},
                {'id': 'subtract', 'kind': 'unit'},
                {'id': 'multiply', 'kind': 'unit'},
                {'id': 'divide', 'kind': 'unit'},
            ]
        }).run(db_conn)


@xfail
def test_traverse(db_conn, units_table, users_table, responses_table,
                  sets_table):
    """
    Expect to take a list of units and traverse them correctly.
    Basic test.
    """

    add_test_set(db_conn,
                 users_table, units_table, responses_table, sets_table)

    set_ = Set.get(db_conn, entity_id='set')
    user = User.get(db_conn, id='user')
    buckets = traverse(db_conn, user, set_)
    assert buckets['diagnose'][0]['entity_id'] == 'divide'
    assert buckets['learn'][0]['entity_id'] == 'multiply'
    assert buckets['review'][0]['entity_id'] == 'subtract'


"""
TODO-3 more traversal tests

traverse
--------
Expect if a node is done, any nodes it requires are left out.
If one node is done, and one is not, continue to the lower node.
Traverse should output units in order.
"""


@xfail
def test_judge_diagnose(db_conn, users_table, units_table, responses_table):
    """
    Expect to add no known ability to "diagnose".
    """

    add_test_set(db_conn, users_table, units_table, responses_table)
    unit = Unit.get(db_conn, entity_id='divide')
    user = User.get(db_conn, id='user')
    assert judge(db_conn, unit, user) == "diagnose"


def test_judge_review(db_conn, users_table, units_table, responses_table):
    """
    Expect to add older, high ability to "review".
    """

    add_test_set(db_conn, users_table, units_table, responses_table)
    unit = Unit.get(db_conn, entity_id='subtract')
    user = User.get(db_conn, id='user')
    assert judge(db_conn, unit, user) == "review"


def test_judge_learn(db_conn, units_table, users_table, responses_table):
    """
    Expect to add known low ability to "learn".
    """

    add_test_set(db_conn, users_table, units_table, responses_table)
    unit = Unit.get(db_conn, entity_id='multiply')
    user = User.get(db_conn, id='user')
    assert judge(db_conn, unit, user) == "learn"


def test_judge_done(db_conn, units_table, users_table, responses_table):
    """
    Expect to show "done".
    """

    add_test_set(db_conn, users_table, units_table, responses_table)
    unit = Unit.get(db_conn, entity_id='add')
    user = User.get(db_conn, id='user')
    assert judge(db_conn, unit, user) == "done"


def test_match_unit_dependents(db_conn, units_table):
    """
    Expect to order units by the number of depending units.
    """

    add_test_set(db_conn, units_table=units_table)
    units = Unit.list_by_entity_ids(db_conn, [
        'add', 'subtract', 'multiply', 'divide',
    ])
    deps = match_unit_dependents(units)
    assert len(deps['add']) == 3
    assert len(deps['multiply']) == 1
    assert len(deps['subtract']) == 1
    assert len(deps['divide']) == 0


def test_order(db_conn, units_table):
    """
    Expect to order units by the number of depending units.
    """

    add_test_set(db_conn, units_table=units_table)
    units = Unit.list_by_entity_ids(db_conn, [
        'add', 'subtract', 'multiply', 'divide',
    ])
    units = order_units_by_need(units)
    entity_ids = [unit['entity_id'] for unit in units]
    assert entity_ids[0] == 'add'
    assert entity_ids[1] in ('subtract', 'multiply')
    assert entity_ids[2] in ('subtract', 'multiply')
    assert entity_ids[3] == 'divide'
