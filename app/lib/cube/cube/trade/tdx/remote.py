"""
    remote service request wraper
"""
import requests
from lib.trade.tdx import config

class Remote:
    def __init__(self, host, port):
        self._host = host
        self._port = port

    def login(self, account, pwd, ip, port, dept, version):
        """
            account login
        :param account:
        :param pwd:
        :param ip:
        :param port:
        :param dept:
        :param version:
        :return:
        """
        # make request url
        url = "http://%s:%s/login" % (self._host, self._port)

        # request parameters
        params = {
            "account":account,
            "pwd" : pwd,
            "ip" : ip,
            "port" : port,
            "dept" : dept,
            "version" : version
        }

        # request remote service
        resp = requests.get(url, params, timeout=config.TIMEOUT).json()

        # get response result
        status, msg = resp["status"], resp["msg"]
        status = True if status is 0 else False

        # return response result
        return status, msg


    def query1(self, account, type):
        """
            query current information of account
        :param account:
        :param type:
        :return:
        """
        # make request url
        url = "http://%s:%s/query/current" % (self._host, self._port)

        # request parameters
        params = {
            "account": account,
            "category": type
        }

        # request remote service
        resp = requests.get(url, params, timeout=config.TIMEOUT).json()

        # get response result
        status, msg, data = resp["status"], resp["msg"], resp["data"]
        status = True if status is 0 else False

        # return response result
        return status, msg, data

    def query2(self, account, type, startdate, enddate):
        """
            query history information of account
        :param account:
        :param type:
        :param startdate:
        :param enddate:
        :return:
        """
        # make request url
        url = "http://%s:%s/query/history" % (self._host, self._port)

        # request parameters
        params = {
            "account": account,
            "category": type,
            "sdate": startdate,
            "edate": enddate
        }

        # request remote service
        resp = requests.get(url, params, timeout = config.TIMEOUT).json()

        # get response result
        status, msg, data = resp["status"], resp["msg"], resp["data"]
        status = True if status is 0 else False

        # return response result
        return status, msg, data

    def quote(self, account, code, market):
        """
            query current quote of code
        :param account:
        :param code:
        :return:
        """
        # make request url
        url = "http://%s:%s/query/quote" % (self._host, self._port)

        # request parameters
        params = {
            "account":account,
            "code" : code,
            "market": market
        }

        # request remote service
        resp = requests.get(url, params, timeout = config.TIMEOUT).json()

        # get response result
        status, msg, data = resp["status"], resp["msg"], resp["data"]
        status = True if status is 0 else False

        # return response result
        return status, msg, data

    def order(self, account, otype, ptype, gddm, zqdm, price, count):
        """
            send an order
        :param account:
        :param otype:
        :param ptype:
        :param gddm:
        :param zqdm:
        :param price:
        :param count:
        :return:
        """
        # make request url
        url = "http://%s:%s/send/order" % (self._host, self._port)
        # request parameters
        params = {
            "account":account,
            "otype" : otype,
            "ptype" : ptype,
            "gddm" : gddm,
            "zqdm" : zqdm,
            "price" : price,
            "count" : count
        }

        # request remote service
        resp = requests.get(url, params, timeout = config.TIMEOUT).json()

        # get response result
        status, msg, data = resp["status"], resp["msg"], resp["data"]
        status = True if status is 0 else False

        # return response result
        return status, msg, data

    def cancel(self, account, orderno, seid):
        """
            cancel an order
        :param account:
        :param orderno:
        :param seid:
        :return:
        """
        # make request url
        url = "http://%s:%s/cancel/order" % (self._host, self._port)
        # request parameters
        params = {
            "account":account,
            "seid" : seid,
            "orderno" : orderno
        }

        # request remote service
        resp = requests.get(url, params, timeout = config.TIMEOUT).json()

        # get response result
        status, msg, data = resp["status"], resp["msg"], resp["data"]
        status = True if status is 0 else False

        # return response result
        return status, msg, data

    def logout(self, account):
        """
            account logout
        :param account:
        :return:
        """
        # make request url
        url = "http://%s:%s/logout" % (self._host, self._port)

        # request parameters
        params =  {
            "account": account
        }

        # request remote service
        resp = requests.get(url, params, timeout = config.TIMEOUT).json()

        # get response result
        status, msg = resp["status"], resp["msg"]
        status = True if status is 0 else False

        # return response result
        return status, msg

if __name__ == "__main__":
    remote = Remote("172.16.21.135", "80")
    res = remote.login("030000012782", "013579", "116.228.234.71",  7708, 1, "7.38")
    print(res)

    res = remote.query1("030000012782", "0")
    print(res)

    res = remote.logout("030000012782")
    print(res)