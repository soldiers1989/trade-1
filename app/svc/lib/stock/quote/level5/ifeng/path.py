"""
    make request path
"""
import random
from lib.stock.util import stock


def addse(codes):
    """
        add securities exchange flag before stock codes, like: 000001->sz000001
    :param codes: array, stock codes
    :return:
        array, stock codes with exchange flag
    """
    ncodes = []
    for code in codes:
        ncodes.append(stock.addse(code))
    return ncodes


def make(codes):
    """
        make request url by stock codes
    :param codes:
    :return:
    """
    # make path
    path = "/q.php?l="

    return path + ",".join(addse(codes)) + "&f=json&r=" + str(random.random())
