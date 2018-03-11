import uuid
from datetime import datetime
import psycopg2.extras

import database.util as util
from database.util import insert_row, update_row, save_row, get_row, \
  list_rows, delete_row, convert_fields_to_pgjson
from modules.util import extend, omit, convert_slug_to_uuid
from modules.validations import is_required, is_string, \
  has_min_length, is_one_of
from schemas.index import schema as default
from schemas.user import schema as user_schema
from conftest import user_id


def test_convert_fields_to_pgjson():
  params = {
    'data': {},
  }
  result = convert_fields_to_pgjson(params)
  assert not isinstance(result['data'], dict)


def test_insert_row(db_conn):
  query = """
    INSERT INTO users
    (  name  ,   email  ,   password  ,   settings  )
    VALUES
    (%(name)s, %(email)s, %(password)s, %(settings)s)
    RETURNING *;
  """
  data = {
    'name': 'Hi',
    'email': 'hi@example.com',
    'password': 'abcd1234',
    'settings': {},
  }
  result, errors = insert_row(db_conn, user_schema, query, data)
  assert not errors
  assert result


def test_insert_row_err(db_conn):
  query = """
    INSERT INTO users
    (  name  ,   email  ,   password  ,   settings  )
    VALUES
    (%(name)s, %(email)s, %(password)s, %(settings)s)
    RETURNING *;
  """
  data = {
    'name': 'Hi',
    'email': 'hi@example.com',
    'password': 'abcd',
    'settings': {},
  }
  result, errors = insert_row(db_conn, user_schema, query, data)
  assert errors
  assert not result


def test_update_row(db_conn, session):
  query = """
    UPDATE users
    SET name = %(name)s
    WHERE id = %(id)s
    RETURNING *;
  """
  prev_data = {
    'id': convert_slug_to_uuid(user_id),
    'email': 'test@example.com',
    'password': '$2a$abcd1234',
  }
  data = {
    'name': 'Hello!',
  }
  result, errors = update_row(db_conn, user_schema, query, prev_data, data)
  assert not errors
  assert result


def test_update_row_error(db_conn, session):
  query = """
    UPDATE users
    SET name = %(name)s
    WHERE id = %(id)s
    RETURNING *;
  """
  prev_data = {
    'id': convert_slug_to_uuid(user_id),
    'email': 'test@example.com',
    'password': '$2a$ab',
  }
  data = {
    'name': 'Hello!',
  }
  result, errors = update_row(db_conn, user_schema, query, prev_data, data)
  assert errors
  assert not result


def test_save_row(db_conn):
  query = """
    INSERT INTO users
    (  id  ,   created  ,   modified  ,
       name  ,   email  ,   password  ,   settings)
    VALUES
    (%(id)s, %(created)s, %(modified)s,
     %(name)s, %(email)s, %(password)s, %(settings)s)
    RETURNING *;
  """
  params = {
    'id': uuid.uuid4(),
    'created': datetime.utcnow(),
    'modified': datetime.utcnow(),
    'name': 'Hi',
    'email': 'hi@example.com',
    'password': '$2a$abcd1234',
    'settings': psycopg2.extras.Json({}),
  }
  result, errors = save_row(db_conn, query, params)
  assert not errors
  assert result


def test_save_row_error(db_conn):
  query = """
    INSERT INTO users
    (  id  ,   created  ,   modified  ,
       name  ,   email  ,   password  ,   settings)
    VALUES
    (%(id)s, %(created)s, %(modified)s,
     %(name)s, %(email)s, %(password)s, %(settings)s)
    RETURNING *;
  """
  params = {
    'id': uuid.uuid4(),
    'created': datetime.utcnow(),
    'modified': datetime.utcnow(),
    'name': 'Hi',
    'email': 'hi@example.com',
    'password': '',
    'settings': psycopg2.extras.Json({}),
  }
  result, errors = save_row(db_conn, query, params)
  assert errors
  assert not result


def test_get_row(db_conn, session):
  query = """
    SELECT *
    FROM users
    WHERE id = %(id)s
    LIMIT 1;
  """
  params = {
    'id': convert_slug_to_uuid(user_id),
  }
  result = get_row(db_conn, query, params)
  assert result['id'] == convert_slug_to_uuid(user_id)


