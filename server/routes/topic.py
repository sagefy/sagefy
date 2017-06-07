"""
Routes for the discussion platform.
Includes topics.
"""

from framework.routes import get, post, put, abort
from framework.session import get_current_user
from modules.notices import send_notices
from database.follow import insert_follow
from database.topic import get_topic, deliver_topic, \
    update_topic, insert_topic, list_topics_by_entity_id
from modules.content import get as c


@get('/s/topics/{topic_id}')
def get_topic_route(request, topic_id):
    """
    Get a topic
    """

    db_conn = request['db_conn']
    topic = get_topic({'id': topic_id}, db_conn)
    if not topic:
        return 404, {
            'errors': [{
                'name': 'topic_id',
                'message': c('no_topic'),
            }],
            'ref': 'lWX0Scbdx5y8YcHA7wm7Jfm4',
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
        topics = list_topics_by_entity_id(entity_id, {}, db_conn)
        return 200, {'topics': [
            deliver_topic(topic)
            for topic in topics
        ]}
    else:
        return abort(404)


@post('/s/topics')
def create_topic_route(request):
    """
    Create a new topic.
    """

    db_conn = request['db_conn']
    current_user = get_current_user(request)
    if not current_user:
        return abort(401)

    # ## STEP 1) Create topic
    topic_data = request['params']
    if not topic_data:
        return 400, {
            'errors': [{
                'name': 'topic',
                'message': 'Missing topic data.'
            }],
            'ref': 'zknSd46f2hRNjSjVHCg6YLwN'
        }
    topic_data['user_id'] = current_user['id']
    topic, errors = insert_topic(topic_data, db_conn)
    if len(errors):
        return 400, {
            'errors': errors,
            'ref': 'TAY5pX3ghWBkSIVGTHzpQySa'
        }

    # ## STEP 2) Add author as a follower
    insert_follow({
        'user_id': current_user['id'],
        'entity': {
            'id': topic['id'],
            'kind': 'topic',
        }
    }, db_conn)
    # TODO-2 also follow the entity automatically IF needed

    # ## STEP 3) Send out any needed notices
    send_notices(
        db_conn,
        entity_id=topic['entity']['id'],
        entity_kind=topic['entity']['kind'],
        notice_kind='create_topic',
        notice_data={
            'user_name': current_user['name'],
            'topic_name': topic['name'],
            'entity_kind': topic['entity']['kind'],
            'entity_name': topic['entity']['id'],
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
        return abort(401)

    # ## STEP 1) Find existing topic instance ## #
    topic = get_topic({'id': topic_id}, db_conn)
    if not topic:
        return abort(404)
    if topic['user_id'] != current_user['id']:
        return abort(403)

    # ## STEP 2) Validate and save topic instance ## #
    topic_data = request['params']
    topic, errors = update_topic(topic, topic_data, db_conn)
    if errors:
        return 400, {
            'errors': errors,
            'ref': 'k7ItNedf0I0vXfiIUcDtvHgQ',
        }

    # ## STEP 3) Return response ## #
    return 200, {'topic': deliver_topic(topic)}
