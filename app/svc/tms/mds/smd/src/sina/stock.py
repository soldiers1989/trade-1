"""
    stock data from sina
"""
import io, time, random, math, pandas
import lxml, lxml.html, lxml.etree

from . import client, config
from .. import util


class _Quotes:
    """
        获取指定或者所有股票当前行情
        所有股票：
            页面地址：http://vip.stock.finance.sina.com.cn/mkt/#hs_a
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
                    zqdm: 股票代码, zqmc: 股票名称,
                    dqj: 当前价格, mrj1: 买一价, mcj: 卖一价
                    zsj: 昨收价, jkj: 今开价, zgj: 最高价, zdj: 最低价,
                    cjl: 成交量, cje: 成交额, zde: 涨跌额, zdf: 涨跌幅, hsl: 换手率,
                    syl: 市盈率, sjl: 市净率, zsz: 总市值, ltsz: 流通市值,
                    tm: tick时间
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
        return self._get()

    def _parse(self, record):
        """
            parse one record
        :param record:
        :return:
        """
        # alias for source to target
        alias = {
            'zqdm': 'code', 'zqmc': 'name',
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

    def _get(self):
        """
            get stock all stock quotes
        :return:
            list
        """
        # path for get market quote
        pathtpl = '/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?sort=symbol&asc=1&symbol=&_s_r_a=page&num=40&page=%d&node=hs_a#"'

        results = []

        page = 1
        while page < 120:
            # generate current page url
            path = pathtpl % page

            # request page data
            resp = client.vsf.get(path)

            # translate to json object
            records = util.json(resp.text)
            if records == 'null':
                break

            # parse records
            for record in records:
                results.append(self._parse(record))

            # fetch next page
            page = page + 1

            # sleep for a while
            time.sleep(config.vsf.page_interval)

        return results

quotes = _Quotes()


class _Quote:
    """
        获取指定股票当前行情，多个股票用','分割
        -页面地址：
                http://hq.sinajs.cn/rn=y92ka7&list=sz000001,sz000725
        -数据来源格式：
                var hq_str_sz000001="平安银行,11.200,11.180,10.640,11.240,10.620,10.630,10.640,139470933,1514557705.160,7600,10.630,342418,10.620,646300,10.610,1718900,10.600,102100,10.590,29200,10.640,393900,10.650,2700,10.660,8900,10.670,126100,10.680,2018-10-29,14:18:54,00";
                var hq_str_sz000725="京东方Ａ,2.800,2.790,2.770,2.820,2.760,2.770,2.780,239219203,666810556.350,2900500,2.770,9358300,2.760,7909100,2.750,3179900,2.740,2813800,2.730,4382000,2.780,5471369,2.790,10453300,2.800,12796992,2.810,11890500,2.820,2018-10-29,14:18:54,00";

        -返回数据格式：
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
        """
            init fetch stock list object
        """
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
            "jkj": 1, "zsj": 2, "dqj": 3, "zgj": 4, "zdj": 5,
            "cjl": 8, "cje": 9,
            "mrl1": 10, "mrj1": 11, "mrl2": 12, "mrj2": 13, "mrl3": 14, "mrj3": 15, "mrl4": 16, "mrj4": 17, "mrl5": 18, "mrj5": 19,
            "mcl1": 20, "mcj1": 21, "mcl2": 22, "mcj2": 23, "mcl3": 24, "mcj3": 25, "mcl4": 26, "mcj4": 27, "mcl5": 28, "mcj5": 29,
            "date": 30, "time": 31
        }

        # parse all response quotes
        quotes = text.strip().split('\n')

        # parse each quote
        for quote in quotes:
            items = quote.split(',')

            # stock code
            code = items[0].split('=')[0][-6:]

            qte = {'zqdm': code}
            # stock quote
            for k in alias:
                qte[k] = items[alias[k]]

            # process date&time
            qte['time'] = qte['date'] + " " + qte['time']
            del qte['date']

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
        # random number for path
        randnum = util.strbasen(round(random.random() * 60466176), 36)
        # path for query quotes
        path = "/rn=" + randnum + "&list=" + ','.join(util.addse(zqdm.split(',')))

        # request data
        resp = client.hqjs.get(path)

        # parse data
        return self._parse(resp.text)

quote = _Quote()


class _Ticks:
    """
        获取指定股票和日期的逐笔委托记录
    """
    def __init__(self, clt=client.vsf, pinterval=config.vsf.page_interval):
        """
            init ticks fetcher
        :param clt:
        """
        self._clent = clt
        self._pinterval = pinterval

    def get(self, **kwargs):
        """
            get every ticks of date
        :param zqdm: str, 股票代码
        :param date: str, 日期格式: YYYY-mm-dd
        :return:
            逐笔委托列表
        """
        # get parameters
        zqdm, date = kwargs.get('zqdm'), kwargs.get('date')
        if zqdm is None or date is None:
            raise ValueError('missing parameters, need (zqdm, date)')

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
        pages = util.json(resp.text)

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
        try:
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
        except Exception as e:
            return []

    def _parse_item(self, record):
        """
            parset item
        :param record:
        :return:
        """
        try:
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
        except Exception as e:
            raise e

ticks = _Ticks()