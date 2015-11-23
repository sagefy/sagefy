from framework.redis import redis
from modules.memoize_redis import memoize_redis


def test_memoize_redis():
    """
    Expect to memoize the result of a function into Redis.
    """

    def a():
        return {'a': 1, 'z': 1}

    key = 'test_memoize_redis'
    redis.delete(key)
    assert memoize_redis(key, a) == {'a': 1, 'z': 1}
    redis.delete(key)
