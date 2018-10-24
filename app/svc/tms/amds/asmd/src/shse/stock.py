"""
    stock data from list
"""
import io, pandas

from . import client
from ... import fetch

class _List(fetch.Fetcher):
    """
        获取所有股票列表，页面地址：http://www.sse.com.cn/assortment/stock/list/share/，原始数据格式：

        公司代码 	公司简称 	A股代码	A股简称	A股上市日期	A股总股本	A股流通股本
        600000	  浦发银行	  600000	  浦发银行	  1999-11-10	  2935208.04  2810376.39
        600004	  白云机场	  600004	  白云机场	  2003-04-28	  206932.05	  206932.05
        600006	  东风汽车	  600006	  东风汽车	  1999-07-27	  200000.00	  200000.00
        600007	  中国国贸	  600007	  中国国贸	  1999-03-12	  100728.25	  100728.25
        600008	  首创股份	  600008	  首创股份	  2000-04-27	  482061.41	  482061.41
    """
    # path for stock list
    PATH = '/security/stock/downloadStockListFile.do?csrcCode=&stockCode=&areaName=&stockType=1'

    def __init__(self, clt=client.query):
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

        # request page data
        resp = self._client.get(self.PATH)

        # parse response data
        df = pandas.read_csv(io.StringIO(resp.text), sep='\s+', dtype=object)

        for index, row in df.iterrows():
            results.append(self.parse(row))

        return results


list = _List()
