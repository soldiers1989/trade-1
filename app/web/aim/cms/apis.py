"""
    api for cms
"""
import json, time

from cms import models
from cms import auth, hint, forms

from django.http import HttpResponse
from django.forms import modelform_factory


def success(message='success', data={}):
    """
        success response
    :param message:
    :param data:
    :return:
    """
    resp = {
        'status': True,
        'message': message,
        'data': data
    }

    resp = json.dumps(resp).encode('utf-8')

    return HttpResponse(resp, content_type='application/json;charset=utf8')


def failure(message='failure', data={}):
    """
        failure response
    :param message:
    :param data:
    :return:
    """
    resp = {
        'status': False,
        'message': message,
        'data': data
    }

    resp = json.dumps(resp).encode('utf-8')

    return HttpResponse(resp, content_type='application/json;charset=utf8')


def login(request):
    """
        login api
    :param request:
    :return:
    """
    res, msg = auth.login(request)
    if res:
        return success(message=msg)
    else:
        return failure(message=msg)


def auth_admin_list(request):
    """
        login api
    :param request:
    :return:
    """
    try:
        admins = models.Admin.objects.filter().all()

        data = []

        for admin in admins:
            data.append(admin.dict())

        return success(data=data)
    except Exception as e:
        return failure(str(e))


def auth_admin_get(request):
    """
        login api
    :param request:
    :return:
    """
    AdminForm = modelform_factory(models.Admin, fields=['admin_id'])
    admins = models.Admin.objects.filter().all()

    resp = {
        'data': []
    }

    for admin in admins:
        resp['data'].append([admin.admin_id, admin.user, admin.name, admin.phone, admin.disable, admin.ctime])

    content = json.dumps(resp).encode('utf-8')

    return HttpResponse(content, content_type='application/json;charset=utf8')


def auth_admin_add(request):
    """
        login api
    :param request:
    :return:
    """
    try:
        form = forms.AdminAdd(request.POST)
        if form.is_valid():
            item = models.Admin(user=form.cleaned_data['user'],
                                pwd=form.cleaned_data['pwd'],
                                name=form.cleaned_data['name'],
                                phone=form.cleaned_data['phone'],
                                disable=form.cleaned_data['disable'],
                                ctime=int(time.time()));
            item.save()
            return success(data=item.dict())
        else:
            errs = form.errors
            return failure(hint.ERR_FORM_DATA)
    except Exception as e:
        return failure(str(e))


def auth_admin_mod(request):
    """
        modify admin
    :param request:
    :return:
    """
    try:
        form = forms.AdminMod(request.POST)
        if form.is_valid():
            id = form.cleaned_data['id']
            models.Admin.objects.filter(id=id).update(name=form.cleaned_data['name'],
                                                      phone=form.cleaned_data['phone'],
                                                      disable=form.cleaned_data['disable']);
            item = models.Admin.objects.get(id=id)
            return success(data=item.dict())
        else:
            errs = form.errors
            return failure(hint.ERR_FORM_DATA)
    except Exception as e:
        return failure(str(e))


def auth_admin_del(request):
    """
        login api
    :param request:
    :return:
    """
    try:
        id = request.POST['id']
        models.Admin.objects.filter(id=id).delete()
        return success()
    except Exception as e:
        return failure(str(e))


def auth_module_list(request):
    """
        login api
    :param request:
    :return:
    """

    modules = models.Module.objects.filter().all()

    resp = {
        'data': []
    }

    for module in modules:
        resp['data'].append([module.module_id, module.name, module.path, module.icon, module.order, module.disable, module.ctime])

    content = json.dumps(resp).encode('utf-8')

    return HttpResponse(content, content_type='application/json;charset=utf8')
