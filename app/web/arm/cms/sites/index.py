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
    # get admin id from session
    id = auth.get_admin_id(request);

    # get admin
    admin = models.Admin.objects.get(id=id)

    # get modules of admin
    modules, mobjs = [], None
    # get admin roles
    roles = admin.roles.filter(disable=False).all()
    for role in roles:
        if mobjs is None:
            mobjs = role.modules.filter(disable=False).all()
        else:
            mobjs = mobjs | role.modules.filter(disable=False).all()
    # pack modules to session
    for mobj in mobjs:
        modules.append(mobj.dict())

    # save admin modules to session
    auth.set_admin_modules(request, modules)

    # context data
    data = []

    # get parent modules
    for m in modules:
        if m['parent'] is None:
            data.append(m)

    # set child modules
    for p in data:
        p['childs'] = []
        for m in modules:
            if m['parent'] == p['id']:
                p['childs'].append(m)

    return render(request, 'index.html', context={'name': admin.name, 'modules': data})
