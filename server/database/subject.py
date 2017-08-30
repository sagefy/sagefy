# TODO all saves should go to ES

from schemas.subject import schema as subject_schema
from database.util import deliver_fields
from database.entity_base import insert_entity, update_entity, \
    save_entity_to_es


def insert_subject(db_conn, data):
    """
    Create a card, saving to ES.

    *M2P Insert Subject Version

        WITH temp AS (
            INSERT INTO subjects_entity_id (entity_id) VALUES (uuid_generate_v4())
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

    schema = subject_schema
    subject, errors = insert_entity(db_conn, schema, data)
    if not errors:
        save_entity_to_es('subject', deliver_subject(subject, access='view'))
    return subject, errors


def update_subject(db_conn, prev_data, data):
    """
    Update a card.

    *M2P Update Subject Version Status [hidden]

        UPDATE subjects
        SET status = %(status)s
        WHERE version_id = %(version_id)s
        RETURNING *;
    """

    schema = subject_schema
    subject, errors = update_entity(db_conn, schema, prev_data, data)
    if not errors:
        save_entity_to_es('subject', deliver_subject(subject, access='view'))
    return subject, errors


def deliver_subject(data, access=None):
    """
    Prepare a response for JSON output.
    """

    schema = subject_schema
    return deliver_fields(schema, data, access)


"""

*M2P Get Latest Accepted Subject Version by EID

    SELECT DISTINCT ON (entity_id) *
    FROM subjects
    WHERE status = 'accepted' AND entity_id = %(entity_id)s
    ORDER BY entity_id, created DESC;
    /* TODO LIMIT */

*M2P List Latest Accepted Subject Versions by EIDs

    SELECT DISTINCT ON (entity_id) *
    FROM subjects
    WHERE status = 'accepted' AND entity_id in %(entity_ids)s
    ORDER BY entity_id, created DESC;
    /* TODO LIMIT OFFSET */

*M2P List Subject Versions by VIDs

    SELECT *
    FROM subjects
    WHERE version_id in %(version_ids)s
    ORDER BY created DESC;
    /* TODO LIMIT OFFSET */

*M2P List Subjects Versions by EID

    SELECT *
    FROM subjects
    WHERE entity_id = %(entity_id)s
    ORDER BY created DESC;
    /* TODO LIMIT OFFSET */

*M2P List Subjects by Unit EID

    TBD

*M2P List My Recently Created Subjects (by User ID)

    SELECT DISTINCT ON (entity_id) *
    FROM subjects
    WHERE user_id = %(user_id)s
    ORDER BY entity_id, created DESC;
    /* TODO LIMIT OFFSET */
"""
