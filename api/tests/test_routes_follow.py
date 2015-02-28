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

    assert False


@xfail
def test_unfollow_401(db_conn, c_user, follows_table):
    """
    Expect to fail to unfollow an entity if not logged in.
    """

    assert False


@xfail
def test_unfollow_404(db_conn, c_user, follows_table):
    """
    Expect to fail to unfollow an entity if no entity.
    """

    assert False


@xfail
def test_unfollow_409(db_conn, c_user, follows_table):
    """
    Expect to fail to unfollow an entity if not followed.
    """

    assert False


@xfail
def test_unfollow_400(db_conn, c_user, follows_table):
    """
    Expect to fail to unfollow an entity if request is nonsense.
    """

    assert False


@xfail
def test_get_follows(db_conn, c_user, follows_table):
    """
    Expect to get a list of follows for user.
    """

    assert False


@xfail
def test_get_follows_401(db_conn, c_user, follows_table):
    """
    Expect fail to to get a list of follows for user if not logged in.
    """

    assert False


@xfail
def test_get_follows_400(db_conn, c_user, follows_table):
    """
    Expect fail to to get a list of follows for user if nonsense params.
    """

    assert False
