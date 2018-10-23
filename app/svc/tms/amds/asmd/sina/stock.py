"""
    stock data from sina
"""
import time
from . import client
from .. import fetch


class _Quote(fetch.Fetcher):
    """
        获取所有股票当前行情，页面地址：http://vip.stock.finance.sina.com.cn/mkt/#hs_a
    """
    # path for get market quote
    PATH = '/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?sort=symbol&asc=1&symbol=&_s_r_a=page&num=40&page=%d&node=hs_a#"'

    def __init__(self, clt=client.vip):
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
            'code': 'code', 'name': 'name',
            'dqj': 'trade', 'mrj1': 'buy', 'mcj1': 'sell',
            'zsj': 'settlement', 'jkj': 'open', 'zgj': 'high', 'zdj': 'low',
            'cjl': 'volume', 'cje': 'amount',
            'zde': 'pricechange', 'zdf': 'changepercent',
            'tm': 'ticktime'
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

        page = 1
        while page < 120:
            # generate current page url
            path = self.PATH % page

            # request page data
            resp = self._client.get(path)

            # translate to json object
            records = self.json(resp.text)
            if records == 'null':
                break;

            # parse records
            for record in records:
                results.append(self.parse(record))

            # sleep for a while
            time.sleep(1)

            # fetch next page
            page = page + 1

        return results

quote = _Quote
