# TODO all saves should go to ES

import uuid

from schemas.unit import schema as unit_schema
from database.util import deliver_fields
from database.entity_base import save_entity_to_es
from database.util import insert_row, save_row, get_row, list_rows
from modules.util import convert_slug_to_uuid


def ensure_requires(db_conn, data):
  """
  Make sure every required unit actually exists.
  """

  units = list_latest_accepted_units(db_conn, data['require_ids'])
  if len(data['require_ids']) != len(units):
    return [{
      'name': 'require_ids',
      'message': 'Didn\'t find all requires.',
      'ref': 'wpd1JttyS02i8jN1CFM78w',
    }]
  return []


def ensure_no_cycles(db_conn, data):
  """
  Ensure no require cycles form.
  """

  from database.entity_facade import find_requires_cycle

  if find_requires_cycle(db_conn, 'units', data):
    return [{
      'name': 'require_ids',
      'message': 'Found a cycle in requires.',
      'ref': '5Ld85zgEQmGfAF7HkRRVvA',
    }]
  return []


def insert_unit(db_conn, data):
  """
  Create a new version of a new unit, saving to ES.
  """

  schema = unit_schema
  query = """
    INSERT INTO units_entity_id (entity_id)
    VALUES (%(entity_id)s);
    INSERT INTO units
    (  entity_id  ,   name  ,   user_id  ,
       body  ,   require_ids  )
    VALUES
    (%(entity_id)s  , %(name)s, %(user_id)s,
     %(body)s, %(require_ids)s)
    RETURNING *;
  """
  data = {
    'entity_id': uuid.uuid4(),
    'name': data['name'],
    'user_id': convert_slug_to_uuid(data['user_id']),
    'body': data['body'],
    'require_ids': [convert_slug_to_uuid(require_id)
                    for require_id in data.get('require_ids', [])],
  }
  errors = ensure_requires(db_conn, data) + ensure_no_cycles(db_conn, data)
  if errors:
    return None, errors
  data, errors = insert_row(db_conn, schema, query, data)
  if not errors:
    save_entity_to_es('unit', deliver_unit(data, access='view'))
  return data, errors


def insert_unit_version(db_conn, current_data, next_data):
  """
  Create a new version of a existing unit, saving to ES.
  """

  schema = unit_schema
  query = """
    INSERT INTO units
    (  entity_id  ,   previous_id  ,   name  ,   user_id  ,
       body  ,   require_ids  )
    VALUES
    (%(entity_id)s, %(previous_id)s, %(name)s, %(user_id)s,
     %(body)s, %(require_ids)s)
    RETURNING *;
  """
  data = {
    'entity_id': current_data['entity_id'],
    'previous_id': current_data['version_id'],
    'user_id': convert_slug_to_uuid(next_data['user_id']),
    'name': next_data.get('name') or current_data.get('name'),
    'body': next_data.get('body') or current_data.get('body'),
    'require_ids': [convert_slug_to_uuid(require_id)
                    for require_id in
                    next_data.get('require_ids') or
                    current_data.get('require_ids') or []],
  }
  errors = ensure_requires(db_conn, data) + ensure_no_cycles(db_conn, data)
  if errors:
    return None, errors
  data, errors = insert_row(db_conn, schema, query, data)
  if not errors:
    save_entity_to_es('unit', deliver_unit(data, access='view'))
  return data, errors


def update_unit(db_conn, version_id, status):
  """
  Update a unit versions's status and available. [hidden]
  """

  query = """
    UPDATE units
    SET status = %(status)s
    WHERE version_id = %(version_id)s
    RETURNING *;
  """
  data = {
    'version_id': convert_slug_to_uuid(version_id),
    'status': status,
  }
  data, errors = save_row(db_conn, query, data)
  if not errors:
    save_entity_to_es('unit', deliver_unit(data, access='view'))
  return data, errors


def deliver_unit(data, access=None):
  """
  Prepare a response for JSON output.
  """

  schema = unit_schema
  return deliver_fields(schema, data, access)


def does_unit_exist(db_conn, entity_id):
  """
  Just... is this a valid unit entity_id.
  """

  query = """
    SELECT entity_id
    FROM units_entity_id
    WHERE entity_id = %(entity_id)s
    LIMIT 1;
  """
  params = {
    'entity_id': convert_slug_to_uuid(entity_id),
  }
  return get_row(db_conn, query, params)


