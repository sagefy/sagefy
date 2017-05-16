import rethinkdb as r
from modules.util import omit, extend, pick
from copy import deepcopy
from modules.content import get as c


def insert_document(schema, data, db_conn):
    """
    Create a new document.
    Return document and errors if failed.
    """

    data = omit(data, ('id', 'created', 'modified'))
    return save_document(schema, data, db_conn)


def update_document(schema, prev_data, data, db_conn):
    """
    Update the document in the database.
    Return document and errors if failed.
    NOTICE: `prev_data` should be the _return_ of `insert_document`, not the
            originally provided data.
    """

    data = omit(data, ('id', 'created', 'modified'))
    data = extend({}, prev_data, data)
    return save_document(schema, data, db_conn)


def save_document(schema, data, db_conn):
    """
    NOTICE: You should use `insert_document` or `update_document` instead.
    Insert the document in the database.
    Return document and errors if failed.
    """

    data, errors = prepare_document(schema, data, db_conn)
    if errors:
        return None, errors
    data = bundle_fields(schema, data)
    r.table(schema['tablename']).insert(data, conflict='update').run(db_conn)
    data = r.table(schema['tablename']).get(data['id']).run(db_conn)
    return data, errors


def get_document(tablename, params, db_conn):
    """
    Get one document which matches the provided keyword arguments.
    Return None when there's no matching document.
    """

    data = None
    if params.get('id'):
        data = (r.table(tablename)
                 .get(params.get('id'))
                 .run(db_conn))
    else:
        data = list(r.table(tablename)
                     .filter(params)
                     .limit(1)
                     .run(db_conn))
        data = data[0] if len(data) > 0 else None
    return data


def list_documents(tablename, params, db_conn):
    """
    Get a list of documents matching the provided keyword arguments.
    Return empty array when no documents match.
    """

    return (r.table(tablename)
             .filter(params)
             .run(db_conn))


def delete_document(tablename, doc_id, db_conn):
    """
    Remove the document from the database.
    """

    r.table(tablename).get(doc_id).delete().run(db_conn)
    return None


###############################################################################


def recurse_embeds(fn, data, schema, prefix=''):
    for field_name, field_schema in schema.items():
        fn(data, field_name, field_schema, prefix)

        if 'embed' in field_schema:
            data[field_name] = data.get(field_name) or {}
            recurse_embeds(fn, data[field_name], field_schema['embed'],
                           '%s%s.' % (prefix, field_name))

        elif 'embed_many' in field_schema:
            data[field_name] = data.get(field_name) or []
            for i, d in enumerate(data[field_name]):
                recurse_embeds(fn, d, field_schema['embed_many'],
                               '%s%s.%i.' % (prefix, field_name, i))


def prepare_document(schema, data, db_conn):
    """
    Prepare a document to be saved.
    """

    data = tidy_fields(schema, data)
    data = add_default_fields(schema, data)
    # NOTA BENE: add_default_fields must come before validate_unique_fields
    errors = validate_fields(schema, data)
    if errors:
        return data, errors
    errors = validate_unique_fields(schema, data, db_conn)
    if errors:
        return data, errors
    if 'validate' in schema:
        for fn in schema['validate']:
            errors = fn(schema, data, db_conn)
            if errors:
                return data, errors
    return data, []


def tidy_fields(schema, data):
    """
    Remove any fields that aren't part of the schema.
    For now, we'll just remove extra fields.
    Later, we might want an option to throw errors instead.
    """

    data = deepcopy(data)

    def _(data, schema):
        for name, field_schema in schema.items():
            if 'embed' in field_schema and name in data:
                data[name] = _(data[name], field_schema['embed'])
            elif 'embed_many' in field_schema and name in data:
                for i, d in enumerate(data[name]):
                    data[name][i] = _(d, field_schema['embed_many'])
        return pick(data, schema.keys())

    return _(data, schema['fields'])


def add_default_fields(schema, data):
    """
    Set up defaults for data if not applied.
    """

    data = deepcopy(data)

    def _(data, field_name, field_schema, prefix):
        if 'default' in field_schema and data.get(field_name) is None:
            if hasattr(field_schema['default'], '__call__'):
                data[field_name] = field_schema['default']()
            else:
                data[field_name] = field_schema['default']

    recurse_embeds(_, data, schema['fields'])
    return data


def validate_fields(schema, data):
    """
    Iterate over the schema, ensuring that everything matches up.
    """

    errors = []

    def _(data, field_name, field_schema, prefix):
        if 'validate' not in field_schema:
            return
        error = None
        for fn in field_schema['validate']:
            if isinstance(fn, (list, tuple)):
                error = fn[0](data.get(field_name), *fn[1:])
            else:
                error = fn(data.get(field_name))
            if error:
                errors.append({
                    'name': prefix + field_name,
                    'message': error,
                })
                break
    recurse_embeds(_, data, schema['fields'])
    return errors


def validate_unique_fields(schema, data, db_conn):
    """
    Test all top-level fields marked as unique.
    """

    errors = []

    def _(data, field_name, field_schema, prefix):
        if ('unique' not in field_schema or
                data.get(field_name) is None):
            return
        query = (r.table(schema['tablename'])
                  .filter(r.row[field_name] == data.get(field_name))
                  .filter(r.row['id'] != data['id']))
        if len(list(query.run(db_conn))) > 0:
            errors.append({
                'name': prefix + field_name,
                'message': c('unique'),
            })
    recurse_embeds(_, data, schema['fields'])
    return errors


def bundle_fields(schema, data):
    """
    Prepare the data for saving into the database.
    Consider default values and will call `bundle`
    in the schema if present.
    """

    def _(data, field_name, field_schema, prefix):
        if 'bundle' in field_schema and data.get(field_name):
            data[field_name] = field_schema['bundle'](data[field_name])

    data = deepcopy(data)
    recurse_embeds(_, data, schema['fields'])
    return data


def deliver_fields(schema, data, access=None):
    """
    Prepare the data for consumption.
    Consider access allowed and will call `deliver`
    in the schema if present.
    """

    def _(data, field_name, field_schema, prefix):
        if ('access' in field_schema and
                data.get(field_name) is not None and
                access not in field_schema['access']):
            del data[field_name]

        elif 'deliver' in field_schema and data.get(field_name):
            data[field_name] = field_schema['deliver'](data[field_name])

    data = deepcopy(data)
    recurse_embeds(_, data, schema['fields'])
    return data
