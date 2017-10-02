import routes.unit
from datetime import datetime, timezone
from raw_insert import raw_insert_units, raw_insert_subjects, raw_insert_topics


def test_get_unit(db_conn):
    """
    Expect to get the unit information for displaying to a contributor.
    """

    raw_insert_units(db_conn, [{
        'entity_id': 'zytx',
        'created': datetime.utcnow(),
        'modified': datetime.utcnow(),
        'status': 'accepted',
        'name': 'Wildwood',
        'require_ids': ['ntza'],
    }, {
        'entity_id': 'zytx',
        'created': datetime(1986, 11, 3, tzinfo=timezone.utc),
        'modified': datetime(1986, 11, 3, tzinfo=timezone.utc),
        'status': 'accepted',
        'name': 'Umberwood',
    }, {
        'entity_id': 'ntza',
        'created': datetime(1986, 11, 3, tzinfo=timezone.utc),
        'modified': datetime(1986, 11, 3, tzinfo=timezone.utc),
        'status': 'accepted',
        'name': 'Limberwood',
    }, {
        'entity_id': 'tyui',
        'created': datetime.utcnow(),
        'modified': datetime.utcnow(),
        'status': 'accepted',
        'name': 'Wildwood',
        'require_ids': ['zytx'],
    }])

    raw_insert_subjects(db_conn, {
        'entity_id': 'W',
        'name': 'Woods',
        'created': datetime.utcnow(),
        'modified': datetime.utcnow(),
        'status': 'accepted',
        'members': [{
            'kind': 'unit',
            'id': 'zytx',
        }]
    })

    raw_insert_topics(db_conn, [{
        'created': datetime.utcnow(),
        'modified': datetime.utcnow(),
        'user_id': 'abcd1234',
        'name': 'A Modest Proposal',
        'entity_id': 'zytx',
        'entity_kind': 'unit',
    }, {
        'created': datetime.utcnow(),
        'modified': datetime.utcnow(),
        'user_id': 'abcd1234',
        'name': 'Another Proposal',
        'entity_id': 'zytx',
        'entity_kind': 'unit',
    }, {
        'created': datetime.utcnow(),
        'modified': datetime.utcnow(),
        'user_id': 'abcd1234',
        'name': 'A Third Proposal',
        'entity_id': 'abcd',
        'entity_kind': 'card',
    }])

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
