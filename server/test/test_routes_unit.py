import rethinkdb as r
import routes.unit


def test_get_unit(db_conn,
                  units_table, subjects_table, topics_table):
    """
    Expect to get the unit information for displaying to a contributor.
    """

    units_table.insert([{
        'entity_id': 'zytx',
        'created': r.now(),
        'modified': r.now(),
        'status': 'accepted',
        'name': 'Wildwood',
        'require_ids': ['ntza'],
    }, {
        'entity_id': 'zytx',
        'created': r.time(1986, 11, 3, 'Z'),
        'modified': r.time(1986, 11, 3, 'Z'),
        'status': 'accepted',
        'name': 'Umberwood',
    }, {
        'entity_id': 'ntza',
        'created': r.time(1986, 11, 3, 'Z'),
        'modified': r.time(1986, 11, 3, 'Z'),
        'status': 'accepted',
        'name': 'Limberwood',
    }, {
        'entity_id': 'tyui',
        'created': r.now(),
        'modified': r.now(),
        'status': 'accepted',
        'name': 'Wildwood',
        'require_ids': ['zytx'],
    }]).run(db_conn)

    subjects_table.insert({
        'entity_id': 'W',
        'name': 'Woods',
        'created': r.now(),
        'modified': r.now(),
        'status': 'accepted',
        'members': [{
            'kind': 'unit',
            'id': 'zytx',
        }]
    }).run(db_conn)

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

    code, response = routes.unit.get_unit_route({
        'db_conn': db_conn
    }, 'zytx')
    assert code == 200
    # Model
    assert response['unit']['entity_id'] == 'zytx'
    assert response['unit']['name'] == 'Wildwood'
    # Requires
    assert len(response['requires']) == 1
    assert response['requires'][0]['entity_id'] == 'ntza'
    # Required By
    assert len(response['required_by']) == 1
    assert response['required_by'][0]['entity_id'] == 'tyui'
    # Subjects
    assert len(response['belongs_to']) == 1
    assert response['belongs_to'][0]['entity_id'] == 'W'
    # TODO-3 sequencer data: learners, quality, difficulty


def test_get_unit_404(db_conn):
    """
    Expect to fail to get an unknown unit (404).
    """

    code, response = routes.unit.get_unit_route({
        'db_conn': db_conn
    }, 'zytx')
    assert code == 404
