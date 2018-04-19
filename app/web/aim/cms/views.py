from django.shortcuts import render, redirect

from cms import auth, context


def login(request):
    """
        administrator login
    :param request:
    :return:
    """
    if request.method == 'GET':
        # user has login
        if auth.has_login(request):
            return redirect('cms.index')

        # user has not login
        return render(request, 'login.html', context=context.extend())
    elif request.method == 'POST':
        # user login request
        if auth.do_login(request):
            pass
        else:
            pass
    else:
        pass


@auth.has_auth
def logout(request):
    """
        administrator logout
    :param request:
    :return:
    """
    pass


@auth.has_auth
def index(request):
    """
        administrator index page
    :param request:
    :return:
    """
    return render(request, 'index.html', context=context.extend())
