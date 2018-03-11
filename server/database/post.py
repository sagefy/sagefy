from framework.elasticsearch_conn import es
from modules.util import json_prep, pick
from modules.util import convert_slug_to_uuid, convert_uuid_to_slug
from schemas.post import schema as post_schema
from schemas.proposal import schema as proposal_schema
from schemas.vote import schema as vote_schema
from database.util import deliver_fields
from database.util import insert_row, update_row, get_row, list_rows


def get_post_schema(data):
  kind = data.get('kind')
  mapping = {
    'post': post_schema,
    'proposal': proposal_schema,
    'vote': vote_schema,
  }
  return mapping.get(kind) or post_schema


def is_valid_reply(db_conn, data):
  """
  For Post, Proposal, Vote.

  A reply must belong to the same topic.
  - A post can reply to a post, proposal, or vote.
  - A proposal can reply to a post, proposal, or vote.
  - A vote may only reply to a proposal.
  """

  if data.get('replies_to_id'):
    post_data = get_post(db_conn, {'id': data['replies_to_id']})
    if (not post_data
        or post_data.get('topic_id') != data.get('topic_id')):
      return [{
        'name': 'replies_to_id',
        'message': 'A reply must be in the same topic.',
        'ref': 'RmjIAVPpRQCEXTADnTzhkQ',
      }]
  return []


def validate_entity_versions(db_conn, data):
  """
  For Proposal.

  Ensure all the entity versions exist.
  """

  from database.entity_facade import get_entity_version

  for p_entity_version in data['entity_versions']:
    entity_kind = p_entity_version.get('kind')
    version_id = p_entity_version.get('id')
    entity_version = get_entity_version(db_conn, entity_kind, version_id)
    if not entity_version:
      return [{
        'name': 'entity_versions',
        'message': 'Not a valid version: {entity_kind} {version_id}'.format(
          entity_kind=entity_kind,
          version_id=version_id
        ),
        'ref': 'p4MMkyqaS8u4Z3AIAh4d0w',
      }]
  return []


def is_valid_reply_kind(db_conn, data):
  """
  For Vote.

  A vote can reply to a proposal.
  A vote cannot reply to a proposal that is accepted or declined.
  A user cannot vote on their own proposal.
  """

  from database.entity_facade import get_entity_version

  proposal_data = get_post(db_conn, {'id': data['replies_to_id']})
  if not proposal_data:
    return [{
      'name': 'replies_to_id',
      'message': 'No proposal found.',
      'ref': 'B9x2Np5mQQyNYLKv3j9rCQ',
    }]
  if proposal_data['kind'] != 'proposal':
    return [{
      'name': 'replies_to_id',
      'message': 'A vote must reply to a proposal.',
      'ref': 'qq3Im6MDS5iDYji2h645Ug',
    }]
  if proposal_data['user_id'] == data['user_id']:
    return [{
      'name': 'replies_to_id',
      'message': 'You cannot vote on your own proposal.',
      'ref': 'sVuOAjaJTcqvCrd7DewDLw',
    }]
  entity_kind = proposal_data['entity_versions'][0]['kind']
  version_id = proposal_data['entity_versions'][0]['id']
  entity_version = get_entity_version(db_conn, entity_kind, version_id)
  if not entity_version:
    return [{
      'name': 'replies_to_id',
      'message': 'No entity version for proposal.',
      'ref': 'NVhViFxxQVCcfehbtui4Rg',
    }]
  if entity_version['status'] in ('accepted', 'declined'):
    return [{
      'name': 'replies_to_id',
      'message': 'Proposal is already complete.',
      'ref': 'ute0nhymRXORNxHxRDF9eA',
    }]
  return []


def insert_post(db_conn, data):
  """
  Create a new post.
  """

  schema = post_schema
  query = """
    INSERT INTO posts
    (  user_id  ,   topic_id  ,   kind  ,   body  ,   replies_to_id  )
    VALUES
    (%(user_id)s, %(topic_id)s, %(kind)s, %(body)s, %(replies_to_id)s)
    RETURNING *;
  """
  data = {
    'user_id': convert_slug_to_uuid(data['user_id']),
    'topic_id': convert_slug_to_uuid(data['topic_id']),
    'kind': 'post',
    'body': data.get('body'),
    'replies_to_id': data.get('replies_to_id') or None,
  }
  errors = is_valid_reply(db_conn, data)
  if errors:
    return None, errors
  data, errors = insert_row(db_conn, schema, query, data)
  if not errors:
    add_post_to_es(db_conn, data)
  return data, errors


def insert_proposal(db_conn, data):
  """
  Create a new proposal.
  """

  schema = proposal_schema
  query = """
    INSERT INTO posts
    (  user_id  ,   topic_id  ,   kind  ,   body  ,
       replies_to_id  ,   entity_versions  )
    VALUES
    (%(user_id)s, %(topic_id)s, %(kind)s, %(body)s,
     %(replies_to_id)s, %(entity_versions)s)
    RETURNING *;
  """
  data = {
    'user_id': convert_slug_to_uuid(data['user_id']),
    'topic_id': convert_slug_to_uuid(data['topic_id']),
    'kind': 'proposal',
    'body': data.get('body'),
    'replies_to_id': data.get('replies_to_id'),
    'entity_versions': data['entity_versions'],
  }
  errors = is_valid_reply(db_conn, data)
  if errors:
    return None, errors
  errors = validate_entity_versions(db_conn, data)
  if errors:
    return None, errors
  data, errors = insert_row(db_conn, schema, query, data)
  if not errors:
    add_post_to_es(db_conn, data)
  return data, errors


