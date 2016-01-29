from models.follow import Follow
import rethinkdb as r


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
    follow, errors = Follow.insert(db_conn, {
        'entity': {
            'id': 'A',
            'kind': 'card',
        }
    })
    assert len(errors) == 1
    follow['user_id'] = 'A'
    follow, errors = follow.save(db_conn)
    assert len(errors) == 0


def test_entity(db_conn, cards_table, follows_table):
    """
    Expect a follow to require an entity kind and id.
    """

    create_card_a(db_conn, cards_table)
    follow, errors = Follow.insert(db_conn, {
        'user_id': 'A',
    })
    assert len(errors) == 2
    follow['entity'] = {
        'id': 'A',
        'kind': 'card',
    }
    follow, errors = follow.save(db_conn)
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

    assert len(Follow.list(db_conn, user_id='abcd1234')) == 2
    assert len(Follow.list(db_conn, user_id='JFldl93k')) == 1


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

    assert len(Follow.list(db_conn, kind='card')) == 2
    assert len(Follow.list(db_conn, kind='unit')) == 1


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

    assert len(Follow.list(db_conn, entity_id='JFlsjFm')) == 2
    assert len(Follow.list(db_conn, entity_id='u39Fdjf0')) == 1
