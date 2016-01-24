import rethinkdb as r
from modules.util import uniqid, omit, pick, extend
from modules.content import get as c
from modules.classproperty import classproperty
from copy import deepcopy

# TODO-2 Remove OOP based model. Instead, just use simple functions,
#      preferring pure functions where possible.


def update_modified(field):
    return r.now()


def iter(fn, data, schema, prefix=''):
    for field_name, field_schema in schema.items():
        fn(data, field_name, field_schema, prefix)

        if 'embed' in field_schema:
            data[field_name] = data.get(field_name) or {}
            iter(fn, data[field_name], field_schema['embed'],
                 '%s%s.' % (prefix, field_name))

        elif 'embed_many' in field_schema:
            data[field_name] = data.get(field_name) or []
            for i, d in enumerate(data[field_name]):
                iter(fn, d, field_schema['embed_many'],
                     '%s%s.%i.' % (prefix, field_name, i))


class Model(object):
    strict = True
    # strict = True will remove any fields not defined in the schema
    # to open up, either do strict = False or specify the field names in the
    # schema with an empty dict

    schema = {
        'id': {
            'default': uniqid
            # RethinkDB by default uses UUID, but as its JSON,
            # there's no reason to not use the full alphanumeric set
        },
        'created': {
            'default': r.now()
        },
        'modified': {
            'default': r.now(),
            'bundle': update_modified
        }
    }
    # Extend with: schema = dict(Parent.schema.copy(), **{ ... })

    # Avaliable per field:
    # - validate:   a list of functions to run on the field.
    #               return a string if error, None if okay
    # - bundle:     before saving to the database,
    #               transform the data
    # - default:    default value of the field
    #               can be a value or a function to call
    # - deliver:    tranform the data before sending out to the client
    #               can also be used for permissions
    # - access:     control which client can access this field's information
    # - unique:     True will check to make sure no other row has
    #               the same value not needed on `id` field,
    #               as it is the primary key
    # - embed:      list of fields contained in the field
    # - embed_many: list of fields contained in a list of dicts

    indexes = ()
    # A list of indexes for the table

    def __init__(self, data=None):
        """
        Initialize the model, setting defaults where needed.
        """

        self.data = data or {}
        self.defaults()

    def __getitem__(self, key):
        """
        Enable `model['field']`.
        """

        return self.data.get(key)

    def __setitem__(self, key, value):
        """
        Enable `model['field'] = value`.
        """

        self.data[key] = value

    def __delitem__(self, key):
        """
        Enable `del model['field']`.
        """

        del self.data[key]

    def __contains__(self, item):
        """
        Enable `field in model`.
        """

        return item in self.data

    @classproperty
    def table(self):
        """
        Refer to `self.table` and get a RethinkDB reference to the table.
        """

        assert self.tablename, 'You must provide a tablename.'
        return r.table(self.tablename)

    @classmethod
    def get(cls, db_conn, **params):
        """
        Get one model which matches the provided keyword arguments.
        Return None when there's no matching document.
        """

        data = None
        if params.get('id'):
            data = (cls.table
                       .get(params.get('id'))
                       .run(db_conn))
        else:
            data = list(cls.table
                           .filter(params)
                           .limit(1)
                           .run(db_conn))
            data = data[0] if len(data) > 0 else None
        if data:
            return cls(data)

    @classmethod
    def list(cls, db_conn, **params):
        """
        Get a list of models matching the provided keyword arguments.
        Return empty array when no models match.
        """

        data_list = (cls.table
                        .filter(params)
                        .run(db_conn))
        return [cls(data) for data in data_list]

    @classmethod
    def insert(cls, db_conn, data):
        """
        Create a new model instance.
        Return model and errors if failed.
        """

        assert isinstance(data, dict)
        data = omit(data, ('id', 'created', 'modified'))
        instance = cls(data)
        return instance.save(db_conn)

    def update(self, db_conn, data):
        """
        Update the model in the database.
        Return model and errors if failed.
        """

        assert isinstance(data, dict)
        data = omit(data, ('id', 'created', 'modified'))
        extend(self.data, data)
        return self.save(db_conn)

    def save(self, db_conn):
        """
        Insert the model in the database.
        Return model and errors if failed.
        """

        errors = self.validate(db_conn)
        if len(errors):
            return self, errors
        data = self.bundle()
        self.id = data['id']
        self.table.insert(data, conflict='update').run(db_conn)
        self.sync(db_conn)
        return self, []

    def sync(self, db_conn):
        """
        Pull the fields from the database.
        """

        data = (self.table
                    .get(self['id'])
                    .run(db_conn))
        extend(self.data, data)
        return self

    def delete(self, db_conn):
        """
        Remove the model from the database.
        """

        (self.table
             .get(self['id'])
             .delete()
             .run(db_conn))
        return self, []

    def validate(self, db_conn):
        """
        Ensure the data presented matches the validations in the schema.
        Allow all data that is not specified in the schema.

        To limit database queries, first we do strict checks, which
        takes no lookups. Then we validate fields, which are unlikely to
        have lookups. Then we test unique, which we know will have one lookup
        each.

        To add model-level validations, extend this method, such as:

            def validate(self):
                errors = super().validate(db_conn)
                if not errors:
                    errors += self.validate_...()
                return errors
        """

        errors = []
        errors += self.enforce_strict_mode()
        if not errors:
            errors += self.validate_fields()
        if not errors:
            errors += self.test_unique(db_conn)
        return errors

    def enforce_strict_mode(self):
        """
        If strict mode, remove any fields that aren't part of the schema.

        For now, we'll just remove extra fields.
        Later, we might want an option to throw errors instead.
        """

        def _(data, schema):
            for name, field_schema in schema.items():
                if 'embed' in field_schema and name in data:
                    data[name] = _(data[name], field_schema['embed'])
                elif 'embed_many' in field_schema and name in data:
                    for i, d in enumerate(data[name]):
                        data[name][i] = _(d, field_schema['embed_many'])
            return pick(data, schema.keys())

        self.data = _(self.data, self.schema)
        return []

    def validate_fields(self):
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

        iter(_, self.data, self.schema)
        return errors

    def test_unique(self, db_conn):
        """
        Test all top-level fields marked as unique.
        """

        errors = []

        def _(data, field_name, field_schema, prefix):
            if ('unique' not in field_schema or
                    data.get(field_name) is None):
                return

            query = (self.table
                         .filter(r.row[field_name] == data.get(field_name))
                         .filter(r.row['id'] != self['id']))

            if len(list(query.run(db_conn))) > 0:
                errors.append({
                    'name': prefix + field_name,
                    'message': c('unique'),
                })

        iter(_, self.data, self.schema)
        return errors

    def defaults(self):
        """
        Set up defaults for data if not applied.
        """

        def _(data, field_name, field_schema, prefix):
            if 'default' in field_schema and data.get(field_name) is None:
                if hasattr(field_schema['default'], '__call__'):
                    data[field_name] = field_schema['default']()
                else:
                    data[field_name] = field_schema['default']

        iter(_, self.data, self.schema)
        return self.data

    def bundle(self):
        """
        Prepare the data for saving into the database.
        Consider default values and will call `bundle`
        in the schema if present.
        """

        def _(data, field_name, field_schema, prefix):
            if 'bundle' in field_schema and data.get(field_name):
                data[field_name] = field_schema['bundle'](data[field_name])

        data = deepcopy(self.data)
        iter(_, data, self.schema)
        return data

    def deliver(self, access=None):
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

        data = deepcopy(self.data)
        iter(_, data, self.schema)
        return data
