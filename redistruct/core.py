

def selfkeymaker(key):
    return key

def gen_keymaker(prefix, suffix, keymaker):
    """

    :param prefix:
    :type prefix: :class:`str`
    :param suffix:
    :type suffix: :class:`str`
    :param keymaker:
    :type keymaker: :func:
    :return:
    :rtype: :func:
    """
    if keymaker:
        return keymaker
    if prefix or suffix:
        return lambda key: prefix + key + suffix
    return selfkeymaker


class WrapObject(object):
    def __init__(self, redis):
        self._redis = redis
        self._result = None

class KeyValueObject(WrapObject):
    def __init__(self, redis, prefix='', suffix='', keymaker=None):
        super(KeyValueObject, self).__init__(redis)
        self._keymaker = gen_keymaker(prefix, suffix, keymaker)

    def keys(self):
        pattern = self._keymaker('*')
        self._result = self._redis.keys(pattern)
        return self._result

    def __iter__(self):
        return iter(self.keys())

    def __getitem__(self, item):
        key = self._keymaker(item)
        self._result = self._redis.get(key)
        return self._result

    def __setitem__(self, item, value):
        key = self._keymaker(item)
        self._result = self._redis.set(key, value)

    def __delitem__(self, item):
        key = self._keymaker(item)
        self._result = self._redis.delete(key)

    def __contains__(self, item):
        key = self._keymaker(item)
        self._result = self._redis.exists(key)
        return self._result

    def items(self):
        for key in self:
            yield key,

class HashObject(WrapObject):
    def __init__(self, redis, datakey, prefix='', suffix='', keymaker=None):
        super(HashObject, self).__init__(redis)
        self._dkey = datakey
        self._keymaker = gen_keymaker(prefix, suffix, keymaker)

    def keys(self):
        self._result = self._redis.hkeys(self._dkey)
        return self._result

    def values(self):
        self._result = self._redis.hvals(self._dkey)
        return self._result

    def dict(self):
        self._result = self._redis.hgetall(self._dkey)
        return self._result

    def items(self):
        return self.dict().items()

    def __getitem__(self, item):
        key = self._keymaker(item)
        self._result = self._redis.hget(self._dkey, key)
        return self._result

    def __setitem__(self, item, value):
        key = self._keymaker(item)
        self._result = self._redis.hset(self._dkey, key, value)

    def __delitem__(self, item):
        key = self._keymaker(item)
        self._result = self._redis.hdel(self._dkey, key)

    def __contains__(self, item):
        key = self._keymaker(item)
        self._result = self._redis.hexists(self._dkey, key)

    def __iter__(self):
        return iter(self.keys())

    def __len__(self):
        return self._redis.hlen(self._dkey)


class ListObject(WrapObject):
    def __init__(self, redis, datakey):
        super(ListObject, self).__init__(redis)
        self._dkey = datakey

    def __getitem__(self, key):
        if isinstance(key, slice):
            self._result = self._redis.lrange(self._dkey, key.start, key.stop)
            return self._result
        else:
            self._result = self._redis.lindex(self._dkey, key)
            return self._result

    def __setitem__(self, item, value):
        self._result = self._redis.lset(self._dkey, item, value)

    def __len__(self):
        self._result = self._redis.llen(self._dkey)
        return self._result

    def __iter__(self):
        return iter(self[0:-1])

    def append(self, item, *args):
        self._result = self._redis.rpush(self._dkey, item, *args)

    def lappend(self, item, *args):
        self._result = self._redis.lpush(self._dkey, item, *args)

    def pop(self):
        self._result = self._redis.lpop(self._dkey)
        return self._result

    def rpop(self):
        self._result = self._redis.rpop(self._dkey)
        return self._result


class SetObject(WrapObject):
    def __init__(self, redis, datakey):
        super(SetObject, self).__init__(redis)
        self._dkey = datakey

    def add(self, member, *args):
        self._result = self._redis.sadd(self._dkey, member, *args)

    def __len__(self):
        self._result = self._redis.scard(self._dkey)
        return self._result

    def __sub__(self, other):
        self._result = self._redis.sdiff(self._dkey, other._dkey)
        return set(self._result)

    def intersection(self, other):
        self._result = self._redis.sinter(self._dkey, other._dkey)
        return set(self._result)

    def __contains__(self, item):
        self._result = self._redis.sismember(self._dkey, item)
        return self._result

    def pop(self):
        self._result = self._redis.spop(self._dkey)
        return self._result

    def remove(self, member, *args):
        self._result = self._redis.srem(self._dkey, member, *args)

    def union(self, other):
        self._result = self._redis.sunion(self._dkey, other._dkey)
        return set(self._result)


class SortedSetValueObject(WrapObject):
    def __init__(self, redis, datakey):
        super(SortedSetValueObject, self).__init__(redis)
        self._dkey = datakey

    def __len__(self):
        self._result = self._redis.zcard(self._dkey)
        return self._result

    def __setitem__(self, key, value):
        self._result = self._redis.zadd(self._dkey, value, key)

    def __getitem__(self, key):
        self._result = self._redis.zscore(self._dkey, key)
        return self._result

    def __delitem__(self, key):
        self._result = self._redis.zrem(self._dkey, key)

    def rank(self, key):
        self._result = self._redis.zrank(self._dkey)


class SortedSetRankObject(WrapObject):
    def __init__(self, redis, datakey):
        super(SortedSetRankObject, self).__init__(redis)
        self._dkey = datakey

    def __len__(self):
        self._result = self._redis.zcard(self._dkey)
        return self._result

    def __getitem__(self, key):
        if isinstance(key, slice):
            self._result = self._redis.zrange(key.start, key.stop)
            return self._result
        else:
            self._result = self._redis.zrange(key, key)
            return self._result[0]

    def add(self, member, score):
        self._result = self._redis.zadd(self._dkey, score, member)

    def remove(self, member):
        self._result = self._redis.zrem(self._dkey, member)
