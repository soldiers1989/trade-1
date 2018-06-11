from cms import auth

from django.shortcuts import render


@auth.need_permit
def admin(request):
    """

    :param request:
    :return:
    """
    return render(request, 'auth/admin.html')


@auth.need_permit
def module(request):
    """

    :param request:
    :return:
    """
    return render(request, 'auth/module.html')


@auth.need_permit
def role(request):
    """

    :param request:
    :return:
    """
    return render(request, 'auth/role.html')