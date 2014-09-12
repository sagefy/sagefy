from weakref import WeakKeyDictionary


class Field(object):
    """
    A single field (aka column),
    either in a document or in an embedded document.
    """

    def __init__(self, validations=(), default=None, access=True,
                 transform=None, unique=False):
        """
        Initialize Field.
        Sets to self the following keyword arguments:
        - validations
        - default
        - access
        - transform
        """
        self.data = WeakKeyDictionary()
        self.validations = validations
        self.default = default
        self.access = access
        self.transform = transform
        self.unique = unique

    def __get__(self, instance, owner):
        """
        Gets the fields value.
        Returns set value, default, or None.
        """
        if instance is None:  # Allows us to super into the value
            return self
        value = self.data.get(instance)
        if value is None and self.default is not None:
            if hasattr(self.default, '__call__'):
                return self.default()
                # Methods defined outside a class, even if refered to,
                # still do not automatically receive `self`
            return self.default
        return value

    def __set__(self, instance, value):
        """
        Sets the value.
        Will use default on `get` if set to None.
        """
        self.data[instance] = value

    def validate(self, instance):
        """
        Validates the field using given validations.
        Returns a string if a validation fails.
        Otherwise returns None.
        """
        value = self.__get__(instance, None)
        for validation in self.validations:
            if isinstance(validation, (list, tuple)):
                error = validation[0](value, params=validation[1:])
            else:
                error = validation(value)
            if error:
                return error

    def bundle(self, instance):
        """
        Gets the value for the database.
        Calls transform if applicable.
        Otherwise, its the same as `get`.
        """
        value = self.__get__(instance, None)
        if self.transform and hasattr(self.transform, '__call__'):
            return self.transform(value)
        return value

    def deliver(self, instance, private=False):
        """
        Ensure if the data can be accessed.
        """
        if (self.access == 'private' and private) or self.access is True:
            return self.__get__(instance, None)
