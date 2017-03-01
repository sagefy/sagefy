from models.set import Set
from schemas.user_sets import schema as user_sets_schema
from database.util import insert_document, update_document, get_document
from copy import deepcopy

"""
Record the list of sets the learner has added.
"""


def insert_user_sets(data, db_conn):
    """
    Add a new user sets entry to the database.
    """

    schema = user_sets_schema
    return insert_document(schema, data, db_conn)


def get_user_sets(user_id, db_conn):
    """
    Get the user sets entry for a user from the database.
    """

    tablename = user_sets_schema['tablename']
    params = {'user_id': user_id}
    return get_document(tablename, params, db_conn)


def append_user_sets(user_id, set_id, db_conn):
    """
    Add a set to a user's list of sets.
    """

    prev_data = get_user_sets(user_id, db_conn)
    data = deepcopy(prev_data)
    data['set_ids'].append(set_id)
    schema = user_sets_schema
    return update_document(schema, prev_data, data, db_conn)


def remove_user_sets(user_id, set_id, db_conn):
    """
    Remove a set from a user's list of sets.
    """

    prev_data = get_user_sets(user_id, db_conn)
    data = deepcopy(prev_data)
    data['set_ids'].remove(set_id)
    schema = user_sets_schema
    return update_document(schema, prev_data, data, db_conn)


def list_user_sets_entity(user_id, params, db_conn):
    """
    Join the user's set_ids with set information.
    Return empty list when there's no matching documents.
    """

    # TODO-2 each set -- needs review?
    # TODO-2 order by last reviewed time
    uset = get_user_sets(user_id, db_conn)
    # TODO-3 limit = params.get('limit') or 10
    # TODO-3 skip = params.get('skip') or 0
    return Set.list_by_entity_ids(db_conn, uset['set_ids'])
