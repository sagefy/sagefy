import uuid
from routes.topic import get_topic_route, \
  list_topics_route, \
  create_topic_route, \
  update_topic_route
from conftest import user_id
from raw_insert import raw_insert_topics, raw_insert_units, \
  raw_insert_users


topic_uuid = uuid.uuid4()
unit_uuid = uuid.uuid4()
user_b_uuid = uuid.uuid4()


def create_topic_in_db(db_conn, user_id=user_id):
  users = [{
    'id': user_b_uuid,
    'name': 'other',
    'email': 'other@example.com',
    'password': 'abcd1234',
  }]
  raw_insert_users(db_conn, users)
  raw_insert_units(db_conn, [{
    'user_id': user_id,
    'entity_id': unit_uuid,
    'name': 'test unit subtract',
    'body': 'subtracting numbers is fun',
  }])
  raw_insert_topics(db_conn, [{
    'id': topic_uuid,
    'user_id': user_id,
    'name': 'A Modest Proposal',
    'entity_id': unit_uuid,
    'entity_kind': 'unit'
  }])


def test_get_topic_route(db_conn, session):
  create_topic_in_db(db_conn)
  request = {
    'db_conn': db_conn,
  }
  topic_id = topic_uuid
  code, response = get_topic_route(request, topic_id)
  assert code == 200
  assert response['topic']['id'] == topic_uuid


def test_list_topics_route(db_conn, session):
  create_topic_in_db(db_conn)
  request = {
    'db_conn': db_conn,
    'params': {
      'entity_id': unit_uuid,
    },
  }
  code, response = list_topics_route(request)
  assert code == 200
  assert len(response['topics']) == 1
  assert response['topics'][0]['id'] == topic_uuid


def test_create_topic(db_conn, session):
  """
  Expect to create a topic with post.
  """

  create_topic_in_db(db_conn)
  request = {
    'params': {
      'name': 'An entity',
      'entity_kind': 'unit',
      'entity_id': unit_uuid,
    },
    'cookies': {
      'session_id': session,
    },
    'db_conn': db_conn
  }
  code, response = create_topic_route(request)
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
  code, response = create_topic_route(request)
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
      'topic_id': topic_uuid,
    },
    'db_conn': db_conn
  }
  code, response = update_topic_route(request, topic_uuid)
  assert code == 200
  assert response['topic']['name'] == 'Another entity'


def test_update_topic_author(db_conn, session):
  """
  Expect update topic to require original author.
  """

  create_topic_in_db(db_conn, user_id=user_b_uuid)
  request = {
    'cookies': {
      'session_id': session
    },
    'params': {
      'name': 'Another entity',
      'topic_id': topic_uuid,
    },
    'db_conn': db_conn
  }
  code, response = update_topic_route(request, topic_uuid)
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
      'name': '',
      'topic_id': topic_uuid,
    },
    'db_conn': db_conn
  }
  code, response = update_topic_route(request, topic_uuid)
  assert code == 400
  assert 'errors' in response
