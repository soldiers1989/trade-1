"""
    stock data from list
"""
import io, pandas, random

from . import client
from ... import fetch

class _List(fetch.Fetcher):
    """
        获取所有股票列表，页面地址：http://www.szse.cn/market/stock/list/index.html，原始数据格式：
        '公司代码', '公司简称', '公司全称', '英文名称', '注册地址', 'A股代码', 'A股简称', 'A股上市日期', 'A股总股本', 'A股流通股本',
        'B股代码', 'B股 简 称', 'B股上市日期', 'B股总股本', 'B股流通股本',   '地区', '省份', '城市', '所属行业', '公司网址'
    """
    # path for stock list
    PATH = '/api/report/ShowReport?SHOWTYPE=xlsx&CATALOGID=1110&TABKEY=tab1&random=%s'

    def __init__(self, clt=client.api):
        """
            init fetch stock list object
        :param clt: obj, http client object
        """
        self._client = clt

    @staticmethod
    def parse(record):
        """
            parse one record
        :param record:
        :return:
        """
        # alias for source to target
        alias = {
            'zqdm': 'A股代码', 'zqmc': 'A股简称', 'ssrq': 'A股上市日期', 'zgb': 'A股总股本', 'ltgb': 'A股流通股本'
        }

        result = {}
        # translate record by alias
        for key in alias.keys():
            result[key] = record[alias[key]]

        return result

    def fetch(self):
        """
            fetch stock list
        :return:
        """
        results = []

        # make path
        path = self.PATH % str(random.random())

        # request page data
        resp = self._client.get(path)

        # parse response data
        df = pandas.read_excel(io.BytesIO(resp.content), dtype=object, encoding='gbk')

        for index, row in df.iterrows():
            results.append(self.parse(row))

        return results


list = _List()
