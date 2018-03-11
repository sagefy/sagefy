import uuid
from database.entity_facade import get_entity_version, \
  list_one_entity_versions, \
  update_entity_status_by_kind, \
  list_subjects_by_unit_recursive, \
  list_units_in_subject_recursive, \
  get_entity_status, \
  update_entity_statuses, \
  find_requires_cycle
from database.unit import get_unit_version
from database.card import get_card_version
from database.subject import get_latest_accepted_subject
from database.post import get_post
from test_database_unit import create_unit_test_data, \
  unit_b_uuid as XU_unit_b_uuid, \
  unit_version_a_uuid as XU_unit_version_a_uuid
from test_database_card import create_card_test_data, \
  card_b_uuid as XU_card_b_uuid, \
  card_version_a_uuid as XU_card_version_a_uuid
from raw_insert import raw_insert_users, \
  raw_insert_units, \
  raw_insert_subjects, \
  raw_insert_cards, \
  raw_insert_topics, \
  raw_insert_posts
from modules.util import convert_uuid_to_slug



user_a_uuid = uuid.uuid4()
unit_a_uuid = uuid.uuid4()
unit_b_uuid = uuid.uuid4()
subject_a_uuid = uuid.uuid4()
subject_b_uuid = uuid.uuid4()


def create_test_user(db_conn):
  users = [{
    'id': user_a_uuid,
    'name': 'test',
    'email': 'test@example.com',
    'password': 'abcd1234',
  }]
  raw_insert_users(db_conn, users)


def create_recurse_test_data(db_conn):
  create_test_user(db_conn)
  units = [{
    'user_id': user_a_uuid,
    'entity_id': unit_a_uuid,
    'name': 'test unit add',
    'body': 'adding numbers is fun'
  }, {
    'user_id': user_a_uuid,
    'entity_id': unit_b_uuid,
    'name': 'test unit subtract',
    'body': 'subtracting numbers is fun',
  }]
  raw_insert_units(db_conn, units)
  subjects = [{
    'entity_id': subject_a_uuid,
    'name': 'Math',
    'user_id': user_a_uuid,
    'body': 'Math is fun.',
    'members': [{
      'kind': 'unit',
      'id': convert_uuid_to_slug(unit_a_uuid),
    }, {
      'kind': 'unit',
      'id': convert_uuid_to_slug(unit_b_uuid),
    }],
  }, {
    'entity_id': subject_b_uuid,
    'name': 'Art',
    'user_id': user_a_uuid,
    'body': 'Art is fun.',
    'members': [{
      'kind': 'subject',
      'id': convert_uuid_to_slug(subject_a_uuid),
    }],
  }]
  raw_insert_subjects(db_conn, subjects)


def test_get_entity_version(db_conn):
  assert not get_entity_version(
    db_conn,
    kind='card',
    version_id=uuid.uuid4()
  )
  assert not get_entity_version(
    db_conn,
    kind='unit',
    version_id=uuid.uuid4()
  )
  assert not get_entity_version(
    db_conn,
    kind='subject',
    version_id=uuid.uuid4()
  )


def test_list_one_entity_versions(db_conn):
  assert not list_one_entity_versions(
    db_conn,
    kind='card',
    entity_id=uuid.uuid4()
  )
  assert not list_one_entity_versions(
    db_conn,
    kind='unit',
    entity_id=uuid.uuid4()
  )
  assert not list_one_entity_versions(
    db_conn,
    kind='subject',
    entity_id=uuid.uuid4()
  )


