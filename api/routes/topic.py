"""
Routes for the discussion platform.
Includes topics, posts, proposals, votes, and flags.
"""

from framework.routes import get, post, put, abort
from models.topic import Topic
from framework.session import get_current_user
from modules.util import omit
from modules.discuss import instance_post_facade, create_post_facade, \
    get_post_facade, get_posts_facade
from modules.content import get as c


@post('/api/topics')
def create_topic_route(request):
    """
    Create a new topic. The first post (proposal, flag) must be provided.
    Flag: if a flag for the same reason exists for the entity,
        create a vote there instead.
    """

    current_user = get_current_user(request)
    if not current_user:
        return abort(401)

    if 'topic' not in request['params']:
        return 400, {'errors': [{
            'name': 'topic'
        }]}

    if 'post' not in request['params']:
        return 400, {'errors': [{
            'name': 'post'
        }]}

    # Let's create the topic, but not save it until we know we
    # have a valid post
    # TODO@ should this validation be part of the model?
    topic_data = dict(**request['params']['topic'])
    topic_data['user_id'] = current_user['id']
    topic = Topic(topic_data)
    post_data = dict(**request['params']['post'])
    post_data['user_id'] = current_user['id']
    post_data['topic_id'] = topic['id']
    post = instance_post_facade(post_data)

    errors, errors2 = topic.validate(), post.validate()
    if len(errors + errors2):
        return 400, {'errors': errors + errors2}

    # TODO@ validate topic entity is valid

    post, errors = post.save()
    topic, errors2 = topic.save()
    if len(errors + errors2):
        return 400, {'errors': errors + errors2}

    return 200, {'topic': topic.deliver(), 'post': post.deliver()}


@put('/api/topics/{topic_id}')
def update_topic_route(request, topic_id):
    """
    Update the topic. Only the name can be changed. Only by original author.
    """

    current_user = get_current_user(request)
    if not current_user:
        return abort(401)

    # Must be a valid topic_id
    topic = Topic.get(id=request['params'].get('topic_id'))
    if not topic:
        return 404, {'errors': [{
            'name': 'topic_id',
            'message': c('no_topic'),
        }]}

    # Must be logged in as topic's author
    if topic['user_id'] != current_user['id']:
        return abort(403)

    # Request must only be for name
    # TODO@ should this be part of the model?
    topic, errors = topic.update({
        'name': request['params'].get('name')
    })
    if errors:
        return 400, {'errors': errors}

    return 200, {'topic': topic.deliver()}


@get('/api/topics/{topic_id}/posts')
def get_posts_route(request, topic_id):
    """
    Get a reverse chronological listing of posts for given topic.
    Includes topic meta data and posts (proposals, votes, flags).
    Paginates.
    """

    # Is the topic valid?
    topic = Topic.get(id=topic_id)
    if not topic:
        return 404, {'errors': [{
            'name': 'topic_id',
            'message': c('no_topic'),
        }]}

    # Pull all kinds of posts
    posts = get_posts_facade(
        limit=request['params'].get('limit') or 10,
        skip=request['params'].get('skip') or 0,
        topic_id=topic_id
    )

    # TODO@ Should the following checks be part of the model?

    # TODO@ For proposals, pull up the proposal entity version

    # TODO@ ...then pull up the proposal latest accepted version

    # TODO@ ...if the proposal isn't based off the latest accepted,
    #       it's invalid

    # TODO@ Make a diff between the latest accepted
    #       ... and the proposal entity version

    return 200, {'posts': [p.deliver() for p in posts]}


@post('/api/topics/{topic_id}/posts')
def create_post_route(request, topic_id):
    """
    Create a new post on a given topic.
    Accounts for posts, proposals, votes, and flags.
    Proposal: must include entity (card, unit, set) information.
    Vote: must refer to a proposal.
    """

    current_user = get_current_user(request)
    if not current_user:
        return abort(401)

    # TODO@ what checks should be moved to the model?

    # TODO@ For proposal or flag, entity must be included and valid
    kind = request['params'].get('kind')
    if kind in ('proposal', 'flag',):
        pass

    # TODO@ For vote, must refer to a valid proposal
    if kind == 'vote':
        pass

    # The topic must be valid
    topic = Topic.get(id=request['params'].get('topic_id'))
    if not request['params'].get('topic_id') or not topic:
        return 404, {'errors': [{
            'name': 'topic_id',
            'message': c('no_topic'),
        }]}

    # Try to save the post (and others)
    post_data = dict(**request['params'])
    post_data['user_id'] = current_user['id']
    post, errors = create_post_facade(post_data)
    if len(errors):
        return 400, {'errors': errors}

    # TODO@ If a proposal has sufficient votes, move it to accepted
    #      ... and close out any prior versions dependent
    if kind == 'vote':
        pass

    return 200, {'post': post.deliver()}


@put('/api/topics/{topic_id}/posts/{post_id}')
def update_post_route(request, topic_id, post_id):
    """
    Update an existing post. Must be one's own post.

    For proposals and flags:
    The only field that can be updated is the status;
    the status can only be changed to declined, and only when
    the current status is pending or blocked.

    For votes:
    The only fields that can be updated are body and response.
    """

    current_user = get_current_user(request)
    if not current_user:
        return abort(401)

    post = get_post_facade(post_id)

    # Must be user's own post
    # TODO@should some of these checks be part of the model?
    if post['user_id'] != current_user['id']:
        return abort(403)

    # TODO@ If proposal, make sure its allowed changes
    if post['kind'] in ('proposal', 'flag'):
        pass

    # TODO@ If vote, make sure its allowed changes
    if post['kind'] == 'vote':
        pass

    post_data = dict(**request['params'])
    post_data = omit(post_data, ('user_id', 'topic_id', 'kind'))
    post, errors = post.update(post_data)
    if errors:
        return 400, {'errors': errors}
    return 200, {'post': post.deliver()}
