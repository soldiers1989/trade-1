"""
    redis object for aim app
"""
import redis
from app.atm import config


# redis for log
log = redis.Redis(**config.REDISS['aim'][config.MODE], db=16)

all = {
    'log': log
}