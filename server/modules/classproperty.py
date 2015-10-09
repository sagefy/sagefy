class classproperty(object):  # flake8: noqa
    """
    Enable `instance.property` to call a function on reference.
    """


    def __init__(self, fn):
        """
        Set the property to refer to the function
        """

        self.fn = fn

    def __get__(self, ins, owner):
        """
        Call the property with the owner when reference.
        """

        return self.fn(owner)

    def __set__(self):
        """
        Disallow overriding property.
        """

        raise "Cannot set static class property."

    def __delete__(self):
        """
        Disallow removing property.
        """

        raise "Cannot delete static class property."
