"""
Short, one-off methods that could potentially be reused anywhere.
"""


from datetime import datetime
import collections
import uuid
import base64

# uuid.uuid4()  create a new UUID

"""
Example:

my_uuid = uuid.UUID('24014660-55a1-20b7-2c88-1cb21f63bd7e')
convert_uuid_to_slug(my_uuid)
-> 'JAFGYFWhILcsiByyH2O9fg'

convert_slug_to_uuid('JAFGYFWhILcsiByyH2O9frcU')
-> UUID('24014660-55a1-20b7-2c88-1cb21f63bd7e')
convert_slug_to_uuid('JAFGYFWhILcsiByyH2O9fg')
-> UUID('24014660-55a1-20b7-2c88-1cb21f63bd7e')
"""


def convert_uuid_to_slug(my_uuid):
  if isinstance(my_uuid, str):
    return my_uuid
  assert isinstance(my_uuid, uuid.UUID)
  return base64.urlsafe_b64encode(my_uuid.bytes)[:-2].decode()


def convert_slug_to_uuid(slug):
  if isinstance(slug, uuid.UUID):
    return slug
  assert isinstance(slug, str)
  if len(slug) != 22:
    return None
  slug = slug[0:22]
  return uuid.UUID(bytes=base64.urlsafe_b64decode(slug + '=='))


def create_uuid_b64():
  """
  Create a new Base 64 UUID.
  """
  return convert_uuid_to_slug(uuid.uuid4())


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
  if isinstance(val, uuid.UUID):
    return convert_uuid_to_slug(val)
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
      elif injector[key] is not None:
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
