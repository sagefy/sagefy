import re


def required(field):
    """
    Given a doc and field, ensure the field is present on the model.
    """
    if field.get() is None:
        return 'Required.'


def boolean(field):
    """
    Ensure the given doc field is a boolean.
    """
    if not isinstance(field.get(), bool):
        return 'Must be true or false.'


def email(field):
    """
    Ensure the given field is formatted as an email
    """
    if not re.match(r'\S+@\S+\.\S+', field.get()):
        return 'Must be an email.'


def minlength(field, params):
    """
    Ensure the given field is a minimum length.
    """
    ln = params[0]
    if not field.get() or len(field.get()) < ln:
        return 'Minimum length of %s.' % ln
