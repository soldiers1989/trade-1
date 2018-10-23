"""
    stock market data
"""
from . import shse, szse, sina


def get_list():
    """
        获取所有A股上市股票列表， 数据源：
        -深交所
        -上交所
    :return:
    """
    # get shanghai securities exchange stock list
    shstocks = shse.stock.list.fetch()

    # get shenzhen securities exchange stock list
    szstocks = szse.stock.list.fetch()

    return shstocks+szstocks
