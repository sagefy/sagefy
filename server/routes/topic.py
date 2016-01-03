"""
Routes for the discussion platform.
Includes topics, posts, proposals, and votes.
"""

# TODO-3 what checks should be moved to models?
# TODO-0 test plan doesn't generate any notices

from framework.routes import get, post, put, abort
from framework.session import get_current_user
from modules.discuss import instance_post_facade, \
    get_post_facade, get_posts_facade
from modules.util import pick, omit, object_diff
from modules.entity import get_kind, get_latest_accepted, get_version, \
    instance_new_entity
from models.topic import Topic
from models.user import User
from models.proposal import Proposal
from models.vote import Vote
from modules.content import get as c
from modules.notices import send_notices


def prefix_error_names(prefix, errors):
    for error in errors:
        error['name'] = prefix + error['name']
    return errors


def update_entity_status(proposal):
    """
    Update the entity's status based on the vote power received.
    Move to accepted or blocked if qualified.
    TODO-2 Update this to work as described in:
        https://github.com/heiskr/sagefy/wiki/Planning%3A-Contributor-Ratings
        This requires knowing two things:
        - Number of learners the entity impacts
        - The vote and proposal history of the contributor
    """

    # Get the entity version
    entity_version = get_version(proposal['entity_version']['kind'],
                                 proposal['entity_version']['id'])

    # Make sure the entity version status is not declined or accepted
    if entity_version['status'] in ('accepted', 'declined'):
        return

    # Count the "no" and "yes" vote power
    no_vote_power = 0
    yes_vote_power = 1
    # For now, we will assume the proposer is one "yes" vote until
    # contributor vote power is calculated
    votes = Vote.list(replies_to_id=proposal['id'])
    for vote in votes:
        if vote['response']:
            yes_vote_power = yes_vote_power + 1
        else:
            no_vote_power = no_vote_power + 1

    # If no power is great enough, then block the version
    if no_vote_power >= 1:
        entity_version['status'] = 'blocked'
        entity_version.save()
        send_notices(
            entity_id=proposal['entity_version']['id'],
            entity_kind=proposal['entity_version']['kind'],
            notice_kind='block_proposal',
            notice_data={
                'user_name': '???',  # TODO-2
                'proposal_name': proposal['name'],
                'entity_kind': proposal['entity_version']['kind'],
                'entity_name': entity_version['name'],
            }
        )

    # If yes power is great enough, then accept the version
    if yes_vote_power >= 3:
        entity_version['status'] = 'accepted'
        entity_version.save()
        send_notices(
            entity_id=proposal['entity_version']['id'],
            entity_kind=proposal['entity_version']['kind'],
            notice_kind='accept_proposal',
            notice_data={
                'proposal_name': proposal['name'],
                'entity_kind': proposal['entity_version']['kind'],
                'entity_name': entity_version['name'],
            }
        )


