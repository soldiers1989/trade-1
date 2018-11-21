"""
    configure for cms
"""
MODE = 'dev'

## remote service configure ##
REMOTES = {
    'aam': {
        'dev': {
            'baseurl': 'http://127.0.0.1:9001',
            'key': 'abc',
            'safety': True
        },
        'test': {
            'baseurl': 'http://127.0.0.1:9001',
            'key': 'abc',
            'safety': True
        },
        'online': {
            'baseurl': 'http://127.0.0.1:9001',
            'key': 'abc',
            'safety': True
        }
    },
    'atm': {
        'dev': {
            'baseurl': 'http://127.0.0.1:9003',
            'key': 'abc',
            'safety': True
        },
        'test': {
            'baseurl': 'http://127.0.0.1:9003',
            'key': 'abc',
            'safety': True
        },
        'online': {
            'baseurl': 'http://127.0.0.1:9003',
            'key': 'abc',
            'safety': True
        }
    },
    'mds': {
        'dev': {
            'baseurl': 'http://127.0.0.1:10007',
            'key': 'abc',
            'safety': True
        },
        'test': {
            'baseurl': 'http://127.0.0.1:10007',
            'key': 'abc',
            'safety': True
        },
        'online': {
            'baseurl': 'http://127.0.0.1:10007',
            'key': 'abc',
            'safety': True
        }
    },
    'crond': {
        'dev': {
            'baseurl': 'http://127.0.0.1:10001',
            'key': 'abc',
            'safety': True
        },
        'test': {
            'baseurl': 'http://127.0.0.1:10001',
            'key': 'abc',
            'safety': True
        },
        'online': {
            'baseurl': 'http://127.0.0.1:10001',
            'key': 'abc',
            'safety': True
        }
    }
}
