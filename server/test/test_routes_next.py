import routes.next
from database.user import get_user, set_learning_context


def test_seq_next(db_conn, session):
    """
    Expect sequencer route to say where to go next.
    """

    request = {
        'cookies': {'session_id': session},
        'db_conn': db_conn,
    }
    user = get_user({'id': 'abcd1234'}, db_conn)
    set_learning_context(user, next={
        'method': 'DANCE',
        'path': '/s/unicorns'
    })
    code, response = routes.next.next_route(request)
    assert code == 200
    assert response['next']['method'] == 'DANCE'
    set_learning_context(user, next=None)


def test_seq_next_default(db_conn, session):
    """
    Expect sequencer route to say where to go next if no current state.
    """

    request = {
        'cookies': {'session_id': session},
        'db_conn': db_conn,
    }
    code, response = routes.next.next_route(request)
    assert code == 200
    assert response == {
        'next': {
            'method': 'GET',
            'path': '/s/users/abcd1234/subjects',
        }
    }