def test_get_row_error(db_conn):
  query = "a;"
  params = {}
  result = get_row(db_conn, query, params)
  assert result is None


def test_list_rows(db_conn, session):
  query = """
    SELECT id
    FROM users
    ORDER BY created DESC;
    /* TODO OFFSET LIMIT */
  """
  params = {}
  result = list_rows(db_conn, query, params)
  assert result[0]['id'] == convert_slug_to_uuid(user_id)


def test_list_rows_error(db_conn):
  query = "a;"
  params = {}
  result = list_rows(db_conn, query, params)
  assert result == []


def test_delete_row(db_conn, session):
  params = {
    'id': convert_slug_to_uuid(user_id),
  }

  def get():
    query = """
      SELECT *
      FROM users
      WHERE id = %(id)s
      LIMIT 1;
    """
    result = get_row(db_conn, query, params)
    return result

  assert get()
  query = """
    DELETE FROM users
    WHERE id = %(id)s;
  """
  errors = delete_row(db_conn, query, params)
  assert not errors
  assert not get()


def test_delete_row_error(db_conn):
  query = "a;"
  params = {}
  errors = delete_row(db_conn, query, params)
  assert errors


###############################################################################


def lowercase_and_strip(s):
  return s.lower().strip()


def default_brown():
  return 'brown'


vases_schema = extend({}, default, {
  'tablename': 'vases',
  'fields': {
    'name': {
      'validate': (is_required, is_string,),
      'bundle': lowercase_and_strip,
      'unique': True,
    },
    'shape': {
      'validate': ((is_one_of, 'round', 'square', 'triangle'),),
      'default': 'round'
    },
    'plants': {
      'validate': (is_required, (has_min_length, 1,),),
      'default': [],
      'embed_many': {
        'species': {
          'bundle': lowercase_and_strip,
        },
        'quantity': {
          'default': 1,
          'access': ('private',)
        }
      },
    },
    'soil': {
      'validate': (is_required,),
      'default': {},
      'access': ('private',),
      'embed': {
        'color': {
          'default': default_brown,
          'bundle': lowercase_and_strip,
          'validate': (is_required, (is_one_of,
                                     'brown',
                                     'black',
                                     'gray',
                                     'clay',
                                    ))
          }
        },
    }
  },
})


def create_test_data_set(db_conn):
  """
  Create a set of fake data.
  """

  data = [{
    'name': 'celestial',
    'shape': 'round',
    'plants': [
      {'species': 'zzplant', 'quantity': 2},
      {'species': 'rubbertree', 'quantity': 1},
    ],
    'soil': {'color': 'black'}
  }, {
    'name': 'kitch',
    'shape': 'round',
    'plants': [
      {'species': 'sunflower', 'quantity': 1},
      {'species': 'geranium', 'quantity': 3},
    ],
    'soil': {'color': 'brown'}
  }, {
    'name': 'modern',
    'shape': 'square',
    'plants': [
      {'species': 'fiddle-leaf-fig', 'quantity': 1},
      {'species': 'rubbertree', 'quantity': 3},
    ],
    'soil': {'color': 'black'}
  }]
  return data


def test_recurse_embeds():
  o = {}

  def _(data, field_name, field_schema, prefix):
    o[prefix + field_name] = data.get(field_name)

  schema = vases_schema
  data = {
    'name': 'celestial',
    'shape': 'round',
    'plants': [
      {'species': 'zzplant'},
      {'species': 'rubbertree'},
    ],
    'soil': {'color': 'black'}
  }
  util.recurse_embeds(_, data, schema['fields'])
  assert o == {
    'created': None,
    'id': None,
    'modified': None,
    'name': 'celestial',
    'plants': [{'species': 'zzplant'}, {'species': 'rubbertree'}],
    'plants.0.species': 'zzplant',
    'plants.0.quantity': None,
    'plants.1.species': 'rubbertree',
    'plants.1.quantity': None,
    'shape': 'round',
    'soil': {'color': 'black'},
    'soil.color': 'black'
  }


