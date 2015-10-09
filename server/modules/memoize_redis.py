import json
from framework.redis import redis
from modules.util import json_serial


def memoize_redis(key, fn,  *args, time=24 * 60 * 60, **kwargs):
    """
    Memoize the results of a function into Redis.
    """

    data = redis.get(key)
    if isinstance(data, bytes):
        try:
            data = json.loads(data.decode())
        except:
            pass

    if data:
        return data

    data = fn(*args, **kwargs)

    redis.setex(key, time, json.dumps(
        data,
        default=json_serial,
        ensure_ascii=False))

    return data
