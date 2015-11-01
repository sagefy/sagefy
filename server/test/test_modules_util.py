from modules import util
import string
import datetime


def test_uniqid_length():
    # Expect the length of the ID to be 24
    assert len(util.uniqid()) is 24


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


def test_compact_dict():
    d = {'a': 1, 'b': None}
    assert util.compact_dict(d) == {'a': 1}


def test_json_serial():
    """
    Expect to tell JSON how to format non-JSON types.
    """

    assert isinstance(util.json_serial(datetime.datetime.now()), str)


def test_omit():
    """
    Expect to omit given keys and return a new dict.
    """

    d = {'a': 1, 'b': 2, 'c': 3, 'd': 4}

    assert util.omit(d, ('a', 'c')) == {
        'b': 2,
        'd': 4,
    }


def test_get_first():
    """
    Expect to get the first key available in the list.
    """

    d = {'a': 1, 'b': 2}

    assert util.get_first(d, 'A', 'a', 'b') == 1


def test_json_prep():
    """
    Expect to convert dates in objects to ISO strings.
    """

    from datetime import datetime

    assert isinstance(util.json_prep({
        'a': datetime.now()
    })['a'], str)


def test_extend():
    """
    Expect to add properties of one object to another, recursively.
    """

    a = {
        'a': 0,
        'q': 1,
    }
    b = {
        'a': 1,
        'b': 2,
        'c': {
            'c1': True,
            'c2': False,
        }
    }
    c = {
        'b': 3,
        'c': {
            'c2': True,
        }
    }

    assert util.extend(a, b, c) == {
        'a': 1,
        'b': 3,
        'c': {
            'c1': True,
            'c2': True,
        },
        'q': 1
    }


def test_object_diff():
    """

    """

    prev = {
        'a': 1,
        'b': 2,
        'c': {
            'c1': 1,
            'c2': 2,
            'c3': {
                'd1': 1,
            }
        },
        # 'e': [
        #     1,
        #     2,
        #     3
        # ]
    }

    next_ = {
        'a': 1,
        'b': 3,
        'c': {
            'c1': 1,
            'c2': 3,
            'c3': {
                'd1': 2,
            }
        },
        # 'e': [
        #     1,
        #     2,
        #     5
        # ]
    }

    assert util.object_diff(prev, next_) == set([
        'b',
        'c.c2',
        'c.c3.d1'
        # 'e.2'
    ])
