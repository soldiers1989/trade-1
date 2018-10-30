"""
    rpc base class
"""
from tlib import token


class Rpc:
    def __init__(self, baseurl:str, key:str, safety:bool):
        """
            init rpc
        :param baseurl: str, base url for remote http service
        :param key: str, private key for safety verification or None
        :param safety: bool, enable safety key verification with True
        """
        self.baseurl = baseurl
        self.key = key
        self.safety = safety

    def make_token(self, params):
        """
            add token to params
        :param params:
        :return:
        """
        if not self.safety:
            return params

        return token.generate(params, self.key)