def test_update_entity_status_by_kind(db_conn):
  create_test_user(db_conn)
  unit_version_a_uuid = uuid.uuid4()
  card_version_a_uuid = uuid.uuid4()
  subject_version_a_uuid = uuid.uuid4()
  units = [{
    'version_id': unit_version_a_uuid,
    'user_id': user_a_uuid,
    'entity_id': unit_a_uuid,
    'name': 'test unit add',
    'body': 'adding numbers is fun',
    'status': 'pending',
  }]
  raw_insert_units(db_conn, units)
  cards = [{
    'version_id': card_version_a_uuid,
    'status': 'pending',
    'entity_id': uuid.uuid4(),
    'unit_id': unit_a_uuid,
    'user_id': user_a_uuid,
    'kind': 'video',
    'name': 'Meaning of Life Video',
    'data': {
      'site': 'youtube',
      'video_id': convert_uuid_to_slug(uuid.uuid4()),
    },
  }]
  raw_insert_cards(db_conn, cards)
  subjects = [{
    'version_id': subject_version_a_uuid,
    'status': 'pending',
    'entity_id': subject_a_uuid,
    'name': 'Math',
    'user_id': user_a_uuid,
    'body': 'Math is fun.',
    'members': [],
  }]
  raw_insert_subjects(db_conn, subjects)
  unit, errors = update_entity_status_by_kind(
    db_conn,
    kind='unit',
    version_id=unit_version_a_uuid,
    status='accepted'
  )
  assert not errors
  assert unit['status'] == 'accepted'
  card, errors = update_entity_status_by_kind(
    db_conn,
    kind='card',
    version_id=card_version_a_uuid,
    status='accepted'
  )
  assert not errors
  assert card['status'] == 'accepted'
  subject, errors = update_entity_status_by_kind(
    db_conn,
    kind='subject',
    version_id=subject_version_a_uuid,
    status='accepted'
  )
  assert not errors
  assert subject['status'] == 'accepted'


def test_list_subjects_by_unit_recursive(db_conn):
  create_recurse_test_data(db_conn)
  subjects = list_subjects_by_unit_recursive(db_conn, unit_id=unit_a_uuid)
  assert subjects
  assert len(subjects) == 2
  assert subjects[0]['entity_id'] in (subject_a_uuid, subject_b_uuid)
  assert subjects[1]['entity_id'] in (subject_a_uuid, subject_b_uuid)


def test_list_units_in_subject_recursive(db_conn):
  create_recurse_test_data(db_conn)
  subject = get_latest_accepted_subject(db_conn, subject_b_uuid)
  units = list_units_in_subject_recursive(db_conn, subject)
  assert units
  assert len(units) == 2
  assert units[0]['entity_id'] in (unit_a_uuid, unit_b_uuid)
  assert units[1]['entity_id'] in (unit_a_uuid, unit_b_uuid)


def test_find_requires_cycle_unit(db_conn):
  create_unit_test_data(db_conn)
  data = get_unit_version(db_conn, XU_unit_version_a_uuid)
  data['require_ids'] = [XU_unit_b_uuid]
  found = find_requires_cycle(db_conn, 'units', data)
  assert found
  data['require_ids'] = []
  found = find_requires_cycle(db_conn, 'units', data)
  assert not found


def test_find_requires_cycle_card(db_conn):
  create_card_test_data(db_conn)
  data = get_card_version(db_conn, XU_card_version_a_uuid)
  data['require_ids'] = [XU_card_b_uuid]
  found = find_requires_cycle(db_conn, 'cards', data)
  assert found
  data['require_ids'] = []
  found = find_requires_cycle(db_conn, 'cards', data)
  assert not found


def test_get_entity_status():
  changed, status = get_entity_status(current_status='accepted', votes=[])
  assert not changed
  assert status == 'accepted'
  changed, status = get_entity_status(current_status='pending', votes=[])
  assert changed
  assert status == 'accepted'


def test_update_entity_statuses(db_conn):
  create_test_user(db_conn)
  unit_version_a_uuid = uuid.uuid4()
  topic_uuid = uuid.uuid4()
  proposal_uuid = uuid.uuid4()
  units = [{
    'version_id': unit_version_a_uuid,
    'user_id': user_a_uuid,
    'entity_id': unit_a_uuid,
    'name': 'test unit add',
    'body': 'adding numbers is fun',
    'status': 'pending',
  }]
  raw_insert_units(db_conn, units)
  topics = [{
    'id': topic_uuid,
    'user_id': user_a_uuid,
    'entity_id': unit_a_uuid,
    'entity_kind': 'unit',
    'name': 'Lets talk about adding numbers',
  }]
  raw_insert_topics(db_conn, topics)
  posts = [{
    'id': proposal_uuid,
    'kind': 'proposal',
    'body': 'A new version',
    'entity_versions': [{
      'id': convert_uuid_to_slug(unit_version_a_uuid),
      'kind': 'unit',
    }],
    'user_id': user_a_uuid,
    'topic_id': topic_uuid,
  }]
  raw_insert_posts(db_conn, posts)
  proposal = get_post(db_conn, {'id': proposal_uuid})
  update_entity_statuses(db_conn, proposal)
  unit = get_unit_version(db_conn, unit_version_a_uuid)
  assert unit
  assert unit['status'] == 'accepted'
