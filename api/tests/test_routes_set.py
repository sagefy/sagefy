import pytest

xfail = pytest.mark.xfail

import rethinkdb as r
import json


def test_get_set(app, db_conn,
                 sets_table, units_table, topics_table):
    """
    Expect to get the set information for displaying to a contributor.
    """

    sets_table.insert([{
        'entity_id': 'zytx',
        'created': r.now(),
        'modified': r.now(),
        'canonical': True,
        'name': 'Wildwood',
    }, {
        'entity_id': 'zytx',
        'created': r.time(1986, 11, 3, 'Z'),
        'modified': r.time(1986, 11, 3, 'Z'),
        'canonical': True,
        'name': 'Umberwood',
    }]).run(db_conn)

    topics_table.insert([{
        'created': r.now(),
        'modified': r.now(),
        'user_id': 'abcd1234',
        'name': 'A Modest Proposal',
        'entity': {
            'id': 'zytx',
            'kind': 'set'
        }
    }, {
        'created': r.now(),
        'modified': r.now(),
        'user_id': 'abcd1234',
        'name': 'Another Proposal',
        'entity': {
            'id': 'zytx',
            'kind': 'set'
        }
    }, {
        'created': r.now(),
        'modified': r.now(),
        'user_id': 'abcd1234',
        'name': 'A Third Proposal',
        'entity': {
            'id': 'abcd',
            'kind': 'card'
        }
    }]).run(db_conn)

    response = app.test_client().get('/api/sets/zytx/')
    assert response.status_code == 200
    response = json.loads(response.data.decode('utf-8'))
    # Model
    assert response['set']['entity_id'] == 'zytx'
    assert response['set']['name'] == 'Wildwood'
    # Topics
    assert len(response['topics']) == 2
    assert response['topics'][0]['entity']['kind'] == 'set'
    # Versions
    assert len(response['versions']) == 2
    assert response['versions'][1]['name'] == 'Umberwood'

    # TODO@ join through units
    # TODO@ sequencer: learners, quality, difficulty


def test_get_set_404(app, db_conn):
    """
    Expect to fail to get set information if set is unknown. (404)
    """

    response = app.test_client().get('/api/sets/abcd/')
    assert response.status_code == 404


@xfail
def test_set_tree():
    """
    Expect to get set information in tree format.
    """

    assert False


@xfail
def test_set_tree_401():
    """
    Expect to fail to get set in tree format if not log in. (401)
    """

    assert False


@xfail
def test_set_tree_404():
    """
    Expect to fail to get set in tree format if no set. (404)
    """

    assert False


@xfail
def test_set_tree_400():
    """
    Expect to fail to get set in tree format
    if parameters don't make sense. (400)
    """

    assert False


@xfail
def test_set_units():
    """
    Expect to provide list of units to choose from.
    """

    assert False


@xfail
def test_set_units_401():
    """
    Expect to fail to provide list of units if not log in. (401)
    """

    assert False


@xfail
def test_set_units_404():
    """
    Expect to fail to provide list of units if set not found. (404)
    """

    assert False


@xfail
def test_set_units_400():
    """
    Expect to fail to provide list of units if request is nonsense. (400)
    """

    assert False


@xfail
def test_choose_unit():
    """
    Expect to let a learner choose their unit.
    """

    assert False


@xfail
def test_choose_unit_401():
    """
    Expect to fail to choose unit if not log in. (401)
    """

    assert False


@xfail
def test_choose_unit_404():
    """
    Expect to fail to choose unit if unit doesn't exist. (404)
    """

    assert False


@xfail
def test_choose_unit_400():
    """
    Expect to fail to choose unit if request is nonsense. (400)
    """

    assert False
