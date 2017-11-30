from copy import deepcopy

from schemas.notice import schema as notice_schema
from modules.content import get as c
from modules.util import convert_slug_to_uuid, pick
from database.util import insert_row, save_row, get_row, list_rows
from database.util import deliver_fields


# done-- implement create_topic notice
# done-- implement create_proposal notice
# done-- implement block_proposal notice
# TODO-2 implement decline_proposal notice
# done-- implement accept_proposal notice
# TODO-2 implement create_post notice
# TODO-2 implement come_back notice


"""
Required data fields per kind:

create_topic: user_name, topic_name, entity_kind, entity_name
create_proposal: user_name, proposal_name, entity_kind, entity_name
block_proposal: user_name, proposal_name, entity_kind, entity_name
decline_proposal: user_name, proposal_name, entity_kind, entity_name
accept_proposal: proposal_name, entity_kind, entity_name
create_post: user_name, topic_name, entity_kind, entity_name
come_back: -
"""


def get_notice(db_conn, params):
  """
  Get the user matching the parameters.
  """

  query = """
    SELECT *
    FROM notices
    WHERE id = %(id)s
    LIMIT 1;
  """
  params = {
    'id': convert_slug_to_uuid(params['id']),
  }
  return get_row(db_conn, query, params)


def insert_notice(db_conn, data):
  """
  Create a new notice.
  """

  schema = notice_schema
  query = """
    INSERT INTO notices
    (  user_id  ,   kind  ,   data  )
    VALUES
    (%(user_id)s, %(kind)s, %(data)s)
    RETURNING *;
  """
  data = pick(data, ('user_id', 'kind', 'data'))
  data, errors = insert_row(db_conn, schema, query, data)
  return data, errors


def list_notices(db_conn, params):
  """
  Get a list of models matching the provided arguments.
  Also adds pagination capabilities.
  Returns empty array when no models match.
  TODO-2 add filters for kind, tags, read
  """

  query = """
    SELECT *
    FROM notices
    WHERE user_id = %(user_id)s
    ORDER BY created DESC
    LIMIT %(limit)s
    OFFSET %(offset)s;
  """
  params = {
    'user_id': convert_slug_to_uuid(params['user_id']),
    'limit': params.get('limit') or 10,
    'offset': params.get('offset') or 0,
  }
  return list_rows(db_conn, query, params)


def mark_notice_as_read(db_conn, notice):
  """
  Marks the notice as read.
  """

  query = """
    UPDATE notices
    SET read = TRUE
    WHERE id = %(id)s
    RETURNING *;
  """
  data = {
    'id': convert_slug_to_uuid(notice['id']),
  }
  # Skipping validation here... there's only one field changing.
  data, errors = save_row(db_conn, query, data)
  return data, errors


def mark_notice_as_unread(db_conn, notice):
  """
  Marks the notice as unread.
  """

  query = """
    UPDATE notices
    SET read = FALSE
    WHERE id = %(id)s
    RETURNING *;
  """
  data = {
    'id': convert_slug_to_uuid(notice['id']),
  }
  # Skipping validation here... there's only one field changing.
  data, errors = save_row(db_conn, query, data)
  return data, errors


def get_notice_body(notice):
  """
  Get the copy associated with this notice.
  """

  return c('notice_' + notice['kind']).format(**notice['data'])


def deliver_notice(notice, access=None):
  """
  Add the notice body to the notice before delivering.
  """

  schema = notice_schema
  notice = deepcopy(notice)
  notice['body'] = get_notice_body(notice)
  return deliver_fields(schema, notice, access)
