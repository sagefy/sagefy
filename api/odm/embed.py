from odm.field import Field


class Embeds(Field):
    """
    Allows a document to be embedded within another document directly.
    """

    def __init__(self, Doc, validations=(), default=None, access=True,
                 before_save=None):
        """
        Store initialized parameters onto self.
        """
        self.value = None
        self.Doc = Doc
        self.validations = validations
        self.default = default
        self.access = access
        self.before_save = before_save

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


class EmbedsMany(Embeds):
    """
    Allows for multiple documents of the same kind to be embedded
    into another document.
    """

    def __init__(self, Doc, validations=(), default=None, access=True,
                 before_save=None):
        """
        Store initialized parameters onto self.
        """
        self.value = []
        self.Doc = Doc
        self.validations = validations
        self.default = default
        self.access = access
        self.before_save = before_save

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
