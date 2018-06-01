from django.shortcuts import render, redirect

from cms import auth


def index(request):
    """
        administrator index page
    :param request:
    :return:
    """

    return render(request, 'index.html', context={})


def login(request):
    """
        administrator index page
    :param request:
    :return:
    """
    if request.method == 'GET':
        return render(request, 'login.html', context={})
    elif request.method == 'POST':
        return "abc"
    else:
        return "not support"


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
