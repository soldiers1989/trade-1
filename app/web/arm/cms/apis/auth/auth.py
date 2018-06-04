"""
    api for cms
"""
import time

from adb import models
from cms import auth, resp, hint, forms


@auth.need_permit
def list(request):
    """
        list api
    :param request:
    :return:
    """
    try:
        items = models.Authority.objects.filter().all()

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
        item = models.Authority.objects.get(id=id)
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
        form = forms.auth.auth.Add(request.POST)
        if form.is_valid():
            item = models.Authority(admin=models.Admin(id=form.cleaned_data['admin']),
                                    module=models.Module(id=form.cleaned_data['module']),
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
        form = forms.auth.auth.Modify(request.POST)
        if form.is_valid():
            id = form.cleaned_data['id']
            models.Authority.objects.filter(id=id).update(admin=form.cleaned_data['admin'],
                                                          module=form.cleaned_data['module'],
                                                          disable=form.cleaned_data['disable']);
            item = models.Authority.objects.get(id=id)
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
        models.Authority.objects.filter(id=id).delete()
        return resp.success()
    except Exception as e:
        return resp.failure(str(e))
