"""
    stock market data
"""
import logging
from . import shse, szse, sina, ifeng
from . import error


def get_list():
    """
        获取所有A股上市股票列表， 数据源：
        -深交所 + 上交所
    :return:
        [{'zqdm': 'A股代码', 'zqmc': 'A股简称', 'ssrq': 'A股上市日期', 'zgb': 'A股总股本', 'ltgb': 'A股流通股本'}, ...]
    """
    # source group
    source_groups = {
        'se': [shse.stock.list, szse.stock.list] # 上交所/深交所数据源，需要合并
    }

    # fetch data from group
    for name, group in source_groups.items():
        try:
            results = []
            for source in group:
                results.extend(source.get())
            return results
        except Exception as e:
            logging.error('get stock list from %s failed, error: %s' % (name, str(e)))

    raise error.ASMDSrcError('get stock list failed, all data source has been tried.')


def get_quote(**kwargs):
    """
        获取所有或者指定股票的当前行情
    :return:
    """
    # source group
    source_groups = {
        'sina': [sina.stock.quote] # 新浪
    }

    # fetch data from group
    for name, group in source_groups.items():
        try:
            results = []
            for source in group:
                results.extend(source.get(**kwargs))
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
    source_groups = {
        'sina': [sina.stock.ticks] # 新浪
    }

    # fetch data from group
    for name, group in source_groups.items():
        try:
            results = []
            for source in group:
                results.extend(source.get(**kwargs))
            return results
        except Exception as e:
            logging.error('get stock ticks from %s failed, error: %s' % (name, str(e)))

    raise error.ASMDSrcError('get stock ticks failed, all data source has been tried.')


def get_kdata(**kwargs):
    """
        获取指定股票的K线数据
    :param kwargs:
    :return:
    """
    # source group
    source_groups = {
        'ifeng': [ifeng.stock.kdata] # 凤凰
    }

    # fetch data from group
    for name, group in source_groups.items():
        try:
            results = []
            for source in group:
                results.extend(source.get(**kwargs))
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
