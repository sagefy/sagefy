# TODO all saves should go to ES

import re
import uuid

from schemas.subject import schema as subject_schema
from database.util import deliver_fields
from database.entity_base import save_entity_to_es
from database.util import insert_row, save_row, get_row, list_rows
from modules.util import convert_slug_to_uuid, convert_uuid_to_slug


def is_valid_members(db_conn, data):
  """

  """

  from database.unit import does_unit_exist

  # TODO-3 this is going to be slow
  for member_desc in data['members']:
    entity_id, kind = member_desc['id'], member_desc['kind']
    entity = None
    if kind == 'unit':
      entity = does_unit_exist(db_conn, entity_id)
    elif kind == 'subject':
      entity = does_subject_exist(db_conn, entity_id)
    if not entity:
      return [{
        'name': 'id',
        'message': 'Not a valid entity.',
        'value': entity_id,
        'ref': 'qKUTNkDuSiGLh0PZdhu9Xw',
      }]

  return []


def ensure_no_cycles(db_conn, data):
  """
  Ensure no membership cycles form.
  """

  seen = set()
  found = {'cycle': False}

  def _(members):
    entity_ids = [
      convert_slug_to_uuid(member['id'])
      for member in members
      if member['kind'] == 'subject'
    ]
    entities = list_latest_accepted_subjects(db_conn, entity_ids)
    for entity in entities:
      if entity['entity_id'] in seen:
        found['cycle'] = True
        break
      seen.add(entity['entity_id'])
      _(entity['members'])

  seen.add(data['entity_id'])
  _(data['members'])

  if found['cycle']:
    return [{
      'name': 'members',
      'message': 'Found a cycle in membership.',
      'ref': 'PfEdjTllRpqh_bKGM9oyTA',
    }]

  return []


def insert_subject(db_conn, data):
  """
  Create a new version of a new a subject, saving to ES.
  """

  schema = subject_schema
  query = """
    INSERT INTO subjects_entity_id (entity_id)
    VALUES (%(entity_id)s);
    INSERT INTO subjects
    (  entity_id  ,   name  ,   user_id  ,
       body  ,   members  )
    VALUES
    (%(entity_id)s, %(name)s, %(user_id)s,
     %(body)s, %(members)s)
    RETURNING *;
  """
  data = {
    'entity_id': uuid.uuid4(),
    'name': data['name'],
    'user_id': convert_slug_to_uuid(data['user_id']),
    'body': data['body'],
    'members': data.get('members', []),
  }
  errors = is_valid_members(db_conn, data) + ensure_no_cycles(db_conn, data)
  if errors:
    return None, errors
  data, errors = insert_row(db_conn, schema, query, data)
  if not errors:
    save_entity_to_es('subject', deliver_subject(data, access='view'))
  return data, errors


def insert_subject_version(db_conn, current_data, next_data):
  """
  Create a new version of an existing subject.
  """

  schema = subject_schema
  query = """
    INSERT INTO subjects
    (  entity_id  ,   previous_id  ,   name  ,   user_id  ,
       body  ,   members  )
    VALUES
    (%(entity_id)s, %(previous_id)s, %(name)s, %(user_id)s,
     %(body)s, %(members)s)
    RETURNING *;
  """
  data = {
    'entity_id': current_data['entity_id'],
    'previous_id': current_data['version_id'],
    'user_id': convert_slug_to_uuid(next_data['user_id']),
    'name': next_data.get('name') or current_data.get('name'),
    'body': next_data.get('body') or current_data.get('body'),
    'members': (next_data.get('members') or
                current_data.get('members') or
                []),
  }
  errors = is_valid_members(db_conn, data) + ensure_no_cycles(db_conn, data)
  if errors:
    return None, errors
  data, errors = insert_row(db_conn, schema, query, data)
  if not errors:
    save_entity_to_es('subject', deliver_subject(data, access='view'))
  return data, errors


