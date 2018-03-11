import json
from framework.redis_conn import red
from modules.util import json_serial


def memoize_redis(key, fnn, time=24 * 60 * 60, *args, **kwargs):
  """
  Memoize the results of a function into Redis.
  """

  data = red.get(key)
  if isinstance(data, bytes):
    try:
      data = json.loads(data.decode())
    except:
      pass
  if data:
    return data
  data = fnn(*args, **kwargs)
  red.setex(key, time, json.dumps(
    data,
    default=json_serial,
    ensure_ascii=False
  ))
  return data
