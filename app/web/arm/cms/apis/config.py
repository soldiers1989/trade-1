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
    }
}
