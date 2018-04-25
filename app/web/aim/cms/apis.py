"""
    api for cms
"""
import json

from cms import auth, hint, forms

from django.http import HttpResponse


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

    resp = json.dumps(resp).encode('utf-8')

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

    resp = json.dumps(resp).encode('utf-8')

    return HttpResponse(resp, content_type='application/json;charset=utf8')


def login(request):
    """
        login api
    :param request:
    :return:
    """
    res, msg = auth.login(request)
    if res:
        return success(message=msg)
    else:
        return failure(message=msg)


def auth_admin_list(request):
    """
        login api
    :param request:
    :return:
    """
    admins = [[1,2,3,4]]

    resp = json.dumps(admins).encode('utf-8')
    return HttpResponse(resp, content_type='application/json;charset=utf8')


def auth_module_list(request):
    """
        login api
    :param request:
    :return:
    """

    data = []
    for i in range(0, 100):
        data.append([i,i,i,i])

    modules = {
                'data':data
            }

    resp = json.dumps(modules).encode('utf-8')
    return HttpResponse(resp, content_type='application/json;charset=utf8')
