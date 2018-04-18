from django.shortcuts import render

from cms import auth, config


def extend_context(context = None):
    """
        extend context with default common context
    :param context:
    :return:
    """
    if context is None:
        return config.default_context

    return context.update(config.default_context)


def login(request):
    """
        administrator login
    :param request:
    :return:
    """
    # user has not login


    # user has login

    # login checking

    return render(request, 'login.html', context=extend_context())


def logout(request):
    """
        administrator logout
    :param request:
    :return:
    """


@auth.check_auth
def index(request):
    """
        administrator index page
    :param request:
    :return:
    """
    context = {'pagename':'index', 'platform':'test', 'username':'polly', 'modulename':'abc', 'submodule':'efg'}

    return render(request, 'index.html', context=context)
