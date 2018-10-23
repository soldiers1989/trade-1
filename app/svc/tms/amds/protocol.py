"""
    protocol for quote service
"""
import json, decimal


class JEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)

        return super(JEncoder, self).default(o)


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

    return json.dumps(ret, cls=JEncoder)


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

    return json.dumps(ret, cls=JEncoder)
