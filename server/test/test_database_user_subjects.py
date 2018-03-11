import uuid
from database.user_subjects import insert_user_subject, \
  list_user_subjects, \
  remove_user_subject, \
  list_user_subjects_entity
from raw_insert import raw_insert_users, \
  raw_insert_subjects, \
  raw_insert_user_subjects



user_a_uuid = uuid.uuid4()
user_b_uuid = uuid.uuid4()
test_subject_uuid = uuid.uuid4()


def create_user_subjects_test_data(db_conn):
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
  subjects = [{
    'entity_id': test_subject_uuid,
    'name': 'Calculus',
    'user_id': user_b_uuid,
    'body': 'Calculus is fun sometimes.',
    'members': [],
  }]
  raw_insert_subjects(db_conn, subjects)
  user_subjects = [{
    'user_id': user_a_uuid,
    'subject_id': test_subject_uuid,
  }]
  raw_insert_user_subjects(db_conn, user_subjects)


def test_insert_user_subject(db_conn):
  create_user_subjects_test_data(db_conn)
  user_subject, errors = insert_user_subject(
    db_conn,
    user_id=user_a_uuid,
    subject_id=test_subject_uuid
  )
  assert errors
  assert not user_subject
  user_subject, errors = insert_user_subject(
    db_conn,
    user_id=user_b_uuid,
    subject_id=test_subject_uuid
  )
  assert not errors
  assert user_subject


def test_list_user_subjects(db_conn):
  create_user_subjects_test_data(db_conn)
  user_subjects = list_user_subjects(db_conn, user_a_uuid)
  assert user_subjects
  assert len(user_subjects) == 1
  assert user_subjects[0]['user_id'] == user_a_uuid


def test_remove_user_subject(db_conn):
  create_user_subjects_test_data(db_conn)
  remove_user_subject(
    db_conn,
    user_id=user_a_uuid,
    subject_id=test_subject_uuid
  )
  user_subjects = list_user_subjects(db_conn, user_a_uuid)
  assert not user_subjects


def test_list_user_subjects_entity(db_conn):
  create_user_subjects_test_data(db_conn)
  params = {}
  subjects = list_user_subjects_entity(db_conn, user_a_uuid, params)
  assert subjects
  assert len(subjects) == 1
  assert subjects[0]['entity_id'] == test_subject_uuid
