from models.set import Set
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


def test_entity(db_conn, sets_table, units_table):
    """
    Expect a set to require an entity_id.
    """

    create_unit_a(db_conn, units_table)
    set_, errors = Set.insert(db_conn, {
        'name': 'Statistics',
        'body': 'A beginning course focused on probability.',
        'members': [{
            'id': 'A',
            'kind': 'unit',
        }]
    })
    assert len(errors) == 0
    assert set_['entity_id']


def test_previous(db_conn, sets_table, units_table):
    """
    Expect a set to allow a previous version id.
    """

    create_unit_a(db_conn, units_table)
    set_, errors = Set.insert(db_conn, {
        'name': 'Statistics',
        'body': 'A beginning course focused on probability.',
        'members': [{
            'id': 'A',
            'kind': 'unit',
        }],
        'previous_id': 'fdsjKO',
    })
    assert len(errors) == 0


def test_language(db_conn, sets_table, units_table):
    """
    Expect a set to require a language.
    """

    create_unit_a(db_conn, units_table)
    set_, errors = Set.insert(db_conn, {
        'name': 'Statistics',
        'body': 'A beginning course focused on probability.',
        'members': [{
            'id': 'A',
            'kind': 'unit',
        }],
    })
    assert len(errors) == 0
    assert set_['language'] == 'en'


def test_name(db_conn, sets_table, units_table):
    """
    Expect a set to require a name.
    """

    create_unit_a(db_conn, units_table)
    set_, errors = Set.insert(db_conn, {
        'body': 'A beginning course focused on probability.',
        'members': [{
            'id': 'A',
            'kind': 'unit',
        }],
    })
    assert len(errors) == 1
    set_['name'] = 'Statistics'
    set_, errors = set_.save(db_conn)
    assert len(errors) == 0


def test_body(db_conn, sets_table, units_table):
    """
    Expect a set to require a body.
    """

    create_unit_a(db_conn, units_table)
    set_, errors = Set.insert(db_conn, {
        'name': 'Statistics',
        'members': [{
            'id': 'A',
            'kind': 'unit',
        }],
    })
    assert len(errors) == 1
    set_['body'] = 'A beginning course focused on probability.'
    set_, errors = set_.save(db_conn)
    assert len(errors) == 0


def test_status(db_conn, sets_table, units_table):
    """
    Expect a set status to be a string.
    """

    create_unit_a(db_conn, units_table)
    set_, errors = Set.insert(db_conn, {
        'name': 'Statistics',
        'body': 'A beginning course focused on probability.',
        'members': [{
            'id': 'A',
            'kind': 'unit',
        }],
    })
    assert len(errors) == 0
    assert set_['status'] == 'pending'
    set_['status'] = 'accepted'
    set_, errors = set_.save(db_conn)
    assert len(errors) == 0


def test_tags(db_conn, sets_table, units_table):
    """
    Expect a set to allow tags.
    """

    create_unit_a(db_conn, units_table)
    set_, errors = Set.insert(db_conn, {
        'name': 'Statistics',
        'body': 'A beginning course focused on probability.',
        'members': [{
            'id': 'A',
            'kind': 'unit',
        }],
        'tags': ['A', 'B', 'C']
    })
    assert len(errors) == 0


def test_members(db_conn, sets_table, units_table):
    """
    Expect a set to record a list of members.
    """

    create_unit_a(db_conn, units_table)
    set_, errors = Set.insert(db_conn, {
        'name': 'Statistics',
        'body': 'A beginning course focused on probability.',
    })
    assert len(errors) == 1
    set_['members'] = [{
        'id': 'A',
        'kind': 'unit',
    }]
    set_, errors = set_.save(db_conn)
    assert len(errors) == 0


def test_list_by_entity_ids(db_conn, sets_table):
    """
    Expect to list sets by given entity IDs.
    """

    sets_table.insert([{
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
    sets = Set.list_by_entity_ids(db_conn, ['A1', 'C3'])
    assert sets[0]['body'] in ('Apple', 'Coconut')
    assert sets[0]['body'] in ('Apple', 'Coconut')


def test_list_by_unit_ids(db_conn, units_table, sets_table):
    """
    Expect to get a list of sets which contain the given unit ID.
    Recursive.
    """

    units_table.insert({
        'entity_id': 'Z',
        'created': r.now(),
        'modified': r.now(),
        'status': 'accepted',
        'name': 'Z',
    }).run(db_conn)

    sets_table.insert([{
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
            'kind': 'set',
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
            'kind': 'set',
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
            'kind': 'set',
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
            'kind': 'set',
            'id': 'B1',
        }, {
            'kind': 'set',
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

    sets = Set.list_by_unit_id(db_conn, 'Z')
    set_ids = set(set_['entity_id'] for set_ in sets)
    assert set_ids == {'A', 'B1', 'B2', 'C'}


def test_list_units(db_conn, units_table, sets_table):
    """
    Expect to get a list of units contained within the set.
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

    sets_table.insert([{
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
            'kind': 'set',
            'id': 'T',
        }, {
            'kind': 'unit',
            'id': 'Q',
        }]
    }]).run(db_conn)

    set_ = Set.get(db_conn, entity_id='S')
    cards = set_.list_units(db_conn)
    card_ids = set(card['entity_id'] for card in cards)
    assert card_ids == {'B', 'V', 'Q', 'N'}
