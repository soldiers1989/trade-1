"""
    redis object for api
"""
from lib.util import redis
from app.api import config

_default = redis.MyRedis(config.redis)

new = _default.get()

