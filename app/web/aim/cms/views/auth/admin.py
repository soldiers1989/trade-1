from cms import ctx, auth

from django.shortcuts import render, redirect


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


@auth.protect
def list(request):
    """

    :param request:
    :return:
    """
    return render(request, 'auth/admin/list.html', context=ctx.default(request, 'cms.auth.admin.list'))
