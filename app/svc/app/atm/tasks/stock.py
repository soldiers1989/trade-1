"""
    stock relate tasks
"""

from xpinyin import Pinyin

from .. import daos, timer, mysql
from tlib import rand
from tlib.stock.detail import cninfo, sina


class SyncStockFromSina(timer.Runnable):
    """
        sync all stock list from sina, update local stock list in database
    """
    def do(self):
        """
            thread function
        :return:
        """
        # stock model
        stockdao = daos.stock.Stock(mysql.get())

        newstocks, localstocks = [], {}
        # fetch all stocks from local database
        stocks = stockdao.get()
        for stock in stocks:
            localstocks[stock['id']] = stock['name']
        localcnt = len(stocks)

        # fetch all stocks from cninfo
        stocks = sina.list.fetch()
        for stock in stocks:
            if localstocks.get(stock['code']) is None:
                newstocks.append(stock)
        sinacnt, newcnt = len(stocks), len(newstocks)

        # pinyin translater
        py = Pinyin()

        # add new stocks to database
        for stock in newstocks:
            id, name = stock['code'], stock['name']
            jianpin = py.get_initials(name, u'').lower()
            quanpin = py.get_pinyin(name, u'')
            status, limit = 'open', 'none'
            stockdao.add(id, name, jianpin, quanpin, status, limit)

        # commit exchanges
        stockdao.commit()

        # return result
        result = 'local:%d, sina:%d, new:%d' %(localcnt, sinacnt, newcnt)

        return result


class SyncStockFromCNInfo(timer.Runnable):
    """
        sync all stock list from cninfo, update local stock list in database
    """

    def do(self):
        """
            thread function
        :return:
        """
        # stock model
        stockdao = daos.stock.Stock(mysql.get())

        newstocks, localstocks = [], {}
        # fetch all stocks from local database
        stocks = stockdao.get()
        for stock in stocks:
            localstocks[stock['id']] = stock['name']
        localcnt = len(stocks)

        # fetch all stocks from cninfo
        stocks = cninfo.list.fetch()
        for stock in stocks:
            if localstocks.get(stock['code']) is None:
                newstocks.append(stock)
        cnicnt, newcnt = len(stocks), len(newstocks)

        # pinyin translater
        py = Pinyin()

        # add new stocks to database
        for stock in newstocks:
            id, name = stock['code'], stock['name']
            jianpin = py.get_initials(name, u'').lower()
            quanpin = py.get_pinyin(name, u'')
            status, limit = 'open', 'none'
            stockdao.add(id, name, jianpin, quanpin, status, limit)

        # commit exchanges
        stockdao.commit()

        # return result
        result = 'local:%d, sina:%d, new:%d' %(localcnt, cnicnt, newcnt)

        return result


# setup stock sync task
timer.default.setup(rand.uuid(), '新浪股票列表同步', SyncStockFromSina, min=0, hour=1, exclusive=True, maxkeep=20)
timer.default.setup(rand.uuid(), '巨潮股票列表同步', SyncStockFromCNInfo, min=0, hour=7, exclusive=True, maxkeep=20)

