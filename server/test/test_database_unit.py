import uuid
from database.unit import ensure_requires, \
  ensure_no_cycles, \
  insert_unit, \
  insert_unit_version, \
  update_unit, \
  deliver_unit, \
  does_unit_exist, \
  get_latest_accepted_unit, \
  list_latest_accepted_units, \
  list_many_unit_versions, \
  get_unit_version, \
  list_one_unit_versions, \
  list_required_units, \
  list_required_by_units, \
  list_units_by_subject_flat, \
  list_my_recently_created_units, \
  list_all_unit_entity_ids
from raw_insert import raw_insert_users, \
  raw_insert_units, \
  raw_insert_subjects
from modules.util import convert_uuid_to_slug

user_a_uuid = uuid.uuid4()
user_b_uuid = uuid.uuid4()
unit_a_uuid = uuid.uuid4()
unit_version_a_uuid = uuid.uuid4()
unit_b_uuid = uuid.uuid4()
test_subject_uuid = uuid.uuid4()


def create_unit_test_data(db_conn):
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
    'version_id': unit_version_a_uuid,
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
    'entity_id': test_subject_uuid,
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
  }]
  raw_insert_subjects(db_conn, subjects)


def test_ensure_requires(db_conn):
  create_unit_test_data(db_conn)
  data = {
    'require_ids': [unit_a_uuid, uuid.uuid4()],
  }
  errors = ensure_requires(db_conn, data)
  assert errors
  data = {
    'require_ids': [unit_a_uuid, unit_b_uuid],
  }
  errors = ensure_requires(db_conn, data)
  assert not errors


def test_ensure_no_cycles(db_conn):
  create_unit_test_data(db_conn)
  data = get_unit_version(db_conn, unit_version_a_uuid)
  data['require_ids'] = [unit_b_uuid]
  errors = ensure_no_cycles(db_conn, data)
  assert errors
  data['require_ids'] = []
  errors = ensure_no_cycles(db_conn, data)
  assert not errors


def test_insert_unit(db_conn):
  create_unit_test_data(db_conn)
  data = {
    'user_id': user_a_uuid,
    'entity_id': uuid.uuid4(),
    'name': 'test unit add',
    'body': 'multiplying numbers is fun',
    'require_ids': [uuid.uuid4()],
  }
  unit, errors = insert_unit(db_conn, data)
  assert errors
  assert not unit
  data = {
    'user_id': user_a_uuid,
    'entity_id': uuid.uuid4(),
    'name': 'test unit add',
    'body': 'multiplying numbers is fun'
  }
  unit, errors = insert_unit(db_conn, data)
  assert not errors
  assert unit


def test_insert_unit_version(db_conn):
  create_unit_test_data(db_conn)
  current_data = get_unit_version(db_conn, unit_version_a_uuid)
  next_data = {
    'user_id': user_a_uuid,
    'name': 'test unit add',
    'body': 'multiplying numbers is fun',
    'require_ids': [uuid.uuid4()]
  }
  version, errors = insert_unit_version(db_conn, current_data, next_data)
  assert errors
  assert not version
  current_data['entity_id'] = uuid.uuid4()
  next_data = {
    'user_id': user_a_uuid,
    'name': 'test unit add',
    'body': 'multiplying numbers is fun'
  }
  version, errors = insert_unit_version(db_conn, current_data, next_data)
  assert errors
  assert not version
  current_data['entity_id'] = unit_a_uuid
  version, errors = insert_unit_version(db_conn, current_data, next_data)
  assert not errors
  assert version


def test_update_unit(db_conn):
  create_unit_test_data(db_conn)
  current_data = get_unit_version(db_conn, unit_version_a_uuid)
  assert current_data['status'] == 'accepted'
  unit, errors = update_unit(
    db_conn,
    version_id=unit_version_a_uuid,
    status='pending'
  )
  assert not errors
  assert unit['status'] == 'pending'


def test_deliver_unit(db_conn):
  create_unit_test_data(db_conn)
  data = get_unit_version(db_conn, unit_version_a_uuid)
  assert deliver_unit(data, access=None)


def test_does_unit_exist(db_conn):
  create_unit_test_data(db_conn)
  assert not does_unit_exist(db_conn, entity_id=uuid.uuid4())
  assert does_unit_exist(db_conn, entity_id=unit_a_uuid)


def test_get_latest_accepted_unit(db_conn):
  create_unit_test_data(db_conn)
  unit = get_latest_accepted_unit(db_conn, entity_id=unit_a_uuid)
  assert unit
  assert unit['status'] == 'accepted'
  assert unit['entity_id'] == unit_a_uuid


def test_list_latest_accepted_units(db_conn):
  create_unit_test_data(db_conn)
  units = list_latest_accepted_units(db_conn, entity_ids=[
    unit_a_uuid,
    unit_b_uuid,
  ])
  assert units
  assert len(units) == 2
  assert units[0]['status'] == 'accepted'
  assert units[1]['status'] == 'accepted'
  assert units[0]['entity_id'] in (unit_a_uuid, unit_b_uuid)
  assert units[1]['entity_id'] in (unit_a_uuid, unit_b_uuid)


def test_list_many_unit_versions(db_conn):
  create_unit_test_data(db_conn)
  versions = list_many_unit_versions(db_conn, version_ids=[
    unit_version_a_uuid,
  ])
  assert versions
  assert len(versions) == 1
  assert versions[0]['version_id'] == unit_version_a_uuid


def test_get_unit_version(db_conn):
  create_unit_test_data(db_conn)
  data = get_unit_version(db_conn, unit_version_a_uuid)
  assert data


def test_list_one_unit_versions(db_conn):
  create_unit_test_data(db_conn)
  versions = list_one_unit_versions(db_conn, entity_id=unit_a_uuid)
  assert versions
  assert len(versions) == 1
  assert versions[0]['entity_id'] == unit_a_uuid


def test_list_required_units(db_conn):
  create_unit_test_data(db_conn)
  units = list_required_units(db_conn, entity_id=unit_b_uuid)
  assert units
  assert len(units) == 1
  assert units[0]['entity_id'] == unit_a_uuid


def test_list_required_by_units(db_conn):
  create_unit_test_data(db_conn)
  units = list_required_by_units(db_conn, entity_id=unit_a_uuid)
  assert units
  assert len(units) == 1
  assert units[0]['entity_id'] == unit_b_uuid


def test_list_units_by_subject_flat(db_conn):
  create_unit_test_data(db_conn)
  units = list_units_by_subject_flat(db_conn, subject_id=test_subject_uuid)
  assert units
  assert len(units) == 2
  assert units[0]['entity_id'] in (unit_a_uuid, unit_b_uuid)
  assert units[1]['entity_id'] in (unit_a_uuid, unit_b_uuid)


def test_list_my_recently_created_units(db_conn):
  create_unit_test_data(db_conn)
  units = list_my_recently_created_units(db_conn, user_id=user_a_uuid)
  assert len(units) == 2
  assert units[0]['user_id'] == user_a_uuid
  assert units[1]['user_id'] == user_a_uuid


def test_list_all_unit_entity_ids(db_conn):
  create_unit_test_data(db_conn)
  entity_ids = list_all_unit_entity_ids(db_conn)
  assert len(entity_ids) == 2
  assert unit_a_uuid in entity_ids
  assert unit_b_uuid in entity_ids
