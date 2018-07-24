"""

"""
import random
from lib.stock.util import digit, stock


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


def randnum():
    """
        generate random number
    :return:
    """
    return digit.strbasen(round(random.random() * 60466176), 36)


def make(codes):
    """
        make request url by stock codes
    :param codes:
    :return:
    """
    # make url
    path = "/rn=" + randnum() + "&list="

    return path + ",".join(addse(codes))
