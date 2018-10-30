"""
    stock market data
"""
import logging
from . import shse, szse, sina, ifeng, icaopan, eastmoney
from . import error


def get_list(**kwargs):
    """
        获取所有A股上市股票列表， 数据源：
        -深交所 + 上交所
    :return:
        [{'zqdm': 'A股代码', 'zqmc': 'A股简称', 'ssrq': 'A股上市日期', 'zgb': 'A股总股本', 'ltgb': 'A股流通股本'}, ...]
    """
    # data sources
    sources = {
        'se': [shse.stock.list, szse.stock.list], # 上交所/深交所数据源，需要合并
    }

    # get specified source
    src = kwargs.get('src')
    if src is not None and src not in sources.keys():
        raise ValueError('source must be in :' + ','.join(sources.keys()))

    if src is not None:
        results = []
        for source in sources[src]:
            results.extend(source.get())
        return results
    else:
        # fetch data
        for name, group in sources.items():
            try:
                results = []
                for source in group:
                    results.extend(source.get())
                return results
            except Exception as e:
                logging.error('get stock list from %s failed, error: %s' % (name, str(e)))

        raise error.ASMDSrcError('get stock list failed, all data source has been tried.')


def _get_quotes(**kwargs):
    """
        获取所有股票的当前行情
    :return:
    """
    # data sources
    sources = {
        'sina': sina.stock.quotes, # 新浪
    }

    # get specified source
    src = kwargs.get('src')
    if src is not None and src not in sources.keys():
        raise ValueError('source must be in :' + ','.join(sources.keys()))

    if src is not None:
        return sources[src].get(**kwargs)
    else:
        # fetch data from all sources
        for name, source in sources.items():
            try:
                results = source.get(**kwargs)
                return results
            except Exception as e:
                logging.error('get stock quotes from %s failed, error: %s' % (name, str(e)))

        raise error.ASMDSrcError('get stock quotes failed, all data source has been tried.')


def get_quote(**kwargs):
    """
        获取所有或指定股票的当前行情
    :return:
    """
    # want get all stock's quote
    if kwargs.get('zqdm') is None:
        return _get_quotes(**kwargs)

    # data sources
    sources = {
        'sina': sina.stock.quote, # 新浪
        'icaopan': icaopan.stock.quote, # 爱操盘
        'ifeng': ifeng.stock.quote, #凤凰
        'eastmoney': eastmoney.stock.quote, #东方财富
    }

    # get specified source
    src = kwargs.get('src')
    if src is not None and src not in sources.keys():
        raise ValueError('source must be in :' + ','.join(sources.keys()))

    if src is not None:
        return sources[src].get(**kwargs)
    else:
        for name, source in sources.items():
            try:
                results = source.get(**kwargs)
                return results
            except Exception as e:
                logging.error('get stock quote from %s failed, error: %s' % (name, str(e)))

        raise error.ASMDSrcError('get stock quote failed, all data source has been tried.')


def get_ticks(**kwargs):
    """
        获取指定股票和日期的历史逐笔委托数据
    :param zqdm:
    :param date:
    :return:
    """
    # source group
    sources = {
        'sina': sina.stock.ticks, # 新浪
    }

    # get specified source
    src = kwargs.get('src')
    if src is not None and src not in sources.keys():
        raise ValueError('source must be in :' + ','.join(sources.keys()))

    if src is not None:
        return sources[src].get(**kwargs)
    else:
        for name, source in sources.items():
            try:
                results = source.get(**kwargs)
                return results
            except Exception as e:
                logging.error('get stock ticks from %s failed, error: %s' % (name, str(e)))

        raise error.ASMDSrcError('get stock ticks failed, all data source has been tried.')


def get_kline(**kwargs):
    """
        获取指定股票的K线数据
    :param kwargs:
    :return:
    """
    # data sources
    sources = {
        'ifeng': ifeng.stock.kline, # 凤凰
    }

    # get specified source
    src = kwargs.get('src')
    if src is not None and src not in sources.keys():
        raise ValueError('source must be in :' + ','.join(sources.keys()))

    if src is not None:
        return sources[src].get(**kwargs)
    else:
        for name, source in sources.items():
            try:
                results = source.get(**kwargs)
                return results
            except Exception as e:
                logging.error('get stock kdata from %s failed, error: %s' % (name, str(e)))

        raise error.ASMDSrcError('get stock kdata failed, all data source has been tried.')


def sub_quote(zqdm, callback):
    """
        订阅指定股票的五档行情
    :param zqdm:
    :param callback:
    :return:
    """
    pass