@post('/s/topics')
def create_topic_route(request):
    """
    Create a new topic.
    The first post (or proposal) must be provided.
    """

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
    topic = Topic(topic_data)
    post_data = omit(post_data, ('id', 'created', 'modified',))
    post_data['user_id'] = current_user['id']
    post_data['topic_id'] = topic['id']
    post_ = instance_post_facade(post_data)
    post_kind = post_['kind']
    if post_kind == 'proposal':
        entity = instance_new_entity(request['params'])
        entity_kind = get_kind(request['params'])
        post_['entity_version'] = {
            'id': entity['id'],
            'kind': entity_kind,
        }

    # ## STEP 2) Validate post and topic (and entity) instances
    errors = prefix_error_names('topic.', topic.validate())
    errors = errors + prefix_error_names('post.', post_.validate())
    if post_kind == 'proposal':
        errors = errors + prefix_error_names('entity.', entity.validate())
    if len(errors):
        return 400, {
            'errors': errors,
            'ref': 'TAY5pX3ghWBkSIVGTHzpQySa'
        }

    # ## STEP 3) Save post and topic (and entity)
    topic.save()
    post_.save()
    if post_kind == 'proposal':
        entity.save()

    # ## STEP 4) Send out any needed notifications
    send_notices(
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

    # ## STEP 5) Return response
    return 200, {'topic': topic.deliver(), 'post': post_.deliver()}


@put('/s/topics/{topic_id}')
def update_topic_route(request, topic_id):
    """
    Update the topic.
    - Only the name can be changed.
    - Only by original author.
    """

    current_user = get_current_user(request)
    if not current_user:
        return abort(401)

    # ## STEP 1) Find existing topic instance ## #
    topic = Topic.get(id=topic_id)
    if not topic:
        return abort(404)
    if topic['user_id'] != current_user['id']:
        return abort(403)

    # ## STEP 2) Limit the scope of changes ## #
    topic_data = request['params']['topic']
    topic_data = pick(topic_data, ('name',))

    # ## STEP 3) Validate and save topic instance ## #
    topic, errors = topic.update(topic_data)
    if errors:
        errors = prefix_error_names('topic.', errors)
        return 400, {
            'errors': errors,
            'ref': 'k7ItNedf0I0vXfiIUcDtvHgQ',
        }

    # ## STEP 4) Return response ## #
    return 200, {'topic': topic.deliver()}


@get('/s/topics/{topic_id}/posts')
def get_posts_route(request, topic_id):
    """
    Get a reverse chronological listing of posts for given topic.
    Includes topic meta data and posts (or proposals or votes).
    Paginates.
    """

    # Is the topic valid?
    topic = Topic.get(id=topic_id)
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
    entity = get_latest_accepted(entity_kind,
                                 topic['entity']['id'])

    # Pull all kinds of posts
    posts = get_posts_facade(
        limit=request['params'].get('limit') or 10,
        skip=request['params'].get('skip') or 0,
        topic_id=topic_id
    )

    # For proposals, pull up the proposal entity version
    # ...then pull up the previous version
    # ...make a diff between the previous and the proposal entity version
    diffs = {}
    entity_versions = {}
    for post_ in posts:
        if post_['kind'] == 'proposal':
            entity_version = entity_versions[post_['id']] = get_version(
                post_['entity_version']['kind'],
                post_['entity_version']['id']
            )
            previous_version = get_version(
                post_['entity_version']['kind'],
                entity_version['previous_id']
            )
            if previous_version:
                diffs[post_['id']] = object_diff(previous_version.deliver(),
                                                 entity_version.deliver())

    # TODO-2 SPLITUP create new endpoint for this instead
    users = {}
    for post_ in posts:
        user_id = post_['user_id']
        if user_id not in users:
            user = User.get(id=user_id)
            if user:
                users[user_id] = {
                    'name': user['name'],
                    'avatar': user.get_avatar(48)
                }

    # TODO-2 SPLITUP create new endpoints for these instead
    output = {
        'topic': topic.deliver(),
        'posts': [p.deliver() for p in posts],
        'entity_versions': {
            p: ev.deliver()
            for p, ev in entity_versions.items()
        },
        'diffs': diffs,
        'users': users,
    }
    if entity:
        output[entity_kind] = entity.deliver()
    return 200, output


@post('/s/topics/{topic_id}/posts')
def create_post_route(request, topic_id):
    """
    Create a new post on a given topic.
    Proposal: must include entity (card, unit, or set) information.
    Vote: must refer to a valid proposal.
    """

    current_user = get_current_user(request)
    if not current_user:
        return abort(401)

    topic = Topic.get(id=topic_id)
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
    post_ = instance_post_facade(post_data)
    post_kind = post_['kind']
    if post_kind == 'proposal':
        entity = instance_new_entity(request['params'])
        entity_kind = get_kind(request['params'])
        post_['entity_version'] = {
            'id': entity['id'],
            'kind': entity_kind,
        }

    # ## STEP 2) Validate post (and entity) instances
    errors = prefix_error_names('post.', post_.validate())
    if post_kind == 'proposal':
        errors = errors + prefix_error_names('entity.', entity.validate())
    if len(errors):
        return 400, {
            'errors': errors,
            'ref': 'tux33ztgFj9ittSpS7WKIkq7'
        }

    # ## STEP 3) Save post (and entity)
    post_.save()
    if post_kind == 'proposal':
        entity.save()

    # ## STEP 4) Make updates based on proposal / vote status
    if post_kind == 'proposal':
        update_entity_status(post_)
    if post_kind == 'vote':
        proposal = Proposal.get(id=post_['replies_to_id'])
        update_entity_status(proposal)

    # ## STEP 5) Return response
    return 200, {'post': post_.deliver()}


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

    current_user = get_current_user(request)
    if not current_user:
        return abort(401)

    # ## STEP 1) Find existing post instance ## #
    post_ = get_post_facade(post_id)
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
                post_data.get('status') not in ('pending', 'blocked',)):
            del post_data['status']
    elif post_kind is 'vote':
        post_data = pick(post_data, ('body', 'response',))

    # ## STEP 3) Validate and save post instance ## #
    post_, errors = post_.update(post_data)
    if errors:
        errors = prefix_error_names('post.', errors)
        return 400, {
            'errors': errors,
            'ref': 'E4LFwRv2WEJZks7use7TCpww'
        }

    # ## STEP 4) Make updates based on proposal / vote status ## #
    if post_kind == 'proposal':
        update_entity_status(post_)
    if post_kind == 'vote':
        proposal = Proposal.get(id=post_['replies_to_id'])
        update_entity_status(proposal)

    # ## STEP 5) Return response ## #
    return 200, {'post': post_.deliver()}
