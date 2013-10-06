"""
A simple class that wraps Redis functions
with the purpose of caching ORM objects.
"""
from framework import redis
import pickle


class RedisCache(object):
    def __init__(self, base_key=None):
        """
        Initialize a new cache library.
        A base_key on the class must be defined
        to namespace the storage within Redis.
        """
        if base_key:
            self.base_key = base_key

    def get(self, key, method=None, *args, **kwargs):
        """
        Get a value, and if it doesn't exist,
        set it to the return of the method.

        Define querying methods on the cache object.
        Pass the method to call by name <string>.

        Unpickle the value if necessary.

        Optional `time` keyword argument in seconds
        sets with the key and value expire.
        """
        assert self.base_key
        assert isinstance(key, basestring)

        value = redis.get('%s_%s' % (self.base_key, key))

        if value is None:
            time = kwargs.get('time') or 0
            if kwargs.get('time'):
                del kwargs['time']
            if method and hasattr(method, '__call__'):
                value = method(*args, **kwargs)
            self.set(key, value, time=time)

        elif isinstance(value, basestring):
            try:
                value = pickle.loads(value)
            except:
                pass

        return value

    def set(self, key, value, time=0):
        """
        Set the value at the key.
        If the value needs it, pickle first.
        """
        assert self.base_key
        assert isinstance(key, basestring)

        if not isinstance(value, (bool, int, float, basestring)):
            value = pickle.dumps(value)

        set_key = '%s_%s' % (self.base_key, key)

        if time:
            return redis.setex(set_key, time, value)

        return redis.set(set_key, value)

    def delete(self, key):
        """
        Remove the key and its corresponding value.
        """
        assert self.base_key
        assert isinstance(key, basestring)

        return redis.delete('%s_%s' % (self.base_key, key))
