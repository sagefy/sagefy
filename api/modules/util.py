"""
Short, one-off methods that could potentially be reused anywhere.
"""

import random
import string
from datetime import datetime


def uniqid():
    """
    Generate a unique string with 24 characters.
    https://stackoverflow.com/a/2257449
    """
    return ''.join(
        random.choice(string.ascii_lowercase
                      + string.ascii_uppercase
                      + string.digits)
        for i in range(24)
    )


def pick(d, keys):
    """
    Return a dictionary with only the specified keys.
    """
    return {key: d[key] for key in keys if key in d}


def omit(d, keys):
    """
    Return a dictionary without the specified keys.
    """
    return {key: d[key] for key in d if key not in keys}


def compact(a):
    """
    Return an array with None removed.
    """
    return [b for b in a if b is not None]


def compact_dict(d):
    """
    Return a dict with None removed.
    """
    return {k: v for k, v in d.items() if v is not None}


def get_first(dct, *keys):
    """
    Given a dictionary, find the value for the first available key in the
    list of keys. Otherwise, return none.
    """
    for key in keys:
        if key in dct:
            return dct[key]
    return None


def json_serial(val):
    """
    Tell `json.dumps` how to convert non-JSON types.
    """

    if isinstance(val, datetime):
        return val.isoformat()
