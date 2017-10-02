import routes.subject
from datetime import datetime, timezone
from raw_insert import raw_insert_subjects, raw_insert_units, raw_insert_topics


def test_get_recommended_subjects_route():
    assert False


def test_get_subject(db_conn):
    """
    Expect to get the subject information for displaying to a contributor.
    """

    raw_insert_units(db_conn, [{
        'entity_id': 'W',
        'name': 'Wood',
        'created': datetime.utcnow(),
        'modified': datetime.utcnow(),
        'status': 'accepted',
    }])

    raw_insert_subjects(db_conn, [{
        'entity_id': 'zytx',
        'created': datetime.utcnow(),
        'modified': datetime.utcnow(),
        'status': 'accepted',
        'name': 'Wildwood',
        'members': [{
            'kind': 'unit',
            'id': 'W'
        }]
    }, {
        'entity_id': 'zytx',
        'created': datetime(1986, 11, 3, tzinfo=timezone.utc),
        'modified': datetime(1986, 11, 3, tzinfo=timezone.utc),
        'status': 'accepted',
        'name': 'Umberwood',
    }])

    raw_insert_topics(db_conn, [{
        'created': datetime.utcnow(),
        'modified': datetime.utcnow(),
        'user_id': 'abcd1234',
        'name': 'A Modest Proposal',
        'entity_id': 'zytx',
        'entity_kind': 'subject',
    }, {
        'created': datetime.utcnow(),
        'modified': datetime.utcnow(),
        'user_id': 'abcd1234',
        'name': 'Another Proposal',
        'entity_id': 'zytx',
        'entity_kind': 'subject',
    }, {
        'created': datetime.utcnow(),
        'modified': datetime.utcnow(),
        'user_id': 'abcd1234',
        'name': 'A Third Proposal',
        'entity_id': 'abcd',
        'entity_kind': 'card',
    }])

    code, response = routes.subject.get_subject_route({
        'db_conn': db_conn
    }, 'zytx')
    assert code == 200
    # Model
    assert response['subject']['entity_id'] == 'zytx'
    assert response['subject']['name'] == 'Wildwood'
    # Units
    assert len(response['units']) == 1
    assert response['units'][0]['entity_id'] == 'W'

    # TODO-3 sequencer: learners, quality, difficulty


def test_get_subject_404(db_conn):
    """
    Expect to fail to get subject information if subject is unknown. (404)
    """

    code, response = routes.subject.get_subject_route({
        'db_conn': db_conn
    }, 'abcd')
    assert code == 404


def test_list_subjects_route():
    assert False


def test_get_subject_versions_route():
    assert False


def test_get_subject_version_route():
    assert False


def test_subject_tree():
    """
    Expect to get subject information in tree format.
    """

    assert False


def test_subject_tree_401():
    """
    Expect to fail to get subject in tree format if not log in. (401)
    """

    assert False


def test_subject_tree_404():
    """
    Expect to fail to get subject in tree format if no subject. (404)
    """

    assert False


def test_subject_tree_400():
    """
    Expect to fail to get subject in tree format
    if parameters don't make sense. (400)
    """

    assert False


def test_subject_units():
    """
    Expect to provide list of units to choose from.
    """

    assert False


def test_subject_units_401():
    """
    Expect to fail to provide list of units if not log in. (401)
    """

    assert False


def test_subject_units_404():
    """
    Expect to fail to provide list of units if subject not found. (404)
    """

    assert False


def test_subject_units_400():
    """
    Expect to fail to provide list of units if request is nonsense. (400)
    """

    assert False


def test_choose_unit():
    """
    Expect to let a learner choose their unit.
    """

    assert False


def test_choose_unit_401():
    """
    Expect to fail to choose unit if not log in. (401)
    """

    assert False


def test_choose_unit_404():
    """
    Expect to fail to choose unit if unit doesn't exist. (404)
    """

    assert False


def test_choose_unit_400():
    """
    Expect to fail to choose unit if request is nonsense. (400)
    """

    assert False


def test_choose_unit_extra():
    """
    Expect choose unit to show time estimate and learning objective.
    """

    assert False


def test_choose_unit_avail():
    """
    Expect choose unit to only show available units. (No requires remaining.)
    """

    assert False


def test_choose_unit_ordering():
    """
    Expect to prefer units with more dependencies in choose unit.
    """

    assert False


def test_get_my_recently_created_subjects_route():
    assert False


def test_create_new_subject_version_route():
    assert False


def test_create_existing_subject_version_route():
    assert False
