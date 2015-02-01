"""
Short, one-off methods that could potentially be reused anywhere.
"""

import random
import string
import re


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


def parse_args(args):
    """
    Return a dict with the args parsed into types.
    """
    output = {}
    if not args:
        return output
    for key, value in args.items():
        if value == 'true':
            output[key] = True
        elif value == 'false':
            output[key] = False
        elif re.match(r'^\d+$', value):
            output[key] = int(value)
        elif re.match(r'^\d+\.\d+$', value):
            output[key] = float(value)
        else:
            output[key] = value
    return output


def get_first(dct, *keys):
    """
    Given a dictionary, find the value for the first available key in the
    list of keys. Otherwise, return none.
    """
    for key in keys:
        if key in dct:
            return dct[key]
    return None
