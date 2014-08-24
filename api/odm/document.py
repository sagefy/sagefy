from copy import deepcopy
import inspect
from odm.field import Field


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
        self.init_fields()
        if fields:
            self.update_fields(fields)

    def init_fields(self):
        """
        Create new versions of each field.
        """
        for name, field in self.get_fields():
            setattr(self, name, deepcopy(field))

    def update_fields(self, fields):
        """
        For each field provided, set it to the model's field.
        Error if any field present not in model.
        """
        assert isinstance(fields, dict)
        errors = []
        for name, value in fields.iteritems():
            if (hasattr(self, name) and
                    Document.isfield(getattr(self, name))):
                getattr(self, name).set(value)
            else:
                errors.append({
                    'name': name,
                    'message': 'No such field.',
                })
        return self, errors

    @staticmethod
    def isfield(field):
        """
        Returns if a given entity is a field.
        """
        return isinstance(field, Field)

    def get_fields(self):
        """
        Returns a list of fields in the document.
        """
        return inspect.getmembers(self, Document.isfield)

    def bundle(self):
        """
        Returns a dict form of the model's fields.
        Ready for going into the database.
        """
        return {
            name: field.bundle()
            for name, field in self.get_fields()
        }

    def deliver(self, private=False):
        """
        Returns a dict form of the model's fields.
        Only returns fields allowed.
        """
        return {
            name: field.deliver(private)
            for name, field in self.get_fields()
            if field.deliver(private) is not None
        }

    def validate(self):
        """
        Validates own's fields.
        Returns model and errors if can't save it to the DB.
        """
        errors = []
        for name, field in self.get_fields():
            error = field.validate()
            if error:
                errors.append({
                    'name': name,
                    'message': error,
                })
        return errors
