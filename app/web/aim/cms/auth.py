"""
     authority control
"""
import re
from django.shortcuts import redirect

from cms import forms, hint, models, cfg

class Sid:
    UID = 'g_uid'
    UNAME = 'g_uname'
    UMODULES = 'g_umodules'

sid = Sid


class User:
    @staticmethod
    def id(request, id=None):
        """
            get user id
        :param request:
        :return:
        """
        if id is not None:
            request.session[sid.UID] = id
        else:
            return request.session.get(sid.UID)

    @staticmethod
    def name(request, name=None):
        """
            get user name
        :param request:
        :return:
        """
        if name is not None:
            request.session[sid.UNAME] = name
        else:
            return request.session.get(sid.UNAME)

    @staticmethod
    def modules(request, mobjs=None):
        """
            get admin authorized modules
        :return:
        """
        if mobjs is not None:
            request.session[sid.UMODULES] = user.build_modules(mobjs)
        else:
            return request.session.get(sid.UMODULES)

    @staticmethod
    def parents(request, mcode=None):
        """

        :param request:
        :param mcode:
        :return:
        """
        return user._parents(user.modules(request), mcode)

    @staticmethod
    def _parents(modules, mcode):
        """

        :param modules:
        :param mcode:
        :return:
        """
        parents = {}

        for mdl in modules:
            # compare current
            parents[mdl['id']] = mdl
            if mdl['code'] == mcode:
                return parents

            # find childs
            results = user._parents(mdl['childs'], mcode)
            if len(results) > 0:
                parents.update(results)
                return parents

            # find next
            parents.pop(mdl['id'])

        return parents


    @staticmethod
    def has_module(request):
        """

        :param modules:
        :return:
        """
        modules = request.session.get(sid.UMODULES)
        return user._has_module(modules, request.path)

    @staticmethod
    def _has_module(modules, path):
        """

        :param modules:
        :param path:
        :return:
        """
        for module in modules:
            # compare current
            cpath = module['path']
            if cpath and re.match(cpath, path):
                return True

            # compare childs
            childs = module['childs']
            if childs is not None and user._has_module(childs, path):
                return True

        return False

    @staticmethod
    def build_modules(mobjs, parent=None):
        """

        :param mobjs:
        :return:
        """
        # child modules of parent
        childs = []

        # filter child modules
        for obj in mobjs:
            if obj.parent_id == parent:
                child = {'id': obj.id,
                         'parent': obj.parent_id,
                         'code': obj.code,
                         'name': obj.name,
                         'path': obj.path,
                         'icon': obj.icon,
                         'order': obj.order,
                         'disable': obj.disable,
                         'ctime': obj.ctime,
                         'childs': []}

                childs.append(child)

        # sort child modules by order
        childs.sort(key=lambda x: x['order'], reverse=True)

        # process child's child modules
        for child in childs:
            schilds = user.build_modules(mobjs, child['id'])
            child['childs'].extend(schilds)

        return childs


user = User


def protect(func):
    def _has_auth(request):
        if is_login(request):
            if user.has_module(request):
                return func(request)
            return redirect('cms.index')
        else:
            return redirect('cms.login')
    return _has_auth


def has_login(func):
    """
        login authority decorator
    :param request:
    :return:
    """
    def _has_login(request):
        if is_login(request):
            # go on with request
            return func(request)
        else:
            # goto login
            return redirect('cms.login')
    return _has_login


def is_login(request):
    """
        check login status
    :return:
    """
    uid = user.id(request)
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
        login_form = forms.auth.admin.Login(request.POST)
        if login_form.is_valid():
            # get login data form user input
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            remember = login_form.cleaned_data.get('remember')

            # super admin login
            if username == cfg.super_admin['user']:
                if password == cfg.super_admin['password']:
                    # set session expire for not remember choice
                    if not remember:
                        request.session.set_expiry(0)

                    # get user modules
                    mobjs = models.Module.objects.filter(disable=False).all()

                    # set user session
                    user.id(request, cfg.super_admin['id'])
                    user.name(request, cfg.super_admin['name'])
                    user.modules(request, mobjs)

                    return True, hint.MSG_LOGIN_SUCCESS
                else:
                    return False, hint.ERR_LOGIN_PASSWORD

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

                # get user modules
                mobjs = models.Module.objects.filter(authority__admin_id=admin.id, authority__disable=False, disable=False).all()

                # set user session
                user.id(request, admin.id)
                user.name(request, admin.user)
                user.modules(request, mobjs)

                return True, hint.MSG_LOGIN_SUCCESS
            else:
                return False, hint.ERR_LOGIN_PASSWORD
        else:
            return False, hint.ERR_LOGIN_INPUT
    except models.Admin.DoesNotExist:
        return False, hint.ERR_LOGIN_USER
    except Exception as e:
        return False, hint.ERR_EXCEPTION


def logout(request):
    """
        administrator logout
    :return:
    """
    # clear session
    request.session.clear()
