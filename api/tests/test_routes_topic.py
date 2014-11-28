import pytest

xfail = pytest.mark.xfail


from conftest import create_user_in_db
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


def create_proposal_in_db(posts_table, db_conn):
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


@xfail
def test_create_topic(app, db_conn, clogin, topics_table, posts_table):
    """
    Expect to create a topic with post.
    """
    response = clogin.post('/api/topics', data=json.dumps({
        'name': 'An entity',
        'entity': {
            'kind': 'unit',
            'entity_id': 'dfgh4567'
        },
        'post': {
            'body': 'Here\'s a pear.'
        }
    }), content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data.decode('utf-8'))
    assert 'post' in data
    assert 'topic' in data
    assert data['topic']['name'] == 'An entity'
    assert data['post']['body'] == 'Here\'s a pear.'


@xfail
def test_create_topic_proposal(app, db_conn, users_table, topics_table,
                               posts_table, clogin):
    """
    Expect to create a topic with proposal.
    """
    response = clogin.post('/api/topics', data=json.dumps({
        'name': 'An entity',
        'entity': {
            'kind': 'unit',
            'entity_id': 'dfgh4567'
        },
        'post': {
            'kind': 'proposal',
            'body': 'Here\'s a pear.'
        }
    }), content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data.decode('utf-8'))
    assert 'post' in data
    assert 'topic' in data
    assert data['topic']['name'] == 'An entity'
    assert data['post']['body'] == 'Here\'s a pear.'


@xfail
def test_create_topic_flag(app, db_conn, users_table, topics_table,
                           posts_table, clogin):
    """
    Expect to create topic with a flag.
    """
    response = clogin.post('/api/topics', data=json.dumps({
        'name': 'An entity',
        'entity': {
            'kind': 'unit',
            'entity_id': 'dfgh4567'
        },
        'post': {
            'kind': 'flag',
            'reason': 'duplicate',
        }
    }), content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data.decode('utf-8'))
    assert 'post' in data
    assert 'topic' in data
    assert data['topic']['name'] == 'An entity'
    assert data['post']['body'] == 'Here\'s a pear.'


@xfail
def test_create_topic_login(app, db_conn, users_table, topics_table,
                            posts_table):
    """
    Expect create topic to fail when logged out.
    """
    with app.test_client() as c:
        response = c.post('/api/topics', data=json.dumps({
            'name': 'An entity',
            'entity': {
                'kind': 'unit',
                'entity_id': 'dfgh4567'
            },
            'post': {
                'body': 'Here\'s a pear.'
            }
        }), content_type='application/json')
        assert response.status_code == 401
        data = json.loads(response.data.decode('utf-8'))
        assert 'errors' in data


@xfail
def test_create_topic_no_post(app, db_conn, users_table, topics_table,
                              posts_table, clogin):
    """
    Expect create topic to fail without post.
    """
    response = clogin.post('/api/topics', data=json.dumps({
        'name': 'An entity',
        'entity': {
            'kind': 'unit',
            'entity_id': 'dfgh4567'
        }
    }), content_type='application/json')
    assert response.status_code == 400
    data = json.loads(response.data.decode('utf-8'))
    assert 'errors' in data


@xfail
def test_topic_update(app, db_conn, users_table, topics_table,
                      posts_table, clogin):
    """
    Expect to update topic name.
    """
    create_topic_in_db(topics_table, db_conn)
    response = clogin.put('/api/topics', data=json.dumps({
        'name': 'Another entity',
    }), content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data.decode('utf-8'))
    assert data['topic']['name'] == 'Another entity'


@xfail
def test_update_topic_author(app, db_conn, users_table, topics_table,
                             posts_table, clogin):
    """
    Expect update topic to require original author.
    """
    create_topic_in_db(topics_table, db_conn)
    response = clogin.put('/api/topics', data=json.dumps({
        'name': 'Another entity',
    }), content_type='application/json')
    assert response.status_code == 403
    data = json.loads(response.data.decode('utf-8'))
    assert 'errors' in data


@xfail
def test_update_topic_fields(app, db_conn, users_table, topics_table,
                             posts_table, clogin):
    """
    Expect update topic to only change name.
    """
    create_topic_in_db(topics_table, db_conn)
    response = clogin.put('/api/topics', data=json.dumps({
        'entity': {
            'kind': 'set'
        }
    }), content_type='application/json')
    assert response.status_code == 400
    data = json.loads(response.data.decode('utf-8'))
    assert 'errors' in data


