import re
from modules.content import get as _


def is_required(value):
    """
    Ensure the value is present.
    """
    if value is None:
        return _('error', 'required')


def is_boolean(value):
    """
    Ensure the given value is a boolean.
    """
    if not (value is None or isinstance(value, bool)):
        return _('error', 'boolean')


def is_string(value):
    """Ensure the given value is a string."""
    if not (value is None or isinstance(value, str)):
        return _('error', 'string')


def is_language(value):
    """Entity must be ISO 639-1 code."""
    if not (value is None or
            (isinstance(value, basestring) or len(value) != 2)):
        return _('error', 'language')


def is_list(value):
    """Ensure the given value is a list."""
    if not (value is None or isinstance(value, list)):
        return _('error', 'list')


def is_email(value):
    """
    Ensure the given value is formatted as an email.
    """
    if not (value is None or re.match(r'\S+@\S+\.\S+', value)):
        return _('error', 'email')


def has_min_length(value, params):
    """
    Ensure the given value is a minimum length.
    """
    ln = params[0]
    if not value or len(value) < ln:
        return _('error', 'minlength').replace('{length}', str(ln))


def is_one_of(value, params):
    """
    Ensure the value is within an enumerated set.
    """
    if value not in params:
        return _('error', 'options').replace('{options}', ', '.join(params))
