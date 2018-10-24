"""
    http client for request data from sina
"""
from ... import net
from . import config

# vip client for access host: vip.stock.finance.sina.com.cn
vip = net.http.Client(config.vip.baseurls, **config.vip.client)
