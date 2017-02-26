from schemas.response import schema as response_schema
from database.util import insert_document, deliver_fields
import rethinkdb as r


def insert_response(data, db_conn):
    """
    Create a new response.
    """

    schema = response_schema
    return insert_document(schema, data, db_conn)


def get_latest_response(user_id, unit_id, db_conn):
    """
    Get the latest response given a user ID and a unit ID.
    """

    tablename = response_schema['tablename']
    query = (r.table(tablename)
              .filter(r.row['user_id'].eq(user_id))
              .filter(r.row['unit_id'].eq(unit_id))
              .max('created')
              .default(None))
    document = query.run(db_conn)
    if document:
        return document


def deliver_response(data, access=None):
    """
    Prepare a response for JSON output.
    """

    schema = response_schema
    return deliver_fields(schema, data, access)
