import uuid
import routes.notice  # TODO-2 switch to direct imports
from database.notice import insert_notice, get_notice
from raw_insert import raw_insert_users, \
  raw_insert_notices
from conftest import user_id


def test_list(db_conn, session):
  """
  Expect to get a list of 10 notices by user ID.
  """
  raw_insert_notices(db_conn, [{
    'user_id': user_id,
    'kind': 'create_proposal',
    'data': {
      'user_name': '',
      'proposal_name': '',
      'entity_kind': '',
      'entity_name': '',
    }
  } for _ in range(0, 10)])
  request = {
    'cookies': {'session_id': session},
    'params': {},
    'db_conn': db_conn,
  }
  code, response = routes.notice.list_notices_route(request)
  assert code == 200
  assert len(response['notices']) == 10
  assert 'user_id' in response['notices'][0]


def test_list_no_user(db_conn):
  """
  Expect to get an error if not logged in.
  """

  request = {
    'params': {},
    'db_conn': db_conn
  }
  code, _ = routes.notice.list_notices_route(request)
  assert code == 401


def test_list_paginate(db_conn, session):
  """
  Expect to paginate lists of notices.
  """

  raw_insert_notices(db_conn, [{
    'user_id': user_id,
    'kind': 'create_proposal',
    'data': {
      'user_name': '',
      'proposal_name': '',
      'entity_kind': '',
      'entity_name': '',
    }
  } for _ in range(0, 25)])

  request = {
    'cookies': {'session_id': session},
    'params': {},
    'db_conn': db_conn,
  }
  code, response = routes.notice.list_notices_route(request)
  assert code == 200
  assert len(response['notices']) == 10
  request.update({'params': {'offset': 10}})
  code, response = routes.notice.list_notices_route(request)
  assert len(response['notices']) == 10
  request.update({'params': {'offset': 20}})
  code, response = routes.notice.list_notices_route(request)
  assert len(response['notices']) == 5


def test_mark(db_conn, session):
  """
  Expect to mark a notice as read.
  """
  notice, errors = insert_notice(db_conn, {
    'user_id': user_id,
    'kind': 'create_proposal',
    'data': {
      'user_name': '',
      'proposal_name': '',
      'entity_kind': '',
      'entity_name': '',
    }
  })
  nid = notice['id']

  request = {
    'cookies': {'session_id': session},
    'params': {'read': True},
    'db_conn': db_conn
  }
  code, response = routes.notice.mark_notice_route(request, nid)
  assert code == 200
  assert response['notice']['read'] is True
  record = get_notice(db_conn, {'id': nid})
  assert record['read'] is True
  assert not errors


def test_mark_no_user(db_conn, session):
  """
  Expect to error on not logged in when marking as read.
  """
  notice, errors = insert_notice(db_conn, {
    'user_id': user_id,
    'kind': 'create_proposal',
    'data': {
      'user_name': '',
      'proposal_name': '',
      'entity_kind': '',
      'entity_name': '',
    }
  })
  assert not errors
  nid = notice['id']
  request = {
    'params': {'read': True},
    'db_conn': db_conn
  }
  code, _ = routes.notice.mark_notice_route(request, nid)
  assert code == 401
  record = get_notice(db_conn, {'id': nid})
  assert record['read'] is False



def test_mark_no_notice(db_conn, session):
  """
  Expect to error on no notice in when marking as read.
  """

  request = {
    'cookies': {'session_id': session},
    'params': {'read': True},
    'db_conn': db_conn,
  }
  code, _ = (routes.notice.mark_notice_route(request, user_id))
  assert code == 404


def test_mark_not_owned(db_conn, session):
  """
  Expect to error when not own notice when marking as read.
  """
  user_b_uuid = uuid.uuid4()
  raw_insert_users(db_conn, [{
    'id': user_b_uuid,
    'name': 'other',
    'email': 'other@example.com',
    'password': 'abcd1234',
  }])
  notice, errors = insert_notice(db_conn, {
    'user_id': user_b_uuid,
    'kind': 'create_proposal',
    'data': {
      'user_name': '',
      'proposal_name': '',
      'entity_kind': '',
      'entity_name': '',
    }
  })
  assert not errors
  nid = notice['id']

  request = {
    'cookies': {'session_id': session},
    'params': {'read': True},
    'db_conn': db_conn,
  }
  code, _ = routes.notice.mark_notice_route(request, nid)
  assert code == 403
  record = get_notice(db_conn, {'id': nid})
  assert record['read'] is False
