import uuid
from database.topic import insert_topic, \
  update_topic, \
  get_topic, \
  list_topics, \
  deliver_topic, \
  list_topics_by_entity_id, \
  add_topic_to_es
from raw_insert import raw_insert_users, \
  raw_insert_units, \
  raw_insert_topics



user_uuid = uuid.uuid4()
user_b_uuid = uuid.uuid4()
test_unit_uuid = uuid.uuid4()
test_unit_b_uuid = uuid.uuid4()
test_follow_a_id = uuid.uuid4()
test_topic_id = uuid.uuid4()


def create_test_topics(db_conn):
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
  topics = [{
    'id': test_topic_id,
    'user_id': user_uuid,
    'entity_id': test_unit_uuid,
    'entity_kind': 'unit',
    'name': 'Lets talk about adding numbers',
  }]
  raw_insert_topics(db_conn, topics)


def test_insert_topic(db_conn):
  create_test_topics(db_conn)
  data = {
    'user_id': user_uuid,
    'entity_id': test_unit_uuid,
    'entity_kind': 'truck',
    'name': 'Lets talk even more about adding numbers',
  }
  topic, errors = insert_topic(db_conn, data)
  assert errors
  assert not topic
  data = {
    'user_id': user_uuid,
    'entity_id': test_unit_uuid,
    'entity_kind': 'unit',
    'name': 'Lets talk even more about adding numbers',
  }
  topic, errors = insert_topic(db_conn, data)
  assert not errors
  assert topic


def test_update_topic(db_conn):
  create_test_topics(db_conn)
  params = {
    'id': test_topic_id,
  }
  prev_data = get_topic(db_conn, params)
  assert prev_data
  data = {
    'name': 'a',
  }
  topic, errors = update_topic(db_conn, prev_data, data)
  assert not errors
  assert topic


def test_get_topic(db_conn):
  create_test_topics(db_conn)
  params = {
    'id': test_topic_id,
  }
  topic = get_topic(db_conn, params)
  assert topic
  assert topic['id'] == test_topic_id


def test_list_topics(db_conn):
  create_test_topics(db_conn)
  params = {}
  topics = list_topics(db_conn, params)
  assert topics
  assert len(topics) == 1


def test_deliver_topic(db_conn):
  create_test_topics(db_conn)
  params = {
    'id': test_topic_id,
  }
  topic = get_topic(db_conn, params)
  topic = deliver_topic(topic, access=None)
  assert topic


def test_list_topics_by_entity_id(db_conn):
  create_test_topics(db_conn)
  params = {}
  entity_id = test_unit_uuid
  topics = list_topics_by_entity_id(db_conn, entity_id, params)
  assert topics
  assert len(topics) == 1
  assert topics[0]['entity_id'] == entity_id


def test_add_topic_to_es(db_conn):
  create_test_topics(db_conn)
  params = {
    'id': test_topic_id,
  }
  topic = get_topic(db_conn, params)
  assert add_topic_to_es(topic)
