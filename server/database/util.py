import rethinkdb as r
from modules.util import omit, extend


def insert_document(schema, data, db_conn):
    data = omit(data, ('id', 'created', 'modified'))
    return save_document(schema, data, db_conn)


def update_document(schema, prev_data, data, db_conn):
    data = omit(data, ('id', 'created', 'modified'))
    data = extend({}, prev_data, data)
    return save_document(schema, data, db_conn)


def save_document(schema, data, db_conn):
    """
    Insert the model in the database.
    Return model and errors if failed.
    """

    data = tidy_fields(schema, data)
    data = add_default_fields(schema, data)
    errors = (validate_fields(schema, data)
              + validate_unique_fields(schema, data))
    if errors:
        return None, errors
    data = bundle_fields(schema, data)
    r.table(schema['tablename']).insert(data, conflict='update').run(db_conn)
    data = r.table(schema['tablename']).get(data['id']).run(db_conn)
    return data, errors


def delete_document(tablename, doc_id, db_conn):
    r.table(tablename).get(doc_id).delete().run(db_conn)
    return None


def tidy_fields(schema, data):
    output = {}
    # TODO-2 write function
    return output


def add_default_fields(schema, data):
    output = {}
    # TODO-2 write function
    return output


def validate_fields(schema, data):
    errors = []
    # TODO-2 write function
    return errors


def validate_unique_fields(schema, data):
    errors = []
    # TODO-2 write function
    return errors


def bundle_fields(schema, data):
    output = {}
    # TODO-2 write function
    return output


def deliver_fields(schema, data, access=None):
    output = {}
    # TODO-2 write function
    return output
