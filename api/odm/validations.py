import re


def is_required(value):
    """
    Ensure the value is present.
    """
    if value is None:
        return 'Required.'


def is_boolean(value):
    """
    Ensure the given value is a boolean.
    """
    if not isinstance(value, bool):
        return 'Must be true or false.'


def is_string(value):
    """Ensure the given value is a string."""
    if not isinstance(value, basestring):
        return 'Must be a string.'


def is_list(value):
    """Ensure the given value is a list."""
    if not isinstance(value, list):
        return 'Must be a list.'


def is_email(value):
    """
    Ensure the given value is formatted as an email.
    """
    if not re.match(r'\S+@\S+\.\S+', value):
        return 'Must be an email.'


def has_min_length(value, params):
    """
    Ensure the given value is a minimum length.
    """
    ln = params[0]
    if not value or len(value) < ln:
        return 'Minimum length of %s.' % ln
