from modules.content import get as c
from framework.routes import get, post, put, abort
from framework.session import get_current_user
from database.follow import insert_follow
from database.topic import get_topic
from database.post import deliver_post, insert_post, \
    list_posts, get_post, update_post
from database.entity_facade import update_entity_statuses
from modules.notices import send_notices
from copy import deepcopy


# TODO-2 re-enable diffs see object_diff

@get('/s/topics/{topic_id}/posts')
def get_posts_route(request, topic_id):
    """
    Get a reverse chronological listing of posts for given topic.
    Includes topic meta data and posts (or proposals or votes).
    Paginates.
    """

    db_conn = request['db_conn']
    topic = get_topic({'id': topic_id}, db_conn)
    if not topic:
        return 404, {
            'errors': [{
                'name': 'topic_id',
                'message': c('no_topic'),
            }],
            'ref': 'pgnNbqSP1VUWkOYq8MVGPrSS',
        }
    posts = list_posts({
        'limit': request['params'].get('limit') or 10,
        'skip': request['params'].get('skip') or 0,
        'topic_id': topic_id,
    }, db_conn)
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
        return abort(401)
    topic = get_topic({'id': topic_id}, db_conn)
    if not topic:
        return 404, {
            'errors': [{
                'name': 'topic_id',
                'message': c('no_topic'),
            }],
            'ref': 'PCSFCxsJtnlP0x9WzbPoKcwM',
        }

    # ## STEP 1) Create post
    post_data = deepcopy(request['params'])
    if not post_data:
        return 400, {
            'errors': [{
                'name': 'post',
                'message': 'Missing post data.',
            }],
            'ref': 'ykQpZwJKq54MTCxgkx0p6baW'
        }
    post_data['user_id'] = current_user['id']
    post_data['topic_id'] = topic_id
    post_kind = post_data.get('kind')

    # ## STEP 2) Validate and save post
    post_, post_errors = insert_post(post_data, db_conn)
    if len(post_errors):
        return 400, {
            'errors': post_errors,
            'ref': 'tux33ztgFj9ittSpS7WKIkq7'
        }

    # ## STEP 3) Add author as a follower
    insert_follow({
        'user_id': current_user['id'],
        'entity': {
            'id': topic['id'],
            'kind': 'topic',
        }
    }, db_conn)
    # TODO-2 also follow the entity

    # ## STEP 4) Send notices
    send_notices(
        db_conn,
        entity_id=topic['entity']['id'],
        entity_kind=topic['entity']['kind'],
        notice_kind='create_{kind}'.format(kind=post_['kind']),
        notice_data={
            'user_name': current_user['name'],
            'topic_name': topic['name'],
            'entity_kind': topic['entity']['kind'],
            'entity_name': topic['entity']['id'],
        }
    )

    # ## STEP 5) Make updates based on proposal / vote status
    if post_kind == 'proposal':
        update_entity_statuses(db_conn, post_)
    if post_kind == 'vote':
        proposal = get_post({'id': post_['replies_to_id']}, db_conn)
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
        return abort(401)

    # ## STEP 1) Find existing post instance ## #
    post_ = get_post({'id': post_id}, db_conn)
    if not post_:
        return abort(404)
    if post_['user_id'] != current_user['id']:
        return abort(403)
    post_kind = post_['kind']

    # ## STEP 2) Validate and save post instance ## #
    post_data = request['params']
    post_, errors = update_post(post_, post_data, db_conn)
    if errors:
        return 400, {
            'errors': errors,
            'ref': 'E4LFwRv2WEJZks7use7TCpww'
        }

    # ## STEP 3) Make updates based on proposal / vote status ## #
    if post_kind == 'proposal':
        update_entity_statuses(db_conn, post_)
    if post_kind == 'vote':
        proposal = get_post({'id': post_['replies_to_id']}, db_conn)
        update_entity_statuses(db_conn, proposal)

    # ## STEP 4) Return response ## #
    return 200, {'post': deliver_post(post_)}
