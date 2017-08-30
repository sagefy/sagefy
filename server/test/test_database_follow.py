
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
    follow, errors = insert_follow(db_conn, follow_data)
    assert len(errors) == 1
    follow_data['user_id'] = 'A'
    follow, errors = insert_follow(db_conn, follow_data)
    assert len(errors) == 0


def test_entity(db_conn, cards_table, follows_table):
    """
    Expect a follow to require an entity kind and id.
    """

    create_card_a(db_conn, cards_table)
    follow_data = {
        'user_id': 'A',
    }
    follow, errors = insert_follow(db_conn, follow_data)
    assert len(errors) == 2
    follow_data['entity'] = {
        'id': 'A',
        'kind': 'card',
    }
    follow, errors = insert_follow(db_conn, follow_data)
    assert len(errors) == 0


def test_list_user(db_conn, follows_table):
    """
    Expect to get follows by user id.
    """

    follows_table.insert([{
        'user_id': 'JFldl93k',
        'created': datetime.utcnow(),
        'modified': datetime.utcnow(),
        'entity': {
            'kind': 'card',
            'id': 'JFlsjFm',
        },
    }, {
        'user_id': 'abcd1234',
        'created': datetime.utcnow(),
        'modified': datetime.utcnow(),
        'entity': {
            'kind': 'card',
            'id': 'JFlsjFm',
        },
    }, {
        'user_id': 'abcd1234',
        'created': datetime.utcnow(),
        'modified': datetime.utcnow(),
        'entity': {
            'kind': 'unit',
            'id': 'u39Fdjf0',
        },
    }]).run(db_conn)

    assert len(db_conn, list_follows({'user_id': 'abcd1234'})) == 2
    assert len(db_conn, list_follows({'user_id': 'JFldl93k'})) == 1


def test_list_kind(db_conn, follows_table):
    """
    Expect to get follows by kind.
    """

    follows_table.insert([{
        'user_id': 'JFldl93k',
        'created': datetime.utcnow(),
        'modified': datetime.utcnow(),
        'entity': {
            'kind': 'card',
            'id': 'JFlsjFm',
        },
    }, {
        'user_id': 'abcd1234',
        'created': datetime.utcnow(),
        'modified': datetime.utcnow(),
        'entity': {
            'kind': 'card',
            'id': 'JFlsjFm',
        },
    }, {
        'user_id': 'abcd1234',
        'created': datetime.utcnow(),
        'modified': datetime.utcnow(),
        'entity': {
            'kind': 'unit',
            'id': 'u39Fdjf0',
        },
    }]).run(db_conn)

    assert len(db_conn, list_follows({'kind': 'card'})) == 2
    assert len(db_conn, list_follows({'kind': 'unit'})) == 1


def test_list_id(db_conn, follows_table):
    """
    Expect to list follows by entity id.
    """

    follows_table.insert([{
        'user_id': 'JFldl93k',
        'created': datetime.utcnow(),
        'modified': datetime.utcnow(),
        'entity': {
            'kind': 'card',
            'id': 'JFlsjFm',
        },
    }, {
        'user_id': 'abcd1234',
        'created': datetime.utcnow(),
        'modified': datetime.utcnow(),
        'entity': {
            'kind': 'card',
            'id': 'JFlsjFm',
        },
    }, {
        'user_id': 'abcd1234',
        'created': datetime.utcnow(),
        'modified': datetime.utcnow(),
        'entity': {
            'kind': 'unit',
            'id': 'u39Fdjf0',
        },
    }]).run(db_conn)

    assert len(db_conn, list_follows({'entity_id': 'JFlsjFm'})) == 2
    assert len(db_conn, list_follows({'entity_id': 'u39Fdjf0'})) == 1
