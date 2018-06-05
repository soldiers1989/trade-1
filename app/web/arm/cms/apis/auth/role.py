import time, cube, datetime

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


@auth.need_login
def add(request):
    """
        add api
    :param request:
    :return:
    """
    try:
        form = forms.auth.admin.Add(request.POST)
        if form.is_valid():
            params = form.cleaned_data

            item = models.Admin(user=params['user'],
                                pwd=cube.hash.sha1(params['pwd']),
                                name=params['name'],
                                phone=params['phone'],
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
        form = forms.auth.admin.Update(request.POST)
        if form.is_valid():
            params = form.cleaned_data

            models.Admin.objects.filter(id=params['id']).update(name=params['name'],
                                                                phone=params['phone'],
                                                                disable=params['disable'])
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
        form = forms.auth.admin.Delete(request.POST)
        if form.is_valid():
            id = form.cleaned_data['id']
            models.Admin.objects.filter(id=id).delete()
            return resp.success()
        else:
            return resp.failure(form.errors)
    except Exception as e:
        return resp.failure(str(e))

