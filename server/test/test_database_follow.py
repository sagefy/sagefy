import uuid
from database.follow import get_follow, \
  get_follow_by_id, \
  list_follows_by_user, \
  list_follows_by_entity, \
  insert_follow, \
  deliver_follow, \
  delete_follow, \
  is_valid_entity, \
  get_user_ids_by_followed_entity
from raw_insert import raw_insert_follows, raw_insert_units, \
  raw_insert_users


user_uuid = uuid.uuid4()
user_b_uuid = uuid.uuid4()
test_unit_uuid = uuid.uuid4()
test_unit_b_uuid = uuid.uuid4()
test_follow_a_id = uuid.uuid4()


def create_test_follows(db_conn):
  users = [{
    'id': user_uuid,
    'name': 'test',
    'email': 'test@example.com',
    'password': 'abcd1234',
  }, {
    'id': user_b_uuid,
    'name': 'other',
    'email': 'other@example.com',
    'password': 'abcd1234',
  }]
  raw_insert_users(db_conn, users)
  units = [{
    'user_id': user_uuid,
    'entity_id': test_unit_uuid,
    'name': 'test unit add',
    'body': 'adding numbers is fun'
  }, {
    'user_id': user_uuid,
    'entity_id': test_unit_b_uuid,
    'name': 'test unit subtract',
    'body': 'subtracting numbers is fun'
  }]
  raw_insert_units(db_conn, units)
  follows = [{
    'id': test_follow_a_id,
    'user_id': user_uuid,
    'entity_id': test_unit_uuid,
    'entity_kind': 'unit',
  }, {
    'user_id': user_uuid,
    'entity_id': test_unit_b_uuid,
    'entity_kind': 'unit',
  }, {
    'user_id': user_b_uuid,
    'entity_id': test_unit_uuid,
    'entity_kind': 'unit',
  }]
  raw_insert_follows(db_conn, follows)


def test_get_follow(db_conn):
  create_test_follows(db_conn)
  follow = get_follow(db_conn, user_uuid, test_unit_uuid)
  assert follow
  assert follow['user_id'] == user_uuid
  assert follow['entity_id'] == test_unit_uuid


def test_get_follow_by_id(db_conn):
  create_test_follows(db_conn)
  follow = get_follow_by_id(db_conn, test_follow_a_id)
  assert follow
  assert follow['id'] == test_follow_a_id


def test_list_follows_by_user(db_conn):
  create_test_follows(db_conn)
  params = {
    'user_id': user_uuid,
  }
  follows = list_follows_by_user(db_conn, params)
  assert follows
  assert len(follows) == 2
  assert follows[0]['user_id'] == user_uuid
  assert follows[1]['user_id'] == user_uuid


def test_list_follows_by_entity(db_conn):
  create_test_follows(db_conn)
  params = {
    'entity_id': test_unit_uuid,
    'entity_kind': 'unit',
  }
  follows = list_follows_by_entity(db_conn, params)
  assert follows
  assert len(follows) == 2
  assert follows[0]['entity_id'] == test_unit_uuid
  assert follows[1]['entity_id'] == test_unit_uuid


def test_insert_follow(db_conn):
  create_test_follows(db_conn)
  data = {
    'user_id': user_b_uuid,
    'entity_id': test_unit_uuid,
    'entity_kind': 'unit',
  }
  follow, errors = insert_follow(db_conn, data)
  assert not follow
  assert errors
  data['entity_kind'] = 'subject'
  data['entity_id'] = test_unit_b_uuid
  follow, errors = insert_follow(db_conn, data)
  assert not follow
  assert errors
  data['entity_kind'] = 'unit'
  follow, errors = insert_follow(db_conn, data)
  assert not errors
  assert follow


def test_deliver_follow(db_conn):
  create_test_follows(db_conn)
  follow = get_follow_by_id(db_conn, test_follow_a_id)
  assert follow
  follow = deliver_follow(follow, access=None)
  assert follow


def test_delete_follow(db_conn):
  create_test_follows(db_conn)
  follow = get_follow_by_id(db_conn, test_follow_a_id)
  assert follow
  delete_follow(db_conn, test_follow_a_id)
  follow = get_follow_by_id(db_conn, test_follow_a_id)
  assert not follow


def test_is_valid_entity(db_conn):
  create_test_follows(db_conn)
  follow = {
    'entity_kind': 'subject',
    'entity_id': test_unit_uuid,
  }
  errors = is_valid_entity(db_conn, follow)
  assert errors
  follow['entity_kind'] = 'topic'
  errors = is_valid_entity(db_conn, follow)
  assert errors
  follow['entity_kind'] = 'unit'
  errors = is_valid_entity(db_conn, follow)
  assert not errors


def test_get_user_ids_by_followed_entity(db_conn):
  create_test_follows(db_conn)
  user_ids = get_user_ids_by_followed_entity(db_conn, test_unit_uuid, 'unit')
  assert len(user_ids) == 2
