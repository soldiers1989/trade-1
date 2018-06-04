"""
    api for cms
"""
import time, cube, datetime

from adb import models
from cms import auth, resp, hint, forms


def login(request):
    """
        login
    :param request:
    :return:
    """
    try:
        login_form = forms.auth.admin.Login(request.POST)
        if login_form.is_valid():
            # get login data form user input
            username = login_form.cleaned_data.get('user')
            password = cube.hash.sha1(login_form.cleaned_data.get('pwd'))
            remember = login_form.cleaned_data.get('remember')

            # get user data from database
            admin = models.Admin.objects.get(user=username)

            # check password
            if admin.pwd == password:
                # user has been disabled
                if admin.disable:
                    return False, hint.ERR_LOGIN_DISABLED

                # set session expire for not remember choice
                if not remember:
                    request.session.set_expiry(0)


                # set user session
                request.session['user'] = {
                    'id': admin.id,
                    'name': admin.name,
                }

                return resp.success(hint.MSG_LOGIN_SUCCESS)
            else:
                return resp.failure(hint.ERR_LOGIN_PASSWORD)
        else:
            return resp.failure(hint.ERR_LOGIN_INPUT)
    except Exception as e:
        return resp.failure(e)


@auth.need_login
def logout(request):
    """
        logout
    :param request:
    :return:
    """
    try:
        request.session.clear()
        return resp.success(hint.MSG_LOGOUT_SUCCESS)
    except Exception as e:
        return resp.failure(e);


@auth.need_login
def pwd(request):
    """
        change password
    :param request:
    :return:
    """
    try:
        form = forms.auth.admin.Pwd(request.POST)
        if form.is_valid():
            # get new password
            pwd = cube.hash.sha1(form.cleaned_data['pwd'])
            # get current user
            user = auth.get_user(request)
            # update password
            models.Admin.objects.filter(id=user['id']).update(pwd=pwd)

            #
            return resp.success(hint.MSG_CHANGEPWD_SUCCESS)
        else:
            return resp.failure(hint.ERR_FORM_DATA)
    except Exception as e:
        return resp.failure(e);


@auth.need_login
def list(request):
    """
        list api
    :param request:
    :return:
    """
    try:
        form = forms.auth.admin.List(request.POST)
        if form.is_valid():
            ## form parameters ##
            params = form.cleaned_data

            ## filter results ##
            sdate, edate = params['sdate'], params['edate']
            filters = {}
            if sdate:
                filters['ctime__gte'] = cube.time.utime(sdate)
            if edate:
                filters['ctime__lt'] = cube.time.utime(edate+datetime.timedelta(days=1))
            objects = models.Admin.objects.filter(**filters).all()

            ## search words ##
            words = params['words']
            if words:
                objects = objects.filter(id=words) | objects.filter(user__contains=words) | objects.filter(name__contains=words) | objects.filter(phone__contains=words)


            ## pagination & sort ##
            page, size, sort, order = params['page'], params['rows'], params['sort'], params['order']

            # order #
            if sort and order:
                order = '-' if order=='desc' else ''
                objects = objects.order_by(order+sort)

            # pagination #
            total = objects.count()
            objects = objects[(page-1)*size : size]

            ## make results ##
            rows = []
            for object in objects:
                item = object.dict()
                del item['pwd']
                rows.append(item)

            ## response data ##
            data = {
                'total': total,
                'rows': rows
            }

            return resp.success(data=data)
        else:
            return resp.failure(hint.ERR_FORM_DATA)
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
        item = models.Admin.objects.get(id=id)
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


@auth.need_permit
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


@auth.need_permit
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
