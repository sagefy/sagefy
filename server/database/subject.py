# TODO all saves should go to ES

from schemas.subject import schema as subject_schema
from database.util import deliver_fields
from database.entity_base import save_entity_to_es
from database.util import insert_row, update_row, get_row, list_rows
from modules.util import convert_slug_to_uuid


def insert_subject(db_conn, data):
    """
    Create a card, saving to ES.
    """

    schema = subject_schema
    query = """
        WITH temp AS (
            INSERT INTO subjects_entity_id (entity_id)
            VALUES (uuid_generate_v4())
            RETURNING entity_id
        )
        INSERT INTO subjects
        (entity_id  ,   previous_id  ,   name  ,   user_id  ,
           body  ,   members  )
        SELECT
         entity_id  , %(previous_id)s, %(name)s, %(user_id)s,
         %(body)s, %(members)s
        FROM temp
        RETURNING *;
    """
    previous_id = None  # TODO-1
    # latest = get_latest_accepted_subject(..., entity_id)
    # if latest: data['previous_id'] = latest['version_id']
    data = {
        FALSE
    }
    data, errors = insert_row(db_conn, schema, query, data)
    if not errors:
        save_entity_to_es('subject', deliver_subject(data, access='view'))
    return data, errors


# TODO insert subject version


def update_subject(db_conn, prev_data, data):
    """
    Update a card version's status and available. [hidden]
    """

    schema = subject_schema
    query = """
        UPDATE subjects
        SET status = %(status)s
        WHERE version_id = %(version_id)s
        RETURNING *;
    """
    data = {
        'id': convert_slug_to_uuid(prev_data['id']),
    }
    data, errors = update_row(db_conn, schema, query, prev_data, data)
    if not errors:
        save_entity_to_es('subject', deliver_subject(data, access='view'))
    return data, errors


def deliver_subject(data, access=None):
    """
    Prepare a response for JSON output.
    """

    schema = subject_schema
    return deliver_fields(schema, data, access)


def get_latest_accepted_subject(db_conn, entity_id):
    """
    Get Latest Accepted Subject Version by EID
    """

    query = """
        SELECT DISTINCT ON (entity_id) *
        FROM subjects
        WHERE status = 'accepted' AND entity_id = %(entity_id)s
        ORDER BY entity_id, created DESC;
        /* TODO LIMIT */
    """
    params = {
        'entity_id': entity_id,
    }
    return get_row(db_conn, query, params)


def list_latest_accepted_subjects(db_conn, entity_ids):
    """
    List Latest Accepted Subject Versions by EIDs
    """

    query = """
        SELECT DISTINCT ON (entity_id) *
        FROM subjects
        WHERE status = 'accepted' AND entity_id in %(entity_ids)s
        ORDER BY entity_id, created DESC;
        /* TODO LIMIT OFFSET */
    """
    params = {'entity_ids': entity_ids}
    return list_rows(db_conn, query, params)


def list_many_subject_versions(db_conn, version_ids):
    """
    List Subject Versions by VIDs
    """

    query = """
        SELECT *
        FROM subjects
        WHERE version_id in %(version_ids)s
        ORDER BY created DESC;
        /* TODO LIMIT OFFSET */
    """
    params = {'version_ids': version_ids}
    return list_rows(db_conn, query, params)


def list_one_subject_versions(db_conn, entity_id):
    """
    List Subjects Versions by EID
    """

    query = """
        SELECT *
        FROM subjects
        WHERE entity_id = %(entity_id)s
        ORDER BY created DESC;
        /* TODO LIMIT OFFSET */
    """
    params = {'entity_id': entity_id}
    return list_rows(db_conn, query, params)


def list_subjects_by_unit_flat(db_conn, unit_id):
    """
    *M2P List Subjects by Unit EID

        TBD
    """

    query = """

    """
    params = {}
    return list_rows(db_conn, query, params)


def list_subject_parents(db_conn, subject_id):
    """
        *M2P TBD
    """

    query = """

    """
    params = {}
    return list_rows(db_conn, query, params)


def list_my_recently_created_subjects(db_conn, user_id):
    """
    List My Recently Created Subjects (by User ID)
    """

    query = """
        SELECT DISTINCT ON (entity_id) *
        FROM subjects
        WHERE user_id = %(user_id)s
        ORDER BY entity_id, created DESC;
        /* TODO LIMIT OFFSET */
    """
    params = {'user_id': user_id}
    return list_rows(db_conn, query, params)
