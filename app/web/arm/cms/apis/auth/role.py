import time, cube, datetime

from django.db.models import Q
from adb import models
from cms import auth, resp, hint, forms


@auth.need_login
def list(request):
    """
        list api
    :param request:
    :return:
    """
    try:
        roles = models.Role.objects.all()

        total = roles.count()
        rows = []
        for role in roles:
            rows.append(role.dict());

        data = {
            'total': total,
            'rows': rows
        }

        return resp.success(data=data)
    except Exception as e:
        return resp.failure(str(e))


@auth.need_login
def add(request):
    """
        add api
    :param request:
    :return:
    """
    try:
        form = forms.auth.role.Add(request.POST)
        if form.is_valid():
            params = form.cleaned_data

            item = models.Role(name=params['name'],
                                disable=params['disable'],
                                ctime=int(time.time()))
            item.save()
            return resp.success(data=item.dict())
        else:
            return resp.failure(form.errors)
    except Exception as e:
        return resp.failure(str(e))


@auth.need_login
def update(request):
    """
        modify admin
    :param request:
    :return:
    """
    try:
        form = forms.auth.role.Update(request.POST)
        if form.is_valid():
            params = form.cleaned_data

            role = models.Role.objects.filter(id=params['id'])
            role.update(name=params['name'], disable=params['disable'])

            return resp.success()
        else:
            return resp.failure(form.errors)
    except Exception as e:
        return resp.failure(str(e))


@auth.need_login
def delete(request):
    """
        delete api
    :param request:
    :return:
    """
    try:
        form = forms.auth.role.Delete(request.POST)
        if form.is_valid():
            id = form.cleaned_data['id']
            models.Role.objects.filter(id=id).delete()
            return resp.success()
        else:
            return resp.failure(form.errors)
    except Exception as e:
        return resp.failure(str(e))


@auth.need_login
def moduletree(request):
    """

    :param request:
    :return:
    """
    try:
        form = forms.auth.role.Get(request.POST)
        if form.is_valid():
            id = form.cleaned_data['id']

            # get role modules
            mids = []
            rolemodules = models.Module.objects.filter(role__id=id).all()
            for rolemodule in rolemodules:
                mids.append(rolemodule.id)

            # get all modules
            modules = []
            items = models.Module.objects.all()
            for item in items:
                modules.append(item.dict())

            # process data
            nodes = []
            for module in modules:
                module['text'] = module['name']

                if module['id'] in mids and cube.tree.isleaf(module, modules):
                    module['checked'] = True

                nodes.append(module)

            data = cube.tree.make(nodes)

            return resp.success(data=data)
        else:
            return resp.failure(form.errors)
    except Exception as e:
        return resp.failure(str(e))


@auth.need_login
def addmodule(request):
    """

    :param request:
    :return:
    """
    try:
        form = forms.auth.role.AddModule(request.POST)
        if form.is_valid():
            id = form.cleaned_data['id']
            mid = form.cleaned_data['module']

            # get module
            module = models.Module.objects.get(id=mid).dict()

            # get role modules
            mids = []
            rolemodules = models.Module.objects.filter(role__id=id).all()
            for rolemodule in rolemodules:
                mids.append(rolemodule.id)

            # get all modules
            modules = []
            items = models.Module.objects.all()
            for item in items:
                modules.append(item.dict())

            # get module childs
            childs = cube.tree.childids(module, modules)

            # get module parents
            parents = cube.tree.parentids(module, modules)

            # get relate modules for role need to add
            relates = childs+parents+[mid]

            rmodules = []
            # remove modules already related
            for relate in relates:
                if relate not in mids:
                    rmodules.append(models.RoleModule(role_id=id, module_id=relate, ctime=int(time.time())))

            # add new modules
            d = models.RoleModule.objects.bulk_create(rmodules)

            return resp.success()
        else:
            return resp.failure(form.errors)
    except Exception as e:
        return resp.failure(str(e))


@auth.need_login
def delmodule(request):
    """

    :param request:
    :return:
    """
    try:
        form = forms.auth.role.AddModule(request.POST)
        if form.is_valid():
            id = form.cleaned_data['id']
            mid = form.cleaned_data['module']

            # get role
            role = models.Role.objects.get(id=id)

            # get all modules
            modules = []
            items = models.Module.objects.all()
            for item in items:
                modules.append(item.dict())

            # get childs of delete role's module
            childs = cube.tree.childids({'id':mid}, modules)

            # get role module ids need to delete
            mids = childs + [mid]

            # get role modules
            qs = None
            rmodules = models.Module.objects.filter(role__id=id).all()
            for rmodule in rmodules:
                if rmodule.id in mids:
                    if qs is None:
                        qs = Q(module_id=rmodule.id)
                    else:
                        qs = qs | Q(module_id=rmodule.id)

            # delete role modules
            s = role.rolemodule_set.filter(qs).delete()

            return resp.success()
        else:
            return resp.failure(form.errors)
    except Exception as e:
        return resp.failure(str(e))