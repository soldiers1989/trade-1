from django.shortcuts import render

from adb import models
from cms import auth


def login(request):
    """
        administrator index page
    :param request:
    :return:
    """
    return render(request, 'login.html')


@auth.need_login
def index(request):
    """
        administrator index page
    :param request:
    :return:
    """
    # get user id from session
    user = request.session.get('user');

    # get user model
    admin = models.Admin.objects.get(id=user['id'])

    # get user modules
    modules = admin.modules.filter(disable=False).order_by('order')

    # context data
    data = []

    # get parent modules
    for m in modules:
        if m.parent is None:
            data.append(m.dict())

    # set child modules
    for p in data:
        p['childs'] = []
        for m in modules:
            if m.parent_id == p['id']:
                p['childs'].append(m.dict())

    return render(request, 'index.html', context={'name': admin.name, 'modules': data})


@auth.need_login
def header(request):
    """
        get header
    :param request:
    :return:
    """
    return render(request, 'header.html', context=auth.get_user(request))


@auth.need_login
def footer(request):
    """
        get footer
    :param request:
    :return:
    """
    return render(request, 'footer.html')


@auth.need_login
def menus(request):
    """
        get menu
    :param request:
    :return:
    """

    # get user id from session
    user = request.session.get('user');

    # get user model
    admin = models.Admin.objects.get(id=user['id'])

    # get user modules
    modules = admin.modules.filter(disable=False).order_by('order')

    # context data
    data = []

    # get parent modules
    for m in modules:
        if m.parent is None:
            data.append(m.dict())

    # set child modules
    for p in data:
        p['childs'] = []
        for m in modules:
            if m.parent_id == p['id']:
                p['childs'].append(m.dict())

    return render(request, 'menus.html', context={'modules': data})


@auth.need_login
def welcome(request):
    """
        get header
    :param request:
    :return:
    """
    return render(request, 'welcome.html')
