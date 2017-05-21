"""
Short, one-off methods that could potentially be reused anywhere.
"""

from random import SystemRandom
import string
from datetime import datetime
import collections
import rethinkdb


random = SystemRandom()


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

    if isinstance(val, rethinkdb.ast.Now):
        return datetime.now().isoformat()

    return val


def json_prep(d):
    f = {}
    for key, value in d.items():
        if isinstance(value, collections.Mapping):
            f[key] = json_prep(value)
        else:
            f[key] = json_serial(value)
    return f


def extend(base, *injects):
    """
    Do a recursive extension of an object.
    http://stackoverflow.com/a/3233356
    TODO-2 Update so it doesn't change any input arguments
    """

    for injector in injects:
        for key, value in injector.items():
            if isinstance(value, collections.Mapping):
                _ = extend(base.get(key, {}), value)
                base[key] = _
            else:
                base[key] = injector[key]
    return base


def object_diff(prev, next_):
    """
    Return a description of the differences between two dicts.
    Assume the keys are the same either way.
    TODO-2 use this instead?
    https://blog.jcoglan.com/2017/02/12/the-myers-diff-algorithm-part-1/
    """

    diffs = set()

    def _(p, n, pre=''):
        for key, value in p.items():
            if p[key] != n[key]:
                if isinstance(value, collections.Mapping):
                    _(p[key], n[key], pre + key + '.')
                # TODO-3 handle lists/tuples
                else:
                    diffs.add(pre + key)

    _(prev, next_)

    return diffs
