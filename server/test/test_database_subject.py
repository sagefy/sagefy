import uuid
from database.subject import is_valid_members, \
  ensure_no_cycles, \
  insert_subject, \
  insert_subject_version, \
  update_subject, \
  deliver_subject, \
  does_subject_exist, \
  get_latest_accepted_subject, \
  list_latest_accepted_subjects, \
  list_many_subject_versions, \
  get_subject_version, \
  list_one_subject_versions, \
  list_subjects_by_unit_flat, \
  list_subject_parents, \
  list_my_recently_created_subjects, \
  list_all_subject_entity_ids, \
  get_recommended_subjects
from raw_insert import raw_insert_users, \
  raw_insert_units, \
  raw_insert_subjects
from modules.util import convert_uuid_to_slug



user_a_uuid = uuid.uuid4()
user_b_uuid = uuid.uuid4()
unit_a_uuid = uuid.uuid4()
unit_b_uuid = uuid.uuid4()
test_subject_a_uuid = uuid.uuid4()
test_subject_b_uuid = uuid.uuid4()
subject_version_a_uuid = uuid.uuid4()


def create_subject_test_data(db_conn):
  users = [{
    'id': user_a_uuid,
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
    'user_id': user_a_uuid,
    'entity_id': unit_a_uuid,
    'name': 'test unit add',
    'body': 'adding numbers is fun'
  }, {
    'user_id': user_a_uuid,
    'entity_id': unit_b_uuid,
    'name': 'test unit subtract',
    'body': 'subtracting numbers is fun',
    'require_ids': [unit_a_uuid],
  }]
  raw_insert_units(db_conn, units)
  subjects = [{
    'version_id': subject_version_a_uuid,
    'entity_id': test_subject_a_uuid,
    'name': 'Math',
    'user_id': user_b_uuid,
    'body': 'Math is fun.',
    'members': [{
      'kind': 'unit',
      'id': convert_uuid_to_slug(unit_a_uuid),
    }, {
      'kind': 'unit',
      'id': convert_uuid_to_slug(unit_b_uuid),
    }],
  }, {
    'entity_id': test_subject_b_uuid,
    'name': 'Art',
    'user_id': user_b_uuid,
    'body': 'Art is fun.',
    'members': [{
      'kind': 'subject',
      'id': convert_uuid_to_slug(test_subject_a_uuid),
    }],
  }]
  raw_insert_subjects(db_conn, subjects)


def test_is_valid_members(db_conn):
  create_subject_test_data(db_conn)
  data = {
    'members': [{
      'kind': 'unit',
      'id': convert_uuid_to_slug(uuid.uuid4()),
    }],
  }
  errors = is_valid_members(db_conn, data)
  assert errors
  data = {
    'members': [{
      'kind': 'unit',
      'id': convert_uuid_to_slug(unit_a_uuid),
    }],
  }
  errors = is_valid_members(db_conn, data)
  assert not errors
  data = {
    'members': [{
      'kind': 'subject',
      'id': convert_uuid_to_slug(test_subject_a_uuid),
    }],
  }
  errors = is_valid_members(db_conn, data)
  assert not errors


def test_ensure_no_cycles(db_conn):
  create_subject_test_data(db_conn)
  data = get_subject_version(db_conn, subject_version_a_uuid)
  data['members'] = [{
    'id': convert_uuid_to_slug(test_subject_b_uuid),
    'kind': 'subject',
  }]
  errors = ensure_no_cycles(db_conn, data)
  assert errors
  data['members'] = []
  errors = ensure_no_cycles(db_conn, data)
  assert not errors


def test_insert_subject(db_conn):
  create_subject_test_data(db_conn)
  data = {
    'entity_id': uuid.uuid4(),
    'name': 'History',
    'user_id': user_b_uuid,
    'body': 'History is fun.',
    'members': [{
      'kind': 'unit',
      'id': convert_uuid_to_slug(uuid.uuid4()),
    }],
  }
  subject, errors = insert_subject(db_conn, data)
  assert errors
  assert not subject
  data = {
    'entity_id': uuid.uuid4(),
    'name': 'History',
    'user_id': user_b_uuid,
    'body': 'History is fun.',
    'members': []
  }
  subject, errors = insert_subject(db_conn, data)
  assert not errors
  assert subject


