from odm.field import Field


class Embeds(Field):
    """
    Allows a document to be embedded within another document directly.
    """

    def __init__(self, Doc, validations=(), default=None, access=True):
        """
        Store initialized parameters onto self.
        """
        self.value = None
        self.Doc = Doc
        self.validations = validations
        self.default = default
        self.access = access
        self.unique = False

    def set(self, value):
        """
        Set should update the fields on the document instead.
        """
        if not self.value:
            self.value = self.Doc()
        self.value.update_fields(value)

    def validate(self):
        """
        Runs own validations, and then child field validations.
        """
        error = Field.validate(self)
        if error:
            return error

        if self.value is not None:
            errors = []
            for name, field in self.value.get_fields():
                error = field.validate()
                if error:
                    errors.append({
                        'name': name,
                        'message': error,
                    })
            return errors

    def bundle(self):
        """
        Gets the value for the database.
        Calls before_save if applicable.
        Otherwise, its the same as `get`.
        """
        if self.value:
            return {
                name: field.bundle()
                for name, field in self.value.get_fields()
            }

    def deliver(self, private=False):
        """
        Ensure if the data can be accessed.
        """
        if self.value and (
            (self.access == 'private' and private) or self.access is True
        ):
            return {
                name: field.deliver(private)
                for name, field in self.value.get_fields()
                if field.deliver(private) is not None
            }


class EmbedsMany(Embeds):
    """
    Allows for multiple documents of the same kind to be embedded
    into another document.
    """

    def __init__(self, Doc, validations=(), default=None, access=True):
        """
        Store initialized parameters onto self.
        """
        self.value = []
        self.Doc = Doc
        self.validations = validations
        self.default = default
        self.access = access
        self.unique = False

    def set(self, value):
        """
        Set should update the fields in the documents instead.
        """
        for i, v in enumerate(value):
            if i >= len(self.value):
                self.value.append(self.Doc())
            self.value[i].update_fields(v)

    def validate(self):
        """
        Runs own validations, and then child field validations.
        """
        error = Field.validate(self)
        if error:
            return error

        if self.value is not None:
            errors = []
            for doc in self.value:
                for name, field in doc.get_fields():
                    error = field.validate()
                    if error:
                        errors.append({
                            'name': name,
                            'message': error,
                        })
            return errors

    def bundle(self):
        """
        Gets the value for the database.
        Calls before_save if applicable.
        Otherwise, its the same as `get`.
        """
        if self.value:
            return [{
                name: field.bundle()
                for name, field in v.get_fields()
            } for v in self.value]

    def deliver(self, private=False):
        """
        Ensure if the data can be accessed.
        """
        if self.value and (
            (self.access == 'private' and private) or self.access is True
        ):
            return [{
                name: field.deliver(private)
                for name, field in v.get_fields()
                if field.deliver(private) is not None
            } for v in self.value]
