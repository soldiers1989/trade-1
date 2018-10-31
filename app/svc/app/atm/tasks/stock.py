"""
    stock relate tasks
"""
import logging, tms, app
from xpinyin import Pinyin

from .. import task


class SyncAllService(task.Task):
    """
        sync stock from remote source: sina/cninfo/...etc
        config format:
        {
            rpc: {
                aam: {
                    baseurl: <baseurl>
                    key: <key>
                    safety: <True|False>
                },
                mds: {
                    baseurl: <baseurl>
                    key: <key>
                    safety: <True|False>
                }
            }
        }
    """
    def __init__(self, *args, **kwargs):
        """
            init
        :param args:
        :param kwargs:
        """
        # get config
        config = kwargs.get('config')['rpc']

        # init remote rpc
        self._aam = app.rpc.Aam(config['aam']['baseurl'], config['aam'].get('key'), config['aam'].get('safety', False))
        self._mds = tms.rpc.Mds(config['mds']['baseurl'], config['mds'].get('key'), config['mds'].get('safety', False))

        super().__init__(*args, **kwargs)

    def execute(self):
        """
            sync stock
        :return:
        """
        # get local stock list
        localstocks = {}
        stocks = self._aam.stock_list()
        for stock in stocks:
            localstocks[stock['id']] = stock['id']

        # new stocks
        newstocks = []

        # get remote stocks from
        remotestocks = self._mds.stock_list()
        for stock in remotestocks:
            if localstocks.get(stock['zqdm']) is None:
                newstocks.append(stock)

        # pinyin translater
        py = Pinyin()

        tidystocks = []
        # tidy new stocks
        for stock in newstocks:
            id, name = stock['zqdm'], stock['zqmc']
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
        resp = self._aam.stock_add(tidystocks)

        # add/failed count
        added, failed = len(resp.get('added')), len(resp.get('failed'))

        return 'local:%d, remote:%d, added:%d, failed:%d' % (len(localstocks), len(remotestocks), added, failed)
