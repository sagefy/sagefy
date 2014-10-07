"""
Short, one-off methods that could potentially be reused anywhere.
"""

import random
import string


def uniqid():
    """
    Generates a unique string with 16 characters.
    https://stackoverflow.com/a/2257449
    """
    return ''.join(
        random.choice(string.ascii_lowercase + string.ascii_uppercase +
                      string.digits)
        for i in range(16)
    )


def pick(d, keys):
    """
    Returns a dictionary with only the specified keys.
    """
    return {key: d[key] for key in keys if key in d}


def omit(d, keys):
    """
    Returns a dictionary without the specified keys.
    """
    return {key: d[key] for key in d if key not in keys}


def compact(a):
    """
    Returns an array with None removed.
    """
    return [b for b in a if b is not None]
