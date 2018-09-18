"""
    stock relate tasks
"""
import logging
from xpinyin import Pinyin

from .. import task
from tlib.stock.detail import cninfo, sina
from trpc import aam


class SyncAll(task.Task):
    """
        sync stock from remote source: sina/cninfo/...etc
    """
    def execute(self):
        """
            sync stock
        :return:
        """
        # get local stock list
        localstocks = {}
        stocks = aam.stock.list()
        for stock in stocks:
            localstocks[stock['id']] = stock['id']

        # new stocks
        newstocks = []

        # get remote stocks from
        remotestocks = self._fetch()
        for stock in remotestocks:
            if localstocks.get(stock['code']) is None:
                newstocks.append(stock)

        # pinyin translater
        py = Pinyin()

        tidystocks = []
        # tidy new stocks
        for stock in newstocks:
            id, name = stock['code'], stock['name']
            jianpin = py.get_initials(name, u'').lower()
            quanpin = py.get_pinyin(name, u'')
            tidystocks.append({
                'id': id,
                'name': name,
                'jianpin': jianpin,
                'quanpin': quanpin,
                'status': 'open',
                'limit': 'none'
            })

        # add new stocks
        resp = aam.stock.add(tidystocks)

        # add/failed count
        added, failed = len(resp.get('added')), len(resp.get('failed'))

        return 'local:%d, remote:%d, added:%d, failed:%d' % (len(localstocks), len(remotestocks), added, failed)


    def _fetch(self):
        """
            fetch stocks from source sites
        :return:
        """
        # none-repeated stocks fetched
        stocks = {}

        # sync from sina
        try:
            sinas = sina.list.fetch()
            for stock in sinas:
                stocks[stock['code']] = stock
        except Exception as e:
            logging.error('sync stocks from sina error: %s' % str(e))

        # sync from cninfo
        try:
            cninfos = cninfo.list.fetch()
            for stock in cninfos:
                stocks[stock['code']] = stock
        except Exception as e:
            logging.error('sync stocks from sina error: %s' % str(e))

        # all stocks fetched
        return list(stocks.values())
