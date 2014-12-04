from modules import util
import string


def test_uniqid_length():
    # Expect the length of the ID to be 32
    assert len(util.uniqid()) is 16


def test_uniqid_charset():
    # Expect the ID to only have numbers and letters (mixed case)
    uid = util.uniqid()
    for c in uid:
        assert c in (string.ascii_lowercase + string.ascii_uppercase +
                     string.digits)


def test_pick():
    # Expect pick to make a new dict with only keys presented
    d = {'a': 1, 'b': 2}
    keys = ('a',)
    assert util.pick(d, keys) == {'a': 1}
    assert d == {'a': 1, 'b': 2}


def test_compact():
    # Expect compact to remove None from an array
    a = [1, None, 3, None]
    assert util.compact(a) == [1, 3]


def test_parse_args():
    """
    Expect to take a dict of args, all strings, and convert to appropriate
    types.
    """
    args = {
        'a': 'test',
        'b': 'true',
        'c': 'false',
        'd': '56',
        'e': '3.15',
    }
    result = {
        'a': 'test',
        'b': True,
        'c': False,
        'd': 56,
        'e': 3.15,
    }

    assert util.parse_args(args) == result
