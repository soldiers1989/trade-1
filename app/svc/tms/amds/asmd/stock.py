"""
    stock market data
"""
import logging
from . import src, error


def get_list():
    """
        获取所有A股上市股票列表， 数据源：
        -深交所 + 上交所
    :return:
        [{'zqdm': 'A股代码', 'zqmc': 'A股简称', 'ssrq': 'A股上市日期', 'zgb': 'A股总股本', 'ltgb': 'A股流通股本'}, ...]
    """
    # source group
    source_groups = {
        'se': [src.shse.stock.list, src.szse.stock.list] # 上交所/深交所数据源，需要合并
    }

    # fetch data from group
    for name, group in source_groups.items():
        try:
            results = []
            for source in group:
                results.extend(source.fetch())
            return results
        except Exception as e:
            logging.error('get stock list from %s failed, error: %s' % (name, str(e)))

    raise error.ASMDError('get stock list failed, all data source has been tried.')


def get_quote(zqdm=None):
    """
        获取所有或者指定股票的当前行情
    :return:
    """
    pass


def get_kdata(zqdm, **kwargs):
    """
        获取指定股票的K线数据
    :param zqdm:
    :param kwargs:
    :return:
    """
    pass


def get_level5(zqdm, **kwargs):
    """
        获取指定股票五档行情
    :return:
    """
    pass


def get_ticks(zqdm, date):
    """
        获取指定股票和日期的历史逐笔委托数据
    :param zqdm:
    :param date:
    :return:
    """
    # source group
    source_groups = {
        'sina': [src.sina.stock.ticks] # 新浪
    }

    # fetch data from group
    for name, group in source_groups.items():
        try:
            results = []
            for source in group:
                results.extend(source.fetch(zqdm, date))
            return results
        except Exception as e:
            logging.error('get stock ticks <%s, %s> from %s failed, error: %s' % (zqdm, date, name, str(e)))

    raise error.ASMDError('get stock ticks <%s, %s> failed, all data source has been tried.' % (zqdm, date))