def test_prepare_row(db_conn):
  schema = vases_schema
  create_test_data_set(db_conn)
  data = {
    'id': uuid.uuid4(),
    'name': ' celestial ',
    'shape': 'round',
    'plants': [
      {'species': 'zzplant', 'quantity': 2},
      {'species': 'rubbertree', 'quantity': 1},
    ],
    'soil': {'color': 'black'}
  }
  result, errors = util.prepare_row(db_conn, schema, data)
  assert not errors
  result = omit(result, ('id', 'modified', 'created',))
  assert result == omit(data, ('id',))


def test_tidy_fields():
  schema = vases_schema
  data = {
    'shiny': True,
    'name': 'celestial',
    'shape': 'round',
    'plants': [
      {'species': 'zzplant', 'quantity': 2},
      {'species': 'rubbertree', 'leaves': 90},
    ],
    'soil': {'color': 'black', 'texture': 'gritty'}
  }
  data2 = util.tidy_fields(schema, data)
  assert data2 == {
    'name': 'celestial',
    'shape': 'round',
    'plants': [
      {'species': 'zzplant', 'quantity': 2},
      {'species': 'rubbertree'},
    ],
    'soil': {'color': 'black'}
  }


def test_add_default_fields():
  schema = vases_schema
  data = {}
  data2 = util.add_default_fields(schema, data)
  data2 = omit(data2, ('id', 'created', 'modified',))
  assert data2 == {
    'plants': [],
    'shape': 'round',
    'soil': {'color': 'brown'},
  }


def test_validate_fields():
  schema = vases_schema
  data = {
    'name': 43,
    'shape': 'turkey',
    'plants': [],
    'soil': {'color': 'green'}
  }
  errors = util.validate_fields(schema, data)
  assert len(errors) == 4

  def find(fn, l):
    return list(filter(fn, l))[0]

  name_error = find(lambda e: e['name'] == 'name', errors)
  assert name_error['message'] == 'Must be a string.'
  soil_error = find(lambda e: e['name'] == 'soil.color', errors)
  assert soil_error['message'] == 'Must be one of brown, black, gray, clay.'
  plants_error = find(lambda e: e['name'] == 'plants', errors)
  assert plants_error['message'] == 'Must have minimum length of 1.'
  shape_error = find(lambda e: e['name'] == 'shape', errors)
  assert shape_error['message'] == 'Must be one of round, square, triangle.'


def test_bundle_fields():
  schema = vases_schema
  data = {
    'id': 'ZdhhJQ9U9YJaanmfMEpm05qc',
    'name': ' cElEstial ',
    'shape': 'round',
    'plants': [
      {'species': '  zzplant', 'quantity': 2},
      {'species': 'rubbertree', 'quantity': 1},
    ],
    'soil': {'color': '  BLACK  '}
  }
  bundle = util.bundle_fields(schema, data)
  assert bundle == {
    'id': 'ZdhhJQ9U9YJaanmfMEpm05qc',
    'name': 'celestial',
    'shape': 'round',
    'plants': [
      {'species': 'zzplant', 'quantity': 2},
      {'species': 'rubbertree', 'quantity': 1},
    ],
    'soil': {'color': 'black'}
  }


def test_deliver_fields():
  schema = vases_schema
  data = {
    'id': 'ZdhhJQ9U9YJaanmfMEpm05qc',
    'name': ' cElEstial ',
    'shape': 'round',
    'plants': [
      {'species': '  zzplant', 'quantity': 2},
      {'species': 'rubbertree', 'quantity': 1},
    ],
    'soil': {'color': '  BLACK  '}
  }
  assert util.deliver_fields(schema, data, 'private') == {
    'id': 'ZdhhJQ9U9YJaanmfMEpm05qc',
    'name': ' cElEstial ',
    'shape': 'round',
    'plants': [
      {'species': '  zzplant', 'quantity': 2},
      {'species': 'rubbertree', 'quantity': 1},
    ],
    'soil': {'color': '  BLACK  '}
  }
  assert util.deliver_fields(schema, data) == {
    'id': 'ZdhhJQ9U9YJaanmfMEpm05qc',
    'name': ' cElEstial ',
    'shape': 'round',
    'plants': [
      {'species': '  zzplant'},
      {'species': 'rubbertree'},
    ],
    'soil': {}
  }
