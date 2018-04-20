from django.shortcuts import render, redirect

from cms import auth, context


def login(request):
    """
        administrator login
    :param request:
    :return:
    """
    # user has login
    if auth.has_login(request):
        return redirect('cms.index')

    # user has not login
    return render(request, 'login.html', context=context.extend())


def logout(request):
    """
        administrator logout
    :param request:
    :return:
    """
    # logout
    auth.logout(request)

    # goto login page
    return redirect('cms.login')


@auth.has_auth
def index(request):
    """
        administrator index page
    :param request:
    :return:
    """
    return render(request, 'index.html', context=context.extend())
