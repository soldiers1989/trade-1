"""
    remote trade agent service wraper
"""
import requests, time
from .. import config
from . import protocol, util


class Account:
    """
        securities trade account
    """
    def __init__(self, laccount, lpwd, taccount, tpwd, dept, version, gddm):
        self.laccount = laccount
        self.lpwd = lpwd
        self.taccount = taccount
        self.tpwd = tpwd
        self.dept = dept
        self.version = version
        self.gddm = gddm

    def status(self):
        ret = {
            'laccount': self.laccount,
            'lpwd': self.lpwd,
            'taccount': self.taccount,
            'tpwd': self.tpwd,
            'detp': self.dept,
            'version': self.version,
            'gddm': self.gddm
        }
        return ret


class AgentServer:
    """
        remote agent server for trader
    """
    def __init__(self, id, host, port):
        self.id = id
        self.host = host
        self.port = port

    def status(self):
        return {
            'id': self.id,
            'host': self.host,
            'port': self.port
        }

    def url(self):
        return "http://%s:%s" % (self.host, self.port)


class TradeServer:
    """
        securities trade server
    """
    def __init__(self, id, ip, port):
        """
            init trader server
        :param ip:
        :param port:
        """
        self.id = id
        self.ip = ip
        self.port = port

        self.disabled = False
        self.errors = []

    def disable(self, error):
        """
            set server error message
        :param msg: str, error message
        :return:
        """
        # disable server
        self.disabled = True

        # error message
        err = {
            'time': time.time(),
            'error': error
        }

        # add error message
        self.errors.append(err)

    def status(self):
        return {
            'id': self.id,
            'ip': self.ip,
            'port': self.port,
            'disabled':self.disabled,
            'errors': self.errors
        }


class TradeServers:
    """
        securities trade servers
    """
    def __init__(self, servers):
        """
            init servers with servers[(ip, port), (ip, port), ...]
        :param servers: array, array with tuples(ip, port)
        """
        # usable trade servers
        self._servers = {}
        for id, ip, port in servers:
            self._servers[id] = TradeServer(id, ip, port)

        # current server index
        self._cindex = 0

    def pickone(self):
        """
            pick a trade server for trader
        :return:
        """
        for id in self._servers.keys():
            if not self._servers[id].disabled:
                return self._servers[id]
        return None

    def disable(self, id, error):
        """
            disable a server
        :param id:
        :param error:
        :return:
        """
        if self._servers.get(id) is None:
            return

        self._servers.get(id).disable(error)

    def status(self):
        results = []
        for server in self._servers.values():
            results.append(server.status())
        return results


class Trader:
    """
        a trader is correspond an remote agent server, disaster recovery by more than one trade servers
        when a trade server failed
    """
    def __init__(self, id, account, agentserver, tradeservers):
        """
            init trader
        :param account: obj, Account object
        :param agentserver: obj, Server object
        :param tradeservers: obj, Servers object
        """
        self._id = id
        self._account = account
        self._agents = agentserver
        self._tradess = tradeservers

        self._baseurl = self._agents.url()

        self.disabled = False
        self.errors = []

    def status(self):
        """
            get trader status
        :return:
        """
        stats = {
            'id': self._id,
            'disabled': self.disabled,
            'errors': self.errors,
            'agent': self._agents.status(),
            'servers': self._tradess.status()
        }

        return stats

    def login(self):
        """
            account login
        :return:
        """
        # make request url
        url = self._baseurl + "/login"

        # request parameters
        params = {
            "laccount": self._account.laccount,
            "lpwd": self._account.lpwd,
            "taccount": self._account.taccount,
            "tpwd": self._account.tpwd,
            "dept": self._account.dept,
            "version": self._account.version
        }

        # login to trader server
        server = self._tradess.pickone()
        while server is not None:
            # add trade server
            params["ip"] = server.ip
            params["port"] = server.port

            # request remote service
            resp = requests.get(url, params, timeout=config.TIMEOUT).json()
            if resp['status'] != 0:
                # disable server
                self._tradess.disable(server.id, resp['msg'])
                # pick a new one
                server = self._tradess.pickone()
            else:
                return resp

        # no usable trade server
        raise Exception(self._id+': no trade server usable for trader.')

    def logout(self):
        """
            account logout
        :return:
        """
        # make request url
        url = self._baseurl + "/logout"

        # request parameters
        params =  {
            "account": self._account.laccount
        }

        # request remote service
        resp = requests.get(url, params, timeout = config.TIMEOUT).json()

        # return response result
        return resp

    def disable(self, error):
        """
            disable trader
        :param error:
        :return:
        """
        # disable server
        self.disabled = True

        # error message
        err = {
            'time': time.time(),
            'error': error
        }

        # add error message
        self.errors.append(err)

    def request(self, url, params):
        """

        :param url:
        :param params:
        :return:
        """
        while True:
            # request remote service
            resp = requests.get(url, params, timeout=config.TIMEOUT).json()

            # login if error is not login
            if resp['status'] == protocol.status.ERROR_ACCOUNT_NOT_EXIST:
                self.login()
            else:
                return resp

    def queryc(self, type):
        """
            query current information of account
        :param type:
        :return:
        """
        # make request url
        url = self._baseurl + "/query/current"

        # request parameters
        params = {
            "account": self._account.laccount,
            "category": type
        }

        # request remote service
        resp = self.request(url, params)

        # return response result
        return resp

    def queryh(self, type, startdate, enddate):
        """
            query history information of account
        :param type:
        :param startdate:
        :param enddate:
        :return:
        """
        # make request url
        url = self._baseurl + "/query/history"

        # request parameters
        params = {
            "account": self._account.laccount,
            "category": type,
            "sdate": startdate,
            "edate": enddate
        }

        # request remote service
        resp = self.request(url, params)

        # return response result
        return resp

    def quote(self, zqdm):
        """
            query current quote of code
        :param zqdm:
        :return:
        """
        # make request url
        url = self._baseurl + "/query/quote"

        # request parameters
        params = {
            "account":self._account.laccount,
            "code" : zqdm
        }

        # request remote service
        resp = self.request(url, params)

        # return response result
        return resp

    def order(self, otype, ptype, zqdm, price, count):
        """
            send an order
        :param otype:
        :param ptype:
        :param zqdm:
        :param price:
        :param count:
        :return:
        """
        # make request url
        url = self._baseurl + "/send/order"

        # get gddm
        seid = util.getse(zqdm)
        if seid is None:
            return protocol.failed('invalid securities code: %s'%zqdm)
        gddm = self._account['gddm'].get(seid)
        if gddm is None:
            return protocol.failed('invalid securities code: %s' % zqdm)

        # request parameters
        params = {
            "account":self._account.laccount,
            "otype" : otype,
            "ptype" : ptype,
            "zqdm" : zqdm,
            "gddm" : self._account['gddm'][util.getse(zqdm)],
            "price" : price,
            "count" : count
        }

        # request remote service
        resp = self.request(url, params)

        # return response result
        return resp

    def cancel(self, seid, orderno):
        """
            cancel an order
        :param seid:
        :param orderno:
        :return:
        """
        # make request url
        url = self._baseurl + "/cancel/order"

        # request parameters
        params = {
            "account":self._account.laccount,
            "seid" : seid,
            "orderno" : orderno
        }

        # request remote service
        resp = self.request(url, params)

        # return response result
        return resp

    def echo(self):
        """
            agent echo
        :return:
        """
        # make request url
        url = self._baseurl + "/echo"

        # request parameters
        params =  {}

        # request remote service
        resp = requests.get(url, params, timeout = config.TIMEOUT).json()

        # return response result
        return resp


