"""
     authority control
"""
from cms import forms
from pub import models

from django.shortcuts import redirect


def has_auth(func):
    """
        module authority decorator
    :param request:
    :return:
    """
    def _has_auth(request):
        mdls = request.session.get('modules', None)
        if mdls is not None:
            for mdl in mdls:
                mpath = mdl.get('path')
                # user has module auth
                if mpath is not None and mpath  == request.path:
                    return func(request)

        # user has no auth, goto login
        return redirect('cms.login')
    return _has_auth


def has_login(request):
    """
        check login status
    :return:
    """
    uid = request.session.get('userid', None)
    if uid is not None:
        return True
    return False


def login(request):
    """
        administrator login
    :param username:
    :param password:
    :param remember:
    :return:
    """
    try:
        login_form = forms.LoginForm(request.GET)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            remember = login_form.cleaned_data.get('remember')

            admin = models.Admin.objects.get(user=username)
            if admin.pwd == password:
                # set session expire for not remember choice
                if not remember:
                    request.session.set_expiry(0)

                # set user name
                request.session['userid'] = admin.admin_id
                request.session['username'] = username
                request.session['modules'] = [{'path':'/cms/index/'}]

                return True
    except:
        pass

    return False


def logout(request):
    """
        administrator logout
    :return:
    """
    # clear session
    request.session.clear()


def modules(request):
    """
        get admin authorized modules
    :return:
    """
    return request.session.get('modules', None)

