"""
     authority control
"""
from adb import models
from cms import resp, hint
from django.shortcuts import redirect


def get_user(request):
    """
        get user information from session
    :param request:
    :return:
    """
    return request.session.get('user')


def has_login(request):
    """
        check login
    :param request:
    :return:
    """
    if request.session.get('user') is None:
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

    # get user from session
    user = get_user(request)

    # check access path's permit
    admin = models.Admin.objects.get(id=user['id'])

    # get user's enabled modules
    modules = admin.modules.filter(disable=False).all()
    for m in modules:
        if m.path == request.path:
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
