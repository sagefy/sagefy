import rethinkdb as r

import pytest

xfail = pytest.mark.xfail


def create_unit_a(db_conn, units_table):
    """
    Create a unit for the following tests.
    """

    units_table.insert({
        'entity_id': 'A',
        'status': 'accepted',
    }).run(db_conn)


def test_entity(db_conn, subjects_table, units_table):
    """
    Expect a subject to require an entity_id.
    """

    create_unit_a(db_conn, units_table)
    subject, errors = Subject.insert(db_conn, {
        'name': 'Statistics',
        'body': 'A beginning course focused on probability.',
        'members': [{
            'id': 'A',
            'kind': 'unit',
        }]
    })
    assert len(errors) == 0
    assert subject['entity_id']


def test_previous(db_conn, subjects_table, units_table):
    """
    Expect a subject to allow a previous version id.
    """

    create_unit_a(db_conn, units_table)
    subject, errors = Subject.insert(db_conn, {
        'name': 'Statistics',
        'body': 'A beginning course focused on probability.',
        'members': [{
            'id': 'A',
            'kind': 'unit',
        }],
        'previous_id': 'fdsjKO',
    })
    assert len(errors) == 0


def test_language(db_conn, subjects_table, units_table):
    """
    Expect a subject to require a language.
    """

    create_unit_a(db_conn, units_table)
    subject, errors = Subject.insert(db_conn, {
        'name': 'Statistics',
        'body': 'A beginning course focused on probability.',
        'members': [{
            'id': 'A',
            'kind': 'unit',
        }],
    })
    assert len(errors) == 0
    assert subject['language'] == 'en'


def test_name(db_conn, subjects_table, units_table):
    """
    Expect a subject to require a name.
    """

    create_unit_a(db_conn, units_table)
    subject, errors = Subject.insert(db_conn, {
        'body': 'A beginning course focused on probability.',
        'members': [{
            'id': 'A',
            'kind': 'unit',
        }],
    })
    assert len(errors) == 1
    subject['name'] = 'Statistics'
    subject, errors = subject.save(db_conn)
    assert len(errors) == 0


def test_body(db_conn, subjects_table, units_table):
    """
    Expect a subject to require a body.
    """

    create_unit_a(db_conn, units_table)
    subject, errors = Subject.insert(db_conn, {
        'name': 'Statistics',
        'members': [{
            'id': 'A',
            'kind': 'unit',
        }],
    })
    assert len(errors) == 1
    subject['body'] = 'A beginning course focused on probability.'
    subject, errors = subject.save(db_conn)
    assert len(errors) == 0


def test_status(db_conn, subjects_table, units_table):
    """
    Expect a subject status to be a string.
    """

    create_unit_a(db_conn, units_table)
    subject, errors = Subject.insert(db_conn, {
        'name': 'Statistics',
        'body': 'A beginning course focused on probability.',
        'members': [{
            'id': 'A',
            'kind': 'unit',
        }],
    })
    assert len(errors) == 0
    assert subject['status'] == 'pending'
    subject['status'] = 'accepted'
    subject, errors = subject.save(db_conn)
    assert len(errors) == 0


def test_tags(db_conn, subjects_table, units_table):
    """
    Expect a subject to allow tags.
    """

    create_unit_a(db_conn, units_table)
    subject, errors = Subject.insert(db_conn, {
        'name': 'Statistics',
        'body': 'A beginning course focused on probability.',
        'members': [{
            'id': 'A',
            'kind': 'unit',
        }],
        'tags': ['A', 'B', 'C']
    })
    assert len(errors) == 0


def test_members(db_conn, subjects_table, units_table):
    """
    Expect a subject to record a list of members.
    """

    create_unit_a(db_conn, units_table)
    subject, errors = Subject.insert(db_conn, {
        'name': 'Statistics',
        'body': 'A beginning course focused on probability.',
    })
    assert len(errors) == 0
    subject['members'] = [{
        'id': 'A',
        'kind': 'unit',
    }]
    subject, errors = subject.save(db_conn)
    assert len(errors) == 0


def test_list_by_entity_ids(db_conn, subjects_table):
    """
    Expect to list subjects by given entity IDs.
    """

    subjects_table.insert([{
        'entity_id': 'A1',
        'name': 'A',
        'body': 'Apple',
        'created': r.now(),
        'modified': r.now(),
        'status': 'accepted',
    }, {
        'entity_id': 'B2',
        'name': 'B',
        'body': 'Banana',
        'created': r.now(),
        'modified': r.now(),
        'status': 'accepted',
    }, {
        'entity_id': 'C3',
        'name': 'C',
        'body': 'Coconut',
        'created': r.now(),
        'modified': r.now(),
        'status': 'accepted',
    }, {
        'entity_id': 'D4',
        'name': 'D',
        'body': 'Date',
        'created': r.now(),
        'modified': r.now(),
        'status': 'accepted',
    }]).run(db_conn)
    subjects = Subject.list_by_entity_ids(db_conn, ['A1', 'C3'])
    assert subjects[0]['body'] in ('Apple', 'Coconut')
    assert subjects[0]['body'] in ('Apple', 'Coconut')


