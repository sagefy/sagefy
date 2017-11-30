from schemas.response import schema as response_schema
from database.util import deliver_fields
from database.util import insert_row, get_row
from modules.util import pick, convert_slug_to_uuid


def insert_response(db_conn, data):
  """
  Create a new response.
  """

  schema = response_schema
  query = """
    INSERT INTO responses
    (  user_id  ,   card_id  ,   unit_id  ,
       response  ,   score  ,   learned  )
    VALUES
    (%(user_id)s, %(card_id)s, %(unit_id)s,
     %(response)s, %(score)s, %(learned)s)
    RETURNING *;
  """
  data = pick(data, (
    'user_id',
    'card_id',
    'unit_id',
    'response',
    'score',
    'learned'
  ))
  return insert_row(db_conn, schema, query, data)


def get_latest_response(db_conn, user_id, unit_id):
  """
  Get the latest response given a user ID and a unit ID.
  """

  query = """
    SELECT *
    FROM responses
    WHERE user_id = %(user_id)s AND unit_id = %(unit_id)s
    ORDER BY created DESC
    LIMIT 1;
  """
  params = {
    'user_id': convert_slug_to_uuid(user_id),
    'unit_id': convert_slug_to_uuid(unit_id),
  }
  return get_row(db_conn, query, params)


def deliver_response(data, access=None):
  """
  Prepare a response for JSON output.
  """

  schema = response_schema
  return deliver_fields(schema, data, access)
