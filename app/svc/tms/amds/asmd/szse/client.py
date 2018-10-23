"""
    http client for request data from sse
"""
from .. import http
from . import config

# client for access host: http://www.szse.cn/
api = http.Client(config.api.baseurls, **config.api.client)
