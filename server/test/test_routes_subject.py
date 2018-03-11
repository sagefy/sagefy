import uuid
import pytest

from routes.subject import \
  get_recommended_subjects_route, \
  get_subject_route, \
  list_subjects_route, \
  get_subject_versions_route, \
  get_subject_version_route, \
  get_subject_tree_route, \
  get_subject_units_route, \
  choose_unit_route, \
  get_my_recently_created_subjects_route, \
  create_new_subject_version_route, \
  create_existing_subject_version_route
from conftest import user_id
from raw_insert import raw_insert_units, raw_insert_subjects, raw_insert_cards
from modules.util import convert_uuid_to_slug
from database.user import get_user_by_id, set_learning_context

xfail = pytest.mark.xfail

user_a_uuid = uuid.uuid4()
user_b_uuid = uuid.uuid4()
unit_a_uuid = uuid.uuid4()
unit_version_a_uuid = uuid.uuid4()
unit_b_uuid = uuid.uuid4()
card_a_uuid = uuid.uuid4()
subject_a_uuid = uuid.uuid4()
subject_b_uuid = uuid.uuid4()
subject_version_a_uuid = uuid.uuid4()


def create_route_subject_test_data(db_conn):
  units = [{
    'version_id': unit_version_a_uuid,
    'user_id': user_id,
    'entity_id': unit_a_uuid,
    'name': 'test unit add',
    'body': 'adding numbers is fun'
  }, {
    'user_id': user_id,
    'entity_id': unit_b_uuid,
    'name': 'test unit subtract',
    'body': 'subtracting numbers is fun',
    'require_ids': [unit_a_uuid],
  }]
  raw_insert_units(db_conn, units)
  cards = [{
    'entity_id': card_a_uuid,
    'unit_id': unit_a_uuid,
    'kind': 'video',
    'name': 'Video Z',
  }]
  raw_insert_cards(db_conn, cards)
  subjects = [{
    'version_id': subject_version_a_uuid,
    'entity_id': subject_a_uuid,
    'name': 'Math',
    'user_id': user_id,
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
    'name': 'An Introduction to Electronic Music',
    'user_id': user_id,
    'body': 'Art is fun.',
    'members': [{
      'kind': 'subject',
      'id': convert_uuid_to_slug(subject_a_uuid),
    }],
  }]
  raw_insert_subjects(db_conn, subjects)


def test_get_recommended_subjects_route(db_conn, session):
  create_route_subject_test_data(db_conn)
  request = {
    'db_conn': db_conn,
    'cookies': {
      'session_id': session,
    },
    'params': {}
  }
  code, response = get_recommended_subjects_route(request)
  assert not response.get('errors')
  assert code == 200
  assert response['subjects']


def test_get_subject(db_conn, session):
  """
  Expect to get the subject information for displaying to a contributor.
  """

  create_route_subject_test_data(db_conn)
  request = {
    'db_conn': db_conn,
    'cookies': {
      'session_id': session,
    },
    'params': {}
  }
  code, response = get_subject_route(request, subject_id=subject_a_uuid)
  assert not response.get('errors')
  assert code == 200
  assert response['subject']


def test_get_subject_404(db_conn, session):
  """
  Expect to fail to get subject information if subject is unknown. (404)
  """

  create_route_subject_test_data(db_conn)
  request = {
    'db_conn': db_conn,
    'cookies': {
      'session_id': session,
    },
    'params': {}
  }
  code, response = get_subject_route(request, subject_id=uuid.uuid4())
  assert response.get('errors')
  assert code == 404


def test_list_subjects_route(db_conn, session):
  create_route_subject_test_data(db_conn)
  request = {
    'db_conn': db_conn,
    'cookies': {
      'session_id': session,
    },
    'params': {
      'entity_ids': ','.join([
        convert_uuid_to_slug(subject_a_uuid),
        convert_uuid_to_slug(subject_b_uuid),
      ])
    }
  }
  code, response = list_subjects_route(request)
  assert not response.get('errors')
  assert code == 200
  assert response['subjects']


