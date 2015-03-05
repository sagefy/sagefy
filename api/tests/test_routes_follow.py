import json
import rethinkdb as r


def test_follow(db_conn, c_user, cards_table, follows_table):
    """
    Expect to follow an entity.
    """

    cards_table.insert({
        'entity_id': 'ABCD',
        'created': r.now(),
        'modified': r.now(),
        'canonical': True,
    }).run(db_conn)
    response = c_user.post('/api/follows/', data=json.dumps({
        'entity': {
            'kind': 'card',
            'id': 'ABCD',
        }
    }), content_type='application/json')
    assert response.status_code == 200


def test_follow_401(db_conn, app, follows_table):
    """
    Expect to fail to follow entity if not logged in.
    """

    response = app.test_client().post('/api/follows/', data=json.dumps({
        'entity': {
            'kind': 'card',
            'id': 'ABCD',
        }
    }), content_type='application/json')
    assert response.status_code == 401


def test_follow_404(db_conn, c_user, follows_table):
    """
    Expect to fail to follow entity if not found entity.
    """

    response = c_user.post('/api/follows/', data=json.dumps({
        'entity': {
            'kind': 'card',
            'id': '???',
        }
    }), content_type='application/json')
    assert response.status_code == 404


def test_follow_409(db_conn, c_user, cards_table, follows_table):
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
        'canonical': True,
    }).run(db_conn)
    response = c_user.post('/api/follows/', data=json.dumps({
        'entity': {
            'kind': 'card',
            'id': 'JFlsjFm',
        }
    }), content_type='application/json')
    assert response.status_code == 409


def test_follow_400(db_conn, c_user, follows_table):
    """
    Expect to fail to follow entity if the request is nonsense.
    """

    response = c_user.post('/api/follows/', data=json.dumps({}),
                           content_type='application/json')
    assert response.status_code == 400


def test_unfollow(db_conn, c_user, follows_table):
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
    response = c_user.delete('/api/follows/JIkfo034n/')
    assert response.status_code == 204


def test_unfollow_401(db_conn, app, follows_table):
    """
    Expect to fail to unfollow an entity if not logged in.
    """

    response = app.test_client().delete('/api/follows/JIkfo034n/')
    assert response.status_code == 401


def test_unfollow_404(db_conn, c_user, follows_table):
    """
    Expect to fail to unfollow an entity if no entity.
    """

    response = c_user.delete('/api/follows/JIkfo034n/')
    assert response.status_code == 404


def test_get_follows(db_conn, c_user, follows_table):
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
    response = c_user.get('/api/follows/')
    assert response.status_code == 200
    response = json.loads(response.data.decode('utf-8'))
    assert len(response['follows']) == 2


def test_get_follows_401(db_conn, app, follows_table):
    """
    Expect fail to to get a list of follows for user if not logged in.
    """

    response = app.test_client().get('/api/follows/')
    assert response.status_code == 401
