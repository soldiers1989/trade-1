from django.shortcuts import render, redirect

from cms import auth, config


class Ctx:
    @staticmethod
    def default(request):
        # user not login
        if not auth.is_login(request):
            return config.default_context

        # user has login
        ctx = {
            'userid': auth.user.id(request),
            'username': auth.user.name(request),
            'modules': auth.user.modules(request)
        }

        ctx.update(config.default_context)

        return ctx

ctx = Ctx


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
    return redirect(request, 'cms.login')


@auth.has_login
def index(request):
    """
        administrator index page
    :param request:
    :return:
    """
    return render(request, 'index.html', context=ctx.default(request))


@auth.has_auth
def admin_list(request):
    """

    :param request:
    :return:
    """
    return render(request, 'admin.html', context=ctx.default(request))

@auth.has_auth
def module_list(request):
    """

    :param request:
    :return:
    """
    return render(request, 'module.html', context=ctx.default(request))