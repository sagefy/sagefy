import uuid
from routes.unit import get_unit_route, \
  list_units_route, \
  get_unit_versions_route, \
  get_unit_version_route, \
  get_my_recently_created_units_route, \
  create_new_unit_version_route, \
  create_existing_unit_version_route
from conftest import user_id
from raw_insert import raw_insert_units
from modules.util import convert_uuid_to_slug

unit_a_uuid = uuid.uuid4()
unit_version_a_uuid = uuid.uuid4()
unit_b_uuid = uuid.uuid4()


def create_route_unit_test_data(db_conn):
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


def test_get_unit_route(db_conn, session):
  create_route_unit_test_data(db_conn)
  request = {
    'db_conn': db_conn,
  }
  code, response = get_unit_route(request, unit_id=unit_a_uuid)
  assert not response.get('errors')
  assert code == 200
  assert response['unit']
  # TODO requires
  # TODO required_by
  # TODO belongs_to


def test_list_units_route(db_conn, session):
  create_route_unit_test_data(db_conn)
  request = {
    'db_conn': db_conn,
    'params': {
      'entity_ids': convert_uuid_to_slug(unit_a_uuid)
    }
  }
  code, response = list_units_route(request)
  assert not response.get('errors')
  assert code == 200
  assert response['units']


def test_get_unit_versions_route(db_conn, session):
  create_route_unit_test_data(db_conn)
  request = {
    'db_conn': db_conn,
  }
  code, response = get_unit_versions_route(request, unit_id=unit_a_uuid)
  assert not response.get('errors')
  assert code == 200
  assert response['versions']


def test_get_unit_version_route(db_conn, session):
  create_route_unit_test_data(db_conn)
  request = {
    'db_conn': db_conn,
  }
  code, response = get_unit_version_route(
    request,
    version_id=unit_version_a_uuid
  )
  assert not response.get('errors')
  assert code == 200
  assert response['version']


def test_get_my_recently_created_units_route(db_conn, session):
  create_route_unit_test_data(db_conn)
  request = {
    'db_conn': db_conn,
    'cookies': {
      'session_id': session,
    },
  }
  code, response = get_my_recently_created_units_route(request)
  assert not response.get('errors')
  assert code == 200
  assert response['units']


def test_create_new_unit_version_route(db_conn, session):
  create_route_unit_test_data(db_conn)
  request = {
    'db_conn': db_conn,
    'cookies': {
      'session_id': session,
    },
    'params': {
      'name': 'test unit multiply',
      'body': 'multiplying numbers is fun'
    }
  }
  code, response = create_new_unit_version_route(request)
  assert not response.get('errors')
  assert code == 200
  assert response['version']


def test_create_existing_unit_version_route(db_conn, session):
  create_route_unit_test_data(db_conn)
  request = {
    'db_conn': db_conn,
    'cookies': {
      'session_id': session,
    },
    'params': {
      'name': 'test unit divide',
      'body': 'dividing numbers is fun'
    }
  }
  code, response = create_existing_unit_version_route(
    request,
    unit_id=unit_a_uuid
  )
  assert not response.get('errors')
  assert code == 200
  assert response['version']
