from framework.elasticsearch import es
from modules.util import json_prep, pick, omit
from schemas.post import schema as post_schema
from schemas.proposal import schema as proposal_schema
from schemas.vote import schema as vote_schema
from database.util import insert_document, update_document, deliver_fields, \
    get_document


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

    *M2P Create a new Post

        POST:

        INSERT INTO posts
        (  user_id  ,   topic_id  ,   kind  ,   body  ,   replies_to_id  )
        VALUES
        (%(user_id)s, %(topic_id)s, %(kind)s, %(body)s, %(replies_to_id)s);

        PROPOSAL:

        INSERT INTO posts
        (  user_id  ,   topic_id  ,   kind  ,   body  ,
           replies_to_id  ,   entity_versions  )
        VALUES
        (%(user_id)s, %(topic_id)s, %(kind)s, %(body)s,
         %(replies_to_id)s, %(entity_versions)s);

        VOTE:

        INSERT INTO posts
        (  user_id  ,   topic_id  ,   kind  ,   body  ,
           replies_to_id  ,   response  )
        VALUES
        (%(user_id)s, %(topic_id)s, %(kind)s, %(body)s,
         %(replies_to_id)s, %(response)s);
    """

    schema = get_post_schema(data)
    data, errors = insert_document(schema, data, db_conn)
    if not errors:
        add_post_to_es(data, db_conn)
    return data, errors


def update_post(prev_data, data, db_conn):
    """
    Update an existing post.

    *M2P Update Post (fields limited)

        POST:

        UPDATE posts
        SET body = %(body)s
        WHERE id = %(id)s AND kind = 'post';

        PROPOSAL:

        UPDATE posts
        SET body = %(body)s
        WHERE id = %(id)s AND kind = 'proposal';

        VOTE:

        UPDATE posts
        SET body = %(body)s, response = %(response)s
        WHERE id = %(id)s AND kind = 'vote';
    """

    schema = get_post_schema(data)
    post_kind = prev_data['kind']
    if post_kind is 'post' or post_kind is 'proposal':
        data = pick(data, ('body',))
    elif post_kind is 'vote':
        data = pick(data, ('body', 'response',))
    data, errors = update_document(schema, prev_data, data, db_conn)
    if not errors:
        add_post_to_es(data, db_conn)
    return data, errors


def get_post(params, db_conn):
    """
    Get the post matching the parameters.

    *M2P Get Post by ID

        SELECT *
        FROM posts
        WHERE id = %(id)s
        LIMIT 1;
    """

    tablename = post_schema['tablename']
    return get_document(tablename, params, db_conn)


def list_posts(params, db_conn):
    """
    Get a list of posts in Sagefy.

    *M2P List Posts by Topic ID

        SELECT *
        FROM posts
        WHERE topic_id = %(topic_id)s
        ORDER BY created ASC;
        /* TODO OFFSET LIMIT */

    *M2P List Posts by User ID

        SELECT *
        FROM posts
        WHERE user_id = %(user_id)s
        ORDER BY created ASC;
        /* TODO OFFSET LIMIT */
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
