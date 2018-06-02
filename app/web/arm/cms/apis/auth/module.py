"""
    api for cms
"""
import time

from adb import models
from cms.apis import resp
from cms import auth, hint, forms


@auth.need_permit
def list(request):
    """
        list api
    :param request:
    :return:
    """
    try:
        items = models.Module.objects.filter().all()

        data = []

        for item in items:
            data.append(item.dict())

        return resp.success(data=data)
    except Exception as e:
        return resp.failure(str(e))


@auth.need_permit
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


@auth.need_permit
def add(request):
    """
        add api
    :param request:
    :return:
    """
    try:
        form = forms.auth.module.Add(request.POST)
        if form.is_valid():
            item = models.Module(parent_id=form.cleaned_data['parent'],
                                code=form.cleaned_data['code'],
                                name=form.cleaned_data['name'],
                                path=form.cleaned_data['path'],
                                icon=form.cleaned_data['icon'],
                                order=form.cleaned_data['order'],
                                disable=form.cleaned_data['disable'],
                                ctime=int(time.time()));
            item.save()
            return resp.success(data=item.dict())
        else:
            errs = form.errors
            return resp.failure(hint.ERR_FORM_DATA)
    except Exception as e:
        return resp.failure(str(e))


@auth.need_permit
def modify(request):
    """
        modify admin
    :param request:
    :return:
    """
    try:
        form = forms.auth.module.Modify(request.POST)
        if form.is_valid():
            id = form.cleaned_data['id']
            models.Module.objects.filter(id=id).update(parent_id=form.cleaned_data['parent'],
                                                        code=form.cleaned_data['code'],
                                                        name=form.cleaned_data['name'],
                                                        path=form.cleaned_data['path'],
                                                        icon=form.cleaned_data['icon'],
                                                        order=form.cleaned_data['order'],
                                                        disable=form.cleaned_data['disable']);
            item = models.Module.objects.get(id=id)
            return resp.success(data=item.dict())
        else:
            return resp.failure(hint.ERR_FORM_DATA)
    except Exception as e:
        return resp.failure(str(e))


@auth.need_permit
def delete(request):
    """
        delete api
    :param request:
    :return:
    """
    try:
        id = request.POST['id']
        models.Module.objects.filter(id=id).delete()
        return resp.success()
    except Exception as e:
        return resp.failure(str(e))
