import pytest

xfail = pytest.mark.xfail


from test_routes_user import create_user_in_db, login, logout
import json
import rethinkdb as r


def create_topic_in_db(topics_table, db_conn):
    topics_table.insert({
        'id': 'wxyz7890',
        'created': r.now(),
        'modified': r.now(),
        'name': 'A Modest Proposal',
        'entity': {
            'entity_id': 'efgh5678',
            'kind': 'unit'
        }
    }).run(db_conn)


@xfail
def test_search(app, db_conn):
    """
    Expect to search topics by query.
    """
    return False


@xfail
def test_search_filter(app, db_conn):
    """
    Expect to search topics by kind.
    """
    return False


@xfail
def test_search_language(app, db_conn):
    """
    Expect to search topics by language.
    """
    return False


@xfail
def test_search_user(app, db_conn):
    """
    Expect to search topics by user.
    """
    return False


@xfail
def test_search_proposal(app, db_conn):
    """
    Expect to search for proposals
    """
    return False


@xfail
def test_search_sort(app, db_conn):
    """
    Expect to sort topics in search.
    """
    return False


@xfail
def test_search_paginate(app, db_conn):
    """
    Expect to paginate topics in search.
    """
    return False


@xfail
def test_search_blank(app, db_conn):
    """
    Expect a blank search result.
    """
    return False


@xfail
def test_create_topic(app, db_conn):
    """
    Expect to create a topic with post.
    """
    return False


@xfail
def test_create_topic_proposal(app, db_conn):
    """
    Expect to create a topic with proposal.
    """
    return False


@xfail
def test_create_topic_flag(app, db_conn):
    """
    Expect to create topic with a flag.
    """
    return False


@xfail
def test_create_topic_login(app, db_conn):
    """
    Expect create topic to fail when logged out.
    """
    return False


@xfail
def test_create_topic_no_post(app, db_conn):
    """
    Expect create topic to fail without post.
    """
    return False


@xfail
def test_topic_update(app, db_conn):
    """
    Expect to update topic name.
    """
    return False


@xfail
def test_update_topic_author(app, db_conn):
    """
    Expect update topic to require original author.
    """
    return False


@xfail
def test_update_topic_fields(app, db_conn):
    """
    Expect update topic to only change name.
    """
    return False


@xfail
def test_get_posts(app, db_conn):
    """
    Expect to get posts for given topic.
    """
    return False


@xfail
def test_get_posts_not_topic(app, db_conn):
    """
    Expect 404 to get posts for a nonexistant topic.
    """
    return False


@xfail
def test_get_posts_paginate(app, db_conn):
    """
    Expect get posts for topic to paginate.
    """
    return False


@xfail
def test_get_posts_proposal(app, db_conn):
    """
    Expect get posts for topic to render a proposal correctly.
    """
    return False


@xfail
def test_get_posts_votes(app, db_conn):
    """
    Expect get posts for topic to render votes correctly.
    """
    return False


@xfail
def test_create_post(app, db_conn, users_table, topics_table, posts_table):
    """
    Expect create post.
    """
    create_user_in_db(users_table, db_conn)
    create_topic_in_db(topics_table, db_conn)
    with app.test_client() as c:
        login(c)
        response = c.post('/api/topics/wxyz7890/posts', data=json.dumps({
            # Should default to > 'kind': 'post',
            'body': '''A Modest Proposal for Preventing the Children of Poor
                People From Being a Burthen to Their Parents or Country, and
                for Making Them Beneficial to the Publick.''',
        }), content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data.decode('utf-8'))
        assert 'Beneficial to the Publick' in data['post']['body']
        logout(c)


@xfail
def test_create_post_errors(app, db_conn, users_table, topics_table,
                            posts_table):
    """
    Expect create post missing field to show errors.
    """
    create_user_in_db(users_table, db_conn)
    create_topic_in_db(topics_table, db_conn)
    with app.test_client() as c:
        login(c)
        response = c.post('/api/topics/wxyz7890/posts',
                          data=json.dumps({}),
                          content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data.decode('utf-8'))
        assert 'errors' in data
        logout(c)


@xfail
def test_create_post_login(app, db_conn, users_table, topics_table,
                           posts_table):
    """
    Expect create post to require login.
    """
    create_topic_in_db(topics_table, db_conn)
    with app.test_client() as c:
        response = c.post('/api/topics/wxyz7890/posts', data=json.dumps({
            # Should default to > 'kind': 'post',
            'body': '''A Modest Proposal for Preventing the Children of Poor
                People From Being a Burthen to Their Parents or Country, and
                for Making Them Beneficial to the Publick.''',
        }), content_type='application/json')
        assert response.status_code == 401
        data = json.loads(response.data.decode('utf-8'))
        assert 'errors' in data


@xfail
def test_create_post_proposal(app, db_conn, users_table, topics_table,
                              posts_table):
    """
    Expect create post to create a proposal.
    """
    create_user_in_db(users_table, db_conn)
    create_topic_in_db(topics_table, db_conn)
    with app.test_client() as c:
        login(c)
        response = c.post('/api/topics/wxyz7890/posts', data=json.dumps({
            'kind': 'proposal',
            'name': 'New Unit',
            'body': '''A Modest Proposal for Preventing the Children of Poor
                People From Being a Burthen to Their Parents or Country, and
                for Making Them Beneficial to the Publick.''',
            'action': 'create',
            'unit': {
                'name': 'Satire',
                'body': '''Learn the use of humor, irony, exaggeration, or
                ridicule to expose and criticize people's
                stupidity or vices.''',
                'tags': ['literature']
            },
        }), content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data.decode('utf-8'))
        assert data['post']['kind'] == 'proposal'
        logout(c)


@xfail
def test_create_post_vote(app, db_conn, users_table, topics_table,
                          posts_table):
    """
    Expect create post to create a vote.
    """
    create_user_in_db(users_table, db_conn)
    create_topic_in_db(topics_table, db_conn)
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
        'entity_version_id': '1',
        'name': 'New Unit',
        'status': 'pending',
        'action': 'create'
    }).run(db_conn)
    with app.test_client() as c:
        login(c)
        response = c.post('/api/topics/wxyz7890/posts', data=json.dumps({
            'kind': 'vote',
            'body': 'Hooray!',
            'proposal_id': 'jklm',
            'response': True,
        }), content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data.decode('utf-8'))
        assert data['post']['kind'] == 'vote'
        logout(c)


@xfail
def test_update_post_login(app, db_conn):
    """
    Expect update post to require login.
    """
    return False


@xfail
def test_update_post_author(app, db_conn):
    """
    Expect update post to require own post.
    """
    return False


@xfail
def test_update_post_body(app, db_conn):
    """
    Expect update post to change body only for general post.
    """
    return False


@xfail
def test_update_proposal(app, db_conn):
    """
    Expect update post to handle proposals correctly.
    """
    return False
