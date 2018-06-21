"""
    api for cms
"""
import time, util

from adb import models
from cms import auth, resp, forms


@auth.need_login
def list(request):
    """
        list api
    :param request:
    :return:
    """
    try:
        items = models.Module.objects.all()

        rows = []
        for item in items:
            row = item.dict()
            if(item.parent):
                row['_parentId'] = row['parent']
            rows.append(row)

        data = {
            'total': items.count(),
            'rows': rows
        }

        return resp.success(data=data)
    except Exception as e:
        return resp.failure(str(e))


@auth.need_login
def tree(request):
    """

    :param request:
    :return:
    """
    try:
        items = models.Module.objects.all()

        rows = []
        for item in items:
            row = item.dict()
            if (item.parent):
                row['_parentId'] = row['parent']
            row['text'] = row['name']

            rows.append(row)

        data = util.tree.make(rows)

        return resp.success(data=data)
    except Exception as e:
        return resp.failure(str(e))


@auth.need_login
def get(request):
    """
        get api
    :param request:
    :return:
    """
    try:
        id = request.POST['id']
        item = models.Module.objects.get(id=id)
        return resp.success(data=item.dict())
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
        form = forms.auth.module.Add(request.POST)
        if form.is_valid():
            params = form.cleaned_data
            order = models.Module.objects.count()+1
            item = models.Module(parent_id=params['parent'],
                                name=params['name'],
                                path=params['path'],
                                order=order,
                                disable=params['disable'],
                                ctime=int(time.time()));
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
        form = forms.auth.module.Add(request.POST)
        if form.is_valid():
            params = form.cleaned_data

            module = models.Module.objects.filter(id=params['id'])
            module.update(parent_id=params['parent'], name=params['name'], path=params['path'], disable=params['disable'], ctime=int(time.time()));

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
        form = forms.auth.module.Delete(request.POST)
        if form.is_valid():
            id = form.cleaned_data['id']
            models.Module.objects.filter(id=id).delete()
            return resp.success()
        else:
            return resp.failure(form.errors)

    except Exception as e:
        return resp.failure(str(e))