class Traders:
    """
        traders for an trade account for disaster recovery using different remote agent server
    """
    def __init__(self, account, agentservers, tradeservers):
        """
            init traders
        :param account:
        :param agentservers:
        :param tradeservers:
        """
        # init traders
        self._traders = {}
        for id, host, port in agentservers:
            self._traders[id] = Trader(id, account, AgentServer(id, host, port), TradeServers(tradeservers))

        # current trader
        self._trader = self.pickone()

    def status(self):
        results = []
        for trader in self._traders.values():
            results.append(trader.status())
        return results

    def login(self):
        """
            account login
        :return:
        """
        while self._trader is not None:
            try:
                return self._trader.login()
            except Exception as e:
                # disable current trader
                self._trader.disable(str(e))
                # pick a new trader
                self._trader = self.pickone()

        # no more trader can be used
        raise Exception("no trader usable for account")

    def logout(self):
        """
            account logout
        :return:
        """
        while self._trader is not None:
            try:
                return self._trader.logout()
            except Exception as e:
                # disable current trader
                self._trader.disable(str(e))
                # pick a new trader
                self._trader = self.pickone()

        # no more trader can be used
        raise Exception("no trader usable for account")


    def queryc(self, type):
        """
            query current information of account
        :param type:
        :return:
        """
        while self._trader is not None:
            try:
                return self._trader.queryc(type)
            except Exception as e:
                # disable current trader
                self._trader.disable(str(e))
                # pick a new trader
                self._trader = self.pickone()

        # no more trader can be used
        raise Exception("no trader usable for account")

    def queryh(self, type, startdate, enddate):
        """
            query history information of account
        :param type:
        :param startdate:
        :param enddate:
        :return:
        """
        while self._trader is not None:
            try:
                return self._trader.queryh(type, startdate, enddate)
            except Exception as e:
                # disable current trader
                self._trader.disable(str(e))
                # pick a new trader
                self._trader = self.pickone()

        # no more trader can be used
        return Exception("no trader usable for account")

    def quote(self, zqdm):
        """
            query current quote of code
        :param zqdm:
        :return:
        """
        while self._trader is not None:
            try:
                return self._trader.quote(zqdm)
            except Exception as e:
                # disable current trader
                self._trader.disable(str(e))
                # pick a new trader
                self._trader = self.pickone()

        # no more trader can be used
        raise Exception("no trader usable for account")

    def order(self, otype, ptype, zqdm, price, count):
        """
            send an order
        :param otype:
        :param ptype:
        :param zqdm:
        :param price:
        :param count:
        :return:
        """
        while self._trader is not None:
            try:
                return self._trader.order(otype, ptype, zqdm, price, count)
            except Exception as e:
                # disable current trader
                self._trader.disable(str(e))
                # pick a new trader
                self._trader = self.pickone()

        # no more trader can be used
        return Exception("no trader usable for account")

    def cancel(self, seid, orderno):
        """
            cancel an order
        :param seid:
        :param orderno:
        :return:
        """
        while self._trader is not None:
            try:
                return self._trader.cancel(seid, orderno)
            except Exception as e:
                # disable current trader
                self._trader.disable(str(e))
                # pick a new trader
                self._trader = self.pickone()

        # no more trader can be used
        return Exception("no trader usable for account")

    def echo(self):
        """
            agent echo
        :return:
        """
        while self._trader is not None:
            try:
                return self._trader.echo()
            except Exception as e:
                # disable current trader
                self._trader.disable(str(e))
                # pick a new trader
                self._trader = self.pickone()

        # no more trader can be used
        return Exception("no trader usable for account")

    def pickone(self):
        """
            pick one usable trader
        :return:
        """
        for id in self._traders:
            if not self._traders[id].disabled:
                return self._traders[id]

        return None
