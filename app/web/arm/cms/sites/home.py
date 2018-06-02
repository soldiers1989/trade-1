from django.shortcuts import render

from cms import auth


@auth.need_login
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
    return render(request, 'login.html', context={})
