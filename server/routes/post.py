from modules.content import get as c
from database.user import get_user, get_avatar
from database.entity_base import get_latest_accepted
from database.entity_facade import deliver_entity_by_kind
from framework.routes import get, post, put, abort
from framework.session import get_current_user
from modules.util import pick, omit
from database.follow import insert_follow
from database.topic import get_topic, deliver_topic
from database.post import deliver_post, validate_post, insert_post, \
    list_posts, get_post, update_post
from modules.util import prefix_error_names


@get('/s/topics/{topic_id}/posts')
def get_posts_route(request, topic_id):
    """
    Get a reverse chronological listing of posts for given topic.
    Includes topic meta data and posts (or proposals or votes).
    Paginates.
    """

    db_conn = request['db_conn']

    # Is the topic valid?
    topic = get_topic({'id': topic_id}, db_conn)
    if not topic:
        return 404, {
            'errors': [{
                'name': 'topic_id',
                'message': c('no_topic'),
            }],
            'ref': 'pgnNbqSP1VUWkOYq8MVGPrSS',
        }

    # Pull the entity
    entity_kind = topic['entity']['kind']
    entity = get_latest_accepted('%ss' % entity_kind,
                                 db_conn,
                                 topic['entity']['id'])

    # Pull all kinds of posts
    posts = list_posts({
        'limit': request['params'].get('limit') or 10,
        'skip': request['params'].get('skip') or 0,
        'topic_id': topic_id,
    }, db_conn)

    # For proposals, pull up the proposal entity version
    # ...then pull up the previous version
    # ...make a diff between the previous and the proposal entity version
    # diffs = {}
    # entity_versions = {}
    # for post_ in posts:
    #     if post_['kind'] == 'proposal':
    #         entity_versions[post_['id']] = [get_version(
    #             db_conn,
    #             '%ss' % p_entity_version['kind'],
    #             p_entity_version['id']
    #         ) for p_entity_version in post_['entity_versions']]
    #         # TODO-2 re-enable diffs
    #         # previous_version = get_version(
    #         #     db_conn,
    #         #     '%ss' % p_entity_version['kind'],
    #         #     entity_version['previous_id']
    #         # )
    #         # if previous_version:
    #         #     diffs[post_['id']] = object_diff(deliver previous_version,
    #         #                                      deliver entity_version)

    # TODO-2 SPLITUP create new endpoint for this instead
    users = {}
    for post_ in posts:
        user_id = post_['user_id']
        if user_id not in users:
            user = get_user({'id': user_id}, db_conn)
            if user:
                users[user_id] = {
                    'name': user['name'],
                    'avatar': get_avatar(user['email'], 48),
                }

    # TODO-2 SPLITUP create new endpoints for these instead
    output = {
        'topic': deliver_topic(topic),
        'posts': [deliver_post(p) for p in posts],
        # 'entity_versions': {
        #     p: [deliver_x(ev, 'view') for ev in evs]
        #     for p, evs in entity_versions.items()
        # },
        # 'diffs': diffs,  TODO-2 this causes a circular dependency
        'users': users,
    }
    if entity:
        output[entity_kind] = deliver_entity_by_kind(entity_kind, entity)
    return 200, output


@post('/s/topics/{topic_id}/posts')
def create_post_route(request, topic_id):
    """
    Create a new post on a given topic.
    Proposal: must include entity (card, unit, or subject) information.
    Vote: must refer to a valid proposal.
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

    # ## STEP 1) Create post (and entity) instances
    post_data = request['params'].get('post')
    if not post_data:
        return 400, {
            'errors': [{
                'name': 'post',
                'message': 'Missing post data.',
            }],
            'ref': 'ykQpZwJKq54MTCxgkx0p6baW'
        }
    post_data = omit(post_data, ('id', 'created', 'modified',))
    post_data['user_id'] = current_user['id']
    post_data['topic_id'] = topic_id
    # post_kind = post_data['kind']
    # if post_kind == 'proposal':
    #     entities = instance_entities(request['params'])
    #     post_data['entity_versions'] = []
    #     for entity in entities:
    #         entity_kind = get_kind(entity)
    #         post_data['entity_versions'].push({
    #             'id': entity['id'],
    #             'kind': entity_kind,
    #         })

    # ## STEP 2) Validate post (and entity) instances
    _, post_errors = validate_post(post_data, db_conn)
    errors = prefix_error_names('post.', post_errors)
    # if post_kind == 'proposal':
    #     for entity in entities:
    #         errors = (errors +
    #                   prefix_error_names('entity.', validate_x(
    #                       entity,
    #                       db_conn)))

    if len(errors):
        return 400, {
            'errors': errors,
            'ref': 'tux33ztgFj9ittSpS7WKIkq7'
        }

    # ## STEP 3) Save post (and entity)
    post_, post_errors = insert_post(post_data, db_conn)
    # if post_kind == 'proposal':
    #     for entity in entities:
    #         save_x(entity, db_conn)

    # ## STEP 4) Add author as a follower
    insert_follow({
        'user_id': current_user['id'],
        'entity': {
            'id': topic['id'],
            'kind': 'topic',
        }
    }, db_conn)
    # TODO-2 also follow the entity

    # ## STEP 5) Make updates based on proposal / vote status
    # if post_kind == 'proposal':
    #     update_entity_statuses(db_conn, post_)
    # if post_kind == 'vote':
    #     proposal = get_post({'id': post_data['replies_to_id']}, db_conn)
    #     update_entity_statuses(db_conn, proposal)

    # ## STEP 6) Send notices
    # if post_kind == 'proposal':
    #     send_notices(
    #         db_conn,
    #         entity_id=topic['entity']['id'],
    #         entity_kind=topic['entity']['kind'],
    #         notice_kind='create_proposal',
    #         notice_data={
    #             'user_name': current_user['name'],
    #             'topic_name': topic['name'],
    #             'entity_kind': topic['entity']['kind'],
    #             'entity_name': topic['entity']['id'],
    #         }
    #     )

    # ## STEP 7) Return response
    return 200, {'post': deliver_post(post_data)}


@put('/s/topics/{topic_id}/posts/{post_id}')
def update_post_route(request, topic_id, post_id):
    """
    Update an existing post. Must be one's own post.

    For post:
    - Only the body field may be changed.

    For proposals:
    - Only the name, body, and status fields can be changed.
    - The status can only be changed to declined, and only when
      the current status is pending or blocked.

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

    # ## STEP 2) Limit the scope of changes ## #
    post_data = request['params']['post']
    if post_kind is 'post':
        post_data = pick(post_data, ('body',))
    elif post_kind is 'proposal':
        post_data = pick(post_data, ('name', 'body', 'status',))
        if (post_data.get('status') != 'declined' or
                post_.get('status') not in ('pending', 'blocked',)):
            del post_data['status']
    elif post_kind is 'vote':
        post_data = pick(post_data, ('body', 'response',))

    # ## STEP 3) Validate and save post instance ## #
    post_, errors = update_post(post_, post_data, db_conn)
    if errors:
        errors = prefix_error_names('post.', errors)
        return 400, {
            'errors': errors,
            'ref': 'E4LFwRv2WEJZks7use7TCpww'
        }

    # ## STEP 4) Make updates based on proposal / vote status ## #
    # if post_kind == 'proposal':
    #     update_entity_statuses(db_conn, post_)
    # if post_kind == 'vote':
    #     proposal = get_post({'id': post_['replies_to_id']}, db_conn)
    #     update_entity_statuses(db_conn, proposal)

    # ## STEP 5) Return response ## #
    return 200, {'post': deliver_post(post_)}
