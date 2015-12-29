"""
Routes for the discussion platform.
Includes topics, posts, proposals, and votes.
"""

from framework.routes import get, post, put, abort
from models.topic import Topic
from models.post import Post
from models.user import User
from framework.session import get_current_user
from modules.util import omit, object_diff
from modules.discuss import instance_post_facade, \
    get_post_facade, get_posts_facade
from modules.content import get as c
from modules.entity import create_entity, get_version, get_latest_accepted

# TODO most of this junk should be moved into the models and modules...
#      these methods are waaay too complicated.

# TODO send out notifications!


@post('/s/topics')
def create_topic_route(request):
    """
    Create a new topic. The first post (or proposal) must be provided.
    """

    current_user = get_current_user(request)
    if not current_user:
        return abort(401)

    if 'topic' not in request['params']:
        return 400, {
            'errors': [{
                'name': 'topic',
                'message': 'Missing topic data.'
            }],
            'ref': 'zknSd46f2hRNjSjVHCg6YLwN'
        }

    if 'post' not in request['params']:
        return 400, {
            'errors': [{
                'name': 'post',
                'message': 'Missing post data.'
            }],
            'ref': 'Qki4oWX4nTdNAjYI8z5iNawr'
        }

    # Let's create the topic, but not save it until we know we
    # have a valid post
    topic_data = dict(**request['params']['topic'])
    topic_data['user_id'] = current_user['id']
    topic = Topic(topic_data)
    post_data = dict(**request['params']['post'])
    post_data['user_id'] = current_user['id']
    post_data['topic_id'] = topic['id']
    post_ = instance_post_facade(post_data)

    errors, errors2 = topic.validate(), post_.validate()
    if errors + errors2:
        return 400, {
            'errors': errors + errors2,
            'ref': 'dr1vX0A7kE8RItHBGeObXWkZ'
        }

    # Validate topic entity is valid
    if post_['kind'] == 'proposal':
        entity, errors = create_entity(request['params'])
        if errors:
            return 400, {
                'errors': errors,
                'ref': 'TiIBxS9pPWOcIuFUF5IAUi9o'
            }

    post_, errors = post_.save()
    topic, errors2 = topic.save()
    if len(errors + errors2):
        return 400, {
            'errors': errors + errors2,
            'ref': 'hWZwyUUN8MuyPPMYi0iUwYxm'
        }

    return 200, {'topic': topic.deliver(), 'post': post_.deliver()}


