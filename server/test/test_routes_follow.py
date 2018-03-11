import uuid
import routes.follow  # TODO-2 switch to direct imports
from conftest import user_id
from raw_insert import raw_insert_follows, raw_insert_units, \
  raw_insert_users

card_a_uuid = uuid.uuid4()
card_b_uuid = uuid.uuid4()
unit_a_uuid = uuid.uuid4()
follow_a_uuid = uuid.uuid4()


def test_list_follows_route(db_conn, session):
  """
  Expect to get a list of follows for user.
  """
  raw_insert_follows(db_conn, [{
    'user_id': user_id,
    'entity_kind': 'card',
    'entity_id': card_b_uuid,
  }, {
    'user_id': user_id,
    'entity_kind': 'unit',
    'entity_id': unit_a_uuid,
  }])

  request = {
    'cookies': {'session_id': session},
    'params': {},
    'db_conn': db_conn,
  }
  code, response = routes.follow.get_follows_route(request)

  assert code == 200
  assert len(response['follows']) == 2


def test_list_follows_route_401(db_conn):
  """
  Expect fail to to get a list of follows for user if not logged in.
  """

  code, _ = routes.follow.get_follows_route({
    'params': {},
    'db_conn': db_conn,
  })
  assert code == 401


def test_follow(db_conn, session):
  """
  Expect to follow an entity.
  """

  raw_insert_units(db_conn, [{
    'entity_id': unit_a_uuid,
    'name': 'Foo',
    'body': 'Foo',
  }])

  request = {
    'cookies': {'session_id': session},
    'params': {
      'entity_kind': 'unit',
      'entity_id': unit_a_uuid,
    },
    'db_conn': db_conn
  }
  code, _ = routes.follow.follow_route(request)
  assert code == 200


def test_follow_401(db_conn):
  """
  Expect to fail to follow entity if not logged in.
  """

  request = {
    'params': {
      'entity_kind': 'unit',
      'entity_id': unit_a_uuid,
    },
    'db_conn': db_conn
  }
  code, _ = routes.follow.follow_route(request)
  assert code == 401


def test_follow_400a(db_conn, session):
  """
  Expect to fail to follow entity if not found entity.
  """

  request = {
    'cookies': {'session_id': session},
    'params': {
      'entity_kind': 'unit',
      'entity_id': unit_a_uuid,
    },
    'db_conn': db_conn
  }
  code, response = routes.follow.follow_route(request)
  assert code == 400
  assert len(response['errors']) == 1


def test_follow_409(db_conn, session):
  """
  Expect to fail to follow entity if already followed.
  """

  raw_insert_units(db_conn, [{
    'entity_id': unit_a_uuid,
    'name': 'Foo',
    'body': 'Foo',
  }])
  raw_insert_follows(db_conn, [{
    'user_id': user_id,
    'entity_kind': 'unit',
    'entity_id': unit_a_uuid,
  }])

  request = {
    'cookies': {'session_id': session},
    'params': {
      'entity_kind': 'unit',
      'entity_id': unit_a_uuid,
    },
    'db_conn': db_conn
  }
  code, _ = routes.follow.follow_route(request)
  assert code == 400


def test_unfollow(db_conn, session):
  """
  Expect to unfollow an entity.
  """

  raw_insert_follows(db_conn, [{
    'id': follow_a_uuid,
    'user_id': user_id,
    'entity_kind': 'unit',
    'entity_id': unit_a_uuid,
  }])

  request = {
    'cookies': {'session_id': session},
    'db_conn': db_conn
  }
  code, _ = routes.follow.unfollow_route(request, follow_a_uuid)
  assert code == 200


def test_unfollow_401(db_conn):
  """
  Expect to fail to unfollow an entity if not logged in.
  """

  code, _ = routes.follow.unfollow_route({
    'db_conn': db_conn
  }, follow_a_uuid)
  assert code == 401


def test_unfollow_403(db_conn, session):
  """
  Expect to unfollow an entity.
  """

  user_b_uuid = uuid.uuid4()
  raw_insert_users(db_conn, [{
    'id': user_b_uuid,
    'name': 'other',
    'email': 'other@example.com',
    'password': 'abcd1234',
  }])
  raw_insert_follows(db_conn, [{
    'id': follow_a_uuid,
    'user_id': user_b_uuid,
    'entity_kind': 'unit',
    'entity_id': unit_a_uuid,
  }])

  request = {
    'cookies': {'session_id': session},
    'db_conn': db_conn
  }
  code, _ = routes.follow.unfollow_route(request, follow_a_uuid)
  assert code == 403


def test_unfollow_404(db_conn, session):
  """
  Expect to fail to unfollow an entity if no entity.
  """

  request = {
    'cookies': {'session_id': session},
    'db_conn': db_conn
  }
  code, _ = routes.follow.unfollow_route(request, follow_a_uuid)
  assert code == 404
