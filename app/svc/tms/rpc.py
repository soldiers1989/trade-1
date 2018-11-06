"""
    remote process communication api
"""
import requests
from tlib import token


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


class Broker(Rpc):
    """
        broker service rpc
    """
    def start(self, **params):
        """
            start broker service
        :param params:
        :return:
        """
        # remote path
        path = '/trade/start'

        # access service
        return self.post(path, params=params)

    def stop(self, **params):
        """
            stop broker service
        :param params:
        :return:
        """
        # remote path
        path = '/trade/stop'

        # access service
        return self.post(path, params=params)

    def status(self, **params):
        """
            get broker service status
        :param params:
        :return:
        """
        # remote path
        path = '/trade/status'

        # access service
        return self.post(path, params=params)

    def register(self, **params):
        """
            register accounts
        :param params:
        :return:
        """
        # remote path
        path = '/trade/register'

        # access service
        return self.post(path, params=params)

    def login(self, **params):
        """
            login an account
        :param params:
        :return:
        """
        # remote path
        path = '/trade/login'

        # access service
        return self.post(path, params=params)

    def logout(self, **params):
        """
            logout an account
        :param params:
        :return:
        """
        # remote path
        path = '/trade/logout'

        # access service
        return self.post(path, params=params)

    def transfer(self, **params):
        """
            transfer money
        :param params:
        :return:
        """
        # remote path
        path = '/trade/transfer'

        # access service
        return self.post(path, params=params)

    def query(self, **params):
        """
            query account information
        :param params:
        :return:
        """
        # remote path
        path = '/trade/query'

        # access service
        return self.post(path, params=params)

    def place(self, **params):
        """
            place order
        :param params:
        :return:
        """
        # remote path
        path = '/trade/place'

        # access service
        return self.post(path, params=params)

    def cancel(self, **params):
        """
            cancel order
        :param params:
        :return:
        """
        # remote path
        path = '/trade/cancel'

        # access service
        return self.post(path, params=params)

    def clear(self, **params):
        """
            trade clear
        :param params:
        :return:
        """
        # remote path
        path = '/trade/clear'

        # access service
        return self.post(path, params=params)


class Crond(Rpc):
    """
        crond service rpc
    """
    def add(self, params, data=None, json=None):
        """
            add a new crond task
        :param params:
        :param data:
        :param json:
        :return:
        """
        # remote path
        path = "/task/add"

        # access service
        return self.post(path, params=params, data=data, json=json)

    def delete(self, **params):
        """
            delete a timer task
        :param id:
        :return:
        """
        # remote path
        path = "/task/del"

        # access service
        return self.get(path, params=params)

    def clear(self, **params):
        """
            clear all timer task
        :param id:
        :return:
        """
        # remote path
        path = "/task/clear"

        # access service
        return self.get(path, params=params)

    def disable(self, **params):
        """
            disable a timer task
        :param id:
        :return:
        """
        # remote path
        path = "/task/disable"

        # access service
        return self.get(path, params=params)

    def enable(self, **params):
        """
            enable a timer task
        :param id:
        :return:
        """
        # remote path
        path = "/task/enable"

        # access service
        return self.get(path, params=params)

    def execute(self, **params):
        """
            enable a timer task
        :param id:
        :return:
        """
        # remote path
        path = "/task/execute"

        # access service
        return self.get(path, params=params)

    def status(self, **params):
        """
            get status of all time task or specified @id
        :param id:
        :return:
        """
        # remote path
        path = "/task/status"

        # access service
        return self.get(path, params=params)

    def detail(self, **params):
        """
            get task detial by task @id
        :param id:
        :return:
        """
        # remote path
        path = "/task/detail"

        # access service
        return self.get(path, params=params)


class Mds(Rpc):
    """
        market data service rpc
    """
    def stock_list(self, **params):
        """
            get stock list
        :param params:
        :return:
        """
        # remote path
        path = "/stock/list"

        # access service
        return self.get(path, params=params)

    def stock_quote(self, **params):
        """
            get all or specified stock's current quote
        :param zqdm:
        :return:
        """
        # remote path
        path = "/stock/quote"

        # access service
        return self.get(path, params=params)

    def stock_ticks(self, **params):
        """
            get specified stock ticks data
        :param zqdm:
        :param date:
        :return:
        """
        # remote path
        path = "/stock/ticks"

        # access service
        return self.get(path, params=params)

    def stock_kline(self, **params):
        """
            get specified stock kline data
        :param zqdm:
        :param type:
        :return:
        """
        # remote path
        path = "/stock/kline"

        # access service
        return self.get(path, params=params)


class Quote(Rpc):
    """
        quote service rpc
    """
    def get(self, **params):
        """
            get current level 5 quote of stock by @code
        :param code: str, stock code
        :return:
        """
        # remote path
        path = "/quote/level5"

        # access service
        return self.get(path, params=params)


class Sms(Rpc):
    """
        short message service rpc
    """
    def send(self):
        pass


class Trade(Rpc):
    """
        trade service rpc
    """

    def add(self, account):
        """
            添加股票账户
        :return:
        """
        # remote path
        path = "/account/add"

        # access service
        return self.post(path, json=account)

    def delete(self, **params):
        """
            删除股票账户
        :param account:
        :return:
        """
        # remote path
        path = "/account/del"

        # access service
        return self.get(path, params=params)

    def clear(self, **params):
        """
            清除所有股票账户
        :return:
        """
        # remote path
        path = "/account/clear"

        # access service
        return self.get(path, params=params)

    def login(self, **params):
        """
            股票账户登录
        :param account:
        :return:
        """
        # remote path
        path = "/account/login"

        # access service
        return self.get(path, params=params)

    def logout(self, **params):
        """
            股票账户登出
        :param account:
        :return:
        """
        # remote path
        path = "/account/logout"

        # access service
        return self.get(path, params=params)

    def status(self, **params):
        """
            股票账户交易通道状态
        :param account:
        :return:
            通道状态信息
        """
        # remote path
        path = "/account/status"

        # access service
        return self.get(path, params=params)

    def query(self, **params):
        """
            查询当前或者历史信息
        :param account:
        :param type: str, 查询类别，dqzc/dqcc/drwt/drcj/kcwt/gdxx/lswt/lscj/jgd
        :param sdate: str, 开始日期，yyyymmdd
        :param edate: str, 结束日期, yyyymmdd
        :return:
            dict/list
        """
        # remote path
        path = "/account/query"

        # access service
        return self.get(path, params=params)


    def place(self, **params):
        """
            委托下单
        :param account:
        :param otype:
        :param ptype:
        :param zqdm:
        :param price:
        :param count:
        :return:
            委托编号
        """
        # remote path
        path = "/order/place"

        # access service
        return self.get(path, params=params)

    def cancel(self, **params):
        """
            委托撤单
        :param account:
        :param zqdm:
        :param orderno:
        :return:
        """
        # remote path
        path = "/order/cancel"

        # access service
        return self.get(path, params=params)
