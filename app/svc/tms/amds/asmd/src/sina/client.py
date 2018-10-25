"""
    http client for request data from sina
"""
from ... import net
from . import config

# client for access host: vip.stock.finance.sina.com.cn
vsf = net.http.Client(config.vsf.baseurls, **config.vsf.client)

# client for access host: hq.sina.cn
hqjs = net.http.Client(config.hqjs.baseurls, **config.hqjs.client)
