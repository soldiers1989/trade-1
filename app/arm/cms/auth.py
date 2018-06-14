"""
     authority control
"""
from adb import models
from cms import resp, hint
from django.shortcuts import redirect


def set_admin_id(request, id):
    """
        save admin information to session
    :param request:
    :return:
    """
    request.session['id'] = id


def get_admin_id(request):
    """
        get admin information from session
    :param request:
    :return:
    """
    return request.session.get('id')


def set_admin_modules(request, modules):
    """
        save admin modules to session
    :param request:
    :param modules:
    :return:
    """
    request.session['modules'] = modules


def get_admin_modules(request):
    """
        get admin modules from session
    :param request:
    :return:
    """
    return request.session.get('modules')


def has_login(request):
    """
        check login
    :param request:
    :return:
    """
    if get_admin_id(request) is None:
        return False
    return True


def has_permit(request):
    """
        check permit
    :param request:
    :return:
    """
    # check if login
    if(not has_login(request)):
        return False

    # get admin modules from session
    modules = get_admin_modules(request)

    # check access permission
    for m in modules:
        if m['path'] == request.path:
            return True

    # has no permission
    return False


def need_login(func):
    def check_login(request):
        if not has_login(request):
            if request.path.startswith('/api/'):
                return resp.failure(hint.ERR_NOT_AUTHORIZED)
            return redirect('cms.login')
        else:
            return func(request)
    return check_login


def need_permit(func):
    def check_permit(request):
        if not has_permit(request):
            if request.path.startswith('/api/'):
                return resp.failure(hint.ERR_NOT_AUTHORIZED)
            return redirect('cms.login')
        else:
            return func(request)
    return check_permit
