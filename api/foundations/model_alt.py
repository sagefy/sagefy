import rethinkdb as r
from flask import g
import re
import inspect
from modules.util import uniqid


### EMBEDDING #################################################################


class EmbeddedDocument:
    def __init__(self, Doc):
        self.Doc = Doc


class ManyEmbeddedDocument(EmbeddedDocument):
    def __init__(self, Doc):
        self.Doc = Doc


def has(Doc):
    """
    Allows a document to be embedded within another document directly.
    """
    return EmbeddedDocument(Doc)


def has_many(Doc):
    """
    Allows for multiple documents of the same kind to be embedded
    into another document.
    """
    return ManyEmbeddedDocument(Doc)


### VALIDATIONS ###############################################################

def required(doc, field_name, field):
    """
    Given a doc and field, ensure the field is present on the model.
    """
    if field.value is None:
        return 'Required.'


def unique(doc, field_name, field):
    """
    Ensure the given doc field is unique.
    """
    other = doc.table.filter({
        r.row[field_name]: field.value
    }).run(g.db_conn)
    if other:
        return 'Must be unique.'


def boolean(doc, field_name, field):
    """
    Ensure the given doc field is a boolean.
    """
    if not isinstance(field.value, bool):
        return 'Must be true or false.'


def email(doc, field_name, field):
    """
    Ensure the given field is formatted as an email
    """
    if not re.match(r'\S+@\S+\.\S+', field.value):
        return 'Must be an email.'


def minlength(doc, field_name, field, ln):
    """
    Ensure the given field is a minimum length.
    """
    if len(field.value) < ln:
        return 'Must be at least %s characters.' % ln


### CORE CLASSES ##############################################################


class Field:
    """
    A single field (aka column),
    either in a document or in an embedded document.
    """

    def __init__(self, validations=None, default=None, access=None,
                 before_save=None):
        """
        Initialize Field.
        Sets to self the following keyword arguments:
        - validations
        - default
        - access
        - before_save
        """
        self.value = None
        self.validations = validations or ()
        self.default = default or None
        self.access = access or True
        self.before_save = before_save

    def __get__(self, instance, owner):
        """
        When accessing as an attribute, return value instead.
        """
        if self.default is not None and self.value is None:
            if hasattr(self.default, '__call__'):
                return self.default()
            return self.default
        return self.value

    def __set__(self, instance, value):
        """
        When setting as an attribute, set the value instead.
        """
        if self.default is not None and value is None:
            if hasattr(self.default, '__call__'):
                value = self.default()
            value = self.default
        self.value = value

    def __delete__(self, instance):
        """
        When deleting as an attribute, set the value to default
        or None instead.
        """
        if self.default is not None:
            if hasattr(self.default, '__call__'):
                return self.default()
            return self.default
        self.value = None

    def validate(self, instance, field_name):
        """
        Validates the field using given validations.
        Returns a string if a validation fails.
        Otherwise returns None.
        """
        for validation in self.validations:
            if isinstance(validation, (list, tuple)):
                error = validation[0](doc=instance, field_name=field_name,
                                      field=self, *validation[1:])
            else:
                error = validation(doc=instance, field_name=field_name,
                                   field=self)
            if error:
                return error


class Document:
    """
    A representation of a document.
    Unless its also a model, has no knowledge of the database.
    """
    def __init__(self, fields=None):
        """
        Takes a set of fields, and update self with them.
        Otherwise, its just a blank new instance.
        """
        if fields:
            self.update_fields(fields)

    def update_fields(self, fields):
        """
        For each field provided, set it to the model's field.
        Error if any field present not in model.
        """
        errors = []
        for field, value in fields.iteritems():
            if hasattr(self, field):
                setattr(self, field, value)
            else:
                errors.append('No field %s.' % field)
        return self, errors

    def get_fields(self):
        """
        Returns a list of fields in the document.
        """
        return [a for a in inspect.getmembers(self) if isinstance(a, Field)]

    def to_dict(self, all=False):
        """
        Returns a dict form of the model's fields.
        Only returns fields allowed.
        """
        dict = {}
        for name, field in self.get_fields():
            if (field.access is True or
                    (hasattr(field.access, '__call__') and field.access())):
                dict[name] = field.value
        return dict

    def validate(self):
        """
        Validates own's fields.
        Returns model and errors if can't save it to the DB.
        """
        errors = []
        for name, field in self.get_fields():
            error = field.validate(self, name)
            if error:
                errors.append({
                    'name': name,
                    'message': error,
                })
        return errors


def update_modified():
    return r.now()


class Model(Document):
    """
    Extends the Document to add database-oriented methods.
    """

    id = Field(
        default=uniqid,
        validations=(required, unique)
    )
    created = Field(
        default=r.now(),
    )
    modified = Field(
        default=r.now(),
        before_save=update_modified
    )

    def __init__(self, fields=None):
        """
        Creates a new model instance given a set of fields.
        Does not store into the database, call `save` to store into database.
        """
        assert self.tablename, 'You must provide a tablename.'
        self.table = g.db.table(self.tablename)
        Document.__init__(self, fields)

    @classmethod
    def get_table(cls):
        """
        For classmethods, a way to get the Model database table.
        Returns the table directly.
        """
        assert cls.tablename, 'You must provide a tablename.'
        return g.db.table(cls.tablename)

    @classmethod
    def get(Cls, **params):
        """
        Get one model which matches the provided keyword arguments.
        Returns None when there's no matching document.
        """
        fields = None
        if params.get('id'):
            fields = Cls.get_table()\
                        .get(params.get('id'))\
                        .run(g.db_conn)
        else:
            fields = list(Cls.get_table()
                             .filter(params)
                             .limit(1)
                             .run(g.db_conn))[0]
        if fields:
            return Cls(fields)

    @classmethod
    def list(Cls, **params):
        """
        Get a list of models matching the provided keyword arguments.
        Returns empty array when no models match.
        """
        fields_list = Cls.get_table()\
                         .filter(params)\
                         .run(g.db_conn)
        return [Cls(fields) for fields in fields_list]

    @classmethod
    def insert(Cls, fields):
        """
        Creates a new model instance.
        Returns model and errors if failed.
        """
        instance = Cls(fields)
        return instance.save()

    def update(self, fields):
        """
        Update the model in the database.
        Returns model and errors if failed.
        """
        self.fields.update(fields)
        return self.save()

    def save(self):
        """
        Inserts the model in the database.
        Returns model and errors if failed.
        """
        errors = self.validate()
        if len(errors):
            return self, errors
        self.table.insert(self.get_fields(), upsert=True).run(g.db_conn)
        self.sync()
        return self, []

    def sync(self):
        """
        Pull the fields from the database.
        """
        fields = self.table\
                     .get(self.id)\
                     .run(g.db_conn)
        self.update_fields(fields)
        return self

    def delete(self):
        """
        Removes the model from the database.
        """
        self.table\
            .get(self.id)\
            .delete()\
            .run(g.db_conn)
        self.fields = None
        return self, []
