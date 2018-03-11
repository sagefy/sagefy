import uuid
from routes.sitemap import get_sitemap_route
from raw_insert import raw_insert_users, \
  raw_insert_units, \
  raw_insert_topics

user_uuid = uuid.uuid4()
unit_uuid = uuid.uuid4()
topic_uuid = uuid.uuid4()


def test_get_sitemap_route(db_conn):
  raw_insert_users(db_conn, [{
    'id': user_uuid,
    'name': 'test',
    'email': 'test@example.com',
    'password': 'abcd1234',
  }])
  raw_insert_units(db_conn, [{
    'user_id': user_uuid,
    'entity_id': unit_uuid,
    'name': 'test unit add',
    'body': 'adding numbers is fun'
  }])
  raw_insert_topics(db_conn, [{
    'id': topic_uuid,
    'user_id': user_uuid,
    'entity_id': unit_uuid,
    'entity_kind': 'unit',
    'name': 'Lets talk about adding numbers',
  }])
  request = {'db_conn': db_conn}
  code, _ = get_sitemap_route(request)
  assert code == 200
