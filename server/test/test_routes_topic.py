from datetime import datetime
import routes.topic
from raw_insert import raw_insert_topics


def create_topic_in_db(db_conn, user_id='abcd1234'):
    raw_insert_topics(db_conn, [{
        'id': 'wxyz7890',
        'created': datetime.utcnow(),
        'modified': datetime.utcnow(),
        'user_id': user_id,
        'name': 'A Modest Proposal',
        'entity': {
            'id': 'efgh5678',
            'kind': 'unit'
        }
    }])


def test_get_topic_route():
    assert False


def test_list_topics_route():
    assert False


def test_create_topic(db_conn, session):
    """
    Expect to create a topic with post.
    """

    request = {
        'params': {
            'name': 'An entity',
            'entity': {
                'kind': 'unit',
                'id': 'dfgh4567'
            },
        },
        'cookies': {
            'session_id': session,
        },
        'db_conn': db_conn
    }
    code, response = routes.topic.create_topic_route(request)
    assert code == 200
    assert 'topic' in response
    assert response['topic']['name'] == 'An entity'


def test_create_topic_log_in(db_conn):
    """
    Expect create topic to fail when logged out.
    """

    request = {
        'params': {
            'name': 'An entity',
            'entity': {
                'kind': 'unit',
                'id': 'dfgh4567'
            },
        },
        'db_conn': db_conn
    }
    code, response = routes.topic.create_topic_route(request)
    assert code == 401
    assert 'errors' in response


def test_topic_update(db_conn, session):
    """
    Expect to update topic name.
    """

    create_topic_in_db(db_conn)
    request = {
        'cookies': {
            'session_id': session
        },
        'params': {
            'name': 'Another entity',
            'topic_id': 'wxyz7890',
        },
        'db_conn': db_conn
    }
    code, response = routes.topic.update_topic_route(request, 'wxyz7890')
    assert code == 200
    assert response['topic']['name'] == 'Another entity'


def test_update_topic_author(db_conn, session):
    """
    Expect update topic to require original author.
    """

    create_topic_in_db(db_conn, user_id="qwerty")
    request = {
        'cookies': {
            'session_id': session
        },
        'params': {
            'name': 'Another entity',
            'topic_id': 'wxyz7890',
        },
        'db_conn': db_conn
    }
    code, response = routes.topic.update_topic_route(request, 'wxyz7890')
    assert code == 403
    assert 'errors' in response


def test_update_topic_fields(db_conn, session):
    """
    Expect update topic to only change name.
    """

    create_topic_in_db(db_conn)
    request = {
        'cookies': {
            'session_id': session
        },
        'params': {
            'name': 'Another entity',
            'topic_id': 'wxyz7890',
            'entity': {
                'kind': 'subject'
            }
        },
        'db_conn': db_conn
    }
    code, response = routes.topic.update_topic_route(request, 'wxyz7890')
    assert code == 400
    assert 'errors' in response
