"""
    util for tdx trade service
"""


def getse(code):
    """
        get securities exchange id by stock code, shanghai - 1, shenzhen - 0
    :param code: str, stock code
    :return:
    """
    # stock code rules
    codes = {
        "0": ['000', '002', '300'],  # shenzhen
        "1": ['600','601','603'] # shanghai
    }

    if len(code) < 3:
        return None

    code = code[:3]
    for se in codes.keys():
        if code in codes[se]:
            return se

    return None
