"""
    remote process communication api
"""
import requests
from . import token


# rpc access error
class RpcError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)


class Rpc:
    """
        remote rpc base class
    """
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

    def _token(self, params):
        """
            add token to params
        :param params:
        :return:
        """
        if not self.safety:
            return params

        params = {} if params is None else params

        return token.generate(params, self.key)

    def get(self, path, params=None, **kwargs):
        """
            get method
        :param path:
        :param params:
        :return:
        """
        # remote url path
        url = self.baseurl + path

        # params with token
        params = self._token(params)

        # request remote service
        resp = requests.get(url, params=params, **kwargs).json()

        if resp.get('status') != 0:
            raise RpcError(resp.get('msg'))

        return resp.get('data')

    def post(self, path, params=None, data=None, json=None, **kwargs):
        """
            post method
        :param path:
        :param params:
        :param data:
        :param json:
        :return:
        """
        # remote url path
        url = self.baseurl + path

        # params with token
        params = self._token(params)

        # request remote service
        resp = requests.post(url, params=params, data=data, json=json, **kwargs).json()

        if resp.get('status') != 0:
            raise RpcError(resp.get('msg'))

        return resp.get('data')


class Atm(Rpc):
    """
        atm service rpc
    """

    def risk_check(self, json):
        """
            rick check
        :return:
        """
        # remote path
        path = '/task/risk/check'

        # access service
        return self.post(path, json=json)
