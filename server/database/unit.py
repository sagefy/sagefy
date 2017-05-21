# TODO all saves should go to ES

from schemas.unit import schema as unit_schema
from database.util import deliver_fields


def deliver_unit(data, access=None):
    """
    Prepare a response for JSON output.
    """

    schema = unit_schema
    return deliver_fields(schema, data, access)
