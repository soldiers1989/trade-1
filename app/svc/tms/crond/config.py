"""
    atm app config
"""
# running mode, dev/test/online
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

# callback url for remote task
CALLBACK_URL = "http://localhost:10001/remote/callback?id=%s&seq=%s"

# public headers for response
HEADERS = [
    ('Content-Type', 'application/json;charset=utf8'),
    ('Server', 'nginx/1.0')
]



## database configure ##
DATABASES = {
    'arm': {
        'dev': {
            'host': '127.0.0.1',
            'user': 'root',
            'password': 'root',
            'database': 'arm',
            'port': 3306,
            'charset': 'utf8'
        },

        'test': {
            'host': '127.0.0.1',
            'user': 'root',
            'password': 'root',
            'database': 'arm',
            'port': 3306,
            'charset': 'utf8'
        },

        'online': {
            'host': '127.0.0.1',
            'user': 'root',
            'password': 'root',
            'database': 'arm',
            'port': 3306,
            'charset': 'utf8'
        }
    }
}