def test_insert_subject_version(db_conn):
  create_subject_test_data(db_conn)
  current_data = get_subject_version(db_conn, subject_version_a_uuid)
  next_data = {
    'name': 'Mart',
    'user_id': user_b_uuid,
    'members': [{
      'kind': 'unit',
      'id': convert_uuid_to_slug(uuid.uuid4()),
    }],
  }
  version, errors = insert_subject_version(db_conn, current_data, next_data)
  assert errors
  assert not version
  next_data = {
    'name': 'Mart',
    'user_id': user_b_uuid,
  }
  version, errors = insert_subject_version(db_conn, current_data, next_data)
  assert not errors
  assert version


def test_update_subject(db_conn):
  create_subject_test_data(db_conn)
  current_data = get_subject_version(db_conn, subject_version_a_uuid)
  assert current_data['status'] == 'accepted'
  subject, errors = update_subject(
    db_conn,
    version_id=subject_version_a_uuid,
    status='pending'
  )
  assert not errors
  assert subject['status'] == 'pending'


def test_deliver_subject(db_conn):
  create_subject_test_data(db_conn)
  data = get_subject_version(db_conn, subject_version_a_uuid)
  data = deliver_subject(data, access=None)
  assert data


def test_does_subject_exist(db_conn):
  create_subject_test_data(db_conn)
  assert not does_subject_exist(db_conn, entity_id=uuid.uuid4())
  assert does_subject_exist(db_conn, entity_id=test_subject_a_uuid)


def test_get_latest_accepted_subject(db_conn):
  create_subject_test_data(db_conn)
  subject = get_latest_accepted_subject(
    db_conn,
    entity_id=test_subject_a_uuid
  )
  assert subject
  assert subject['status'] == 'accepted'
  assert subject['entity_id'] == test_subject_a_uuid


def test_list_latest_accepted_subjects(db_conn):
  create_subject_test_data(db_conn)
  uuids = (test_subject_a_uuid, test_subject_b_uuid)
  subjects = list_latest_accepted_subjects(db_conn, entity_ids=uuids)
  assert subjects
  assert len(subjects) == 2
  assert subjects[0]['status'] == 'accepted'
  assert subjects[1]['status'] == 'accepted'
  assert subjects[0]['entity_id'] in uuids
  assert subjects[1]['entity_id'] in uuids


def test_list_many_subject_versions(db_conn):
  create_subject_test_data(db_conn)
  versions = list_many_subject_versions(db_conn, version_ids=[
    subject_version_a_uuid,
  ])
  assert versions
  assert len(versions) == 1
  assert versions[0]['version_id'] == subject_version_a_uuid


def test_get_subject_version(db_conn):
  create_subject_test_data(db_conn)
  data = get_subject_version(db_conn, subject_version_a_uuid)
  assert data


def test_list_one_subject_versions(db_conn):
  create_subject_test_data(db_conn)
  versions = list_one_subject_versions(
    db_conn,
    entity_id=test_subject_a_uuid
  )
  assert versions
  assert len(versions) == 1
  assert versions[0]['entity_id'] == test_subject_a_uuid


def test_list_subjects_by_unit_flat(db_conn):
  create_subject_test_data(db_conn)
  subjects = list_subjects_by_unit_flat(db_conn, unit_id=unit_a_uuid)
  assert subjects
  assert len(subjects) == 1
  assert subjects[0]['entity_id'] == test_subject_a_uuid


def test_list_subject_parents(db_conn):
  create_subject_test_data(db_conn)
  parents = list_subject_parents(db_conn, subject_id=test_subject_a_uuid)
  assert parents
  assert len(parents) == 1
  assert parents[0]['entity_id'] == test_subject_b_uuid


def test_list_my_recently_created_subjects(db_conn):
  create_subject_test_data(db_conn)
  subjects = list_my_recently_created_subjects(db_conn, user_id=user_b_uuid)
  assert len(subjects) == 2
  assert subjects[0]['user_id'] == user_b_uuid
  assert subjects[1]['user_id'] == user_b_uuid


def test_list_all_subject_entity_ids(db_conn):
  create_subject_test_data(db_conn)
  entity_ids = list_all_subject_entity_ids(db_conn)
  assert len(entity_ids) == 2
  assert test_subject_a_uuid in entity_ids
  assert test_subject_b_uuid in entity_ids


def test_get_recommended_subjects(db_conn):
  create_subject_test_data(db_conn)
  subjects = get_recommended_subjects(db_conn)
  assert not subjects
