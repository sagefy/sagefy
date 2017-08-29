from schemas.follow import schema as follow_schema
from database.util import get_document, prepare_document, insert_document, \
    deliver_fields, delete_document


def get_follow(params, db_conn):
    """
    Find a specific follow (entity <-> user).

    *M2P Get Follow by User ID AND EID

        SELECT *
        FROM follows
        WHERE user_id = %(user_id)s AND entity_id = %(entity_id)s
        LIMIT 1;
    """

    schema = follow_schema
    tablename = schema['tablename']
    return get_document(tablename, params, db_conn)


def list_follows(params, db_conn):
    """
    Get a list of models matching the provided arguments.
    Also adds pagination capabilities.
    Returns empty array when no models match.

    *M2P List Follows by User ID

        SELECT *
        FROM follows
        WHERE user_id = %(user_id)s
        ORDER BY created DESC;
        /* TODO OFFSET LIMIT */

    *M2P List Follows by EID

        SELECT *
        FROM follows
        WHERE entity_id = %(entity_id)s
        ORDER BY created DESC;
        /* TODO OFFSET LIMIT */
    """

    schema = follow_schema
    user_id = params.get('user_id')
    limit = params.get('limit') or 10
    skip = params.get('skip') or 0
    kind = params.get('kind')
    entity_id = params.get('entity_id')
    query = (r.table(schema['tablename'])
              .order_by(r.desc('created'))
              .filter(r.row['user_id'] == user_id
                      if user_id is not None else True)
              .filter(r.row['entity']['kind'] == kind
                      if kind is not None else True)
              .filter(r.row['entity']['id'] == entity_id
                      if entity_id is not None else True)
              .skip(skip)
              .limit(limit))
    return query.run(db_conn)


def insert_follow(data, db_conn):
    """
    Create a new follow (user <-> entity).

    *M2P Insert Follow

        INSERT INTO follows
        (  user_id  ,   entity_id  ,   entity_kind  )
        VALUES
        (%(user_id)s, %(entity_id)s, %(entity_kind)s);
    """

    # TODO-2 move these to schema-level 'validate' fns instead.
    # See database/util.py: for fn in schema['validate']:

    schema = follow_schema
    data, errors = prepare_document(schema, data, db_conn)
    if errors:
        return None, errors
    errors = validate_uniqueness(data, db_conn)
    if errors:
        return None, errors
    errors = is_valid_entity(data, db_conn)
    if errors:
        return None, errors
    return insert_document(schema, data, db_conn)


def deliver_follow(data, access=None):
    """
    Prepare a follow for JSON output.
    """

    schema = follow_schema
    return deliver_fields(schema, data, access)


def delete_follow(doc_id, db_conn):
    """
    Remove a follow from the database.

    *M2P Delete Follow

        DELETE FROM follows WHERE id = %(id)s;
    """

    schema = follow_schema
    tablename = schema['tablename']
    return delete_document(tablename, doc_id, db_conn)


def validate_uniqueness(follow, db_conn):
    """
    Ensure the user is not already following the entity BEFORE insert.
    """

    prev = list_follows({
        'user_id': follow['user_id'],
        'entity_id': follow['entity']['id'],
    }, db_conn)
    if prev:
        return [{'message': 'Already followed.'}]
    return []


def is_valid_entity(follow, db_conn):
    """
    Check that the entity ID of the follow is valid.
    """

    kind = follow['entity']['kind']

    query = (r.table(kind + 's')
              .filter(r.row[
                  'id' if kind == 'topic' else 'entity_id'
              ] == follow['entity']['id']))

    entities = [e for e in query.run(db_conn)]

    if not entities:
        return [{'message': 'Not a valid entity'}]

    return []


def get_user_ids_by_followed_entity(entity_id, entity_kind, db_conn):
    """
    Produce a list of `user_id`s for a given entity.
    """

    schema = follow_schema
    tablename = schema['tablename']
    query = (r.table(tablename)
              .filter(r.row['entity']['id'] == entity_id)
              .filter(r.row['entity']['kind'] == entity_kind))
    fields_list = query.run(db_conn)
    return [fields['user_id'] for fields in fields_list]
