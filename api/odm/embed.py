from odm.field import Field
from weakref import WeakKeyDictionary


class Embeds(Field):
    """
    Allows a document to be embedded within another document directly.
    """

    def __init__(self, doc, validations=(), default={}, access=True):
        """
        Store initialized parameters onto self.
        """
        self.data = WeakKeyDictionary()
        self.Doc = doc
        self.validations = validations
        self.default = default
        self.access = access
        self.unique = False

    def __set__(self, instance, value):
        """
        Set should update the fields on the document instead.
        """
        if not self.data.get(instance):
            self.data[instance] = self.Doc()
        self.data[instance].update_fields(value)

    def validate(self, instance):
        """
        Runs own validations, and then child field validations.
        """
        error = Field.validate(self, instance)
        if error:
            return error

        doc = self.__get__(instance, None)
        if doc is not None:
            errors = []
            for name, field in doc.get_fields():
                error = getattr(doc.__class__, name).validate(doc)
                if error:
                    errors.append({
                        'name': name,
                        'message': error,
                    })
            return errors

    def bundle(self, instance):
        """
        Gets the value for the database.
        Calls transform if applicable.
        Otherwise, its the same as `get`.
        """
        doc = self.__get__(instance, None)
        if doc:
            return {
                name: getattr(doc.__class__, name).bundle(doc)
                for name, field in doc.get_fields()
            }

    def deliver(self, instance, private=False):
        """
        Ensure if the data can be accessed.
        """
        doc = self.__get__(instance, None)
        if doc and (
            (self.access == 'private' and private) or self.access is True
        ):
            package = {}
            for name, field in doc.get_fields():
                value = getattr(doc.__class__, name).deliver(doc, private)
                if value is not None:
                    package[name] = value
            return package


class EmbedsMany(Embeds):
    """
    Allows for multiple documents of the same kind to be embedded
    into another document.
    """

    def __init__(self, doc, validations=(), default=[], access=True):
        """
        Store initialized parameters onto self.
        """
        self.data = WeakKeyDictionary()
        self.Doc = doc
        self.validations = validations
        self.default = default
        self.access = access
        self.unique = False

    def __set__(self, instance, value):
        """
        Set should update the fields in the documents instead.
        """
        if not self.data.get(instance):
            self.data[instance] = []
        for i, v in enumerate(value):
            if i >= len(self.data[instance]):
                self.data[instance].append(self.Doc())
            self.data[instance][i].update_fields(v)

    def validate(self, instance):
        """
        Runs own validations, and then child field validations.
        """
        error = Field.validate(self, instance)
        if error:
            return error

        docs = self.__get__(instance, None)
        if docs is not None:
            errors = []
            for doc in docs:
                for name, field in doc.get_fields():
                    error = getattr(doc.__class__, name).validate(doc)
                    if error:
                        errors.append({
                            'name': name,
                            'message': error,
                        })
            return errors

    def bundle(self, instance):
        """
        Gets the value for the database.
        Calls transform if applicable.
        Otherwise, its the same as `get`.
        """
        docs = self.__get__(instance, None)
        if docs:
            return [{
                name: getattr(doc.__class__, name).bundle(doc)
                for name, field in doc.get_fields()
            } for doc in docs]

    def deliver(self, instance, private=False):
        """
        Ensure if the data can be accessed.
        """
        docs = self.__get__(instance, None)
        if docs and (
            (self.access == 'private' and private) or self.access is True
        ):
            packages = []
            for doc in docs:
                package = {}
                for name, field in doc.get_fields():
                    value = getattr(doc.__class__, name).deliver(doc, private)
                    if value is not None:
                        package[name] = value
                packages.append(package)
            return packages
