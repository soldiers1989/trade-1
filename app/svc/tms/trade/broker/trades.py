"""
    trade service
"""
import threading
from . import account, error


class Trades:
    def __init__(self):
        """
            init trade service
        """
        # account in trade service
        self._accounts = {}

        # lock for accounts
        self._lock = threading.RLock()

    def add(self, aid:str, **kwargs):
        """
            add a new trade account by specified channel with an unique account @aid
        :param aid: str, unique account id
        :param channel: str, trade channel name
        :param kwargs: dict, account init parameters
        :return:
            json, add result
        """
        with self._lock:
            acnt = self._accounts.get(aid)
            if acnt is not None:
                raise error.TradeError('account with id: %s has exists.' % aid)

            self._accounts[aid] = account.create(**kwargs)

            return {'id': aid}

    def delete(self, aid):
        """
            delete account
        :param id:
        :return:
        """
        with self._lock:
            account = self._accounts.get(aid)
            if account is not None:
                # remove from account list
                del self._accounts[aid]
                # logout first
                return account.logout()
            else:
                raise error.TradeError('account %s is not exist' % (aid))

    def clear(self):
        """
            clear all account
        :return:
        """
        with self._lock:
            results = []
            for id, account in self._accounts.items():
                # logout
                try:
                    result = account.logout()
                    results.append({'id': id, 'result': result})
                except Exception as e:
                    results.append({'id': id, 'result': str(e)})

            # empty accounts
            self._accounts = {}

            return results

    def login(self, aid = None):
        """
            账户登录
        :param aid:
        :return:
        """
        with self._lock:
            if aid is not None:
                # login account
                account = self._accounts.get(aid)
                if account is not None:
                    return account.login()
                else:
                    raise error.TradeError('account not exist')
            else:
                results = []
                # login all account
                for id, account in self._accounts.items():
                    try:
                        result = account.login()
                        results.append({'id': id, 'result': result})
                    except Exception as e:
                        results.append({'id': id, 'result': str(e)})
                return results

    def logout(self, aid = None):
        """
            账户退出
        :param aid:
        :return:
        """
        with self._lock:
            if aid is not None:
                # account logout
                account = self._accounts.get(aid)
                if account is not None:
                    return account.logout()
                else:
                    raise error.TradeError('account not exist')
            else:
                results = []
                # all account logout
                for id, account in self._accounts.items():
                    try:
                        result = account.logout()
                        results.append({'id': id, 'result': result})
                    except Exception as e:
                        results.append({'id': id, 'result': str(e)})
                return results

    def status(self, aid = None):
        """
            get account status
        :param aid:
        :return:
        """
        with self._lock:
            if aid is not None:
                account = self._accounts.get(aid)
                if account is not None:
                    return account.status()
                else:
                    raise error.TradeError('account is not exist')
            else:
                results = []
                for id, account in self._accounts.items():
                    results.append(account.status())

                return results

    def quote(self, aid, zqdm):
        """
            get current quote of stock by @code
        :param aid: str, account id
        :param zqdm: str, stock code
        :return:
            dict
        """
        with self._lock:
            account = self._accounts.get(aid)
            if account is not None:
                return account.quote(zqdm)
            else:
                raise error.TradeError('account not exist')

    def query(self, aid, type, sdate=None, edate=None):
        """
            query account data by specified type
        :param aid: str, account id
        :param type: str, data type: dqzc/dqcc/drwt/drcj/kcwt/gdxx/lswt/lscj/jgd
        :param sdate: str, in, format: yyyymmdd
        :param edate: str, in, format: yyyymmdd
        :return:
            list/dict
        """
        with self._lock:
            account = self._accounts.get(aid)
            if account is not None:
                return account.query(type, sdate, edate)
            else:
                raise error.TradeError('account not exist')

    def place(self, aid, otype, ptype, zqdm, price, count):
        """
            委托订单
        :param aid: account id
        :param otype: order type: buy/sell
        :param ptype: price type: xj/sj
        :param zqdm: stock code
        :param price: order price
        :param count: order count
        :return:
        """
        with self._lock:
            account = self._accounts.get(aid)
            if account is not None:
                return account.place(otype, ptype, zqdm, price, count)
            else:
                raise error.TradeError('account not exist')

    def cancel(self, aid, zqdm, orderno):
        """
            委托撤单
        :param aid: str, account id
        :param zqdm: str, stock code
        :param orderno: str, order number
        :return:
        """
        with self._lock:
            account = self._accounts.get(aid)
            if account is not None:
                return account.cancel(zqdm, orderno)
            else:
                raise error.TradeError('account not exist')
