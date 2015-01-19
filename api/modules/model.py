import rethinkdb as r
from flask import g
from modules.util import uniqid, omit, pick
from modules.content import get as _


def update_modified(field):
    return r.now()


class classproperty(object):  # flake8: noqa
    def __init__(self, fn):
        self.fn = fn

    def __get__(self, ins, owner):
        return self.fn(owner)

    def __set__(self):
        raise "Cannot set static class property."

    def __delete__(self):
        raise "Cannot delete static class property."


class Model(object):
    strict = True
    # strict = True will remove any fields not defined in the schema
    # to open up, either do strict = False or specify the field names in the
    # schema with an empty dict

    schema = {
        'id': {
            'default': uniqid
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
    # - validate
    # - bundle
    # - default
    # - deliver
    # - access
    # - unique

    def __init__(self, data=None):
        self.data = {}
        if data and self.strict:
            data = pick(data, self.schema.keys())
        if data:
            self.data.update(data)
        self.defaults()

    def __getitem__(self, key):
        return self.data.get(key)

    def __setitem__(self, key, value):
        self.data[key] = value

    def __delitem__(self, key):
        del self.data[key]

    def __contains__(self, item):
        return item in self.data

    @classproperty
    def table(self):
        assert self.tablename, 'You must provide a tablename.'
        return g.db.table(self.tablename)

    def validate(self):
        """
        Ensure the data presented matches the validations in the schema.
        Allows all data that is not specified in the schema.
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

    def defaults(self):
        """
        Sets up defaults for data if not applied.
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
        Prepares the data for saving into the database.
        Considers default values and will call `bundle`
        in the schema if present.
        """
        data = self.data.copy()

        for name, field_schema in self.schema.items():
            if 'bundle' in field_schema and data.get(name):
                data[name] = field_schema['bundle'](data[name])

        return data

    def deliver(self, access=None):
        """
        Prepares the data for consumption.
        Considers access allowed and will call `deliver`
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
        Returns None when there's no matching document.
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
        Returns empty array when no models match.
        """
        data_list = (cls.table
                        .filter(params)
                        .run(g.db_conn))
        return [cls(data) for data in data_list]

    @classmethod
    def insert(cls, data):
        """
        Creates a new model instance.
        Returns model and errors if failed.
        """
        assert isinstance(data, dict)
        data = omit(data, ('id', 'created', 'modified'))
        instance = cls(data)
        return instance.save()

    def update(self, data):
        """
        Update the model in the database.
        Returns model and errors if failed.
        """
        assert isinstance(data, dict)
        data = omit(data, ('id', 'created', 'modified'))
        self.data.update(data)
        return self.save()

    def save(self):
        """
        Inserts the model in the database.
        Returns model and errors if failed.
        """
        errors = self.validate()
        if len(errors):
            return self, errors
        errors = self.test_unique()
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
        Removes the model from the database.
        """
        (self.table
             .get(self['id'])
             .delete()
             .run(g.db_conn))
        return self, []

    def test_unique(self):
        """
        Tests all top-level fields marked as unique.
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
                    'message': _('error', 'unique'),
                })
        return errors
