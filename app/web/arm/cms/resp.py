"""
    api for cms
"""
import json, decimal, datetime

from django.http import HttpResponse


class JEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal) or isinstance(o, datetime.date):
            return str(o)

        return super(JEncoder, self).default(o)


def success(msg='success', data={}):
    """
        success response
    :param msg:
    :param data:
    :return:
    """
    resp = {
        'status': True,
        'msg': msg,
        'data': data
    }

    resp = json.dumps(resp, cls=JEncoder).encode('utf-8')

    return HttpResponse(resp, content_type='application/json;charset=utf8')


def failure(msg='failure', data={}):
    """
        failure response
    :param msg:
    :param data:
    :return:
    """
    resp = {
        'status': False,
        'msg': msg,
        'data': data
    }

    resp = json.dumps(resp, cls=JEncoder).encode('utf-8')

    return HttpResponse(resp, content_type='application/json;charset=utf8')


def text(txt):
    return HttpResponse(txt, content_type='application/json;charset=utf8')