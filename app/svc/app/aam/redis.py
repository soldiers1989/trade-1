"""
    redis object for aam app
"""
import redis
from app.aam import config


# redis for log
log = redis.Redis(**config.REDISS['aam'][config.MODE], db=15)

all = {
    'log': log
}