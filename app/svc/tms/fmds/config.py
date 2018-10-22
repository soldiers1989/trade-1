"""
    configure for quote app
"""

# debug/autoreload flag for tornado
DEBUG = True
AUTORELOAD = True

# private key for access
ENABLE_KEY = False
PRIVATE_KEY = 'abc'

# public headers for response
HEADERS = [
    ('Content-Type', 'application/json;charset=utf8'),
    ('Server', 'nginx/1.0')
]
