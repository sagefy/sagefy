import rethinkdb as r
import routes.follow


def test_follow(db_conn, session, cards_table, follows_table):
    """
    Expect to follow an entity.
    """

    cards_table.insert({
        'entity_id': 'ABCD',
        'created': r.now(),
        'modified': r.now(),
        'status': 'accepted',
        'kind': 'video',
    }).run(db_conn)

    request = {
        'cookies': {'session_id': session},
        'params': {
            'entity': {
                'kind': 'card',
                'id': 'ABCD',
            }
        },
        'db_conn': db_conn
    }
    code, response = routes.follow.follow_route(request)
    assert code == 200


def test_follow_401(db_conn, follows_table):
    """
    Expect to fail to follow entity if not logged in.
    """

    request = {
        'params': {
            'entity': {
                'kind': 'card',
                'id': 'ABCD',
            }
        },
        'db_conn': db_conn
    }
    code, response = routes.follow.follow_route(request)
    assert code == 401


def test_follow_400(db_conn, session, follows_table):
    """
    Expect to fail to follow entity if not found entity.
    """

    request = {
        'cookies': {'session_id': session},
        'params': {
            'entity': {
                'kind': 'card',
                'id': '???',
            }
        },
        'db_conn': db_conn
    }
    code, response = routes.follow.follow_route(request)
    assert code == 400
    assert len(response['errors']) == 1


def test_follow_409(db_conn, session, cards_table, follows_table):
    """
    Expect to fail to follow entity if already followed.
    """

    follows_table.insert({
        'id': 'JIkfo034n',
        'user_id': 'abcd1234',
        'entity': {
            'kind': 'card',
            'id': 'JFlsjFm',
        },
    }).run(db_conn)
    cards_table.insert({
        'entity_id': 'JFlsjFm',
        'created': r.now(),
        'modified': r.now(),
        'status': 'accepted',
    }).run(db_conn)

    request = {
        'cookies': {'session_id': session},
        'params': {
            'entity': {
                'kind': 'card',
                'id': 'JFlsjFm',
            }
        },
        'db_conn': db_conn
    }
    code, response = routes.follow.follow_route(request)
    assert code == 400


def test_follow_400(db_conn, session, follows_table):
    """
    Expect to fail to follow entity if the request is nonsense.
    """

    request = {
        'cookies': {'session_id': session},
        'params': {},
        'db_conn': db_conn,
    }
    code, response = routes.follow.follow_route(request)
    assert code == 400


def test_unfollow(db_conn, session, follows_table):
    """
    Expect to unfollow an entity.
    """

    follows_table.insert({
        'id': 'JIkfo034n',
        'user_id': 'abcd1234',
        'entity': {
            'kind': 'card',
            'id': 'JFlsjFm',
        },
    }).run(db_conn)

    request = {
        'cookies': {'session_id': session},
        'db_conn': db_conn
    }
    code, response = routes.follow.unfollow_route(request, 'JIkfo034n')
    assert code == 200


def test_unfollow_401(db_conn, follows_table):
    """
    Expect to fail to unfollow an entity if not logged in.
    """

    code, response = routes.follow.unfollow_route({
        'db_conn': db_conn
    }, 'JIkfo034n')
    assert code == 401


def test_unfollow_404(db_conn, session, follows_table):
    """
    Expect to fail to unfollow an entity if no entity.
    """

    request = {
        'cookies': {'session_id': session},
        'db_conn': db_conn
    }
    code, response = routes.follow.unfollow_route(request, 'JIkfo034n')
    assert code == 404


def test_get_follows(db_conn, session, follows_table):
    """
    Expect to get a list of follows for user.
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

    request = {
        'cookies': {'session_id': session},
        'params': {},
        'db_conn': db_conn,
    }
    code, response = routes.follow.get_follows_route(request)

    assert code == 200
    assert len(response['follows']) == 2


def test_get_follows_401(db_conn, follows_table):
    """
    Expect fail to to get a list of follows for user if not logged in.
    """

    code, response = routes.follow.get_follows_route({
        'params': {},
        'db_conn': db_conn,
    })
    assert code == 401
