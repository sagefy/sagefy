import re


def required(value):
    """
    Ensure the value is present.
    """
    if value is None:
        return 'Required.'


def boolean(value):
    """
    Ensure the given value is a boolean.
    """
    if not isinstance(value, bool):
        return 'Must be true or false.'


def email(value):
    """
    Ensure the given value is formatted as an email.
    """
    if not re.match(r'\S+@\S+\.\S+', value):
        return 'Must be an email.'


def minlength(value, params):
    """
    Ensure the given value is a minimum length.
    """
    ln = params[0]
    if not value or len(value) < ln:
        return 'Minimum length of %s.' % ln
