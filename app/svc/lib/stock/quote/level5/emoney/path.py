"""
    path for east money
"""
import time
from lib.stock.util import stock


def make(code):
    """
        make request url by stock codes
    :param codes:
    :return:
    """
    # generate id by code
    id = code + "1" if stock.getse(code) == 'sh' else code + "2"

    # generate token
    token = "4f1862fc3b5e77c150a2b985b12db0fd"

    # add random parameter
    rd = str(int(time.time() * 1000))

    # make path
    path = "/EM_Finance2015TradeInterface/JS.ashx?id=" + id + "&token=" + "&_=" + rd

    return path
