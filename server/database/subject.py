# TODO all saves should go to ES

from schemas.subject import schema as subject_schema
from database.util import deliver_fields
from database.entity_base import insert_entity, update_entity, \
    save_entity_to_es


def insert_subject(db_conn, data):
    """
    Create a card, saving to ES.
    """

    schema = subject_schema
    subject, errors = insert_entity(schema, db_conn, data)
    if not errors:
        save_entity_to_es('subject', deliver_subject(subject, access='view'))
    return subject, errors


def update_subject(prev_data, data, db_conn):
    """
    Update a card.
    """

    schema = subject_schema
    subject, errors = update_entity(schema, prev_data, data, db_conn)
    if not errors:
        save_entity_to_es('subject', deliver_subject(subject, access='view'))
    return subject, errors


def deliver_subject(data, access=None):
    """
    Prepare a response for JSON output.
    """

    schema = subject_schema
    return deliver_fields(schema, data, access)
