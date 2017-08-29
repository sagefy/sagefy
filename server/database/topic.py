from modules.util import json_prep, pick
from framework.elasticsearch import es
from schemas.topic import schema as topic_schema
from database.util import insert_document, update_document, deliver_fields, \
    get_document


def insert_topic(data, db_conn):
    """
    Create a new topic.

    *M2P Insert a Topic

        INSERT INTO topics
        (  user_id  ,   entity_id  ,   entity_kind  ,   name  )
        VALUES
        (%(user_id)s, %(entity_id)s, %(entity_kind)s, %(name)s)
        RETURNING *;
    """

    schema = topic_schema
    data, errors = insert_document(schema, data, db_conn)
    if not errors:
        add_topic_to_es(data)
    return data, errors


def update_topic(prev_data, data, db_conn):
    """
    Update an existing topic.

    *M2P Update a Topic Name

        UPDATE topics
        SET name = %(name)s
        WHERE id = %(id)s
        RETURNING *;
    """

    schema = topic_schema
    data = pick(data, ('name',))
    data, errors = update_document(schema, prev_data, data, db_conn)
    if not errors:
        add_topic_to_es(data)
    return data, errors


def get_topic(params, db_conn):
    """
    Get the topic matching the parameters.

    *M2P Get Topic by ID

        SELECT *
        FROM topics
        WHERE id = %(id)s
        LIMIT 1;
    """

    tablename = topic_schema['tablename']
    return get_document(tablename, params, db_conn)


def list_topics(params, db_conn):
    """
    Get a list of topics in Sagefy.

    *M2P List Topics (All)

        SELECT *
        FROM topics
        ORDER BY created DESC;
        /* TODO OFFSET LIMIT */
    """

    schema = topic_schema
    query = r.table(schema['tablename'])
    return list(query.run(db_conn))


def deliver_topic(data, access=None):
    """
    Prepare user data for JSON response.
    """

    schema = topic_schema
    return deliver_fields(schema, data, access)


def list_topics_by_entity_id(entity_id, params, db_conn):
    """
    Get a list of models matching the provided keyword arguments.
    Return empty array when no models match.

    *M2P List Topics by EID

    SELECT *
    FROM topics
    WHERE entity_id = %(entity_id)s
    ORDER BY created DESC;
    /* TODO OFFSET LIMIT */
    """

    limit = params.get('limit') or 10
    skip = params.get('skip') or 0
    tablename = topic_schema['tablename']
    documents = (r.table(tablename)
                  .filter(r.row['entity']['id'] == entity_id)
                  .order_by(r.desc('created'))
                  .limit(limit)
                  .skip(skip)
                  .run(db_conn))
    return documents


def add_topic_to_es(topic):
    """
    Add the topic to ElasticSearch.
    """

    data = json_prep(deliver_topic(topic))
    es.index(
        index='entity',
        doc_type='topic',
        body=data,
        id=data['id'],
    )
