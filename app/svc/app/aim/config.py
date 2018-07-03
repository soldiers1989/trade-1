"""
    aim app config
"""
from app import config


# debug/autoreload flag for tornado
DEBUG = False
AUTORELOAD = True


## redis configure ##
REDISS = {
    'dev': {
        'host': '127.0.0.1',
        'port': '3306',
        'db': 'arm',
        'password': 'root',
        'encoding': 'utf-8'
    },

    'test': {
        'host': '127.0.0.1',
        'port': '3306',
        'db': 'arm',
        'password': 'root',
        'encoding': 'utf-8'
    },

    'online': {
        'host': '127.0.0.1',
        'port': '3306',
        'db': 'arm',
        'password': 'root',
        'encoding': 'utf-8'
    }
}
redis = REDISS[config.mode]


## database configure ##
# all databases
DATABASES = {
    'dev': {
        'host': '127.0.0.1',
        'user': 'root',
        'password': 'root',
        'database': 'arm',
        'port': '3306',
        'charset': 'utf8'
    },

    'test': {
        'host': '127.0.0.1',
        'user': 'root',
        'password': 'root',
        'database': 'arm',
        'port': '3306',
        'charset': 'utf8'
    },

    'online': {
        'host': '127.0.0.1',
        'user': 'root',
        'password': 'root',
        'database': 'arm',
        'port': '3306',
        'charset': 'utf8'
    }
}
# current mysql database
mysql = DATABASES[config.mode]
