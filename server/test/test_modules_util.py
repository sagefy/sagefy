import uuid
from datetime import datetime
from modules import util
from modules.util import convert_uuid_to_slug, convert_slug_to_uuid, \
  create_uuid_b64, json_serial


def test_convert_uuid_to_slug():
  my_uuid = uuid.UUID('24014660-55a1-20b7-2c88-1cb21f63bd7e')
  assert convert_uuid_to_slug('abcd') == 'abcd'
  assert convert_uuid_to_slug(my_uuid) == 'JAFGYFWhILcsiByyH2O9fg'


def test_convert_slug_to_uuid():
  my_uuid = uuid.UUID('24014660-55a1-20b7-2c88-1cb21f63bd7e')
  assert convert_slug_to_uuid(my_uuid) == my_uuid
  assert convert_slug_to_uuid('JAFGYFWhILcsiByyH2O9fg') == my_uuid


def test_create_uuid_b64():
  assert len(create_uuid_b64()) == 22


def test_pick():
  # Expect pick to make a new dict with only keys presented
  d = {'a': 1, 'b': 2}
  keys = ('a',)
  assert util.pick(d, keys) == {'a': 1}
  assert d == {'a': 1, 'b': 2}


def test_omit():
  """
  Expect to omit given keys and return a new dict.
  """

  d = {'a': 1, 'b': 2, 'c': 3, 'd': 4}

  assert util.omit(d, ('a', 'c')) == {
    'b': 2,
    'd': 4,
  }


def test_compact():
  # Expect compact to remove None from an array
  a = [1, None, 3, None]
  assert util.compact(a) == [1, 3]


def test_compact_dict():
  d = {'a': 1, 'b': None}
  assert util.compact_dict(d) == {'a': 1}


def test_get_first():
  """
  Expect to get the first key available in the list.
  """

  d = {'a': 1, 'b': 2}
  assert util.get_first(d, 'A', 'a', 'b') == 1


def test_get_first2():
  d = {}
  assert util.get_first(d, 'A', 'a', 'b') is None


def test_json_serial():
  """
  Expect to tell JSON how to format non-JSON types.
  """

  assert json_serial('a') == 'a'
  assert isinstance(json_serial(datetime.now()), str)
  assert isinstance(json_serial(uuid.uuid4()), str)
  assert len(json_serial(uuid.uuid4())) == 22


def test_json_prep():
  """
  Expect to convert dates in objects to ISO strings.
  """

  assert isinstance(util.json_prep({
    'a': datetime.now()
  })['a'], str)
  assert isinstance(util.json_prep({
    'a': {
      'a': datetime.now()
    },
  })['a']['a'], str)


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
    #   1,
    #   2,
    #   3
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
    #   1,
    #   2,
    #   5
    # ]
  }

  assert util.object_diff(prev, next_) == set([
    'b',
    'c.c2',
    'c.c3.d1'
    # 'e.2'
  ])