def update_subject(db_conn, version_id, status):
  """
  Update a subject version's status and available. [hidden]
  """

  query = """
    UPDATE subjects
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
    save_entity_to_es('subject', deliver_subject(data, access='view'))
  return data, errors


def deliver_subject(data, access=None):
  """
  Prepare a response for JSON output.
  """

  schema = subject_schema
  return deliver_fields(schema, data, access)


def does_subject_exist(db_conn, entity_id):
  """
  Just... is this a valid subject entity_id.
  """

  query = """
    SELECT entity_id
    FROM subjects_entity_id
    WHERE entity_id = %(entity_id)s
    LIMIT 1;
  """
  params = {
    'entity_id': convert_slug_to_uuid(entity_id),
  }
  return get_row(db_conn, query, params)


def get_latest_accepted_subject(db_conn, entity_id):
  """
  Get Latest Accepted Subject Version by EID
  """

  query = """
    SELECT DISTINCT ON (entity_id) *
    FROM subjects
    WHERE status = 'accepted' AND entity_id = %(entity_id)s
    ORDER BY entity_id, created DESC;
    /* TODO LIMIT */
  """
  params = {
    'entity_id': convert_slug_to_uuid(entity_id),
  }
  return get_row(db_conn, query, params)


def list_latest_accepted_subjects(db_conn, entity_ids):
  """
  List Latest Accepted Subject Versions by EIDs
  """

  if not entity_ids:
    return []
  query = """
    SELECT DISTINCT ON (entity_id) *
    FROM subjects
    WHERE status = 'accepted' AND entity_id in %(entity_ids)s
    ORDER BY entity_id, created DESC;
    /* TODO LIMIT OFFSET */
  """
  params = {'entity_ids': tuple([
    convert_slug_to_uuid(entity_id)
    for entity_id in entity_ids
  ])}
  return list_rows(db_conn, query, params)


def list_many_subject_versions(db_conn, version_ids):
  """
  List Subject Versions by VIDs
  """

  if not version_ids:
    return []
  query = """
    SELECT *
    FROM subjects
    WHERE version_id in %(version_ids)s
    ORDER BY created DESC;
    /* TODO LIMIT OFFSET */
  """
  params = {'version_ids': tuple(
    convert_slug_to_uuid(vid)
    for vid in version_ids
  )}
  return list_rows(db_conn, query, params)


def get_subject_version(db_conn, version_id):
  """
  Get a subject version.
  """

  query = """
    SELECT *
    FROM subjects
    WHERE version_id = %(version_id)s
    ORDER BY created DESC;
    /* TODO LIMIT OFFSET */
  """
  params = {'version_id': convert_slug_to_uuid(version_id)}
  return get_row(db_conn, query, params)


def list_one_subject_versions(db_conn, entity_id):
  """
  List Subjects Versions by EID
  """

  query = """
    SELECT *
    FROM subjects
    WHERE entity_id = %(entity_id)s
    ORDER BY created DESC;
    /* TODO LIMIT OFFSET */
  """
  params = {'entity_id': convert_slug_to_uuid(entity_id)}
  return list_rows(db_conn, query, params)


def list_subjects_by_unit_flat(db_conn, unit_id):
  """
  List Subjects by Unit EID
  """

  unit_id = convert_uuid_to_slug(unit_id)
  # ENSURE THIS IS SQL SAFE
  unit_id = re.sub(r'[^a-zA-Z0-9\-\_]', '', unit_id)
  query = """
    WITH temp AS (
      SELECT DISTINCT ON (entity_id) *
      FROM subjects
      WHERE status = 'accepted'
      ORDER BY entity_id, created DESC
    )
    SELECT *
    FROM temp
    WHERE members @> '[{"id":"%(unit_id)s"}]'
    ORDER BY created DESC;
    /* TODO limit offset */
  """ % {'unit_id': unit_id}
  params = {}
  return list_rows(db_conn, query, params)


def list_subject_parents(db_conn, subject_id):
  """
  List the direct parents of the subject specified.
  """

  subject_id = convert_uuid_to_slug(subject_id)
  # ENSURE THIS IS SQL SAFE
  subject_id = re.sub(r'[^a-zA-Z0-9\-\_]', '', subject_id)
  query = """
    WITH temp AS (
      SELECT DISTINCT ON (entity_id) *
      FROM subjects
      WHERE status = 'accepted'
      ORDER BY entity_id, created DESC
    )
    SELECT *
    FROM temp
    WHERE members @> '[{"id":"%(subject_id)s"}]'
    ORDER BY created DESC;
    /* TODO limit offset */
  """ % {'subject_id': subject_id}
  params = {}
  return list_rows(db_conn, query, params)


def list_my_recently_created_subjects(db_conn, user_id):
  """
  List My Recently Created Subjects (by User ID)
  """

  query = """
    SELECT DISTINCT ON (entity_id) *
    FROM subjects
    WHERE user_id = %(user_id)s
    ORDER BY entity_id, created DESC;
    /* TODO LIMIT OFFSET */
  """
  params = {'user_id': user_id}
  return list_rows(db_conn, query, params)


def list_all_subject_entity_ids(db_conn):
  """
  List all subject entity ids.
  """

  query = """
    SELECT entity_id
    FROM subjects;
  """
  params = {}
  return [
    row['entity_id']
    for row in list_rows(db_conn, query, params)
  ]


def get_recommended_subjects(db_conn):
  """
  list recommended subjects
  """

  query = """
    SELECT DISTINCT ON (entity_id) *
    FROM subjects
    WHERE status = 'accepted' AND name = %(name)s
    ORDER BY entity_id, created DESC;
    /* TODO LIMIT OFFSET */
  """
  params = {
    'name': 'An Introduction to Electronic Music',
  }
  return list_rows(db_conn, query, params)
