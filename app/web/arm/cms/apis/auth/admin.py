"""
    api for cms
"""
import time, cube, datetime
from django.db.models import Q
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

            # get admin data from database
            admin = models.Admin.objects.get(user=username)

            # check password
            if admin.pwd == password:
                # user has been disabled
                if admin.disable:
                    return resp.failure(hint.ERR_LOGIN_DISABLED)

                # set session expire for not remember choice
                if not remember:
                    request.session.set_expiry(0)

                # save admin id to session
                auth.set_admin_id(request, admin.id)

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
            # get current admin
            id = auth.get_admin_id(request)
            # update password
            models.Admin.objects.filter(id=id).update(pwd=pwd)

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
                tmpobjs = None
                if(words.isdigit()):
                    tmpobjs = objects.filter(id=int(words))

                if(tmpobjs is None or tmpobjs.count() == 0):
                    objects = objects.filter(user__contains=words) | objects.filter(name__contains=words) | objects.filter(phone__contains=words)
                else:
                    objects = tmpobjs;

            ## pagination & sort ##
            page, size, sort, order = params['page'], params['rows'], params['sort'], params['order']

            # order #
            if sort and order:
                order = '-' if order=='desc' else ''
                objects = objects.order_by(order+sort)

            # pagination #
            total = objects.count()

            if page and size:
                objects = objects[(page-1)*size : page*size]

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


@auth.need_login
def resetpwd(request):
    """
        delete api
    :param request:
    :return:
    """
    try:
        form = forms.auth.admin.ResetPwd(request.POST)
        if form.is_valid():
            id = form.cleaned_data['id']
            pwd = cube.hash.sha1(form.cleaned_data['pwd'])

            models.Admin.objects.filter(id=id).update(pwd=pwd)

            return resp.success()
        else:
            return resp.failure(form.errors)
    except Exception as e:
        return resp.failure(str(e))


@auth.need_login
def getroles(request):
    """
        get admin
    :param request:
    :return:
    """
    try:
        form = forms.auth.admin.Get(request.POST)
        if form.is_valid():
            id = form.cleaned_data['id']

            # get admin's roles
            roleids = []
            roles = models.Role.objects.filter(admin__id=id).all()
            for role in roles:
                roleids.append(role.id)

            # get all roles
            roles = models.Role.objects.all()

            total = roles.count()
            rows = []

            for role in roles:
                items = role.dict()

                if role.id in roleids:
                    items['checked'] = True
                else:
                    items['checked'] = False

                rows.append(items);

            data = {
                'total': total,
                'rows': rows
            }

            return resp.success(data=data)
        else:
            roles = models.Role.objects.all()

            total = roles.count()
            rows = []

            for role in roles:
                items = role.dict()
                items['checked'] = False
                rows.append(items);

            data = {
                'total': total,
                'rows': rows
            }
            return resp.success(data=data)
    except Exception as e:
        return resp.failure(str(e))


@auth.need_login
def addroles(request):
    """
        update roles
    :param request:
    :return:
    """
    try:
        form = forms.auth.admin.AddRoles(request.POST)
        if form.is_valid():
            params = form.cleaned_data
            id = params['id']
            roles = params['roles'].split(',')

            adminroles = models.Admin.objects.get(id=id).roles.all()
            for role in roles:
                if not adminroles.filter(id=role).exists():
                    models.AdminRole(admin_id=id, role_id=role, ctime=int(time.time())).save()

            return resp.success()
        else:
            return resp.failure(form.errors)
    except Exception as e:
        return resp.failure(str(e))


@auth.need_login
def delroles(request):
    """
        update roles
    :param request:
    :return:
    """
    try:
        form = forms.auth.admin.AddRoles(request.POST)
        if form.is_valid():
            params = form.cleaned_data
            id = params['id']

            qs = None
            roles = params['roles'].split(',')
            for role in roles:
                if qs is None:
                    qs = Q(role__id=role)
                else:
                    qs = qs | Q(role__id=role)

            admin = models.Admin.objects.get(id=id)
            if qs is not None:
                admin.adminrole_set.filter(qs).delete()

            return resp.success()
        else:
            return resp.failure(form.errors)
    except Exception as e:
        return resp.failure(str(e))
