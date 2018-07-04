"""
    protocol for quote service
"""
import json


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

    return json.dumps(ret)


def failed(status=-1, msg = 'failed', data = None):
    """
        error return format
    :param msg:
    :return:
    """
    # make formatted return
    ret = {
        'status': status,
        'msg': msg,
        'data': data
    }

    return json.dumps(ret)
