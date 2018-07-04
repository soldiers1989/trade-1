"""
    redis object for aim app
"""
import redis
from app.aim import config

# aim redis
aim = redis.Redis(**config.REDISS['aim'][config.MODE])
