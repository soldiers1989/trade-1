from django.urls import reverse
from django.shortcuts import render, redirect

from cms import auth, config


class Ctx:
    @staticmethod
    def default(request, mpath=None):
        # user not login
        if not auth.is_login(request):
            return config.default_context



        # user has login
        ctx = {
            'userid': auth.user.id(request),
            'username': auth.user.name(request),
            'modules': auth.user.modules(request),
            'actives': auth.user.parents(request, mpath)
        }

        ctx.update(config.default_context)

        return ctx

ctx = Ctx


def test(request):
    """
        administrator login
    :param request:
    :return:
    """
    return render(request, 'test.html', context=ctx.default(request))


def login(request):
    """
        administrator login
    :param request:
    :return:
    """
    # user has login, logout first
    if auth.is_login(request):
        auth.logout(request)

    # user has not login
    return render(request, 'login.html', context=ctx.default(request))


def logout(request):
    """
        administrator logout
    :param request:
    :return:
    """
    # logout if user has logint
    if auth.is_login(request):
        auth.logout(request)

    # goto login page
    return redirect('cms.login')


@auth.has_login
def index(request):
    """
        administrator index page
    :param request:
    :return:
    """

    return render(request, 'index.html', context=ctx.default(request, 'cms.index'))


@auth.has_auth('cms.auth.admin.list')
def auth_admin_list(request):
    """

    :param request:
    :return:
    """
    return render(request, 'auth/admin/list.html', context=ctx.default(request, 'cms.auth.admin.list'))


@auth.has_auth('cms.auth.module.list')
def auth_module_list(request):
    """

    :param request:
    :return:
    """
    return render(request, 'module.html', context=ctx.default(request, 'cms.auth.module.list'))


@auth.has_auth('cms.order.order.list')
def order_order_list(request):
    """

    :param request:
    :return:
    """
    return render(request, 'order.html', context=ctx.default(request, 'cms.order.order.list'))
