"""
    redis object for aim app
"""
from lib.util import redis
from app.aim import config

_default = redis.MyRedis(config.redis)

new = _default.get()
