
from database.follow import insert_follow, list_follows
# from database.follow import get_follow, \
#     deliver_follow, delete_follow, get_user_ids_by_followed_entity


def create_card_a(db_conn, cards_table):
    """
    Create a unit for the following tests.
    """

    cards_table.insert({
        'entity_id': 'A',
        'status': 'accepted',
    }).run(db_conn)


def test_user_id(db_conn, cards_table, follows_table):
    """
    A follow should require a user_id.
    """

    create_card_a(db_conn, cards_table)
    follow_data = {
        'entity': {
            'id': 'A',
            'kind': 'card',
        }
    }
    follow, errors = insert_follow(follow_data, db_conn)
    assert len(errors) == 1
    follow_data['user_id'] = 'A'
    follow, errors = insert_follow(follow_data, db_conn)
    assert len(errors) == 0


def test_entity(db_conn, cards_table, follows_table):
    """
    Expect a follow to require an entity kind and id.
    """

    create_card_a(db_conn, cards_table)
    follow_data = {
        'user_id': 'A',
    }
    follow, errors = insert_follow(follow_data, db_conn)
    assert len(errors) == 2
    follow_data['entity'] = {
        'id': 'A',
        'kind': 'card',
    }
    follow, errors = insert_follow(follow_data, db_conn)
    assert len(errors) == 0


def test_list_user(db_conn, follows_table):
    """
    Expect to get follows by user id.
    """

    follows_table.insert([{
        'user_id': 'JFldl93k',
        'created': r.now(),
        'modified': r.now(),
        'entity': {
            'kind': 'card',
            'id': 'JFlsjFm',
        },
    }, {
        'user_id': 'abcd1234',
        'created': r.now(),
        'modified': r.now(),
        'entity': {
            'kind': 'card',
            'id': 'JFlsjFm',
        },
    }, {
        'user_id': 'abcd1234',
        'created': r.now(),
        'modified': r.now(),
        'entity': {
            'kind': 'unit',
            'id': 'u39Fdjf0',
        },
    }]).run(db_conn)

    assert len(list_follows({'user_id': 'abcd1234'}, db_conn)) == 2
    assert len(list_follows({'user_id': 'JFldl93k'}, db_conn)) == 1


def test_list_kind(db_conn, follows_table):
    """
    Expect to get follows by kind.
    """

    follows_table.insert([{
        'user_id': 'JFldl93k',
        'created': r.now(),
        'modified': r.now(),
        'entity': {
            'kind': 'card',
            'id': 'JFlsjFm',
        },
    }, {
        'user_id': 'abcd1234',
        'created': r.now(),
        'modified': r.now(),
        'entity': {
            'kind': 'card',
            'id': 'JFlsjFm',
        },
    }, {
        'user_id': 'abcd1234',
        'created': r.now(),
        'modified': r.now(),
        'entity': {
            'kind': 'unit',
            'id': 'u39Fdjf0',
        },
    }]).run(db_conn)

    assert len(list_follows({'kind': 'card'}, db_conn)) == 2
    assert len(list_follows({'kind': 'unit'}, db_conn)) == 1


def test_list_id(db_conn, follows_table):
    """
    Expect to list follows by entity id.
    """

    follows_table.insert([{
        'user_id': 'JFldl93k',
        'created': r.now(),
        'modified': r.now(),
        'entity': {
            'kind': 'card',
            'id': 'JFlsjFm',
        },
    }, {
        'user_id': 'abcd1234',
        'created': r.now(),
        'modified': r.now(),
        'entity': {
            'kind': 'card',
            'id': 'JFlsjFm',
        },
    }, {
        'user_id': 'abcd1234',
        'created': r.now(),
        'modified': r.now(),
        'entity': {
            'kind': 'unit',
            'id': 'u39Fdjf0',
        },
    }]).run(db_conn)

    assert len(list_follows({'entity_id': 'JFlsjFm'}, db_conn)) == 2
    assert len(list_follows({'entity_id': 'u39Fdjf0'}, db_conn)) == 1
