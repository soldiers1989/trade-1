import cube

import json
from dss.Serializer import serializer
from django.core import serializers

from adb import models
from cms.apis import resp
from cms import auth, hint, forms


def login(request):
    """
        login
    :param request:
    :return:
    """
    try:
        login_form = forms.user.Login(request.POST)
        if login_form.is_valid():
            # get login data form user input
            username = login_form.cleaned_data.get('user')
            password = cube.hash.sha1(login_form.cleaned_data.get('pwd'))
            remember = login_form.cleaned_data.get('remember')

            # get user data from database
            admin = models.Admin.objects.get(user=username)

            # check password
            if admin.pwd == password:
                # user has been disabled
                if admin.disable:
                    return False, hint.ERR_LOGIN_DISABLED

                # set session expire for not remember choice
                if not remember:
                    request.session.set_expiry(0)


                # set user session
                request.session['user'] = {
                    'id': admin.id,
                    'name': admin.name,
                }

                return resp.success(hint.MSG_LOGIN_SUCCESS)
            else:
                return resp.failure(hint.ERR_LOGIN_PASSWORD)
        else:
            return resp.failure(hint.ERR_LOGIN_INPUT)
    except Exception as e:
        return resp.failure(e)


@auth.need_login
def user(request):
    """
        get user
    :param request:
    :return:
    """
    try:
        # get user id from session
        user = request.session.get('user');

        # get user model
        admin = models.Admin.objects.get(id=user['id'])

        # get user modules
        modules = admin.modules.filter(disable=False).order_by('order')

        # response data
        data = {
            'id': admin.id,
            'name': admin.name,
            'modules': []
        }

        # get parent modules
        for m in modules:
            if m.parent is None:
                data['modules'].append(m.dict())

        # set child modules
        for p in data['modules']:
            p['childs'] = []
            for m in modules:
                if m.parent_id == p['id']:
                    p['childs'].append(m.dict())

        # return user modules
        return resp.success(data = data)
    except Exception as e:
        return resp.failure(e);


@auth.need_login
def logout(request):
    """
        logout
    :param request:
    :return:
    """
    try:
        request.session.clear()
        return resp.success(hint.MSG_LOGOUT_SUCCESS)
    except Exception as e:
        return resp.failure(e);