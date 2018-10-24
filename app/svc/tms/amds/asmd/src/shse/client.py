"""
    http client for request data from sse
"""
from ... import net
from . import config

# client for access host: http://query.sse.com.cn/
query = net.http.Client(config.query.baseurls, **config.query.client)
