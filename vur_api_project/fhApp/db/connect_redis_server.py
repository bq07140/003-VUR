#!/usr/bin/env python
# coding:utf-8
"""
@author : liuyi
@file : redis_connect_server.py
@time : 2020/9/7 16:26
@desc :
"""
import logging

# from fhApp.db.check_redis import get_redis_version
# from .db_config import RedisCfg
from redis import StrictRedis


# class RedisConn(RedisCluster):
class RedisConn(StrictRedis):
    def __init__(self):
        try:
            # suffix = get_redis_version()
            # super(RedisConn, self).__init__(startup_nodes=RedisCfg["startup_nodes_" + suffix],
            #                                 password=RedisCfg["pass_wd"],
            #                                 decode_responses=True, socket_connect_timeout=0.1)
            super(RedisConn, self).__init__(host='39.107.107.149', port=6379, db=0, decode_responses=True)
        except Exception as e:
            logging.error(e)
            raise e

    def get_keys(self):
        """Returns a list of keys matching ``pattern``"""
        return self.keys()

    def lpush_link(self, r_list, value):
        """push a new link at the end of list"""
        return self.lpush(r_list, value)

    def rpush_link(self, r_list, value):
        """Push ``values`` onto the tail of the list ``name``"""
        return self.rpush(r_list, value)

    def lpop_link(self, r_list):
        """return the last link"""
        return self.lpop(r_list)

    def rpop_link(self, rlist):
        """return the first link"""
        return self.rpop(rlist)

    def len_list(self, rlist):
        """get length of list"""
        return self.llen(rlist)

    def del_list(self, rlist):
        """init list"""
        return self.delete(rlist)

    def set_name_value(self, name, value):
        """set the value at key ``name`` to ``value``"""
        return self.set(name, value)

    def get_name_value(self, name):
        """Return the value at key ``name``, or None if the key doesn't exist"""
        return self.get(name)

    def set_one_hash(self, name, key, value):
        """Set ``key`` to ``value`` within hash ``name`` Returns 1 if HSET created a new field, otherwise 0"""
        return self.hset(name, key, value)

    def get_keys_hash(self, name):
        """Return the list of keys within hash ``name``"""
        return self.hkeys(name)

    def get_one_hash(self, name, key):
        """Return the value of ``key`` within the hash ``name``"""
        return self.hget(name, key)

    def get_all_hash(self, name):
        """Return a Python dict of the hash's name/value pairs"""
        return self.hgetall(name)

    def set_many_hash(self, name, mapping):
        """Set key to value within hash ``name`` for each corresponding
        key and value from the ``mapping`` dict."""
        return self.hmset(name, mapping)

    def get_many_hash(self, name, keys, *args):
        """Returns a list of values ordered identically to ``keys``"""
        return self.hmget(name, keys, *args)

    def exists_hash(self, name, key):
        """Returns a boolean indicating if ``key`` exists within hash ``name``"""
        return self.hexists(name, key)

    def del_hash(self, name, *keys):
        """Delete ``keys`` from hash ``name``"""
        return self.hdel(name, *keys)

    def get_parttern_hash(self, name, cursor=0, match=None, count=None):
        """
        Incrementally return key/value slices in a hash. Also return a cursor
        indicating the scan position.
        ``match`` allows for filtering the keys by pattern
        ``count`` allows for hint the minimum number of returns
        统配查询二级键值
        """
        return self.hscan(name, cursor=cursor, match=match, count=count)
