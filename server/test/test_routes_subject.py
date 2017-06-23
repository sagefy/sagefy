import pytest
import rethinkdb as r
import routes.subject


xfail = pytest.mark.xfail


def test_get_subject(db_conn,
                     subjects_table, units_table, topics_table):
    """
    Expect to get the subject information for displaying to a contributor.
    """

    subjects_table.insert([{
        'entity_id': 'zytx',
        'created': r.now(),
        'modified': r.now(),
        'status': 'accepted',
        'name': 'Wildwood',
        'members': [{
            'kind': 'unit',
            'id': 'W'
        }]
    }, {
        'entity_id': 'zytx',
        'created': r.time(1986, 11, 3, 'Z'),
        'modified': r.time(1986, 11, 3, 'Z'),
        'status': 'accepted',
        'name': 'Umberwood',
    }]).run(db_conn)

    units_table.insert({
        'entity_id': 'W',
        'name': 'Wood',
        'created': r.now(),
        'modified': r.now(),
        'status': 'accepted',
    }).run(db_conn)

    topics_table.insert([{
        'created': r.now(),
        'modified': r.now(),
        'user_id': 'abcd1234',
        'name': 'A Modest Proposal',
        'entity': {
            'id': 'zytx',
            'kind': 'subject'
        }
    }, {
        'created': r.now(),
        'modified': r.now(),
        'user_id': 'abcd1234',
        'name': 'Another Proposal',
        'entity': {
            'id': 'zytx',
            'kind': 'subject'
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


@xfail
def test_subject_tree():
    """
    Expect to get subject information in tree format.
    """

    assert False


@xfail
def test_subject_tree_401():
    """
    Expect to fail to get subject in tree format if not log in. (401)
    """

    assert False


@xfail
def test_subject_tree_404():
    """
    Expect to fail to get subject in tree format if no subject. (404)
    """

    assert False


@xfail
def test_subject_tree_400():
    """
    Expect to fail to get subject in tree format
    if parameters don't make sense. (400)
    """

    assert False


@xfail
def test_subject_units():
    """
    Expect to provide list of units to choose from.
    """

    assert False


@xfail
def test_subject_units_401():
    """
    Expect to fail to provide list of units if not log in. (401)
    """

    assert False


@xfail
def test_subject_units_404():
    """
    Expect to fail to provide list of units if subject not found. (404)
    """

    assert False


@xfail
def test_subject_units_400():
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


@xfail
def test_choose_unit_extra():
    """
    Expect choose unit to show time estimate and learning objective.
    """

    assert False


@xfail
def test_choose_unit_avail():
    """
    Expect choose unit to only show available units. (No requires remaining.)
    """

    assert False


@xfail
def test_choose_unit_ordering():
    """
    Expect to prefer units with more dependencies in choose unit.
    """

    assert False
