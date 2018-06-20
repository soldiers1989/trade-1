"""
    stock util functions
"""


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

    return None


def addse(code):
    """
        add securities exchange flag before stock code, like: 000001->sz000001, 600301->sh600301
    :param code: str, stock code
    :return:
        stock code with exchange flag
    """
    return getse(code)+code