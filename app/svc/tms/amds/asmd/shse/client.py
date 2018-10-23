"""
    http client for request data from sse
"""
from .. import http
from . import config

# client for access host: http://query.sse.com.cn/
query = http.Client(config.query.baseurls, **config.query.client)
