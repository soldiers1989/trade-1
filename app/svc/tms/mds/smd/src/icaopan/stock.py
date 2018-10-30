"""
    stock data
"""
import math, time
from . import client


class _Quote:
    """
        获取指定股票当前行情
        - 页面地址
            http://md.icaopan.com/openapi/queryMarketDataBySecurityCode?securityCode=000001&_=2312312312
        - 数据来源格式
           {
                "info": {
                    "rescode": "success",
                    "result": {
                        "amount": 1725932497.61,
                        "askPrice1": 10.76,
                        "askPrice2": 10.77,
                        "askPrice3": 10.78,
                        "askPrice4": 10.79,
                        "askPrice5": 10.8,
                        "askVolume1": 996,
                        "askVolume2": 1926,
                        "askVolume3": 1515,
                        "askVolume4": 2455,
                        "askVolume5": 4211,
                        "bidPrice1": 10.75,
                        "bidPrice2": 10.74,
                        "bidPrice3": 10.73,
                        "bidPrice4": 10.72,
                        "bidPrice5": 10.71,
                        "bidVolume1": 1716.05,
                        "bidVolume2": 900,
                        "bidVolume3": 881,
                        "bidVolume4": 531,
                        "bidVolume5": 394,
                        "dailyChange": -0.43,
                        "dailyChangePercent": -0.0385,
                        "downLimit": 10.06,
                        "earnings": 8.27,
                        "earnings2": 0,
                        "highPrice": 11.24,
                        "lastModifyTime": "2018-10-29 15:33:03",
                        "lastPrice": 10.75,
                        "lowPrice": 10.62,
                        "marketDataDateTime": "2018-10-29 15:33:03",
                        "openPrice": 11.2,
                        "preClosePrice": 11.18,
                        "stockCode": "000001",
                        "stockName": "平安银行",
                        "suspensionFlag": false,
                        "time": 1540798383000,
                        "upLimit": 12.3,
                        "volume": 159162878
                    }
                }
            }
        - 返回数据格式
            [
                 {
                    "zqdm":证券代码,
                    "jkj": 今开价, "zsj": 昨收价, "dqj": 当前价, "zgj": 最高价, "zdj": 最低价,
                    "cjl": 成交量, "cje": 成交额,
                    "mrl1": 买一量, "mrj1": ，买一价, "mrl2": 12, "mrj2": 13, "mrl3": 14, "mrj3": 15, "mrl4": 16, "mrj4": 17, "mrl5": 18, "mrj5": 19,
                    "mcl1": 卖一量, "mcj1": 卖一价, "mcl2": 22, "mcj2": 23, "mcl3": 24, "mcj3": 25, "mcl4": 26, "mcj4": 27, "mcl5": 28, "mcj5": 29,
                    "date": 日期, "time": 时间
                }
            ]
    """
    def __init__(self):
        pass

    def get(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        zqdm = kwargs.get('zqdm')
        if zqdm is None:
            raise ValueError('missing parameter zqdm')

        return self._get(zqdm)

    def _tidy(self, quote):
        """
            tidy quote data
        :param quote:
        :return:
        """
        # prices
        prices = ["jkj", "zsj", "dqj", "zgj", "zdj", "cje", "mrj1", "mrj2", "mrj3", "mrj4", "mrj5", "mcj1", "mcj2", "mcj3", "mcj4", "mcj5"]

        # volumes
        volumes = ["cjl", "mrl1", "mrl2", "mrl3", "mrl4", "mrl5", "mcl1", "mcl2", "mcl3", "mcl4", "mcl5"]

        # tidy prices
        for p in prices:
            if quote.get(p) is not None:
                quote[p] = quote[p]  # str(decimal.Decimal(quote[p]).quantize(decimal.Decimal('0.00')))

        # tidy volumes
        for v in volumes:
            if quote.get(v) is not None:
                quote[v] = int(quote[v])

        return quote

    def _parse(self, jsonobj):
        """
            parse response jsonobj
        :param jsonobj:
        :return:
        """
        # parse results
        results = []

        # alias for item
        alias = {
            "jkj": 'openPrice', "zsj": 'preClosePrice', "dqj": 'lastPrice', "zgj": 'highPrice', "zdj": 'lowPrice',
            "cjl": 'volume', "cje": 'amount',
            "mrl1": 'bidVolume1', "mrj1": 'bidPrice1', "mrl2": 'bidVolume2', "mrj2": 'bidPrice2', "mrl3": 'bidVolume3', "mrj3": 'bidPrice3', "mrl4": 'bidVolume4', "mrj4": 'bidPrice4', "mrl5": 'bidVolume5', "mrj5": 'bidPrice5',
            "mcl1": 'askVolume1', "mcj1": 'askPrice1', "mcl2": 'askVolume2', "mcj2": 'askPrice2', "mcl3": 'askVolume3', "mcj3": 'askPrice3', "mcl4": 'askVolume4', "mcj4": 'askPrice4', "mcl5": 'askVolume5', "mcj5": 'askPrice5',
            "time": 'lastModifyTime',
        }

        # quote items
        items = jsonobj['info']['result']
        # stock code
        code = items['stockCode']

        qte = {'zqdm': code, 'source': 'icaopan'}
        # stock quote
        for k in alias:
            qte[k] = items[alias[k]]

        # transfer volume
        qte['cjl'] = math.floor(qte['cjl'] / 100)

        # tidy quote
        qte = self._tidy(qte)

        # compute ztj&dtj
        qte['ztj'] = round(qte['zsj'] * 1.1, 2)
        qte['dtj'] = round(qte['zsj'] * 0.9, 2)

        return qte

    def _get(self, zqdm):
        """
            get one stock quotes
        :param zqdm: str, stock code
        :return:
            dict
        """
        results = []

        for code in zqdm.split(','):
            # make path
            path = "/openapi/queryMarketDataBySecurityCode?securityCode=" + zqdm + "&_=" + str(int(time.time() * 1000))
            # request data
            resp = client.md.get(path)
            # parse data
            results.append(self._parse(resp.json()))

        return results

quote = _Quote()
