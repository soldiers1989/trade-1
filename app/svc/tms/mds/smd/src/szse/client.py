"""
    http client for request data from sse
"""
from ... import net
from . import config

# client for access host: http://www.szse.cn/
api = net.http.Client(config.api.baseurls, **config.api.client)
