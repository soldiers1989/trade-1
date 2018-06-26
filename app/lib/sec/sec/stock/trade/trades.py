"""
    trade service
"""
import threading
from sec.stock.trade import protocol


class Trades:
    def __init__(self):
        """
            init trade service
        """
        # account in trade service
        self._accounts = {}

        # lock for accounts
        self._lock = threading.RLock()

    def add(self, aid, account):
        """
            add account
        :param aid:
        :param account:
        :return:
        """
        resp = None

        self._lock.acquire()
        acnt = self._accounts.get(aid)
        self._accounts[aid] = account
        self._lock.release()

        if acnt is not None:
            resp = protocol.success('account has already exist, replaced.')
        else:
            resp = protocol.success('account has added')

        return resp

    def delete(self, aid):
        """
            delete account
        :param id:
        :return:
        """
        resp = None
        self._lock.acquire()
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
        self._lock.release()

        return resp

    def clear(self):
        """
            clear all account
        :return:
        """
        resp, data = None, []
        self._lock.acquire()

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

        self._lock.release()

        return resp

    def status(self, aid = None):
        """
            get account status
        :param aid:
        :return:
        """
        resp = None
        self._lock.acquire()
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

        self._lock.release()

        return resp

    def login(self, aid = None):
        """
            账户登录
        :param aid:
        :return:
        """
        resp = None
        self._lock.acquire()
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
        self._lock.release()

        return resp

    def logout(self, aid = None):
        """
            账户退出
        :param aid:
        :return:
        """
        resp = None
        self._lock.acquire()
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
        self._lock.release()

        return resp

    def query_dqzc(self, aid):
        """
            当前资产查询
        :param aid: in, account
        :return:
        """
        resp = None

        self._lock.acquire()
        account = self._accounts.get(aid)
        if account is not None:
            resp = account.query_dqzc()
        else:
            resp = protocol.failed('account not exist', data={'id':aid})
        self._lock.release()

        return resp

    def query_dqcc(self, aid):
        """
            当前持仓查询
        :param aid: in, account
        :return:
        """
        self._lock.acquire()
        account = self._accounts.get(aid)
        if account is not None:
            resp = account.query_dqcc()
        else:
            resp = protocol.failed('account not exist', data={'id':aid})
        self._lock.release()

        return resp

    def query_drwt(self, aid):
        """
            当日委托查询
        :param aid: in, account id
        :return:
        """
        self._lock.acquire()
        account = self._accounts.get(aid)
        if account is not None:
            resp = account.query_drwt()
        else:
            resp = protocol.failed('account not exist', data={'id':aid})
        self._lock.release()

        return resp

    def query_drcj(self, aid):
        """
            当日成交查询
        :param aid: in, account id
        :return:
        """
        self._lock.acquire()
        account = self._accounts.get(aid)
        if account is not None:
            resp = account.query_drcj()
        else:
            resp = protocol.failed('account not exist', data={'id':aid})
        self._lock.release()

        return resp

    def query_kcwt(self, aid):
        """
            可撤委托查询
        :param aid: in, account id
        :return:
        """
        self._lock.acquire()
        account = self._accounts.get(aid)
        if account is not None:
            resp = account.query_kcwt()
        else:
            resp = protocol.failed('account not exist', data={'id':aid})
        self._lock.release()

        return resp

    def query_gdxx(self, aid):
        """
            股东信息查询
        :param aid: in, account
        :return:
            (True, [gddm list]) or (False, error message)
        """
        self._lock.acquire()
        account = self._accounts.get(aid)
        if account is not None:
            resp = account.query_gdxx()
        else:
            resp = protocol.failed('account not exist', data={'id':aid})
        self._lock.release()

        return resp

    def query_lswt(self, aid, sdate, edate):
        """
            查询历史委托
        :param aid:
        :param sdate: str, in, format: yyyymmdd
        :param edate: str, in, format: yyyymmdd
        :return:
        """
        self._lock.acquire()
        account = self._accounts.get(aid)
        if account is not None:
            resp = account.query_lswt(sdate, edate)
        else:
            resp = protocol.failed('account not exist', data={'id':aid})
        self._lock.release()

        return resp

    def query_lscj(self, aid, sdate, edate):
        """
            查询历史成交
        :param aid:
        :param sdate: str, in, format: yyyymmdd
        :param edate: str, in, format: yyyymmdd
        :return:
        """
        self._lock.acquire()
        account = self._accounts.get(aid)
        if account is not None:
            resp = account.query_lscj(sdate, edate)
        else:
            resp = protocol.failed('account not exist', data={'id':aid})
        self._lock.release()

        return resp


    def query_jgd(self, aid, sdate, edate):
        """
            查询交割单
        :param aid:
        :param sdate: str, in, format: yyyymmdd
        :param edate: str, in, format: yyyymmdd
        :return:
        """
        self._lock.acquire()
        account = self._accounts.get(aid)
        if account is not None:
            resp = account.query_jgd(sdate, edate)
        else:
            resp = protocol.failed('account not exist', data={'id':aid})
        self._lock.release()

        return resp

    def query_gphq(self, aid, code):
        """
            查询股票行情
        :param aid: str, in, user account
        :param code: str, in, stock code
        :return:
        """
        self._lock.acquire()
        account = self._accounts.get(aid)
        if account is not None:
            resp = account.query_gphq(code)
        else:
            resp = protocol.failed('account not exist', data={'id':aid})
        self._lock.release()

        return resp

    def order_xjmr(self, aid, zqdm, price, count):
        """
            限价买入
        :param aid:
        :param zqdm:
        :param price:
        :param count:
        :return:
        """
        self._lock.acquire()
        account = self._accounts.get(aid)
        if account is not None:
            resp = account.order_xjmr(zqdm, price, count)
        else:
            resp = protocol.failed('account not exist', data={'id':aid})
        self._lock.release()

        return resp

    def order_xjmc(self, aid, zqdm, price, count):
        """
            限价卖出
        :param aid:
        :param zqdm:
        :param price:
        :param count:
        :return:
        """
        self._lock.acquire()
        account = self._accounts.get(aid)
        if account is not None:
            resp = account.order_xjmc(zqdm, price, count)
        else:
            resp = protocol.failed('account not exist', data={'id':aid})
        self._lock.release()

        return resp

    def order_sjmr(self, aid, zqdm, price, count):
        """
            市价买入
        :param aid:
        :param zqdm:
        :param price:
        :param count:
        :return:
        """
        self._lock.acquire()
        account = self._accounts.get(aid)
        if account is not None:
            resp = account.order_sjmr(zqdm, price, count)
        else:
            resp = protocol.failed('account not exist', data={'id':aid})
        self._lock.release()

        return resp

    def order_sjmc(self, aid, zqdm, price, count):
        """
            市价卖出
        :param aid:
        :param zqdm:
        :param price:
        :param count:
        :return:
        """
        self._lock.acquire()
        account = self._accounts.get(aid)
        if account is not None:
            resp = account.order_sjmc(zqdm, price, count)
        else:
            resp = protocol.failed('account not exist', data={'id':aid})
        self._lock.release()

        return resp

    def cancel_order(self, aid, orderno):
        """
            委托撤单
        :param aid:
        :param orderno:
        :return:
        """
        self._lock.acquire()
        account = self._accounts.get(aid)
        if account is not None:
            resp = account.cancel_order(orderno)
        else:
            resp = protocol.failed('account not exist', data={'id':aid})
        self._lock.release()

        return resp


