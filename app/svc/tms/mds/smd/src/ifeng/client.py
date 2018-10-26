"""
    http client for request data from ifeng
"""
from ... import net
from . import config

# client for access host: http://api.finance.ifeng.com
apifinance = net.http.Client(config.apifinance.baseurls, **config.apifinance.client)
