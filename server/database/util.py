
from copy import deepcopy
from modules.util import omit, extend, pick
import psycopg2
import psycopg2.extras


def convert_fields_to_pgjson(data):
  """
  Whatever. Ughh.. TODO-1 fix this.
  """

  fields = (
    'settings',
    'data',
    'members',
    'entity_versions',
    'guess_distribution',
    'slip_distribution',
  )
  for field in fields:
    if data.get(field) is not None:
      data[field] = psycopg2.extras.Json(data[field])
  return data


def insert_row(db_conn, schema, query, data):
  """
  Validate a row, then insert the row.
  """

  data = omit(data, ('id', 'created', 'modified'))
  # TODO-2 is it possible to have postgres do this work of
  #    validating/preparing?
  data, errors = prepare_row(db_conn, schema, data)
  if errors:
    return None, errors
  data = bundle_fields(schema, data)
  data = convert_fields_to_pgjson(data)  # TODO-1 fix this
  data, errors = save_row(db_conn, query, data)
  return data, errors


def update_row(db_conn, schema, query, prev_data, data):
  """
  Validate changes, then update row.
  """

  data = omit(data, ('id', 'created', 'modified'))
  data = extend({}, prev_data, data)
  # TODO-2 is it possible to have postgres do this work of
  #    validating/preparing?
  data, errors = prepare_row(db_conn, schema, data)
  if errors:
    return None, errors
  data = bundle_fields(schema, data)
  data = convert_fields_to_pgjson(data)  # TODO-1 fix this
  data, errors = save_row(db_conn, query, data)
  return data, errors


def save_row(db_conn, query, params):
  """
  Insert or update a row using psycopg2.
  Validate data before using!
  Probably best to not call this directly: use `insert` or `update` instead.
  """

  data, errors = None, []
  try:
    db_curr = db_conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    with db_curr:
      db_curr.execute(query, params)
      data = db_curr.fetchone()
      db_conn.commit()
  except (Exception, psycopg2.DatabaseError) as error:  #
    print('DB Error', query, error)
    errors = [{
      'message': 'There was an error. Contact <support@sagefy.org>.',
      'ref': 'pu7amyK_REGFYCpUSfbdMw',
    }]
    db_conn.rollback()
    # TODO-1 parse through errors, make user friendly
  return data, errors


def get_row(db_conn, query, params):
  """
  Get a single row using psycopg2.
  """

  data = None
  try:
    db_curr = db_conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    with db_curr:
      db_curr.execute(query, params)
      data = db_curr.fetchone()
  except (Exception, psycopg2.DatabaseError) as error:
    print('DB Error', query, error)
    db_conn.rollback()
  return data


def list_rows(db_conn, query, params):
  """
  List rows using psycopg2.
  """

  data = []
  try:
    db_curr = db_conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    with db_curr:
      db_curr.execute(query, params)
      data = db_curr.fetchall()
    data = [row for row in data]
  except (Exception, psycopg2.DatabaseError) as error:
    print('DB Error', query, error)
    db_conn.rollback()
  return data


def delete_row(db_conn, query, params):
  """
  Delete a row using psycopg2.
  """

  errors = []
  try:
    db_curr = db_conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    with db_curr:
      db_curr.execute(query, params)
      db_conn.commit()
  except (Exception, psycopg2.DatabaseError) as error:
    print('DB Error', query, error)
    errors = [{
      'message': 'There was an error. Contact <support@sagefy.org>.',
      'ref': 'hpaIei7gT9SwihpJxRYYQA',
    }]
    db_conn.rollback()
    # TODO-1 parse through errors, make user friendly
  return errors


###############################################################################


def recurse_embeds(fn, data, schema, prefix=''):
  for field_name, field_schema in schema.items():
    fn(data, field_name, field_schema, prefix)

    if 'embed' in field_schema:
      data[field_name] = data.get(field_name) or {}
      recurse_embeds(fn, data[field_name], field_schema['embed'],
                     '%s%s.' % (prefix, field_name))

    elif 'embed_many' in field_schema:
      data[field_name] = data.get(field_name) or []
      for i, d in enumerate(data[field_name]):
        recurse_embeds(fn, d, field_schema['embed_many'],
                       '%s%s.%i.' % (prefix, field_name, i))


def prepare_row(db_conn, schema, data):
  """
  Prepare a document to be saved.
  """

  data = tidy_fields(schema, data)
  data = add_default_fields(schema, data)
  # NOTA BENE: add_default_fields must come before validate_unique_fields
  errors = validate_fields(schema, data)
  if errors:
    return data, errors
  return data, []


def tidy_fields(schema, data):
  """
  Remove any fields that aren't part of the schema.
  For now, we'll just remove extra fields.
  Later, we might want an option to throw errors instead.
  """

  data = deepcopy(data)

  def _(data, schema):
    for name, field_schema in schema.items():
      if 'embed' in field_schema and name in data:
        data[name] = _(data[name], field_schema['embed'])
      elif 'embed_many' in field_schema and name in data:
        for i, d in enumerate(data[name]):
          data[name][i] = _(d, field_schema['embed_many'])
    return pick(data, schema.keys())

  return _(data, schema['fields'])


def add_default_fields(schema, data):
  """
  Set up defaults for data if not applied.
  """

  data = deepcopy(data)

  def _(data, field_name, field_schema, prefix):
    if 'default' in field_schema and data.get(field_name) is None:
      if hasattr(field_schema['default'], '__call__'):
        data[field_name] = field_schema['default']()
      else:
        data[field_name] = field_schema['default']

  recurse_embeds(_, data, schema['fields'])
  return data


def validate_fields(schema, data):
  """
  Iterate over the schema, ensuring that everything matches up.
  """

  errors = []

  def _(data, field_name, field_schema, prefix):
    if 'validate' not in field_schema:
      return
    error = None
    for fn in field_schema['validate']:
      if isinstance(fn, (list, tuple)):
        error = fn[0](data.get(field_name), *fn[1:])
      else:
        error = fn(data.get(field_name))
      if error:
        errors.append({
          'name': prefix + field_name,
          'message': error,
          'ref': '02PtyWvDQTKJkcD-nuSftg',
        })
        break
  recurse_embeds(_, data, schema['fields'])
  return errors


def bundle_fields(schema, data):
  """
  Prepare the data for saving into the database.
  Consider default values and will call `bundle`
  in the schema if present.
  """

  def _(data, field_name, field_schema, prefix):
    if 'bundle' in field_schema and data.get(field_name):
      data[field_name] = field_schema['bundle'](data[field_name])

  data = deepcopy(data)
  recurse_embeds(_, data, schema['fields'])
  return data


def deliver_fields(schema, data, access=None):
  """
  Prepare the data for consumption.
  Consider access allowed and will call `deliver`
  in the schema if present.
  """

  def _(data, field_name, field_schema, prefix):
    if ('access' in field_schema and
        data.get(field_name) is not None and
        access not in field_schema['access']):
      del data[field_name]

  data = deepcopy(data)
  recurse_embeds(_, data, schema['fields'])
  return data
