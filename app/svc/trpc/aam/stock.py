"""
    stock api
"""
import requests

from .. import rpc


class AamStockRpcError(Exception):
    """
        crond api error
    """
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)


class StockRpc(rpc.Rpc):
    def __init__(self, baseurl:str, key:str, safety:bool):
        """
            init rpc
        :param baseurl: str, base url for remote http service
        :param key: str, private key for safety verification or None
        :param safety: bool, enable safety key verification with True
        """
        super().__init__(baseurl, key, safety)

    def list(self):
        """
            list all stocks
        :return:
        """
        url = self.baseurl+"/stock/list"

        params = {
        }
        params = self.make_toekn(params)

        resp = requests.get(url, params=params).json()

        if resp.get('status') != 0:
            raise AamStockRpcError(resp.get('msg'))

        return resp.get('data')


    def get(self, id):
        """
            get stock by @id
        :param id:
        :return:
        """
        url = self.baseurl+"/stock/get"

        params = {
            'id': id
        }
        params = self.make_toekn(params)

        resp = requests.get(url, params=params).json()

        if resp.get('status') != 0:
            raise AamStockRpcError(resp.get('msg'))

        return resp.get('data')


    def add(self, stocks):
        """
            add new stocks
        :param stocks: list, stock list
        :return:
        """
        url = self.baseurl+"/stock/add"

        params = {
        }
        params = self.make_toekn(params)

        resp = requests.post(url, params=params, json=stocks).json()

        if resp.get('status') != 0:
            raise AamStockRpcError(resp.get('msg'))

        return resp.get('data')
