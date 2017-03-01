from database.user_sets import insert_user_sets, \
    list_user_sets_entity
# get_user_sets, append_user_sets, remove_user_sets,
import rethinkdb as r


def test_user(db_conn, users_sets_table):
    """
    Expect to require a user ID.
    """

    uset_data = {
        'set_ids': [
            'A',
            'B',
        ],
    }
    user_sets, errors = insert_user_sets(uset_data, db_conn)
    assert len(errors) == 1
    uset_data['user_id'] = 'A'
    user_sets, errors = insert_user_sets(uset_data, db_conn)
    assert len(errors) == 0


def test_sets(db_conn, users_sets_table):
    """
    Expect to require a list of set IDs.
    """

    uset_data = {
        'user_id': 'A'
    }
    user_sets, errors = insert_user_sets(uset_data, db_conn)
    assert len(errors) == 1
    uset_data['set_ids'] = [
        'A',
        'B',
    ]
    user_sets, errors = insert_user_sets(uset_data, db_conn)
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
    users_sets_table.insert({
        'user_id': 'abcd1234',
        'set_ids': [
            'A1',
            'C3',
        ],
        'created': r.now(),
        'modified': r.now(),
    }).run(db_conn)
    user_id = 'abcd1234'
    sets = list_user_sets_entity(user_id, {}, db_conn)
    assert sets[0]['body'] in ('Apple', 'Coconut')
    assert sets[1]['body'] in ('Apple', 'Coconut')
