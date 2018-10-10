"""
    configure for trade service
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


# accounts for trade #
ACCOUNTS = [
    {
        'id': '29633865',
        'channel': 'tdx',
        'laccount': '29633865',
        'lpwd': '456789',
        'taccount': '29633865',
        'tpwd': '456789',
        'dept': '0',
        'version': '7.16',
        "gddm": {
            "0": "0161323426",
            "1": "A493512281"
        },
        'agents': [('agent1', '172.16.21.137', 81),  ('agent2', '172.16.21.135', 80)],
        'servers': [('szxjt1', '117.40.3.6', 7708), ('szxjt2', '202.130.235.187', 7708)]
    },
    #
    # {
    #     'id': 'polly1',
    #     'channel': 'tdx',
    #     'account': '29633865',
    #     'pwd': '456789',
    #     'dept': '0',
    #     'version': '7.16',
    #     'agents': [('agent1', '172.16.21.137', 81), ('agent2', '172.16.21.135', 80)],
    #     'servers': [('szxjt1', '117.40.3.6', 7708), ('szxjt2', '202.130.235.187', 7708)]
    # }
]


