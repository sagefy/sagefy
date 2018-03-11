from framework.elasticsearch_conn import es
from schemas.topic import schema as topic_schema
from database.util import deliver_fields
from database.util import insert_row, update_row, get_row, list_rows
from modules.util import json_prep, pick
from modules.util import convert_slug_to_uuid, convert_uuid_to_slug


# TODO-1 validate foreign on entity_id

def insert_topic(db_conn, data):
  """
  Create a new topic.
  """

  schema = topic_schema
  query = """
    INSERT INTO topics
    (  user_id  ,   entity_id  ,   entity_kind  ,   name  )
    VALUES
    (%(user_id)s, %(entity_id)s, %(entity_kind)s, %(name)s)
    RETURNING *;
  """
  data = pick(data, ('user_id', 'entity_id', 'entity_kind', 'name'))
  if data.get('entity_id'):
    data['entity_id'] = convert_slug_to_uuid(data['entity_id'])
  data, errors = insert_row(db_conn, schema, query, data)
  if not errors:
    add_topic_to_es(data)
  return data, errors


def update_topic(db_conn, prev_data, data):
  """
  Update an existing topic. Only the name can be changed.
  """

  schema = topic_schema
  query = """
    UPDATE topics
    SET name = %(name)s
    WHERE id = %(id)s
    RETURNING *;
  """
  data = {
    'id': convert_slug_to_uuid(prev_data['id']),
    'name': data['name'],
  }
  data, errors = update_row(db_conn, schema, query, prev_data, data)
  if not errors:
    add_topic_to_es(data)
  return data, errors


def get_topic(db_conn, params):
  """
  Get the topic matching the parameters.
  """

  query = """
    SELECT *
    FROM topics
    WHERE id = %(id)s
    LIMIT 1;
  """
  params = {
    'id': convert_slug_to_uuid(params['id']),
  }
  return get_row(db_conn, query, params)


def list_topics(db_conn, params):
  """
  Get a list of _all_ topics in Sagefy.
  """

  query = """
    SELECT *
    FROM topics
    ORDER BY created DESC;
    /* TODO OFFSET LIMIT */
  """
  params = {}
  return list_rows(db_conn, query, params)


def deliver_topic(data, access=None):
  """
  Prepare user data for JSON response.
  """

  schema = topic_schema
  return deliver_fields(schema, data, access)


def list_topics_by_entity_id(db_conn, entity_id, params):
  """
  Get a list of models matching the provided keyword arguments.
  Return empty array when no models match.
  """

  query = """
    SELECT *
    FROM topics
    WHERE entity_id = %(entity_id)s
    ORDER BY created DESC;
    /* TODO OFFSET LIMIT */
  """
  params = {
    'entity_id': convert_slug_to_uuid(entity_id),
  }
  return list_rows(db_conn, query, params)


def add_topic_to_es(topic):
  """
  Add the topic to ElasticSearch.
  """

  data = json_prep(deliver_topic(topic))
  return es.index(
    index='entity',
    doc_type='topic',
    body=data,
    id=convert_uuid_to_slug(data['id']),
  )
