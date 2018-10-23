"""
    make request path
"""
import random


def _valid(code):
    """
        valid stock code
    :param code:
    :return:
    """
    codes = ['000', '002', '300', '600', '601', '603']

    if len(code) != 6 or not code.isdecimal() or not code[0:3] in codes:
        return False

    return True


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


def _addse(code):
    """
        add securities exchange flag before stock code, like: 000001->sz000001, 600301->sh600301
    :param code: str, stock code
    :return:
        stock code with exchange flag
    """
    return _getse(code)+code


def addse(codes):
    """
        add securities exchange flag before stock codes, like: 000001->sz000001
    :param codes: array, stock codes
    :return:
        array, stock codes with exchange flag
    """
    ncodes = []
    for code in codes:
        ncodes.append(_addse(code))
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
