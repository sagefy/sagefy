class Field:
    """
    A single field (aka column),
    either in a document or in an embedded document.
    """

    def __init__(self, validations=None, default=None, access=None,
                 before_save=None, unique=False):
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
        self.default = default
        self.access = access if access is not None else True
        self.before_save = before_save
        self.unique = unique

    def get(self):
        """
        Gets the fields value.
        Returns set value, default, or None.
        """
        if self.value is None and self.default is not None:
            if hasattr(self.default, '__call__'):
                return self.default(self)
                # Methods defined outside a class,
                # even if refered to,
                # still do not automatically receive `self`
            return self.default
        return self.value

    def to_database(self):
        """
        Gets the value for the database.
        Calls before_save if applicable.
        Otherwise, its the same as `get`.
        """
        if self.before_save and hasattr(self.before_save, '__call__'):
            return self.before_save(self)
        return self.get()

    def to_json(self):
        """
        Ensure if the data can be accessed.
        """
        if hasattr(self.access, '__call__'):
            if self.access(self):
                return self.get()
        elif self.access:
            return self.get()

    def set(self, value):
        """
        Sets the value.
        Will use default on `get` if set to None.
        """
        self.value = value
        return self

    # TODO: is there a way to use __get__, __set__, __delete__, __getattr__ ...
    # so we don't have to do `field.get()` and `field.set(value)` all the time?

    def validate(self):
        """
        Validates the field using given validations.
        Returns a string if a validation fails.
        Otherwise returns None.
        """
        for validation in self.validations:
            if isinstance(validation, (list, tuple)):
                error = validation[0](self, params=validation[1:])
            else:
                error = validation(self)
            if error:
                return error
