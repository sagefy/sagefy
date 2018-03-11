
from modules.notices import send_notices
from test_database_follow import test_unit_uuid, create_test_follows


def test_send_notices(db_conn):
  create_test_follows(db_conn)
  notices, errors = send_notices(
    db_conn,
    entity_id=test_unit_uuid,
    entity_kind='unit',
    notice_kind='create_topic',
    notice_data={
      'user_name': 'Doris',
      'topic_name': 'A new topic',
      'entity_kind': 'unit',
      'entity_name': 'Adding numbers',
    }
  )
  assert not errors
  assert len(notices) == 2


def test_send_notices_fail(db_conn):
  create_test_follows(db_conn)
  notices, errors = send_notices(
    db_conn,
    entity_id=test_unit_uuid,
    entity_kind='unit',
    notice_kind='create_octopus',
    notice_data={
      'user_name': 'Doris',
      'topic_name': 'A new topic',
      'entity_kind': 'unit',
      'entity_name': 'Adding numbers',
    }
  )
  assert not notices
  assert errors
