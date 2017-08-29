from schemas.response import schema as response_schema
from database.util import insert_document, deliver_fields


def insert_response(data, db_conn):
    """
    Create a new response.

    *M2P Insert Response

        INSERT INTO responses
        (  user_id  ,   card_id  ,   unit_id  ,
           response  ,   score  ,   learned  )
        VALUES
        (%(user_id)s, %(card_id)s, %(unit_id)s,
         %(response)s, %(score)s, %(learned)s);
    """

    schema = response_schema
    return insert_document(schema, data, db_conn)


def get_latest_response(user_id, unit_id, db_conn):
    """
    Get the latest response given a user ID and a unit ID.

    *M2P List Responses by User ID and Unit EID

        SELECT *
        FROM responses
        WHERE user_id = %(user_id)s AND unit_id = %(unit_id)s
        ORDER BY created DESC;
        /* TODO LIMIT OFFSET */
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
