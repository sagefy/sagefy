from copy import deepcopy

from framework.routes import get, post, put, abort
from framework.session import get_current_user
from database.follow import insert_follow
from database.topic import get_topic
from database.post import deliver_post, insert_post, \
    list_posts_by_topic, get_post, update_post, insert_proposal, \
    insert_vote, update_proposal, update_vote
from database.entity_facade import update_entity_statuses
from modules.content import get as c
from modules.notices import send_notices
from modules.util import convert_uuid_to_slug

# TODO-1 remove /topics/{topic_id} from these routes.
# TODO-2 re-enable diffs see object_diff


@get('/s/topics/{topic_id}/posts')
def get_posts_route(request, topic_id):
  """
  Get a reverse chronological listing of posts for given topic.
  Includes topic meta data and posts (or proposals or votes).
  Paginates.
  """

  db_conn = request['db_conn']
  topic = get_topic(db_conn, {'id': topic_id})
  if not topic:
    return 404, {
      'errors': [{
        'name': 'topic_id',
        'message': c('no_topic'),
        'ref': 'vtnCzkc9S6Olp_l5AHsG_A',
      }],
    }
  posts = list_posts_by_topic(db_conn, {
    'limit': request['params'].get('limit'),
    'offset': request['params'].get('offset'),
    'topic_id': topic_id,
  })
  return 200, {
    'posts': [deliver_post(p) for p in posts],
  }


@post('/s/topics/{topic_id}/posts')
def create_post_route(request, topic_id):
  """
  Create a new post on a given topic.
  """

  db_conn = request['db_conn']
  current_user = get_current_user(request)
  if not current_user:
    return abort(401, 'rIRQxwqcRRSwWi2ies4YfA')
  topic = get_topic(db_conn, {'id': topic_id})
  if not topic:
    return 404, {
      'errors': [{
        'name': 'topic_id',
        'message': c('no_topic'),
        'ref': 'DRuU_wBOSaWR-SBYm0Rd2g',
      }],
    }

  # ## STEP 1) Create post
  post_data = deepcopy(request['params'])
  if not post_data:
    return 400, {
      'errors': [{
        'name': 'post',
        'message': 'Missing post data.',
        'ref': '8eKpBWShSI6jfmdXjXb5WQ',
      }],
    }
  post_data['user_id'] = current_user['id']
  post_data['topic_id'] = topic_id
  post_kind = post_data.get('kind')

  # ## STEP 2) Validate and save post
  if post_kind == 'proposal':
    post_, post_errors = insert_proposal(db_conn, post_data)
  elif post_kind == 'vote':
    post_, post_errors = insert_vote(db_conn, post_data)
  else:
    post_, post_errors = insert_post(db_conn, post_data)
  if post_errors:
    return 400, {
      'errors': post_errors,
      'ref': 'GakpqCGjS2KZhbTIBYOpVQ'
    }

  # ## STEP 3) Add author as a follower
  insert_follow(db_conn, {
    'user_id': current_user['id'],
    'entity_id': topic['id'],
    'entity_kind': 'topic',
  })
  # TODO-2 also follow the entity

  # ## STEP 4) Send notices
  send_notices(
    db_conn,
    entity_id=topic['entity_id'],
    entity_kind=topic['entity_kind'],
    notice_kind='create_{kind}'.format(kind=post_['kind']),
    notice_data={
      'user_name': current_user['name'],
      'topic_name': topic['name'],
      'entity_kind': topic['entity_kind'],
      'entity_name': convert_uuid_to_slug(topic['entity_id']),
    }
  )

  # ## STEP 5) Make updates based on proposal / vote status
  if post_kind == 'proposal':
    update_entity_statuses(db_conn, post_)
  if post_kind == 'vote':
    proposal = get_post(db_conn, {'id': post_['replies_to_id']})  # TODO-0
    update_entity_statuses(db_conn, proposal)

  # ## STEP 6) Return response
  return 200, {'post': deliver_post(post_)}


@put('/s/topics/{topic_id}/posts/{post_id}')
def update_post_route(request, topic_id, post_id):
  """
  Update an existing post. Must be one's own post.
  For post:
  - Only the body field may be changed.
  - TODO-2 For proposals, the status can only be changed to declined,
    and only when the current status is pending or blocked.
  For votes:
  - The only fields that can be updated are body and response.
  """

  db_conn = request['db_conn']
  current_user = get_current_user(request)
  if not current_user:
    return abort(401, 'RGGeXRuNTQ2lZVukUzXNNw')

  # ## STEP 1) Find existing post instance ## #
  post_ = get_post(db_conn, {'id': post_id})
  if not post_:
    return abort(404, 'HOSjVbXlSRihzU9_kRynIQ')
  if post_['user_id'] != current_user['id']:
    return abort(403, 'K8UUA1TIQLuLBNev_y2sbw')
  post_kind = post_['kind']

  # ## STEP 2) Validate and save post instance ## #
  post_data = request['params']
  if post_kind == 'proposal':
    post_, errors = update_proposal(db_conn, post_, post_data)
  elif post_kind == 'vote':
    post_, errors = update_vote(db_conn, post_, post_data)
  else:
    post_, errors = update_post(db_conn, post_, post_data)
  if errors:
    return 400, {
      'errors': errors,
      'ref': 'rBj6wR4LQH6Kxym0P0-3OA'
    }

  # ## STEP 3) Make updates based on proposal / vote status ## #
  if post_kind == 'proposal':
    update_entity_statuses(db_conn, post_)
  if post_kind == 'vote':
    proposal = get_post(db_conn, {'id': post_['replies_to_id']})  # TODO-0
    update_entity_statuses(db_conn, proposal)

  # ## STEP 4) Return response ## #
  return 200, {'post': deliver_post(post_)}
