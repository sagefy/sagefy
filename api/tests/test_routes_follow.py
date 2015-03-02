import pytest

xfail = pytest.mark.xfail

import json


@xfail
def test_follow(db_conn, c_user, follows_table):
    """
    Expect to follow an entity.
    """

    response = c_user.post('/api/follows/', data=json.dumps({
        'entity': {
            'kind': 'card',
            'id': 'ABCD',
        }
    }), content_type='application/json')
    response = json.loads(response.data.decode('utf-8'))
    assert response.status_code == 200


@xfail
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
    response = json.loads(response.data.decode('utf-8'))
    assert response.status_code == 401


@xfail
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
    response = json.loads(response.data.decode('utf-8'))
    assert response.status_code == 404


@xfail
def test_follow_409(db_conn, c_user, follows_table):
    """
    Expect to fail to follow entity if already followed.
    """

    response = c_user.post('/api/follows/', data=json.dumps({
        'entity': {
            'kind': 'card',
            'id': 'ABCD',
        }
    }), content_type='application/json')
    response = json.loads(response.data.decode('utf-8'))
    assert response.status_code == 409


@xfail
def test_follow_400(db_conn, c_user, follows_table):
    """
    Expect to fail to follow entity if the request is nonsense.
    """

    response = c_user.post('/api/follows/', data=json.dumps({}),
                           content_type='application/json')
    response = json.loads(response.data.decode('utf-8'))
    assert response.status_code == 400


@xfail
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


@xfail
def test_unfollow_401(db_conn, app, follows_table):
    """
    Expect to fail to unfollow an entity if not logged in.
    """

    response = app.test_client().delete('/api/follows/JIkfo034n/')
    assert response.status_code == 401


@xfail
def test_unfollow_404(db_conn, c_user, follows_table):
    """
    Expect to fail to unfollow an entity if no entity.
    """

    response = c_user.delete('/api/follows/JIkfo034n/')
    assert response.status_code == 404


@xfail
def test_unfollow_400(db_conn, c_user, follows_table):
    """
    Expect to fail to unfollow an entity if request is nonsense.
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
    assert response.status_code == 400


@xfail
def test_get_follows(db_conn, c_user, follows_table):
    """
    Expect to get a list of follows for user.
    """
    follows_table.insert([{
        'user_id': 'JFldl93k',
        'entity': {
            'kind': 'card',
            'id': 'JFlsjFm',
        },
    }, {
        'user_id': 'abcd1234',
        'entity': {
            'kind': 'card',
            'id': 'JFlsjFm',
        },
    }, {
        'user_id': 'abcd1234',
        'entity': {
            'kind': 'unit',
            'id': 'u39Fdjf0',
        },
    }]).run(db_conn)
    response = c_user.get('/api/follows/')
    assert response.status_code == 200
    response = json.loads(response.data.decode('utf-8'))
    assert len(response['follows']) == 2


@xfail
def test_get_follows_401(db_conn, app, follows_table):
    """
    Expect fail to to get a list of follows for user if not logged in.
    """

    response = app.test_client().get('/api/follows/')
    assert response.status_code == 401


@xfail
def test_get_follows_400(db_conn, c_user, follows_table):
    """
    Expect fail to to get a list of follows for user if nonsense params.
    """

    response = c_user.get('/api/follows/?card=abcd1234')
    assert response.status_code == 400
