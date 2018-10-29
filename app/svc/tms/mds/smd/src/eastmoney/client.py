"""
    http client for request data from ifeng
"""
from ... import net
from . import config

# client for access host: http://md.icaopan.com
md = net.http.Client(config.nuff.baseurls, **config.nuff.client)
