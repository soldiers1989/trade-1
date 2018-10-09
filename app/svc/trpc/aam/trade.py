"""
    aam trade rpc
"""
import requests, decimal

from .. import rpc


class AamTradeRpcError(Exception):
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

    def list(self, **conds):
        """
            filter trade records by @conds
        :param conds: dict, sql filter conditions
        :return:
        """
        url = self.baseurl+"/trade/list"

        params = conds.copy()
        params = self.make_token(params)

        resp = requests.get(url, params=params).json()

        if resp.get('status') != 0:
            raise AamTradeRpcError(resp.get('msg'))

        return resp.get('data')

    def user_buy(self, user:int, lever:int, stock:str, ptype:str, price:decimal.Decimal, count:int):
        """
            user buy
        :param user: int, user id
        :param lever: int, lever id
        :param stock: str, stock code
        :param ptype: str, price type: xj or sj
        :param price: decimal, buy price
        :param count: int, buy count
        :return:
        """
        url = self.baseurl+"/trade/user/buy"

        params = {
            'user': user,
            'lever': lever,
            'stock': stock,
            'ptype': ptype,
            'price': str(price),
            'count': count
        }
        params = self.make_token(params)

        resp = requests.post(url, params=params).json()

        if resp.get('status') != 0:
            raise AamTradeRpcError(resp.get('msg'))

        return resp.get('data')

    def user_sell(self, user:int, trade:int, ptype:str, price:decimal.Decimal):
        """
            user sell
        :param user: int, user id
        :param trade: int, trade id
        :param ptype: str, sell price type: xj or sj
        :param price: decimal, sell price
        :return:
        """
        url = self.baseurl+"/trade/user/sell"

        params = {
            'user': user,
            'trade': trade,
            'ptype': ptype,
            'price': str(price)
        }
        params = self.make_token(params)

        resp = requests.post(url, params=params).json()

        if resp.get('status') != 0:
            raise AamTradeRpcError(resp.get('msg'))

        return resp.get('data')

    def user_close(self, user:int, trade:int, ptype:str, price:decimal.Decimal):
        """
            user sell
        :param user: int, user id
        :param trade: int, trade id
        :param ptype: str, sell price type: xj or sj
        :param price: decimal, sell price
        :return:
        """
        url = self.baseurl+"/trade/user/close"

        params = {
            'user': user,
            'trade': trade,
            'ptype': ptype,
            'price': str(price)
        }
        params = self.make_token(params)

        resp = requests.post(url, params=params).json()

        if resp.get('status') != 0:
            raise AamTradeRpcError(resp.get('msg'))

        return resp.get('data')

    def user_cancel(self, user:int, trade:int):
        """
            user cancel
        :param user: int, user id
        :param trade: int, trade id
        :return:
        """
        url = self.baseurl+"/trade/user/cancel"

        params = {
            'user': user,
            'trade': trade,
        }
        params = self.make_token(params)

        resp = requests.post(url, params=params).json()

        if resp.get('status') != 0:
            raise AamTradeRpcError(resp.get('msg'))

        return resp.get('data')

    def sys_buy(self, user:int, trade:int, account:str):
        """
            sys buy
        :param user: int, user id
        :param trade: int, trade id
        :param account: str, trade account
        :return:
        """
        url = self.baseurl+"/trade/sys/buy"

        params = {
            'user': user,
            'trade': trade,
            'account': account
        }
        params = self.make_token(params)

        resp = requests.post(url, params=params).json()

        if resp.get('status') != 0:
            raise AamTradeRpcError(resp.get('msg'))

        return resp.get('data')

    def sys_sell(self, user:int, trade:int):
        """
            sys sell
        :param user: int, user id
        :param trade: int, trade id
        :return:
        """
        url = self.baseurl+"/trade/sys/sell"

        params = {
            'user': user,
            'trade': trade,
        }
        params = self.make_token(params)

        resp = requests.post(url, params=params).json()

        if resp.get('status') != 0:
            raise AamTradeRpcError(resp.get('msg'))

        return resp.get('data')

    def sys_close(self, user:int, trade:int):
        """
            sys close
        :param user: int, user id
        :param trade: int, trade id
        :return:
        """
        url = self.baseurl+"/trade/sys/close"

        params = {
            'user': user,
            'trade': trade,
        }
        params = self.make_token(params)

        resp = requests.post(url, params=params).json()

        if resp.get('status') != 0:
            raise AamTradeRpcError(resp.get('msg'))

        return resp.get('data')

    def sys_cancel(self, user:int, trade:int):
        """
            sys cancel
        :param user: int, user id
        :param trade: int, trade id
        :return:
        """
        url = self.baseurl+"/trade/sys/cancel"

        params = {
            'user': user,
            'trade': trade,
        }
        params = self.make_token(params)

        resp = requests.post(url, params=params).json()

        if resp.get('status') != 0:
            raise AamTradeRpcError(resp.get('msg'))

        return resp.get('data')

    def sys_bought(self, user:int, trade:int, price:decimal.Decimal, count:int):
        """
            sys bought
        :param user: int, user id
        :param trade: int, trade id
        :param price: decimal, stock price
        :param count: int, stock count
        :return:
        """
        url = self.baseurl+"/trade/sys/bought"

        params = {
            'user': user,
            'trade': trade,
            'price': str(price),
            'count': count
        }
        params = self.make_token(params)

        resp = requests.post(url, params=params).json()

        if resp.get('status') != 0:
            raise AamTradeRpcError(resp.get('msg'))

        return resp.get('data')

    def sys_sold(self, user:int, trade:int, price:decimal.Decimal, count:int):
        """
            sys sold
        :param user: int, user id
        :param trade: int, trade id
        :param price: decimal, stock price
        :param count: int, stock count
        :return:
        """
        url = self.baseurl+"/trade/sys/sold"

        params = {
            'user': user,
            'trade': trade,
            'price': str(price),
            'count': count
        }
        params = self.make_token(params)

        resp = requests.post(url, params=params).json()

        if resp.get('status') != 0:
            raise AamTradeRpcError(resp.get('msg'))

        return resp.get('data')

    def sys_closed(self, user:int, trade:int, price:decimal.Decimal, count:int):
        """
            sys closed
        :param user: int, user id
        :param trade: int, trade id
        :param price: decimal, stock price
        :param count: int, stock count
        :return:
        """
        url = self.baseurl+"/trade/sys/closed"

        params = {
            'user': user,
            'trade': trade,
            'price': str(price),
            'count': count
        }
        params = self.make_token(params)

        resp = requests.post(url, params=params).json()

        if resp.get('status') != 0:
            raise AamTradeRpcError(resp.get('msg'))

        return resp.get('data')

    def sys_canceled(self, user:int, trade:int):
        """
            sys canceled
        :param user: int, user id
        :param trade: int, trade id
        :return:
        """
        url = self.baseurl+"/trade/sys/canceled"

        params = {
            'user': user,
            'trade': trade,
        }
        params = self.make_token(params)

        resp = requests.post(url, params=params).json()

        if resp.get('status') != 0:
            raise AamTradeRpcError(resp.get('msg'))

        return resp.get('data')

    def sys_dropped(self, user:int, trade:int):
        """
            sys dropped
        :param user: int, user id
        :param trade: int, trade id
        :return:
        """
        url = self.baseurl+"/trade/sys/dropped"

        params = {
            'user': user,
            'trade': trade,
        }
        params = self.make_token(params)

        resp = requests.post(url, params=params).json()

        if resp.get('status') != 0:
            raise AamTradeRpcError(resp.get('msg'))

        return resp.get('data')

    def sys_expired(self, user:int, trade:int):
        """
            sys expired
        :param user: int, user id
        :param trade: int, trade id
        :return:
        """
        url = self.baseurl+"/trade/sys/expired"

        params = {
            'user': user,
            'trade': trade,
        }
        params = self.make_token(params)

        resp = requests.post(url, params=params).json()

        if resp.get('status') != 0:
            raise AamTradeRpcError(resp.get('msg'))

        return resp.get('data')

    def notify(self, code:str, dprice:decimal.Decimal, dcount:int, dcode:str):
        """
            notify trade result
        :param code: str, trade code
        :param dprice: decimal, stock price
        :param dcount: int, stock count
        :param dcode: str, deal code
        :return:
        """
        url = self.baseurl+"/trade/notify"

        params = {
            'code': code,
            'dprice': str(dprice),
            'dcount': dcount,
            'dcode': dcode
        }
        params = self.make_token(params)

        resp = requests.post(url, params=params).json()

        if resp.get('status') != 0:
            raise AamTradeRpcError(resp.get('msg'))

        return resp.get('data')
