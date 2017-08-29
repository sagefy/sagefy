from schemas.user_subjects import schema as user_subjects_schema
from database.util import insert_document, update_document, get_document
from copy import deepcopy
from database.entity_base import list_by_entity_ids

"""
Record the list of subjects the learner has added.
"""


def insert_user_subjects(data, db_conn):
    """
    Add a new user subjects entry to the database.

    *M2P Insert User Subject Relation

        INSERT INTO users_subjects
        (  user_id  ,   subject_id  )
        VALUES
        (%(user_id)s, %(subject_id)s);
    """

    schema = user_subjects_schema
    return insert_document(schema, data, db_conn)


def get_user_subjects(user_id, db_conn):
    """
    Get the user subjects entry for a user from the database.

    *M2P List User Subjects by User ID

        SELECT *
        FROM users_subjects
        WHERE user_id = %(user_id)s
        ORDER BY created DESC;
        /* TODO OFFSET LIMIT */
    """

    tablename = user_subjects_schema['tablename']
    params = {'user_id': user_id}
    return get_document(tablename, params, db_conn)


def append_user_subjects(user_id, subject_id, db_conn):
    """
    Add a subject to a user's list of subjects.
    """

    prev_data = get_user_subjects(user_id, db_conn)
    data = deepcopy(prev_data)
    data['subject_ids'].append(subject_id)
    schema = user_subjects_schema
    return update_document(schema, prev_data, data, db_conn)


def remove_user_subjects(user_id, subject_id, db_conn):
    """
    Remove a subject from a user's list of subjects.

    *M2P Delete User Subject

        DELETE FROM users_subjects WHERE id = %(id)s;
    """

    prev_data = get_user_subjects(user_id, db_conn)
    data = deepcopy(prev_data)
    data['subject_ids'].remove(subject_id)
    schema = user_subjects_schema
    return update_document(schema, prev_data, data, db_conn)


def list_user_subjects_entity(user_id, params, db_conn):
    """
    Join the user's subject_ids with subject information.
    Return empty list when there's no matching documents.
    """

    # TODO-2 each subject -- needs review?
    # TODO-2 order by last reviewed time
    user_subject = get_user_subjects(user_id, db_conn)
    # TODO-3 limit = params.get('limit') or 10
    # TODO-3 skip = params.get('skip') or 0
    return list_by_entity_ids('subjects', db_conn, user_subject['subject_ids'])
