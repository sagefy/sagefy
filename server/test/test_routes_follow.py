import routes.follow
from datetime import datetime
from raw_insert import raw_insert_follows, raw_insert_cards


def test_list_follows_route(db_conn, session):
    """
    Expect to get a list of follows for user.
    """
    raw_insert_follows(db_conn, [{
        'user_id': 'JFldl93k',
        'created': datetime.utcnow(),
        'modified': datetime.utcnow(),
        'entity_kind': 'card',
        'entity_id': 'JFlsjFm',
    }, {
        'user_id': 'abcd1234',
        'created': datetime.utcnow(),
        'modified': datetime.utcnow(),
        'entity_kind': 'card',
        'entity_id': 'JFlsjFm',
    }, {
        'user_id': 'abcd1234',
        'created': datetime.utcnow(),
        'modified': datetime.utcnow(),
        'entity_kind': 'unit',
        'entity_id': 'u39Fdjf0',
    }])

    request = {
        'cookies': {'session_id': session},
        'params': {},
        'db_conn': db_conn,
    }
    code, response = routes.follow.get_follows_route(request)

    assert code == 200
    assert len(response['follows']) == 2


def test_list_follows_route_401(db_conn):
    """
    Expect fail to to get a list of follows for user if not logged in.
    """

    code, response = routes.follow.get_follows_route({
        'params': {},
        'db_conn': db_conn,
    })
    assert code == 401


def test_follow(db_conn, session):
    """
    Expect to follow an entity.
    """

    raw_insert_cards(db_conn, [{
        'entity_id': 'ABCD',
        'created': datetime.utcnow(),
        'modified': datetime.utcnow(),
        'status': 'accepted',
        'kind': 'video',
    }])

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


def test_follow_401(db_conn):
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


def test_follow_400a(db_conn, session):
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


def test_follow_409(db_conn, session):
    """
    Expect to fail to follow entity if already followed.
    """

    raw_insert_cards(db_conn, [{
        'entity_id': 'JFlsjFm',
        'created': datetime.utcnow(),
        'modified': datetime.utcnow(),
        'status': 'accepted',
    }])
    raw_insert_follows(db_conn, [{
        'id': 'JIkfo034n',
        'user_id': 'abcd1234',
        'entity_kind': 'card',
        'entity_id': 'JFlsjFm',
    }])

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


def test_follow_400b(db_conn, session):
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


def test_unfollow(db_conn, session):
    """
    Expect to unfollow an entity.
    """

    raw_insert_follows(db_conn, [{
        'id': 'JIkfo034n',
        'user_id': 'abcd1234',
        'entity_kind': 'card',
        'entity_id': 'JFlsjFm',
    }])

    request = {
        'cookies': {'session_id': session},
        'db_conn': db_conn
    }
    code, response = routes.follow.unfollow_route(request, 'JIkfo034n')
    assert code == 200


def test_unfollow_401(db_conn):
    """
    Expect to fail to unfollow an entity if not logged in.
    """

    code, response = routes.follow.unfollow_route({
        'db_conn': db_conn
    }, 'JIkfo034n')
    assert code == 401


def test_unfollow_404(db_conn, session):
    """
    Expect to fail to unfollow an entity if no entity.
    """

    request = {
        'cookies': {'session_id': session},
        'db_conn': db_conn
    }
    code, response = routes.follow.unfollow_route(request, 'JIkfo034n')
    assert code == 404
