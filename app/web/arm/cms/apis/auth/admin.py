"""
    api for cms
"""
import time

from adb import models
from cms.apis import resp
from cms import auth, hint, forms


def login(request):
    """
        login api
    :param request:
    :return:
    """
    res, msg = auth.login(request)
    if res:
        return resp.success(message=msg)
    else:
        return resp.failure(message=msg)


@auth.protect
def list(request):
    """
        list api
    :param request:
    :return:
    """
    try:
        items = models.Admin.objects.filter().all()

        data = []

        for item in items:
            data.append(item.dict())

        return resp.success(data=data)
    except Exception as e:
        return resp.failure(str(e))


@auth.protect
def get(request):
    """
        get api
    :param request:
    :return:
    """
    try:
        id = request.POST['id']
        item = models.Admin.objects.get(id=id)
        return resp.success(data=item.dict())
    except Exception as e:
        return resp.failure(str(e))


@auth.protect
def add(request):
    """
        add api
    :param request:
    :return:
    """
    try:
        form = forms.auth.admin.Add(request.POST)
        if form.is_valid():
            item = models.Admin(user=form.cleaned_data['user'],
                                pwd=form.cleaned_data['pwd'],
                                name=form.cleaned_data['name'],
                                phone=form.cleaned_data['phone'],
                                disable=form.cleaned_data['disable'],
                                ctime=int(time.time()));
            item.save()
            return resp.success(data=item.dict())
        else:
            errs = form.errors
            return resp.failure(hint.ERR_FORM_DATA)
    except Exception as e:
        return resp.failure(str(e))


@auth.protect
def modify(request):
    """
        modify admin
    :param request:
    :return:
    """
    try:
        form = forms.auth.admin.Modify(request.POST)
        if form.is_valid():
            id = form.cleaned_data['id']
            models.Admin.objects.filter(id=id).update(name=form.cleaned_data['name'],
                                                      phone=form.cleaned_data['phone'],
                                                      disable=form.cleaned_data['disable']);
            item = models.Admin.objects.get(id=id)
            return resp.success(data=item.dict())
        else:
            return resp.failure(hint.ERR_FORM_DATA)
    except Exception as e:
        return resp.failure(str(e))


@auth.protect
def delete(request):
    """
        delete api
    :param request:
    :return:
    """
    try:
        id = request.POST['id']
        models.Admin.objects.filter(id=id).delete()
        return resp.success()
    except Exception as e:
        return resp.failure(str(e))
