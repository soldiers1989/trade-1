"""
    configure for quote app
"""

# debug/autoreload flag for tornado
DEBUG = False
AUTORELOAD = True


# public headers for response
HEADERS = [
    ('Content-Type', 'application/json;charset=utf8'),
    ('Server', 'nginx/1.0')
]
