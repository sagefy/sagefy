from models.follow import Follow
import rethinkdb as r


def test_user_id(app, db_conn, follows_table):
    """
    A follow should require a user_id.
    """

    follow, errors = Follow.insert({
        'entity': {
            'id': 'A',
            'kind': 'card',
        }
    })
    assert len(errors) == 1
    follow['user_id'] = 'A'
    follow, errors = follow.save()
    assert len(errors) == 0


def test_entity(app, db_conn, follows_table):
    """
    Expect a follow to require an entity kind and id.
    """

    follow, errors = Follow.insert({
        'user_id': 'A',
    })
    assert len(errors) == 2
    follow['entity'] = {
        'id': 'A',
        'kind': 'card',
    }
    follow, errors = follow.save()
    assert len(errors) == 0


def test_list_user(app, db_conn, follows_table):
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

    assert len(Follow.list(user_id='abcd1234')) == 2
    assert len(Follow.list(user_id='JFldl93k')) == 1


def test_list_kind(app, db_conn, follows_table):
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

    assert len(Follow.list(kind='card')) == 2
    assert len(Follow.list(kind='unit')) == 1


def test_list_id(app, db_conn, follows_table):
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

    assert len(Follow.list(entity_id='JFlsjFm')) == 2
    assert len(Follow.list(entity_id='u39Fdjf0')) == 1
