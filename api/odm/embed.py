from odm.field import Field


class EmbeddedDocument(Field):
    def __init__(self, Doc, validations=None, default=None, access=None,
                 before_save=None):
        self.value = None
        self.Doc = Doc
        self.validations = validations or ()
        self.default = default
        self.access = access if access is not None else True
        self.before_save = before_save

    def get(self):
        if self.value:
            return self.value.to_database()

    def set(self, value):
        self.value = value

    def validate(self, instance, name):
        pass


class ManyEmbeddedDocument(EmbeddedDocument):
    def __init__(self, Doc, validations=None, default=None, access=None,
                 before_save=None):
        self.value = []
        self.Doc = Doc
        self.validations = validations or ()
        self.default = default
        self.access = access if access is not None else True
        self.before_save = before_save

    def get(self, index):
        if index:
            return self.value[index].to_database()
        return [d.to_database() for d in self.value]

    def set(self, index, value):
        if index:
            self.value[index] = value
        else:
            self.value = value
        return self

    def validate(self, instance, name):
        pass


def has(Doc, validations=None, default=None, access=None, before_save=None):
    """
    Allows a document to be embedded within another document directly.
    """
    return EmbeddedDocument(Doc, validations, default, access, before_save)


def has_many(Doc, validations=None, default=None, access=None,
             before_save=None):
    """
    Allows for multiple documents of the same kind to be embedded
    into another document.
    """
    return ManyEmbeddedDocument(Doc, validations, default, access, before_save)
