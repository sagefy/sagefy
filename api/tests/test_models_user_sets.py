from models.user_sets import UserSets
import rethinkdb as r


def test_user(db_conn, users_sets_table):
    """
    Expect to require a user ID.
    """

    user_sets, errors = UserSets.insert({
        'set_ids': [
            'A',
            'B',
        ],
    })
    assert len(errors) == 1
    user_sets['user_id'] = 'A'
    user_sets, errors = user_sets.save()
    assert len(errors) == 0


def test_sets(db_conn, users_sets_table):
    """
    Expect to require a list of set IDs.
    """

    user_sets, errors = UserSets.insert({
        'user_id': 'A'
    })
    assert len(errors) == 1
    user_sets['set_ids'] = [
        'A',
        'B',
    ]
    user_sets, errors = user_sets.save()
    assert len(errors) == 0


def test_list_sets(db_conn, users_sets_table, sets_table):
    """
    Expect to list sets a user subscribes to.
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
    users_sets_table.insert({
        'user_id': 'abcd1234',
        'set_ids': [
            'A1',
            'C3',
        ],
        'created': r.now(),
        'modified': r.now(),
    }).run(db_conn)
    uset = UserSets.get(user_id='abcd1234')
    sets = uset.list_sets()
    assert sets[0]['body'] in ('Apple', 'Coconut')
    assert sets[0]['body'] in ('Apple', 'Coconut')
