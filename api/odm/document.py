import inspect
from odm.field import Field


class Document(object):
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
        assert isinstance(fields, dict)
        errors = []
        for name, value in fields.items():
            if (hasattr(self, name) and
                    Document.isfield(getattr(self.__class__, name))):
                setattr(self, name, value)
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
        return inspect.getmembers(self.__class__, Document.isfield)

    def bundle(self):
        """
        Returns a dict form of the model's fields.
        Ready for going into the database.
        """
        return {
            name: getattr(self.__class__, name).bundle(self)
            for name, field in self.get_fields()
        }

    def deliver(self, private=False):
        """
        Returns a dict form of the model's fields.
        Only returns fields allowed.
        """
        package = {}
        for name, field in self.get_fields():
            value = getattr(self.__class__, name).deliver(self, private)
            if value is not None:
                package[name] = value
        return package

    def validate(self):
        """
        Validates own's fields.
        Returns model and errors if can't save it to the DB.
        """
        errors = []
        for name, field in self.get_fields():
            error = getattr(self.__class__, name).validate(self)
            if error:
                errors.append({
                    'name': name,
                    'message': error,
                })
        return errors