def insert_vote(db_conn, data):
  """
  Create a new vote.
  """

  schema = vote_schema
  query = """
    INSERT INTO posts
    (  user_id  ,   topic_id  ,   kind  ,   body  ,
       replies_to_id  ,   response  )
    VALUES
    (%(user_id)s, %(topic_id)s, %(kind)s, %(body)s,
     %(replies_to_id)s, %(response)s)
    RETURNING *;
  """
  data = {
    'user_id': convert_slug_to_uuid(data['user_id']),
    'topic_id': convert_slug_to_uuid(data['topic_id']),
    'kind': 'vote',
    'body': data.get('body'),
    'replies_to_id': data.get('replies_to_id'),
    'response': data['response'],
  }
  errors = is_valid_reply(db_conn, data)
  if errors:
    return None, errors
  errors = is_valid_reply_kind(db_conn, data)
  if errors:
    return None, errors
  data, errors = insert_row(db_conn, schema, query, data)
  if not errors:
    add_post_to_es(db_conn, data)
  return data, errors


def update_post(db_conn, prev_data, data):
  """
  Update an existing post.
  """

  schema = post_schema
  query = """
    UPDATE posts
    SET body = %(body)s
    WHERE id = %(id)s AND kind = 'post'
    RETURNING *;
  """
  data = {
    'id': convert_slug_to_uuid(prev_data['id']),
    'body': data.get('body') or prev_data.get('body'),
  }
  data, errors = update_row(db_conn, schema, query, prev_data, data)
  if not errors:
    add_post_to_es(db_conn, data)
  return data, errors


def update_proposal(db_conn, prev_data, data):
  """
  Update an existing proposal.
  """

  schema = proposal_schema
  query = """
    UPDATE posts
    SET body = %(body)s
    WHERE id = %(id)s AND kind = 'proposal'
    RETURNING *;
  """
  data = {
    'id': convert_slug_to_uuid(prev_data['id']),
    'body': data.get('body') or prev_data.get('body'),
  }
  data, errors = update_row(db_conn, schema, query, prev_data, data)
  if not errors:
    add_post_to_es(db_conn, data)
  return data, errors


def update_vote(db_conn, prev_data, data):
  """
  Update an existing vote.
  """

  schema = vote_schema
  query = """
    UPDATE posts
    SET body = %(body)s, response = %(response)s
    WHERE id = %(id)s AND kind = 'vote'
    RETURNING *;
  """
  data = {
    'id': convert_slug_to_uuid(prev_data['id']),
    'body': data.get('body') or prev_data.get('body'),
    'response': (data['response']
                 if data['response'] is not None
                 else prev_data['response']),
  }
  data, errors = update_row(db_conn, schema, query, prev_data, data)
  if not errors:
    add_post_to_es(db_conn, data)
  return data, errors


def get_post(db_conn, params):
  """
  Get the post matching the parameters.
  """

  query = """
    SELECT *
    FROM posts
    WHERE id = %(id)s
    LIMIT 1;
  """
  params = {
    'id': convert_slug_to_uuid(params['id']),
  }
  return get_row(db_conn, query, params)


def list_posts_by_topic(db_conn, params):
  """
  Get a list of posts in Sagefy.
  """

  query = """
    SELECT *
    FROM posts
    WHERE topic_id = %(topic_id)s
    ORDER BY created ASC
    OFFSET %(offset)s
    LIMIT %(limit)s;
  """
  params = {
    'topic_id': convert_slug_to_uuid(params['topic_id']),
    'offset': params.get('offset') or 0,
    'limit': params.get('limit') or 10,
  }
  return list_rows(db_conn, query, params)


def list_posts_by_user(db_conn, params):
  """
  Get a list of posts in Sagefy.
  """

  query = """
    SELECT *
    FROM posts
    WHERE user_id = %(user_id)s
    ORDER BY created ASC;
    /* TODO OFFSET LIMIT */
  """
  params = pick(params, ('user_id',))
  return list_rows(db_conn, query, params)


def deliver_post(data, access=None):
  """
  Prepare post data for JSON response.
  """

  schema = get_post_schema(data)
  return deliver_fields(schema, data, access)


def add_post_to_es(db_conn, post):
  """
  Upsert the post data into elasticsearch.
  """

  from database.topic import get_topic, deliver_topic
  from database.user import get_user, deliver_user

  data = json_prep(deliver_post(post))
  topic = get_topic(db_conn, {'id': post['topic_id']})
  if topic:
    data['topic'] = json_prep(deliver_topic(topic))
  user = get_user(db_conn, {'id': post['user_id']})
  if user:
    data['user'] = json_prep(deliver_user(user))

  return es.index(
    index='entity',
    doc_type='post',
    body=data,
    id=convert_uuid_to_slug(post['id']),
  )


def list_votes_by_proposal(db_conn, proposal_id):
  """
  List votes for a given proposal.
  """

  query = """
    SELECT *
    FROM posts
    WHERE kind = 'vote' AND replies_to_id = %(proposal_id)s
    ORDER BY created DESC;
    /* TODO OFFSET LIMIT */
  """
  params = {
    'proposal_id': convert_slug_to_uuid(proposal_id),
  }
  return list_rows(db_conn, query, params)
