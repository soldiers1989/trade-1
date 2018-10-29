"""
    stock data
"""
import math, random, json, time
from . import client
from .. import util


class _Quote:
    """
        获取指定股票当前行情
        - 页面地址
            http://hq.finance.ifeng.com/q.php?l=sz000001,sz000725&f=json&r=0.5896401872698729
        - 数据来源格式
            var json_q={
            "sz000001":[10.67,11.18,-0.51,-4.56,11.20,11.24,10.64,10.66,10.67,134331248.00,1459893760.00,10.66,10.65,10.64,10.63,10.62,97200.00,725300.00,344700.00,420700.00,754400.00,10.67,10.68,10.69,10.70,10.71,184000.00,326459.00,168000.00,356093.00,57900.00,0.00,0.00,0.00,1540793532,1540764732,0.00],
            "sz000725":[2.77,2.79,-0.02,-0.72,2.80,2.82,2.76,2.77,2.78,233507696.00,650987200.00,2.77,2.76,2.75,2.74,2.73,6765100.00,9575100.00,7972300.00,2559100.00,2779800.00,2.78,2.79,2.80,2.81,2.82,1393400.00,4277369.00,10381800.00,9973192.00,11834300.00,0.00,0.00,0.00,1540793532,1540764732,0.00]};
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
                quote[v] = math.floor(int(quote[v]) / 100)

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
            "jkj": 4, "zsj": 1, "dqj": 0, "zgj": 5, "zdj": 6,
            "cjl": 9, "cje": 10,
            "mrl1": 16, "mrj1": 11, "mrl2": 17, "mrj2": 12, "mrl3": 18, "mrj3": 13, "mrl4": 19, "mrj4": 14, "mrl5": 20, "mrj5": 15,
            "mcl1": 26, "mcj1": 21, "mcl2": 27, "mcj2": 22, "mcl3": 28, "mcj3": 23, "mcl4": 29, "mcj4": 24, "mcl5": 30, "mcj5": 25,
            "time": 34,
        }

        # parse all response quotes
        rpos = text.find('=') + 1
        text = text[rpos:].rstrip().rstrip(';')
        quotes = json.loads(text)

        # parse each quote
        for stock in quotes:
            # stock code
            code = stock[-6:]

            # quote items
            items = quotes[stock]

            qte = {'zqdm': code}

            # stock quote
            for k in alias:
                qte[k] = items[alias[k]]

            # translate time from unix timestamp to datetime
            qte['time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(qte['time']))

            # tidy quote
            qte = self._tidy(qte)

            # compute ztj&dtj
            qte['ztj'] = round(qte['zsj'] * 1.1, 2)
            qte['dtj'] = round(qte['zsj'] * 0.9, 2)

            # add to results
            results.append(qte)

        return results


    def _get(self, zqdm):
        """
            get one stock quotes
        :param zqdm: str, stock code
        :return:
            dict
        """
        # make path
        path = "/q.php?l=" + ','.join(util.addse(zqdm.split(','))) + "&f=json&r=" + str(random.random())

        # request data
        resp = client.hqfinance.get(path)

        # parse data
        return self._parse(resp.text)

quote = _Quote()


class _KData:
    def __init__(self):
        pass

    def get(self, **kwargs):
        """
            获取K线数据
        :param kwargs:
                zqdm: 证券代码
                type: d-日线, w-周, m-月, 5-5分钟, 15-15分钟, 30-30分钟, 60-60分钟
        :return:
            list, 格式:
            [{time:时间, kpj:开盘价, spj: 收盘价, zgj: 最高价, zdj: 最低价, zde: 涨跌额, zdf: 涨跌幅, cjl: 成交量, hsl: 换手率}, ... ]

        """
        # url templates
        urltpls = {
            'd': '/akdaily/?code=%s&type=last',
            'w': '/akweekly/?code=%s&type=last',
            'm': '/akmonthly/?code=%s&type=last',
            '5': '/akmin?scode=%s&type=5',
            '15': '/akmin?scode=%s&type=15',
            '30': '/akmin?scode=%s&type=30',
            '60': '/akmin?scode=%s&type=60'
        }

        # get parameters
        zqdm, type = kwargs.get('zqdm'), kwargs.get('type')
        if zqdm is None or type is None:
            raise ValueError('parameters zqdm and type must not be none')
        zqdm, type = util.addse(zqdm), type.lower()
        if type not in urltpls.keys():
            raise ValueError('k-data type %s not support in <d, w, m, 5, 15, 30, 60>' % type)

        # request path
        path = urltpls[type] % zqdm

        # request data
        resp = client.apifinance.get(path)

        # parse data
        results = self._parse(resp.text)

        return results

    def _parse(self, text):
        """
            解析每条数据记录
        :param record:
        :return:
        """
        # convert text
        objs = util.json(text)

        # get records
        records = objs['record']

        results = []
        # parse each records
        for record in records:
            results.append({
                'time': record[0],
                'kpj': record[1],
                'spj': record[3],
                'zgj': record[2],
                'zdj': record[4],
                'zde': record[6],
                'zdf': record[7],
                'cjl': record[5],
                'hsl': None if len(record)<15 else record[14]
            })

        return results

kdata = _KData()