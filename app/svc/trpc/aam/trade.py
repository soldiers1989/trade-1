"""
    aam trade rpc
"""

import requests

from .. import rpc


class AamOrderRpcError(Exception):
    """
        crond api error
    """
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)


class TradeRpc(rpc.Rpc):
    def __init__(self, baseurl:str, key:str, safety:bool):
        """
            init rpc
        :param baseurl: str, base url for remote http service
        :param key: str, private key for safety verification or None
        :param safety: bool, enable safety key verification with True
        """
        super().__init__(baseurl, key, safety)