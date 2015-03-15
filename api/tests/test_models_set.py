from models.set import Set
import rethinkdb as r

import pytest

xfail = pytest.mark.xfail


def test_entity(app, db_conn, sets_table):
    """
    Expect a set to require an entity_id.
    """

    set_, errors = Set.insert({
        'name': 'Statistics',
        'body': 'A beginning course focused on probability.',
        'members': [{
            'id': 'A',
            'kind': 'unit',
        }]
    })
    assert len(errors) == 0
    assert set_['entity_id']


def test_previous(app, db_conn, sets_table):
    """
    Expect a set to allow a previous version id.
    """

    set_, errors = Set.insert({
        'name': 'Statistics',
        'body': 'A beginning course focused on probability.',
        'members': [{
            'id': 'A',
            'kind': 'unit',
        }],
        'previous_id': 'fdsjKO',
    })
    assert len(errors) == 0


def test_language(app, db_conn, sets_table):
    """
    Expect a set to require a language.
    """

    set_, errors = Set.insert({
        'name': 'Statistics',
        'body': 'A beginning course focused on probability.',
        'members': [{
            'id': 'A',
            'kind': 'unit',
        }],
    })
    assert len(errors) == 0
    assert set_['language'] == 'en'


def test_name(app, db_conn, sets_table):
    """
    Expect a set to require a name.
    """

    set_, errors = Set.insert({
        'body': 'A beginning course focused on probability.',
        'members': [{
            'id': 'A',
            'kind': 'unit',
        }],
    })
    assert len(errors) == 1
    set_['name'] = 'Statistics'
    set_, errors = set_.save()
    assert len(errors) == 0


def test_body(app, db_conn, sets_table):
    """
    Expect a set to require a body.
    """

    set_, errors = Set.insert({
        'name': 'Statistics',
        'members': [{
            'id': 'A',
            'kind': 'unit',
        }],
    })
    assert len(errors) == 1
    set_['body'] = 'A beginning course focused on probability.'
    set_, errors = set_.save()
    assert len(errors) == 0


def test_canonical(app, db_conn, sets_table):
    """
    Expect a set canonical to be a boolean.
    """

    set_, errors = Set.insert({
        'name': 'Statistics',
        'body': 'A beginning course focused on probability.',
        'members': [{
            'id': 'A',
            'kind': 'unit',
        }],
    })
    assert len(errors) == 0
    assert set_['canonical'] is False
    set_['canonical'] = True
    set_, errors = set_.save()
    assert len(errors) == 0


def test_tags(app, db_conn, sets_table):
    """
    Expect a set to allow tags.
    """

    set_, errors = Set.insert({
        'name': 'Statistics',
        'body': 'A beginning course focused on probability.',
        'members': [{
            'id': 'A',
            'kind': 'unit',
        }],
        'tags': ['A', 'B', 'C']
    })
    assert len(errors) == 0


def test_members(app, db_conn, sets_table):
    """
    Expect a set to record a list of members.
    """

    set_, errors = Set.insert({
        'name': 'Statistics',
        'body': 'A beginning course focused on probability.',
    })
    assert len(errors) == 1
    set_['members'] = [{
        'id': 'A',
        'kind': 'unit',
    }]
    set_, errors = set_.save()
    assert len(errors) == 0


def test_list_by_entity_ids(app, db_conn, sets_table):
    """
    Expect to list sets by given entity IDs.
    """

    sets_table.insert([{
        'entity_id': 'A1',
        'name': 'A',
        'body': 'Apple',
        'created': r.now(),
        'modified': r.now(),
        'canonical': True,
    }, {
        'entity_id': 'B2',
        'name': 'B',
        'body': 'Banana',
        'created': r.now(),
        'modified': r.now(),
        'canonical': True,
    }, {
        'entity_id': 'C3',
        'name': 'C',
        'body': 'Coconut',
        'created': r.now(),
        'modified': r.now(),
        'canonical': True,
    }, {
        'entity_id': 'D4',
        'name': 'D',
        'body': 'Date',
        'created': r.now(),
        'modified': r.now(),
        'canonical': True,
    }]).run(db_conn)
    sets = Set.list_by_entity_ids(['A1', 'C3'])
    assert sets[0]['body'] in ('Apple', 'Coconut')
    assert sets[0]['body'] in ('Apple', 'Coconut')


@xfail
def test_list_by_unit_ids(app, db_conn, units_table, sets_table):
    """
    Expect to get a list of sets which contain the given unit ID.
    Recursive.
    """

    assert False


@xfail
def test_list_units(app, db_conn, units_table, sets_table):
    """
    Expect to get a list of units contained within the set.
    Recursive.
    """

    assert False
