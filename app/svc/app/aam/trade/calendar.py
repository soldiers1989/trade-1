import time, datetime

# debug flag
DEBUG = True


#holiday
HOLIDAYS = [
    "2018-09-24", "2018-10-01", "2018-10-02", "2018-10-03", "2018-10-04", "2018-10-05",
]


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