"""
    atm app config
"""
# running mode, mock/simulation
MODE = "dev"

# configure for tornado appliaction
DEBUG = True
AUTORELOAD = True

# private key for access
ENABLE_KEY = False
PRIVATE_KEY = 'abc'

# cookie expire time in seconds
COOKIE_SECRET = 'abc'
COOKIE_TIMEOUT = 30*24*3600

# public headers for response
HEADERS = [
    ('Content-Type', 'application/json;charset=utf8'),
    ('Server', 'nginx/1.0')
]


