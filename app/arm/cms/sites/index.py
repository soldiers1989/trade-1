from django.shortcuts import render

from django.db.models import Q

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

    qs = None
    # get admin roles
    roles = admin.roles.filter(disable=False).all()
    for role in roles:
        if qs is None:
            qs = Q(role__id=role.id)
        else:
            qs = qs | Q(role__id=role.id)

    # get admin's modules
    mobjs = models.Module.objects.filter(qs, disable=False).distinct()

    # pack modules to session
    if mobjs is not None:
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
