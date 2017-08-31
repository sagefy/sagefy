import re
from modules.content import get as c


def is_required(value):
    """
    Ensure the value is present.
    """

    if value is None:
        return c('required')


def is_boolean(value):
    """
    Ensure the given value is a boolean.
    """

    if value is None:
        return

    if not isinstance(value, bool):
        return c('boolean')


def is_string(value):
    """
    Ensure the given value is a string.
    """

    if value is None:
        return

    if not isinstance(value, str):
        return c('string')


def is_number(value):
    """
    Ensure the given value is a number.
    """

    if value is None:
        return

    if not isinstance(value, (int, float)):
        return c('number')


def is_integer(value):
    """
    Ensure the given value is a integer.
    """

    if value is None:
        return

    if not isinstance(value, int):
        return c('integer')


def is_string_or_number(value):
    """
    Ensure the given value is a string or number.
    """

    if value is None:
        return

    if not isinstance(value, (str, int, float, complex)):
        return c('string_or_number')


def is_language(value):
    """
    Entity must be BPC 47 code.
    https://tools.ietf.org/rfc/bcp/bcp47.txt
    """

    if value is None:
        return

    if not isinstance(value, str) or len(value) != 2:
        return c('language')


def is_list(value):
    """
    Ensure the given value is a list.
    """

    if value is None:
        return

    if not isinstance(value, list):
        return c('list')


def is_dict(value):
    """
    Ensure the given value is a dict.
    """

    if value is None:
        return

    if not isinstance(value, dict):
        return c('dict')


def is_email(value):
    """
    Ensure the given value is formatted as an email.
    """

    if value is None:
        return

    if not re.match(r'\S+@\S+\.\S+', value):
        return c('email')


def is_url(value):
    """
    Ensure the given value is formatted as an URL.
    """

    if value is None:
        return

    if not re.match(r'^(http(s)?:)?//[^.]+\..+$', value):
        return c('url')


def has_min_length(value, ln):
    """
    Ensure the given value is a minimum length.
    """
    if value is None:
        return

    if not value or len(value) < ln:
        return c('minlength').replace('{length}', str(ln))


def has_max_length(value, ln):
    """
    Ensure the given value is a maximum length.
    """

    if value is None:
        return

    if not value or len(value) > ln:
        return c('maxlength').replace('{length}', str(ln))


def is_one_of(value, *options):
    """
    Ensure the value is within an enumerated set.
    """
    if value is None:
        return

    if value not in options:
        str_options = [str(o) for o in options]
        return (c('options')
                .replace('{options}', ', '.join(str_options)))


def is_list_of_strings(value):
    """
    Ensure the number is a list of strings.
    """

    if value is None:
        return

    if not isinstance(value, list):
        return c('list')

    for v in value:
        if not isinstance(v, str):
            return c('string')
