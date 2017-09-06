# TODO all saves should go to ES

from schemas.unit import schema as unit_schema
from database.util import deliver_fields
from database.entity_base import save_entity_to_es
from database.util import insert_row, update_row, get_row, list_rows
from modules.util import convert_slug_to_uuid


def ensure_requires(db_conn, data):
    """

    """

    units = list_latest_accepted_units(db_conn, data['require_ids'])
    if len(data['require_ids']) != len(units):
        return [{'message': 'Didn\'t find all requires.'}]
    return []


def ensure_no_cycles(db_conn, data):
    """
    Ensure no require cycles form.
    """

    from database.entity_facade import find_requires_cycle

    if find_requires_cycle(db_conn, 'units', data):
        return [{'message': 'Found a cycle in requires.'}]
    return []


def insert_unit(db_conn, data):
    """
    Create a unit, saving to ES.
    """

    schema = unit_schema
    query = """
        WITH temp AS (
            INSERT INTO units_entity_id (entity_id)
            VALUES (uuid_generate_v4())
            RETURNING entity_id
        )
        INSERT INTO units
        (entity_id  ,   name  ,   user_id  ,
           body  ,   require_ids  )
        SELECT
         entity_id  , %(name)s, %(user_id)s,
         %(body)s, %(require_ids)s
        FROM temp
        RETURNING *;
    """
    errors = ensure_requires(db_conn, data) + ensure_no_cycles(db_conn, data)
    if errors:
        return None, errors
    data, errors = insert_row(db_conn, schema, query, data)
    if not errors:
        save_entity_to_es('unit', deliver_unit(data, access='view'))
    return data, errors


# TODO insert unit version, adding in previous version
"""
    previous_id = None  # TODO-1
    # latest = get_latest_accepted_unit(..., entity_id)
    # if latest: data['previous_id'] = latest['version_id']
    data = {
        FALSE
    }
"""


def update_unit(db_conn, prev_data, data):
    """
    Update a unit versions's status and available. [hidden]
    """

    schema = unit_schema
    query = """
        UPDATE units
        SET status = %(status)s
        WHERE version_id = %(version_id)s
        RETURNING *;
    """
    data = {
        'id': convert_slug_to_uuid(prev_data['id']),
        'status': data['status'],
    }
    data, errors = update_row(db_conn, schema, query, prev_data, data)
    if not errors:
        save_entity_to_es('unit', deliver_unit(data, access='view'))
    return data, errors


def deliver_unit(data, access=None):
    """
    Prepare a response for JSON output.
    """

    schema = unit_schema
    return deliver_fields(schema, data, access)


def get_latest_accepted_unit(db_conn, entity_id):
    """
    Get Latest Accepted Unit Version by EID
    """

    query = """
        SELECT DISTINCT ON (entity_id) *
        FROM units
        WHERE status = 'accepted' AND entity_id = %(entity_id)s
        ORDER BY entity_id, created DESC;
        /* TODO LIMIT */
    """
    params = {
        'entity_id': convert_slug_to_uuid(entity_id),
    }
    return get_row(db_conn, query, params)


def list_latest_accepted_units(db_conn, entity_ids):
    """
    List Latest Accepted Unit Versions by EIDs
    """

    if not entity_ids:
        return []
    query = """
        SELECT DISTINCT ON (entity_id) *
        FROM units
        WHERE status = 'accepted' AND entity_id in %(entity_ids)s
        ORDER BY entity_id, created DESC;
        /* TODO LIMIT OFFSET */
    """
    params = {'entity_ids': tuple(entity_ids)}
    return list_rows(db_conn, query, params)


def list_many_unit_versions(db_conn, version_ids):
    """
    List Unit Versions by VIDs
    """

    query = """
        SELECT *
        FROM units
        WHERE version_id in %(version_ids)s
        ORDER BY created DESC;
        /* TODO LIMIT OFFSET */
    """
    params = {'version_ids': version_ids}
    return list_rows(db_conn, query, params)


def get_unit_version(db_conn, version_id):
    """
    Get a unit version.
    """

    query = """
        SELECT *
        FROM units
        WHERE version_id = %(version_id)s
        ORDER BY created DESC;
        /* TODO LIMIT OFFSET */
    """
    params = {'version_id': version_id}
    return list_rows(db_conn, query, params)


def list_one_unit_versions(db_conn, entity_id):
    """
    List Unit Versions by EID
    """

    query = """
        SELECT *
        FROM units
        WHERE entity_id = %(entity_id)s
        ORDER BY created DESC;
        /* TODO LIMIT OFFSET */
    """
    params = {'entity_id': convert_slug_to_uuid(entity_id)}
    return list_rows(db_conn, query, params)


def list_required_units(db_conn, entity_id):
    """
    List Latest Version of Required Units by EID
    """

    later_unit = get_latest_accepted_unit(db_conn, entity_id)
    return list_latest_accepted_units(db_conn, later_unit['require_ids'])


def list_required_by_units(db_conn, entity_id):
    """
    List Latest Version of Required By Units by EID
    """

    query = """
        WITH temp as (
            SELECT DISTINCT ON (entity_id) *
            FROM units
            WHERE status = 'accepted'
            ORDER BY entity_id, created DESC
        )
        SELECT *
        FROM temp
        WHERE %(entity_id)s = ANY(require_ids)
        ORDER BY created DESC;
        /* TODO LIMIT OFFSET */
    """
    params = {
        'entity_id': convert_slug_to_uuid(entity_id),
    }
    return list_rows(db_conn, query, params)


def list_units_by_subject_flat(db_conn, subject_id):
    """
    List Units by Subject EID
    """

    from database.subject import get_latest_accepted_subject

    subject = get_latest_accepted_subject(db_conn, subject_id)
    unit_ids = [
        member['id']
        for member in subject['members']
        if member['kind'] == 'unit'
    ]
    return list_latest_accepted_units(db_conn, unit_ids)


def list_my_recently_created_units(db_conn, user_id):
    """
    List My Recently Created Units (by User ID)
    """

    query = """
        SELECT DISTINCT ON (entity_id) *
        FROM units
        WHERE user_id = %(user_id)s
        ORDER BY entity_id, created DESC;
        /* TODO LIMIT OFFSET */
    """
    params = {'user_id': user_id}
    return list_rows(db_conn, query, params)


def list_all_unit_entity_ids(db_conn):
    """
    List all unit entity ids.
    """

    query = """
        SELECT entity_id
        FROM units;
    """
    params = {}
    return [
        row['entity_id']
        for row in list_rows(db_conn, query, params)
    ]