@xfail
def test_get_posts(app, db_conn, users_table, topics_table, posts_table):
    """
    Expect to get posts for given topic.
    """
    create_user_in_db(users_table, db_conn)
    create_topic_in_db(topics_table, db_conn)
    posts_table.insert([{
        'id': 'jklm',
        'created': r.now(),
        'modified': r.now(),
        'user_id': 'abcd1234',
        'topic_id': 'wxyz7890',
        'body': '''A Modest Proposal for Preventing the Children of Poor
            People From Being a Burthen to Their Parents or Country, and
            for Making Them Beneficial to the Publick.''',
        'kind': 'post',
    }, {
        'id': 'tyui',
        'created': r.now(),
        'modified': r.now(),
        'user_id': 'abcd1234',
        'topic_id': 'wxyz7890',
        'body': 'A follow up.',
        'kind': 'post',
    }]).run(db_conn)
    with app.test_client() as c:
        response = c.get('/api/topics/wxyz7890/posts')
        assert response.status_code == 200
        data = json.loads(response.data.decode('utf-8'))
        assert 'Beneficial to the Publick' in data['posts'][0]['body']
        assert 'Beneficial to the Publick' in data['posts'][1]['body']


@xfail
def test_get_posts_not_topic(app, db_conn, users_table, topics_table,
                             posts_table):
    """
    Expect 404 to get posts for a nonexistant topic.
    """
    with app.test_client() as c:
        response = c.get('/api/topics/wxyz7890/posts')
        assert response.status_code == 404


@xfail
def test_get_posts_paginate(app, db_conn, users_table, topics_table,
                            posts_table):
    """
    Expect get posts for topic to paginate.
    """
    create_user_in_db(users_table, db_conn)
    create_topic_in_db(topics_table, db_conn)
    for i in range(0, 25):
        posts_table.insert({
            'id': 'jklm%s' % i,
            'created': r.now(),
            'modified': r.now(),
            'user_id': 'abcd1234',
            'topic_id': 'wxyz7890',
            'body': 'test %s' % i,
            'kind': 'post',
        }).run(db_conn)
    with app.test_client() as c:
        response = c.get('/api/topics/wxyz7890/posts')
        assert response.status_code == 200
        data = json.loads(response.data.decode('utf-8'))
        assert len(data['posts']) == 10
        response = c.get('/api/notices/?skip=20')
        data = json.loads(response.data.decode('utf-8'))
        assert len(data['posts']) == 5


@xfail
def test_get_posts_proposal(app, db_conn, users_table, topics_table,
                            posts_table):
    """
    Expect get posts for topic to render a proposal correctly.
    """
    create_user_in_db(users_table, db_conn)
    create_topic_in_db(topics_table, db_conn)
    create_proposal_in_db(posts_table, db_conn)
    with app.test_client() as c:
        response = c.get('/api/topics/wxyz7890/posts')
        assert response.status_code == 200
        data = json.loads(response.data.decode('utf-8'))
        assert data['posts'][0]['kind'] == 'proposal'


@xfail
def test_get_posts_votes(app, db_conn, users_table, topics_table, posts_table):
    """
    Expect get posts for topic to render votes correctly.
    """
    create_user_in_db(users_table, db_conn)
    create_topic_in_db(topics_table, db_conn)
    create_proposal_in_db(posts_table, db_conn)
    posts_table.insert({
        'id': 'asdf4567',
        'created': r.now(),
        'modified': r.now(),
        'kind': 'vote',
        'body': 'Hooray!',
        'proposal_id': 'jklm',
        'topic_id': 'wxyz7890',
        'response': True,
    }).run(db_conn)
    with app.test_client() as c:
        response = c.get('/api/topics/wxyz7890/posts')
        assert response.status_code == 200
        data = json.loads(response.data.decode('utf-8'))
        assert data['posts'][0]['kind'] == 'proposal'
        assert data['posts'][1]['kind'] == 'vote'


@xfail
def test_create_post(app, db_conn, users_table, topics_table, posts_table,
                     clogin):
    """
    Expect create post.
    """
    create_topic_in_db(topics_table, db_conn)
    response = clogin.post('/api/topics/wxyz7890/posts', data=json.dumps({
        # Should default to > 'kind': 'post',
        'body': '''A Modest Proposal for Preventing the Children of Poor
            People From Being a Burthen to Their Parents or Country, and
            for Making Them Beneficial to the Publick.''',
    }), content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data.decode('utf-8'))
    assert 'Beneficial to the Publick' in data['post']['body']


