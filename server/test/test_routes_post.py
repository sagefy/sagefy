import uuid
from conftest import create_user_in_db, user_id
import routes.post  # TODO-2 switch to direct imports
from raw_insert import raw_insert_topics, raw_insert_posts, raw_insert_units, \
  raw_insert_users
from modules.util import convert_uuid_to_slug

user_a_uuid = uuid.uuid4()
user_b_uuid = uuid.uuid4()
unit_a_uuid = uuid.uuid4()
unit_version_a_uuid = uuid.uuid4()
topic_a_uuid = uuid.uuid4()
post_a_uuid = uuid.uuid4()
proposal_a_uuid = uuid.uuid4()


def create_users_in_db(db_conn):
  users = [{
    'id': user_a_uuid,
    'name': 'another',
    'email': 'another@example.com',
    'password': 'abcd1234',
  }, {
    'id': user_b_uuid,
    'name': 'other',
    'email': 'other@example.com',
    'password': 'abcd1234',
  }]
  raw_insert_users(db_conn, users)


def create_unit_in_db(db_conn, status='accepted'):
  units = [{
    'version_id': unit_version_a_uuid,
    'user_id': user_id,
    'entity_id': unit_a_uuid,
    'name': 'test unit add',
    'body': 'adding numbers is fun',
    'status': status,
  }]
  raw_insert_units(db_conn, units)


def create_topic_in_db(db_conn, user_id=user_id):
  raw_insert_topics(db_conn, [{
    'id': topic_a_uuid,
    'user_id': user_id,
    'name': 'A Modest Proposal',
    'entity_id': unit_a_uuid,
    'entity_kind': 'unit',
  }])


def create_post_in_db(db_conn, user_id=user_id):
  raw_insert_posts(db_conn, [{
    'id': post_a_uuid,
    'user_id': user_id,
    'topic_id': topic_a_uuid,
    'body': '''A Modest Proposal for Preventing the Children of Poor
    People From Being a Burthen to Their Parents or Country, and
    for Making Them Beneficial to the Publick.''',
    'kind': 'post',
  }])


def create_proposal_in_db(db_conn, user_id=user_id):
  raw_insert_posts(db_conn, [{
    'id': proposal_a_uuid,
    'user_id': user_id,
    'topic_id': topic_a_uuid,
    'body': '''A Modest Proposal for Preventing the Children of Poor
    People From Being a Burthen to Their Parents or Country, and
    for Making Them Beneficial to the Publick.''',
    'kind': 'proposal',
    'name': 'New Unit',
    'replies_to_id': None,
    'entity_versions': [{
      'id': convert_uuid_to_slug(unit_version_a_uuid),
      'kind': 'unit',
    }],
  }])


def test_get_posts(db_conn):
  """
  Expect to get posts for given topic.
  """

  create_user_in_db(db_conn)
  create_topic_in_db(db_conn)
  raw_insert_posts(db_conn, [{
    'user_id': user_id,
    'topic_id': topic_a_uuid,
    'body': '''A Modest Proposal for Preventing the Children of Poor
    People From Being a Burthen to Their Parents or Country, and
    for Making Them Beneficial to the Publick.''',
    'kind': 'post',
  }, {
    'user_id': user_id,
    'topic_id': topic_a_uuid,
    'body': 'A follow up.',
    'kind': 'post',
  }])

  request = {
    'params': {},
    'db_conn': db_conn
  }
  code, response = routes.post.get_posts_route(request, topic_a_uuid)
  assert code == 200
  assert ('Beneficial to the Publick' in response['posts'][0]['body']
          or 'Beneficial to the Publick' in response['posts'][1]['body'])


def test_get_posts_not_topic(db_conn):
  """
  Expect 404 to get posts for a nonexistant topic.
  """

  request = {
    'params': {},
    'db_conn': db_conn
  }
  code, _ = routes.post.get_posts_route(request, topic_a_uuid)
  assert code == 404


