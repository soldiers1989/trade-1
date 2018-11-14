"""
    atm app config
"""
# running mode, dev/test/online
MODE = "dev"

# max executor works
EXECUTOR_WORKERS = 10

# configure for tornado appliaction
DEBUG = True
AUTORELOAD = True

# private key for access
ENABLE_KEY = False
PRIVATE_KEY = 'abc'

# cookie expire time in seconds
COOKIE_SECRET = 'abc'
COOKIE_TIMEOUT = 30*24*3600

# session id
SESSION_NAME = '_sid'
# session expire time in seconds
SESSION_TIMEOUT = 30*24*3600
# session cookie timeout in days
SESSION_COOKIE_TIMEOUT = 30

# public headers for response
HEADERS = [
    ('Content-Type', 'application/json;charset=utf8'),
    ('Server', 'nginx/1.0')
]
