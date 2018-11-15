"""
    util functions
"""
import random


def valid(code):
    """
        valid stock code
    :param code:
    :return:
    """
    codes = ['000', '002', '300', '600', '601', '603']

    if len(code) != 6 or not code.isdecimal() or not code[0:3] in codes:
        return False

    return True


def getse(code):
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

    raise ValueError('code not valid, must be start with: %s' % (','.join(codes['sh'])+','+','.join(codes['sz'])))


def addse(codes):
    """
        add securities exchange flag before stock code, like: 000001->sz000001, 600301->sh600301
    :param code: str, stock code
    :return:
        stock code with exchange flag
    """
    if isinstance(codes, str):
        return getse(codes)+codes
    elif isinstance(codes, list) or isinstance(codes, tuple):
        ncodes = []
        for code in codes:
            ncodes.append(getse(code)+code)
        return ncodes
    else:
        raise TypeError('code must be str/list/tuple.')


def json(text):
    """
    解析非标准JSON的Javascript字符串，等同于json.loads(JSON str)
    :param expr:非标准JSON的Javascript字符串
    :return:Python字典
    """
    obj = eval(text, type('Dummy', (dict,), dict(__getitem__=lambda s, n: n))())
    return obj


def strbasen(num, b):
    """
        return string of num(oct number) with base by (b) string
    :return: str
    """
    return ((num == 0) and "0") or (strbasen(num // b, b).lstrip("0") + "0123456789abcdefghijklmnopqrstuvwxyz"[num % b])


def randnum():
    """
        generate random number
    :return:
    """
    return strbasen(round(random.random() * 60466176), 36)