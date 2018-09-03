import time, datetime


DEFAULT_DATE_FORMAT = "%Y-%m-%d"
DEFAULT_DATE_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def utime(date, format=None):
    """
        transfer date to unix timestamp
    :param date: str or date, string with format or datetime.date
    :param format: str, data string format
    :return:
        unix timestamp
    """
    if date is None:
        return 0;

    if isinstance(date, datetime.date):
        return time.mktime(date.timetuple())
    elif isinstance(date, str):
        format = format if format is not None else DEFAULT_DATE_FORMAT
        return time.mktime(time.strptime(date, format))
    else:
        raise 'input date format is not support'


def dates(tm, format=None):
    """
        transfer unix timestamp to date string
    :param tm: int, unix timestamp
    :param format: str, date string format
    :return: str, date string
    """
    if tm is None:
        return ''
    format = DEFAULT_DATE_FORMAT if format is None else format
    return time.strftime(format, time.localtime(tm))


def datetms(tm, format=None):
    """
        transfer unix timestamp to date string
    :param tm: int, unix timestamp
    :param format: str, date string format
    :return: str, date string
    """
    if tm is None:
        return ''

    format = DEFAULT_DATE_TIME_FORMAT if format is None else format
    return time.strftime(format, time.localtime(tm))
