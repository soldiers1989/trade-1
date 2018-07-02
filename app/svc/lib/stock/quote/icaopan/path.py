"""
    path for icaopan
"""
import time
from lib.stock.util import stock


def make(code):
    """
        make request url by stock codes
    :param codes:
    :return:
    """
    # add random parameter
    rd = str(int(time.time() * 1000))

    # make path
    path = "/openapi/queryMarketDataBySecurityCode?securityCode=" + code + "&_=" + rd

    return path
