"""
    path for east money
"""
import time


def _getse(code):
    """
        get securities exchange of specified stock by code
    :param code: str, stock code
    :return:
        sz, sh or None
    """
    # stock code rules
    codes = {
        "sh": ['600','601','603'],
        "sz": ['000','002','300']
    }

    if len(code) < 3:
        return None

    code = code[:3]
    for se in codes.keys():
        if code in codes[se]:
            return se

    return None


def make(code):
    """
        make request url by stock codes
    :param codes:
    :return:
    """
    # generate id by code
    id = code + "1" if _getse(code) == 'sh' else code + "2"

    # generate token
    token = "4f1862fc3b5e77c150a2b985b12db0fd"

    # add random parameter
    rd = str(int(time.time() * 1000))

    # make path
    path = "/EM_Finance2015TradeInterface/JS.ashx?id=" + id + "&token=" + token + "&_=" + rd

    return path
