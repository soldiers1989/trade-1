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


class Aam(Rpc):
    """
        aam service rpc
    """

    def stock_list(self, **params):
        """
            list all stocks
        :return:
        """
        # remote path
        path = '/stock/list'

        # access service
        return self.get(path, params=params)

    def stock_get(self, **params):
        """
            get stock by @id
        :param id:
        :return:
        """
        # remote path
        path = '/stock/get'

        # access service
        return self.get(path, params=params)

    def stock_add(self, stocks):
        """
            add new stocks
        :param stocks: list, stock list
        :return:
        """
        # remote path
        path = '/stock/add'

        # access service
        return self.post(path, json=stocks)

    def account_list(self, **params):
        """
            list account by @conds
        :param conds: dict, account filter conditions
        :return:
            list
        """
        # remote path
        path = '/account/list'

        # access service
        return self.get(path, params=params)

    def account_select(self, **params):
        """
            select a account by @conds
        :param conds: dict, account select conditions
        :return:
            account
        """
        # remote path
        path = '/account/select'

        # access service
        return self.get(path, params=params)

    def order_list(self, **params):
        """
            filter order records by @conds
        :param conds: dict, sql filters
        :return:
            list
        """
        # remote path
        path = '/order/list'

        # access service
        return self.get(path, params=params)

    def order_place(self, **params):
        """
            order buy
        :param account:
        :param tcode:
        :param scode:
        :param sname:
        :param optype:
        :param ocount:
        :param oprice:
        :param operator:
        :return:
        """
        # remote path
        path = '/order/place'

        # access service
        return self.post(path, params=params)

    def order_cancel(self, **params):
        """
            order cancel
        :param id:
        :param operator:
        :return:
        """
        # remote path
        path = '/order/cancel'

        # access service
        return self.post(path, params=params)

    def order_notify(self, **params):
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
        # remote path
        path = '/order/notify'

        # access service
        return self.post(path, params=params)

    def order_ocode(self, **params):
        """
            update order code
        :param id:
        :param status:
        :param operator:
        :param ocode:
        :return:
            dict
        """
        # remote path
        path = '/order/ocode'

        # access service
        return self.post(path, params=params)

    def trade_list(self, **params):
        """
            filter trade records by @conds
        :param conds: dict, sql filter conditions
        :return:
        """
        # remote path
        path = '/trade/list'

        # access service
        return self.get(path, params=params)

    def trade_update(self, **params):
        """
            update a trade record
        :param id: user trade id
        :return:
        """
        # remote path
        path = '/trade/update'

        # access service
        return self.post(path, params=params)

    def trade_user_buy(self, **params):
        """
            user buy
        :param user: int, user id
        :param stock: str, stock code
        :param lever: int, lever id
        :param coupon: int, coupon id
        :param optype: str, price type: xj or sj
        :param oprice: decimal, buy price
        :param ocount: int, buy count
        :return:
        """
        # remote path
        path = '/trade/user/buy'

        # access service
        return self.post(path, params=params)

    def trade_user_sell(self, **params):
        """
            user sell
        :param user: int, user id
        :param trade: int, trade id
        :param ptype: str, sell price type: xj or sj
        :param price: decimal, sell price
        :return:
        """
        # remote path
        path = '/trade/user/sell'

        # access service
        return self.post(path, params=params)

    def trade_user_cancel(self, **params):
        """
            user cancel
        :param user: int, user id
        :param trade: int, trade id
        :return:
        """
        # remote path
        path = '/trade/user/cancel'

        # access service
        return self.post(path, params=params)

    def trade_sys_buy(self, **params):
        """
            sys buy
        :param user: int, user id
        :param trade: int, trade id
        :param account: str, trade account
        :return:
        """
        # remote path
        path = '/trade/sys/buy'

        # access service
        return self.post(path, params=params)

    def trade_sys_sell(self, **params):
        """
            sys sell
        :param user: int, user id
        :param trade: int, trade id
        :return:
        """
        # remote path
        path = '/trade/sys/sell'

        # access service
        return self.post(path, params=params)

    def trade_sys_cancel(self, **params):
        """
            sys cancel
        :param user: int, user id
        :param trade: int, trade id
        :return:
        """
        # remote path
        path = '/trade/sys/cancel'

        # access service
        return self.post(path, params=params)

    def trade_sys_drop(self, **params):
        """
            sys drop user trade
        :param user: int, user id
        :param trade: int, trade id
        :return:
        """
        # remote path
        path = '/trade/sys/drop'

        # access service
        return self.post(path, params=params)

    def trade_order_sent(self, **params):
        """
            trade order has sent
        :param id: int, order id
        :return:
        """
        # remote path
        path = '/trade/order/sent'

        # access service
        return self.post(path, params=params)

    def trade_order_bought(self, **params):
        """
            trade order has bought
        :param id: int, trade order id
        :param dprice: decimal, stock price
        :param dcount: int, stock count
        :return:
        """
        # remote path
        path = '/trade/order/bought'

        # access service
        return self.post(path, params=params)

    def trade_order_sold(self, **params):
        """
            trade order has sold
        :param id: int, trade order id
        :param dprice: decimal, stock price
        :param dcount: int, stock count
        :return:
        """
        # remote path
        path = '/trade/order/sold'

        # access service
        return self.post(path, params=params)

    def trade_order_canceling(self, **params):
        """
            trade order is canceling
        :param id: int, trade order id
        :return:
        """
        # remote path
        path = '/trade/order/canceling'

        # access service
        return self.post(path, params=params)

    def trade_order_canceled(self, **params):
        """
            trade order has canceled
        :param id: int, trade order id
        :return:
        """
        # remote path
        path = '/trade/order/canceled'

        # access service
        return self.post(path, params=params)

    def trade_order_expired(self, **params):
        """
            trade order has expired
        :param id: int, trade order id
        :return:
        """
        # remote path
        path = '/trade/order/expired'

        # access service
        return self.post(path, params=params)

    def trade_order_update(self, **params):
        """
            update a trade order record
        :param id: trade order id
        :return:
        """
        # remote path
        path = '/trade/order/update'

        # access service
        return self.post(path, params=params)