@xfail
def test_create_post_errors(app, db_conn, users_table, topics_table,
                            posts_table, clogin):
    """
    Expect create post missing field to show errors.
    """
    create_topic_in_db(topics_table, db_conn)
    response = clogin.post('/api/topics/wxyz7890/posts',
                           data=json.dumps({}),
                           content_type='application/json')
    assert response.status_code == 400
    data = json.loads(response.data.decode('utf-8'))
    assert 'errors' in data


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
                              posts_table, clogin):
    """
    Expect create post to create a proposal.
    """
    create_topic_in_db(topics_table, db_conn)
    response = clogin.post('/api/topics/wxyz7890/posts', data=json.dumps({
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


@xfail
def test_create_post_vote(app, db_conn, users_table, topics_table,
                          posts_table, clogin):
    """
    Expect create post to create a vote.
    """
    create_topic_in_db(topics_table, db_conn)
    create_proposal_in_db(posts_table, db_conn)
    response = clogin.post('/api/topics/wxyz7890/posts', data=json.dumps({
        'kind': 'vote',
        'body': 'Hooray!',
        'proposal_id': 'jklm',
        'response': True,
    }), content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data.decode('utf-8'))
    assert data['post']['kind'] == 'vote'


@xfail
def test_update_post_login(app, db_conn, users_table, topics_table,
                           posts_table):
    """
    Expect update post to require login.
    """
    create_user_in_db(users_table, db_conn)
    create_topic_in_db(topics_table, db_conn)
    create_post_in_db(posts_table, db_conn)
    with app.test_client() as c:
        response = c.put('/api/topics/wxyz7890/posts/jklm', data=json.dumps({
            'body': '''Update.''',
        }), content_type='application/json')
        assert response.status_code == 401
        data = json.loads(response.data.decode('utf-8'))
        assert 'errors' in data


@xfail
def test_update_post_author(app, db_conn, users_table, topics_table,
                            posts_table, clogin):
    """
    Expect update post to require own post.
    """
    create_topic_in_db(topics_table, db_conn)
    create_post_in_db(posts_table, db_conn, user_id='1234yuio')
    response = clogin.put('/api/topics/wxyz7890/posts/jklm', data=json.dumps({
        'body': '''Update.''',
    }), content_type='application/json')
    assert response.status_code == 403
    data = json.loads(response.data.decode('utf-8'))
    assert 'errors' in data


@xfail
def test_update_post_body(app, db_conn, users_table, topics_table,
                          posts_table, clogin):
    """
    Expect update post to change body for general post.
    """
    create_topic_in_db(topics_table, db_conn)
    create_post_in_db(posts_table, db_conn)
    response = clogin.put('/api/topics/wxyz7890/posts/jklm', data=json.dumps({
        'body': '''Update.''',
    }), content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data.decode('utf-8'))
    assert 'Update' in data['post']['body']


@xfail
def test_update_proposal(app, db_conn, users_table, topics_table,
                         posts_table, clogin):
    """
    Expect update post to handle proposals correctly.
    """
    create_topic_in_db(topics_table, db_conn)
    create_proposal_in_db(posts_table, db_conn)
    response = clogin.put('/api/topics/wxyz7890/posts/jklm', data=json.dumps({
        'status': 'declined'
    }), content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data.decode('utf-8'))
    assert 'declined' in data['proposal']['status']


@xfail
def test_update_vote(app, db_conn, users_table, topics_table,
                     posts_table, clogin):
    """
    Expect update vote to handle proposals correctly.
    """
    create_user_in_db(users_table, db_conn)
    create_topic_in_db(topics_table, db_conn)
    create_proposal_in_db(posts_table, db_conn)
    posts_table.insert({
        'id': 'vbnm1234',
        'created': r.now(),
        'modified': r.now(),
        'user_id': 'abcd1234',
        'topic_id': 'wxyz7890',
        'proposal_id': 'jklm',
        'body': 'Boo!',
        'response': False,
        'kind': 'vote',
    }).run(db_conn)
    response = clogin.put(
        '/api/topics/wxyz7890/posts/vbnm1234',
        data=json.dumps({
            'body': 'Yay!',
            'response': True,
        }), content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data.decode('utf-8'))
    assert True in data['vote']['response']
