"""
Routes for the discussion platform.
Includes topics.
"""

from framework.routes import get, post, put, abort
from framework.session import get_current_user
from modules.notices import send_notices
from modules.content import get as c
from modules.util import convert_uuid_to_slug
from database.follow import insert_follow
from database.topic import get_topic, deliver_topic, \
    update_topic, insert_topic, list_topics_by_entity_id


@get('/s/topics/{topic_id}')
def get_topic_route(request, topic_id):
  """
  Get a topic
  """

  db_conn = request['db_conn']
  topic = get_topic(db_conn, {'id': topic_id})
  if not topic:
    return 404, {
      'errors': [{
        'name': 'topic_id',
        'message': c('no_topic'),
      }],
      'ref': 'o5V4uBFXQC6WNeyKrhn5kA',
    }
  return 200, {'topic': deliver_topic(topic)}


@get('/s/topics')
def list_topics_route(request):
  """
  List topics by specified parameters.
  """

  db_conn = request['db_conn']
  entity_id = request['params'].get('entity_id')
  if entity_id:
    topics = list_topics_by_entity_id(db_conn, entity_id, {})
    return 200, {'topics': [
      deliver_topic(topic)
      for topic in topics
    ]}
  return abort(404, '4ubANCBYSvCABWyqvjH62A')


@post('/s/topics')
def create_topic_route(request):
  """
  Create a new topic.
  """

  db_conn = request['db_conn']
  current_user = get_current_user(request)
  if not current_user:
    return abort(401, 'WJ50hh2STw-5ujy62wyXew')

  # ## STEP 1) Create topic
  topic_data = request['params']
  if not topic_data:
    return 400, {
      'errors': [{
        'name': 'topic',
        'message': 'Missing topic data.',
        'ref': 'PmocSz4OQUGa2T7x98yVlg',
      }],
    }
  topic_data['user_id'] = current_user['id']
  topic, errors = insert_topic(db_conn, topic_data)
  if errors:
    return 400, {
      'errors': errors,
      'ref': 'UoyXf_vwSWee0tCWgxg4Zw'
    }

  # ## STEP 2) Add author as a follower
  insert_follow(db_conn, {
    'user_id': current_user['id'],
    'entity_id': topic['id'],
    'entity_kind': 'topic',
  })
  # TODO-2 also follow the entity automatically IF needed

  # ## STEP 3) Send out any needed notices
  send_notices(
    db_conn,
    entity_id=topic['entity_id'],
    entity_kind=topic['entity_kind'],
    notice_kind='create_topic',
    notice_data={
      'user_name': current_user['name'],
      'topic_name': topic['name'],
      'entity_kind': topic['entity_kind'],
      'entity_name': convert_uuid_to_slug(topic['entity_id']),
    }
  )

  # ## STEP 4) Return response
  return 200, {
    'topic': deliver_topic(topic),
  }


@put('/s/topics/{topic_id}')
def update_topic_route(request, topic_id):
  """
  Update the topic.
  - Only the name can be changed.
  - Only by original author.
  """

  db_conn = request['db_conn']
  current_user = get_current_user(request)
  if not current_user:
    return abort(401, 'ZUiN62FFR3OcBM6s8UJSmg')

  # ## STEP 1) Find existing topic instance ## #
  topic = get_topic(db_conn, {'id': topic_id})
  if not topic:
    return abort(404, 'MXzNqBU6SN28tNtRXW9rNw')
  if topic['user_id'] != current_user['id']:
    return abort(403, 'MZZbJNt3RK-4kVMo2rROWA')

  # ## STEP 2) Validate and save topic instance ## #
  topic_data = request['params']
  topic, errors = update_topic(db_conn, topic, topic_data)
  if errors:
    return 400, {
      'errors': errors,
      'ref': 'zu7VABcJT5qCzF7BHNCH5w',
    }

  # ## STEP 3) Return response ## #
  return 200, {'topic': deliver_topic(topic)}