def test_get_subject_versions_route(db_conn, session):
  create_route_subject_test_data(db_conn)
  request = {
    'db_conn': db_conn,
    'cookies': {
      'session_id': session,
    },
    'params': {}
  }
  code, response = get_subject_versions_route(
    request,
    subject_id=subject_a_uuid
  )
  assert not response.get('errors')
  assert code == 200
  assert response['versions']


def test_get_subject_version_route(db_conn, session):
  create_route_subject_test_data(db_conn)
  request = {
    'db_conn': db_conn,
    'cookies': {
      'session_id': session,
    },
    'params': {}
  }
  code, response = get_subject_version_route(
    request,
    version_id=subject_version_a_uuid
  )
  assert not response.get('errors')
  assert code == 200
  assert response['version']


def test_subject_tree(db_conn, session):
  """
  Expect to get subject information in tree format.
  """

  create_route_subject_test_data(db_conn)
  request = {
    'db_conn': db_conn,
    'cookies': {
      'session_id': session,
    },
    'params': {}
  }
  code, response = get_subject_tree_route(request, subject_id=subject_a_uuid)
  assert not response.get('errors')
  assert code == 200
  assert response['subjects']
  assert response['units']
  assert response['buckets']


def test_subject_tree_logged_out(db_conn, session):
  """
  Expect to fail to get subject in tree format if not log in. (401)
  """

  create_route_subject_test_data(db_conn)
  request = {
    'db_conn': db_conn,
    'params': {}
  }
  code, response = get_subject_tree_route(request, subject_id=subject_a_uuid)
  assert code == 200
  assert response['subjects']
  assert response['units']
  assert not response.get('buckets')


def test_subject_tree_404(db_conn, session):
  """
  Expect to fail to get subject in tree format if no subject. (404)
  """

  create_route_subject_test_data(db_conn)
  request = {
    'db_conn': db_conn,
    'cookies': {
      'session_id': session,
    },
    'params': {}
  }
  code, response = get_subject_tree_route(request, subject_id=uuid.uuid4())
  assert code == 404
  assert response.get('errors')


def test_subject_units(db_conn, session):
  """
  Expect to provide list of units to choose from.
  """

  create_route_subject_test_data(db_conn)
  request = {
    'db_conn': db_conn,
    'cookies': {
      'session_id': session,
    },
    'params': {}
  }
  code, response = get_subject_units_route(
    request,
    subject_id=subject_a_uuid
  )
  assert not response.get('errors')
  assert code == 200
  assert response['units']
  assert response['subject']
  assert response['next']


def test_subject_units_401(db_conn, session):
  """
  Expect to fail to provide list of units if not log in. (401)
  """

  create_route_subject_test_data(db_conn)
  request = {
    'db_conn': db_conn,
    'params': {}
  }
  code, response = get_subject_units_route(
    request,
    subject_id=subject_a_uuid
  )
  assert code == 401
  assert response.get('errors')


def test_subject_units_404(db_conn, session):
  """
  Expect to fail to provide list of units if subject not found. (404)
  """

  create_route_subject_test_data(db_conn)
  request = {
    'db_conn': db_conn,
    'cookies': {
      'session_id': session,
    },
    'params': {}
  }
  code, response = get_subject_units_route(request, subject_id=uuid.uuid4())
  assert code == 404
  assert response.get('errors')


def test_choose_unit(db_conn, session):
  """
  Expect to let a learner choose their unit.
  """

  create_route_subject_test_data(db_conn)
  current_user = get_user_by_id(db_conn, {'id': user_id})
  set_learning_context(
    user=current_user,
    subject={'entity_id': convert_uuid_to_slug(subject_a_uuid)}
  )
  request = {
    'db_conn': db_conn,
    'cookies': {
      'session_id': session,
    },
    'params': {}
  }
  code, response = choose_unit_route(
    request,
    subject_id=subject_a_uuid,
    unit_id=unit_a_uuid
  )
  assert not response.get('errors')
  assert code == 200
  assert response['next']


