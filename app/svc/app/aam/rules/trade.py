"""
    trade relate utility
"""
import trpc
import time, datetime


HOLIDAYS = [
    "2018-09-24", "2018-10-01", "2018-10-02", "2018-10-03", "2018-10-04", "2018-10-05",
]


def _is_trading_day(tm = time.time()):
    """
        trading day: except weekday and holiday
    :param tm:
    :return:
    """
    # date time
    dt = datetime.datetime.fromtimestamp(tm)

    # check weekday
    if dt.isoweekday() in [6, 7]:
        return False

    # check holiday
    if dt.date().strftime('%Y-%m-%d') in HOLIDAYS:
        return False

    return True


def _is_auction_time(tm = time.time()):
    """
        auction time: 9:15~9:25, 14:57~15:00
    :param tm:
    :return:
    """
    # date time
    dtm = datetime.datetime.fromtimestamp(tm).time()

    if (dtm > datetime.time(9, 15) and dtm < datetime.time(9, 25)) \
        or (dtm > datetime.time(14, 57) and dtm < datetime.time(15, 00)) :
        return True

    return False


def _is_trading_time(tm = time.time()):
    """
        trading time: 9:30~11:30, 13:00~14:57
    :param tm:
    :return:
    """
    # date time
    dtm = datetime.datetime.fromtimestamp(tm).time()

    if (dtm > datetime.time(9, 30) and dtm < datetime.time(11, 30)) \
        or (dtm > datetime.time(13, 00) and dtm < datetime.time(14, 57)):
        return True

    return False


def valid_user_buy_time(ptype, tm = time.time()):
    """

    :param tm:
    :return:
    """
    # check trading day
    if _is_trading_day() and _is_trading_time():
        return True

    return False


def valid_user_sell_time(ptype, tm = time.time()):
    """

    :param tm:
    :return:
    """
    # check trading day
    if _is_trading_day() and _is_trading_time():
        return True

    return False


def valid_user_close_time(ptype, tm = time.time()):
    """

    :param tm:
    :return:
    """
    # check trading day
    if _is_trading_day() and _is_trading_time():
        return True

    return False


def valid_user_cancel_time(tm = time.time()):
    """

    :param tm:
    :return:
    """
    # check trading day
    if _is_trading_day() and _is_trading_time():
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
    # check trading day
    if _is_trading_day() and _is_trading_time():
        return True

    return False


def valid_sys_sell_time(ptype, tm = time.time()):
    """

    :param tm:
    :return:
    """
    # check trading day
    if _is_trading_day() and _is_trading_time():
        return True

    return False


def valid_sys_close_time(ptype, tm = time.time()):
    """

    :param tm:
    :return:
    """
    # check trading day
    if _is_trading_day() and _is_trading_time():
        return True

    return False


def valid_sys_cancel_time(tm = time.time()):
    """

    :param tm:
    :return:
    """
    # check trading day
    if _is_trading_day() and _is_trading_time():
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
