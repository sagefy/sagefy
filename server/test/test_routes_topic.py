import pytest
import rethinkdb as r
import routes.topic

xfail = pytest.mark.xfail


def create_topic_in_db(topics_table, db_conn, user_id='abcd1234'):
    topics_table.insert({
        'id': 'wxyz7890',
        'created': r.now(),
        'modified': r.now(),
        'user_id': user_id,
        'name': 'A Modest Proposal',
        'entity': {
            'id': 'efgh5678',
            'kind': 'unit'
        }
    }).run(db_conn)


def test_create_topic(db_conn, session, topics_table, posts_table):
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


def test_create_topic_log_in(db_conn, users_table, topics_table,
                             posts_table):
    """
    Expect create topic to fail when logged out.
    """

    request = {
        'params': {
            'topic': {
                'name': 'An entity',
                'entity': {
                    'kind': 'unit',
                    'id': 'dfgh4567'
                },
            },
            'post': {
                'body': 'Here\'s a pear.',
                'kind': 'post'
            }
        },
        'db_conn': db_conn
    }
    code, response = routes.topic.create_topic_route(request)
    assert code == 401
    assert 'errors' in response


def test_create_topic_no_post(db_conn, users_table, topics_table,
                              posts_table, session):
    """
    Expect create topic to fail without post.
    """

    request = {
        'params': {
            'topic': {
                'name': 'An entity',
                'entity': {
                    'kind': 'unit',
                    'id': 'dfgh4567'
                },
            }
        },
        'cookies': {
            'session_id': session,
        },
        'db_conn': db_conn
    }
    code, response = routes.topic.create_topic_route(request)
    assert code == 400
    assert 'errors' in response


def test_topic_update(db_conn, users_table, topics_table,
                      posts_table, session):
    """
    Expect to update topic name.
    """

    create_topic_in_db(topics_table, db_conn)
    request = {
        'cookies': {
            'session_id': session
        },
        'params': {
            'topic': {
                'name': 'Another entity',
                'topic_id': 'wxyz7890',
            }
        },
        'db_conn': db_conn
    }
    code, response = routes.topic.update_topic_route(request, 'wxyz7890')
    assert code == 200
    assert response['topic']['name'] == 'Another entity'


def test_update_topic_author(db_conn, users_table, topics_table,
                             posts_table, session):
    """
    Expect update topic to require original author.
    """

    create_topic_in_db(topics_table, db_conn, user_id="qwerty")
    request = {
        'cookies': {
            'session_id': session
        },
        'params': {
            'topic': {
                'name': 'Another entity',
                'topic_id': 'wxyz7890',
            }
        },
        'db_conn': db_conn
    }
    code, response = routes.topic.update_topic_route(request, 'wxyz7890')
    assert code == 403
    assert 'errors' in response


@xfail
def test_update_topic_fields(db_conn, users_table, topics_table,
                             posts_table, session):
    """
    Expect update topic to only change name.
    """

    create_topic_in_db(topics_table, db_conn)
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
