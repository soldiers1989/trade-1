"""
    stock relate tasks
"""
import threading

from xpinyin import Pinyin

from app.atm import models, timer
from lib.stock.detail import cninfo


class SyncAll(timer.Runnable):
    """
        sync all stock list from cninfo/sina, update local stock list in database
    """
    def do(self):
        """
            thread function
        :return:
        """
        # stock model
        model = models.stock.Stock()

        newstocks, localstocks = [], {}
        # fetch all stocks from local database
        stocks = model.get()
        for stock in stocks:
            localstocks[stock['id']] = stock['name']

        # fetch all stocks from cninfo
        stocks = cninfo.list.fetch()
        for stock in stocks:
            if localstocks.get(stock['code']) is None:
                newstocks.append(stock)

        # pinyin translater
        py = Pinyin()

        # add new stocks to database
        for stock in newstocks:
            id, name = stock['code'], stock['name']
            jianpin = py.get_initials(name, u'').lower()
            quanpin = py.get_pinyin(name, u'')
            status, limit = 'open', 'none'
            model.add(id, name, jianpin, quanpin, status, limit)

        # commit exchanges
        model.dbcommit()


if __name__ == "__main__":
    ss = SyncAll()
    ss.start()
    ss.join()
    print(ss.is_alive())