@xfail
def test_choose_unit_401(db_conn, session):
  """
  Expect to fail to choose unit if not log in. (401)
  """

  create_route_subject_test_data(db_conn)
  request = {
    'db_conn': db_conn,
    'cookies': {
      'session_id': session,
    },
    'params': {}
  }
  code, response = choose_unit_route(
    request,
    subject_id=subject_a_uuid,
    unit_id=unit_a_uuid
  )
  assert not response.get('errors')
  assert code == 200
  assert response['###']


@xfail
def test_choose_unit_404(db_conn, session):
  """
  Expect to fail to choose unit if unit doesn't exist. (404)
  """

  create_route_subject_test_data(db_conn)
  request = {
    'db_conn': db_conn,
    'cookies': {
      'session_id': session,
    },
    'params': {}
  }
  code, response = choose_unit_route(
    request,
    subject_id=subject_a_uuid,
    unit_id=unit_a_uuid
  )
  assert not response.get('errors')
  assert code == 200
  assert response['###']


@xfail
def test_choose_unit_400(db_conn, session):
  """
  Expect to fail to choose unit if request is nonsense. (400)
  """

  create_route_subject_test_data(db_conn)
  request = {
    'db_conn': db_conn,
    'cookies': {
      'session_id': session,
    },
    'params': {}
  }
  code, response = choose_unit_route(
    request,
    subject_id=subject_a_uuid,
    unit_id=unit_a_uuid
  )
  assert not response.get('errors')
  assert code == 200
  assert response['###']


@xfail
def test_choose_unit_extra(db_conn, session):
  """
  Expect choose unit to show time estimate and learning objective.
  """

  create_route_subject_test_data(db_conn)
  request = {
    'db_conn': db_conn,
    'cookies': {
      'session_id': session,
    },
    'params': {}
  }
  code, response = choose_unit_route(
    request,
    subject_id=subject_a_uuid,
    unit_id=unit_a_uuid
  )
  assert not response.get('errors')
  assert code == 200
  assert response['###']


@xfail
def test_choose_unit_avail(db_conn, session):
  """
  Expect choose unit to only show available units. (No requires remaining.)
  """

  create_route_subject_test_data(db_conn)
  request = {
    'db_conn': db_conn,
    'cookies': {
      'session_id': session,
    },
    'params': {}
  }
  code, response = choose_unit_route(
    request,
    subject_id=subject_a_uuid,
    unit_id=unit_a_uuid
  )
  assert not response.get('errors')
  assert code == 200
  assert response['###']


@xfail
def test_choose_unit_ordering(db_conn, session):
  """
  Expect to prefer units with more dependencies in choose unit.
  """

  create_route_subject_test_data(db_conn)
  request = {
    'db_conn': db_conn,
    'cookies': {
      'session_id': session,
    },
    'params': {}
  }
  code, response = choose_unit_route(
    request,
    subject_id=subject_a_uuid,
    unit_id=unit_a_uuid
  )
  assert not response.get('errors')
  assert code == 200
  assert response['###']


def test_get_my_recently_created_subjects_route(db_conn, session):
  create_route_subject_test_data(db_conn)
  request = {
    'db_conn': db_conn,
    'cookies': {
      'session_id': session,
    },
    'params': {}
  }
  code, response = get_my_recently_created_subjects_route(request)
  assert not response.get('errors')
  assert code == 200
  assert response['subjects']


def test_create_new_subject_version_route(db_conn, session):
  create_route_subject_test_data(db_conn)
  request = {
    'db_conn': db_conn,
    'cookies': {
      'session_id': session,
    },
    'params': {
      'name': 'History',
      'body': 'History is fun.',
      'members': [{
        'kind': 'subject',
        'id': convert_uuid_to_slug(subject_a_uuid),
      }],
    }
  }
  code, response = create_new_subject_version_route(request)
  assert not response.get('errors')
  assert code == 200
  assert response['version']


def test_create_existing_subject_version_route(db_conn, session):
  create_route_subject_test_data(db_conn)
  request = {
    'db_conn': db_conn,
    'cookies': {
      'session_id': session,
    },
    'params': {
      'name': 'Historyz',
    }
  }
  code, response = create_existing_subject_version_route(
    request,
    subject_id=subject_b_uuid
  )
  assert not response.get('errors')
  assert code == 200
  assert response['version']
