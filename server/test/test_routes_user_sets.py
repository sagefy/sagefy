import routes.user_sets
import rethinkdb as r


def prep(sets_table, users_sets_table, db_conn):
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


def test_get_user_sets(db_conn, session, sets_table, users_sets_table):
    """
    Expect to get a list of the user's sets.
    """

    prep(sets_table, users_sets_table, db_conn)
    request = {
        'cookies': {'session_id': session},
        'params': {},
        'db_conn': db_conn,
    }
    code, response = routes.user_sets.get_user_sets_route(request, 'abcd1234')
    assert code == 200
    assert len(response['sets']) == 2
    assert response['sets'][0]['body'] in ('Apple', 'Coconut')


def test_get_user_sets_401(db_conn, users_sets_table):
    """
    Expect get user sets to 401 when not logged in.
    """

    code, response = routes.user_sets.get_user_sets_route({
        'db_conn': db_conn
    }, 'abcd1234')
    assert code == 401


def test_get_user_sets_403(db_conn, session, users_sets_table):
    """
    Expect to 403 if trying to get other user's sets.
    """

    request = {
        'cookies': {'session_id': session},
        'db_conn': db_conn,
    }
    code, response = routes.user_sets.get_user_sets_route(request, '1234abcd')
    assert code == 403


def test_add_set(db_conn, session, sets_table, users_sets_table):
    """
    Expect to add a set to the user's list.
    """

    sets_table.insert({
        'entity_id': 'A1',
        'name': 'A',
        'body': 'Apple',
        'created': r.now(),
        'modified': r.now(),
        'status': 'accepted',
    }).run(db_conn)

    request = {
        'cookies': {'session_id': session},
        'db_conn': db_conn
    }
    code, response = routes.user_sets.add_set_route(request, 'abcd1234', 'A1')
    assert code == 200
    assert 'A1' in response['sets']


def test_add_set_401(db_conn, users_sets_table):
    """
    Expect to 401 when trying to add a set but not logged in.
    """

    code, response = routes.user_sets.add_set_route({
        'db_conn': db_conn
    }, 'abcd1234', 'A1')
    assert code == 401


def test_add_set_403(db_conn, session, users_sets_table):
    """
    Expect to 403 when attempt to add to another user's sets.
    """

    request = {
        'cookies': {'session_id': session},
        'db_conn': db_conn,
    }
    code, response = routes.user_sets.add_set_route(request, '1234dbca', '2')
    assert code == 403


def test_add_set_404(db_conn, session, users_sets_table):
    """
    Expect to 404 if set not found.
    """

    request = {
        'cookies': {'session_id': session},
        'db_conn': db_conn,
    }
    code, response = routes.user_sets.add_set_route(request, 'abcd1234', 'Z9')
    assert code == 404


def test_add_set_already_added(db_conn, session, sets_table, users_sets_table):
    """
    Expect to 400 if already added set.
    """

    sets_table.insert({
        'entity_id': 'A1',
        'name': 'A',
        'body': 'Apple',
        'created': r.now(),
        'modified': r.now(),
        'status': 'accepted',
    }).run(db_conn)

    request = {
        'cookies': {'session_id': session},
        'db_conn': db_conn,
    }
    code, response = routes.user_sets.add_set_route(request, 'abcd1234', 'A1')
    assert code == 200
    code, response = routes.user_sets.add_set_route(request, 'abcd1234', 'A1')
    assert code == 400


def test_select_set_route(db_conn, session, sets_table, users_sets_table):
    """
    Expect to select a set.
    """

    sets_table.insert({
        'entity_id': 'A1',
        'name': 'A',
        'body': 'Apple',
        'created': r.now(),
        'modified': r.now(),
        'status': 'accepted',
    }).run(db_conn)

    request = {
        'cookies': {'session_id': session},
        'db_conn': db_conn,
    }
    code, response = routes.user_sets.select_set_route(request,
                                                       'abcd1234',
                                                       'A1')
    assert code == 200
    assert response['next']['path'] == '/s/sets/A1/tree'


def test_remove_set(db_conn, session, sets_table, users_sets_table):
    """
    Expect to remove a set from the user's list.
    """

    sets_table.insert({
        'entity_id': 'A1',
        'name': 'A',
        'body': 'Apple',
        'created': r.now(),
        'modified': r.now(),
        'status': 'accepted',
    }).run(db_conn)

    users_sets_table.insert({
        'user_id': 'abcd1234',
        'set_ids': ['A1'],
    }).run(db_conn)

    request = {
        'cookies': {'session_id': session},
        'db_conn': db_conn,
    }
    code, response = routes.user_sets.remove_set_route(request,
                                                       'abcd1234', 'A1')
    assert code == 200


def test_remove_set_401(db_conn, users_sets_table):
    """
    Expect to 401 when trying to remove a user set not logged in.
    """

    request = {
        'db_conn': db_conn,
    }
    code, response = routes.user_sets.remove_set_route(request,
                                                       'abcd1234', 'A1')
    assert code == 401


def test_remove_set_403(db_conn, session, users_sets_table):
    """
    Expect forbidden when trying to remove another user's set.
    """

    request = {
        'cookies': {'session_id': session},
        'db_conn': db_conn,
    }
    code, response = routes.user_sets.remove_set_route(request,
                                                       '1234dcba', '2')
    assert code == 403


def test_remove_set_404(db_conn, session, users_sets_table):
    """
    Expect to not found when trying to delete an unadded set.
    """

    request = {
        'cookies': {'session_id': session},
        'db_conn': db_conn,
    }
    code, response = routes.user_sets.remove_set_route(request,
                                                       'abcd1234', 'A1')
    assert code == 404