def test_get_posts_paginate(db_conn):
  """
  Expect get posts for topic to paginate.
  """
  create_user_in_db(db_conn)
  create_topic_in_db(db_conn)
  raw_insert_posts(db_conn, [{
    'user_id': user_id,
    'topic_id': topic_a_uuid,
    'body': 'test %s' % i,
    'kind': 'post',
  } for i in range(0, 25)])
  request = {
    'params': {},
    'db_conn': db_conn
  }
  code, response = routes.post.get_posts_route(request, topic_a_uuid)
  assert code == 200
  assert len(response['posts']) == 10
  request = {
    'params': {
      'offset': 20,
    },
    'db_conn': db_conn
  }
  code, response = routes.post.get_posts_route(request, topic_a_uuid)
  assert len(response['posts']) == 5


def test_get_posts_proposal(db_conn):
  """
  Expect get posts for topic to render a proposal correctly.
  """

  create_user_in_db(db_conn)
  create_topic_in_db(db_conn)
  create_proposal_in_db(db_conn)

  request = {
    'params': {},
    'db_conn': db_conn,
  }
  code, response = routes.post.get_posts_route(request, topic_a_uuid)
  assert code == 200
  assert response['posts'][0]['kind'] == 'proposal'


def test_get_posts_votes(db_conn):
  """
  Expect get posts for topic to render votes correctly.
  """

  create_user_in_db(db_conn)
  create_topic_in_db(db_conn)
  create_proposal_in_db(db_conn)
  raw_insert_posts(db_conn, [{
    'kind': 'vote',
    'body': 'Hooray!',
    'replies_to_id': proposal_a_uuid,
    'topic_id': topic_a_uuid,
    'response': True,
    'user_id': user_id,
  }])

  request = {
    'params': {},
    'db_conn': db_conn
  }
  code, response = routes.post.get_posts_route(request, topic_a_uuid)

  assert code == 200
  assert response['posts'][0]['kind'] in ('proposal', 'vote')
  assert response['posts'][1]['kind'] in ('proposal', 'vote')


def test_create_post(db_conn, session):
  """
  Expect create post.
  """

  create_topic_in_db(db_conn)
  request = {
    'cookies': {'session_id': session},
    'params': {
      # Should default to > 'kind': 'post',
      'body': '''A Modest Proposal for Preventing the Children of
    Poor People From Being a Burthen to Their Parents or
    Country, and for Making Them Beneficial to the Publick.''',
      'kind': 'post',
      'topic_id': topic_a_uuid,
    },
    'db_conn': db_conn
  }
  code, response = routes.post.create_post_route(request, topic_a_uuid)
  assert code == 200
  assert 'Beneficial to the Publick' in response['post']['body']


def test_create_post_errors(db_conn, session):
  """
  Expect create post missing field to show errors.
  """

  create_topic_in_db(db_conn)
  request = {
    'cookies': {'session_id': session},
    'params': {
      'kind': 'post',
      'topic_id': topic_a_uuid,
    },
    'db_conn': db_conn
  }
  code, response = routes.post.create_post_route(request, topic_a_uuid)
  assert code == 400
  assert 'errors' in response


def test_create_post_log_in(db_conn, session):
  """
  Expect create post to require log in.
  """

  create_topic_in_db(db_conn)
  request = {
    'params': {
      # Should default to > 'kind': 'post',
      'body': '''A Modest Proposal for Preventing the Children of Poor
    People From Being a Burthen to Their Parents or Country, and
    for Making Them Beneficial to the Publick.''',
      'kind': 'post',
      'topic_id': topic_a_uuid,
    },
    'db_conn': db_conn
  }
  code, response = routes.post.create_post_route(request, topic_a_uuid)

  assert code == 401
  assert 'errors' in response


def test_create_post_proposal(db_conn, session):
  """
  Expect create post to create a proposal.
  """

  create_unit_in_db(db_conn)
  create_topic_in_db(db_conn)
  request = {
    'cookies': {'session_id': session},
    'params': {
      'kind': 'proposal',
      'name': 'New Unit',
      'body': '''A Modest Proposal for Preventing the Children of
    Poor People From Being a Burthen to Their Parents or
    Country, and for Making Them Beneficial to the Publick.''',
      'entity_versions': [{
        'kind': 'unit',
        'id': convert_uuid_to_slug(unit_version_a_uuid),
      }]
    },
    'db_conn': db_conn
  }
  code, response = routes.post.create_post_route(request, topic_a_uuid)
  assert not response.get('errors')
  assert code == 200
  assert response['post']['kind'] == 'proposal'


