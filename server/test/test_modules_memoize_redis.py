from framework.redis import redis
from modules.memoize_redis import memoize_redis


def test_memoize_redis():
    """
    Expect to memoize the result of a function into Redis.
    """

    def a(z):
        return {'a': 1, 'z': z}

    key = 'test_memoize_redis_{id}'

    redis.delete(key)

    assert memoize_redis(key.format(id=1), a, 1) == {'a': 1, 'z': 1}
    assert memoize_redis(key.format(id=3), a, 3) == {'a': 1, 'z': 3}

    def a(z):
        pass

    assert memoize_redis(key.format(id=1), a, 1) == {'a': 1, 'z': 1}

    redis.delete(key.format(id=1))
    redis.delete(key.format(id=3))
