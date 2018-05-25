"""
    page
"""

DEFAULT_PAGE_SIZE = 20


def start(s, total):
    """
       get corrent start pos for page
    :param s: int, start pos from front
    :param total: int, total records
    :return: int, correct start value
    """
    if s is None or s < 0:
        s = 0
    elif s > total:
        s = total
    else:
        pass

    return s


def count(count):
    """
        get corrent count for page
    :param start: int, start pos from front
    :param count: int, want count
    :param total: int, total records
    :return: int, correct count value
    """
    if count is None:
        return DEFAULT_PAGE_SIZE

    if count < 0:
        count = 0;

    return count
