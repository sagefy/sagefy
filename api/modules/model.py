import rethinkdb as r
from flask import g
from modules.util import uniqid, omit, pick
from modules.content import get as c
from modules.classproperty import classproperty


def update_modified(field):
    return r.now()


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
    # - validate: a list of functions to run on the field.
    #             return a string if error, None if okay
    # - bundle:   before saving to the database,
    #             transform the data
    # - default:  default value of the field
    #             can be a value or a function to call
    # - deliver:  tranform the data before sending out to the client
    #             can also be used for permissions
    # - access:   control which client can access this field's information
    # - unique:   True will check to make sure no other row has the same value
    #             not needed on `id` field, as it is the primary key

    indexes = ()
    # A list of indexes for the table

    validations = ()
    # A list of methods to run before saving,
    # which can check class-level characteristics on the model

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
        return g.db.table(self.tablename)

    def validate(self):
        """
        Ensure the data presented matches the validations in the schema.
        Allow all data that is not specified in the schema.
        """

        # To limit database queries, first we do strict checks, which
        # takes no lookups. Then we validate fields, which are unlikely to
        # have lookups. Then we test unique, which we know will have one lookup
        # each. Finally we validate extras, which are likely to have multiple
        # lookups.

        errors = []
        errors += self.enforce_strict_mode()
        if not errors:
            errors += self.validate_fields()
        if not errors:
            errors += self.test_unique()
        if not errors:
            errors += self.validate_extras()
        return errors

    def enforce_strict_mode(self):
        """
        If strict mode, remove any fields that aren't part of the schema
        """

        if self.strict:
            self.data = pick(self.data, self.schema.keys())

        return []
        # For now, we'll just remove extra fields
        # Later, we might want an option to throw errors instead

    def validate_fields(self):
        """
        Iterate over the schema, ensuring that everything matches up.
        """

        errors = []
        for name, field_schema in self.schema.items():
            if 'validate' in field_schema:
                for fn in field_schema['validate']:
                    if isinstance(fn, (list, tuple)):
                        error = fn[0](self[name], *fn[1:])
                    else:
                        error = fn(self[name])
                    if error:
                        errors.append({
                            'name': name,
                            'message': error,
                        })
                        break
        return errors

    def validate_extras(self):
        """
        Finally, run any class level validations.
        """

        errors = []
        for name, fn in self.validations:
            error = fn(self)
            if error:
                errors.append({
                    'name': name,
                    'message': error,
                })
        return errors

    def defaults(self):
        """
        Set up defaults for data if not applied.
        """

        for name, field_schema in self.schema.items():
            if 'default' in field_schema and self.data.get(name) is None:
                if hasattr(field_schema['default'], '__call__'):
                    self.data[name] = field_schema['default']()
                else:
                    self.data[name] = field_schema['default']
        return self.data

    def bundle(self):
        """
        Prepare the data for saving into the database.
        Consider default values and will call `bundle`
        in the schema if present.
        """

        data = self.data.copy()

        for name, field_schema in self.schema.items():
            if 'bundle' in field_schema and data.get(name):
                data[name] = field_schema['bundle'](data[name])

        return data

    def deliver(self, access=None):
        """
        Prepare the data for consumption.
        Consider access allowed and will call `deliver`
        in the schema if present.
        """

        data = self.data.copy()

        for name, field_schema in self.schema.items():
            if 'access' in field_schema and data.get(name):
                if field_schema['access'] != access:
                    del data[name]

            if 'deliver' in field_schema and data.get(name):
                data[name] = field_schema['deliver'](data[name])

        return data

    @classmethod
    def get(cls, **params):
        """
        Get one model which matches the provided keyword arguments.
        Return None when there's no matching document.
        """

        data = None
        if params.get('id'):
            data = (cls.table
                       .get(params.get('id'))
                       .run(g.db_conn))
        else:
            data = list(cls.table
                           .filter(params)
                           .limit(1)
                           .run(g.db_conn))
            if len(data) > 0:
                data = data[0]
            else:
                data = None
        if data:
            return cls(data)

    @classmethod
    def list(cls, **params):
        """
        Get a list of models matching the provided keyword arguments.
        Return empty array when no models match.
        """

        data_list = (cls.table
                        .filter(params)
                        .run(g.db_conn))
        return [cls(data) for data in data_list]

    @classmethod
    def insert(cls, data):
        """
        Create a new model instance.
        Return model and errors if failed.
        """

        assert isinstance(data, dict)
        data = omit(data, ('id', 'created', 'modified'))
        instance = cls(data)
        return instance.save()

    def update(self, data):
        """
        Update the model in the database.
        Return model and errors if failed.
        """

        assert isinstance(data, dict)
        data = omit(data, ('id', 'created', 'modified'))
        self.data.update(data)
        return self.save()

    def save(self):
        """
        Insert the model in the database.
        Return model and errors if failed.
        """

        errors = self.validate()
        if len(errors):
            return self, errors
        data = self.bundle()
        self.id = data['id']
        self.table.insert(data, conflict='update').run(g.db_conn)
        self.sync()
        return self, []

    def sync(self):
        """
        Pull the fields from the database.
        """

        data = (self.table
                    .get(self['id'])
                    .run(g.db_conn))
        self.data.update(data)
        return self

    def delete(self):
        """
        Remove the model from the database.
        """

        (self.table
             .get(self['id'])
             .delete()
             .run(g.db_conn))
        return self, []

    def test_unique(self):
        """
        Test all top-level fields marked as unique.
        """

        errors = []
        for name, value in self.data.items():
            if 'unique' not in self.schema[name]:
                continue
            query = (self.table
                         .filter(lambda m: (m[name] == value) &
                                           (m['id'] != self['id'])))
            entries = list(query.run(g.db_conn))
            if len(entries) > 0:
                errors.append({
                    'name': name,
                    'message': c('error', 'unique'),
                })
        return errors
