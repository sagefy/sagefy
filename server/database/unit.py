# TODO all saves should go to ES

from schemas.unit import schema as unit_schema
from database.util import deliver_fields
from database.entity_base import insert_entity, update_entity, \
    save_entity_to_es


def insert_unit(db_conn, data):
    """
    Create a card, saving to ES.

    *M2P Insert Unit Version

        WITH temp AS (
            INSERT INTO units_entity_id (entity_id) VALUES (uuid_generate_v4())
            RETURNING entity_id
        )
        INSERT INTO units
        (entity_id  ,   previous_id  ,   name  ,   user_id  ,
           body  ,   require_ids  )
        SELECT
         entity_id  , %(previous_id)s, %(name)s, %(user_id)s,
         %(body)s, %(require_ids)s
        FROM temp;
    """

    schema = unit_schema
    unit, errors = insert_entity(schema, db_conn, data)
    if not errors:
        save_entity_to_es('unit', deliver_unit(unit, access='view'))
    return unit, errors


def update_unit(prev_data, data, db_conn):
    """
    Update a card.

    *M2P Update Unit Version Status [hidden]

        UPDATE units
        SET status = %(status)s
        WHERE version_id = %(version_id)s;
    """

    schema = unit_schema
    unit, errors = update_entity(schema, prev_data, data, db_conn)
    if not errors:
        save_entity_to_es('unit', deliver_unit(unit, access='view'))
    return unit, errors


def deliver_unit(data, access=None):
    """
    Prepare a response for JSON output.
    """

    schema = unit_schema
    return deliver_fields(schema, data, access)


"""

*M2P Get Latest Accepted Unit Version by EID

    SELECT DISTINCT ON (entity_id) *
    FROM units
    WHERE status = 'accepted' AND entity_id = %(entity_id)s
    ORDER BY entity_id, created DESC;
    /* TODO LIMIT */

*M2P List Latest Accepted Unit Versions by EIDs

    SELECT DISTINCT ON (entity_id) *
    FROM units
    WHERE status = 'accepted' AND entity_id in %(entity_ids)s
    ORDER BY entity_id, created DESC;
    /* TODO LIMIT OFFSET */

*M2P List Unit Versions by VIDs

    SELECT *
    FROM units
    WHERE version_id in %(version_ids)s
    ORDER BY created DESC;
    /* TODO LIMIT OFFSET */

*M2P List Unit Versions by EID

    SELECT *
    FROM units
    WHERE entity_id = %(entity_id)s
    ORDER BY created DESC;
    /* TODO LIMIT OFFSET */

*M2P List Latest Version of Required Units by EID

    1. Get Latest Accepted Unit Version by EID
    2. List Latest Accepted Unit Versions by EIDs (require_ids)

*M2P List Latest Version of Required By Units by EID

    WITH temp as (
        SELECT DISTINCT ON (entity_id) *
        FROM units
        WHERE status = 'accepted'
        ORDER BY entity_id, created DESC
    )
    SELECT *
    FROM temp
    WHERE %(entity_id)s in require_ids
    ORDER BY created DESC;
    /* TODO LIMIT OFFSET */

*M2P List Units by Subject EID

    TBD

*M2P List My Recently Created Units (by User ID)

    SELECT DISTINCT ON (entity_id) *
    FROM units
    WHERE user_id = %(user_id)s
    ORDER BY entity_id, created DESC;
    /* TODO LIMIT OFFSET */
"""
