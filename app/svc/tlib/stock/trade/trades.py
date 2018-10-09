"""
    trade service
"""
import threading, decimal
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
                raise error.TradeError('account with id: %s has exists.' % aid)

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

    def quote(self, aid:str, zqdm:str):
        """
            get current quote of stock by @code
        :param aid: str, account id
        :param zqdm: str, stock code
        :return:
            dict
        """
        return self.query_gphq(aid, zqdm)

    def query(self, aid:str, type:str, sdate:str=None, edate:str=None):
        """
            query account data by specified type
        :param aid: str, account id
        :param type: str, data type: dqzc/dqcc/drwt/drcj/kcwt/gdxx/lswt/lscj/jgd
        :return:
            list/dict
        """
        if type == 'dqzc':
            return self.query_dqzc(aid)
        elif type == 'dqcc':
            return self.query_dqcc(aid)
        elif type == 'drwt':
            return self.query_drwt(aid)
        elif type == 'drcj':
            return self.query_drcj(aid)
        elif type == 'kcwt':
            return self.query_kcwt(aid)
        elif type == 'gdxx':
            return self.query_gdxx(aid)
        elif type == 'lswt':
            return self.query_lswt(aid, sdate, edate)
        elif type == 'lscj':
            return self.query_lscj(aid, sdate, edate)
        elif type == 'jgd':
            return self.query_jgd(aid, sdate, edate)
        else:
            return protocol.failed('query type %s not support'%type, data={'aid':aid})

    def place(self, aid:str, otype:str, ptype:str, code:str, price:str|decimal.Decimal, count:str|int):
        """
            委托订单
        :param aid: account id
        :param otype: order type: buy/sell
        :param ptype: price type: xj/sj
        :param code: stock code
        :param price: order price
        :param count: order count
        :return:
        """
        if otype == 'buy':
            if ptype == 'xj':
                return self.order_xjmr(aid, code, price, count)
            elif ptype == 'sj':
                return self.order_sjmr(aid, code, price, count)
            else:
                return protocol.failed('place price type %s not support' % otype, data={'aid': aid})
        elif otype == 'sell':
            if ptype == 'xj':
                return self.order_xjmc(aid, code, price, count)
            elif ptype == 'sj':
                return self.order_sjmc(aid, code, price, count)
            else:
                return protocol.failed('place price type %s not support' % otype, data={'aid': aid})
        else:
            return protocol.failed('place order type %s not support'%otype, data={'aid':aid})

    def cancel(self, aid, zqdm, orderno):
        """
            委托撤单
        :param aid: str, account id
        :param zqdm: str, stock code
        :param orderno: str, order number
        :return:
        """
        return self.cancel_order(aid, zqdm, orderno)

    def query_dqzc(self, aid):
        """
            当前资产查询
        :param aid: in, account
        :return:
        """
        with self._lock:
            account = self._accounts.get(aid)
            if account is not None:
                resp = account.query_dqzc()
            else:
                resp = protocol.failed('account not exist', data={'id':aid})
            return resp

    def query_dqcc(self, aid):
        """
            当前持仓查询
        :param aid: in, account
        :return:
        """
        with self._lock:
            account = self._accounts.get(aid)
            if account is not None:
                resp = account.query_dqcc()
            else:
                resp = protocol.failed('account not exist', data={'id':aid})

            return resp

    def query_drwt(self, aid):
        """
            当日委托查询
        :param aid: in, account id
        :return:
        """
        with self._lock:
            account = self._accounts.get(aid)
            if account is not None:
                resp = account.query_drwt()
            else:
                resp = protocol.failed('account not exist', data={'id':aid})

            return resp

    def query_drcj(self, aid):
        """
            当日成交查询
        :param aid: in, account id
        :return:
        """
        with self._lock:
            account = self._accounts.get(aid)
            if account is not None:
                resp = account.query_drcj()
            else:
                resp = protocol.failed('account not exist', data={'id':aid})

            return resp

    def query_kcwt(self, aid):
        """
            可撤委托查询
        :param aid: in, account id
        :return:
        """
        with self._lock:
            account = self._accounts.get(aid)
            if account is not None:
                resp = account.query_kcwt()
            else:
                resp = protocol.failed('account not exist', data={'id':aid})

            return resp

    def query_gdxx(self, aid):
        """
            股东信息查询
        :param aid: in, account
        :return:
            (True, [gddm list]) or (False, error message)
        """
        with self._lock:
            account = self._accounts.get(aid)
            if account is not None:
                resp = account.query_gdxx()
            else:
                resp = protocol.failed('account not exist', data={'id':aid})

            return resp

    def query_lswt(self, aid, sdate, edate):
        """
            查询历史委托
        :param aid:
        :param sdate: str, in, format: yyyymmdd
        :param edate: str, in, format: yyyymmdd
        :return:
        """
        with self._lock:
            account = self._accounts.get(aid)
            if account is not None:
                resp = account.query_lswt(sdate, edate)
            else:
                resp = protocol.failed('account not exist', data={'id':aid})

            return resp

    def query_lscj(self, aid, sdate, edate):
        """
            查询历史成交
        :param aid:
        :param sdate: str, in, format: yyyymmdd
        :param edate: str, in, format: yyyymmdd
        :return:
        """
        with self._lock:
            account = self._accounts.get(aid)
            if account is not None:
                resp = account.query_lscj(sdate, edate)
            else:
                resp = protocol.failed('account not exist', data={'id':aid})

            return resp


    def query_jgd(self, aid, sdate, edate):
        """
            查询交割单
        :param aid:
        :param sdate: str, in, format: yyyymmdd
        :param edate: str, in, format: yyyymmdd
        :return:
        """
        with self._lock:
            account = self._accounts.get(aid)
            if account is not None:
                resp = account.query_jgd(sdate, edate)
            else:
                resp = protocol.failed('account not exist', data={'id':aid})

            return resp

    def query_gphq(self, aid, code):
        """
            查询股票行情
        :param aid: str, in, user account
        :param code: str, in, stock code
        :return:
        """
        with self._lock:
            account = self._accounts.get(aid)
            if account is not None:
                resp = account.query_gphq(code)
            else:
                resp = protocol.failed('account not exist', data={'id':aid})

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
        with self._lock:
            account = self._accounts.get(aid)
            if account is not None:
                resp = account.order_xjmr(zqdm, price, count)
            else:
                resp = protocol.failed('account not exist', data={'id':aid})

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
        with self._lock:
            account = self._accounts.get(aid)
            if account is not None:
                resp = account.order_xjmc(zqdm, price, count)
            else:
                resp = protocol.failed('account not exist', data={'id':aid})

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
        with self._lock:
            account = self._accounts.get(aid)
            if account is not None:
                resp = account.order_sjmr(zqdm, price, count)
            else:
                resp = protocol.failed('account not exist', data={'id':aid})

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
        with self._lock:
            account = self._accounts.get(aid)
            if account is not None:
                resp = account.order_sjmc(zqdm, price, count)
            else:
                resp = protocol.failed('account not exist', data={'id':aid})

            return resp

    def cancel_order(self, aid, zqdm, orderno):
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
                resp = account.cancel_order(zqdm, orderno)
            else:
                resp = protocol.failed('account not exist', data={'id':aid})

        return resp
