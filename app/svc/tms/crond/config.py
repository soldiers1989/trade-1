"""
    atm app config
"""
# running mode, dev/test/online
MODE = "dev"

# configure for tornado appliaction
DEBUG = False
AUTORELOAD = True

# token for access
TOKEN_NAME = '_token'
TOKEN_VALUE = 'abc'

# cookie expire time in seconds
COOKIE_SECRET = 'abc'
COOKIE_TIMEOUT = 30*24*3600

# callback url for remote task
CALLBACK_URL = "http://localhost:9000/remote/callback?id=%s&seq=%s"

# public headers for response
HEADERS = [
    ('Content-Type', 'application/json;charset=utf8'),
    ('Server', 'nginx/1.0')
]


