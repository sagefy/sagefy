from framework.redis import redis
from modules.memoize_redis import memoize_redis


def test_memoize_redis():
  """
  Expect to memoize the result of a function into Redis.
  """

  value = {'a': 1, 'z': 1}

  def a():
    return value

  key = 'test_memoize_redis'
  redis.delete(key)

  # try memoization
  assert memoize_redis(key, a) == value
  assert memoize_redis(key, a) == value  # a second time, memoized

  # try a bad value
  redis.setex(key, 24 * 60 * 60, b'\x80abc')
  assert memoize_redis(key, a) == b'\x80abc'

  # clean up
  redis.delete(key)
