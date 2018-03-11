import uuid
from database.notice import get_notice, \
  insert_notice, \
  list_notices, \
  mark_notice_as_read, \
  mark_notice_as_unread, \
  get_notice_body, \
  deliver_notice
from raw_insert import raw_insert_notices, raw_insert_users



notice_a_id = uuid.uuid4()
user_uuid = uuid.uuid4()
user_b_uuid = uuid.uuid4()


def create_test_notices(db_conn):
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
  notices = [{
    'id': notice_a_id,
    'user_id': user_uuid,
    'kind': 'create_topic',
    'data': {
      'user_name': 'Doris',
      'topic_name': 'A new topic',
      'entity_kind': 'unit',
      'entity_name': 'Adding numbers',
    },
  }, {
    'user_id': user_uuid,
    'kind': 'create_topic',
    'data': {
      'user_name': 'Doris',
      'topic_name': 'Another new topic',
      'entity_kind': 'unit',
      'entity_name': 'Subtracting numbers',
    },
  }, {
    'user_id': user_b_uuid,
    'kind': 'create_topic',
    'data': {
      'user_name': 'Francesca',
      'topic_name': 'A third new topic',
      'entity_kind': 'unit',
      'entity_name': 'Multiplying numbers',
    },
  }]
  return raw_insert_notices(db_conn, notices)


def test_get_notice(db_conn):
  create_test_notices(db_conn)
  params = {
    'id': notice_a_id,
  }
  notice = get_notice(db_conn, params)
  assert notice
  assert notice['id'] == notice_a_id


def test_insert_notice(db_conn):
  create_test_notices(db_conn)
  data = {
    'user_id': user_uuid,
    'kind': 'OMG',
    'data': {
      'user_name': 'Doris',
      'topic_name': 'A new topic',
      'entity_kind': 'unit',
      'entity_name': 'Adding numbers',
    }
  }
  notice, errors = insert_notice(db_conn, data)
  assert errors
  assert not notice
  data['kind'] = 'create_topic'
  notice, errors = insert_notice(db_conn, data)
  assert not errors
  assert notice
  got_notice = get_notice(db_conn, {
    'id': notice['id']
  })
  assert got_notice
  assert notice['id'] == got_notice['id']


def test_list_notices(db_conn):
  create_test_notices(db_conn)
  params = {
    'user_id': user_uuid
  }
  notices = list_notices(db_conn, params)
  assert notices
  assert len(notices) == 2
  assert notices[0]['user_id'] == user_uuid
  assert notices[1]['user_id'] == user_uuid


def test_mark_notice_as_read(db_conn):
  create_test_notices(db_conn)
  notice = get_notice(db_conn, {
    'id': notice_a_id
  })
  assert notice
  notice, errors = mark_notice_as_read(db_conn, notice)
  assert not errors
  assert notice
  assert notice['read'] is True


def test_mark_notice_as_unread(db_conn):
  create_test_notices(db_conn)
  notice = get_notice(db_conn, {
    'id': notice_a_id
  })
  assert notice
  notice, errors = mark_notice_as_read(db_conn, notice)
  assert not errors
  assert notice
  assert notice['read'] is True
  notice, errors = mark_notice_as_unread(db_conn, notice)
  assert not errors
  assert notice
  assert notice['read'] is False


def test_get_notice_body(db_conn):
  create_test_notices(db_conn)
  notice = get_notice(db_conn, {
    'id': notice_a_id
  })
  body = get_notice_body(notice)
  assert body == ('Doris created a new topic, ' +
                  'A new topic, for unit Adding numbers.')


def test_deliver_notice(db_conn):
  create_test_notices(db_conn)
  notice = get_notice(db_conn, {
    'id': notice_a_id
  })
  notice = deliver_notice(notice, access=None)
  assert notice['body']
