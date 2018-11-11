import time, datetime, decimal
from tms.mds import smd
from . import config

# debug flag
DEBUG = config.DEBUG

#holiday
HOLIDAYS = [
    "2018-09-24", "2018-10-01", "2018-10-02", "2018-10-03", "2018-10-04", "2018-10-05",
]


class InvalidOrder(Exception):
    pass


def is_trading_day(tm = time.time()):
    """
        trading day: except weekday and holiday
    :param tm:
    :return:
    """
    if DEBUG:
        return True

    # date time
    dt = datetime.datetime.fromtimestamp(tm)

    # check weekday
    if dt.isoweekday() in [6, 7]:
        return False

    # check holiday
    if dt.date().strftime('%Y-%m-%d') in HOLIDAYS:
        return False

    return True


def is_auction_time(tm = time.time()):
    """
        集合竞价时间，auction time: 9:15~9:25, 14:57~15:00
    :param tm:
    :return:
    """
    if DEBUG:
        return True

    # check trading day
    if not is_trading_day(tm):
        return False

    # check trading time
    dtm = datetime.datetime.fromtimestamp(tm).time()

    if (datetime.time(9, 15) < dtm < datetime.time(9, 25)) \
        or (datetime.time(14, 57) < dtm < datetime.time(15, 00)) :
        return True

    return False


def is_trading_time(tm = time.time()):
    """
        trading time: 9:30~11:30, 13:00~14:57
    :param tm:
    :return:
    """
    if DEBUG:
        return True

    # check trading day
    if not is_trading_day(tm):
        return False

    # check trading time
    dtm = datetime.datetime.fromtimestamp(tm).time()

    if ( datetime.time(9, 30) < dtm < datetime.time(11, 30)) \
        or (datetime.time(13, 00) < dtm < datetime.time(14, 57)):
        return True

    return False


def is_clearing_time(tm = time.time()):
    """
        clearing time: trading day's 15:00~15:10
    :param tm:
    :return:
    """
    if DEBUG:
        return False

    # check trading day
    if not is_trading_day(tm):
        return False

    # check clearing time
    dtm = datetime.datetime.fromtimestamp(tm).time()

    if datetime.time(15, 00) < dtm < datetime.time(15, 10):
        return True

    return False


def is_valid_count(count):
    """
        check if valid buy count
    :param count:
    :return:
    """
    if count < 100 or count % 100 != 0:
        return False
    return True


def is_valid_price(code, price):
    """
        check if price if a valid order price for stock in current time
    :param code: str, stock code
    :param price: float, order price
    :return:
    """
    q = smd.api.stock.get_quote(zqdm=code)[0]
    if price < q['dtj'] or price > q['ztj']:
        return False

    return True


def get_trading_price(scode):
    """
        get current stock price
    :param scode:
    :return:
    """
    q = smd.api.stock.get_quote(zqdm=scode)[0]
    return decimal.Decimal(q['dqj'])


def valid_trading_time(optype=None):
    """
        validate trading time
    :param otype:
    :param optype:
    :return:
    """
    if DEBUG:
        return

    if not is_trading_day():
        raise InvalidOrder('非交易日期不能报单')

    if not is_trading_time() or not is_auction_time():
        raise InvalidOrder('非交易时间不能报单')

    if optype == 'sj' and is_auction_time():
        raise InvalidOrder('集合竞价时间不能报市价单')


def valid_trading_price(scode, oprice):
    """
        validate trading price
    :param scode:
    :param oprice:
    :return:
    """
    if not is_valid_price(scode, oprice):
        raise InvalidOrder('订单的报价不能操作当日涨跌停的限制')


def valid_trading_count(ocount):
    """
        validate trading price
    :param scode:
    :param oprice:
    :return:
    """
    if not is_valid_count(ocount):
            raise InvalidOrder('订单数量必须是100的整数倍')


def valid(scode, optype, oprice, ocount):
    """
        validate trade order
    :param scode:
    :param otype:
    :param ocount:
    :param oprice:
    :return:
    """
    valid_trading_time(optype)
    valid_trading_price(scode, oprice)
    valid_trading_count(ocount)
