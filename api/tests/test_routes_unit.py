import pytest

xfail = pytest.mark.xfail


import rethinkdb as r
import json


@xfail
def test_get_unit(app, db_conn,
                  units_table, sets_table, topics_table):
    """
    Expect to get the unit information for displaying to a contributor.
    """

    units_table.insert([{
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
            'kind': 'unit'
        }
    }, {
        'created': r.now(),
        'modified': r.now(),
        'user_id': 'abcd1234',
        'name': 'Another Proposal',
        'entity': {
            'id': 'zytx',
            'kind': 'unit'
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

    response = app.test_client().get('/api/units/zytx/')
    assert response.status_code == 200
    response = json.loads(response.data.decode('utf-8'))
    # Model
    assert response['unit']['entity_id'] == 'zytx'
    assert response['unit']['name'] == 'Wildwood'
    # Topics
    assert len(response['topics']) == 2
    assert response['topics'][0]['entity']['kind'] == 'unit'
    # Versions
    assert len(response['versions']) == 2
    assert response['versions'][1]['name'] == 'Umberwood'

    # TODO@ join through requires
    # TODO@ join through sets
    # TODO@ sequencer data: learners, quality, difficulty


def test_get_unit_404(app, db_conn):
    """
    Expect to fail to get an unknown unit (404).
    """

    response = app.test_client().get('/api/units/abcd/')
    assert response.status_code == 404
