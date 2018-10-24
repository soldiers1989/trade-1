"""
    stock data from sina
"""
import io, time, lxml, lxml.html, pandas

from . import client, config
from .. import util
from ... import fetch


class _QuoteAll(fetch.Fetcher):
    """
        获取所有股票当前行情，页面地址：http://vip.stock.finance.sina.com.cn/mkt/#hs_a
        数据源格式：
        [{
            symbol:"sh600000",code:"600000",name:"浦发银行",trade:"10.710",
            pricechange:"0.260",changepercent:"2.488",buy:"10.700",sell:"10.710",
            settlement:"10.450",open:"10.570",high:"10.730",low:"10.520",volume:12905082,
            amount:137763231,ticktime:"10:08:02",per:5.821,pb:0.765,mktcap:31436078.105187,
            nmc:30098757.892329,turnoverratio:0.04592
        }]

        归一化格式：
        [
            {
                code: 股票代码, name: 股票名称,
                dqj: 当前价格, mrj1: 买一价, mcj: 卖一价
                zsj: 昨收价, jkj: 今开价, zgj: 最高价, zdj: 最低价,
                cjl: 成交量, cje: 成交额, zde: 涨跌额, zdf: 涨跌幅, hsl: 换手率,
                syl: 市盈率, sjl: 市净率, zsz: 总市值, ltsz: 流通市值,
                tm: tick时间
            }
        ]
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
            'zde': 'pricechange', 'zdf': 'changepercent', 'hsl': 'turnoverratio',
            'syl': 'per', 'sjl': 'pb', 'zsz': 'mktcap', 'ltsz': 'nmc',
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

quote_all = _QuoteAll


class _Ticks(fetch.Fetcher):
    """
        获取指定股票和日期的逐笔委托记录
    """
    def __init__(self, clt=client.vip, pinterval=config.vip.page_interval):
        """
            init ticks fetcher
        :param clt:
        """
        self._clent = clt
        self._pinterval = pinterval

    def fetch(self, zqdm, date):
        """

        :param zqdm: str, 股票代码
        :param date: str, 日期格式: YYYY-mm-dd
        :return:
            逐笔委托列表
        """
        # translate zqdm from 000001->sz000001
        zqdm = util.addse(zqdm)

        # get page counts
        npage = self._get_pages(zqdm, date)

        items = []
        # get all tick items
        for page in range(1, npage+1):
            items.extend(self._get_items(zqdm, date, page))
            time.sleep(self._pinterval)

        return items

    def _get_pages(self, zqdm, date):
        """
            获取逐笔数据总页数, url路径示例:
            http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_Transactions.getAllPageTime?date=2018-10-24&symbol=sz000001
        :param zqdm:
        :param date:
        :return:
            int, 逐笔总页数
        """
        # url path
        path = "/quotes_service/api/json_v2.php/CN_Transactions.getAllPageTime?date=%s&symbol=%s"  % (date, zqdm)

        # request data
        resp = self._clent.get(path)

        # parse pages data
        pages = self.json(resp.text)

        return len(pages['detailPages'])

    def _get_items(self, zqdm, date, page):
        """
            获取分页的逐笔委托记录, url路径示例:
            http://vip.stock.finance.sina.com.cn/quotes_service/view/vMS_tradedetail.php?symbol=sz000001&date=2018-10-24&page=2
        :param zqdm:
        :param date:
        :param page:
        :return:
            list
        """
        # url path
        path = '/quotes_service/view/vMS_tradedetail.php?symbol=%s&date=%s&page=%s'  % (zqdm, date, str(page))

        # request data
        resp = self._clent.get(path)

        # get html
        html = lxml.html.fromstring(resp.content.decode('gb2312'))
        res = html.xpath('//table[@id=\"datatbl\"]/tbody/tr')
        sarr = [lxml.etree.tostring(node).decode() for node in res]
        sarr = ''.join(sarr)
        sarr = '<table>%s</table>' % sarr
        sarr = sarr.replace('--', '0')

        df = pandas.read_html(io.StringIO(sarr), parse_dates=False)[0]
        df.columns = ['time', 'price', 'pchange', 'change', 'volume', 'amount', 'type']

        items = []
        for index, row in df.iterrows():
            items.append(self._parse_item(row))

        return items

    def _parse_item(self, record):
        """
            parset item
        :param record:
        :return:
        """
        # alias for source to target
        alias = {
            'cjsj': 'time', # 成交时间
            'cjjg': 'price', # 成交价格
            'zdf': 'pchange', # 涨跌幅
            'zde': 'change', # 涨跌额
            'cjl': 'volume', # 成交量
            'cje': 'amount', # 成交额
            'xz': 'type' # 成交性质
        }

        result = {}
        # translate record by alias
        for key in alias.keys():
            result[key] = record[alias[key]]

        return result

ticks = _Ticks()