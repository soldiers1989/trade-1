"""
    configure for trade service
"""
# debug/autoreload flag for tornado
DEBUG = True
AUTORELOAD = True


# private key for access
ENABLE_KEY = True
PRIVATE_KEY = 'abc'


# public headers for response
HEADERS = [
    ('Content-Type', 'application/json;charset=utf8'),
    ('Server', 'nginx/1.0')
]


# agents for trade
AGENTS = [
    ('agent1', '172.16.21.137', 81),
    ('agent2', '172.16.21.135', 80)
]

# servers for trade #
# 中信建投
S_ZXJT = [
    ('szxjt1', '117.40.3.6', 7708),
    ('szxjt2', '202.130.235.187', 7708)
]

# accounts for trade #
ACCOUNTS = [
    # (login-account, login-password, trade-account, trade-password, department, version, agent servers, trade servers)
    # ('29633865', '456789', '29633865', '456789', '0', '7.16', AGENTS, S_ZXJT) # 中信建投
]

