"""
    cms app configure
"""

# default common context for all template
default_context = {
    'platform': '运营管理平台',
    'company': '天合'
}

# super user configure
super_admin = {
    'id': 0,
    'user': 'admin',
    'name': 'admin',
    'password': '123456'
}