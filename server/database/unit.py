# TODO all saves should go to ES

from schemas.unit import schema as unit_schema
from database.util import deliver_fields
from database.entity_base import insert_entity, update_entity, \
    save_entity_to_es


def insert_unit(db_conn, data):
    """
    Create a card, saving to ES.
    """

    schema = unit_schema
    unit, errors = insert_entity(schema, db_conn, data)
    if not errors:
        save_entity_to_es('unit', deliver_unit(unit, access='view'))
    return unit, errors


def update_unit(prev_data, data, db_conn):
    """
    Update a card.
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
