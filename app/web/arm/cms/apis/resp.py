"""
    api for cms
"""
import json, decimal

from django.http import HttpResponse


class JEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)

        return super(JEncoder, self).default(o)


def success(message='success', data={}):
    """
        success response
    :param message:
    :param data:
    :return:
    """
    resp = {
        'status': True,
        'message': message,
        'data': data
    }

    resp = json.dumps(resp, cls=JEncoder).encode('utf-8')

    return HttpResponse(resp, content_type='application/json;charset=utf8')


def failure(message='failure', data={}):
    """
        failure response
    :param message:
    :param data:
    :return:
    """
    resp = {
        'status': False,
        'message': message,
        'data': data
    }

    resp = json.dumps(resp, cls=JEncoder).encode('utf-8')

    return HttpResponse(resp, content_type='application/json;charset=utf8')
