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


def create_post_in_db(posts_table, db_conn, user_id='abcd1234'):
    posts_table.insert({
        'id': 'jklm',
        'created': r.now(),
        'modified': r.now(),
        'user_id': user_id,
        'topic_id': 'wxyz7890',
        'body': '''A Modest Proposal for Preventing the Children of Poor
            People From Being a Burthen to Their Parents or Country, and
            for Making Them Beneficial to the Publick.''',
        'kind': 'post',
    }).run(db_conn)


def create_proposal_in_db(posts_table, units_table, db_conn):
    posts_table.insert({
        'id': 'jklm',
        'created': r.now(),
        'modified': r.now(),
        'user_id': 'abcd1234',
        'topic_id': 'wxyz7890',
        'body': '''A Modest Proposal for Preventing the Children of Poor
            People From Being a Burthen to Their Parents or Country, and
            for Making Them Beneficial to the Publick.''',
        'kind': 'proposal',
        'name': 'New Unit',
        'replies_to_id': None,
        'entity_versions': [{
            'id': 'slash-1',
            'kind': 'unit',
        }],
    }).run(db_conn)

    units_table.insert({
        'id': 'slash-1',
        'created': r.time(2014, 1, 1, 'Z'),
        'modified': r.time(2014, 1, 1, 'Z'),
        'entity_id': 'slash',
        'previous_id': None,
        'language': 'en',
        'name': 'Dividing two numbers.',
        'status': 'accepted',
        'available': True,
        'tags': ['math'],
        'body': 'The joy and pleasure of dividing numbers.',
        'require_ids': ['plus', 'minus', 'times'],
    }).run(db_conn)


def test_create_topic(db_conn, session, topics_table, posts_table):
    """
    Expect to create a topic with post.
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
        'cookies': {
            'session_id': session,
        },
        'db_conn': db_conn
    }
    code, response = routes.topic.create_topic_route(request)
    assert code == 200
    assert 'post' in response
    assert 'topic' in response
    assert response['topic']['name'] == 'An entity'
    assert response['post']['body'] == 'Here\'s a pear.'


@xfail
def test_create_topic_proposal(db_conn, users_table, topics_table,
                               posts_table, session):
    """
    Expect to create a topic with proposal.
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
                'kind': 'proposal',
                'body': 'Here\'s a pear.'
            }
        },
        'cookies': {
            'session_id': session,
        },
        'db_conn': db_conn
    }
    code, response = routes.topic.create_topic_route(request)
    assert code == 200
    assert 'post' in response
    assert 'topic' in response
    assert response['topic']['name'] == 'An entity'
    assert response['post']['body'] == 'Here\'s a pear.'


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
