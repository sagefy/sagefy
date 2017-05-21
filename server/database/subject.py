# TODO all saves should go to ES

from schemas.subject import schema as subject_schema
from database.util import deliver_fields


def deliver_subject(data, access=None):
    """
    Prepare a response for JSON output.
    """

    schema = subject_schema
    return deliver_fields(schema, data, access)
