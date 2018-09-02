"""
    redis object for aam app
"""
import redis
from app.aam import config


# redis for log
log = redis.Redis(**config.REDISS['aam'][config.MODE], db=15)

# redis for lock
lock = redis.Redis(**config.REDISS['aam'][config.MODE], db=14)

# for admin redis data
all = {
    'log': log,
    'lock': lock
}