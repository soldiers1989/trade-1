"""
    stock relate tasks
"""

from xpinyin import Pinyin
from app.atm import task, models
from app.util import rand
from lib.stock.detail import sina, cninfo


class SyncStocks(task.Task):
    def __init__(self):
        """
            init sync stocks task
        """
        task.Task.__init__(self, rand.uuid(), 'syncstocks', '同步股票列表')

    def run(self):
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
    ss = SyncStocks()
    ss.start()

    import time
    time.sleep(100)
