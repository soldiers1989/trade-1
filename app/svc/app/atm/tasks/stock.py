"""
    stock relate tasks
"""
import time
from xpinyin import Pinyin

from .. import remote


def sync_all(*args, **kwargs):
    """
        sync all stocks from market data service, update the new stocks to aam service
        kwargs:
        {
            config:{
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
            },
            callback: <url>
        }
    :param args:
    :param kwargs:
    :return:
    """
    try:
        # get config
        config, callback = kwargs.get('config'), kwargs.get('callback')

        # init remote rpc
        rpcaam = remote.aam.Aam(config['rpc']['aam']['baseurl'], config['rpc']['aam'].get('key'), config['rpc']['aam'].get('safety', False))
        rpcmds = remote.tms.Mds(config['rpc']['mds']['baseurl'], config['rpc']['mds'].get('key'), config['rpc']['mds'].get('safety', False))

        # get local stock list
        localstocks = {}
        stocks = rpcaam.stock_list()
        for stock in stocks:
            localstocks[stock['id']] = stock['id']

        # new stocks
        newstocks = []

        # get remote stocks from
        remotestocks = rpcmds.stock_list()
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
                'limit': 'none',
                'ctime': int(time.time()),
                'mtime': int(time.time())
            })

        # add new stocks
        resp = rpcaam.stock_add(tidystocks)

        # add/failed count
        added, failed = resp.get('added'), resp.get('failed')

        return 'stock(sync_all): local:%d, remote:%d, added:%d, failed:%d' % (len(localstocks), len(remotestocks), added, failed)
    except Exception as e:
        raise RuntimeError('stock(sync_all): %s'%str(e))
