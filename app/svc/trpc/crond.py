"""
    quote api
"""
import requests
from . import rpc


class CrondApiError(Exception):
    """
        crond api error
    """
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)


class CrondRpc(rpc.Rpc):
    def __init__(self, baseurl:str, key:str, safety:bool):
        """
            init rpc
        :param baseurl: str, base url for remote http service
        :param key: str, private key for safety verification or None
        :param safety: bool, enable safety key verification with True
        """
        super().__init__(baseurl, key, safety)

    def add_task(self, id, name, cond, remoteurl, method='get', data=None, json=None):
        """
            add a new crond task
        :param id:
        :param name:
        :param cond:
        :param remoteurl:
        :param method:
        :param data:
        :param json:
        :return:
        """
        # check data/json
        if data is not None and json is not None:
            raise CrondApiError('data/json must not be duplicate')

        # ignore method if data or json set
        if data is not None or json is not None:
            method = 'post'

        # check method
        if method not in ['get', 'post']:
            raise CrondApiError('method %s not suppoert.' % str(method))

        url = self.baseurl+"/task/add"

        params = {
            'id': id,
            'name': name,
            'cond': cond,
            'url': remoteurl,
            'method': method,
        }
        params = self.make_token(params)

        if method == 'get':
            resp = requests.get(url, params=params).json()
        elif method == 'post':
            resp = requests.post(url, params=params, data=data, json=json).json()
        else:
            raise CrondApiError('method %s not suppoert.' % str(method))

        if resp.get('status') != 0:
            raise CrondApiError(resp.get('msg'))

    def del_task(self, id):
        """
            delete a timer task
        :param id:
        :return:
        """
        url = self.baseurl+"/task/del"

        params = {
            'id': id,
        }
        params = self.make_token(params)

        resp = requests.get(url, params=params).json()

        if resp.get('status') != 0:
            raise CrondApiError(resp.get('msg'))

    def clear_task(self, ):
        """
            clear all timer task
        :param id:
        :return:
        """
        url = self.baseurl+"/task/clear"

        params = {
        }
        params = self.make_token(params)

        resp = requests.get(url, params=params).json()

        if resp.get('status') != 0:
            raise CrondApiError(resp.get('msg'))

    def disable_task(self, id):
        """
            disable a timer task
        :param id:
        :return:
        """
        url = self.baseurl+"/task/disable"

        params = {
            'id': id,
        }
        params = self.make_token(params)

        resp = requests.get(url, params=params).json()

        if resp.get('status') != 0:
            raise CrondApiError(resp.get('msg'))

    def enable_task(self, id):
        """
            enable a timer task
        :param id:
        :return:
        """
        url = self.baseurl+"/task/enable"

        params = {
            'id': id,
        }
        params = self.make_token(params)

        resp = requests.get(url, params=params).json()

        if resp.get('status') != 0:
            raise CrondApiError(resp.get('msg'))

    def execute_task(self, id):
        """
            enable a timer task
        :param id:
        :return:
        """
        url = self.baseurl+"/task/execute"

        params = {
            'id': id,
        }
        params = self.make_token(params)

        resp = requests.get(url, params=params).json()

        if resp.get('status') != 0:
            raise CrondApiError(resp.get('msg'))

    def get_status(self, id = None):
        """
            get status of all time task or specified @id
        :param id:
        :return:
        """
        url = self.baseurl+"/task/status"

        params = {
            'id': id,
        }
        params = self.make_token(params)

        resp = requests.get(url, params=params).json()

        return resp

    def get_detail(self, id):
        """
            get task detial by task @id
        :param id:
        :return:
        """
        url = self.baseurl + "/task/detail"

        params = {
            'id': id,
        }
        params = self.make_token(params)

        resp = requests.get(url, params=params).json()

        return resp
