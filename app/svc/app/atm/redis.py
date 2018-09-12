"""
    redis object for atm app
"""
import redis
from . import config


# redis for log
log = redis.Redis(**config.REDISS['atm'][config.MODE], db=16)

all = {
    'log': log
}