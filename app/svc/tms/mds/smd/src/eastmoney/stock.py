"""
    stock data
"""
import json, time, decimal
from . import client
from .. import util


class _Quote:
    """
        获取指定股票当前行情
        - 页面地址
            http://nuff.eastmoney.com/EM_Finance2015TradeInterface/JS.ashx?id=0000012&token=4f1862fc3b5e77c150a2b985b12db0fd&_=2313
        - 数据来源格式
            {
                "Comment": [],
                "Value": [
                    "2",
                    "000001",
                    "平安银行",
                    "10.75",
                    "10.74",
                    "10.73",
                    "10.72",
                    "10.71",
                    "10.76",
                    "10.77",
                    "10.78",
                    "10.79",
                    "10.80",
                    "1716",
                    "900",
                    "881",
                    "531",
                    "394",
                    "996",
                    "1926",
                    "1515",
                    "2455",
                    "4211",
                    "12.30",
                    "10.06",
                    "10.75",
                    "10.84",
                    "-0.43",
                    "11.20",
                    "-3.85",
                    "11.24",
                    "1591629",
                    "10.62",
                    "12783",
                    "11.18",
                    "17.3亿",
                    "0.88",
                    "0.93",
                    "6.77",
                    "577145",
                    "1014483",
                    "-43.03",
                    "-6681",
                    "0.86",
                    "1",
                    "184580151552",
                    "184581922184",
                    "0|0|0|0|0",
                    "0|0|0|0|0",
                    "2018-10-29 15:38:06",
                    "5.55",
                    "-",
                    "-"
                ]
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
                quote[p] = round(float(quote[p]), 2)  # str(decimal.Decimal(quote[p]).quantize(decimal.Decimal('0.00')))

        # tidy volumes
        for v in volumes:
            if quote.get(v) is not None:
                quote[v] = int(quote[v])

        return quote

    def _parse(self, text):
        """
            parse response text
        :param text:
        :return:
        """
        # parse results
        results = []

        # alias for item
        alias = {
            "jkj": 28, "zsj": 34, "dqj": 25, "zgj": 30, "zdj": 32,
            "cjl": 31, "cje": 35,
            "mrl1": 13, "mrj1": 3, "mrl2": 14, "mrj2": 4, "mrl3": 15, "mrj3": 5, "mrl4": 16, "mrj4": 6, "mrl5": 17, "mrj5": 7,
            "mcl1": 18, "mcj1": 8, "mcl2": 19, "mcj2": 9, "mcl3": 20, "mcj3": 10, "mcl4": 21, "mcj4": 11, "mcl5": 22, "mcj5": 12,
            "time": 49,
        }

        # parse response quote
        rpos = text.find('(') + 1
        text = text[rpos:].rstrip().rstrip(')')

        # quote items
        items = json.loads(text)['Value']
        # stock code
        code = items[1]

        qte = {'zqdm':code}
        # stock quote
        for k in alias:
            qte[k] = items[alias[k]]

        # process cje
        unit = qte['cje'][-1:]
        unit = 100000000 if unit == '亿' else 10000 if unit == '万' else 1
        qte['cje'] = str(decimal.Decimal(qte['cje'][:-1]) * unit)

        # tidy result
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
        # generate token
        token = "4f1862fc3b5e77c150a2b985b12db0fd"

        results = []

        for code in zqdm.split(','):
            # generate id by code
            id = code + "1" if util.getse(code) == 'sh' else code + "2"

            # make path
            path = "/EM_Finance2015TradeInterface/JS.ashx?id=" + id + "&token=" + token + "&_=" + str(int(time.time() * 1000))
            # request data
            resp = client.md.get(path)
            # parse data
            results.append(self._parse(resp.text))

        return results

quote = _Quote()