def test_create_post_vote(db_conn, session):
  """
  Expect create post to create a vote.
  """

  create_users_in_db(db_conn)
  create_unit_in_db(db_conn, status='pending')
  create_topic_in_db(db_conn)
  create_proposal_in_db(db_conn, user_id=user_a_uuid)
  request = {
    'cookies': {'session_id': session},
    'params': {
      'kind': 'vote',
      'body': 'Hooray!',
      'topic_id': topic_a_uuid,
      'replies_to_id': proposal_a_uuid,
      'response': True,
    },
    'db_conn': db_conn
  }
  code, response = routes.post.create_post_route(request, topic_a_uuid)
  assert not response.get('errors')
  assert code == 200
  assert response['post']['kind'] == 'vote'


def test_update_post_log_in(db_conn):
  """
  Expect update post to require log in.
  """

  create_user_in_db(db_conn)
  create_topic_in_db(db_conn)
  create_post_in_db(db_conn)
  request = {
    'params': {
      'body': 'Update.'
    },
    'db_conn': db_conn
  }
  code, response = routes.post.update_post_route(
    request, topic_a_uuid, post_a_uuid)

  assert code == 401
  assert 'errors' in response


def test_update_post_author(db_conn, session):
  """
  Expect update post to require own post.
  """

  create_users_in_db(db_conn)
  create_topic_in_db(db_conn)
  create_post_in_db(db_conn, user_id=user_a_uuid)
  request = {
    'cookies': {'session_id': session},
    'params': {
      'body': 'Update.'
    },
    'db_conn': db_conn
  }
  code, response = routes.post.update_post_route(
    request, topic_a_uuid, post_a_uuid)
  assert code == 403
  assert 'errors' in response


def test_update_post_body(db_conn, session):
  """
  Expect update post to change body for general post.
  """

  create_topic_in_db(db_conn)
  create_post_in_db(db_conn)
  request = {
    'cookies': {'session_id': session},
    'params': {
      'body': 'Update.'
    },
    'db_conn': db_conn,
  }
  code, response = routes.post.update_post_route(
    request, topic_a_uuid, post_a_uuid)
  assert not response.get('errors')
  assert code == 200
  assert 'Update' in response['post']['body']


def test_update_proposal(db_conn, session):
  """
  Expect update post to handle proposals correctly.
  """

  create_unit_in_db(db_conn)
  create_topic_in_db(db_conn)
  create_proposal_in_db(db_conn)

  request = {
    'cookies': {'session_id': session},
    'params': {
      'body': 'Yay'
    },
    'db_conn': db_conn,
  }
  code, response = routes.post.update_post_route(
    request, topic_a_uuid, proposal_a_uuid)

  assert code == 200
  assert response['post']['body'] == 'Yay'


def test_update_vote(db_conn, session):
  """
  Expect update vote to handle proposals correctly.
  """

  vote_a_uuid = uuid.uuid4()
  create_users_in_db(db_conn)
  create_unit_in_db(db_conn)
  create_topic_in_db(db_conn)
  create_proposal_in_db(db_conn)
  raw_insert_posts(db_conn, [{
    'id': vote_a_uuid,
    'user_id': user_id,
    'topic_id': topic_a_uuid,
    'body': 'Boo!',
    'response': False,
    'kind': 'vote',
    'replies_to_id': proposal_a_uuid,
  }])

  request = {
    'cookies': {'session_id': session},
    'params': {
      'body': 'Yay!',
      'response': True,
    },
    'db_conn': db_conn
  }
  code, response = routes.post.update_post_route(
    request, topic_a_uuid, vote_a_uuid)
  assert code == 200
  assert True is response['post']['response']
