"""
    redis object for aim app
"""
import redis
from app.aim import config

# redis for session
session = redis.Redis(**config.REDISS['aim'][config.MODE], db=0)

# redis for verify image
vimg = redis.Redis(**config.REDISS['aim'][config.MODE], db=1)

# redis for verify sms
vsms = redis.Redis(**config.REDISS['aim'][config.MODE], db=2)

# redis for cache
cache = redis.Redis(**config.REDISS['aim'][config.MODE], db=3)

# redis for log
log = redis.Redis(**config.REDISS['aim'][config.MODE], db=15)

all = {
    'session': session,
    'vimg': vimg,
    'vsms': vsms,
    'cache': cache,
    'log': log
}