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
        self.default = default
        self.access = access if access is not None else True
        self.before_save = before_save

    def get(self):
        """
        Gets the fields value.
        Returns set value, default, or None.
        """
        if self.value is None and self.default is not None:
            if hasattr(self.default, '__call__'):
                return self.default()
            return self.default
        return self.value

    def to_database(self):
        """
        Gets the value for the database.
        Calls before_save if applicable.
        Otherwise, its the same as `get`.
        """
        # if self.before_save and hasattr(self.before_save, '__call__'):
            # return self.before_save()
        return self.get()

    def set(self, value):
        """
        Sets the value.
        Will use default if set to None.
        """
        if value is None and self.default is not None:
            if hasattr(self.default, '__call'):
                self.value = self.default()
            self.value = self.default
        self.value = value
        return self

    # TODO: is there a way to use __get__, __set__, __delete__, __getattr__ ...
    # so we don't have to do `field.get()` and `field.set(value)` all the time?

    def validate(self, instance, name):
        """
        Validates the field using given validations.
        Returns a string if a validation fails.
        Otherwise returns None.
        """
        for validation in self.validations:
            if isinstance(validation, (list, tuple)):
                error = validation[0](doc=instance, name=name,
                                      params=validation[1:])
            else:
                error = validation(doc=instance, name=name)
            if error:
                return error
