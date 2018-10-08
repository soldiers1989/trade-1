"""
    aam order rpc
"""
import requests

from .. import rpc


class AamAccountRpcError(Exception):
    """
        api error
    """
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)


class AccountRpc(rpc.Rpc):
    def __init__(self, baseurl:str, key:str, safety:bool):
        """
            init rpc
        :param baseurl: str, base url for remote http service
        :param key: str, private key for safety verification or None
        :param safety: bool, enable safety key verification with True
        """
        super().__init__(baseurl, key, safety)

    def list(self, **conds):
        """
            list account by @conds
        :param conds: dict, account filter conditions
        :return:
            list
        """
        # remote service url
        url = self.baseurl+"/account/list"

        # parameters
        params = conds.copy()
        params = self.make_token(params)

        resp = requests.get(url, params=params).json()

        if resp.get('status') != 0:
            raise AamAccountRpcError(resp.get('msg'))

        return resp.get('data')

    def select(self, **conds):
        """
            select a account by @conds
        :param conds: dict, account select conditions
        :return:
            account
        """
        # remote service url
        url = self.baseurl+"/account/select"

        # parameters
        params = conds.copy()
        params = self.make_token(params)

        resp = requests.post(url, params=params).json()

        if resp.get('status') != 0:
            raise AamAccountRpcError(resp.get('msg'))

        return resp.get('data')
