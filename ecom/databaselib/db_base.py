# coding=utf-8
import redis

"""
是访问底层数据库的接口
包含了对缓存数据库的访问，如redis
对数据库的访问，如mysql
"""

ConnectionPool = redis.ConnectionPool.from_url('redis://127.0.0.1:6379/0')


class RedisBase:
    """
    封装redis的接口
    """
    def __init__ (self):
        self._redis = redis.Redis(connection_pool = ConnectionPool)
        return

    def Append(self, key, value):
        ret = self._redis.append(key, value)
        return ret

    def Delete(self, *names):
        ret = self._redis.delete(*names)
        return ret

    def Expire(self, name, time):
        self._redis.expire(name, time)
        return

    def Exists(self, name):
        ret = self._redis.exists(name)
        return ret

    def Get(self, name):
        """
        如果没有返回None
        """
        ret = self._redis.get(name)
        return ret

    def Set(self, name, value, ex=None, px=None, nx=False, xx=False):
        self._redis.set(name, value, ex, px, nx, xx)
        return

    def Hget(self, name, key):
        """
        如果没有返回None
        """
        ret = self._redis.hget(name, key)
        return ret

    def Hgetall(self, name):
        ret = self._redis.hgetall(name)
        return ret

    def Hset(self, name, key, value):
        ret = self._redis.hset(name, key, value)
        return

    def Hsetnx(self, name, key, value):
        """
        成功返回1，失败返回0
        """
        ret = self._redis.hsetnx(name, key, value)
        return ret

    def Hmset(self, name, mapping):
        ret = self._redis.hmset(name, mapping)
        return

    def Hmget(self, name, keys, *args):
        ret = self._redis.hmget(name, keys, *args)
        return ret

    def Hincrby(self, name, key, amount=1):
        ret = self._redis.hincrby(name, key, amount)
        return ret

    def Hdel(self, name, *keys):
        ret = self._redis.hdel(name, *keys)
        return ret

    def Sadd(self, name, *values):
        ret = self._redis.sadd(name, *values)
        return ret

    def Smembers(self, name):
        ret = self._redis.smembers(name)
        return ret

    def Lpush(self, name, *values):
        ret = self._redis.lpush(name, *values)
        return ret

    def Rpush(self, name, *values):
        ret = self._redis.rpush(name, *values)
        return ret

    def Lpop(self, name):
        ret = self._redis.lpop(name)
        return ret

    def Rpop(self, name):
        ret = self._redis.rpop(name)
        return ret
