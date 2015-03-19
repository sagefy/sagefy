import re
from modules.content import get as c


def is_required(value):
    """
    Ensure the value is present.
    """

    if value is None:
        return c('error', 'required')


def is_boolean(value):
    """
    Ensure the given value is a boolean.
    """

    if value is None:
        return

    if not isinstance(value, bool):
        return c('error', 'boolean')


def is_string(value):
    """
    Ensure the given value is a string.
    """

    if value is None:
        return

    if not isinstance(value, str):
        return c('error', 'string')


def is_number(value):
    """
    Ensure the given value is a number.
    """

    if value is None:
        return

    if not isinstance(value, (int, float, complex)):
        return c('error', 'number')


def is_string_or_number(value):
    """
    Ensure the given value is a string or number.
    """

    if value is None:
        return

    if not isinstance(value, (str, int, float, complex)):
        return c('error', 'string_or_number')


def is_language(value):
    """
    Entity must be ISO 639-1 code.
    """

    if value is None:
        return

    if not isinstance(value, str) or len(value) != 2:
        return c('error', 'language')


def is_list(value):
    """
    Ensure the given value is a list.
    """

    if value is None:
        return

    if not isinstance(value, list):
        return c('error', 'list')


def is_email(value):
    """
    Ensure the given value is formatted as an email.
    """

    if value is None:
        return

    if not re.match(r'\S+@\S+\.\S+', value):
        return c('error', 'email')


def is_url(value):
    """
    Ensure the given value is formatted as an URL.
    """

    if value is None:
        return

    if not re.match(r'^(http(s)?:)?//[^.]+\..+$', value):
        return c('error', 'url')


def has_min_length(value, ln):
    """
    Ensure the given value is a minimum length.
    """
    if value is None:
        return

    if not value or len(value) < ln:
        return c('error', 'minlength').replace('{length}', str(ln))


def is_one_of(value, *options):
    """
    Ensure the value is within an enumerated set.
    """
    if value is None:
        return

    if value not in options:
        str_options = [str(o) for o in options]
        return (c('error', 'options')
                .replace('{options}', ', '.join(str_options)))


def is_list_of_strings(value):
    """
    Ensure the number is a list of strings.
    """

    if value is None:
        return

    if not isinstance(value, list):
        return c('error', 'list')

    for v in value:
        if not isinstance(v, str):
            return c('error', 'string')
