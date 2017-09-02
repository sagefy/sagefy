from schemas.follow import schema as follow_schema
from database.util import deliver_fields
from database.util import insert_row, get_row, list_rows, delete_row
from module.util import pick


def get_follow(db_conn, user_id, entity_id):
    """
    Find a specific follow (entity <-> user).
    """

    query = """
        SELECT *
        FROM follows
        WHERE user_id = %(user_id)s AND entity_id = %(entity_id)s
        LIMIT 1;
    """
    params = {
        'user_id': user_id,
        'entity_id': entity_id,
    }
    return get_row(db_conn, query, params)


def list_follows_by_user(db_conn, params):
    """
    Get a list of models matching the provided arguments.
    Also adds pagination capabilities.
    Returns empty array when no models match.
    TODO-3 filter by entity kind as well
    """

    query = """
        SELECT *
        FROM follows
        WHERE user_id = %(user_id)s
        ORDER BY created DESC;
        /* TODO OFFSET LIMIT */
    """
    params = {
        'user_id': params['user_id'],
    }
    return list_rows(db_conn, query, params)


def list_follows_by_entity(db_conn, params):
    """
    Get a list of models matching the provided arguments.
    Also adds pagination capabilities.
    Returns empty array when no models match.
    TODO-3 Also filter by kind.
    """

    query = """
        SELECT *
        FROM follows
        WHERE entity_id = %(entity_id)s
        ORDER BY created DESC;
        /* TODO OFFSET LIMIT */
    """
    params = {
        'entity_id': params['entity_id'],
    }
    return list_rows(db_conn, query, params)


def insert_follow(db_conn, data):
    """
    Create a new follow (user <-> entity).
    """

    # TODO-2 move these to schema-level 'validate' fns instead.
    # See database/util.py: for fn in schema['validate']:

    schema = follow_schema
    query = """
        INSERT INTO follows
        (  user_id  ,   entity_id  ,   entity_kind  )
        VALUES
        (%(user_id)s, %(entity_id)s, %(entity_kind)s)
        RETURNING *;
    """
    data = pick(data, ('user_id', 'entity_id', 'entity_kind'))
    data, errors = insert_row(db_conn, schema, query, data)
    return data, errors

    schema = follow_schema
    data, errors = prepare_row(db_conn, schema, data)
    if errors:
        return None, errors
    errors = is_valid_entity(db_conn, data)
    if errors:
        return None, errors
    return insert_document(db_conn, schema, data)


def deliver_follow(data, access=None):
    """
    Prepare a follow for JSON output.
    """

    schema = follow_schema
    return deliver_fields(schema, data, access)


def delete_follow(db_conn, id_):
    """
    Remove a follow from the database.
    """

    query = """
        DELETE FROM follows
        WHERE id = %(id)s;
    """
    params = {
        'id': id_,
    }
    return delete_row(db_conn, query, params)


def is_valid_entity(db_conn, follow):
    """
    Check that the entity ID of the follow is valid.
    """

    kind = follow['entity_kind']
    stuff = None
    if kind == 'topic':
        stuff = get_topic(db_conn, {'id': follow['id']})
    else:
        stuff = list_one_entity_versions(db_conn, kind, follow['entity_id'])
    if not stuff:
        return [{'message': 'Not a valid entity'}]
    return []


def get_user_ids_by_followed_entity(db_conn, entity_id, entity_kind):
    """
    Produce a list of `user_id`s for a given entity.
    """

    follows = list_follows_by_entity(db_conn, {'entity_id': entity_id})
    return [fields['user_id'] for fields in follows]
