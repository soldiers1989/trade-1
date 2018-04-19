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
    login_form = forms.LoginForm(request.GET)
    if login_form.is_valid():
        username = login_form.cleaned_data.get('username')
        password = login_form.cleaned_data.get('password')
        remember = login_form.cleaned_data.get('remember')

        if auth.do_login(username, password, remember):
            return success(message=hint.MSG_LOGIN_SUCCESS)
        else:
            return failure(message=hint.ERR_USERNAME_OR_PASSWORD)
    else:
        return failure(message=hint.ERR_USERNAME_OR_PASSWORD)