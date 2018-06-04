from django.shortcuts import render

from adb import models
from cms import auth


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
