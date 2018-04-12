"""
    remote service request wraper
"""
import requests
from lib.quote.tdx import config


class Remote:
    def __init__(self, host, port):
        self._host = host
        self._port = port

    def connect(self, ip, port):
        """
            连接行情服务器
        :param ip: str, in, remote quote server ip
        :param port: int, in, remote quote server port
        :return:
        """
        # make request url
        url = "http://%s:%s/connect" % (self._host, self._port)

        # request parameters
        params = {
            "ip": ip,
            "port" : port
        }

        # request remote service
        resp = requests.get(url, params, timeout=config.TIMEOUT).json()

        # get response result
        status, msg = resp["status"], resp["msg"]
        status = True if status is 0 else False

        # return response result
        return status, msg

    def count(self, market):
        """
            查询证券数量
        :param market: str, in, 0 - shenzhen, 1 - shanghai
        :return:
        """
        # make request url
        url = "http://%s:%s/count" % (self._host, self._port)

        # request parameters
        params = {
            "market": market,
        }

        # request remote service
        resp = requests.get(url, params, timeout=config.TIMEOUT).json()

        # get response result
        status, msg, data = resp["status"], resp["msg"], resp["data"]
        status = True if status is 0 else False

        # return response result
        return status, msg, data

    def list(self, market, start):
        """
            查询证券列表
        :param market: str, in, 0 - shenzhen, 1 - shanghai
        :param start: int, in, list start position from 0
        :return:
        """
        # make request url
        url = "http://%s:%s/list" % (self._host, self._port)

        # request parameters
        params = {
            "market": market,
            "start": start
        }

        # request remote service
        resp = requests.get(url, params, timeout=config.TIMEOUT).json()

        # get response result
        status, msg, data = resp["status"], resp["msg"], resp["data"]
        status = True if status is 0 else False

        # return response result
        return status, msg, data

    def quote(self, market, zqdm):
        """
            查询当前行情
        :param market: str, in, 0 - shenzhen, 1 - shanghai
        :param zqdm: str, in, stock code
        :return:
        """
        # make request url
        url = "http://%s:%s/quote" % (self._host, self._port)

        # request parameters
        params = {
            "zqdm": zqdm,
            "market": market
        }

        # request remote service
        resp = requests.get(url, params, timeout=config.TIMEOUT).json()

        # get response result
        status, msg, data = resp["status"], resp["msg"], resp["data"]
        status = True if status is 0 else False

        # return response result
        return status, msg, data

    def disconnect(self):
        """
            断开行情服务器
        :return:
        """
        # make request url
        url = "http://%s:%s/disconnect" % (self._host, self._port)

        # request parameters
        params = { }

        # request remote service
        resp = requests.get(url, params, timeout=config.TIMEOUT).json()

        # get response result
        status, msg = resp["status"], resp["msg"]
        status = True if status is 0 else False

        # return response result
        return status, msg