def get_latest_accepted_unit(db_conn, entity_id):
  """
  Get Latest Accepted Unit Version by EID
  """

  query = """
    SELECT DISTINCT ON (entity_id) *
    FROM units
    WHERE status = 'accepted' AND entity_id = %(entity_id)s
    ORDER BY entity_id, created DESC;
    /* TODO LIMIT */
  """
  params = {
    'entity_id': convert_slug_to_uuid(entity_id),
  }
  return get_row(db_conn, query, params)


def list_latest_accepted_units(db_conn, entity_ids):
  """
  List Latest Accepted Unit Versions by EIDs
  """

  if not entity_ids:
    return []
  query = """
    SELECT DISTINCT ON (entity_id) *
    FROM units
    WHERE status = 'accepted' AND entity_id in %(entity_ids)s
    ORDER BY entity_id, created DESC;
    /* TODO LIMIT OFFSET */
  """
  params = {'entity_ids': tuple([
    convert_slug_to_uuid(entity_id)
    for entity_id in entity_ids
  ])}
  return list_rows(db_conn, query, params)


def list_many_unit_versions(db_conn, version_ids):
  """
  List Unit Versions by VIDs
  """

  if not version_ids:
    return []
  query = """
    SELECT *
    FROM units
    WHERE version_id in %(version_ids)s
    ORDER BY created DESC;
    /* TODO LIMIT OFFSET */
  """
  params = {'version_ids': tuple(
    convert_slug_to_uuid(vid)
    for vid in version_ids
  )}
  return list_rows(db_conn, query, params)


def get_unit_version(db_conn, version_id):
  """
  Get a unit version.
  """

  query = """
    SELECT *
    FROM units
    WHERE version_id = %(version_id)s
    ORDER BY created DESC;
    /* TODO LIMIT OFFSET */
  """
  params = {'version_id': convert_slug_to_uuid(version_id)}
  return get_row(db_conn, query, params)


def list_one_unit_versions(db_conn, entity_id):
  """
  List Unit Versions by EID
  """

  query = """
    SELECT *
    FROM units
    WHERE entity_id = %(entity_id)s
    ORDER BY created DESC;
    /* TODO LIMIT OFFSET */
  """
  params = {'entity_id': convert_slug_to_uuid(entity_id)}
  return list_rows(db_conn, query, params)


def list_required_units(db_conn, entity_id):
  """
  List Latest Version of Required Units by EID
  """

  later_unit = get_latest_accepted_unit(db_conn, entity_id)
  return list_latest_accepted_units(db_conn, later_unit['require_ids'])


def list_required_by_units(db_conn, entity_id):
  """
  List Latest Version of Required By Units by EID
  """

  query = """
    WITH temp as (
      SELECT DISTINCT ON (entity_id) *
      FROM units
      WHERE status = 'accepted'
      ORDER BY entity_id, created DESC
    )
    SELECT *
    FROM temp
    WHERE %(entity_id)s = ANY(require_ids)
    ORDER BY created DESC;
    /* TODO LIMIT OFFSET */
  """
  params = {
    'entity_id': convert_slug_to_uuid(entity_id),
  }
  return list_rows(db_conn, query, params)


def list_units_by_subject_flat(db_conn, subject_id):
  """
  List Units by Subject EID
  """

  from database.subject import get_latest_accepted_subject

  subject = get_latest_accepted_subject(db_conn, subject_id)
  unit_ids = [
    member['id']
    for member in subject['members']
    if member['kind'] == 'unit'
  ]
  return list_latest_accepted_units(db_conn, unit_ids)


def list_my_recently_created_units(db_conn, user_id):
  """
  List My Recently Created Units (by User ID)
  """

  query = """
    SELECT DISTINCT ON (entity_id) *
    FROM units
    WHERE user_id = %(user_id)s
    ORDER BY entity_id, created DESC;
    /* TODO LIMIT OFFSET */
  """
  params = {'user_id': user_id}
  return list_rows(db_conn, query, params)


def list_all_unit_entity_ids(db_conn):
  """
  List all unit entity ids.
  """

  query = """
    SELECT entity_id
    FROM units;
  """
  params = {}
  return [
    row['entity_id']
    for row in list_rows(db_conn, query, params)
  ]
