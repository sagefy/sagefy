"""
Core model class, structures Rethink queries and caching.
"""
from flask import g
from modules.util import uniqid, pick, compact
import re
import rethinkdb as r


class Model:
    def __init__(self, fields):
        """
        Creates a new model instance given a set of fields.
        Does not store into the database, call `insert` to store into database.
        """
        assert self.tablename, 'You must provide a tablename.'
        self.table = g.db.table(self.tablename)
        self.fields = fields or {}

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
        fields = None
        if params.get('id'):
            fields = cls.get_table()\
                        .get(params.get('id'))\
                        .run(g.db_conn)
        else:
            fields = cls.get_table()\
                        .filter(params)\
                        .limit(1)\
                        .run(g.db_conn)
            fields = list(fields)[0]
        if fields:
            return cls(fields)

    @classmethod
    def list(cls, **params):
        """
        Given a set of paramaters, fetchs a list of models that match.
        Returns a list of Model instances if found, otherwise returns [].
        """
        fields_list = cls.get_table()\
                         .filter(params)\
                         .run(g.db_conn)
        if fields_list:
            return [cls(fields) for fields in fields_list]

    def insert(self):
        """
        Stores the fields to the database.
        Takes no arguments.
        Returns a True if succeeded.
        Returns False and a list of errors if failed.
        """
        valid, errors = self.validate()
        if valid:
            self.tidy_fields()
            self.table.insert(self.fields).run(g.db_conn)
            self.sync_fields()
            return True, []
        else:
            return False, errors

    def update(self, fields):
        """
        Updates the model in the database.
        Takes no fields.
        Updates the database fields.
        Returns a True if succeeded.
        Returns False and a list of errors if failed.
        """
        self.fields.update(fields)
        valid, errors = self.validate()
        if valid:
            self.tidy_fields()
            self.table\
                .get(self.fields.get('id'))\
                .update(self.fields)\
                .run(g.db_conn)
            self.sync_fields()
            return True, []
        else:
            return False, errors

    def sync_fields(self):
        """
        Get fields updated to what is actually in the database.
        """
        self.fields = self.table.get(self.fields.get('id')).run(g.db_conn)

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
        self.fields = None
        return True, []

    def get_fields(self):
        """
        Returns a dict representation of the model for outputting to JSON.
        Defaults to returning all fields.
        Overwrite to change.
        """
        return self.fields

    def tidy_fields(self):
        """
        Only allow fields specified in the schema.
        """

        # Add in generic fields
        if not self.fields.get('id'):
            self.fields['id'] = uniqid()
        if not self.fields.get('created'):
            self.fields['created'] = r.now()
        self.fields['modified'] = r.now()

        # Only allow fields specified in the schema.
        assert self.schema, 'You must provide a schema.'
        keys = self.schema.keys() + ['id', 'created', 'modified']
        # TODO: handle subfields
        self.fields = pick(self.fields, keys)

        # Update password if needed
        if (
            self.fields.get('password') and
            not self.fields['password'].startswith('$2a$')
        ):
            self.encrypt_password()

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
        Given a field key and a list of validations,
        ensure the field matches the specification.
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
        Ensure the field exists.
        None if okay, String if failed.
        """
        if self.fields.get(key) is None:
            return "%s is required" % key

    def test_unique(self, key):
        """
        Ensure field is unique in database.
        None if okay, String if failed.
        """
        value = self.fields.get(key)
        entries = list(self.table
                           .filter({key: value})
                           .filter(r.row['id'] != self.fields.get('id'))
                           .run(g.db_conn))
        if entries:
            return "%s must be unique" % key

    def test_email(self, key):
        """
        Ensure field is formatted like an email address.
        None if okay, String if failed.
        """
        value = self.fields.get(key)
        if not re.match(r'\S+@\S+\.\S+', value):
            return "%s must be an email" % key

    def test_minlength(self, key, length):
        """
        Ensure field has minimum length.
        None if okay, String if failed.
        """
        value = self.fields.get(key)
        if len(value) < length:
            return "%s requires at least %s characters" % (key, length)
