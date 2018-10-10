"""
    aam order rpc
"""
import requests, decimal

from .. import rpc


class AamOrderRpcError(Exception):
    """
        crond api error
    """
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)


class OrderRpc(rpc.Rpc):
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
            filter order records by @conds
        :param conds: dict, sql filters
        :return:
            list
        """
        # remote service url
        url = self.baseurl+"/order/list"

        # parameters
        params = conds.copy()
        params = self.make_token(params)

        resp = requests.get(url, params=params).json()

        if resp.get('status') != 0:
            raise AamOrderRpcError(resp.get('msg'))

        return resp.get('data')

    def buy(self, account:str, tcode:str, scode:str, sname:str, optype:str, ocount:int, oprice:decimal.Decimal, callback:str, operator:str):
        """
            order buy
        :param account:
        :param tcode:
        :param scode:
        :param sname:
        :param optype:
        :param ocount:
        :param oprice:
        :param callback:
        :param operator:
        :return:
        """
        url = self.baseurl+"/order/buy"

        params = {
            'account': account,
            'tcode': tcode,
            'scode': scode,
            'sname': sname,
            'optype': optype,
            'ocount': ocount,
            'oprice': str(oprice),
            'callback': callback,
            'operator': operator
        }
        params = self.make_token(params)

        resp = requests.post(url, params=params).json()

        if resp.get('status') != 0:
            raise AamOrderRpcError(resp.get('msg'))

        return resp.get('data')

    def sell(self, account:str, tcode:str, scode:str, sname:str, optype:str, ocount:int, oprice:decimal.Decimal, callback:str, operator:str):
        """
            order sell
        :param account:
        :param tcode:
        :param scode:
        :param sname:
        :param optype:
        :param ocount:
        :param oprice:
        :param callback:
        :param operator:
        :return:
        """
        url = self.baseurl+"/order/sell"

        params = {
            'account': account,
            'tcode': tcode,
            'scode': scode,
            'sname': sname,
            'optype': optype,
            'ocount': ocount,
            'oprice': str(oprice),
            'callback': callback,
            'operator': operator
        }
        params = self.make_token(params)

        resp = requests.post(url, params=params).json()

        if resp.get('status') != 0:
            raise AamOrderRpcError(resp.get('msg'))

        return resp.get('data')

    def cancel(self, id:str, operator:str):
        """
            order cancel
        :param id:
        :param operator:
        :return:
        """
        url = self.baseurl+"/order/cancel"

        params = {
            'id': id,
            'operator': operator
        }
        params = self.make_token(params)

        resp = requests.post(url, params=params).json()

        if resp.get('status') != 0:
            raise AamOrderRpcError(resp.get('msg'))

        return resp.get('data')

    def notify(self, id:str, status:str, operator:str, dcount:int=None, dprice:decimal.Decimal=None, dcode:str=None):
        """
            order notify
        :param id:
        :param dcount:
        :param dprice:
        :param dcode:
        :param status:
        :param operator:
        :return:
        """
        url = self.baseurl+"/order/notify"

        params = {
            'id': id,
            'status': status,
            'operator': operator
        }
        if dcount is not None:
            params['dcount'] = dcount
        if dprice is not None:
            params['dprice'] = str(dprice)
        if dcode is not None:
            params['dcode'] = dcode

        params = self.make_token(params)

        resp = requests.post(url, params=params).json()

        if resp.get('status') != 0:
            raise AamOrderRpcError(resp.get('msg'))

        return resp.get('data')

    def update(self, id:str, status:str, operator:str, ocode:str=None):
        """
            update order
        :param id:
        :param status:
        :param operator:
        :param ocode:
        :return:
            dict
        """
        url = self.baseurl+"/order/update"

        params = {
            'id': id,
            'status': status,
            'operator': operator
        }
        if ocode is not None:
            params['ocode'] = ocode

        params = self.make_token(params)

        resp = requests.post(url, params=params).json()

        if resp.get('status') != 0:
            raise AamOrderRpcError(resp.get('msg'))

        return resp.get('data')
