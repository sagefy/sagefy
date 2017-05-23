"""
Routes for the discussion platform.
Includes topics.
"""

# TODO-3 what checks should be moved to models?
# TODO-2 perhaps, these endpoints are too large
#        can they be split up while maintaining guarantees?

from framework.routes import post, put, abort
from framework.session import get_current_user
from modules.util import pick, omit
from modules.notices import send_notices
from database.follow import insert_follow
from database.topic import get_topic, deliver_topic, validate_topic, \
    update_topic, insert_topic
from database.post import deliver_post, validate_post, insert_post
from modules.util import prefix_error_names


@post('/s/topics')
def create_topic_route(request):
    """
    Create a new topic.
    The first post (or proposal) must be provided.
    """

    db_conn = request['db_conn']

    current_user = get_current_user(request)
    if not current_user:
        return abort(401)

    # ## STEP 1) Create post and topic (and entity) instances
    topic_data = request['params'].get('topic')
    post_data = request['params'].get('post')
    if not topic_data:
        return 400, {
            'errors': [{
                'name': 'topic',
                'message': 'Missing topic data.'
            }],
            'ref': 'zknSd46f2hRNjSjVHCg6YLwN'
        }
    if not post_data:
        return 400, {
            'errors': [{
                'name': 'post',
                'message': 'Missing post data.'
            }],
            'ref': 'Qki4oWX4nTdNAjYI8z5iNawr'
        }
    topic_data = omit(topic_data, ('id', 'created', 'modified'))
    topic_data['user_id'] = current_user['id']
    topic_data, topic_errors = validate_topic(topic_data, db_conn)

    post_data = omit(post_data, ('id', 'created', 'modified',))
    post_data['user_id'] = current_user['id']
    post_data['topic_id'] = topic_data['id']
    # post_kind = post_data['kind']
    # if post_kind == 'proposal':
    #     entities = instance_entities(request['params'])
    #     post_data['entity_versions'] = []
    #     for entity in entities:
    #         entity_kind = get_kind(entity)
    #         post_data['entity_versions'].append({
    #             'id': entity['id'],
    #             'kind': entity_kind,
    #         })

    # ## STEP 2) Validate post and topic (and entity) instances
    errors = prefix_error_names('topic.', topic_errors)
    _, post_errors = validate_post(post_data, db_conn)
    errors = errors + prefix_error_names('post.', post_errors)
    # if post_kind == 'proposal':
    #     for entity in entities:
    #         errors = (errors +
    #                   prefix_error_names(
    #                       'entity.',
    #                       validate_x(entity, db_conn)))
    if len(errors):
        return 400, {
            'errors': errors,
            'ref': 'TAY5pX3ghWBkSIVGTHzpQySa'
        }

    # ## STEP 3) Save post and topic (and entity)
    topic_data, topic_errors = insert_topic(topic_data, db_conn)
    post_data['topic_id'] = topic_data['id']
    post_, errors = insert_post(post_data, db_conn)
    # if post_kind == 'proposal':
    #     for entity in entities:
    #         save_x(entity, db_conn)

    # ## STEP 4) Add author as a follower
    insert_follow({
        'user_id': current_user['id'],
        'entity': {
            'id': topic_data['id'],
            'kind': 'topic',
        }
    }, db_conn)
    # TODO-2 also follow the entity automatically IF needed

    # ## STEP 5) Send out any needed notices
    send_notices(
        db_conn,
        entity_id=topic_data['entity']['id'],
        entity_kind=topic_data['entity']['kind'],
        notice_kind='create_topic',
        notice_data={
            'user_name': current_user['name'],
            'topic_name': topic_data['name'],
            'entity_kind': topic_data['entity']['kind'],
            'entity_name': topic_data['entity']['id'],
        }
    )

    # if post_kind == 'proposal':
    #     send_notices(
    #         db_conn,
    #         entity_id=topic_data['entity']['id'],
    #         entity_kind=topic_data['entity']['kind'],
    #         notice_kind='create_proposal',
    #         notice_data={
    #             'user_name': current_user['name'],
    #             'topic_name': topic_data['name'],
    #             'entity_kind': topic_data['entity']['kind'],
    #             'entity_name': topic_data['entity']['id'],
    #         }
    #     )

    # ## STEP 5) Return response
    return 200, {
        'topic': deliver_topic(topic_data),
        'post': deliver_post(post_),
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
        return abort(401)

    # ## STEP 1) Find existing topic instance ## #
    topic = get_topic({'id': topic_id}, db_conn)
    if not topic:
        return abort(404)
    if topic['user_id'] != current_user['id']:
        return abort(403)

    # ## STEP 2) Limit the scope of changes ## #
    topic_data = request['params']['topic']
    topic_data = pick(topic_data, ('name',))

    # ## STEP 3) Validate and save topic instance ## #
    topic, errors = update_topic(topic, topic_data, db_conn)
    if errors:
        errors = prefix_error_names('topic.', errors)
        return 400, {
            'errors': errors,
            'ref': 'k7ItNedf0I0vXfiIUcDtvHgQ',
        }

    # ## STEP 4) Return response ## #
    return 200, {'topic': deliver_topic(topic)}
