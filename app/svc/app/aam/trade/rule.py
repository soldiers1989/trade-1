"""
    trade relate utility
"""
import trpc
import time
from . import calendar


class _PType:
    sj = 'sj'
    xj = 'xj'


def valid_user_buy_time(ptype, tm = time.time()):
    """
        限价7*24小时，市价只能连续竞价时间
    :param tm:
    :return:
    """
    # check clear time
    if calendar.is_clearing_time(tm):
        return False

    # check price type & trading time
    if ptype == _PType.xj or calendar.is_trading_time(tm):
        return True

    return False


def valid_user_sell_time(ptype, tm = time.time()):
    """

    :param tm:
    :return:
    """
    # check clear time
    if calendar.is_clearing_time(tm):
        return False

    # check price type & trading time
    if ptype == _PType.xj or calendar.is_trading_time(tm):
        return True

    return False


def valid_user_close_time(ptype, tm = time.time()):
    """
        系统发起的用户订单市价平仓
    :param tm:
    :return:
    """
    # check clear time
    if calendar.is_clearing_time(tm):
        return False

    # check price type
    if ptype == _PType.xj or calendar.is_trading_time(tm):
        return True

    return False


def valid_user_cancel_time(tm = time.time()):
    """
        清算时间不能取消订单
    :param tm:
    :return:
    """
    # check trading day
    if not calendar.is_clearing_time(tm):
        return True

    return False


def valid_user_buy_count(count):
    """
        check if buy
    :param count:
    :return:
    """
    if count < 100 or count % 100 != 0:
        return False
    return True


def valid_user_buy_price(code, price):
    """
        check if price if a valid order price for stock in current time
    :param code: str, stock code
    :param price: float, order price
    :return:
    """
    q = trpc.quote.get_quote(code)
    if price < q.dtj or price > q.ztj:
        return False

    return True


def valid_user_sell_price(code, price):
    """

    :param code:
    :param price:
    :return:
    """
    q = trpc.quote.get_quote(code)
    if price < q.dtj or price > q.ztj:
        return False

    return True


def valid_user_close_price(code, price):
    """

    :param code:
    :param price:
    :return:
    """
    q = trpc.quote.get_quote(code)
    if price < q.dtj or price > q.ztj:
        return False

    return True


def valid_sys_buy_time(ptype, tm = time.time()):
    """

    :param tm:
    :return:
    """
    # check price type
    if ptype == _PType.xj:
        if calendar.is_auction_time(tm) or calendar.is_trading_time(tm):
            return True
        else:
            return False
    else:
        # check trading day
        if calendar.is_trading_time(tm):
            return True
        else:
            return False


def valid_sys_sell_time(ptype, tm = time.time()):
    """

    :param tm:
    :return:
    """
    # check price type
    if ptype == _PType.xj:
        if calendar.is_auction_time(tm) or calendar.is_trading_time(tm):
            return True
        else:
            return False
    else:
        # check trading day
        if calendar.is_trading_time(tm):
            return True
        else:
            return False


def valid_sys_close_time(ptype, tm = time.time()):
    """
        系统平仓指令
    :param tm:
    :return:
    """
    # check price type
    if ptype == _PType.xj:
        if calendar.is_auction_time(tm) or calendar.is_trading_time(tm):
            return True
        else:
            return False
    else:
        # check trading day
        if calendar.is_trading_time(tm):
            return True
        else:
            return False


def valid_sys_cancel_time(tm = time.time()):
    """

    :param tm:
    :return:
    """
    # check trading day
    if calendar.is_trading_time(tm):
        return True

    return False


def valid_sys_close_price(code, price):
    """

    :param code:
    :param price:
    :return:
    """
    q = trpc.quote.get_quote(code)
    if price < q.dtj or price > q.ztj:
        return False

    return True
