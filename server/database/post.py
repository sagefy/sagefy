from framework.elasticsearch import es
from modules.util import json_prep, pick
from schemas.post import schema as post_schema
from schemas.proposal import schema as proposal_schema
from schemas.vote import schema as vote_schema
from database.util import deliver_fields
from database.util import insert_row, update_row, get_row, list_rows
from modules.util import convert_slug_to_uuid


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
    query = """
        INSERT INTO posts
        (  user_id  ,   topic_id  ,   kind  ,   body  ,   replies_to_id  )
        VALUES
        (%(user_id)s, %(topic_id)s, %(kind)s, %(body)s, %(replies_to_id)s)
        RETURNING *;
    """
    data = pick(data, (
        'user_id',
        'topic_id',
        'kind',
        'body',
        'replies_to_id',
    ))
    data, errors = insert_row(db_conn, schema, query, data)
    if not errors:
        add_post_to_es(data, db_conn)
    return data, errors


def insert_proposal(data, db_conn):
    """
    Create a new proposal.
    """

    schema = get_post_schema(data)
    query = """
        INSERT INTO posts
        (  user_id  ,   topic_id  ,   kind  ,   body  ,
           replies_to_id  ,   entity_versions  )
        VALUES
        (%(user_id)s, %(topic_id)s, %(kind)s, %(body)s,
         %(replies_to_id)s, %(entity_versions)s)
        RETURNING *;
    """
    data = pick(data, (
        'user_id',
        'topic_id',
        'kind',
        'body',
        'replies_to_id',
        'entity_versions',
    ))
    data, errors = insert_row(db_conn, schema, query, data)
    if not errors:
        add_post_to_es(data, db_conn)
    return data, errors


def insert_vote(data, db_conn):
    """
    Create a new vote.
    """

    schema = get_post_schema(data)
    query = """
        INSERT INTO posts
        (  user_id  ,   topic_id  ,   kind  ,   body  ,
           replies_to_id  ,   response  )
        VALUES
        (%(user_id)s, %(topic_id)s, %(kind)s, %(body)s,
         %(replies_to_id)s, %(response)s)
        RETURNING *;
    """
    data = pick(data, (
        'user_id',
        'topic_id',
        'kind',
        'body',
        'replies_to_id',
        'response',
    ))
    data, errors = insert_row(db_conn, schema, query, data)
    if not errors:
        add_post_to_es(data, db_conn)
    return data, errors


def update_post(prev_data, data, db_conn):
    """
    Update an existing post.
    """

    schema = get_post_schema(data)
    query = """
        UPDATE posts
        SET body = %(body)s
        WHERE id = %(id)s AND kind = 'post'
        RETURNING *;
    """
    data = {
        'id': convert_slug_to_uuid(prev_data['id']),
        'body': data['body'],
    }
    data, errors = update_row(db_conn, schema, query, prev_data, data)
    if not errors:
        add_post_to_es(data, db_conn)
    return data, errors


def update_proposal(prev_data, data, db_conn):
    """
    Update an existing proposal.
    """

    schema = get_post_schema(data)
    query = """
        UPDATE posts
        SET body = %(body)s
        WHERE id = %(id)s AND kind = 'proposal'
        RETURNING *;
    """
    data = {
        'id': convert_slug_to_uuid(prev_data['id']),
        'body': data['body'],
    }
    data, errors = update_row(db_conn, schema, query, prev_data, data)
    if not errors:
        add_post_to_es(data, db_conn)
    return data, errors


def update_vote(prev_data, data, db_conn):
    """
    Update an existing vote.
    """

    schema = get_post_schema(data)
    query = """
        UPDATE posts
        SET body = %(body)s, response = %(response)s
        WHERE id = %(id)s AND kind = 'vote'
        RETURNING *;
    """
    data = {
        'id': convert_slug_to_uuid(prev_data['id']),
        'body': data['body'],
        'response': data['response'],
    }
    data, errors = update_row(db_conn, schema, query, prev_data, data)
    if not errors:
        add_post_to_es(data, db_conn)
    return data, errors


def get_post(params, db_conn):
    """
    Get the post matching the parameters.
    """

    query = """
        SELECT *
        FROM posts
        WHERE id = %(id)s
        LIMIT 1;
    """
    params = {
        'id': params['id'],
    }
    return get_row(db_conn, query, params)


def list_posts_by_topic(params, db_conn):
    """
    Get a list of posts in Sagefy.
    """

    query = """
        SELECT *
        FROM posts
        WHERE topic_id = %(topic_id)s
        ORDER BY created ASC;
        /* TODO OFFSET LIMIT */
    """
    params = {
        'topic_id': params['topic_id'],
    }
    return list_rows(db_conn, query, params)


def list_posts_by_user(params, db_conn):
    """
    Get a list of posts in Sagefy.
    """

    query = """
        SELECT *
        FROM posts
        WHERE user_id = %(user_id)s
        ORDER BY created ASC;
        /* TODO OFFSET LIMIT */
    """
    params = pick(params, ('user_id',))
    return list_rows(db_conn, query, params)


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
