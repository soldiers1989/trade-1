"""
    trade service
"""
import threading
from . import account, protocol, error


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
                return protocol.failed('account with id: %s has exists.' % aid)

            self._accounts[aid] = account.create(**kwargs)

            return protocol.success('account has added')

    def delete(self, aid):
        """
            delete account
        :param id:
        :return:
        """
        with self._lock:
            account = self._accounts.get(aid)
            if account is not None:
                # logout first
                account.logout()
                # remove from account list
                del self._accounts[aid]
                # response
                resp = protocol.success('account has deleted.', data={'id':aid})
            else:
                resp = protocol.success('account is not exist.', data={'id':aid})

            return resp

    def clear(self):
        """
            clear all account
        :return:
        """
        with self._lock:
            resp, data = None, []

            for id, account in self._accounts.items():
                # logout first
                res = account.logout()
                code, msg = res.get('status'), res.get('msg')
                # add data
                data.append({'id':id, 'code':code, 'msg':msg})

            # make response
            resp = protocol.success(data=data)

            # empty accounts
            self._accounts = {}

            return resp

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
                    res = account.login()
                    code, msg = res.get('status'), res.get('msg')
                    if code == 0:
                        resp = protocol.success(data={'id':aid, 'code':code, msg:msg})
                    else:
                        resp = protocol.failed(data={'id': aid, 'code': code, msg: msg})
                else:
                    resp = protocol.failed(data={'id':aid, 'code':-1, 'msg':'account not exist'})
            else:
                succeed, data = True, []
                # login all account
                for id, account in self._accounts.items():
                    res = account.login()
                    code, msg = res.get('status'), res.get('msg')
                    if code != 0:
                        succeed = False
                    data.append({'id': id, 'code': code, 'msg': msg})

                if succeed:
                    resp = protocol.success(data = data)
                else:
                    resp = protocol.failed(data = data)

            return resp

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
                    res = account.logout()
                    code, msg = res.get('status'), res.get('msg')
                    if code == 0:
                        resp = protocol.success(data={'id':aid, 'code':code, 'msg':msg})
                    else:
                        resp = protocol.failed(data={'id': aid, 'code': code, 'msg': msg})
                else:
                    resp = protocol.failed(data={'id':aid, 'code':-1, 'msg':'account not exist'})
            else:
                # all account logout
                succeed, data = True, []
                # login all account
                for id, account in self._accounts.items():
                    res = account.logout()
                    code, msg = res.get('status'), res.get('msg')
                    if code != 0:
                        succeed = False
                    data.append({'id': id, 'login': True, 'msg': msg})

                if succeed:
                    resp = protocol.success(data = data)
                else:
                    resp = protocol.failed(data = data)

            return resp

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
                    data = {'id':aid}
                    data.update(account.status())
                    resp = protocol.success(data=data)
                else:
                    resp = protocol.failed('account is not exist', data={'id':aid})
            else:
                stats = []
                for id, account in self._accounts.items():
                    data = account.status()
                    data['id'] = aid
                    stats.append(data)
                resp = protocol.success(data=stats)

            return resp

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
                resp = account.quote(zqdm)
            else:
                resp = protocol.failed('account not exist', data={'id':aid})
            return resp

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
                resp = account.query(type, sdate, edate)
            else:
                resp = protocol.failed('account not exist', data={'id':aid})
            return resp

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
                resp = account.place(otype, ptype, zqdm, price, count)
            else:
                resp = protocol.failed('account not exist', data={'id':aid})
            return resp

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
                resp = account.cancel(zqdm, orderno)
            else:
                resp = protocol.failed('account not exist', data={'id':aid})
            return resp
