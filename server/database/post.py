from framework.elasticsearch import es
from modules.util import json_prep, omit, extend
from schemas.post import schema as post_schema
from schemas.proposal import schema as proposal_schema
from schemas.vote import schema as vote_schema
from database.util import insert_document, update_document, deliver_fields, \
    get_document, prepare_document
import rethinkdb as r
from modules.entity import get_version  # TODO-2 this may cause a problem


def get_post_schema(data):
    kind = data.get('kind')
    mapping = {
        'post': post_schema,
        'proposal': proposal_schema,
        'vote': vote_schema,
    }
    return mapping.get(kind) or post_schema


def insert_post(data, db_conn):
    """
    Create a new post.
    """

    schema = get_post_schema(data)
    data, errors = validate_post(data, db_conn)
    if errors:
        return data, errors
    data, errors = insert_document(schema, data, db_conn)
    if not errors:
        add_post_to_es(data, db_conn)
    return data, errors


def update_post(prev_data, data, db_conn):
    """
    Update an existing post.
    """

    schema = get_post_schema(data)
    data2 = omit(data, ('id', 'created', 'modified'))
    data2 = extend({}, prev_data, data2)
    data, errors = validate_post(data2, db_conn)
    if errors:
        return data, errors
    data, errors = update_document(schema, prev_data, data, db_conn)
    if not errors:
        add_post_to_es(data, db_conn)
    return data, errors


def validate_post(data, db_conn):
    """
    Validate a post before saving it against the schema.
    """

    schema = get_post_schema(data)
    data, errors = prepare_document(schema, data, db_conn)
    if not errors:
        errors += is_valid_topic_id(data)
    if not errors:
        errors += is_valid_reply(data, db_conn)
    if data['kind'] == 'proposal':
        if not errors:
            errors += is_valid_version(data)
    if data['kind'] == 'vote':
        if not errors:
            errors += is_unique_vote(data, db_conn)
        if not errors:
            errors += is_valid_reply_kind(data, db_conn)
    return data, errors


def get_post(params, db_conn):
    """
    Get the post matching the parameters.
    """

    tablename = post_schema['tablename']
    return get_document(tablename, params, db_conn)


def list_posts(params, db_conn):
    """
    Get a list of posts in Sagefy.
    """

    skip = params.get('skip') or 0
    limit = params.get('limit') or 10
    params = omit(params, ('skip', 'limit',))
    query = (r.table(post_schema['tablename'])
              .filter(params)
              .order_by(r.asc('created'))
              .skip(skip)
              .limit(limit))
    return list(query.run(db_conn))


def deliver_post(data, access=None):
    """
    Prepare post data for JSON response.
    """

    schema = get_post_schema(data)
    return deliver_fields(schema, data, access)


def add_post_to_es(post, db_conn):
    """
    Upsert the post data into elasticsearch.
    """

    from database.topic import get_topic, deliver_topic
    from database.user import get_user, deliver_user

    data = json_prep(deliver_post(post))
    topic = get_topic({'id': post['topic_id']}, db_conn)
    if topic:
        data['topic'] = json_prep(deliver_topic(topic))
    user = get_user({'id': post['user_id']}, db_conn)
    if user:
        data['user'] = json_prep(deliver_user(user))

    return es.index(
        index='entity',
        doc_type='post',
        body=data,
        id=post['id'],
    )


def is_valid_topic_id(data):
    """
    TODO-3 Ensure the topic is valid.
           Is there a way to allow for 'in memory only' topic?
    (We're currently validating this in the route for now...)
    """

    return []


def is_valid_reply(data, db_conn):
    """
    A reply must belong to the same topic.
    - A post can reply to a post, proposal, or vote.
    - A proposal can reply to a post, proposal, or vote.
    - A vote may only reply to a proposal.
    """

    if data.get('replies_to_id'):
        query = (r.table(post_schema['tablename'])
                  .get(data['replies_to_id']))
        post_data = query.run(db_conn)
        if not post_data:
            return [{'message': 'Replying to a non-existant post.'}]
        if post_data['topic_id'] != data['topic_id']:
            return [{'message': 'A reply must be in the same topic.'}]
    return []


def is_valid_version(data):
    """
    TODO-2 Ensure this is a valid version of the entity. (circular)
    This is checked on the create/update form already.
    """
    return []


def is_unique_vote(data, db_conn):
    """
    Ensure a user can only vote once per proposal.
    """

    query = (r.table(post_schema['tablename'])
              .filter(r.row['user_id'] == data['user_id'])
              .filter(r.row['replies_to_id'] == data['replies_to_id'])
              .filter(r.row['kind'] == 'vote'))
    documents = [doc for doc in query.run(db_conn)]
    if documents:
        return [{'message': 'You already have a vote on this proposal.'}]
    return []


def is_valid_reply_kind(data, db_conn):
    """
    A vote can reply to a proposal.
    A vote cannot reply to a proposal that is accepted or declined.
    A user cannot vote on their own proposal.
    """

    query = (r.table(post_schema['tablename'])
              .get(data['replies_to_id']))
    proposal_data = query.run(db_conn)
    if not proposal_data:
        return [{'message': 'No proposal found.'}]
    if proposal_data['kind'] != 'proposal':
        return [{'message': 'A vote must reply to a proposal.'}]
    if proposal_data['user_id'] == data['user_id']:
        return [{'message': 'You cannot vote on your own proposal.'}]
    entity_version = get_version(db_conn,
                                 proposal_data['entity_versions'][0]['kind'],
                                 proposal_data['entity_versions'][0]['id'])
    if not entity_version:
        return [{'message': 'No entity version for proposal.'}]
    if entity_version['status'] in ('accepted', 'declined'):
        return [{'message': 'Proposal is already complete.'}]
    return []
