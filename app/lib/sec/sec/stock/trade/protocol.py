"""
    protocol for trade service
"""


def success(msg = 'success', data = None):
    """
        error return format
    :param msg:
    :return:
    """
    # make formatted return
    ret = {
        'status': 0,
        'msg': msg,
        'data': data
    }

    return ret


def failed(msg = 'failed', data = None):
    """
        error return format
    :param msg:
    :return:
    """
    # make formatted return
    ret = {
        'status': -1,
        'msg': msg,
        'data': data
    }

    return ret
