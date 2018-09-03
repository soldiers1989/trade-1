"""
    trade relate utility
"""
import time, datetime


class _Auction:
    """
        auction type definition
    """
    kpjj = 'kpjj' # 开盘集合竞价时间
    spjj = 'spjj' # 收盘集合竞价时间
    lxjj = 'lxjj' # 连续竞价交易时间
    closed = 'closed' # 休市时间

auction = _Auction


def get_auction(tm = time.time()):
    """
        get current auction type: kpjj, spjj, lxjj, closed
    :return:
    """
    pass


def get_current_quote(code):
    """
        get current stock quote
    :param code:
    :return:
    """
    pass


def get_open_quote(code, date=datetime.date.today()):
    """

    :param code:
    :return:
    """
    pass


def get_close_quote(code, date=datetime.date.today()):
    """

    :param code:
    :return:
    """
    pass


def valid_buy_time(ptype, tm = time.time()):
    """

    :param tm:
    :return:
    """
    pass


def valid_buy_count(count):
    """
        check if buy
    :param count:
    :return:
    """
    if count < 100 or count % 100 != 0:
        return False
    return True


def valid_buy_price(code, price):
    """
        check if price if a valid order price for stock in current time
    :param code: str, stock code
    :param price: float, order price
    :return:
    """
    return True


def valid_sell_time(ptype, tm = time.time()):
    """

    :param tm:
    :return:
    """
    pass


def valid_sell_price(code, price):
    """

    :param code:
    :param price:
    :return:
    """
    pass