@put('/s/topics/{topic_id}')
def update_topic_route(request, topic_id):
    """
    Update the topic. Only the name can be changed. Only by original author.
    """

    current_user = get_current_user(request)
    if not current_user:
        return abort(401)

    # Must be a valid topic_id
    topic = Topic.get(id=topic_id)
    if not topic:
        return 404, {
            'errors': [{
                'name': 'topic_id',
                'message': c('no_topic'),
            }],
            'ref': 'Uwn359F67hC66d66I8lkUwpE'
        }

    # Must be logged in as topic's author
    if topic['user_id'] != current_user['id']:
        return abort(403)

    # Request must only be for name
    # TODO should this be part of the model?
    topic, errors = topic.update({
        'name': request['params'].get('topic', {}).get('name')
    })
    if errors:
        return 400, {
            'errors': errors,
            'ref': 'k7ItNedf0I0vXfiIUcDtvHgQ',
        }

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
    for post_ in posts:
        if post_['type'] == 'proposal':
            kind = post_['entity_version']['kind']
            entity_version = get_version(kind,
                                         post_['entity_version']['id'])
            previous_version = get_version(kind,
                                           entity_version['previous_id'])
            diff = object_diff(previous_version.deliver(),
                               entity_version.deliver())
            diffs[post_['id']] = diff

    # TODO SPLITUP create new endpoint for this instead
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

    # TODO SPLITUP create new endpoints for these instead
    output = {
        'topic': topic.deliver(),
        'posts': [p.deliver() for p in posts],
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
    Accounts for posts, proposals, and votes.
    Proposal: must include entity (card, unit, set) information.
    Vote: must refer to a proposal.
    """

    current_user = get_current_user(request)
    if not current_user:
        return abort(401)

    # TODO what checks should be moved to the model?

    if not request['params'].get('post'):
        return 400, {
            'errors': [{
                'name': 'post',
                'message': 'Missing post data.',
            }],
            'ref': 'ykQpZwJKq54MTCxgkx0p6baW'
        }

    post_data = request['params']['post']
    kind = post_data.get('kind')

    # The topic must be valid
    topic_id = post_data.get('topic_id')
    topic = Topic.get(id=topic_id)
    if not topic_id or not topic:
        return 404, {
            'errors': [{
                'name': 'topic_id',
                'message': c('no_topic'),
            }],
            'ref': 'uTmChkRuUng5fpf8c51iVela',
        }

    # For proposal, entity must be included and valid
    if kind == 'proposal':
        entity, errors = create_entity(request['params'])
        if errors:
            return 400, {
                'errors': errors,
                'ref': 'mlTfMLy4PTdLedrWFRzrDEax'
            }

    # Try to save the post (and others)
    post_data = dict(**post_data)
    post_data['user_id'] = current_user['id']
    post_data['topic_id'] = topic['id']
    post_ = instance_post_facade(post_data)

    errors = post_.validate()
    if len(errors):
        return 400, {
            'errors': errors,
            'ref': 'tux33ztgFj9ittSpS7WKIkq7'
        }

    # If a proposal has sufficient votes, move it to accepted
    # ... and close out any prior versions dependent
    # TODO@ only allow one vote per proposal per user
    if kind == 'vote':
        proposal_id = post_['replies_to_id']
        proposal = Post.get(id=proposal_id)
        entity = get_version(proposal['entity_version']['kind'],
                             proposal['entity_version']['id'])
        entity['status'] = 'accepted'
        # TODO actually count the votes first
        # TODO block if negative response
        entity.save()

    post_.save()

    return 200, {'post': post_.deliver()}


@put('/s/topics/{topic_id}/posts/{post_id}')
def update_post_route(request, topic_id, post_id):
    """
    Update an existing post. Must be one's own post.

    For proposals:
    The only field that can be updated is the status;
    the status can only be changed to declined, and only when
    the current status is pending or blocked.

    For votes:
    The only fields that can be updated are body and response.
    """

    current_user = get_current_user(request)
    if not current_user:
        return abort(401)

    post_ = get_post_facade(post_id)
    kind = post_['kind']

    post_data = dict(**request['params']['post'])
    post_data = omit(post_data, ('id', 'user_id', 'topic_id', 'kind'))

    # Must be user's own post
    # TODO Should some of these checks be part of the model?
    if post_['user_id'] != current_user['id']:
        return abort(403)

    # If proposal, make sure its allowed changes
    if post_['kind'] == 'proposal':
        if post_data['status'] == 'declined':
            post_data = {
                'status': 'declined'
            }
        else:
            post_data = {}

    # If vote, make sure its allowed changes
    if post_['kind'] == 'vote':
        post_data = {
            'body': post_data['body'],
            'response': post_data['response'],
        }

    post_, errors = post_.update(post_data)
    if errors:
        return 400, {
            'errors': errors,
            'ref': 'E4LFwRv2WEJZks7use7TCpww'
        }

    # If a proposal has sufficient votes, move it to accepted
    # ... and close out any prior versions dependent
    if kind == 'vote':
        proposal_id = post_['replies_to_id']
        proposal = Post.get(id=proposal_id)
        entity = get_version(proposal['entity_version']['kind'],
                             proposal['entity_version']['id'])
        entity['status'] = 'accepted'
        # TODO actually count the votes first
        # TODO block if negative response
        entity.save()

    return 200, {'post': post_.deliver()}
