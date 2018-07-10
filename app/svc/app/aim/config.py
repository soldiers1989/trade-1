"""
    aim app config
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

# session id
SESSION_NAME = '_sid'
# session expire time in seconds
SESSION_TIMEOUT = 30*24*3600
# session cookie timeout in days
SESSION_COOKIE_TIMEOUT = 30


# image verifier code expire time in seconds
EXPIRE_VERIFIER_IMAGE = 120

# sms verifier code expire time in seconds
EXPIRE_VERIFIER_SMS = 300

# public headers for response
HEADERS = [
    ('Content-Type', 'application/json;charset=utf8'),
    ('Server', 'nginx/1.0')
]

## redis configure ##
REDISS = {
    'aim':{
        'dev': {
            'host': '127.0.0.1',
            'port': 6379,
            'db': 0,
            'password': None,
            'encoding': 'utf-8',
            'decode_responses': True
        },

        'test': {
            'host': '127.0.0.1',
            'port': 6379,
            'db': 0,
            'password': None,
            'encoding': 'utf-8',
            'decode_responses': True
        },

        'online': {
            'host': '127.0.0.1',
            'port': 6379,
            'db': 0,
            'password': None,
            'encoding': 'utf-8',
            'decode_responses': True
        }
    }
}


## database configure ##
# all databases
DATABASES = {
    'aim': {
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

