import uuid
import routes.user_subjects  # TODO-2 switch to direct imports
from raw_insert import raw_insert_subjects, raw_insert_user_subjects, \
  raw_insert_units
from conftest import user_id
from modules.util import convert_uuid_to_slug

subject_a_uuid = uuid.uuid4()
subject_b_uuid = uuid.uuid4()
subject_c_uuid = uuid.uuid4()
subject_d_uuid = uuid.uuid4()
unit_a_uuid = uuid.uuid4()


def prep(db_conn):
  raw_insert_subjects(db_conn, [{
    'entity_id': subject_a_uuid,
    'name': 'A',
    'body': 'Apple',
    'status': 'accepted',
  }, {
    'entity_id': subject_b_uuid,
    'name': 'B',
    'body': 'Banana',
    'status': 'accepted',
  }, {
    'entity_id': subject_c_uuid,
    'name': 'C',
    'body': 'Coconut',
    'status': 'accepted',
  }, {
    'entity_id': subject_d_uuid,
    'name': 'D',
    'body': 'Date',
    'status': 'accepted',
  }])
  raw_insert_user_subjects(db_conn, [{
    'user_id': user_id,
    'subject_id': subject_a_uuid,
  }, {
    'user_id': user_id,
    'subject_id': subject_c_uuid,
  }])


def create_one_subject(db_conn):
  raw_insert_units(db_conn, [{
    'entity_id': unit_a_uuid,
    'name': 'Unit',
    'body': 'doesnt matter',
  }])
  raw_insert_subjects(db_conn, [{
    'entity_id': subject_a_uuid,
    'name': 'A',
    'body': 'Apple',
    'members': [{
      'kind': 'unit',
      'id': convert_uuid_to_slug(unit_a_uuid),
    }]
  }])


def test_list_user_subjects_route(db_conn, session):

  """
  Expect to get a list of the user's subjects.
  """

  prep(db_conn)
  request = {
    'cookies': {'session_id': session},
    'params': {},
    'db_conn': db_conn,
  }
  code, response = routes.user_subjects.list_user_subjects_route(
    request, user_id)
  assert code == 200
  assert len(response['subjects']) == 2
  assert response['subjects'][0]['body'] in ('Apple', 'Coconut')


def test_list_user_subjects_route_other_404(db_conn, session):
  code, _ = routes.user_subjects.list_user_subjects_route({
    'db_conn': db_conn,
  }, uuid.uuid4())
  assert code == 404


def test_list_user_subjects_route_other_403(db_conn):
  this_user_id = uuid.uuid4()
  from raw_insert import raw_insert_users
  raw_insert_users(db_conn, [{
    'id': this_user_id,
    'name': 'test',
    'email': 'test@example.com',
    'password': 'abcd1234',
    'settings': {
      'email_frequency': 'daily',
      'view_subjects': 'private',
      'view_follows': 'private',
    },
  }])
  request = {
    'params': {},
    'db_conn': db_conn,
  }
  code, _ = routes.user_subjects.list_user_subjects_route(
    request, this_user_id)
  assert code == 403


def test_add_subject(db_conn, session):
  """
  Expect to add a subject to the user's list.
  """

  create_one_subject(db_conn)
  request = {
    'cookies': {'session_id': session},
    'db_conn': db_conn
  }
  code, response = routes.user_subjects.add_subject_route(
    request, user_id, subject_a_uuid)
  assert code == 200
  assert response['user_subject']['subject_id'] == subject_a_uuid


def test_add_subject_401(db_conn):
  """
  Expect to 401 when trying to add a subject but not logged in.
  """

  code, _ = routes.user_subjects.add_subject_route({
    'db_conn': db_conn
  }, user_id, subject_a_uuid)
  assert code == 401


def test_add_subject_403(db_conn, session):
  """
  Expect to 403 when attempt to add to another user's subjects.
  """

  request = {
    'cookies': {'session_id': session},
    'db_conn': db_conn,
  }
  code, _ = routes.user_subjects.add_subject_route(
    request, uuid.uuid4(), '2')
  assert code == 403


def test_add_subject_404(db_conn, session):
  """
  Expect to 404 if subject not found.
  """

  request = {
    'cookies': {'session_id': session},
    'db_conn': db_conn,
  }
  code, _ = routes.user_subjects.add_subject_route(
    request, user_id, uuid.uuid4())
  assert code == 404


def test_add_subject_already_added(db_conn, session):
  """
  Expect to 400 if already added subject.
  """

  create_one_subject(db_conn)
  request = {
    'cookies': {'session_id': session},
    'db_conn': db_conn,
  }
  code, _ = routes.user_subjects.add_subject_route(
    request, user_id, subject_a_uuid)
  assert code == 200
  code, _ = routes.user_subjects.add_subject_route(
    request, user_id, subject_a_uuid)
  assert code == 400


def test_select_subject_route(db_conn, session):
  """
  Expect to select a subject.
  """

  create_one_subject(db_conn)
  request = {
    'cookies': {'session_id': session},
    'db_conn': db_conn,
  }
  code, response = routes.user_subjects.select_subject_route(
    request, user_id, subject_a_uuid)
  assert code == 200
  assert (response['next']['path'] ==
          '/s/subjects/{subject_a_uuid}/units'
          .format(subject_a_uuid=convert_uuid_to_slug(subject_a_uuid)))


def test_remove_subject(db_conn, session):
  """
  Expect to remove a subject from the user's list.
  """

  create_one_subject(db_conn)
  raw_insert_user_subjects(db_conn, [{
    'user_id': user_id,
    'subject_id': subject_a_uuid,
  }])
  request = {
    'cookies': {'session_id': session},
    'db_conn': db_conn,
  }
  code, _ = routes.user_subjects.remove_subject_route(
    request, user_id, subject_a_uuid)
  assert code == 200


def test_remove_subject_401(db_conn):
  """
  Expect to 401 when trying to remove a user subject not logged in.
  """

  request = {
    'db_conn': db_conn,
  }
  code, _ = routes.user_subjects.remove_subject_route(
    request, user_id, subject_a_uuid)
  assert code == 401


def test_remove_subject_403(db_conn, session):
  """
  Expect forbidden when trying to remove another user's subject.
  """

  request = {
    'cookies': {'session_id': session},
    'db_conn': db_conn,
  }
  code, _ = routes.user_subjects.remove_subject_route(
    request, uuid.uuid4(), '2')
  assert code == 403


def test_remove_subject_404(db_conn, session):
  """
  Expect to not found when trying to delete an unadded subject.
  """

  request = {
    'cookies': {'session_id': session},
    'db_conn': db_conn,
  }
  code, _ = routes.user_subjects.remove_subject_route(
    request, user_id, subject_a_uuid)
  assert code == 404