def test_list_by_unit_ids(db_conn, units_table, subjects_table):
    """
    Expect to get a list of subjects which contain the given unit ID.
    Recursive.
    """

    units_table.insert({
        'entity_id': 'Z',
        'created': r.now(),
        'modified': r.now(),
        'status': 'accepted',
        'name': 'Z',
    }).run(db_conn)

    subjects_table.insert([{
        'entity_id': 'A',
        'name': 'Apple',
        'body': 'Apple',
        'created': r.now(),
        'modified': r.now(),
        'status': 'accepted',
        'members': [{
            'kind': 'unit',
            'id': 'Z',
        }]
    }, {
        'entity_id': 'B1',
        'name': 'Banana',
        'body': 'Banana',
        'created': r.now(),
        'modified': r.now(),
        'status': 'accepted',
        'members': [{
            'kind': 'subject',
            'id': 'A',
        }]
    }, {
        'entity_id': 'B2',
        'name': 'Blueberry',
        'body': 'Blueberry',
        'created': r.now(),
        'modified': r.now(),
        'status': 'accepted',
        'members': [{
            'kind': 'subject',
            'id': 'A',
        }]
    }, {
        'entity_id': 'B3',
        'name': 'Brazil Nut',
        'body': 'Brazil Nut',
        'created': r.now(),
        'modified': r.now(),
        'status': 'accepted',
        'members': [{
            'kind': 'subject',
            'id': 'N',
        }]
    }, {
        'entity_id': 'C',
        'name': 'Coconut',
        'body': 'Coconut',
        'created': r.now(),
        'modified': r.now(),
        'status': 'accepted',
        'members': [{
            'kind': 'subject',
            'id': 'B1',
        }, {
            'kind': 'subject',
            'id': 'B2',
        }]
    }, {
        'entity_id': 'D',
        'name': 'Date',
        'body': 'Date',
        'created': r.now(),
        'modified': r.now(),
        'status': 'accepted'
    }]).run(db_conn)

    subjects = Subject.list_by_unit_id(db_conn, 'Z')
    subject_ids = set(subject['entity_id'] for subject in subjects)
    assert subject_ids == {'A', 'B1', 'B2', 'C'}


def test_list_units(db_conn, units_table, subjects_table):
    """
    Expect to get a list of units contained within the subject.
    Recursive.
    """

    units_table.insert([{
        'entity_id': 'B',
        'name': 'B',
        'created': r.now(),
        'modified': r.now(),
        'status': 'accepted',
        'require_ids': ['A', 'N']
    }, {
        'entity_id': 'V',
        'name': 'V',
        'created': r.now(),
        'modified': r.now(),
        'status': 'accepted',
        'require_ids': ['Q']
    }, {
        'entity_id': 'Q',
        'name': 'Q',
        'created': r.now(),
        'modified': r.now(),
        'status': 'accepted',
    }, {
        'entity_id': 'A',
        'name': 'A',
        'created': r.now(),
        'modified': r.now(),
        'status': 'accepted',
    }, {
        'entity_id': 'N',
        'name': 'N',
        'created': r.now(),
        'modified': r.now(),
        'status': 'accepted',
        'require_ids': ['Q', 'A']
    }]).run(db_conn)

    subjects_table.insert([{
        'entity_id': 'T',
        'name': 'TRex',
        'body': 'TRex',
        'created': r.now(),
        'modified': r.now(),
        'status': 'accepted',
        'members': [{
            'kind': 'unit',
            'id': 'B',
        }, {
            'kind': 'unit',
            'id': 'V',
        }]
    }, {
        'entity_id': 'S',
        'name': 'Saurus',
        'body': 'Saurus',
        'created': r.now(),
        'modified': r.now(),
        'status': 'accepted',
        'members': [{
            'kind': 'subject',
            'id': 'T',
        }, {
            'kind': 'unit',
            'id': 'Q',
        }]
    }]).run(db_conn)

    subject = Subject.get(db_conn, entity_id='S')
    cards = subject.list_units(db_conn)
    card_ids = set(card['entity_id'] for card in cards)
    assert card_ids == {'B', 'V', 'Q', 'N'}
