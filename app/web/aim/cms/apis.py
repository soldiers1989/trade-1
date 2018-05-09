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
    admins = models.Admin.objects.filter().all()

    data = []

    for admin in admins:
        data.append( {
            'id': admin.id,
            'user': admin.user,
            'name': admin.name,
            'phone': admin.phone,
            'disable': admin.disable,
            'ctime': admin.ctime
        } )

    return success(data=data)


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
    form = forms.Admin(request.POST)
    if form.is_valid():
        disable = form.cleaned_data['disable']
        item = models.Admin(user=form.cleaned_data['user'],
                            pwd=form.cleaned_data['pwd'],
                            name=form.cleaned_data['name'],
                            phone=form.cleaned_data['phone'],
                            disable=form.cleaned_data['disable']);
        print(item);

        item.save()
        return success()
    else:
        errs = form.errors
        return failure(hint.ERR_FORM_DATA)


def auth_admin_del(request):
    """
        login api
    :param request:
    :return:
    """
    admins = models.Admin.objects.filter().all()

    return success('not exist')


def auth_admin_mod(request):
    """
        login api
    :param request:
    :return:
    """
    admins = models.Admin.objects.filter().all()

    resp = {
        'data': []
    }

    for admin in admins:
        resp['data'].append([admin.admin_id, admin.user, admin.name, admin.phone, admin.disable, admin.ctime])

    content = json.dumps(resp).encode('utf-8')

    return HttpResponse(content, content_type='application/json;charset=utf8')


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
