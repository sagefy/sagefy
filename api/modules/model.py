"""
Core model class, structures Rethink queries and caching.
"""
from flask import g
from modules.util import uniqid, pick, compact
import re

# TODO: created and modified


class Model:
    def __init__(self, fields):
        """
        Creates a new model instance given a set of fields.
        Does not store into the database, call `insert` to store into database.
        """
        assert self.tablename, 'You must provide a tablename.'
        self.table = g.db.table(self.tablename)

        assert self.schema, 'You must provide a schema.'
        self.fields = pick(fields or {}, self.schema.keys())

    @classmethod
    def get_table(cls):
        """
        For classmethods, a way to get the Model database table.
        Returns the table directly.
        """
        assert cls.tablename, 'You must provide a tablename.'
        return g.db.table(cls.tablename)

    @classmethod
    def get(cls, **params):
        """
        Given a set of parameters, fetchs a single model.
        Returns a Model instance if found, otherwise returns None.
        """
        if params.get('id'):
            fields = cls.get_table()\
                        .get(params.get('id'))\
                        .run(g.db_conn)
            # TODO: cache in Redis
        if fields:
            return cls(fields)

    @classmethod
    def list(cls, **params):
        """
        Given a set of paramaters, fetchs a list of models that match.
        Returns a list of Model instances if found, otherwise returns None.
        """
        fields_list = cls.get_table()\
                         .filter(params)\
                         .run(g.db_conn)
        if fields_list:
            return [cls(fields) for fields in fields_list]
            # TODO: cache each in Redis

    def insert(self):
        """
        Stores the fields to the database.
        Takes no arguments.
        Returns a True if succeeded.
        Returns False and a list of errors if failed.
        """
        if not self.fields.get('id'):
            self.fields['id'] = uniqid()
        valid, errors = self.validate()
        if valid:
            self.table.insert(self.fields).run(g.db_conn)
            # TODO: clear Redis cache
            return True, []
        else:
            return False, errors

    def update(self):
        """
        Updates the model in the database.
        Takes no fields.
        Updates the database fields.
        Returns a True if succeeded.
        Returns False and a list of errors if failed.
        """
        valid, errors = self.validate()
        if valid:
            self.table\
                .get(self.fields.get('id'))\
                .update(self.fields)\
                .run(g.db_conn)
            # TODO: clear cache in Redis
            return True, []
        else:
            return False, errors

    def delete(self):
        """
        Removes the instance.
        Removes from the database and sets the fields to None.
        Returns a True if succeeded.
        Returns False and a list of errors if failed.
        """
        self.table\
            .get(self.fields.get('id'))\
            .delete()\
            .run(g.db_conn)
        # TODO: clear cache in Redis
        self.fields = None
        return True, []

    def get_fields(self):
        """
        Returns a dict representation of the model for outputting to JSON.
        Defaults to returning all fields.
        Overwrite to limit the fields that are returned based on context.
        """
        return self.fields

    def validate(self):
        """
        Validate fields before insert or update.
        Return of
            1) whether the fields are valid and
            2) a list of errors, formatted as {name: , message: }
        """
        errors = []
        for key, qualities in self.schema.iteritems():
            errors.append(
                self.validate_field(
                    key,
                    qualities.get('validations', [])
                )
            )
        errors = compact(errors)
        if errors:
            return False, errors
        return True, []

    def validate_field(self, key, validations):
        """

        """
        message = None
        for validation in validations:
            if isinstance(validation, (list, tuple)):
                fn_name = 'test_%s' % validation[0]
                args = validation[1:]
            else:
                fn_name = 'test_%s' % validation
                args = ()
            message = getattr(self, fn_name)(key, *args)
            if message:
                return {'name': key, 'message': message}

    def test_required(self, key):
        """

        """
        if self.fields.get(key) is None:
            return "%s is required" % key

    def test_unique(self, key):
        """

        """
        value = self.fields.get(key)
        result = self.table.filter({key: value}).limit(1).run(g.db_conn)
        if [u for u in result]:
            return "%s must be unique" % key

    def test_email(self, key):
        """

        """
        value = self.fields.get(key)
        if not re.match(r'\S+@\S+\.\S+', value):
            return "%s must be an email" % key

    def test_minlength(self, key, length):
        """

        """
        value = self.fields.get(key)
        if len(value) < length:
            return "%s requires at least %s characters" % ()
